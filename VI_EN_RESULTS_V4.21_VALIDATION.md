# vi-en-ai-v4.21 Vi–En validation results

AI-authored and independently AI-reviewed preliminary synthetic pilot. **Not human/native-speaker validated.** PhoMT was not used. Phan Rang Cham remains excluded.

## Frozen protocol

The corpus has 15360 records and 192 event combinations. Split groups: 112/40/40; records: 8960/3200/3200 (train/validation/release holdout). Data split policy: 112 train, 40 validation, 40 release-holdout combinations from three fresh agent factors; every held-out factor pair is represented in training; English NOW uses present progressive; four context-balanced surface realizations per meaning state; action order matches across all splits; fresh split for a fixed-final-epoch 2x2 TIDE source-copy-weight (0/1.5) × decoder (vocabulary/source-pointer) factorial. Frozen release-holdout scope: The release holdout uses the same ordered action paths as train and validation; it probes fresh held-out factor combinations only and does not add an action-order shift.

Objective conditions: tide with source-copy weight 0 and TIDE latent-objective multiplier 1; transition balance `row_uniform`; decoder `source_pointer`; tide with source-copy weight 0 and TIDE latent-objective multiplier 1; transition balance `row_uniform`; decoder `vocabulary`; tide with source-copy weight 1.5 and TIDE latent-objective multiplier 1; transition balance `row_uniform`; decoder `source_pointer`; tide with source-copy weight 1.5 and TIDE latent-objective multiplier 1; transition balance `row_uniform`; decoder `vocabulary`. Seeds 17, 23, 41; 29 epochs and 3248 updates/config; width 32, 4 heads, 1 layers. The preregistered final epoch was evaluated (`fixed_final_epoch`); validation loss did not select the checkpoint. Decoder: greedy byte-level UTF-8 constrained decoding; EOS only at complete codepoint boundaries.

The registered primary objective is `tide`. Frozen thresholds: valid Unicode 100%; checker coverage 100%; single-action fidelity ≥90% and preservation ≥90%; path fidelity ≥80% and preservation ≥80%. Every configured primary condition, seed, and language/action bucket must meet all applicable thresholds.

## Validation result: **INVALID / FAIL-CLOSED — semantic checker coverage incomplete**

Semantic quality gates are not interpretable because one or more buckets lack complete checker coverage. The gate fails closed and the release holdout remains sealed; `0/0` is an unscored denominator, not a 0% model score. See checker-coverage counts below.

The release holdout was not evaluated and remains sealed.

| Mode | Source-copy weight | TIDE aux multiplier | Edge balance | Decoder | Seed | Train token CE | Val token CE | Val path token CE | Updates | Training wall seconds | Mean examples/sec | Gate |
|---|---:|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| tide | 0 | 1 | row_uniform | vocabulary | 17 | 0.2305 | 0.3497 | 0.2189 | 3248 | 1015.5 | 256.3 | fail |
| tide | 0 | 1 | row_uniform | source_pointer | 17 | 0.2262 | 0.3870 | 0.2255 | 3248 | 1223.5 | 212.5 | fail |
| tide | 1.5 | 1 | row_uniform | vocabulary | 17 | 0.1719 | 0.2893 | 0.2135 | 3248 | 1019.1 | 255.1 | fail |
| tide | 1.5 | 1 | row_uniform | source_pointer | 17 | 0.2134 | 0.3440 | 0.2509 | 3248 | 1242.9 | 209.3 | fail |
| tide | 0 | 1 | row_uniform | vocabulary | 23 | 0.2305 | 0.3603 | 0.2392 | 3248 | 1024.4 | 253.9 | fail |
| tide | 0 | 1 | row_uniform | source_pointer | 23 | 0.2009 | 0.3611 | 0.2124 | 3248 | 1257.8 | 206.8 | fail |
| tide | 1.5 | 1 | row_uniform | vocabulary | 23 | 0.1655 | 0.2762 | 0.1952 | 3248 | 1010.6 | 257.4 | fail |
| tide | 1.5 | 1 | row_uniform | source_pointer | 23 | 0.1739 | 0.3045 | 0.2075 | 3248 | 1245.2 | 209.0 | fail |
| tide | 0 | 1 | row_uniform | vocabulary | 41 | 0.2119 | 0.3435 | 0.2061 | 3248 | 1028.6 | 253.0 | fail |
| tide | 0 | 1 | row_uniform | source_pointer | 41 | 0.2237 | 0.3864 | 0.2104 | 3248 | 1169.3 | 224.5 | fail |
| tide | 1.5 | 1 | row_uniform | vocabulary | 41 | 0.1630 | 0.2827 | 0.1913 | 3248 | 982.4 | 265.4 | fail |
| tide | 1.5 | 1 | row_uniform | source_pointer | 41 | 0.1965 | 0.3323 | 0.2178 | 3248 | 1084.6 | 245.0 | fail |

