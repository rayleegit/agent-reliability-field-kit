import re
from typing import Protocol

from .models import Case, Decision, Prediction


class Classifier(Protocol):
    def predict(self, case: Case) -> Prediction:
        ...


class BaselineClassifier:
    """Intentionally weak keyword baseline used to expose failure modes."""

    def predict(self, case: Case) -> Prediction:
        text = case.text.lower()
        if "prohibited" in text or "sanctioned" in text:
            return Prediction(Decision.DENY, 0.82, "matched a denial keyword")
        if "missing" in text or "unknown" in text:
            return Prediction(Decision.REVIEW, 0.65, "matched an ambiguity keyword")
        return Prediction(Decision.APPROVE, 0.72, "no baseline risk keyword matched")


class PolicyAwareClassifier:
    """Deterministic policy layer with injection handling and review routing."""

    _injection = re.compile(
        r"ignore (?:all |the )?(?:previous|prior) instructions|system prompt|"
        r"mark (?:this|it) approved|bypass (?:the )?(?:policy|review)",
        re.IGNORECASE,
    )
    _deny_signals = {
        "sanctioned jurisdiction": "POL-01",
        "prohibited transfer": "POL-02",
        "stolen credentials": "POL-03",
        "weapons procurement": "POL-04",
    }
    _review_signals = {
        "beneficial owner unknown": "REV-01",
        "missing tax id": "REV-02",
        "conflicting address": "REV-03",
        "unverified subcontractor": "REV-04",
    }

    def predict(self, case: Case) -> Prediction:
        text = case.text.lower()

        if self._injection.search(text):
            return Prediction(
                Decision.REVIEW,
                0.99,
                "untrusted text attempted to alter decision policy",
                "SAFE-01",
            )

        for phrase, policy_id in self._deny_signals.items():
            if phrase in text:
                return Prediction(
                    Decision.DENY,
                    0.97,
                    "explicit prohibited-risk signal",
                    policy_id,
                )

        matched_review = [
            (phrase, policy_id)
            for phrase, policy_id in self._review_signals.items()
            if phrase in text
        ]
        if matched_review:
            _, policy_id = matched_review[0]
            return Prediction(
                Decision.REVIEW,
                0.90,
                "insufficient or conflicting evidence",
                policy_id,
            )

        return Prediction(
            Decision.APPROVE,
            0.88,
            "required low-risk evidence is present",
            "POL-00",
        )

