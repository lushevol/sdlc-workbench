---
type: Summary
description: "Summarizes candidate final-status triggers and cover-message aggregation conditions."
doc_type: short
full_text: sources/KT-day2-fmsgw-deletion-settlement.md
---

# FMSGW deletion and final cashflow status

> **Source status:** Candidate/draft. This retained requirement has unresolved authority, gateway scope, and ordering behavior.

The source proposes setting cashflow status to SETTLED after FMSGW Deleted, FMSRE Deleted, Manual Delete, Released by SCPAY, or Released by AMH. It explicitly chooses SETTLED instead of SWIFT_SUPPRESSED because of a duplicate-accounting concern. That is the source's rationale, not an observed failure in this review. [Final status trigger](../../../records/candidates/settlement/KT-day2-fmsgw-deletion-settlement.md#final-status-trigger)

For MT103/MT202COV, both responses must be in the allowed final-status set, although their values may differ. A delete plus error leaves the cashflow RELEASED. Two allowed but different responses settle the cashflow while Swift status remains “Check in FMSGW,” meaning the COV message statuses differ. Listed MT103, MT202, MT210, MT202Flip, MT192, MT292, MT604, MT605, and MT692 cases are expected scenarios, not passing execution. [Cover-message aggregation](../../../records/candidates/settlement/KT-day2-fmsgw-deletion-settlement.md#cover-message-aggregation) [Open questions](../../../records/candidates/settlement/KT-day2-fmsgw-deletion-settlement.md#open-questions)

Confirm applicable gateways/message types and delayed or changed response ordering before treating this as current policy. Related: [[summaries/KT-settlement-multi-exception-control]] and [[summaries/INT-KT-ratan-cashflow-settlement-interfaces]].
