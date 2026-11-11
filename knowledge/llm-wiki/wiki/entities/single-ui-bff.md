---
sources: ["summaries/KT-ces-migration-parity.md", "summaries/KT-authentication-and-sessions.md", "summaries/REQ-active-session-renewal.md", "summaries/KT-release-operations.md", "summaries/KT-admin-and-onboarding.md", "summaries/KT-observability-and-performance.md", "summaries/KT-application-interoperability.md", "summaries/KT-architecture-evolution.md", "summaries/KT-portal-purpose.md", "summaries/ARC-portal-service-relationships.md"]
type: "Product"
description: "Portal backend-for-frontend for auth, sessions, admin, entitlements, analytics, and CES metadata."
---

# Single UI BFF

## What it is

The Single UI BFF is the backend-for-frontend service for the portal described in [[summaries/ARC-portal-service-relationships]]. In the user-reported architecture it is the **sole backend for the described portal scope**, handling authentication, sessions, administration, and analytics.

It sits behind the portal ingress path: [[entities/nginx]] forwards requests to [[entities/api-gateway]], which forwards to application services including the BFF. That transport path is reported but not verified — see [[concepts/portal-ingress-path]].

## Administration backend role

The admin module material in [[summaries/KT-admin-and-onboarding]] records reuse of `single-ui-bff` for the admin backend. The admin proposal describes a previous process that changed `mfe-base` source and raised a production change request for each tile update. It proposes tenant-maintained configuration instead, with this BFF serving the admin APIs.

The admin manual defines three admin functions: Module Mapping, Drawer Category, and Tile Configuration — see [[concepts/admin-catalog-configuration]]. A module mapping links an import-map module name to an asset path, a category groups tiles, and a tile record holds display details, container and route information, and entitlement configuration. The source states reuse of the BFF for the admin backend; it does not map each function to a specific endpoint.

Input conventions are attributed to the admin APIs, not to a named layer:

- The active import-map API adds `@fm/` to the module name automatically; users enter the name without that prefix and without spaces.
- Comma-separated role entities are converted into an array.
- Module and tile paths are entered without a leading slash and must match the routing paths.

Whether these conversions occur in the BFF or in another layer is unconfirmed.

The manual requires a maker-checker sequence: creation or modification produces an `un-verified` record, a different user checks and verifies it, and deactivation returns a verified record to `un-verified`. Each admin function keeps its own audit history. See [[concepts/maker-checker-verification-workflow]]. Where that state is stored and enforced — BFF, database, or frontend — is not established. The supplied text also leaves rollback, activation propagation, and concurrent edits unspecified.

The retained Flyway SQL defines import-map records with unique keys, categories with unique labels, and tile records that reference both through foreign keys, plus separate audit tables — see [[entities/flyway]]. Those are design definitions, not a confirmed deployed schema, and they do not establish that this BFF owns that data store.

Tile authorization records link a tile to EMS2 entities — see [[entities/ems2]], [[concepts/ems2-entitlement-provisioning]], and [[concepts/portal-entry-and-tile-authorization]]. The admin manual identifies `FMO PORTAL ADMIN` entitlements for the three admin functions, so the BFF's admin APIs are gated by that authorization data. The documented procedures are prerequisites; they do not establish grants for any current operator.

The authentication topic records a separate user-stated portal-entry rule: an authenticated SC user with no registered application entity entitlement must be denied portal entry in local, test, UAT, and production. The user named `portal team` as owner for that policy only; authority and approval remain unconfirmed, and the answer defines no HTTP status or denial wording. See [[entities/portal-team]] and [[concepts/portal-entry-and-tile-authorization]]. Separate user-stated rules cover tiles without a configured EMS2 entity and the empty-subject case with one configured entity and zero configured subjects — see [[summaries/KT-sdk-and-entitlements]].

The proposal to avoid repeated production change requests does not establish an approved exemption from production change controls. Review and audit history in the manual are separate from an approved release, rollback, or emergency-change policy.

## Release and promotion role

The release-operations material in [[summaries/KT-release-operations]] connects the admin backend to a configuration-promotion workflow. Module Map, Drawer Category, and Tile Configuration changes are made in Development, exported as CSV files, retained in a tenant-owned repository, and uploaded by an ADO pipeline to the Portal Admin service at `/api/auth/v1/fmo/admin/config/upload`. The flow states that the service validates an [[entities/fmaa]] JWT before processing CSV files. This page records the admin backend as the BFF; the release-operations text calls it the Portal Admin service and does not separately map that endpoint to the BFF, so endpoint ownership remains an inference rather than a confirmed route. See [[concepts/configuration-promotion]].

