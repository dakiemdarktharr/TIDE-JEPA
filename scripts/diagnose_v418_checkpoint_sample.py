"""Compare v4.18 best/latest checkpoints on a small fixed validation sample.

Post-hoc diagnostic only: temporary identities bind the current evaluator, the
sample is not a frozen quality gate, and this script never selects test rows or
prints/saves source, reference, or generated text.
"""

import argparse
import json
import shutil
import sys
import tempfile
from pathlib import Path

import torch

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from tide_jepa.data import read_jsonl, read_split_manifest
from tide_jepa.experiment import (
    _canonical_hash,
    _implementation_identity,
    _parse_inventory,
    _runtime_identity,
)
from tide_jepa.infer import OfflineGenerator
from tide_jepa.pilot import _norm_text, _read, _semantic_frame_flags, validate_review_gate


ARTIFACTS = (
    "approval.json", "corpus.jsonl", "inventory.json", "alignments.json",
    "semantic_frames.json", "split_manifest.json", "inventory.draft.json",
    "alignments.draft.json", "groups.json", "data_statement.json",
    "semantic_frames.draft.json", "review-a.json", "review-b.json",
    "adjudication.json",
)


def _prepare_case(source, original_run, config_path, temporary):
    case = Path(temporary)
    for name in ARTIFACTS:
        shutil.copy2(source / name, case / name)

    # v4.18 predates the corrected semantic checker. Rebind only the temporary
    # diagnostic protocol so the current checker can score these checkpoints.
    protocol = _read(source / "protocol.json")
    protocol["implementation_sha256"] = _implementation_identity()
    protocol["runtime"] = _runtime_identity()
    (case / "protocol.json").write_text(json.dumps(protocol), encoding="utf-8")

    config = _read(config_path)
    config["output_dir"] = "run"
    local_config = case / config_path.name
    local_config.write_text(json.dumps(config), encoding="utf-8")
    inventory = _parse_inventory(_read(case / config["inventory"]))
    rows = read_jsonl(case / config["corpus"], inventory, languages=("en", "vi"))
    manifest = read_split_manifest(case / config["frozen_split"], rows, inventory)
    inventory_sha = _canonical_hash(_read(case / config["inventory"]))
    alignment_sha = _canonical_hash(_read(case / config["alignments"]))
    approval_sha = validate_review_gate(case, config, manifest, inventory_sha, alignment_sha)
    identity = {
        "config": config,
        "corpus_sha256": manifest.dataset_sha256,
        "split_sha256": manifest.sha256,
        "inventory_sha256": inventory_sha,
        "alignments_sha256": alignment_sha,
        "implementation_sha256": _implementation_identity(),
        "runtime": _runtime_identity(),
        "review_approval_sha256": approval_sha,
    }
    run_sha = _canonical_hash(identity)
    output = case / "run"
    output.mkdir()
    (output / "resolved_run.json").write_text(
        json.dumps({**identity, "run_sha256": run_sha}), encoding="utf-8"
    )
    states = {}
    for label in ("best", "latest"):
        state = torch.load(original_run / f"{label}.pt", map_location="cpu", weights_only=True)
        state["run_sha256"] = run_sha
        checkpoint = output / f"{label}.pt"
        torch.save(state, checkpoint)
        states[label] = checkpoint
    return local_config, config, rows, manifest, states


def _sample_requests(rows, manifest, frames, max_per_bucket):
    validation = [row for row in rows if manifest.groups[row.split_group_id] == "validation"]
    references = {}
    for row in validation:
        references.setdefault((row.language, row.target_frame_id), set()).add(row.target_text)

    requests = []
    single_samples = {}
    for row in validation:
        if row.path_id is None:
            key = (row.language, row.action.kind, row.action.value)
            sample = single_samples.setdefault(key, [])
            if len(sample) < max_per_bucket:
                sample.append(row)
    for key, sample in sorted(single_samples.items()):
        for row in sample:
            requests.append((row.language, "single", row.source_text, [row.action],
                             row.target_frame_id, references[(row.language, row.target_frame_id)]))

    paths = {}
    for row in validation:
        if row.path_id is not None:
            paths.setdefault((row.path_id, row.language), []).append(row)
    path_samples = {}
    for (_, language), path_rows in sorted(paths.items()):
        ordered = sorted(path_rows, key=lambda row: row.path_step)
        actions = tuple((row.action.kind, row.action.value) for row in ordered)
        sample = path_samples.setdefault((language, actions), [])
        if len(sample) < max_per_bucket:
            sample.append(ordered)
    for (language, _), samples in sorted(path_samples.items()):
        for ordered in samples:
            requests.append((language, "held_out_path", ordered[0].source_text,
                             [row.action for row in ordered], ordered[-1].target_frame_id,
                             references[(language, ordered[-1].target_frame_id)]))
    return requests


