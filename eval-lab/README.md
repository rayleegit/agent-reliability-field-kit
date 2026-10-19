# Evaluation-Driven Agent Lab

This demo evaluates a fictional vendor-risk intake agent. It compares a deliberately weak baseline with a policy-aware classifier that can route ambiguous cases to human review.

## Run

```bash
python3 run_demo.py
python3 -m unittest discover -s test -v
```

The demo reports:

- accuracy;
- macro F1;
- high-risk recall;
- adversarial robustness;
- human-review rate; and
- a release-gate decision.

## Why these metrics

Aggregate accuracy can hide expensive mistakes. A risk workflow needs asymmetric measures: missing a prohibited transfer matters more than reviewing an ambiguous low-risk request. The release gate therefore requires both overall quality and a minimum high-risk recall.

## Optional model adapter

The default run is deterministic and offline. To exercise an OpenAI model, install the SDK, set `OPENAI_API_KEY`, and call `OpenAIClassifier` from `openai_adapter.py`. The adapter uses the Responses API and returns the same `Prediction` contract as the local classifiers.

The evaluation system remains provider-independent; switching the inference implementation does not change the golden set, metrics, or release criteria.

