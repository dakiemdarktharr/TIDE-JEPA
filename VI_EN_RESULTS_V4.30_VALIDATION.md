# vi-en-ai-v4.30 Vi–En validation results

AI-authored and independently AI-reviewed preliminary synthetic pilot. **Not human/native-speaker validated.** PhoMT was not used. Phan Rang Cham remains excluded.

## Frozen protocol

The corpus has 15360 records and 192 event combinations. Split groups: 112/40/40; records: 8960/3200/3200 (train/validation/release holdout). Data split policy: 112/40/40 combinations from agents 71–73 × eight verbs × eight patients on a fresh split, with the shared four-form grammar and action order; train/validation-only review package and sealed release holdout for a TIDE vocabulary-versus-source-pointer decoder comparison at source-copy weight 0. Frozen release-holdout scope: The release holdout uses the same ordered action paths as train and validation; it probes fresh held-out factor combinations only and does not add an action-order shift. Transition weighting: There are 3072 duplicated path-step rows across the full split: 1792 in training, 640 in validation, and 640 in the sealed release holdout. Each logical path-step transition has one standalone single-edge record and one path-linked record. In training this adds 1792 record exposures, so those path-selected transitions contribute twice the row-wise token/edge exposure. Validation and holdout duplicates are evaluation records, not training exposure. The representation is fixed identically across conditions; results describe a path-enriched training distribution, not uniform weighting over unique transitions.

Objective conditions: tide with one-pass self-feeding rate 0 and source-copy weight 0 and TIDE latent-objective multiplier 1; language-balance weight 0; transition balance `row_uniform`; decoder `source_pointer`; tide with one-pass self-feeding rate 0 and source-copy weight 0 and TIDE latent-objective multiplier 1; language-balance weight 0; transition balance `row_uniform`; decoder `vocabulary`. Seeds 17, 23, 41; 29 epochs and 3248 updates/config; width 64, 4 heads, 2 layers. The preregistered final epoch was evaluated (`fixed_final_epoch`); validation loss did not select the checkpoint. Decoder: greedy byte-level UTF-8 constrained decoding; EOS only at complete codepoint boundaries.

The registered primary objective is `tide`. Frozen thresholds: valid Unicode 100%; checker coverage 100%; single-action fidelity ≥90% and preservation ≥90%; path fidelity ≥80% and preservation ≥80%. Every configured primary condition, seed, and language/action bucket must meet all applicable thresholds.

## Validation result: **FAIL**

Semantic checker coverage is complete across all primary buckets.

The release holdout was not evaluated and remains sealed.

| Mode | Self-feeding rate | Source-copy weight | Language-balance weight | TIDE aux multiplier | Edge balance | Decoder | Seed | Train token CE | Val token CE | Train balanced CE | Val balanced CE | Val path token CE | Updates | Training wall seconds | Mean examples/sec | Gate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tide | 0 | 0 | 0 | 1 | row_uniform | vocabulary | 17 | 0.0063 | 0.0063 | 0.0069 | 0.0068 | 0.0026 | 3248 | 2633.4 | 98.7 | fail |
| tide | 0 | 0 | 0 | 1 | row_uniform | source_pointer | 17 | 0.0040 | 0.0038 | 0.0041 | 0.0041 | 0.0017 | 3248 | 2943.6 | 88.3 | pass |
| tide | 0 | 0 | 0 | 1 | row_uniform | vocabulary | 23 | 0.0097 | 0.0091 | 0.0105 | 0.0090 | 0.0054 | 3248 | 2676.1 | 97.2 | fail |
| tide | 0 | 0 | 0 | 1 | row_uniform | source_pointer | 23 | 0.0184 | 0.0209 | 0.0196 | 0.0232 | 0.0069 | 3248 | 2947.6 | 88.2 | fail |
| tide | 0 | 0 | 0 | 1 | row_uniform | vocabulary | 41 | 0.0108 | 0.0135 | 0.0116 | 0.0149 | 0.0087 | 3248 | 2087.3 | 125.5 | fail |
| tide | 0 | 0 | 0 | 1 | row_uniform | source_pointer | 41 | 0.0149 | 0.0302 | 0.0150 | 0.0297 | 0.0166 | 3248 | 2267.5 | 115.6 | fail |

## Validation generation by condition and bucket

Action fidelity, preservation, and context-marker counts are pooled across seeds within each condition and bucket; thresholds are still checked for every primary condition/seed/bucket. Exact-reference match and CER are synthetic-reference metrics, not human naturalness.

