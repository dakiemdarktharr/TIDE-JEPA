# vi-en-ai-v4.15 Vi–En validation results

AI-authored and independently AI-reviewed preliminary synthetic pilot. **Not human/native-speaker validated.** PhoMT was not used. Phan Rang Cham remains excluded.

## Frozen protocol

The corpus has 15360 records and 192 event combinations. Split groups: 112/40/40; records: 8960/3200/3200 (train/validation/release holdout). Data split policy: 112 train, 40 validation, 40 release-holdout combinations from three fresh agent factors; every held-out factor pair is represented in training; English NOW uses present progressive; four context-balanced surface realizations per meaning state; fresh sealed holdout for an exposure-diversity test. Transition weighting: There are 3072 duplicated path-step rows across the full split: 1792 in training, 640 in validation, and 640 in the sealed release holdout. Each logical path-step transition has one standalone single-edge record and one path-linked record. In training this adds 1792 record exposures, so those path-selected transitions contribute twice the row-wise token/edge exposure. Validation and holdout duplicates are evaluation records, not training exposure. The representation is fixed identically across conditions; results describe a path-enriched training distribution, not uniform weighting over unique transitions.

Objective conditions: tide with source-copy weight 1.5 and TIDE latent-objective multiplier 0.5; tide with source-copy weight 1.5 and TIDE latent-objective multiplier 1; token_only with source-copy weight 1.5. Seeds 17, 23, 41; 29 epochs and 3248 updates/config; width 48, 4 heads, 2 layers. Checkpoints selected using the frozen validation criterion. Decoder: greedy byte-level UTF-8 constrained decoding; EOS only at complete codepoint boundaries.

The registered primary objective is `tide`. Its engineering gate requires every configured primary weight, seed, and language/action bucket to meet the frozen thresholds.

## Validation result: **FAIL**

The release holdout was not evaluated and remains sealed.

| Mode | Source-copy weight | TIDE aux multiplier | Seed | Val token CE | Val path token CE | Updates | Training wall seconds | Mean examples/sec | Gate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| token_only | 1.5 | — | 17 | 0.0239 | 0.0134 | 3248 | 2010.0 | 129.3 | control_only |
| tide | 1.5 | 0.5 | 17 | 0.0304 | 0.0170 | 3248 | 2240.4 | 116.1 | fail |
| tide | 1.5 | 1 | 17 | 0.0375 | 0.0290 | 3248 | 2221.3 | 117.0 | fail |
| token_only | 1.5 | — | 23 | 0.0285 | 0.0203 | 3248 | 1991.3 | 130.6 | control_only |
| tide | 1.5 | 0.5 | 23 | 0.0399 | 0.0236 | 3248 | 2250.3 | 115.5 | fail |
| tide | 1.5 | 1 | 23 | 0.0398 | 0.0278 | 3248 | 2276.9 | 114.2 | fail |
| token_only | 1.5 | — | 41 | 0.0524 | 0.0234 | 3248 | 1991.3 | 130.6 | control_only |
| tide | 1.5 | 0.5 | 41 | 0.0527 | 0.0339 | 3248 | 2171.6 | 120.5 | fail |
| tide | 1.5 | 1 | 41 | 0.0596 | 0.0441 | 3248 | 1531.6 | 170.1 | fail |

## Validation generation by condition and bucket

Action fidelity and preservation are pooled across seeds within each condition and bucket; thresholds are still checked for every primary condition/seed/bucket. Exact-reference match and CER are synthetic-reference metrics, not human naturalness.

