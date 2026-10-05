# vi-en-ai-v4.11 Vi–En validation results

AI-authored and independently AI-reviewed preliminary synthetic pilot. **Not human/native-speaker validated.** PhoMT was not used. Phan Rang Cham remains excluded.

## Frozen protocol

The corpus has 7680 records and 192 event combinations. Split groups: 112/40/40; records: 4480/1600/1600 (train/validation/release holdout). Data split policy: 112 train, 40 validation, 40 release-holdout combinations (schema split label test) from three agents not used in prior pilot pools; every held-out factor pair is represented in training; English NOW uses present progressive.

Objective conditions: generic_jepa with source-copy weight 1.5; static_alignment with source-copy weight 1.5; tide with source-copy weight 1.5; token_only with source-copy weight 1.5. Seeds 17, 23, 41; 58 epochs and 3248 updates/config; width 48, 4 heads, 2 layers. Checkpoints selected using the frozen validation criterion. Decoder: greedy byte-level UTF-8 constrained decoding; EOS only at complete codepoint boundaries.

The registered primary objective is `tide`. Its engineering gate requires every configured primary weight, seed, and language/action bucket to meet the frozen thresholds.

## Validation result: **FAIL**

The release holdout was not evaluated and remains sealed.

| Mode | Source-copy weight | Seed | Val token CE | Val path token CE | Updates | Training wall seconds | Mean examples/sec | Gate |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| token_only | 1.5 | 17 | 0.0288 | 0.0239 | 3248 | 1505.4 | 172.8 | control_only |
| generic_jepa | 1.5 | 17 | 0.0564 | 0.0410 | 3248 | 1631.5 | 159.5 | control_only |
| static_alignment | 1.5 | 17 | 0.0155 | 0.0153 | 3248 | 1653.0 | 157.4 | control_only |
| tide | 1.5 | 17 | 0.0446 | 0.0388 | 3248 | 1640.0 | 158.6 | fail |
| token_only | 1.5 | 23 | 0.0165 | 0.0117 | 3248 | 1498.8 | 173.9 | control_only |
| generic_jepa | 1.5 | 23 | 0.0364 | 0.0286 | 3248 | 1643.3 | 158.3 | control_only |
| static_alignment | 1.5 | 23 | 0.0263 | 0.0280 | 3248 | 1655.0 | 157.2 | control_only |
| tide | 1.5 | 23 | 0.0299 | 0.0287 | 3248 | 1678.5 | 155.0 | fail |
| token_only | 1.5 | 41 | 0.0209 | 0.0179 | 3248 | 1519.3 | 171.4 | control_only |
| generic_jepa | 1.5 | 41 | 0.0644 | 0.0563 | 3248 | 1585.8 | 164.8 | control_only |
| static_alignment | 1.5 | 41 | 0.0259 | 0.0234 | 3248 | 1573.7 | 166.0 | control_only |
| tide | 1.5 | 41 | 0.0386 | 0.0227 | 3248 | 1569.5 | 166.9 | fail |

## Validation generation by condition and bucket

Action fidelity and preservation are pooled across seeds within each condition and bucket; thresholds are still checked for every primary condition/seed/bucket. Exact-reference match and CER are synthetic-reference metrics, not human naturalness.

