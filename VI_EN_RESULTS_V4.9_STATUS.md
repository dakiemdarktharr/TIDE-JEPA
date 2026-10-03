# v4.9 preliminary synthetic pilot — frozen, superseded before training

Status recorded 2026-10-03 on lattice. This is an aggregate-only protocol and artifact status note. Corpus, reviews, checkpoints, generated text, and metrics remain under Git-ignored `data/` or `runs/`.

## Data and review

v4.9 is an original AI-authored synthetic English–Vietnamese pilot, not PhoMT. It has 7,680 records across 192 event/action groups: 112 train, 40 validation, and 40 release-holdout groups (the frozen schema labels that split `test`). The holdout uses a fresh combination pool built from three newly authored agent identities; every held-out factor pair appears in train. Surface grammar uses a deliberately narrow present/past and polarity contract with two variants per frame. It is not natural-corpus or domain-generalization evidence.

Two independent `gpt-6-luna` reviews checked all 7,680 rows and bound the reviewed artifact hashes. Reviewer A approved only the preliminary AI scope after structural, frame/action, and representative bilingual checks. Reviewer B's aggregate checks passed; a text-attestation limitation was adjudicated against A's independent pattern review and the deterministic checker. AI adjudication resolved the schema-label/hash wording. Human validation and language-community clearance remain false and unavailable.

Canonical draft fingerprint: `b7e97c84b196ac73cd9aa7e433ce84b2f68eda413ce453af7b6bde046d4dcc2c`.

## Frozen training and quality protocol

- Four modes: `token_only`, `generic_jepa`, `static_alignment`, `tide`.
- Seeds: 17, 23, 41; 58 epochs; width 48; four heads; two layers; batch size 80; learning rate 0.001; max length 192; source-copy weight 0.5.
- Validation quality gate for primary mode `tide`: 100% valid Unicode; every language/action single-action bucket at least 90% action fidelity and preservation; held-out path buckets at least 80% for both checks.
- The frozen runner first trains every configuration and writes validation generation evidence. It only permits release-test evaluation after every primary-seed validation report passes the frozen thresholds. Direct model and generation test-evaluation entry points enforce this gate. If validation fails or misses evidence, test stays sealed.

Frozen corpus SHA-256: `d722db234b7e5849891a0fd25d685014ce3cecf519439876b518ff2b72cee3b9`.

Frozen split SHA-256: `cfb59416e266d8cbe7203ae6255e684c63d9cc2dd7f570bdae532fb4c32a2a45`.

Training never started; there are no checkpoints, validation metrics, or release-test scores. After freeze, the evaluation implementation was hardened to require a passing validation gate before release-test scoring. That changed the implementation identity, so the current runner correctly refuses this earlier frozen snapshot. Its artifacts and unopened holdout remain preserved. Do not rewrite its protocol identity or claim a run. The project proceeds with a fresh version and holdout under the hardened runner. PhoMT was not downloaded or used for this version. Phan Rang Cham remains deferred.

## Verified Linux commands

From the project root, after review/freeze and before any test scoring:

```bash
.venv/bin/python -B -m tide_jepa.pilot run data/pilot/vi-en-ai-v4.9
.venv/bin/python -B -m tide_jepa.pilot evaluate data/pilot/vi-en-ai-v4.9 --evaluation-split validation
```

The first command trains registered runs and validation evaluations, then opens release-test scoring only if the gate passes. Prefer the parallel runner for CPU scheduling:

```bash
.venv/bin/python -B scripts/train_vi_en_parallel.py data/pilot/vi-en-ai-v4.9 --workers 4
```

Do not run the release-test evaluation manually unless all training has completed and every frozen primary-seed validation gate passes. Results must be aggregate-only; generated rows stay private in `runs/`.
