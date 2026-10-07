# vi-en-ai-v4.24 post-hoc semantic rescore

This is a post-hoc component diagnostic of saved validation generations with the current semantic checker. It is **not frozen-protocol gate evidence** and does not authorize opening the release holdout.

Results remain preliminary AI-authored synthetic evidence; `human_validated=false`, `phomt_used=false`. Coverage and role-preservation denominators are shown below; unscored values are n/a. Decoder variants are reported separately.

Frozen training protocol SHA-256: `9939b50d2cdb9bd8099724baa4a6a2f2f875e003b3484efc3dfadb60d7df346f`.

| Condition | Language | Task | Examples | Checker coverage | Action fidelity | Agent | Patient | Predicate | Place | All preserved |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| tide, copy 0, aux 1, vocabulary | en | held_out_path | 480 | 480/480 (100.0%) | 479/480 (99.8%) | 100.0% | 92.7% | 98.3% | 100.0% | 439/480 (91.5%) |
| tide, copy 0, aux 1, vocabulary | en | single | 3840 | 3840/3840 (100.0%) | 3809/3840 (99.2%) | 99.9% | 86.1% | 92.8% | 99.5% | 3082/3840 (80.3%) |
| tide, copy 0, aux 1, vocabulary | vi | held_out_path | 480 | 480/480 (100.0%) | 477/480 (99.4%) | 100.0% | 98.5% | 98.1% | 99.6% | 466/480 (97.1%) |
| tide, copy 0, aux 1, vocabulary | vi | single | 3840 | 3840/3840 (100.0%) | 3743/3840 (97.5%) | 99.8% | 96.0% | 94.6% | 99.6% | 3507/3840 (91.3%) |
| tide, copy 1.5, aux 1, vocabulary | en | held_out_path | 480 | 480/480 (100.0%) | 476/480 (99.2%) | 100.0% | 93.3% | 95.8% | 99.6% | 429/480 (89.4%) |
| tide, copy 1.5, aux 1, vocabulary | en | single | 3840 | 3840/3840 (100.0%) | 3764/3840 (98.0%) | 100.0% | 88.8% | 89.7% | 98.8% | 3059/3840 (79.7%) |
| tide, copy 1.5, aux 1, vocabulary | vi | held_out_path | 480 | 480/480 (100.0%) | 447/480 (93.1%) | 100.0% | 96.5% | 92.7% | 99.2% | 428/480 (89.2%) |
| tide, copy 1.5, aux 1, vocabulary | vi | single | 3840 | 3840/3840 (100.0%) | 3297/3840 (85.9%) | 99.1% | 92.0% | 86.7% | 98.8% | 3035/3840 (79.0%) |

This component diagnostic does not change the frozen gate or its thresholds. Any follow-up quality experiment must use a fresh reviewed version; the release holdout remains sealed unless the original frozen validation gates pass.

To reproduce without printing examples: `.venv/bin/python -B scripts/diagnose_validation_preservation.py data/pilot/vi-en-ai-v4.24 --markdown YOUR_DIAGNOSTIC.md`.

The script reads private validation generations but emits only aggregate counts; all private rows and generations remain Git-ignored under `data/` and `runs/`.
