---
type: "Summary"
description: "Documents a four-layer microfrontend model, ownership rules, and onboarding flow."
doc_type: short
full_text: "sources/KT-frontend-composition.md"
---

> Derived from [KT-frontend-composition, version 4](../../../records/candidates/architecture/KT-frontend-composition.md), candidate/draft. [Source bindings](../../source-manifest.json).

# Frontend composition and application ownership

## Overview

This topic documents a microfrontend composition model that separates shared platform modules from independently owned application modules. The reported design has four layers: root configuration/import map, base shell, application container, and feature tile — the arrangement described in [[concepts/microfrontend-layering]]. [[entities/single-spa]] registers the shell, while import maps and [[entities/systemjs]] resolve and load modules. React Router then supports successive container and tile loading.

The architecture clarification is bounded: it records current local declarations but does not establish runtime rendering, accepted dependency versions, or active deployment. Deployed interface compatibility remains unconfirmed.

## Composition roles

| Element | Documented responsibility |
| --- | --- |
| Root configuration and import map | Locate modules and support shared loading configuration. |
| [[entities/systemjs]] | Resolve module names to files and load modules. |
| [[entities/single-spa]] | Mount applications and manage lifecycle. |
| Base container | Provide common routing, global state, and theme context. |
| Application container | Connect domain modules with the shared portal. |
| Feature tiles | Supply user-facing domain views within workspaces. |
| [[entities/nginx]] | Route application static files and API requests. |

Historical scan notes describe unauthenticated access to non-sensitive static files. The note concerns direct file retrieval and supplies no rule for directory listing, portal entry, or protected APIs. [Canonical source scope](../../../records/candidates/architecture/KT-frontend-composition.md#roles-in-composition).

## Ownership and delivery

The design assigns shared backend availability and shared-repository review to the microfrontend team. Its organizational relationship with the [[entities/portal-team]] remains unconfirmed. Application teams own domain backend availability, choose their deployment approach, and supply static-file and API URLs. The intended benefits are independent releases, narrower testing, clearer [[concepts/application-ownership]], and reusable components such as those in [[entities/mfe-base]].

Current named owners and effective approvals are unknown. The source records role declarations rather than confirmed organizational authority.

## Onboarding sequence

The documented [[concepts/frontend-onboarding]] flow is:

1. Obtain root configuration and application templates.
2. Create separate application container and tile repositories.
3. Update module names, build configuration, imports, interfaces, and container entry points.
4. Update unit tests and the local import map.
5. Configure the tile through the Admin Module procedure.
6. Build and deploy application files, then supply static-file and API URLs to the platform team.

## Shared code and standards

Modules are shared through exports, imports, and registered names. Shared dependencies require coordinated upgrades; a shared interface change can affect several tenant consumers, though this inference needs exact provider and consumer evidence. This is the concern covered by [[concepts/shared-dependency-governance]].

The development guideline prescribes TypeScript, functional components, shared MUI themes, and separation of view, logic, styles, and interfaces. It names React 18.2.0 and prefers Context and Reducer over additional state libraries. The same versioned guidance calls for component error boundaries and prefers lazy tile loading where possible. Its current applicability requires review. [Canonical development guidance](../../../records/candidates/architecture/KT-frontend-composition.md#development-guidance-and-performance-boundaries).

Optional loading guidance suggests 500 KB files and six concurrent static-file requests, but does not establish an accepted performance SLA. The external frontend dependency control principle prohibits direct external GUI dependencies without platform review and approval, with tenant teams retaining security, licensing, vulnerability, support, resilience, and rollback responsibilities.

The standalone [[entities/react]] template reuses MFE-Base components through import-map registration. Its no-install statement concerns consuming those components; the template still installs its own dependencies.

## Evidence limits

The source manifest identifies local bytes but not original page revisions or confirmed source authority. Missing archives and screenshots prevent full reproduction of the getting-started and standalone setup procedures. The guideline names an older React version without an effective-date or supersession record. The framework comparison contains scores and opinions without retained project measurements, so it is historical rationale rather than current performance evidence.

## Open questions

- Which repository revisions implement the current container, tile, and routing interfaces?
- Which development guidelines and shared dependency versions are currently accepted?
- Which owner controls compatibility changes across shared modules and tenant applications?
- Which dependency exceptions have platform review, accountable tenant ownership, and effective dates?
- Which standalone template and shared-component versions remain supported?

## Related pages

- [[concepts/microfrontend-layering]]
- [[concepts/application-ownership]]
- [[concepts/frontend-onboarding]]
- [[concepts/shared-dependency-governance]]
- [[entities/single-spa]]
- [[entities/systemjs]]
- [[entities/nginx]]
- [[entities/react]]
- [[entities/mfe-base]]
- [[entities/fmo-post-trade-portal]]

## Related Concepts
- [[concepts/portal-ingress-path]]
- [[concepts/single-ui-sdk-authentication]]

## Entities
- [[entities/mui]]
- [[entities/mfe-root-config]]
- [[entities/mfe-ratan-container]]
- [[entities/mfe-cashflow-blotter]]
- [[entities/api-gateway]]
