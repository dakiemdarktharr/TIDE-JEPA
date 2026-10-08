"""Integration checks use original synthetic fixtures only, never PhoMT rows."""

from contextlib import redirect_stdout
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

from tide_jepa.phomt_intake import TRAIN_MEMBERS, _select_pairs
from tide_jepa.data import dataset_fingerprint, read_jsonl
from tide_jepa.pilot_seed import (FAMILIES_V43, FAMILIES_V44, FAMILIES_V45,
                                  FAMILIES_V46, FAMILIES_V47, FAMILIES_V48,
                                  FAMILIES_V49, FAMILIES_V410, FAMILIES_V411, FAMILIES_V412, FAMILIES_V413, FAMILIES_V414, FAMILIES_V415, FAMILIES_V416, FAMILIES_V417, FAMILIES_V418, FAMILIES_V419, FAMILIES_V420, FAMILIES_V421, FAMILIES_V422, FAMILIES_V423, FAMILIES_V424, FAMILIES_V425, author_seed,
                                  author_seed_v4)
from tide_jepa.schema import Action, Inventory

TORCH_AVAILABLE = importlib.util.find_spec("torch") is not None


class SourceSelectionTests(unittest.TestCase):
    def make_zip(self, en, vi):
        memory = io.BytesIO()
        with zipfile.ZipFile(memory, "w") as archive:
            archive.writestr(TRAIN_MEMBERS[0], en)
            archive.writestr(TRAIN_MEMBERS[1], vi)
            archive.writestr("PhoMT/detokenization/test/test.en", b"DO NOT READ")
        memory.seek(0)
        return zipfile.ZipFile(memory)

    def test_selection_is_deterministic_and_reads_train_only(self):
        en = "\n".join(f"original test English {n}" for n in range(50))
        vi = "\n".join(f"ví dụ tự tạo {n}" for n in range(50))
        with self.make_zip(en, vi) as archive:
            first = _select_pairs(archive, count=5, seed=7, max_bytes=128)
        with self.make_zip(en, vi) as archive:
            second = _select_pairs(archive, count=5, seed=7, max_bytes=128)
        self.assertEqual(first, second)
        self.assertEqual(first[1:], (50, 50))
        self.assertTrue(all("DO NOT READ" not in pair["en"] for pair in first[0]))

    def test_pair_count_mismatch_and_bad_utf8_fail_without_text(self):
        with self.make_zip(b"private-test-only\nextra\n", b"one\n") as archive:
            with self.assertRaisesRegex(ValueError, "different line counts"):
                _select_pairs(archive, count=5, seed=7, max_bytes=128)
        with self.make_zip(b"secret-fixture\xff", b"one") as archive:
            with self.assertRaises(ValueError) as raised:
                _select_pairs(archive, count=5, seed=7, max_bytes=128)
        self.assertNotIn("secret-fixture", str(raised.exception))

    def test_empty_long_and_duplicate_source_sentences_are_filtered(self):
        with self.make_zip("Same\nsame\n\nvery long content\n", "Một\nHai\nBa\nBốn\n") as archive:
            pairs, total, eligible = _select_pairs(archive, count=10, seed=7, max_bytes=10)
        self.assertEqual(total, 4)
        self.assertEqual(eligible, 2)
        self.assertEqual(len(pairs), 1)


