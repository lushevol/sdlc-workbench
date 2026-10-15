---
type: KnowledgeTopic
id: KT-admin-and-onboarding
version: 1
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/page.md
  revision: sha256:4be78457402c3fab32bac328a1690d852fdc34d41f363f8941efae41a3482911
  sha256: 4be78457402c3fab32bac328a1690d852fdc34d41f363f8941efae41a3482911
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Table
    Schema and Screen Draft/page.md
  revision: sha256:e0b574ea07d2f94a1c7a46439b97b4fd59670de7a9cdc88be3b34ef09896dd28
  sha256: e0b574ea07d2f94a1c7a46439b97b4fd59670de7a9cdc88be3b34ef09896dd28
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/User
    Manual/page.md
  revision: sha256:04d6ef196815349bd9144e81cde136c35b2ffae4a63fff825d89c687ec3fe16c
  sha256: 04d6ef196815349bd9144e81cde136c35b2ffae4a63fff825d89c687ec3fe16c
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Development Principle
    - Development Guideline - Onboarding Process/Development Principle/page.md
  revision: sha256:06ce1c57bd699e5100e82a59b79c59a1cec1a8973223586a2eba9a9bda29d5b3
  sha256: 06ce1c57bd699e5100e82a59b79c59a1cec1a8973223586a2eba9a9bda29d5b3
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Development Principle
    - Development Guideline - Onboarding Process/Frontend Onboarding Process/page.md
  revision: sha256:b93d2fc08759df036482b632fe9c8f8f966be1d4c98eedc235c5206a036c587f
  sha256: b93d2fc08759df036482b632fe9c8f8f966be1d4c98eedc235c5206a036c587f
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Development Principle
    - Development Guideline - Onboarding Process/Backend Onboarding Process/page.md
  revision: sha256:d861539b93503406149b03d7917f985fbebba26499ddd43338fe5ce1de42d6a8
  sha256: d861539b93503406149b03d7917f985fbebba26499ddd43338fe5ce1de42d6a8
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Development Principle
    - Development Guideline - Onboarding Process/Creating EMS2 Entity Role Subject Action/page.md
  revision: sha256:e55b2b4df69be6340dfd38f59083f31c71abb0464cbe152573f60079ab3dc4b7
  sha256: e55b2b4df69be6340dfd38f59083f31c71abb0464cbe152573f60079ab3dc4b7
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/EMS2/page.md
  revision: sha256:f6c34b31a788d6d634845965506b96672573cbd40cb176afe870b963e0c3bcd2
  sha256: f6c34b31a788d6d634845965506b96672573cbd40cb176afe870b963e0c3bcd2
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Flywaydb/page.md
  revision: sha256:dbb70c8147ccd91f3c8d10cf724f8421038e36a378f8d693181928127fc30165
  sha256: dbb70c8147ccd91f3c8d10cf724f8421038e36a378f8d693181928127fc30165
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Drafts/The Proxy Config
    of Nginx Operation Standard Step/page.md
  revision: sha256:3f1ad32cd017284ddb988f39cadc8e07813597bca193b49fae194f7ea639d09e
  sha256: 3f1ad32cd017284ddb988f39cadc8e07813597bca193b49fae194f7ea639d09e
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Firewall
    Configurations/page.md
  revision: sha256:df7621489221d46c454f903aca629fb54c21dc95f79a84ce347dcceee9c192fb
  sha256: df7621489221d46c454f903aca629fb54c21dc95f79a84ce347dcceee9c192fb
- resource: knowledge/raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/On Boarding Records/SSDR
    On Board Discussion/page.md
  revision: sha256:3d6304273d70a0dc7558c6f3072ac02ae50382d6931cb70a3990dd0bef53f0ef
  sha256: 3d6304273d70a0dc7558c6f3072ac02ae50382d6931cb70a3990dd0bef53f0ef
generated:
  by: agent:codex
  at: '2026-10-15T00:38:52.657060+00:00'
verified: []
classification: operations
scope: Portal tenant onboarding, application catalog administration, and documented team responsibilities.
summary: Onboarding joins frontend deployment, backend routing, EMS2 roles, and reviewed application catalog changes.
related:
- KT-sdk-and-entitlements
- KT-authentication-and-sessions
- KT-frontend-composition
- KT-release-operations
- single-ui-application-catalog
- single-ui-importmap-admin
- single-ui-active-importmap
- single-ui-category-tile-admin
open_questions:
- Which onboarding and admin procedures apply to the current environment?
- How are tenant record boundaries enforced for maker and checker users?
- Which release controls apply to configuration changes made through self-service?
- Which source revisions and environment checks establish the deployed catalog schema?
- Which SSDR entitlement option and subject-checking rule apply to the current tenant configuration?
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
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
[Admin overview, lines 1–37](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/page.md>)

