# vi-en-ai-v4.17 Vi–En validation results

AI-authored and independently AI-reviewed preliminary synthetic pilot. **Not human/native-speaker validated.** PhoMT was not used. Phan Rang Cham remains excluded.

## Frozen protocol

The corpus has 15360 records and 192 event combinations. Split groups: 112/40/40; records: 8960/3200/3200 (train/validation/release holdout). Data split policy: 112 train, 40 validation, 40 release-holdout combinations from three fresh agent factors; every held-out factor pair is represented in training; English NOW uses present progressive; four context-balanced surface realizations per meaning state; fresh split and sealed holdout for a unique-transition row-exposure balance study. Train/validation paths apply negative polarity then past time; test paths reverse this order, so the sealed holdout also probes action-order recombination and is not a matched measure of the weighting contrast. Frozen release-holdout scope: Test paths reverse the action order used in train and validation (TIME:PAST then POLARITY:NEGATIVE); if opened after all validation gates pass, the holdout probes action-order recombination as well as held-out factor combinations and is not a matched estimate of the transition-weighting contrast. Transition weighting: There are 3072 duplicated path-step rows across the full split: 1792 in training, 640 in validation, and 640 in the sealed release holdout. Each logical path-step transition has one standalone single-edge record and one path-linked record. In training this adds 1792 record exposures, so those path-selected transitions contribute twice the row-wise token/edge exposure. Validation and holdout duplicates are evaluation records, not training exposure. The v4.17 protocol crosses uniform row weighting with a unique-transition condition assigning 0.5 weight to each standalone/path-linked representation in base per-edge losses; path-composition losses are unchanged. This is an aggregate weighting contrast, not removal of either record.

Objective conditions: tide with source-copy weight 1.5 and TIDE latent-objective multiplier 0.1; transition balance `row_uniform`; tide with source-copy weight 1.5 and TIDE latent-objective multiplier 0.1; transition balance `unique_transition`; token_only with source-copy weight 1.5; transition balance `row_uniform`; token_only with source-copy weight 1.5; transition balance `unique_transition`. Seeds 17, 23, 41; 29 epochs and 3248 updates/config; width 32, 4 heads, 1 layers. Checkpoints selected using the frozen validation criterion. Decoder: greedy byte-level UTF-8 constrained decoding; EOS only at complete codepoint boundaries.

The registered primary objective is `tide`. Frozen thresholds: valid Unicode 100%; single-action action fidelity and preservation each ≥90%; held-out-path action fidelity and preservation each ≥80%. Every configured primary weight, seed, and language/action bucket must meet all applicable thresholds.

## Validation result: **FAIL**

The release holdout was not evaluated and remains sealed.

| Mode | Source-copy weight | TIDE aux multiplier | Edge balance | Seed | Val token CE | Val path token CE | Updates | Training wall seconds | Mean examples/sec | Gate |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---|
| token_only | 1.5 | — | row_uniform | 17 | 0.3349 | 0.2539 | 3248 | 650.2 | 399.6 | control_only |
| token_only | 1.5 | — | unique_transition | 17 | 0.3113 | 0.2347 | 3248 | 651.7 | 398.7 | control_only |
| tide | 1.5 | 0.1 | row_uniform | 17 | 0.3108 | 0.2007 | 3248 | 731.7 | 355.1 | fail |
| tide | 1.5 | 0.1 | unique_transition | 17 | 0.2956 | 0.2031 | 3248 | 733.2 | 354.4 | fail |
| token_only | 1.5 | — | row_uniform | 23 | 0.2830 | 0.1720 | 3248 | 651.9 | 398.6 | control_only |
| token_only | 1.5 | — | unique_transition | 23 | 0.2592 | 0.1623 | 3248 | 651.0 | 399.2 | control_only |
| tide | 1.5 | 0.1 | row_uniform | 23 | 0.2638 | 0.1729 | 3248 | 734.0 | 354.0 | fail |
| tide | 1.5 | 0.1 | unique_transition | 23 | 0.2543 | 0.1617 | 3248 | 732.7 | 354.7 | fail |
| token_only | 1.5 | — | row_uniform | 41 | 0.2765 | 0.1756 | 3248 | 652.0 | 398.6 | control_only |
| token_only | 1.5 | — | unique_transition | 41 | 0.2632 | 0.1722 | 3248 | 655.6 | 396.4 | control_only |
| tide | 1.5 | 0.1 | row_uniform | 41 | 0.2603 | 0.1601 | 3248 | 642.0 | 425.5 | fail |
| tide | 1.5 | 0.1 | unique_transition | 41 | 0.2483 | 0.1691 | 3248 | 452.4 | 574.6 | fail |

