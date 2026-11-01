---
type: Requirement
id: REQ-active-session-renewal
version: 7
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
- resource: conversation:workbench:knowledge-intent-boundary-20261101
  revision: user-clarification-20261101-1
  sha256: e720c3f1d5b817526a5d3f7e984d59234241b69e3c8ade22ce3f8b13ea7fe22b
previous_version: 6
previous_content_sha256: 8df3874875f2d2352d09f3c5c91da0c12c9041ac5d6f50a992570b021076a767
generated:
  by: agent:codex
  at: '2026-11-01T15:27:12.559701+00:00'
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
- Human publication review remains pending.
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

**Status: candidate requirement for intended target behavior. Human publication review remains pending.**

## Intended scope

These criteria define the requested ideal session behavior.
Mouse, keyboard, and scroll activity must support continued renewal without an elapsed-time-only authentication maximum.
Manual recovery must keep the expiry prompt open until renewal succeeds and permit retry after rejection.
The recorded user replies supply intent. Their exact source identities are listed above.

Implementation, execution, rollout, backlog, and conformance belong in the independent [intent-to-reality gap record](../../../tasks/portal-background-session-20261019/09-intent-reality-gaps.md).
Those records do not change these seven criteria or approve a substitute behavior.
Supporting cancellation and request-sharing boundaries have no separate approved criterion in this requirement.
Their operational disposition belongs in the gap record.

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
Implementation plans, execution results, and conformance differences belong to the independent task gap record.
