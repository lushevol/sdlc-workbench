---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
status: draft
owner: unknown
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
  - Local configuration checks do not establish UAT1 access or business behavior.
---

# UAT1 session renewal execution plan

The user selected UAT1.
The scoped execution proposal is ready for setup review.
No UAT1 business test has run.
All seven acceptance criteria remain `NOT_VERIFIED`.
The publication reviewer remains unknown.

## Current evidence

The [readiness assessment](../../knowledge/raw/execution/session-renewal-full-2026-10-19/readiness/readiness.json) records actual local diagnostics.
The Jest attempt stopped before loading tests because its runner was missing.
Robot passed 32 dependency metadata checks and syntax checks for three selected source files.
These checks do not establish browser execution or private environment readiness.

The [UAT1 proposal](../../knowledge/raw/execution/session-renewal-full-2026-10-19/readiness/readiness-UAT1.json) preserves the selected environment and fixed command.
The [configuration check](../../knowledge/raw/execution/session-renewal-full-2026-10-19/readiness/proposed-UAT1-after-fix-verification.json) passed after commit `fb39c03`.
The separate workspace accepts a timeout of 1800 seconds.
The supported maximum is 3600 seconds.
The canonical workspace retains its 30-second timeout.

The proposed resource grants no operations.
Its local `list` attempt returned the expected `DENIED` status.
The original timeout failure remains retained in the [historical check](../../knowledge/raw/execution/session-renewal-full-2026-10-19/readiness/proposed-UAT1-schema-validation.json).
No external request or dependency installation occurred during this assessment.

## Execution scope

Use the existing `testing.command` provider with one fixed named command.
The [local proposed workspace](../../.workbench/session-renewal-full-20261019/readiness/uat1-proposed-workspace/workspace.yaml) contains the exact arguments.
This file remains in ignored local storage.
It selects only `BAU-UI-RP-LOGIN-001-006` from `Tests/ratan/workspace/ui/BAU-UI-RP.robot`.
Its `--test` filter excludes every other case, including the cashflow creation case `BAU-UI-RP-LOGIN-001-007`.
The suite setup still runs before the selected case.

The [selected source](../../knowledge/raw/execution/session-renewal-full-2026-10-19/readiness/uat1-source-inputs/repos/testing/ratan-test-engine/Tests/ratan/workspace/ui/BAU-UI-RP.robot) waits for the expired-session prompt.
It clicks Extend, opens MO Rules, and checks LIVE.
This provides limited evidence of access after extension.
It does not assert token validity, request success, pending state, or an exact prompt closure count.

The command explicitly supplies `--variable ENV:uat1`.
This overrides the source default `ENV:stg`.
The private `SECRET` binding selects `Tests/ratan/data/env_${ENV}_${SECRET}.yaml`.
Its contents and usable credentials remain unconfirmed.

## Steps and verification

Owners for the following work remain unknown.
Each step must retain its actual result and evidence limits.

| Step | Action | Verification gate |
| --- | --- | --- |
| 1 | Provision the declared Browser and Jest dependencies through the owning repositories' supported setup. | Resolve required packages. Confirm compatible Browser wrapper assets. Complete a local browser launch without business imports. |
| 2 | Supply private UAT1 bindings in the ignored variable file. Confirm certificate sourcing and login context behavior. | Confirm required names, the resolved UAT1 configuration path, and account suitability without publishing values. |
| 3 | Identify the deployed UAT1 application and backend revisions. | Retain deployment evidence and compare exact source bytes with the selected pilot revision. |
| 4 | When runnable, grant only `list` and `run` to the isolated resource. | Run `status` and `list`. Confirm one fixed named command, `ENV:uat1`, timeout 1800, and the exact case filter. |
| 5 | Execute the selected case once with a fresh output directory. | Inspect Robot assertions, exit status, and retained native outputs. Report only the assertions actually executed. |
| 6 | Add assertions for all seven criteria in the owning test sources. | Inspect fixtures, preconditions, request chains, delayed responses, rejected responses, token updates, and closure counts. |
| 7 | Execute the complete criterion set at its required integration level. | Bind results to exact assertions, implementation revisions, deployed revisions, configuration identities, and input hashes. |
| 8 | Obtain human review before publishing important requirements or decisions. | Record the actual reviewer, review result, unresolved findings, and an immutable governance event when publication changes state. |

The following working checkout links provide optional operating guidance.
Their contents can differ from the assessed revisions.
Use the [test-engine setup guide](../../repos/testing/ratan-test-engine/docs/WORKBENCH.md) for its supported Python and Robot environment.
Use its [manifest](../../repos/testing/ratan-test-engine/pyproject.toml) and platform-specific browser setup for declared dependencies.
Use the MFE [manifest](../../repos/ui/mfe-base/package.json), [Jest configuration](../../repos/ui/mfe-base/jest.config.ts), and owning installation policy.
Resolve the private package source before installing MFE dependencies.

The [pilot retention map](../../knowledge/raw/execution/session-renewal-full-2026-10-19/readiness/pilot-input-retention-map.json) records exact hashes and retained locations.
Use the [retained manifest](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/package.json.snapshot) to review the assessed dependency declarations.
Use the [retained Jest configuration](../../knowledge/raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/jest.config.ts.snapshot) to review the assessed runner settings.
The optional current MFE checkout is at `dddb76c8e8ba8ea66bb941feaad562740fdb8346`.
Confirm the selected checkout before using its installation files.

