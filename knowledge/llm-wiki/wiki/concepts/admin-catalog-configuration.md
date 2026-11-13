---
type: "Concept"
sources: ["summaries/KT-release-operations.md", "summaries/KT-admin-and-onboarding.md"]
description: "Portal admin functions that maintain module mappings, drawer categories, and tiles as versioned configuration"
---

> Derived candidate/draft knowledge; publication review remains pending. [Canonical source bindings](../../source-manifest.json).

# Admin catalog configuration

## Definition

Admin catalog configuration lets an authorized user maintain module mappings, drawer categories, and application tiles without a portal source change for each edit. Each part is an editable record with its own review and audit history.

[[summaries/KT-admin-and-onboarding]] records the procedures for these functions. The [[entities/fmo-post-trade-portal]] provides them. The admin backend uses [[entities/single-ui-bff]].

## Why it exists

The earlier process changed the [[entities/mfe-base]] source for each tile update and then raised a production change request. The admin proposal replaces that repeated release work with tenant-maintained configuration. The proposal does not establish an approved exemption from production change controls. Configuration still crosses environment boundaries, so catalog changes remain within the scope of [[concepts/configuration-promotion]] and [[concepts/release-window-governance]].

## The three functions

### Module mapping

A module mapping connects an [[concepts/frontend-onboarding|import-map module name]] with its asset path. The user enters the module name without the `@fm/` prefix and without spaces. The active import-map API adds `@fm/` automatically. The stored path supplies the import-map value that the browser uses when it loads the module.

### Drawer category

A drawer category groups application tiles into one drawer. Categories have unique labels. The category record controls where the portal shows the group of tiles.

### Tile configuration

A tile record connects display details, container and route information, and entitlement configuration. The fields are:

- Label and description.
- Theme image.
- Container identity and routes.
- Role subjects and role entities.

The module path and the tile path must match the corresponding routing path. The user enters both paths without a leading slash and without spaces. The API converts comma-separated role entities into an array.

The tile record is the catalog side of [[concepts/portal-entry-and-tile-authorization]]. [[concepts/portal-tile-workspace-model]] explains how a launched tile opens in the workspace.

## Review and activation workflow

The manual defines a [[concepts/maker-checker-verification-workflow]]:

1. A maker creates or modifies a record. The record becomes `un-verified`.
2. A different user checks the record and verifies it.
3. The record becomes active.
4. A user can deactivate a verified record. The record returns to `un-verified`.

Each admin function keeps its own audit history. A user can view the history of one record.

The supplied text does not fully specify rollback, activation propagation, or concurrent edits.

## Configuration promotion between environments

[[summaries/KT-release-operations]] documents the promotion flow that moves catalog records between environments. Teams first make Module Map, Drawer Category, and Tile Configuration changes in Development. They export those records as CSV files and retain them in a tenant-owned repository. An ADO pipeline then uploads the configuration to the Portal Admin service at `/api/auth/v1/fmo/admin/config/upload`.

The flow states that the service validates an [[entities/fmaa]] JWT before it processes CSV files. The first bulk insert into UAT and Production uses a separate BFF release. Later uploads depend on tenant connectivity to the Admin service. This describes the documented procedure; no upload execution was inspected during ingestion.

Two dependencies remain open. The release checklist flags planned FMAA decommissioning, which would affect both the upload authentication and the review workflow. The checklist also remains under construction, so the governing prerequisites are unconfirmed. The retained CSV repository becomes the effective version history of the catalog outside the portal audit tables, and it must agree with the portal records.

A successful upload proves neither tile reachability nor business readiness. [[concepts/tenant-production-readiness]] requires separate connectivity, security, and acceptance evidence.

## Access prerequisites

A user needs [[entities/ems2]] entitlements to use these functions. The manual identifies `FMO PORTAL ADMIN` entitlements for the import-map, category, and tile functions. [[concepts/ems2-entitlement-provisioning]] explains how to create the entity, actions, roles, and subjects. These are prerequisites only. They do not show that any current operator has a grant.

Portal administrators can read every tenant's audit history and configuration. A tile must never reference metadata from another tile, including when a portal administrator submits its configuration. The classification of particular category or import-map records as tile-specific or shared remains open. [ADMIN-CROSS-TENANT-READ-AC-001](../../../records/candidates/operations/KT-admin-and-onboarding.md#admin-cross-tenant-read-ac-001) · [ADMIN-TILE-METADATA-AC-001](../../../records/candidates/operations/KT-admin-and-onboarding.md#admin-tile-metadata-ac-001)

## Persistence

The retained SQL defines the catalog tables. Import-map records have unique keys. Categories have unique labels. Tile records reference a category and an import-map record through foreign keys. Separate audit tables keep the change history. [[entities/flyway]] configures the schema-history table and baselines the migration from version zero.

These definitions are retained design material. They do not confirm a deployed schema or an executed migration.

## Relationship to routing

A tile can become visible and launchable only when its container is reachable. [[concepts/portal-ingress-path]] and [[entities/nginx]] describe the proxy route that serves the frontend assets and the application API. The onboarding intake collects the upstream name, host, port, route path, rewrite rule, protocol, environment, timeout values, and custom headers. The catalog record and the proxy route must agree.

## Empty-subject tile policy

One explicit user clarification permits tile visibility and launch through a single configured EMS2 entity when the tile subject setting is empty. The user must still satisfy the portal-entry requirements and hold entitlement for that entity. The [[entities/portal-team]] owns this decision for local, test, UAT, and production. Approval is pending. The decision covers only the single-entity, empty-subject scope. It selects no multiple-entity matching rule and no SSDR delegation option.

## Open questions

- Which cross-tenant write and verification permissions apply to makers and checkers?
- Which release, approval, rollback, and emergency-change rules govern self-service configuration in production? The release proposal contains conflicting duration and urgent-release confirmation rules.
- Which authentication mechanism replaces the FMAA JWT for the upload interface?
- Which source revisions and environment checks establish the deployed catalog schema?
- Which records prove that an uploaded catalog matches the routing and entitlement state of the target environment?

## Evidence limits

The admin overview and the schema draft are proposals. The user manual gives procedures. Their revisions and current applicability are unconfirmed. The manual depends on screenshots that are absent from the copy. The EMS2 page refers to entitlement spreadsheets and change attachments that are also absent. The promotion flow comes from a release-operations topic whose authority is unconfirmed and whose checklist is incomplete. The combined sources cannot show that the proposed controls became production behavior.

## Related pages

- [[summaries/KT-admin-and-onboarding]]
- [[summaries/KT-frontend-composition]]
- [[summaries/KT-sdk-and-entitlements]]
- [[summaries/KT-release-operations]]
- [[concepts/application-ownership]]
- [[concepts/configuration-promotion]]
- [[concepts/frontend-onboarding]]
- [[concepts/portal-entry-and-tile-authorization]]
- [[concepts/maker-checker-verification-workflow]]
- [[concepts/tenant-production-readiness]]
- [[entities/admin-module]]
- [[entities/fmaa]]
