---
type: Summary
description: "Summarizes candidate FMRP and BCS cashflow actions, display rules, historical paths, and version limits."
doc_type: short
full_text: sources/KT-settlement-cashflow-blotter-actions.md
---

# Cashflow blotter actions and display

> **Source status:** Candidate/draft. Action matrices are source-specific designs, not proof of current authorization or execution.

The FMRP detail view proposes separate trade and cashflow fields, exception panels, and action visibility based on state, sub-state, exception, settlement method, and other attributes. Most mutation rows exclude UTIL. Netting, splitting, un-split, and un-net have distinct predicates; the source leaves some fields and historical rows incomplete. [WF-CF-001](../../../records/candidates/settlement/KT-settlement-cashflow-blotter-actions.md#wf-cf-001) [WF-CF-003](../../../records/candidates/settlement/KT-settlement-cashflow-blotter-actions.md#wf-cf-003) [WF-CF-004](../../../records/candidates/settlement/KT-settlement-cashflow-blotter-actions.md#wf-cf-004)

BCS has a separate permission and action matrix. Its literal `RATAN_CASHFLOW_BLOTTER` permissions cannot be merged with FMRP or translated into CES roles from this record. The leading FMRP matrix also conflicts with historical notes on Hold eligibility and manual-settle statuses. [WF-CF-007](../../../records/candidates/settlement/KT-settlement-cashflow-blotter-actions.md#wf-cf-007) [WF-CF-008](../../../records/candidates/settlement/KT-settlement-cashflow-blotter-actions.md#wf-cf-008) [Leading-matrix limits](../../../records/candidates/settlement/KT-settlement-cashflow-blotter-actions.md#leading-matrix-limits)

Historical notes distinguish SWIFT suppression from cashflow suppression and describe maker/checker recovery through QUEUED. Separate UI proposals cover BIC display, filter ordering, and a UTC/local toggle; the field inventory and conversion rule remain open. No design establishes deployed behavior. [Historical suppression and recovery distinctions](../../../records/candidates/settlement/KT-settlement-cashflow-blotter-actions.md#historical-suppression-and-recovery-distinctions) [WF-CF-033](../../../records/candidates/settlement/KT-settlement-cashflow-blotter-actions.md#wf-cf-033)

Related proposal: [[summaries/KT-settlement-multi-exception-control]].
