# First implementation milestone — source record

> Source: completion report from `heavy` and independent initial/recheck reports from `review`, received 2026-09-28; current workspace files listed below.
> Record type: concise extraction of worker reports and validation results.
> Status: Current source record for this milestone; later changes require a new dated record.

## Implementation delivered

- Root files: `README.md`, `tide_jepa_spec.md`, `.gitignore`.
- Package: `tide_jepa/__init__.py`, `config.py`, `schema.py`, `model.py`, `training.py`.
- Tests: `tests/test_schema.py`, `tests/test_model.py`.
- Existing prospectus drafts were marked historical; the research note remains background; the annotation protocol was framed as a Vietnamese–English component with a Phan Rang Cham validation gate.
- Implementation is data-agnostic. It contains original attention/encoder components, a typed action predictor, frozen EMA target, causal decoder/generation path, batch validation, trainer, and objective modes. No Cham grammar, tokenizer, action inventory, or sample text is assumed.
- Current experimental scope uses within-language action edges with cross-language paired supervision. Cross-language source-to-target translation edges, composed paths, corpus ingestion/splits, and matched-compute experiments are not implemented.

## Verification reported

- `python -m unittest discover -s tests -v`: 13 discovered; 4 passed; 9 skipped because PyTorch is absent from the available Python environment.
- `python -m compileall -q tide_jepa tests`: passed.
- No software installed, dataset downloaded, or third-party model/code reused.
- Tensor/model runtime therefore remains unverified.

## Review finding and resolution

Review found a P2 mismatch: training batch validation did not ensure the decoder's initial token matched the BOS used at inference. Heavy added validated `ModelConfig.bos_id`, required each decoder row to start with it, rejected conflicting generation BOS, and added regression tests. Review rechecked `config.py`, `training.py`, `model.py`, and test cases and marked the finding resolved. Review reported no additional high-severity finding for this milestone.
