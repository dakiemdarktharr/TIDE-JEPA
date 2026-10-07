# 2026-10-02 audit repair closure

Status: active engineering closure record. Findings are traced to regression coverage and probe evidence; this does not assert that untested bugs cannot exist. The current project-local runtime on Windows is Python 3.11.9 with PyTorch 2.14.0+cpu; after v4.8 implementation changes, 69 unit tests passed with 0 skipped, plus compile and dependency checks. A v4.8 CPU training run was stopped at the user's request before all configurations completed. See [the aggregate-only v4.8 status](../../VI_EN_RESULTS_V4.8_STATUS.md). No v4.8 validation result exists; Q01 remains open and blocks goal completion.

The historical snapshots below are retained as dated records. Current status is summarized in the latest dated checkpoint at the end of this file; the 2026-10-07 v4.25 section supersedes older pending-run statements and prior model-quality status summaries.

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

## 2026-10-07 current audit and v4.23 quality checkpoint

Linux runtime: Python 3.11.17, PyTorch 2.14.0+cpu. The latest full suite remains 112/112 with 0 skips; compileall, `pip check`, and isolated demo-DOM checks passed. The new aggregate action-sensitivity script was run against all 12 saved validation runs and produced 24 language-condition rows without displaying or writing source/generated text. `git diff --check` passed for this update.

| ID | Current status | Evidence and remaining boundary |
|---|---|---|
| E01 | Closed for tested metrics | Denominator regressions remain covered by the 112-test Linux suite. |
| E02 | Partial | Resume/crash recovery is covered; remaining filesystem-publication interruption points lack a full fault-injection matrix. |
| E03–E11 | Closed for tested cases | Identity, split, evaluator, holdout, resource preflight, and schema checks remain bounded to the regression cases documented above. |
| E12 | Partial | Request limits/timeouts are covered; slow/incomplete-body and soak behavior remain untested. |
| E13 | Closed for declared contract | Same-language generation is enforced; cross-language translation is unsupported. |
| E14 | Partial | Isolated DOM behavior is covered; full visual browser integration remains unverified on this host. |
| Q01 | Open; blocks completion | v4.23 had complete checker coverage but 0/120 frozen quality checks passed. Validation-only scoring left its 3,200-record release holdout sealed; no test artifacts exist. A fresh reviewed version is required for further model selection. |
| G01 | Partial | Current Linux CPU suite/compile/dependency evidence passes. Exact clean-source bootstrap exists for an earlier tracked snapshot; fresh OS image, locked transitive dependencies, and GPU remain unverified. |
| G02 | Closed for v4.23 aggregate report | The frozen report verifies all 12 runs and validation identities, separates decoder conditions, and reports aggregate results only. New post-hoc diagnostics are explicitly labeled and do not change the frozen gate. |
| G03 | Updated for v4.23 | README, ROADMAP, spec, pilot/results/history, Ground Truth, vault indexes/log now identify v4.23 as current. Raw historical notes remain unchanged. |
| G04 | Open research gate | No human language evaluation, natural-corpus evidence, matched-FLOP efficacy, or TIDE advantage is established. |
| G05 | External gates remain closed | No PhoMT training/derived action annotation and no Cham training/evaluation occurred. Cham remains deferred pending data-use permission and language/community review. |

v4.23's post-hoc component analysis locates weak patient/predicate retention. Exact output comparison across two distinct requested actions for the same source changed the generated string in 97.7–100% of 640 pairs per language/condition. This argues against a simple “action ignored” explanation but does not prove correct action semantics. Mean final-epoch teacher-forced token-loss gaps were modest; free-generation quality still failed. The latent variance penalty remained nonzero and rose under copy weight 1.5, so under-dispersion is a hypothesis, not proof of total latent collapse. See [v4.23 status](../../VI_EN_RESULTS_V4.23_STATUS.md), [frozen report](../../VI_EN_RESULTS_V4.23_VALIDATION.md), [component diagnostic](../../VI_EN_RESULTS_V4.23_DIAGNOSTIC.md), and [action-sensitivity diagnostic](../../VI_EN_RESULTS_V4.23_ACTION_SENSITIVITY.md). No private rows/generations entered Git. No commit or push was made.

## 2026-10-07 v4.24 checkpoint and resume-log repair

