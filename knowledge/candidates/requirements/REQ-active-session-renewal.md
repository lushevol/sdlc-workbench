---
type: Requirement
id: REQ-active-session-renewal
version: 5
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: conversation:current/user-reply/session-renewal-intent
  revision: request-2026-10-15
  sha256: d3976f80aaeba02b2397d9731a142767225d2a3ee6dcd1a2de351d3d748217e9
- resource: conversation:current/user-reply/session-activity-and-idle-intent
  revision: reply-2026-10-15
  sha256: a9654884d2ff9f2f27a3185268b251694b51145d50aa7bee6ab2d75c911e90e3
- resource: conversation:portal-session-renewal-clarification-20261020
  revision: user-reply-20261020
  sha256: cce729b9225850ceb9e671e0922af1d2e1666488a36b897f43d304334322c9ba
- resource: conversation:portal-session-refresh-prod-status-20261026
  revision: user-clarification-20261026-1
  sha256: 2f44886e5044d5459d5330f0886e39b118080330ca182673d699246fb90cb98e
- resource: conversation:portal-session-failed-case-triage-20261026
  revision: user-clarification-20261026-1
  sha256: 7edd8d3e187ec65ec1555fc79dc45f44d130a3647e851b048344a7fe75b49e6e
previous_version: 4
previous_content_sha256: 828d62209f11dd9bb9dee893ddc80e7e5d4dc6abd3c58170e902dab61bc587aa
generated:
  by: agent:codex
  at: '2026-10-26T05:32:15.641082+00:00'
verified: []
description: Keep active portal sessions renewable through mouse, keyboard, and scroll
  activity without a fixed reauthentication maximum.
rationale: The user requested continued renewal during active use and retained refresh-token
  renewal after inactivity.
acceptance_criteria:
- id: AC-1
  given: Given a valid portal session with at least 30 seconds remaining before access
    expiry
  when: When mouse movement occurs every 100 milliseconds for 15 seconds
  then: Then at least one successful renewal occurs before the controlled interval
    ends
  measure:
    metric: successful renewal count
    operator: at_least
    value: 1
    unit: count
- id: AC-2
  given: Given a valid portal session with at least 30 seconds remaining before access
    expiry
  when: When keyboard input occurs every 100 milliseconds for 15 seconds
  then: Then at least one successful renewal occurs before the controlled interval
    ends
  measure:
    metric: successful renewal count
    operator: at_least
    value: 1
    unit: count
- id: AC-3
  given: Given a valid portal session with at least 30 seconds remaining before access
    expiry
  when: When scroll activity occurs every 100 milliseconds for 15 seconds
  then: Then at least one successful renewal occurs before the controlled interval
    ends
  measure:
    metric: successful renewal count
    operator: at_least
    value: 1
    unit: count
- id: AC-4
  given: Given successful renewal responses and accepted user activity before each
    access deadline, including the initial refresh-token expiry
  when: When a controlled clock advances through four hours of continued activity
  then: Then zero fresh SSO prompts occur solely because elapsed session time crosses
    an earlier maximum
  measure:
    metric: elapsed-time-only SSO prompt count
    operator: equals
    value: 0
    unit: count
- id: AC-5
  given: Given an idle-expiry prompt and a usable refresh token
  when: When the user selects renewal and its request remains pending
  then: Then the prompt has zero successful closure transitions before renewal succeeds
  measure:
    metric: premature prompt closure count
    operator: equals
    value: 0
    unit: count
- id: AC-6
  given: Given an idle-expiry prompt and a usable refresh token
  when: When the requested renewal succeeds
  then: Then the prompt closes exactly once after completion
  measure:
    metric: successful prompt closure count
    operator: equals
    value: 1
    unit: count
- id: AC-7
  given: Given an idle-expiry prompt and an unsuccessful refresh-based renewal request
  when: When the request rejects
  then: Then the prompt has zero successful closure transitions and permits another
    renewal attempt
  measure:
    metric: failed-renewal prompt closure count
    operator: equals
    value: 0
    unit: count
review_limits:
- The four-hour fixture horizon does not prove infinite execution.
- Portal-document activity is in scope. Cross-origin embedded application activity
  requires separate integration evidence.
- Environment execution and publication review remain pending.
delivery_status:
  change_kind: requested_session_refresh_enhancement
  production_adoption: not_existing_per_user
  production_status_source: conversation:portal-session-refresh-prod-status-20261026
  production_independently_verified: false
  scope_limit: This status concerns the session-refresh enhancements under assessment. It does not state
    that PROD lacks authentication or all session renewal.
  backlog:
    continuous_activity_renewal:
      priority: P4
      severity: S4
      source: conversation:portal-session-failed-case-triage-20261026
    activity_request_cancellation:
      priority: P4
      severity: S4
      source: conversation:portal-session-failed-case-triage-20261026
  sharing_boundary: Supporting requested boundary; P3/S3 is an analyst proposal. No independent sharing
    failure is demonstrated.
  publication: candidate; human publication review pending
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
---
# Active session renewal