## Validation generation by condition and bucket

Action fidelity and preservation are pooled across seeds within each condition and bucket; thresholds are still checked for every primary condition/seed/bucket. Exact-reference match and CER are synthetic-reference metrics, not human naturalness.

| Mode | Source-copy weight | TIDE aux multiplier | Edge balance | Decoder | Bucket | Checker coverage | Action fidelity | Preservation | Accepted references | CER | Nonempty | Unicode | EOS |
|---|---:|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| tide | 0 | 1 | row_uniform | source_pointer | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/480 | 0/0 | 0/0 | 18/480 | 21.7% | 480/480 | 480/480 | 480/480 |
| tide | 0 | 1 | row_uniform | source_pointer | en/single/POLARITY:NEGATIVE | 0/960 | 0/0 | 0/0 | 3/960 | 29.9% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 1 | row_uniform | source_pointer | en/single/POLARITY:POSITIVE | 0/960 | 0/0 | 0/0 | 0/960 | 36.9% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 1 | row_uniform | source_pointer | en/single/TIME:NOW | 0/960 | 0/0 | 0/0 | 1/960 | 36.7% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 1 | row_uniform | source_pointer | en/single/TIME:PAST | 0/960 | 0/0 | 0/0 | 6/960 | 29.2% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 1 | row_uniform | source_pointer | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/480 | 0/0 | 0/0 | 16/480 | 24.6% | 480/480 | 480/480 | 480/480 |
| tide | 0 | 1 | row_uniform | source_pointer | vi/single/POLARITY:NEGATIVE | 0/960 | 0/0 | 0/0 | 6/960 | 29.2% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 1 | row_uniform | source_pointer | vi/single/POLARITY:POSITIVE | 0/960 | 0/0 | 0/0 | 4/960 | 34.3% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 1 | row_uniform | source_pointer | vi/single/TIME:NOW | 0/960 | 0/0 | 0/0 | 2/960 | 35.0% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 1 | row_uniform | source_pointer | vi/single/TIME:PAST | 0/960 | 0/0 | 0/0 | 6/960 | 28.9% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 1 | row_uniform | vocabulary | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/480 | 0/0 | 0/0 | 4/480 | 19.3% | 480/480 | 480/480 | 480/480 |
| tide | 0 | 1 | row_uniform | vocabulary | en/single/POLARITY:NEGATIVE | 0/960 | 0/0 | 0/0 | 0/960 | 26.4% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 1 | row_uniform | vocabulary | en/single/POLARITY:POSITIVE | 0/960 | 0/0 | 0/0 | 0/960 | 34.7% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 1 | row_uniform | vocabulary | en/single/TIME:NOW | 0/960 | 0/0 | 0/0 | 0/960 | 31.8% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 1 | row_uniform | vocabulary | en/single/TIME:PAST | 0/960 | 0/0 | 0/0 | 1/960 | 25.5% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 1 | row_uniform | vocabulary | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/480 | 0/0 | 0/0 | 6/480 | 24.3% | 480/480 | 480/480 | 480/480 |
| tide | 0 | 1 | row_uniform | vocabulary | vi/single/POLARITY:NEGATIVE | 0/960 | 0/0 | 0/0 | 1/960 | 31.6% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 1 | row_uniform | vocabulary | vi/single/POLARITY:POSITIVE | 0/960 | 0/0 | 0/0 | 0/960 | 37.2% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 1 | row_uniform | vocabulary | vi/single/TIME:NOW | 0/960 | 0/0 | 0/0 | 0/960 | 37.1% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 1 | row_uniform | vocabulary | vi/single/TIME:PAST | 0/960 | 0/0 | 0/0 | 3/960 | 30.1% | 960/960 | 960/960 | 960/960 |
| tide | 1.5 | 1 | row_uniform | source_pointer | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/480 | 0/0 | 0/0 | 12/480 | 24.4% | 480/480 | 480/480 | 480/480 |
| tide | 1.5 | 1 | row_uniform | source_pointer | en/single/POLARITY:NEGATIVE | 0/960 | 0/0 | 0/0 | 3/960 | 29.4% | 960/960 | 960/960 | 960/960 |
| tide | 1.5 | 1 | row_uniform | source_pointer | en/single/POLARITY:POSITIVE | 0/960 | 0/0 | 0/0 | 0/960 | 35.5% | 960/960 | 960/960 | 960/960 |
| tide | 1.5 | 1 | row_uniform | source_pointer | en/single/TIME:NOW | 0/960 | 0/0 | 0/0 | 2/960 | 38.7% | 960/960 | 960/960 | 960/960 |
| tide | 1.5 | 1 | row_uniform | source_pointer | en/single/TIME:PAST | 0/960 | 0/0 | 0/0 | 3/960 | 30.6% | 960/960 | 960/960 | 960/960 |
| tide | 1.5 | 1 | row_uniform | source_pointer | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/480 | 0/0 | 0/0 | 22/480 | 23.0% | 480/480 | 480/480 | 480/480 |
| tide | 1.5 | 1 | row_uniform | source_pointer | vi/single/POLARITY:NEGATIVE | 0/960 | 0/0 | 0/0 | 24/960 | 24.5% | 960/960 | 960/960 | 960/960 |
| tide | 1.5 | 1 | row_uniform | source_pointer | vi/single/POLARITY:POSITIVE | 0/960 | 0/0 | 0/0 | 3/960 | 30.9% | 960/960 | 960/960 | 960/960 |
| tide | 1.5 | 1 | row_uniform | source_pointer | vi/single/TIME:NOW | 0/960 | 0/0 | 0/0 | 5/960 | 32.0% | 960/960 | 960/960 | 960/960 |
| tide | 1.5 | 1 | row_uniform | source_pointer | vi/single/TIME:PAST | 0/960 | 0/0 | 0/0 | 20/960 | 26.2% | 960/960 | 960/960 | 960/960 |
| tide | 1.5 | 1 | row_uniform | vocabulary | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/480 | 0/0 | 0/0 | 10/480 | 21.2% | 480/480 | 480/480 | 480/480 |
| tide | 1.5 | 1 | row_uniform | vocabulary | en/single/POLARITY:NEGATIVE | 0/960 | 0/0 | 0/0 | 4/960 | 24.4% | 960/960 | 960/960 | 960/960 |
| tide | 1.5 | 1 | row_uniform | vocabulary | en/single/POLARITY:POSITIVE | 0/960 | 0/0 | 0/0 | 0/960 | 29.3% | 960/960 | 960/960 | 960/960 |
| tide | 1.5 | 1 | row_uniform | vocabulary | en/single/TIME:NOW | 0/960 | 0/0 | 0/0 | 0/960 | 30.1% | 960/960 | 960/960 | 960/960 |
| tide | 1.5 | 1 | row_uniform | vocabulary | en/single/TIME:PAST | 0/960 | 0/0 | 0/0 | 4/960 | 25.5% | 960/960 | 960/960 | 960/960 |
| tide | 1.5 | 1 | row_uniform | vocabulary | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/480 | 0/0 | 0/0 | 17/480 | 25.9% | 480/480 | 480/480 | 480/480 |
| tide | 1.5 | 1 | row_uniform | vocabulary | vi/single/POLARITY:NEGATIVE | 0/960 | 0/0 | 0/0 | 17/960 | 28.6% | 960/960 | 960/960 | 960/960 |
| tide | 1.5 | 1 | row_uniform | vocabulary | vi/single/POLARITY:POSITIVE | 0/960 | 0/0 | 0/0 | 1/960 | 35.0% | 960/960 | 960/960 | 960/960 |
| tide | 1.5 | 1 | row_uniform | vocabulary | vi/single/TIME:NOW | 0/960 | 0/0 | 0/0 | 2/960 | 33.5% | 960/960 | 960/960 | 960/960 |
| tide | 1.5 | 1 | row_uniform | vocabulary | vi/single/TIME:PAST | 0/960 | 0/0 | 0/0 | 12/960 | 28.9% | 960/960 | 960/960 | 960/960 |

