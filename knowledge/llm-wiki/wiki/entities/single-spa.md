---
sources: ["summaries/KT-release-operations.md", "summaries/KT-architecture-evolution.md", "summaries/KT-portal-purpose.md", "summaries/KT-frontend-composition.md", "summaries/ARC-portal-service-relationships.md"]
type: "Product"
description: "Single-SPA is the microfrontend orchestration framework that mounts the portal's registered shell."
---

# Single-SPA

Single-SPA is the microfrontend orchestration framework used by the [[entities/fmo-post-trade-portal]] to register, load, and mount its frontend layers. It is a product dependency of the four-layer composition rather than a portal service: it defines the lifecycle contract that the registered shell implements and coordinates application mounting.

## Role in the portal

- [[entities/mfe-root-config]] supplies the HTML and static entry resources, initializes Single-SPA, and registers only [[entities/mfe-base]]. The root layout declares only `@fm/base`, so Single-SPA is bootstrapped with a single registered application at that stage.
- [[entities/mfe-base]] is the registered Single-SPA application. It owns themes, login, logout, sessions, tiles, drawers, and remote container loading.
- Single-SPA mounts applications and manages the application lifecycle. It does not itself resolve every module: [[entities/systemjs]] resolves module names to deployed files and loads modules into the page, while import maps connect those module names to the deployed files.
- The documented UI stack separates these two responsibilities explicitly: SystemJS handles module resolution, and Single-SPA handles lifecycle management. Neither component substitutes for the other.
- Named modules are loaded through SystemJS, not through static bundling alone. JavaScript entry bundles can produce lazy chunks, so the number of loaded chunks is not fixed by the reported topology.
- Single-SPA registers only the shell. SystemJS and React Router support successive container and tile loading.

## Composition rationale

The documented design separates common platform modules from application-owned domain modules. The shared base supplies common context, while tenant teams supply containers and tiles. The stated design problems are coupled releases, broad testing scope, unclear ownership, and repeated components; the intended benefit is separate team delivery within one user workspace.

Single-SPA sits on the platform side of that boundary: it is part of the shared loading and lifecycle mechanism rather than tenant domain code. These are design goals, and the sources do not demonstrate their achievement across every application. See [[concepts/microfrontend-layering]] and [[concepts/application-ownership]].

## Interfaces

- Single-SPA lifecycle and SystemJS module loading are recorded as interfaces of the portal composition.
- Loading, routing, and props are distinct stages. Single-SPA loads the shell; the shell then selects `props.container` and forwards `module`, `tile`, `parameters`, `panelId`, and `tabId` toward the container and tile layers.
- Container and tile props select distinct route stages. Downstream routing is framework-independent of Single-SPA itself: the container selects its route from `props.module`, and the tile uses `props.tile` for its feature route.
- The [[entities/nginx]] integration routes application static files and API requests through configured locations, separate from Single-SPA's lifecycle role.

## Shared dependencies and compatibility

The design shares modules through exports and imports registered by name. Shared dependencies require coordinated upgrades, and a shared Single-SPA shell or interface change can affect several tenant consumers. That inference requires exact provider and consumer evidence before assessing a particular change. See [[concepts/shared-dependency-governance]].

Development guidance names [[entities/react]] 18.2.0 and [[entities/mui]] themes, but its effective date and supersession status remain unresolved. These versioned instructions must retain their source context before reuse.

## Migration and evolution

Build-tool research proposes [[entities/rspack]] for incremental migration from [[entities/webpack]] and [[entities/vite]] for new or simpler applications. It treats SystemJS compatibility as an architectural constraint and proposes a pilot that checks loading, HMR, and asset paths before a gradual rollout. Because Single-SPA owns the lifecycle contract while SystemJS owns module resolution, a bundler change must preserve both boundaries, not only individual application builds. See [[concepts/build-tool-migration]].

The same research proposes a longer-term move away from SystemJS. That suggestion changes the platform boundary beyond a bundler substitution, so it could alter how Single-SPA receives registered applications. Changed output formats or shared dependencies can affect the portal loading boundary; this is an inference, and the applicable implementation versions require inspection before it can be validated. See [[summaries/KT-architecture-evolution]].

The build-tool report has no publication date and retains no project benchmark provenance. Its recommendations remain research statements, not verified technical conclusions or accepted migration instructions. No evidence establishes that any proposed bundler or module-loading change has been adopted.

## Related pages

- [[concepts/microfrontend-layering]] — the four-layer responsibility model Single-SPA bootstraps.
- [[concepts/frontend-onboarding]] — the application setup and tile configuration flow around the shared shell.
- [[concepts/build-tool-migration]] — the proposed tooling changes that must preserve the lifecycle contract.
- [[entities/mfe-ratan-container]] and [[entities/mfe-cashflow-blotter]] — container and tile layers reached through the shell rather than registered directly.
- [[summaries/ARC-portal-service-relationships]] — the candidate architecture record for this composition.
- [[summaries/KT-frontend-composition]] — the composition, ownership, and onboarding guidance summarized here.
- [[summaries/KT-architecture-evolution]] — the historical evaluations and proposals that surround later changes to this composition.

## Qualifications

The composition facts come from a 22 October 2026 user clarification, local file inspection, and Confluence-derived design and onboarding documents. Four repositories have no independent Git history, so inspected hashes identify files without an upstream commit. No live requests, browser behavior, setup command, or deployment were executed. The getting-started guide depends on missing archives and screenshots, and the standalone template archive is absent, so setup cannot be reproduced from the supplied copy. The build-tool research supplies performance tables without retained inputs or execution records, so its rankings cannot predict results for these repositories. Current template, dependency, module-loading, and bundler compatibility require separate inspection.

See also: [[summaries/KT-portal-purpose]]

See also: [[summaries/KT-release-operations]]