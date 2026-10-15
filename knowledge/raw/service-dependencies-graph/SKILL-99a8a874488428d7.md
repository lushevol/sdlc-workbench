---
name: service-dependencies-graph
description: Build and query a deterministic, static cross-repository dependency graph from local source and configuration. Use for architecture discovery, coverage audits, and requirement or code impact analysis.
---

# Service Dependencies Graph

Use explicit graph-build and MCP query commands to answer architecture questions with the published Service Dependencies Graph.
Use the workflow table to select the command sequence before interpreting results.
The graph proves static source and configuration relationships.
It does not prove deployment, runtime reachability, or future business intent.
Follow the [output standard](../../../docs/SDLC_OUTPUT_STANDARD.md) for authored reports and review results.

## Purpose and design

Repository-scoped tools cannot show the dependency picture across all repositories.
This skill builds that picture from deterministic source and configuration extraction.
Scripts establish declarations, identity joins, evidence, and coverage limits.
AI selects commands, queries the graph, and explains the result.
AI must not invent a dependency when scripts cannot establish one.

Use this execution order for a cross-repository system view:

1. Inventory every manifest entry and local repository checkout.
2. Extract dependency declarations from each supported repository.
3. Resolve only joins that satisfy the declared evidence rules.
4. Validate one complete snapshot before publication.
5. Query the snapshot and explain confirmed links, candidates, and gaps.

The graph is the shared system model for all repositories in scope.
The human report is a projection of that model.
The MCP server reads the same validated snapshot.
Do not replace a graph build with prompt-only repository inspection.

## Dependency extraction map

Use the extractor and resolver that match the dependency type.

| Dependency | Extraction and resolution | Evidence limit |
| --- | --- | --- |
| Web API | `extract_web_interfaces.py`, `extract_spring_endpoints.py`, then HTTP resolution | Requires an explicit provider, compatible method/path, and known authority when needed |
| WebSocket/STOMP | `extract_web_interfaces.py`, `extract_websocket_endpoints.py`, nginx route resolution | SockJS/STOMP client paths and Spring `registerStompEndpoints` paths require a declared upstream identity and exact rewritten path; IP-only or unknown upstreams remain unresolved |
| GraphQL provider/client | Spring/DGS resolver annotations and `extract_web_interfaces.py`, then protocol-specific evidence review | Annotated providers and static client endpoints are supported; schema-only fields, imported wrappers, and resolver-to-schema type checking remain unresolved |
| Feign service call | `extract_feign_clients.py`, service identity extraction, then alias resolution | Requires a unique declared service identity; URL overrides remain unresolved |
| Java URI-based HTTP call | `extract_java_http.py`, then authority/path resolution | Literal URLs and unambiguous same-repository string constants are supported; dynamic URI expressions remain unresolved diagnostics |
| Kafka flow | `extract_kafka_dependencies.py`, `java_kafka_helpers.py`, then topic comparison | Exact constants, supported record/header sends, configuration bindings, and bounded typed helpers retain source evidence; equal names without cluster/environment identity remain candidates |
| npm or Maven/POM | `resolve_repository_relationships.py` retains every supported direct dependency and resolves exact published coordinates | External packages remain unresolved build boundaries; package declarations do not prove runtime invocation |
| Database access | `extract_java_dependencies.py` using runtime clients, queries, and mapper declarations | Migrations and equal table names do not prove runtime access |
| MFE or SystemJS import | Web manifest and literal import extraction, then package identity resolution | Requires an exact declared provider identity |
| Gateway/API route | `extract_gateway_routes.py` plus resolver joins for nginx and Spring `open-apis` declarations | Unsupported rewrite chains and deployment activation remain unresolved |
| Cache/platform | Spring Redis client/configuration extraction plus explicit platform clients | Cluster identity and key-level behavior require separate evidence |
| Internal gRPC/data-provider SDK | `extract_grpc_dependencies.py` detects an imported `RatanBusinessDataProviderService` with a direct `performCashflowInternallyQuery(...)` call and retains the exact Maven SDK coordinate | The external provider and channel/authority remain unresolved; generic gRPC stubs, `.proto` files, protobuf serialization, wildcard aliases, and tracing-only gRPC configuration are unsupported |
| Camel/file-transfer route | Camel getter calls are bound to matching configuration keys for input and publish direction; Kafka, file, HTTP, and unknown routes retain their raw URI and protocol | The provider or deployment remains unresolved. A `file:` route is an external file channel, not Kafka or SFTP. A Maven SFTP dependency or local transfer strategy does not prove runtime SFTP. Dynamic Camel endpoints remain unresolved diagnostics |
| Local file access | `extract_file_dependencies.py` checks parsed calls to known Java file APIs | Each repository has its own FILE boundary. Path and provider identity remain unknown. Arguments and deployment paths are omitted |
| External platform | Explicit client or configuration extraction | Naming alone does not establish a platform or deployment path |

