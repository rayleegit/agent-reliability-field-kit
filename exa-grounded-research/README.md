# Grounded Research Release Gate

A compact, offline-first reference implementation for turning web-search results into inspectable research evidence. It demonstrates the layer around a search API: normalize results, prefer diverse sources, require claim-level citations, and stop unsupported answers before release.

The included scenario is fictional. It contains no client data, prompts, or architecture.

## Run it

```bash
python3 run_demo.py
python3 -m unittest discover -s test -v
```

No credentials or network access are required. `exa_adapter.py` shows the current Exa Search API request shape behind an explicit `EXA_API_KEY` requirement, but the demo and tests use deterministic local results.

## What the gate checks

- every claim has at least one valid citation;
- cited result IDs exist in the retrieved evidence;
- high-stakes reports use at least two source domains;
- no duplicate URL is counted twice;
- low-scoring evidence is excluded before synthesis.

This is deliberately not a full RAG framework. It is a small example of the reliability and evaluation layer that should surround a search-backed application.