class SeedAuthoringTests(unittest.TestCase):
    def test_v433_release_amendment_binds_current_checker_and_reassessment(self):
        from tide_jepa.experiment import _implementation_identity, _runtime_identity
        from tide_jepa.pilot import _load_v433_checker_reassessment

        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            (base / "data_statement.json").write_text(json.dumps({"version": "vi-en-ai-v4.33"}))
            protocol = {"runtime": _runtime_identity(), "implementation_sha256": {"old": "frozen"},
                        "quality_thresholds": {"valid_unicode_rate": 1.0}}
            protocol_path = base / "protocol.json"
            protocol_path.write_text(json.dumps(protocol))
            pilot_file = Path(__import__("tide_jepa.pilot", fromlist=["__file__"]).__file__)
            report = {"schema_version": "v433-semantic-checker-reassessment-v1",
                      "pilot_version": "vi-en-ai-v4.33", "release_holdout_opened": False,
                      "human_validated": False, "phomt_used": False,
                      "corrected_checker_sha256": hashlib.sha256(pilot_file.read_bytes()).hexdigest(),
                      "runs": [{"run": "seed17.json", "primary": True, "gate": "pass"}]}
            report_path = base / "reassessment.json"
            report_path.write_text(json.dumps(report))
            current = _implementation_identity()
            amendment = {
                "schema_version": "v433-release-test-amendment-v1",
                "protocol_sha256": hashlib.sha256(protocol_path.read_bytes()).hexdigest(),
                "frozen_implementation_sha256": protocol["implementation_sha256"],
                "amended_evaluator_sha256": {key: value for key, value in current.items()
                                             if key in {"pilot.py", "infer.py", "data.py"}},
                "runtime": protocol["runtime"], "quality_thresholds": protocol["quality_thresholds"],
                "validation_reassessment": "reassessment.json",
                "validation_reassessment_sha256": hashlib.sha256(report_path.read_bytes()).hexdigest(),
                "primary_configs": ["seed17.json"],
            }
            (base / "release_test_amendment.json").write_text(json.dumps(amendment))
            self.assertEqual(_load_v433_checker_reassessment(base, protocol)["entries"]["seed17.json"]["gate"],
                             "pass")
            report["release_holdout_opened"] = True
            report_path.write_text(json.dumps(report))
            with self.assertRaisesRegex(ValueError, "checker amendment identity"):
                _load_v433_checker_reassessment(base, protocol)

    def test_registered_primary_matrix_includes_decoder_and_rejects_duplicates(self):
        from tide_jepa.pilot import _registered_primary_configs
        protocol = {"primary_quality_mode": "tide", "seeds": [17, 23],
                    "primary_source_copy_weights": [0.0], "primary_latent_objective_weights": [0.0],
                    "primary_source_pointer_decoder_modes": ["vocabulary", "source_pointer"]}
        configs = [(f"{seed}-{pointer}.json", {
            "seed": seed, "objective": {"mode": "tide", "latent_objective_weight": 0.0},
            "model": {"source_pointer_decoder": pointer}})
            for seed in protocol["seeds"] for pointer in (False, True)]
        self.assertEqual(_registered_primary_configs(protocol, configs), configs)
        for invalid in (configs[:-1], configs + [configs[0]], configs[:-1] + [configs[0]]):
            with self.assertRaisesRegex(ValueError, "decoder condition"):
                _registered_primary_configs(protocol, invalid)

    def test_quality_gate_applies_to_frozen_primary_mode_only(self):
        from tide_jepa.pilot import _quality_gate_status
        passing = {"en/single/action": {"valid_unicode_pass": True,
                                        "semantic_checker_coverage_pass": True,
                                        "action_fidelity_pass": True}}
        failing = {"en/single/action": {"valid_unicode_pass": True,
                                        "semantic_checker_coverage_pass": True,
                                        "action_fidelity_pass": False}}
        uncovered = {"en/single/action": {"valid_unicode_pass": True,
                                          "semantic_checker_coverage_pass": False,
                                          "action_fidelity_pass": True}}
        self.assertEqual(_quality_gate_status("tide", "tide", passing), "pass")
        self.assertEqual(_quality_gate_status("tide", "tide", failing), "fail")
        self.assertEqual(_quality_gate_status("tide", "tide", uncovered), "fail")
        self.assertEqual(_quality_gate_status("tide", "token_only", failing), "control_only")
        self.assertEqual(_quality_gate_status("tide", "tide", {"bucket": {}}), "fail")
        self.assertEqual(_quality_gate_status("tide", "tide", {"bucket": {"pass": "false"}}), "fail")
        self.assertEqual(_quality_gate_status("tide", "tide", {}), "fail")

    def test_v43_is_frame_disjoint_compositional_split(self):
        train = FAMILIES_V43["train"]
        validation = FAMILIES_V43["validation"]
        test = FAMILIES_V43["test"]
        components = lambda rows, position: {row[position] for row in rows}
        self.assertEqual((len(train), len(validation), len(test)), (20, 6, 6))
        self.assertEqual(len({row[0] for row in train + validation + test}), 32)
        self.assertFalse(set(row[0] for row in train) & set(row[0] for row in validation + test))
        for held_out in (validation, test):
            for position in (1, 2, 5):
                self.assertLessEqual(components(held_out, position), components(train, position),
                                     "held-out combination contains an unseen lexical component")
        train_triples = {(row[1], row[2], row[5]) for row in train}
        self.assertFalse(train_triples & {(row[1], row[2], row[5]) for row in validation + test})
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "v4.3"
            statement = author_seed_v4(destination, version="v4.3")
            inventory_value = json.loads((destination / "inventory.draft.json").read_text(encoding="utf-8"))
            actions = tuple(Action(**value) for value in inventory_value["actions"])
            inventory = Inventory(actions, {
                language: frozenset(Action(**value) for value in inventory_value["proposed_by_language"][language])
                for language in ("en", "vi")
            })
            rows = read_jsonl(destination / "corpus.draft.jsonl", inventory,
                              languages=("en", "vi"), require_approved=False)
            groups = json.loads((destination / "groups.json").read_text(encoding="utf-8"))
            self.assertEqual(len(rows), 1280)
            self.assertEqual(statement["draft_sha256"], dataset_fingerprint(rows))
            self.assertEqual({name: list(groups.values()).count(name)
                              for name in ("train", "validation", "test")},
                             {"train": 20, "validation": 6, "test": 6})
            self.assertFalse(statement["human_validated"])

    def test_v44_is_compositional_split_with_seen_lexical_components(self):
        train = FAMILIES_V44["train"]
        validation = FAMILIES_V44["validation"]
        test = FAMILIES_V44["test"]
        component_set = lambda rows, positions: {row[position] for row in rows for position in positions}
        self.assertEqual((len(train), len(validation), len(test)), (80, 12, 12))
        self.assertEqual(len({row[0] for row in train + validation + test}), 104)
        train_triples = {(row[1], row[2], row[5]) for row in train}
        heldout_triples = {(row[1], row[2], row[5]) for row in validation + test}
        self.assertFalse(train_triples & heldout_triples)
        for held_out in (validation, test):
            self.assertLessEqual(component_set(held_out, (1, 2, 5)),
                                 component_set(train, (1, 2, 5)))
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "v4.4"
            statement = author_seed_v4(destination, version="v4.4")
            inventory_value = json.loads((destination / "inventory.draft.json").read_text(encoding="utf-8"))
            actions = tuple(Action(**value) for value in inventory_value["actions"])
            inventory = Inventory(actions, {
                language: frozenset(Action(**value) for value in inventory_value["proposed_by_language"][language])
                for language in ("en", "vi")
            })
            rows = read_jsonl(destination / "corpus.draft.jsonl", inventory,
                              languages=("en", "vi"), require_approved=False)
            groups = json.loads((destination / "groups.json").read_text(encoding="utf-8"))
            self.assertEqual(len(rows), 4160)
            self.assertEqual(statement["draft_sha256"], dataset_fingerprint(rows))
            self.assertEqual({name: list(groups.values()).count(name)
                              for name in ("train", "validation", "test")},
                             {"train": 80, "validation": 12, "test": 12})
            self.assertFalse(statement["human_validated"])

    def test_v45_uses_new_combinations_and_covers_train_lexicon(self):
        train = FAMILIES_V45["train"]
        validation = FAMILIES_V45["validation"]
        test = FAMILIES_V45["test"]
        combinations = lambda rows: {(row[1], row[2], row[5]) for row in rows}
        components = lambda rows, position: {row[position] for row in rows}
        prior = {tuple(map(int, row[0].removeprefix("compose_").split("_")))
                 for families in FAMILIES_V44.values() for row in families}
        train_combinations = combinations(train)
        held_out_combinations = combinations(validation + test)
        self.assertEqual((len(train), len(validation), len(test)), (80, 12, 12))
        self.assertEqual(len(train_combinations | held_out_combinations), 104)
        self.assertFalse(train_combinations & held_out_combinations)
        prior_surfaces = {(FAMILIES_V44[split][index][1], FAMILIES_V44[split][index][2],
                           FAMILIES_V44[split][index][5])
                          for split in FAMILIES_V44 for index in range(len(FAMILIES_V44[split]))}
        self.assertEqual(len(prior), 104)
        self.assertFalse((train_combinations | held_out_combinations) & prior_surfaces)
        for held_out in (validation, test):
            for position in (1, 2, 5):
                self.assertLessEqual(components(held_out, position), components(train, position))
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "v4.5"
            statement = author_seed_v4(destination, version="v4.5")
            inventory_value = json.loads((destination / "inventory.draft.json").read_text(encoding="utf-8"))
            actions = tuple(Action(**value) for value in inventory_value["actions"])
            inventory = Inventory(actions, {
                language: frozenset(Action(**value) for value in inventory_value["proposed_by_language"][language])
                for language in ("en", "vi")
            })
            rows = read_jsonl(destination / "corpus.draft.jsonl", inventory,
                              languages=("en", "vi"), require_approved=False)
            groups = json.loads((destination / "groups.json").read_text(encoding="utf-8"))
            self.assertEqual(len(rows), 4160)
            self.assertEqual(statement["draft_sha256"], dataset_fingerprint(rows))
            self.assertEqual({name: list(groups.values()).count(name)
                              for name in ("train", "validation", "test")},
                             {"train": 80, "validation": 12, "test": 12})
            self.assertFalse(statement["human_validated"])

    def test_v46_progressive_grammar_and_fresh_combinations(self):
        train = FAMILIES_V46["train"]
        validation = FAMILIES_V46["validation"]
        test = FAMILIES_V46["test"]
        prior = set()
        for family_map, prefix in ((FAMILIES_V44, "compose_"),
                                   (FAMILIES_V45, "compose45_")):
            prior.update(tuple(map(int, row[0].removeprefix(prefix).split("_")))
                         for families in family_map.values() for row in families)
        current = {tuple(map(int, row[0].removeprefix("compose46_").split("_")))
                   for row in train + validation + test}
        self.assertEqual((len(train), len(validation), len(test)), (80, 12, 12))
        self.assertEqual(len(current), 104)
        self.assertFalse(current & prior)
        for held_out in (validation, test):
            for position in (1, 2, 5):
                self.assertLessEqual({row[position] for row in held_out},
                                     {row[position] for row in train})
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "v4.6"
            statement = author_seed_v4(destination, version="v4.6")
            inventory_value = json.loads((destination / "inventory.draft.json").read_text(encoding="utf-8"))
            actions = tuple(Action(**value) for value in inventory_value["actions"])
            inventory = Inventory(actions, {
                language: frozenset(Action(**value) for value in inventory_value["proposed_by_language"][language])
                for language in ("en", "vi")
            })
            rows = read_jsonl(destination / "corpus.draft.jsonl", inventory,
                              languages=("en", "vi"), require_approved=False)
            frames = json.loads((destination / "semantic_frames.draft.json").read_text(encoding="utf-8"))
            from tide_jepa.pilot import _semantic_frame_flags
            self.assertEqual(len(rows), 4160)
            self.assertTrue(all((lambda flags: flags["action_fidelity"] and flags["preservation"])(
                                _semantic_frame_flags(row.target_text, row.language,
                                                      frames[row.target_frame_id]))
                                for row in rows))
            self.assertEqual(statement["draft_sha256"], dataset_fingerprint(rows))
            self.assertFalse(statement["human_validated"])
            self.assertFalse(statement["phomt_used"])

    def test_v47_pairwise_covered_compositional_holdout(self):
        train = FAMILIES_V47["train"]
        validation = FAMILIES_V47["validation"]
        test = FAMILIES_V47["test"]
        prior = set()
        for family_map, prefix in ((FAMILIES_V44, "compose_"),
                                   (FAMILIES_V45, "compose45_"),
                                   (FAMILIES_V46, "compose46_")):
            prior.update(tuple(map(int, row[0].removeprefix(prefix).split("_")))
                         for families in family_map.values() for row in families)
        current = {tuple(map(int, row[0].removeprefix("compose47_").split("_")))
                   for row in train + validation + test}
        self.assertEqual((len(train), len(validation), len(test)), (120, 40, 40))
        self.assertEqual(len(current), 200)
        self.assertFalse(current & prior)

        def factor_pairs(families):
            triples = [tuple(map(int, row[0].removeprefix("compose47_").split("_")))
                       for row in families]
            return ({(a, v) for a, v, _ in triples},
                    {(a, p) for a, _, p in triples},
                    {(v, p) for _, v, p in triples})

        train_pairs = factor_pairs(train)
        self.assertEqual(tuple(map(len, train_pairs)), (62, 63, 64))
        for held_out in (validation, test):
            held_pairs = factor_pairs(held_out)
            for observed, covered in zip(held_pairs, train_pairs):
                self.assertLessEqual(observed, covered)
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "v4.7"
            statement = author_seed_v4(destination, version="v4.7")
            inventory_value = json.loads((destination / "inventory.draft.json").read_text(encoding="utf-8"))
            actions = tuple(Action(**value) for value in inventory_value["actions"])
            inventory = Inventory(actions, {
                language: frozenset(Action(**value) for value in inventory_value["proposed_by_language"][language])
                for language in ("en", "vi")
            })
            rows = read_jsonl(destination / "corpus.draft.jsonl", inventory,
                              languages=("en", "vi"), require_approved=False)
            groups = json.loads((destination / "groups.json").read_text(encoding="utf-8"))
            self.assertEqual(len(rows), 8000)
            self.assertEqual(statement["draft_sha256"], dataset_fingerprint(rows))
            self.assertEqual({name: list(groups.values()).count(name)
                              for name in ("train", "validation", "test")},
                             {"train": 120, "validation": 40, "test": 40})
            self.assertFalse(statement["human_validated"])

    def test_v48_new_agent_factor_holdout_has_train_covered_pairs(self):
        train = FAMILIES_V48["train"]
        validation = FAMILIES_V48["validation"]
        test = FAMILIES_V48["test"]
        prior = set()
        for family_map, prefix in ((FAMILIES_V44, "compose_"),
                                   (FAMILIES_V45, "compose45_"),
                                   (FAMILIES_V46, "compose46_"),
                                   (FAMILIES_V47, "compose47_")):
            prior.update(tuple(map(int, row[0].removeprefix(prefix).split("_")))
                         for families in family_map.values() for row in families)
        current = {tuple(map(int, row[0].removeprefix("compose48_").split("_")))
                   for row in train + validation + test}
        self.assertEqual((len(train), len(validation), len(test)), (112, 40, 40))
        self.assertEqual(len(current), 192)
        self.assertTrue(all(agent >= 8 for agent, _, _ in current))
        self.assertFalse(current & prior)

        def factor_pairs(families):
            triples = [tuple(map(int, row[0].removeprefix("compose48_").split("_")))
                       for row in families]
            return ({(agent, verb) for agent, verb, _ in triples},
                    {(agent, patient) for agent, _, patient in triples},
                    {(verb, patient) for _, verb, patient in triples})

        train_pairs = factor_pairs(train)
        for held_out in (validation, test):
            for observed, covered in zip(factor_pairs(held_out), train_pairs):
                self.assertLessEqual(observed, covered)

        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "v4.12"
            statement = author_seed_v4(destination, version="v4.12")
            inventory_value = json.loads((destination / "inventory.draft.json").read_text(encoding="utf-8"))
            inventory = Inventory(tuple(Action(**value) for value in inventory_value["actions"]), {
                language: frozenset(Action(**value) for value in inventory_value["proposed_by_language"][language])
                for language in ("en", "vi")
            })
            rows = read_jsonl(destination / "corpus.draft.jsonl", inventory,
                              languages=("en", "vi"), require_approved=False)
            frames = json.loads((destination / "semantic_frames.draft.json").read_text(encoding="utf-8"))
            from tide_jepa.pilot import _semantic_frame_flags
            self.assertEqual(len(rows), 7680)
            self.assertEqual(statement["draft_sha256"], dataset_fingerprint(rows))
            self.assertIn("matched source-copy ablation", statement["split_policy"])
            self.assertFalse(statement["phomt_used"])
            self.assertFalse(statement["human_validated"])
            self.assertTrue(all((lambda flags: flags and flags["action_fidelity"] and flags["preservation"])(
                _semantic_frame_flags(row.target_text, row.language, frames[row.target_frame_id]))
                for row in rows))
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "v4.8"
            statement = author_seed_v4(destination, version="v4.8")
            inventory_value = json.loads((destination / "inventory.draft.json").read_text(encoding="utf-8"))
            actions = tuple(Action(**value) for value in inventory_value["actions"])
            inventory = Inventory(actions, {
                language: frozenset(Action(**value) for value in inventory_value["proposed_by_language"][language])
                for language in ("en", "vi")
            })
            rows = read_jsonl(destination / "corpus.draft.jsonl", inventory,
                              languages=("en", "vi"), require_approved=False)
            groups = json.loads((destination / "groups.json").read_text(encoding="utf-8"))
            frames = json.loads((destination / "semantic_frames.draft.json").read_text(encoding="utf-8"))
            from tide_jepa.pilot import _semantic_frame_flags
            self.assertEqual(len(rows), 7680)
            self.assertTrue(all((lambda flags: flags and flags["action_fidelity"] and flags["preservation"])(
                                _semantic_frame_flags(row.target_text, row.language,
                                                      frames[row.target_frame_id]))
                                for row in rows))
            self.assertEqual(statement["draft_sha256"], dataset_fingerprint(rows))
            self.assertEqual({name: list(groups.values()).count(name)
                              for name in ("train", "validation", "test")},
                             {"train": 112, "validation": 40, "test": 40})
            self.assertFalse(statement["human_validated"])

    def test_v49_uses_fresh_agents_and_train_covered_holdout_pairs(self):
        train, validation, test = (FAMILIES_V49[name]
                                   for name in ("train", "validation", "test"))
        self.assertEqual((len(train), len(validation), len(test)), (112, 40, 40))
        self.assertTrue(all(row[0].startswith("compose49_") for row in train + validation + test))
        self.assertEqual({row[1] for row in train + validation + test}, {"Kieu", "Thien", "Oanh"})

        def factor_pairs(families):
            triples = [tuple(map(int, row[0].removeprefix("compose49_").split("_")))
                       for row in families]
            return ({(agent, verb) for agent, verb, _ in triples},
                    {(agent, patient) for agent, _, patient in triples},
                    {(verb, patient) for _, verb, patient in triples})

        train_pairs = factor_pairs(train)
        for held_out in (validation, test):
            for observed, covered in zip(factor_pairs(held_out), train_pairs):
                self.assertLessEqual(observed, covered)
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "v4.9"
            statement = author_seed_v4(destination, version="v4.9")
            inventory_value = json.loads((destination / "inventory.draft.json").read_text(encoding="utf-8"))
            actions = tuple(Action(**value) for value in inventory_value["actions"])
            inventory = Inventory(actions, {
                language: frozenset(Action(**value) for value in inventory_value["proposed_by_language"][language])
                for language in ("en", "vi")
            })
            rows = read_jsonl(destination / "corpus.draft.jsonl", inventory,
                              languages=("en", "vi"), require_approved=False)
            groups = json.loads((destination / "groups.json").read_text(encoding="utf-8"))
            frames = json.loads((destination / "semantic_frames.draft.json").read_text(encoding="utf-8"))
            from tide_jepa.pilot import _semantic_frame_flags
            self.assertEqual(len(rows), 7680)
            self.assertTrue(all((lambda flags: flags and flags["action_fidelity"] and flags["preservation"])(
                                _semantic_frame_flags(row.target_text, row.language,
                                                      frames[row.target_frame_id]))
                                for row in rows))
            self.assertEqual(statement["draft_sha256"], dataset_fingerprint(rows))
            self.assertEqual({name: list(groups.values()).count(name)
                              for name in ("train", "validation", "test")},
                             {"train": 112, "validation": 40, "test": 40})
            self.assertFalse(statement["human_validated"])

    def test_v410_holdout_is_fresh_and_pairs_are_train_covered(self):
        train, validation, test = (FAMILIES_V410[name]
                                   for name in ("train", "validation", "test"))
        self.assertEqual((len(train), len(validation), len(test)), (112, 40, 40))
        self.assertTrue(all(row[0].startswith("compose410_") for row in train + validation + test))
        self.assertEqual({row[1] for row in train + validation + test}, {"Nhu", "Tuyen", "Loc"})

        def triples(families, prefix):
            return {tuple(map(int, row[0].removeprefix(prefix).split("_"))) for row in families}

        prior_v49 = triples(sum(FAMILIES_V49.values(), []), "compose49_")
        current_v410 = triples(train + validation + test, "compose410_")
        self.assertFalse(prior_v49 & current_v410)

        def factor_pairs(families):
            triples = [tuple(map(int, row[0].removeprefix("compose410_").split("_")))
                       for row in families]
            return ({(agent, verb) for agent, verb, _ in triples},
                    {(agent, patient) for agent, _, patient in triples},
                    {(verb, patient) for _, verb, patient in triples})

        train_pairs = factor_pairs(train)
        for held_out in (validation, test):
            for observed, covered in zip(factor_pairs(held_out), train_pairs):
                self.assertLessEqual(observed, covered)
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "v4.10"
            statement = author_seed_v4(destination, version="v4.10")
            inventory_value = json.loads((destination / "inventory.draft.json").read_text(encoding="utf-8"))
            actions = tuple(Action(**value) for value in inventory_value["actions"])
            inventory = Inventory(actions, {
                language: frozenset(Action(**value) for value in inventory_value["proposed_by_language"][language])
                for language in ("en", "vi")
            })
            rows = read_jsonl(destination / "corpus.draft.jsonl", inventory,
                              languages=("en", "vi"), require_approved=False)
            groups = json.loads((destination / "groups.json").read_text(encoding="utf-8"))
            frames = json.loads((destination / "semantic_frames.draft.json").read_text(encoding="utf-8"))
            from tide_jepa.pilot import _semantic_frame_flags
            self.assertEqual(len(rows), 7680)
            self.assertTrue(all((lambda flags: flags and flags["action_fidelity"] and flags["preservation"])(
                                _semantic_frame_flags(row.target_text, row.language,
                                                      frames[row.target_frame_id]))
                                for row in rows))
            self.assertEqual(statement["draft_sha256"], dataset_fingerprint(rows))
            self.assertEqual({name: list(groups.values()).count(name)
                              for name in ("train", "validation", "test")},
                             {"train": 112, "validation": 40, "test": 40})
            self.assertFalse(statement["human_validated"])

    def test_v411_holdout_is_fresh_and_copy_focused_draft_is_valid(self):
        train, validation, test = (FAMILIES_V411[name]
                                   for name in ("train", "validation", "test"))
        self.assertEqual((len(train), len(validation), len(test)), (112, 40, 40))
        all_rows = train + validation + test
        self.assertTrue(all(row[0].startswith("compose411_") for row in all_rows))
        self.assertEqual({row[1] for row in all_rows}, {"Kha My", "Tuan Kiet", "An Vy"})

        def triples(families, prefix):
            return {tuple(map(int, row[0].removeprefix(prefix).split("_"))) for row in families}

        current = triples(all_rows, "compose411_")
        prior_v49 = triples(sum(FAMILIES_V49.values(), []), "compose49_")
        prior_v410 = triples(sum(FAMILIES_V410.values(), []), "compose410_")
        self.assertFalse(current & prior_v49)
        self.assertFalse(current & prior_v410)

        def factor_pairs(families):
            values = [tuple(map(int, row[0].removeprefix("compose411_").split("_")))
                      for row in families]
            return ({(agent, verb) for agent, verb, _ in values},
                    {(agent, patient) for agent, _, patient in values},
                    {(verb, patient) for _, verb, patient in values})

        train_pairs = factor_pairs(train)
        for held_out in (validation, test):
            for observed, covered in zip(factor_pairs(held_out), train_pairs):
                self.assertLessEqual(observed, covered)

        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "v4.11"
            statement = author_seed_v4(destination, version="v4.11")
            inventory_value = json.loads((destination / "inventory.draft.json").read_text(encoding="utf-8"))
            actions = tuple(Action(**value) for value in inventory_value["actions"])
            inventory = Inventory(actions, {
                language: frozenset(Action(**value) for value in inventory_value["proposed_by_language"][language])
                for language in ("en", "vi")
            })
            rows = read_jsonl(destination / "corpus.draft.jsonl", inventory,
                              languages=("en", "vi"), require_approved=False)
            groups = json.loads((destination / "groups.json").read_text(encoding="utf-8"))
            frames = json.loads((destination / "semantic_frames.draft.json").read_text(encoding="utf-8"))
            from tide_jepa.pilot import _semantic_frame_flags
            self.assertEqual(len(rows), 7680)
            self.assertTrue(all((lambda flags: flags and flags["action_fidelity"] and flags["preservation"])(
                                _semantic_frame_flags(row.target_text, row.language,
                                                      frames[row.target_frame_id]))
                                for row in rows))
            self.assertEqual(statement["draft_sha256"], dataset_fingerprint(rows))
            self.assertFalse(statement["human_validated"])

    def test_v412_holdout_is_fresh_for_matched_copy_loss_ablation(self):
        train, validation, test = (FAMILIES_V412[name]
                                   for name in ("train", "validation", "test"))
        self.assertEqual((len(train), len(validation), len(test)), (112, 40, 40))
        all_rows = train + validation + test
        self.assertTrue(all(row[0].startswith("compose412_") for row in all_rows))
        self.assertEqual({row[1] for row in all_rows}, {"My Dung", "Quoc Bao", "Thao Nhi"})

        def triples(families, prefix):
            return {tuple(map(int, row[0].removeprefix(prefix).split("_"))) for row in families}

        current = triples(all_rows, "compose412_")
        for previous, prefix in ((FAMILIES_V49, "compose49_"),
                                 (FAMILIES_V410, "compose410_"),
                                 (FAMILIES_V411, "compose411_")):
            self.assertFalse(current & triples(sum(previous.values(), []), prefix))

        def factor_pairs(families):
            values = [tuple(map(int, row[0].removeprefix("compose412_").split("_")))
                      for row in families]
            return ({(agent, verb) for agent, verb, _ in values},
                    {(agent, patient) for agent, _, patient in values},
                    {(verb, patient) for _, verb, patient in values})

        train_pairs = factor_pairs(train)
        for held_out in (validation, test):
            for observed, covered in zip(factor_pairs(held_out), train_pairs):
                self.assertLessEqual(observed, covered)

        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "v4.12"
            statement = author_seed_v4(destination, version="v4.12")
            inventory_value = json.loads((destination / "inventory.draft.json").read_text(encoding="utf-8"))
            inventory = Inventory(tuple(Action(**value) for value in inventory_value["actions"]), {
                language: frozenset(Action(**value) for value in inventory_value["proposed_by_language"][language])
                for language in ("en", "vi")
            })
            rows = read_jsonl(destination / "corpus.draft.jsonl", inventory,
                              languages=("en", "vi"), require_approved=False)
            frames = json.loads((destination / "semantic_frames.draft.json").read_text(encoding="utf-8"))
            from tide_jepa.pilot import _semantic_frame_flags
            self.assertEqual(len(rows), 7680)
            self.assertEqual(statement["draft_sha256"], dataset_fingerprint(rows))
            self.assertIn("matched source-copy ablation", statement["split_policy"])
            self.assertFalse(statement["phomt_used"])
            self.assertFalse(statement["human_validated"])
            self.assertTrue(all((lambda flags: flags and flags["action_fidelity"] and flags["preservation"])(
                _semantic_frame_flags(row.target_text, row.language, frames[row.target_frame_id]))
                for row in rows))

    def test_v413_dose_response_corpus_has_fresh_agents_and_pairwise_covered_holdout(self):
        train, validation, test = (FAMILIES_V413[name]
                                   for name in ("train", "validation", "test"))
        self.assertEqual((len(train), len(validation), len(test)), (112, 40, 40))
        all_rows = train + validation + test
        self.assertTrue(all(row[0].startswith("compose413_") for row in all_rows))
        self.assertEqual({row[1] for row in all_rows}, {"Bao Tram", "Huu Phuoc", "Gia Han"})

        def triples(families, prefix="compose413_"):
            return {tuple(map(int, row[0].removeprefix(prefix).split("_"))) for row in families}

        current = triples(all_rows)
        self.assertEqual(len(current), 192)
        for previous, prefix in ((FAMILIES_V49, "compose49_"),
                                 (FAMILIES_V410, "compose410_"),
                                 (FAMILIES_V411, "compose411_"),
                                 (FAMILIES_V412, "compose412_")):
            self.assertFalse(current & triples(sum(previous.values(), []), prefix))

        def factor_pairs(families):
            values = triples(families)
            return ({(agent, verb) for agent, verb, _ in values},
                    {(agent, patient) for agent, _, patient in values},
                    {(verb, patient) for _, verb, patient in values})

        train_pairs = factor_pairs(train)
        for held_out in (validation, test):
            for observed, covered in zip(factor_pairs(held_out), train_pairs):
                self.assertLessEqual(observed, covered)

        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "v4.13"
            statement = author_seed_v4(destination, version="v4.13")
            inventory_value = json.loads((destination / "inventory.draft.json").read_text(encoding="utf-8"))
            inventory = Inventory(tuple(Action(**value) for value in inventory_value["actions"]), {
                language: frozenset(Action(**value) for value in inventory_value["proposed_by_language"][language])
                for language in ("en", "vi")
            })
            rows = read_jsonl(destination / "corpus.draft.jsonl", inventory,
                              languages=("en", "vi"), require_approved=False)
            frames = json.loads((destination / "semantic_frames.draft.json").read_text(encoding="utf-8"))
            from tide_jepa.pilot import _semantic_frame_flags
            self.assertEqual(statement["records"], 7680)
            self.assertIn("source-copy dose-response", statement["split_policy"])
            self.assertFalse(statement["phomt_used"])
            self.assertFalse(statement["human_validated"])
            self.assertEqual(statement["draft_sha256"], dataset_fingerprint(rows))
            self.assertTrue(all((lambda flags: flags and flags["action_fidelity"] and flags["preservation"])(
                _semantic_frame_flags(row.target_text, row.language, frames[row.target_frame_id]))
                for row in rows))

    def test_v414_adds_balanced_context_forms_on_a_fresh_pairwise_split(self):
        train, validation, test = (FAMILIES_V414[name]
                                   for name in ("train", "validation", "test"))
        all_families = train + validation + test
        self.assertEqual((len(train), len(validation), len(test)), (112, 40, 40))
        self.assertTrue(all(row[0].startswith("compose414_") for row in all_families))
        self.assertEqual({row[1] for row in all_families}, {"Ngoc Mai", "Tuan Anh", "Khanh Vy"})

        def triples(families):
            return {tuple(map(int, row[0].removeprefix("compose414_").split("_")))
                    for row in families}

        current = triples(all_families)
        self.assertEqual(len(current), 192)
        for prior, prefix in ((FAMILIES_V49, "compose49_"),
                              (FAMILIES_V410, "compose410_"),
                              (FAMILIES_V411, "compose411_"),
                              (FAMILIES_V412, "compose412_"),
                              (FAMILIES_V413, "compose413_")):
            previous = {tuple(map(int, row[0].removeprefix(prefix).split("_")))
                        for row in sum(prior.values(), [])}
            self.assertFalse(current & previous)

        def factor_pairs(families):
            values = triples(families)
            return ({(a, v) for a, v, _ in values}, {(a, p) for a, _, p in values},
                    {(v, p) for _, v, p in values})

        train_pairs = factor_pairs(train)
        for held_out in (validation, test):
            for observed, covered in zip(factor_pairs(held_out), train_pairs):
                self.assertLessEqual(observed, covered)

        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "v4.14"
            statement = author_seed_v4(destination, version="v4.14")
            inventory_value = json.loads((destination / "inventory.draft.json").read_text(encoding="utf-8"))
            inventory = Inventory(tuple(Action(**value) for value in inventory_value["actions"]), {
                language: frozenset(Action(**value) for value in inventory_value["proposed_by_language"][language])
                for language in ("en", "vi")
            })
            rows = read_jsonl(destination / "corpus.draft.jsonl", inventory,
                              languages=("en", "vi"), require_approved=False)
            frames = json.loads((destination / "semantic_frames.draft.json").read_text(encoding="utf-8"))
            from tide_jepa.pilot import _semantic_frame_flags
            self.assertEqual(statement["records"], 15360)
            self.assertEqual(statement["surface_realizations_per_state"], 4)
            self.assertFalse(statement["phomt_used"])
            self.assertFalse(statement["human_validated"])
            self.assertEqual(statement["draft_sha256"], dataset_fingerprint(rows))
            for row in rows:
                flags = _semantic_frame_flags(row.target_text, row.language, frames[row.target_frame_id])
                self.assertTrue(flags and flags["action_fidelity"] and flags["preservation"])

    def test_v415_reuses_balanced_forms_with_fresh_agent_factors(self):
        splits = [FAMILIES_V415[name] for name in ("train", "validation", "test")]
        triples = [tuple(map(int, row[0].removeprefix("compose415_").split("_")))
                   for split in splits for row in split]
        self.assertEqual([len(split) for split in splits], [112, 40, 40])
        self.assertEqual(len(set(triples)), 192)
        self.assertEqual({row[1] for split in splits for row in split},
                         {"Bao Nguyen", "Mai Pham", "Duc Tran"})
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "v4.15"
            statement = author_seed_v4(destination, version="v4.15")
            inventory_value = json.loads((destination / "inventory.draft.json").read_text(encoding="utf-8"))
            inventory = Inventory(tuple(Action(**value) for value in inventory_value["actions"]), {
                language: frozenset(Action(**value) for value in inventory_value["proposed_by_language"][language])
                for language in ("en", "vi")
            })
            rows = read_jsonl(destination / "corpus.draft.jsonl", inventory,
                              languages=("en", "vi"), require_approved=False)
            frames = json.loads((destination / "semantic_frames.draft.json").read_text(encoding="utf-8"))
            from tide_jepa.pilot import _semantic_frame_flags
            self.assertEqual(statement["records"], 15360)
            self.assertEqual(statement["surface_realizations_per_state"], 4)
            self.assertFalse(statement["human_validated"])
            self.assertIn("1792 in training", statement["transition_weighting_note"])
            self.assertIn("640 in validation", statement["transition_weighting_note"])
            self.assertIn("640 in the sealed release holdout", statement["transition_weighting_note"])
            self.assertIn("evaluation records, not training exposure", statement["transition_weighting_note"])
            self.assertTrue(all((lambda flags: flags and flags["action_fidelity"] and flags["preservation"])(
                _semantic_frame_flags(row.target_text, row.language, frames[row.target_frame_id]))
                for row in rows))

    def test_v418_semantic_checker_covers_all_authored_surface_forms(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "v4.18"
            statement = author_seed_v4(destination, version="v4.18")
            inventory_value = json.loads((destination / "inventory.draft.json").read_text(encoding="utf-8"))
            inventory = Inventory(tuple(Action(**value) for value in inventory_value["actions"]), {
                language: frozenset(Action(**value) for value in inventory_value["proposed_by_language"][language])
                for language in ("en", "vi")
            })
            rows = read_jsonl(destination / "corpus.draft.jsonl", inventory,
                              languages=("en", "vi"), require_approved=False)
            frames = json.loads((destination / "semantic_frames.draft.json").read_text(encoding="utf-8"))
            from tide_jepa.pilot import _semantic_frame_flags
            self.assertEqual(statement["version"], "vi-en-ai-v4.18")
            self.assertTrue(all((lambda flags: flags is not None and flags["action_fidelity"]
                                 and flags["preservation"])(
                _semantic_frame_flags(row.target_text, row.language, frames[row.target_frame_id]))
                for row in rows))

    def test_v416_lower_dose_corpus_has_fresh_factors_and_weighting_disclosure(self):
        splits = [FAMILIES_V416[name] for name in ("train", "validation", "test")]
        triples = [tuple(map(int, row[0].removeprefix("compose416_").split("_")))
                   for split in splits for row in split]
        self.assertEqual([len(split) for split in splits], [112, 40, 40])
        self.assertEqual(len(set(triples)), 192)
        self.assertTrue(all(29 <= triple[0] < 32 for triple in triples))
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "v4.16"
            statement = author_seed_v4(destination, version="v4.16")
            self.assertEqual(statement["records"], 15360)
            self.assertEqual(statement["surface_realizations_per_state"], 4)
            self.assertFalse(statement["phomt_used"])
            self.assertFalse(statement["human_validated"])
            self.assertIn("lower latent-objective-dose study", statement["split_policy"])
            self.assertIn("1792 in training", statement["transition_weighting_note"])
            self.assertIn("640 in validation", statement["transition_weighting_note"])
            self.assertIn("640 in the sealed release holdout", statement["transition_weighting_note"])

    def test_v417_transition_balance_weights_both_duplicate_representations(self):
        splits = [FAMILIES_V417[name] for name in ("train", "validation", "test")]
        triples = [tuple(map(int, row[0].removeprefix("compose417_").split("_")))
                   for split in splits for row in split]
        self.assertEqual([len(split) for split in splits], [112, 40, 40])
        self.assertEqual(len(set(triples)), 192)
        self.assertTrue(all(32 <= triple[0] < 35 for triple in triples))
        self.assertFalse(set(triple[0] for triple in triples) & set(range(29, 32)))
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "v4.17"
            statement = author_seed_v4(destination, version="v4.17")
            self.assertEqual(statement["records"], 15360)
            self.assertEqual(statement["surface_realizations_per_state"], 4)
            self.assertIn("unique-transition row-exposure balance study", statement["split_policy"])
            self.assertIn("test paths reverse this order", statement["split_policy"])
            self.assertIn("0.5 weight to each standalone/path-linked", statement["transition_weighting_note"])
            inventory_value = json.loads((destination / "inventory.draft.json").read_text(encoding="utf-8"))
            inventory = Inventory(tuple(Action(**value) for value in inventory_value["actions"]), {
                language: frozenset(Action(**value) for value in inventory_value["proposed_by_language"][language])
                for language in ("en", "vi")
            })
            rows = read_jsonl(destination / "corpus.draft.jsonl", inventory,
                              languages=("en", "vi"), require_approved=False)
            groups = json.loads((destination / "groups.json").read_text(encoding="utf-8"))
            train_rows = [row for row in rows if groups[row.split_group_id] == "train"]
            from tide_jepa.experiment import _transition_record_weights
            representations = {}
            for row in train_rows:
                key = (row.language, row.source_frame_id, row.target_frame_id,
                       row.action.kind, row.action.value)
                representations.setdefault(key, [[], []])[row.path_id is not None].append(row.record_id)
            self.assertTrue(all(len(record_ids) == 4
                                for roles in representations.values() for record_ids in roles if record_ids))
            self.assertTrue(all(len(roles[0]) == len(roles[1])
                                for roles in representations.values() if roles[0] and roles[1]))
            uniform = _transition_record_weights(train_rows, "row_uniform")
            balanced = _transition_record_weights(train_rows, "unique_transition")
            self.assertTrue(all(weight == 1.0 for weight in uniform.values()))
            self.assertEqual(sum(weight == 0.5 for weight in balanced.values()), 3584)
            self.assertEqual(sum(balanced.values()), 7168.0)

    def test_v418_fresh_factorial_corpus_uses_matched_path_order(self):
        splits = [FAMILIES_V418[name] for name in ("train", "validation", "test")]
        triples = [tuple(map(int, row[0].removeprefix("compose418_").split("_")))
                   for split in splits for row in split]
        self.assertEqual([len(split) for split in splits], [112, 40, 40])
        self.assertEqual(len(set(triples)), 192)
        self.assertTrue(all(35 <= triple[0] < 38 for triple in triples))
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "v4.18"
            statement = author_seed_v4(destination, version="v4.18")
            self.assertEqual(statement["records"], 15360)
            self.assertEqual(statement["surface_realizations_per_state"], 4)
            self.assertFalse(statement["human_validated"])
            self.assertIn("same action order", statement["split_policy"])
            self.assertEqual(set(statement["registered_hypotheses"]), {
                "source_copy_supervision", "tide_auxiliary", "primary_quality_gate", "interpretation"})
            inventory_value = json.loads((destination / "inventory.draft.json").read_text(encoding="utf-8"))
            inventory = Inventory(tuple(Action(**value) for value in inventory_value["actions"]), {
                language: frozenset(Action(**value) for value in inventory_value["proposed_by_language"][language])
                for language in ("en", "vi")
            })
            rows = read_jsonl(destination / "corpus.draft.jsonl", inventory,
                              languages=("en", "vi"), require_approved=False)
            groups = json.loads((destination / "groups.json").read_text(encoding="utf-8"))
            path_sequences = {}
            for row in rows:
                if row.path_id:
                    path_sequences.setdefault(groups[row.split_group_id], {})[row.path_step] = (
                        row.action.kind, row.action.value)
            signatures = {split: tuple(sequence[index] for index in sorted(sequence))
                          for split, sequence in path_sequences.items()}
            self.assertEqual(len(signatures), 3)
            self.assertEqual(len(set(signatures.values())), 1)

    def test_v419_fresh_corpus_supports_checker_and_pairwise_holdout(self):
        splits = [FAMILIES_V419[name] for name in ("train", "validation", "test")]
        triples = [tuple(map(int, row[0].removeprefix("compose419_").split("_")))
                   for split in splits for row in split]
        self.assertEqual([len(split) for split in splits], [112, 40, 40])
        self.assertEqual(len(set(triples)), 192)
        self.assertTrue(all(38 <= triple[0] < 41 for triple in triples))
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "v4.19"
            statement = author_seed_v4(destination, version="v4.19")
            self.assertEqual(statement["records"], 15360)
            self.assertEqual(statement["surface_realizations_per_state"], 4)
            self.assertFalse(statement["phomt_used"])
            self.assertFalse(statement["human_validated"])
            self.assertIn("matched loss computation", statement["split_policy"])
            self.assertIn("fixed-final-epoch", statement["split_policy"])
            self.assertIn("matched_compute", statement["registered_hypotheses"])
            inventory_value = json.loads((destination / "inventory.draft.json").read_text(encoding="utf-8"))
            inventory = Inventory(tuple(Action(**value) for value in inventory_value["actions"]), {
                language: frozenset(Action(**value) for value in inventory_value["proposed_by_language"][language])
                for language in ("en", "vi")
            })
            rows = read_jsonl(destination / "corpus.draft.jsonl", inventory,
                              languages=("en", "vi"), require_approved=False)
            frames = json.loads((destination / "semantic_frames.draft.json").read_text(encoding="utf-8"))
            from tide_jepa.pilot import _semantic_frame_flags
            self.assertTrue(all((lambda flags: flags is not None and flags["action_fidelity"]
                                 and flags["preservation"])(
                _semantic_frame_flags(row.target_text, row.language, frames[row.target_frame_id]))
                for row in rows))

    def test_v420_fresh_corpus_supports_checker_and_pairwise_holdout(self):
        splits = [FAMILIES_V420[name] for name in ("train", "validation", "test")]
        triples = [tuple(map(int, row[0].removeprefix("compose420_").split("_")))
                   for split in splits for row in split]
        self.assertEqual([len(split) for split in splits], [112, 40, 40])
        self.assertEqual(len(set(triples)), 192)
        self.assertTrue(all(41 <= triple[0] < 44 for triple in triples))
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "v4.20"
            statement = author_seed_v4(destination, version="v4.20")
            self.assertEqual(statement["records"], 15360)
            self.assertEqual(statement["surface_realizations_per_state"], 4)
            self.assertFalse(statement["phomt_used"])
            self.assertFalse(statement["human_validated"])
            self.assertIn("source-pointer decoder comparison", statement["split_policy"])
            self.assertIn("source_pointer_decoder", statement["registered_hypotheses"])
            inventory_value = json.loads((destination / "inventory.draft.json").read_text(encoding="utf-8"))
            inventory = Inventory(tuple(Action(**value) for value in inventory_value["actions"]), {
                language: frozenset(Action(**value) for value in inventory_value["proposed_by_language"][language])
                for language in ("en", "vi")
            })
            rows = read_jsonl(destination / "corpus.draft.jsonl", inventory,
                              languages=("en", "vi"), require_approved=False)
            frames = json.loads((destination / "semantic_frames.draft.json").read_text(encoding="utf-8"))
            from tide_jepa.pilot import _semantic_frame_flags
            self.assertTrue(all((lambda flags: flags is not None and flags["action_fidelity"]
                                 and flags["preservation"])(
                _semantic_frame_flags(row.target_text, row.language, frames[row.target_frame_id]))
                for row in rows))

    def test_v421_registers_fresh_split_and_copy_decoder_factorial(self):
        splits = [FAMILIES_V421[name] for name in ("train", "validation", "test")]
        triples = [tuple(map(int, row[0].removeprefix("compose421_").split("_")))
                   for split in splits for row in split]
        self.assertEqual([len(split) for split in splits], [112, 40, 40])
        self.assertEqual(len(set(triples)), 192)
        self.assertTrue(all(44 <= triple[0] < 47 for triple in triples))
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "v4.21"
            statement = author_seed_v4(destination, version="v4.21")
            self.assertEqual(statement["records"], 15360)
            self.assertEqual(statement["surface_realizations_per_state"], 4)
            self.assertFalse(statement["phomt_used"])
            self.assertFalse(statement["human_validated"])
            self.assertIn("2x2", statement["split_policy"])
            self.assertIn("copy_decoder_interaction", statement["registered_hypotheses"])
            inventory_value = json.loads((destination / "inventory.draft.json").read_text(encoding="utf-8"))
            inventory = Inventory(tuple(Action(**value) for value in inventory_value["actions"]), {
                language: frozenset(Action(**value) for value in inventory_value["proposed_by_language"][language])
                for language in ("en", "vi")})
            rows = read_jsonl(destination / "corpus.draft.jsonl", inventory,
                              languages=("en", "vi"), require_approved=False)
            frames = json.loads((destination / "semantic_frames.draft.json").read_text(encoding="utf-8"))
            from tide_jepa.pilot import _semantic_frame_flags
            self.assertTrue(all(_semantic_frame_flags(row.target_text, row.language,
                                                       frames[row.target_frame_id]) is not None
                                for row in rows))

            from tide_jepa.pilot import REVIEWED_ARTIFACTS, freeze_pilot
            artifact_hashes = {name: hashlib.sha256((destination / name).read_bytes()).hexdigest()
                               for name in REVIEWED_ARTIFACTS}
            for suffix in ("a", "b"):
                review = {"schema_version": "tide-jepa-ai-pilot-review-v1",
                          "reviewer_id": f"fixture-luna-{suffix}", "reviewer_type": "AI",
                          "decision": "approve", "draft_sha256": statement["draft_sha256"],
                          "rows_checked": 15360, "artifact_sha256": artifact_hashes,
                          "human_validated": False}
                (destination / f"review-{suffix}.json").write_text(json.dumps(review), encoding="utf-8")
            (destination / "adjudication.json").write_text(json.dumps({
                "decision": "approve", "draft_sha256": statement["draft_sha256"],
                "human_validated": False}), encoding="utf-8")
            freeze_pilot(destination, epochs=1, seeds=(17,), model_width=8, model_heads=2,
                         condition_modes=("tide",), condition_source_copy_weights=(0.0, 1.5),
                         condition_source_pointer_decoder_modes=("vocabulary", "source_pointer"),
                         checkpoint_selection_policy="fixed_final_epoch", compute_source_copy_term=True)
            protocol = json.loads((destination / "protocol.json").read_text(encoding="utf-8"))
            self.assertEqual(len(protocol["configs"]), 4)
            self.assertEqual(protocol["primary_source_copy_weights"], [0.0, 1.5])
            self.assertEqual(protocol["primary_source_pointer_decoder_modes"], ["vocabulary", "source_pointer"])
            self.assertTrue(all(name in protocol["registered_hypotheses"]
                                for name in ("copy_decoder_interaction", "primary_quality_gate")))

    def test_v422_fresh_corpus_checker_knows_authored_version(self):
        splits = [FAMILIES_V422[name] for name in ("train", "validation", "test")]
        triples = [tuple(map(int, row[0].removeprefix("compose422_").split("_")))
                   for split in splits for row in split]
        self.assertEqual([len(split) for split in splits], [112, 40, 40])
        self.assertEqual(len(set(triples)), 192)
        self.assertTrue(all(47 <= triple[0] < 50 for triple in triples))
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "v4.22"
            statement = author_seed_v4(destination, version="v4.22")
            self.assertEqual(statement["records"], 15360)
            self.assertEqual(statement["surface_realizations_per_state"], 4)
            self.assertFalse(statement["phomt_used"])
            self.assertFalse(statement["human_validated"])
            self.assertIn("copy-loss", statement["split_policy"])
            inventory_value = json.loads((destination / "inventory.draft.json").read_text(encoding="utf-8"))
            inventory = Inventory(tuple(Action(**value) for value in inventory_value["actions"]), {
                language: frozenset(Action(**value) for value in inventory_value["proposed_by_language"][language])
                for language in ("en", "vi")})
            rows = read_jsonl(destination / "corpus.draft.jsonl", inventory,
                              languages=("en", "vi"), require_approved=False)
            frames = json.loads((destination / "semantic_frames.draft.json").read_text(encoding="utf-8"))
            from tide_jepa.pilot import _semantic_frame_flags
            self.assertTrue(all(_semantic_frame_flags(row.target_text, row.language,
                                                       frames[row.target_frame_id]) is not None
                                for row in rows))

    def test_v423_balances_factors_and_aligns_progressive_translation(self):
        from collections import Counter
        splits = [FAMILIES_V423[name] for name in ("train", "validation", "test")]
        triples = [tuple(map(int, row[0].removeprefix("compose423_").split("_")))
                   for split in splits for row in split]
        self.assertEqual([len(split) for split in splits], [112, 40, 40])
        self.assertEqual(len(set(triples)), 192)
        self.assertTrue(any(row[0].startswith("compose423_") and row[2] == "search for"
                            and row[7] == "tìm kiếm"
                            for split in splits for row in split))
        for split in splits:
            rows = [tuple(map(int, row[0].removeprefix("compose423_").split("_"))) for row in split]
            self.assertEqual(set(row[0] for row in rows), {50, 51, 52})
            for dimension in range(3):
                counts = Counter(row[dimension] for row in rows)
                self.assertLessEqual(max(counts.values()) - min(counts.values()), 1)
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "v4.23"
            statement = author_seed_v4(destination, version="v4.23")
            self.assertEqual(statement["records"], 15360)
            self.assertIn("Vietnamese đang", statement["split_policy"])
            self.assertIn("path-enriched", statement["transition_weighting_note"])
            inventory_value = json.loads((destination / "inventory.draft.json").read_text(encoding="utf-8"))
            inventory = Inventory(tuple(Action(**value) for value in inventory_value["actions"]), {
                language: frozenset(Action(**value) for value in inventory_value["proposed_by_language"][language])
                for language in ("en", "vi")})
            rows = read_jsonl(destination / "corpus.draft.jsonl", inventory,
                              languages=("en", "vi"), require_approved=False)
            frames = json.loads((destination / "semantic_frames.draft.json").read_text(encoding="utf-8"))
            from tide_jepa.pilot import _semantic_frame_flags
            self.assertTrue(all((lambda flags: flags is not None and flags["action_fidelity"]
                                 and flags["preservation"])(
                _semantic_frame_flags(row.target_text, row.language, frames[row.target_frame_id]))
                for row in rows))

    def test_v424_uses_fresh_balanced_factor_pool_and_supported_checker(self):
        from collections import Counter
        splits = [FAMILIES_V424[name] for name in ("train", "validation", "test")]
        triples = [tuple(map(int, row[0].removeprefix("compose424_").split("_")))
                   for split in splits for row in split]
        self.assertEqual([len(split) for split in splits], [112, 40, 40])
        self.assertEqual(len(set(triples)), 192)
        train = [tuple(map(int, row[0].removeprefix("compose424_").split("_")))
                 for row in splits[0]]
        known_pairs = {(i, j, row[i], row[j])
                       for row in train for i, j in ((0, 1), (0, 2), (1, 2))}
        for split in splits[1:]:
            for row in (tuple(map(int, item[0].removeprefix("compose424_").split("_")))
                        for item in split):
                self.assertTrue(all((i, j, row[i], row[j]) in known_pairs
                                    for i, j in ((0, 1), (0, 2), (1, 2))))
            rows = [tuple(map(int, item[0].removeprefix("compose424_").split("_")))
                    for item in split]
            for dimension in range(3):
                counts = Counter(row[dimension] for row in rows)
                self.assertLessEqual(max(counts.values()) - min(counts.values()), 1)
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "v4.24"
            statement = author_seed_v4(destination, version="v4.24")
            self.assertEqual(statement["records"], 15360)
            self.assertIn("64-width/two-layer", statement["split_policy"])
            self.assertFalse(statement["phomt_used"])
            self.assertFalse(statement["human_validated"])
            inventory_value = json.loads((destination / "inventory.draft.json").read_text(encoding="utf-8"))
            inventory = Inventory(tuple(Action(**value) for value in inventory_value["actions"]), {
                language: frozenset(Action(**value) for value in inventory_value["proposed_by_language"][language])
                for language in ("en", "vi")})
            rows = read_jsonl(destination / "corpus.draft.jsonl", inventory,
                              languages=("en", "vi"), require_approved=False)
            frames = json.loads((destination / "semantic_frames.draft.json").read_text(encoding="utf-8"))
            from tide_jepa.pilot import _semantic_frame_flags
            self.assertTrue(all((lambda flags: flags is not None and flags["action_fidelity"]
                                 and flags["preservation"])(
                _semantic_frame_flags(row.target_text, row.language, frames[row.target_frame_id]))
                for row in rows))
            now_negative_vi = [row for row in rows if row.language == "vi"
                               and frames[row.target_frame_id]["time"] == "present"
                               and frames[row.target_frame_id]["polarity"] == "negative"]
            self.assertTrue(now_negative_vi)
            self.assertTrue(all("đang không" in " ".join(row.target_text.split())
                                and _semantic_frame_flags(row.target_text, row.language,
                                                          frames[row.target_frame_id])["action_fidelity"]
                                for row in now_negative_vi))

    def test_v425_self_feeding_corpus_is_fresh_pairwise_covered_and_checkable(self):
        from collections import Counter
        splits = [FAMILIES_V425[name] for name in ("train", "validation", "test")]
        triples = [tuple(map(int, row[0].removeprefix("compose425_").split("_")))
                   for split in splits for row in split]
        self.assertEqual([len(split) for split in splits], [112, 40, 40])
        self.assertEqual(len(set(triples)), 192)
        self.assertEqual({row[1] for split in splits for row in split},
                         {"Bich Ngoc", "Phan Minh", "Thu Trang"})
        train_pairs = {(i, j, row[i], row[j]) for row in triples[:112]
                       for i, j in ((0, 1), (0, 2), (1, 2))}
        for heldout in triples[112:]:
            self.assertTrue(all((i, j, heldout[i], heldout[j]) in train_pairs
                                for i, j in ((0, 1), (0, 2), (1, 2))))
        for split in splits:
            for dimension in range(3):
                counts = Counter(row[dimension] for row in
                                 (tuple(map(int, item[0].removeprefix("compose425_").split("_")))
                                  for item in split))
                self.assertLessEqual(max(counts.values()) - min(counts.values()), 1)
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "v4.25"
            statement = author_seed_v4(destination, version="v4.25")
            self.assertEqual(statement["records"], 15360)
            self.assertIn("one-pass 0.2 self-feeding", statement["split_policy"])
            self.assertIn("no matched-compute claim", statement["split_policy"])
            inventory_value = json.loads((destination / "inventory.draft.json").read_text(encoding="utf-8"))
            inventory = Inventory(tuple(Action(**value) for value in inventory_value["actions"]), {
                language: frozenset(Action(**value) for value in inventory_value["proposed_by_language"][language])
                for language in ("en", "vi")})
            rows = read_jsonl(destination / "corpus.draft.jsonl", inventory,
                              languages=("en", "vi"), require_approved=False)
            frames = json.loads((destination / "semantic_frames.draft.json").read_text(encoding="utf-8"))
            from tide_jepa.pilot import _semantic_frame_flags
            self.assertTrue(all((lambda flags: flags is not None and flags["action_fidelity"]
                                 and flags["preservation"])(
                _semantic_frame_flags(row.target_text, row.language, frames[row.target_frame_id]))
                for row in rows))
            now_negative_vi = [row for row in rows if row.language == "vi"
                               and frames[row.target_frame_id]["time"] == "present"
                               and frames[row.target_frame_id]["polarity"] == "negative"]
            self.assertTrue(all("đang không" in " ".join(row.target_text.split())
                                for row in now_negative_vi))

    def test_unique_transition_weighting_rejects_unequal_representation_counts(self):
        from types import SimpleNamespace
        from tide_jepa.experiment import _transition_record_weights
        action = SimpleNamespace(kind="tense", value="past")
        records = [SimpleNamespace(record_id=f"single-{index}", language="en",
                                   source_frame_id="source", target_frame_id="target",
                                   action=action, path_id=None) for index in range(2)]
        records.append(SimpleNamespace(record_id="path", language="en", source_frame_id="source",
                                       target_frame_id="target", action=action, path_id="path-1"))
        with self.assertRaisesRegex(ValueError, "matched standalone/path"):
            _transition_record_weights(records, "unique_transition")

    def test_v42_seed_has_unique_alignments_and_frozen_group_counts(self):
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "v4.2"
            statement = author_seed_v4(destination, version="v4.2")
            inventory_value = json.loads((destination / "inventory.draft.json").read_text(encoding="utf-8"))
            actions = tuple(Action(**value) for value in inventory_value["actions"])
            inventory = Inventory(actions, {
                language: frozenset(Action(**value) for value in inventory_value["proposed_by_language"][language])
                for language in ("en", "vi")
            })
            rows = read_jsonl(destination / "corpus.draft.jsonl", inventory,
                              languages=("en", "vi"), require_approved=False)
            alignments = json.loads((destination / "alignments.draft.json").read_text(encoding="utf-8"))
            edge_signatures = [tuple(sorted(pair.items())) for pair in alignments["edge_pairs"]]
            path_signatures = [tuple(sorted(pair.items())) for pair in alignments["path_pairs"]]
            groups = json.loads((destination / "groups.json").read_text(encoding="utf-8"))
            self.assertEqual(len(rows), 1280)
            self.assertEqual(statement["draft_sha256"], dataset_fingerprint(rows))
            self.assertEqual(len(edge_signatures), len(set(edge_signatures)))
            self.assertEqual(len(edge_signatures), 640)
            self.assertEqual(len(path_signatures), len(set(path_signatures)))
            self.assertEqual(len(path_signatures), 64)
            self.assertEqual({name: list(groups.values()).count(name)
                              for name in ("train", "validation", "test")},
                             {"train": 20, "validation": 6, "test": 6})
            self.assertFalse(statement["human_validated"])


class DemoAPITests(unittest.TestCase):
    @unittest.skipUnless(TORCH_AVAILABLE, "PyTorch is required for offline inference")
    def test_inference_default_budget_fits_small_checkpoint(self):
        from types import SimpleNamespace
        import torch
        from tide_jepa.data import UTF8ByteTokenizer
        from tide_jepa.infer import OfflineGenerator
        generator = OfflineGenerator.__new__(OfflineGenerator)
        generator.cfg = SimpleNamespace(languages=("en", "vi"), max_length=12)
        generator.device = "cpu"
        generator.tokenizer = UTF8ByteTokenizer()
        generator.inventory = SimpleNamespace(require=lambda *_: 0)
        budgets = []
        def generate(*args):
            budgets.append(args[-1])
            return torch.tensor([[1, 2]])
        generator.model = SimpleNamespace(generate=generate)
        request = {"source": "Test", "source_language": "en", "target_language": "en",
                   "actions": [{"kind": "TIME", "value": "PAST"}]}
        self.assertTrue(generator.generate(request)["valid_utf8"])
        self.assertEqual(budgets, [11])
        with self.assertRaisesRegex(ValueError, "through 11"):
            generator.generate({**request, "max_new_tokens": 12})

    def test_demo_recovers_inference_slot_after_model_error(self):
        from http.server import ThreadingHTTPServer
        from threading import Thread
        from types import SimpleNamespace
        from urllib.error import HTTPError
        from urllib.request import Request, urlopen
        from tide_jepa.demo import make_handler
        class FailingOnce:
            cfg = SimpleNamespace(languages=("en", "vi"))
            calls = 0
            def generate(self, _value):
                self.calls += 1
                if self.calls == 1:
                    raise RuntimeError("internal model details must stay private")
                return {"generated_text": "synthetic", "valid_utf8": True}
        server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(FailingOnce(), {}))
        worker = Thread(target=server.serve_forever, daemon=True)
        worker.start()
        url = f"http://127.0.0.1:{server.server_port}/generate"
        body = json.dumps({"source_language": "en", "target_language": "en",
                           "actions": [{"kind": "TIME", "value": "PAST"}]}).encode()
        def request():
            return Request(url, data=body, headers={"Content-Type": "application/json"})
        try:
            with self.assertRaises(HTTPError) as raised:
                urlopen(request(), timeout=2)
            self.assertEqual(raised.exception.code, 500)
            self.assertNotIn("internal model", raised.exception.read().decode())
            with urlopen(request(), timeout=2) as response:
                self.assertEqual(response.status, 200)
        finally:
            server.shutdown()
            server.server_close()
            worker.join(timeout=2)

    @unittest.skipUnless(TORCH_AVAILABLE, "PyTorch is required for offline inference")
    def test_inference_rejects_malformed_actions_before_model_work(self):
        from types import SimpleNamespace
        from tide_jepa.infer import OfflineGenerator

        generator = OfflineGenerator.__new__(OfflineGenerator)
        generator.cfg = SimpleNamespace(languages=("en", "vi"))
        generator.inventory = SimpleNamespace(
            require=lambda *_: self.fail("malformed action reached inventory lookup"))
        request = {"source": "Original synthetic source.", "source_language": "en",
                   "target_language": "en"}
        for actions in (None, 4, True, "TIME:PAST", {}, []):
            with self.subTest(actions_type=type(actions).__name__):
                with self.assertRaisesRegex(ValueError, "actions must be a nonempty list"):
                    generator.generate({**request, "actions": actions})
        with self.assertRaisesRegex(ValueError, "at most 8"):
            generator.generate({**request, "actions": [{}] * 9})
        for action in ({"kind": "TIME"}, {"kind": 4, "value": "PAST"},
                       {"kind": "TIME", "value": None}):
            with self.subTest(action=action):
                with self.assertRaises(ValueError):
                    generator.generate({**request, "actions": [action]})
        self.assertFalse(hasattr(generator, "model"))
        self.assertFalse(hasattr(generator, "tokenizer"))

    def test_local_demo_reports_actual_model_and_rejects_invalid_requests(self):
        from http.server import HTTPServer
        from threading import Thread
        from types import SimpleNamespace
        from urllib.error import HTTPError
        from urllib.request import Request, urlopen
        from tide_jepa.demo import make_handler

        class FakeGenerator:
            cfg = SimpleNamespace(languages=("en", "vi"))
            def generate(self, value):
                if value.get("target_language") not in self.cfg.languages:
                    raise ValueError("language not approved")
                return {"generated_text": "Original synthetic output.", "valid_utf8": True}
        server = HTTPServer(("127.0.0.1", 0), make_handler(FakeGenerator(), {"mode": "generic_jepa", "seed": 41, "pilot_version": "vi-en-ai-test", "primary_quality_mode": "tide", "validation_gate_status": "control_only", "human_validated": False, "phomt_trained": False}))
        worker = Thread(target=server.serve_forever, daemon=True)
        worker.start()
        url = f"http://127.0.0.1:{server.server_port}"
        try:
            with urlopen(url + "/health") as response:
                metadata = json.load(response)
            self.assertEqual((metadata["mode"], metadata["seed"]), ("generic_jepa", 41))
            self.assertEqual(metadata["quality_status"], "diagnostic_only")
            self.assertEqual(metadata["validation_gate_status"], "control_only")
            valid = Request(url + "/generate", data=json.dumps({"source_language": "en", "target_language": "en", "actions": [{"kind": "TIME", "value": "PAST"}]}).encode(), headers={"Content-Type": "application/json"})
            with urlopen(valid) as response:
                self.assertTrue(json.load(response)["valid_utf8"])
            invalid = Request(url + "/generate", data=b"not-json", headers={"Content-Type": "application/json"})
            with self.assertRaises(HTTPError) as error:
                urlopen(invalid)
            self.assertEqual(error.exception.code, 400)
            oversized_path = Request(url + "/generate", data=json.dumps({"source_language": "en", "target_language": "en", "actions": [{"kind": "TIME", "value": "PAST"}] * 9}).encode(), headers={"Content-Type": "application/json"})
            with self.assertRaises(HTTPError) as error:
                urlopen(oversized_path)
            self.assertEqual(error.exception.code, 400)
            with self.assertRaises(HTTPError) as error:
                urlopen(url + "/../../README.md")
            self.assertEqual(error.exception.code, 404)
        finally:
            server.shutdown()
            server.server_close()
            worker.join(timeout=2)

    def test_local_demo_limits_generation_to_one_concurrent_request(self):
        from http.server import ThreadingHTTPServer
        from threading import Event, Thread
        from types import SimpleNamespace
        from urllib.error import HTTPError
        from urllib.request import Request, urlopen
        from tide_jepa.demo import make_handler

        started, release = Event(), Event()

        class SlowGenerator:
            cfg = SimpleNamespace(languages=("en", "vi"))

            def generate(self, _value):
                started.set()
                if not release.wait(timeout=5):
                    raise TimeoutError("synthetic test generator timed out")
                return {"generated_text": "synthetic", "valid_utf8": True}

        server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(SlowGenerator(), {}))
        worker = Thread(target=server.serve_forever, daemon=True)
        worker.start()
        url = f"http://127.0.0.1:{server.server_port}/generate"
        body = json.dumps({"source": "synthetic", "source_language": "en",
                           "target_language": "en", "actions": [{"kind": "TIME", "value": "PAST"}]}).encode()
        first_result = []

        def send_first():
            try:
                with urlopen(Request(url, data=body, headers={"Content-Type": "application/json"}), timeout=3) as response:
                    first_result.append((response.status, json.load(response)))
            except Exception as error:  # surfaced as an assertion below
                first_result.append(error)

        first = Thread(target=send_first, daemon=True)
        first.start()
        try:
            self.assertTrue(started.wait(timeout=2))
            with self.assertRaises(HTTPError) as error:
                urlopen(Request(url, data=body, headers={"Content-Type": "application/json"}), timeout=2)
            self.assertEqual(error.exception.code, 503)
        finally:
            release.set()
            first.join(timeout=3)
            server.shutdown()
            server.server_close()
            worker.join(timeout=2)
        self.assertEqual(len(first_result), 1)
        self.assertFalse(isinstance(first_result[0], Exception), repr(first_result[0]))
        self.assertEqual(first_result[0][0], 200)


