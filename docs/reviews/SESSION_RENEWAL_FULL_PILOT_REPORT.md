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

# Full session-renewal pilot

## Scope and source

The user requested continued pilot work on 19 October 2026.
The user selected UAT1 for business testing.
The business reviewer remains unknown.
The Workbench source baseline is `141bf45`.
The assessed MFE implementation is `4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8`.

The independent MFE checkout still uses `dddb76c8e8ba8ea66bb941feaad562740fdb8346`.
Exact revision reads and an isolated export supplied pilot evidence.
This stage preserves the unrelated `TODO` file and existing test-engine `CLAUDE.md` changes.

## Confirmed Workbench timeout defect

The existing UAT1 session case permits 960 seconds for the expiry prompt.
The workspace schema rejected timeouts above 300 seconds.
The provider timeout helper already supported 3600 seconds.
This mismatch prevented a scoped 1800-second test workspace from loading.

The workspace schema now supports up to 3600 seconds.
The canonical workspace timeout remains 30 seconds.
The [Robot guide](../ROBOT_TESTING.md) documents separate workspaces for long scenarios.
No dependency, credential, or business runtime source changed.

Affected interfaces include workspace loading, CLI and MCP dispatch, and provider execution contexts.
Qualitative risk is moderate because explicitly configured operations can run longer.
Existing default behavior remains unchanged.
One regression checks actual dispatch and retained results with an 1800-second timeout.
Another regression rejects a value above 3600 seconds before dispatch.

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| Schema cap 300 conflicts with provider cap 3600 | The existing long session case could not load. | Workbench maintainers; individual unknown | Keep configuration and provider limits aligned through regression checks. |

## Runtime and distribution checks

The [runtime suite](../evidence/session-renewal-full-20261019/runtime-tests.txt) completed 479 tests without failures; two tests were skipped.
The [wheel build](../evidence/session-renewal-full-20261019/wheel-build.txt) passed with installed build dependencies and `--no-build-isolation`.
An isolated installed environment passed 27 [wheel checks](../evidence/session-renewal-full-20261019/wheel-check.json) outside the source checkout.
Four additional [timeout checks](../evidence/session-renewal-full-20261019/timeout-wheel-check.json) passed through that installed runtime.
Those fixtures do not establish UAT1 behavior.

## Remaining verification gates

The requirement remains a candidate with no recorded human approval.
All seven business criteria remain `NOT_VERIFIED`.
Controlled source characterization, assertion inspection, and live business verification have separate evidence boundaries.

## Complete criterion scope

The [full trace](SESSION_RENEWAL_FULL_TRACE.md) includes all seven candidate criteria.
The [immutable baseline](../../relationships/requirement-code/baselines/PILOT-session-renewal-full-20261019.json) preserves the prior three behavior records exactly.
It adds four behavior identities at version 1.
Historical source captures, assertion links, findings, and execution records remain retained.

| Candidate criteria | Controlled result | Missing system evidence |
| --- | --- | --- |
| AC-1, AC-2, AC-3 | Each activity type produces three requests across 15 seconds. | Successful backend renewal within the interval. |
| AC-4 | Four controlled hours produce zero Home timeout signals under mocked store updates. | Actual response handling, token replacement, and fresh SSO navigation. |
| AC-5 | A present refresh string produces zero closures while renewal remains pending. | Real credential usability, pending deadlines, and mounted browser behavior. |
| AC-6 | Controlled successful renewal produces exactly one closure after completion. | Backend acceptance, real credentials, and browser integration. |
| AC-7 | Controlled rejection preserves the prompt and permits a successful retry. | Real rejection, retry, and browser state. |

Seven behaviors have source, assertion, and controlled execution mappings.
Those mappings do not establish complete assertion coverage or passing system behavior.
The complete system verification count remains zero of seven.

## Retained controlled execution

