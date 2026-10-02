# Historical preliminary Vi–En pilot results

This file preserves earlier AI-authored/AI-reviewed synthetic pilot results after the active summary moved to v4.2. All results are preliminary; none were human/native-speaker validated. PhoMT was not used for model training, and Phan Rang Cham remains excluded.

## v3 baseline

The v3 corpus contained 400 records in 20 event families, with 240/80/80 train/validation/test. Four objective controls and seeds 17/23/41 ran for 40 epochs (120 updates per run). The immutable historical evaluation reported:

| Mode | Test token CE, mean ± SD | Test path token CE, mean ± SD | Exact matches | Valid UTF-8 |
|---|---:|---:|---:|---:|
| token_only | 2.6403 ± 0.0824 | 2.5078 ± 0.0581 | 0/216 | 151/216 (69.9%) |
| generic_jepa | 2.5869 ± 0.0545 | 2.4287 ± 0.0325 | 0/216 | 139/216 (64.4%) |
| static_alignment | 2.5852 ± 0.0513 | 2.4256 ± 0.0303 | 0/216 | 139/216 (64.4%) |
| tide | 2.5862 ± 0.0520 | 2.4275 ± 0.0314 | 0/216 | 135/216 (62.5%) |

Overall, v3 produced 0/864 exact matches and 564/864 valid UTF-8 outputs. Its report did not measure semantic action fidelity or preservation.

## v4.1 development evaluation

The v4.1 fresh synthetic corpus contained 800 records in 20 families. All 12 fixed runs were completed before the holdout was opened. The old pooled-vector decoder produced zero accepted-reference matches across the 2,592 generated outputs, zero semantic preservation passes, action fidelity below the frozen thresholds, and unreliable Vietnamese Unicode. These results motivated a model iteration; v4.1's opened holdout was not reused for tuning.

## v4.2 cross-attention evaluation

The full aggregate report is preserved in [VI_EN_RESULTS_V4.2.md](VI_EN_RESULTS_V4.2.md). It records the 12-run table and per-language/action buckets: 0/2,592 accepted-reference matches, 0 preservation passes, and 2,592/2,592 valid Unicode and EOS-terminated outputs. The frozen gate failed.

## Current result

The newer v4.2 experiment uses a fresh corpus and holdout, a source-memory cross-attention decoder and UTF-8-constrained decoding. The complete aggregate results and frozen quality-gate status are in [VI_EN_RESULTS.md](VI_EN_RESULTS.md). v4.2 also failed its preregistered generation quality gate; its negative result is preserved and must not be tuned against.
