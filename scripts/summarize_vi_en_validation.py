"""Write an aggregate-only report for validation before release-test opening."""

import argparse
import csv
import hashlib
import json
from pathlib import Path
import statistics
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from tide_jepa.pilot import _registered_primary_configs


SCORE_FIELDS = (
    "examples", "accepted_reference_matches", "valid_unicode", "terminated_eos", "nonempty",
    "action_fidelity_known", "action_fidelity_pass", "preservation_known",
    "preservation_pass", "checker_coverage", "edit_distance", "reference_characters",
)


def _sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _canonical_hash(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(",", ":")).encode("utf-8")).hexdigest()


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
    named_configs = []
    for name in protocol["configs"]:
        if _sha256(base / name) != protocol.get("config_files_sha256", {}).get(name):
            raise ValueError("registered config identity changed")
        config = json.loads((base / name).read_text(encoding="utf-8"))
        named_configs.append((name, config))
        output = (base / config["output_dir"]).resolve()
        if (output / "test_metrics.json").exists() or (output / "generation_metrics.json").exists():
            raise ValueError("release-test metrics exist; validation-only report is not applicable")
        generation_path = output / "generation_metrics.validation.json"
        if not generation_path.is_file() or not (output / "best.pt").is_file():
            raise FileNotFoundError("all training and validation generation must finish first")
        generation = json.loads(generation_path.read_text(encoding="utf-8"))
        resolved = json.loads((output / "resolved_run.json").read_text(encoding="utf-8"))
        identity_keys = ("config", "corpus_sha256", "split_sha256", "inventory_sha256",
                         "alignments_sha256", "implementation_sha256", "runtime", "review_approval_sha256")
        identity = {key: resolved[key] for key in identity_keys if key in resolved}
        expected_identity = _canonical_hash({
            "checkpoint_sha256": _sha256(output / "best.pt"),
            "run_sha256": resolved.get("run_sha256"),
            "corpus_sha256": manifest["dataset_sha256"],
            "split_sha256": _canonical_hash(manifest),
            "protocol_sha256": _sha256(base / "protocol.json"),
            "evaluation_split": "validation",
            "evaluator_sha256": {key: value for key, value in protocol["implementation_sha256"].items()
                                 if key in {"pilot.py", "infer.py", "data.py"}},
            "decoder_policy": {"max_new_tokens": protocol["generation_max_new_tokens"],
                               "source_language_equals_target": True},
        })
        if (resolved.get("config") != config or resolved.get("run_sha256") != _canonical_hash(identity)
                or resolved.get("implementation_sha256") != protocol["implementation_sha256"]
                or resolved.get("runtime") != protocol["runtime"]
                or generation.get("evaluation_split") != "validation"
                or generation.get("_evaluation_identity") != expected_identity
                or generation.get("human_validated") is not False):
            raise ValueError("validation report differs from frozen run/checkpoint/protocol identity")
        metrics_path = output / "metrics.csv"
        with metrics_path.open(encoding="utf-8", newline="") as stream:
            metrics = list(csv.DictReader(stream))
        validation_rows = [row for row in metrics if row["split"] == "validation"]
        train_rows = [row for row in metrics if row["split"] == "train"]
        if not validation_rows or not train_rows:
            raise ValueError("training metrics lack train or validation records")
        expected_epochs = list(range(1, protocol["epochs"] + 1))
        if any([int(row["epoch"]) for row in partition] != expected_epochs
               for partition in (train_rows, validation_rows)):
            raise ValueError("training metrics do not contain every registered epoch exactly once")
        final_validation = validation_rows[-1]
        results.append({
            "config": name,
            "mode": config["objective"]["mode"],
            "source_copy_weight": config["objective"].get("source_copy_weight", 0.0),
            "latent_objective_weight": (config["objective"].get("latent_objective_weight", 1.0)
                                        if config["objective"]["mode"] == "tide" else None),
            "transition_balance": config.get("training", {}).get("transition_balance", "row_uniform"),
            "decoder": "source_pointer" if config.get("model", {}).get("source_pointer_decoder", False) else "vocabulary",
            "seed": config["seed"],
            "generation": generation,
            "last_val_token_ce": float(final_validation["token"]),
            "last_train_token_ce": float(train_rows[-1]["token"]),
            "last_val_path_token_ce": float(final_validation["path_token"]),
            "train_wall_seconds": sum(float(row["seconds"]) for row in train_rows),
            "mean_examples_per_second": statistics.mean(float(row["examples_per_second"]) for row in train_rows),
            "updates": sum(int(row["updates"]) for row in train_rows),
        })
    if {item["config"] for item in results} != expected:
        raise ValueError("validation evidence does not cover every frozen config")

    modes = protocol["modes"]
    seeds = protocol["seeds"]
    primary = protocol["primary_quality_mode"]
    buckets = sorted(results[0]["generation"]["scores"])
    if not buckets:
        raise ValueError("validation reports have no scored buckets")
    primary_names = {name for name, _ in _registered_primary_configs(protocol, named_configs)}
    primary_runs = [item for item in results if item["config"] in primary_names]
    if any(set(item["generation"]["scores"]) != set(buckets) for item in results):
        raise ValueError("validation reports have inconsistent bucket coverage")
    quality_pass = all(item["generation"]["quality_gate"]["status"] == "pass"
                       for item in primary_runs)
    checker_coverage_complete = all(
        score.get("checker_coverage") == score.get("examples")
        for item in primary_runs for score in item["generation"]["scores"].values())
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
            f"; transition balance `{balance}`; decoder `{decoder}`"
            for mode, weight, latent, balance, decoder in sorted({(item["mode"], item["source_copy_weight"], item["latent_objective_weight"], item["transition_balance"], item["decoder"])
                                                for item in results}, key=lambda value: (value[0], value[1], value[2] or 0.0, value[3], value[4])))
        + f". Seeds {', '.join(map(str, seeds))}; {protocol['epochs']} epochs and {results[0]['updates']} updates/config; width {protocol['model']['width']}, {protocol['model']['heads']} heads, {protocol['model']['layers']} layers. "
        + (f"The preregistered final epoch was evaluated (`{protocol['checkpoint_selection_policy']}`); validation loss did not select the checkpoint. "
           if protocol.get("checkpoint_selection_policy") == "fixed_final_epoch" else
           "Checkpoints were selected using the frozen validation criterion. ")
        + f"Decoder: {protocol['decoder_policy']}.", "",
        f"The registered primary objective is `{primary}`. Frozen thresholds: "
        f"valid Unicode {protocol['quality_thresholds']['valid_unicode_rate']:.0%}; "
        f"checker coverage {protocol['quality_thresholds'].get('semantic_checker_coverage_rate', 1.0):.0%}; "
        f"single-action fidelity ≥{protocol['quality_thresholds']['single_action_action_fidelity_rate']:.0%} "
        f"and preservation ≥{protocol['quality_thresholds']['single_action_preservation_rate']:.0%}; "
        f"path fidelity ≥{protocol['quality_thresholds']['held_out_path_action_fidelity_rate']:.0%} "
        f"and preservation ≥{protocol['quality_thresholds']['held_out_path_preservation_rate']:.0%}. "
        "Every configured primary condition, seed, and language/action bucket must meet all applicable thresholds.", "",
        ("## Validation result: **PASS**" if quality_pass and checker_coverage_complete else
         "## Validation result: **INVALID / FAIL-CLOSED — semantic checker coverage incomplete**"
         if not checker_coverage_complete else "## Validation result: **FAIL**"), "",
        ("Semantic quality gates are not interpretable because one or more buckets lack complete checker coverage. The gate fails closed and the release holdout remains sealed; `0/0` is an unscored denominator, not a 0% model score. See checker-coverage counts below."
         if not checker_coverage_complete else "Semantic checker coverage is complete across all primary buckets."), "",
        "The release holdout was not evaluated and remains sealed.", "",
        "| Mode | Source-copy weight | TIDE aux multiplier | Edge balance | Decoder | Seed | Train token CE | Val token CE | Val path token CE | Updates | Training wall seconds | Mean examples/sec | Gate |", "|---|---:|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---|"
    ]
    for item in results:
        gate = item["generation"]["quality_gate"]["status"]
        latent = "—" if item["latent_objective_weight"] is None else f"{item['latent_objective_weight']:g}"
        lines.append(f"| {item['mode']} | {item['source_copy_weight']:g} | {latent} | {item['transition_balance']} | {item['decoder']} | {item['seed']} | {item['last_train_token_ce']:.4f} | {item['last_val_token_ce']:.4f} | {item['last_val_path_token_ce']:.4f} | {item['updates']} | {item['train_wall_seconds']:.1f} | {item['mean_examples_per_second']:.1f} | {gate} |")

    lines += ["", "## Validation generation by condition and bucket", "",
              "Action fidelity and preservation are pooled across seeds within each condition and bucket; thresholds are still checked for every primary condition/seed/bucket. Exact-reference match and CER are synthetic-reference metrics, not human naturalness.", "",
              "| Mode | Source-copy weight | TIDE aux multiplier | Edge balance | Decoder | Bucket | Checker coverage | Action fidelity | Preservation | Accepted references | CER | Nonempty | Unicode | EOS |", "|---|---:|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    conditions = sorted({(item["mode"], item["source_copy_weight"], item["latent_objective_weight"], item["transition_balance"], item["decoder"])
                         for item in results}, key=lambda value: (value[0], value[1], value[2] or 0.0, value[3], value[4]))
    for mode, copy_weight, latent_weight, transition_balance, decoder in conditions:
        condition_runs = [item for item in results
                          if item["mode"] == mode and item["source_copy_weight"] == copy_weight
                          and item["latent_objective_weight"] == latent_weight
                          and item["transition_balance"] == transition_balance and item["decoder"] == decoder]
        for bucket in buckets:
            scores = [item["generation"]["scores"][bucket] for item in condition_runs]
            sums = {key: sum(score[key] for score in scores) for key in SCORE_FIELDS}
            action = f"{sums['action_fidelity_pass']}/{sums['action_fidelity_known']}"
            preserve = f"{sums['preservation_pass']}/{sums['preservation_known']}"
            coverage = f"{sums['checker_coverage']}/{sums['examples']}"
            accepted = f"{sums['accepted_reference_matches']}/{sums['examples']}"
            cer = sums["edit_distance"] / sums["reference_characters"] if sums["reference_characters"] else 0.0
            unicode_rate = f"{sums['valid_unicode']}/{sums['examples']}"
            eos_rate = f"{sums['terminated_eos']}/{sums['examples']}"
            nonempty_rate = f"{sums['nonempty']}/{sums['examples']}"
            latent = "—" if latent_weight is None else f"{latent_weight:g}"
            lines.append(f"| {mode} | {copy_weight:g} | {latent} | {transition_balance} | {decoder} | {bucket} | {coverage} | {action} | {preserve} | {accepted} | {cer:.1%} | {nonempty_rate} | {unicode_rate} | {eos_rate} |")

    lines += ["", "## Primary-mode validation diagnostics by seed", "",
              "Counts below preserve the frozen seed-by-seed gate denominator. No generated or reference text is included.", "",
              "| Source-copy weight | TIDE aux multiplier | Edge balance | Decoder | Seed | Bucket | Checker coverage | Action fidelity | Preservation | Accepted references | CER | Unicode | EOS | Failure reason | Bucket gate |",
              "|---:|---:|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---|---|"]
    for item in sorted(primary_runs, key=lambda value: (value["source_copy_weight"], value["latent_objective_weight"] or 0.0, value["transition_balance"], value["decoder"], value["seed"])):
        generation = item["generation"]
        checks = generation["quality_gate"]["bucket_checks"]
        for bucket in buckets:
            score = generation["scores"][bucket]
            action = f"{score['action_fidelity_pass']}/{score['action_fidelity_known']}"
            preserve = f"{score['preservation_pass']}/{score['preservation_known']}"
            coverage = f"{score['checker_coverage']}/{score['examples']}"
            accepted = f"{score['accepted_reference_matches']}/{score['examples']}"
            cer = (score["edit_distance"] / score["reference_characters"]
                   if score["reference_characters"] else 0.0)
            unicode_rate = f"{score['valid_unicode']}/{score['examples']}"
            eos_rate = f"{score['terminated_eos']}/{score['examples']}"
            bucket_gate = "pass" if all(checks[bucket].values()) else "fail"
            failures = [name for name, passed in checks[bucket].items() if not passed]
            if score.get("checker_coverage", 0) != score.get("examples"):
                failures.append("semantic_checker_coverage")
            failure_reason = ", ".join(failures) if failures else "—"
            latent = "—" if item["latent_objective_weight"] is None else f"{item['latent_objective_weight']:g}"
            lines.append(f"| {item['source_copy_weight']:g} | {latent} | {item['transition_balance']} | {item['decoder']} | {item['seed']} | {bucket} | {coverage} | {action} | {preserve} | {accepted} | {cer:.1%} | {unicode_rate} | {eos_rate} | {failure_reason} | {bucket_gate} |")

    lines += ["", "## Limits and interpretation", "",
              "Valid Unicode and EOS termination do not establish semantic correctness. The deterministic checker covers only the declared synthetic tense/polarity grammar and named roles. This benchmark tests recombination of familiar lexical factors; it does not establish naturalness, natural-corpus efficacy, or scientific efficacy. Control results are diagnostic; no TIDE advantage is claimed.", "",
              "All examples and generated outputs remain private under Git-ignored `data/` and `runs/`. This report contains aggregate metrics only. `human_validated` is false. PhoMT raw/derived data and Phan Rang Cham data were not used.", "",
              f"Private aggregate evidence: `{base.name}/protocol.json`, validation generation metrics under `{base.name}`, and associated ignored run artifacts. Protocol SHA-256: `{_sha256(base / 'protocol.json')}`.", ""]
    Path(destination).write_text("\n".join(lines), encoding="utf-8")
    return {"version": statement["version"], "runs": len(results),
            "quality_gate": "pass" if quality_pass and checker_coverage_complete else "fail",
            "evaluation_valid": checker_coverage_complete, "release_test_opened": False}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory")
    parser.add_argument("destination")
    args = parser.parse_args()
    print(json.dumps(summarize_validation(args.directory, args.destination), sort_keys=True))