Follow [dependency maintenance](../../AGENTS.md#dependency-maintenance), [dependency analysis](../DEPENDENCIES.md), and [setup guidance](../SETUP.md) for dependency changes.
This plan does not install or change dependencies.

## Private bindings

The proposed variable-file location is relative to the isolated execution workspace:

```text
.workbench/private/uat1.robot.variables.yaml
```

Supply these names through that private YAML file:

- `SECRET`
- `USERNAME_MO`
- `PASSWORD_MO`
- `LOGIN_URL`
- `MARKETS_OPERATIONS_ONE`
- `SECURITY_SOURCE`

Portal certificate sourcing also requires `TEST_PORTAL_URL` and `TEST_PORTAL_CERTIFICATE_ENDPOINT`.
Confirm the approved sourcing mode before execution.
The [suite setup](../../knowledge/raw/execution/session-renewal-full-2026-10-19/readiness/uat1-source-inputs/repos/testing/ratan-test-engine/Resources/keywords/commonBiz.resource) can contact that portal during initialization.
The [browser helper](../../knowledge/raw/execution/session-renewal-full-2026-10-19/readiness/uat1-source-inputs/repos/testing/ratan-test-engine/Resources/keywords/playwright.resource) can reuse stored login context.
Record the chosen session-state policy with the run evidence.

The Workbench root `.env` exists.
Its values were not read.
Its presence does not supply Robot scalar bindings automatically.
Keep private values outside catalogs, command arguments, and published reports.

## Proposed invocation

Use the installed Workbench CLI from the standalone checkout.
Run these commands only after setup, deployment mapping, and the narrow resource grant are ready.

```sh
ai-sdlc --workspace .workbench/session-renewal-full-20261019/readiness/uat1-proposed-workspace status
ai-sdlc --workspace .workbench/session-renewal-full-20261019/readiness/uat1-proposed-workspace call uat1-session-extension list
ai-sdlc --workspace .workbench/session-renewal-full-20261019/readiness/uat1-proposed-workspace call uat1-session-extension run --args '{"suite":"session-extend-001-006"}'
```

The command has a fixed `--test BAU-UI-RP-LOGIN-001-006` filter.
It has no arbitrary suite or argument input.
The current empty grant prevents execution.
Select a fresh fixed output directory before each later run.
Preserve prior native outputs and Workbench action records.
Review native logs before sharing them because setup can handle private values.

## Required criterion assertions

Use the [candidate requirement](../../knowledge/candidates/requirements/REQ-active-session-renewal.md) for the complete Gherkin declarations and measurements.
The existing selected case cannot verify these criteria completely.

| Criterion | Additional measurable assertion |
| --- | --- |
| AC-1 | Mouse activity every 100 milliseconds for 15 seconds produces at least one successful renewal. |
| AC-2 | Keyboard activity every 100 milliseconds for 15 seconds produces at least one successful renewal. |
| AC-3 | Scroll activity every 100 milliseconds for 15 seconds produces at least one successful renewal. |
| AC-4 | Four controlled hours produce zero fresh SSO prompts caused solely by elapsed session time. |
| AC-5 | A usable refresh token and a pending renewal produce zero premature successful prompt closures. |
| AC-6 | Successful refresh-based renewal closes the prompt exactly once after completion. |
| AC-7 | Rejected renewal produces zero successful closures and permits another renewal attempt. |

Retain the valid-session and expiry preconditions for the activity criteria.
Use controlled delayed responses to inspect AC-5 before the request settles.
Observe the request, backend response, token update, and resulting UI transition.
Use rejected responses and a successful retry to inspect AC-7.
The controlled four-hour horizon does not establish unlimited session duration.
Keep mocked assertions separate from browser and backend integration evidence.

## Open findings

| Finding | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| Missing Browser assets | [Browser diagnostic](../../knowledge/raw/execution/session-renewal-full-2026-10-19/readiness/robot-browser-files.stdout.txt) | Wrapper dependencies and `playwright-core` are absent. Browser execution remains blocked. | unknown | Prepare supported wrapper dependencies and compatible binaries. |
| Missing Jest runtime | [Module diagnostic](../../knowledge/raw/execution/session-renewal-full-2026-10-19/readiness/mfe-required-modules.stdout.txt) | Saved Jest assertions cannot execute locally. | unknown | Provision the owning repository's declared dependencies. |
| Private bindings unconfirmed | [UAT1 assessment](../../knowledge/raw/execution/session-renewal-full-2026-10-19/readiness/readiness-UAT1.json) | File existence does not establish usable UAT1 access. | unknown | Supply and confirm the private variable bindings. |
| Deployment mapping missing | [UAT1 assessment](../../knowledge/raw/execution/session-renewal-full-2026-10-19/readiness/readiness-UAT1.json) | UAT1 observations cannot establish execution of the pilot revision. | unknown | Retain exact deployed application and backend revision evidence. |
| Criterion assertions incomplete | [Selected source](../../knowledge/raw/execution/session-renewal-full-2026-10-19/readiness/uat1-source-inputs/repos/testing/ratan-test-engine/Tests/ratan/workspace/ui/BAU-UI-RP.robot) | A passing selected case cannot verify all seven criteria. | unknown | Implement and inspect the missing criterion assertions. |
| Publication review pending | [Candidate requirement](../../knowledge/candidates/requirements/REQ-active-session-renewal.md) | Approved intent and publication readiness remain unresolved. | unknown | Record authorized human review before publication. |

The pilot MFE revision is `4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8`.
Its relationship to the deployed UAT1 application remains unknown.
The [Java diagnostic](../../knowledge/raw/execution/session-renewal-full-2026-10-19/readiness/java-version.stderr.txt) reports no local runtime.
That limits local BFF execution; hosted UAT1 browser execution does not require that local launcher.

The planned completion gate requires explicit evidence or a recorded unresolved gap for every criterion.
Passing configuration checks alone cannot establish business verification.
