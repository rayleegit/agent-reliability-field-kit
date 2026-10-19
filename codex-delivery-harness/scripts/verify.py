from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "AGENTS.md",
    "GOALS.md",
    "PLANS.md",
    "PROMPTS.md",
    "src/triage.py",
    "test/test_triage.py",
    "harness/build-log.md",
]


def main() -> None:
    missing = [relative for relative in REQUIRED if not (ROOT / relative).is_file()]
    if missing:
        raise SystemExit(f"Missing required harness files: {', '.join(missing)}")

    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    goals = (ROOT / "GOALS.md").read_text(encoding="utf-8")
    if "untrusted data" not in agents:
        raise SystemExit("AGENTS.md must preserve the untrusted-data boundary")
    if "Critical incidents always require human review" not in goals:
        raise SystemExit("GOALS.md must preserve the critical-review acceptance criterion")

    print(f"Harness verification passed: {len(REQUIRED)} required files present")


if __name__ == "__main__":
    main()

