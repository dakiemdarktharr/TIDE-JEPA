# vi-en-ai-v4.13 Vi–En validation results

AI-authored and independently AI-reviewed preliminary synthetic pilot. **Not human/native-speaker validated.** PhoMT was not used. Phan Rang Cham remains excluded.

## Frozen protocol

The corpus has 7680 records and 192 event combinations. Split groups: 112/40/40; records: 4480/1600/1600 (train/validation/release holdout). Data split policy: 112 train, 40 validation, 40 release-holdout combinations from three fresh agent factors; every held-out factor pair is represented in training; English NOW uses present progressive; fresh split and sealed holdout for a source-copy dose-response ablation.

Objective conditions: tide with source-copy weight 1.5; tide with source-copy weight 3; token_only with source-copy weight 1.5; token_only with source-copy weight 3. Seeds 17, 23, 41; 58 epochs and 3248 updates/config; width 48, 4 heads, 2 layers. Checkpoints selected using the frozen validation criterion. Decoder: greedy byte-level UTF-8 constrained decoding; EOS only at complete codepoint boundaries.

The registered primary objective is `tide`. Its engineering gate requires every configured primary weight, seed, and language/action bucket to meet the frozen thresholds.

## Validation result: **FAIL**

The release holdout was not evaluated and remains sealed.

| Mode | Source-copy weight | Seed | Val token CE | Val path token CE | Updates | Training wall seconds | Mean examples/sec | Gate |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| token_only | 1.5 | 17 | 0.0139 | 0.0085 | 3248 | 1548.7 | 168.1 | control_only |
| token_only | 3 | 17 | 0.0267 | 0.0203 | 3248 | 1551.7 | 167.6 | control_only |
| tide | 1.5 | 17 | 0.0158 | 0.0131 | 3248 | 1724.8 | 150.8 | fail |
| tide | 3 | 17 | 0.0241 | 0.0116 | 3248 | 1750.4 | 148.6 | fail |
| token_only | 1.5 | 23 | 0.0475 | 0.0319 | 3248 | 1554.8 | 167.3 | control_only |
| token_only | 3 | 23 | 0.0314 | 0.0190 | 3248 | 1558.5 | 167.0 | control_only |
| tide | 1.5 | 23 | 0.0254 | 0.0141 | 3248 | 1731.5 | 150.3 | fail |
| tide | 3 | 23 | 0.0307 | 0.0172 | 3248 | 1741.0 | 149.4 | fail |
| token_only | 1.5 | 41 | 0.0176 | 0.0114 | 3248 | 1549.1 | 167.9 | control_only |
| token_only | 3 | 41 | 0.0235 | 0.0106 | 3248 | 1544.2 | 168.6 | control_only |
| tide | 1.5 | 41 | 0.0477 | 0.0482 | 3248 | 1592.0 | 166.7 | fail |
| tide | 3 | 41 | 0.0341 | 0.0210 | 3248 | 1578.8 | 167.7 | fail |

## Validation generation by condition and bucket

Action fidelity and preservation are pooled across seeds within each condition and bucket; thresholds are still checked for every primary condition/seed/bucket. Exact-reference match and CER are synthetic-reference metrics, not human naturalness.

