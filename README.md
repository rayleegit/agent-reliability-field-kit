# Agent Reliability Field Kit

A small, runnable portfolio showing how I approach production agent systems: define behavior before implementation, evaluate against representative edge cases, enforce least-privilege tool access, and leave an auditable delivery trail.

The examples use fictional vendor-risk and incident-response data. They do **not** contain client code, data, prompts, or architecture.

## What is included

| Demo | What it proves | Best conversation |
|---|---|---|
| [`eval-lab`](./eval-lab) | Golden sets, failure taxonomies, regression metrics, adversarial robustness, and human-review thresholds | Distyl, Appen, SafetyKit |
| [`identity-gateway`](./identity-gateway) | Audience, expiry, and scope enforcement for MCP-style tools, including an OAuth challenge | OpenAI Sign in with ChatGPT, 1Password |
| [`codex-delivery-harness`](./codex-delivery-harness) | A repeatable spec → implementation → test → review workflow for AI-assisted engineering | OpenAI Codex, OpenHands |
| [`exa-grounded-research`](./exa-grounded-research) | Search-result normalization, source diversity, claim-level citation checks, and release gates | Exa Developer Advocate |
| [`typed-decision-lab`](./typed-decision-lab) | Typed decisions, calibrated-confidence evaluation, and human-review routing | TypeSafe AI Developer Advocate |

## Five-minute tour

```bash
python3 verify_all.py
python3 scripts/security_audit.py
```

The commands run all five demos and their tests, then scan tracked files for common secrets and credential-bearing filenames. They run locally without credentials or network access.

## Design principles

1. **Behavior first.** Define representative cases and release criteria before optimizing prompts or models.
2. **Decision-relevant metrics.** Track high-risk recall and adversarial robustness in addition to aggregate accuracy.
3. **Human control.** Ambiguous or high-impact cases can be routed to review instead of forcing a confident answer.
4. **Least privilege.** Tool access is tied to explicit scopes, expected audience, and unexpired credentials.
5. **Reproducibility.** Every demo has deterministic tests and a short path from clone to evidence.

## Optional OpenAI integration

`eval-lab/openai_adapter.py` demonstrates the current Responses API shape behind an explicit environment flag. The default demo stays offline so a reviewer can reproduce it without an API key. The local evaluator is deliberately independent of any provider.

## Suggested review path

- Engineering lead: run the commands, then inspect the tests and failure taxonomy.
- Applied AI lead: start with `eval-lab/report.md` and `eval-lab/eval_lab/evaluator.py`.
- Identity/platform lead: inspect `identity-gateway/src/policy.mjs` and the challenge tests.
- Customer engineering lead: read [`SHARING_GUIDE.md`](./SHARING_GUIDE.md) for a 90-second walkthrough.

## Scope

This is a foundational portfolio project, not a production security product. The identity demo validates mock claims to make authorization behavior inspectable; production deployments should use an established identity provider and verified signed tokens.
