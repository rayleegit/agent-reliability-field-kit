# Sharing Guide

## 90-second walkthrough

> I built this field kit to make my approach to production agents inspectable without exposing confidential client systems. The evaluation lab starts with a golden set, measures a simple baseline, then adds explicit policy logic, adversarial defenses, and a human-review path. The identity gateway shows how I gate MCP-style tools by audience, expiry, and least-privilege scopes. The Codex harness shows how I structure AI-assisted engineering so requirements, tests, and review evidence remain traceable. Everything runs locally without credentials, and the optional model adapter is separated from the evaluator so the quality system is provider-independent.

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

## Short outreach line

> I built a small, confidential-safe field kit showing how I evaluate agent behavior, enforce scoped tool access, and structure repeatable AI-assisted delivery. It is intentionally small enough to inspect in one sitting and runs without credentials. I’d value your feedback on which part is most representative of the work your team needs.

