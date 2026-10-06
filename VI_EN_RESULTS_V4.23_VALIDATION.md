# vi-en-ai-v4.23 Vi–En validation results

AI-authored and independently AI-reviewed preliminary synthetic pilot. **Not human/native-speaker validated.** PhoMT was not used. Phan Rang Cham remains excluded.

## Frozen protocol

The corpus has 15360 records and 192 event combinations. Split groups: 112/40/40; records: 8960/3200/3200 (train/validation/release holdout). Data split policy: 112/40/40 event combinations from three fresh agents × eight verbs × eight patients; train agent marginals 37/37/38 and verb/patient marginals exactly 14 each; validation and release-holdout agent marginals 13/13/14 and verb/patient marginals 4–6; all held-out factor pairs occur in training; fixed split seed; English progressive NOW aligns with Vietnamese đang; search for / tìm kiếm replaces the achievement predicate; four context-balanced surface forms; same path order in all splits. Frozen release-holdout scope: The release holdout uses the same ordered action paths as train and validation; it probes fresh held-out factor combinations only and does not add an action-order shift. Transition weighting: There are 3072 duplicated path-step rows across the full split: 1792 in training, 640 in validation, and 640 in the sealed release holdout. Each logical path-step transition has one standalone single-edge record and one path-linked record. In training this adds 1792 record exposures, so those path-selected transitions contribute twice the row-wise token/edge exposure. Validation and holdout duplicates are evaluation records, not training exposure. The representation is fixed identically across conditions; results describe a path-enriched training distribution, not uniform weighting over unique transitions.

Objective conditions: tide with source-copy weight 0 and TIDE latent-objective multiplier 1; transition balance `row_uniform`; decoder `source_pointer`; tide with source-copy weight 0 and TIDE latent-objective multiplier 1; transition balance `row_uniform`; decoder `vocabulary`; tide with source-copy weight 1.5 and TIDE latent-objective multiplier 1; transition balance `row_uniform`; decoder `source_pointer`; tide with source-copy weight 1.5 and TIDE latent-objective multiplier 1; transition balance `row_uniform`; decoder `vocabulary`. Seeds 17, 23, 41; 29 epochs and 3248 updates/config; width 32, 4 heads, 1 layers. The preregistered final epoch was evaluated (`fixed_final_epoch`); validation loss did not select the checkpoint. Decoder: greedy byte-level UTF-8 constrained decoding; EOS only at complete codepoint boundaries.

The registered primary objective is `tide`. Frozen thresholds: valid Unicode 100%; checker coverage 100%; single-action fidelity ≥90% and preservation ≥90%; path fidelity ≥80% and preservation ≥80%. Every configured primary condition, seed, and language/action bucket must meet all applicable thresholds.

## Validation result: **FAIL**

Semantic checker coverage is complete across all primary buckets.

The release holdout was not evaluated and remains sealed.

