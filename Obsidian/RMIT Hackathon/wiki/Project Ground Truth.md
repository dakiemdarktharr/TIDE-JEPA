# Project Ground Truth

> Raw: [[../raw/Conversation Decisions]], [[../raw/Workspace Snapshot]], [[../raw/PhoMT Permission Confirmation — 2026-10-01]], [[../raw/PhoMT Intake and Vi-En Pilot — 2026-10-01]]
> Fingerprint: GitHub source snapshot `ed4f65c4f0c8268487a2afdd0d69fa7c2812a962` on `master`; latest status update is recorded in Git after this source snapshot.
> Monitored: `ROADMAP.md`, `tide_jepa_spec.md`, `README.md`, `tide_jepa/**`, `tests/**`, `Obsidian/RMIT Hackathon/**`
> Status (2026-10-05): M1–M3 implemented; Linux CPU suite passes 91 tests, 0 skipped, plus compile, dependency and synthetic crash/identity checks. PhoMT archive is locally hash-verified and metadata-audited; 160 private pending source packets exist, with no PhoMT training. v4.8 artifacts remain absent on lattice. v4.10–v4.18 completed registered training/validation but failed or invalidated primary TIDE gates; all fresh release holdouts remain sealed. v4.18's evaluator omitted its event family and had zero semantic-checker coverage, so its gate failed closed; post-hoc corrected scoring remained below thresholds. These are preliminary synthetic AI-reviewed results, not human language validation. Human-validated M4 remains open; Cham is deferred pending source-use permission and linguistic review. Current evidence: [Linux revalidation](../../../audits/2026-10-03/LINUX_REVALIDATION.md), [v4.18 status](../../../VI_EN_RESULTS_V4.18_STATUS.md), [v4.18 aggregate](../../../VI_EN_RESULTS_V4.18_VALIDATION.md), [v4.18 rescore](../../../VI_EN_RESULTS_V4.18_RESCORING.md), [v4.17 status](../../../VI_EN_RESULTS_V4.17_STATUS.md), [v4.16 status](../../../VI_EN_RESULTS_V4.16_STATUS.md), [results](../../../VI_EN_RESULTS.md) and [history](../../../VI_EN_RESULTS_HISTORY.md). Event facts below retain their historical verification dates and were not rechecked this session.

## Goal

Develop and evaluate a from-scratch, action-conditioned JEPA approach for controlled generation in Vietnamese, English, and Phan Rang Cham under fixed task-data budgets. The project's immediate goal is a reproducible, falsifiable research implementation. The official event page now confirms four English-labelled Kaggle tasks at the intersection of security, GenAI, and low-resource languages, but does not provide their definitions, scoring, or deliverables; hackathon alignment remains provisional.

## Accepted constraints

- **Languages:** Vietnamese, English, and Phan Rang Cham. The user's latest correction explicitly adds Phan Rang Cham and supersedes the intermediate Vietnamese–English-only constraint. La Ha, Bố Y, and other languages remain out of scope.
- **Code:** implement the model, trainer, and project-specific baselines from scratch; do not reuse source code from existing repositories or open-source projects.
- **Runtime:** PyTorch is permitted as a tensor/autodiff/runtime dependency.
- **Model shape:** JEPA predicts latent meaning-state transitions conditioned on typed semantic actions; an autoregressive decoder still generates the output sentence.
- **Task:** controlled generation from an event/meaning frame, testing time (`PAST`/`NOW`) and polarity (`POSITIVE`/`NEGATIVE`) and held-out compositions. Human reviewers determine acceptable realizations. Do not assume the Vietnamese–English action inventory or writing conventions transfer to Phan Rang Cham; validate them with appropriate speakers and linguistic expertise first.
- **Evidence:** match training examples and compute across controls. Novelty, efficacy, Q1/Q2 suitability, and hackathon fit are unproven until tested.
- **PhoMT publication invariant:** every paper, preprint, academic report, or published result that PhoMT helps produce must cite Doan et al. (EMNLP 2021). Use is research/education only; do not distribute PhoMT or any part in original or modified form; any released PhoMT-trained weights must use a non-commercial license. The specific license name/version is not yet confirmed. Follow the ready-to-paste citation and release checklist in [[Dataset Research — 2026-09-30]].

## Model identity and draft status

The user explicitly selected **TIDE-JEPA**. The active implementation specification and README now use this name and the three-language scope. Earlier MATE-JEPA/La Ha prospectuses are marked historical drafts; preserve them as research history, not as active requirements. The exact paper title remains provisional.

## Open decisions

