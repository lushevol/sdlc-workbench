---
title: "Admin and onboarding"
type: source
tags: []
sources: []
source_file: raw/workbench/knowledge/candidates/operations/KT-admin-and-onboarding.md
source: raw/workbench/knowledge/candidates/operations/KT-admin-and-onboarding.md
source_hash: 9d397b95e056c25c
last_updated: 2026-11-11
candidate_id: KT-admin-and-onboarding
candidate_version: 3
candidate_governance_state: candidate
candidate_status: draft
candidate_classification: operations
workbench_origin: knowledge/candidates/operations/KT-admin-and-onboarding.md
workbench_sha256: 9d397b95e056c25caf04471930ddb0b84a29c21789e76287576cea33b1ce6869
workbench_status: candidate-derived
---

# Admin and onboarding

## Scope

This topic connects tenant onboarding with module mappings, drawer categories, tile configuration, and EMS2 setup.
It distinguishes an earlier admin proposal from the later procedural manual.
It records documented responsibilities without assigning current owners or claiming executed onboarding.

## Summary

An onboarded application needs frontend assets, backend routing, entitlements, and portal catalog records.
The admin proposal seeks self-service configuration in place of source changes for every tile update.
The manual describes separate maker and checker users, activation, deactivation, and per-record audit history.
The documents do not establish current production authorization or release controls.

## Documented knowledge

### Purpose and component vocabulary

The admin overview describes a previous process that changed `mfe-base` source and raised a production change request.
It proposes tenant-maintained configuration to reduce that repeated release work.
It records reuse of `single-ui-bff` for the admin backend.
The proposal does not establish an approved exemption from production change controls.
[Admin overview, lines 1–37](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/page.md>)

The user manual identifies three admin functions: Module Mapping, Drawer Category, and Tile Configuration.
A module mapping connects an import-map module name with its asset path.
A drawer category groups application tiles.
A tile record connects display details, container and route information, and entitlement configuration.
[Admin user manual, lines 3–35, 49–127, 169–217](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/User Manual/page.md>)

The schema draft separates application categories, application tiles, and tile authorization records.
Its tile authorization records link a tile to EMS2 entities.
These draft relationships explain the design vocabulary, rather than the deployed database schema.
[Admin schema draft, lines 3–60, 99–101](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Table Schema and Screen Draft/page.md>)

### Team responsibilities and onboarding sequence

The development principle assigns portal-backend availability to the microfrontend team.
It assigns each application's backend availability to its application team.
Application teams choose deployment approaches and provide static-file and API URLs for NGINX configuration.
The document also separates feature-branch contribution from shared-repository review and approval responsibilities.
[Development principle, lines 2–10](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Development Principle - Development Guideline - Onboarding Process/Development Principle/page.md>)

The frontend procedure starts from separate container and tile templates.
It updates names, webpack, interfaces, entry points, tests, and the local import map.
It then links application registration through the admin manual.
Each application supplies its build pipeline and informs the portal team about static-file and API URLs.
[Frontend onboarding, lines 1–15](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Development Principle - Development Guideline - Onboarding Process/Frontend Onboarding Process/page.md>)

The backend procedure requests application URLs for proxy configuration and CORS handling.
It requires application role or entitlement setup in EMS2.
It directs services to SDK-based JWT validation and entitlement integration.
Onboarding therefore spans routing, authentication, authorization data, and UI registration.
[Backend onboarding, lines 1–7](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Development Principle - Development Guideline - Onboarding Process/Backend Onboarding Process/page.md>)

The EMS2 procedure creates an entity, actions, roles, and subjects.
It then assigns actions to role-and-subject combinations.
The admin manual identifies `FMO PORTAL ADMIN` entitlements for import-map, category, and tile functions.
These procedures describe prerequisites; they do not establish completed grants for any current operator.
[EMS2 setup procedure, lines 1–12](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Development Principle - Development Guideline - Onboarding Process/Creating EMS2 Entity Role Subject Action/page.md>)
[Admin user manual, lines 3–35, 49–127, 169–217](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/User Manual/page.md>)