| Mode | Source-copy weight | TIDE aux multiplier | Edge balance | Decoder | Seed | Train token CE | Val token CE | Val path token CE | Updates | Training wall seconds | Mean examples/sec | Gate |
|---|---:|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| tide | 0 | 1 | row_uniform | vocabulary | 17 | 0.1816 | 0.1893 | 0.0954 | 3248 | 1019.8 | 255.1 | fail |
| tide | 0 | 1 | row_uniform | source_pointer | 17 | 0.2003 | 0.2076 | 0.1025 | 3248 | 1248.3 | 208.3 | fail |
| tide | 1.5 | 1 | row_uniform | vocabulary | 17 | 0.1295 | 0.1366 | 0.0832 | 3248 | 1064.9 | 244.4 | fail |
| tide | 1.5 | 1 | row_uniform | source_pointer | 17 | 0.1733 | 0.1776 | 0.0967 | 3248 | 1274.3 | 204.1 | fail |
| tide | 0 | 1 | row_uniform | vocabulary | 23 | 0.2266 | 0.2302 | 0.1224 | 3248 | 1017.3 | 255.5 | fail |
| tide | 0 | 1 | row_uniform | source_pointer | 23 | 0.2423 | 0.2531 | 0.1271 | 3248 | 1275.1 | 203.9 | fail |
| tide | 1.5 | 1 | row_uniform | vocabulary | 23 | 0.1742 | 0.1779 | 0.1153 | 3248 | 1015.6 | 255.9 | fail |
| tide | 1.5 | 1 | row_uniform | source_pointer | 23 | 0.2105 | 0.2142 | 0.1239 | 3248 | 1261.0 | 206.3 | fail |
| tide | 0 | 1 | row_uniform | vocabulary | 41 | 0.2019 | 0.2162 | 0.1035 | 3248 | 1031.2 | 252.2 | fail |
| tide | 0 | 1 | row_uniform | source_pointer | 41 | 0.2030 | 0.2138 | 0.1050 | 3248 | 1190.1 | 220.4 | fail |
| tide | 1.5 | 1 | row_uniform | vocabulary | 41 | 0.1559 | 0.1762 | 0.1045 | 3248 | 1021.2 | 256.0 | fail |
| tide | 1.5 | 1 | row_uniform | source_pointer | 41 | 0.1661 | 0.1762 | 0.0951 | 3248 | 1120.9 | 237.8 | fail |

## Validation generation by condition and bucket

Action fidelity and preservation are pooled across seeds within each condition and bucket; thresholds are still checked for every primary condition/seed/bucket. Exact-reference match and CER are synthetic-reference metrics, not human naturalness.

