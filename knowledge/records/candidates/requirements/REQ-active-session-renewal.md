---
type: Requirement
id: REQ-active-session-renewal
version: 9
owner: RATAN team
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
- resource: conversation:codex/portal-knowledge-ingestion/2026-11-12/answers
  revision: sha256:b2820b053e32a9b45b44f177e539c2bfe8106c29c9b74c09c8fbd94c8e116303
  sha256: b2820b053e32a9b45b44f177e539c2bfe8106c29c9b74c09c8fbd94c8e116303
previous_version: 8
previous_content_sha256: 7d90d20b35c205940107951497b2b3a48e01d2a8f41bbf573e2ad18250f15779
generated:
  by: agent:codex
  at: '2026-11-12T16:04:45.153234+00:00'
verified: []
description: Keep active portal sessions renewable through mouse, keyboard, and scroll
  activity within the absolute session timeout. Limit idle timeout to 15 minutes and
  absolute timeout to 60 minutes.
rationale: Support renewal during active use and recovery from idle expiry within
  the session limits that the user attributed to ICS bank security policy.
acceptance_criteria:
- id: AC-1
  given: Given a valid portal session when renewal is due before access expiry and
    the absolute session deadline
  when: When eligible mouse movement continues
  then: Then at least one renewal succeeds before access expiry and the absolute
    session deadline
  measure:
    metric: successful renewal count
    operator: at_least
    value: 1
    unit: count
- id: AC-2
  given: Given a valid portal session when renewal is due before access expiry and
    the absolute session deadline
  when: When eligible keyboard input continues
  then: Then at least one renewal succeeds before access expiry and the absolute
    session deadline
  measure:
    metric: successful renewal count
    operator: at_least
    value: 1
    unit: count
- id: AC-3
  given: Given a valid portal session when renewal is due before access expiry and
    the absolute session deadline
  when: When eligible scrolling continues
  then: Then at least one renewal succeeds before access expiry and the absolute
    session deadline
  measure:
    metric: successful renewal count
    operator: at_least
    value: 1
    unit: count
- id: AC-4
  given: Given the initial refresh credential expires before the absolute session deadline
    while access remains valid through eligible activity
  when: When the user supplies eligible activity after the initial refresh credential expires
    and before the absolute session deadline
  then: Then at least one subsequent renewal succeeds within the current portal session
  measure:
    metric: successful renewal count after initial refresh credential expiry
    operator: at_least
    value: 1
    unit: count
- id: AC-5
  given: Given an idle-expiry prompt and a usable refresh token before the absolute session deadline
  when: When manual renewal begins and its request remains pending
  then: Then the prompt has zero successful closure transitions before renewal succeeds
  measure:
    metric: premature prompt closure count
    operator: equals
    value: 0
    unit: count
- id: AC-6
  given: Given an idle-expiry prompt and a usable refresh token before the absolute session deadline
  when: When the requested renewal succeeds before the absolute session deadline
  then: Then the prompt closes exactly once after completion
  measure:
    metric: successful prompt closure count
    operator: equals
    value: 1
    unit: count
- id: AC-7
  given: Given an idle-expiry prompt and a refresh-based renewal request before the absolute session deadline
  when: When the request rejects
  then: Then the prompt has zero successful closure transitions and permits another
    renewal attempt while the refresh token is usable and the absolute deadline has not passed
  measure:
    metric: failed-renewal prompt closure count
    operator: equals
    value: 0
    unit: count
- id: AC-8
  given: Given eligible activity in an active portal session with more than 15 minutes
    before its absolute deadline
  when: When 15 minutes elapse without eligible activity or manual renewal
  then: Then the portal session reaches idle expiry within 15 minutes of its last eligible activity
  measure:
    metric: inactivity duration before idle expiry
    operator: at_most
    value: 15
    unit: minutes
- id: AC-9
  given: Given a portal session kept active by eligible activity and successful renewal
  when: When the session reaches its configured absolute timeout or 60 minutes after
    portal authentication, whichever occurs first
  then: Then the expired portal session permits zero successful protected requests or renewals
  measure:
    metric: successful protected requests or renewals using the expired portal session
    operator: equals
    value: 0
    unit: count
