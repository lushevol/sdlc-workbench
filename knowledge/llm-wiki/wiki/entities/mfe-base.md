---
sources: ["summaries/KT-ces-migration-parity.md", "summaries/KT-authentication-and-sessions.md", "summaries/REQ-active-session-renewal.md", "summaries/KT-release-operations.md", "summaries/KT-admin-and-onboarding.md", "summaries/KT-observability-and-performance.md", "summaries/KT-architecture-evolution.md", "summaries/KT-portal-purpose.md", "summaries/KT-frontend-composition.md", "summaries/ARC-portal-service-relationships.md"]
type: "Product"
description: "MFE Base is the Single-SPA shell layer supplying themes, routing, sessions, and the shared permission and request APIs."
---

> Derived candidate/draft knowledge; publication review remains pending. [Canonical source bindings](../../source-manifest.json).

# MFE Base

MFE Base (`mfe-base`) is the **shell layer** — layer 2 of the four-layer microfrontend stack described in [[summaries/ARC-portal-service-relationships]] and [[concepts/microfrontend-layering]]. It sits between the [[entities/mfe-root-config]] bootstrap and the [[entities/mfe-ratan-container]] container layer, and is the only remote module registered by the root config (the root layout declares only `@fm/base`).

As the shared base, it supplies the common context that tenant-owned containers and tiles consume; application teams supply the containers and tiles themselves under the [[concepts/application-ownership]] model.

## Responsibilities

According to the user-reported responsibility model and the documented development principles, MFE Base supplies:

- Themes and shared MUI theme context ([[entities/mui]])
- Common routing and global state
- Login and logout flows
- Sessions
- Tiles and drawers
- Remote container loading
- The shared frontend request interceptor used across the portal

The development guideline additionally separates view, logic, styles, and interfaces within the shared code and prefers Context and Reducer over additional state libraries — consistent with the shell carrying global state rather than delegating it to a state framework.

## Session behavior

