# Goals and Acceptance Criteria

## Product goal

Turn a short operational incident into a deterministic owner recommendation and review decision.

## Acceptance criteria

1. Every incident receives one owner from `security`, `data`, `platform`, or `operations`.
2. Critical incidents always require human review.
3. Text that attempts to alter system instructions requires human review.
4. Unknown or ambiguous incidents route to operations with human review.
5. Tests cover normal, critical, ambiguous, and adversarial cases.

## Non-goals

- automated remediation;
- production paging;
- model-based inference; and
- ingestion of real customer or employer data.

