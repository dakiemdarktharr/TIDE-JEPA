# vi-en-ai-v4.12 Vi–En validation results

AI-authored and independently AI-reviewed preliminary synthetic pilot. **Not human/native-speaker validated.** PhoMT was not used. Phan Rang Cham remains excluded.

## Frozen protocol

The corpus has 7680 records and 192 event combinations. Split groups: 112/40/40; records: 4480/1600/1600 (train/validation/release holdout). Data split policy: 112 train, 40 validation, 40 release-holdout combinations from three new agents; every held-out factor pair is represented in training; English NOW uses present progressive; fresh factors and holdout for matched source-copy ablation.

Objective conditions: tide with source-copy weight 0; tide with source-copy weight 1.5; token_only with source-copy weight 0; token_only with source-copy weight 1.5. Seeds 17, 23, 41; 58 epochs and 3248 updates/config; width 48, 4 heads, 2 layers. Checkpoints selected using the frozen validation criterion. Decoder: greedy byte-level UTF-8 constrained decoding; EOS only at complete codepoint boundaries.

The registered primary objective is `tide`. Its engineering gate requires every configured primary weight, seed, and language/action bucket to meet the frozen thresholds.

## Validation result: **FAIL**

The release holdout was not evaluated and remains sealed.

| Mode | Source-copy weight | Seed | Val token CE | Val path token CE | Updates | Training wall seconds | Mean examples/sec | Gate |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| token_only | 0 | 17 | 0.0161 | 0.0062 | 3248 | 1436.4 | 181.0 | control_only |
| token_only | 1.5 | 17 | 0.0053 | 0.0025 | 3248 | 1501.8 | 173.1 | control_only |
| tide | 0 | 17 | 0.0710 | 0.0288 | 3248 | 1609.7 | 161.5 | fail |
| tide | 1.5 | 17 | 0.0124 | 0.0083 | 3248 | 1687.9 | 154.0 | fail |
| token_only | 0 | 23 | 0.0198 | 0.0093 | 3248 | 1437.6 | 180.9 | control_only |
| token_only | 1.5 | 23 | 0.0081 | 0.0040 | 3248 | 1511.4 | 172.1 | control_only |
| tide | 0 | 23 | 0.0346 | 0.0102 | 3248 | 1618.9 | 160.8 | fail |
| tide | 1.5 | 23 | 0.0423 | 0.0355 | 3248 | 1712.5 | 152.0 | fail |
| token_only | 0 | 41 | 0.0146 | 0.0087 | 3248 | 1438.7 | 180.9 | control_only |
| token_only | 1.5 | 41 | 0.0221 | 0.0389 | 3248 | 1490.9 | 175.0 | control_only |
| tide | 0 | 41 | 0.0576 | 0.0361 | 3248 | 1502.5 | 175.2 | fail |
| tide | 1.5 | 41 | 0.0227 | 0.0200 | 3248 | 1520.1 | 174.9 | fail |

## Validation generation by condition and bucket

Action fidelity and preservation are pooled across seeds within each condition and bucket; thresholds are still checked for every primary condition/seed/bucket. Exact-reference match and CER are synthetic-reference metrics, not human naturalness.

