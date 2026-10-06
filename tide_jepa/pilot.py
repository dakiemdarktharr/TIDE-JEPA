"""Freeze AI-reviewed original pilot artifacts and run a fixed comparison suite.

AI approval is explicitly preliminary. This module does not approve PhoMT
translation pairs, community permissions, or human linguistic ground truth.
"""

import argparse
from dataclasses import replace
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import tempfile
import unicodedata

from .data import (SplitManifest, dataset_fingerprint, read_jsonl,
                   read_split_manifest, write_split_manifest)
from .schema import Action, Inventory


MODES = ("token_only", "generic_jepa", "static_alignment", "tide")
REVIEWED_ARTIFACTS = ("inventory.draft.json", "alignments.draft.json", "groups.json", "data_statement.json", "semantic_frames.draft.json")


def _quality_gate_status(primary_mode, objective_mode, bucket_checks):
    if objective_mode != primary_mode:
        return "control_only"
    return "pass" if bucket_checks and all(check and all(value is True for value in check.values())
                                          for check in bucket_checks.values()) else "fail"


def _read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _write(path, value):
    path = Path(path)
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


def _hash_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _registered_primary_configs(protocol, named_configs):
    """Check the complete registered factorial, including decoder variants."""
    primary = protocol.get("primary_quality_mode")
    configs = [(name, config) for name, config in named_configs
               if config.get("objective", {}).get("mode") == primary]
    weights = set(protocol.get("primary_source_copy_weights", [
        config.get("objective", {}).get("source_copy_weight", 0.0) for _, config in configs]))
    latent_weights = set(protocol.get("primary_latent_objective_weights", [
        config.get("objective", {}).get("latent_objective_weight", 1.0) for _, config in configs]))
    balances = set(protocol.get("primary_transition_balance_modes", ["row_uniform"]))
    decoders = set(protocol.get("primary_source_pointer_decoder_modes", ["vocabulary"]))
    selected = []
    signatures = []
    for name, config in configs:
        objective = config.get("objective", {})
        weight = objective.get("source_copy_weight", 0.0)
        latent = objective.get("latent_objective_weight", 1.0)
        balance = config.get("training", {}).get("transition_balance", "row_uniform")
        decoder = "source_pointer" if config.get("model", {}).get("source_pointer_decoder", False) else "vocabulary"
        if weight in weights and latent in latent_weights and balance in balances and decoder in decoders:
            selected.append((name, config))
            signatures.append((config.get("seed"), weight, latent, balance, decoder))
    expected = {(seed, weight, latent, balance, decoder)
                for seed in protocol.get("seeds", []) for weight in weights
                for latent in latent_weights for balance in balances for decoder in decoders}
    if not expected or len(signatures) != len(expected) or set(signatures) != expected:
        raise ValueError("primary validation evidence does not cover every frozen seed/objective/decoder condition")
    return selected


