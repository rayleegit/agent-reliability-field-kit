"""Minimal optional Exa adapter. The offline demo never calls this module."""

import json
import os
from typing import Any, Dict
from urllib.request import Request, urlopen


SEARCH_URL = "https://api.exa.ai/search"


def search(query: str, num_results: int = 8) -> Dict[str, Any]:
    api_key = os.environ.get("EXA_API_KEY")
    if not api_key:
        raise RuntimeError("Set EXA_API_KEY to run the live adapter.")

    payload = {
        "query": query,
        "type": "auto",
        "numResults": num_results,
        "contents": {"highlights": True},
    }
    request = Request(
        SEARCH_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"x-api-key": api_key, "Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=20) as response:
        return json.load(response)
