# Portal composition and service relationships

Derived navigation. Source state: candidate/draft. This page grants no approval.

[Wiki index](../../index.md)

Canonical record: [ARC-portal-service-relationships, version 1](../../../candidates/architecture/ARC-portal-service-relationships.md#L2-L7).

## Summary

This candidate records user-reported portal layers and service responsibilities.
It separates reported topology from source qualifications and runtime verification.
See the canonical [scope](../../../candidates/architecture/ARC-portal-service-relationships.md#scope) and [decisions](../../../candidates/architecture/ARC-portal-service-relationships.md#decisions).

## Key rules and qualifiers

- The reported layers are Root Config, Base shell, application container, and feature tile.
  See [four MFE layers](../../../candidates/architecture/ARC-portal-service-relationships.md#four-mfe-layers).
- Reported BFF responsibilities include authentication, sessions, administration, and analytics within the described portal scope.
  See [backend roles](../../../candidates/architecture/ARC-portal-service-relationships.md#backend-and-infrastructure-roles).
- The SDK remains a library. Universal downstream adoption remains unconfirmed.
  See [portal and SDK boundaries](../../../candidates/architecture/ARC-portal-service-relationships.md#portal-and-sdk-boundaries).
- Logical frontend-to-BFF contracts remain distinct from reported DNS, Nginx, and gateway transport paths.
  See [HTTP and token interfaces](../../../candidates/architecture/ARC-portal-service-relationships.md#http-and-token-interfaces).
- Reported authentication delegation does not establish that every portal request invokes RATAN Auth Server.
  See [authentication and authorization](../../../candidates/architecture/ARC-portal-service-relationships.md#ratan-authentication-and-authorization).

## Unresolved questions

- Which effective deployment confirms DNS, gateway forwarding, and direct proxy exceptions?
- Which applicable Auth revision confirms the reported Entra SPN and EMS3 delegation?
- Which exact endpoint defines the reported health-management responsibility?

These questions follow the canonical [evidence limits](../../../candidates/architecture/ARC-portal-service-relationships.md#evidence-limits).
Owner: unknown. Next action: obtain the applicable configuration, revisions, and responsibility clarification.

## Connections

- [Frontend composition](../KT-frontend-composition/index.md)
- [Authentication and sessions](../KT-authentication-and-sessions/index.md)
- [SDK and entitlements](../KT-sdk-and-entitlements/index.md)

The canonical [connections](../../../candidates/architecture/ARC-portal-service-relationships.md#connections) define these relationships.
