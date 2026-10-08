# vi-en-ai-v4.31 Vi–En validation results

AI-authored and independently AI-reviewed preliminary synthetic pilot. **Not human/native-speaker validated.** PhoMT was not used. Phan Rang Cham remains excluded.

## Frozen protocol

The corpus has 15360 records and 192 event combinations. Split groups: 112/40/40; records: 8960/3200/3200 (train/validation/release holdout). Data split policy: 112/40/40 combinations from fresh agents 74–76 × eight verbs × eight patients; deterministic split seed 20261034, shared four-form grammar/action order; isolated train/validation review bundle and fresh sealed release holdout for a three-seed TIDE versus token-only objective comparison. Frozen release-holdout scope: The release holdout uses the same ordered action paths as train and validation; it probes fresh held-out factor combinations only and does not add an action-order shift. Transition weighting: There are 3072 duplicated path-step rows across the full split: 1792 in training, 640 in validation, and 640 in the sealed release holdout. Each logical path-step transition has one standalone single-edge record and one path-linked record. In training this adds 1792 record exposures, so those path-selected transitions contribute twice the row-wise token/edge exposure. Validation and holdout duplicates are evaluation records, not training exposure. The representation is fixed identically across conditions; results describe a path-enriched training distribution, not uniform weighting over unique transitions.

Objective conditions: tide with one-pass self-feeding rate 0 and source-copy weight 0 and TIDE latent-objective multiplier 1; language-balance weight 0; transition balance `row_uniform`; decoder `vocabulary`; token_only with one-pass self-feeding rate 0 and source-copy weight 0; language-balance weight 0; transition balance `row_uniform`; decoder `vocabulary`. Seeds 17, 23, 41; 29 epochs and 3248 updates/config; width 64, 4 heads, 2 layers. The preregistered final epoch was evaluated (`fixed_final_epoch`); validation loss did not select the checkpoint. Decoder: greedy byte-level UTF-8 constrained decoding; EOS only at complete codepoint boundaries.

The registered primary objective is `tide`. Frozen thresholds: valid Unicode 100%; checker coverage 100%; single-action fidelity ≥90% and preservation ≥90%; path fidelity ≥80% and preservation ≥80%. Every configured primary condition, seed, and language/action bucket must meet all applicable thresholds.

## Validation result: **FAIL**

Semantic checker coverage is complete across all primary buckets.

The release holdout was not evaluated and remains sealed.

| Mode | Self-feeding rate | Source-copy weight | Language-balance weight | TIDE aux multiplier | Edge balance | Decoder | Seed | Train token CE | Val token CE | Train balanced CE | Val balanced CE | Val path token CE | Updates | Training wall seconds | Mean examples/sec | Gate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tide | 0 | 0 | 0 | 1 | row_uniform | vocabulary | 17 | 0.0057 | 0.0073 | 0.0062 | 0.0078 | 0.0044 | 3248 | 2672.5 | 97.3 | fail |
| token_only | 0 | 0 | 0 | — | row_uniform | vocabulary | 17 | 0.0007 | 0.0020 | 0.0007 | 0.0021 | 0.0009 | 3248 | 2404.7 | 108.1 | control_only |
| tide | 0 | 0 | 0 | 1 | row_uniform | vocabulary | 23 | 0.0094 | 0.0104 | 0.0098 | 0.0109 | 0.0060 | 3248 | 2673.3 | 97.2 | fail |
| token_only | 0 | 0 | 0 | — | row_uniform | vocabulary | 23 | 0.0200 | 0.0137 | 0.0214 | 0.0146 | 0.0114 | 3248 | 2407.9 | 108.0 | control_only |
| tide | 0 | 0 | 0 | 1 | row_uniform | vocabulary | 41 | 0.0201 | 0.0185 | 0.0214 | 0.0192 | 0.0139 | 3248 | 2154.9 | 121.5 | fail |
| token_only | 0 | 0 | 0 | — | row_uniform | vocabulary | 41 | 0.0031 | 0.0044 | 0.0033 | 0.0046 | 0.0016 | 3248 | 1927.5 | 136.0 | control_only |

## Validation generation by condition and bucket

Action fidelity, preservation, and context-marker counts are pooled across seeds within each condition and bucket; thresholds are still checked for every primary condition/seed/bucket. Exact-reference match and CER are synthetic-reference metrics, not human naturalness.

