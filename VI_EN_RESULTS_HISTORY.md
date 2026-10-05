# Historical preliminary Vi–En pilot results

This file preserves earlier AI-authored/AI-reviewed synthetic pilot results. All results are preliminary; none were human/native-speaker validated. PhoMT was not used for model training, and Phan Rang Cham remains excluded. Current v4.18 completed 12 runs and validation-only evaluation. Every primary condition × seed × bucket failed: action fidelity and preservation were 0%, while Unicode/EOS were 100%. The fresh release holdout remains sealed. See [v4.18 status](VI_EN_RESULTS_V4.18_STATUS.md) and [aggregate report](VI_EN_RESULTS_V4.18_VALIDATION.md). v4.17-r2 also failed all 60 primary checks; see its [status](VI_EN_RESULTS_V4.17_STATUS.md) and [report](VI_EN_RESULTS_V4.17_VALIDATION.md). v4.16-r2 and earlier outcomes remain preserved below. v4.15 also failed and remains sealed; see its [status](VI_EN_RESULTS_V4.15_STATUS.md) and [report](VI_EN_RESULTS_V4.15_VALIDATION.md). v4.13 also failed both TIDE conditions and kept its holdout sealed; see the [status](VI_EN_RESULTS_V4.13_STATUS.md) and [aggregate report](VI_EN_RESULTS_V4.13_VALIDATION.md). v4.12, v4.10 and v4.11 validation failures remain preserved in their respective status and validation records; all holdouts remain sealed. The v4.8 training pause is summarized in [VI_EN_RESULTS_V4.8_STATUS.md](VI_EN_RESULTS_V4.8_STATUS.md); it has no evaluation result.

Linux code-path revalidation on 2026-10-03 passed 77 CPU tests, compile and dependency checks, plus synthetic crash/identity probes. The checks do not establish model quality. The v4.8 private artifacts are absent from lattice; see the dated [Linux report](audits/2026-10-03/LINUX_REVALIDATION.md). All earlier model-quality outcomes below remain unchanged.

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
