# First Implementation Milestone

> Raw: [[../raw/First Milestone Evidence]], [[../raw/PyTorch Runtime Probe]], [[../raw/CPU Model Test Validation]], [[../raw/CPU Requirements Recheck]], [[../raw/Conversation Decisions]], [[../raw/Workspace Snapshot]]
> Fingerprint: uncommitted workspace snapshot after initial implementation, 2026-09-28
> Monitored: `README.md`, `tide_jepa_spec.md`, `tide_jepa/**`, `tests/**`, `.gitignore`
> Status: Current for the first data-agnostic prototype; synthetic runtime tests pass on CPU. GPU and language/research validation remain incomplete.

## Result

Heavy delivered the first from-scratch, PyTorch-based TIDE-JEPA code milestone. It establishes a data-agnostic prototype for Vietnamese, English, and Phan Rang Cham, while leaving Cham grammar, writing practice, tokenizer choices, action inventory, text examples, and data use behind a speaker/expert validation gate. No dataset was downloaded or added.

Current code implements within-language action edges with cross-language paired supervision. It does not yet implement cross-language source-to-target translation edges, composed paths, corpus ingestion/splits, or matched-compute experiments. See the active [TIDE-JEPA specification](../../../tide_jepa_spec.md).

## Review and verification

Review identified a P2 training/inference BOS-prefix mismatch. Heavy fixed it by validating a shared configured BOS in `ModelConfig`, every training batch, and generation; regression cases were added. Review rechecked the fix and found no additional high-severity issue for this milestone.

The project's default Python has no usable Torch, and the Windows Store Python 3.13 Torch files were incomplete. A project-local `.venv` was then created with the official CPU wheel `torch==2.14.0+cpu`. The exact README `pip install -r requirements-test-cpu.txt` command resolved successfully; `pip check` found no broken requirements; all 13 tests passed and `compileall` passed. CUDA is unavailable in this CPU-only wheel. This verifies the covered synthetic tensor/software contracts on CPU, but does not verify GPU behavior, language quality, or research efficacy. Evidence: [[../raw/PyTorch Runtime Probe]], [[../raw/CPU Model Test Validation]], [[../raw/CPU Requirements Recheck]].

## Later project verification — 2026-10-02

The first milestone notes above are historical. The current complete CPU suite passes 58 tests with 0 skips, and compileall plus root crash/replay probes pass. The user-authorized preliminary v4.2 synthetic Vi–En pilot completed 12 fixed runs but failed its frozen generation quality gate (0/2,592 accepted-reference matches; 0 preservation passes). This is AI-reviewed synthetic evidence only, not human language validation. See [current results](../../../VI_EN_RESULTS.md) and [historical pilot results](../../../VI_EN_RESULTS_HISTORY.md). No PhoMT rows were used for model training. Phan Rang Cham remains deferred.

## Next owners

- **heavy:** continue only on the next user-requested feature/version, or a concrete review finding.
- **review:** review each completed implementation and approximately every 10 minutes of active implementation; report exact severity/location and recheck fixes.
- **find:** handle reviewer evidence questions and dataset follow-up. The current dataset report is [[Dataset Research — 2026-09-28]].
- **orchestrator:** maintain the user-approved scope and route work; return completed, reviewed milestones and wait for the next requested feature/version.
