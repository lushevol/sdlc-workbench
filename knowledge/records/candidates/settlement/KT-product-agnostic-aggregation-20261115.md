---
type: KnowledgeTopic
id: KT-product-agnostic-aggregation-20261115
version: 2
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/RATANONE Cash Settlement Technical Design/Product Agnostic Aggregation
    Design.md
  revision: sha256:be292a5b56d53663ae9e5215759e851be1a358fa1357be3c874db7967b63e513
  sha256: be292a5b56d53663ae9e5215759e851be1a358fa1357be3c874db7967b63e513
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Online
    Offline currency conversion solution/page.md
  revision: sha256:d14ba60756912ce565656bca374f20ba73b3ad30e2b56a274015428f8b1e09bc
  sha256: d14ba60756912ce565656bca374f20ba73b3ad30e2b56a274015428f8b1e09bc
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/RATANONE
    Cash Settlement Technical Design/Product Agnostic Aggregation Design/page.md
  revision: sha256:992d8849782e4460b605d0dedb38cf190497d4712211818f9acdddbbe5c6772b
  sha256: 992d8849782e4460b605d0dedb38cf190497d4712211818f9acdddbbe5c6772b
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/RATANONE
    Cash Settlement Technical Design/Product Agnostic Aggregation Design.md
  revision: sha256:be292a5b56d53663ae9e5215759e851be1a358fa1357be3c874db7967b63e513
  sha256: be292a5b56d53663ae9e5215759e851be1a358fa1357be3c874db7967b63e513
generated:
  by: agent:sol-auto-netting-review
  at: '2026-11-16T09:29:53.302130+08:00'
verified: []
scope: Historical selected-source design for product agnostic aggregation 20261115.
classification: settlement
summary: The selected documents define historical intent and proposals. Current authority
  and applicability remain unresolved.
related: []
open_questions:
- Which aggregation placement, rule scope, schedule availability, and current source
  revision are approved?
- How must historical cashflows, released/netted rebooks, Stella writeback, and cross-system
  netting behave?
- Where must SGD-to-SGO conversion occur, and which downstream fields and consumers
  must observe the alias?
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# Product agnostic aggregation 20261115

## Scope

Historical selected-source design for product agnostic aggregation 20261115.

## Summary

The selected documents define historical intent and proposals. Current authority and applicability remain unresolved.

## Documented knowledge

### Preserve normalized schedules

The aggregation draft requires Group service to preserve NormalizedPaymentSchedule when splitting Uber messages into cashflows.
The foundation proposal requires compatible Uber client libraries for the new element.
The rule-service proposal introduces AUTO_AGGREGATION rules for STRATEGIC_SETTLEMENT.

Sources: [original lines 7–11](../../../evidence/sources/sha256/be292a5b56d53663ae9e5215759e851be1a358fa1357be3c874db7967b63e513.md#L7-L11), [original lines 17–21](../../../evidence/sources/sha256/be292a5b56d53663ae9e5215759e851be1a358fa1357be3c874db7967b63e513.md#L17-L21), [original lines 49–53](../../../evidence/sources/sha256/be292a5b56d53663ae9e5215759e851be1a358fa1357be3c874db7967b63e513.md#L49-L53).

### Wait for expected eligible legs

The draft counts schedule elements by currency and payment date, excluding fees.
It compares that count with trade cashflows sharing currency and payment date and excluding AsGross cashflows.
When expected elements exceed eligible cashflows, the cashflow waits for another leg.
Otherwise, the proposal aggregates those cashflows.

Fee cashflows bypass aggregation, and fee schedule elements reduce the expected count.

Sources: [original lines 33–43](../../../evidence/sources/sha256/be292a5b56d53663ae9e5215759e851be1a358fa1357be3c874db7967b63e513.md#L33-L43).

### Source-specific draft rule scope

The detailed V2 draft selects Stella sender and five InterestRate:IRSwap taxonomies.
Those suffixes are FixedFloat, OIS, FloatFloat, Basis, and FixedFixed.
Booking entity FMIDs are 300011345 and 10038345.
Counterparty FMIDs are 10055390, 10037780, 10023033, and 205001936.

Cashflow eligibility excludes Fee payment types and settle-as-gross cashflows.
Aggregate status must be Pending_Aggregate or Auto_Aggregated.

Sources: [original lines 28–37](../../../evidence/sources/sha256/992d8849782e4460b605d0dedb38cf190497d4712211818f9acdddbbe5c6772b.md#L28-L37).

### Unselected aggregation placement alternatives

The detailed draft presents aggregation before and after Group-service processing.
It leaves historical cashflows, released/netted rebooks, Stella writeback, and netting with Murex cashflows unresolved.
The selected source supplies no final choice between these placements.

Sources: [original lines 39–91](../../../evidence/sources/sha256/992d8849782e4460b605d0dedb38cf190497d4712211818f9acdddbbe5c6772b.md#L39-L91).

### Currency alias proposal remains unresolved

The currency proposal requests SGD-to-SGO normalization before downstream processing.
Its first option places normalization only in Group Management before currency-dependent standardization.
Its second option places normalization only in Netting Service.
That option covers manual netting, IRS, and auto-netting.

The source does not select either option.

Sources: [original lines 1–31](../../../evidence/sources/sha256/d14ba60756912ce565656bca374f20ba73b3ad30e2b56a274015428f8b1e09bc.md#L1-L31), [original lines 38–75](../../../evidence/sources/sha256/d14ba60756912ce565656bca374f20ba73b3ad30e2b56a274015428f8b1e09bc.md#L38-L75).

## Connections

Relationships describe the named design responsibilities.
No uninspected canonical relationships are asserted.

## Evidence limits

Historical documents and proposals do not establish current approved behavior.
No implementation, live service, deployment, or business execution was verified.
Excluded page content and unavailable attachments remain unreviewed.

## Open questions

Owner: unknown.

- Which aggregation placement, rule scope, schedule availability, and current source revision are approved?
- How must historical cashflows, released/netted rebooks, Stella writeback, and cross-system netting behave?
- Where must SGD-to-SGO conversion occur, and which downstream fields and consumers must observe the alias?
