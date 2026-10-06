# 2026-10-02 audit repair closure

Status: active engineering closure record. Findings are traced to regression coverage and probe evidence; this does not assert that untested bugs cannot exist. The current project-local runtime on Windows is Python 3.11.9 with PyTorch 2.14.0+cpu; after v4.8 implementation changes, 69 unit tests passed with 0 skipped, plus compile and dependency checks. A v4.8 CPU training run was stopped at the user's request before all configurations completed. See [the aggregate-only v4.8 status](../../VI_EN_RESULTS_V4.8_STATUS.md). No v4.8 validation result exists; Q01 remains open and blocks goal completion.

The historical snapshots below are retained as dated records. Current status is summarized in the 2026-10-06 v4.20 section at the end of this file; that section supersedes earlier statements that v4.16/v4.19 training or validation remained pending.

| ID | Closure evidence | Status |
|---|---|---|
| E01 | Metric-specific sufficient statistics and denominators; `tests/test_pilot.py::test_evaluation_metrics_use_metric_specific_denominators`; aggregate test losses expose token counts. | Closed |
| E02 | Atomic checkpoint/log recovery and latest-to-best reconciliation; interrupted-resume equivalence and crash-recovery tests; `root_probes.py` confirms best checkpoint recovery. | Closed |
| E03 | Generation evaluator re-reads and binds current corpus, split, approval, frames, protocol, checkpoint, decoder, evaluator implementation; modified test corpus rejected by runner and evaluator in root probes. | Closed |
| E04 | Shared frame/text split invariant for fresh grouping and frozen manifests; `test_fresh_grouped_split_rejects_cross_group_frame_and_text_leakage` and `test_frozen_manifest_rejects_corpus_change_and_cross_split_text`. | Closed |
| E05 | Test scoring is immutable/idempotent under a bound evaluation identity; `test_latest_best_crash_recovers_and_test_evaluation_is_immutable`; cached report refuses identity changes. | Closed |
| E06 | Resolved config binds implementation and runtime identities; frozen implementation snapshot and inference/evaluator identity checks reject protocol drift. | Closed |
| E07 | PhoMT-derived output paths are constrained under project `data/`; `test_phomt_protected_output_is_rejected_before_directory_creation`. Pilot reports contain aggregates and generated rows stay private. | Closed for enforced placement and current artifacts |
| E08 | Group-memory/token preflight protects indivisible groups; `test_group_batch_preflight_rejects_large_indivisible_group`. | Closed |
| E09 | Public generation validates integer EOS/budgets and IDs; `test_generation_rejects_fractional_or_boolean_eos_and_budget`. | Closed |
| E10 | Encoder rejects unsupported left padding before positional encoding; `test_direct_encoder_rejects_left_padding`. | Closed |
| E11 | Edge/pair indices require exact integers; schema regression coverage rejects boolean indices. | Closed |
| E12 | Loopback demo bounds request body, socket read, action depth and generation budget, validates Host/Origin and suppresses request text from logs; `test_local_demo_reports_actual_model_and_rejects_invalid_requests`. | Closed for covered request paths |
| E13 | Inference declares source and target language and rejects cross-language requests; `test_train_resume_generate_and_identity_guard`. | Closed |
| E14 | Request snapshot and disabled controls are implemented; a local browser loaded a real v4.19 checkpoint, displayed the failed-gate/provenance banner, and completed one diagnostic generation. | Partially closed; delayed/stale-response behavior remains unverified |
| Q01 | v3 and v4.1–v4.19 quality outcomes are preserved. v4.19 completed 12/12 runs and validation with complete checker coverage, but 0/12 configurations and only 4/120 seed-by-bucket checks passed. The v4.19 release holdout was not generated or scored. | Open; blocks goal completion |
| G01 | A clean tracked-source archive and fresh Python 3.11 virtualenv passed 96 CPU tests with no skips, `compileall`, and `pip check` on Linux; exact commands are in README. | Partially closed; transitive dependencies are not lockfile-pinned, and fresh OS provisioning/GPU remain unverified |
| G02 | `scripts/summarize_vi_en.py` validates registered runs and derives version, split sizes, mode, seed count, CE and gate from evidence; it emits aggregate metrics only. | Closed for current report contract |
| G03 | README, ROADMAP, spec, pilot guide, current results, history, Ground Truth and vault index now distinguish preliminary AI evidence, failed quality gates, and human/external gates. Historical raw notes remain unchanged. | Closed for current state |
| G04 | Matched FLOPs, broader human evaluation, natural-corpus evidence and scientific efficacy remain unclaimed. | Open research gates; not engineering bug closures |
| G05 | PhoMT action approval and Phan Rang Cham permission/language gates remain open. No PhoMT training or Cham generation/evaluation is part of this goal. | External gates remain closed to use |

