---
type: Requirement
id: REQ-active-session-renewal
version: 2
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
- resource: git://mfe-base/src/pages/Home/common/useController.ts#L1-L31
  revision: 99b4eda666bedf06574bc48766e4efdb339f4cc7
  sha256: c27cc263a0cb6b6c1a81d0ad236d3348378c1de7c65c8a881c1b94b7c592a739
- resource: git://mfe-base/src/hooks/service/index.ts
  revision: 99b4eda666bedf06574bc48766e4efdb339f4cc7
  sha256: dad8c0cc23240d926a5e73fa83e1fc6830c8134046e59defcf61990e9b38989e
- resource: git://mfe-base/src/components/Timeout/common/useController.ts
  revision: 99b4eda666bedf06574bc48766e4efdb339f4cc7
  sha256: 97227366722ab25eb92bc07d5fa2dc16e53c85153d91869eacb9c4930cac345b
- resource: git://mfe-base/src/components/Timeout/common/useController.test.tsx
  revision: 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8
  sha256: b6f04007994e2a77f1952cb7a4829f57bb5e7e6818ca40d03b4f6f21940dae79
- resource: git://mfe-base/src/components/Timeout/common/useController.ts
  revision: 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8
  sha256: 9c9fed8b70bb8a5913210663a11974928d167b4e8676bf413483f3101db2c2b1
- resource: git://mfe-base/src/hooks/service/index.ts
  revision: 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8
  sha256: 72182d3bb36584e00982377e0137dd6effb527a4c2a24a8ffd89fcaf44b6cf13
- resource: git://mfe-base/src/hooks/service/relogin.test.ts
  revision: 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8
  sha256: 1dc0069cbac221d31af28e8ba93d34b7a46eec2876c151e5c6aba7f1cfeb52fc
- resource: git://mfe-base/src/pages/Home/common/useController.session.test.tsx
  revision: 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8
  sha256: 6e17c8889f61770d4b0f261401fbd43f1559617731a8c038d0b08da6c67698a3
- resource: git://mfe-base/src/pages/Home/common/useController.ts
  revision: 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8
  sha256: cca50a13a8bd05705127e8d25c74db57014be04068ffff59b5a7c3bd5779a272
- resource: local-review:authentication-stage-2026-10-16/mfe-session-pilot-characterization-committed-result.json
  revision: 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8
  sha256: 8ffc1eb5ebf798c9eb2793447127e852eb7dd7c2dc73749482a35311d3649fe8
generated:
  by: agent:codex
  at: '2026-10-15T14:16:21.148537+00:00'
verified: []
description: Keep active portal sessions renewable through mouse, keyboard, and scroll activity without a fixed
  reauthentication maximum.
rationale: The user requested continued renewal during active use and retained refresh-token renewal after
  inactivity.
acceptance_criteria:
- id: AC-1
  given: Given a valid portal session with at least 30 seconds remaining before access expiry
  when: When mouse movement occurs every 100 milliseconds for 15 seconds
  then: Then at least one successful renewal occurs before the controlled interval ends
  measure:
    metric: successful renewal count
    operator: at_least
    value: 1
    unit: count
- id: AC-2
  given: Given a valid portal session with at least 30 seconds remaining before access expiry
  when: When keyboard input occurs every 100 milliseconds for 15 seconds
  then: Then at least one successful renewal occurs before the controlled interval ends
  measure:
    metric: successful renewal count
    operator: at_least
    value: 1
    unit: count
- id: AC-3
  given: Given a valid portal session with at least 30 seconds remaining before access expiry
  when: When scroll activity occurs every 100 milliseconds for 15 seconds
  then: Then at least one successful renewal occurs before the controlled interval ends
  measure:
    metric: successful renewal count
    operator: at_least
    value: 1
    unit: count
- id: AC-4
  given: Given successful renewal responses and accepted user activity before each access deadline
  when: When a controlled clock advances through four hours of continued activity
  then: Then zero fresh SSO prompts occur solely because elapsed session time crosses an earlier maximum
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
  then: Then the prompt has zero successful closure transitions and permits another renewal attempt
  measure:
    metric: failed-renewal prompt closure count
    operator: equals
    value: 0
    unit: count
review_limits:
- The four-hour fixture horizon does not prove infinite execution.
- Portal-document activity is in scope. Cross-origin embedded application activity requires separate integration
  evidence.
