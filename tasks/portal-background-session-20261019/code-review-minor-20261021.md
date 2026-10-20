---
artifact_kind: pull-request-review
id: REVIEW-session-minor-20261021
version: 1
status: draft
owner: unknown
source_refs:
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
> **Four regressions require correction before acceptance.**
> Action: correct the [review findings](#review-findings), then repeat their focused checks.
> Consequence: active sessions can end, recovery can fail, and the declared type build fails.
> Owner: unknown application owner. Evidence: [current executions](evidence/code-review-20261021/jest-run.json) and [compiler errors](evidence/code-review-20261021/typecheck.log).
> Timer lateness and session crossing are source-backed inferences. Their specific interleavings were not executed.

## Review findings

### F-01: [P2] Preserve active access across the refresh deadline

Evidence: [new expiry condition](../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L117-L123) and [new refresh timer](../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L171-L173).
Trigger: acquire refresh credentials by hiding, then extend access successfully before each access deadline.
Each extension postpones refresh acquisition. The changed reducer retains the original refresh credential.
The refresh timer opens Timeout even while access remains valid.
The [Timeout controller](../../repos/ui/mfe-base/src/components/Timeout/common/useController.ts#L25-L52) then starts logout because refresh credentials have expired.
Baseline `f025513` had no refresh deadline that forced this active-session logout.
The [new lifecycle assertion](../../repos/ui/mfe-base/src/pages/Home/common/sessionLifecycle.test.tsx#L529-L558) explicitly expects logout after 23 successful extensions.
That assertion passed in the [current execution](evidence/code-review-20261021/jest-result.json).
It contradicts [AC-4](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L158-L162), requirement version 4.
Owner: unknown application owner.
Next action: replace refresh credentials while access remains usable. Avoid logout solely from the original refresh deadline.
Validation: extend access across the initial refresh deadline. Assert zero forced sign-ins under [AC-4](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L158-L162).
Limit: the passing assertion demonstrates controlled logout. It does not establish deployed token lifetimes.
Resolution: open; suggestion unapplied.

### F-02: [P2] Permit acquisition when its timer runs slightly late

Evidence: [new remaining-time guard](../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L125-L135) and [acquisition deadline](../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L138-L146).
Trigger: a visible idle session retains readable refresh credentials with at most three hours remaining.
The service [permits replacement](../../repos/ui/mfe-base/src/hooks/service/index.ts#L38-L52) in that window.
The timer targets exactly 25,000 milliseconds before access expiry.
A callback one millisecond late has 24,999 milliseconds remaining. The new guard rejects acquisition.
No retry is scheduled. Baseline invoked acquisition when the timer ran.
The old credential therefore remains, reducing recovery time and allowing its earlier expiry to end the session.
Owner: unknown application owner.
Next action: separate acquisition timing from eligibility. Permit replacement while access remains valid.
Validation: deliver the callback with 24,999 milliseconds remaining and an eligible existing refresh credential. Assert one acquisition.
Limit: source arithmetic establishes this failure condition. The current fake-timer assertions do not execute that late delivery.
Resolution: open; suggestion unapplied.

### F-03: [P2] Clear previous-session refresh credentials on fresh sign-in

Evidence: [changed token reducer](../../repos/ui/mfe-base/src/hooks/reducer/root0.reducers.ts#L6-L9); base `f025513` cleared refresh state at line 8.
Trigger: refresh acquisition completes after logout clears state, but before another normal sign-in completes in the same page.
The [response handler](../../repos/ui/mfe-base/src/hooks/service/util/succes.response.handler.ts#L39-L40) installs the old refresh credential.
The [normal sign-in path](../../repos/ui/mfe-base/src/pages/Login/common/useController.ts#L58-L62) does not require page navigation.
Fresh sign-in now preserves that credential through `SET_TOKEN`.
The [reuse guard](../../repos/ui/mfe-base/src/hooks/service/index.ts#L38-L52) can suppress replacement while more than three hours remain.
Subsequent [relogin](../../repos/ui/mfe-base/src/hooks/service/util/success.request.handler.ts#L18-L19) sends the previous session's refresh credential.
The BFF [logout path](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L365-L373) revokes that session.
Its [session check](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v1/implementation/SessionServiceImplementation.java#L28-L33) rejects recovery.
The [error handler](../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L29-L32) then clears the new authentication state.
Baseline also allowed late response delivery, but fresh sign-in cleared its stale refresh state.
Owner: unknown application owner.
Next action: preserve refresh credentials only within the same session. Reject responses from ended sessions.
Validation: delay acquisition, logout, deliver the response, sign in normally, then exercise idle recovery.
Limit: this interleaving was not executed. The supported normal sign-in path makes it reachable without a reload.
The inspected BFF rejects revoked credentials. This review establishes no cross-user authentication.
Resolution: open; suggestion unapplied.

### F-04: [P2] Update callers for the stricter event parameter

Evidence: [changed event signature](../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L36-L37).
Trigger: run the configured TypeScript check, which includes tests through [tsconfig](../../repos/ui/mfe-base/tsconfig.json#L25-L28).
Existing [test callers](../../repos/ui/mfe-base/src/pages/Home/index.test.tsx#L183-L184) pass fabricated targets that cannot satisfy `React.SyntheticEvent`.
The [current compiler output](evidence/code-review-20261021/typecheck.log) reports two `TS2322` errors. The declared type build cannot pass.
The [retained baseline check](evidence/minor-branch-rerun-20261020/unit/initial-baseline-typecheck-run.json) passed using TypeScript 4.9.5.
Owner: unknown application owner.
Next action: update the callers or provide a compatible event contract.
Validation: rerun the [current compiler command](evidence/code-review-20261021/typecheck-run.json). Require exit code zero.
Limit: historical dependency installation was not recreated. The baseline used the current installed compiler.
Resolution: open; suggestion unapplied.

## Change identity

| Field | Value |
| --- | --- |
| PR locator | null; no remote or PR is configured. |
| Repository ID | `mfe-base`; `repos/ui/mfe-base`. |
| Review mode | Branch comparison; suggestions only. |
| Requested base and merge base | `main`; `f025513f696476a9cc8162681410cbd21e029bcb`. |
| Head commit | `6d4c37c839b99d14ea41fd936da1a36cda526b17`. |
| Branch | `feature/session-refresh-minor`. |
| Change state | Implemented locally; deployment and merge states unknown. |
| Change fingerprint | `9c8cf98eec6e826241e09087395aebdd56f4a597aa81e2e49bfda064369488df`. |
| Requirements | [Active renewal](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria), version 4; publication review pending. |
| Frozen intake | [Intake](intake.md); Git `cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c`; SHA-256 `1650a20f8a2aba2105b30b8abc4bd2a881f58ee335925a3daa9f6a6c0d0e0948`. |
| Current stage | [Read-only assessment readiness](change-review.md#stage-boundary-and-readiness); `READY` for evidence collection. |
| Unrelated local change | `tsconfig.tsbuildinfo`; original hash retained in [inputs](evidence/code-review-20261021/inputs.json). |

All MFE source links identify head `6d4c37c839b99d14ea41fd936da1a36cda526b17`.
All BFF source links identify `85d7cc03eb12710d6facf581987fd4ae24fc9844`.
The [inspection inventory](evidence/code-review-20261021/inspection.json) binds unchanged consumers, requirement bytes, and baseline distinctions.

## Problem and behavior

Trigger: users hide the portal or approach access expiry.
Before: refresh acquisition depended on one browser timer. Access rotation discarded refresh credentials.
After: hiding starts acquisition, overlapping requests share transport, and access rotation retains refresh credentials.
Reason: improve background recovery with reduced application changes.
The [stage record](change-review.md#request-and-source-facts) records that purpose and the remaining acceptance decisions.

## Change scope and risks

| Boundary | Change and inspected consumers | Qualitative risk |
| --- | --- | --- |
| Home lifecycle | Acquisition, visibility reconciliation, refresh expiry, Timeout mounting, and workspace selection. | High: valid access can reach forced logout. |
| Refresh service | Credential reuse, request sharing, abort replacement, interceptors, and public exports. | Medium: credentials cross asynchronous session boundaries. |
| Reducer | Preserve refresh during access rotation; inspect login, logout, and relogin. | Medium: fresh sign-in also preserves stale refresh. |
| Event interface | Explicit event type; inspect UI bindings and existing test callers. | Medium: configured compiler fails. |
| Configuration | Four environment files, ESLint, Prettier, ignore rules, and build consumers. | No additional actionable defect established. |

Compatibility and data impact: HTTP paths and header names remain unchanged. Authentication state lifetime changes.
Recovery: revert through the owning repository after separate authorization. This review changes no application source.

## Validation evidence

| Check | Inputs and assertions | Actual result | Retained evidence and limit |
| --- | --- | --- | --- |
| Focused Jest | Six suites; refresh service, reducer, Home, and lifecycle assertions. | `FAILED`: 113 passed; one failed; 114 total. | [Run](evidence/code-review-20261021/jest-run.json), [assertions](evidence/code-review-20261021/jest-result.json), [log](evidence/code-review-20261021/jest.log). JSDOM and controlled transport. |
| Active cutoff | [Lifecycle assertion](../../repos/ui/mfe-base/src/pages/Home/common/sessionLifecycle.test.tsx#L529-L558). | Passed its logout expectation. This supports [F-01](#f-01-p2-preserve-active-access-across-the-refresh-deadline). | [Result](evidence/code-review-20261021/jest-result.json); the expectation conflicts with candidate intent. |
| TypeScript | `node node_modules/typescript/bin/tsc --noEmit --emitDeclarationOnly false --incremental false`. | `FAILED`: exit 2; two `TS2322` errors. | [Run](evidence/code-review-20261021/typecheck-run.json), [log](evidence/code-review-20261021/typecheck.log). No cache or declaration writes. |
| Baseline compiler | Retained initial-baseline execution, TypeScript 4.9.5. | `PASSED`: historical exit 0. | [Run](evidence/minor-branch-rerun-20261020/unit/initial-baseline-typecheck-run.json). Shared installed dependencies; no fresh baseline run. |
| Changed-content scan | Fourteen files; 1,707 added lines. | Eight credential candidates; all are synthetic test values. | [Scan](evidence/code-review-20261021/scan.json). Pattern matching cannot establish complete credential absence. |
| Browser and production build | Existing stage results remain separate. | `NOT_RUN` during this review. | [Existing browser report](test-execution-report.md). No fresh browser, production, or dependency advisory claim. |

Document lint passed with eight warnings across this review and the stage record.
The warnings concern unknown owners, pending business review, unresolved decisions, and pending ASD review.
These warnings remain explicit because the review supplies no missing ownership or approval.

The failed Jest case concerns delayed refresh delivery and the unchanged Timeout controller.
It remains a known acceptance gap. This review does not classify it as a new baseline regression.
The [earlier execution report](test-execution-report.md#case-mapping) retains individual mappings for all seven candidate criteria.
This review uses [AC-4](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L158-L162) to assess the introduced active-session cutoff.

## Review coverage and suggestions

All fourteen changed paths were inspected. The [context inventory](evidence/code-review-20261021/context.json) lists each path and hash.
All changed production files and their enclosing implementations were read at both endpoints.
The three new test files and the reducer assertion were inspected for observable outcomes and mocks.
Configuration review covered webpack, package scripts, pipeline, Docker, and static server consumers.
No binary or generated changed file belongs to this branch comparison.
The local generated build-cache modification remains excluded.
All four suggestions remain unapplied.

## Review disposition

Reviewer: null. Decision: pending. Review date: null.
Assessment: four actionable findings; local review complete.
Reviewed commits: `f025513f696476a9cc8162681410cbd21e029bcb` to `6d4c37c839b99d14ea41fd936da1a36cda526b17`.
Review scope limits: timer lateness and session crossing rely on source inspection. Neither interleaving received a new execution.
Merge or publication authority: null.
The [final identity check](evidence/code-review-20261021/integrity.json) records source, fingerprint, intake, and cache preservation.

## Evidence and uncertainty

| Source ID | Locator | Exact identity | Authority and limits |
| --- | --- | --- | --- |
| SRC-mfe-code-review-20261021 | [Inputs](evidence/code-review-20261021/inputs.json), [context](evidence/code-review-20261021/context.json), and [inspection](evidence/code-review-20261021/inspection.json). | Full commits above; individual SHA-256 values retained. | Direct source inspection and local execution; owner unknown. |
| SRC-session-review-intent-v4 | [Candidate requirement](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria). | Version 4; SHA-256 `828d62209f11dd9bb9dee893ddc80e7e5d4dc6abd3c58170e902dab61bc587aa`. | Recorded user intent; publication review pending. |

Facts: the active-cutoff assertion passes, the delayed-refresh assertion fails, and the compiler reports two errors.
Inferences: timer lateness skips replacement. A late old-session response can survive normal sign-in.
Unresolved questions: application ownership and acceptance waivers remain unknown. The [current stage](change-review.md#unknowns-and-blockers) retains those decisions.
No new business clarification or knowledge publication occurred.

## Findings and actions

All findings remain open. The unknown application owner must correct and validate their linked failure conditions.
The user requested code review. Implementation, new test authoring, release approval, and publication remain separate actions.
