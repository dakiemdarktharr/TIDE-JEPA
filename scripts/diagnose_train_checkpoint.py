"""Fast, aggregate-only train diagnostics for a completed frozen pilot.

Uses only the protocol-bound train/validation review bundle, never the full
corpus or holdout frame catalog. Selects train singles before any scoring.
Run in a fresh process so the verified frozen package cannot mix with imports
from the workspace. Does not train, select checkpoints, or open release gates.
"""

import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def canonical_hash(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(",", ":")).encode()).hexdigest()


def load_review_bundle(base):
    """Fail closed on unbound bundles, test groups, or extra frame annotations."""
    base = Path(base).resolve()
    protocol = read_json(base / "protocol.json")
    bundle = base / "review_bundle"
    manifest_path = bundle / "manifest.json"
    manifest = read_json(manifest_path)
    if (protocol.get("review_scope") != "train-validation-only"
            or manifest.get("review_scope") != "train-validation-only"
            or protocol.get("review_bundle_sha256") != sha256(manifest_path)
            or protocol.get("reviewed_records") != manifest.get("reviewed_records")):
        raise ValueError("review bundle scope/count/hash is not bound to the frozen protocol")
    required = {"records.jsonl", "groups.json", "inventory.json", "alignments.json",
                "statement.json", "semantic_frames.json"}
    if set(manifest.get("files_sha256", {})) != required:
        raise ValueError("unexpected review bundle file inventory")
    for name, digest in manifest["files_sha256"].items():
        path = bundle / name
        if not path.resolve().is_relative_to(bundle.resolve()) or sha256(path) != digest:
            raise ValueError("review bundle file identity differs")
    groups = read_json(bundle / "groups.json")
    if not groups or not set(groups.values()) <= {"train", "validation"}:
        raise ValueError("review bundle contains a test or unknown split")
    statement = read_json(bundle / "statement.json")
    if (statement.get("human_validated") is not False or statement.get("phomt_used") is not False
            or statement.get("review_scope") != "train-validation-only"):
        raise ValueError("diagnostic requires the preliminary synthetic review bundle")
    rows, record_ids, frame_ids, seen_groups = [], set(), set(), set()
    count = 0
    with (bundle / "records.jsonl").open(encoding="utf-8") as stream:
        for line in stream:
            item = json.loads(line)
            count += 1
            group = item["split_group_id"]
            if group not in groups or item["record_id"] in record_ids:
                raise ValueError("review rows have unknown groups or duplicate record IDs")
            record_ids.add(item["record_id"])
            seen_groups.add(group)
            frame_ids.update((item["source_frame_id"], item["target_frame_id"]))
            rows.append(item)
    frames = read_json(bundle / "semantic_frames.json")
    if (count != manifest["reviewed_records"] or seen_groups != set(groups)
            or set(frames) != frame_ids):
        raise ValueError("review bundle row/group/frame inventory differs")
    return protocol, rows, frames, groups


def load_train_bundle(base):
    protocol, reviewed, frames, groups = load_review_bundle(base)
    rows = [row for row in reviewed if groups[row["split_group_id"]] == "train"
            and row.get("path_id") is None]
    train_frame_ids = {row[key] for row in rows for key in ("source_frame_id", "target_frame_id")}
    return protocol, rows, {key: frames[key] for key in train_frame_ids}


def bucket_key(row):
    return f"{row['language']}/{row['action']['kind']}:{row['action']['value']}"


def select_train_sample(rows, per_bucket=16, sample_seed=731):
    """One unique transition per group per language/action, ordered by hashes.

    Selection is fixed before checkpoint loading and never uses model scores.
    The same sample is reused across all registered conditions and seeds.
    """
    if type(per_bucket) is not int or not 2 <= per_bucket <= 64:
        raise ValueError("per_bucket must be an integer from 2 through 64")
    buckets = defaultdict(lambda: defaultdict(list))
    for row in rows:
        buckets[bucket_key(row)][row["split_group_id"]].append(row)
    selected = []
    for bucket, by_group in sorted(buckets.items()):
        if len(by_group) < per_bucket:
            raise ValueError("insufficient distinct train groups for the requested sample")
        ordered = sorted(by_group, key=lambda group: canonical_hash([sample_seed, bucket, group]))
        for group in ordered[:per_bucket]:
            selected.append(min(by_group[group], key=lambda row: canonical_hash(
                [sample_seed, row["record_id"]])))
    if not selected:
        raise ValueError("no train single-action transitions available")
    return selected


