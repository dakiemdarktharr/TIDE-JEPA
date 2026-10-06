# Project troubleshooting — 2026-10-06

The reproducible software defects found in this review are repaired. The final Linux CPU suite passed **109 tests, zero skips**, with Python 3.11.17 / PyTorch 2.14.0+cpu. The model's language-quality failure remains open: v4.20 failed every registered validation bucket. This report does not claim the project is free of untested bugs or that its model is usable for language generation.

## Reproduced defects and repairs

| Defect | Repair and evidence |
|---|---|
| The v4.20 validation summarizer raised `primary validation evidence does not cover every frozen seed` despite all six decoder/seed runs being present. The release guard omitted the same decoder dimension. | A shared primary-matrix validator checks seed, copy weight, latent dose, balance, and decoder. Reports and component diagnostics keep decoder variants separate. Synthetic missing/duplicate-condition tests and a two-decoder training/holdout-guard integration test passed. Actual v4.20 aggregation now succeeds for six runs; historical v4.19 aggregation still succeeds for 12. |
| Validation reporting trusted unbound or incomplete aggregate artifacts and estimated updates as final-epoch updates × epochs. | Reporting verifies registered config hashes, checkpoint/evaluation/run/protocol identities, and exactly one train/validation row for every registered epoch; updates are summed from the actual log. Changed-checkpoint and incomplete-log regressions passed. |
| `token_count.clamp_min(1.0)` understated token loss for valid edge weights whose weighted token count was below one. | The mean uses its positive validated denominator. A regression verifies loss and gradient invariance under uniform weight scaling. This defect does not explain v4.20, whose row-uniform counts exceeded one. |
| Pilot freeze checked a hard-coded 32-width/192-token configuration instead of the requested model limits, and accepted invalid learning rates. | Freeze validates the actual requested dimensions/length and finite numeric learning rate before publishing approved artifacts. Generation budget leaves room for BOS; the CLI now exposes `--max-length`. Invalid-rate and short-length regressions passed. |
| Default inference budget could exceed a small checkpoint's maximum sequence length; the browser always requested 160 tokens. | Inference and HTTP defaults fit the checkpoint; health advertises the supported limit and the current UI follows it. Small-checkpoint and DOM regressions passed. |
| An unexpected model runtime failure disconnected HTTP clients instead of returning a controlled response; disconnected clients could cause error traces while responding. | Model failures return a generic HTTP 500, disconnected responses close quietly, and the inference semaphore is released. A failure-then-success loopback regression passed. |
| Duplicate submit events could race a pending browser response. | The current UI refuses a second submission while one is pending. A DOM simulation verifies one request, an unchanged submitted-input snapshot, delayed-reply handling, and restored controls after a server error. |
| Workspace repairs prevent old checkpoints from passing their frozen source-identity checks; the PowerShell demo default referenced an absent old pilot. | `scripts/run_frozen.py` verifies the original snapshot's complete source inventory, every source hash, and Python/PyTorch runtime before running the original module. The PowerShell wrapper requires explicit config/checkpoint paths and selects that launcher. Actual v4.20 inference and cached validation replay succeeded without changing frozen artifacts. PowerShell execution itself was not verified on this Linux host. |
| Parallel training did not check the full registered config/approval/code/runtime identity before starting workers. | The launcher now performs that preflight before worker dispatch. Changed protocols remain refused; existing pilot snapshots and evidence are preserved. |
| A release report could claim pass despite empty/nonboolean bucket checks, missing score buckets, incomplete checker coverage, or nonfinite rates. | The gate requires complete score/check coverage, true check values, nonempty denominators, and finite rates meeting the original thresholds. It also recognizes complete action paths rather than only their first two steps. No quality threshold was relaxed. |

## Verification

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B -m unittest discover -s tests -q
.venv/bin/python -B -m compileall -q tide_jepa tests scripts
.venv/bin/python -m pip check
node tests/demo_ui.test.js
git diff --check
```

All checks passed. The full Python suite needs local loopback binding: its initial sandbox-only run had two `PermissionError: Operation not permitted` errors when creating sockets, while all 100 baseline tests passed after granting host loopback access. The final 109-test suite passed with that access. These environmental failures were not repaired by skipping tests.

The synthetic root probes in [root-probe-results.json](root-probe-results.json) verified crash-before-best-checkpoint recovery, preserved epoch/step accounting, refusal to open release holdout after only one run, and rejection of changed corpus/review evidence. No PhoMT rows were loaded or emitted by those probes.

The actual v4.20 source-pointer seed-17 checkpoint loaded through the frozen launcher and served only at `127.0.0.1:8765`. The page was nonempty, health reported v4.20/TIDE/failed validation, and one original synthetic same-language request returned HTTP 200, valid UTF-8, `quality_status=diagnostic_only`, and `human_validated=false`. No input or generated text is retained here. The server was stopped afterward. Cached validation replay also succeeded for the frozen six-run protocol; it did not generate new evidence or change the protocol.

Visual browser verification remains unavailable on this host: `agent-browser` is not installed and the computer-use inventory contains no browsers. The attempted [agent-browser-verify skill](/home/koi/.codex/plugins/cache/openai-curated-remote/vercel/0.21.4/skills/agent-browser-verify/SKILL.md) calls for “verify the dev server with agent-browser”; that step could not run. HTTP and isolated DOM checks provide narrower evidence and do not verify layout or real-browser behavior.

PyTorch still emits its existing optional-NumPy warning on import because NumPy is absent. No tested path depends on NumPy, all tensor tests ran, and `pip check` found no broken requirements. The CPU runtime remains the pinned project runtime; no CUDA installation or GPU claim was introduced.

## Remaining quality failure

The bound [v4.20 aggregate validation report](../../VI_EN_RESULTS_V4.20_VALIDATION.md) includes 17,280 generated validation requests across six configurations, complete checker coverage, Unicode and EOS, but **0/60 bucket gates passed**. Pooled preservation was 49/8,640 for the vocabulary decoder and 39/8,640 for the source-pointer decoder. The [post-hoc component diagnostic](../../VI_EN_RESULTS_V4.20_DIAGNOSTIC.md) shows especially weak patient and predicate preservation. It is diagnostic, not new frozen-gate evidence or proof of a particular causal mechanism.

`run_suite` refuses to open the release holdout when validation fails. That refusal is expected behavior, not a training crash to suppress. Changes to source hashes also correctly refuse replay through the current package; committing edits does not restore old source hashes. Use the verified original snapshot for existing checkpoints and create a fresh reviewed protocol for new experiments.

Further linguistic improvement requires a new research iteration and fresh validation evidence; it is not established by these software repairs. The existing release holdout remains sealed, and no test loss, test generation, or suite-report artifact was created. All AI-authored/AI-reviewed results remain **preliminary, not human validated**. PhoMT action labeling/training and Phan Rang Cham training/evaluation were not performed. Private rows, checkpoints, and frozen artifacts remain Git-ignored.
