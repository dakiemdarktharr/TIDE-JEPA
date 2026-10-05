"""Aggregate-only diagnosis of validation entity/predicate preservation.

Reads private synthetic validation generations and emits only category counts.
Never prints or writes source, reference, or generated text.
"""

import argparse
import hashlib
import json
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from tide_jepa.pilot import _semantic_frame_flags


def diagnose(directory, modes=("tide",), output=None, markdown=None):
    base = Path(directory).resolve()
    statement = json.loads((base / "data_statement.json").read_text(encoding="utf-8"))
    version = statement.get("version")
    frames = json.loads((base / "semantic_frames.json").read_text(encoding="utf-8"))
    results = {}
    for config_path in sorted(base.glob("*-seed-*.json")):
        config = json.loads(config_path.read_text(encoding="utf-8"))
        if config.get("objective", {}).get("mode") not in modes:
            continue
        seed = config["seed"]
        run_dir = (base / config["output_dir"]).resolve()
        private_path = run_dir / "generation.validation.private.jsonl"
        if not private_path.is_file():
            raise FileNotFoundError("private validation generation is missing")
        with private_path.open(encoding="utf-8") as stream:
            for line in stream:
                item = json.loads(line)
                language = item["language"]
                task = item["task"]
                frame = frames[item["target_frame"]]
                semantic = _semantic_frame_flags(item["generated_text"], language, frame)
                bucket = (f"{config['objective']['mode']}/seed-{seed}/"
                          f"copy-{config['objective'].get('source_copy_weight', 0):g}/"
                          f"aux-{config['objective'].get('latent_objective_weight', 1):g}/"
                          f"{language}/{task}/{item.get('action_key', 'aggregate')}")
                counts = results.setdefault(bucket, {
                    "examples": 0, "checker_covered": 0,
                    "action_fidelity_pass": 0, "preservation_pass": 0,
                    "agent_preserved": 0, "patient_preserved": 0,
                    "predicate_preserved": 0, "place_preserved": 0,
                    "place_known": 0,
                })
                counts["examples"] += 1
                if semantic is not None:
                    counts["checker_covered"] += 1
                    counts["action_fidelity_pass"] += int(semantic["action_fidelity"])
                    counts["preservation_pass"] += int(semantic["preservation"])
                    for component in ("agent_preserved", "patient_preserved", "predicate_preserved"):
                        counts[component] += int(semantic[component])
                    if semantic["place_preserved"] is not None:
                        counts["place_known"] += 1
                        counts["place_preserved"] += int(semantic["place_preserved"])
    for counts in results.values():
        denominator = counts["checker_covered"]
        counts["checker_coverage_rate"] = denominator / counts["examples"]
        counts["action_fidelity_rate"] = (counts["action_fidelity_pass"] / denominator
                                           if denominator else None)
        counts["preservation_rate"] = (counts["preservation_pass"] / denominator
                                       if denominator else None)
        for component in ("agent_preserved", "patient_preserved", "predicate_preserved"):
            counts[component + "_rate"] = counts[component] / denominator if denominator else None
        counts["place_preserved_rate"] = (counts["place_preserved"] / counts["place_known"]
                                           if counts["place_known"] else None)
    report = {
        "scope": f"{version} post-hoc aggregate-only rescore of saved validation generations",
        "not_frozen_protocol_evidence": True,
        "human_validated": False,
        "phomt_used": False,
        "source_reference_and_generated_text_emitted": False,
        "aggregate": results,
    }
    summary = {}
    for bucket, counts in results.items():
        mode, _seed, copy_weight, aux_weight, language, task, _action = bucket.split("/", 6)
        key = f"{mode}/{copy_weight}/{aux_weight}/{language}/{task}"
        total = summary.setdefault(key, {"examples": 0, "checker_covered": 0,
                                         "action_fidelity_pass": 0, "preservation_pass": 0,
                                         "agent_preserved": 0, "patient_preserved": 0,
                                         "predicate_preserved": 0, "place_preserved": 0,
                                         "place_known": 0})
        for field in total:
            total[field] += counts[field]
    for counts in summary.values():
        denominator = counts["checker_covered"]
        counts["checker_coverage_rate"] = denominator / counts["examples"]
        counts["action_fidelity_rate"] = (counts["action_fidelity_pass"] / denominator
                                           if denominator else None)
        counts["preservation_rate"] = (counts["preservation_pass"] / denominator
                                       if denominator else None)
        for component in ("agent_preserved", "patient_preserved", "predicate_preserved"):
            counts[component + "_rate"] = counts[component] / denominator if denominator else None
        counts["place_preserved_rate"] = (counts["place_preserved"] / counts["place_known"]
                                           if counts["place_known"] else None)
    report["aggregate_by_condition_language_task"] = summary
    if markdown:
        protocol_sha = hashlib.sha256((base / "protocol.json").read_bytes()).hexdigest()
        lines = [
            f"# {version} post-hoc semantic rescore",
            "",
            "This is a diagnostic rescore of saved validation generations after discovering that the frozen evaluator omitted v4.18 event families. It is **not frozen-protocol gate evidence** and does not authorize opening the release holdout.",
            "",
            "The original evaluator had zero semantic checker coverage (`0/0` action fidelity and preservation denominators). After adding v4.18 coverage to the checker, this rescore covers every saved validation example. Results remain preliminary AI-authored synthetic evidence; `human_validated=false`, `phomt_used=false`.",
            "The component breakdown shows that single-action patient presence is 7.7–22.1% and predicate presence is 5.2–11.2% across conditions; these source-slot and transformation deficits explain much of the low joint-preservation score.",
            "",
            f"Frozen training protocol SHA-256: `{protocol_sha}`.",
            "",
            "| Condition | Language | Task | Examples | Checker coverage | Action fidelity | Agent | Patient | Predicate | Place | All preserved |",
            "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
        for key, counts in sorted(summary.items()):
            mode, copy_weight, aux_weight, language, task = key.split("/")
            fidelity = (f"{counts['action_fidelity_pass']}/{counts['checker_covered']} "
                        f"({counts['action_fidelity_rate']:.1%})")
            preservation = (f"{counts['preservation_pass']}/{counts['checker_covered']} "
                            f"({counts['preservation_rate']:.1%})")
            rates = [counts[f"{field}_rate"] for field in
                     ("agent_preserved", "patient_preserved", "predicate_preserved", "place_preserved")]
            component_cells = [f"{rate:.1%}" if rate is not None else "n/a" for rate in rates]
            lines.append(f"| {mode}, copy {copy_weight.removeprefix('copy-')}, aux {aux_weight.removeprefix('aux-')} | {language} | {task} | {counts['examples']} | {counts['checker_covered']}/{counts['examples']} ({counts['checker_coverage_rate']:.1%}) | {fidelity} | {component_cells[0]} | {component_cells[1]} | {component_cells[2]} | {component_cells[3]} | {preservation} |")
        lines += [
            "",
            "The rescore does not pass the preregistered single-action (≥90%) or held-out-path (≥80%) thresholds. Its post-hoc timing means it is diagnostic only; any follow-up quality gate must use a fresh version with the corrected evaluator frozen before training/evaluation. The release holdout remains sealed.",
            "",
            "To reproduce without printing examples: `.venv/bin/python -B scripts/diagnose_validation_preservation.py data/pilot/vi-en-ai-v4.18 --markdown VI_EN_RESULTS_V4.18_RESCORING.md`.",
            "",
            "The script reads private validation generations but emits only aggregate counts; all private rows and generations remain Git-ignored under `data/` and `runs/`.",
        ]
        destination = Path(markdown)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text("\n".join(lines) + "\n", encoding="utf-8")
    if output:
        destination = Path(output)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                               encoding="utf-8")
    print(json.dumps({"scope": report["scope"], "not_frozen_protocol_evidence": True,
                      "human_validated": False, "phomt_used": False,
                      "source_reference_and_generated_text_emitted": False,
                      "aggregate_by_condition_language_task": summary},
                     ensure_ascii=False, sort_keys=True))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory")
    parser.add_argument("--mode", action="append", default=None)
    parser.add_argument("--output")
    parser.add_argument("--markdown")
    args = parser.parse_args()
    diagnose(args.directory, tuple(args.mode or ("tide",)), args.output, args.markdown)


if __name__ == "__main__":
    main()
