---
artifact_kind: test-execution-report
id: EXEC-session-active-cutoff-fix-20261024
version: 3
status: draft
owner: unknown
source_refs:
  - SRC-session-active-cutoff-fix-request-20261024
  - SRC-session-active-cutoff-fix-inputs-20261024
related_ids:
  - REQ-active-session-renewal
  - CHANGE-session-post-review-20261020
  - TEST-session-canonical-20261021
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

# Issue 1 correction: original E2E comparison

> **E2E-06 changed from FAILED to PASSED. Complete the remaining comparison.**
> Action: finish the two pending background cases.
> Consequence: the fixed candidate passes the refresh-boundary assertions. PROD readiness remains blocked.
> Owner: Codex for local verification; unknown release owner for PROD evidence.
> Evidence: [candidate result](evidence/active-cutoff-fix-20261024/browser/cutoff-cross-20261024T234223/artifacts/result.json) and [progress](evidence/active-cutoff-fix-20261024/progress.json).

## Run identity and provenance

The [high-priority request](evidence/active-cutoff-fix-20261024/user-request.txt) authorizes issue 1 correction and E2E reruns.
The [continuation request](evidence/active-cutoff-fix-20261024/setup/continuation-20261025.json) requests continued execution within that scope.
The [stage inputs](evidence/active-cutoff-fix-20261024/inputs.json) record scoped readiness, baseline identities, and unrelated changes.
No business clarification or knowledge policy changed. No deployment occurred.

| Identity | Value and evidence |
| --- | --- |
| Application | `mfe-base`; candidate `ae8213f2963047e7c126d01f4003cee1236abc25`, base `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85`. [Commit binding](evidence/active-cutoff-fix-20261024/commit-binding.json). |
| Executed bytes | [All source hashes](evidence/active-cutoff-fix-20261024/setup/source-binding.json) and [served-source validation](evidence/active-cutoff-fix-20261024/setup/runtime-readiness.json). |
| Requirement | [Candidate version 4](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria); publication review remains pending. |
| Browser assertions | Original test revision `7a504c13a8d51bb52af5cc89bd4af88d1988da94`; SHA-256 `94db4519b1d8e2f3669eeea6df59b7a4242300e797f53d28fb2e3152c689e984`. |
| Baseline browser runtime | `6d4c37c839b99d14ea41fd936da1a36cda526b17`; relevant runtime matches the pre-fix application. |
| Browser | Native Microsoft Edge `156.0.4314.42`; isolated profiles and native default contexts through CDP. |
| Invocation | [Retained launcher](evidence/active-cutoff-fix-20261024/setup/run-expanded.py.snapshot) and [browser driver](evidence/active-cutoff-fix-20261024/setup/browser-runner.mjs.snapshot). |
| Execution | `RUNNING`; 20 valid scoped results and two pending cases. [Checkpoint](evidence/active-cutoff-fix-20261024/progress.json). |

The unchanged runner configuration records the pre-fix base in `sourceRevisions`.
The saved source and commit bindings identify the actual executed candidate bytes.

## Correction and impact

The Home controller previously opened Timeout when either access or refresh expired.
Timeout could then start logout despite usable access.
The correction opens Timeout at access expiry. Expired refresh credentials instead trigger replacement while access remains usable.
The existing service deduplicates acquisition for the same access token.
Access expiry and server access validation remain effective.

Business impact: active users can continue working across the original refresh deadline under the corrected conditions.
System impact: Home expiry reconciliation can issue replacement acquisition through the existing BFF endpoint.
The change adds no endpoint, dependency, configuration value, or storage contract.
Risk is medium because Home timers and authentication state serve active and idle paths.
The [focused review](evidence/active-cutoff-fix-20261024/review.json) found no new actionable defect in the selected patch.
Its machine outcome remains `INCOMPLETE` because review excludes a preexisting compiler cache.

## Browser environment and suite completeness

The [complete inventory](evidence/active-cutoff-fix-20261024/case-inventory.json) retains all 22 original definitions, assertions, and historical result hashes.
Native browser modes run sequentially to preserve foreground and hidden conditions.
The natural and missing-refresh modes each require 1,800 real seconds.
Fast cases use one-minute access and refresh expiry at two minutes plus 24 seconds.
Natural cases use 15-minute access and refresh expiry at 225 minutes plus 24 seconds.

