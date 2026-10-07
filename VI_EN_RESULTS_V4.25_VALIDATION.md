# vi-en-ai-v4.25 Vi–En validation results

AI-authored and independently AI-reviewed preliminary synthetic pilot. **Not human/native-speaker validated.** PhoMT was not used. Phan Rang Cham remains excluded.

## Frozen protocol

The corpus has 15360 records and 192 event combinations. Split groups: 112/40/40; records: 8960/3200/3200 (train/validation/release holdout). Data split policy: 112/40/40 event combinations from three fresh agents × eight verbs × eight patients; pairwise-covered held-out combinations, fixed deterministic split seed, English progressive NOW aligned with Vietnamese đang (including đang không for negative NOW), shared four-form realization grammar and action order; fresh synthetic corpus and release holdout to test one-pass 0.2 self-feeding against teacher forcing at fixed 64-width/two-layer TIDE capacity; the extra proposal forward costs more compute, so no matched-compute claim; this is a preliminary exposure-mismatch hypothesis test, not a causal diagnosis or generalization benchmark. Frozen release-holdout scope: The release holdout uses the same ordered action paths as train and validation; it probes fresh held-out factor combinations only and does not add an action-order shift. Transition weighting: There are 3072 duplicated path-step rows across the full split: 1792 in training, 640 in validation, and 640 in the sealed release holdout. Each logical path-step transition has one standalone single-edge record and one path-linked record. In training this adds 1792 record exposures, so those path-selected transitions contribute twice the row-wise token/edge exposure. Validation and holdout duplicates are evaluation records, not training exposure. The representation is fixed identically across conditions; results describe a path-enriched training distribution, not uniform weighting over unique transitions.

Objective conditions: tide with one-pass self-feeding rate 0 and source-copy weight 0 and TIDE latent-objective multiplier 1; transition balance `row_uniform`; decoder `vocabulary`; tide with one-pass self-feeding rate 0.2 and source-copy weight 0 and TIDE latent-objective multiplier 1; transition balance `row_uniform`; decoder `vocabulary`. Seeds 17, 23, 41; 29 epochs and 3248 updates/config; width 64, 4 heads, 2 layers. The preregistered final epoch was evaluated (`fixed_final_epoch`); validation loss did not select the checkpoint. Decoder: greedy byte-level UTF-8 constrained decoding; EOS only at complete codepoint boundaries.

The registered primary objective is `tide`. Frozen thresholds: valid Unicode 100%; checker coverage 100%; single-action fidelity ≥90% and preservation ≥90%; path fidelity ≥80% and preservation ≥80%. Every configured primary condition, seed, and language/action bucket must meet all applicable thresholds.

## Validation result: **FAIL**

Semantic checker coverage is complete across all primary buckets.

The release holdout was not evaluated and remains sealed.

| Mode | Self-feeding rate | Source-copy weight | TIDE aux multiplier | Edge balance | Decoder | Seed | Train token CE | Val token CE | Val path token CE | Updates | Training wall seconds | Mean examples/sec | Gate |
|---|---:|---:|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| tide | 0 | 0 | 1 | row_uniform | vocabulary | 17 | 0.0013 | 0.0022 | 0.0005 | 3248 | 1076.3 | 241.8 | pass |
| tide | 0.2 | 0 | 1 | row_uniform | vocabulary | 17 | 0.0404 | 0.0148 | 0.0059 | 3248 | 1334.1 | 194.8 | fail |
| tide | 0 | 0 | 1 | row_uniform | vocabulary | 23 | 0.0034 | 0.0032 | 0.0017 | 3248 | 1065.9 | 243.8 | pass |
| tide | 0.2 | 0 | 1 | row_uniform | vocabulary | 23 | 0.0060 | 0.0035 | 0.0010 | 3248 | 1315.5 | 197.6 | pass |
| tide | 0 | 0 | 1 | row_uniform | vocabulary | 41 | 0.0034 | 0.0116 | 0.0081 | 3248 | 1057.4 | 245.8 | fail |
| tide | 0.2 | 0 | 1 | row_uniform | vocabulary | 41 | 0.0117 | 0.0109 | 0.0089 | 3248 | 1316.1 | 197.5 | fail |

## Validation generation by condition and bucket

Action fidelity and preservation are pooled across seeds within each condition and bucket; thresholds are still checked for every primary condition/seed/bucket. Exact-reference match and CER are synthetic-reference metrics, not human naturalness.

