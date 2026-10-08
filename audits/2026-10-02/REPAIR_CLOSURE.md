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

## 2026-10-08 v4.32 validation, Linux verification, and current closure

v4.32 completed six fixed-final TIDE runs at epoch 29 / 3,248 updates per run. After all workers exited, the training audit verified frozen protocol/config/runtime identities, complete metric epochs, matching `latest.pt`/`best.pt` checkpoints, and no test artifacts. Validation-only generation completed; the frozen quality gate failed. The release holdout remains sealed, no checkpoint is approved for usable output, and the current demo is diagnostic-only. Aggregate evidence is in [v4.32 status](../../VI_EN_RESULTS_V4.32_STATUS.md), [validation](../../audits/2026-10-08/VI_EN_V4.32_VALIDATION.md), and [training audit](../../audits/2026-10-08/training_v4.32_audit.json).

The v4.32 train-only checkpoint report found weak English teacher-forced exactness on train despite high token accuracy. A separate sanity experiment freshly trained the registered TIDE/source-pointer model on one train-only group (8 rows) and four train-only groups (32 rows); both reached full checker action-fidelity and preservation by step 300 and remained there at step 600. This shows the model can memorize small reviewed samples, not that it generalizes or explains full-dataset errors. No validation rows were scored by the sanity experiment, no checkpoint was written, and no release-holdout data was accessed. See [overfit report](../../audits/2026-10-08/V432_TRAIN_GROUP_OVERFIT.md).

### Engineering findings E01–E14

| ID | Reproduction / cause | Repair and regression evidence | Current status |
|---|---|---|---|
| E01 | Pack examples with unequal target lengths; batch means misweight token metrics. | Metric-specific sufficient statistics/denominators; denominator and aggregation regressions pass in the full CPU suite. | Closed for tested metrics. |
| E02 | Inject failure after `latest.pt` publication but before `best.pt`; older code could resume without reconciling the pair/log. | Recovery/reconciliation and duplicate/missing metric-row checks; current synthetic [root probe](../../audits/2026-10-08/root-probe-results.json) confirms recovery after crash-before-best. Other filesystem interruption points and concurrent-run locking lack a full matrix. | Partial; broader fault injection remains. |
| E03 | Change a reviewed evaluation target while retaining stale approval. | Runner/evaluator rebind corpus, split, approval, protocol, checkpoint, decoder and implementation; current root probe confirms both evaluator and runner reject the changed synthetic corpus. | Closed for tested identity paths. |
| E04 | Put duplicate frame/text evidence in separate split groups. | Shared leakage invariants for grouped and frozen splitting; cross-group frame/text leakage regressions pass. | Closed for tested leakage cases. |
| E05 | Re-run an evaluation with changed checkpoint/protocol identity. | Test evidence is immutable/idempotent and bound to evaluation identity; regression coverage rejects changed identities/overwrites. | Closed for tested evaluation paths. |
| E06 | Change source/runtime after freezing a study. | Resolved configs bind source/runtime and frozen implementation snapshots; drift tests reject mismatches. | Closed for the declared identity policy. |
| E07 | Request PhoMT-derived outputs outside the protected project data root. | Protected path validation fails before directory creation; private rows/references remain under ignored `data/`/`runs/`. | Closed for enforced placement and current artifacts. |
| E08 | Submit one oversized indivisible group to batching. | Group/token preflight rejects oversized groups; resource-bound regression passes. | Closed for tested bounds. |
| E09 | Pass fractional/boolean EOS or token budgets to generation. | Exact integer/type/range validation rejects malformed arguments; regression passes. | Closed for tested API inputs. |
| E10 | Left-pad a direct encoder input. | Encoder rejects unsupported left padding before positional encoding; direct-boundary regression passes. | Closed for tested padding contract. |
| E11 | Supply booleans as edge/pair indices. | Schema requires exact integer indices; malformed-index regressions pass. | Closed for tested schema cases. |
| E12 | Send long, malformed, or slow HTTP bodies/action paths. | Loopback-only host/origin checks, body/action/token limits, socket timeout and single-inference bound are implemented and covered by integration tests. A live v4.32 loopback probe confirmed malformed/cross-language/unsupported-action/oversized requests return 400, bad Host/Origin return 403, an incomplete body times out, and `/health` still returns 200. Soak testing remains open. | Partial; slow-client path is directly exercised, soak remains. |
| E13 | Request source/target language mismatch. | Request schema declares both languages and rejects cross-language generation; same-language contract test passes. | Closed for declared API behavior. |
| E14 | Edit form controls while an earlier request is pending. | UI snapshots the submitted request and marks stale state; isolated UI/API checks pass. The v4.32 page was loaded in the local browser and visibly showed the failed-gate diagnostic banner and checkpoint/seed provenance. Delayed-response visual integration remains unverified. | Partial; full delayed/stale browser check remains. |

