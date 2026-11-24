---
type: KnowledgeTopic
id: KT-settlement-aggregation-intent
version: 1
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Netting/Product Agnostic model to identify all cashflows
    for a specific value date to support Auto Aggregation.md
  revision: sha256:5cdf7e3744ca545ec918245a46afd026058f5f6de33f6cfe0f6c632b28e69518
  sha256: 5cdf7e3744ca545ec918245a46afd026058f5f6de33f6cfe0f6c632b28e69518
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Settlement Day2 Requirement/Cashflow Aggregation.md
  revision: sha256:a2e5add76324239925327225cafff754f10573c681a9be54188794adb9bb47df
  sha256: a2e5add76324239925327225cafff754f10573c681a9be54188794adb9bb47df
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Netting/Product Agnostic model to identify all cashflows for a specific
    value date to support Auto Aggregation/page.md
  revision: sha256:5cdf7e3744ca545ec918245a46afd026058f5f6de33f6cfe0f6c632b28e69518
  sha256: 5cdf7e3744ca545ec918245a46afd026058f5f6de33f6cfe0f6c632b28e69518
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Netting/Product Agnostic model to identify all cashflows for a specific
    value date to support Auto Aggregation.md
  revision: sha256:5cdf7e3744ca545ec918245a46afd026058f5f6de33f6cfe0f6c632b28e69518
  sha256: 5cdf7e3744ca545ec918245a46afd026058f5f6de33f6cfe0f6c632b28e69518
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Settlement Day2 Requirement/Cashflow Aggregation/page.md
  revision: sha256:a2e5add76324239925327225cafff754f10573c681a9be54188794adb9bb47df
  sha256: a2e5add76324239925327225cafff754f10573c681a9be54188794adb9bb47df
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Settlement Day2 Requirement/Cashflow Aggregation.md
  revision: sha256:a2e5add76324239925327225cafff754f10573c681a9be54188794adb9bb47df
  sha256: a2e5add76324239925327225cafff754f10573c681a9be54188794adb9bb47df
generated:
  by: agent:sol-auto-netting-review
  at: '2026-11-16T09:45:10.412835+08:00'
verified: []
scope: Historical selected-source design for settlement aggregation intent.
classification: settlement
summary: The selected documents define historical intent and proposals. Current authority
  and applicability remain unresolved.
related: []
open_questions:
- Which aggregation model, action/status vocabulary, and resultant netting permissions
  are approved?
- How do duplicate, cancelled, amended, delayed, fee, and incomplete schedules change
  expected count and grouping?
- Is manual unaggregation required, and what downstream feeds and filters must support
  aggregation?
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# Settlement aggregation intent

## Scope

Historical selected-source design for settlement aggregation intent.

## Summary

The selected documents define historical intent and proposals. Current authority and applicability remain unresolved.

## Documented knowledge

### Dedicated aggregation proposal

The IRS proposal introduces Aggregate and AggregateNew to distinguish two-leg settlement aggregation from user netting.
Aggregate moves eligible WAITING/Pending Another Leg or QUEUED components to AGGREGATED.
AggregateNew creates a QUEUED resultant.
UnAggregate returns AGGREGATED components to QUEUED.

The listed resultant states transition to DEAD when unaggregated.

Sources: [original lines 5–12](../../../evidence/sources/sha256/a2e5add76324239925327225cafff754f10573c681a9be54188794adb9bb47df.md#L5-L12), [original lines 5–12](../../../evidence/sources/sha256/a2e5add76324239925327225cafff754f10573c681a9be54188794adb9bb47df.md#L5-L12).

### Expected schedule count

The product-agnostic proposal counts only trade schedule entries matching cashflow payment currency and payment date.
For IRS and CCS, both legs contribute when their schedules match.
Its coupon and principal mappings prefer cash-settlement currency over notional currency.
It also maps additional payments and amortization schedules.

The amortization currency cells remain blank.

Sources: [original lines 1–18](../../../evidence/sources/sha256/5cdf7e3744ca545ec918245a46afd026058f5f6de33f6cfe0f6c632b28e69518.md#L1-L18), [original lines 1–18](../../../evidence/sources/sha256/5cdf7e3744ca545ec918245a46afd026058f5f6de33f6cfe0f6c632b28e69518.md#L1-L18).

### Completion and grouping

The example waits in Pending Another Leg until four expected payments arrive.
Four is an example count, not a universal product limit.
The grouping key is trade ID, payment date, payment currency, entity, and counterparty.
The proposal permits subsequent netting of the aggregation resultant.

Sources: [original lines 20–35](../../../evidence/sources/sha256/5cdf7e3744ca545ec918245a46afd026058f5f6de33f6cfe0f6c632b28e69518.md#L20-L35), [original lines 20–35](../../../evidence/sources/sha256/5cdf7e3744ca545ec918245a46afd026058f5f6de33f6cfe0f6c632b28e69518.md#L20-L35).

## Connections

Relationships describe the named design responsibilities.
No uninspected canonical relationships are asserted.

## Evidence limits

Historical documents and proposals do not establish current approved behavior.
No implementation, live service, deployment, or business execution was verified.
Excluded page content and unavailable attachments remain unreviewed.

## Open questions

Owner: unknown.

- Which aggregation model, action/status vocabulary, and resultant netting permissions are approved?
- How do duplicate, cancelled, amended, delayed, fee, and incomplete schedules change expected count and grouping?
- Is manual unaggregation required, and what downstream feeds and filters must support aggregation?