The local BFF executes actual controller, JWT, session, and JPA paths with isolated H2 storage.
Identity and entitlement dependencies use local fixtures. The frontend uses existing toolkit presentation substitutes.
CDP and instrumentation can affect browser lifecycle. Only recorded visibility and freeze events establish observed transitions.
Local execution does not establish UAT or PROD parity.
Historical cases used Edge `155.0.4283.62`. Current cases use Edge `156.0.4314.42`.
Historical natural, missing-refresh, and fast runs overlapped. Current native runs execute sequentially.
These differences limit causal attribution from historical status transitions alone.
A separate same-browser baseline control tests issue 1 with the original Home code.
Its first attempt failed the required visibility setup. The [fresh same-browser baseline](evidence/active-cutoff-fix-20261024/counterfactual/browser/baseline-cross-20261024T234541/artifacts/result.json) fails validly with the original Home code.
It opens Timeout at refresh expiry while renewed access still has 51 seconds remaining.
The [fixed candidate](evidence/active-cutoff-fix-20261024/browser/cutoff-cross-20261024T234223/artifacts/result.json) completes eighteen renewals and replaces the refresh credential.
The total assertion elapsed time is 186,376 milliseconds, including protected validation.
The preceding activity window records zero Timeout openings, extra logins, or main-frame navigations.
The later protected-validation step navigates deliberately and returns HTTP 200 with `result=true`.
Both runs use Edge `156.0.4314.42` and unchanged assertions.

The [prior visibility investigation](evidence/active-cutoff-fix-20261024/setup/visibility-investigation.json) recorded a locked Mac.
The [prior native recheck](evidence/active-cutoff-fix-20261024/setup/native-ui-recheck.json) returned the same lock error.
The [continuation preflight](evidence/active-cutoff-fix-20261024/setup/visibility-preflight.json) now confirms explicit OS unlock and genuine tab visibility.
The [service check](evidence/active-cutoff-fix-20261024/setup/resume-service-check-20261025.json) confirms current source bindings and healthy local services.
The prior lock's effect on earlier tab transitions remains an inference. The lock onset time is unknown.
The natural attempt completed 1,800,046 elapsed milliseconds, but its visible control became hidden.
A profile-cleanup error then masked the original assertion. That attempt supplies no business verdict.
Both initial refresh-boundary attempts failed the required hidden-tab setup. Neither reached the expiry assertion.
Their raw results remain unchanged. Derived comparison metadata marks these attempts invalid.

