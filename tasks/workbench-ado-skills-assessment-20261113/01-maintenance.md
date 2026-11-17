# Azure DevOps skills capability assessment

> **Critical conclusion: Keep the existing ADO connectors for current consumers.**
>
> The requested skills cover a subset of agent workflows and depend on a separate MCP service. They cannot replace the executable connector and report contracts. Action: retain the current integration; use this assessment for any later replacement proposal. Consequence of direct removal: existing ADO calls and release collection lose their providers. Owner of any replacement decision: unknown. Evidence: [complete local inventory](evidence/local-ado-inventory.md), [all upstream skills](evidence/upstream-skills-inventory.md), and [consumer contracts](evidence/bridge-consumer-review.md). No user action is required to complete this assessment. Live service equivalence was not tested.

## Request and scope

- Date: 13 November 2026 (Asia/Singapore).
- High-priority reference: [exact user request](evidence/user-input.md#exact-user-input).
- Authorized work: inspect `microsoft/azure-devops-skills`, compare all ADO connector capabilities in `core/`, and report replacement gaps.
- This is a harness assessment. No connector replacement, installation, external writes, or business behavior changes are requested.

## Outcome

**No: `microsoft/azure-devops-skills` does not cover all ADO connector capabilities in `core/`.** High confidence applies to this source comparison. Runtime equivalence with the separate MCP service remains unverified.

At inspected upstream commit [`b418a6c8fa9fd622274882a1378e664df746f356`](https://github.com/microsoft/azure-devops-skills/tree/b418a6c8fa9fd622274882a1378e664df746f356), the repository contains seven example skills and no executable tools, API client, scripts, tests, or tool schemas. Its [README](https://github.com/microsoft/azure-devops-skills/blob/b418a6c8fa9fd622274882a1378e664df746f356/README.md#L23-L53) requires a configured, authenticated Azure DevOps MCP server. The shipped [MCP configuration](https://github.com/microsoft/azure-devops-skills/blob/b418a6c8fa9fd622274882a1378e664df746f356/.vscode/mcp.json#L1-L8) points to `https://mcp.dev.azure.com`.

The local [`configureAdoTools`](../../core/connectors/packages/ado/src/tools.js) registers 87 tools in nine modules. The [native server](../../core/connectors/workbench/server.js) adds 14 report readers, for **101 registered ADO tools**. The separate [upload app](../../core/connectors/packages/ado-upload-app/src/tools.js) adds **two tools and an embedded UI**, outside the native aggregator. The [current catalog](../../registry/tools.yaml) grants **26** of the 101 tools. [Credential-free discovery](evidence/capability-checks.json) confirmed those counts; registration is not a live execution result.

## Complete capability comparison

Here, “partial” means a documented workflow addresses some related user goals. It does not establish equivalent schemas, output, paging, or errors. “Absent” means no shipped skill workflow covers the named local operations; the separate server may have more tools.

| Local capability family | Local tools | Coverage by the seven skills | Material gaps |
| --- | ---: | --- | --- |
| Work-item and project reads | 20 | Partial: assigned work, item details, batches, comments, backlog hierarchy, project/team/iteration selection | Work-item type metadata, arbitrary saved queries/query URLs, dashboard query aggregation, revisions, attachment download, and specific iteration-item queries have no corresponding workflow. Summary relations provide some link information but do not define all dedicated PR/commit/link helper contracts. |
| Work-item writes | 9 | Absent | Create/update items, JSON Patch, batch updates, child/relation/PR links, unlink, comment create/edit. Iteration creation belongs to sprint administration and does not supply these operations. |
| Repository and PR reads | 12 | Partial: repository listing for security scope | File content at branch/tag/commit, directory listing, branches, commit search, PR details/list/threads/changes. Displaying a PR link in a work-item summary does not fetch its repository or PR data. |
| Repository and PR writes / identities | 9 | Absent | Branch/PR create and update, completion options, reviewer/identity resolution, voting, inline threads, thread updates and replies. |
| PR review workflows | 4 | Absent | Git clone/fetch and merge-base textual diffs, local review-guide loading, prefixed inline review comments and cleanup. The existing review handler returns context; agent analysis and posting remain separate actions. |
| Pipeline operations | 14 | Partial: definitions, build list/status, failed-step log content, associated changes | Queue/run parameters, run details, cancel, stage retry, linked-work-item build discovery, artifacts and variable groups. Selected failed-step logs do not establish parity with the local combined all-step log output. |
| Test Plans | 9 | Absent | Plans, hierarchical suites, recursive test cases, case creation, step XML updates and build test results. |
| Sprint administration | 8 | Partial: project/team iteration list, create and assign | Capacity across teams, team/member capacity reads and updates, and team settings. |
| Search | 2 | Absent | Azure DevOps Code Search and Work Item Search with filters and paging. Backlog filtering and assigned-work retrieval are narrower workflows. |
| Workbench report readers | 14 | No equivalent executable contracts; some work-item/build/log retrieval goals overlap | Full historical expanded work items, timelines, artifacts, build properties, named timeline attachments, coverage, deployment contribution queries, exact commit comparison/history/files, raw headers and evidence contracts. |
| Separate upload app | 2 + UI | Absent | Headless multi-file attachment upload/linking and embedded MCP upload UI. These are not enabled by the current native ADO registration. |

The skills also add an **Advanced Security alert review workflow**. Its `advsec_get_alerts` and `advsec_get_alert_details` tools are not provided by the local ADO modules. This is a useful additional workflow when a compatible service is supplied; it does not close other gaps. See the [complete upstream inventory](evidence/upstream-skills-inventory.md#complete-skill-surface).

All 87 imported operations and both upload operations are enumerated with implementation lines in the [local inventory](evidence/local-ado-inventory.md#exhaustive-tool-registrations). All 14 report readers are enumerated in the [native bridge inventory](evidence/bridge-consumer-review.md#fourteen-ado-report-readers). Tool counts are inventory denominators, not functional coverage percentages.

## Existing caller compatibility

1. **The tool interface differs.** The upstream skills use `wit_work_item` with `action=get`, `pipelines_build` with `action=get_status`, and `work_iteration_write` with `action=create`. Local callers use `wit_get_work_item`, `pipelines_get_build_status`, and `work_create_iterations`. The skills supply neither aliases nor an argument/result adapter. See [upstream tool definitions](evidence/upstream-skills-inventory.md#complete-skill-surface) and [discovered local names/schema hashes](evidence/capability-checks.json).
2. **Release collection has direct executable consumers.** [`core/release_report.py`](../../core/release_report.py) requires matching `connector.mcp` resources, exact reader grants, a persistent session protocol, and `report_*` calls. Adding skill instructions does not satisfy these callers. The [consumer review](evidence/bridge-consumer-review.md#executable-contracts-beyond-endpoint-coverage) traces these paths.
3. **Evidence and execution contracts need preservation.** The native implementation retains raw response data and continuation headers, streams large payloads into exclusive hash-bound files, limits requests and deadlines, retries selected failures, and applies proxy/CA settings. Human-readable skill summaries provide no equivalent runtime implementation.
4. **Service reachability and authentication remain separate.** The local connector uses a configured organization URL/PAT and selected-workspace settings. The skills require an authenticated MCP server but do not define corresponding PAT, proxy, CA, or Azure DevOps Server compatibility. Those properties are unestablished for the separate server, not proven impossible.

No adapter or replacement implementation is authorized by this assessment. If replacement becomes a goal, assess the separate [`microsoft/azure-devops-mcp`](https://github.com/microsoft/azure-devops-mcp) or deployed remote-service schemas as the execution candidate, preserve existing consumer calls through deterministic adapters where possible, and verify raw evidence and configuration parity. Skills alone cannot add missing server operations. Upstream skills can inform optional workflow guidance after tool routing and grants are mapped.

## Scope and risk

Workbench revision: `79a4104035785b7d8c37e6d424d5d4c888104eee`. The worktree has extensive pre-existing documentation and layout migration changes. The inspected ADO implementations, native provider/readers, catalog, and report collector have no local changes; `core/connectors/yarn.lock` has an unrelated pre-existing deletion. All were preserved.

Affected consumers assessed: agent calls through `external-ado`, imported standalone ADO modules and upload app, and native release-report collection. This assessment changes only its task records. Runtime risk is low; removing the connectors without a compatible execution layer would break existing calls. Current implementation limitations in the [local inventory](evidence/local-ado-inventory.md#material-semantics-and-limits) are not guarantees to reproduce or silently fix.

## Evidence and checks

- [User request](evidence/user-input.md).
- [Local complete operation inventory and source hashes](evidence/local-ado-inventory.md).
- [Upstream complete skill inventory with pinned GitHub citations](evidence/upstream-skills-inventory.md).
- [Native bridge, report readers, affected callers and inspected assertions](evidence/bridge-consumer-review.md).
- [Executed discovery, exact registered tool names, grants, schema hashes and upstream file hashes](evidence/capability-checks.json).

Performed checks:

- Inspected all seven shipped skills and all nine local ADO tool modules, standalone upload tools/UI, bridge additions, provider and release-report consumer paths.
- `.venv/bin/ai-sdlc --workspace . status`: succeeded; registered `external-ado` discovered.
- `.venv/bin/ai-sdlc --workspace . call external-ado list`: succeeded, action `4c3cdccad3b746409b09846addbcdd00`; 101 unique tools, 26 granted, 14 report readers. Discovery made no external ADO request.
- Assertions on operation counts, unique names, grants, reader count and seven upstream skill files: passed. Existing report tests were inspected for consequential contracts; tests were not rerun because no implementation changed.
- Final checks passed: retained JSON parsed; all 89 imported/upload tool registrations reconciled with the exhaustive inventory; all 14 report readers reconciled; ten upstream skill/metadata hashes matched; 56 local Markdown file links resolved.

Limits: no skill installation, connector replacement, live ADO operation, separate MCP-server source/schema audit, or end-to-end parity run. The public repository was fetched for inspection only. The initial sandbox fetch failed through the configured proxy; the approved public-repository fetch completed. No credentials were printed or used for service calls.

Writing review: automated link, inventory and data checks passed; manual technical review completed in this chat; formal ASD-STE100 human review pending, reviewer unknown. Link checks do not verify the complete approved dictionary or grammar.

## Documentation reconciliation

Assessed [docs/CONNECTORS.md](../../docs/CONNECTORS.md) sections “Discover and invoke tools” and root configuration, and [docs/RELEASE_REPORT.md](../../docs/RELEASE_REPORT.md) native reader/grant/evidence contracts. They describe the current supported implementation consistently with the inspected sources. No current-guide change is needed because this comparison introduces no integration, configuration, or supported behavior change. The recommendation and its evidence remain with this assessment task.
