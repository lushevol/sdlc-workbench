---
type: Summary
description: Compares the Day 2 and Korea migration designs for manual payment amount adjustments.
doc_type: short
full_text: sources/KT-settlement-payment-amount-adjustment.md
---

# Payment amount adjustment

This summary derives from version 3 of the candidate draft. [Canonical record](../../../records/candidates/settlement/KT-settlement-payment-amount-adjustment.md).

## Shared controls

Both designs keep the amount change below USD 1 equivalent and require maker/checker approval. The Day 2 design uses the upstream exchange rate. The applicable rate and timestamp need confirmation. [Canonical summary](../../../records/candidates/settlement/KT-settlement-payment-amount-adjustment.md#summary).

## Day 2 manual rounding

The Day 2 design allows changes in WAITING. SWIFT and accounting use the updated amount. The reconciliation team needs to confirm how TLM handles differences. [Day 2 design](../../../records/candidates/settlement/KT-settlement-payment-amount-adjustment.md#day-2-manual-rounding).

## Korea migration adjustment

The Korea design allows editing in specified WAITING and READY states before downstream release. It covers gross cashflows, net resultants, aggregation resultants, and split parents. It excludes all X-prefixed currencies and split resultants. Submission enters Pending Verification, and approval returns the cashflow to READY. SWIFT uses the adjusted amount. Settlement accounting uses the original amount. [Korea design](../../../records/candidates/settlement/KT-settlement-payment-amount-adjustment.md#korea-migration-adjustment).

## Open decisions

The rules for state eligibility and accounting differ between the sources. A Korea test scenario also contradicts the recorded split-parent answer. Confirm which design applies per payment flow, entity, and date. [Evidence limits](../../../records/candidates/settlement/KT-settlement-payment-amount-adjustment.md#evidence-limits).

## Related topics

- [[summaries/KT-settlement-auto-netting|Cash Settlement auto-netting]]
- [[summaries/KT-settlement-cashflow-identity-and-stella-write-back|Cashflow identity and Stella status write-back]]

## Korea state and inheritance boundaries

Only makers edit amounts. The eligible states are READY/NA/NA or WAITING/PendingOperator/PendingException without Pending NDS Netting. Backend validation checks currency, range, and decimal precision. Submission enters WAITING/PendingVerification/PendingException. Approval returns READY; rejection returns WAITING/PendingOperator/PendingException. Adjustment rejection and cancellation rejection retain different table-specific amount flags. [Maker/checker responsibility](../../../records/candidates/settlement/KT-settlement-payment-amount-adjustment.md#maker-checker-and-amount-responsibility). [Decision states](../../../records/candidates/settlement/KT-settlement-payment-amount-adjustment.md#korea-submission-and-decision-states).

An adjusted cashflow cannot net until its adjustment is removed. Returning the same cashflow to QUEUED preserves its adjustment. Economic replacement cashflows do not inherit it. Split adjustment requires unsplitting, changing the parent, then splitting again. The conflicting split-resultant test table has no recorded result. Repeated netting after reversal/rebooking does not inherit the prior resultant difference. [Adjustment boundary](../../../records/candidates/settlement/KT-settlement-payment-amount-adjustment.md#adjustment-scope-and-threshold). [Split and withdrawal limits](../../../records/candidates/settlement/KT-settlement-payment-amount-adjustment.md#split-and-withdrawal-contradiction).

The Korea variant uses adjusted amounts for payment and LMS while accounting keeps original amounts. It covers MT, MX, and Flip MT202. Its interface analysis lists FMSWG, ENISIS, and LMS. FXU remains outside this SWIFT change. LoanIQ amount amendment is excluded because RATAN does not feed LoanIQ payment amounts. Day 2 separately updates both SWIFT and accounting. Neither variant establishes precedence over the other. [Korea downstream scope](../../../records/candidates/settlement/KT-settlement-payment-amount-adjustment.md#korea-submission-and-decision-states). [Variant limits](../../../records/candidates/settlement/KT-settlement-payment-amount-adjustment.md#evidence-limits).
