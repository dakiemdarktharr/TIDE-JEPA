#!/usr/bin/env python3
"""Measure loopback demo latency and process RSS without saving request text.

The benchmark submits the demo page's own default request repeatedly. Output
contains aggregate timings, HTTP/UTF-8 counts, and RSS samples only.
"""

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from html.parser import HTMLParser
import json
import math
import os
from pathlib import Path
import socket
import statistics
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class _Defaults(HTMLParser):
    def __init__(self):
        super().__init__()
        self.textarea = None
        self.select_defaults = {}
        self._active_select = None
        self._select_options = {}
        self._in_source = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "textarea" and attrs.get("id") == "source":
            self._in_source = True
            self.textarea = ""
        elif tag == "select":
            self._active_select = attrs.get("id")
            if self._active_select:
                self._select_options[self._active_select] = []
        elif tag == "option" and self._active_select:
            self._select_options[self._active_select].append(
                (attrs.get("value", ""), "selected" in attrs)
            )

    def handle_endtag(self, tag):
        if tag == "textarea":
            self._in_source = False
        elif tag == "select":
            self._active_select = None

    def handle_data(self, data):
        if self._in_source and self.textarea is not None:
            self.textarea += data

    def request_defaults(self):
        result = {}
        for key, options in self._select_options.items():
            if options:
                result[key] = next((value for value, selected in options if selected), options[0][0])
        source_language = result.get("source-language")
        target_language = result.get("language")
        action_values = [result.get("first", ""), result.get("second", "")]
        actions = []
        for value in action_values:
            if value:
                kind, action_value = value.split(":", 1)
                actions.append({"kind": kind, "value": action_value})
        if not self.textarea or not source_language or not target_language or not actions:
            raise ValueError("demo page did not expose a complete default request")
        return {
            "source": self.textarea,
            "source_language": source_language,
            "target_language": target_language,
            "actions": actions,
            "max_new_tokens": 96,
        }


def _listener_pid(port):
    inodes = set()
    for filename in ("/proc/net/tcp", "/proc/net/tcp6"):
        try:
            lines = Path(filename).read_text().splitlines()[1:]
        except OSError:
            continue
        for line in lines:
            fields = line.split()
            if len(fields) > 9 and fields[3] == "0A" and int(fields[1].rsplit(":", 1)[1], 16) == port:
                inodes.add(fields[9])
    pids = set()
    if not inodes:
        return None
    for proc in Path("/proc").iterdir():
        if not proc.name.isdigit():
            continue
        try:
            descriptors = (proc / "fd").iterdir()
            for descriptor in descriptors:
                try:
                    target = os.readlink(descriptor)
                except OSError:
                    continue
                if target.startswith("socket:[") and target.endswith("]"):
                    if target[8:-1] in inodes:
                        pids.add(int(proc.name))
                        break
        except OSError:
            continue
    if len(pids) != 1:
        return None
    return pids.pop()


def _rss_kib(pid):
    if pid is None:
        return None
    try:
        for line in Path(f"/proc/{pid}/status").read_text().splitlines():
            if line.startswith("VmRSS:"):
                return int(line.split()[1])
    except (OSError, ValueError):
        pass
    return None


def _is_v433_demo_runner(pid):
    if pid is None:
        return False
    try:
        command = Path(f"/proc/{pid}/cmdline").read_bytes().split(b"\0")
    except OSError:
        return False
    return any(b"run_v433_demo.py" in argument for argument in command)


def _percentile(values, quantile):
    ordered = sorted(values)
    index = max(0, min(len(ordered) - 1, math.ceil(quantile * len(ordered)) - 1))
    return ordered[index]


