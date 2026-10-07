# Research bottlenecks and acceleration — 2026-10-07

The immediate bottlenecks are unreliable measurement and repeated full training matrices before checking whether the existing model can solve its own training examples. The working checker and launch workflow are repaired. Model quality and the scientific contribution remain unresolved.

All evidence below is preliminary AI-authored/AI-reviewed English–Vietnamese synthetic evidence, not human or native-speaker validation. PhoMT was not used. Phan Rang Cham remains deferred pending dataset-use permission and language review.

## What is blocking progress

| Problem | Evidence | Action taken or next decision |
|---|---|---|
| Quality varies substantially across seeds | Latest completed v4.29 passes only 1/6 full configuration gates and 37/60 buckets. English single-action preservation is 83.2% at language-balance weight 0 and 76.4% at weight 1. | Keep per-seed, per-language/action reporting. Prioritize predicate and patient errors; do not accept pooled improvements that hide regressions. |
| Low byte loss conceals sentence failures, including on train | New checkpoint diagnostic scores the same 128 train singles per checkpoint, balanced across eight language/action buckets, from 79 distinct groups. Several English configurations are only 84–89% exact despite >99.6% teacher-forced byte accuracy. | Use checkpoint diagnostics before another training matrix. The failure is not purely unseen-combination generalization. |
| v4.30's frozen checker is too permissive about Vietnamese progressive forms | All 7,168 train single-action references pass, but deleting `đang` from 1,792 present-progressive references also passes. A positive-reference coverage check alone misses this defect. | Repaired the working checker. It now rejects all 1,792 corruptions and accepts all 7,168 intact references. Added regression tests and a mandatory negative-control preflight for scoped review-bundle matrices. |
| Hypothesis exploration is expensive | v4.29 records about 35 train minutes/run, about 210 minutes summed across six logs, excluding generation. Runs were concurrent: this sum is not elapsed suite time or measured CPU process time. | The new six-checkpoint diagnostic takes about two minutes on this host, without training. This is a cheaper way to answer mechanism questions, not a measured training-speed improvement. |
| Measurement and code drift complicate reproduction | Protocols bind exact source/runtime identities. Repairs to working code must not silently replace old frozen evaluators. | Training launches and workers now load the verified source snapshot. Frozen inference/evaluation remains available through `scripts/run_frozen.py`. Mixed cached packages are rejected. |
| Evidence is still narrow | Recent matrices compare TIDE variants, not a decisive matched baseline study; no human/natural-corpus evidence establishes TIDE benefit. Earlier v4.27/28 were retired after holdout exposure during review. | Restore a token-only control after a mechanism survives screening. Continue using filtered review bundles. Keep natural-language review and Cham permissions as explicit external dependencies. |

## What the new checkpoint probe establishes

The [aggregate checkpoint report](audits/2026-10-07/TRAIN_CHECKPOINT_V4.29.md) and [JSON evidence](audits/2026-10-07/train_checkpoint_v4.29.json) bind the protocol, checkpoints, sample, and diagnostic source hash. Selection uses hashes and a fixed seed before model loading, with one transition per group per language/action bucket. Conditions share the exact sample; language/action buckets still share groups and are not independent linguistic observations.

Examples of aggregate results, each based on 64 train singles per language:

| Condition | Language | Teacher-forced exact | Greedy preservation | Teacher-forced byte errors | Greedy byte edit rate, including EOS |
|---|---|---:|---:|---:|---:|
| balance 0, seed 17 | en | 63/64 | 63/64 | 0.027% | 0.109% |
| balance 0, seed 23 | en | 55/64 | 55/64 | 0.246% | 1.751% |
| balance 0, seed 41 | en | 57/64 | 57/64 | 0.219% | 0.985% |
| balance 1, seed 17 | en | 54/64 | 56/64 | 0.301% | 2.024% |
| balance 1, seed 41 | vi | 37/64 | 43/64 | 0.709% | 7.967% |

Wrong-source, wrong-action, and zero-latent controls increase reference NLL in every language/configuration tested. These models use conditioning signals on this sample; completely ignoring the action is not a sufficient explanation. Zeroing a latent is an out-of-distribution intervention, not an ablation proving benefit from JEPA training.

