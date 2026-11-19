---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not establish complete writing review.
---

# Workbench Ready skill

**No critical conclusions require user attention or action.**

## Exact user input

- 19 November 2026, this Codex chat:

  > do you suggest I extend the skill to be "workbench ready" which also includs all initial set up works so that users can start their works directly ?

- 19 November 2026, the user's response to the proposed skill and Portal review pilot:

  > yes go on

## Scope

Add a shared skill for initial setup, repository preparation, and readiness for the first requested task.
Pilot a Portal cross-repository source review in a fresh workspace.
Reuse the current installer, repository onboarding, dependency graph, and test preflight.

## Affected interfaces and risk

The base revision is `1ecd0d794`. The skill adds workspace guidance and a packaged skill alias.
Existing source review and test operations retain their current interfaces.
Pre-existing local changes affect the connector lockfile and release report tree.
Runtime compatibility risk is low. Setup routing risk is moderate across platforms.

## Current outcome

The [skill](../../.agents/skills/workbench-ready/SKILL.md) prepares the workspace and starts the first requested task when its prerequisites pass.
It reuses setup tools, repository onboarding, graph queries, and runner preflight.
The [setup guide](../../docs/SETUP.md#start-setup) and [README](../../README.md#adopt-an-existing-project) document the entry point.
The [architecture](../../ARCHITECTURE.md#skills-and-adapters) and [workspace design](../../docs/WORKSPACE_DESIGN.md#adoption-sequence) document its responsibilities.

## Verification

- The skill validator, workspace validation, and added guide links passed.
- The full unit suite ran 1,122 tests with two skips. The loopback-enabled run passed.
- A fresh workspace installed from the final wheel exposed the canonical skill and Claude alias.
- Core doctor, workspace validation, and a direct graph query passed in check-only use. No workspace files were added by those checks.
- An independent agent completed the Portal review from a fresh workspace. An unchanged rerun reused the graph manifest. [Pilot evidence](evidence/portal-pilot.json)

## Pilot finding and limits

The pilot reviewed the effect of removing the `data` field from the BFF import-map response.
Both the Import Map page and Tile editor read the field and fall back to an empty array.
The graph found the candidate call sites. Direct source inspection established their use of the field. [Pilot evidence](evidence/portal-pilot.json)

The pilot used clean local checkouts, macOS arm64, and an existing Python environment.
Graph coverage was partial for both repositories. The deployed gateway binding remains unknown.
Launcher behavior on a new machine, Windows, browser execution, and live integrations remain untested.
