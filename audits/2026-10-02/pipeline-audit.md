# TIDE-JEPA pipeline audit — 2026-10-02

## Scope and evidence boundary

Read `AGENTS.md` first. Reviewed `README.md`, `ROADMAP.md`, `tide_jepa_spec.md`, `VI_EN_PILOT.md`; `tide_jepa/data.py`, `experiment.py`, `pilot.py`, `phomt_audit.py`, `phomt_intake.py`, `pilot_seed.py`; and `tests/test_data.py`, `test_pilot.py`, `test_phomt_audit.py`. I also traced `schema.py`, `training.py`, and `infer.py` where needed to assess alignment and metric semantics. No PhoMT archive or private PhoMT authoring packet was opened. Reproductions used synthetic records only and emitted aggregate results, never row text. No archive member was extracted, unpickled, or executed.

The implementation correctly validates edge/path correspondences against explicit frame and action metadata, requires approved records by default, hashes canonical record contents, and confines PhoMT intake output to `data/`. The metadata-only ZIP audit does not decompress or deserialize members by default; source intake checks the approved archive digest and reads only the two declared training members. Git ignore rules cover `/data/`, `/runs/`, and checkpoints. The AI pilot and Cham boundaries in the docs are consistent with `AGENTS.md`.

## Findings

### P1 — a crash between `latest.pt` and `best.pt` can lose the selected checkpoint

**Evidence:** `tide_jepa/experiment.py:359-389` appends epoch metrics, saves `latest.pt`, and then saves `best.pt` if the epoch improves validation. The latest checkpoint already stores the new lower `best_validation` at lines 370-385. If the process stops after the latest save but before the best save, resume restores that lower value and will not promote the latest model to `best.pt` on the next non-improving epoch. The selection state and selected checkpoint can therefore disagree.

**Reproduction:** the root agent's synthetic interruption probe (`audits/2026-10-02/root_probes.py`, results in `root-probe-results.json`) interrupted at this save boundary. Epoch 1 left `latest.pt` present and `best.pt` absent; resume returned successfully at the same completed epoch, then requested test evaluation failed because no best checkpoint existed.

**Repair acceptance:** persist best-selection state and its checkpoint as one recoverable transaction, or make resume reconcile `latest.pt` against the recorded best score and create/update `best.pt` before evaluation. A synthetic interruption at each checkpoint boundary must resume and produce the same final model and best checkpoint as an uninterrupted run.

### P1 — held-out evaluation can be repeated and overwritten

**Evidence:** `tide_jepa/experiment.py:412-427` evaluates the test split whenever `evaluate_test=True` and atomically overwrites `test_metrics.json`; it does not reject an existing test result or bind it to an immutable evaluation record. `tide_jepa/pilot.py:227-243` always loops over test evaluation when `run_suite` is called, even when `suite_report.json` already exists. The docs (`README.md` experiment section and `VI_EN_PILOT.md:19-21`) say to evaluate test once and not tune against it.

**Impact:** repeated calls permit repeated test peeking and replacement of the recorded result. Current suite orchestration does not enforce the stated one-time test policy.

**Repair acceptance:** make first test scoring a one-way state transition tied to the selected checkpoint, frozen protocol, and run identity. A second test-evaluation request must refuse or return the already recorded immutable result without rescoring or overwriting it. Add a synthetic regression for both direct `run_experiment` and suite entry points.

### P1 — token-loss aggregation uses example count instead of the loss denominator

**Evidence:** `compute_loss` in `tide_jepa/training.py:113-116` computes token cross-entropy with padding ignored, so each batch metric is a mean over valid target tokens. `tide_jepa/experiment.py:145-159` then averages batch metrics with `weight = len(rows)`. Training aggregation repeats this at `experiment.py:342-350`. When group-preserving batches have different record counts or target lengths, logged validation loss and checkpoint-selection loss are not the corpus valid-token mean. Path token CE is itself averaged over paths (`training.py:132-160`) and then is also weighted by edge-record count; edge/path alignment metrics are averaged over pairs and then weighted by records. A single row-count denominator is not valid for all metrics.

**Synthetic reproduction:** two one-record batches had 2 and 10 valid target tokens, with controlled per-token losses 0 and 10. `_evaluate` reported `5.0`; the valid-token-weighted reference was `8.333333333333334`. The fixture contained no language data.

