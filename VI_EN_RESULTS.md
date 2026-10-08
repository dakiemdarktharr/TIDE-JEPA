# TIDE-JEPA preliminary Vi–En pilot results

This is an AI-authored and AI-reviewed synthetic pilot. **It is preliminary and has not been human/native-speaker validated.** PhoMT was not used for training; Phan Rang Cham is excluded.

## Current status: v4.33 narrow synthetic gate passed; demo remains diagnostic-only

v4.33 completed six fixed-final runs (TIDE and token-only, three seeds, 58 epochs). After correcting a missing checker registration by rescoring the unchanged cached validation generations, all three TIDE seeds passed every validation bucket. A separate v2 amendment bound the original protocol, unchanged thresholds, training identities, current evaluator and corrected validation evidence before test scoring. All 30/30 TIDE release-test buckets passed; the aggregate report includes all six configs and hashes. The original checker-failure metrics remain preserved. Token-only was similar and there is no consistent TIDE advantage. The stock UI default was out of corpus and produced a corrupted output; the runner now defaults to an approved train-only example that passes the narrow checker. A separate 19-case HTTP/allowlist boundary smoke passed its expected accept/refusal statuses, but it is not a semantic OOD detector. Two bounded 240-request runtime runs also passed with stable sampled RSS. Subsequent varied-input loopback checks used 40 approved train-only requests per pass, balanced across language and task; the narrow action/preservation checker passed 10/10 cases in each of four cells on both passes. Four-client overload checks returned one 200 and 79 schema-valid 503 responses per 80-request pass under the one-inference limit. These are bounded synthetic diagnostics, not natural-corpus quality or production-capacity evidence. Semantic OOD and human validation remain unverified, so the checkpoint stays diagnostic-only and is not approved for natural-language or translation use. A two-reviewer preliminary Luna review of 48 stratified validation outputs found 47/48 naturalness-acceptable and 48/48 passing sampled meaning/action checks, with one spelling issue. Human/native-speaker review and natural-corpus quality are not established. See [v4.33 status](VI_EN_RESULTS_V4.33_STATUS.md), [checker reassessment](audits/2026-10-08/v433_validation_checker_reassessment.json), [release report](audits/2026-10-08/v433_release_holdout_aggregate.json), [varied demo run 1](audits/2026-10-09/v433_demo_varied_quality_benchmark_1.json), [run 2](audits/2026-10-09/v433_demo_varied_quality_benchmark_2.json), [concurrent demo run 1](audits/2026-10-09/v433_demo_concurrent_bound.json), [run 2](audits/2026-10-09/v433_demo_concurrent_bound_repeat.json), [demo boundary smoke](audits/2026-10-08/v433_demo_boundary_smoke.json), [demo smoke](audits/2026-10-08/v433_demo_smoke.json), and [AI linguistic review](audits/2026-10-08/v433_validation_ai_linguistic_review.json). Earlier negative results and the v4.32 overfit diagnostic remain unchanged in [history](VI_EN_RESULTS_HISTORY.md).

### Previous checkpoint: v4.29

The fresh v4.29 protocol completed all six fixed-final TIDE runs (29 epochs / 3,248 updates each). Post-training integrity checks confirmed code/runtime/approval/config identities, matching `latest.pt` and `best.pt` weights, complete per-epoch train/validation metrics, and no test artifacts. Validation-only generation completed for all six runs, with 17,280 scored examples and complete evaluator identity checks.