review_limits:
- Exact timeout settings and access-token and refresh-token lifetimes remain unspecified.
- Review the applicable ICS policy revision, including whether the earlier
  refresh-based recovery after idle expiry satisfies the idle timeout rule.
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

The [12 November clarification](../../../../tasks/ui-test-coverage-20261022/evidence/portal-ingestion-answers-20261112.md#exact-user-input) sets the idle and absolute timeout ceilings.
The RATAN team owns and reviews the portal policy under ICS bank security policy.
The absolute ceiling supersedes the earlier request for renewal without a fixed elapsed-time limit.
Eligible activity and manual renewal remain in scope within the absolute limit.

Implementation, execution, rollout, backlog, and conformance belong in the independent [intent-to-reality gap record](../../../../tasks/portal-background-session-20261019/09-intent-reality-gaps.md).
The gap record contains comparisons against the earlier requirement version.
Supporting cancellation and request-sharing boundaries have no separate criterion in this requirement.

## Description

Mouse, keyboard, and scroll activity must support continued portal-session renewal.
Idle timeout must be at most 15 minutes. Absolute timeout must be at most 60 minutes from portal authentication.
Activity and renewal cannot extend the portal session beyond its absolute deadline. Continued access then requires a new authenticated portal session.
Before the absolute deadline, a usable refresh token can renew a session after idle expiry.
Within that deadline, eligible activity must support renewal across the initial refresh credential expiry while access remains valid.
Manual recovery must keep the expiry prompt open until renewal succeeds and permit retry after rejection within the applicable limits.

## Rationale

Renewal reduces repeated authentication during portal use within the session limits the user attributed to ICS bank security policy.
The ceilings bound the portal session. The exact timeout settings and individual token lifetimes remain unspecified.

The activity criteria use the session's renewal condition and credential deadlines. They define no fixed event cadence or renewal interval.

## Acceptance criteria

```gherkin
Feature: Renew portal sessions within the idle and absolute timeouts

  @AC-1
  Scenario: AC-1
    Given a valid portal session when renewal is due before access expiry and the absolute session deadline
    When eligible mouse movement continues
    Then at least one renewal succeeds before access expiry and the absolute session deadline

  @AC-2
  Scenario: AC-2
    Given a valid portal session when renewal is due before access expiry and the absolute session deadline
    When eligible keyboard input continues
    Then at least one renewal succeeds before access expiry and the absolute session deadline

  @AC-3
  Scenario: AC-3
    Given a valid portal session when renewal is due before access expiry and the absolute session deadline
    When eligible scrolling continues
    Then at least one renewal succeeds before access expiry and the absolute session deadline

  @AC-4
  Scenario: AC-4
    Given the initial refresh credential expires before the absolute session deadline while access remains valid through eligible activity
    When the user supplies eligible activity after the initial refresh credential expires and before the absolute session deadline
    Then at least one subsequent renewal succeeds within the current portal session

  @AC-5
  Scenario: AC-5
    Given an idle-expiry prompt and a usable refresh token before the absolute session deadline
    When manual renewal begins and its request remains pending
    Then the prompt has zero successful closure transitions before renewal succeeds

  @AC-6
  Scenario: AC-6
    Given an idle-expiry prompt and a usable refresh token before the absolute session deadline
    When the requested renewal succeeds before the absolute session deadline
    Then the prompt closes exactly once after completion

  @AC-7
  Scenario: AC-7
    Given an idle-expiry prompt and a refresh-based renewal request before the absolute session deadline
    When the request rejects
    Then the prompt has zero successful closure transitions and permits another renewal attempt while the refresh token is usable and the absolute deadline has not passed

  @AC-8
  Scenario: AC-8
    Given eligible activity in an active portal session with more than 15 minutes before its absolute deadline
    When 15 minutes elapse without eligible activity or manual renewal
    Then the portal session reaches idle expiry within 15 minutes of its last eligible activity

  @AC-9
  Scenario: AC-9
    Given a portal session kept active by eligible activity and successful renewal
    When the session reaches its configured absolute timeout or 60 minutes after portal authentication, whichever occurs first
    Then the expired portal session permits zero successful protected requests or renewals
```

Owner: RATAN team.
Next action: review the candidate criteria and the applicable ICS policy revision before publication.
Implementation plans, execution results, and conformance differences belong to the independent task gap record.
