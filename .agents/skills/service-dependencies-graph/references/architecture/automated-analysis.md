# Automated repository analysis

## Execution and ownership

The local skill runner builds inventories, extracts declarations, resolves identities, renders projections, validates, and publishes one bundle.
The skill owns every graph implementation and enhancement.
Workbench integrations remain thin adapters.
No language model participates in deterministic extraction.

`build_graph.py` owns canonical nodes and edges.
Extraction modules return declarations.
`resolve_repository_relationships.py` joins identities.
`repository_reports.py` produces coverage and relationship projections.
`viewer_model.py` and viewer assets control presentation without changing canonical facts.

The census covers grouped directories, manifest entries, and registered local mappings inside the workspace.
Symlink roots and source paths remain excluded.
Only independent Git metadata can supply a repository commit and dirty state.
Filesystem copies retain fingerprints and explicit revision limits.

Source fingerprints cover recognized source/configuration and contract files
(`.graphqls`, `.gql`, `.proto`, `.mjs`, `.cjs`, `.html`, `.ejs`, `.env.*`, and
common build/config suffixes) within recorded exclusions.
They are not Git commits or semantic coverage scores.
Excluded test directories, dependencies, hidden directories, and generated output remain outside the source inventory.
Explicitly registered testing repositories receive bounded Python and Robot analysis within the shared source policy.
Inventory failures stop generation.

Generation compares inventories before and after extraction.
Changed sources abort publication and preserve the previous valid bundle.
Coverage queries compare saved and current fingerprints, revisions, and repository discovery.
Freshness is `CURRENT`, `STALE`, or `UNKNOWN` within those evidence limits.
Freshness also compares catalog extraction classifications and declared Java source roots.

Typed RestTemplate calls retain literal or symbolic destinations and explicit HTTP methods.
Exact getter spans can connect an endpoint expression to configuration keys without selecting values or profiles.
Supported web clients retain rooted and absolute endpoints beyond the `/api/` prefix.
Dynamic fetch methods remain conditional and inferred.

## Resolution rules

| Boundary | Required evidence | Unresolved cases |
| --- | --- | --- |
| SystemJS | Literal module import and exact declared package identity. | Missing or duplicate providers. |
| ES value imports | Exact module name and in-scope npm producer, with both source declarations. | Missing producers, duplicate producers, or dynamic names. |
| Feign | Parsed service name and unique declared service identity. | URL overrides, unresolved constants, or duplicate aliases. |
| HTTP | Exposed provider, compatible method/path, and known authority when required. | External authorities, unsupported rewrites, missing base URLs, or ambiguous routes. |
| WebSocket/STOMP | Static client path, exposed Spring endpoint, supported upgrade route, and declared upstream identity. | Dynamic endpoints, imported wrappers, unknown upstreams, or unsupported rewrites. |
| npm | Direct dependency and exact package name, including nested manifests. | Duplicate publishers and external build boundaries. |
| Maven | Root direct dependency and exact group/artifact coordinates, with supported local property resolution. | Remote models, transitive dependencies, profiles, and installed version compatibility. |
| Kafka | Supported producer/consumer declarations and concrete topic values. | Unknown cluster/environment identity prevents confirmed cross-repository flows. |

Absolute URLs retain authority during matching.
Path parameters can occupy complete segments.
The resolver cannot remove arbitrary wildcards or gateway prefixes without supported evidence.
An API node is not a provider unless the graph explicitly exposes it.

Owned `open-apis` routes can declare transport operations without controllers.
These retain `implementation_status=UNKNOWN`.
GraphQL transport ownership cannot establish field-level resolver calls.
Conflicting identities, foreign authorities, and incompatible methods prevent joins.

Static profile aliases do not select an active environment.
Package links retain build scopes and do not become service invocations.
Resolved joins retain consumer and provider evidence.
Alias collisions remain candidates or diagnostics.

`IMPORTS_MODULE` carries `dependency_kind=MODULE`.
Type-only imports are excluded.
Namespaces control scanning and cannot prove aliases.
Missing exact providers remain `UNRESOLVED_MODULE_PROVIDER` boundaries.
Module edges do not establish compiler, bundler, version, deployment, or runtime behavior.

Kafka channels remain repository-scoped without shared cluster identity.
Matching names can produce inferred, unresolved report candidates.
Configuration-only topics cannot establish publication or consumption.
Generic file and HTTP channels cannot become Kafka topics through naming.

## Implemented extraction surface

