---
artifact_kind: investigation-report
id: RPT-case-e2e-match-review-20261024
version: 1
status: complete
owner: unknown
source_refs:
  - evidence/user-request-case-e2e-check-20261024.txt
  - evidence/canonical-gherkin-20261021/case-mapping.json
  - evidence/minor-branch-rerun-20261020/browser-manifest.json
  - evidence/uat-blotter-browser-20261021/summary.json
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
    - Automated checks verify counts and identities. They do not verify complete ASD-STE100 compliance.
    - No new browser execution was started for this review.
---

# Test case and E2E execution match review

> **Critical conclusions: Action required**
>
> The historical 22-case result set matches the old case definitions and source hashes.
> The current modularized 22-case suite remains `NOT_RUN`.
> The corrected native run covers 14 cases only. Eight canonical cases have no corrected native result.
> Owner: unknown test owner. Consequence: the current full catalog has no complete rerun.
> Evidence: [case mapping](../canonical-gherkin-20261021/case-mapping.json#L5-L11), [execution binding](../../06-test-cases.md#L2278-L2296), and [corrected coverage](../../09-coverage.md#L108-L119).

## User input

The exact request is retained in [user input evidence](../user-request-case-e2e-check-20261024.txt).

## Match result

The catalog contains 32 definitions: 22 E2E cases, two supplemental probes, and eight review cases.
The historical mapping lists all E2E IDs in the same order as the catalog.
The historical manifest declares 22 cases and marks the collection complete.
Its executed source and embedded result hashes match the retained revisions.

The historical result set therefore matches the 22 old definitions one-to-one.
It ran application revision `6d4c37c839b99d14ea41fd936da1a36cda526b17` and test revision `7a504c13a8d51bb52af5cc89bd4af88d1988da94`.
The current modularized test revision is `975af64c55303ee4a138968813ef4e85570f96d2`.
That suite has only offline checks and browser keyword discovery.
It has no new business execution.

The historical 22-case outcomes are:

| Outcome | Cases | Meaning |
| --- | --- | --- |
| `PASSED` | E2E-11, E2E-14, E2E-15, E2E-16, E2E-20 | The retained predicates passed in the local fixture. |
| `FAILED` | E2E-01–E2E-10, E2E-13, E2E-17–E2E-19 | The first assertion failed. Later assertions remain unverified. |
| `DIAGNOSTIC_FAILED` | E2E-12 | A supporting negative-contract diagnostic failed. It has no approved business criterion. |
| `OBSERVATION_ONLY` | E2E-21, E2E-22 | The observations passed, but no acceptance verdict is defined. |

The manifest counts are five passed, fourteen failed, one diagnostic failure, and two observations.
Twenty native Edge startup failures are setup failures. They are excluded from the 22 functional cases.

## Why the historical cases failed

| Cases | First failed predicate | Cause shown by retained evidence |
| --- | --- | --- |
| E2E-01, E2E-02, E2E-03 | A successful renewal did not finish within 15 seconds. | Mouse and keyboard runs recorded activity but no `/extend` response. E2E-03 received a 200 response, but the required renewal assertion still failed. See [mouse](../minor-branch-rerun-20261020/browser/minor-mouse-20261020T142055/artifacts/result.json), [keyboard](../minor-branch-rerun-20261020/browser/minor-keyboard-20261020T142128/artifacts/result.json), and [scroll](../minor-branch-rerun-20261020/browser/minor-scroll-20261020T142155/artifacts/result.json). |
| E2E-04, E2E-05, E2E-07, E2E-10, E2E-13, E2E-17 | The Timeout prompt had to remain visible while renewal was pending. | The prompt closed before the held or failed relogin completed. E2E-07 also waited 1,800,011 milliseconds and observed a freeze. See [E2E-04](../minor-branch-rerun-20261020/browser/minor-pending-20261020T142222/artifacts/result.json), [E2E-05](../minor-branch-rerun-20261020/browser/minor-retry-20261020T142329/artifacts/result.json), [E2E-07](../minor-branch-rerun-20261020/browser/minor-natural-20261020T141953/artifacts/result.json), [E2E-10](../minor-branch-rerun-20261020/browser/minor-keyboardExtend-20261020T143319/artifacts/result.json), [E2E-13](../minor-branch-rerun-20261020/browser/minor-promptActivity-20261020T143514/artifacts/result.json), and [E2E-17](../minor-branch-rerun-20261020/browser/minor-manualLogout-20261020T142736/artifacts/result.json). |
| E2E-06 | The authenticated portal had to remain available at the shortened refresh boundary. | Many `/extend` responses returned 200, but Home became unavailable when the refresh boundary was reached. See [result](../minor-branch-rerun-20261020/browser/minor-cross-20261020T142434/artifacts/result.json). |
| E2E-08 | Repeated activity had to share one pending extension. | No held extension request appeared. The observed request count was zero. See [result](../minor-branch-rerun-20261020/browser/minor-single-20261020T142711/artifacts/result.json). |
| E2E-09 | The driver had to locate Extend for the second activation. | Playwright `locator.boundingBox` timed out after 30 seconds. See [result](../minor-branch-rerun-20261020/browser/minor-rapid-20261020T143143/artifacts/result.json). |
| E2E-12 | A `result=false` response must not install its authorization header. | The controlled 200 response carried a new authorization header, and the browser installed it. This is diagnostic evidence only. See [result](../minor-branch-rerun-20261020/browser/minor-inconsistent-20261020T143455/artifacts/result.json). |
| E2E-18 | Logout or Home unmount had to cancel the pending extension. | The cancellation was not observed. The run recorded a later 401 response. See [result](../minor-branch-rerun-20261020/browser/minor-activityLogout-20261020T142841/artifacts/result.json). |
| E2E-19 | Opening Timeout had to cancel the earlier activity extension. | The cancellation assertion failed before manual renewal and late-delivery checks. See [result](../minor-branch-rerun-20261020/browser/minor-late-20261020T142910/artifacts/result.json). |

These failures stop each case at its first failed assertion.
They do not prove later token resurrection, overwrite, or protected-operation failures.

The separate delayed-refresh probe shows the main background-recovery defect.
The service returned HTTP 200 while access remained valid.
The driver delivered the response 58.537 seconds later, with 84.627 seconds of refresh validity remaining.
Extend was disabled, no relogin request occurred, logout returned 200, and Sign in appeared.
Evidence: [analysis](../minor-branch-rerun-20261020/supplemental/delayed-refresh/analysis.json).
The retained inference is that timeout and pending-refresh state handling start logout before usable refresh delivery completes.

## Later Blotter and realistic executions

The later Blotter cases have their own definitions and results.
They do not replace the historical 22-case run.

| Scope | Match and outcome | Failure or limit |
| --- | --- | --- |
| UAT Blotter cases | Five executed; four passed; one failed; one was not run. | `UAT-BLOTTER-PRIOR-TILE` failed five of seven assertions because native pointer activity contaminated the removal phase. `UAT-BLOTTER-NO-REFRESH` remains unexecuted. See [summary](../uat-blotter-browser-20261021/summary.json#L191-L205) and [case definition](../../06-test-cases.md#L1788-L1824). |
| UAT setup attempts | Two setup attempts did not run business assertions. | One had invalid SockJS fixture data. One failed during Native Edge startup. See [setup records](../uat-blotter-browser-20261021/summary.json#L207-L217). |
| Realistic 30-minute hidden case | The case completed 33 of 34 assertions. | One successful `/extend` changed access expiry during the supposed fixed-expiry interval. The fixed-expiry assertion failed. See [result](../real-world-tests-20261022/rw-blotter-hidden-30m-03/result.json#L8251-L8285). |
| Realistic controls | Schedule, mismatch detection, and shortened-idle controls passed. | These controls do not prove eight-hour timer firing, UAT parity, or production behavior. See [case definitions](../../06-test-cases.md#L1885-L1921) and [coverage](../../09-coverage.md#L108-L124). |

## Review limits

The current modularized 22-case suite has no business execution result.
The corrected native run covers 14 cases and excludes E2E-09 through E2E-16.
Local fixtures replace external identity, notification, catalog, and business services.
No result establishes production configuration, provider revocation, downstream authorization, or UAT parity.

The automated consistency checks passed in [validation receipt](validation.json).
Human review and acceptance decisions remain pending.
