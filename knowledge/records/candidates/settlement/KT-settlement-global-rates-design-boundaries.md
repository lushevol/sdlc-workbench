---
type: KnowledgeTopic
id: KT-settlement-global-rates-design-boundaries
version: 1
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/03-FMRP Requirement/Global Rates - Settlement Strategy Process & Dependency/page.md
  revision: sha256:43a1b07ba01c8e19d7ba14fa9be377f2f1bbbbf441b1d8bbeb7ca1aa198fd427
  sha256: 43a1b07ba01c8e19d7ba14fa9be377f2f1bbbbf441b1d8bbeb7ca1aa198fd427
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/03-FMRP Requirement/page.md
  revision: sha256:845035aa0a6f78cdd25e21d0da3123e558455ebca450cc91dc5798a76efe38f5
  sha256: 845035aa0a6f78cdd25e21d0da3123e558455ebca450cc91dc5798a76efe38f5
generated:
  by: agent:sol-auto-netting-review
  at: '2026-11-16T09:52:25.926813+08:00'
verified: []
scope: Historical selected-source design for settlement global rates design boundaries.
classification: settlement
summary: The selected documents define historical intent and proposals. Current authority
  and applicability remain unresolved.
related: []
open_questions:
- Which Global Rates scope, event contracts, golden sources, and settlement-method
  amendment design are approved?
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# Settlement global rates design boundaries

## Scope

Historical selected-source design for settlement global rates design boundaries.

## Summary

The selected documents define historical intent and proposals. Current authority and applicability remain unresolved.

## Documented knowledge

### Global Rates target responsibilities

The strategy asks Blade or Stella to stamp settlement method on trades and cashflows.
Later settlement-method amendment remains required but its operating solution is unresolved.
The DVP proposal holds payments until receipt settlement confirmation.
Shared rounding, identifiers, currencies, and product classification need aligned source ownership.

CLS, PVP, netting agreements, LIEN, rollover, and utilization contain unanswered design questions.

Sources: [original lines 1–25](../../../evidence/sources/sha256/43a1b07ba01c8e19d7ba14fa9be377f2f1bbbbf441b1d8bbeb7ca1aa198fd427.md#L1-L25).

### Event and booking proposals

The feature inventory proposes distinct Clearing and Remaining Party Full events.
Allocation block trades generate SUSPENDED cashflows, while child trades generate PROJECTED cashflows.
Refresh represents calendar-driven amendment behavior.
Step-in events are described as new bookings.

Deliverable-currency and ND-convert features require explicit product and currency scope.
Feature labels and No Dev/Only UAT annotations do not prove conformance or execution.

Sources: [original lines 16–78](../../../evidence/sources/sha256/845035aa0a6f78cdd25e21d0da3123e558455ebca450cc91dc5798a76efe38f5.md#L16-L78).

## Connections

Relationships describe the named design responsibilities.
No uninspected canonical relationships are asserted.

## Evidence limits

Historical documents and proposals do not establish current approved behavior.
No implementation, live service, deployment, or business execution was verified.
Excluded page content and unavailable attachments remain unreviewed.

## Open questions

Owner: unknown.

- Which Global Rates scope, event contracts, golden sources, and settlement-method amendment design are approved?