| Mode | Source-copy weight | Bucket | Action fidelity | Preservation | Accepted references | CER | Unicode | EOS |
|---|---:|---|---:|---:|---:|---:|---:|---:|---|
| tide | 0 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 237/240 | 224/240 | 216/240 | 1.0% | 240/240 | 240/240 |
| tide | 0 | en/single/POLARITY:NEGATIVE | 473/480 | 419/480 | 414/480 | 1.6% | 480/480 | 480/480 |
| tide | 0 | en/single/POLARITY:POSITIVE | 473/480 | 395/480 | 385/480 | 2.9% | 480/480 | 480/480 |
| tide | 0 | en/single/TIME:NOW | 468/480 | 403/480 | 392/480 | 2.1% | 480/480 | 480/480 |
| tide | 0 | en/single/TIME:PAST | 466/480 | 403/480 | 393/480 | 2.8% | 480/480 | 480/480 |
| tide | 0 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 239/240 | 218/240 | 215/240 | 1.1% | 240/240 | 240/240 |
| tide | 0 | vi/single/POLARITY:NEGATIVE | 462/480 | 396/480 | 385/480 | 2.9% | 480/480 | 480/480 |
| tide | 0 | vi/single/POLARITY:POSITIVE | 446/480 | 347/480 | 314/480 | 5.1% | 480/480 | 480/480 |
| tide | 0 | vi/single/TIME:NOW | 437/480 | 359/480 | 322/480 | 5.2% | 480/480 | 480/480 |
| tide | 0 | vi/single/TIME:PAST | 446/480 | 365/480 | 354/480 | 3.3% | 480/480 | 480/480 |
| tide | 1.5 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 238/240 | 229/240 | 227/240 | 0.7% | 240/240 | 240/240 |
| tide | 1.5 | en/single/POLARITY:NEGATIVE | 476/480 | 440/480 | 432/480 | 1.0% | 480/480 | 480/480 |
| tide | 1.5 | en/single/POLARITY:POSITIVE | 476/480 | 419/480 | 415/480 | 1.6% | 480/480 | 480/480 |
| tide | 1.5 | en/single/TIME:NOW | 477/480 | 439/480 | 433/480 | 0.9% | 480/480 | 480/480 |
| tide | 1.5 | en/single/TIME:PAST | 473/480 | 439/480 | 437/480 | 1.1% | 480/480 | 480/480 |
| tide | 1.5 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 236/240 | 224/240 | 219/240 | 1.0% | 240/240 | 240/240 |
| tide | 1.5 | vi/single/POLARITY:NEGATIVE | 469/480 | 435/480 | 426/480 | 1.6% | 480/480 | 480/480 |
| tide | 1.5 | vi/single/POLARITY:POSITIVE | 467/480 | 401/480 | 375/480 | 3.0% | 480/480 | 480/480 |
| tide | 1.5 | vi/single/TIME:NOW | 456/480 | 416/480 | 382/480 | 2.9% | 480/480 | 480/480 |
| tide | 1.5 | vi/single/TIME:PAST | 462/480 | 407/480 | 401/480 | 2.0% | 480/480 | 480/480 |
| token_only | 0 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 239/240 | 236/240 | 231/240 | 0.3% | 240/240 | 240/240 |
| token_only | 0 | en/single/POLARITY:NEGATIVE | 473/480 | 428/480 | 416/480 | 1.3% | 480/480 | 480/480 |
| token_only | 0 | en/single/POLARITY:POSITIVE | 473/480 | 430/480 | 423/480 | 1.5% | 480/480 | 480/480 |
| token_only | 0 | en/single/TIME:NOW | 473/480 | 420/480 | 413/480 | 1.5% | 480/480 | 480/480 |
| token_only | 0 | en/single/TIME:PAST | 474/480 | 436/480 | 429/480 | 1.4% | 480/480 | 480/480 |
| token_only | 0 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 235/240 | 214/240 | 208/240 | 1.5% | 240/240 | 240/240 |
| token_only | 0 | vi/single/POLARITY:NEGATIVE | 461/480 | 394/480 | 378/480 | 2.7% | 480/480 | 480/480 |
| token_only | 0 | vi/single/POLARITY:POSITIVE | 451/480 | 384/480 | 350/480 | 3.9% | 480/480 | 480/480 |
| token_only | 0 | vi/single/TIME:NOW | 454/480 | 372/480 | 342/480 | 4.6% | 480/480 | 480/480 |
| token_only | 0 | vi/single/TIME:PAST | 465/480 | 403/480 | 395/480 | 2.5% | 480/480 | 480/480 |
| token_only | 1.5 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 238/240 | 230/240 | 228/240 | 0.6% | 240/240 | 240/240 |
| token_only | 1.5 | en/single/POLARITY:NEGATIVE | 474/480 | 451/480 | 443/480 | 0.8% | 480/480 | 480/480 |
| token_only | 1.5 | en/single/POLARITY:POSITIVE | 472/480 | 441/480 | 435/480 | 1.4% | 480/480 | 480/480 |
| token_only | 1.5 | en/single/TIME:NOW | 472/480 | 440/480 | 434/480 | 1.0% | 480/480 | 480/480 |
| token_only | 1.5 | en/single/TIME:PAST | 468/480 | 442/480 | 435/480 | 1.1% | 480/480 | 480/480 |
| token_only | 1.5 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 234/240 | 224/240 | 221/240 | 1.2% | 240/240 | 240/240 |
| token_only | 1.5 | vi/single/POLARITY:NEGATIVE | 467/480 | 448/480 | 438/480 | 0.9% | 480/480 | 480/480 |
| token_only | 1.5 | vi/single/POLARITY:POSITIVE | 469/480 | 435/480 | 415/480 | 1.6% | 480/480 | 480/480 |
| token_only | 1.5 | vi/single/TIME:NOW | 462/480 | 438/480 | 413/480 | 1.7% | 480/480 | 480/480 |
| token_only | 1.5 | vi/single/TIME:PAST | 468/480 | 442/480 | 437/480 | 1.1% | 480/480 | 480/480 |