## Quality evidence sequence

- v3: 0/864 exact matches; 564/864 valid UTF-8. Preserve as immutable historical evidence.
- v4.1: 0 accepted-reference matches and 0 preservation passes on its opened development holdout; no retuning against it.
- v4.2: 12 fixed runs, 0/2,592 accepted-reference matches and 0 preservation passes; all outputs Unicode-valid and EOS-terminated, but semantic quality gate failed. Preserve and do not tune against its opened holdout.
- v4.7: validation failed because some single-action preservation buckets fell below 90%; do not use its opened development evidence as a new test.
- v4.8: training paused by user request. Four/12 configurations completed, four partial, four not started. Validation and release-holdout evaluation have not run. See `VI_EN_RESULTS_V4.8_STATUS.md` for local checkpoint hashes and frozen artifact hashes.

All data-generation, review, training and evaluation rows stay under Git-ignored `data/` or `runs/`. This closure note includes only aggregate status and test names.

## 2026-10-04 Linux evidence review and current residual status

An independent read-only Luna review compared the earlier closure table with current code/tests and Linux records. The 83-test suite, compile check, dependency check, artifact identities, prior synthetic root probes, and aggregate v4.15 report are current evidence. This follow-up preserves the dated historical rows above and records the narrower current status; it does not claim exhaustive failure-mode coverage.

| ID | Current status | Evidence boundary / remaining work |
|---|---|---|
| E01 | Closed for tested denominators | Linux suite covers per-metric denominators. |
| E02 | Partial | Synthetic crash-before-`best.pt` publication and recovery are covered. A fault-injection matrix for other checkpoint/log publication interruption points remains absent. |
| E03–E11 | Closed for tested cases | Identity/evaluator, tested split-leakage cases, holdout gate, runtime snapshot, PhoMT path preflight, batch cap, EOS budget, padding, and schema cases have regression coverage; see dated closure and Linux evidence. This is bounded to tested cases. |
| E12 | Partial | Body/action/token limits, loopback Host/Origin checks, and a 5-second socket timeout are implemented; the loopback test passed with host access. Slow/incomplete-body and soak behavior have not been directly exercised. |
| E13 | Closed for same-language request contract | Cross-language generation remains explicitly unsupported. |
| E14 | Partial | Real v4.19 checkpoint flow and failed-gate/provenance banner were verified in the local browser on 2026-10-06. Delayed/stale response handling remains unverified. |
| Q01 | Open; blocks completion | v4.15 failed validation. v4.16-r2 has a fresh frozen lower-dose protocol and is training; identities must be verified before validation-only evaluation. Keep holdout sealed unless all frozen validation gates pass. |
| G01 | Partial | Linux Python 3.11.17 / PyTorch 2.14 CPU, 83 tests with no skips, compileall and `pip check` pass. Clean-checkout/bootstrap reproduction remains unverified. |
| G02 | Closed for reporting contract | v4.15 aggregate report was generated by the frozen summarizer. Generate and review v4.16 aggregate report after validation; never include private rows. |
| G03 | Partial | Current user-facing status and indexes have been updated; finish reconciling remaining references after v4.16 evaluation. Raw notes remain historical. |
| G04 | Open research gate | No human language evaluation, broad natural-corpus evidence, or matched-FLOP scientific evidence. |
| G05 | Open external gate; restrictions maintained | No PhoMT semantic-action permission and no Phan Rang Cham dataset-use/language review. Neither is used for training/evaluation. |

The v4.17 validation-only report exposes numeric thresholds and per-bucket failure reasons. v4.18 identities were verified before validation-only generation; however, its evaluator omitted v4.18 families, so semantic-checker coverage was zero and the frozen result is invalid for quality interpretation. The gate failed closed. A corrected-checker post-hoc diagnostic remained below all thresholds. The release holdout remains sealed. No threshold was relaxed after observing validation.

## 2026-10-05 v4.19 preregistration checkpoint

