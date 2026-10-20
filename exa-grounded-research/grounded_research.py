from dataclasses import dataclass
from typing import Iterable, List, Sequence
from urllib.parse import urlparse


@dataclass(frozen=True)
class SearchResult:
    id: str
    title: str
    url: str
    highlight: str
    score: float

    @property
    def domain(self) -> str:
        return urlparse(self.url).netloc.lower()


@dataclass(frozen=True)
class Claim:
    text: str
    citation_ids: Sequence[str]


@dataclass(frozen=True)
class GateReport:
    passed: bool
    citation_coverage: float
    source_domains: int
    invalid_citations: Sequence[str]
    reasons: Sequence[str]


def select_evidence(
    results: Iterable[SearchResult], minimum_score: float = 0.65, limit: int = 5
) -> List[SearchResult]:
    """Keep strong, unique, well-formed results in deterministic rank order."""
    selected: List[SearchResult] = []
    seen_urls = set()
    ranked = sorted(results, key=lambda item: (-item.score, item.url))
    for result in ranked:
        if result.score < minimum_score or not result.domain or not result.highlight.strip():
            continue
        normalized_url = result.url.rstrip("/")
        if normalized_url in seen_urls:
            continue
        seen_urls.add(normalized_url)
        selected.append(result)
        if len(selected) == limit:
            break
    return selected


def evaluate_release(
    claims: Sequence[Claim], evidence: Sequence[SearchResult], minimum_domains: int = 2
) -> GateReport:
    evidence_ids = {item.id for item in evidence}
    cited_claims = 0
    invalid = []
    cited_domains = set()

    for claim in claims:
        valid_ids = [citation for citation in claim.citation_ids if citation in evidence_ids]
        invalid.extend(
            citation for citation in claim.citation_ids if citation not in evidence_ids
        )
        if valid_ids:
            cited_claims += 1
            for result in evidence:
                if result.id in valid_ids:
                    cited_domains.add(result.domain)

    coverage = cited_claims / len(claims) if claims else 0.0
    reasons = []
    if coverage < 1.0:
        reasons.append("Every released claim must cite retrieved evidence.")
    if invalid:
        reasons.append("One or more citations do not resolve to retrieved evidence.")
    if len(cited_domains) < minimum_domains:
        reasons.append(f"At least {minimum_domains} independent source domains are required.")

    return GateReport(
        passed=not reasons,
        citation_coverage=coverage,
        source_domains=len(cited_domains),
        invalid_citations=tuple(sorted(set(invalid))),
        reasons=tuple(reasons),
    )
