# vi-en-ai-v4.26 Vi–En validation results

AI-authored and independently AI-reviewed preliminary synthetic pilot. **Not human/native-speaker validated.** PhoMT was not used. Phan Rang Cham remains excluded.

## Frozen protocol

The corpus has 15360 records and 192 event combinations. Split groups: 112/40/40; records: 8960/3200/3200 (train/validation/release holdout). Data split policy: 112/40/40 event combinations from three fresh agents × eight verbs × eight patients; pairwise-covered held-out combinations, fixed deterministic split seed; shared four-form realization grammar and action order; fresh synthetic corpus and sealed release holdout for a low-dose source-copy supervision (0/0.25) study informed by v4.25's free-generation preservation diagnosis; fixed 64-width/two-layer TIDE and final-epoch evaluation. Frozen release-holdout scope: The release holdout uses the same ordered action paths as train and validation; it probes fresh held-out factor combinations only and does not add an action-order shift. Transition weighting: There are 3072 duplicated path-step rows across the full split: 1792 in training, 640 in validation, and 640 in the sealed release holdout. Each logical path-step transition has one standalone single-edge record and one path-linked record. In training this adds 1792 record exposures, so those path-selected transitions contribute twice the row-wise token/edge exposure. Validation and holdout duplicates are evaluation records, not training exposure. The representation is fixed identically across conditions; results describe a path-enriched training distribution, not uniform weighting over unique transitions.

Objective conditions: tide with one-pass self-feeding rate 0 and source-copy weight 0 and TIDE latent-objective multiplier 1; transition balance `row_uniform`; decoder `vocabulary`; tide with one-pass self-feeding rate 0 and source-copy weight 0.25 and TIDE latent-objective multiplier 1; transition balance `row_uniform`; decoder `vocabulary`. Seeds 17, 23, 41; 29 epochs and 3248 updates/config; width 64, 4 heads, 2 layers. The preregistered final epoch was evaluated (`fixed_final_epoch`); validation loss did not select the checkpoint. Decoder: greedy byte-level UTF-8 constrained decoding; EOS only at complete codepoint boundaries.

The registered primary objective is `tide`. Frozen thresholds: valid Unicode 100%; checker coverage 100%; single-action fidelity ≥90% and preservation ≥90%; path fidelity ≥80% and preservation ≥80%. Every configured primary condition, seed, and language/action bucket must meet all applicable thresholds.

## Validation result: **FAIL**

Semantic checker coverage is complete across all primary buckets.

The release holdout was not evaluated and remains sealed.

| Mode | Self-feeding rate | Source-copy weight | TIDE aux multiplier | Edge balance | Decoder | Seed | Train token CE | Val token CE | Val path token CE | Updates | Training wall seconds | Mean examples/sec | Gate |
|---|---:|---:|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| tide | 0 | 0 | 1 | row_uniform | vocabulary | 17 | 0.0112 | 0.0183 | 0.0142 | 3248 | 2690.2 | 96.6 | fail |
| tide | 0 | 0.25 | 1 | row_uniform | vocabulary | 17 | 0.0148 | 0.0201 | 0.0128 | 3248 | 2747.0 | 94.6 | fail |
| tide | 0 | 0 | 1 | row_uniform | vocabulary | 23 | 0.0034 | 0.0040 | 0.0015 | 3248 | 2715.7 | 95.8 | pass |
| tide | 0 | 0.25 | 1 | row_uniform | vocabulary | 23 | 0.0087 | 0.0097 | 0.0040 | 3248 | 2731.7 | 95.2 | fail |
| tide | 0 | 0 | 1 | row_uniform | vocabulary | 41 | 0.0304 | 0.0175 | 0.0095 | 3248 | 2055.3 | 126.4 | fail |
| tide | 0 | 0.25 | 1 | row_uniform | vocabulary | 41 | 0.0083 | 0.0096 | 0.0053 | 3248 | 2049.8 | 126.8 | fail |

## Validation generation by condition and bucket

