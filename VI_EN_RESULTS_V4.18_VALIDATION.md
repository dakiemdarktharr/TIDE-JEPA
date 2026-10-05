# vi-en-ai-v4.18 Vi–En validation results

AI-authored and independently AI-reviewed preliminary synthetic pilot. **Not human/native-speaker validated.** PhoMT was not used. Phan Rang Cham remains excluded.

## Frozen protocol

The corpus has 15360 records and 192 event combinations. Split groups: 112/40/40; records: 8960/3200/3200 (train/validation/release holdout). Data split policy: 112 train, 40 validation, 40 release-holdout combinations from three fresh agent factors; every held-out factor pair is represented in training; English NOW uses present progressive; four context-balanced surface realizations per meaning state; train, validation, and sealed holdout use the same action order; fresh split for a 2x2 TIDE-auxiliary/source-copy supervision factorial. Frozen release-holdout scope: The release holdout uses the same ordered action paths as train and validation; it probes fresh held-out factor combinations only and does not add an action-order shift.

Objective conditions: tide with source-copy weight 0 and TIDE latent-objective multiplier 0; transition balance `unique_transition`; tide with source-copy weight 0 and TIDE latent-objective multiplier 0.1; transition balance `unique_transition`; tide with source-copy weight 1.5 and TIDE latent-objective multiplier 0; transition balance `unique_transition`; tide with source-copy weight 1.5 and TIDE latent-objective multiplier 0.1; transition balance `unique_transition`. Seeds 17, 23, 41; 29 epochs and 3248 updates/config; width 32, 4 heads, 1 layers. Checkpoints selected using the frozen validation criterion. Decoder: greedy byte-level UTF-8 constrained decoding; EOS only at complete codepoint boundaries.

The registered primary objective is `tide`. Frozen thresholds: valid Unicode 100%; single-action action fidelity and preservation each ≥90%; held-out-path action fidelity and preservation each ≥80%. Every configured primary weight, seed, and language/action bucket must meet all applicable thresholds.

## Validation result: **FAIL**

The release holdout was not evaluated and remains sealed.

| Mode | Source-copy weight | TIDE aux multiplier | Edge balance | Seed | Val token CE | Val path token CE | Updates | Training wall seconds | Mean examples/sec | Gate |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---|
| tide | 0 | 0 | unique_transition | 17 | 0.3864 | 0.2383 | 3248 | 1023.0 | 254.5 | fail |
| tide | 0 | 0.1 | unique_transition | 17 | 0.4133 | 0.2427 | 3248 | 1023.7 | 253.9 | fail |
| tide | 1.5 | 0 | unique_transition | 17 | 0.3176 | 0.2214 | 3248 | 990.1 | 262.8 | fail |
| tide | 1.5 | 0.1 | unique_transition | 17 | 0.3438 | 0.2369 | 3248 | 1023.6 | 254.1 | fail |
| tide | 0 | 0 | unique_transition | 23 | 0.3756 | 0.2231 | 3248 | 970.8 | 268.2 | fail |
| tide | 0 | 0.1 | unique_transition | 23 | 0.3260 | 0.1825 | 3248 | 1038.3 | 250.4 | fail |
| tide | 1.5 | 0 | unique_transition | 23 | 0.2765 | 0.1836 | 3248 | 1014.5 | 256.4 | fail |
| tide | 1.5 | 0.1 | unique_transition | 23 | 0.2685 | 0.1747 | 3248 | 1032.1 | 251.9 | fail |
| tide | 0 | 0 | unique_transition | 41 | 0.4230 | 0.2554 | 3248 | 976.8 | 266.3 | fail |
| tide | 0 | 0.1 | unique_transition | 41 | 0.4111 | 0.2560 | 3248 | 1008.5 | 258.7 | fail |
| tide | 1.5 | 0 | unique_transition | 41 | 0.3197 | 0.2187 | 3248 | 1010.1 | 258.4 | fail |
| tide | 1.5 | 0.1 | unique_transition | 41 | 0.3246 | 0.2078 | 3248 | 999.5 | 261.0 | fail |

## Validation generation by condition and bucket

Action fidelity and preservation are pooled across seeds within each condition and bucket; thresholds are still checked for every primary condition/seed/bucket. Exact-reference match and CER are synthetic-reference metrics, not human naturalness.

