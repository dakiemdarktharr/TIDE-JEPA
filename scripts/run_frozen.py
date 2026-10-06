"""Run a pilot with its verified original source snapshot and runtime.

Preserves checkpoint identities after workspace repairs. This does not rebind
or modify any protocol, checkpoint, corpus, or evaluation evidence.
"""

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import runpy
import sys


def verify_snapshot(directory):
    base = Path(directory).resolve()
    protocol = json.loads((base / "protocol.json").read_text(encoding="utf-8"))
    snapshot = (base / protocol["implementation_snapshot"]).resolve()
    if snapshot == base or not snapshot.is_relative_to(base):
        raise ValueError("implementation snapshot must be inside the pilot directory")
    expected = protocol.get("implementation_sha256", {})
    if not expected or "__init__.py" not in expected:
        raise ValueError("protocol lacks a complete implementation snapshot identity")
    for name, digest in expected.items():
        if Path(name).name != name or Path(name).suffix not in {".py", ".html"}:
            raise ValueError("snapshot identity contains an invalid source filename")
        source = snapshot / name
        if (not source.is_file() or not source.resolve().is_relative_to(snapshot)
                or hashlib.sha256(source.read_bytes()).hexdigest() != digest):
            raise ValueError(f"frozen source identity differs: {name}")
    actual = {path.name for path in snapshot.iterdir()
              if path.is_file() and path.suffix in {".py", ".html"}}
    if actual != set(expected):
        raise ValueError("snapshot source file inventory differs from the protocol")
    import torch

    if protocol.get("runtime") != {"python": sys.version, "torch": torch.__version__}:
        raise ValueError("current Python/PyTorch runtime differs from the frozen pilot")
    return snapshot


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", help="pilot directory containing protocol.json")
    parser.add_argument("module", choices=("demo", "infer", "pilot", "experiment"))
    parser.add_argument("arguments", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    snapshot = verify_snapshot(args.directory)
    spec = importlib.util.spec_from_file_location(
        "tide_jepa", snapshot / "__init__.py", submodule_search_locations=[str(snapshot)])
    package = importlib.util.module_from_spec(spec)
    sys.modules["tide_jepa"] = package
    spec.loader.exec_module(package)
    sys.argv = [f"tide_jepa.{args.module}", *args.arguments]
    runpy.run_module(f"tide_jepa.{args.module}", run_name="__main__")


if __name__ == "__main__":
    main()
