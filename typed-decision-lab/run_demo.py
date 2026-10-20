from typed_decisions import TypedDecision, apply_policy, brier_score


def main() -> None:
    cases = [
        ("complete", TypedDecision("approve", 0.91, 0.08)),
        ("ambiguous", TypedDecision("request_documents", 0.61, 0.22)),
        ("high-risk", TypedDecision("escalate", 0.88, 0.79)),
    ]
    for case_id, decision in cases:
        outcome = apply_policy(decision)
        print(f"{case_id}: decision={decision.route} action={outcome.action}")

    score = brier_score([0.10, 0.80, 0.65, 0.25], [0, 1, 1, 0])
    print(f"calibration_brier_score={score:.4f}")


if __name__ == "__main__":
    main()
