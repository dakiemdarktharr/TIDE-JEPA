# vi-en-ai-v4.14 Vi–En validation results

AI-authored and independently AI-reviewed preliminary synthetic pilot. **Not human/native-speaker validated.** PhoMT was not used. Phan Rang Cham remains excluded.

## Frozen protocol

The corpus has 15360 records and 192 event combinations. Split groups: 112/40/40; records: 8960/3200/3200 (train/validation/release holdout). Data split policy: 112 train, 40 validation, 40 release-holdout combinations from three fresh agent factors; every held-out factor pair is represented in training; English NOW uses present progressive; four context-balanced surface realizations per meaning state; fresh sealed holdout for an exposure-diversity test.

Objective conditions: tide with source-copy weight 1.5; token_only with source-copy weight 1.5. Seeds 17, 23, 41; 29 epochs and 3248 updates/config; width 48, 4 heads, 2 layers. Checkpoints selected using the frozen validation criterion. Decoder: greedy byte-level UTF-8 constrained decoding; EOS only at complete codepoint boundaries.

The registered primary objective is `tide`. Its engineering gate requires every configured primary weight, seed, and language/action bucket to meet the frozen thresholds.

## Validation result: **FAIL**

The release holdout was not evaluated and remains sealed.

| Mode | Source-copy weight | Seed | Val token CE | Val path token CE | Updates | Training wall seconds | Mean examples/sec | Gate |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| token_only | 1.5 | 17 | 0.0146 | 0.0078 | 3248 | 1921.8 | 135.3 | control_only |
| tide | 1.5 | 17 | 0.0586 | 0.0441 | 3248 | 2153.9 | 120.7 | fail |
| token_only | 1.5 | 23 | 0.0113 | 0.0067 | 3248 | 1900.6 | 136.8 | control_only |
| tide | 1.5 | 23 | 0.0406 | 0.0256 | 3248 | 2120.4 | 122.6 | fail |
| token_only | 1.5 | 41 | 0.0257 | 0.0161 | 3248 | 1487.6 | 176.3 | control_only |
| tide | 1.5 | 41 | 0.0302 | 0.0129 | 3248 | 1669.6 | 157.4 | fail |

## Validation generation by condition and bucket

Action fidelity and preservation are pooled across seeds within each condition and bucket; thresholds are still checked for every primary condition/seed/bucket. Exact-reference match and CER are synthetic-reference metrics, not human naturalness.

