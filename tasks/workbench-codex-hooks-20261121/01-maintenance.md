---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not establish native Codex dispatch or client trust.
  - Windows execution remains unverified.
---

# Repair Codex session hooks

## Request and scope

Date: 21 November 2026 (Asia/Singapore).
Work type: Workbench harness maintenance.
Owner: agent:codex; human maintenance owner is not recorded.
Baseline: `981651727a202de9b168fa988ac7dccc88b09de0`.

Exact user input:

> Looks like looks like the hooks of this project failed in codex session. Please fix them, both session start and session and off field.

Repair the project Codex hook registration and shared adapter. Preserve unrelated worktree changes, client settings, and business records.

## Diagnosis

The registered commands used bare `ai-sdlc`, while this Codex process did not inherit the project virtual environment on `PATH`. Both native commands exited 127 before the Workbench runtime started.

The registration used Codex `Stop` for session completion. The current Codex contract uses `SessionEnd` for the main session lifecycle. `SessionEnd` accepts the session payload and has a maximum three-second handler timeout.

## Changes

- Map Codex completion to `SessionEnd` and retain `Stop` for Claude Code.
- Bound Codex session-end checks to two seconds, within the native timeout.
- Let Codex registrations find `.venv/bin/ai-sdlc` in the native working directory or its ancestors before falling back to `PATH`.
- Migrate the existing schema-2 Codex `Stop` registration without losing ownership or unrelated hooks.
- Refresh the local ignored Codex registration and installation state.
- Update current hook, dependency, setup, and Codex adapter guidance.

## Checks and outcome

- `PYTHONPATH=core .venv/bin/python -m unittest tests.test_hooks tests.test_hook_install -q` passed 50 tests.
- `PYTHONPATH=core .venv/bin/python -m unittest discover -s tests -q` passed 1,131 tests with two optional skips.
- `.venv/bin/python -m pip wheel . --no-deps --no-build-isolation --wheel-dir dist` built the package wheel successfully.
- `.venv/bin/ai-sdlc --workspace . validate` returned `VALID` with zero findings across 119 documents.
- The Codex registration probe passed from a nested directory with `PATH` excluding the project environment.
- Both refreshed native commands were exercised with `SessionStart` and `SessionEnd` payloads. They returned JSON and exit code zero for an unbound session.
- `.venv/bin/ai-sdlc --workspace . hooks status` returned `READY` for all three configured clients.

The tests and probes establish local adapter behavior. They do not prove the installed Codex client dispatched the events or accepted the hook trust prompt.

## Current documentation

Updated [hooks](../../docs/HOOKS.md), [dependencies](../../docs/DEPENDENCIES.md), [setup](../../docs/SETUP.md), and the [Codex adapter guide](../../adapters/codex/README.md).

OpenAI hook event reference: [Codex hooks](https://learn.chatgpt.com/docs/hooks).
