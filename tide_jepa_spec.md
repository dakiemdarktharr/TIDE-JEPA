# TIDE-JEPA — active implementation specification

Date: 2026-10-03. Status: M1–M3 are implemented; the full Linux CPU suite passed with 70 tests and 0 skipped, plus compile and dependency checks. PhoMT archive intake and private train-only source selection are complete, but no PhoMT action corpus or PhoMT training exists. v4.8 training is paused with four of 12 configurations complete and four partial; no v4.8 validation result exists, and its release holdout is still sealed. Its local data and run artifacts are absent on the current Linux host, so exact resume is pending transfer; see [v4.8 training status](VI_EN_RESULTS_V4.8_STATUS.md) and the [Linux revalidation report](audits/2026-10-03/LINUX_REVALIDATION.md). Earlier v4.7 and v4.2 failures remain preserved. No human validation, natural-corpus efficacy or novelty claim is made. Cham training/evaluation is deferred pending permissions and linguistic review. See [pilot workflow](VI_EN_PILOT.md), [current results](VI_EN_RESULTS.md), [historical results](VI_EN_RESULTS_HISTORY.md) and [AGENTS.md](AGENTS.md).

## Authority and scope

The user selected **TIDE-JEPA** and **Vietnamese, English, and Phan Rang Cham (Chăm Phan Rang)**. This supersedes MATE-JEPA, the temporary Vietnamese–English-only scope, and the La Ha extension in earlier drafts. The [decision ledger](Obsidian/RMIT%20Hackathon/wiki/Project%20Ground%20Truth.md) records this authority. No expansion of the TIDE acronym is assumed.

Working title: *TIDE-JEPA: Action-Conditioned Latent Transitions for Data-Constrained Vietnamese, English, and Phan Rang Cham Generation*.

Implement model, trainer, and project-specific controls from scratch. PyTorch may provide tensors, autodiff, neural-network primitives, and optimization. Do not copy external implementation code or use pretrained weights/tokenizers. PhoMT may be acquired and used only within the conditional written permission recorded in the [data research note](Obsidian/RMIT%20Hackathon/wiki/Dataset%20Research%20%E2%80%94%202026-09-30.md); never publish or upload its raw/derived rows.

Installing the pinned CPU test runtime is explicitly permitted: use Windows Python 3.11 and the project-local, Git-ignored `.venv`, with official `torch==2.14.0+cpu` from `https://download.pytorch.org/whl/cpu` as specified in [requirements-test-cpu.txt](requirements-test-cpu.txt). Follow the setup and test commands in the [README](README.md). This permission covers the CPU test environment only; do not install CUDA or a GPU runtime in this milestone. PhoMT has conditional written permission and a verified local archive; its derived action labels remain a separate gate. No other discovered corpus is automatically approved.

## Research direction

Encode a source utterance or approved representation, predict its latent meaning state after a typed semantic action, and autoregressively render the requested target language. Test whether matching action-induced latent changes across languages helps held-out compositions at matched task-data and compute budgets. Vietnamese is not assumed inherently low-resource.

Time (`PAST`/`NOW`) and polarity (`POSITIVE`/`NEGATIVE`) are proposed English–Vietnamese annotation categories. They do not define Phan Rang Cham grammar. Appropriate speakers and linguistic expertise must validate Phan Rang Cham variety, writing/recording conventions, actions, scope, permissions, and acceptable outputs before linguistic training or evaluation. Its registry entry is deliberately present without a default approved action inventory.

## Milestone 1 contract