The user manual identifies three admin functions: Module Mapping, Drawer Category, and Tile Configuration.
A module mapping connects an import-map module name with its asset path.
A drawer category groups application tiles.
A tile record connects display details, container and route information, and entitlement configuration.
[Admin user manual, lines 3–35, 49–127, 169–217](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/User Manual/page.md>)

The schema draft separates application categories, application tiles, and tile authorization records.
Its tile authorization records link a tile to EMS2 entities.
These draft relationships explain the design vocabulary, rather than the deployed database schema.
[Admin schema draft, lines 3–60, 99–101](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Table Schema and Screen Draft/page.md>)

### Team responsibilities and onboarding sequence

The development principle assigns portal-backend availability to the microfrontend team.
It assigns each application's backend availability to its application team.
Application teams choose deployment approaches and provide static-file and API URLs for NGINX configuration.
The document also separates feature-branch contribution from shared-repository review and approval responsibilities.
[Development principle, lines 2–10](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Development Principle - Development Guideline - Onboarding Process/Development Principle/page.md>)

The frontend procedure starts from separate container and tile templates.
It updates names, webpack, interfaces, entry points, tests, and the local import map.
It then links application registration through the admin manual.
Each application supplies its build pipeline and informs the portal team about static-file and API URLs.
[Frontend onboarding, lines 1–15](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Development Principle - Development Guideline - Onboarding Process/Frontend Onboarding Process/page.md>)

The backend procedure requests application URLs for proxy configuration and CORS handling.
It requires application role or entitlement setup in EMS2.
It directs services to SDK-based JWT validation and entitlement integration.
Onboarding therefore spans routing, authentication, authorization data, and UI registration.
[Backend onboarding, lines 1–7](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Development Principle - Development Guideline - Onboarding Process/Backend Onboarding Process/page.md>)

The EMS2 procedure creates an entity, actions, roles, and subjects.
It then assigns actions to role-and-subject combinations.
The admin manual identifies `FMO PORTAL ADMIN` entitlements for import-map, category, and tile functions.
These procedures describe prerequisites; they do not establish completed grants for any current operator.
[EMS2 setup procedure, lines 1–12](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Development Principle - Development Guideline - Onboarding Process/Creating EMS2 Entity Role Subject Action/page.md>)
[Admin user manual, lines 3–35, 49–127, 169–217](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/User Manual/page.md>)

### Review and activation workflow

The manual requires different maker and checker users.
Creation and modification produce an `un-verified` record.
Another user checks and verifies that record before activation.
The manual states that each admin function maintains its own audit history.
[Admin user manual, lines 3–35, 49–127, 169–217](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/User Manual/page.md>)

For module mappings, users enter the module name without `@fm/` or spaces.
The manual says the active import-map API adds `@fm/` automatically.
The stored path supplies the import-map value.
These input conventions connect administration with frontend module loading.
[Admin user manual, lines 3–35, 49–127, 169–217](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/User Manual/page.md>)

Tile configuration captures labels, descriptions, theme images, container identity, routes, role subjects, and role entities.
Module and tile paths must match their corresponding routing paths.
The manual requests those paths without a leading slash or spaces.
It describes API conversion of comma-separated role entities into an array.
[Admin user manual, lines 3–35, 49–127, 169–217](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/User Manual/page.md>)

The manual permits deactivation of a verified record and returns it to `un-verified` status.
It provides record-specific history viewing.
The supplied text does not fully specify rollback, activation propagation, or concurrent edits.
[Admin user manual, lines 3–35, 49–127, 169–217](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/User Manual/page.md>)

### Historical persistence relationships

The Flyway page configures a schema-history table and enables migration baselining from version zero.
Its SQL defines import-map records with unique keys and categories with unique labels.
Tile records reference both category and import-map records through foreign keys.
Separate import-map, category, and tile audit tables preserve the design's change-history vocabulary.
These relationships describe retained SQL, rather than a confirmed deployed schema or executed migration.
[Flyway configuration and schema, lines 16–24, 77–220](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Flywaydb/page.md>)

### Draft routing intake and operational context

The NGINX draft collects an upstream name, host, port, route path, rewrite rule, protocol, and request limits.
Its intake also includes environment, WebSocket settings, timeout values, load-balancing method, and custom headers.
These fields explain the routing information required during tenant onboarding.
They do not establish current endpoint values, active configuration, or a working deployment pipeline.
[NGINX draft, lines 3–46](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Drafts/The Proxy Config of Nginx Operation Standard Step/page.md>)

The draft separates non-production maintenance from UAT and stage configuration work.
Its manual-deployment discussion identifies configuration testing and rollback as improvement proposals.
Those proposals require an applicable operating procedure before use.
[NGINX environment discussion, lines 48–61](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Drafts/The Proxy Config of Nginx Operation Standard Step/page.md>)

