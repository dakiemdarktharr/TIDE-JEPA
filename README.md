# TIDE-JEPA

From-scratch research prototype for action-conditioned latent transitions and controlled generation in **Vietnamese, English, and Phan Rang Cham**.

Read [the current specification](tide_jepa_spec.md) first. The [project decision ledger](Obsidian/RMIT%20Hackathon/wiki/Project%20Ground%20Truth.md) records user authority. Earlier MATE-JEPA/La Ha proposals are superseded drafts.

Current data-source findings and the PhoMT permission record are in [Dataset Research — 2026-09-30](Obsidian/RMIT%20Hackathon/wiki/Dataset%20Research%20%E2%80%94%202026-09-30.md). PhoMT is conditionally approved for the requested research/education scope; its local archive now passes the supplied SHA-256 and metadata audit. It has not been used for model training.

The user-authorized **preliminary AI-reviewed English–Vietnamese synthetic pilot** has a reproducible training/evaluation workflow and an offline diagnostic demo. v4.19 completed 12 frozen CPU configurations and validation-only generation after all config/data/split/runtime/checkpoint identities passed. The semantic checker covered all 8,640 validation examples; Unicode and EOS were 100%, yet the quality gate failed: 0/12 configurations passed all buckets and only 4/120 seed-by-bucket checks passed, mainly due to preservation failures. Its release holdout remains sealed, with no test generation or scoring. See the [v4.19 status](VI_EN_RESULTS_V4.19_STATUS.md) and [aggregate validation report](VI_EN_RESULTS_V4.19_VALIDATION.md). Earlier v4.18 had zero checker coverage in its frozen evaluator and failed closed; a corrected post-hoc rescore and paired checkpoint diagnostic also remained below thresholds. See [v4.18 status](VI_EN_RESULTS_V4.18_STATUS.md), [rescore](VI_EN_RESULTS_V4.18_RESCORING.md), and [checkpoint sample](VI_EN_RESULTS_V4.18_CHECKPOINT_SAMPLE.md). v4.17-r2 and earlier studies also failed; their holdouts remain sealed. See [v4.17 status](VI_EN_RESULTS_V4.17_STATUS.md), [current results](VI_EN_RESULTS.md), [historical pilot summary](VI_EN_RESULTS_HISTORY.md), [pilot workflow](VI_EN_PILOT.md), and [Linux revalidation report](audits/2026-10-03/LINUX_REVALIDATION.md). The current Linux CPU suite passes 96 tests with no skips, including a single-flight loopback guard that bounds inference to one concurrent request. The corpus is original AI-authored synthetic text, not PhoMT and not human-validated. Phan Rang Cham is deferred pending separate dataset-use permission and language review. Agent creation follows [the user's Luna-only requirement](AGENTS.md).

## Current implementation: action-path composition

The prototype now supports ordered paths containing multiple licensed semantic-action edges. It rolls the transition predictor forward, predicts the final EMA-teacher state, trains the decoder from that composed state against the final target text, and can align composed transition deltas across explicitly paired languages. `generate_path` exposes the same ordered rollout at inference. This is still infrastructure, not a trained language system or evidence of research benefit.

The original, small PyTorch implementation of masked attention, an encoder, typed action transitions, a frozen EMA target encoder, and a causal decoder remains the shared architecture. Objective controls are `token_only`, `generic_jepa`, `static_alignment`, and `tide`; all controls receive the same path-level text-generation supervision, JEPA controls additionally predict the terminal latent state, and static/TIDE alignment additionally use explicitly licensed cross-language path pairs.

An `EdgePath` is an ordered chain of at least two single-action edges in one language. Consecutive semantic frame IDs must connect. A `PathPair` can align paths only when the same complete frame chain and action sequence are explicitly licensed across different languages. Batch position never implies a correspondence. Human-provided metadata is still an assertion that requires evidence; the code cannot validate a speaker's judgment.

No external source code, tokenizer, checkpoint, or dataset is included. PyTorch is the only runtime dependency. Token IDs and approved action inventories are supplied by callers; no Phan Rang Cham orthography or grammar is assumed. PhoMT is approved conditionally as a private Vietnamese–English source; no PhoMT archive is in the repository, and no Phan Rang Cham corpus is approved.

## Milestone 3: reproducible data foundation

`tide_jepa.data` now defines a versioned JSONL transition record, checks declared provenance/license and per-language action approval before experimental splitting, assigns whole `split_group_id` groups deterministically to train/validation/test, writes a SHA-256-addressed split manifest, and converts approved records to validated padded TIDE-JEPA batches. A fixed UTF-8 byte tokenizer maps normalized Unicode to a 259-token vocabulary, so it has no fitted vocabulary or unknown-character bucket. This prevents tokenizer-vocabulary OOVs but can make sequences longer; it is an infrastructure baseline, not a claim that byte encoding improves linguistic accuracy.

Every record has `approval_status`; loaders and grouped splitting reject anything except `approved` by default. That flag is a workflow guard, not proof that the license is legally sufficient. The team must verify source terms, consent, and Cham community/expert approval. Tests use only synthetic records. The separate preliminary pilot has AI review evidence and explicitly records `human_validated=false`.

## PhoMT intake — M4 data annotation gate remains open

The PhoMT author has confirmed the project scopes in writing, conditioned on research/education-only use, no redistribution of any original or modified dataset material, citation of the EMNLP 2021 paper, and a non-commercial license for any released model weights. The Hugging Face repository is gated and requires account login plus acceptance of its access conditions; no login or legal terms were accepted by Codex. After you complete that access step, put the official archive at `data/raw/phomt/PhoMT.zip`. The whole `data/` directory, run outputs, and model checkpoints are Git-ignored.

The local archive has completed a metadata-only audit without member decompression. Run that mode with:

```powershell
py -3.11 -B -m tide_jepa.phomt_audit data/raw/phomt/PhoMT.zip
```

The audit hashes the archive and checks ZIP paths/sizes without extracting it or deserializing pickle members. `--verify-crc` is optional and streams/decompresses members; it was not used for the initial metadata-only audit. Private source selection has prepared 160 pending train-only packets; no translation link was assigned an action label. See [the pilot workflow](VI_EN_PILOT.md) and [the M4 roadmap](ROADMAP.md#milestone-4--approved-pilot-corpus-and-preregistered-benchmark).

## Verified CPU test setup (Windows)

The verified runtime is Python 3.11 with the official `torch==2.14.0+cpu` wheel from PyTorch's CPU package index. From the repository root in PowerShell, create a local environment on a fresh checkout and install the [CPU test requirements](requirements-test-cpu.txt):

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-test-cpu.txt
```

The `.venv` directory is ignored by Git. If it already contains this runtime, use it directly; activation is unnecessary. The requirements file pins PyTorch and its CPU channel; pip resolves transitive dependencies, so this is not a complete dependency lock.

Run the checks with that environment:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m compileall -q tide_jepa tests
```

Verified by the independent scheduled review on 2026-09-29: **all 18 tests passed on CPU, with 0 skipped**, including the action-path tests, using the project-local `.venv` with Python 3.11.9 and PyTorch `2.14.0+cpu`. The review ran `.\.venv\Scripts\python.exe -B -m unittest discover -s tests -v` with `PYTHONDONTWRITEBYTECODE=1`. CUDA was unavailable, and the review did not run `compileall`. This successful run supersedes the earlier report that the local environment could not launch and action-path tensor verification was pending. Synthetic integer IDs are not linguistic examples or Cham data. These CPU checks do not establish GPU compatibility, GPU performance, or research efficacy.

For a dependency-free schema check, `python -m unittest discover -s tests -v` also works with Python 3.10+: tensor tests explicitly skip if PyTorch is absent. A run with skips does not verify the tensor implementation.

The M1/M2 18-test CPU suite passed again on 2026-09-29 after strengthening action-path assertions. After completing M3, the full suite passed **29 tests, 0 skipped** on Python 3.11.9 with PyTorch `2.14.0+cpu`; `compileall` and `pip check` passed. In this shell the installed interpreter loaded Torch from the project `.venv` because its launcher intermittently failed to spawn the base interpreter. No GPU or real-language evaluation was run.

Future GPU training requires the user's device/driver-matched official PyTorch build, selected from [PyTorch's installation guide](https://pytorch.org/get-started/locally/), with separate verification on that device. `requirements-test-cpu.txt` deliberately selects a CPU-only wheel and is not the GPU training setup. No CUDA installation or GPU performance claim is included in this milestone.

## Layout

- `tide_jepa/config.py`: language registry and model sizes.
- `tide_jepa/data.py`: versioned corpus rows, UTF-8 byte tokenizer, approval gate, grouped splits, and fingerprints.
- `tide_jepa/schema.py`: typed actions and explicit licensing of comparable transition edges.
- `tide_jepa/model.py`: original attention, encoder, predictor, and autoregressive decoder.
- `tide_jepa/training.py`: shared trainer and objective controls.
- `tide_jepa/experiment.py`: approval-gated runner, grouped batches, metric logs, explicit alignment loading, and atomic checkpoints.
- `tests/`: standard-library unit tests, with optional PyTorch execution.

The full-batch/experiment runner, checkpointing, deterministic grouped batching, split fingerprints, and train/validation accounting are now implemented. Real-language empirical training still needs an approved corpus; matched-FLOP scheduling, human evaluation, and hackathon task integration remain future work. The included tokenizer and corpus contract do not bundle a corpus. Caller-supplied approval and license references are assertions requiring real evidence; the code cannot validate a speaker's judgment.

## Experiment runner

`python -m tide_jepa.experiment path\to\run.json` runs a configured experiment on a corpus that has already passed source-rights and language-review checks. It refuses records without `approval_status: "approved"`; it does not fetch or approve data. Batches keep every `split_group_id` intact, so aligned translations and multi-edge paths cannot be divided between optimizer steps. The runner writes the split manifest, resolved config and hashes, per-epoch train/validation metrics, and atomic `latest.pt` / `best.pt` checkpoints. It logs examples, UTF-8 byte-token counts, updates, wall time, throughput, and peak allocated VRAM. `--resume` continues only when the config, corpus, split, action inventory, and alignment hashes match.

The held-out test split is reserved and fingerprinted but is not evaluated during training or checkpoint selection. After the protocol and checkpoint-selection rule are frozen, evaluate it once with `python -m tide_jepa.experiment run.json --resume --evaluate-test`; this loads `best.pt` selected on validation and writes `test_metrics.json`. Do not use the test result to change the model or protocol. FLOPs are not estimated; wall time, updates, token counts, examples, throughput, and peak allocated VRAM are recorded. Cross-language losses are enabled only by an optional explicit alignment JSON whose pairs refer to records/paths in the same semantic split group. A blank or missing alignment file never implies a cross-language pair.

An experiment config points to a corpus JSONL, an inventory JSON, and an output directory. The inventory format is:

```json
{
  "actions": [{"kind": "POLARITY", "value": "NEGATIVE"}],
  "approved_by_language": {
    "vi": [{"kind": "POLARITY", "value": "NEGATIVE"}],
    "en": [{"kind": "POLARITY", "value": "NEGATIVE"}],
    "cham_phan_rang": []
  }
}
```

The Cham list stays empty until Cham speakers and a qualified linguist approve a task-specific inventory. A minimal run config is:

```json
{
  "corpus": "approved-pilot.jsonl",
  "inventory": "inventory.json",
  "output_dir": "runs/tide-seed-1",
  "seed": 1,
  "split": {"train": 0.8, "validation": 0.1, "test": 0.1},
  "model": {"width": 64, "heads": 4, "layers": 2, "max_length": 512},
  "objective": {"mode": "tide"},
  "training": {"epochs": 20, "batch_size": 32, "learning_rate": 0.001}
}
```

Use `"alignments": "alignments.json"` to enable separately reviewed pairs. Its `edge_pairs` entries identify `left_record_id`, `right_record_id`, and optionally `relation: "same_event"`; `path_pairs` entries identify each side with `path_id` and `language`, plus the same relation. Pairs must share a `split_group_id`. Run with `python -m tide_jepa.experiment run.json`; resume with `python -m tide_jepa.experiment run.json --resume`. Configs and corpus paths are relative to the config file.

For offline inference with a trained checkpoint, run `python -m tide_jepa.infer run.json runs/tide-seed-1/best.pt`. Send one JSON request per line on stdin, for example `{"request_id":"demo-1","source":"Lan mua một quyển sách.","target_language":"vi","actions":[{"kind":"TIME","value":"PAST"},{"kind":"POLARITY","value":"NEGATIVE"}],"max_new_tokens":96}`. Responses are JSONL and include generated text, token IDs, and a UTF-8 validity flag. The adapter checks the language's approved action inventory and supports single actions or ordered action paths. It does not claim generated text is linguistically correct; use only after human validation.

This runner makes training executable, not scientifically validated. v4.2 failed its generation quality gate; v4.7 also failed validation; v4.8 training is currently incomplete and has not been evaluated. None provides natural-corpus or human linguistic evidence. PhoMT-derived action annotations and the human-validated benchmark remain unfinished.