The first bulk insert into UAT and Production uses a separate BFF release, while later uploads depend on tenant connectivity to the Admin service. That makes BFF deployment and tenant network reachability separate readiness items. The release calendar separates Portal release dates from tenant release dates and separates Entra technical go-live from business go-live — see [[entities/entra]] and [[concepts/tenant-production-readiness]]. A BFF release is a Portal-side technical event; it does not establish tenant application deployment, business UAT sign-off, or user adoption.

The checklist also flags planned FMAA decommissioning. That warning creates an unresolved dependency for a promotion workflow that validates FMAA JWTs, and for the BFF's other FMAA-dependent paths. The replacement authentication plan is not established. The authentication topic adds historical FMAA context: client-credential authentication for machine-to-machine callers, with 17-year validity for service accounts and seven-day validity for bank IDs. Those historical values do not establish approved portal-session limits or current token policy, but they show why FMAA decommissioning is a BFF dependency rather than only an admin-upload concern.

The production checklist recommends Portal connections through tenant Nginx or load balancers, with tenant teams controlling internal server and port changes behind that boundary. That is consistent with the reported ingress path but does not confirm the BFF's deployed upstreams; see [[entities/nginx]] and [[concepts/portal-ingress-path]].

The release window proposal in the same material remains proposed and contains unresolved duration and urgent-confirmation contradictions; see the release-window governance notes. None of these records proves that a BFF release occurred or was approved.

Tenant capability requests for [[entities/fss]], [[entities/cdups]], [[entities/ddr]], and [[entities/vpa]] sit in the same release calendar. They explain why tenant tiles need Portal integration; they do not establish BFF business logic or endpoint coverage for those applications.

## Session and authentication renewal role

The candidate requirement in [[summaries/REQ-active-session-renewal]] states the intended target behavior for portal session renewal. Because this BFF is recorded as the portal's authentication and session backend, the renewal path is a BFF-facing concern, but the requirement does not name the BFF, an endpoint, or a service owner — the association is an inference, not a confirmed route.

The requested behavior has two mechanisms:

- **Activity-driven renewal.** Mouse movement, keyboard input, and scroll activity must each keep a valid session renewable, with no elapsed-time-only maximum that forces fresh authentication. The criteria use controlled fixtures (activity every 100 milliseconds for 15 seconds, at least 30 seconds of access time remaining) and require at least one successful renewal in each case — see [[concepts/session-activity-renewal]].
- **Refresh-token recovery after inactivity.** When inactivity expires the access token, renewal continues through the existing refresh token, and continued eligible activity must preserve renewal across the initial refresh-token expiry. A four-hour controlled-clock fixture requires zero SSO prompts caused solely by elapsed time.

Manual recovery from the idle-expiry prompt is specified as a prompt-lifecycle contract: the prompt must not close before renewal succeeds, must close exactly once after success, and must stay open and permit another attempt when the renewal request rejects — see [[concepts/session-expiry-prompt-recovery]]. Cancellation handling and request sharing have no approved criterion in that requirement.

The authentication topic records session designs that use an access token for application requests, an idle timeout for inactivity, an absolute timeout since authentication, and a refresh token for another authentication interval without repeating the initial SSO journey. Those are documented concepts, not a confirmed runtime contract. Version 0 states limits below 60 minutes for absolute timeout and below 15 minutes for idle timeout, with examples of a 15-minute access token and a 24-hour refresh token. Version 1 proposes `exp = iat + 15 minutes` for idle timeout, ties absolute timeout to `auth_time` and a 60-minute `max_age`, and contains conflicting 105-minute and 225-minute refresh-token durations. It also proposes changing `auth_time` during continued activity while separately stating that refresh tokens have no absolute timeout because they lack `auth_time` and `max_age`. Those proposals cannot define a single BFF timing rule without authoritative review — see [[concepts/token-lifecycle-and-timeout-policy]].

### Entra migration and authentication responsibilities

The Entra design assigns the BFF a central role in the browser-based login journey. The browser redirects to the identity provider, and the BFF performs the authorization-code exchange. The BFF builds user information, retrieves EMS2 entitlements, and issues authentication and entitlement tokens. The design retains an OneMFA fallback and a separate username/password path — see [[entities/entra]] and [[concepts/identity-provider-delegation]].

The phase 1 migration scope is narrower than this page's full BFF role. Phase 1 covers UI SSO only and explicitly excludes EMS2 replacement, portal session management, and tenant-onboarding authentication. Machine-to-machine authentication has a separate migration document with unresolved central dependencies. Consequently, the BFF's session-renewal responsibility is outside the documented phase-1 migration boundary even though this page records the BFF as the session backend.

