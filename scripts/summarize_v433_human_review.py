#!/usr/bin/env python3
"""Validate two completed v4.33 review forms and emit aggregate-only evidence."""

import argparse
from collections import Counter, defaultdict
import csv
from datetime import date
import json
import math
from pathlib import Path
import statistics


BASE = Path("data/pilot/vi-en-ai-v4.33/human-review")
RATING_FIELDS = {
    "naturalness_1_to_5",
    "meaning_preserved_yes_no_uncertain",
    "action_faithful_yes_no_uncertain",
    "confidence_high_medium_low",
}
IDENTITY_FIELDS = {
    "language", "task", "source_text", "requested_actions",
    "expected_target_frame", "candidate_output",
}


def _load(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        required = {"case_id", *IDENTITY_FIELDS, *RATING_FIELDS, "issues_or_notes"}
        if not reader.fieldnames or not required <= set(reader.fieldnames):
            raise ValueError("review form is missing required columns")
        rows = {}
        for row in reader:
            case = row.get("case_id", "")
            if not case or case in rows:
                raise ValueError("review form has an empty or duplicate case ID")
            rows[case] = row
    if len(rows) != 48:
        raise ValueError("each review form must contain exactly 48 cases")
    return rows


def _validate_pair(forms):
    a, b = forms
    if a.keys() != b.keys():
        raise ValueError("the two forms contain different case IDs")
    for case in a:
        if any(a[case][field] != b[case][field] for field in IDENTITY_FIELDS):
            raise ValueError("the two forms differ in case content or stratification")
        for row in (a[case], b[case]):
            if row["language"] not in {"en", "vi"} or row["task"] not in {"single", "held_out_path"}:
                raise ValueError("a review case has an unknown language or task")
            if row["naturalness_1_to_5"] not in {"1", "2", "3", "4", "5"}:
                raise ValueError("every case needs a naturalness rating from 1 through 5")
            if row["meaning_preserved_yes_no_uncertain"] not in {"yes", "no", "uncertain"}:
                raise ValueError("meaning ratings must be yes, no, or uncertain")
            if row["action_faithful_yes_no_uncertain"] not in {"yes", "no", "uncertain"}:
                raise ValueError("action ratings must be yes, no, or uncertain")
            if row["confidence_high_medium_low"] not in {"high", "medium", "low"}:
                raise ValueError("confidence ratings must be high, medium, or low")


def _nominal_kappa(left, right):
    n = len(left)
    observed = sum(x == y for x, y in zip(left, right)) / n
    left_counts, right_counts = Counter(left), Counter(right)
    expected = sum(left_counts[c] * right_counts[c] for c in set(left_counts) | set(right_counts)) / (n * n)
    return None if math.isclose(expected, 1.0) else round((observed - expected) / (1 - expected), 4)


def _weighted_kappa(left, right):
    n = len(left)
    scale = 4
    observed = sum(((x - y) / scale) ** 2 for x, y in zip(left, right)) / n
    left_counts, right_counts = Counter(left), Counter(right)
    expected = sum(
        left_counts[x] * right_counts[y] * ((x - y) / scale) ** 2
        for x in range(1, 6) for y in range(1, 6)
    ) / (n * n)
    return None if math.isclose(expected, 0.0) else round(1 - observed / expected, 4)


def _reviewer_summary(rows):
    naturalness = [int(row["naturalness_1_to_5"]) for row in rows.values()]
    meaning = [row["meaning_preserved_yes_no_uncertain"] for row in rows.values()]
    action = [row["action_faithful_yes_no_uncertain"] for row in rows.values()]
    confidence = [row["confidence_high_medium_low"] for row in rows.values()]
    return {
        "cases": len(rows),
        "naturalness": {
            "mean": round(statistics.fmean(naturalness), 3),
            "median": statistics.median(naturalness),
            "ratings": {str(k): naturalness.count(k) for k in range(1, 6)},
            "rated_4_or_5": sum(value >= 4 for value in naturalness),
        },
        "meaning_preservation": dict(sorted(Counter(meaning).items())),
        "action_fidelity": dict(sorted(Counter(action).items())),
        "confidence": dict(sorted(Counter(confidence).items())),
    }


def _summarize(a, b):
    metrics = {
        "naturalness": ("naturalness_1_to_5", int, _weighted_kappa),
        "meaning_preservation": ("meaning_preserved_yes_no_uncertain", str, _nominal_kappa),
        "action_fidelity": ("action_faithful_yes_no_uncertain", str, _nominal_kappa),
    }
    agreement = {}
    for name, (field, convert, kappa) in metrics.items():
        left = [convert(a[case][field]) for case in a]
        right = [convert(b[case][field]) for case in a]
        agreement[name] = {
            "exact_agreement_cases": sum(x == y for x, y in zip(left, right)),
            "exact_agreement_rate": round(sum(x == y for x, y in zip(left, right)) / len(left), 4),
            "cohen_kappa": kappa(left, right),
        }

    strata = defaultdict(lambda: [dict(), dict()])
    for index, rows in enumerate((a, b)):
        for case, row in rows.items():
            strata[(row["language"], row["task"])][index][case] = row
    by_stratum = {}
    for (language, task), pair in sorted(strata.items()):
        by_stratum[f"{language}/{task}"] = {
            "reviewer_a": _reviewer_summary(pair[0]),
            "reviewer_b": _reviewer_summary(pair[1]),
        }
    if len(by_stratum) != 4 or any(v["reviewer_a"]["cases"] != 12 for v in by_stratum.values()):
        raise ValueError("the review packet must retain its four 12-case language/task strata")
    return {
        "schema_version": "v433-human-review-aggregate-v1",
        "date": date.today().isoformat(),
        "pilot_version": "vi-en-ai-v4.33",
        "provenance": "human reviewer-submitted ratings of AI-authored synthetic validation examples; reviewer qualifications are external attestations",
        "scope": {
            "cases": len(a),
            "split": "validation only",
            "release_test_rows_reviewed": False,
            "phomt_used": False,
            "strata": {key: value["reviewer_a"]["cases"] for key, value in by_stratum.items()},
        },
        "reviewer_a": _reviewer_summary(a),
        "reviewer_b": _reviewer_summary(b),
        "inter_rater_agreement": agreement,
        "by_language_and_task": by_stratum,
        "limitations": [
            "Small synthetic validation sample; not a natural-corpus estimate or efficacy result.",
            "This descriptive report defines no post-hoc pass threshold and does not establish broad OOD quality.",
            "Source, target, and free-text reviewer notes are intentionally excluded from this report.",
        ],
        "source_or_generated_text_recorded": False,
        "reviewer_notes_recorded": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reviewer_a", nargs="?", type=Path, default=BASE / "reviewer-a.csv")
    parser.add_argument("reviewer_b", nargs="?", type=Path, default=BASE / "reviewer-b.csv")
    parser.add_argument("--output", required=True, type=Path,
                        help="aggregate JSON destination; must not already exist")
    args = parser.parse_args()
    forms = (_load(args.reviewer_a), _load(args.reviewer_b))
    _validate_pair(forms)
    report = _summarize(*forms)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2, sort_keys=True)
        stream.write("\n")
    print(json.dumps({
        "report": str(args.output),
        "cases": report["scope"]["cases"],
        "agreement": report["inter_rater_agreement"],
        "source_or_generated_text_emitted": False,
        "reviewer_notes_emitted": False,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
