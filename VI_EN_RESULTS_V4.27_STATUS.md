# v4.27 status: draft retained; holdout boundary compromised

**Decision:** preserve this draft as non-trainable incident evidence. Do not freeze, train, validate, or open its release holdout. No checkpoint was created.

This is an AI-authored synthetic English–Vietnamese pilot. Any review is preliminary AI evidence, not human/native-speaker validation. PhoMT was not used. Phan Rang Cham remains excluded.

## Preregistered diagnostic

The unrun v4.27 draft proposed testing whether a base per-edge token-loss denominator that balances languages improves English patient/predicate preservation without reducing action fidelity or Vietnamese preservation. It was not frozen or trained. The proposed control uses global token-weighted byte cross-entropy. The treatment normalizes token CE per example, averages examples within each language using the frozen edge weights, then gives the present languages equal weight. Both conditions compute both summaries. Only the registered interpolation weight changes the base per-edge token term; composed path-token CE and auxiliary terms remain fixed. This was an optimization hypothesis informed by earlier aggregate results, not a causal diagnosis.

The fixed TIDE model uses width 64, two layers, source-copy weight 0, three seeds (17/23/41), and a fixed final-epoch checkpoint. The two language-balance weights are 0 and 1. All conditions must satisfy the unchanged validation thresholds: Unicode and checker coverage 100%; action fidelity and preservation at least 90% in every single-action language bucket and 80% in every path bucket. The holdout opens only if every primary seed/condition/bucket passes.

## Draft identity and split

- Draft SHA-256: `737c00ba176aa9ccaeac11f452881c5877d5bc37983c87bbb9e65eeb598ed4ae`
- 15,360 records across 192 event combinations; 112/40/40 train/validation/release-holdout groups and 8,960/3,200/3,200 records.
- English and Vietnamese each have 7,680 records.
- Corpus, semantic frames, groups, alignments, reviews, generated outputs, and checkpoints stay under Git-ignored `data/` and `runs/`.

The draft is at `data/pilot/vi-en-ai-v4.27/`; it remains Git-ignored. During review, one reviewer accidentally emitted test-split sentence text into tool output, a second parsed test-split rows for marker checks, and a third printed some source-template examples from code output. No PhoMT material was involved. Those tool-output logs cannot be retracted here. Reviews are retained as incident records, not valid approval for training. The source corpus and generated/reference text are not reproduced in this report.

## Engineering checkpoint

Linux lattice: x86_64, Python 3.11.17, PyTorch 2.14.0+cpu; CPU only. The implementation adds a per-example, equal-language token-loss summary and a registered 0/1 interpolation dimension. Full suite: 121 tests passed, 0 skipped, when run with host loopback access for local demo tests. `compileall`, `pip check`, `git diff --check`, and the synthetic root probe passed. PyTorch reports an optional warning because NumPy is absent; no dependency errors were reported.

The earlier v4.8 artifact hashes match its status file, but its frozen runtime is Windows Python 3.11.9 while this host is Linux Python 3.11.17. v4.8 was not resumed and its identity guard was not bypassed. v4.26 remains a failed validation diagnostic; its holdout also remains sealed.

## Disposition

The language-balanced ablation moves to v4.28 with a new corpus and split. Its reviewers are scoped to train/validation text only; the new test split is not inspected by reviewers. `freeze_pilot` now checks and records that review scope and count. The unchanged validation quality thresholds still control any release-holdout evaluation.
