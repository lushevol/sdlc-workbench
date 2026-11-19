---
name: workbench-ready
description: Set up, restore, or check an AI SDLC Workbench workspace and its repositories for a first engineering task. Reuse existing installers, repository onboarding, dependency graphs, and task preflight to get the user working in the same session.
---

# Get Workbench ready

Identify the workspace, the repositories in scope, and the user's first task. Reuse existing project declarations and setup instructions.
For a general setup request, prepare local source navigation and report which workflows are available.

For a check-only request, run the launcher with `--check` or use `doctor` and `validate`.
Read catalogs and repository instructions directly. Use `python -B` with the direct script to query an existing graph.
Report prerequisites and stop before operations that write files, probe services, or start the task.

## Prepare the workspace

1. **Check the installation.** Identify the platform, selected workspace, and installed interpreter or executable.
   Check the existing environment's executable if `ai-sdlc` is absent from PATH.
   Use the existing launcher check when the runtime is missing. Follow the connected or matching offline installation route.
   Select core-only setup when the requested work needs only the core.
   Run source launchers from the Workbench source checkout. Use the installed runtime for generated workspaces.
   Follow the [setup guide](../../../docs/SETUP.md#start-setup).
2. **Initialize or restore.** Use an existing workspace in place. Run `ai-sdlc init` for a new empty destination.
   If the launcher already initialized the destination, reuse it.
   When restoring a project, use its tracked workspace and catalogs. Check both catalog locations and executable tool settings.
   Run `doctor --profile core`, `validate`, and `status` with `ai-sdlc --workspace PATH` against the selected workspace.
   Inspect individual diagnostic results to identify prerequisites for the selected task.
3. **Attach the required repositories.** Reuse readable checkouts. Bind registered identities to local paths and record source revisions and checkout changes.
   Restore missing checkouts when the task authorizes it and provides verified source identity.
   Preserve existing branches and local edits. Report unknown upstreams or missing revisions as evidence limits.
   Apply authorized catalog changes through existing schemas. Keep private paths and credentials in their existing local settings.
   Follow the [independent repository guide](../../../repos/README.md).

## Make source easy to navigate

1. Use [repository onboarding](../repository-onboarding/SKILL.md) to locate responsibilities, entry points, contracts, commands, and test assertions.
   Reuse current assessments for the selected scope. Assess changed or missing evidence and keep staging outside target checkouts.
   When requested, generate the repository topic documents and their managed `AGENTS.md` links through the onboarding skill.
2. For multi-repository setup or cross-repository work, use [service dependency discovery](../service-dependencies-graph/SKILL.md).
   Query coverage first. Reuse a current validated snapshot for its covered scope.
   The graph scans checkouts inside the workspace. Inspect external checkouts directly unless the request covers an in-workspace copy.
   Build a missing or stale snapshot when the task permits.
   For stale reviewed context, use the direct graph script with `build --no-context` and a separate output directory.
   Inspect each relevant caller, wrapper, binding, and provider. Record unresolved or unavailable boundaries.
   Where graph coverage is incomplete, use direct source inspection for reachable scope. Name any material gap in the result.

## Start the first task

| First task | Check before starting |
| --- | --- |
| Source navigation or static review | Read the relevant sources at identified revisions. Locate contracts, callers, and available assertions. Route any change review through the [code-review skill](../code-review/SKILL.md). |
| Local development or tests | Check the owning repository's documented toolchain, dependencies, and configuration. Use [test plan and preflight](../../../docs/TEST_PREFLIGHT.md) for supported runners. |
| Live integration or browser verification | Check the selected resource, operation grant, inputs, and environment. Follow the [setup and E2E readiness procedure](../repository-onboarding/references/setup-readiness.md). |

Use the existing installation, tool, and repository permissions for each step. Check private inputs by presence without showing values.
Run approved setup steps that are missing and recheck the affected boundary. Reuse valid results when the evidence still matches.
Use the existing setup reports and owning task record to resume blocked or interrupted work.

Report readiness for the named task with the commands, revisions, and evidence that support it.
For a blocker, name the blocked operation, missing prerequisite, and specific recovery action. Continue independent work within scope.
When the request includes a task and its prerequisites pass, start that task in the same session.
Record actual smoke or suite execution separately from prerequisite checks.
