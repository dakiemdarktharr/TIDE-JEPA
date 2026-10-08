# TIDE-JEPA experiments

v4.33 completed six frozen runs. Corrected validation and release-test gates pass for all three TIDE seeds, while token-only controls are similar. The old stock-page example was out of corpus and produced semantic corruption; the current runner uses an exact train source/action allowlist and its default passes the narrow checker. Two independent Luna reviewers judged 47/48 sampled validation outputs naturalness-acceptable and 48/48 meaning/action-faithful; one spelling issue remains, and this is preliminary AI review only. A 19-case allowlist/request-boundary smoke, repeated five-minute 3,219-request soak, two bounded 240-request runtime/RSS runs, burst/incomplete-body behavior, and delayed stale-response browser check passed. These checks do not establish semantic OOD detection. Two varied train-only benchmark passes each passed the narrow checker in all four language/task cells (10/10 each); four-client overload checks returned schema-valid 503 refusals under the one-inference limit. Natural/arbitrary payload quality, production capacity, and broad semantic OOD remain open; the demo stays diagnostic-only. See [v4.33 status](../../../VI_EN_RESULTS_V4.33_STATUS.md), [release aggregates](../../../audits/2026-10-08/v433_release_holdout_aggregate.json), [demo smoke](../../../audits/2026-10-08/v433_demo_smoke.json), [boundary smoke](../../../audits/2026-10-08/v433_demo_boundary_smoke.json), [AI linguistic review](../../../audits/2026-10-08/v433_validation_ai_linguistic_review.json), [runtime benchmark 1](../../../audits/2026-10-08/v433_demo_runtime_benchmark_3.json), [runtime benchmark 2](../../../audits/2026-10-08/v433_demo_runtime_benchmark_4.json), [varied benchmark 1](../../../audits/2026-10-09/v433_demo_varied_quality_benchmark_1.json), [varied benchmark 2](../../../audits/2026-10-09/v433_demo_varied_quality_benchmark_2.json), [concurrency benchmark 1](../../../audits/2026-10-09/v433_demo_concurrent_bound.json), [concurrency benchmark 2](../../../audits/2026-10-09/v433_demo_concurrent_bound_repeat.json), and [research acceleration](../../../RESEARCH_ACCELERATION.md).

- [v4.33 status](../../../VI_EN_RESULTS_V4.33_STATUS.md) — corrected validation and release test pass; diagnostic-only demo boundary.
- [v4.33 validation checker reassessment](../../../audits/2026-10-08/v433_validation_checker_reassessment.json) — aggregate-only cached-generation rescore.
- [v4.33 release aggregates](../../../audits/2026-10-08/v433_release_holdout_aggregate.json) — all six frozen configs, bucket metrics and hashes.
- [v4.33 demo smoke](../../../audits/2026-10-08/v433_demo_smoke.json) — loopback behavior, provenance and qualitative limitation.
- [v4.33 preliminary AI linguistic review](../../../audits/2026-10-08/v433_validation_ai_linguistic_review.json) — aggregate-only, stratified validation sample; not human validation.
- [Linux lock bootstrap](../../../audits/2026-10-08/linux-lock-bootstrap.json) — pinned CPython 3.11 CPU environment from a source-only snapshot.

- [v4.32 status](../../../VI_EN_RESULTS_V4.32_STATUS.md) — six runs complete, frozen validation gate failed, release holdout sealed.
- [v4.32 validation](../../../audits/2026-10-08/VI_EN_V4.32_VALIDATION.md) — aggregate-only validation, per-bucket thresholds and gate results.
- [v4.32 train checkpoint diagnostic](../../../audits/2026-10-08/V432_TRAIN_DIAGNOSTIC.md) — train-only TF/greedy, semantic and conditioning probes.
- [v4.32 train-group overfit sanity check](../../../audits/2026-10-08/V432_TRAIN_GROUP_OVERFIT.md) — small-sample memorization capacity, not generalization evidence.
- [v4.32 action-sensitivity diagnostic](../../../audits/2026-10-08/V432_ACTION_SENSITIVITY.md) — output-change diagnostic, not semantic correctness evidence.
- [v4.32 preservation diagnostic](../../../audits/2026-10-08/V432_PRESERVATION_DIAGNOSTIC.md) — post-hoc checker-component rescore, not frozen-gate evidence.

Earlier runs and incident records remain below.

- [v4.30 status](../../../VI_EN_RESULTS_V4.30_STATUS.md) — six runs complete; frozen report recorded 1/6 configurations and 29/60 bucket checks passing, with a later checker negative-control defect limiting interpretation.
- [v4.30 validation](../../../VI_EN_RESULTS_V4.30_VALIDATION.md) — aggregate-only original frozen results; do not treat the gate as confirmatory.
- [v4.30 component diagnostic](../../../VI_EN_RESULTS_V4.30_DIAGNOSTIC.md) — post-hoc checker and role rescore, not frozen-gate evidence.
- [v4.30 action-sensitivity diagnostic](../../../VI_EN_RESULTS_V4.30_ACTION_SENSITIVITY.md) — paired-output change diagnostic, not correctness evidence.

