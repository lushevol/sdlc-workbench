# Workbench integration analysis

Date: 2026-10-24 (Asia/Singapore).
Scope: Local source inspection for release-report reproduction preparation.
Workbench revision: `4797c7f8944251c5a0b2c1c8fdf20a7147a66db9`.
Intent reference: [exact user input](user-input.md#exact-input).

**Preparation can continue locally. Live collection needs selected ADO identities and exact tool grants.**

## Facts and reuse boundaries

| Surface | Observed behavior | Reproduction use | Evidence |
| --- | --- | --- | --- |
| Python application | `ai-sdlc` maps to `ai_sdlc_workbench.cli:main`. | Keep report orchestration in the existing Python runtime. | [package mapping](../../../pyproject.toml#L34) |
| CLI | `release-clinic` exposes `doctor`, `path`, `collect`, `report`, `portfolio`, `audit`, and `serve`. | Reuse setup and root environment selection. | [CLI parser](../../../core/cli.py#L51), [dispatch](../../../core/cli.py#L93) |
| MCP | `workbench_status` and `workbench_call` share the runtime with CLI operations. | Expose collection through existing registered resources. | [MCP tools](../../../core/mcp.py#L16) |
| Retained actions | Runtime calls retain arguments, configuration hash, result, status, and evidence. | Link each report section to retained collection actions. | [runtime call](../../../core/runtime.py#L56) |
| Connector permissions | The provider checks exact tool names before starting the bridge. | Grant only required reads through the resource catalog. | [grant check](../../../core/providers/connectors.py#L52) |
| Connector credentials | The bridge merges root `.env` with process settings. | Reuse `AZURE_DEVOPS_ORG_URL`, `AZURE_DEVOPS_PAT`, `SONAR_BASE_URL`, and `SONAR_TOKEN`. | [root config](../../../core/connectors/workbench/config.js#L5) |
| Connector lifecycle | The bridge creates an in-memory MCP client, invokes one tool, then closes it. | Avoid importing the snippet's application server. | [bridge execution](../../../core/connectors/workbench/bridge.js#L30) |
| Collection limits | Connector responses have a four MiB limit and the workspace operation timeout. | Design paginated, bounded calls and preserve partial results. | [limits](../../../core/providers/connectors.py#L24), [timeout](../../../core/providers/connectors.py#L62) |
| Release Clinic | It collects release items, build identities, tests, Sonar data, and traceability. | Reuse compatible retained inputs after an explicit field mapping. | [collection](../../../core/release-clinic/plugins/test/dtp-tda-report/skills/dtp-tda-report/scripts/AutoTDAScript.py#L250), [traceability](../../../core/release-clinic/plugins/test/dtp-tda-report/skills/dtp-tda-report/scripts/AutoTDAScript.py#L355) |
| Report output | Release Clinic writes full JSON and compact summary JSON. | Support an adapter for these inputs where evidence supports equivalence. | [JSON output](../../../core/release-clinic/plugins/test/dtp-tda-report/skills/dtp-tda-report/scripts/AutoTDAScript.py#L386) |
| Packaging | The build copies Release Clinic runtime assets into the installed package. | Extend installed assets only when the new feature needs them. | [wheel build customization](../../../setup.py#L11) |
| Workspace generation | Initialization copies selected guides, contracts, and skills from `scaffold.json`. | Ship report guides through the manifest without copying runtime source. | [initialization](../../../core/workspace.py#L77), [manifest](../../../scaffold.json#L2) |

## Available source tools and current grants

Local [ADO discovery](ado-tool-discovery.json) returned `SUCCEEDED` with 87 tool schemas.
The [capability summary](ado-capability-summary.json) preserves selected schemas and exact grants.
No external service request ran during discovery.

| Needed information | Existing tool definition | Current catalog grant | Remaining work |
| --- | --- | --- | --- |
| Release work item and linked items | `wit_get_work_item`, `wit_get_work_items_batch_by_ids` | Granted. | Map custom release fields and relation direction. |
| Build metadata | `pipelines_get_builds`, `pipelines_get_build_status` | Not granted. | Select exact tools after schema discovery. |
| Build changes | `pipelines_get_build_changes` | Not granted. | Confirm whether build changes satisfy the comparison scope. |
| Build artifacts | `pipelines_list_artifacts` | Not granted. | Add only if the selected report consumes artifacts. |
| Commits | `repo_search_commits` | Not granted. | Check supported criteria against required comparison semantics. |
| Pull requests | `repo_get_pull_request_by_id`, `repo_get_pull_request_changes` | Granted. | Keep repository, project, and exact commit identities. |
| Build test results | `testplan_show_test_results_from_build_id` | Not granted. | Check completeness before using these results as test evidence. |
| Sonar measures and quality status | `sonar_get_measures`, `sonar_get_quality_gate_status` | Granted. | Match the component and branch to the report build. |

Evidence: [ADO grants](../../../registry/tools.yaml#L65), [Sonar grants](../../../registry/tools.yaml#L92),
[pipeline definitions](../../../core/connectors/packages/ado-pipelines/src/tools/pipelines.js#L4),
[build changes](../../../core/connectors/packages/ado-pipelines/src/tools/pipelines.js#L503),
[artifacts](../../../core/connectors/packages/ado-pipelines/src/tools/pipelines.js#L524),
[commit search](../../../core/connectors/packages/ado-repos-read/src/tools/repos-read.js#L333),
and [build tests](../../../core/connectors/packages/ado-testplans/src/tools/testplans.js#L271).

## Material findings

### Integration finding 1: Existing grants do not cover the complete collection flow

Fact: ADO pipeline and test source tools exist, but the catalog excludes their names.
Evidence: [tool definitions](../../../core/connectors/packages/ado-pipelines/src/tools/pipelines.js#L4) and [current grants](../../../registry/tools.yaml#L72).
Consequence: The reproduction cannot collect all build and test sections through current grants.
Owner: Workbench maintainer.
Next action: Discover exact schemas and propose the smallest required read grants.

### Integration finding 2: Existing TDA output does not establish snippet parity

Fact: Release Clinic accepts a release work item, build, and stream.
The snippet service starts with a release identifier and optional report fields.
Evidence: [collector parser](../../../core/release-clinic/plugins/test/dtp-tda-report/skills/dtp-tda-report/scripts/AutoTDAScript.py#L69)
and [snippet entry](../../../core/release-report/release-report.service.ts#L38).
Inference: Shared ADO data can reduce duplicate collection, but the output contracts need a field-by-field comparison.
Consequence: Replacing one output with the other can lose comparison or compliance meaning.
Owner: Workbench maintainer.
Next action: Define a versioned report model and document each source adapter's coverage.

### Integration finding 3: Direct Release Clinic commands bypass retained resource actions

Fact: The wrapper starts subprocesses directly and returns their exit codes.
Evidence: [wrapper](../../../core/release_clinic.py#L83) and [runtime evidence](../../../core/runtime.py#L68).
Consequence: A new report cannot assume these commands created Workbench action records.
Owner: Workbench maintainer.
Next action: Save input hashes and operation provenance explicitly, or use registered collection operations.

### Integration finding 4: Existing test output loses test case identities

Fact: The build test tool returns run IDs, titles, outcomes, error text, and duration.
Its result mapping omits test case IDs and result IDs.
Evidence: [result mapping](../../../core/connectors/packages/ado-testplans/src/tools/testplans.js#L288).
Consequence: This output cannot establish the snippet's work-item-to-test relationship by test case identity.
Owner: Workbench maintainer.
Next action: Add a bounded identity-preserving result read before claiming full test traceability.

### Integration finding 5: Missing connector operations need focused additions

Fact: [discovery](ado-capability-summary.json) exposes build metadata and commit search.
It exposes no ADO coverage summary or deployment hierarchy operation.
It also lacks arbitrary commit comparison counts and normalized custom compliance gates.
Evidence: [all discovered schemas](ado-tool-discovery.json) and [snippet diff calls](../../../core/release-report/ado-api/git.ts#L287).
Consequence: Existing pipeline tools alone cannot reproduce build comparison and coverage sections.
Owner: Workbench maintainer.
Next action: Define focused read contracts for these gaps after confirming the intended baseline.

### Integration finding 6: Packaging must preserve the single runtime boundary

Fact: Python owns the CLI and installed runtime.
Optional Node connector source remains outside the Python wheel.
Evidence: [package mapping](../../../pyproject.toml#L34), [build logic](../../../setup.py#L18),
and [generated workspace contract](../../../docs/CONNECTORS.md#L100).
Consequence: A NestJS server, database, and React host would add unsupported installation responsibilities.
Owner: Workbench maintainer.
Next action: Implement the report model and local rendering in Python before considering a separate interactive host.

## Proposed small stages

These stages are proposals.
They do not establish selected business policy or external write authorization.

1. Define the report contract using the supplied service and UI as source evidence.
   Preserve release identity, section states, source locators, timestamps, hashes, and comparison boundaries.
   Distinguish missing, unavailable, skipped, and successful collection.
2. Build an offline Python normalizer and local report renderer from retained JSON.
   Keep TDA interpretation separate from raw report sections.
   Add assertions for partial data, comparison scope, duplicate identifiers, and output escaping.
3. Add required read tools through the existing connector and resource boundaries.
   Reuse current tools where their input contracts fit.
   Add bounded read operations only for confirmed gaps.
4. Collect one selected release and compare its normalized output with retained source responses.
   Preserve project, build, commit, test run, and baseline identities.
   Record unavailable evidence beside affected sections.
5. Add optional graph presentation only after the report contract is stable.
   Keep generated workspaces free from runtime source.
   Validate the wheel and initialized workspace outside this checkout when packaging changes.

Dependency changes must also update dependency analysis, setup, manifests, offline preparation, and readiness checks.
Evidence: [dependency principle](../../../PRINCIPLE.md#7-local-first-minimal-dependencies).

## Existing test evidence and limits

The following assertions were inspected.
No tests ran as part of this analysis.

- [Connector call evidence](../../../tests/test_connector_provider.py#L102) checks retained results and evidence hashes.
- [Exact grant denial](../../../tests/test_connector_provider.py#L131) checks denial before process startup.
- [Discovery grants](../../../tests/test_connector_provider.py#L119) checks allowed flags and input schemas.
- [Local report output](../../../tests/test_release_clinic.py#L37) checks missing Sonar text and review placeholders.
- [Output path boundaries](../../../tests/test_release_clinic.py#L60) check generated filenames remain inside the configured directory.
- [Credential isolation](../../../tests/test_release_clinic.py#L83) checks diagnostic output and process environment preservation.
- [Generated skill assets](../../../tests/test_release_clinic_skill.py#L122) check instruction parity and exclusion of runtime copies.
- [Wheel layout](../../../tests/test_workspace_layout.py#L142) checks installed Release Clinic assets and scaffold separation.

These assertions cover integration boundaries.
They do not verify the supplied TypeScript report or any live ADO release.

## Unknowns

- The intended first release, project, and comparison baseline remain unspecified.
- Custom compliance fields require local mapping and source confirmation.
- The required output format remains unspecified.
- Full graph parity may need a separate browser interaction scope.
- Uploading or attaching output requires a defined destination and separate write scope.

## Local discovery execution

Command: `.venv/bin/ai-sdlc --workspace . call external-ado list`.
Exit code: `0`.
Action: `1288108bd12b48ba8953166a2d4b5c6f`.
Result: `SUCCEEDED`; 87 tools returned.
Evidence: [complete retained response](ado-tool-discovery.json).

This check verifies local schema discovery only.
It does not verify service access, complete collection, or report behavior.

## Review status

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
  - Analysis used local source only.
  - Only local connector schema discovery ran.
  - No external service request or runtime test ran.
```
