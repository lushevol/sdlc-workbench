---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
  - Native client execution and platform support require checks in the selected installation.
---

# Workbench hooks across agent clients

Workbench supplies shared session context and scoped completion checks for Codex, GitHub Copilot, and Claude Code.
The installed Python runtime owns the behavior. Client configuration translates native events into that shared behavior.
The existing [workflow skills](../.agents/skills/) retain semantic decisions and authorization boundaries.

## Install and inspect

Use an installed Workbench environment and an explicit workspace path.
Install only in a workspace whose hook configuration you intend to maintain.

```sh
ai-sdlc --workspace PATH hooks install
ai-sdlc --workspace PATH hooks status
```

Installation preserves unrelated hook entries and settings. Repeating installation updates only Workbench-owned entries.
The installed handlers select the current Python executable explicitly.
Reinstall after moving the virtual environment or selecting another interpreter.

**Claude Code requires the returned launch command with `--settings`. Bare `claude` does not load this isolated registration.**
The installer returns `launch_argv` for the Claude adapter.
For example, launch Claude Code with `claude --settings "/ABSOLUTE/WORKSPACE/.claude/workbench-hooks.json"`.
Use that workspace's absolute path. Ordinary `.claude/settings.json` and `.claude/settings.local.json` remain untouched.

To select one client, use `--client codex`, `--client copilot`, or `--client claude` with installation.
Support for all three clients shares the same runtime and check rules.
Installing configuration does not prove that a client trusted or executed its hooks.
`hooks status` checks registration ownership, workspace location, and the selected Python executable.
It does not launch clients or check native event delivery.

| Client surface | Native project configuration | Session context | Completion check |
| --- | --- | --- | --- |
| Codex | `.codex/hooks.json` | `SessionStart` | `Stop` |
| GitHub Copilot CLI | `.github/hooks/workbench.json` | `sessionStart` | `agentStop` |
| GitHub Copilot in VS Code, Copilot harness | Same Copilot format | `sessionStart` | `agentStop` |
| Claude Code | `.claude/workbench-hooks.json`, selected with `claude --settings ABSOLUTE_FILE` | `SessionStart` | `Stop` |

Codex requires review and trust for non-managed hooks. Review the installed entries through `/hooks` or desktop hook settings.
Claude Code applies its workspace trust and settings rules.
Copilot in VS Code requires the Copilot harness. Its hooks experience is preview.
The deprecated VS Code Local harness uses a separate schema.
Cloud environments require their own installed runtime and hook configuration.
Local installation does not establish cloud availability.

Copilot loads ordinary repository Claude settings, so Workbench stores its Claude registration in a separate explicit settings file.
Copilot does not discover that file through the documented ordinary Claude settings locations.
This keeps the installed Workbench handlers separate without disabling unrelated user hooks.

## Bind the active scope

Hooks do not guess a task from its filename, modification time, or dirty files.
Bind the exact living record and optional evidence inputs to the current client session.
Use the native session ID supplied by the client.
The start cue includes that ID and a bind command.
Bind before editing so the completion hook can compare the selected inputs with their starting bytes.

```sh
ai-sdlc --workspace PATH hooks bind --client codex --session SESSION --record tasks/TASK/01-intake.md
ai-sdlc --workspace PATH hooks bind --client copilot --session SESSION --record tasks/TASK/01-intake.md --index tasks/TASK/evidence/review-index.json
ai-sdlc --workspace PATH hooks bind --client claude --session SESSION --record tasks/TASK/01-intake.md --baseline relationships/requirement-code/baselines/BASELINE.json
```

Select a current stage record when intake is frozen.
Use workspace-relative paths for the selected record and evidence inputs.
An index must follow the existing [review index contract](REVIEW_INDEX.md).
A baseline must follow the existing [behavior review contract](BEHAVIOR_REVIEW.md).
Use `--artifact PATH` for supported SDLC artifact checks and `--case PATH` for relevant Gherkin cases.
Use repeated `--watch PATH` options for dependent source, test, or intent files whose changes must trigger checks.
These options select existing checks; they do not create or modify the selected files.
Dependency completeness is not inferred. Files outside the declared selection do not trigger scoped checks.

Bindings and disposable hook state stay under ignored `.workbench/hooks/` storage.
They are session pointers, rather than another authoritative workflow ledger.
Separate clients and sessions retain separate bindings.
Clear a binding when the session no longer owns that scope:

```sh
ai-sdlc --workspace PATH hooks clear --client codex --session SESSION
```

## Shared behavior and limits

The session hook supplies compact workspace and scope pointers.
It points to existing skills and living records instead of replaying every instruction.
Without an explicit binding, it supplies neutral navigation and skips task-specific validation.

After a watched change, the completion hook runs workspace validation and the explicitly selected deterministic checks.
Workspace validation has broader scope than the task. Its findings are labelled accordingly.
Do not attribute those broader findings to the selected task or user impact without separate evidence.
It reports advisory findings without continuing the agent automatically.
Unchanged inputs avoid repeated checks. Relevant source or configuration changes invalidate disposable results.
Read-only turns and unrelated drafts must not become inferred task work.
Successful checks are silent. The last compact result stays in the ignored session state.
An advisory finding includes the path to those details.

Hook results do not establish verified business behavior, publication approval, or release authorization.
The hooks do not publish knowledge, create governance events, compile the wiki, or run remote tools.
Required full unit tests remain part of deliberate delivery verification.
Hooks cannot replace immediate persistence of completed case evidence before further execution or waits.

