"""Train diagnostic safety and sampling tests using invented fixtures only."""

import importlib.util
from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import tempfile
import types
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "diagnose_train_checkpoint", ROOT / "scripts/diagnose_train_checkpoint.py")
diagnostic = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(diagnostic)


class TrainBundleTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.base = Path(self.temporary.name)
        self.bundle = self.base / "review_bundle"
        self.bundle.mkdir()
        self.rows = []
        for group, split in (("a", "train"), ("b", "train"), ("c", "validation")):
            for language in ("en", "vi"):
                for value in ("NOW", "PAST"):
                    self.rows.append({"record_id": f"{group}-{language}-{value}",
                        "split_group_id": group, "language": language,
                        "action": {"kind": "TIME", "value": value}, "path_id": None,
                        "source_text": f"invented source {group}", "target_text": "invented target",
                        "source_frame_id": group + "-source", "target_frame_id": group + "-target"})
        self.groups = {"a": "train", "b": "train", "c": "validation"}
        self.frames = {group + suffix: {"invented_fixture": True}
                       for group in self.groups for suffix in ("-source", "-target")}
        self.write(self.bundle / "inventory.json", {})
        self.write(self.bundle / "alignments.json", {})
        self.write(self.bundle / "statement.json", {"human_validated": False, "phomt_used": False,
                                                   "review_scope": "train-validation-only"})
        # Full-corpus files are intentionally invalid: the loader must never use them.
        (self.base / "corpus.jsonl").write_text("do not parse this full corpus")
        (self.base / "semantic_frames.json").write_text("do not parse this full catalog")
        self.bind_bundle()

    def write(self, path, value):
        path.write_text(json.dumps(value), encoding="utf-8")

    def bind_bundle(self):
        self.write(self.bundle / "groups.json", self.groups)
        self.write(self.bundle / "semantic_frames.json", self.frames)
        (self.bundle / "records.jsonl").write_text(
            "\n".join(json.dumps(row) for row in self.rows) + "\n", encoding="utf-8")
        manifest = {"review_scope": "train-validation-only", "reviewed_records": len(self.rows),
                    "files_sha256": {path.name: diagnostic.sha256(path)
                                     for path in self.bundle.iterdir() if path.name != "manifest.json"}}
        self.write(self.bundle / "manifest.json", manifest)
        self.write(self.base / "protocol.json", {"review_scope": "train-validation-only",
            "reviewed_records": len(self.rows),
            "review_bundle_sha256": diagnostic.sha256(self.bundle / "manifest.json")})

    def tearDown(self):
        self.temporary.cleanup()

    def test_filters_train_singles_without_opening_full_corpus_or_catalog(self):
        _, rows, frames = diagnostic.load_train_bundle(self.base)
        self.assertEqual(len(rows), 8)
        self.assertEqual({row["split_group_id"] for row in rows}, {"a", "b"})
        self.assertEqual(set(frames), {"a-source", "a-target", "b-source", "b-target"})
        selected = diagnostic.select_train_sample(rows, per_bucket=2)
        self.assertEqual(len(selected), 8)

    def test_rejects_test_groups_even_with_updated_manifest_hash(self):
        self.groups["c"] = "test"
        self.bind_bundle()
        with self.assertRaisesRegex(ValueError, "test or unknown split"):
            diagnostic.load_train_bundle(self.base)

    def test_rejects_hash_drift_before_parsing_rows(self):
        (self.bundle / "records.jsonl").write_text("invalid JSON and changed identity")
        with self.assertRaisesRegex(ValueError, "file identity"):
            diagnostic.load_train_bundle(self.base)

    def test_rejects_unreferenced_frame_catalog_entries(self):
        self.frames["unreviewed-extra-frame"] = {"invented_fixture": True}
        self.bind_bundle()
        with self.assertRaisesRegex(ValueError, "frame inventory"):
            diagnostic.load_train_bundle(self.base)

    def test_rejects_duplicate_ids_and_unknown_groups(self):
        self.rows[-1]["record_id"] = self.rows[0]["record_id"]
        self.bind_bundle()
        with self.assertRaisesRegex(ValueError, "duplicate record IDs"):
            diagnostic.load_train_bundle(self.base)
        self.rows[-1]["record_id"] = "unique-again"
        self.rows[-1]["split_group_id"] = "unknown"
        self.bind_bundle()
        with self.assertRaisesRegex(ValueError, "unknown groups"):
            diagnostic.load_train_bundle(self.base)

    def test_sampling_is_order_independent_and_never_weights_row_duplicates(self):
        _, rows, _ = diagnostic.load_train_bundle(self.base)
        duplicated = {**rows[0], "record_id": "another-row-for-the-same-transition"}
        selected = diagnostic.select_train_sample(rows + [duplicated], per_bucket=2)
        reverse = diagnostic.select_train_sample(list(reversed(rows + [duplicated])), per_bucket=2)
        self.assertEqual(selected, reverse)
        self.assertEqual(len(selected), 8)
        self.assertEqual(len({(diagnostic.bucket_key(row), row["split_group_id"])
                              for row in selected}), 8)
        with self.assertRaisesRegex(ValueError, "insufficient distinct train groups"):
            diagnostic.select_train_sample(rows, per_bucket=3)

    def test_source_controls_match_bucket_but_change_group_and_text(self):
        _, rows, _ = diagnostic.load_train_bundle(self.base)
        controls = diagnostic.source_controls(rows)
        for row in rows:
            self.assertNotEqual(controls[row["record_id"]], row["source_text"])
        with self.assertRaisesRegex(ValueError, "another distinct train group/source"):
            diagnostic.source_controls(rows[:1])

    def validation_fixture(self):
        self.write(self.base / "data_statement.json", {"version": "invented-fixture"})
        self.write(self.base / "tide-fixture-seed-17.json", {"seed": 17, "objective": {"mode": "tide"},
                                                         "output_dir": "invented-run"})
        output = self.base / "invented-run"
        output.mkdir()
        values = [{"record_id": row["record_id"], "language": row["language"], "task": "single",
                   "target_frame": row["target_frame_id"],
                   "generated_text": "invented generated " + row["action"]["value"]}
                  for row in self.rows if row["split_group_id"] == "c"]
        (output / "generation.validation.private.jsonl").write_text(
            "\n".join(json.dumps(value) for value in values) + "\n", encoding="utf-8")

    def test_validation_preservation_uses_scoped_catalog_without_opening_full_catalog(self):
        self.validation_fixture()
        from scripts.diagnose_validation_preservation import diagnose
        flags = {"action_fidelity": True, "preservation": True, "agent_preserved": True,
                 "patient_preserved": True, "predicate_preserved": True, "place_preserved": True}
        with patch("scripts.diagnose_validation_preservation._semantic_frame_flags", return_value=flags), \
                redirect_stdout(io.StringIO()):
            report = diagnose(self.base)
        self.assertEqual(sum(value["examples"] for value in report["aggregate"].values()), 4)

    def test_validation_action_sensitivity_uses_scoped_rows_without_opening_full_corpus(self):
        self.validation_fixture()
        from scripts.diagnose_validation_action_sensitivity import diagnose
        values = diagnose(self.base)
        self.assertEqual(len(values), 2)
        self.assertTrue(all(value["source_pairs"] == 1 and value["different_outputs"] == 1
                            for value in values))