The non-production verification guide requires a development AD account, Authenticator registration, and RATAN AD-group membership. It asks teams to check successful login, user information, and expected tile visibility; its FAQ ties missing entitlements to tile access and EMS2 configuration. The production pilot guide describes Windows Hello or Authenticator login and a one-hour Entra session; that provider-session statement does not settle the portal refresh-token lifetime managed on the BFF side.

The production guide also warns that AD profile values differ from OUD values: surname formatting, country codes, and missing locale values can change. Because the BFF builds user information for downstream use, those differences can affect audit or application logic during migration. The identity-provider profile contract for downstream services remains unresolved — see [[concepts/identity-profile-attribute-migration]].

The design and production guide also disagree on activation syntax and persistence. The design uses `ENABLE_ENTRA_SSO=true/false`; the production guide uses `yes/no` and describes both temporary activation and persistent activation after first use. Those differences can produce incorrect pilot or fallback instructions and require an owner decision before they can be treated as BFF configuration rules.

Boundaries recorded by the requirement, which this page does not resolve:

- Portal-document activity is in scope; activity inside cross-origin embedded applications requires separate integration evidence.
- Expired or revoked credentials cannot authorize renewal, and recovery with no usable credential and provider failures remain separate boundaries.
- No finite fixture, including the four-hour horizon, proves indefinite execution.

Status caveats apply. The requirement is version 7, governance state `candidate`, status `draft`, and owner `unknown`; human publication review and the human ASD-STE100 review are pending. It describes requested intent and does not establish that the supplied implementation — BFF included — already satisfies any of the seven criteria. Implementation, rollout, backlog, and conformance differences belong to the independent intent-to-reality gap record, which cannot modify the criteria.

## CES migration metadata role

The candidate topic in [[summaries/KT-ces-migration-parity]] requires two new fields on EMS3 entities returned to upper applications: `roleList` and `applicationId`. It defines target metadata only; it does not establish implemented, tested, or deployed BFF response behavior.

- `roleList` must contain the corresponding CES application's `entitlements.entitlement_name` values, bound to that application. Entitlement names from another application must not populate the entity.
- `applicationId` must contain the corresponding CES application's `itam_id`. In the clarified RATAN mapping the value is `"51358"`.

The same clarification retains the existing `name` and `applicationName` fields and keeps three field meanings separate for the clarified mapping: `name` is the CES application/entity name `RATAN_ENTITLEMENT_RULE` corresponding to EMS2 `X_RATANONE`, `applicationName` stays the legacy team label `RATAN`, and the new `applicationId` field is the CES `itam_id`. CES `user_data.app_name` supplies the CES authorization name, not the legacy team label. The values are stated for this RATAN mapping only — see [[entities/ratan]], [[entities/ces]], and [[entities/ems3]].

The additions are constrained by the compatibility objective: existing entity fields and EMS2 authorization decisions must not change because of them, and the BFF must not convert multiple CES entitlement names into one selected scalar role. Role multiplicity stays an explicit compatibility concern, separate from mapped feature/action permission meaning — see [[concepts/ces-role-multiplicity]] and [[concepts/ems2-to-ces-permission-mapping]]. The source does not define where in the BFF these fields are assembled, which CES calls supply them, or how they combine with the existing EMS2 or EMS3 entitlement retrieval paths.

Related intended behavior sits in the upper-application and tile layers rather than in this BFF, and this page does not attribute it to the BFF. Each tile selects its entitlement provider independently, so an EMS2 tile keeps its existing admission logic while a CES tile uses CES admission logic and CES application identity — see [[concepts/per-tile-provider-selection]]. Existing `hasPermission(code)` calls must accept a mapped grant from either provider and log the provider that supplied an accepted grant, with no new caller argument — see [[concepts/permission-check-provider-union]]. CES saved-view and filter writes that require one owner role remain deferred until an ownership rule is agreed.

Status caveats apply. The CES migration topic is governance state `candidate`, status `draft`, owner `unknown`, and its ASD review is pending. Its stated absence of entitlement gaps is a user expectation, not retained execution proof, and no migration acceptance or deployment approval is recorded.

## Key facts from the clarification

