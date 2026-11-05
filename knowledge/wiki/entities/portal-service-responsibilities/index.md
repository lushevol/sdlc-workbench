# Portal service responsibilities

Derived navigation, 6 November 2026.
**The linked records remain candidate/draft. Reported responsibilities do not establish active topology, universal adoption, or publication approval.**

## Frontend responsibility map

The user-reported architecture identifies Root Config, Base shell, application container, and feature tile as separate layers.
The shared shell supplies common Portal capabilities; application containers and tiles supply domain integration and views.
The composition design connects this separation with application ownership and independent delivery goals.
See [four MFE layers](../../../candidates/architecture/ARC-portal-service-relationships.md#four-mfe-layers), candidate/draft, version 1, and [composition ownership](../../../candidates/architecture/KT-frontend-composition.md#ownership-and-availability), candidate/draft, version 3.

| Layer | Reported responsibility | Named repository context |
| --- | --- | --- |
| Root Config | Supply entry resources and initialize the shell lifecycle. | `mfe-root-config` |
| Base shell | Supply themes, login, logout, sessions, tiles, drawers, and container loading. | `mfe-base` |
| Application container | Supply application routing, shared components, utilities, and related services. | `mfe-ratan-container` |
| Feature tile | Supply feature views and application functionality. | `mfe-cashflow-blotter` is an example. |

The [canonical layer table](../../../candidates/architecture/ARC-portal-service-relationships.md#four-mfe-layers) defines these reported roles.
Repository names identify the cited context rather than an exhaustive consumer inventory.

## Backend and infrastructure responsibility map

| Component | User-reported responsibility | Required distinction |
| --- | --- | --- |
| Nginx | First ingress endpoint and load-balancer routing boundary. | Reported ingress ordering requires effective configuration before deployment claims. |
| API Gateway | Second ingress endpoint, forwarding requests to application services. | Its implementation is outside the available source scope. |
| Single UI BFF | Authentication, sessions, administration, and analytics for the described Portal scope. | Sole Portal backend does not mean sole backend for every RATAN application. |
| Single UI SDK starter | Java library for application-backend JWT validation. | A library is not a deployed service or public endpoint. |
| RATAN Auth Server | Internal service authentication and external API caller authorization. | Reported responsibility does not establish a hop in every Portal request. |

See [backend roles](../../../candidates/architecture/ARC-portal-service-relationships.md#backend-and-infrastructure-roles) and [dependency boundaries](../../../candidates/architecture/ARC-portal-service-relationships.md#dependencies), candidate/draft, version 1.

These roles connect the shared platform with tenant-owned applications.
Portal authentication and SDK token validation remain distinct from application data permission enforcement.
See [SDK responsibility](../../../candidates/security/KT-sdk-and-entitlements.md#integration-purpose-and-responsibility-boundary), candidate/draft, version 8.
The [Portal capability map](../../../candidates/background/KT-portal-purpose.md#capability-boundaries), candidate/draft, version 2, supplies the wider business context.

## Proposed changes and unresolved scope

The future deployment proposal names separate authentication, tile-management, telemetry, and AI services.
Those target names do not define approved contracts, migration order, or delivered services.
Keep that proposal separate from the user-reported responsibility map.
See [proposed platform changes](../../../candidates/evolution/KT-architecture-evolution.md#platform-proposals-for-2026-and-early-2027), candidate/draft, version 2.

Effective ingress configuration, provider delegation, consumer adoption, and operational ownership require separate evidence.
The canonical [architecture limits](../../../candidates/architecture/ARC-portal-service-relationships.md#evidence-limits) retain the unavailable boundaries.
Owners remain unknown for those confirmations.
This navigation page contains no live traffic, deployed configuration, or execution claim.

## Canonical records and related topics

| Canonical record | Version | Source state |
| --- | --- | --- |
| [ARC-portal-service-relationships](../../../candidates/architecture/ARC-portal-service-relationships.md) | 1 | candidate/draft |
| [KT-frontend-composition](../../../candidates/architecture/KT-frontend-composition.md) | 3 | candidate/draft |
| [KT-sdk-and-entitlements](../../../candidates/security/KT-sdk-and-entitlements.md) | 8 | candidate/draft |
| [KT-portal-purpose](../../../candidates/background/KT-portal-purpose.md) | 2 | candidate/draft |
| [KT-architecture-evolution](../../../candidates/evolution/KT-architecture-evolution.md) | 2 | candidate/draft |

Continue with [composition and interoperability](../../concepts/portal-composition-and-interoperability/index.md), [session lifecycle](../../concepts/session-lifecycle/index.md), or [entitlement migration](../../concepts/entitlements-and-ces-migration/index.md).
Return to the [wiki index](../../index.md).
