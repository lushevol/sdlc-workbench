---
type: "Concept"
sources: ["summaries/REQ-active-session-renewal.md"]
description: "Session lifetime extended by mouse, keyboard, and scroll activity instead of a fixed elapsed-time reauthentication maximum."
---

> Derived candidate/draft knowledge; publication review remains pending. [Canonical source bindings](../../source-manifest.json).

Canonical criteria: [active session renewal](../../../candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria).

# Activity-Driven Session Renewal

Activity-driven session renewal is a session-management policy in which a user's continued interaction with an application — pointer movement, keystrokes, and scrolling — is treated as evidence of an active session, and that evidence is used to keep renewing the session's credentials. The defining contrast is with **elapsed-time session caps**: fixed maximum lifetimes after which a user must re-authenticate no matter how actively they are working. Under an activity-driven policy, time alone is not a reason to force a fresh login; only genuine inactivity or credential failure is.

## Why it matters

Portal users work in long, uninterrupted stretches. A time-based maximum produces disruptive reauthentication in the middle of that work, while adding little security value if the session is continuously proven active. Activity-driven renewal reduces repeated sign-in while preserving the protective value of an idle timeout.

## Mechanics

1. **Activity capture** — pointer, keyboard, and scroll events are observed in the portal document.
2. **Renewal** — eligible activity triggers renewal of the access credential before it expires, typically coalesced/throttled rather than fired per event.
3. **Idle expiry** — if no activity occurs, the access token expires and the session no longer authorizes requests.
4. **Refresh-based recovery** — after idle expiry, an existing refresh token can still restore the session, so the user is not sent through full SSO again.
5. **Refresh-token rotation** — continued activity must also survive the expiry of the *initial* refresh token, which is only possible if successful renewals themselves mint replacement refresh credentials under the service contract.

Step 5 is the subtle one: a design that renews the access token but never rotates the long-lived credential still hits a hard wall at the refresh token's expiry.

## Requirements expressed in the source

The candidate requirement [[summaries/REQ-active-session-renewal]] turns this policy into seven measurable scenarios:

- Three parallel criteria assert that mouse (AC-1), keyboard (AC-2), and scroll (AC-3) activity each independently produce at least one successful renewal within a controlled 15-second observation window with 100 ms event spacing.
- AC-4 asserts that a controlled clock advancing through four hours of continued activity yields **zero** SSO prompts caused solely by elapsed time — explicitly including the point where the initial refresh token expires.
- AC-5 through AC-7 govern the prompt shown after idle expiry: it must not close while a renewal request is pending, must close exactly once on success, and must remain open and retryable on rejection (see [[concepts/session-expiry-prompt-recovery]]).

## Boundaries and cautions

- The 100 ms / 15 s / four-hour figures are **test fixtures, not production timeout settings**. No finite test proves indefinite execution.
- Activity inside cross-origin embedded applications is out of scope; that requires separate integration evidence, which matters for composed portals built from independently deployed frontends.
- Expired or revoked credentials cannot authorize renewal. Recovery with no usable credential, and provider outages, are separate failure domains handled by the identity provider — see [[concepts/identity-provider-delegation]] and [[concepts/cross-application-authentication-handoff]].
- Cancellation handling and request coalescing have no approved criterion in the source requirement; their disposition belongs to an implementation gap record, not to the behavioral intent.

## Relationship to the surrounding architecture

In this portal the renewal path sits with the authentication SDK and the auth server rather than with individual feature applications: [[entities/single-ui-sdk]] mediates session state in the browser, backed by the [[entities/ratan-auth-server]] and, upstream, the enterprise identity provider. Broader context on the SDK model is in [[concepts/single-ui-sdk-authentication]].

## Open questions

- What throttling or debounce policy keeps high-frequency pointer events from flooding the renewal endpoint?
- Should activity detection be shared across microfrontends so that interaction in one tile counts for the whole session?
- How should the idle-expiry prompt behave when multiple tabs or applications hold overlapping sessions?