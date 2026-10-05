# vi-en-ai-v4.16 Vi–En validation results

AI-authored and independently AI-reviewed preliminary synthetic pilot. **Not human/native-speaker validated.** PhoMT was not used. Phan Rang Cham remains excluded.

## Frozen protocol

The corpus has 15360 records and 192 event combinations. Split groups: 112/40/40; records: 8960/3200/3200 (train/validation/release holdout). Data split policy: 112 train, 40 validation, 40 release-holdout combinations from three fresh agent factors; every held-out factor pair is represented in training; English NOW uses present progressive; four context-balanced surface realizations per meaning state; fresh split and sealed holdout for a lower latent-objective-dose study. Transition weighting: There are 3072 duplicated path-step rows across the full split: 1792 in training, 640 in validation, and 640 in the sealed release holdout. Each logical path-step transition has one standalone single-edge record and one path-linked record. In training this adds 1792 record exposures, so those path-selected transitions contribute twice the row-wise token/edge exposure. Validation and holdout duplicates are evaluation records, not training exposure. The representation is fixed identically across conditions; results describe a path-enriched training distribution, not uniform weighting over unique transitions.

Objective conditions: tide with source-copy weight 1.5 and TIDE latent-objective multiplier 0.1; tide with source-copy weight 1.5 and TIDE latent-objective multiplier 0.25; token_only with source-copy weight 1.5. Seeds 17, 23, 41; 29 epochs and 3248 updates/config; width 48, 4 heads, 2 layers. Checkpoints selected using the frozen validation criterion. Decoder: greedy byte-level UTF-8 constrained decoding; EOS only at complete codepoint boundaries.

The registered primary objective is `tide`. Its engineering gate requires every configured primary weight, seed, and language/action bucket to meet the frozen thresholds.

## Validation result: **FAIL**

The release holdout was not evaluated and remains sealed.

| Mode | Source-copy weight | TIDE aux multiplier | Seed | Val token CE | Val path token CE | Updates | Training wall seconds | Mean examples/sec | Gate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| token_only | 1.5 | — | 17 | 0.0273 | 0.0227 | 3248 | 1910.8 | 136.1 | control_only |
| tide | 1.5 | 0.1 | 17 | 0.0337 | 0.0225 | 3248 | 2139.5 | 121.5 | fail |
| tide | 1.5 | 0.25 | 17 | 0.0308 | 0.0169 | 3248 | 2142.9 | 121.4 | fail |
| token_only | 1.5 | — | 23 | 0.0321 | 0.0236 | 3248 | 1932.5 | 134.6 | control_only |
| tide | 1.5 | 0.1 | 23 | 0.0406 | 0.0286 | 3248 | 2179.0 | 119.4 | fail |
| tide | 1.5 | 0.25 | 23 | 0.0387 | 0.0200 | 3248 | 2177.1 | 119.5 | fail |
| token_only | 1.5 | — | 41 | 0.0415 | 0.0327 | 3248 | 1933.0 | 134.6 | control_only |
| tide | 1.5 | 0.1 | 41 | 0.0365 | 0.0236 | 3248 | 2105.3 | 124.6 | fail |
| tide | 1.5 | 0.25 | 41 | 0.0330 | 0.0164 | 3248 | 1477.7 | 176.5 | fail |

## Validation generation by condition and bucket

Action fidelity and preservation are pooled across seeds within each condition and bucket; thresholds are still checked for every primary condition/seed/bucket. Exact-reference match and CER are synthetic-reference metrics, not human naturalness.

