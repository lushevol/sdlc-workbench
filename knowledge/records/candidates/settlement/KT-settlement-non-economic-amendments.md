---
type: KnowledgeTopic
id: KT-settlement-non-economic-amendments
version: 1
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Trade & Cashflow Events Control/Non Economic amendment(FMRP) Cashflows/page.md
  revision: sha256:752c1e23c76e212e6ecdc6f59120e69309227912713718837473375c86a5532d
  sha256: 752c1e23c76e212e6ecdc6f59120e69309227912713718837473375c86a5532d
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Trade & Cashflow Events Control/Ratan Non Economic Cashflow Handling/page.md
  revision: sha256:b967cfa06e39ffd5a6d884c7ab223f44b3efdbf2e1e8df482eb2663d15c80753
  sha256: b967cfa06e39ffd5a6d884c7ab223f44b3efdbf2e1e8df482eb2663d15c80753
generated:
  by: agent:sol-auto-netting-review
  at: '2026-11-16T09:50:02.841324+08:00'
verified: []
scope: Historical selected-source design for settlement non economic amendments.
classification: settlement
summary: The selected documents define historical intent and proposals. Current authority
  and applicability remain unresolved.
related: []
open_questions:
- What approved identity mapping governs repeated non-economic amendments followed
  by economic amendments?
- Which products, feeds, and effective versions implement the six-field non-economic
  contract?
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# Settlement non economic amendments

## Scope

Historical selected-source design for settlement non economic amendments.

## Summary

The selected documents define historical intent and proposals. Current authority and applicability remain unresolved.

## Documented knowledge

### Non-economic comparison

The design compares booking FMID, counterparty FMID, currency, amount, value date, and pay/receive.
When all six match, replacement cashflows are ignored operationally and originals remain active for settlement.
The trade still receives a new version and replacement cashflow identities.
The proposed UI hides the non-economic replacements.

Sources: [original lines 3–3](../../../evidence/sources/sha256/752c1e23c76e212e6ecdc6f59120e69309227912713718837473375c86a5532d.md#L3-L3), [original lines 10–16](../../../evidence/sources/sha256/752c1e23c76e212e6ecdc6f59120e69309227912713718837473375c86a5532d.md#L10-L16), [original lines 1–68](../../../evidence/sources/sha256/b967cfa06e39ffd5a6d884c7ab223f44b3efdbf2e1e8df482eb2663d15c80753.md#L1-L68).

### Settlement identity and external status identity

Original settlement identities remain in Razor, LMS, and the EOD cashflow API.
Replacement identities are excluded from these feeds.
Stella status updates target replacement active identities.
Released, Settled, and Netted statuses propagate to those replacements.

Projected remains Projected until a later status update targets the replacement.
A later economic amendment withdraws original settlement identities before creating new cashflows.

Sources: [original lines 10–16](../../../evidence/sources/sha256/752c1e23c76e212e6ecdc6f59120e69309227912713718837473375c86a5532d.md#L10-L16), [original lines 34–39](../../../evidence/sources/sha256/752c1e23c76e212e6ecdc6f59120e69309227912713718837473375c86a5532d.md#L34-L39), [original lines 1–68](../../../evidence/sources/sha256/b967cfa06e39ffd5a6d884c7ab223f44b3efdbf2e1e8df482eb2663d15c80753.md#L1-L68).

### Trade confirmation identity

The proposal uses the latest CDU trade ID and trade version for confirmation.
This rule applies to both economic and non-economic amendments.

Sources: [original lines 1–68](../../../evidence/sources/sha256/b967cfa06e39ffd5a6d884c7ab223f44b3efdbf2e1e8df482eb2663d15c80753.md#L1-L68).

## Connections

Relationships describe the named design responsibilities.
No uninspected canonical relationships are asserted.

## Evidence limits

Historical documents and proposals do not establish current approved behavior.
No implementation, live service, deployment, or business execution was verified.
Excluded page content and unavailable attachments remain unreviewed.

## Open questions

Owner: unknown.

- What approved identity mapping governs repeated non-economic amendments followed by economic amendments?
- Which products, feeds, and effective versions implement the six-field non-economic contract?
