---
sources: ["summaries/KT-ces-migration-parity.md", "summaries/KT-authentication-and-sessions.md", "summaries/REQ-active-session-renewal.md", "summaries/KT-release-operations.md", "summaries/KT-admin-and-onboarding.md", "summaries/KT-observability-and-performance.md", "summaries/KT-application-interoperability.md", "summaries/KT-architecture-evolution.md", "summaries/KT-portal-purpose.md", "summaries/KT-frontend-composition.md", "summaries/ARC-portal-service-relationships.md", "summaries/KT-sdk-and-entitlements.md"]
type: "Product"
description: "SCB post-trade portal product: entry, tile authorization, microfrontend composition, admin, release, and session policy."
---

> Derived candidate/draft knowledge; publication review remains pending. [Canonical source bindings](../../source-manifest.json).

# FMO Post Trade Portal

## Reading routes

Use this entity page for product identity, scope and the retained context below. Start with the focused topic for a specific rule or question.

| Question | Focused page |
| --- | --- |
| Portal entry and tile admission | [[concepts/portal-entry-and-tile-authorization]] |
| Login tokens and downstream validation | [[concepts/single-ui-sdk-authentication]] |
| Active-session renewal and prompt recovery | [[concepts/session-activity-renewal]] and [[concepts/session-expiry-prompt-recovery]] |
| Frontend layers and shared modules | [[concepts/microfrontend-layering]] |
| Team responsibilities | [[concepts/application-ownership]] |
| Onboarding and catalog setup | [[concepts/frontend-onboarding]] and [[concepts/admin-catalog-configuration]] |
| Release readiness and promotion | [[concepts/tenant-production-readiness]] and [[concepts/configuration-promotion]] |
| Performance and cache evidence | [[concepts/frontend-performance]] and [[concepts/mfe-cache-strategy]] |

The detailed source context, unresolved questions and evidence limits remain below.

## What it is

The FMO Post Trade Portal is the SCB web portal that provides a common entry point and workspace for post-trade applications. It presents tenant application tiles to authenticated users. It is the product documented under the FM TPT UI Guild / Microfrontend knowledge space, and it governs who may enter the portal and which tiles each user sees and can launch.

The UI guild aims to provide consistent design, shared components, and utilities across application teams. The portal is one implementation of that shared UI approach: application teams retain their domain functions, while the platform supplies shared integration capabilities. See [[summaries/KT-portal-purpose]].

The portal introduction names affirmation, confirmation, settlements, and reporting as supported post-trade activities, with blotters and a rules engine as examples. That page remains under edit, so the examples describe stated scope, not a complete application inventory. The supplied materials cover the portal and UI platform, including draft principles and a future deployment proposal. They do not establish complete Financial Markets business-domain coverage.