| Mode | Source-copy weight | TIDE aux multiplier | Bucket | Action fidelity | Preservation | Accepted references | CER | Unicode | EOS |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---|
| tide | 1.5 | 0.1 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 469/480 | 334/480 | 320/480 | 2.2% | 480/480 | 480/480 |
| tide | 1.5 | 0.1 | en/single/POLARITY:NEGATIVE | 904/960 | 537/960 | 514/960 | 3.8% | 960/960 | 960/960 |
| tide | 1.5 | 0.1 | en/single/POLARITY:POSITIVE | 926/960 | 396/960 | 369/960 | 5.6% | 960/960 | 960/960 |
| tide | 1.5 | 0.1 | en/single/TIME:NOW | 907/960 | 445/960 | 423/960 | 4.7% | 960/960 | 960/960 |
| tide | 1.5 | 0.1 | en/single/TIME:PAST | 847/960 | 396/960 | 369/960 | 6.5% | 960/960 | 960/960 |
| tide | 1.5 | 0.1 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 468/480 | 402/480 | 398/480 | 1.9% | 480/480 | 480/480 |
| tide | 1.5 | 0.1 | vi/single/POLARITY:NEGATIVE | 891/960 | 735/960 | 732/960 | 2.4% | 960/960 | 960/960 |
| tide | 1.5 | 0.1 | vi/single/POLARITY:POSITIVE | 827/960 | 619/960 | 606/960 | 4.1% | 960/960 | 960/960 |
| tide | 1.5 | 0.1 | vi/single/TIME:NOW | 927/960 | 713/960 | 693/960 | 3.3% | 960/960 | 960/960 |
| tide | 1.5 | 0.1 | vi/single/TIME:PAST | 832/960 | 696/960 | 688/960 | 3.0% | 960/960 | 960/960 |
| tide | 1.5 | 0.25 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 434/480 | 319/480 | 304/480 | 3.0% | 480/480 | 480/480 |
| tide | 1.5 | 0.25 | en/single/POLARITY:NEGATIVE | 833/960 | 490/960 | 464/960 | 4.9% | 960/960 | 960/960 |
| tide | 1.5 | 0.25 | en/single/POLARITY:POSITIVE | 922/960 | 383/960 | 355/960 | 6.6% | 960/960 | 960/960 |
| tide | 1.5 | 0.25 | en/single/TIME:NOW | 854/960 | 359/960 | 329/960 | 7.7% | 960/960 | 960/960 |
| tide | 1.5 | 0.25 | en/single/TIME:PAST | 824/960 | 423/960 | 391/960 | 7.3% | 960/960 | 960/960 |
| tide | 1.5 | 0.25 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 468/480 | 415/480 | 409/480 | 1.6% | 480/480 | 480/480 |
| tide | 1.5 | 0.25 | vi/single/POLARITY:NEGATIVE | 867/960 | 752/960 | 741/960 | 2.5% | 960/960 | 960/960 |
| tide | 1.5 | 0.25 | vi/single/POLARITY:POSITIVE | 798/960 | 617/960 | 579/960 | 4.5% | 960/960 | 960/960 |
| tide | 1.5 | 0.25 | vi/single/TIME:NOW | 895/960 | 699/960 | 657/960 | 4.2% | 960/960 | 960/960 |
| tide | 1.5 | 0.25 | vi/single/TIME:PAST | 781/960 | 691/960 | 683/960 | 2.9% | 960/960 | 960/960 |
| token_only | 1.5 | — | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 440/480 | 301/480 | 285/480 | 3.1% | 480/480 | 480/480 |
| token_only | 1.5 | — | en/single/POLARITY:NEGATIVE | 881/960 | 548/960 | 514/960 | 3.5% | 960/960 | 960/960 |
| token_only | 1.5 | — | en/single/POLARITY:POSITIVE | 903/960 | 388/960 | 362/960 | 5.7% | 960/960 | 960/960 |
| token_only | 1.5 | — | en/single/TIME:NOW | 875/960 | 487/960 | 454/960 | 4.5% | 960/960 | 960/960 |
| token_only | 1.5 | — | en/single/TIME:PAST | 819/960 | 403/960 | 380/960 | 6.5% | 960/960 | 960/960 |
| token_only | 1.5 | — | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 466/480 | 395/480 | 391/480 | 1.9% | 480/480 | 480/480 |
| token_only | 1.5 | — | vi/single/POLARITY:NEGATIVE | 927/960 | 773/960 | 757/960 | 2.5% | 960/960 | 960/960 |
| token_only | 1.5 | — | vi/single/POLARITY:POSITIVE | 887/960 | 696/960 | 671/960 | 3.4% | 960/960 | 960/960 |
| token_only | 1.5 | — | vi/single/TIME:NOW | 910/960 | 756/960 | 727/960 | 4.0% | 960/960 | 960/960 |
| token_only | 1.5 | — | vi/single/TIME:PAST | 814/960 | 684/960 | 667/960 | 3.3% | 960/960 | 960/960 |

