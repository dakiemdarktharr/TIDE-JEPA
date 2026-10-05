# v4.19 status — frozen; training not started

v4.19 is a fresh original AI-authored synthetic Vi–En corpus and split. Two independent `gpt-6-luna` high reviewers approved the same draft fingerprint `52d34c118838996544574a0f4b61c3b80dd1b57f159918c7b9c0cd8719c17e6c`, checked all 15,360 records, and reported zero unresolved in-scope defects. Their evidence is bound to the draft inventory, alignments, group manifest, data statement, and semantic-frame catalog. This is preliminary AI review; `human_validated=false`.

The frozen protocol SHA-256 is `7a6f2fa674833bdd11b769ee771fdd5d7f7ab88d10b1f5576d34a5bb2b25ded3`; the approval SHA-256 is `11c93e8ce419b0040ac3cb93ed96f7326c009f6552e7f084d75082656330b270`. Frozen corpus and split identities are `2eff02d30fa1714fc8ff702e8863791e6e3921bde5224aa7c4a0dcd1721f8058` and `de663fcbfe8b798e627139b750f6737991aad0106e64aefd1e584f57d7aefc7c`. The pilot has 192 event groups in a 112/40/40 train/validation/release-holdout split (8,960/3,200/3,200 records). The holdout is sealed.

## Frozen design

The registered study is a TIDE-only 2×2 objective matrix: source-copy weight 0/1.5 × latent-objective multiplier 0/0.1, crossed with seeds 17/23/41. All cells use unique-transition weighting, width 48, four heads, two layers, maximum length 192, batch size 80, learning rate 0.001, 29 epochs, and 3,248 optimizer updates. Every cell computes the same TIDE and source-copy loss terms; the source-copy term is calculated even at weight zero, so the treatment changes its gradient multiplier rather than adding a compute branch. The model, examples, batch schedule, and loss computation path are matched within this factorial; per-run tokens, updates, throughput, wall time, and memory remain logged.

Checkpoint selection is `fixed_final_epoch`: the completed run evaluates the preregistered epoch-29 checkpoint, with `best.pt` kept synchronized with `latest.pt` for recovery. Validation loss does not choose which checkpoint is evaluated. Frozen quality thresholds remain Unicode 100%, single-action action fidelity and preservation ≥90% per bucket, and held-out-path action fidelity and preservation ≥80% per bucket. Every primary cell, seed, language, and action bucket must pass before the release holdout can be opened.

The study uses fresh agent factors and a new holdout, four context-balanced surface forms per state, and the same action order in every split. It tests the source-copy and latent-dose hypotheses at a fixed restored 48×2 architecture. Cross-version comparisons with v4.18 are descriptive because architecture and pilot version differ. The corpus is synthetic; it does not establish natural-language generalization or human validation.

## Status and limits

Training has not started; no run directories or model checkpoints exist. There is no validation generation, suite report, or quality result yet. No generation or metric evaluation has been run on the release holdout. No PhoMT or Phan Rang Cham data was used. The preliminary pilot remains not human validated.

## Reproduction

Author the private draft and bind the frozen protocol with the verified commands below. The draft and all reviewer/protocol artifacts stay under Git-ignored `data/`.

```sh
.venv/bin/python -B -m tide_jepa.pilot_seed data/pilot/vi-en-ai-v4.19 --pilot-version v4.19
.venv/bin/python -B -m tide_jepa.pilot freeze data/pilot/vi-en-ai-v4.19 --epochs 29 --model-width 48 --model-heads 4 --model-layers 2 --batch-size 80 --learning-rate 0.001 --primary-mode tide --condition-modes tide --condition-source-copy-weights 0 1.5 --condition-latent-objective-weights 0 0.1 --condition-transition-balances unique_transition --checkpoint-selection-policy fixed_final_epoch --compute-source-copy-term
```

The source code, tests, protocol hash, and aggregate status are versioned in Git. The corpus, review records, approvals, configs, run outputs, and checkpoints remain local and ignored.
