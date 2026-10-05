# v4.14 status — validation gate failed; holdout sealed

v4.14 tests whether balanced surface/context diversity improves single-action preservation without changing the model or frozen quality gate. The first draft added tense-dependent context that reviewers correctly identified as a confound. It remains unapproved and was never frozen or trained. The corrected revision keeps a single workshop location invariant across all time/polarity states and records that place in the semantic frames and narrow checker.

The revised draft is `data/pilot/vi-en-ai-v4.14-r1/`, SHA-256 `ca106f8defe36bfa14628b635b0f86393921ac3bfaf5d4254532e74fc0035482`. It has 15,360 AI-authored synthetic records (8,960/3,200/3,200 train/validation/release holdout), four surface forms per meaning state, and 192 fresh event groups split 112/40/40. Two independent `gpt-6-luna` high reviewers approved this exact revision; their artifact-bound review and adjudication are private under ignored `data/`. The first draft's reviewers found a real time/context confound; the correction passed both independent reviews.

The frozen matched conditions are `token_only` and `tide`, source-copy weight 1.5, seeds 17/23/41, width 48, four heads, two layers, batch 80, 29 epochs (3,248 updates/config). Four-worker CPU training and validation-only generation completed for all six configurations. The primary `tide` gate failed: only 4/30 seed-by-bucket checks passed, all four being held-out paths; 0/24 single-action buckets passed. Four of six path buckets passed. Unicode and EOS were 100%. Token-only had higher pooled preservation in every language/action/path bucket, so these results do not support a TIDE advantage. Full aggregate-only measurements are in [VI_EN_RESULTS_V4.14_VALIDATION.md](VI_EN_RESULTS_V4.14_VALIDATION.md). The v4.14 release holdout remains sealed because at least one frozen validation gate failed; no test metrics or generated test artifacts exist.

All three seeds use the same 40 validation event groups, so seed-by-bucket counts are operational checks, not independent linguistic observations. The deterministic checker covers only the declared synthetic tense/polarity grammar and named roles. This AI-authored, AI-reviewed preliminary experiment is not human/native-speaker validated and does not establish naturalness or natural-corpus efficacy.

Two independent Luna agents reviewed aggregate results and agreed the token-only control outperformed TIDE on pooled preservation. A separate engineering audit found that TIDE-specific terms made up 32.8%–41.0% of selected-checkpoint validation loss; one train-batch gradient probe per seed found auxiliary gradient norms below the shared decoder norms and below the clip threshold. That probe is too narrow to infer a better coefficient. See the [objective implementation audit](VI_EN_RESULTS_V4.14_OBJECTIVE_AUDIT.md). A future comparison should keep this failed version and holdout unchanged, then test a pre-registered lower auxiliary coefficient on a fresh reviewed split alongside the matched token-only and current-TIDE conditions.

This is an AI-authored, AI-reviewed preliminary synthetic experiment, never human/native-speaker validated. PhoMT was not used; Phan Rang Cham remains excluded. All rows and review evidence stay under ignored `data/`; checkpoints and run logs stay under ignored `runs/`.

```bash
.venv/bin/python -B scripts/train_vi_en_parallel.py data/pilot/vi-en-ai-v4.14-r1 --workers 4
.venv/bin/python -B -m tide_jepa.pilot evaluate data/pilot/vi-en-ai-v4.14-r1 --evaluation-split validation
.venv/bin/python -B scripts/summarize_vi_en_validation.py data/pilot/vi-en-ai-v4.14-r1 VI_EN_RESULTS_V4.14_VALIDATION.md
```