def freeze_pilot(directory, *, epochs=40, seeds=(17, 23, 41), model_width=32,
                 model_heads=4, model_layers=1, max_length=192, batch_size=80,
                 learning_rate=0.001, primary_mode="tide", source_copy_weight=0.0,
                 condition_modes=None, condition_source_copy_weights=None,
                 condition_latent_objective_weights=None, condition_transition_balances=None,
                 condition_source_pointer_decoder_modes=None,
                 checkpoint_selection_policy="validation_loss", compute_source_copy_term=False):
    """Bind two distinct AI review records and adjudication to an exact draft.

    The user has authorized AI-reviewed preliminary experiments. This specific
    workflow accepts only the original authored corpus and excludes PhoMT.
    """
    from .experiment import _build_experiment_batch, _canonical_hash, _read_alignments
    from .config import ModelConfig

    base = Path(directory).resolve()
    if (base / "approval.json").exists():
        raise FileExistsError("pilot is already frozen; preserve it and create a new version")
    if type(epochs) is not int or epochs <= 0 or not seeds or any(type(s) is not int for s in seeds) or len(set(seeds)) != len(seeds):
        raise ValueError("epochs and independent integer seeds are required")
    if (any(type(value) is not int or value <= 0 for value in
            (model_width, model_heads, model_layers, max_length, batch_size))
            or model_width % model_heads != 0
            or type(learning_rate) not in {int, float}
            or not math.isfinite(learning_rate) or learning_rate <= 0):
        raise ValueError("model dimensions, batch size, and learning rate must be positive and compatible")
    if not isinstance(source_copy_weight, (int, float)) or isinstance(source_copy_weight, bool) or not math.isfinite(source_copy_weight) or source_copy_weight < 0:
        raise ValueError("source_copy_weight must be a finite nonnegative number")
    if primary_mode not in MODES:
        raise ValueError("primary_mode must name one registered objective control")
    if checkpoint_selection_policy not in {"validation_loss", "fixed_final_epoch"}:
        raise ValueError("checkpoint_selection_policy must be validation_loss or fixed_final_epoch")
    if type(compute_source_copy_term) is not bool:
        raise ValueError("compute_source_copy_term must be boolean")
    selected_modes = tuple(condition_modes) if condition_modes is not None else MODES
    copy_weights = (tuple(condition_source_copy_weights)
                    if condition_source_copy_weights is not None else (source_copy_weight,))
    latent_weights = (tuple(condition_latent_objective_weights)
                      if condition_latent_objective_weights is not None else (1.0,))
    transition_balances = (tuple(condition_transition_balances)
                           if condition_transition_balances is not None else ("row_uniform",))
    pointer_decoder_modes = (tuple(condition_source_pointer_decoder_modes)
                              if condition_source_pointer_decoder_modes is not None else ("vocabulary",))
    if (not selected_modes or len(set(selected_modes)) != len(selected_modes)
            or any(mode not in MODES for mode in selected_modes)
            or primary_mode not in selected_modes):
        raise ValueError("condition modes must be unique registered controls and include the primary mode")
    if (not copy_weights or len(set(copy_weights)) != len(copy_weights)
            or any(not isinstance(value, (int, float)) or isinstance(value, bool)
                   or not math.isfinite(value) or value < 0 for value in copy_weights)):
        raise ValueError("condition source-copy weights must be unique finite nonnegative values")
    if (not latent_weights or len(set(latent_weights)) != len(latent_weights)
            or any(not isinstance(value, (int, float)) or isinstance(value, bool)
                   or not math.isfinite(value) or value < 0 for value in latent_weights)):
        raise ValueError("condition latent-objective weights must be unique finite nonnegative values")
    if (not transition_balances or len(set(transition_balances)) != len(transition_balances)
            or any(value not in ("row_uniform", "unique_transition") for value in transition_balances)):
        raise ValueError("condition transition balances must be unique registered weighting modes")
    if (not pointer_decoder_modes or len(set(pointer_decoder_modes)) != len(pointer_decoder_modes)
            or any(value not in ("vocabulary", "source_pointer") for value in pointer_decoder_modes)):
        raise ValueError("condition source-pointer decoder modes must be unique registered modes")
    if condition_latent_objective_weights is not None and primary_mode != "tide":
        raise ValueError("latent-objective dose registration currently requires tide as the primary mode")
    if compute_source_copy_term and set(selected_modes) != {"tide"}:
        raise ValueError("matched source-copy-term computation is currently restricted to TIDE-only conditions")
    custom_matrix = (condition_modes is not None or condition_source_copy_weights is not None
                     or condition_latent_objective_weights is not None or condition_transition_balances is not None
                     or condition_source_pointer_decoder_modes is not None
                     or checkpoint_selection_policy != "validation_loss" or compute_source_copy_term)
    draft_inventory = _read(base / "inventory.draft.json")
    actions = tuple(Action(**item) for item in draft_inventory["actions"])
    proposed = draft_inventory["proposed_by_language"]
    if set(proposed) != {"en", "vi"} or draft_inventory["approved_by_language"].get("cham_phan_rang"):
        raise ValueError("this pilot permits English and Vietnamese only")
    inventory = Inventory(actions, {lang: frozenset(Action(**a) for a in proposed[lang]) for lang in ("en", "vi")})
    rows = read_jsonl(base / "corpus.draft.jsonl", inventory, languages=("en", "vi"), require_approved=False)
    draft_sha = dataset_fingerprint(rows)
    statement = _read(base / "data_statement.json")
    version = statement.get("version", "").removeprefix("vi-en-ai-")
    if not version:
        version = "v3"  # Legacy v3 author_seed fixtures predate version labels.
    expected_provenance = {
        "v3": "tide_jepa/pilot_seed.py:original-ai-authored-v1",
        "v4": "tide_jepa/pilot_seed.py:original-ai-authored-v4",
        "v4.1": "tide_jepa/pilot_seed.py:original-ai-authored-v4",
        "v4.2": "tide_jepa/pilot_seed.py:original-ai-authored-v4.2",
        "v4.3": "tide_jepa/pilot_seed.py:original-ai-authored-v4.3",
        "v4.4": "tide_jepa/pilot_seed.py:original-ai-authored-v4.4",
        "v4.5": "tide_jepa/pilot_seed.py:original-ai-authored-v4.5",
        "v4.6": "tide_jepa/pilot_seed.py:original-ai-authored-v4.6",
        "v4.7": "tide_jepa/pilot_seed.py:original-ai-authored-v4.7",
        "v4.8": "tide_jepa/pilot_seed.py:original-ai-authored-v4.8",
        "v4.9": "tide_jepa/pilot_seed.py:original-ai-authored-v4.9",
        "v4.10": "tide_jepa/pilot_seed.py:original-ai-authored-v4.10",
        "v4.11": "tide_jepa/pilot_seed.py:original-ai-authored-v4.11",
        "v4.12": "tide_jepa/pilot_seed.py:original-ai-authored-v4.12",
        "v4.13": "tide_jepa/pilot_seed.py:original-ai-authored-v4.13",
        "v4.14": "tide_jepa/pilot_seed.py:original-ai-authored-v4.14",
        "v4.15": "tide_jepa/pilot_seed.py:original-ai-authored-v4.15",
        "v4.16": "tide_jepa/pilot_seed.py:original-ai-authored-v4.16",
        "v4.17": "tide_jepa/pilot_seed.py:original-ai-authored-v4.17",
                  "v4.18": "tide_jepa/pilot_seed.py:original-ai-authored-v4.18",
        "v4.19": "tide_jepa/pilot_seed.py:original-ai-authored-v4.19",
        "v4.20": "tide_jepa/pilot_seed.py:original-ai-authored-v4.20",
        "v4.21": "tide_jepa/pilot_seed.py:original-ai-authored-v4.21",
        "v4.22": "tide_jepa/pilot_seed.py:original-ai-authored-v4.22",
        "v4.23": "tide_jepa/pilot_seed.py:original-ai-authored-v4.23",
    }.get(version)
    if expected_provenance is None or any(r.provenance_ref != expected_provenance
           or r.license_ref != "original-ai-authored-internal-research; no-PhoMT-content" for r in rows):
        raise ValueError("this gate refuses non-original corpus provenance or license references")
    if statement.get("phomt_used") is not False or statement.get("human_validated") is not False:
        raise ValueError("this workflow is for the original AI-authored preliminary pilot only")
    if statement.get("draft_sha256") != draft_sha or statement.get("records") != len(rows):
        raise ValueError("data statement differs from the draft corpus")
    reviewed_hashes = {name: _hash_file(base / name) for name in REVIEWED_ARTIFACTS}
    frames = _read(base / "semantic_frames.draft.json")
    required_frames = {frame for row in rows for frame in (row.source_frame_id, row.target_frame_id)}
    if set(frames) != required_frames:
        raise ValueError("semantic frame catalog must describe every and only referenced frame")
    reviews = [_read(base / name) for name in ("review-a.json", "review-b.json")]
    if len({r.get("reviewer_id") for r in reviews}) != 2:
        raise ValueError("two distinct AI reviewers are required")
    pending_adjudication = []
    for review in reviews:
        if (review.get("reviewer_type") != "AI" or review.get("decision") not in ("approve", "needs-adjudication")
                or review.get("draft_sha256") != draft_sha or review.get("rows_checked") != len(rows)
                or review.get("artifact_sha256") != reviewed_hashes):
            raise ValueError("review missing, pending, rejected, or bound to different artifacts")
        if review["decision"] == "needs-adjudication":
            pending_adjudication.append(review["reviewer_id"])
    adjudication = _read(base / "adjudication.json")
    if (adjudication.get("decision") != "approve" or adjudication.get("draft_sha256") != draft_sha
            or adjudication.get("human_validated") is not False):
        raise ValueError("preliminary AI adjudication is required")
    if pending_adjudication and (
            adjudication.get("adjudicator_type") != "AI"
            or set(adjudication.get("reviewer_ids", [])) != {r["reviewer_id"] for r in reviews}
            or set(adjudication.get("resolved_review_ids", [])) != set(pending_adjudication)
            or adjudication.get("artifact_sha256") != reviewed_hashes
            or not adjudication.get("resolution")):
        raise ValueError("explicit artifact-bound adjudication is required for pending reviews")
    approved_rows = tuple(replace(row, approval_status="approved") for row in rows)
    groups = _read(base / "groups.json")
    fractions = {name: sum(r.split_group_id in {g for g, s in groups.items() if s == name} for r in rows) / len(rows)
                 for name in ("train", "validation", "test")}
    split_seed = {"v4.9": 20261008, "v4.10": 20261009, "v4.11": 20261010,
                  "v4.12": 20261011, "v4.13": 20261012, "v4.14": 20261013,
                  "v4.15": 20261015, "v4.16": 20261017,
                  "v4.17": 20261018, "v4.18": 20261019,
                  "v4.19": 20261020, "v4.20": 20261021, "v4.21": 20261022,
                  "v4.22": 20261023, "v4.23": 20261024}.get(version, 20261001)
    manifest = SplitManifest(dataset_fingerprint(approved_rows), split_seed, fractions, groups,
                             {name: tuple(sorted(r.record_id for r in rows if groups[r.split_group_id] == name))
                              for name in ("train", "validation", "test")})
    approved_inventory = {"actions": draft_inventory["actions"], "approved_by_language": {"en": proposed["en"], "vi": proposed["vi"], "cham_phan_rang": []}}
    alignments = _read(base / "alignments.draft.json")
    cfg = ModelConfig(vocab_size=259, action_count=len(actions), width=model_width,
                      heads=model_heads, layers=model_layers, max_length=max_length,
                      languages=("en", "vi"))
    generation_budget = min(160, max_length - 1)
    if generation_budget < 1:
        raise ValueError("max_length must leave room for BOS and a generated token")
    with tempfile.TemporaryDirectory(prefix=".freeze-", dir=base) as temporary:
        stage = Path(temporary)
        (stage / "corpus.jsonl").write_text("".join(json.dumps(r.to_dict(), ensure_ascii=False, sort_keys=True) + "\n" for r in approved_rows), encoding="utf-8")
        _write(stage / "inventory.json", approved_inventory)
        _write(stage / "alignments.json", alignments)
        _write(stage / "semantic_frames.json", frames)
        write_split_manifest(stage / "split_manifest.json", manifest)
        read_split_manifest(stage / "split_manifest.json", approved_rows, inventory)
        edge_pairs, path_pairs = _read_alignments(stage / "alignments.json", {r.record_id: r for r in approved_rows})
        for split in ("train", "validation", "test"):
            partition = [r for r in approved_rows if groups[r.split_group_id] == split]
            if {r.language for r in partition} != {"en", "vi"}:
                raise ValueError("each split must contain both pilot languages")
            _build_experiment_batch(partition, cfg, inventory, "cpu", edge_pairs, path_pairs)
        for name in ("corpus.jsonl", "inventory.json", "alignments.json", "semantic_frames.json", "split_manifest.json"):
            os.replace(stage / name, base / name)
    approval = {"schema_version": "tide-jepa-ai-pilot-approval-v1", "approval_kind": "AI-preliminary",
                "human_validated": False, "phomt_used": False, "languages": ["en", "vi"],
                "draft_sha256": draft_sha, "corpus_sha256": manifest.dataset_sha256, "split_sha256": manifest.sha256,
                "inventory_sha256": _canonical_hash(approved_inventory), "alignments_sha256": _canonical_hash(alignments),
                "semantic_frames_sha256": _hash_file(base / "semantic_frames.json"),
                "reviewer_ids": [r["reviewer_id"] for r in reviews],
                "review_files_sha256": {name: _hash_file(base / name) for name in ("review-a.json", "review-b.json", "adjudication.json")},
                "user_authorization": "2026-10-01: user explicitly permits AI authoring/review for a preliminary Vi-En pilot; human review deferred"}
    config_names = []
    root = Path(__file__).resolve().parents[1]
    for seed in seeds:
        for mode in selected_modes:
            for condition_weight in copy_weights:
                mode_latent_weights = latent_weights if mode == "tide" else (1.0,)
                for latent_weight in mode_latent_weights:
                    for transition_balance in transition_balances:
                        for pointer_decoder_mode in pointer_decoder_modes:
                            weight_slug = str(condition_weight).replace(".", "p")
                            latent_slug = str(latent_weight).replace(".", "p")
                            name_prefix = (f"{mode}-aux-{latent_slug}" if condition_latent_objective_weights is not None and mode == "tide"
                                           else mode)
                            if condition_transition_balances is not None:
                                name_prefix += f"-balance-{transition_balance}"
                            if condition_source_pointer_decoder_modes is not None:
                                name_prefix += f"-decoder-{pointer_decoder_mode}"
                            name = (f"{name_prefix}-copy-{weight_slug}-seed-{seed}.json" if custom_matrix
                                    else f"{name_prefix}-seed-{seed}.json")
                            output_name = (f"{name_prefix}-copy-{weight_slug}-seed-{seed}" if custom_matrix
                                           else f"{name_prefix}-seed-{seed}")
                            objective_config = {"mode": mode, **({"source_copy_weight": condition_weight}
                                                                    if condition_weight else {})}
                            if compute_source_copy_term:
                                objective_config["compute_source_copy_term"] = True
                            if condition_latent_objective_weights is not None and mode == "tide":
                                objective_config["latent_objective_weight"] = latent_weight
                            config = {"corpus": "corpus.jsonl", "inventory": "inventory.json", "alignments": "alignments.json",
                                      "frozen_split": "split_manifest.json", "review_gate": "approval.json", "languages": ["en", "vi"],
                                      "output_dir": os.path.relpath(root / "runs" / base.name / output_name, base),
                                      "seed": seed, "model": {"width": model_width, "heads": model_heads,
                                                                "layers": model_layers, "max_length": max_length,
                                                                "source_pointer_decoder": pointer_decoder_mode == "source_pointer"},
                                      "objective": objective_config,
                                      **({"checkpoint_selection_policy": checkpoint_selection_policy}
                                         if checkpoint_selection_policy != "validation_loss" else {}),
                                      "training": {"epochs": epochs, "batch_size": batch_size,
                                                   "learning_rate": learning_rate,
                                                   "transition_balance": transition_balance}}
                            _write(base / name, config)
                            config_names.append(name)
    # Local review files are assertions, not cryptographic proof of reviewer
    # identity. Actual independent Luna dispatch/review evidence is recorded by
    # the project owner; people with write access can alter every local gate.
    _write(base / "approval.json", approval)
    from .experiment import _implementation_identity, _runtime_identity
    implementation = _implementation_identity()
    runtime = _runtime_identity()
    snapshot = base / "implementation-snapshot"
    snapshot.mkdir()
    package_root = Path(__file__).parent
    for name in implementation:
        shutil.copy2(package_root / name, snapshot / name)
    primary_weights = sorted({weight for mode in selected_modes if mode == primary_mode for weight in copy_weights})
    primary_latent_weights = sorted(set(latent_weights)) if condition_latent_objective_weights is not None else None
    primary_transition_balances = list(transition_balances) if condition_transition_balances is not None else ["row_uniform"]
    _write(base / "protocol.json", {"schema_version": "tide-jepa-preliminary-protocol-v3", "configs": config_names,
                                     "modes": list(selected_modes), "seeds": list(seeds), "epochs": epochs,
                                     "primary_quality_mode": primary_mode,
                                     "primary_source_copy_weights": primary_weights,
                                     "primary_transition_balance_modes": primary_transition_balances,
                                     "transition_balance_scope": ("base per-edge token, source-copy, JEPA, alignment, and variance losses; path-composition losses remain unweighted"
                                                                  if condition_transition_balances is not None else "uniform record-row weighting"),
                                     **({"release_holdout_scope": (
                                         "Test paths reverse the action order used in train and validation "
                                         "(TIME:PAST then POLARITY:NEGATIVE); if opened after all validation "
                                         "gates pass, the holdout probes action-order recombination as well as "
                                         "held-out factor combinations and is not a matched estimate of the "
                                         "transition-weighting contrast.")}
                                        if version == "v4.17" else {}),
                                     **({"release_holdout_scope": (
                                         "The release holdout uses the same ordered action paths as train and validation; "
                                         "it probes fresh held-out factor combinations only and does not add an action-order shift.")}
                                        if version in ("v4.18", "v4.19", "v4.20", "v4.21", "v4.22", "v4.23") else {}),
                                     **({"registered_hypotheses": statement["registered_hypotheses"]}
                                        if version in ("v4.18", "v4.19", "v4.20", "v4.21", "v4.22", "v4.23") else {}),
                                     **({"primary_latent_objective_weights": primary_latent_weights}
                                        if primary_latent_weights is not None else {}),
                                     **({"latent_objective_multiplier_scope": [
                                         "jepa", "alignment", "variance", "path_jepa", "path_alignment"]}
                                        if primary_latent_weights is not None else {}),
                                     "approval_sha256": _hash_file(base / "approval.json"),
                                     "config_files_sha256": {name: _hash_file(base / name) for name in config_names},
                                     "implementation_sha256": implementation, "runtime": runtime,
                                     "implementation_snapshot": "implementation-snapshot/",
                                     "checkpoint_selection_policy": checkpoint_selection_policy,
                                     "checkpoint_selection": ("fixed final epoch for every condition; validation losses do not choose the evaluated checkpoint"
                                                               if checkpoint_selection_policy == "fixed_final_epoch" else
                                                               "validation token CE + path token CE + weighted aligned-source token CE; same criterion for all conditions"
                                                               if any(copy_weights) else
                                                               "validation token CE + path token CE; same criterion for all modes"),
                                     "test_policy": "train every registered config; all primary-seed validation generation gates must pass before opening the sealed release holdout; never tune on test",
                                     "model": {"width": model_width, "heads": model_heads, "layers": model_layers,
                                               "max_length": max_length, "batch_size": batch_size,
                                               "learning_rate": learning_rate},
                                     "primary_source_pointer_decoder_modes": list(pointer_decoder_modes),
                                     "generation_max_new_tokens": generation_budget, "human_validated": False,
                                     "decoder_policy": "greedy byte-level UTF-8 constrained decoding; EOS only at complete codepoint boundaries",
                                     "quality_thresholds": {"valid_unicode_rate": 1.0,
                                                            "semantic_checker_coverage_rate": 1.0,
                                                            "single_action_action_fidelity_rate": 0.9,
                                                            "single_action_preservation_rate": 0.9,
                                                            "held_out_path_action_fidelity_rate": 0.8,
                                                            "held_out_path_preservation_rate": 0.8,
                                                            "scope": "each language/action bucket using the narrow synthetic frame checker"},
                                     "compute_policy": ("Decoder-mode conditions share corpus, split, objective, seeds, examples, epochs, and batch order. Vocabulary-softmax and source-pointer variants differ in parameter count and per-token operations; no matched-FLOP claim is made. Log updates, tokens, wall time, and throughput."
                                                        if condition_source_pointer_decoder_modes is not None else
                                                        "TIDE-only conditions share architecture, examples, epochs, seed-wise batch order, and all loss computations; source-copy loss is computed in every condition and only its registered multiplier differs. Updates, tokens, and wall time are logged."
                                                        if compute_source_copy_term else
                                                        "equal examples, epochs, seed-wise batch order and architecture; log tokens, updates and wall time; no matched-FLOP claim")})
    return approval


