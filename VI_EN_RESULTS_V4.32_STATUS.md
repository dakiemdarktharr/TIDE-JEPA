# v4.32 status — frozen validation gate failed

This is preliminary AI-authored, independently AI-reviewed synthetic English–Vietnamese evidence. It is not human/native-speaker validated. PhoMT was not used; Phan Rang Cham was not used.

## Frozen study and integrity

Version: `vi-en-ai-v4.32`; protocol SHA-256: `c288e9749402282ff27f2279e33ad13b58ee6c96612695ba41711bffcd5b0524`. The train/validation-only review bundle SHA-256 is `62fe45059d794b2b02091221da9fdad48b9e267a2391703abe21fcc5833f1077`. The study used a fresh 112/40/40 group split (8,960/3,200/3,200 records), six TIDE configurations (vocabulary/source-pointer decoders × seeds 17/23/41), fixed-final epoch 29, 3,248 optimizer updates per run, width 64, four heads, two layers, and CPU training. Checkpoint/config/runtime identities were audited after all workers exited; all six runs completed, with 29 train/validation metric epochs and 3,248 updates each. Validation generation was run on validation only.

## Quality result

The frozen quality gate **failed**. Zero of six complete configurations passed all required buckets. The 100% Unicode/EOS/checker coverage did not compensate for weak English single-action preservation and action fidelity. Across the source-pointer condition and seeds, English single-action pooled preservation was 58.4% and action fidelity was 85.5%; the held-out-path bucket reached 81.2% preservation and 98.1% action fidelity. Vietnamese single-action source-pointer preservation was 93.1% and action fidelity 98.0%. The thresholds remain unchanged: 100% valid Unicode/checker coverage; at least 90% fidelity and preservation for every single-action bucket; at least 80% for each held-out-path bucket. Since validation failed, **the 3,200-record release holdout remains sealed** and no checkpoint is admitted for user-facing language output.

The train-only checkpoint diagnostic found weak English teacher-forced exactness on the training sample despite approximately 99% byte accuracy. Wrong-source, wrong-action, and zero-latent interventions changed reference likelihood, showing that conditioning signals affect predictions; this does not establish correctness or a TIDE advantage. A separate bounded overfit sanity check memorized 8/8 and 32/32 reviewed train examples by 300 updates. It shows small-sample fitting capacity only, not generalization or the cause of full-dataset train weakness.

Detailed aggregate reports: [validation](audits/2026-10-08/VI_EN_V4.32_VALIDATION.md), [train checkpoint diagnostic](audits/2026-10-08/V432_TRAIN_DIAGNOSTIC.md), [action sensitivity](audits/2026-10-08/V432_ACTION_SENSITIVITY.md), [preservation diagnostic](audits/2026-10-08/V432_PRESERVATION_DIAGNOSTIC.md), and [train-only overfit sanity check](audits/2026-10-08/V432_TRAIN_GROUP_OVERFIT.md). These reports contain aggregate metrics only. The private corpus, review records, generated text, and checkpoints remain under Git-ignored `data/` and `runs/`.

## Linux reproduction

The frozen run and local artifacts are required for reproduction; training or evaluation commands fail closed if identity checks differ.

```sh
.venv/bin/python -B scripts/train_vi_en_parallel.py data/pilot/vi-en-ai-v4.32 --workers 4
.venv/bin/python -B -m tide_jepa.pilot evaluate data/pilot/vi-en-ai-v4.32 --evaluation-split validation
.venv/bin/python -B scripts/summarize_vi_en_validation.py data/pilot/vi-en-ai-v4.32 audits/2026-10-08/VI_EN_V4.32_VALIDATION.md
.venv/bin/python -B scripts/diagnose_train_checkpoint.py data/pilot/vi-en-ai-v4.32 --output /tmp/v432-train.json --markdown /tmp/v432-train.md
.venv/bin/python -B scripts/diagnose_train_group_overfit.py data/pilot/vi-en-ai-v4.32 --steps 600 --groups 1 --output /tmp/v432-overfit-one.json
.venv/bin/python -B scripts/diagnose_train_group_overfit.py data/pilot/vi-en-ai-v4.32 --steps 600 --groups 4 --output /tmp/v432-overfit-four.json
```

This evidence does not complete scientific M4, establish natural-language quality, or close external language/data gates. No commit or push was made.
