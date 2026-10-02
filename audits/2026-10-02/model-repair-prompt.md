# Copy-ready repair prompt for a separate Luna conversation

You are working in `C:\Users\ANHKHOI\Documents\ChatGPT\RMIT_HACKATHON`. First read `AGENTS.md`, `audits/2026-10-02/model-audit.md`, `tide_jepa_spec.md`, `ROADMAP.md`, `VI_EN_PILOT.md`, and `VI_EN_RESULTS.md`. Implement the confirmed software repairs from the audit, add focused synthetic regression tests, update the relevant implementation documentation, and return a concise evidence-based report.

Use only `gpt-6-luna` with high or xhigh reasoning. Do not create subagents. Keep PhoMT raw and derived rows in ignored `data/`; do not read private PhoMT authoring rows, print any PhoMT row, open or unpickle archives, or use translation links as action labels. Use original synthetic fixtures for new tests. Do not use external code, tokenizers, checkpoints, pretrained assets, or datasets. Keep Phan Rang Cham training and evaluation deferred until separate data-use permission and qualified language review are documented.

Repair these findings:

1. In `tide_jepa/experiment.py`, aggregate evaluation and epoch metrics by the denominator each component actually uses: non-padding tokens for token CE, path examples for path terms, explicit pairs for alignment terms, and records/examples for per-example terms. Derive validation checkpoint selection from the resulting corpus-level token and path means. Ensure group-preserving batch packing and `batch_size` do not change metrics on a fixed synthetic dataset.
2. In `tide_jepa/model.py`, make the padding contract true at the model boundary. Either support position IDs that do not shift when padding is added, or reject unsupported padding layouts clearly and narrow the documentation claim. Keep the existing right-padding training behavior covered.
3. Make checkpoint recovery consistent if execution stops between saving `latest.pt` and `best.pt`, and in the reverse ordering. A resumed synthetic run must recover the same best-validation model as an uninterrupted run.
4. Require an exact integer EOS token ID in generation validation, rejecting floats and booleans before generation.
5. Require exact integer indices in `schema.validate_pair`, matching path-pair validation.

Treat the inference implementation fingerprint as an explicit policy question from the audit: either verify the current compatible source fingerprint (including inference code if appropriate) or document why stored provenance is sufficient. Add a focused test for the selected policy.

Do not alter the frozen pilot corpus, split, annotations, review records, configurations, generated outputs, checkpoints, or the published 0/864 pilot result. Do not tune against its held-out test scores. Any future language-quality experiment must use a separately frozen protocol and untouched evaluation examples. Keep all pilot claims labeled preliminary and AI-reviewed; do not claim human validation.

After changes, run the focused synthetic tests and the documented CPU suite with the existing Python 3.11 / PyTorch 2.14 CPU environment, plus compilation and `pip check` if available. Report exact commands and results, list changed files, and identify any remaining limitation. Do not claim Cham readiness or linguistic efficacy from software tests.
