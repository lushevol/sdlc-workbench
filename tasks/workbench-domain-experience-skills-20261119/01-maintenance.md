---
artifact_kind: maintenance
task_id: workbench-domain-experience-skills-20261119
received_at: "2026-11-19"
status: IN_PROGRESS
---

# Domain experience packaging skills

## User input

The user requested new skills that package successful task experience into reusable domain materials and scan past sessions to extract experience for later use. The target agent environments are Codex, Claude Code, and VS Code with Copilot.
The follow-up request makes a minimal end-to-end script, workflow, or instruction set the primary package output after a session retrospective. Session learning must use a bounded past duration, default to one week, skip unchanged sessions that were already scanned, and stop at explicit review and decision before packaging.

Exact inputs are retained in [user-input.md](evidence/user-input.md) and [user-input-20261119-followup.md](evidence/user-input-20261119-followup.md).

## Scope and risk

Update the canonical shared skills, packet contract, deterministic packet validation and history scanning helpers, review-only learning state, and focused coverage. Do not change runtime execution, client hook registrations, knowledge governance, or unrelated worktree files.

Risk is low for runtime behavior. The main risk is promoting secrets, stale configuration, synthetic data, or unsupported conclusions into reusable assets.

## Planned checks

- Validate both new skills with the skill creator checker.
- Run focused packet, history, and workspace layout tests.
- Run the applicable Python test suite and package checks when the focused checks pass.

## Current outcome

Implemented the two client-neutral skills, packet contract, history scanner, packet validator, index builder, project guidance, scaffold aliases, and focused tests. The follow-up now makes the primary recipe explicit, adds one-week session scanning with scan-state reuse, and stops learning at pending review.

Checks completed:

- Skill creator validation passed for both skills.
- Four focused packet and history tests passed.
- Workspace layout and packaging checks passed, including generated workspace and wheel coverage.
- `ai-sdlc --workspace . validate` passed with 119 documents and no findings.
- The full unit suite reached 1,115 tests. Thirty-nine pre-existing release-report integration cases could not bind localhost sockets in the sandbox. The failures are environment limits, not failures in the new skills.
- Wheel creation passed with `--no-build-isolation`. The default build-isolation attempt could not reach the configured package index in this sandbox.
- Eight focused packet and history tests pass, including duration filtering, invalid duration handling, unchanged-session skipping, changed-session re-scan, review-only output, and primary-recipe validation.

Remaining work is limited to the scoped commit and any later pilot packets created from real completed tasks.

## Documentation updated

- [Reusable domain experience](../../docs/EXPERIENCE_ASSETS.md)
- [Documentation map](../../docs/README.md)
- [Workspace design](../../docs/WORKSPACE_DESIGN.md)
- [Task evidence and promotion rules](../README.md)
