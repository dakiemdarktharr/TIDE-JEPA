# vi-en-ai-v4.32 post-hoc semantic rescore

This is a post-hoc component diagnostic of saved validation generations with the current semantic checker. It is **not frozen-protocol gate evidence** and does not authorize opening the release holdout.

Results remain preliminary AI-authored synthetic evidence; `human_validated=false`, `phomt_used=false`. Coverage and role-preservation denominators are shown below; unscored values are n/a. Decoder variants are reported separately.

Frozen training protocol SHA-256: `c288e9749402282ff27f2279e33ad13b58ee6c96612695ba41711bffcd5b0524`.

| Condition | Language | Task | Examples | Checker coverage | Action fidelity | Agent | Patient | Predicate | Place | All preserved |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| tide, self-feeding 0, copy 0, aux 1, language-balance 0, source_pointer | en | held_out_path | 480 | 480/480 (100.0%) | 471/480 (98.1%) | 99.4% | 84.4% | 98.3% | 98.5% | 390/480 (81.2%) |
| tide, self-feeding 0, copy 0, aux 1, language-balance 0, source_pointer | en | single | 3840 | 3840/3840 (100.0%) | 3283/3840 (85.5%) | 98.5% | 78.0% | 73.6% | 96.0% | 2244/3840 (58.4%) |
| tide, self-feeding 0, copy 0, aux 1, language-balance 0, source_pointer | vi | held_out_path | 480 | 480/480 (100.0%) | 479/480 (99.8%) | 100.0% | 99.0% | 99.0% | 99.8% | 471/480 (98.1%) |
| tide, self-feeding 0, copy 0, aux 1, language-balance 0, source_pointer | vi | single | 3840 | 3840/3840 (100.0%) | 3765/3840 (98.0%) | 100.0% | 95.9% | 96.8% | 99.5% | 3576/3840 (93.1%) |
| tide, self-feeding 0, copy 0, aux 1, language-balance 0, vocabulary | en | held_out_path | 480 | 480/480 (100.0%) | 471/480 (98.1%) | 99.8% | 77.9% | 94.2% | 100.0% | 351/480 (73.1%) |
| tide, self-feeding 0, copy 0, aux 1, language-balance 0, vocabulary | en | single | 3840 | 3840/3840 (100.0%) | 3379/3840 (88.0%) | 99.3% | 74.0% | 73.0% | 98.5% | 2119/3840 (55.2%) |
| tide, self-feeding 0, copy 0, aux 1, language-balance 0, vocabulary | vi | held_out_path | 480 | 480/480 (100.0%) | 478/480 (99.6%) | 100.0% | 99.6% | 99.8% | 99.8% | 476/480 (99.2%) |
| tide, self-feeding 0, copy 0, aux 1, language-balance 0, vocabulary | vi | single | 3840 | 3840/3840 (100.0%) | 3701/3840 (96.4%) | 99.9% | 97.4% | 95.0% | 99.3% | 3543/3840 (92.3%) |

This component diagnostic does not change the frozen gate or its thresholds. Any follow-up quality experiment must use a fresh reviewed version; the release holdout remains sealed unless the original frozen validation gates pass.

To reproduce without printing examples: `.venv/bin/python -B scripts/diagnose_validation_preservation.py data/pilot/vi-en-ai-v4.32 --markdown YOUR_DIAGNOSTIC.md`.

The script reads private validation generations but emits only aggregate counts; all private rows and generations remain Git-ignored under `data/` and `runs/`.
