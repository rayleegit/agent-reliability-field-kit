import unittest

from grounded_research import Claim, SearchResult, evaluate_release, select_evidence


class GroundedResearchTests(unittest.TestCase):
    def setUp(self):
        self.results = [
            SearchResult("a", "A", "https://a.example/one", "evidence a", 0.9),
            SearchResult("b", "B", "https://b.example/two", "evidence b", 0.8),
            SearchResult("dup", "A copy", "https://a.example/one/", "copy", 0.7),
            SearchResult("low", "Low", "https://c.example/three", "weak", 0.2),
        ]

    def test_selects_unique_high_quality_results(self):
        selected = select_evidence(self.results)
        self.assertEqual([item.id for item in selected], ["a", "b"])

    def test_passes_grounded_diverse_report(self):
        evidence = select_evidence(self.results)
        report = evaluate_release(
            [Claim("claim one", ["a"]), Claim("claim two", ["b"])], evidence
        )
        self.assertTrue(report.passed)
        self.assertEqual(report.citation_coverage, 1.0)

    def test_blocks_unsupported_claim(self):
        evidence = select_evidence(self.results)
        report = evaluate_release([Claim("unsupported", [])], evidence)
        self.assertFalse(report.passed)
        self.assertEqual(report.citation_coverage, 0.0)

    def test_blocks_unknown_citation(self):
        evidence = select_evidence(self.results)
        report = evaluate_release([Claim("claim", ["missing"])], evidence, minimum_domains=0)
        self.assertFalse(report.passed)
        self.assertIn("missing", report.invalid_citations)


if __name__ == "__main__":
    unittest.main()
