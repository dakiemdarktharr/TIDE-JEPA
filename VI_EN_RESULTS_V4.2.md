# TIDE-JEPA preliminary Vi–En pilot results

This is an AI-authored and AI-reviewed synthetic pilot. **It is preliminary and has not been human/native-speaker validated.** PhoMT was not used for training; Phan Rang Cham is excluded.

## Frozen v4.2 evaluation

The fresh v4.2 corpus has 1,280 records across 32 event families (20/6/6 train/validation/release holdout). Its 28 abstract templates are shared across partitions, so the holdout probes new event families and a narrow action composition, not broad template or domain generalization. The test split was opened once after all 12 preregistered configurations completed training; these results were not used for tuning.

Four controls, seeds 17/23/41, 80 epochs and 800 updates per run were fixed in the protocol. Models use a width-48, four-head, two-layer configuration. Checkpoints were selected using validation token and path token cross-entropy. UTF-8-constrained greedy decoding is part of this protocol.

The preregistered quality gate failed. Every configuration had zero accepted-reference matches and zero preservation passes in every language/action bucket. All outputs were valid Unicode and all terminated with EOS; these mechanical checks do not establish useful generation. Action fidelity varied by bucket and did not meet every frozen threshold.

| Mode | Test token CE, mean ± SD | Test path token CE, mean ± SD | Accepted refs | Valid Unicode | EOS terminated | Gate |
|---|---:|---:|---:|---:|---:|---|
| token_only | 1.9154 ± 0.0207 | 1.7770 ± 0.0310 | 0/648 | 648/648 (100.0%) | 648/648 (100.0%) | **fail** |
| generic_jepa | 1.9244 ± 0.0403 | 1.7654 ± 0.0504 | 0/648 | 648/648 (100.0%) | 648/648 (100.0%) | **fail** |
| static_alignment | 1.9298 ± 0.0340 | 1.7689 ± 0.0414 | 0/648 | 648/648 (100.0%) | 648/648 (100.0%) | **fail** |
| tide | 1.9261 ± 0.0311 | 1.7681 ± 0.0392 | 0/648 | 648/648 (100.0%) | 648/648 (100.0%) | **fail** |

Across all 12 runs: **0/2592 accepted-reference matches**, 2592/2592 valid Unicode outputs, 2592/2592 EOS-terminated outputs. Overall frozen quality gate: **fail**.

## Action-fidelity and preservation breakdown

Pooled across the three seeds for each mode; each value is passes/known examples. Thresholds require at least 90% for single actions and 80% for held-out paths, separately in every language/action bucket. Preservation was 0 throughout.

