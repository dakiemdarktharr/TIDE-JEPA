#!/usr/bin/env python3
"""Re-score frozen v4.33 validation generations after registering compose433 events.

This deterministic checker repair reads only cached validation generations and
their approved frame metadata. It never regenerates text, reads the release
holdout, or emits private rows or generated text.
"""

import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tide_jepa.data import read_jsonl, read_split_manifest
from tide_jepa.experiment import _parse_inventory
from tide_jepa.pilot import (_edit_distance, _hash_file, _norm_text, _quality_gate_status,
                             _read, _semantic_frame_flags)


def _sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _expected_validation_requests(base, config):
    inventory = _parse_inventory(_read(base / config["inventory"]))
    rows = read_jsonl(base / config["corpus"], inventory, languages=("en", "vi"))
    manifest = read_split_manifest(base / config["frozen_split"], rows, inventory)
    held_out = [row for row in rows if manifest.groups[row.split_group_id] == "validation"]
    expected = []
    for row in held_out:
        if row.path_id is None:
            expected.append({
                "record_id": row.record_id,
                "language": row.language,
                "task": "single",
                "action_key": f"{row.action.kind}:{row.action.value}",
                "target_frame_id": row.target_frame_id,
            })
    paths = {}
    for row in held_out:
        if row.path_id is not None:
            paths.setdefault((row.path_id, row.language), []).append(row)
    for (path_id, language), path_rows in sorted(paths.items()):
        ordered = sorted(path_rows, key=lambda row: row.path_step)
        expected.append({
            "record_id": path_id,
            "language": language,
            "task": "held_out_path",
            "action_key": "+".join(f"{row.action.kind}:{row.action.value}" for row in ordered),
            "target_frame_id": ordered[-1].target_frame_id,
        })
    return expected


def _run_summary(run_name, report, revised_scores, bucket_checks):
    thresholds = report["quality_thresholds"]
    primary = bool(report["primary_for_quality_gate"])
    objective_mode = "tide" if primary else "token_only"
    gate = _quality_gate_status("tide", objective_mode, bucket_checks)
    grouped = {}
    for bucket, checks in bucket_checks.items():
        language, task, _ = bucket.split("/", 2)
        key = f"{language}/{task}"
        group = grouped.setdefault(key, {
            "buckets": 0,
            "failed_buckets": 0,
            "failed_checks": {},
            "minima": {name: [] for name in (
                "valid_unicode_rate", "checker_coverage_rate",
                "action_fidelity_rate", "preservation_rate")},
        })
        group["buckets"] += 1
        failed = [name for name, passed in checks.items() if not passed]
        if failed:
            group["failed_buckets"] += 1
            for name in failed:
                group["failed_checks"][name] = group["failed_checks"].get(name, 0) + 1
        score = revised_scores[bucket]
        for name in group["minima"]:
            value = score.get(name)
            if value is not None:
                group["minima"][name].append(value)
    for group in grouped.values():
        group["minima"] = {
            name: round(min(values), 6) if values else None
            for name, values in group["minima"].items()
        }
    return {"run": run_name, "primary": primary, "gate": gate,
            "bucket_summary": grouped,
            "quality_thresholds": thresholds}


