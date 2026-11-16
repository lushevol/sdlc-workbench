---
type: Architecture
id: ARC-platform-cashflow-data-query
version: 2
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Cash
    Settlement System Design/Cash Settlement Query Service Design/Cash flow query
    model/page.md
  revision: sha256:752edd6f465190c725f7440244fe3f42c251593a755d55dbfbcbfa0e7d34ee83
  sha256: 752edd6f465190c725f7440244fe3f42c251593a755d55dbfbcbfa0e7d34ee83
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Cash
    Settlement System Design/Cash Settlement Query Service Design/cashflow notification/page.md
  revision: sha256:1dcb5bb3c3869392848262ba9eb1960c462585f6ba0c29d661bf1ef5ca9c511e
  sha256: 1dcb5bb3c3869392848262ba9eb1960c462585f6ba0c29d661bf1ef5ca9c511e
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Cash
    Settlement System Design/Cash Settlement Query Service Design/page.md
  revision: sha256:15126a1e95e2e319c486757ef75d9a90811a438ef49d5e07e242fad63f9cfff3
  sha256: 15126a1e95e2e319c486757ef75d9a90811a438ef49d5e07e242fad63f9cfff3
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Cash
    Settlement System Design/Cashflow Blotter Dashboard add NSTP exception filter/page.md
  revision: sha256:e0cd1c6713e36a098bfaf4ec60234a20eb73d84a89acd01d5549c88bdcf94527
  sha256: e0cd1c6713e36a098bfaf4ec60234a20eb73d84a89acd01d5549c88bdcf94527
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Cash
    Settlement System Design/Query Service -Dashboard/page.md
  revision: sha256:ed8d144c7e9f9aede3db78105e91e89491b144d90ce28964eda1f9153118710e
  sha256: ed8d144c7e9f9aede3db78105e91e89491b144d90ce28964eda1f9153118710e
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Cashflow
    Query Service - GraghQL schema and DB column mapping for dynamic query/page.md
  revision: sha256:e6fae5521783aec72bda7d252c61aedaf723f2d35d0abcfb9200002b17bb61bd
  sha256: e6fae5521783aec72bda7d252c61aedaf723f2d35d0abcfb9200002b17bb61bd
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/GraphQL
    Used For Front End In RATAN/GraphQL Proposal/page.md
  revision: sha256:bdf6eee37dcea57a2bc7c10a997f91b6026610ef8997baf0ff49fcc915299a50
  sha256: bdf6eee37dcea57a2bc7c10a997f91b6026610ef8997baf0ff49fcc915299a50
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/GraphQL
    Used For Front End In RATAN/GraphQL Schema Completion 2025/page.md
  revision: sha256:6acb86fee2fa59a8e9efa181f2491804cb9bba5b16231bc08eaa439e9ba3ab05
  sha256: 6acb86fee2fa59a8e9efa181f2491804cb9bba5b16231bc08eaa439e9ba3ab05
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/GraphQL
    Used For Front End In RATAN/page.md
  revision: sha256:4b916ca3d1a43de7b1c3627c8eb2a70b4a7caef434569ea715ebd11cdecf16f9
  sha256: 4b916ca3d1a43de7b1c3627c8eb2a70b4a7caef434569ea715ebd11cdecf16f9
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/RATANONE
    Cash Settlement Technical Design/RATAN - Uber Integration/Cash Settlement Query
    Service - cashflow_data_history purge/page.md
  revision: sha256:3d8d4c644470c27470ea197260bf4b2d1f0b881eee3860039068590141320ae9
  sha256: 3d8d4c644470c27470ea197260bf4b2d1f0b881eee3860039068590141320ae9
generated:
  by: agent:sol-auto-netting-review
  at: '2026-11-16T09:23:59.420945+08:00'
verified: []
scope: Historical selected-source design for platform cashflow data query.
components:
- Query read model and history projection
- Rule-owned logical mapping and foundation transformer
- GraphQL aggregation
- Notification and dashboard projections
interfaces:
- Cashflow and detail GraphQL queries
- Per-cashflow change notices
- Dashboard and exception-code query APIs
dependencies:
- Domain cashflow events
- Rule, SSI, exception, and trade sources
- Authorized data-entitlement evaluation
decisions:
- Model query fields centrally and keep unresolved mappings explicit.
- Partial errors retain requested paths; final empty-value contract remains unresolved.
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# Platform cashflow data query

