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
            "source_copy_weight": config["objective"].get("source_copy_weight", 0.0),
            "latent_objective_weight": (config["objective"].get("latent_objective_weight", 1.0)
                                        if config["objective"]["mode"] == "tide" else None),
            "transition_balance": config.get("training", {}).get("transition_balance", "row_uniform"),
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
    actual_weights = {item["source_copy_weight"] for item in primary_runs}
    primary_weights = ({float(weight) for weight in protocol["primary_source_copy_weights"]}
                       if "primary_source_copy_weights" in protocol else actual_weights)
    primary_latent_weights = protocol.get("primary_latent_objective_weights")
    primary_balances = set(protocol.get("primary_transition_balance_modes", ["row_uniform"]))
    if primary_latent_weights is None:
        expected_primary = {(seed, weight, balance) for seed in seeds for weight in primary_weights
                            for balance in primary_balances}
        actual_primary = {(item["seed"], item["source_copy_weight"], item["transition_balance"])
                          for item in primary_runs}
    else:
        primary_latent_weights = {float(weight) for weight in primary_latent_weights}
        expected_primary = {(seed, weight, latent_weight, balance) for seed in seeds for weight in primary_weights
                            for latent_weight in primary_latent_weights for balance in primary_balances}
        actual_primary = {(item["seed"], item["source_copy_weight"], item["latent_objective_weight"],
                           item["transition_balance"])
                          for item in primary_runs}
    if len(primary_runs) != len(expected_primary) or actual_primary != expected_primary:
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
        f"The corpus has {statement['records']} records and {statement['event_families']} event combinations. Split groups: {group_counts['train']}/{group_counts['validation']}/{group_counts['test']}; records: {record_counts['train']}/{record_counts['validation']}/{record_counts['test']} (train/validation/release holdout). Data split policy: {statement['split_policy']}."
        + (f" Frozen release-holdout scope: {protocol['release_holdout_scope']}" if protocol.get("release_holdout_scope") else "")
        + (f" Transition weighting: {statement['transition_weighting_note']}" if statement.get("transition_weighting_note") else ""), "",
        "Objective conditions: " + "; ".join(
            f"{mode} with source-copy weight {weight:g}" +
            (f" and TIDE latent-objective multiplier {latent:g}" if latent is not None else "") +
            f"; transition balance `{balance}`"
            for mode, weight, latent, balance in sorted({(item["mode"], item["source_copy_weight"], item["latent_objective_weight"], item["transition_balance"])
                                                for item in results}, key=lambda value: (value[0], value[1], value[2] or 0.0, value[3])))
        + f". Seeds {', '.join(map(str, seeds))}; {protocol['epochs']} epochs and {results[0]['updates']} updates/config; width {protocol['model']['width']}, {protocol['model']['heads']} heads, {protocol['model']['layers']} layers. Checkpoints selected using the frozen validation criterion. Decoder: {protocol['decoder_policy']}.", "",
        f"The registered primary objective is `{primary}`. Frozen thresholds: valid Unicode 100%; single-action action fidelity and preservation each ≥90%; held-out-path action fidelity and preservation each ≥80%. Every configured primary weight, seed, and language/action bucket must meet all applicable thresholds.", "",
        f"## Validation result: **{'PASS' if quality_pass else 'FAIL'}**", "",
        "The release holdout was not evaluated and remains sealed.", "",
        "| Mode | Source-copy weight | TIDE aux multiplier | Edge balance | Seed | Val token CE | Val path token CE | Updates | Training wall seconds | Mean examples/sec | Gate |", "|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---|"
    ]
    for item in results:
        gate = item["generation"]["quality_gate"]["status"]
        latent = "—" if item["latent_objective_weight"] is None else f"{item['latent_objective_weight']:g}"
        lines.append(f"| {item['mode']} | {item['source_copy_weight']:g} | {latent} | {item['transition_balance']} | {item['seed']} | {item['last_val_token_ce']:.4f} | {item['last_val_path_token_ce']:.4f} | {item['updates']} | {item['train_wall_seconds']:.1f} | {item['mean_examples_per_second']:.1f} | {gate} |")

    lines += ["", "## Validation generation by condition and bucket", "",
              "Action fidelity and preservation are pooled across seeds within each condition and bucket; thresholds are still checked for every primary condition/seed/bucket. Exact-reference match and CER are synthetic-reference metrics, not human naturalness.", "",
              "| Mode | Source-copy weight | TIDE aux multiplier | Edge balance | Bucket | Action fidelity | Preservation | Accepted references | CER | Unicode | EOS |", "|---|---:|---:|---|---|---:|---:|---:|---:|---:|---:|---|"]
    conditions = sorted({(item["mode"], item["source_copy_weight"], item["latent_objective_weight"], item["transition_balance"])
                         for item in results}, key=lambda value: (value[0], value[1], value[2] or 0.0, value[3]))
    for mode, copy_weight, latent_weight, transition_balance in conditions:
        condition_runs = [item for item in results
                          if item["mode"] == mode and item["source_copy_weight"] == copy_weight
                          and item["latent_objective_weight"] == latent_weight
                          and item["transition_balance"] == transition_balance]
        for bucket in buckets:
            scores = [item["generation"]["scores"][bucket] for item in condition_runs]
            sums = {key: sum(score[key] for score in scores) for key in SCORE_FIELDS}
            action = f"{sums['action_fidelity_pass']}/{sums['action_fidelity_known']}"
            preserve = f"{sums['preservation_pass']}/{sums['preservation_known']}"
            accepted = f"{sums['accepted_reference_matches']}/{sums['examples']}"
            cer = sums["edit_distance"] / sums["reference_characters"] if sums["reference_characters"] else 0.0
            unicode_rate = f"{sums['valid_unicode']}/{sums['examples']}"
            eos_rate = f"{sums['terminated_eos']}/{sums['examples']}"
            latent = "—" if latent_weight is None else f"{latent_weight:g}"
            lines.append(f"| {mode} | {copy_weight:g} | {latent} | {transition_balance} | {bucket} | {action} | {preserve} | {accepted} | {cer:.1%} | {unicode_rate} | {eos_rate} |")

    lines += ["", "## Primary-mode validation diagnostics by seed", "",
              "Counts below preserve the frozen seed-by-seed gate denominator. No generated or reference text is included.", "",
              "| Source-copy weight | TIDE aux multiplier | Edge balance | Seed | Bucket | Action fidelity | Preservation | Accepted references | CER | Unicode | EOS | Failure reason | Bucket gate |",
              "|---:|---:|---|---:|---|---:|---:|---:|---:|---:|---:|---|---|"]
    for item in sorted(primary_runs, key=lambda value: (value["source_copy_weight"], value["latent_objective_weight"] or 0.0, value["transition_balance"], value["seed"])):
        generation = item["generation"]
        checks = generation["quality_gate"]["bucket_checks"]
        for bucket in buckets:
            score = generation["scores"][bucket]
            action = f"{score['action_fidelity_pass']}/{score['action_fidelity_known']}"
            preserve = f"{score['preservation_pass']}/{score['preservation_known']}"
            accepted = f"{score['accepted_reference_matches']}/{score['examples']}"
            cer = (score["edit_distance"] / score["reference_characters"]
                   if score["reference_characters"] else 0.0)
            unicode_rate = f"{score['valid_unicode']}/{score['examples']}"
            eos_rate = f"{score['terminated_eos']}/{score['examples']}"
            bucket_gate = "pass" if all(checks[bucket].values()) else "fail"
            failures = [name for name, passed in checks[bucket].items() if not passed]
            failure_reason = ", ".join(failures) if failures else "—"
            lines.append(f"| {item['source_copy_weight']:g} | {item['latent_objective_weight']:g} | {item['transition_balance']} | {item['seed']} | {bucket} | {action} | {preserve} | {accepted} | {cer:.1%} | {unicode_rate} | {eos_rate} | {failure_reason} | {bucket_gate} |")

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
