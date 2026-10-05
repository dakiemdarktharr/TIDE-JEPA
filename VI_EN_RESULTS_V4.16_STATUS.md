# v4.16 status — lower TIDE latent-objective doses

Status date: 2026-10-04. This is an AI-authored and independently AI-reviewed preliminary synthetic English–Vietnamese pilot, not human/native-speaker validation. PhoMT was not used; Phan Rang Cham remains deferred.

The completed v4.15 validation failed its frozen primary TIDE gate: 3/60 per-seed bucket checks passed (all Vietnamese paths), and no single-action bucket passed preservation. Unicode and EOS were 100%; pooled single-action preservation was lower for TIDE ×0.5 and ×1.0 than for token-only. Its fresh release holdout remains sealed. See [v4.15 aggregate status](VI_EN_RESULTS_V4.15_STATUS.md) and [validation report](VI_EN_RESULTS_V4.15_VALIDATION.md).

## v4.16 preregistration

To test whether the latent TIDE objective dose contributed to the prior preservation failures, v4.16-r2 freezes token-only against TIDE latent-objective multipliers 0.1 and 0.25, with source-copy weight fixed at 1.5. It uses seeds 17, 23, and 41; 29 epochs / 3,248 updates; width 48, four heads, two layers; and a fresh 112/40/40 group split (8,960/3,200/3,200 records). All thresholds are unchanged. The holdout is reserved unless every required validation gate passes.

Two independent `gpt-6-luna` high reviewers approved the exact r2 draft fingerprint `9076a9a4e235f3b4e8a9b1c82ec9deb6ca30ab97af728c799ee6ea947d2c9a6d` and all five reviewed artifact hashes. They reported no split, factor-coverage, semantic/context, alignment/path, provenance, or action-contract issue. Their review was aggregate-only; no corpus rows or text were disclosed. The review and adjudication files are bound privately to the ignored draft under `data/pilot/vi-en-ai-v4.16-r2/`.

The frozen protocol SHA-256 is `f24214a9582268b0ccea2a5547a79b46aefdfcad48d0ca894de2c06df9338dc0`. All nine CPU configurations completed at 29 epochs / 3,248 updates. Every config hash and resolved config matches the protocol; every run has both `best.pt` and `latest.pt`; runtime identity is Python 3.11.17 / PyTorch 2.14.0+cpu. Validation-only generation completed for all nine configs. The frozen primary gate failed: 6/60 seed-by-bucket checks passed, all six Vietnamese held-out-path checks; every single-action preservation bucket and every English path bucket failed. Pooled single-action preservation was 4,537/7,680 (59.1%) at TIDE ×0.1, 4,414/7,680 (57.5%) at TIDE ×0.25, and 4,735/7,680 (61.7%) for token-only. Unicode and EOS were 100%. The report is [VI_EN_RESULTS_V4.16_VALIDATION.md](VI_EN_RESULTS_V4.16_VALIDATION.md). No release-test artifacts exist; holdout remains sealed.

The dataset's fixed representation includes 3,072 path-step transition duplicates overall: 1,792 training rows and 640 each in validation and sealed holdout. Only the training copies add exposure during learning. This is a path-enriched record distribution, fixed across all conditions.
