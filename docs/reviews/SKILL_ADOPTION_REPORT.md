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

## Procedure adoption

Five existing skills now share the [behavior review handoff](../../.agents/skills/verify-implementation/references/behavior-review.md).
The handoff assigns all nine parent procedures to existing Workbench skills.
It retains atomic behaviors, evidence grades, exact revisions, assertion chains, gap categories, and declared coverage denominators.
It defines on-demand incremental checks and preserves earlier evidence records.

Five skill frontmatter checks passed.
All 24 selected relative links and anchors resolved.
The installed CLI discovered the revised verification procedure.
An independent pilot agent followed the handoff and exposed additional evidence limits.

## Real pilot and drift check

The [traceability record](SESSION_RENEWAL_BEHAVIOR_TRACE.md) covers requirement criteria AC-5 through AC-7.
All three selected behaviors have inspected implementation and controlled assertion mappings.
Their required browser/backend verification remains missing.
Saved Jest assertions have no retained Jest execution.

Thirteen [offline byte checks](../evidence/skill-adoption/pilot-offline-checks.json) passed.
All five executed source hashes match commit `4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8`.
The [historical comparison](../evidence/skill-adoption/pilot-drift-checks.json) finds one stale Timeout hash.
Both retained original result files remain unchanged.

The [traceability lint](../evidence/skill-adoption/traceability-lint.json) passed with four disclosed warnings.
Unknown ownership, pending review, unresolved evidence, and pending writing review remain visible.
The independent [handoff exercise](../evidence/skill-adoption/handoff-usability.json) found the procedure usable.

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| Pending and success fixtures omit refresh credentials | Those checks do not establish every required precondition. | unknown | Add and execute suitable integration fixtures in the owning repository. |
| Original result omits harness hash and command arguments | Later declarations cannot establish original test-byte bindings. | unknown | Retain original harness, configuration, and input hashes in future runs. |

## Deterministic evidence support

The installed `assurance` CLI now validates, saves, reports, and compares behavior evidence baselines.
The [guide](../BEHAVIOR_REVIEW.md) defines its narrow schema and supported commands.
The runtime checks retained file bytes, record hashes, exact Git sources, references, and complete execution-source inventories.
It separates contract validity from freshness and keeps business verification at `NOT_VERIFIED`.

The [current baseline](../../relationships/requirement-code/baselines/PILOT-session-renewal-current-20261017.json) is `VALID` and `CURRENT`.
The [historical baseline](../../relationships/requirement-code/baselines/PILOT-session-renewal-historical-20261017.json) is `VALID` and `STALE`.
Strict freshness validation accepts the current baseline and rejects the historical baseline.
The [comparison](../evidence/skill-adoption/baseline-comparison.json) identifies all three affected behaviors.
These baselines hold current behavior constant and compare retained run evidence.
Their counts do not establish historical assurance improvement.

All 39 new API and CLI checks passed.
They cover stale results, malformed inputs, incomplete inventories, missing source, immutable saves, and dependent records.
They also cover path confinement, record versions, access-time changes, and real byte changes during inspection.
The complete runtime suite passed all 364 tests.
The [runtime log](../evidence/skill-adoption/runtime-tests.txt) retains that result.
Workspace validation remained `VALID` with 12 knowledge documents and no findings.

The runtime adds no approval engine, native result importer, or automatic scheduler.
Existing governed records and audit history remain unchanged.

## Standalone distribution

The [wheel build](../evidence/skill-adoption/wheel-build.txt) passed with installed build dependencies and no network dependency installation.
The build used `--no-build-isolation` to reuse those dependencies.
The wheel was installed into a fresh environment outside this checkout.
Available third-party libraries were copied into that environment without editable project paths.

An independent agent ran 27 [installed-wheel checks](../evidence/skill-adoption/wheel-check.json) from outside the source checkout.
All checks passed.
The imported runtime came from the installed distribution.
The generated workspace retained canonical skills, aliases, references, guidance, and the installed schema command.
It contained no core runtime source, build source, runtime tests, or live knowledge records.
Its [workspace validation](../evidence/skill-adoption/generated-workspace-validation.json) passed with empty catalogs and provenance.

Installed CLI checks covered strict freshness, immutable saves, reports, and transitive baseline comparison.
Synthetic fixture results tested interfaces and did not establish business execution.
The source workspace remains valid, and the unrelated `TODO` file remains unchanged.

## Evidence limits and next actions

The session-renewal requirement remains a candidate.
Its existing characterization uses controlled dependencies.
It does not establish browser, backend, identity-provider, or end-to-end behavior.
Human approval and full ASD review remain pending.

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| Candidate requirement and controlled execution | Business behavior remains unverified. | unknown | Review intent and run the supported integration scenarios. |
| Earlier passing result has changed source bytes | Reusing its pass can misstate current evidence. | unknown | Compare all executed source hashes with the selected revision. |