The [locked-screen scope review](evidence/active-cutoff-fix-20261024/setup/locked-mac-case-scope.json) permits eleven independent DOM and service checks.
Those cases use original assertions, actual HTTP responses, controlled input, and real elapsed time.
Their results establish the asserted DOM and service predicates only. They establish no physical-screen or browser-lifecycle behavior.
Two background cases remain: [E2E-07](06-test-cases.md#e2e-07) and [E2E-21](06-test-cases.md#e2e-21).

The [cleanup correction](evidence/active-cutoff-fix-20261024/setup/driver-cleanup-change.json) adds bounded profile-removal retries.
It changes the browser driver only. The original business assertions remain unchanged.
The [result safeguard](evidence/active-cutoff-fix-20261024/setup/natural-control-validity-regression.json) rejects hidden visible controls regardless of cleanup status.
This safeguard changes result classification. It preserves raw results and invalid attempts.
The [visibility safeguard](evidence/active-cutoff-fix-20261024/setup/visibility-setup-validity-regression-20261025.json) also excludes unambiguous visibility setup timeouts.
It preserves reload token-install failures as business failures. That site has a different assertion purpose.

## Assertions and outcomes

Each case below links its canonical Gherkin definition. The inventory separately links exact executable assertions and prior results.
Candidate outcomes use retained results. Invalid setup comparisons require a separate valid rerun.
Diagnostic and observation outcomes remain outside business pass counts.
The current inventory has twelve business failures, six business passes, one diagnostic failure, and one observation.
[E2E-06](06-test-cases.md#e2e-06) changed from failed to passed. The same-browser original-Home control still fails.
One selected invalid candidate attempt and one running background case form the two pending cases.

| Case | Purpose | Before | Candidate | Evidence |
| --- | --- | --- | --- | --- |
| [E2E-01](06-test-cases.md#e2e-01) | AC-1 Continuous Mouse Activity Renews The Session | FAILED | FAILED | [Retained attempt](evidence/active-cutoff-fix-20261024/browser/cutoff-mouse-20261024T155628/artifacts/result.json) |
| [E2E-02](06-test-cases.md#e2e-02) | AC-2 Continuous Keyboard Activity Renews The Session | FAILED | FAILED | [Retained attempt](evidence/active-cutoff-fix-20261024/browser/cutoff-keyboard-20261024T155659/artifacts/result.json) |
| [E2E-03](06-test-cases.md#e2e-03) | AC-3 Continuous Scroll Activity Renews The Session | FAILED | FAILED | [Retained attempt](evidence/active-cutoff-fix-20261024/browser/cutoff-scroll-20261024T155731/artifacts/result.json) |
| [E2E-04](06-test-cases.md#e2e-04) | AC-5 And AC-6 Pending Renewal Closes Only After Success | FAILED | FAILED | [Retained attempt](evidence/active-cutoff-fix-20261024/browser/cutoff-pending-20261024T155803/artifacts/result.json) |
| [E2E-05](06-test-cases.md#e2e-05) | AC-7 Rejected Renewal Permits A Successful Retry | FAILED | FAILED | [Retained attempt](evidence/active-cutoff-fix-20261024/browser/cutoff-retry-20261024T155915/artifacts/result.json) |
| [E2E-06](06-test-cases.md#e2e-06) | Continuous Activity Crosses The Initial Refresh Expiry | FAILED | PASSED | [Retained result](evidence/active-cutoff-fix-20261024/browser/cutoff-cross-20261024T234223/artifacts/result.json) |
| [E2E-07](06-test-cases.md#e2e-07) | Hidden And Visible Sessions Recover After Natural Background Time | FAILED | EXECUTION_ERROR | [Retained attempt](evidence/active-cutoff-fix-20261024/browser/cutoff-natural-20261024T152518/artifacts/result.json) |
| [E2E-08](06-test-cases.md#e2e-08) | Repeated Activity Shares One Slow Extension Request | FAILED | FAILED | [Retained attempt](evidence/active-cutoff-fix-20261024/browser/cutoff-single-20261024T161702/artifacts/result.json) |
| [E2E-09](06-test-cases.md#e2e-09) | Rapid Extend Input Shares One Renewal Request | FAILED | FAILED | [Retained attempt](evidence/active-cutoff-fix-20261024/browser/cutoff-rapid-20261024T161757/artifacts/result.json) |
| [E2E-10](06-test-cases.md#e2e-10) | Keyboard Extend Activation Renews The Session | FAILED | FAILED | [Retained attempt](evidence/active-cutoff-fix-20261024/browser/cutoff-keyboardExtend-20261024T162010/artifacts/result.json) |
| [E2E-11](06-test-cases.md#e2e-11) | Activity Failure Allows A Later Activity Retry | PASSED | PASSED | [Retained attempt](evidence/active-cutoff-fix-20261024/browser/cutoff-activityRetry-20261024T162145/artifacts/result.json) |
| [E2E-12](06-test-cases.md#e2e-12) | Inconsistent Activity Response Does Not Advance The Session | DIAGNOSTIC_FAILED | DIAGNOSTIC_FAILED | [Retained attempt](evidence/active-cutoff-fix-20261024/browser/cutoff-inconsistent-20261024T162252/artifacts/result.json) |
| [E2E-13](06-test-cases.md#e2e-13) | Activity Is Ignored While The Timeout Prompt Is Open | FAILED | FAILED | [Retained attempt](evidence/active-cutoff-fix-20261024/browser/cutoff-promptActivity-20261024T162425/artifacts/result.json) |
| [E2E-14](06-test-cases.md#e2e-14) | Idle Prompt Logout Clears The Session | PASSED | PASSED | [Retained attempt](evidence/active-cutoff-fix-20261024/browser/cutoff-idleLogout-20261024T162610/artifacts/result.json) |
| [E2E-15](06-test-cases.md#e2e-15) | Quick Background Switch Acquires Refresh Credentials | PASSED | PASSED | [Retained result](evidence/active-cutoff-fix-20261024/browser/cutoff-visibility-20261024T234941/artifacts/result.json) |
| [E2E-16](06-test-cases.md#e2e-16) | Reload After Renewal Preserves The Session | PASSED | PASSED | [Retained result](evidence/active-cutoff-fix-20261024/browser/cutoff-reload-20261024T235007/artifacts/result.json) |
| [E2E-17](06-test-cases.md#e2e-17) | Logout Cancels Pending Manual Renewal And Ignores Late Success | FAILED | FAILED | [Retained attempt](evidence/active-cutoff-fix-20261024/browser/cutoff-manualLogout-20261024T162738/artifacts/result.json) |
| [E2E-18](06-test-cases.md#e2e-18) | Logout Unmounts Home And Cancels Pending Activity Renewal | FAILED | FAILED | [Retained attempt](evidence/active-cutoff-fix-20261024/browser/cutoff-activityLogout-20261024T162917/artifacts/result.json) |
| [E2E-19](06-test-cases.md#e2e-19) | Late Activity Response Cannot Replace Successful Manual Renewal | FAILED | FAILED | [Retained result](evidence/active-cutoff-fix-20261024/browser/cutoff-late-20261024T234822/artifacts/result.json) |
| [E2E-20](06-test-cases.md#e2e-20) | Actual Expired Credential Cannot Authorize The Protected Operation | PASSED | PASSED | [Retained attempt](evidence/active-cutoff-fix-20261024/browser/cutoff-expired-20261024T163032/artifacts/result.json) |
| [E2E-21](06-test-cases.md#e2e-21) | Observe Background Return Without Refresh Credentials | OBSERVATION_ONLY | NOT_RUN | Pending |
| [E2E-22](06-test-cases.md#e2e-22) | Observe Saved Workspace Descriptors After Same User Sign In | OBSERVATION_ONLY | OBSERVATION_ONLY | [Retained attempt](evidence/active-cutoff-fix-20261024/browser/cutoff-workspace-20261024T163235/artifacts/result.json) |

## Unchanged failure boundaries

The [source-backed grouping](evidence/active-cutoff-fix-20261024/setup/failure-scope-analysis-20261025.json) binds the first eleven unchanged failures and candidate source locations.
The [late-response case](evidence/active-cutoff-fix-20261024/browser/cutoff-late-20261024T234822/artifacts/result.json) also remains failed at earlier-request cancellation.
Their first failed predicates occur before observed refresh expiry. Issue 1 changes a separate expiry branch.
Source causes below are inferences from inspected code and observed failures. Later blocked assertions remain untested.

| Cases | First failed predicate and source explanation | Consequence | Owner and next action |
| --- | --- | --- | --- |
| [E2E-01](06-test-cases.md#e2e-01), [E2E-02](06-test-cases.md#e2e-02), [E2E-03](06-test-cases.md#e2e-03), [E2E-08](06-test-cases.md#e2e-08) | Expected activity renewal did not start or complete. Home debounces mouse input; keyboard and scroll bindings are absent. | These activity requirements remain unmet. | Unknown application owner: correct activity scheduling and input coverage. |
| [E2E-04](06-test-cases.md#e2e-04), [E2E-05](06-test-cases.md#e2e-05), [E2E-10](06-test-cases.md#e2e-10), [E2E-13](06-test-cases.md#e2e-13), [E2E-17](06-test-cases.md#e2e-17) | Timeout closed before renewal completed or after rejection. The service does not return its POST promise. | Later recovery or cancellation assertions can remain unreached. | Unknown application owner: preserve the prompt through actual renewal completion. |
| [E2E-09](06-test-cases.md#e2e-09) | The second Extend target disappeared after early prompt closure. | Request sharing remains untested beyond that failure. | Unknown application owner: correct completion handling, then rerun rapid activation. |
| [E2E-18](06-test-cases.md#e2e-18), [E2E-19](06-test-cases.md#e2e-19) | Logout or Timeout opening did not cancel the held activity extension. Existing cleanup does not abort that request. | Cancellation remains unmet. Later stale-response behavior is untested by this result. | Unknown application owner: cancel pending extension work and verify session ownership. |

## Controlled regression evidence

The corrected tests fail against the original Home and pass against the candidate Home.
[Baseline red execution](evidence/active-cutoff-fix-20261024/unit/baseline-home-focused-execution.json) records five failures and 74 passes.
[Candidate green execution](evidence/active-cutoff-fix-20261024/unit/candidate-focused-execution.json) records 79 runner passes and zero failures.
The focused total includes one known delayed-recovery expected failure.
Both use the same updated tests and isolated source copies.
The [source binding](evidence/active-cutoff-fix-20261024/unit/regression-source-binding.json) proves that only Home differs between those runs.

[REVIEW-F01-RECOVERY](06-test-cases.md#review-f01-recovery) asserts replacement, retained access, and later manual recovery.
[REVIEW-F01-MANUAL](06-test-cases.md#review-f01-manual) asserts continuity after manual renewal near refresh expiry.
These are controlled JSDOM integrations with synthetic credentials and fake clocks.
The [full Jest execution](evidence/active-cutoff-fix-20261024/unit/candidate-full-execution.json) reports 116 passing suites and 413 runner passes.
Those totals include 412 ordinary passes and one known delayed-recovery expected failure.
A [normal-test diagnostic](evidence/active-cutoff-fix-20261024/unit/candidate-known-defect-normal-execution.json) confirms that delayed recovery still fails.
The known delayed-recovery `it.failing` remains distinct from passing behavior.
Both [TypeScript source checks](evidence/active-cutoff-fix-20261024/unit/typescript-source-comparison.json) pass without emitting files or changing the compiler cache.
The [unit report](evidence/active-cutoff-fix-20261024/unit/report.md) records exact commands and the retained initial option conflict.

## Retained evidence inventory

The [case inventory](evidence/active-cutoff-fix-20261024/case-inventory.json) records each original hash and source locator.
The [source binding](evidence/active-cutoff-fix-20261024/setup/source-binding.json) records executed implementation and dependency identities.
The [progress checkpoint](evidence/active-cutoff-fix-20261024/progress.json) records completed, running, and pending cases.
The [retention helper](evidence/active-cutoff-fix-20261024/compare-results.py) preserves each completed case before the next begins.
The [resume plan](evidence/active-cutoff-fix-20261024/setup/resume-plan.json) records the guarded command and remaining case order.
The [scoped batch receipt](evidence/active-cutoff-fix-20261024/dom-service-batch/manifest.json) retains commands, actual native exit codes, timestamps, and hashes.
The [initial batch receipt](evidence/active-cutoff-fix-20261024/initial-browser-batch/manifest.json) preserves available original launcher output.
Original failed and contradictory evidence remains unchanged.

## Browser evidence bindings

Completed candidate case records retain result JSON and named PNG captures under the task evidence directory.
The inventory binds each retained artifact by SHA-256 and case identity.
Screenshots support visible state. Request and lifecycle records support timing and credential assertions separately.
Missing captures or interrupted executions will remain visible in the final comparison.

## Verification conclusion

The focused controlled regressions support corrected expiry handling within their disclosed boundaries.
The complete browser comparison remains pending. [E2E-06](06-test-cases.md#e2e-06) changed from failed to passed.
Twenty scoped results are valid. Twelve business cases still fail. Six business cases pass.
The diagnostic remains failed. The workspace case remains an observation.
Two native background cases remain pending. The key candidate expiry case passes; its same-browser original-Home baseline fails.
The [integrity audit](evidence/active-cutoff-fix-20261024/implementation-validation.json) passes its source and evidence checks.
The [completion gate](evidence/active-cutoff-fix-20261024/browser-completion-gate.json) fails because two cases lack completed valid results.
A completed evidence audit does not establish a completed browser suite.
The original release assessment remains historical evidence for the uncorrected candidate.
This patch does not close stale-session ownership, required delayed recovery, or PROD artifact gaps.

## Facts, inferences, and unresolved questions

Facts: the patch changes Home expiry reconciliation and two regression files. Focused red and green evidence exists.
Fact: the fixed candidate passes the real-browser refresh-boundary predicates. A same-browser original-Home baseline reproduces the failure.
Unknown: deployed configuration, actual release artifact, operational owners, and production failure frequency.

## Findings

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| [Native preflight passed](evidence/active-cutoff-fix-20261024/setup/visibility-preflight.json). | Two candidate background cases still require completed results. | Codex | Run pending original cases and retain each completed result. |
| [Existing release blockers](10-release-confidence.md#findings). | A positive PROD recommendation remains blocked. | unknown application and release owners | Correct remaining runtime defects and bind release evidence. |

## Sources

| Source ID | Locator | Exact revision or identity | Authority and limits |
| --- | --- | --- | --- |
| SRC-session-active-cutoff-fix-request-20261024 | [Exact request](evidence/active-cutoff-fix-20261024/user-request.txt). | User message, 24 October 2026; SHA-256 in stage inputs. | Authorizes this local correction and comparison. No deployment authorization. |
| SRC-session-active-cutoff-fix-inputs-20261024 | [Inputs](evidence/active-cutoff-fix-20261024/inputs.json). | Full baseline commits and captured source hashes. | Engineering provenance. It establishes no business approval. |
