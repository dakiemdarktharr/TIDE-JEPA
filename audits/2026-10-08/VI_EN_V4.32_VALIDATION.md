# vi-en-ai-v4.32 Vi–En validation results

AI-authored and independently AI-reviewed preliminary synthetic pilot. **Not human/native-speaker validated.** PhoMT was not used. Phan Rang Cham remains excluded.

## Frozen protocol

The corpus has 15360 records and 192 event combinations. Split groups: 112/40/40; records: 8960/3200/3200 (train/validation/release holdout). Data split policy: 112/40/40 combinations from fresh agents 77–79 × eight verbs × eight patients; deterministic split seed 20261035, shared four-form grammar/action order; train/validation-only review bundle and fresh sealed release holdout for a three-seed TIDE vocabulary versus source-pointer decoder comparison. Frozen release-holdout scope: The release holdout uses the same ordered action paths as train and validation; it probes fresh held-out factor combinations only and does not add an action-order shift. Transition weighting: There are 3072 duplicated path-step rows across the full split: 1792 in training, 640 in validation, and 640 in the sealed release holdout. Each logical path-step transition has one standalone single-edge record and one path-linked record. In training this adds 1792 record exposures, so those path-selected transitions contribute twice the row-wise token/edge exposure. Validation and holdout duplicates are evaluation records, not training exposure. The representation is fixed identically across conditions; results describe a path-enriched training distribution, not uniform weighting over unique transitions.

Objective conditions: tide with one-pass self-feeding rate 0 and source-copy weight 0 and TIDE latent-objective multiplier 1; language-balance weight 0; transition balance `row_uniform`; decoder `source_pointer`; tide with one-pass self-feeding rate 0 and source-copy weight 0 and TIDE latent-objective multiplier 1; language-balance weight 0; transition balance `row_uniform`; decoder `vocabulary`. Seeds 17, 23, 41; 29 epochs and 3248 updates/config; width 64, 4 heads, 2 layers. The preregistered final epoch was evaluated (`fixed_final_epoch`); validation loss did not select the checkpoint. Decoder: greedy byte-level UTF-8 constrained decoding; EOS only at complete codepoint boundaries.

The registered primary objective is `tide`. Frozen thresholds: valid Unicode 100%; checker coverage 100%; single-action fidelity ≥90% and preservation ≥90%; path fidelity ≥80% and preservation ≥80%. Every configured primary condition, seed, and language/action bucket must meet all applicable thresholds.

## Validation result: **FAIL**

Semantic checker coverage is complete across all primary buckets.

The release holdout was not evaluated and remains sealed.

| Mode | Self-feeding rate | Source-copy weight | Language-balance weight | TIDE aux multiplier | Edge balance | Decoder | Seed | Train token CE | Val token CE | Train balanced CE | Val balanced CE | Val path token CE | Updates | Training wall seconds | Mean examples/sec | Gate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tide | 0 | 0 | 0 | 1 | row_uniform | vocabulary | 17 | 0.0096 | 0.0090 | 0.0105 | 0.0095 | 0.0038 | 3248 | 2722.3 | 95.5 | fail |
| tide | 0 | 0 | 0 | 1 | row_uniform | source_pointer | 17 | 0.0129 | 0.0177 | 0.0145 | 0.0194 | 0.0083 | 3248 | 3029.1 | 85.8 | fail |
| tide | 0 | 0 | 0 | 1 | row_uniform | vocabulary | 23 | 0.0150 | 0.0227 | 0.0158 | 0.0250 | 0.0101 | 3248 | 2676.1 | 97.2 | fail |
| tide | 0 | 0 | 0 | 1 | row_uniform | source_pointer | 23 | 0.0195 | 0.0204 | 0.0216 | 0.0228 | 0.0089 | 3248 | 3057.8 | 85.0 | fail |
| tide | 0 | 0 | 0 | 1 | row_uniform | vocabulary | 41 | 0.0136 | 0.0244 | 0.0148 | 0.0268 | 0.0161 | 3248 | 2089.9 | 125.6 | fail |
| tide | 0 | 0 | 0 | 1 | row_uniform | source_pointer | 41 | 0.0098 | 0.0102 | 0.0108 | 0.0113 | 0.0048 | 3248 | 2299.3 | 114.1 | fail |

## Validation generation by condition and bucket

Action fidelity, preservation, and context-marker counts are pooled across seeds within each condition and bucket; thresholds are still checked for every primary condition/seed/bucket. Exact-reference match and CER are synthetic-reference metrics, not human naturalness.

