# v4.30 status: source-pointer preservation replication

**State:** six frozen CPU runs completed and validation-only evaluation completed. The frozen report recorded a quality-gate failure: 1/6 configurations and 29/60 seed-by-bucket checks passed. The release holdout remains sealed, and no checkpoint is approved for usable language output.

**Measurement limitation:** a later train-only negative-control audit found that the frozen semantic checker accepts all 1,792 Vietnamese present-progressive references even after deleting `đang`. It accepted all 7,168 intact train singles, so ordinary reference coverage did not reveal this defect. The original report and run identities remain unchanged; the reported gate is historical evidence from an invalidly permissive checker and cannot be treated as confirmatory quality evidence. The repaired workspace checker accepts all 7,168 intact references and rejects all 1,792 progressive deletions. A fresh reviewed protocol is required for confirmatory scoring. See [checker and research-workflow evidence](RESEARCH_ACCELERATION.md) and [Linux validation record](audits/2026-10-07/RESEARCH_VALIDATION.md).

All six runs completed 29 epochs / 3,248 updates. Frozen protocol, approval, source/runtime/configuration identities, and checkpoint consistency were verified. Validation generated 17,280 examples; Unicode, EOS, and checker coverage were complete under the frozen checker. The release holdout was not opened. Post-hoc rescoring and role diagnostics remain explicitly diagnostic; they do not repair the frozen gate.

The project-authored synthetic pilot has only preliminary AI review, not human or native-speaker validation. PhoMT was not used. Phan Rang Cham remains excluded pending dataset-use permission and language/community review.

## Motivation and registered hypothesis

v4.29 had a high-quality checker but failed its frozen validation gate, chiefly through English single-action preservation weakness. v4.30 compared vocabulary and source-pointer decoders at fixed TIDE objective and source-copy weight 0, testing whether a pointer decoder could improve preservation without reducing action fidelity by more than five percentage points. The pointer decoder adds computation, so the comparison made no matched-FLOP claim. This was a fresh split, not reuse of earlier exposed holdouts.

The matrix crossed decoders `vocabulary` and `source_pointer` with seeds 17/23/41. Settings were TIDE, source-copy weight 0, language-balance weight 0, width 64, four heads, two layers, 29 epochs, batch 80, learning rate 0.001, and fixed-final-epoch selection. Reviewer A approved; reviewer B's questions about duplicate weighting and English tense forms were adjudicated before freeze. Generation scoring creates single-action requests from standalone rows and one composed request per path; exact path-edge copies are not scored twice as single-action examples. Validation token CE remains row-weighted, and path-linked training rows contribute additional row-wise training exposure. The original checker defect was discovered after the protocol froze.

## Integrity, results, and reproduction

All six registered runs finished. Run records match the frozen protocol and source/runtime/configuration identities; `latest.pt` and `best.pt` are consistent, and there are no release-test generation or metric artifacts. Validation-only generation completed. The original aggregate tables and all private rows/checkpoints remain under Git-ignored `data/` and `runs/`.

The frozen validation report is [VI_EN_RESULTS_V4.30_VALIDATION.md](VI_EN_RESULTS_V4.30_VALIDATION.md). Its measured gate is 1/6 complete configurations and 29/60 seed-by-bucket checks, but the checker limitation above makes this result non-confirmatory. The [post-hoc role diagnostic](VI_EN_RESULTS_V4.30_DIAGNOSTIC.md) reports the repaired checker against saved generations; the [action-sensitivity diagnostic](VI_EN_RESULTS_V4.30_ACTION_SENSITIVITY.md) measures output changes, not correctness. Neither opens the holdout.

Reproduce checker evidence without emitting examples:

```sh
.venv/bin/python -B scripts/audit_research_checker.py data/pilot/vi-en-ai-v4.29 --output /tmp/checker-v429.json
.venv/bin/python -B scripts/audit_research_checker.py data/pilot/vi-en-ai-v4.30 --output /tmp/checker-v430-frozen.json
.venv/bin/python -B scripts/audit_research_checker.py data/pilot/vi-en-ai-v4.30 --implementation workspace --output /tmp/checker-v430-repaired.json
```

The first and third commands pass; the second exits 1 by design to reproduce the frozen v4.30 defect. Release holdout access remains gated on a fresh valid frozen validation study that passes every pre-registered bucket.
