---
type: "Concept"
sources: ["summaries/KT-ces-migration-parity.md", "summaries/KT-authentication-and-sessions.md", "summaries/KT-release-operations.md", "summaries/KT-admin-and-onboarding.md", "summaries/KT-observability-and-performance.md", "summaries/KT-application-interoperability.md", "summaries/KT-architecture-evolution.md", "summaries/KT-portal-purpose.md", "summaries/KT-frontend-composition.md"]
description: "How platform and tenant teams divide delivery, catalog, and release accountability."
---

> Derived candidate/draft knowledge; publication review remains pending. [Canonical source bindings](../../source-manifest.json).

Canonical basis: [composition ownership](../../../candidates/architecture/KT-frontend-composition.md#ownership-and-availability) and [release ownership](../../../candidates/operations/KT-release-operations.md#ownership-and-release-scope).

# Application ownership and team responsibilities

## Reading routes

This page explains responsibility boundaries and unresolved owners. Use the focused process page for its detailed operating steps.

| Responsibility area | Focused process page |
| --- | --- |
| Application onboarding | [[concepts/frontend-onboarding]] |
| Catalog records and verification | [[concepts/admin-catalog-configuration]] and [[concepts/maker-checker-verification-workflow]] |
| Configuration promotion | [[concepts/configuration-promotion]] |
| Caller/provider interoperability | [[concepts/interoperability-contract-governance]] |
| Release scheduling and readiness | [[concepts/release-window-governance]] and [[concepts/tenant-production-readiness]] |
| Shared code and compatibility | [[concepts/shared-dependency-governance]] |

Retain the cross-process ownership analysis and open decisions below when assigning accountability.

## Definition

Application ownership is the division of responsibility between the platform team that maintains shared portal infrastructure and the tenant teams that build and operate application-specific modules. In the documented microfrontend model, ownership follows the composition boundary: shared foundations are centrally governed, while domain containers and feature tiles belong to individual application teams. Two further axes qualify that simple split. Interoperability separates a requesting tenant team that owns the caller side, a provider team that owns the receiving handler, and the portal platform that owns intent routing and dispatch. Catalog administration separates the application team that supplies module, tile, and deployment inputs from the portal-side administrators who verify and activate the resulting catalog records. Release operations add a temporal axis: one party executes Portal-side release steps while the other validates the tenant application and confirms business activation. See [[summaries/KT-frontend-composition]] for the source summary, [[summaries/KT-portal-purpose]] for the portal-level statement of purpose, [[summaries/KT-application-interoperability]] for the interoperability evidence, [[summaries/KT-admin-and-onboarding]] for the administration and onboarding evidence, and [[summaries/KT-release-operations]] for the release and production-readiness evidence.

## Ownership split

| Area | Documented responsibility |
| --- | --- |
| Shared base and shell | The microfrontend team provides common routing, global state, theme context, and shared component libraries such as [[entities/mfe-base]]. |
| Shared backend availability | The microfrontend team owns availability of shared platform services, including the portal backend. |
| Shared repositories | The microfrontend team reviews and approves changes to shared repositories. |
| Application container | Each application team owns the container that connects its domain modules to the shared portal, such as [[entities/mfe-ratan-container]]. |
| Feature tiles | Each application team owns user-facing domain views, such as [[entities/mfe-cashflow-blotter]]. |
| Application backend availability | Each application team owns availability of its domain backend, services, databases, and infrastructure. |
| Deployment | Each application team chooses its deployment approach, supplies its build pipeline, and provides static-file and API URLs for proxy configuration. |
| Dependency exceptions | Tenant teams retain security, licensing, vulnerability, support, resilience, and rollback accountability. |
| Common UI work | The guild supplies shared design, components, and utilities through one design language. |
| Business delivery | Application teams keep their domain functions and delivery responsibility. |
| Catalog administration | Portal-side administrators maintain module mappings, drawer categories, and tile records; application teams supply the module names, paths, tile content, and hosting URLs. |
| Catalog verification | Creation and modification require a second, different user to check and verify the record before activation; each admin function keeps its own audit history. |
| Interoperability caller | The requesting tenant team owns business demand and caller-side implementation. |
| Interoperability provider handler | The provider team registers the intent, implements the receiving handler, consumes context, performs the business action, and may return a result or status. |
| Intent routing and dispatch | The portal platform receives standardized intents and provides routing, access control, context passing, and dispatch. |
| Interoperability readiness | Caller and provider jointly deliver the feature; caller completion alone does not enable it. |
| Portal release execution | The release proposal assigns Portal routing, route enabling, tenant interface changes, and Portal-owned production changes to Portal teams, including routing rollback. |
| Tenant application delivery | Tenant teams own their UI, backend, services, databases, and infrastructure and validate their applications before release. |
| Tenant validation and support | Tenant teams perform UVT and support tenant-raised issues after release. |
| Configuration promotion | The tenant team retains the exported CSV records in a tenant-owned repository; the first bulk insert into UAT and Production runs as a separate backend release. |
| Release window decisions | Unresolved; the proposal defines release windows, freeze rules, and exception paths without a confirmed approving owner. |
| Technical versus business activation | Unresolved; records separate technical go-live from business go-live but name no accepting owner. |
| SSDR entitlement choices | Unresolved; the discussion records multiple-entity, subject-check, added-assignment, and delegated-authorization alternatives without a retained decision. |
| Production authentication handoff | Unresolved; the proof of concept uses a provider token in URL parameters, which does not establish an approved production design. |

These role declarations describe the intended operating model. They do not confirm current named owners or effective approvals. The release statements in particular come from a proposal whose authority remains unconfirmed.

The portal-level materials state the same split in purpose terms: the guild provides consistent design, shared components, and utilities, while application teams retain their domain functions. The portal is one implementation of that UI approach. See [[summaries/KT-portal-purpose]].

## Boundary within the composition model

The [[concepts/microfrontend-layering]] model separates four layers: root configuration, base shell, application container, and feature tile. Ownership maps onto this structure. The root configuration and base shell are platform-controlled, while the application container and its tiles are tenant-controlled. [[entities/mfe-root-config]] represents the root configuration layer, [[entities/single-spa]] manages application lifecycle, and [[entities/systemjs]] resolves registered module names to deployed files.

This boundary lets a tenant team change its own domain views without changing the shared shell. It also means a change to a shared interface may affect several tenant consumers. That risk requires coordinated review across the shared boundary.

### Ambiguity of the term container

The sources use *container* for two roles: the shared base that supplies common context, and the application-owned module described above. The platform role and the tenant role therefore share one word. When an interface or a review responsibility is described, state which role is meant; otherwise the ownership boundary is unclear.

### Ambiguity of the term provider

Interoperability introduces a similar ambiguity around *provider*. The portal may be described as the provider of routing, access control, context passing, and dispatch, while the target application team may be described as the provider of the receiving handler. The briefing also describes a platform provider as the coordination hub and states that the Ratan provider customizes intent routing. These are different roles. A statement that "the provider" must register an intent, implement a handler, or approve a context contract is unclear until the role is named.

### Ambiguity of platform-team names

The onboarding materials use *microfrontend team*, *portal team*, and *guild* for the platform side. The development principle assigns portal-backend availability to the microfrontend team and shared-repository review to the same group. The admin clarification names `portal team` as the owner of the empty-subject tile policy across local, test, UAT, and production. The release proposal uses *Platform Team* and *Portal Team* for release execution and routing rollback. The user manual refers to shared `FMO PORTAL ADMIN` entitlements rather than to a team. The sources do not state whether these labels denote one organization, overlapping groups, or distinct roles. Ownership statements should name the role that must act, not only the label used in a sentence.

## Capability boundaries at portal level

The portal materials group responsibilities by capability rather than by team. Entry and identity, composition, access, administration, integration, and observation are described as platform-supplied. Interoperability is described as in progress, with [[entities/fdc3]] marked accordingly. The OpenFin materials add a desktop agent and an example context and intent contract. The caller and provider split crosses the platform-tenant boundary, so accountability for an interoperability feature cannot be assigned from the capability label alone.

The capability descriptions mix present-tense statements with unfinished items. They do not establish deployed or tested coverage, so they cannot be used alone to assign operational accountability.

## Admin module and catalog administration

The admin materials add a third responsibility zone between infrastructure and domain delivery. Three functions are described: Module Mapping, Drawer Category, and Tile Configuration. A module mapping connects an import-map module name with its asset path; a drawer category groups tiles; a tile record connects display details, container and route information, and entitlement configuration. The schema draft separates application categories, application tiles, and tile authorization records, and links a tile authorization record to [[entities/ems2]] entities. These draft relationships explain the design vocabulary, not a confirmed deployed database schema. See [[concepts/admin-catalog-configuration]].

Input conventions bind administration to frontend module loading. Operators enter module names without `@fm/` or spaces, and the active import-map API adds the prefix. Module and tile paths must match their routing paths, are entered without a leading slash or spaces, and comma-separated role entities are converted into an array. Tile records also carry labels, descriptions, theme images, container identity, routes, role subjects, and role entities. Correct record content therefore depends on the application team, even though the record is maintained and verified by administrators.

### Maker and checker responsibilities

The user manual requires different maker and checker users. Creation or modification produces an `un-verified` record; another user checks and verifies it before activation. Deactivation of a verified record returns it to `un-verified`, and record-specific history is available per function. This is a separation-of-duty control on the catalog, not a statement of tenant isolation. The proposal discusses tenant-specific roles, while the manual lists shared admin subjects and only the different-user check, so record-level tenant isolation is not established. See [[concepts/maker-checker-verification-workflow]].

### Administration boundaries

The overview proposes tenant-maintained configuration in place of source changes to `mfe-base` and a production change request for every tile update, and records reuse of [[entities/single-ui-bff]] as the admin backend. The proposal does not establish an approved exemption from production change controls, and the manual's review and audit history do not establish an approved production governance policy. Whether self-service catalog changes reduce or relocate release accountability therefore remains open.

The SSDR discussion states that the portal does not implement entitlement control outside existing systems such as [[entities/ems2]]. That statement bounds platform responsibility: the portal consumes entity and role data rather than operating its own entitlement store. The same discussion records alternatives, including adding missing EMS2 assignments or delegating authorization to SSDR, without a retained decision. The empty-subject clarification resolves only a single-entity scope, permits tile visibility and launch through one configured EMS2 entity with an empty subject, names `portal team` as owner, and leaves approval pending. See [[concepts/ems2-entitlement-provisioning]] and [[concepts/portal-entry-and-tile-authorization]].

### Configuration promotion as a joint responsibility

The documented promotion flow crosses three parties. The tenant team edits Module Map, Drawer Category, and Tile Configuration records in Development, exports them as CSV files, and retains them in a tenant-owned repository. An ADO pipeline then uploads configuration through the Portal Admin service at `/api/auth/v1/fmo/admin/config/upload`, and the flow states that the service validates an FMAA JWT before processing the files. The first bulk insert into UAT and Production runs as a separate backend release rather than through tenant self-service. Later uploads depend on tenant connectivity to the Admin service.

The checklist also flags planned [[entities/fmaa]] decommissioning, which leaves the authentication prerequisite of the promotion path unresolved. Promotion accountability therefore spans the tenant pipeline, the platform-side Admin service and its release, and the identity component that guards the upload endpoint. No upload, validation, or rollback ran during ingestion. See [[concepts/configuration-promotion]].

## Interoperability ownership and joint delivery

The interoperability guide assigns business demand and caller implementation to the requesting tenant team. The portal receives standardized intents and supplies routing, access control, context passing, and dispatch. The provider team registers the intent, implements the receiving handler, consumes context, performs the business action, and can optionally return a result or status.

A completed caller alone cannot enable the full feature under this guide. Provider readiness also requires intent registration, a handler, agreed context, authorization readiness, testing, and production deployment. The guide therefore treats interoperability as a joint delivery dependency. Its development code blocks are empty and its diagrams are absent from the supplied copy, so it supplies cooperation intent rather than a runnable integration contract and does not confirm passing access-control enforcement.

The example contract uses application channel `fmchannel`, with listeners such as `fmchannel.provider`, `fmchannel.reactapp`, and `fmchannel.fmoportal`. It documents `openTile`, `changeTheme`, and `getToken` actions. The launch example declares `fdc3InteropApi` value `1.2` and an `OpenTile` intent, while other entries use different intent and context names. Until a versioned schema and compatibility tests are agreed, caller and provider implementations can diverge. Contract authority therefore sits between the platform and the participating teams and requires explicit governance. See [[concepts/intent-based-application-interoperability]] and [[concepts/interoperability-contract-governance]].

Authentication handoff is another shared boundary. The proof of concept launches applications with a provider token in URL parameters after provider authentication. It presents that handoff as a way to avoid another login prompt and states that a real provider should run hidden after authentication. No production authentication design, security approval, or token-handling verification was inspected. Ownership of token transport and the trust boundary remains unresolved. See [[concepts/cross-application-authentication-handoff]].

The briefing limits its stated business scope to application rendering and interoperability. Third-party integrations and native adapters are outside that stated plan. It separates production identity verification, blotter onboarding, and business user onboarding as distinct milestones. That separation implies different technical and business acceptance owners, but the briefing supplies no approval attachments or completion records, and its month-based timelines omit the year.

## Release operations and production activation

The release materials add an operational phase to the ownership model. The proposal defines Portal scope as routing, route enabling, tenant interface changes, and Portal-owned production changes, and states that Portal teams execute those and perform routing rollback. Tenant teams validate their applications, perform UVT, and support tenant-raised issues. The same separation appears in the release calendar, which distinguishes Portal release dates from tenant release dates, and in the request template, which permits Portal deployment before application deployment. The release vehicle for these requests is [[entities/markets-operations-one-release]].

Release scheduling authority is not confirmed. The proposal sets windows on the first, third, and available fifth Saturdays from 09:00 SGT, freezes scope after Monday EOD in the first week, cancels windows without requests, and requires approved exceptions for late additions. It gives 24 hours in its summary but 10 hours and a 19:00 SGT finish in its table, and its urgent-release section requires all confirmations while also permitting progress when nobody objects. Until an owner resolves these points, no team can be held to a specific standby or confirmation obligation. See [[concepts/release-window-governance]].

### Evidence for technical and business activation

Several records separate technical deployment from business acceptance. The release calendar lists Entra technical and business go-live entries. The OpenFin briefing separates technical onboarding from business user onboarding. The [[entities/ddr]] request states that business UAT sign-off follows technical go-live and lists separate technical and business target dates. The [[entities/vpa]] request separates Portal and application go-live dates. This pattern implies one owner for deployment and another for acceptance, but none of these records names the accepting owner or retains completion evidence.

Request evidence gaps reinforce that limit. The [[entities/cdups]] request leaves UAT sign-off, user profiles, user counts, and UVT details unprovided. The [[entities/ddr]] request records pending connectivity and separates technical sign-off from business validation. Several [[entities/vpa]] references are struck through. The blank template asks for DNS resolution, expected totals and concurrent users, routing changes, connectivity evidence, sign-off, and UVT contacts, which distributes the readiness burden between the requesting tenant and the reviewing platform side. Missing or withdrawn evidence cannot demonstrate that either side met its gate.

### Tenant boundary and production connectivity

The production checklist recommends that Portal connections reach tenants through tenant-controlled [[entities/nginx]] or load balancers, after which tenant teams control internal server and port changes behind that boundary. The checklist separately requests browser reachability, Portal-to-tenant connectivity, operating agreements, penetration testing, and tile release. Configuration upload alone therefore does not establish business readiness, and ingress maintenance is split between the tenant boundary owner and the platform routing owner. See [[concepts/tenant-production-readiness]] and [[concepts/portal-ingress-path]].

## Onboarding and repository ownership

The [[concepts/frontend-onboarding]] procedure expects an application team to create separate container and tile repositories from separate templates. The team then updates module names, build configuration, imports, interfaces, container entry points, unit tests, and the local import map. After that, it registers the application through the admin manual, builds and deploys the files, and informs the platform team of the static-file and API URLs. Onboarding is therefore a two-party handoff: the application team produces and hosts assets, and the platform side registers the module and configures access.

The backend onboarding procedure completes the same handoff on the service side. It requests application URLs for proxy configuration and CORS handling, requires application role or entitlement setup in [[entities/ems2]], and directs services to SDK-based JWT validation and entitlement integration through [[entities/single-ui-sdk]]. Onboarding therefore spans routing, authentication, authorization data, and UI registration, and no single team completes it alone.

Separate repositories and pipelines are intended to support independent delivery while preserving one user workspace. The sources present this as a design goal; they do not demonstrate that every application achieves it. For an interoperability feature, tile onboarding is also not sufficient by itself: the provider-side intent registration, handler, agreed context, authorization readiness, testing, and production deployment must also be complete. The release proposal adds a 30-day engagement expectation for new interfaces, which shifts early coordination onto the requesting tenant team.

Routing configuration adds a further boundary. Application teams supply the static-file and API URLs, and the platform side turns them into [[entities/nginx]] proxy configuration. The NGINX draft collects the upstream name, host, port, route path, rewrite rule, protocol, request limits, environment, WebSocket settings, timeouts, load-balancing method, and custom headers needed for that work. Its discussion separates non-production maintenance from UAT and stage changes and raises configuration testing and rollback as improvement proposals. Those proposals do not yet have an owning procedure or a named approver. See [[concepts/portal-ingress-path]].

## Shared dependency governance

Shared modules are connected through exports, imports, and registered names. [[concepts/shared-dependency-governance]] therefore sits between platform and tenant ownership: the platform controls the shared contract, while tenant teams consume it. Shared dependencies require coordinated upgrades, and the framework comparison warns that shared libraries can constrain independent release.

The interoperability proof of concept reports that two FDC3 libraries did not exchange broadcast messages, that one library produced intent errors, and that the other handled intents successfully. Its workaround uses `fdc3-2.1` for broadcast and `openfin-fdc3` for intents. This is a reported proof-of-concept observation without a supported compatibility guarantee. Library selection and workaround ownership therefore belong under shared dependency governance, not only under individual application delivery.

The supplementary dependency principle prohibits direct external GUI dependencies unless platform governance reviews and approves an exception. Tenant teams remain accountable for the associated security, licensing, vulnerability, support, resilience, and rollback risks. The source does not identify which exceptions are approved or when they apply.

## Draft principles and proposed changes

Draft principles add SSO, tile authorization, interoperability, action tracing, and a forthcoming notification center as shared concerns. These statements are draft intent, not accepted rules, so they do not yet transfer accountability to the platform. The interoperability materials show that naming interoperability as a shared concern does not by itself assign caller, provider, contract, or authentication ownership. Those roles must be named explicitly.

A deployment proposal names onboarding changes, workflow AI, telemetry, and infrastructure migration for 2026 and early 2027, and lists notification, dashboards, and OpenFin as refining requirements. The proposal has no approval record in the supplied materials. The release proposal is likewise unapproved, and its responsibility table therefore describes intended allocation rather than effective accountability. Until an owner approves either document, neither changes current team responsibilities, and their target service lists remain proposed decompositions rather than agreed ownership maps.

## Authority and evidence limits

The sources record role declarations rather than confirmed organizational authority. Current named owners, effective approvals, and the owner who controls compatibility changes across shared modules and tenant applications remain unknown. The portal introduction remains under edit and the principles remain draft, so accepted scope is not established. The admin overview and schema are proposals, while the user manual is procedural; their revisions and current applicability are unconfirmed. The EMS2 setup page refers to entitlement spreadsheets, change attachments, and later setup actions that are absent from the supplied copy, and the manual depends on screenshots that are also missing, so detailed grants and visual procedures cannot be reconstructed. One capabilities page depends on screenshots absent from the export, and the deployment proposal carries no approval record. The interoperability guide has empty development examples and missing diagrams, and the proof of concept's screenshots and source archives are absent from the supplied copy. The release proposal and the admin release checklist are unapproved and under construction, the release calendar carries planning dates, and several tenant requests contain pending or struck-through fields. The retained [[entities/flyway]] SQL, NGINX draft, and firewall register have no inspected deployment, migration, or connectivity execution, so they cannot establish the current schema, active routes, or network permissions. No desktop agent, provider, application, catalog operation, configuration upload, release, or compatibility test ran during ingestion.

The source manifest identifies local bytes without original page revisions or confirmed source authority, so the citations support a reproducible reading but not approved or current project intent. Ownership statements should be confirmed before they are used to implement a new application, approve a shared change, or schedule a release.

## Open questions

- Which exact repository revisions implement the current container, tile, and routing interfaces?
- Which development guidelines and shared dependency versions are currently accepted?
- Which owner controls compatibility changes across shared modules and tenant applications?
- Which dependency exceptions have platform review, accountable tenant ownership, and effective dates?
- Which owner can confirm the current portal name, scope, and capability inventory?
- Which draft principles became accepted rules, and when?
- Which 2026 and 2027 proposals have approved scope or deployed implementations?
- Which owner controls the caller and provider contract, including intent names, context schemas, and versions?
- Which team owns the production authentication handoff and approves token transport?
- Which provider teams have registered intents, implemented handlers, and completed authorization, testing, and deployment?
- Which FDC3 library combination is supported, and who owns the compatibility workaround?
- How are tenant record boundaries enforced for maker and checker users, and who verifies cross-tenant isolation?
- Which release, approval, rollback, and emergency-change controls govern self-service catalog changes in production?
- Who approves the pending empty-subject tile policy, and which multiple-entity matching rule and SSDR option apply to current tenants?
- Which source revisions and environment checks establish the deployed catalog schema and the current onboarding procedure?
- Who owns NGINX configuration testing and rollback, and which environment procedure is currently approved?
- Who decides release-window exceptions, cancellations, and urgent-release confirmations, and whether a window lasts 10 or 24 hours?
- Who records technical go-live separately from business activation for each tenant, environment, and application?
- Which party owns the configuration promotion pipeline after FMAA decommissioning, and which replacement authentication component applies?
- Which team supplies connectivity, operating-agreement, and penetration-test evidence for the tenant boundary, and who verifies it?

## Related pages

- [[summaries/KT-frontend-composition]]
- [[summaries/KT-portal-purpose]]
- [[summaries/KT-application-interoperability]]
- [[summaries/KT-admin-and-onboarding]]
- [[summaries/KT-sdk-and-entitlements]]
- [[summaries/KT-release-operations]]
- [[concepts/microfrontend-layering]]
- [[concepts/frontend-onboarding]]
- [[concepts/admin-catalog-configuration]]
- [[concepts/configuration-promotion]]
- [[concepts/maker-checker-verification-workflow]]
- [[concepts/ems2-entitlement-provisioning]]
- [[concepts/shared-dependency-governance]]
- [[concepts/portal-entry-and-tile-authorization]]
- [[concepts/portal-tile-workspace-model]]
- [[concepts/portal-ingress-path]]
- [[concepts/intent-based-application-interoperability]]
- [[concepts/interoperability-contract-governance]]
- [[concepts/cross-application-authentication-handoff]]
- [[concepts/release-window-governance]]
- [[concepts/tenant-production-readiness]]
- [[entities/portal-team]]
- [[entities/fmo-post-trade-portal]]
- [[entities/markets-operations-one-release]]
- [[entities/mfe-base]]
- [[entities/mfe-root-config]]
- [[entities/mfe-ratan-container]]
- [[entities/mfe-cashflow-blotter]]
- [[entities/single-spa]]
- [[entities/systemjs]]
- [[entities/ems2]]
- [[entities/single-ui-bff]]
- [[entities/single-ui-sdk]]
- [[entities/fmaa]]
- [[entities/nginx]]
- [[entities/flyway]]
- [[entities/fdc3]]
- [[entities/openfin]]
- [[entities/ddr]]
- [[entities/vpa]]
- [[entities/cdups]]

See also: [[summaries/KT-architecture-evolution]]

See also: [[summaries/KT-observability-and-performance]]


See also: [[summaries/KT-authentication-and-sessions]]

See also: [[summaries/KT-ces-migration-parity]]