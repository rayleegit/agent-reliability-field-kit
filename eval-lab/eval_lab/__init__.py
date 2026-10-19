"""Small, provider-independent evaluation harness for agent decisions."""

from .classifiers import BaselineClassifier, PolicyAwareClassifier
from .evaluator import EvaluationReport, evaluate
from .models import Case, Decision, Prediction

__all__ = [
    "BaselineClassifier",
    "PolicyAwareClassifier",
    "EvaluationReport",
    "evaluate",
    "Case",
    "Decision",
    "Prediction",
]

