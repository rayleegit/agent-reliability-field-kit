"""Fail fast when tracked project files contain common secret patterns."""

import re
import subprocess
from pathlib import Path
from typing import List, Tuple


ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_NAMES = {
    ".env",
    ".env.local",
    ".env.production",
    "credentials.json",
    "service-account.json",
}
FORBIDDEN_SUFFIXES = {".pem", ".key", ".p12", ".pfx"}
PATTERNS = {
    "OpenAI-style secret key": re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"),
    "GitHub personal token": re.compile(r"\b(?:ghp|github_pat)_[A-Za-z0-9_]{20,}\b"),
    "AWS access key": re.compile(r"\bAKIA[A-Z0-9]{16}\b"),
    "private key material": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "assigned secret value": re.compile(
        r"(?i)\b(?:api[_-]?key|client[_-]?secret|access[_-]?token|refresh[_-]?token|password)"
        r"\s*[:=]\s*['\"][^'\"\s]{8,}['\"]"
    ),
}


def tracked_files() -> List[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=str(ROOT),
        check=True,
        capture_output=True,
    )
    return [ROOT / item.decode() for item in result.stdout.split(b"\0") if item]


def audit() -> List[Tuple[str, str]]:
    findings: List[Tuple[str, str]] = []
    for path in tracked_files():
        relative = path.relative_to(ROOT).as_posix()
        if path.name in FORBIDDEN_NAMES or path.suffix.lower() in FORBIDDEN_SUFFIXES:
            findings.append((relative, "credential-bearing filename"))
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            findings.append((relative, "unexpected binary tracked file"))
            continue
        for label, pattern in PATTERNS.items():
            if pattern.search(text):
                findings.append((relative, label))
    return findings


def main() -> None:
    findings = audit()
    if findings:
        for path, reason in findings:
            print(f"SECURITY AUDIT FAILED: {path}: {reason}")
        raise SystemExit(1)
    print("Security audit passed: no common secrets or credential files found")


if __name__ == "__main__":
    main()

