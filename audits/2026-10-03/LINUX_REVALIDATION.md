# Linux revalidation — 2026-10-03

This report adds current-host evidence to the historical 2026-10-02 audit. It does not replace earlier findings or establish pilot quality. All probes used disposable original synthetic fixtures; no PhoMT rows were read, printed, downloaded, or derived, and no Phan Rang Cham data was used.

## Runtime and reproducibility evidence

- Host runtime: Linux `7.2.8-arch1-2`, `x86_64`; Python `3.11.17`; PyTorch `2.14.0+cpu`; CUDA unavailable; six Torch CPU threads.
- `.venv/bin/python -B -m unittest discover -s tests -v`: 77 tests passed, 0 skipped. The suite includes the loopback demo test, CPU tensor tests, release-holdout gate refusal, and v4.9–v4.13 draft split/frame checks. PyTorch emitted a warning that NumPy is not installed; no test failed or was skipped because of it.
- `.venv/bin/python -m compileall -q tide_jepa tests audits/2026-10-02/root_probes.py`: passed.
- `.venv/bin/python -m pip check`: no broken requirements.
- `git diff --check`: passed.
- The probe's explicit-output collision path was manually checked against the existing 2026-10-03 result and refused to overwrite it before creating a fixture.
- `.venv/bin/python -B audits/2026-10-02/root_probes.py --output audits/2026-10-03/root-probe-results-final.json`: passed using a disposable synthetic fixture. The probe confirmed latest checkpoint recovery after a simulated crash, best checkpoint publication after resume, refusal to score the release holdout before all runs finish, and rejection of a changed synthetic evaluation corpus by both evaluator and strict runner. Aggregate evidence: [root-probe-results-final.json](root-probe-results-final.json). The historical `audits/2026-10-02/root-probe-results.json` remains untouched.
- Clean checkout/bootstrap in a fresh environment has not been tested. The current venv already exists; this report does not claim fresh-machine reproducibility.

## Audit status matrix

“Closed” below means the recorded regression/probe evidence covers the stated finding. It is not a claim that every possible failure mode was exhaustively tested. Earlier detailed descriptions remain in [the 2026-10-02 audit](../2026-10-02/AUDIT_SUMMARY.md) and [repair closure](../2026-10-02/REPAIR_CLOSURE.md).

| ID | Current status | Linux evidence / remaining scope |
|---|---|---|
| E01 | Closed for covered metric aggregation | Metric-denominator regression is included in the 77-test suite. |
| E02 | Closed for covered recovery paths | Crash/recovery regression and this run's synthetic root probe pass; not an exhaustive process-kill matrix. |
| E03 | Closed for covered identity drift | Frozen identity tests and probe reject modified corpus/review identity before evaluation. |
| E04 | Closed for tested leakage cases | Fresh/frozen split leakage checks pass in the full suite. |
| E05 | Closed for covered immutable evaluation behavior | Bound/idempotent evaluation identity is enforced. Release-test scoring now requires all registered runs complete and every primary-seed validation generation gate pass; direct-runner and generation APIs are regression-tested to keep the holdout sealed before that gate. |
| E06 | Closed for current-code identity checks | Snapshot/runtime guard tests pass; cross-machine checkpoint migration was not attempted. |
| E07 | Closed for enforced output placement | Protected PhoMT output rejection test passes. No corpus rows were accessed in this revalidation. |
| E08 | Closed for configured batch bounds | Oversized indivisible-group preflight test passes; no stress/peak-memory benchmark was run. |
| E09 | Closed for exact generation argument validation | Invalid EOS/budget and generation checks pass. |
| E10 | Closed for direct encoder padding contract | Left-padding rejection test passes. |
| E11 | Closed for tested schema index validation | Exact-integer edge/pair schema checks pass. |
| E12 | Closed for covered local API requests | Loopback HTTP test and 77-test suite pass; no soak test or adversarial socket-read test was run. |
| E13 | Closed for declared same-language inference contract | Inference identity and request tests pass; cross-language translation remains unsupported. |
| E14 | Partially closed | Interacted with the current demo UI in a local browser using a mock generator: the failed-gate banner, request summary, diagnostic response, and provenance warning displayed correctly. The real trained-checkpoint demo and delayed/stale-response behavior remain unverified. |
| Q01 | Open; blocks completion | v4.8 has no Linux artifacts on this host. v4.10–v4.13 synthetic validation gates fail; all release holdouts remain sealed. v4.13 has no passing single-action bucket. Neural output quality remains unestablished. |
| G01 | Partially closed | Linux OS/Python/Torch, complete CPU suite, compileall and pip check are recorded here. Clean bootstrap is unverified. |
| G02 | Closed for current reporting contract | Aggregate report validator and synthetic/report tests pass; no new model report was generated. |
| G03 | Closed for the recorded documentation snapshot | Existing docs preserve preliminary AI provenance and failed prior gates; this dated report records new Linux evidence without editing raw history. |
| G04 | Open research gates | Matched-FLOP evidence, broader human assessment and scientific efficacy remain unmeasured. |
| G05 | External data/language gates remain closed to use | PhoMT action-label review is not part of this run; Phan Rang Cham remains deferred pending permission and language/community review. |

