"""Audit a semantic checker using train references and deliberate corruptions.

Checks the protocol-bound review bundle only. Emits counts and identities, never
text. Exit 1 means checker defects were found, so quality claims need repair.
"""

import argparse
from collections import defaultdict
import json
from pathlib import Path
import re
import sys
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.diagnose_train_checkpoint import activate_frozen, load_train_bundle, sha256


def corruptions(row, frame):
    """Expected failed flag for each single, declared semantic corruption."""
    text, language = row["target_text"], row["language"]
    for component in ("agent", "patient", "place"):
        marker = frame.get(f"{component}_{language}")
        if marker and re.search(re.escape(marker), text, flags=re.IGNORECASE):
            yield component, re.sub(re.escape(marker), "", text, flags=re.IGNORECASE), component + "_preserved"
    if language == "vi" and frame["time"] != "past" and re.search(r"\bđang\s+", text, re.IGNORECASE):
        yield "vi_progressive", re.sub(r"\bđang\s+", "", text, flags=re.IGNORECASE), "action_fidelity"
    time_marker = {"en": ("yesterday", "right now"), "vi": ("hôm qua", "bây giờ")}[language]
    original, changed = time_marker if frame["time"] == "past" else tuple(reversed(time_marker))
    if re.search(re.escape(original), text, flags=re.IGNORECASE):
        yield "time", re.sub(re.escape(original), changed, text, flags=re.IGNORECASE), "action_fidelity"


def audit(directory, implementation="frozen"):
    base = Path(directory).resolve()
    protocol, rows, frames = load_train_bundle(base)
    if implementation == "frozen":
        activate_frozen(base)
    elif implementation != "workspace":
        raise ValueError("implementation must be frozen or workspace")
    from tide_jepa.experiment import _implementation_identity
    from tide_jepa.pilot import _semantic_frame_flags
    gold = {"examples": 0, "covered": 0, "action_and_preservation_pass": 0}
    checks = defaultdict(lambda: {"cases": 0, "rejected_as_expected": 0})
    for row in rows:
        frame = frames[row["target_frame_id"]]
        text = unicodedata.normalize("NFC", row["target_text"])
        flags = _semantic_frame_flags(text, row["language"], frame)
        gold["examples"] += 1
        gold["covered"] += int(flags is not None)
        gold["action_and_preservation_pass"] += int(flags is not None and flags["action_fidelity"]
                                                   and flags["preservation"])
        for mutation, changed, failed_flag in corruptions({**row, "target_text": text}, frame):
            changed_flags = _semantic_frame_flags(changed, row["language"], frame)
            counts = checks[row["language"] + "/" + mutation]
            counts["cases"] += 1
            counts["rejected_as_expected"] += int(changed_flags is not None and not changed_flags[failed_flag])
    passed = (gold["examples"] > 0 and gold["examples"] == gold["covered"]
              == gold["action_and_preservation_pass"] and bool(checks)
              and all(value["cases"] == value["rejected_as_expected"] for value in checks.values()))
    return {"status": "pass" if passed else "fail", "implementation": implementation,
        "scope": "train-only checker mechanism audit on approved-scope synthetic references",
        "human_validated": False, "phomt_used": False, "text_emitted": False,
        "release_holdout_opened": False, "validation_rows_scored": False,
        "not_frozen_protocol_evidence": True, "protocol_sha256": sha256(base / "protocol.json"),
        "review_bundle_sha256": protocol["review_bundle_sha256"],
        "implementation_sha256": _implementation_identity(), "script_sha256": sha256(__file__),
        "gold": gold, "negative_controls": dict(sorted(checks.items()))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory")
    parser.add_argument("--implementation", choices=("frozen", "workspace"), default="frozen")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    report = audit(args.directory, args.implementation)
    destination = Path(args.output)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("status", "implementation", "gold", "negative_controls",
                                                 "text_emitted", "release_holdout_opened")}, sort_keys=True))
    raise SystemExit(0 if report["status"] == "pass" else 1)


if __name__ == "__main__":
    main()
