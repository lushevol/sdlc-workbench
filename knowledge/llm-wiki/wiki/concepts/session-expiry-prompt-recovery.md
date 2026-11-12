---
type: "Concept"
sources: ["summaries/KT-authentication-and-sessions.md", "summaries/REQ-active-session-renewal.md"]
description: "How the expiry prompt behaves across pending, success, and rejection renewal states."
---

> Derived candidate/draft knowledge; publication review remains pending. [Canonical source bindings](../../source-manifest.json).

Canonical criteria: [pending, successful and rejected renewal outcomes](../../../candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria).

# Session Expiry Prompt and Recovery

When a portal session reaches idle expiry, the user is shown a prompt offering renewal. This concept covers how that prompt should behave across the three states of a renewal attempt: pending, succeeded, and rejected. It is the recovery-facing half of session handling, complementing the activity-facing behavior described in [[concepts/session-activity-renewal]].

## The problem it addresses

A renewal prompt is a small piece of UI with outsized consequences. If it closes before renewal actually succeeds, the user is dropped into an unauthenticated state with no obvious path back. If it refuses to close after a successful renewal, it blocks the user behind a stale modal. If it locks up after a failed request, the user has no way to retry. Each failure mode is a different defect, so each needs its own measurable criterion rather than a single vague "prompt works" expectation.

## Required behavior

Three transitions in [[summaries/REQ-active-session-renewal]] apply before the session's absolute deadline:

- **Pending (AC-5).** When the user selects renewal and the request is still in flight, the prompt must have *zero* successful closure transitions. The prompt stays open until renewal actually completes — not when the click is registered, not when the request is dispatched.
- **Success (AC-6).** When the requested renewal succeeds, the prompt closes *exactly once*, after completion. Both halves matter: never closing and closing twice are separate bugs (double-close can double-fire downstream handlers or tear down UI twice).
- **Rejection (AC-7).** When a refresh-based renewal request rejects, the prompt has zero closure transitions *and* permits another renewal attempt. The user can retry while the refresh token remains usable and the absolute deadline has yet to pass.

Together these define a prompt whose lifecycle is bound to the outcome of the renewal request rather than to the user's click.

The [canonical criteria](../../../candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria) define the measurable outcomes. Both the requirement and its parent topic remain candidate drafts for RATAN review.

## Preconditions that keep the prompt meaningful

Recovery through the prompt assumes a usable refresh token exists. Expired or revoked credentials cannot authorize renewal, and recovery with no usable credential at all — plus identity-provider failures — sit outside this concept as separate boundaries. This is why the prompt is a *recovery* mechanism rather than a general re-authentication path: it buys time for active users whose credentials remain valid, and escalates to full authentication otherwise.

The 12 November clarification caps the portal session at 60 minutes from authentication, including during manual renewal. The historical session designs propose different refresh-token lifetimes, and the Entra provider session has its own lifetime. The exact token settings and whether refresh-based recovery after idle expiry satisfies ICS require RATAN review. See [[concepts/token-lifecycle-and-timeout-policy]].

Interaction with the [[entities/single-ui-sdk]] and [[concepts/single-ui-sdk-authentication]] matters here, because the prompt is the visible surface of a token-refresh call whose semantics are owned lower in the stack. Cross-origin embedded applications present a further edge: activity and, by extension, renewal signals originating inside embedded frames require separate integration evidence, as noted in the requirement's review limits.

## Relationship to activity-driven renewal

The criteria apply when the portal presents an eligible idle-expiry prompt. The relationship between idle expiry and the access token's lifetime depends on the applicable settings. [[concepts/session-activity-renewal]] describes renewal during continued use.

Observed defects, passing observations, and deployment state are tracked in a separate intent-to-reality gap record and do not redefine the intended behavior described here. That record compares intent against execution; this page describes only the intent.

## Design implications

- Treat prompt visibility as state derived from the renewal request's outcome, not from the click event.
- Model closure as an idempotent, single-fire transition so that success cannot close twice.
- Keep the prompt mounted and interactive after a rejection so a retry can be initiated without a full page recovery.
- Make the pending state observable, since AC-5's guarantee is precisely that nothing closes during it.
- Respect the applicable session deadline and credential validity when presenting the recovery action.

## Related

- [[concepts/session-activity-renewal]]
- [[concepts/token-lifecycle-and-timeout-policy]]
- [[concepts/single-ui-sdk-authentication]]
- [[concepts/cross-application-authentication-handoff]]
- [[entities/single-ui-sdk]]
- [[entities/ratan-auth-server]]
- [[summaries/REQ-active-session-renewal]]
- [[summaries/KT-authentication-and-sessions]]