The retained firewall register supplies operational connectivity context for tenant onboarding.
Its addresses and contact details remain in the original material.
Current network approvals and reachability were not verified.
[Firewall operational register, lines 1–8](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Firewall Configurations/page.md>)

### SSDR entitlement discussion

The SSDR discussion describes report and download users with differing EMS2 entity assignments.
It proposes multiple tile entities and optional subject checks for selected tenants.
An empty subject would skip that validation under the described proposal.
It also considers adding missing EMS2 assignments or delegating authorization to SSDR.
[SSDR onboarding discussion, lines 3–20, 27–37, 67–69](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/On Boarding Records/SSDR On Board Discussion/page.md>)

The temporary guest-access approach is struck through.
The discussion states that the portal does not implement entitlement control outside existing systems such as EMS2.
These recorded alternatives do not establish an approved bypass, selected solution, or deployed permission rule.
[SSDR alternatives and boundary, lines 42–69](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/On Boarding Records/SSDR On Board Discussion/page.md>)

## Connections

[Frontend composition](../architecture/KT-frontend-composition.md) explains containers, tiles, routing, and import maps.
[SDK and entitlements](../security/KT-sdk-and-entitlements.md) explains backend validation and application permissions.
[Authentication and sessions](../security/KT-authentication-and-sessions.md) separates user login from tenant configuration.
[Release operations](KT-release-operations.md) connects configuration work with documented release procedures.

Capability `single-ui-application-catalog` groups declared catalog interfaces.
Contracts `single-ui-importmap-admin`, `single-ui-active-importmap`, and `single-ui-category-tile-admin` provide existing interface context.
These declarations do not establish operator permissions, approved workflow, or passing maker-checker enforcement.

## Evidence limits

The overview and schema are proposals; the manual provides procedural instructions.
Their source revisions and current applicability remain unconfirmed.
Combining them cannot establish that all proposed controls became production behavior.
Owner: unknown.
Next action: identify the current manual and schema through an applicable release record.
[Admin overview, lines 1–37](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/page.md>)
[Admin schema draft, lines 3–60, 99–101](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Table Schema and Screen Draft/page.md>)
[Admin user manual, lines 3–35, 49–127, 169–217](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/User Manual/page.md>)

The EMS2 setup page refers to absent entitlement spreadsheets, change attachments, and later setup actions.
The manual also depends on screenshots absent from this copy.
Detailed grants and visual procedures cannot be reconstructed from those references alone.
Owner: unknown.
Next action: retrieve the missing materials or retain a reviewed textual procedure.
[Admin EMS2 setup, lines 7–31](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/EMS2/page.md>)
[Admin user manual, lines 3–35, 49–127, 169–217](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/User Manual/page.md>)

The Flyway SQL, NGINX draft, and firewall register have no inspected deployment or connectivity execution.
Their retained definitions cannot establish the current schema, active routes, or network permissions.
Owner: unknown.
Next action: connect applicable migrations, operating procedures, and environment-specific checks before executing onboarding changes.
[Flyway configuration and schema, lines 16–24, 77–220](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Flywaydb/page.md>)
[NGINX environment discussion, lines 48–61](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Drafts/The Proxy Config of Nginx Operation Standard Step/page.md>)
[Firewall operational register, lines 1–8](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/Firewall Configurations/page.md>)

## Open questions

How do tenant boundaries apply to maker and checker permissions?
The proposal discusses tenant-specific roles; the manual lists shared admin subjects and a different-user check.
The supplied text does not establish record-level tenant isolation.
Owner: unknown.
Next action: map role checks to record ownership and retain denied-cross-tenant assertions.
[Admin overview, lines 1–37](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/page.md>)
[Admin user manual, lines 3–35, 49–127, 169–217](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/User Manual/page.md>)

Which production controls govern self-service configuration changes?
The overview proposes avoiding repeated change requests, while the manual describes record review and audit history.
These statements do not establish an approved production governance policy.
Owner: unknown.
Next action: record the applicable release, approval, rollback, and emergency-change rules.
[Admin overview, lines 1–37](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/page.md>)
[Admin user manual, lines 3–35, 49–127, 169–217](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/Admin Module/User Manual/page.md>)

Which SSDR entitlement option and subject-checking rule apply to the current tenant configuration?
The discussion records alternatives and a struck-through guest-access proposal without retained approval or execution.
Assuming an empty subject grants access could misstate the intended authorization boundary.
Owner: unknown.
Next action: obtain the applicable reviewed rule and inspect denied-access assertions for each selected tenant configuration.
[SSDR onboarding discussion, lines 13–69](<../../raw/confluence/FM TPT UI Guild/Microfrontend/FMO Post Trade Portal Home/On Boarding Records/SSDR On Board Discussion/page.md>)