### Quality, runtime, and project gates

| ID | Current finding and status | Evidence / remaining boundary |
|---|---|---|
| Q01 | Open; blocks goal completion. | v4.32 validation failed its frozen contract. Single-action English preservation is weak; keep its 3,200-row release holdout sealed. No checkpoint is approved for usable language output. |
| G01 | Linux CPU path verified; clean-host scope remains partial. | Host: Arch Linux x86_64, kernel 7.2.8; Python 3.11.17; PyTorch 2.14.0+cpu; CUDA unavailable. Full suite: 142 passed, 0 skipped. `compileall`, `pip check`, synthetic root probe, and `git diff --check` pass. A complete transitive lock, clean OS image, GPU, and fresh bootstrap after all latest uncommitted edits are not evidenced. PyTorch emits an optional NumPy initialization warning; requirements are healthy. |
| G02 | Closed for the v4.32 aggregate report contract. | Report derives registered run/configuration counts and validation denominators from frozen evidence; aggregate-only output records the failed gate and absence of test artifacts. |
| G03 | Current-state reconciliation updated. | README, ROADMAP, spec, pilot, results/history, Ground Truth, indexes, log, and this closure now identify v4.32 and distinguish engineering evidence from quality/external gates. Historical raw notes and prior result reports remain unchanged. |
| G04 | Open research gate. | No human/native-speaker validation, natural-corpus efficacy, matched-compute scientific comparison, or TIDE advantage is established. |
| G05 | External gates remain closed. | PhoMT was not used for training/evaluation; derived action labels remain unapproved. Phan Rang Cham remains excluded pending dataset-use permission and language/community review. |

### M1–M5 disposition

| Milestone | Classification | Evidence / remaining work |
|---|---|---|
| M1 | Engineering complete | Core model and objective controls are implemented and covered by the Linux CPU suite. This is not research-efficacy evidence. |
| M2 | Engineering complete | Ordered action-path composition and path tests are implemented; benchmark benefit is not established. |
| M3 | Engineering complete | Data contracts, approval checks, deterministic group splits, and batch conversion are implemented; data rights remain separately governed. |
| M4 | Preliminary evidence only; acceptance open | v4.32 is AI-authored/AI-reviewed synthetic evidence and failed its quality gate. Natural-corpus data and human linguistic validation are external requirements. |
| M5 | Engineering infrastructure complete only; diagnostic mode | Offline demo has provenance/refusal boundaries but no checkpoint passed the quality contract. Slow-body/soak and full delayed-response browser checks remain incomplete. |

The live v4.32 demo smoke used the frozen seed-17 source-pointer checkpoint on `127.0.0.1:8766`; the browser showed `diagnostic_only`, `validation_gate_status=fail`, and `human_validated=false`. One synthetic same-language request returned 200, valid UTF-8, diagnostic-only provenance, and about 0.015 s for this one call. This is a functional smoke, not a latency/memory benchmark. Malformed JSON, cross-language, unsupported action, excessive token budget, oversized body, invalid Host and Origin were rejected. An incomplete body exceeded the 5-second socket timeout while `/health` continued returning 200. The handler suppresses request/response text in logs. The server was stopped. Semantic OOD/refusal quality remains unmeasured; the UI does not classify arbitrary source sentences as in- or out-of-distribution.

