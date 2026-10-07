# v4.25 status: self-feeding validation failed

**Decision:** diagnostic research checkpoint only. Do not present any v4.25 checkpoint as usable language output. The frozen validation gate failed, so the 3,200-record release holdout remains sealed and no release-split evaluation or generation was run.

The pilot is AI-authored and independently AI-reviewed synthetic English–Vietnamese data. It is preliminary and not human/native-speaker validated (`human_validated=false`). PhoMT was not used. Phan Rang Cham remains excluded pending data-use permission and language/community review.

## Experiment and result

v4.25 tested whether one-pass self-feeding at rate 0.2 improves autoregressive preservation compared with teacher forcing at rate 0. The 6-run TIDE design used seeds 17/23/41 per condition, width 64, 4 heads, 2 layers, 29 fixed-final epochs, and 3,248 updates per run. Each run finished; post-training checks confirmed config/protocol identity, final checkpoint identity, matching `latest.pt` and `best.pt` weights, and exactly one train and validation metric row per epoch. No test artifacts exist.

The frozen gate requires 100% Unicode and checker coverage, at least 90% action fidelity and preservation in every single-action seed/language bucket, and at least 80% for every path bucket. The gate failed: **3/6 configs and 44/60 seed-by-bucket checks passed**. Full details, denominators, final teacher-forced loss, free-generation metrics, and per-seed reasons are in the [validation report](VI_EN_RESULTS_V4.25_VALIDATION.md).

EOS termination and valid Unicode were 100% in all validation buckets. The final train/validation token cross-entropies are teacher-forced metrics and cannot substitute for autoregressive generation. Self-feeding 0.2 did not consistently improve free-generation preservation; its results varied by seed, and it cost more wall time because the proposal pass is additional computation. This narrow experiment does not establish a causal diagnosis of earlier failures. The validation set has no OOD/unsupported prompt cases; refusal quality was not measured. Max-length truncation was not separately counted, though EOS was reached on every scored example.

Two post-hoc aggregate-only analyses are available: [role/component preservation](VI_EN_RESULTS_V4.25_DIAGNOSTIC.md) and [same-source action sensitivity](VI_EN_RESULTS_V4.25_ACTION_SENSITIVITY.md). Every one of the six models changed its output for 640/640 paired source/action comparisons in each language. This verifies action-conditioned variation, not semantic correctness. Component analysis separates self-feeding conditions and is diagnostic, not frozen gate evidence.

## Provenance and integrity

- Draft corpus SHA-256: `71ba206be5b800e067363bd3b574128aba4fd69f3477d7c6b6833c0f4e04ea0a`
- Frozen protocol SHA-256: `6604805a86221a4958da9ea38ac0e845da99a3524f5cb802bfbb243e65c243b6`
- The corpus contains 15,360 records in 192 event combinations, partitioned by event group as 112/40/40 groups and 8,960/3,200/3,200 records. Held-out groups recombine familiar factors; the experiment does not establish template or domain generalization.
- Review artifacts bind two independent Luna high reviews to the exact draft and five reviewed artifacts. Both approved; there are no pending review findings. AI review is not human validation.
- Corpus, review, protocol, split, generation, and checkpoint artifacts remain in Git-ignored `data/` and `runs/`. This report contains aggregate metrics only.

## Reproduction and next gate

On the verified Linux CPU environment, reproduce the frozen validation report and post-hoc aggregate diagnostics without displaying examples:

```sh
.venv/bin/python -B -m tide_jepa.pilot evaluate data/pilot/vi-en-ai-v4.25 --evaluation-split validation
.venv/bin/python -B scripts/summarize_vi_en_validation.py data/pilot/vi-en-ai-v4.25 VI_EN_RESULTS_V4.25_VALIDATION.md
.venv/bin/python -B scripts/diagnose_validation_preservation.py data/pilot/vi-en-ai-v4.25 --markdown VI_EN_RESULTS_V4.25_DIAGNOSTIC.md
.venv/bin/python -B scripts/diagnose_validation_action_sensitivity.py data/pilot/vi-en-ai-v4.25 --markdown VI_EN_RESULTS_V4.25_ACTION_SENSITIVITY.md
```

Do not open the release holdout. Any next model experiment requires a fresh version with new corpus/review/adjudication/protocol/holdout identities, a hypothesis informed by the current aggregate evidence, and unchanged frozen quality thresholds. No checkpoint currently meets the declared output contract.
