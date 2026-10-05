"""Training-only TIDE-JEPA overfit sanity check; emits aggregate metrics only."""

import argparse
import json
import random
from pathlib import Path
import sys

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tide_jepa.config import ModelConfig
from tide_jepa.data import UTF8ByteTokenizer, build_batch, read_jsonl, read_split_manifest
from tide_jepa.experiment import _parse_inventory
from tide_jepa.model import TIDEJEPA
from tide_jepa.pilot import _semantic_frame_flags
from tide_jepa.training import Objective, Trainer


def run_diagnostic(directory, *, steps=600, seed=613):
    """Overfit one complete training event group and score those same train rows."""
    base = Path(directory).resolve()
    if type(steps) is not int or steps < 1 or type(seed) is not int:
        raise ValueError("steps must be positive and seed must be an integer")
    configs = []
    for path in sorted(base.glob("*seed-17.json")):
        value = json.loads(path.read_text(encoding="utf-8"))
        objective = value.get("objective", {})
        if (objective.get("mode") == "tide" and objective.get("source_copy_weight") == 1.5
                and objective.get("latent_objective_weight") == 0.1
                and value.get("training", {}).get("transition_balance") == "unique_transition"):
            configs.append((path, value))
    if len(configs) != 1:
        raise ValueError("expected exactly one registered v4.18 TIDE train config for seed 17")
    config_path, config = configs[0]
    inventory_value = json.loads((base / config["inventory"]).read_text(encoding="utf-8"))
    inventory = _parse_inventory(inventory_value)
    rows = read_jsonl(base / config["corpus"], inventory, languages=("en", "vi"))
    manifest = read_split_manifest(base / config["frozen_split"], rows, inventory)
    train_ids = set(manifest.record_ids["train"])
    train_rows = [row for row in rows if row.record_id in train_ids]
    if not train_rows or any(manifest.groups[row.split_group_id] != "train" for row in train_rows):
        raise ValueError("training-only split selection failed")

    group_id = train_rows[0].split_group_id
    group_rows = [row for row in train_rows if row.split_group_id == group_id]
    if not group_rows or any(row.record_id not in train_ids for row in group_rows):
        raise ValueError("selected event group is not wholly in train")
    selected = {}
    for row in group_rows:
        if row.path_id is None:
            selected.setdefault((row.language, row.action.kind, row.action.value), row)
    selected_rows = [selected[key] for key in sorted(selected)]
    if len(selected_rows) != 8:
        raise ValueError("expected one single-action train example per language/action")

    tokenizer = UTF8ByteTokenizer()
    settings = config["model"]
    model_config = ModelConfig(
        vocab_size=tokenizer.vocab_size,
        action_count=len(inventory.actions),
        width=settings["width"], heads=settings["heads"], layers=settings["layers"],
        max_length=settings["max_length"], languages=tuple(config["languages"]),
    )
    batch = build_batch(group_rows, model_config, inventory, tokenizer, device="cpu")
    frames = json.loads((base / "semantic_frames.json").read_text(encoding="utf-8"))
    random.seed(seed)
    torch.manual_seed(seed)
    model = TIDEJEPA(model_config)
    objective = Objective(mode="tide", latent_objective_weight=0.1, source_copy_weight=1.5)
    trainer = Trainer(model, inventory, objective, learning_rate=config["training"]["learning_rate"])

    def score_train_examples():
        model.eval()
        counts = {"examples": 0, "action_fidelity_pass": 0, "preservation_pass": 0}
        with torch.inference_mode():
            for row in selected_rows:
                source = torch.tensor([tokenizer.encode(row.source_text)], dtype=torch.long)
                action_id = torch.tensor([inventory.require(row.language, row.action)], dtype=torch.long)
                language_id = torch.tensor([model_config.languages.index(row.language)], dtype=torch.long)
                output = model.generate(source, action_id, language_id, tokenizer.bos_id,
                                        tokenizer.eos_id, 160)[0].tolist()
                generated = tokenizer.decode(output)
                flags = _semantic_frame_flags(generated, row.language, frames[row.target_frame_id])
                if flags is None:
                    raise ValueError("training example is not covered by the semantic checker")
                counts["examples"] += 1
                counts["action_fidelity_pass"] += int(flags["action_fidelity"])
                counts["preservation_pass"] += int(flags["preservation"])
        return counts

    checkpoints = {1, steps}
    checkpoints.update(value for value in (100, 300, 600, 1000) if value <= steps)
    history = []
    initial = score_train_examples()
    for step in range(1, steps + 1):
        values = trainer.step(batch)
        if step in checkpoints:
            history.append({"step": step, "loss": round(values["loss"], 4),
                            "train_semantic": score_train_examples()})
    return {
        "scope": "one v4.18 event group from train only; same train examples scored after repeated optimization",
        "training_group_examples": len(group_rows),
        "scored_single_action_examples": len(selected_rows),
        "initial_train_semantic": initial,
        "training_curve": history,
        "checkpoint_written": False,
        "corpus_rows_loaded_for_split_integrity_validation": True,
        "validation_rows_selected_or_scored": False,
        "release_holdout_rows_selected_or_scored": False,
        "human_validated": False,
        "phomt_used": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pilot_directory")
    parser.add_argument("--steps", type=int, default=600)
    parser.add_argument("--seed", type=int, default=613)
    args = parser.parse_args()
    print(json.dumps(run_diagnostic(args.pilot_directory, steps=args.steps, seed=args.seed),
                     ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
