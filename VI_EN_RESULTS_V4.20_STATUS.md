# v4.20 status — validation gate failed; release holdout sealed

v4.20 is a new original AI-authored synthetic Vi–En pilot. Two independent `gpt-6-luna` high reviewers checked all 15,360 draft records; reviewer B approved and reviewer A's checksum-method concern was resolved by an artifact-bound AI adjudication. The statement fingerprint is the canonical `dataset_fingerprint`, and it matches the frozen corpus identity. This remains AI-reviewed preliminary work; `human_validated=false`.

The frozen protocol SHA-256 is `d2e911cb4d6e16627d7630a7d113530dcd73ae65a7806dc4bb68b70315400f23`; approval SHA-256 is `aec68baf28639c3eebdb84519c2e288b4e857b988ff8737008cd32699f1cb2c0`. The frozen corpus and split identities are `614a25a0d77604ccc0d7efdda74da5fdf9d36d6ca3ebe511b7aae8b95147bb1f` and `01aba80869bba126196bfa62835303e8ed721d26c6a0cdacb644f354f0c3197f`. The 192 event combinations use a 112/40/40 train/validation/release-holdout split (8,960/3,200/3,200 rows). All data and model artifacts remain local under Git-ignored `data/` and `runs/`.

## Frozen design

The preregistered study compares vocabulary-softmax and source-pointer mixture decoders at fixed TIDE objective, source-copy weight 0, latent-objective multiplier 0, row-uniform transition weighting, and seeds 17/23/41. Both decoder conditions use width 32, four heads, one layer, maximum length 192, batch size 80, learning rate 0.001, 29 fixed epochs, and 3,248 optimizer updates. The decoder variants differ in parameters and per-token operations; this is not a matched-FLOP comparison. The checkpoint policy is `fixed_final_epoch`.

Frozen thresholds are valid Unicode and checker coverage 100%, single-action action fidelity and preservation at least 90% in every language/action bucket, and held-out-path fidelity and preservation at least 80% in every bucket. Every primary decoder/seed must pass before a release holdout can be read.

## Training and validation outcome

All six runs completed 29/29 epochs and 3,248/3,248 updates. Every `latest.pt`, `best.pt`, and `resolved_run.json` has the same run identity for its registered configuration. No trainer remains active.

Validation generation completed for all six runs with complete semantic checker coverage. The quality gate **failed** for all six configurations and all 60 seed-by-bucket checks. Unicode, EOS termination, and nonempty output were 8,640/8,640 for each decoder across three seeds. Semantic performance remained poor:

| Decoder | Action fidelity | Preservation | Accepted synthetic references | Full buckets passed |
|---|---:|---:|---:|---:|
| Vocabulary | 3,682/8,640 (42.6%) | 49/8,640 (0.57%) | 22/8,640 | 0/30 |
| Source pointer | 2,809/8,640 (32.5%) | 39/8,640 (0.45%) | 16/8,640 | 0/30 |

The source-pointer hypothesis was not supported: its pooled action fidelity and preservation were lower than the vocabulary decoder. Three seeds on synthetic data do not establish a population-level treatment effect. Per-language/action/path denominators and seed-level diagnostics are in [v4.20 validation results](VI_EN_RESULTS_V4.20_VALIDATION.md).

## Why the run command stopped

Training did not stop from a model, memory, or checkpoint crash. `run_suite` finished training and validation, then failed closed at the validation-to-release-test transition because the primary validation buckets missed the frozen fidelity and preservation thresholds. Its release guard raises `ValueError` when those bound validation checks do not all pass. There is no `suite_report.json`, `test_metrics.json`, or release-generation artifact; the release holdout remains sealed.

After the run, the working tree also acquired uncommitted changes to files covered by the frozen implementation identity (`pilot.py`, `infer.py`, and `training.py`, among others). A fresh validation command now refuses to replay the frozen protocol with `current code/runtime differs from the frozen pilot protocol`. The already-recorded validation metrics remain bound to the protocol's original implementation identity; the working-tree edits require a fresh reviewed protocol for new training. Committing edits does not restore the old source hashes. `scripts/run_frozen.py` verifies the original implementation snapshot and runtime, so the old checkpoint can still run for diagnostic inference and cached validation replay without changing its identity. The original terminal buffer expired, so its exact final traceback is unavailable; the completed checkpoints, validation gate failure, and current replay-identity failure are directly verified.

Do not tune this version against validation or open its release holdout. Any next quality iteration needs a new corpus/version, independent review, adjudication, protocol, and sealed release holdout.

## Reproduction and evidence

The verified aggregate-only report command was:

```sh
/tmp/tide-jepa-bootstrap-20261006/bin/python scripts/summarize_vi_en_validation.py data/pilot/vi-en-ai-v4.20 VI_EN_RESULTS_V4.20_VALIDATION.md
```

It verified all six configs, checkpoints, validation evaluation identities, and every registered epoch, and reported `evaluation_valid=true`, `quality_gate=fail`, `release_test_opened=false`. The complete private review, approval, protocol, run, and generation artifacts are Git-ignored. No generated/reference text is included here. PhoMT and Phan Rang Cham were not used.
