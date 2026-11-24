---
type: KnowledgeTopic
id: KT-static-config-governance-p3
version: 3
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
  by: agent:sol_complete_sources
  at: '2026-11-16T07:53:29.508381+00:00'
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
previous_version: 2
previous_content_sha256: 3f5b21821848b3a654b8df0ff2ebcf65da2d2930612cf7ba28a2d0a9b4470c93
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

### Versioned generic-configuration field contracts

The draft assumes that static-data-service can expose GraphQL queries. It separates UI-only configuration from configuration shared across applications.
Its examples distinguish low-frequency operator mappings from frequently changed booking-entity configuration.
These are draft scope declarations. Populated booking entities and operator examples remain source context.

| Draft table | Mandatory fields | Optional fields |
| --- | --- | --- |
| Config | id, context, state, version | domain, schema |
| Config content | id, context, key, value, state, version | type, sub_type, metadata |

The config fields use VARCHAR. Its state values are LIVE and DISABLED, and domain permits comma-separated names.
Content fields use VARCHAR except integer version. Its key must be unique within context.
Content state values are LIVE, DISABLED, UPDATE_PENDING, DEAD and ADD_PENDING.

Metadata normally contains JSON text. The optional schema field uses JSON Schema to validate content.

The audit table records config/content identifiers, context/domain, state, key/value/type, metadata/schema, version, updated_at and updated_by.
It shows integer audit version and VARCHAR for the other fields. Its table supplies no mandatory-column declaration.
Audit states are UPDATE, ADDED, DELETED, PENDING_UPDATE, PENDING_ADDED and PENDING_DELETED.

The differing version types remain source-specific declarations, pending a selected storage contract.

The operator example requires key and value and rejects additional properties. Its schema calls value a string while examples show arrays.
The booking-entity example requires key, value, type and metadata. It rejects additional properties and restricts type to NORMAL, STRATEGIC or CPT.
Its metadata object can hold country. These examples establish no approved entity inventory or resolved operator-value type.

The proposal offers API or GUI management. Its illustrated fetch uses POST /api/ratan/staticconfig.
The hook example returns totalResults and results. Plain API callers handle cache and loading themselves.
The cache-first hook returns cached values immediately, requests the latest values and returns them when ready.

Without cache, dependent components wait for the latest response while the cache is populated.
The feature-flag use case requests realtime reaction to changes. Protocol, timing and backend cache behavior remain incomplete.
[Selected original lines 3–52](../../../evidence/sources/sha256/a6712b3ee4cbc0ae4af541199f3f681090c8df1a2ae9920175001ec0608c5166.md#L3-L52) [Selected original lines 56–177](../../../evidence/sources/sha256/a6712b3ee4cbc0ae4af541199f3f681090c8df1a2ae9920175001ec0608c5166.md#L56-L177)

### Historical self-service onboarding option details

The first option uses service-oriented blotters with database and configuration-server storage.
The second uses service-oriented blotters and database storage. Both retrieve frontend configuration through service APIs.
The third uses one aggregated blotter and static-data-service storage, then distributes configuration through Kafka to consumer-owned tables.

The fourth uploads entity spreadsheets and downloads add/update/delete templates plus result spreadsheets.
That fourth option parses uploaded data into different database schemas.
It requires configuration-server hot updates when application.yml values remain outside database storage.

The design proposes country, entity and common-metadata dictionaries for shared frontend configuration.
The database options also name ISO-currency mappings and Swift MX-generation conditions.
Its aggregated option adds entity-onboarding configuration and synchronization-result tables.

Source table-name spelling varies across option lists. The document selects no single authoritative schema.

The following destinations apply to database-based migration alternatives.

| Configuration | Proposed migration destination |
| --- | --- |
| Entity selectors and branch mappings | Entity configuration. |
| Currency and settlement-means selectors | Common metadata. |
| Country/region and accounting timezone mappings | Country configuration. |
| Swift MX entity-scope conditions | Swift MX-generation-condition data. |
| Orchestration STRATEGIC_FM_LIST | Common metadata in the database options. |

The remaining scope includes rounding, correspondent/sender BIC, bridge flows/accounts, transaction codes and currency cutoffs.
Its service-blotter options add CRUD and audit behavior for those configuration families.
Its aggregate option centralizes onboarding CRUD/audit and distributes service-owned values through Kafka.

The closing task list proposes FMID filtering in orchestration, configuration-fetch APIs and accounting cron-job changes.
Blacklists, rarely changed values, batch onboarding and FMID-to-branch mapping remain unresolved in the source.
[Selected original lines 3–209](../../../evidence/sources/sha256/2271f4dca3928dc2c6a8d4839de9f295ec5cae1f00275f42d5692863667cee82.md#L3-L209) [Selected original lines 421–483](../../../evidence/sources/sha256/2271f4dca3928dc2c6a8d4839de9f295ec5cae1f00275f42d5692863667cee82.md#L421-L483)

### Shared maker-checker workflow and effective data contract

The intended fetch behavior returns the previous effective configuration while a maker's update awaits checker approval.
The source proposes separating pending requests from effective records in the UI to support pagination.
It requests reusable maker/checker status, validation and audit handling, with independently defined feature fetch APIs.

Current Nostro/BIC implementation differences and reported defects remain source-reported context, outside newly derived target behavior.

The separated-table option stores maker requests with target table/id, operation, payload, maker/checker identifiers and timestamps.
Its declared operation values are insert, update and delete. Request states are pending, confirmed, rejected and cancelled.
The sample requires maker_id, target_table, operation_type, data_status and payload. It leaves checker_id and target_id nullable.

The audit proposal stores operator, role, operation, target table/id, target snapshot and creation time.
Its sample requires operator, role, operation_type, target_table and target_snapshot, while target_id remains nullable.
The samples use timestamp defaults for creation and update fields. These are proposed schema contracts.

The selected DDL remains the exact field-type and nullability catalog for this proposed model.

Alternative storage uses unified JSON or metadata-driven value tables with type, format and mandatory descriptors.
Those options retain audit snapshots. The comparison discusses validation, database constraints, custom UI behavior and manual import/export tradeoffs.
Its effort estimates and current-implementation comparisons remain retained evaluation context. They select no approved architecture.

| Action | Proposed HTTP interface |
| --- | --- |
| List requests | GET /v1/static/config/{target_table} |
| Maker create | POST /v1/static/config/{target_table} |
| Maker update | POST /v1/static/config/{target_table}/{target_id}/update |
| Maker delete | POST /v1/static/config/{target_table}/{target_id}/delete |
| Maker cancel | POST /v1/static/config/{target_table}/{target_id}/cancel |
| Checker confirm | POST /v1/static/config/{target_table}/{target_id}/approve |
| Checker reject | POST /v1/static/config/{target_table}/{target_id}/reject |
| Audit list | GET /v1/static/config-audit-logs/{target_table}?page=0&size=5 |

The create and update examples supply configuration payloads. Feature-specific fetch APIs remain independently implemented.
The requirements name checker confirm/cancel, while the API section names maker cancel and checker reject.
That role/action wording difference remains unresolved. It grants no current maker/checker permissions.
[Selected original lines 1–254](../../../evidence/sources/sha256/10b1d8cce5b25b05f3cc67de524008a8c130a37cf91b7b6d6aa48073f280e95d.md#L1-L254)

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
