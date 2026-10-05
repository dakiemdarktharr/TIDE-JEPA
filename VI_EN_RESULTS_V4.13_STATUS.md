# v4.13 status — validation complete, gate failed

v4.13 is a fresh AI-authored preliminary synthetic pilot with 7,680 records, 192 event groups and 112/40/40 train/validation/release-holdout groups. Its draft SHA-256 is `e633b47e33567f00943d0912dfb8c8ba7ad4b467f0c909c45d4eca1c7a3e4aec`. Two independent `gpt-6-luna` high reviewers approved the exact draft; their aggregate-only reviews and adjudication are bound to artifacts under ignored `data/`. This is preliminary AI review, not human validation.

The frozen dose-response protocol compared `token_only` and `tide` at source-copy weights 1.5 and 3.0, with seeds 17, 23 and 41. Both TIDE weight conditions were primary gates. All 12 unique runs completed 58 epochs / 3,248 steps. Post-training checks found matching config hashes, resolved/latest/best checkpoint run identities, implementation identity and runtime identity. Validation-only generation completed for all runs; the aggregate-only report is [VI_EN_RESULTS_V4.13_VALIDATION.md](VI_EN_RESULTS_V4.13_VALIDATION.md).

**The primary quality gate failed for both TIDE weights.** Only 10 of 60 seed-by-bucket checks passed. 47 of the 48 single-action language × action × seed × weight buckets missed the 90% preservation threshold; 9 of 12 path buckets met their 80% threshold. Unicode and EOS were 100%. `token_only` had higher pooled preservation at both matched weights, though individual buckets and other metrics vary, so this comparison supports no TIDE advantage. Exact-reference match and CER are synthetic-reference diagnostics, not measures of human naturalness. Per-seed denominators (160 single-action or 80 path examples) reuse the same 40 validation groups across seeds; they are operational counts, not independent linguistic observations.

The direct test-evaluation API refused the request before scoring because validation gates did not pass. No test metrics or test-generation artifacts were created. The release holdout remains sealed. PhoMT and Phan Rang Cham were not used. Rows, reviewer files, metrics and checkpoints remain private under Git-ignored `data/` and `runs/`.

Validation was run on Linux with the frozen v4.13 protocol and CPU runtime. Reproduction commands:

```bash
.venv/bin/python -B scripts/train_vi_en_parallel.py data/pilot/vi-en-ai-v4.13 --workers 4
.venv/bin/python -B -m tide_jepa.pilot evaluate data/pilot/vi-en-ai-v4.13 --evaluation-split validation
.venv/bin/python scripts/summarize_vi_en_validation.py data/pilot/vi-en-ai-v4.13 VI_EN_RESULTS_V4.13_VALIDATION.md
```

The training command resumes only when the existing run identity guard accepts the same configuration, data, split, implementation and runtime. Do not run the test-split command unless a future fresh version passes every preregistered validation gate. This preliminary synthetic result does not establish usable natural-language output or complete the scientific M4 benchmark.
