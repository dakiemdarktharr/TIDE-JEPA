"""Aggregate-only diagnosis of validation entity/predicate preservation.

Reads private synthetic validation generations and emits only category counts.
Never prints or writes source, reference, or generated text.
"""

import argparse
import json
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from tide_jepa.pilot import _norm_text
from tide_jepa.pilot_seed import FAMILIES_V46, FAMILIES_V47, FAMILIES_V48


def diagnose(directory, modes=("tide",), output=None):
    base = Path(directory).resolve()
    statement = json.loads((base / "data_statement.json").read_text(encoding="utf-8"))
    version = statement.get("version")
    family_map = {"vi-en-ai-v4.6": FAMILIES_V46, "vi-en-ai-v4.7": FAMILIES_V47,
                  "vi-en-ai-v4.8": FAMILIES_V48}.get(version)
    if family_map is None:
        raise ValueError("this diagnostic is bound to the v4.6-v4.8 synthetic validation grammar")
    families = {item[0]: item for group in family_map.values() for item in group}
    frames = json.loads((base / "semantic_frames.json").read_text(encoding="utf-8"))
    results = {}
    for config_path in sorted(base.glob("*-seed-*.json")):
        config = json.loads(config_path.read_text(encoding="utf-8"))
        if config.get("objective", {}).get("mode") not in modes:
            continue
        seed = config["seed"]
        run_dir = (base / config["output_dir"]).resolve()
        private_path = run_dir / "generation.validation.private.jsonl"
        if not private_path.is_file():
            raise FileNotFoundError("private validation generation is missing")
        with private_path.open(encoding="utf-8") as stream:
            for line in stream:
                item = json.loads(line)
                language = item["language"]
                task = item["task"]
                frame = frames[item["target_frame"]]
                family = families[frame["event"]]
                generated = _norm_text(item["generated_text"])
                if language == "en":
                    agent, patient = family[1], family[5]
                    progressive = frame.get("predicate_en_progressive")
                    if progressive and frame["time"] != "past":
                        predicate = (("is not " if frame["polarity"] == "negative" else "is ")
                                     + progressive)
                    elif frame["polarity"] == "negative":
                        predicate = (("did not " if frame["time"] == "past" else "does not ")
                                     + family[2])
                    elif frame["time"] == "past":
                        predicate = family[4]
                    else:
                        predicate = family[3]
                elif language == "vi":
                    agent, patient = family[6], family[8]
                    predicate = (("không " + family[7]) if frame["polarity"] == "negative" else
                                 (("đã " if frame["time"] == "past" else "") + family[7]))
                else:
                    raise ValueError("validation generation has unsupported language")
                bucket = (f"{config['objective']['mode']}/seed-{seed}/"
                          f"{language}/{task}/{item.get('action_key', 'aggregate')}")
                counts = results.setdefault(bucket, {
                    "examples": 0, "agent_present": 0, "patient_present": 0,
                    "predicate_present": 0, "all_preserved": 0,
                })
                agent_ok = _norm_text(agent) in generated
                patient_ok = _norm_text(patient) in generated
                predicate_ok = _norm_text(predicate) in generated
                counts["examples"] += 1
                counts["agent_present"] += int(agent_ok)
                counts["patient_present"] += int(patient_ok)
                counts["predicate_present"] += int(predicate_ok)
                counts["all_preserved"] += int(agent_ok and patient_ok and predicate_ok)
    report = {
        "scope": f"{version} AI-authored synthetic validation only",
        "human_validated": False,
        "phomt_used": False,
        "source_reference_and_generated_text_emitted": False,
        "aggregate": results,
    }
    if output:
        destination = Path(output)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                               encoding="utf-8")
    print(json.dumps({"scope": report["scope"], "human_validated": False,
                      "phomt_used": False, "aggregate": results}, ensure_ascii=False, sort_keys=True))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory")
    parser.add_argument("--mode", action="append", default=None)
    parser.add_argument("--output")
    args = parser.parse_args()
    diagnose(args.directory, tuple(args.mode or ("tide",)), args.output)


if __name__ == "__main__":
    main()
