# vi-en-ai-v4.30 post-hoc semantic rescore

This is a post-hoc component diagnostic of saved validation generations with the current semantic checker. It is **not frozen-protocol gate evidence** and does not authorize opening the release holdout.

Results remain preliminary AI-authored synthetic evidence; `human_validated=false`, `phomt_used=false`. Coverage and role-preservation denominators are shown below; unscored values are n/a. Decoder variants are reported separately.

Frozen training protocol SHA-256: `748119b1291ada27dec2731a2e53e7a0c9e8d16d804f0c113c408fdbdbf9dc77`.

| Condition | Language | Task | Examples | Checker coverage | Action fidelity | Agent | Patient | Predicate | Place | All preserved |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| tide, self-feeding 0, copy 0, aux 1, language-balance 0, source_pointer | en | held_out_path | 480 | 480/480 (100.0%) | 479/480 (99.8%) | 100.0% | 87.7% | 99.4% | 99.0% | 418/480 (87.1%) |
| tide, self-feeding 0, copy 0, aux 1, language-balance 0, source_pointer | en | single | 3840 | 3840/3840 (100.0%) | 3494/3840 (91.0%) | 99.9% | 84.1% | 86.0% | 97.5% | 2816/3840 (73.3%) |
| tide, self-feeding 0, copy 0, aux 1, language-balance 0, source_pointer | vi | held_out_path | 480 | 480/480 (100.0%) | 465/480 (96.9%) | 100.0% | 92.1% | 99.6% | 96.7% | 433/480 (90.2%) |
| tide, self-feeding 0, copy 0, aux 1, language-balance 0, source_pointer | vi | single | 3840 | 3840/3840 (100.0%) | 3629/3840 (94.5%) | 99.9% | 85.7% | 97.2% | 95.2% | 3137/3840 (81.7%) |
| tide, self-feeding 0, copy 0, aux 1, language-balance 0, vocabulary | en | held_out_path | 480 | 480/480 (100.0%) | 477/480 (99.4%) | 100.0% | 85.4% | 99.0% | 100.0% | 408/480 (85.0%) |
| tide, self-feeding 0, copy 0, aux 1, language-balance 0, vocabulary | en | single | 3840 | 3840/3840 (100.0%) | 3760/3840 (97.9%) | 99.9% | 83.0% | 90.0% | 99.0% | 2914/3840 (75.9%) |
| tide, self-feeding 0, copy 0, aux 1, language-balance 0, vocabulary | vi | held_out_path | 480 | 480/480 (100.0%) | 461/480 (96.0%) | 100.0% | 99.4% | 95.4% | 100.0% | 456/480 (95.0%) |
| tide, self-feeding 0, copy 0, aux 1, language-balance 0, vocabulary | vi | single | 3840 | 3840/3840 (100.0%) | 3699/3840 (96.3%) | 99.9% | 98.4% | 94.2% | 99.8% | 3563/3840 (92.8%) |

This component diagnostic does not change the frozen gate or its thresholds. Any follow-up quality experiment must use a fresh reviewed version; the release holdout remains sealed unless the original frozen validation gates pass.

To reproduce without printing examples: `.venv/bin/python -B scripts/diagnose_validation_preservation.py data/pilot/vi-en-ai-v4.30 --markdown YOUR_DIAGNOSTIC.md`.

The script reads private validation generations but emits only aggregate counts; all private rows and generations remain Git-ignored under `data/` and `runs/`.
