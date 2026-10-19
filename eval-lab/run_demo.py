import json
from pathlib import Path

from eval_lab.classifiers import BaselineClassifier, PolicyAwareClassifier
from eval_lab.data import load_cases
from eval_lab.evaluator import evaluate


def _percent(value: float) -> str:
    return f"{value * 100:5.1f}%"


def main() -> None:
    root = Path(__file__).resolve().parent
    cases = load_cases(root / "data" / "cases.jsonl")
    reports = {
        "baseline": evaluate(BaselineClassifier(), cases),
        "policy_aware": evaluate(PolicyAwareClassifier(), cases),
    }

    print("Agent evaluation: fictional vendor-risk intake")
    print("=" * 55)
    for name, report in reports.items():
        print(f"\n{name.replace('_', ' ').title()}")
        print(f"  accuracy:               {_percent(report.accuracy)}")
        print(f"  macro F1:               {_percent(report.macro_f1)}")
        print(f"  high-risk recall:       {_percent(report.high_risk_recall)}")
        print(f"  adversarial robustness: {_percent(report.adversarial_robustness)}")
        print(f"  review rate:            {_percent(report.review_rate)}")
        print(f"  release ready:          {report.release_ready}")
        print(f"  failures:               {len(report.failures)}")

    output = {name: report.to_dict() for name, report in reports.items()}
    (root / "report.json").write_text(json.dumps(output, indent=2) + "\n")
    print("\nWrote report.json")


if __name__ == "__main__":
    main()