def _request_once(base_url, request_body, checker_context=None):
    request = Request(base_url + "/generate", data=request_body,
                      headers={"Content-Type": "application/json"}, method="POST")
    started = time.perf_counter()
    try:
        with urlopen(request, timeout=15) as response:
            body = response.read()
            status = response.status
    except HTTPError as error:
        body = error.read()
        status = error.code
    except (TimeoutError, URLError, OSError) as error:
        raise RuntimeError(f"loopback transport failed: {type(error).__name__}") from None
    elapsed_ms = (time.perf_counter() - started) * 1000
    try:
        payload = json.loads(body.decode("utf-8", errors="strict"))
        valid_utf8 = True
    except (UnicodeDecodeError, json.JSONDecodeError):
        payload = {}
        valid_utf8 = False
    semantic = None
    if checker_context is not None and isinstance(payload.get("generated_text"), str):
        from tide_jepa.pilot import _semantic_frame_flags
        semantic = _semantic_frame_flags(
            payload["generated_text"], checker_context["language"], checker_context["frame"])
    return {
        "status": status,
        "valid_utf8": valid_utf8,
        "nonempty": isinstance(payload.get("generated_text"), str) and bool(payload["generated_text"].strip()),
        "diagnostic_only": payload.get("quality_status") == "diagnostic_only",
        "overload_refusal_schema_valid": (
            status == 503 and isinstance(payload.get("error"), str) and bool(payload["error"])
        ),
        "semantic_checker_coverage": semantic is not None,
        "action_fidelity_pass": bool(semantic and semantic["action_fidelity"]),
        "preservation_pass": bool(semantic and semantic["preservation"]),
        "checker_language": checker_context["language"] if checker_context is not None else None,
        "checker_task": checker_context["task"] if checker_context is not None else None,
        "latency_ms": elapsed_ms,
    }


