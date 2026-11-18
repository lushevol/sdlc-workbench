# Service dependency relationships

The [canonical graph skill](../../.agents/skills/service-dependencies-graph/SKILL.md) owns extraction, resolution, validation, queries, and visualization.
Keep graph enhancements inside that skill.
Build a static dependency graph through the installed Workbench adapter:

```sh
ai-sdlc --workspace PATH graph build
```

You can also invoke the skill directly with your installed Python environment:

```sh
python .agents/skills/service-dependencies-graph/scripts/graph.py --workspace PATH build
```

The default bundle is `relationships/service-dependencies/generated/`.
The default output directory is ignored by Git.
Keep the complete bundle and matching manifest together.
Use `--open` to display its interactive viewer.
Use `--repos` to select a repository directory within the workspace.
Use `--out` to select a separate output directory.
Use `--no-context` for source-only extraction without saved architecture claims.
Use `--context PATH` to select a different context file; these two options cannot combine.

Read `analysis-coverage.json` before interpreting the graph.
The same bundle includes the [knowledge graph projection](../../.agents/skills/service-dependencies-graph/references/architecture/knowledge-graph.md).
It connects declared domain records, exact sources, catalogs, audits, and behavior-review evidence.
Query `knowledge`, `references`, or bounded `paths` through the registered resource.
Check `knowledge_freshness` separately from repository freshness.
Candidate states and original evidence grades remain visible.
Read `coverage-declarations.json` for deterministic pattern candidates that
typed extractors did not yet account for. Query them with:

```sh
python .agents/skills/service-dependencies-graph/scripts/graph.py --workspace PATH query \
  --data-dir relationships/service-dependencies/generated patterns \
  --args '{"family":"HTTP_ENDPOINT","limit":100}'
```

These candidates have exact source lines and require review before they become
canonical relationships. This separates high-recall searching from semantic
provider resolution.
Record snapshot identity, source freshness, independent Git revisions, dirty states, and source fingerprints.
Filesystem source copies can have fingerprints without Git revisions.
Static declarations do not prove runtime invocation, deployment, or approved business intent.
Dynamic nginx templates cannot establish concrete upstream identities without supported bindings.

## Viewer hierarchy

The viewer opens Knowledge when the bundle contains its projection.
Select Architecture for system connections and source dependency details.
The hierarchy controls presentation depth and does not assign business criticality.

| Priority | View | Included relationships |
| --- | --- | --- |
| Highest | System connections | Resolved API, data, and shared-module links between repositories. |
| Medium | Interfaces, data, and shared code | Individual calls, data access, module imports, and handler invocations. |
| Lowest | Package dependencies | Declared libraries and build tools. |

Ownership context remains optional within the medium view.
Structural grouping does not establish component reuse or function execution.
The extractors do not provide complete function-call analysis.

Line colors identify relationship families.
Card markers identify node roles.
Arrows follow the recorded relationship.
For reads, arrows point to data sources.
Provider status controls line style and appears in the relationship inspector.

`Resolved` means that consumer and provider evidence matched within the graph.
`Declared only` means that source evidence exists without an established provider match.
`Unresolved` means that the extractor could not identify the provider.
`Ambiguous` means that several providers matched.
`Candidate` means that the relationship is inferred and requires source review.

An unresolved relationship does not establish a defect.
An external or unknown node does not establish a third-party service.

Filter by repository, family, provider status, boundary, exact relationship, or search text.
Sort by connection count, name, family, or provider status.
The diagram displays at most 36 nodes and 48 relationships.
The overview also retains unconnected repository cards.
The relationship list includes every filtered match across pages.
Select a relationship to inspect canonical edge IDs and source evidence.

Registered `graph.snapshot` adapters query the same validated bundle through CLI `call` or MCP `workbench_call`.
The project resource grants `coverage`, `patterns`, `relationships`, `services`, `search`, `neighborhood`, `knowledge`, `references`, and `paths`.
The adapters invoke skill helpers and retain Workbench action records.
Direct skill commands retain snapshot metadata without Workbench action records.

Generated workspaces use their copied skill helpers and configured tool grants.
Initialization copies this guide and the complete canonical skill.
It leaves live graph output behind.

Read the canonical skill for build, query, evidence, and source audit procedures.

## Source-driven discovery

Ask the [canonical skill](../../.agents/skills/service-dependencies-graph/SKILL.md) to discover dependencies from all in-scope repositories.
Human relationship input and architecture notes are optional.
The [source investigation workflow](../../.agents/skills/service-dependencies-graph/references/architecture/initial-instruction-investigation.md) starts with the repository census and boundary declarations.
The agent inspects missing syntax and unresolved identities, repairs demonstrated extraction gaps, and checks the rebuilt evidence.
It records unavailable sources and deployment bindings as explicit limits.

Use optional `relationships/service-dependencies/initial-instructions.md` for hypotheses, source locations, and corrections when useful.
Its absence does not block discovery. Existing notes are checked against independently inspected sources.

The optional `architecture-context.json` stores reviewed conclusions, source hashes, and relationship assessments.
Version `1.1.0` integrates investigated relationships into graph nodes, queries, and the main viewer.
Keep corresponding business explanations in candidate knowledge with source qualifications and unavailable boundaries.
Keep unavailable gateways as explicit boundaries. Library subjects do not assert deployed services.
Reviewed relationships preserve provider uncertainty and do not select deployments.

Normal builds include the JSON context when it exists.
Build commands do not investigate Markdown notes or refresh saved conclusions.
Ask the agent to investigate sources before final regeneration. A build command alone does not complete semantic source review.
Discovery completeness applies to the reviewed source boundary, with unavailable and unsupported scope stated explicitly.
Keep project-specific architecture in optional workspace inputs. Keep validation and rendering enhancements inside the canonical skill.