The frozen gate **failed**: 1/6 complete configurations passed all buckets and 37/60 seed-by-bucket checks passed (22/30 at language-balance weight 0; 15/30 at weight 1). Unicode, EOS, nonempty output, and semantic checker coverage were each 17,280/17,280. Preservation is the main failure, especially in English single-action buckets; weight 1 also regressed Vietnamese at seed 41. A post-hoc component rescore found English single-action preservation of 83.2% at weight 0 and 76.4% at weight 1; Vietnamese was 98.9% and 87.9%. Distinct actions changed outputs for 100% of 640 paired sources in each run/language, which shows action sensitivity but not correct realization. Accepted-reference matches were 7,894/8,640 at weight 0 and 6,983/8,640 at weight 1; CER was 0.8% and 2.1%. These are synthetic-reference metrics, not human naturalness ratings. The context-marker check is a narrow diagnostic and is not part of the quality gate.

For v4.32, OOD/unsupported-input refusal and truncation quality were not measured. All v4.32 examples are preliminary AI-reviewed synthetic evidence, not human/native-speaker validation. Earlier outcomes and the v4.30 checker limitation remain preserved in [history](VI_EN_RESULTS_HISTORY.md).

### Previous checkpoint: v4.29

v4.27 and v4.28 remain retired incident evidence after review activity inspected holdout content/annotations; neither version produced an eligible sealed-holdout result. v4.29 uses a fresh split and a train/validation-only review package. The v4.8 hashes match its handoff note, but private data/runs are absent on lattice and its Windows runtime identity differs from Linux, so it was not resumed.

### Previous checkpoint: v4.26

v4.26 completed six fixed-final TIDE runs and validation-only generation. It tested source-copy auxiliary weights 0 and 0.25; 1/6 full-config gates and 32/60 seed-by-bucket checks passed, so its frozen gate failed. Unicode, EOS, and checker coverage were complete. Low teacher-forced cross-entropy did not ensure reliable free generation. See [v4.26 status](VI_EN_RESULTS_V4.26_STATUS.md), [validation](VI_EN_RESULTS_V4.26_VALIDATION.md), [component diagnostic](VI_EN_RESULTS_V4.26_DIAGNOSTIC.md), and [action sensitivity](VI_EN_RESULTS_V4.26_ACTION_SENSITIVITY.md).

The v4.26 post-hoc component diagnostic found English single-action preservation of 79.5% at copy weight 0 and 68.8% at 0.25, while Vietnamese preservation improved from 89.3% to 93.7%. Same-source action sensitivity found changed outputs for 640/640 pairs in both languages for every run; this confirms action-conditioned variation, not semantic correctness. OOD/refusal quality was not measured, and EOS termination did not independently test truncation behavior.

### Previous checkpoint: v4.25

v4.25 tested one-pass self-feeding at rate 0.2 against teacher forcing at rate 0; it passed 3/6 full-config gates and 44/60 seed-by-bucket checks. See [v4.25 status](VI_EN_RESULTS_V4.25_STATUS.md) and its linked aggregate reports.

### Previous checkpoint: v4.24

v4.24 completed all six fixed-final-epoch runs (29 epochs / 3,248 updates per checkpoint) and validation-only generation. The evaluator had full coverage; 0/6 configs passed all ten frozen buckets (28/60 individual checks passed). Unicode, EOS, and checker coverage were all 100%; aggregate action fidelity was 95.4% and preservation 83.6%. English TIME:NOW preservation failed in all six configs. The 3,200-record release holdout remains sealed. Three training CSVs contain duplicate conflicting epoch rows, so they do not support epoch-curve claims; the resume guard now fails closed on duplicates. See [v4.24 status](VI_EN_RESULTS_V4.24_STATUS.md), [aggregate report](VI_EN_RESULTS_V4.24_VALIDATION.md), [component diagnostic](VI_EN_RESULTS_V4.24_DIAGNOSTIC.md), and [action sensitivity](VI_EN_RESULTS_V4.24_ACTION_SENSITIVITY.md).

Post-hoc component scoring finds agent/place retention near ceiling and lower patient/predicate retention, especially in English and with source-copy weight 1.5. Requested-action changes produced distinct outputs in 99.8–100% of same-source comparisons, but that does not prove the intended event was preserved. The frozen gate remains unchanged. See the [component metrics](VI_EN_RESULTS_V4.24_DIAGNOSTIC.md) and [action sensitivity](VI_EN_RESULTS_V4.24_ACTION_SENSITIVITY.md). Training-log duplicates prevent reliable teacher-forced loss-curve claims for v4.24.

