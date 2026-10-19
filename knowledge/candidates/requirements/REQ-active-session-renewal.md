---
type: Requirement
id: REQ-active-session-renewal
version: 3
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
generated:
  by: agent:codex
  at: '2026-10-19T17:31:38.280427+00:00'
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
    access deadline
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

## Description

Mouse, keyboard, and scroll activity must support continued portal-session renewal.
Elapsed time alone must not require fresh authentication while eligible activity and successful renewal continue.
After inactivity expires the access token, retain renewal through the existing refresh token.
The requested policy comes from the user's recorded replies.
It does not establish that the supplied implementation already satisfies every scenario.

## Rationale

The user requested continued renewal during eligible activity and refresh-token renewal after inactivity.
The requested behavior reduces repeated authentication during portal use.
Invalid tokens, revoked sessions, provider failures, and browser suspension require separate policy decisions.
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