def diagnose(data_dir, runs_dir, config_names, max_per_bucket=2):
    source = Path(data_dir).resolve()
    runs = Path(runs_dir).resolve()
    statement = _read(source / "data_statement.json")
    if statement.get("version") != "vi-en-ai-v4.18" or statement.get("human_validated") is not False:
        raise ValueError("this diagnostic is restricted to the preliminary v4.18 synthetic pilot")
    frames = _read(source / "semantic_frames.json")
    reports = []
    with tempfile.TemporaryDirectory(prefix="tide-v418-checkpoint-sample-") as temporary_root:
        for index, name in enumerate(config_names):
            config_path = source / name
            original_config = _read(config_path)
            run_name = Path(original_config["output_dir"]).name
            original_run = runs / run_name
            case = Path(temporary_root) / f"case-{index}"
            case.mkdir()
            local_config, config, rows, manifest, checkpoints = _prepare_case(
                source, original_run, config_path, case
            )
            requests = _sample_requests(rows, manifest, frames, max_per_bucket)
            for label, checkpoint in checkpoints.items():
                generator = OfflineGenerator(local_config, checkpoint, device="cpu")
                totals = {}
                for language, task, source_text, actions, target_frame, references in requests:
                    response = generator.generate({
                        "source": source_text,
                        "source_language": language,
                        "target_language": language,
                        "actions": [{"kind": action.kind, "value": action.value}
                                    for action in actions],
                        "max_new_tokens": 160,
                    })
                    flags = _semantic_frame_flags(response["generated_text"], language,
                                                  frames[target_frame])
                    bucket = f"{language}/{task}"
                    counts = totals.setdefault(bucket, {
                        "examples": 0, "checker_coverage": 0, "action_fidelity_pass": 0,
                        "preservation_pass": 0, "accepted_reference_match": 0,
                        "valid_unicode": 0,
                    })
                    counts["examples"] += 1
                    counts["valid_unicode"] += int(response["valid_utf8"])
                    counts["accepted_reference_match"] += int(any(
                        _norm_text(response["generated_text"]) == _norm_text(reference)
                        for reference in references
                    ))
                    if flags is not None:
                        counts["checker_coverage"] += 1
                        counts["action_fidelity_pass"] += int(flags["action_fidelity"])
                        counts["preservation_pass"] += int(flags["preservation"])

                aggregate = {}
                for bucket, counts in totals.items():
                    denominator = counts["checker_coverage"]
                    aggregate[bucket] = {
                        "examples": counts["examples"],
                        "checker_coverage": denominator,
                        "action_fidelity": (counts["action_fidelity_pass"] / denominator
                                            if denominator else None),
                        "preservation": (counts["preservation_pass"] / denominator
                                         if denominator else None),
                        "valid_unicode": counts["valid_unicode"] / counts["examples"],
                        "accepted_reference_match": (counts["accepted_reference_match"]
                                                      / counts["examples"]),
                    }
                reports.append({
                    "condition": name,
                    "checkpoint": label,
                    "evaluation_split": "validation",
                    "sample_size": len(requests),
                    "aggregate": aggregate,
                    "not_frozen_gate_evidence": True,
                    "human_validated": False,
                    "phomt_used": False,
                    "private_text_emitted": False,
                })
    return reports


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data_dir")
    parser.add_argument("runs_dir")
    parser.add_argument("--config", action="append", dest="configs")
    parser.add_argument("--max-per-bucket", type=int, default=2)
    args = parser.parse_args()
    if args.max_per_bucket < 1:
        parser.error("--max-per-bucket must be positive")
    configs = args.configs or [
        "tide-aux-0p0-balance-unique_transition-copy-0p0-seed-23.json",
        "tide-aux-0p0-balance-unique_transition-copy-1p5-seed-23.json",
    ]
    print(json.dumps(diagnose(args.data_dir, args.runs_dir, configs, args.max_per_bucket),
                     ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
