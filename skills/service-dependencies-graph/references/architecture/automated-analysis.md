# Implemented analysis and limits

The installed command builds source inventories, extracts declarations, resolves identities, renders projections, validates, and publishes one bundle.
The Python runtime owns this process.
The shared skill selects commands and interprets evidence.

## Inventory and provenance

The census covers repository directories, supported group directories, manifest entries, and registered local mappings within the workspace.
Inspect coverage for the actual selected scope.
Symlink roots and source paths are excluded rather than silently traversed.
Only a repository's independent Git metadata can supply its commit and dirty state.

Filesystem copies retain content fingerprints and explicit revision limits.

The source fingerprint covers recognized source/configuration files within the recorded exclusions.
It is not a Git commit or proof of complete semantic coverage.
Tests, dependencies, generated output, and other excluded paths remain outside that fingerprint.
Inventory failures stop publication.

Unsupported stacks remain visible in the census.
Generation compares source inventories before and after extraction.
Changed sources abort publication and preserve the previous valid bundle.
Coverage queries compare current fingerprints and Git revisions with the saved inventory.

They report `CURRENT`, `STALE`, or `UNKNOWN`, including changes to discovered repository directories.

## Evidence rules

| Boundary | Supported evidence | Main limits |
| --- | --- | --- |
| MFE imports | Literal imports and exact declared package identity. | Missing or duplicate providers remain unresolved or ambiguous. |
| ES module imports | Exact value imports and an in-scope npm producer, with evidence from both sides. | Type-only imports are excluded; duplicate producers remain ambiguous. |
| Feign | Declared service identity, method, and path. | URL overrides, inherited mappings, and dynamic identities remain unresolved. |
| HTTP | Exposed provider, compatible method/path, and known authority when required. | External hosts, dynamic clients, and unsupported rewrite chains prevent joins. |
| WebSocket/STOMP | Static client path, exposed Spring endpoint, supported upgrade route, and declared upstream identity. | Dynamic configuration and unknown upstreams remain unresolved. |
| GraphQL | Selected static client endpoints, annotated resolver fields, and explicit transport routes. | Schema-only fields and field-level transport inference remain unsupported. |
| npm/Maven | Direct dependency coordinates, local publishers, and declared scopes. | External packages remain build boundaries; version compatibility and transitive models are not established. |
| Kafka/Camel | Supported listener/send declarations, constants, configuration bindings, and bounded typed helpers. | Dynamic topics and unknown cluster/environment identity remain unresolved. |
| Database | Runtime client, mapping, supported SQL, or mapper evidence. | Entity-only mappings are inferred; migrations do not establish runtime access. |
| Redis | Known configuration and declared client types or construction. | Imports alone, key access, cluster identity, and reachability are insufficient. |
| Files/external SDKs | Selected instantiated clients and direct calls. | File identities, generic generated clients, and remote provider identity can remain unknown. |
| Nginx | Supported static location, rewrite, proxy target, and upstream declarations. | Unresolved Jinja variables do not establish concrete route or service identities. |

In-scope npm namespaces control scanning and cannot establish aliases.
Module provider joins require exact names.
Missing providers remain `UNRESOLVED_MODULE_PROVIDER` boundaries.
Supported nginx proxy URI prefix replacement retains the unmatched request suffix.

Multiple or empty upstream pools remain unresolved.

The parser references describe review rules within this supported surface.
They do not authorize inferring unimplemented compiler or data-flow behavior.
Use current diagnostics and regressions when support for a syntax form is uncertain.

## Extraction limits

Runtime extraction targets root web `src` and supported Maven Java/resource layouts.
Nested manifests can supply build dependency evidence without runtime source extraction.
Mixed manifests select Spring when `pom.xml` and `src/main/java` identify Java source.
An npm tooling wrapper does not replace that Spring classification.

Gradle, Kotlin, Python, Go, and other unsupported stacks need separate adapters.
Text heuristics and selected AST extraction do not establish compiler-level call or data flow.

Active profiles, reflection, generated clients, runtime import-map changes, and deployment activation are not inferred.
Database names require datasource identity before cross-repository joins.
Kafka names require cluster identity before resolved event-flow claims.
Platform names and directory names do not establish bound runtime clients.

Business descriptions remain inferred unless reviewed sources support them.
`IMPORTS_MODULE` records a source module dependency with `dependency_kind=MODULE`.
It does not prove compiler, bundler, version, deployment, or runtime behavior.

Read [graph contracts](graph-contract.md) before changing producers or consumers.
Use the [source audit](dependency-audit.md) for a confirmed coverage gap.
