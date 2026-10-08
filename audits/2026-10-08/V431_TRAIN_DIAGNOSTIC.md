# vi-en-ai-v4.31 train checkpoint diagnostic

Preliminary AI-authored/AI-reviewed synthetic evidence; no human validation. Post-hoc train-only mechanism probe, not validation or release-gate evidence.

Scored 128 fixed train singles per checkpoint from 80 distinct groups; 16 per language/action bucket. One transition per group per bucket; buckets/languages still share groups and are correlated. Review bundle parsing includes validation rows for inventory checks, but only train rows are scored. Full corpus and holdout annotations are never opened; no text is emitted.

Sample identity: `104ea95f059b5558f900b441df565176eec8e9aeeb5b7127ba1983893118b7d1`. Protocol: `a34113c4f74b804d50120c7472a9dbf1f10c5329542293c5f43eb6b14f1215e5`.

| Run | Language | N | TF token accuracy | TF exact | Greedy exact | Greedy byte edit rate | Action | Preservation | Predicate | Wrong source ΔNLL/token | Wrong action ΔNLL/token | Zero latent ΔNLL/token |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tide-copy-0p0-seed-17 | en | 64 | 99.7% | 82.8% | 82.8% | 1.5% | 100.0% | 82.8% | 98.4% | 0.8920 | 1.0471 | 1.6624 |
| tide-copy-0p0-seed-17 | vi | 64 | 100.0% | 98.4% | 98.4% | 0.1% | 100.0% | 98.4% | 98.4% | 0.6211 | 0.5799 | 0.4936 |
| token_only-copy-0p0-seed-17 | en | 64 | 100.0% | 100.0% | 100.0% | 0.0% | 100.0% | 100.0% | 100.0% | 1.1461 | 1.0217 | 0.3416 |
| token_only-copy-0p0-seed-17 | vi | 64 | 100.0% | 100.0% | 100.0% | 0.0% | 100.0% | 100.0% | 100.0% | 0.7232 | 0.4347 | 0.1459 |
| tide-copy-0p0-seed-23 | en | 64 | 99.8% | 89.1% | 89.1% | 1.2% | 100.0% | 89.1% | 100.0% | 0.8018 | 1.0839 | 0.4492 |
| tide-copy-0p0-seed-23 | vi | 64 | 99.8% | 87.5% | 87.5% | 1.4% | 89.1% | 87.5% | 89.1% | 0.7065 | 0.5785 | 0.5067 |
| token_only-copy-0p0-seed-23 | en | 64 | 99.3% | 67.2% | 67.2% | 3.4% | 96.9% | 67.2% | 82.8% | 1.0231 | 0.8468 | 0.4542 |
| token_only-copy-0p0-seed-23 | vi | 64 | 99.9% | 95.3% | 95.3% | 0.2% | 95.3% | 95.3% | 95.3% | 0.8075 | 0.4689 | 0.1855 |
| tide-copy-0p0-seed-41 | en | 64 | 99.5% | 76.6% | 76.6% | 2.1% | 93.8% | 78.1% | 87.5% | 0.9232 | 0.9339 | 1.6587 |
| tide-copy-0p0-seed-41 | vi | 64 | 99.8% | 87.5% | 87.5% | 1.7% | 100.0% | 87.5% | 98.4% | 0.6584 | 0.5373 | 0.4023 |
| token_only-copy-0p0-seed-41 | en | 64 | 99.9% | 92.2% | 92.2% | 0.5% | 100.0% | 92.2% | 93.8% | 0.9962 | 0.7385 | 0.3492 |
| token_only-copy-0p0-seed-41 | vi | 64 | 100.0% | 100.0% | 100.0% | 0.0% | 100.0% | 100.0% | 100.0% | 0.7564 | 0.4701 | 0.1084 |

TF = teacher forcing with the correct reference prefix. Exactness uses one reference and can reject other valid wording; semantic rates use the frozen narrow checker. High byte accuracy can conceal whole-sentence errors. TF exactness already failing on train rules out a purely unseen-group explanation. TF exactness and greedy exactness are expected to agree when both use the same unconstrained argmax policy, since they share the first error. The free-generation byte edit rate measures error magnitude; comparison with TF byte errors alone does not establish exposure bias as the cause.

Negative controls retain the original target and correct prefix. Positive ΔNLL means that removing the corresponding signal worsened reference likelihood. Source controls replace the source with another group's source from the same language/action bucket. Action controls use a licensed opposite value of the same action kind. Zero-latent controls keep source memory. These deliberately mismatched inputs are mechanism probes, not quality scores or evidence of JEPA benefit. Different controls can have different scales.

Elapsed CPU wall time: 75.9s with one Torch thread. No training, checkpoint selection, or frozen-protocol mutation occurred.
