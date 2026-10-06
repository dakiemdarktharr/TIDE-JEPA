# v4.21 frozen pilot status — 2026-10-06

This is a fresh, AI-authored English–Vietnamese synthetic pilot. Its two reviews and adjudication are AI-only and preliminary; `human_validated=false`. PhoMT was not used. Phan Rang Cham remains excluded.

## Frozen evidence

- Draft SHA-256: `edd6c1e2a92adace02ca280faa68548c2cf9d520fa6f9b5c130cc8a5c36ca12d` (15,360 records; 192 event combinations; 112/40/40 whole-group train/validation/release-holdout split).
- The three agent factors are new relative to v4.20. Every held-out factor pair is represented in training. English NOW uses present progressive; all splits use the same ordered action paths and four context-balanced surface realizations per meaning state.
- Two independent `gpt-6-luna` high reviewers inspected all 15,360 records and approved the exact draft. Review A recorded one nonblocking English punctuation-style note. AI adjudication retained it as a limitation; no human validation is implied.
- Approved corpus SHA-256: `f5153214e5dcf991dc585b679f0354c9cab33b0bd6b3b545413f659524e05c48`.
- Split SHA-256: `b5244e30e9778829f206058dea726b53e4c1409860ded7730aa4ab4df25c746e`.
- Inventory SHA-256: `288d9c3f598b2a7708dcfedfb4c4baa7982f08a704dd69dd722590f454e4729d`.
- Alignment SHA-256: `cb5043b244169ff253c5a0766ded6e694218b2206863b7380be87ad1fb5357f2`.
- Frozen protocol SHA-256: `5b48e8348c2ef3fc1a4db9841c713560fd7bc24bbbd57a67691884f87e33d7de`.
- Protocol registers 12 runs: TIDE, seeds 17/23/41, source-copy weights 0/1.5, vocabulary/source-pointer decoders, 29 fixed epochs, width 32, four heads, one layer, batch size 80, learning rate 0.001. The source-copy term is computed in all cells; its multiplier and decoder mode are crossed. Decoder compute differs, so no matched-FLOP claim is made.
- Checkpoint selection is fixed-final-epoch. Validation cannot select checkpoints. Gate thresholds remain Unicode/checker coverage 100%, single-action fidelity and preservation ≥90%, held-out-path fidelity and preservation ≥80%, for every registered seed and language/action bucket.
- Code and runtime identities, all 12 config hashes, and the complete 2×2×3 matrix were verified against the frozen protocol. No training output directory existed when this protocol was frozen.

## Run state

Training has not started. Validation generation has not run. No release-holdout metrics or generations exist; the release holdout remains sealed. The hypothesis is that source-copy supervision and a source-pointer decoder may interact to improve joint role preservation and action fidelity over either component alone. This is a preregistered hypothesis, not an expected result. Results will be reported per cell and descriptively across three seeds; no population-level claim is planned.

All corpus, review, adjudication, protocol and future run/checkpoint artifacts stay in Git-ignored `data/` and `runs/`. Public reports will contain aggregate metrics only.

## Reproduction

The verified freeze command was:

```sh
.venv/bin/python -B -m tide_jepa.pilot freeze data/pilot/vi-en-ai-v4.21 \
  --epochs 29 --model-width 32 --model-heads 4 --model-layers 1 --max-length 192 \
  --batch-size 80 --learning-rate 0.001 --primary-mode tide --condition-modes tide \
  --condition-source-copy-weights 0 1.5 \
  --condition-source-pointer-decoder-modes vocabulary source_pointer \
  --checkpoint-selection-policy fixed_final_epoch --compute-source-copy-term
```

After freeze, run the registered configurations with the identity-checking launcher, wait until all workers exit, and verify every checkpoint/config/runtime identity before validation-only generation:

```sh
.venv/bin/python -B scripts/train_vi_en_parallel.py data/pilot/vi-en-ai-v4.21 --workers 4
.venv/bin/python -B -m tide_jepa.pilot evaluate data/pilot/vi-en-ai-v4.21 --evaluation-split validation
```

Do not evaluate the release holdout unless every frozen primary validation gate passes.