| Mode | Bucket | Action fidelity | Preservation | Accepted refs |
|---|---|---:|---:|---:|
| token_only | en/held_out_path/TIME:PAST+POLARITY:NEGATIVE | 32/36 (88.9%) | 0/36 | 0/36 |
| token_only | en/single/POLARITY:NEGATIVE | 19/72 (26.4%) | 0/72 | 0/72 |
| token_only | en/single/POLARITY:POSITIVE | 6/72 (8.3%) | 0/72 | 0/72 |
| token_only | en/single/TIME:NOW | 0/72 (0.0%) | 0/72 | 0/72 |
| token_only | en/single/TIME:PAST | 35/72 (48.6%) | 0/72 | 0/72 |
| token_only | vi/held_out_path/TIME:PAST+POLARITY:NEGATIVE | 36/36 (100.0%) | 0/36 | 0/36 |
| token_only | vi/single/POLARITY:NEGATIVE | 33/72 (45.8%) | 0/72 | 0/72 |
| token_only | vi/single/POLARITY:POSITIVE | 0/72 (0.0%) | 0/72 | 0/72 |
| token_only | vi/single/TIME:NOW | 0/72 (0.0%) | 0/72 | 0/72 |
| token_only | vi/single/TIME:PAST | 34/72 (47.2%) | 0/72 | 0/72 |
| generic_jepa | en/held_out_path/TIME:PAST+POLARITY:NEGATIVE | 21/36 (58.3%) | 0/36 | 0/36 |
| generic_jepa | en/single/POLARITY:NEGATIVE | 21/72 (29.2%) | 0/72 | 0/72 |
| generic_jepa | en/single/POLARITY:POSITIVE | 16/72 (22.2%) | 0/72 | 0/72 |
| generic_jepa | en/single/TIME:NOW | 0/72 (0.0%) | 0/72 | 0/72 |
| generic_jepa | en/single/TIME:PAST | 32/72 (44.4%) | 0/72 | 0/72 |
| generic_jepa | vi/held_out_path/TIME:PAST+POLARITY:NEGATIVE | 34/36 (94.4%) | 0/36 | 0/36 |
| generic_jepa | vi/single/POLARITY:NEGATIVE | 31/72 (43.1%) | 0/72 | 0/72 |
| generic_jepa | vi/single/POLARITY:POSITIVE | 0/72 (0.0%) | 0/72 | 0/72 |
| generic_jepa | vi/single/TIME:NOW | 0/72 (0.0%) | 0/72 | 0/72 |
| generic_jepa | vi/single/TIME:PAST | 36/72 (50.0%) | 0/72 | 0/72 |
| static_alignment | en/held_out_path/TIME:PAST+POLARITY:NEGATIVE | 26/36 (72.2%) | 0/36 | 0/36 |
| static_alignment | en/single/POLARITY:NEGATIVE | 22/72 (30.6%) | 0/72 | 0/72 |
| static_alignment | en/single/POLARITY:POSITIVE | 21/72 (29.2%) | 0/72 | 0/72 |
| static_alignment | en/single/TIME:NOW | 0/72 (0.0%) | 0/72 | 0/72 |
| static_alignment | en/single/TIME:PAST | 34/72 (47.2%) | 0/72 | 0/72 |
| static_alignment | vi/held_out_path/TIME:PAST+POLARITY:NEGATIVE | 35/36 (97.2%) | 0/36 | 0/36 |
| static_alignment | vi/single/POLARITY:NEGATIVE | 34/72 (47.2%) | 0/72 | 0/72 |
| static_alignment | vi/single/POLARITY:POSITIVE | 0/72 (0.0%) | 0/72 | 0/72 |
| static_alignment | vi/single/TIME:NOW | 0/72 (0.0%) | 0/72 | 0/72 |
| static_alignment | vi/single/TIME:PAST | 36/72 (50.0%) | 0/72 | 0/72 |
| tide | en/held_out_path/TIME:PAST+POLARITY:NEGATIVE | 14/36 (38.9%) | 0/36 | 0/36 |
| tide | en/single/POLARITY:NEGATIVE | 18/72 (25.0%) | 0/72 | 0/72 |
| tide | en/single/POLARITY:POSITIVE | 16/72 (22.2%) | 0/72 | 0/72 |
| tide | en/single/TIME:NOW | 0/72 (0.0%) | 0/72 | 0/72 |
| tide | en/single/TIME:PAST | 38/72 (52.8%) | 0/72 | 0/72 |
| tide | vi/held_out_path/TIME:PAST+POLARITY:NEGATIVE | 35/36 (97.2%) | 0/36 | 0/36 |
| tide | vi/single/POLARITY:NEGATIVE | 32/72 (44.4%) | 0/72 | 0/72 |
| tide | vi/single/POLARITY:POSITIVE | 0/72 (0.0%) | 0/72 | 0/72 |
| tide | vi/single/TIME:NOW | 0/72 (0.0%) | 0/72 | 0/72 |
| tide | vi/single/TIME:PAST | 36/72 (50.0%) | 0/72 | 0/72 |

## Interpretation and limits

The model learned the training set in a one-event overfit diagnostic, but none of the frozen v4.2 configurations generalized usefully to the release holdout under this generator. Teacher-forced loss and valid Unicode do not imply semantic correctness. The deterministic semantic checker covers only its declared synthetic present/past and polarity grammar plus named roles; it is not a human language-quality measure. Shared abstract templates, one target per state, three seeds, CPU-only execution, and no matched-FLOP comparison limit conclusions. No TIDE advantage, natural-language efficacy, or human validation is established.

The v4.2 negative result is frozen. Do not tune against this opened holdout. Any further model or protocol work requires a new version, fresh independent review, and a new untouched test set. PhoMT-derived labels remain a separate permission and bilingual review gate; Phan Rang Cham remains deferred pending data-use permission and language review.

## Verified engineering scope

- The 58-test CPU unit suite and root crash/replay probes passed after the final implementation changes; compileall passed. The final `pip check` is recorded in the workspace verification log.
- Two independent Luna/high AI reviews approved the v4.2 draft for this preliminary synthetic scope. `human_validated` is false.
- Group/frame/exact-text leakage checks, frozen fingerprints, checkpoint/config identity checks, and epoch-resume tensor equivalence are covered by the engineering suite.
- PhoMT raw/derived rows and generated examples stay private under Git-ignored `data/` or `runs/`; this report contains aggregate metrics only. No release was performed.

Private machine-readable aggregate evidence: `vi-en-ai-v4.2/suite_report.json` and the frozen protocol/review records in `vi-en-ai-v4.2/`. Raw examples, generated rows, and model weights are not included in this published summary.
