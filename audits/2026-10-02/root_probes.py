"""Read-only implementation probes using original synthetic test fixtures.

Creates disposable synthetic artifacts; never accesses or prints PhoMT rows.
"""
from contextlib import redirect_stdout
import argparse
from dataclasses import replace
from datetime import datetime, timezone
import io
import hashlib
import json
from pathlib import Path
import sys
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))

import torch
from test_pilot import PilotWorkflowTests
import tide_jepa.experiment as experiment
from tide_jepa.data import dataset_fingerprint, read_jsonl
from tide_jepa.pilot import evaluate_generation


def main(output_path=None):
    if output_path:
        destination = Path(output_path)
    else:
        now = datetime.now(timezone.utc)
        stamp = now.strftime("%Y%m%dT%H%M%SZ")
        destination = ROOT / "audits" / now.strftime("%Y-%m-%d") / f"root-probe-results-{stamp}.json"
    if destination.exists():
        raise FileExistsError(f"refusing to overwrite probe evidence: {destination}")
    fixture = PilotWorkflowTests()
    fixture.setUp()
    try:
        fixture.freeze()
        path = fixture.base / "token_only-seed-17.json"
        config = json.loads(path.read_text(encoding="utf-8"))
        output = fixture.base / "root-probe-run"
        config["output_dir"] = str(output)
        path.write_text(json.dumps(config), encoding="utf-8")
        protocol_path = fixture.base / "protocol.json"
        protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
        protocol["config_files_sha256"][path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
        protocol_path.write_text(json.dumps(protocol), encoding="utf-8")
        original_save = experiment._save_checkpoint

        def fail_before_best(destination, state):
            if destination.name == "best.pt":
                raise RuntimeError("simulated crash before best publication")
            return original_save(destination, state)

        with patch.object(experiment, "_save_checkpoint", fail_before_best), redirect_stdout(io.StringIO()):
            try:
                experiment.run_experiment(path, device="cpu")
            except RuntimeError as error:
                if "simulated crash" not in str(error):
                    raise
        latest = torch.load(output / "latest.pt", weights_only=True)
        with redirect_stdout(io.StringIO()):
            resumed = experiment.run_experiment(path, resume=True, device="cpu")
            try:
                experiment.run_experiment(path, resume=True, evaluate_test=True, device="cpu")
                test_failure = None
            except ValueError as error:
                test_failure = str(error)
        evidence = {
            "fixture": "original synthetic, one epoch; no PhoMT",
            "latest_epoch_after_crash": latest["epoch"],
            "latest_steps_after_crash": latest["steps"],
            "best_exists_after_resume": (output / "best.pt").exists(),
            "resume_reports_last_epoch": resumed["last_epoch"],
            "release_test_gate_after_single_run": "unexpectedly opened" if test_failure is None else test_failure,
        }
        # Restore a consistent run in the disposable fixture, then alter only
        # its synthetic evaluation corpus/manifest, leaving approvals stale.
        output2 = fixture.base / "evaluation-probe-run"
        config["output_dir"] = str(output2)
        path.write_text(json.dumps(config), encoding="utf-8")
        with redirect_stdout(io.StringIO()):
            experiment.run_experiment(path, device="cpu")
        inventory = experiment._parse_inventory(json.loads((fixture.base / "inventory.json").read_text()))
        rows = list(read_jsonl(fixture.base / "corpus.jsonl", inventory))
        manifest_path = fixture.base / "split_manifest.json"
        manifest = json.loads(manifest_path.read_text())
        chosen = next(i for i, row in enumerate(rows)
                      if manifest["groups"][row.split_group_id] == "test" and row.path_id is None)
        rows[chosen] = replace(rows[chosen], target_text=rows[chosen].target_text + " Extra original synthetic text.")
        (fixture.base / "corpus.jsonl").write_text(
            "".join(json.dumps(row.to_dict(), ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")
        manifest["dataset_sha256"] = dataset_fingerprint(rows)
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        with redirect_stdout(io.StringIO()):
            try:
                evaluate_generation(path, max_new_tokens=1)
                generation_failure = None
            except ValueError as error:
                generation_failure = str(error)
            try:
                experiment.run_experiment(path, resume=True, device="cpu")
                strict_runner_failure = None
            except ValueError as error:
                strict_runner_failure = str(error)
        evidence["modified_evaluation_corpus_rejected_by_evaluate_generation"] = generation_failure
        evidence["strict_runner_refuses_same_modified_corpus"] = strict_runner_failure
        print(json.dumps(evidence, indent=2))
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("x", encoding="utf-8") as result_file:
            result_file.write(json.dumps(evidence, indent=2) + "\n")
    finally:
        fixture.tearDown()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", help="save new evidence separately from the historical probe result")
    main(parser.parse_args().output)
