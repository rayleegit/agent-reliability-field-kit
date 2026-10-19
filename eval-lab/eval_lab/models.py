from dataclasses import dataclass
from enum import Enum
from typing import FrozenSet, Optional


class Decision(str, Enum):
    APPROVE = "approve"
    REVIEW = "review"
    DENY = "deny"


@dataclass(frozen=True)
class Case:
    case_id: str
    text: str
    expected: Decision
    tags: FrozenSet[str]

    @property
    def is_high_risk(self) -> bool:
        return "high_risk" in self.tags

    @property
    def is_adversarial(self) -> bool:
        return "adversarial" in self.tags


@dataclass(frozen=True)
class Prediction:
    decision: Decision
    confidence: float
    reason: str
    policy_signal: Optional[str] = None

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")

