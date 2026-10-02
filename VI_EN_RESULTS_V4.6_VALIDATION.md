# vi-en-ai-v4.6 Vi–En validation results

AI-authored and independently AI-reviewed preliminary synthetic pilot. **Not human/native-speaker validated.** PhoMT was not used. Phan Rang Cham remains excluded.

## Frozen protocol

The corpus has 4160 records and 104 event combinations. Split groups: 80/12/12; records: 3200/480/480 (train/validation/release holdout). Data split policy: 80 train, 12 validation, 12 release-holdout event combinations sampled outside every v4.4 and v4.5 combination; all agent, verb lemma, and patient phrase values occur in training; English NOW uses present progressive; new holdout combinations are unused by prior versions.

Four controls; seeds 17, 23, 41; 80 epochs and 3200 updates/config; width 48, 4 heads, 2 layers. Checkpoints selected with validation token and path token CE. Decoder: greedy byte-level UTF-8 constrained decoding; EOS only at complete codepoint boundaries.

The registered primary mode is `tide`. Its engineering gate requires every seed and every language/action bucket to meet the frozen thresholds.

## Validation result: **FAIL**

The release holdout was not evaluated and remains sealed.

| Mode | Seed | Val token CE | Val path token CE | Updates | Training wall seconds | Mean examples/sec | Gate |
|---|---:|---:|---:|---:|---:|---:|---|
| token_only | 17 | 0.0909 | 0.0761 | 3200 | 1723.3 | 148.8 | control_only |
| generic_jepa | 17 | 0.0816 | 0.0771 | 3200 | 1878.9 | 136.5 | control_only |
| static_alignment | 17 | 0.0724 | 0.0606 | 3200 | 1894.2 | 135.4 | control_only |
| tide | 17 | 0.0824 | 0.0806 | 3200 | 1888.7 | 135.8 | fail |
| token_only | 23 | 0.0680 | 0.0399 | 3200 | 1664.6 | 154.3 | control_only |
| generic_jepa | 23 | 0.0842 | 0.0711 | 3200 | 1808.8 | 142.1 | control_only |
| static_alignment | 23 | 0.0637 | 0.0533 | 3200 | 1824.8 | 140.7 | control_only |
| tide | 23 | 0.0833 | 0.0740 | 3200 | 1837.1 | 139.8 | fail |
| token_only | 41 | 0.1278 | 0.1209 | 3200 | 1648.2 | 155.9 | control_only |
| generic_jepa | 41 | 0.0880 | 0.0739 | 3200 | 1711.0 | 151.0 | control_only |
| static_alignment | 41 | 0.0973 | 0.0826 | 3200 | 1719.6 | 150.5 | control_only |
| tide | 41 | 0.0895 | 0.0752 | 3200 | 1710.2 | 151.9 | fail |

## Validation generation by mode and bucket

Action fidelity and preservation are pooled across seeds within each bucket; thresholds are still checked for every seed/bucket. Exact-reference match and CER are synthetic-reference metrics, not human naturalness.