## Validation generation by condition and bucket

Action fidelity and preservation are pooled across seeds within each condition and bucket; thresholds are still checked for every primary condition/seed/bucket. Exact-reference match and CER are synthetic-reference metrics, not human naturalness.

| Mode | Source-copy weight | TIDE aux multiplier | Edge balance | Bucket | Action fidelity | Preservation | Accepted references | CER | Unicode | EOS |
|---|---:|---:|---|---|---:|---:|---:|---:|---:|---:|---|
| tide | 1.5 | 0.1 | row_uniform | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 343/480 | 35/480 | 27/480 | 17.1% | 480/480 | 480/480 |
| tide | 1.5 | 0.1 | row_uniform | en/single/POLARITY:NEGATIVE | 456/960 | 21/960 | 12/960 | 21.7% | 960/960 | 960/960 |
| tide | 1.5 | 0.1 | row_uniform | en/single/POLARITY:POSITIVE | 563/960 | 2/960 | 1/960 | 28.6% | 960/960 | 960/960 |
| tide | 1.5 | 0.1 | row_uniform | en/single/TIME:NOW | 381/960 | 8/960 | 5/960 | 27.1% | 960/960 | 960/960 |
| tide | 1.5 | 0.1 | row_uniform | en/single/TIME:PAST | 553/960 | 24/960 | 16/960 | 23.5% | 960/960 | 960/960 |
| tide | 1.5 | 0.1 | row_uniform | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 268/480 | 9/480 | 4/480 | 25.1% | 480/480 | 480/480 |
| tide | 1.5 | 0.1 | row_uniform | vi/single/POLARITY:NEGATIVE | 266/960 | 10/960 | 2/960 | 28.7% | 960/960 | 960/960 |
| tide | 1.5 | 0.1 | row_uniform | vi/single/POLARITY:POSITIVE | 228/960 | 0/960 | 0/960 | 33.5% | 960/960 | 960/960 |
| tide | 1.5 | 0.1 | row_uniform | vi/single/TIME:NOW | 168/960 | 4/960 | 1/960 | 33.7% | 960/960 | 960/960 |
| tide | 1.5 | 0.1 | row_uniform | vi/single/TIME:PAST | 269/960 | 11/960 | 4/960 | 28.3% | 960/960 | 960/960 |
| tide | 1.5 | 0.1 | unique_transition | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 342/480 | 27/480 | 22/480 | 17.1% | 480/480 | 480/480 |
| tide | 1.5 | 0.1 | unique_transition | en/single/POLARITY:NEGATIVE | 366/960 | 15/960 | 7/960 | 24.1% | 960/960 | 960/960 |
| tide | 1.5 | 0.1 | unique_transition | en/single/POLARITY:POSITIVE | 602/960 | 5/960 | 2/960 | 27.3% | 960/960 | 960/960 |
| tide | 1.5 | 0.1 | unique_transition | en/single/TIME:NOW | 344/960 | 3/960 | 1/960 | 28.1% | 960/960 | 960/960 |
| tide | 1.5 | 0.1 | unique_transition | en/single/TIME:PAST | 538/960 | 22/960 | 15/960 | 23.5% | 960/960 | 960/960 |
| tide | 1.5 | 0.1 | unique_transition | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 279/480 | 5/480 | 1/480 | 24.2% | 480/480 | 480/480 |
| tide | 1.5 | 0.1 | unique_transition | vi/single/POLARITY:NEGATIVE | 317/960 | 7/960 | 3/960 | 28.2% | 960/960 | 960/960 |
| tide | 1.5 | 0.1 | unique_transition | vi/single/POLARITY:POSITIVE | 242/960 | 1/960 | 0/960 | 34.5% | 960/960 | 960/960 |
| tide | 1.5 | 0.1 | unique_transition | vi/single/TIME:NOW | 183/960 | 3/960 | 0/960 | 33.4% | 960/960 | 960/960 |
| tide | 1.5 | 0.1 | unique_transition | vi/single/TIME:PAST | 301/960 | 9/960 | 4/960 | 28.8% | 960/960 | 960/960 |
| token_only | 1.5 | — | row_uniform | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 327/480 | 20/480 | 16/480 | 17.2% | 480/480 | 480/480 |
| token_only | 1.5 | — | row_uniform | en/single/POLARITY:NEGATIVE | 432/960 | 15/960 | 14/960 | 22.6% | 960/960 | 960/960 |
| token_only | 1.5 | — | row_uniform | en/single/POLARITY:POSITIVE | 540/960 | 1/960 | 0/960 | 28.9% | 960/960 | 960/960 |
| token_only | 1.5 | — | row_uniform | en/single/TIME:NOW | 347/960 | 1/960 | 0/960 | 27.6% | 960/960 | 960/960 |
| token_only | 1.5 | — | row_uniform | en/single/TIME:PAST | 533/960 | 15/960 | 8/960 | 24.1% | 960/960 | 960/960 |
| token_only | 1.5 | — | row_uniform | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 275/480 | 6/480 | 2/480 | 26.0% | 480/480 | 480/480 |
| token_only | 1.5 | — | row_uniform | vi/single/POLARITY:NEGATIVE | 293/960 | 6/960 | 2/960 | 29.7% | 960/960 | 960/960 |
| token_only | 1.5 | — | row_uniform | vi/single/POLARITY:POSITIVE | 180/960 | 6/960 | 1/960 | 35.3% | 960/960 | 960/960 |
| token_only | 1.5 | — | row_uniform | vi/single/TIME:NOW | 134/960 | 6/960 | 1/960 | 36.7% | 960/960 | 960/960 |
| token_only | 1.5 | — | row_uniform | vi/single/TIME:PAST | 249/960 | 6/960 | 4/960 | 31.3% | 960/960 | 960/960 |
| token_only | 1.5 | — | unique_transition | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 301/480 | 18/480 | 15/480 | 18.5% | 480/480 | 480/480 |
| token_only | 1.5 | — | unique_transition | en/single/POLARITY:NEGATIVE | 410/960 | 20/960 | 9/960 | 23.2% | 960/960 | 960/960 |
| token_only | 1.5 | — | unique_transition | en/single/POLARITY:POSITIVE | 571/960 | 1/960 | 1/960 | 27.5% | 960/960 | 960/960 |
| token_only | 1.5 | — | unique_transition | en/single/TIME:NOW | 362/960 | 6/960 | 3/960 | 26.5% | 960/960 | 960/960 |
| token_only | 1.5 | — | unique_transition | en/single/TIME:PAST | 471/960 | 9/960 | 5/960 | 25.5% | 960/960 | 960/960 |
| token_only | 1.5 | — | unique_transition | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 266/480 | 8/480 | 4/480 | 24.7% | 480/480 | 480/480 |
| token_only | 1.5 | — | unique_transition | vi/single/POLARITY:NEGATIVE | 275/960 | 17/960 | 3/960 | 29.8% | 960/960 | 960/960 |
| token_only | 1.5 | — | unique_transition | vi/single/POLARITY:POSITIVE | 151/960 | 7/960 | 2/960 | 34.0% | 960/960 | 960/960 |
| token_only | 1.5 | — | unique_transition | vi/single/TIME:NOW | 106/960 | 10/960 | 1/960 | 35.8% | 960/960 | 960/960 |
| token_only | 1.5 | — | unique_transition | vi/single/TIME:PAST | 272/960 | 10/960 | 4/960 | 28.6% | 960/960 | 960/960 |

