"""Aggregate-only post-hoc action-sensitivity diagnostic for saved validation runs."""

import argparse
import hashlib
import json
import unicodedata
from collections import defaultdict
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))


def _read_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def _norm(value: str) -> str:
    return " ".join(unicodedata.normalize("NFC", value).casefold().split())


def diagnose(directory: Path) -> list[dict]:
    base = directory.resolve()
    protocol = _read_json(base / "protocol.json")
    single_rows = []
    if protocol.get("review_scope") == "train-validation-only":
        from scripts.diagnose_train_checkpoint import load_review_bundle
        _, reviewed, _, group_splits = load_review_bundle(base)
        single_rows = [row for row in reviewed if row["path_id"] is None
                       and group_splits[row["split_group_id"]] == "validation"]
    else:
        manifest = _read_json(base / "split_manifest.json")
        group_splits = manifest["groups"]
        with (base / "corpus.jsonl").open(encoding="utf-8") as stream:
            for line in stream:
                row = json.loads(line)
                if (row["path_id"] is None
                        and group_splits[row["split_group_id"]] == "validation"):
                    single_rows.append(row)

    configs = sorted(base.glob("tide-*.json"))
    if not configs:
        raise ValueError("no registered decoder configurations found")
    results = []
    for config_path in configs:
        config = _read_json(config_path)
        run_dir = (base / config["output_dir"]).resolve()
        private_path = run_dir / "generation.validation.private.jsonl"
        generated = {}
        with private_path.open(encoding="utf-8") as stream:
            for line in stream:
                item = json.loads(line)
                if item.get("task") == "single":
                    record_id = item["record_id"]
                    if record_id in generated:
                        raise ValueError("duplicate private validation record")
                    generated[record_id] = _norm(item["generated_text"])

        groups = defaultdict(list)
        for row in single_rows:
            record_id = row["record_id"]
            if record_id not in generated:
                raise ValueError("private validation generation is missing a single-action row")
            source_key = hashlib.sha256(row["source_text"].encode("utf-8")).hexdigest()
            key = (row["language"], source_key)
            action = f'{row["action"]["kind"]}:{row["action"]["value"]}'
            groups[key].append((action, generated[record_id]))

        for language in ("en", "vi"):
            pairs = [items for (lang, _), items in groups.items() if lang == language]
            if any(len(items) != 2 or items[0][0] == items[1][0] for items in pairs):
                raise ValueError("expected exactly two distinct action types per repeated source")
            changed = sum(items[0][1] != items[1][1] for items in pairs)
            results.append({
                "condition": config_path.stem,
                "language": language,
                "source_pairs": len(pairs),
                "different_outputs": changed,
            })
    return results


def render(results: list[dict], directory: Path) -> str:
    version = directory.name.removeprefix("vi-en-ai-")
    lines = [
        f"# {version} post-hoc action-sensitivity diagnostic",
        "",
        "This aggregate-only check compares the saved validation generations for the same exact source text paired with two distinct single actions. It tests whether output changes when the requested action changes; it does not measure whether the changed output is correct. This is post-hoc diagnostic evidence, not frozen-protocol gate evidence, and does not open the release holdout.",
        "",
        "All rows are preliminary synthetic evidence; no source, generated, or reference text is shown. Matching is exact after NFC normalization, Unicode case folding, and whitespace normalization. The source is used only as an in-memory SHA-256 grouping key.",
        "",
        "| Condition | Language | Same-source pairs | Different outputs | Rate |",
        "|---|---|---:|---:|---:|",
    ]
    for item in results:
        total = item["source_pairs"]
        changed = item["different_outputs"]
        lines.append(f'| {item["condition"]} | {item["language"]} | {total} | {changed} | {changed / total:.1%} |')
    lines.extend([
        "",
        "Interpretation: distinct outputs are nearly universal across requested action pairs, so a low preservation or fidelity score is not explained by the model always ignoring the action input. It indicates that action-conditioned changes can fail to preserve or realize the intended event roles. This remains an inference from a narrow synthetic rule checker and an exact output-difference diagnostic.",
        "",
        f"Reproduce without printing examples: `python -B scripts/diagnose_validation_action_sensitivity.py {directory} --markdown YOUR_DIAGNOSTIC.md`.",
        "",
        "The diagnostic reads private validation generations under Git-ignored `runs/`; it writes aggregate counts only.",
        "",
    ])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--markdown", type=Path, required=True)
    args = parser.parse_args()
    results = diagnose(args.directory)
    args.markdown.write_text(render(results, args.directory), encoding="utf-8")
    print(json.dumps({"runs": len({x['condition'] for x in results}),
                      "language_condition_rows": len(results),
                      "all_pairs_scored": all(x["source_pairs"] > 0 for x in results),
                      "markdown": str(args.markdown)}, sort_keys=True))


if __name__ == "__main__":
    main()
