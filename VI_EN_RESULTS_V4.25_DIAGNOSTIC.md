# vi-en-ai-v4.25 post-hoc semantic rescore

This is a post-hoc component diagnostic of saved validation generations with the current semantic checker. It is **not frozen-protocol gate evidence** and does not authorize opening the release holdout.

Results remain preliminary AI-authored synthetic evidence; `human_validated=false`, `phomt_used=false`. Coverage and role-preservation denominators are shown below; unscored values are n/a. Decoder variants are reported separately.

Frozen training protocol SHA-256: `6604805a86221a4958da9ea38ac0e845da99a3524f5cb802bfbb243e65c243b6`.

| Condition | Language | Task | Examples | Checker coverage | Action fidelity | Agent | Patient | Predicate | Place | All preserved |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| tide, self-feeding 0.2, copy 0, aux 1, vocabulary | en | held_out_path | 480 | 480/480 (100.0%) | 480/480 (100.0%) | 100.0% | 91.7% | 100.0% | 100.0% | 440/480 (91.7%) |
| tide, self-feeding 0.2, copy 0, aux 1, vocabulary | en | single | 3840 | 3840/3840 (100.0%) | 3791/3840 (98.7%) | 100.0% | 86.2% | 97.7% | 99.7% | 3249/3840 (84.6%) |
| tide, self-feeding 0.2, copy 0, aux 1, vocabulary | vi | held_out_path | 480 | 480/480 (100.0%) | 472/480 (98.3%) | 100.0% | 96.2% | 99.6% | 99.8% | 459/480 (95.6%) |
| tide, self-feeding 0.2, copy 0, aux 1, vocabulary | vi | single | 3840 | 3840/3840 (100.0%) | 3744/3840 (97.5%) | 99.7% | 94.3% | 96.1% | 99.7% | 3494/3840 (91.0%) |
| tide, self-feeding 0, copy 0, aux 1, vocabulary | en | held_out_path | 480 | 480/480 (100.0%) | 480/480 (100.0%) | 100.0% | 93.3% | 100.0% | 100.0% | 448/480 (93.3%) |
| tide, self-feeding 0, copy 0, aux 1, vocabulary | en | single | 3840 | 3840/3840 (100.0%) | 3827/3840 (99.7%) | 100.0% | 90.0% | 99.4% | 99.6% | 3432/3840 (89.4%) |
| tide, self-feeding 0, copy 0, aux 1, vocabulary | vi | held_out_path | 480 | 480/480 (100.0%) | 480/480 (100.0%) | 100.0% | 98.3% | 100.0% | 100.0% | 472/480 (98.3%) |
| tide, self-feeding 0, copy 0, aux 1, vocabulary | vi | single | 3840 | 3840/3840 (100.0%) | 3817/3840 (99.4%) | 100.0% | 97.8% | 99.2% | 99.9% | 3723/3840 (97.0%) |

This component diagnostic does not change the frozen gate or its thresholds. Any follow-up quality experiment must use a fresh reviewed version; the release holdout remains sealed unless the original frozen validation gates pass.

To reproduce without printing examples: `.venv/bin/python -B scripts/diagnose_validation_preservation.py data/pilot/vi-en-ai-v4.25 --markdown YOUR_DIAGNOSTIC.md`.

The script reads private validation generations but emits only aggregate counts; all private rows and generations remain Git-ignored under `data/` and `runs/`.