| Mode | Self-feeding rate | Source-copy weight | Language-balance weight | TIDE aux multiplier | Edge balance | Decoder | Bucket | Checker coverage | Action fidelity | Preservation | Context marker | Accepted references | CER | Nonempty | Unicode | EOS |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tide | 0 | 0 | 0 | 1 | row_uniform | source_pointer | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 480/480 | 479/480 | 418/480 | 475/480 | 410/480 | 0.9% | 480/480 | 480/480 | 480/480 |
| tide | 0 | 0 | 0 | 1 | row_uniform | source_pointer | en/single/POLARITY:NEGATIVE | 960/960 | 921/960 | 775/960 | 934/960 | 738/960 | 2.0% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 0 | 1 | row_uniform | source_pointer | en/single/POLARITY:POSITIVE | 960/960 | 883/960 | 681/960 | 937/960 | 621/960 | 3.9% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 0 | 1 | row_uniform | source_pointer | en/single/TIME:NOW | 960/960 | 878/960 | 699/960 | 928/960 | 651/960 | 3.2% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 0 | 1 | row_uniform | source_pointer | en/single/TIME:PAST | 960/960 | 812/960 | 661/960 | 945/960 | 625/960 | 4.8% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 0 | 1 | row_uniform | source_pointer | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 480/480 | 465/480 | 433/480 | 464/480 | 429/480 | 1.3% | 480/480 | 480/480 | 480/480 |
| tide | 0 | 0 | 0 | 1 | row_uniform | source_pointer | vi/single/POLARITY:NEGATIVE | 960/960 | 913/960 | 813/960 | 910/960 | 795/960 | 2.2% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 0 | 1 | row_uniform | source_pointer | vi/single/POLARITY:POSITIVE | 960/960 | 908/960 | 774/960 | 915/960 | 757/960 | 2.6% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 0 | 1 | row_uniform | source_pointer | vi/single/TIME:NOW | 960/960 | 922/960 | 787/960 | 912/960 | 772/960 | 2.7% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 0 | 1 | row_uniform | source_pointer | vi/single/TIME:PAST | 960/960 | 887/960 | 769/960 | 920/960 | 757/960 | 2.5% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 0 | 1 | row_uniform | vocabulary | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 480/480 | 477/480 | 408/480 | 480/480 | 405/480 | 0.8% | 480/480 | 480/480 | 480/480 |
| tide | 0 | 0 | 0 | 1 | row_uniform | vocabulary | en/single/POLARITY:NEGATIVE | 960/960 | 950/960 | 763/960 | 952/960 | 752/960 | 1.7% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 0 | 1 | row_uniform | vocabulary | en/single/POLARITY:POSITIVE | 960/960 | 952/960 | 712/960 | 946/960 | 697/960 | 2.4% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 0 | 1 | row_uniform | vocabulary | en/single/TIME:NOW | 960/960 | 945/960 | 738/960 | 948/960 | 719/960 | 2.0% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 0 | 1 | row_uniform | vocabulary | en/single/TIME:PAST | 960/960 | 913/960 | 701/960 | 954/960 | 693/960 | 2.9% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 0 | 1 | row_uniform | vocabulary | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 480/480 | 461/480 | 456/480 | 480/480 | 455/480 | 0.5% | 480/480 | 480/480 | 480/480 |
| tide | 0 | 0 | 0 | 1 | row_uniform | vocabulary | vi/single/POLARITY:NEGATIVE | 960/960 | 913/960 | 885/960 | 959/960 | 883/960 | 0.8% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 0 | 1 | row_uniform | vocabulary | vi/single/POLARITY:POSITIVE | 960/960 | 954/960 | 911/960 | 959/960 | 909/960 | 0.7% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 0 | 1 | row_uniform | vocabulary | vi/single/TIME:NOW | 960/960 | 925/960 | 888/960 | 958/960 | 880/960 | 0.8% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 0 | 1 | row_uniform | vocabulary | vi/single/TIME:PAST | 960/960 | 907/960 | 883/960 | 958/960 | 881/960 | 0.8% | 960/960 | 960/960 | 960/960 |

## Primary-mode validation diagnostics by seed

Counts below preserve the frozen seed-by-seed gate denominator. No generated or reference text is included.

