# vi-en-ai-v4.4 Vi–En validation results

AI-authored and independently AI-reviewed preliminary synthetic pilot. **Not human/native-speaker validated.** PhoMT was not used. Phan Rang Cham remains excluded.

## Frozen protocol

The corpus has 4160 records and 104 event combinations. Split groups: 80/12/12; records: 3200/480/480 (train/validation/release holdout). Data split policy: 80 train, 12 validation, 12 release-holdout event combinations; every agent, verb lemma and patient phrase occurs in training; frame/group-disjoint combinations built from broadly compatible actions and objects; test path order is held out.

Four controls; seeds 17, 23, 41; 20 epochs and 800 updates/config; width 48, 4 heads, 2 layers. Checkpoints selected with validation token and path token CE. Decoder: greedy byte-level UTF-8 constrained decoding; EOS only at complete codepoint boundaries.

The registered primary mode is `tide`. Its engineering gate requires every seed and every language/action bucket to meet the frozen thresholds.

## Validation result: **FAIL**

The release holdout was not evaluated and remains sealed.

| Mode | Seed | Val token CE | Val path token CE | Updates | Training wall seconds | Mean examples/sec | Gate |
|---|---:|---:|---:|---:|---:|---:|---|
| token_only | 17 | 0.1891 | 0.0852 | 800 | 371.9 | 174.6 | control_only |
| generic_jepa | 17 | 0.2249 | 0.0951 | 800 | 407.5 | 158.7 | control_only |
| static_alignment | 17 | 0.2142 | 0.0844 | 800 | 409.7 | 157.6 | control_only |
| tide | 17 | 0.2109 | 0.0861 | 800 | 409.4 | 157.8 | fail |
| token_only | 23 | 0.2075 | 0.0940 | 800 | 370.9 | 173.8 | control_only |
| generic_jepa | 23 | 0.1876 | 0.0844 | 800 | 406.8 | 159.0 | control_only |
| static_alignment | 23 | 0.1665 | 0.0715 | 800 | 409.0 | 157.9 | control_only |
| tide | 23 | 0.1702 | 0.0724 | 800 | 405.9 | 159.2 | fail |
| token_only | 41 | 0.2205 | 0.1054 | 800 | 353.2 | 183.3 | control_only |
| generic_jepa | 41 | 0.2623 | 0.1247 | 800 | 376.3 | 172.0 | control_only |
| static_alignment | 41 | 0.2568 | 0.1267 | 800 | 377.9 | 170.6 | control_only |
| tide | 41 | 0.2667 | 0.1267 | 800 | 377.5 | 170.8 | fail |

## Validation generation by mode and bucket

Action fidelity and preservation are pooled across seeds within each bucket; thresholds are still checked for every seed/bucket. Exact-reference match and CER are synthetic-reference metrics, not human naturalness.

