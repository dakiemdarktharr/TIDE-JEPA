"""Measure local inference latency/resource use without printing generated text."""

import argparse
import hashlib
import json
import math
from pathlib import Path
import statistics
import sys
import time

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))


def _memory_counters():
    """Return Windows process working-set counters, or None off Windows."""
    if sys.platform != "win32":
        return None
    import ctypes
    from ctypes import wintypes

    class Counters(ctypes.Structure):
        _fields_ = [
            ("cb", wintypes.DWORD), ("PageFaultCount", wintypes.DWORD),
            ("PeakWorkingSetSize", ctypes.c_size_t), ("WorkingSetSize", ctypes.c_size_t),
            ("QuotaPeakPagedPoolUsage", ctypes.c_size_t), ("QuotaPagedPoolUsage", ctypes.c_size_t),
            ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t), ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
            ("PagefileUsage", ctypes.c_size_t), ("PeakPagefileUsage", ctypes.c_size_t),
        ]

    value = Counters()
    value.cb = ctypes.sizeof(value)
    handle = ctypes.windll.kernel32.GetCurrentProcess()
    ok = ctypes.windll.psapi.GetProcessMemoryInfo(handle, ctypes.byref(value), value.cb)
    if not ok:
        return None
    return {"working_set_bytes": int(value.WorkingSetSize),
            "peak_working_set_bytes": int(value.PeakWorkingSetSize),
            "private_commit_bytes": int(value.PagefileUsage)}


def benchmark(config_path, checkpoint_path, *, repeats=20, max_new_tokens=96):
    import torch
    from tide_jepa.data import read_jsonl, read_split_manifest
    from tide_jepa.experiment import _parse_inventory
    from tide_jepa.infer import OfflineGenerator

    if type(repeats) is not int or not 5 <= repeats <= 100:
        raise ValueError("repeats must be an integer in 5..100")
    if type(max_new_tokens) is not int or not 1 <= max_new_tokens <= 160:
        raise ValueError("max_new_tokens must be an integer in 1..160")
    config_path, checkpoint_path = Path(config_path).resolve(), Path(checkpoint_path).resolve()
    config = json.loads(config_path.read_text(encoding="utf-8"))
    base = config_path.parent
    inventory = _parse_inventory(json.loads((base / config["inventory"]).read_text(encoding="utf-8")))
    rows = read_jsonl(base / config["corpus"], inventory, languages=("en", "vi"))
    manifest = read_split_manifest(base / config["frozen_split"], rows, inventory)
    example = next(row for row in rows if row.path_id is None
                   and manifest.groups[row.split_group_id] == "validation")
    request = {"source": example.source_text, "source_language": example.language,
               "target_language": example.language,
               "actions": [{"kind": example.action.kind, "value": example.action.value}],
               "max_new_tokens": max_new_tokens}
    torch.set_num_threads(1)
    before_load = _memory_counters()
    started = time.perf_counter()
    generator = OfflineGenerator(config_path, checkpoint_path, device="cpu")
    load_seconds = time.perf_counter() - started
    after_load = _memory_counters()
    generator.generate(request)  # warm-up is excluded from request latency
    durations = []
    for _ in range(repeats):
        started = time.perf_counter()
        response = generator.generate(request)
        durations.append((time.perf_counter() - started) * 1000)
        if not response["valid_utf8"]:
            raise RuntimeError("UTF-8 constrained decoder returned invalid Unicode")
    memory_after = _memory_counters()
    sorted_ms = sorted(durations)
    p95 = sorted_ms[min(len(sorted_ms) - 1, math.ceil(0.95 * len(sorted_ms)) - 1)]
    report = {
        "scope": "local CPU inference benchmark; original synthetic validation input; generated text withheld",
        "human_validated": False, "phomt_used": False,
        "mode": config["objective"]["mode"], "seed": config["seed"],
        "repeats": repeats, "max_new_tokens": max_new_tokens,
        "model_load_seconds": round(load_seconds, 6),
        "request_latency_ms_median": round(statistics.median(durations), 3),
        "request_latency_ms_p95": round(p95, 3),
        "memory_before_model_load": before_load, "memory_after_model_load": after_load,
        "memory_after_requests": memory_after,
        "python": sys.version.split()[0], "torch": torch.__version__,
        "checkpoint_sha256": hashlib.sha256(checkpoint_path.read_bytes()).hexdigest(),
        "protocol_sha256": hashlib.sha256((base / "protocol.json").read_bytes()).hexdigest(),
    }
    output_dir = checkpoint_path.parent
    destination = output_dir / "latency_benchmark.json"
    if destination.exists():
        raise FileExistsError("latency benchmark already exists; preserve it and select another checkpoint version")
    destination.write_text(json.dumps(report, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config")
    parser.add_argument("checkpoint")
    parser.add_argument("--repeats", type=int, default=20)
    parser.add_argument("--max-new-tokens", type=int, default=96)
    args = parser.parse_args()
    print(json.dumps(benchmark(args.config, args.checkpoint, repeats=args.repeats,
                               max_new_tokens=args.max_new_tokens), sort_keys=True))
