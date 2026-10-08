# vi-en-ai-v4.32 train checkpoint diagnostic

Preliminary AI-authored/AI-reviewed synthetic evidence; no human validation. Post-hoc train-only mechanism probe, not validation or release-gate evidence.

Scored 512 fixed train singles per checkpoint from 112 distinct groups; 64 per language/action bucket. One transition per group per bucket; buckets/languages still share groups and are correlated. Review bundle parsing includes validation rows for inventory checks, but only train rows are scored. Full corpus and holdout annotations are never opened; no text is emitted.

Sample identity: `ea46fa777ef921c20b8a393b9ded2683ff25d2614756f05655d7c5198748ff35`. Protocol: `c288e9749402282ff27f2279e33ad13b58ee6c96612695ba41711bffcd5b0524`.

| Run | Language | N | TF token accuracy | TF exact | Greedy exact | Greedy byte edit rate | Action | Preservation | Predicate | Wrong source ΔNLL/token | Wrong action ΔNLL/token | Zero latent ΔNLL/token |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tide-decoder-vocabulary-copy-0p0-seed-17 | en | 256 | 99.7% | 85.2% | 85.2% | 1.4% | 97.7% | 86.3% | 90.6% | 1.0768 | 0.9714 | 0.9238 |
| tide-decoder-vocabulary-copy-0p0-seed-17 | vi | 256 | 99.9% | 94.1% | 94.1% | 0.7% | 96.9% | 95.7% | 97.3% | 0.6973 | 0.5751 | 1.1089 |
| tide-decoder-source_pointer-copy-0p0-seed-17 | en | 256 | 99.0% | 55.9% | 55.9% | 5.0% | 84.4% | 60.2% | 75.4% | 2.3657 | 1.0574 | 3.9801 |
| tide-decoder-source_pointer-copy-0p0-seed-17 | vi | 256 | 100.0% | 97.7% | 97.7% | 0.4% | 99.2% | 98.8% | 99.2% | 2.6523 | 0.4855 | 1.7488 |
| tide-decoder-vocabulary-copy-0p0-seed-23 | en | 256 | 98.9% | 55.9% | 55.9% | 5.3% | 77.3% | 57.8% | 66.8% | 0.8914 | 1.3564 | 0.7501 |
| tide-decoder-vocabulary-copy-0p0-seed-23 | vi | 256 | 99.9% | 94.1% | 94.1% | 1.1% | 96.1% | 97.3% | 98.4% | 0.6665 | 0.6107 | 0.8085 |
| tide-decoder-source_pointer-copy-0p0-seed-23 | en | 256 | 99.0% | 56.6% | 56.6% | 6.4% | 78.1% | 60.2% | 68.8% | 2.3277 | 1.2739 | 1.6272 |
| tide-decoder-source_pointer-copy-0p0-seed-23 | vi | 256 | 100.0% | 97.7% | 98.0% | 0.2% | 99.6% | 98.0% | 99.2% | 2.5580 | 0.6835 | 2.0860 |
| tide-decoder-vocabulary-copy-0p0-seed-41 | en | 256 | 98.8% | 50.4% | 50.4% | 5.7% | 87.5% | 53.1% | 72.7% | 0.9265 | 1.1506 | 1.4184 |
| tide-decoder-vocabulary-copy-0p0-seed-41 | vi | 256 | 99.9% | 96.1% | 96.1% | 0.4% | 99.6% | 96.5% | 98.8% | 0.5818 | 0.5764 | 0.3185 |
| tide-decoder-source_pointer-copy-0p0-seed-41 | en | 256 | 99.4% | 69.5% | 69.5% | 2.8% | 89.8% | 70.3% | 82.8% | 2.8019 | 1.0264 | 3.2910 |
| tide-decoder-source_pointer-copy-0p0-seed-41 | vi | 256 | 100.0% | 99.6% | 99.6% | 0.0% | 99.6% | 99.6% | 99.6% | 3.1909 | 0.6437 | 2.1689 |

TF = teacher forcing with the correct reference prefix. Exactness uses one reference and can reject other valid wording; semantic rates use the frozen narrow checker. High byte accuracy can conceal whole-sentence errors. TF exactness already failing on train rules out a purely unseen-group explanation. TF exactness and greedy exactness are expected to agree when both use the same unconstrained argmax policy, since they share the first error. The free-generation byte edit rate measures error magnitude; comparison with TF byte errors alone does not establish exposure bias as the cause.

Negative controls retain the original target and correct prefix. Positive ΔNLL means that removing the corresponding signal worsened reference likelihood. Source controls replace the source with another group's source from the same language/action bucket. Action controls use a licensed opposite value of the same action kind. Zero-latent controls keep source memory. These deliberately mismatched inputs are mechanism probes, not quality scores or evidence of JEPA benefit. Different controls can have different scales.

Elapsed CPU wall time: 320.9s with one Torch thread. No training, checkpoint selection, or frozen-protocol mutation occurred.
