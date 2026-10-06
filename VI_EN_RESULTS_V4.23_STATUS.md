# v4.23 status — validation gate failed; release holdout sealed

v4.23 is an AI-authored, independently AI-reviewed preliminary English–Vietnamese synthetic pilot. Two independent Luna reviewers approved all 15,360 records, bound to the exact draft and reviewed-artifact hashes; AI adjudication followed. `human_validated=false`. PhoMT and Phan Rang Cham were not used.

## Frozen protocol and run audit

- Draft SHA-256: `7592f6c9090345a791e3218c2572114a9c8869e9abbc5c30e2d779e7357d33ea`
- Approved corpus SHA-256: `75bfc6c794a879a972f0fcb1f0d16ceed70bfa063fc179ac10354018994c2adc`
- Split SHA-256: `878afe2917e26a0ea2164ff953f31427f00a2adf7c7fdb8c1227abdd0416b69d`
- Protocol SHA-256: `0ad11b544e6884660484d0796b77de01f12335bb6afbc9344cd23a959c9fc14b`
- The frozen study crossed source-copy weights 0/1.5 with vocabulary/source-pointer decoders over seeds 17/23/41: 12 TIDE runs, 29 fixed epochs, 3,248 updates per run. Copy loss was computed in every cell. Checkpoint selection was fixed to the final epoch.
- All 12 configs, source/runtime identities, resolved run hashes, checkpoint identities and 29-epoch metric histories passed the pre-validation audit. No validation/test generation existed before the validation-only command.

## Validation outcome

Checker coverage was complete, but the quality gate failed: **0/120** frozen seed-by-bucket checks passed. Unicode validity and EOS termination were both 100%. Across seeds, pooled action fidelity by copy-weight/decoder cell was 43.1% (0/vocabulary), 44.1% (0/source-pointer), 45.6% (1.5/vocabulary), and 38.1% (1.5/source-pointer). Pooled preservation was 6.2%, 10.6%, 9.1%, and 17.7%, respectively. Frozen per-bucket thresholds are 90% for single-action fidelity/preservation and 80% for held-out-path fidelity/preservation; pooled figures are descriptive and do not replace those checks. Source-copy weight improved pooled preservation descriptively for the source-pointer decoder but reduced action fidelity; neither factor combination met the gate. These pooled figures are descriptive over three seeds, not population-level claims. See the [aggregate validation report](VI_EN_RESULTS_V4.23_VALIDATION.md).

Because validation failed, the release holdout was not evaluated. No `test_metrics.json` or suite/test report exists; the test split remains sealed. All examples and generations remain private in Git-ignored `data/` and `runs/`. The result is preliminary synthetic evidence only and establishes neither natural-language efficacy nor human linguistic quality.
