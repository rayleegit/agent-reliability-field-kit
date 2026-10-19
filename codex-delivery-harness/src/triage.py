import re
from dataclasses import dataclass
from typing import Literal


Owner = Literal["security", "data", "platform", "operations"]
Severity = Literal["low", "medium", "high", "critical"]


@dataclass(frozen=True)
class Incident:
    incident_id: str
    text: str
    severity: Severity


@dataclass(frozen=True)
class TriageResult:
    owner: Owner
    needs_human_review: bool
    reason: str


INJECTION_PATTERN = re.compile(
    r"ignore (?:all |the )?(?:previous|prior) instructions|"
    r"reveal (?:the )?system prompt|bypass (?:the )?(?:policy|review)",
    re.IGNORECASE,
)


def triage(incident: Incident) -> TriageResult:
    text = incident.text.lower()

    if INJECTION_PATTERN.search(text):
        return TriageResult(
            owner="security",
            needs_human_review=True,
            reason="untrusted text attempted to alter triage policy",
        )

    if any(term in text for term in ("credential", "token", "phishing", "unauthorized")):
        owner: Owner = "security"
    elif any(term in text for term in ("pipeline", "schema", "warehouse", "data quality")):
        owner = "data"
    elif any(term in text for term in ("latency", "deployment", "container", "outage")):
        owner = "platform"
    else:
        owner = "operations"

    ambiguous = owner == "operations"
    needs_review = incident.severity == "critical" or ambiguous
    reason = "critical severity" if incident.severity == "critical" else (
        "no specialized routing signal" if ambiguous else "matched routing signal"
    )
    return TriageResult(owner=owner, needs_human_review=needs_review, reason=reason)


def main() -> None:
    samples = [
        Incident("inc-01", "Warehouse schema mismatch blocked the pipeline", "high"),
        Incident("inc-02", "Unauthorized token use detected", "critical"),
        Incident("inc-03", "Customer reports an unclear workflow problem", "medium"),
    ]
    for incident in samples:
        print(incident.incident_id, triage(incident))


if __name__ == "__main__":
    main()

