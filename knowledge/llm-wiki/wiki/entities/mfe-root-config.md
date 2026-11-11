---
sources: ["summaries/KT-admin-and-onboarding.md", "summaries/KT-observability-and-performance.md", "summaries/KT-architecture-evolution.md", "summaries/KT-portal-purpose.md", "summaries/KT-frontend-composition.md", "summaries/ARC-portal-service-relationships.md"]
type: "Product"
description: "First microfrontend layer: portal HTML entry, import map, and Single-SPA bootstrap."
---

# MFE Root Config

**MFE Root Config** is the first layer of the portal's four-layer microfrontend composition. It is implemented in the `mfe-root-config` repository and supplies the HTML document, static entry resources, and the import-map configuration that locates shared modules. It initializes [[entities/single-spa]] and registers only [[entities/mfe-base]]; it does not register containers or tiles directly.

## Role in the portal composition

The four MFE layers are ordered as follows:

1. **Root Config** — `mfe-root-config`: supplies HTML and static entry resources, publishes the import map, initializes Single-SPA, and registers only MFE Base.
2. **Shell** — [[entities/mfe-base]]: supplies themes, login, logout, sessions, tiles, drawers, and remote container loading.
3. **Container** — [[entities/mfe-ratan-container]]: supplies application routing, shared components, utilities, and related services.
4. **Tile** — for example [[entities/mfe-cashflow-blotter]]: renders feature views and application functionality.

The root configuration therefore establishes the bootstrap boundary for [[concepts/microfrontend-layering]]. The inspected layout declares only `@fm/base`, and the root bootstrap initializes Single-SPA with that single registered application. Containers and tiles enter the composition later through the shell's dynamic loading path.

## Loading and registration details

- The root layout declares only the Base microfrontend (`@fm/base`).
- The root bootstrap initializes [[entities/single-spa]] and registers MFE Base.
- The import map connects registered module names to deployed files, so [[entities/systemjs]] can resolve and load them.
- The shell subsequently selects a container and forwards `module`, `tile`, `parameters`, `panelId`, and `tabId` props.
- React Router supports the successive container and tile loading stages that follow the shell.
- The user describes JavaScript entry bundles; lazy loading permits additional chunks beyond the initial entry.
- The root config is not itself the ingress endpoint. Nginx and the API Gateway sit in the request path described by [[concepts/portal-ingress-path]]; see [[entities/nginx]] and [[entities/api-gateway]].

## Configuration and onboarding

The documented [[concepts/frontend-onboarding]] sequence starts by obtaining the root configuration and application templates. A new team then updates module names, build configuration, imports, and the local import map before it supplies its own container and tile repositories.

Because the root configuration publishes shared module names, a change to that configuration can affect several tenant consumers. Such changes fall under the coordination concerns of [[concepts/shared-dependency-governance]]. The sources do not name the owner who approves compatibility changes to the root configuration.

## Evidence and limits

This entity is documented in [[summaries/ARC-portal-service-relationships]], which records a user clarification dated 22 October 2026, and in [[summaries/KT-frontend-composition]], which consolidates the documented microfrontend design.

The clarification supplies the responsibility model, while selected local declarations — including the layout and root bootstrap — were inspected and hashed by the source review. The record does not establish an effective deployment, DNS forwarding, gateway routes, or authenticated architecture ownership. The inspected repositories have no independent Git history, so the hashes identify inspected files without an upstream commit.

No live requests, browser behavior, or business tests were executed for this review. The root config's role is therefore reported architecture supported by local file inspection, not runtime verification. The exact repository revision that implements the current root configuration and import map remains unconfirmed.

See also: [[summaries/KT-portal-purpose]]

See also: [[summaries/KT-architecture-evolution]]

See also: [[summaries/KT-observability-and-performance]]

See also: [[summaries/KT-admin-and-onboarding]]