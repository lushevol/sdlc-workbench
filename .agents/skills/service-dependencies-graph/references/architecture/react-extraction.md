# React and micro-frontend extraction

This guide preserves source-review targets from the imported procedure.
The [implemented analysis](automated-analysis.md) defines current support and diagnostics.
Do not assume every target below has an extractor.

Exclude dependencies, compiled bundles, coverage, source maps, and vendored libraries from primary evidence.
Inspect declarations and imports alongside generated graph evidence.
Tests can explain expectations but cannot replace production call sites.

## Inventory and composition

Inspect root/nested package manifests, source entry points, path aliases, Webpack configuration, import maps, and application layouts.
Identify React roots, single-spa registration, lifecycle exports, and literal remote imports.
Review route objects, JSX routes, nested layouts, redirects, and guards when relevant.
Keep unsupported router or bundler semantics explicit.

Inspect component calls, hooks, stores, service factories, and client construction.
Shared exports identify module interfaces.
Directory grouping and semantic descriptions remain inferred without explicit declarations.
Ordinary utility imports do not automatically establish business capabilities.

Literal SystemJS imports require exact declared provider identities.
`IMPORTS_MODULE` joins exact ES value imports to in-scope npm producers.
It carries `dependency_kind=MODULE` and evidence from both consumer and producer.
Type-only imports are excluded.

Namespaces control scanning and cannot prove module aliases.
Missing exact providers remain `UNRESOLVED_MODULE_PROVIDER` boundaries.
Duplicate providers remain ambiguous.
Environment-derived bundler names cannot establish aliases without concrete binding evidence.

Import maps record configured targets at one source revision.
They do not establish active deployment or runtime loading.
Runtime administration and import-map overrides can change mappings beyond the static snapshot.
Dynamic module names remain unresolved.

## Semantic grouping

Bootstrap and lifecycle roots can identify application modules.
Route declarations can identify pages and layouts within supported syntax.
Shared exports, directory cohesion, and client ownership can support inferred component groups.
Do not present semantic grouping as compiler-level invocation evidence.

Hooks, stores, clients, runtime configuration, flags, and security components can require separate inspection.
Keep grouping rationale and source scope available.
Broad source wildcards require direct inspection before detailed impact claims.
Ownership links do not establish function reuse or execution.

## Client and boundary clues

Inspect fetch, axios, RTK Query, GraphQL links, WebSocket, SockJS, and STOMP construction.
Retain protocol, method, sanitized endpoint, authority, and supporting source identities.
Inspect wrapper imports and URL/method forwarding before assigning a client type.
Mutation naming alone cannot establish `POST`.

Unsupported imported wrappers and dynamic URL composition remain diagnostics or unresolved boundaries.
Keep feature-flagged alternatives distinct.
Do not select an active branch without environment evidence.
Authentication review records header names and token sources, never token values.

Browser events, storage keys, and interoperability APIs can identify possible cross-component contracts.
They require dedicated extraction or direct review before graph claims.
Generic DOM events cannot establish business dependencies through naming.
Generated client types cannot replace a bound runtime call.

## GraphQL documents

`extract_graphql_documents.py` separates imported gql source documents from API transport calls.
Read the [document extraction guide](graphql-document-extraction.md) for supported import bindings and syntax limits.
Supported direct library imports retain named or anonymous operation metadata.
Static documents retain field and response paths without argument literal values.

Dynamic substitutions retain partial document metadata and explicit limitations.
Unbound wrapper tags retain unresolved ledger records.
Document declarations and selected fields do not establish calls, providers, schemas, or transport bindings.
GraphQL operation names follow GraphQL identifier syntax; interpolation markers cannot become operation names.

## Brownfield cautions

Frameworks and bundler mechanisms can coexist.
A shell can load a container that later loads feature modules.
Static import maps can remain incomplete or environment-specific.
Dead exports and legacy routes require explicit reachability evidence before removal.

The viewer separates module boundaries from packages and ownership context.
Read [viewer hierarchy](viewer-hierarchy.md) before changing presentation.
Use the [source audit](dependency-audit.md) for observed extraction gaps.
