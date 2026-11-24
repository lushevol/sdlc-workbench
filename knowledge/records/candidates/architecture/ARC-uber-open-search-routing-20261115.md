---
type: Architecture
id: ARC-uber-open-search-routing-20261115
version: 2
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Open
    Search Plan/page.md
  revision: sha256:a1fc80934b6906a7636fabf775e2ef26094c795a038e81105c5701f7cec95668
  sha256: a1fc80934b6906a7636fabf775e2ef26094c795a038e81105c5701f7cec95668
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/RATANONE
    Cash Settlement Technical Design/RATAN - Uber Integration/OpenSearch Business
    Live Plan/page.md
  revision: sha256:f582095d6ab538660512f96727a62223681ca9c35d5c4cd90876e9ea12ca5e91
  sha256: f582095d6ab538660512f96727a62223681ca9c35d5c4cd90876e9ea12ca5e91
generated:
  by: agent:sol-auto-netting-review
  at: '2026-11-16T09:23:59.464780+08:00'
verified: []
scope: Historical selected-source design for uber open search routing 20261115.
components:
- OpenSearch query/read persistence
- PostgreSQL fallback
- Three-source reconciliation and DLT recovery
interfaces:
- Internal cashflow/detail/dashboard queries
- Planned external V2 data queries
dependencies:
- Lifecycle history
- Query PostgreSQL data
- Aligned protobuf/GraphQL/OpenSearch models
decisions:
- Stage internal and external adoption separately.
- Retain fallback and require reconciled migration.
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# Uber open search routing 20261115

## Scope

Historical selected-source design for uber open search routing 20261115.

## Components

- OpenSearch query/read persistence
- PostgreSQL fallback
- Three-source reconciliation and DLT recovery

## Interfaces

- Internal cashflow/detail/dashboard queries
- Planned external V2 data queries

## Dependencies

- Lifecycle history
- Query PostgreSQL data
- Aligned protobuf/GraphQL/OpenSearch models

## Decisions

- Stage internal and external adoption separately.
- Retain fallback and require reconciled migration.

## Documented knowledge

### Business-live query target

The OpenSearch plan aims to improve UI querying and reduce relational-database pressure.
Its proposed budgets include 20000-record cashflow/group pages within two seconds and two-second dashboard loads.
It proposes removing the 30-day date limit in favor of a volume bound.
These goals differ from the earlier one-month value-date proposal and require versioned selection.

The plan separately lists detail/history/SWIFT/Accounting, rules, exception, suppression, and netting budgets.
Those remain proposed objectives rather than accepted or executed SLAs.

Sources: [original lines 1–25](../../../evidence/sources/sha256/a1fc80934b6906a7636fabf775e2ef26094c795a038e81105c5701f7cec95668.md#L1-L25).

### Staged adoption and fallback

Day-one internal flow defaults cashflow, details, and dashboard queries to OpenSearch while retaining PostgreSQL persistence.
It requires a switch back to PostgreSQL for production issues.
Historical migration uses a cutoff and idempotent processing.
Real-time reconciliation compares lifecycle history, query PostgreSQL current/history, and OpenSearch current/history.

Earlier planning proposes one month of parallel operation and reconciliation before removing database dependency.
Neither plan grants decommissioning or proves a completed migration.

Sources: [original lines 1–12](../../../evidence/sources/sha256/f582095d6ab538660512f96727a62223681ca9c35d5c4cd90876e9ea12ca5e91.md#L1-L12), [original lines 20–54](../../../evidence/sources/sha256/f582095d6ab538660512f96727a62223681ca9c35d5c4cd90876e9ea12ca5e91.md#L20-L54), [original lines 61–63](../../../evidence/sources/sha256/a1fc80934b6906a7636fabf775e2ef26094c795a038e81105c5701f7cec95668.md#L61-L63).

### Models, external consumers, and recovery

The plan requires alignment among protobuf data, GraphQL results, and OpenSearch schemas.
It distinguishes cashflow/history queries from exception, SSI stashing/candidates, affirmation, and netting-component sources.
Day-two external queries require compatible model changes and an exposed V2 interface.
Reconciliation should identify exact missing cashflows.

The design proposes a DLT index and manual/automatic replay.
Cross-cluster replication enhancement remains an unanswered input.

Sources: [original lines 20–54](../../../evidence/sources/sha256/f582095d6ab538660512f96727a62223681ca9c35d5c4cd90876e9ea12ca5e91.md#L20-L54), [original lines 56–80](../../../evidence/sources/sha256/f582095d6ab538660512f96727a62223681ca9c35d5c4cd90876e9ea12ca5e91.md#L56-L80), [original lines 89–91](../../../evidence/sources/sha256/f582095d6ab538660512f96727a62223681ca9c35d5c4cd90876e9ea12ca5e91.md#L89-L91).

## Connections

Relationships describe the named design responsibilities.
No uninspected canonical relationships are asserted.

## Evidence limits

Historical documents and proposals do not establish current approved behavior.
No implementation, live service, deployment, or business execution was verified.
Excluded page content and unavailable attachments remain unreviewed.

## Open questions

Owner: unknown.

- Which query/date-volume limits, proposed NFR budgets, and fallback/decommission exit criteria are approved?
- Which versioned model routing, reconciliation/replay idempotency, external V2, and replication contracts are complete?
