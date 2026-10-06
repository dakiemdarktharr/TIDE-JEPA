# vi-en-ai-v4.20 post-hoc semantic rescore

This is a post-hoc component diagnostic of saved validation generations with the current semantic checker. It is **not frozen-protocol gate evidence** and does not authorize opening the release holdout.

Results remain preliminary AI-authored synthetic evidence; `human_validated=false`, `phomt_used=false`. Coverage and role-preservation denominators are shown below; unscored values are n/a. Decoder variants are reported separately.

Frozen training protocol SHA-256: `d2e911cb4d6e16627d7630a7d113530dcd73ae65a7806dc4bb68b70315400f23`.

| Condition | Language | Task | Examples | Checker coverage | Action fidelity | Agent | Patient | Predicate | Place | All preserved |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| tide, copy 0, aux 0, source_pointer | en | held_out_path | 480 | 480/480 (100.0%) | 317/480 (66.0%) | 88.3% | 15.2% | 22.1% | 63.3% | 12/480 (2.5%) |
| tide, copy 0, aux 0, source_pointer | en | single | 3840 | 3840/3840 (100.0%) | 1287/3840 (33.5%) | 69.2% | 8.3% | 2.5% | 54.5% | 14/3840 (0.4%) |
| tide, copy 0, aux 0, source_pointer | vi | held_out_path | 480 | 480/480 (100.0%) | 175/480 (36.5%) | 65.8% | 9.8% | 7.7% | 71.7% | 1/480 (0.2%) |
| tide, copy 0, aux 0, source_pointer | vi | single | 3840 | 3840/3840 (100.0%) | 1030/3840 (26.8%) | 63.1% | 6.2% | 6.3% | 69.9% | 12/3840 (0.3%) |
| tide, copy 0, aux 0, vocabulary | en | held_out_path | 480 | 480/480 (100.0%) | 354/480 (73.8%) | 85.0% | 17.3% | 14.0% | 82.9% | 13/480 (2.7%) |
| tide, copy 0, aux 0, vocabulary | en | single | 3840 | 3840/3840 (100.0%) | 1792/3840 (46.7%) | 75.1% | 11.2% | 2.6% | 72.5% | 13/3840 (0.3%) |
| tide, copy 0, aux 0, vocabulary | vi | held_out_path | 480 | 480/480 (100.0%) | 316/480 (65.8%) | 74.6% | 19.0% | 12.3% | 81.0% | 8/480 (1.7%) |
| tide, copy 0, aux 0, vocabulary | vi | single | 3840 | 3840/3840 (100.0%) | 1220/3840 (31.8%) | 65.8% | 11.5% | 8.2% | 82.9% | 15/3840 (0.4%) |

This component diagnostic does not change the frozen gate or its thresholds. Any follow-up quality experiment must use a fresh reviewed version; the release holdout remains sealed unless the original frozen validation gates pass.

To reproduce without printing examples: `.venv/bin/python -B scripts/diagnose_validation_preservation.py data/pilot/vi-en-ai-v4.20 --markdown YOUR_DIAGNOSTIC.md`.

The script reads private validation generations but emits only aggregate counts; all private rows and generations remain Git-ignored under `data/` and `runs/`.