Linux checks for this checkpoint:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m unittest discover -s tests -q
.venv/bin/python -B -m compileall -q tide_jepa tests scripts audits/2026-10-02/root_probes.py
.venv/bin/python -m pip check
.venv/bin/python -B audits/2026-10-02/root_probes.py --output audits/2026-10-08/root-probe-results.json
git diff --check
```

No PhoMT raw/derived rows, corpus text, or generated/reference text were added to this report. No commit or push was made. The goal remains active because Q01 and the listed partial/external gates are not complete.

## 2026-10-08 v4.33 corrected quality gate, release evaluation, and current closure

v4.33 froze a fresh AI-authored English–Vietnamese synthetic corpus, a train/validation-only review bundle, and six fixed-final runs (TIDE/token-only × seeds 17/23/41; 58 epochs). All runs completed. The initial validation report recorded zero semantic-checker coverage because the narrow evaluator registry omitted the new `compose433_` event family. The registry was repaired, generated validation strings were not changed, and an aggregate-only reassessment recomputed checker/action/preservation fields from the cached outputs. The initial evaluator metrics remain immutable evidence. All three primary TIDE runs pass every corrected validation bucket under the original thresholds.

Before opening the release split, a separate v2 amendment bound the original protocol/runtime, configs, split/corpus, all checkpoints and run identities, the current amended evaluator, the corrected validation reassessment, and unchanged quality thresholds. A first release attempt stopped at the checkpoint identity guard before writing test outputs. The amended inference path accepts only the protocol's original implementation identity after the amendment verifies; default inference remains strict. All six registered release configurations were then scored once. All 30/30 primary TIDE release buckets pass; no generation output was used to tune the experiment. Token-only controls were similar, with no consistent TIDE advantage. Aggregate metrics/hashes are in [the checker reassessment](../../audits/2026-10-08/v433_validation_checker_reassessment.json) and [release report](../../audits/2026-10-08/v433_release_holdout_aggregate.json).

The local demo smoke confirmed v4.33 provenance, corrected validation status, diagnostic-only labeling, valid UTF-8 on one synthetic same-language request, and 400 responses for cross-language, malformed JSON, and unsupported action inputs. The browser UI loaded and submitted a request. The stock page default had no exact v4.33 corpus match and produced a semantically corrupted output; that is an observation of an out-of-corpus input, not an in-distribution estimate or human evaluation. The amended runner now loads a train-only example and allows only exact approved train source/action combinations. A fresh direct loopback smoke returned 200 for an approved sample and 400 for unknown source, an unregistered action on a known source, unsupported action, and cross-language input. The earlier browser smoke confirmed the train-only default returned valid UTF-8 and passed the narrow checker. A separate real-browser test with a deliberate two-second response delay verified that editing the source during inference does not mutate the submitted request and the result is visibly marked as belonging to the previous form state. This exact membership gate is not semantic OOD detection; naturalness and human evaluation remain unverified, so the checkpoint stays diagnostic-only and is not approved for natural-language or translation use. The preview server is left running for the user. See [demo evidence](../../audits/2026-10-08/v433_demo_smoke.json).

### Consolidated audit E01–E14, Q01, G01–G05

| ID | Reproduction / root cause or dependency | Repair, regression, and current evidence | Status / boundary |
|---|---|---|---|
| E01 | Aggregate batches with unequal target lengths; batch-mean metrics use the wrong denominator. | Metric-specific numerators/denominators are retained; `test_evaluation_metrics_use_metric_specific_denominators` and report regressions pass. | Closed for tested metrics; new metrics need their own denominator audit. |
| E02 | Exit between `latest.pt`, `best.pt`, and metrics publication; orphan temp files or concurrent writers can leave inconsistent state. | Run lock, reconciliation, synced atomic writers, first-run restart/archive, `best.pt` reconstruction, and temp cleanup are covered by fault-injection and four `os._exit` points. Root probe recovered latest/best and refused a single-run release gate. | Closed for audited process-crash/error paths. Physical power loss and filesystem/platform-specific durability remain unverified. |
| E03 | Change corpus/evaluation text after review while retaining stale approval identities. | Frozen runner and evaluator rebind corpus, split, review, protocol, checkpoint, decoder, and implementation; root probe confirms both refuse the changed synthetic corpus. | Closed for tested identity paths. |
| E04 | Place duplicate frame or normalized text in separate split groups. | Shared grouped/frozen split leakage checks reject cross-split frame/text collisions; `test_fresh_grouped_split_rejects_cross_group_frame_and_text_leakage` passes. | Closed for tested leakage cases. |
| E05 | Repeat evaluation with changed checkpoint/protocol or overwrite existing results. | Identity-bound immutable evaluations and overwrite guards are covered by `test_train_resume_generate_and_identity_guard` and aggregate reporter regressions; release aggregate records evaluator/checkpoint hashes. | Closed for tested overwrite/evaluation paths. |
| E06 | Change source/runtime after freezing a study. | Resolved configs, protocol, and snapshots bind source/runtime; drift regressions reject mismatches without executing frozen snapshots. | Closed for declared identity policy. |
| E07 | Direct PhoMT-derived writes outside protected project data roots. | Protected-path validation rejects before directory creation; raw/derived PhoMT content remains in ignored `data/`; no PhoMT-derived rows were used for v4.33. | Closed for enforced placement/current artifacts. |
| E08 | Submit an indivisible batch group exceeding the resource budget. | Preflight rejects before training; `test_group_batch_preflight_rejects_large_indivisible_group` passes. | Closed for tested bounds. |
| E09 | Pass fractional, boolean, missing, negative, or oversized EOS/token budgets. | Exact type/range validation rejects malformed generation arguments; `test_generation_rejects_fractional_or_boolean_eos_and_budget` passes. | Closed for tested API inputs. |
| E10 | Left-pad direct encoder inputs. | Encoder rejects unsupported padding before positional encoding; `test_direct_encoder_rejects_left_padding` passes. | Closed for declared padding contract. |
| E11 | Supply boolean/fractional edge or path indices. | Schema requires exact integer indices; malformed alignment regressions pass. | Closed for tested schema cases. |
| E12 | Send oversized, malformed, incomplete, slow, or concurrent HTTP bodies/actions. | Loopback/Host/Origin checks, request/action/token limits, socket timeout, and one-inference bound are tested. The historical five-minute soak passed 3,132/3,132 requests; a repeated 300-second current-runner soak passed 3,219/3,219 requests (all valid UTF-8; p95 103.5 ms, p99 108.7 ms, max 143.8 ms) with 30/30 diagnostic-only health checks ([soak report](../../audits/2026-10-08/v433_live_loopback_soak_repeat.json)). Current request smoke confirms `/health` and page 200, an approved train-only request with valid UTF-8 and positive narrow checker flags, and 400 for unknown-source/cross-language requests ([checker smoke](../../audits/2026-10-08/v433_current_loopback_smoke_v3.json), [health/allowlist smoke](../../audits/2026-10-08/v433_current_loopback_smoke_v2.json)). A 19-case aggregate-only boundary smoke passed the exact train example and expected refusals for text variants, plausible out-of-corpus input, action/token limits, malformed/oversized bodies, bad Host/Origin, and unsupported content type ([report](../../audits/2026-10-08/v433_demo_boundary_smoke.json)). Two bounded 240-request runtime runs returned 240/240 HTTP 200 responses each; RSS sampled 14 times per run remained at 85,520 KiB, with p95 latency 106.920 ms and 106.642 ms ([run 1](../../audits/2026-10-08/v433_demo_runtime_benchmark_3.json), [run 2](../../audits/2026-10-08/v433_demo_runtime_benchmark_4.json)). A new 4-client/80-request approved-default benchmark repeated twice returned one 200 and 79 schema-valid 503 busy refusals in each run; the repeated run increased RSS by 112 KiB after an initial 1.6 MiB warm-up ([run 1](../../audits/2026-10-09/v433_demo_concurrent_bound.json), [run 2](../../audits/2026-10-09/v433_demo_concurrent_bound_repeat.json)). | Partial: broad semantic OOD detection, natural/arbitrary payloads, and production capacity remain open. Repeated synthetic varied-input and overload tests have narrow checker and RSS evidence; concurrent overload is safely refused with HTTP 503 rather than queued. |
| E13 | Request source/target language mismatch. | Request schema rejects cross-language calls; live v4.33 smoke returned HTTP 400; unit contract tests pass. | Closed for declared API behavior; product supports same-language transforms, not translation. |
| E14 | Edit UI controls while an earlier inference request is pending. | UI snapshots the submitted request and visibly marks stale results; real-browser delayed-response test and DOM regression pass. | Closed for the tested path; broader browser/device coverage remains untested. |
| Q01 | Evaluate v4.33 against frozen single-action/path thresholds, then test release only after validation passes. | Corrected validation passed 3/3 TIDE seeds; 30/30 release buckets passed with Unicode/EOS/checker coverage complete. Reports preserve aggregates only; token-only was similar, with no consistent TIDE advantage. | Narrow synthetic gate passed. A separate two-reviewer Luna sample review found 47/48 outputs naturalness-acceptable and 48/48 passing sampled meaning/action checks, with one spelling issue. Usable-language acceptance remains open: this is not human/native-speaker validation, broad OOD, natural-corpus quality, or efficacy evidence; demo is diagnostic-only. |
| G01 | Rebuild from the pinned Linux CPU lock using a source-only snapshot, then run suite/compile/dependency checks. | Arch Linux / Python 3.11.17 / PyTorch 2.14.0+cpu: a newly created virtualenv installed from the pinned CPU lock ran the refreshed 219-source-file snapshot (including current scripts/tests; no `.git`, `.venv`, `data/`, or `runs/`): 154 tests passed with zero skips, plus `compileall` and `pip check`. The project `git diff --check` passes. See the [2026-10-09 final source-only reproduction report](../../audits/2026-10-09/linux-source-only-final-reproduction.json). | Linux CPU source/bootstrap path verified for the current uncommitted tree; clean OS-image bootstrap and CUDA remain unverified. |
| G02 | Recompute aggregate release report from frozen evaluation identities and denominators. | Aggregate-only v4.33 report binds six configs, 2,880 examples/config, ten buckets/config, checkpoints, evaluators, amendment, and result hashes. | Closed for v4.33 report contract; private rows/generated text remain ignored. |
| G03 | Reconcile current behavior across README, roadmap, spec, pilot/results/history, Obsidian, and audit closure. | Current documentation identifies v4.33, narrow synthetic pass, diagnostic-only demo, negative TIDE finding, and external gates; historical incident notes remain preserved. | Updated at this checkpoint; future evidence changes need another reconciliation. |
| G04 | Require independent language evaluation, broad OOD testing, and a matched-compute comparison before efficacy claims. | Current AI-authored/AI-reviewed synthetic evidence is explicitly preliminary; no unsupported use is advertised by the demo. | Open research gate; human/native-speaker review, natural-corpus efficacy, broad OOD, matched-compute evidence, and TIDE advantage are absent. |
| G05 | Verify rights and language/community review before using additional datasets or Cham. | PhoMT was excluded from v4.33; 160 private source packets remain pending with no action labels/training approval. Cham was not used. | External gates remain closed; Phan Rang Cham stays deferred pending dataset-use permission and language/community review. |

### M1–M5 disposition

| Milestone | Classification | Evidence / remaining work |
|---|---|---|
| M1 | Engineering complete | Model and objective controls pass the Linux CPU suite; this is not efficacy evidence. |
| M2 | Engineering complete | Ordered path objective and evaluator behavior are tested; TIDE advantage is unproven. |
| M3 | Engineering complete | Approval gates, grouped splits, data integrity, and training/recovery paths pass tested cases. Dataset rights remain separate. |
| M4 | Preliminary evidence only; external acceptance open | The narrow synthetic validation and release contract pass, but human bilingual review, natural-corpus evidence, and scientific effect are absent. |
| M5 | Diagnostic infrastructure complete; quality boundary open | Offline loopback demo has provenance, protocol guards, an exact train source/action allowlist, and a directly tested stale-response warning. The old out-of-corpus page sample produced corrupted output; broad semantic OOD remains open. |

Current Linux reproduction checks:

```sh
.venv/bin/python -B -m unittest discover -s tests
.venv/bin/python -B -m compileall -q tide_jepa scripts tests
.venv/bin/python -m pip check
.venv/bin/python -B audits/2026-10-02/root_probes.py --output audits/2026-10-08/root-probe-results-v433-fsync-manifest.json
.venv/bin/python -B scripts/rescore_v433_validation_checker.py data/pilot/vi-en-ai-v4.33
.venv/bin/python -B scripts/evaluate_v433_release_holdout.py
.venv/bin/python -B scripts/run_v433_demo.py --port 8765
git diff --check
```

The release aggregate command rechecks immutable cached results; it does not regenerate model output. The demo command binds only to loopback and is diagnostic-only. No commit or push was made. The goal remains active because human/semantic quality, OOD, clean-host/bootstrap, and soak acceptance remain open.

### 2026-10-08 continuation: recovery probe and PhoMT intake state

The post-lock synthetic root probe was rerun against the original one-epoch fixture. Resume recovered `latest.pt` after the injected crash, reconstructed `best.pt`, and preserved epoch/step identity. The release-test gate refused with only one registered run, and both the strict runner and evaluator rejected a modified evaluation corpus. Aggregate evidence is in [the post-lock root probe](../../audits/2026-10-08/root-probe-results-v433-postlock.json). This covers the named synthetic paths; broader filesystem interruption points and actual power-loss durability remain outside the probe.

The pinned PhoMT archive is now restored under Git-ignored `data/`, hash-verified, and CRC-checked. A deterministic train-only intake created 160 private source packets; all remain pending, with no action labels, approval, training, or evaluation. Only the paired detokenized train members were streamed; dev/test members were not opened. No archive extraction or deserialization occurred. Translation pairs are source material, not semantic-action labels. See [archive metadata/CRC audit](../../audits/2026-10-08/phomt_archive_audit.json) and [current intake state](../../audits/2026-10-08/phomt_current_availability.json). This updates the earlier absence state without changing historical notes.

No PhoMT rows or generated/reference text were emitted to chat, logs, versioned reports, or Git. No commit or push was made. The goal remains active: the v4.33 model is diagnostic-only, natural-language semantic quality and human review remain unproven, and the 160 source packets cannot enter training until semantic actions are independently authored/reviewed and approved.

The follow-up E02 tests inject `os.replace` and file/parent-directory `fsync` failures through the training-run atomic publication helper used for split manifests, resolved-run JSON, metrics CSV, and checkpoints. The standalone data-authoring manifest helper remains atomic without fsync durability. Pre-rename failures preserve the previous destination and remove the temporary file; post-rename directory-sync failures propagate while leaving the complete new destination visible. Separate-process regressions call `os._exit` before initial metrics publication, after durable metrics publication, after durable `latest.pt` publication, and after the epoch-2 metrics temp file is synced but before rename. Resume safely restarts with no checkpoint/log, archives orphan metrics or reconstructs `best.pt`, cleans the abandoned temp under the run lock, and continues without duplicate rows. With host loopback enabled, the complete Linux suite passed 150 tests with zero skips in both the project environment and pinned-lock source-only snapshot; compileall and pip check passed in both, and `git diff --check` passed in the project. The synthetic root probe passed after the durability changes: resume recovered latest/best, the single-run release gate remained closed, and both runner/evaluator rejected the changed synthetic corpus ([evidence](../../audits/2026-10-08/root-probe-results-v433-experiment-manifest-atomic.json)). These checks exercise process-level interruption/error paths; they cannot prove power-loss behavior on physical storage or every filesystem.

The v4.33 local demo health check on loopback port 8765 returns HTTP 200 and reports operational status, v4.33, diagnostic boundary (`human_validated=false`, `phomt_trained=false`), and its approved train-only default sample. The process is left running at `http://127.0.0.1:8765`; this is availability evidence only, not linguistic quality evidence.