Earlier, v4.20 also failed its quality gate; the historical outcomes below remain unchanged. Its release holdout remains sealed and its frozen-replay workflow is described in [v4.20 status](VI_EN_RESULTS_V4.20_STATUS.md).

v4.20 completed six fixed-final-epoch CPU runs and validation-only generation. All six checkpoints reached epoch 29 / 3,248 updates with matching `best.pt`/`latest.pt` identities. Unicode and EOS were 100%, but none of the 60 frozen seed-by-bucket gates passed: pooled action fidelity was 42.6% for the vocabulary decoder and 32.5% for the source-pointer decoder; preservation was 0.57% and 0.45%, respectively. The source-pointer hypothesis was not supported. The run exited nonzero at the fail-closed validation-to-test guard; no test metrics or generation were created and the release holdout remains sealed. See [v4.20 status](VI_EN_RESULTS_V4.20_STATUS.md) and the [aggregate validation report](VI_EN_RESULTS_V4.20_VALIDATION.md). Workspace repairs change the frozen implementation identity. The hash-verified `scripts/run_frozen.py` launcher restores access to the original source snapshot for diagnostic inference and cached validation replay; new experiments require a fresh protocol. No human or natural-language quality claim is supported.

v4.21 completed all 12 registered runs and validation generation, but its frozen evaluator omitted the v4.21 family from the semantic checker registry. Checker coverage is zero, so the report is invalid for model-quality scoring; the gate failed closed and the release holdout remains sealed. The artifacts are preserved without post-hoc rescoring. The checker registration is fixed with regression coverage. v4.22 was not frozen or trained: its independent reviews raised factor-balance and progressive-aspect concerns, recorded in [v4.22 status](VI_EN_RESULTS_V4.22_STATUS.md). v4.23 addressed those points with balanced factors and aligned progressive markers, passed two independent AI reviews, and was evaluated with full checker coverage; its quality gate failed and the holdout remains sealed. v4.24 also used a fresh reviewed corpus and complete evaluator coverage, but failed its preservation gate; see [v4.21 status](VI_EN_RESULTS_V4.21_STATUS.md), [v4.22 status](VI_EN_RESULTS_V4.22_STATUS.md), [v4.23 status](VI_EN_RESULTS_V4.23_STATUS.md), and [v4.24 status](VI_EN_RESULTS_V4.24_STATUS.md).

v4.18 completed all 12 frozen CPU runs and validation-only generation, but its frozen semantic evaluator had zero v4.18 checker coverage (`0/0` denominators), making that report invalid for semantic scoring; the gate failed closed and the holdout remains sealed. A post-hoc corrected-checker rescore (diagnostic, not frozen gate evidence) found action fidelity 26.5–52.5% for single actions and 51.0–72.9% for paths, with preservation 0.4–1.9% and 0.8–8.3%, below thresholds. Single-action patient and predicate presence were especially low, indicating weak source-slot retention and transformation control. A separate training-only overfit reached 8/8 on one seen group, which demonstrates memorization capacity but not generalization. A 20-input paired sample comparing epoch-28 `best` with epoch-29 `latest` found zero preservation and zero accepted-reference matches for both; it is only a narrow post-hoc diagnostic. See [v4.18 status](VI_EN_RESULTS_V4.18_STATUS.md), [frozen evaluation report](VI_EN_RESULTS_V4.18_VALIDATION.md), [post-hoc rescore](VI_EN_RESULTS_V4.18_RESCORING.md), [overfit diagnostic](VI_EN_RESULTS_V4.18_OVERFIT_DIAGNOSTIC.md), and [checkpoint sample](VI_EN_RESULTS_V4.18_CHECKPOINT_SAMPLE.md). The preceding v4.17-r2 weighting study also failed all 60 checks; its holdout remains sealed. See [v4.17 status](VI_EN_RESULTS_V4.17_STATUS.md) and [report](VI_EN_RESULTS_V4.17_VALIDATION.md).

