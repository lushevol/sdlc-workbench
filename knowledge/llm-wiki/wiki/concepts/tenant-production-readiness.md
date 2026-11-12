---
type: "Concept"
sources: ["summaries/KT-authentication-and-sessions.md", "summaries/KT-release-operations.md"]
description: "Separating technical deployment evidence from business activation before a tenant goes live."
---

> Derived candidate/draft knowledge; publication review remains pending. [Canonical source bindings](../../source-manifest.json).

# Tenant Production Readiness

Tenant production readiness is the evidence-backed state in which a tenant's applications are both technically deployed through the [[entities/fmo-post-trade-portal]] and accepted by the business that depends on them. In the supplied [[summaries/KT-release-operations]] materials, readiness is defined by two separate questions: has the technical path been proven, and has the business confirmed that the delivered capability works?

## Two gates, not one

Technical readiness covers Portal-to-tenant reachability, routing, configuration, and deployment of the application artifact. Business readiness covers validation, user acceptance, and adoption by named user groups.

The release calendar separates Portal release dates from tenant release dates, and lists separate Entra technical and business go-live entries. The OpenFin briefing also separates technical onboarding from business user onboarding. The DDR request states that business UAT sign-off follows technical go-live and records separate technical and business target dates. The VPA request separates Portal and application go-live dates, and the request template explicitly allows Portal deployment before the application deployment.

A calendar entry or a date therefore establishes planning context only. It does not prove deployment, approval, or successful adoption. Combine this with [[concepts/release-window-governance]] to understand when the work may be scheduled, and with the ownership rules in [[concepts/application-ownership]] to understand who accounts for which gate.

## Requested readiness inputs

The release proposal asks for solution intent, user profiles, routing details, connectivity checks, UAT sign-off, and rollback planning, and requires 30 days of engagement for new interfaces. The unfinished checklist adds SDK validation, shared frontend requests, entitlement checks, disaster recovery, performance inputs, operating agreements, and penetration testing. The blank request template adds DNS resolution, expected total/new/concurrent users, routing changes, connectivity evidence, sign-off, and UVT contacts.

These describe what a complete request should contain. They do not show that any particular tenant satisfied them.

The unfinished checklist calls for tenant review with RATAN before preparing each production release and gives the tenant responsibility for checking its new upstream host for disaster recovery. A separate production checklist includes viewing the sign-in page before authentication. [Canonical release guidance](../../../candidates/operations/KT-release-operations.md#readiness-before-scheduling).

## Evidence gaps observed

The supplied requests demonstrate how readiness evidence can be missing or withdrawn:

- The CDUPS request leaves UAT sign-off, user profiles, user counts, and UVT details unprovided.
- The DDR request records pending connectivity and separates technical sign-off from business validation.
- Several VPA evidence references are struck through.

A missing or struck-through reference cannot establish the corresponding release gate. A target date alone cannot establish release readiness or acceptance.

## Connectivity and network boundary

The production checklist recommends that Portal connections reach tenants through tenant Nginx or load balancers. Tenant teams then control internal server and port changes behind that boundary. The checklist treats browser reachability, Portal-to-tenant connectivity, operating agreements, security testing, and tile release as distinct checks. Successful configuration upload alone does not establish business readiness.

For the mechanics of that path, see [[concepts/portal-ingress-path]] and the related authentication handoff in [[concepts/cross-application-authentication-handoff]].

## Relationship to configuration promotion

The documented promotion flow uploads Module Map, Drawer Category, and Tile Configuration CSV records to the Portal Admin service. It connects to separate routing, authentication, entitlement, and validation prerequisites; the supplied guide does not establish that all of those settings are uploaded. See [[concepts/configuration-promotion]] and [[concepts/admin-catalog-configuration]]. Promotion is a technical prerequisite for tile visibility, but tile visibility is not business acceptance. The planned FMAA decommissioning flagged in the checklist remains an unresolved dependency for that promotion workflow.

## Why this separation matters

The historical deployment guides describe mechanisms that may no longer be current: an older static-artifact, blue-green proposal with a shared Pilot and Production backend, and an Nginx draft proposing versioned configuration, syntax checks, restart checks, and rollback. Neither establishes the currently deployed pipeline.

If one gate is treated as proof of the other, planned dates get mistaken for delivered capability, and releases can proceed toward a business activation that no one has actually validated. Readiness should be retained as evidence per gate: configuration, connectivity, technical sign-off, and business sign-off.

## Related pages

- [[summaries/KT-release-operations]]
- [[concepts/release-window-governance]]
- [[concepts/configuration-promotion]]
- [[concepts/portal-ingress-path]]
- [[concepts/application-ownership]]
- [[entities/markets-operations-one-release]]
- [[entities/portal-team]]
- [[entities/nginx]]
- [[entities/fmaa]]
- [[entities/cdups]], [[entities/ddr]], [[entities/vpa]], [[entities/fss]]
- [[entities/entra]], [[entities/openfin]]


See also: [[summaries/KT-authentication-and-sessions]]