**Status: requested enhancement; not existing PROD behavior, according to the user.**

The [26 October clarification](../../../tasks/portal-background-session-20261019/evidence/minor-fixes-20261025/setup/knowledge-prod-status-user-input-20261026.txt) controls this production-status correction.
Deployment receipts remain unavailable. No replacement PROD behavior is inferred.

## Delivery status

These criteria define target behavior. They do not describe an existing PROD guarantee.

| Scope | Requirement status | PROD status | Source |
| --- | --- | --- | --- |
| Continuous mouse, keyboard, and scroll renewal | Requested target; P4/S4 backlog | Not existing behavior, per user | [Backlog direction](../../../tasks/portal-background-session-20261019/evidence/minor-fixes-20261025/setup/failed-case-priority-user-input-20261026.txt) |
| Renewal across the initial refresh expiry | Requested target; complete duration verification pending | Target adoption is not established | [Current task](../../../tasks/portal-background-session-20261019/10-change-review.md#current-task-state) |
| Pending, successful, and failed manual recovery | Requested target; candidate implementation assessed separately | Candidate evidence does not establish deployment | [Current task](../../../tasks/portal-background-session-20261019/10-change-review.md#current-task-state) |
| Pending activity-request cancellation | Supporting change boundary; P4/S4 backlog | Not existing behavior, per user | [Backlog direction](../../../tasks/portal-background-session-20261019/evidence/minor-fixes-20261025/setup/failed-case-priority-user-input-20261026.txt) |
| Share one pending activity renewal | Supporting requested boundary; verification incomplete | No existing PROD guarantee is asserted | [Sharing scope](../../../tasks/portal-background-session-20261019/10-release-confidence-triage-20261026.md#what-e2e-08-actually-proves) |

Cancellation and sharing have no separate approved criterion in this requirement.
P3/S3 for sharing remains an analyst proposal. The user assigned P4/S4 only to the named backlog groups.
All seven acceptance criteria retain their target meaning. Deferral changes delivery scope, not intended behavior.
The record remains a candidate draft. Human publication review remains pending.
The [version 4 snapshot](../../../tasks/portal-background-session-20261019/evidence/knowledge-status-20261026/REQ-active-session-renewal-v4.md) preserves the requirement used by retained verification.

## Description

Mouse, keyboard, and scroll activity must support continued portal-session renewal.
Elapsed time alone must not require fresh authentication while eligible activity and successful renewal continue.
After inactivity expires the access token, retain renewal through the existing refresh token.
Continued eligible activity must preserve renewal across the initial refresh-token expiry.
The user confirmed this requested target on 20 October 2026.
The requested policy comes from the user's recorded replies.
It does not establish that the supplied implementation already satisfies every scenario.

## Rationale

The user requested continued renewal during eligible activity and refresh-token renewal after inactivity.
The requested behavior reduces repeated authentication during portal use.
Expired or revoked credentials cannot authorize renewal.
A valid access token can support replacement refresh credentials under the existing service contract.
Recovery without any usable credential and provider failures remain separate boundaries.
The controlled intervals below define measurable scenarios. They introduce no production timeout setting.

## Acceptance criteria

```gherkin
Scenario: AC-1
  Given a valid portal session with at least 30 seconds remaining before access expiry
  When mouse movement occurs every 100 milliseconds for 15 seconds
  Then at least one successful renewal occurs before the controlled interval ends
```

```gherkin
Scenario: AC-2
  Given a valid portal session with at least 30 seconds remaining before access expiry
  When keyboard input occurs every 100 milliseconds for 15 seconds
  Then at least one successful renewal occurs before the controlled interval ends
```

```gherkin
Scenario: AC-3
  Given a valid portal session with at least 30 seconds remaining before access expiry
  When scroll activity occurs every 100 milliseconds for 15 seconds
  Then at least one successful renewal occurs before the controlled interval ends
```

```gherkin
Scenario: AC-4
  Given successful renewal responses and accepted user activity before each access deadline
  And the initial refresh token expires within the controlled interval
  When a controlled clock advances through four hours of continued activity
  Then zero fresh SSO prompts occur solely because elapsed session time crosses an earlier maximum
```

```gherkin
Scenario: AC-5
  Given an idle-expiry prompt and a usable refresh token
  When the user selects renewal and its request remains pending
  Then the prompt has zero successful closure transitions before renewal succeeds
```

```gherkin
Scenario: AC-6
  Given an idle-expiry prompt and a usable refresh token
  When the requested renewal succeeds
  Then the prompt closes exactly once after completion
```

```gherkin
Scenario: AC-7
  Given an idle-expiry prompt and an unsuccessful refresh-based renewal request
  When the request rejects
  Then the prompt has zero successful closure transitions and permits another renewal attempt
```

The controlled intervals are test fixtures, not new business timeout limits.
No finite test proves indefinite execution.
Review the renewal path for fixed elapsed-time cutoffs and use bounded execution to test representative cycles.

Owner: unknown.
Next action: review the candidate criteria with the session owner before publication.
Implementation plans and execution results belong to the owning task.
