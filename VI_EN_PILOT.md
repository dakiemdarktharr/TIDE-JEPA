# TIDE-JEPA preliminary English–Vietnamese pilot

The user authorized AI authoring and review on 2026-10-01, with human review deferred. The newest completed pilot, v4.18, finished all 12 frozen CPU runs and validation-only generation after two independent Luna approvals. Its frozen evaluator omitted v4.18 event families, giving 0% checker coverage (`0/0` semantic denominators); that gate failed closed and cannot be interpreted as a 0% model score. A post-hoc corrected-checker rescore still missed all thresholds: action fidelity 26.5–52.5% for single actions and 51.0–72.9% for paths, with preservation at 0.4–1.9% and 0.8–8.3%. A train-only overfit reached 8/8 on one seen combination after 600 updates; this demonstrates memorization, not generalization. The fresh release holdout remains sealed. See [v4.18 status](VI_EN_RESULTS_V4.18_STATUS.md), [frozen report](VI_EN_RESULTS_V4.18_VALIDATION.md), [post-hoc rescore](VI_EN_RESULTS_V4.18_RESCORING.md), and [overfit diagnostic](VI_EN_RESULTS_V4.18_OVERFIT_DIAGNOSTIC.md). v4.17-r2 also failed all 60/60 seed × balance × bucket checks; its pooled preservation was 1.44% under row-uniform and 1.12% under unique-transition weighting. See [v4.17 status](VI_EN_RESULTS_V4.17_STATUS.md) and [aggregate report](VI_EN_RESULTS_V4.17_VALIDATION.md). v4.15 also failed; see its [status](VI_EN_RESULTS_V4.15_STATUS.md) and [aggregate report](VI_EN_RESULTS_V4.15_VALIDATION.md). These remain preliminary AI-reviewed synthetic results, not human/native-speaker validation. v4.13 also failed both TIDE conditions; its holdout remains sealed. See [v4.13 status](VI_EN_RESULTS_V4.13_STATUS.md) and [aggregate validation report](VI_EN_RESULTS_V4.13_VALIDATION.md). v4.12, v4.11, v4.10, v4.9 historical status, v4.8 status, [current results](VI_EN_RESULTS.md), and [historical results](VI_EN_RESULTS_HISTORY.md) preserve earlier work. None establishes human-validated language quality or completes the scientific M4 benchmark.

Phan Rang Cham stays out of the pilot until source-use permission and language review are available. New agents/subagents use only `gpt-6-luna` with `high` or `xhigh`, unless the user approves another model; see [AGENTS.md](AGENTS.md).

## Data and review

### Historical completed v4.10

The frozen v4.10 protocol contains 7,680 AI-authored synthetic records in 192 groups (112/40/40 train/validation/release holdout) and uses a factor pool disjoint from v4.9. The schema key for the held-out partition is `test`; test evaluation remains gated until every registered run completes and all primary-seed validation generation gates pass. Two independent Luna reviews approved the exact draft and an AI adjudication recorded their agreement. This is not human or community validation. Training and validation completed; the primary TIDE gate failed, so no release-test scoring was done. See the [aggregate-only v4.10 status](VI_EN_RESULTS_V4.10_STATUS.md) and [validation report](VI_EN_RESULTS_V4.10_VALIDATION.md).

### Completed v4.11; release holdout sealed

The frozen v4.11 pilot contains 7,680 AI-authored synthetic records in 192 groups (112/40/40 train/validation/release holdout), with three new agent factors and a holdout pool disjoint from v4.9/v4.10. Two independent `gpt-6-luna` high reviews approved the exact draft and the artifact-bound adjudication records their agreement. The 12 configurations use seeds 17/23/41, 58 epochs, width 48, four heads, two layers, batch 80, learning rate 0.001, TIDE primary, and preregistered source-copy weight 1.5. All runs completed with identities verified; validation-only evaluation failed for all three TIDE seeds, chiefly on single-action preservation. The release holdout remains unopened and the direct test API refused scoring. The source-copy change did not clear the frozen gate. All data remains under ignored `data/`, and no PhoMT/Cham rows were used. See the [frozen status](VI_EN_RESULTS_V4.11_STATUS.md) and [aggregate report](VI_EN_RESULTS_V4.11_VALIDATION.md).