Action fidelity and preservation are pooled across seeds within each condition and bucket; thresholds are still checked for every primary condition/seed/bucket. Exact-reference match and CER are synthetic-reference metrics, not human naturalness.

| Mode | Self-feeding rate | Source-copy weight | TIDE aux multiplier | Edge balance | Decoder | Bucket | Checker coverage | Action fidelity | Preservation | Accepted references | CER | Nonempty | Unicode | EOS |
|---|---:|---:|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| tide | 0 | 0 | 1 | row_uniform | vocabulary | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 480/480 | 468/480 | 421/480 | 420/480 | 0.8% | 480/480 | 480/480 | 480/480 |
| tide | 0 | 0 | 1 | row_uniform | vocabulary | en/single/POLARITY:NEGATIVE | 960/960 | 947/960 | 794/960 | 790/960 | 1.2% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 1 | row_uniform | vocabulary | en/single/POLARITY:POSITIVE | 960/960 | 939/960 | 747/960 | 736/960 | 2.2% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 1 | row_uniform | vocabulary | en/single/TIME:NOW | 960/960 | 944/960 | 753/960 | 746/960 | 1.6% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 1 | row_uniform | vocabulary | en/single/TIME:PAST | 960/960 | 919/960 | 759/960 | 755/960 | 2.2% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 1 | row_uniform | vocabulary | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 480/480 | 472/480 | 459/480 | 451/480 | 0.9% | 480/480 | 480/480 | 480/480 |
| tide | 0 | 0 | 1 | row_uniform | vocabulary | vi/single/POLARITY:NEGATIVE | 960/960 | 922/960 | 865/960 | 826/960 | 2.1% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 1 | row_uniform | vocabulary | vi/single/POLARITY:POSITIVE | 960/960 | 911/960 | 841/960 | 818/960 | 2.1% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 1 | row_uniform | vocabulary | vi/single/TIME:NOW | 960/960 | 924/960 | 853/960 | 834/960 | 1.9% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 1 | row_uniform | vocabulary | vi/single/TIME:PAST | 960/960 | 940/960 | 869/960 | 857/960 | 1.3% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0.25 | 1 | row_uniform | vocabulary | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 480/480 | 476/480 | 400/480 | 397/480 | 1.1% | 480/480 | 480/480 | 480/480 |
| tide | 0 | 0.25 | 1 | row_uniform | vocabulary | en/single/POLARITY:NEGATIVE | 960/960 | 944/960 | 705/960 | 699/960 | 2.6% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0.25 | 1 | row_uniform | vocabulary | en/single/POLARITY:POSITIVE | 960/960 | 925/960 | 641/960 | 619/960 | 3.5% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0.25 | 1 | row_uniform | vocabulary | en/single/TIME:NOW | 960/960 | 934/960 | 647/960 | 636/960 | 2.7% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0.25 | 1 | row_uniform | vocabulary | en/single/TIME:PAST | 960/960 | 885/960 | 648/960 | 626/960 | 3.9% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0.25 | 1 | row_uniform | vocabulary | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 480/480 | 480/480 | 464/480 | 463/480 | 0.5% | 480/480 | 480/480 | 480/480 |
| tide | 0 | 0.25 | 1 | row_uniform | vocabulary | vi/single/POLARITY:NEGATIVE | 960/960 | 944/960 | 922/960 | 903/960 | 1.6% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0.25 | 1 | row_uniform | vocabulary | vi/single/POLARITY:POSITIVE | 960/960 | 956/960 | 910/960 | 898/960 | 0.7% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0.25 | 1 | row_uniform | vocabulary | vi/single/TIME:NOW | 960/960 | 908/960 | 882/960 | 866/960 | 1.4% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0.25 | 1 | row_uniform | vocabulary | vi/single/TIME:PAST | 960/960 | 933/960 | 885/960 | 882/960 | 0.9% | 960/960 | 960/960 | 960/960 |

## Primary-mode validation diagnostics by seed

Counts below preserve the frozen seed-by-seed gate denominator. No generated or reference text is included.

