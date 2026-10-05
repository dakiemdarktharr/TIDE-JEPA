# v4.14 TIDE objective implementation audit

This is an engineering diagnosis of the completed v4.14 preliminary synthetic pilot, not a new quality evaluation. No raw source/target rows or private generated output are included.

## Loss construction

`token_only` suppresses latent JEPA/alignment/variance/path-state terms. It still receives the matched source-copy term and supervised composed-path token loss, so the control is an action-conditioned supervised generator without the latent objective terms, not an unconditioned language model. TIDE adds `jepa`, `alignment`, `variance`, `path_jepa`, and `path_alignment` terms. The shared decoder token, source-copy, and path-token losses are trained in both conditions.

Checkpoint selection is matched across modes using only validation decoder loss: token CE + weighted path-token CE + weighted source-copy CE. The TIDE latent terms are excluded from selection, so TIDE checkpoints were not selected to minimize their own auxiliary objective. This is implemented in `tide_jepa/experiment.py` and `tide_jepa/training.py`.

At the selected checkpoints, the logged validation TIDE-specific terms contributed 32.8%, 40.3%, and 41.0% of the weighted total loss for seeds 17, 23, and 41 respectively. This scalar share is descriptive; it is not a proxy for gradient contribution.

## Bounded gradient probe

Using each selected TIDE checkpoint, one deterministic training batch with 80 edges and eight paths was used to compare the weighted shared decoder losses (`token + source-copy + path-token`) with the weighted TIDE-specific terms. No record text was printed or retained by the diagnostic.

| Seed | Shared decoder gradient norm | TIDE-term gradient norm | Combined norm | Cosine, decoder vs TIDE | Clip threshold |
|---:|---:|---:|---:|---:|---:|
| 17 | 0.300 | 0.067 | 0.309 | 0.027 | 1.0 |
| 23 | 0.200 | 0.086 | 0.223 | 0.070 | 1.0 |
| 41 | 0.450 | 0.157 | 0.507 | 0.213 | 1.0 |

None of these three batches reached the 1.0 global clipping threshold, and TIDE-term gradient norms were below the shared decoder norms. The low positive cosine values indicate that the auxiliary gradient directions were mostly distinct from the shared decoder gradient on these batches, without showing strong opposition. This is a single-batch-per-seed probe at selected checkpoints; it does not characterize training-time variation or prove that reducing the auxiliary coefficient would improve preservation.

## Next diagnostic

Keep v4.14 unchanged and keep its release holdout sealed. A follow-up may compare the existing TIDE auxiliary coefficient with a preregistered lower coefficient alongside the matched `token_only` control on a fresh independently reviewed corpus/split, with the architecture, updates, seeds, and quality thresholds fixed. The coefficient should scale only the five TIDE-specific terms; shared source-copy and path-token supervision must remain identical. This will test whether lower latent-objective pressure improves preservation without tuning on v4.14 validation groups. Any result remains preliminary and AI-reviewed only.
