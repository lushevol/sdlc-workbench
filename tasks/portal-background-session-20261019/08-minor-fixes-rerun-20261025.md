---
artifact_kind: test-execution-report
id: EXEC-session-sequential-minor-fixes-20261025
version: 1
status: draft
owner: unknown
source_refs:
  - SRC-session-sequential-minor-fixes-20261025
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

# Sequential minor fixes and case reruns

> **Both fixes pass local checks. Five remaining failures keep PROD on hold.**
> Action: correct the remaining activity behavior and complete blocked native verification.
> Consequence: active work can expire without renewal; pending activity requests can survive Logout.
> Owner: unknown application owner; user for unlock; Codex for verification.
> Evidence: [browser comparison](evidence/minor-fixes-20261025/issue-2/browser-comparison.json) and [controlled comparison](evidence/minor-fixes-20261025/controlled-comparison.json).

| Fix | Commit | Controlled comparison | Browser comparison |
| --- | --- | --- | --- |
| Reject ended-session responses. | `5a397ec` | Seven failures corrected; two controls pass. | Two stale-response cases changed from failed to passed. |
| Preserve pending renewal and recovery. | `26803ed` | Twelve failures corrected; one control passes. | Six original failures changed to passed. |

**Final candidate: `c42e760`. Full suite: 118 suites and 435 tests pass. TypeScript passes.**
The last commit updates two legacy tests. Runtime bytes match the second fix.
Jest used `--forceExit`. Resource cleanup remains unverified.

## Assertions and outcomes

Original business cases: **9 passed, 5 failed, 5 blocked by the Mac lock**.
These totals cover nineteen cases. Diagnostics, observations, and added probes remain separate.
All 120 original assertion calls remain unchanged.

