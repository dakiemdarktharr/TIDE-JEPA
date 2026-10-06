# vi-en-ai-v4.20 Vi–En validation results

AI-authored and independently AI-reviewed preliminary synthetic pilot. **Not human/native-speaker validated.** PhoMT was not used. Phan Rang Cham remains excluded.

## Frozen protocol

The corpus has 15360 records and 192 event combinations. Split groups: 112/40/40; records: 8960/3200/3200 (train/validation/release holdout). Data split policy: 112 train, 40 validation, 40 release-holdout combinations from three fresh agent factors; every held-out factor pair is represented in training; English NOW uses present progressive; four context-balanced surface realizations per meaning state; action order matches across all splits; fresh split for a TIDE vocabulary-softmax versus source-pointer decoder comparison with fixed-final-epoch evaluation. Frozen release-holdout scope: The release holdout uses the same ordered action paths as train and validation; it probes fresh held-out factor combinations only and does not add an action-order shift.

Objective conditions: tide with source-copy weight 0 and TIDE latent-objective multiplier 0; transition balance `row_uniform`; decoder `vocabulary`; tide with source-copy weight 0 and TIDE latent-objective multiplier 0; transition balance `row_uniform`; decoder `source_pointer`. Seeds 17, 23, 41; 29 epochs and 3248 updates/config; width 32, 4 heads, 1 layers. The preregistered final epoch was evaluated (`fixed_final_epoch`); validation loss did not select the checkpoint. Decoder: greedy byte-level UTF-8 constrained decoding; EOS only at complete codepoint boundaries.

The registered primary objective is `tide`. Frozen thresholds: valid Unicode 100%; checker coverage 100%; single-action fidelity ≥90% and preservation ≥90%; path fidelity ≥80% and preservation ≥80%. Every configured primary condition, seed, and language/action bucket must meet all applicable thresholds.

## Validation result: **FAIL**

Semantic checker coverage is complete across all primary buckets.

The release holdout was not evaluated and remains sealed.

| Mode | Source-copy weight | TIDE aux multiplier | Edge balance | Decoder | Seed | Train token CE | Val token CE | Val path token CE | Updates | Training wall seconds | Mean examples/sec | Gate |
|---|---:|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| tide | 0 | 0 | row_uniform | vocabulary | 17 | 0.2087 | 0.3841 | 0.2401 | 3248 | 729.7 | 356.1 | fail |
| tide | 0 | 0 | row_uniform | source_pointer | 17 | 0.2424 | 0.4138 | 0.2259 | 3248 | 885.7 | 293.4 | fail |
| tide | 0 | 0 | row_uniform | vocabulary | 23 | 0.1915 | 0.3322 | 0.1910 | 3248 | 728.3 | 356.8 | fail |
| tide | 0 | 0 | row_uniform | source_pointer | 23 | 0.1996 | 0.3938 | 0.2259 | 3248 | 889.3 | 292.2 | fail |
| tide | 0 | 0 | row_uniform | vocabulary | 41 | 0.1749 | 0.3508 | 0.1871 | 3248 | 729.3 | 356.3 | fail |
| tide | 0 | 0 | row_uniform | source_pointer | 41 | 0.2275 | 0.4315 | 0.2455 | 3248 | 887.9 | 292.6 | fail |

## Validation generation by condition and bucket

Action fidelity and preservation are pooled across seeds within each condition and bucket; thresholds are still checked for every primary condition/seed/bucket. Exact-reference match and CER are synthetic-reference metrics, not human naturalness.

