# TIDE-JEPA experiments

> Status (2026-10-05): The v4.18 frozen evaluator omitted its event family, leaving zero semantic-checker coverage (`0/0` denominators); the gate failed closed and its report is invalid for semantic interpretation. The holdout remains sealed. A post-hoc corrected-checker rescore is diagnostic only and remains below thresholds. A one-group train-only overfit diagnostic reached 8/8 on the same seen single-action requests; this shows memorization, not generalization. A paired 20-input best/latest checkpoint sample found zero preservation and reference matches, but is too small and clustered to estimate full validation performance. See [v4.18 status](../../../VI_EN_RESULTS_V4.18_STATUS.md), [frozen report](../../../VI_EN_RESULTS_V4.18_VALIDATION.md), [rescore](../../../VI_EN_RESULTS_V4.18_RESCORING.md), [overfit diagnostic](../../../VI_EN_RESULTS_V4.18_OVERFIT_DIAGNOSTIC.md), and [checkpoint sample](../../../VI_EN_RESULTS_V4.18_CHECKPOINT_SAMPLE.md). Aggregate-only, preliminary synthetic evidence; not human validated. v4.17-r2 also failed all 60 checks, with no consistent weighting benefit. See [v4.17 status](../../../VI_EN_RESULTS_V4.17_STATUS.md), [report](../../../VI_EN_RESULTS_V4.17_VALIDATION.md), [v4.16 status](../../../VI_EN_RESULTS_V4.16_STATUS.md), and [Linux audit](../../../audits/2026-10-03/LINUX_REVALIDATION.md).

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