| Case | Behavior | Before `ae8213f` | After `c42e760` |
| --- | --- | --- | --- |
| [E2E-04](06-test-cases.md#e2e-04) | Keep Timeout open during pending renewal | [FAILED](evidence/active-cutoff-fix-20261024/browser/cutoff-pending-20261024T155803/artifacts/result.json) | [PASSED](evidence/minor-fixes-20261025/issue-2/browser/issue-2-pending-20261025T092741/artifacts/pending-renewal-1792920465568/result.json) |
| [E2E-05](06-test-cases.md#e2e-05) | Retry after renewal failure | [FAILED](evidence/active-cutoff-fix-20261024/browser/cutoff-retry-20261024T155915/artifacts/result.json) | [PASSED](evidence/minor-fixes-20261025/issue-2/browser/issue-2-retry-20261025T093024/artifacts/rejected-renewal-retry-1792920631883/result.json) |
| [E2E-09](06-test-cases.md#e2e-09) | Prevent duplicate Extend activation | [FAILED](evidence/active-cutoff-fix-20261024/browser/cutoff-rapid-20261024T161757/artifacts/result.json) | [PASSED](evidence/minor-fixes-20261025/issue-2/browser/issue-2-rapid-20261025T093141/artifacts/rapid-extend-single-flight-1792920708096/result.json) |
| [E2E-10](06-test-cases.md#e2e-10) | Activate Extend with the keyboard | [FAILED](evidence/active-cutoff-fix-20261024/browser/cutoff-keyboardExtend-20261024T162010/artifacts/result.json) | [PASSED](evidence/minor-fixes-20261025/issue-2/browser/issue-2-keyboardExtend-20261025T093257/artifacts/keyboard-extend-activation-1792920784140/result.json) |
| [E2E-13](06-test-cases.md#e2e-13) | Keep recovery explicit during activity | [FAILED](evidence/active-cutoff-fix-20261024/browser/cutoff-promptActivity-20261024T162425/artifacts/result.json) | [PASSED](evidence/minor-fixes-20261025/issue-2/browser/issue-2-promptActivity-20261025T093414/artifacts/prompt-ignores-activity-1792920861525/result.json) |
| [E2E-17](06-test-cases.md#e2e-17) | Allow Logout during pending renewal | [FAILED](evidence/active-cutoff-fix-20261024/browser/cutoff-manualLogout-20261024T162738/artifacts/result.json) | [PASSED](evidence/minor-fixes-20261025/issue-2/browser/issue-2-manualLogout-20261025T093538/artifacts/pending-manual-logout-cancellation-1792920945026/result.json) |

The [complete comparison](evidence/minor-fixes-20261025/issue-2/browser-comparison.json) binds every case, assertion source, result hash, and execution scope.
Native runs passed six corrected cases. Independent DOM/service checks passed three additional business cases while macOS was locked.
Those checks do not establish physical UI or native lifecycle behavior.
The additional [scheduled delayed-recovery probe](06-test-cases.md#fix-delayed-browser-scheduled) also passed.
The [first-stage ownership comparison](evidence/minor-fixes-20261025/issue-1/browser-comparison.json) records two separate failed-to-passed browser controls.
Final-candidate ownership browser reruns remain blocked. Their controlled regressions pass on the final candidate.

Remaining failures:

- [E2E-01](06-test-cases.md#e2e-01), [E2E-02](06-test-cases.md#e2e-02), and [E2E-03](06-test-cases.md#e2e-03): continuous input misses the required renewal interval.
- [E2E-08](06-test-cases.md#e2e-08): repeated activity does not meet the shared pending-extension assertion.
- [E2E-18](06-test-cases.md#e2e-18): Logout does not meet the pending activity-request cancellation assertion.

Blocked native cases:
[E2E-06](06-test-cases.md#e2e-06), [E2E-07](06-test-cases.md#e2e-07), [E2E-15](06-test-cases.md#e2e-15), [E2E-16](06-test-cases.md#e2e-16), and [E2E-19](06-test-cases.md#e2e-19).
Two cross-window attempts had invalid setup. They are not application failures.
No runner remains active. The [resume checkpoint](evidence/minor-fixes-20261025/issue-2/native-resume-checkpoint.json) preserves the queue.

[E2E-12](06-test-cases.md#e2e-12) remains diagnostic failure.
[E2E-22](06-test-cases.md#e2e-22) remains an observation.
[E2E-21](06-test-cases.md#e2e-21) is [not rerun](evidence/minor-fixes-20261025/issue-2/not-rerun.json).
These outcomes do not enter the nineteen business-case totals.

## Run identity and provenance

The [exact request](evidence/minor-fixes-20261025/user-request.txt) authorizes two sequential fixes and case reruns.
The [phase inputs](evidence/minor-fixes-20261025/inputs.json) record `READY`, the baseline, affected interfaces, and preserved changes.
Initial candidate: `ae8213f2963047e7c126d01f4003cee1236abc25`.
Final candidate: `c42e7609c4e14eb53de32702e4bd3424a223988a`.
Separate [ownership](evidence/minor-fixes-20261025/issue-1/commit-binding.json) and [pending-renewal](evidence/minor-fixes-20261025/issue-2/commit-binding.json) records bind the staged changes.
The [served-source check](evidence/minor-fixes-20261025/setup/final-served-source-binding.json) matches 136 local application sources to the final candidate.
This local binding does not establish a PROD artifact or configuration.
No requirement, knowledge policy, deployment, or waiver changed.

## Correction and impact

| Boundary | Corrected behavior | Consequence |
| --- | --- | --- |
| Session ownership | Reject old success and errors before shared mutations. Preserve normal access rotation. | Ended-session responses cannot adopt stale refresh credentials or clear a newer login. |
| Pending acquisition | Wait for current-session acquisition. Check received refresh expiry after settlement. | Usable late credentials permit explicit recovery. |
| Manual renewal | Await completion. Reject unusable access before mutation. Preserve retry after transport failure. | Timeout closes after valid renewal and stays open during failure. |
| Explicit Logout | Keep Logout available. Abort both pending recovery requests and guard delayed callbacks. | The user can exit pending recovery without later session restoration. |

Pending activity-request cancellation remains a separate failed boundary.
Existing timing remains: two-second recovery cutoff, one-second logout delay, and sixty-second request timeout.
System scope covers Home, Timeout, shared Axios interceptors, credential state, and their consumers.
Business scope covers portal sign-in, active work, recovery, and logout. Application ownership remains unknown.
Deployed microfrontend versions and effective PROD settings remain unbound.
The [caller review](evidence/minor-fixes-20261025/fresh-login-reachability-review.json) found no ordinary in-place replacement-login journey.
Uninspected remote consumers remain a limit.

## Controlled regression evidence

The [comparison](evidence/minor-fixes-20261025/controlled-comparison.json) records nineteen failed-to-passed changes and three passing controls.
These twenty-two new regressions remain separate from thirty-one existing lifecycle cases and browser totals.
[Ownership definitions](06-test-cases.md#session-ownership-regressions-25-october-2026) and [pending definitions](06-test-cases.md#pending-renewal-regressions-25-october-2026) retain canonical Gherkin.
The former delayed-recovery expected failure now passes as a normal case.
The [full execution](evidence/minor-fixes-20261025/issue-2/full-rerun-2/execution.json) binds all 435 results to final source hashes.
The first full attempt exposed two obsolete tests. Its [failure receipt](evidence/minor-fixes-20261025/issue-2/full/execution.json) remains retained.
Historical F03 diagnostics use a synthetic adapter. Their missing-refresh control cannot establish valid recovery.

## Retained evidence inventory

| Evidence | Purpose and limit |
| --- | --- |
| [Controlled comparison](evidence/minor-fixes-20261025/controlled-comparison.json) | Before/after predicates, final source matching, and fixture limits. |
| [Full unit execution](evidence/minor-fixes-20261025/issue-2/full-rerun-2/execution.json) | 435 passing tests; cleanup remains unverified. |
| [Ownership browser comparison](evidence/minor-fixes-20261025/issue-1/browser-comparison.json) | Two native failed-to-passed comparisons at the first fix. |
| [Final browser comparison](evidence/minor-fixes-20261025/issue-2/browser-comparison.json) | Original nineteen business cases, diagnostics, observations, added probes, and blocked cases. |
| [Browser validation](evidence/minor-fixes-20261025/issue-2/browser-evidence-validation.json) | Matching retained result hashes and declared inventories. |
| [Original assertion audit](evidence/minor-fixes-20261025/setup/original-assertion-integrity.json) | All 120 original assertion calls remain unchanged. |

## Verification conclusion

Both requested corrections pass controlled verification. Final native browser verification remains blocked by the Mac lock.
The thirty-minute natural case remains distinct from the shortened delayed-recovery probe.
The exact controlled-clock four-hour criterion remains unverified.
The [current release assessment](10-release-confidence-minor-fixes-20261025.md) retains the five failures and missing PROD evidence.

## Facts, inferences, and unresolved questions

Facts: both targeted corrections pass controlled verification. Six original browser failures now pass.
Inference: these fixes reduce stale-session adoption and failed recovery within the inspected conditions.
Unknowns: PROD frequency, artifact identity, effective configuration, complete four-hour verification, and operating ownership.
Local browser fixtures do not establish PROD parity.

## Findings

| Finding | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| Five original business cases fail. | Activity renewal or cancellation remains unmet. | unknown application owner | Correct the failed boundaries and rerun unchanged assertions. |
| Five native cases are blocked. | Complete lifecycle closure is unsupported. | user for unlock; Codex for execution | Unlock, verify native setup, and resume the saved queue. |
| Release evidence remains unbound. | A positive PROD decision remains unsupported. | unknown release owner | Bind artifact, settings, recovery, monitoring, and operators. |


## Document validation

[Document lint](evidence/minor-fixes-20261025/setup/final-document-lint.json) passes with sixteen warnings across four documents.
Warnings retain unknown owners, pending business review, unresolved values, and pending full ASD review.
[Workspace validation](evidence/minor-fixes-20261025/setup/final-workspace-validation.json) passes without findings.
These checks do not verify business execution or grant deployment authorization.

## Sources

The [exact request](evidence/minor-fixes-20261025/user-request.txt) is `SRC-session-sequential-minor-fixes-20261025`.
Intended behavior follows [requirement version 4](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria).
Publication review remains pending. These corrections restore recorded intent without publishing knowledge.
