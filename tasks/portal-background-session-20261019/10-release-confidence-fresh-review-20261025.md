---
artifact_kind: release-readiness
id: ASSESS-session-refresh-fresh-review-20261025
version: 1
status: draft
owner: unknown
source_refs:
  - SRC-session-active-cutoff-fix-request-20261024
  - SRC-session-release-source-20261022
  - SRC-session-release-coverage-20261022
  - SRC-session-fresh-code-review-20261025
related_ids:
  - ASSESS-session-refresh-active-cutoff-20261025
  - DEFECT-portal-background-session-20261019
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

# MFE Base fresh release confidence

> **Release status: `NO_GO`; evidence confidence score: `100/100` (`HIGH`); `can_go: false`.**
> Do not promote candidate `ae8213f2963047e7c126d01f4003cee1236abc25` to PROD.
> Required action: fix `FRESH-CR-01`, then rerun the delayed-session, natural-recovery, delayed-refresh, and stale-session cases.
> Consequence: a late refresh response can replace a new session's credential and clear the new session.
> Owner: unknown application owner; unknown release owner for artifact evidence.
> Evidence: [fresh review](evidence/code-review-refresh-20261025/review.json), [fresh race execution](evidence/code-review-fresh-20261025/race-f03-after/run.json), and [natural recovery result](evidence/active-cutoff-fix-20261024/browser/cutoff-natural-20261025T004053/artifacts/result.json).

> **This is a fresh review of the exact candidate range. Previous review conclusions were not reused.**
> Human deployment authorization, a waiver, and a production exception are not recorded.

## Release scope

| Identity | Evidence and limit |
| --- | --- |
| Release candidate | `mfe-base`, branch `feature/session-refresh-minor`, candidate `ae8213f2963047e7c126d01f4003cee1236abc25`. |
| Comparison | Base `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85`; exact range review fingerprint `c45cc6ef54834da6e88e65650a79ec6e2813afbb592ec9c229b47f025363a462`. [Review context](evidence/code-review-refresh-20261025/context.json). |
| Changed paths | `useController.ts`, `sessionRefresh.test.tsx`, and `sessionLifecycle.test.tsx`. Added lines scanned: 84. [Scan](evidence/code-review-refresh-20261025/scan.json). |
| Local worktree | `tsconfig.tsbuildinfo` is modified and excluded as a pre-existing generated cache. |
| Intended environment | PROD. No served module identity, artifact digest, deployment receipt, or target configuration is bound. |
| Excluded scope | No application fix, deployment, push, or external publication occurred during this review. |

## Readiness conditions

| Condition | Required evidence | Actual evidence | State | Owner | Next action |
| --- | --- | --- | --- | --- | --- |
| Fresh code review has no material failure | Exact candidate range, changed-path inspection, race assertions, and review result | [FRESH-CR-01](evidence/code-review-refresh-20261025/review.json) at `useController.ts:131`; current candidate race records Session A after Session B login | FAILED | unknown application owner | Bind refresh responses to the initiating session and rerun both delivery orders. |
| Active session renewal meets the requirement | Current requirement mappings and passing assertions for active cutoff, natural return, delayed delivery, and stale-session isolation | E2E-06 passes; E2E-07 fails; delayed and stale-session cases remain failed | FAILED | unknown application owner | Correct the failed behavior and rerun canonical cases. |
| Unit and integration checks match the candidate | Candidate source revision, focused assertions, full suite, and clean runner completion | 3 focused suites and 95 tests pass; full Jest reports 116 suites and 413 tests pass, with open-handle shutdown warning | LIMITED | unknown application owner | Add the missing race assertion and remove the open-handle condition. |
| Browser system behavior is verified | Candidate-bound browser runs with required assertions | [E2E-07](evidence/active-cutoff-fix-20261024/browser/cutoff-natural-20261025T004053/artifacts/result.json) fails; E2E-06 passes | FAILED | unknown application owner | Keep the timeout control visible during renewal and rerun E2E-07. |
| Artifact and target identity are bound | Immutable build, artifact digest, served bytes, target, and effective configuration | No build ID, digest, served bytes, or target receipt | UNKNOWN | unknown release owner | Bind build provenance and deployed configuration. |
| Recovery and operation are ready | Rollback, monitoring, stop triggers, and operator ownership | No retained rollback or operating evidence | UNKNOWN | unknown release owner | Test rollback and record monitoring and response ownership. |

## Execution evidence

