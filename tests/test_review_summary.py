import json
import unittest

from scripts.summarize_v433_human_review import (
    _nominal_kappa,
    _summarize,
    _validate_pair,
    _weighted_kappa,
)


def _fixture_forms():
    reviewer_a, reviewer_b = {}, {}
    for index in range(48):
        stratum = index // 12
        language = "en" if stratum in {0, 1} else "vi"
        task = "single" if stratum in {0, 2} else "held_out_path"
        identity = {
            "language": language,
            "task": task,
            "source_text": f"PRIVATE_SOURCE_{index}",
            "requested_actions": "[]",
            "expected_target_frame": "{}",
            "candidate_output": f"PRIVATE_CANDIDATE_{index}",
        }
        common = {
            "naturalness_1_to_5": "4",
            "meaning_preserved_yes_no_uncertain": "yes",
            "action_faithful_yes_no_uncertain": "yes",
            "confidence_high_medium_low": "high",
            "issues_or_notes": f"PRIVATE_NOTE_{index}",
        }
        case_id = f"C{index + 1:03d}"
        reviewer_a[case_id] = {"case_id": case_id, **identity, **common}
        reviewer_b[case_id] = {
            "case_id": case_id,
            **identity,
            **common,
            "naturalness_1_to_5": "5",
        }
    return reviewer_a, reviewer_b


class HumanReviewSummaryTests(unittest.TestCase):
    def test_agreement_coefficients_cover_perfect_and_disagreement(self):
        self.assertEqual(_nominal_kappa(["yes", "no", "yes", "no"], ["yes", "no", "yes", "no"]), 1.0)
        self.assertEqual(_weighted_kappa([1, 2, 4, 5], [1, 2, 4, 5]), 1.0)
        self.assertLess(_weighted_kappa([1, 2, 4, 5], [5, 4, 2, 1]), 0.0)
        self.assertIsNone(_nominal_kappa(["yes"] * 4, ["yes"] * 4))

    def test_aggregate_keeps_strata_and_omits_all_example_text_and_notes(self):
        reviewer_a, reviewer_b = _fixture_forms()
        _validate_pair((reviewer_a, reviewer_b))
        report = _summarize(reviewer_a, reviewer_b)
        encoded = json.dumps(report)
        self.assertEqual(report["scope"]["cases"], 48)
        self.assertEqual(set(report["scope"]["strata"].values()), {12})
        self.assertEqual(report["inter_rater_agreement"]["naturalness"]["exact_agreement_cases"], 0)
        self.assertNotIn("PRIVATE_SOURCE", encoded)
        self.assertNotIn("PRIVATE_CANDIDATE", encoded)
        self.assertNotIn("PRIVATE_NOTE", encoded)
        self.assertNotIn("source_text", encoded)
        self.assertNotIn("candidate_output", encoded)

    def test_pair_validation_rejects_changed_case_content(self):
        reviewer_a, reviewer_b = _fixture_forms()
        reviewer_b["C001"]["candidate_output"] = "altered"
        with self.assertRaisesRegex(ValueError, "differ in case content"):
            _validate_pair((reviewer_a, reviewer_b))

    def test_pair_validation_rejects_missing_ratings(self):
        reviewer_a, reviewer_b = _fixture_forms()
        reviewer_b["C048"]["action_faithful_yes_no_uncertain"] = ""
        with self.assertRaisesRegex(ValueError, "action ratings"):
            _validate_pair((reviewer_a, reviewer_b))


if __name__ == "__main__":
    unittest.main()
