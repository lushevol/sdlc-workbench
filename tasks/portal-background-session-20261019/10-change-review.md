---
artifact_kind: change-request
id: CHANGE-session-post-review-20261020
version: 15
status: draft
owner: unknown
source_refs:
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

> **Do not promote the current minor candidate to PROD.**
> Action: resolve the current session regressions and required delayed recovery, then reassess the exact release artifact.
> Consequence: active work or fresh-session recovery can end. A positive PROD handoff remains blocked.
> Owner: unknown application, authentication, and release owners.
> Evidence: [release confidence assessment](10-release-confidence.md#findings) and [current source review](evidence/release-confidence-20261022/source-review.json).
> Evidence confidence is high for this technical hold. PROD frequency remains unknown.

> **Action required: verify the eight-hour UAT access lifetime.**
> The photograph shows `difftime = 28,788,109` milliseconds. This equals 7 hours, 59 minutes, 48.109 seconds.
> Action: confirm the effective BFF property source, JWT lifetime, and clock agreement.
> Consequence: the photographed access timer cannot expire within thirty minutes. UAT configuration correction remains blocked.
> Owner: unknown authentication owner. Evidence: [photograph](evidence/uat-blotter-browser-20261021/uat-screenshot/observation.json) and [source receipt](evidence/uat-blotter-browser-20261021/uat-screenshot/timing-contract-source-receipt.json).
> The BFF contains `jwt.tokenExpiration=480`. Its use in UAT remains inferred. Refresh expiry can trigger an earlier dialog.

> **🔴 Action required: two P2 regressions remain.**
> Correct [active-session cutoff](code-review-minor-20261021.md#f-01-p2-preserve-active-access-across-the-refresh-deadline) and [stale-credential reuse](code-review-minor-20261021.md#f-03-p2-stop-stale-credential-persistence-and-reuse).
> Consequence: active access can end; stale credentials can clear a fresh session.
> Owner: unknown application owner. Evidence: [paired results](evidence/code-review-refresh-20261021/summary.json).
>
> **👤 Decision required: delayed recovery and broader deferrals remain open.**
> Decide whether to correct delayed recovery or explicitly accept a named fallback.
> Name each broader criterion proposed for deferral. Acceptance remains open until those decisions are recorded.
> Owner: user and unknown authentication owner. Evidence: [failed recovery](test-cases.md#review-delayed-scheduled) and [scope request](evidence/minor-branch-rerun-20261020/user-request.txt).
> Controlled local evidence does not establish production frequency or release approval.

## Current coverage inquiry: 24 October 2026

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

## Current task state

| Item | Current assessment |
| --- | --- |
| Latest request | [Audit coverage and earlier detection](evidence/coverage-detection-audit-20261024/user-request.txt) for the three runtime issues. |
| Source | `feature/session-refresh-minor`; `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85`. Runtime remains unchanged from retained failure evidence. |
| Named phase | Retrospective test-evidence audit: `READY`; [audit complete](09-test-detection-audit.md). Current source and retained history support its conclusions. |
| Result | [DO_NOT_RECOMMEND; HIGH evidence confidence](10-release-confidence.md#readiness-conclusion-and-authorization). No production success probability is claimed. |
| Blocking conditions | [Active cutoff](10-release-confidence.md#rc-01-active-access-can-end), [stale-session recovery](10-release-confidence.md#rc-02-stale-responses-can-clear-a-fresh-session), and [required delayed recovery](10-release-confidence.md#rc-03-required-delayed-recovery-remains-unmet). |
| Target limits | [Build, configuration, release composition, rollback, and operational ownership](10-release-confidence.md#rc-04-prod-artifact-and-operating-evidence-remain-incomplete) remain unbound. |
| Next action | Unknown application owner: correct the demonstrated runtime conditions and retain matching passing cases. Release owner: bind the actual artifact and target. |
| Decisions | No named criterion waiver or completed deployment authorization was found. Use the [living decision table](#unknowns-and-blockers). |

## Minimal correction proposal: 23 October 2026

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
| 🔴 Two P2 regressions | Active cutoff is conditional. Stale-response reuse can end a fresh session. | [Current findings](code-review-minor-20261021.md#review-findings). |
| 🟠 Inherited recovery defect | Both versions logout after delayed credentials arrive. | [Old/new comparison](code-review-minor-20261021.md#inherited-delayed-refresh-recovery). |
| 🟡 P3 timer issue | Request count changes. No user-visible difference was demonstrated. | [Timer finding](code-review-minor-20261021.md#f-02-p3-permit-acquisition-when-its-timer-runs-slightly-late). |
| ✅ Local checks complete | Compiler passes. 413 runner passes include one expected failure. | [Latest checks](code-review-minor-20261021.md#fresh-branch-review-21-october-2026). |
| ⏳ Acceptance open | No criterion waiver or release approval is recorded. | [Decisions and blockers](#unknowns-and-blockers). |

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
