---
type: KnowledgeTopic
id: KT-settlement-trade-lien-controls
version: 1
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/2024 changes/Lien Settlement Process - Cashflow Migration/RATAN Cashflow
    Process with Lien - Function Specs/page.md
  revision: sha256:a9d89f81465bed149ccf33102cc05693e25a55cfd8229724ce5b3fb83fae3dd2
  sha256: a9d89f81465bed149ccf33102cc05693e25a55cfd8229724ce5b3fb83fae3dd2
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/2024 changes/Lien Settlement Process - Cashflow Migration/page.md
  revision: sha256:e5f59a8d572f48ddce5d09ac52b7ff89ea624a6999f609075dbcb15948e2b186
  sha256: e5f59a8d572f48ddce5d09ac52b7ff89ea624a6999f609075dbcb15948e2b186
generated:
  by: agent:sol-auto-netting-review
  at: '2026-11-16T09:52:25.943978+08:00'
verified: []
scope: Historical selected-source design for settlement trade lien controls.
classification: settlement
summary: The selected documents define historical intent and proposals. Current authority
  and applicability remain unresolved.
related: []
open_questions:
- Which LIEN amount, removal, post-release, and notification-state rules are approved?
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# Settlement trade lien controls

## Scope

Historical selected-source design for settlement trade lien controls.

## Summary

The selected documents define historical intent and proposals. Current authority and applicability remain unresolved.

## Documented knowledge

### Trade-level LIEN governs cashflows

LIEN placement or amount update makes every underlying payment type NSTP, including interest and notional.
The exception requires maker/checker handling.
Removal permits STP only when no other exception remains.
Latest parent-trade LIEN is correlated through original trade identity.

A resultant inherits LIEN when any component parent trade carries LIEN.
Operations profiles cannot remove or edit the predefined exception.

Sources: [original lines 3–3](../../../evidence/sources/sha256/e5f59a8d572f48ddce5d09ac52b7ff89ea624a6999f609075dbcb15948e2b186.md#L3-L3), [original lines 12–13](../../../evidence/sources/sha256/e5f59a8d572f48ddce5d09ac52b7ff89ea624a6999f609075dbcb15948e2b186.md#L12-L13), [original lines 17–17](../../../evidence/sources/sha256/e5f59a8d572f48ddce5d09ac52b7ff89ea624a6999f609075dbcb15948e2b186.md#L17-L17), [original lines 23–23](../../../evidence/sources/sha256/e5f59a8d572f48ddce5d09ac52b7ff89ea624a6999f609075dbcb15948e2b186.md#L23-L23), [original lines 3–3](../../../evidence/sources/sha256/a9d89f81465bed149ccf33102cc05693e25a55cfd8229724ce5b3fb83fae3dd2.md#L3-L3), [original lines 7–16](../../../evidence/sources/sha256/a9d89f81465bed149ccf33102cc05693e25a55cfd8229724ce5b3fb83fae3dd2.md#L7-L16).

### LIEN notification reprocessing

New LIEN can reprocess WAITING/Pending Exception, HOLD, and READY cashflows lacking the exception.
It can trigger unnetting only when the resultant lacks LIEN and remains outside protected released-like states.
Protected states include READY/Pending Ack, RELEASED, and SETTLED.
A later trade notification must handle cashflows received before the trade update.

Sources: [original lines 7–16](../../../evidence/sources/sha256/a9d89f81465bed149ccf33102cc05693e25a55cfd8229724ce5b3fb83fae3dd2.md#L7-L16), [original lines 28–30](../../../evidence/sources/sha256/a9d89f81465bed149ccf33102cc05693e25a55cfd8229724ce5b3fb83fae3dd2.md#L28-L30).

## Connections

Relationships describe the named design responsibilities.
No uninspected canonical relationships are asserted.

## Evidence limits

Historical documents and proposals do not establish current approved behavior.
No implementation, live service, deployment, or business execution was verified.
Excluded page content and unavailable attachments remain unreviewed.

## Open questions

Owner: unknown.

- Which LIEN amount, removal, post-release, and notification-state rules are approved?
