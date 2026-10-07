# vi-en-ai-v4.26 post-hoc semantic rescore

This is a post-hoc component diagnostic of saved validation generations with the current semantic checker. It is **not frozen-protocol gate evidence** and does not authorize opening the release holdout.

Results remain preliminary AI-authored synthetic evidence; `human_validated=false`, `phomt_used=false`. Coverage and role-preservation denominators are shown below; unscored values are n/a. Decoder variants are reported separately.

Frozen training protocol SHA-256: `b8d2c78cc0de9f833d05eb2ea200f82b0b614839390695ad3fe281d6a7105dd2`.

| Condition | Language | Task | Examples | Checker coverage | Action fidelity | Agent | Patient | Predicate | Place | All preserved |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| tide, self-feeding 0, copy 0.25, aux 1, vocabulary | en | held_out_path | 480 | 480/480 (100.0%) | 476/480 (99.2%) | 100.0% | 87.1% | 96.7% | 99.0% | 400/480 (83.3%) |
| tide, self-feeding 0, copy 0.25, aux 1, vocabulary | en | single | 3840 | 3840/3840 (100.0%) | 3688/3840 (96.0%) | 100.0% | 79.1% | 87.6% | 97.0% | 2641/3840 (68.8%) |
| tide, self-feeding 0, copy 0.25, aux 1, vocabulary | vi | held_out_path | 480 | 480/480 (100.0%) | 480/480 (100.0%) | 100.0% | 98.1% | 99.4% | 99.2% | 464/480 (96.7%) |
| tide, self-feeding 0, copy 0.25, aux 1, vocabulary | vi | single | 3840 | 3840/3840 (100.0%) | 3741/3840 (97.4%) | 100.0% | 97.2% | 96.6% | 99.7% | 3599/3840 (93.7%) |
| tide, self-feeding 0, copy 0, aux 1, vocabulary | en | held_out_path | 480 | 480/480 (100.0%) | 468/480 (97.5%) | 100.0% | 89.0% | 98.8% | 99.6% | 421/480 (87.7%) |
| tide, self-feeding 0, copy 0, aux 1, vocabulary | en | single | 3840 | 3840/3840 (100.0%) | 3749/3840 (97.6%) | 100.0% | 85.3% | 93.6% | 98.8% | 3053/3840 (79.5%) |
| tide, self-feeding 0, copy 0, aux 1, vocabulary | vi | held_out_path | 480 | 480/480 (100.0%) | 472/480 (98.3%) | 100.0% | 97.3% | 98.5% | 99.4% | 459/480 (95.6%) |
| tide, self-feeding 0, copy 0, aux 1, vocabulary | vi | single | 3840 | 3840/3840 (100.0%) | 3697/3840 (96.3%) | 99.9% | 94.3% | 94.6% | 99.2% | 3428/3840 (89.3%) |

This component diagnostic does not change the frozen gate or its thresholds. Any follow-up quality experiment must use a fresh reviewed version; the release holdout remains sealed unless the original frozen validation gates pass.

To reproduce without printing examples: `.venv/bin/python -B scripts/diagnose_validation_preservation.py data/pilot/vi-en-ai-v4.26 --markdown YOUR_DIAGNOSTIC.md`.

The script reads private validation generations but emits only aggregate counts; all private rows and generations remain Git-ignored under `data/` and `runs/`.