## v4.8 handoff state

The required local directories `data/pilot/vi-en-ai-v4.8/` and `runs/vi-en-ai-v4.8/` are absent on this Linux host. The status document's hashes cannot substitute for missing corpus, review/adjudication, protocol and checkpoint files. Exact v4.8 resume is therefore not verified and must not be claimed. No artifact was reconstructed and no identity guard was bypassed. Resume that exact run only after those local artifacts are transferred and checked against [the recorded hashes and run state](../../VI_EN_RESULTS_V4.8_STATUS.md). A new pilot requires a new version, fresh independent AI reviews, a frozen protocol and a fresh unopened release holdout.

## Code changes in this revalidation

- `tide_jepa/infer.py` now validates that `actions` is a nonempty list before calling `len`, so malformed top-level values produce the intended request error rather than a Python type error.
- Both release-test evaluation entry points refuse test scoring until all frozen configurations finish and all primary-seed validation reports pass the bound frozen quality thresholds.
- `tests/test_pilot.py` covers malformed top-level action values, malformed action elements, overlong action lists, and rejection before model/tokenizer use.
- `audits/2026-10-02/root_probes.py` now writes default evidence under the current UTC date with a unique timestamp and opens output exclusively. Explicit destinations also refuse overwrite, protecting historical evidence.

No commit or push was made.

## New pilot versions

Because the exact v4.8 artifacts are unavailable on lattice, a new synthetic v4.9 protocol was frozen but superseded before training: the evaluator was hardened after freeze to require validation before any release-test scoring, changing the implementation identity. v4.9 was never run; its holdout remains unopened and its artifacts remain preserved. The frozen protocol was not edited to bypass its identity guard.

A fresh v4.10 corpus under ignored `data/pilot/vi-en-ai-v4.10/` has 7,680 records, a 112/40/40 group split and a factor-disjoint holdout. Two independent Luna reviews and AI adjudication approved the exact draft for preliminary use; all 12 configs completed at 58 epochs / 3,248 updates each. Validation-only evaluation failed the frozen TIDE preservation gate, and the release holdout stayed sealed; see the [v4.10 status](../../VI_EN_RESULTS_V4.10_STATUS.md) and [aggregate validation report](../../VI_EN_RESULTS_V4.10_VALIDATION.md). A direct API check confirmed test scoring refuses to open the release holdout after the validation failure. Both v4.9 and v4.10 use original synthetic text; no PhoMT or Cham data was used. All rows stay private under Git-ignored `data/`.

After v4.10 evaluation, the offline demo was updated to read validation status from its selected checkpoint and show a versioned diagnostic banner instead of the stale hard-coded v4.2 result. The browser flow was checked with a mock response and clearly labels it diagnostic; it was not a trained-model demonstration. This source edit changes implementation identity, so v4.10 remains a completed historical result and must not be resumed or rescored with current code. A new version is required for subsequent experiments.

The v4.10 validation gate failed on single-action preservation, with all 12 frozen runs and validation reports complete. v4.11 used a fresh draft and the preregistered source-copy weight 1.5; its 12-run protocol and validation-only evaluation completed, but every TIDE seed failed the single-action preservation gate. Its release holdout remains sealed. See [v4.11 status](../../VI_EN_RESULTS_V4.11_STATUS.md) and [aggregate report](../../VI_EN_RESULTS_V4.11_VALIDATION.md).

