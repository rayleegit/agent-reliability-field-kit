# Circle Agent Spend Guard

A credential-free TypeScript/JavaScript teaching demo for the control plane around agentic payments. It models how an AI agent can discover services freely while every command that could move USDC is checked against deterministic policy and routed to a named human approver.

This project was inspired by Circle's open-source [Agent Stack Starter Kits](https://github.com/circlefin/agent-stack-starter-kits), which expose Circle CLI commands to agents and place an approval gate in front of money-moving commands.

## What it demonstrates

- separation between read-only discovery and money movement;
- allowlisted payment destinations;
- per-transaction and daily spending limits;
- explicit human approval for every in-policy payment;
- blocking rather than prompting when policy is violated; and
- an auditable receipt containing the command, amount, destination, and approver.

## Run

```bash
node demo.mjs
node --test test/policy.test.mjs
```

The demo is deterministic, offline, and requires no Circle account, wallet, API key, model provider, blockchain, or funds.

## Why this is useful

Agent commerce changes the failure mode of an AI application. A bad answer is no longer the only risk; the agent may attempt an irreversible external action. The guard therefore evaluates the exact proposed command before execution:

1. Read-only Circle commands can proceed.
2. Unknown destinations and policy-limit violations are blocked.
3. Valid money movement is paused and rendered as a concrete approval prompt.
4. Execution requires an affirmative decision tied to an approver identity.
5. The result is written as an inspectable receipt.

This mirrors the product principle described by Circle's starter kits: put the approval gate on the command, then enforce wallet-level limits as defense in depth.

## Production boundary

This is a policy simulator, not a wallet, payment service, or production Circle integration. It never invokes the Circle CLI and never signs or broadcasts a transaction. A production implementation should use Circle's supported CLI/SDK, verified wallet identity, durable policy and ledger storage, idempotency keys, transaction-status reconciliation, secrets management, and Circle's platform-level spending limits.

The example is educational only and should not be interpreted as financial advice or production security guidance.
