# Historical preliminary Vi–En pilot results

This file preserves earlier AI-authored/AI-reviewed synthetic pilot results. All results are preliminary; none were human/native-speaker validated. PhoMT was not used for model training, and Phan Rang Cham remains excluded. **Latest completed quality experiment: v4.29 failed its frozen gate (1/6 full-config gates; 37/60 seed-by-bucket checks); its release holdout remains sealed.** Earlier outcomes and holdouts remain preserved below. See [v4.29 status](VI_EN_RESULTS_V4.29_STATUS.md) and its [aggregate validation report](VI_EN_RESULTS_V4.29_VALIDATION.md). OOD/refusal quality remains unmeasured.

## v4.29 validation

Six fixed-final TIDE runs completed 29 epochs / 3,248 updates each. Integrity checks passed for protocol, approval, code/runtime/config identities, `latest.pt`/`best.pt` equality, complete train/validation metrics, and absence of test artifacts. Validation-only generation covered 17,280 examples. Unicode, EOS, nonempty output, and checker coverage were 17,280/17,280. The frozen quality gate failed: one of six configurations passed all buckets and 37/60 seed-by-bucket checks passed (22/30 at language-balance weight 0; 15/30 at weight 1). Preservation was the primary weakness in English single-action buckets; weight 1 also regressed Vietnamese for seed 41. Accepted-reference matches were 7,894/8,640 and 6,983/8,640; CER was 0.8% and 2.1% for weights 0 and 1. A post-hoc component rescore separated the conditions: English single-action preservation was 83.2% at weight 0 and 76.4% at weight 1; Vietnamese was 98.9% and 87.9%. Distinct actions changed outputs for all 640 paired sources in every run/language, which is action sensitivity but not correctness. The context-marker diagnostic has narrow scope and is not a gate. The 3,200-record release holdout remains sealed. OOD/refusal and truncation quality were not measured. No checkpoint is approved for usable output. See [status](VI_EN_RESULTS_V4.29_STATUS.md), [validation report](VI_EN_RESULTS_V4.29_VALIDATION.md), [component diagnostic](VI_EN_RESULTS_V4.29_DIAGNOSTIC.md), and [action-sensitivity diagnostic](VI_EN_RESULTS_V4.29_ACTION_SENSITIVITY.md).

## 2026-10-07 — v4.30 checker-limited validation

Six fixed-final vocabulary/source-pointer runs completed 29 epochs / 3,248 updates each. Frozen identity and checkpoint checks passed, and validation-only generation covered 17,280 examples. The original frozen report recorded 1/6 configurations and 29/60 seed-by-bucket checks passing. A later train-only negative-control audit exposed a checker defect: it accepts all 1,792 Vietnamese present-progressive references after deleting `đang`, despite accepting all 7,168 intact train singles. The v4.30 frozen score is therefore retained as historical diagnostic evidence, not a confirmatory quality gate. A working checker repair passes all 7,168 intact references and rejects all 1,792 corruptions; it is a different evaluator and does not overwrite frozen scores. No release-test outputs or metrics were created; the 3,200-record release holdout remains sealed. The current trainer now rejects this defective frozen checker before launching a new scoped matrix. See [v4.30 status](VI_EN_RESULTS_V4.30_STATUS.md), [validation](VI_EN_RESULTS_V4.30_VALIDATION.md), and [checker audit/research workflow](RESEARCH_ACCELERATION.md).


Linux code-path revalidation on 2026-10-03 passed 77 CPU tests, compile and dependency checks, plus synthetic crash/identity probes. The checks do not establish model quality. The v4.8 private artifacts are not present on lattice; its local hash verification exists, but the frozen runtime identity differs. See the dated [Linux report](audits/2026-10-03/LINUX_REVALIDATION.md). All earlier model-quality outcomes below remain unchanged.

## v3 baseline

The v3 corpus contained 400 records in 20 event families, with 240/80/80 train/validation/test. Four objective controls and seeds 17/23/41 ran for 40 epochs (120 updates per run). The immutable historical evaluation reported:

| Mode | Test token CE, mean ± SD | Test path token CE, mean ± SD | Exact matches | Valid UTF-8 |
|---|---:|---:|---:|---:|
| token_only | 2.6403 ± 0.0824 | 2.5078 ± 0.0581 | 0/216 | 151/216 (69.9%) |
| generic_jepa | 2.5869 ± 0.0545 | 2.4287 ± 0.0325 | 0/216 | 139/216 (64.4%) |
| static_alignment | 2.5852 ± 0.0513 | 2.4256 ± 0.0303 | 0/216 | 139/216 (64.4%) |
| tide | 2.5862 ± 0.0520 | 2.4275 ± 0.0314 | 0/216 | 135/216 (62.5%) |

Overall, v3 produced 0/864 exact matches and 564/864 valid UTF-8 outputs. Its report did not measure semantic action fidelity or preservation.

## v4.1 development evaluation

The v4.1 fresh synthetic corpus contained 800 records in 20 families. All 12 fixed runs were completed before the holdout was opened. The old pooled-vector decoder produced zero accepted-reference matches across the 2,592 generated outputs, zero semantic preservation passes, action fidelity below the frozen thresholds, and unreliable Vietnamese Unicode. These results motivated a model iteration; v4.1's opened holdout was not reused for tuning.

## v4.2 cross-attention evaluation

The full aggregate report is preserved in [VI_EN_RESULTS_V4.2.md](VI_EN_RESULTS_V4.2.md). It records the 12-run table and per-language/action buckets: 0/2,592 accepted-reference matches, 0 preservation passes, and 2,592/2,592 valid Unicode and EOS-terminated outputs. The frozen gate failed.

## v4.7 validation

The v4.7 validation report is preserved in [VI_EN_RESULTS_V4.7_VALIDATION.md](VI_EN_RESULTS_V4.7_VALIDATION.md). The frozen quality gate failed because several single-action preservation buckets were below 90%. The test set was not opened to tune the version.

## Latest experiment status

v4.8 uses a new AI-reviewed synthetic corpus and a new sealed release holdout. Training is paused partway through; no v4.8 validation or release evaluation has been run. Earlier v4.2 aggregate results remain in [VI_EN_RESULTS.md](VI_EN_RESULTS.md), and that version failed its preregistered generation quality gate. Do not retune against an opened holdout.
