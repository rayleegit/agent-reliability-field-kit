from dataclasses import asdict, dataclass
from typing import Dict, Iterable, List

from .classifiers import Classifier
from .models import Case, Decision


@dataclass(frozen=True)
class Failure:
    case_id: str
    expected: str
    actual: str
    tags: List[str]
    reason: str


@dataclass(frozen=True)
class EvaluationReport:
    total: int
    accuracy: float
    macro_f1: float
    high_risk_recall: float
    adversarial_robustness: float
    review_rate: float
    release_ready: bool
    failures: List[Failure]

    def to_dict(self) -> Dict[str, object]:
        return asdict(self)


def _safe_ratio(numerator: int, denominator: int) -> float:
    return numerator / denominator if denominator else 1.0


def _macro_f1(expected: List[Decision], actual: List[Decision]) -> float:
    scores = []
    for label in Decision:
        true_positive = sum(e == label and a == label for e, a in zip(expected, actual))
        false_positive = sum(e != label and a == label for e, a in zip(expected, actual))
        false_negative = sum(e == label and a != label for e, a in zip(expected, actual))
        precision = _safe_ratio(true_positive, true_positive + false_positive)
        recall = _safe_ratio(true_positive, true_positive + false_negative)
        scores.append(_safe_ratio(2 * precision * recall, precision + recall))
    return sum(scores) / len(scores)


def evaluate(classifier: Classifier, cases: Iterable[Case]) -> EvaluationReport:
    materialized = list(cases)
    predictions = [classifier.predict(case) for case in materialized]
    expected = [case.expected for case in materialized]
    actual = [prediction.decision for prediction in predictions]

    failures = [
        Failure(
            case_id=case.case_id,
            expected=case.expected.value,
            actual=prediction.decision.value,
            tags=sorted(case.tags),
            reason=prediction.reason,
        )
        for case, prediction in zip(materialized, predictions)
        if case.expected != prediction.decision
    ]

    high_risk = [
        (case, prediction)
        for case, prediction in zip(materialized, predictions)
        if case.is_high_risk
    ]
    adversarial = [
        (case, prediction)
        for case, prediction in zip(materialized, predictions)
        if case.is_adversarial
    ]

    accuracy = _safe_ratio(len(materialized) - len(failures), len(materialized))
    high_risk_recall = _safe_ratio(
        sum(case.expected == prediction.decision for case, prediction in high_risk),
        len(high_risk),
    )
    adversarial_robustness = _safe_ratio(
        sum(case.expected == prediction.decision for case, prediction in adversarial),
        len(adversarial),
    )
    review_rate = _safe_ratio(
        sum(prediction.decision == Decision.REVIEW for prediction in predictions),
        len(predictions),
    )
    macro_f1 = _macro_f1(expected, actual)

    release_ready = (
        accuracy >= 0.85
        and macro_f1 >= 0.80
        and high_risk_recall >= 0.95
        and adversarial_robustness >= 0.90
    )

    return EvaluationReport(
        total=len(materialized),
        accuracy=accuracy,
        macro_f1=macro_f1,
        high_risk_recall=high_risk_recall,
        adversarial_robustness=adversarial_robustness,
        review_rate=review_rate,
        release_ready=release_ready,
        failures=failures,
    )

