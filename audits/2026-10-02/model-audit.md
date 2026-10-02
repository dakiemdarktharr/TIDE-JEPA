# TIDE-JEPA model and runner audit — 2026-10-02

## Scope and evidence

Read `AGENTS.md`, `README.md`, `ROADMAP.md`, `tide_jepa_spec.md`, `VI_EN_PILOT.md`, and `VI_EN_RESULTS.md`. Reviewed `config.py`, `schema.py`, `model.py`, `training.py`, `infer.py`, and the connected `experiment.py` / `data.py` paths plus model, schema, data, and pilot tests.

All probes used small, in-memory synthetic English records and random model weights. No PhoMT rows, private source packets, archive members, pilot corpus rows, generated outputs, or checkpoints were read. No archive was opened or executed. No implementation or test files were changed.

The project docs report 48 CPU tests passing with 0 skips. I inspected the relevant test coverage but did not rerun the full suite. CPU synthetic probes used Python 3.11.9 and PyTorch 2.14.0+cpu through the project venv import path.

Severity: **P1** blocks trustworthy validation or checkpoint selection in supported runner use; **P2** is a reproducible model/API or recovery correctness defect outside the pilot's normal request shape; **P3** is malformed-input validation that is currently inconsistent but has limited workflow exposure.

## Confirmed defects

### P1 — Validation metrics depend on group batch packing

**Location:** [experiment.py](/C:/Users/ANHKHOI/Documents/ChatGPT/RMIT_HACKATHON/tide_jepa/experiment.py:146), especially lines 153–160; the same record-weighted aggregation is used for training logs at lines 343–351. Validation checkpoint selection consumes these values at lines 384–387.

`compute_loss` returns token cross-entropy averaged over non-padding tokens, while path token and alignment components are averaged over paths and pairs. `_evaluate` then multiplies every component by `len(rows)` and divides by record count. This produces the wrong global token mean when batches contain different target lengths, and the wrong path/alignment means when batches have different eligible path or pair counts. It also makes validation results depend on batch size and group packing. Since the checkpoint selector uses validation token and path losses, it can select a different checkpoint from the one selected by the intended corpus-level metric.

**Reproduction:** a synthetic corpus with variable target lengths and group-preserving batch sizes `[1, 3]` yielded runner token CE `5.527216` versus `5.398693` when evaluated as one batch over the same records (difference `0.128523`). No linguistic or private data was involved.

**Repair:** accumulate token CE as a summed loss plus non-padding-token count; accumulate path loss by path count, alignment by pair count, and other per-example terms by their actual unit count. Derive reported aggregate loss and checkpoint-selection loss from those global component means. Apply the same component-aware accounting to epoch metrics. Keep optimizer batching policy separate from metric aggregation.

**Acceptance:** synthetic variable-length records split into unequal group batches must produce the same corpus-level token CE as one-batch evaluation. Add paths and alignments with unequal counts across batches and assert each component matches a direct aggregate. Vary `batch_size` while preserving records and groups; validation metrics and selected checkpoint must not change due solely to packing.

### P2 — Encoder padding invariance fails for left padding

**Location:** [model.py](/C:/Users/ANHKHOI/Documents/ChatGPT/RMIT_HACKATHON/tide_jepa/model.py:48), lines 53–57.

Attention masks padding keys, but position embeddings use raw tensor indices. Prepending a PAD token shifts every valid token's learned position, so the pooled state changes. `Batch.validate` currently requires right padding, which protects the training runner, but direct `SequenceEncoder` callers can provide left padding and the active specification says padding positions cannot affect valid states.

**Reproduction:** the same synthetic token sequence encoded as `[4, 5]` and `[0, 4, 5]` differed by a maximum latent-coordinate delta of `0.386273`; right-padding as `[4, 5, 0]` differed by `0`.

**Repair:** either make valid-token positions independent of padding placement (for encoder and decoder) or explicitly enforce the supported right-padding contract at the model boundary and revise the broader invariance claim. Prefer position IDs derived from valid-token positions if left padding is intended to be supported.

**Acceptance:** assert identical valid outputs when padding is added on any supported side, or assert that unsupported left padding raises a clear `ValueError` before the model computes a state. Keep a regression for right-padding invariance.

### P2 — Checkpoint recovery can lose the best-validation checkpoint

**Location:** [experiment.py](/C:/Users/ANHKHOI/Documents/ChatGPT/RMIT_HACKATHON/tide_jepa/experiment.py:371), lines 374–390.

The runner writes `latest.pt` first with `best_validation` already updated to the current epoch's minimum, then writes `best.pt`. If the process stops between those writes, `latest.pt` says the current epoch is the best but the matching best weights were never saved. Resume restores that score, so it may not save the epoch again; held-out evaluation then fails if `best.pt` is missing or can use an older best checkpoint.