Teacher forcing supplies the correct reference prefix. Exactness is measured against one reference, so valid alternative wording can fail it. Teacher-forced and greedy exactness are expected to agree under the same argmax policy because they share the first error. The larger free-generation edit rate is a useful error-magnitude diagnostic; it does not establish exposure bias as the cause. Scheduled sampling is therefore a hypothesis to test, not a default fix. Its theoretical limitations and empirical tradeoffs are discussed in [Huszár, 2015](https://arxiv.org/abs/1511.05101) and [Korakakis and Vlachos, 2022](https://aclanthology.org/2022.findings-emnlp.536/); those papers do not diagnose this repository.

## Repairs and evidence boundaries

- `tide_jepa/pilot.py` checks v4.30's Vietnamese progressive forms correctly, with compatibility for earlier frozen annotation schemas.
- Newly authored frames declare `predicate_vi_present`. The checker consumes that declaration instead of depending only on a manually extended version-prefix list. Previously reviewed artifacts are not rewritten; new annotations require new review/freeze identities.
- `scripts/audit_research_checker.py` verifies a protocol-bound review bundle, checks intact train references, and deletes agents, patients, places, and progressive markers or swaps time markers. It emits counts and hashes only and exits nonzero on defects.
- `scripts/train_vi_en_parallel.py` runs that audit before creating the worker pool for `train-validation-only` protocols. Both parent and workers load verified frozen source. A real v4.30 preflight was confirmed to block before worker launch.
- `scripts/diagnose_train_checkpoint.py` compares teacher-forced prediction, greedy generation, and conditioning controls using completed fixed-final-epoch checkpoints. It verifies bundle hashes, rejects test groups/unreferenced frames, scores train singles only, and emits aggregates.
- Existing preservation and action-sensitivity diagnostics now use the verified review bundle for scoped protocols, without opening the full corpus or holdout frame catalog. Legacy protocols retain their historical input paths.

The existing v4.30 workers were already running and all six original run identities were recorded before the working checker changed. Their frozen implementation snapshots, protocols, checkpoints, and datasets were not rebound. All six runs later completed at epoch 29; identity and checkpoint checks passed. Their training remains descriptive evidence, but the frozen checker defect limits any quality conclusion. The repaired checker is a different evaluator: post-hoc scores must not overwrite frozen metrics or authorize opening the release holdout. A corrected confirmatory study needs a fresh reviewed protocol. The new parallel-launch preflight intentionally rejects relaunching the defective frozen v4.30 matrix.

## Shorter research loop

1. **Measurement first.** After freezing a candidate protocol, audit its exact frozen checker before spending a training budget. Require both intact-reference coverage and rejection of deliberate semantic corruptions.
2. **Reuse approved train evidence for engineering probes.** Inspect saved checkpoints with the fixed balanced sample before making another corpus version. Use per-action and per-role metrics, not only mean byte CE or distinct-output rates.
3. **Bound candidate screening.** For a new optimization/decoder mechanism, compare at most two candidates on a fixed train-only diagnostic with a small declared update budget, then repeat the promising candidate on a second seed. Label all such probes as training diagnostics. Stop and revise the mechanism if gains do not reproduce; do not use frozen validation or release holdouts for this screening.
4. **Confirm once there is a mechanism.** Freeze one fresh reviewed study with unchanged quality thresholds, full seeds, and a token-only baseline sharing architecture, data, supervision, and an explicit compute policy. Report extra pointer/self-feeding compute; equal epochs alone are not equal FLOPs.
5. **Develop external evidence separately.** Obtain approved natural Vi–En action annotations and human language review before claims about natural language or low-resource benefit. Translation pairs alone are not action labels. Cham training/evaluation remains deferred.

These steps set a research workflow; they do not retroactively change a frozen gate or establish an improved model.

## Reproduce without emitting text

```sh
# Audit the exact checker that the frozen study would use.
.venv/bin/python -B scripts/audit_research_checker.py data/pilot/vi-en-ai-v4.29 --output /tmp/checker-v429.json

# This exits 1: the historical v4.30 checker misses progressive deletions.
.venv/bin/python -B scripts/audit_research_checker.py data/pilot/vi-en-ai-v4.30 --output /tmp/checker-v430-frozen.json

# Verify the working repair against the same approved train references.
.venv/bin/python -B scripts/audit_research_checker.py data/pilot/vi-en-ai-v4.30 --implementation workspace --output /tmp/checker-v430-repaired.json

# No training; default fixed sample is 16 examples per language/action bucket.
.venv/bin/python -B scripts/diagnose_train_checkpoint.py data/pilot/vi-en-ai-v4.29 --output /tmp/train-checkpoint.json --markdown /tmp/train-checkpoint.md

# Example frozen validation-only evaluation after a completed run.
# Preserve its original metrics and disclose the v4.30 checker limitation.
.venv/bin/python -B scripts/run_frozen.py data/pilot/vi-en-ai-v4.30 pilot evaluate data/pilot/vi-en-ai-v4.30 --evaluation-split validation
```

Checker evidence: [v4.29 frozen pass](audits/2026-10-07/checker_v4.29_frozen.json), [v4.30 frozen failure](audits/2026-10-07/checker_v4.30_frozen.json), [working repair pass](audits/2026-10-07/checker_v4.30_repaired.json). Reports contain aggregate counts only; source/reference/generated rows stay private under Git-ignored data/run paths.

Final engineering verification: **140 CPU tests passed, zero skips**. The six-checkpoint probe completed twice with the same fixed sample and aggregate results: 105.350 seconds in the recorded run and 77.165 seconds in the 2026-10-08 rerun. See the [validation record](audits/2026-10-07/RESEARCH_VALIDATION.md) for safety-boundary tests, actual probes, and limits.
