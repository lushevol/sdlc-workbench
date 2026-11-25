# Requirement Grill skill adoption

> **No critical conclusions require user attention or action.**
> The adapted skill supports focused requirement clarification within existing Workbench procedures.
> Owner: Workbench maintainer. Next action: use the skill for material requirement ambiguity or incomplete acceptance criteria.

## Exact user input

Source: Codex chat `01a21369-b98a-7461-924f-603ef12f0e73`.
Date: 25 November 2026, Asia/Singapore.

> Check the skill in the release impact analysis directory called requirement-grill skill, and see if it is suitable for our project. If it is, add it to our skill library and adapt it for our project.

## Scope and authorization

Inspect the supplied skill and compare its responsibilities with existing Workbench procedures.
Adapt and add the skill when suitable, including discovery links and current documentation.
This request directly authorizes skill adoption and adaptation.
It does not request session learning, registry promotion, business publication, deployment, or external messages.
No extracted learning or global memory update is proposed.

## Repository state and risk

Workbench repository: `https://github.com/lushevol/sdlc-workbench.git`.
Branch: `feature/knowledge-layout-consolidation`.
Starting revision: `82d943adc`.
`git fetch --all` succeeded on 25 November 2026.
The checkout has zero incoming and zero unpublished commits against `origin/feature/knowledge-layout-consolidation`.

Unrelated changes affect the service graph viewer and `tasks/service-graph-viewer-20261125/`.
Preserve those changes and exclude them from this task's commit.

The parent repository is `https://github.com/lushevol/ratan-release-impact.git`.
Its current branch is `codex/mvp-setup`, at `b43f21001b6d696bdd48e0c1b041eea4025d7634`.
Its fetch succeeded, but its branch has no configured upstream or matching remote branch.
Against fetched `origin/main`, its current branch has eight additional commits and zero incoming commits.
Its worktree contains extensive existing changes, including historical Workbench paths.
Read the candidate only; do not change the parent checkout.

Consumers include requirement intake, impact analysis, skill discovery, packaging, and generated workspaces.
Qualitative risk: low to moderate.
Incorrect readiness rules could block authorized investigation or imply implementation authority.
Use existing Workbench phase rules and preserve bounded exploration.

## Suitability and adaptation