def validate_review_gate(base, config, manifest, inventory_hash, alignments_hash):
    approval = _read(Path(base) / config["review_gate"])
    if (approval.get("schema_version") != "tide-jepa-ai-pilot-approval-v1"
            or approval.get("approval_kind") != "AI-preliminary" or approval.get("human_validated") is not False
            or approval.get("languages") != config.get("languages")
            or approval.get("corpus_sha256") != manifest.dataset_sha256
            or approval.get("split_sha256") != manifest.sha256
            or approval.get("inventory_sha256") != inventory_hash
            or approval.get("alignments_sha256") != alignments_hash):
        raise ValueError("review gate differs from current corpus/split/inventory/alignment")
    review_hashes = approval.get("review_files_sha256", {})
    if set(review_hashes) != {"review-a.json", "review-b.json", "adjudication.json"}:
        raise ValueError("review gate requires both complete reviews and adjudication hashes")
    if len(set(approval.get("reviewer_ids", []))) != 2:
        raise ValueError("review gate requires two distinct reviewer records")
    if approval.get("phomt_used") is not False:
        raise ValueError("this preliminary gate does not authorize PhoMT training")
    if approval.get("semantic_frames_sha256") != _hash_file(Path(base) / "semantic_frames.json"):
        raise ValueError("semantic frame catalog changed after freeze")
    if any(_hash_file(Path(base) / name) != sha for name, sha in review_hashes.items()):
        raise ValueError("review or adjudication changed after freeze")
    return _hash_file(Path(base) / config["review_gate"])


