"""Synthetic aggregate fixtures; no corpus or generated text is loaded."""

import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


def load_script(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ValidationReportTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.base = Path(self.temporary.name)
        self.script = load_script("summarize_vi_en_validation")
        self.manifest = {"dataset_sha256": "synthetic-dataset", "record_ids": {
            "train": ["a"], "validation": ["b"], "test": ["c"]}}
        self.write(self.base / "split_manifest.json", self.manifest)
        self.write(self.base / "groups.json", {"a": "train", "b": "validation", "c": "test"})
        self.write(self.base / "data_statement.json", {
            "version": "synthetic-tools-fixture", "records": 3, "event_families": 3,
            "split_policy": "synthetic independent groups"})
        self.protocol = {
            "configs": [], "config_files_sha256": {}, "modes": ["tide"], "seeds": [17],
            "epochs": 1, "primary_quality_mode": "tide", "primary_source_copy_weights": [0],
            "primary_latent_objective_weights": [0],
            "primary_source_pointer_decoder_modes": ["vocabulary", "source_pointer"],
            "implementation_sha256": {"pilot.py": "synthetic-source-hash"}, "runtime": {},
            "model": {"width": 8, "heads": 2, "layers": 1}, "generation_max_new_tokens": 160,
            "decoder_policy": "synthetic fixture", "quality_thresholds": {
                "valid_unicode_rate": 1.0, "single_action_action_fidelity_rate": 0.9,
                "single_action_preservation_rate": 0.9, "held_out_path_action_fidelity_rate": 0.8,
                "held_out_path_preservation_rate": 0.8}}
        for pointer in (False, True):
            decoder = "source_pointer" if pointer else "vocabulary"
            name = f"tide-{decoder}.json"
            config = {"seed": 17, "objective": {"mode": "tide", "latent_objective_weight": 0},
                      "model": {"source_pointer_decoder": pointer}, "training": {"epochs": 1},
                      "output_dir": decoder}
            self.write(self.base / name, config)
            self.protocol["configs"].append(name)
            self.protocol["config_files_sha256"][name] = self.script._sha256(self.base / name)
        self.write(self.base / "protocol.json", self.protocol)
        for name in self.protocol["configs"]:
            config = json.loads((self.base / name).read_text())
            output = self.base / config["output_dir"]
            output.mkdir()
            (output / "best.pt").write_bytes(b"synthetic hash fixture, never deserialized")
            resolved = {"config": config, "corpus_sha256": self.manifest["dataset_sha256"],
                        "split_sha256": self.script._canonical_hash(self.manifest),
                        "inventory_sha256": "synthetic", "alignments_sha256": None,
                        "implementation_sha256": self.protocol["implementation_sha256"], "runtime": {}}
            resolved["run_sha256"] = self.script._canonical_hash(resolved)
            self.write(output / "resolved_run.json", resolved)
            identity = {"checkpoint_sha256": self.script._sha256(output / "best.pt"),
                        "run_sha256": resolved["run_sha256"],
                        "corpus_sha256": self.manifest["dataset_sha256"],
                        "split_sha256": self.script._canonical_hash(self.manifest),
                        "protocol_sha256": self.script._sha256(self.base / "protocol.json"),
                        "evaluation_split": "validation",
                        "evaluator_sha256": self.protocol["implementation_sha256"],
                        "decoder_policy": {"max_new_tokens": 160, "source_language_equals_target": True}}
            score = {key: 0 for key in self.script.SCORE_FIELDS}
            score.update(examples=4, valid_unicode=4, terminated_eos=4, checker_coverage=4,
                         action_fidelity_known=4, preservation_known=4, reference_characters=20)
            self.write(output / "generation_metrics.validation.json", {
                "evaluation_split": "validation", "human_validated": False,
                "_evaluation_identity": self.script._canonical_hash(identity),
                "scores": {"en/single/TIME:PAST": score},
                "quality_gate": {"status": "fail", "bucket_checks": {
                    "en/single/TIME:PAST": {"preservation_pass": False}}}})
            (output / "metrics.csv").write_text(
                "epoch,split,updates,token,path_token,seconds,examples_per_second\n"
                "1,train,2,1,1,1,4\n1,validation,0,2,2,0,0\n")

    def write(self, path, value):
        path.write_text(json.dumps(value), encoding="utf-8")

    def tearDown(self):
        self.temporary.cleanup()

    def test_reports_each_decoder_without_pooling_or_opening_test(self):
        destination = self.base / "report.md"
        result = self.script.summarize_validation(self.base, destination)
        self.assertEqual(result["runs"], 2)
        self.assertEqual(result["quality_gate"], "fail")
        self.assertFalse(result["release_test_opened"])
        text = destination.read_text()
        self.assertIn("| vocabulary | en/single/TIME:PAST | 4/4 |", text)
        self.assertIn("| source_pointer | en/single/TIME:PAST | 4/4 |", text)
        self.assertIn("| Preservation | Context marker | Accepted references |", text)
        self.assertIn("| 0/4 | 0/4 | 0/0 | 0/4 |", text)
        self.assertNotIn("8/8", text)

    def test_rejects_changed_checkpoint_or_incomplete_epoch_log(self):
        output = self.base / "vocabulary"
        original = (output / "best.pt").read_bytes()
        (output / "best.pt").write_bytes(b"changed synthetic fixture")
        with self.assertRaisesRegex(ValueError, "identity"):
            self.script.summarize_validation(self.base, self.base / "report.md")
        (output / "best.pt").write_bytes(original)
        (output / "metrics.csv").write_text(
            "epoch,split,updates,token,path_token,seconds,examples_per_second\n"
            "1,train,2,1,1,1,4\n2,validation,0,2,2,0,0\n")
        with self.assertRaisesRegex(ValueError, "registered epoch"):
            self.script.summarize_validation(self.base, self.base / "report.md")
        self.assertFalse((self.base / "report.md").exists())


class PreservationDiagnosticTests(unittest.TestCase):
    def test_keeps_language_balance_conditions_separate(self):
        script = load_script("diagnose_validation_preservation")
        base = {"seed": 17, "objective": {"mode": "tide", "source_copy_weight": 0}}
        unbalanced = {**base, "objective": {**base["objective"], "language_balance_weight": 0}}
        balanced = {**base, "objective": {**base["objective"], "language_balance_weight": 1}}
        key_zero = script._condition_bucket(unbalanced, "en", "single", "TIME:NOW")
        key_one = script._condition_bucket(balanced, "en", "single", "TIME:NOW")
        self.assertNotEqual(key_zero, key_one)
        self.assertIn("language-balance-0", key_zero)
        self.assertIn("language-balance-1", key_one)


class FrozenLauncherTests(unittest.TestCase):
    @unittest.skipUnless(importlib.util.find_spec("torch"), "PyTorch required for frozen runtime identity")
    def test_verifies_source_hashes_without_executing_snapshot(self):
        import sys
        import torch
        launcher = load_script("run_frozen")
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            snapshot = base / "snapshot"
            snapshot.mkdir()
            source = snapshot / "__init__.py"
            source.write_text("raise RuntimeError('must not execute during verification')\n")
            protocol = {"implementation_snapshot": "snapshot",
                        "implementation_sha256": {source.name: hashlib.sha256(source.read_bytes()).hexdigest()},
                        "runtime": {"python": sys.version, "torch": torch.__version__}}
            (base / "protocol.json").write_text(json.dumps(protocol))
            self.assertEqual(launcher.verify_snapshot(base), snapshot)
            source.write_text("changed source")
            with self.assertRaisesRegex(ValueError, "source identity differs"):
                launcher.verify_snapshot(base)


if __name__ == "__main__":
    unittest.main()
