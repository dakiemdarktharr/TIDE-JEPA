# vi-en-ai-v4.23 post-hoc semantic rescore

This is a post-hoc component diagnostic of saved validation generations with the current semantic checker. It is **not frozen-protocol gate evidence** and does not authorize opening the release holdout.

Results remain preliminary AI-authored synthetic evidence; `human_validated=false`, `phomt_used=false`. Coverage and role-preservation denominators are shown below; unscored values are n/a. Decoder variants are reported separately.

Frozen training protocol SHA-256: `0ad11b544e6884660484d0796b77de01f12335bb6afbc9344cd23a959c9fc14b`.

| Condition | Language | Task | Examples | Checker coverage | Action fidelity | Agent | Patient | Predicate | Place | All preserved |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| tide, copy 0, aux 1, source_pointer | en | held_out_path | 480 | 480/480 (100.0%) | 294/480 (61.3%) | 100.0% | 14.8% | 58.3% | 40.6% | 23/480 (4.8%) |
| tide, copy 0, aux 1, source_pointer | en | single | 3840 | 3840/3840 (100.0%) | 1367/3840 (35.6%) | 98.3% | 6.8% | 11.9% | 35.3% | 17/3840 (0.4%) |
| tide, copy 0, aux 1, source_pointer | vi | held_out_path | 480 | 480/480 (100.0%) | 417/480 (86.9%) | 100.0% | 51.9% | 86.9% | 93.3% | 222/480 (46.2%) |
| tide, copy 0, aux 1, source_pointer | vi | single | 3840 | 3840/3840 (100.0%) | 1733/3840 (45.1%) | 98.9% | 31.1% | 49.2% | 84.7% | 653/3840 (17.0%) |
| tide, copy 0, aux 1, vocabulary | en | held_out_path | 480 | 480/480 (100.0%) | 387/480 (80.6%) | 100.0% | 21.9% | 61.3% | 92.1% | 80/480 (16.7%) |
| tide, copy 0, aux 1, vocabulary | en | single | 3840 | 3840/3840 (100.0%) | 1626/3840 (42.3%) | 99.3% | 14.7% | 15.2% | 79.7% | 124/3840 (3.2%) |
| tide, copy 0, aux 1, vocabulary | vi | held_out_path | 480 | 480/480 (100.0%) | 396/480 (82.5%) | 99.0% | 35.6% | 51.5% | 93.5% | 99/480 (20.6%) |
| tide, copy 0, aux 1, vocabulary | vi | single | 3840 | 3840/3840 (100.0%) | 1313/3840 (34.2%) | 95.7% | 21.6% | 23.2% | 88.0% | 232/3840 (6.0%) |
| tide, copy 1.5, aux 1, source_pointer | en | held_out_path | 480 | 480/480 (100.0%) | 209/480 (43.5%) | 100.0% | 20.0% | 52.3% | 68.3% | 40/480 (8.3%) |
| tide, copy 1.5, aux 1, source_pointer | en | single | 3840 | 3840/3840 (100.0%) | 1290/3840 (33.6%) | 98.8% | 10.9% | 14.3% | 60.8% | 65/3840 (1.7%) |
| tide, copy 1.5, aux 1, source_pointer | vi | held_out_path | 480 | 480/480 (100.0%) | 344/480 (71.7%) | 99.8% | 63.5% | 90.0% | 91.0% | 269/480 (56.0%) |
| tide, copy 1.5, aux 1, source_pointer | vi | single | 3840 | 3840/3840 (100.0%) | 1448/3840 (37.7%) | 99.2% | 50.1% | 57.2% | 88.2% | 1156/3840 (30.1%) |
| tide, copy 1.5, aux 1, vocabulary | en | held_out_path | 480 | 480/480 (100.0%) | 381/480 (79.4%) | 99.4% | 23.1% | 56.9% | 85.2% | 72/480 (15.0%) |
| tide, copy 1.5, aux 1, vocabulary | en | single | 3840 | 3840/3840 (100.0%) | 1924/3840 (50.1%) | 99.0% | 15.9% | 19.8% | 80.5% | 176/3840 (4.6%) |
| tide, copy 1.5, aux 1, vocabulary | vi | held_out_path | 480 | 480/480 (100.0%) | 365/480 (76.0%) | 99.4% | 42.7% | 56.5% | 93.1% | 128/480 (26.7%) |
| tide, copy 1.5, aux 1, vocabulary | vi | single | 3840 | 3840/3840 (100.0%) | 1269/3840 (33.0%) | 98.6% | 32.2% | 27.7% | 91.7% | 414/3840 (10.8%) |

This component diagnostic does not change the frozen gate or its thresholds. Any follow-up quality experiment must use a fresh reviewed version; the release holdout remains sealed unless the original frozen validation gates pass.

## Teacher-forced fit and action sensitivity

The final-epoch training log shows a small mean single-edge token-CE gap between train and validation for each decoder/copy-weight condition, while path token CE is lower than single-edge CE. This suggests the failed free-generation scores are not explained by a large train/validation token-loss gap alone. These are teacher-forced aggregate losses; they do not prove sequence-level fit or semantic correctness.

| Decoder | Source-copy weight | Seeds | Train token CE | Validation token CE | Validation path token CE | Validation JEPA loss | Validation variance penalty |
|---|---:|---:|---:|---:|---:|---:|---:|
| source_pointer | 0 | 3 | 0.2152 | 0.2248 | 0.1115 | 0.0061 | 0.4293 |
| source_pointer | 1.5 | 3 | 0.1833 | 0.1893 | 0.1052 | 0.0073 | 0.6301 |
| vocabulary | 0 | 3 | 0.2034 | 0.2119 | 0.1071 | 0.0048 | 0.3975 |
| vocabulary | 1.5 | 3 | 0.1532 | 0.1636 | 0.1010 | 0.0056 | 0.6269 |

The nonzero variance penalty is consistent with under-dispersed latent features under the configured unit-spread target, especially with source-copy weight 1.5. It does not establish full representation collapse. In a separate exact post-hoc comparison of saved validation generations, changing the requested action for the same source changed the normalized output in 97.7–100% of 640 source pairs per language/configuration. Action insensitivity is therefore not the leading explanation for poor preservation; correctness and stable use of source roles remain unresolved. See [the action-sensitivity diagnostic](VI_EN_RESULTS_V4.23_ACTION_SENSITIVITY.md).

To reproduce without printing examples: `.venv/bin/python -B scripts/diagnose_validation_preservation.py data/pilot/vi-en-ai-v4.23 --markdown YOUR_DIAGNOSTIC.md`.

The script reads private validation generations but emits only aggregate counts; all private rows and generations remain Git-ignored under `data/` and `runs/`.
