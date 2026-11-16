---
type: KnowledgeTopic
id: KT-settlement-fx-utilization-responsibilities
version: 1
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: source:ratan-51358/RATAN - 51358/RATAN -Core Function/Function_RATAN-FXU/page.md
  revision: sha256:ec2e8695d390d6078e1803a94420e97382a2c7d0d668904491b58b5733771c40
  sha256: ec2e8695d390d6078e1803a94420e97382a2c7d0d668904491b58b5733771c40
generated:
  by: agent:sol-auto-netting-review
  at: '2026-11-16T09:52:25.905463+08:00'
verified: []
scope: Historical selected-source design for settlement fx utilization responsibilities.
classification: settlement
summary: The selected documents define historical intent and proposals. Current authority
  and applicability remain unresolved.
related: []
open_questions:
- What utilization eligibility, remaining-amount, accounting-date, and amendment-lock
  contracts are approved?
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# Settlement fx utilization responsibilities

## Scope

Historical selected-source design for settlement fx utilization responsibilities.

## Summary

The selected documents define historical intent and proposals. Current authority and applicability remain unresolved.

## Documented knowledge

### FX utilization responsibility

FX utilization settles through Transaction Banking systems while RATAN generates accounting.
Utilization classification uses booking entity and counterparty.
Utilization cashflows suppress RATAN SWIFT and retain accounting.
The design returns utilization status to FXU and TDS3 for trade amendment locking.

Remaining-amount queries support further utilization and reverse-trade booking.
Past-due automatic utilization and partial accounting remain Day2 proposals.

Sources: [original lines 9–24](../../../evidence/sources/sha256/ec2e8695d390d6078e1803a94420e97382a2c7d0d668904491b58b5733771c40.md#L9-L24), [original lines 28–34](../../../evidence/sources/sha256/ec2e8695d390d6078e1803a94420e97382a2c7d0d668904491b58b5733771c40.md#L28-L34).

## Connections

Relationships describe the named design responsibilities.
No uninspected canonical relationships are asserted.

## Evidence limits

Historical documents and proposals do not establish current approved behavior.
No implementation, live service, deployment, or business execution was verified.
Excluded page content and unavailable attachments remain unreviewed.

## Open questions

Owner: unknown.

- What utilization eligibility, remaining-amount, accounting-date, and amendment-lock contracts are approved?
