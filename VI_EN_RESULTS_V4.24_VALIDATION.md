# v4.24 frozen validation report

This report contains aggregate-only validation metrics for the AI-authored/AI-reviewed preliminary synthetic Vi–En pilot. `human_validated=false`; `phomt_used=false`. It does not include corpus rows, references, or generated text. The release holdout remains sealed.

## Protocol and completeness

Protocol SHA-256: `9939b50d2cdb9bd8099724baa4a6a2f2f875e003b3484efc3dfadb60d7df346f`.

Six vocabulary-decoder TIDE configs crossed source-copy weights 0 and 1.5 with seeds 17, 23, and 41. Each final checkpoint is epoch 29 / 3,248 updates; all config, approval, implementation, runtime, checkpoint, and validation-report identities were checked. The final `best.pt` and `latest.pt` tensors matched in all six runs. There are ten validation buckets per config: four single actions per language and one held-out path per language. Each config scored 2,880 generated examples; total `n=17,280`.

Gate thresholds were frozen before training: Unicode 100%, checker coverage 100%, single-action action fidelity and preservation at least 90% per bucket, and held-out-path fidelity and preservation at least 80% per bucket. No threshold was relaxed.

## Aggregate metrics

| Metric | Total | Rate |
|---|---:|---:|
| Valid Unicode | 17,280 / 17,280 | 100.0% |
| EOS termination | 17,280 / 17,280 | 100.0% |
| Semantic-checker coverage | 17,280 / 17,280 | 100.0% |
| Action fidelity | 16,492 / 17,280 | 95.4% |
| Preservation | 14,445 / 17,280 | 83.6% |
| Accepted-reference match | 14,219 / 17,280 | 82.3% |
| Weighted character error rate | 17,465 / 1,010,557 reference characters | 1.73% |

These totals are descriptive. The gate applies to every required bucket in every config, not to pooled rates. **0/6 configs passed all buckets; 28/60 individual bucket checks passed.**

| Config | Passed buckets | Frozen gate |
|---|---:|---|
| Copy 0, seed 17 | 8/10 | Fail |
| Copy 0, seed 23 | 4/10 | Fail |
| Copy 0, seed 41 | 5/10 | Fail |
| Copy 1.5, seed 17 | 4/10 | Fail |
| Copy 1.5, seed 23 | 1/10 | Fail |
| Copy 1.5, seed 41 | 6/10 | Fail |

## Bucket failures across the six configs

The table shows how often each bucket missed at least one applicable threshold, plus the observed range across the six configs. Fidelity/preservation ranges are not pooled estimates.

| Language / bucket | Failed configs | Action-fidelity range | Preservation range |
|---|---:|---:|---:|
| English / negative + past path | 2/6 | 97.5–100.0% | 76.3–100.0% |
| English / negative | 4/6 | 96.6–100.0% | 64.4–93.8% |
| English / positive | 4/6 | 95.6–100.0% | 56.3–93.1% |
| English / now | 6/6 | 95.9–99.7% | 54.4–89.7% |
| English / past | 3/6 | 97.5–99.1% | 65.3–93.4% |
| Vietnamese / negative + past path | 1/6 | 80.6–100.0% | 76.9–100.0% |
| Vietnamese / negative | 3/6 | 36.6–98.8% | 33.8–98.8% |
| Vietnamese / positive | 3/6 | 92.2–99.1% | 76.6–97.2% |
| Vietnamese / now | 3/6 | 52.8–99.7% | 50.6–98.8% |
| Vietnamese / past | 3/6 | 80.6–100.0% | 75.0–98.4% |

English `TIME:NOW` preservation is the most consistent blocker: all six configs missed its 90% threshold. Vietnamese performance varied substantially by seed in the negative and present buckets. Increasing source-copy weight did not yield a stable pass across both languages or all seeds. With three seeds per condition, this is descriptive seed/condition sensitivity, not a causal estimate.

## Interpretation and limits

Unicode, EOS, and evaluator coverage passed completely. Action fidelity was high in most buckets, while preservation varied more and failed across multiple single-action buckets. The near-universal same-source output changes under distinct requested actions (see [action-sensitivity diagnostic](VI_EN_RESULTS_V4.24_ACTION_SENSITIVITY.md)) show that the model responds to action conditioning, but do not establish that it preserves the source event. The [component rescore](VI_EN_RESULTS_V4.24_DIAGNOSTIC.md) finds agent/place retention near ceiling and lower patient/predicate retention, especially for English and the copy-weight-1.5 condition. This is a post-hoc, narrow synthetic rule-checker diagnosis, not human evaluation or proof of root cause.

Training CSVs for three configs contain duplicate, conflicting epoch/split rows. Final checkpoints and frozen identities were verified, but the affected CSVs are not suitable for epoch-wise or teacher-forced fit claims. A fail-closed resume-log check has since been added; the original artifacts remain unchanged. See [v4.24 status](VI_EN_RESULTS_V4.24_STATUS.md) and [audit closure](audits/2026-10-02/REPAIR_CLOSURE.md).

The runner refused release-test scoring because at least one primary validation bucket missed its frozen threshold. No test generation, test metric, or `suite_report.json` was created. The 3,200-record release holdout remains sealed. The result is preliminary synthetic evidence; it does not establish natural-language efficacy, human language quality, or a usable translation/demo checkpoint.
