# v4.12 status

The v4.12 preliminary pilot uses a fresh AI-authored synthetic corpus and release holdout. Two independent `gpt-6-luna` high reviews approved the exact draft, bound to SHA-256 `cee551c5c9405240c94fad320530cf62e14143480934e13d4fef1908297485ac`. The review and adjudication files remain private under Git-ignored `data/`; approval is preliminary AI review, not human validation.

The frozen 2×2 ablation compared `token_only` and `tide` with source-copy weights 0 and 1.5, across seeds 17, 23 and 41. All 12 runs completed 58 epochs / 3,248 updates. Configuration, approval, implementation, runtime, `latest.pt`, `best.pt` and resolved run identities matched the frozen protocol before evaluation.

Validation-only generation completed for all 12 runs. **The primary TIDE gate failed for both configured source-copy weights across all three seeds.** Unicode validity and EOS termination were 100%. Held-out-path buckets met their lower engineering thresholds. At weight 1.5, preservation improved substantially over weight 0, especially in English, but several English seed-41 buckets and Vietnamese single-action buckets still fell below the required 90%. The result does not meet the engineering quality contract; no usable neural translation/generation claim is supported. Controls are diagnostic, and no TIDE advantage is claimed.

The release holdout remains sealed. A direct `--evaluation-split test` request was refused with “every primary validation gate must pass on bound evidence” before test scoring. No test metrics were created. PhoMT was not used. Phan Rang Cham remains excluded.

See the [aggregate-only validation report](VI_EN_RESULTS_V4.12_VALIDATION.md) for per-condition and seed-by-bucket counts. Private examples, generations, metrics and checkpoints remain under Git-ignored `data/` and `runs/`.