The v4.12 fresh draft was independently approved by two `gpt-6-luna` high reviewers and frozen as a matched 2×2 comparison (`token_only`/`tide` × source-copy weights 0/1.5) across seeds 17/23/41. All 12 runs completed 58 epochs / 3,248 updates with config, protocol, runtime, and checkpoint identities matching. Validation-only generation failed both TIDE weight conditions across the three seeds. Weight 1.5 improved preservation relative to 0, especially for English, but multiple single-action buckets remained below 90%; Unicode and EOS were 100%, and held-out-path buckets met their lower threshold. The direct release-test request was refused before test scoring and no release-test metrics exist. See [v4.12 status](../../VI_EN_RESULTS_V4.12_STATUS.md) and [aggregate report](../../VI_EN_RESULTS_V4.12_VALIDATION.md). The holdout remains sealed; no PhoMT or Cham data was used.

## v4.13 result — 2026-10-04

The fresh v4.13 dose-response pilot completed all 12 registered runs at 58 epochs / 3,248 steps. Config hashes, runtime/implementation identities, and latest/best/resolved checkpoint run identities matched. Validation-only generation completed; the aggregate-only report is [VI_EN_RESULTS_V4.13_VALIDATION.md](../../VI_EN_RESULTS_V4.13_VALIDATION.md). Only 10 of 60 seed-by-bucket checks passed, including one single-action bucket. The other 47/48 single-action buckets missed the 90% preservation gate; three path buckets also failed, while 9/12 paths met their 80% gate. Unicode and EOS were 100%. Pooled preservation favored the matched token-only controls at both weights, though individual buckets and other metrics varied. Each seed reuses the same validation groups, so these counts are operational, not independent linguistic observations; the benchmark has no human confidence intervals or language validation.

The direct release-test API refused scoring before generating test output because bound validation gates failed. No test metrics or test-generation files exist; holdout remains sealed. The report is preliminary AI-reviewed synthetic evidence and does not support a usable natural-language claim. PhoMT and Cham were not used. Two independent Luna agents separately reviewed aggregate results only and recommended preserving failures while considering fresh data/context diversity or objective-balance hypotheses in a new, preregistered version; no threshold or holdout should be altered.

## Linux follow-up — 2026-10-04

After adding the v4.14 four-form authoring path and invariant-place semantic check, `.venv/bin/python -B -m unittest discover -s tests -v` passed 78/78 with no skips; compileall, `pip check`, and `git diff --check` passed. PyTorch warned NumPy is unavailable; tensor tests still ran and passed. Two independent `gpt-6-luna` high reviewers approved the corrected v4.14-r1 draft, after both rejected its first draft for confounding context that changed with tense. The corrected 15,360-row corpus has a fresh 112/40/40 event-group split, invariants recorded in its frames, and a fresh release holdout. All six matched CPU runs completed at 29 epochs / 3,248 updates, and validation-only generation completed. The frozen TIDE gate failed: 4/30 seed-by-bucket checks passed (all four held-out paths); all 24 single-action checks failed. Four of six path checks passed; Unicode and EOS were 100%. Token-only preservation was higher in every pooled bucket. The holdout remains sealed; inspection found no test metrics or generated test files. Two independent Luna agents read only aggregate reports and recommended an objective/loss contribution audit before another fresh, preregistered ablation. See [v4.14 status](../../VI_EN_RESULTS_V4.14_STATUS.md) and the [aggregate report](../../VI_EN_RESULTS_V4.14_VALIDATION.md).


## 2026-10-04 follow-up — v4.15 completion and v4.16 start

The full Linux CPU suite now passes 83/83 with no skips. Its loopback demo test requires binding to `127.0.0.1`; the sandboxed invocation was denied by the environment, then the same suite passed when run with host loopback access. `compileall`, `pip check`, and `git diff --check` pass. PyTorch continues to warn that NumPy is unavailable; the tensor tests ran and passed.

