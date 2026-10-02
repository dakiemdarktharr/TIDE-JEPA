"""Publish aggregate-only results for a frozen synthetic Vi-En pilot."""

import argparse
import json
from pathlib import Path
import statistics


def _rate(scores, numerator, denominator):
    n = sum(score[numerator] for score in scores)
    d = sum(score[denominator] for score in scores)
    return n, d, n / d if d else 0.0


def summarize(directory, destination):
    base = Path(directory).resolve()
    report = json.loads((base / "suite_report.json").read_text(encoding="utf-8"))
    protocol = json.loads((base / "protocol.json").read_text(encoding="utf-8"))
    statement = json.loads((base / "data_statement.json").read_text(encoding="utf-8"))
    groups = json.loads((base / "groups.json").read_text(encoding="utf-8"))
    manifest = json.loads((base / "split_manifest.json").read_text(encoding="utf-8"))
    expected = set(protocol["configs"])
    actual = [r["config"] for r in report["runs"]]
    if len(actual) != len(set(actual)) or set(actual) != expected:
        raise ValueError("suite report has duplicate, missing, or unregistered runs")
    modes = protocol["modes"]
    primary = protocol.get("primary_quality_mode", "tide")
    if primary not in modes:
        raise ValueError("primary quality mode is absent from the registered controls")
    seeds = protocol["seeds"]
    bucket_keys = sorted(report["runs"][0]["generation"]["scores"])
    group_counts = {name: sum(value == name for value in groups.values())
                    for name in ("train", "validation", "test")}
    record_counts = {name: len(values) for name, values in manifest["record_ids"].items()}
    validation_reports = []
    for run in report["runs"]:
        if run["config"].startswith(primary + "-"):
            config = json.loads((base / run["config"]).read_text(encoding="utf-8"))
            output = (base / config["output_dir"]).resolve()
            validation_path = output / "generation_metrics.validation.json"
            if validation_path.is_file():
                validation_reports.append((run["config"], json.loads(validation_path.read_text(encoding="utf-8"))))
    lines = [
        "# TIDE-JEPA preliminary Vi–En pilot results", "",
        "This is an AI-authored and AI-reviewed synthetic pilot. **It is preliminary and has not been human/native-speaker validated.** PhoMT was not used for training; Phan Rang Cham is excluded.", "",
        f"## Frozen {statement['version']} evaluation", "",
        f"The corpus contains {statement['records']} records across {statement['event_families']} meaning frames ({group_counts['train']}/{group_counts['validation']}/{group_counts['test']} train/validation/release-holdout groups; {record_counts['train']}/{record_counts['validation']}/{record_counts['test']} records). Split scope: {statement['split_policy']}. The release holdout was opened once after all {len(expected)} preregistered configurations completed training; these results were not used for tuning.", "",
        f"Four controls, seeds {', '.join(map(str, seeds))}, {protocol['epochs']} epochs and {report['runs'][0]['steps']} updates per run were frozen. Models use width {protocol['model']['width']}, {protocol['model']['heads']} heads and {protocol['model']['layers']} layers. Checkpoints were selected by validation token and path token cross-entropy. Decoder policy: {protocol['decoder_policy']}.", "",
        f"The frozen quality gate applies to primary mode `{primary}` and requires every seed and every language/action bucket to meet the protocol thresholds. Controls are diagnostic comparisons and do not define this gate.", "",
        "| Mode | Test token CE, mean ± SD | Test path token CE, mean ± SD | Accepted refs | Valid Unicode | EOS terminated | Quality gate |", "|---|---:|---:|---:|---:|---:|---|"
    ]
    if validation_reports:
        validation_pass = (len(validation_reports) == len(seeds)
                           and all(value["quality_gate"]["status"] == "pass" for _, value in validation_reports))
        val_scores = [score for _, value in validation_reports for score in value["scores"].values()]
        val_matches, val_examples, _ = _rate(val_scores, "accepted_reference_matches", "examples")
        lines += [f"Validation generation gate across {len(validation_reports)}/{len(seeds)} primary seeds: **{('pass' if validation_pass else 'fail')}**; {val_matches}/{val_examples} accepted-reference matches. This development evidence was read before release-test evaluation.", ""]
    totals = {key: 0 for key in ("examples", "accepted", "unicode", "eos")}
    mode_runs = {}
    for mode in modes:
        runs = [r for r in report["runs"] if r["config"].startswith(mode + "-")]
        if len(runs) != len(seeds):
            raise ValueError(f"expected one run per registered seed for {mode}")
        mode_runs[mode] = runs
        token = [r["test_losses"]["token"] for r in runs]
        path = [r["test_losses"]["path_token"] for r in runs]
        scores = [s for r in runs for s in r["generation"]["scores"].values()]
        matches, count, _ = _rate(scores, "accepted_reference_matches", "examples")
        unicode_count, _, unicode_rate = _rate(scores, "valid_unicode", "examples")
        eos_count, _, eos_rate = _rate(scores, "terminated_eos", "examples")
        gate = "control" if mode != primary else (
            "pass" if all(r["generation"]["quality_gate"]["status"] == "pass" for r in runs) else "fail")
        lines.append(f"| {mode} | {statistics.mean(token):.4f} ± {statistics.stdev(token):.4f} | {statistics.mean(path):.4f} ± {statistics.stdev(path):.4f} | {matches}/{count} | {unicode_count}/{count} ({unicode_rate:.1%}) | {eos_count}/{count} ({eos_rate:.1%}) | **{gate}** |")
        totals["examples"] += count
        totals["accepted"] += matches
        totals["unicode"] += unicode_count
        totals["eos"] += eos_count
    primary_runs = mode_runs[primary]
    quality_pass = (len(primary_runs) == len(seeds)
                    and all(r["generation"]["quality_gate"]["status"] == "pass" for r in primary_runs))
    lines += [
        "", f"Across all runs: **{totals['accepted']}/{totals['examples']} accepted-reference matches**, {totals['unicode']}/{totals['examples']} valid Unicode outputs, {totals['eos']}/{totals['examples']} EOS-terminated outputs. Primary `{primary}` quality gate: **{('pass' if quality_pass else 'fail')}**.", "",
        "## Action fidelity and state preservation", "",
        "Values are pooled across seeds within each mode and bucket. Thresholds are evaluated separately for every bucket; a pooled pass across languages/actions cannot hide a failing bucket.", "",
        "| Mode | Bucket | Action fidelity | Preservation | Accepted refs |", "|---|---|---:|---:|---:|"
    ]
    for mode in modes:
        for key in bucket_keys:
            scores = [r["generation"]["scores"][key] for r in mode_runs[mode]]
            af_n, af_d, af = _rate(scores, "action_fidelity_pass", "action_fidelity_known")
            pr_n, pr_d, _ = _rate(scores, "preservation_pass", "preservation_known")
            ar_n, ar_d, _ = _rate(scores, "accepted_reference_matches", "examples")
            lines.append(f"| {mode} | {key} | {af_n}/{af_d} ({af:.1%}) | {pr_n}/{pr_d} | {ar_n}/{ar_d} |")
    lines += [
        "", "## Interpretation and limits", "",
        "Teacher-forced loss and valid Unicode do not establish semantic correctness. The deterministic checker covers only its declared synthetic present/past and polarity grammar plus named roles; it does not measure naturalness. Shared templates, one target per state, three seeds, CPU-only execution and no matched-FLOP comparison limit conclusions. No human validation, natural-corpus efficacy, or TIDE advantage is established.", "",
        f"This {statement['version']} holdout is frozen. Do not tune against it. PhoMT-derived labels remain a separate data-use and bilingual review gate; Phan Rang Cham remains deferred pending dataset-use permission and language/community review.", "",
        "## Verified engineering scope", "",
        "- The CPU unit suite, compilation and root crash/replay probes are recorded in the current verification note; passing engineering checks do not establish language quality.",
        "- Two independent Luna/high AI reviews and an adjudication are bound to this version. `human_validated` is false.",
        "- Group/frame/exact-text leakage checks, frozen fingerprints, checkpoint/config identity checks and epoch-resume tensor equivalence are covered by the engineering suite.",
        "- PhoMT raw/derived rows and generated examples remain private under Git-ignored `data/` or `runs/`. This report contains aggregate metrics only; no release was performed.",
        "", f"Private aggregate evidence: `{base.name}/suite_report.json` and the versioned protocol/review records in `{base.name}/`. Raw examples, generated rows and model weights are not included in this summary.", ""
    ]
    Path(destination).write_text("\n".join(lines), encoding="utf-8")
    return {"runs": len(report["runs"]), "generated_examples": totals["examples"],
            "accepted_reference_matches": totals["accepted"], "valid_unicode": totals["unicode"],
            "quality_gate": "pass" if quality_pass else "fail"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Summarize aggregate synthetic Vi-En pilot scores")
    parser.add_argument("directory")
    parser.add_argument("destination")
    args = parser.parse_args()
    print(json.dumps(summarize(args.directory, args.destination), sort_keys=True))
