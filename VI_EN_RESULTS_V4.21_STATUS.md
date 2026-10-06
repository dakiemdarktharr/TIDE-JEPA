# v4.21 pilot status — evaluator coverage invalidated; holdout sealed

v4.21 is a fresh AI-authored and AI-reviewed English–Vietnamese synthetic pilot. Reviews and adjudication were AI-only and preliminary; `human_validated=false`. PhoMT was not used, and Phan Rang Cham remains excluded.

## Frozen evidence and run outcome

The draft contains 15,360 records across 192 event combinations, split by whole event groups 112/40/40. Two independent Luna reviewers approved the exact corpus; one recorded a nonblocking punctuation-style limitation retained in adjudication. Draft, approved corpus, split and frozen protocol identities are recorded below. The protocol registered 12 fixed-final-epoch TIDE runs: source-copy weights 0/1.5 crossed with vocabulary/source-pointer decoders across seeds 17/23/41.

- Draft SHA-256: `edd6c1e2a92adace02ca280faa68548c2cf9d520fa6f9b5c130cc8a5c36ca12d`
- Approved corpus SHA-256: `f5153214e5dcf991dc585b679f0354c9cab33b0bd6b3b545413f659524e05c48`
- Split SHA-256: `b5244e30e9778829f206058dea726b53e4c1409860ded7730aa4ab4df25c746e`
- Frozen protocol SHA-256: `5b48e8348c2ef3fc1a4db9841c713560fd7bc24bbbd57a67691884f87e33d7de`

All 12 runs completed the registered 29 epochs / 3,248 updates, and validation-only generation completed. However, the frozen evaluator omitted `FAMILIES_V421` from its semantic checker registry. The report therefore has zero semantic checker coverage (unscored `0/0` denominators) across its buckets. This is an invalid evaluator result, not a model-quality score; its quality gate failed closed. The release holdout was not evaluated and remains sealed. See the [aggregate validation report](VI_EN_RESULTS_V4.21_VALIDATION.md).

We preserved the corpus, protocol, checkpoints and validation artifacts as diagnostic evidence. We did not rescore the old runs with the repaired checker, because doing so would change the frozen implementation identity. The checker registration now has a regression test for v4.21; a fresh corpus, reviews, protocol and holdout are being prepared as v4.22. No linguistic-quality or TIDE-advantage claim follows from v4.21.

## Reproduction record

The original frozen run can be audited with the identity records in ignored `data/pilot/vi-en-ai-v4.21/` and `runs/vi-en-ai-v4.21/`. Do not reopen the release holdout. Any new experiment must use a separately reviewed and frozen version. All row-level corpus, review and generated-text artifacts remain in Git-ignored paths; public reports contain aggregate evidence only.