**Reproduction:** on a nine-record synthetic corpus, an injected interruption at the `best.pt` save left `latest.pt` at epoch 1 with a finite best score and no `best.pt`. Resume with `--evaluate-test` failed with `FileNotFoundError: test evaluation requires a completed best-validation checkpoint`.

**Repair:** make the latest/best update recoverable as one transaction, or make resume reconcile the latest epoch's score and weights with the best checkpoint before continuing or evaluating. Do not persist a best score without a recoverable corresponding model state.

**Acceptance:** inject failure after the latest write and before the best write, resume, and verify the selected checkpoint and held-out evaluation match an uninterrupted synthetic run. Also cover interruption after the best write but before the latest write.

### P2 — Fractional EOS IDs pass generation validation

**Location:** [model.py](/C:/Users/ANHKHOI/Documents/ChatGPT/RMIT_HACKATHON/tide_jepa/model.py:157), especially lines 162–165.

The configured BOS is checked with an exact integer type check, but EOS is checked only with numeric range comparisons. `_validate_generation_args(1, 2.5, 4)` accepts a fractional EOS value. Since generated token IDs are integers, the stop comparison can never match `2.5`; generation silently runs to its limit.

**Reproduction:** the direct synthetic validation call above returned successfully for EOS `2.5`.

**Repair:** require exact integer types for EOS (and retain the existing exact BOS check) before range and distinctness checks; reject booleans and floats.

**Acceptance:** tests reject EOS values such as `2.5`, `2.0`, `True`, `None`, negative values, and out-of-vocabulary integers; a valid integer EOS still stops generation immediately.

### P3 — Edge-pair validator accepts boolean indices

**Location:** [schema.py](/C:/Users/ANHKHOI/Documents/ChatGPT/RMIT_HACKATHON/tide_jepa/schema.py:83), lines 86–88.

`validate_pair` checks numeric bounds without checking exact integer types. Python treats booleans as integers, so `EdgePair(True, False, "same_event")` can silently align edges 1 and 0. The path-pair validator already uses exact `int` checks, making the edge-pair contract inconsistent.

**Reproduction:** a two-edge synthetic bilingual fixture passed `EdgePair(True, False, "same_event")` through `validate_pair`.

**Repair:** require `type(left) is int` and `type(right) is int`, matching `validate_path_pair`.

**Acceptance:** reject boolean and non-integer edge indices with `ValueError`; keep valid integer pair behavior unchanged.

## Provenance gap to resolve or document

Training records source hashes for `config.py`, `schema.py`, `data.py`, `model.py`, `training.py`, and `experiment.py` in [experiment.py](/C:/Users/ANHKHOI/Documents/ChatGPT/RMIT_HACKATHON/tide_jepa/experiment.py:255). Inference at [infer.py](/C:/Users/ANHKHOI/Documents/ChatGPT/RMIT_HACKATHON/tide_jepa/infer.py:51) checks the stored hash map against the checkpoint's stored run hash, but does not compare it with the current implementation files; `infer.py` is not in the recorded list either. Thus this is self-consistency checking, not proof that the current inference implementation matches the training implementation. I did not classify this as a confirmed runtime defect because same-shape code changes may remain checkpoint-compatible, but the intended compatibility policy should be made explicit and tested.

## Findings that are not software defects

The preliminary pilot's **0/864 exact matches and 564/864 valid UTF-8 outputs (65.3%)** show that the current model is not a useful controlled generator. The pilot is small, synthetic, AI-authored/AI-reviewed, and reports only automated single-reference metrics. The evidence does not isolate undertraining from byte-level generation limits, model capacity, data size, or other design choices. Treat this as a negative preliminary result, not as proof of a specific code defect. The adapter already masks PAD and BOS during generation and reports invalid UTF-8; these were not reported as defects.

The byte tokenizer does not guarantee that arbitrary generated byte sequences form UTF-8; a validity flag is the current contract. Action semantics, naturalness, and human acceptability remain unmeasured. The pilot's shared sentence patterns and small seed count limit generalization and comparative claims. Any quality work needs a new frozen protocol and untouched evaluation examples; do not tune against the current test scores.

Phan Rang Cham remains deferred. The registry slot is not training or evaluation approval; no Cham actions, data, orthography, or language claims should be added until the separate data-use permission and qualified language review gates are satisfied.

## Coverage and unresolved checks

Existing tests cover objective gradients, teacher forcing, right padding, causal decoding, path composition, alignment licensing, JSONL data contracts, pilot freeze/resume, and basic offline inference identity. They do not cover the five confirmed defects above. The project documentation reports 48 CPU tests passing with 0 skips; this audit did not rerun that suite. GPU behavior, empirical repair effects, and the inference code-drift policy remain unverified.
