---
type: Summary
description: "Captures proposed FMRP manual and threshold-based cashflow splitting controls, with unresolved scope and lifecycle outcomes."
doc_type: short
full_text: sources/KT-day2-cashflow-splitting.md
---

> **Candidate/draft only:** Split rules and test rows remain proposals; no current permission or executed result is established.

# Cashflow Splitting and Threshold Distribution

The dated requirement limits manual splitting to FMRP flows, with New events in WAITING or READY and no netting or splitting ID, with non-LOANIQ source. PROJECTED eligibility is struck through. Generic and IRS resultant scope conflicts across dated requirement and test rows.

Manual split starts from the original amount. Each entered amount must be positive and below the available balance at currency precision; the remainder becomes another child. A parent becomes SPLIT, and children return to the workflow with Split Cashflow. Amendment permits changing amounts for at least two WAITING children but not adding or deleting children. Unsplit eligibility and withdrawal outcomes differ between the main rule and demo cases.

Threshold static is maker-checker maintained. Proposed matching prefers currency, entity, then Nostro agent; qualifying payments split before Swift generation and each child generates its own Swift/accounting. The distribution algorithm relies on unavailable images, and a later TechFail proposal lacks its exact result/comment. Confirm the static action contract, child reversal treatment, and supported scope before reuse.

See [[concepts/cashflow-netting-grouping-and-outcomes]] for the distinct auto-netting grouping topic.

## Canonical sections

- [Scope and manual eligibility](../../../records/candidates/settlement/KT-day2-cashflow-splitting.md#scope-and-manual-eligibility)
- [Manual amounts and confirmation](../../../records/candidates/settlement/KT-day2-cashflow-splitting.md#manual-amounts-and-confirmation)
- [Amendment and unsplit](../../../records/candidates/settlement/KT-day2-cashflow-splitting.md#amendment-and-unsplit)
- [Withdrawal conflicts](../../../records/candidates/settlement/KT-day2-cashflow-splitting.md#withdrawal-conflicts)
- [Threshold static and distribution](../../../records/candidates/settlement/KT-day2-cashflow-splitting.md#threshold-static-and-distribution)
- [Failure and rule controls](../../../records/candidates/settlement/KT-day2-cashflow-splitting.md#failure-and-rule-controls)


## Related candidate topics

- [[summaries/KT-settlement-hold-and-manual-fail]]

These links connect source-specific proposals. Their rules retain their separate scope and evidence limits.