### Completed v4.12; release holdout sealed

The fresh v4.12 corpus contains 7,680 AI-authored synthetic records in 192 event groups (112/40/40 train/validation/release holdout). Two independent `gpt-6-luna` high reviews approved the exact artifact; their aggregate-only findings and adjudication are bound to the ignored draft and mark the review as preliminary, not human validation. The preregistered comparison was a matched 2×2 ablation: `token_only` and `tide`, each with source-copy weight 0 or 1.5, across seeds 17/23/41. All 12 configurations completed 58 epochs, width 48, four heads, two layers, batch 80 and learning rate 0.001. Validation failed both primary TIDE source-copy conditions across all three seeds, chiefly on Vietnamese single-action preservation; the frozen 90% single-action threshold was not met. Unicode and EOS were 100%, and held-out-path buckets met their lower thresholds. The direct test command was refused by the gate, so the fresh release holdout remains sealed. PhoMT was not used, and Phan Rang Cham remains excluded. See the [aggregate-only results](VI_EN_RESULTS_V4.12_VALIDATION.md). All corpus, review, metric and run artifacts remain Git-ignored under `data/` and `runs/`.

### Completed v4.13; release holdout sealed

The v4.13 pilot used another fresh 7,680-record synthetic corpus, 112/40/40 event groups, and three new agent factors. Two independent `gpt-6-luna` high reviews approved the exact draft; artifact-bound review and adjudication remain under ignored `data/`. The frozen comparison tested `token_only` and `tide` at source-copy weights 1.5 and 3.0 over seeds 17/23/41. All 12 configs completed 58 epochs / 3,248 steps, and checkpoint/runtime/implementation identities matched. Validation failed both TIDE weights overall: 10/60 seed-by-bucket checks passed, including one single-action bucket; 47/48 single-action buckets missed the 90% preservation threshold and 9/12 path buckets met threshold. Unicode/EOS were 100%, but pooled preservation favored token-only at both weights. The direct test command was refused before scoring; no test metrics were created and the fresh holdout remains sealed. See [status](VI_EN_RESULTS_V4.13_STATUS.md) and [aggregate results](VI_EN_RESULTS_V4.13_VALIDATION.md). PhoMT and Phan Rang Cham were excluded.

### v4.14 corrected draft and failed validation result

The first 15,360-record v4.14 draft was not approved because its context adjunct changed with the tense action and was absent from the event frame. It was never frozen or trained. The corrected revision at `data/pilot/vi-en-ai-v4.14-r1/` keeps a single location invariant across all four surface forms and semantic states, and the frame/checker both preserve that location. Two independent `gpt-6-luna` high reviews approved the revised SHA. The frozen design compares `token_only` and TIDE at copy weight 1.5 across three seeds for 29 epochs / 3,248 updates per configuration, holding the existing thresholds fixed. All six runs and validation-only generation completed. TIDE passed only 4/30 per-seed bucket checks; all 24 single-action checks failed, while 4/6 path checks passed. Token-only preservation was higher in all pooled buckets. The holdout remains sealed. Two independent Luna aggregate-only diagnostics recommend preserving the failure and next auditing TIDE loss/gradient contribution before any fresh, preregistered objective-dose experiment. See the [v4.14 aggregate report](VI_EN_RESULTS_V4.14_VALIDATION.md).

### Historical paused v4.8

The previously frozen version `data/pilot/vi-en-ai-v4.8` had 7,680 AI-authored synthetic records in 192 combinations and 112/40/40 train/validation/release-holdout groups. Two independent AI reviews and an AI adjudication were recorded for preliminary use; this is not human or native-speaker validation. The frozen protocol specified four controls, seeds 17/23/41, 58 epochs, width 48, four heads, two layers, max length 192, batch 80, learning rate 0.001 and source-copy weight 0.5. Its data and run directories are absent on lattice; do not claim an exact resume here.