| Mode | Source-copy weight | Bucket | Action fidelity | Preservation | Accepted references | CER | Unicode | EOS |
|---|---:|---|---:|---:|---:|---:|---:|---:|---|
| tide | 1.5 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 238/240 | 216/240 | 207/240 | 1.3% | 240/240 | 240/240 |
| tide | 1.5 | en/single/POLARITY:NEGATIVE | 446/480 | 350/480 | 339/480 | 4.1% | 480/480 | 480/480 |
| tide | 1.5 | en/single/POLARITY:POSITIVE | 462/480 | 322/480 | 305/480 | 4.7% | 480/480 | 480/480 |
| tide | 1.5 | en/single/TIME:NOW | 449/480 | 329/480 | 316/480 | 4.6% | 480/480 | 480/480 |
| tide | 1.5 | en/single/TIME:PAST | 461/480 | 346/480 | 327/480 | 4.4% | 480/480 | 480/480 |
| tide | 1.5 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 235/240 | 200/240 | 186/240 | 2.4% | 240/240 | 240/240 |
| tide | 1.5 | vi/single/POLARITY:NEGATIVE | 456/480 | 395/480 | 370/480 | 2.9% | 480/480 | 480/480 |
| tide | 1.5 | vi/single/POLARITY:POSITIVE | 440/480 | 362/480 | 335/480 | 4.2% | 480/480 | 480/480 |
| tide | 1.5 | vi/single/TIME:NOW | 447/480 | 367/480 | 344/480 | 3.9% | 480/480 | 480/480 |
| tide | 1.5 | vi/single/TIME:PAST | 433/480 | 394/480 | 369/480 | 3.3% | 480/480 | 480/480 |
| tide | 3 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 238/240 | 195/240 | 189/240 | 2.3% | 240/240 | 240/240 |
| tide | 3 | en/single/POLARITY:NEGATIVE | 470/480 | 346/480 | 335/480 | 3.4% | 480/480 | 480/480 |
| tide | 3 | en/single/POLARITY:POSITIVE | 467/480 | 303/480 | 293/480 | 5.2% | 480/480 | 480/480 |
| tide | 3 | en/single/TIME:NOW | 455/480 | 322/480 | 308/480 | 3.6% | 480/480 | 480/480 |
| tide | 3 | en/single/TIME:PAST | 452/480 | 328/480 | 304/480 | 5.0% | 480/480 | 480/480 |
| tide | 3 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 238/240 | 191/240 | 184/240 | 2.6% | 240/240 | 240/240 |
| tide | 3 | vi/single/POLARITY:NEGATIVE | 456/480 | 362/480 | 339/480 | 3.8% | 480/480 | 480/480 |
| tide | 3 | vi/single/POLARITY:POSITIVE | 397/480 | 282/480 | 249/480 | 6.8% | 480/480 | 480/480 |
| tide | 3 | vi/single/TIME:NOW | 442/480 | 366/480 | 328/480 | 4.6% | 480/480 | 480/480 |
| tide | 3 | vi/single/TIME:PAST | 389/480 | 311/480 | 297/480 | 5.7% | 480/480 | 480/480 |
| token_only | 1.5 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 237/240 | 205/240 | 201/240 | 1.9% | 240/240 | 240/240 |
| token_only | 1.5 | en/single/POLARITY:NEGATIVE | 465/480 | 373/480 | 363/480 | 2.5% | 480/480 | 480/480 |
| token_only | 1.5 | en/single/POLARITY:POSITIVE | 464/480 | 361/480 | 342/480 | 3.1% | 480/480 | 480/480 |
| token_only | 1.5 | en/single/TIME:NOW | 456/480 | 343/480 | 331/480 | 3.4% | 480/480 | 480/480 |
| token_only | 1.5 | en/single/TIME:PAST | 458/480 | 355/480 | 338/480 | 3.5% | 480/480 | 480/480 |
| token_only | 1.5 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 229/240 | 219/240 | 206/240 | 1.5% | 240/240 | 240/240 |
| token_only | 1.5 | vi/single/POLARITY:NEGATIVE | 464/480 | 419/480 | 404/480 | 2.0% | 480/480 | 480/480 |
| token_only | 1.5 | vi/single/POLARITY:POSITIVE | 463/480 | 412/480 | 395/480 | 2.2% | 480/480 | 480/480 |
| token_only | 1.5 | vi/single/TIME:NOW | 457/480 | 406/480 | 376/480 | 2.5% | 480/480 | 480/480 |
| token_only | 1.5 | vi/single/TIME:PAST | 446/480 | 408/480 | 387/480 | 2.4% | 480/480 | 480/480 |
| token_only | 3 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 229/240 | 186/240 | 174/240 | 3.1% | 240/240 | 240/240 |
| token_only | 3 | en/single/POLARITY:NEGATIVE | 446/480 | 356/480 | 346/480 | 3.4% | 480/480 | 480/480 |
| token_only | 3 | en/single/POLARITY:POSITIVE | 459/480 | 326/480 | 305/480 | 5.0% | 480/480 | 480/480 |
| token_only | 3 | en/single/TIME:NOW | 425/480 | 300/480 | 284/480 | 4.6% | 480/480 | 480/480 |
| token_only | 3 | en/single/TIME:PAST | 443/480 | 291/480 | 271/480 | 6.2% | 480/480 | 480/480 |
| token_only | 3 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 238/240 | 219/240 | 210/240 | 1.9% | 240/240 | 240/240 |
| token_only | 3 | vi/single/POLARITY:NEGATIVE | 468/480 | 423/480 | 405/480 | 2.1% | 480/480 | 480/480 |
| token_only | 3 | vi/single/POLARITY:POSITIVE | 454/480 | 411/480 | 389/480 | 2.6% | 480/480 | 480/480 |
| token_only | 3 | vi/single/TIME:NOW | 467/480 | 414/480 | 400/480 | 1.9% | 480/480 | 480/480 |
| token_only | 3 | vi/single/TIME:PAST | 433/480 | 400/480 | 386/480 | 2.7% | 480/480 | 480/480 |