def source_controls(rows):
    """Use a different group's source in the same language/action bucket."""
    buckets = defaultdict(list)
    for row in rows:
        buckets[bucket_key(row)].append(row)
    controls = {}
    for values in buckets.values():
        for index, row in enumerate(values):
            candidates = values[index + 1:] + values[:index]
            other = next((item for item in candidates
                          if item["split_group_id"] != row["split_group_id"]
                          and item["source_text"] != row["source_text"]), None)
            if other is None:
                raise ValueError("source control needs another distinct train group/source")
            controls[row["record_id"]] = other["source_text"]
    return controls


def activate_frozen(base):
    from scripts.run_frozen import load_frozen_package
    load_frozen_package(base)


def score_checkpoint(generator, rows, frames, controls, max_new_tokens):
    import torch
    from torch.nn import functional as F
    from tide_jepa.pilot import _edit_distance, _semantic_frame_flags
    from tide_jepa.schema import Action

    result = {}
    tokenizer, model = generator.tokenizer, generator.model
    with torch.inference_mode():
        for row in rows:
            language = row["language"]
            action = Action(**row["action"])
            alternate = next((candidate for candidate in generator.inventory.actions
                              if candidate.kind == action.kind and candidate != action
                              and candidate in generator.inventory.approved_by_language[language]), None)
            if alternate is None:
                raise ValueError("action control needs a licensed same-kind alternative")
            tensor = lambda values: torch.tensor([values], dtype=torch.long, device=generator.device)
            source = tensor(tokenizer.encode(row["source_text"]))
            wrong_source = tensor(tokenizer.encode(controls[row["record_id"]]))
            labels = tensor(tokenizer.encode(row["target_text"], add_eos=True))
            decoder = tensor([tokenizer.bos_id] + labels[0, :-1].tolist())
            action_ids = tensor([generator.inventory.require(language, action)]).flatten()
            wrong_action = tensor([generator.inventory.require(language, alternate)]).flatten()
            language_ids = tensor([generator.cfg.languages.index(language)]).flatten()
            logits, _, predicted = model(source, decoder, action_ids, language_ids)
            wrong_source_logits = model(wrong_source, decoder, action_ids, language_ids)[0]
            wrong_action_logits = model(source, decoder, wrong_action, language_ids)[0]
            _, memory, valid = model.online.encode(source)
            zero_latent_logits = model.decode(decoder, torch.zeros_like(predicted), language_ids,
                                              memory, valid, source)
            nll = lambda value: F.cross_entropy(value.reshape(-1, value.shape[-1]),
                                                labels.reshape(-1), reduction="sum").item()
            correct = logits.argmax(dim=-1).eq(labels)
            generated = generator.generate({"source": row["source_text"],
                "source_language": language, "target_language": language,
                "actions": [row["action"]], "max_new_tokens": max_new_tokens})
            frame = frames[row["target_frame_id"]]
            gold_flags = _semantic_frame_flags(row["target_text"], language, frame)
            flags = _semantic_frame_flags(generated["generated_text"], language, frame)
            if (flags is None or gold_flags is None or not gold_flags["preservation"]
                    or not gold_flags["action_fidelity"]):
                raise ValueError("sample references lack complete, correct frozen checker coverage")
            counts = result.setdefault(bucket_key(row), {
                "examples": 0, "tokens_including_eos": 0, "teacher_forced_correct_tokens": 0,
                "teacher_forced_exact": 0, "greedy_exact": 0, "greedy_action_fidelity": 0,
                "greedy_preservation": 0, "greedy_predicate_preserved": 0,
                "greedy_patient_preserved": 0, "valid_utf8": 0, "terminated_eos": 0,
                "greedy_byte_edits_including_eos": 0,
                "gold_nll_sum": 0., "wrong_source_nll_sum": 0., "wrong_action_nll_sum": 0.,
                "zero_latent_nll_sum": 0.,
            })
            counts["examples"] += 1
            counts["tokens_including_eos"] += labels.numel()
            counts["teacher_forced_correct_tokens"] += int(correct.sum())
            counts["teacher_forced_exact"] += int(correct.all())
            counts["greedy_exact"] += int(generated["generated_text"] == tokenizer.decode(labels[0].tolist()))
            for field in ("action_fidelity", "preservation", "predicate_preserved", "patient_preserved"):
                counts["greedy_" + field] += int(flags[field])
            counts["valid_utf8"] += int(generated["valid_utf8"])
            counts["terminated_eos"] += int(tokenizer.eos_id in generated["generated_token_ids"])
            generated_ids = generated["generated_token_ids"]
            if generated_ids and generated_ids[0] == tokenizer.bos_id:
                generated_ids = generated_ids[1:]
            if tokenizer.eos_id in generated_ids:
                generated_ids = generated_ids[:generated_ids.index(tokenizer.eos_id) + 1]
            counts["greedy_byte_edits_including_eos"] += _edit_distance(labels[0].tolist(), generated_ids)
            for field, value in (("gold", logits), ("wrong_source", wrong_source_logits),
                                 ("wrong_action", wrong_action_logits), ("zero_latent", zero_latent_logits)):
                counts[field + "_nll_sum"] += nll(value)
    return result


