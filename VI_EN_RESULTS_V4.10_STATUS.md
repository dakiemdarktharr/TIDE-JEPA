# v4.10 pilot status — 2026-10-03

## Scope and current state

v4.10 is an original AI-authored English–Vietnamese synthetic controlled-language pilot. Two independent Luna reviewers approved the exact draft for **AI-preliminary use only**. An AI adjudication recorded agreement. These checks are not human, native-speaker, community, or independent naturalness validation. The data statement records `human_validated=false` and `phomt_used=false`; no PhoMT or Phan Rang Cham rows were used.

The private corpus has 7,680 records in 192 groups, split into 112/40/40 train/validation/release-holdout groups. Its holdout factor triples are disjoint from training and v4.9 definitions, while individual factors and pairs occur in training. The release holdout uses the schema split name `test` and remains sealed until every registered run finishes and the primary TIDE validation-generation gates pass.

The frozen protocol specifies four modes (`token_only`, `generic_jepa`, `static_alignment`, `tide`), seeds 17/23/41, 58 epochs, width 48, four heads, two layers, batch size 80, learning rate 0.001, maximum sequence length 192, source-copy weight 0.5, and generation budget 160. The primary quality gate applies to TIDE and requires 100% valid Unicode, at least 90% action fidelity and preservation for every single-action language/action bucket, and at least 80% for held-out paths. These are narrow synthetic frame-checker thresholds, not evidence of natural language quality.

All 12 frozen configurations completed Linux CPU training at 58 epochs / 3,248 updates each. Validation-only generation then completed for all 12 configurations. The frozen TIDE gate **failed**: action fidelity and Unicode passed all per-seed buckets, as did both held-out-path preservation buckets, but single-action preservation fell below 90% in multiple English and Vietnamese buckets. The release holdout was not evaluated and remains sealed. See the [aggregate validation report](VI_EN_RESULTS_V4.10_VALIDATION.md) for counts and thresholds.

## Frozen identities

- Draft fingerprint: `c8a08e6042c979e46c5b4d8b53dbe54c702761c459bd5a7402364ede2e6e222f`
- Approved corpus fingerprint: `7f137d8e2c01aaa523e64e9e1585cc9dfb084212043b8759d8cf05fa144de08f`
- Split manifest fingerprint: `95539ef3667da0d07f0a2b4277995449373c1bb0bf623e019148a1773d91c04f`
- Protocol SHA-256: `b5c25b54d917faa35ac58649c6565fdd94320f5fd01d4b8b28aa5b0fd95e2d48`
- AI approval: `approval_kind=AI-preliminary`; `human_validated=false`; `phomt_used=false`
- Reviewer IDs: `AI-Luna-v4.10-final-A-2026-10-03`, `AI-Luna-v4.10-final-B-2026-10-03`

All private rows, review files, configs, protocol and run outputs remain under Git-ignored `data/` and `runs/`. No dataset rows or generated text are reproduced in this report.

## Reproduction commands

From the project root on the Linux lattice host:

```sh
.venv/bin/python -B scripts/train_vi_en_parallel.py data/pilot/vi-en-ai-v4.10 --workers 4
.venv/bin/python -B -m tide_jepa.pilot evaluate data/pilot/vi-en-ai-v4.10 --evaluation-split validation
```

The first command completed successfully on 2026-10-03 (12/12 configurations). The second command completed validation-only generation and failed the primary TIDE gate. Do not score test for v4.10. A subsequent model iteration requires a new reviewed version and a fresh holdout; do not tune v4.10 using release-test outcomes.

Earlier v4.9 was superseded before training because evaluator hardening changed its frozen implementation identity. v4.8 remains paused because its exact private corpus and run artifacts are absent from lattice. See [Linux revalidation](audits/2026-10-03/LINUX_REVALIDATION.md), [v4.8 status](VI_EN_RESULTS_V4.8_STATUS.md), and the [historical results](VI_EN_RESULTS_HISTORY.md).

After v4.10 evaluation, the local demo's quality banner was changed to read the selected checkpoint's validation status; its previous text described only v4.2. This source edit changes the current implementation fingerprint, so preserve v4.10 as a historical completed run. Do not resume or rescore v4.10 with the edited code. Any further model experiment needs a separately reviewed version and a fresh split/holdout.
