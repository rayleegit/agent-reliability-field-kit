# Sample Evaluation Report

Generated locally on 2026-10-18 from 16 synthetic, fictional cases.

| Metric | Keyword baseline | Policy-aware version |
|---|---:|---:|
| Accuracy | 56.2% | 93.8% |
| Macro F1 | 56.2% | 93.3% |
| High-risk recall | 40.0% | 100.0% |
| Adversarial robustness | 50.0% | 100.0% |
| Human-review rate | 25.0% | 50.0% |
| Release gate | Fail | Pass |

## What changed

- Added explicit prohibited-risk policy signals.
- Added a review path for incomplete or conflicting evidence.
- Treated instructions inside submitted text as untrusted data.
- Evaluated high-risk and adversarial subsets separately from aggregate accuracy.

## Known failure

The policy-aware version incorrectly approves a request whose ownership change is pending verification because that phrasing is not represented in its review rules. The failure is intentionally retained to show the next iteration target instead of presenting a perfect synthetic result.

## Next experiment

Add paraphrase coverage for ownership changes, then compare three strategies:

1. extend deterministic policy rules;
2. use a structured model prediction with an explicit rubric; and
3. use retrieval over policy clauses with a calibrated human-review threshold.

The release decision should be based on the same held-out cases and should report any increase in review load.

