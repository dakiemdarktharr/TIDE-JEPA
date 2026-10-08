# TIDE-JEPA preliminary English–Vietnamese pilot

v4.33 is the latest synthetic AI-reviewed pilot. All six 58-epoch runs completed; the corrected narrow checker gives 3/3 TIDE seeds passing validation and all 30/30 TIDE release-test buckets. The first validation report exposed a missing checker registration for the new event family; that report is retained and cached generations were rescored without regeneration. A hash-bound amendment preserves the original protocol and checkpoint identities. These results do not establish TIDE benefit: token-only controls are similar. Two independent Luna reviewers assessed 48 stratified validation outputs: 47/48 were acceptable for naturalness, 48/48 passed meaning/action checks, and both noted one minor spelling issue. This is preliminary AI evidence, not human/native-speaker validation. The stock UI example was out of corpus and corrupted; the runner now uses an approved train-only example. Keep the checkpoint diagnostic-only pending semantic OOD and human review. See [v4.33 status](VI_EN_RESULTS_V4.33_STATUS.md), [release aggregates](audits/2026-10-08/v433_release_holdout_aggregate.json), [AI review summary](audits/2026-10-08/v433_validation_ai_linguistic_review.md), and [demo smoke](audits/2026-10-08/v433_demo_smoke.json).

v4.27 and v4.28 remain retired after review exposed holdout content/annotations; their artifacts are preserved as incident evidence. v4.33 used a fresh split and an isolated train/validation-only review bundle. Validation and release-holdout outputs are synthetic, AI-reviewed preliminary evidence, not human/native-speaker validation. PhoMT was not used; Phan Rang Cham remains deferred pending data-use permission and language/community review. Semantic OOD detection remains unverified.

Linux verification uses Python 3.11.17 and PyTorch 2.14.0+cpu. The current project environment previously passed 150 tests; four new review-summarizer tests then passed individually, and the refreshed pinned-lock source-only snapshot passed the full 154-test suite with zero skips, `compileall`, and `pip check` in a newly created virtualenv. The 219-source-file snapshot includes the diagnostic benchmark, boundary-smoke, human-review aggregation scripts, and regression test; it excludes `.git`, `.venv`, `data/`, and `runs/`. See the [2026-10-09 final reproduction report](audits/2026-10-09/linux-source-only-final-reproduction.json). Training-run split-manifest, JSON, CSV, and checkpoint publication fsyncs file data before rename and the parent directory after rename on POSIX. Hard-process-exit tests verify safe restart before initial metrics publication, recovery after durable metrics/checkpoint publication, and cleanup of synced temp files left before rename. The original v4.33 training identity is retained in the frozen snapshot. Release evaluation used the separate, hash-bound v2 amendment described in the [v4.33 status](VI_EN_RESULTS_V4.33_STATUS.md).

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

The previously frozen version `data/pilot/vi-en-ai-v4.8` had 7,680 AI-authored synthetic records in 192 combinations and 112/40/40 train/validation/release-holdout groups. Two independent AI reviews and an AI adjudication were recorded for preliminary use; this is not human or native-speaker validation. The frozen protocol specified four controls, seeds 17/23/41, 58 epochs, width 48, four heads, two layers, max length 192, batch 80, learning rate 0.001 and source-copy weight 0.5. The directories are now confirmed present on lattice; seven frozen corpus/protocol/approval hashes and eight recorded `latest.pt` hashes match the handoff status. Do not resume: the frozen Python 3.11.9/Windows runtime differs from lattice Python 3.11.17/Arch Linux, and the runner enforces runtime identity.

At the user's request, the training runner and workers were stopped after seed 17 completed all four controls and seed 23 partially trained four controls. Seed 41 did not start. No suite report or evaluation exists for v4.8; its release holdout remains sealed. The data and checkpoint files are Git-ignored and were not pushed. See the [aggregate-only v4.8 status and local checkpoint hashes](VI_EN_RESULTS_V4.8_STATUS.md).

### Historical frozen v4.2