Read [implemented extraction and limits](references/architecture/automated-analysis.md) before claiming support.
The coverage report takes precedence over this summary when a repository has diagnostics or an unsupported layout.

Keep four evidence classes separate:

- `CONFIRMED`: a validated declaration or join with direct evidence.
- Resolved repository joins also retain consumer and provider evidence.
- `CANDIDATE`: a semantic match or inferred relationship that needs corroboration.
- `UNRESOLVED`: a boundary or declaration with a recorded missing, conflicting, or unsupported link.
- `UNKNOWN`: a repository, layout, or execution state that the analysis did not inspect.

Do not convert a `CANDIDATE`, `UNRESOLVED`, or `UNKNOWN` result into a confirmed fact.
An empty result does not prove independence.
These reporting classes do not replace graph status fields.
Preserve exact `assertion_status` and `resolution_status` values in evidence records.

## Choose the workflow

Select the smallest workflow that answers the request.

| User intent | Start here | Required inputs | Primary output |
| --- | --- | --- | --- |
| Build or audit the repository census | `scripts/graph-build.sh` | Workspace and local repositories | Coverage, diagnostics, and generated snapshot |
| Explain the architecture | `get_analysis_coverage`, then `get_system_overview` or `list_services` | Repository name, capability, or protocol | Services, nodes, links, and limits |
| Trace one repository or boundary | `get_service_picture`, `get_dependencies`, `get_repository_relationships` | Repository name or optional repository filter | Consumer/provider evidence and unresolved frontiers |
| Explore a named concept | `search_architecture`, then `get_node_neighborhood` | Concrete term or node ID | Candidate nodes and direct evidence |
| Assess a requirement | Route to `$requirement-impact-analysis` | Requirement and business context | Business-first impact with graph candidates |
| Assess a PR or code change | `analyze_code_impact`, then GitNexus | Workspace-relative changed files and repository refs | Business/runtime impact and exact symbol follow-up |
| Change graph behavior | Read the graph contract and extension references | Defect or supported syntax target | Fixture-backed extractor, resolver, and validation change |

Use `$ask-repo` for setup, cloning, indexing, dependency checks, and general harness maintenance.
Use `$gitnexus-exploring` or `$gitnexus-impact-analysis` for exact symbols, callers, and business-repository blast radius.

## Readiness gate

Before drawing conclusions, establish the input state.

1. If setup is uncertain, run `./scripts/check-dependencies.sh` and `./scripts/status.sh`.
2. Call `get_analysis_coverage` before other graph interpretation.
3. Record the snapshot checksum, generation time, and source fingerprints.
4. If the bundle is missing, incomplete, or stale for the question, run `scripts/graph-build.sh`.
5. Re-read coverage after the build and report failed or partial repository states.

If required coverage remains missing or stale, block conclusions that depend on it.
You may report independent inspected scope with the blocked claim clearly marked.

Graph generation reads local source. It does not clone repositories or refresh GitNexus indexes.
The harness root remains unindexed. Business repositories live under `repos/`.

Do not use a previous report as current evidence without checking its snapshot identity.
Do not claim freshness from directory timestamps alone.

## Build the graph

From the harness root, run:

```sh
scripts/graph-build.sh
```

This command inventories repositories, extracts declarations, resolves identities, renders projections, validates the bundle, and publishes it atomically.
Use `scripts/graph-build.sh --open` when the viewer is useful.

For another repository directory inside this workspace, with an external output directory, run:

```sh
.venv/bin/python .claude/skills/service-dependencies-graph/tools/generate_all_graphs.py \
  --repos repos/review --out /tmp/service-dependencies-review
```

The build accounts for direct directories under `repos/` and entries in `repos/manifest.json`.
Missing repositories, unsupported stacks, and nested-module gaps remain visible in coverage.

