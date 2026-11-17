# Local ADO connector capability inventory

> No critical conclusions require user attention or action in this inventory. Replacement suitability is assessed in the owning maintenance record.

Assessed 13 November 2026 for the [preserved user request](user-input.md#exact-user-input).

- Workbench HEAD: `79a4104035785b7d8c37e6d424d5d4c888104eee`.
- `git status --short -- core/connectors/packages/ado core/connectors/packages/ado-*` returned no changes at inspection. Other worktree changes are outside this inventory.
- Inspection method: read registrations, schemas, API calls, and workflow implementation; enumerate tool registrations from the source. This is source evidence, not live ADO verification.
- `configureAdoTools` registers **87 tools in 9 modules**. The separate upload app adds **2 tools and 1 UI resource** and is not imported by the aggregator. Native bridge additions and grants are assessed by the parent task separately.
- Source of aggregation: [ado/src/tools.js](../../../core/connectors/packages/ado/src/tools.js), lines 1–27. The standalone entry also registers prompt helpers; the native Workbench bridge must be assessed separately before claiming those helpers are available there.

## Material semantics and limits

These details matter when comparing a skill or CLI workflow with the existing interface.

| Source | Behavior to preserve or deliberately replace |
| --- | --- |
| Work-item reads, lines 44–62, 253–298, 468–511 | `my_work_items` runs WIQL then hydrates IDs (default 20); saved-query results hydrate IDs (default 100); query URL helper parses query/query-edit GUID URLs or project+ID and hydrates up to 200 by default. |
| Work-item reads, lines 302–372, 424–464 | PR/commit helpers filter work-item `ArtifactLink` relations. Linked-work-item helper expands and hydrates parent/child/related IDs into named groups. |
| Work-item reads, lines 376–420 | Revision retrieval has top/skip; attachment download streams bytes and returns `base64Content` in JSON. |
| Work-item reads, lines 515–573 | Dashboard helper parses URL or project/team/dashboard ID, reads widgets, extracts `queryId`/`savedQueryId` from JSON settings, executes each saved query, and returns widget identity plus hydrated work items. This is an aggregation workflow, not only dashboard metadata retrieval. |
| Work-item writes, lines 35–73, 142–171 | Arbitrary JSON Patch create/update; batch update loops over items and retains per-item success/error, rather than an atomic bulk transaction. |
| Work-item writes, lines 76–139, 174–247 | Child/relation links, removal by relation type or URL with descending index deletion, and explicit PR artifact URI linking. |
| Repo reads, lines 54–101, 104–205, 256–328 | PR list supports creator/reviewer/source/target/status; several branch helpers auto-discover project by searching projects. PR detail may include linked work-item refs. `list_my_branches` currently does not actually restrict by creator; it is a best-effort alias over returned branches. |
| Repo reads, lines 332–486 | Commit search has message/author/committer/date/range/IDs/version/paging and optional work-item links. File content and directory listing accept branch/tag/commit versions. `get_pull_request_changes` returns iteration change metadata; despite its description, its handler does not fetch textual patch content. |
| Repo writes, lines 88–213 | Branch creation can select source commit/branch/default; PR create normalizes refs, supports fork, draft, linked work items, and only adds the first supplied label in its current handler. |
| Repo writes, lines 216–376, 520–543 | PR completion settings plus fuzzy identity resolution and reviewer add/remove. IdentityPicker tries original, then two comma orders for a two-token name. Numeric reviewer identifiers are converted to `@zone1.scb.net` by the current implementation; this is tenant-specific behavior, not a generic ADO contract. |
| Repo writes, lines 378–517 | General or inline right-side threads, thread status updates, replies, and vote mapping. Current vote handler uses the PR creator identity; do not claim correct current-user voting from its description alone. |
| Review, lines 128–239 | `post_pr_comment` creates inline thread or reply and prepends `🤖 Co-pilot Assisted Review: `. Cleanup enumerates all threads and deletes comments containing that prefix, collecting per-comment errors. |
| Review, lines 251–466 | `repo_review_pr` and `repo_pr_diff` retrieve PR metadata then clone/fetch Git, resolve merge base, and return full per-file textual diffs; clean temporary repositories. Review also loads `CODE_REVIEW_GUIDE_FILE`. Analysis and suggestion posting are performed by the agent: the handler itself returns context and does not autonomously review/post findings. Tool descriptions about automatic posting do not supply authorization. |
| Pipelines, lines 54–192, 194–297 | Run supports normalized self branch, string template parameters, variables with secret flags, and stagesToSkip. Run list uses Pipelines API per pipeline or Build API project-wide. Build list has definition/branch/status/result/IDs/top filters. |
| Pipelines, lines 300–391 | Cancellation updates Build status. Stage retry uses explicit PATCH to `builds/{buildId}/stages/{stageName}` with `state: retry` and `forceRetryAllJobs`. |
| Pipelines, lines 394–472 | Work-item-associated pipelines scans recent builds (default 50), checks each build's work-item refs, and returns a projected build summary; failures for individual builds are skipped. It does not establish an exhaustive historical relationship. |
| Pipelines, lines 475–581 | Build log helper lists logs, fetches every log's lines and concatenates them; build changes, artifact metadata, and variable-group reads have separate tools. |
| Testplans, lines 18–183 | Plan list/create, hierarchical suite list/create, add cases, and recursive case listing (child suites included by default). A suiteType schema does not itself guarantee every dynamic/requirement-suite variant is valid without additional data. |
| Testplans, lines 186–267 | Test-case create and full step replacement build `Microsoft.VSTS.TCM.Steps` XML from action/expectedResult fields. Create also sets title, area, optional iteration/priority. |
| Testplans, lines 270–305 | Build test-results helper discovers runs, fetches each run's results, filters outcomes, and projects title/outcome/error/stack/duration into `testRuns`. |
| Sprints, lines 6–210 | Project iteration tree, batch create dated iterations, team assignment and timeframe list, capacity reads across teams or one team, member activity/days-off update, and team settings. Cross-team capacity helper skips teams that error. |
| Search, lines 6–87 | ADO Code Search and Work Item Search REST endpoints on `almsearch.dev.azure.com`, with domain-specific filters and top/skip. These differ from merely searching a local clone or running WIQL. |
| Upload app tools, lines 17–132, 140–166 | Separate MCP App UI plus headless multi-file base64 upload. Headless upload calls createAttachment per file then adds AttachedFile relations to the work item; returns attachment IDs. UI is exposed as `ui://ado-upload-ui`. |
| `ado-core/src/connection.js`, lines 4–8 | SDK connection uses configured org URL and PAT. The native bridge has additional configuration/security behavior assessed outside this package inventory. |

## Exhaustive tool registrations

Each link points to the implementation file; the line is the `server.tool` registration. Counts represent exposed operations, not behavior-equivalence coverage percentages.

### ado-pipelines — 14 tools

[Source](../../../core/connectors/packages/ado-pipelines/src/tools/pipelines.js)

| Tool | Line | Registered description (qualified above) |
| --- | ---: | --- |
| `pipelines_get_build_definitions` | 24 | Retrieves a list of build/pipeline definitions for a given project. |
| `pipelines_run_pipeline` | 54 | Trigger/queue a new pipeline run. You can specify branch, variables, and other parameters. |
| `pipelines_list_runs` | 105 | List pipeline runs for a specific pipeline or project. Can filter by branch and status. |
| `pipelines_get_run` | 194 | Get details of a specific pipeline run. |
| `pipelines_get_build_status` | 215 | Get the status of a specific build/pipeline run using build ID. |
| `pipelines_get_builds` | 235 | Get builds/pipeline runs with various filters including branch, status, and definition. |
| `pipelines_cancel_run` | 300 | Cancel a running pipeline/build. |
| `pipelines_retry_stage` | 335 | Retry/restart a specific stage in a pipeline run. |
| `pipelines_list_work_item_pipelines` | 394 | Find all pipeline runs that are linked to a specific work item (useful for release work items). |
| `pipelines_get_build_log` | 475 | Retrieve the combined log output for all steps of a specific build. |
| `pipelines_get_build_changes` | 504 | Get the commits and changesets associated with a specific build. |
| `pipelines_list_artifacts` | 525 | List all published artifacts for a given build. |
| `pipelines_list_variable_groups` | 545 | List variable groups (Library) for a project, optionally filtered by name. |
| `pipelines_get_variable_group` | 566 | Get a specific variable group (Library) by ID, including its variables. |

### ado-repos-read — 12 tools

[Source](../../../core/connectors/packages/ado-repos-read/src/tools/repos-read.js)

| Tool | Line | Registered description (qualified above) |
| --- | ---: | --- |
| `repo_list_repos_by_project` | 22 | List all repositories in a given Azure DevOps project. |
| `repo_list_pull_requests_by_repo_or_project` | 54 | List pull requests for a repository or project with optional filters. |
| `repo_list_branches_by_repo` | 104 | List all branches in a repository. |
| `repo_list_my_branches_by_repo` | 156 | List branches in a repository created by current user. |
| `repo_list_pull_request_threads` | 208 | List all comment threads for a pull request. |
| `repo_get_repo_by_name_or_id` | 237 | Get repository details by name or ID. |
| `repo_get_branch_by_name` | 256 | Get branch details by name. |
| `repo_get_pull_request_by_id` | 295 | Get pull request details by ID. |
| `repo_search_commits` | 332 | Search for commits in a repository with comprehensive filtering. |
| `repo_get_file_content` | 391 | Get the content of a file from a Git repository at a specific version (branch, tag, or commit SHA). |
| `repo_list_directory` | 423 | List files and folders in a directory within a repository. Supports recursive listing. |
| `repo_get_pull_request_changes` | 452 | Get the file changes (diff) for a pull request with line-by-line code content. |

### ado-repos-write — 9 tools

[Source](../../../core/connectors/packages/ado-repos-write/src/tools/repos-write.js)

| Tool | Line | Registered description (qualified above) |
| --- | ---: | --- |
| `repo_create_branch` | 88 | Create a new branch in a repository. |
| `repo_create_pull_request` | 150 | Create a new pull request from a source branch to a target branch in an Azure DevOps repository, with optional title, description, draft mode, labels, and linked work items. |
| `repo_update_pull_request` | 216 | Update an existing pull request (title, description, status, completion settings). |
| `repo_update_pull_request_reviewers` | 282 | Add or remove reviewers from a pull request using employee ID, email, or display name (fuzzy-matched, including "Surname, Firstname" order). |
| `repo_create_pull_request_thread` | 378 | Create a new comment thread on a pull request. |
| `repo_vote_pull_request` | 438 | Cast a vote on a pull request (approve, approve with suggestions, wait for author, reject, or reset). |
| `repo_update_pull_request_thread` | 472 | Update the status of an existing pull request comment thread (e.g., resolve, close, reactivate). |
| `repo_reply_to_comment` | 496 | Reply to a specific comment inside an existing pull request thread. |
| `core_get_identity_ids` | 520 | Resolve Azure DevOps user identities (names, emails, or usernames) to their ADO identity IDs. Fuzzy-matched, including "Surname, Firstname" order. Call once per person — do not join multiple people into a single searchFilter. Useful for reviewer assignment and other identity-based operations. |

### ado-review — 4 tools

[Source](../../../core/connectors/packages/ado-review/src/tools/review.js)

| Tool | Line | Registered description (qualified above) |
| --- | ---: | --- |
| `post_pr_comment` | 128 | Post a comment on a PR. Usage: 'Post PR Comment <PR_URL> <filePath> <line> <commentText> [threadId]'. If threadId is omitted, creates a new thread. |
| `delete_all_pr_review_comments` | 183 | Delete all AI-generated review comments from a PR. Usage: 'Delete all PR review comments <PR_URL>' |
| `repo_review_pr` | 251 | Review PR <PR URL>. Posts suggestions as PR comments on the corresponding lines. Loads review guidelines from the file path set in CODE_REVIEW_GUIDE_FILE; if not configured, includes a notice to set it. All suggestions are posted automatically without requiring permission. |
| `repo_pr_diff` | 361 | Get the diff of a pull request by providing its Azure DevOps PR URL. Usage: 'PR Diff <PR_URL>' |

### ado-search — 2 tools

[Source](../../../core/connectors/packages/ado-search/src/tools/search.js)

| Tool | Line | Registered description (qualified above) |
| --- | ---: | --- |
| `search_code` | 6 | Search for code text across Azure DevOps repositories. Supports filtering by project, repository, branch, and file path. |
| `search_workitem` | 48 | Search Azure DevOps work items by free text with optional filters for project, type, state, and assignee. |

### ado-sprints — 8 tools

[Source](../../../core/connectors/packages/ado-sprints/src/tools/sprints.js)

| Tool | Line | Registered description (qualified above) |
| --- | ---: | --- |
| `work_list_iterations` | 6 | List all iterations (sprints) defined in an Azure DevOps project. |
| `work_create_iterations` | 26 | Create new sprint iterations in an Azure DevOps project. |
| `work_list_team_iterations` | 57 | List sprint iterations assigned to a specific team in a project. |
| `work_assign_iterations` | 79 | Assign existing project iterations to a specific team. |
| `work_get_iteration_capacities` | 107 | Get capacity breakdown for all teams in a project iteration. |
| `work_get_team_capacity` | 138 | Get capacity for a specific team in a specific sprint iteration. |
| `work_update_team_capacity` | 160 | Update a team member's activity capacity for a sprint. |
| `work_get_team_settings` | 193 | Get team settings including default iteration, backlog iteration, and default area path. |

### ado-testplans — 9 tools

[Source](../../../core/connectors/packages/ado-testplans/src/tools/testplans.js)

| Tool | Line | Registered description (qualified above) |
| --- | ---: | --- |
| `testplan_list_test_plans` | 18 | List all test plans in an Azure DevOps project. |
| `testplan_create_test_plan` | 44 | Create a new test plan in an Azure DevOps project. |
| `testplan_list_test_suites` | 77 | List all test suites in a test plan, returned in a hierarchical structure. |
| `testplan_create_test_suite` | 102 | Create a new test suite inside a test plan. |
| `testplan_add_test_cases_to_suite` | 130 | Add existing test case work items to a test suite. |
| `testplan_list_test_cases` | 153 | List all test cases in a test suite. By default also includes test cases from child suites, since many suites are organized as containers whose test cases live in nested child suites. |
| `testplan_create_test_case` | 186 | Create a new test case work item with optional steps. |
| `testplan_update_test_case_steps` | 232 | Update the steps of an existing test case work item. |
| `testplan_show_test_results_from_build_id` | 270 | Get test pass/fail results for a specific build. Returns test case titles, error messages, stack traces, and outcomes. |

### ado-workitems-read — 20 tools

[Source](../../../core/connectors/packages/ado-workitems-read/src/tools/workitems-read.js)

| Tool | Line | Registered description (qualified above) |
| --- | ---: | --- |
| `wit_list_projects` | 5 | List all projects in the Azure DevOps organization. |
| `wit_get_work_item` | 21 | Retrieve details of a specific Azure DevOps work item by its ID. |
| `wit_my_work_items` | 44 | List work items assigned to the current user. |
| `wit_get_work_items_batch_by_ids` | 70 | Get multiple work items by IDs. |
| `wit_list_work_item_comments` | 89 | List comments for a work item. |
| `wit_get_work_item_type` | 117 | Get field definitions and metadata for a specific work item type (e.g., Bug, Task, User Story) in an Azure DevOps project. |
| `wit_list_backlogs` | 137 | List all backlog levels (e.g., Epics, Features, Stories) available to a specific team in an Azure DevOps project. |
| `wit_list_backlog_work_items` | 157 | List all work items in a named team backlog level (identified by backlogId, e.g. 'Microsoft.RequirementCategory') in an Azure DevOps project. |
| `wit_list_teams` | 178 | List all teams in an Azure DevOps project. |
| `wit_list_iterations` | 197 | List all iterations for a project and team. |
| `wit_get_work_items_for_iteration` | 217 | Get work items for a specific iteration. |
| `wit_get_query` | 253 | Get a work item query by ID. |
| `wit_get_query_results_by_id` | 273 | Execute a query and get results by query ID. |
| `wit_list_work_item_pull_requests` | 302 | List all pull requests linked to a work item. |
| `wit_list_work_item_commits` | 339 | List all commits linked to a work item. |
| `wit_list_work_item_revisions` | 376 | Get the full revision/change history of a work item. |
| `wit_get_work_item_attachment` | 398 | Download a work item attachment by its ID and return the content as base64. Useful for viewing images or files attached to bugs. |
| `wit_get_work_item_links` | 424 | Get work items linked to a given work item, grouped by relation type (parent, child, related). |
| `wit_query_by_url` | 468 | Get work items from a saved Azure DevOps query, given its URL or project+queryId. |
| `wit_get_dashboard_work_items` | 515 | Get work items from all query-backed widgets on an Azure DevOps dashboard, given its URL or project+dashboardId. |

### ado-workitems-write — 9 tools

[Source](../../../core/connectors/packages/ado-workitems-write/src/tools/workitems-write.js)

| Tool | Line | Registered description (qualified above) |
| --- | ---: | --- |
| `wit_add_work_item_comment` | 6 | Add a comment to a work item. |
| `wit_update_work_item` | 35 | Update a work item by applying a JSON patch document (array of {op, path, value} operations) to the specified work item ID. |
| `wit_create_work_item` | 55 | Create a new work item of a given type in an Azure DevOps project using a JSON patch document to set fields such as title, description, and area path. |
| `wit_add_child_work_items` | 76 | Add child work items to a parent work item. |
| `wit_work_items_link` | 108 | Create a link between two work items with a specified relation type. |
| `wit_update_work_items_batch` | 142 | Update multiple work items in batch. |
| `wit_work_item_unlink` | 174 | Remove one or more links from a work item by link relation type or URL. |
| `wit_link_work_item_to_pull_request` | 217 | Explicitly link a work item to an existing pull request using an artifact link. |
| `wit_update_work_item_comment` | 252 | Edit the text of an existing comment on a work item. |

### Separate upload app — 2 tools and 1 resource

[Source](../../../core/connectors/packages/ado-upload-app/src/tools.js)

| Surface | Line | Purpose |
| --- | ---: | --- |
| `wit_upload_attachment_ui` | 22 | Open embedded attachment picker with optional project/work-item prefill. |
| `wit_upload_attachment` | 58 | Upload base64 files and add work-item attachment relations. |
| `ui://ado-upload-ui` | 141 | Serve the bundled MCP App HTML resource. |

## Prompt helpers

The aggregator's `configureAdoPrompts` delegates to nine prompt modules (87 named prompt registrations across those modules). These are agent guidance over the tool families, not 87 additional deterministic operations. Examples include `review-pr`, `analyze-pr-diff`, `delete-pr-review-comments`, `query-by-url`, `get-dashboard-work-items`, `retry-pipeline-stage`, `show-build-test-results`, capacity management and code/work-item search. No additional SDK operation was found only in prompts. See [aggregator prompts](../../../core/connectors/packages/ado/src/prompts.js) and each module's `src/prompts.js`.

## Source bindings

Files below were inspected or used to enumerate the surface. SHA-256 binds this inventory to the source bytes in the otherwise dirty workspace.

| File | SHA-256 |
| --- | --- |
| `core/connectors/packages/ado-pipelines/src/tools/pipelines.js` | `8b5113e413c4835d2468f5925a548fbaeff82cb355740020c0e1306385a7decf` |
| `core/connectors/packages/ado-repos-read/src/tools/repos-read.js` | `a3a92d602c52568301c67e0b1f0a7f7d060e1bbd0c9059573e4467d67d82a2b3` |
| `core/connectors/packages/ado-repos-write/src/tools/repos-write.js` | `223431ea8b41eb4050e2780063ee097246807e50b89059c26e67127ae0c327d5` |
| `core/connectors/packages/ado-review/src/tools/review.js` | `7e0b7a5f9f872b27773713b88a0dfd848da3a5fb2c671ca5617c6094affcfbde` |
| `core/connectors/packages/ado-search/src/tools/search.js` | `ff09f0e0e6bc16b69623e985e0c8e44d0e035e1d7fdbf9b16c141985a23c6cd5` |
| `core/connectors/packages/ado-sprints/src/tools/sprints.js` | `53e6c0f7e7589928fd5f3a9fb247dc38cf1a200c536aff2a10d658e5af5b9669` |
| `core/connectors/packages/ado-testplans/src/tools/testplans.js` | `92086b484bceb56e814e1904c0df688489e6aab4da8ca796bb28e7ad15799460` |
| `core/connectors/packages/ado-workitems-read/src/tools/workitems-read.js` | `338e94d510716072466109b700e011e811c8665d84fd79ac3426db1df3fc3bb1` |
| `core/connectors/packages/ado-workitems-write/src/tools/workitems-write.js` | `aac8537ad0577cffa344e7310052afcb028b10b90dc9426f95266caecee13b13` |
| `core/connectors/packages/ado/src/tools.js` | `ede0443fe6526de823b10f1289e621b6b16eb3c75ff3a026dc01bfda03f24b00` |
| `core/connectors/packages/ado/src/prompts.js` | `6f5ef892638019d8c1528d0e85b9bc4775c33739d91021452ed2cc7bfbc633bd` |
| `core/connectors/packages/ado-core/src/connection.js` | `b8e6a122d571689e5cdcd7fa89cd93643b756dbc7784384cab3361928135ddc4` |
| `core/connectors/packages/ado-upload-app/src/tools.js` | `f56210c80493a3e6bde013f120bbe77d74fbc3156953d34999f886cafd7f3539` |

## Verification limits

Static registration count and handler inspection completed. No ADO requests, writes, reviews, live authentication, or upload operations were executed. Existing test suites were not rerun because no implementation changed. Source inspection exposes existing implementation limits; this inventory does not certify all registered tools as correct. No runtime, grants, credentials, or upstream packages were changed.
