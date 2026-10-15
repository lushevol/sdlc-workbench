---
name: service-dependencies-graph
description: Build and query static dependency graphs from local source for architecture discovery, coverage audits, and change impact.
---

# Service Dependencies Graph

This imported skill owns graph generation, queries, validation, and visualization.
Keep every graph enhancement in its `scripts/`, `tools/`, `assets/`, `references/`, or `tests/` directories.
Workbench CLI and MCP integrations remain thin adapters to this skill.
The graph records static source declarations and supported identity joins.
It does not establish deployment, runtime execution, or approved business intent.

Discovery aliases at `skills/service-dependencies-graph/` and `.claude/skills/service-dependencies-graph/` point to this canonical directory.
Initialization creates directory links where the platform permits them.
If directory links fail, initialization creates forwarding `SKILL.md` files.

## Choose the workflow

| Request | Procedure | Output |
| --- | --- | --- |
| Build or audit the repository census | Run the skill build command, then inspect coverage. | Snapshot, census, diagnostics, and fingerprints. |
| Explain the architecture | Check coverage, services, and repository relationships. | Analysis roots, confirmed links, and unresolved boundaries. |
| Trace one repository or boundary | Search concrete names or paths, then inspect neighborhoods and cited source. | Consumer/provider evidence and identity limits. |
| Inspect the viewer | Use the [viewer guide](references/architecture/viewer-hierarchy.md). | System connections, interaction details, and package declarations. |
| Assess requirement or code impact | Use [impact guidance](references/architecture/impact-analysis.md). | Source-backed effects, candidates, and unexamined scope. |
| Audit missing dependency syntax | Use the [source audit](references/architecture/dependency-audit.md). | Extracted evidence or explicit gap records. |
| Change graph behavior | Read the [graph contract](references/architecture/graph-contract.md) and relevant parser guide. | Skill-owned implementation, regression, and evidence updates. |

## Readiness and build

Read workspace instructions and inspect the worktree before changing files.
Inspect repository declarations, registered source locations, and local mappings.
Keep business repositories in their current locations.

Use Python 3.10 or later.
Standalone skill operation requires PyYAML, tree-sitter, tree-sitter-java, tree-sitter-typescript, and jsonschema.
Installing Workbench installs the declared dependency versions.
For standalone skill operation, install them in the selected Python environment:

```sh
python -m pip install PyYAML==6.0.2 tree-sitter==0.25.2 tree-sitter-java==0.23.5 tree-sitter-typescript==0.23.2 jsonschema==4.25.1
```

Run the skill directly from the workspace root:

```sh
python .agents/skills/service-dependencies-graph/scripts/graph.py --workspace PATH build
```

The default source directory is `repos/`.
The default output is `relationships/service-dependencies/generated/`.
Use explicit locations and open the viewer when useful:

```sh
python .agents/skills/service-dependencies-graph/scripts/graph.py --workspace PATH build --repos repos --out relationships/service-dependencies/generated --open
```

The build inventories source, extracts declarations, resolves identities, renders projections, validates, and publishes one bundle.
Generation compares source inventories before and after extraction.
Source changes or failed validation stop publication and preserve the previous valid bundle.
Generation does not clone repositories, select active profiles, or refresh code indexes.

Inspect coverage before interpreting relationships.
Record snapshot time, manifest checksum, independent Git revisions, dirty states, and source fingerprints.
Filesystem copies can have fingerprints without independent Git revisions.
Never substitute the Workbench commit for a business source revision.

Missing repositories, unsupported layouts, and dynamic expressions remain explicit limits.
Coverage freshness is `CURRENT`, `STALE`, or `UNKNOWN` within recorded inventory exclusions.
It compares source fingerprints, Git revisions, and discovered repository directories.
Do not infer freshness from directory timestamps or an old report.

Read these artifacts as needed:

- `analysis-report.md`: readable census and relationship summary.
- `analysis-coverage.json`: source fingerprints, extraction states, diagnostics, and limits.
- `repository-relationships.json`: resolved joins, candidates, and unresolved boundaries.
- `graph.json`: canonical nodes, edges, and evidence.
- `relationship-viewer.html`: interactive projection of the same snapshot.
- `manifest.json`: artifact checksums and snapshot identity.

## Query the snapshot

Use the skill runner's `query` command.
Read its help and operation schemas before supplying arguments.
Start with coverage, then select relationships, services, search, or a node neighborhood.
Inspect source evidence at both endpoints before reporting a resolved relationship.
Check returned counts and limits before claiming completeness.

```sh
python .agents/skills/service-dependencies-graph/scripts/graph.py --workspace PATH query --data-dir relationships/service-dependencies/generated coverage --args '{}'
python .agents/skills/service-dependencies-graph/scripts/graph.py --workspace PATH query --data-dir relationships/service-dependencies/generated relationships --args '{}'
```

`coverage` accepts an empty object.
`relationships` accepts `repository` and `limit` from 1 through 200.
`services` accepts `repository`.
`search` requires `query` and accepts `repository` and `limit` from 1 through 100.
`neighborhood` requires `node_id` and accepts `limit` from 1 through 200.
Neighborhood results contain direct edges, not recursive impact traversal.

