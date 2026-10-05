# v4.18 training-only overfit diagnostic

This is a training-fit sanity check, not a validation result, quality-gate result, or generalization claim. It uses one complete event group from the v4.18 **train split only** and never reads validation or release-holdout rows.

## Setup

- 80 approved synthetic training rows from one event group, including ordered paths.
- Eight representative single-action train requests, one for each language × action combination.
- Fresh randomly initialized TIDE-JEPA model; random seed 613; TIDE latent multiplier 0.1, source-copy weight 1.5, learning rate 0.001.
- The same 80 rows are repeated for 600 optimizer updates. No checkpoint is written.

## Aggregate outcome

| Update | Training loss | Action fidelity | Preservation |
|---:|---:|---:|---:|
| Initial | — | 0/8 | 0/8 |
| 1 | 20.1382 | 0/8 | 0/8 |
| 100 | 7.6249 | 0/8 | 0/8 |
| 300 | 0.2261 | 3/8 | 6/8 |
| 600 | 0.0334 | 8/8 | 8/8 |

This shows the implementation can memorize source-conditioned transformations on one seen lexical combination. It does not show lexical recombination or held-out generalization. Together with v4.18's poor post-hoc validation rescore, it points toward a generalization/data-coverage problem rather than a complete inability to fit the task. The diagnostic has one training group and one random seed, so this interpretation is preliminary.

The validation quality gate remains unmet, and the release holdout remains sealed. No PhoMT or Phan Rang Cham data was used. `human_validated=false`.

## Reproduction

```sh
.venv/bin/python -B scripts/diagnose_train_group_overfit.py data/pilot/vi-en-ai-v4.18 --steps 600 --seed 613
```

The script prints aggregate counts only, does not save a checkpoint, and asserts that its selected examples belong to the training split.