Source: [original skill at the inspected revision](https://github.com/lushevol/ratan-release-impact/blob/b43f21001b6d696bdd48e0c1b041eea4025d7634/.claude/skills/requirement-grill/SKILL.md).
Both source files match the parent checkout's `HEAD`.
Their original SHA-256 values and source identities are retained in [source review](evidence/source-review.json).
The original distinguishes missing criteria from ambiguous criteria.
It adds a completeness ledger, predicate tracing, and focused decision questions.
These details complement the existing [intake skill](../../.agents/skills/analyze-requirement/SKILL.md).

The [adapted skill](../../.agents/skills/requirement-grill/SKILL.md) uses registered knowledge retrieval and exact canonical sources.
It replaces hardcoded MCP names, ReBook examples, parent paths, and conflicting readiness labels.
Existing `READY`, `READY_WITH_LIMITS`, and `NEEDS_CLARIFICATION` decisions remain authoritative.
Completeness labels describe ledger rows. They add no runtime status, schema, or execution gate.
The skill reuses existing intake, current stage, canonical cases, and editable clarification documents.
It preserves unchanged predicates, bounded exploration, prior answers, and actual review states.

The original UI metadata required three named MCP servers.
The adapted metadata retains automatic discovery and requires no fixed tool connection.
The request introduces no runtime dependency, startup download, tenant value, or business policy.

## Integration and current documentation

Canonical owner: [requirement-grill](../../.agents/skills/requirement-grill/SKILL.md).
Claude discovery uses `.claude/skills/requirement-grill`, linked to the canonical directory.
The scaffold manifest declares the same alias for generated workspaces.
Existing shared-skill inventory tests now include `requirement-grill`.
No new runtime code or duplicate lifecycle implementation is needed.

Updated [agent guidance](../../AGENTS.md#requirement-and-issue-intake), [intake routing](../../.agents/skills/analyze-requirement/SKILL.md#start-intake-immediately), and [shared skills](../../README.md#shared-skills-and-agent-adapters).
Updated the [documentation map](../../docs/README.md#read-by-lifecycle) to make the refinement route discoverable.
The architecture, dependency, setup, and workspace-design contracts require no change for this instruction-only addition.
Concurrent graph work changes several of those files independently; those edits retain their existing ownership.

## Semantic review scope

The following checks are a manual walkthrough of the final instructions.
They are not independent agent trials, business tests, or execution evidence.

| Review case | Assessed disposition |
| --- | --- |
| A request adds one discriminator but omits its null behavior. | Keep the material missing rule unresolved; retain unchanged predicates with exact sources. |
| A draft states a complete criterion. | Mark completeness `EXPLICIT` while retaining its actual authority and review state. |
| An authorized experiment has unrelated unresolved product criteria. | Assess only uncertainties that can change the bounded experiment or its decision. |
| Tools or an index are unavailable. | Inspect exact available sources; disclose coverage limits without requiring fixed MCP servers. |
| An owner answer changes intended meaning. | Preserve the answer and reconcile candidate knowledge through existing governance before handoff. |

No independent behavioral evaluation or live business workflow was executed.
These limits do not prevent the directly authorized instruction-library update.

## Work, checks, and limits

The skill creator validator passed using the Workbench virtual environment.
The existing workspace layout suite passed all 24 tests.
These tests cover discovery, packaging, canonical aliases, initialization, and controlled directory-link denial.
Workspace validation passed with 119 documents and zero findings.
Local links, UI metadata, and the source-checkout alias passed [skill checks](evidence/skill-checks.json).

An isolated [candidate snapshot](evidence/candidate-snapshot.json) contains the baseline plus this task's library and integration changes.
It excludes concurrent graph viewer modifications.
Its wheel build passed without dependency downloads or build isolation.
The [installed-wheel probe](evidence/installed-wheel.json) passed outside the source checkout.
Two generated workspaces exercised directory links and controlled forwarding fallback.
Both could list and read the skill, match canonical bytes, resolve skill links, and pass workspace validation.
Generated workspaces omitted runtime source, runtime tests, and `pyproject.toml`.

The complete unit suite passed all 1,175 tests with optional local connector integrations enabled.
There were zero failures, errors, skips, expected failures, or unexpected successes.
The [verification receipt](evidence/verification.json) retains commands, candidate hashes, counts, and material limits.
Original outputs remain in [passing output](evidence/unit-suite-passed.txt.gz) and [sandbox failure output](evidence/unit-suite-sandbox.txt.gz).
The suite ran in the shared worktree with concurrent graph changes present.
The isolated wheel inputs still match every task-owned library and integration change.
The final staged diff passed whitespace checks and contains only this task's 17 files.
The staged review excludes all concurrent graph changes and routine logs.
Routine output remains under ignored `logs/validation/`.

### Meaningful failed checks and corrections

The generic Python lacked PyYAML for the skill validator.
Rerunning with the existing Workbench virtual environment passed without installation.
An additional metadata probe used the same generic Python and hit the same missing module.
Its virtual-environment replacement passed the YAML and alias checks.

The first focused test command selected the wrong test class and produced two loader errors.
Those methods belong to `WorkspaceLayoutTests`, not `WorkspacePackagingTests`.
The subsequent complete `test_workspace_layout.py` run passed all 24 actual tests.
No assertions or runtime code changed to obtain that result.

The sandboxed full suite ran 1,168 tests and returned 40 errors.
All 40 errors were `PermissionError` failures while binding local HTTP fixtures.
A test class could not initialize, so that attempt did not execute the complete inventory.
The same complete command was retried outside the sandbox with optional local connector integrations enabled.
The unrestricted retry passed all 1,175 tests without changing tests or assertions to accommodate the sandbox restriction.
The earlier class setup error prevented complete inventory execution.

The final fetch initially failed because the sandbox denied updating `.git/FETCH_HEAD`.
The escalated retry completed successfully.
The branch still has zero incoming commits against its fetched upstream before the task commit.

## Capability handoff and limits

Capability lookup used `learning list --query 'requirement clarification skill'` and returned no matching entries.
The existing intake, question resolution, retrieval, and phase-gate procedures supply the reusable owners.
This task directly adapts a supplied skill under explicit user authorization.
No session-extracted rule, registry promotion, experience packet, or global memory change is proposed.

Invoke `$requirement-grill` where the client supports skill invocation.
Alternatively, read it with `ai-sdlc --workspace PATH skills requirement-grill`.
Skill metadata and CLI discovery do not prove that every client has refreshed its skill list.
The forwarding probe does not establish native Windows execution.
No business knowledge, release assessment, live system, publication, deployment, or push is part of this change.

## Writing review

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not establish complete writing review.
```