The v4.24 review-bound corpus and protocol identities were verified. Six fixed-final TIDE runs reached epoch 29 / 3,248 updates; `best.pt` and `latest.pt` tensors matched in every run. Six validation-only reports covered 17,280 examples with 100% Unicode, EOS, and checker coverage. The quality gate failed for all six configs (28/60 bucket checks passed); English TIME:NOW preservation was below threshold in all six. The 3,200-record release holdout remains sealed, and the suite exited at the intended fail-closed test gate. See [v4.24 status](../../VI_EN_RESULTS_V4.24_STATUS.md), [aggregate report](../../VI_EN_RESULTS_V4.24_VALIDATION.md), [component diagnostic](../../VI_EN_RESULTS_V4.24_DIAGNOSTIC.md), and [action sensitivity](../../VI_EN_RESULTS_V4.24_ACTION_SENSITIVITY.md).

The post-training audit found duplicate, conflicting epoch/split rows in the v4.24 CSVs for copy-0 seed 17, copy-1.5 seed 17, and copy-1.5 seed 41. Their final checkpoints are complete and matched to the saved validation generation identities, but those three logs cannot support loss-curve or teacher-forced fit claims. `_reconcile_metrics_log` previously accepted repeated rows when both split names existed for an epoch. It now requires exactly one train and one validation row per published epoch, rejects malformed rows, and only discards rows beyond the checkpoint epoch. A regression test appends a duplicate row and verifies that resume fails closed. The historical v4.24 artifacts were not edited. E02 remains partial until a fresh crash/recovery run also proves unique metrics across interruption boundaries.

Linux verification after the fix: 113/113 CPU tests passed with zero skips, including the duplicate-log rejection regression; `compileall`, `pip check`, `git diff --check`, and the synthetic `root_probes.py` run passed. The root probe used only the original synthetic test fixture and verified crash recovery, the single-run release-test gate, and rejection when corpus/split identities are changed. Runtime was Linux x86_64, Python 3.11.17, PyTorch 2.14.0+cpu, CPU-only; NumPy is absent and PyTorch emitted its optional NumPy initialization warning, but `pip check` found no broken requirements and tests/tensor runs passed.

| Gate | Updated status | Evidence |
|---|---|---|
| E02 | Partial; duplicate/missing metric rows now fail closed. Additional publication fault-injection cases remain open. | Regression test rejects a duplicate CSV row; synthetic crash probe still recovers the `latest.pt`/`best.pt` publication window. v4.24 historical logs remain anomalous and unchanged. |
| Q01 | Open; blocks goal completion. | v4.24 completed validation but passed 0/6 full configs and 28/60 buckets. Its 3,200-record release holdout remains sealed. |
| G01 | Partial. | Linux suite, compile, dependency check, and root probe pass. Fresh clean-source bootstrap after the latest source fix and dependency lockfile remain outstanding. |
| G02 | Closed for v4.24 report contract. | 17,280 validation examples, aggregate-only rates/denominators and per-bucket gates recorded; test artifacts absent. |
| G03 | Updated for v4.24. | README, ROADMAP, spec, pilot/results/history, Ground Truth, vault indexes/log, and audit closure now identify v4.24 as current; raw history remains unchanged. |

Raw source/generation text remains private and was not included in this closure. No commit or push was made.

## 2026-10-07 v4.25 quality and evidence checkpoint

The fresh v4.25 corpus/protocol was independently reviewed and frozen; six CPU runs completed at the registered final epoch, and validation-only generation finished for every config. Post-training checks verified the frozen config/protocol identities, checkpoint identity, equal `latest.pt`/`best.pt` tensors, exactly one train and validation metric row per epoch, and no test artifacts. The frozen validation gate failed: **3/6 full-config gates and 44/60 seed-by-bucket checks passed**. Unicode, EOS, and checker coverage were complete. One-pass self-feeding at 0.2 did not consistently improve free-generation preservation over teacher forcing; losses are teacher-forced and do not substitute for autoregressive quality. The release holdout was not evaluated. OOD/refusal behavior was not measured by this validation set. See [v4.25 status](../../VI_EN_RESULTS_V4.25_STATUS.md), [validation](../../VI_EN_RESULTS_V4.25_VALIDATION.md), [component diagnostic](../../VI_EN_RESULTS_V4.25_DIAGNOSTIC.md), and [action sensitivity](../../VI_EN_RESULTS_V4.25_ACTION_SENSITIVITY.md).

