---
type: "Summary"
description: "Links onboarding, admin catalog setup, EMS2 roles, and maker-checker review."
doc_type: short
full_text: "sources/KT-admin-and-onboarding.md"
---

> Derived from [KT-admin-and-onboarding, version 3](../../../candidates/operations/KT-admin-and-onboarding.md), candidate/draft. [Source bindings](../../source-manifest.json).

# Admin and onboarding — Summary

**Source:** `KT-admin-and-onboarding` (KnowledgeTopic v3, draft/candidate, owner unknown). This page summarizes the topic; it does not confirm that any described procedure is currently deployed or approved.

## Core idea

Tenant onboarding is a cross-team operation. An application needs frontend assets, backend routing, EMS2 entitlements, and portal catalog records before it can appear and launch for a tenant. The topic centers on the [[entities/fmo-post-trade-portal]] admin module and connects the frontend and backend onboarding procedures, retained schema and routing material, and the SSDR entitlement discussion. It also records one explicit user clarification about tiles with an empty subject.

## Key findings

### Admin catalog functions

The admin manual describes three functions in the application catalog: Module Mapping, Drawer Category, and Tile Configuration. A module mapping links an import-map module name to an asset path; users enter the name without `@fm/` or spaces, and the active import-map API adds `@fm/` automatically. A drawer category groups tiles. A tile configuration record stores display details, container and route information, and entitlement configuration. Module and tile paths must match routing paths and are entered without a leading slash or spaces. Comma-separated role entities are converted into an array by the API. These functions and their relationships are collected in [[concepts/admin-catalog-configuration]] and [[concepts/portal-tile-workspace-model]].

The manual defines a [[concepts/maker-checker-verification-workflow]]: creation or modification produces an `un-verified` record; a different user checks and verifies it before activation. Deactivation returns a verified record to `un-verified`. Each admin function keeps its own audit history. The supplied text does not fully specify rollback, activation propagation, or concurrent edits.

### Onboarding path

[[concepts/frontend-onboarding]] spans frontend and backend work. The development principle assigns portal-backend availability to the microfrontend team and each application's backend availability to its application team, an [[concepts/application-ownership]] split. Application teams choose their deployment approach and provide static-file and API URLs for NGINX configuration. The frontend procedure starts from separate container and tile templates, updates names, webpack, interfaces, entry points, tests, and the local import map, then links application registration through the admin manual. The backend procedure collects application URLs for proxy and CORS configuration, requires EMS2 role or entitlement setup, and directs services to SDK-based JWT validation and entitlement integration.

### EMS2 and access control

[[entities/ems2]] setup creates an entity, actions, roles, and subjects, then assigns actions to role-and-subject combinations. The admin manual identifies `FMO PORTAL ADMIN` entitlements for import-map, category, and tile functions. These are prerequisites, not evidence that any current operator has been granted access. See [[concepts/ems2-entitlement-provisioning]].

### Persistence and routing context

The Flyway page describes schema-history configuration and baseline migration from version zero. Its SQL defines import-map records with unique keys, categories with unique labels, and tile records that reference both through foreign keys. Separate audit tables preserve change history. These are retained design definitions, not a confirmed deployed schema or executed migration. See [[entities/flyway]].

The NGINX draft collects upstream name, host, port, route path, rewrite rule, protocol, request limits, environment, WebSocket settings, timeouts, load-balancing method, and custom headers. It separates non-production maintenance from UAT and stage work, and mentions configuration testing and rollback as improvement proposals. The firewall register supplies connectivity context. Neither source establishes active routes, current endpoint values, network approvals, or reachability. See [[entities/nginx]] and [[concepts/portal-ingress-path]].

### Empty-subject tile clarification

The explicit user clarification permits tile visibility and launch through one configured EMS2 entity when the tile's subject setting is empty. The user must still satisfy portal-entry requirements and hold entitlement for that entity. The owner and scope answer identifies [[entities/portal-team]] across local, test, UAT, and production. This decision has approval pending. It resolves only the single-entity, empty-subject scope; it does not select a multiple-entity matching rule or an SSDR delegation option. The measurable result is defined in [UI-EMPTY-SUBJECT-AC-001](../../../candidates/security/KT-sdk-and-entitlements.md#ui-empty-subject-ac-001). See [[concepts/portal-entry-and-tile-authorization]].

### SSDR alternatives

The SSDR discussion describes report and download users with different EMS2 entity assignments. It proposes multiple tile entities and optional subject checks for selected tenants; an empty subject would skip validation under that proposal. It also considers adding missing EMS2 assignments or delegating authorization to SSDR. The temporary guest-access approach is struck through. The discussion states that the portal does not implement entitlement control outside existing systems such as EMS2. These are alternatives, not an approved bypass or deployed permission rule.

## Evidence limits

The admin overview and schema are proposals; the user manual is procedural. Their source revisions and current applicability are unconfirmed. The EMS2 page refers to absent entitlement spreadsheets, change attachments, and later setup actions, and the manual depends on screenshots missing from this copy. The Flyway SQL, NGINX draft, and firewall register have no inspected deployment or connectivity execution. Combining these sources cannot establish that proposed controls became production behavior.

## Open questions

- How are tenant record boundaries enforced for maker and checker users? The proposal discusses tenant-specific roles, while the manual lists shared admin subjects and a different-user check.
- Which release, approval, rollback, and emergency-change controls govern self-service configuration changes in production?
- Which SSDR entitlement option and multiple-entity matching rule apply to the current tenant configuration?
- Which source revisions and environment checks establish the deployed catalog schema and current onboarding procedure?

## Related pages

- [[summaries/KT-frontend-composition]] — containers, tiles, routing, and import maps.
- [[summaries/KT-sdk-and-entitlements]] — backend validation and application permissions.
- Authentication and sessions topic — login versus tenant configuration; see [[concepts/single-ui-sdk-authentication]] and [[concepts/cross-application-authentication-handoff]].
- Release operations topic — configuration work and release procedures.
- Capability single-ui-application-catalog and contracts single-ui-importmap-admin, single-ui-active-importmap, and single-ui-category-tile-admin — interface context, not proof of operator permissions or passing maker-checker enforcement.

## Related Concepts
- [[concepts/entitlement-retrieval]]
- [[concepts/microfrontend-layering]]

## Entities
- [[entities/mfe-base]]
- [[entities/single-ui-bff]]
- [[entities/single-ui-sdk]]
- [[entities/mfe-root-config]]
- [[entities/systemjs]]
