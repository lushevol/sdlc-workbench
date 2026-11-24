---
type: Summary
description: "Summarizes temporary PSS recovery limits, approval and ticket controls, remediation triggers, and escalation proposals."
doc_type: short
full_text: sources/KT-ratan-technical-recovery-exceptions.md
---

> **Candidate/draft only:** This temporary process lacks effective-version and approval confirmation. Owner is unknown; `verified` is empty.

# RATAN temporary technical recovery controls

The process is limited to strategic-flow technical failures. It excludes BCS flow, data issues, and business exceptions. PSS recovery is temporary and exceptional; Development owns root-cause analysis, recovery design, permanent fixes, and automation. Ops validates outcomes when business confirmation is required.

The process requires Product Owner approval before using a documented workaround and tracks each recovery with an ADO ticket, named Development owner, and committed permanent-fix ETA. It proposes RCA for P4-or-higher incidents or two occurrences in one week, and next-major-release-cycle prioritization after more than three manual recoveries in a month. The Impact Assessment Matrix version and current authority remain unconfirmed.

A two-week KTLO review and escalation path are described. The long-term goal is to remove recurring PSS recovery, not transfer permanent ownership. The related [[summaries/KT-settlement-failed-cashflow-recovery]] describes cashflow failure and reinstatement rules; it does not replace this technical recovery scope.

## Canonical sections

- [Scope and ownership](../../../records/candidates/operations/KT-ratan-technical-recovery-exceptions.md#scope-and-ownership)
- [Approval and tracking](../../../records/candidates/operations/KT-ratan-technical-recovery-exceptions.md#approval-and-tracking)
- [Permanent remediation triggers](../../../records/candidates/operations/KT-ratan-technical-recovery-exceptions.md#permanent-remediation-triggers)
- [Review, escalation, and end state](../../../records/candidates/operations/KT-ratan-technical-recovery-exceptions.md#review-escalation-and-end-state)

## Related candidate topics

- [[summaries/KT-settlement-hold-and-manual-fail]]

These links connect source-specific proposals. Their rules retain their separate scope and evidence limits.