def _edit_distance(a, b):
    previous = list(range(len(b) + 1))
    for i, char in enumerate(a, 1):
        current = [i]
        for j, other in enumerate(b, 1):
            current.append(min(current[-1] + 1, previous[j] + 1, previous[j - 1] + (char != other)))
        previous = current
    return previous[-1]


def _norm_text(value):
    value = unicodedata.normalize("NFC", value).casefold()
    return " ".join(re.findall(r"\w+", value, flags=re.UNICODE))


def _semantic_frame_flags(text, language, frame):
    """Narrow rule checker over the declared synthetic v4 grammar only."""
    from .pilot_seed import (FAMILIES_V4, FAMILIES_V42, FAMILIES_V43, FAMILIES_V44,
                             FAMILIES_V45, FAMILIES_V46, FAMILIES_V47, FAMILIES_V48,
                             FAMILIES_V49, FAMILIES_V410, FAMILIES_V411, FAMILIES_V412,
                             FAMILIES_V413, FAMILIES_V414, FAMILIES_V415, FAMILIES_V416,
                             FAMILIES_V417, FAMILIES_V418, FAMILIES_V419, FAMILIES_V420,
                             FAMILIES_V421, FAMILIES_V422, FAMILIES_V423)
    event = frame.get("event")
    definition = next((item for family_set in (FAMILIES_V4, FAMILIES_V42, FAMILIES_V43,
                                               FAMILIES_V44, FAMILIES_V45, FAMILIES_V46,
                                               FAMILIES_V47, FAMILIES_V48, FAMILIES_V49, FAMILIES_V410,
                                               FAMILIES_V411, FAMILIES_V412, FAMILIES_V413,
                                               FAMILIES_V414, FAMILIES_V415, FAMILIES_V416,
                                               FAMILIES_V417, FAMILIES_V418, FAMILIES_V419,
                                               FAMILIES_V420, FAMILIES_V421, FAMILIES_V422, FAMILIES_V423)
                       for group in family_set.values() for item in group if item[0] == event), None)
    if definition is None:
        return None
    _, agent_en, base, present, past, patient_en, agent_vi, verb_vi, patient_vi = definition
    normalized = _norm_text(text)
    required_markers = []
    if language == "en":
        agent, patient = agent_en, patient_en
        place = frame.get("place_en")
        progressive = frame.get("predicate_en_progressive")
        if frame["time"] == "past":
            required_markers.append("yesterday")
        else:
            required_markers.append("right now")
        if progressive and frame["time"] != "past":
            verb_phrase = (("is not " if frame["polarity"] == "negative" else "is ") + progressive)
        elif frame["polarity"] == "negative":
            verb_phrase = ("did not " + base) if frame["time"] == "past" else ("does not " + base)
        else:
            verb_phrase = past if frame["time"] == "past" else present
        agent_present = _norm_text(agent) in normalized
        patient_present = _norm_text(patient) in normalized
        predicate_present = _norm_text(verb_phrase) in normalized
        place_present = _norm_text(place) in normalized if place else None
        preservation = agent_present and patient_present and predicate_present
        if place_present is not None:
            preservation = preservation and place_present
        negative = "did not" in normalized or "does not" in normalized or "is not" in normalized
        other_time = "right now" if frame["time"] == "past" else "yesterday"
        action = (all(_norm_text(marker) in normalized for marker in required_markers)
                  and _norm_text(other_time) not in normalized
                  and negative == (frame["polarity"] == "negative"))
    elif language == "vi":
        agent, patient = agent_vi, patient_vi
        place = frame.get("place_vi")
        required_markers.append("hôm qua" if frame["time"] == "past" else "bây giờ")
        progressive_now = (event.startswith("compose423_") and frame["time"] != "past"
                           and frame["polarity"] == "positive")
        verb_phrase = ("không " + verb_vi) if frame["polarity"] == "negative" else (
            ("đã " if frame["time"] == "past" else "đang " if progressive_now else "") + verb_vi)
        agent_present = _norm_text(agent) in normalized
        patient_present = _norm_text(patient) in normalized
        predicate_present = _norm_text(verb_phrase) in normalized
        place_present = _norm_text(place) in normalized if place else None
        preservation = agent_present and patient_present and predicate_present
        if place_present is not None:
            preservation = preservation and place_present
        negative = "không" in normalized.split()
        past_positive = "đã" in normalized.split()
        other_time = "bây giờ" if frame["time"] == "past" else "hôm qua"
        action = (all(_norm_text(marker) in normalized for marker in required_markers)
                  and _norm_text(other_time) not in normalized
                  and negative == (frame["polarity"] == "negative")
                  and (not progressive_now or "đang" in normalized.split())
                  and (frame["time"] != "past" or frame["polarity"] == "negative" or past_positive))
    else:
        return None
    return {"action_fidelity": bool(action), "preservation": bool(preservation),
            "agent_preserved": bool(agent_present), "patient_preserved": bool(patient_present),
            "predicate_preserved": bool(predicate_present), "place_preserved": place_present,
            "checker_scope": "v4 synthetic tense/polarity grammar; event roles and listed surface forms only"}


