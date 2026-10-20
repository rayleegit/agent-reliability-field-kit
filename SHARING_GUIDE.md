# Sharing Guide

## 90-second walkthrough

> I built this field kit to make my approach to production agents inspectable without exposing confidential client systems. The evaluation lab starts with a golden set, measures a simple baseline, then adds explicit policy logic, adversarial defenses, and a human-review path. The identity gateway shows how I gate tools by audience, expiry, and least-privilege scopes. The grounded-research demo checks source diversity and claim-level citations, while the typed-decision lab separates probabilistic judgment from application policy. Everything runs locally without credentials, and optional provider adapters remain separate from deterministic evaluation.

## Lead-specific hooks

### Distyl

The strongest artifact is the evaluation lab: golden cases, a failure taxonomy, high-risk recall, adversarial robustness, and release gates. Ask which additional signal would make the case more representative of their evaluation-driven development practice.

### Appen

Focus on acceptance criteria, validation automation, reproducibility, and the separation between data quality and model behavior. Ask how their FDEs adjudicate ambiguous labels with client experts.

### SafetyKit

Focus on adversarial cases, instruction-injection resistance, asymmetric error costs, and human review. Ask which abuse or policy domain would be most useful for a second dataset.

### OpenAI — Sign in with ChatGPT

Focus on the identity gateway: resource audience, scopes, expiry, stable identity, and the challenge path. Be explicit that the project is an authorization-policy simulator, not a home-grown identity provider.

### OpenAI — Codex

Focus on the delivery harness: repository instructions, acceptance criteria, small phases, deterministic verification, and a build log. Pair it with a live code change during the conversation.

### Exa

Focus on the grounded-research demo: normalize search results, remove duplicate URLs, require claim-level citations, enforce source diversity, and block unsupported reports. Explain that the included Exa adapter follows the current Search API shape while the evaluation path stays deterministic and credential-free. Ask how Exa's DevRel team measures whether an example teaches developers good retrieval habits rather than only producing an impressive demo.

### TypeSafe AI

Focus on the typed-decision lab: fixed outcomes, explicit confidence and risk thresholds, Brier score calculation, and human-review routing. Explain that the application owns the consequential policy decision; the model supplies typed probabilistic judgment. Ask which real developer workflow would be most useful as a second Jev example.

## Short outreach line

> I built a small, confidential-safe field kit showing how I evaluate agent behavior, enforce scoped tool access, and structure repeatable AI-assisted delivery. It is intentionally small enough to inspect in one sitting and runs without credentials. I’d value your feedback on which part is most representative of the work your team needs.

