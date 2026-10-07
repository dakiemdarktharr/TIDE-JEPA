# vi-en-ai-v4.29 post-hoc semantic rescore

This is a post-hoc component diagnostic of saved validation generations with the current semantic checker. It is **not frozen-protocol gate evidence** and does not authorize opening the release holdout.

Results remain preliminary AI-authored synthetic evidence; `human_validated=false`, `phomt_used=false`. Coverage and role-preservation denominators are shown below; unscored values are n/a. Decoder variants are reported separately.

Frozen training protocol SHA-256: `d4d33cedbbec2fe53147653c4a729e12175408cff9d7fc05828fc4b4a13a02d8`.

| Condition | Language | Task | Examples | Checker coverage | Action fidelity | Agent | Patient | Predicate | Place | All preserved |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| tide, self-feeding 0, copy 0, aux 1, language-balance 0, vocabulary | en | held_out_path | 480 | 480/480 (100.0%) | 480/480 (100.0%) | 100.0% | 95.4% | 98.8% | 100.0% | 452/480 (94.2%) |
| tide, self-feeding 0, copy 0, aux 1, language-balance 0, vocabulary | en | single | 3840 | 3840/3840 (100.0%) | 3606/3840 (93.9%) | 100.0% | 93.3% | 88.8% | 99.9% | 3196/3840 (83.2%) |
| tide, self-feeding 0, copy 0, aux 1, language-balance 0, vocabulary | vi | held_out_path | 480 | 480/480 (100.0%) | 480/480 (100.0%) | 100.0% | 99.8% | 100.0% | 100.0% | 479/480 (99.8%) |
| tide, self-feeding 0, copy 0, aux 1, language-balance 0, vocabulary | vi | single | 3840 | 3840/3840 (100.0%) | 3824/3840 (99.6%) | 100.0% | 99.3% | 99.6% | 100.0% | 3798/3840 (98.9%) |
| tide, self-feeding 0, copy 0, aux 1, language-balance 1, vocabulary | en | held_out_path | 480 | 480/480 (100.0%) | 478/480 (99.6%) | 100.0% | 94.8% | 98.3% | 99.8% | 446/480 (92.9%) |
| tide, self-feeding 0, copy 0, aux 1, language-balance 1, vocabulary | en | single | 3840 | 3840/3840 (100.0%) | 3500/3840 (91.1%) | 100.0% | 90.0% | 85.1% | 99.5% | 2932/3840 (76.4%) |
| tide, self-feeding 0, copy 0, aux 1, language-balance 1, vocabulary | vi | held_out_path | 480 | 480/480 (100.0%) | 476/480 (99.2%) | 100.0% | 96.9% | 97.5% | 98.3% | 449/480 (93.5%) |
| tide, self-feeding 0, copy 0, aux 1, language-balance 1, vocabulary | vi | single | 3840 | 3840/3840 (100.0%) | 3735/3840 (97.3%) | 99.9% | 93.3% | 93.9% | 98.0% | 3375/3840 (87.9%) |

This component diagnostic does not change the frozen gate or its thresholds. Any follow-up quality experiment must use a fresh reviewed version; the release holdout remains sealed unless the original frozen validation gates pass.

To reproduce without printing examples: `.venv/bin/python -B scripts/diagnose_validation_preservation.py data/pilot/vi-en-ai-v4.29 --markdown YOUR_DIAGNOSTIC.md`.

The script reads private validation generations but emits only aggregate counts; all private rows and generations remain Git-ignored under `data/` and `runs/`.
