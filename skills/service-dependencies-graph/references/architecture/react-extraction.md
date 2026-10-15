# React and MFE source review

Read [implemented analysis](automated-analysis.md) before assuming support for a syntax form.
Inspect source declarations and exact imports alongside generated evidence.
Exclude vendored libraries, compiled bundles, coverage, and source maps from primary evidence.

## Composition

Inspect root `package.json`, web entry points, single-spa registration, application layouts, and literal module imports.
Exact package identity can resolve an MFE provider.
Missing or duplicate local providers cannot become resolved through similar names.
`IMPORTS_MODULE` joins exact ES value imports to in-scope npm producers.

It retains `dependency_kind=MODULE` and source evidence for both consumer and producer.
Type-only imports are excluded, and duplicate producers remain ambiguous.
Module imports do not establish compiler, bundler, version, deployment, or runtime behavior.
An in-scope npm namespace controls scanning and never proves a module alias.

Provider resolution requires exact module names.
Missing providers remain `UNRESOLVED_MODULE_PROVIDER` boundaries.
Environment-derived bundler names cannot establish aliases without concrete binding evidence.
Import maps record configured targets at one source revision.

They do not establish active deployment or runtime loading.
Runtime administration can change import maps beyond the static snapshot.

Shared exports identify module interfaces.
An imported utility does not automatically establish a business capability or service invocation.
Directory grouping and descriptive labels remain inferred where syntax supplies no explicit semantic boundary.

## Clients

Inspect fetch, axios, RTK Query, GraphQL links, WebSocket/SockJS/STOMP constructors, and supported client wrappers.
Retain protocol, method, raw URL, normalized path, authority, and supporting constant evidence.
Check wrapper imports and URL/method forwarding before treating a wrapper as an HTTP client.
Mutation naming alone does not establish `POST`.

Dynamic URL construction and unsupported imported wrappers remain diagnostics or unresolved boundaries.

Keep feature-flagged alternatives distinct.
Do not select an active branch without environment evidence.
Authentication review records header names and token sources, never token values.
Tests can explain expectations but cannot replace a production call site.

Use the [boundary review](external-boundaries.md) for route resolution and the [source audit](dependency-audit.md) for extraction gaps.
