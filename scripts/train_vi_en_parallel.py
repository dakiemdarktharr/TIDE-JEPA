"""Train all preregistered CPU configs concurrently; never scores the test split."""

from concurrent.futures import ProcessPoolExecutor, as_completed
import argparse
from contextlib import redirect_stderr, redirect_stdout
import json
import multiprocessing
import os
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))


def _train_one(base_text, config_name):
    import torch
    from tide_jepa.experiment import run_experiment

    base = Path(base_text)
    config_path = base / config_name
    config = json.loads(config_path.read_text(encoding="utf-8"))
    output = (base / config["output_dir"]).resolve()
    output.mkdir(parents=True, exist_ok=True)
    torch.set_num_threads(1)
    with (output / "training.log").open("a", encoding="utf-8") as log, \
            redirect_stdout(log), redirect_stderr(log):
        result = run_experiment(config_path, resume=(output / "latest.pt").is_file(), device="cpu")
    return {"config": config_name, "last_epoch": result["last_epoch"], "steps": result["steps"],
            "best_validation_loss": result["best_validation_loss"]}


def train_all(directory, *, workers=4):
    from tide_jepa.experiment import _implementation_identity, _runtime_identity
    from tide_jepa.pilot import _hash_file

    base = Path(directory).resolve()
    protocol = json.loads((base / "protocol.json").read_text(encoding="utf-8"))
    if (base / "suite_report.json").exists():
        raise FileExistsError("suite is already evaluated; preserve it and use another pilot version")
    if type(workers) is not int or not 1 <= workers <= 8:
        raise ValueError("workers must be an integer in 1..8")
    names = protocol.get("configs", [])
    if not names or len(names) != len(set(names)):
        raise ValueError("protocol needs unique registered configs")
    if (protocol.get("implementation_sha256") != _implementation_identity()
            or protocol.get("runtime") != _runtime_identity()
            or protocol.get("approval_sha256") != _hash_file(base / "approval.json")
            or protocol.get("config_files_sha256") != {name: _hash_file(base / name) for name in names}):
        raise ValueError("current config/approval/code/runtime differs from frozen training protocol")
    results = []
    with ProcessPoolExecutor(max_workers=workers) as pool:
        pending = {pool.submit(_train_one, str(base), name): name for name in protocol["configs"]}
        for future in as_completed(pending):
            result = future.result()
            results.append(result)
            print(json.dumps({"trained": result["config"], "last_epoch": result["last_epoch"],
                              "steps": result["steps"]}, sort_keys=True), flush=True)
    if len(results) != len(protocol["configs"]):
        raise RuntimeError("not every preregistered config completed training")
    return results


if __name__ == "__main__":
    multiprocessing.freeze_support()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory")
    parser.add_argument("--workers", type=int, default=min(4, os.cpu_count() or 1))
    args = parser.parse_args()
    completed = train_all(args.directory, workers=args.workers)
    print(json.dumps({"training_only": True, "configs_completed": len(completed)}, sort_keys=True))