### Review and activation workflow

The manual requires different maker and checker users.
Creation and modification produce an `un-verified` record.
Another user checks and verifies that record before activation.
The manual states that each admin function maintains its own audit history.
[Admin user manual, lines 3–35, 49–127, 169–217](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/User Manual/page.md>)

For module mappings, users enter the module name without `@fm/` or spaces.
The manual says the active import-map API adds `@fm/` automatically.
The stored path supplies the import-map value.
These input conventions connect administration with frontend module loading.
[Admin user manual, lines 3–35, 49–127, 169–217](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/User Manual/page.md>)

Tile configuration captures labels, descriptions, theme images, container identity, routes, role subjects, and role entities.
Module and tile paths must match their corresponding routing paths.
The manual requests those paths without a leading slash or spaces.
It describes API conversion of comma-separated role entities into an array.
[Admin user manual, lines 3–35, 49–127, 169–217](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/User Manual/page.md>)

The manual permits deactivation of a verified record and returns it to `un-verified` status.
It provides record-specific history viewing.
The supplied text does not fully specify rollback, activation propagation, or concurrent edits.
[Admin user manual, lines 3–35, 49–127, 169–217](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/User Manual/page.md>)

### Historical persistence relationships

The Flyway page configures a schema-history table and enables migration baselining from version zero.
Its SQL defines import-map records with unique keys and categories with unique labels.
Tile records reference both category and import-map records through foreign keys.
Separate import-map, category, and tile audit tables preserve the design's change-history vocabulary.
These relationships describe retained SQL, rather than a confirmed deployed schema or executed migration.
[Flyway configuration and schema, lines 16–24, 77–220](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Flywaydb/page.md>)

### Draft routing intake and operational context

The NGINX draft collects an upstream name, host, port, route path, rewrite rule, protocol, and request limits.
Its intake also includes environment, WebSocket settings, timeout values, load-balancing method, and custom headers.
These fields explain the routing information required during tenant onboarding.
They do not establish current endpoint values, active configuration, or a working deployment pipeline.
[NGINX draft, lines 3–46](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Drafts/The Proxy Config of Nginx Operation Standard Step/page.md>)

The draft separates non-production maintenance from UAT and stage configuration work.
Its manual-deployment discussion identifies configuration testing and rollback as improvement proposals.
Those proposals require an applicable operating procedure before use.
[NGINX environment discussion, lines 48–61](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Drafts/The Proxy Config of Nginx Operation Standard Step/page.md>)

The retained firewall register supplies operational connectivity context for tenant onboarding.
Its addresses and contact details remain in the original material.
Current network approvals and reachability were not verified.
[Firewall operational register, lines 1–8](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Firewall Configurations/page.md>)

### Current empty-subject clarification

The [explicit user answer](../../../../tasks/ui-test-coverage-20261022/evidence/clarification-20261022/empty-subject-source.json) permits tile visibility and launch through one configured EMS2 entity.
The user must satisfy portal-entry requirements and hold entitlement for that entity.
The tile's subject setting must be empty.
The [owner and scope answer](../../../../tasks/ui-test-coverage-20261022/evidence/clarification-20261022/empty-subject-owner-scope-source.json) identifies `portal team` across local, test, UAT, and production.
The SDK criterion ([[wb-candidate-security-kt-sdk-and-entitlements]]) defines the measurable results.

This explicit user clarification is the first-priority intended-behavior reference within its scope.
It selects no multiple-entity matching rule or SSDR delegation option.
Application data permissions, publication approval, and deployed enforcement remain separate.

### SSDR entitlement discussion

The SSDR discussion describes report and download users with differing EMS2 entity assignments.
It proposes multiple tile entities and optional subject checks for selected tenants.
An empty subject would skip that validation under the described proposal.
It also considers adding missing EMS2 assignments or delegating authorization to SSDR.
[SSDR onboarding discussion, lines 3–20, 27–37, 67–69](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/On Boarding Records/SSDR On Board Discussion/page.md>)