- Environment execution and publication review remain pending.
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
implementation:
  repository_id: mfe-base
  revision: 4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8
  branch: codex/session-renewal-pilot
  controlled_source_characterization: PASSED
  jest: NOT_RUN
  browser_backend_execution: NOT_RUN
  four_hour_criterion: NOT_VERIFIED
---
# Active session renewal pilot

## Description

Mouse, keyboard, and scroll activity must support continued portal-session renewal.
Elapsed time alone must not require fresh authentication while eligible activity and successful renewal continue.
After inactivity expires the access token, retain renewal through the existing refresh token.
The requested policy comes from the user's recorded replies.
It does not establish that the supplied implementation already satisfies every scenario.

## Rationale

The [code baseline](../architecture/ARCH-authentication-runtime-baseline.md) separates implemented behavior from document proposals.
The original shell listens to mouse movement and postpones renewal until five seconds after movement stops.
It does not bind keyboard or scroll activity to that handler.
Its refresh-renewal helper starts a request without returning the promise to the prompt.
These paths supply concrete pilot targets.

The requested rule concerns eligible activity and elapsed-time reauthentication.
Invalid tokens, revoked sessions, provider failures, browser suspension, and unsupported embedded contexts remain separate conditions.
No new server timeout value or deployment configuration is introduced by this pilot.

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

AC-1 through AC-3 characterize activity handling in a controlled source-function test.
Activity checks cover each event type and continuous movement; they do not execute the exact three service/browser fixtures.
AC-5 through AC-7 characterize request completion and prompt state with controlled responses.
AC-4 requires service and browser execution, which is unavailable here.
A passing isolated characterization does not establish end-to-end behavior verification.

Owner: unknown.
Next action: review this draft and execute the service/browser scenarios in the supported environment.
Publication and recorded human approval remain pending.

[Initial implementation evidence](<../../raw/code/mfe-base/99b4eda666bedf06574bc48766e4efdb339f4cc7/src/pages/Home/common/useController.ts.L1-L31.snapshot#L1>)

[Initial implementation evidence](<../../raw/code/mfe-base/99b4eda666bedf06574bc48766e4efdb339f4cc7/src/hooks/service/index.ts.snapshot#L1>)

[Initial implementation evidence](<../../raw/code/mfe-base/99b4eda666bedf06574bc48766e4efdb339f4cc7/src/components/Timeout/common/useController.ts.snapshot#L1>)

## Isolated implementation

Pilot commit `4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8` implements the frontend changes on `codex/session-renewal-pilot`.
Document capture listeners count mouse, keyboard, and scroll activity.
They share a five-second leading throttle and read the current session state.
Idle periods create no renewal loop.
Existing near-expiry and logout guards remain in the renewal helper.

The relogin helper returns its request promise.
The prompt waits for success before closing.
Rejected renewal keeps the prompt open and resets its loading state for retry.
Its existing refresh-expiry logout deadline remains active after failure.

Twelve controlled source-function checks passed against the actual committed TypeScript.
All five executed source hashes match the pilot commit.
The harness controls React hooks, timers, document events, token decoding, and network responses.
It does not execute React, a browser, the BFF, or an identity provider.
Jest regressions were saved but not executed because the runner is absent.
The four-hour service/browser criterion remains unverified.

The isolated branch is committed without a merge or deployment.
The initial code baseline remains a separate historical revision.

[Pilot source or retained characterization](<../../raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/components/Timeout/common/useController.test.tsx.snapshot>)

[Pilot source or retained characterization](<../../raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/components/Timeout/common/useController.ts.snapshot>)

[Pilot source or retained characterization](<../../raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/hooks/service/index.ts.snapshot>)

[Pilot source or retained characterization](<../../raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/hooks/service/relogin.test.ts.snapshot>)

[Pilot source or retained characterization](<../../raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/pages/Home/common/useController.session.test.tsx.snapshot>)

[Pilot source or retained characterization](<../../raw/code/mfe-base/4c6b149a69e3bffe6e9975d65ee16ba02c1e91f8/src/pages/Home/common/useController.ts.snapshot>)

[Pilot source or retained characterization](<../../raw/execution/authentication-stage-2026-10-16/mfe-session-pilot-characterization-committed-result.json>)
