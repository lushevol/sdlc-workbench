---
type: Architecture
id: ARC-portal-service-relationships
version: 1
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: evidence/knowledge/sources/user-clarifications/architecture-20261022/user-message.txt
  revision: sha256:446e451dd9300d8d28028b0d51e0687e3dfb4c70e6bdbf063a2f4b9ce96c4758
  sha256: 446e451dd9300d8d28028b0d51e0687e3dfb4c70e6bdbf063a2f4b9ce96c4758
- resource: evidence/knowledge/sources/user-clarifications/architecture-20261022/source-review.json
  revision: sha256:aaf97f8c1b92df9f761092265b591d8bba7bc1a13cdaf18770d8d422a9c61628
  sha256: aaf97f8c1b92df9f761092265b591d8bba7bc1a13cdaf18770d8d422a9c61628
generated:
  by: agent:codex
  at: '2026-10-22T09:28:35.876006+00:00'
verified: []
scope: User-reported portal composition, ingress, and security responsibilities, with
  bounded local source qualifications.
components:
- MFE Root Config
- MFE Base
- RATAN Container
- Cashflow Blotter
- Nginx
- Single UI BFF
- Single UI SDK starter
- RATAN Auth Server
interfaces:
- Single-SPA lifecycle and SystemJS module loading.
- React Router paths and container/module/tile props.
- Portal HTTP APIs and the Single-UI-Authorization header.
dependencies:
- User-reported Nginx and API Gateway forwarding; effective deployment unconfirmed.
- Application backend library adoption; exact downstream consumers unconfirmed.
- Auth delegation to identity and entitlement providers; implementation scope qualified
  below.
decisions:
- Record current architecture clarification as candidate knowledge.
- Keep user-reported topology separate from source-extracted relationships.
- Exclude unavailable API Gateway implementation from this review.
related:
- KT-frontend-composition
- KT-authentication-and-sessions
- KT-sdk-and-entitlements
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Portal composition and service relationships

## Scope

The user supplied the [architecture clarification](../../../evidence/knowledge/sources/user-clarifications/architecture-20261022/user-message.txt) on 22 October 2026.
It explains the portal layers, ingress, backend, SDK, and RATAN authentication responsibilities.
The [source review](../../../evidence/knowledge/sources/user-clarifications/architecture-20261022/source-review.json) checks selected local declarations.
This record changes no application behavior and grants no publication approval.
The clarification identifies no effective deployment, complete consumer inventory, or authenticated architecture owner.

## Components

### Four MFE layers

| Order | Layer | Repository | Responsibility |
| --- | --- | --- | --- |
| 1 | Base | `mfe-root-config` | Supply HTML and static entry resources. Initialize Single-SPA and register only MFE Base. |
| 2 | Shell | `mfe-base` | Supply themes, login, logout, sessions, tiles, drawers, and remote container loading. |
| 3 | Container | `mfe-ratan-container` | Supply application routing, shared components, utilities, and related services. |
| 4 | Tile | `mfe-cashflow-blotter` example | Render feature views and application functionality. |