- PhoMT is approved only within the author-confirmed conditions: research/education-only, no redistribution, EMNLP citation, and a non-commercial license for released weights. The later archive/hash/metadata check supersedes the earlier empty-folder finding; action packets remain pending and no PhoMT training has run. Source: [[../raw/PhoMT Intake and Vi-En Pilot — 2026-10-01]].
- The user permits AI authoring/review for preliminary Vi–En pilot work, with human review later. v4.2 synthetic-text runs are complete and the quality gate failed; this is not human language evidence. Any future pilot version needs a fresh untouched holdout and independent review. Cham remains deferred. New agents/subagents use only `gpt-6-luna` at `high` or `xhigh` unless another model is explicitly approved. Source: [[../raw/PhoMT Intake and Vi-En Pilot — 2026-10-01]].
- PhoMT supplies translations, not action-conditioned transitions. PhoMT-derived action annotation and the human-validated benchmark still need human-authored semantic edits, bilingual review, adjudication and a fresh frozen split. See [[Dataset Research — 2026-09-30]] and the current pilot results.
- User has now explicitly authorized continuing the project with PhoMT under the received written conditions. Do not infer permission to redistribute PhoMT or to use it commercially.
- How should the research prototype adapt once the official RMIT challenge is released?

## Implementation status

The first three milestones and preliminary AI-reviewed Vi–En engineering workflow are implemented. The current Linux CPU suite passes **91 tests, 0 skipped**; all tests use synthetic fixtures. v4.18 completed all 12 registered runs and validation-only generation, but its frozen evaluator had zero semantic-checker coverage; corrected post-hoc scores remain below thresholds. Its release holdout remains sealed. PhoMT was not used for training; no Cham data was used. CUDA and human linguistic efficacy remain unverified. See [v4.18 status](../../../VI_EN_RESULTS_V4.18_STATUS.md), [frozen evaluation](../../../VI_EN_RESULTS_V4.18_VALIDATION.md), and [aggregate rescore](../../../VI_EN_RESULTS_V4.18_RESCORING.md).

This verifies the tested CPU software contracts, including action-path composition; it does not validate GPU behavior, research efficacy, or real-language outputs. Real-language training remains gated on approved data and language-specific validation, including Phan Rang Cham conventions and actions.

Primary follow-up verification on 2026-09-29 reran all 18 tests successfully with Python 3.11.9 and the project venv's PyTorch `2.14.0+cpu`; `compileall` and `pip check` also passed. The current shell needed the installed interpreter plus the venv site-packages path because the venv launcher intermittently failed to spawn its base interpreter. No runtime reinstall, dataset access, or training was needed.

M3 has since added a versioned record schema, UTF-8 byte tokenizer, approval-gated loader, group-level split manifest, dataset fingerprint, and validated record-to-batch adapter. All 29 tests pass; see [ROADMAP.md](../../../ROADMAP.md) for M3–M5 scope and gates.

## Don't infer

- Do not call Vietnamese inherently low-resource; define the experimental resource limit by a fixed number of task examples.
- Do not equate English tense markers mechanically with Vietnamese particles.
- Do not treat prior-year hackathon tasks as 2026 requirements.
- Do not present candidate research hypotheses as experimental findings.

## Provenance

User decisions and prior-chat research summaries are captured in [[../raw/Conversation Decisions]]. File/repository status is in [[../raw/Workspace Snapshot]].

The 2026-09-29 milestone/test-status correction records the independent scheduled review result relayed by the orchestrator in the current project conversation. It reconciles this ledger with the active specification and README; it does not alter earlier raw records or assert new language/data approvals.

The subsequent regression-coverage follow-up on 2026-09-29 reran the same CPU command after strengthening path-text equality and static/TIDE path-alignment assertions: 18 passed, 0 skipped. No `compileall` or GPU check was run in that follow-up.

## Update — 2026-09-30

The user confirmed that intended project use includes research/education and the RMIT hackathon. On 2026-10-01, PhoMT author Dat Quoc Nguyen replied that the scopes requested are allowed subject to the stated dataset terms, and added that released PhoMT-trained weights must use a non-commercial license. The archive is still gated on Hugging Face; no dataset has yet been downloaded. CLA Eastern Cham Field Materials remains an archive lead, not an approved training corpus; item-level and community/linguist review is still required. See [[Dataset Research — 2026-09-30]].

The approval-gated experiment runner and offline inference adapter were added on 2026-09-30. They have not yet been run or independently reviewed; prior 29/29 CPU results apply to the earlier M1–M3 code snapshot only. No language training or efficacy result exists.

## Update — 2026-10-01: PhoMT intake

This section preserves the earlier access handoff. The later local intake and preliminary-pilot record supersedes its download state: [[../raw/PhoMT Intake and Vi-En Pilot — 2026-10-01]].

The user authorized continuing with PhoMT after receiving written author approval for the requested non-commercial research/education and hackathon scope. The access conditions remain binding: no redistribution of PhoMT or any part in original or modified form; cite the EMNLP paper; use a non-commercial license for any released weights. The current official Hugging Face page requires sign-in and acceptance of access conditions that share account contact information. Codex stopped before login or acceptance; the page was left open for user handoff. A project-authored metadata-only ZIP auditor and six synthetic tests were added. No PhoMT records were ingested and no model was trained.
