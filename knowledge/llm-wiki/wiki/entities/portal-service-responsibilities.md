---
title: "Portal service responsibilities"
type: entity
tags: [candidate-derived, architecture]
sources: [wb-candidate-architecture-arc-portal-service-relationships, wb-candidate-architecture-kt-frontend-composition, wb-candidate-security-kt-sdk-and-entitlements, wb-candidate-background-kt-portal-purpose]
workbench_status: candidate-derived
---

# Portal service responsibilities

This entity page records responsibilities reported by the architecture candidates. It does not establish active topology, complete consumer inventory, deployment, or publication approval.

## Frontend layers

| Layer | Reported responsibility |
| --- | --- |
| Root Config | Entry resources and shell lifecycle initialization. |
| Base shell | Themes, authentication, sessions, tiles, drawers, and container loading. |
| Application container | Application routing, shared components, utilities, and related services. |
| Feature tile | Feature views and application functionality. |

The four-layer distinction and ownership boundaries come from the architecture candidates. [[wb-candidate-architecture-arc-portal-service-relationships]] [[wb-candidate-architecture-kt-frontend-composition]]

## Backend and infrastructure roles

The candidates describe Nginx and an API Gateway as ingress boundaries, the Single UI BFF as a Portal backend for authentication, sessions, administration, and analytics, the Single UI SDK starter as a JWT-validation library, and the RATAN Auth Server as an internal or external authorization boundary. [[wb-candidate-architecture-arc-portal-service-relationships]]

These reported roles do not prove that every request follows the same hop sequence or that the SDK is a deployed service. Authentication and token validation remain separate from application data permission enforcement. [[wb-candidate-security-kt-sdk-and-entitlements]]