```yaml
execution_status: PASSED_WITH_LIMITS
repository_revision: ae8213f2963047e7c126d01f4003cee1236abc25
test_revision: ae8213f2963047e7c126d01f4003cee1236abc25
actual_results:
  focused_jest: "3 suites, 95 tests passed"
  full_jest: "116 suites, 413 tests passed; Jest reported open asynchronous handles after the summary"
  fresh_race: "F03 characterization passed while recording stale Session A delivery, failed Session B recovery, and cleared Session B"
retained_execution_refs:
  - evidence/code-review-fresh-20261025/race-f03-after/run.json
  - evidence/code-review-refresh-20261025/review.json
  - evidence/active-cutoff-fix-20261024/browser/cutoff-cross-20261024T234223/artifacts/result.json
  - evidence/active-cutoff-fix-20261024/browser/cutoff-natural-20261025T004053/artifacts/result.json
acceptance_decision_ref: null
rollback_execution_status: NOT_RUN
rollback_results: null
```

The focused and full Jest passes show test execution. They do not close the confirmed race because no existing assertion covers automatic expiry, logout, new login, and delayed response delivery.

## Business impact

The candidate intends to preserve portal work when the refresh credential expires while access remains valid.
The fresh review found a cross-session credential failure in that same path.
A late response from Session A can overwrite Session B state after the user signs in again.
The next recovery can send a revoked credential and clear Session B.
Users can lose active work and must sign in again. Population, frequency, and financial exposure remain unknown.

| Journey | Current result | Consequence | Required action |
| --- | --- | --- | --- |
| Active work crosses refresh expiry | E2E-06 passes in the local fixture | The tested active path remains available in that fixture. | Confirm the served candidate and production-parity timing. |
| Natural background return | E2E-07 fails after the declared natural wait | The timeout control becomes unavailable while renewal is pending. | Preserve the control and rerun the case. |
| Delayed refresh delivery | The canonical case remains a known failure | A late usable response does not provide the required recovery. | Correct response coordination or record an approved behavior change. |
| Logout and new login during refresh | Fresh F03 records `session-A` refresh state after Session B login and clears Session B | A user can lose the new session after a delayed old response. | Add session ownership or generation checks and rerun both delivery orders. |

No unauthorized data access or credential disclosure was demonstrated.

## System impact

The candidate changes shared Home expiry reconciliation.
The changed line starts a refresh request when access remains usable and the refresh token has expired.
The response path crosses the shared service, Axios success interceptor, refresh-token reducer, logout cleanup, login, and relogin.
The response handler does not receive or compare the initiating access token or session generation.
Logout clears the store, but it does not cancel this refresh request.
The served consumer versions, effective token settings, deployment order, and rollback target remain unknown.

## Risks and exceptions

| Evidence | Consequence | Owner | Next action | Human disposition |
| --- | --- | --- | --- | --- |
| [FRESH-CR-01](evidence/code-review-refresh-20261025/review.json) at `useController.ts:131` | A stale response can clear a fresh session. | unknown application owner | Fix response ownership and add the delayed cross-session test. | null |
| [E2E-07 result](evidence/active-cutoff-fix-20261024/browser/cutoff-natural-20261025T004053/artifacts/result.json) | Natural recovery does not meet the required prompt behavior. | unknown application owner | Preserve prompt visibility through response completion and rerun. | null |
| No immutable artifact or target receipt | Source evidence cannot establish PROD bytes or configuration. | unknown release owner | Bind build, target, configuration, and deployment evidence. | null |
| No rollback or operating record | Recovery readiness is unknown. | unknown release owner | Test rollback and record stop and response ownership. | null |

No exception authority, criterion waiver, or deployment authorization is recorded.

## Confidence score and release status

