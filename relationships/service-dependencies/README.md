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

## Progressive viewer

The initial map contains service and UI module nodes with aggregated directed relationships.
Each service pair has one connection line. Components and other implementation declarations remain in cards and source indexes.
Click a service to focus inbound callers and outbound dependencies in that graph.
Select direction and depth, then expand neighbors or use **Load connections** to append bounded batches.
Use **Overview** to restore the complete service map.
Use the wheel to zoom, drag the background to pan, and **Fit graph** to fit the current graph.

The architecture inventory and legend start collapsed.
The inspector loads source evidence when requested.
The repository inventory includes source-only and testing repositories without creating runtime service identities.
Unknown destination groups add no common provider or runtime relationship.
Provider status remains separate from investigation assessments and execution evidence.
An unresolved dependency does not establish a defect.

Keep `relationship-viewer.html` beside its `relationship-viewer.data/` directory.
Compressed local data loads progressively without a server.
Use a current browser with gzip `DecompressionStream` support.
The complete data bundle still grows with graph evidence. The HTML does not embed all evidence or traces.

Filters select repository, family, provider status, scope, dimension, and evidence assessment.
Search applies to loaded names and paths.
Use **Browse all declarations** to inspect the complete canonical indexes in bounded batches.
Index filters apply within each batch. Continue through remaining batches before claiming absence.
Read the [viewer guide](../../.agents/skills/service-dependencies-graph/references/architecture/viewer-hierarchy.md) for evidence and trace limits.

Registered `graph.snapshot` adapters query the same validated bundle through CLI `call` or MCP `workbench_call`.
The project resource grants `coverage`, `patterns`, `relationships`, `services`, `search`, and `neighborhood`.
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

### Service call snippets

Prioritize internal and external service calls when extending the architecture graph.
Use [snippet discovery](../../.agents/skills/service-dependencies-graph/references/architecture/snippet-discovery.md) to collect candidates and connect call chains through AI source review.
For a flat repository parent, use `build --repos PATH --layout flat`; repository names do not select search patterns.
Use `patterns` with `service_only: true` and `include_snippets: true` to inspect service call candidates.
Search related symbols or destinations with `query`, then trace wrappers, configuration, routes, and providers.

Project direction identifies Solace as the future messaging platform.
Review Solace publishers, consumers, broker/VPN settings, queue/topic destinations, subscriptions, and request/reply bindings when sources contain them.
Keep current Kafka evidence until actual source changes support its removal or replacement.