- **Scope is bounded.** Being the only backend "in this portal scope" does not establish that the portal platform has one backend across every application.
- **Endpoint coverage is partly qualified.** The local source declares endpoints corresponding to the reported responsibilities, but no dedicated health-management controller was identified, so that label has no exact endpoint mapping.
- **Token exchange lives here.** The BFF contains an [[entities/entra]] token exchange service implementation, while the [[entities/ratan-auth-server]] copy reviewed has no identified Entra SPN integration. The clarification does not replace this source path with an inferred Auth Server hop.
- **Entitlement calls live here.** The BFF makes EMS3 entitlement calls directly, again separate from the Auth Server copy. See [[entities/ems3]] and [[concepts/entitlement-retrieval]]. The Entra design instead describes EMS2 entitlement retrieval during login. The two source statements are not reconciled here.
- **Authentication context is not proof of invocation.** The reported Auth Server scope does not prove that every portal request invokes that service; the BFF paths remain relevant on their own.

## Observability and analytics role

The analytics material in [[summaries/KT-observability-and-performance]] places analytics intake at the BFF. The documented `useAnalytics` hook submits events to `/analytics/v1/fmo/print?extend=false`, while the surrounding prose gives `/api/analytics/v1/fmo/print?extend=false` as the requested API. The two forms differ, and which path the deployed ingress actually rewrites to the BFF is unconfirmed.

- The BFF is the implied receiver for the documented interaction events — tiles, modals, workspace tabs, buttons, switches, and dropdowns. See [[concepts/interaction-analytics]].
- Example submissions attach session-derived authorization and describe deriving client addresses from request headers and the remote address. No credentials, tokens, or individual user data are reproduced here.
- The analytics models declare 20 custom attribute fields in one declaration and 10 in another. The supported producer, transport, and storage limit is unresolved, so the BFF-side intake schema cannot be treated as a fixed contract.
- Usage reporting is described through nine [[entities/kibana]] dashboards covering authentication, authentication errors, tiles, workspace movement, workspace additions, selected buttons, login choices, and themes. Whether those dashboards read data ingested through this BFF, and whether the Production dashboard exists, remains unverified.
- The BFF's service throughput is not established by the supplied material. The UAT test on `/api/auth/v2/sso/validate` reported 500 users, a 250-second ramp-up, five iterations, 17,500 successful requests, and a maximum response time of 2,023 milliseconds; the linked [[entities/apache-jmeter]] plan and result archive are absent. That same SSO validation path is the closest named surface to the renewal behavior requested in [[summaries/REQ-active-session-renewal]], but the material does not state that it performs renewal.
- Static asset caching described in [[concepts/mfe-cache-strategy]] concerns the frontend delivery path rather than BFF API responses; the two should not be conflated when reviewing headers.

## Interfaces

- Serves the portal's HTTP APIs to the frontend layers ([[entities/mfe-base]], [[entities/mfe-ratan-container]], tiles such as [[entities/mfe-cashflow-blotter]]), which call it through the shared request interceptor using the `Single-UI-Authorization` header and `Single-UI-Refresh` for relogin.
- That header contract is validated on the application-backend side by the [[entities/single-ui-sdk]] conditional servlet filter — see [[concepts/single-ui-sdk-authentication]].
- Performs the Entra authorization-code exchange and token issuance described in the migration design, including building user information and retrieving EMS2 entitlements. The separate clarification reports direct EMS3 entitlement calls, so the entitlement source remains source-specific and unresolved. The design's OneMFA fallback and username/password path are part of the same BFF responsibility statement.
- Returns EMS3 entities to upper applications; the CES migration topic requires the additive `roleList` and `applicationId` fields on those entities while keeping `applicationName` as the legacy team label. The assembly location and source calls are not established.
- Serves the admin module backend: import-map, drawer-category, and tile-configuration records, plus the documented CSV upload endpoint `/api/auth/v1/fmo/admin/config/upload` under the release-operations material. The endpoint-to-BFF mapping remains inferred.
- Exposes the analytics submission endpoint used by the frontend hook, subject to the path-form discrepancy noted above.
- Delegates identity and authorization to external providers: OUD, [[entities/fmaa]], [[entities/ems2]], [[entities/entra]], and CES — see [[concepts/identity-provider-delegation]]. The admin upload flow explicitly validates an FMAA JWT before CSV processing; how that dependency survives planned FMAA decommissioning is unresolved.
- Is the presumptive server side of the renewal and idle-expiry recovery contract requested in [[summaries/REQ-active-session-renewal]]; the requirement does not assign that behavior to a named component or endpoint.

## Open questions