| Extractor | Implemented forms | Main limits |
| --- | --- | --- |
| Spring providers | Direct controller mappings, supported constants/path arrays, selected GraphQL annotations, and static `open-apis` routes. | Composed/inherited mappings, context paths, schema-only fields, and active profiles remain unsupported or unresolved. |
| Feign | Literal service identities with supported method mappings. | URL overrides, inherited contracts, generated clients, and unresolved configuration. |
| Web clients | Selected fetch/axios forms, RTK Query, static GraphQL/WebSocket clients, constants, and bounded wrappers. | General receiver typing, arbitrary wrappers, dynamic URL composition, and compiler scope resolution. |
| Java URI HTTP | Supported clients with literal URLs or unambiguous static string constants. | Mutable, dynamic, ambiguous, or unimported expressions. |
| Spring WebSocket | Literal `registerStompEndpoints` paths and supported defaults. | Dynamic endpoints, broker destinations, message handlers, and live sessions. |
| Kafka/Camel | Supported listeners, sends, topic headers, constants, configuration getters, and bounded typed helpers. | Ambiguous implementations, overloaded helpers, reassignment, generated code, active profiles, and cluster identity. |
| Database | Selected entity mappings, framework table configuration, native/JDBC queries, and mapper XML. | Entity-only mappings remain inferred; dynamic SQL and concrete ORM execution are outside supported proof. |
| Redis | Known configuration with imported client types or client construction. | Imports alone, unrelated type names, key-level access, TTL behavior, and deployment reachability. |
| Local files | Selected typed/instantiated Java file APIs and supported directions. | Shared path identity, helper data flow, static imports, and SFTP. |
| Internal gRPC SDK | Selected direct `RatanBusinessDataProviderService` calls with explicit imported types. | Generic stubs, `.proto` files, channel authority, and remote provider identity. |
| Nginx | Supported static locations, rewrites, proxy URI replacement, and upstream declarations. | Dynamic templates, IP-only identities, and multiple/empty upstream pools. |

Supported nginx proxy URI replacement preserves the unmatched request suffix.
Templates retain evidence and unresolved diagnostics.
Dynamic upstream names cannot establish concrete services without binding evidence.
IP similarity cannot establish a repository provider.

## Layouts and coverage limits

Runtime extraction targets supported web source and declared Maven Java/resource roots.
Unconditional Maven modules and literal custom roots retain repository-relative source identities.
Nested npm manifests supply package identity and supported source import detail.
Mixed roots select Spring when declared Maven roots contain Java source.
An npm tooling wrapper does not replace that Spring classification.

Explicit testing catalogs enable bounded Python client and Robot Settings extraction within test scope.
Gradle, Kotlin, Go, general Python applications, and unsupported layouts require separate adapters.
Selected AST extraction and text heuristics do not establish compiler-level calls or data flow.
Reflection, generated clients, active profiles, dynamic import maps, and environment activation remain outside supported proof.
Business descriptions remain inferred unless reviewed sources support them.

Evidence-file counts measure retained provenance and do not measure semantic coverage.
Platform names, DTOs, interfaces, and directory names cannot establish runtime queries.
Search-engine and external data-lake findings can remain inferred and unresolved.
No complete dependency score follows from successful extraction alone.

## Published projections and checks

Coverage retains source states, fingerprints, exclusions, diagnostics, and limits.
The build also runs `extract_pattern_candidates.py` over the included source
boundary. It uses bounded regular-expression searches for literal HTTP
endpoints, configuration reads, Kafka/Camel channels, SQL tables, imports,
gateway directives, and GraphQL schema files. It deduplicates values per file,
skips Robot fixture interpolation and non-contract JSON, and retains exact line
evidence. Robot and resource files remain listed as specialized-extractor
skips. Pattern candidates expose recall gaps; they do not prove execution or
provider identity.

Use the `patterns` snapshot query to filter these candidates by repository or
family. Review candidates against typed extractor evidence before promoting a
relationship. This keeps AI work focused on ambiguous bindings instead of
repeating repository-wide searches.

Repository relationships retain canonical edge IDs and evidence IDs.
Unresolved boundaries remain visible even when targets belong to their caller repository.
The human report summarizes these projections.

Validation recomputes relationship projections and checks the skill-owned schema.
The manifest checksums every generated artifact.
Queries read captured, checksum-validated bytes from that bundle.
Use [source audits](dependency-audit.md) and skill regressions for confirmed extraction defects.
Use the [viewer guide](viewer-hierarchy.md) for presentation changes.
