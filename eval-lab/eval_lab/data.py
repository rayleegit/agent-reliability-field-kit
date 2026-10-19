import json
from pathlib import Path
from typing import List

from .models import Case, Decision


def load_cases(path: Path) -> List[Case]:
    cases = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            record = json.loads(line)
            cases.append(
                Case(
                    case_id=record["case_id"],
                    text=record["text"],
                    expected=Decision(record["expected"]),
                    tags=frozenset(record.get("tags", [])),
                )
            )
    return cases

