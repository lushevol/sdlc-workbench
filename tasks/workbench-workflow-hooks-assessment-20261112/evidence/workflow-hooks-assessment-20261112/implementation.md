---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
  - Native client delivery, Windows execution, and cloud execution remain unverified.
---

# Shared hook implementation

The shared runtime now supplies session context and advisory completion checks for Codex, Copilot, and Claude Code.
The [three-client requirement](cross-client-requirement.md#exact-user-input) and [implementation authorization](implementation-request.md#exact-user-input) govern this change.
The [portable-path clarification](portability-request.md#exact-user-input) supersedes machine-specific hook registration and guidance.
Use the [hook guide](../../HOOKS.md) for installation, scope binding, trust requirements, and removal.

**Claude requires the isolated `--settings` launch. Codex requires client trust. Native event delivery remains unverified.**
Copilot reads ordinary Claude settings. The isolated Claude file prevents the documented inherited registration path.
The installed Copilot executable is unavailable here. The same restriction applies to the VS Code CLI.

## Scope and risk

The installed runtime owns all behavior. Generated workspaces receive guides and local registrations without copied Python runtime modules.
Bindings select one client, native session, living record, and optional dependent files.
Hooks do not discover task ownership from dirty files.
Registrations invoke the installed `ai-sdlc` command through the client's `PATH`.
Hooks discover the nearest declared workspace above the native working directory.
Context cues, new installation state, and saved diagnostic paths use portable relative locators.
Claude launches from the workspace root with `claude --settings .claude/workbench-hooks.json`.

Completion checks reuse existing workspace, artifact, Gherkin, review-index, and behavior-baseline validators.
The input fingerprint covers declared files, workspace configuration, declared catalogs, and the validation recipe.
Unbound and unchanged inputs skip validation. Failed deterministic results remain available without repeated warnings.
Timeouts and changes during validation remain retryable.

Installation writes local client settings. This has moderate configuration risk.
Ownership checks, preflight validation, atomic replacement, rollback, and uninstall preserve unrelated settings.
Reinstallation migrates exact legacy registrations without retaining their machine-specific bindings.
The destination needs its own installed command on `PATH`. Copying a virtual environment is outside the portability contract.
Session state uses ignored storage and client-specific locks.
Native payloads, selected paths, and file reads have explicit bounds.
The hooks request no continuation and run no semantic governance, publication, model, or remote operation.

## Verification

The [portability receipt](portability-verification.json) binds current source hashes, commands, checks, and remaining limits.
The [portable installed-wheel receipt](portable-installed-smoke.json) checks copied and moved workspaces outside the source checkout.
These checks use native-shaped payloads. They do not establish native client dispatch.
All 1,038 current tests passed, including Node connector integration. No tests failed, errored, or skipped.
All 54 focused hook tests passed. The external wheel check confirms portable registered commands after copying and moving workspaces.

The original [verification receipt](verification.json) and [installed-wheel receipt](installed-smoke.json) preserve the initial implementation evidence.
That baseline passed 1,027 tests, including Node connector integration, and 43 focused hook tests.
Those historical receipts retain their original environment bindings. They do not configure reusable workspaces.
The packaging check builds an sdist, builds its wheel, and initializes an external workspace.

The first suite failed because the sandbox denied localhost sockets and the sdist omitted two new guide files.
The manifest now includes those guides. The final suite runs with localhost access.
All three local registrations now use the portable command format.
The clients must inherit an environment containing the installed `ai-sdlc` command.
The current agent environment lacks `ai-sdlc` and Copilot on `PATH`. Configuration readiness does not remove those prerequisites.
General-guide artifact lint is inapplicable because this guide has no business artifact schema.
Gherkin checking reports `UNVERIFIED`, with zero `FAIL` findings. Its evidence manifest and semantic reviews remain absent.
Passing unit assertions remain separate from that status and native execution.

## AC to code changes

The eight [canonical criteria](../../HOOKS.md#acceptance-criteria) define this harness behavior.
All eight have implementation links. These links do not establish complete native conformance.

| Criterion | Changed implementation | Evidence limit |
| --- | --- | --- |
| [AC-HOOK-CONTEXT](../../HOOKS.md#ac-hook-context) | [hooks.py](../../../core/hooks.py): `run_hook`, `_native`; [cli.py](../../../core/cli.py): native dispatch | Client delivery requires live confirmation. |
| [AC-HOOK-SCOPE](../../HOOKS.md#ac-hook-scope) | [hooks.py](../../../core/hooks.py): `bind_scope`, `run_hook`, `_checks` | Dependency selection remains explicit. |
| [AC-HOOK-ISOLATION](../../HOOKS.md#ac-hook-isolation) | [hooks.py](../../../core/hooks.py): `_identity`, `_state_path`; [hook_install.py](../../../core/hook_install.py): `CONFIGS`, `_registrations` | Inherited host behavior remains untested. |
| [AC-HOOK-INSTALLATION](../../HOOKS.md#ac-hook-installation) | [hook_install.py](../../../core/hook_install.py): `install_hooks`, `remove_hooks`, `_transaction` | Native trust remains outside installation. |
| [AC-HOOK-FRESHNESS](../../HOOKS.md#ac-hook-freshness) | [hooks.py](../../../core/hooks.py): `_fingerprint`, `run_hook` | Undeclared indirect dependencies require `--watch`. |
| [AC-HOOK-ADVISORY](../../HOOKS.md#ac-hook-advisory) | [hooks.py](../../../core/hooks.py): `_run_checks`, `advisory`; [cli.py](../../../core/cli.py): bounded input | Native warning presentation remains untested. |
| [AC-HOOK-PACKAGE](../../HOOKS.md#ac-hook-package) | [scaffold.json](../../../scaffold.json), [MANIFEST.in](../../../MANIFEST.in), installed runtime modules | Windows and cloud execution remain untested. |
| [AC-HOOK-PORTABILITY](../../HOOKS.md#ac-hook-portability) | [hooks.py](../../../core/hooks.py): `discover_workspace`, relative cues and diagnostics; [hook_install.py](../../../core/hook_install.py): portable registrations and legacy migration | Destination runtime availability remains required. |

## AC to test assertions

Eight of eight criteria have direct assertion links. Native integration coverage remains zero of three clients.
The isolation criterion has partial contract evidence until the clients execute their hooks together.

| Criterion | Inspected assertion chain | Retained execution |
| --- | --- | --- |
| [AC-HOOK-CONTEXT](../../HOOKS.md#ac-hook-context) | [Runtime tests](../../../tests/test_hooks.py): `test_public_cli_returns_one_native_context_object_for_each_client`, `test_start_returns_native_context_without_reading_document_content` | [Unit receipt](portability-verification.json), [installed smoke](portable-installed-smoke.json) |
| [AC-HOOK-SCOPE](../../HOOKS.md#ac-hook-scope) | [Runtime tests](../../../tests/test_hooks.py): `test_unbound_stop_does_not_scan_or_create_state`, `test_only_explicitly_selected_artifact_and_evidence_checks_run` | [Unit receipt](portability-verification.json) |
| [AC-HOOK-ISOLATION](../../HOOKS.md#ac-hook-isolation) | [Runtime tests](../../../tests/test_hooks.py): `test_same_native_session_id_remains_separate_between_clients`; [installer tests](../../../tests/test_hook_install.py): `test_installation_is_idempotent_and_claude_does_not_cross_load` | [Unit receipt](portability-verification.json), [installed smoke](portable-installed-smoke.json); native inheritance unverified |
| [AC-HOOK-INSTALLATION](../../HOOKS.md#ac-hook-installation) | [Installer tests](../../../tests/test_hook_install.py): idempotence, unrelated settings, collision refusal, partial removal, rollback, concurrent edits | [Unit receipt](portability-verification.json), [installed smoke](portable-installed-smoke.json) |
| [AC-HOOK-FRESHNESS](../../HOOKS.md#ac-hook-freshness) | [Runtime tests](../../../tests/test_hooks.py): changed watched files, workspace configuration, and changes during validation | [Unit receipt](portability-verification.json) |
| [AC-HOOK-ADVISORY](../../HOOKS.md#ac-hook-advisory) | [Runtime tests](../../../tests/test_hooks.py): failures, timeout, malformed input, byte limits, option-shaped paths, snapshot equality | [Unit receipt](portability-verification.json), [installed smoke](portable-installed-smoke.json) |
| [AC-HOOK-PACKAGE](../../HOOKS.md#ac-hook-package) | [Packaging test](../../../tests/test_workspace_layout.py): `test_complete_llm_wiki_source_survives_sdist_wheel_and_initialization`; external registered-command assertions | [Unit receipt](portability-verification.json), [installed smoke](portable-installed-smoke.json) |
| [AC-HOOK-PORTABILITY](../../HOOKS.md#ac-hook-portability) | [Runtime tests](../../../tests/test_hooks.py): nearest workspace, relocation, relative bind command, relative diagnostics; [installer tests](../../../tests/test_hook_install.py): copy-safe state, legacy migration, unchanged relocated commands | [Current receipt](portability-verification.json), [portable installed smoke](portable-installed-smoke.json) |

## Code changes to test assertions

All five functional change groups have direct tests. Documentation and ignore rules support these groups.
Test-only changes add assertion coverage. No business implementation or intended domain behavior changes.

| Change group | Direct checks | Coverage limit |
| --- | --- | --- |
| Shared hook runtime | [Runtime tests](../../../tests/test_hooks.py): native outputs, workspace discovery, relative diagnostics, scope, freshness, locks, bounds, retry, and file hashes | Live client callbacks untested. |
| Safe native installer | [Installer tests](../../../tests/test_hook_install.py): portable state, migration, ownership, rollback, collision, removal, and actual POSIX command execution | Native Windows execution untested. |
| Public CLI | [Runtime tests](../../../tests/test_hooks.py): subprocess invocation for all clients, implicit native workspace discovery, and malformed input | Model sessions not launched. |
| Optional readiness diagnosis | [Doctor tests](../../../tests/test_hook_doctor.py): absent, corrupt, missing runtime, and missing client states | Readiness does not establish native delivery. |
| Workspace and distribution integration | [Packaging test](../../../tests/test_workspace_layout.py), [installed smoke](portable-installed-smoke.json), scaffold path checks | Cloud installation untested. |

## Remaining verification

Installed inventory reports Codex `0.167.1` and Claude Code `2.1.310`.
No paid model session was launched. Native event dispatch, resume behavior, and warning presentation need client execution evidence.
Windows and cloud need their own installed-environment checks.
These limits do not establish defects. They prevent a claim of complete three-client experience verification.
