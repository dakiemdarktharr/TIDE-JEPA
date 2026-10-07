# v4.26 status: low-dose source-copy validation failed

**Decision:** diagnostic research checkpoint only. No v4.26 checkpoint is approved for usable language output. The frozen validation gate failed, so the 3,200-record release holdout remains sealed; no release-split evaluation or generation was run.

This is a preliminary AI-authored and independently AI-reviewed synthetic pilot. It is not human/native-speaker validated (`human_validated=false`). PhoMT was not used. Phan Rang Cham remains excluded.

## Experiment and result

v4.26 tested whether a low source-copy auxiliary weight (0.25) improves free-generation role preservation relative to weight 0. Both conditions computed the source-copy term, with three seeds per condition. Six fixed-final TIDE runs completed 29 epochs / 3,248 updates each. After training stopped, checks confirmed protocol/config/runtime identity, matching `latest.pt` and `best.pt` tensors, and exactly 58 train/validation rows per config. A pair of overlapping intermediate seed-41 outputs was quarantined and excluded; those two configs were rerun/resumed without overlap, and the accepted final artifacts passed all integrity checks. No test artifacts were created.

The unchanged frozen gate requires 100% Unicode and checker coverage, at least 90% action fidelity and preservation in every single-action seed/language bucket, and at least 80% for every path bucket. The gate failed: **1/6 configs passed all checks and 32/60 seed-by-bucket checks passed**. Unicode, EOS and checker coverage were 100% throughout. The full aggregate report includes per-seed denominators and exact frozen gate results: [validation report](VI_EN_RESULTS_V4.26_VALIDATION.md).

Teacher-forced token CE was low but did not predict reliable free generation. The post-hoc component diagnostic found English single-action preservation at 79.5% for copy weight 0 and 68.8% for 0.25; English patient retention was 85.3% and 79.1%, respectively. Vietnamese single-action preservation was 89.3% and 93.7%. Thus 0.25 helped Vietnamese aggregate preservation while materially worsening English; this is a diagnostic result, not a causal proof. Same-source action sensitivity was 640/640 pairs in both languages for every run, which demonstrates output variation but not semantic correctness. See [role/component diagnostic](VI_EN_RESULTS_V4.26_DIAGNOSTIC.md) and [action sensitivity](VI_EN_RESULTS_V4.26_ACTION_SENSITIVITY.md).

The checker only covers the declared synthetic grammar. Validation had no OOD/unsupported requests, refusal quality was not measured, and max-length truncation was not separately counted. The offline demo remains diagnostic only; no checkpoint meets the declared output contract.

## Provenance and integrity

- Draft corpus SHA-256: `002451243da0095255c5353f935f85711fb062df1741682b1a2a096872371868`
- Frozen protocol SHA-256: `b8d2c78cc0de9f833d05eb2ea200f82b0b614839390695ad3fe281d6a7105dd2`
- The corpus contains 15,360 records in 192 event combinations; split groups are 112/40/40 and records are 8,960/3,200/3,200. The release holdout is sealed.
- Two independent Luna/high AI reviews and adjudication bind to the exact frozen corpus and reviewed artifacts. This is AI review, not human validation.
- The report contains aggregate-only metrics. Corpus, reviewer artifacts, protocol, validation generations and weights remain in Git-ignored `data/` and `runs/`.

## Reproduction and next gate

On the verified Linux CPU environment, reproduce the validation report and post-hoc aggregate diagnostics without displaying examples:

```sh
.venv/bin/python -B -m tide_jepa.pilot evaluate data/pilot/vi-en-ai-v4.26 --evaluation-split validation
.venv/bin/python -B scripts/summarize_vi_en_validation.py data/pilot/vi-en-ai-v4.26 VI_EN_RESULTS_V4.26_VALIDATION.md
.venv/bin/python -B scripts/diagnose_validation_preservation.py data/pilot/vi-en-ai-v4.26 --markdown VI_EN_RESULTS_V4.26_DIAGNOSTIC.md
.venv/bin/python -B scripts/diagnose_validation_action_sensitivity.py data/pilot/vi-en-ai-v4.26 --markdown VI_EN_RESULTS_V4.26_ACTION_SENSITIVITY.md
```

Do not open the release holdout. A follow-up model experiment requires a fresh version with new corpus/review/adjudication/protocol/holdout identities, a hypothesis that addresses English entity/patient retention without sacrificing Vietnamese quality, and the same frozen thresholds. No checkpoint currently meets the output contract.
