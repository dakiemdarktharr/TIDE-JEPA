# TIDE-JEPA experiments

> Status: AI-reviewed original synthetic Vi–En preliminary pilot completed; no PhoMT training or human-validated language result. Source: [[../raw/PhoMT Intake and Vi-En Pilot — 2026-10-01]].

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
