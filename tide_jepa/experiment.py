"""Reproducible, approval-gated TIDE-JEPA experiment runner.

This runner consumes an already reviewed JSONL corpus and action inventory. It
never downloads data, changes approval metadata, or scores the held-out test set.
"""

import argparse
import csv
from dataclasses import asdict, replace
import hashlib
import json
import math
import os
from pathlib import Path
import random
import tempfile
import time

import torch

from tide_jepa.config import ModelConfig
from tide_jepa.data import (
    UTF8ByteTokenizer,
    build_batch,
    grouped_split,
    read_jsonl,
    read_split_manifest,
    write_split_manifest,
)
from tide_jepa.model import TIDEJEPA
from tide_jepa.schema import Action, EdgePair, Inventory, PathPair
from tide_jepa.training import Objective, Trainer, compute_loss


def _read_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        raise ValueError(f"expected a JSON object in {path}")
    return value


def _parse_inventory(value: dict) -> Inventory:
    try:
        actions = tuple(Action(item["kind"], item["value"]) for item in value["actions"])
        approved = {
            language: frozenset(Action(item["kind"], item["value"]) for item in items)
            for language, items in value["approved_by_language"].items()
        }
    except (KeyError, TypeError, AttributeError) as error:
        raise ValueError("inventory needs actions and approved_by_language lists") from error
    return Inventory(actions, approved)


def _canonical_hash(value: object) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _implementation_identity() -> dict:
    package = Path(__file__).parent
    sources = sorted(path for path in package.iterdir() if path.is_file() and path.suffix in {".py", ".html"})
    return {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in sources}


def _runtime_identity() -> dict:
    import sys
    return {"python": sys.version, "torch": torch.__version__}


def _atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(value, stream, ensure_ascii=False, sort_keys=True, indent=2)
            stream.write("\n")
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def _write_csv_atomic(path: Path, header: tuple[str, ...], rows) -> None:
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as stream:
            writer = csv.writer(stream)
            writer.writerow(header)
            writer.writerows(rows)
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def _reconcile_metrics_log(path: Path, checkpoint_epoch: int) -> None:
    """Drop durable metric rows for epochs whose checkpoint was not published."""
    header = ("epoch", "split", "loss", "token", "jepa", "alignment", "variance", "path_jepa",
              "path_token", "path_alignment", "copy_token", "token_count", "copy_token_count", "edge_count", "alignment_count", "path_count",
              "path_alignment_count", "examples", "source_tokens", "target_tokens", "updates",
              "seconds", "examples_per_second", "peak_vram_bytes")
    with path.open("r", encoding="utf-8", newline="") as stream:
        reader = csv.reader(stream)
        current_header = next(reader, None)
        rows = [row for row in reader if row and row[0].isdigit() and int(row[0]) <= checkpoint_epoch]
    if tuple(current_header or ()) != header:
        raise ValueError("metrics log schema differs from the checkpoint run")
    counts = {}
    for row in rows:
        if len(row) != len(header):
            raise ValueError("metrics log has a malformed committed row")
        counts.setdefault(int(row[0]), set()).add(row[1])
    if any(counts.get(epoch) != {"train", "validation"} for epoch in range(1, checkpoint_epoch + 1)):
        raise ValueError("metrics log is incomplete for a published checkpoint epoch")
    _write_csv_atomic(path, header, rows)


def _append_metrics_rows(path: Path, new_rows) -> None:
    with path.open("r", encoding="utf-8", newline="") as stream:
        reader = csv.reader(stream)
        header = tuple(next(reader))
        rows = list(reader)
    _write_csv_atomic(path, header, rows + new_rows)


def _batch_records(records, batch_size: int, *, shuffle_seed: int | None = None):
    """Yield group-preserving batches after a conservative allocation preflight."""
    grouped = {}
    for record in records:
        grouped.setdefault(record.split_group_id, []).append(record)
    group_ids = sorted(grouped)
    if shuffle_seed is not None:
        random.Random(shuffle_seed).shuffle(group_ids)
    pending = []
    pending_size = 0
    for group_id in group_ids:
        group = grouped[group_id]
        # 512 rows or 262144 UTF-8 bytes per indivisible event group is a
        # deliberately conservative hard ceiling before tensor allocation.
        if len(group) > 512 or sum(len((r.source_text + r.target_text).encode("utf-8")) for r in group) > 262144:
            raise ValueError("split group exceeds the 512-record/262144-byte preflight budget")
        if pending and pending_size + len(group) > batch_size:
            yield tuple(record for key in pending for record in grouped[key])
            pending, pending_size = [], 0
        pending.append(group_id)
        pending_size += len(group)
    if pending:
        yield tuple(record for key in pending for record in grouped[key])


