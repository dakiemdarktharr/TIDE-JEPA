"""Local-only offline demo for a provenance-checked preliminary checkpoint."""

import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path


def make_handler(generator, metadata):
    page = (Path(__file__).parent / "demo.html").read_bytes()

    class Handler(BaseHTTPRequestHandler):
        def setup(self):
            super().setup()
            self.connection.settimeout(5.0)

        def log_message(self, *_args):
            # No input or output text is written to terminal logs.
            pass

        def respond(self, status, body, content_type="application/json; charset=utf-8"):
            if isinstance(body, dict):
                body = json.dumps(body, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            if self.path == "/":
                self.respond(200, page, "text/html; charset=utf-8")
            elif self.path == "/health":
                self.respond(200, {"status": "operational", "quality_status": "diagnostic_only",
                                   "languages": list(generator.cfg.languages), **metadata})
            else:
                self.respond(404, {"error": "Không có trang này."})

        def do_POST(self):
            if self.path != "/generate":
                self.respond(404, {"error": "Không có chức năng này."})
                return
            if not self.client_address[0].startswith(("127.", "::1")):
                self.respond(403, {"error": "Chỉ chấp nhận kết nối loopback."})
                return
            allowed_hosts = {f"127.0.0.1:{self.server.server_port}", f"localhost:{self.server.server_port}",
                             f"[::1]:{self.server.server_port}"}
            if self.headers.get("Host", "") not in allowed_hosts:
                self.respond(403, {"error": "Host không hợp lệ cho demo loopback."})
                return
            origin = self.headers.get("Origin")
            if origin and origin not in {f"http://127.0.0.1:{self.server.server_port}",
                                         f"http://localhost:{self.server.server_port}",
                                         f"http://[::1]:{self.server.server_port}"}:
                self.respond(403, {"error": "Origin không được phép."})
                return
            if self.headers.get_content_type() != "application/json":
                self.respond(415, {"error": "Yêu cầu phải ở dạng JSON."})
                return
            try:
                size = int(self.headers.get("Content-Length", "0"))
                if not 0 < size <= 65536:
                    raise ValueError("Yêu cầu trống hoặc vượt giới hạn kích thước.")
                body = self.rfile.read(size)
                if len(body) != size:
                    raise ValueError("Yêu cầu JSON chưa được gửi đầy đủ.")
                value = json.loads(body)
                if not isinstance(value, dict):
                    raise ValueError("Yêu cầu phải là một đối tượng JSON.")
                if value.get("source_language") != value.get("target_language"):
                    raise ValueError("Demo chỉ hỗ trợ biến đổi trong cùng một ngôn ngữ.")
                actions = value.get("actions")
                if not isinstance(actions, list) or not 1 <= len(actions) <= 8:
                    raise ValueError("Số hành động vượt phạm vi hỗ trợ.")
                token_budget = value.get("max_new_tokens", 128)
                if type(token_budget) is not int or not 0 < token_budget <= 160:
                    raise ValueError("Ngân sách token vượt phạm vi hỗ trợ.")
                self.respond(200, generator.generate(value))
            except (UnicodeDecodeError, json.JSONDecodeError, TypeError, ValueError, KeyError, TimeoutError, OSError) as error:
                self.respond(400, {"error": "Yêu cầu không hợp lệ hoặc nằm ngoài phạm vi demo."})

    return Handler


def main():
    import torch
    from .infer import OfflineGenerator

    parser = argparse.ArgumentParser(description="Serve the preliminary Vi-En demo locally, without cloud calls")
    parser.add_argument("run_config")
    parser.add_argument("checkpoint")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    torch.set_num_threads(1)
    config_path = Path(args.run_config).resolve()
    config = json.loads(config_path.read_text(encoding="utf-8"))
    if not config.get("review_gate"):
        raise ValueError("this demo requires a preliminary AI review gate")
    approval = json.loads((config_path.parent / config["review_gate"]).read_text(encoding="utf-8"))
    if (approval.get("approval_kind") != "AI-preliminary" or approval.get("human_validated") is not False
            or approval.get("phomt_used") is not False):
        raise ValueError("this demo's provenance labels require an original AI-authored preliminary checkpoint")
    resolved = json.loads((Path(args.checkpoint).parent / "resolved_run.json").read_text(encoding="utf-8"))
    from .pilot import _hash_file
    if resolved.get("review_approval_sha256") != _hash_file(config_path.parent / config["review_gate"]):
        raise ValueError("demo approval file differs from checkpoint approval identity")
    review_hashes = approval.get("review_files_sha256", {})
    if set(review_hashes) != {"review-a.json", "review-b.json", "adjudication.json"}:
        raise ValueError("demo needs the checkpoint's complete review evidence")
    if any(_hash_file(config_path.parent / name) != sha for name, sha in review_hashes.items()):
        raise ValueError("demo review evidence changed after checkpoint approval")
    generator = OfflineGenerator(args.run_config, args.checkpoint, device="cpu")
    if set(generator.cfg.languages) != {"en", "vi"}:
        raise ValueError("this preliminary demo requires an English-Vietnamese checkpoint")
    protocol_path = config_path.parent / "protocol.json"
    protocol = json.loads(protocol_path.read_text(encoding="utf-8")) if protocol_path.is_file() else {}
    validation_path = Path(args.checkpoint).resolve().parent / "generation_metrics.validation.json"
    validation_gate = "unverified"
    if validation_path.is_file() and config["objective"]["mode"] == protocol.get("primary_quality_mode"):
        validation = json.loads(validation_path.read_text(encoding="utf-8"))
        validation_gate = validation.get("quality_gate", {}).get("status", "unverified")
    elif config["objective"]["mode"] != protocol.get("primary_quality_mode"):
        validation_gate = "control_only"
    statement_path = config_path.parent / "data_statement.json"
    version = json.loads(statement_path.read_text(encoding="utf-8")).get("version", "preliminary pilot") if statement_path.is_file() else "preliminary pilot"
    metadata = {"human_validated": False, "phomt_trained": False,
                "mode": config["objective"]["mode"], "seed": config["seed"],
                "pilot_version": version,
                "primary_quality_mode": protocol.get("primary_quality_mode"),
                "validation_gate_status": validation_gate}
    with ThreadingHTTPServer(("127.0.0.1", args.port), make_handler(generator, metadata)) as server:
        print(f"TIDE-JEPA preliminary offline demo: http://127.0.0.1:{args.port}", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