| ID | Current status at v4.25 checkpoint | Evidence and remaining boundary |
|---|---|---|
| E01 | Closed for tested metrics | Linux tensor/regression suite passes without skips; aggregate reporting preserves metric-specific denominators. |
| E02 | Partial | Duplicate/missing metric rows fail closed; checkpoint crash recovery and latest/best identity are covered, but all filesystem publication interruption points lack a complete fault-injection matrix. |
| E03–E11 | Closed for tested cases | Identity, grouped split, reviewer/protocol, immutable release holdout, resource limits, generation validation, padding, and schema checks remain bounded to documented regression coverage. |
| E12 | Partial | Tested body/action/token limits, loopback checks, timeouts, and inference-slot recovery; slow/incomplete-body and soak tests remain outstanding. |
| E13 | Closed for declared API contract | Same-language generation is enforced; cross-language translation is unsupported. |
| E14 | Partial | Browser/API and stale-response evidence remains bounded to the previously documented local/simulated paths; full end-to-end visual coverage is incomplete. |
| Q01 | Open; blocks completion | v4.25 fails the frozen validation gate (3/6 configs, 44/60 seed-by-bucket checks); the release holdout remains sealed. No checkpoint is approved for usable language output. |
| G01 | Partial | Linux Python 3.11.17 / PyTorch 2.14.0+cpu suite: 118 tests, 0 skips; compileall and `pip check` pass. The refreshed synthetic root probe confirms crash recovery, `latest`/`best` recovery, the release gate, and stale-review rejection. A clean-source bootstrap after the newest source edits and a complete dependency lock remain outstanding. |
| G02 | Closed for v4.25 validation report contract | The aggregate report separates the two self-feeding rates, lists denominators and per-seed gate outcomes, and records that no holdout/test artifact was produced. |
| G03 | Updated for v4.25 | README, roadmap, specification, pilot/results/history, Ground Truth, vault indexes/log, and this closure now point to the latest failure while preserving prior outcomes. Raw notes remain unchanged. |
| G04 | Open research gate | No human/native-speaker validation, broad natural-corpus evidence, or matched-compute scientific claim exists. |
| G05 | External gates remain closed | PhoMT was not used for training or evaluation. Phan Rang Cham remains deferred pending dataset-use permission and language/community review. |

The pilot remains preliminary AI-authored/AI-reviewed synthetic evidence (`human_validated=false`). All source, generated, and reference rows remain in Git-ignored `data/` and `runs/`; reports contain aggregate metrics only. No commit or push was made.

