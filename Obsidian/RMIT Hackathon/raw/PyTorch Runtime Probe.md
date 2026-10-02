# PyTorch runtime probe — 2026-09-28

> Source: commands run from the project workspace on 2026-09-28.
> Status: Current environment evidence only; recheck if Python/dependencies change.

## Runtimes checked

- Python 3.11.9: `importlib.util.find_spec('torch')` returned false; direct `import torch` raised `ModuleNotFoundError`.
- Python 3.9.13 and bundled Python 3.12.14: `find_spec('torch')` returned false.
- Windows Store Python 3.13.14: `find_spec('torch')` returned true, but `import torch` failed with `ImportError: DLL load failed while importing _C: The specified module could not be found.`

## Commands and outcomes

- `py -3.13 -c "import torch; print('torch', torch.__version__); print('cuda_available', torch.cuda.is_available())"` — failed at import with the DLL error above.
- `py -3.13 -m unittest discover -s tests -v` — 4 schema tests passed; loading `test_model` errored during `import torch`; no model tensor tests ran.
- Inspected the Python 3.13 `site-packages/torch` directory: `_C.cp313-win_amd64.pyd` is present, but there is no `torch/lib` directory/bundled native library set. `py -3.13 -m pip show torch` reports `Package(s) not found: torch`.
- No package installation, download, or system configuration change was attempted.

## Conclusion

The Python 3.13 Torch files are not a usable runtime. On the available standard Python 3.11 runtime, model tests skip because Torch is absent. Tensor execution and model behavior remain unverified until a valid PyTorch runtime is provided or installed in an approved project environment.
