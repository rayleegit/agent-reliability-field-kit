# Codex-Ready Delivery Harness

A tiny incident-triage project structured to make AI-assisted engineering reviewable. It separates durable repository guidance, product goals, phased work, reusable prompts, code, tests, and a verification log.

## Run

```bash
python3 -m unittest discover -s test -v
python3 scripts/verify.py
python3 -m src.triage
```

## What this demonstrates

- repository-specific instructions in `AGENTS.md`;
- explicit success conditions in `GOALS.md`;
- small human-reviewable phases in `PLANS.md`;
- reusable task prompts in `PROMPTS.md`;
- deterministic unit tests; and
- an append-only build log containing verification evidence.

The sample application classifies fictional operational incidents and routes low-confidence or high-severity items to human review. The implementation is intentionally small; the portfolio signal is the disciplined workflow around it.