| Mode | Self-feeding rate | Source-copy weight | Language-balance weight | TIDE aux multiplier | Edge balance | Decoder | Bucket | Checker coverage | Action fidelity | Preservation | Context marker | Accepted references | CER | Nonempty | Unicode | EOS |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tide | 0 | 0 | 0 | 1 | row_uniform | source_pointer | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 480/480 | 471/480 | 390/480 | 473/480 | 385/480 | 0.9% | 480/480 | 480/480 | 480/480 |
| tide | 0 | 0 | 0 | 1 | row_uniform | source_pointer | en/single/POLARITY:NEGATIVE | 960/960 | 912/960 | 646/960 | 929/960 | 623/960 | 2.6% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 0 | 1 | row_uniform | source_pointer | en/single/POLARITY:POSITIVE | 960/960 | 750/960 | 478/960 | 917/960 | 434/960 | 6.9% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 0 | 1 | row_uniform | source_pointer | en/single/TIME:NOW | 960/960 | 788/960 | 494/960 | 911/960 | 457/960 | 5.4% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 0 | 1 | row_uniform | source_pointer | en/single/TIME:PAST | 960/960 | 833/960 | 626/960 | 930/960 | 596/960 | 4.7% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 0 | 1 | row_uniform | source_pointer | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 480/480 | 479/480 | 471/480 | 479/480 | 469/480 | 0.2% | 480/480 | 480/480 | 480/480 |
| tide | 0 | 0 | 0 | 1 | row_uniform | source_pointer | vi/single/POLARITY:NEGATIVE | 960/960 | 955/960 | 918/960 | 956/960 | 910/960 | 0.4% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 0 | 1 | row_uniform | source_pointer | vi/single/POLARITY:POSITIVE | 960/960 | 944/960 | 891/960 | 951/960 | 879/960 | 1.0% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 0 | 1 | row_uniform | source_pointer | vi/single/TIME:NOW | 960/960 | 939/960 | 896/960 | 957/960 | 882/960 | 0.6% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 0 | 1 | row_uniform | source_pointer | vi/single/TIME:PAST | 960/960 | 927/960 | 871/960 | 955/960 | 864/960 | 1.0% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 0 | 1 | row_uniform | vocabulary | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 480/480 | 471/480 | 351/480 | 480/480 | 345/480 | 2.0% | 480/480 | 480/480 | 480/480 |
| tide | 0 | 0 | 0 | 1 | row_uniform | vocabulary | en/single/POLARITY:NEGATIVE | 960/960 | 903/960 | 574/960 | 948/960 | 551/960 | 4.1% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 0 | 1 | row_uniform | vocabulary | en/single/POLARITY:POSITIVE | 960/960 | 844/960 | 501/960 | 943/960 | 474/960 | 5.8% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 0 | 1 | row_uniform | vocabulary | en/single/TIME:NOW | 960/960 | 783/960 | 493/960 | 938/960 | 462/960 | 5.8% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 0 | 1 | row_uniform | vocabulary | en/single/TIME:PAST | 960/960 | 849/960 | 551/960 | 953/960 | 538/960 | 5.3% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 0 | 1 | row_uniform | vocabulary | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 480/480 | 478/480 | 476/480 | 479/480 | 473/480 | 0.2% | 480/480 | 480/480 | 480/480 |
| tide | 0 | 0 | 0 | 1 | row_uniform | vocabulary | vi/single/POLARITY:NEGATIVE | 960/960 | 935/960 | 913/960 | 951/960 | 886/960 | 1.0% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 0 | 1 | row_uniform | vocabulary | vi/single/POLARITY:POSITIVE | 960/960 | 913/960 | 883/960 | 957/960 | 849/960 | 1.6% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 0 | 1 | row_uniform | vocabulary | vi/single/TIME:NOW | 960/960 | 935/960 | 865/960 | 947/960 | 854/960 | 1.3% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 0 | 1 | row_uniform | vocabulary | vi/single/TIME:PAST | 960/960 | 918/960 | 882/960 | 960/960 | 866/960 | 1.1% | 960/960 | 960/960 | 960/960 |

## Primary-mode validation diagnostics by seed

Counts below preserve the frozen seed-by-seed gate denominator. No generated or reference text is included.

