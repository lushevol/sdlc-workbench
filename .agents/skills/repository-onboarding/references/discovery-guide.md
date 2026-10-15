# Repository discovery guide

Use these hints to investigate *candidate* ownership and call relationships. They are not proof of behavior.

## General sequence

1. Capture repository path and revision. Detect tracked code vs vendored/generated output and ignore caches.
2. Read existing `README.md`, `AGENTS.md`, architecture notes, and CI config; confirm their claims in source.
3. Locate deployable entrypoints and public interfaces before diving into leaf functions.
4. Cluster code into **business functions** and source path patterns. Do not make a component for every file or every Java class.
5. Find tests and CI gates that validate the identified behavior.
6. Record factual evidence as `repo-relative/path:line1-line2` at an exact revision.

## React/TypeScript/MFE

- Discover `package.json`, workspace manifests, `tsconfig*.json`, Vite/Webpack/Rsbuild configuration, SystemJS/import maps and single-spa registration.
- Look for routes, feature directories, state stores, event handlers, API clients, GraphQL queries, data-fetching hooks, FDC3/OpenFin interop calls, and entitlements.
- Trace component/UI action -> hook/state -> API client or broker -> contract; distinguish compile-time import from dynamic module federation or broker resolution.
- For each business component record route/tile entrypoint, user actions, remote dependencies, API consumers and associated tests.
- Do not infer a remote MFE's implementation from its alias or import-map key.

## Spring Boot/Java

- Discover `pom.xml` / Gradle, Spring Boot application classes, configuration profiles, deployment definitions.
- Look for controllers, GraphQL resolvers (DGS), service interfaces/implementations, repositories, Feign clients, Kafka producers/consumers, database migrations and scheduled jobs.
- Trace inbound REST/GraphQL/event -> service -> persistence/outbound client/event; record interface-contract edges separately from wiring at runtime.
- Spring DI/profiles/conditional beans, transactions, reflection, proxies and feature flags can change runtime invocation paths.
- Distinguish schema-level relationships from business ownership of tables.

## Contracts and cross-repository edges

- Prefer checked-in OpenAPI/GraphQL/AsyncAPI schemas and actual source/config over README-only claims.
- Resolve a cross-repository edge only when **both ends** establish it; an authoritative contract can support a declared relationship. Otherwise label it `candidate`.
- Record edge kind: `rest`, `graphql`, `event`, `database`, `mfe-import`, `broker-intent`, `proxy-route`, or `build`.
- Include producing and consuming service identifiers only when confirmed. Do not equate repository IDs with runtime service IDs.

## Sensitive data and local environment

- Ignore `.env*`, secrets, key stores, generated bundles, vendored modules and large logs.
- Use approved source access and tooling. Do not disclose source to unrelated external services.
- Do not invoke `npm install`, Maven dependency downloads, builds, runtime tests or database probes without authorization covering that execution.
