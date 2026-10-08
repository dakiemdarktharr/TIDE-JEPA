#!/usr/bin/env python3
"""Serve the amended v4.33 checkpoint locally with corrected gate provenance."""

import argparse
import html
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import torch

from tide_jepa.data import read_jsonl, read_split_manifest
from tide_jepa.demo import ThreadingHTTPServer, make_handler
from tide_jepa.experiment import _canonical_hash, _parse_inventory
from tide_jepa.infer import OfflineGenerator
from tide_jepa.pilot import (_load_v433_checker_reassessment, _read,
                             _require_release_test_gate, validate_review_gate)


def create_server(config_path, port):
    config_path = Path(config_path).resolve()
    base = config_path.parent
    config = _read(config_path)
    protocol = _read(base / "protocol.json")
    statement = _read(base / "data_statement.json")
    if (statement.get("version") != "vi-en-ai-v4.33"
            or config.get("objective", {}).get("mode") != protocol.get("primary_quality_mode")):
        raise ValueError("demo requires a primary v4.33 TIDE configuration")
    amendment = _load_v433_checker_reassessment(base, protocol)
    if amendment is None:
        raise ValueError("demo requires the validated v4.33 checker amendment")

    inventory_value = _read(base / config["inventory"])
    inventory = _parse_inventory(inventory_value)
    rows = read_jsonl(base / config["corpus"], inventory, languages=("en", "vi"))
    manifest = read_split_manifest(base / config["frozen_split"], rows, inventory)
    alignment_path = base / config["alignments"] if config.get("alignments") else None
    alignment_hash = _canonical_hash(_read(alignment_path)) if alignment_path else None
    validate_review_gate(base, config, manifest, _canonical_hash(inventory_value), alignment_hash)
    _require_release_test_gate(base, protocol, manifest, rows)
    report_entry = amendment["entries"].get(config_path.name)
    if report_entry is None or report_entry.get("gate") != "pass":
        raise ValueError("demo checkpoint did not pass amended validation")

    approval_path = base / config["review_gate"]
    approval = _read(approval_path)
    if (approval.get("approval_kind") != "AI-preliminary"
            or approval.get("human_validated") is not False
            or approval.get("phomt_used") is not False):
        raise ValueError("demo provenance must remain preliminary and PhoMT-free")
    output = (base / config["output_dir"]).resolve()
    resolved = _read(output / "resolved_run.json")
    from tide_jepa.pilot import _hash_file
    if resolved.get("review_approval_sha256") != _hash_file(approval_path):
        raise ValueError("demo approval differs from the checkpoint run identity")
    review_hashes = approval.get("review_files_sha256", {})
    expected_review_files = {"review-a.json", "review-b.json", "adjudication.json"}
    if (set(review_hashes) != expected_review_files
            or any(_hash_file(base / name) != digest for name, digest in review_hashes.items())):
        raise ValueError("demo review evidence is incomplete or has changed")

    # The stock demo page's historical example is outside this pilot's corpus.
    # Populate the v4.33 page from one approved train-only single-action row so
    # its first request stays inside the demonstrated data scope.
    default_row = next((row for row in rows
                        if manifest.groups[row.split_group_id] == "train"
                        and row.language == "vi" and row.path_id is None
                        and row.action.kind == "TIME" and row.action.value == "PAST"), None)
    if default_row is None:
        raise ValueError("demo needs an approved Vietnamese train-only TIME:PAST example")
    page_path = Path(__import__("tide_jepa.demo", fromlist=["__file__"]).__file__).with_name("demo.html")
    page = page_path.read_text(encoding="utf-8")
    old_default = "Bây giờ Lan đọc một quyển sách."
    if page.count(old_default) != 1:
        raise ValueError("demo page default changed; review the v4.33 sample injection")
    page_scope = "Pilot chỉ hỗ trợ biến đổi trong cùng một ngôn ngữ; không hỗ trợ dịch."
    if page.count(page_scope) != 1:
        raise ValueError("demo scope notice changed; review the v4.33 scope injection")
    page = page.replace(old_default, html.escape(default_row.source_text, quote=False), 1)
    page = page.replace(
        page_scope,
        "Demo chỉ nhận đúng câu và chuỗi hành động trong tập train đã duyệt; câu khác bị từ chối. "
        "Chỉ hỗ trợ biến đổi cùng ngôn ngữ, không hỗ trợ dịch.", 1).encode("utf-8")

    allowed_requests = set()
    train_rows = [row for row in rows if manifest.groups[row.split_group_id] == "train"]
    for row in train_rows:
        if row.path_id is None:
            allowed_requests.add((row.language, row.source_text,
                                  ((row.action.kind, row.action.value),)))
    paths = {}
    for row in train_rows:
        if row.path_id is not None:
            paths.setdefault((row.path_id, row.language), []).append(row)
    for path_rows in paths.values():
        ordered = sorted(path_rows, key=lambda row: row.path_step)
        allowed_requests.add((ordered[0].language, ordered[0].source_text,
                              tuple((row.action.kind, row.action.value) for row in ordered)))

    checkpoint = output / "best.pt"
    generator = OfflineGenerator(config_path, checkpoint, device="cpu",
                                 allowed_implementation_identity=protocol["implementation_sha256"])
    if set(generator.cfg.languages) != {"en", "vi"}:
        raise ValueError("demo only serves the preliminary English–Vietnamese pilot")
    original_generate = generator.generate
    def generate_train_scope(request):
        actions = tuple((action.get("kind"), action.get("value"))
                        for action in request.get("actions", []) if isinstance(action, dict))
        key = (request.get("source_language"), request.get("source"), actions)
        if key not in allowed_requests:
            raise ValueError("Demo chỉ chấp nhận câu/action mẫu trong train đã duyệt.")
        return original_generate(request)
    generator.generate = generate_train_scope
    metadata = {
        "human_validated": False,
        "phomt_trained": False,
        "pilot_version": statement["version"],
        "mode": config["objective"]["mode"],
        "seed": config["seed"],
        "primary_quality_mode": protocol["primary_quality_mode"],
        "validation_gate_status": "pass",
        "validation_gate_basis": "v4.33 amended narrow synthetic semantic checker",
        "release_holdout_opened": True,
        "scope": "exact approved train source/action combinations only; arbitrary inputs are rejected",
        "default_sample_scope": "approved train-only Vietnamese TIME:PAST example",
        "quality_status": "diagnostic_only",
        "max_new_tokens": min(160, generator.cfg.max_length - 1),
    }
    handler = make_handler(generator, metadata)
    original_get = handler.do_GET
    def serve_page(self):
        if self.path == "/":
            self.respond(200, page, "text/html; charset=utf-8")
            return
        original_get(self)
    handler.do_GET = serve_page
    server = ThreadingHTTPServer(("127.0.0.1", port), handler)
    return server


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path,
                        default=Path("data/pilot/vi-en-ai-v4.33/tide-copy-0p0-seed-17.json"))
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    torch.set_num_threads(1)
    server = create_server(args.config, args.port)
    print(f"TIDE-JEPA v4.33 diagnostic-only offline demo: http://127.0.0.1:{server.server_port}",
          flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
