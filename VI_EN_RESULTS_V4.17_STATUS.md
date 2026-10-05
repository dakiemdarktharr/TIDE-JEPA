# v4.17-r2 status — validation gate failed

The v4.17-r2 AI-authored, independently AI-reviewed synthetic pilot completed all 12 frozen CPU runs and validation-only generation. The frozen TIDE gate failed all **60/60** seed × transition-balance × language/task bucket checks. The release holdout was not evaluated and remains sealed. Results are preliminary and not human/native-speaker validated.

## Frozen experiment and run evidence

- Corpus: 15,360 records in 192 event combinations; 112/40/40 train/validation/release-holdout groups and 8,960/3,200/3,200 records. Two independent Luna high reviews approved the exact r2 draft; `human_validated=false`.
- Protocol SHA-256: `9aaca397ce2b7ec8e16419ad9d19fdf46fed4d2fc04ef1e59d86ac61ddbb35a6`.
- Twelve runs crossed `token_only` and `tide` (TIDE auxiliary multiplier 0.1) with `row_uniform` and `unique_transition`, using source-copy weight 1.5 and seeds 17/23/41. Each run completed 29 epochs and 3,248 updates. The verified run audit found matching protocol/config/runtime/checkpoint identities, 29 train and 29 validation metric rows, and 112 updates per epoch for each run.
- `unique_transition` assigns half weight to standalone and path-linked copies in base per-edge losses; path-composition losses remain unchanged.
- Training/validation paths apply negative polarity then past time. The sealed test paths reverse the order, so the holdout would additionally probe action-order recombination and is not a matched estimate of the weighting contrast.

## Validation findings

All 60 primary checks failed the frozen thresholds (Unicode 100%; single-action fidelity and preservation each ≥90%; held-out-path fidelity and preservation each ≥80%). All validation outputs were valid Unicode and EOS-terminated, but these checks do not establish semantic correctness.

Pooled TIDE results show heterogeneous action fidelity and very weak preservation. With row-uniform weighting, action fidelity was 40.45% overall and preservation 1.44%; with unique-transition weighting, action fidelity was 40.67% and preservation 1.12%. Unique weighting improved Vietnamese single-action fidelity modestly while lowering English single-action fidelity; preservation fell in all four pooled language/task categories. These are descriptive outcomes on this synthetic corpus and three seeds; they do not establish cause, natural-text quality, or a TIDE advantage. The reversed-order path split also limits path comparisons.

The aggregate report now prints the numeric frozen thresholds and per-check failure reasons so readers can audit the reported gate. It contains aggregate counts only; no examples or generated/reference strings. See [validation report](VI_EN_RESULTS_V4.17_VALIDATION.md).

## Reproduction and boundaries

The private corpus, review records, protocol, generation metrics, and checkpoints remain in Git-ignored `data/` and `runs/`. PhoMT raw or derived rows and Phan Rang Cham data were not used. Do not open this holdout for tuning. Any follow-up must use a new reviewed corpus and fresh sealed split. A fresh v4.18 factorial draft subsequently passed two independent Luna reviews and was frozen; its 12-run CPU training is underway. See [v4.18 status](VI_EN_RESULTS_V4.18_STATUS.md).

Verified aggregate regeneration command:

```sh
.venv/bin/python -B scripts/summarize_vi_en_validation.py data/pilot/vi-en-ai-v4.17-r2 VI_EN_RESULTS_V4.17_VALIDATION.md
```

Full training and validation run identities are recorded in the ignored local artifacts. This status file deliberately does not expose private rows, generations, or checkpoint hashes.
