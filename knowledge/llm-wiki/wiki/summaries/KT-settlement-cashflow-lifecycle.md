---
type: Summary
description: "Summarizes the proposed cashflow state and version model while retaining unresolved transition and suppression conflicts."
doc_type: short
full_text: sources/KT-settlement-cashflow-lifecycle.md
---

> **Candidate/draft only:** State names and transitions are documented designs, not an approved or implemented state machine.

# Cashflow Lifecycle and Versions

The selected state-machine material covers projected, queued, waiting, hold, ready, released, settled, suppressed, netted, failed, utilized, past-due, and split states. It describes materialization, exception checking, release, settlement, suppression, netting, failure, and withdrawal transitions. External requests update business, cashflow, and minor versions; internal requests use minor version in the stated design.

The matrix contains unresolved conflicts. HOLD amendment returns to QUEUED despite dedicated hold descriptions; UnSplit and Fail rows also differ from specialist documents. NOSTRO MATCHED is labeled out of scope but has transition rows. The source warns that matrix entries do not create GUI permission.

For multiple payments, the source selects the sole isIntentToSettle=true item, but its stated fallback chooses the first item when zero or multiple items qualify. Suppression distinguishes payment-only from payment-and-accounting suppression and requires maker-checker for manual changes. Shared SCBML generation responsibilities are proposed, but the selected template and field inventory are incomplete.

## Canonical sections

- [WF-CF-035](../../../records/candidates/settlement/KT-settlement-cashflow-lifecycle.md#wf-cf-035)
- [WF-CF-039](../../../records/candidates/settlement/KT-settlement-cashflow-lifecycle.md#wf-cf-039)
- [WF-CF-041](../../../records/candidates/settlement/KT-settlement-cashflow-lifecycle.md#wf-cf-041)
- [Multiple payment selection](../../../records/candidates/settlement/KT-settlement-cashflow-lifecycle.md#multiple-payment-selection)
- [Suppression purpose and reversal boundaries](../../../records/candidates/settlement/KT-settlement-cashflow-lifecycle.md#suppression-purpose-and-reversal-boundaries)
- [Common SCBML generation responsibility](../../../records/candidates/settlement/KT-settlement-cashflow-lifecycle.md#common-scbml-generation-responsibility)


## Related candidate topics

- [[summaries/KT-settlement-failed-cashflow-recovery]]
- [[summaries/KT-settlement-hold-and-manual-fail]]

These links connect source-specific proposals. Their rules retain their separate scope and evidence limits.
