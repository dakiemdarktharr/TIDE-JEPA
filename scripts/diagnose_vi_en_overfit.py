"""Synthetic train-only overfit diagnostic; reports aggregates, never examples."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile

import torch

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from tide_jepa.config import ModelConfig
from tide_jepa.data import UTF8ByteTokenizer, build_batch, read_jsonl
from tide_jepa.experiment import _parse_inventory
from tide_jepa.model import TIDEJEPA
from tide_jepa.pilot_seed import (FAMILIES_V4, FAMILIES_V42, FAMILIES_V43,
                                  FAMILIES_V44, FAMILIES_V45, FAMILIES_V46,
                                  FAMILIES_V47, FAMILIES_V48)
from tide_jepa.training import Objective, Trainer, compute_loss


def _atomic_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix=".diagnostic.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(value, stream, ensure_ascii=False, sort_keys=True, indent=2)
            stream.write("\n")
        os.replace(temp, path)
    except BaseException:
        try:
            os.unlink(temp)
        except FileNotFoundError:
            pass
        raise


def diagnose(directory, *, steps=300, event="borrow"):
    requested = Path(directory)
    base = (PROJECT_ROOT / requested).resolve() if not requested.is_absolute() else requested.resolve()
    output = base / "diagnostic" / f"overfit-{event}-{steps}-steps.json"
    if output.exists():
        raise FileExistsError("diagnostic evidence already exists; use a new diagnostic version")
    statement = json.loads((base / "data_statement.json").read_text(encoding="utf-8"))
    version = statement.get("version", "").removeprefix("vi-en-ai-")
    family_sets = {"v4": FAMILIES_V4, "v4.1": FAMILIES_V4, "v4.2": FAMILIES_V42,
                   "v4.3": FAMILIES_V43, "v4.4": FAMILIES_V44, "v4.5": FAMILIES_V45,
                   "v4.6": FAMILIES_V46, "v4.7": FAMILIES_V47,
                   "v4.8": FAMILIES_V48}
    families = family_sets.get(version)
    if families is None or event not in {item[0] for item in families["train"]}:
        raise ValueError("overfit diagnostic event must be a train-only family in this pilot version")
    torch.set_num_threads(1)
    tokenizer = UTF8ByteTokenizer()
    proposed = json.loads((base / "inventory.draft.json").read_text(encoding="utf-8"))
    from tide_jepa.schema import Action, Inventory
    actions = tuple(Action(**item) for item in proposed["actions"])
    inventory = Inventory(actions, {lang: frozenset(Action(**a) for a in proposed["proposed_by_language"][lang])
                                    for lang in ("en", "vi")})
    rows = read_jsonl(base / "corpus.draft.jsonl", inventory, languages=("en", "vi"), require_approved=False)
    train_rows = [row for row in rows if row.split_group_id == f"{version}-{event}"]
    from dataclasses import replace
    train_rows = [replace(row, approval_status="approved") for row in train_rows]
    cfg = ModelConfig(vocab_size=tokenizer.vocab_size, action_count=len(actions), width=48, heads=4,
                      layers=2, max_length=192, languages=("en", "vi"))
    batch = build_batch(train_rows, cfg, inventory, device="cpu")
    torch.manual_seed(20261002)
    model = TIDEJEPA(cfg)
    trainer = Trainer(model, inventory, Objective(mode="token_only"), learning_rate=0.001)
    model.eval()
    with torch.no_grad():
        initial_loss, _ = compute_loss(model, batch, inventory, Objective(mode="token_only"))
    model.train()
    for _ in range(steps):
        trainer.step(batch)
    model.eval()
    with torch.no_grad():
        final_loss, _ = compute_loss(model, batch, inventory, Objective(mode="token_only"))
    single_rows = [row for row in train_rows if row.path_id is None]
    generations = []
    by_source_action = {}
    by_action_sources = {}
    for row in single_rows:
        source = torch.tensor([tokenizer.encode(row.source_text)], dtype=torch.long)
        action_id = torch.tensor([inventory.require(row.language, row.action)], dtype=torch.long)
        language_id = torch.tensor([cfg.languages.index(row.language)], dtype=torch.long)
        generated_ids = model.generate(source, action_id, language_id, tokenizer.bos_id, tokenizer.eos_id, 96)[0].tolist()
        try:
            generated = tokenizer.decode(generated_ids)
            valid = True
        except UnicodeDecodeError:
            generated = tokenizer.decode(generated_ids, errors="replace")
            valid = False
        generations.append((generated == row.target_text, valid, row))
        by_source_action.setdefault((row.language, row.source_text), {})[row.action.kind + ":" + row.action.value] = generated
        by_action_sources.setdefault((row.language, row.action.kind + ":" + row.action.value), {})[row.source_text] = generated
    counterfactuals = [(len(set(outputs.values())) > 1, outputs) for outputs in by_source_action.values() if len(outputs) > 1]
    source_sensitivity = [(len(set(outputs.values())) > 1, outputs) for outputs in by_action_sources.values() if len(outputs) > 1]
    per_action = {}
    for exact, valid, row in generations:
        key = f"{row.language}/{row.action.kind}:{row.action.value}"
        score = per_action.setdefault(key, {"n": 0, "exact": 0, "valid_utf8": 0})
        score["n"] += 1
        score["exact"] += int(exact)
        score["valid_utf8"] += int(valid)
    report = {"scope": f"single-event train-only overfit diagnostic on original synthetic {version} draft",
              "preliminary": True, "human_validated": False, "phomt_used": False,
              "event_family_count": 1, "training_edge_records": len(train_rows),
              "training_updates": steps, "width": cfg.width, "layers": cfg.layers,
              "teacher_forced_token_ce_initial": float(initial_loss),
              "teacher_forced_token_ce_final": float(final_loss),
              "train_generation_count": len(generations),
              "train_generation_exact": sum(int(exact) for exact, _, _ in generations),
              "train_generation_valid_utf8": sum(int(valid) for _, valid, _ in generations),
              "per_language_action": per_action,
              "action_counterfactual_pairs": len(counterfactuals),
              "action_counterfactual_distinct": sum(int(distinct) for distinct, _ in counterfactuals),
              "source_counterfactual_groups": len(source_sensitivity),
              "source_counterfactual_distinct": sum(int(distinct) for distinct, _ in source_sensitivity),
              "metric_limit": "Training memorization is a sanity check only; it provides no held-out quality evidence."}
    _atomic_json(output, report)
    print(json.dumps(report, sort_keys=True))
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory")
    parser.add_argument("--steps", type=int, default=300)
    parser.add_argument("--event", default="borrow")
    args = parser.parse_args()
    diagnose(args.directory, steps=args.steps, event=args.event)


if __name__ == "__main__":
    main()
