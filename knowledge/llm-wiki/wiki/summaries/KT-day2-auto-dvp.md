---
type: Summary
description: "Summarizes candidate AutoDVP receipt matching, closure predicates, exceptions, and evidence-retention gaps."
doc_type: short
full_text: sources/KT-day2-auto-dvp.md
---

> **Candidate/draft only:** The selected scenarios do not establish current scope, implementation, UAT, or approval. Owner is unknown; `verified` is empty.

# Day 2 AutoDVP receipt handling

The requirement covers EBBS debit notifications for external counterparties whose accounts are held at SCB. Internal-account-only notifications are out of scope, and the pilot heading and scenarios disagree on country count. Murex and Stella have separate product-taxonomy predicates. RTA currency and amount must match the RATAN receive cashflow. The source-specific date window runs from payment date through two business days later, inclusive; linkage uses trade ID, payment date, and a payment-type prefix, with major version added for Stella.

After a qualifying receipt, only a WAITING pay cashflow with a recognized DVP exception qualifies for closure. Netted-resultant and split-child receipt notifications are excluded, although one parent may close multiple eligible split pay children. Withdrawal events are ignored. Amended-linkage cases differ by whether trade identity changes.

The scenario describes receipt-before-pay handling and manual fallback but does not define persistence, deduplication, or replay. [[summaries/KT-settlement-cashflow-identity-and-stella-write-back]] separately records source-specific cashflow identity and status write-back questions; it does not resolve AutoDVP matching. These missing guarantees and the unresolved country scope prevent treating examples as a current contract.

## Canonical sections

- [EBBS receipt notification boundary](../../../records/candidates/settlement/KT-day2-auto-dvp.md#ebbs-receipt-notification-boundary)
- [Receive verification and pay linkage](../../../records/candidates/settlement/KT-day2-auto-dvp.md#receive-verification-and-pay-linkage)
- [Recognized DVP exceptions and closure](../../../records/candidates/settlement/KT-day2-auto-dvp.md#recognized-dvp-exceptions-and-closure)
- [Arrival order and operator fallback](../../../records/candidates/settlement/KT-day2-auto-dvp.md#arrival-order-and-operator-fallback)

## Related candidate topics

- [[summaries/KT-ratan-settlement-integration-checklist-scope]]

These links connect source-specific proposals. Their rules retain their separate scope and evidence limits.
