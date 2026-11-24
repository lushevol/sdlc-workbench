---
type: Summary
description: Summarizes Group Blotter eligibility, batch processing proposals, and field projections.
doc_type: short
full_text: sources/KT-settlement-group-blotter-controls.md
---

> Derived from [candidate record version 1](../../../records/candidates/settlement/KT-settlement-group-blotter-controls.md). Owner review and publication remain pending.

# Group Blotter controls

The candidate covers pagination, Manual STP selection, batch processing, expected outcomes, and a separate cashflow and trade field projection. [Action eligibility](../../../records/candidates/settlement/KT-settlement-group-blotter-controls.md#action-eligibility-and-warning) [Processing cases](../../../records/candidates/settlement/KT-settlement-group-blotter-controls.md#processing-and-expected-outcomes) [Field projection](../../../records/candidates/settlement/KT-settlement-group-blotter-controls.md#field-projection).

The proposed UI eligibility and processor filtering predicates differ. Status labels also vary across the requirement and later decision. The candidate leaves mapping, retry behavior, partial outcomes, and release applicability open. [Evidence limits](../../../records/candidates/settlement/KT-settlement-group-blotter-controls.md#evidence-limits) [Open questions](../../../records/candidates/settlement/KT-settlement-group-blotter-controls.md#open-questions).

These proposals do not establish current production behavior or approval.

## Related topics

- [[summaries/KT-settlement-cashflow-identity-and-stella-write-back|Cashflow identity and downstream processing]] covers the related cashflow lifecycle and identity questions.
- [[summaries/KT-settlement-cpn-netting|CPN netting]] records separate netting proposals that also affect cashflow selection and status.

## Bounded action and processing predicates

Pagination defaults to 1,000 records, with another 1,000 load or a 5,000 page size. Bulk Manual STP requires every selected cashflow's group to be PENDING_TRADE_VALIDATION or PENDING_PRE_GROUP. Other statuses produce an error. The warning requires support-team instruction and displays the selected cashflow count. A closed November 2025 entry instead uses PENDING_PREV_GROUP. That spelling difference remains unresolved. [Action gate and warning](../../../records/candidates/settlement/KT-settlement-group-blotter-controls.md#action-eligibility-and-warning).

The technical design accepts PENDING or ERROR messages only when the previous major version has no pending group message. Bulk processing groups by trade, prechecks, orders major versions, and filters DATA_VALIDATION_FAILED or PENDING_PRE_GROUP. UI eligibility does not guarantee processor success. Expected successful cases reach cashflow END, group COMPLETED, and ManualDeliver. A later group with an incomplete earlier group must fail. These are expected cases, without passing execution. [Processing expectations](../../../records/candidates/settlement/KT-settlement-group-blotter-controls.md#processing-and-expected-outcomes).

The field list separates cashflow economic fields from trade LIEN_Monitoring and special trade fields. Source labels associate settlement method with SCBML/Uber and portfolio with RFI. These labels supply no verified rollout, grouping, filtering, or action authorization. [Projection scope](../../../records/candidates/settlement/KT-settlement-group-blotter-controls.md#field-projection).
