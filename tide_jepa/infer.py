"""Offline JSONL inference adapter for a trained TIDE-JEPA checkpoint."""

import argparse
import json
from pathlib import Path

import torch

from tide_jepa.config import ModelConfig
from tide_jepa.data import UTF8ByteTokenizer
from tide_jepa.experiment import _canonical_hash, _implementation_identity, _parse_inventory, _runtime_identity
from tide_jepa.model import TIDEJEPA


class OfflineGenerator:
    """Load one trained checkpoint and serve single-request generation offline."""

    def __init__(self, run_config: str | Path, checkpoint: str | Path, *, device: str = "auto"):
        config_path = Path(run_config).resolve()
        with config_path.open("r", encoding="utf-8") as stream:
            config = json.load(stream)
        if device == "auto":
            device = "cuda" if torch.cuda.is_available() else "cpu"
        if device.startswith("cuda") and not torch.cuda.is_available():
            raise RuntimeError("CUDA was requested but is unavailable")
        self.device = device
        self.tokenizer = UTF8ByteTokenizer()
        inventory_path = (config_path.parent / config["inventory"]).resolve()
        with inventory_path.open("r", encoding="utf-8") as stream:
            inventory_value = json.load(stream)
            self.inventory = _parse_inventory(inventory_value)
        model_settings = config.get("model", {})
        self.cfg = ModelConfig(
            vocab_size=self.tokenizer.vocab_size,
            action_count=len(self.inventory.actions),
            width=model_settings.get("width", 64),
            heads=model_settings.get("heads", 4),
            layers=model_settings.get("layers", 2),
            max_length=model_settings.get("max_length", 512),
            languages=tuple(config.get("languages", ("vi", "en", "cham_phan_rang"))),
            source_pointer_decoder=model_settings.get("source_pointer_decoder", False),
        )
        self.model = TIDEJEPA(self.cfg).to(device)
        state = torch.load(Path(checkpoint), map_location="cpu", weights_only=True)
        if "model" not in state:
            raise ValueError("checkpoint does not contain model weights")
        resolved_path = Path(checkpoint).parent / "resolved_run.json"
        if not resolved_path.is_file():
            raise ValueError("checkpoint needs its resolved_run.json provenance file")
        with resolved_path.open(encoding="utf-8") as stream:
            resolved = json.load(stream)
        identity_keys = ("config", "corpus_sha256", "split_sha256", "inventory_sha256", "alignments_sha256", "implementation_sha256", "runtime")
        identity = {key: resolved[key] for key in identity_keys}
        if "review_approval_sha256" in resolved:
            identity["review_approval_sha256"] = resolved["review_approval_sha256"]
        if (resolved.get("config") != config
                or resolved.get("inventory_sha256") != _canonical_hash(inventory_value)
                or resolved.get("implementation_sha256") != _implementation_identity()
                or resolved.get("runtime") != _runtime_identity()
                or resolved.get("run_sha256") != state.get("run_sha256")
                or resolved.get("run_sha256") != _canonical_hash(identity)):
            raise ValueError("checkpoint identity differs from the supplied config/inventory")
        self.model.load_state_dict(state["model"])
        self.model.eval()

    @torch.inference_mode()
    def generate(self, request: dict) -> dict:
        if not isinstance(request, dict):
            raise ValueError("each request must be a JSON object")
        source = request.get("source")
        source_language = request.get("source_language")
        language = request.get("target_language")
        actions = request.get("actions")
        if not isinstance(source, str) or not source.strip():
            raise ValueError("source must be a nonempty string")
        if source_language not in self.cfg.languages or language not in self.cfg.languages:
            raise ValueError("source_language and target_language must be configured languages")
        if source_language != language:
            raise ValueError("cross-language translation is unsupported; source and target languages must match")
        if not isinstance(actions, list) or not actions:
            raise ValueError("actions must be a nonempty list of {kind, value} objects")
        if len(actions) > 8:
            raise ValueError("at most 8 ordered actions are supported per request")
        action_ids = []
        for action in actions:
            if not isinstance(action, dict) or set(action) != {"kind", "value"}:
                raise ValueError("each action must contain exactly kind and value")
            from tide_jepa.schema import Action

            action_ids.append(self.inventory.require(language, Action(action["kind"], action["value"])))
        encoded = self.tokenizer.encode(source)
        if not encoded or len(encoded) > self.cfg.max_length:
            raise ValueError("source exceeds configured byte-token length")
        token_limit = min(160, self.cfg.max_length - 1)
        max_new_tokens = request.get("max_new_tokens", min(128, token_limit))
        if type(max_new_tokens) is not int or not 0 < max_new_tokens <= token_limit:
            raise ValueError(f"max_new_tokens must be an integer from 1 through {token_limit}")
        source_tensor = torch.tensor([encoded], dtype=torch.long, device=self.device)
        language_ids = torch.tensor([self.cfg.languages.index(language)], dtype=torch.long, device=self.device)
        actions_tensor = torch.tensor(action_ids, dtype=torch.long, device=self.device)
        if len(action_ids) == 1:
            output = self.model.generate(
                source_tensor,
                actions_tensor,
                language_ids,
                self.tokenizer.bos_id,
                self.tokenizer.eos_id,
                max_new_tokens,
            )
        else:
            output = self.model.generate_path(
                source_tensor,
                actions_tensor,
                language_ids,
                self.tokenizer.bos_id,
                self.tokenizer.eos_id,
                max_new_tokens,
            )
        raw_ids = output[0].tolist()
        try:
            text = self.tokenizer.decode(raw_ids)
            valid_utf8 = True
        except UnicodeDecodeError:
            text = self.tokenizer.decode(raw_ids, errors="replace")
            valid_utf8 = False
        result = {
            "generated_text": text,
            "valid_utf8": valid_utf8,
            "generated_token_ids": raw_ids,
            "quality_status": "diagnostic_only",
            "human_validated": False,
        }
        if "request_id" in request:
            result["request_id"] = request["request_id"]
        return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Run offline TIDE-JEPA inference over JSON Lines")
    parser.add_argument("run_config", help="the JSON config used to train the checkpoint")
    parser.add_argument("checkpoint", help="trained checkpoint, usually runs/.../best.pt")
    parser.add_argument("--device", default="auto", help="auto, cpu, cuda, or cuda:N")
    args = parser.parse_args()
    generator = OfflineGenerator(args.run_config, args.checkpoint, device=args.device)
    for line_number, line in enumerate(__import__("sys").stdin, start=1):
        if not line.strip():
            continue
        try:
            request = json.loads(line)
            response = generator.generate(request)
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
            response = {"error": str(error), "line": line_number}
        print(json.dumps(response, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
