---
artifact_kind: pull-request-review
id: REVIEW-session-minor-20261021
version: 2
status: draft
owner: unknown
source_refs:
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

## Review findings

### F-01: [P2] Preserve active access across the refresh deadline

Trigger: refresh credentials exist, and accepted activity extends access before each access deadline.
The [new expiry condition](../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L117-L123) opens Timeout at the original refresh deadline.
The [refresh timer](../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L171-L173) applies that condition while access remains valid.
The [Timeout controller](../../repos/ui/mfe-base/src/components/Timeout/common/useController.ts#L25-L52) then starts logout.

The same diagnostic seeds equal credentials and performs 23 successful extensions on both revisions.
[Baseline execution](evidence/baseline-reassessment-20261021/lifecycle/active_cutoff-baseline/run.json) remains authenticated and sends zero logout requests.
[Candidate execution](evidence/baseline-reassessment-20261021/lifecycle/active_cutoff-candidate/run.json) sends one logout request and clears authentication.
Their [observed states](evidence/baseline-reassessment-20261021/lifecycle/analysis.json) confirm an introduced active-session cutoff.
The existing [characterization assertion](../../repos/ui/mfe-base/src/pages/Home/common/sessionLifecycle.test.tsx#L542-L571) expects this adverse logout.
That expectation conflicts with [AC-4](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L158-L162), requirement version 4.

Owner: unknown application owner.
Next action: replace refresh credentials while access remains usable. Avoid forced logout solely from the original refresh deadline.
Validation: repeat the [paired diagnostic](evidence/baseline-reassessment-20261021/lifecycle/diagnostic.test.tsx.snapshot) and require zero forced sign-ins.
Limits: equal seeded credentials isolate the cutoff. The controlled four-hour refresh lifetime is not a deployed setting.
Resolution: open; retain P2.

### F-03: [P2] Stop stale-credential persistence and reuse

Trigger: an old refresh request completes after logout, around a fresh normal sign-in in the same page.
The [response handler](../../repos/ui/mfe-base/src/hooks/service/util/succes.response.handler.ts#L39-L40) can install the old credential in both revisions.
This response-installation race already existed.

The changed [token reducer](../../repos/ui/mfe-base/src/hooks/reducer/root0.reducers.ts#L6-L9) also preserves it when delivery precedes fresh sign-in.
The [reuse guard](../../repos/ui/mfe-base/src/hooks/service/index.ts#L38-L52) can suppress replacement when its remaining lifetime exceeds three hours.
[Relogin](../../repos/ui/mfe-base/src/hooks/service/util/success.request.handler.ts#L18-L19) then sends the ended session's credential.
A rejected response [clears authentication](../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L29-L32) for the new session.

| Paired condition | Baseline behavior | Candidate behavior | Interpretation |
| --- | --- | --- | --- |
| Old response before fresh sign-in; next acquisition occurs. | Sign-in clears stale refresh; replacement supports recovery. | Sign-in retains stale refresh; reuse skips replacement; recovery clears the new session. | Added failure window. [Before-sign-in pair](evidence/baseline-reassessment-20261021/races/analysis.json). |
| Old response after fresh sign-in; next acquisition occurs. | Replacement repairs stale state; recovery succeeds. | Reuse skips repair; recovery clears the new session. | Existing race worsens. [After-sign-in pair](evidence/baseline-reassessment-20261021/races/analysis.json). |
| Old response after fresh sign-in; next acquisition is omitted. | Stale credential causes recovery failure. | Same recovery failure. | Inherited race confirmed. [Control pair](evidence/baseline-reassessment-20261021/races/analysis.json). |

Owner: unknown application owner.
Next action: distinguish fresh sign-in from same-session rotation. Reject responses associated with ended sessions.
Validation: repeat all six [race executions](evidence/baseline-reassessment-20261021/races/analysis.json) with both response orderings and the omitted-acquisition control.
Limits: the adapter models revocation. Actual reducers, interceptors, and service functions execute; no live identity provider participates.
The next acquisition is invoked directly at its deadline. These cases isolate reuse, rather than execute Home scheduling.
The BFF [logout implementation](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L365-L373) supports the revocation model.
Its [session check](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v1/implementation/SessionServiceImplementation.java#L28-L33) rejects revoked sessions.
No cross-user authentication or production occurrence rate is established.
Resolution: open; retain P2 for the worsened persistence and reuse behavior.

### F-02: [P3] Permit acquisition when its timer runs slightly late

Trigger: readable refresh credentials remain eligible for replacement, and the acquisition callback runs one millisecond late.
The [remaining-time guard](../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L125-L135) rejects replacement with 24,999 milliseconds remaining.
The [timer](../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L138-L146) targets 25,000 milliseconds before access expiry.

The [baseline execution](evidence/baseline-reassessment-20261021/races/f02-baseline/run.json) sends one replacement request.
The [candidate execution](evidence/baseline-reassessment-20261021/races/f02-candidate/run.json) sends zero replacement requests.
Both retain usable refresh credentials. Neither opens the timeout prompt in this check.
The prior review's claim of resulting recovery failure was too broad. No user recovery regression was demonstrated.

Owner: unknown application owner.
Next action: permit eligible replacement while access remains valid, or retain this as a lower-priority robustness issue.
Validation: repeat the [timing diagnostic](evidence/baseline-reassessment-20261021/races/raceComparison.v1.test.tsx.snapshot) at 24,999 milliseconds remaining.
Limits: the equal retained-refresh initial state is synthetic for baseline's usual Home journey.
Baseline lacks early hide acquisition and clears refresh state during access rotation.
Resolution: downgrade from P2 to P3; no demonstrated user failure delta.

### F-04: Resolved event-fixture type errors

The changed [event signature](../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L36-L37) exposed two incomplete test fixtures.
The repaired [test callers](../../repos/ui/mfe-base/src/pages/Home/index.test.tsx#L180-L211) use complete `React.SyntheticEvent` values with real DOM ancestry.
No runtime signature, compiler configuration, dependency, cast, or diagnostic suppression changed.
The [final compiler execution](evidence/baseline-reassessment-20261021/test-repairs/run-002/typecheck-run.json) passed with exit code zero.
Owner: Codex for this authorized test-only repair.
Next action: none for F-04; retain the passing check and committed input hashes.
Resolution: fixed in test commit `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85`.

### Inherited delayed-refresh recovery

Trigger: scheduled refresh acquisition starts before access expiry, but its response arrives after expiry.
The [same diagnostic](evidence/baseline-reassessment-20261021/lifecycle/diagnostic.test.tsx.snapshot) uses the shared scheduled-acquisition boundary on both revisions.
Both [baseline](evidence/baseline-reassessment-20261021/lifecycle/delayed_recovery-baseline/run.json) and [candidate](evidence/baseline-reassessment-20261021/lifecycle/delayed_recovery-candidate/run.json) install late refresh credentials.
Both disable Extend, send zero relogin requests, and subsequently logout.
This downstream recovery failure is pre-existing and unchanged in the tested condition.

Owner: unknown application owner; user for acceptance decisions.
Next action: reduce its incremental release importance. Retain the limitation against the required background-recovery outcome.
The test repair adds an ordinary [logout characterization](../../repos/ui/mfe-base/src/pages/Home/common/sessionLifecycle.test.tsx#L365-L368).
The desired [recovery assertions](../../repos/ui/mfe-base/src/pages/Home/common/sessionLifecycle.test.tsx#L370-L379) remain in an explicit `it.failing` case.
Setup assertions execute outside expected-failure inversion. An unexpected recovery success makes that known-defect test fail.
Limits: baseline does not implement the candidate-only hide acquisition. The shared scheduled boundary establishes downstream parity.
Resolution: downgrade as inherited change risk; runtime recovery remains unfixed. No behavior criterion was waived.

## Change identity

| Field | Value |
| --- | --- |
| PR locator | null; no remote or PR is configured. |
| Repository ID | `mfe-base`; `repos/ui/mfe-base`. |
| Review mode | Exact branch endpoints; followed by authorized test-only repairs and paired diagnostics. |
| Requested base and merge base | `main`; `f025513f696476a9cc8162681410cbd21e029bcb`. |
| Runtime candidate | `6d4c37c839b99d14ea41fd936da1a36cda526b17`. |
| Test-only repair commit | `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85`. |
| Branch | `feature/session-refresh-minor`. |
| Change state | Implemented locally; deployment and merge states unknown. |
| Final change fingerprint | `f75227799aec00144fb3ea7524957cde2921290eaf154baacbfd2f1208e42688`. [Final context](evidence/baseline-reassessment-20261021/final-context.json). |
| Requirements | [Active renewal](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria), version 4; publication review pending. |
| Frozen intake | [Intake](intake.md); Git `cfcc2be4bfe81a0cb9d0eb1ab5592f00fe74b13c`; SHA-256 `1650a20f8a2aba2105b30b8abc4bd2a881f58ee335925a3daa9f6a6c0d0e0948`. |
| Current stage | [Test-only repair and reassessment](change-review.md#test-repair-and-baseline-reassessment-21-october-2026); `READY`, complete. |
| Unrelated local change | `tsconfig.tsbuildinfo`; original hash preserved in [commit binding](evidence/baseline-reassessment-20261021/commit-binding.json). |

MFE runtime links bind revision `6d4c37c839b99d14ea41fd936da1a36cda526b17`.
Repaired test links bind revision `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85`.
BFF source links bind revision `85d7cc03eb12710d6facf581987fd4ae24fc9844`.
Version 1 remains in Workbench Git `b4f2e22`, with its hash in [stage inputs](evidence/baseline-reassessment-20261021/stage-inputs.json).
Its four-open-findings conclusion is superseded by this reassessment. Previous failed executions remain evidence.

## Problem and behavior

Before: refresh acquisition depended on one browser timer. Access rotation discarded refresh credentials.
After: hiding starts acquisition, overlapping requests share transport, and access rotation retains refresh credentials.
Purpose: improve background recovery with reduced application changes.
The latest [user request](evidence/baseline-reassessment-20261021/user-request.txt) authorizes test repairs and comparison with previous behavior.
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

[Document validation](evidence/baseline-reassessment-20261021/final-validation.json) passed with eight warnings.
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