def _read_alignments(path: Path | None, record_map: dict):
    if path is None:
        return (), ()
    value = _read_json(path)
    edge_pairs = []
    path_pairs = []
    for item in value.get("edge_pairs", []):
        left_id, right_id = item["left_record_id"], item["right_record_id"]
        if left_id not in record_map or right_id not in record_map:
            raise ValueError("edge alignment references a record outside the corpus")
        if record_map[left_id].split_group_id != record_map[right_id].split_group_id:
            raise ValueError("aligned records must share a split_group_id")
        edge_pairs.append((left_id, right_id, item.get("relation", "same_event")))
    for item in value.get("path_pairs", []):
        left = (item["left_path_id"], item["left_language"])
        right = (item["right_path_id"], item["right_language"])
        left_rows = [r for r in record_map.values() if (r.path_id, r.language) == left]
        right_rows = [r for r in record_map.values() if (r.path_id, r.language) == right]
        if not left_rows or not right_rows:
            raise ValueError("path alignment references a path outside the corpus")
        if {r.split_group_id for r in left_rows} != {r.split_group_id for r in right_rows}:
            raise ValueError("aligned paths must share one split_group_id")
        path_pairs.append((left, right, item.get("relation", "same_event")))
    return tuple(edge_pairs), tuple(path_pairs)


def _build_experiment_batch(rows, cfg, inventory, device, edge_alignment, path_alignment):
    batch = build_batch(rows, cfg, inventory, device=device)
    local_edges = {record.record_id: index for index, record in enumerate(rows)}
    edge_pairs = tuple(
        EdgePair(local_edges[left], local_edges[right], relation)
        for left, right, relation in edge_alignment
        if left in local_edges and right in local_edges
    )
    local_paths = {
        key: index
        for index, key in enumerate(sorted({(r.path_id, r.language) for r in rows if r.path_id is not None}))
    }
    path_pairs = tuple(
        PathPair(local_paths[left], local_paths[right], relation)
        for left, right, relation in path_alignment
        if left in local_paths and right in local_paths
    )
    batch = replace(batch, pairs=edge_pairs, path_pairs=path_pairs)
    batch.validate(cfg, inventory)
    return batch


def _evaluate(model, records, cfg, inventory, objective, batch_size, device, edge_alignment, path_alignment):
    model.eval()
    totals, metric_denoms = {}, {name: 0 for name in ("token", "copy_token", "jepa", "alignment", "variance", "path_jepa", "path_token", "path_alignment", "latent_std")}
    denominators = {key: 0 for key in ("token_count", "copy_token_count", "edge_count", "alignment_count", "path_count", "path_alignment_count")}
    examples = 0
    with torch.no_grad():
        for rows in _batch_records(records, batch_size):
            batch = _build_experiment_batch(rows, cfg, inventory, device, edge_alignment, path_alignment)
            _, metrics = compute_loss(model, batch, inventory, objective)
            examples += len(rows)
            for key in denominators:
                denominators[key] += metrics[key]
            units = {"token": metrics["token_count"], "copy_token": metrics["copy_token_count"],
                     "jepa": metrics["edge_count"],
                     "alignment": metrics["alignment_count"], "variance": metrics["edge_count"],
                     "path_jepa": metrics["path_count"], "path_token": metrics["path_count"],
                     "path_alignment": metrics["path_alignment_count"], "latent_std": metrics["edge_count"]}
            for name, count in units.items():
                metric_denoms[name] += count
                if count:
                    totals[name] = totals.get(name, 0.0) + float(metrics[name]) * count
    if not examples:
        raise ValueError("validation split is empty")
    result = {name: totals.get(name, 0.0) / count if count else 0.0
              for name, count in metric_denoms.items()}
    result.update(denominators)
    result["examples"] = examples
    result["loss"] = (result.get("token", 0.0) + objective.source_copy_weight * result.get("copy_token", 0.0)
                      + objective.jepa_weight * result.get("jepa", 0.0)
                      + objective.alignment_weight * result.get("alignment", 0.0)
                      + objective.variance_weight * result.get("variance", 0.0)
                      + objective.path_weight * result.get("path_jepa", 0.0)
                      + objective.path_token_weight * result.get("path_token", 0.0)
                      + objective.path_alignment_weight * result.get("path_alignment", 0.0))
    return result


