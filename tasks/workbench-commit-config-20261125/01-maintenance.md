# Configurable agent workflow defaults

> **Critical conclusions: All requested settings implemented and checked**
>
> **All five confirmed additions preserve current behavior through explicit defaults.**
> Owner: Workbench maintainer. Next action: read effective settings before branch creation and stage or task completion.
> Evidence: [Follow-up request](#exact-user-input), [configuration guide](../../README.md#configure-agent-settings), and [verification](evidence/additional-settings/verification.json).

## Exact user input

Source: Codex chat `01a2118d-d014-74f2-ab0c-70913e950bd6`.
Date: 25 November 2026, Asia/Singapore.

> Create a workbench config that includes an option for whether to always automatically commit staged changes. I mentioned this rule in agent.md, but I'd like it to be configurable. Can you provide other configurable suggestions?

Follow-up source: the same Codex chat, 25 November 2026, Asia/Singapore.

> yes add these configs, use current value as default.

The follow-up authorizes the five previously proposed settings and their applicable guides, consumers, and tests.
The follow-up implementation starts from commit `c6475b148`.
The refreshed checkout has five unpublished commits, no incoming commits, and no unrelated local changes.

## Scope and authorization

Implement all six settings in the existing Workbench configuration.
The follow-up authorizes the five earlier suggestions.
Keep current behavior as each default.
This request authorizes configuration, runtime, tests, and applicable guide changes.
It is direct maintenance, not extracted session learning.

The follow-up extends implementation to all five proposed settings.
Defaults preserve free-form commit subjects, stage commits, `feature/` branch names, `full` Ponytail mode, and standard report detail.
The schema is the single owner for omitted-field and initialization defaults.

## Source and risk

Repository: `https://github.com/lushevol/sdlc-workbench.git`.
Branch: `feature/knowledge-layout-consolidation`.
Starting revision: `800e28395`.
Fetched comparison: `origin/feature/knowledge-layout-consolidation`, at `b3df0435d`.
The original stage starts with four unpublished commits and no incoming commits.
Both stage-entry worktrees are clean.

The sandbox blocked the first fetch; the approved retry completed successfully.

Consumers include workspace loading, initialization, status output, native hooks, validation, packaging, and agent instructions.
Qualitative risk: moderate.
Incorrect defaults could change existing commit behavior.
Unrelated staged changes must retain their ownership.

## Initial automatic-commit change and checks

Commit `c6475b148` completed this initial scope.
The following results retain their original execution scope.

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

## Confirmed additional settings

The [follow-up request](#exact-user-input) confirms all five earlier proposals.
The following defaults preserve current instructions and behavior.

| Setting | Purpose | Default |
| --- | --- | --- |
| `commit_message_style` | Choose plain or Conventional Commit messages. | `plain` |
| `commit_granularity` | Commit after each completed stage or once per completed task. | `per_stage` |
| `branch_prefix` | Supply the default prefix when branch creation is authorized. | `feature/` |
| `ponytail_mode` | Choose `lite`, `full`, `ultra`, or `"off"` implementation style. | `full` |
| `report_verbosity` | Choose concise, standard, or detailed reports. | `standard` |

Existing commit subjects have no fixed format requirement; `plain` preserves that freedom.
The existing stage-completion rule supplies `per_stage`.
Current branch guidance supplies `feature/`.
Project instructions supply Ponytail `full`; `standard` preserves the current reporting detail.
Required checks, staged review, unrelated-file preservation, and external authorization remain mandatory.

### Implementation and current checks

Schema defaults now supply both initialization and omitted fields during loading.
Older configurations can contain no settings, an empty object, or only selected overrides.
Workspace status and all three native session contexts expose all six effective values.
The context distinguishes stage commits, task commits, and disabled automatic commits.
Agent instructions define each setting and retain explicit user precedence.

Ponytail mode uses the project guide; upstream skill bytes and attribution remain unchanged.
Quote `"off"` in YAML because the existing YAML reader interprets unquoted `off` as a boolean.
Branch creation still requires authorization and a valid complete Git branch name.
No new dependencies or automatic branch operations were added.

The focused suite passed 66 tests.
Full discovery passed 1,173 tests with optional local integrations enabled.
There were no skips, expected failures, unexpected successes, or runner errors.
Workspace validation passed with 119 documents and zero findings.
The wheel build passed without new dependencies or downloads.

The isolated installed-wheel probe passed 30 native-context cases across YAML, JSON, and all three clients.
It checked eight shipped files, defaults, partial overrides, invalid settings, and omitted runtime source.
The probe also verified unchanged upstream Ponytail bytes.
Final Markdown link and staged-diff checks are recorded in [verification](evidence/additional-settings/verification.json).

Selected results include [unit output](evidence/additional-settings/unit-suite.txt.gz) and [wheel verification](evidence/additional-settings/wheel-smoke.json).
Routine output remains under ignored `logs/additional-settings-20261125/`.

## Documentation and capability handoff

Updated [agent instructions](../../AGENTS.md#validation-and-commits) to read the setting before stage completion.
Updated the [configuration guide](../../README.md#configure-agent-settings), [workspace design](../../docs/WORKSPACE_DESIGN.md#independent-system-workspaces), and [hook guide](../../docs/HOOKS.md#shared-behavior-and-limits).
The [setup guide](../../docs/SETUP.md#ponytail-coding-skill) now describes the configured Ponytail mode.
No dependencies, business records, canonical governance, or repository grants changed.
Registry lookup found no applicable commit-configuration capability.
This directly requested feature needs no extracted-learning promotion.

The latest request explicitly confirms the five earlier configuration candidates.
No separate learning asset, registry promotion, or global memory update is required.

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
