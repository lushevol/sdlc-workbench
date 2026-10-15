# Service Dependencies Graph Contract v2

`service-dependencies-graph-output/graph.json` is the canonical architecture and impact graph. Every viewer, repository view, catalog, and MCP response is derived from it.

## Envelope

The exact top-level fields are `schema_version`, `generated_at`, `generator`, `repositories`, `nodes`, `edges`, `evidence`, and `diagnostics`. Collections and IDs are sorted and unique. Optional fields are omitted when empty; do not store confidence labels, repeated commits, null placeholders, or separate interface/resolution copies.

Repositories declare `kind` (`WEB` or `SPRING`), `role`, and `visible`. `mfe-root-config` remains repository metadata with `role=FOUNDATION`, `visible=false`, and owns no graph nodes.

## Nodes

Every node contains:

- identity: `id`, `type`, `name`, nullable `repository`;
- projections: one or both of `RUNTIME`, `BUSINESS` in `dimensions`;
- explanations: `functional_role`, `business_meaning`;
- provenance: `source_paths`, `evidence`, `assertion_status`;
- optional non-empty `component_kind` and protocol-specific `properties`.

External nodes have `repository=null` and may have no source path. Local nodes use workspace-relative files or the narrowest honest wildcard. Wildcard labels remain intact; viewers link them to the nearest concrete parent.

## Edges

Edges contain `source`, `target`, `relationship`, one `dimension`, evidence, and assertion status. `resolution_status` appears only for a resolved, ambiguous, or unresolved boundary. Edges point from owner/caller to dependency, except provider containment such as `DATABASE CONTAINS TABLE`.

Runtime relationships include `ROUTES_TO`, `USES_COMPONENT`, `LOADS_REMOTE`, `CALLS_REST`, `CALLS_GRAPHQL`, `SUBSCRIBES_WS`, `EXPOSES`, `INVOKES`, `CALLS_SERVICE`, `CONNECTS_TO`, `READS`, `WRITES`, `CONTAINS`, `PUBLISHES`, `CONSUMES`, `CALLS_DATA_PLATFORM`, and `QUERIES_DATA_PLATFORM`.

`CONTAINS_COMPONENT` links a semantic domain/layer group to a detailed module or class without duplicating its responsibility. Description enrichment may replace `functional_role` and `business_meaning` and attach provenance properties, but it cannot add runtime facts.

Business relationships include `DELIVERS`, `IMPLEMENTS`, and `REALIZED_BY`.

## Evidence and dependency claims

Evidence records the workspace-relative `path`, line, sanitized declaration, extractor, and directness. Do not store secrets.

- PostgreSQL connection evidence may come from build or datasource configuration.
- Tables and read/write access require runtime client evidence: Spring Data/JPA, MyBatis, native query, JDBC, or equivalent. Migration SQL cannot establish a runtime dependency.
- Kafka topic nodes require a producer/consumer declaration and direction.
- `GATEWAY_TRANSPORT` operations require an owned `open-apis` route and a unique service identity.
  They record static transport declarations with `implementation_status=UNKNOWN`.
  They do not establish an implemented handler or a field-level GraphQL call.
  REST joins without a controller require caller service identity or a known authority.
- DQSL is `DATA_PLATFORM` with `platform_kind=EXTERNAL_DATA_LAKE`; its datasets or upstream sources appear only when directly identified.
- Elasticsearch/OpenSearch appears only from an explicit engine client or configuration, never by interpreting DQSL.

The normative machine contract is [architecture-graph.schema.json](architecture-graph.schema.json). `tools/validate_graph.py` additionally validates source existence and domain-specific invariants.

## Repository analysis projections

`analysis-coverage.json` records the repository census and extraction limits, including repositories without a supported canonical graph kind. `repository-relationships.json` is derived from canonical edges and retains their IDs/evidence. `analysis-report.md` summarizes those projections. All are manifest-checksummed; the relationship projection is recomputed during validation.

`DEPENDS_ON_PACKAGE` connects in-scope package producers and consumers with exact coordinate evidence. It carries `dependency_kind=BUILD`, `coordinate`, and `scopes`; its runtime dimension is for dependency navigation, not an assertion of runtime invocation. Impact traversal includes these declared consumers.

Packages without an in-scope producer remain canonical external build boundaries.
They retain exact coordinate evidence, declared scopes, and `resolution_status=UNRESOLVED`.
Duplicate local producers remain `AMBIGUOUS`.
The `packages` dependency projection includes both local and external declarations.

Resolved boundary edges carry a `resolution_rule` and consumer/provider evidence; original boundary edges retain candidate provider IDs. Kafka channels with unknown cluster identity are repository-scoped. Matching concrete producer/consumer topic names are emitted only as unresolved, inferred report candidates, never resolved canonical edges.

The relationship projection retains unresolved boundaries even when their nodes belong to the caller repository.
Repository ownership records provenance. It does not establish file path or provider identity.