| Mode | Source-copy weight | TIDE aux multiplier | Edge balance | Decoder | Bucket | Checker coverage | Action fidelity | Preservation | Accepted references | CER | Nonempty | Unicode | EOS |
|---|---:|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| tide | 0 | 0 | row_uniform | vocabulary | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 480/480 | 354/480 | 13/480 | 10/480 | 18.9% | 480/480 | 480/480 | 480/480 |
| tide | 0 | 0 | row_uniform | vocabulary | en/single/POLARITY:NEGATIVE | 960/960 | 436/960 | 4/960 | 1/960 | 25.3% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | row_uniform | vocabulary | en/single/POLARITY:POSITIVE | 960/960 | 482/960 | 1/960 | 0/960 | 33.1% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | row_uniform | vocabulary | en/single/TIME:NOW | 960/960 | 339/960 | 0/960 | 0/960 | 31.3% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | row_uniform | vocabulary | en/single/TIME:PAST | 960/960 | 535/960 | 8/960 | 2/960 | 26.4% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | row_uniform | vocabulary | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 480/480 | 316/480 | 8/480 | 3/480 | 26.7% | 480/480 | 480/480 | 480/480 |
| tide | 0 | 0 | row_uniform | vocabulary | vi/single/POLARITY:NEGATIVE | 960/960 | 338/960 | 7/960 | 2/960 | 29.6% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | row_uniform | vocabulary | vi/single/POLARITY:POSITIVE | 960/960 | 246/960 | 0/960 | 0/960 | 36.9% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | row_uniform | vocabulary | vi/single/TIME:NOW | 960/960 | 286/960 | 4/960 | 2/960 | 34.8% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | row_uniform | vocabulary | vi/single/TIME:PAST | 960/960 | 350/960 | 4/960 | 2/960 | 30.1% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | row_uniform | source_pointer | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 480/480 | 317/480 | 12/480 | 6/480 | 19.6% | 480/480 | 480/480 | 480/480 |
| tide | 0 | 0 | row_uniform | source_pointer | en/single/POLARITY:NEGATIVE | 960/960 | 254/960 | 5/960 | 1/960 | 30.4% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | row_uniform | source_pointer | en/single/POLARITY:POSITIVE | 960/960 | 374/960 | 0/960 | 0/960 | 38.3% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | row_uniform | source_pointer | en/single/TIME:NOW | 960/960 | 184/960 | 0/960 | 0/960 | 38.2% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | row_uniform | source_pointer | en/single/TIME:PAST | 960/960 | 475/960 | 9/960 | 3/960 | 30.0% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | row_uniform | source_pointer | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 480/480 | 175/480 | 1/480 | 0/480 | 31.6% | 480/480 | 480/480 | 480/480 |
| tide | 0 | 0 | row_uniform | source_pointer | vi/single/POLARITY:NEGATIVE | 960/960 | 249/960 | 8/960 | 3/960 | 32.7% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | row_uniform | source_pointer | vi/single/POLARITY:POSITIVE | 960/960 | 305/960 | 1/960 | 0/960 | 35.5% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | row_uniform | source_pointer | vi/single/TIME:NOW | 960/960 | 262/960 | 1/960 | 1/960 | 37.0% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | row_uniform | source_pointer | vi/single/TIME:PAST | 960/960 | 214/960 | 2/960 | 2/960 | 35.7% | 960/960 | 960/960 | 960/960 |

## Primary-mode validation diagnostics by seed

Counts below preserve the frozen seed-by-seed gate denominator. No generated or reference text is included.

