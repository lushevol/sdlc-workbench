---
type: "Summary"
description: "Candidate session renewal and idle recovery within the 15-minute idle and 60-minute absolute ceilings."
doc_type: short
full_text: "sources/REQ-active-session-renewal.md"
---

> Derived from [REQ-active-session-renewal, version 9](../../../candidates/requirements/REQ-active-session-renewal.md), candidate/draft. [Source bindings](../../source-manifest.json).

# Active Session Renewal (REQ-active-session-renewal)

**Source type:** Requirement (version 9) · **Governance state:** candidate · **Status:** draft · **Owner:** RATAN team

This is a candidate requirement describing *intended target behavior* for portal session renewal. Human publication review is still pending, so the criteria express requested ideals rather than proof that the supplied implementation already conforms.

## Core intent

- Mouse, keyboard, and scroll activity must each support continued session renewal — see [[concepts/session-activity-renewal]].
- Idle timeout is at most 15 minutes. Absolute timeout is at most 60 minutes from portal authentication and applies during eligible activity and renewal.
- Within the absolute deadline, a usable refresh token can support recovery after idle expiry. Continued activity can support renewal across the initial refresh credential expiry while access remains valid.
- At the absolute deadline, the portal requires a new authenticated session.
- Manual recovery from an idle-expiry prompt must keep the prompt open until renewal succeeds, and must allow retry after a rejected request — see [[concepts/session-expiry-prompt-recovery]].

## Acceptance criteria (9 scenarios)

[Canonical acceptance criteria](../../../candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria).

| ID | Scenario | Measure |
|---|---|---|
| AC-1 | Eligible mouse movement continues when renewal is due | ≥1 successful renewal before access expiry and the absolute deadline |
| AC-2 | Eligible keyboard input continues when renewal is due | ≥1 successful renewal before access expiry and the absolute deadline |
| AC-3 | Eligible scrolling continues when renewal is due | ≥1 successful renewal before access expiry and the absolute deadline |
| AC-4 | Eligible activity after initial refresh-credential expiry and before the absolute deadline, with valid access | ≥1 subsequent renewal in the current session |
| AC-5 | Manual renewal pending before the absolute deadline | 0 premature prompt closures |
| AC-6 | Requested renewal succeeds before the absolute deadline | Exactly 1 closure, after completion |
| AC-7 | Refresh-based renewal rejects | 0 closures; retry while the token remains usable and the absolute deadline has yet to pass |
| AC-8 | No eligible activity or manual renewal | Idle expiry within 15 minutes of last eligible activity |
| AC-9 | The session reaches its absolute deadline during eligible activity | 0 successful protected requests or renewals using that expired session |

## Key distinctions and boundaries

- AC-1 through AC-3 prescribe no fixed event cadence or renewal interval. Version 9 removes unsupported timing fixtures. The 15- and 60-minute ceilings come from the 12 November clarification. The prior four-hour criterion belongs to the earlier requirement.
- Portal-document activity is in scope; activity inside cross-origin embedded applications requires **separate integration evidence**.
- Expired or revoked credentials cannot authorize renewal; recovery with no usable credential and provider failures remain separate boundaries.
- Cancellation handling and request-sharing behavior have **no approved criterion here**; their disposition belongs in the gap record.
- Implementation, rollout, backlog, and conformance evidence belong in the independent intent-to-reality gap record, which cannot modify these criteria.

## Open items

- RATAN owns and reviews the policy. Review the applicable ICS policy revision, including whether refresh-based recovery after idle expiry satisfies the idle limit. Exact settings and individual token lifetimes remain unspecified.
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