Final same-checkout Linux regression rerun on 2026-10-08: `.venv/bin/python -B -m unittest discover -s tests -q` passed 150/150 with zero skips when run with the authorized host loopback capability. The default sandbox blocks local socket binds, which produces three `EPERM` errors in demo HTTP tests; these are execution-policy failures, not product test failures. `compileall`, `pip check`, `node tests/demo_ui.test.js`, and `git diff --check` passed on the same working tree. The 48-case AI-review packet was independently regenerated with SHA-256 `3af4273d31d6878b305446533946419b7617abdcb8819dd7e357cefc3153b018`; the sampler emitted aggregate metadata only.

Final source-only follow-up on 2026-10-09: four regression tests now cover review-form agreement coefficients, four-stratum aggregation, refusal of changed/missing ratings, and omission of example text/free-text notes. The refreshed 219-source-file snapshot passed 154/154 tests with zero skips, `compileall`, and `pip check` in a newly created virtualenv installed from the pinned Python 3.11/PyTorch 2.14 CPU lock; it excluded `.git`, `.venv`, `data/`, and `runs/`. PyTorch emitted a non-fatal warning because NumPy is not in the pinned lock. See [the final reproduction report](../../audits/2026-10-09/linux-source-only-final-reproduction.json). The loopback, uncommitted-tree, clean-OS-image, and CUDA limitations stated above still apply.

