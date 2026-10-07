# vi-en-ai-v4.29 Vi–En validation results

AI-authored and independently AI-reviewed preliminary synthetic pilot. **Not human/native-speaker validated.** PhoMT was not used. Phan Rang Cham remains excluded.

## Frozen protocol

The corpus has 15360 records and 192 event combinations. Split groups: 112/40/40; records: 8960/3200/3200 (train/validation/release holdout). Data split policy: 112/40/40 event combinations from a fresh three-agent factor block with a new deterministic split seed; the release holdout is separate from v4.28 and only train/validation records, frames, groups, and alignments enter the reviewer bundle; the shared workshop context is checked through the declared place marker. Frozen release-holdout scope: The release holdout uses the same ordered action paths as train and validation; it probes fresh held-out factor combinations only and does not add an action-order shift. Transition weighting: There are 3072 duplicated path-step rows across the full split: 1792 in training, 640 in validation, and 640 in the sealed release holdout. Each logical path-step transition has one standalone single-edge record and one path-linked record. In training this adds 1792 record exposures, so those path-selected transitions contribute twice the row-wise token/edge exposure. Validation and holdout duplicates are evaluation records, not training exposure. The representation is fixed identically across conditions; results describe a path-enriched training distribution, not uniform weighting over unique transitions. Language-balance intervention scope: Base per-edge token CE only: per-example token-normalized CE is edge-weight averaged within each language and then equally averaged across present languages. Composed path-token CE and auxiliary terms are unchanged across conditions.

Objective conditions: tide with one-pass self-feeding rate 0 and source-copy weight 0 and TIDE latent-objective multiplier 1; language-balance weight 0; transition balance `row_uniform`; decoder `vocabulary`; tide with one-pass self-feeding rate 0 and source-copy weight 0 and TIDE latent-objective multiplier 1; language-balance weight 1; transition balance `row_uniform`; decoder `vocabulary`. Seeds 17, 23, 41; 29 epochs and 3248 updates/config; width 64, 4 heads, 2 layers. The preregistered final epoch was evaluated (`fixed_final_epoch`); validation loss did not select the checkpoint. Decoder: greedy byte-level UTF-8 constrained decoding; EOS only at complete codepoint boundaries.

The registered primary objective is `tide`. Frozen thresholds: valid Unicode 100%; checker coverage 100%; single-action fidelity ≥90% and preservation ≥90%; path fidelity ≥80% and preservation ≥80%. Every configured primary condition, seed, and language/action bucket must meet all applicable thresholds.

## Validation result: **FAIL**

Semantic checker coverage is complete across all primary buckets.

The release holdout was not evaluated and remains sealed.

| Mode | Self-feeding rate | Source-copy weight | Language-balance weight | TIDE aux multiplier | Edge balance | Decoder | Seed | Train token CE | Val token CE | Train balanced CE | Val balanced CE | Val path token CE | Updates | Training wall seconds | Mean examples/sec | Gate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tide | 0 | 0 | 0 | 1 | row_uniform | vocabulary | 17 | 0.0017 | 0.0023 | 0.0018 | 0.0025 | 0.0006 | 3248 | 2103.6 | 123.5 | pass |
| tide | 0 | 0 | 1 | 1 | row_uniform | vocabulary | 17 | 0.0059 | 0.0090 | 0.0064 | 0.0101 | 0.0023 | 3248 | 2103.6 | 123.5 | fail |
| tide | 0 | 0 | 0 | 1 | row_uniform | vocabulary | 23 | 0.0046 | 0.0071 | 0.0046 | 0.0080 | 0.0013 | 3248 | 2107.1 | 123.3 | fail |
| tide | 0 | 0 | 1 | 1 | row_uniform | vocabulary | 23 | 0.0032 | 0.0058 | 0.0033 | 0.0064 | 0.0018 | 3248 | 2107.2 | 123.3 | fail |
| tide | 0 | 0 | 0 | 1 | row_uniform | vocabulary | 41 | 0.0074 | 0.0065 | 0.0082 | 0.0072 | 0.0032 | 3248 | 2100.7 | 123.7 | fail |
| tide | 0 | 0 | 1 | 1 | row_uniform | vocabulary | 41 | 0.0254 | 0.0223 | 0.0243 | 0.0217 | 0.0120 | 3248 | 2102.6 | 123.6 | fail |