| Mode | Bucket | Action fidelity | Preservation | Accepted references | CER | Unicode | EOS |
|---|---|---:|---:|---:|---:|---:|---:|
| token_only | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 68/72 | 46/72 | 44/72 | 4.4% | 72/72 | 72/72 |
| token_only | en/single/POLARITY:NEGATIVE | 103/144 | 61/144 | 49/144 | 13.0% | 144/144 | 144/144 |
| token_only | en/single/POLARITY:POSITIVE | 91/144 | 27/144 | 20/144 | 26.9% | 144/144 | 144/144 |
| token_only | en/single/TIME:NOW | 95/144 | 31/144 | 25/144 | 23.6% | 144/144 | 144/144 |
| token_only | en/single/TIME:PAST | 115/144 | 53/144 | 45/144 | 15.4% | 144/144 | 144/144 |
| token_only | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 60/72 | 23/72 | 23/72 | 17.9% | 72/72 | 72/72 |
| token_only | vi/single/POLARITY:NEGATIVE | 94/144 | 32/144 | 24/144 | 27.9% | 144/144 | 144/144 |
| token_only | vi/single/POLARITY:POSITIVE | 52/144 | 6/144 | 4/144 | 39.6% | 144/144 | 144/144 |
| token_only | vi/single/TIME:NOW | 65/144 | 17/144 | 10/144 | 37.8% | 144/144 | 144/144 |
| token_only | vi/single/TIME:PAST | 65/144 | 22/144 | 20/144 | 26.8% | 144/144 | 144/144 |
| generic_jepa | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 63/72 | 44/72 | 42/72 | 5.6% | 72/72 | 72/72 |
| generic_jepa | en/single/POLARITY:NEGATIVE | 107/144 | 59/144 | 53/144 | 14.9% | 144/144 | 144/144 |
| generic_jepa | en/single/POLARITY:POSITIVE | 95/144 | 19/144 | 13/144 | 28.1% | 144/144 | 144/144 |
| generic_jepa | en/single/TIME:NOW | 88/144 | 30/144 | 17/144 | 24.9% | 144/144 | 144/144 |
| generic_jepa | en/single/TIME:PAST | 107/144 | 39/144 | 38/144 | 18.7% | 144/144 | 144/144 |
| generic_jepa | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 59/72 | 32/72 | 30/72 | 12.5% | 72/72 | 72/72 |
| generic_jepa | vi/single/POLARITY:NEGATIVE | 64/144 | 44/144 | 23/144 | 23.8% | 144/144 | 144/144 |
| generic_jepa | vi/single/POLARITY:POSITIVE | 23/144 | 9/144 | 3/144 | 40.3% | 144/144 | 144/144 |
| generic_jepa | vi/single/TIME:NOW | 27/144 | 21/144 | 1/144 | 35.6% | 144/144 | 144/144 |
| generic_jepa | vi/single/TIME:PAST | 64/144 | 22/144 | 21/144 | 23.6% | 144/144 | 144/144 |
| static_alignment | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 68/72 | 52/72 | 52/72 | 4.0% | 72/72 | 72/72 |
| static_alignment | en/single/POLARITY:NEGATIVE | 86/144 | 53/144 | 48/144 | 16.7% | 144/144 | 144/144 |
| static_alignment | en/single/POLARITY:POSITIVE | 82/144 | 16/144 | 9/144 | 31.3% | 144/144 | 144/144 |
| static_alignment | en/single/TIME:NOW | 94/144 | 23/144 | 15/144 | 23.3% | 144/144 | 144/144 |
| static_alignment | en/single/TIME:PAST | 106/144 | 44/144 | 41/144 | 17.2% | 144/144 | 144/144 |
| static_alignment | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 61/72 | 30/72 | 30/72 | 16.4% | 72/72 | 72/72 |
| static_alignment | vi/single/POLARITY:NEGATIVE | 53/144 | 47/144 | 21/144 | 25.8% | 144/144 | 144/144 |
| static_alignment | vi/single/POLARITY:POSITIVE | 47/144 | 6/144 | 2/144 | 41.9% | 144/144 | 144/144 |
| static_alignment | vi/single/TIME:NOW | 66/144 | 17/144 | 5/144 | 34.4% | 144/144 | 144/144 |
| static_alignment | vi/single/TIME:PAST | 66/144 | 27/144 | 23/144 | 24.2% | 144/144 | 144/144 |
| tide | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 67/72 | 47/72 | 45/72 | 5.2% | 72/72 | 72/72 |
| tide | en/single/POLARITY:NEGATIVE | 92/144 | 58/144 | 51/144 | 16.5% | 144/144 | 144/144 |
| tide | en/single/POLARITY:POSITIVE | 69/144 | 17/144 | 11/144 | 33.5% | 144/144 | 144/144 |
| tide | en/single/TIME:NOW | 89/144 | 23/144 | 17/144 | 25.5% | 144/144 | 144/144 |
| tide | en/single/TIME:PAST | 101/144 | 48/144 | 43/144 | 17.3% | 144/144 | 144/144 |
| tide | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 62/72 | 30/72 | 30/72 | 16.1% | 72/72 | 72/72 |
| tide | vi/single/POLARITY:NEGATIVE | 78/144 | 42/144 | 27/144 | 25.5% | 144/144 | 144/144 |
| tide | vi/single/POLARITY:POSITIVE | 32/144 | 7/144 | 2/144 | 42.8% | 144/144 | 144/144 |
| tide | vi/single/TIME:NOW | 41/144 | 21/144 | 7/144 | 35.7% | 144/144 | 144/144 |
| tide | vi/single/TIME:PAST | 60/144 | 18/144 | 17/144 | 26.1% | 144/144 | 144/144 |

## Limits and interpretation

Valid Unicode and EOS termination do not establish semantic correctness. The deterministic checker covers only the declared synthetic tense/polarity grammar and named roles. This benchmark tests recombination of familiar lexical factors; it does not establish naturalness, natural-corpus efficacy, or scientific efficacy. Control results are diagnostic; no TIDE advantage is claimed.

All examples and generated outputs remain private under Git-ignored `data/` and `runs/`. This report contains aggregate metrics only. `human_validated` is false. PhoMT raw/derived data and Phan Rang Cham data were not used.

Private aggregate evidence: `vi-en-ai-v4.4/protocol.json`, validation generation metrics under `vi-en-ai-v4.4`, and associated ignored run artifacts. Protocol SHA-256: `8cd59dbf1ee7c87b4cec8a4604614eeac4225c132755b58f9d1de25510228eb0`.