def _approved_train_requests(config_path):
    """Build local-only requests from the v4.33 approved train split."""
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from tide_jepa.data import read_jsonl, read_split_manifest
    from tide_jepa.experiment import _parse_inventory

    config_path = Path(config_path).resolve()
    base = config_path.parent
    config = json.loads(config_path.read_text(encoding="utf-8"))
    statement = json.loads((base / "data_statement.json").read_text(encoding="utf-8"))
    approval = json.loads((base / config["review_gate"]).read_text(encoding="utf-8"))
    if (statement.get("version") != "vi-en-ai-v4.33"
            or approval.get("human_validated") is not False
            or approval.get("phomt_used") is not False):
        raise ValueError("varied requests require the preliminary PhoMT-free v4.33 pilot")
    inventory_value = json.loads((base / config["inventory"]).read_text(encoding="utf-8"))
    inventory = _parse_inventory(inventory_value)
    rows = read_jsonl(base / config["corpus"], inventory, languages=("en", "vi"))
    manifest = read_split_manifest(base / config["frozen_split"], rows, inventory)
    frames = json.loads((base / "semantic_frames.json").read_text(encoding="utf-8"))

    single_candidates = {"en": [], "vi": []}
    path_candidates = {"en": [], "vi": []}
    seen = set()
    for row in rows:
        if manifest.groups[row.split_group_id] != "train" or row.path_id is not None:
            continue
        request = {
            "source": row.source_text,
            "source_language": row.language,
            "target_language": row.language,
            "actions": [{"kind": row.action.kind, "value": row.action.value}],
            "max_new_tokens": 96,
        }
        key = (row.language, row.source_text, ((row.action.kind, row.action.value),))
        if key not in seen:
            seen.add(key)
            single_candidates[row.language].append((request, {
                "language": row.language,
                "task": "single_action",
                "frame": frames[row.target_frame_id],
            }))

    paths = {}
    for row in rows:
        if manifest.groups[row.split_group_id] == "train" and row.path_id is not None:
            paths.setdefault((row.path_id, row.language), []).append(row)
    for (_, language), path_rows in paths.items():
        ordered = sorted(path_rows, key=lambda row: row.path_step)
        actions = tuple((row.action.kind, row.action.value) for row in ordered)
        key = (language, ordered[0].source_text, actions)
        if key not in seen:
            seen.add(key)
            path_candidates[language].append(({
                    "source": ordered[0].source_text,
                    "source_language": language,
                    "target_language": language,
                    "actions": [{"kind": kind, "value": value} for kind, value in actions],
                    "max_new_tokens": 96,
                }, {
                    "language": language,
                    "task": "two_action_path",
                    "frame": frames[ordered[-1].target_frame_id],
                }))

    # Interleave languages so each bounded sample covers both without depending
    # on the corpus's storage order. Text stays in process memory only.
    balanced = []
    for index in range(max(map(len, path_candidates.values()))):
        for language in ("en", "vi"):
            for candidates in (path_candidates, single_candidates):
                if index < len(candidates[language]):
                    balanced.append(candidates[language][index])
            if len(balanced) >= 64:
                break
        if len(balanced) >= 64:
            break
    if len(balanced) < 2:
        raise ValueError("the approved train split did not provide varied requests")
    return balanced


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--requests", type=int, default=240)
    parser.add_argument("--workers", type=int, default=1,
                        help="simultaneous loopback clients (1-16); the demo still applies its own inference bound")
    parser.add_argument("--vary-approved", action="store_true",
                        help="cycle through exact single-action/path requests from the PhoMT-free v4.33 train split")
    parser.add_argument("--config", type=Path,
                        default=Path("data/pilot/vi-en-ai-v4.33/tide-copy-0p0-seed-17.json"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not 1 <= args.port <= 65535 or not 20 <= args.requests <= 10000 or not 1 <= args.workers <= 16:
        raise ValueError("port or request count is outside the benchmark bounds")

    base_url = f"http://127.0.0.1:{args.port}"
    with urlopen(base_url + "/health", timeout=5) as response:
        health = json.loads(response.read())
        if response.status != 200 or health.get("status") != "operational" or health.get("quality_status") != "diagnostic_only":
            raise RuntimeError("loopback health did not match the expected diagnostic service")
    with urlopen(base_url + "/", timeout=5) as response:
        page = response.read().decode("utf-8", errors="strict")
    defaults = _Defaults()
    defaults.feed(page)
    samples = (_approved_train_requests(args.config) if args.vary_approved
               else [(defaults.request_defaults(), None)])
    request_values = [sample[0] for sample in samples]
    checker_contexts = [sample[1] for sample in samples]
    request_bodies = [json.dumps(request, ensure_ascii=False).encode("utf-8")
                      for request in request_values]

    pid = _listener_pid(args.port)
    if not _is_v433_demo_runner(pid):
        raise RuntimeError("the loopback port is not owned by the v4.33 demo runner")
    rss_samples = [_rss_kib(pid)]
    latencies_ms = []
    status_counts = {}
    valid_utf8 = 0
    nonempty = 0
    diagnostic_only = 0
    overload_refusal_schema_valid = 0
    quality_groups = {}
    sent_languages = Counter()
    sent_action_steps = Counter()
    sent_tasks = Counter()
    started_batch = time.perf_counter()
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        responses = executor.map(
            lambda index: _request_once(
                base_url, request_bodies[index % len(request_bodies)],
                checker_contexts[index % len(checker_contexts)]),
            range(args.requests),
        )
        for index, result in enumerate(responses, start=1):
            sample_index = (index - 1) % len(request_values)
            sample = request_values[sample_index]
            context = checker_contexts[sample_index]
            sent_languages[sample["source_language"]] += 1
            sent_action_steps[str(len(sample["actions"]))] += 1
            sent_tasks[context["task"] if context else "page_default"] += 1
            latencies_ms.append(result["latency_ms"])
            status = result["status"]
            status_counts[str(status)] = status_counts.get(str(status), 0) + 1
            valid_utf8 += int(result["valid_utf8"])
            nonempty += int(result["nonempty"])
            diagnostic_only += int(result["diagnostic_only"])
            overload_refusal_schema_valid += int(result["overload_refusal_schema_valid"])
            if context:
                group = quality_groups.setdefault(
                    (result["checker_language"], result["checker_task"]),
                    {"examples": 0, "checker_coverage": 0, "action_fidelity_pass": 0,
                     "preservation_pass": 0})
                group["examples"] += 1
                group["checker_coverage"] += int(result["semantic_checker_coverage"])
                group["action_fidelity_pass"] += int(result["action_fidelity_pass"])
                group["preservation_pass"] += int(result["preservation_pass"])
            if index % 20 == 0:
                rss_samples.append(_rss_kib(pid))
    batch_elapsed_seconds = time.perf_counter() - started_batch
    rss_samples.append(_rss_kib(pid))
    quality_summary = {
        f"{language}/{task}": {
            **counts,
            "action_fidelity_rate": counts["action_fidelity_pass"] / counts["checker_coverage"]
            if counts["checker_coverage"] else None,
            "preservation_rate": counts["preservation_pass"] / counts["checker_coverage"]
            if counts["checker_coverage"] else None,
        }
        for (language, task), counts in quality_groups.items()
    }

    report = {
        "schema_version": "v433-demo-runtime-benchmark-v1",
        "date": date.today().isoformat(),
        "service": "loopback v4.33 diagnostic demo",
        "listener_identity_verified": True,
        "request_source": "page-default; text omitted from report",
        "request_count": args.requests,
        "request_variation": {
            "source": "approved v4.33 train split" if args.vary_approved else "page default",
            "unique_candidates": len(request_bodies),
            "source_languages": dict(Counter(request["source_language"] for request in request_values)),
            "action_step_counts": dict(Counter(str(len(request["actions"])) for request in request_values)),
            "requests_sent_by_language": dict(sent_languages),
            "requests_sent_by_action_steps": dict(sent_action_steps),
            "requests_sent_by_task": dict(sent_tasks),
            "request_body_bytes_min": min(map(len, request_bodies)),
            "request_body_bytes_max": max(map(len, request_bodies)),
            "text_recorded": False,
        },
        "concurrent_clients": args.workers,
        "batch_elapsed_seconds": round(batch_elapsed_seconds, 3),
        "throughput_requests_per_second": round(args.requests / batch_elapsed_seconds, 3),
        "http_status_counts": status_counts,
        "valid_utf8_responses": valid_utf8,
        "nonempty_outputs": nonempty,
        "diagnostic_only_responses": diagnostic_only,
        "narrow_checker_summary": quality_summary,
        "expected_overload_refusals": status_counts.get("503", 0),
        "overload_refusal_schema_valid": overload_refusal_schema_valid,
        "bounded_concurrency_behavior": (
            set(status_counts).issubset({"200", "503"})
            and status_counts.get("503", 0) == overload_refusal_schema_valid
        ),
        "all_requests_passed": (
            status_counts == {"200": args.requests}
            and valid_utf8 == args.requests
            and nonempty == args.requests
            and diagnostic_only == args.requests
        ),
        "latency_ms": {
            "mean": round(statistics.fmean(latencies_ms), 3),
            "p50": round(_percentile(latencies_ms, 0.50), 3),
            "p95": round(_percentile(latencies_ms, 0.95), 3),
            "p99": round(_percentile(latencies_ms, 0.99), 3),
            "max": round(max(latencies_ms), 3),
        },
        "server_pid_found": pid is not None,
        "server_rss_kib_samples": [value for value in rss_samples if value is not None],
        "server_rss_first_kib": next((value for value in rss_samples if value is not None), None),
        "server_rss_last_kib": next((value for value in reversed(rss_samples) if value is not None), None),
        "source_or_generated_text_recorded": False,
        "human_validated": False,
        "phomt_used": False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(report, stream, indent=2, sort_keys=True)
        stream.write("\n")
    print(json.dumps({
        "report": str(args.output),
        "requests": args.requests,
        "status_counts": status_counts,
        "expected_overload_refusals": report["expected_overload_refusals"],
        "bounded_concurrency_behavior": report["bounded_concurrency_behavior"],
        "p95_ms": report["latency_ms"]["p95"],
        "rss_first_kib": report["server_rss_first_kib"],
        "rss_last_kib": report["server_rss_last_kib"],
        "source_or_generated_text_emitted": False,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
