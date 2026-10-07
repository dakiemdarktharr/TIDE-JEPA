# v4.29 status: fresh scoped-review language-balance pilot

**State:** six frozen TIDE runs and validation-only generation completed on Linux CPU. The validation evidence is identity-checked and complete, but the frozen quality gate **failed**: 1/6 configurations and 37/60 seed-by-bucket checks passed. The release holdout remains sealed. No checkpoint is approved for usable language output.

This is an original AI-authored English–Vietnamese synthetic pilot. Its review is preliminary AI evidence, not human/native-speaker validation. PhoMT was not used. Phan Rang Cham remains excluded.

## Why v4.29 exists

v4.27 was retired after review activity exposed test-split content. v4.28 was retired before freeze or training after a reviewer parsed the full semantic-frame catalog, which includes holdout frame annotations; the review record therefore marks holdout text inspected. No holdout sentence was emitted or scored, but that split is no longer eligible for a sealed-holdout claim. The v4.29 corpus and split are fresh.

The v4.29 comparison preserves the v4.28 hypothesis: at fixed 64-width/two-layer TIDE, source-copy weight 0, three seeds (17/23/41), 29 epochs, and fixed-final-epoch selection, compare global token CE with an equal-language-balanced base per-edge token term. Six configurations are registered after review. The validation gates remain unchanged: Unicode and checker coverage 100%, single-action action fidelity and preservation at least 90% for each language/bucket, and path buckets at least 80%.

## Review and context scope

The reviewer package is `data/pilot/vi-en-ai-v4.29/review_bundle/`. It contains only train/validation records, frames, groups, alignments, and inventory. Freeze verifies the bundle manifest hash, record count, split membership, and each bundle file hash. Two Luna/high reviews approved 12,160 rows each; both checked action/frame mappings, surface realization, alignments, and the declared context scope. They did not inspect holdout text and did not emit corpus text. The AI adjudication records the limited scope; no human validation is claimed.

The checker now reports a separate `context_preservation` diagnostic. Its declared scope is narrow: it checks the language-specific place marker for the shared-workshop context. It does not claim to evaluate broader discourse context. Context is diagnostic; frozen quality thresholds are unchanged.

## Identity

- Draft fingerprint: `cfcd2509550a0a194dda69dacb6f77fb552343d4aa8f1ebe06ed7ac23548edd1`
- Records: 15,360 total, 7,680 per language; 112/40/40 event groups and 8,960/3,200/3,200 train/validation/release-holdout rows.
- Reviewer scope: 12,160 train/validation rows; bundle manifest SHA-256 `a4ac06e3b32f0cb5f041192c70bff11d0803c04ca35f97c1f2e04faaea27f80c`.
- `inventory.draft.json`: `0aaaa75072502aff856d8540684e273ebac265152b5cf48f8075cf6af0c98fb3`
- `alignments.draft.json`: `50b8b62192965421f8f0d8ffee348fd4922fefbafde266b2b7e42584346106e4`
- `groups.json`: `bcd34f0782da707e340093193a20f6ec6a82baa70c4c95a1826a6c5a5f4af209`
- `data_statement.json`: `74ddb62f6ff537e3edba70183e26e0e6c2aee43f44c34fe116c51e291c8cdea3`
- `semantic_frames.draft.json`: `6ab973d724b401b67a3155dcc5de77cdea2d286a9f9db8a7f3aa8de2808b5ddf`

All corpus, review, model, and run data stay under Git-ignored `data/` and `runs/`. The latest Linux suite passes 123 tests with no skips; compileall, dependency, and diff checks pass. Those are engineering checks only, not quality evidence.

## Frozen protocol and current work

The six configurations cross seeds 17/23/41 with language-balance weights 0/1. Fixed settings: TIDE 64 width, 4 heads, 2 layers, source-copy weight 0, 29 epochs, batch 80, learning rate 0.001, and fixed-final-epoch checkpoint selection. Training command: `.venv/bin/python -B scripts/train_vi_en_parallel.py data/pilot/vi-en-ai-v4.29 --workers 2`. Validation runs only after every worker exits and checkpoint, log, config, runtime, and protocol identities pass integrity checks. If any validation gate fails, preserve the experiment and keep the release holdout sealed.

Verified freeze command:

```sh
.venv/bin/python -B -m tide_jepa.pilot freeze data/pilot/vi-en-ai-v4.29 --epochs 29 --model-width 64 --model-heads 4 --model-layers 2 --batch-size 80 --learning-rate 0.001 --primary-mode tide --condition-modes tide --condition-source-copy-weights 0 --condition-language-balance-weights 0 1 --checkpoint-selection-policy fixed_final_epoch
```

Validation-only command, to run after the complete training/integrity gate:

```sh
.venv/bin/python -B -m tide_jepa.pilot evaluate data/pilot/vi-en-ai-v4.29 --evaluation-split validation
```

## 2026-10-07 validation result

All six registered runs completed epoch 29 / 3,248 updates. A post-training audit verified the frozen code/runtime/approval/config hashes, matching resolved run identities, exact `latest.pt`/`best.pt` tensor equality at epoch 29, 29 train plus 29 validation metric rows per run, and no test artifacts. Validation-only generation completed with exit code 0 for all six runs. The aggregate report verifies each run/checkpoint/protocol/evaluator identity and includes no sample text.

The frozen gate **failed**. One of six complete configurations passed all buckets: language-balance weight 0 with seed 17. Across the 60 registered seed-by-bucket checks, 37 passed (22/30 at weight 0; 15/30 at weight 1). Preservation is the main weakness, especially English single-action buckets; the weight-1 condition also has substantial Vietnamese regressions at seed 41. A post-hoc component rescore found English single-action preservation of 83.2% at weight 0 and 76.4% at weight 1; Vietnamese was 98.9% and 87.9%. Distinct actions changed outputs for 100% of 640 paired sources in every run/language, which shows action sensitivity but not correct realization. Unicode, EOS, nonempty output, and semantic checker coverage were each 17,280/17,280 across conditions. Accepted-reference matches were 7,894/8,640 at weight 0 and 6,983/8,640 at weight 1; CER was 0.8% and 2.1%, respectively. These are synthetic-reference diagnostics, not naturalness judgments. The context-marker diagnostic is reported separately and is not part of the frozen gate.

No release-holdout generation or scoring occurred. The release holdout stays sealed because validation failed. OOD/unsupported-input refusal and truncation quality were not measured; EOS termination does not establish those behaviors. No model is cleared for user-facing language output. The evidence remains preliminary AI-reviewed synthetic data, not human/native-speaker validation.

Aggregate report: [v4.29 validation results](VI_EN_RESULTS_V4.29_VALIDATION.md), [post-hoc component rescore](VI_EN_RESULTS_V4.29_DIAGNOSTIC.md), and [action sensitivity](VI_EN_RESULTS_V4.29_ACTION_SENSITIVITY.md). Reproduction after training artifacts are present:

```sh
.venv/bin/python -B -m tide_jepa.pilot evaluate data/pilot/vi-en-ai-v4.29 --evaluation-split validation
.venv/bin/python -B scripts/summarize_vi_en_validation.py data/pilot/vi-en-ai-v4.29 VI_EN_RESULTS_V4.29_VALIDATION.md
```
