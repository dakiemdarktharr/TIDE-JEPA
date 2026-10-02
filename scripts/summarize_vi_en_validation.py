"""Write an aggregate-only report for validation before release-test opening."""

import argparse
import csv
import hashlib
import json
from pathlib import Path
import statistics


SCORE_FIELDS = (
    "examples", "accepted_reference_matches", "valid_unicode", "terminated_eos",
    "action_fidelity_known", "action_fidelity_pass", "preservation_known",
    "preservation_pass", "edit_distance", "reference_characters",
)


def _sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def summarize_validation(directory, destination):
    base = Path(directory).resolve()
    protocol = json.loads((base / "protocol.json").read_text(encoding="utf-8"))
    statement = json.loads((base / "data_statement.json").read_text(encoding="utf-8"))
    groups = json.loads((base / "groups.json").read_text(encoding="utf-8"))
    manifest = json.loads((base / "split_manifest.json").read_text(encoding="utf-8"))
    if protocol.get("primary_quality_mode") not in protocol.get("modes", []):
        raise ValueError("a frozen primary quality mode is required")
    if (base / "suite_report.json").exists():
        raise ValueError("a release-test suite report exists; use the test-result summarizer")
    expected = set(protocol["configs"])
    if len(expected) != len(protocol["configs"]):
        raise ValueError("protocol has duplicate config registrations")

    results = []
    for name in protocol["configs"]:
        config = json.loads((base / name).read_text(encoding="utf-8"))
        output = (base / config["output_dir"]).resolve()
        if (output / "test_metrics.json").exists() or (output / "generation_metrics.json").exists():
            raise ValueError("release-test metrics exist; validation-only report is not applicable")
        generation_path = output / "generation_metrics.validation.json"
        if not generation_path.is_file() or not (output / "best.pt").is_file():
            raise FileNotFoundError("all training and validation generation must finish first")
        generation = json.loads(generation_path.read_text(encoding="utf-8"))
        metrics_path = output / "metrics.csv"
        with metrics_path.open(encoding="utf-8", newline="") as stream:
            metrics = list(csv.DictReader(stream))
        validation_rows = [row for row in metrics if row["split"] == "validation"]
        train_rows = [row for row in metrics if row["split"] == "train"]
        if not validation_rows or not train_rows:
            raise ValueError("training metrics lack train or validation records")
        final_validation = validation_rows[-1]
        steps_per_epoch = int(train_rows[-1]["updates"])
        results.append({
            "config": name,
            "mode": config["objective"]["mode"],
            "seed": config["seed"],
            "generation": generation,
            "last_val_token_ce": float(final_validation["token"]),
            "last_val_path_token_ce": float(final_validation["path_token"]),
            "train_wall_seconds": sum(float(row["seconds"]) for row in train_rows),
            "mean_examples_per_second": statistics.mean(float(row["examples_per_second"]) for row in train_rows),
            "updates": int(config["training"]["epochs"]) * steps_per_epoch,
        })
    if {item["config"] for item in results} != expected:
        raise ValueError("validation evidence does not cover every frozen config")

    modes = protocol["modes"]
    seeds = protocol["seeds"]
    primary = protocol["primary_quality_mode"]
    buckets = sorted(results[0]["generation"]["scores"])
    primary_runs = [item for item in results if item["mode"] == primary]
    if {item["seed"] for item in primary_runs} != set(seeds):
        raise ValueError("primary validation evidence does not cover every frozen seed")
    quality_pass = all(item["generation"]["quality_gate"]["status"] == "pass"
                       for item in primary_runs)
    group_counts = {split: sum(value == split for value in groups.values())
                    for split in ("train", "validation", "test")}
    record_counts = {split: len(values) for split, values in manifest["record_ids"].items()}

    lines = [
        f"# {statement['version']} Vi–En validation results", "",
        "AI-authored and independently AI-reviewed preliminary synthetic pilot. **Not human/native-speaker validated.** PhoMT was not used. Phan Rang Cham remains excluded.", "",
        f"## Frozen protocol", "",
        f"The corpus has {statement['records']} records and {statement['event_families']} event combinations. Split groups: {group_counts['train']}/{group_counts['validation']}/{group_counts['test']}; records: {record_counts['train']}/{record_counts['validation']}/{record_counts['test']} (train/validation/release holdout). Data split policy: {statement['split_policy']}.", "",
        f"Four controls; seeds {', '.join(map(str, seeds))}; {protocol['epochs']} epochs and {results[0]['updates']} updates/config; width {protocol['model']['width']}, {protocol['model']['heads']} heads, {protocol['model']['layers']} layers. Checkpoints selected with validation token and path token CE. Decoder: {protocol['decoder_policy']}.", "",
        f"The registered primary mode is `{primary}`. Its engineering gate requires every seed and every language/action bucket to meet the frozen thresholds.", "",
        f"## Validation result: **{'PASS' if quality_pass else 'FAIL'}**", "",
        "The release holdout was not evaluated and remains sealed.", "",
        "| Mode | Seed | Val token CE | Val path token CE | Updates | Training wall seconds | Mean examples/sec | Gate |", "|---|---:|---:|---:|---:|---:|---:|---|"
    ]
    for item in results:
        gate = item["generation"]["quality_gate"]["status"]
        lines.append(f"| {item['mode']} | {item['seed']} | {item['last_val_token_ce']:.4f} | {item['last_val_path_token_ce']:.4f} | {item['updates']} | {item['train_wall_seconds']:.1f} | {item['mean_examples_per_second']:.1f} | {gate} |")

    lines += ["", "## Validation generation by mode and bucket", "",
              "Action fidelity and preservation are pooled across seeds within each bucket; thresholds are still checked for every seed/bucket. Exact-reference match and CER are synthetic-reference metrics, not human naturalness.", "",
              "| Mode | Bucket | Action fidelity | Preservation | Accepted references | CER | Unicode | EOS |", "|---|---|---:|---:|---:|---:|---:|---:|"]
    mode_summary = {}
    for mode in modes:
        mode_runs = [item for item in results if item["mode"] == mode]
        mode_summary[mode] = {"gate": "control_only" if mode != primary else (
            "pass" if all(item["generation"]["quality_gate"]["status"] == "pass" for item in mode_runs) else "fail")}
        for bucket in buckets:
            scores = [item["generation"]["scores"][bucket] for item in mode_runs]
            sums = {key: sum(score[key] for score in scores) for key in SCORE_FIELDS}
            action = f"{sums['action_fidelity_pass']}/{sums['action_fidelity_known']}"
            preserve = f"{sums['preservation_pass']}/{sums['preservation_known']}"
            accepted = f"{sums['accepted_reference_matches']}/{sums['examples']}"
            cer = sums["edit_distance"] / sums["reference_characters"] if sums["reference_characters"] else 0.0
            unicode_rate = f"{sums['valid_unicode']}/{sums['examples']}"
            eos_rate = f"{sums['terminated_eos']}/{sums['examples']}"
            lines.append(f"| {mode} | {bucket} | {action} | {preserve} | {accepted} | {cer:.1%} | {unicode_rate} | {eos_rate} |")

    lines += ["", "## Limits and interpretation", "",
              "Valid Unicode and EOS termination do not establish semantic correctness. The deterministic checker covers only the declared synthetic tense/polarity grammar and named roles. This benchmark tests recombination of familiar lexical factors; it does not establish naturalness, natural-corpus efficacy, or scientific efficacy. Control results are diagnostic; no TIDE advantage is claimed.", "",
              "All examples and generated outputs remain private under Git-ignored `data/` and `runs/`. This report contains aggregate metrics only. `human_validated` is false. PhoMT raw/derived data and Phan Rang Cham data were not used.", "",
              f"Private aggregate evidence: `{base.name}/protocol.json`, validation generation metrics under `{base.name}`, and associated ignored run artifacts. Protocol SHA-256: `{_sha256(base / 'protocol.json')}`.", ""]
    Path(destination).write_text("\n".join(lines), encoding="utf-8")
    return {"version": statement["version"], "runs": len(results), "quality_gate": "pass" if quality_pass else "fail", "release_test_opened": False}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory")
    parser.add_argument("destination")
    args = parser.parse_args()
    print(json.dumps(summarize_validation(args.directory, args.destination), sort_keys=True))
