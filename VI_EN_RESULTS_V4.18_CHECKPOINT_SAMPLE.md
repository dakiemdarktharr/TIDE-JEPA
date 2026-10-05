# v4.18 checkpoint-selection sample diagnostic

This post-hoc check compares the frozen `best.pt` checkpoint (selected at epoch 28) with `latest.pt` (epoch 29) for the two seed-23 source-copy conditions. It is a small diagnostic sample, **not** frozen protocol evidence, a quality-gate result, or a reason to open the release holdout.

The script chooses the first two validation records for each language/single-action bucket and first two paths for each language/path-action bucket in the stored corpus order. The same 20 inputs are used for each checkpoint in a condition. Because those examples cluster in very few event families, the denominators are too small to estimate full validation quality. The script copies only the required synthetic artifacts and checkpoints to a temporary directory, rebinds temporary protocol/run identities to the current checker, emits aggregate counts only, and removes the temporary files at exit. It never selects or scores release-holdout records and never prints or saves source, reference, or generated text.

| Source-copy weight | Checkpoint | Examples | Action fidelity | Preservation | Accepted reference match | Valid Unicode |
|---:|---|---:|---:|---:|---:|---:|
| 0 | best, epoch 28 | 20 | 14/20 (70%) | 0/20 (0%) | 0/20 (0%) | 20/20 (100%) |
| 0 | latest, epoch 29 | 20 | 11/20 (55%) | 0/20 (0%) | 0/20 (0%) | 20/20 (100%) |
| 1.5 | best, epoch 28 | 20 | 14/20 (70%) | 0/20 (0%) | 0/20 (0%) | 20/20 (100%) |
| 1.5 | latest, epoch 29 | 20 | 13/20 (65%) | 0/20 (0%) | 0/20 (0%) | 20/20 (100%) |

Per-language/task checker coverage was 100% in all four samples. The small sample gives no indication that the final epoch repairs the failure: `best` is slightly higher on action fidelity, while neither checkpoint preserves all required frame slots or matches an accepted reference. The broader v4.18 corrected-checker validation rescore remains the relevant aggregate evidence and also fails the frozen thresholds; see [the v4.18 rescore](VI_EN_RESULTS_V4.18_RESCORING.md).

This check is consistent with a source-slot/generalization problem and shows that checkpoint epoch alone does not explain the observed collapse. Its narrow sampling does not establish that checkpoint selection is harmless across the full validation set. A follow-up should freeze a selection/confirmation design before training and should keep neural checkpoint scores separate from any rule-based fallback.

`human_validated=false`; PhoMT was not used. The v4.18 release holdout remains sealed.

Reproduce the aggregate-only sample with:

```sh
.venv/bin/python -B scripts/diagnose_v418_checkpoint_sample.py data/pilot/vi-en-ai-v4.18 runs/vi-en-ai-v4.18
```