For the remaining human-language gate, two separate blinded rating forms for qualified bilingual reviewers have been prepared under the Git-ignored `data/pilot/vi-en-ai-v4.33/human-review/`. They contain only the same 48 validation cases, not release-test rows; the rating fields are blank. This is a handoff artifact, not completed human evaluation.

### 2026-10-09 v4.8 artifact and resume-identity recheck

The previously transferred v4.8 corpus/protocol/approval files and eight recorded `latest.pt` checkpoints are present locally, and all 15 hashes recorded in `VI_EN_RESULTS_V4.8_STATUS.md` match. No trainer process is running. The stored v4.8 protocol runtime is Python 3.11.9 on Windows; lattice is Python 3.11.17 on Arch Linux. Since `tide_jepa.experiment` includes Python and PyTorch versions in `run_identity` and rejects protocol runtime drift, the old v4.8 workers were not resumed and no guard was bypassed. v4.8 remains paused at 4/12 completed and 4/12 partial; validation was not run and its release holdout remains sealed. This supersedes the earlier handoff observation that those local artifact directories were absent; the historical entry is retained.


### 2026-10-09 bounded concurrent demo check

The existing loopback demo was verified from its process command line and `/health` provenance before testing. Two runs of 80 exact approved page-default requests from four concurrent clients each yielded one successful inference and 79 schema-valid HTTP 503 busy refusals, matching the regression-tested one-inference policy in `tide_jepa/demo.py`. RSS rose 1,656 KiB on the initial pass and 112 KiB on the repeated pass. Aggregate-only reports: [run 1](../../audits/2026-10-09/v433_demo_concurrent_bound.json), [run 2](../../audits/2026-10-09/v433_demo_concurrent_bound_repeat.json). This confirms bounded overload handling and memory behavior for concurrent clients. In a separate varied-input run, 40 requests per pass cycled through 64 exact train-only candidates balanced across English/Vietnamese and single-action/two-action paths; both passes returned 40/40 HTTP 200 and passed the narrow action/preservation checker in all four language/task cells (10/10 each); RSS was unchanged on the first pass and rose 4 KiB on the repeat ([run 1](../../audits/2026-10-09/v433_demo_varied_quality_benchmark_1.json), [run 2](../../audits/2026-10-09/v433_demo_varied_quality_benchmark_2.json)). These are synthetic train-only requests; semantic OOD, natural-corpus behavior, and production capacity remain unverified.