| Mode | Source-copy weight | TIDE aux multiplier | Bucket | Action fidelity | Preservation | Accepted references | CER | Unicode | EOS |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---|
| tide | 1.5 | 0.5 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 458/480 | 308/480 | 294/480 | 3.3% | 480/480 | 480/480 |
| tide | 1.5 | 0.5 | en/single/POLARITY:NEGATIVE | 864/960 | 508/960 | 487/960 | 5.5% | 960/960 | 960/960 |
| tide | 1.5 | 0.5 | en/single/POLARITY:POSITIVE | 890/960 | 438/960 | 392/960 | 6.9% | 960/960 | 960/960 |
| tide | 1.5 | 0.5 | en/single/TIME:NOW | 905/960 | 488/960 | 464/960 | 5.3% | 960/960 | 960/960 |
| tide | 1.5 | 0.5 | en/single/TIME:PAST | 861/960 | 451/960 | 404/960 | 7.3% | 960/960 | 960/960 |
| tide | 1.5 | 0.5 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 469/480 | 385/480 | 371/480 | 2.8% | 480/480 | 480/480 |
| tide | 1.5 | 0.5 | vi/single/POLARITY:NEGATIVE | 898/960 | 649/960 | 593/960 | 4.8% | 960/960 | 960/960 |
| tide | 1.5 | 0.5 | vi/single/POLARITY:POSITIVE | 819/960 | 441/960 | 396/960 | 7.8% | 960/960 | 960/960 |
| tide | 1.5 | 0.5 | vi/single/TIME:NOW | 883/960 | 584/960 | 506/960 | 6.2% | 960/960 | 960/960 |
| tide | 1.5 | 0.5 | vi/single/TIME:PAST | 753/960 | 529/960 | 508/960 | 5.6% | 960/960 | 960/960 |
| tide | 1.5 | 1 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 474/480 | 292/480 | 287/480 | 3.5% | 480/480 | 480/480 |
| tide | 1.5 | 1 | en/single/POLARITY:NEGATIVE | 921/960 | 520/960 | 509/960 | 4.3% | 960/960 | 960/960 |
| tide | 1.5 | 1 | en/single/POLARITY:POSITIVE | 906/960 | 387/960 | 356/960 | 8.2% | 960/960 | 960/960 |
| tide | 1.5 | 1 | en/single/TIME:NOW | 877/960 | 453/960 | 421/960 | 6.3% | 960/960 | 960/960 |
| tide | 1.5 | 1 | en/single/TIME:PAST | 896/960 | 399/960 | 381/960 | 8.0% | 960/960 | 960/960 |
| tide | 1.5 | 1 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 456/480 | 350/480 | 332/480 | 3.5% | 480/480 | 480/480 |
| tide | 1.5 | 1 | vi/single/POLARITY:NEGATIVE | 837/960 | 619/960 | 558/960 | 5.7% | 960/960 | 960/960 |
| tide | 1.5 | 1 | vi/single/POLARITY:POSITIVE | 728/960 | 440/960 | 372/960 | 8.0% | 960/960 | 960/960 |
| tide | 1.5 | 1 | vi/single/TIME:NOW | 829/960 | 520/960 | 408/960 | 7.8% | 960/960 | 960/960 |
| tide | 1.5 | 1 | vi/single/TIME:PAST | 664/960 | 479/960 | 458/960 | 6.5% | 960/960 | 960/960 |
| token_only | 1.5 | — | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 463/480 | 359/480 | 346/480 | 2.4% | 480/480 | 480/480 |
| token_only | 1.5 | — | en/single/POLARITY:NEGATIVE | 925/960 | 646/960 | 634/960 | 3.2% | 960/960 | 960/960 |
| token_only | 1.5 | — | en/single/POLARITY:POSITIVE | 944/960 | 546/960 | 512/960 | 4.8% | 960/960 | 960/960 |
| token_only | 1.5 | — | en/single/TIME:NOW | 923/960 | 555/960 | 536/960 | 4.2% | 960/960 | 960/960 |
| token_only | 1.5 | — | en/single/TIME:PAST | 919/960 | 569/960 | 542/960 | 4.4% | 960/960 | 960/960 |
| token_only | 1.5 | — | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 473/480 | 360/480 | 342/480 | 2.5% | 480/480 | 480/480 |
| token_only | 1.5 | — | vi/single/POLARITY:NEGATIVE | 895/960 | 631/960 | 595/960 | 4.5% | 960/960 | 960/960 |
| token_only | 1.5 | — | vi/single/POLARITY:POSITIVE | 794/960 | 550/960 | 514/960 | 5.6% | 960/960 | 960/960 |
| token_only | 1.5 | — | vi/single/TIME:NOW | 883/960 | 616/960 | 550/960 | 5.4% | 960/960 | 960/960 |
| token_only | 1.5 | — | vi/single/TIME:PAST | 769/960 | 569/960 | 534/960 | 4.8% | 960/960 | 960/960 |

## Primary-mode validation diagnostics by seed

Counts below preserve the frozen seed-by-seed gate denominator. No generated or reference text is included.

