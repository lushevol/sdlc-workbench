---
type: Summary
description: Compares the Day 2 and Korea migration designs for manual payment amount adjustments.
doc_type: short
full_text: sources/KT-settlement-payment-amount-adjustment.md
---

# Payment amount adjustment

This summary derives from version 1 of the candidate draft. [Canonical record](../../../records/candidates/settlement/KT-settlement-payment-amount-adjustment.md).

## Shared controls

Both designs keep the amount change below USD 1 equivalent and require maker/checker approval. The Day 2 design uses the upstream exchange rate. The applicable rate and timestamp need confirmation. [Canonical summary](../../../records/candidates/settlement/KT-settlement-payment-amount-adjustment.md#summary).

## Day 2 manual rounding

The Day 2 design allows changes in WAITING. SWIFT and accounting use the updated amount. The reconciliation team needs to confirm how TLM handles differences. [Day 2 design](../../../records/candidates/settlement/KT-settlement-payment-amount-adjustment.md#day-2-manual-rounding).

## Korea migration adjustment

The Korea design allows editing in specified WAITING and READY states before downstream release. It covers gross cashflows, net resultants, and split parents. It excludes X-prefixed precious-metal currencies and split resultants. Submission enters Pending Verification, and approval returns the cashflow to READY. SWIFT uses the adjusted amount. Settlement accounting uses the original amount. [Korea design](../../../records/candidates/settlement/KT-settlement-payment-amount-adjustment.md#korea-migration-adjustment).

## Open decisions

The rules for state eligibility and accounting differ between the sources. A Korea test scenario also contradicts the recorded split-parent answer. Confirm which design applies per payment flow, entity, and date. [Evidence limits](../../../records/candidates/settlement/KT-settlement-payment-amount-adjustment.md#evidence-limits).

## Related topics

- [[summaries/KT-settlement-auto-netting|Cash Settlement auto-netting]]
- [[summaries/KT-settlement-cashflow-identity-and-stella-write-back|Cashflow identity and Stella status write-back]]