Two independent `gpt-6-luna` high reviewers approved the same fresh v4.19 synthetic Vi–En corpus; the new 112/40/40 group split and 12-run matched-computation TIDE factorial are frozen. The protocol uses fixed-final-epoch selection and retains the existing per-bucket quality thresholds. Training and generation have not started, so this adds no new quality evidence and does not close Q01. Keep the release holdout sealed unless every registered validation cell, seed, language, and action bucket passes. The full aggregate protocol identities and reproduction commands are in [v4.19 status](../../VI_EN_RESULTS_V4.19_STATUS.md). No PhoMT or Cham data was used; AI review remains preliminary and is not human validation.

## 2026-10-06 v4.19 validation checkpoint

Training completed all 12 frozen runs at epoch 29 / 3,248 updates each. A post-training identity audit verified configs, approvals, data/split, code/runtime, checkpoint epochs/steps, matching `best.pt`/`latest.pt` weights, and complete train/validation metric epochs for all runs. Validation-only generation then completed 12/12; checker coverage, Unicode, and EOS were 8,640/8,640. The frozen quality gate failed: 0/12 configs passed all buckets and only 4/120 seed-by-bucket checks passed, with preservation the primary failure. The release holdout remains sealed and no test artifacts exist. Q01 remains open. See [aggregate validation report](../../VI_EN_RESULTS_V4.19_VALIDATION.md) and [status](../../VI_EN_RESULTS_V4.19_STATUS.md). The evidence is preliminary synthetic AI review, not human language validation.

## 2026-10-06 local diagnostic-demo checkpoint

The actual v4.19 seed-17 `best.pt` loaded on the Linux CPU host and served only at `127.0.0.1`. A browser smoke confirmed HTTP 200 for the page and health endpoint, the failed-validation diagnostic banner, checkpoint/mode/seed provenance, and the explicit not-human-validated notice. One synthetic same-language request returned HTTP 200, `quality_status=diagnostic_only`, `human_validated=false`, valid UTF-8, 33 generated byte tokens / 25 Unicode characters, in 0.034 seconds. The displayed sample was visibly not reliable language output; it is not included here. A malformed JSON body and a cross-language request were both rejected with HTTP 400. One process RSS observation was 240,880 KiB; this is a single smoke, not a memory or latency benchmark. No input/output text was logged or added to this report. The release holdout was not accessed. E14 now has real-checkpoint browser evidence but remains partial because delayed/stale-response behavior is still untested. E12 remains bounded to tested request paths; slow-body and soak tests are still outstanding. v4.19's failed quality gate means this is not a usable language demo. The server was stopped after the check.

## 2026-10-06 clean Linux source/bootstrap verification

