---
sources: ["summaries/KT-application-interoperability.md", "summaries/KT-frontend-composition.md", "summaries/ARC-portal-service-relationships.md"]
type: "Product"
description: "Feature tile microfrontend in the RATAN portal that renders cashflow blotter views."
---

> Derived candidate/draft knowledge; publication review remains pending. [Canonical source bindings](../../source-manifest.json).

# Cashflow Blotter

Cashflow Blotter is a **tile-level** microfrontend in the RATAN portal composition. The architecture record cites its repository, `mfe-cashflow-blotter`, as the example of the fourth and lowest MFE layer: the layer that renders feature views and application functionality.

## Position in the four-layer composition

The portal is described in four ordered layers, from outermost to innermost:

| Order | Layer | Example |
| --- | --- | --- |
| 1 | Base | [[entities/mfe-root-config]] — HTML, static resources, Single-SPA bootstrap |
| 2 | Shell | [[entities/mfe-base]] — themes, login/logout, sessions, tiles, drawers, remote loading |
| 3 | Container | [[entities/mfe-ratan-container]] — application routing, shared components, utilities |
| 4 | Tile | Cashflow Blotter — feature views and application functionality |

The layering pattern itself is described in [[concepts/microfrontend-layering]].

## Loading and routing

Cashflow Blotter is reached through two upstream stages:

1. The shell ([[entities/mfe-base]]) uses [[entities/single-spa]] and SystemJS to load the container module, forwarding `module`, `tile`, `parameters`, `panelId`, and `tabId` props.
2. The container ([[entities/mfe-ratan-container]]) uses `props.module` to select its route; a selected loader imports the tile and forwards the props onward.

Within the tile, `props.tile` selects the tile's own feature route. The document stresses that these are **distinct routing and loading stages** — shell, container, and tile each resolve a different prop at a different level.

## Shared-code direction

The dependency flow is not purely top-down. Shared-code imports also flow from containers and tiles **back** into shell and container libraries; the tile's imports of RATAN shared components are cited as evidence of this reuse. The record notes that the user described JavaScript entry bundles only, and that lazy loading permits additional chunks.

## Evidence status

- Responsibility model comes from a user clarification dated 22 October 2026, recorded as candidate architecture, not verified deployment.
- The tile appears as an *example*; no complete tile inventory is claimed.
- No live requests, browser behavior, or business tests were executed, and the record changes no application behavior.

## Related pages

- [[summaries/ARC-portal-service-relationships]] — the source architecture clarification
- [[entities/fmo-post-trade-portal]] — the portal this tile serves
- [[concepts/portal-entry-and-tile-authorization]] — authorization applied to tile-level entry
- [[entities/single-ui-bff]] — backend serving the described portal scope


See also: [[summaries/KT-frontend-composition]]

See also: [[summaries/KT-application-interoperability]]