# Vi–En v4.8 training pause — 2026-10-02

At the user's request, the active training parent and its four worker processes were stopped at 2026-10-02 20:16 Asia/Saigon. Process inspection confirmed no trainer process remained. This note records only aggregate metadata and hashes; it contains no corpus rows or generated text.

Four of 12 frozen configurations completed all 58 epochs / 3,248 steps (the four controls at seed 17). Four configurations at seed 23 were interrupted at epochs 8, 8, 7 and 15 respectively. Seed 41 did not start. Each existing run directory had `latest.pt` and `best.pt`. Checkpoint SHA-256 values and frozen v4.8 artifact identities are in [VI_EN_RESULTS_V4.8_STATUS.md](../../../VI_EN_RESULTS_V4.8_STATUS.md).

No v4.8 suite report was created and no validation or release-holdout evaluation was run. The release holdout remains sealed. The frozen corpus, approvals, protocol, reviewer records and checkpoints remain under Git-ignored `data/` and `runs/`; none were pushed. Source status is recorded in commit `ed4f65c4f0c8268487a0afdd0d69fa7c2812a962`, with the pause update in the following commit.