def _require_release_test_gate(base, protocol, manifest, rows):
    """Keep release-test scoring closed until all registered training and validation gates pass."""
    from .experiment import _canonical_hash, _implementation_identity
    import torch

    base = Path(base)
    config_names = protocol.get("configs", [])
    modes, seeds = protocol.get("modes", []), protocol.get("seeds", [])
    primary = protocol.get("primary_quality_mode")
    if (not config_names or not modes or not seeds or primary not in modes
            or len(config_names) != len(set(config_names))):
        raise ValueError("release holdout remains sealed: frozen protocol registration is incomplete")
    if protocol.get("config_files_sha256") != {
            name: _hash_file(base / name) for name in config_names}:
        raise ValueError("release holdout remains sealed: registered config identity changed")

    registered = [(name, _read(base / name)) for name in config_names]
    try:
        selected_primary = {name for name, _ in _registered_primary_configs(protocol, registered)}
    except ValueError as error:
        raise ValueError(f"release holdout remains sealed: {error}") from error
    primary_configs = []
    for name, config in registered:
        output = (base / config["output_dir"]).resolve()
        latest_path, best_path = output / "latest.pt", output / "best.pt"
        resolved_path = output / "resolved_run.json"
        if not latest_path.is_file() or not best_path.is_file() or not resolved_path.is_file():
            raise ValueError("release holdout remains sealed: every registered training run must finish first")
        latest = torch.load(latest_path, map_location="cpu", weights_only=True)
        best = torch.load(best_path, map_location="cpu", weights_only=True)
        resolved = _read(resolved_path)
        if (latest.get("epoch") != protocol.get("epochs")
                or latest.get("run_sha256") != resolved.get("run_sha256")
                or best.get("run_sha256") != resolved.get("run_sha256")):
            raise ValueError("release holdout remains sealed: a registered run is incomplete or has mixed checkpoints")
        if name in selected_primary:
            primary_configs.append((name, config, output, resolved))

    expected_buckets = set()
    held_out = [row for row in rows if manifest.groups[row.split_group_id] == "validation"]
    paths = {}
    for row in held_out:
        if row.path_id is None:
            expected_buckets.add(f"{row.language}/single/{row.action.kind}:{row.action.value}")
        else:
            paths.setdefault((row.path_id, row.language), []).append(row)
    for (_, language), path_rows in paths.items():
        ordered = sorted(path_rows, key=lambda row: row.path_step)
        actions = "+".join(f"{row.action.kind}:{row.action.value}" for row in ordered)
        expected_buckets.add(f"{language}/held_out_path/{actions}")
    if not expected_buckets:
        raise ValueError("release holdout remains sealed: frozen validation buckets are empty")

    expected_evaluator = {key: value for key, value in _implementation_identity().items()
                          if key in {"pilot.py", "infer.py", "data.py"}}
    protocol_sha = _hash_file(base / "protocol.json")
    for name, config, output, resolved in primary_configs:
        metrics_path = output / "generation_metrics.validation.json"
        private_path = output / "generation.validation.private.jsonl"
        if not metrics_path.is_file() or not private_path.is_file():
            raise ValueError("release holdout remains sealed: validation generation evidence is missing")
        report = _read(metrics_path)
        expected_identity = _canonical_hash({
            "checkpoint_sha256": _hash_file(output / "best.pt"),
            "run_sha256": resolved["run_sha256"],
            "corpus_sha256": manifest.dataset_sha256,
            "split_sha256": manifest.sha256,
            "protocol_sha256": protocol_sha,
            "evaluation_split": "validation",
            "evaluator_sha256": expected_evaluator,
            "decoder_policy": {"max_new_tokens": protocol.get("generation_max_new_tokens", 160),
                               "source_language_equals_target": True},
        })
        checks = report.get("quality_gate", {}).get("bucket_checks", {})
        if (report.get("evaluation_split") != "validation"
                or report.get("primary_for_quality_gate") is not True
                or report.get("human_validated") is not False
                or report.get("_evaluation_identity") != expected_identity
                or set(checks) != expected_buckets
                or set(report.get("scores", {})) != expected_buckets
                or not all(check and all(value is True for value in check.values())
                           for check in checks.values())
                or report.get("quality_gate", {}).get("status") != "pass"):
            raise ValueError("release holdout remains sealed: every primary validation gate must pass on bound evidence")
        for bucket, score in report.get("scores", {}).items():
            task = bucket.split("/", 2)[1]
            prefix = "single_action" if task == "single" else "held_out_path"
            thresholds = protocol.get("quality_thresholds", {})
            required_rates = (
                (score.get("valid_unicode_rate"), thresholds.get("valid_unicode_rate", 1.0)),
                (score.get("checker_coverage_rate"), thresholds.get("semantic_checker_coverage_rate", 1.0)),
                (score.get("action_fidelity_rate"), thresholds.get(f"{prefix}_action_fidelity_rate", 1.0)),
                (score.get("preservation_rate"), thresholds.get(f"{prefix}_preservation_rate", 1.0)),
            )
            if (bucket not in expected_buckets or not score.get("examples", 0)
                    or any(type(rate) not in {int, float} or not math.isfinite(rate)
                           or not 0 <= rate <= 1 or rate < threshold
                           for rate, threshold in required_rates)):
                raise ValueError("release holdout remains sealed: recorded validation scores miss frozen thresholds")