| Mode | Source-copy weight | TIDE aux multiplier | Edge balance | Bucket | Action fidelity | Preservation | Accepted references | CER | Unicode | EOS |
|---|---:|---:|---|---|---:|---:|---:|---:|---:|---:|---|
| tide | 0 | 0 | unique_transition | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/0 | 0/0 | 30/480 | 20.0% | 480/480 | 480/480 |
| tide | 0 | 0 | unique_transition | en/single/POLARITY:NEGATIVE | 0/0 | 0/0 | 10/960 | 28.6% | 960/960 | 960/960 |
| tide | 0 | 0 | unique_transition | en/single/POLARITY:POSITIVE | 0/0 | 0/0 | 0/960 | 37.1% | 960/960 | 960/960 |
| tide | 0 | 0 | unique_transition | en/single/TIME:NOW | 0/0 | 0/0 | 0/960 | 34.3% | 960/960 | 960/960 |
| tide | 0 | 0 | unique_transition | en/single/TIME:PAST | 0/0 | 0/0 | 12/960 | 29.4% | 960/960 | 960/960 |
| tide | 0 | 0 | unique_transition | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/0 | 0/0 | 1/480 | 26.7% | 480/480 | 480/480 |
| tide | 0 | 0 | unique_transition | vi/single/POLARITY:NEGATIVE | 0/0 | 0/0 | 0/960 | 32.2% | 960/960 | 960/960 |
| tide | 0 | 0 | unique_transition | vi/single/POLARITY:POSITIVE | 0/0 | 0/0 | 0/960 | 37.7% | 960/960 | 960/960 |
| tide | 0 | 0 | unique_transition | vi/single/TIME:NOW | 0/0 | 0/0 | 0/960 | 39.3% | 960/960 | 960/960 |
| tide | 0 | 0 | unique_transition | vi/single/TIME:PAST | 0/0 | 0/0 | 3/960 | 30.5% | 960/960 | 960/960 |
| tide | 0 | 0.1 | unique_transition | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/0 | 0/0 | 18/480 | 20.8% | 480/480 | 480/480 |
| tide | 0 | 0.1 | unique_transition | en/single/POLARITY:NEGATIVE | 0/0 | 0/0 | 2/960 | 29.3% | 960/960 | 960/960 |
| tide | 0 | 0.1 | unique_transition | en/single/POLARITY:POSITIVE | 0/0 | 0/0 | 0/960 | 36.5% | 960/960 | 960/960 |
| tide | 0 | 0.1 | unique_transition | en/single/TIME:NOW | 0/0 | 0/0 | 0/960 | 34.0% | 960/960 | 960/960 |
| tide | 0 | 0.1 | unique_transition | en/single/TIME:PAST | 0/0 | 0/0 | 8/960 | 30.3% | 960/960 | 960/960 |
| tide | 0 | 0.1 | unique_transition | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/0 | 0/0 | 3/480 | 25.1% | 480/480 | 480/480 |
| tide | 0 | 0.1 | unique_transition | vi/single/POLARITY:NEGATIVE | 0/0 | 0/0 | 3/960 | 31.8% | 960/960 | 960/960 |
| tide | 0 | 0.1 | unique_transition | vi/single/POLARITY:POSITIVE | 0/0 | 0/0 | 0/960 | 36.3% | 960/960 | 960/960 |
| tide | 0 | 0.1 | unique_transition | vi/single/TIME:NOW | 0/0 | 0/0 | 0/960 | 37.2% | 960/960 | 960/960 |
| tide | 0 | 0.1 | unique_transition | vi/single/TIME:PAST | 0/0 | 0/0 | 5/960 | 29.0% | 960/960 | 960/960 |
| tide | 1.5 | 0 | unique_transition | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/0 | 0/0 | 19/480 | 20.0% | 480/480 | 480/480 |
| tide | 1.5 | 0 | unique_transition | en/single/POLARITY:NEGATIVE | 0/0 | 0/0 | 18/960 | 25.2% | 960/960 | 960/960 |
| tide | 1.5 | 0 | unique_transition | en/single/POLARITY:POSITIVE | 0/0 | 0/0 | 5/960 | 31.4% | 960/960 | 960/960 |
| tide | 1.5 | 0 | unique_transition | en/single/TIME:NOW | 0/0 | 0/0 | 4/960 | 29.7% | 960/960 | 960/960 |
| tide | 1.5 | 0 | unique_transition | en/single/TIME:PAST | 0/0 | 0/0 | 7/960 | 27.5% | 960/960 | 960/960 |
| tide | 1.5 | 0 | unique_transition | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/0 | 0/0 | 11/480 | 27.1% | 480/480 | 480/480 |
| tide | 1.5 | 0 | unique_transition | vi/single/POLARITY:NEGATIVE | 0/0 | 0/0 | 7/960 | 30.2% | 960/960 | 960/960 |
| tide | 1.5 | 0 | unique_transition | vi/single/POLARITY:POSITIVE | 0/0 | 0/0 | 1/960 | 34.5% | 960/960 | 960/960 |
| tide | 1.5 | 0 | unique_transition | vi/single/TIME:NOW | 0/0 | 0/0 | 3/960 | 34.2% | 960/960 | 960/960 |
| tide | 1.5 | 0 | unique_transition | vi/single/TIME:PAST | 0/0 | 0/0 | 8/960 | 31.2% | 960/960 | 960/960 |
| tide | 1.5 | 0.1 | unique_transition | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/0 | 0/0 | 24/480 | 19.8% | 480/480 | 480/480 |
| tide | 1.5 | 0.1 | unique_transition | en/single/POLARITY:NEGATIVE | 0/0 | 0/0 | 15/960 | 27.4% | 960/960 | 960/960 |
| tide | 1.5 | 0.1 | unique_transition | en/single/POLARITY:POSITIVE | 0/0 | 0/0 | 2/960 | 30.6% | 960/960 | 960/960 |
| tide | 1.5 | 0.1 | unique_transition | en/single/TIME:NOW | 0/0 | 0/0 | 2/960 | 32.3% | 960/960 | 960/960 |
| tide | 1.5 | 0.1 | unique_transition | en/single/TIME:PAST | 0/0 | 0/0 | 13/960 | 26.9% | 960/960 | 960/960 |
| tide | 1.5 | 0.1 | unique_transition | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/0 | 0/0 | 8/480 | 25.4% | 480/480 | 480/480 |
| tide | 1.5 | 0.1 | unique_transition | vi/single/POLARITY:NEGATIVE | 0/0 | 0/0 | 6/960 | 29.3% | 960/960 | 960/960 |
| tide | 1.5 | 0.1 | unique_transition | vi/single/POLARITY:POSITIVE | 0/0 | 0/0 | 3/960 | 34.2% | 960/960 | 960/960 |
| tide | 1.5 | 0.1 | unique_transition | vi/single/TIME:NOW | 0/0 | 0/0 | 1/960 | 35.8% | 960/960 | 960/960 |
| tide | 1.5 | 0.1 | unique_transition | vi/single/TIME:PAST | 0/0 | 0/0 | 4/960 | 30.9% | 960/960 | 960/960 |