| Mode | Self-feeding rate | Source-copy weight | TIDE aux multiplier | Edge balance | Decoder | Bucket | Checker coverage | Action fidelity | Preservation | Accepted references | CER | Nonempty | Unicode | EOS |
|---|---:|---:|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| tide | 0 | 0 | 1 | row_uniform | vocabulary | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 480/480 | 480/480 | 448/480 | 448/480 | 0.2% | 480/480 | 480/480 | 480/480 |
| tide | 0 | 0 | 1 | row_uniform | vocabulary | en/single/POLARITY:NEGATIVE | 960/960 | 959/960 | 872/960 | 872/960 | 0.5% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 1 | row_uniform | vocabulary | en/single/POLARITY:POSITIVE | 960/960 | 955/960 | 834/960 | 833/960 | 0.9% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 1 | row_uniform | vocabulary | en/single/TIME:NOW | 960/960 | 953/960 | 847/960 | 846/960 | 0.8% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 1 | row_uniform | vocabulary | en/single/TIME:PAST | 960/960 | 960/960 | 879/960 | 879/960 | 0.3% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 1 | row_uniform | vocabulary | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 480/480 | 480/480 | 472/480 | 468/480 | 0.1% | 480/480 | 480/480 | 480/480 |
| tide | 0 | 0 | 1 | row_uniform | vocabulary | vi/single/POLARITY:NEGATIVE | 960/960 | 953/960 | 936/960 | 926/960 | 0.4% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 1 | row_uniform | vocabulary | vi/single/POLARITY:POSITIVE | 960/960 | 956/960 | 926/960 | 921/960 | 0.5% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 1 | row_uniform | vocabulary | vi/single/TIME:NOW | 960/960 | 950/960 | 933/960 | 928/960 | 0.3% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 1 | row_uniform | vocabulary | vi/single/TIME:PAST | 960/960 | 958/960 | 928/960 | 922/960 | 0.3% | 960/960 | 960/960 | 960/960 |
| tide | 0.2 | 0 | 1 | row_uniform | vocabulary | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 480/480 | 480/480 | 440/480 | 440/480 | 0.2% | 480/480 | 480/480 | 480/480 |
| tide | 0.2 | 0 | 1 | row_uniform | vocabulary | en/single/POLARITY:NEGATIVE | 960/960 | 952/960 | 835/960 | 830/960 | 0.5% | 960/960 | 960/960 | 960/960 |
| tide | 0.2 | 0 | 1 | row_uniform | vocabulary | en/single/POLARITY:POSITIVE | 960/960 | 952/960 | 789/960 | 786/960 | 1.0% | 960/960 | 960/960 | 960/960 |
| tide | 0.2 | 0 | 1 | row_uniform | vocabulary | en/single/TIME:NOW | 960/960 | 942/960 | 805/960 | 801/960 | 0.9% | 960/960 | 960/960 | 960/960 |
| tide | 0.2 | 0 | 1 | row_uniform | vocabulary | en/single/TIME:PAST | 960/960 | 945/960 | 820/960 | 817/960 | 0.9% | 960/960 | 960/960 | 960/960 |
| tide | 0.2 | 0 | 1 | row_uniform | vocabulary | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 480/480 | 472/480 | 459/480 | 455/480 | 0.6% | 480/480 | 480/480 | 480/480 |
| tide | 0.2 | 0 | 1 | row_uniform | vocabulary | vi/single/POLARITY:NEGATIVE | 960/960 | 942/960 | 897/960 | 885/960 | 0.7% | 960/960 | 960/960 | 960/960 |
| tide | 0.2 | 0 | 1 | row_uniform | vocabulary | vi/single/POLARITY:POSITIVE | 960/960 | 950/960 | 860/960 | 852/960 | 1.3% | 960/960 | 960/960 | 960/960 |
| tide | 0.2 | 0 | 1 | row_uniform | vocabulary | vi/single/TIME:NOW | 960/960 | 935/960 | 878/960 | 873/960 | 1.1% | 960/960 | 960/960 | 960/960 |
| tide | 0.2 | 0 | 1 | row_uniform | vocabulary | vi/single/TIME:PAST | 960/960 | 917/960 | 859/960 | 851/960 | 1.2% | 960/960 | 960/960 | 960/960 |

## Primary-mode validation diagnostics by seed

