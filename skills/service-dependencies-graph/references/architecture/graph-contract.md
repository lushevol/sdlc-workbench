# Graph contract

`graph.json` is the canonical architecture graph within a generated bundle.
The viewer, service catalog, repository relationships, and query results derive from that snapshot.
Keep its matching `manifest.json` and projections together.

## Machine contract

The installed package owns `relationships/graph/architecture-graph.schema.json` under `ai_sdlc_workbench`.
The standalone source owns it under `core/relationships/graph/`.
Generated workspaces use the installed runtime and do not contain runtime source.
Do not create a second schema inside this skill.

The runtime also validates source paths, relationship projections, and protocol-specific invariants.

The canonical envelope contains `schema_version`, `generated_at`, `generator`, `repositories`, `nodes`, `edges`, `evidence`, and `diagnostics`.
Collections use stable identities and deterministic ordering.
Repository metadata and coverage can retain repositories that own no canonical nodes.
Use the installed schema for current node types, repository kinds, and required fields.

Include every supported repository, including application shells and foundation modules.
Graph repository/service roots are analysis nodes.
They do not declare catalog service identities or deployments.

## Nodes and edges

Nodes retain identity, repository ownership, dimensions, explanations, source paths, evidence IDs, and assertion status.
External nodes can have no local repository or source path.
Source wildcards describe scope and require source inspection before detailed claims.
Business descriptions do not add runtime facts.

Edges retain endpoints, relationship, dimension, evidence, and assertion status.
Boundary edges also retain resolved, ambiguous, or unresolved status where applicable.
Caller edges point toward their dependency.
Containment edges supply navigation context.

Resolved boundaries require a resolution rule and evidence for both consumer and provider.
Ambiguous aliases remain ambiguous.
Dynamic expressions cannot become concrete identities through naming assumptions.

## Evidence and projections

Evidence retains relative source paths, line numbers, sanitized declarations, extractor identity, and directness.
Do not store credentials or token values.
Source fingerprints identify analyzed bytes within the declared inventory exclusions.
They are distinct from Git commits and do not establish source authority.

Unknown origin commits remain unknown even when current source bytes have a fingerprint.

`analysis-coverage.json` records the census, extraction states, fingerprints, exclusions, and limits.
`repository-relationships.json` retains canonical edge and evidence references, plus explicit candidates and unresolved boundaries.
`analysis-report.md` summarizes those projections.
The manifest records artifact checksums and snapshot identity.

Runtime validation recomputes the relationship projection before publication.
Generation checks that source inventories remain stable during extraction.
Coverage queries report freshness from current source fingerprints, Git revisions, and repository discovery.

`DEPENDS_ON_PACKAGE` denotes a build dependency with coordinates and scopes.
External packages remain unresolved build boundaries.
Duplicate local publishers remain ambiguous.
`IMPORTS_MODULE` denotes an exact ES value import to an in-scope npm producer.

It retains `dependency_kind=MODULE` and evidence from both consumer and producer.
Type-only imports are excluded.
Duplicate module producers remain ambiguous.
The edge does not establish compiler, bundler, version, deployment, or runtime behavior.

Kafka names without shared cluster identity cannot establish a resolved event flow.
Database configuration cannot establish table read/write behavior.
Static routes cannot establish deployed connectivity.

Read [implemented analysis](automated-analysis.md) for protocol-specific evidence rules.