A Git-tracked source archive of commit `925acb1` was extracted to `/tmp` and confirmed to contain neither ignored `data/` nor `runs/`. A fresh Python 3.11 virtualenv installed `requirements-test-cpu.txt` from the official PyTorch CPU package index. From the clean source tree, all 96 tests passed with 0 skipped, `compileall` passed, and `pip check` reported no broken requirements. The first test attempt inside the restricted sandbox failed only because its two loopback tests could not bind `127.0.0.1`; rerunning with host loopback access passed. PyTorch emitted its existing warning that NumPy is not installed; no test uses or skips tensor coverage because of that warning. This closes the documented CPU bootstrap commands for the tested host/source archive, but dependency transitive versions remain resolver-selected and no fresh OS image or GPU environment was tested. Exact Linux commands are in [README](../../README.md#verified-cpu-setup-linux). G01 remains partial at lockfile/system-image scope.


## 2026-10-05 state update

The v4.17-r2 and v4.18 pilots and current Linux suite add evidence but do not close the overall goal. The 92-test CPU suite and compile/dependency checks pass. A fresh Linux synthetic root probe confirmed checkpoint recovery/publication, stale-review rejection, and refusal to open release holdout after only one registered run. v4.17's validation gate failed; v4.18's semantic gate was invalid due zero checker coverage and its corrected post-hoc diagnostic misses thresholds. A train-only one-group overfit check reached 8/8 action-fidelity and preservation on the same seen examples after 600 updates; the script parses all corpus rows to verify split integrity but selects and scores only train examples. It supports memorization capacity only and does not establish generalization. The demo now rejects concurrent inference while a generation is active, covered by a loopback regression test. Q01 remains open and both release holdouts remain sealed. E14 remains partially closed pending real-checkpoint and delayed/stale-response integration evidence. Clean-checkout/bootstrap reproducibility and human/native-speaker validation remain unproven. See [v4.18 status](../../VI_EN_RESULTS_V4.18_STATUS.md), [frozen evaluation](../../VI_EN_RESULTS_V4.18_VALIDATION.md), [post-hoc rescore](../../VI_EN_RESULTS_V4.18_RESCORING.md), [overfit diagnostic](../../VI_EN_RESULTS_V4.18_OVERFIT_DIAGNOSTIC.md), [v4.17 status](../../VI_EN_RESULTS_V4.17_STATUS.md), and the [Linux follow-up](../2026-10-03/LINUX_REVALIDATION.md).

## 2026-10-06 current audit and v4.20 quality checkpoint

Current runtime verification used Python 3.11.17 and PyTorch 2.14.0+cpu. The repaired suite passed 109 tests with 0 skips when run with host loopback access; compileall, `pip check`, isolated browser-DOM checks, and `git diff --check` passed. A sandbox-only attempt failed three HTTP tests at socket bind with `PermissionError`; those tests passed when loopback was enabled. The earlier clean-source bootstrap check remains 96/96 for its archived commit; this 109-test result was run from the current repaired checkout. See [2026-10-06 troubleshooting](../2026-10-06/TROUBLESHOOTING.md).

| ID | Current status | Evidence and remaining boundary |
|---|---|---|
| E01 | Closed for tested metrics | Metric-specific denominators and uniform edge-weight scaling have direct regressions; tensor tests ran without skips. |
| E02 | Partial | Resume/crash recovery and latest/best reconciliation passed regressions and synthetic probes. Other filesystem publication interruption points lack a complete fault-injection matrix. |
| E03–E11 | Closed for tested cases | Corpus/review/protocol/checkpoint/runtime identity, grouped split leakage, immutable test evidence, protected PhoMT output placement, resource preflight, generation argument validation, padding, and exact schema indices have regression coverage. Closure is bounded to tested cases. |
| E12 | Partial | Body/action/token limits, loopback Host/Origin validation, timeout and inference-slot recovery are exercised. Slow/incomplete-body and soak behavior remain untested. |
| E13 | Closed for the declared request contract | Same-language generation is enforced; cross-language translation remains unsupported. |
| E14 | Partial | Delayed response, duplicate submit, submitted-input snapshot and error recovery pass isolated DOM simulation. Visual browser integration could not run because no browser automation/browser is installed on this host. |
| Q01 | Open; blocks goal completion | v4.20 completed six runs and validation generation, but 0/60 frozen seed-by-bucket gates passed. The release holdout remains sealed; no release metrics/generation were produced. A new version needs fresh data, independent reviews, adjudication, protocol and holdout. |
| G01 | Partial | Current 109-test Linux CPU suite, compileall and dependency checks pass. The separate clean-source bootstrap passed 96 tests on commit `925acb1`; dependency transitive versions are not fully locked, and a fresh OS image/GPU remain unverified. |
| G02 | Closed for current aggregate report contract | The v4.20 report verifies registered config/checkpoint/evaluation/protocol identities and every epoch, keeps decoders separate, and reports aggregates only. No release report was created. |
| G03 | Closed for the v4.20 state | Current README, roadmap, pilot/results/history, Ground Truth and vault indexes link the v4.20 failure and preserve older results. Historical raw notes remain unchanged. |
| G04 | Open research gate | No matched-FLOP efficacy claim, broad natural-corpus evidence or human language validation exists. |
| G05 | External gates remain closed | No PhoMT semantic-action labeling/training or Phan Rang Cham training/evaluation occurred. Cham remains deferred pending dataset-use permission and language/community review. |

v4.20 used a fresh AI-authored synthetic corpus and two independent AI reviews. All six fixed-final-epoch runs reached 29 epochs / 3,248 updates; latest/best/resolved identities matched. Validation covered all 8,640 requests per decoder with full checker coverage, Unicode and EOS. The frozen quality gate failed all 60 seed-by-bucket checks. Pooled action fidelity was 42.6% (vocabulary) and 32.5% (source pointer); preservation was 0.57% and 0.45%. The decoder hypothesis was unsupported. These remain preliminary synthetic results, not human validation. See [v4.20 status](../../VI_EN_RESULTS_V4.20_STATUS.md), [aggregate report](../../VI_EN_RESULTS_V4.20_VALIDATION.md), and the explicitly post-hoc [component diagnostic](../../VI_EN_RESULTS_V4.20_DIAGNOSTIC.md). Training did not crash; the fail-closed validation-to-test guard stopped the suite and kept the release holdout sealed.