| Mode | Self-feeding rate | Source-copy weight | Language-balance weight | TIDE aux multiplier | Edge balance | Decoder | Bucket | Checker coverage | Action fidelity | Preservation | Context marker | Accepted references | CER | Nonempty | Unicode | EOS |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tide | 0 | 0 | 0 | 1 | row_uniform | vocabulary | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 480/480 | 476/480 | 378/480 | 480/480 | 377/480 | 1.3% | 480/480 | 480/480 | 480/480 |
| tide | 0 | 0 | 0 | 1 | row_uniform | vocabulary | en/single/POLARITY:NEGATIVE | 960/960 | 923/960 | 660/960 | 959/960 | 654/960 | 2.5% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 0 | 1 | row_uniform | vocabulary | en/single/POLARITY:POSITIVE | 960/960 | 951/960 | 662/960 | 956/960 | 654/960 | 2.7% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 0 | 1 | row_uniform | vocabulary | en/single/TIME:NOW | 960/960 | 932/960 | 679/960 | 956/960 | 670/960 | 2.6% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 0 | 1 | row_uniform | vocabulary | en/single/TIME:PAST | 960/960 | 907/960 | 683/960 | 960/960 | 677/960 | 2.8% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 0 | 1 | row_uniform | vocabulary | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 480/480 | 480/480 | 441/480 | 480/480 | 441/480 | 1.0% | 480/480 | 480/480 | 480/480 |
| tide | 0 | 0 | 0 | 1 | row_uniform | vocabulary | vi/single/POLARITY:NEGATIVE | 960/960 | 944/960 | 898/960 | 960/960 | 879/960 | 1.8% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 0 | 1 | row_uniform | vocabulary | vi/single/POLARITY:POSITIVE | 960/960 | 925/960 | 852/960 | 957/960 | 833/960 | 1.8% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 0 | 1 | row_uniform | vocabulary | vi/single/TIME:NOW | 960/960 | 930/960 | 891/960 | 959/960 | 863/960 | 1.5% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 0 | 1 | row_uniform | vocabulary | vi/single/TIME:PAST | 960/960 | 916/960 | 808/960 | 955/960 | 799/960 | 2.2% | 960/960 | 960/960 | 960/960 |
| token_only | 0 | 0 | 0 | — | row_uniform | vocabulary | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 480/480 | 480/480 | 407/480 | 479/480 | 407/480 | 0.7% | 480/480 | 480/480 | 480/480 |
| token_only | 0 | 0 | 0 | — | row_uniform | vocabulary | en/single/POLARITY:NEGATIVE | 960/960 | 957/960 | 799/960 | 957/960 | 796/960 | 1.0% | 960/960 | 960/960 | 960/960 |
| token_only | 0 | 0 | 0 | — | row_uniform | vocabulary | en/single/POLARITY:POSITIVE | 960/960 | 955/960 | 790/960 | 954/960 | 776/960 | 1.2% | 960/960 | 960/960 | 960/960 |
| token_only | 0 | 0 | 0 | — | row_uniform | vocabulary | en/single/TIME:NOW | 960/960 | 946/960 | 775/960 | 954/960 | 769/960 | 1.4% | 960/960 | 960/960 | 960/960 |
| token_only | 0 | 0 | 0 | — | row_uniform | vocabulary | en/single/TIME:PAST | 960/960 | 945/960 | 794/960 | 956/960 | 785/960 | 1.3% | 960/960 | 960/960 | 960/960 |
| token_only | 0 | 0 | 0 | — | row_uniform | vocabulary | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 480/480 | 480/480 | 477/480 | 480/480 | 477/480 | 0.0% | 480/480 | 480/480 | 480/480 |
| token_only | 0 | 0 | 0 | — | row_uniform | vocabulary | vi/single/POLARITY:NEGATIVE | 960/960 | 954/960 | 931/960 | 957/960 | 927/960 | 0.5% | 960/960 | 960/960 | 960/960 |
| token_only | 0 | 0 | 0 | — | row_uniform | vocabulary | vi/single/POLARITY:POSITIVE | 960/960 | 943/960 | 922/960 | 959/960 | 919/960 | 0.5% | 960/960 | 960/960 | 960/960 |
| token_only | 0 | 0 | 0 | — | row_uniform | vocabulary | vi/single/TIME:NOW | 960/960 | 953/960 | 931/960 | 958/960 | 927/960 | 0.5% | 960/960 | 960/960 | 960/960 |
| token_only | 0 | 0 | 0 | — | row_uniform | vocabulary | vi/single/TIME:PAST | 960/960 | 952/960 | 925/960 | 960/960 | 922/960 | 0.4% | 960/960 | 960/960 | 960/960 |

## Primary-mode validation diagnostics by seed

Counts below preserve the frozen seed-by-seed gate denominator. No generated or reference text is included.

