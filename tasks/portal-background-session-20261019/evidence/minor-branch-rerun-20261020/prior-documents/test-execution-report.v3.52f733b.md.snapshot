---
artifact_kind: test-execution-report
id: EXEC-session-renewal-browser-20261020
version: 3
status: draft
owner: unknown
source_refs:
  - SRC-session-browser-final-manifest-20261020
  - SRC-session-e2e-final-20261020
  - SRC-session-stage-baseline-20261020
  - SRC-session-expanded-frontend-login-20261020
  - SRC-session-expanded-frontend-handler-20261020
  - SRC-session-expanded-validate-contract-20261020
  - SRC-session-expanded-equivalence-20261020
  - SRC-session-expanded-browser-20261020
  - SRC-session-expanded-stage-20261020
  - SRC-session-expanded-tests-20261020
  - SRC-session-expanded-fixture-20261020
  - SRC-session-review-intent-v4
  - SRC-session-expanded-unit-20261020
  - SRC-session-expanded-build-20261020
  - SRC-session-expanded-proposal-20261020
  - SRC-session-expanded-release-gaps-20261020
related_ids:
  - DEFECT-portal-background-session-20261019
  - REQ-active-session-renewal
  - CHANGE-session-post-review-20261020
  - EXEC-session-renewal-expanded-20261020
review:
  state: pending
  reviewer: null
  reviewed_at: null
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
    - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Session renewal E2E test execution

