#!/usr/bin/env python3
"""Create a text-private, stratified sample from v4.33 validation outputs.

The sampled packet is written to /tmp (or an explicitly supplied path). Stdout
contains only its count, stratification, and SHA-256; never prints example text.
The source records come from the train/validation-only reviewer bundle.
"""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tide_jepa.data import read_jsonl
from tide_jepa.pilot import _read
from tide_jepa.schema import Action, Inventory


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("/tmp/v433-ai-review-20261008/validation_sample.jsonl"),
        help="private packet destination; defaults outside the repository",
    )
    args = parser.parse_args()

    base = ROOT / "data/pilot/vi-en-ai-v4.33"
    bundle = base / "review_bundle"
    statement = _read(bundle / "statement.json")
    manifest = _read(bundle / "manifest.json")
    if (statement.get("version") != "vi-en-ai-v4.33"
            or statement.get("human_validated") is not False
            or statement.get("phomt_used") is not False
            or manifest.get("review_scope") != "train-validation-only"):
        raise ValueError("refusing to sample outside the preliminary train/validation bundle")

    inventory_value = _read(bundle / "inventory.json")
    actions = tuple(Action(item["kind"], item["value"])
                    for item in inventory_value["actions"])
    # Validation records are preliminary and intentionally not approved for
    # training; the sampler only needs structural validation of their actions.
    # Preserve the declared action set without treating approval metadata as
    # a training authorization.
    inventory = Inventory(
        actions,
        {language: frozenset(actions) for language in ("en", "vi")},
    )
    split_groups = _read(bundle / "groups.json")
    if set(split_groups.values()) != {"train", "validation"}:
        raise ValueError("review bundle contains unexpected split membership")
    validation_rows = [
        row for row in read_jsonl(
            bundle / "records.jsonl", inventory, languages=("en", "vi"), require_approved=False
        )
        if split_groups.get(row.split_group_id) == "validation"
    ]
    by_record = {row.record_id: row for row in validation_rows if row.path_id is None}
    by_path = {}
    for row in validation_rows:
        if row.path_id is not None:
            by_path.setdefault((row.path_id, row.language), []).append(row)
    for path_rows in by_path.values():
        path_rows.sort(key=lambda row: row.path_step)
    frames = _read(bundle / "semantic_frames.json")

    selection_rng = random.Random(43320261008)
    selected = []
    for seed in (17, 23, 41):
        private_path = ROOT / f"runs/vi-en-ai-v4.33/tide-copy-0p0-seed-{seed}/generation.validation.private.jsonl"
        strata = {}
        with private_path.open("r", encoding="utf-8") as stream:
            for line in stream:
                item = json.loads(line)
                language, task = item.get("language"), item.get("task")
                if language not in {"en", "vi"} or task not in {"single", "held_out_path"}:
                    raise ValueError("unexpected validation-output schema")
                strata.setdefault((language, task), []).append(item)
        if set(strata) != {(lang, task) for lang in ("en", "vi")
                           for task in ("single", "held_out_path")}:
            raise ValueError("validation outputs do not cover the registered strata")
        for (language, task), items in sorted(strata.items()):
            if len(items) < 4:
                raise ValueError("validation stratum is too small for the fixed sample")
            for item in selection_rng.sample(items, 4):
                if task == "single":
                    source_row = by_record.get(item.get("record_id"))
                    if (source_row is None or source_row.language != language
                            or source_row.target_frame_id != item.get("target_frame")):
                        raise ValueError("validation single identity mismatch")
                    source = source_row.source_text
                    actions = [{"kind": source_row.action.kind, "value": source_row.action.value}]
                else:
                    path_rows = by_path.get((item.get("record_id"), language))
                    if (not path_rows or path_rows[0].source_frame_id != item.get("source_frame")
                            or path_rows[-1].target_frame_id != item.get("target_frame")):
                        raise ValueError("validation path identity mismatch")
                    source = path_rows[0].source_text
                    actions = [{"kind": row.action.kind, "value": row.action.value}
                               for row in path_rows]
                selected.append({
                    "seed": seed,
                    "language": language,
                    "task": task,
                    "source": source,
                    "actions": actions,
                    "reference_outputs": item["reference_variants"],
                    "candidate_output": item["generated_text"],
                    "expected_target_frame": frames[item["target_frame"]],
                })

    random.Random(433).shuffle(selected)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    counts = Counter((row["seed"], row["language"], row["task"]) for row in selected)
    with args.output.open("x", encoding="utf-8") as output:
        for number, item in enumerate(selected, start=1):
            item["case"] = f"C{number:03d}"
            output.write(json.dumps(item, ensure_ascii=False) + "\n")
    digest = hashlib.sha256(args.output.read_bytes()).hexdigest()
    print(json.dumps({
        "packet_path": str(args.output),
        "cases": len(selected),
        "strata": len(counts),
        "cases_per_stratum": sorted(set(counts.values())),
        "validation_only": True,
        "release_test_rows_reviewed": False,
        "source_or_generated_text_emitted": False,
        "packet_sha256": digest,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