The shell is responsible for portal session interactions. Version 8 of the [canonical session requirement](../sources/REQ-active-session-renewal.md) is a draft owned by the RATAN team under ICS bank security policy. Idle timeout is at most 15 minutes. Absolute timeout is at most 60 minutes from portal authentication and applies during activity and renewal. [Canonical renewal criteria](../sources/REQ-active-session-renewal.md#acceptance-criteria)

| Criterion | Setup and expected result |
| --- | --- |
| AC-1–AC-3 | Mouse movement, keyboard input, or scrolling every 100 ms for 15 seconds each yields at least one successful renewal, with at least 30 seconds left before both access and absolute expiry. |
| AC-4 | If the initial refresh credential expires first and access remains valid, eligible activity before the absolute deadline yields at least one subsequent renewal in the same portal session. |
| AC-5–AC-7 | Before absolute expiry, the idle-expiry prompt stays open while renewal is pending, closes once after success, and allows retry after rejection while the refresh token remains usable and time remains. |
| AC-8 | With more than 15 minutes left before absolute expiry, 15 minutes without eligible activity or manual renewal reaches idle expiry within 15 minutes of the last eligible activity. |
| AC-9 | Even with successful renewal and eligible activity, the earlier of the configured absolute timeout and 60 minutes ends the session. It can no longer complete protected requests or renewals. |

Cross-origin embedded application activity needs separate integration evidence. The user also described an ideal of immediate revocation of all portal sessions at logout, excluding the identity-provider session. The implementation and independent execution evidence do not establish deployed conformance. [Canonical logout criterion](../sources/KT-authentication-and-sessions.md#portal-logout-ac-001)

## CES migration compatibility

MFE Base is explicitly inside the frontend compatibility scope of the EMS2-to-CES entitlement migration, together with the shared Ratan container and their upper applications, from 6 November 2026 ([[summaries/KT-ces-migration-parity]]).

- **Compatibility first.** Established upper-application caller contracts must be preserved where possible; provider-specific identities and permission data are adapted inside the shell and container APIs. The user names non-unique CES roles as the known compatibility gap — that statement does not establish that every other API is compatible.
- **Per-tile provider selection.** Each tile selects its entitlement provider independently. An EMS2 tile keeps its existing admission logic; a CES tile uses CES admission logic, its configured application identity, and the CES permission structure ([[concepts/per-tile-provider-selection]]). Moving one tile to [[entities/ces]] must not force provider changes on unrelated tiles.
- **Provider-union permission check.** Existing `hasPermission(code)` calls may accept a mapped grant from either EMS2 or CES, must log which provider supplied an accepted grant, and must not require a new caller scope argument ([[concepts/permission-check-provider-union]]). This shared functional check stays separate from tile admission.
- **Role multiplicity stays separate.** Multiple CES assignments must not be represented as one proven scalar role; callers expecting a single role need a sourced business mapping ([[concepts/ces-role-multiplicity]]). CES saved-view and filter writes that require one owner role stay deferred until an ownership rule is agreed.
- **Additive CES entity metadata.** The two new EMS3 entity fields are `roleList` (CES `entitlements.entitlement_name` values) and `applicationId` (CES `itam_id`). The existing `applicationName` retains the legacy team label, and the existing `name` carries the clarified CES application name. These additions must not remove existing fields or change EMS2 decisions. See [[concepts/ems2-to-ces-permission-mapping]] and [[entities/ems3]].

These are user-stated intentions with acceptance criteria defined elsewhere; the sources do not establish implemented, tested, or deployed shell behavior, and no human review is recorded.

## Interfaces

### Loading and props

[[entities/single-spa]] registers the shell; [[entities/systemjs]] resolves registered names to deployed files and loads the named modules. MFE Base selects `props.container` and forwards `module`, `tile`, `parameters`, `panelId`, and `tabId` down to the container. This is the entry point of the routing chain documented at [[concepts/portal-entry-and-tile-authorization]].

Shared-code imports flow back from containers and tiles into shell and container libraries, so MFE Base also acts as a shared library source for [[entities/mfe-ratan-container]] and [[entities/mfe-cashflow-blotter]]. Because shared dependencies require coordinated upgrades, a change to a shell interface can affect several tenant consumers; see [[concepts/shared-dependency-governance]].

### HTTP and token handling

The shared interceptor applies the `Single-UI-Authorization` header to portal requests, with exceptions for authentication, analytics, and server-sent-event requests; relogin uses `Single-UI-Refresh`. The documented downstream SDK filter validates supported requests where it is adopted and enabled; see [[concepts/single-ui-sdk-authentication]] and the [canonical boundary](../../../candidates/architecture/ARC-portal-service-relationships.md#portal-and-sdk-boundaries). The [candidate session requirement](../../../candidates/requirements/REQ-active-session-renewal.md) defines renewal and idle-expiry prompt outcomes. Mapping those outcomes to interceptor or session code requires separate implementation evidence.

### Permission API

The intended `hasPermission(code)` API accepts a mapped grant from either EMS2 or CES and logs a provider that supplied an accepted grant. [FE-COMPAT-AC-004](../../../candidates/security/KT-ces-migration-parity.md#fe-compat-ac-004) defines the result and logging contract. Its transport and any interceptor dependency require separate implementation evidence.

### Templates for new applications

The frontend onboarding procedure starts from container and tile templates held in the shared code. It updates names, webpack configuration, interfaces, entry points, tests, and the local import map before application registration is linked through the admin manual. Each application supplies its own build pipeline and informs the portal team about its static-file and API URLs, so the shell templates define the shape of a new module without owning its delivery pipeline. See [[concepts/frontend-onboarding]] and [[entities/portal-team]].

## Administrative configuration

Tile and category data reach the shell through portal catalog records rather than through shell code. The admin overview records that the earlier process changed `mfe-base` source and raised a production change request for every tile update; the proposal seeks tenant-maintained, self-service configuration to reduce that repeated release work. The proposal reuses [[entities/single-ui-bff]] as the admin backend and does not establish an approved exemption from production change controls.

Because catalog changes reach deployed tiles through the import map and the shell's container loading, MFE Base is the runtime consumer of [[concepts/admin-catalog-configuration]] and of the [[concepts/portal-tile-workspace-model]]. MFE Base itself is not described as an admin client: the maker-checker review defined in [[concepts/maker-checker-verification-workflow]] governs catalog records, while shell interfaces are governed by shared-repository review.

## Development standards

The documented guideline prescribes TypeScript, functional components, shared MUI themes, and separation of view, logic, styles, and interfaces. It names React 18.2.0 ([[entities/react]]) and prefers Context and Reducer over additional state libraries.

These versioned instructions carry no effective-date or supersession record in the sources, so they cannot establish the current platform baseline. Reuse for new development should retain the source context and be confirmed against [[concepts/frontend-onboarding]].

## Relationships

| Neighbor | Relationship |
| --- | --- |
| [[entities/mfe-root-config]] | Bootstraps Single-SPA and registers only MFE Base |
| [[entities/mfe-ratan-container]] | Loaded by the shell; receives `module` and UI props; shares the CES migration compatibility scope |
| [[entities/mfe-cashflow-blotter]] | Tile reached through the container's tile loader |
| [[entities/single-ui-bff]] | Backend that the interceptor's authenticated calls target; also the reused admin backend in the proposal |
| [[entities/portal-team]] | Receives static-file and API URLs from each onboarding application |
| [[entities/ems2]] / [[entities/ces]] | Entitlement providers whose grants the shared permission check may accept |
| `mfe-base` shared repositories | Reviewed and approved by the microfrontend team, per the development principles |

Ingress to the portal ([[entities/nginx]], then [[entities/api-gateway]]) is described at [[concepts/portal-ingress-path]]; identity and entitlement decisions behind the session live with [[entities/ratan-auth-server]] under [[concepts/identity-provider-delegation]] and [[concepts/entitlement-retrieval]]. The RATAN application mapping that supplies CES entity metadata is recorded at [[entities/ratan]].

## Evidence notes

The responsibility list comes from a user clarification and the documented design, not from an independently verified deployment. The container-loading behavior is supported by the shell loader source (`mfe-base/src/pages/Home/common/Container.tsx`); the interceptor behavior by `mfe-base/src/hooks/service/util/success.request.handler.ts`. The described JavaScript entry bundles may be split into additional lazy-loaded chunks.

The administrative context comes from a proposal and a procedural manual; their source revisions and current applicability are unconfirmed, and the manual depends on screenshots absent from its copy. Whether the self-service catalog replaced source changes for tile updates in production is not established.

The session criteria come from version 8 of the candidate requirement owned by the RATAN team under ICS bank security policy. Human review and deployed conformance remain pending.

The CES migration statements come from a candidate knowledge topic (version 6, owner unknown) built on dated user clarifications from 3–9 November 2026. They record intended permission preservation, compatibility, and per-tile migration behavior only; they do not establish implemented shell behavior, complete API compatibility, an approved scalar role mapping, or deployed log collection.

Evidence limits: the sources identify local bytes without original page revisions or confirmed source authority; runtime rendering, accepted dependency versions, and active deployment are unconfirmed. Named owners and effective approvals of the shell remain unknown.

## Related Documents
- [[summaries/KT-frontend-composition]]
- [[summaries/KT-admin-and-onboarding]]
- [[summaries/REQ-active-session-renewal]]
- [[summaries/KT-ces-migration-parity]]

See also: [[summaries/KT-portal-purpose]]

See also: [[summaries/KT-architecture-evolution]]

See also: [[summaries/KT-observability-and-performance]]

See also: [[summaries/KT-release-operations]]

See also: [[summaries/KT-authentication-and-sessions]]