Linux verification commands for this checkpoint:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m unittest discover -s tests -q
.venv/bin/python -B -m compileall -q tide_jepa tests scripts audits/2026-10-02/root_probes.py
.venv/bin/python -m pip check
.venv/bin/python -B audits/2026-10-02/root_probes.py --output /tmp/rmit-root-probe-v426-20261007.json
git diff --check
```

## 2026-10-07 v4.26 quality and evidence checkpoint

The fresh v4.26 corpus and protocol passed two independent Luna/high AI reviews and artifact-bound adjudication. Six fixed-final TIDE configs completed 29 epochs / 3,248 updates. The first pair of seed-41 output directories showed overlapping/incomplete intermediate writes after an accidentally repeated trainer invocation; those outputs were moved to an ignored quarantine directory and excluded. The two seed-41 configs were then completed from a coherent epoch-19 checkpoint under one process pool. Accepted artifacts across all six configs passed protocol/config/runtime identity checks, exact latest/best tensor equality, 58 unique train/validation rows, and absence of test artifacts. All workers had exited before the integrity audit and validation-only evaluation.

Validation covered 17,280 examples with 100% Unicode, EOS, and semantic checker coverage. The frozen quality gate failed: **1/6 configs and 32/60 seed-by-bucket checks passed**. Source-copy weight 0.25 improved Vietnamese aggregate preservation but lowered English single-action preservation (79.5% to 68.8% when compared with weight 0); English patient retention was 85.3% at weight 0 and 79.1% at 0.25. The same-source action-sensitivity diagnostic found different outputs for all 640 pairs per language/config, which is not proof of semantic correctness. The 3,200-record release holdout remains sealed. OOD/refusal quality was not measured. See [v4.26 status](../../VI_EN_RESULTS_V4.26_STATUS.md), [validation](../../VI_EN_RESULTS_V4.26_VALIDATION.md), [component diagnostic](../../VI_EN_RESULTS_V4.26_DIAGNOSTIC.md), and [action sensitivity](../../VI_EN_RESULTS_V4.26_ACTION_SENSITIVITY.md).

Linux verification for the implementation used in v4.26: Python 3.11.17, PyTorch 2.14.0+cpu; 118 unit tests passed with 0 skips, `compileall`, `pip check`, `git diff --check`, and the aggregate synthetic root probe passed. NumPy is absent and PyTorch emits its optional NumPy initialization warning; no requirements are broken. Tests and software probes establish engineering behavior only, not language quality.

| ID | Current status at v4.26 checkpoint | Evidence and remaining boundary |
|---|---|---|
| E01 | Closed for tested metrics | Denominator/accounting regressions pass the Linux suite; semantic gate remains independent. |
| E02 | Partial | Resume reconciles exact checkpoint epochs; accepted v4.26 logs have unique rows and matching checkpoints. Broader filesystem-publication fault injection and concurrent-run locking remain untested. |
| E03–E11 | Closed for tested cases | Identity, grouped split, review/protocol, immutable holdout, resource preflight, generation validation, padding, and schema checks remain bounded to documented regressions. |
| E12 | Partial | Request limits/timeouts are covered; slow/incomplete-body and soak behavior remain outstanding. |
| E13 | Closed for declared API contract | Same-language generation is enforced; cross-language translation is unsupported. |
| E14 | Partial | Isolated DOM/API evidence exists; full visual browser integration remains unverified on this host. |
| Q01 | Open; blocks goal completion | v4.26 failed with 1/6 full configs and 32/60 bucket checks; no checkpoint is usable and release holdout remains sealed. |
| G01 | Partial | Linux 118-test suite, compile, dependency check, and root probe pass. A blank-host clean bootstrap and complete dependency lock remain outstanding. |
| G02 | Closed for v4.26 report contract | All six runs passed identity/metrics checks; validation report contains per-seed denominators and aggregate metrics only; no test artifacts were created. |
| G03 | Updated for v4.26 | README, ROADMAP, spec, pilot/results/history, Ground Truth, vault indexes/log, and this closure identify v4.26 as current; raw notes and prior results remain unchanged. |
| G04 | Open research gate | No human/native-speaker validation, natural-corpus efficacy, matched-compute scientific claim, or TIDE advantage is established. |
| G05 | External gates remain closed | PhoMT was not used for training/evaluation. Phan Rang Cham remains deferred pending dataset-use permission and language/community review. |

All source, reference, and generated rows remain under Git-ignored `data/` and `runs/`; reports contain only aggregate evidence. No commit or push was made.

Linux verification commands for this checkpoint:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m unittest discover -s tests -q
.venv/bin/python -B -m compileall -q tide_jepa tests scripts audits/2026-10-02/root_probes.py
.venv/bin/python -m pip check
.venv/bin/python -B audits/2026-10-02/root_probes.py --output /tmp/rmit-root-probe-v426-20261007.json
git diff --check
.venv/bin/python -B scripts/train_vi_en_parallel.py data/pilot/vi-en-ai-v4.26 --workers 2
.venv/bin/python -B -m tide_jepa.pilot evaluate data/pilot/vi-en-ai-v4.26 --evaluation-split validation
.venv/bin/python -B scripts/summarize_vi_en_validation.py data/pilot/vi-en-ai-v4.26 VI_EN_RESULTS_V4.26_VALIDATION.md
```

## 2026-10-07 v4.30 frozen training checkpoint

The fresh v4.30 train/validation-only review bundle was inspected independently by two `gpt-6-luna` high reviewers. One approved; the other requested adjudication on duplicate row weighting and English tense forms. An aggregate-only local check confirmed the declared progressive form on all 3,040 present-target records. Past-tense targets correctly use the past form under positive polarity and `did not` plus the base form under negative polarity. Exact source-target duplicates occur as standalone and path-edge rows in the same group/split; the 640 extra validation rows are disclosed as row weighting and are not treated as independent evidence. The release holdout was not inspected.

The initial freeze attempt uncovered a review-binding defect: the reviewer records included the corpus hash, while `REVIEWED_ARTIFACTS` omitted it from the equality check. Added `corpus.draft.jsonl` to the bound artifact set and passed four focused review/freeze regression tests, including current two-review adjudication and incomplete-hash rejection. The exact v4.30 draft then froze successfully with six configs (vocabulary/source-pointer decoders × seeds 17/23/41), fixed 29 epochs, width 64, and CPU runtime identity. Six workers are training; no metrics have been read while training is in progress. Holdout remains sealed; Q01 remains open and no usable checkpoint is approved.