| Mode | Source-copy weight | Bucket | Action fidelity | Preservation | Accepted references | CER | Unicode | EOS |
|---|---:|---|---:|---:|---:|---:|---:|---:|---|
| generic_jepa | 1.5 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 229/240 | 186/240 | 175/240 | 2.8% | 240/240 | 240/240 |
| generic_jepa | 1.5 | en/single/POLARITY:NEGATIVE | 462/480 | 358/480 | 340/480 | 3.4% | 480/480 | 480/480 |
| generic_jepa | 1.5 | en/single/POLARITY:POSITIVE | 466/480 | 308/480 | 289/480 | 5.2% | 480/480 | 480/480 |
| generic_jepa | 1.5 | en/single/TIME:NOW | 451/480 | 328/480 | 307/480 | 5.2% | 480/480 | 480/480 |
| generic_jepa | 1.5 | en/single/TIME:PAST | 450/480 | 305/480 | 285/480 | 5.5% | 480/480 | 480/480 |
| generic_jepa | 1.5 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 227/240 | 177/240 | 167/240 | 4.3% | 240/240 | 240/240 |
| generic_jepa | 1.5 | vi/single/POLARITY:NEGATIVE | 445/480 | 376/480 | 356/480 | 4.0% | 480/480 | 480/480 |
| generic_jepa | 1.5 | vi/single/POLARITY:POSITIVE | 428/480 | 359/480 | 328/480 | 5.0% | 480/480 | 480/480 |
| generic_jepa | 1.5 | vi/single/TIME:NOW | 413/480 | 374/480 | 321/480 | 5.8% | 480/480 | 480/480 |
| generic_jepa | 1.5 | vi/single/TIME:PAST | 423/480 | 346/480 | 331/480 | 5.0% | 480/480 | 480/480 |
| static_alignment | 1.5 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 237/240 | 216/240 | 208/240 | 1.4% | 240/240 | 240/240 |
| static_alignment | 1.5 | en/single/POLARITY:NEGATIVE | 468/480 | 403/480 | 389/480 | 2.2% | 480/480 | 480/480 |
| static_alignment | 1.5 | en/single/POLARITY:POSITIVE | 468/480 | 401/480 | 379/480 | 2.7% | 480/480 | 480/480 |
| static_alignment | 1.5 | en/single/TIME:NOW | 470/480 | 420/480 | 406/480 | 2.0% | 480/480 | 480/480 |
| static_alignment | 1.5 | en/single/TIME:PAST | 462/480 | 398/480 | 382/480 | 2.9% | 480/480 | 480/480 |
| static_alignment | 1.5 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 236/240 | 192/240 | 190/240 | 3.7% | 240/240 | 240/240 |
| static_alignment | 1.5 | vi/single/POLARITY:NEGATIVE | 471/480 | 384/480 | 376/480 | 3.4% | 480/480 | 480/480 |
| static_alignment | 1.5 | vi/single/POLARITY:POSITIVE | 463/480 | 381/480 | 362/480 | 3.9% | 480/480 | 480/480 |
| static_alignment | 1.5 | vi/single/TIME:NOW | 470/480 | 407/480 | 386/480 | 3.1% | 480/480 | 480/480 |
| static_alignment | 1.5 | vi/single/TIME:PAST | 453/480 | 389/480 | 379/480 | 3.7% | 480/480 | 480/480 |
| tide | 1.5 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 234/240 | 204/240 | 197/240 | 2.1% | 240/240 | 240/240 |
| tide | 1.5 | en/single/POLARITY:NEGATIVE | 461/480 | 384/480 | 370/480 | 2.7% | 480/480 | 480/480 |
| tide | 1.5 | en/single/POLARITY:POSITIVE | 458/480 | 350/480 | 335/480 | 4.5% | 480/480 | 480/480 |
| tide | 1.5 | en/single/TIME:NOW | 455/480 | 363/480 | 353/480 | 3.2% | 480/480 | 480/480 |
| tide | 1.5 | en/single/TIME:PAST | 449/480 | 339/480 | 327/480 | 5.0% | 480/480 | 480/480 |
| tide | 1.5 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 229/240 | 191/240 | 180/240 | 3.5% | 240/240 | 240/240 |
| tide | 1.5 | vi/single/POLARITY:NEGATIVE | 453/480 | 364/480 | 346/480 | 3.7% | 480/480 | 480/480 |
| tide | 1.5 | vi/single/POLARITY:POSITIVE | 426/480 | 334/480 | 299/480 | 6.0% | 480/480 | 480/480 |
| tide | 1.5 | vi/single/TIME:NOW | 405/480 | 354/480 | 298/480 | 6.8% | 480/480 | 480/480 |
| tide | 1.5 | vi/single/TIME:PAST | 410/480 | 315/480 | 303/480 | 6.2% | 480/480 | 480/480 |
| token_only | 1.5 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 231/240 | 217/240 | 202/240 | 1.8% | 240/240 | 240/240 |
| token_only | 1.5 | en/single/POLARITY:NEGATIVE | 465/480 | 397/480 | 381/480 | 2.3% | 480/480 | 480/480 |
| token_only | 1.5 | en/single/POLARITY:POSITIVE | 470/480 | 395/480 | 387/480 | 2.4% | 480/480 | 480/480 |
| token_only | 1.5 | en/single/TIME:NOW | 465/480 | 384/480 | 376/480 | 2.6% | 480/480 | 480/480 |
| token_only | 1.5 | en/single/TIME:PAST | 460/480 | 385/480 | 367/480 | 3.2% | 480/480 | 480/480 |
| token_only | 1.5 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 229/240 | 199/240 | 192/240 | 3.1% | 240/240 | 240/240 |
| token_only | 1.5 | vi/single/POLARITY:NEGATIVE | 473/480 | 403/480 | 389/480 | 2.8% | 480/480 | 480/480 |
| token_only | 1.5 | vi/single/POLARITY:POSITIVE | 460/480 | 412/480 | 388/480 | 2.8% | 480/480 | 480/480 |
| token_only | 1.5 | vi/single/TIME:NOW | 465/480 | 413/480 | 391/480 | 2.5% | 480/480 | 480/480 |
| token_only | 1.5 | vi/single/TIME:PAST | 462/480 | 407/480 | 388/480 | 2.3% | 480/480 | 480/480 |

