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

Three distinct transitions are specified in [[summaries/REQ-active-session-renewal]], within that requirement's intended scope:

- **Pending (AC-5).** When the user selects renewal and the request is still in flight, the prompt must have *zero* successful closure transitions. The prompt stays open until renewal actually completes — not when the click is registered, not when the request is dispatched.
- **Success (AC-6).** When the requested renewal succeeds, the prompt closes *exactly once*, after completion. Both halves matter: never closing and closing twice are separate bugs (double-close can double-fire downstream handlers or tear down UI twice).
- **Rejection (AC-7).** When a refresh-based renewal request rejects, the prompt has zero closure transitions *and* permits another renewal attempt. Failure is a retryable state, not a terminal one.

Together these define a prompt whose lifecycle is bound to the outcome of the renewal request rather than to the user's click.

The requirement holds the canonical measurable scenarios for these transitions. The broader authentication and sessions topic that surveys this material deliberately adds no extra scenario and no timeout setting of its own, so this page should not invent threshold values or additional cases. The criteria remain candidate intent: human publication review of both the requirement and its parent topic is still pending, so none of the three transitions should be cited as approved policy or as verified deployed behavior.

## Preconditions that keep the prompt meaningful

Recovery through the prompt assumes a usable refresh token exists. Expired or revoked credentials cannot authorize renewal, and recovery with no usable credential at all — plus identity-provider failures — sit outside this concept as separate boundaries. This is why the prompt is a *recovery* mechanism rather than a general re-authentication path: it buys time for active users whose credentials remain valid, and escalates to full authentication otherwise.

How long that precondition actually holds is unresolved. The source session designs propose incompatible refresh-token lifetimes (durations of both 105 and 225 minutes appear in the same calculation) and competing rules for whether continued activity moves the absolute-timeout anchor; one design additionally claims refresh tokens carry no absolute timeout at all. The published Entra pilot guidance describes a one-hour provider session, which does not settle the portal refresh-token lifetime. The consequence for this page is that the window during which the prompt can usefully recover a session has no authoritative bound — see [[concepts/token-lifecycle-and-timeout-policy]] for the timing question itself, which must be reconciled by the responsible owner before any value is treated as a target rule.

Interaction with the [[entities/single-ui-sdk]] and [[concepts/single-ui-sdk-authentication]] matters here, because the prompt is the visible surface of a token-refresh call whose semantics are owned lower in the stack. Cross-origin embedded applications present a further edge: activity and, by extension, renewal signals originating inside embedded frames require separate integration evidence, as noted in the requirement's review limits.

## Relationship to activity-driven renewal

The prompt only fires after inactivity has already expired the access token. The primary path — continued renewal driven by mouse, keyboard, and scroll activity — is covered in [[concepts/session-activity-renewal]]. The two mechanisms are complementary: activity renewal keeps sessions alive silently during use, while the expiry prompt handles the gap after the user steps away and comes back.

Observed defects, passing observations, and deployment state are tracked in a separate intent-to-reality gap record and do not redefine the intended behavior described here. That record compares intent against execution; this page describes only the intent.

## Design implications

- Treat prompt visibility as state derived from the renewal request's outcome, not from the click event.
- Model closure as an idempotent, single-fire transition so that success cannot close twice.
- Keep the prompt mounted and interactive after a rejection so a retry can be initiated without a full page recovery.
- Make the pending state observable, since AC-5's guarantee is precisely that nothing closes during it.
- Do not encode refresh-token or timeout durations into prompt logic while the target timing policy remains undecided; read them from configuration owned elsewhere.

## Related

- [[concepts/session-activity-renewal]]
- [[concepts/token-lifecycle-and-timeout-policy]]
- [[concepts/single-ui-sdk-authentication]]
- [[concepts/cross-application-authentication-handoff]]
- [[entities/single-ui-sdk]]
- [[entities/ratan-auth-server]]
- [[summaries/REQ-active-session-renewal]]
- [[summaries/KT-authentication-and-sessions]]