At the user's request, the training runner and workers were stopped after seed 17 completed all four controls and seed 23 partially trained four controls. Seed 41 did not start. No suite report or evaluation exists for v4.8; its release holdout remains sealed. The data and checkpoint files are Git-ignored and were not pushed. See the [aggregate-only v4.8 status and local checkpoint hashes](VI_EN_RESULTS_V4.8_STATUS.md).

### Historical frozen v4.2

The current release candidate is `data/pilot/vi-en-ai-v4.2`: 1,280 AI-authored synthetic records across 32 event families, with 20/6/6 families and records split as 800/240/240 train/validation/release holdout. Its 28 abstract templates are shared across partitions. The two independent AI reviewers approved the draft for preliminary use; this is not human or native-speaker validation. The held-out set was evaluated once after all training completed. It produced 0/2,592 accepted-reference matches and 0 preservation passes; all outputs were valid Unicode and EOS-terminated. The frozen quality gate failed. Do not tune against this opened holdout. Any new experiment needs a new reviewed version and untouched holdout.

Four controls and seeds 17, 23 and 41 were frozen for 80 epochs / 800 updates per run, width 48, four heads, two layers, max length 192, batch 80 and learning rate 0.001. Checkpoints were selected on validation token and path token CE. The decoder uses source-memory cross-attention and UTF-8-constrained greedy decoding; both are part of this version's implementation/protocol identity. The narrow synthetic checker reports action fidelity and state preservation, but does not evaluate natural language. See `protocol.json` and `suite_report.json` in the ignored v4.2 data directory for frozen aggregate evidence.

### Historical v4.1

The original AI-authored corpus has 20 predicate/event families, four explicit time/polarity states per event, and 400 single-action records including two-step path edges. It contains no PhoMT text. Two separate Luna/high reviewers checked the actual draft independently. Their first-round disagreement led to a correction of object specificity; both approved the corrected draft. The root agent adjudicated the issue. These are AI judgments, not human/native-speaker validation.

The fixed partitions contain 240 train, 80 validation and 80 test records (12/4/4 event families). English and Vietnamese realizations, variants and intermediate path states share a group. Frame reuse and normalized exact-text reuse across splits are rejected. Sentence patterns are shared across partitions, so this tests held-out event/predicate families; it does **not** demonstrate template or domain generalization. Near-duplicate/semantic leakage beyond these declared frames and families remains a review limitation.

Training and validation paths apply `POLARITY=NEGATIVE` followed by `TIME=PAST`; the test paths apply the held-out reverse order. All constituent single actions occur in training. This is a narrow synthetic composition probe.

PhoMT is separately present at `data/raw/phomt/PhoMT.zip`, verified against the supplied SHA-256. The metadata audit passes. Source selection streams only the detokenized training files, checks paired line counts and UTF-8, and chooses 160 pending private source packets. It never extracts the whole archive, unpickles, opens official dev/test files, assigns action labels from translation links, or prints source rows. Those source packets are **not** approved training transitions and are not used by this pilot.

## Historical v4.1 comparison

The four modes are `token_only`, `generic_jepa`, `static_alignment`, and `tide`; the seeds are 17, 23 and 41. Every mode uses the same fixed corpus, action inventory, explicit alignments, split, 259-token byte vocabulary, width 32, four heads, one layer, maximum length 192, batch size 80, learning rate 0.001 and 40 epochs. This gives 120 updates per run.

Checkpoints are selected by validation single-edge token loss plus path token loss for all modes. All training runs complete before test scoring. Configurations, approvals, corpus, split, inventory, alignments and implementation files are fingerprinted. Epoch-boundary resume restores Python/Torch RNG; a regression test checks identical final tensors against an uninterrupted run. Existing results are protected from an accidental fresh-run overwrite.

