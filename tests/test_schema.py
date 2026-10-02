import unittest

from tide_jepa import (
    Action,
    Edge,
    EdgePair,
    EdgePath,
    Inventory,
    ModelConfig,
    PathPair,
    validate_pair,
    validate_path,
    validate_path_pair,
)


class SchemaTests(unittest.TestCase):
    def setUp(self):
        self.action = Action("TEST_KIND", "TEST_VALUE")
        self.inventory = Inventory((self.action,), {"en": frozenset([self.action]), "vi": frozenset([self.action])})
        self.edges = (Edge("en", "source", "target", self.action), Edge("vi", "source", "target", self.action))

    def test_registry_includes_cham_without_implied_action_approval(self):
        cfg = ModelConfig(vocab_size=12, action_count=1)
        self.assertEqual(cfg.languages, ("vi", "en", "cham_phan_rang"))
        with self.assertRaises(ValueError):
            self.inventory.require("cham_phan_rang", self.action)

    def test_only_matching_licensed_edges_align(self):
        validate_pair(EdgePair(0, 1, "same_event"), self.edges, self.inventory)
        for relation in ("unknown", "scope_different"):
            with self.assertRaises(ValueError):
                validate_pair(EdgePair(0, 1, relation), self.edges, self.inventory)
        mismatched = (self.edges[0], Edge("vi", "different", "target", self.action))
        with self.assertRaises(ValueError):
            validate_pair(EdgePair(0, 1, "same_event"), mismatched, self.inventory)
        for left, right in ((True, False), (0.0, 1)):
            with self.subTest(indices=(left, right)), self.assertRaisesRegex(ValueError, "integers"):
                validate_pair(EdgePair(left, right, "same_event"), self.edges, self.inventory)

    def test_invalid_configuration(self):
        with self.assertRaises(ValueError):
            ModelConfig(vocab_size=12, action_count=1, width=7, heads=2)
        with self.assertRaises(ValueError):
            Inventory((self.action, self.action), {})

    def test_continuous_action_paths_and_cross_language_pairs_are_explicit(self):
        second = Action("TEST_KIND", "SECOND_VALUE")
        inventory = Inventory(
            (self.action, second),
            {
                "en": frozenset((self.action, second)),
                "vi": frozenset((self.action, second)),
            },
        )
        edges = (
            Edge("en", "frame-0", "frame-1", self.action),
            Edge("en", "frame-1", "frame-2", second),
            Edge("vi", "frame-0", "frame-1", self.action),
            Edge("vi", "frame-1", "frame-2", second),
            Edge("en", "unrelated-frame", "frame-3", second),
        )
        paths = (EdgePath((0, 1)), EdgePath((2, 3)))
        validate_path(paths[0], edges, inventory)
        validate_path_pair(PathPair(0, 1, "same_event"), paths, edges, inventory)

        with self.assertRaisesRegex(ValueError, "continuous"):
            validate_path(EdgePath((0, 4)), edges, inventory)
        with self.assertRaisesRegex(ValueError, "same_event"):
            validate_path_pair(PathPair(0, 1, "unknown"), paths, edges, inventory)
        mismatched = (paths[0], EdgePath((2, 1)))
        with self.assertRaises(ValueError):
            validate_path_pair(PathPair(0, 1, "same_event"), mismatched, edges, inventory)
        with self.assertRaises(ValueError):
            EdgePath((0, 0))

    def test_bos_must_be_an_integer_in_vocabulary_and_not_padding(self):
        self.assertEqual(ModelConfig(vocab_size=12, action_count=1, bos_id=7).bos_id, 7)
        for invalid_bos in (0, -1, 12, 1.0, True):
            with self.subTest(bos_id=invalid_bos), self.assertRaises(ValueError):
                ModelConfig(vocab_size=12, action_count=1, bos_id=invalid_bos)


if __name__ == "__main__":
    unittest.main()