Read generated files in this order:

1. `analysis-report.md` for the human-readable census and relationship summary.
2. `analysis-coverage.json` for statuses, fingerprints, extractors, diagnostics, and limits.
3. `repository-relationships.json` for resolved links, candidates, and unresolved boundaries.
4. `graph.json` for canonical nodes, edges, and source evidence.

`graph.json` is the canonical graph. Other files are projections or summaries.
Inspect consumer and provider evidence before reporting a resolved relationship.
The manifest checksum and snapshot identity must match across published artifacts.

## Query through MCP

The configured `serviceDependenciesGraph` server reads the published bundle.
Use this call order unless the request needs fewer calls:

1. `get_analysis_coverage` establishes readiness and limits.
2. `get_system_overview` or `list_services` establishes the service catalog.
3. `get_repository_relationships` shows cross-repository links and unresolved boundaries.
4. `get_service_picture` and `get_dependencies` explain one repository.
5. `search_architecture` finds named concepts, paths, protocols, or business descriptions.
6. `get_node_neighborhood` verifies direct edges and source evidence.
7. `analyze_requirement_impact` or `analyze_code_impact` runs bounded impact traversal.

For every MCP result, retain the returned snapshot metadata.
Use `repo:<name>` when a tool accepts either a repository name or repository ID.
Use workspace-relative paths for `analyze_code_impact`.
Impact tools default to depth `4` and limit `60`; they accept depth `1`–`8` and limit `1`–`200`.
Neighborhood depth accepts `1`–`4`.

Set depth and limit explicitly when the default traversal does not cover the question.
Inspect total counts before claiming that a bounded result is complete.

Restart the MCP client after changing its advertised tools or launch configuration.
For manual launch, use:

```sh
.venv/bin/python .claude/skills/service-dependencies-graph/tools/service_dependencies_graph_mcp.py \
  --data-dir service-dependencies-graph-output
```

## Interpret graph evidence

Treat resolved cross-repository boundaries as confirmed only when the graph records both sides and a resolution rule.
Treat package and Maven edges as build dependencies with declared scope.
They do not prove a runtime invocation or compatible installed version.
Use the `packages` projection to inspect external declarations without an in-scope producer.

Treat matching Kafka topic names as candidates when cluster or environment identity is unknown. Keep file, HTTP, and unknown Camel channels in the generic message-channel projection; do not report them as Kafka topics.
Local file API calls also use the message-channel projection.
An unknown file path does not establish a shared file or an SFTP connection.
Treat shared table names as unrelated until runtime client evidence proves access.
Treat semantic requirement seeds and AI descriptions as candidates unless authoritative evidence supports them.
Treat external authorities, unsupported gateway syntax, dynamic configuration, and unsupported syntax as unresolved. Supported nginx rewrite plus Spring `open-apis` joins are static routing evidence and still do not prove deployment or runtime reachability.

The graph can establish these supported declarations and joins:

- Web routes, selected HTTP, Java `URI` HTTP calls, GraphQL, SockJS/STOMP WebSocket client declarations, Spring STOMP endpoints, and SystemJS imports.
- Spring controllers, Feign clients, runtime table access, Kafka declarations, and external platforms.
- Camel input and publish routes when Java getter names match the exact configuration key; dynamic endpoint values remain unresolved.
- Direct internal gRPC SDK calls to an external data-provider boundary, with unresolved provider identity.
- Exact internal npm and Maven coordinates, service identities, and explicit provider/client route matches.

The graph does not establish active profiles, deployment routing, generated clients, compiler-level data flow, or production execution. A WebSocket join is static route evidence. It does not prove a live broker session.
Kafka helper analysis requires declared types and a supported topic parameter.
Ambiguous implementations, equal-arity overloads, reassigned topics, and external helpers remain unresolved.
`mfe-root-config` is scan-only foundation metadata, not a selectable application.
DQSL is an external data lake; do not infer Elasticsearch from its name.
Read [implemented extraction and limits](references/architecture/automated-analysis.md) before relying on support claims.
Read the React, Spring, and external-boundary references before extending extraction.

## Requirement and code impact

Requirement impact is a candidate architecture map.
Use OpenKB to establish business intent before treating a graph match as business evidence.
Route material ambiguity to `$requirement-grill` before making an implementation recommendation.
Requirement seeds use `config/service-dependencies-graph-config.json`.
Pass `--config` when you need another policy.

