---
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
    - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Behavior skill adoption

## Scope and baseline

The user requested adoption of the parent behavior review procedures on 17 October 2026.
The source baseline is Workbench commit `718f685`.
The worktree contains an unrelated untracked `TODO` file.
This stage preserves that file.

The current consumer is an agent reviewing the session-renewal requirement.
The benefit is a repeatable evidence chain across intent, source, assertions, and retained results.
The existing pilot also contains a passing result with an outdated source hash.
That result supplies a concrete case for deterministic freshness checks.

## Affected scope and risk

Procedure changes affect five canonical skills under `.agents/skills/` and their shared references.
Runtime changes affect the CLI parser and a new evidence checking module under `core/`.
The existing CLI tests and MCP adapter call the CLI and shared runtime interfaces.
The new operations will not change configured tool grants or execute business commands.

Qualitative risk is moderate.
An incorrect evidence check could accept an outdated passing result.
Contract validity, source freshness, and business verification must remain separate.
The scoped implementation will not calculate a `VERIFIED` business verdict.

## Stage gates

| Stage | Required evidence |
| --- | --- |
| Baseline | Runtime tests, workspace validation, revision, and worktree state. |
| Procedures | Nine mapped procedures, resolved links, supported commands, and skill discovery. |
| Pilot | Exact intent, source, inspected assertions, retained runs, and explicit gaps. |
| Drift | A real earlier result exposes the changed Timeout source hash. |
| Deterministic support | Contract, freshness, immutable save, and comparison checks pass. |
| Distribution | Installed wheel initializes and operates outside this checkout. |

## Verification results

Workspace validation passed with 12 knowledge documents and no findings.
The sandboxed baseline ran 325 tests with one environment error.
The mock-registry test could not bind its local loopback socket.
The rerun with loopback access passed all 325 tests.
The [retained baseline log](../evidence/skill-adoption-baseline-tests.txt) records the command results.

## Evidence limits and next actions

The session-renewal requirement remains a candidate.
Its existing characterization uses controlled dependencies.
It does not establish browser, backend, identity-provider, or end-to-end behavior.
Human approval and full ASD review remain pending.

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| Candidate requirement and controlled execution | Business behavior remains unverified. | unknown | Review intent and run the supported integration scenarios. |
| Earlier passing result has changed source bytes | Reusing its pass can misstate current evidence. | unknown | Compare all executed source hashes with the selected revision. |