v4.19 completed 12/12 frozen CPU runs and validation-only generation after 12/12 config, data, split, code/runtime, and checkpoint identity checks passed. The checker covered all 8,640 validation examples; Unicode and EOS termination were also 100%. The frozen quality gate failed: 0/12 configurations passed every bucket and only 4/120 seed-by-bucket checks passed, mainly due to preservation failures. Its 3,200-record release holdout was not generated or scored and remains sealed. The exact aggregate results and reproduction commands are in [v4.19 status](VI_EN_RESULTS_V4.19_STATUS.md) and the [validation report](VI_EN_RESULTS_V4.19_VALIDATION.md). No human or natural-language validation claim is supported.


v4.15-r1 completed all nine matched runs and validation-only generation. The frozen primary TIDE gate failed: only 3/60 seed-by-bucket checks passed (all Vietnamese held-out paths); no single-action bucket passed preservation. Unicode and EOS were 100%. Pooled single-action preservation was 53.2% for TIDE ×0.5, 49.7% for TIDE ×1.0, and 61.0% for token-only. The fresh release holdout remains sealed, with no test metrics or generated test artifacts. Each seed reuses the same 40 validation groups, so denominators are operational rather than independent linguistic observations. See the [v4.15 status](VI_EN_RESULTS_V4.15_STATUS.md) and [aggregate report](VI_EN_RESULTS_V4.15_VALIDATION.md). Earlier v4.14 and v4.13 failures remain preserved.

### Historical v4.13 result

The fresh v4.13 AI-reviewed synthetic pilot completed all 12 registered runs and validation-only generation. It compared token-only and TIDE with source-copy weights 1.5 and 3.0 across seeds 17/23/41. Both TIDE conditions failed overall: only 10/60 seed-by-bucket checks passed, including one single-action bucket; 47/48 single-action buckets missed the frozen 90% preservation threshold, and 9/12 path buckets met threshold. Unicode and EOS were 100%. Token-only exceeded TIDE in pooled preservation at both weights, so there is no evidence of a TIDE advantage. A direct test-evaluation request was refused before scoring; the fresh release holdout remains sealed and no test metrics exist. See [v4.13 status](VI_EN_RESULTS_V4.13_STATUS.md) and the [aggregate validation report](VI_EN_RESULTS_V4.13_VALIDATION.md). This preliminary result is not human/native-speaker validated and does not support a usable neural language-output claim.

Earlier v4.12, v4.11 and v4.10 results remain preserved in their respective status and validation reports; every release holdout remains sealed.

The v4.8 synthetic pilot was frozen with a fresh split and release holdout. Training was stopped at the user's request after four of 12 configurations completed and four were partial. Four configurations have not started. No validation evaluation or `suite_report.json` exists; the release holdout remains sealed. The dataset, review records, protocol and model checkpoints remain local under Git-ignored `data/` and `runs/`. See the [aggregate-only status note with checkpoint hashes](VI_EN_RESULTS_V4.8_STATUS.md). v4.8 has no quality result yet.

Linux revalidation on 2026-10-03 passed 75 CPU tests with no skips, plus compile, dependency and synthetic crash/identity probes. The v4.8 data and run directories are absent on this host, so this code verification does not resume or evaluate v4.8. v4.9 was superseded before training because evaluator hardening changed its frozen implementation identity. v4.10 and v4.11 also failed their primary TIDE validation gates and have sealed holdouts. See the [v4.11 status](VI_EN_RESULTS_V4.11_STATUS.md) and [aggregate validation report](VI_EN_RESULTS_V4.11_VALIDATION.md), [v4.10 status](VI_EN_RESULTS_V4.10_STATUS.md), [aggregate validation report](VI_EN_RESULTS_V4.10_VALIDATION.md), [v4.9 historical status](VI_EN_RESULTS_V4.9_STATUS.md) and the [Linux revalidation report](audits/2026-10-03/LINUX_REVALIDATION.md).