| Source-copy weight | TIDE aux multiplier | Edge balance | Decoder | Seed | Bucket | Checker coverage | Action fidelity | Preservation | Accepted references | CER | Unicode | EOS | Failure reason | Bucket gate |
|---:|---:|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| 0 | 0 | row_uniform | source_pointer | 17 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 117/160 | 2/160 | 0/160 | 18.1% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | source_pointer | 17 | en/single/POLARITY:NEGATIVE | 320/320 | 76/320 | 0/320 | 0/320 | 30.8% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | source_pointer | 17 | en/single/POLARITY:POSITIVE | 320/320 | 118/320 | 0/320 | 0/320 | 36.1% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | source_pointer | 17 | en/single/TIME:NOW | 320/320 | 46/320 | 0/320 | 0/320 | 40.1% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | source_pointer | 17 | en/single/TIME:PAST | 320/320 | 169/320 | 1/320 | 1/320 | 29.1% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | source_pointer | 17 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 52/160 | 0/160 | 0/160 | 27.6% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | source_pointer | 17 | vi/single/POLARITY:NEGATIVE | 320/320 | 94/320 | 3/320 | 1/320 | 28.5% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | source_pointer | 17 | vi/single/POLARITY:POSITIVE | 320/320 | 95/320 | 1/320 | 0/320 | 34.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | source_pointer | 17 | vi/single/TIME:NOW | 320/320 | 67/320 | 1/320 | 1/320 | 35.7% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | source_pointer | 17 | vi/single/TIME:PAST | 320/320 | 87/320 | 2/320 | 2/320 | 30.8% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | source_pointer | 23 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 105/160 | 5/160 | 2/160 | 20.2% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | source_pointer | 23 | en/single/POLARITY:NEGATIVE | 320/320 | 96/320 | 2/320 | 0/320 | 30.5% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | source_pointer | 23 | en/single/POLARITY:POSITIVE | 320/320 | 140/320 | 0/320 | 0/320 | 37.2% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | source_pointer | 23 | en/single/TIME:NOW | 320/320 | 76/320 | 0/320 | 0/320 | 35.1% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | source_pointer | 23 | en/single/TIME:PAST | 320/320 | 168/320 | 5/320 | 2/320 | 26.1% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | source_pointer | 23 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 64/160 | 0/160 | 0/160 | 31.5% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | source_pointer | 23 | vi/single/POLARITY:NEGATIVE | 320/320 | 91/320 | 4/320 | 2/320 | 30.1% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | source_pointer | 23 | vi/single/POLARITY:POSITIVE | 320/320 | 105/320 | 0/320 | 0/320 | 33.5% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | source_pointer | 23 | vi/single/TIME:NOW | 320/320 | 103/320 | 0/320 | 0/320 | 35.1% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | source_pointer | 23 | vi/single/TIME:PAST | 320/320 | 54/320 | 0/320 | 0/320 | 39.3% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | source_pointer | 41 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 95/160 | 5/160 | 4/160 | 20.4% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | source_pointer | 41 | en/single/POLARITY:NEGATIVE | 320/320 | 82/320 | 3/320 | 1/320 | 30.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | source_pointer | 41 | en/single/POLARITY:POSITIVE | 320/320 | 116/320 | 0/320 | 0/320 | 41.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | source_pointer | 41 | en/single/TIME:NOW | 320/320 | 62/320 | 0/320 | 0/320 | 39.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | source_pointer | 41 | en/single/TIME:PAST | 320/320 | 138/320 | 3/320 | 0/320 | 34.7% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | source_pointer | 41 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 59/160 | 1/160 | 0/160 | 35.6% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | source_pointer | 41 | vi/single/POLARITY:NEGATIVE | 320/320 | 64/320 | 1/320 | 0/320 | 39.3% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | source_pointer | 41 | vi/single/POLARITY:POSITIVE | 320/320 | 105/320 | 0/320 | 0/320 | 38.7% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | source_pointer | 41 | vi/single/TIME:NOW | 320/320 | 92/320 | 0/320 | 0/320 | 40.2% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | source_pointer | 41 | vi/single/TIME:PAST | 320/320 | 73/320 | 0/320 | 0/320 | 36.9% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | vocabulary | 17 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 115/160 | 1/160 | 0/160 | 20.6% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | vocabulary | 17 | en/single/POLARITY:NEGATIVE | 320/320 | 142/320 | 0/320 | 0/320 | 26.2% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | vocabulary | 17 | en/single/POLARITY:POSITIVE | 320/320 | 147/320 | 0/320 | 0/320 | 32.5% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | vocabulary | 17 | en/single/TIME:NOW | 320/320 | 87/320 | 0/320 | 0/320 | 32.8% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | vocabulary | 17 | en/single/TIME:PAST | 320/320 | 180/320 | 1/320 | 0/320 | 27.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | vocabulary | 17 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 92/160 | 3/160 | 0/160 | 31.7% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | vocabulary | 17 | vi/single/POLARITY:NEGATIVE | 320/320 | 107/320 | 2/320 | 0/320 | 31.3% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | vocabulary | 17 | vi/single/POLARITY:POSITIVE | 320/320 | 66/320 | 0/320 | 0/320 | 36.5% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | vocabulary | 17 | vi/single/TIME:NOW | 320/320 | 88/320 | 0/320 | 0/320 | 35.8% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | vocabulary | 17 | vi/single/TIME:PAST | 320/320 | 92/320 | 2/320 | 1/320 | 31.5% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | vocabulary | 23 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 133/160 | 9/160 | 8/160 | 17.1% | 160/160 | 160/160 | preservation_pass | fail |
| 0 | 0 | row_uniform | vocabulary | 23 | en/single/POLARITY:NEGATIVE | 320/320 | 139/320 | 3/320 | 1/320 | 24.8% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | vocabulary | 23 | en/single/POLARITY:POSITIVE | 320/320 | 174/320 | 1/320 | 0/320 | 31.8% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | vocabulary | 23 | en/single/TIME:NOW | 320/320 | 109/320 | 0/320 | 0/320 | 31.1% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | vocabulary | 23 | en/single/TIME:PAST | 320/320 | 172/320 | 2/320 | 0/320 | 25.3% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | vocabulary | 23 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 138/160 | 1/160 | 1/160 | 24.7% | 160/160 | 160/160 | preservation_pass | fail |
| 0 | 0 | row_uniform | vocabulary | 23 | vi/single/POLARITY:NEGATIVE | 320/320 | 148/320 | 3/320 | 2/320 | 29.2% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | vocabulary | 23 | vi/single/POLARITY:POSITIVE | 320/320 | 97/320 | 0/320 | 0/320 | 36.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | vocabulary | 23 | vi/single/TIME:NOW | 320/320 | 98/320 | 2/320 | 1/320 | 34.3% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | vocabulary | 23 | vi/single/TIME:PAST | 320/320 | 150/320 | 0/320 | 0/320 | 29.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | vocabulary | 41 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 106/160 | 3/160 | 2/160 | 19.0% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | vocabulary | 41 | en/single/POLARITY:NEGATIVE | 320/320 | 155/320 | 1/320 | 0/320 | 24.8% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | vocabulary | 41 | en/single/POLARITY:POSITIVE | 320/320 | 161/320 | 0/320 | 0/320 | 34.9% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | vocabulary | 41 | en/single/TIME:NOW | 320/320 | 143/320 | 0/320 | 0/320 | 30.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | vocabulary | 41 | en/single/TIME:PAST | 320/320 | 183/320 | 5/320 | 2/320 | 26.3% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | vocabulary | 41 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 86/160 | 4/160 | 2/160 | 23.6% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | vocabulary | 41 | vi/single/POLARITY:NEGATIVE | 320/320 | 83/320 | 2/320 | 0/320 | 28.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | vocabulary | 41 | vi/single/POLARITY:POSITIVE | 320/320 | 83/320 | 0/320 | 0/320 | 37.7% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | vocabulary | 41 | vi/single/TIME:NOW | 320/320 | 100/320 | 2/320 | 1/320 | 34.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | row_uniform | vocabulary | 41 | vi/single/TIME:PAST | 320/320 | 108/320 | 2/320 | 1/320 | 29.1% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |

## Limits and interpretation

Valid Unicode and EOS termination do not establish semantic correctness. The deterministic checker covers only the declared synthetic tense/polarity grammar and named roles. This benchmark tests recombination of familiar lexical factors; it does not establish naturalness, natural-corpus efficacy, or scientific efficacy. Control results are diagnostic; no TIDE advantage is claimed.

All examples and generated outputs remain private under Git-ignored `data/` and `runs/`. This report contains aggregate metrics only. `human_validated` is false. PhoMT raw/derived data and Phan Rang Cham data were not used.

Private aggregate evidence: `vi-en-ai-v4.20/protocol.json`, validation generation metrics under `vi-en-ai-v4.20`, and associated ignored run artifacts. Protocol SHA-256: `d2e911cb4d6e16627d7630a7d113530dcd73ae65a7806dc4bb68b70315400f23`.