The temporary guest-access approach is struck through.
The discussion states that the portal does not implement entitlement control outside existing systems such as EMS2.
These recorded alternatives do not establish an approved bypass, selected solution, or deployed permission rule.
[SSDR alternatives and boundary, lines 42–69](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/On Boarding Records/SSDR On Board Discussion/page.md>)

## Connections

Frontend composition ([[wb-candidate-architecture-kt-frontend-composition]]) explains containers, tiles, routing, and import maps.
SDK and entitlements ([[wb-candidate-security-kt-sdk-and-entitlements]]) explains backend validation and application permissions.
Authentication and sessions ([[wb-candidate-security-kt-authentication-and-sessions]]) separates user login from tenant configuration.
Release operations ([[wb-candidate-operations-kt-release-operations]]) connects configuration work with documented release procedures.

Capability `single-ui-application-catalog` groups declared catalog interfaces.
Contracts `single-ui-importmap-admin`, `single-ui-active-importmap`, and `single-ui-category-tile-admin` provide existing interface context.
These declarations do not establish operator permissions, approved workflow, or passing maker-checker enforcement.

## Evidence limits

The overview and schema are proposals; the manual provides procedural instructions.
Their source revisions and current applicability remain unconfirmed.
Combining them cannot establish that all proposed controls became production behavior.
Owner: unknown.
Next action: identify the current manual and schema through an applicable release record.
[Admin overview, lines 1–37](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/page.md>)
[Admin schema draft, lines 3–60, 99–101](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Table Schema and Screen Draft/page.md>)
[Admin user manual, lines 3–35, 49–127, 169–217](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/User Manual/page.md>)

The EMS2 setup page refers to absent entitlement spreadsheets, change attachments, and later setup actions.
The manual also depends on screenshots absent from this copy.
Detailed grants and visual procedures cannot be reconstructed from those references alone.
Owner: unknown.
Next action: retrieve the missing materials or retain a reviewed textual procedure.
[Admin EMS2 setup, lines 7–31](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/EMS2/page.md>)
[Admin user manual, lines 3–35, 49–127, 169–217](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/User Manual/page.md>)

The Flyway SQL, NGINX draft, and firewall register have no inspected deployment or connectivity execution.
Their retained definitions cannot establish the current schema, active routes, or network permissions.
Owner: unknown.
Next action: connect applicable migrations, operating procedures, and environment-specific checks before executing onboarding changes.
[Flyway configuration and schema, lines 16–24, 77–220](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Flywaydb/page.md>)
[NGINX environment discussion, lines 48–61](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Drafts/The Proxy Config of Nginx Operation Standard Step/page.md>)
[Firewall operational register, lines 1–8](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Firewall Configurations/page.md>)

## Open questions

How do tenant boundaries apply to maker and checker permissions?
The proposal discusses tenant-specific roles; the manual lists shared admin subjects and a different-user check.
The supplied text does not establish record-level tenant isolation.
Owner: unknown.
Next action: map role checks to record ownership and retain denied-cross-tenant assertions.
[Admin overview, lines 1–37](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/page.md>)
[Admin user manual, lines 3–35, 49–127, 169–217](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/User Manual/page.md>)

Which production controls govern self-service configuration changes?
The overview proposes avoiding repeated change requests, while the manual describes record review and audit history.
These statements do not establish an approved production governance policy.
Owner: unknown.
Next action: record the applicable release, approval, rollback, and emergency-change rules.
[Admin overview, lines 1–37](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/page.md>)
[Admin user manual, lines 3–35, 49–127, 169–217](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/User Manual/page.md>)

Which SSDR entitlement option and multiple-entity matching rule apply to the current tenant configuration?
The discussion records alternatives and a struck-through guest-access proposal without retained approval or execution.
The [empty-subject clarification](#current-empty-subject-clarification) resolves the single-entity scope only.
Owner: unknown.
Next action: Resolve multiple-entity matching and SSDR delegation before accepting those separate scopes.
[SSDR onboarding discussion, lines 13–69](<../../../evidence/knowledge/sources/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/On Boarding Records/SSDR On Board Discussion/page.md>)
