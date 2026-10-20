"""Minimal optional TypeSafe AI adapter. The offline demo never calls it."""

import json
import os
from typing import Any, Dict
from urllib.request import Request, urlopen


SYSTEM_ONE_URL = "https://api.typesafe.ai/v1/systemone"


def decide(state: Dict[str, Any]) -> Dict[str, Any]:
    api_key = os.environ.get("TYPESAFE_API_KEY")
    if not api_key:
        raise RuntimeError("Set TYPESAFE_API_KEY to run the live adapter.")

    payload = {
        "model": "jev-latest",
        "state": state,
        "questions": {
            "route": {
                "type": "choice",
                "instructions": "Choose the next review route.",
                "criteria": {
                    "approve": "Evidence is complete and no material risk signal is present.",
                    "request_documents": "Required evidence is missing.",
                    "escalate": "A material conflict or risk signal requires specialist review.",
                },
            },
            "high_risk": {
                "type": "noul",
                "instructions": "Is there a material compliance-risk signal?",
            },
        },
    }
    request = Request(
        SYSTEM_ONE_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=20) as response:
        return json.load(response)
