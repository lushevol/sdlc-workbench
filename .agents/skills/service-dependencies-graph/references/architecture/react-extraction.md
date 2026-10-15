# React and Micro-Frontend Internal Extraction

This document describes extraction targets. The [implemented extraction guide](automated-analysis.md) lists the current supported forms and diagnostics; do not assume every feature below is implemented.

Use TypeScript/JavaScript ASTs plus parsed JSON/HTML/Webpack configuration. Exclude `node_modules`, coverage, compiled bundles, source maps, and vendored browser libraries from primary evidence; they may be diagnostics or corroboration only.

## Deterministic inventory

1. Parse `package.json`, workspace manifests, TypeScript path aliases, Webpack/Vite configs, environment templates, public import maps, nginx/gateway files, and deployment manifests.
2. Identify bootstrap roots from Webpack/Vite entry, `createRoot`/`render`, single-spa lifecycle exports, `registerApplication`, `constructApplications`, and application layouts.
3. Parse React Router route objects and JSX routes. Resolve static imports, lazy imports, redirects, nested routes, guards, loaders, and route parameters.
4. Parse JSX/component calls, hooks, context providers, Redux/Zustand/MobX/RTK Query/Apollo stores, service factories, and client call sites.
5. Parse `System.import`, dynamic `import()`, import-map names/targets, single-spa application names, and Module Federation `remotes`, `exposes`, and `shared`.
6. Parse browser custom-event dispatch/listeners, storage keys, BroadcastChannel/postMessage, FDC3 APIs, authentication tokens, permission/feature-flag checks, and runtime config reads.

## Semantic grouping

- `APPLICATION`/`MICRO_FRONTEND`: lifecycle/bootstrap root plus its exported runtime contract.
- `ROUTE` and `PAGE`: route declaration and the page/layout it activates.
- `FEATURE`: cohesive business workflow reached from routes/actions and owning related page/components/hooks/services. Generic UI libraries are `COMPONENT`/`MODULE`, not business features.
- `HOOK`, `STORE`, `REST_CLIENT`, `GRAPHQL_CLIENT`, `RUNTIME_CONFIG`, `FEATURE_FLAG`, and `SECURITY_COMPONENT`: retain as separate Level 2 nodes when shared across features or architecturally significant; otherwise keep at Level 3.
- A shared package that exports lifecycle, service, routing, state, or contract behavior may be a semantic module. Ordinary utility imports remain symbol facts.

Group using multiple signals: route reachability, directory/package cohesion, public exports, shared state/client ownership, naming, tests, and call graph. If no direct module declaration exists, the component is `INFERRED` and must list its member symbols and rationale.

## Relationship rules

Emit direct relationships only when syntax proves them:

```text
Route ROUTES_TO Page
Page RENDERS Component
Component CALLS Hook
Hook CALLS REST/GraphQL client
Component DEPENDS_ON Store
Feature REQUIRES_PERMISSION Security/permission rule
Feature CONFIGURES Runtime config/feature flag
Application LOADS_MFE Import-map/SystemJS module
Module EMITS_EVENT or LISTENS_EVENT Browser event
```

For `React.lazy(() => System.import("@fm/x"))`, preserve both `RENDERS`/`CALLS` to the loader symbol and `LOADS_MFE` to an MFE placeholder. For `System.import(name)` where `name` comes from a single-spa layout, join the layout application name through the function parameter and retain both declarations as evidence.

An import map is environment-specific configuration. A mapping such as `@fm/base -> /base/base.js` confirms the configured target for that map but not runtime use. Import-map overrides, variable remotes, or values such as Webpack `process.env.cduplatform` create variants or unresolved placeholders.

## Client and boundary clues

- REST: `fetch`, axios instances/interceptors, RTK Query base/query endpoints, generated clients, URL constants/template strings, base URL/config composition, methods and request/response types.
- WebSocket/STOMP: `WebSocket`, `SockJS`, STOMP clients, `WebSocketLink`, `SubscriptionClient`, broker URLs, and subscription destinations. A client path becomes a `SUBSCRIBES_WS` boundary only when the transport constructor or a bounded local wrapper receives a static URL.
- GraphQL: client/link construction, HTTP/WebSocket endpoints, parsed documents, operation name/type/root field, fragments, generated types, subscriptions.
- Authentication: token source, headers, route guards, permission/entitlement calls, session/local storage key—not token values.
- Events/storage: record stable event/channel/storage-key nodes only when they coordinate components or repositories; ignore generic DOM events unless they affect the business/runtime architecture.

Carry unresolved string construction as an expression tree or normalized template. Do not guess a concrete URL or module name.

## Brownfield cautions

- Multiple frameworks may coexist: the sampled MFE base uses single-spa and Module Federation together.
- Root-config layouts may register only a container; that container may dynamically load feature MFEs through SystemJS.
- Runtime admin APIs may mutate import maps, so static public maps can be incomplete or environment-local.
- Tests and API summaries often reveal intent but cannot replace a production call site.
- Feature flags can switch clients or wrappers; model both branches and the guard.
- Dead exports and legacy routes remain `ACTIVE` declarations with a dead-code diagnostic unless reachability proves otherwise; do not delete them silently.