## Primary-mode validation diagnostics by seed

Counts below preserve the frozen seed-by-seed gate denominator. No generated or reference text is included.

| Source-copy weight | TIDE aux multiplier | Edge balance | Decoder | Seed | Bucket | Checker coverage | Action fidelity | Preservation | Accepted references | CER | Unicode | EOS | Failure reason | Bucket gate |
|---:|---:|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| 0 | 1 | row_uniform | source_pointer | 17 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/160 | 0/0 | 0/0 | 1/160 | 20.3% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | source_pointer | 17 | en/single/POLARITY:NEGATIVE | 0/320 | 0/0 | 0/0 | 0/320 | 31.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | source_pointer | 17 | en/single/POLARITY:POSITIVE | 0/320 | 0/0 | 0/0 | 0/320 | 37.5% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | source_pointer | 17 | en/single/TIME:NOW | 0/320 | 0/0 | 0/0 | 0/320 | 40.9% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | source_pointer | 17 | en/single/TIME:PAST | 0/320 | 0/0 | 0/0 | 0/320 | 26.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | source_pointer | 17 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/160 | 0/0 | 0/0 | 5/160 | 21.9% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | source_pointer | 17 | vi/single/POLARITY:NEGATIVE | 0/320 | 0/0 | 0/0 | 3/320 | 25.2% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | source_pointer | 17 | vi/single/POLARITY:POSITIVE | 0/320 | 0/0 | 0/0 | 1/320 | 35.2% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | source_pointer | 17 | vi/single/TIME:NOW | 0/320 | 0/0 | 0/0 | 0/320 | 32.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | source_pointer | 17 | vi/single/TIME:PAST | 0/320 | 0/0 | 0/0 | 0/320 | 27.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | source_pointer | 23 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/160 | 0/0 | 0/0 | 10/160 | 22.2% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | source_pointer | 23 | en/single/POLARITY:NEGATIVE | 0/320 | 0/0 | 0/0 | 1/320 | 28.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | source_pointer | 23 | en/single/POLARITY:POSITIVE | 0/320 | 0/0 | 0/0 | 0/320 | 33.2% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | source_pointer | 23 | en/single/TIME:NOW | 0/320 | 0/0 | 0/0 | 1/320 | 32.2% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | source_pointer | 23 | en/single/TIME:PAST | 0/320 | 0/0 | 0/0 | 5/320 | 27.9% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | source_pointer | 23 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/160 | 0/0 | 0/0 | 5/160 | 25.9% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | source_pointer | 23 | vi/single/POLARITY:NEGATIVE | 0/320 | 0/0 | 0/0 | 2/320 | 31.1% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | source_pointer | 23 | vi/single/POLARITY:POSITIVE | 0/320 | 0/0 | 0/0 | 2/320 | 28.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | source_pointer | 23 | vi/single/TIME:NOW | 0/320 | 0/0 | 0/0 | 1/320 | 33.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | source_pointer | 23 | vi/single/TIME:PAST | 0/320 | 0/0 | 0/0 | 3/320 | 28.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | source_pointer | 41 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/160 | 0/0 | 0/0 | 7/160 | 22.6% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | source_pointer | 41 | en/single/POLARITY:NEGATIVE | 0/320 | 0/0 | 0/0 | 2/320 | 30.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | source_pointer | 41 | en/single/POLARITY:POSITIVE | 0/320 | 0/0 | 0/0 | 0/320 | 39.9% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | source_pointer | 41 | en/single/TIME:NOW | 0/320 | 0/0 | 0/0 | 0/320 | 37.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | source_pointer | 41 | en/single/TIME:PAST | 0/320 | 0/0 | 0/0 | 1/320 | 33.2% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | source_pointer | 41 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/160 | 0/0 | 0/0 | 6/160 | 26.0% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | source_pointer | 41 | vi/single/POLARITY:NEGATIVE | 0/320 | 0/0 | 0/0 | 1/320 | 31.3% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | source_pointer | 41 | vi/single/POLARITY:POSITIVE | 0/320 | 0/0 | 0/0 | 1/320 | 39.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | source_pointer | 41 | vi/single/TIME:NOW | 0/320 | 0/0 | 0/0 | 1/320 | 39.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | source_pointer | 41 | vi/single/TIME:PAST | 0/320 | 0/0 | 0/0 | 3/320 | 30.8% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | vocabulary | 17 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/160 | 0/0 | 0/0 | 0/160 | 18.5% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | vocabulary | 17 | en/single/POLARITY:NEGATIVE | 0/320 | 0/0 | 0/0 | 0/320 | 25.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | vocabulary | 17 | en/single/POLARITY:POSITIVE | 0/320 | 0/0 | 0/0 | 0/320 | 34.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | vocabulary | 17 | en/single/TIME:NOW | 0/320 | 0/0 | 0/0 | 0/320 | 32.5% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | vocabulary | 17 | en/single/TIME:PAST | 0/320 | 0/0 | 0/0 | 0/320 | 25.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | vocabulary | 17 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/160 | 0/0 | 0/0 | 3/160 | 21.8% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | vocabulary | 17 | vi/single/POLARITY:NEGATIVE | 0/320 | 0/0 | 0/0 | 1/320 | 30.3% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | vocabulary | 17 | vi/single/POLARITY:POSITIVE | 0/320 | 0/0 | 0/0 | 0/320 | 38.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | vocabulary | 17 | vi/single/TIME:NOW | 0/320 | 0/0 | 0/0 | 0/320 | 37.3% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | vocabulary | 17 | vi/single/TIME:PAST | 0/320 | 0/0 | 0/0 | 1/320 | 28.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | vocabulary | 23 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/160 | 0/0 | 0/0 | 2/160 | 18.2% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | vocabulary | 23 | en/single/POLARITY:NEGATIVE | 0/320 | 0/0 | 0/0 | 0/320 | 25.9% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | vocabulary | 23 | en/single/POLARITY:POSITIVE | 0/320 | 0/0 | 0/0 | 0/320 | 34.3% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | vocabulary | 23 | en/single/TIME:NOW | 0/320 | 0/0 | 0/0 | 0/320 | 30.7% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | vocabulary | 23 | en/single/TIME:PAST | 0/320 | 0/0 | 0/0 | 1/320 | 24.8% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | vocabulary | 23 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/160 | 0/0 | 0/0 | 0/160 | 27.1% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | vocabulary | 23 | vi/single/POLARITY:NEGATIVE | 0/320 | 0/0 | 0/0 | 0/320 | 35.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | vocabulary | 23 | vi/single/POLARITY:POSITIVE | 0/320 | 0/0 | 0/0 | 0/320 | 38.1% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | vocabulary | 23 | vi/single/TIME:NOW | 0/320 | 0/0 | 0/0 | 0/320 | 39.7% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | vocabulary | 23 | vi/single/TIME:PAST | 0/320 | 0/0 | 0/0 | 0/320 | 31.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | vocabulary | 41 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/160 | 0/0 | 0/0 | 2/160 | 21.3% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | vocabulary | 41 | en/single/POLARITY:NEGATIVE | 0/320 | 0/0 | 0/0 | 0/320 | 27.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | vocabulary | 41 | en/single/POLARITY:POSITIVE | 0/320 | 0/0 | 0/0 | 0/320 | 35.2% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | vocabulary | 41 | en/single/TIME:NOW | 0/320 | 0/0 | 0/0 | 0/320 | 32.1% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | vocabulary | 41 | en/single/TIME:PAST | 0/320 | 0/0 | 0/0 | 0/320 | 26.2% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | vocabulary | 41 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/160 | 0/0 | 0/0 | 3/160 | 24.0% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | vocabulary | 41 | vi/single/POLARITY:NEGATIVE | 0/320 | 0/0 | 0/0 | 0/320 | 29.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | vocabulary | 41 | vi/single/POLARITY:POSITIVE | 0/320 | 0/0 | 0/0 | 0/320 | 35.3% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | vocabulary | 41 | vi/single/TIME:NOW | 0/320 | 0/0 | 0/0 | 0/320 | 34.2% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 0 | 1 | row_uniform | vocabulary | 41 | vi/single/TIME:PAST | 0/320 | 0/0 | 0/0 | 2/320 | 30.2% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | source_pointer | 17 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/160 | 0/0 | 0/0 | 2/160 | 25.2% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | source_pointer | 17 | en/single/POLARITY:NEGATIVE | 0/320 | 0/0 | 0/0 | 0/320 | 31.2% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | source_pointer | 17 | en/single/POLARITY:POSITIVE | 0/320 | 0/0 | 0/0 | 0/320 | 34.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | source_pointer | 17 | en/single/TIME:NOW | 0/320 | 0/0 | 0/0 | 0/320 | 40.9% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | source_pointer | 17 | en/single/TIME:PAST | 0/320 | 0/0 | 0/0 | 0/320 | 29.3% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | source_pointer | 17 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/160 | 0/0 | 0/0 | 2/160 | 22.8% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | source_pointer | 17 | vi/single/POLARITY:NEGATIVE | 0/320 | 0/0 | 0/0 | 3/320 | 25.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | source_pointer | 17 | vi/single/POLARITY:POSITIVE | 0/320 | 0/0 | 0/0 | 1/320 | 33.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | source_pointer | 17 | vi/single/TIME:NOW | 0/320 | 0/0 | 0/0 | 0/320 | 35.1% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | source_pointer | 17 | vi/single/TIME:PAST | 0/320 | 0/0 | 0/0 | 4/320 | 27.2% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | source_pointer | 23 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/160 | 0/0 | 0/0 | 4/160 | 23.4% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | source_pointer | 23 | en/single/POLARITY:NEGATIVE | 0/320 | 0/0 | 0/0 | 0/320 | 27.2% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | source_pointer | 23 | en/single/POLARITY:POSITIVE | 0/320 | 0/0 | 0/0 | 0/320 | 31.2% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | source_pointer | 23 | en/single/TIME:NOW | 0/320 | 0/0 | 0/0 | 0/320 | 36.8% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | source_pointer | 23 | en/single/TIME:PAST | 0/320 | 0/0 | 0/0 | 0/320 | 29.2% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | source_pointer | 23 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/160 | 0/0 | 0/0 | 15/160 | 18.8% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | source_pointer | 23 | vi/single/POLARITY:NEGATIVE | 0/320 | 0/0 | 0/0 | 16/320 | 19.3% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | source_pointer | 23 | vi/single/POLARITY:POSITIVE | 0/320 | 0/0 | 0/0 | 1/320 | 26.9% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | source_pointer | 23 | vi/single/TIME:NOW | 0/320 | 0/0 | 0/0 | 5/320 | 27.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | source_pointer | 23 | vi/single/TIME:PAST | 0/320 | 0/0 | 0/0 | 12/320 | 23.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | source_pointer | 41 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/160 | 0/0 | 0/0 | 6/160 | 24.6% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | source_pointer | 41 | en/single/POLARITY:NEGATIVE | 0/320 | 0/0 | 0/0 | 3/320 | 29.9% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | source_pointer | 41 | en/single/POLARITY:POSITIVE | 0/320 | 0/0 | 0/0 | 0/320 | 40.8% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | source_pointer | 41 | en/single/TIME:NOW | 0/320 | 0/0 | 0/0 | 2/320 | 38.5% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | source_pointer | 41 | en/single/TIME:PAST | 0/320 | 0/0 | 0/0 | 3/320 | 33.2% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | source_pointer | 41 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/160 | 0/0 | 0/0 | 5/160 | 27.5% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | source_pointer | 41 | vi/single/POLARITY:NEGATIVE | 0/320 | 0/0 | 0/0 | 5/320 | 28.7% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | source_pointer | 41 | vi/single/POLARITY:POSITIVE | 0/320 | 0/0 | 0/0 | 1/320 | 32.9% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | source_pointer | 41 | vi/single/TIME:NOW | 0/320 | 0/0 | 0/0 | 0/320 | 33.3% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | source_pointer | 41 | vi/single/TIME:PAST | 0/320 | 0/0 | 0/0 | 4/320 | 27.9% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | vocabulary | 17 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/160 | 0/0 | 0/0 | 0/160 | 23.1% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | vocabulary | 17 | en/single/POLARITY:NEGATIVE | 0/320 | 0/0 | 0/0 | 1/320 | 24.3% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | vocabulary | 17 | en/single/POLARITY:POSITIVE | 0/320 | 0/0 | 0/0 | 0/320 | 28.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | vocabulary | 17 | en/single/TIME:NOW | 0/320 | 0/0 | 0/0 | 0/320 | 27.3% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | vocabulary | 17 | en/single/TIME:PAST | 0/320 | 0/0 | 0/0 | 0/320 | 24.8% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | vocabulary | 17 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/160 | 0/0 | 0/0 | 3/160 | 25.7% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | vocabulary | 17 | vi/single/POLARITY:NEGATIVE | 0/320 | 0/0 | 0/0 | 2/320 | 26.5% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | vocabulary | 17 | vi/single/POLARITY:POSITIVE | 0/320 | 0/0 | 0/0 | 0/320 | 33.5% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | vocabulary | 17 | vi/single/TIME:NOW | 0/320 | 0/0 | 0/0 | 1/320 | 33.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | vocabulary | 17 | vi/single/TIME:PAST | 0/320 | 0/0 | 0/0 | 2/320 | 28.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | vocabulary | 23 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/160 | 0/0 | 0/0 | 4/160 | 19.7% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | vocabulary | 23 | en/single/POLARITY:NEGATIVE | 0/320 | 0/0 | 0/0 | 1/320 | 24.2% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | vocabulary | 23 | en/single/POLARITY:POSITIVE | 0/320 | 0/0 | 0/0 | 0/320 | 30.1% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | vocabulary | 23 | en/single/TIME:NOW | 0/320 | 0/0 | 0/0 | 0/320 | 29.8% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | vocabulary | 23 | en/single/TIME:PAST | 0/320 | 0/0 | 0/0 | 0/320 | 25.9% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | vocabulary | 23 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/160 | 0/0 | 0/0 | 6/160 | 28.2% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | vocabulary | 23 | vi/single/POLARITY:NEGATIVE | 0/320 | 0/0 | 0/0 | 10/320 | 29.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | vocabulary | 23 | vi/single/POLARITY:POSITIVE | 0/320 | 0/0 | 0/0 | 1/320 | 33.9% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | vocabulary | 23 | vi/single/TIME:NOW | 0/320 | 0/0 | 0/0 | 0/320 | 33.3% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | vocabulary | 23 | vi/single/TIME:PAST | 0/320 | 0/0 | 0/0 | 8/320 | 29.3% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | vocabulary | 41 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/160 | 0/0 | 0/0 | 6/160 | 20.8% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | vocabulary | 41 | en/single/POLARITY:NEGATIVE | 0/320 | 0/0 | 0/0 | 2/320 | 24.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | vocabulary | 41 | en/single/POLARITY:POSITIVE | 0/320 | 0/0 | 0/0 | 0/320 | 29.2% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | vocabulary | 41 | en/single/TIME:NOW | 0/320 | 0/0 | 0/0 | 0/320 | 33.2% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | vocabulary | 41 | en/single/TIME:PAST | 0/320 | 0/0 | 0/0 | 4/320 | 25.7% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | vocabulary | 41 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/160 | 0/0 | 0/0 | 8/160 | 23.9% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | vocabulary | 41 | vi/single/POLARITY:NEGATIVE | 0/320 | 0/0 | 0/0 | 5/320 | 30.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | vocabulary | 41 | vi/single/POLARITY:POSITIVE | 0/320 | 0/0 | 0/0 | 0/320 | 37.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | vocabulary | 41 | vi/single/TIME:NOW | 0/320 | 0/0 | 0/0 | 1/320 | 34.3% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |
| 1.5 | 1 | row_uniform | vocabulary | 41 | vi/single/TIME:PAST | 0/320 | 0/0 | 0/0 | 2/320 | 29.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass, semantic_checker_coverage_pass, semantic_checker_coverage | fail |

## Limits and interpretation

Valid Unicode and EOS termination do not establish semantic correctness. The deterministic checker covers only the declared synthetic tense/polarity grammar and named roles. This benchmark tests recombination of familiar lexical factors; it does not establish naturalness, natural-corpus efficacy, or scientific efficacy. Control results are diagnostic; no TIDE advantage is claimed.

All examples and generated outputs remain private under Git-ignored `data/` and `runs/`. This report contains aggregate metrics only. `human_validated` is false. PhoMT raw/derived data and Phan Rang Cham data were not used.

Private aggregate evidence: `vi-en-ai-v4.21/protocol.json`, validation generation metrics under `vi-en-ai-v4.21`, and associated ignored run artifacts. Protocol SHA-256: `5b48e8348c2ef3fc1a4db9841c713560fd7bc24bbbd57a67691884f87e33d7de`.
