---
type: Summary
description: "Preserves product-agnostic aggregation predicates, placement alternatives, and the separate SGD-to-SGO proposal."
doc_type: short
full_text: sources/KT-product-agnostic-aggregation-20261115.md
---

> **Candidate/draft only:** The selected aggregation and currency documents do not establish an approved rule or deployment. Owner is unknown; `verified` is empty.

# Product-agnostic aggregation

The aggregation draft requires Group service to preserve `NormalizedPaymentSchedule` while splitting Uber messages into cashflows. It proposes AUTO_AGGREGATION rules for STRATEGIC_SETTLEMENT. The detailed draft selects Stella sender and a stated set of InterestRate:IRSwap taxonomies, booking entities, and counterparties. It excludes fee and settle-as-gross cashflows and recognizes named aggregate statuses.

The proposed wait rule compares expected non-fee schedule elements by currency and payment date with eligible trade cashflows. It waits when expected elements exceed eligible cashflows and otherwise aggregates. Fee cashflows bypass aggregation. The sources present aggregation before and after Group-service processing as alternatives and leave historical cashflows, released/netted rebooks, Stella write-back, and cross-system netting open.

A separate currency note proposes SGD-to-SGO normalization either in Group Management or Netting Service. It does not select where conversion occurs or which downstream fields and consumers use the alias. Existing auto-netting pages cover a distinct scheduled cash-netting workflow and do not settle aggregation placement.

## Canonical sections

- [Preserve normalized schedules](../../../records/candidates/settlement/KT-product-agnostic-aggregation-20261115.md#preserve-normalized-schedules)
- [Source-specific draft rule scope](../../../records/candidates/settlement/KT-product-agnostic-aggregation-20261115.md#source-specific-draft-rule-scope)
- [Unselected aggregation placement alternatives](../../../records/candidates/settlement/KT-product-agnostic-aggregation-20261115.md#unselected-aggregation-placement-alternatives)
- [Currency alias proposal remains unresolved](../../../records/candidates/settlement/KT-product-agnostic-aggregation-20261115.md#currency-alias-proposal-remains-unresolved)

Related service context: [[summaries/KT-day2-auto-netting-service-design]].

## Related candidate topics

- [[summaries/KT-cashflow-group-validation-p3]]

These links connect source-specific proposals. Their rules retain their separate scope and evidence limits.