def evaluate_generation(config_path, *, max_new_tokens=160, split="test"):
    """Aggregate automated held-out scores; save generated text only privately."""
    from .experiment import (_canonical_hash, _implementation_identity, _parse_inventory,
                             _runtime_identity)
    from .infer import OfflineGenerator

    path = Path(config_path).resolve()
    if split not in {"validation", "test"}:
        raise ValueError("generation evaluation supports only frozen validation or test splits")
    config = _read(path)
    base = path.parent
    output = (base / config["output_dir"]).resolve()
    inventory = _parse_inventory(_read(base / config["inventory"]))
    rows = read_jsonl(base / config["corpus"], inventory, languages=("en", "vi"))
    manifest = read_split_manifest(base / config["frozen_split"], rows, inventory)
    inventory_value = _read(base / config["inventory"])
    align_path = base / config["alignments"] if config.get("alignments") else None
    alignment_hash = _canonical_hash(_read(align_path)) if align_path else None
    validate_review_gate(base, config, manifest, _canonical_hash(inventory_value), alignment_hash)
    protocol = _read(base / "protocol.json")
    if (protocol.get("implementation_sha256") != _implementation_identity()
            or protocol.get("runtime") != _runtime_identity()):
        raise ValueError("current code/runtime differs from the frozen pilot protocol")
    if max_new_tokens != protocol.get("generation_max_new_tokens"):
        raise ValueError("generation budget differs from the frozen pilot protocol")
    if split == "test":
        _require_release_test_gate(base, protocol, manifest, rows)
    checkpoint_path = output / "best.pt"
    if not checkpoint_path.is_file():
        raise FileNotFoundError("generation evaluation requires best.pt")
    generation_identity = _canonical_hash({"checkpoint_sha256": _hash_file(checkpoint_path),
                                            "run_sha256": _read(output / "resolved_run.json").get("run_sha256"),
                                            "corpus_sha256": manifest.dataset_sha256,
                                            "split_sha256": manifest.sha256,
                                            "protocol_sha256": _hash_file(base / "protocol.json"),
                                            "evaluation_split": split,
                                            "evaluator_sha256": {k: v for k, v in _implementation_identity().items()
                                                                 if k in {"pilot.py", "infer.py", "data.py"}},
                                            "decoder_policy": {"max_new_tokens": max_new_tokens,
                                                               "source_language_equals_target": True}})
    suffix = ".validation" if split == "validation" else ""
    metrics_path = output / f"generation_metrics{suffix}.json"
    private_path = output / f"generation{suffix}.private.jsonl"
    if metrics_path.exists():
        cached = _read(metrics_path)
        if cached.get("_evaluation_identity") != generation_identity or not private_path.is_file():
            raise FileExistsError("generation evaluation evidence already exists with a different identity; create a new run")
        return {k: v for k, v in cached.items() if not k.startswith("_")}
    if private_path.exists():
        raise FileExistsError("partial private generation evidence exists; preserve it and create a new run")
    generator = OfflineGenerator(path, checkpoint_path, device="cpu")
    held_out = [r for r in rows if manifest.groups[r.split_group_id] == split]
    frames = _read(base / "semantic_frames.json")
    accepted_by_frame = {}
    for row in held_out:
        accepted_by_frame.setdefault((row.language, row.target_frame_id), set()).add(row.target_text)
    requests = [(r.language, "single", r.record_id, r.source_text, [r.action],
                 r.source_frame_id, r.target_frame_id, accepted_by_frame[(r.language, r.target_frame_id)])
                for r in held_out if r.path_id is None]
    paths = {}
    for row in held_out:
        if row.path_id is not None:
            paths.setdefault((row.path_id, row.language), []).append(row)
    for (path_id, language), path_rows in sorted(paths.items()):
        ordered = sorted(path_rows, key=lambda r: r.path_step)
        requests.append((language, "held_out_path", path_id, ordered[0].source_text,
                         [r.action for r in ordered], ordered[0].source_frame_id,
                         ordered[-1].target_frame_id,
                         accepted_by_frame[(language, ordered[-1].target_frame_id)]))
    totals, private = {}, []
    for language, task, record_id, source, actions, source_frame, target_frame, references in requests:
        response = generator.generate({"source": source, "source_language": language,
                                       "target_language": language,
                                       "actions": [{"kind": a.kind, "value": a.value} for a in actions],
                                       "max_new_tokens": max_new_tokens})
        generated = response["generated_text"]
        action_key = "+".join(f"{a.kind}:{a.value}" for a in actions)
        bucket = f"{language}/{task}/{action_key}"
        total = totals.setdefault(bucket, {"examples": 0, "accepted_reference_matches": 0,
            "valid_unicode": 0, "terminated_eos": 0, "nonempty": 0,
            "action_fidelity_pass": 0, "action_fidelity_known": 0,
            "preservation_pass": 0, "preservation_known": 0, "checker_coverage": 0,
            "edit_distance": 0, "reference_characters": 0})
        normalized_generated = _norm_text(generated)
        accepted_match = any(normalized_generated == _norm_text(reference) for reference in references)
        best_reference = min(references, key=lambda reference: _edit_distance(generated, reference))
        semantic = _semantic_frame_flags(generated, language, frames.get(target_frame, {}))
        total["examples"] += 1
        total["accepted_reference_matches"] += int(accepted_match)
        total["valid_unicode"] += int(response["valid_utf8"])
        total["terminated_eos"] += int(generator.tokenizer.eos_id in response["generated_token_ids"])
        total["nonempty"] += int(bool(generated.strip()))
        if semantic is not None:
            total["action_fidelity_known"] += 1
            total["preservation_known"] += 1
            total["checker_coverage"] += 1
            total["action_fidelity_pass"] += int(semantic["action_fidelity"])
            total["preservation_pass"] += int(semantic["preservation"])
        total["edit_distance"] += _edit_distance(generated, best_reference)
        total["reference_characters"] += len(best_reference)
        private.append({"record_id": record_id, "language": language, "task": task,
                        "source_frame": source_frame, "target_frame": target_frame,
                        "reference_variants": sorted(references), "semantic_checker": semantic, **response})
    for total in totals.values():
        total["accepted_reference_rate"] = total["accepted_reference_matches"] / total["examples"]
        total["valid_unicode_rate"] = total["valid_unicode"] / total["examples"]
        total["eos_termination_rate"] = total["terminated_eos"] / total["examples"]
        total["nonempty_rate"] = total["nonempty"] / total["examples"]
        total["action_fidelity_rate"] = (total["action_fidelity_pass"] / total["action_fidelity_known"]
                                         if total["action_fidelity_known"] else None)
        total["preservation_rate"] = (total["preservation_pass"] / total["preservation_known"]
                                      if total["preservation_known"] else None)
        total["checker_coverage_rate"] = total["checker_coverage"] / total["examples"]
        total["character_error_rate"] = total["edit_distance"] / total["reference_characters"]
    thresholds = protocol.get("quality_thresholds", {})
    bucket_checks = {}
    for bucket, total in totals.items():
        task = bucket.split("/", 2)[1]
        prefix = "single_action" if task == "single" else "held_out_path"
        required_fidelity = thresholds.get(f"{prefix}_action_fidelity_rate")
        required_preservation = thresholds.get(f"{prefix}_preservation_rate")
        bucket_checks[bucket] = {
            "valid_unicode_pass": total["valid_unicode_rate"] >= thresholds.get("valid_unicode_rate", 1.0),
            "semantic_checker_coverage_pass": (
                total["checker_coverage_rate"] >= thresholds.get("semantic_checker_coverage_rate", 1.0)),
            "action_fidelity_pass": (total["action_fidelity_rate"] is not None
                                      and required_fidelity is not None
                                      and total["action_fidelity_rate"] >= required_fidelity),
            "preservation_pass": (total["preservation_rate"] is not None
                                  and required_preservation is not None
                                  and total["preservation_rate"] >= required_preservation),
        }
    primary_mode = protocol.get("primary_quality_mode", "tide")
    is_primary = config.get("objective", {}).get("mode") == primary_mode
    statement = _read(base / "data_statement.json")
    version = statement.get("version", "synthetic pilot")
    report = {"scope": f"{version} original AI-authored/AI-reviewed synthetic Vi-En {split} evaluation",
              "preliminary": True, "human_validated": False, "phomt_used": False,
              "evaluation_split": split,
              "quality_thresholds": thresholds,
              "primary_for_quality_gate": is_primary,
              "quality_gate": {"status": _quality_gate_status(primary_mode, config.get("objective", {}).get("mode"), bucket_checks),
                               "bucket_checks": bucket_checks},
              "scores": totals,
              "_evaluation_identity": generation_identity,
              "metric_limits": f"The {version} deterministic semantic checker covers only its declared synthetic present/past and polarity grammar plus named roles; checker scores and accepted-reference matches are preliminary, not human naturalness or validation."}
    descriptor, temporary = tempfile.mkstemp(prefix=".generation.private.", dir=output)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            stream.write("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in private))
        os.replace(temporary, private_path)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise
    _write(metrics_path, report)
    return report


def run_suite(directory, *, resume=False):
    import torch
    from .experiment import run_experiment

    base = Path(directory).resolve()
    protocol = _read(base / "protocol.json")
    from .experiment import _implementation_identity, _runtime_identity
    if (protocol.get("implementation_sha256") != _implementation_identity()
            or protocol.get("runtime") != _runtime_identity()):
        raise ValueError("current code/runtime differs from the frozen pilot protocol")
    suite_path = base / "suite_report.json"
    if suite_path.exists():
        saved = _read(suite_path)
        if saved.get("protocol_sha256") != _hash_file(base / "protocol.json"):
            raise FileExistsError("suite report exists for a different protocol; preserve it and create a new version")
        return saved
    if _hash_file(base / "approval.json") != protocol["approval_sha256"]:
        raise ValueError("protocol approval identity changed")
    for name in protocol["configs"]:
        if _hash_file(base / name) != protocol["config_files_sha256"][name]:
            raise ValueError("preregistered config changed")
    torch.set_num_threads(1)
    # Test is reserved until EVERY mode and seed has completed training.
    results = []
    for name in protocol["configs"]:
        config = _read(base / name)
        output = (base / config["output_dir"]).resolve()
        run_experiment(base / name, resume=resume and (output / "latest.pt").is_file(), device="cpu")
    # Score development generation for every registered config first. The
    # release evaluator checks all primary-seed validation gates before it
    # reads or scores any test targets.
    for name in protocol["configs"]:
        evaluate_generation(base / name, max_new_tokens=protocol["generation_max_new_tokens"],
                            split="validation")
    for name in protocol["configs"]:
        result = run_experiment(base / name, resume=True, evaluate_test=True, device="cpu")
        generation = evaluate_generation(base / name, max_new_tokens=protocol["generation_max_new_tokens"])
        results.append({"config": name, "run_sha256": result["run_sha256"], "steps": result["steps"],
                        "validation_generation_loss": result["best_validation_loss"], "test_losses": result["test_metrics"],
                        "generation": generation})
        print(json.dumps({"completed": name, "test_evaluated": True, "human_validated": False}))
    report = {"scope": "AI-reviewed preliminary synthetic Vi-En pilot", "human_validated": False,
              "phomt_used": False, "protocol_sha256": _hash_file(base / "protocol.json"), "runs": results}
    _write(base / "suite_report.json", report)
    return report


def main():
    parser = argparse.ArgumentParser(description="Freeze or run the preliminary AI-reviewed Vi-En pilot")
    parser.add_argument("command", choices=("freeze", "run", "evaluate"))
    parser.add_argument("directory")
    parser.add_argument("--epochs", type=int, default=40)
    parser.add_argument("--model-width", type=int, default=32)
    parser.add_argument("--model-heads", type=int, default=4)
    parser.add_argument("--model-layers", type=int, default=1)
    parser.add_argument("--max-length", type=int, default=192)
    parser.add_argument("--batch-size", type=int, default=80)
    parser.add_argument("--learning-rate", type=float, default=0.001)
    parser.add_argument("--primary-mode", choices=MODES, default="tide")
    parser.add_argument("--source-copy-weight", type=float, default=0.0)
    parser.add_argument("--condition-modes", nargs="+", choices=MODES)
    parser.add_argument("--condition-source-copy-weights", nargs="+", type=float)
    parser.add_argument("--condition-latent-objective-weights", nargs="+", type=float)
    parser.add_argument("--condition-transition-balances", nargs="+",
                        choices=("row_uniform", "unique_transition"))
    parser.add_argument("--condition-source-pointer-decoder-modes", nargs="+",
                        choices=("vocabulary", "source_pointer"))
    parser.add_argument("--checkpoint-selection-policy", choices=("validation_loss", "fixed_final_epoch"),
                        default="validation_loss")
    parser.add_argument("--compute-source-copy-term", action="store_true")
    parser.add_argument("--evaluation-split", choices=("validation", "test"), default="validation")
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    if args.command == "freeze":
        result = freeze_pilot(args.directory, epochs=args.epochs, model_width=args.model_width,
                              model_heads=args.model_heads, model_layers=args.model_layers,
                              max_length=args.max_length,
                              batch_size=args.batch_size, learning_rate=args.learning_rate,
                              primary_mode=args.primary_mode, source_copy_weight=args.source_copy_weight,
                              condition_modes=args.condition_modes,
                              condition_source_copy_weights=args.condition_source_copy_weights,
                              condition_latent_objective_weights=args.condition_latent_objective_weights,
                              condition_transition_balances=args.condition_transition_balances,
                              condition_source_pointer_decoder_modes=args.condition_source_pointer_decoder_modes,
                              checkpoint_selection_policy=args.checkpoint_selection_policy,
                              compute_source_copy_term=args.compute_source_copy_term)
    elif args.command == "run":
        result = run_suite(args.directory, resume=args.resume)
    else:
        base = Path(args.directory).resolve()
        protocol = _read(base / "protocol.json")
        if protocol.get("primary_quality_mode") is None:
            raise ValueError("validation generation requires a frozen primary quality mode")
        evaluations = []
        for name in protocol["configs"]:
            config = _read(base / name)
            output = (base / config["output_dir"]).resolve()
            if not (output / "best.pt").is_file():
                raise FileNotFoundError("finish all preregistered training before generation evaluation")
            if (output / "test_metrics.json").exists():
                raise ValueError("the release test has already been opened; do not use this protocol for tuning")
            measured = evaluate_generation(base / name, max_new_tokens=protocol["generation_max_new_tokens"],
                                           split=args.evaluation_split)
            evaluations.append({"config": name, "status": measured["quality_gate"]["status"],
                                "examples": sum(x["examples"] for x in measured["scores"].values())})
        result = {"evaluation_split": args.evaluation_split, "runs": evaluations,
                  "human_validated": False, "phomt_used": False}
    print(json.dumps({k: v for k, v in result.items() if k != "runs"}, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
