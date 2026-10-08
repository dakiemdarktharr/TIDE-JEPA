#!/usr/bin/env python3
"""Write a local, evidence-bound release-test amendment for v4.33.

This does not open or score the test split. It only authorizes the subsequent
one-time generation evaluator after checking the corrected validation report.
"""

import argparse
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tide_jepa.experiment import _implementation_identity, _runtime_identity
from tide_jepa.pilot import _read


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def authorize(base, reassessment_path):
    base = Path(base).resolve()
    protocol_path = base / "protocol.json"
    protocol = _read(protocol_path)
    if _read(base / "data_statement.json").get("version") != "vi-en-ai-v4.33":
        raise ValueError("release amendment is restricted to v4.33")
    current = _implementation_identity()
    frozen = protocol.get("implementation_sha256", {})
    changed = {name for name in set(frozen) | set(current)
               if frozen.get(name) != current.get(name)}
    if protocol.get("runtime") != _runtime_identity() or changed != {"pilot.py", "infer.py"}:
        raise ValueError("only pilot.py and its amendment-aware inference identity guard may differ")

    report_path = Path(reassessment_path).resolve()
    report = _read(report_path)
    if (report.get("schema_version") != "v433-semantic-checker-reassessment-v1"
            or report.get("pilot_version") != "vi-en-ai-v4.33"
            or report.get("release_holdout_opened") is not False
            or report.get("human_validated") is not False
            or report.get("phomt_used") is not False
            or report.get("corrected_checker_sha256") != current.get("pilot.py")):
        raise ValueError("checker reassessment provenance is not valid for current code")

    registered = protocol.get("configs", [])
    entries = {entry.get("run"): entry for entry in report.get("runs", [])}
    if len(entries) != len(report.get("runs", [])) or set(entries) != set(registered):
        raise ValueError("reassessment runs do not match every frozen config")
    selected = []
    for name in registered:
        config = _read(base / name)
        output = (base / config["output_dir"]).resolve()
        for suffix in ("generation_metrics.test.json", "generation.test.private.jsonl",
                       "test_metrics.json", "suite_report.json"):
            if (output / suffix).exists():
                raise ValueError("release evidence already exists; preserve it and do not re-authorize")
        entry = entries[name]
        evidence = entry.get("evidence_identity", {})
        identity = {
            "protocol_sha256": sha256(protocol_path),
            "config_sha256": sha256(base / name),
            "checkpoint_sha256": sha256(output / "best.pt"),
            "resolved_run_sha256": sha256(output / "resolved_run.json"),
            "original_metrics_sha256": sha256(output / "generation_metrics.validation.json"),
            "private_validation_generation_sha256": sha256(output / "generation.validation.private.jsonl"),
        }
        if any(evidence.get(key) != value for key, value in identity.items()):
            raise ValueError(f"reassessment evidence does not match frozen run {name}")
        if entry.get("primary"):
            if entry.get("gate") != "pass":
                raise ValueError(f"primary validation gate has not passed for {name}")
            selected.append(name)
    if not selected or len(selected) != len([e for e in entries.values() if e.get("primary")]):
        raise ValueError("no complete primary validation gate evidence")

    amendment = {
        "schema_version": "v433-release-test-amendment-v2",
        "pilot_version": "vi-en-ai-v4.33",
        "purpose": "Authorize test-split scoring after a narrow semantic-checker registration repair and protocol-bound checkpoint identity compatibility; does not alter data, split, thresholds, model, checkpoints, or frozen training identity.",
        "protocol_sha256": sha256(protocol_path),
        "frozen_implementation_sha256": protocol["implementation_sha256"],
        "amended_evaluator_sha256": {key: value for key, value in current.items()
                                     if key in {"pilot.py", "infer.py", "data.py"}},
        "runtime": protocol["runtime"],
        "validation_reassessment": str(report_path.relative_to(base.parents[1]))
        if base.parents[1] in report_path.parents else str(report_path),
        "validation_reassessment_sha256": sha256(report_path),
        "primary_configs": selected,
        "quality_thresholds": protocol["quality_thresholds"],
        "release_holdout_opened": False,
        "human_validated": False,
        "phomt_used": False,
    }
    target = base / "release_test_amendment.v2.json"
    if target.exists():
        raise FileExistsError("release_test_amendment.v2.json already exists; preserve it")
    target.write_text(json.dumps(amendment, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                      encoding="utf-8")
    print(json.dumps({"amendment": str(target), "primary_configs": selected,
                      "release_holdout_opened": False}, ensure_ascii=False, sort_keys=True))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--reassessment", type=Path,
                        default=Path("audits/2026-10-08/v433_validation_checker_reassessment.json"))
    args = parser.parse_args()
    authorize(args.directory, args.reassessment)


if __name__ == "__main__":
    main()
