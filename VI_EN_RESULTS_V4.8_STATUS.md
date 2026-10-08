# v4.8 training status — paused

Status captured 2026-10-02 20:16 Asia/Saigon, after the user requested stopping the active training run. This is an aggregate engineering status note, not an evaluation report. The synthetic corpus and all model checkpoints remain local under Git-ignored `data/` and `runs/`.

## Frozen preliminary pilot

`vi-en-ai-v4.8` is an AI-authored, independently AI-reviewed synthetic English–Vietnamese pilot. Review and adjudication are preliminary AI evidence; `human_validated` is false. The frozen corpus has 7,680 records across 192 event/action combinations, with 112/40/40 groups and 4,480/1,600/1,600 records in train/validation/release holdout. The release holdout has not been opened.

The frozen protocol specifies four controls (`token_only`, `generic_jepa`, `static_alignment`, `tide`), seeds 17, 23 and 41, 58 epochs, width 48, four heads, two layers, batch size 80, learning rate 0.001, maximum length 192 and source-copy weight 0.5. All four seed-17 configurations completed 58 epochs. The runner was interrupted by the user while seed 23 was in progress.

## Training state after workers stopped

The parent runner and all four worker processes were confirmed stopped. All eight run directories have `latest.pt` and `best.pt`; `latest.pt` metadata and SHA-256 values are recorded here to support later local transfer and verification.

| Mode | Seed | State | Epoch | Steps | `latest.pt` SHA-256 |
|---|---:|---|---:|---:|---|
| generic_jepa | 17 | complete | 58/58 | 3,248 | `18260f01685c25b8fb3cd3011c6b21cbf372ef113f2a43c792564c8a5333c9dc` |
| static_alignment | 17 | complete | 58/58 | 3,248 | `392d645ffcd932dffac3360712d0e18b1321470e5d2333515325c15412076fcd` |
| tide | 17 | complete | 58/58 | 3,248 | `6a5eb9e9dfe4ee6677c3582d963f3ffbbb436d99d86bfcc9602cb19b82b6de4a` |
| token_only | 17 | complete | 58/58 | 3,248 | `affc3de521bf7f49efa0c91717baa76395cc36974034a7c02524a037ace350b2` |
| generic_jepa | 23 | interrupted | 8/58 | 448 | `1259e41bed4b2fda497a7501f8d0e678eb3175f30d01bb32af6a87bb24883167` |
| static_alignment | 23 | interrupted | 8/58 | 448 | `ae93970425162dab9e2fb82b1bdbb78ea7dd442e10fadacdd91f9ad0e7eddcc5` |
| tide | 23 | interrupted | 7/58 | 392 | `d0665b4f0e957ae131bd4cfa653e3681a6c0a648b5a0de5284c0acfe6c5233d6` |
| token_only | 23 | interrupted | 15/58 | 840 | `dc48939a908def2149c82f9cf3ffe4e3eeee4e10e14aa00bdc2c4a382c91edbc` |

Seed 41 has not started. Thus, four of 12 configurations are complete, four are partial and four have not started. The training-only runner did not create `suite_report.json`; no evaluation was performed after the interruption. Validation has not been scored, and the release holdout remains sealed. No current v4.8 neural quality result is available.

## Frozen artifact identity

The following hashes were computed from the local frozen files after training stopped. Hashes identify files but do not contain or publish their rows.

| File under `data/pilot/vi-en-ai-v4.8/` | SHA-256 |
|---|---|
| `approval.json` | `b6cee5546625fa0a78f23723ccb110e1263b655e55a939d31ed3e54871e0efc4` |
| `protocol.json` | `ca31c4bca9877c7901358e5668c657d38e1892ed3bb69d6dbe7dbd372d771232` |
| `corpus.jsonl` | `ba112eea7963a541c8e359a7f81f45a1a96c7053566539b1496930f78b8764d4` |
| `alignments.json` | `5adc713bcfd9c39df4b73219d6dee6184b15b2ee702a07bb98f4bc61d6f8c215` |
| `inventory.json` | `b5d3532da2de6423e3beafd8fa8a5fd4af3c42e953bdd769c859f869cd1f66d4` |
| `semantic_frames.json` | `32350a6651c42a39bb5baf7eda9715e726a1dd9340dbea45b3ff638ee5f4675d` |
| `split_manifest.json` | `3c2cc83e0eb6524f65d82a934f70ac8341343745ce3bf8593482998ee23c904d` |

## Handoff and next action

The source snapshot is pushed to GitHub at commit `ed4f65c4f0c8268487a2afdd0d69fa7c2812a962`. The corpus, reviews, approval/protocol files, run logs and checkpoints are Git-ignored and were not pushed. To resume this exact pilot, transfer the required non-PhoMT v4.8 artifacts and run directories locally, verify the hashes above, then run the frozen training runner, which resumes from each `latest.pt`. Do not copy PhoMT raw/derived rows to GitHub or include any dataset rows in reports.

After all 12 runs finish and all workers stop, evaluate validation only. Open the sealed release holdout only if the frozen validation gate passes. If it fails, preserve this version as development evidence and use a new version with a new holdout. Phan Rang Cham remains disabled pending data-use permission and language/community review.

## 2026-10-09 Linux handoff recheck

The v4.8 data and run directories are present on lattice. All seven frozen corpus/protocol/approval hashes above and all eight recorded `latest.pt` checkpoint hashes match the local files; all eight runs also have `best.pt`. No v4.8 trainer process was found running. Resume was not attempted: the frozen protocol and checkpoint identities record Python 3.11.9 on Windows, while lattice uses Python 3.11.17 on Arch Linux, and the runner binds Python/PyTorch runtime identity into the run identity. The runtime mismatch therefore requires preserving v4.8 as paused evidence; do not bypass its guard. No v4.8 validation or release-holdout evaluation has occurred. v4.33 is the later active synthetic pilot and remains diagnostic-only pending external language-quality gates.
