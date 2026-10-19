# Delivery Plan

## Phase 1 — Contract and fixtures

- Define immutable input and output types.
- Write acceptance tests for representative incidents.

Exit: tests express every acceptance criterion.

## Phase 2 — Safe routing

- Implement deterministic routing.
- Detect instruction-injection language.
- Route critical and ambiguous cases to review.

Exit: unit tests pass.

## Phase 3 — Verification evidence

- Add repository verifier.
- Record commands and observed results in `harness/build-log.md`.

Exit: verifier reports success and the log contains reproducible evidence.

