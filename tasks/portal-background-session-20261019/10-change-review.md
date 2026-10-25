---
artifact_kind: change-request
id: CHANGE-session-post-review-20261020
version: 23
status: draft
owner: unknown
source_refs:
  - SRC-session-sequential-minor-fixes-20261025
  - SRC-session-active-cutoff-fix-request-20261024
  - SRC-session-coverage-detection-request-20261024
  - SRC-session-minimal-request-20261023
  - SRC-session-release-source-20261022
  - SRC-session-real-world-tests-20261022
  - SRC-session-uat-blotter-browser-20261021
  - SRC-session-uat-screenshot-20261021
  - SRC-session-uat-timeout-inquiry-20261021
  - SRC-session-branch-refresh-20261021
  - SRC-session-baseline-reassessment-20261021
  - SRC-session-minor-stage-20261020
  - SRC-session-review-intent-v4
  - SRC-session-minor-browser-20261020
related_ids:
  - ASSESS-session-refresh-release-20261022
  - DEFECT-portal-background-session-20261019
  - REQ-active-session-renewal
  - REVIEW-session-minor-20261021
  - EXEC-session-renewal-browser-20261020
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

# Reduced session-change assessment

> **NO_GO: both minor corrections pass local checks, but six business cases still fail.**
> Action: correct activity renewal and pending activity-request cancellation, then rerun the failed cases.
> Consequence: active portal work can expire without renewal. PROD promotion remains blocked.
> Owner: unknown application owner.
> Evidence: [current rerun report](08-minor-fixes-rerun-20261025.md) and [current release assessment](10-release-confidence-minor-fixes-20261025.md).
>
> **All native reruns are complete. Natural recovery passed with an observed freeze.**
> Action: resolve remaining failures and bind artifact, target, and operating evidence.
> Consequence: complete requirement conformance and positive PROD handoff remain unsupported.
> Owner: unknown application and release owners.
> Evidence: [browser comparison](evidence/minor-fixes-20261025/issue-2/browser-comparison.json) and [final checkpoint](evidence/minor-fixes-20261025/issue-2/native-resume-checkpoint.json).
> Earlier locked-Mac checks retain their narrower DOM/service scope.

<details>
<summary>Historical conclusions before the sequential corrections</summary>

These conclusions describe earlier candidates. The current results below supersede their runtime status claims.
Historical issue 1 means the active-cutoff correction at `ae8213f`.
Current issue 1 means the session-ownership correction at `5a397ec`.
The photographed UAT lifetime and effective configuration remain unverified release boundaries.

> **The authorized native comparison completed, but E2E-07 remains failed.**
> Action: preserve the Timeout prompt during pending renewal, then rerun E2E-07 and delayed recovery.
> Consequence: natural background recovery remains unmet.
> Owner: unknown application owner; Codex for local verification.
> Evidence: [E2E-07 result](evidence/active-cutoff-fix-20261024/browser/cutoff-natural-20261025T004053/artifacts/result.json) and [current comparison](08-active-cutoff-fix-20261024.md).