## Primary-mode validation diagnostics by seed

Counts below preserve the frozen seed-by-seed gate denominator. No generated or reference text is included.

| Source-copy weight | TIDE aux multiplier | Seed | Bucket | Action fidelity | Preservation | Accepted references | CER | Unicode | EOS | Bucket gate |
|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---|
| 1.5 | 0.1 | 17 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 158/160 | 118/160 | 118/160 | 1.4% | 160/160 | 160/160 | fail |
| 1.5 | 0.1 | 17 | en/single/POLARITY:NEGATIVE | 311/320 | 186/320 | 184/320 | 3.5% | 320/320 | 320/320 | fail |
| 1.5 | 0.1 | 17 | en/single/POLARITY:POSITIVE | 310/320 | 159/320 | 149/320 | 4.6% | 320/320 | 320/320 | fail |
| 1.5 | 0.1 | 17 | en/single/TIME:NOW | 303/320 | 131/320 | 129/320 | 5.1% | 320/320 | 320/320 | fail |
| 1.5 | 0.1 | 17 | en/single/TIME:PAST | 296/320 | 166/320 | 165/320 | 4.7% | 320/320 | 320/320 | fail |
| 1.5 | 0.1 | 17 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 158/160 | 132/160 | 129/160 | 2.1% | 160/160 | 160/160 | pass |
| 1.5 | 0.1 | 17 | vi/single/POLARITY:NEGATIVE | 301/320 | 229/320 | 228/320 | 2.6% | 320/320 | 320/320 | fail |
| 1.5 | 0.1 | 17 | vi/single/POLARITY:POSITIVE | 280/320 | 219/320 | 215/320 | 3.8% | 320/320 | 320/320 | fail |
| 1.5 | 0.1 | 17 | vi/single/TIME:NOW | 310/320 | 241/320 | 231/320 | 2.7% | 320/320 | 320/320 | fail |
| 1.5 | 0.1 | 17 | vi/single/TIME:PAST | 290/320 | 244/320 | 237/320 | 2.8% | 320/320 | 320/320 | fail |
| 1.5 | 0.1 | 23 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 155/160 | 110/160 | 103/160 | 2.5% | 160/160 | 160/160 | fail |
| 1.5 | 0.1 | 23 | en/single/POLARITY:NEGATIVE | 309/320 | 167/320 | 162/320 | 3.9% | 320/320 | 320/320 | fail |
| 1.5 | 0.1 | 23 | en/single/POLARITY:POSITIVE | 310/320 | 111/320 | 104/320 | 5.7% | 320/320 | 320/320 | fail |
| 1.5 | 0.1 | 23 | en/single/TIME:NOW | 307/320 | 150/320 | 148/320 | 4.4% | 320/320 | 320/320 | fail |
| 1.5 | 0.1 | 23 | en/single/TIME:PAST | 279/320 | 116/320 | 105/320 | 7.0% | 320/320 | 320/320 | fail |
| 1.5 | 0.1 | 23 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 151/160 | 129/160 | 129/160 | 2.3% | 160/160 | 160/160 | pass |
| 1.5 | 0.1 | 23 | vi/single/POLARITY:NEGATIVE | 274/320 | 219/320 | 217/320 | 3.8% | 320/320 | 320/320 | fail |
| 1.5 | 0.1 | 23 | vi/single/POLARITY:POSITIVE | 246/320 | 151/320 | 145/320 | 6.3% | 320/320 | 320/320 | fail |
| 1.5 | 0.1 | 23 | vi/single/TIME:NOW | 300/320 | 206/320 | 199/320 | 5.3% | 320/320 | 320/320 | fail |
| 1.5 | 0.1 | 23 | vi/single/TIME:PAST | 246/320 | 185/320 | 185/320 | 4.8% | 320/320 | 320/320 | fail |
| 1.5 | 0.1 | 41 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 156/160 | 106/160 | 99/160 | 2.7% | 160/160 | 160/160 | fail |
| 1.5 | 0.1 | 41 | en/single/POLARITY:NEGATIVE | 284/320 | 184/320 | 168/320 | 4.0% | 320/320 | 320/320 | fail |
| 1.5 | 0.1 | 41 | en/single/POLARITY:POSITIVE | 306/320 | 126/320 | 116/320 | 6.5% | 320/320 | 320/320 | fail |
| 1.5 | 0.1 | 41 | en/single/TIME:NOW | 297/320 | 164/320 | 146/320 | 4.5% | 320/320 | 320/320 | fail |
| 1.5 | 0.1 | 41 | en/single/TIME:PAST | 272/320 | 114/320 | 99/320 | 7.8% | 320/320 | 320/320 | fail |
| 1.5 | 0.1 | 41 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 159/160 | 141/160 | 140/160 | 1.2% | 160/160 | 160/160 | pass |
| 1.5 | 0.1 | 41 | vi/single/POLARITY:NEGATIVE | 316/320 | 287/320 | 287/320 | 0.9% | 320/320 | 320/320 | fail |
| 1.5 | 0.1 | 41 | vi/single/POLARITY:POSITIVE | 301/320 | 249/320 | 246/320 | 2.1% | 320/320 | 320/320 | fail |
| 1.5 | 0.1 | 41 | vi/single/TIME:NOW | 317/320 | 266/320 | 263/320 | 1.9% | 320/320 | 320/320 | fail |
| 1.5 | 0.1 | 41 | vi/single/TIME:PAST | 296/320 | 267/320 | 266/320 | 1.5% | 320/320 | 320/320 | fail |
| 1.5 | 0.25 | 17 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 158/160 | 110/160 | 109/160 | 3.2% | 160/160 | 160/160 | fail |
| 1.5 | 0.25 | 17 | en/single/POLARITY:NEGATIVE | 294/320 | 154/320 | 150/320 | 6.1% | 320/320 | 320/320 | fail |
| 1.5 | 0.25 | 17 | en/single/POLARITY:POSITIVE | 306/320 | 127/320 | 111/320 | 8.4% | 320/320 | 320/320 | fail |
| 1.5 | 0.25 | 17 | en/single/TIME:NOW | 278/320 | 109/320 | 96/320 | 10.3% | 320/320 | 320/320 | fail |
| 1.5 | 0.25 | 17 | en/single/TIME:PAST | 288/320 | 148/320 | 133/320 | 8.2% | 320/320 | 320/320 | fail |
| 1.5 | 0.25 | 17 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 154/160 | 136/160 | 131/160 | 2.1% | 160/160 | 160/160 | pass |
| 1.5 | 0.25 | 17 | vi/single/POLARITY:NEGATIVE | 306/320 | 267/320 | 263/320 | 1.8% | 320/320 | 320/320 | fail |
| 1.5 | 0.25 | 17 | vi/single/POLARITY:POSITIVE | 306/320 | 271/320 | 252/320 | 2.5% | 320/320 | 320/320 | fail |
| 1.5 | 0.25 | 17 | vi/single/TIME:NOW | 300/320 | 259/320 | 239/320 | 3.4% | 320/320 | 320/320 | fail |
| 1.5 | 0.25 | 17 | vi/single/TIME:PAST | 292/320 | 256/320 | 251/320 | 2.4% | 320/320 | 320/320 | fail |
| 1.5 | 0.25 | 23 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 148/160 | 99/160 | 90/160 | 3.3% | 160/160 | 160/160 | fail |
| 1.5 | 0.25 | 23 | en/single/POLARITY:NEGATIVE | 287/320 | 171/320 | 158/320 | 3.9% | 320/320 | 320/320 | fail |
| 1.5 | 0.25 | 23 | en/single/POLARITY:POSITIVE | 310/320 | 116/320 | 112/320 | 5.6% | 320/320 | 320/320 | fail |
| 1.5 | 0.25 | 23 | en/single/TIME:NOW | 289/320 | 118/320 | 112/320 | 5.6% | 320/320 | 320/320 | fail |
| 1.5 | 0.25 | 23 | en/single/TIME:PAST | 263/320 | 115/320 | 110/320 | 7.5% | 320/320 | 320/320 | fail |
| 1.5 | 0.25 | 23 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 159/160 | 145/160 | 145/160 | 0.9% | 160/160 | 160/160 | pass |
| 1.5 | 0.25 | 23 | vi/single/POLARITY:NEGATIVE | 311/320 | 278/320 | 274/320 | 1.5% | 320/320 | 320/320 | fail |
| 1.5 | 0.25 | 23 | vi/single/POLARITY:POSITIVE | 276/320 | 225/320 | 211/320 | 3.4% | 320/320 | 320/320 | fail |
| 1.5 | 0.25 | 23 | vi/single/TIME:NOW | 304/320 | 259/320 | 249/320 | 2.4% | 320/320 | 320/320 | fail |
| 1.5 | 0.25 | 23 | vi/single/TIME:PAST | 255/320 | 225/320 | 223/320 | 2.6% | 320/320 | 320/320 | fail |
| 1.5 | 0.25 | 41 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 128/160 | 110/160 | 105/160 | 2.6% | 160/160 | 160/160 | fail |
| 1.5 | 0.25 | 41 | en/single/POLARITY:NEGATIVE | 252/320 | 165/320 | 156/320 | 4.6% | 320/320 | 320/320 | fail |
| 1.5 | 0.25 | 41 | en/single/POLARITY:POSITIVE | 306/320 | 140/320 | 132/320 | 5.7% | 320/320 | 320/320 | fail |
| 1.5 | 0.25 | 41 | en/single/TIME:NOW | 287/320 | 132/320 | 121/320 | 7.2% | 320/320 | 320/320 | fail |
| 1.5 | 0.25 | 41 | en/single/TIME:PAST | 273/320 | 160/320 | 148/320 | 6.3% | 320/320 | 320/320 | fail |
| 1.5 | 0.25 | 41 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 155/160 | 134/160 | 133/160 | 1.7% | 160/160 | 160/160 | pass |
| 1.5 | 0.25 | 41 | vi/single/POLARITY:NEGATIVE | 250/320 | 207/320 | 204/320 | 4.1% | 320/320 | 320/320 | fail |
| 1.5 | 0.25 | 41 | vi/single/POLARITY:POSITIVE | 216/320 | 121/320 | 116/320 | 7.5% | 320/320 | 320/320 | fail |
| 1.5 | 0.25 | 41 | vi/single/TIME:NOW | 291/320 | 181/320 | 169/320 | 6.9% | 320/320 | 320/320 | fail |
| 1.5 | 0.25 | 41 | vi/single/TIME:PAST | 234/320 | 210/320 | 209/320 | 3.5% | 320/320 | 320/320 | fail |

## Limits and interpretation

Valid Unicode and EOS termination do not establish semantic correctness. The deterministic checker covers only the declared synthetic tense/polarity grammar and named roles. This benchmark tests recombination of familiar lexical factors; it does not establish naturalness, natural-corpus efficacy, or scientific efficacy. Control results are diagnostic; no TIDE advantage is claimed.

All examples and generated outputs remain private under Git-ignored `data/` and `runs/`. This report contains aggregate metrics only. `human_validated` is false. PhoMT raw/derived data and Phan Rang Cham data were not used.

Private aggregate evidence: `vi-en-ai-v4.16-r2/protocol.json`, validation generation metrics under `vi-en-ai-v4.16-r2`, and associated ignored run artifacts. Protocol SHA-256: `f24214a9582268b0ccea2a5547a79b46aefdfcad48d0ca894de2c06df9338dc0`.
