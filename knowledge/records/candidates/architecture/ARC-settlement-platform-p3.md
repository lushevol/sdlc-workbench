---
type: Architecture
id: ARC-settlement-platform-p3
version: 2
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Cash
    Settlement Data Store Requirements/page.md
  revision: sha256:975e93f47e78a5169dc1924552a681cd48105628f8933cf045863bef60e18ed5
  sha256: 975e93f47e78a5169dc1924552a681cd48105628f8933cf045863bef60e18ed5
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Cash
    Settlement Platform - Co-development Guideline/page.md
  revision: sha256:e83e47b47ab92a185a1e0b6ecfd22e31d734cc6b6ba838b5e1a9600074a385ad
  sha256: e83e47b47ab92a185a1e0b6ecfd22e31d734cc6b6ba838b5e1a9600074a385ad
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Cash
    Settlement System Design/page.md
  revision: sha256:90c928350263c632830707d008e0c835ff478a0bfd669b8b2033fd4e893b3bd8
  sha256: 90c928350263c632830707d008e0c835ff478a0bfd669b8b2033fd4e893b3bd8
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/RATANONE
    Cash Settlement Technical Design/page.md
  revision: sha256:600da2fa0ed91bc2bd0a3ca531fb206b872edf82b125339a91c7149de13791ec
  sha256: 600da2fa0ed91bc2bd0a3ca531fb206b872edf82b125339a91c7149de13791ec
generated:
  by: agent:sol-auto-netting-review
  at: '2026-11-16T09:16:56.022208+08:00'
verified: []
scope: Historical selected-source design for settlement platform p3.
components:
- Group management and standardization
- Lifecycle write model and status machine
- Camunda orchestration
- Rule, netting, and SSI services
- Query read model and external interfaces
interfaces:
- Upstream cashflow and trade events
- Domain status and query APIs
- Downstream settlement and accounting publication
dependencies:
- PostgreSQL business schemas
- Shared messaging, cache, discovery, gateway, and authentication infrastructure
decisions:
- Historical design separates orchestration, processing state, and read queries.
- Current component and infrastructure applicability remains unresolved.
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# Settlement platform p3

## Scope

Historical selected-source design for settlement platform p3.

## Components

- Group management and standardization
- Lifecycle write model and status machine
- Camunda orchestration
- Rule, netting, and SSI services
- Query read model and external interfaces

## Interfaces

- Upstream cashflow and trade events
- Domain status and query APIs
- Downstream settlement and accounting publication

## Dependencies

- PostgreSQL business schemas
- Shared messaging, cache, discovery, gateway, and authentication infrastructure

## Decisions

- Historical design separates orchestration, processing state, and read queries.
- Current component and infrastructure applicability remains unresolved.

## Documented knowledge

### Strategic service responsibilities

The strategic design assigns cashflow creation, lifecycle, materialization, netting, and fail/reinstate to RATAN.
Its comparison retains different historical BCS/EG responsibilities and product scope.
Group management assembles complete groups, handles validation/confirmation, standardizes cashflows, and writes status upstream.
Camunda orchestrates STP, multi-exception maker/checker processing, and technical failures.

Lifecycle owns processing storage and single or transactional batch status changes.
Rules own configuration and execution; netting owns component validation and resultant creation.
SSI owns stamping and related exceptions; query owns event-driven read storage and UI/external query interfaces.
The table marks some split, auto-netting, and non-economic handling as future scope, without establishing their current absence.

Sources: [original lines 1–45](../../../evidence/sources/sha256/600da2fa0ed91bc2bd0a3ca531fb206b872edf82b125339a91c7149de13791ec.md#L1-L45).

### Persistence and audit boundaries

The storage requirements choose PostgreSQL with separate schemas for business-domain services.
They include payment/history, suppression, SSI, SWIFT, workflow, exceptions, audit, login/logout audit, and customized views.
Suppression rules and customized views have stated forever retention; other retention fields are blank.
The requirements demand replication, transparent recovery, and real-time consistency without measurable bounds.

The strategic table assigns read history/events to query, stamping/audit/outbox data to SSI, group/mapping histories to grouping, and lifecycle status/message histories to lifecycle.
It separately names LMS, adaptor, exception-platform, and FX-utilization storage.
These declared table responsibilities are not verified database inventories.

Sources: [original lines 1–25](../../../evidence/sources/sha256/975e93f47e78a5169dc1924552a681cd48105628f8933cf045863bef60e18ed5.md#L1-L25), [original lines 183–201](../../../evidence/sources/sha256/975e93f47e78a5169dc1924552a681cd48105628f8933cf045863bef60e18ed5.md#L183-L201), [original lines 49–84](../../../evidence/sources/sha256/600da2fa0ed91bc2bd0a3ca531fb206b872edf82b125339a91c7149de13791ec.md#L49-L84).

### Shared infrastructure agreement and limits

The co-development notes agree shared Kafka, Redis, ELK, servers, PostgreSQL, foundation services, and CI/CD.
They favor Spring Boot/Cloud and reusable Camunda orchestration.
Domain work can focus on business logic before archetypes are available.
The notes retain alternative cluster layouts and unresolved PSS and availability coordination.

The system-design inventory labels common, BAU, and CN services but leaves responsibility cells blank.
Its links to SSDR query and cache design do not establish those linked contracts.

Sources: [original lines 1–9](../../../evidence/sources/sha256/e83e47b47ab92a185a1e0b6ecfd22e31d734cc6b6ba838b5e1a9600074a385ad.md#L1-L9), [original lines 13–16](../../../evidence/sources/sha256/e83e47b47ab92a185a1e0b6ecfd22e31d734cc6b6ba838b5e1a9600074a385ad.md#L13-L16), [original lines 20–22](../../../evidence/sources/sha256/e83e47b47ab92a185a1e0b6ecfd22e31d734cc6b6ba838b5e1a9600074a385ad.md#L20-L22), [original lines 24–26](../../../evidence/sources/sha256/e83e47b47ab92a185a1e0b6ecfd22e31d734cc6b6ba838b5e1a9600074a385ad.md#L24-L26), [original lines 34–36](../../../evidence/sources/sha256/e83e47b47ab92a185a1e0b6ecfd22e31d734cc6b6ba838b5e1a9600074a385ad.md#L34-L36), [original lines 47–48](../../../evidence/sources/sha256/e83e47b47ab92a185a1e0b6ecfd22e31d734cc6b6ba838b5e1a9600074a385ad.md#L47-L48), [original lines 59–59](../../../evidence/sources/sha256/e83e47b47ab92a185a1e0b6ecfd22e31d734cc6b6ba838b5e1a9600074a385ad.md#L59-L59), [original lines 71–83](../../../evidence/sources/sha256/e83e47b47ab92a185a1e0b6ecfd22e31d734cc6b6ba838b5e1a9600074a385ad.md#L71-L83), [original lines 3–33](../../../evidence/sources/sha256/90c928350263c632830707d008e0c835ff478a0bfd669b8b2033fd4e893b3bd8.md#L3-L33), [original lines 65–77](../../../evidence/sources/sha256/90c928350263c632830707d008e0c835ff478a0bfd669b8b2033fd4e893b3bd8.md#L65-L77).

## Connections

Relationships describe the named design responsibilities.
No uninspected canonical relationships are asserted.

## Evidence limits

Historical documents and proposals do not establish current approved behavior.
No implementation, live service, deployment, or business execution was verified.
Excluded page content and unavailable attachments remain unreviewed.

## Open questions

Owner: unknown.

- Which effective service boundary, retention policy, consistency target, and shared-infrastructure layout are approved?