- Effective deployment, DNS, and active upstreams are unconfirmed; the repository copy has no independent Git history, so file hashes identify inspected files without an upstream commit.
- Whether every application backend adopts the shared SDK in front of the BFF remains unconfirmed.
- The health-management responsibility needs clarification before endpoint-level analysis.
- Which admin endpoints the BFF actually serves, and where the input conversions and the `un-verified` to verified state change occur, is not mapped.
- Whether `/api/auth/v1/fmo/admin/config/upload` is served by this BFF, and which layer enforces FMAA JWT validation for CSV uploads, is not mapped.
- Which approval, rollback, and emergency-change records cover the separate BFF release used for first bulk inserts into UAT and Production is unresolved.
- How tenant record boundaries apply to maker and checker permissions is unresolved; the proposal discusses tenant-specific roles, while the manual lists shared admin subjects and a different-user check.
- Which release, approval, rollback, and emergency-change rules govern self-service configuration changes through the admin APIs, and which release window applies to BFF releases, is unresolved.
- Which BFF endpoint or service issues the activity-driven renewals and refresh-token exchanges described in [[summaries/REQ-active-session-renewal]], and whether the current implementation satisfies AC-1 to AC-7, is not established by that requirement.
- Whether renewal eligibility is evaluated in this BFF, in the frontend activity listeners, or in both, and how cross-origin embedded application activity could be observed at all, is unresolved.
- Which session timing rule — idle timeout, absolute timeout, and refresh-token duration — applies to BFF-issued tokens, given the conflicting version 0 and version 1 proposals summarized in [[concepts/token-lifecycle-and-timeout-policy]].
- Which Entra migration phase covers BFF session renewal, given that phase 1 explicitly excludes portal session management.
- Which activation grammar and persistence rule apply to `ENABLE_ENTRA_SSO` for the BFF's Entra exchange: `true/false`, `yes/no`, temporary activation, or persistent activation after first use.
- Which identity-provider profile contract the BFF must enforce when it builds user information from AD versus OUD values, and which downstream consumers depend on the changed surname, country, or locale fields.
- Whether the BFF's Entra token exchange retrieves EMS2 or EMS3 entitlements, how that maps to the user-stated portal-entry denial rule owned by [[entities/portal-team]], and how it relates to the separately reported direct EMS3 entitlement calls.
- Whether the BFF already returns `roleList` and `applicationId` on EMS3 entities, which CES calls populate them, and how application-scoped entitlement names are kept from leaking across applications, is unestablished by [[summaries/KT-ces-migration-parity]].
- How multiple CES roles will map to any caller contract that expects one role, given that `roleList` is a list and no scalar role projection is approved — see [[concepts/ces-role-multiplicity]].
- Which analytics model defines the supported custom attribute limit, and which fields the BFF is permitted to store or forward, is unresolved.
- Collection and retention rules for identity context and search values carried in analytics events are undocumented.
- Which tenant connectivity check proves reachability to the BFF admin service through tenant Nginx or load balancers is unresolved.
- How the planned FMAA decommissioning will affect admin CSV upload authentication and the BFF's other FMAA-dependent paths is unresolved.
- No browser measurement, telemetry query, or server-header check was run, so the BFF's production performance and response headers are unverified.

## Related

- [[summaries/ARC-portal-service-relationships]]
- [[summaries/KT-admin-and-onboarding]]
- [[summaries/KT-authentication-and-sessions]]
- [[summaries/KT-ces-migration-parity]]
- [[summaries/KT-observability-and-performance]]
- [[summaries/KT-release-operations]]
- [[summaries/KT-sdk-and-entitlements]]
- [[summaries/REQ-active-session-renewal]]
- [[entities/ces]]
- [[entities/ems2]]
- [[entities/ems3]]
- [[entities/fmo-post-trade-portal]]
- [[entities/markets-operations-one-release]]
- [[entities/portal-team]]
- [[entities/ratan]]
- [[concepts/admin-catalog-configuration]]
- [[concepts/ces-role-multiplicity]]
- [[concepts/configuration-promotion]]
- [[concepts/ems2-to-ces-permission-mapping]]
- [[concepts/entitlement-retrieval]]
- [[concepts/identity-profile-attribute-migration]]
- [[concepts/maker-checker-verification-workflow]]
- [[concepts/microfrontend-layering]]
- [[concepts/per-tile-provider-selection]]
- [[concepts/permission-check-provider-union]]
- [[concepts/session-activity-renewal]]
- [[concepts/session-expiry-prompt-recovery]]
- [[concepts/tenant-production-readiness]]
- [[concepts/token-lifecycle-and-timeout-policy]]
- [[concepts/frontend-performance]]

See also: [[summaries/KT-portal-purpose]]

See also: [[summaries/KT-architecture-evolution]]

See also: [[summaries/KT-application-interoperability]]
