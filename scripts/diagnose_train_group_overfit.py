"""Train-only overfit sanity check for a frozen, bundle-scoped Vi-En pilot.

Selects one complete training group from the protocol-bound train/validation
review bundle, optimizes its single-action rows repeatedly, and reports
aggregate checker rates only. It never reads the full corpus or release
holdout, writes a checkpoint, or emits any example text.
"""

import argparse
import hashlib
import json
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.diagnose_train_checkpoint import canonical_hash, load_review_bundle, sha256


def run_diagnostic(directory, *, steps=600, seed=613, groups_to_fit=1):
    if type(steps) is not int or steps < 1 or type(seed) is not int:
        raise ValueError("steps must be positive and seed must be an integer")
    if type(groups_to_fit) is not int or not 1 <= groups_to_fit <= 4:
        raise ValueError("groups_to_fit must be an integer from 1 through 4")
    base = Path(directory).resolve()
    protocol, raw_rows, frames, groups = load_review_bundle(base)
    if base.name != "vi-en-ai-v4.32":
        raise ValueError("this diagnostic is registered for v4.32 only")

    bundle = base / "review_bundle"
    from tide_jepa.data import UTF8ByteTokenizer, build_batch, read_jsonl
    from tide_jepa.experiment import _parse_inventory
    from tide_jepa.schema import EdgePair
    from tide_jepa.config import ModelConfig
    from tide_jepa.model import TIDEJEPA
    from tide_jepa.pilot import _semantic_frame_flags
    from tide_jepa.training import Objective, Trainer
    import torch

    config_names = protocol.get("configs", [])
    primary = []
    for name in config_names:
        config = json.loads((base / name).read_text(encoding="utf-8"))
        if (config.get("objective", {}).get("mode") == "tide"
                and config.get("model", {}).get("source_pointer_decoder") is True
                and name.endswith("seed-17.json")):
            primary.append((name, config))
    if len(primary) != 1:
        raise ValueError("expected one registered v4.32 primary source-pointer config")
    config_name, config = primary[0]
    if protocol.get("config_files_sha256", {}).get(config_name) != sha256(base / config_name):
        raise ValueError("primary config hash differs from frozen protocol")
    inventory_path = base / config["inventory"]
    inventory_value = json.loads(inventory_path.read_text(encoding="utf-8"))
    review_inventory = json.loads((bundle / "inventory.json").read_text(encoding="utf-8"))
    if inventory_value.get("actions") != review_inventory.get("actions"):
        raise ValueError("registered action inventory differs from the reviewed bundle")
    inventory = _parse_inventory(inventory_value)
    approval_path = base / config["review_gate"]
    approval = json.loads(approval_path.read_text(encoding="utf-8"))
    review_bundle_sha = protocol["review_bundle_sha256"]
    if (protocol.get("approval_sha256") != sha256(approval_path)
            or approval.get("approval_kind") != "AI-preliminary"
            or approval.get("human_validated") is not False
            or approval.get("phomt_used") is not False):
        raise ValueError("preliminary approval identity differs from the frozen protocol")
    if approval.get("inventory_sha256") != canonical_hash(inventory_value):
        raise ValueError("registered inventory differs from frozen preliminary approval")
    review_hashes = approval.get("review_files_sha256", {})
    if set(review_hashes) != {"review-a.json", "review-b.json", "adjudication.json"}:
        raise ValueError("frozen approval lacks both reviews and adjudication")
    for name, digest in review_hashes.items():
        if sha256(base / name) != digest:
            raise ValueError("review or adjudication identity differs from frozen approval")
        review = json.loads((base / name).read_text(encoding="utf-8"))
        if name == "adjudication.json":
            if review.get("decision") != "approve" or review.get("human_validated") is not False:
                raise ValueError("AI adjudication is not an approval for preliminary use")
        elif (review.get("reviewer_type") != "AI"
              or review.get("decision") not in {"approve", "needs-adjudication"}
              or review.get("rows_checked") != protocol.get("reviewed_records")
              or review.get("review_bundle_sha256") != review_bundle_sha):
            raise ValueError("review is not an approved, bundle-bound preliminary review")
    rows = read_jsonl(bundle / "records.jsonl", inventory, languages=("en", "vi"),
                      require_approved=False)
    row_splits = {item["record_id"]: groups[item["split_group_id"]] for item in raw_rows}
    train_rows = [row for row in rows if row_splits.get(row.record_id) == "train" and row.path_id is None]
    if len(train_rows) != sum(1 for item in raw_rows
                              if groups[item["split_group_id"]] == "train" and item.get("path_id") is None):
        raise ValueError("bundle train-row mapping is incomplete")

    by_group = {}
    for row in train_rows:
        by_group.setdefault(row.split_group_id, []).append(row)
    eligible = []
    for group_id, values in by_group.items():
        keys = {(row.language, row.action.kind, row.action.value) for row in values}
        if len(keys) == 8:
            eligible.append(group_id)
    if not eligible:
        raise ValueError("no complete eight-example single-action train group found")
    selected_groups = sorted(eligible, key=lambda value: hashlib.sha256(
        json.dumps([seed, value], separators=(",", ":")).encode()).hexdigest())[:groups_to_fit]
    representatives = []
    for group_id in selected_groups:
        by_key = {}
        for row in by_group[group_id]:
            key = (row.language, row.action.kind, row.action.value)
            current = by_key.get(key)
            rank = lambda item: hashlib.sha256(
                json.dumps([seed, item.record_id], separators=(",", ":")).encode()).hexdigest()
            if current is None or rank(row) < rank(current):
                by_key[key] = row
        if len(by_key) != 8:
            raise ValueError("selected train group lacks one example per language/action bucket")
        representatives.extend(by_key.values())
    from dataclasses import replace
    selected = sorted((replace(row, approval_status="approved") for row in representatives),
                      key=lambda row: (row.split_group_id, row.language, row.action.kind, row.action.value))
    if len(selected) != 8 * groups_to_fit:
        raise ValueError("selected group sample is incomplete")
    selected_ids = {row.record_id for row in selected}

    alignment_value = json.loads((bundle / "alignments.json").read_text(encoding="utf-8"))
    local_index = {row.record_id: index for index, row in enumerate(selected)}
    pairs = tuple(EdgePair(local_index[item["left_record_id"]],
                           local_index[item["right_record_id"]],
                           item.get("relation", "same_event"))
                  for item in alignment_value.get("edge_pairs", [])
                  if item.get("left_record_id") in selected_ids
                  and item.get("right_record_id") in selected_ids)

    settings = config["model"]
    tokenizer = UTF8ByteTokenizer()
    model_config = ModelConfig(
        vocab_size=tokenizer.vocab_size,
        action_count=len(inventory.actions),
        width=settings["width"], heads=settings["heads"], layers=settings["layers"],
        max_length=settings["max_length"], languages=tuple(config["languages"]),
        source_pointer_decoder=settings["source_pointer_decoder"],
    )
    batch = build_batch(selected, model_config, inventory, tokenizer, device="cpu")
    batch = replace(batch, pairs=pairs)
    batch.validate(model_config, inventory)

    random.seed(seed)
    torch.manual_seed(seed)
    torch.set_num_threads(1)
    model = TIDEJEPA(model_config)
    objective = Objective(**config["objective"])
    trainer = Trainer(model, inventory, objective,
                      learning_rate=config["training"]["learning_rate"])

    def score():
        model.eval()
        counts = {"examples": 0, "action_fidelity_pass": 0, "preservation_pass": 0,
                  "predicate_preserved": 0, "patient_preserved": 0, "valid_utf8": 0,
                  "terminated_eos": 0}
        with torch.inference_mode():
            for row in selected:
                source = torch.tensor([tokenizer.encode(row.source_text)], dtype=torch.long)
                action_id = torch.tensor([inventory.require(row.language, row.action)], dtype=torch.long)
                language_id = torch.tensor([model_config.languages.index(row.language)], dtype=torch.long)
                generated_ids = model.generate(source, action_id, language_id, tokenizer.bos_id,
                                               tokenizer.eos_id, 160)[0].tolist()
                generated = tokenizer.decode(generated_ids)
                flags = _semantic_frame_flags(generated, row.language, frames[row.target_frame_id])
                if flags is None:
                    raise ValueError("selected train example lacks semantic-checker coverage")
                counts["examples"] += 1
                counts["action_fidelity_pass"] += int(flags["action_fidelity"])
                counts["preservation_pass"] += int(flags["preservation"])
                counts["predicate_preserved"] += int(flags["predicate_preserved"])
                counts["patient_preserved"] += int(flags["patient_preserved"])
                counts["valid_utf8"] += 1
                counts["terminated_eos"] += int(tokenizer.eos_id in generated_ids)
        return counts

    checkpoints = sorted({1, steps, *(value for value in (100, 300, 600, 1000) if value <= steps)})
    history = [{"step": 0, "train_semantic": score()}]
    for step in range(1, steps + 1):
        loss_values = trainer.step(batch)
        if step in checkpoints:
            history.append({"step": step, "loss": round(float(loss_values["loss"]), 5),
                            "train_semantic": score()})
    return {
        "pilot_version": "vi-en-ai-v4.32",
        "scope": f"{groups_to_fit} complete event group(s), one train single-action row per language/action bucket",
        "groups_fit": groups_to_fit,
        "training_examples": len(selected),
        "review_scope": protocol["review_scope"],
        "protocol_sha256": sha256(base / "protocol.json"),
        "review_bundle_sha256": protocol["review_bundle_sha256"],
        "config": config_name,
        "config_sha256": sha256(base / config_name),
        "inventory_sha256": sha256(inventory_path),
        "approval_sha256": sha256(approval_path),
        "diagnostic_script_sha256": sha256(Path(__file__)),
        "group_id_sha256": [hashlib.sha256(group_id.encode()).hexdigest() for group_id in selected_groups],
        "alignment_pairs_in_batch": len(pairs),
        "steps": steps,
        "seed": seed,
        "training_curve": history,
        "checkpoint_written": False,
        "validation_rows_scored": False,
        "release_holdout_opened": False,
        "human_validated": False,
        "phomt_used": False,
        "cham_used": False,
        "text_emitted": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pilot_directory")
    parser.add_argument("--steps", type=int, default=600)
    parser.add_argument("--seed", type=int, default=613)
    parser.add_argument("--groups", type=int, default=1)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run_diagnostic(args.pilot_directory, steps=args.steps, seed=args.seed,
                            groups_to_fit=args.groups)
    encoded = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")


if __name__ == "__main__":
    main()