def rates(counts):
    examples, tokens = counts["examples"], counts["tokens_including_eos"]
    result = dict(counts)
    result["teacher_forced_token_accuracy"] = counts["teacher_forced_correct_tokens"] / tokens
    for field in ("teacher_forced_exact", "greedy_exact", "greedy_action_fidelity",
                  "greedy_preservation", "greedy_predicate_preserved", "greedy_patient_preserved"):
        result[field + "_rate"] = counts[field] / examples
    result["gold_nll_per_token"] = counts["gold_nll_sum"] / tokens
    result["greedy_byte_edit_rate_including_eos"] = counts["greedy_byte_edits_including_eos"] / tokens
    for control in ("wrong_source", "wrong_action", "zero_latent"):
        result[control + "_nll_delta_per_token"] = (
            counts[control + "_nll_sum"] - counts["gold_nll_sum"]) / tokens
    return result


def markdown_report(report):
    lines = [f"# {report['pilot_version']} train checkpoint diagnostic", "",
        "Preliminary AI-authored/AI-reviewed synthetic evidence; no human validation. "
        "Post-hoc train-only mechanism probe, not validation or release-gate evidence.", "",
        f"Scored {report['sample_examples']} fixed train singles per checkpoint from "
        f"{report['sample_groups']} distinct groups; {report['per_bucket']} per language/action bucket. "
        "One transition per group per bucket; buckets/languages still share groups and are correlated. "
        "Review bundle parsing includes validation rows for inventory checks, but only train rows are scored. "
        "Full corpus and holdout annotations are never opened; no text is emitted.", "",
        f"Sample identity: `{report['sample_sha256']}`. Protocol: `{report['protocol_sha256']}`.", "",
        "| Run | Language | N | TF token accuracy | TF exact | Greedy exact | Greedy byte edit rate | Action | Preservation | Predicate | Wrong source ΔNLL/token | Wrong action ΔNLL/token | Zero latent ΔNLL/token |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for name, run in report["runs"].items():
        for language, counts in run["by_language"].items():
            cells = [name, language, str(counts["examples"])]
            cells += [f"{counts[key]:.1%}" for key in ("teacher_forced_token_accuracy",
                "teacher_forced_exact_rate", "greedy_exact_rate", "greedy_byte_edit_rate_including_eos", "greedy_action_fidelity_rate",
                "greedy_preservation_rate", "greedy_predicate_preserved_rate")]
            cells += [f"{counts[key + '_nll_delta_per_token']:.4f}" for key in (
                "wrong_source", "wrong_action", "zero_latent")]
            lines.append("| " + " | ".join(cells) + " |")
    lines += ["", "TF = teacher forcing with the correct reference prefix. Exactness uses one "
        "reference and can reject other valid wording; semantic rates use the frozen narrow checker. "
        "High byte accuracy can conceal whole-sentence errors. TF exactness already failing on train "
        "rules out a purely unseen-group explanation. TF exactness and greedy exactness are expected "
        "to agree when both use the same unconstrained argmax policy, since they share the first error. "
        "The free-generation byte edit rate measures error magnitude; comparison with TF byte errors "
        "alone does not establish exposure bias as the cause.", "",
        "Negative controls retain the original target and correct prefix. Positive ΔNLL means that "
        "removing the corresponding signal worsened reference likelihood. Source controls replace the "
        "source with another group's source from the same language/action bucket. Action controls use "
        "a licensed opposite value of the same action kind. Zero-latent controls keep source memory. "
        "These deliberately mismatched inputs are mechanism probes, not quality scores or evidence "
        "of JEPA benefit. Different controls can have different scales.", "",
        f"Elapsed CPU wall time: {report['seconds']:.1f}s with one Torch thread. "
        "No training, checkpoint selection, or frozen-protocol mutation occurred.", ""]
    return "\n".join(lines)


def diagnose(directory, *, per_bucket=16, sample_seed=731, config_names=None):
    started = time.monotonic()
    base = Path(directory).resolve()
    protocol, rows, frames = load_train_bundle(base)
    selected = select_train_sample(rows, per_bucket, sample_seed)
    controls = source_controls(selected)
    registered = protocol["configs"]
    names = config_names or registered
    if len(set(names)) != len(names) or any(name not in registered for name in names):
        raise ValueError("select only distinct configs registered in the frozen protocol")
    for name in names:
        if Path(name).name != name or sha256(base / name) != protocol["config_files_sha256"][name]:
            raise ValueError("registered config identity differs")
    activate_frozen(base)
    import torch
    from tide_jepa.infer import OfflineGenerator
    torch.set_num_threads(1)
    report = {"pilot_version": read_json(base / "review_bundle/statement.json")["version"],
        "scope": "post-hoc train singles only; fixed sample; aggregate-only mechanism diagnostic",
        "human_validated": False, "phomt_used": False, "release_holdout_opened": False,
        "validation_rows_scored": False, "full_corpus_or_holdout_frames_opened": False,
        "not_frozen_protocol_evidence": True, "text_emitted": False,
        "protocol_sha256": sha256(base / "protocol.json"),
        "review_bundle_sha256": protocol["review_bundle_sha256"],
        "diagnostic_script_sha256": sha256(__file__),
        "sample_sha256": canonical_hash(sorted(row["record_id"] for row in selected)),
        "sample_seed": sample_seed, "per_bucket": per_bucket,
        "sample_examples": len(selected), "sample_groups": len({r["split_group_id"] for r in selected}),
        "runs": {}}
    for name in names:
        config_path = base / name
        config = read_json(config_path)
        run_dir = (base / config["output_dir"]).resolve()
        # A final checkpoint must exist; partial runs are never silently diagnosed.
        checkpoint = run_dir / "best.pt"
        state = torch.load(checkpoint, map_location="cpu", weights_only=True)
        if state.get("epoch") != protocol["epochs"]:
            raise ValueError("diagnostic requires a completed fixed-final-epoch checkpoint")
        if config.get("checkpoint_selection_policy") != "fixed_final_epoch":
            raise ValueError("diagnostic currently supports fixed-final-epoch protocols only")
        generator = OfflineGenerator(config_path, checkpoint, device="cpu")
        scores = score_checkpoint(generator, selected, frames, controls,
                                  protocol["generation_max_new_tokens"])
        languages = {}
        for bucket, counts in scores.items():
            total = languages.setdefault(bucket.split("/")[0], {key: 0 for key in counts})
            for key, value in counts.items():
                total[key] += value
        report["runs"][Path(name).stem] = {"checkpoint_sha256": sha256(checkpoint),
            "config_sha256": sha256(config_path), "epoch": state["epoch"],
            "by_bucket": {key: rates(value) for key, value in scores.items()},
            "by_language": {key: rates(value) for key, value in sorted(languages.items())}}
        print(json.dumps({"completed_checkpoints": len(report["runs"]), "total_checkpoints": len(names),
                          "seconds": round(time.monotonic() - started, 1)}, sort_keys=True), flush=True)
    report["seconds"] = time.monotonic() - started
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory")
    parser.add_argument("--per-bucket", type=int, default=16)
    parser.add_argument("--sample-seed", type=int, default=731)
    parser.add_argument("--config", action="append", dest="config_names")
    parser.add_argument("--output", required=True, help="aggregate JSON report; never contains text")
    parser.add_argument("--markdown", required=True, help="aggregate Markdown report")
    args = parser.parse_args()
    report = diagnose(args.directory, per_bucket=args.per_bucket,
                      sample_seed=args.sample_seed, config_names=args.config_names)
    for destination, value in ((args.output, json.dumps(report, sort_keys=True, indent=2) + "\n"),
                               (args.markdown, markdown_report(report))):
        path = Path(destination)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value, encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("scope", "sample_examples", "sample_groups",
        "seconds", "text_emitted", "release_holdout_opened")}, sort_keys=True))


if __name__ == "__main__":
    main()