| ID | Current status at v4.30 freeze | Evidence / boundary |
|---|---|---|
| E01 | Closed for tested denominators | Existing metric-denominator regression suite remains in place; v4.30 evaluation still pending. |
| E03 | Closed for the newly observed review-hash omission | `REVIEWED_ARTIFACTS` now includes the corpus and all five metadata artifacts; focused current-review freeze and tamper tests pass. |
| Q01 | Open; blocks goal completion | v4.29 failed its frozen quality gate. v4.30 training and validation are not complete. |
| G01 | Partial | Four targeted review/freeze regression tests pass. Full suite and post-training integrity/evaluation checks remain to run. |
| G02 | In progress | v4.30 protocol is frozen; runs and validation-only aggregate report remain pending. |
| G03 | Updated for the v4.30 freeze | README, ROADMAP, pilot/results, Ground Truth, vault indexes/log, and this checkpoint now distinguish v4.29's failed result from v4.30's active runs. |
| G04–G05 | External/research gates unchanged | No human/native-speaker evidence, matched-FLOP claim, PhoMT training, or Phan Rang Cham use is authorized by this checkpoint. |

The corpus, review records, adjudication, protocol, metrics and weights remain under ignored `data/` and `runs/`. No commit or push was made.

## 2026-10-07 v4.27–v4.29 review-scope incident and remediation

v4.27 was retired after review activity exposed test-split content. v4.28 was also retired before freeze/training after a reviewer parsed the complete semantic-frame catalog and marked holdout annotations inspected. No v4.28 holdout sentence was emitted or evaluated. Both versions remain preserved as incident evidence and are not eligible for a sealed-holdout claim.

v4.29 uses a fresh split and a generated reviewer bundle that contains only train/validation records, frames, groups, alignments, and inventory. Freeze verifies the manifest, content hashes, record count, and split membership; both Luna/high reviewers approved 12,160 rows against the exact bundle and draft hashes without inspecting or emitting holdout text. The adjudication records the action-to-frame mapping and the narrow context checker scope: the declared place marker only, not broader discourse context. Six configurations are frozen (three seeds × language-balance weight 0/1); CPU training has started. No checkpoint integrity audit, validation, or release-holdout evaluation has yet occurred. Q01 remains open and no checkpoint is usable.

The latest Linux suite passed 123 tests with no skips. `compileall`, `pip check`, `git diff --check`, and the synthetic root probe passed. These results establish engineering behavior only. Runtime remains Python 3.11.17 / PyTorch 2.14.0+cpu, with no CUDA and an optional NumPy initialization warning. The v4.8 local artifact hashes match its status note, but its private data/run directories are absent on lattice and its frozen Windows runtime identity differs, so it was not resumed.

No PhoMT rows were used or printed. Phan Rang Cham remains deferred. No commit or push was made.

## 2026-10-07 v4.29 validation and current closure

The v4.29 review-scope remediation passed its frozen checks: both independent Luna/high reviews were bound to the isolated train/validation bundle, and the complete frozen protocol/runtime identities matched before training. All six CPU runs completed at epoch 29 / 3,248 updates. After every worker exited, an integrity audit verified config/approval/code/runtime hashes, resolved run identities, identical `latest.pt` and `best.pt` tensors, complete 29-epoch train/validation metrics, and absence of test artifacts. Validation-only generation completed for all six runs with full identity checking.

The quality gate failed closed. One of six configurations passed all its buckets; 37/60 seed-by-bucket checks passed (22/30 with language-balance weight 0, 15/30 with weight 1). Validation covered 17,280 generated examples. Unicode, EOS, nonempty output, and semantic checker coverage were each 17,280/17,280. Preservation failures were concentrated in English single-action buckets; language-balance weight 1 also regressed Vietnamese seed 41. The 3,200-record release holdout remains sealed, with no test metrics or generated test artifacts. OOD/refusal and truncation quality were not measured. No checkpoint is approved for usable output. See [v4.29 status](../../VI_EN_RESULTS_V4.29_STATUS.md) and the [aggregate-only validation report](../../VI_EN_RESULTS_V4.29_VALIDATION.md).

The aggregate-report review caught a presentation defect in the per-seed diagnostic table: its context-marker column was missing from the header and inherited a stale value from the pooled table. The summarizer now derives the context count from each run/bucket and a regression test checks column alignment. The corrected report was regenerated; validation metrics and the frozen evaluator were not changed.

