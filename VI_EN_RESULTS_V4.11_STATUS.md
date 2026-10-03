# v4.11 frozen pilot status — 2026-10-03

This is an original AI-authored synthetic English–Vietnamese pilot. It is preliminary and **not human/native-speaker validated**. PhoMT was not used; Phan Rang Cham is excluded.

## Frozen evidence

- Draft fingerprint: `7faaa648bd40d9634891cb2ca3eb593fb132071e2173716ba8e4130e3888241d` (7,680 records; 3,840 per language; 192 groups, split 112/40/40).
- Two independent `gpt-6-luna` high reviews approved the exact draft; the artifact-bound adjudication records agreement. Their judgments are AI-only and preliminary.
- Frozen corpus fingerprint: `47efa4720a556497adebada742857d829d4290da1cd5429098527c8faae79061`.
- Frozen split fingerprint: `66ad9e5699ff6ec75bcdcb7031476c1e8a891d26b42c84f91fbf25b5e45621d4`.
- Frozen protocol fingerprint: `4fcbfc16c9398939193f03b1a16eb05eefb48e397404e02a82213d0bee109ad5`.
- 12 configurations: `token_only`, `generic_jepa`, `static_alignment`, and `tide`; seeds 17, 23, and 41; 58 epochs each. Width 48, four heads, two layers, max length 192, batch size 80, learning rate 0.001.
- Primary mode is TIDE. Source-copy loss weight is 1.5, preregistered as an unverified response to v4.10's preservation failure. It is not evidence of improvement.
- Frozen gates are unchanged: valid Unicode 100%; each language/action single-action fidelity and preservation bucket at least 90%; held-out path fidelity and preservation at least 80%. Holdout access requires all runs complete and primary TIDE validation gates passing.

## Run state

Freeze and all 12 CPU training runs completed on lattice's project `.venv` using Python 3.11.17 and CPU PyTorch 2.14.0. Every run reached 58 epochs / 3,248 steps; protocol/runtime/implementation and run identities match, and `best.pt`/`latest.pt` agree for every run. Validation-only evaluation is now running. No test metrics exist. Keep the release holdout sealed if any primary validation gate fails. Dataset, reviews, protocol, checkpoints and run logs stay under Git-ignored `data/` and `runs/`.

Reproduce the frozen run from the repository root:

```bash
.venv/bin/python -B scripts/train_vi_en_parallel.py data/pilot/vi-en-ai-v4.11 --workers 4
.venv/bin/python -B -m tide_jepa.pilot evaluate data/pilot/vi-en-ai-v4.11 --evaluation-split validation
```

Only after validation passes every primary TIDE gate may the release test be evaluated:

```bash
.venv/bin/python -B -m tide_jepa.pilot evaluate data/pilot/vi-en-ai-v4.11 --evaluation-split test
```

The exact aggregate validation and test results must be recorded in a separate dated report. Never put corpus rows or generated/reference text in public documents.
