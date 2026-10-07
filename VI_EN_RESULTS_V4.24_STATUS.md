# v4.24 status — validation gate failed; release holdout sealed

v4.24 is a preliminary AI-authored and independently AI-reviewed English–Vietnamese synthetic pilot. Two independent Luna high reviews approved the exact 15,360-record draft (draft SHA-256 `e124f25ee7409a2bd492707669edbeb84beb626a8d832417dccec109934b54c5`); the review artifacts are bound locally to that draft. `human_validated=false`; PhoMT and Phan Rang Cham were not used.

## Frozen protocol and run audit

- Approved corpus SHA-256: `e00276e5cc0e7f7cfa929a62bd6704225d4e835f2866e4109ccf8a98e6082afb`
- Split-manifest SHA-256: `800d8934605c648f4a2190e1f9faaad0dceac0781d19761812a58940b5c5607d`
- Protocol SHA-256: `9939b50d2cdb9bd8099724baa4a6a2f2f875e003b3484efc3dfadb60d7df346f`
- The new 112/40/40 group split uses 192 event groups, balanced three-agent/eight-verb/eight-patient factors, four surface realizations per state, and 7,680 path-alignment pairs. Path template sharing across partitions is disclosed; this does not establish template- or domain-generalization.
- Six primary TIDE runs crossed source-copy weights 0/1.5 and seeds 17/23/41, using the vocabulary decoder, 29 fixed-final epochs, and 3,248 updates per checkpoint. All six config hashes, current implementation/runtime identities, approval hash, final checkpoint epochs/steps, and saved validation-report identities matched the frozen protocol. Each `best.pt` and `latest.pt` had identical model tensors.
- Validation-only generation completed for all six configs: 2,880 examples per config (17,280 total) across ten language/task/action buckets. No release-test generation or test metrics were produced. The suite stopped at the frozen validation gate before scoring test targets.

## Validation outcome

The frozen gate failed for **all six configurations**; only 28/60 individual seed-by-bucket checks passed. Unicode validity, EOS termination, and checker coverage were each 17,280/17,280 (100%). Aggregate action fidelity was 16,492/17,280 (95.4%), preservation 14,445/17,280 (83.6%), accepted-reference match 14,219/17,280 (82.3%), and weighted character error rate 1.73%. These pooled descriptive metrics do not replace the frozen per-bucket requirements: 90% fidelity and preservation for each single-action bucket, and 80% for each held-out-path bucket.

English `TIME:NOW` preservation was below 90% in all six configs (range 54.4–89.7%). English `POLARITY:POSITIVE` failed preservation in four configs; the other English single-action buckets also varied by seed and source-copy weight. Vietnamese single-action preservation failed in three of six configs for each action bucket. Held-out-path preservation failed in two English configs and one Vietnamese config. The copy-weight condition did not produce a stable all-bucket pass. See the [aggregate validation report](VI_EN_RESULTS_V4.24_VALIDATION.md).

The release holdout contains 3,200 records and remains sealed. No test artifact exists. No checkpoint is approved for a user-facing language demo; the existing offline interface must remain explicitly diagnostic-only.

## Post-hoc diagnosis and run-log limitation

The saved validation generations changed for 99.8–100% of same-source pairs with distinct requested actions. This argues against the model simply ignoring the action input, but it does not establish that the requested action or the source event was preserved. A component rescore found agent and place retention near ceiling, while patient and predicate retention were lower, especially for English and for the source-copy 1.5 condition. These are diagnostics from the narrow synthetic checker, not human language evaluation. See the [component diagnostic](VI_EN_RESULTS_V4.24_DIAGNOSTIC.md) and [action-sensitivity diagnostic](VI_EN_RESULTS_V4.24_ACTION_SENSITIVITY.md).

The training CSV logs in three run directories contain duplicate, conflicting epoch/split rows (copy-0 seed 17, copy-1.5 seed 17, and copy-1.5 seed 41). Checkpoint identity and final model tensors agree, but those CSVs cannot support epoch-curve or train/validation-loss claims. The runner's resume reconciliation accepted duplicate rows; it now rejects duplicate or missing rows. The preserved v4.24 artifacts were not edited. This logging anomaly is recorded as a partial crash-recovery/audit issue; future runs use a fresh version and the corrected guard.

These results are preliminary synthetic AI evidence only. No threshold was changed after evaluation. The failed result does not establish natural-language efficacy or human/native-speaker quality, and no v4.24 holdout will be used for tuning.