| Source-copy weight | TIDE aux multiplier | Seed | Bucket | Action fidelity | Preservation | Accepted references | CER | Unicode | EOS | Bucket gate |
|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---|
| 1.5 | 0.5 | 17 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 146/160 | 116/160 | 107/160 | 3.7% | 160/160 | 160/160 | fail |
| 1.5 | 0.5 | 17 | en/single/POLARITY:NEGATIVE | 260/320 | 177/320 | 160/320 | 7.8% | 320/320 | 320/320 | fail |
| 1.5 | 0.5 | 17 | en/single/POLARITY:POSITIVE | 294/320 | 180/320 | 148/320 | 6.7% | 320/320 | 320/320 | fail |
| 1.5 | 0.5 | 17 | en/single/TIME:NOW | 301/320 | 178/320 | 162/320 | 5.3% | 320/320 | 320/320 | fail |
| 1.5 | 0.5 | 17 | en/single/TIME:PAST | 267/320 | 181/320 | 152/320 | 8.3% | 320/320 | 320/320 | fail |
| 1.5 | 0.5 | 17 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 157/160 | 143/160 | 140/160 | 2.3% | 160/160 | 160/160 | pass |
| 1.5 | 0.5 | 17 | vi/single/POLARITY:NEGATIVE | 304/320 | 246/320 | 225/320 | 4.0% | 320/320 | 320/320 | fail |
| 1.5 | 0.5 | 17 | vi/single/POLARITY:POSITIVE | 291/320 | 190/320 | 176/320 | 5.6% | 320/320 | 320/320 | fail |
| 1.5 | 0.5 | 17 | vi/single/TIME:NOW | 311/320 | 255/320 | 226/320 | 3.7% | 320/320 | 320/320 | fail |
| 1.5 | 0.5 | 17 | vi/single/TIME:PAST | 298/320 | 230/320 | 227/320 | 3.7% | 320/320 | 320/320 | fail |
| 1.5 | 0.5 | 23 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 153/160 | 104/160 | 100/160 | 2.4% | 160/160 | 160/160 | fail |
| 1.5 | 0.5 | 23 | en/single/POLARITY:NEGATIVE | 311/320 | 180/320 | 179/320 | 3.1% | 320/320 | 320/320 | fail |
| 1.5 | 0.5 | 23 | en/single/POLARITY:POSITIVE | 301/320 | 131/320 | 123/320 | 5.7% | 320/320 | 320/320 | fail |
| 1.5 | 0.5 | 23 | en/single/TIME:NOW | 306/320 | 153/320 | 149/320 | 4.1% | 320/320 | 320/320 | fail |
| 1.5 | 0.5 | 23 | en/single/TIME:PAST | 294/320 | 135/320 | 122/320 | 6.2% | 320/320 | 320/320 | fail |
| 1.5 | 0.5 | 23 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 155/160 | 132/160 | 125/160 | 2.1% | 160/160 | 160/160 | pass |
| 1.5 | 0.5 | 23 | vi/single/POLARITY:NEGATIVE | 300/320 | 212/320 | 189/320 | 5.2% | 320/320 | 320/320 | fail |
| 1.5 | 0.5 | 23 | vi/single/POLARITY:POSITIVE | 274/320 | 159/320 | 132/320 | 8.6% | 320/320 | 320/320 | fail |
| 1.5 | 0.5 | 23 | vi/single/TIME:NOW | 279/320 | 181/320 | 140/320 | 7.3% | 320/320 | 320/320 | fail |
| 1.5 | 0.5 | 23 | vi/single/TIME:PAST | 207/320 | 149/320 | 141/320 | 6.3% | 320/320 | 320/320 | fail |
| 1.5 | 0.5 | 41 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 159/160 | 88/160 | 87/160 | 3.7% | 160/160 | 160/160 | fail |
| 1.5 | 0.5 | 41 | en/single/POLARITY:NEGATIVE | 293/320 | 151/320 | 148/320 | 5.7% | 320/320 | 320/320 | fail |
| 1.5 | 0.5 | 41 | en/single/POLARITY:POSITIVE | 295/320 | 127/320 | 121/320 | 8.2% | 320/320 | 320/320 | fail |
| 1.5 | 0.5 | 41 | en/single/TIME:NOW | 298/320 | 157/320 | 153/320 | 6.5% | 320/320 | 320/320 | fail |
| 1.5 | 0.5 | 41 | en/single/TIME:PAST | 300/320 | 135/320 | 130/320 | 7.5% | 320/320 | 320/320 | fail |
| 1.5 | 0.5 | 41 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 157/160 | 110/160 | 106/160 | 4.0% | 160/160 | 160/160 | fail |
| 1.5 | 0.5 | 41 | vi/single/POLARITY:NEGATIVE | 294/320 | 191/320 | 179/320 | 5.1% | 320/320 | 320/320 | fail |
| 1.5 | 0.5 | 41 | vi/single/POLARITY:POSITIVE | 254/320 | 92/320 | 88/320 | 9.2% | 320/320 | 320/320 | fail |
| 1.5 | 0.5 | 41 | vi/single/TIME:NOW | 293/320 | 148/320 | 140/320 | 7.8% | 320/320 | 320/320 | fail |
| 1.5 | 0.5 | 41 | vi/single/TIME:PAST | 248/320 | 150/320 | 140/320 | 6.9% | 320/320 | 320/320 | fail |
| 1.5 | 1 | 17 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 158/160 | 116/160 | 116/160 | 2.1% | 160/160 | 160/160 | fail |
| 1.5 | 1 | 17 | en/single/POLARITY:NEGATIVE | 301/320 | 208/320 | 204/320 | 3.1% | 320/320 | 320/320 | fail |
| 1.5 | 1 | 17 | en/single/POLARITY:POSITIVE | 308/320 | 157/320 | 139/320 | 6.0% | 320/320 | 320/320 | fail |
| 1.5 | 1 | 17 | en/single/TIME:NOW | 281/320 | 182/320 | 165/320 | 5.6% | 320/320 | 320/320 | fail |
| 1.5 | 1 | 17 | en/single/TIME:PAST | 300/320 | 161/320 | 156/320 | 6.7% | 320/320 | 320/320 | fail |
| 1.5 | 1 | 17 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 154/160 | 136/160 | 128/160 | 1.9% | 160/160 | 160/160 | pass |
| 1.5 | 1 | 17 | vi/single/POLARITY:NEGATIVE | 291/320 | 229/320 | 215/320 | 4.1% | 320/320 | 320/320 | fail |
| 1.5 | 1 | 17 | vi/single/POLARITY:POSITIVE | 268/320 | 184/320 | 164/320 | 4.9% | 320/320 | 320/320 | fail |
| 1.5 | 1 | 17 | vi/single/TIME:NOW | 295/320 | 188/320 | 154/320 | 6.1% | 320/320 | 320/320 | fail |
| 1.5 | 1 | 17 | vi/single/TIME:PAST | 229/320 | 174/320 | 167/320 | 5.2% | 320/320 | 320/320 | fail |
| 1.5 | 1 | 23 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 157/160 | 89/160 | 88/160 | 3.7% | 160/160 | 160/160 | fail |
| 1.5 | 1 | 23 | en/single/POLARITY:NEGATIVE | 307/320 | 163/320 | 161/320 | 4.6% | 320/320 | 320/320 | fail |
| 1.5 | 1 | 23 | en/single/POLARITY:POSITIVE | 294/320 | 114/320 | 106/320 | 9.1% | 320/320 | 320/320 | fail |
| 1.5 | 1 | 23 | en/single/TIME:NOW | 281/320 | 147/320 | 141/320 | 6.6% | 320/320 | 320/320 | fail |
| 1.5 | 1 | 23 | en/single/TIME:PAST | 295/320 | 122/320 | 121/320 | 8.6% | 320/320 | 320/320 | fail |
| 1.5 | 1 | 23 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 156/160 | 124/160 | 120/160 | 2.5% | 160/160 | 160/160 | fail |
| 1.5 | 1 | 23 | vi/single/POLARITY:NEGATIVE | 279/320 | 219/320 | 198/320 | 5.6% | 320/320 | 320/320 | fail |
| 1.5 | 1 | 23 | vi/single/POLARITY:POSITIVE | 229/320 | 124/320 | 106/320 | 9.9% | 320/320 | 320/320 | fail |
| 1.5 | 1 | 23 | vi/single/TIME:NOW | 277/320 | 181/320 | 146/320 | 8.2% | 320/320 | 320/320 | fail |
| 1.5 | 1 | 23 | vi/single/TIME:PAST | 248/320 | 184/320 | 180/320 | 6.2% | 320/320 | 320/320 | fail |
| 1.5 | 1 | 41 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 159/160 | 87/160 | 83/160 | 4.7% | 160/160 | 160/160 | fail |
| 1.5 | 1 | 41 | en/single/POLARITY:NEGATIVE | 313/320 | 149/320 | 144/320 | 5.2% | 320/320 | 320/320 | fail |
| 1.5 | 1 | 41 | en/single/POLARITY:POSITIVE | 304/320 | 116/320 | 111/320 | 9.5% | 320/320 | 320/320 | fail |
| 1.5 | 1 | 41 | en/single/TIME:NOW | 315/320 | 124/320 | 115/320 | 6.8% | 320/320 | 320/320 | fail |
| 1.5 | 1 | 41 | en/single/TIME:PAST | 301/320 | 116/320 | 104/320 | 8.7% | 320/320 | 320/320 | fail |
| 1.5 | 1 | 41 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 146/160 | 90/160 | 84/160 | 6.2% | 160/160 | 160/160 | fail |
| 1.5 | 1 | 41 | vi/single/POLARITY:NEGATIVE | 267/320 | 171/320 | 145/320 | 7.3% | 320/320 | 320/320 | fail |
| 1.5 | 1 | 41 | vi/single/POLARITY:POSITIVE | 231/320 | 132/320 | 102/320 | 9.2% | 320/320 | 320/320 | fail |
| 1.5 | 1 | 41 | vi/single/TIME:NOW | 257/320 | 151/320 | 108/320 | 9.0% | 320/320 | 320/320 | fail |
| 1.5 | 1 | 41 | vi/single/TIME:PAST | 187/320 | 121/320 | 111/320 | 8.1% | 320/320 | 320/320 | fail |

