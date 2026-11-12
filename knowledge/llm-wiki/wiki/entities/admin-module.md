---
sources: ["summaries/KT-authentication-and-sessions.md", "summaries/KT-release-operations.md", "summaries/KT-admin-and-onboarding.md"]
type: "Product"
description: "Portal product where tenant catalog configuration (module map, drawer, tile) is uploaded and promoted across environments."
---

> Derived candidate/draft knowledge; publication review remains pending. [Canonical source bindings](../../source-manifest.json).

# Admin Module

The Admin Module is the [[entities/fmo-post-trade-portal]] product area where tenant catalog configuration is maintained and promoted from Development to UAT and Production. It is documented in the release-flow and checklist material summarized in [[summaries/KT-release-operations]].

## What it covers

The module manages Module Map, Drawer Category, and Tile Configuration records — the catalog inputs behind [[concepts/admin-catalog-configuration]] and the tile-level behavior described in [[concepts/portal-tile-workspace-model]].

The current user-stated access rule permits portal administrators to read every tenant's audit history and configuration. A tile must never reference another tile's metadata. [[concepts/maker-checker-verification-workflow]] describes the separate write and verification process. Cross-tenant write permissions and the classification of shared catalog records remain open. [ADMIN-CROSS-TENANT-READ-AC-001](../../../candidates/operations/KT-admin-and-onboarding.md#admin-cross-tenant-read-ac-001) · [ADMIN-TILE-METADATA-AC-001](../../../candidates/operations/KT-admin-and-onboarding.md#admin-tile-metadata-ac-001)

## Documented release flow

1. Teams make Module Map, Drawer Category, and Tile Configuration changes in Development.
2. Teams export those records as CSV files and retain them in a tenant-owned repository.
3. An ADO pipeline uploads the configuration to the Portal Admin service at `/api/auth/v1/fmo/admin/config/upload`.
4. The flow states that the service validates an [[entities/fmaa]] JWT before processing the CSV files.

The first bulk insert into UAT and Production uses a separate [[entities/single-ui-bff]] release. Later uploads depend on tenant connectivity to the Admin service, which makes the workflow part of [[concepts/configuration-promotion]] and of [[concepts/tenant-production-readiness]].

## Constraints and open issues

The Admin Module release checklist is explicitly under construction. It adds SDK validation, shared frontend requests, entitlement checks, disaster recovery, and performance inputs, and flags a planned [[entities/fmaa]] decommissioning. That warning leaves the documented JWT validation step without a confirmed replacement path.

## Ownership

Portal teams execute Portal releases and routing rollback; tenant teams validate their applications and support tenant issues, as recorded for the [[entities/portal-team]] boundary. Current approval of these responsibility statements is unconfirmed, and the supplied material does not establish which checklist or deployment process governs each environment.

## Evidence limits

No configuration upload, pipeline run, or rollback was executed during ingestion. Local hashes identify the supplied bytes only; original page revisions and human approval remain unconfirmed.

See also: [[summaries/KT-authentication-and-sessions]]