## Primary-mode validation diagnostics by seed

Counts below preserve the frozen seed-by-seed gate denominator. No generated or reference text is included.

| Source-copy weight | TIDE aux multiplier | Edge balance | Seed | Bucket | Action fidelity | Preservation | Accepted references | CER | Unicode | EOS | Failure reason | Bucket gate |
|---:|---:|---|---:|---|---:|---:|---:|---:|---:|---:|---|---|
| 1.5 | 0.1 | row_uniform | 17 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 116/160 | 10/160 | 6/160 | 15.7% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | row_uniform | 17 | en/single/POLARITY:NEGATIVE | 140/320 | 4/320 | 2/320 | 24.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | row_uniform | 17 | en/single/POLARITY:POSITIVE | 197/320 | 0/320 | 0/320 | 29.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | row_uniform | 17 | en/single/TIME:NOW | 110/320 | 1/320 | 1/320 | 30.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | row_uniform | 17 | en/single/TIME:PAST | 203/320 | 4/320 | 4/320 | 23.8% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | row_uniform | 17 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 75/160 | 2/160 | 0/160 | 26.6% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | row_uniform | 17 | vi/single/POLARITY:NEGATIVE | 63/320 | 0/320 | 0/320 | 29.8% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | row_uniform | 17 | vi/single/POLARITY:POSITIVE | 65/320 | 0/320 | 0/320 | 34.1% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | row_uniform | 17 | vi/single/TIME:NOW | 21/320 | 0/320 | 0/320 | 37.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | row_uniform | 17 | vi/single/TIME:PAST | 66/320 | 4/320 | 0/320 | 30.2% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | row_uniform | 23 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 110/160 | 9/160 | 9/160 | 16.7% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | row_uniform | 23 | en/single/POLARITY:NEGATIVE | 139/320 | 5/320 | 3/320 | 21.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | row_uniform | 23 | en/single/POLARITY:POSITIVE | 177/320 | 1/320 | 0/320 | 25.1% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | row_uniform | 23 | en/single/TIME:NOW | 148/320 | 4/320 | 2/320 | 23.9% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | row_uniform | 23 | en/single/TIME:PAST | 162/320 | 8/320 | 6/320 | 23.3% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | row_uniform | 23 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 93/160 | 5/160 | 2/160 | 21.9% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | row_uniform | 23 | vi/single/POLARITY:NEGATIVE | 83/320 | 5/320 | 1/320 | 28.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | row_uniform | 23 | vi/single/POLARITY:POSITIVE | 66/320 | 0/320 | 0/320 | 34.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | row_uniform | 23 | vi/single/TIME:NOW | 85/320 | 2/320 | 1/320 | 32.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | row_uniform | 23 | vi/single/TIME:PAST | 84/320 | 6/320 | 4/320 | 27.2% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | row_uniform | 41 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 117/160 | 16/160 | 12/160 | 18.9% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | row_uniform | 41 | en/single/POLARITY:NEGATIVE | 177/320 | 12/320 | 7/320 | 20.2% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | row_uniform | 41 | en/single/POLARITY:POSITIVE | 189/320 | 1/320 | 1/320 | 31.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | row_uniform | 41 | en/single/TIME:NOW | 123/320 | 3/320 | 2/320 | 26.7% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | row_uniform | 41 | en/single/TIME:PAST | 188/320 | 12/320 | 6/320 | 23.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | row_uniform | 41 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 100/160 | 2/160 | 2/160 | 26.9% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | row_uniform | 41 | vi/single/POLARITY:NEGATIVE | 120/320 | 5/320 | 1/320 | 28.3% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | row_uniform | 41 | vi/single/POLARITY:POSITIVE | 97/320 | 0/320 | 0/320 | 32.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | row_uniform | 41 | vi/single/TIME:NOW | 62/320 | 2/320 | 0/320 | 31.5% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | row_uniform | 41 | vi/single/TIME:PAST | 119/320 | 1/320 | 0/320 | 27.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 17 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 116/160 | 4/160 | 4/160 | 18.9% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 17 | en/single/POLARITY:NEGATIVE | 115/320 | 1/320 | 1/320 | 26.8% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 17 | en/single/POLARITY:POSITIVE | 173/320 | 0/320 | 0/320 | 29.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 17 | en/single/TIME:NOW | 118/320 | 1/320 | 0/320 | 30.1% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 17 | en/single/TIME:PAST | 176/320 | 8/320 | 5/320 | 23.5% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 17 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 58/160 | 2/160 | 0/160 | 28.1% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 17 | vi/single/POLARITY:NEGATIVE | 56/320 | 3/320 | 0/320 | 30.3% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 17 | vi/single/POLARITY:POSITIVE | 66/320 | 1/320 | 0/320 | 35.9% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 17 | vi/single/TIME:NOW | 35/320 | 2/320 | 0/320 | 36.3% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 17 | vi/single/TIME:PAST | 71/320 | 4/320 | 1/320 | 31.3% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 23 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 117/160 | 14/160 | 11/160 | 14.4% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 23 | en/single/POLARITY:NEGATIVE | 99/320 | 6/320 | 3/320 | 23.9% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 23 | en/single/POLARITY:POSITIVE | 232/320 | 4/320 | 1/320 | 23.5% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 23 | en/single/TIME:NOW | 117/320 | 2/320 | 1/320 | 26.1% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 23 | en/single/TIME:PAST | 181/320 | 6/320 | 5/320 | 23.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 23 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 107/160 | 3/160 | 1/160 | 19.8% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 23 | vi/single/POLARITY:NEGATIVE | 116/320 | 4/320 | 3/320 | 26.3% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 23 | vi/single/POLARITY:POSITIVE | 82/320 | 0/320 | 0/320 | 32.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 23 | vi/single/TIME:NOW | 86/320 | 0/320 | 0/320 | 30.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 23 | vi/single/TIME:PAST | 105/320 | 3/320 | 2/320 | 25.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 41 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 109/160 | 9/160 | 7/160 | 17.9% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 41 | en/single/POLARITY:NEGATIVE | 152/320 | 8/320 | 3/320 | 21.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 41 | en/single/POLARITY:POSITIVE | 197/320 | 1/320 | 1/320 | 29.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 41 | en/single/TIME:NOW | 109/320 | 0/320 | 0/320 | 28.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 41 | en/single/TIME:PAST | 181/320 | 8/320 | 5/320 | 23.9% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 41 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 114/160 | 0/160 | 0/160 | 24.7% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 41 | vi/single/POLARITY:NEGATIVE | 145/320 | 0/320 | 0/320 | 28.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 41 | vi/single/POLARITY:POSITIVE | 94/320 | 0/320 | 0/320 | 34.9% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 41 | vi/single/TIME:NOW | 62/320 | 1/320 | 0/320 | 33.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 41 | vi/single/TIME:PAST | 125/320 | 2/320 | 1/320 | 29.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |

## Limits and interpretation

Valid Unicode and EOS termination do not establish semantic correctness. The deterministic checker covers only the declared synthetic tense/polarity grammar and named roles. This benchmark tests recombination of familiar lexical factors; it does not establish naturalness, natural-corpus efficacy, or scientific efficacy. Control results are diagnostic; no TIDE advantage is claimed.

All examples and generated outputs remain private under Git-ignored `data/` and `runs/`. This report contains aggregate metrics only. `human_validated` is false. PhoMT raw/derived data and Phan Rang Cham data were not used.

Private aggregate evidence: `vi-en-ai-v4.17-r2/protocol.json`, validation generation metrics under `vi-en-ai-v4.17-r2`, and associated ignored run artifacts. Protocol SHA-256: `9aaca397ce2b7ec8e16419ad9d19fdf46fed4f2dc04ef1e59d86ac61ddbb35a6`.
