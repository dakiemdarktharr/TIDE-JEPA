# 2026-10-02 audit repair closure

Status: active engineering closure record. Findings are traced to regression coverage and probe evidence; this does not assert that untested bugs cannot exist. The current project-local runtime on Windows is Python 3.11.9 with PyTorch 2.14.0+cpu; after v4.8 implementation changes, 69 unit tests passed with 0 skipped, plus compile and dependency checks. A v4.8 CPU training run was stopped at the user's request before all configurations completed. See [the aggregate-only v4.8 status](../../VI_EN_RESULTS_V4.8_STATUS.md). No v4.8 validation result exists; Q01 remains open and blocks goal completion.

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
| E14 | Demo request snapshot, disabled form controls, and explicit status/error presentation are covered by UI implementation; full interactive browser automation remains unverified in the current desktop task. | Partially closed; browser behavior requires a fresh UI integration check |
| Q01 | v3 and v4.1–v4.7 quality failures are preserved. v4.8 has a fresh AI-reviewed compositional synthetic split and untouched release holdout, but training stopped after four complete and four partial runs; validation has not run. The required semantic thresholds are not demonstrated. | Open; blocks goal completion |
| G01 | Python 3.11.9 / PyTorch 2.14.0+cpu, compileall, unit suite, and pip consistency were checked; clean-machine bootstrap and venv launcher reliability remain out of scope. | Partially closed |
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