### Historical completed v4.2; development holdout already opened

The v4.2 study used `data/pilot/vi-en-ai-v4.2`: 1,280 AI-authored synthetic records across 32 event families, with 20/6/6 families and records split as 800/240/240 train/validation/release holdout. Its 28 abstract templates are shared across partitions. Two independent AI reviewers approved the draft for preliminary use; this is not human or native-speaker validation. The held-out set was evaluated once after all training completed. It produced 0/2,592 accepted-reference matches and 0 preservation passes; all outputs were valid Unicode and EOS-terminated. The frozen quality gate failed. Do not tune against that opened holdout.

Four controls and seeds 17, 23 and 41 were frozen for 80 epochs / 800 updates per run, width 48, four heads, two layers, max length 192, batch 80 and learning rate 0.001. Checkpoints were selected on validation token and path token CE. The decoder uses source-memory cross-attention and UTF-8-constrained greedy decoding; both are part of this version's implementation/protocol identity. The narrow synthetic checker reports action fidelity and state preservation, but does not evaluate natural language. See `protocol.json` and `suite_report.json` in the ignored v4.2 data directory for frozen aggregate evidence.

### Historical v4.1

The original AI-authored corpus has 20 predicate/event families, four explicit time/polarity states per event, and 400 single-action records including two-step path edges. It contains no PhoMT text. Two separate Luna/high reviewers checked the actual draft independently. Their first-round disagreement led to a correction of object specificity; both approved the corrected draft. The root agent adjudicated the issue. These are AI judgments, not human/native-speaker validation.

The fixed partitions contain 240 train, 80 validation and 80 test records (12/4/4 event families). English and Vietnamese realizations, variants and intermediate path states share a group. Frame reuse and normalized exact-text reuse across splits are rejected. Sentence patterns are shared across partitions, so this tests held-out event/predicate families; it does **not** demonstrate template or domain generalization. Near-duplicate/semantic leakage beyond these declared frames and families remains a review limitation.

Training and validation paths apply `POLARITY=NEGATIVE` followed by `TIME=PAST`; the test paths apply the held-out reverse order. All constituent single actions occur in training. This is a narrow synthetic composition probe.

Historical PhoMT intake recorded an archive at `data/raw/phomt/PhoMT.zip`, verified against the supplied SHA-256, and selected 160 pending private source packets using a text-only training-file sampler. On 2026-10-08 the archive was restored and reverified; a CRC check passed and 160 private training-only source packets were recreated at `data/pilot/vi-en-ai-phomt-source-v1`. They remain pending with no action labels, approved transitions, training, or evaluation. No dev/test member was opened, and no archive content was extracted, unpickled, or executed. See [ROADMAP](ROADMAP.md) and the current [availability audit](audits/2026-10-08/phomt_current_availability.json).

## Historical v4.1 comparison

The four modes are `token_only`, `generic_jepa`, `static_alignment`, and `tide`; the seeds are 17, 23 and 41. Every mode uses the same fixed corpus, action inventory, explicit alignments, split, 259-token byte vocabulary, width 32, four heads, one layer, maximum length 192, batch size 80, learning rate 0.001 and 40 epochs. This gives 120 updates per run.

Checkpoints are selected by validation single-edge token loss plus path token loss for all modes. All training runs complete before test scoring. Configurations, approvals, corpus, split, inventory, alignments and implementation files are fingerprinted. Epoch-boundary resume restores Python/Torch RNG; a regression test checks identical final tensors against an uninterrupted run. Existing results are protected from an accidental fresh-run overwrite.

Equal examples, updates and architecture do not imply equal FLOPs. The runs log tokens, updates and wall time; no matched-compute efficacy claim is made. Automated scores include token/path cross-entropy, single-reference exact match, character error and UTF-8 validity. They do not measure action fidelity, meaning preservation or naturalness. Test results must not be used to rewrite the benchmark or tune these runs.

## Local commands