## Disable or remove

Use the native client's hook controls to pause execution.
Remove Workbench-owned entries without deleting unrelated client configuration:

```sh
ai-sdlc --workspace PATH hooks uninstall
```

Use `--client CLIENT` to remove one client registration.
Inspect reported conflicts when a Workbench-owned entry has been changed independently.
Do not overwrite those changes by copying an example configuration over the settings file.

## Prerequisites and verification

Hooks reuse Python, the installed Workbench package, and existing validation dependencies.
They add no Python or npm package, background service, model credential, or runtime network endpoint.
The Codex Windows registration uses Windows PowerShell to launch the selected executable with safe path quoting.
Its standard `powershell.exe` prerequisite applies only on Windows.
Install the chosen agent client through its approved installation process.
The client must support the native events listed above and allow the installed hooks.
Keep the actual client version and enabled harness in execution evidence.
After installation, `ai-sdlc --workspace PATH doctor` checks configured client executables on `PATH` and the Windows PowerShell prerequisite where applicable.
Desktop-only installations can need separate executable verification. Doctor does not establish client trust or live event delivery.

Use the selected virtual environment's executable when `ai-sdlc` is absent from the shell path.
For example, use `.venv/bin/ai-sdlc` on macOS or `.venv\Scripts\ai-sdlc.exe` on Windows.
Installed handlers must retain correct executable and workspace paths, including spaces and Unicode.
See [setup](SETUP.md#workbench-hooks) and [dependency analysis](DEPENDENCIES.md#workbench-hooks).

Verify start-context delivery and completion checks in each selected client.
Include resumed sessions, missing scope, unchanged inputs, unrelated drafts, unavailable runtime, and validation failures.
Test all installed configurations together to detect inherited or duplicate registrations.
Use generated workspaces to check that the installed package works without the source checkout.
Native Windows execution, cloud execution, and installed client compatibility require their own retained results.
Payload tests and configuration validation alone cannot establish live client execution.

## Acceptance criteria

These criteria define hook behavior. Native-client execution remains separate from deterministic adapter and package tests.

### AC-HOOK-CONTEXT

```gherkin
Feature: Shared Workbench hooks

  @AC-HOOK-CONTEXT
Scenario Outline: Restore the explicitly selected scope
  Given the <client> session has an explicit binding to one existing living record
  When its native session-start hook runs
  Then its supported context output identifies that record and the next applicable check
  And the hook does not infer another task from filenames or modification times

  Examples:
    | client |
    | codex |
    | copilot |
    | claude |
```

### AC-HOOK-SCOPE

```gherkin
Feature: Shared Workbench hooks

  @AC-HOOK-SCOPE
Scenario: Skip task checks without an active binding
  Given the selected client session has no scope binding
  And unrelated draft files exist in the workspace
  When its completion hook runs
  Then zero task-specific validators run
  And no task, knowledge record, audit event, or wiki page changes
```

### AC-HOOK-ISOLATION

```gherkin
Feature: Shared Workbench hooks

  @AC-HOOK-ISOLATION
Scenario: Isolate all three clients with the same native session string
  Given Codex, Copilot, and Claude use the same session string in one workspace
  And each client is bound to a different living record
  And Claude uses the returned isolated settings file
  When each native start hook runs
  Then each client receives only its own selected record
  And Copilot does not execute the isolated Claude Workbench registration
```

### AC-HOOK-INSTALLATION

```gherkin
Feature: Shared Workbench hooks

  @AC-HOOK-INSTALLATION
Scenario: Preserve unrelated client configuration
  Given all native settings contain unrelated user values and hook handlers
  When Workbench hooks are installed twice and then uninstalled
  Then the second installation adds zero duplicate Workbench handlers
  And all unrelated values and handlers remain
  And ordinary Claude settings remain byte-identical
```

### AC-HOOK-FRESHNESS

```gherkin
Feature: Shared Workbench hooks

  @AC-HOOK-FRESHNESS
Scenario: Recheck changed evidence inputs
  Given the selected scope has a retained deterministic validation result
  When a filesystem write changes a bound record or an explicitly watched dependency
  Then the next completion check does not reuse the stale result
  And its reported findings identify the current selected inputs
```

### AC-HOOK-ADVISORY

```gherkin
Feature: Shared Workbench hooks

  @AC-HOOK-ADVISORY
Scenario: Report a bounded check failure without changing business state
  Given the selected validator fails or exceeds its execution limit
  When the completion hook returns
  Then the result reports the failure or timeout
  And it requests zero automatic continuation turns
  And it changes zero application, task, knowledge, audit, receipt, or wiki files
```

### AC-HOOK-PACKAGE

```gherkin
Feature: Shared Workbench hooks

  @AC-HOOK-PACKAGE
Scenario: Use the installed runtime from a generated workspace
  Given Workbench is installed from its wheel outside the source checkout
  And the generated workspace has no copied Python runtime source
  When hook registrations are installed and exercised with native payloads
  Then every supported client registration invokes the installed package
  And zero copied Python runtime modules appear in the generated workspace
```

## Native references

- [Codex hooks](https://learn.chatgpt.com/docs/hooks)
- [GitHub Copilot hooks](https://docs.github.com/en/copilot/reference/hooks-configuration)
- [Copilot harness hooks in VS Code](https://code.visualstudio.com/docs/copilot/customization/hooks)
- [Claude Code hooks](https://code.claude.com/docs/en/hooks)

These references describe native capability. Project verification must identify the versions and environments actually tested.
