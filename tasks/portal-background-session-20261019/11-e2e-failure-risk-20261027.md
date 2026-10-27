---
artifact_kind: test-execution-report
id: REPORT-session-e2e-failure-risk-20261027
version: 1
status: draft
owner: unknown
source_refs:
  - SRC-renewed-e2e-20261027
related_ids:
  - DEFECT-portal-background-session-20261019
  - REQ-active-session-renewal
  - ASSESS-session-delivery-20261026
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

# E2E failures and go-live risk

> **Production remains blocked. Eight final-runtime browser cases failed.**
> Action: retain the requested backlog scope and close the [release evidence gaps](#production-release-gaps).
> Consequence: local results cannot establish the deployed artifact or its operational readiness.
> Owner: unknown release owner. Evidence: [final case inventory](evidence/four-checks-20261027/e2e/completion.json) and [release-access audit](evidence/four-checks-20261027/release-evidence/closure-audit.md).

SRC-renewed-e2e-20261027: the [latest user request](evidence/user-input-20261027-review-e2e-traceability.txt), 27 October 2026.
The request asks for failure points and go-live risks.
The [scope answer](evidence/user-input-20261027-backlog-scope.txt) retains the earlier backlog scope for activity and sharing failures.
The earlier [P4/S4 direction](evidence/minor-fixes-20261025/setup/failed-case-priority-user-input-20261026.txt) names activity and cancellation groups.
It does not assign a numeric priority to the isolated sharing failure or the provider diagnostic.

No deployment approval or universal risk waiver is inferred.

## Run identity and provenance

The final test commit is `e0030f5cf920b715f5831faf7df86cb9789b6d0f`.
Browser runtime `1b7de4fe5d7db0c7f490a060d4e3b1c441a5c303` matches that commit's runtime.
The [binding](evidence/four-checks-20261027/e2e/final-release-binding.json) records the test-only difference and matched source.
The local main comparison uses `f025513f696476a9cc8162681410cbd21e029bcb`.
The inspected test engine uses `78141a4eec8040dd0d1ac8a6579b20f612fca0f0`.

The [source audit](evidence/renewed-review-20261027/e2e/source-audit.json) records hashes and source identities.

The final run executed 27 cases. Nineteen runner cases passed and eight failed.
The original business inventory contains 13 passes and six failures. It excludes the provider diagnostic and supplemental sharing case.
Some cases use a 60-second access fixture, a local BFF, and a toolkit substitute.

The [environment evidence](evidence/four-checks-20261027/e2e/environment.json) does not establish production parity.
Failure stops each affected case at its first failed assertion. Later outcomes are not proven.

## Assertions and outcomes

The following eight sections link each canonical case, first failure, baseline, and affected source.
Each outcome is scoped to its disclosed fixture. A failed prerequisite prevents later assertions.

## Findings

Six failures concern activity renewal, request sharing, and cancellation. Their earlier scope remains in the backlog.
One supplemental sharing case confirms a separate pending-request failure. The provider diagnostic remains conditional.

## Continuous activity: mouse, keyboard, and scroll

The actor has a valid session with at least 30 seconds before access expiry.
The test records trusted activity events. It checks a 15-second interval.

1. The actor performs the specified activity every 100 milliseconds.
2. The driver counts successful renewal responses during the interval.
3. The driver checks that renewal advances access expiry.

The [shared assertion](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/support/activity.cjs#L9) defines the exact checks.
The intended result is at least one successful renewal during the interval.

### E2E-01: continuous mouse movement

Definition: [E2E-01](06-test-cases.md#e2e-01). Requirement: [AC-1](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L187).
Main failed the renewal assertion. See the [paired baseline](evidence/delivery-confidence-20261026/browser/comparison.json).
The [final result](evidence/four-checks-20261027/e2e/native-mouse-20261027T064442/artifacts/activity-mouse-1793083491523/result.json) also failed that assertion.

The retained lifecycle recorded 147 mouse events, including setup events. No extension succeeded inside the asserted window.

The [Home handler](../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L63) resets a five-second timer after each mouse movement.
Continuous movement prevents that timer from reaching its callback during the test interval.
Inference: sufficiently continuous activity can leave access approaching expiry without activity renewal.
An eventual prompt or sign-in depends on later expiry and recovery behavior. This test did not establish either outcome.

Disposition: inherited under the paired fixture. User direction is P4/S4 backlog.
Owner: unknown application owner. Next action: retain the backlog and rerun the original predicate after any future correction.

### E2E-02: continuous keyboard activity

Definition: [E2E-02](06-test-cases.md#e2e-02). Requirement: [AC-2](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L194).
Main failed the renewal assertion. See the [paired baseline](evidence/delivery-confidence-20261026/browser/comparison.json).
The [final result](evidence/four-checks-20261027/e2e/native-keyboard-20261027T064514/artifacts/activity-keyboard-1793083523326/result.json) also failed.

The retained lifecycle recorded 139 keyboard events. No extension succeeded inside the asserted window.

The inspected [Home root](../../repos/ui/mfe-base/src/pages/Home/index.tsx#L56) binds mouse movement, not keyboard renewal.
Inference: keyboard-only work can continue without the requested activity renewal.
The test did not demonstrate an eventual sign-in, lost work, or production frequency.
Disposition: inherited under the paired fixture. User direction is P4/S4 backlog.

Owner: unknown application owner. Next action: retain the backlog and verify keyboard activity after any future correction.

### E2E-03: continuous scroll activity

Definition: [E2E-03](06-test-cases.md#e2e-03). Requirement: [AC-3](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L201).
Main failed the renewal assertion. See the [paired baseline](evidence/delivery-confidence-20261026/browser/comparison.json).
The [final result](evidence/four-checks-20261027/e2e/native-scroll-20261027T064546/artifacts/activity-scroll-1793083554616/result.json) also failed.

The retained lifecycle recorded 146 scroll events. No extension succeeded inside the asserted window.
One earlier setup extension occurred before the assertion window. The test explicitly excludes setup renewal.

The inspected [Home root](../../repos/ui/mfe-base/src/pages/Home/index.tsx#L56) binds mouse movement, not scroll renewal.
Inference: scroll-only work can continue without the requested activity renewal.
The test did not demonstrate an eventual sign-in, lost work, or production frequency.
Disposition: inherited under the paired fixture. User direction is P4/S4 backlog.

Owner: unknown application owner. Next action: retain the backlog and verify scroll activity after any future correction.

## E2E-08: original request-sharing test

Definition: [E2E-08](06-test-cases.md#e2e-08). Assertions: [original test](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/cases/e2e-08.cjs#L7).
Setup: valid access remains for at least 30 seconds. The fixture holds any extension request before dispatch.

1. The actor moves the mouse repeatedly for 12 seconds.
2. The driver checks for exactly one held extension request.
3. The driver would release that request and check the installed access and protected call.

Intended result: one pending request is shared without cancellation.
Main observed zero held requests. The [paired baseline](evidence/delivery-confidence-20261026/browser/comparison.json) records the failed prerequisite.
The [final result](evidence/four-checks-20261027/e2e/native-single-20261027T065231/artifacts/slow-activity-single-flight-1793083961157/result.json) also observed zero.
The five-second debounce explains why repeated 100-millisecond events do not dispatch during the interval.

The case stopped before it could test sharing or protected access. It cannot by itself prove a sharing failure.

Potential consequence: continuous activity may not trigger renewal within the interval.
Disposition: inherited under this fixture. P3/S3 for sharing was an analyst proposal, not a human classification.
Owner: unknown application owner. Next action: retain the failed prerequisite and the independent pending-request result below.

## BROWSER-SHARING-PENDING: already pending request

Definition: [BROWSER-SHARING-PENDING](06-test-cases.md#browser-sharing-pending).
Assertions: [supplemental test](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/supplemental/deliveryConfidence.cjs#L55).
Setup: valid access exists. The driver holds the first actual extension request before dispatch.

1. The actor moves the mouse and waits until one request is pending.
2. The actor moves the mouse again while that request remains pending.
3. The driver waits 6.5 seconds and checks request and cancellation counts.

Intended result: one request remains pending and no cancellation occurs.
Main observed two requests and one cancellation. See the [baseline result](evidence/delivery-confidence-20261026/browser/supplemental-comparison.json).
The [final result](evidence/four-checks-20261027/e2e/headless-sharingPending-20261027T064826/artifacts/BROWSER-SHARING-PENDING-1793083716933/result.json) observed the same counts.
The unchanged [extension helper](../../repos/ui/mfe-base/src/hooks/service/util/extend.ts#L8) aborts its prior controller before starting another request.

The case stopped at the request-count assertion. It did not prove that the original response installed or protected access succeeded.

Potential consequence: redundant authentication requests and canceled pending work during repeated activity.
The extent of user-visible delay, service load, and production exposure remains unmeasured.
Disposition: inherited in the controlled comparison. The user retained the earlier backlog scope.

Owner: unknown business and application owners. Next action: record the remaining sharing impact disposition for the selected release.

## E2E-18: logout while activity renewal is pending

Definition: [E2E-18](06-test-cases.md#e2e-18). Assertions: [cancellation test](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/cases/e2e-18.cjs#L7).
Setup: an actual successful extension response is held before browser delivery.

1. The actor signs out while the extension remains pending.
2. The driver checks whether logout or Home unmount cancels the pending browser request.
3. The driver would release the late response and inspect authentication and Home state.

Intended result: cancellation occurs and late work cannot restore the ended session.
Main failed the cancellation predicate. See the [paired baseline](evidence/delivery-confidence-20261026/browser/comparison.json).
The [final result](evidence/four-checks-20261027/e2e/native-activityLogout-20261027T070124/artifacts/pending-activity-home-unmount-cancellation-1793084494188/result.json) also failed that predicate.

The case stopped before its late-response restoration assertions. It does not prove that authentication was restored.

The [Home cleanup](../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L69) clears timers. It does not directly abort the extension controller.
The final [session guard](../../repos/ui/mfe-base/src/hooks/service/util/succes.response.handler.ts#L35) rejects identified stale-session responses.
That guard limits a potential late-response risk. This failed case does not establish its outcome.

Disposition: inherited cancellation failure in the paired fixture. User direction is P4/S4 backlog.
Owner: unknown application owner. Next action: retain the backlog and verify late-response behavior if that scope resumes.

## E2E-19: activity renewal held through the expiry prompt

Definition: [E2E-19](06-test-cases.md#e2e-19). Assertions: [late-response test](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/cases/e2e-19.cjs#L7).
Setup: the session has usable refresh credentials. A successful activity extension response is held before browser delivery.

1. The actor starts an activity renewal before access expiry.
2. The access deadline passes and the timeout prompt opens.
3. The driver checks that the earlier activity request was canceled.
4. The driver would complete manual renewal and release the earlier response.

Intended result: cancellation prevents the earlier response from replacing successful manual renewal.
The original main setup did not reach the cancellation assertion.
Main then failed the same predicate after an [adapted real-service refresh setup](evidence/delivery-confidence-20261026/browser/main-adapted-setup.json).
The [final result](evidence/four-checks-20261027/e2e/native-late-20261027T070159/artifacts/late-activity-after-manual-success-1793084525224/result.json) also failed cancellation.

This is a conditional inherited comparison. It is not an unmodified main-to-candidate execution.
The case stopped before manual renewal and late-response assertions. It does not prove a token overwrite.

The [session guard](../../repos/ui/mfe-base/src/utils/sessionEpoch.ts#L17) distinguishes session epochs, not every same-session renewal order.
Potential consequence: the ordering of a late response and manual renewal remains unverified under this failure.
Disposition: the named cancellation group remains P4/S4 backlog by user direction.
Owner: unknown application owner. Next action: retain the adapted baseline limit and test the full late-response sequence when the scope resumes.

## E2E-12: inconsistent authentication response diagnostic

Definition: [E2E-12](06-test-cases.md#e2e-12). Assertions: [diagnostic test](../../repos/testing/ratan-test-engine/Tests/ratan/plugin/ui/session/cases/e2e-12.cjs#L7).
Setup: the driver obtains a successful real extension response and keeps its access header.
The driver deliberately changes the response body to `result=false`.

1. The actor triggers activity renewal.
2. The browser receives the controlled inconsistent response.
3. The driver checks that the previous access remains installed.
4. The driver would check a later successful retry and protected access.

Intended diagnostic result: the negative body does not replace access.
No paired main execution is retained. The [historical comparison](evidence/delivery-confidence-20261026/browser/comparison.json) records that absence.
The [final result](evidence/four-checks-20261027/e2e/native-inconsistent-20261027T065615/artifacts/inconsistent-activity-response-rejected-1793084182571/result.json) installed the response header and failed the access-preservation assertion.
The inspected [final handler](../../repos/ui/mfe-base/src/hooks/service/util/succes.response.handler.ts#L84) calls `handleLogin` for extension responses.

It does so before checking a business `result` value for this endpoint.

The baseline handler also called `handleLogin` on extension responses. That is a source comparison, not a paired execution.
The actual provider contract and occurrence of this contradictory response remain unknown.
If the provider can issue it, the client may accept the header despite a negative body. That consequence remains conditional.

The test stopped before the retry and protected-call assertions. It does not establish their outcomes.
Disposition: diagnostic outside business acceptance totals. No user priority or production incident is established.

Owner: unknown authentication owner. Next action: confirm the actual provider contract and decide the applicable expectation.

## Production release gaps

The [release-access audit](evidence/four-checks-20261027/release-evidence/closure-audit.md) found no evidence closing these items.
An allowed ADO project-list read failed generically. Its cause remains unknown.
No target access, production test, deployment, or external write occurred.

| Item | Remaining evidence or decision | Consequence and owner action |
| --- | --- | --- |
| [GL-03](10-delivery-confidence-20261026.md#gl-03) | CI build, dependency identity, artifact digest, and served module are unbound. | The target package cannot be matched to tested source. Unknown release owner: bind matching receipts. |
| [GL-04](10-delivery-confidence-20261026.md#gl-04) | Deployed baseline, settings, authentication service, and consumer versions are unknown. | Local checks cannot establish target behavior. Unknown release owner: bind and verify the target composition. |
| [GL-05](10-delivery-confidence-20261026.md#gl-05) | No recovery exercise is bound to the selected artifact and target. | Restoration behavior is unknown. Unknown release owner: exercise recovery and protected access. |
| [GL-06](10-delivery-confidence-20261026.md#gl-06) | Smoke checks, monitoring, stop conditions, and operating owners are unbound. | Detection and response remain unproven. Unknown release owner: record and exercise the operating plan. |
| [GL-07](10-delivery-confidence-20261026.md#gl-07) | Full release-scope acceptance and residual-impact decisions remain unrecorded. | Remaining exposure is unaccepted. Unknown business owner: review the exact scope and sharing risk. |
| [GL-08](10-delivery-confidence-20261026.md#gl-08) | Actual deployment authorization is unrecorded. | The record cannot represent deployment as authorized. Unknown authorizing owner: record the decision after reassessment. |

The [current assessment](10-delivery-confidence-20261026.md) records `BLOCKED`, `can_go: false`, and `INSUFFICIENT_EVIDENCE`.
Its decision certainty is `0/100`, `UNDETERMINED`. The score measures support for the production judgment, not failure probability.
Natural frozen-tab recovery passed locally. Local success does not resolve deployment identity or production exposure.

No test establishes zero impact across every configuration or consumer.

## Verification conclusion

All 27 planned browser cases ran. Six original business cases and two additional checks failed.
The user retained the earlier backlog scope. Four foundational evidence groups and two decision records remain open.

The current evidence does not support a production recommendation. No deployment authorization is recorded.

## Facts, inferences, and unresolved questions

Fact: local final-source executions failed the eight assertions described above.
Inference: unrecovered access expiry can interrupt work. These failures do not establish an observed production incident.
Unknown: actual deployed versions, occurrence frequency, affected population, and the inconsistent provider response contract.
Unknown: expected recovery behavior when no usable refresh credential exists.

## Retained evidence inventory

| Evidence | Identity and result | Limit |
| --- | --- | --- |
| [Final case reconciliation](evidence/four-checks-20261027/e2e/reconciliation.json) | Runtime `1b7de4f`; 27 cases, 19 runner passes, eight failures. | Controlled local environment; failed assertions block later assertions. |
| [Baseline comparison](evidence/delivery-confidence-20261026/browser/comparison.json) | Main `f025513`; selected paired cases. | Original E2E-19 setup did not reach cancellation. |
| [Adapted main setup](evidence/delivery-confidence-20261026/browser/main-adapted-setup.json) | Actual local BFF and public refresh service. | The setup differs from the original main execution. |
| [Source audit](evidence/renewed-review-20261027/e2e/source-audit.json) | Exact source commits and SHA-256 hashes. | Source inspection does not establish deployed bytes. |

## Sources

SRC-renewed-e2e-20261027: [user request](evidence/user-input-20261027-review-e2e-traceability.txt), 27 October 2026.
The [scope answer](evidence/user-input-20261027-backlog-scope.txt) retains the earlier backlog treatment.
The [canonical cases](06-test-cases.md) define the test steps and expected assertions.