| Mode | Source-copy weight | TIDE aux multiplier | Edge balance | Decoder | Bucket | Checker coverage | Action fidelity | Preservation | Accepted references | CER | Nonempty | Unicode | EOS |
|---|---:|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| tide | 0 | 1 | row_uniform | source_pointer | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 480/480 | 294/480 | 23/480 | 17/480 | 18.1% | 480/480 | 480/480 | 480/480 |
| tide | 0 | 1 | row_uniform | source_pointer | en/single/POLARITY:NEGATIVE | 960/960 | 362/960 | 6/960 | 1/960 | 27.0% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 1 | row_uniform | source_pointer | en/single/POLARITY:POSITIVE | 960/960 | 351/960 | 1/960 | 0/960 | 35.7% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 1 | row_uniform | source_pointer | en/single/TIME:NOW | 960/960 | 240/960 | 2/960 | 0/960 | 35.4% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 1 | row_uniform | source_pointer | en/single/TIME:PAST | 960/960 | 414/960 | 8/960 | 6/960 | 28.2% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 1 | row_uniform | source_pointer | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 480/480 | 417/480 | 222/480 | 186/480 | 6.7% | 480/480 | 480/480 | 480/480 |
| tide | 0 | 1 | row_uniform | source_pointer | vi/single/POLARITY:NEGATIVE | 960/960 | 556/960 | 248/960 | 137/960 | 13.8% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 1 | row_uniform | source_pointer | vi/single/POLARITY:POSITIVE | 960/960 | 360/960 | 103/960 | 43/960 | 18.9% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 1 | row_uniform | source_pointer | vi/single/TIME:NOW | 960/960 | 340/960 | 123/960 | 50/960 | 19.5% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 1 | row_uniform | source_pointer | vi/single/TIME:PAST | 960/960 | 477/960 | 179/960 | 128/960 | 13.4% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 1 | row_uniform | vocabulary | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 480/480 | 387/480 | 80/480 | 66/480 | 12.2% | 480/480 | 480/480 | 480/480 |
| tide | 0 | 1 | row_uniform | vocabulary | en/single/POLARITY:NEGATIVE | 960/960 | 503/960 | 47/960 | 30/960 | 20.6% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 1 | row_uniform | vocabulary | en/single/POLARITY:POSITIVE | 960/960 | 361/960 | 12/960 | 3/960 | 30.2% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 1 | row_uniform | vocabulary | en/single/TIME:NOW | 960/960 | 289/960 | 17/960 | 5/960 | 26.8% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 1 | row_uniform | vocabulary | en/single/TIME:PAST | 960/960 | 473/960 | 48/960 | 39/960 | 21.7% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 1 | row_uniform | vocabulary | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 480/480 | 396/480 | 99/480 | 85/480 | 13.1% | 480/480 | 480/480 | 480/480 |
| tide | 0 | 1 | row_uniform | vocabulary | vi/single/POLARITY:NEGATIVE | 960/960 | 463/960 | 110/960 | 40/960 | 19.8% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 1 | row_uniform | vocabulary | vi/single/POLARITY:POSITIVE | 960/960 | 229/960 | 15/960 | 4/960 | 26.4% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 1 | row_uniform | vocabulary | vi/single/TIME:NOW | 960/960 | 212/960 | 38/960 | 8/960 | 26.1% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 1 | row_uniform | vocabulary | vi/single/TIME:PAST | 960/960 | 409/960 | 69/960 | 59/960 | 19.5% | 960/960 | 960/960 | 960/960 |
| tide | 1.5 | 1 | row_uniform | source_pointer | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 480/480 | 209/480 | 40/480 | 14/480 | 17.0% | 480/480 | 480/480 | 480/480 |
| tide | 1.5 | 1 | row_uniform | source_pointer | en/single/POLARITY:NEGATIVE | 960/960 | 282/960 | 31/960 | 11/960 | 22.9% | 960/960 | 960/960 | 960/960 |
| tide | 1.5 | 1 | row_uniform | source_pointer | en/single/POLARITY:POSITIVE | 960/960 | 421/960 | 6/960 | 3/960 | 29.7% | 960/960 | 960/960 | 960/960 |
| tide | 1.5 | 1 | row_uniform | source_pointer | en/single/TIME:NOW | 960/960 | 210/960 | 7/960 | 2/960 | 31.2% | 960/960 | 960/960 | 960/960 |
| tide | 1.5 | 1 | row_uniform | source_pointer | en/single/TIME:PAST | 960/960 | 377/960 | 21/960 | 9/960 | 24.9% | 960/960 | 960/960 | 960/960 |
| tide | 1.5 | 1 | row_uniform | source_pointer | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 480/480 | 344/480 | 269/480 | 189/480 | 7.6% | 480/480 | 480/480 | 480/480 |
| tide | 1.5 | 1 | row_uniform | source_pointer | vi/single/POLARITY:NEGATIVE | 960/960 | 551/960 | 391/960 | 234/960 | 10.2% | 960/960 | 960/960 | 960/960 |
| tide | 1.5 | 1 | row_uniform | source_pointer | vi/single/POLARITY:POSITIVE | 960/960 | 342/960 | 187/960 | 103/960 | 15.0% | 960/960 | 960/960 | 960/960 |
| tide | 1.5 | 1 | row_uniform | source_pointer | vi/single/TIME:NOW | 960/960 | 132/960 | 283/960 | 41/960 | 17.9% | 960/960 | 960/960 | 960/960 |
| tide | 1.5 | 1 | row_uniform | source_pointer | vi/single/TIME:PAST | 960/960 | 423/960 | 295/960 | 177/960 | 12.5% | 960/960 | 960/960 | 960/960 |
| tide | 1.5 | 1 | row_uniform | vocabulary | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 480/480 | 381/480 | 72/480 | 67/480 | 13.5% | 480/480 | 480/480 | 480/480 |
| tide | 1.5 | 1 | row_uniform | vocabulary | en/single/POLARITY:NEGATIVE | 960/960 | 558/960 | 61/960 | 52/960 | 19.4% | 960/960 | 960/960 | 960/960 |
| tide | 1.5 | 1 | row_uniform | vocabulary | en/single/POLARITY:POSITIVE | 960/960 | 512/960 | 26/960 | 12/960 | 26.8% | 960/960 | 960/960 | 960/960 |
| tide | 1.5 | 1 | row_uniform | vocabulary | en/single/TIME:NOW | 960/960 | 342/960 | 39/960 | 22/960 | 25.8% | 960/960 | 960/960 | 960/960 |
| tide | 1.5 | 1 | row_uniform | vocabulary | en/single/TIME:PAST | 960/960 | 512/960 | 50/960 | 46/960 | 21.8% | 960/960 | 960/960 | 960/960 |
| tide | 1.5 | 1 | row_uniform | vocabulary | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 480/480 | 365/480 | 128/480 | 98/480 | 13.2% | 480/480 | 480/480 | 480/480 |
| tide | 1.5 | 1 | row_uniform | vocabulary | vi/single/POLARITY:NEGATIVE | 960/960 | 517/960 | 148/960 | 90/960 | 16.9% | 960/960 | 960/960 | 960/960 |
| tide | 1.5 | 1 | row_uniform | vocabulary | vi/single/POLARITY:POSITIVE | 960/960 | 137/960 | 24/960 | 14/960 | 23.7% | 960/960 | 960/960 | 960/960 |
| tide | 1.5 | 1 | row_uniform | vocabulary | vi/single/TIME:NOW | 960/960 | 239/960 | 117/960 | 54/960 | 21.5% | 960/960 | 960/960 | 960/960 |
| tide | 1.5 | 1 | row_uniform | vocabulary | vi/single/TIME:PAST | 960/960 | 376/960 | 125/960 | 85/960 | 18.2% | 960/960 | 960/960 | 960/960 |