Counts below preserve the frozen seed-by-seed gate denominator. No generated or reference text is included.

| Self-feeding rate | Source-copy weight | TIDE aux multiplier | Edge balance | Decoder | Seed | Bucket | Checker coverage | Action fidelity | Preservation | Accepted references | CER | Unicode | EOS | Failure reason | Bucket gate |
|---:|---:|---:|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| 0 | 0 | 1 | row_uniform | vocabulary | 17 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 160/160 | 160/160 | 160/160 | 0.0% | 160/160 | 160/160 | — | pass |
| 0 | 0 | 1 | row_uniform | vocabulary | 17 | en/single/POLARITY:NEGATIVE | 320/320 | 320/320 | 318/320 | 318/320 | 0.0% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 1 | row_uniform | vocabulary | 17 | en/single/POLARITY:POSITIVE | 320/320 | 319/320 | 307/320 | 307/320 | 0.3% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 1 | row_uniform | vocabulary | 17 | en/single/TIME:NOW | 320/320 | 320/320 | 317/320 | 317/320 | 0.1% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 1 | row_uniform | vocabulary | 17 | en/single/TIME:PAST | 320/320 | 320/320 | 318/320 | 318/320 | 0.0% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 1 | row_uniform | vocabulary | 17 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 160/160 | 159/160 | 159/160 | 0.1% | 160/160 | 160/160 | — | pass |
| 0 | 0 | 1 | row_uniform | vocabulary | 17 | vi/single/POLARITY:NEGATIVE | 320/320 | 318/320 | 316/320 | 314/320 | 0.4% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 1 | row_uniform | vocabulary | 17 | vi/single/POLARITY:POSITIVE | 320/320 | 318/320 | 316/320 | 314/320 | 0.2% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 1 | row_uniform | vocabulary | 17 | vi/single/TIME:NOW | 320/320 | 320/320 | 316/320 | 316/320 | 0.1% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 1 | row_uniform | vocabulary | 17 | vi/single/TIME:PAST | 320/320 | 319/320 | 318/320 | 316/320 | 0.1% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 1 | row_uniform | vocabulary | 23 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 160/160 | 157/160 | 157/160 | 0.1% | 160/160 | 160/160 | — | pass |
| 0 | 0 | 1 | row_uniform | vocabulary | 23 | en/single/POLARITY:NEGATIVE | 320/320 | 320/320 | 309/320 | 309/320 | 0.2% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 1 | row_uniform | vocabulary | 23 | en/single/POLARITY:POSITIVE | 320/320 | 318/320 | 304/320 | 303/320 | 0.5% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 1 | row_uniform | vocabulary | 23 | en/single/TIME:NOW | 320/320 | 319/320 | 311/320 | 311/320 | 0.2% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 1 | row_uniform | vocabulary | 23 | en/single/TIME:PAST | 320/320 | 320/320 | 311/320 | 311/320 | 0.2% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 1 | row_uniform | vocabulary | 23 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 160/160 | 155/160 | 153/160 | 0.2% | 160/160 | 160/160 | — | pass |
| 0 | 0 | 1 | row_uniform | vocabulary | 23 | vi/single/POLARITY:NEGATIVE | 320/320 | 319/320 | 309/320 | 303/320 | 0.3% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 1 | row_uniform | vocabulary | 23 | vi/single/POLARITY:POSITIVE | 320/320 | 320/320 | 309/320 | 309/320 | 0.4% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 1 | row_uniform | vocabulary | 23 | vi/single/TIME:NOW | 320/320 | 320/320 | 318/320 | 318/320 | 0.0% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 1 | row_uniform | vocabulary | 23 | vi/single/TIME:PAST | 320/320 | 319/320 | 300/320 | 298/320 | 0.6% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 1 | row_uniform | vocabulary | 41 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 160/160 | 131/160 | 131/160 | 0.5% | 160/160 | 160/160 | — | pass |
| 0 | 0 | 1 | row_uniform | vocabulary | 41 | en/single/POLARITY:NEGATIVE | 320/320 | 319/320 | 245/320 | 245/320 | 1.1% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 1 | row_uniform | vocabulary | 41 | en/single/POLARITY:POSITIVE | 320/320 | 318/320 | 223/320 | 223/320 | 1.8% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 1 | row_uniform | vocabulary | 41 | en/single/TIME:NOW | 320/320 | 314/320 | 219/320 | 218/320 | 2.0% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 1 | row_uniform | vocabulary | 41 | en/single/TIME:PAST | 320/320 | 320/320 | 250/320 | 250/320 | 0.8% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 1 | row_uniform | vocabulary | 41 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 160/160 | 158/160 | 156/160 | 0.2% | 160/160 | 160/160 | — | pass |
| 0 | 0 | 1 | row_uniform | vocabulary | 41 | vi/single/POLARITY:NEGATIVE | 320/320 | 316/320 | 311/320 | 309/320 | 0.6% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 1 | row_uniform | vocabulary | 41 | vi/single/POLARITY:POSITIVE | 320/320 | 318/320 | 301/320 | 298/320 | 0.8% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 1 | row_uniform | vocabulary | 41 | vi/single/TIME:NOW | 320/320 | 310/320 | 299/320 | 294/320 | 0.8% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 1 | row_uniform | vocabulary | 41 | vi/single/TIME:PAST | 320/320 | 320/320 | 310/320 | 308/320 | 0.3% | 320/320 | 320/320 | — | pass |
| 0.2 | 0 | 1 | row_uniform | vocabulary | 17 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 160/160 | 143/160 | 143/160 | 0.2% | 160/160 | 160/160 | — | pass |
| 0.2 | 0 | 1 | row_uniform | vocabulary | 17 | en/single/POLARITY:NEGATIVE | 320/320 | 314/320 | 256/320 | 252/320 | 1.0% | 320/320 | 320/320 | preservation_pass | fail |
| 0.2 | 0 | 1 | row_uniform | vocabulary | 17 | en/single/POLARITY:POSITIVE | 320/320 | 315/320 | 214/320 | 214/320 | 2.0% | 320/320 | 320/320 | preservation_pass | fail |
| 0.2 | 0 | 1 | row_uniform | vocabulary | 17 | en/single/TIME:NOW | 320/320 | 313/320 | 227/320 | 225/320 | 1.8% | 320/320 | 320/320 | preservation_pass | fail |
| 0.2 | 0 | 1 | row_uniform | vocabulary | 17 | en/single/TIME:PAST | 320/320 | 317/320 | 248/320 | 247/320 | 1.1% | 320/320 | 320/320 | preservation_pass | fail |
| 0.2 | 0 | 1 | row_uniform | vocabulary | 17 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 153/160 | 140/160 | 139/160 | 1.5% | 160/160 | 160/160 | — | pass |
| 0.2 | 0 | 1 | row_uniform | vocabulary | 17 | vi/single/POLARITY:NEGATIVE | 320/320 | 305/320 | 271/320 | 265/320 | 1.7% | 320/320 | 320/320 | preservation_pass | fail |
| 0.2 | 0 | 1 | row_uniform | vocabulary | 17 | vi/single/POLARITY:POSITIVE | 320/320 | 310/320 | 245/320 | 243/320 | 2.8% | 320/320 | 320/320 | preservation_pass | fail |
| 0.2 | 0 | 1 | row_uniform | vocabulary | 17 | vi/single/TIME:NOW | 320/320 | 296/320 | 255/320 | 252/320 | 2.7% | 320/320 | 320/320 | preservation_pass | fail |
| 0.2 | 0 | 1 | row_uniform | vocabulary | 17 | vi/single/TIME:PAST | 320/320 | 285/320 | 243/320 | 241/320 | 2.7% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0.2 | 0 | 1 | row_uniform | vocabulary | 23 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 160/160 | 157/160 | 157/160 | 0.1% | 160/160 | 160/160 | — | pass |
| 0.2 | 0 | 1 | row_uniform | vocabulary | 23 | en/single/POLARITY:NEGATIVE | 320/320 | 320/320 | 308/320 | 308/320 | 0.2% | 320/320 | 320/320 | — | pass |
| 0.2 | 0 | 1 | row_uniform | vocabulary | 23 | en/single/POLARITY:POSITIVE | 320/320 | 319/320 | 302/320 | 302/320 | 0.4% | 320/320 | 320/320 | — | pass |
| 0.2 | 0 | 1 | row_uniform | vocabulary | 23 | en/single/TIME:NOW | 320/320 | 319/320 | 306/320 | 305/320 | 0.3% | 320/320 | 320/320 | — | pass |
| 0.2 | 0 | 1 | row_uniform | vocabulary | 23 | en/single/TIME:PAST | 320/320 | 308/320 | 297/320 | 297/320 | 1.0% | 320/320 | 320/320 | — | pass |
| 0.2 | 0 | 1 | row_uniform | vocabulary | 23 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 159/160 | 160/160 | 159/160 | 0.0% | 160/160 | 160/160 | — | pass |
| 0.2 | 0 | 1 | row_uniform | vocabulary | 23 | vi/single/POLARITY:NEGATIVE | 320/320 | 319/320 | 315/320 | 314/320 | 0.1% | 320/320 | 320/320 | — | pass |
| 0.2 | 0 | 1 | row_uniform | vocabulary | 23 | vi/single/POLARITY:POSITIVE | 320/320 | 320/320 | 309/320 | 309/320 | 0.4% | 320/320 | 320/320 | — | pass |
| 0.2 | 0 | 1 | row_uniform | vocabulary | 23 | vi/single/TIME:NOW | 320/320 | 319/320 | 314/320 | 313/320 | 0.2% | 320/320 | 320/320 | — | pass |
| 0.2 | 0 | 1 | row_uniform | vocabulary | 23 | vi/single/TIME:PAST | 320/320 | 315/320 | 306/320 | 305/320 | 0.5% | 320/320 | 320/320 | — | pass |
| 0.2 | 0 | 1 | row_uniform | vocabulary | 41 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 160/160 | 140/160 | 140/160 | 0.2% | 160/160 | 160/160 | — | pass |
| 0.2 | 0 | 1 | row_uniform | vocabulary | 41 | en/single/POLARITY:NEGATIVE | 320/320 | 318/320 | 271/320 | 270/320 | 0.5% | 320/320 | 320/320 | preservation_pass | fail |
| 0.2 | 0 | 1 | row_uniform | vocabulary | 41 | en/single/POLARITY:POSITIVE | 320/320 | 318/320 | 273/320 | 270/320 | 0.5% | 320/320 | 320/320 | preservation_pass | fail |
| 0.2 | 0 | 1 | row_uniform | vocabulary | 41 | en/single/TIME:NOW | 320/320 | 310/320 | 272/320 | 271/320 | 0.7% | 320/320 | 320/320 | preservation_pass | fail |
| 0.2 | 0 | 1 | row_uniform | vocabulary | 41 | en/single/TIME:PAST | 320/320 | 320/320 | 275/320 | 273/320 | 0.5% | 320/320 | 320/320 | preservation_pass | fail |
| 0.2 | 0 | 1 | row_uniform | vocabulary | 41 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 160/160 | 159/160 | 157/160 | 0.1% | 160/160 | 160/160 | — | pass |
| 0.2 | 0 | 1 | row_uniform | vocabulary | 41 | vi/single/POLARITY:NEGATIVE | 320/320 | 318/320 | 311/320 | 306/320 | 0.3% | 320/320 | 320/320 | — | pass |
| 0.2 | 0 | 1 | row_uniform | vocabulary | 41 | vi/single/POLARITY:POSITIVE | 320/320 | 320/320 | 306/320 | 300/320 | 0.6% | 320/320 | 320/320 | — | pass |
| 0.2 | 0 | 1 | row_uniform | vocabulary | 41 | vi/single/TIME:NOW | 320/320 | 320/320 | 309/320 | 308/320 | 0.3% | 320/320 | 320/320 | — | pass |
| 0.2 | 0 | 1 | row_uniform | vocabulary | 41 | vi/single/TIME:PAST | 320/320 | 317/320 | 310/320 | 305/320 | 0.4% | 320/320 | 320/320 | — | pass |

## Limits and interpretation

Valid Unicode and EOS termination do not establish semantic correctness. The deterministic checker covers only the declared synthetic tense/polarity grammar and named roles. This benchmark tests recombination of familiar lexical factors; it does not establish naturalness, natural-corpus efficacy, or scientific efficacy. Control results are diagnostic; no TIDE advantage is claimed.

All examples and generated outputs remain private under Git-ignored `data/` and `runs/`. This report contains aggregate metrics only. `human_validated` is false. PhoMT raw/derived data and Phan Rang Cham data were not used.

Private aggregate evidence: `vi-en-ai-v4.25/protocol.json`, validation generation metrics under `vi-en-ai-v4.25`, and associated ignored run artifacts. Protocol SHA-256: `6604805a86221a4958da9ea38ac0e845da99a3524f5cb802bfbb243e65c243b6`.
