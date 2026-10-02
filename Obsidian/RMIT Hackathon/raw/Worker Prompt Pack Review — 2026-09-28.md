# Worker prompt pack independent review — 2026-09-28

> Status: Read-only audit by `review`; orchestrator addressed the findings below in the prompt pack and workflow.

## Findings and disposition

1. **P2 — Data-use wording was broader than Ground Truth.** The reusable heavy/find prompts said datasets could never be downloaded/imported, but Ground Truth leaves public data-use open and the active spec's no-download rule applies to the current infrastructure milestone. Updated the prompts to require a user-approved, source-specific purpose/rights/governance gate and to explicitly prohibit downloads for the current milestone.
2. **P2 — “Exact diff” could omit untracked files.** The repository currently has no baseline Git commit and project files are untracked, so `git diff` is insufficient for review. Updated the reviewer and workflow instructions to inspect the exact changed-file list including new/untracked files, and to use a full patch/snapshot or inspect listed contents when no baseline exists.
3. **P3 — Group broadcast operation is unavailable.** The collaboration interface provides direct point-to-point worker messages, not a group broadcast. Updated the orchestrator prompt to message each affected worker directly.

## Review scope and result

The reviewer found role scopes/model-effort targets consistent with the user-defined roles and supported launch options; it found no further mismatch in the Cham/data governance, no-external-contact, prompt-injection, or read-only-review boundaries. It verified relevant Obsidian links. No tests were run because the reviewed changes are Markdown-only.

The orchestrator updated [[../wiki/Worker Prompt Pack]] and [[../wiki/Agentic Workflow]] after receiving these findings. A follow-up review of those corrections is still required before the prompts are considered closed.