## Validation generation by condition and bucket

Action fidelity, preservation, and context-marker counts are pooled across seeds within each condition and bucket; thresholds are still checked for every primary condition/seed/bucket. Exact-reference match and CER are synthetic-reference metrics, not human naturalness.

| Mode | Self-feeding rate | Source-copy weight | Language-balance weight | TIDE aux multiplier | Edge balance | Decoder | Bucket | Checker coverage | Action fidelity | Preservation | Context marker | Accepted references | CER | Nonempty | Unicode | EOS |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tide | 0 | 0 | 0 | 1 | row_uniform | vocabulary | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 480/480 | 480/480 | 452/480 | 480/480 | 452/480 | 0.3% | 480/480 | 480/480 | 480/480 |
| tide | 0 | 0 | 0 | 1 | row_uniform | vocabulary | en/single/POLARITY:NEGATIVE | 960/960 | 957/960 | 837/960 | 960/960 | 832/960 | 0.9% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 0 | 1 | row_uniform | vocabulary | en/single/POLARITY:POSITIVE | 960/960 | 917/960 | 818/960 | 960/960 | 810/960 | 1.3% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 0 | 1 | row_uniform | vocabulary | en/single/TIME:NOW | 960/960 | 918/960 | 796/960 | 958/960 | 792/960 | 1.3% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 0 | 1 | row_uniform | vocabulary | en/single/TIME:PAST | 960/960 | 814/960 | 745/960 | 960/960 | 740/960 | 3.4% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 0 | 1 | row_uniform | vocabulary | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 480/480 | 480/480 | 479/480 | 480/480 | 479/480 | 0.0% | 480/480 | 480/480 | 480/480 |
| tide | 0 | 0 | 0 | 1 | row_uniform | vocabulary | vi/single/POLARITY:NEGATIVE | 960/960 | 956/960 | 954/960 | 960/960 | 952/960 | 0.1% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 0 | 1 | row_uniform | vocabulary | vi/single/POLARITY:POSITIVE | 960/960 | 959/960 | 946/960 | 960/960 | 941/960 | 0.2% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 0 | 1 | row_uniform | vocabulary | vi/single/TIME:NOW | 960/960 | 956/960 | 953/960 | 960/960 | 951/960 | 0.1% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 0 | 1 | row_uniform | vocabulary | vi/single/TIME:PAST | 960/960 | 953/960 | 945/960 | 959/960 | 945/960 | 0.1% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 1 | 1 | row_uniform | vocabulary | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 480/480 | 478/480 | 446/480 | 479/480 | 443/480 | 0.3% | 480/480 | 480/480 | 480/480 |
| tide | 0 | 0 | 1 | 1 | row_uniform | vocabulary | en/single/POLARITY:NEGATIVE | 960/960 | 955/960 | 791/960 | 955/960 | 772/960 | 1.3% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 1 | 1 | row_uniform | vocabulary | en/single/POLARITY:POSITIVE | 960/960 | 860/960 | 721/960 | 955/960 | 707/960 | 2.5% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 1 | 1 | row_uniform | vocabulary | en/single/TIME:NOW | 960/960 | 909/960 | 741/960 | 953/960 | 716/960 | 1.7% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 1 | 1 | row_uniform | vocabulary | en/single/TIME:PAST | 960/960 | 776/960 | 679/960 | 959/960 | 665/960 | 4.3% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 1 | 1 | row_uniform | vocabulary | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 480/480 | 476/480 | 449/480 | 472/480 | 437/480 | 0.9% | 480/480 | 480/480 | 480/480 |
| tide | 0 | 0 | 1 | 1 | row_uniform | vocabulary | vi/single/POLARITY:NEGATIVE | 960/960 | 927/960 | 835/960 | 938/960 | 801/960 | 2.3% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 1 | 1 | row_uniform | vocabulary | vi/single/POLARITY:POSITIVE | 960/960 | 942/960 | 847/960 | 949/960 | 812/960 | 1.9% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 1 | 1 | row_uniform | vocabulary | vi/single/TIME:NOW | 960/960 | 925/960 | 829/960 | 931/960 | 792/960 | 2.7% | 960/960 | 960/960 | 960/960 |
| tide | 0 | 0 | 1 | 1 | row_uniform | vocabulary | vi/single/TIME:PAST | 960/960 | 941/960 | 864/960 | 947/960 | 838/960 | 1.6% | 960/960 | 960/960 | 960/960 |

