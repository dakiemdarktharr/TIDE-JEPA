# vi-en-ai-v4.31 post-hoc semantic rescore

This is a post-hoc component diagnostic of saved validation generations with the current semantic checker. It is **not frozen-protocol gate evidence** and does not authorize opening the release holdout.

Results remain preliminary AI-authored synthetic evidence; `human_validated=false`, `phomt_used=false`. Coverage and role-preservation denominators are shown below; unscored values are n/a. Decoder variants are reported separately.

Frozen training protocol SHA-256: `a34113c4f74b804d50120c7472a9dbf1f10c5329542293c5f43eb6b14f1215e5`.

| Condition | Language | Task | Examples | Checker coverage | Action fidelity | Agent | Patient | Predicate | Place | All preserved |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| tide, self-feeding 0, copy 0, aux 1, language-balance 0, vocabulary | en | held_out_path | 480 | 480/480 (100.0%) | 476/480 (99.2%) | 100.0% | 79.4% | 98.5% | 100.0% | 378/480 (78.8%) |
| tide, self-feeding 0, copy 0, aux 1, language-balance 0, vocabulary | en | single | 3840 | 3840/3840 (100.0%) | 3713/3840 (96.7%) | 99.9% | 78.1% | 88.5% | 99.8% | 2684/3840 (69.9%) |
| tide, self-feeding 0, copy 0, aux 1, language-balance 0, vocabulary | vi | held_out_path | 480 | 480/480 (100.0%) | 480/480 (100.0%) | 100.0% | 94.8% | 96.0% | 100.0% | 441/480 (91.9%) |
| tide, self-feeding 0, copy 0, aux 1, language-balance 0, vocabulary | vi | single | 3840 | 3840/3840 (100.0%) | 3715/3840 (96.7%) | 100.0% | 95.1% | 94.0% | 99.8% | 3449/3840 (89.8%) |

This component diagnostic does not change the frozen gate or its thresholds. Any follow-up quality experiment must use a fresh reviewed version; the release holdout remains sealed unless the original frozen validation gates pass.

To reproduce without printing examples: `.venv/bin/python -B scripts/diagnose_validation_preservation.py data/pilot/vi-en-ai-v4.31 --markdown YOUR_DIAGNOSTIC.md`.

The script reads private validation generations but emits only aggregate counts; all private rows and generations remain Git-ignored under `data/` and `runs/`.