## Primary-mode validation diagnostics by seed

Counts below preserve the frozen seed-by-seed gate denominator. No generated or reference text is included.

| Source-copy weight | TIDE aux multiplier | Edge balance | Decoder | Seed | Bucket | Checker coverage | Action fidelity | Preservation | Accepted references | CER | Unicode | EOS | Failure reason | Bucket gate |
|---:|---:|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| 0 | 1 | row_uniform | source_pointer | 17 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 95/160 | 4/160 | 4/160 | 21.6% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 0 | 1 | row_uniform | source_pointer | 17 | en/single/POLARITY:NEGATIVE | 320/320 | 129/320 | 1/320 | 0/320 | 27.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 1 | row_uniform | source_pointer | 17 | en/single/POLARITY:POSITIVE | 320/320 | 135/320 | 0/320 | 0/320 | 35.7% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 1 | row_uniform | source_pointer | 17 | en/single/TIME:NOW | 320/320 | 101/320 | 0/320 | 0/320 | 33.1% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 1 | row_uniform | source_pointer | 17 | en/single/TIME:PAST | 320/320 | 165/320 | 2/320 | 1/320 | 31.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 1 | row_uniform | source_pointer | 17 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 140/160 | 82/160 | 75/160 | 5.3% | 160/160 | 160/160 | preservation_pass | fail |
| 0 | 1 | row_uniform | source_pointer | 17 | vi/single/POLARITY:NEGATIVE | 320/320 | 215/320 | 90/320 | 59/320 | 10.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 1 | row_uniform | source_pointer | 17 | vi/single/POLARITY:POSITIVE | 320/320 | 173/320 | 61/320 | 32/320 | 13.8% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 1 | row_uniform | source_pointer | 17 | vi/single/TIME:NOW | 320/320 | 121/320 | 48/320 | 21/320 | 16.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 1 | row_uniform | source_pointer | 17 | vi/single/TIME:PAST | 320/320 | 197/320 | 78/320 | 65/320 | 11.9% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 1 | row_uniform | source_pointer | 23 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 117/160 | 17/160 | 13/160 | 14.6% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 0 | 1 | row_uniform | source_pointer | 23 | en/single/POLARITY:NEGATIVE | 320/320 | 135/320 | 1/320 | 1/320 | 26.1% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 1 | row_uniform | source_pointer | 23 | en/single/POLARITY:POSITIVE | 320/320 | 115/320 | 1/320 | 0/320 | 35.1% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 1 | row_uniform | source_pointer | 23 | en/single/TIME:NOW | 320/320 | 61/320 | 0/320 | 0/320 | 35.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 1 | row_uniform | source_pointer | 23 | en/single/TIME:PAST | 320/320 | 139/320 | 5/320 | 5/320 | 26.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 1 | row_uniform | source_pointer | 23 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 138/160 | 52/160 | 42/160 | 8.5% | 160/160 | 160/160 | preservation_pass | fail |
| 0 | 1 | row_uniform | source_pointer | 23 | vi/single/POLARITY:NEGATIVE | 320/320 | 153/320 | 66/320 | 25/320 | 15.2% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 1 | row_uniform | source_pointer | 23 | vi/single/POLARITY:POSITIVE | 320/320 | 74/320 | 10/320 | 1/320 | 22.7% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 1 | row_uniform | source_pointer | 23 | vi/single/TIME:NOW | 320/320 | 122/320 | 18/320 | 2/320 | 18.9% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 1 | row_uniform | source_pointer | 23 | vi/single/TIME:PAST | 320/320 | 118/320 | 28/320 | 16/320 | 16.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 1 | row_uniform | source_pointer | 41 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 82/160 | 2/160 | 0/160 | 18.0% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 0 | 1 | row_uniform | source_pointer | 41 | en/single/POLARITY:NEGATIVE | 320/320 | 98/320 | 4/320 | 0/320 | 27.9% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 1 | row_uniform | source_pointer | 41 | en/single/POLARITY:POSITIVE | 320/320 | 101/320 | 0/320 | 0/320 | 36.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 1 | row_uniform | source_pointer | 41 | en/single/TIME:NOW | 320/320 | 78/320 | 2/320 | 0/320 | 37.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 1 | row_uniform | source_pointer | 41 | en/single/TIME:PAST | 320/320 | 110/320 | 1/320 | 0/320 | 27.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 1 | row_uniform | source_pointer | 41 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 139/160 | 88/160 | 69/160 | 6.3% | 160/160 | 160/160 | preservation_pass | fail |
| 0 | 1 | row_uniform | source_pointer | 41 | vi/single/POLARITY:NEGATIVE | 320/320 | 188/320 | 92/320 | 53/320 | 15.9% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 1 | row_uniform | source_pointer | 41 | vi/single/POLARITY:POSITIVE | 320/320 | 113/320 | 32/320 | 10/320 | 20.3% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 1 | row_uniform | source_pointer | 41 | vi/single/TIME:NOW | 320/320 | 97/320 | 57/320 | 27/320 | 23.7% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 1 | row_uniform | source_pointer | 41 | vi/single/TIME:PAST | 320/320 | 162/320 | 73/320 | 47/320 | 11.9% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 1 | row_uniform | vocabulary | 17 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 128/160 | 23/160 | 19/160 | 13.2% | 160/160 | 160/160 | preservation_pass | fail |
| 0 | 1 | row_uniform | vocabulary | 17 | en/single/POLARITY:NEGATIVE | 320/320 | 187/320 | 22/320 | 16/320 | 19.7% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 1 | row_uniform | vocabulary | 17 | en/single/POLARITY:POSITIVE | 320/320 | 144/320 | 6/320 | 2/320 | 28.5% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 1 | row_uniform | vocabulary | 17 | en/single/TIME:NOW | 320/320 | 123/320 | 7/320 | 4/320 | 24.2% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 1 | row_uniform | vocabulary | 17 | en/single/TIME:PAST | 320/320 | 175/320 | 18/320 | 16/320 | 21.9% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 1 | row_uniform | vocabulary | 17 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 128/160 | 27/160 | 22/160 | 13.4% | 160/160 | 160/160 | preservation_pass | fail |
| 0 | 1 | row_uniform | vocabulary | 17 | vi/single/POLARITY:NEGATIVE | 320/320 | 146/320 | 35/320 | 18/320 | 20.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 1 | row_uniform | vocabulary | 17 | vi/single/POLARITY:POSITIVE | 320/320 | 104/320 | 12/320 | 3/320 | 25.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 1 | row_uniform | vocabulary | 17 | vi/single/TIME:NOW | 320/320 | 85/320 | 10/320 | 7/320 | 26.9% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 1 | row_uniform | vocabulary | 17 | vi/single/TIME:PAST | 320/320 | 142/320 | 19/320 | 17/320 | 20.5% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 1 | row_uniform | vocabulary | 23 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 124/160 | 20/160 | 16/160 | 13.2% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 0 | 1 | row_uniform | vocabulary | 23 | en/single/POLARITY:NEGATIVE | 320/320 | 159/320 | 8/320 | 2/320 | 20.9% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 1 | row_uniform | vocabulary | 23 | en/single/POLARITY:POSITIVE | 320/320 | 108/320 | 1/320 | 0/320 | 32.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 1 | row_uniform | vocabulary | 23 | en/single/TIME:NOW | 320/320 | 84/320 | 2/320 | 0/320 | 28.1% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 1 | row_uniform | vocabulary | 23 | en/single/TIME:PAST | 320/320 | 138/320 | 9/320 | 6/320 | 23.7% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 1 | row_uniform | vocabulary | 23 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 124/160 | 17/160 | 13/160 | 16.5% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 0 | 1 | row_uniform | vocabulary | 23 | vi/single/POLARITY:NEGATIVE | 320/320 | 176/320 | 18/320 | 5/320 | 21.7% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 1 | row_uniform | vocabulary | 23 | vi/single/POLARITY:POSITIVE | 320/320 | 82/320 | 0/320 | 0/320 | 29.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 1 | row_uniform | vocabulary | 23 | vi/single/TIME:NOW | 320/320 | 80/320 | 4/320 | 1/320 | 27.9% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 1 | row_uniform | vocabulary | 23 | vi/single/TIME:PAST | 320/320 | 123/320 | 10/320 | 9/320 | 22.7% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 1 | row_uniform | vocabulary | 41 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 135/160 | 37/160 | 31/160 | 10.2% | 160/160 | 160/160 | preservation_pass | fail |
| 0 | 1 | row_uniform | vocabulary | 41 | en/single/POLARITY:NEGATIVE | 320/320 | 157/320 | 17/320 | 12/320 | 21.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 1 | row_uniform | vocabulary | 41 | en/single/POLARITY:POSITIVE | 320/320 | 109/320 | 5/320 | 1/320 | 30.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 1 | row_uniform | vocabulary | 41 | en/single/TIME:NOW | 320/320 | 82/320 | 8/320 | 1/320 | 28.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 1 | row_uniform | vocabulary | 41 | en/single/TIME:PAST | 320/320 | 160/320 | 21/320 | 17/320 | 19.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 1 | row_uniform | vocabulary | 41 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 144/160 | 55/160 | 50/160 | 9.3% | 160/160 | 160/160 | preservation_pass | fail |
| 0 | 1 | row_uniform | vocabulary | 41 | vi/single/POLARITY:NEGATIVE | 320/320 | 141/320 | 57/320 | 17/320 | 17.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 1 | row_uniform | vocabulary | 41 | vi/single/POLARITY:POSITIVE | 320/320 | 43/320 | 3/320 | 1/320 | 24.7% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 1 | row_uniform | vocabulary | 41 | vi/single/TIME:NOW | 320/320 | 47/320 | 24/320 | 0/320 | 23.5% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 1 | row_uniform | vocabulary | 41 | vi/single/TIME:PAST | 320/320 | 144/320 | 40/320 | 33/320 | 15.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | source_pointer | 17 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 62/160 | 18/160 | 6/160 | 15.5% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | source_pointer | 17 | en/single/POLARITY:NEGATIVE | 320/320 | 79/320 | 17/320 | 6/320 | 21.1% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | source_pointer | 17 | en/single/POLARITY:POSITIVE | 320/320 | 124/320 | 1/320 | 1/320 | 29.5% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | source_pointer | 17 | en/single/TIME:NOW | 320/320 | 46/320 | 1/320 | 0/320 | 32.3% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | source_pointer | 17 | en/single/TIME:PAST | 320/320 | 94/320 | 13/320 | 5/320 | 24.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | source_pointer | 17 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 118/160 | 82/160 | 63/160 | 6.0% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | source_pointer | 17 | vi/single/POLARITY:NEGATIVE | 320/320 | 187/320 | 125/320 | 75/320 | 8.8% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | source_pointer | 17 | vi/single/POLARITY:POSITIVE | 320/320 | 146/320 | 78/320 | 52/320 | 12.2% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | source_pointer | 17 | vi/single/TIME:NOW | 320/320 | 69/320 | 96/320 | 19/320 | 15.1% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | source_pointer | 17 | vi/single/TIME:PAST | 320/320 | 182/320 | 103/320 | 73/320 | 10.1% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | source_pointer | 23 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 71/160 | 6/160 | 3/160 | 19.1% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | source_pointer | 23 | en/single/POLARITY:NEGATIVE | 320/320 | 100/320 | 10/320 | 2/320 | 25.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | source_pointer | 23 | en/single/POLARITY:POSITIVE | 320/320 | 150/320 | 3/320 | 0/320 | 30.3% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | source_pointer | 23 | en/single/TIME:NOW | 320/320 | 73/320 | 3/320 | 0/320 | 30.7% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | source_pointer | 23 | en/single/TIME:PAST | 320/320 | 150/320 | 6/320 | 3/320 | 26.1% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | source_pointer | 23 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 116/160 | 81/160 | 62/160 | 8.1% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | source_pointer | 23 | vi/single/POLARITY:NEGATIVE | 320/320 | 187/320 | 128/320 | 92/320 | 11.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | source_pointer | 23 | vi/single/POLARITY:POSITIVE | 320/320 | 96/320 | 60/320 | 31/320 | 16.7% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | source_pointer | 23 | vi/single/TIME:NOW | 320/320 | 29/320 | 76/320 | 10/320 | 19.8% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | source_pointer | 23 | vi/single/TIME:PAST | 320/320 | 125/320 | 82/320 | 47/320 | 13.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | source_pointer | 41 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 76/160 | 16/160 | 5/160 | 16.4% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | source_pointer | 41 | en/single/POLARITY:NEGATIVE | 320/320 | 103/320 | 4/320 | 3/320 | 22.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | source_pointer | 41 | en/single/POLARITY:POSITIVE | 320/320 | 147/320 | 2/320 | 2/320 | 29.2% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | source_pointer | 41 | en/single/TIME:NOW | 320/320 | 91/320 | 3/320 | 2/320 | 30.7% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | source_pointer | 41 | en/single/TIME:PAST | 320/320 | 133/320 | 2/320 | 1/320 | 23.8% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | source_pointer | 41 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 110/160 | 106/160 | 64/160 | 8.7% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | source_pointer | 41 | vi/single/POLARITY:NEGATIVE | 320/320 | 177/320 | 138/320 | 67/320 | 10.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | source_pointer | 41 | vi/single/POLARITY:POSITIVE | 320/320 | 100/320 | 49/320 | 20/320 | 16.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | source_pointer | 41 | vi/single/TIME:NOW | 320/320 | 34/320 | 111/320 | 12/320 | 18.9% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | source_pointer | 41 | vi/single/TIME:PAST | 320/320 | 116/320 | 110/320 | 57/320 | 14.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | vocabulary | 17 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 128/160 | 31/160 | 30/160 | 13.7% | 160/160 | 160/160 | preservation_pass | fail |
| 1.5 | 1 | row_uniform | vocabulary | 17 | en/single/POLARITY:NEGATIVE | 320/320 | 213/320 | 31/320 | 28/320 | 16.9% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | vocabulary | 17 | en/single/POLARITY:POSITIVE | 320/320 | 176/320 | 12/320 | 8/320 | 25.5% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | vocabulary | 17 | en/single/TIME:NOW | 320/320 | 168/320 | 24/320 | 18/320 | 20.7% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | vocabulary | 17 | en/single/TIME:PAST | 320/320 | 182/320 | 26/320 | 25/320 | 22.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | vocabulary | 17 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 132/160 | 72/160 | 58/160 | 9.4% | 160/160 | 160/160 | preservation_pass | fail |
| 1.5 | 1 | row_uniform | vocabulary | 17 | vi/single/POLARITY:NEGATIVE | 320/320 | 180/320 | 65/320 | 45/320 | 15.5% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | vocabulary | 17 | vi/single/POLARITY:POSITIVE | 320/320 | 55/320 | 9/320 | 7/320 | 22.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | vocabulary | 17 | vi/single/TIME:NOW | 320/320 | 118/320 | 53/320 | 36/320 | 18.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | vocabulary | 17 | vi/single/TIME:PAST | 320/320 | 121/320 | 61/320 | 42/320 | 15.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | vocabulary | 23 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 129/160 | 20/160 | 17/160 | 14.4% | 160/160 | 160/160 | preservation_pass | fail |
| 1.5 | 1 | row_uniform | vocabulary | 23 | en/single/POLARITY:NEGATIVE | 320/320 | 189/320 | 19/320 | 14/320 | 19.7% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | vocabulary | 23 | en/single/POLARITY:POSITIVE | 320/320 | 189/320 | 4/320 | 1/320 | 27.3% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | vocabulary | 23 | en/single/TIME:NOW | 320/320 | 84/320 | 6/320 | 0/320 | 27.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | vocabulary | 23 | en/single/TIME:PAST | 320/320 | 161/320 | 14/320 | 12/320 | 22.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | vocabulary | 23 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 107/160 | 31/160 | 20/160 | 15.9% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | vocabulary | 23 | vi/single/POLARITY:NEGATIVE | 320/320 | 193/320 | 39/320 | 22/320 | 17.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | vocabulary | 23 | vi/single/POLARITY:POSITIVE | 320/320 | 57/320 | 12/320 | 4/320 | 24.8% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | vocabulary | 23 | vi/single/TIME:NOW | 320/320 | 87/320 | 36/320 | 12/320 | 21.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | vocabulary | 23 | vi/single/TIME:PAST | 320/320 | 131/320 | 35/320 | 23/320 | 21.1% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | vocabulary | 41 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 124/160 | 21/160 | 20/160 | 12.4% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | vocabulary | 41 | en/single/POLARITY:NEGATIVE | 320/320 | 156/320 | 11/320 | 10/320 | 21.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | vocabulary | 41 | en/single/POLARITY:POSITIVE | 320/320 | 147/320 | 10/320 | 3/320 | 27.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | vocabulary | 41 | en/single/TIME:NOW | 320/320 | 90/320 | 9/320 | 4/320 | 29.5% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | vocabulary | 41 | en/single/TIME:PAST | 320/320 | 169/320 | 10/320 | 9/320 | 21.3% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | vocabulary | 41 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 126/160 | 25/160 | 20/160 | 14.5% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | vocabulary | 41 | vi/single/POLARITY:NEGATIVE | 320/320 | 144/320 | 44/320 | 23/320 | 18.2% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | vocabulary | 41 | vi/single/POLARITY:POSITIVE | 320/320 | 25/320 | 3/320 | 3/320 | 24.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | vocabulary | 41 | vi/single/TIME:NOW | 320/320 | 34/320 | 28/320 | 6/320 | 25.2% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 1 | row_uniform | vocabulary | 41 | vi/single/TIME:PAST | 320/320 | 124/320 | 29/320 | 20/320 | 17.9% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |

## Limits and interpretation

Valid Unicode and EOS termination do not establish semantic correctness. The deterministic checker covers only the declared synthetic tense/polarity grammar and named roles. This benchmark tests recombination of familiar lexical factors; it does not establish naturalness, natural-corpus efficacy, or scientific efficacy. Control results are diagnostic; no TIDE advantage is claimed.

All examples and generated outputs remain private under Git-ignored `data/` and `runs/`. This report contains aggregate metrics only. `human_validated` is false. PhoMT raw/derived data and Phan Rang Cham data were not used.

Private aggregate evidence: `vi-en-ai-v4.23/protocol.json`, validation generation metrics under `vi-en-ai-v4.23`, and associated ignored run artifacts. Protocol SHA-256: `0ad11b544e6884660484d0796b77de01f12335bb6afbc9344cd23a959c9fc14b`.
