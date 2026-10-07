# v4.23 post-hoc action-sensitivity diagnostic

This aggregate-only check compares the saved validation generations for the same exact source text paired with two distinct single actions. It tests whether output changes when the requested action changes; it does not measure whether the changed output is correct. This is post-hoc diagnostic evidence, not frozen-protocol gate evidence, and does not open the release holdout.

All rows are preliminary synthetic evidence; no source, generated, or reference text is shown. Matching is exact after NFC normalization, Unicode case folding, and whitespace normalization. The source is used only as an in-memory SHA-256 grouping key.

| Condition | Language | Same-source pairs | Different outputs | Rate |
|---|---|---:|---:|---:|
| tide-decoder-source_pointer-copy-0p0-seed-17 | en | 640 | 640 | 100.0% |
| tide-decoder-source_pointer-copy-0p0-seed-17 | vi | 640 | 639 | 99.8% |
| tide-decoder-source_pointer-copy-0p0-seed-23 | en | 640 | 640 | 100.0% |
| tide-decoder-source_pointer-copy-0p0-seed-23 | vi | 640 | 635 | 99.2% |
| tide-decoder-source_pointer-copy-0p0-seed-41 | en | 640 | 640 | 100.0% |
| tide-decoder-source_pointer-copy-0p0-seed-41 | vi | 640 | 636 | 99.4% |
| tide-decoder-source_pointer-copy-1p5-seed-17 | en | 640 | 640 | 100.0% |
| tide-decoder-source_pointer-copy-1p5-seed-17 | vi | 640 | 640 | 100.0% |
| tide-decoder-source_pointer-copy-1p5-seed-23 | en | 640 | 640 | 100.0% |
| tide-decoder-source_pointer-copy-1p5-seed-23 | vi | 640 | 633 | 98.9% |
| tide-decoder-source_pointer-copy-1p5-seed-41 | en | 640 | 640 | 100.0% |
| tide-decoder-source_pointer-copy-1p5-seed-41 | vi | 640 | 632 | 98.8% |
| tide-decoder-vocabulary-copy-0p0-seed-17 | en | 640 | 640 | 100.0% |
| tide-decoder-vocabulary-copy-0p0-seed-17 | vi | 640 | 633 | 98.9% |
| tide-decoder-vocabulary-copy-0p0-seed-23 | en | 640 | 640 | 100.0% |
| tide-decoder-vocabulary-copy-0p0-seed-23 | vi | 640 | 637 | 99.5% |
| tide-decoder-vocabulary-copy-0p0-seed-41 | en | 640 | 640 | 100.0% |
| tide-decoder-vocabulary-copy-0p0-seed-41 | vi | 640 | 626 | 97.8% |
| tide-decoder-vocabulary-copy-1p5-seed-17 | en | 640 | 640 | 100.0% |
| tide-decoder-vocabulary-copy-1p5-seed-17 | vi | 640 | 633 | 98.9% |
| tide-decoder-vocabulary-copy-1p5-seed-23 | en | 640 | 640 | 100.0% |
| tide-decoder-vocabulary-copy-1p5-seed-23 | vi | 640 | 630 | 98.4% |
| tide-decoder-vocabulary-copy-1p5-seed-41 | en | 640 | 640 | 100.0% |
| tide-decoder-vocabulary-copy-1p5-seed-41 | vi | 640 | 625 | 97.7% |

Interpretation: distinct outputs are nearly universal across requested action pairs, so the low v4.23 role-preservation and fidelity results are not explained by the model always ignoring the action input. They indicate that action-conditioned changes frequently fail to preserve or realize the intended event roles. This remains an inference from a narrow synthetic rule checker and an exact output-difference diagnostic.

Reproduce without printing examples: `python -B scripts/diagnose_validation_action_sensitivity.py data/pilot/vi-en-ai-v4.23 --markdown YOUR_DIAGNOSTIC.md`.

The diagnostic reads private validation generations under Git-ignored `runs/`; it writes aggregate counts only.