## Primary-mode validation diagnostics by seed

Counts below preserve the frozen seed-by-seed gate denominator. No generated or reference text is included.

| Source-copy weight | Seed | Bucket | Action fidelity | Preservation | Accepted references | CER | Unicode | EOS | Bucket gate |
|---:|---:|---|---:|---:|---:|---:|---:|---:|---|
| 1.5 | 17 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 79/80 | 69/80 | 68/80 | 1.6% | 80/80 | 80/80 | pass |
| 1.5 | 17 | en/single/POLARITY:NEGATIVE | 152/160 | 127/160 | 122/160 | 2.6% | 160/160 | 160/160 | fail |
| 1.5 | 17 | en/single/POLARITY:POSITIVE | 150/160 | 118/160 | 111/160 | 4.2% | 160/160 | 160/160 | fail |
| 1.5 | 17 | en/single/TIME:NOW | 147/160 | 107/160 | 104/160 | 3.9% | 160/160 | 160/160 | fail |
| 1.5 | 17 | en/single/TIME:PAST | 153/160 | 120/160 | 118/160 | 3.4% | 160/160 | 160/160 | fail |
| 1.5 | 17 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 73/80 | 67/80 | 57/80 | 4.1% | 80/80 | 80/80 | pass |
| 1.5 | 17 | vi/single/POLARITY:NEGATIVE | 151/160 | 112/160 | 104/160 | 4.4% | 160/160 | 160/160 | fail |
| 1.5 | 17 | vi/single/POLARITY:POSITIVE | 151/160 | 102/160 | 89/160 | 6.6% | 160/160 | 160/160 | fail |
| 1.5 | 17 | vi/single/TIME:NOW | 135/160 | 110/160 | 90/160 | 7.7% | 160/160 | 160/160 | fail |
| 1.5 | 17 | vi/single/TIME:PAST | 144/160 | 103/160 | 96/160 | 6.4% | 160/160 | 160/160 | fail |
| 1.5 | 23 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 80/80 | 69/80 | 67/80 | 1.6% | 80/80 | 80/80 | pass |
| 1.5 | 23 | en/single/POLARITY:NEGATIVE | 156/160 | 135/160 | 129/160 | 1.8% | 160/160 | 160/160 | fail |
| 1.5 | 23 | en/single/POLARITY:POSITIVE | 154/160 | 128/160 | 123/160 | 3.4% | 160/160 | 160/160 | fail |
| 1.5 | 23 | en/single/TIME:NOW | 157/160 | 131/160 | 128/160 | 2.6% | 160/160 | 160/160 | fail |
| 1.5 | 23 | en/single/TIME:PAST | 155/160 | 124/160 | 119/160 | 3.9% | 160/160 | 160/160 | fail |
| 1.5 | 23 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 78/80 | 62/80 | 62/80 | 3.3% | 80/80 | 80/80 | fail |
| 1.5 | 23 | vi/single/POLARITY:NEGATIVE | 155/160 | 132/160 | 129/160 | 2.5% | 160/160 | 160/160 | fail |
| 1.5 | 23 | vi/single/POLARITY:POSITIVE | 147/160 | 130/160 | 124/160 | 4.0% | 160/160 | 160/160 | fail |
| 1.5 | 23 | vi/single/TIME:NOW | 149/160 | 134/160 | 126/160 | 3.2% | 160/160 | 160/160 | fail |
| 1.5 | 23 | vi/single/TIME:PAST | 151/160 | 121/160 | 118/160 | 4.2% | 160/160 | 160/160 | fail |
| 1.5 | 41 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 75/80 | 66/80 | 62/80 | 3.1% | 80/80 | 80/80 | pass |
| 1.5 | 41 | en/single/POLARITY:NEGATIVE | 153/160 | 122/160 | 119/160 | 3.7% | 160/160 | 160/160 | fail |
| 1.5 | 41 | en/single/POLARITY:POSITIVE | 154/160 | 104/160 | 101/160 | 5.9% | 160/160 | 160/160 | fail |
| 1.5 | 41 | en/single/TIME:NOW | 151/160 | 125/160 | 121/160 | 3.0% | 160/160 | 160/160 | fail |
| 1.5 | 41 | en/single/TIME:PAST | 141/160 | 95/160 | 90/160 | 7.6% | 160/160 | 160/160 | fail |
| 1.5 | 41 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 78/80 | 62/80 | 61/80 | 3.0% | 80/80 | 80/80 | fail |
| 1.5 | 41 | vi/single/POLARITY:NEGATIVE | 147/160 | 120/160 | 113/160 | 4.1% | 160/160 | 160/160 | fail |
| 1.5 | 41 | vi/single/POLARITY:POSITIVE | 128/160 | 102/160 | 86/160 | 7.3% | 160/160 | 160/160 | fail |
| 1.5 | 41 | vi/single/TIME:NOW | 121/160 | 110/160 | 82/160 | 9.5% | 160/160 | 160/160 | fail |
| 1.5 | 41 | vi/single/TIME:PAST | 115/160 | 91/160 | 89/160 | 8.1% | 160/160 | 160/160 | fail |

## Limits and interpretation

Valid Unicode and EOS termination do not establish semantic correctness. The deterministic checker covers only the declared synthetic tense/polarity grammar and named roles. This benchmark tests recombination of familiar lexical factors; it does not establish naturalness, natural-corpus efficacy, or scientific efficacy. Control results are diagnostic; no TIDE advantage is claimed.

All examples and generated outputs remain private under Git-ignored `data/` and `runs/`. This report contains aggregate metrics only. `human_validated` is false. PhoMT raw/derived data and Phan Rang Cham data were not used.

Private aggregate evidence: `vi-en-ai-v4.11/protocol.json`, validation generation metrics under `vi-en-ai-v4.11`, and associated ignored run artifacts. Protocol SHA-256: `4fcbfc16c9398939193f03b1a16eb05eefb48e397404e02a82213d0bee109ad5`.