> **Critical conclusions: Action required**
>
> **GO-LIVE HOLD: resolve four TypeScript errors before release.**
> Action: review the guard proposal and correct baseline test typing. Repeat typecheck and the configured production build.
> Consequence: passing browser cases do not establish build readiness.
> Owner: unknown application and build owners. Evidence: [compiler results and unapplied proposal](#unit-execution-and-build-readiness).
>
> **Two observations still need acceptance decisions. Production verification remains open.**
> Action: define recovery outcomes and populated workspace fixtures. Assign owners for deployment and integration checks.
> Consequence: local results cannot close production acceptance.
> Owner: unknown business and release owners. Evidence: [case outcomes](#assertions-and-outcomes) and [release findings](#findings).

## Stage boundary and readiness

This stage expands the existing browser inventory from 14 cases to 22 cases.
This file consolidates the original execution report and its expanded review.
The [earlier 14-case run](#earlier-14-case-execution) retains its source identity and scoped results below.
The frozen intake and earlier coverage report remain historical evidence.
Earlier results do not verify the current test source or application runtime.
The [consolidation record](evidence/report-consolidation-20261020.json) preserves prior report hashes and Git recovery locators.
All 22 cases have retained results. The manifest preserves 25 attempts, including three historical harness failures.

| Named phase | Status | Evidence and rationale | Owner and next action |
| --- | --- | --- | --- |
| Local evidence collection | READY | The stage baseline records user authorization, exact revisions, inspected assertions, and isolated fixtures. | unknown: session test owner. Review all 22 results and retain their scope limits. |
| Production release | NEEDS_CLARIFICATION | Introduced type errors remain. Production configuration, deployment binding, and policy acceptance remain absent. | unknown: release owner. Resolve build and acceptance blockers before release decisions. |

Risk is medium because timing, credentials, request cancellation, and test controls affect verdicts.
The named readiness permits local evidence collection only.
It grants no production release approval or knowledge publication.
The requirement remains a candidate with pending human review.
Go-live remains on hold because the changed extension guard introduces two type errors.
The proposed correction remains unapplied under the earlier review-only boundary.

## Tests that did not pass

**No final browser case failed.** Nineteen cases passed, one diagnostic passed, and two observations completed.
**Current unit execution passed all 451 tests.** The declared TypeScript check failed with four errors.
The production build remains `NOT_RUN` because required configuration is absent.
See [unit and build readiness](#unit-execution-and-build-readiness) for exact diagnostics and next actions.

Three earlier browser attempts failed. Their corrected reruns completed at the verdicts below.
These failures concern test setup or an incorrect assertion.

The first natural and missing-refresh attempts timed out before the required hidden state.
The runner replaced native-window foreground assumptions with real covering tabs.
The current driver records tab activation and observed document visibility.
It does not override visibility or force freezing.
Both replacement natural runs completed. Their original failed setup attempts remain retained.

The first reload attempt failed an incorrect token-equality assertion.
[BFF validation](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L245) calls `buildEntities()`, which returns newly generated authorization.
The [frontend response handler](../../repos/ui/mfe-base/src/hooks/service/util/succes.response.handler.ts#L36) installs that header through [authorization helpers](../../repos/ui/mfe-base/src/utils/login.ts#L56).
Final reload assertions bind the validation request to the exact pre-reload token.
They require usable returned access, exact installation, refresh reacquisition, protected success, and zero additional login requests.
The corrected reload passed at `7a504c1`.

| Case and failed attempt | Why it failed | Corrected outcome | Evidence |
| --- | --- | --- | --- |
| [E2E-07](evidence/expanded-e2e-20261020/case-inventory.json#L579): Natural background recovery; `expanded-natural-20261020T011507` | The subject tab stayed visible. Its hidden-state wait timed out after ten seconds. | Real covering tabs established hidden state. The final 30-minute recovery passed. | [Failed attempt](evidence/expanded-e2e-20261020/browser/expanded-natural-20261020T011507/run.json) |
| [E2E-21](evidence/expanded-e2e-20261020/case-inventory.json#L1802): Missing-refresh return; `expanded-missing-20261020T011512` | The same visibility setup failed before the intended background interval. | Corrected setup completed. The final result remains `OBSERVATION_ONLY` because recovery policy is unresolved. | [Failed attempt](evidence/expanded-e2e-20261020/browser/expanded-missing-20261020T011512/run.json) |
| [E2E-16](evidence/expanded-e2e-20261020/case-inventory.json#L1334): Reload after renewal; `expanded-reload-20261020T013310` | The assertion required identical tokens after reload. BFF validation legitimately issues another token. | Corrected request and response assertions passed at `7a504c1`. | [Failed attempt](evidence/expanded-e2e-20261020/browser/expanded-reload-20261020T013310/run.json) |

Two final cases have no acceptance verdict:

| Case | Observed result | Why acceptance remains open | Owner and required action |
| --- | --- | --- | --- |
| [E2E-21](evidence/expanded-e2e-20261020/case-inventory.json#L1802) / [TC-04](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L266): Missing-refresh return | Sign-in appeared after background return. No access or refresh remained. | No approved recovery outcome exists. | unknown authentication owner. Define the expected recovery policy. |
| [E2E-22](evidence/expanded-e2e-20261020/case-inventory.json#L1870) / [TC-07](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L269): Workspace restoration | Two workspace descriptors and entitlements matched after sign-in. | Empty application descriptors cannot establish application-edit retention. | unknown workspace owner. Provide populated fixtures and acceptance criteria. |

These observations are evidence limits. They are not failed acceptance tests.

## Run identity and provenance

```yaml
execution_id: EXPANDED-session-browser-20261020
execution_status: COMPLETED
repository_id: ratan-test-engine
repository_revision: 7a504c13a8d51bb52af5cc89bd4af88d1988da94
test_revision: 7a504c13a8d51bb52af5cc89bd4af88d1988da94
test_source_sha256: 94db4519b1d8e2f3669eeea6df59b7a4242300e797f53d28fb2e3152c689e984
application_repository: mfe-base
application_revision: 9dcf201dc5ba3890bb527e750defb78e5f9dc75c
service_repository: single-ui-bff
service_revision: 85d7cc03eb12710d6facf581987fd4ae24fc9844
environment_identity: fast portal/BFF on 127.0.0.1:8103/8091; natural portal/BFF on 127.0.0.1:8101/8088
started_at: "2026-10-20T01:15:07.790Z"
completed_at: "2026-10-20T01:47:59.401Z"
command_or_tool_reference: .workbench/session-post-change-20261020/run-expanded.py
process_exit_status: null
actual_results: 19 PASSED; 1 DIAGNOSTIC_PASSED; 2 OBSERVATION_ONLY; 22 complete cases; 25 retained attempts.
retained_execution_refs:
  - evidence/expanded-e2e-20261020/browser-manifest.json
  - evidence/expanded-e2e-20261020/source-dependency-equivalence.json
```

The final reviewed test source is `7a504c1`. Actual executions retain their original revisions and module hashes.
Reload ran at `7a504c1`. The other 21 cases loaded `6de6fe8`.
All 22 cases have reconciled results. The 25 retained attempts include three historical harness failures.
Per-attempt results remain separate. No single aggregate process exit status is asserted.

## Browser environment and suite completeness

- Inventory: [22 inspected cases](evidence/expanded-e2e-20261020/case-inventory.json), final source `7a504c1`, with per-case revision locators.
- Original suite cases: seven from `62f1685`; all seven passed their scoped local predicates.
- Additional cases: 12 passed, one diagnostic passed, and two observations completed.
- Runtime source: MFE `9dcf201` and BFF `85d7cc0`. Tests retain their actual `6de6fe8` or `7a504c1` revisions.
- Binding: [Fixture binding](evidence/expanded-e2e-20261020/fixture-binding.json) records 343 matching MFE source files and harness hashes.
- Fast target: `http://127.0.0.1:8103/`; BFF: `127.0.0.1:8091`.
- Natural target: `http://127.0.0.1:8101/`; BFF: `127.0.0.1:8088`. Both profiles validate portal authentication.
- Browser: native Microsoft Edge `155.0.4283.62`, macOS, and fresh local profiles.
- Launch settings: retained arguments disable first-run, sync, updater, and background networking. CDP uses `noDefaults=true`.
- Clock: real wall clock. Natural cases require at least 1,800 seconds of hidden time.
- Source integrity: each retained result matches its executed module hash and revision. Dependency comparison supports 21 unchanged case closures.
- Incomplete executions: none. All 22 declared cases have retained results.
- Integrity: all case hashes match executed revisions. All embedded result hashes match their runs.
- Compatibility: 21 unchanged dependency closures support original evidence at the final source revision.

The fixture replaces toolkit elements and disables module federation remotes.
The BFF fixture uses actual controller, JWT, and session classes.
Identity, authorization, analytics, and catalog adapters are synthetic local fixtures.
Fast access expires after 60 seconds. Fast refresh expires after 144 seconds.
Natural access expires after 900 seconds. Natural refresh expires after 13,524 seconds.

Protected validation checks portal authentication. It does not execute a trading workflow.
Route holds, transport aborts, and the diagnostic response body are controlled test inputs.
Automation can affect browser suspension. Hidden time alone does not prove a frozen-tab condition.
The natural cases require recorded lifecycle events before any freeze coverage claim.

## Unit execution and build readiness

The [unit binding](evidence/expanded-e2e-20261020/unit/commit-binding.json) matches retained source and result hashes to MFE commit `4cddb38`.
The targeted run passed six tests across two suites.
The full run passed 451 tests across 119 suites.
Both runs retained unchanged source hashes during execution.
JSDOM, existing mocks, and forced process exit limit these unit results.
Unit counts do not establish browser behavior or production build success.

Browser runtime `9dcf201` has the same application source as `4cddb38`.
Only `succes.response.handler.session.test.ts` changed between those revisions.
That test correction freezes the fixture clock and adds a valid-success control.
The [release gap review](evidence/expanded-e2e-20261020/release-gap-review.json) marks the earlier clock-sensitivity finding resolved.

The [build review](evidence/expanded-e2e-20261020/build/typecheck-review.json) records four diagnostics from TypeScript `4.9.5`.
The selected declared typecheck returned exit status `2`.

| Check | Actual result | Source and consequence | Owner and next action |
| --- | --- | --- | --- |
| Current application guard | Two `TS18048` errors at `extend.ts:18` and `extend.ts:20`. | Changed session-correction lines fail the declared typecheck. Go-live remains on hold. | unknown: application owner. Review the proposed existence guard and repeat validation. |
| Existing Home tests | Two `TS2322` errors at `Home/index.test.tsx:183` and `Home/index.test.tsx:184`. | Exact baseline `2af6b83` reproduces both errors with current dependencies. Historical dependencies remain untested. | unknown: test owner. Correct the baseline fixture typing and repeat typecheck. |
| Proposed guard | Isolated typecheck removes both introduced errors. The two reproduced baseline errors remain. | The [proposed patch](evidence/expanded-e2e-20261020/proposed-type-fix.patch) remains unapplied. No proposed-code browser or unit execution exists. | unknown: application owner. Review the patch within the recorded review boundary. |
| Complete production build | NOT_RUN | `.env.server`, `.env.mfe`, and `.storybook` are absent. Webpack, server, Storybook, and declaration success remain unverified. | unknown: build owner. Supply approved configuration and run the complete declared build. |

The proposed guard appears to preserve runtime request-sharing behavior.
That conclusion is a source inference, not a passing runtime result.
The existing application checkout remains unchanged by the proposal.

## Definitions and BDD navigation

AC links open the exact Given/When/Then scenario in candidate requirement version 4.
TC links open the original proposed case scope in the frozen intake.
These links identify source definitions. They do not establish business approval or passing execution.

| Definition set | Exact source and version | SHA-256 |
| --- | --- | --- |
| [AC-1](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L137-L140), [AC-2](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L144-L147), [AC-3](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L151-L154), [AC-4](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L158-L162), [AC-5](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L166-L169), [AC-6](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L173-L176), [AC-7](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L180-L183) | [Local requirement](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria); version 4; Git `d6adcff452f1329d99528f0f7e8a6450a27ddc8c`. | `828d62209f11dd9bb9dee893ddc80e7e5d4dc6abd3c58170e902dab61bc587aa` |
| [TC-01](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L263), [TC-02](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L264), [TC-03](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L265), [TC-04](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L266), [TC-05](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L267), [TC-06](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L268), [TC-07](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L269) | [Frozen intake](intake.md#proposed-regression-cases); Git `cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c`. | `1650a20f8a2aba2105b30b8abc4bd2a881f58ee335925a3daa9f6a6c0d0e0948` |

[TC-01](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L263) uses [AC-5](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L166-L169) and [AC-6](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L173-L176). [TC-02](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L264) uses [AC-7](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L180-L183).
[TC-03](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L265), [TC-04](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L266), [TC-05](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L267), and [TC-06](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L268) define investigation scopes without standalone approved Gherkin scenarios.
[TC-07](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L269) also has a [proposed workspace scenario](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L274-L278).
Its populated application-edit boundary remains unresolved.
Owner: unknown session and workspace owners. Next action: define missing acceptance behavior before acceptance decisions.

[AC-4](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L158-L162) defines a controlled four-hour scenario. The current browser boundary covers initial refresh expiry within a shorter interval.
E2E IDs link the retained case inventory. Assertion links open the executed source snapshots.
Each result and screenshot link remains separate from its behavior definition.

## Case mapping

The stable IDs below follow the current Robot suite order.
Original means present at `62f1685`. Prior additions first appear at `66595b8`.
Current additions belong to this eight-case expansion.
Function lines retain executed source revisions. Reload uses `7a504c1`; all other case locators use `6de6fe8`.
The inventory retains exact Robot, function, helper, and assertion line mappings.

| Test ID | Mode | Function and line | Criteria or scope | Origin |
| --- | --- | --- | --- | --- |
| [E2E-01](evidence/expanded-e2e-20261020/case-inventory.json#L64) | `mouse` | [assertActivityRenewsSession:231](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot#L231) | [AC-1](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L137-L140) | original |
| [E2E-02](evidence/expanded-e2e-20261020/case-inventory.json#L146) | `keyboard` | [assertActivityRenewsSession:231](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot#L231) | [AC-2](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L144-L147) | original |
| [E2E-03](evidence/expanded-e2e-20261020/case-inventory.json#L228) | `scroll` | [assertActivityRenewsSession:231](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot#L231) | [AC-3](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L151-L154) | original |
| [E2E-04](evidence/expanded-e2e-20261020/case-inventory.json#L310) | `pending` | [assertPendingRenewalCompletes:313](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot#L313) | [AC-5](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L166-L169), [AC-6](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L173-L176), [TC-01](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L263) | original |
| [E2E-05](evidence/expanded-e2e-20261020/case-inventory.json#L402) | `retry` | [assertRejectedRenewalCanRetry:320](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot#L320) | [AC-7](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L180-L183), [TC-02](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L264) | original |
| [E2E-06](evidence/expanded-e2e-20261020/case-inventory.json#L495) | `cross` | [assertActivityCrossesRefreshExpiry:581](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot#L581) | [AC-4-live-boundary](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L158-L162) | original |
| [E2E-07](evidence/expanded-e2e-20261020/case-inventory.json#L579) | `natural` | [assertNaturalBackgroundRecovery:623](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot#L623) | [TC-03](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L265), [TC-06](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L268), [AC-5](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L166-L169), [AC-6](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L173-L176) | original |
| [E2E-08](evidence/expanded-e2e-20261020/case-inventory.json#L680) | `single` | [assertSlowActivitySharesRequest:686](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot#L686) | Supporting boundary | prior-addition |
| [E2E-09](evidence/expanded-e2e-20261020/case-inventory.json#L763) | `rapid` | [assertRapidExtendSharesRequest:337](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot#L337) | [AC-5](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L166-L169), [AC-6](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L173-L176) | current-addition |
| [E2E-10](evidence/expanded-e2e-20261020/case-inventory.json#L848) | `keyboardExtend` | [assertKeyboardExtendActivation:378](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot#L378) | [AC-5](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L166-L169), [AC-6](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L173-L176) | current-addition |
| [E2E-11](evidence/expanded-e2e-20261020/case-inventory.json#L937) | `activityRetry` | [assertActivityFailureCanRetry:386](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot#L386) | Supporting boundary | current-addition |
| [E2E-12](evidence/expanded-e2e-20261020/case-inventory.json#L1019) | `inconsistent` | [assertInconsistentActivityResponseRejected:416](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot#L416) | Supporting boundary | current-addition |
| [E2E-13](evidence/expanded-e2e-20261020/case-inventory.json#L1108) | `promptActivity` | [assertPromptIgnoresActivity:461](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot#L461) | Supporting boundary | current-addition |
| [E2E-14](evidence/expanded-e2e-20261020/case-inventory.json#L1200) | `idleLogout` | [assertIdlePromptLogout:493](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot#L493) | Supporting boundary | current-addition |
| [E2E-15](evidence/expanded-e2e-20261020/case-inventory.json#L1263) | `visibility` | [assertQuickVisibilityRefresh:523](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot#L523) | Supporting boundary | current-addition |
| [E2E-16](evidence/expanded-e2e-20261020/case-inventory.json#L1334) | `reload` | [assertReloadPreservesRenewedSession:554](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L554) | Supporting boundary | current-addition |
| [E2E-17](evidence/expanded-e2e-20261020/case-inventory.json#L1434) | `manualLogout` | [assertPendingManualLogoutCancels:738](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot#L738) | Supporting boundary | prior-addition |
| [E2E-18](evidence/expanded-e2e-20261020/case-inventory.json#L1515) | `activityLogout` | [assertPendingActivityLogoutCancels:770](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot#L770) | Supporting boundary | prior-addition |
| [E2E-19](evidence/expanded-e2e-20261020/case-inventory.json#L1609) | `late` | [assertLateActivityCannotReplaceManualSuccess:800](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot#L800) | Supporting boundary | prior-addition |
| [E2E-20](evidence/expanded-e2e-20261020/case-inventory.json#L1736) | `expired` | [assertActualExpiredCredentialDenied:836](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot#L836) | [TC-05](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L267) | prior-addition |
| [E2E-21](evidence/expanded-e2e-20261020/case-inventory.json#L1802) | `missing` | [observeBackgroundWithoutRefresh:873](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot#L873) | [TC-04](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L266) | prior-addition |
| [E2E-22](evidence/expanded-e2e-20261020/case-inventory.json#L1870) | `workspace` | [observeWorkspaceDescriptorsAfterSignIn:926](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot#L926) | [TC-07](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L269) | prior-addition |

## Assertions and outcomes

| Test ID | Requirement or criterion | Inspected assertion entry | Expected result | Actual result | Outcome | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| [E2E-01](evidence/expanded-e2e-20261020/case-inventory.json#L64) | [AC-1](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L137-L140) | [sessionRenewal.cjs:231](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot#L231) | Trusted mouse activity renews access within 15 seconds and passes protected validation. | 146 trusted events; two successful renewals; protected validation passed. | PASSED | [Result](evidence/expanded-e2e-20261020/browser/expanded-mouse-20261020T011515/artifacts/result.json) |
| [E2E-02](evidence/expanded-e2e-20261020/case-inventory.json#L146) | [AC-2](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L144-L147) | [sessionRenewal.cjs:231](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot#L231) | Trusted keyboard activity renews access within 15 seconds and passes protected validation. | 139 trusted events; two successful renewals; protected validation passed. | PASSED | [Result](evidence/expanded-e2e-20261020/browser/expanded-keyboard-20261020T011555/artifacts/result.json) |
| [E2E-03](evidence/expanded-e2e-20261020/case-inventory.json#L228) | [AC-3](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L151-L154) | [sessionRenewal.cjs:231](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot#L231) | Trusted scroll activity renews access within 15 seconds and passes protected validation. | 146 trusted events; two successful renewals; protected validation passed. | PASSED | [Result](evidence/expanded-e2e-20261020/browser/expanded-scroll-20261020T011627/artifacts/result.json) |
| [E2E-04](evidence/expanded-e2e-20261020/case-inventory.json#L310) | [AC-5](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L166-L169), [AC-6](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L173-L176), [TC-01](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L263) | [sessionRenewal.cjs:313](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot#L313) | Pending renewal closes zero prompts; actual success closes once and passes protected validation. | Zero pending closures; one completion closure; protected validation passed. | PASSED | [Result](evidence/expanded-e2e-20261020/browser/expanded-pending-20261020T011700/artifacts/result.json) |
| [E2E-05](evidence/expanded-e2e-20261020/case-inventory.json#L402) | [AC-7](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L180-L183), [TC-02](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L264) | [sessionRenewal.cjs:320](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot#L320) | Transport failure preserves the prompt; actual retry installs access and closes once. | Failure preserved retry and zero closures. Actual retry closed once. | PASSED | [Result](evidence/expanded-e2e-20261020/browser/expanded-retry-20261020T011812/artifacts/result.json) |
| [E2E-06](evidence/expanded-e2e-20261020/case-inventory.json#L495) | [AC-4-live-boundary](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L158-L162) | [sessionRenewal.cjs:581](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot#L581) | Activity crosses initial refresh expiry without sign-in or prompt and passes protected validation. | 186 seconds; 18 renewals; replaced refresh; zero login, navigation, or prompt events. | PASSED | [Result](evidence/expanded-e2e-20261020/browser/expanded-cross-20261020T011926/artifacts/result.json) |
| [E2E-07](evidence/expanded-e2e-20261020/case-inventory.json#L579) | [TC-03](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L265), [TC-06](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L268), [AC-5](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L166-L169), [AC-6](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L173-L176) | [sessionRenewal.cjs:623](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot#L623) | After 1,800 seconds, hidden recovery completes renewal while the visible idle control expires. | Hidden 1,800,016 milliseconds; freeze flag true; control expired; zero pending closures; one completion closure; protected 200. | PASSED | [Result](evidence/expanded-e2e-20261020/browser/expanded-natural-20261020T011740/artifacts/result.json) |
| [E2E-08](evidence/expanded-e2e-20261020/case-inventory.json#L680) | Supporting boundary | [sessionRenewal.cjs:686](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot#L686) | Repeated activity shares one pending extension with zero cancellations and installs actual renewed access. | 116 inputs; one held request; zero cancellations; protected validation passed. | PASSED | [Result](evidence/expanded-e2e-20261020/browser/expanded-single-20261020T012239/artifacts/result.json) |
| [E2E-09](evidence/expanded-e2e-20261020/case-inventory.json#L763) | [AC-5](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L166-L169), [AC-6](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L173-L176) | [sessionRenewal.cjs:337](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot#L337) | Two pointer attempts create one relogin; pending closure count is zero and successful closure count is one. | Two pointer attempts; one request; zero pending closures; one completion closure. | PASSED | [Result](evidence/expanded-e2e-20261020/browser/expanded-rapid-20261020T012705/artifacts/result.json) |
| [E2E-10](evidence/expanded-e2e-20261020/case-inventory.json#L848) | [AC-5](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L166-L169), [AC-6](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L173-L176) | [sessionRenewal.cjs:378](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot#L378) | Enter activates Extend; actual renewal installs access and closes the prompt once. | Enter completed actual renewal. Prompt closed once; protected validation passed. | PASSED | [Result](evidence/expanded-e2e-20261020/browser/expanded-keyboardExtend-20261020T012816/artifacts/result.json) |
| [E2E-11](evidence/expanded-e2e-20261020/case-inventory.json#L937) | Supporting boundary | [sessionRenewal.cjs:386](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot#L386) | A failed activity extension preserves available access; later activity renews against the actual service. | One failed transport attempt; one successful retry; no prompt after failure. | PASSED | [Result](evidence/expanded-e2e-20261020/browser/expanded-activityRetry-20261020T012929/artifacts/result.json) |
| [E2E-12](evidence/expanded-e2e-20261020/case-inventory.json#L1019) | Supporting boundary | [sessionRenewal.cjs:416](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot#L416) | A negative body preserves access; a distinct successful retry installs its actual token. | Negative body preserved access. Distinct actual retry returned success and installed its token. | DIAGNOSTIC_PASSED | [Result](evidence/expanded-e2e-20261020/browser/expanded-inconsistent-20261020T012957/artifacts/result.json) |
| [E2E-13](evidence/expanded-e2e-20261020/case-inventory.json#L1108) | Supporting boundary | [sessionRenewal.cjs:461](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot#L461) | Prompt activity starts zero extensions and closes zero prompts; actual Extend later succeeds. | Six mouse, keyboard, and scroll inputs each; zero extensions; later Extend succeeded. | PASSED | [Result](evidence/expanded-e2e-20261020/browser/expanded-promptActivity-20261020T013027/artifacts/result.json) |
| [E2E-14](evidence/expanded-e2e-20261020/case-inventory.json#L1200) | Supporting boundary | [sessionRenewal.cjs:493](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot#L493) | Idle logout clears stored access, leaves no persisted refresh, and returns to sign-in without relogin. | Logout observed; stored access cleared; persisted refresh absent; sign-in shown; zero relogin. | PASSED | [Result](evidence/expanded-e2e-20261020/browser/expanded-idleLogout-20261020T013146/artifacts/result.json) |
| [E2E-15](evidence/expanded-e2e-20261020/case-inventory.json#L1263) | Supporting boundary | [sessionRenewal.cjs:523](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot#L523) | A short hidden switch receives one refresh response and preserves authentication on return. | One refresh response; no return prompt; authenticated portal and protected validation passed. | PASSED | [Result](evidence/expanded-e2e-20261020/browser/expanded-visibility-20261020T013251/artifacts/result.json) |
| [E2E-16](evidence/expanded-e2e-20261020/case-inventory.json#L1334) | Supporting boundary | [sessionRenewal.cjs:554](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot#L554) | Reload validates with the exact prior token and installs usable returned access. Refresh reacquisition and protected validation succeed without login. | Prior renewed token validated; returned rotated token installed; refresh reacquired; zero login; protected validation passed. | PASSED | [Result](evidence/expanded-e2e-20261020/browser/expanded-reload-20261020T013558/artifacts/result.json) |
| [E2E-17](evidence/expanded-e2e-20261020/case-inventory.json#L1434) | Supporting boundary | [sessionRenewal.cjs:738](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot#L738) | Logout cancels pending manual renewal; late success restores neither access nor the portal. | Manual request cancelled; late success restored neither access nor portal. | PASSED | [Result](evidence/expanded-e2e-20261020/browser/expanded-manualLogout-20261020T012308/artifacts/result.json) |
| [E2E-18](evidence/expanded-e2e-20261020/case-inventory.json#L1515) | Supporting boundary | [sessionRenewal.cjs:770](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot#L770) | Logout unmounts Home, cancels pending activity renewal, and prevents late access restoration. | Home unmounted through logout; extension cancelled; late success restored no access. | PASSED | [Result](evidence/expanded-e2e-20261020/browser/expanded-activityLogout-20261020T012415/artifacts/result.json) |
| [E2E-19](evidence/expanded-e2e-20261020/case-inventory.json#L1609) | Supporting boundary | [sessionRenewal.cjs:800](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot#L800) | Manual renewal survives an older activity response with exactly one prompt closure. | Stale activity cancelled; manual token preserved; one prompt closure; protected validation passed. | PASSED | [Result](evidence/expanded-e2e-20261020/browser/expanded-late-20261020T012436/artifacts/result.json) |
| [E2E-20](evidence/expanded-e2e-20261020/case-inventory.json#L1736) | [TC-05](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L267) | [sessionRenewal.cjs:836](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot#L836) | The actual service rejects a naturally expired credential with HTTP 401 or 403. | Initial validation returned 200. Naturally expired credential returned 401. | PASSED | [Result](evidence/expanded-e2e-20261020/browser/expanded-expired-20261020T012551/artifacts/result.json) |
| [E2E-21](evidence/expanded-e2e-20261020/case-inventory.json#L1802) | [TC-04](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L266) | [sessionRenewal.cjs:873](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot#L873) | Record return state after 1,800 seconds with blocked refresh acquisition and no observed refresh. | After 1,802,220 milliseconds: freeze observed; one blocked acquisition; no refresh or retained access; sign-in visible. | OBSERVATION_ONLY | [Result](evidence/expanded-e2e-20261020/browser/expanded-missing-20261020T011743/artifacts/result.json) |
| [E2E-22](evidence/expanded-e2e-20261020/case-inventory.json#L1870) | [TC-07](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L269) | [sessionRenewal.cjs:926](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot#L926) | Create two workspaces and record descriptor comparison after sign-out and same-user sign-in. | Two empty descriptors and entitlements matched after same-user sign-in. Populated parameters remain uncovered. | OBSERVATION_ONLY | [Result](evidence/expanded-e2e-20261020/browser/expanded-workspace-20261020T012657/artifacts/result.json) |

[AC-4](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L158-L162) has a short live refresh boundary. The exact four-hour criterion remains outside this browser inventory.
[TC-04](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L266) and [TC-07](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L269) remain observations because their acceptance policies are unresolved.
The inconsistent-response case remains diagnostic until its deployed contract is confirmed.
A diagnostic outcome cannot establish a confirmed application defect without that contract.

## Per-case source and result bindings

| Source label | Exact revision | Whole-module SHA-256 |
| --- | --- | --- |
| [A](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot) | 6de6fe8abfe67541bd207433689f86102a0e44ad | 8e5797903ed3eea2e490f548e55227d1047f6eaa20185032f78a1896c44b7598 |
| [B](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot) | 7a504c13a8d51bb52af5cc89bd4af88d1988da94 | 94db4519b1d8e2f3669eeea6df59b7a4242300e797f53d28fb2e3152c689e984 |

Source labels below resolve to these exact revision and hash pairs.
The [dependency comparison](evidence/expanded-e2e-20261020/source-dependency-equivalence.json) finds only the reload function changed.
All 21 other case dependency closures and all non-function bytes match the final source.
This comparison supports reuse of their original evidence. It does not create a new execution.
Whole-module hashes differ. The report does not label original runs as final-module executions.

| Case | Mode | Executed source label | Final-source evidence basis | Retained result or current state |
| --- | --- | --- | --- | --- |
| [E2E-01](evidence/expanded-e2e-20261020/case-inventory.json#L64) | `mouse` | [A](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot) | Unchanged case dependency bytes | [Result](evidence/expanded-e2e-20261020/browser/expanded-mouse-20261020T011515/artifacts/result.json); SHA-256 `b994ab04b3a29c9ea42d5c656e59a4ee5b0b2193ccd74cbaf0eb9e506e03ff00` |
| [E2E-02](evidence/expanded-e2e-20261020/case-inventory.json#L146) | `keyboard` | [A](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot) | Unchanged case dependency bytes | [Result](evidence/expanded-e2e-20261020/browser/expanded-keyboard-20261020T011555/artifacts/result.json); SHA-256 `47c41c3a575ea31976ff21a85a3e735a7e886e55c078f34c18c2ef8440eab610` |
| [E2E-03](evidence/expanded-e2e-20261020/case-inventory.json#L228) | `scroll` | [A](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot) | Unchanged case dependency bytes | [Result](evidence/expanded-e2e-20261020/browser/expanded-scroll-20261020T011627/artifacts/result.json); SHA-256 `e891ef27fa895fe5fd0d56770377c08d4313ec668bdbf27481dff90ab6ce5aa3` |
| [E2E-04](evidence/expanded-e2e-20261020/case-inventory.json#L310) | `pending` | [A](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot) | Unchanged case dependency bytes | [Result](evidence/expanded-e2e-20261020/browser/expanded-pending-20261020T011700/artifacts/result.json); SHA-256 `68f4aaa6f10985c0bf599619dfcb7320ca2d2f7d740b61d8db61c971e41d563b` |
| [E2E-05](evidence/expanded-e2e-20261020/case-inventory.json#L402) | `retry` | [A](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot) | Unchanged case dependency bytes | [Result](evidence/expanded-e2e-20261020/browser/expanded-retry-20261020T011812/artifacts/result.json); SHA-256 `71a22fee3cd6723398a1f7191713b977a9cc90e2145ac11e3c646eec7bb20082` |
| [E2E-06](evidence/expanded-e2e-20261020/case-inventory.json#L495) | `cross` | [A](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot) | Unchanged case dependency bytes | [Result](evidence/expanded-e2e-20261020/browser/expanded-cross-20261020T011926/artifacts/result.json); SHA-256 `065656b5121fc6d84f9c8d33f84169fffb5289ffcb997eecea1749ec807eee9c` |
| [E2E-07](evidence/expanded-e2e-20261020/case-inventory.json#L579) | `natural` | [A](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot) | Unchanged case dependency bytes | [Result](evidence/expanded-e2e-20261020/browser/expanded-natural-20261020T011740/artifacts/result.json); SHA-256 `6ede720830b8893b27f262739d4a28c8c437f0a3f597934e75cb5d3623aa0d87` |
| [E2E-08](evidence/expanded-e2e-20261020/case-inventory.json#L680) | `single` | [A](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot) | Unchanged case dependency bytes | [Result](evidence/expanded-e2e-20261020/browser/expanded-single-20261020T012239/artifacts/result.json); SHA-256 `e71b2b1cd01910c1cfa10433669ae8836ec05f74f894b87f497f51e32cf80bae` |
| [E2E-09](evidence/expanded-e2e-20261020/case-inventory.json#L763) | `rapid` | [A](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot) | Unchanged case dependency bytes | [Result](evidence/expanded-e2e-20261020/browser/expanded-rapid-20261020T012705/artifacts/result.json); SHA-256 `3d01c62124c3056972e33a95c2b3c8a3765ca498795677479595eab412e2c95a` |
| [E2E-10](evidence/expanded-e2e-20261020/case-inventory.json#L848) | `keyboardExtend` | [A](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot) | Unchanged case dependency bytes | [Result](evidence/expanded-e2e-20261020/browser/expanded-keyboardExtend-20261020T012816/artifacts/result.json); SHA-256 `cf5ac6ca7be93959b9f2b3754f69f95e39632afec46617e940b64dfe4f66ffe6` |
| [E2E-11](evidence/expanded-e2e-20261020/case-inventory.json#L937) | `activityRetry` | [A](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot) | Unchanged case dependency bytes | [Result](evidence/expanded-e2e-20261020/browser/expanded-activityRetry-20261020T012929/artifacts/result.json); SHA-256 `5ce6f1d48584b14f5284a41ff2ed1900063504282b8794a2d424f74febffc71b` |
| [E2E-12](evidence/expanded-e2e-20261020/case-inventory.json#L1019) | `inconsistent` | [A](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot) | Unchanged case dependency bytes | [Result](evidence/expanded-e2e-20261020/browser/expanded-inconsistent-20261020T012957/artifacts/result.json); SHA-256 `5ace62011c4034925890f65ea36e0887d4adf4d098532d49374501e9599c6aed` |
| [E2E-13](evidence/expanded-e2e-20261020/case-inventory.json#L1108) | `promptActivity` | [A](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot) | Unchanged case dependency bytes | [Result](evidence/expanded-e2e-20261020/browser/expanded-promptActivity-20261020T013027/artifacts/result.json); SHA-256 `44f4a43c0df9c790f8280742de58facfbeb00436a9fc30545a83256fad7535c6` |
| [E2E-14](evidence/expanded-e2e-20261020/case-inventory.json#L1200) | `idleLogout` | [A](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot) | Unchanged case dependency bytes | [Result](evidence/expanded-e2e-20261020/browser/expanded-idleLogout-20261020T013146/artifacts/result.json); SHA-256 `f3790f876aa8dc69b9a344a17b76189e86fdab3c3a18a306d6ad7b0156a82c75` |
| [E2E-15](evidence/expanded-e2e-20261020/case-inventory.json#L1263) | `visibility` | [A](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot) | Unchanged case dependency bytes | [Result](evidence/expanded-e2e-20261020/browser/expanded-visibility-20261020T013251/artifacts/result.json); SHA-256 `fa349bc473de96f30eaacb3fffbf9a6c3815ea7ba41ec50766af35adadc8ce7c` |
| [E2E-16](evidence/expanded-e2e-20261020/case-inventory.json#L1334) | `reload` | [B](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot) | Exact final module | [Result](evidence/expanded-e2e-20261020/browser/expanded-reload-20261020T013558/artifacts/result.json); SHA-256 `295c377538985c188b687c2b7ec81cccb47c4b0432788bce5ba355a16f2efe0f` |
| [E2E-17](evidence/expanded-e2e-20261020/case-inventory.json#L1434) | `manualLogout` | [A](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot) | Unchanged case dependency bytes | [Result](evidence/expanded-e2e-20261020/browser/expanded-manualLogout-20261020T012308/artifacts/result.json); SHA-256 `9cf014c0e60eeae4e33da509a95db74db5dd536c64f6e6d81fcb777273b1fbca` |
| [E2E-18](evidence/expanded-e2e-20261020/case-inventory.json#L1515) | `activityLogout` | [A](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot) | Unchanged case dependency bytes | [Result](evidence/expanded-e2e-20261020/browser/expanded-activityLogout-20261020T012415/artifacts/result.json); SHA-256 `835bcdd279cebb9928259e45af77319c6235f320c7591b61baac43d8cfdda31e` |
| [E2E-19](evidence/expanded-e2e-20261020/case-inventory.json#L1609) | `late` | [A](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot) | Unchanged case dependency bytes | [Result](evidence/expanded-e2e-20261020/browser/expanded-late-20261020T012436/artifacts/result.json); SHA-256 `ea55b28fe22f70bff5925ca0bcc05c2fe7dfe82dd6d037f241569c5bc53bca97` |
| [E2E-20](evidence/expanded-e2e-20261020/case-inventory.json#L1736) | `expired` | [A](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot) | Unchanged case dependency bytes | [Result](evidence/expanded-e2e-20261020/browser/expanded-expired-20261020T012551/artifacts/result.json); SHA-256 `145877432a680bb1fc09683461ce6e522514ca7b47663117632a308a1485dd4b` |
| [E2E-21](evidence/expanded-e2e-20261020/case-inventory.json#L1802) | `missing` | [A](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot) | Unchanged case dependency bytes | [Result](evidence/expanded-e2e-20261020/browser/expanded-missing-20261020T011743/artifacts/result.json); SHA-256 `072faec98485b5d0f7c46afd2a0ab829c76bb17324d40ec3f4085958b600304a` |
| [E2E-22](evidence/expanded-e2e-20261020/case-inventory.json#L1870) | `workspace` | [A](evidence/expanded-e2e-20261020/test-source/sessionRenewal.6de6fe8.8e5797903ed3.cjs.snapshot) | Unchanged case dependency bytes | [Result](evidence/expanded-e2e-20261020/browser/expanded-workspace-20261020T012657/artifacts/result.json); SHA-256 `ff41c3af9e8899d89fbb66b6212f56c7f08ef9e148a4329448f457b098148a96` |

## Retained evidence inventory

| Evidence ID | Locator | SHA-256 | Run identity | Integrity or availability limit |
| --- | --- | --- | --- | --- |
| E-001 | [Stage baseline](evidence/expanded-e2e-20261020/stage-baseline.json) | 20b4e338df3f340508a8a6756d5252fe1caf63917b99bd1ee427c45af8b45577 | Expanded local stage | Records scope and authorization; no release approval. |
| E-002 | [Fixture binding](evidence/expanded-e2e-20261020/fixture-binding.json) | 71d92e582aa9f092976fba62bf94ec169b1df38a458daaa3586b59bd1b1994e6 | Expanded local stage | Local substitutions limit production claims. |
| E-003 | [Case inventory](evidence/expanded-e2e-20261020/case-inventory.json) | 4a9af6e91c2bd6910347ea33e9c8d1bb8f2da6007a39ef176a3ebf983269c813 | Mixed exact revisions; final `7a504c1` | Static mappings link to separate execution evidence. |
| E-004 | [Browser manifest](evidence/expanded-e2e-20261020/browser-manifest.json) | bf27397a7d92a4ca1a2d515312853d34d62f6fda149ce3dbddf59ac8abaa1d3b | EXPANDED-session-browser-20261020 | All 22 cases completed; 25 attempts remain retained. |
| E-005 | [Unit binding](evidence/expanded-e2e-20261020/unit/commit-binding.json) | 5d30acaa83c926b2ce926cd793fc7b7be2fc7d184f6f45fdf6ff59d77597aea3 | Expanded local stage | unknown; matching controlled unit evidence; no browser or release approval. |
| E-006 | [Build review](evidence/expanded-e2e-20261020/build/typecheck-review.json) | 9165b42562fdddbdffe87406a0807d4628854da807b8e51826bd6947340e876d | Expanded local stage | unknown; retained compiler results and isolated proposal check; complete production build absent. |
| E-007 | [Proposed guard patch](evidence/expanded-e2e-20261020/proposed-type-fix.patch) | 2d5c8178ec862fd1d99e6c08a112aa9f2fdac836c6ec3fea66b5cf52044e6e78 | Expanded local stage | unknown; unapplied suggestion; runtime equivalence remains inferred. |
| E-008 | [Release gap review](evidence/expanded-e2e-20261020/release-gap-review.json) | 9bf12f02afbe8b9e622f1deacf46757f3fcf9931a6ccfb114d80741a72b1edd3 | Expanded local stage | unknown; source-backed findings; browser reconciliation and release approval remain separate. |

## Browser evidence bindings

The manifest retains every screenshot and its SHA-256 hash.
The table selects one decisive checkpoint for each completed case.
Result links bind captures to assertions and request evidence.

| Case and step | Capture time and phase | Screenshot or trace | SHA-256 | Assertion or request evidence | Supported claim and limit |
| --- | --- | --- | --- | --- | --- |
| [E2E-01](evidence/expanded-e2e-20261020/case-inventory.json#L64) | 2026-10-20T01:15:53.425Z; after | [Capture](evidence/expanded-e2e-20261020/browser/expanded-mouse-20261020T011515/artifacts/after.png) | e7cff489df4e60222973012775ab8a05db6f05e6b58635c06d143e12783f8e0d | [Result](evidence/expanded-e2e-20261020/browser/expanded-mouse-20261020T011515/artifacts/result.json) | Recorded local predicate only. |
| [E2E-02](evidence/expanded-e2e-20261020/case-inventory.json#L146) | 2026-10-20T01:16:25.524Z; after | [Capture](evidence/expanded-e2e-20261020/browser/expanded-keyboard-20261020T011555/artifacts/after.png) | d124a9b9c8725b7e81aeafbf0626e3b81fdbe82d14e687e0fde1891097397c5d | [Result](evidence/expanded-e2e-20261020/browser/expanded-keyboard-20261020T011555/artifacts/result.json) | Recorded local predicate only. |
| [E2E-03](evidence/expanded-e2e-20261020/case-inventory.json#L228) | 2026-10-20T01:16:58.630Z; after | [Capture](evidence/expanded-e2e-20261020/browser/expanded-scroll-20261020T011627/artifacts/after.png) | d124a9b9c8725b7e81aeafbf0626e3b81fdbe82d14e687e0fde1891097397c5d | [Result](evidence/expanded-e2e-20261020/browser/expanded-scroll-20261020T011627/artifacts/result.json) | Recorded local predicate only. |
| [E2E-04](evidence/expanded-e2e-20261020/case-inventory.json#L310) | 2026-10-20T01:18:03.972Z; pending-prompt | [Capture](evidence/expanded-e2e-20261020/browser/expanded-pending-20261020T011700/artifacts/pending-prompt.png) | 04056f5f65795244c7a1da43fd28221b9c3b37dc530220a7a04dc45fd3ec3eea | [Result](evidence/expanded-e2e-20261020/browser/expanded-pending-20261020T011700/artifacts/result.json) | Recorded local predicate only. |
| [E2E-05](evidence/expanded-e2e-20261020/case-inventory.json#L402) | 2026-10-20T01:19:17.207Z; pending-prompt | [Capture](evidence/expanded-e2e-20261020/browser/expanded-retry-20261020T011812/artifacts/pending-prompt.png) | 42f205c4f189cb1dba93ae68b13a662fd9f19fbd55d41c7bb985cb0655102478 | [Result](evidence/expanded-e2e-20261020/browser/expanded-retry-20261020T011812/artifacts/result.json) | Recorded local predicate only. |
| [E2E-06](evidence/expanded-e2e-20261020/case-inventory.json#L495) | 2026-10-20T01:22:37.037Z; after | [Capture](evidence/expanded-e2e-20261020/browser/expanded-cross-20261020T011926/artifacts/after.png) | d1d28cfc26c7c23d0283e9d04e721280010ca4f097e6b2e5afc301436999acb6 | [Result](evidence/expanded-e2e-20261020/browser/expanded-cross-20261020T011926/artifacts/result.json) | Recorded local predicate only. |
| [E2E-07](evidence/expanded-e2e-20261020/case-inventory.json#L579) | 2026-10-20T01:47:50.225Z; hidden-subject-return | [Capture](evidence/expanded-e2e-20261020/browser/expanded-natural-20261020T011740/artifacts/hidden-subject-return.png) | 693b897ec645a2a368a0dc7705e254f94fc319a0c569f4aa31fd3f7ae27cf17f | [Result](evidence/expanded-e2e-20261020/browser/expanded-natural-20261020T011740/artifacts/result.json) | Freeze flag retained; exact freeze timestamp absent. |
| [E2E-08](evidence/expanded-e2e-20261020/case-inventory.json#L680) | 2026-10-20T01:23:00.014Z; held-activity-request | [Capture](evidence/expanded-e2e-20261020/browser/expanded-single-20261020T012239/artifacts/held-activity-request.png) | 2ff12d56df568b0812157ff0883171b5d78d7bc4ee7b8d5ae95c1240df207d9c | [Result](evidence/expanded-e2e-20261020/browser/expanded-single-20261020T012239/artifacts/result.json) | Recorded local predicate only. |
| [E2E-09](evidence/expanded-e2e-20261020/case-inventory.json#L763) | 2026-10-20T01:28:07.349Z; expired-prompt | [Capture](evidence/expanded-e2e-20261020/browser/expanded-rapid-20261020T012705/artifacts/expired-prompt.png) | 4320fd1cff7a5bb41fc1910c72c620b3d4708fa9d8fb1feca5c98b883360b820 | [Result](evidence/expanded-e2e-20261020/browser/expanded-rapid-20261020T012705/artifacts/result.json) | Recorded local predicate only. |
| [E2E-10](evidence/expanded-e2e-20261020/case-inventory.json#L848) | 2026-10-20T01:29:20.669Z; pending-prompt | [Capture](evidence/expanded-e2e-20261020/browser/expanded-keyboardExtend-20261020T012816/artifacts/pending-prompt.png) | 6dabcd06f6b03bda574a0e50f763157c4279d129481d8cf2163410c201a74ff3 | [Result](evidence/expanded-e2e-20261020/browser/expanded-keyboardExtend-20261020T012816/artifacts/result.json) | Recorded local predicate only. |
| [E2E-11](evidence/expanded-e2e-20261020/case-inventory.json#L937) | 2026-10-20T01:29:55.832Z; after | [Capture](evidence/expanded-e2e-20261020/browser/expanded-activityRetry-20261020T012929/artifacts/after.png) | 47c13864dff99fdb032700f4eaff3d8ba118036ad561e0ea602a0d6c90c6bc61 | [Result](evidence/expanded-e2e-20261020/browser/expanded-activityRetry-20261020T012929/artifacts/result.json) | Recorded local predicate only. |
| [E2E-12](evidence/expanded-e2e-20261020/case-inventory.json#L1019) | 2026-10-20T01:30:25.075Z; after | [Capture](evidence/expanded-e2e-20261020/browser/expanded-inconsistent-20261020T012957/artifacts/after.png) | 561fd887f67124bba9cfd70b161d48bc4139b374538b83a19954e0ee85153d69 | [Result](evidence/expanded-e2e-20261020/browser/expanded-inconsistent-20261020T012957/artifacts/result.json) | Recorded local predicate only. |
| [E2E-13](evidence/expanded-e2e-20261020/case-inventory.json#L1108) | 2026-10-20T01:31:37.763Z; pending-prompt | [Capture](evidence/expanded-e2e-20261020/browser/expanded-promptActivity-20261020T013027/artifacts/pending-prompt.png) | 90847a1001c39ce80468766d2fb422cad0e3ea9156ad55b1a52ef8ff2a667945 | [Result](evidence/expanded-e2e-20261020/browser/expanded-promptActivity-20261020T013027/artifacts/result.json) | Recorded local predicate only. |
| [E2E-14](evidence/expanded-e2e-20261020/case-inventory.json#L1200) | 2026-10-20T01:32:48.200Z; expired-prompt | [Capture](evidence/expanded-e2e-20261020/browser/expanded-idleLogout-20261020T013146/artifacts/expired-prompt.png) | 42dd382d7ee0d2ce0dd8b7975fed9460fb690c6084e8a012a6ad5cbf277e1e97 | [Result](evidence/expanded-e2e-20261020/browser/expanded-idleLogout-20261020T013146/artifacts/result.json) | Recorded local predicate only. |
| [E2E-15](evidence/expanded-e2e-20261020/case-inventory.json#L1263) | 2026-10-20T01:33:08.490Z; after | [Capture](evidence/expanded-e2e-20261020/browser/expanded-visibility-20261020T013251/artifacts/after.png) | a08241c4933c611b7015003e62d60743626c52cedf4ec3465ca176dc1adda73d | [Result](evidence/expanded-e2e-20261020/browser/expanded-visibility-20261020T013251/artifacts/result.json) | Recorded local predicate only. |
| [E2E-16](evidence/expanded-e2e-20261020/case-inventory.json#L1334) | 2026-10-20T01:36:20.460Z; after | [Capture](evidence/expanded-e2e-20261020/browser/expanded-reload-20261020T013558/artifacts/after.png) | fee4ecd18e3d1a6de8b7e5338fb351ffcb3e8869017ce7df9aad349d3a2eb004 | [Result](evidence/expanded-e2e-20261020/browser/expanded-reload-20261020T013558/artifacts/result.json) | Recorded local predicate only. |
| [E2E-17](evidence/expanded-e2e-20261020/case-inventory.json#L1434) | 2026-10-20T01:24:10.152Z; expired-prompt | [Capture](evidence/expanded-e2e-20261020/browser/expanded-manualLogout-20261020T012308/artifacts/expired-prompt.png) | e990dc234ef0d733304051b27402e70714775a544dd5e4c77c1c8668bf37567e | [Result](evidence/expanded-e2e-20261020/browser/expanded-manualLogout-20261020T012308/artifacts/result.json) | Recorded local predicate only. |
| [E2E-18](evidence/expanded-e2e-20261020/case-inventory.json#L1515) | 2026-10-20T01:24:32.951Z; home-unmounted | [Capture](evidence/expanded-e2e-20261020/browser/expanded-activityLogout-20261020T012415/artifacts/home-unmounted.png) | b42f85cbc98f2a38a5181fcbaa6d46c670df143ac49b3974e8325c453a5ee169 | [Result](evidence/expanded-e2e-20261020/browser/expanded-activityLogout-20261020T012415/artifacts/result.json) | Recorded local predicate only. |
| [E2E-19](evidence/expanded-e2e-20261020/case-inventory.json#L1609) | 2026-10-20T01:25:41.703Z; pending-prompt | [Capture](evidence/expanded-e2e-20261020/browser/expanded-late-20261020T012436/artifacts/pending-prompt.png) | 08c58287679fcb4daf07d6342c6566f30879978d250ebbf3a1b198a7ce65f85b | [Result](evidence/expanded-e2e-20261020/browser/expanded-late-20261020T012436/artifacts/result.json) | Recorded local predicate only. |
| [E2E-20](evidence/expanded-e2e-20261020/case-inventory.json#L1736) | 2026-10-20T01:26:55.523Z; after | [Capture](evidence/expanded-e2e-20261020/browser/expanded-expired-20261020T012551/artifacts/after.png) | 945df48a44b769d8fe95e9d11b143c7e96aaab6b442a04e2bb07402f54ee2825 | [Result](evidence/expanded-e2e-20261020/browser/expanded-expired-20261020T012551/artifacts/result.json) | Recorded local predicate only. |
| [E2E-21](evidence/expanded-e2e-20261020/case-inventory.json#L1802) | 2026-10-20T01:47:55.026Z; missing-refresh-return | [Capture](evidence/expanded-e2e-20261020/browser/expanded-missing-20261020T011743/artifacts/missing-refresh-return.png) | ba6fc2a2826d9545fa4770865d63933fc74cfd411f3bc17f13b200353a677dbc | [Result](evidence/expanded-e2e-20261020/browser/expanded-missing-20261020T011743/artifacts/result.json) | Full subject freeze/resume events retained; recovery policy unresolved. |
| [E2E-22](evidence/expanded-e2e-20261020/case-inventory.json#L1870) | 2026-10-20T01:27:01.035Z; workspaces-before-logout | [Capture](evidence/expanded-e2e-20261020/browser/expanded-workspace-20261020T012657/artifacts/workspaces-before-logout.png) | c044f58ae27f46b21ab769a9bbf342c1886a4c92bcf8479fb643c8ede4c389bd | [Result](evidence/expanded-e2e-20261020/browser/expanded-workspace-20261020T012657/artifacts/result.json) | Recorded local predicate only. |

Failed attempts remain in the manifest and evidence tree.
All final case captures and results are retained.

## Natural lifecycle evidence limits

Natural recovery recorded `hiddenElapsedMs: 1800016` and `freezeObserved: true`.
The visible idle control expired. Pending renewal closed zero prompts; successful completion closed exactly once.
Protected authentication validation returned HTTP `200`.
Protected navigation then reloaded the subject and replaced `result.lifecycle` with new-document events.
The freeze flag remains retained. The exact natural freeze timestamp and pre-return subject event array are absent.
This result does not provide a paired raw lifecycle trace.

The missing-refresh observation recorded `elapsedMs: 1802220` and `freezeObserved: true`.
It retained one blocked acquisition, no observed refresh, no retained access, and visible sign-in on return.
Its nested observation retains complete subject freeze and resume events.
The freeze event occurred at `2026-10-20T01:32:53.232Z`.
The resume event occurred at `2026-10-20T01:47:53.511Z`.
This remains observation-only because the absent-credential recovery policy is unresolved.

## Automated validation

Artifact lint passed with four warnings.
The warnings preserve unknown ownership, pending business review, unresolved content, and pending ASD review.
The [earlier report validation](evidence/expanded-e2e-20261020/final-report-validation.json) retains checks for the pre-consolidation report.
The [consolidation checks](evidence/report-consolidation-validation-20261020.json) bind the earlier report version 2.
The [reference checks](evidence/reference-link-validation-20261020.json) bind current version 3 and validate its exact definition links.
These checks establish authoring structure only.
They grant no business approval, production readiness, or full ASD compliance.

## Verification conclusion

- Behavior claim: Nineteen local predicates passed. One diagnostic passed and two observations completed.
- Completed behavior: Natural recovery passed its scoped predicates. Missing-refresh return remains observation-only. Unit execution passed within controlled limits.
- Release consequence: Go-live remains on hold for introduced type errors, unavailable build configuration, and unresolved integration evidence.
- Covered conditions: Static inspection maps all 22 cases to source assertions and fixture limits.
- Uncovered conditions: Production deployment, provider revocation, cross-origin activity, and populated application-edit retention remain outside accepted coverage.
- Evidence limits: Natural recovery retains a freeze flag without its exact freeze timestamp. Local fixtures and mixed executed revisions remain explicit.

## Facts, inferences, and unresolved questions

- Facts: The committed suite declares 22 cases and 21 exported functions, including session setup.
- Facts: The inventory preserves seven original cases, seven prior additions, and eight current additions.
- Facts: Reload checks access persistence and refresh reacquisition. Refresh credentials remain memory-only.
- Inferences: The reconciled interaction and race results improve local confidence within the stated fixture limits.
- Facts: Unit results match `4cddb38`. Current typecheck has two introduced errors and two reproduced baseline test errors.
- Inferences: The proposed existence guard appears to preserve runtime behavior. Only isolated typechecking exercised that proposal.
- Unknowns: Production applicability, absent-credential recovery, workspace-edit retention, and accountable owners remain unresolved.

## Findings

The [release gap review](evidence/expanded-e2e-20261020/release-gap-review.json) retains exact source locators, hashes, and review limits.
All nine release findings remain open.
All 22 browser outcomes are bound. The 25 attempts retain three historical harness failures.

| Finding and evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| [RG-001](evidence/expanded-e2e-20261020/release-gap-review.json#L42), P1: [Fixture binding](evidence/expanded-e2e-20261020/fixture-binding.json) lacks production deployment identities and replaces integration adapters. | Local results cannot establish production provider, gateway, toolkit, or embedded application behavior. | unknown: environment owner | Bind deployed revisions and settings. Execute representative environment cases. |
| [RG-002](evidence/expanded-e2e-20261020/release-gap-review.json#L62), P2: Review sources [storage](evidence/expanded-e2e-20261020/release-gap-review.json#L272), [provider](evidence/expanded-e2e-20261020/release-gap-review.json#L283), and [persist](evidence/expanded-e2e-20261020/release-gap-review.json#L294) show separate reducer state and shared access storage. | Concurrent tabs could retain inconsistent sessions. No failure was reproduced. | unknown: session policy owner | Confirm tab policy. Test concurrent renewal, logout, and reload within one context. |
| [RG-003](evidence/expanded-e2e-20261020/release-gap-review.json#L88), P2: Review sources [shared](evidence/expanded-e2e-20261020/release-gap-review.json#L316), [cashflow](evidence/expanded-e2e-20261020/release-gap-review.json#L327), and [ratan](evidence/expanded-e2e-20261020/release-gap-review.json#L338) show application queries can call extension outside Home checks. | Embedded background traffic could change idle observations. Consumer revisions and deployed behavior remain unknown. | unknown: integration owner | Confirm eligible activity. Test representative visible-idle and hidden application traffic. |
| [RG-004](evidence/expanded-e2e-20261020/release-gap-review.json#L114), P2: The configured protected operation validates portal authentication only. | Portal renewal does not establish downstream business authorization or query success. | unknown: application test owner | Configure an inspected read-only application operation. Assert its response and renewed request credential. |
| [RG-005](evidence/expanded-e2e-20261020/release-gap-review.json#L134), P2: Retry uses transport aborts. Denial uses natural expiry. Provider adapters remain synthetic. | These fixtures do not establish provider refusal or revocation behavior. | unknown: authentication owner | Obtain an authorized provider fixture. Assert agreed refusal, revocation, and recovery outcomes. |
| [RG-006](evidence/expanded-e2e-20261020/release-gap-review.json#L156), P2: [TC-04](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L266) retains [O-001](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L136). [TC-07](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L269) retains [O-004](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L138) and empty workspace descriptors. | Observations cannot establish recovery acceptance or application-edit retention. | unknown: business owner | Resolve both policies. Define expected outcomes and populated application fixtures. |
| [RG-007](evidence/expanded-e2e-20261020/release-gap-review.json#L177), P3: Requirement version 4 and Home bindings cover mouse movement, keyboard input, and captured scroll. | Click-only and touch-only eligibility remain scope questions. No criterion violation was demonstrated. | unknown: input policy owner | Confirm supported input types before adding acceptance cases or changing bindings. |
| [RG-008](evidence/expanded-e2e-20261020/release-gap-review.json#L200), P3: The timeout controller schedules logout two seconds before refresh expiry. | Slow renewal near that inherited boundary could lose its final response window. | unknown: session policy owner | Confirm the early-logout policy. Add boundary assertions before changing it. |
| [RG-009](evidence/expanded-e2e-20261020/release-gap-review.json#L220), P1: [Typecheck review](evidence/expanded-e2e-20261020/build/typecheck-review.json) confirms two introduced guard errors and two reproduced baseline test errors. | The selected revision lacks a passing declared typecheck. Browser results cannot establish production build success. | unknown: application owner | Review the [unapplied patch](evidence/expanded-e2e-20261020/proposed-type-fix.patch). Resolve baseline typing and complete the configured build. |
| Natural recovery retained its freeze flag after protected navigation replaced the subject lifecycle array. | The exact natural freeze timestamp is unavailable. | unknown: session test owner | Preserve pre-navigation lifecycle snapshots in later investigations. |
| The negative response body with valid access header lacks a confirmed deployed contract. | Diagnostic failure alone cannot establish a production defect. | unknown: authentication owner | Confirm the response contract before interpreting that outcome. |

## Sources

| Source ID | Locator | Exact revision | SHA-256 | Owner, authority, and limits |
| --- | --- | --- | --- | --- |
| SRC-session-expanded-stage-20261020 | [Stage baseline](evidence/expanded-e2e-20261020/stage-baseline.json) | Local stage, 20 October 2026 | 20b4e338df3f340508a8a6756d5252fe1caf63917b99bd1ee427c45af8b45577 | unknown; retained direct user scope; no release approval. |
| SRC-session-expanded-tests-20261020 | [Final test snapshot](evidence/expanded-e2e-20261020/test-source/sessionRenewal.7a504c1.94db4519b1d8.cjs.snapshot) | 7a504c13a8d51bb52af5cc89bd4af88d1988da94 | 94db4519b1d8e2f3669eeea6df59b7a4242300e797f53d28fb2e3152c689e984 | unknown; final reviewed source. Individual executions retain their actual source label. |
| SRC-session-expanded-fixture-20261020 | [Fixture binding](evidence/expanded-e2e-20261020/fixture-binding.json) | 9dcf201dc5ba3890bb527e750defb78e5f9dc75c | 71d92e582aa9f092976fba62bf94ec169b1df38a458daaa3586b59bd1b1994e6 | unknown; local source and fixture binding; no deployed production identity. |
| SRC-session-review-intent-v4 | [Requirement version 4](../../knowledge/candidates/requirements/REQ-active-session-renewal.md) | Version 4 | 828d62209f11dd9bb9dee893ddc80e7e5d4dc6abd3c58170e902dab61bc587aa | unknown; documented intent; publication review remains pending. |
| SRC-session-expanded-unit-20261020 | [Unit binding](evidence/expanded-e2e-20261020/unit/commit-binding.json) | 4cddb38dc0e3117708fea00bdbb886f7b4b3d5c5 | 5d30acaa83c926b2ce926cd793fc7b7be2fc7d184f6f45fdf6ff59d77597aea3 | unknown; matching controlled unit evidence; no browser or release approval. |
| SRC-session-expanded-build-20261020 | [Build review](evidence/expanded-e2e-20261020/build/typecheck-review.json) | 4cddb38dc0e3117708fea00bdbb886f7b4b3d5c5 | 9165b42562fdddbdffe87406a0807d4628854da807b8e51826bd6947340e876d | unknown; retained compiler results and isolated proposal check; complete production build absent. |
| SRC-session-expanded-proposal-20261020 | [Proposed guard patch](evidence/expanded-e2e-20261020/proposed-type-fix.patch) | Proposal against 4cddb38 | 2d5c8178ec862fd1d99e6c08a112aa9f2fdac836c6ec3fea66b5cf52044e6e78 | unknown; unapplied suggestion; runtime equivalence remains inferred. |
| SRC-session-expanded-release-gaps-20261020 | [Release gap review](evidence/expanded-e2e-20261020/release-gap-review.json) | Source review at 4cddb38; tests 6de6fe8 | 9bf12f02afbe8b9e622f1deacf46757f3fcf9931a6ccfb114d80741a72b1edd3 | unknown; source-backed findings; browser reconciliation and release approval remain separate. |
| SRC-session-expanded-browser-20261020 | [Browser manifest](evidence/expanded-e2e-20261020/browser-manifest.json) | Current expanded execution | bf27397a7d92a4ca1a2d515312853d34d62f6fda149ce3dbddf59ac8abaa1d3b | unknown; all 22 outcomes complete; local and policy limits remain explicit. |
| SRC-session-expanded-equivalence-20261020 | [Dependency equivalence](evidence/expanded-e2e-20261020/source-dependency-equivalence.json) | 6de6fe8abfe67541bd207433689f86102a0e44ad to 7a504c13a8d51bb52af5cc89bd4af88d1988da94 | f87802519026667db7131aadf6234c637f342c2d25154622a499512188d2c566 | unknown; exact source and function-closure comparison; no new execution. |
| SRC-session-expanded-validate-contract-20261020 | [BFF validation](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L245) | 85d7cc03eb12710d6facf581987fd4ae24fc9844 | b71df7273263aa8c17b8ea58e9e727008b108ec51ffdc70e266207ed07efad4a | unknown; validation calls token-generating buildEntities at line 94. Deployment remains unknown. |
| SRC-session-expanded-frontend-handler-20261020 | [Frontend response handler](../../repos/ui/mfe-base/src/hooks/service/util/succes.response.handler.ts) | 4cddb38dc0e3117708fea00bdbb886f7b4b3d5c5 | e7fe28d721e1a3200b7a9978c264d52c7c96b3a5299978fca16b202a78b3fd88 | unknown; inspected token installation path; runtime source matches browser revision. |
| SRC-session-expanded-frontend-login-20261020 | [Authorization helpers](../../repos/ui/mfe-base/src/utils/login.ts) | 4cddb38dc0e3117708fea00bdbb886f7b4b3d5c5 | 364c29cab3c107b14e2a914e27c38bd7073a271811c67071fa8d8f1bed738730 | unknown; inspected token installation path; runtime source matches browser revision. |

## Earlier 14-case execution

This section preserves the earlier report's execution identity and distinct results.
The earlier inventory contains 12 passing local predicates and two observations.
All 14 native runs and result records have machine status `PASSED`.
[TC-04](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L266) and [TC-07](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L269) remain `OBSERVATION_ONLY`; their machine status does not establish business acceptance.
These results belong to their historical revisions, not the current 22-case execution.

| Provenance field | Historical value |
| --- | --- |
| Report identity | `EXEC-session-renewal-browser-20261020`, version `1`. |
| Report Git revision | `3ef6e1b18401acda32ca292c80b6fa031567ca8e`. |
| Original report SHA-256 | `d8cc08d59318589f717fb33bd7b00972c00025b75d0ed5c02b747b51817d0675`. |
| Execution identity | `native-edge-post-change-20261020`. |
| Recorded execution window | `2026-10-19T19:04:57Z` through `2026-10-19T20:18:38Z`. |
| Recorded command | `.workbench/session-post-change-20261020/browser-runner.mjs`. |
| Recorded exit status | `0`. |
| Test repository revision | `66595b84e2ed8c78ff1a74f1e1fc0afc856d33af`. |
| Test module SHA-256 | `41d3ee444936039f1ec09cdca12bee8a3fdca5d25d2c5ec741c753e5c43a8b3a`. |
| MFE revision | `4da985a9fa302d7f1ecc04a81b2924b49410ce6a`. |
| BFF revision | `85d7cc03eb12710d6facf581987fd4ae24fc9844`. |
| Inventory | Seven original suite cases and seven additions; all 14 have retained results. |
| Evidence manifest | [Historical manifest](evidence/post-change-review-20261020/browser-execution/final/manifest.json). |
| Manifest SHA-256 | `75ddf4bde85430d78d67e0e1de11bc739a7ead32a7c85ea76fdae441942b570d`. |

### Historical outcomes

The manifest records matching source hashes and result artifacts for every historical case.
Each result directory also retains native run metadata and screenshots.

| Case | Distinct actual result | Verification outcome | Retained result |
| --- | --- | --- | --- |
| [AC-1](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L137-L140) mouse | 144 trusted events; two successful renewals. | PASSED | [Mouse](evidence/post-change-review-20261020/browser-execution/final/mouse-final/result-artifacts/result.json) |
| [AC-2](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L144-L147) keyboard | 138 trusted events; two successful renewals. | PASSED | [Keyboard](evidence/post-change-review-20261020/browser-execution/final/keyboard-final/result-artifacts/result.json) |
| [AC-3](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L151-L154) scroll | 145 trusted events; two successful renewals. | PASSED | [Scroll](evidence/post-change-review-20261020/browser-execution/final/scroll-final/result-artifacts/result.json) |
| [AC-4](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L158-L162) live boundary | 186,356 milliseconds; 18 renewals; replacement refresh; zero additional login, navigation, or prompt events. | PASSED | [Refresh boundary](evidence/post-change-review-20261020/browser-execution/final/cross-1/result-artifacts/result.json) |
| [TC-01](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L263), [AC-5](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L166-L169), [AC-6](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L173-L176) | Zero pending closures; exactly one successful completion closure. | PASSED | [Pending renewal](evidence/post-change-review-20261020/browser-execution/final/pending-fast-001/result-artifacts/result.json) |
| [TC-02](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L264), [AC-7](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L180-L183) | Controlled transport failure preserved retry and zero closures. Actual retry completed with one closure. | PASSED | [Retry](evidence/post-change-review-20261020/browser-execution/final/retry-fast-001/result-artifacts/result.json) |
| [TC-03](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L265), [TC-06](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L268) | Hidden time reached 1,800,058 milliseconds; freeze flag true; manual renewal completed with one closure. | PASSED | [Natural background](evidence/post-change-review-20261020/browser-execution/final/natural-edge-final-001/result-artifacts/result.json) |
| Slow activity sharing | 115 inputs shared one held request with zero cancellations. | PASSED | [Single flight](evidence/post-change-review-20261020/browser-execution/final/single-fast-002/result-artifacts/result.json) |
| Manual logout cancellation | Browser relogin cancelled. Late success restored no access. | PASSED | [Manual logout](evidence/post-change-review-20261020/browser-execution/final/manual-logout-final/result-artifacts/result.json) |
| Home unmount cancellation | Logout unmounted Home and cancelled extension. Late success restored no access. | PASSED | [Activity logout](evidence/post-change-review-20261020/browser-execution/final/activity-logout-final/result-artifacts/result.json) |
| Late activity response | Stale activity cancelled; manual token preserved; one completion closure. | PASSED | [Late response](evidence/post-change-review-20261020/browser-execution/final/late-final/result-artifacts/result.json) |
| [TC-05](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L267) expired access | Initial validation returned HTTP `200`. Naturally expired replay returned HTTP `401`. | PASSED | [Expiry denial](evidence/post-change-review-20261020/browser-execution/final/expired-fast-001/result-artifacts/result.json) |
| [TC-04](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L266) missing refresh | After 1,801,751 milliseconds, one acquisition was blocked; no refresh or access remained; sign-in was visible; freeze flag true. | OBSERVATION_ONLY | [Missing refresh](evidence/post-change-review-20261020/browser-execution/final/missing-edge-final-001/result-artifacts/result.json) |
| [TC-07](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L269) workspace descriptors | Two empty workspace descriptors and entitlements matched after same-user sign-in. | OBSERVATION_ONLY | [Workspace observation](evidence/post-change-review-20261020/browser-execution/final/workspace-final/result-artifacts/result.json) |

### Historical environment and evidence limits

Native Microsoft Edge `155.0.4283.62` used fresh macOS profiles and CDP `noDefaults=true`.
Launch arguments disabled first-run, sync, updater, and background networking.
The recorded fast portal used `127.0.0.1:8103`; its BFF used `127.0.0.1:8091`.
Fast access and refresh lifetimes were 60 and 144 seconds.
Natural cases used real wall-clock time without clock overrides or page heartbeats during their hidden intervals.
Route holds and transport failures remained disclosed test controls.

Protected validation checked `/api/auth/v2/sso/validate`, including HTTP success, `result=true`, and the request credential hash.
It did not establish downstream business authorization or production deployment behavior.
The short [AC-4](https://github.com/lushevol/sdlc-workbench/blob/d6adcff452f1329d99528f0f7e8a6450a27ddc8c/knowledge/candidates/requirements/REQ-active-session-renewal.md#L158-L162) browser boundary did not replace the controlled four-hour criterion or prove indefinite renewal.
[TC-04](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L266) had no accepted absent-credential recovery outcome.
[TC-07](https://github.com/lushevol/sdlc-workbench/blob/cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c/tasks/portal-background-session-20261019/intake.md#L269) did not cover populated application parameters or application-edit retention.
Owners and business review remained unresolved.

The historical natural result retains `freezeObserved: true`.
Its final `result.lifecycle.events` contains only a later `pageshow` event.
The exact natural freeze timestamp and pre-return subject event array are absent.
The freeze flag must not be described as a complete retained raw lifecycle trace.

### Preserved historical source identities

| Source ID | Locator | Revision or hash | Authority and limit |
| --- | --- | --- | --- |
| `SRC-session-browser-final-manifest-20261020` | [Historical browser manifest](evidence/post-change-review-20261020/browser-execution/final/manifest.json) | Test `66595b84e2ed8c78ff1a74f1e1fc0afc856d33af`; manifest SHA-256 above. | Local browser results. Two observations establish no policy acceptance. |
| `SRC-session-e2e-final-20261020` | `repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/sessionRenewal.cjs` at historical revision. | Revision `66595b84e2ed8c78ff1a74f1e1fc0afc856d33af`; source SHA-256 above. | Historical executable assertions. Current checkout bytes differ. |
| `SRC-session-stage-baseline-20261020` | [Historical stage baseline](evidence/post-change-review-20261020/stage-baseline.json) | Stage SHA-256 `2ae44cdf8ecbd7c91e3d5645fe2f90925544093fa807697b4739972f2d689b34`. | Frozen intake revision `cfcc2be`; intake SHA-256 `1650a20f8a2aba2105b30b8abc4bd2a881f58ee335925a3daa9f6a6c0d0e0948`. |
