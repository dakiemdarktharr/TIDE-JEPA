# vi-en-ai-v4.10 Vi–En validation results

AI-authored and independently AI-reviewed preliminary synthetic pilot. **Not human/native-speaker validated.** PhoMT was not used. Phan Rang Cham remains excluded.

## Frozen protocol

The corpus has 7680 records and 192 event combinations. Split groups: 112/40/40; records: 4480/1600/1600 (train/validation/release holdout). Data split policy: 112 train, 40 validation, 40 release-holdout combinations (schema split label test) from three new agents; every held-out factor pair is represented in training; English NOW uses present progressive.

Four controls; seeds 17, 23, 41; 58 epochs and 3248 updates/config; width 48, 4 heads, 2 layers. Checkpoints selected with validation token and path token CE. Decoder: greedy byte-level UTF-8 constrained decoding; EOS only at complete codepoint boundaries.

The registered primary mode is `tide`. Its engineering gate requires every seed and every language/action bucket to meet the frozen thresholds.

### Primary TIDE gate by seed

The gate counts checks per seed, with 8 single-action language/action buckets and 2 path buckets. All three seeds passed action-fidelity checks and valid-Unicode checks. Both path buckets passed the frozen path-preservation threshold for every seed. The single-action preservation threshold failed repeatedly:

| Seed | Single-action action fidelity | Single-action preservation | Path preservation | Unicode buckets |
|---:|---:|---:|---:|---:|
| 17 | 8/8 | 5/8 | 2/2 | 10/10 |
| 23 | 8/8 | 2/8 | 2/2 | 10/10 |
| 41 | 8/8 | 2/8 | 2/2 | 10/10 |

The release gate therefore failed on single-action preservation, despite high action fidelity and valid decoding. The held-out release test remains sealed.

## Validation result: **FAIL**

The release holdout was not evaluated and remains sealed.

| Mode | Seed | Val token CE | Val path token CE | Updates | Training wall seconds | Mean examples/sec | Gate |
|---|---:|---:|---:|---:|---:|---:|---|
| token_only | 17 | 0.0133 | 0.0095 | 3248 | 1341.3 | 194.2 | control_only |
| generic_jepa | 17 | 0.0115 | 0.0069 | 3248 | 1511.2 | 172.4 | control_only |
| static_alignment | 17 | 0.0085 | 0.0053 | 3248 | 1536.5 | 169.4 | control_only |
| tide | 17 | 0.0097 | 0.0057 | 3248 | 1557.6 | 167.2 | fail |
| token_only | 23 | 0.0082 | 0.0026 | 3248 | 1350.8 | 192.8 | control_only |
| generic_jepa | 23 | 0.0617 | 0.0355 | 3248 | 1487.0 | 175.0 | control_only |
| static_alignment | 23 | 0.0441 | 0.0280 | 3248 | 1517.9 | 171.3 | control_only |
| tide | 23 | 0.0223 | 0.0083 | 3248 | 1554.0 | 167.5 | fail |
| token_only | 41 | 0.0126 | 0.0063 | 3248 | 1333.6 | 195.2 | control_only |
| generic_jepa | 41 | 0.0098 | 0.0054 | 3248 | 1423.8 | 183.6 | control_only |
| static_alignment | 41 | 0.0090 | 0.0045 | 3248 | 1451.9 | 180.7 | control_only |
| tide | 41 | 0.0318 | 0.0114 | 3248 | 1437.6 | 182.6 | fail |

## Validation generation by mode and bucket

Action fidelity and preservation are pooled across seeds within each bucket; thresholds are still checked for every seed/bucket. Exact-reference match and CER are synthetic-reference metrics, not human naturalness.

