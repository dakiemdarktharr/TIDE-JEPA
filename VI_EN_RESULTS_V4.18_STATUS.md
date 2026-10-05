# v4.18 status — validation failed; holdout sealed

The v4.18 corpus received two independent `gpt-6-luna` high approvals for preliminary AI use. Both reviews were bound to draft fingerprint `d6560f6896fe1f2d067f83147caedce1bcac88236aa23c0a5fcdb31dc91b09a8`; together they checked 15,360 unique rows, 192 groups, 768 semantic states, 7,680 bilingual edge alignments, and 768 bilingual path alignments. They reported no structural, frame/action, split coverage, surface, or alignment defects. This is AI review only; `human_validated=false`.

The frozen protocol SHA-256 is `278cefdd57da675211a1a9312701f6892a9d0bcdea14384bc73e35122bb3bb5e`. The approval artifact SHA-256 is `cc252f35d680cea86a2dfaf8d5b76bfbb7a1d38be9f41f604ed4c45147843bfc`. It registers 12 unique TIDE configurations: source-copy supervision 0/1.5 × TIDE auxiliary multiplier 0/0.1 × seeds 17/23/41, with unique-transition weighting held fixed. Every run uses the v4.17-matched CPU architecture and budget (width 32, four heads, one layer, batch 80, 29 epochs, 3,248 updates). The primary engineering thresholds remain Unicode 100%, single-action fidelity and preservation each ≥90%, and held-out-path fidelity and preservation each ≥80%, evaluated for every frozen primary condition, seed, and language/task bucket.

The fresh split uses 112/40/40 groups (8,960/3,200/3,200 records), holds out fresh factor combinations while requiring every held-out factor pair in training, and keeps the negative-polarity-then-past-time path order matched across train, validation, and release holdout. Thus the release holdout does not add the v4.17 action-order shift. The holdout is sealed and must not be evaluated unless every validation gate passes.

## Completed run and validation

All 12 frozen CPU configurations completed 29 epochs and 3,248 updates each. Checkpoint, corpus, split, config, review, and protocol identities were audited before validation. Validation-only generation completed for all 12 configurations; the release holdout was not evaluated and remains sealed.

The first frozen validation report is **invalid for semantic scoring**: the evaluator's event-family registry stopped at v4.17, so v4.18 had 0% checker coverage (`0/0` semantic denominators). Those values do not mean the model scored 0%. The gate correctly failed closed and the release holdout was not evaluated. A supplemental post-hoc rescore using the corrected checker covered all saved validation generations, but it is diagnostic only and cannot replace the frozen gate. It measured action fidelity of 26.5–52.5% for single actions and 51.0–72.9% for paths; preservation was 0.4–1.9% and 0.8–8.3%, respectively. In single-action outputs, patient presence was only 7.7–22.1% and predicate presence 5.2–11.2%, pointing to weak source-slot retention and transformation control. The corrected scores remain below every registered threshold. See the [frozen evaluation report](VI_EN_RESULTS_V4.18_VALIDATION.md) and [post-hoc rescore](VI_EN_RESULTS_V4.18_RESCORING.md); both contain aggregate metrics only.

A separate training-only sanity check overfit one 80-row training group: action fidelity and preservation rose from 0/8 to 8/8 after 600 updates, with final loss 0.0334. This shows memorization capacity for seen combinations, not generalization. The evidence shifts diagnosis toward generalization/data coverage rather than a complete inability to fit the training transformation. The script parses the complete corpus to verify the frozen split manifest, then selects and scores train rows only; it never selects, scores, or emits validation or release-holdout rows. See the [overfit diagnostic](VI_EN_RESULTS_V4.18_OVERFIT_DIAGNOSTIC.md).

The private corpus, reviews, protocol, metrics, generations, and checkpoints remain under Git-ignored `data/` and `runs/`. No PhoMT or Phan Rang Cham data was used. `human_validated=false`.

The run command is:

```sh
.venv/bin/python -B scripts/train_vi_en_parallel.py data/pilot/vi-en-ai-v4.18 --workers 4
```

After training is complete, verify every registered config and checkpoint identity before running validation only:

```sh
.venv/bin/python -B -m tide_jepa.pilot evaluate data/pilot/vi-en-ai-v4.18 --evaluation-split validation
.venv/bin/python -B scripts/summarize_vi_en_validation.py data/pilot/vi-en-ai-v4.18 VI_EN_RESULTS_V4.18_VALIDATION.md
```

The v4.18 semantic checker fix and complete-coverage precondition are now regression-tested. Current Linux verification passes 92 CPU tests with no skips, including the demo's one-at-a-time generation limit; compileall, `pip check`, and `git diff --check` also pass. Any follow-up quality gate must freeze the corrected evaluator before validation; use a fresh version, corpus/reviews/protocol, and release holdout. Never tune against the sealed v4.18 holdout. All reports remain aggregate-only and label the work preliminary and AI-reviewed, not human validated.
