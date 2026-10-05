# vi-en-ai-v4.19 Vi–En validation results

AI-authored and independently AI-reviewed preliminary synthetic pilot. **Not human/native-speaker validated.** PhoMT was not used. Phan Rang Cham remains excluded.

## Frozen protocol

The corpus has 15360 records and 192 event combinations. Split groups: 112/40/40; records: 8960/3200/3200 (train/validation/release holdout). Data split policy: 112 train, 40 validation, 40 release-holdout combinations from three fresh agent factors; every held-out factor pair is represented in training; English NOW uses present progressive; four context-balanced surface realizations per meaning state; action order matches across all splits; fresh split for a TIDE copy-weight (0/1.5) × latent-dose (0/0.1) study with matched loss computation and fixed-final-epoch evaluation. Frozen release-holdout scope: The release holdout uses the same ordered action paths as train and validation; it probes fresh held-out factor combinations only and does not add an action-order shift.

Objective conditions: tide with source-copy weight 0 and TIDE latent-objective multiplier 0; transition balance `unique_transition`; tide with source-copy weight 0 and TIDE latent-objective multiplier 0.1; transition balance `unique_transition`; tide with source-copy weight 1.5 and TIDE latent-objective multiplier 0; transition balance `unique_transition`; tide with source-copy weight 1.5 and TIDE latent-objective multiplier 0.1; transition balance `unique_transition`. Seeds 17, 23, 41; 29 epochs and 3248 updates/config; width 48, 4 heads, 2 layers. The preregistered final epoch was evaluated (`fixed_final_epoch`); validation loss did not select the checkpoint. Decoder: greedy byte-level UTF-8 constrained decoding; EOS only at complete codepoint boundaries.

The registered primary objective is `tide`. Frozen thresholds: valid Unicode 100%; single-action action fidelity and preservation each ≥90%; held-out-path action fidelity and preservation each ≥80%. Every configured primary weight, seed, and language/action bucket must meet all applicable thresholds.

## Validation result: **FAIL**

Semantic checker coverage is complete across all primary buckets.

The release holdout was not evaluated and remains sealed.

| Mode | Source-copy weight | TIDE aux multiplier | Edge balance | Seed | Train token CE | Val token CE | Val path token CE | Updates | Training wall seconds | Mean examples/sec | Gate |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---|
| tide | 0 | 0 | unique_transition | 17 | 0.0130 | 0.0440 | 0.0215 | 3248 | 2148.7 | 121.0 | fail |
| tide | 0 | 0.1 | unique_transition | 17 | 0.0163 | 0.0500 | 0.0238 | 3248 | 2140.3 | 121.4 | fail |
| tide | 1.5 | 0 | unique_transition | 17 | 0.0118 | 0.0585 | 0.0422 | 3248 | 2142.5 | 121.4 | fail |
| tide | 1.5 | 0.1 | unique_transition | 17 | 0.0126 | 0.0599 | 0.0399 | 3248 | 2125.9 | 122.4 | fail |
| tide | 0 | 0 | unique_transition | 23 | 0.0105 | 0.0413 | 0.0207 | 3248 | 2127.3 | 122.2 | fail |
| tide | 0 | 0.1 | unique_transition | 23 | 0.0115 | 0.0490 | 0.0247 | 3248 | 2138.7 | 121.6 | fail |
| tide | 1.5 | 0 | unique_transition | 23 | 0.0089 | 0.0356 | 0.0218 | 3248 | 2153.8 | 120.7 | fail |
| tide | 1.5 | 0.1 | unique_transition | 23 | 0.0137 | 0.0499 | 0.0401 | 3248 | 2137.4 | 121.6 | fail |
| tide | 0 | 0 | unique_transition | 41 | 0.0100 | 0.0410 | 0.0227 | 3248 | 2125.9 | 122.3 | fail |
| tide | 0 | 0.1 | unique_transition | 41 | 0.0124 | 0.0488 | 0.0229 | 3248 | 2146.1 | 121.2 | fail |
| tide | 1.5 | 0 | unique_transition | 41 | 0.0117 | 0.0581 | 0.0346 | 3248 | 2129.7 | 122.2 | fail |
| tide | 1.5 | 0.1 | unique_transition | 41 | 0.0088 | 0.0472 | 0.0317 | 3248 | 2138.7 | 121.7 | fail |