def rescore(directory, output_path):
    base = Path(directory).resolve()
    protocol_path = base / "protocol.json"
    protocol = _read(protocol_path)
    statement = _read(base / "data_statement.json")
    if statement.get("version") != "vi-en-ai-v4.33":
        raise ValueError("this repair is scoped to the frozen v4.33 pilot")
    frames = _read(base / "semantic_frames.json")
    results = []
    for config_name in protocol["configs"]:
        config = _read(base / config_name)
        output = (base / config["output_dir"]).resolve()
        metrics_path = output / "generation_metrics.validation.json"
        private_path = output / "generation.validation.private.jsonl"
        if not metrics_path.is_file() or not private_path.is_file():
            raise FileNotFoundError(f"cached validation evidence missing for {config_name}")
        report = _read(metrics_path)
        if (report.get("evaluation_split") != "validation"
                or report.get("human_validated") is not False
                or report.get("phomt_used") is not False):
            raise ValueError("cached evaluation scope or provenance differs from v4.33 validation")
        expected = _expected_validation_requests(base, config)
        with private_path.open(encoding="utf-8") as stream:
            private = [json.loads(line) for line in stream if line.strip()]
        if len(private) != len(expected):
            raise ValueError(f"cached validation record count mismatch for {config_name}")
        stats = defaultdict(lambda: {
            "examples": 0, "valid_unicode": 0, "checker_coverage": 0,
            "action_fidelity_pass": 0, "action_fidelity_known": 0,
            "preservation_pass": 0, "preservation_known": 0,
            "context_preservation_pass": 0, "context_preservation_known": 0,
        })
        for item, request in zip(private, expected):
            identities = {"record_id": "record_id", "language": "language",
                          "task": "task", "target_frame": "target_frame_id"}
            if any(item.get(item_key) != request[request_key]
                   for item_key, request_key in identities.items()):
                raise ValueError(f"cached validation sequence identity mismatch for {config_name}")
            bucket = f"{request['language']}/{request['task']}/{request['action_key']}"
            total = stats[bucket]
            total["examples"] += 1
            total["valid_unicode"] += int(bool(item.get("valid_utf8")))
            flags = _semantic_frame_flags(item["generated_text"], item["language"],
                                          frames[request["target_frame_id"]])
            if flags is None:
                continue
            total["checker_coverage"] += 1
            total["action_fidelity_known"] += 1
            total["preservation_known"] += 1
            total["action_fidelity_pass"] += int(flags["action_fidelity"])
            total["preservation_pass"] += int(flags["preservation"])
            if flags.get("context_preserved") is not None:
                total["context_preservation_known"] += 1
                total["context_preservation_pass"] += int(flags["context_preserved"])

        if set(stats) != set(report.get("scores", {})):
            raise ValueError(f"cached validation bucket set mismatch for {config_name}")
        revised_scores = json.loads(json.dumps(report["scores"]))
        thresholds = report["quality_thresholds"]
        bucket_checks = {}
        for bucket, total in stats.items():
            score = revised_scores[bucket]
            if score.get("examples") != total["examples"]:
                raise ValueError(f"cached validation bucket count mismatch for {config_name}")
            score["valid_unicode"] = total["valid_unicode"]
            score["valid_unicode_rate"] = total["valid_unicode"] / total["examples"]
            for name in ("checker_coverage", "action_fidelity_pass", "action_fidelity_known",
                         "preservation_pass", "preservation_known", "context_preservation_pass",
                         "context_preservation_known"):
                score[name] = total[name]
            score["checker_coverage_rate"] = total["checker_coverage"] / total["examples"]
            score["action_fidelity_rate"] = (
                total["action_fidelity_pass"] / total["action_fidelity_known"]
                if total["action_fidelity_known"] else None)
            score["preservation_rate"] = (
                total["preservation_pass"] / total["preservation_known"]
                if total["preservation_known"] else None)
            score["context_preservation_rate"] = (
                total["context_preservation_pass"] / total["context_preservation_known"]
                if total["context_preservation_known"] else None)
            task = bucket.split("/", 2)[1]
            prefix = "single_action" if task == "single" else "held_out_path"
            required_fidelity = thresholds.get(f"{prefix}_action_fidelity_rate")
            required_preservation = thresholds.get(f"{prefix}_preservation_rate")
            bucket_checks[bucket] = {
                "valid_unicode_pass": score["valid_unicode_rate"] >= thresholds.get("valid_unicode_rate", 1.0),
                "semantic_checker_coverage_pass": score["checker_coverage_rate"] >= thresholds.get("semantic_checker_coverage_rate", 1.0),
                "action_fidelity_pass": (score["action_fidelity_rate"] is not None
                                          and required_fidelity is not None
                                          and score["action_fidelity_rate"] >= required_fidelity),
                "preservation_pass": (score["preservation_rate"] is not None
                                      and required_preservation is not None
                                      and score["preservation_rate"] >= required_preservation),
            }
        result = _run_summary(config_name, report, revised_scores, bucket_checks)
        result["evidence_identity"] = {
            "protocol_sha256": _sha256(protocol_path),
            "config_sha256": _sha256(base / config_name),
            "checkpoint_sha256": _sha256(output / "best.pt"),
            "resolved_run_sha256": _sha256(output / "resolved_run.json"),
            "original_metrics_sha256": _sha256(metrics_path),
            "private_validation_generation_sha256": _sha256(private_path),
        }
        results.append(result)
    aggregate = {
        "schema_version": "v433-semantic-checker-reassessment-v1",
        "pilot_version": statement["version"],
        "scope": "cached validation generations only; generated text was not changed or emitted",
        "preliminary": True,
        "human_validated": False,
        "phomt_used": False,
        "release_holdout_opened": False,
        "repair": "register compose433 event families in the existing narrow semantic checker",
        "corrected_checker_sha256": _sha256(Path(__file__).resolve().parents[1] / "tide_jepa" / "pilot.py"),
        "runs": results,
    }
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(aggregate, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                           encoding="utf-8")
    summary = [{"run": item["run"], "primary": item["primary"], "gate": item["gate"],
                "bucket_summary": item["bucket_summary"]} for item in results]
    print(json.dumps({"output": str(output_path), "runs": summary,
                      "release_holdout_opened": False}, ensure_ascii=False, sort_keys=True))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path,
                        help="v4.33 data directory under the Git-ignored data/ tree")
    parser.add_argument("--output", type=Path,
                        default=Path("audits/2026-10-08/v433_validation_checker_reassessment.json"))
    args = parser.parse_args()
    rescore(args.directory, args.output)


if __name__ == "__main__":
    main()