| Self-feeding rate | Source-copy weight | Language-balance weight | TIDE aux multiplier | Edge balance | Decoder | Seed | Bucket | Checker coverage | Action fidelity | Preservation | Context marker | Accepted references | CER | Unicode | EOS | Failure reason | Bucket gate |
|---:|---:|---:|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 17 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 157/160 | 128/160 | 159/160 | 124/160 | 1.1% | 160/160 | 160/160 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 17 | en/single/POLARITY:NEGATIVE | 320/320 | 295/320 | 214/320 | 313/320 | 201/320 | 2.9% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 17 | en/single/POLARITY:POSITIVE | 320/320 | 243/320 | 146/320 | 305/320 | 131/320 | 6.8% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 17 | en/single/TIME:NOW | 320/320 | 271/320 | 174/320 | 299/320 | 151/320 | 5.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 17 | en/single/TIME:PAST | 320/320 | 278/320 | 210/320 | 317/320 | 195/320 | 4.5% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 17 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 160/160 | 157/160 | 160/160 | 156/160 | 0.1% | 160/160 | 160/160 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 17 | vi/single/POLARITY:NEGATIVE | 320/320 | 319/320 | 307/320 | 318/320 | 304/320 | 0.4% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 17 | vi/single/POLARITY:POSITIVE | 320/320 | 314/320 | 299/320 | 317/320 | 292/320 | 1.3% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 17 | vi/single/TIME:NOW | 320/320 | 311/320 | 290/320 | 318/320 | 284/320 | 0.9% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 17 | vi/single/TIME:PAST | 320/320 | 313/320 | 294/320 | 320/320 | 290/320 | 0.8% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 23 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 154/160 | 130/160 | 154/160 | 129/160 | 1.1% | 160/160 | 160/160 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 23 | en/single/POLARITY:NEGATIVE | 320/320 | 301/320 | 206/320 | 301/320 | 198/320 | 3.2% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 23 | en/single/POLARITY:POSITIVE | 320/320 | 212/320 | 127/320 | 297/320 | 106/320 | 11.1% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 23 | en/single/TIME:NOW | 320/320 | 241/320 | 134/320 | 300/320 | 123/320 | 6.8% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 23 | en/single/TIME:PAST | 320/320 | 245/320 | 170/320 | 294/320 | 163/320 | 8.2% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 23 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 160/160 | 156/160 | 160/160 | 155/160 | 0.2% | 160/160 | 160/160 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 23 | vi/single/POLARITY:NEGATIVE | 320/320 | 317/320 | 301/320 | 318/320 | 299/320 | 0.7% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 23 | vi/single/POLARITY:POSITIVE | 320/320 | 313/320 | 279/320 | 315/320 | 277/320 | 1.5% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 23 | vi/single/TIME:NOW | 320/320 | 313/320 | 299/320 | 320/320 | 293/320 | 0.7% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 23 | vi/single/TIME:PAST | 320/320 | 318/320 | 285/320 | 315/320 | 284/320 | 1.2% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 41 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 160/160 | 132/160 | 160/160 | 132/160 | 0.5% | 160/160 | 160/160 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 41 | en/single/POLARITY:NEGATIVE | 320/320 | 316/320 | 226/320 | 315/320 | 224/320 | 1.6% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 41 | en/single/POLARITY:POSITIVE | 320/320 | 295/320 | 205/320 | 315/320 | 197/320 | 3.0% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 41 | en/single/TIME:NOW | 320/320 | 276/320 | 186/320 | 312/320 | 183/320 | 3.7% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 41 | en/single/TIME:PAST | 320/320 | 310/320 | 246/320 | 319/320 | 238/320 | 1.6% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 41 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 159/160 | 158/160 | 159/160 | 158/160 | 0.2% | 160/160 | 160/160 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 41 | vi/single/POLARITY:NEGATIVE | 320/320 | 319/320 | 310/320 | 320/320 | 307/320 | 0.3% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 41 | vi/single/POLARITY:POSITIVE | 320/320 | 317/320 | 313/320 | 319/320 | 310/320 | 0.3% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 41 | vi/single/TIME:NOW | 320/320 | 315/320 | 307/320 | 319/320 | 305/320 | 0.4% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | source_pointer | 41 | vi/single/TIME:PAST | 320/320 | 296/320 | 292/320 | 320/320 | 290/320 | 0.9% | 320/320 | 320/320 | — | pass |

## Limits and interpretation

Valid Unicode and EOS termination do not establish semantic correctness. The deterministic checker covers only the declared synthetic tense/polarity grammar and named roles. This benchmark tests recombination of familiar lexical factors; it does not establish naturalness, natural-corpus efficacy, or scientific efficacy. Control results are diagnostic; no TIDE advantage is claimed.

All examples and generated outputs remain private under Git-ignored `data/` and `runs/`. This report contains aggregate metrics only. `human_validated` is false. PhoMT raw/derived data and Phan Rang Cham data were not used.

Private aggregate evidence: `vi-en-ai-v4.32/protocol.json`, validation generation metrics under `vi-en-ai-v4.32`, and associated ignored run artifacts. Protocol SHA-256: `c288e9749402282ff27f2279e33ad13b58ee6c96612695ba41711bffcd5b0524`.