- [v4.29 status](../../../VI_EN_RESULTS_V4.29_STATUS.md) — six runs and validation complete; 1/6 full-config gates and 37/60 seed-by-bucket checks passed; release holdout sealed.
- [v4.29 validation](../../../VI_EN_RESULTS_V4.29_VALIDATION.md) — aggregate-only generation metrics, thresholds, and per-seed failure reasons.
- [v4.29 component diagnostic](../../../VI_EN_RESULTS_V4.29_DIAGNOSTIC.md) — post-hoc role preservation by language and language-balance condition.
- [v4.29 action-sensitivity diagnostic](../../../VI_EN_RESULTS_V4.29_ACTION_SENSITIVITY.md) — different requested actions changed every paired output; not correctness evidence.
- [v4.28 disposition](../../../VI_EN_RESULTS_V4.28_STATUS.md) — retired before freeze/training after holdout semantic-frame annotations were accessed during review.
- [v4.27 disposition](../../../VI_EN_RESULTS_V4.27_STATUS.md) — retired before training after review exposed test-split content.

- [v4.26 status](../../../VI_EN_RESULTS_V4.26_STATUS.md) — six runs and validation complete; 1/6 full-config gates and 32/60 seed-by-bucket checks passed; release holdout sealed.
- [v4.26 validation](../../../VI_EN_RESULTS_V4.26_VALIDATION.md) — aggregate-only free-generation results and frozen gates, with teacher-forced losses reported separately.
- [v4.26 component diagnostic](../../../VI_EN_RESULTS_V4.26_DIAGNOSTIC.md) — post-hoc agent/patient/predicate/place retention by language and source-copy condition.
- [v4.26 action-sensitivity diagnostic](../../../VI_EN_RESULTS_V4.26_ACTION_SENSITIVITY.md) — same-source/different-action validation outputs, aggregate only.
- [v4.25 status](../../../VI_EN_RESULTS_V4.25_STATUS.md) — six runs and validation complete; 3/6 full-config gates and 44/60 seed-by-bucket checks passed; release holdout sealed.
- [v4.25 validation](../../../VI_EN_RESULTS_V4.25_VALIDATION.md) — aggregate-only free-generation results and frozen gates, with teacher-forced losses reported separately.
- [v4.25 component diagnostic](../../../VI_EN_RESULTS_V4.25_DIAGNOSTIC.md) — post-hoc role retention, separated by self-feeding condition.
- [v4.25 action-sensitivity diagnostic](../../../VI_EN_RESULTS_V4.25_ACTION_SENSITIVITY.md) — same-source/different-action validation outputs, aggregate only.
- [v4.24 status](../../../VI_EN_RESULTS_V4.24_STATUS.md) — historical six-run failure; duplicate training-log rows preserved.
- [v4.24 validation](../../../VI_EN_RESULTS_V4.24_VALIDATION.md) — aggregate-only metrics and per-bucket gate results.
- [v4.24 component diagnostic](../../../VI_EN_RESULTS_V4.24_DIAGNOSTIC.md) — post-hoc agent/patient/predicate/place retention.
- [v4.24 action-sensitivity diagnostic](../../../VI_EN_RESULTS_V4.24_ACTION_SENSITIVITY.md) — same-source/different-action validation outputs, aggregate only.
- [v4.23 status](../../../VI_EN_RESULTS_V4.23_STATUS.md) — historical 12-run validation failure; holdout remains sealed.

> Current status (2026-10-08): v4.33 completed six frozen runs; all three TIDE seeds passed corrected validation and release-test gates under the unchanged narrow synthetic contract. The checker registration defect and original failure report are preserved. Token-only was similar; no TIDE advantage is established. The stock UI default was out of corpus; the amended runner uses an exact train source/action allowlist and a train-only example that passes the narrow checker. A bounded 20-request/timeout smoke and delayed stale-response browser path passed; long soak, semantic OOD, and human review remain open, so the demo is diagnostic-only. v4.27/v4.28 remain retired after holdout exposure. See [v4.33 status](../../../VI_EN_RESULTS_V4.33_STATUS.md), [release aggregate](../../../audits/2026-10-08/v433_release_holdout_aggregate.json), and [demo smoke](../../../audits/2026-10-08/v433_demo_smoke.json). This is preliminary synthetic AI review, not human validation.

## Completed preliminary pilot

[Workflow](../../../VI_EN_PILOT.md) and [aggregate results](../../../VI_EN_RESULTS.md) document the user-authorized AI pilot. Twelve fixed runs produced 0/864 exact matches and 564/864 valid UTF-8 outputs; the engineering path works but linguistic quality remains poor. Private corpus/reviews/protocol/results are under `data/pilot/vi-en-ai-v3/`; checkpoints and private generations are under `runs/vi-en-ai-v3/`. Both are Git-ignored. Source: [[../raw/PhoMT Intake and Vi-En Pilot — 2026-10-01]].

Use this folder for versioned experiment protocols, run manifests, analysis, and results. Keep source data outside this vault unless its source-specific rights, consent/governance, and task-fit gates are approved. Never treat discovery of a dataset as permission to use it.

## Before an experiment

- Read [[../wiki/Project Ground Truth]] and the active `tide_jepa_spec.md` at the project root before planning a run.
- Define hypotheses, baselines, matched data/compute budgets, splits, seeds, metrics, and human-review procedure before running.
- For Phan Rang Cham, get appropriate speaker/community and linguistic validation for variety, modality, orthography/transcription, actions, permissions, and acceptable outputs. Do not infer these from Vietnamese–English labels.
- Record the exact code revision/change-set, configuration, environment, data provenance/rights decision, commands, output, and limitations for every run.

## Current evidence boundary

The first implementation milestone has only synthetic integer software tests; those are not language experiments. See [[../wiki/First Implementation Milestone]]. Dataset candidates and unresolved terms are in [[../wiki/Dataset Research — 2026-09-28]].