| Self-feeding rate | Source-copy weight | TIDE aux multiplier | Edge balance | Decoder | Seed | Bucket | Checker coverage | Action fidelity | Preservation | Accepted references | CER | Unicode | EOS | Failure reason | Bucket gate |
|---:|---:|---:|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| 0 | 0 | 1 | row_uniform | vocabulary | 17 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 151/160 | 121/160 | 121/160 | 1.4% | 160/160 | 160/160 | preservation_pass | fail |
| 0 | 0 | 1 | row_uniform | vocabulary | 17 | en/single/POLARITY:NEGATIVE | 320/320 | 313/320 | 224/320 | 223/320 | 1.8% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 1 | row_uniform | vocabulary | 17 | en/single/POLARITY:POSITIVE | 320/320 | 307/320 | 205/320 | 197/320 | 3.6% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 1 | row_uniform | vocabulary | 17 | en/single/TIME:NOW | 320/320 | 315/320 | 217/320 | 214/320 | 2.2% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 1 | row_uniform | vocabulary | 17 | en/single/TIME:PAST | 320/320 | 305/320 | 222/320 | 220/320 | 2.7% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 1 | row_uniform | vocabulary | 17 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 160/160 | 158/160 | 157/160 | 0.2% | 160/160 | 160/160 | — | pass |
| 0 | 0 | 1 | row_uniform | vocabulary | 17 | vi/single/POLARITY:NEGATIVE | 320/320 | 317/320 | 310/320 | 307/320 | 1.0% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 1 | row_uniform | vocabulary | 17 | vi/single/POLARITY:POSITIVE | 320/320 | 307/320 | 297/320 | 292/320 | 1.3% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 1 | row_uniform | vocabulary | 17 | vi/single/TIME:NOW | 320/320 | 313/320 | 302/320 | 298/320 | 0.9% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 1 | row_uniform | vocabulary | 17 | vi/single/TIME:PAST | 320/320 | 316/320 | 299/320 | 297/320 | 0.8% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 1 | row_uniform | vocabulary | 23 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 158/160 | 156/160 | 156/160 | 0.3% | 160/160 | 160/160 | — | pass |
| 0 | 0 | 1 | row_uniform | vocabulary | 23 | en/single/POLARITY:NEGATIVE | 320/320 | 319/320 | 301/320 | 301/320 | 0.5% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 1 | row_uniform | vocabulary | 23 | en/single/POLARITY:POSITIVE | 320/320 | 320/320 | 302/320 | 302/320 | 0.5% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 1 | row_uniform | vocabulary | 23 | en/single/TIME:NOW | 320/320 | 319/320 | 297/320 | 297/320 | 0.5% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 1 | row_uniform | vocabulary | 23 | en/single/TIME:PAST | 320/320 | 315/320 | 302/320 | 302/320 | 0.7% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 1 | row_uniform | vocabulary | 23 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 159/160 | 159/160 | 158/160 | 0.1% | 160/160 | 160/160 | — | pass |
| 0 | 0 | 1 | row_uniform | vocabulary | 23 | vi/single/POLARITY:NEGATIVE | 320/320 | 313/320 | 310/320 | 304/320 | 0.7% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 1 | row_uniform | vocabulary | 23 | vi/single/POLARITY:POSITIVE | 320/320 | 320/320 | 313/320 | 312/320 | 0.3% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 1 | row_uniform | vocabulary | 23 | vi/single/TIME:NOW | 320/320 | 316/320 | 312/320 | 310/320 | 0.5% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 1 | row_uniform | vocabulary | 23 | vi/single/TIME:PAST | 320/320 | 316/320 | 312/320 | 311/320 | 0.3% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 1 | row_uniform | vocabulary | 41 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 159/160 | 144/160 | 143/160 | 0.8% | 160/160 | 160/160 | — | pass |
| 0 | 0 | 1 | row_uniform | vocabulary | 41 | en/single/POLARITY:NEGATIVE | 320/320 | 315/320 | 269/320 | 266/320 | 1.2% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 1 | row_uniform | vocabulary | 41 | en/single/POLARITY:POSITIVE | 320/320 | 312/320 | 240/320 | 237/320 | 2.4% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 1 | row_uniform | vocabulary | 41 | en/single/TIME:NOW | 320/320 | 310/320 | 239/320 | 235/320 | 2.1% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 1 | row_uniform | vocabulary | 41 | en/single/TIME:PAST | 320/320 | 299/320 | 235/320 | 233/320 | 3.1% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 1 | row_uniform | vocabulary | 41 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 153/160 | 142/160 | 136/160 | 2.4% | 160/160 | 160/160 | — | pass |
| 0 | 0 | 1 | row_uniform | vocabulary | 41 | vi/single/POLARITY:NEGATIVE | 320/320 | 292/320 | 245/320 | 215/320 | 4.6% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 1 | row_uniform | vocabulary | 41 | vi/single/POLARITY:POSITIVE | 320/320 | 284/320 | 231/320 | 214/320 | 4.7% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | 1 | row_uniform | vocabulary | 41 | vi/single/TIME:NOW | 320/320 | 295/320 | 239/320 | 226/320 | 4.3% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 1 | row_uniform | vocabulary | 41 | vi/single/TIME:PAST | 320/320 | 308/320 | 258/320 | 249/320 | 2.7% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0.25 | 1 | row_uniform | vocabulary | 17 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 158/160 | 110/160 | 110/160 | 1.9% | 160/160 | 160/160 | preservation_pass | fail |
| 0 | 0.25 | 1 | row_uniform | vocabulary | 17 | en/single/POLARITY:NEGATIVE | 320/320 | 315/320 | 202/320 | 197/320 | 2.7% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0.25 | 1 | row_uniform | vocabulary | 17 | en/single/POLARITY:POSITIVE | 320/320 | 299/320 | 158/320 | 151/320 | 5.7% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0.25 | 1 | row_uniform | vocabulary | 17 | en/single/TIME:NOW | 320/320 | 299/320 | 165/320 | 160/320 | 4.5% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0.25 | 1 | row_uniform | vocabulary | 17 | en/single/TIME:PAST | 320/320 | 268/320 | 162/320 | 158/320 | 6.9% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0.25 | 1 | row_uniform | vocabulary | 17 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 160/160 | 151/160 | 151/160 | 0.4% | 160/160 | 160/160 | — | pass |
| 0 | 0.25 | 1 | row_uniform | vocabulary | 17 | vi/single/POLARITY:NEGATIVE | 320/320 | 315/320 | 301/320 | 296/320 | 1.7% | 320/320 | 320/320 | — | pass |
| 0 | 0.25 | 1 | row_uniform | vocabulary | 17 | vi/single/POLARITY:POSITIVE | 320/320 | 316/320 | 299/320 | 295/320 | 0.9% | 320/320 | 320/320 | — | pass |
| 0 | 0.25 | 1 | row_uniform | vocabulary | 17 | vi/single/TIME:NOW | 320/320 | 300/320 | 290/320 | 283/320 | 2.0% | 320/320 | 320/320 | — | pass |
| 0 | 0.25 | 1 | row_uniform | vocabulary | 17 | vi/single/TIME:PAST | 320/320 | 317/320 | 300/320 | 299/320 | 0.7% | 320/320 | 320/320 | — | pass |
| 0 | 0.25 | 1 | row_uniform | vocabulary | 23 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 158/160 | 150/160 | 147/160 | 0.6% | 160/160 | 160/160 | — | pass |
| 0 | 0.25 | 1 | row_uniform | vocabulary | 23 | en/single/POLARITY:NEGATIVE | 320/320 | 311/320 | 260/320 | 259/320 | 3.4% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0.25 | 1 | row_uniform | vocabulary | 23 | en/single/POLARITY:POSITIVE | 320/320 | 307/320 | 257/320 | 246/320 | 2.6% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0.25 | 1 | row_uniform | vocabulary | 23 | en/single/TIME:NOW | 320/320 | 316/320 | 245/320 | 240/320 | 1.8% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0.25 | 1 | row_uniform | vocabulary | 23 | en/single/TIME:PAST | 320/320 | 306/320 | 247/320 | 234/320 | 2.7% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0.25 | 1 | row_uniform | vocabulary | 23 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 160/160 | 156/160 | 155/160 | 0.9% | 160/160 | 160/160 | — | pass |
| 0 | 0.25 | 1 | row_uniform | vocabulary | 23 | vi/single/POLARITY:NEGATIVE | 320/320 | 315/320 | 314/320 | 309/320 | 1.0% | 320/320 | 320/320 | — | pass |
| 0 | 0.25 | 1 | row_uniform | vocabulary | 23 | vi/single/POLARITY:POSITIVE | 320/320 | 320/320 | 310/320 | 305/320 | 0.4% | 320/320 | 320/320 | — | pass |
| 0 | 0.25 | 1 | row_uniform | vocabulary | 23 | vi/single/TIME:NOW | 320/320 | 313/320 | 313/320 | 306/320 | 0.5% | 320/320 | 320/320 | — | pass |
| 0 | 0.25 | 1 | row_uniform | vocabulary | 23 | vi/single/TIME:PAST | 320/320 | 296/320 | 281/320 | 279/320 | 1.2% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0.25 | 1 | row_uniform | vocabulary | 41 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 160/160 | 140/160 | 140/160 | 0.9% | 160/160 | 160/160 | — | pass |
| 0 | 0.25 | 1 | row_uniform | vocabulary | 41 | en/single/POLARITY:NEGATIVE | 320/320 | 318/320 | 243/320 | 243/320 | 1.8% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0.25 | 1 | row_uniform | vocabulary | 41 | en/single/POLARITY:POSITIVE | 320/320 | 319/320 | 226/320 | 222/320 | 2.3% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0.25 | 1 | row_uniform | vocabulary | 41 | en/single/TIME:NOW | 320/320 | 319/320 | 237/320 | 236/320 | 1.9% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0.25 | 1 | row_uniform | vocabulary | 41 | en/single/TIME:PAST | 320/320 | 311/320 | 239/320 | 234/320 | 2.1% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0.25 | 1 | row_uniform | vocabulary | 41 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 160/160 | 157/160 | 157/160 | 0.2% | 160/160 | 160/160 | — | pass |
| 0 | 0.25 | 1 | row_uniform | vocabulary | 41 | vi/single/POLARITY:NEGATIVE | 320/320 | 314/320 | 307/320 | 298/320 | 2.0% | 320/320 | 320/320 | — | pass |
| 0 | 0.25 | 1 | row_uniform | vocabulary | 41 | vi/single/POLARITY:POSITIVE | 320/320 | 320/320 | 301/320 | 298/320 | 0.6% | 320/320 | 320/320 | — | pass |
| 0 | 0.25 | 1 | row_uniform | vocabulary | 41 | vi/single/TIME:NOW | 320/320 | 295/320 | 279/320 | 277/320 | 1.8% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0.25 | 1 | row_uniform | vocabulary | 41 | vi/single/TIME:PAST | 320/320 | 320/320 | 304/320 | 304/320 | 0.6% | 320/320 | 320/320 | — | pass |

## Limits and interpretation

Valid Unicode and EOS termination do not establish semantic correctness. The deterministic checker covers only the declared synthetic tense/polarity grammar and named roles. This benchmark tests recombination of familiar lexical factors; it does not establish naturalness, natural-corpus efficacy, or scientific efficacy. Control results are diagnostic; no TIDE advantage is claimed.

All examples and generated outputs remain private under Git-ignored `data/` and `runs/`. This report contains aggregate metrics only. `human_validated` is false. PhoMT raw/derived data and Phan Rang Cham data were not used.

Private aggregate evidence: `vi-en-ai-v4.26/protocol.json`, validation generation metrics under `vi-en-ai-v4.26`, and associated ignored run artifacts. Protocol SHA-256: `b8d2c78cc0de9f833d05eb2ea200f82b0b614839390695ad3fe281d6a7105dd2`.
