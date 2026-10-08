#!/usr/bin/env python3
"""Open the v4.33 release holdout once and write aggregate-only evidence."""

import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import torch

from tide_jepa.pilot import _read, evaluate_generation


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def summarize(report, metrics):
    scores = report["scores"]
    return {
        "evaluation_split": report["evaluation_split"],
        "primary_for_quality_gate": report["primary_for_quality_gate"],
        "quality_gate": report["quality_gate"]["status"],
        "evaluation_identity": metrics["_evaluation_identity"],
        "bucket_checks": report["quality_gate"]["bucket_checks"],
        "buckets": {
            key: {name: value for name, value in score.items()
                  if name not in {"edit_distance", "reference_characters"}}
            | {"character_error_rate": score["character_error_rate"]}
            for key, score in sorted(scores.items())
        },
    }


def main():
    torch.set_num_threads(1)
    base = Path("data/pilot/vi-en-ai-v4.33").resolve()
    protocol = _read(base / "protocol.json")
    results = []
    for name in protocol["configs"]:
        config = _read(base / name)
        run_output = (base / config["output_dir"]).resolve()
        result = evaluate_generation(base / name,
                                     max_new_tokens=protocol["generation_max_new_tokens"],
                                     split="test")
        results.append({
            "config": name,
            "config_sha256": sha256(base / name),
            "checkpoint_sha256": sha256(run_output / "best.pt"),
            "resolved_run_sha256": sha256(run_output / "resolved_run.json"),
            "metrics_sha256": sha256(run_output / "generation_metrics.json"),
            "private_generation_sha256": sha256(run_output / "generation.private.jsonl"),
            **summarize(result, _read(run_output / "generation_metrics.json")),
        })
        print(json.dumps({"completed": name, "quality_gate": result["quality_gate"]["status"],
                          "primary": result["primary_for_quality_gate"]}, sort_keys=True))

    amendment_path = base / "release_test_amendment.v2.json"
    primary = [run for run in results if run["primary_for_quality_gate"]]
    if (len(results) != len(protocol["configs"]) or len(primary) != len(protocol["seeds"])
            or any(run["quality_gate"] != "pass" for run in primary)
            or any(any(value is not True for value in check.values())
                   for run in primary for check in run["bucket_checks"].values())):
        raise ValueError("one or more primary release-holdout buckets failed the frozen quality gate")
    output = {
        "schema_version": "v433-release-holdout-aggregate-v1",
        "pilot_version": "vi-en-ai-v4.33",
        "scope": "sealed release holdout; aggregate metrics only; generated text remains private under ignored runs/",
        "preliminary": True,
        "human_validated": False,
        "phomt_used": False,
        "validation_gate_passed_before_opening": True,
        "release_holdout_opened": True,
        "protocol_sha256": sha256(base / "protocol.json"),
        "release_test_amendment_sha256": sha256(amendment_path),
        "runs": results,
    }
    target = Path("audits/2026-10-08/v433_release_holdout_aggregate.json")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(output, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                      encoding="utf-8")
    print(json.dumps({"aggregate_report": str(target), "runs": len(results),
                      "release_holdout_opened": True}, sort_keys=True))


if __name__ == "__main__":
    main()
