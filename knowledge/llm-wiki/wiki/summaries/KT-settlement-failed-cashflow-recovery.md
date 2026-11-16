---
type: Summary
description: "Summarizes proposed scheduled failure and reinstatement workflows with date-choice, maker-checker, and accounting differences retained."
doc_type: short
full_text: sources/KT-settlement-failed-cashflow-recovery.md
---

> **Candidate/draft only:** Failure cutoffs and recovery actions remain source-specific proposals, not verified current operations.

# Failed Cashflow Recovery

The selected material describes a scheduled failed-cashflow job and manual failure for PROJECTED, QUEUED, WAITING, READY, or ONHOLD states. It excludes named terminal, suppressed, released, settled, netted, split, and Nostro-matched states. The CN Day 1 job includes weekends and holidays with an unspecified time; the longer-term proposal uses currency-specific cutoffs. A sample 10:00 GMT row is not a universal cutoff.

Reinstatement returns FAILED cashflows to QUEUED and reruns netting/client and exception checks. The maker and checker select the Swift value date independently; mismatch warns the checker. The child page lists two date choices, while the parent source lists three. Manual fail is immediate in one design, while another requires maker-checker.

One historical design sends failed cashflows to Razor for accounting at value-date EOD, then generates Swift only after reinstatement, unless amendment or cancellation requires accounting reversal. How this relates to later RATAN accounting remains open. The record does not establish current schedule, recovery execution, or approval.

## Canonical sections

- [WF-CF-017](../../../records/candidates/settlement/KT-settlement-failed-cashflow-recovery.md#wf-cf-017)
- [WF-CF-018](../../../records/candidates/settlement/KT-settlement-failed-cashflow-recovery.md#wf-cf-018)
- [WF-CF-019](../../../records/candidates/settlement/KT-settlement-failed-cashflow-recovery.md#wf-cf-019)
- [WF-CF-020](../../../records/candidates/settlement/KT-settlement-failed-cashflow-recovery.md#wf-cf-020)
- [WF-CF-021](../../../records/candidates/settlement/KT-settlement-failed-cashflow-recovery.md#wf-cf-021)
- [Exact failed-state and date boundaries](../../../records/candidates/settlement/KT-settlement-failed-cashflow-recovery.md#exact-failed-state-and-date-boundaries)


## Related candidate topics

- [[summaries/KT-settlement-hold-and-manual-fail]]
- [[summaries/KT-settlement-cashflow-lifecycle]]

These links connect source-specific proposals. Their rules retain their separate scope and evidence limits.