**Repair acceptance:** aggregate each reported metric from its sufficient statistics and matching denominator (valid target tokens for token CE, path target tokens or the declared per-path estimand for path CE, pair counts for alignment, and corresponding sample counts for row-level metrics). Use the same documented validation estimand for checkpoint selection. Add unequal-length and unequal-group synthetic regressions that compare runner metrics with a direct full-split calculation.

### P2 — newly generated splits skip the frame and exact-text leakage checks

**Evidence:** `tide_jepa/data.py:303-372` validates records and assigns `split_group_id` groups but does not check frame reuse or normalized sentence reuse between groups. Those checks exist only in `read_split_manifest` at `data.py:393-435`. `experiment.py:218-226` calls `grouped_split` directly whenever no frozen manifest is configured. Thus the validation does not cover the generic runner's normal fresh-split path. The current pilot freeze uses a frozen manifest and receives the stricter check, so this finding concerns fresh generic experiments.

**Synthetic reproduction:** three approved rows with distinct group IDs but identical normalized source/target text and repeated source/target frame IDs were accepted by `grouped_split(seed=7)` and assigned to three distinct splits.

**Repair acceptance:** apply the same cross-split frame and normalized-text checks to generated manifests before returning them (or route generated manifests through the same validator). Add a synthetic case proving a fresh split refuses both repeated frames and repeated normalized text across groups, while records grouped together remain valid.

### P2 — run identity omits review-gate and inference code, runtime versions, and the frozen protocol does not bind implementation hashes

**Evidence:** `tide_jepa/experiment.py:260-263` fingerprints `config.py`, `schema.py`, `data.py`, `model.py`, `training.py`, and `experiment.py`, but omits `pilot.py` even though `validate_review_gate` in that module gates pilot runs. It also omits `infer.py`, which is used for held-out generation scoring. Python and PyTorch versions are recorded in `resolved_run.json` at lines 285-294 but are absent from the identity. Separately, `pilot.py:127-134` freezes approval/config hashes and policy text but no implementation fingerprint. `run_suite` checks those saved files at `pilot.py:219-225`, not that all runs used the same implementation. Consequently code or runtime can drift between mode/seed runs without violating the frozen protocol; a change to `pilot.py` does not invalidate a resumed run identity.

**Repair acceptance:** freeze a digest of all behavior-affecting source files and runtime versions into the protocol before runs start; verify it on every run/resume and require identical implementation identity across the suite. Include review-gate and evaluation/inference code. Preserve an immutable code snapshot or otherwise make the exact implementation recoverable. Add synthetic code-hash drift tests. Keep reviewer identity claims preliminary: the docs correctly state that local review files are assertions, not cryptographic proof, and this audit does not treat that limitation as a bypass vulnerability.

### P2 — experiment output paths are not constrained to private/ignored locations

**Evidence:** `tide_jepa/experiment.py:200-203` resolves `output_dir` directly from config, then `experiment.py:284-296` creates it and writes run metadata and split artifacts; checkpoints and metrics are written there later. There is no check that the destination is in the project's ignored `/runs/` or `/data/` trees. A PhoMT-derived run configured with an ordinary visible project path can therefore place checkpoints or reports outside the stated private locations. This is an accidental-placement risk; the current documented pilot configs point into ignored `runs/`.

**Repair acceptance:** enforce an approved private output root for data-bearing experiments, or make the destination's privacy/ignore status an explicit validated setting that fails before creating files. Add a synthetic path test for an outside-root destination and verify failure occurs before any output is written.

### P2 — `batch_size` is a soft limit with no oversized-group bound

**Evidence:** `tide_jepa/experiment.py:76-94` keeps each `split_group_id` intact and yields an oversized group as one batch. The configured positive `batch_size` is checked at `experiment.py:210-216`, but no record/token/group-size maximum is applied. A large group can exceed the requested size by an arbitrary amount and exhaust CPU/GPU memory during `build_batch` or model forward.

**Repair acceptance:** define and enforce a maximum group/edge/token budget with a clear preflight error, or implement a memory-safe way to retain required path/alignment integrity without materializing the whole group at once. Cover an oversized synthetic group and ensure the limit fails before tensor allocation.

## Alignment, archive, and privacy checks