class AggregateTests(unittest.TestCase):
    def test_token_normalized_nll_and_sentence_denominators_remain_distinct(self):
        counts = {"examples": 2, "tokens_including_eos": 10, "teacher_forced_correct_tokens": 9,
            "teacher_forced_exact": 1, "greedy_exact": 0, "greedy_action_fidelity": 2,
            "greedy_preservation": 1, "greedy_predicate_preserved": 1,
            "greedy_patient_preserved": 2, "greedy_byte_edits_including_eos": 3,
            "gold_nll_sum": 2., "wrong_source_nll_sum": 7.,
            "wrong_action_nll_sum": 3., "zero_latent_nll_sum": 1.}
        rates = diagnostic.rates(counts)
        self.assertAlmostEqual(rates["teacher_forced_token_accuracy"], .9)
        self.assertAlmostEqual(rates["teacher_forced_exact_rate"], .5)
        self.assertAlmostEqual(rates["greedy_byte_edit_rate_including_eos"], .3)
        self.assertAlmostEqual(rates["wrong_source_nll_delta_per_token"], .5)
        self.assertAlmostEqual(rates["wrong_action_nll_delta_per_token"], .1)
        self.assertAlmostEqual(rates["zero_latent_nll_delta_per_token"], -.1)

    def test_training_preflight_blocks_a_bad_checker_before_launching_workers(self):
        from scripts.train_vi_en_parallel import checker_preflight
        with patch("scripts.audit_research_checker.audit", return_value={"status": "fail"}) as audit:
            with self.assertRaisesRegex(ValueError, "checker failed train-reference negative controls"):
                checker_preflight(Path("invented-fixture"), {"review_scope": "train-validation-only"})
            audit.assert_called_once_with(Path("invented-fixture"), implementation="frozen")

    def test_frozen_loader_reuses_its_package_but_rejects_mixed_cached_submodules(self):
        import sys
        from scripts.run_frozen import load_frozen_package
        with tempfile.TemporaryDirectory() as temporary:
            snapshot = Path(temporary)
            module = types.ModuleType("tide_jepa")
            module.__file__ = str(snapshot / "__init__.py")
            with patch.dict(sys.modules), patch("scripts.run_frozen.verify_snapshot", return_value=snapshot):
                for name in list(sys.modules):
                    if name == "tide_jepa" or name.startswith("tide_jepa."):
                        del sys.modules[name]
                sys.modules["tide_jepa"] = module
                self.assertEqual(load_frozen_package("invented-fixture"), snapshot)
                mixed = types.ModuleType("tide_jepa.model")
                mixed.__file__ = str(ROOT / "tide_jepa/model.py")
                sys.modules["tide_jepa.model"] = mixed
                with self.assertRaisesRegex(RuntimeError, "another tide_jepa implementation"):
                    load_frozen_package("invented-fixture")


if __name__ == "__main__":
    unittest.main()
