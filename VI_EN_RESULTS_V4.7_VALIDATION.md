# vi-en-ai-v4.7 Vi–En validation results

AI-authored and independently AI-reviewed preliminary synthetic pilot. **Not human/native-speaker validated.** PhoMT was not used. Phan Rang Cham remains excluded.

## Frozen protocol

The corpus has 8000 records and 200 event combinations. Split groups: 120/40/40; records: 4800/1600/1600 (train/validation/release holdout). Data split policy: 120 train, 40 validation, 40 release-holdout event combinations sampled outside every v4.4-v4.6 combination; all agent, verb lemma, and patient phrase values occur in training; every validation and release-holdout triple uses only factor pairs represented in training; English NOW uses present progressive.

Four controls; seeds 17, 23, 41; 54 epochs and 3240 updates/config; width 48, 4 heads, 2 layers. Checkpoints selected with validation token and path token CE. Decoder: greedy byte-level UTF-8 constrained decoding; EOS only at complete codepoint boundaries.

The registered primary mode is `tide`. Its engineering gate requires every seed and every language/action bucket to meet the frozen thresholds.

## Validation result: **FAIL**

The release holdout was not evaluated and remains sealed.

| Mode | Seed | Val token CE | Val path token CE | Updates | Training wall seconds | Mean examples/sec | Gate |
|---|---:|---:|---:|---:|---:|---:|---|
| token_only | 17 | 0.0093 | 0.0065 | 3240 | 1719.2 | 151.4 | control_only |
| generic_jepa | 17 | 0.0698 | 0.0395 | 3240 | 1870.3 | 139.1 | control_only |
| static_alignment | 17 | 0.0249 | 0.0264 | 3240 | 1894.2 | 137.4 | control_only |
| tide | 17 | 0.0319 | 0.0274 | 3240 | 1900.6 | 136.9 | pass |
| token_only | 23 | 0.0161 | 0.0076 | 3240 | 1696.0 | 153.2 | control_only |
| generic_jepa | 23 | 0.0079 | 0.0022 | 3240 | 1862.0 | 139.7 | control_only |
| static_alignment | 23 | 0.0123 | 0.0043 | 3240 | 1875.0 | 138.7 | control_only |
| tide | 23 | 0.0069 | 0.0030 | 3240 | 1874.6 | 138.8 | pass |
| token_only | 41 | 0.0125 | 0.0049 | 3240 | 1418.6 | 185.6 | control_only |
| generic_jepa | 41 | 0.0115 | 0.0056 | 3240 | 1373.0 | 191.3 | control_only |
| static_alignment | 41 | 0.0144 | 0.0101 | 3240 | 1369.2 | 191.7 | control_only |
| tide | 41 | 0.0153 | 0.0089 | 3240 | 1364.8 | 192.3 | fail |

## Validation generation by mode and bucket

Action fidelity and preservation are pooled across seeds within each bucket; thresholds are still checked for every seed/bucket. Exact-reference match and CER are synthetic-reference metrics, not human naturalness.