| Mode | Bucket | Action fidelity | Preservation | Accepted references | CER | Unicode | EOS |
|---|---|---:|---:|---:|---:|---:|---:|
| token_only | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 239/240 | 228/240 | 226/240 | 0.7% | 240/240 | 240/240 |
| token_only | en/single/POLARITY:NEGATIVE | 480/480 | 446/480 | 446/480 | 0.8% | 480/480 | 480/480 |
| token_only | en/single/POLARITY:POSITIVE | 475/480 | 421/480 | 414/480 | 1.9% | 480/480 | 480/480 |
| token_only | en/single/TIME:NOW | 478/480 | 430/480 | 426/480 | 1.4% | 480/480 | 480/480 |
| token_only | en/single/TIME:PAST | 476/480 | 401/480 | 395/480 | 2.6% | 480/480 | 480/480 |
| token_only | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 239/240 | 225/240 | 224/240 | 0.7% | 240/240 | 240/240 |
| token_only | vi/single/POLARITY:NEGATIVE | 471/480 | 436/480 | 423/480 | 1.6% | 480/480 | 480/480 |
| token_only | vi/single/POLARITY:POSITIVE | 472/480 | 431/480 | 420/480 | 1.6% | 480/480 | 480/480 |
| token_only | vi/single/TIME:NOW | 471/480 | 423/480 | 408/480 | 2.0% | 480/480 | 480/480 |
| token_only | vi/single/TIME:PAST | 470/480 | 436/480 | 430/480 | 1.3% | 480/480 | 480/480 |
| generic_jepa | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 240/240 | 224/240 | 223/240 | 0.6% | 240/240 | 240/240 |
| generic_jepa | en/single/POLARITY:NEGATIVE | 479/480 | 445/480 | 443/480 | 0.7% | 480/480 | 480/480 |
| generic_jepa | en/single/POLARITY:POSITIVE | 478/480 | 423/480 | 418/480 | 1.4% | 480/480 | 480/480 |
| generic_jepa | en/single/TIME:NOW | 477/480 | 435/480 | 434/480 | 1.1% | 480/480 | 480/480 |
| generic_jepa | en/single/TIME:PAST | 479/480 | 421/480 | 414/480 | 1.9% | 480/480 | 480/480 |
| generic_jepa | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 238/240 | 227/240 | 225/240 | 0.6% | 240/240 | 240/240 |
| generic_jepa | vi/single/POLARITY:NEGATIVE | 473/480 | 441/480 | 434/480 | 1.0% | 480/480 | 480/480 |
| generic_jepa | vi/single/POLARITY:POSITIVE | 467/480 | 434/480 | 417/480 | 2.2% | 480/480 | 480/480 |
| generic_jepa | vi/single/TIME:NOW | 464/480 | 440/480 | 413/480 | 1.9% | 480/480 | 480/480 |
| generic_jepa | vi/single/TIME:PAST | 470/480 | 450/480 | 445/480 | 0.9% | 480/480 | 480/480 |
| static_alignment | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 240/240 | 229/240 | 228/240 | 0.6% | 240/240 | 240/240 |
| static_alignment | en/single/POLARITY:NEGATIVE | 480/480 | 443/480 | 442/480 | 0.9% | 480/480 | 480/480 |
| static_alignment | en/single/POLARITY:POSITIVE | 479/480 | 439/480 | 435/480 | 1.2% | 480/480 | 480/480 |
| static_alignment | en/single/TIME:NOW | 479/480 | 446/480 | 444/480 | 0.9% | 480/480 | 480/480 |
| static_alignment | en/single/TIME:PAST | 477/480 | 435/480 | 429/480 | 1.3% | 480/480 | 480/480 |
| static_alignment | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 240/240 | 226/240 | 225/240 | 0.5% | 240/240 | 240/240 |
| static_alignment | vi/single/POLARITY:NEGATIVE | 476/480 | 438/480 | 429/480 | 1.3% | 480/480 | 480/480 |
| static_alignment | vi/single/POLARITY:POSITIVE | 475/480 | 434/480 | 431/480 | 1.3% | 480/480 | 480/480 |
| static_alignment | vi/single/TIME:NOW | 472/480 | 427/480 | 410/480 | 1.7% | 480/480 | 480/480 |
| static_alignment | vi/single/TIME:PAST | 474/480 | 452/480 | 448/480 | 0.8% | 480/480 | 480/480 |
| tide | en/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 240/240 | 214/240 | 213/240 | 0.9% | 240/240 | 240/240 |
| tide | en/single/POLARITY:NEGATIVE | 480/480 | 413/480 | 409/480 | 1.2% | 480/480 | 480/480 |
| tide | en/single/POLARITY:POSITIVE | 471/480 | 364/480 | 360/480 | 3.6% | 480/480 | 480/480 |
| tide | en/single/TIME:NOW | 473/480 | 382/480 | 376/480 | 2.2% | 480/480 | 480/480 |
| tide | en/single/TIME:PAST | 474/480 | 384/480 | 376/480 | 2.6% | 480/480 | 480/480 |
| tide | vi/held_out_path/POLARITY:NEGATIVE+TIME:PAST | 237/240 | 229/240 | 225/240 | 0.7% | 240/240 | 240/240 |
| tide | vi/single/POLARITY:NEGATIVE | 468/480 | 420/480 | 408/480 | 2.1% | 480/480 | 480/480 |
| tide | vi/single/POLARITY:POSITIVE | 476/480 | 438/480 | 428/480 | 1.5% | 480/480 | 480/480 |
| tide | vi/single/TIME:NOW | 468/480 | 410/480 | 394/480 | 2.5% | 480/480 | 480/480 |
| tide | vi/single/TIME:PAST | 468/480 | 454/480 | 443/480 | 1.2% | 480/480 | 480/480 |

## Limits and interpretation

Valid Unicode and EOS termination do not establish semantic correctness. The deterministic checker covers only the declared synthetic tense/polarity grammar and named roles. This benchmark tests recombination of familiar lexical factors; it does not establish naturalness, natural-corpus efficacy, or scientific efficacy. Control results are diagnostic; no TIDE advantage is claimed.

All examples and generated outputs remain private under Git-ignored `data/` and `runs/`. This report contains aggregate metrics only. `human_validated` is false. PhoMT raw/derived data and Phan Rang Cham data were not used.

Private aggregate evidence: `vi-en-ai-v4.10/protocol.json`, validation generation metrics under `vi-en-ai-v4.10`, and associated ignored run artifacts. Protocol SHA-256: `b5c25b54d917faa35ac58649c6565fdd94320f5fd01d4b8b28aa5b0fd95e2d48`.