| ID | Current status | Evidence and remaining boundary |
|---|---|---|
| E01–E11 | Closed for tested cases | Linux unit/probe coverage, frozen identities, split and output gates, run/checkpoint consistency, and v4.29 validation report checks pass within documented test scope. Broader filesystem publication fault injection remains incomplete. |
| E12 | Partial | Request limits, loopback checks, timeouts, and inference-slot recovery have regression coverage; slow/incomplete-body and soak behavior remain open. |
| E13 | Closed for declared API contract | Same-language generation is enforced; cross-language translation is unsupported. |
| E14 | Partial | Diagnostic UI/API behavior has prior local evidence; delayed/stale-response and full visual integration remain unverified. |
| Q01 | Open; blocks goal completion | v4.29 passed 1/6 full configs and 37/60 seed-by-bucket checks. Release holdout is sealed; no checkpoint is usable. |
| G01 | Partial | Linux Python 3.11.17 / PyTorch 2.14.0+cpu suite, compile, dependency, probe, and report regression checks pass. Blank-host bootstrap and a complete dependency lock remain outstanding. |
| G02 | Closed for v4.29 validation report | Six run/evaluation identities and all denominators are verified; report contains aggregates only and confirms no release test artifacts. |
| G03 | Updated for v4.29 | Current docs and indexes point to the failed validation gate and preserve v4.27/v4.28 incident history; raw notes remain unchanged. |
| G04 | Open research gate | No human/native-speaker validation, broad natural-corpus evidence, matched-compute efficacy claim, or TIDE advantage is established. |
| G05 | External gates remain closed | PhoMT was not used. Phan Rang Cham remains deferred pending dataset-use permission and language/community review. |

Linux reproduction commands for this checkpoint:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m unittest discover -s tests -q
.venv/bin/python -B -m compileall -q tide_jepa tests scripts audits/2026-10-02/root_probes.py
.venv/bin/python -m pip check
.venv/bin/python -B audits/2026-10-02/root_probes.py --output /tmp/rmit-root-probe-v429-20261007.json
.venv/bin/python -B -m tide_jepa.pilot evaluate data/pilot/vi-en-ai-v4.29 --evaluation-split validation
.venv/bin/python -B scripts/summarize_vi_en_validation.py data/pilot/vi-en-ai-v4.29 VI_EN_RESULTS_V4.29_VALIDATION.md
git diff --check
```

No PhoMT raw or derived rows were used, printed, or added to versioned reports. No commit or push was made.

## 2026-10-07 v4.30 completion, checker limitation, and current engineering status

All six frozen v4.30 runs completed 29 epochs / 3,248 updates. Protocol, approval, code/runtime/config identities, checkpoint equality, and validation evaluation identities were checked. The frozen validation report recorded 1/6 complete configs and 29/60 seed-by-bucket checks passing. A later train-only negative-control audit found the frozen checker accepted all 1,792 Vietnamese present-progressive references after deleting `đang`, while all 7,168 intact train singles passed. The historical scores remain immutable but are not confirmatory quality evidence. The repaired workspace checker passes all intact train references and rejects all 1,792 progressive deletions; it cannot retroactively validate the frozen protocol. No release holdout output or metric exists. Both the v4.29 and v4.30 release holdouts remain sealed.

The current parallel trainer runs a frozen-checker negative-control preflight before creating a worker pool for train/validation-only review protocols. It therefore rejects the defective frozen v4.30 protocol before launching duplicate training. New confirmatory work requires a fresh reviewed version and protocol. The train-only checkpoint probe on completed v4.29 checkpoints reports exact generation errors in training examples despite very high teacher-forced byte accuracy; source/action/latent interventions affect reference NLL but do not establish JEPA benefit. See [research acceleration](../../RESEARCH_ACCELERATION.md), [checker and checkpoint audit](../2026-10-07/RESEARCH_VALIDATION.md), and [v4.30 status](../../VI_EN_RESULTS_V4.30_STATUS.md).

The full Linux CPU suite passed 140 tests with zero skips. `compileall`, `pip check`, and `git diff --check` passed; runtime was Python 3.11.17 and PyTorch 2.14.0+cpu. The NumPy initialization warning is optional and did not affect tests or probes. E12 and E14 remain partial for slow/incomplete request and stale-response/full-browser integration coverage; G01 remains partial for blank-host bootstrap and fully pinned dependencies. Q01 remains open and blocks goal completion. Human language review, natural-corpus evidence, matched-compute efficacy, PhoMT permission/use, and Cham language/community gates remain external or research dependencies. The AI-reviewed pilot is preliminary and no model is approved as a usable language-output checkpoint.

No PhoMT rows were used, emitted, or committed. Phan Rang Cham remains excluded. No commit or push was made.
