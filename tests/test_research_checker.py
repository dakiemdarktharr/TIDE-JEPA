"""Checker regression fixtures constructed from registered train families only."""

import unittest

from tide_jepa.pilot import _semantic_frame_flags
from tide_jepa.pilot_seed import FAMILIES_V422, FAMILIES_V423, FAMILIES_V430


class ProgressiveCheckerTests(unittest.TestCase):
    def fixture(self, families, negative=False, declared=False):
        event, _, _, _, _, _, agent, verb, patient = families["train"][0]
        phrase = "đang " + ("không " if negative else "") + verb
        frame = {"event": event, "time": "present", "polarity": "negative" if negative else "positive",
                 "place_vi": "trong xưởng"}
        if declared:
            frame["predicate_vi_present"] = phrase
        text = f"{agent} {phrase} {patient} bây giờ, trong xưởng."
        return frame, text

    def test_v430_legacy_annotations_require_progressive_for_both_polarities(self):
        for negative in (False, True):
            frame, text = self.fixture(FAMILIES_V430, negative)
            flags = _semantic_frame_flags(text, "vi", frame)
            self.assertTrue(flags["action_fidelity"] and flags["preservation"])
            changed = _semantic_frame_flags(text.replace("đang ", ""), "vi", frame)
            self.assertFalse(changed["action_fidelity"])
            self.assertFalse(changed["predicate_preserved"])
            self.assertFalse(changed["preservation"])

    def test_explicit_present_form_does_not_depend_on_version_prefix(self):
        for negative in (False, True):
            frame, text = self.fixture(FAMILIES_V422, negative, declared=True)
            flags = _semantic_frame_flags(text, "vi", frame)
            self.assertTrue(flags["action_fidelity"] and flags["preservation"])
            changed = _semantic_frame_flags(text.replace("đang ", ""), "vi", frame)
            self.assertFalse(changed["action_fidelity"] or changed["preservation"])

    def test_v423_legacy_nonprogressive_negative_remains_valid(self):
        frame, text = self.fixture(FAMILIES_V423, negative=True)
        flags = _semantic_frame_flags(text.replace("đang ", ""), "vi", frame)
        self.assertTrue(flags["action_fidelity"] and flags["preservation"])


if __name__ == "__main__":
    unittest.main()