Code impact must select each independent business repository and its base and head revisions.
Use `tools/analyze_impact.py` for repository-aware comparisons:

```sh
.venv/bin/python .claude/skills/service-dependencies-graph/tools/analyze_impact.py \
  --repository service-name --base-ref main --head-ref feature
```

The result must distinguish direct impact, indirect impact, context, candidates, and unresolved frontiers.
Incoming runtime dependencies can propagate impact. Containment is navigation context.
Outgoing reads and dependencies do not make their other callers affected.
Missing or unexamined repositories are limitations, not unaffected results.

For exact symbols or callers, inspect the owning business repository with GitNexus.
Run impact analysis before editing any indexed business symbol.
Run `detect_changes` before committing indexed business-repository changes.
Do not invent a GitNexus risk score when the index is absent or stale.

## Report shape

Use the project output standard for every human-facing result.
Keep the following sections in this order:

1. **Scope and snapshot**: request, repositories, revisions, checksum, and generation time.
2. **Confirmed static evidence**: exact nodes, edges, source paths, and line evidence.
3. **Candidates and inferences**: match reason and required corroboration.
4. **Unresolved and unknown items**: edge status, reason, evidence, and owner.
5. **Impact or architecture view**: direct paths, dependent services, and business/runtime dimensions.
6. **Coverage limits**: unsupported layouts, extractors, missing repositories, and stale inputs.
7. **Next actions**: one concrete action for each material gap.
8. **Validation record**: commands, revisions, results, and artifact identity.

Separate automated output checks from the ASD review:

```json
{
  "standard": "ASD-STE100",
  "automated_check": "PASSED",
  "asd_review": "PENDING",
  "reviewer": null,
  "reviewed_at": null,
  "limitations": ["Automated checks do not certify complete ASD-STE100 compliance."]
}
```

Do not state `PROVEN`, `VERIFIED`, or `NO IMPACT` unless the stated evidence contract supports that status.

## Failure and handoff rules

- If coverage is missing, run `scripts/graph-build.sh` or report the exact missing prerequisite.
- If a snapshot fails validation, keep the prior published snapshot and report the failed build.
- If a repository is absent, use `scripts/clone-repos.sh`; do not invent a local path.
- If a stack or module is unsupported, report the coverage gap and do not infer its relationships.
- If a search or join returns no result, report the search scope and keep independence unresolved.
- If business intent is missing, use OpenKB and `$requirement-grill`; graph descriptions do not approve requirements.
- If exact code callers are needed, hand off to GitNexus with an explicit repository.

## Extend and validate

Read the [graph contract](references/architecture/graph-contract.md) before changing producers or consumers.
For a dependency coverage audit, use the [source audit loop](references/architecture/dependency-audit.md).
Build the baseline before reviewing source declarations.
Do not stop after the build passes.
Compare dependency declarations with canonical evidence and diagnostics.
Fix an observed extraction gap with scripts and regression fixtures.
Rebuild the graph after each completed change set.
Stop when each reviewed declaration has evidence or an explicit unresolved record.
State the reviewed protocols, source layouts, and remaining limits.
Do not claim that static extraction proves complete runtime dependency coverage.

Use this sequence for repeatable graph changes:

1. Define the supported syntax and evidence rule.
2. Update the extractor or declaration parser.
3. Update identity resolution and boundary status handling.
4. Update schema and semantic validation.
5. Update relationship projections and reports.
6. Add positive, negative, ambiguous, and unsupported fixtures.
7. Run `scripts/run-tests.sh`.
8. Run `scripts/graph-build.sh` and inspect the complete published bundle.
9. Review the diff, manifest, diagnostics, and source links.

Do not hand-edit generated graph facts or checksums.
Keep source paths workspace-relative and preserve consumer/provider evidence.
Keep unsupported syntax and ambiguous matches visible through diagnostics.

For parser-specific behavior and limits, use:

- [automated analysis](references/architecture/automated-analysis.md)
- [React extraction](references/architecture/react-extraction.md)
- [Spring extraction](references/architecture/spring-extraction.md)
- [external boundaries](references/architecture/external-boundaries.md)
- [impact analysis](references/architecture/impact-analysis.md)