- Callers supply padded integer sequences, lengths implied by a reserved padding ID, target-language IDs, and a single typed action per transition edge. No text tokenizer is chosen.
- A small custom attention encoder gives a pooled source state. An action/language-conditioned residual predictor maps it to a target state. A causal attention decoder conditions on that predicted state and language to predict tokens.
- An EMA encoder supplies stop-gradient target states. Only the online encoder is averaged; target parameters never enter the optimizer. Padding positions cannot affect valid states. The decoder receives teacher-forcing input and next-token labels supplied by the caller.
- `token_only` uses token cross-entropy. `generic_jepa` adds paired-target latent prediction. `static_alignment` adds endpoint alignment across explicitly comparable edges. `tide` instead aligns differences between projected predicted and source states across explicitly comparable edges. These are initial objective controls, not the full publication baseline suite.
- The initial canonical projection is fixed identity in the shared latent basis, so a learned comparison head cannot shrink to zero to minimize alignment. Learnable language-specific projections remain a future design/ablation decision.
- Every comparison requires an explicit license carrying source/target frame IDs and a common action. Unknown or scope-different edges cannot enter alignment. No cross-language pair is inferred from batch position. Comparable edges must realize the same source and target semantic frames in different languages.
- A batch edge currently represents an action within one language; cross-language supervision compares two such edges. The interface does not yet support a single translation edge with different source and target languages. Decoder labels and EMA target tokens must be identical, and decoder input is the right-shifted target preceded by `ModelConfig.bos_id`. This configured BOS must be an integer in the vocabulary, distinct from padding. Training validates every row's first token, and generation rejects a caller-supplied BOS that differs from configuration.
- The JEPA modes include configurable variance regularization and return latent spread diagnostics. Tiny batches cannot demonstrate absence of representation collapse. Objective weights are experimental hyperparameters.
- Training returns scalar metrics and updates EMA after the optimizer step. It does not download data or run on import. The trainer assumes caller-provided batches were validated by the batch validator and validates each call itself.

## Evidence and limitations

Synthetic integer tests exercise software contracts only. They are not language evaluation. No real-language corpus, action licenses, accepted output strings, or Phan Rang Cham forms are supplied.

On 2026-09-28, all 13 tests passed without skips on Windows Python 3.11 with official PyTorch `2.14.0+cpu`, and compilation checks passed. [CPU test requirements](requirements-test-cpu.txt) pin the tested PyTorch wheel and official CPU index; transitive dependencies are not fully locked. GPU training requires a device-matched official PyTorch build and its own verification. CPU success does not demonstrate GPU performance or research efficacy.

## Milestone 2: ordered action-path composition

The second requested implementation milestone adds a data-agnostic, ordered path objective without changing the approved three-language scope or introducing Cham grammar assumptions.

- `EdgePath` contains at least two edge indices. Each path must be licensed, continuous in semantic-frame IDs, and entirely within one language.
- `PathPair` links two paths only when their complete semantic-frame chain and ordered action sequence match and their languages differ. Batch position does not imply alignment.
- The predictor is applied sequentially from the first edge's source state. Every objective control receives the same final-target text supervision through the decoder. JEPA modes also train the composed prediction against the EMA target encoding of the final edge's target, so `token_only` remains a matched path-text baseline rather than losing access to the path examples.
- `static_alignment` compares composed endpoints for a licensed path pair. `tide` compares composed predicted-minus-source transitions. These losses remain experimental formulations, not language-validated results.
- `generate_path` supports inference-time rollout for a supplied ordered action sequence.
- Synthetic tests cover schema and objective contracts only. They do not establish that action paths are meaningful for any language or that composition generalizes to held-out linguistic combinations.

Verification status for this milestone: independent scheduled review on 2026-09-29 ran `.\.venv\Scripts\python.exe -B -m unittest discover -s tests -v` with `PYTHONDONTWRITEBYTECODE=1` in the project-local environment, using Python 3.11.9 and PyTorch `2.14.0+cpu`. All 18 tests passed, with 0 skipped, including the action-path tests. A same-day primary rerun also passed all 18 tests, and `compileall` plus `pip check` passed. In that shell, I launched the installed Python 3.11.9 interpreter and added the project's `.venv\Lib\site-packages` to its import path because the venv launcher intermittently failed to spawn its base interpreter; no runtime reinstall was needed. CUDA was unavailable. This evidence supersedes the earlier runtime-launch failure and pending tensor-verification report. The 2026-09-28 all-13 test and compilation results above remain historical evidence for the first milestone. The current CPU result verifies the tested software contracts only; it does not establish CUDA support, GPU performance, or linguistic/research efficacy.

