# vi-en-ai-v4.29 train checkpoint diagnostic

Preliminary AI-authored/AI-reviewed synthetic evidence; no human validation. Post-hoc train-only mechanism probe, not validation or release-gate evidence.

Scored 128 fixed train singles per checkpoint from 79 distinct groups; 16 per language/action bucket. One transition per group per bucket; buckets/languages still share groups and are correlated. Review bundle parsing includes validation rows for inventory checks, but only train rows are scored. Full corpus and holdout annotations are never opened; no text is emitted.

Sample identity: `4c58afee86c1130e938490724f4f86a51190b4efe3d66f610c757dd9c2f1bbe0`. Protocol: `d4d33cedbbec2fe53147653c4a729e12175408cff9d7fc05828fc4b4a13a02d8`.

| Run | Language | N | TF token accuracy | TF exact | Greedy exact | Greedy byte edit rate | Action | Preservation | Predicate | Wrong source ΔNLL/token | Wrong action ΔNLL/token | Zero latent ΔNLL/token |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tide-langbal-0p0-copy-0p0-seed-17 | en | 64 | 100.0% | 98.4% | 98.4% | 0.1% | 100.0% | 98.4% | 98.4% | 0.8651 | 0.8355 | 1.9691 |
| tide-langbal-0p0-copy-0p0-seed-17 | vi | 64 | 100.0% | 100.0% | 100.0% | 0.0% | 100.0% | 100.0% | 100.0% | 0.6228 | 0.4221 | 0.5122 |
| tide-langbal-1p0-copy-0p0-seed-17 | en | 64 | 99.7% | 84.4% | 84.4% | 2.0% | 89.1% | 87.5% | 87.5% | 0.9531 | 1.0310 | 2.1136 |
| tide-langbal-1p0-copy-0p0-seed-17 | vi | 64 | 100.0% | 100.0% | 100.0% | 0.0% | 100.0% | 100.0% | 100.0% | 0.6367 | 0.4268 | 0.6657 |
| tide-langbal-0p0-copy-0p0-seed-23 | en | 64 | 99.8% | 85.9% | 85.9% | 1.8% | 87.5% | 85.9% | 87.5% | 0.8125 | 1.2754 | 1.0314 |
| tide-langbal-0p0-copy-0p0-seed-23 | vi | 64 | 100.0% | 98.4% | 98.4% | 0.2% | 100.0% | 98.4% | 98.4% | 0.7182 | 0.5896 | 0.5102 |
| tide-langbal-1p0-copy-0p0-seed-23 | en | 64 | 99.9% | 92.2% | 92.2% | 1.4% | 93.8% | 92.2% | 92.2% | 0.8419 | 1.3452 | 0.8347 |
| tide-langbal-1p0-copy-0p0-seed-23 | vi | 64 | 100.0% | 98.4% | 98.4% | 0.1% | 98.4% | 98.4% | 98.4% | 0.7388 | 0.5659 | 0.6330 |
| tide-langbal-0p0-copy-0p0-seed-41 | en | 64 | 99.8% | 89.1% | 89.1% | 1.0% | 96.9% | 89.1% | 92.2% | 0.7456 | 1.1040 | 0.8384 |
| tide-langbal-0p0-copy-0p0-seed-41 | vi | 64 | 100.0% | 100.0% | 100.0% | 0.0% | 100.0% | 100.0% | 100.0% | 0.5735 | 0.5636 | 0.3941 |
| tide-langbal-1p0-copy-0p0-seed-41 | en | 64 | 99.8% | 89.1% | 89.1% | 0.6% | 98.4% | 89.1% | 95.3% | 0.8245 | 1.1852 | 1.2108 |
| tide-langbal-1p0-copy-0p0-seed-41 | vi | 64 | 99.3% | 57.8% | 57.8% | 8.0% | 95.3% | 67.2% | 79.7% | 0.5495 | 0.5769 | 0.4206 |

TF = teacher forcing with the correct reference prefix. Exactness uses one reference and can reject other valid wording; semantic rates use the frozen narrow checker. High byte accuracy can conceal whole-sentence errors. TF exactness already failing on train rules out a purely unseen-group explanation. TF exactness and greedy exactness are expected to agree when both use the same unconstrained argmax policy, since they share the first error. The free-generation byte edit rate measures error magnitude; comparison with TF byte errors alone does not establish exposure bias as the cause.

Negative controls retain the original target and correct prefix. Positive ΔNLL means that removing the corresponding signal worsened reference likelihood. Source controls replace the source with another group's source from the same language/action bucket. Action controls use a licensed opposite value of the same action kind. Zero-latent controls keep source memory. These deliberately mismatched inputs are mechanism probes, not quality scores or evidence of JEPA benefit. Different controls can have different scales.

Elapsed CPU wall time: 105.4s with one Torch thread. No training, checkpoint selection, or frozen-protocol mutation occurred.
