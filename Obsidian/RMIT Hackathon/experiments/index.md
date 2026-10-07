# TIDE-JEPA experiments

v4.29 failed its frozen validation gate. v4.30's six runs and validation completed, but its frozen checker accepts Vietnamese progressive-marker deletions; its metrics are limited historical evidence, not a confirmatory quality gate. Both release holdouts remain sealed. See [v4.30 status](../../../VI_EN_RESULTS_V4.30_STATUS.md) and [research acceleration](../../../RESEARCH_ACCELERATION.md).

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

> Current status (2026-10-07): v4.29 completed all six frozen runs and validation-only generation; identities and checker coverage passed. The quality gate failed: 1/6 full-config gates and 37/60 seed-by-bucket checks passed. English single-action preservation remains weak. v4.27 and v4.28 remain retired after holdout exposure during review. The v4.29 release holdout remains sealed. See [v4.29 status](../../../VI_EN_RESULTS_V4.29_STATUS.md) and [aggregate validation](../../../VI_EN_RESULTS_V4.29_VALIDATION.md) above. Older failed/invalid runs and their holdouts remain historical. All evidence is preliminary synthetic AI review, not human validation.

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
