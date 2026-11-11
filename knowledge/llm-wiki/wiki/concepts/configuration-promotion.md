---
type: "Concept"
sources: ["summaries/KT-release-operations.md"]
description: "Moving Portal catalog and tile configuration from Development to UAT and Production."
---

> Derived candidate/draft knowledge; publication review remains pending. [Canonical source bindings](../../source-manifest.json).

# Configuration Promotion

## Definition

Configuration promotion is the controlled movement of Portal catalog and tile records from Development into UAT and Production. The records include Module Map entries, Drawer Categories, and Tile Configuration. Promotion makes tenant tiles visible in the Portal workspace, so it connects catalog definition to [[concepts/portal-entry-and-tile-authorization]].

## Documented flow

The supplied guide describes these steps:

1. Teams change Module Map, Drawer Category, and Tile Configuration records in Development.
2. Teams export the records as CSV files.
3. Teams keep the CSV files in a tenant-owned repository.
4. An ADO pipeline uploads the configuration to the Portal Admin service.
5. The documented upload interface is `/api/auth/v1/fmo/admin/config/upload`.
6. The flow states that the service validates an [[entities/fmaa]] JWT before it processes CSV files.

The first bulk insert into UAT and Production uses a separate [[entities/single-ui-bff]] release. Later uploads depend on tenant connectivity to the Admin service. The [[entities/admin-module]] holds the configuration that teams promote.

This page describes the documented procedure. The ingestion inspected no upload execution.

## Dependencies and risks

The release checklist flags planned [[entities/fmaa]] decommissioning. That warning creates an unresolved dependency for the documented promotion workflow. A replacement authentication mechanism is not identified in the supplied materials. This dependency differs from runtime [[concepts/identity-provider-delegation]], which concerns user sign-in rather than pipeline authentication.

Later uploads also depend on network access from the tenant environment to the Portal Admin service. The production checklist recommends Portal connections through tenant [[entities/nginx]] or load balancers. Tenant teams then control internal server and port changes behind that boundary. These are separate checks; a successful configuration upload alone does not establish business readiness.

## Relationship to other concepts

- [[concepts/admin-catalog-configuration]] defines the catalog and tile records that teams promote.
- [[concepts/portal-entry-and-tile-authorization]] describes the visible effect of promoted records.
- [[concepts/release-window-governance]] controls when promotion and release activity may occur.
- [[concepts/tenant-production-readiness]] requires separate evidence for technical deployment and business activation.
- [[concepts/single-ui-sdk-authentication]] and [[concepts/entitlement-retrieval]] govern user identity and entitlement context at runtime.
- [[concepts/portal-ingress-path]] and [[concepts/application-ownership]] define reachability and responsibility boundaries.

Related registry IDs are `single-ui-importmap-admin`, `single-ui-active-importmap`, and `single-ui-category-tile-admin`. Capability `single-ui-application-catalog` groups that declared context.

## Evidence limits

The flow comes from the Admin Module release guide and the unfinished release checklist. Original page revisions, current authority, and human approval remain unconfirmed. No pipeline, upload, or rollback check ran during ingestion. The guide does not show a completed promotion for any tenant.

## Open questions

| Issue | Consequence | Next action |
| --- | --- | --- |
| Planned FMAA decommissioning has no replacement plan in the supplied copy. | Pipeline authentication continuity is uncertain. | Confirm the replacement mechanism and its owner. |
| The checklist remains under construction. | Promotion prerequisites are uncertain. | Confirm the governing checklist. |
| The first bulk insert depends on a separate BFF release. | Promotion scheduling depends on another release. | Confirm the BFF release dependency and order. |
| No upload execution evidence is retained. | A completed upload cannot be proven. | Retain pipeline logs and validation results per environment. |

See [[summaries/KT-release-operations]] for the full source summary.