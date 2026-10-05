# vi-en-ai-v4.18 post-hoc semantic rescore

This is a diagnostic rescore of saved validation generations after discovering that the frozen evaluator omitted v4.18 event families. It is **not frozen-protocol gate evidence** and does not authorize opening the release holdout.

The original evaluator had zero semantic checker coverage (`0/0` action fidelity and preservation denominators). After adding v4.18 coverage to the checker, this rescore covers every saved validation example. Results remain preliminary AI-authored synthetic evidence; `human_validated=false`, `phomt_used=false`.

Frozen training protocol SHA-256: `278cefdd57da675211a1a9312701f6892a9d0bcdea14384bc73e35122bb3bb5e`.

| Condition | Language | Task | Examples | Checker coverage | Action fidelity | Agent | Patient | Predicate | Place | All preserved |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| tide, copy 0, aux 0.1 | en | held_out_path | 480 | 480/480 (100.0%) | 350/480 (72.9%) | 89.2% | 14.4% | 23.3% | 84.2% | 27/480 (5.6%) |
| tide, copy 0, aux 0.1 | en | single | 3840 | 3840/3840 (100.0%) | 1679/3840 (43.7%) | 75.9% | 7.7% | 5.4% | 71.9% | 18/3840 (0.5%) |
| tide, copy 0, aux 0.1 | vi | held_out_path | 480 | 480/480 (100.0%) | 323/480 (67.3%) | 75.4% | 17.5% | 20.0% | 86.2% | 6/480 (1.2%) |
| tide, copy 0, aux 0.1 | vi | single | 3840 | 3840/3840 (100.0%) | 1229/3840 (32.0%) | 68.8% | 12.9% | 12.3% | 83.5% | 43/3840 (1.1%) |
| tide, copy 0, aux 0 | en | held_out_path | 480 | 480/480 (100.0%) | 339/480 (70.6%) | 94.4% | 13.3% | 22.9% | 81.7% | 34/480 (7.1%) |
| tide, copy 0, aux 0 | en | single | 3840 | 3840/3840 (100.0%) | 1685/3840 (43.9%) | 70.7% | 9.8% | 5.2% | 67.3% | 27/3840 (0.7%) |
| tide, copy 0, aux 0 | vi | held_out_path | 480 | 480/480 (100.0%) | 245/480 (51.0%) | 82.7% | 20.4% | 13.8% | 81.2% | 4/480 (0.8%) |
| tide, copy 0, aux 0 | vi | single | 3840 | 3840/3840 (100.0%) | 1051/3840 (27.4%) | 67.6% | 14.6% | 8.9% | 78.5% | 15/3840 (0.4%) |
| tide, copy 1.5, aux 0.1 | en | held_out_path | 480 | 480/480 (100.0%) | 316/480 (65.8%) | 95.0% | 21.9% | 24.2% | 84.8% | 40/480 (8.3%) |
| tide, copy 1.5, aux 0.1 | en | single | 3840 | 3840/3840 (100.0%) | 1834/3840 (47.8%) | 84.3% | 12.8% | 6.5% | 76.6% | 50/3840 (1.3%) |
| tide, copy 1.5, aux 0.1 | vi | held_out_path | 480 | 480/480 (100.0%) | 279/480 (58.1%) | 72.9% | 24.6% | 21.5% | 94.8% | 11/480 (2.3%) |
| tide, copy 1.5, aux 0.1 | vi | single | 3840 | 3840/3840 (100.0%) | 1053/3840 (27.4%) | 72.9% | 21.9% | 11.2% | 93.5% | 73/3840 (1.9%) |
| tide, copy 1.5, aux 0 | en | held_out_path | 480 | 480/480 (100.0%) | 328/480 (68.3%) | 80.4% | 19.8% | 24.0% | 88.3% | 24/480 (5.0%) |
| tide, copy 1.5, aux 0 | en | single | 3840 | 3840/3840 (100.0%) | 2017/3840 (52.5%) | 79.1% | 11.2% | 6.9% | 79.7% | 40/3840 (1.0%) |
| tide, copy 1.5, aux 0 | vi | held_out_path | 480 | 480/480 (100.0%) | 260/480 (54.2%) | 77.9% | 24.2% | 15.6% | 89.4% | 18/480 (3.8%) |
| tide, copy 1.5, aux 0 | vi | single | 3840 | 3840/3840 (100.0%) | 1016/3840 (26.5%) | 74.7% | 22.1% | 9.5% | 91.2% | 68/3840 (1.8%) |

The rescore does not pass the preregistered single-action (≥90%) or held-out-path (≥80%) thresholds. Its post-hoc timing means it is diagnostic only; any follow-up quality gate must use a fresh version with the corrected evaluator frozen before training/evaluation. The release holdout remains sealed.

To reproduce without printing examples: `.venv/bin/python -B scripts/diagnose_validation_preservation.py data/pilot/vi-en-ai-v4.18 --markdown VI_EN_RESULTS_V4.18_RESCORING.md`.

The script reads private validation generations but emits only aggregate counts; all private rows and generations remain Git-ignored under `data/` and `runs/`.