| Self-feeding rate | Source-copy weight | Language-balance weight | TIDE aux multiplier | Edge balance | Decoder | Seed | Bucket | Checker coverage | Action fidelity | Preservation | Context marker | Accepted references | CER | Unicode | EOS | Failure reason | Bucket gate |
|---:|---:|---:|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 17 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 160/160 | 136/160 | 160/160 | 136/160 | 0.8% | 160/160 | 160/160 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 17 | en/single/POLARITY:NEGATIVE | 320/320 | 317/320 | 236/320 | 320/320 | 236/320 | 1.9% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 17 | en/single/POLARITY:POSITIVE | 320/320 | 316/320 | 238/320 | 320/320 | 237/320 | 2.0% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 17 | en/single/TIME:NOW | 320/320 | 319/320 | 255/320 | 319/320 | 254/320 | 1.5% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 17 | en/single/TIME:PAST | 320/320 | 311/320 | 245/320 | 320/320 | 242/320 | 2.1% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 17 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 160/160 | 154/160 | 160/160 | 154/160 | 0.3% | 160/160 | 160/160 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 17 | vi/single/POLARITY:NEGATIVE | 320/320 | 318/320 | 314/320 | 320/320 | 311/320 | 0.7% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 17 | vi/single/POLARITY:POSITIVE | 320/320 | 319/320 | 304/320 | 320/320 | 304/320 | 0.4% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 17 | vi/single/TIME:NOW | 320/320 | 312/320 | 312/320 | 320/320 | 306/320 | 0.9% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 17 | vi/single/TIME:PAST | 320/320 | 320/320 | 308/320 | 320/320 | 308/320 | 0.3% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 23 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 160/160 | 128/160 | 160/160 | 128/160 | 1.1% | 160/160 | 160/160 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 23 | en/single/POLARITY:NEGATIVE | 320/320 | 317/320 | 245/320 | 320/320 | 242/320 | 1.7% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 23 | en/single/POLARITY:POSITIVE | 320/320 | 317/320 | 230/320 | 320/320 | 223/320 | 2.2% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 23 | en/single/TIME:NOW | 320/320 | 318/320 | 249/320 | 319/320 | 246/320 | 1.9% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 23 | en/single/TIME:PAST | 320/320 | 304/320 | 239/320 | 320/320 | 237/320 | 2.4% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 23 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 160/160 | 156/160 | 160/160 | 156/160 | 0.2% | 160/160 | 160/160 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 23 | vi/single/POLARITY:NEGATIVE | 320/320 | 316/320 | 309/320 | 320/320 | 306/320 | 0.4% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 23 | vi/single/POLARITY:POSITIVE | 320/320 | 292/320 | 279/320 | 319/320 | 277/320 | 1.8% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 23 | vi/single/TIME:NOW | 320/320 | 305/320 | 289/320 | 320/320 | 289/320 | 1.0% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 23 | vi/single/TIME:PAST | 320/320 | 277/320 | 252/320 | 315/320 | 251/320 | 2.4% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 41 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 156/160 | 114/160 | 160/160 | 113/160 | 1.9% | 160/160 | 160/160 | preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 41 | en/single/POLARITY:NEGATIVE | 320/320 | 289/320 | 179/320 | 319/320 | 176/320 | 3.8% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 41 | en/single/POLARITY:POSITIVE | 320/320 | 318/320 | 194/320 | 316/320 | 194/320 | 3.9% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 41 | en/single/TIME:NOW | 320/320 | 295/320 | 175/320 | 318/320 | 170/320 | 4.2% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 41 | en/single/TIME:PAST | 320/320 | 292/320 | 199/320 | 320/320 | 198/320 | 3.9% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 41 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 160/160 | 131/160 | 160/160 | 131/160 | 2.6% | 160/160 | 160/160 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 41 | vi/single/POLARITY:NEGATIVE | 320/320 | 310/320 | 275/320 | 320/320 | 262/320 | 4.3% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 41 | vi/single/POLARITY:POSITIVE | 320/320 | 314/320 | 269/320 | 318/320 | 252/320 | 3.1% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 41 | vi/single/TIME:NOW | 320/320 | 313/320 | 290/320 | 319/320 | 268/320 | 2.8% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 41 | vi/single/TIME:PAST | 320/320 | 319/320 | 248/320 | 320/320 | 240/320 | 3.8% | 320/320 | 320/320 | preservation_pass | fail |

## Limits and interpretation

Valid Unicode and EOS termination do not establish semantic correctness. The deterministic checker covers only the declared synthetic tense/polarity grammar and named roles. This benchmark tests recombination of familiar lexical factors; it does not establish naturalness, natural-corpus efficacy, or scientific efficacy. Control results are diagnostic; no TIDE advantage is claimed.

All examples and generated outputs remain private under Git-ignored `data/` and `runs/`. This report contains aggregate metrics only. `human_validated` is false. PhoMT raw/derived data and Phan Rang Cham data were not used.

Private aggregate evidence: `vi-en-ai-v4.31/protocol.json`, validation generation metrics under `vi-en-ai-v4.31`, and associated ignored run artifacts. Protocol SHA-256: `a34113c4f74b804d50120c7472a9dbf1f10c5329542293c5f43eb6b14f1215e5`.