## Primary-mode validation diagnostics by seed

Counts below preserve the frozen seed-by-seed gate denominator. No generated or reference text is included.

| Source-copy weight | Seed | Bucket | Action fidelity | Preservation | Accepted references | CER | Unicode | EOS | Bucket gate |
|---:|---:|---|---:|---:|---:|---:|---:|---:|---|
| 0 | 17 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 79/80 | 79/80 | 78/80 | 0.6% | 80/80 | 80/80 | pass |
| 0 | 17 | en/single/POLARITY:NEGATIVE | 159/160 | 157/160 | 155/160 | 0.3% | 160/160 | 160/160 | pass |
| 0 | 17 | en/single/POLARITY:POSITIVE | 160/160 | 148/160 | 146/160 | 1.2% | 160/160 | 160/160 | pass |
| 0 | 17 | en/single/TIME:NOW | 159/160 | 148/160 | 148/160 | 0.8% | 160/160 | 160/160 | pass |
| 0 | 17 | en/single/TIME:PAST | 158/160 | 153/160 | 149/160 | 0.9% | 160/160 | 160/160 | pass |
| 0 | 17 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 80/80 | 73/80 | 72/80 | 1.2% | 80/80 | 80/80 | pass |
| 0 | 17 | vi/single/POLARITY:NEGATIVE | 159/160 | 141/160 | 140/160 | 2.7% | 160/160 | 160/160 | fail |
| 0 | 17 | vi/single/POLARITY:POSITIVE | 156/160 | 127/160 | 125/160 | 3.1% | 160/160 | 160/160 | fail |
| 0 | 17 | vi/single/TIME:NOW | 152/160 | 128/160 | 123/160 | 3.5% | 160/160 | 160/160 | fail |
| 0 | 17 | vi/single/TIME:PAST | 152/160 | 132/160 | 129/160 | 2.4% | 160/160 | 160/160 | fail |
| 0 | 23 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 79/80 | 71/80 | 66/80 | 1.4% | 80/80 | 80/80 | pass |
| 0 | 23 | en/single/POLARITY:NEGATIVE | 155/160 | 133/160 | 132/160 | 2.1% | 160/160 | 160/160 | fail |
| 0 | 23 | en/single/POLARITY:POSITIVE | 154/160 | 122/160 | 119/160 | 4.2% | 160/160 | 160/160 | fail |
| 0 | 23 | en/single/TIME:NOW | 156/160 | 132/160 | 126/160 | 2.0% | 160/160 | 160/160 | fail |
| 0 | 23 | en/single/TIME:PAST | 156/160 | 123/160 | 120/160 | 3.7% | 160/160 | 160/160 | fail |
| 0 | 23 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 79/80 | 71/80 | 71/80 | 1.0% | 80/80 | 80/80 | pass |
| 0 | 23 | vi/single/POLARITY:NEGATIVE | 153/160 | 127/160 | 121/160 | 2.7% | 160/160 | 160/160 | fail |
| 0 | 23 | vi/single/POLARITY:POSITIVE | 142/160 | 97/160 | 80/160 | 7.6% | 160/160 | 160/160 | fail |
| 0 | 23 | vi/single/TIME:NOW | 136/160 | 111/160 | 91/160 | 6.6% | 160/160 | 160/160 | fail |
| 0 | 23 | vi/single/TIME:PAST | 143/160 | 103/160 | 103/160 | 4.8% | 160/160 | 160/160 | fail |
| 0 | 41 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 79/80 | 74/80 | 72/80 | 1.1% | 80/80 | 80/80 | pass |
| 0 | 41 | en/single/POLARITY:NEGATIVE | 159/160 | 129/160 | 127/160 | 2.4% | 160/160 | 160/160 | fail |
| 0 | 41 | en/single/POLARITY:POSITIVE | 159/160 | 125/160 | 120/160 | 3.3% | 160/160 | 160/160 | fail |
| 0 | 41 | en/single/TIME:NOW | 153/160 | 123/160 | 118/160 | 3.6% | 160/160 | 160/160 | fail |
| 0 | 41 | en/single/TIME:PAST | 152/160 | 127/160 | 124/160 | 3.7% | 160/160 | 160/160 | fail |
| 0 | 41 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 80/80 | 74/80 | 72/80 | 1.1% | 80/80 | 80/80 | pass |
| 0 | 41 | vi/single/POLARITY:NEGATIVE | 150/160 | 128/160 | 124/160 | 3.3% | 160/160 | 160/160 | fail |
| 0 | 41 | vi/single/POLARITY:POSITIVE | 148/160 | 123/160 | 109/160 | 4.5% | 160/160 | 160/160 | fail |
| 0 | 41 | vi/single/TIME:NOW | 149/160 | 120/160 | 108/160 | 5.4% | 160/160 | 160/160 | fail |
| 0 | 41 | vi/single/TIME:PAST | 151/160 | 130/160 | 122/160 | 2.8% | 160/160 | 160/160 | fail |
| 1.5 | 17 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 80/80 | 79/80 | 79/80 | 0.2% | 80/80 | 80/80 | pass |
| 1.5 | 17 | en/single/POLARITY:NEGATIVE | 160/160 | 153/160 | 153/160 | 0.5% | 160/160 | 160/160 | pass |
| 1.5 | 17 | en/single/POLARITY:POSITIVE | 159/160 | 145/160 | 144/160 | 1.0% | 160/160 | 160/160 | pass |
| 1.5 | 17 | en/single/TIME:NOW | 160/160 | 153/160 | 153/160 | 0.4% | 160/160 | 160/160 | pass |
| 1.5 | 17 | en/single/TIME:PAST | 160/160 | 149/160 | 149/160 | 0.5% | 160/160 | 160/160 | pass |
| 1.5 | 17 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 80/80 | 79/80 | 78/80 | 0.2% | 80/80 | 80/80 | pass |
| 1.5 | 17 | vi/single/POLARITY:NEGATIVE | 158/160 | 156/160 | 152/160 | 1.2% | 160/160 | 160/160 | pass |
| 1.5 | 17 | vi/single/POLARITY:POSITIVE | 158/160 | 135/160 | 127/160 | 2.7% | 160/160 | 160/160 | fail |
| 1.5 | 17 | vi/single/TIME:NOW | 155/160 | 142/160 | 135/160 | 2.1% | 160/160 | 160/160 | fail |
| 1.5 | 17 | vi/single/TIME:PAST | 156/160 | 132/160 | 130/160 | 1.6% | 160/160 | 160/160 | fail |
| 1.5 | 23 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 79/80 | 71/80 | 70/80 | 1.6% | 80/80 | 80/80 | pass |
| 1.5 | 23 | en/single/POLARITY:NEGATIVE | 158/160 | 145/160 | 141/160 | 1.3% | 160/160 | 160/160 | pass |
| 1.5 | 23 | en/single/POLARITY:POSITIVE | 158/160 | 146/160 | 144/160 | 1.2% | 160/160 | 160/160 | pass |
| 1.5 | 23 | en/single/TIME:NOW | 159/160 | 154/160 | 149/160 | 0.5% | 160/160 | 160/160 | pass |
| 1.5 | 23 | en/single/TIME:PAST | 156/160 | 145/160 | 144/160 | 1.4% | 160/160 | 160/160 | pass |
| 1.5 | 23 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 79/80 | 75/80 | 74/80 | 0.5% | 80/80 | 80/80 | pass |
| 1.5 | 23 | vi/single/POLARITY:NEGATIVE | 159/160 | 150/160 | 150/160 | 0.6% | 160/160 | 160/160 | pass |
| 1.5 | 23 | vi/single/POLARITY:POSITIVE | 156/160 | 135/160 | 131/160 | 2.2% | 160/160 | 160/160 | fail |
| 1.5 | 23 | vi/single/TIME:NOW | 153/160 | 139/160 | 130/160 | 2.4% | 160/160 | 160/160 | fail |
| 1.5 | 23 | vi/single/TIME:PAST | 156/160 | 143/160 | 143/160 | 1.2% | 160/160 | 160/160 | fail |
| 1.5 | 41 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 79/80 | 79/80 | 78/80 | 0.2% | 80/80 | 80/80 | pass |
| 1.5 | 41 | en/single/POLARITY:NEGATIVE | 158/160 | 142/160 | 138/160 | 1.3% | 160/160 | 160/160 | fail |
| 1.5 | 41 | en/single/POLARITY:POSITIVE | 159/160 | 128/160 | 127/160 | 2.7% | 160/160 | 160/160 | fail |
| 1.5 | 41 | en/single/TIME:NOW | 158/160 | 132/160 | 131/160 | 1.8% | 160/160 | 160/160 | fail |
| 1.5 | 41 | en/single/TIME:PAST | 157/160 | 145/160 | 144/160 | 1.5% | 160/160 | 160/160 | pass |
| 1.5 | 41 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 77/80 | 70/80 | 67/80 | 2.3% | 80/80 | 80/80 | pass |
| 1.5 | 41 | vi/single/POLARITY:NEGATIVE | 152/160 | 129/160 | 124/160 | 3.1% | 160/160 | 160/160 | fail |
| 1.5 | 41 | vi/single/POLARITY:POSITIVE | 153/160 | 131/160 | 117/160 | 4.0% | 160/160 | 160/160 | fail |
| 1.5 | 41 | vi/single/TIME:NOW | 148/160 | 135/160 | 117/160 | 4.1% | 160/160 | 160/160 | fail |
| 1.5 | 41 | vi/single/TIME:PAST | 150/160 | 132/160 | 128/160 | 3.2% | 160/160 | 160/160 | fail |

## Limits and interpretation

Valid Unicode and EOS termination do not establish semantic correctness. The deterministic checker covers only the declared synthetic tense/polarity grammar and named roles. This benchmark tests recombination of familiar lexical factors; it does not establish naturalness, natural-corpus efficacy, or scientific efficacy. Control results are diagnostic; no TIDE advantage is claimed.

All examples and generated outputs remain private under Git-ignored `data/` and `runs/`. This report contains aggregate metrics only. `human_validated` is false. PhoMT raw/derived data and Phan Rang Cham data were not used.

Private aggregate evidence: `vi-en-ai-v4.12/protocol.json`, validation generation metrics under `vi-en-ai-v4.12`, and associated ignored run artifacts. Protocol SHA-256: `5cb47361a01969c0b115d3e4db8e6d7b52a4b7f0e7850439f7819d020c4bd92b`.
