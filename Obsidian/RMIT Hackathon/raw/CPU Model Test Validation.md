# CPU model-test validation — 2026-09-28

> Source: direct command output from the project workspace after creating an ignored `.venv` and installing the official PyTorch CPU wheel.
> Status: Current verification for the present code snapshot; rerun after code changes.

## Environment

- Python 3.11 virtual environment at project-local `.venv` (ignored by Git).
- `torch 2.14.0+cpu` installed from `https://download.pytorch.org/whl/cpu`.
- `torch.cuda.is_available()` returned `False`; this is a CPU-only runtime.
- PyTorch emitted a warning that optional NumPy integration could not initialize because NumPy is not installed. The exercised tests did not use NumPy.

## Results

- Import/tensor smoke check: passed; `torch.rand(1)` produced a tensor.
- `python -m unittest discover -s tests -v` using `.venv`: **13 tests passed, 0 skipped, 0 failures**.
- `python -m compileall -q tide_jepa tests` using `.venv`: passed.

## Limits

This verifies covered synthetic schema/model/training behavior on CPU only. It does not verify GPU execution/performance, any language outputs, corpus rights, semantic correctness, benchmark results, or the research hypothesis.
