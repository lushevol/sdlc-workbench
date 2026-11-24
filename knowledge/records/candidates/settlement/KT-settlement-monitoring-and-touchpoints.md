---
type: KnowledgeTopic
id: KT-settlement-monitoring-and-touchpoints
version: 1
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/MX2.11 Decomm
    - Cash Settlement Business Workflow/High Level Workflow/MIS Requirements/page.md
  revision: sha256:8b6da8180ec826e473cc52bf07ab4fcd3246e53386617779ee8b2ad106b02e23
  sha256: 8b6da8180ec826e473cc52bf07ab4fcd3246e53386617779ee8b2ad106b02e23
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/MX2.11 Decomm
    - Cash Settlement Business Workflow/Settlement Touchpoints/page.md
  revision: sha256:ef93d1374fa97781b08068ef55a4396bc011bcb79f6346aed889739a1a54dc38
  sha256: ef93d1374fa97781b08068ef55a4396bc011bcb79f6346aed889739a1a54dc38
generated:
  by: agent:sol-auto-netting-review
  at: '2026-11-16T09:52:25.840131+08:00'
verified: []
scope: Historical selected-source design for settlement monitoring and touchpoints.
classification: settlement
summary: The selected documents define historical intent and proposals. Current authority
  and applicability remain unresolved.
related: []
open_questions:
- Which dashboard measures, cutoff definitions, drilldowns, and roadmap targets are
  approved for each rollout?
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# Settlement monitoring and touchpoints

## Scope

Historical selected-source design for settlement monitoring and touchpoints.

## Summary

The selected documents define historical intent and proposals. Current authority and applicability remain unresolved.

## Documented knowledge

### Management information

The MIS requirement measures complete front-to-back STP and function-level manual touchpoints.
Settlement dashboards show volume and value near cutoffs, missing SSI, high value, failed trades, and priority clients.
Missing-SSI monitoring covers the next five business days.
Breakdowns include geography, client, settlement method, period, product, touchpoint, and status.

Required attributes include cashflows, maker/checker actions, user profiles, client type, and P100 tagging.
RATAN should feed the TPP report.

Sources: [original lines 1–32](../../../evidence/sources/sha256/8b6da8180ec826e473cc52bf07ab4fcd3246e53386617779ee8b2ad106b02e23.md#L1-L32).

### Touchpoint roadmap boundary

The touchpoint roadmap separates China Day1 handling from target automation and dependencies.
Target automation includes external-venue netting, SSI selection, receipt-driven DVP release, and payment-gateway integration.
Settlement-method authority, commodity handling, mandatory currency identifiers, and several manual workflows remain unresolved.
Its existing-state descriptions do not establish target implementation or completion.

Sources: [original lines 1–56](../../../evidence/sources/sha256/ef93d1374fa97781b08068ef55a4396bc011bcb79f6346aed889739a1a54dc38.md#L1-L56).

## Connections

Relationships describe the named design responsibilities.
No uninspected canonical relationships are asserted.

## Evidence limits

Historical documents and proposals do not establish current approved behavior.
No implementation, live service, deployment, or business execution was verified.
Excluded page content and unavailable attachments remain unreviewed.

## Open questions

Owner: unknown.

- Which dashboard measures, cutoff definitions, drilldowns, and roadmap targets are approved for each rollout?
