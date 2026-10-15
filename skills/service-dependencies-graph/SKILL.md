---
name: service-dependencies-graph
description: Build and query static dependency graphs for architecture discovery, coverage audits, and change impact.
---

# Service dependency graph

Build one validated snapshot before interpreting cross-repository relationships.
The installed Workbench runtime owns extraction, identity resolution, validation, publication, and queries.
Use source evidence to distinguish confirmed static links, inferred candidates, and unresolved boundaries.
Static links do not prove deployment, runtime reachability, or approved business intent.

## Build and establish coverage

Read workspace instructions and inspect the worktree before making changes.
Inspect `registry/repositories.yaml`, source declarations, and local mappings.
Keep business source in its current location.
Run from the standalone workspace:

```sh
ai-sdlc --workspace PATH graph build
```

The defaults scan `repos/` and publish `relationships/service-dependencies/generated/`.
Use explicit locations or open the viewer when needed:

```sh
ai-sdlc --workspace PATH graph build --repos repos --out relationships/service-dependencies/generated --open
```

Generation reads local source and accounts for grouped repository directories and registered local mappings.
It does not clone repositories, select active profiles, or refresh code indexes.
The bundle is validated before publication.
Generation compares source inventories before and after extraction.

Source changes during generation abort publication.
A failed build must preserve the prior valid bundle.
Do not use the prior bundle as current evidence without checking freshness.

Inspect `analysis-coverage.json` before interpreting results.
Record generation time, manifest checksum, repository commits, dirty states, and source content fingerprints.
Filesystem copies can have fingerprints without independent Git revisions.
Never substitute the Workbench commit for a business source revision.

Missing repositories, unsupported layouts, and dynamic expressions remain coverage limits.
The coverage operation reports freshness as `CURRENT`, `STALE`, or `UNKNOWN`.
It compares source fingerprints and Git revisions, including newly discovered repository directories.
Read the returned evidence and limits before using a current-state claim.

Read generated files as needed:

- `analysis-report.md`: repository census and relationship summary.
- `analysis-coverage.json`: source fingerprints, extraction status, diagnostics, and limits.
- `repository-relationships.json`: resolved links, candidates, and unresolved boundaries.
- `graph.json`: canonical nodes, edges, and evidence.
- `relationship-viewer.html`: interactive projection of the same snapshot.

## Query the snapshot

Read `ai-sdlc --workspace PATH status` to discover registered tools and operation schemas.
The project resource is `service-dependencies`, with provider `graph.snapshot`.
Its operations are `coverage`, `relationships`, `services`, `search`, and `neighborhood`.
Call coverage first:

```sh
ai-sdlc --workspace PATH call service-dependencies coverage --args '{}'
ai-sdlc --workspace PATH call service-dependencies relationships --args '{}'
ai-sdlc --workspace PATH call service-dependencies services --args '{}'
```

CLI `call` and MCP `workbench_call` use the same runtime and resource grants.
Use the advertised operation schemas for search terms, node IDs, repository filters, and traversal limits.
Retain action IDs and returned snapshot metadata.
Queries retain Workbench action records.

Graph builds retain bundle metadata and do not create Workbench action records.
Check total counts and truncation before claiming a bounded result is complete.
Inspect both source endpoints and the resolution rule before reporting a resolved link.

`search` requires `query` and accepts `repository` and `limit` from 1 through 100.
`neighborhood` requires `node_id` and accepts `limit` from 1 through 200.
It returns direct edges, not a recursive impact traversal.
`relationships` accepts `repository` and `limit` from 1 through 200.

`services` accepts `repository`.
The provider has no semantic impact operation.

## Select the procedure

| Request | Procedure |
| --- | --- |
| Explain the system | Coverage, service catalog, repository relationships, then relevant node neighborhoods. |
| Trace one boundary | Search concrete names or paths, inspect neighborhoods, and read cited consumer/provider source. |
| Audit missing dependencies | Read the [source audit](references/architecture/dependency-audit.md) and compare declarations with canonical evidence. |
| Assess requirement or code impact | Read [impact guidance](references/architecture/impact-analysis.md) and use the shared `impact-analysis` skill. |
| Change extraction or graph consumers | Read the [graph contract](references/architecture/graph-contract.md) and the relevant parser reference. |

## Evidence rules

Package edges establish declared build dependencies, including scopes.
They do not prove runtime invocation or installed version compatibility.
`IMPORTS_MODULE` joins exact ES value imports to in-scope npm producers.
These `MODULE` dependencies retain evidence from both sides.

Type-only imports are excluded, and duplicate producers remain ambiguous.
Module imports do not establish compiler, bundler, version, or deployment behavior.
Matching Kafka topic names remain candidates when cluster or environment identity is unknown.
Equal table names do not establish a shared database.

Nginx templates with unresolved variables do not establish concrete routes or upstream service identities.
Unsupported rewrites and dynamic clients remain unresolved.
Source declarations do not establish active deployment configuration.
Semantic requirement matches remain candidates until reviewed intent supports them.

Read [implemented analysis and limits](references/architecture/automated-analysis.md) before relying on extraction support.
Use the [React](references/architecture/react-extraction.md), [Spring](references/architecture/spring-extraction.md), or [boundary](references/architecture/external-boundaries.md) reference for focused source reviews.
Use direct source inspection for exact callers when no usable repository index exists.
Do not invent index scores or query an unrelated repository.

## Report and maintain

Report scope, snapshot identity, confirmed static evidence, candidates, unresolved items, and coverage limits.
Give each finding evidence, a consequence, an owner, and a next action.
Mark unknown owners explicitly.
Keep facts, inferences, and questions separate.

Use ASD-STE100 for authored reports under the workspace instructions.
Include this review record in each saved report:

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
A passing graph build does not establish verified business behavior.
Keep generated facts and checksums under runtime ownership.
Repair confirmed extraction defects with focused regressions, then rebuild and review the affected evidence.
