# TIDE-JEPA preliminary English–Vietnamese pilot

The user authorized AI authoring and review on 2026-10-01, with human review deferred. The current v4.2 frozen engineering pilot completes controlled synthetic-data authoring, four objective controls, held-out evaluation and offline inference, but its preregistered generation quality gate **failed**. It does not establish language quality or complete the human-validated M4 benchmark. See the [aggregate results](VI_EN_RESULTS.md) and [historical version results](VI_EN_RESULTS_HISTORY.md).

Phan Rang Cham stays out of the pilot until source-use permission and language review are available. New agents/subagents use only `gpt-6-luna` with `high` or `xhigh`, unless the user approves another model; see [AGENTS.md](AGENTS.md).

## Data and review

### Current frozen v4.2

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

Use the existing Python 3.11 runtime and the project venv libraries if its launcher fails:

```powershell
$env:PYTHONPATH = Join-Path (Get-Location) '.venv\Lib\site-packages'
py -3.11 -B -m unittest discover -s tests -v
```

For a **new, separately reviewed version**, from the project root use the following order. These commands describe the protocol workflow; never overwrite an existing version or reopen its release test for tuning. Freeze the data/code identity and primary quality gate before training, finish all controls/seeds, evaluate generation on validation only, and proceed to release-test scoring only after validation/model selection is complete.

```powershell
$env:PYTHONPATH = Join-Path (Get-Location) '.venv\Lib\site-packages'
py -3.11 -B -m tide_jepa.pilot_seed data/pilot/vi-en-ai-vX --pilot-version vX
# Obtain and bind two independent AI review records and adjudication for this exact draft.
py -3.11 -B -m tide_jepa.pilot freeze data/pilot/vi-en-ai-vX --epochs 80 --model-width 48 --model-heads 4 --model-layers 2 --batch-size 80 --learning-rate 0.001 --primary-mode tide
py -3.11 -B scripts/train_vi_en_parallel.py data/pilot/vi-en-ai-vX --workers 4
py -3.11 -B -m tide_jepa.pilot evaluate data/pilot/vi-en-ai-vX --evaluation-split validation
# Stop if primary-mode validation misses a frozen threshold; create a new version to iterate.
py -3.11 -B -m tide_jepa.pilot run data/pilot/vi-en-ai-vX --resume
py -3.11 -B scripts/summarize_vi_en.py data/pilot/vi-en-ai-vX VI_EN_RESULTS.md
```

The private frozen corpus, review records, protocol and reports are under `data/pilot/`. Checkpoints, metric logs, private generated outputs and code snapshots are under `runs/`. Both trees are Git-ignored. They are local artifacts; the project does not publish model weights or dataset material.

To launch the local browser demo:

```powershell
.\scripts\run_vi_en_demo.ps1
```

Open `http://127.0.0.1:8765`. The demo runs on CPU, binds only to loopback, makes no cloud/model API calls, and does not log user input or generated text. It explicitly identifies the checkpoint as an AI-reviewed synthetic pilot. Default model choice is TIDE/seed 17, for demonstrating the project architecture; it is not selected by test performance. Use the same source and target language: translation edges are not supported by this prototype.

## Remaining scientific gates

- Curate and review PhoMT-derived within-language actions privately, with evidence per example and explicit alignment licenses. Keep the author's research/education, no-redistribution, citation and non-commercial-weight requirements.
- Obtain human bilingual evaluation, accepted variants, agreement/adjudication and independently authored held-out examples.
- Improve learning/generation under a new preregistered protocol; preserve the present negative pilot results.
- Measure compute and broaden seeds/data before making comparative efficacy claims.
- Keep Cham deferred; an English–Vietnamese pilot does not imply Cham coverage or rights.

Local review records guard workflow drift. They are not cryptographic proof of reviewer identity or independence; the separate Luna dispatches and user authorization are recorded in the project evidence. A workspace owner can modify local files and approval assertions.
