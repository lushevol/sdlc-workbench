---
type: KnowledgeTopic
id: KT-static-config-governance-p3
version: 2
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/RATANONE
    Cash Settlement Technical Design/Self Service new branch entity onboarding Design/page.md
  revision: sha256:2271f4dca3928dc2c6a8d4839de9f295ec5cae1f00275f42d5692863667cee82
  sha256: 2271f4dca3928dc2c6a8d4839de9f295ec5cae1f00275f42d5692863667cee82
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/RATANONE
    Cash Settlement Technical Design/Static configuration design/page.md
  revision: sha256:10b1d8cce5b25b05f3cc67de524008a8c130a37cf91b7b6d6aa48073f280e95d
  sha256: 10b1d8cce5b25b05f3cc67de524008a8c130a37cf91b7b6d6aa48073f280e95d
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Ratan
    Static Config Service Design (Draft)/page.md
  revision: sha256:a6712b3ee4cbc0ae4af541199f3f681090c8df1a2ae9920175001ec0608c5166
  sha256: a6712b3ee4cbc0ae4af541199f3f681090c8df1a2ae9920175001ec0608c5166
generated:
  by: agent:sol-auto-netting-review
  at: '2026-11-16T09:29:53.328447+08:00'
verified: []
scope: Historical selected-source design for static config governance p3.
classification: operations
summary: The selected documents define historical intent and proposals. Current authority
  and applicability remain unresolved.
related: []
open_questions:
- Which onboarding architecture and configuration-store contract are approved, and
  for which configuration families?
- Which maker/checker permissions, validations, approval boundaries, and audit retention
  govern each configuration family?
- Which pending-versus-effective-data behavior and cache freshness guarantees must
  existing consumers retain?
- Do blacklist, low-frequency configuration, and batch onboarding fall within self-service
  scope?
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# Static config governance p3

## Scope

Historical selected-source design for static config governance p3.

## Summary

The selected documents define historical intent and proposals. Current authority and applicability remain unresolved.

## Documented knowledge

### Self-service onboarding objective

The onboarding requirement lets users add branches or entities through the UI blotter.
It requires onboarding without a production code deployment.
Mutable frontend and backend configuration moves into databases or a configuration server.

Sources: [original lines 11–17](../../../evidence/sources/sha256/2271f4dca3928dc2c6a8d4839de9f295ec5cae1f00275f42d5692863667cee82.md#L11-L17).

### Alternative onboarding responsibilities

The design offers service-owned blotters backed by databases and optionally a configuration server.
Another option uses one aggregated blotter and static-data service with Kafka distribution to service-owned tables.
A fourth option imports entity spreadsheets through the blotter.
The selected document does not establish a final architecture choice.

The configuration scope spans entity lists, currency, rounding, BIC, accounting, cutoff, and orchestration filters.

Sources: [original lines 19–75](../../../evidence/sources/sha256/2271f4dca3928dc2c6a8d4839de9f295ec5cae1f00275f42d5692863667cee82.md#L19-L75), [original lines 95–118](../../../evidence/sources/sha256/2271f4dca3928dc2c6a8d4839de9f295ec5cae1f00275f42d5692863667cee82.md#L95-L118), [original lines 183–209](../../../evidence/sources/sha256/2271f4dca3928dc2c6a8d4839de9f295ec5cae1f00275f42d5692863667cee82.md#L183-L209).

### Configuration management and audit intent

The configuration design requires filtered fetch APIs for consumers.
Its UI requirements include search, maker create/update/delete, checker confirm/cancel, and audit history.
A shared workflow proposal separates maker requests and audit snapshots from effective configuration tables.
Other options use unified JSON or metadata-driven value tables.

These are alternatives, not an approved common storage contract.

Sources: [original lines 7–10](../../../evidence/sources/sha256/10b1d8cce5b25b05f3cc67de524008a8c130a37cf91b7b6d6aa48073f280e95d.md#L7-L10), [original lines 75–173](../../../evidence/sources/sha256/10b1d8cce5b25b05f3cc67de524008a8c130a37cf91b7b6d6aa48073f280e95d.md#L75-L173).

### Proposed shared management interface

The shared API proposal uses /v1/static/config/{target_table}.
It defines create, update, delete, cancel, approve, and reject operations.
It provides paginated audit logs through /v1/static/config-audit-logs/{target_table}.
Feature-specific fetch APIs remain independently defined.

The source identifies separation of pending requests and effective records as a proposed UI change.

Sources: [original lines 190–254](../../../evidence/sources/sha256/10b1d8cce5b25b05f3cc67de524008a8c130a37cf91b7b6d6aa48073f280e95d.md#L190-L254).

### Versioned generic configuration draft

The static-config draft requests mutable database-backed values, query by name or domain, version control, and audit.
Its model separates configuration, configuration content, and audit entries.
JSON Schema defines content validation.
Booking-entity examples distinguish NORMAL, STRATEGIC, and CPT flow types.

These examples do not approve the illustrated entities for onboarding.

Sources: [original lines 38–52](../../../evidence/sources/sha256/a6712b3ee4cbc0ae4af541199f3f681090c8df1a2ae9920175001ec0608c5166.md#L38-L52), [original lines 56–100](../../../evidence/sources/sha256/a6712b3ee4cbc0ae4af541199f3f681090c8df1a2ae9920175001ec0608c5166.md#L56-L100), [original lines 119–133](../../../evidence/sources/sha256/a6712b3ee4cbc0ae4af541199f3f681090c8df1a2ae9920175001ec0608c5166.md#L119-L133).

### Proposed frontend freshness behavior

The draft cache-first hook returns cached configuration while requesting the latest values.
Without cached data, dependent components wait for the latest response.
Normal mode depends on the latest configuration.
Backend cache behavior and realtime subscriptions remain incomplete.

Sources: [original lines 142–177](../../../evidence/sources/sha256/a6712b3ee4cbc0ae4af541199f3f681090c8df1a2ae9920175001ec0608c5166.md#L142-L177).

## Connections

Relationships describe the named design responsibilities.
No uninspected canonical relationships are asserted.

## Evidence limits

Historical documents and proposals do not establish current approved behavior.
No implementation, live service, deployment, or business execution was verified.
Excluded page content and unavailable attachments remain unreviewed.

## Open questions

Owner: unknown.

- Which onboarding architecture and configuration-store contract are approved, and for which configuration families?
- Which maker/checker permissions, validations, approval boundaries, and audit retention govern each configuration family?
- Which pending-versus-effective-data behavior and cache freshness guarantees must existing consumers retain?
- Do blacklist, low-frequency configuration, and batch onboarding fall within self-service scope?