| Mode | Bucket | Action fidelity | Preservation | Accepted references | CER | Unicode | EOS |
|---|---|---:|---:|---:|---:|---:|---:|
| token_only | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 239/240 | 231/240 | 226/240 | 0.4% | 240/240 | 240/240 |
| token_only | en/single/POLARITY:NEGATIVE | 473/480 | 447/480 | 435/480 | 1.2% | 480/480 | 480/480 |
| token_only | en/single/POLARITY:POSITIVE | 468/480 | 430/480 | 419/480 | 1.5% | 480/480 | 480/480 |
| token_only | en/single/TIME:NOW | 469/480 | 435/480 | 427/480 | 1.5% | 480/480 | 480/480 |
| token_only | en/single/TIME:PAST | 472/480 | 435/480 | 428/480 | 1.2% | 480/480 | 480/480 |
| token_only | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 235/240 | 224/240 | 221/240 | 1.2% | 240/240 | 240/240 |
| token_only | vi/single/POLARITY:NEGATIVE | 472/480 | 443/480 | 436/480 | 1.7% | 480/480 | 480/480 |
| token_only | vi/single/POLARITY:POSITIVE | 467/480 | 429/480 | 411/480 | 2.6% | 480/480 | 480/480 |
| token_only | vi/single/TIME:NOW | 470/480 | 434/480 | 420/480 | 1.9% | 480/480 | 480/480 |
| token_only | vi/single/TIME:PAST | 466/480 | 443/480 | 432/480 | 1.4% | 480/480 | 480/480 |
| generic_jepa | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 239/240 | 231/240 | 229/240 | 0.5% | 240/240 | 240/240 |
| generic_jepa | en/single/POLARITY:NEGATIVE | 474/480 | 446/480 | 438/480 | 1.1% | 480/480 | 480/480 |
| generic_jepa | en/single/POLARITY:POSITIVE | 475/480 | 442/480 | 436/480 | 0.9% | 480/480 | 480/480 |
| generic_jepa | en/single/TIME:NOW | 473/480 | 444/480 | 434/480 | 1.2% | 480/480 | 480/480 |
| generic_jepa | en/single/TIME:PAST | 474/480 | 447/480 | 441/480 | 1.0% | 480/480 | 480/480 |
| generic_jepa | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 235/240 | 234/240 | 229/240 | 1.2% | 240/240 | 240/240 |
| generic_jepa | vi/single/POLARITY:NEGATIVE | 469/480 | 459/480 | 447/480 | 1.9% | 480/480 | 480/480 |
| generic_jepa | vi/single/POLARITY:POSITIVE | 474/480 | 457/480 | 444/480 | 1.1% | 480/480 | 480/480 |
| generic_jepa | vi/single/TIME:NOW | 470/480 | 453/480 | 441/480 | 1.5% | 480/480 | 480/480 |
| generic_jepa | vi/single/TIME:PAST | 476/480 | 461/480 | 458/480 | 0.6% | 480/480 | 480/480 |
| static_alignment | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 237/240 | 229/240 | 227/240 | 0.8% | 240/240 | 240/240 |
| static_alignment | en/single/POLARITY:NEGATIVE | 471/480 | 436/480 | 429/480 | 1.4% | 480/480 | 480/480 |
| static_alignment | en/single/POLARITY:POSITIVE | 478/480 | 435/480 | 425/480 | 1.3% | 480/480 | 480/480 |
| static_alignment | en/single/TIME:NOW | 470/480 | 445/480 | 433/480 | 1.2% | 480/480 | 480/480 |
| static_alignment | en/single/TIME:PAST | 478/480 | 436/480 | 429/480 | 1.2% | 480/480 | 480/480 |
| static_alignment | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 237/240 | 227/240 | 223/240 | 1.7% | 240/240 | 240/240 |
| static_alignment | vi/single/POLARITY:NEGATIVE | 472/480 | 438/480 | 428/480 | 2.4% | 480/480 | 480/480 |
| static_alignment | vi/single/POLARITY:POSITIVE | 476/480 | 443/480 | 434/480 | 1.4% | 480/480 | 480/480 |
| static_alignment | vi/single/TIME:NOW | 466/480 | 437/480 | 425/480 | 1.9% | 480/480 | 480/480 |
| static_alignment | vi/single/TIME:PAST | 471/480 | 453/480 | 443/480 | 1.5% | 480/480 | 480/480 |
| tide | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 237/240 | 228/240 | 224/240 | 0.6% | 240/240 | 240/240 |
| tide | en/single/POLARITY:NEGATIVE | 475/480 | 445/480 | 441/480 | 1.0% | 480/480 | 480/480 |
| tide | en/single/POLARITY:POSITIVE | 478/480 | 446/480 | 435/480 | 1.1% | 480/480 | 480/480 |
| tide | en/single/TIME:NOW | 470/480 | 437/480 | 429/480 | 1.6% | 480/480 | 480/480 |
| tide | en/single/TIME:PAST | 477/480 | 435/480 | 427/480 | 1.2% | 480/480 | 480/480 |
| tide | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 237/240 | 232/240 | 226/240 | 2.1% | 240/240 | 240/240 |
| tide | vi/single/POLARITY:NEGATIVE | 471/480 | 451/480 | 445/480 | 1.6% | 480/480 | 480/480 |
| tide | vi/single/POLARITY:POSITIVE | 473/480 | 443/480 | 428/480 | 1.8% | 480/480 | 480/480 |
| tide | vi/single/TIME:NOW | 472/480 | 452/480 | 439/480 | 1.4% | 480/480 | 480/480 |
| tide | vi/single/TIME:PAST | 473/480 | 458/480 | 449/480 | 1.9% | 480/480 | 480/480 |

## Limits and interpretation

Valid Unicode and EOS termination do not establish semantic correctness. The deterministic checker covers only the declared synthetic tense/polarity grammar and named roles. This benchmark tests recombination of familiar lexical factors; it does not establish naturalness, natural-corpus efficacy, or scientific efficacy. Control results are diagnostic; no TIDE advantage is claimed.

All examples and generated outputs remain private under Git-ignored `data/` and `runs/`. This report contains aggregate metrics only. `human_validated` is false. PhoMT raw/derived data and Phan Rang Cham data were not used.

Private aggregate evidence: `vi-en-ai-v4.7/protocol.json`, validation generation metrics under `vi-en-ai-v4.7`, and associated ignored run artifacts. Protocol SHA-256: `e5cd4c51acf0828ed1db0a4161d415b44c64e5da49ccfb61a3dfa1325d7b3358`.
