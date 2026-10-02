# Workflow reassessment — 2026-09-28

> Status: Orchestrator process review using the `agent-teams:task-coordination-strategies` skill and the current workflow, ground-truth, and heartbeat notes. This changes coordination documentation only; no code or worker model settings changed.

## Current design reviewed

The current process already has distinct code (`heavy`), independent review (`review`), and evidence (`find`) owners; the orchestrator mediates scope and handoffs. It has prompt-injection boundaries, an immediate review on heavy completion, a 10-minute quiet heartbeat, and a requirement to recheck fixes.

## Gaps found

1. The handoff sequence did not require every assignment to name owned files, interfaces/dependencies, acceptance criteria, and exact evidence. A worker could finish a plausible implementation while leaving the scope of review implicit.
2. It allowed parallel work without an explicit file-ownership / dependency condition, risking conflicting edits or review of a stale diff.
3. “Distribute work evenly” was not translated into role-appropriate deliverables. Equal hours would be a poor measure because code, independent review, and external evidence have different shapes; unused roles should remain available instead of receiving duplicate or invented work.
4. The delivery gate named critical/high review findings but did not define how fixes are closed against the reviewed diff or prevent re-reviewing unchanged code.

## Changes made

Updated [[../wiki/Agentic Workflow]] to:

- Require an explicit task contract for each user-requested feature/research milestone, including ground-truth links, ownership, requirements, acceptance evidence, boundaries, dependencies, and next owner.
- Give each role explicit file ownership and make read-only review the default for `review`.
- Permit parallel dispatch only for independent work with separate owned files; require data-dependent code to wait for evidence and an explicit data-use gate.
- Bind review to the exact implementation diff, require per-finding fix/recheck closure, and make delivery criteria explicit.
- Balance work through distinct measurable artifacts per relevant role, while forbidding duplicate reviews or dataset searches merely to occupy a worker.
- Carry source-trust/prompt-injection handling into each task brief and define conflict escalation.

## Evidence, limits, next use

- Inputs inspected: current workflow, Project Ground Truth, and Review Heartbeat Setup notes; coordination-skill guidance on decomposition, dependencies, task descriptions, and workload balancing.
- This is a design correction, not evidence of run-time enforcement by the Codex app. On the next requested milestone, inspect whether the task contract and review-closure steps are actually followed and amend the workflow if not.
- No new feature was dispatched because the ground-truth ledger says the first implementation milestone is complete and the next feature/version remains unspecified.