## Validation generation by condition and bucket

Action fidelity and preservation are pooled across seeds within each condition and bucket; thresholds are still checked for every primary condition/seed/bucket. Exact-reference match and CER are synthetic-reference metrics, not human naturalness.

| Mode | Source-copy weight | TIDE aux multiplier | Edge balance | Bucket | Checker coverage | Action fidelity | Preservation | Accepted references | CER | Nonempty | Unicode | EOS |
|---|---:|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| tide | 0 | 0 | unique_transition | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 480/480 | 465/480 | 324/480 | 310/480 | 3.3% | 480/480 | 480/480 | 480/480 |
| tide | 0 | 0 | unique_transition | en/single/POLARITY:NEGATIVE | 960/960 | 877/960 | 509/960 | 486/960 | 5.6% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | unique_transition | en/single/POLARITY:POSITIVE | 960/960 | 889/960 | 396/960 | 370/960 | 9.1% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | unique_transition | en/single/TIME:NOW | 960/960 | 847/960 | 414/960 | 400/960 | 7.7% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | unique_transition | en/single/TIME:PAST | 960/960 | 833/960 | 394/960 | 366/960 | 8.5% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | unique_transition | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 480/480 | 468/480 | 379/480 | 364/480 | 2.5% | 480/480 | 480/480 | 480/480 |
| tide | 0 | 0 | unique_transition | vi/single/POLARITY:NEGATIVE | 960/960 | 856/960 | 710/960 | 651/960 | 3.8% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | unique_transition | vi/single/POLARITY:POSITIVE | 960/960 | 849/960 | 573/960 | 496/960 | 6.3% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | unique_transition | vi/single/TIME:NOW | 960/960 | 837/960 | 628/960 | 532/960 | 5.9% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | unique_transition | vi/single/TIME:PAST | 960/960 | 785/960 | 597/960 | 574/960 | 4.7% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0.1 | unique_transition | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 480/480 | 459/480 | 335/480 | 322/480 | 2.7% | 480/480 | 480/480 | 480/480 |
| tide | 0 | 0.1 | unique_transition | en/single/POLARITY:NEGATIVE | 960/960 | 801/960 | 409/960 | 389/960 | 7.5% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0.1 | unique_transition | en/single/POLARITY:POSITIVE | 960/960 | 891/960 | 327/960 | 302/960 | 10.0% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0.1 | unique_transition | en/single/TIME:NOW | 960/960 | 819/960 | 339/960 | 324/960 | 8.6% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0.1 | unique_transition | en/single/TIME:PAST | 960/960 | 838/960 | 382/960 | 349/960 | 8.2% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0.1 | unique_transition | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 480/480 | 454/480 | 341/480 | 309/480 | 4.6% | 480/480 | 480/480 | 480/480 |
| tide | 0 | 0.1 | unique_transition | vi/single/POLARITY:NEGATIVE | 960/960 | 863/960 | 652/960 | 567/960 | 5.5% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0.1 | unique_transition | vi/single/POLARITY:POSITIVE | 960/960 | 852/960 | 533/960 | 445/960 | 6.8% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0.1 | unique_transition | vi/single/TIME:NOW | 960/960 | 900/960 | 548/960 | 433/960 | 7.0% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0.1 | unique_transition | vi/single/TIME:PAST | 960/960 | 833/960 | 585/960 | 545/960 | 5.5% | 960/960 | 960/960 | 960/960 |
| tide | 1.5 | 0 | unique_transition | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 480/480 | 441/480 | 225/480 | 216/480 | 5.7% | 480/480 | 480/480 | 480/480 |
| tide | 1.5 | 0 | unique_transition | en/single/POLARITY:NEGATIVE | 960/960 | 780/960 | 394/960 | 373/960 | 7.5% | 960/960 | 960/960 | 960/960 |
| tide | 1.5 | 0 | unique_transition | en/single/POLARITY:POSITIVE | 960/960 | 828/960 | 291/960 | 277/960 | 10.3% | 960/960 | 960/960 | 960/960 |
| tide | 1.5 | 0 | unique_transition | en/single/TIME:NOW | 960/960 | 787/960 | 351/960 | 336/960 | 8.5% | 960/960 | 960/960 | 960/960 |
| tide | 1.5 | 0 | unique_transition | en/single/TIME:PAST | 960/960 | 774/960 | 280/960 | 265/960 | 9.7% | 960/960 | 960/960 | 960/960 |
| tide | 1.5 | 0 | unique_transition | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 480/480 | 463/480 | 369/480 | 358/480 | 3.1% | 480/480 | 480/480 | 480/480 |
| tide | 1.5 | 0 | unique_transition | vi/single/POLARITY:NEGATIVE | 960/960 | 843/960 | 689/960 | 621/960 | 4.0% | 960/960 | 960/960 | 960/960 |
| tide | 1.5 | 0 | unique_transition | vi/single/POLARITY:POSITIVE | 960/960 | 763/960 | 493/960 | 449/960 | 6.3% | 960/960 | 960/960 | 960/960 |
| tide | 1.5 | 0 | unique_transition | vi/single/TIME:NOW | 960/960 | 788/960 | 595/960 | 502/960 | 6.7% | 960/960 | 960/960 | 960/960 |
| tide | 1.5 | 0 | unique_transition | vi/single/TIME:PAST | 960/960 | 763/960 | 572/960 | 554/960 | 4.3% | 960/960 | 960/960 | 960/960 |
| tide | 1.5 | 0.1 | unique_transition | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 480/480 | 407/480 | 256/480 | 233/480 | 5.8% | 480/480 | 480/480 | 480/480 |
| tide | 1.5 | 0.1 | unique_transition | en/single/POLARITY:NEGATIVE | 960/960 | 717/960 | 397/960 | 354/960 | 7.7% | 960/960 | 960/960 | 960/960 |
| tide | 1.5 | 0.1 | unique_transition | en/single/POLARITY:POSITIVE | 960/960 | 879/960 | 326/960 | 293/960 | 9.8% | 960/960 | 960/960 | 960/960 |
| tide | 1.5 | 0.1 | unique_transition | en/single/TIME:NOW | 960/960 | 775/960 | 364/960 | 343/960 | 8.2% | 960/960 | 960/960 | 960/960 |
| tide | 1.5 | 0.1 | unique_transition | en/single/TIME:PAST | 960/960 | 708/960 | 317/960 | 282/960 | 9.9% | 960/960 | 960/960 | 960/960 |
| tide | 1.5 | 0.1 | unique_transition | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 480/480 | 458/480 | 383/480 | 363/480 | 3.0% | 480/480 | 480/480 | 480/480 |
| tide | 1.5 | 0.1 | unique_transition | vi/single/POLARITY:NEGATIVE | 960/960 | 877/960 | 714/960 | 640/960 | 5.5% | 960/960 | 960/960 | 960/960 |
| tide | 1.5 | 0.1 | unique_transition | vi/single/POLARITY:POSITIVE | 960/960 | 825/960 | 627/960 | 578/960 | 5.6% | 960/960 | 960/960 | 960/960 |
| tide | 1.5 | 0.1 | unique_transition | vi/single/TIME:NOW | 960/960 | 877/960 | 691/960 | 576/960 | 6.4% | 960/960 | 960/960 | 960/960 |
| tide | 1.5 | 0.1 | unique_transition | vi/single/TIME:PAST | 960/960 | 773/960 | 665/960 | 619/960 | 4.6% | 960/960 | 960/960 | 960/960 |

