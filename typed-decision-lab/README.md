# Typed Decision and Review Lab

A compact example of placing probabilistic, typed decisions inside ordinary software. A decision model classifies a fictional compliance case, reports confidence, and lets application code decide whether to act automatically or request human review.

The included records and model outputs are synthetic. They contain no client data, prompts, or architecture.

## Run it

```bash
python3 run_demo.py
python3 -m unittest discover -s test -v
```

No credentials or network access are required. `typesafe_adapter.py` documents an optional request to TypeSafe AI's System One endpoint behind `TYPESAFE_API_KEY`; the default path is deterministic and offline.

## What it demonstrates

- a fixed set of typed outcomes rather than free-form generated text;
- separate confidence and risk thresholds;
- automatic escalation for ambiguous or consequential cases;
- Brier score calculation over a small labeled calibration set;
- explicit, testable policy outside the model.

The goal is not to claim production readiness. It is to make the boundary between model judgment and application policy easy to inspect and discuss.
