from dataclasses import dataclass
from typing import Iterable, Sequence


ALLOWED_ROUTES = {"approve", "request_documents", "escalate"}


@dataclass(frozen=True)
class TypedDecision:
    route: str
    route_probability: float
    high_risk_probability: float

    def __post_init__(self) -> None:
        if self.route not in ALLOWED_ROUTES:
            raise ValueError(f"Unsupported route: {self.route}")
        for value in (self.route_probability, self.high_risk_probability):
            if not 0.0 <= value <= 1.0:
                raise ValueError("Probabilities must be between 0 and 1.")


@dataclass(frozen=True)
class PolicyOutcome:
    action: str
    reason: str


def apply_policy(
    decision: TypedDecision,
    minimum_confidence: float = 0.80,
    high_risk_threshold: float = 0.65,
) -> PolicyOutcome:
    if decision.high_risk_probability >= high_risk_threshold:
        return PolicyOutcome("human_review", "High-risk probability crossed the review threshold.")
    if decision.route_probability < minimum_confidence:
        return PolicyOutcome("human_review", "Route confidence is below the automation threshold.")
    return PolicyOutcome(decision.route, "Typed decision satisfied both policy thresholds.")


def brier_score(probabilities: Iterable[float], labels: Iterable[int]) -> float:
    pairs: Sequence[tuple[float, int]] = tuple(zip(probabilities, labels))
    if not pairs:
        raise ValueError("At least one prediction and label are required.")
    for probability, label in pairs:
        if not 0.0 <= probability <= 1.0 or label not in (0, 1):
            raise ValueError("Probabilities must be in [0, 1] and labels must be binary.")
    return sum((probability - label) ** 2 for probability, label in pairs) / len(pairs)