## Historical frozen vi-en-ai-v4.2 evaluation

The corpus contains 1280 records across 32 meaning frames (20/6/6 train/validation/release-holdout groups; 800/240/240 records). Split scope: 20 train, 6 validation, 6 release-holdout event families, fixed before model selection; fresh families not used in prior versions. The release holdout was opened once after all 12 preregistered configurations completed training; these results were not used for tuning.

Four controls, seeds 17, 23, 41, 80 epochs and 800 updates per run were frozen. Models use width 48, 4 heads and 2 layers. Checkpoints were selected by validation token and path token cross-entropy. Decoder policy: greedy byte-level UTF-8 constrained decoding; EOS only at complete codepoint boundaries.

The frozen quality gate applies to primary mode `tide` and requires every seed and every language/action bucket to meet the protocol thresholds. Controls are diagnostic comparisons and do not define this gate.

| Mode | Test token CE, mean ± SD | Test path token CE, mean ± SD | Accepted refs | Valid Unicode | EOS terminated | Quality gate |
|---|---:|---:|---:|---:|---:|---|
| token_only | 1.9154 ± 0.0207 | 1.7770 ± 0.0310 | 0/648 | 648/648 (100.0%) | 648/648 (100.0%) | **control** |
| generic_jepa | 1.9244 ± 0.0403 | 1.7654 ± 0.0504 | 0/648 | 648/648 (100.0%) | 648/648 (100.0%) | **control** |
| static_alignment | 1.9298 ± 0.0340 | 1.7689 ± 0.0414 | 0/648 | 648/648 (100.0%) | 648/648 (100.0%) | **control** |
| tide | 1.9261 ± 0.0311 | 1.7681 ± 0.0392 | 0/648 | 648/648 (100.0%) | 648/648 (100.0%) | **fail** |

Across all runs: **0/2592 accepted-reference matches**, 2592/2592 valid Unicode outputs, 2592/2592 EOS-terminated outputs. Primary `tide` quality gate: **fail**.

## Action fidelity and state preservation

Values are pooled across seeds within each mode and bucket. Thresholds are evaluated separately for every bucket; a pooled pass across languages/actions cannot hide a failing bucket.

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

Teacher-forced loss and valid Unicode do not establish semantic correctness. The deterministic checker covers only its declared synthetic present/past and polarity grammar plus named roles; it does not measure naturalness. Shared templates, one target per state, three seeds, CPU-only execution and no matched-FLOP comparison limit conclusions. No human validation, natural-corpus efficacy, or TIDE advantage is established.

This vi-en-ai-v4.2 holdout is frozen. Do not tune against it. PhoMT-derived labels remain a separate data-use and bilingual review gate; Phan Rang Cham remains deferred pending dataset-use permission and language/community review.

## Verified engineering scope

- The CPU unit suite, compilation and root crash/replay probes are recorded in the current verification note; passing engineering checks do not establish language quality.
- Two independent Luna/high AI reviews and an adjudication are bound to this version. `human_validated` is false.
- Group/frame/exact-text leakage checks, frozen fingerprints, checkpoint/config identity checks and epoch-resume tensor equivalence are covered by the engineering suite.
- PhoMT raw/derived rows and generated examples remain private under Git-ignored `data/` or `runs/`. This report contains aggregate metrics only; no release was performed.

Private aggregate evidence: `vi-en-ai-v4.2/suite_report.json` and the versioned protocol/review records in `vi-en-ai-v4.2/`. Raw examples, generated rows and model weights are not included in this summary.