## Primary-mode validation diagnostics by seed

Counts below preserve the frozen seed-by-seed gate denominator. No generated or reference text is included.

| Source-copy weight | Seed | Bucket | Action fidelity | Preservation | Accepted references | CER | Unicode | EOS | Bucket gate |
|---:|---:|---|---:|---:|---:|---:|---:|---:|---|
| 1.5 | 17 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 80/80 | 69/80 | 69/80 | 1.6% | 80/80 | 80/80 | pass |
| 1.5 | 17 | en/single/POLARITY:NEGATIVE | 159/160 | 128/160 | 126/160 | 2.1% | 160/160 | 160/160 | fail |
| 1.5 | 17 | en/single/POLARITY:POSITIVE | 158/160 | 127/160 | 120/160 | 2.8% | 160/160 | 160/160 | fail |
| 1.5 | 17 | en/single/TIME:NOW | 160/160 | 139/160 | 139/160 | 1.1% | 160/160 | 160/160 | fail |
| 1.5 | 17 | en/single/TIME:PAST | 157/160 | 124/160 | 119/160 | 2.9% | 160/160 | 160/160 | fail |
| 1.5 | 17 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 79/80 | 68/80 | 65/80 | 1.8% | 80/80 | 80/80 | pass |
| 1.5 | 17 | vi/single/POLARITY:NEGATIVE | 157/160 | 141/160 | 134/160 | 2.3% | 160/160 | 160/160 | fail |
| 1.5 | 17 | vi/single/POLARITY:POSITIVE | 153/160 | 130/160 | 126/160 | 2.7% | 160/160 | 160/160 | fail |
| 1.5 | 17 | vi/single/TIME:NOW | 156/160 | 130/160 | 128/160 | 2.5% | 160/160 | 160/160 | fail |
| 1.5 | 17 | vi/single/TIME:PAST | 153/160 | 144/160 | 138/160 | 1.9% | 160/160 | 160/160 | pass |
| 1.5 | 23 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 79/80 | 73/80 | 71/80 | 1.3% | 80/80 | 80/80 | pass |
| 1.5 | 23 | en/single/POLARITY:NEGATIVE | 157/160 | 126/160 | 124/160 | 3.1% | 160/160 | 160/160 | fail |
| 1.5 | 23 | en/single/POLARITY:POSITIVE | 151/160 | 115/160 | 108/160 | 4.1% | 160/160 | 160/160 | fail |
| 1.5 | 23 | en/single/TIME:NOW | 153/160 | 107/160 | 99/160 | 4.1% | 160/160 | 160/160 | fail |
| 1.5 | 23 | en/single/TIME:PAST | 157/160 | 121/160 | 115/160 | 2.8% | 160/160 | 160/160 | fail |
| 1.5 | 23 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 79/80 | 63/80 | 59/80 | 2.5% | 80/80 | 80/80 | fail |
| 1.5 | 23 | vi/single/POLARITY:NEGATIVE | 153/160 | 127/160 | 119/160 | 2.7% | 160/160 | 160/160 | fail |
| 1.5 | 23 | vi/single/POLARITY:POSITIVE | 137/160 | 115/160 | 105/160 | 5.0% | 160/160 | 160/160 | fail |
| 1.5 | 23 | vi/single/TIME:NOW | 142/160 | 111/160 | 102/160 | 4.6% | 160/160 | 160/160 | fail |
| 1.5 | 23 | vi/single/TIME:PAST | 142/160 | 128/160 | 118/160 | 3.4% | 160/160 | 160/160 | fail |
| 1.5 | 41 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 79/80 | 74/80 | 67/80 | 1.1% | 80/80 | 80/80 | pass |
| 1.5 | 41 | en/single/POLARITY:NEGATIVE | 130/160 | 96/160 | 89/160 | 7.2% | 160/160 | 160/160 | fail |
| 1.5 | 41 | en/single/POLARITY:POSITIVE | 153/160 | 80/160 | 77/160 | 7.0% | 160/160 | 160/160 | fail |
| 1.5 | 41 | en/single/TIME:NOW | 136/160 | 83/160 | 78/160 | 8.7% | 160/160 | 160/160 | fail |
| 1.5 | 41 | en/single/TIME:PAST | 147/160 | 101/160 | 93/160 | 7.3% | 160/160 | 160/160 | fail |
| 1.5 | 41 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 77/80 | 69/80 | 62/80 | 2.8% | 80/80 | 80/80 | pass |
| 1.5 | 41 | vi/single/POLARITY:NEGATIVE | 146/160 | 127/160 | 117/160 | 3.7% | 160/160 | 160/160 | fail |
| 1.5 | 41 | vi/single/POLARITY:POSITIVE | 150/160 | 117/160 | 104/160 | 4.8% | 160/160 | 160/160 | fail |
| 1.5 | 41 | vi/single/TIME:NOW | 149/160 | 126/160 | 114/160 | 4.6% | 160/160 | 160/160 | fail |
| 1.5 | 41 | vi/single/TIME:PAST | 138/160 | 122/160 | 113/160 | 4.6% | 160/160 | 160/160 | fail |
| 3 | 17 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 80/80 | 65/80 | 65/80 | 2.4% | 80/80 | 80/80 | pass |
| 3 | 17 | en/single/POLARITY:NEGATIVE | 158/160 | 123/160 | 122/160 | 3.2% | 160/160 | 160/160 | fail |
| 3 | 17 | en/single/POLARITY:POSITIVE | 157/160 | 102/160 | 102/160 | 5.1% | 160/160 | 160/160 | fail |
| 3 | 17 | en/single/TIME:NOW | 157/160 | 123/160 | 120/160 | 2.7% | 160/160 | 160/160 | fail |
| 3 | 17 | en/single/TIME:PAST | 154/160 | 112/160 | 109/160 | 4.8% | 160/160 | 160/160 | fail |
| 3 | 17 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 80/80 | 72/80 | 69/80 | 1.2% | 80/80 | 80/80 | pass |
| 3 | 17 | vi/single/POLARITY:NEGATIVE | 153/160 | 131/160 | 125/160 | 3.5% | 160/160 | 160/160 | fail |
| 3 | 17 | vi/single/POLARITY:POSITIVE | 144/160 | 111/160 | 103/160 | 4.4% | 160/160 | 160/160 | fail |
| 3 | 17 | vi/single/TIME:NOW | 151/160 | 128/160 | 120/160 | 4.9% | 160/160 | 160/160 | fail |
| 3 | 17 | vi/single/TIME:PAST | 145/160 | 116/160 | 112/160 | 4.4% | 160/160 | 160/160 | fail |
| 3 | 23 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 80/80 | 63/80 | 62/80 | 1.8% | 80/80 | 80/80 | fail |
| 3 | 23 | en/single/POLARITY:NEGATIVE | 157/160 | 100/160 | 98/160 | 4.1% | 160/160 | 160/160 | fail |
| 3 | 23 | en/single/POLARITY:POSITIVE | 153/160 | 79/160 | 71/160 | 7.5% | 160/160 | 160/160 | fail |
| 3 | 23 | en/single/TIME:NOW | 147/160 | 93/160 | 86/160 | 4.7% | 160/160 | 160/160 | fail |
| 3 | 23 | en/single/TIME:PAST | 154/160 | 105/160 | 97/160 | 4.6% | 160/160 | 160/160 | fail |
| 3 | 23 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 78/80 | 66/80 | 63/80 | 1.9% | 80/80 | 80/80 | pass |
| 3 | 23 | vi/single/POLARITY:NEGATIVE | 154/160 | 135/160 | 124/160 | 2.7% | 160/160 | 160/160 | fail |
| 3 | 23 | vi/single/POLARITY:POSITIVE | 142/160 | 109/160 | 95/160 | 5.8% | 160/160 | 160/160 | fail |
| 3 | 23 | vi/single/TIME:NOW | 137/160 | 123/160 | 107/160 | 3.9% | 160/160 | 160/160 | fail |
| 3 | 23 | vi/single/TIME:PAST | 136/160 | 119/160 | 113/160 | 4.3% | 160/160 | 160/160 | fail |
| 3 | 41 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 78/80 | 67/80 | 62/80 | 2.6% | 80/80 | 80/80 | pass |
| 3 | 41 | en/single/POLARITY:NEGATIVE | 155/160 | 123/160 | 115/160 | 2.9% | 160/160 | 160/160 | fail |
| 3 | 41 | en/single/POLARITY:POSITIVE | 157/160 | 122/160 | 120/160 | 3.1% | 160/160 | 160/160 | fail |
| 3 | 41 | en/single/TIME:NOW | 151/160 | 106/160 | 102/160 | 3.5% | 160/160 | 160/160 | fail |
| 3 | 41 | en/single/TIME:PAST | 144/160 | 111/160 | 98/160 | 5.5% | 160/160 | 160/160 | fail |
| 3 | 41 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 80/80 | 53/80 | 52/80 | 4.8% | 80/80 | 80/80 | fail |
| 3 | 41 | vi/single/POLARITY:NEGATIVE | 149/160 | 96/160 | 90/160 | 5.2% | 160/160 | 160/160 | fail |
| 3 | 41 | vi/single/POLARITY:POSITIVE | 111/160 | 62/160 | 51/160 | 10.1% | 160/160 | 160/160 | fail |
| 3 | 41 | vi/single/TIME:NOW | 154/160 | 115/160 | 101/160 | 5.0% | 160/160 | 160/160 | fail |
| 3 | 41 | vi/single/TIME:PAST | 108/160 | 76/160 | 72/160 | 8.2% | 160/160 | 160/160 | fail |