## Primary-mode validation diagnostics by seed

Counts below preserve the frozen seed-by-seed gate denominator. No generated or reference text is included.

| Self-feeding rate | Source-copy weight | Language-balance weight | TIDE aux multiplier | Edge balance | Decoder | Seed | Bucket | Checker coverage | Action fidelity | Preservation | Context marker | Accepted references | CER | Unicode | EOS | Failure reason | Bucket gate |
|---:|---:|---:|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 17 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 160/160 | 160/160 | 160/160 | 160/160 | 0.0% | 160/160 | 160/160 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 17 | en/single/POLARITY:NEGATIVE | 320/320 | 319/320 | 299/320 | 320/320 | 297/320 | 0.5% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 17 | en/single/POLARITY:POSITIVE | 320/320 | 319/320 | 311/320 | 320/320 | 309/320 | 0.3% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 17 | en/single/TIME:NOW | 320/320 | 319/320 | 300/320 | 320/320 | 300/320 | 0.5% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 17 | en/single/TIME:PAST | 320/320 | 319/320 | 311/320 | 320/320 | 310/320 | 0.2% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 17 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 160/160 | 160/160 | 160/160 | 160/160 | 0.0% | 160/160 | 160/160 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 17 | vi/single/POLARITY:NEGATIVE | 320/320 | 320/320 | 319/320 | 320/320 | 319/320 | 0.0% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 17 | vi/single/POLARITY:POSITIVE | 320/320 | 320/320 | 314/320 | 320/320 | 314/320 | 0.2% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 17 | vi/single/TIME:NOW | 320/320 | 320/320 | 318/320 | 320/320 | 318/320 | 0.0% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 17 | vi/single/TIME:PAST | 320/320 | 320/320 | 319/320 | 320/320 | 319/320 | 0.0% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 23 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 160/160 | 155/160 | 160/160 | 155/160 | 0.2% | 160/160 | 160/160 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 23 | en/single/POLARITY:NEGATIVE | 320/320 | 319/320 | 285/320 | 320/320 | 283/320 | 1.0% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 23 | en/single/POLARITY:POSITIVE | 320/320 | 280/320 | 256/320 | 320/320 | 255/320 | 2.1% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 23 | en/single/TIME:NOW | 320/320 | 286/320 | 259/320 | 320/320 | 257/320 | 1.6% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 23 | en/single/TIME:PAST | 320/320 | 211/320 | 196/320 | 320/320 | 193/320 | 7.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 23 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 160/160 | 159/160 | 160/160 | 159/160 | 0.0% | 160/160 | 160/160 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 23 | vi/single/POLARITY:NEGATIVE | 320/320 | 319/320 | 317/320 | 320/320 | 317/320 | 0.1% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 23 | vi/single/POLARITY:POSITIVE | 320/320 | 319/320 | 315/320 | 320/320 | 310/320 | 0.2% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 23 | vi/single/TIME:NOW | 320/320 | 319/320 | 317/320 | 320/320 | 317/320 | 0.1% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 23 | vi/single/TIME:PAST | 320/320 | 313/320 | 308/320 | 319/320 | 308/320 | 0.3% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 41 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 160/160 | 137/160 | 160/160 | 137/160 | 0.6% | 160/160 | 160/160 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 41 | en/single/POLARITY:NEGATIVE | 320/320 | 319/320 | 253/320 | 320/320 | 252/320 | 1.3% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 41 | en/single/POLARITY:POSITIVE | 320/320 | 318/320 | 251/320 | 320/320 | 246/320 | 1.6% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 41 | en/single/TIME:NOW | 320/320 | 313/320 | 237/320 | 318/320 | 235/320 | 1.7% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 41 | en/single/TIME:PAST | 320/320 | 284/320 | 238/320 | 320/320 | 237/320 | 3.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 41 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 160/160 | 160/160 | 160/160 | 160/160 | 0.0% | 160/160 | 160/160 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 41 | vi/single/POLARITY:NEGATIVE | 320/320 | 317/320 | 318/320 | 320/320 | 316/320 | 0.2% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 41 | vi/single/POLARITY:POSITIVE | 320/320 | 320/320 | 317/320 | 320/320 | 317/320 | 0.1% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 41 | vi/single/TIME:NOW | 320/320 | 317/320 | 318/320 | 320/320 | 316/320 | 0.1% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 0 | 1 | row_uniform | vocabulary | 41 | vi/single/TIME:PAST | 320/320 | 320/320 | 318/320 | 320/320 | 318/320 | 0.0% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 1 | 1 | row_uniform | vocabulary | 17 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 159/160 | 152/160 | 160/160 | 151/160 | 0.3% | 160/160 | 160/160 | — | pass |
| 0 | 0 | 1 | 1 | row_uniform | vocabulary | 17 | en/single/POLARITY:NEGATIVE | 320/320 | 316/320 | 267/320 | 319/320 | 257/320 | 1.3% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 1 | 1 | row_uniform | vocabulary | 17 | en/single/POLARITY:POSITIVE | 320/320 | 264/320 | 217/320 | 318/320 | 208/320 | 3.7% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | 1 | 1 | row_uniform | vocabulary | 17 | en/single/TIME:NOW | 320/320 | 290/320 | 242/320 | 319/320 | 221/320 | 2.1% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 1 | 1 | row_uniform | vocabulary | 17 | en/single/TIME:PAST | 320/320 | 246/320 | 209/320 | 319/320 | 205/320 | 5.2% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | 1 | 1 | row_uniform | vocabulary | 17 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 160/160 | 160/160 | 160/160 | 160/160 | 0.0% | 160/160 | 160/160 | — | pass |
| 0 | 0 | 1 | 1 | row_uniform | vocabulary | 17 | vi/single/POLARITY:NEGATIVE | 320/320 | 319/320 | 318/320 | 320/320 | 316/320 | 0.1% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 1 | 1 | row_uniform | vocabulary | 17 | vi/single/POLARITY:POSITIVE | 320/320 | 319/320 | 320/320 | 320/320 | 319/320 | 0.0% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 1 | 1 | row_uniform | vocabulary | 17 | vi/single/TIME:NOW | 320/320 | 320/320 | 313/320 | 320/320 | 312/320 | 0.1% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 1 | 1 | row_uniform | vocabulary | 17 | vi/single/TIME:PAST | 320/320 | 319/320 | 319/320 | 320/320 | 319/320 | 0.0% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 1 | 1 | row_uniform | vocabulary | 23 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 160/160 | 152/160 | 160/160 | 152/160 | 0.3% | 160/160 | 160/160 | — | pass |
| 0 | 0 | 1 | 1 | row_uniform | vocabulary | 23 | en/single/POLARITY:NEGATIVE | 320/320 | 320/320 | 288/320 | 320/320 | 284/320 | 1.0% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 1 | 1 | row_uniform | vocabulary | 23 | en/single/POLARITY:POSITIVE | 320/320 | 286/320 | 268/320 | 319/320 | 265/320 | 1.9% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | 1 | 1 | row_uniform | vocabulary | 23 | en/single/TIME:NOW | 320/320 | 299/320 | 271/320 | 318/320 | 268/320 | 1.3% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 1 | 1 | row_uniform | vocabulary | 23 | en/single/TIME:PAST | 320/320 | 237/320 | 224/320 | 320/320 | 221/320 | 5.2% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | 1 | 1 | row_uniform | vocabulary | 23 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 160/160 | 160/160 | 160/160 | 160/160 | 0.0% | 160/160 | 160/160 | — | pass |
| 0 | 0 | 1 | 1 | row_uniform | vocabulary | 23 | vi/single/POLARITY:NEGATIVE | 320/320 | 319/320 | 318/320 | 320/320 | 317/320 | 0.1% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 1 | 1 | row_uniform | vocabulary | 23 | vi/single/POLARITY:POSITIVE | 320/320 | 319/320 | 318/320 | 320/320 | 317/320 | 0.1% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 1 | 1 | row_uniform | vocabulary | 23 | vi/single/TIME:NOW | 320/320 | 320/320 | 319/320 | 320/320 | 319/320 | 0.0% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 1 | 1 | row_uniform | vocabulary | 23 | vi/single/TIME:PAST | 320/320 | 312/320 | 310/320 | 320/320 | 310/320 | 0.3% | 320/320 | 320/320 | — | pass |
| 0 | 0 | 1 | 1 | row_uniform | vocabulary | 41 | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 159/160 | 142/160 | 159/160 | 140/160 | 0.4% | 160/160 | 160/160 | — | pass |
| 0 | 0 | 1 | 1 | row_uniform | vocabulary | 41 | en/single/POLARITY:NEGATIVE | 320/320 | 319/320 | 236/320 | 316/320 | 231/320 | 1.7% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 1 | 1 | row_uniform | vocabulary | 41 | en/single/POLARITY:POSITIVE | 320/320 | 310/320 | 236/320 | 318/320 | 234/320 | 2.0% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 1 | 1 | row_uniform | vocabulary | 41 | en/single/TIME:NOW | 320/320 | 320/320 | 228/320 | 316/320 | 227/320 | 1.5% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 1 | 1 | row_uniform | vocabulary | 41 | en/single/TIME:PAST | 320/320 | 293/320 | 246/320 | 320/320 | 239/320 | 2.4% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 1 | 1 | row_uniform | vocabulary | 41 | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 160/160 | 156/160 | 129/160 | 152/160 | 117/160 | 2.8% | 160/160 | 160/160 | — | pass |
| 0 | 0 | 1 | 1 | row_uniform | vocabulary | 41 | vi/single/POLARITY:NEGATIVE | 320/320 | 289/320 | 199/320 | 298/320 | 168/320 | 6.6% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 1 | 1 | row_uniform | vocabulary | 41 | vi/single/POLARITY:POSITIVE | 320/320 | 304/320 | 209/320 | 309/320 | 176/320 | 5.6% | 320/320 | 320/320 | preservation_pass | fail |
| 0 | 0 | 1 | 1 | row_uniform | vocabulary | 41 | vi/single/TIME:NOW | 320/320 | 285/320 | 197/320 | 291/320 | 161/320 | 8.0% | 320/320 | 320/320 | action_fidelity_pass, preservation_pass | fail |
| 0 | 0 | 1 | 1 | row_uniform | vocabulary | 41 | vi/single/TIME:PAST | 320/320 | 310/320 | 235/320 | 307/320 | 209/320 | 4.6% | 320/320 | 320/320 | preservation_pass | fail |

## Limits and interpretation

Valid Unicode and EOS termination do not establish semantic correctness. The deterministic checker covers only the declared synthetic tense/polarity grammar and named roles. This benchmark tests recombination of familiar lexical factors; it does not establish naturalness, natural-corpus efficacy, or scientific efficacy. Control results are diagnostic; no TIDE advantage is claimed.

All examples and generated outputs remain private under Git-ignored `data/` and `runs/`. This report contains aggregate metrics only. `human_validated` is false. PhoMT raw/derived data and Phan Rang Cham data were not used.

Private aggregate evidence: `vi-en-ai-v4.29/protocol.json`, validation generation metrics under `vi-en-ai-v4.29`, and associated ignored run artifacts. Protocol SHA-256: `d4d33cedbbec2fe53147653c4a729e12175408cff9d7fc05828fc4b4a13a02d8`.