def _token_counts(records, tokenizer):
    return {
        "source_tokens": sum(len(tokenizer.encode(row.source_text)) for row in records),
        "target_tokens": sum(len(tokenizer.encode(row.target_text, add_eos=True)) for row in records),
    }


def _save_checkpoint(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    os.close(descriptor)
    try:
        torch.save(state, temporary)
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def run_experiment(
    config_path: str | Path,
    *,
    resume: bool = False,
    evaluate_test: bool = False,
    device: str = "auto",
) -> dict:
    """Train one objective with deterministic splits, group-safe batches and checkpoints."""
    config_path = Path(config_path).resolve()
    config = _read_json(config_path)
    base = config_path.parent
    required = {"corpus", "inventory", "output_dir", "seed", "training"}
    missing = required - set(config)
    if missing:
        raise ValueError(f"missing experiment settings: {', '.join(sorted(missing))}")

    corpus_path = (base / config["corpus"]).resolve()
    inventory_path = (base / config["inventory"]).resolve()
    output_dir = (base / config["output_dir"]).resolve()
    inventory = _parse_inventory(_read_json(inventory_path))
    languages = tuple(config.get("languages", ("vi", "en", "cham_phan_rang")))
    records = read_jsonl(corpus_path, inventory, languages=languages, require_approved=True)
    protected = ("phomt" in str(corpus_path).casefold()
                 or any("phomt" in (row.provenance_ref + " " + row.license_ref).casefold()
                        and "no-phomt-content" not in (row.provenance_ref + " " + row.license_ref).casefold()
                        for row in records))
    if protected:
        data_root = (Path(__file__).resolve().parents[1] / "data").resolve()
        if output_dir != data_root and data_root not in output_dir.parents:
            raise ValueError("PhoMT-derived checkpoints, reports, and generated rows must stay under project data/")
    training = config["training"]
    seed = config["seed"]
    if type(seed) is not int:
        raise ValueError("seed must be an integer")
    epochs = training.get("epochs", 20)
    batch_size = training.get("batch_size", 32)
    learning_rate = training.get("learning_rate", 1e-3)
    if type(epochs) is not int or epochs <= 0 or type(batch_size) is not int or batch_size <= 0:
        raise ValueError("epochs and batch_size must be positive integers")
    if not isinstance(learning_rate, (int, float)) or not math.isfinite(learning_rate) or learning_rate <= 0:
        raise ValueError("learning_rate must be finite and positive")

    split_settings = config.get("split", {})
    manifest = read_split_manifest(base / config["frozen_split"], records, inventory) if config.get("frozen_split") else grouped_split(
        records,
        inventory,
        seed=split_settings.get("seed", seed),
        train=split_settings.get("train", 0.8),
        validation=split_settings.get("validation", 0.1),
        test=split_settings.get("test", 0.1),
    )
    record_map = {record.record_id: record for record in records}
    alignments_path = (base / config["alignments"]).resolve() if config.get("alignments") else None
    edge_alignment, path_alignment = _read_alignments(alignments_path, record_map)
    split_records = {
        name: tuple(record_map[record_id] for record_id in manifest.record_ids[name])
        for name in ("train", "validation", "test")
    }
    if not split_records["train"] or not split_records["validation"] or not split_records["test"]:
        raise ValueError("train, validation, and test splits must all contain records")

    objective = Objective(**config.get("objective", {}))
    model_settings = config.get("model", {})
    tokenizer = UTF8ByteTokenizer()
    cfg = ModelConfig(
        vocab_size=tokenizer.vocab_size,
        action_count=len(inventory.actions),
        width=model_settings.get("width", 64),
        heads=model_settings.get("heads", 4),
        layers=model_settings.get("layers", 2),
        max_length=model_settings.get("max_length", 512),
        languages=languages,
    )
    if device == "auto":
        device = "cuda" if torch.cuda.is_available() else "cpu"
    if device.startswith("cuda") and not torch.cuda.is_available():
        raise RuntimeError("CUDA was requested but is not available in this PyTorch runtime")

    run_identity = {
        "config": config,
        "corpus_sha256": manifest.dataset_sha256,
        "split_sha256": manifest.sha256,
        "inventory_sha256": _canonical_hash(_read_json(inventory_path)),
        "alignments_sha256": _canonical_hash(_read_json(alignments_path)) if alignments_path else None,
        "implementation_sha256": _implementation_identity(),
        "runtime": _runtime_identity(),
    }
    if config.get("review_gate"):
        from .pilot import validate_review_gate
        run_identity["review_approval_sha256"] = validate_review_gate(
            base, config, manifest, run_identity["inventory_sha256"], run_identity["alignments_sha256"]
        )
        protocol_path = base / "protocol.json"
        if protocol_path.is_file():
            protocol = _read_json(protocol_path)
            if (protocol.get("implementation_sha256") != run_identity["implementation_sha256"]
                    or protocol.get("runtime") != run_identity["runtime"]):
                raise ValueError("current code/runtime differs from the frozen pilot protocol")
    identity_hash = _canonical_hash(run_identity)
    resume_state = None
    if resume:
        if not (output_dir / "latest.pt").is_file():
            raise FileNotFoundError("cannot resume; latest checkpoint not found")
        resume_state = torch.load(output_dir / "latest.pt", map_location="cpu", weights_only=True)
        if resume_state.get("run_sha256") != identity_hash:
            raise ValueError("checkpoint run identity differs from the current config/data/split")
        if "torch_rng_state" not in resume_state or "python_rng_state" not in resume_state:
            raise ValueError("checkpoint lacks RNG state required for reproducible resume")
        if not (output_dir / "metrics.csv").is_file():
            raise FileNotFoundError("cannot resume; metrics log not found")
    if not resume and any((output_dir / name).exists() for name in ("latest.pt", "best.pt", "metrics.csv")):
        raise FileExistsError("run output already contains results; resume or choose a new directory")
    output_dir.mkdir(parents=True, exist_ok=True)
    _atomic_json(output_dir / "resolved_run.json", {
        **run_identity,
        "run_sha256": identity_hash,
        "device": device,
        "python_version": __import__("sys").version,
        "torch_version": torch.__version__,
        "cuda_device_name": torch.cuda.get_device_name(device) if device.startswith("cuda") else None,
        "model": asdict(cfg),
        "objective": asdict(objective),
        "split_counts": {name: len(rows) for name, rows in split_records.items()},
    })
    write_split_manifest(output_dir / "split_manifest.json", manifest)

    random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    model = TIDEJEPA(cfg).to(device)
    trainer = Trainer(model, inventory, objective, learning_rate=learning_rate)
    latest_path = output_dir / "latest.pt"
    best_path = output_dir / "best.pt"
    start_epoch = 0
    best_validation = float("inf")
    best_epoch = None
    if resume:
        state = resume_state
        model.load_state_dict(state["model"])
        trainer.optimizer.load_state_dict(state["optimizer"])
        trainer.steps = state["steps"]
        start_epoch = state["epoch"]
        best_validation = state["best_validation"]
        best_epoch = state.get("best_epoch")
        torch.set_rng_state(state["torch_rng_state"])
        random.setstate(state["python_rng_state"])
        if device.startswith("cuda"):
            if "cuda_rng_state" not in state:
                raise ValueError("CUDA checkpoint lacks CUDA RNG state")
            torch.cuda.set_rng_state_all(state["cuda_rng_state"])
        for optimizer_state in trainer.optimizer.state.values():
            for key, value in optimizer_state.items():
                if isinstance(value, torch.Tensor):
                    optimizer_state[key] = value.to(device)
        # Recover the only interrupted publication window: latest was made
        # durable after recording a new best score, but best.pt was not.
        best_missing_or_stale = not best_path.is_file()
        if not best_missing_or_stale:
            prior_best = torch.load(best_path, map_location="cpu", weights_only=True)
            best_missing_or_stale = prior_best.get("epoch") != best_epoch
        if best_missing_or_stale:
            if state.get("selection_loss") != best_validation or state.get("epoch") != best_epoch:
                raise ValueError("best checkpoint is missing or inconsistent and latest cannot safely recover it")
            _save_checkpoint(best_path, state)

    log_path = output_dir / "metrics.csv"
    header = ("epoch", "split", "loss", "token", "jepa", "alignment", "variance", "path_jepa",
              "path_token", "path_alignment", "copy_token", "token_count", "copy_token_count", "edge_count", "alignment_count", "path_count",
              "path_alignment_count", "examples", "source_tokens", "target_tokens", "updates",
              "seconds", "examples_per_second", "peak_vram_bytes")
    if not resume:
        _write_csv_atomic(log_path, header, [])
    elif not log_path.is_file():
        raise FileNotFoundError(f"cannot resume; metrics log not found: {log_path}")
    else:
        _reconcile_metrics_log(log_path, start_epoch)

    history = []
    for epoch in range(start_epoch + 1, epochs + 1):
        if device.startswith("cuda"):
            torch.cuda.reset_peak_memory_stats(device)
        started = time.perf_counter()
        model.train()
        totals = {}
        metric_counts = {name: 0 for name in ("token", "copy_token", "jepa", "alignment", "variance", "path_jepa", "path_token", "path_alignment", "latent_std")}
        seen = 0
        updates_before = trainer.steps
        for rows in _batch_records(split_records["train"], batch_size, shuffle_seed=seed + epoch):
            batch = _build_experiment_batch(rows, cfg, inventory, device, edge_alignment, path_alignment)
            metrics = trainer.step(batch)
            weight = len(rows)
            seen += weight
            units = {"token": metrics["token_count"], "copy_token": metrics["copy_token_count"],
                     "jepa": metrics["edge_count"],
                     "alignment": metrics["alignment_count"], "variance": metrics["edge_count"],
                     "path_jepa": metrics["path_count"], "path_token": metrics["path_count"],
                     "path_alignment": metrics["path_alignment_count"], "latent_std": metrics["edge_count"]}
            for name, count in units.items():
                metric_counts[name] += count
                if count:
                    totals[name] = totals.get(name, 0.0) + metrics[name] * count
        seconds = time.perf_counter() - started
        train_metrics = {name: totals.get(name, 0.0) / count if count else 0.0
                         for name, count in metric_counts.items()}
        train_metrics["loss"] = (train_metrics["token"] + objective.source_copy_weight * train_metrics["copy_token"]
                                  + objective.jepa_weight * train_metrics["jepa"]
                                  + objective.alignment_weight * train_metrics["alignment"]
                                  + objective.variance_weight * train_metrics["variance"]
                                  + objective.path_weight * train_metrics["path_jepa"]
                                  + objective.path_token_weight * train_metrics["path_token"]
                                  + objective.path_alignment_weight * train_metrics["path_alignment"])
        train_metrics.update({"token_count": metric_counts["token"], "copy_token_count": metric_counts["copy_token"], "edge_count": seen,
                              "alignment_count": metric_counts["alignment"],
                              "path_count": metric_counts["path_token"],
                              "path_alignment_count": metric_counts["path_alignment"]})
        train_metrics.update(_token_counts(split_records["train"], tokenizer))
        peak_vram_bytes = torch.cuda.max_memory_allocated(device) if device.startswith("cuda") else 0
        validation_metrics = _evaluate(
            model, split_records["validation"], cfg, inventory, objective, batch_size, device,
            edge_alignment, path_alignment,
        )
        validation_metrics.update(_token_counts(split_records["validation"], tokenizer))
        row_base = [epoch]
        csv_rows = []
        for split_name, metrics, count, elapsed in (
                ("train", train_metrics, seen, seconds),
                ("validation", validation_metrics, len(split_records["validation"]), 0.0),
            ):
                csv_rows.append(row_base + [split_name] + [metrics.get(key, 0.0) for key in (
                    "loss", "token", "jepa", "alignment", "variance", "path_jepa", "path_token", "path_alignment", "copy_token"
                )] + [metrics.get(key, 0) for key in ("token_count", "copy_token_count", "edge_count", "alignment_count", "path_count", "path_alignment_count")]
                    + [count, metrics.get("source_tokens", 0), metrics.get("target_tokens", 0),
                      trainer.steps - updates_before if split_name == "train" else 0, elapsed,
                      count / elapsed if elapsed else 0.0, peak_vram_bytes if split_name == "train" else 0])
        _append_metrics_rows(log_path, csv_rows)
        selection_loss = (validation_metrics["token"]
                          + objective.path_token_weight * validation_metrics["path_token"]
                          + objective.source_copy_weight * validation_metrics["copy_token"])
        improved = selection_loss < best_validation
        checkpoint = {
            "run_sha256": identity_hash,
            "epoch": epoch,
            "steps": trainer.steps,
            "best_validation": selection_loss if improved else best_validation,
            "selection_loss": selection_loss,
            "best_epoch": epoch if improved else best_epoch,
            "model": model.state_dict(),
            "optimizer": trainer.optimizer.state_dict(),
            "torch_rng_state": torch.get_rng_state(),
            "python_rng_state": random.getstate(),
        }
        if device.startswith("cuda"):
            checkpoint["cuda_rng_state"] = torch.cuda.get_rng_state_all()
        _save_checkpoint(latest_path, checkpoint)
        # Select all objective controls by the same generation loss criterion.
        if improved:
            best_validation = selection_loss
            best_epoch = epoch
            _save_checkpoint(best_path, checkpoint)
        result = {
            "epoch": epoch,
            "train": train_metrics,
            "validation": validation_metrics,
            "updates": trainer.steps - updates_before,
            "seconds": seconds,
            "examples_per_second": seen / seconds if seconds else 0.0,
            **_token_counts(split_records["train"], tokenizer),
            "peak_vram_bytes": peak_vram_bytes,
        }
        history.append(result)
        print(json.dumps(result, sort_keys=True))

    result = {
        "run_sha256": identity_hash,
        "last_epoch": start_epoch + len(history),
        "steps": trainer.steps,
        "best_validation_loss": best_validation,
        "test_records_reserved": len(split_records["test"]),
        "test_evaluated": False,
        "history": history,
    }
    if evaluate_test:
        evaluation_path = output_dir / "test_metrics.json"
        if not best_path.is_file():
            raise FileNotFoundError("test evaluation requires a completed best-validation checkpoint")
        best_state = torch.load(best_path, map_location="cpu", weights_only=True)
        if best_state.get("run_sha256") != identity_hash:
            raise ValueError("best checkpoint run identity differs from the current config/data/split")
        checkpoint_sha = hashlib.sha256(best_path.read_bytes()).hexdigest()
        evaluation_identity = _canonical_hash({"run_sha256": identity_hash, "checkpoint_sha256": checkpoint_sha,
                                               "test_record_ids": manifest.record_ids["test"],
                                               "evaluator_sha256": {k: _implementation_identity()[k]
                                                                    for k in ("infer.py", "experiment.py")}})
        if evaluation_path.exists():
            saved = _read_json(evaluation_path)
            if saved.get("_evaluation_identity") != evaluation_identity:
                raise FileExistsError("held-out test evidence exists with a different identity; preserve it and create a new run")
            result["test_metrics"] = {k: v for k, v in saved.items() if not k.startswith("_")}
            result["test_evaluated"] = True
            return result
        model.load_state_dict(best_state["model"])
        test_metrics = _evaluate(
            model, split_records["test"], cfg, inventory, objective, batch_size, device,
            edge_alignment, path_alignment,
        )
        test_metrics.update(_token_counts(split_records["test"], tokenizer))
        test_metrics["examples"] = len(split_records["test"])
        test_metrics["_evaluation_identity"] = evaluation_identity
        _atomic_json(output_dir / "test_metrics.json", test_metrics)
        result["test_metrics"] = test_metrics
        result["test_evaluated"] = True
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Run an approved TIDE-JEPA corpus experiment")
    parser.add_argument("config", help="path to experiment JSON config")
    parser.add_argument("--resume", action="store_true", help="resume from output_dir/latest.pt")
    parser.add_argument("--evaluate-test", action="store_true", help="score the reserved test split with best.pt after training")
    parser.add_argument("--device", default="auto", help="auto, cpu, cuda, or cuda:N")
    args = parser.parse_args()
    result = run_experiment(args.config, resume=args.resume, evaluate_test=args.evaluate_test, device=args.device)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