| Mode | Source-copy weight | Bucket | Action fidelity | Preservation | Accepted references | CER | Unicode | EOS |
|---|---:|---|---:|---:|---:|---:|---:|---:|---|
| tide | 1.5 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 475/480 | 449/480 | 447/480 | 1.1% | 480/480 | 480/480 |
| tide | 1.5 | en/single/POLARITY:NEGATIVE | 935/960 | 804/960 | 796/960 | 1.8% | 960/960 | 960/960 |
| tide | 1.5 | en/single/POLARITY:POSITIVE | 917/960 | 672/960 | 650/960 | 4.0% | 960/960 | 960/960 |
| tide | 1.5 | en/single/TIME:NOW | 829/960 | 636/960 | 618/960 | 5.7% | 960/960 | 960/960 |
| tide | 1.5 | en/single/TIME:PAST | 932/960 | 783/960 | 764/960 | 2.5% | 960/960 | 960/960 |
| tide | 1.5 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 453/480 | 351/480 | 330/480 | 3.8% | 480/480 | 480/480 |
| tide | 1.5 | vi/single/POLARITY:NEGATIVE | 876/960 | 613/960 | 578/960 | 4.7% | 960/960 | 960/960 |
| tide | 1.5 | vi/single/POLARITY:POSITIVE | 690/960 | 420/960 | 368/960 | 9.8% | 960/960 | 960/960 |
| tide | 1.5 | vi/single/TIME:NOW | 808/960 | 542/960 | 460/960 | 7.2% | 960/960 | 960/960 |
| tide | 1.5 | vi/single/TIME:PAST | 659/960 | 513/960 | 491/960 | 6.8% | 960/960 | 960/960 |
| token_only | 1.5 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 480/480 | 479/480 | 479/480 | 0.0% | 480/480 | 480/480 |
| token_only | 1.5 | en/single/POLARITY:NEGATIVE | 946/960 | 918/960 | 915/960 | 0.4% | 960/960 | 960/960 |
| token_only | 1.5 | en/single/POLARITY:POSITIVE | 955/960 | 854/960 | 852/960 | 1.1% | 960/960 | 960/960 |
| token_only | 1.5 | en/single/TIME:NOW | 943/960 | 855/960 | 846/960 | 1.1% | 960/960 | 960/960 |
| token_only | 1.5 | en/single/TIME:PAST | 927/960 | 857/960 | 850/960 | 1.4% | 960/960 | 960/960 |
| token_only | 1.5 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 464/480 | 403/480 | 385/480 | 2.6% | 480/480 | 480/480 |
| token_only | 1.5 | vi/single/POLARITY:NEGATIVE | 920/960 | 763/960 | 720/960 | 3.5% | 960/960 | 960/960 |
| token_only | 1.5 | vi/single/POLARITY:POSITIVE | 870/960 | 665/960 | 595/960 | 5.2% | 960/960 | 960/960 |
| token_only | 1.5 | vi/single/TIME:NOW | 879/960 | 721/960 | 624/960 | 5.0% | 960/960 | 960/960 |
| token_only | 1.5 | vi/single/TIME:PAST | 767/960 | 650/960 | 607/960 | 4.4% | 960/960 | 960/960 |

## Primary-mode validation diagnostics by seed

Counts below preserve the frozen seed-by-seed gate denominator. No generated or reference text is included.