The [[entities/portal-team]] owns the user-stated portal-entry and tile-authorization rules. The documented Entra UI SSO design assigns authorization-code exchange, user information, EMS2 entitlement retrieval and token issuance to [[entities/single-ui-bff]]. The [[entities/single-ui-sdk]] supplies JWT validation and separate entitlement helpers for downstream Spring applications. Consumer adoption remains conditional and unconfirmed. See the canonical [authentication responsibilities](../../../candidates/security/KT-authentication-and-sessions.md#authentication-responsibilities) and [SDK responsibility boundary](../../../candidates/security/KT-sdk-and-entitlements.md#integration-purpose-and-responsibility-boundary).

## Working vocabulary

| Term | Meaning in these materials |
| --- | --- |
| Tenant application | A domain application integrated into the shared portal. |
| Tile | An application view that a user opens in a workspace. |
| Workspace | A user area that holds opened tiles. |
| Container | An application-owned module or the shared base that supplies common context. The role must be made explicit when describing an interface. |
| Import map | A mapping used to locate modules for dynamic loading. |

After onboarding, two further terms enter the same vocabulary. A *module mapping* connects an import-map module name with its asset path. A *drawer category* groups application tiles. A *tile record* connects display details, container and route information, and entitlement configuration.

Release materials add a third set of terms. A *release request* records a tenant tile, its target dates, connectivity, sign-off, and UVT contacts. A *release window* is a scheduled Saturday interval for Portal changes. *Technical go-live* is deployment readiness; *business go-live* is user adoption after acceptance.

Session materials add a fourth set. *Access expiry* is the deadline after which the current access token no longer admits the user. An *idle-expiry prompt* asks the user to renew after inactivity. A *renewal* is a successful replacement of session credentials, whether from activity or from refresh-token recovery.

The terms support the tile lifecycle and module ownership described in [[concepts/portal-tile-workspace-model]] and [[concepts/microfrontend-layering]]. The sources use *container* for both common and application-specific roles, so keep the role explicit.

## Key facts from this document

### Entry and tile authorization
The portal denies entry to an authenticated SC user who has no entitlement for any registered application entity. This user-stated rule applies in local, test, UAT, and production environments. See [[concepts/portal-entry-and-tile-authorization]].

Tile behavior depends on configuration:
- A tile with zero configured EMS2 entities is hidden and direct launch is denied.
- A tile with one configured EMS2 entity and zero configured subjects remains visible and launchable when the user holds entitlement for that entity. The tile's subject setting must be empty, and the user must still satisfy portal-entry requirements and hold entitlement for that entity.

The owner and scope answer attributes the empty-subject rule to the [[entities/portal-team]] and applies it to local, test, UAT, and production. The decision is recorded as explicit user-stated intent with approval pending; it does not select a multiple-entity matching rule or an SSDR delegation option.

These rules are recorded as user-stated intent. Approval and deployed enforcement remain unconfirmed.

### Entitlement sources
The portal's entitlement model derives from [[entities/ems2]], which defines entities, roles, subjects, and actions. During migration, EMS2 entity `X_RATANONE` became CES application `RATAN_ENTITLEMENT_RULE` in [[entities/ces]]. That mapping establishes a name correspondence only, not identifier or role equivalence.

Services obtain entitlements either by querying EMS2 directly or by validating a separate entitlement token. An entitlement token must not be used as an authentication credential. See [[concepts/entitlement-retrieval]].

### Authentication context
Requests to portal-backed applications are validated by a request filter supplied by the [[entities/single-ui-sdk]]. Successful validation exposes `userId`, `entitlements`, `oud`, and `sessionId` through the `userInfo` request attribute. See [[concepts/single-ui-sdk-authentication]].

The documented identity capability covers common application entry, SSO, MFA, and session renewal. [[concepts/identity-provider-delegation]] records the identity-provider boundary.

The Admin Module flow states that the Portal Admin service validates an [[entities/fmaa]] JWT before it processes configuration CSV files. The checklist also flags planned FMAA decommissioning. That plan creates an unresolved dependency for configuration promotion and for the authentication boundary that the promotion workflow names. See [[concepts/configuration-promotion]].

### Session renewal
A candidate requirement, [[summaries/REQ-active-session-renewal]], states the intended renewal behavior for portal sessions. It remains version 7 in `candidate` governance state with `draft` status and an unknown owner, so it records requested target behavior rather than confirmed deployed behavior. Human publication review is pending.

The requested behavior is:
- Mouse movement, keyboard input, and scroll activity must each be able to drive continued renewal.
- Elapsed time alone must not produce a fresh SSO prompt while eligible activity and successful renewal continue; no fixed reauthentication maximum applies.
- After inactivity expires the access token, renewal continues through the existing refresh token, and must survive the initial refresh-token expiry.
- An idle-expiry prompt stays open while a requested renewal is pending, closes exactly once after success, and permits another attempt when the request rejects.

Seven acceptance criteria cover these points. Three criteria count at least one successful renewal during 15 seconds of sustained mouse, keyboard, or scroll activity; one requires zero elapsed-time-only SSO prompts across a four-hour controlled clock that crosses the initial refresh-token expiry; three govern prompt closure for pending, successful, and rejected renewal requests. See [[concepts/session-activity-renewal]] and [[concepts/session-expiry-prompt-recovery]].

The 100 millisecond activity cadence, 15 second observation window, and four-hour clock are test fixtures, not production timeout settings, and no finite test proves indefinite execution. Only portal-document activity is in scope; activity inside cross-origin embedded applications requires separate integration evidence. Cancellation, request sharing, recovery without any usable credential, and provider failures have no approved criterion in this requirement. Expired or revoked credentials cannot authorize renewal, though the existing service contract lets a valid access token support replacement refresh credentials. Implementation, execution, rollout, and conformance differences belong to the separate intent-to-reality gap record, which cannot modify the criteria.

### Responsibility boundary
Portal tile visibility and launch authorization are separate from application data permissions. Each tile application owns its own read and edit permission checks. A visible tile does not by itself establish permission to read or modify business data, and the SDK guides do not prove automatic subject-and-action enforcement for every API.

The same boundary applies to administration. The portal stores tile and import-map configuration; it does not thereby grant the operator rights to the business data behind those tiles.

A third boundary separates Portal release work from tenant deployment work. The Portal team changes routing and Portal-owned production configuration. Tenant teams deploy and validate their own UI, backend, services, databases, and infrastructure. See [[concepts/tenant-production-readiness]].

### Capability boundaries
The supplied capability map describes the following concerns:

| Concern | Capability described in the supplied material |
| --- | --- |
| Entry and identity | Common application entry, SSO, MFA, and session renewal; activity-driven renewal is stated as a candidate requirement, not confirmed behavior. |
| Composition | Shared themes, dynamic module loading, tiles, and workspaces. |
| Access | EMS2 roles and configured tile eligibility. |
| Administration | Configuration management and tenant onboarding. |
| Integration | Tenant UI and API routing through the portal's Nginx boundary. |
| Observation | Interaction analytics, usage dashboards, frontend and throughput measurement, and static-asset cache strategy. |
| Interoperability | Cross-application interaction, with FDC3 explicitly marked as in progress. |

This map summarizes the capabilities page, which mixes present-tense descriptions with an unfinished [[entities/fdc3]] item. The wording does not establish deployed or tested coverage for each capability. Composition and access detail also belong to [[concepts/portal-tile-workspace-model]] and [[concepts/portal-entry-and-tile-authorization]]. Integration through [[entities/nginx]] is described in [[concepts/portal-ingress-path]]. Administration overlaps with [[concepts/frontend-onboarding]] and with the administration section below. The observation row draws on [[summaries/KT-observability-and-performance]], which separates documented telemetry intent from verified operational state.

### User and application flow
The capabilities page describes one entry, authentication, tile selection, and multiple workspaces. It connects module loading with import maps and renewal with session control. This sequence explains how the documented capabilities fit together; it is a synthesis, not retained execution evidence. See [[concepts/portal-tile-workspace-model]].

## Frontend composition

The portal is built as a microfrontend composition with four reported layers: root configuration, base shell, application container, and feature tile. [[concepts/microfrontend-layering]] records the layer roles. [[entities/single-spa]] registers only the shell, while [[entities/systemjs]] and import maps resolve module names to deployed files and load successive container and tile stages. [[entities/nginx]] routes application static files and API requests through configured locations.

Known composition elements include the [[entities/mfe-root-config]] root configuration, the [[entities/mfe-ratan-container]] application container, and the demo tile [[entities/mfe-cashflow-blotter]]. Shared UI components come from [[entities/mfe-base]], which is consumed through import-map registration in both container-and-tile startup and the standalone [[entities/react]] template.

SystemJS module resolution and single-spa lifecycle management are separate responsibilities. The development guideline records shared MUI themes and a specific React version. A tooling change therefore reaches beyond individual application builds: changed output formats or shared dependencies can affect the portal loading boundary. This is an inference from the documented roles, and it requires inspection of the deployed versions before use in a migration plan.

### Ownership and delivery

[[concepts/application-ownership]] assigns shared backend availability and shared-repository review to the microfrontend team, while each application team owns its domain backend availability, chooses its deployment approach, and supplies static-file and API URLs. Application containers and tiles live in separate application-owned repositories with their own pipelines. The sources record role declarations only; current named owners and effective approvals remain unknown.

### Onboarding sequence

The documented [[concepts/frontend-onboarding]] flow is:

1. Obtain root configuration and application templates.
2. Create separate application container and tile repositories.
3. Update module names, build configuration, imports, interfaces, and container entry points.
4. Update unit tests and the local import map.
5. Configure the tile through the Admin Module procedure.
6. Build and deploy application files, then supply static-file and API URLs to the platform team.

Onboarding therefore spans four prerequisite sets rather than one: frontend assets, backend routing, EMS2 authorization data, and portal catalog records. The backend procedure collects application URLs for proxy and CORS configuration, requires application role or entitlement setup in EMS2, and directs services to SDK-based JWT validation and entitlement integration. The EMS2 setup procedure creates an entity, actions, roles, and subjects, then assigns actions to role-and-subject combinations. See [[concepts/ems2-entitlement-provisioning]].

Each application supplies its own build pipeline and informs the portal team about its static-file and API URLs. The procedures describe prerequisites; they do not establish completed onboarding for any current tenant or completed grants for any current operator.

The unfinished release checklist adds onboarding inputs beyond the six steps: SDK validation, shared frontend requests, entitlement checks, disaster recovery, performance data, operating agreements, and penetration testing. It lists these as requested readiness items, not as completed checks.

### Shared code and standards

Modules are shared through exports, imports, and registered names, so [[concepts/shared-dependency-governance]] applies: shared dependencies require coordinated upgrades, and a shared interface change can affect several tenant consumers. The development guideline prescribes TypeScript, functional components, shared [[entities/mui]] themes, and separation of view, logic, styles, and interfaces. It names React 18.2.0 and prefers Context and Reducer over additional state libraries, without a recorded effective date or supersession notice.

Optional loading guidance suggests 500 KB files and six concurrent static-file requests, but does not establish an accepted performance SLA. Direct external GUI dependencies are prohibited unless platform governance approves an exception, with tenant teams retaining security, licensing, vulnerability, support, resilience, and rollback responsibilities.

## Administration module

The Admin Module is the portal's configuration surface. An earlier overview describes a process in which every tile change required editing `mfe-base` source and raising a production change request, and proposes tenant-maintained configuration in its place. The overview records reuse of [[entities/single-ui-bff]] as the admin backend. It does not establish an approved exemption from production change controls. Full synthesis: [[summaries/KT-admin-and-onboarding]].

### Catalog functions

The manual identifies three functions: Module Mapping, Drawer Category, and Tile Configuration. A module mapping links an import-map module name to its asset path; users enter the module name without `@fm/` or spaces, and the active import-map API adds `@fm/` automatically. A drawer category groups application tiles. A tile record stores labels, descriptions, theme images, container identity, routes, role subjects, and role entities.

Module and tile paths must match their corresponding routing paths. The manual requests those paths without a leading slash or spaces, and the API converts comma-separated role entities into an array. These input conventions connect administration directly with frontend module loading and with [[concepts/portal-ingress-path]]. See [[concepts/admin-catalog-configuration]].

### Maker-checker verification

The manual requires different maker and checker users. Creation or modification produces an `un-verified` record; another user checks and verifies that record before activation. Deactivation of a verified record returns it to `un-verified`. Each admin function maintains its own audit history and offers record-specific history viewing. The supplied text does not fully specify rollback, activation propagation, or concurrent edits. See [[concepts/maker-checker-verification-workflow]].

The admin manual identifies `FMO PORTAL ADMIN` entitlements for import-map, category, and tile functions. These are prerequisites, not evidence of completed grants.

### Configuration promotion

The Admin Module release flow connects Development configuration with UAT and Production. Teams change Module Map, Drawer Category, and Tile Configuration records in Development. They export those records as CSV files and keep them in a tenant-owned repository. An ADO pipeline then uploads the files to the Portal Admin service at `/api/auth/v1/fmo/admin/config/upload`. The flow states that the service validates an FMAA JWT before it processes the files.

The first bulk insert into UAT and Production uses a separate BFF release. Later uploads depend on tenant connectivity to the Admin service. The checklist flags planned FMAA decommissioning, so the authentication step has an unresolved future owner. These statements describe a procedure; the ingestion ran no upload. See [[concepts/configuration-promotion]] and [[summaries/KT-release-operations]].

### Catalog persistence

The [[entities/flyway]] page configures a schema-history table and enables migration baselining from version zero. Its SQL defines import-map records with unique keys and categories with unique labels; tile records reference both through foreign keys, and separate import-map, category, and tile audit tables preserve change-history vocabulary. A schema draft likewise separates application categories, application tiles, and tile authorization records that link a tile to EMS2 entities. These are retained design definitions and draft relationships, not a confirmed deployed schema or an executed migration.

### Routing and connectivity intake
The NGINX draft collects an upstream name, host, port, route path, rewrite rule, protocol, and request limits, together with environment, WebSocket settings, timeout values, load-balancing method, and custom headers. It separates non-production maintenance from UAT and stage configuration work, and records configuration testing and rollback as improvement proposals rather than operating procedure. A retained firewall register supplies further connectivity context. Neither source establishes current endpoint values, active routes, or verified network approvals. See [[concepts/portal-ingress-path]] and [[entities/nginx]].

The production checklist recommends Portal connections through tenant Nginx or load balancers. Tenant teams then control internal server and port changes behind that boundary. The checklist also asks for browser reachability and Portal-to-tenant connectivity as separate checks.

### SSDR onboarding discussion

An onboarding record for SSDR describes report users and download users with differing EMS2 entity assignments. It proposes multiple tile entities and optional subject checks for selected tenants, under which an empty subject would skip that validation. It also considers adding missing EMS2 assignments or delegating authorization to SSDR, and it records a struck-through temporary guest-access approach. The discussion states that the portal does not implement entitlement control outside existing systems such as EMS2. These are recorded alternatives, not an approved bypass, selected solution, or deployed permission rule. See [[concepts/portal-entry-and-tile-authorization]].

## Release operations

Full synthesis: [[summaries/KT-release-operations]]. The release materials contain a proposal, an unfinished checklist, historical deployment guidance, and tenant requests. Their current authority remains unconfirmed.

### Release scope and responsibility split

The proposal covers Portal routing, route enabling, tenant interfaces, and Portal-owned production changes. Tenant teams keep responsibility for their UI, backend, services, databases, and infrastructure. The Portal team runs Portal releases and routing rollback. Tenant teams validate their applications, perform UVT, and support tenant issues.

These are documented responsibility statements. They do not carry confirmed present approval, and the Portal team's authority for entry and tile rules remains unverified.

### Markets Operations One release

The [[entities/markets-operations-one-release]] calendar records the tenant requests that need Portal integration. It separates Portal release dates from tenant release dates and lists separate Entra technical and business go-live entries. A calendar entry supplies planning context only; it does not prove deployment, approval, or successful adoption.

### Tenant capability requests

Release requests explain why tenant tiles need Portal integration. These descriptions identify intended business functions. They do not establish approved rules, release completion, or present availability.

| Requested capability | Documented purpose |
| --- | --- |
| [[entities/fss]] Cash Projection | Supply a cash-projection rule-engine tile. |
| FSS Funds Gating | Limit investor redemptions to a percentage of daily net asset value. |
| FSS SSI | Generate settlement instructions from stored agent accounts, with email and download options. |
| FSS Domestic Disbursement | Reconcile depository files and create MT566 messages after credit. |
| FSS Gold Custody | Capture purchases and sales, settle services, and produce daily position updates. |
| FSS Digital Asset Collateral | Support collateral use of custodied digital assets. |
| [[entities/ddr]] Reporting | Show reports received from upstream systems and forwarded downstream. |
| [[entities/cdups]] Confirmation | Manage outbound and inbound confirmation documents in separate blotters. |
| [[entities/vpa]] Fix Link | Correct broken links so subsequent trade processing can continue. |
| VPA Trade Monitor | Monitor trade status and retrieve source and transformed files. |

### Readiness before scheduling

The proposal requests solution intent, user profiles, routing details, connectivity checks, UAT sign-off, and rollback planning. It requires 30 days of engagement for a new interface. The blank request template asks for DNS resolution, expected total, new, and concurrent users, routing changes, connectivity evidence, sign-off, and UVT contacts.

Several requests do not yet satisfy these fields. The CDUPS request leaves UAT sign-off, user profiles, user counts, and UVT details unprovided. The DDR request records pending connectivity. Several VPA evidence references are struck through. Missing or withdrawn references cannot establish the corresponding release gate. See [[concepts/tenant-production-readiness]].

### Release window proposal

The proposal schedules first, third, and available fifth Saturdays, starting at 09:00 SGT. It freezes scope after Monday EOD in the first week of the release window. It cancels windows without requests and requires approved exceptions for late additions. Freeze periods require rescheduling or dispensation.

Two rules conflict. The summary specifies 24 hours, while the table specifies 10 hours and a 19:00 SGT finish. The urgent-release section requires all confirmations but also permits proceeding when nobody raises concerns. Silence and explicit confirmation are different conditions. This page does not choose between these alternatives. The release-window governance topic records the conflict.

### Technical and business activation

The Portal release date and the tenant release date are separate. Technical go-live and business go-live are also separate. The DDR request states that business UAT sign-off follows technical go-live and lists separate target dates. The VPA request separates Portal and application go-live dates. The request template explicitly allows Portal deployment before application deployment. The [[entities/openfin]] briefing likewise separates technical onboarding from business user onboarding.

A recorded date cannot prove completed deployment or accepted business capability. Keep deployment, validation, and business activation records distinct. See [[concepts/tenant-production-readiness]].

### Deployment evolution

The older frontend deployment guide describes static artifacts and a proposed blue-green model. Its Pilot and Production environments share a backend. The guide separates feature checks, artifact publication, and manual production deployment after approval. The Nginx draft proposes versioned configuration, syntax checks, restart checks, and rollback. Neither document establishes the currently deployed pipeline. See [[concepts/configuration-promotion]].

## Observability, performance, and caching

Full synthesis: [[summaries/KT-observability-and-performance]]. The materials mix design examples, draft targets, historical results, and future planning; none of them establishes current production capacity or approved service limits.

### Interaction analytics

The analytics effort aims to understand how users interact with portal features, improve adoption, and reduce time to value. The design captures tiles, modals, workspace tabs, buttons, switches, and dropdowns. Tiles and modals expose open and close events, tabs, buttons, and switches expose click events, and dropdowns expose select events. See [[concepts/interaction-analytics]].

Event identity combines container, tile, and component name. Optional values and custom attributes describe interactions such as searches. Those fields connect an event to its UI context, but they do not define an approved vocabulary for every tenant event.

The example `useAnalytics` hook submits events to `/analytics/v1/fmo/print?extend=false`, while the surrounding prose gives `/api/analytics/v1/fmo/print?extend=false` as the requested API. The example attaches session-derived authorization information for user identification, and the source also describes deriving client addresses from request headers and the remote address. The model declarations disagree: the data model declares 20 custom attribute fields, the type model declares 10, and the explanatory prose also refers to 10. The supported producer, transport, and storage limit remains unresolved.

### Usage dashboards

The dashboard guide reports nine [[entities/kibana]] dashboards for Portal usage: authentication, authentication errors, tiles, workspace movement, workspace additions, selected buttons, login choices, and themes. The error dashboard exposes `traceId` for investigation, and raw data is described as downloadable. The Production dashboard URL remains a placeholder, so present availability and data completeness are not proven.

### Frontend and throughput measurement

The monitoring page proposes weekly review of development performance, covering login, post-login, and blotter rendering together with cache and compression changes. See [[concepts/frontend-performance]].

The May 2023 performance document is explicitly a draft with no sign-off record. It lists five-second response time, 100 users, CPU below 50 percent, and JavaScript heap below 80 percent as targets, and covers login, home, trade, cashflow, exception, and rules pages using browser performance monitoring and Lighthouse. It assumes that supporting APIs remain available and sufficiently responsive. Reported values are login FCP 0.8 seconds and LCP 1.3 seconds, and home FCP 0.9 seconds and LCP 1.3 seconds. The supporting screenshots and measurement captures are absent from the supplied copy, so these values cannot establish present performance.

The UAT throughput test describes 500 users, a 250-second ramp-up, and five iterations, with 17,500 successful requests and a maximum response time of 2,023 milliseconds for `/api/auth/v2/sso/validate`. The linked [[entities/apache-jmeter]] plan and result archive are absent. A newer deployment page reports user estimates and additional performance figures alongside future onboarding and architecture changes, but its test-result and metric materials are not supplied. Every such figure requires its workload, time period, environment, and execution evidence before use in sizing.

### Cache strategy

The cache guide proposes revalidating layer entry files while caching subsequent static files for longer, with a documented 120-day expiry for chunks, images, CSS, fonts, JSON, and icons. A changed entry should reference new subsequent files, and users still need logout or page refresh to obtain updated UI code. The guide explicitly excludes a first-load improvement, and its implementation section contains no configuration. See [[concepts/mfe-cache-strategy]].

## Technology evaluations and experiments

The materials contain independent investigations. They record evaluations and demonstrations, not adopted standards. See [[summaries/KT-architecture-evolution]].

### Component-library evaluation

The library comparison records GitHub statistics dated 5 July 2023 and compares [[entities/mui]], [[entities/ant-design]], and [[entities/ag-grid]] across components, styling, licensing, and related criteria. The Ant Design note emphasizes forms, feedback components, and layout differences. The conceptual-design draft still holds unresolved rationale and selection placeholders, and its review and decision tables do not establish completed approval. See [[concepts/component-library-selection]].

These records explain historical evaluation concerns. They do not establish present library capability or an accepted purchasing decision.

### Build-tool research

The research recommends [[entities/rspack]] for incremental migration from [[entities/webpack]] and [[entities/vite]] for new or simpler applications. It treats SystemJS compatibility as an architectural constraint and proposes a pilot that checks loading, HMR, and asset paths before gradual rollout. It also proposes a longer-term move away from SystemJS, which changes the platform boundary beyond a bundler substitution. See [[concepts/build-tool-migration]].

The report has no publication date and no retained project benchmark provenance. Its recommendations remain research statements, not verified technical conclusions or accepted migration instructions.

## Notification draft

The notification draft describes many tiles opening separate subscription connections and proposes one SSE connection per user to reduce browser resources. This is proposed behavior; the source does not record an accepted connection limit or a deployed service. See [[concepts/realtime-notification-delivery]].

Three distinct experiments are described:
- [[entities/graphql]] over SSE with a Node.js backend.
- GraphQL over WebSocket with a [[entities/spring-boot]] backend.
- SSE with a Spring Boot backend.

Branch and demonstration references establish experiment locations, not successful retained execution.

The store draft considers tile reactions through React effects or registered callbacks. It declares `isRead` as a string but assigns boolean `false` in its event handler, so the field contract remains unresolved.

The table draft separates notification topics, user subscriptions, notification messages, and each user's read or display state. Topics connect container, module, tile, endpoint, and subscription payload. User-topic records add enabled and muted preferences. Notification records carry message payloads; user-notification records hold read and display flags. The same draft suggests one-hour, six-hour, or 24-hour retention, without an approved policy or cleanup rule, and without a rule for unread notifications.

## Draft principles and roadmap

The draft principles focus on SSO, tile authorization, interoperability, action tracing, and a forthcoming notification center. Their login and tile eligibility statements remain draft intent. See [[concepts/portal-entry-and-tile-authorization]].

A deployment proposal names onboarding changes, workflow AI, telemetry, and infrastructure migration for 2026 and early 2027. It also lists notification, persona dashboards, and [[entities/openfin]] as refining requirements. Its target service list separates proposed authentication, tile-management, telemetry, and AI services. The current-architecture and target logical-architecture sections have no explanatory content, so the proposal does not define service interfaces or a migration path. These targets must remain distinct from the capability inventory and current implementation.

A separate unchecked list proposes central-monitoring foundation work, an upgrade to Spring Boot 4.0.6, moving properties into services, and removal of account-and-password login. It supplies no completion records, migration order, or accepted scope, so it cannot establish current platform versions or enabled login methods.

## Evidence limits

- Source authority and original revisions are unconfirmed; the source manifest identifies local bytes only. The citations support a reproducible reading but do not establish approved or current project intent.
- The portal introduction remains under edit, and the principles remain draft. The topic cannot establish accepted scope or enforceable business rules.
- The capabilities page depends on screenshots absent from the supplied export. The textual meaning survives, but illustrated behavior cannot be reconstructed.
- The deployment proposal describes future changes without an approval record in these materials. Target services and planned features cannot serve as current implementation facts.
- The portal team's authority and approval for the entry and tile rules remain unverified across all four environments. The empty-subject decision carries approval `pending`. The SDK artifact version deployed by each downstream service is also unresolved, as is the current shape of environment tokens now that EMS2 details are being removed from authentication JWTs.
- The session-renewal requirement is a candidate version 7 draft with an unknown owner and no recorded verification, and its human publication review is pending. Its acceptance criteria describe requested target behavior: no execution, browser measurement, or provider-side refresh-token lifetime check ran during ingestion. The stated 100 millisecond cadence, 15 second window, and four-hour horizon are fixtures only, and cross-origin embedded application activity is explicitly out of scope. Cancellation and request-sharing behavior has no approved criterion in that requirement.
- For the frontend composition, the following remain unresolved: which exact repository revisions implement the current container, tile, and routing interfaces; which development guidelines and shared dependency versions are currently accepted; which owner controls compatibility changes across shared modules and tenant applications; which dependency exceptions have platform review, accountable ownership, and effective dates; and which standalone template and shared-component versions remain supported. Runtime rendering, deployment state, and template archives are not established by the supplied documentation.
- For administration and onboarding, the following remain unresolved: which admin manual and catalog schema revisions are deployed; whether the self-service model replaced or supplements the change-request path; how tenant record boundaries are enforced for maker and checker users; and which production release, approval, rollback, and emergency-change rules govern configuration made through the module. The EMS2 setup page refers to absent entitlement spreadsheets, change attachments, and later setup actions, and the manual depends on screenshots missing from the supplied copy, so detailed grants and visual procedures cannot be reconstructed. The retained Flyway SQL, NGINX draft, and firewall register have no inspected deployment or connectivity execution and cannot establish the current schema, active routes, or network permissions.
- For release operations, the following remain unresolved: which release duration applies; whether an urgent release needs explicit confirmation from every stakeholder; which checklist and deployment process govern each environment; which records prove technical readiness and business activation separately; and which tenant request evidence establishes accepted capability scope and completed readiness. No pipeline, deployment, upload, rollback, or production access check ran during ingestion. Diagrams, emails, and example projects that the guides reference are absent. The older deployment guide and the Nginx draft describe historical or proposed mechanisms, not the active pipeline.
- For the SSDR onboarding record, no approval, selected option, or execution record is retained. The empty-subject clarification resolves only the single-entity scope; multiple-entity matching and SSDR delegation remain open.
- For observability, the named non-functional requirements page contains no substantive text, so it supplies no accepted service targets or measurable acceptance criteria. Historical test targets cannot be treated as accepted current limits. The analytics models disagree on custom attribute counts, the Production dashboard address is a placeholder, examples collect identity context and search values without recorded retention rules, and the cache implementation section holds no configuration. Missing screenshots, JMeter plans, and execution archives block verification; no browser measurement, telemetry query, load test, or server-header check ran during ingestion.
- The 2023 library statistics, the build-tool benchmark tables, the notification protocols, the performance figures, and the retention alternatives have no accepted decisions attached in these materials. None can supply implementation requirements without review.

## Open questions

- Which owner can confirm the current portal name, scope, and capability inventory?
- Which draft principles became accepted rules, and when?
- Which admin manual, catalog schema, and migration revisions are currently applicable, and which environment checks confirm them?
- How are tenant record boundaries enforced for maker and checker users? The proposal discusses tenant-specific roles, while the manual lists shared admin subjects and a different-user check.
- Which release, approval, rollback, and emergency-change controls govern self-service configuration changes in production?
- Which release duration applies: 10 hours or 24 hours?
- Does an urgent release require explicit confirmation from every stakeholder?
- Which checklist and deployment process currently govern each environment?
- Which records prove technical readiness and business activation separately?
- Which FMAA replacement plan governs Admin service authentication after decommissioning?
- Who will approve the session-renewal requirement, and does the current session-renewal implementation meet its seven criteria?
- Do provider-side refresh-token lifetimes, and any cross-origin embedded application, support the requested activity-driven renewal beyond the four-hour fixture?
- Which SSDR entitlement option and multiple-entity matching rule apply to the current tenant configuration?
- Which component-library and licensing choices have accepted decisions and effective dates?
- Who authored the build-tool research, and which versions and benchmark runs support it?
- Which notification experiment, if any, became a supported portal service, and which retention and unread-message rules are accepted?
- Which 2026 and 2027 proposals have approved scope or deployed implementations?
- Which analytics model defines the supported custom attribute limit across producer, transport, storage, and dashboards?
- Which current execution records establish response time and capacity, and which non-functional requirements are accepted?
- Which deployed cache settings and asset naming rules implement the documented strategy?
- Which data collection and retention rules govern identity context and search values captured by analytics?

## Related pages
[[summaries/KT-portal-purpose]] · [[summaries/KT-sdk-and-entitlements]] · [[summaries/KT-architecture-evolution]] · [[summaries/KT-observability-and-performance]] · [[summaries/KT-admin-and-onboarding]] · [[summaries/KT-release-operations]] · [[summaries/REQ-active-session-renewal]] · [[concepts/portal-entry-and-tile-authorization]] · [[concepts/entitlement-retrieval]] · [[concepts/single-ui-sdk-authentication]] · [[concepts/session-activity-renewal]] · [[concepts/session-expiry-prompt-recovery]] · [[entities/portal-team]] · [[entities/single-ui-sdk]] · [[entities/ems2]] · [[entities/ces]] · [[entities/fmaa]]

[[summaries/KT-frontend-composition]] · [[concepts/microfrontend-layering]] · [[concepts/portal-tile-workspace-model]] · [[concepts/portal-ingress-path]] · [[concepts/application-ownership]] · [[concepts/frontend-onboarding]] · [[concepts/shared-dependency-governance]] · [[entities/mfe-root-config]] · [[entities/mfe-ratan-container]] · [[entities/mfe-base]] · [[entities/mfe-cashflow-blotter]] · [[entities/single-spa]] · [[entities/systemjs]] · [[entities/nginx]] · [[entities/react]] · [[entities/mui]] · [[entities/fdc3]]

[[concepts/admin-catalog-configuration]] · [[concepts/maker-checker-verification-workflow]] · [[concepts/ems2-entitlement-provisioning]] · [[concepts/configuration-promotion]] · [[concepts/tenant-production-readiness]] · [[entities/single-ui-bff]] · [[entities/flyway]] · [[entities/markets-operations-one-release]] · [[entities/fss]] · [[entities/ddr]] · [[entities/cdups]] · [[entities/vpa]]

[[concepts/interaction-analytics]] · [[concepts/frontend-performance]] · [[concepts/mfe-cache-strategy]] · [[entities/kibana]] · [[entities/apache-jmeter]]

[[concepts/component-library-selection]] · [[concepts/build-tool-migration]] · [[concepts/realtime-notification-delivery]] · [[entities/ant-design]] · [[entities/ag-grid]] · [[entities/rspack]] · [[entities/vite]] · [[entities/webpack]] · [[entities/spring-boot]] · [[entities/graphql]] · [[entities/openfin]]

See also: [[summaries/ARC-portal-service-relationships]]

See also: [[summaries/KT-application-interoperability]]

See also: [[summaries/KT-authentication-and-sessions]]

See also: [[summaries/KT-ces-migration-parity]]