## Scope

Historical selected-source design for platform cashflow data query.

## Components

- Query read model and history projection
- Rule-owned logical mapping and foundation transformer
- GraphQL aggregation
- Notification and dashboard projections

## Interfaces

- Cashflow and detail GraphQL queries
- Per-cashflow change notices
- Dashboard and exception-code query APIs

## Dependencies

- Domain cashflow events
- Rule, SSI, exception, and trade sources
- Authorized data-entitlement evaluation

## Decisions

- Model query fields centrally and keep unresolved mappings explicit.
- Partial errors retain requested paths; final empty-value contract remains unresolved.

## Documented knowledge

### Query modeling responsibilities

The GraphQL principle models UI query use cases before implementation and uses standard logical-model or RATAN extension terms.
Rule service owns supported fields and versioned logical-to-XPath mappings by context.
The foundation SDK transforms SCBML into logical JSON; query uses JSONB instead of a separate local XPath map.
Optional mapping retrieval, hourly caching, and version events remain optional.

An aggregation component with performance problems can become a separate API.
Query performance needs monitoring.

Sources: [original lines 15–53](../../../evidence/sources/sha256/4b916ca3d1a43de7b1c3627c8eb2a70b4a7caef434569ea715ebd11cdecf16f9.md#L15-L53), [original lines 3–16](../../../evidence/sources/sha256/e6fae5521783aec72bda7d252c61aedaf723f2d35d0abcfb9200002b17bb61bd.md#L3-L16).

### Read model and mapping limits

The query design defines current and history storage for cashflow, trade, entity, portfolio, SSI, event, and audit fields.
Its example cashflowsNew response has page metadata and nested logical-model result sections.
The physical mapping replaces dots with double underscores, replaces Settlement_Instruction with ssi, and lowercases names.
The mapping table marks duplicate/unused physical fields and missing instrument fields as unresolved.

The source examples do not supply a single approved typed/nullability contract across GraphQL and storage.
No marked field is authorized for removal by this record.

Sources: [original lines 1–5](../../../evidence/sources/sha256/752edd6f465190c725f7440244fe3f42c251593a755d55dbfbcbfa0e7d34ee83.md#L1-L5), [original lines 7–244](../../../evidence/sources/sha256/752edd6f465190c725f7440244fe3f42c251593a755d55dbfbcbfa0e7d34ee83.md#L7-L244), [original lines 1–337](../../../evidence/sources/sha256/15126a1e95e2e319c486757ef75d9a90811a438ef49d5e07e242fad63f9cfff3.md#L1-L337), [original lines 18–182](../../../evidence/sources/sha256/e6fae5521783aec72bda7d252c61aedaf723f2d35d0abcfb9200002b17bb61bd.md#L18-L182).

### Cashflow notification behavior

The notice model includes cashflow ID, business/version/minor versions, status, eventAction, and cashflow data.
The UI requirement auto-refreshes the blotter and highlights new records without a list-level popup.
It says open details prompt Y/N: No closes details; Yes reopens the latest version with current actions.
A later approach instead requires an action-blocking Refresh-only overlay for details.

These are conflicting interaction proposals.
Notifications include entitlement filtering and full data, with UI-side search/sort filtering.
The later approach compares cashflow, business, and minor versions before refreshing details.

Sources: [original lines 1–15](../../../evidence/sources/sha256/1dcb5bb3c3869392848262ba9eb1960c462585f6ba0c29d661bf1ef5ca9c511e.md#L1-L15), [original lines 197–225](../../../evidence/sources/sha256/1dcb5bb3c3869392848262ba9eb1960c462585f6ba0c29d661bf1ef5ca9c511e.md#L197-L225).

### Dashboard and exception projections

The dashboard requirement counts statuses in real time, refreshes on status changes, and drills into cashflows on selection.
Filter values are alphabetically sorted.
QUEUED covers the next five business days.
Top exposure includes only the specified outstanding WAITING, ERROR, QUEUED, READY, HOLD, NACK, and FAILED states.

The Friday VD-1 bucket includes Saturday, Sunday, and Monday under the stated requirement.
All exceptions remain accessible with scrolling.
The NSTP design adds exception data to current/history models and requests codes by cashflow ordered by exception time.
Its proposed exception-code API accepts statuses and returns label, value, and category.

Event-trigger coverage and the relationship to existing NSTP reason/code fields remain open.

Sources: [original lines 1–10](../../../evidence/sources/sha256/ed8d144c7e9f9aede3db78105e91e89491b144d90ce28964eda1f9153118710e.md#L1-L10), [original lines 18–83](../../../evidence/sources/sha256/ed8d144c7e9f9aede3db78105e91e89491b144d90ce28964eda1f9153118710e.md#L18-L83), [original lines 1–9](../../../evidence/sources/sha256/e0cd1c6713e36a098bfaf4ec60234a20eb73d84a89acd01d5549c88bdcf94527.md#L1-L9), [original lines 66–69](../../../evidence/sources/sha256/e0cd1c6713e36a098bfaf4ec60234a20eb73d84a89acd01d5549c88bdcf94527.md#L66-L69), [original lines 85–91](../../../evidence/sources/sha256/e0cd1c6713e36a098bfaf4ec60234a20eb73d84a89acd01d5549c88bdcf94527.md#L85-L91).

### Aggregation and partial error contract

The proposal aggregates cashflow details, exceptions, stashed maker input, SSI candidates, affirmation metadata, and assigned SSI.
Its size-based timing table is proposed guidance, not an accepted SLA.
Partial failures retain field keys/paths with empty values.
Retries request only failed paths.

The selected material does not define empty-value typing or a complete full-failure response.
The 2025 schema proposal adds cashflow/group counts, top exposure, exception statistics, and currency-to-USD rate queries.
Netting preview and execution are listed, without their schema bodies.

Sources: [original lines 1–3](../../../evidence/sources/sha256/bdf6eee37dcea57a2bc7c10a997f91b6026610ef8997baf0ff49fcc915299a50.md#L1-L3), [original lines 15–28](../../../evidence/sources/sha256/bdf6eee37dcea57a2bc7c10a997f91b6026610ef8997baf0ff49fcc915299a50.md#L15-L28), [original lines 37–43](../../../evidence/sources/sha256/bdf6eee37dcea57a2bc7c10a997f91b6026610ef8997baf0ff49fcc915299a50.md#L37-L43), [original lines 62–85](../../../evidence/sources/sha256/bdf6eee37dcea57a2bc7c10a997f91b6026610ef8997baf0ff49fcc915299a50.md#L62-L85), [original lines 97–111](../../../evidence/sources/sha256/bdf6eee37dcea57a2bc7c10a997f91b6026610ef8997baf0ff49fcc915299a50.md#L97-L111), [original lines 1–35](../../../evidence/sources/sha256/6acb86fee2fa59a8e9efa181f2491804cb9bba5b16231bc08eaa439e9ba3ab05.md#L1-L35).

### History slimming proposal

The purge plan retains direct JSONB slimming and temporary-table/rename alternatives.
Its chosen temporary-table form preserves entity columns while keeping only selected JSON content populated.
Retained JSON keys include identity/version/status, payment date, netting/splitting IDs, and NSTP exception data.
The source still marks netting and splitting IDs to be added.

It requires null-safety, data-processing compatibility, and script-duration checks before adoption.
This proposal does not authorize deletion or establish complete audit/history retention.

Sources: [original lines 1–8](../../../evidence/sources/sha256/3d8d4c644470c27470ea197260bf4b2d1f0b881eee3860039068590141320ae9.md#L1-L8), [original lines 237–259](../../../evidence/sources/sha256/3d8d4c644470c27470ea197260bf4b2d1f0b881eee3860039068590141320ae9.md#L237-L259), [original lines 494–494](../../../evidence/sources/sha256/3d8d4c644470c27470ea197260bf4b2d1f0b881eee3860039068590141320ae9.md#L494-L494), [original lines 496–501](../../../evidence/sources/sha256/3d8d4c644470c27470ea197260bf4b2d1f0b881eee3860039068590141320ae9.md#L496-L501).

## Connections

Relationships describe the named design responsibilities.
No uninspected canonical relationships are asserted.

## Evidence limits

Historical documents and proposals do not establish current approved behavior.
No implementation, live service, deployment, or business execution was verified.
Excluded page content and unavailable attachments remain unreviewed.

## Open questions

Owner: unknown.

- Which typed query model, mapping version, and duplicate/missing-field disposition are approved?
- Which open-details refresh interaction, entitlement/filter path, and dashboard calendar rules are approved?
- Which partial/full GraphQL error shape, numerical SLA, and history-retention/slimming acceptance apply?