## Primary-mode validation diagnostics by seed

Counts below preserve the frozen seed-by-seed gate denominator. No generated or reference text is included.

| Source-copy weight | TIDE aux multiplier | Edge balance | Seed | Bucket | Checker coverage | Action fidelity | Preservation | Accepted references | CER | Unicode | EOS | Failure reason | Bucket gate |
|---:|---:|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| 0 | 0 | unique_transition | 17 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 156/160 | 121/160 | 120/160 | 2.0% | 160/160 | 160/160 | preservation_pass | fail |
| 0 | 0 | unique_transition | 17 | en/single/POLARITY:NEGATIVE | 320/320 | 281/320 | 187/320 | 179/320 | 5.3% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | unique_transition | 17 | en/single/POLARITY:POSITIVE | 320/320 | 296/320 | 143/320 | 139/320 | 8.4% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | unique_transition | 17 | en/single/TIME:NOW | 320/320 | 283/320 | 140/320 | 133/320 | 7.8% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | unique_transition | 17 | en/single/TIME:PAST | 320/320 | 288/320 | 157/320 | 152/320 | 6.8% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | unique_transition | 17 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 153/160 | 100/160 | 91/160 | 4.7% | 160/160 | 160/160 | preservation_pass | fail |
| 0 | 0 | unique_transition | 17 | vi/single/POLARITY:NEGATIVE | 320/320 | 284/320 | 225/320 | 193/320 | 5.2% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | unique_transition | 17 | vi/single/POLARITY:POSITIVE | 320/320 | 285/320 | 163/320 | 124/320 | 8.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | unique_transition | 17 | vi/single/TIME:NOW | 320/320 | 274/320 | 199/320 | 147/320 | 7.1% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | unique_transition | 17 | vi/single/TIME:PAST | 320/320 | 274/320 | 174/320 | 156/320 | 6.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | unique_transition | 23 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 158/160 | 105/160 | 97/160 | 4.1% | 160/160 | 160/160 | preservation_pass | fail |
| 0 | 0 | unique_transition | 23 | en/single/POLARITY:NEGATIVE | 320/320 | 304/320 | 162/320 | 159/320 | 5.7% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | unique_transition | 23 | en/single/POLARITY:POSITIVE | 320/320 | 298/320 | 132/320 | 120/320 | 10.2% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | unique_transition | 23 | en/single/TIME:NOW | 320/320 | 280/320 | 146/320 | 141/320 | 8.3% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | unique_transition | 23 | en/single/TIME:PAST | 320/320 | 268/320 | 118/320 | 103/320 | 10.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | unique_transition | 23 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 156/160 | 143/160 | 137/160 | 1.4% | 160/160 | 160/160 | — | pass |
| 0 | 0 | unique_transition | 23 | vi/single/POLARITY:NEGATIVE | 320/320 | 304/320 | 253/320 | 232/320 | 2.5% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | unique_transition | 23 | vi/single/POLARITY:POSITIVE | 320/320 | 311/320 | 237/320 | 202/320 | 4.0% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | unique_transition | 23 | vi/single/TIME:NOW | 320/320 | 315/320 | 236/320 | 198/320 | 4.1% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | unique_transition | 23 | vi/single/TIME:PAST | 320/320 | 297/320 | 236/320 | 231/320 | 2.6% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | unique_transition | 41 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 151/160 | 98/160 | 93/160 | 3.9% | 160/160 | 160/160 | preservation_pass | fail |
| 0 | 0 | unique_transition | 41 | en/single/POLARITY:NEGATIVE | 320/320 | 292/320 | 160/320 | 148/320 | 5.7% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | unique_transition | 41 | en/single/POLARITY:POSITIVE | 320/320 | 295/320 | 121/320 | 111/320 | 8.7% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | unique_transition | 41 | en/single/TIME:NOW | 320/320 | 284/320 | 128/320 | 126/320 | 6.9% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | unique_transition | 41 | en/single/TIME:PAST | 320/320 | 277/320 | 119/320 | 111/320 | 8.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | unique_transition | 41 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 159/160 | 136/160 | 136/160 | 1.4% | 160/160 | 160/160 | — | pass |
| 0 | 0 | unique_transition | 41 | vi/single/POLARITY:NEGATIVE | 320/320 | 268/320 | 232/320 | 226/320 | 3.7% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | unique_transition | 41 | vi/single/POLARITY:POSITIVE | 320/320 | 253/320 | 173/320 | 170/320 | 6.7% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | unique_transition | 41 | vi/single/TIME:NOW | 320/320 | 248/320 | 193/320 | 187/320 | 6.5% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | unique_transition | 41 | vi/single/TIME:PAST | 320/320 | 214/320 | 187/320 | 187/320 | 5.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0.1 | unique_transition | 17 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 151/160 | 95/160 | 90/160 | 3.7% | 160/160 | 160/160 | preservation_pass | fail |
| 0 | 0.1 | unique_transition | 17 | en/single/POLARITY:NEGATIVE | 320/320 | 271/320 | 104/320 | 96/320 | 8.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0.1 | unique_transition | 17 | en/single/POLARITY:POSITIVE | 320/320 | 283/320 | 86/320 | 79/320 | 12.5% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0.1 | unique_transition | 17 | en/single/TIME:NOW | 320/320 | 277/320 | 75/320 | 70/320 | 10.3% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0.1 | unique_transition | 17 | en/single/TIME:PAST | 320/320 | 271/320 | 105/320 | 93/320 | 9.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0.1 | unique_transition | 17 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 156/160 | 140/160 | 131/160 | 2.4% | 160/160 | 160/160 | — | pass |
| 0 | 0.1 | unique_transition | 17 | vi/single/POLARITY:NEGATIVE | 320/320 | 305/320 | 258/320 | 226/320 | 4.1% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0.1 | unique_transition | 17 | vi/single/POLARITY:POSITIVE | 320/320 | 304/320 | 217/320 | 175/320 | 5.7% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0.1 | unique_transition | 17 | vi/single/TIME:NOW | 320/320 | 301/320 | 225/320 | 172/320 | 6.8% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0.1 | unique_transition | 17 | vi/single/TIME:PAST | 320/320 | 300/320 | 226/320 | 210/320 | 4.4% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0.1 | unique_transition | 23 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 155/160 | 114/160 | 109/160 | 2.7% | 160/160 | 160/160 | preservation_pass | fail |
| 0 | 0.1 | unique_transition | 23 | en/single/POLARITY:NEGATIVE | 320/320 | 246/320 | 145/320 | 138/320 | 8.3% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0.1 | unique_transition | 23 | en/single/POLARITY:POSITIVE | 320/320 | 305/320 | 117/320 | 103/320 | 8.6% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0.1 | unique_transition | 23 | en/single/TIME:NOW | 320/320 | 251/320 | 122/320 | 119/320 | 8.7% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0.1 | unique_transition | 23 | en/single/TIME:PAST | 320/320 | 289/320 | 142/320 | 124/320 | 7.9% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0.1 | unique_transition | 23 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 154/160 | 107/160 | 90/160 | 5.9% | 160/160 | 160/160 | preservation_pass | fail |
| 0 | 0.1 | unique_transition | 23 | vi/single/POLARITY:NEGATIVE | 320/320 | 299/320 | 203/320 | 170/320 | 5.5% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0.1 | unique_transition | 23 | vi/single/POLARITY:POSITIVE | 320/320 | 272/320 | 176/320 | 146/320 | 6.1% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0.1 | unique_transition | 23 | vi/single/TIME:NOW | 320/320 | 306/320 | 168/320 | 129/320 | 6.3% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0.1 | unique_transition | 23 | vi/single/TIME:PAST | 320/320 | 252/320 | 180/320 | 166/320 | 6.3% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0.1 | unique_transition | 41 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 153/160 | 126/160 | 123/160 | 1.7% | 160/160 | 160/160 | preservation_pass | fail |
| 0 | 0.1 | unique_transition | 41 | en/single/POLARITY:NEGATIVE | 320/320 | 284/320 | 160/320 | 155/320 | 5.8% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0.1 | unique_transition | 41 | en/single/POLARITY:POSITIVE | 320/320 | 303/320 | 124/320 | 120/320 | 9.1% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0.1 | unique_transition | 41 | en/single/TIME:NOW | 320/320 | 291/320 | 142/320 | 135/320 | 6.8% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0.1 | unique_transition | 41 | en/single/TIME:PAST | 320/320 | 278/320 | 135/320 | 132/320 | 7.1% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0.1 | unique_transition | 41 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 144/160 | 94/160 | 88/160 | 5.4% | 160/160 | 160/160 | preservation_pass | fail |
| 0 | 0.1 | unique_transition | 41 | vi/single/POLARITY:NEGATIVE | 320/320 | 259/320 | 191/320 | 171/320 | 6.9% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0.1 | unique_transition | 41 | vi/single/POLARITY:POSITIVE | 320/320 | 276/320 | 140/320 | 124/320 | 8.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0.1 | unique_transition | 41 | vi/single/TIME:NOW | 320/320 | 293/320 | 155/320 | 132/320 | 7.9% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0.1 | unique_transition | 41 | vi/single/TIME:PAST | 320/320 | 281/320 | 179/320 | 169/320 | 5.9% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0 | unique_transition | 17 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 153/160 | 62/160 | 60/160 | 5.1% | 160/160 | 160/160 | preservation_pass | fail |
| 1.5 | 0 | unique_transition | 17 | en/single/POLARITY:NEGATIVE | 320/320 | 262/320 | 88/320 | 84/320 | 8.8% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0 | unique_transition | 17 | en/single/POLARITY:POSITIVE | 320/320 | 255/320 | 69/320 | 63/320 | 11.2% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0 | unique_transition | 17 | en/single/TIME:NOW | 320/320 | 252/320 | 71/320 | 67/320 | 10.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0 | unique_transition | 17 | en/single/TIME:PAST | 320/320 | 264/320 | 86/320 | 83/320 | 8.5% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0 | unique_transition | 17 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 156/160 | 119/160 | 112/160 | 3.6% | 160/160 | 160/160 | preservation_pass | fail |
| 1.5 | 0 | unique_transition | 17 | vi/single/POLARITY:NEGATIVE | 320/320 | 295/320 | 232/320 | 201/320 | 3.7% | 320/320 | 320/320 | preservation_pass | fail |
| 1.5 | 0 | unique_transition | 17 | vi/single/POLARITY:POSITIVE | 320/320 | 279/320 | 179/320 | 154/320 | 5.8% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0 | unique_transition | 17 | vi/single/TIME:NOW | 320/320 | 272/320 | 220/320 | 174/320 | 5.8% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0 | unique_transition | 17 | vi/single/TIME:PAST | 320/320 | 285/320 | 206/320 | 194/320 | 3.5% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0 | unique_transition | 23 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 155/160 | 105/160 | 100/160 | 3.2% | 160/160 | 160/160 | preservation_pass | fail |
| 1.5 | 0 | unique_transition | 23 | en/single/POLARITY:NEGATIVE | 320/320 | 278/320 | 167/320 | 160/320 | 5.2% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0 | unique_transition | 23 | en/single/POLARITY:POSITIVE | 320/320 | 316/320 | 165/320 | 160/320 | 4.9% | 320/320 | 320/320 | preservation_pass | fail |
| 1.5 | 0 | unique_transition | 23 | en/single/TIME:NOW | 320/320 | 295/320 | 187/320 | 177/320 | 4.0% | 320/320 | 320/320 | preservation_pass | fail |
| 1.5 | 0 | unique_transition | 23 | en/single/TIME:PAST | 320/320 | 284/320 | 121/320 | 114/320 | 7.1% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0 | unique_transition | 23 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 155/160 | 125/160 | 122/160 | 2.4% | 160/160 | 160/160 | preservation_pass | fail |
| 1.5 | 0 | unique_transition | 23 | vi/single/POLARITY:NEGATIVE | 320/320 | 306/320 | 240/320 | 233/320 | 2.4% | 320/320 | 320/320 | preservation_pass | fail |
| 1.5 | 0 | unique_transition | 23 | vi/single/POLARITY:POSITIVE | 320/320 | 198/320 | 120/320 | 117/320 | 7.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0 | unique_transition | 23 | vi/single/TIME:NOW | 320/320 | 299/320 | 208/320 | 197/320 | 4.1% | 320/320 | 320/320 | preservation_pass | fail |
| 1.5 | 0 | unique_transition | 23 | vi/single/TIME:PAST | 320/320 | 208/320 | 154/320 | 151/320 | 5.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0 | unique_transition | 41 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 133/160 | 58/160 | 56/160 | 8.7% | 160/160 | 160/160 | preservation_pass | fail |
| 1.5 | 0 | unique_transition | 41 | en/single/POLARITY:NEGATIVE | 320/320 | 240/320 | 139/320 | 129/320 | 8.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0 | unique_transition | 41 | en/single/POLARITY:POSITIVE | 320/320 | 257/320 | 57/320 | 54/320 | 14.8% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0 | unique_transition | 41 | en/single/TIME:NOW | 320/320 | 240/320 | 93/320 | 92/320 | 10.9% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0 | unique_transition | 41 | en/single/TIME:PAST | 320/320 | 226/320 | 73/320 | 68/320 | 13.5% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0 | unique_transition | 41 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 152/160 | 125/160 | 124/160 | 3.3% | 160/160 | 160/160 | preservation_pass | fail |
| 1.5 | 0 | unique_transition | 41 | vi/single/POLARITY:NEGATIVE | 320/320 | 242/320 | 217/320 | 187/320 | 5.9% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0 | unique_transition | 41 | vi/single/POLARITY:POSITIVE | 320/320 | 286/320 | 194/320 | 178/320 | 5.8% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0 | unique_transition | 41 | vi/single/TIME:NOW | 320/320 | 217/320 | 167/320 | 131/320 | 10.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0 | unique_transition | 41 | vi/single/TIME:PAST | 320/320 | 270/320 | 212/320 | 209/320 | 4.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 17 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 153/160 | 81/160 | 70/160 | 5.3% | 160/160 | 160/160 | preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 17 | en/single/POLARITY:NEGATIVE | 320/320 | 282/320 | 150/320 | 121/320 | 7.9% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 17 | en/single/POLARITY:POSITIVE | 320/320 | 262/320 | 99/320 | 74/320 | 11.5% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 17 | en/single/TIME:NOW | 320/320 | 278/320 | 114/320 | 100/320 | 8.7% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 17 | en/single/TIME:PAST | 320/320 | 229/320 | 109/320 | 83/320 | 11.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 17 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 150/160 | 127/160 | 111/160 | 5.2% | 160/160 | 160/160 | preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 17 | vi/single/POLARITY:NEGATIVE | 320/320 | 282/320 | 233/320 | 184/320 | 10.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 17 | vi/single/POLARITY:POSITIVE | 320/320 | 243/320 | 166/320 | 139/320 | 9.2% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 17 | vi/single/TIME:NOW | 320/320 | 282/320 | 209/320 | 152/320 | 11.9% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 17 | vi/single/TIME:PAST | 320/320 | 236/320 | 198/320 | 169/320 | 6.5% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 23 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 122/160 | 84/160 | 79/160 | 5.8% | 160/160 | 160/160 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 23 | en/single/POLARITY:NEGATIVE | 320/320 | 226/320 | 117/320 | 113/320 | 7.2% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 23 | en/single/POLARITY:POSITIVE | 320/320 | 316/320 | 100/320 | 98/320 | 9.1% | 320/320 | 320/320 | preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 23 | en/single/TIME:NOW | 320/320 | 269/320 | 134/320 | 131/320 | 7.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 23 | en/single/TIME:PAST | 320/320 | 234/320 | 93/320 | 93/320 | 9.1% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 23 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 158/160 | 135/160 | 135/160 | 1.2% | 160/160 | 160/160 | — | pass |
| 1.5 | 0.1 | unique_transition | 23 | vi/single/POLARITY:NEGATIVE | 320/320 | 308/320 | 246/320 | 238/320 | 2.2% | 320/320 | 320/320 | preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 23 | vi/single/POLARITY:POSITIVE | 320/320 | 285/320 | 215/320 | 205/320 | 3.9% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 23 | vi/single/TIME:NOW | 320/320 | 304/320 | 264/320 | 227/320 | 2.5% | 320/320 | 320/320 | preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 23 | vi/single/TIME:PAST | 320/320 | 263/320 | 222/320 | 217/320 | 3.3% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 41 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 132/160 | 91/160 | 84/160 | 6.2% | 160/160 | 160/160 | preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 41 | en/single/POLARITY:NEGATIVE | 320/320 | 209/320 | 130/320 | 120/320 | 8.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 41 | en/single/POLARITY:POSITIVE | 320/320 | 301/320 | 127/320 | 121/320 | 8.8% | 320/320 | 320/320 | preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 41 | en/single/TIME:NOW | 320/320 | 228/320 | 116/320 | 112/320 | 8.5% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 41 | en/single/TIME:PAST | 320/320 | 245/320 | 115/320 | 106/320 | 9.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 41 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 150/160 | 121/160 | 117/160 | 2.7% | 160/160 | 160/160 | preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 41 | vi/single/POLARITY:NEGATIVE | 320/320 | 287/320 | 235/320 | 218/320 | 3.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 41 | vi/single/POLARITY:POSITIVE | 320/320 | 297/320 | 246/320 | 234/320 | 3.5% | 320/320 | 320/320 | preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 41 | vi/single/TIME:NOW | 320/320 | 291/320 | 218/320 | 197/320 | 4.6% | 320/320 | 320/320 | preservation_pass | fail |
| 1.5 | 0.1 | unique_transition | 41 | vi/single/TIME:PAST | 320/320 | 274/320 | 245/320 | 233/320 | 3.9% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |

## Limits and interpretation

Valid Unicode and EOS termination do not establish semantic correctness. The deterministic checker covers only the declared synthetic tense/polarity grammar and named roles. This benchmark tests recombination of familiar lexical factors; it does not establish naturalness, natural-corpus efficacy, or scientific efficacy. Control results are diagnostic; no TIDE advantage is claimed.

All examples and generated outputs remain private under Git-ignored `data/` and `runs/`. This report contains aggregate metrics only. `human_validated` is false. PhoMT raw/derived data and Phan Rang Cham data were not used.

Private aggregate evidence: `vi-en-ai-v4.19/protocol.json`, validation generation metrics under `vi-en-ai-v4.19`, and associated ignored run artifacts. Protocol SHA-256: `7a6f2fa674833bdd11b769ee771fdd5d7f7ab88d10b1f5576d34a5bb2b25ded3`.