No alignment correctness defect was confirmed in the reviewed validators: edge pairs must be cross-language with equal source frame, target frame, and action (`tide_jepa/schema.py:83-95`); path pairs must be cross-language and match the complete frame chain and ordered actions (`schema.py:112-138`). The runner checks alignment references and common split groups (`experiment.py:97-120`), and batch grouping keeps a split group together. The generic runner accepts caller-asserted `same_event` metadata; the documentation correctly says that code cannot establish the truth of a human/AI semantic judgment.

No PhoMT row leakage, unpickling, extraction, or archive-content execution occurred in this audit. `phomt_intake.py:64-88` checks count/length parameters, confines outputs beneath `data/`, verifies the expected archive SHA-256, rejects pickle members, and opens only the declared training pair. `phomt_audit.py:25-45, 56-135` rejects traversal, absolute paths, symlinks, encrypted and duplicate normalized members and bounds member count and declared aggregate size. CRC mode streams ZIP bytes but does not extract or deserialize. The test suite has synthetic coverage for these controls; no claim is made about the private archive beyond the docs' recorded audit.

## Coverage gaps

The existing tests cover frozen-manifest text leakage (`tests/test_pilot.py:156-173`), deterministic grouped assignment, review-file drift, valid alignment metadata, and interruption during training followed by epoch-boundary resume (`test_pilot.py:233-267`). They do not cover fresh-split frame/text leakage, metric aggregation with uneven batches or target lengths, interruption between latest and best checkpoint writes, repeated test scoring, implementation/runtime drift across a suite, outside-root run output, or oversized intact groups. `tests/test_pilot.py` creates synthetic review records, so those tests check workflow mechanics rather than reviewer identity. The project docs already label the pilot preliminary and disclose absent human validation, single-reference metric limits, and Cham deferral.

The root agent reports a full CPU suite result of 48 passed, 0 skipped before this audit. This audit independently reproduced only the two synthetic cases documented above plus the checkpoint-boundary result reported in the evidence section; it did not rerun the full suite.

## Copy-ready Luna repair prompt

```text
Use gpt-6-luna with high reasoning effort. Work directly in C:\Users\ANHKHOI\Documents\ChatGPT\RMIT_HACKATHON; do not create subagents.

Read AGENTS.md first, then audits/2026-10-02/pipeline-audit.md, README.md, ROADMAP.md, tide_jepa_spec.md, and VI_EN_PILOT.md. Implement the audit findings in the repository and make the result reviewable. Do not alter the PhoMT archive or private PhoMT authoring packets, and never print, log, or commit PhoMT raw/derived rows. Use only synthetic fixtures for new regression tests. Never unpickle or execute archive contents. Do not use external implementations, pretrained weights, or pretrained tokenizers. Keep the pilot explicitly AI-authored/AI-reviewed and preliminary; do not claim human validation. Keep Phan Rang Cham training/evaluation deferred pending separate use permission and language review.

Fix and cover these findings:
1. Make latest/best checkpoint persistence recoverable across interruption at every save boundary; resume must reconcile the validation selection score and leave an evaluable best checkpoint.
2. Enforce the documented one-time held-out test policy. First evaluation must bind to the selected checkpoint/protocol/run identity and be immutable; a repeat must not rescore or overwrite.
3. Correct training/validation metric aggregation. Use denominators matching each metric's declared estimand, especially valid target tokens for token CE, path-level/token denominators for path CE, and pair counts for alignment. Ensure checkpoint selection uses the correct full-validation metric. Test uneven target lengths and group batches with synthetic fixtures.
4. Apply frame and normalized exact-text cross-split leakage checks to freshly generated splits as well as frozen manifests.
5. Bind all behavior-affecting code and relevant runtime versions into the frozen protocol and run identity, including review-gate and inference/evaluation code; refuse drift on resume and require one implementation identity across suite runs. Keep local AI reviewer records labeled as assertions, not cryptographic identity proof.
6. Prevent experiment outputs derived from protected corpora from being written to unignored/outside private roots; reject unsafe destinations before creating files.
7. Bound oversized split groups/batches before tensor allocation, or implement a memory-safe batching scheme that preserves path/alignment semantics.

Add focused synthetic regression tests for each repair, then run the relevant CPU test suite using the repository's documented Python 3.11 environment/PYTHONPATH. Do not run against or inspect the real PhoMT archive or private packets. Update docs where enforcement or workflow behavior changes. Do not commit. Finish by reporting changed files, test results, any remaining limits, and the exact acceptance criteria that remain unmet.
```