Still future work: alternative-path equivalence, semantic classifier losses, active elicitation, uncertainty calibration, generation metrics, multi-reference loss, corpus-to-batch integration, serialization/resumption, and matched-compute scheduling. Equal architecture/batches alone do not establish equal compute: final studies must record frames, token counts, label access, updates, FLOPs/wall time, memory, and annotation time. Generic paired-target JEPA is one provisional control and needs a finalized experimental definition.

Regression-coverage follow-up on 2026-09-29: the same CPU suite passed all 18 tests, with 0 skipped, after adding assertions that all four modes share equal path-text loss and that static path alignment compares endpoints while TIDE compares transition deltas. The later primary rerun additionally verified `compileall` and `pip check`; no GPU verification was performed.

The [Vi–En annotation draft](vi_en_annotation_protocol.md) remains a useful component. The [research note](jepa_low_resource_q1_research.md) preserves earlier literature exploration; linked factual and publication claims require fresh verification before reuse. The two older prospectuses remain historical design records. No claim is made that this prototype meets undisclosed hackathon requirements or journal acceptance criteria.

## Milestone 3 implemented: data contract and reproducibility

`tide_jepa.data` adds `CorpusRecord`, a versioned UTF-8 JSONL reader, a fixed UTF-8 byte tokenizer, approval/provenance/license fields, group-safe deterministic splitting, canonical dataset fingerprints, and atomically written split manifests. The record stores one single-action edge; `path_id`/`path_step` group ordered edges, which are checked for contiguous steps and semantic-frame continuity. Aligned language realizations must share a split group, preventing their event-level leakage across partitions.

The loader and splitter require `approval_status="approved"` by default and validate each action against the caller's `Inventory`. `require_approved=False` is reserved for metadata audit, not training. The flag and license reference cannot establish legal rights or speaker consent; those remain human review gates. UTF-8 byte encoding is no-OOV and corpus-independent but can expand sequence lengths; it is an input baseline, not an asserted innovation or result. Unicode is normalized to NFC at tokenization time, while stored source strings are left unchanged.

At M3 completion, the suite exercised conversion from approved in-memory records to padded tensors and ordered paths without inferring cross-language alignments; its fixtures were synthetic only. M4 received conditional PhoMT rights, and a local archive passed its metadata audit. A private pending source selection exists, but no PhoMT action labels or model training are approved/completed. The AI-reviewed v4.2 synthetic preliminary pilot is an engineering experiment, not the human-validated M4 benchmark; it failed its frozen generation quality gate. See [ROADMAP.md](ROADMAP.md) for the full M3–M5 sequence and gates.

## M4 update — PhoMT permission and safe intake (2026-10-01)

The original access handoff below is historical. The later verified archive, pending private source selection and completed AI-reviewed synthetic pilot are documented in [VI_EN_PILOT.md](VI_EN_PILOT.md), [VI_EN_RESULTS.md](VI_EN_RESULTS.md), and the [intake/pilot evidence](Obsidian/RMIT%20Hackathon/raw/PhoMT%20Intake%20and%20Vi-En%20Pilot%20%E2%80%94%202026-10-01.md). Those records supersede its acquisition state without claiming PhoMT training or human validation.

PhoMT author Dat Quoc Nguyen confirmed the proposed internal selection/annotation, training/evaluation, and limited model-output/aggregate-result presentation scopes, conditioned on research/education-only use, no redistribution of PhoMT or any original/modified portion, and citation of the EMNLP 2021 paper. He added that released PhoMT-trained weights must use a non-commercial license. The archive is gated on Hugging Face; Codex stopped before sign-in or acceptance of access conditions that share account contact information. No archive has been downloaded or used. `tide_jepa.phomt_audit` provides a project-authored ZIP metadata/CRC audit and refuses unsafe paths; it does not extract or unpickle content. PhoMT translation links alone must not be converted into action edges: the pilot still needs human-authored, reviewed within-language semantic transformations. See [ROADMAP.md](ROADMAP.md) and the [data research note](Obsidian/RMIT%20Hackathon/wiki/Dataset%20Research%20%E2%80%94%202026-09-30.md).

