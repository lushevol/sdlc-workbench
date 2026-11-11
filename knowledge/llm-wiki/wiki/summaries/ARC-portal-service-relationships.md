---
type: "Summary"
description: "Maps the four-layer portal MFE stack, ingress, BFF, SDK, and RATAN auth responsibilities with evidence limits."
doc_type: short
full_text: "sources/ARC-portal-service-relationships.md"
---

> Derived from [ARC-portal-service-relationships, version 1](../../../candidates/architecture/ARC-portal-service-relationships.md), candidate/draft. [Source bindings](../../source-manifest.json).

# Portal composition and service relationships — Summary

Candidate architecture record of the portal's layers, ingress, backend, SDK, and RATAN authentication responsibilities.

## Scope

A user-supplied architecture clarification dated 22 October 2026 explains the portal layers, ingress, backend, SDK, and RATAN authentication responsibilities. A companion source review checks selected local declarations. The record changes no application behavior and grants no publication approval. The clarification identifies no effective deployment, no complete consumer inventory, and no authenticated architecture owner.

## Components

### Four MFE layers

| Order | Layer | Repository | Responsibility |
| --- | --- | --- | --- |
| 1 | Base | [[entities/mfe-root-config]] | Supply HTML and static entry resources. Initialize [[entities/single-spa]] and register only MFE Base. |
| 2 | Shell | [[entities/mfe-base]] | Supply themes, login, logout, sessions, tiles, drawers, and remote container loading. |
| 3 | Container | [[entities/mfe-ratan-container]] | Supply application routing, shared components, utilities, and related services. |
| 4 | Tile | [[entities/mfe-cashflow-blotter]] | Render feature views and application functionality. |

This responsibility model matches the [[concepts/microfrontend-layering]] pattern of a root-config base, a shell, a container, and feature tiles. The root layout declares only `@fm/base`; the layout file and root bootstrap confirm it, and the source review records file hashes and independent revisions.

### Backend and infrastructure roles

| Component | User-reported responsibility | Source qualification |
| --- | --- | --- |
| [[entities/nginx]] | First ingress endpoint; rules belong to the RATAN Ansible load-balancer scope. | Local templates exist. The wider Ansible repository and rendered deployment are unavailable. |
| [[entities/api-gateway]] | Second ingress endpoint; forwards requests to application services. | No gateway repository is available. Implementation analysis remains excluded. |
| [[entities/single-ui-bff]] | Sole backend for the described portal scope; authentication, sessions, administration, and analytics. | Source declares corresponding endpoints. The health-management label has no confirmed dedicated endpoint. |
| [[entities/single-ui-sdk]] starter | Java library for application backend JWT validation. | Source supplies a conditional servlet filter. Universal consumer adoption remains unconfirmed. |
| [[entities/ratan-auth-server]] | Internal service authentication and external API caller authorization. | Source supports several strategies. Not every reported provider appears in this copy. |

The source review separates inspected declarations from reported scope. The SDK remains a library; its repository does not establish a deployed service or public endpoint.

## Interfaces

### Loading, routing, and props

Single-SPA registers the shell; SystemJS loads named modules. The shell selects `props.container` and forwards `module`, `tile`, `parameters`, `panelId`, and `tabId`.

The container uses `props.module` to select its route. A selected loader imports the tile and forwards props. The tile uses `props.tile` for its feature route. These are distinct routing and loading stages and map to the [[concepts/portal-entry-and-tile-authorization]] path of container-to-tile entry.

Shared-code imports also flow from containers and tiles back to shell and container libraries, showing shared container reuse. The user describes JavaScript entry bundles; lazy loading permits additional chunks. The source review retains that qualification.

### HTTP and token interfaces

The user reports a common public domain with DNS forwarding to Nginx, followed by API Gateway — the reported [[concepts/portal-ingress-path]]. The logical MFE-to-BFF contract remains distinct from this reported transport path. DNS, effective upstreams, gateway routes, and active deployment remain unverified. The Nginx template includes gateway routes and direct proxy exceptions.

The shared frontend interceptor uses `Single-UI-Authorization`. Authentication, analytics, and SSE requests include exceptions; relogin uses `Single-UI-Refresh`. The SDK filter validates supported requests and supplies attributes, consistent with [[concepts/single-ui-sdk-authentication]].

## Dependencies

### Portal and SDK boundaries

The user reports Single UI BFF as the sole backend in this portal scope. This does not establish that RATAN has one backend across every application. SDK adoption across application backends remains reported architecture because those exact consumers are unavailable. The SDK configuration conditionally registers validation.

### RATAN authentication and authorization

The user reports authentication delegation to OUD, Entra SPN, and FMAA, and authorization delegation to [[entities/ems2]] and [[entities/ems3]] — the general pattern of [[concepts/identity-provider-delegation]] and [[concepts/entitlement-retrieval]]. The source review supports local OUD, FMAA, and EMS2 paths.

This Auth Server copy has no identified Entra SPN or EMS3 implementation. BFF separately contains Entra token exchange and EMS3 calls. These source paths remain relevant; the clarification does not replace them with an inferred Auth Server hop. The reported Auth Server scope does not prove that every portal request invokes this service.

## Decisions

Retain the explanation as candidate architecture with source qualifications. Keep reported topology separate from source-extracted joins and runtime verification. Keep API Gateway visible as an unavailable boundary without inspecting its implementation. This record authorizes no business implementation, release, or publication.

## Connections

Frontend composition retains historical design context and links this clarification. Authentication and sessions retains portal authentication and policy context. [[summaries/KT-sdk-and-entitlements]] retains token and authorization distinctions. Those policy records retain their separate versions, sources, and review state.

## Evidence limits

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| User clarification has no deployment identifier. | Reported topology cannot establish active DNS or gateway forwarding. | unknown | Obtain effective configuration when deployment confirmation becomes necessary. |
| Nginx templates include direct proxy routes. | The supplied copy cannot establish universal gateway traversal. | unknown | Compare rendered routes with the reported environment. |
| Auth copy lacks identified Entra SPN and EMS3 integrations. | Reported provider delegation remains unconfirmed locally. | unknown | Inspect the applicable Auth revision when implementation confirmation becomes necessary. |
| BFF has admin endpoints but no identified health-management controller. | That responsibility has no exact endpoint mapping. | unknown | Clarify the term when endpoint-level analysis requires it. |
| Four repositories have no independent Git history. | Hashes identify inspected files without an upstream commit. | unknown | Obtain original repository revisions when available. |

The source review retains exact locators, hashes, revisions, and source limits. The review executed no live requests, browser behavior, or business tests. No required business behavior changed, so the record adds no acceptance criterion.

## Entities
- [[entities/fmo-post-trade-portal]]
- [[entities/portal-team]]