Equal examples, updates and architecture do not imply equal FLOPs. The runs log tokens, updates and wall time; no matched-compute efficacy claim is made. Automated scores include token/path cross-entropy, single-reference exact match, character error and UTF-8 validity. They do not measure action fidelity, meaning preservation or naturalness. Test results must not be used to rewrite the benchmark or tune these runs.

## Local commands

On the current Linux host, the full CPU suite passes 92 tests with 0 skips; compileall and `pip check` pass. The loopback demo tests verify request limits and single-flight inference concurrency. Latest evidence is in [Linux revalidation](audits/2026-10-03/LINUX_REVALIDATION.md). v4.18 completed 12/12 29-epoch runs and validation-only generation, but its frozen evaluator had zero semantic-checker coverage; the gate failed closed, and the holdout remains sealed. The post-hoc corrected-checker diagnostic still misses thresholds, as documented in the [rescore](VI_EN_RESULTS_V4.18_RESCORING.md). v4.17-r2 completed 12/12 29-epoch runs and validation-only generation; all 60 primary checks failed. All prior failed-version holdouts also remain sealed.

For a **new, separately reviewed version**, run from the project root. These are workflow commands, not an assertion that a clean bootstrap or full training run has already been verified. Never overwrite an existing version or reopen its release test for tuning. Bind the two independent AI reviews and adjudication to the exact draft before freezing. Finish all controls/seeds, evaluate generation on validation only, and proceed to release-test scoring only when every primary-seed validation gate passes.

```sh
.venv/bin/python -B -m tide_jepa.pilot_seed data/pilot/vi-en-ai-vX --pilot-version vX
# Obtain and bind two independent AI review records and adjudication for this exact draft.
.venv/bin/python -B -m tide_jepa.pilot freeze data/pilot/vi-en-ai-vX --epochs 58 --model-width 48 --model-heads 4 --model-layers 2 --batch-size 80 --learning-rate 0.001 --primary-mode tide
.venv/bin/python -B scripts/train_vi_en_parallel.py data/pilot/vi-en-ai-vX --workers 4
.venv/bin/python -B -m tide_jepa.pilot evaluate data/pilot/vi-en-ai-vX --evaluation-split validation
# Stop if primary-mode validation misses a frozen threshold; create a new version to iterate.
.venv/bin/python -B -m tide_jepa.pilot run data/pilot/vi-en-ai-vX --resume
.venv/bin/python -B scripts/summarize_vi_en.py data/pilot/vi-en-ai-vX VI_EN_RESULTS.md
```

The private frozen corpus, review records, protocol and reports are under `data/pilot/`. Checkpoints, metric logs, private generated outputs and code snapshots are under `runs/`. Both trees are Git-ignored. They are local artifacts; the project does not publish model weights or dataset material.

To launch the local browser demo, use the exact frozen configuration and `best.pt` from a completed reviewed run:

```sh
.venv/bin/python -B -m tide_jepa.demo data/pilot/vi-en-ai-vX/tide-seed-17.json runs/vi-en-ai-vX/tide-seed-17/best.pt --port 8765
```

Then open `http://127.0.0.1:8765`. The server binds only to loopback, makes no cloud/model API calls, and does not log user input or generated text. It identifies the checkpoint provenance and labels outputs diagnostic until quality is established. Use the same source and target language: translation edges are not supported by this prototype. No checkpoint has passed the frozen quality gate, so no usable demo checkpoint is currently available on this host.

## Remaining scientific gates

- Curate and review PhoMT-derived within-language actions privately, with evidence per example and explicit alignment licenses. Keep the author's research/education, no-redistribution, citation and non-commercial-weight requirements.
- Obtain human bilingual evaluation, accepted variants, agreement/adjudication and independently authored held-out examples.
- Improve learning/generation under a new preregistered protocol; preserve the present negative pilot results.
- Measure compute and broaden seeds/data before making comparative efficacy claims.
- Keep Cham deferred; an English–Vietnamese pilot does not imply Cham coverage or rights.

Local review records guard workflow drift. They are not cryptographic proof of reviewer identity or independence; the separate Luna dispatches and user authorization are recorded in the project evidence. A workspace owner can modify local files and approval assertions.