## Limits and interpretation

Valid Unicode and EOS termination do not establish semantic correctness. The deterministic checker covers only the declared synthetic tense/polarity grammar and named roles. This benchmark tests recombination of familiar lexical factors; it does not establish naturalness, natural-corpus efficacy, or scientific efficacy. Control results are diagnostic; no TIDE advantage is claimed.

Across the 60 frozen primary seed-by-bucket checks (two weights × three seeds × ten buckets), 10 passed and 50 failed. This includes one single-action bucket at exactly 90% preservation; the other 47/48 single-action buckets failed, as did three held-out-path buckets. Each seed uses the same 40 validation event groups; 160 single-action or 80 path rows per seed are operational denominators, not independent linguistic observations. Pooled comparisons must not be read as statistical precision; no confidence intervals or human assessments are available.

All examples and generated outputs remain private under Git-ignored `data/` and `runs/`. This report contains aggregate metrics only. `human_validated` is false. PhoMT raw/derived data and Phan Rang Cham data were not used.

Private aggregate evidence: `vi-en-ai-v4.13/protocol.json`, validation generation metrics under `vi-en-ai-v4.13`, and associated ignored run artifacts. Protocol SHA-256: `0971674ed583938435e9939edc270a0cb7e752e7747dea39f126eb74a32ff1d3`.
