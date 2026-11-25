# Configurable automatic commits

> **Critical conclusions: Implemented and checked**
>
> **Automatic commits are now a workspace setting.**
> Owner: Workbench maintainer. Next action: use `settings.auto_commit_staged_changes` at stage completion.
> Evidence: [Configuration guide](../../README.md#configure-automatic-commits) and [verification](evidence/verification.json).

## Exact user input

Source: Codex chat `01a2118d-d014-74f2-ab0c-70913e950bd6`.
Date: 25 November 2026, Asia/Singapore.

> Create a workbench config that includes an option for whether to always automatically commit staged changes. I mentioned this rule in agent.md, but I'd like it to be configurable. Can you provide other configurable suggestions?

## Scope and authorization

Implement configurable automatic commits in the existing Workbench configuration.
Keep the current default unless source inspection requires another choice.
Suggest other useful settings without implementing them.
This request authorizes configuration, runtime, tests, and applicable guide changes.
It is direct maintenance, not extracted session learning.

## Source and risk

Repository: `https://github.com/lushevol/sdlc-workbench.git`.
Branch: `feature/knowledge-layout-consolidation`.
Starting revision: `800e28395`.
Fetched comparison: `origin/feature/knowledge-layout-consolidation`, at `b3df0435d`.
The checkout has four unpublished commits and no incoming commits.
The initial worktree is clean.

The sandbox blocked the first fetch; the approved retry completed successfully.

Consumers include workspace loading, initialization, status output, native hooks, validation, packaging, and agent instructions.
Qualitative risk: moderate.
Incorrect defaults could change existing commit behavior.
Unrelated staged changes must retain their ownership.

## Work and checks

The workspace schema now accepts `settings.auto_commit_staged_changes`.
The effective default is `true` for new and older YAML or JSON declarations.
Workspace status reports the effective setting.
Session-start hooks report it for Codex, Copilot, and Claude.
The agent guide commits reviewed task-owned staged changes only when the setting is `true`.
The runtime and hooks do not execute Git commits.

Invalid types and unknown setting names fail closed.
The workspace declaration sets the current repository to `true`.

The focused suite passed 64 tests.
Full discovery ran 1,171 tests: 1,169 passed and two optional tests were skipped.
The optional Node integration suite then passed both skipped tests.
Every discovered test passed across these executions, with no unresolved skips or failures.
Workspace validation passed with 119 documents and zero findings.
The wheel build passed.

The wheel smoke test passed outside the source checkout.
It checked seven shipped files, both policy values, all three client contexts, invalid input rejection, and runtime-source omission.
`git diff --check` passed.

Selected results are in [verification](evidence/verification.json), [unit output](evidence/unit-suite.txt.gz), and [optional integration output](evidence/optional-node-integration.txt).
The installed-wheel results are in [wheel verification](evidence/wheel-smoke.json).
Routine command output remains in ignored `logs/validation-20261125/`.

### Corrected check assumptions

The initial focused run had three failing subtests in one new test.
It expected a field-specific diagnostic from a loader that intentionally returns a sanitized workspace error.
The assertion now checks that existing error contract and still rejects an automatic-commit cue.
Runtime validation did not change to accommodate the test.

The initial standalone wheel probe compared a resolved package path with an unresolved temporary path.
macOS `/var` and `/private/var` aliases caused that probe assertion to fail.
Resolving both paths fixed the probe. The installed package already came from the wheel.
The passing probe also uses the existing requirement schema filename.
These probe errors did not require product changes.

## Suggested future settings

These are proposals only.
They need a separate user decision and implementation scope.

| Setting | Purpose | Suggested default |
| --- | --- | --- |
| `commit_message_style` | Choose plain or Conventional Commit messages. | `plain` |
| `commit_granularity` | Commit after each completed stage or once per completed task. | `per_stage` |
| `branch_prefix` | Supply the default prefix when branch creation is authorized. | `feature/` |
| `ponytail_mode` | Choose the existing `lite`, `full`, or `ultra` implementation style. | `full` |
| `report_verbosity` | Choose concise, standard, or detailed reports. | `standard` |

Commit message style and granularity are the closest useful additions to this request.
Required checks, staged review, unrelated-file preservation, and external authorization remain mandatory.
Do not add these proposed keys to the current declaration; unknown settings fail validation.

## Documentation and capability handoff

Updated [agent instructions](../../AGENTS.md#validation-and-commits) to read the setting before stage completion.
Updated the [configuration guide](../../README.md#configure-automatic-commits), [workspace design](../../docs/WORKSPACE_DESIGN.md#independent-system-workspaces), and [hook guide](../../docs/HOOKS.md#shared-behavior-and-limits).
No dependencies, business records, canonical governance, or repository grants changed.
Registry lookup found no applicable commit-configuration capability.
This directly requested feature needs no extracted-learning promotion.

## Limits and disposition

This is agent policy exposed through status, instructions, and hook context.
Tests do not establish that every agent always follows the policy.
No live native client or Windows execution was added to the controlled adapter checks.
The default remains `true`; this task follows the current scoped automatic-commit instruction.
No push is authorized by the new setting.

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