The optional Workbench resource `service-dependencies` uses provider `graph.snapshot`.
It exposes `coverage`, `relationships`, `services`, `search`, and `neighborhood` through CLI `call` and MCP `workbench_call`.
These adapters invoke the skill implementation and retain Workbench action records.
Direct skill commands retain snapshot metadata without creating Workbench action records.

The original dedicated MCP server and advanced impact commands depended on the source project's runtime.
They are unavailable unless adapted and validated within this skill.
Do not invoke imported compatibility wrappers that still require an external harness.

## Dependency extraction map

| Dependency | Skill implementation | Evidence limit |
| --- | --- | --- |
| Web API | Web clients, Spring mappings, and HTTP resolution. | Requires exposed provider identity and compatible method/path. |
| WebSocket/STOMP | Static client paths, Spring endpoints, and supported upgrade routes. | Unknown upstream identities and dynamic paths remain unresolved. |
| GraphQL | Selected static clients, annotated resolvers, and explicit transport routes. | Schema-only fields and field-level transport inference remain unsupported. |
| Feign | Declared service identity and method contract extraction. | URL overrides, collisions, and dynamic identities remain unresolved. |
| Java URI HTTP | Recognized clients with literal or unambiguous constant URLs. | Dynamic expressions remain diagnostics. |
| Kafka/Camel | Supported listeners, sends, configuration bindings, and bounded typed helpers. | Equal topic names do not establish cluster identity. |
| npm/Maven | Direct coordinates, local publishers, and scopes. | Build declarations do not establish runtime invocation or version compatibility. |
| ES module imports | Exact value imports and in-scope npm producers. | Type-only imports are excluded; duplicate providers remain ambiguous. |
| Database | Supported runtime clients, queries, and mapper declarations. | Migrations and equal table names do not prove runtime access. |
| MFE/SystemJS | Literal remote imports and exact package identity. | Missing or duplicate provider identities remain unresolved or ambiguous. |
| Nginx/gateway | Supported static routes, rewrites, proxy targets, and service aliases. | Dynamic templates and ambiguous upstream pools remain unresolved. |
| Cache/platform | Known Redis clients/configuration and selected platform clients. | Names alone do not establish dependency or cluster identity. |
| Internal gRPC SDK | Selected direct SDK calls with explicit imported types. | Generic stubs and external provider identities remain unsupported or unresolved. |
| Local files | Selected instantiated Java file APIs. | Path identity remains unknown; no shared-file or SFTP join is inferred. |

Read [implemented extraction and limits](references/architecture/automated-analysis.md) before claiming support.
Use the [React](references/architecture/react-extraction.md), [Spring](references/architecture/spring-extraction.md), and [boundary](references/architecture/external-boundaries.md) guides for focused reviews.
Coverage diagnostics take precedence over these summaries.

## Interpret evidence and hierarchy

Keep `assertion_status` separate from `resolution_status`.
`CONFIRMED` describes an observed declaration or supported join.
It does not establish a resolved provider or active deployment.
`INFERRED` relationships remain candidates.

`RESOLVED` joins retain a resolution rule and consumer/provider evidence.
`AMBIGUOUS` means multiple providers match.
`UNRESOLVED` means missing, conflicting, dynamic, or unsupported evidence prevents resolution.
These states do not mean a dependency is broken.

The viewer uses three presentation levels:

- Highest: confirmed, resolved API, data, and shared-module links between repositories.
- Medium: individual APIs, storage access, module imports, handler mappings, and uncertain boundaries.
- Lowest: package and build-tool declarations.

The hierarchy controls navigation depth and does not assign business criticality.
Ownership context remains optional within the medium view.
Graph roots are analysis identities, not service catalog declarations or deployments.
Include supported application shells and foundation repositories.

Use the legend for relationship colors, node roles, arrow direction, and provider status.
Filters select repository, family, provider status, boundary, relationship, and search text.
The relationship list retains every filtered match across pages.
Diagram limits do not remove canonical evidence.

Exact module names establish `IMPORTS_MODULE` joins with `dependency_kind=MODULE` and evidence from both sides.
Namespace matching only controls scan scope and cannot prove aliases.
Missing providers remain `UNRESOLVED_MODULE_PROVIDER` boundaries.
Module joins do not establish compiler, bundler, version, deployment, or runtime behavior.

Kafka cluster identity, shared datasource identity, and concrete gateway bindings require separate evidence.
Unresolved nginx templates cannot establish concrete upstream service identities.
Unsupported rewrites and dynamic clients remain unresolved.
A search miss does not establish independence or no impact.

## Report and maintain

Report scope, snapshot identity, confirmed static evidence, candidates, unresolved items, and coverage limits.
Give each finding evidence, a consequence, an owner, and a next action.
Mark unknown owners explicitly.
Read cited requirements before treating retrieved text as approved intent.

Use ASD-STE100 for authored reports under workspace instructions.
Keep automated checks separate from writing review:

```yaml
standard: ASD-STE100
automated_check: PENDING
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```

Set `automated_check` from checks actually performed.
Do not invent reviewer identities, approvals, or execution results.
Passing commands do not establish verified business behavior.

For a confirmed extraction defect, add a focused regression under this skill's `tests/` directory.
Update affected skill tools, schema, projections, viewer assets, and references together.
Run relevant regressions, rebuild, and inspect evidence before completing the change.
Never hand-edit generated graph facts or checksums.
Keep unsupported syntax and ambiguous identities visible.
