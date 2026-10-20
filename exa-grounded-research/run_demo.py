from grounded_research import Claim, SearchResult, evaluate_release, select_evidence


RESULTS = [
    SearchResult(
        "regulator",
        "Fictional regulator guidance",
        "https://regulator.example/guidance",
        "Organizations should document review thresholds for consequential automated decisions.",
        0.94,
    ),
    SearchResult(
        "standard",
        "Fictional assurance standard",
        "https://standards.example/assurance",
        "Evaluation records should include failures, overrides, and the evidence used for release.",
        0.89,
    ),
    SearchResult(
        "vendor",
        "Fictional vendor announcement",
        "https://vendor.example/product",
        "The product supports configurable human review.",
        0.72,
    ),
]


def main() -> None:
    evidence = select_evidence(RESULTS)
    claims = [
        Claim("Consequential automation should use documented review thresholds.", ["regulator"]),
        Claim("Release records should preserve failures and evidence.", ["standard"]),
    ]
    report = evaluate_release(claims, evidence)
    print(f"evidence={len(evidence)} domains={report.source_domains}")
    print(f"citation_coverage={report.citation_coverage:.0%}")
    print("release=PASS" if report.passed else "release=BLOCK")


if __name__ == "__main__":
    main()
