# v4.32 train-only overfit sanity check

Preliminary AI-authored/AI-reviewed synthetic evidence. This is a memorization sanity check, not validation, a frozen quality gate, or evidence of generalization. It reads the protocol-bound train/validation review bundle, scores train rows only, writes no checkpoint, emits no source/reference/generated text, and leaves the release holdout sealed.

The v4.32 primary source-pointer/TIDE configuration was freshly initialized with seed 613 and its registered optimizer/objective. For each selected group, one reviewed single-action row was chosen for each language/action bucket. The 4-group run contains 32 examples and two explicitly licensed cross-language alignment pairs. The one-group run contains eight examples and one alignment pair. Group selection was deterministic and bound by hashes in the JSON artifacts. Scoring uses the frozen narrow semantic checker.

| Train sample | Step | Loss | Action fidelity | Preservation | Predicate | Patient | Unicode | EOS |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 group (8) | 0 | — | 0/8 | 0/8 | 0/8 | 0/8 | 8/8 | 8/8 |
| 1 group (8) | 100 | 0.16324 | 6/8 | 6/8 | 7/8 | 6/8 | 8/8 | 8/8 |
| 1 group (8) | 300 | 0.01585 | 8/8 | 8/8 | 8/8 | 8/8 | 8/8 | 8/8 |
| 1 group (8) | 600 | 0.00111 | 8/8 | 8/8 | 8/8 | 8/8 | 8/8 | 8/8 |
| 4 groups (32) | 0 | — | 0/32 | 0/32 | 0/32 | 0/32 | 32/32 | 32/32 |
| 4 groups (32) | 100 | 0.51959 | 3/32 | 0/32 | 2/32 | 2/32 | 32/32 | 32/32 |
| 4 groups (32) | 300 | 0.04674 | 32/32 | 32/32 | 32/32 | 32/32 | 32/32 | 32/32 |
| 4 groups (32) | 600 | 0.00201 | 32/32 | 32/32 | 32/32 | 32/32 | 32/32 | 32/32 |

Both samples became fully memorized by step 300, showing the current model and optimizer can fit small reviewed samples. This does not identify why full v4.32 training had weak English train exactness: scaling/interference across many groups, seed sensitivity, optimization schedule, and the synthetic task distribution remain possible contributors. It does not show unseen-group generalization, natural-language quality, or a TIDE advantage. The result is not used to alter v4.32 thresholds or admit a checkpoint.

Reproduce the one-group and four-group checks on Linux:

```sh
.venv/bin/python -B scripts/diagnose_train_group_overfit.py data/pilot/vi-en-ai-v4.32 --steps 600 --groups 1 --output /tmp/v432-overfit-one.json
.venv/bin/python -B scripts/diagnose_train_group_overfit.py data/pilot/vi-en-ai-v4.32 --steps 600 --groups 4 --output /tmp/v432-overfit-four.json
```

Machine-readable aggregate evidence: [one group](v432_train_group_overfit_1group.json), [four groups](v432_train_group_overfit_4groups.json). The script, protocol, review bundle, approval, config, and inventory SHA-256 identities are recorded in each file. Human validation is false; PhoMT and Phan Rang Cham were not used.