On lattice (Arch Linux x86_64, Python 3.11.17, PyTorch 2.14.0+cpu, CPU-only), the refreshed source-only snapshot passed 154 tests with no skips; `compileall`, `pip check`, and `git diff --check` passed in the corresponding checks. A 48-output preliminary AI spot check found one spelling issue and no sampled meaning/action failures; human/native-speaker review remains open. Two independent human-review forms are prepared under Git-ignored `data/pilot/vi-en-ai-v4.33/human-review/`; [the summarizer](scripts/summarize_v433_human_review.py) produces agreement and subgroup aggregates only, and has been tested with synthetic dummy ratings. v4.33 passed its narrow corrected validation/release gates. The original stock demo example was outside the corpus and produced semantic corruption; the current train-only default passed the narrow checker, but the checkpoint remains diagnostic-only because broad OOD and human quality are unverified. A separate 4-client/80-request benchmark repeated twice confirmed that one inference is served at a time and overlapping calls receive schema-valid 503 busy responses; repeat RSS rose 112 KiB after initial warm-up. A separate varied-train run used 40 requests per pass from 64 approved candidates balanced across English/Vietnamese and single actions/two-action paths; both passes returned 40/40 HTTP 200 and passed the narrow checker in all four language/task cells (10/10 each); RSS was unchanged on the repeat. The aggregate reports contain no text. This remains synthetic train-only evidence, not natural-corpus or production-capacity validation. The test report is aggregate-only; PhoMT was not used. Current audit boundaries are in [repair closure](audits/2026-10-02/REPAIR_CLOSURE.md), [v4.33 status](VI_EN_RESULTS_V4.33_STATUS.md), and [research acceleration](RESEARCH_ACCELERATION.md).

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
.venv/bin/python -B scripts/run_v433_demo.py --port 8765
```

Then open `http://127.0.0.1:8765`. The v4.33 runner verifies the amendment, review evidence, runtime, config and checkpoint identity; it binds only to loopback, makes no cloud/model API calls, and does not log user input or generated text. The page shows `diagnostic_only`, `human_validated=false`, and the corrected validation gate. Use the same source and target language; cross-language requests are rejected. The original stock-page example was out of corpus and produced semantic corruption; the current train-only default passes the narrow checker. A 19-case boundary smoke verifies exact allowlist refusals and HTTP limits, but the demo does not detect semantic OOD generally. The checkpoint is not approved for natural-language or translation use. Stop the server with Ctrl-C.

With the v4.33 demo running, reproduce the aggregate-only request-boundary smoke and bounded runtime/RSS benchmark using new output paths:

```sh
.venv/bin/python -B scripts/smoke_v433_demo_boundaries.py --port 8765 --output /tmp/v433-demo-boundary-recheck.json
.venv/bin/python -B scripts/benchmark_v433_demo_runtime.py --port 8765 --requests 240 --output /tmp/v433-demo-runtime-recheck.json
```

The current reports are [boundary smoke](audits/2026-10-08/v433_demo_boundary_smoke.json), [runtime benchmark 1](audits/2026-10-08/v433_demo_runtime_benchmark_3.json), and [runtime benchmark 2](audits/2026-10-08/v433_demo_runtime_benchmark_4.json). They contain aggregate statuses and resource metrics only, not source or generated text.

## Remaining scientific gates

- Curate and review PhoMT-derived within-language actions privately, with evidence per example and explicit alignment licenses. Keep the author's research/education, no-redistribution, citation and non-commercial-weight requirements.
- Obtain human bilingual evaluation, accepted variants, agreement/adjudication and independently authored held-out examples.
- Improve learning/generation under a new preregistered protocol; preserve the present negative pilot results.
- Measure compute and broaden seeds/data before making comparative efficacy claims.
- Keep Cham deferred; an English–Vietnamese pilot does not imply Cham coverage or rights.

Local review records guard workflow drift. They are not cryptographic proof of reviewer identity or independence; the separate Luna dispatches and user authorization are recorded in the project evidence. A workspace owner can modify local files and approval assertions.