| Dimension ID | Dimension | Score (0-5) | Status | Critical | Evidence and rationale | Owner | Action to increase confidence | Target score/status | Expected release-status effect | Closure evidence |
| --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| CR-01 | Code review | 5 | FAILED | true | Fresh range review confirms the P1 stale-session race at the new automatic refresh call. | unknown application owner | Bind the response to the initiating session and review the fixed range. | 5 / SUPPORTED | Removes the code-review blocker. | Fresh review with the race assertion passing. |
| CR-02 | Requirement conformance | 5 | FAILED | true | E2E-07, delayed recovery, and stale-session requirements remain unmet. | unknown application owner | Correct the failed behaviors and rerun canonical cases. | 5 / SUPPORTED | Removes material conformance blockers. | Passing E2E-07, delayed, and stale-session results. |
| CR-03 | Business impact | 3 | LIMITED | true | Affected journeys and consequences are known. Population and frequency are unknown. | unknown business owner | Bind affected users, workaround, and acceptance evidence. | 4 / SUPPORTED | Supports a complete impact decision. | Reviewed impact and acceptance record. |
| CR-04 | System impact | 3 | LIMITED | true | Changed lifecycle and shared authentication paths are inspected. Served composition and effective settings are unknown. | unknown release owner | Bind consumer versions, served source, and effective settings. | 4 / SUPPORTED | Removes target uncertainty. | Deployment composition and configuration receipt. |
| CR-05 | Unit and integration execution | 4 | LIMITED | true | Focused and full Jest assertions pass. Open handles and the missing race assertion remain. | unknown application owner | Add the race assertion and close open handles. | 5 / SUPPORTED | Removes a test-quality limit. | Clean focused and full runs with race coverage. |
| CR-06 | Browser and system execution | 5 | FAILED | true | E2E-07 is a current valid failure. E2E-06 is a current valid pass. | unknown application owner | Correct natural recovery and rerun affected browser cases. | 5 / SUPPORTED | Removes a material NO_GO blocker. | Candidate-bound passing browser results. |
| CR-07 | Artifact and target identity | 0 | UNKNOWN | true | No immutable build, digest, served bytes, or target identity is bound. | unknown release owner | Bind artifact provenance, target, configuration, and deployment receipt. | 5 / SUPPORTED | Changes artifact evidence from unknown to assessed. | Immutable provenance and target receipt. |
| CR-08 | Recovery and operations | 0 | UNKNOWN | true | Rollback, monitoring, stop triggers, and operators are not bound. | unknown release owner | Test rollback and record operating checks and owners. | 4 / SUPPORTED | Removes operational blocking evidence gaps. | Reviewed rollback and operating evidence. |

```yaml
evidence_confidence_score: 100
confidence_level: HIGH
evidence_confidence: HIGH
confidence_score_basis: "The NO_GO recommendation is controlled by direct current failures in code review, requirement conformance, and browser execution. Each controlling dimension scores 5/5 for evidence of failure. Artifact and operations remain unknown and block any positive release judgment, but they do not weaken confidence in this technical hold."
release_status: NO_GO
can_go: false
production_recommendation: DO_NOT_RECOMMEND
confidence_increasing_actions:
  - id: RC-FRESH-ACT-01
    priority: P0
    owner: unknown application owner
    current_score: 5
    current_status: FAILED
    action: "Bind automatic refresh responses to the initiating session or generation and add the delayed logout/login race assertion."
    evidence_to_close: "Fresh F03 before-login and after-login cases pass with Session B preserved."
    target_score: 5
    target_status: SUPPORTED
    expected_release_status_effect: "Closes the fresh P1 code-review blocker; reassess remaining blockers."
    reassess_when: "The fixed candidate and matching race execution are retained."
  - id: RC-FRESH-ACT-02
    priority: P0
    owner: unknown application owner
    current_score: 5
    current_status: FAILED
    action: "Preserve the Timeout control during natural renewal and correct delayed recovery."
    evidence_to_close: "Passing E2E-07 and delayed-recovery results bound to the fixed candidate."
    target_score: 5
    target_status: SUPPORTED
    expected_release_status_effect: "Closes two material behavior blockers; reassess requirement status."
    reassess_when: "Natural and delayed canonical cases pass with source and environment bindings."
  - id: RC-FRESH-ACT-03
    priority: P1
    owner: unknown release owner
    current_score: 0
    current_status: UNKNOWN
    action: "Bind immutable artifact, target configuration, rollback, monitoring, stop triggers, and operator ownership."
    evidence_to_close: "Build manifest, artifact digest, deployment receipt, rollback proof, and operating checks."
    target_score: 4
    target_status: SUPPORTED
    expected_release_status_effect: "Changes artifact and operating dimensions from unknown to assessed."
    reassess_when: "The exact PROD candidate and operating evidence are retained."
```

The score measures evidence support for the `NO_GO` recommendation. It is not a success probability.
The `NO_GO` status means the candidate cannot go to PROD. Human authorization remains separate.

## Readiness conclusion and authorization