v4.15 completed all nine registered 29-epoch runs and validation-only generation. Its TIDE gate failed (3/60 seed-by-bucket checks passed; no single-action bucket passed preservation), and its fresh release holdout remains sealed. Aggregate report: [v4.15 validation](../../VI_EN_RESULTS_V4.15_VALIDATION.md).

v4.16-r2 was approved by two independent aggregate-only Luna reviews and frozen to protocol SHA-256 `f24214a9582268b0ccea2a5547a79b46aefdfcad48d0ca894de2c06df9338dc0`. The nine registered runs compare token-only with TIDE latent-objective multipliers 0.1/0.25, source-copy weight 1.5, three seeds, and 29 epochs. All nine runs completed at 3,248 updates; config hashes, resolved config, Python/PyTorch runtime identity, and `best.pt`/`latest.pt` presence match. Validation-only evaluation has now started. No release-holdout evaluation has occurred. See [v4.16 status](../../VI_EN_RESULTS_V4.16_STATUS.md).


## 2026-10-05 follow-up — v4.17-r2 validation and next study

The current full Linux CPU suite passes 91/91 with no skips; `.venv/bin/python -B -m compileall -q tide_jepa tests`, `.venv/bin/python -B -m pip check`, and `git diff --check` pass. Runtime remains Python 3.11.17 and PyTorch 2.14.0+cpu; NumPy is absent, and tensor tests did not skip.

v4.17-r2 completed all 12 frozen 29-epoch runs (3,248 updates each) and validation-only generation. Run/protocol/config/runtime/checkpoint identities and 29 train + 29 validation metric rows per run were verified before evaluation. The frozen TIDE gate failed all 60/60 seed × transition-balance × language/task checks. Unicode and EOS were 100%; pooled preservation was 1.44% with row-uniform and 1.12% with unique-transition weighting. The release holdout remains sealed and no test metrics or generations exist. Two independent Luna reviewers read aggregate evidence only; their interpretation is descriptive and preliminary. The aggregate report now includes explicit numeric thresholds and failure reasons. See [v4.17 status](../../VI_EN_RESULTS_V4.17_STATUS.md) and [validation report](../../VI_EN_RESULTS_V4.17_VALIDATION.md).

No PhoMT raw/derived rows or Cham data were used. The next proposed v4.18 is a new synthetic corpus and split, with a frozen 2×2 TIDE auxiliary multiplier (0/0.1) × source-copy supervision (0/1.5), fixed unique-transition weighting, and three seeds. It must be reviewed and frozen before any training; the release holdout stays unopened unless every validation gate passes.


v4.18 received two independent Luna high preliminary approvals and was frozen to protocol SHA-256 `278cefdd57da675211a1a9312701f6892a9d0bcdea14384bc73e35122bb3bb5e`. The 12-config TIDE factorial crosses source-copy weights 0/1.5 with TIDE auxiliary multipliers 0/0.1 across seeds 17/23/41; unique-transition weighting, 29 epochs, and the v4.17 architecture/budget are fixed. All runs completed and identities were verified before validation-only generation. The frozen evaluator omitted v4.18 families, giving zero semantic-checker coverage (`0/0` denominators); its gate failed closed and the result is invalid for semantic interpretation. A post-hoc corrected-checker rescore found action fidelity 26.5–52.5% for single actions and 51.0–72.9% for paths, with preservation 0.4–1.9% and 0.8–8.3%; this is diagnostic, not frozen-gate evidence, and remains below thresholds. The release holdout remains sealed, with no test evaluation. See [v4.18 status](../../VI_EN_RESULTS_V4.18_STATUS.md), [frozen evaluation](../../VI_EN_RESULTS_V4.18_VALIDATION.md), and [post-hoc rescore](../../VI_EN_RESULTS_V4.18_RESCORING.md).

The evaluator's semantic-family registry now includes v4.18, and the release gate requires complete semantic-checker coverage. A regression test checks every authored v4.18 surface form. The Linux CPU suite passes 91/91 with no skips; compileall, pip check, and diff check pass. The post-hoc generation diagnosis found outputs were nonempty, but target patient/predicate preservation was weak. Corrected rescore is diagnostic only because it occurred after the frozen run; a fresh preregistered version must use the corrected evaluator before validation. No holdout was opened.