## Primary-mode validation diagnostics by seed

Counts below preserve the frozen seed-by-seed gate denominator. No generated or reference text is included.

| Source-copy weight | TIDE aux multiplier | Edge balance | Seed | Bucket | Action fidelity | Preservation | Accepted references | CER | Unicode | EOS | Failure reason | Bucket gate |
|---:|---:|---|---:|---|---:|---:|---:|---:|---:|---:|---|---|
| 0 | 0 | unique_transition | 17 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/0 | 0/0 | 13/160 | 20.6% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | unique_transition | 17 | en/single/POLARITY:NEGATIVE | 0/0 | 0/0 | 4/320 | 28.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | unique_transition | 17 | en/single/POLARITY:POSITIVE | 0/0 | 0/0 | 0/320 | 36.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | unique_transition | 17 | en/single/TIME:NOW | 0/0 | 0/0 | 0/320 | 34.1% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | unique_transition | 17 | en/single/TIME:PAST | 0/0 | 0/0 | 6/320 | 28.5% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | unique_transition | 17 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/0 | 0/0 | 0/160 | 29.5% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | unique_transition | 17 | vi/single/POLARITY:NEGATIVE | 0/0 | 0/0 | 0/320 | 34.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | unique_transition | 17 | vi/single/POLARITY:POSITIVE | 0/0 | 0/0 | 0/320 | 39.2% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | unique_transition | 17 | vi/single/TIME:NOW | 0/0 | 0/0 | 0/320 | 42.7% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | unique_transition | 17 | vi/single/TIME:PAST | 0/0 | 0/0 | 0/320 | 33.5% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | unique_transition | 23 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/0 | 0/0 | 5/160 | 19.1% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | unique_transition | 23 | en/single/POLARITY:NEGATIVE | 0/0 | 0/0 | 1/320 | 27.8% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | unique_transition | 23 | en/single/POLARITY:POSITIVE | 0/0 | 0/0 | 0/320 | 37.9% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | unique_transition | 23 | en/single/TIME:NOW | 0/0 | 0/0 | 0/320 | 36.1% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | unique_transition | 23 | en/single/TIME:PAST | 0/0 | 0/0 | 3/320 | 29.7% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | unique_transition | 23 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/0 | 0/0 | 1/160 | 23.4% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | unique_transition | 23 | vi/single/POLARITY:NEGATIVE | 0/0 | 0/0 | 0/320 | 31.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | unique_transition | 23 | vi/single/POLARITY:POSITIVE | 0/0 | 0/0 | 0/320 | 36.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | unique_transition | 23 | vi/single/TIME:NOW | 0/0 | 0/0 | 0/320 | 38.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | unique_transition | 23 | vi/single/TIME:PAST | 0/0 | 0/0 | 1/320 | 28.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | unique_transition | 41 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/0 | 0/0 | 12/160 | 20.2% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | unique_transition | 41 | en/single/POLARITY:NEGATIVE | 0/0 | 0/0 | 5/320 | 29.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | unique_transition | 41 | en/single/POLARITY:POSITIVE | 0/0 | 0/0 | 0/320 | 37.3% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | unique_transition | 41 | en/single/TIME:NOW | 0/0 | 0/0 | 0/320 | 32.7% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | unique_transition | 41 | en/single/TIME:PAST | 0/0 | 0/0 | 3/320 | 30.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | unique_transition | 41 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/0 | 0/0 | 0/160 | 27.1% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | unique_transition | 41 | vi/single/POLARITY:NEGATIVE | 0/0 | 0/0 | 0/320 | 30.9% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | unique_transition | 41 | vi/single/POLARITY:POSITIVE | 0/0 | 0/0 | 0/320 | 37.5% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | unique_transition | 41 | vi/single/TIME:NOW | 0/0 | 0/0 | 0/320 | 36.8% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | unique_transition | 41 | vi/single/TIME:PAST | 0/0 | 0/0 | 2/320 | 30.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0.1 | unique_transition | 17 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/0 | 0/0 | 6/160 | 21.3% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0.1 | unique_transition | 17 | en/single/POLARITY:NEGATIVE | 0/0 | 0/0 | 0/320 | 31.2% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0.1 | unique_transition | 17 | en/single/POLARITY:POSITIVE | 0/0 | 0/0 | 0/320 | 36.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0.1 | unique_transition | 17 | en/single/TIME:NOW | 0/0 | 0/0 | 0/320 | 34.2% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0.1 | unique_transition | 17 | en/single/TIME:PAST | 0/0 | 0/0 | 1/320 | 30.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0.1 | unique_transition | 17 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/0 | 0/0 | 1/160 | 26.9% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0.1 | unique_transition | 17 | vi/single/POLARITY:NEGATIVE | 0/0 | 0/0 | 0/320 | 33.8% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0.1 | unique_transition | 17 | vi/single/POLARITY:POSITIVE | 0/0 | 0/0 | 0/320 | 38.8% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0.1 | unique_transition | 17 | vi/single/TIME:NOW | 0/0 | 0/0 | 0/320 | 38.9% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0.1 | unique_transition | 17 | vi/single/TIME:PAST | 0/0 | 0/0 | 1/320 | 31.8% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0.1 | unique_transition | 23 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/0 | 0/0 | 6/160 | 17.4% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0.1 | unique_transition | 23 | en/single/POLARITY:NEGATIVE | 0/0 | 0/0 | 0/320 | 27.7% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0.1 | unique_transition | 23 | en/single/POLARITY:POSITIVE | 0/0 | 0/0 | 0/320 | 33.7% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0.1 | unique_transition | 23 | en/single/TIME:NOW | 0/0 | 0/0 | 0/320 | 33.8% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0.1 | unique_transition | 23 | en/single/TIME:PAST | 0/0 | 0/0 | 1/320 | 26.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0.1 | unique_transition | 23 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/0 | 0/0 | 1/160 | 23.0% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0.1 | unique_transition | 23 | vi/single/POLARITY:NEGATIVE | 0/0 | 0/0 | 3/320 | 28.2% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0.1 | unique_transition | 23 | vi/single/POLARITY:POSITIVE | 0/0 | 0/0 | 0/320 | 33.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0.1 | unique_transition | 23 | vi/single/TIME:NOW | 0/0 | 0/0 | 0/320 | 34.2% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0.1 | unique_transition | 23 | vi/single/TIME:PAST | 0/0 | 0/0 | 3/320 | 25.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0.1 | unique_transition | 41 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/0 | 0/0 | 6/160 | 23.7% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0.1 | unique_transition | 41 | en/single/POLARITY:NEGATIVE | 0/0 | 0/0 | 2/320 | 29.1% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0.1 | unique_transition | 41 | en/single/POLARITY:POSITIVE | 0/0 | 0/0 | 0/320 | 39.1% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0.1 | unique_transition | 41 | en/single/TIME:NOW | 0/0 | 0/0 | 0/320 | 34.1% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0.1 | unique_transition | 41 | en/single/TIME:PAST | 0/0 | 0/0 | 6/320 | 34.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0.1 | unique_transition | 41 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/0 | 0/0 | 1/160 | 25.5% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0.1 | unique_transition | 41 | vi/single/POLARITY:NEGATIVE | 0/0 | 0/0 | 0/320 | 33.5% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0.1 | unique_transition | 41 | vi/single/POLARITY:POSITIVE | 0/0 | 0/0 | 0/320 | 37.1% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0.1 | unique_transition | 41 | vi/single/TIME:NOW | 0/0 | 0/0 | 0/320 | 38.5% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0.1 | unique_transition | 41 | vi/single/TIME:PAST | 0/0 | 0/0 | 1/320 | 29.7% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0 | unique_transition | 17 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/0 | 0/0 | 1/160 | 20.5% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0 | unique_transition | 17 | en/single/POLARITY:NEGATIVE | 0/0 | 0/0 | 2/320 | 25.8% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0 | unique_transition | 17 | en/single/POLARITY:POSITIVE | 0/0 | 0/0 | 0/320 | 32.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0 | unique_transition | 17 | en/single/TIME:NOW | 0/0 | 0/0 | 0/320 | 32.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0 | unique_transition | 17 | en/single/TIME:PAST | 0/0 | 0/0 | 0/320 | 27.5% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0 | unique_transition | 17 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/0 | 0/0 | 2/160 | 31.8% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0 | unique_transition | 17 | vi/single/POLARITY:NEGATIVE | 0/0 | 0/0 | 0/320 | 33.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0 | unique_transition | 17 | vi/single/POLARITY:POSITIVE | 0/0 | 0/0 | 0/320 | 35.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0 | unique_transition | 17 | vi/single/TIME:NOW | 0/0 | 0/0 | 0/320 | 36.1% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0 | unique_transition | 17 | vi/single/TIME:PAST | 0/0 | 0/0 | 0/320 | 34.3% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0 | unique_transition | 23 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/0 | 0/0 | 3/160 | 20.4% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0 | unique_transition | 23 | en/single/POLARITY:NEGATIVE | 0/0 | 0/0 | 3/320 | 24.5% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0 | unique_transition | 23 | en/single/POLARITY:POSITIVE | 0/0 | 0/0 | 2/320 | 33.1% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0 | unique_transition | 23 | en/single/TIME:NOW | 0/0 | 0/0 | 0/320 | 29.7% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0 | unique_transition | 23 | en/single/TIME:PAST | 0/0 | 0/0 | 3/320 | 28.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0 | unique_transition | 23 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/0 | 0/0 | 9/160 | 23.1% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0 | unique_transition | 23 | vi/single/POLARITY:NEGATIVE | 0/0 | 0/0 | 4/320 | 29.2% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0 | unique_transition | 23 | vi/single/POLARITY:POSITIVE | 0/0 | 0/0 | 1/320 | 33.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0 | unique_transition | 23 | vi/single/TIME:NOW | 0/0 | 0/0 | 3/320 | 32.9% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0 | unique_transition | 23 | vi/single/TIME:PAST | 0/0 | 0/0 | 7/320 | 30.5% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0 | unique_transition | 41 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/0 | 0/0 | 15/160 | 19.0% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0 | unique_transition | 41 | en/single/POLARITY:NEGATIVE | 0/0 | 0/0 | 13/320 | 25.2% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0 | unique_transition | 41 | en/single/POLARITY:POSITIVE | 0/0 | 0/0 | 3/320 | 29.2% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0 | unique_transition | 41 | en/single/TIME:NOW | 0/0 | 0/0 | 4/320 | 26.9% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0 | unique_transition | 41 | en/single/TIME:PAST | 0/0 | 0/0 | 4/320 | 26.9% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0 | unique_transition | 41 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/0 | 0/0 | 0/160 | 26.4% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0 | unique_transition | 41 | vi/single/POLARITY:NEGATIVE | 0/0 | 0/0 | 3/320 | 27.7% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0 | unique_transition | 41 | vi/single/POLARITY:POSITIVE | 0/0 | 0/0 | 0/320 | 34.5% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0 | unique_transition | 41 | vi/single/TIME:NOW | 0/0 | 0/0 | 0/320 | 33.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0 | unique_transition | 41 | vi/single/TIME:PAST | 0/0 | 0/0 | 1/320 | 28.7% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 17 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/0 | 0/0 | 0/160 | 21.3% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 17 | en/single/POLARITY:NEGATIVE | 0/0 | 0/0 | 0/320 | 30.1% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 17 | en/single/POLARITY:POSITIVE | 0/0 | 0/0 | 0/320 | 31.9% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 17 | en/single/TIME:NOW | 0/0 | 0/0 | 0/320 | 33.8% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 17 | en/single/TIME:PAST | 0/0 | 0/0 | 1/320 | 26.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 17 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/0 | 0/0 | 0/160 | 32.4% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 17 | vi/single/POLARITY:NEGATIVE | 0/0 | 0/0 | 1/320 | 33.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 17 | vi/single/POLARITY:POSITIVE | 0/0 | 0/0 | 0/320 | 40.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 17 | vi/single/TIME:NOW | 0/0 | 0/0 | 0/320 | 37.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 17 | vi/single/TIME:PAST | 0/0 | 0/0 | 0/320 | 36.5% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 23 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/0 | 0/0 | 11/160 | 17.3% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 23 | en/single/POLARITY:NEGATIVE | 0/0 | 0/0 | 2/320 | 24.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 23 | en/single/POLARITY:POSITIVE | 0/0 | 0/0 | 1/320 | 27.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 23 | en/single/TIME:NOW | 0/0 | 0/0 | 0/320 | 29.1% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 23 | en/single/TIME:PAST | 0/0 | 0/0 | 3/320 | 25.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 23 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/0 | 0/0 | 5/160 | 24.2% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 23 | vi/single/POLARITY:NEGATIVE | 0/0 | 0/0 | 4/320 | 26.5% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 23 | vi/single/POLARITY:POSITIVE | 0/0 | 0/0 | 3/320 | 32.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 23 | vi/single/TIME:NOW | 0/0 | 0/0 | 0/320 | 38.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 23 | vi/single/TIME:PAST | 0/0 | 0/0 | 2/320 | 29.3% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 41 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/0 | 0/0 | 13/160 | 20.7% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 41 | en/single/POLARITY:NEGATIVE | 0/0 | 0/0 | 13/320 | 27.5% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 41 | en/single/POLARITY:POSITIVE | 0/0 | 0/0 | 1/320 | 32.8% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 41 | en/single/TIME:NOW | 0/0 | 0/0 | 2/320 | 34.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 41 | en/single/TIME:PAST | 0/0 | 0/0 | 9/320 | 29.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 41 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 0/0 | 0/0 | 3/160 | 19.5% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 41 | vi/single/POLARITY:NEGATIVE | 0/0 | 0/0 | 1/320 | 28.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 41 | vi/single/POLARITY:POSITIVE | 0/0 | 0/0 | 0/320 | 30.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 41 | vi/single/TIME:NOW | 0/0 | 0/0 | 1/320 | 31.8% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 41 | vi/single/TIME:PAST | 0/0 | 0/0 | 2/320 | 26.8% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |

## Limits and interpretation

Valid Unicode and EOS termination do not establish semantic correctness. The deterministic checker covers only the declared synthetic tense/polarity grammar and named roles. This benchmark tests recombination of familiar lexical factors; it does not establish naturalness, natural-corpus efficacy, or scientific efficacy. Control results are diagnostic; no TIDE advantage is claimed.

All examples and generated outputs remain private under Git-ignored `data/` and `runs/`. This report contains aggregate metrics only. `human_validated` is false. PhoMT raw/derived data and Phan Rang Cham data were not used.

Private aggregate evidence: `vi-en-ai-v4.18/protocol.json`, validation generation metrics under `vi-en-ai-v4.18`, and associated ignored run artifacts. Protocol SHA-256: `278cefdd57da675211a1a9312701f6892a9d0bcdea14384bc73e35122bb3bb5e`.
