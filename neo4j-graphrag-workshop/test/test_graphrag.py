import unittest

from graphrag import demo_graph, evaluate


class GraphRAGWorkshopTests(unittest.TestCase):
    def test_retrieval_expands_typed_relationships(self) -> None:
        evidence = demo_graph().retrieve("compliance agents evaluation")
        self.assertTrue(any("-[" in item.path and "]->" in item.path for item in evidence))

    def test_public_query_excludes_internal_nodes(self) -> None:
        evidence = demo_graph().retrieve("Acme budget compliance")
        self.assertNotIn("private_budget", {item.node_id for item in evidence})

    def test_authorized_query_can_include_internal_nodes(self) -> None:
        evidence = demo_graph().retrieve(
            "Acme budget compliance", allowed_access=("public", "internal")
        )
        self.assertIn("private_budget", {item.node_id for item in evidence})

    def test_evaluation_requires_linked_multi_source_context(self) -> None:
        evidence = demo_graph().retrieve("compliance agents evaluation")
        self.assertEqual("PASS", evaluate("question", evidence)["release_decision"])


if __name__ == "__main__":
    unittest.main()
