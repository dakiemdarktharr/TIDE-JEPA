# Research workflow repair validation — 2026-10-07

The complete CPU test suite passed **140 tests, zero skips**, in 116.715 seconds after the final code changes:

```sh
OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 .venv/bin/python -B -m unittest discover -s tests -v
```

The HTTP tests require loopback access. The environment uses Python 3.11.17 and PyTorch 2.14.0+cpu. The optional NumPy initialization warning does not prevent these tests or inference. `git diff --check` passed.

The new regression cases cover v4.30 progressive corruption in both polarities, preservation of v4.23's legacy negative forms, explicit Vietnamese present-form declarations, negative-control preflight failure, mixed frozen/workspace module rejection, deterministic group-based sampling, corrupted bundle hashes, test groups, extra frame annotations, duplicate IDs, unknown groups, and separate token/sentence denominators. Validation diagnostic fixtures deliberately contain invalid full-corpus/full-catalog files; both tools succeed using the scoped review bundle.

Actual aggregate-only probes:

| Probe | Result |
|---|---|
| v4.29 exact frozen checker | All 7,168 intact train singles accepted; all tested negative controls rejected, including 1,792 progressive deletions. |
| v4.30 exact frozen checker | Intact references accepted; **0/1,792** progressive deletions rejected. CLI exit 1 is the expected reproduction of the historical defect. |
| Repaired working checker on the same v4.30 train bundle | All 7,168 intact references accepted and **1,792/1,792** progressive deletions rejected; remaining controls pass. |
| Real v4.30 launch preflight | Raises before creating a worker pool because the frozen checker fails negative controls. No duplicate training was launched. |
| Six completed v4.29 checkpoints | 128 fixed train singles/checkpoint, 79 distinct sampled groups, all six reports completed in **105.350 seconds** with one Torch thread. An independent rerun on 2026-10-08 reproduced the same sample identity and all aggregate metrics in **77.165 seconds**; output was aggregate-only under `/tmp/train-checkpoint-v429-recheck.md`. |
| Synthetic crash/identity root probe | Re-run on 2026-10-08 after inspecting its side effects. It created a disposable one-epoch fixture, recovered `best.pt` from `latest.pt`, kept release-test scoring sealed, and rejected a modified corpus at both evaluator and runner. Aggregate evidence: [root-probe JSON](root-probe-2026-10-08.json). |
| Scoped validation preservation diagnostic | All 17,280 saved generated examples processed with complete checker coverage, using review-bundle frames. No full corpus/holdout catalog opened. |
| Scoped validation action sensitivity | Six runs, 12 language/condition rows, all source pairs scored, using review-bundle records. |

Before changing the working checker, every v4.30 worker had already recorded its original run identity. Subsequent read-only checks confirmed all six still match the frozen implementation identity and no release-test generation/metrics artifacts are present. Four runs were at epoch 29; seed 41 runs continued. No frozen protocol, review artifact, checkpoint, dataset, or implementation snapshot was rebound by this repair.

The tests verify engineering behavior. Checkpoint probes use train examples and remain post-hoc preliminary synthetic evidence. They do not establish improved validation quality, JEPA benefit, human validation, or a released model. The original v4.29 quality gate remains failed and the v4.30 frozen checker limitation remains attached to that historical protocol. Release holdouts remain sealed. See [the research workflow](../../RESEARCH_ACCELERATION.md) and [checkpoint evidence](TRAIN_CHECKPOINT_V4.29.md).