The [successor result](../../knowledge/raw/execution/session-renewal-full-2026-10-19/controlled/run-002/characterization-result.json) records 16 passing controlled source check groups.
The [pre-run binding](../../knowledge/raw/execution/session-renewal-full-2026-10-19/controlled/run-002/original-binding.json) identifies original command, input, configuration, harness, and source hashes.
Five executed module hashes match the assessed exact Git revision.
Ten [integrity checks](../../knowledge/raw/execution/session-renewal-full-2026-10-19/controlled/run-002/evidence-integrity-check.json) passed.
Twenty-eight independent [peer checks](../../knowledge/raw/execution/session-renewal-full-2026-10-19/review/peer-review.json) passed, including hash checks for 439 exported source files.

Each short activity fixture uses 150 events at 100-millisecond intervals.
The four-hour fixture uses 14,400 events and 2,880 requests.
That fixture manually replaces session state; the real response handler does not execute.
The prompt fixture now includes a controlled refresh string and exact closure assertions.
Mocked decoding does not establish real credential usability.

The prior harness, original result, and setup failures remain unchanged.
Setup failures establish unavailable setup, without establishing a business test failure.
The successor executes transformed TypeScript with modeled hooks, timers, events, transport, and decoding.
It does not execute React, Jest, a browser, the backend, or an identity provider.

## UAT1 preparation and open findings

The [UAT1 plan](SESSION_RENEWAL_UAT1_PLAN.md) provides each remaining step and its verification.
The fixed proposal selects only `BAU-UI-RP-LOGIN-001-006` with `ENV:uat1`.
The scoped workspace accepts 1800 seconds after timeout correction commit `fb39c03`.
Its empty grants deny execution until setup is ready.
No UAT1 business scenario ran.

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| [Readiness](../../knowledge/raw/execution/session-renewal-full-2026-10-19/readiness/readiness-UAT1.json) records missing Browser wrapper dependencies. | Browser execution cannot start through the selected setup. | unknown | Prepare supported Browser dependencies and compatible binaries. |
| The same assessment leaves private bindings unconfirmed. | The selected account, URL, and configuration remain unbound. | unknown | Supply private bindings locally and confirm UAT1 setup. |
| No deployment evidence maps UAT1 to the pilot revision. | A future result cannot yet establish pilot behavior. | unknown | Retain exact frontend and backend deployment identities. |
| The existing case checks Extend followed by LIVE. | It lacks complete assertions for all seven criteria. | unknown | Add dedicated criterion assertions through the owning repository procedure. |
| The local Jest runner could not load. | Zero Jest cases executed. | unknown | Provision declared test dependencies and retain runner results. |
| Activity cadence is five seconds; the helper aborts older requests. | Slow response completion remains unassessed. | unknown | Exercise requests pending beyond five seconds through the actual response chain. |
| Requirement review remains pending. | Publication has no required human approval. | unknown | Record the actual reviewer and review before publication. |

The [governance finding](../../knowledge/findings/GF-session-renewal-verification-gates.md) retains these verification limits.
It does not assert a deployed defect.
No credentials, dependencies, business repository source, or live connector catalogs changed during this stage.

## Evidence package checks

The saved [baseline check](../evidence/session-renewal-full-20261019/assurance-validation.json) reports `VALID` and `CURRENT` with no diagnostics.
The [comparison](../evidence/session-renewal-full-20261019/baseline-comparison.json) identifies four added behaviors and seven affected behavior mappings.
A separate [baseline peer review](../evidence/session-renewal-full-20261019/baseline-peer-review.json) passed 59 checks and included a retrieval exercise.
The [trace review](../evidence/session-renewal-full-20261019/trace-review.json) checks exact criteria, source hashes, citations, and writing limits.
The [UAT1 plan review](../evidence/session-renewal-full-20261019/UAT1-plan-review.json) checks the narrow filter, configuration, links, and pending review state.

Authoring lint passes with four expected warnings.
Those warnings retain unknown ownership, pending business review, unresolved content, and pending ASD review.
Workspace validation passes for 13 knowledge documents without findings.
The ingestion check preserves prior raw bytes, manifest records, and audit events.
It binds five executed source hashes to the selected Git revision.
These deterministic results grant neither human approval nor business verification.
