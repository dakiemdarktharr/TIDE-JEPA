# Linux revalidation — 2026-10-03

This report adds current-host evidence to the historical 2026-10-02 audit. It does not replace earlier findings or establish pilot quality. All probes used disposable original synthetic fixtures; no PhoMT rows were read, printed, downloaded, or derived, and no Phan Rang Cham data was used.

## Runtime and reproducibility evidence

- Host runtime: Linux `7.2.8-arch1-2`, `x86_64`; Python `3.11.17`; PyTorch `2.14.0+cpu`; CUDA unavailable; six Torch CPU threads.
- `.venv/bin/python -B -m unittest discover -s tests -v`: 73 tests passed, 0 skipped, 8.582 seconds. The suite includes the loopback demo test, CPU tensor tests, release-holdout gate refusal, and v4.9/v4.10/v4.11 draft split/frame checks. PyTorch emitted a warning that NumPy is not installed; no test failed or was skipped because of it.
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
| E01 | Closed for covered metric aggregation | Metric-denominator regression is included in the 73-test suite. |
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
| E12 | Closed for covered local API requests | Loopback HTTP test and 73-test suite pass; no soak test or adversarial socket-read test was run. |
| E13 | Closed for declared same-language inference contract | Inference identity and request tests pass; cross-language translation remains unsupported. |
| E14 | Partially closed | Interacted with the current demo UI in a local browser using a mock generator: the failed-gate banner, request summary, diagnostic response, and provenance warning displayed correctly. The real trained-checkpoint demo and delayed/stale-response behavior remain unverified. |
| Q01 | Open; blocks completion | v4.8 has no Linux artifacts on this host, and no validation or release-holdout result exists. Do not open its holdout. Neural output quality remains unestablished. |
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

The v4.10 validation gate failed on single-action preservation, with all 12 frozen runs and validation reports complete. A new v4.11 draft (7,680 synthetic records, 112/40/40 split, three new agent factors) is under ignored `data/pilot/vi-en-ai-v4.11/`. Its copy-supervision weight is set to 1.5 as an unverified hypothesis, not an improvement claim. Two independent `gpt-6-luna` high reviews approved the exact draft; artifact-bound review and adjudication records were written locally. The frozen 12-run 58-epoch protocol completed training, and every run passed config/protocol/runtime/checkpoint identity checks. Validation-only evaluation is running; its release holdout remains sealed. See [v4.11 status](../../VI_EN_RESULTS_V4.11_STATUS.md). The updated 73-test suite, including v4.11 split/grammar regression, passes.
