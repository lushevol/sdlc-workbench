---
artifact_kind: test-execution-report
id: REPORT-session-bau-exposure-20261028
version: 1
status: draft
owner: unknown
source_refs:
  - SRC-session-bau-exposure-20261028
related_ids:
  - DEFECT-portal-background-session-20261019
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

# User exposure and BAU impact

> **BLOCKED: the stale dialog blocks a synthetic session; production exposure remains unknown.**
> Action: verify production trigger reachability and close the release evidence gaps.
> Consequence: the available evidence cannot establish business-as-usual safety or user frequency.
> Owner: unknown release owner. Evidence: [stale-dialog probe](evidence/claude-coordination-20261027/reconciliation/stale-modal-probe/execution.json) and [release inventory](12-final-release-issues-20261027.md).

## Run identity and provenance

SRC-session-bau-exposure-20261028: the [user request](evidence/user-input-20261028-bau-exposure-impact.txt) asks about user exposure and BAU interruption.
The inspected source is final candidate `e0030f5cf920b715f5831faf7df86cb9789b6d0f`.
Main `f025513f696476a9cc8162681410cbd21e029bcb` is a source baseline, not an identified production deployment.
The [reproduction report](13-review-e2e-reproduction-20261028.md) gives steps for each issue.
The [origin and priority assessment](14-issue-baseline-priority-20261028.md) records baseline status and proposed ratings.

No representative production session counts, request timing, affected users, or incident rates are available.
Production occurrence frequency is UNKNOWN for every issue below. Do not interpret deterministic test results as prevalence.
`Observed` refers only to the stated local fixture. `Possible` requires the listed conditions.
`Conditional block` means the affected journey may stop if those conditions occur.
`Unknown impact` means the evidence does not support labeling the user effect minor or blocking.
Unverified restoration, refresh, or reauthentication is not presented as a guaranteed workaround.

## Assertions and outcomes

The [E2E analysis](11-e2e-failure-risk-20261027.md) retains the failed predicates and their execution limits.
The local final-runtime inventory has 19 runner passes and eight failures across 27 cases.
The user-assigned P4/S4 backlog ratings remain unchanged for E2E-01, 02, 03, 18, and 19.