| Source-copy weight | Seed | Bucket | Action fidelity | Preservation | Accepted references | CER | Unicode | EOS | Bucket gate |
|---:|---:|---|---:|---:|---:|---:|---:|---:|---|
| 1.5 | 17 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 159/160 | 155/160 | 154/160 | 0.3% | 160/160 | 160/160 | pass |
| 1.5 | 17 | en/single/POLARITY:NEGATIVE | 311/320 | 285/320 | 285/320 | 1.0% | 320/320 | 320/320 | fail |
| 1.5 | 17 | en/single/POLARITY:POSITIVE | 310/320 | 250/320 | 243/320 | 2.5% | 320/320 | 320/320 | fail |
| 1.5 | 17 | en/single/TIME:NOW | 314/320 | 268/320 | 264/320 | 1.2% | 320/320 | 320/320 | fail |
| 1.5 | 17 | en/single/TIME:PAST | 319/320 | 284/320 | 283/320 | 1.0% | 320/320 | 320/320 | fail |
| 1.5 | 17 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 143/160 | 109/160 | 99/160 | 5.5% | 160/160 | 160/160 | fail |
| 1.5 | 17 | vi/single/POLARITY:NEGATIVE | 266/320 | 193/320 | 179/320 | 5.8% | 320/320 | 320/320 | fail |
| 1.5 | 17 | vi/single/POLARITY:POSITIVE | 215/320 | 117/320 | 105/320 | 10.6% | 320/320 | 320/320 | fail |
| 1.5 | 17 | vi/single/TIME:NOW | 265/320 | 171/320 | 142/320 | 7.8% | 320/320 | 320/320 | fail |
| 1.5 | 17 | vi/single/TIME:PAST | 199/320 | 147/320 | 141/320 | 8.1% | 320/320 | 320/320 | fail |
| 1.5 | 23 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 159/160 | 151/160 | 151/160 | 0.5% | 160/160 | 160/160 | pass |
| 1.5 | 23 | en/single/POLARITY:NEGATIVE | 317/320 | 263/320 | 263/320 | 1.8% | 320/320 | 320/320 | fail |
| 1.5 | 23 | en/single/POLARITY:POSITIVE | 315/320 | 254/320 | 251/320 | 2.2% | 320/320 | 320/320 | fail |
| 1.5 | 23 | en/single/TIME:NOW | 309/320 | 247/320 | 241/320 | 2.7% | 320/320 | 320/320 | fail |
| 1.5 | 23 | en/single/TIME:PAST | 309/320 | 267/320 | 266/320 | 2.0% | 320/320 | 320/320 | fail |
| 1.5 | 23 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 153/160 | 112/160 | 105/160 | 4.2% | 160/160 | 160/160 | fail |
| 1.5 | 23 | vi/single/POLARITY:NEGATIVE | 298/320 | 206/320 | 195/320 | 4.7% | 320/320 | 320/320 | fail |
| 1.5 | 23 | vi/single/POLARITY:POSITIVE | 188/320 | 116/320 | 98/320 | 11.6% | 320/320 | 320/320 | fail |
| 1.5 | 23 | vi/single/TIME:NOW | 270/320 | 168/320 | 146/320 | 7.8% | 320/320 | 320/320 | fail |
| 1.5 | 23 | vi/single/TIME:PAST | 193/320 | 163/320 | 154/320 | 7.7% | 320/320 | 320/320 | fail |
| 1.5 | 41 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 157/160 | 143/160 | 142/160 | 2.3% | 160/160 | 160/160 | pass |
| 1.5 | 41 | en/single/POLARITY:NEGATIVE | 307/320 | 256/320 | 248/320 | 2.7% | 320/320 | 320/320 | fail |
| 1.5 | 41 | en/single/POLARITY:POSITIVE | 292/320 | 168/320 | 156/320 | 7.3% | 320/320 | 320/320 | fail |
| 1.5 | 41 | en/single/TIME:NOW | 206/320 | 121/320 | 113/320 | 13.2% | 320/320 | 320/320 | fail |
| 1.5 | 41 | en/single/TIME:PAST | 304/320 | 232/320 | 215/320 | 4.6% | 320/320 | 320/320 | fail |
| 1.5 | 41 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 157/160 | 130/160 | 126/160 | 1.6% | 160/160 | 160/160 | pass |
| 1.5 | 41 | vi/single/POLARITY:NEGATIVE | 312/320 | 214/320 | 204/320 | 3.5% | 320/320 | 320/320 | fail |
| 1.5 | 41 | vi/single/POLARITY:POSITIVE | 287/320 | 187/320 | 165/320 | 7.1% | 320/320 | 320/320 | fail |
| 1.5 | 41 | vi/single/TIME:NOW | 273/320 | 203/320 | 172/320 | 5.9% | 320/320 | 320/320 | fail |
| 1.5 | 41 | vi/single/TIME:PAST | 267/320 | 203/320 | 196/320 | 4.7% | 320/320 | 320/320 | fail |

## Limits and interpretation

Valid Unicode and EOS termination do not establish semantic correctness. The deterministic checker covers only the declared synthetic tense/polarity grammar and named roles. This benchmark tests recombination of familiar lexical factors; it does not establish naturalness, natural-corpus efficacy, or scientific efficacy. Control results are diagnostic; no TIDE advantage is claimed.

All examples and generated outputs remain private under Git-ignored `data/` and `runs/`. This report contains aggregate metrics only. `human_validated` is false. PhoMT raw/derived data and Phan Rang Cham data were not used.

Private aggregate evidence: `vi-en-ai-v4.14-r1/protocol.json`, validation generation metrics under `vi-en-ai-v4.14-r1`, and associated ignored run artifacts. Protocol SHA-256: `447d3fbf79105d819e4aaf9e3921521c1c9d3d851d0831e899c773c5ad9aa865`.
