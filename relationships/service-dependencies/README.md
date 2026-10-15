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

Read `analysis-coverage.json` before interpreting the graph.
Record snapshot identity, source freshness, independent Git revisions, dirty states, and source fingerprints.
Filesystem source copies can have fingerprints without Git revisions.
Static declarations do not prove runtime invocation, deployment, or approved business intent.
Dynamic nginx templates cannot establish concrete upstream identities without supported bindings.

## Viewer hierarchy

The viewer opens with confirmed system connections.
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
The project resource `service-dependencies` grants `coverage`, `relationships`, `services`, `search`, and `neighborhood`.
The adapters invoke skill helpers and retain Workbench action records.
Direct skill commands retain snapshot metadata without Workbench action records.

Generated workspaces use their copied skill helpers and configured tool grants.
Initialization copies this guide and the complete canonical skill.
It leaves live graph output behind.

Read the canonical skill for build, query, evidence, and source audit procedures.
