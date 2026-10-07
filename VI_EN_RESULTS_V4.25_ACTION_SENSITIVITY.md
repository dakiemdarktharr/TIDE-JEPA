# v4.25 post-hoc action-sensitivity diagnostic

This aggregate-only check compares the saved validation generations for the same exact source text paired with two distinct single actions. It tests whether output changes when the requested action changes; it does not measure whether the changed output is correct. This is post-hoc diagnostic evidence, not frozen-protocol gate evidence, and does not open the release holdout.

All rows are preliminary synthetic evidence; no source, generated, or reference text is shown. Matching is exact after NFC normalization, Unicode case folding, and whitespace normalization. The source is used only as an in-memory SHA-256 grouping key.

| Condition | Language | Same-source pairs | Different outputs | Rate |
|---|---|---:|---:|---:|
| tide-ss-0p0-copy-0p0-seed-17 | en | 640 | 640 | 100.0% |
| tide-ss-0p0-copy-0p0-seed-17 | vi | 640 | 640 | 100.0% |
| tide-ss-0p0-copy-0p0-seed-23 | en | 640 | 640 | 100.0% |
| tide-ss-0p0-copy-0p0-seed-23 | vi | 640 | 640 | 100.0% |
| tide-ss-0p0-copy-0p0-seed-41 | en | 640 | 640 | 100.0% |
| tide-ss-0p0-copy-0p0-seed-41 | vi | 640 | 640 | 100.0% |
| tide-ss-0p2-copy-0p0-seed-17 | en | 640 | 640 | 100.0% |
| tide-ss-0p2-copy-0p0-seed-17 | vi | 640 | 640 | 100.0% |
| tide-ss-0p2-copy-0p0-seed-23 | en | 640 | 640 | 100.0% |
| tide-ss-0p2-copy-0p0-seed-23 | vi | 640 | 640 | 100.0% |
| tide-ss-0p2-copy-0p0-seed-41 | en | 640 | 640 | 100.0% |
| tide-ss-0p2-copy-0p0-seed-41 | vi | 640 | 640 | 100.0% |

Interpretation: distinct outputs are nearly universal across requested action pairs, so a low preservation or fidelity score is not explained by the model always ignoring the action input. It indicates that action-conditioned changes can fail to preserve or realize the intended event roles. This remains an inference from a narrow synthetic rule checker and an exact output-difference diagnostic.

Reproduce without printing examples: `python -B scripts/diagnose_validation_action_sensitivity.py data/pilot/vi-en-ai-v4.25 --markdown YOUR_DIAGNOSTIC.md`.

The diagnostic reads private validation generations under Git-ignored `runs/`; it writes aggregate counts only.
