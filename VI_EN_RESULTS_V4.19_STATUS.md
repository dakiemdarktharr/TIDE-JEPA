# v4.19 status — validation gate failed; release holdout sealed

v4.19 is a fresh original AI-authored synthetic Vi–En corpus and split. Two independent `gpt-6-luna` high reviewers approved the same draft fingerprint `52d34c118838996544574a0f4b61c3b80dd1b57f159918c7b9c0cd8719c17e6c`, checked all 15,360 records, and reported zero unresolved in-scope defects. Their evidence is bound to the draft inventory, alignments, group manifest, data statement, and semantic-frame catalog. This is preliminary AI review; `human_validated=false`.

The frozen protocol SHA-256 is `7a6f2fa674833bdd11b769ee771fdd5d7f7ab88d10b1f5576d34a5bb2b25ded3`; the approval SHA-256 is `11c93e8ce419b0040ac3cb93ed96f7326c009f6552e7f084d75082656330b270`. Frozen corpus and split identities are `2eff02d30fa1714fc8ff702e8863791e6e3921bde5224aa7c4a0dcd1721f8058` and `de663fcbfe8b798e627139b750f6737991aad0106e64aefd1e584f57d7aefc7c`. The pilot has 192 event groups in a 112/40/40 train/validation/release-holdout split (8,960/3,200/3,200 records). The holdout is sealed.

## Frozen design

The registered study is a TIDE-only 2×2 objective matrix: source-copy weight 0/1.5 × latent-objective multiplier 0/0.1, crossed with seeds 17/23/41. All cells use unique-transition weighting, width 48, four heads, two layers, maximum length 192, batch size 80, learning rate 0.001, 29 epochs, and 3,248 optimizer updates. Every cell computes the same TIDE and source-copy loss terms; the source-copy term is calculated even at weight zero, so the treatment changes its gradient multiplier rather than adding a compute branch. The model, examples, batch schedule, and loss computation path are matched within this factorial; per-run tokens, updates, throughput, wall time, and memory remain logged.

Checkpoint selection is `fixed_final_epoch`: the completed run evaluates the preregistered epoch-29 checkpoint, with `best.pt` kept synchronized with `latest.pt` for recovery. Validation loss does not choose which checkpoint is evaluated. Frozen quality thresholds remain Unicode 100%, single-action action fidelity and preservation ≥90% per bucket, and held-out-path action fidelity and preservation ≥80% per bucket. Every primary cell, seed, language, and action bucket must pass before the release holdout can be opened.

The study uses fresh agent factors and a new holdout, four context-balanced surface forms per state, and the same action order in every split. It tests the source-copy and latent-dose hypotheses at a fixed restored 48×2 architecture. Cross-version comparisons with v4.18 are descriptive because architecture and pilot version differ. The corpus is synthetic; it does not establish natural-language generalization or human validation.

## Training and validation outcome

All 12 frozen CPU configurations completed at epoch 29 / 3,248 optimizer steps each. Before generation, code verified every registered config, review approval, corpus/split, implementation, runtime, checkpoint identity, train/validation epoch count, and matching `best.pt`/`latest.pt` model weights. The check passed 12/12; no trainer remained active. Validation-only generation then completed for all 12 configurations, with complete semantic-checker coverage.

The frozen quality gate **failed**. No configuration passed all its required buckets (0/12); 4 of 120 seed-by-bucket checks passed all applicable criteria. Unicode and EOS termination were 8,640/8,640; semantic checker coverage was 8,640/8,640. Failures were driven mainly by state preservation, with additional single-action action-fidelity misses. The detailed aggregate-only denominators and per-seed failure reasons are in [v4.19 validation results](VI_EN_RESULTS_V4.19_VALIDATION.md).

Across the three seeds, the pooled condition aggregates were:

| Source-copy weight | Latent multiplier | Action fidelity | Preservation | Accepted synthetic references | Gate checks passed |
|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 7,706/8,640 (89.2%) | 4,924/8,640 (57.0%) | 4,549/8,640 | 2/30 |
| 0 | 0.1 | 7,710/8,640 (89.2%) | 4,451/8,640 (51.5%) | 3,985/8,640 | 1/30 |
| 1.5 | 0 | 7,230/8,640 (83.7%) | 4,259/8,640 (49.3%) | 3,951/8,640 | 0/30 |
| 1.5 | 0.1 | 7,296/8,640 (84.4%) | 4,740/8,640 (54.9%) | 4,281/8,640 | 1/30 |

These aggregates do not establish a reliable treatment effect with three seeds and synthetic grammar. Source-copy weight 1.5 reduced pooled action fidelity in both latent-dose comparisons; its preservation response changed direction across latent doses. No non-TIDE baseline was registered in this version, so no TIDE-versus-control advantage is tested. The results do not support a usable natural-language output claim.

The release holdout remains sealed: no test generation, test metrics, or suite report exists. Do not tune v4.19 against its validation split. No PhoMT or Phan Rang Cham data was used. This pilot remains AI-reviewed and preliminary, not human/native-speaker validated.

## Reproduction

Author the private draft and bind the frozen protocol with the verified commands below. The draft and all reviewer/protocol artifacts stay under Git-ignored `data/`.

```sh
.venv/bin/python -B -m tide_jepa.pilot_seed data/pilot/vi-en-ai-v4.19 --pilot-version v4.19
.venv/bin/python -B -m tide_jepa.pilot freeze data/pilot/vi-en-ai-v4.19 --epochs 29 --model-width 48 --model-heads 4 --model-layers 2 --batch-size 80 --learning-rate 0.001 --primary-mode tide --condition-modes tide --condition-source-copy-weights 0 1.5 --condition-latent-objective-weights 0 0.1 --condition-transition-balances unique_transition --checkpoint-selection-policy fixed_final_epoch --compute-source-copy-term
```

The source code, tests, protocol hash, and aggregate validation report are versioned in Git. The corpus, review records, approvals, configs, run outputs, generated validation text, and checkpoints remain local and ignored. Reproduce training with `.venv/bin/python -B scripts/train_vi_en_parallel.py data/pilot/vi-en-ai-v4.19 --workers 4`, then run validation only with `.venv/bin/python -B -m tide_jepa.pilot evaluate data/pilot/vi-en-ai-v4.19 --evaluation-split validation` and summarize with `.venv/bin/python -B scripts/summarize_vi_en_validation.py data/pilot/vi-en-ai-v4.19 VI_EN_RESULTS_V4.19_VALIDATION.md`.