```yaml
assistant_assessment:
  assessment_state: COMPLETE
  evidence_confidence_score: 100
  confidence_level: HIGH
  evidence_confidence: HIGH
  confidence_score_basis: "Direct candidate-bound race, requirement, and browser failures support the technical hold."
  release_status: NO_GO
  can_go: false
  production_recommendation: DO_NOT_RECOMMEND
  scope_basis: Fresh review of candidate ae8213f against base 6e34da3 with retained local test and browser evidence.
  controlling_evidence_refs:
    - evidence/code-review-refresh-20261025/review.json
    - evidence/code-review-fresh-20261025/race-f03-after/run.json
    - evidence/active-cutoff-fix-20261024/browser/cutoff-natural-20261025T004053/artifacts/result.json
  blocking_action_refs:
    - "#risks-and-exceptions"
    - "#confidence-score-and-release-status"
  confidence_increasing_actions:
    - RC-FRESH-ACT-01
    - RC-FRESH-ACT-02
    - RC-FRESH-ACT-03
  reassess_when:
    - FRESH-CR-01 passes before-login and after-login delivery tests.
    - E2E-07 and delayed recovery pass on the fixed candidate.
    - Immutable build, target, configuration, rollback, and operating evidence is supplied.
readiness_state: pending
readiness_decision: null
reviewer: null
reviewed_at: null
decision_evidence: null
deployment_authorization: null
authorizing_actor: null
authorized_at: null
audit_event_ref: null
```

## Facts, inferences, and unresolved questions

- Fact: the fresh exact-range review inspected three changed paths and found one P1 finding.
- Fact: the new `useController.ts:131` path calls `getRefreshToken()` at refresh expiry while access remains valid.
- Fact: the fresh F03 characterization leaves Session A refresh state after Session B login and clears Session B during recovery.
- Fact: focused Jest reports 3 suites and 95 tests passed. Full Jest reports 116 suites and 413 tests passed, with an open-handle warning after the summary.
- Fact: E2E-06 passes and E2E-07 fails in the retained local browser fixture.
- Inference: users can lose a fresh session when the target shares this response and logout behavior.
- Unknown: production bytes, effective token settings, served consumers, affected population, occurrence rate, rollback operator, and deployment authorization.

## Findings

### FRESH-CR-01: Automatic refresh can overwrite a fresh session

The candidate adds `getRefreshToken()` at [useController.ts:131](../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L131).
The success interceptor sends refresh responses to [handleRefreshToken](../../repos/ui/mfe-base/src/utils/login.ts#L117).
The handler dispatches the returned token without checking the initiating session.
The fresh F03 run records Session A after Session B login, sends Session A during recovery, and clears Session B.
Owner: unknown application owner.
Action: add session ownership or generation checks, cancel pending work at logout, and rerun both delivery orders.

### Existing conformance blockers

E2E-07 remains failed. Delayed recovery remains failed. Artifact, target, rollback, and operating evidence remain unknown.
These findings remain separate from the fresh code-review finding and continue to control the release recommendation.

## Sources

| Source ID | Locator | Exact revision | Hash | Owner, authority, and limits |
| --- | --- | --- | --- | --- |
| SRC-session-fresh-code-review-20261025 | [fresh review](evidence/code-review-refresh-20261025/review.json) | `ae8213f` vs `6e34da3` | `sha256: 5db4fbbc2a0947e2e0becef21c9306b9add89df1c955d45c2feaa361b3d56925` | unknown owner; local source and synthetic race evidence |
| SRC-session-fresh-race-20261025 | [F03 run](evidence/code-review-fresh-20261025/race-f03-after/run.json) | `ae8213f2963047e7c126d01f4003cee1236abc25` | `sha256: 7b6093a522ecf6c53d6dae52f0c5eee68cc0984e1e95927bea91bff0794c54cd` | unknown owner; synthetic Axios adapter, no provider parity |
| SRC-session-natural-recovery-20261025 | [E2E-07 result](evidence/active-cutoff-fix-20261024/browser/cutoff-natural-20261025T004053/artifacts/result.json) | candidate-bound local fixture | retained artifact hash | unknown owner; local browser and fixture only |
| SRC-session-active-cutoff-20261024 | [E2E-06 result](evidence/active-cutoff-fix-20261024/browser/cutoff-cross-20261024T234223/artifacts/result.json) | candidate-bound local fixture | retained artifact hash | unknown owner; local browser and fixture only |
| SRC-session-requirement | [active session renewal requirement](../../knowledge/candidates/requirements/REQ-active-session-renewal.md) | v4 | `sha256: 828d62209f11dd9bb9dee893ddc80e7e5d4dc6abd3c58170e902dab61bc587aa` | publication review pending; intent source, not execution evidence |

No deployment, push, pull request, or external communication occurred during this assessment.