| Self-feeding rate | Source-copy weight | Language-balance weight | TIDE aux multiplier | Edge balance | Decoder | Seed | Bucket | Checker coverage | Action fidelity | Preservation | Context marker | Accepted references | CER | Unicode | EOS | Failure reason | Bucket gate |
|---:|---:|---:|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 17 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 160/160 | 152/160 | 160/160 | 152/160 | 0.2% | 160/160 | 160/160 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 17 | en/single/POLARITY:NEGATIVE | 320/320 | 320/320 | 297/320 | 320/320 | 297/320 | 0.3% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 17 | en/single/POLARITY:POSITIVE | 320/320 | 319/320 | 294/320 | 318/320 | 289/320 | 0.8% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 17 | en/single/TIME:NOW | 320/320 | 317/320 | 296/320 | 319/320 | 293/320 | 0.6% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 17 | en/single/TIME:PAST | 320/320 | 316/320 | 291/320 | 319/320 | 288/320 | 1.0% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 17 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 160/160 | 160/160 | 160/160 | 160/160 | 0.0% | 160/160 | 160/160 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 17 | vi/single/POLARITY:NEGATIVE | 320/320 | 319/320 | 318/320 | 320/320 | 317/320 | 0.1% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 17 | vi/single/POLARITY:POSITIVE | 320/320 | 318/320 | 313/320 | 319/320 | 313/320 | 0.2% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 17 | vi/single/TIME:NOW | 320/320 | 319/320 | 309/320 | 320/320 | 309/320 | 0.3% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 17 | vi/single/TIME:PAST | 320/320 | 316/320 | 312/320 | 320/320 | 312/320 | 0.2% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 23 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 159/160 | 135/160 | 155/160 | 132/160 | 1.3% | 160/160 | 160/160 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 23 | en/single/POLARITY:NEGATIVE | 320/320 | 296/320 | 227/320 | 305/320 | 206/320 | 2.5% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 23 | en/single/POLARITY:POSITIVE | 320/320 | 263/320 | 171/320 | 307/320 | 134/320 | 6.9% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 23 | en/single/TIME:NOW | 320/320 | 260/320 | 175/320 | 299/320 | 148/320 | 5.2% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 23 | en/single/TIME:PAST | 320/320 | 185/320 | 142/320 | 310/320 | 129/320 | 10.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 23 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 160/160 | 158/160 | 159/160 | 158/160 | 0.1% | 160/160 | 160/160 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 23 | vi/single/POLARITY:NEGATIVE | 320/320 | 317/320 | 305/320 | 318/320 | 304/320 | 0.7% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 23 | vi/single/POLARITY:POSITIVE | 320/320 | 312/320 | 290/320 | 320/320 | 286/320 | 1.0% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 23 | vi/single/TIME:NOW | 320/320 | 311/320 | 291/320 | 317/320 | 287/320 | 0.8% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 23 | vi/single/TIME:PAST | 320/320 | 308/320 | 281/320 | 317/320 | 281/320 | 1.1% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 41 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 160/160 | 131/160 | 160/160 | 126/160 | 1.2% | 160/160 | 160/160 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 41 | en/single/POLARITY:NEGATIVE | 320/320 | 305/320 | 251/320 | 309/320 | 235/320 | 3.3% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 41 | en/single/POLARITY:POSITIVE | 320/320 | 301/320 | 216/320 | 312/320 | 198/320 | 4.0% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 41 | en/single/TIME:NOW | 320/320 | 301/320 | 228/320 | 310/320 | 210/320 | 3.6% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 41 | en/single/TIME:PAST | 320/320 | 311/320 | 228/320 | 316/320 | 208/320 | 2.9% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 41 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 145/160 | 115/160 | 145/160 | 111/160 | 3.8% | 160/160 | 160/160 | preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 41 | vi/single/POLARITY:NEGATIVE | 320/320 | 277/320 | 190/320 | 272/320 | 174/320 | 5.7% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 41 | vi/single/POLARITY:POSITIVE | 320/320 | 278/320 | 171/320 | 276/320 | 158/320 | 6.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 41 | vi/single/TIME:NOW | 320/320 | 292/320 | 187/320 | 275/320 | 176/320 | 7.1% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 41 | vi/single/TIME:PAST | 320/320 | 263/320 | 176/320 | 283/320 | 164/320 | 6.2% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 17 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 160/160 | 149/160 | 160/160 | 149/160 | 0.2% | 160/160 | 160/160 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 17 | en/single/POLARITY:NEGATIVE | 320/320 | 316/320 | 269/320 | 317/320 | 264/320 | 1.5% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 17 | en/single/POLARITY:POSITIVE | 320/320 | 318/320 | 268/320 | 319/320 | 265/320 | 1.3% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 17 | en/single/TIME:NOW | 320/320 | 311/320 | 265/320 | 319/320 | 252/320 | 1.7% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 17 | en/single/TIME:PAST | 320/320 | 315/320 | 268/320 | 320/320 | 265/320 | 1.5% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 17 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 160/160 | 158/160 | 160/160 | 157/160 | 0.1% | 160/160 | 160/160 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 17 | vi/single/POLARITY:NEGATIVE | 320/320 | 319/320 | 316/320 | 320/320 | 314/320 | 0.1% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 17 | vi/single/POLARITY:POSITIVE | 320/320 | 318/320 | 318/320 | 320/320 | 318/320 | 0.1% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 17 | vi/single/TIME:NOW | 320/320 | 319/320 | 317/320 | 320/320 | 316/320 | 0.1% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 17 | vi/single/TIME:PAST | 320/320 | 320/320 | 315/320 | 318/320 | 314/320 | 0.1% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 23 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 158/160 | 146/160 | 160/160 | 143/160 | 0.5% | 160/160 | 160/160 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 23 | en/single/POLARITY:NEGATIVE | 320/320 | 316/320 | 285/320 | 320/320 | 282/320 | 1.1% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 23 | en/single/POLARITY:POSITIVE | 320/320 | 318/320 | 265/320 | 318/320 | 265/320 | 1.5% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 23 | en/single/TIME:NOW | 320/320 | 317/320 | 286/320 | 319/320 | 283/320 | 1.0% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 23 | en/single/TIME:PAST | 320/320 | 314/320 | 270/320 | 318/320 | 268/320 | 1.4% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 23 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 141/160 | 138/160 | 160/160 | 138/160 | 1.3% | 160/160 | 160/160 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 23 | vi/single/POLARITY:NEGATIVE | 320/320 | 274/320 | 269/320 | 319/320 | 269/320 | 1.9% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 23 | vi/single/POLARITY:POSITIVE | 320/320 | 318/320 | 295/320 | 319/320 | 295/320 | 1.0% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 23 | vi/single/TIME:NOW | 320/320 | 292/320 | 285/320 | 319/320 | 284/320 | 1.4% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 23 | vi/single/TIME:PAST | 320/320 | 267/320 | 260/320 | 320/320 | 260/320 | 1.8% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 41 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 159/160 | 113/160 | 160/160 | 113/160 | 1.8% | 160/160 | 160/160 | preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 41 | en/single/POLARITY:NEGATIVE | 320/320 | 318/320 | 209/320 | 315/320 | 206/320 | 2.5% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 41 | en/single/POLARITY:POSITIVE | 320/320 | 316/320 | 179/320 | 309/320 | 167/320 | 4.5% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 41 | en/single/TIME:NOW | 320/320 | 317/320 | 187/320 | 310/320 | 184/320 | 3.4% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 41 | en/single/TIME:PAST | 320/320 | 284/320 | 163/320 | 316/320 | 160/320 | 5.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 41 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 160/160 | 160/160 | 160/160 | 160/160 | 0.0% | 160/160 | 160/160 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 41 | vi/single/POLARITY:NEGATIVE | 320/320 | 320/320 | 300/320 | 320/320 | 300/320 | 0.4% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 41 | vi/single/POLARITY:POSITIVE | 320/320 | 318/320 | 298/320 | 320/320 | 296/320 | 0.9% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 41 | vi/single/TIME:NOW | 320/320 | 314/320 | 286/320 | 319/320 | 280/320 | 0.9% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 41 | vi/single/TIME:PAST | 320/320 | 320/320 | 308/320 | 320/320 | 307/320 | 0.4% | 320/320 | 320/320 | — | pass |

## Limits and interpretation

Valid Unicode and EOS termination do not establish semantic correctness. The deterministic checker covers only the declared synthetic tense/polarity grammar and named roles. This benchmark tests recombination of familiar lexical factors; it does not establish naturalness, natural-corpus efficacy, or scientific efficacy. Control results are diagnostic; no TIDE advantage is claimed.

All examples and generated outputs remain private under Git-ignored `data/` and `runs/`. This report contains aggregate metrics only. `human_validated` is false. PhoMT raw/derived data and Phan Rang Cham data were not used.

Private aggregate evidence: `vi-en-ai-v4.30/protocol.json`, validation generation metrics under `vi-en-ai-v4.30`, and associated ignored run artifacts. Protocol SHA-256: `748119b1291ada27dec2731a2e53e7a0c9e8d16d804f0c113c408fdbdbf9dc77`.
