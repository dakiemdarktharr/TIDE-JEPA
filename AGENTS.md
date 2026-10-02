# User requirements for agents

- Create agents/subagents only with `gpt-6-luna` and reasoning effort `high` or `xhigh`.
- Ask the user before using any other model for an agent/subagent.
- This requirement also applies to agents created by subagents and to replacement agents.
- Do not reactivate the interrupted `review_vi_en_a` / `review_vi_en_b` agents; their tasks have been transferred to Luna.

# Dataset and evidence boundaries

- Keep PhoMT raw and derived rows in Git-ignored `data/`; never print them into chat/logs or commit them.
- Never unpickle or execute archive contents. Translation links are not semantic-action labels.
- The user authorizes an AI-authored/AI-reviewed preliminary English–Vietnamese pilot. Label its provenance and results as preliminary; never claim human validation.
- Phan Rang Cham training/evaluation remains deferred pending dataset-use permission and language review.