> **Do not promote the current minor candidate to PROD.**
> Action: resolve the current session regressions and required delayed recovery, then reassess the exact release artifact.
> Consequence: active work or fresh-session recovery can end. A positive PROD handoff remains blocked.
> Owner: unknown application, authentication, and release owners.
> Evidence: [successor release confidence assessment](10-release-confidence-active-cutoff-20261025.md#findings) and [current source review](evidence/release-confidence-20261022/source-review.json).
> Evidence confidence is high for this technical hold. PROD frequency remains unknown.

> **Action required: verify the eight-hour UAT access lifetime.**
> The photograph shows `difftime = 28,788,109` milliseconds. This equals 7 hours, 59 minutes, 48.109 seconds.
> Action: confirm the effective BFF property source, JWT lifetime, and clock agreement.
> Consequence: the photographed access timer cannot expire within thirty minutes. UAT configuration correction remains blocked.
> Owner: unknown authentication owner. Evidence: [photograph](evidence/uat-blotter-browser-20261021/uat-screenshot/observation.json) and [source receipt](evidence/uat-blotter-browser-20261021/uat-screenshot/timing-contract-source-receipt.json).
> The BFF contains `jwt.tokenExpiration=480`. Its use in UAT remains inferred. Refresh expiry can trigger an earlier dialog.

> **🔴 Action required: stale-session recovery remains open after the active-cutoff correction.**
> Verify the [active-cutoff correction](08-active-cutoff-fix-20261024.md) and correct [stale-credential reuse](code-review-minor-20261021.md#f-03-p2-stop-stale-credential-persistence-and-reuse).
> Consequence: active access can end; stale credentials can clear a fresh session.
> Owner: unknown application owner. Evidence: [paired results](evidence/code-review-refresh-20261021/summary.json) and [successor release confidence assessment](10-release-confidence-active-cutoff-20261025.md#findings).
>
> **👤 Decision required: delayed recovery and broader deferrals remain open.**
> Decide whether to correct delayed recovery or explicitly accept a named fallback.
> Name each broader criterion proposed for deferral. Acceptance remains open until those decisions are recorded.
> Owner: user and unknown authentication owner. Evidence: [failed recovery](test-cases.md#review-delayed-scheduled) and [scope request](evidence/minor-branch-rerun-20261020/user-request.txt).
> Controlled local evidence does not establish production frequency or release approval.

</details>

## Sequential minor corrections: 25 October 2026

The [release-scope question](evidence/minor-fixes-20261025/setup/no-go-clarification-question-20261025.txt) asks why the completed corrections still receive NO_GO.
The decision covers all applicable session-refresh requirements. It does not mark the two corrected defects as unresolved.

The [continuation request](evidence/minor-fixes-20261025/setup/continue-request-20261025.txt) resumes the existing verification scope.
It supplies no missing business policy or deployment authorization.

The [unlock reply](evidence/minor-fixes-20261025/setup/unlock-reply-20261025.json) authorizes native preflight and the retained test queue.
The user answered: “Unlocked; continue”. The reply does not establish passing native setup or execution.

Fresh native setup passed. Cross-expiry, visibility, reload, and both final ownership checks passed.
Late activity-response cancellation failed its unchanged assertion.
The [natural recovery result](evidence/minor-fixes-20261025/issue-2/browser/issue-2-natural-20261025T114548/artifacts/natural-background-paired-control-1792928754518/result.json) passed with an observed freeze.
Native timestamps establish at least `1,800,694` hidden milliseconds before subject restoration.
The earlier sleep sample remains `1,799,958` milliseconds. The [timing analysis](evidence/minor-fixes-20261025/setup/natural-timing-analysis.json) preserves both values.
These are wall-clock measurements. No monotonic-duration receipt was retained.
The [saved checkpoint](evidence/minor-fixes-20261025/issue-2/native-resume-checkpoint.json) retains the prior wait and completion reconciliation.
The [cleanup receipt](evidence/minor-fixes-20261025/setup/native-runtime-cleanup.json) confirms release of the temporary wake assertion.
The wait checkpoint's initial `FAILED` sentinel does not override the completed passing result.

> **Both ordered corrections are committed. The remaining failures keep release status at NO_GO.**
> Action: close the failed activity and cancellation cases, then bind the release evidence.
> Consequence: the two corrections alone cannot establish complete requirement conformance.
> Owner: unknown application owner; Codex for local verification.
> Evidence: [user authorization](evidence/minor-fixes-20261025/user-request.txt) and [current results](08-minor-fixes-rerun-20261025.md).

The named phase was `READY` for the two local corrections and affected verification. Both corrections are complete.
Existing [requirement criteria](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria) define the intended outcomes.
The [minimal proposal](05-minimal-blocker-fixes.md#fix-1-reject-responses-owned-by-an-ended-session) and retained failures establish both causes.
Shared authentication handlers, session boundaries, and Timeout callbacks have medium qualitative risk.
The [phase inputs](evidence/minor-fixes-20261025/inputs.json) record affected interfaces, baseline revisions, hashes, and preserved unrelated changes.

Issue 1 is committed as `5a397ec3e47c57196ba99dc20c7fdab539b03b4a`.
Its [nine ownership cases](evidence/minor-fixes-20261025/issue-1/summary.json) pass. Seven changed from failed to passed.

Issue 2 is committed as `26803ed868702232baab678ead59a24a69bd9952`.
Its [thirteen pending-renewal cases](evidence/minor-fixes-20261025/issue-2/candidate-summary.json) pass. Twelve changed from failed to passed.

The final assertion follow-up commit is `c42e7609c4e14eb53de32702e4bd3424a223988a`.
The [controlled comparison](evidence/minor-fixes-20261025/controlled-comparison.json) reconciles both corrections at that final candidate.

The full Jest run passes 118 suites and 435 tests. TypeScript passes.
The [execution receipt](evidence/minor-fixes-20261025/issue-2/full-rerun-2/execution.json) records `--forceExit`; resource cleanup remains unverified.

The [browser comparison](evidence/minor-fixes-20261025/issue-2/browser-comparison.json) records nineteen business cases: thirteen passed, six failed, and none blocked.
Seven original failures changed to passed. Diagnostic and observation outcomes remain outside those totals.

Two ownership browser cases changed to passed at the first-stage commit. Both final-candidate native ownership reruns also passed.
The added shortened delayed-recovery probe passed. Natural recovery also passed, with the wall-clock measurement limit stated above.
The exact controlled four-hour criterion remains unverified.

The [combined semantic review](evidence/minor-fixes-20261025/combined-semantic-review.json) inspected all seventeen changed paths and relevant consumers.
It found no new actionable defect. External consumers, provider behavior, and clean resource shutdown remain outside that evidence.
The [coverage matrices](09-coverage-minor-fixes-20261025.md) separate AC-to-test, AC-to-code, and code-to-test evidence.

No business clarification changed. Knowledge publication and deployment authorization remain separate.
The source-scoped [release assessment](10-release-confidence-minor-fixes-20261025.md) is `READY` and recommends `NO_GO`.
Here, `READY` permits the named assessment. It does not permit PROD deployment.
Missing artifact evidence cannot reverse the observed activity and cancellation failures.
Native reruns completed after the [recorded unlock](evidence/minor-fixes-20261025/setup/unlock-reply-20261025.json).
The [earlier lock](evidence/minor-fixes-20261025/setup/cross-setup-console-check.json) explains two invalid setup attempts. It is no longer a blocker.

## Current coverage inquiry: 24 October 2026

This historical stage records earlier evidence. Its runtime outcomes do not describe the final `c42e760` candidate.

The [high-priority request](evidence/coverage-detection-audit-20261024/user-request.txt) asks whether three runtime issues had test coverage.
It also asks whether earlier evidence exposed them before the release-confidence assessment.
The named phase is `READY` for a retrospective evidence audit.
Existing intent, assertions, execution records, and Git history support that scope.
The [audit inputs](evidence/coverage-detection-audit-20261024/inputs.json) bind source identities and preserved changes.
This audit separates unit assertions, canonical definitions, retained executions, and recorded findings.

The [completed audit](09-test-detection-audit.md) confirms all three were known before release-confidence work.
Active-cutoff tests expect the defect. Stale-session coverage lacks an exact browser case. Delayed recovery remains an expected failure.
Canonical Gherkin definitions were synchronized after the original executions.
No application correction or new business execution occurred. The release hold remains.

The [documentation and evidence checks](evidence/coverage-detection-audit-20261024/validation.json) pass with owner and review warnings.
No business clarification changed. No knowledge record changed.

## Active-cutoff correction request: 24 October 2026

This historical stage records earlier evidence. Its runtime outcomes do not describe the final `c42e760` candidate.

The [high-priority request](evidence/active-cutoff-fix-20261024/user-request.txt) authorizes a minor correction for issue 1 and E2E reruns.
The requested comparison must identify cases that change from failed to passed.
This stage preserves the original results and excludes unrelated runtime corrections.
The [stage inputs](evidence/active-cutoff-fix-20261024/inputs.json) record `READY` for this correction and local browser comparison.
Existing requirement evidence supports valid-access continuity. The user authorizes implementation and reruns within this scope.
The qualitative risk is medium. Shared Home expiry handling affects active and idle authentication.
The [complete inventory](evidence/active-cutoff-fix-20261024/case-inventory.json) preserves all 22 original cases and their assertions.
The continuation preflight restored native execution readiness. E2E-21 completed as an observation. The fresh E2E-07 run completed after 1,800,046 real milliseconds and failed prompt visibility during pending renewal. The [checkpoint](evidence/active-cutoff-fix-20261024/progress.json) records all retained candidate results.
The [comparison report](08-active-cutoff-fix-20261024.md) links the unchanged browser assertions and controlled correction regressions.
Implementation commit `ae8213f2963047e7c126d01f4003cee1236abc25` passes the full Jest and TypeScript checks.
The [integrity audit](evidence/active-cutoff-fix-20261024/implementation-validation.json) confirms matching candidate bytes and preserved original evidence.
The first five original browser cases retain valid failures. Two attempts have invalid setup conditions.
The independent batch is complete under the [recorded scope](evidence/active-cutoff-fix-20261024/setup/locked-mac-case-scope.json).
Twenty-one eligible comparisons are valid. [E2E-06](06-test-cases.md#e2e-06) changed from failed to passed. [E2E-07](06-test-cases.md#e2e-07) remains failed after a valid natural run. The same-browser original-Home baseline reproduces the refresh-boundary failure.
The [failure grouping](evidence/active-cutoff-fix-20261024/setup/failure-scope-analysis-20261025.json) explains the eleven unchanged failures and their untested later boundaries.

## Current task state

| Item | Current assessment |
| --- | --- |
| Latest request | [Apply two minor fixes sequentially and rerun cases](evidence/minor-fixes-20261025/user-request.txt). |
| Source | `feature/session-refresh-minor`; final `c42e7609c4e14eb53de32702e4bd3424a223988a`; initial `ae8213f2963047e7c126d01f4003cee1236abc25`. |
| Named phase | Both local corrections, controlled verification, and native reruns are complete. Release evidence limits remain. |
| Local result | [Ownership](evidence/minor-fixes-20261025/issue-1/summary.json): seven failures corrected. [Pending renewal](evidence/minor-fixes-20261025/issue-2/candidate-summary.json): twelve failures corrected. |
| Current checks | TypeScript passes. Full suite: 118 suites and 435 tests pass. The [execution receipt](evidence/minor-fixes-20261025/issue-2/full-rerun-2/execution.json) records the shutdown limit and final source binding. |
| Browser result | Original business cases: 13 passed, 6 failed, 0 blocked. Seven changed from failed to passed. [Complete comparison](evidence/minor-fixes-20261025/issue-2/browser-comparison.json). Diagnostics and observations remain separate. |
| Blocking conditions | `NO_GO`: required activity renewal and pending activity-request cancellation fail. Exact criterion and release evidence remain incomplete. |
| Target limits | Immutable artifact, effective PROD configuration, recovery, monitoring, and operator evidence remain unbound. |
| Next action | Unknown application owner: correct six failed boundaries. Unknown release owner: bind release evidence. |
| Decisions | No criterion waiver or completed deployment authorization was found. |

## Minimal correction proposal: 23 October 2026

This historical stage records earlier evidence. Its runtime outcomes do not describe the final `c42e760` candidate.

The [proposal](05-minimal-blocker-fixes.md) gives source-backed snippets for the three runtime blockers.
It covers refresh replacement, session ownership, and delayed manual recovery.
The [design evidence](evidence/minimal-blocker-fixes-20261023/source-inventory.json) binds current source and preservation checks.
The proposal preserves existing timing values. It adds no criterion waiver or knowledge clarification.
No application changes, business executions, or deployment occurred. The release hold remains.
The [documentation checks](evidence/minimal-blocker-fixes-20261023/validation.json) pass with owner and review warnings.

## Realistic test enhancement: 22 October 2026

> **Action required: assess the failed fixed-expiry observation before accepting idle-session stability.**
> A hidden-session renewal moved access expiry ten seconds. The complete thirty-minute case fails one of 34 assertions.
> Consequence: this execution cannot establish fixed access expiry during the complete interval.
> Owner: unknown application owner. Evidence: [completed observation](evidence/real-world-tests-20261022/rw-blotter-hidden-30m-03/result.json).
> A [queued mouse timer](evidence/real-world-tests-20261022/run03-queued-extension-finding.json) strongly explains the early request. Callback-to-request identity remains inferred.
> No later authentication request occurred. This result does not establish recurring background renewal.

The user authorized improved test cases, scripts, and realistic local execution.
The [stage inputs](evidence/real-world-tests-20261022/inputs.json) bind initial revisions, unrelated changes, scope, and the frozen intake hash.

The named phase is **READY: test-script enhancements and local evidence collection**.
Prior diagnosis establishes the missing configuration comparison. No business policy change is required.
UAT acceptance remains blocked by missing effective settings and deployed-byte evidence.

The change scope covers the independent test repository and this task's current records.
The facade initializes every existing case through `openPortalSession`.
Its timing preflight therefore affects all 22 case setups.
The new browser runner consumes the same timing checks where compatible.
Application runtime source and UAT configuration remain outside this stage.

The qualitative risk is medium. Instrumentation, browser focus, and trusted input can change observed session behavior.
Use isolated browser profiles, real elapsed time, separate input controls, and immutable case evidence.
Preserve historical failures and unrelated worktree changes.
Shortened lifetimes remain disclosed controls. They cannot establish deployed configuration parity.

### What changed in the tests

The earlier local cases exercised shortened expiry branches. They did not assert representative launch settings against issued lifetimes.
The enhanced preflight compares access issuance with an explicit profile before any dependent idle wait.
It records refresh and absolute deadlines separately. It checks comparable clocks and later issued access lifetimes.
Failed setup evidence now survives configuration errors and native browser launch failures.

The [source audit](evidence/real-world-tests-20261022/source-config-audit-v2.json) detects fifteen-minute defaults against the 480-minute launch declaration.
Its raw status is `CONFLICT`. The [execution receipt](evidence/real-world-tests-20261022/source-config-audit-execution-v2.json) passes only the discrepancy-detection predicate.
The audit does not establish effective UAT property loading.

| Comparison | Earlier test scope | Enhanced observation | Remaining limit |
| --- | --- | --- | --- |
| Configuration | Shortened test settings drove expiry checks. | [Source audit](evidence/real-world-tests-20261022/source-config-audit-v2.json) retains selected settings, units, locations, and hashes. | Effective UAT settings remain unbound. |
| Issued lifetime | No equivalent configured-versus-issued gate existed. | [Final negative preflight](evidence/real-world-tests-20261022/rw-negative-900-03/result.json) rejects 28,800 seconds against 900 seconds. | The 900-second value is a deliberate diagnostic expectation. It establishes no approved policy. |
| Background interval | Historical controls used shortened expiry. | [Completed observation](evidence/real-world-tests-20261022/rw-blotter-hidden-30m-03/result.json) retains thirty real minutes and 33 passing assertions. | Fixed expiry fails after one early renewal. UAT parity remains unsupported. |
| Harness regressions | The previous source lacked timing-profile gates. | [Twenty-five offline regressions](evidence/real-world-tests-20261022/fixture-retention-offline-regressions.json) pass. | Harness results do not establish portal behavior. |

The [canonical additions](test-cases.md#real-world-session-cases) keep observation outcomes separate from business acceptance.
The [progress checkpoint](evidence/real-world-tests-20261022/progress.json) retains completed results and interrupted attempts.

The [full observation](evidence/real-world-tests-20261022/rw-blotter-hidden-30m-03/result.json) records 1,800,122 wall milliseconds and 1,800,175.709 monotonic milliseconds.
It passes visibility, trusted-input, document-continuity, independent-deadline, and returned-component checks.
One queued extension changes expiry ten seconds. The fixed-expiry assertion fails.

The [source finding](evidence/real-world-tests-20261022/run03-queued-extension-finding.json) links a five-second mouse debounce to the request timeline.
The callback-to-request relationship is strongly supported. It is not directly recorded.
A browser freeze event occurs during this interval. Attached CDP and observers limit general lifecycle conclusions.

The [shortened hidden control](evidence/real-world-tests-20261022/rw-short-idle-01/result.json) passes all 30 assertions.
Timeout opens 1,419 milliseconds after actual access expiry. It remains visible after native return.
The [matching schedule](evidence/real-world-tests-20261022/rw-480-schedule-02/result.json) passes all 34 assertions over fifteen real seconds.
The [frozen-result audit](evidence/real-world-tests-20261022/frozen-results-audit.json) passes integrity checks for four completed executions.
Integrity success does not change the failed browser outcome.

Test commit `9314355b75771d756784ca872480848b9d206deb` binds those exact browser drivers.

The enhancement stage is complete. Application runtime source and UAT settings were not changed.
Final test commit `37b7365aca2203021e7014112b9d15cf00f7455b` adds fixture-snapshot redaction and its regression.
The [exact comparison](evidence/real-world-tests-20261022/fixture-retention-only-comparison.json) proves that timing and assertion bytes remain unchanged.
The thirty-minute case was not rerun after that retention change. Its result remains bound to the earlier commit.

The [final schedule](evidence/real-world-tests-20261022/rw-480-schedule-03/result.json) passes all 34 assertions.
The [final shortened control](evidence/real-world-tests-20261022/rw-short-idle-02/result.json) passes all 30 assertions.
Timeout opens 1,479 milliseconds after access expiry and remains visible after return.
The [final source binding](evidence/real-world-tests-20261022/final-source-commit.json) matches all executed driver and supervisor snapshots.
The [final audit](evidence/real-world-tests-20261022/final-results-audit.json) passes evidence checks for seven completed runs.
The [cleanup audit](evidence/real-world-tests-20261022/final-owned-stack-cleanup.json) confirms stopped owned processes, free owned ports, and a removed lock.

The existing 22-case suite was not rerun. Remote UAT execution remains unavailable.
Eight-hour timer firing and device sleep remain untested.

The [selected specification review](evidence/real-world-tests-20261022/gherkin-validation-v3.json) leaves local scenarios `UNVERIFIED`.
Remote setup has three mandatory component-identity gaps. Remote verification remains blocked.
Owner: unknown test automation owner. Next action: inspect target controls and record semantic review before remote verification.
These specification limits do not change retained execution outcomes.

## Read this first

| Status | Key point | Details |
| --- | --- | --- |
| UAT access deadline | The photograph shows almost eight hours. BFF configuration contains a matching 480-minute value. | [UAT inquiry](#uat-timeout-inquiry-21-october-2026). Effective UAT configuration remains unverified. |
| 🔴 Two P2 regressions | E2E-06 passes after the active-cutoff correction. Stale-response reuse can still end a fresh session. | [Current findings](code-review-minor-20261021.md#review-findings) and [successor assessment](10-release-confidence-active-cutoff-20261025.md#findings). |
| 🟠 Inherited recovery defect | Both versions logout after delayed credentials arrive. | [Old/new comparison](code-review-minor-20261021.md#inherited-delayed-refresh-recovery). |
| 🟡 P3 timer issue | Request count changes. No user-visible difference was demonstrated. | [Timer finding](code-review-minor-20261021.md#f-02-p3-permit-acquisition-when-its-timer-runs-slightly-late). |
| ✅ Local checks complete | Compiler passes. 413 runner passes include one expected failure. | [Latest checks](code-review-minor-20261021.md#fresh-branch-review-21-october-2026). |
| ⏳ Acceptance open | E2E-07, stale-session recovery, delayed recovery, and PROD artifact evidence remain unresolved. | [Decisions and blockers](#unknowns-and-blockers) and [successor assessment](10-release-confidence-active-cutoff-20261025.md#readiness-conclusion-and-authorization). |

Use [case definitions](test-cases.md#catalog-navigation) for steps and assertions.
Use the [execution report](test-execution-report.md#assertions-and-outcomes) for historical browser outcomes.
Use the [evidence index](evidence/index.md) for source records and historical documents.

## Request and source facts

The user reported a missing timeout dialog after deploying the MFE to UAT on 21 October 2026.
The reported wait includes a return after approximately thirty minutes. A later UAT photograph exposes the calculated timer delay.
The user identifies the latest `feature/session-refresh-minor` commit and an untouched background tab containing Cashflow Blotter.
The [correction](evidence/uat-timeout-inquiry-20261021/blotter-correction.txt) supersedes the earlier Cashflow Dashboard identification.
The exact deployed artifact, blotter version, and effective session settings remain unverified.
The user asks whether this behavior is expected and whether previous review identified it.
The [UAT inquiry](evidence/uat-timeout-inquiry-20261021/user-request.txt) preserves the report and clarification answers.

The user selected `feature/session-refresh-minor` to reduce application changes.
The [scope request](evidence/minor-branch-rerun-20261020/user-request.txt) requires background recovery and permits discussion of broader deferrals after execution.
The [latest code-review request](evidence/code-review-refresh-20261021/inputs.json) authorized review and local validation against `main`.
The current inquiry adds an incident report and a corrected application identity.
No business criterion changed. The [candidate requirement](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria) remains version 4, pending publication review.

## Stage boundary and readiness

| Field | Current assessment |
| --- | --- |
| Named phase | Local branch review against main; complete. |
| Readiness | `READY` for that named review phase only. |
| Assessor and time | Codex; timestamps in [review inputs](evidence/code-review-refresh-20261021/inputs.json). |
| Rationale | Exact source review and fresh paired checks support the completed review. |
| Baseline | `f025513f696476a9cc8162681410cbd21e029bcb`. |
| Runtime candidate | `6d4c37c839b99d14ea41fd936da1a36cda526b17`. |
| Reviewed head | `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85`; later changes repair tests only. |
| Frozen intake | [Original issue](intake.md); Git `cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c`; SHA-256 `1650a20f8a2aba2105b30b8abc4bd2a881f58ee335925a3daa9f6a6c0d0e0948`. |
| Preservation | [Review integrity](evidence/code-review-refresh-20261021/integrity.json) retains source, refs, intake, and pre-existing build-cache hashes. |
| Pending actions | Runtime correction requires separate scope. Acceptance decisions and release approval remain open. |
| Owners | User for scope decisions; unknown application, authentication, and release owners. |

Review readiness does not establish acceptance, successful recovery, or production readiness.
Documentation checks and preserved evidence hashes appear in the [clarity checks](evidence/document-clarity-20261021/validation.json).

## Proposed change

The application changes were already implemented when review began.
The earlier [test repair](evidence/baseline-reassessment-20261021/commit-binding.json) changed two test files and preserved runtime bytes.
The latest review made no application changes. Runtime suggestions remain unapplied.
This revision records the supplied photograph, actual Blotter browser controls, and the configuration diagnosis.

## Scope and affected artifacts

| Artifact | Exact source | Effect and limit | Owner |
| --- | --- | --- | --- |
| `mfe-base` | Runtime and reviewed head above. | Local review covers authentication, Home lifecycle, request, and Timeout paths. | unknown application owner |
| Executed browser tests | `ratan-test-engine` `7a504c13a8d51bb52af5cc89bd4af88d1988da94`. | 22 cases completed on 20 October. Results retain their original assertions. | unknown test owner |
| Reorganized Robot modules | `ratan-test-engine` `975af64c55303ee4a138968813ef4e85570f96d2`. | [Offline checks passed](evidence/robot-case-modules-20261021/offline-checks.json). Business execution remains `NOT_RUN`. | unknown test owner |
| Local BFF fixtures | `85d7cc03eb12710d6facf581987fd4ae24fc9844`. | Synthetic provider adapters limit integration claims. | unknown service owner |
| Task documents | Current stage, review, execution report, catalog, and index. | Low editorial risk. Frozen documents and retained execution bytes remain unchanged. | Codex |

## UAT timeout inquiry: 21 October 2026

**The supplied UAT photograph shows almost eight hours before the access-popup callback.**
The frontend conversion uses correct units. The BFF launch configuration contains a matching 480-minute value.
Effective UAT configuration and clock agreement remain unverified.
The [execution request](evidence/uat-blotter-browser-20261021/user-request.txt) and [photograph request](evidence/uat-blotter-browser-20261021/uat-screenshot/user-request.txt) preserve the user's scope.
Cashflow Blotter supersedes Dashboard through the [recorded correction](evidence/uat-timeout-inquiry-20261021/blotter-correction.txt).

### Photograph and source diagnosis

| Claim | Class | Evidence | Limit |
| --- | --- | --- | --- |
| The photograph shows `expiredIn = 1792599728` and `difftime = 28788109` milliseconds. | Observed UAT capture | [Original photograph](evidence/uat-blotter-browser-20261021/uat-screenshot/IMG_3180.HEIC), [extracted values](evidence/uat-blotter-browser-20261021/uat-screenshot/observation.json). | Execution is paused before `setTimeout`. No JWT `iat` is visible. |
| The delay equals 7 hours, 59 minutes, 48.109 seconds. | Arithmetic | [Independent calculation](evidence/uat-blotter-browser-20261021/uat-screenshot/timing-contract-source-receipt.json). | This measures remaining access time, not the complete session policy. |
| `expiredIn` comes from JWT `exp`. The conversion uses epoch seconds and milliseconds. | Inspected implementation | [Decoder ingestion](../../repos/ui/mfe-base/src/utils/login.ts#L26), [Home timer](../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L92). | No timezone conversion occurs. The screenshot cannot establish browser/server clock agreement. |
| BFF `app.conf` contains `-Djwt.tokenExpiration=480`. YAML declares a fifteen-minute default. | Inspected configuration | [Launch value](../../repos/services/single-ui-bff/app.conf#L2), [default](../../repos/services/single-ui-bff/src/main/resources/application.yml#L33). | A JVM property can override YAML. UAT launcher inputs remain unavailable. |
| The BFF adds configured minutes to current epoch milliseconds when issuing access tokens. | Inspected implementation | [JWT generation](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/JwtTokenUtil.java#L49), [hashed source receipt](evidence/uat-blotter-browser-20261021/uat-screenshot/timing-contract-source-receipt.json). | Exact UAT artifact binding remains unavailable. |
| A 480-minute access token closely explains the photographed delay. | Inference | Eight hours minus the delay equals 11.891 seconds. [Calculation](evidence/uat-blotter-browser-20261021/uat-screenshot/observation.json). | Missing `iat` prevents distinguishing token lifetime from clock skew conclusively. |
| Refresh expiry can independently open Timeout before access expiry. | Inspected implementation | [Reconciliation](../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L119), [refresh timer](../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L171). | UAT refresh metadata remains unavailable. Backend absolute expiry can also reject requests earlier. |

The frontend calculation is:

```ts
const difftime = 1000 * store.expiredIn - Date.now();
```

JWT `exp` uses epoch seconds. `Date.now()` uses epoch milliseconds. The conversion is dimensionally correct.
The photographed value is below the browser's signed 32-bit timer limit. Timer overflow does not explain this value.
An eight-hour access deadline cannot expire after thirty minutes. This is implemented token-expiry behavior, not confirmed business acceptance.

Owner: unknown authentication owner. Next action: identify effective `jwt.tokenExpiration` and its property source in UAT.
Compare JWT `exp - iat` with server and browser time. Retain metadata without exposing the complete token.
Do not replace the timer with an arbitrary thirty-minute constant. No approved replacement threshold is recorded.

### Actual Blotter browser controls

The current shell, Ratan container, and supplied Blotter source ran in native Edge with real elapsed time.
The [source binding](evidence/uat-blotter-browser-20261021/setup/shell-source-binding.json) and [build setup](evidence/uat-blotter-browser-20261021/setup/build-setup-binding.json) record exact bytes and substitutions.
Shortened BFF lifetimes keep deadline controls practical. These executions do not establish UAT configuration parity.

| Canonical case | Actual result | Supported conclusion and limit |
| --- | --- | --- |
| [UAT-BLOTTER-VISIBLE](test-cases.md#uat-blotter-visible) | **PASSED**, 3 assertions. [Result](evidence/uat-blotter-browser-20261021/browser/blotter-visible-01/result.json). | Fixed expiry opens Timeout in the visible Blotter session. |
| [UAT-BLOTTER-HIDDEN](test-cases.md#uat-blotter-hidden) | **PASSED**, 4 assertions. [Result](evidence/uat-blotter-browser-20261021/browser/blotter-hidden-01/result.json). | Timeout opens while genuinely hidden and remains visible after return. |
| [UAT-BLOTTER-LATE-RETURN](test-cases.md#uat-blotter-late-return) | **PASSED**, 6 assertions. [Result](evidence/uat-blotter-browser-20261021/browser/blotter-late-return-01/result.json). | Timeout can open and close before return after acquired refresh expires. Final state shows Sign in. |
| [UAT-BLOTTER-PRIOR-TILE](test-cases.md#uat-blotter-prior-tile) | **FAILED**, 5 of 7 assertions passed. [Result](evidence/uat-blotter-browser-20261021/browser/blotter-prior-tile-02/result.json). | Retained Dashboard polling renewed access. Pointer activity invalidated the subsequent removal control. |
| [UAT-BLOTTER-480-SCHEDULE](test-cases.md#uat-blotter-480-schedule) | **PASSED**, 6 assertions. [Result](evidence/uat-blotter-browser-20261021/browser/blotter-480-schedule-03/result.json). | Actual 480-minute BFF issuance schedules a matching Home timer. No eight-hour wait was performed. |
| [UAT-BLOTTER-NO-REFRESH](test-cases.md#uat-blotter-no-refresh) | **NOT_RUN**. | Actual acquired-refresh expiry was prioritized. The rejected-acquisition branch remains unverified. |

The four idle cases contain twenty assertions. Eighteen passed. Two failed in the contaminated removal control.
The additional scheduling case passed six assertions. Five executed cases therefore contain twenty-six assertions, with twenty-four passes.
The local JVM property produced an access lifetime of 28,800 seconds.
The browser recorded a matching 28,799,107-millisecond access-popup timer and a separate refresh timer.
No Timeout appeared during 15,017 real milliseconds. Eventual eight-hour timer firing was not tested.
A prior smoke encountered invalid SockJS fixture data. Another attempt failed before native browser startup.
Two scheduling setup attempts failed readiness. An invalid driver precondition and timer-stack classification also required correction.
Their retained failures remain separate from the passing final scheduling case.
The [reconciliation](evidence/uat-blotter-browser-20261021/summary.json) retains these failures and exact execution boundaries.
The [screenshot index](evidence/uat-blotter-browser-20261021/screenshots.json) binds captures to cases, checkpoints, timestamps, and limits.
The [independent audit](evidence/uat-blotter-browser-20261021/browser-audit.json) confirms the four idle-case predicates and source bindings.
A secondary baseline-driver ancestry hash remains unresolved. The exact executed driver snapshots match their results.

The user did not report opening Dashboard. Its conditional polling mechanism does not establish this incident's cause.
No measured successful renewal moved expiry in the visible, hidden, or late-return Blotter controls.
CDP and passive observers remained attached. Natural freezing and device sleep were not tested.
Synthetic identity, catalog, entitlements, empty business data, and notification failure replace unavailable external services.
Toolkit presentation components and two dependency versions differ from the supplied manifests. Setup evidence records those limits.

### Earlier review coverage

The original [R-001](code-review.md#review-findings) identified API renewal outside activity and visibility checks.
The [impact boundary](impact-analysis.md#user-view) left representative embedded idle execution open.
Those findings describe a separate mechanism. They did not establish the eight-hour UAT lifetime discrepancy.
Earlier local browser execution used shortened lifetimes. It could show the dialog without validating effective deployment settings.
The [review audit](evidence/uat-blotter-browser-20261021/review-audit.json) preserves the earlier coverage boundary.
The [configuration audit](evidence/uat-blotter-browser-20261021/uat-screenshot/review-config-audit.json) checked six committed reports at Workbench `3703b7df`.
None identified the packaged 480-minute value against the fifteen-minute YAML default within that audited scope.
This configuration discrepancy was missed. The reports explicitly left deployed settings unverified.

### Intended, old, and new behavior

Setup: use equivalent access credentials, clock agreement, and unchanged BFF lifetime configuration.
The [source comparison](evidence/uat-blotter-browser-20261021/baseline-comparison.json) binds exact old and new revisions.

1. Sign in and open Cashflow Blotter.
2. Record JWT issue and expiry metadata.
3. Leave the portal untouched in the background.
4. Compare the scheduled delay with credential expiry.

| Result | Evidence and boundary |
| --- | --- |
| Intended | The [candidate requirement](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria) remains unpublished. No new thirty-minute threshold is inferred. |
| Old | Baseline `f025513f696476a9cc8162681410cbd21e029bcb` uses the same access-expiry calculation. An eight-hour credential predicts an eight-hour access timer. Baseline browser execution did not run here. |
| New | Head `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85` retains that calculation. Browser controls show Timeout at fixed expiry. Refresh-expiry reconciliation can act earlier. |
| Reported UAT | The user reports no dialog after thirty minutes. The photograph shows almost eight hours before access expiry. |
| Classification | The access calculation and BFF 480-minute value are inherited source behavior. An introduced arithmetic regression is unsupported. |

### Decision and evidence limits

The source diagnosis, four idle cases, and one scheduling case are complete within their recorded boundaries.
UAT configuration-origin confirmation remains **READY_WITH_LIMITS** for evidence collection only.
Owner: unknown authentication owner. Effective UAT configuration correction and idle-timeout acceptance remain blocked.
Next action: bind effective configuration, JWT lifetime, refresh expiry, and clock agreement to the deployed artifact.
No application correction or criterion waiver is recorded. Source diagnosis does not establish release approval.
Knowledge update: not applicable. These incident observations change no domain rule.

## User impact

| Condition | Before and after | Consequence and evidence |
| --- | --- | --- |
| Initial refresh expires while renewed access remains valid. | Baseline keeps access. Candidate logs out if refresh remains unreplaced. | Sign-in interrupts active work. [REVIEW-F01](test-cases.md#review-f01). |
| An ended session returns a late refresh response. | Candidate persistence and reuse prevent replacement in two controlled conditions. | Recovery can clear a fresh session. [REVIEW-F03A](test-cases.md#review-f03a), [REVIEW-F03B](test-cases.md#review-f03b). |
| Usable refresh arrives after access expires. | Both versions leave Extend disabled and logout. | Required delayed recovery remains unmet. [REVIEW-DELAYED-SCHEDULED](test-cases.md#review-delayed-scheduled). |
| Acquisition callback runs one millisecond late. | Baseline sends one request. Candidate sends zero. | No user-visible difference was demonstrated. [REVIEW-F02](test-cases.md#review-f02). |

The [network explanation](code-review-minor-20261021.md#continuous-activity-and-network-actions) defines mouse activity and the five-second delay.
Aborting a pending refresh can reduce the stale-response race. It cannot correct active cutoff without a pending request.

## System impact

Lifecycle timers, credential persistence, and late responses cross authentication boundaries. The qualitative review risk remains medium.
The [inspection inventory](evidence/code-review-20261021/inspection.json) and [fresh inputs](evidence/code-review-refresh-20261021/inputs.json) retain affected consumers.
Controlled fixtures establish behavior differences. Deployed settings, provider behavior, and production failure frequency remain unverified.

## Options and consequences

| Option | Consequence | Decision owner |
| --- | --- | --- |
| Require all existing criteria. | Each unmet criterion remains an acceptance blocker. | user |
| Defer named broader criteria. | Specific adverse behavior remains accepted only through an explicit recorded decision. | user |
| Correct the demonstrated runtime defects. | Implementation scope and regression evidence must address the selected conditions. | user and unknown application owner |

## Proposed acceptance and validation

| Scope | Retained result | Definition and evidence |
| --- | --- | --- |
| Required background recovery | Immediate-response probe passed; delayed-response probe failed. | [Immediate case](test-cases.md#probe-natural-immediate), [delayed case](test-cases.md#probe-delayed-refresh). |
| 22 browser cases | Five passed; fourteen failed; one diagnostic failed; two observations. | [Browser outcomes](test-execution-report.md#assertions-and-outcomes). |
| Latest local checks | 116 suites; 413 runner passes, including one expected failure. Compiler passes. | [Latest validation](code-review-minor-20261021.md#fresh-branch-review-21-october-2026). |
| Production build and deployment | `NOT_RUN`; local checks do not establish production parity. | [Build boundary](test-execution-report.md#unit-execution-and-build-readiness). |

## Implementation and release proposal

Runtime corrections remain unapplied. No production release is proposed by this review.
Required natural browser cases use at least 30 minutes of actual hidden time.
A later implementation stage must bind its exact source and repeat the affected assertions.

## Sources and evidence limits

The [sequential-fix request](evidence/minor-fixes-20261025/user-request.txt) is `SRC-session-sequential-minor-fixes-20261025`.
Its [phase inputs](evidence/minor-fixes-20261025/inputs.json) preserve the baseline and implementation authorization.

The [coverage inquiry](evidence/coverage-detection-audit-20261024/user-request.txt) is `SRC-session-coverage-detection-request-20261024`.
Its [audit inputs](evidence/coverage-detection-audit-20261024/inputs.json) preserve the high-priority reference and selected revisions.

The [minimal-fix request](evidence/minimal-blocker-fixes-20261023/user-request.txt) is `SRC-session-minimal-request-20261023`.
Its exact bytes and source details appear in the [proposal inventory](evidence/minimal-blocker-fixes-20261023/source-inventory.json).

| Source ID | Locator | Identity and limit |
| --- | --- | --- |
| SRC-session-release-source-20261022 | [Assessment](10-release-confidence.md), [source review](evidence/release-confidence-20261022/source-review.json), [coverage](evidence/release-confidence-20261022/coverage-review.json) | Current candidate remains unchanged. Technical recommendation: do not promote. Target deployment evidence remains incomplete. |
| SRC-session-uat-screenshot-20261021 | [Original photograph](evidence/uat-blotter-browser-20261021/uat-screenshot/IMG_3180.HEIC), [values](evidence/uat-blotter-browser-20261021/uat-screenshot/observation.json), [source receipt](evidence/uat-blotter-browser-20261021/uat-screenshot/timing-contract-source-receipt.json). | UAT access delay observed. Active property source, refresh metadata, and clock agreement remain unverified. |
| SRC-session-uat-blotter-browser-20261021 | [Results](evidence/uat-blotter-browser-20261021/summary.json), [source binding](evidence/uat-blotter-browser-20261021/setup/shell-source-binding.json). | Actual current shell and supplied Blotter. Local substitutions limit deployment claims. |
| SRC-session-uat-timeout-inquiry-20261021 | [Original answers](evidence/uat-timeout-inquiry-20261021/user-request.txt), [blotter correction](evidence/uat-timeout-inquiry-20261021/blotter-correction.txt), [corrected receipt](evidence/uat-timeout-inquiry-20261021/blotter-analysis.json). | Latest minor branch reported in UAT. Cashflow Blotter supersedes Dashboard. The photograph supersedes the earlier missing-capture boundary. |
| SRC-session-branch-refresh-20261021 | [Inputs](evidence/code-review-refresh-20261021/inputs.json), [reconciliation](evidence/code-review-refresh-20261021/summary.json). | Exact endpoints above; fresh local review only. |
| SRC-session-review-intent-v4 | [Requirement](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria). | Version 4; SHA-256 `828d62209f11dd9bb9dee893ddc80e7e5d4dc6abd3c58170e902dab61bc587aa`; publication review pending. |
| SRC-session-minor-stage-20261020 | [Scope request](evidence/minor-branch-rerun-20261020/user-request.txt), [stage baseline](evidence/minor-branch-rerun-20261020/stage-baseline.json). | Original authorization and source hashes; no criterion waiver. |
| SRC-session-baseline-reassessment-20261021 | [Stage inputs](evidence/baseline-reassessment-20261021/stage-inputs.json), [commit binding](evidence/baseline-reassessment-20261021/commit-binding.json). | Test-only repair and paired comparisons; controlled fixtures. |
| SRC-session-minor-browser-20261020 | [Browser manifest](evidence/minor-branch-rerun-20261020/browser-manifest.json). | 22 retained outcomes, screenshots, hashes, and separate probes. |
| Prior stage record | [Immutable stage version 1](evidence/minor-branch-rerun-20261020/prior-documents/change-review.v1.52f733b.md.snapshot). | SHA-256 `6c8bdbc8ee3ca13696b9544f729e0c449f73b3594193a9bb1aa17558795a3de8`; historical broader implementation. |

## Unknowns and blockers

| Decision or missing evidence | Blocked action | Owner | Next action |
| --- | --- | --- | --- |
| Two current runtime regressions remain unresolved. | Positive technical release recommendation. | unknown application owner | Correct [active cutoff](10-release-confidence.md#rc-01-active-access-can-end) and [stale-session recovery](10-release-confidence.md#rc-02-stale-responses-can-clear-a-fresh-session), then retain passing cases. |
| The eight-hour UAT access delay lacks an effective configuration source and clock binding. | UAT configuration correction and idle-timeout acceptance. | unknown authentication owner | Bind `exp - iat`, refresh expiry, clocks, and effective property origin. [Inquiry](#uat-timeout-inquiry-21-october-2026). |
| Required delayed recovery remains failed. | Acceptance of the full required background scope. | user and unknown authentication owner | Decide a targeted correction or an explicit fallback policy. [Failed probe](evidence/minor-branch-rerun-20261020/supplemental/delayed-refresh/analysis.json). |
| Broader criterion deferrals are unnamed. | Acceptance waiver claims. | user | Review [failure recommendations](test-execution-report.md#failure-limits-and-recommended-dispositions) and name each decision. |
| Deployed settings, provider paths, and build evidence are unavailable. | Production readiness and release approval. | unknown release owner | Bind representative deployment and build evidence before a release decision. |
| Current rollback target, response procedures, and decision owners remain unbound. | Production recovery and deployment handoff. | unknown release owner | Retain applicable artifacts, triggers, operator evidence, and actual decisions. [Operational findings](10-release-confidence.md#rc-04-prod-artifact-and-operating-evidence-remain-incomplete). |

## Stage evidence and completion

| Stage | Status | Evidence and remaining action |
| --- | --- | --- |
| Local review and comparative checks | `READY`; complete. | [Latest review](code-review-minor-20261021.md#fresh-branch-review-21-october-2026). Runtime defects remain open. |
| Browser evidence collection | `READY`; complete for the historical selected runtime. | [Execution report](test-execution-report.md). Review failures before acceptance. |
| Actual Blotter controls | Complete for five local cases. | [Reconciliation](evidence/uat-blotter-browser-20261021/summary.json). Four pass; one contaminated comparison fails. UAT settings remain unverified. |
| UAT configuration diagnosis | `READY_WITH_LIMITS`; evidence collection only. | The photograph proves the access delay. Effective UAT property origin remains unresolved. |
| Documentation clarity | Complete after the linked checks. | [Validation](evidence/document-clarity-20261021/validation.json). Full ASD review remains pending. |
| Acceptance and release | No approval recorded. | Resolve the [named blockers](#unknowns-and-blockers). |

## Requested decision and actual disposition

The user requested a smaller change and evidence before deciding broader deferrals.
No named failure is accepted. No criterion waiver is recorded.
Correct or explicitly decide delayed recovery before accepting the required background scope.
The two demonstrated P2 regressions remain open. Unrestricted production rollout is not recommended.

## Saved execution and interruption recovery

Checkpoint `bd36532` retains completed browser cases and screenshots.
The [integrity review](evidence/minor-branch-rerun-20261020/integrity-review.json) reconciles their source bindings and checkpoints.
The [progress record](evidence/baseline-reassessment-20261021/progress.json) preserves completed comparisons, failures, and the initial runner error.

## Initial branch code review: 21 October 2026

**📚 Historical:** the initial review reported four findings and two compiler errors.
The [initial inputs](evidence/code-review-20261021/inputs.json) retain those results.
The later repair resolves the compiler finding. Current findings supersede the original four-open-findings conclusion.

## Test repair and baseline reassessment: 21 October 2026

**📚 Historical:** the [authorized test repair](evidence/baseline-reassessment-20261021/user-request.txt) changed two test files.
The [commit binding](evidence/baseline-reassessment-20261021/commit-binding.json) preserves all 283 recorded runtime and configuration hashes.
The [paired lifecycle results](evidence/baseline-reassessment-20261021/lifecycle/analysis.json) distinguish active cutoff from inherited delayed recovery.
The [race results](evidence/baseline-reassessment-20261021/races/analysis.json) distinguish added, worsened, and unchanged conditions.

## Gap case clarification and reusable rules: 21 October 2026

**📚 Historical:** the [case-step request](evidence/gap-case-steps-20261021/user-request.txt) required readable old/new comparisons.
The [canonical catalog](test-cases.md#current-branch-review-cases) now owns detailed case steps and assertions.
The [comparison rule](../README.md#compare-behavior-for-gap-analysis) applies to later gap analyses.
This clarification changed no business criterion or observed result.

## Fresh branch review: 21 October 2026

**✅ Latest completed code review:** all 15 changed paths received source review.
The [review](code-review-minor-20261021.md#fresh-branch-review-21-october-2026) owns execution details and limits.
The [clarification answers](evidence/code-review-refresh-20261021/clarification.json) explain active cutoff, response aborts, inherited recovery, and timer impact.
No application edit or business-rule change occurred during that review.