| E2E issue | How a user could encounter it | BAU effect and blocking assessment | Origin and priority |
| --- | --- | --- | --- |
| [E2E-01: continuous mouse](06-test-cases.md#e2e-01) | The user moves the mouse continuously. The fixture moves it every 100 ms for 15 seconds. | No renewal succeeds within the test window. A timeout can interrupt work if access expires and recovery fails. Blocking or lost work was not observed. | Existing; P4/S4 user. |
| [E2E-02: keyboard activity](06-test-cases.md#e2e-02) | The user works with keyboard events. The fixture sends one every 100 ms for 15 seconds. | No activity renewal succeeds in that window. Interruption requires later expiry and unsuccessful recovery. Blocking was not observed. | Existing; P4/S4 user. |
| [E2E-03: scroll activity](06-test-cases.md#e2e-03) | The user performs scroll-only work. The fixture sends one event every 100 ms for 15 seconds. | No activity renewal succeeds in that window. Later timeout and interruption are conditional. Blocking was not observed. | Existing; P4/S4 user. |
| [E2E-08: original sharing case](06-test-cases.md#e2e-08) | The user moves continuously while access remains valid. The fixture uses events every 100 ms for 12 seconds. | Zero requests start. The case fails before testing sharing. The later user effect is unknown. | Existing prerequisite; P4/S4 proposed. |
| [Pending sharing](06-test-cases.md#browser-sharing-pending) | A slow extension is pending when later activity starts another eligible extension. | Two requests and one cancellation occur in both fixtures. Delayed renewal and extra traffic are possible. User-visible delay or blocking was not measured. | Existing; P4/S3 conditional, proposed. |
| [E2E-18: logout cancellation](06-test-cases.md#e2e-18) | The user logs out or Home unmounts while an activity extension is pending. | The request is not canceled. The test stops before late-response effects. Session restoration or another user block is not demonstrated. | Existing; P4/S4 user. |
| [E2E-19: expiry-prompt cancellation](06-test-cases.md#e2e-19) | An activity extension remains pending when the expiry prompt opens. | The request is not canceled. The test stops before manual renewal and late delivery. Token overwrite or blocking is not demonstrated. | Likely existing with adapted baseline; P4/S4 user. |
| [E2E-12: inconsistent response](06-test-cases.md#e2e-12) | The provider would need to return `result=false` together with an authorization header. The fixture synthesizes this response. | The client installs the header. Provider occurrence and user effect are unknown. A blocking outcome is not demonstrated. | Paired baseline absent; P3 investigation, S unknown, proposed. |

Some local controls show recovery can work in selected conditions.
Manual renewal closes the prompt in one fixture, and a 30-minute natural freeze recovery passed locally.
These checks do not establish recovery for every real provider response or deployed session.

## Findings

The [code-review audit](evidence/claude-coordination-20261027/reconciliation/review.md) and [configuration evaluation](evidence/delivery-confidence-20261026/independent-review/build-config-effects.json) support the following conditions.
All production frequencies are unknown. The application and business owners are unknown.
Priorities and conditional severities below are analyst proposals except where stated.

| Review issue | User exposure conditions | BAU effect and blocking assessment | Origin and priority |
| --- | --- | --- | --- |
| [Stale timeout dialog](evidence/claude-coordination-20261027/reconciliation/stale-modal-probe/execution.json) | A replacement login completes during the one-second logout delay while Home stays mounted. Normal local routing separates Home and Login; production reachability is unknown. | **Blocking in the synthetic test:** the old modal remains, Extend is disabled, and Logout does nothing. The replacement token remains. No workaround was tested. | New guard; P2/S2 conditional. |
| [Renewal token format](evidence/claude-coordination-20261027/reconciliation/adversarial-client.json) | The deployed BFF returns an opaque or otherwise rejected access token on Extend. The actual contract is unknown. | The response is rejected and the prompt remains. Repeated incompatible responses could block renewal. This is conditional, not an observed production block. | New validation; P2/S2 conditional. |
| [Failed replacement login](evidence/claude-coordination-20261027/reconciliation/adversarial-client.json) | An active session submits an in-place fresh login and it fails. Production UI reachability is unknown. | The request clears existing refresh state before its result. Later recovery or old in-flight work may fail. An immediate user block was not shown. | New transition; P2/S2 conditional. |
| [Direct token replacement](evidence/claude-coordination-20261027/reconciliation/adversarial-support.json) | A consumer replaces access directly without the normal login interceptor. No local non-test caller was found. | Old refresh state can remain with new access. Renewal or identity mismatch is possible. Cross-user access and a user block are unproved. | New reducer semantics; P2/S2 conditional. |
| [Pending acquisition](../../repos/ui/mfe-base/src/components/Timeout/common/useController.ts#L49) | Access expires while refresh acquisition remains pending. | Extend remains disabled until settlement. The prompt can temporarily interrupt work; Logout remains available. Suspended wall-clock duration is unknown. | New wait; P2/S3 conditional. |
| [Unusable refresh expiry](evidence/claude-coordination-20261027/reconciliation/adversarial-session.json) | An existing refresh token lacks usable expiry when access expires. Validity and deployed occurrence are unknown. | The candidate starts logout rather than offering recovery. Affected work can be interrupted and authentication may be needed. Production effect is unverified. | Changed fallback; P2/S2 conditional. |
| [Near-expiry acquisition](evidence/claude-coordination-20261027/reconciliation/adversarial-session.json) | Home starts in the last 25 seconds of access, or visibility returns after a missed deadline. | No immediate catch-up acquisition starts. Existing valid refresh or other paths may permit recovery. A BAU block has not been observed. | Changed schedule; P2/S3 conditional. |
| [Loopback chunk path](evidence/delivery-confidence-20261026/independent-review/build-config-effects.json) | The deployed artifact must retain the loopback path and request a lazy chunk unavailable on the user's browser host. | Home or an admin journey could fail to load. This could block that journey. The actual build and deployment are unverified. | Existing webpack rule; P2/S2 conditional. |
| [Development remote](evidence/delivery-confidence-20261026/independent-review/build-config-effects.json) | The build must select the development remote and an executed consumer must import it. No local application import was found. | A wrong or unavailable remote could block that consumer journey. User exposure is unestablished. | Added setting; P2 investigation, S unknown. |
| [One-byte body limit](evidence/delivery-confidence-20261026/independent-review/build-config-effects.json) | A body request must pass through the affected Express server with that effective limit. No local supported business body route was found. | Such a request could be rejected. Ordinary BFF calls are not shown to use this server. User impact is unknown. | Added setting; P3 investigation, S unknown. |
| [External pipeline template](10-delivery-confidence-20261026.md#gl-04) | A build uses the unavailable external template. Its effective output is unknown. | This is a release-verification gap. A harmful user-facing build has not been observed. | Existing reference; P3 investigation, S unknown. |
| [Stale loader completion](../../repos/ui/mfe-base/src/hooks/service/util/requestLoading.ts#L12) | A stale request completes after an epoch change without a subsequent loader publication. | A page-sized loader could persist and block interaction. Persistence and production reachability are not reproduced. | New state path; P2/S3 conditional. |
| [Configless error cleanup](../../repos/ui/mfe-base/src/hooks/service/util/requestLoading.ts#L36) | An error without request config occurs while another loader-enabled request remains pending. | The loading indication can disappear early while other work continues. A user block or data loss is unproved. | Existing; P4/S3 conditional. |
| [Stale response rejection](evidence/claude-coordination-20261027/reconciliation/adversarial-client.json) | A response arrives after its session changes, and an external consumer mishandles cancellation. | A feature could fail or show an error. Local session paths handle their failures. An affected external consumer is unknown. | New semantics; P3/S3 conditional. |
| [Relogin rejection contract](evidence/claude-coordination-20261027/reconciliation/retry-findings.json) | A network failure reaches an external consumer that ignores the newly returned rejection. | A consumer may show an error or fail to complete a feature. Local Timeout catches it. Actual BAU impact is unknown. | New API behavior; P3/S3 conditional. |
| [Cancellation error shape](evidence/claude-coordination-20261027/reconciliation/retry-findings.json) | A consumer depends on previous cancellation-error identity or properties. No affected caller is known. | User impact is unknown. Neither minor nor blocking behavior is demonstrated. | New semantics; P3 investigation, S unknown. |
| [Renewal after deadline](evidence/renewed-review-20261027/codex/review.md) | The user selects Extend before expiry, but the response arrives after the deadline. Provider validation decides the result. | The prompt waits while the request is pending. Logout remains available. The final renewal outcome and production impact are unknown. | Changed wait; P3 investigation, S unknown. |
| [Ignore pattern](evidence/claude-coordination-20261027/reconciliation/independent-support.json) | A developer runs repository-wide formatting on a matching pnpm lockfile. No tracked lockfile was found. | Possible formatting churn is a maintenance effect. End-user BAU impact is not established. | New typo; P4/S4 conditional. |

## Verification conclusion

The only directly demonstrated current-candidate blocking behavior is the synthetic stale timeout dialog.
It does not establish a reachable production journey. Other blocking impacts are conditional or unknown.
Production release remains `BLOCKED`, with `can_go: false`.
The prior P4/S4 backlog directions do not establish successful behavior or deployment authorization.
No new test or production access occurred for this assessment.

## Facts, inferences, and unresolved questions

Fact: the stated local activity and cancellation predicates failed. The stale dialog was reproduced in a synthetic harness.
Inference: unsuccessful session recovery can interrupt a user's work. Lost transactions or unsaved work were not demonstrated.
Unknown: deployed artifact, provider behavior, affected consumers, occurrence rates, and user interruption duration.
An event's production frequency cannot be derived from a deliberately seeded fixture.

## Retained evidence inventory

The [browser reconciliation](evidence/four-checks-20261027/e2e/reconciliation.json) retains each final-runtime result.
The [claim reconciliation](evidence/claude-coordination-20261027/reconciliation/retry-findings.json) records source-based limits and rejected claims.
The [release-access audit](evidence/four-checks-20261027/release-evidence/closure-audit.md) records unbound production evidence.

## Sources

The [user request](evidence/user-input-20261028-bau-exposure-impact.txt), [E2E analysis](11-e2e-failure-risk-20261027.md), [reproduction report](13-review-e2e-reproduction-20261028.md), and [origin assessment](14-issue-baseline-priority-20261028.md) define this report.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