@unittest.skipUnless(TORCH_AVAILABLE, "PyTorch is required for pilot freeze and integration")
class PilotWorkflowTests(unittest.TestCase):
    def setUp(self):
        import torch
        torch.set_num_threads(1)
        self.temporary = tempfile.TemporaryDirectory()
        self.base = Path(self.temporary.name) / "original-synthetic"
        self.statement = author_seed(self.base)

    def tearDown(self):
        self.temporary.cleanup()

    def write_reviews(self):
        from tide_jepa.pilot import REVIEWED_ARTIFACTS
        hashes = {name: hashlib.sha256((self.base / name).read_bytes()).hexdigest() for name in REVIEWED_ARTIFACTS}
        for name in ("a", "b"):
            value = {"reviewer_id": f"synthetic-test-reviewer-{name}", "reviewer_type": "AI", "decision": "approve",
                     "draft_sha256": self.statement["draft_sha256"], "rows_checked": 400, "artifact_sha256": hashes}
            (self.base / f"review-{name}.json").write_text(json.dumps(value), encoding="utf-8")
        (self.base / "adjudication.json").write_text(json.dumps({"decision": "approve", "draft_sha256": self.statement["draft_sha256"], "human_validated": False}), encoding="utf-8")

    def freeze(self):
        from tide_jepa.pilot import freeze_pilot
        self.write_reviews()
        return freeze_pilot(self.base, epochs=1, seeds=(17,))

    def test_one_pass_self_feeding_replaces_only_sampled_active_decoder_slots(self):
        import torch
        from unittest.mock import patch
        from tide_jepa.training import Objective, _scheduled_sampling_inputs
        decoder_input = torch.tensor([[1, 4, 5, 0]])
        proposal_logits = torch.zeros((1, 4, 8))
        proposal_logits[0, 0, 6] = 1
        proposal_logits[0, 1, 7] = 1
        with patch("tide_jepa.training.torch.rand", return_value=torch.zeros((1, 3))):
            mixed = _scheduled_sampling_inputs(decoder_input, proposal_logits, pad_id=0, rate=0.2)
        self.assertEqual(mixed.tolist(), [[1, 6, 7, 0]])
        self.assertEqual(decoder_input.tolist(), [[1, 4, 5, 0]])
        for invalid in (-0.01, 1.0, float("nan"), True, "0.2"):
            with self.assertRaises((TypeError, ValueError)):
                Objective(scheduled_sampling_rate=invalid)

    def test_v425_freeze_registers_the_scheduled_sampling_factorial(self):
        from tide_jepa.pilot import REVIEWED_ARTIFACTS, _semantic_frame_flags, freeze_pilot
        self.base = Path(self.temporary.name) / "v4.25"
        self.statement = author_seed_v4(self.base, version="v4.25")
        hashes = {name: hashlib.sha256((self.base / name).read_bytes()).hexdigest()
                  for name in REVIEWED_ARTIFACTS}
        for name in ("a", "b"):
            (self.base / f"review-{name}.json").write_text(json.dumps({
                "reviewer_id": f"synthetic-test-reviewer-{name}", "reviewer_type": "AI",
                "decision": "approve", "draft_sha256": self.statement["draft_sha256"],
                "rows_checked": self.statement["records"], "artifact_sha256": hashes,
            }), encoding="utf-8")
        (self.base / "adjudication.json").write_text(json.dumps({
            "decision": "approve", "draft_sha256": self.statement["draft_sha256"],
            "human_validated": False,
        }), encoding="utf-8")
        freeze_pilot(self.base, epochs=1, seeds=(17, 23, 41), model_width=64,
                     model_heads=4, model_layers=2, condition_modes=("tide",),
                     condition_scheduled_sampling_rates=(0.0, 0.2),
                     checkpoint_selection_policy="fixed_final_epoch")
        protocol = json.loads((self.base / "protocol.json").read_text())
        configs = [json.loads((self.base / name).read_text()) for name in protocol["configs"]]
        self.assertEqual(len(configs), 6)
        self.assertEqual(protocol["primary_scheduled_sampling_rates"], [0.0, 0.2])
        self.assertEqual({config["objective"]["scheduled_sampling_rate"] for config in configs},
                         {0.0, 0.2})

    def test_v426_low_dose_copy_corpus_and_factorial_are_fresh_and_bound(self):
        from collections import Counter
        from tide_jepa.pilot_seed import FAMILIES_V426
        from tide_jepa.pilot import REVIEWED_ARTIFACTS, freeze_pilot

        splits = [FAMILIES_V426[name] for name in ("train", "validation", "test")]
        triples = [tuple(map(int, row[0].removeprefix("compose426_").split("_")))
                   for split in splits for row in split]
        self.assertEqual([len(split) for split in splits], [112, 40, 40])
        self.assertEqual(len(set(triples)), 192)
        self.assertEqual({row[1] for split in splits for row in split},
                         {"Bao Chau", "Duc Anh", "Gia Han"})
        train_pairs = {(i, j, row[i], row[j]) for row in triples[:112]
                       for i, j in ((0, 1), (0, 2), (1, 2))}
        self.assertTrue(all(all((i, j, heldout[i], heldout[j]) in train_pairs
                                for i, j in ((0, 1), (0, 2), (1, 2)))
                            for heldout in triples[112:]))
        for split in splits:
            for dimension in range(3):
                counts = Counter(row[dimension] for row in
                                 (tuple(map(int, item[0].removeprefix("compose426_").split("_")))
                                  for item in split))
                self.assertLessEqual(max(counts.values()) - min(counts.values()), 2)

        self.base = Path(self.temporary.name) / "v4.26"
        self.statement = author_seed_v4(self.base, version="v4.26")
        self.assertEqual(self.statement["records"], 15360)
        self.assertIn("low-dose source-copy supervision (0/0.25)", self.statement["split_policy"])
        inventory_value = json.loads((self.base / "inventory.draft.json").read_text(encoding="utf-8"))
        inventory = Inventory(tuple(Action(**value) for value in inventory_value["actions"]), {
            language: frozenset(Action(**value) for value in inventory_value["proposed_by_language"][language])
            for language in ("en", "vi")})
        rows = read_jsonl(self.base / "corpus.draft.jsonl", inventory,
                          languages=("en", "vi"), require_approved=False)
        frames = json.loads((self.base / "semantic_frames.draft.json").read_text(encoding="utf-8"))
        from tide_jepa.pilot import _semantic_frame_flags
        for row in rows:
            flags = _semantic_frame_flags(row.target_text, row.language, frames[row.target_frame_id])
            self.assertIsNotNone(flags)
            self.assertTrue(flags["action_fidelity"] and flags["preservation"])
        hashes = {name: hashlib.sha256((self.base / name).read_bytes()).hexdigest()
                  for name in REVIEWED_ARTIFACTS}
        for name in ("a", "b"):
            (self.base / f"review-{name}.json").write_text(json.dumps({
                "reviewer_id": f"synthetic-test-reviewer-{name}", "reviewer_type": "AI",
                "decision": "approve", "draft_sha256": self.statement["draft_sha256"],
                "rows_checked": self.statement["records"], "artifact_sha256": hashes,
            }), encoding="utf-8")
        (self.base / "adjudication.json").write_text(json.dumps({
            "decision": "approve", "draft_sha256": self.statement["draft_sha256"],
            "human_validated": False,
        }), encoding="utf-8")
        freeze_pilot(self.base, epochs=1, seeds=(17, 23, 41), model_width=64,
                     model_heads=4, model_layers=2, condition_modes=("tide",),
                     condition_source_copy_weights=(0.0, 0.25), compute_source_copy_term=True,
                     checkpoint_selection_policy="fixed_final_epoch")
        protocol = json.loads((self.base / "protocol.json").read_text())
        configs = [json.loads((self.base / name).read_text()) for name in protocol["configs"]]
        self.assertEqual(len(configs), 6)
        self.assertEqual(protocol["primary_source_copy_weights"], [0.0, 0.25])
        self.assertTrue(all(config["objective"]["compute_source_copy_term"] for config in configs))
        self.assertEqual({config["objective"].get("source_copy_weight", 0.0) for config in configs},
                         {0.0, 0.25})
        from tide_jepa.pilot import _registered_primary_configs
        selected = _registered_primary_configs(protocol, [(name, json.loads((self.base / name).read_text()))
                                                            for name in protocol["configs"]])
        self.assertEqual(len(selected), 6)

    def test_v427_language_balance_corpus_checker_and_factorial(self):
        from tide_jepa.pilot_seed import FAMILIES_V427
        from tide_jepa.pilot import REVIEWED_ARTIFACTS, _registered_primary_configs, _semantic_frame_flags, freeze_pilot

        self.assertEqual([len(FAMILIES_V427[split]) for split in ("train", "validation", "test")],
                         [112, 40, 40])
        agent_ids = {int(row[0].removeprefix("compose427_").split("_")[0])
                     for split in FAMILIES_V427.values() for row in split}
        self.assertEqual(agent_ids, {62, 63, 64})
        self.base = Path(self.temporary.name) / "v4.27"
        self.statement = author_seed_v4(self.base, version="v4.27")
        self.assertEqual(self.statement["records"], 15360)
        self.assertIn("equal-language-balanced token CE", self.statement["split_policy"])
        inventory_value = json.loads((self.base / "inventory.draft.json").read_text(encoding="utf-8"))
        inventory = Inventory(tuple(Action(**value) for value in inventory_value["actions"]), {
            language: frozenset(Action(**value) for value in inventory_value["proposed_by_language"][language])
            for language in ("en", "vi")})
        rows = read_jsonl(self.base / "corpus.draft.jsonl", inventory,
                          languages=("en", "vi"), require_approved=False)
        frames = json.loads((self.base / "semantic_frames.draft.json").read_text(encoding="utf-8"))
        for row in rows:
            flags = _semantic_frame_flags(row.target_text, row.language, frames[row.target_frame_id])
            self.assertIsNotNone(flags)
            self.assertTrue(flags["action_fidelity"] and flags["preservation"])
        hashes = {name: hashlib.sha256((self.base / name).read_bytes()).hexdigest()
                  for name in REVIEWED_ARTIFACTS}
        for name in ("a", "b"):
            (self.base / f"review-{name}.json").write_text(json.dumps({
                "reviewer_id": f"synthetic-test-reviewer-{name}", "reviewer_type": "AI",
                "decision": "approve", "draft_sha256": self.statement["draft_sha256"],
                "rows_checked": self.statement["records"], "artifact_sha256": hashes,
            }), encoding="utf-8")
        (self.base / "adjudication.json").write_text(json.dumps({
            "decision": "approve", "draft_sha256": self.statement["draft_sha256"],
            "human_validated": False,
        }), encoding="utf-8")
        freeze_pilot(self.base, epochs=1, seeds=(17, 23, 41), model_width=64,
                     model_heads=4, model_layers=2, condition_modes=("tide",),
                     condition_source_copy_weights=(0.0,),
                     condition_language_balance_weights=(0.0, 1.0),
                     checkpoint_selection_policy="fixed_final_epoch")
        protocol = json.loads((self.base / "protocol.json").read_text())
        named_configs = [(name, json.loads((self.base / name).read_text()))
                         for name in protocol["configs"]]
        self.assertEqual(len(named_configs), 6)
        self.assertEqual(protocol["primary_language_balance_weights"], [0.0, 1.0])
        self.assertEqual({config["objective"].get("language_balance_weight", 0.0)
                          for _, config in named_configs}, {0.0, 1.0})
        self.assertEqual(len(_registered_primary_configs(protocol, named_configs)), 6)

    def test_v428_freeze_binds_train_validation_only_reviews(self):
        from tide_jepa.pilot_seed import FAMILIES_V428
        from tide_jepa.pilot import REVIEWED_ARTIFACTS, _semantic_frame_flags, freeze_pilot

        self.assertEqual([len(FAMILIES_V428[split]) for split in ("train", "validation", "test")],
                         [112, 40, 40])
        self.assertTrue(all(row[0].startswith("compose428_")
                            for split in FAMILIES_V428.values() for row in split))
        self.assertEqual({int(row[0].removeprefix("compose428_").split("_")[0])
                          for split in FAMILIES_V428.values() for row in split}, {65, 66, 67})
        self.base = Path(self.temporary.name) / "v4.28"
        self.statement = author_seed_v4(self.base, version="v4.28")
        self.assertEqual(self.statement["records"], 15360)
        self.assertEqual(self.statement["review_scope"], "train-validation-only")
        self.assertEqual(self.statement["reviewed_records"], 12160)
        inventory_value = json.loads((self.base / "inventory.draft.json").read_text(encoding="utf-8"))
        inventory = Inventory(tuple(Action(**value) for value in inventory_value["actions"]), {
            language: frozenset(Action(**value) for value in inventory_value["proposed_by_language"][language])
            for language in ("en", "vi")})
        rows = read_jsonl(self.base / "corpus.draft.jsonl", inventory,
                          languages=("en", "vi"), require_approved=False)
        frames = json.loads((self.base / "semantic_frames.draft.json").read_text(encoding="utf-8"))
        groups = json.loads((self.base / "groups.json").read_text(encoding="utf-8"))
        reviewed = [row for row in rows if groups[row.split_group_id] != "test"]
        self.assertEqual(len(reviewed), self.statement["reviewed_records"])
        for row in reviewed:
            flags = _semantic_frame_flags(row.target_text, row.language, frames[row.target_frame_id])
            self.assertIsNotNone(flags)
            self.assertTrue(flags["action_fidelity"] and flags["preservation"])
        hashes = {name: hashlib.sha256((self.base / name).read_bytes()).hexdigest()
                  for name in REVIEWED_ARTIFACTS}
        reviews = {}
        for name in ("a", "b"):
            reviews[name] = {
                "reviewer_id": f"synthetic-test-reviewer-{name}", "reviewer_type": "AI",
                "decision": "approve", "draft_sha256": self.statement["draft_sha256"],
                "rows_checked": self.statement["reviewed_records"], "artifact_sha256": hashes,
            }
            (self.base / f"review-{name}.json").write_text(json.dumps(reviews[name]), encoding="utf-8")
        invalid_scope_review = dict(reviews["a"], rows_checked=self.statement["records"])
        (self.base / "review-a.json").write_text(json.dumps(invalid_scope_review), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "review missing"):
            freeze_pilot(self.base, epochs=1, seeds=(17, 23, 41), model_width=64,
                         model_heads=4, model_layers=2, condition_modes=("tide",),
                         condition_source_copy_weights=(0.0,),
                         condition_language_balance_weights=(0.0, 1.0),
                         checkpoint_selection_policy="fixed_final_epoch")
        (self.base / "review-a.json").write_text(json.dumps(reviews["a"]), encoding="utf-8")
        (self.base / "adjudication.json").write_text(json.dumps({
            "decision": "approve", "draft_sha256": self.statement["draft_sha256"],
            "human_validated": False,
        }), encoding="utf-8")
        freeze_pilot(self.base, epochs=1, seeds=(17, 23, 41), model_width=64,
                     model_heads=4, model_layers=2, condition_modes=("tide",),
                     condition_source_copy_weights=(0.0,),
                     condition_language_balance_weights=(0.0, 1.0),
                     checkpoint_selection_policy="fixed_final_epoch")
        protocol = json.loads((self.base / "protocol.json").read_text())
        self.assertEqual(protocol["review_scope"], "train-validation-only")
        self.assertEqual(protocol["reviewed_records"], 12160)
        self.assertEqual(protocol["primary_language_balance_weights"], [0.0, 1.0])
        self.assertEqual(len(protocol["configs"]), 6)

    def test_v429_generates_scoped_review_bundle_and_freeze_binds_it(self):
        from tide_jepa.pilot_seed import FAMILIES_V429
        from tide_jepa.pilot import REVIEWED_ARTIFACTS, _semantic_frame_flags, freeze_pilot

        self.assertEqual([len(FAMILIES_V429[split]) for split in ("train", "validation", "test")],
                         [112, 40, 40])
        self.assertEqual({int(row[0].removeprefix("compose429_").split("_")[0])
                          for split in FAMILIES_V429.values() for row in split}, {68, 69, 70})
        self.base = Path(self.temporary.name) / "v4.29"
        self.statement = author_seed_v4(self.base, version="v4.29")
        self.assertEqual(self.statement["records"], 15360)
        self.assertEqual(self.statement["reviewed_records"], 12160)
        self.assertEqual(self.statement["action_frame_mapping"]["TIME"],
                         {"NOW": "target frame time is present", "PAST": "target frame time is past"})
        self.assertIn("place marker only", self.statement["context_checker_scope"])
        inventory_value = json.loads((self.base / "inventory.draft.json").read_text(encoding="utf-8"))
        inventory = Inventory(tuple(Action(**value) for value in inventory_value["actions"]), {
            language: frozenset(Action(**value) for value in inventory_value["proposed_by_language"][language])
            for language in ("en", "vi")})
        draft_rows = read_jsonl(self.base / "corpus.draft.jsonl", inventory,
                                languages=("en", "vi"), require_approved=False)
        draft_frames = json.loads((self.base / "semantic_frames.draft.json").read_text(encoding="utf-8"))
        sample = next(row for row in draft_rows if row.language == "en")
        sample_frame = draft_frames[sample.target_frame_id]
        flags = _semantic_frame_flags(sample.target_text, sample.language, sample_frame)
        without_place = ""
        omitted_context = _semantic_frame_flags(without_place, sample.language, sample_frame)
        self.assertTrue(flags["context_preserved"])
        self.assertFalse(omitted_context["context_preserved"])
        self.assertIn("only as the declared language-specific place marker", flags["context_checker_scope"])
        bundle = self.base / "review_bundle"
        manifest = json.loads((bundle / "manifest.json").read_text())
        bundle_statement = json.loads((bundle / "statement.json").read_text())
        self.assertEqual(bundle_statement["action_frame_mapping"], self.statement["action_frame_mapping"])
        self.assertIn("Null path fields are intentional", bundle_statement["standalone_records"])
        self.assertIn("place marker only", bundle_statement["context_checker_scope"])
        self.assertEqual(manifest["review_scope"], "train-validation-only")
        self.assertEqual(manifest["reviewed_records"], 12160)
        scoped_groups = json.loads((bundle / "groups.json").read_text())
        self.assertNotIn("test", scoped_groups.values())
        scoped_rows = [json.loads(line) for line in (bundle / "records.jsonl").read_text().splitlines()]
        self.assertEqual(len(scoped_rows), 12160)
        self.assertTrue(all(row["split_group_id"] in scoped_groups for row in scoped_rows))
        bundle_sha = hashlib.sha256((bundle / "manifest.json").read_bytes()).hexdigest()
        self.assertEqual(self.statement["review_bundle_sha256"], bundle_sha)
        hashes = {name: hashlib.sha256((self.base / name).read_bytes()).hexdigest()
                  for name in REVIEWED_ARTIFACTS}
        for name in ("a", "b"):
            (self.base / f"review-{name}.json").write_text(json.dumps({
                "reviewer_id": f"synthetic-test-reviewer-{name}", "reviewer_type": "AI",
                "decision": "approve", "draft_sha256": self.statement["draft_sha256"],
                "rows_checked": 12160, "artifact_sha256": hashes,
                "review_bundle_sha256": bundle_sha,
            }), encoding="utf-8")
        (self.base / "adjudication.json").write_text(json.dumps({
            "decision": "approve", "draft_sha256": self.statement["draft_sha256"],
            "human_validated": False,
        }), encoding="utf-8")
        freeze_pilot(self.base, epochs=1, seeds=(17, 23, 41), model_width=64,
                     model_heads=4, model_layers=2, condition_modes=("tide",),
                     condition_source_copy_weights=(0.0,),
                     condition_language_balance_weights=(0.0, 1.0),
                     checkpoint_selection_policy="fixed_final_epoch")
        protocol = json.loads((self.base / "protocol.json").read_text())
        self.assertEqual(protocol["review_scope"], "train-validation-only")
        self.assertEqual(protocol["review_bundle_sha256"], bundle_sha)

    def test_v430_generates_fresh_pointer_study_bundle_and_freezes_decoder_factor(self):
        from tide_jepa.pilot import REVIEWED_ARTIFACTS, freeze_pilot
        from tide_jepa.pilot_seed import FAMILIES_V430

        self.assertEqual([len(FAMILIES_V430[split]) for split in ("train", "validation", "test")],
                         [112, 40, 40])
        self.assertEqual({int(row[0].removeprefix("compose430_").split("_")[0])
                          for split in FAMILIES_V430.values() for row in split}, {71, 72, 73})
        self.base = Path(self.temporary.name) / "v4.30"
        self.statement = author_seed_v4(self.base, version="v4.30")
        self.assertEqual(self.statement["reviewed_records"], 12160)
        self.assertIn("source-pointer decoder comparison", self.statement["split_policy"])
        bundle = self.base / "review_bundle"
        bundle_manifest = json.loads((bundle / "manifest.json").read_text())
        self.assertEqual(bundle_manifest["review_scope"], "train-validation-only")
        self.assertNotIn("test", json.loads((bundle / "groups.json").read_text()).values())
        bundle_sha = hashlib.sha256((bundle / "manifest.json").read_bytes()).hexdigest()
        hashes = {name: hashlib.sha256((self.base / name).read_bytes()).hexdigest()
                  for name in REVIEWED_ARTIFACTS}
        for label in ("a", "b"):
            (self.base / f"review-{label}.json").write_text(json.dumps({
                "reviewer_id": f"synthetic-test-reviewer-{label}", "reviewer_type": "AI",
                "decision": "approve", "draft_sha256": self.statement["draft_sha256"],
                "rows_checked": 12160, "artifact_sha256": hashes,
                "review_bundle_sha256": bundle_sha,
            }), encoding="utf-8")
        (self.base / "adjudication.json").write_text(json.dumps({
            "decision": "approve", "draft_sha256": self.statement["draft_sha256"],
            "human_validated": False,
        }), encoding="utf-8")
        freeze_pilot(self.base, epochs=1, seeds=(17, 23, 41), model_width=64,
                     model_heads=4, model_layers=2, condition_modes=("tide",),
                     condition_source_copy_weights=(0.0,),
                     condition_source_pointer_decoder_modes=("vocabulary", "source_pointer"),
                     checkpoint_selection_policy="fixed_final_epoch")
        protocol = json.loads((self.base / "protocol.json").read_text())
        configs = [json.loads((self.base / name).read_text()) for name in protocol["configs"]]
        self.assertEqual(protocol["review_scope"], "train-validation-only")
        self.assertEqual(protocol["review_bundle_sha256"], bundle_sha)
        self.assertEqual(protocol["primary_source_pointer_decoder_modes"], ["vocabulary", "source_pointer"])
        self.assertEqual(len(configs), 6)
        self.assertEqual({config["model"]["source_pointer_decoder"] for config in configs}, {False, True})

    def test_v431_generates_fresh_scoped_bundle_and_freezes_tide_token_only_control(self):
        from tide_jepa.pilot import REVIEWED_ARTIFACTS, freeze_pilot
        from tide_jepa.pilot_seed import FAMILIES_V431

        self.assertEqual([len(FAMILIES_V431[split]) for split in ("train", "validation", "test")],
                         [112, 40, 40])
        self.assertEqual({int(row[0].removeprefix("compose431_").split("_")[0])
                          for split in FAMILIES_V431.values() for row in split}, {74, 75, 76})
        self.base = Path(self.temporary.name) / "v4.31"
        self.statement = author_seed_v4(self.base, version="v4.31")
        self.assertEqual(self.statement["reviewed_records"], 12160)
        self.assertIn("TIDE versus token-only", self.statement["split_policy"])
        self.assertIn("jepa_objective_vs_token_only", self.statement["registered_hypotheses"])
        frames = json.loads((self.base / "semantic_frames.draft.json").read_text())
        self.assertTrue(all("predicate_vi_present" in frame for frame in frames.values()))
        bundle = self.base / "review_bundle"
        bundle_manifest = json.loads((bundle / "manifest.json").read_text())
        self.assertEqual(bundle_manifest["review_scope"], "train-validation-only")
        self.assertNotIn("test", json.loads((bundle / "groups.json").read_text()).values())
        bundle_sha = hashlib.sha256((bundle / "manifest.json").read_bytes()).hexdigest()
        hashes = {name: hashlib.sha256((self.base / name).read_bytes()).hexdigest()
                  for name in REVIEWED_ARTIFACTS}
        for label in ("a", "b"):
            (self.base / f"review-{label}.json").write_text(json.dumps({
                "reviewer_id": f"synthetic-test-reviewer-{label}", "reviewer_type": "AI",
                "decision": "approve", "draft_sha256": self.statement["draft_sha256"],
                "rows_checked": 12160, "artifact_sha256": hashes,
                "review_bundle_sha256": bundle_sha,
            }), encoding="utf-8")
        (self.base / "adjudication.json").write_text(json.dumps({
            "decision": "approve", "draft_sha256": self.statement["draft_sha256"],
            "human_validated": False,
        }), encoding="utf-8")
        freeze_pilot(self.base, epochs=1, seeds=(17, 23, 41), model_width=64,
                     model_heads=4, model_layers=2, primary_mode="tide",
                     condition_modes=("tide", "token_only"),
                     condition_source_copy_weights=(0.0,),
                     checkpoint_selection_policy="fixed_final_epoch")
        protocol = json.loads((self.base / "protocol.json").read_text())
        self.assertEqual(protocol["primary_quality_mode"], "tide")
        self.assertEqual(len(protocol["configs"]), 6)
        self.assertEqual(protocol["review_scope"], "train-validation-only")

    def test_v432_registers_fresh_pointer_primary_and_vocabulary_control(self):
        from tide_jepa.pilot import REVIEWED_ARTIFACTS, freeze_pilot
        from tide_jepa.pilot_seed import FAMILIES_V432

        self.assertEqual([len(FAMILIES_V432[split]) for split in ("train", "validation", "test")],
                         [112, 40, 40])
        self.assertEqual({int(row[0].removeprefix("compose432_").split("_")[0])
                          for split in FAMILIES_V432.values() for row in split}, {77, 78, 79})
        self.base = Path(self.temporary.name) / "v4.32"
        self.statement = author_seed_v4(self.base, version="v4.32")
        self.assertEqual(self.statement["reviewed_records"], 12160)
        self.assertIn("source-pointer", self.statement["split_policy"])
        self.assertIn("source_pointer_preservation", self.statement["registered_hypotheses"])
        self.assertEqual(self.statement["quality_thresholds"]["single_action_preservation_rate"], 0.9)
        self.assertEqual(self.statement["quality_thresholds"]["held_out_path_preservation_rate"], 0.8)
        self.assertIn("do not refer to the sealed release-holdout split",
                      self.statement["quality_gate_scope_note"])
        bundle = self.base / "review_bundle"
        bundle_statement = json.loads((bundle / "statement.json").read_text())
        self.assertEqual(self.statement["reviewed_records_sha256"],
                         bundle_statement["reviewed_records_sha256"])
        bundle_manifest = json.loads((bundle / "manifest.json").read_text())
        bundle_sha = hashlib.sha256((bundle / "manifest.json").read_bytes()).hexdigest()
        hashes = bundle_manifest["files_sha256"]
        for label in ("a", "b"):
            (self.base / f"review-{label}.json").write_text(json.dumps({
                "reviewer_id": f"synthetic-test-reviewer-{label}", "reviewer_type": "AI",
                "decision": "approve", "draft_sha256": self.statement["draft_sha256"],
                "rows_checked": 12160, "artifact_sha256": hashes,
                "review_bundle_sha256": bundle_sha,
            }), encoding="utf-8")
        (self.base / "adjudication.json").write_text(json.dumps({
            "decision": "approve", "draft_sha256": self.statement["draft_sha256"],
            "human_validated": False,
        }), encoding="utf-8")
        freeze_pilot(self.base, epochs=1, seeds=(17, 23, 41), model_width=64,
                     model_heads=4, model_layers=2, primary_mode="tide",
                     condition_modes=("tide",), condition_source_copy_weights=(0.0,),
                     condition_source_pointer_decoder_modes=("vocabulary", "source_pointer"),
                     primary_source_pointer_decoder_modes=("source_pointer",),
                     checkpoint_selection_policy="fixed_final_epoch")
        protocol = json.loads((self.base / "protocol.json").read_text())
        configs = [json.loads((self.base / name).read_text()) for name in protocol["configs"]]
        self.assertEqual(len(configs), 6)
        self.assertEqual(protocol["primary_source_pointer_decoder_modes"], ["source_pointer"])
        self.assertEqual({config["model"]["source_pointer_decoder"] for config in configs}, {False, True})
        self.assertEqual(protocol["review_scope"], "train-validation-only")

    def test_v433_registers_fresh_58_epoch_tide_token_only_confirmation(self):
        from tide_jepa.pilot import _semantic_frame_flags, freeze_pilot
        from tide_jepa.pilot_seed import FAMILIES_V433

        self.assertEqual([len(FAMILIES_V433[split]) for split in ("train", "validation", "test")],
                         [112, 40, 40])
        self.assertEqual({int(row[0].removeprefix("compose433_").split("_")[0])
                          for split in FAMILIES_V433.values() for row in split}, {80, 81, 82})
        self.base = Path(self.temporary.name) / "v4.33"
        self.statement = author_seed_v4(self.base, version="v4.33")
        frames = json.loads((self.base / "semantic_frames.draft.json").read_text())
        sample_frame = next(frame for frame in frames.values()
                            if frame.get("event", "").startswith("compose433_"))
        self.assertIsNotNone(_semantic_frame_flags("", "en", sample_frame))
        self.assertIsNotNone(_semantic_frame_flags("", "vi", sample_frame))
        self.assertEqual(self.statement["reviewed_records"], 12160)
        self.assertIn("58-epoch TIDE versus token-only", self.statement["split_policy"])
        self.assertIn("extended_optimization", self.statement["registered_hypotheses"])
        self.assertIn("tide_vs_token_only", self.statement["registered_hypotheses"])
        self.assertEqual(self.statement["quality_thresholds"]["single_action_preservation_rate"], 0.9)
        bundle = self.base / "review_bundle"
        bundle_manifest = json.loads((bundle / "manifest.json").read_text())
        bundle_sha = hashlib.sha256((bundle / "manifest.json").read_bytes()).hexdigest()
        hashes = bundle_manifest["files_sha256"]
        for label in ("a", "b"):
            (self.base / f"review-{label}.json").write_text(json.dumps({
                "reviewer_id": f"synthetic-test-reviewer-{label}", "reviewer_type": "AI",
                "decision": "approve", "draft_sha256": self.statement["draft_sha256"],
                "rows_checked": self.statement["reviewed_records"], "artifact_sha256": hashes,
                "review_bundle_sha256": bundle_sha,
            }), encoding="utf-8")
        (self.base / "adjudication.json").write_text(json.dumps({
            "decision": "approve", "draft_sha256": self.statement["draft_sha256"],
            "human_validated": False,
        }), encoding="utf-8")
        freeze_pilot(self.base, epochs=58, seeds=(17, 23, 41), model_width=64,
                     model_heads=4, model_layers=2, primary_mode="tide",
                     condition_modes=("tide", "token_only"), condition_source_copy_weights=(0.0,),
                     checkpoint_selection_policy="fixed_final_epoch")
        protocol = json.loads((self.base / "protocol.json").read_text())
        configs = [json.loads((self.base / name).read_text()) for name in protocol["configs"]]
        self.assertEqual(len(configs), 6)
        self.assertEqual(protocol["primary_quality_mode"], "tide")
        self.assertEqual(protocol["review_scope"], "train-validation-only")
        self.assertTrue(all(config["training"]["epochs"] == 58 for config in configs))
        self.assertEqual({config["objective"]["mode"] for config in configs}, {"tide", "token_only"})

    def test_self_feeding_training_smoke_writes_identified_checkpoint(self):
        from tide_jepa.experiment import run_experiment
        self.freeze()
        path = self.base / "tide-seed-17.json"
        config = json.loads(path.read_text())
        config["objective"]["scheduled_sampling_rate"] = 0.2
        config["output_dir"] = str(self.base / "self-feeding-smoke")
        path.write_text(json.dumps(config), encoding="utf-8")
        protocol_path = self.base / "protocol.json"
        protocol = json.loads(protocol_path.read_text())
        protocol["config_files_sha256"][path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
        protocol_path.write_text(json.dumps(protocol), encoding="utf-8")
        with redirect_stdout(io.StringIO()):
            result = run_experiment(path, device="cpu")
        self.assertFalse(result["test_evaluated"])
        checkpoint = self.base / "self-feeding-smoke" / "latest.pt"
        self.assertTrue(checkpoint.is_file())
        self.assertTrue(__import__("torch").load(checkpoint, weights_only=True)["model"])
        resolved = json.loads((self.base / "self-feeding-smoke" / "resolved_run.json").read_text())
        self.assertEqual(resolved["objective"]["scheduled_sampling_rate"], 0.2)

    def test_freeze_registers_transition_balance_as_a_crossed_condition(self):
        from tide_jepa.pilot import freeze_pilot
        self.write_reviews()
        freeze_pilot(
            self.base, epochs=1, seeds=(17,), model_width=8, model_heads=2, model_layers=1,
            condition_modes=("token_only", "tide"), condition_source_copy_weights=(1.5,),
            condition_latent_objective_weights=(0.1,),
            condition_transition_balances=("row_uniform", "unique_transition"))
        protocol = json.loads((self.base / "protocol.json").read_text())
        self.assertEqual(len(protocol["configs"]), 4)
        configs = [json.loads((self.base / name).read_text()) for name in protocol["configs"]]
        self.assertEqual({item["training"]["transition_balance"] for item in configs},
                         {"row_uniform", "unique_transition"})
        primary = [item for item in configs if item["objective"]["mode"] == "tide"]
        self.assertEqual({item["objective"]["latent_objective_weight"] for item in primary}, {0.1})
        self.assertEqual(protocol["primary_transition_balance_modes"], ["row_uniform", "unique_transition"])

    def test_freeze_registers_vocabulary_and_source_pointer_decoder_conditions(self):
        from tide_jepa.pilot import freeze_pilot
        self.write_reviews()
        freeze_pilot(
            self.base, epochs=1, seeds=(17,), model_width=8, model_heads=2, model_layers=1,
            condition_modes=("tide",), condition_source_pointer_decoder_modes=("vocabulary", "source_pointer"),
            checkpoint_selection_policy="fixed_final_epoch")
        protocol = json.loads((self.base / "protocol.json").read_text())
        configs = [json.loads((self.base / name).read_text()) for name in protocol["configs"]]
        self.assertEqual(protocol["primary_source_pointer_decoder_modes"], ["vocabulary", "source_pointer"])
        self.assertIn("no matched-FLOP claim", protocol["compute_policy"])
        self.assertEqual({item["model"]["source_pointer_decoder"] for item in configs}, {False, True})
        self.assertEqual(len({item["output_dir"] for item in configs}), 2)

    def test_freeze_records_compute_matched_tide_matrix_and_final_epoch_selection(self):
        from tide_jepa.pilot import freeze_pilot
        self.write_reviews()
        freeze_pilot(
            self.base, epochs=1, seeds=(17,), model_width=8, model_heads=2, model_layers=1,
            condition_modes=("tide",), condition_source_copy_weights=(0.0, 1.5),
            condition_latent_objective_weights=(0.0, 0.1),
            checkpoint_selection_policy="fixed_final_epoch", compute_source_copy_term=True)
        protocol = json.loads((self.base / "protocol.json").read_text())
        configs = [json.loads((self.base / name).read_text()) for name in protocol["configs"]]
        self.assertEqual(len(configs), 4)
        self.assertTrue(all(config["checkpoint_selection_policy"] == "fixed_final_epoch"
                            for config in configs))
        self.assertTrue(all(config["objective"]["compute_source_copy_term"] is True
                            for config in configs))
        self.assertEqual(protocol["checkpoint_selection_policy"], "fixed_final_epoch")
        self.assertIn("all loss computations", protocol["compute_policy"])

    def test_freeze_accepts_reviewed_v419_and_binds_new_identity(self):
        from tide_jepa.pilot import REVIEWED_ARTIFACTS, freeze_pilot
        self.temporary.cleanup()
        self.temporary = tempfile.TemporaryDirectory()
        self.base = Path(self.temporary.name) / "vi-en-ai-v4.19"
        self.statement = author_seed_v4(self.base, version="v4.19")
        reviewed_hashes = {name: hashlib.sha256((self.base / name).read_bytes()).hexdigest()
                           for name in REVIEWED_ARTIFACTS}
        for name, reviewer in (("review-a.json", "luna-a"), ("review-b.json", "luna-b")):
            (self.base / name).write_text(json.dumps({
                "reviewer_id": reviewer, "reviewer_type": "AI", "decision": "approve",
                "draft_sha256": self.statement["draft_sha256"], "rows_checked": 15360,
                "artifact_sha256": reviewed_hashes,
            }))
        (self.base / "adjudication.json").write_text(json.dumps({
            "decision": "approve", "draft_sha256": self.statement["draft_sha256"],
            "human_validated": False,
        }))
        freeze_pilot(
            self.base, epochs=1, seeds=(17,), model_width=8, model_heads=2, model_layers=1,
            condition_modes=("tide",), condition_source_copy_weights=(0.0, 1.5),
            condition_latent_objective_weights=(0.0, 0.1),
            checkpoint_selection_policy="fixed_final_epoch", compute_source_copy_term=True)
        protocol = json.loads((self.base / "protocol.json").read_text())
        self.assertEqual(len(protocol["configs"]), 4)
        self.assertEqual(protocol["primary_quality_mode"], "tide")
        self.assertEqual(protocol["checkpoint_selection_policy"], "fixed_final_epoch")
        self.assertIn("all loss computations", protocol["compute_policy"])
        frozen_inventory = json.loads((self.base / "inventory.json").read_text())
        inventory = Inventory(tuple(Action(**item) for item in frozen_inventory["actions"]), {
            language: frozenset(Action(**item) for item in frozen_inventory["approved_by_language"][language])
            for language in ("en", "vi")
        })
        self.assertTrue(all("original-ai-authored-v4.19" in row.provenance_ref
                            for row in read_jsonl(self.base / "corpus.jsonl", inventory,
                                                  languages=("en", "vi"))))

    def test_freeze_requires_two_current_reviews_and_adjudication(self):
        from tide_jepa.pilot import freeze_pilot
        with self.assertRaises(FileNotFoundError):
            freeze_pilot(self.base, epochs=1, seeds=(17,))
        self.write_reviews()
        review = json.loads((self.base / "review-b.json").read_text())
        review["decision"] = "revise"
        (self.base / "review-b.json").write_text(json.dumps(review))
        with self.assertRaisesRegex(ValueError, "review missing"):
            freeze_pilot(self.base, epochs=1, seeds=(17,))

    def test_freeze_rejects_invalid_learning_rate_and_actual_length_before_publication(self):
        from tide_jepa.pilot import freeze_pilot
        self.write_reviews()
        for rate in (float("nan"), float("inf"), True, "bad", 0):
            with self.subTest(rate=rate), self.assertRaises(ValueError):
                freeze_pilot(self.base, learning_rate=rate)
        with self.assertRaisesRegex(ValueError, "maximum length"):
            freeze_pilot(self.base, max_length=8)
        self.assertFalse((self.base / "approval.json").exists())
        self.assertFalse((self.base / "corpus.jsonl").exists())

    def test_pending_review_requires_explicit_artifact_bound_adjudication(self):
        from tide_jepa.pilot import REVIEWED_ARTIFACTS, freeze_pilot
        self.write_reviews()
        review = json.loads((self.base / "review-a.json").read_text())
        review["decision"] = "needs-adjudication"
        (self.base / "review-a.json").write_text(json.dumps(review), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "explicit artifact-bound adjudication"):
            freeze_pilot(self.base, epochs=1, seeds=(17,))

        hashes = {name: hashlib.sha256((self.base / name).read_bytes()).hexdigest() for name in REVIEWED_ARTIFACTS}
        reviewers = [json.loads((self.base / f"review-{name}.json").read_text())["reviewer_id"] for name in ("a", "b")]
        adjudication = {"decision": "approve", "draft_sha256": self.statement["draft_sha256"],
                        "human_validated": False, "adjudicator_type": "AI", "reviewer_ids": reviewers,
                        "resolved_review_ids": [reviewers[0]], "artifact_sha256": hashes,
                        "resolution": "The independent aggregate-only semantic audit resolved the scope concern."}
        (self.base / "adjudication.json").write_text(json.dumps(adjudication), encoding="utf-8")
        approval = freeze_pilot(self.base, epochs=1, seeds=(17,))
        self.assertFalse(approval["human_validated"])

    def test_frozen_split_is_shared_by_all_modes_and_excludes_cham(self):
        approval = self.freeze()
        self.assertEqual(approval["languages"], ["en", "vi"])
        self.assertFalse(approval["human_validated"])
        configs = [json.loads((self.base / f"{mode}-seed-17.json").read_text()) for mode in ("token_only", "generic_jepa", "static_alignment", "tide")]
        self.assertEqual({c["frozen_split"] for c in configs}, {"split_manifest.json"})
        self.assertTrue(all(c["languages"] == ["en", "vi"] for c in configs))
        split = json.loads((self.base / "split_manifest.json").read_text())
        self.assertEqual({name: len(ids) for name, ids in split["record_ids"].items()}, {"train": 240, "validation": 80, "test": 80})

    def test_freeze_registers_matched_two_by_two_copy_loss_conditions(self):
        from tide_jepa.pilot import freeze_pilot
        self.write_reviews()
        freeze_pilot(self.base, epochs=1, seeds=(17, 23, 41), primary_mode="tide",
                     condition_modes=("token_only", "tide"),
                     condition_source_copy_weights=(0.0, 1.5))
        protocol = json.loads((self.base / "protocol.json").read_text())
        configs = [json.loads((self.base / name).read_text()) for name in protocol["configs"]]
        self.assertEqual(len(configs), 12)
        self.assertEqual(protocol["modes"], ["token_only", "tide"])
        self.assertEqual(protocol["primary_source_copy_weights"], [0.0, 1.5])
        self.assertEqual({(c["objective"]["mode"], c["objective"].get("source_copy_weight", 0.0), c["seed"])
                          for c in configs},
                         {(mode, weight, seed) for mode in ("token_only", "tide")
                          for weight in (0.0, 1.5) for seed in (17, 23, 41)})
        self.assertEqual(len({c["output_dir"] for c in configs}), 12)

    def test_freeze_registers_copy_loss_dose_response_primary_weights(self):
        from tide_jepa.pilot import freeze_pilot
        self.write_reviews()
        freeze_pilot(self.base, epochs=1, seeds=(17, 23, 41), primary_mode="tide",
                     condition_modes=("token_only", "tide"),
                     condition_source_copy_weights=(1.5, 3.0))
        protocol = json.loads((self.base / "protocol.json").read_text())
        configs = [json.loads((self.base / name).read_text()) for name in protocol["configs"]]
        self.assertEqual(len(configs), 12)
        self.assertEqual(protocol["primary_source_copy_weights"], [1.5, 3.0])
        self.assertEqual({(c["objective"]["mode"], c["objective"].get("source_copy_weight", 0.0), c["seed"])
                          for c in configs},
                         {(mode, weight, seed) for mode in ("token_only", "tide")
                          for weight in (1.5, 3.0) for seed in (17, 23, 41)})

    def test_freeze_registers_v418_tide_copy_factorial(self):
        from tide_jepa.pilot import freeze_pilot
        self.write_reviews()
        freeze_pilot(self.base, epochs=1, seeds=(17, 23, 41), primary_mode="tide",
                     condition_modes=("tide",),
                     condition_source_copy_weights=(0.0, 1.5),
                     condition_latent_objective_weights=(0.0, 0.1),
                     condition_transition_balances=("unique_transition",))
        protocol = json.loads((self.base / "protocol.json").read_text())
        configs = [json.loads((self.base / name).read_text()) for name in protocol["configs"]]
        self.assertEqual(len(configs), 12)
        self.assertEqual(protocol["primary_source_copy_weights"], [0.0, 1.5])
        self.assertEqual(protocol["primary_latent_objective_weights"], [0.0, 0.1])
        self.assertEqual(protocol["primary_transition_balance_modes"], ["unique_transition"])
        self.assertEqual(protocol["quality_thresholds"]["semantic_checker_coverage_rate"], 1.0)
        self.assertEqual({(c["objective"].get("source_copy_weight", 0.0),
                           c["objective"]["latent_objective_weight"], c["seed"])
                          for c in configs},
                         {(copy_weight, latent_weight, seed)
                          for copy_weight in (0.0, 1.5) for latent_weight in (0.0, 0.1)
                          for seed in (17, 23, 41)})
        self.assertEqual({c["training"]["transition_balance"] for c in configs},
                         {"unique_transition"})
        self.assertEqual(len({c["output_dir"] for c in configs}), 12)

    def test_freeze_registers_latent_objective_dose_response(self):
        from tide_jepa.pilot import freeze_pilot
        self.write_reviews()
        freeze_pilot(self.base, epochs=1, seeds=(17, 23, 41), primary_mode="tide",
                     condition_modes=("token_only", "tide"),
                     condition_source_copy_weights=(1.5,),
                     condition_latent_objective_weights=(0.5, 1.0))
        protocol = json.loads((self.base / "protocol.json").read_text())
        configs = [json.loads((self.base / name).read_text()) for name in protocol["configs"]]
        self.assertEqual(len(configs), 9)
        self.assertEqual(protocol["primary_latent_objective_weights"], [0.5, 1.0])
        self.assertEqual(protocol["latent_objective_multiplier_scope"],
                         ["jepa", "alignment", "variance", "path_jepa", "path_alignment"])
        self.assertEqual(sum(c["objective"]["mode"] == "token_only" for c in configs), 3)
        self.assertEqual(sum(c["objective"]["mode"] == "tide"
                             and c["objective"]["latent_objective_weight"] == 0.5 for c in configs), 3)
        self.assertEqual(sum(c["objective"]["mode"] == "tide"
                             and c["objective"]["latent_objective_weight"] == 1.0 for c in configs), 3)
        self.assertEqual(len({c["output_dir"] for c in configs}), 9)

    def test_freeze_registers_lower_latent_objective_dose_response(self):
        from tide_jepa.pilot import freeze_pilot
        self.write_reviews()
        freeze_pilot(self.base, epochs=1, seeds=(17, 23, 41), primary_mode="tide",
                     condition_modes=("token_only", "tide"),
                     condition_source_copy_weights=(1.5,),
                     condition_latent_objective_weights=(0.1, 0.25))
        protocol = json.loads((self.base / "protocol.json").read_text())
        configs = [json.loads((self.base / name).read_text()) for name in protocol["configs"]]
        self.assertEqual(len(configs), 9)
        self.assertEqual(protocol["primary_latent_objective_weights"], [0.1, 0.25])
        self.assertEqual(sum(c["objective"]["mode"] == "token_only" for c in configs), 3)
        self.assertEqual(sum(c["objective"]["mode"] == "tide"
                             and c["objective"]["latent_objective_weight"] == 0.1 for c in configs), 3)
        self.assertEqual(sum(c["objective"]["mode"] == "tide"
                             and c["objective"]["latent_objective_weight"] == 0.25 for c in configs), 3)
        self.assertEqual(len({c["output_dir"] for c in configs}), 9)

    def test_modified_review_is_rejected_before_training(self):
        from tide_jepa.experiment import run_experiment
        self.freeze()
        config_path = self.base / "token_only-seed-17.json"
        config = json.loads(config_path.read_text())
        config["output_dir"] = str(self.base / "local-run")
        config_path.write_text(json.dumps(config))
        with (self.base / "review-a.json").open("a") as stream:
            stream.write("\n")
        with self.assertRaisesRegex(ValueError, "changed after freeze"):
            run_experiment(config_path, device="cpu")
        self.assertFalse((self.base / "local-run").exists())

    def test_frozen_manifest_rejects_corpus_change_and_cross_split_text(self):
        from dataclasses import replace
        from tide_jepa.data import dataset_fingerprint, read_jsonl, read_split_manifest
        from tide_jepa.experiment import _parse_inventory
        self.freeze()
        inventory = _parse_inventory(json.loads((self.base / "inventory.json").read_text()))
        rows = read_jsonl(self.base / "corpus.jsonl", inventory)
        changed = (replace(rows[0], source_text="a changed original synthetic sentence"),) + rows[1:]
        with self.assertRaisesRegex(ValueError, "fingerprint differs"):
            read_split_manifest(self.base / "split_manifest.json", changed, inventory)
        test_index = next(i for i, r in enumerate(rows) if r.split_group_id == "authored-paint" and r.language == rows[0].language)
        changed = list(rows)
        changed[test_index] = replace(rows[test_index], source_text=rows[0].source_text)
        manifest = json.loads((self.base / "split_manifest.json").read_text())
        manifest["dataset_sha256"] = dataset_fingerprint(changed)
        (self.base / "split_manifest.json").write_text(json.dumps(manifest))
        with self.assertRaisesRegex(ValueError, "multiple splits"):
            read_split_manifest(self.base / "split_manifest.json", changed, inventory)

    def test_train_resume_generate_and_identity_guard(self):
        from tide_jepa.experiment import run_experiment
        from tide_jepa.infer import OfflineGenerator
        self.freeze()
        path = self.base / "token_only-seed-17.json"
        config = json.loads(path.read_text())
        output = self.base / "local-run"
        config["output_dir"] = str(output)
        path.write_text(json.dumps(config))
        protocol_path = self.base / "protocol.json"
        protocol = json.loads(protocol_path.read_text())
        protocol["config_files_sha256"][path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
        protocol_path.write_text(json.dumps(protocol))
        with redirect_stdout(io.StringIO()):
            result = run_experiment(path, device="cpu")
            resumed = run_experiment(path, resume=True, device="cpu")
        self.assertFalse(result["test_evaluated"])
        self.assertEqual(resumed["steps"], result["steps"])
        self.assertEqual(resumed["best_validation_loss"], result["best_validation_loss"])
        import csv
        with (output / "metrics.csv").open("r", encoding="utf-8", newline="") as stream:
            metric_rows = list(csv.reader(stream))
        with (output / "metrics.csv").open("a", encoding="utf-8", newline="") as stream:
            csv.writer(stream).writerow(metric_rows[-1])
        with self.assertRaisesRegex(ValueError, "duplicate or missing rows"):
            run_experiment(path, resume=True, device="cpu")
        generator = OfflineGenerator(path, output / "best.pt", device="cpu")
        response = generator.generate({"source": "Original test source.", "source_language": "en", "target_language": "en", "actions": [{"kind": "TIME", "value": "PAST"}], "max_new_tokens": 2})
        self.assertIn("valid_utf8", response)
        self.assertEqual(response["quality_status"], "diagnostic_only")
        with self.assertRaisesRegex(ValueError, "cross-language"):
            generator.generate({"source": "Original", "source_language": "vi", "target_language": "en", "actions": [{"kind": "TIME", "value": "PAST"}]})
        with self.assertRaises(ValueError):
            generator.generate({"source": "Original", "target_language": "cham_phan_rang", "actions": [{"kind": "TIME", "value": "PAST"}]})
        with self.assertRaises(FileExistsError):
            run_experiment(path, device="cpu")
        config["seed"] = 99
        path.write_text(json.dumps(config))
        with self.assertRaisesRegex(ValueError, "checkpoint identity"):
            OfflineGenerator(path, output / "best.pt", device="cpu")
        provenance_before = (output / "resolved_run.json").read_bytes()
        with self.assertRaisesRegex(ValueError, "run identity"):
            run_experiment(path, resume=True, device="cpu")
        self.assertEqual((output / "resolved_run.json").read_bytes(), provenance_before)

    def test_source_pointer_checkpoint_trains_and_loads_for_inference(self):
        from tide_jepa.experiment import run_experiment
        from tide_jepa.infer import OfflineGenerator
        from tide_jepa.pilot import freeze_pilot
        self.write_reviews()
        freeze_pilot(
            self.base, epochs=1, seeds=(17,), model_width=8, model_heads=2, model_layers=1,
            condition_modes=("tide",), condition_source_pointer_decoder_modes=("source_pointer",),
            checkpoint_selection_policy="fixed_final_epoch")
        protocol = json.loads((self.base / "protocol.json").read_text())
        path = self.base / protocol["configs"][0]
        config = json.loads(path.read_text())
        self.assertTrue(config["model"]["source_pointer_decoder"])
        output = self.base / "local-pointer-run"
        config["output_dir"] = str(output)
        path.write_text(json.dumps(config))
        protocol["config_files_sha256"][path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
        (self.base / "protocol.json").write_text(json.dumps(protocol))
        with redirect_stdout(io.StringIO()):
            result = run_experiment(path, device="cpu")
        self.assertFalse(result["test_evaluated"])
        generator = OfflineGenerator(path, output / "best.pt", device="cpu")
        response = generator.generate({
            "source": "Lan đọc một cuốn sách.", "source_language": "vi", "target_language": "vi",
            "actions": [{"kind": "TIME", "value": "PAST"}], "max_new_tokens": 16,
        })
        self.assertTrue(response["valid_utf8"])
        self.assertEqual(response["quality_status"], "diagnostic_only")

    def test_release_gate_accepts_decoder_matrix_then_refuses_missing_validation(self):
        from tide_jepa.experiment import run_experiment, _parse_inventory
        from tide_jepa.data import read_split_manifest
        from tide_jepa.pilot import freeze_pilot, _require_release_test_gate
        self.write_reviews()
        freeze_pilot(self.base, epochs=1, seeds=(17,), model_width=8, model_heads=2,
                     condition_modes=("tide",),
                     condition_source_pointer_decoder_modes=("vocabulary", "source_pointer"))
        protocol = json.loads((self.base / "protocol.json").read_text())
        for index, name in enumerate(protocol["configs"]):
            path = self.base / name
            config = json.loads(path.read_text())
            config["output_dir"] = str(self.base / f"local-decoder-{index}")
            path.write_text(json.dumps(config))
            protocol["config_files_sha256"][name] = hashlib.sha256(path.read_bytes()).hexdigest()
        (self.base / "protocol.json").write_text(json.dumps(protocol))
        with redirect_stdout(io.StringIO()):
            for name in protocol["configs"]:
                run_experiment(self.base / name, device="cpu")
        inventory = _parse_inventory(json.loads((self.base / "inventory.json").read_text()))
        rows = read_jsonl(self.base / "corpus.jsonl", inventory)
        manifest = read_split_manifest(self.base / "split_manifest.json", rows, inventory)
        with self.assertRaisesRegex(ValueError, "validation generation evidence is missing"):
            _require_release_test_gate(self.base, protocol, manifest, rows)
        self.assertFalse(any(self.base.glob("local-decoder-*/test_metrics.json")))

    def test_invalid_alignment_does_not_publish_approved_artifacts(self):
        from tide_jepa.pilot import freeze_pilot
        alignments = json.loads((self.base / "alignments.draft.json").read_text())
        alignments["edge_pairs"][0]["relation"] = "unknown"
        (self.base / "alignments.draft.json").write_text(json.dumps(alignments))
        self.write_reviews()
        with self.assertRaisesRegex(ValueError, "same_event"):
            freeze_pilot(self.base, epochs=1, seeds=(17,))
        for name in ("corpus.jsonl", "inventory.json", "approval.json"):
            self.assertFalse((self.base / name).exists())

    def test_incomplete_review_hash_map_is_refused(self):
        from tide_jepa.experiment import _canonical_hash, _parse_inventory
        from tide_jepa.data import read_jsonl, read_split_manifest
        from tide_jepa.pilot import validate_review_gate
        self.freeze()
        approval = json.loads((self.base / "approval.json").read_text())
        approval["review_files_sha256"] = {}
        (self.base / "approval.json").write_text(json.dumps(approval))
        inventory_value = json.loads((self.base / "inventory.json").read_text())
        inventory = _parse_inventory(inventory_value)
        rows = read_jsonl(self.base / "corpus.jsonl", inventory)
        manifest = read_split_manifest(self.base / "split_manifest.json", rows, inventory)
        config = json.loads((self.base / "token_only-seed-17.json").read_text())
        with self.assertRaisesRegex(ValueError, "complete reviews"):
            validate_review_gate(self.base, config, manifest, _canonical_hash(inventory_value), _canonical_hash(json.loads((self.base / "alignments.json").read_text())))

    def test_interrupted_epoch_resume_matches_uninterrupted_run(self):
        from unittest.mock import patch
        import torch
        from tide_jepa.experiment import run_experiment
        from tide_jepa.pilot import freeze_pilot
        from tide_jepa.training import Trainer
        self.write_reviews()
        freeze_pilot(self.base, epochs=2, seeds=(17,))
        config = json.loads((self.base / "tide-seed-17.json").read_text())
        uninterrupted = self.base / "uninterrupted"
        interrupted = self.base / "interrupted"
        config["output_dir"] = str(uninterrupted)
        first_path = self.base / "first.json"
        first_path.write_text(json.dumps(config))
        with redirect_stdout(io.StringIO()):
            run_experiment(first_path, device="cpu")
        config["output_dir"] = str(interrupted)
        second_path = self.base / "second.json"
        second_path.write_text(json.dumps(config))
        original_step = Trainer.step
        calls = []
        def fail_after_first_epoch(trainer, batch):
            calls.append(True)
            if len(calls) == 4:
                raise RuntimeError("synthetic interruption")
            return original_step(trainer, batch)
        with patch.object(Trainer, "step", fail_after_first_epoch), redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(RuntimeError, "synthetic interruption"):
                run_experiment(second_path, device="cpu")
        with redirect_stdout(io.StringIO()):
            run_experiment(second_path, resume=True, device="cpu")
        first = torch.load(uninterrupted / "latest.pt", weights_only=True)
        second = torch.load(interrupted / "latest.pt", weights_only=True)
        self.assertEqual(first["steps"], second["steps"])
        self.assertTrue(all(torch.equal(value, second["model"][key]) for key, value in first["model"].items()))

    def test_fixed_final_epoch_policy_publishes_last_epoch_as_best(self):
        import torch
        from tide_jepa.experiment import run_experiment
        self.freeze()
        path = self.base / "tide-seed-17.json"
        config = json.loads(path.read_text())
        config["output_dir"] = str(self.base / "fixed-final")
        config["training"]["epochs"] = 2
        config["checkpoint_selection_policy"] = "fixed_final_epoch"
        path.write_text(json.dumps(config))
        with redirect_stdout(io.StringIO()):
            run_experiment(path, device="cpu")
        latest = torch.load(self.base / "fixed-final" / "latest.pt", weights_only=True)
        best = torch.load(self.base / "fixed-final" / "best.pt", weights_only=True)
        self.assertEqual(latest["epoch"], 2)
        self.assertEqual(best["epoch"], 2)
        self.assertTrue(all(torch.equal(value, best["model"][key])
                            for key, value in latest["model"].items()))

    def test_latest_best_crash_recovers_but_release_test_stays_sealed(self):
        from unittest.mock import patch
        import torch
        import tide_jepa.experiment as experiment
        self.write_reviews()
        self.freeze()
        path = self.base / "token_only-seed-17.json"
        config = json.loads(path.read_text())
        output = self.base / "crash-recovery"
        config["output_dir"] = str(output)
        path.write_text(json.dumps(config))
        protocol_path = self.base / "protocol.json"
        protocol = json.loads(protocol_path.read_text())
        protocol["config_files_sha256"][path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
        protocol_path.write_text(json.dumps(protocol))
        save = experiment._save_checkpoint
        def crash_before_best(destination, state):
            if destination.name == "best.pt":
                raise RuntimeError("interrupted before best publication")
            return save(destination, state)
        with patch.object(experiment, "_save_checkpoint", crash_before_best), redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(RuntimeError, "best publication"):
                experiment.run_experiment(path, device="cpu")
        latest = torch.load(output / "latest.pt", weights_only=True)
        self.assertFalse((output / "best.pt").exists())
        self.assertEqual(latest["best_epoch"], 1)
        with redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(ValueError, "release holdout remains sealed"):
                experiment.run_experiment(path, resume=True, evaluate_test=True, device="cpu")
        from tide_jepa.pilot import evaluate_generation
        with self.assertRaisesRegex(ValueError, "release holdout remains sealed"):
            evaluate_generation(path, split="test")
        self.assertTrue((output / "best.pt").is_file())
        self.assertFalse((output / "test_metrics.json").exists())
        self.assertFalse((output / "generation_metrics.json").exists())

    def test_hard_process_exit_after_fsynced_metrics_or_latest_recovers(self):
        import os
        import subprocess
        import sys
        self.write_reviews()
        self.freeze()
        template_path = self.base / "token_only-seed-17.json"
        protocol_path = self.base / "protocol.json"
        child_code = r"""
import os
import sys
from pathlib import Path
import tide_jepa.experiment as experiment

output = Path(sys.argv[1])
crash_point = sys.argv[2]
sync_directory = experiment._fsync_directory
replace_file = experiment.os.replace

def replace_then_exit(source, destination):
    if (crash_point == "before_initial_metrics_replace"
            and Path(destination).name == "metrics.csv"
            and not (output / "latest.pt").exists()
            and not Path(destination).exists()):
        os._exit(86)
    if (crash_point == "before_metrics_replace"
            and Path(destination).name == "metrics.csv"
            and (output / "latest.pt").exists()):
        os._exit(86)
    return replace_file(source, destination)

experiment.os.replace = replace_then_exit

def sync_then_exit(directory):
    sync_directory(directory)
    if Path(directory) != output:
        return
    latest = output / "latest.pt"
    best = output / "best.pt"
    metrics = output / "metrics.csv"
    if crash_point == "after_metrics" and metrics.is_file() and not latest.exists():
        if metrics.read_bytes().count(b"\n") > 1:
            os._exit(86)
    if crash_point == "after_latest" and latest.is_file() and not best.exists():
        os._exit(86)

experiment._fsync_directory = sync_then_exit
experiment.run_experiment(sys.argv[3], device="cpu")
"""
        for crash_point in (
            "before_initial_metrics_replace", "after_metrics", "after_latest", "before_metrics_replace"
        ):
            with self.subTest(crash_point=crash_point), tempfile.TemporaryDirectory() as temporary:
                output = Path(temporary) / "run"
                config_path = self.base / f"hard-crash-{crash_point}.json"
                config = json.loads(template_path.read_text(encoding="utf-8"))
                config["output_dir"] = str(output)
                if crash_point == "before_metrics_replace":
                    config["training"]["epochs"] = 2
                config_path.write_text(json.dumps(config), encoding="utf-8")
                protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
                protocol["config_files_sha256"][config_path.name] = hashlib.sha256(
                    config_path.read_bytes()
                ).hexdigest()
                protocol_path.write_text(json.dumps(protocol), encoding="utf-8")

                child = subprocess.run(
                    [sys.executable, "-B", "-c", child_code, str(output), crash_point, str(config_path)],
                    cwd=Path(__file__).resolve().parents[1],
                    env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=120,
                )
                self.assertEqual(child.returncode, 86, child.stderr)
                if crash_point == "before_initial_metrics_replace":
                    self.assertFalse((output / "metrics.csv").exists())
                    self.assertFalse((output / "latest.pt").exists())
                    self.assertEqual(len(list(output.glob(".metrics.csv.*"))), 1)
                else:
                    self.assertTrue((output / "metrics.csv").is_file())
                if crash_point == "before_initial_metrics_replace":
                    pass
                elif crash_point == "after_metrics":
                    self.assertFalse((output / "latest.pt").exists())
                elif crash_point == "after_latest":
                    self.assertTrue((output / "latest.pt").is_file())
                    self.assertFalse((output / "best.pt").exists())
                else:
                    import csv
                    import torch
                    self.assertEqual(torch.load(output / "latest.pt", weights_only=True)["epoch"], 1)
                    with (output / "metrics.csv").open("r", encoding="utf-8", newline="") as stream:
                        epochs = {int(row["epoch"]) for row in csv.DictReader(stream)}
                    self.assertEqual(epochs, {1})
                    self.assertEqual(len(list(output.glob(".metrics.csv.*"))), 1)

                from tide_jepa.experiment import run_experiment
                with redirect_stdout(io.StringIO()):
                    result = run_experiment(config_path, resume=True, device="cpu")
                self.assertEqual(result["last_epoch"], config["training"]["epochs"])
                self.assertTrue((output / "latest.pt").is_file())
                self.assertTrue((output / "best.pt").is_file())
                self.assertFalse((output / "test_metrics.json").exists())
                self.assertFalse((output / "generation_metrics.json").exists())
                if crash_point == "after_metrics":
                    self.assertEqual(len(list(output.glob("metrics.uncheckpointed-*.csv"))), 1)
                self.assertFalse(list(output.glob(".metrics.csv.*")))
                self.assertFalse(list(output.glob(".latest.pt.*")))

    def test_uncheckpointed_first_epoch_metrics_are_preserved_and_restarted(self):
        import csv
        from unittest.mock import patch
        import tide_jepa.experiment as experiment
        self.write_reviews()
        self.freeze()
        path = self.base / "token_only-seed-17.json"
        config = json.loads(path.read_text())
        output = self.base / "crash-before-first-checkpoint"
        config["output_dir"] = str(output)
        path.write_text(json.dumps(config))
        protocol_path = self.base / "protocol.json"
        protocol = json.loads(protocol_path.read_text())
        protocol["config_files_sha256"][path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
        protocol_path.write_text(json.dumps(protocol))
        append = experiment._append_metrics_rows
        def crash_after_metrics(destination, rows):
            append(destination, rows)
            raise RuntimeError("synthetic crash after epoch metrics")
        with patch.object(experiment, "_append_metrics_rows", side_effect=crash_after_metrics), \
                redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(RuntimeError, "after epoch metrics"):
                experiment.run_experiment(path, device="cpu")
        self.assertTrue((output / "metrics.csv").is_file())
        self.assertFalse((output / "latest.pt").exists())
        with redirect_stdout(io.StringIO()):
            result = experiment.run_experiment(path, resume=True, device="cpu")
        archives = list(output.glob("metrics.uncheckpointed-*.csv"))
        self.assertEqual(len(archives), 1)
        self.assertEqual(result["last_epoch"], config["training"]["epochs"])
        self.assertTrue((output / "latest.pt").is_file())
        self.assertTrue((output / "best.pt").is_file())
        with (output / "metrics.csv").open("r", encoding="utf-8", newline="") as stream:
            rows = list(csv.DictReader(stream))
        epochs = sorted({int(row["epoch"]) for row in rows})
        self.assertEqual(epochs, list(range(1, config["training"]["epochs"] + 1)))

    def test_orphan_metrics_after_published_checkpoint_are_reconciled_on_resume(self):
        import csv
        from unittest.mock import patch
        import torch
        import tide_jepa.experiment as experiment
        self.write_reviews()
        self.freeze()
        path = self.base / "token_only-seed-17.json"
        config = json.loads(path.read_text())
        config["training"]["epochs"] = 3
        output = self.base / "crash-after-first-checkpoint"
        config["output_dir"] = str(output)
        path.write_text(json.dumps(config))
        protocol_path = self.base / "protocol.json"
        protocol = json.loads(protocol_path.read_text())
        protocol["config_files_sha256"][path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
        protocol_path.write_text(json.dumps(protocol))
        append = experiment._append_metrics_rows
        calls = 0

        def crash_after_second_epoch_metrics(destination, rows):
            nonlocal calls
            append(destination, rows)
            calls += 1
            if calls == 2:
                raise RuntimeError("synthetic crash after later epoch metrics")

        with patch.object(experiment, "_append_metrics_rows", side_effect=crash_after_second_epoch_metrics), \
                redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(RuntimeError, "later epoch metrics"):
                experiment.run_experiment(path, device="cpu")
        latest = torch.load(output / "latest.pt", weights_only=True)
        self.assertEqual(latest["epoch"], 1)
        with (output / "metrics.csv").open("r", encoding="utf-8", newline="") as stream:
            interrupted_rows = list(csv.DictReader(stream))
        self.assertEqual(sorted({int(row["epoch"]) for row in interrupted_rows}), [1, 2])

        with redirect_stdout(io.StringIO()):
            result = experiment.run_experiment(path, resume=True, device="cpu")
        self.assertEqual(result["last_epoch"], config["training"]["epochs"])
        latest = torch.load(output / "latest.pt", weights_only=True)
        self.assertEqual(latest["epoch"], config["training"]["epochs"])
        with (output / "metrics.csv").open("r", encoding="utf-8", newline="") as stream:
            rows = list(csv.DictReader(stream))
        counts = {}
        for row in rows:
            counts.setdefault(int(row["epoch"]), {})[row["split"]] = counts.get(int(row["epoch"]), {}).get(row["split"], 0) + 1
        self.assertEqual(
            counts,
            {epoch: {"train": 1, "validation": 1}
             for epoch in range(1, config["training"]["epochs"] + 1)},
        )

    def test_atomic_publication_replace_failure_preserves_previous_outputs(self):
        from unittest.mock import patch
        import torch
        import tide_jepa.experiment as experiment

        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            cases = (
                ("json", base / "manifest.json", b'{"old": true}\n',
                 lambda path: experiment._atomic_json(path, {"new": True})),
                ("csv", base / "metrics.csv", b"epoch,split\n1,train\n",
                 lambda path: experiment._write_csv_atomic(path, ("epoch", "split"), [(2, "train")])),
                ("checkpoint", base / "latest.pt", b"previous checkpoint",
                 lambda path: experiment._save_checkpoint(path, {"epoch": 2, "weights": torch.tensor([1.0])})),
            )
            for label, destination, previous, publish in cases:
                with self.subTest(kind=label):
                    destination.write_bytes(previous)
                    with patch.object(experiment.os, "replace", side_effect=OSError("injected replace failure")):
                        with self.assertRaisesRegex(OSError, "injected replace failure"):
                            publish(destination)
                    self.assertEqual(destination.read_bytes(), previous)
                    self.assertFalse(list(base.glob(f".{destination.name}.*")))

    def test_atomic_publication_fsync_failures_have_recoverable_states(self):
        from unittest.mock import patch
        import torch
        import tide_jepa.experiment as experiment

        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            cases = (
                ("json", base / "manifest.json", b'{"old": true}\n',
                 lambda path: experiment._atomic_json(path, {"new": True})),
                ("csv", base / "metrics.csv", b"epoch,split\n1,train\n",
                 lambda path: experiment._write_csv_atomic(path, ("epoch", "split"), [(2, "train")])),
                ("checkpoint", base / "latest.pt", b"previous checkpoint",
                 lambda path: experiment._save_checkpoint(path, {"epoch": 2, "weights": torch.tensor([1.0])})),
            )
            for label, destination, previous, publish in cases:
                for failed_sync, old_destination_survives in ((1, True), (2, False)):
                    with self.subTest(kind=label, failed_sync=failed_sync):
                        destination.write_bytes(previous)
                        sync_calls = 0

                        def fail_selected_sync(_descriptor):
                            nonlocal sync_calls
                            sync_calls += 1
                            if sync_calls == failed_sync:
                                raise OSError("injected fsync failure")

                        with patch.object(experiment.os, "fsync", side_effect=fail_selected_sync):
                            with self.assertRaisesRegex(OSError, "injected fsync failure"):
                                publish(destination)
                        self.assertEqual(sync_calls, failed_sync)
                        if old_destination_survives:
                            self.assertEqual(destination.read_bytes(), previous)
                        else:
                            self.assertNotEqual(destination.read_bytes(), previous)
                        self.assertFalse(list(base.glob(f".{destination.name}.*")))

    def test_run_experiment_excludes_concurrent_writer_and_releases_lock(self):
        import subprocess
        import sys
        from unittest.mock import patch
        import tide_jepa.experiment as experiment
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            config_path = base / "run.json"
            config_path.write_text(json.dumps({"output_dir": "run-output"}))
            output_dir = base / "run-output"
            with patch.object(experiment, "_run_experiment_unlocked", return_value={"started": True}) as runner:
                with experiment._output_directory_lock(output_dir):
                    with self.assertRaisesRegex(RuntimeError, "another training process"):
                        experiment.run_experiment(config_path, device="cpu")
                    runner.assert_not_called()
                    child_script = (
                        "import sys\n"
                        "from pathlib import Path\n"
                        "from tide_jepa.experiment import _output_directory_lock\n"
                        "try:\n"
                        "    with _output_directory_lock(Path(sys.argv[1])):\n"
                        "        pass\n"
                        "except RuntimeError:\n"
                        "    raise SystemExit(23)\n"
                    )
                    child = subprocess.run(
                        [sys.executable, "-c", child_script, str(output_dir)],
                        cwd=Path(__file__).resolve().parents[1],
                        capture_output=True, text=True, check=False, timeout=30,
                    )
                    self.assertEqual(child.returncode, 23, child.stderr)
                self.assertEqual(experiment.run_experiment(config_path, device="cpu"), {"started": True})
                runner.assert_called_once()

            with patch.object(experiment, "_run_experiment_unlocked", side_effect=ValueError("test failure")):
                with self.assertRaisesRegex(ValueError, "test failure"):
                    experiment.run_experiment(config_path, device="cpu")
            with experiment._output_directory_lock(output_dir):
                pass

    def test_group_batch_preflight_rejects_large_indivisible_group(self):
        from types import SimpleNamespace
        from tide_jepa.experiment import _batch_records
        rows = [SimpleNamespace(split_group_id="oversized", source_text="a", target_text="b") for _ in range(513)]
        with self.assertRaisesRegex(ValueError, "preflight budget"):
            list(_batch_records(rows, 32))

    def test_phomt_protected_output_is_rejected_before_directory_creation(self):
        from dataclasses import replace
        from tide_jepa.experiment import run_experiment
        from tide_jepa.data import read_jsonl
        from tide_jepa.experiment import _parse_inventory
        self.freeze()
        inventory = _parse_inventory(json.loads((self.base / "inventory.json").read_text()))
        rows = list(read_jsonl(self.base / "corpus.jsonl", inventory))
        rows[0] = replace(rows[0], provenance_ref="approved PhoMT source", license_ref="PhoMT research-only")
        (self.base / "corpus.jsonl").write_text("".join(json.dumps(r.to_dict(), ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
        path = self.base / "token_only-seed-17.json"
        config = json.loads(path.read_text())
        destination = Path(self.temporary.name) / "unsafe-output"
        config["output_dir"] = str(destination)
        path.write_text(json.dumps(config))
        with self.assertRaisesRegex(ValueError, "under project data"):
            run_experiment(path, device="cpu")
        self.assertFalse(destination.exists())

    def test_evaluation_metrics_use_metric_specific_denominators(self):
        from types import SimpleNamespace
        from unittest.mock import patch
        import tide_jepa.experiment as experiment
        from tide_jepa.training import Objective
        rows = (SimpleNamespace(split_group_id="a", source_text="a", target_text="b"),
                SimpleNamespace(split_group_id="b", source_text="a", target_text="b"),
                SimpleNamespace(split_group_id="b", source_text="a", target_text="b"),
                SimpleNamespace(split_group_id="b", source_text="a", target_text="b"))
        def fake_loss(_model, batch, _inventory, _objective):
            size = len(batch)
            return None, {"token": 0.0 if size == 1 else 10.0,
                          "token_count": 2 if size == 1 else 10,
                          "copy_token": 6.0 if size == 1 else 8.0,
                          "copy_token_count": 2 if size == 1 else 10,
                          "edge_count": size,
                          "jepa": 2.0 if size == 1 else 4.0,
                          "alignment_count": 1 if size == 1 else 3,
                          "alignment": 1.0 if size == 1 else 5.0,
                          "path_count": 1 if size == 1 else 3,
                          "path_jepa": 3.0 if size == 1 else 6.0,
                          "path_token": 7.0 if size == 1 else 9.0,
                          "path_alignment_count": 1 if size == 1 else 2,
                          "path_alignment": 2.0 if size == 1 else 8.0,
                          "variance": 0.0, "latent_std": 1.0}
        class Model:
            def eval(self): pass
        with patch.object(experiment, "_build_experiment_batch", side_effect=lambda batch, *_args: batch), \
             patch.object(experiment, "compute_loss", side_effect=fake_loss):
            result = experiment._evaluate(Model(), rows, None, None, Objective(), 2, "cpu", (), ())
        self.assertAlmostEqual(result["token"], 100 / 12)
        self.assertEqual(result["token_count"], 12)
        self.assertAlmostEqual(result["copy_token"], 92 / 12)
        self.assertEqual(result["copy_token_count"], 12)
        self.assertAlmostEqual(result["jepa"], 3.5)
        self.assertAlmostEqual(result["alignment"], 4.0)
        self.assertAlmostEqual(result["path_token"], 8.5)
        self.assertEqual(result["alignment_count"], 4)


if __name__ == "__main__":
    unittest.main()
