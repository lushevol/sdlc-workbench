---
artifact_kind: pull-request-review
id: REVIEW-session-minor-20261021
version: 4
status: draft
owner: unknown
source_refs:
  - SRC-session-branch-refresh-20261021
  - SRC-session-baseline-reassessment-20261021
  - SRC-mfe-code-review-20261021
  - SRC-session-review-intent-v4
related_ids:
  - DEFECT-portal-background-session-20261019
  - CHANGE-session-post-review-20261020
  - REQ-active-session-renewal
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

# Minor session branch code review

> **Critical conclusions: Action required**
>
> **Two P2 regressions remain after baseline comparison.**
> Action: correct [active-session logout](#f-01-p2-preserve-active-access-across-the-refresh-deadline) and [stale-credential reuse](#f-03-p2-stop-stale-credential-persistence-and-reuse), then validate their paired cases.
> Consequence: valid active access can end; recovery can clear a fresh session.
> Owner: unknown application owner. Evidence: [lifecycle comparison](evidence/baseline-reassessment-20261021/lifecycle/analysis.json) and [race comparison](evidence/baseline-reassessment-20261021/races/analysis.json).
> These controlled fixtures establish changed behavior. They do not measure production failure frequency.
>
> **Delayed recovery remains an inherited limitation.**
> Action: retain its [known-defect status](#inherited-delayed-refresh-recovery) when assessing required recovery.
> Consequence: late usable credentials cannot enable Extend. Passing expected-failure checks do not establish recovery.
> Owner: unknown application owner; user for acceptance decisions. Evidence: [paired outcomes](evidence/baseline-reassessment-20261021/lifecycle/analysis.json).

## Fresh branch review: 21 October 2026

The [current request](evidence/code-review-refresh-20261021/inputs.json) asks for the current branch review against `main`.
The comparison uses merge base `f025513f696476a9cc8162681410cbd21e029bcb` and head `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85`.
All 15 changed files received source review. Independent passes covered lifecycle, credentials, configuration, and test assertions.
The three findings below remain confirmed. No additional actionable defect was established.

| Check | Current result | Evidence and limit |
| --- | --- | --- |
| Full existing Jest suite | 116 suites and 413 runner passes. This includes 412 ordinary checks and one expected failure. | [Execution](evidence/code-review-refresh-20261021/suite-suite-suite/run.json). Forced exit does not establish open-handle freedom. |
| Existing paired diagnostics | Twelve executions confirm six paired conditions at the selected commits. | [Reconciliation](evidence/code-review-refresh-20261021/summary.json). Characterization passes include adverse behavior. |
| TypeScript | Passed with declaration output and incremental output disabled. | [Execution](evidence/code-review-refresh-20261021/types-corrected/run.json). |
| Initial compiler invocation | Inherited declaration settings conflicted with `--noEmit`. No source error was established. | [Initial attempt](evidence/code-review-refresh-20261021/types-suite-types/run.json). The corrected invocation passed. |
| Secret candidates | Eight matches are synthetic test fixtures. No credential finding was established. | [Redacted scan](evidence/code-review-refresh-20261021/scan.json). Pattern checks do not establish complete credential absence. |
| Checkout preservation | Tracked source, reviewed refs, staged content, intake, and existing build-cache bytes remain unchanged. | [Final integrity](evidence/code-review-refresh-20261021/integrity.json). |

Each diagnostic was copied from retained evidence without assertion changes.
The [execution setup](evidence/code-review-refresh-20261021/execution-setup.json) binds exported files, diagnostic hashes, dependencies, and tool versions.
The [document checks](evidence/code-review-refresh-20261021/document-validation.json) pass with eight warnings. Full ASD writing review remains pending.
Installed dependencies were shared through a symlink. No installation or historical dependency recreation occurred.
Controlled clocks, JSDOM, and synthetic service adapters limit the behavior claims.
No fresh browser, production build, live provider, or remote analyzer execution occurred.
The external deployment template was unavailable locally. Deployment behavior remains unverified.
The frozen intake and candidate requirement version 4 remain unchanged. No new knowledge clarification occurred.

## Read the case steps

The access token permits current portal use. The refresh token can obtain a new access token.
An expired access token can therefore need recovery through a usable refresh token.
A revoked refresh token cannot provide recovery, even when its expiry time is later.

Old means runtime commit `f025513f696476a9cc8162681410cbd21e029bcb`.
New means runtime commit `6d4c37c839b99d14ea41fd936da1a36cda526b17`.
The later test-only commit is `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85`.
It does not change the new runtime behavior.

Use the same setup and steps for both versions unless a case states a controlled difference.
These steps describe retained automated investigations. They do not claim manual reproduction on a deployed portal.
Actor: the automated test. It controls time and server responses.
Sign-in, logout, and recovery steps call application service functions. Each case states the resulting limits.

## Review findings

### F-01: [P2] Preserve active access across the refresh deadline

**User case:** A user continues work, but the new version ends the session.

Setup: start each version with valid access and the same initial refresh token.
The test sets access validity to 15 minutes and initial refresh validity to four hours.
These values are test settings. They do not define production session policy.

1. Advance the test clock by ten minutes.
2. Configure a successful response for the next access-extension request.
3. Send a mouse movement event to the workspace.
4. Advance the clock by five seconds to deliver the extension response.
5. Confirm that the access extension succeeds.
6. Repeat steps 1 through 5 until 23 extensions succeed.
7. Confirm that current access remains valid beyond the initial refresh expiry time.
8. Advance the clock to the initial refresh expiry time.
9. Advance the clock by one more second.
10. Check authentication state and the number of logout requests.

Expected result: continued successful activity does not cause fresh authentication solely because the initial refresh token expires.
Definition: [AC-4](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L158-L162), requirement version 4.

| Observation | Old version | New version |
| --- | --- | --- |
| Successful access extensions | 23 | 23 |
| Access remains valid at initial refresh expiry | Yes | Yes |
| Logout requests | Zero | One |
| Authentication after the deadline | Remains available | Cleared |

**Difference:** the new version adds logout while access remains valid. The old version preserves the active session.
Classification: introduced regression; retain P2.
Consequence: the user loses the active session and must sign in again.

Owner: unknown application owner.
Next action: preserve active access when the initial refresh token expires. Repeat these steps after correction.

Evidence: [old execution](evidence/baseline-reassessment-20261021/lifecycle/active_cutoff-baseline/run.json), [new execution](evidence/baseline-reassessment-20261021/lifecycle/active_cutoff-candidate/run.json), and [observed states](evidence/baseline-reassessment-20261021/lifecycle/analysis.json).
Assertions: [paired test](evidence/baseline-reassessment-20261021/lifecycle/diagnostic.test.tsx.snapshot#L73-L94).
Cause: the [expiry condition](../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L117-L123) also checks refresh expiry.
Its [timer](../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L171-L173) opens Timeout while current access remains valid.
The [Timeout controller](../../repos/ui/mfe-base/src/components/Timeout/common/useController.ts#L25-L52) then starts logout.

Limit: both versions receive equal initial refresh credentials. The test compares expiry handling, not acquisition during tab hiding.

### F-03: [P2] Stop stale-credential persistence and reuse

**User case:** a response from an ended session interferes with recovery of a new session.
Session A is the ended session. Session B is the new session.
These names identify sessions. They do not establish access to another user's session.

Review expectation: recover session B with a usable refresh token for session B.
The [service session check](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v1/implementation/SessionServiceImplementation.java#L28-L33) rejects revoked session credentials.
A separate approved criterion for late-response handling is unavailable.
This expectation follows the inspected session boundary. It is not a new approved requirement.

#### Case F-03A: The old response arrives before the new sign-in

Setup: session A has a valid access token. No refresh response has arrived.
The response fixture gives session A's refresh token more than three hours of remaining validity.
Logout revokes session A in the fixture.

1. Start a refresh-token request for session A.
2. Hold its response in the test adapter.
3. Sign out of session A.
4. Deliver the held response for session A.
5. Sign in again to create session B.
6. Invoke refresh acquisition 25 seconds before session B's access expiry.
7. Advance the clock to session B's access expiry.
8. Invoke session recovery.
9. Check the refresh token sent and session B's authentication state.

| Observation | Old version | New version |
| --- | --- | --- |
| Session A's refresh token after sign-in | Cleared | Retained |
| Replacement request for session B | Sent | Skipped because the old token appears reusable |
| Refresh token sent for recovery | Session B's token | Session A's revoked token |
| Recovery result | Session B continues | Rejection clears session B |

**Difference:** the new version retains session A's token through fresh sign-in. It then skips the request that replaces that token.
Classification: added failure condition; retain P2.
Evidence: [old execution](evidence/baseline-reassessment-20261021/races/f03-before-baseline/run.json), [new execution](evidence/baseline-reassessment-20261021/races/f03-before-candidate/run.json), and [paired states](evidence/baseline-reassessment-20261021/races/analysis.json).

#### Case F-03B: The old response arrives after the new sign-in

Use the same setup as [Case F-03A](#case-f-03a-the-old-response-arrives-before-the-new-sign-in).
Change only the response delivery order.

1. Start a refresh-token request for session A.
2. Hold its response in the test adapter.
3. Sign out of session A.
4. Sign in again to create session B.
5. Deliver the held response for session A.
6. Invoke refresh acquisition 25 seconds before session B's access expiry.
7. Advance the clock to session B's access expiry.
8. Invoke session recovery.
9. Check the refresh token sent and session B's authentication state.

| Observation | Old version | New version |
| --- | --- | --- |
| Late session A token enters session B's state | Yes | Yes |
| Replacement request before access expiry | Sent; installs session B's token | Skipped; retains session A's token |
| Recovery result | Session B continues | Rejection clears session B |

**Difference:** accepting the late response was already possible. The new reuse rule prevents the replacement that previously repaired the state.
Classification: worsened existing race; retain P2.
Evidence: [old execution](evidence/baseline-reassessment-20261021/races/f03-after-baseline/run.json), [new execution](evidence/baseline-reassessment-20261021/races/f03-after-candidate/run.json), and [paired states](evidence/baseline-reassessment-20261021/races/analysis.json).

#### Case F-03C: Neither version gets the replacement opportunity

Use the same setup as [Case F-03B](#case-f-03b-the-old-response-arrives-after-the-new-sign-in).
Omit only the acquisition call before access expiry.

1. Start a refresh-token request for session A.
2. Hold its response in the test adapter.
3. Sign out of session A.
4. Sign in again to create session B.
5. Deliver the held response for session A.
6. Advance directly to session B's access expiry without invoking refresh acquisition.
7. Invoke session recovery.
8. Check the refresh token sent and session B's authentication state.

| Observation | Old version | New version |
| --- | --- | --- |
| Refresh token sent for recovery | Session A's revoked token | Session A's revoked token |
| Recovery result | Rejection clears session B | Rejection clears session B |

**Difference:** none in this condition. Both versions fail when the late response remains unreplaced.
Classification: unchanged existing failure for this control case.
Evidence: [old execution](evidence/baseline-reassessment-20261021/races/f03-after-no-acquisition-baseline/run.json), [new execution](evidence/baseline-reassessment-20261021/races/f03-after-no-acquisition-candidate/run.json), and [paired states](evidence/baseline-reassessment-20261021/races/analysis.json).

#### F-03 consequence, cause, and limits

Consequence: a fresh sign-in can later end because recovery sends an ended session's credential.

Owner: unknown application owner.
Next action: separate fresh sign-in from access rotation. Reject refresh responses from ended sessions.
Validation: repeat [Case F-03A](#case-f-03a-the-old-response-arrives-before-the-new-sign-in), [Case F-03B](#case-f-03b-the-old-response-arrives-after-the-new-sign-in), and [Case F-03C](#case-f-03c-neither-version-gets-the-replacement-opportunity).

Assertions: [paired race test](evidence/baseline-reassessment-20261021/races/raceComparison.test.tsx#L78-L148).
The changed [token reducer](../../repos/ui/mfe-base/src/hooks/reducer/root0.reducers.ts#L6-L9) retains the old token during fresh sign-in.
The [reuse guard](../../repos/ui/mfe-base/src/hooks/service/index.ts#L38-L52) skips replacement when expiry exceeds three hours.
The unchanged [response handler](../../repos/ui/mfe-base/src/hooks/service/util/succes.response.handler.ts#L39-L40) explains why late installation also occurred before.

Limits: the adapter models logout revocation and recovery rejection. No live identity provider participates.
The test invokes acquisition directly. It does not execute Home timer delivery for these cases.
The omitted call in Case F-03C is a test control. It does not prove browser suspension.

Conclusion: retain P2 for [Case F-03A](#case-f-03a-the-old-response-arrives-before-the-new-sign-in) and [Case F-03B](#case-f-03b-the-old-response-arrives-after-the-new-sign-in).
The unchanged failure in [Case F-03C](#case-f-03c-neither-version-gets-the-replacement-opportunity) narrows that conclusion.

### F-02: [P3] Permit acquisition when its timer runs slightly late

**User case:** the new version misses a refresh replacement opportunity when a timer runs slightly late.

Setup: give each version 15 minutes of valid access and two hours of valid refresh.
Keep the page visible. The test supplies these credentials directly to isolate the timer guard.
The timer targets 25 seconds before access expiry.
Review expectation: replace eligible refresh credentials while access remains valid.
This expectation follows the existing acquisition path. A separate approved timer-tolerance criterion is unavailable.

1. Allow Home to schedule the acquisition callback.
2. Offset the reported clock time by one millisecond.
3. Run the scheduled callback at its target time.
4. Confirm that 24,999 milliseconds of access validity remain.
5. Check the number of replacement requests.
6. Check refresh validity and timeout-prompt state.

| Observation | Old version | New version |
| --- | --- | --- |
| Replacement requests | One | Zero |
| Existing or replacement refresh remains usable | Yes | Yes |
| Timeout prompt opens during this check | No | No |

**Difference:** the new version skips replacement. This test does not show failed user recovery.
Classification: new scheduling defect with limited demonstrated impact; downgrade from P2 to P3.
Consequence: the existing refresh token remains in use. A later recovery failure is unproved.

Owner: unknown application owner.
Next action: permit eligible acquisition after slight timer delay, or retain this as a lower-priority robustness issue.

Evidence: [old execution](evidence/baseline-reassessment-20261021/races/f02-baseline/run.json), [new execution](evidence/baseline-reassessment-20261021/races/f02-candidate/run.json), and [observed states](evidence/baseline-reassessment-20261021/races/analysis.json).
Assertions: [timing test](evidence/baseline-reassessment-20261021/races/raceComparison.v1.test.tsx.snapshot#L42-L76).
Cause: the [remaining-time guard](../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L125-L135) requires at least 25,000 milliseconds when refresh exists.

Limit: this shared initial state is synthetic for the old Home journey. Old access rotation normally clears refresh credentials.
The clock offset models callback lateness. It does not measure real callback delays.

### F-04: Resolved event-fixture type errors

This finding concerns test fixtures. It does not describe a runtime session gap.
The changed [event signature](../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L36-L37) exposed two incomplete test fixtures.
The repaired [test callers](../../repos/ui/mfe-base/src/pages/Home/index.test.tsx#L180-L211) use complete `React.SyntheticEvent` values with real DOM ancestry.
The [final compiler execution](evidence/baseline-reassessment-20261021/test-repairs/run-002/typecheck-run.json) passed with exit code zero.

Owner: Codex for the authorized test-only repair. Next action: none for F-04.
Resolution: fixed in test commit `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85`.

### Inherited delayed-refresh recovery

**User case:** access expires while a refresh response remains in transit.

Setup: start each version with valid access and no refresh token.
Use scheduled acquisition, which both versions support. Do not use the new tab-hide acquisition path for this comparison.

1. Advance the clock to 25 seconds before access expiry.
2. Allow the scheduled refresh request to start.
3. Hold the refresh response in the test adapter.
4. Advance the clock to access expiry.
5. Confirm that the timeout dialog appears.
6. Deliver the held response with a usable refresh token.
7. Attempt to select Extend.
8. Advance the clock by one second.
9. Check the Extend control, recovery requests, and authentication state.

Review expectation: usable late credentials permit manual recovery before logout completes.
This outcome follows the [requested background-recovery scope](change-review.md#request-and-source-facts).
The paired executions characterize its failure. They do not establish that the requirement has been met.

| Observation | Old version | New version |
| --- | --- | --- |
| Usable refresh arrives after access expiry | Yes | Yes |
| Extend control after response delivery | Disabled | Disabled |
| Recovery requests | Zero | Zero |
| Final result | Logout | Logout |

**Difference:** none in this condition. The failure existed before the change.
Classification: unchanged existing failure; reduce its incremental release importance.
Consequence: the user must sign in again despite the late usable refresh response.

Owner: unknown application owner; user for acceptance decisions.
Next action: retain this known limitation when assessing required background recovery. Lower change risk does not waive that requirement.

Evidence: [old execution](evidence/baseline-reassessment-20261021/lifecycle/delayed_recovery-baseline/run.json), [new execution](evidence/baseline-reassessment-20261021/lifecycle/delayed_recovery-candidate/run.json), and [observed states](evidence/baseline-reassessment-20261021/lifecycle/analysis.json).
Assertions: [paired delayed-response test](evidence/baseline-reassessment-20261021/lifecycle/diagnostic.test.tsx.snapshot#L96-L125).
The required [recovery assertion](../../repos/ui/mfe-base/src/pages/Home/common/sessionLifecycle.test.tsx#L370-L379) remains an explicit `it.failing` case.
Its runner pass records the expected failure. It does not verify successful recovery.

Limit: scheduled acquisition establishes downstream parity. It does not compare acquisition when the page becomes hidden.

## Change identity

| Field | Value |
| --- | --- |
| PR locator | null; no remote or PR is configured. |
| Repository ID | `mfe-base`; `repos/ui/mfe-base`. |
| Review mode | Branch comparison from target merge base to selected head; fresh isolated validation. |
| Requested base and merge base | `main`; `f025513f696476a9cc8162681410cbd21e029bcb`. |
| Runtime candidate | `6d4c37c839b99d14ea41fd936da1a36cda526b17`. |
| Test-only repair commit | `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85`. |
| Branch | `feature/session-refresh-minor`. |
| Change state | Implemented locally; deployment and merge states unknown. |
| Final change fingerprint | `76353634492637ab99a16365a6ff6fc12cbef0482b06035c27b79902c24873b5`. [Current context](evidence/code-review-refresh-20261021/context-final.json). |
| Requirements | [Active renewal](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria), version 4; publication review pending. |
| Frozen intake | [Intake](intake.md); Git `cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c`; SHA-256 `1650a20f8a2aba2105b30b8abc4bd2a881f58ee335925a3daa9f6a6c0d0e0948`. |
| Current stage | [Fresh branch review](change-review.md#fresh-branch-review-21-october-2026); `READY`, complete. |
| Unrelated local change | `tsconfig.tsbuildinfo`; original hash preserved in [commit binding](evidence/baseline-reassessment-20261021/commit-binding.json). |

MFE runtime links bind revision `6d4c37c839b99d14ea41fd936da1a36cda526b17`.
Repaired test links bind revision `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85`.
BFF source links bind revision `85d7cc03eb12710d6facf581987fd4ae24fc9844`.
Version 1 remains in Workbench Git `b4f2e22`, with its hash in [stage inputs](evidence/baseline-reassessment-20261021/stage-inputs.json).
Version 2 remains in Workbench Git `6804507458dab19f50cded43da8af4b3b91560e9`.
Version 3 adds these case steps. It changes no finding priority or observed result.
Version 4 confirms the findings through fresh source inspection and isolated executions at the current head.
Version 1’s four-open-findings conclusion is superseded by this reassessment. Previous failed executions remain evidence.

## Problem and behavior

Before: refresh acquisition depended on one browser timer. Access rotation discarded refresh credentials.
After: hiding starts acquisition, overlapping requests share transport, and access rotation retains refresh credentials.
Purpose: improve background recovery with reduced application changes.
The earlier [user request](evidence/baseline-reassessment-20261021/user-request.txt) authorizes test repairs and comparison with previous behavior.
The earlier [request](evidence/gap-case-steps-20261021/user-request.txt) required clear case steps and a reusable comparison rule.
The current [request](evidence/code-review-refresh-20261021/inputs.json) authorizes review and local validation, without application changes.
The test repair changes validation fixtures and known-defect classification. Application runtime remains unchanged.

## Change scope and risks

| Boundary | Inspected change and consumers | Qualitative risk |
| --- | --- | --- |
| Home lifecycle | Acquisition, visibility reconciliation, refresh expiry, Timeout mounting, and activity extension. | High: valid active access can reach forced logout. |
| Refresh service and reducer | Reuse, shared requests, aborts, interceptors, normal sign-in, logout, and relogin. | Medium: changed persistence worsens an existing response race. |
| Acquisition timer | One-millisecond late callback with eligible retained refresh. | Low demonstrated impact; replacement skipped, recovery consequence unproved. |
| Event and test interface | UI event bindings, complete synthetic fixture, Jest expected-failure typing, and setup assertions. | Compiler issue resolved; inherited runtime recovery remains visible. |
| Configuration | Four environment files, lint, formatting, ignore rules, and build consumers. | No additional actionable defect established. |

HTTP paths and header names remain unchanged. Authentication state lifetime changes between baseline and runtime candidate.
The repair commit changes only two test files. All 283 recorded runtime and configuration hashes remain unchanged.

## Validation evidence

The [fresh review](#fresh-branch-review-21-october-2026) records the current executions at `6e34da3`.
The following executions remain historical evidence with their original source identities.

### Earlier executions

| Check | Actual result | Retained evidence and limits |
| --- | --- | --- |
| Full Jest retry | 116 suites; 413 runner passes; 412 ordinary checks plus one expected failure. Zero pending checks. | [Run](evidence/baseline-reassessment-20261021/full-unit-run-002/run.json), [assertions](evidence/baseline-reassessment-20261021/full-unit-run-002/result.json). Isolated workers; forced exit does not establish open-handle freedom. |
| Initial full Jest attempt | Runner ended with signal 11; aggregate outcome unavailable. | [Error record](evidence/baseline-reassessment-20261021/full-unit/run.json). Cause unconfirmed; no business assertion outcome inferred. |
| Focused final Jest | 45 runner passes across two suites, including one expected failure. | [Run](evidence/baseline-reassessment-20261021/test-repairs/run-002/jest-run.json). [Repair details](evidence/baseline-reassessment-20261021/test-repairs/repair-summary.json) preserve initial failures. |
| TypeScript | Exit code zero using installed TypeScript 4.9.5. | [Run](evidence/baseline-reassessment-20261021/test-repairs/run-002/typecheck-run.json). No cache or declaration writes. |
| Lifecycle comparison | Four executions passed their characterization predicates across two paired cases. | [Analysis](evidence/baseline-reassessment-20261021/lifecycle/analysis.json). The other selected-out diagnostic does not count as unexecuted overall. |
| Timer and race comparison | Eight executions passed their characterization predicates across four paired conditions. | [Analysis](evidence/baseline-reassessment-20261021/races/analysis.json). Passing characterization can demonstrate adverse candidate behavior. |
| Identity preservation | Runtime hashes, committed test bytes, frozen intake, and pre-existing cache match recorded inputs. | [Commit binding](evidence/baseline-reassessment-20261021/commit-binding.json). |
| Browser, production build, and provider | No fresh execution during this reassessment. | [Historical browser report](test-execution-report.md). Earlier observations retain their original revisions and limits. |

Controlled checks use JSDOM, fake clocks, synthetic JWTs, and Axios adapters.
Historical dependency installations were not recreated. No production failure probability is established.
The [earlier execution report](test-execution-report.md#case-mapping) retains all seven criterion mappings and historical browser outcomes.
These test repairs do not convert failed business outcomes into verified behavior.

[Earlier document validation](evidence/gap-case-steps-20261021/validation.json) passed with eight warnings.
Warnings retain unknown owners, pending business review, unresolved decisions, and pending ASD review.
Document validation and ASD writing review remain separate. ASD review is pending.

## Review coverage and suggestions

The prior [inspection inventory](evidence/code-review-20261021/inspection.json) covers all fourteen original branch paths and affected consumers.
The [final context](evidence/baseline-reassessment-20261021/final-context.json) adds the repaired existing Home test path.
Both authorized test diffs were reviewed after repair. Hash checks bind their executed and committed bytes.
The generated build cache remains excluded and preserved.
Runtime suggestions for [F-01](#f-01-p2-preserve-active-access-across-the-refresh-deadline), [F-03](#f-03-p2-stop-stale-credential-persistence-and-reuse), and [F-02](#f-02-p3-permit-acquisition-when-its-timer-runs-slightly-late) remain unapplied.

## Review disposition

Reviewer: null. Decision: pending. Review date: null. Merge or publication authority: null.

Local test repair and comparative review are complete.
Two P2 regressions remain; one scheduling concern is P3. F-04 is resolved.
Delayed recovery has lower incremental release importance because the compared baseline also fails.
This does not waive required background behavior or establish production readiness.
Unrestricted production rollout is not recommended while the two demonstrated P2 regressions remain open.

## Evidence and uncertainty

| Source ID | Locator | Exact identity | Authority and limits |
| --- | --- | --- | --- |
| SRC-session-branch-refresh-20261021 | [Inputs](evidence/code-review-refresh-20261021/inputs.json), [summary](evidence/code-review-refresh-20261021/summary.json), and [integrity](evidence/code-review-refresh-20261021/integrity.json). | Base and head above; current fingerprints, export hashes, and execution hashes retained. | Fresh local review; controlled checks; no application changes or deployment verification. |
| SRC-session-baseline-reassessment-20261021 | [Stage inputs](evidence/baseline-reassessment-20261021/stage-inputs.json), [progress](evidence/baseline-reassessment-20261021/progress.json), and [binding](evidence/baseline-reassessment-20261021/commit-binding.json). | Full base, runtime, and test commits above; per-file SHA-256 values retained. | Authorized local tests and source-bound comparison; application owner unknown. |
| SRC-mfe-code-review-20261021 | [Original inputs](evidence/code-review-20261021/inputs.json) and [inspection](evidence/code-review-20261021/inspection.json). | Original branch fingerprint and revisions retained. | Historical initial findings; current classifications supersede them. |
| SRC-session-review-intent-v4 | [Candidate requirement](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria). | Version 4; SHA-256 `828d62209f11dd9bb9dee893ddc80e7e5d4dc6abd3c58170e902dab61bc587aa`. | Recorded user intent; publication review pending. |

Facts: baseline and candidate differ on active cutoff and stale-credential replacement under the controlled conditions.
Facts: delayed recovery fails both; timer replacement differs without demonstrated recovery failure; test-only type repairs pass.
Unknowns: deployed lifetimes, real browser timing frequency, provider behavior, ownership, and criterion-specific acceptance decisions.
The [current stage](change-review.md#unknowns-and-blockers) retains those decisions.
No new business clarification or knowledge publication occurred.

## Findings and actions

The unknown application owner must address the two P2 regressions and validate their paired failure conditions.
The scheduling issue can receive lower release priority. The inherited delayed-recovery limitation remains explicit.
Codex completed the authorized test repairs and retained the comparative evidence.
Runtime correction, deployment, acceptance waivers, and knowledge publication were outside this request.