## Limits and interpretation

Valid Unicode and EOS termination do not establish semantic correctness. The deterministic checker covers only the declared synthetic tense/polarity grammar and named roles. This benchmark tests recombination of familiar lexical factors; it does not establish naturalness, natural-corpus efficacy, or scientific efficacy. Control results are diagnostic; no TIDE advantage is claimed.

All examples and generated outputs remain private under Git-ignored `data/` and `runs/`. This report contains aggregate metrics only. `human_validated` is false. PhoMT raw/derived data and Phan Rang Cham data were not used.

Private aggregate evidence: `vi-en-ai-v4.15-r1/protocol.json`, validation generation metrics under `vi-en-ai-v4.15-r1`, and associated ignored run artifacts. Protocol SHA-256: `3f8f18aa2e3a674369afebfe5867b657391b1648c02f75b24504dfc76d4aa30d`.

## Aggregate preservation-failure diagnosis

An aggregate-only pass over the private validation outputs counted failures of the checker’s named role and location markers and its required verb phrase. Counts below pool three seeds (single-action n=3,840 per language/condition; held-out paths n=480 per language/condition). These are overlapping failure categories, not additional gate metrics; generated/reference text is not included.

| Mode | TIDE aux | Language | Task | Agent missing | Patient missing | Place missing | Required verb phrase missing | Action fidelity failures |
|---|---:|---|---|---:|---:|---:|---:|---:|
| token_only | — | en | single | 4/3840 | 787/3840 | 57/3840 | 1070/3840 | 129/3840 |
| token_only | — | vi | single | 44/3840 | 448/3840 | 44/3840 | 1212/3840 | 295/3840 |
| tide | 0.5 | en | single | 16/3840 | 1006/3840 | 70/3840 | 1458/3840 | 320/3840 |
| tide | 0.5 | vi | single | 60/3840 | 518/3840 | 92/3840 | 1326/3840 | 321/3840 |
| tide | 1.0 | en | single | 5/3840 | 1186/3840 | 73/3840 | 1537/3840 | 240/3840 |
| tide | 1.0 | vi | single | 23/3840 | 515/3840 | 92/3840 | 1512/3840 | 469/3840 |
| token_only | — | en | held-out path | 0/480 | 80/480 | 6/480 | 52/480 | 17/480 |
| token_only | — | vi | held-out path | 1/480 | 44/480 | 4/480 | 85/480 | 7/480 |
| tide | 0.5 | en | held-out path | 2/480 | 121/480 | 5/480 | 81/480 | 22/480 |
| tide | 0.5 | vi | held-out path | 0/480 | 28/480 | 1/480 | 76/480 | 11/480 |
| tide | 1.0 | en | held-out path | 1/480 | 134/480 | 3/480 | 85/480 | 6/480 |
| tide | 1.0 | vi | held-out path | 0/480 | 35/480 | 6/480 | 116/480 | 24/480 |

Patient and required-verb phrase misses dominate the preservation difficulty; agent and invariant-place misses are less frequent. The comparison is limited to the synthetic event grammar and rule checker, so it cannot establish semantic adequacy or human language quality.