The [user clarification](../../../evidence/knowledge/sources/user-clarifications/architecture-20261022/user-message.txt#L7-L10) supplies this responsibility model.
Root layout declares only `@fm/base`.
See the [layout](../../../repos/ui/mfe-root-config/src/microfrontend-layout.html#L1-L5) and [root bootstrap](../../../repos/ui/mfe-root-config/src/root.ts#L10-L27).
The [source review](../../../evidence/knowledge/sources/user-clarifications/architecture-20261022/source-review.json) records file hashes and independent revisions.

### Backend and infrastructure roles

| Component | User-reported responsibility | Source qualification |
| --- | --- | --- |
| Nginx | First ingress endpoint; rules belong to the RATAN Ansible load-balancer scope. | Local templates exist. The wider Ansible repository and rendered deployment are unavailable. |
| API Gateway | Second ingress endpoint; forwards requests to application services. | No gateway repository is available. Implementation analysis remains excluded. |
| Single UI BFF | Sole backend for the described portal scope; authentication, sessions, administration, and analytics. | Source declares corresponding endpoints. The health-management label has no confirmed dedicated endpoint. |
| Single UI SDK starter | Java library for application backend JWT validation. | Source supplies a conditional servlet filter. Universal consumer adoption remains unconfirmed. |
| RATAN Auth Server | Internal service authentication and external API caller authorization. | Source supports several strategies. Not every reported provider appears in this copy. |

The [user clarification](../../../evidence/knowledge/sources/user-clarifications/architecture-20261022/user-message.txt#L16-L22) supplies these roles.
The [source review](../../../evidence/knowledge/sources/user-clarifications/architecture-20261022/source-review.json) separates inspected declarations from reported scope.
The SDK remains a library. Its repository does not establish a deployed service or public endpoint.

## Interfaces

### Loading, routing, and props

Single-SPA registers the shell; SystemJS loads named modules.
The shell selects `props.container` and forwards `module`, `tile`, `parameters`, `panelId`, and `tabId`.
See the [shell loader](../../../repos/ui/mfe-base/src/pages/Home/common/Container.tsx#L10-L32).

The container uses `props.module` to select its route.
A selected loader imports the tile and forwards props.
See the [container routing](../../../repos/ui/mfe-ratan-container/src/Root/routing/common/useController.ts#L6-L13) and [tile loader](../../../repos/ui/mfe-ratan-container/src/Root/import/CashFlowCN.tsx#L7-L20).
The tile uses `props.tile` for its feature route.
See the [tile routing](../../../repos/ui/mfe-cashflow-blotter/src/Root/routing/common/useController.ts#L7-L15).

These are distinct routing and loading stages.
Shared-code imports also flow from containers and tiles back to shell and container libraries.
The [tile imports](../../../repos/ui/mfe-cashflow-blotter/src/Root/import/ratancomponents/index.ts#L2-L75) show shared container reuse.
The user describes JavaScript entry bundles. Lazy loading permits additional chunks.
The [source review](../../../evidence/knowledge/sources/user-clarifications/architecture-20261022/source-review.json) retains that qualification.

### HTTP and token interfaces

The user reports a common public domain with DNS forwarding to Nginx, followed by API Gateway.
The logical MFE-to-BFF contract remains distinct from this reported transport path.
DNS, effective upstreams, gateway routes, and active deployment remain unverified.
The [Nginx template](../../../repos/infra/nginx/ratan_servers.conf.j2#L150-L256) includes gateway routes and direct proxy exceptions.

The shared frontend interceptor uses `Single-UI-Authorization`.
Authentication, analytics, and SSE requests include exceptions; relogin uses `Single-UI-Refresh`.
See the [request interceptor](../../../repos/ui/mfe-base/src/hooks/service/util/success.request.handler.ts#L17-L28).
The [SDK filter](../../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/filter/AuthTokenFilter.java#L83-L108) validates supported requests and supplies attributes.

## Dependencies

### Portal and SDK boundaries

The user reports Single UI BFF as the sole backend in this portal scope.
This does not establish that RATAN has one backend across every application.
SDK adoption across application backends remains reported architecture because those exact consumers are unavailable.
The [SDK configuration](../../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/config/AuthConfiguration.java#L19-L31) conditionally registers validation.

### RATAN authentication and authorization

The user reports authentication delegation to OUD, Entra SPN, and FMAA.
The user reports authorization delegation to EMS2 and EMS3.
The [source review](../../../evidence/knowledge/sources/user-clarifications/architecture-20261022/source-review.json) supports local OUD, FMAA, and EMS2 paths.

This Auth Server copy has no identified Entra SPN or EMS3 implementation.
BFF separately contains [Entra token exchange](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v1/implementation/EntraAuthenticationServiceImpl.java#L41-L57) and [EMS3 calls](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/filter/ems3/Ems3EntitlementService.java#L85-L93).
These source paths remain relevant. The clarification does not replace them with an inferred Auth Server hop.
The reported Auth Server scope does not prove that every portal request invokes this service.

## Decisions

Retain the explanation as candidate architecture with source qualifications.
Keep reported topology separate from source-extracted joins and runtime verification.
Keep API Gateway visible as an unavailable boundary without inspecting its implementation.
This record authorizes no business implementation, release, or publication.

## Connections

[Frontend composition](KT-frontend-composition.md#current-four-layer-clarification) retains historical design context and links this clarification.
[Authentication and sessions](../security/KT-authentication-and-sessions.md) retains portal authentication and policy context.
[SDK and entitlements](../security/KT-sdk-and-entitlements.md) retains token and authorization distinctions.
Those policy records retain their separate versions, sources, and review state.

## Evidence limits

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| User clarification has no deployment identifier. | Reported topology cannot establish active DNS or gateway forwarding. | unknown | Obtain effective configuration when deployment confirmation becomes necessary. |
| Nginx templates include direct proxy routes. | The supplied copy cannot establish universal gateway traversal. | unknown | Compare rendered routes with the reported environment. |
| Auth copy lacks identified Entra SPN and EMS3 integrations. | Reported provider delegation remains unconfirmed locally. | unknown | Inspect the applicable Auth revision when implementation confirmation becomes necessary. |
| BFF has admin endpoints but no identified health-management controller. | That responsibility has no exact endpoint mapping. | unknown | Clarify the term when endpoint-level analysis requires it. |
| Four repositories have no independent Git history. | Hashes identify inspected files without an upstream commit. | unknown | Obtain original repository revisions when available. |

The [source review](../../../evidence/knowledge/sources/user-clarifications/architecture-20261022/source-review.json) retains exact locators, hashes, revisions, and source limits.
This review executed no live requests, browser behavior, or business tests.
No required business behavior changed, so this record adds no acceptance criterion.
