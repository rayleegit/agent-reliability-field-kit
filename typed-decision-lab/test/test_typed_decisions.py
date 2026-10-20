import unittest

from typed_decisions import TypedDecision, apply_policy, brier_score


class TypedDecisionTests(unittest.TestCase):
    def test_high_confidence_low_risk_decision_can_automate(self):
        outcome = apply_policy(TypedDecision("approve", 0.91, 0.08))
        self.assertEqual(outcome.action, "approve")

    def test_low_confidence_routes_to_review(self):
        outcome = apply_policy(TypedDecision("request_documents", 0.61, 0.20))
        self.assertEqual(outcome.action, "human_review")

    def test_high_risk_routes_to_review(self):
        outcome = apply_policy(TypedDecision("escalate", 0.93, 0.78))
        self.assertEqual(outcome.action, "human_review")

    def test_invalid_type_is_rejected(self):
        with self.assertRaises(ValueError):
            TypedDecision("free_form_answer", 0.9, 0.1)

    def test_brier_score(self):
        self.assertAlmostEqual(brier_score([0.1, 0.8], [0, 1]), 0.025)


if __name__ == "__main__":
    unittest.main()
