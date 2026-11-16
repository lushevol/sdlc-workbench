---
type: Summary
description: Summarizes historical China Day 1 and Payment Lake cross-product netting proposals.
doc_type: short
full_text: sources/KT-settlement-cpn-netting.md
---

> Derived from [candidate record version 1](../../../records/candidates/settlement/KT-settlement-cpn-netting.md). Owner review and publication remain pending.

# CPN eligibility, manual netting, and review

The candidate preserves historical China Day 1 and Payment Lake proposals. They describe eligibility, source routing, manual and ad hoc netting, checker review, Force Gross, un-net, and amendment or cancellation handling. [Scope and routing](../../../records/candidates/settlement/KT-settlement-cpn-netting.md#china-day-1-and-source-routing) [Manual netting](../../../records/candidates/settlement/KT-settlement-cpn-netting.md#manual-and-ad-hoc-netting) [Lifecycle actions](../../../records/candidates/settlement/KT-settlement-cpn-netting.md#force-gross-and-manual-un-net).

The business and technical drafts use different state and action labels. Applicability, review roles, resultant identity, and some lifecycle outcomes remain unresolved. [Evidence limits](../../../records/candidates/settlement/KT-settlement-cpn-netting.md#evidence-limits) [Open questions](../../../records/candidates/settlement/KT-settlement-cpn-netting.md#open-questions).

The candidate records no current approval, deployment, or runtime verification.

## Related topics

- [[summaries/KT-settlement-auto-netting|Scheduled auto-netting]] covers the separate scheduled rule and execution-key design.
- [[summaries/KT-settlement-group-blotter-controls|Group Blotter controls]] records related cashflow selection and status predicates.

## Source-specific workflow boundaries

China Day 1 covers derivatives and excludes Razor cashflows. The FMRP branch checks SCI, counterparty/currency/product static, then currency exclusions. Scheduled CPN remains outside Day 1 in the scenario matrices. A separate future-schedule example has unresolved applicability. [Routing and scope](../../../records/candidates/settlement/KT-settlement-cpn-netting.md#china-day-1-and-source-routing).

Manual netting requires matching entity, counterparty, currency, and value date. Released or Settled components fail validation. A common netting ID links components and resultant. Maker and checker must differ. Submission makes components Netted and creates a Queued gross resultant. Business approval ends at Validated/Pending Release; the technical example uses Validated/Reviewed. First-component SSI/product inheritance and its inconsistent example remain unresolved. [Manual review](../../../records/candidates/settlement/KT-settlement-cpn-netting.md#manual-and-ad-hoc-netting).

Full manual un-net is proposed for Pending or Validated resultants before release. Checker approval marks the resultant Dead and requeues components. Partial un-net and net-of-net remain excluded from that technical draft. Force Gross review-role wording conflicts. [Gross and un-net](../../../records/candidates/settlement/KT-settlement-cpn-netting.md#force-gross-and-manual-un-net).

Before release, component changes can trigger automatic un-net and eligibility rerun. After release or settlement, the original resultant remains. A linked reversal waits in NSTP Release for Operations. MTx92 generation remains a future option. Inconsistent cancellation labels and actions on Dead components cannot establish an accepted action contract. [Component events](../../../records/candidates/settlement/KT-settlement-cpn-netting.md#component-amendment-and-cancellation).
