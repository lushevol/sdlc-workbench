---
type: "Concept"
sources: ["summaries/REQ-active-session-renewal.md"]
description: "Mouse, keyboard, and scroll activity renew a portal session within its absolute deadline."
---

> Derived candidate/draft knowledge; publication review remains pending. [Canonical source bindings](../../source-manifest.json).

Canonical criteria: [active session renewal](../../../candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria).

# Activity-Driven Session Renewal

Pointer movement, keystrokes, and scrolling count as eligible activity for portal session renewal. The 12 November clarification sets an idle ceiling of 15 minutes and an absolute ceiling of 60 minutes from portal authentication. The absolute deadline applies during activity and renewal.

## Why it matters

Eligible activity reduces repeated sign-in within the permitted session window. The portal requires a new authenticated session at the absolute deadline.

## Mechanics

1. **Activity capture** — pointer, keyboard, and scroll events are observed in the portal document.
2. **Renewal** — eligible activity triggers renewal of the access credential before it expires, typically coalesced/throttled rather than fired per event.
3. **Idle expiry** — the session reaches idle expiry within 15 minutes of its last eligible activity.
4. **Refresh-based recovery** — before the absolute deadline, the candidate retains recovery with a usable refresh token. RATAN review needs to confirm how the applicable ICS policy treats this recovery.
5. **Renewal across initial refresh expiry** — if the initial refresh credential expires while access remains valid, eligible activity can support subsequent renewal before the absolute deadline.

## Requirements expressed in the source

The candidate requirement [[summaries/REQ-active-session-renewal]] defines nine measurable scenarios:

- Three parallel criteria assert that continuing eligible mouse (AC-1), keyboard (AC-2), and scroll (AC-3) activity each independently produce at least one successful renewal when renewal is due, before access expiry and the absolute session deadline.
- AC-4 requires at least one subsequent renewal when eligible activity continues after initial refresh expiry and before the absolute deadline, with access still valid.
- AC-5 through AC-7 govern the prompt shown after idle expiry: it must not close while a renewal request is pending, must close exactly once on success, and must remain open and retryable on rejection (see [[concepts/session-expiry-prompt-recovery]]).
- AC-8 measures the 15-minute idle ceiling. AC-9 requires zero successful protected requests or renewals using the expired session once it reaches its absolute deadline.

## Boundaries and cautions

- Version 9 prescribes no fixed activity cadence or renewal interval. The earlier timing fixtures and four-hour criterion are historical. Exact configured deadlines and individual token lifetimes remain open.
- Activity inside cross-origin embedded applications is out of scope; that requires separate integration evidence, which matters for composed portals built from independently deployed frontends.
- Expired or revoked credentials cannot authorize renewal. Recovery without a usable credential and provider outages remain outside these criteria.
- Cancellation handling and request coalescing have no approved criterion in the source requirement; their disposition belongs to an implementation gap record, not to the behavioral intent.

## Relationship to the surrounding architecture

The portal shell [[entities/mfe-base]] handles browser activity and renewal. The BFF and downstream SDK have separate responsibilities for token issuance and protected requests. See [[entities/single-ui-bff]] and [[concepts/single-ui-sdk-authentication]].

## Open questions

- What throttling or debounce policy keeps high-frequency pointer events from flooding the renewal endpoint?
- Should activity detection be shared across microfrontends so that interaction in one tile counts for the whole session?
- How should the idle-expiry prompt behave when multiple tabs or applications hold overlapping sessions?
