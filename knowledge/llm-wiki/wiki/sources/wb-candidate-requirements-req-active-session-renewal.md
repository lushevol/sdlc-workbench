---
title: "Active session renewal"
type: source
tags: []
sources: []
source_file: raw/workbench/knowledge/candidates/requirements/REQ-active-session-renewal.md
source: raw/workbench/knowledge/candidates/requirements/REQ-active-session-renewal.md
source_hash: 773d38682e922289
last_updated: 2026-11-11
candidate_id: REQ-active-session-renewal
candidate_version: 7
candidate_governance_state: candidate
candidate_status: draft
candidate_classification: 
workbench_origin: knowledge/candidates/requirements/REQ-active-session-renewal.md
workbench_sha256: 773d38682e922289f8241512f7ed3819313d0da17d51671c143ca292842711e3
workbench_status: candidate-derived
---

# Active session renewal

**Status: candidate requirement for intended target behavior. Human publication review remains pending.**

## Intended scope

These criteria define the requested ideal session behavior.
Mouse, keyboard, and scroll activity must support continued renewal without an elapsed-time-only authentication maximum.
Manual recovery must keep the expiry prompt open until renewal succeeds and permit retry after rejection.
The recorded user replies supply intent. Their exact source identities are listed above.

Implementation, execution, rollout, backlog, and conformance belong in the independent [intent-to-reality gap record](../../../../tasks/portal-background-session-20261019/09-intent-reality-gaps.md).
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
