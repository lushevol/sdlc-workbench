# Service Dependencies Graph contract

`graph.json` is the canonical architecture graph within each generated bundle.
Viewers, repository projections, catalogs, and query results derive from the same snapshot.
Keep its matching manifest and projections together.

## Envelope and schema

The normative machine contract is [architecture-graph.schema.json](architecture-graph.schema.json).
This skill owns the schema and semantic validation tools.
Do not maintain a competing graph schema or engine outside the skill.
Workbench integrations call the skill through thin adapters.

The envelope contains `schema_version`, `generated_at`, `generator`, `repositories`, `nodes`, `edges`, `evidence`, and `diagnostics`.
Collections use sorted, unique identities.
Use the schema for current kinds, node types, and required fields.
Coverage can retain unsupported repositories without canonical nodes.

Include supported application shells and foundation repositories.
Graph service/repository roots are analysis identities.
They do not create catalog services, execution grants, or deployment identities.

## Nodes and edges

Nodes retain identity, repository ownership, dimensions, explanations, source paths, evidence IDs, and assertion status.
External nodes can have no local repository or source path.
Wildcards describe source scope and require inspection before detailed claims.
Description enrichment cannot add runtime facts.

Investigated architecture can enrich existing nodes and edges through `properties.architecture_subjects` and `properties.architecture_claims`.
New `REVIEWED_RELATIONSHIP` edges retain the investigated kind, assessment, rationale, and exact captured source citations.
Supported source declarations remain distinct from provider resolution, deployment, and execution.
Unbound subjects use explicit `ARCHITECTURE_BOUNDARY` nodes.
Read [the investigated context contract](user-architecture-context.md) before generating these relationships.

Edges retain endpoints, relationship, dimension, evidence, and assertion status.
Boundary edges retain resolved, ambiguous, or unresolved state when applicable.
Caller edges point toward dependencies.
Containment supplies navigation context.

Resolved joins require a resolution rule and evidence for both consumer and provider.
Ambiguous aliases remain ambiguous.
Dynamic expressions cannot become concrete identities through naming assumptions.
The viewer hierarchy cannot change these canonical meanings.

## Evidence and dependency claims

Evidence records relative paths, line numbers, sanitized declarations, extractor identity, and directness.
Never retain credentials or token values.
Source fingerprints identify analyzed bytes within recorded exclusions.
They do not establish source authority or unknown origin commits.

`DEPENDS_ON_PACKAGE` denotes build dependencies with coordinates and scopes.
External packages remain unresolved build boundaries.
Duplicate local publishers remain ambiguous.
Build declarations do not establish runtime calls or installed version compatibility.

`IMPORTS_MODULE` joins exact ES value imports to in-scope npm producers.
It retains `dependency_kind=MODULE` and consumer/provider evidence.
Type-only imports are excluded.
Namespaces control scanning and cannot establish aliases.
Missing providers remain `UNRESOLVED_MODULE_PROVIDER` boundaries.

Kafka declarations require cluster identity before resolved cross-repository flow claims.
Database configuration cannot establish table read/write behavior.
Transport routes cannot establish handlers or active deployments.
Dynamic nginx templates and ambiguous upstream pools remain unresolved.

## Projections and publication

`analysis-coverage.json` records census entries, extraction states, fingerprints, exclusions, and limits.
`repository-relationships.json` retains canonical edge/evidence references, explicit candidates, and unresolved boundaries.
`analysis-report.md` summarizes those projections.
The manifest records artifact checksums and snapshot identity.

Semantic validation recomputes relationship projections before publication.
Generation checks source inventories before and after extraction.
Changed sources abort publication and preserve the previous valid bundle.
Coverage freshness compares current fingerprints, revisions, and repository discovery with the saved inventory.

Read [implemented analysis](automated-analysis.md) for protocol-specific rules.
Read [viewer hierarchy](viewer-hierarchy.md) before changing presentation or aggregation.

## Source detail and coverage

Unconditional Maven modules and literal custom roots retain repository-relative source identities.
Dynamic, unavailable, excluded, profile-only, and escaping module roots retain diagnostics.
Explicit testing catalogs select the `TESTING` repository kind.
Testing declarations retain `dependency_scope=TESTING` within the runtime dimension and require no business projection.
Their calls and resource imports do not establish production dependencies or test execution.

`CONFIGURATION_KEY` identities describe repository-local property names, with source/profile contexts on declarations.
They do not select precedence, active values, profiles, or environment bindings.
Bindings and reads use separate relationships; configuration values and defaults remain excluded.
`ENTITY`, `TABLE`, and `COLUMN` mappings describe source declarations.
`mapping_only` tables cannot assert runtime reads or writes.
Logical names remain distinct from established physical names and unknown datasource identities.

`coverage-declarations.json` retains source fingerprints, parse results, dispositions, and independent marker candidates.
The coverage query includes its checksum-verified summary when available.
Inventory reconciliation and marker accountability do not establish semantic recall or reviewed precision.
Those rates remain `UNKNOWN` until independent source review establishes denominators.
Generator `2.1.0` adds detail categories; validation still accepts generator `2.0.0` projections without them.
