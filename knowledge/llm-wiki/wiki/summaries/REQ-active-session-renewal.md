---
type: "Summary"
description: "Candidate requirement for renewable portal sessions via activity, plus expiry-prompt recovery criteria."
doc_type: short
full_text: "sources/REQ-active-session-renewal.md"
---

> Derived from [REQ-active-session-renewal, version 7](../../../candidates/requirements/REQ-active-session-renewal.md), candidate/draft. [Source bindings](../../source-manifest.json).

# Active Session Renewal (REQ-active-session-renewal)

**Source type:** Requirement (version 7) · **Governance state:** candidate · **Status:** draft · **Owner:** unknown

This is a candidate requirement describing *intended target behavior* for portal session renewal. Human publication review is still pending, so the criteria express requested ideals rather than proof that the supplied implementation already conforms.

## Core intent

- Mouse, keyboard, and scroll activity must each support continued session renewal — see [[concepts/session-activity-renewal]].
- Elapsed time alone must never force a fresh authentication (no fixed reauthentication maximum).
- After inactivity expires the access token, renewal remains possible through the existing refresh token.
- Continued eligible activity must preserve renewal across the initial refresh-token expiry.
- Manual recovery from an idle-expiry prompt must keep the prompt open until renewal succeeds, and must allow retry after a rejected request — see [[concepts/session-expiry-prompt-recovery]].

## Acceptance criteria (7 scenarios)

| ID | Scenario | Measure |
|---|---|---|
| AC-1 | Mouse movement every 100 ms for 15 s, ≥30 s of access time remaining | ≥1 successful renewal |
| AC-2 | Keyboard input every 100 ms for 15 s, ≥30 s remaining | ≥1 successful renewal |
| AC-3 | Scroll activity every 100 ms for 15 s, ≥30 s remaining | ≥1 successful renewal |
| AC-4 | Controlled clock advances through 4 hours of continued activity, including initial refresh-token expiry | 0 elapsed-time-only SSO prompts |
| AC-5 | Renewal selected from idle prompt, request pending | 0 premature prompt closures |
| AC-6 | Requested renewal succeeds | Exactly 1 closure, after completion |
| AC-7 | Refresh-based renewal rejects | 0 closures; another attempt permitted |

## Key distinctions and boundaries

- The controlled intervals (100 ms activity, 15 s observation, 4 h fixture) are **test fixtures, not production timeout settings**.
- A finite four-hour test horizon does not prove indefinite execution.
- Portal-document activity is in scope; activity inside cross-origin embedded applications requires **separate integration evidence**.
- Expired or revoked credentials cannot authorize renewal; recovery with no usable credential and provider failures remain separate boundaries.
- Cancellation handling and request-sharing behavior have **no approved criterion here**; their disposition belongs in the gap record.
- Implementation, rollout, backlog, and conformance evidence belong in the independent intent-to-reality gap record, which cannot modify these criteria.

## Open items

- Owner still `unknown`; next action is review with the session owner before publication.
- ASD-STE100 automated check passed, but the human ASD review is pending.

## Related topics for synthesis

- [[concepts/session-activity-renewal]] — activity-driven token refresh versus elapsed-time session caps.
- [[concepts/session-expiry-prompt-recovery]] — prompt lifecycle, pending-state handling, and retry semantics.
- Acceptance criteria — expressing requirements as measurable Gherkin scenarios.
- Intent-to-reality gap record — separating desired behavior from implementation conformance.
- Refresh-token lifecycle — credential expiry and renewal eligibility.

## Related Concepts
- [[concepts/cross-application-authentication-handoff]]
- [[concepts/single-ui-sdk-authentication]]
- [[concepts/identity-provider-delegation]]
- [[concepts/portal-entry-and-tile-authorization]]

## Entities
- [[entities/fmo-post-trade-portal]]
- [[entities/mfe-base]]
- [[entities/single-ui-bff]]
- [[entities/single-ui-sdk]]
- [[entities/entra]]
- [[entities/ratan-auth-server]]