| Mode | Bucket | Action fidelity | Preservation | Accepted references | CER | Unicode | EOS |
|---|---|---:|---:|---:|---:|---:|---:|
| token_only | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 72/72 | 51/72 | 47/72 | 3.9% | 72/72 | 72/72 |
| token_only | en/single/POLARITY:NEGATIVE | 139/144 | 90/144 | 90/144 | 6.3% | 144/144 | 144/144 |
| token_only | en/single/POLARITY:POSITIVE | 138/144 | 86/144 | 82/144 | 8.1% | 144/144 | 144/144 |
| token_only | en/single/TIME:NOW | 135/144 | 88/144 | 87/144 | 6.9% | 144/144 | 144/144 |
| token_only | en/single/TIME:PAST | 136/144 | 88/144 | 86/144 | 8.0% | 144/144 | 144/144 |
| token_only | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 65/72 | 35/72 | 33/72 | 7.4% | 72/72 | 72/72 |
| token_only | vi/single/POLARITY:NEGATIVE | 141/144 | 85/144 | 81/144 | 6.2% | 144/144 | 144/144 |
| token_only | vi/single/POLARITY:POSITIVE | 135/144 | 91/144 | 80/144 | 8.6% | 144/144 | 144/144 |
| token_only | vi/single/TIME:NOW | 138/144 | 95/144 | 88/144 | 7.2% | 144/144 | 144/144 |
| token_only | vi/single/TIME:PAST | 137/144 | 86/144 | 84/144 | 7.4% | 144/144 | 144/144 |
| generic_jepa | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 70/72 | 48/72 | 46/72 | 5.3% | 72/72 | 72/72 |
| generic_jepa | en/single/POLARITY:NEGATIVE | 144/144 | 89/144 | 87/144 | 5.3% | 144/144 | 144/144 |
| generic_jepa | en/single/POLARITY:POSITIVE | 138/144 | 84/144 | 80/144 | 8.7% | 144/144 | 144/144 |
| generic_jepa | en/single/TIME:NOW | 139/144 | 90/144 | 88/144 | 6.0% | 144/144 | 144/144 |
| generic_jepa | en/single/TIME:PAST | 135/144 | 87/144 | 82/144 | 8.0% | 144/144 | 144/144 |
| generic_jepa | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 64/72 | 42/72 | 40/72 | 8.4% | 72/72 | 72/72 |
| generic_jepa | vi/single/POLARITY:NEGATIVE | 132/144 | 81/144 | 75/144 | 8.0% | 144/144 | 144/144 |
| generic_jepa | vi/single/POLARITY:POSITIVE | 137/144 | 94/144 | 79/144 | 8.6% | 144/144 | 144/144 |
| generic_jepa | vi/single/TIME:NOW | 133/144 | 91/144 | 79/144 | 7.7% | 144/144 | 144/144 |
| generic_jepa | vi/single/TIME:PAST | 134/144 | 83/144 | 78/144 | 8.4% | 144/144 | 144/144 |
| static_alignment | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 72/72 | 56/72 | 52/72 | 2.8% | 72/72 | 72/72 |
| static_alignment | en/single/POLARITY:NEGATIVE | 141/144 | 100/144 | 95/144 | 4.6% | 144/144 | 144/144 |
| static_alignment | en/single/POLARITY:POSITIVE | 138/144 | 88/144 | 84/144 | 7.1% | 144/144 | 144/144 |
| static_alignment | en/single/TIME:NOW | 138/144 | 96/144 | 95/144 | 5.0% | 144/144 | 144/144 |
| static_alignment | en/single/TIME:PAST | 141/144 | 97/144 | 92/144 | 5.6% | 144/144 | 144/144 |
| static_alignment | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 71/72 | 46/72 | 44/72 | 5.5% | 72/72 | 72/72 |
| static_alignment | vi/single/POLARITY:NEGATIVE | 135/144 | 88/144 | 80/144 | 6.6% | 144/144 | 144/144 |
| static_alignment | vi/single/POLARITY:POSITIVE | 134/144 | 104/144 | 92/144 | 7.0% | 144/144 | 144/144 |
| static_alignment | vi/single/TIME:NOW | 138/144 | 104/144 | 95/144 | 5.8% | 144/144 | 144/144 |
| static_alignment | vi/single/TIME:PAST | 132/144 | 89/144 | 83/144 | 6.6% | 144/144 | 144/144 |
| tide | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 72/72 | 50/72 | 46/72 | 4.6% | 72/72 | 72/72 |
| tide | en/single/POLARITY:NEGATIVE | 140/144 | 90/144 | 86/144 | 6.1% | 144/144 | 144/144 |
| tide | en/single/POLARITY:POSITIVE | 135/144 | 91/144 | 82/144 | 9.2% | 144/144 | 144/144 |
| tide | en/single/TIME:NOW | 135/144 | 89/144 | 86/144 | 7.2% | 144/144 | 144/144 |
| tide | en/single/TIME:PAST | 137/144 | 85/144 | 75/144 | 9.2% | 144/144 | 144/144 |
| tide | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 71/72 | 43/72 | 43/72 | 6.0% | 72/72 | 72/72 |
| tide | vi/single/POLARITY:NEGATIVE | 134/144 | 93/144 | 88/144 | 5.9% | 144/144 | 144/144 |
| tide | vi/single/POLARITY:POSITIVE | 137/144 | 94/144 | 86/144 | 8.6% | 144/144 | 144/144 |
| tide | vi/single/TIME:NOW | 134/144 | 94/144 | 86/144 | 7.1% | 144/144 | 144/144 |
| tide | vi/single/TIME:PAST | 131/144 | 94/144 | 89/144 | 6.5% | 144/144 | 144/144 |

## Limits and interpretation

Valid Unicode and EOS termination do not establish semantic correctness. The deterministic checker covers only the declared synthetic tense/polarity grammar and named roles. This benchmark tests recombination of familiar lexical factors; it does not establish naturalness, natural-corpus efficacy, or scientific efficacy. Control results are diagnostic; no TIDE advantage is claimed.

All examples and generated outputs remain private under Git-ignored `data/` and `runs/`. This report contains aggregate metrics only. `human_validated` is false. PhoMT raw/derived data and Phan Rang Cham data were not used.

Private aggregate evidence: `vi-en-ai-v4.6/protocol.json`, validation generation metrics under `vi-en-ai-v4.6`, and associated ignored run artifacts. Protocol SHA-256: `e2ab53fd25f7ae185610627c6db999b53c82375939a124a1ed7403e9a94d301d`.
