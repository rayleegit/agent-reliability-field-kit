"""Small, dependency-free GraphRAG teaching example.

The in-memory graph keeps the workshop reproducible. The query plan mirrors what
would normally be expressed in Cypher: select seed nodes, expand typed
relationships, enforce access policy, then return source-backed context.
"""

from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence, Set, Tuple


@dataclass(frozen=True)
class Node:
    node_id: str
    label: str
    text: str
    source: str
    access: str = "public"


@dataclass(frozen=True)
class Edge:
    source: str
    relationship: str
    target: str


@dataclass(frozen=True)
class Evidence:
    node_id: str
    path: str
    text: str
    source: str


class StartupGraph:
    def __init__(self, nodes: Sequence[Node], edges: Sequence[Edge]) -> None:
        self.nodes: Dict[str, Node] = {node.node_id: node for node in nodes}
        self.edges = list(edges)

    @staticmethod
    def _tokens(text: str) -> Set[str]:
        return {
            token.strip(".,:;!?()[]{}").lower()
            for token in text.split()
            if len(token.strip(".,:;!?()[]{}")) > 2
        }

    def _visible(self, node: Node, allowed_access: Set[str]) -> bool:
        return node.access in allowed_access

    def seed_nodes(self, question: str, allowed_access: Set[str]) -> List[Node]:
        query_tokens = self._tokens(question)
        ranked: List[Tuple[int, Node]] = []
        for node in self.nodes.values():
            if not self._visible(node, allowed_access):
                continue
            score = len(query_tokens & self._tokens(f"{node.label} {node.text}"))
            if score:
                ranked.append((score, node))
        return [node for _, node in sorted(ranked, key=lambda item: (-item[0], item[1].node_id))]

    def retrieve(
        self,
        question: str,
        allowed_access: Iterable[str] = ("public",),
        max_evidence: int = 6,
    ) -> List[Evidence]:
        allowed = set(allowed_access)
        seeds = self.seed_nodes(question, allowed)
        evidence: Dict[str, Evidence] = {}

        for seed in seeds:
            evidence[seed.node_id] = Evidence(
                node_id=seed.node_id,
                path=seed.node_id,
                text=seed.text,
                source=seed.source,
            )
            for edge in self.edges:
                if edge.source != seed.node_id:
                    continue
                neighbor = self.nodes[edge.target]
                if not self._visible(neighbor, allowed):
                    continue
                evidence.setdefault(
                    neighbor.node_id,
                    Evidence(
                        node_id=neighbor.node_id,
                        path=f"{seed.node_id}-[{edge.relationship}]->{neighbor.node_id}",
                        text=neighbor.text,
                        source=neighbor.source,
                    ),
                )
        return list(evidence.values())[:max_evidence]


def evaluate(question: str, evidence: Sequence[Evidence]) -> Dict[str, object]:
    unique_sources = {item.source for item in evidence}
    linked_items = [item for item in evidence if "-[" in item.path]
    passed = bool(evidence) and bool(linked_items) and len(unique_sources) >= 2
    return {
        "question": question,
        "evidence_count": len(evidence),
        "unique_sources": len(unique_sources),
        "linked_context": len(linked_items),
        "release_decision": "PASS" if passed else "REVIEW",
    }


def demo_graph() -> StartupGraph:
    nodes = [
        Node("company_acme", "Company", "Acme builds compliance agents for regulated teams.", "company-profile"),
        Node("founder_maya", "Founder", "Maya leads Acme and participates in Bay Area founder programs.", "founder-interview"),
        Node("need_eval", "Need", "Acme needs measurable evaluation and human review before deployment.", "discovery-notes"),
        Node("tech_graph", "Technology", "GraphRAG connects policies, controls, documents, and evidence.", "technical-brief"),
        Node("program_demo", "Program", "A workshop can move developers from graph model to grounded answer.", "program-outline"),
        Node("private_budget", "Finance", "Confidential budget details.", "internal-finance", access="internal"),
    ]
    edges = [
        Edge("company_acme", "LED_BY", "founder_maya"),
        Edge("company_acme", "HAS_NEED", "need_eval"),
        Edge("need_eval", "SUPPORTED_BY", "tech_graph"),
        Edge("tech_graph", "TAUGHT_IN", "program_demo"),
        Edge("company_acme", "HAS_BUDGET", "private_budget"),
    ]
    return StartupGraph(nodes, edges)
