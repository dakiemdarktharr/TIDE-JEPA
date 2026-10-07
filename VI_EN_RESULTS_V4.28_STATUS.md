# v4.28 status: fresh language-balanced token-loss pilot draft

**Disposition:** retired before freeze or training because one reviewer opened the complete semantic-frame catalog, which includes holdout frame annotations. The reviewer marked holdout text inspected. No holdout sentence was emitted or evaluated, but v4.28 is no longer eligible for a sealed-holdout claim. Preserve its draft and review artifacts as an exposure incident; no checkpoint exists.

This is an AI-authored synthetic English–Vietnamese pilot. Reviews are preliminary AI evidence, not human/native-speaker validation. PhoMT was not used. Phan Rang Cham remains excluded.

## Diagnostic hypothesis

v4.28 tests whether balancing the base per-edge token-loss reduction by language improves English patient/predicate preservation without reducing action fidelity or Vietnamese preservation. The control uses global token-weighted byte cross-entropy. The treatment normalizes token CE per example, takes an edge-weighted mean within each language, then gives English and Vietnamese equal weight. Both summaries are computed in every arm; only their registered interpolation weight (0 versus 1) changes the base per-edge token term. Composed path-token CE and auxiliary terms stay fixed. This is a preliminary optimization diagnostic informed by prior aggregate results, not a causal diagnosis.

The comparison uses fixed 64-width/two-layer TIDE, source-copy weight 0, three seeds (17/23/41), 29 epochs, and a fixed final-epoch checkpoint. It has six configurations. Every primary configuration/seed/language/action bucket must pass the unchanged validation thresholds: 100% valid Unicode and checker coverage; at least 90% action fidelity and preservation in every single-action bucket; at least 80% in every path bucket. The release holdout opens only after every validation gate passes.

## Draft identity and review boundary

- Draft fingerprint: `1b9e1eb16e9a491c02dd25fc2bc036e1c9eea753269cff8d348ad74485b6a7c5`
- 15,360 records across 192 event combinations; 112/40/40 groups and 8,960/3,200/3,200 train/validation/release-holdout records.
- English and Vietnamese each have 7,680 records.
- Review scope is frozen to train and validation: 12,160 rows. Reviewers are instructed not to inspect test-split text. `freeze_pilot` verifies the declared scope and expected count.
- All corpus, frame, review, generated-text, and checkpoint artifacts remain under Git-ignored `data/` and `runs/`.

The draft is at `data/pilot/vi-en-ai-v4.28/`. Its test split uses a new factor block and deterministic split seed. No release-holdout text is reproduced here.

## Engineering checkpoint

The objective now validates and records the language-balance condition. Metrics retain global and per-language-balanced token CE with numeric denominators, and training/resume CSV schemas match. Tests cover the loss formula, blend endpoints, protocol matrix, fresh corpus construction, and train/validation-only review scope.

The current Linux runtime is x86_64, Python 3.11.17, PyTorch 2.14.0+cpu, CPU only. After the v4.28 review-scope changes, all 122 tests passed with no skips, including local loopback demo tests. `compileall`, `pip check`, `git diff --check`, and the synthetic root probe passed. NumPy is absent and causes an optional PyTorch warning; `pip check` reports no broken requirements.

## Disposition

The v4.28 review-a record reports `release_holdout_text_inspected: true` after its reviewer parsed the full semantic-frame file. The v4.28 review-b record independently found that context realization was not separately reported by the evaluator. Neither review was approved, and the draft was never frozen or trained. A fresh v4.29 draft has a new split and an isolated train/validation-only review bundle. No v4.28 data or model will be used for quality evaluation.
