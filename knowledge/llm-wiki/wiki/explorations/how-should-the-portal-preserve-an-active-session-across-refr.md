---
query: "How should the Portal preserve an active session across refresh-token expiry, and what manual recovery is required after a rejected renewal?"
---

## Preserving an active session across refresh-token expiry

The candidate requirement `REQ-active-session-renewal` defines the intended target: an active session should be sustained by **activity-driven renewal** rather than a fixed elapsed-time reauthentication cap.

- **Eligible activity renews the session.** Mouse movement (AC-1), keyboard input (AC-2), and scroll activity (AC-3) must each independently produce at least one successful renewal — see [[concepts/session-activity-renewal]].
- **Elapsed time alone must never force re-login.** AC-4 requires that a controlled clock advancing through four hours of continued activity — *explicitly including the point where the initial refresh token expires* — yields **zero** SSO prompts caused solely by elapsed time.
- **Surviving refresh-token expiry requires rotation.** As [[concepts/session-activity-renewal]] puts it, a design that renews only the access token but never rotates the long-lived credential "still hits a hard wall at the refresh token's expiry." Successful renewals must therefore mint replacement refresh credentials under the service contract.
- **After idle expiry, recovery uses the existing refresh token** rather than a full SSO round trip.

Caveats: the 100 ms / 15 s / four-hour figures are **test fixtures, not production timeout settings**, and a finite test horizon does not prove indefinite execution. Activity inside cross-origin embedded applications is out of scope and needs separate integration evidence. Expired or revoked credentials cannot authorize renewal — that is a separate boundary handled by the identity provider. See [[concepts/token-lifecycle-and-timeout-policy]].

## Manual recovery after a rejected renewal

The expiry prompt shown at idle expiry must bind its lifecycle to the **outcome of the renewal request**, not to the user's click ([[concepts/session-expiry-prompt-recovery]]):

- **Pending (AC-5):** zero premature prompt closures while the request is in flight — the prompt stays open until renewal actually completes.
- **Success (AC-6):** exactly one closure, after completion (never closing and closing twice are separate bugs).
- **Rejection (AC-7):** **zero closures, and another attempt is permitted.** Failure is a retryable state, not a terminal one — the prompt stays mounted and interactive so a retry can be initiated without a full page recovery.

Design implications: model closure as idempotent and single-fire, make the pending state observable, and don't hard-code refresh-token or timeout durations into prompt logic while the timing policy is undecided — read them from configuration owned elsewhere.

## Governance status

These are **candidate intent**, not approved policy or verified deployed behavior: the requirement is at version 7, status *draft*, owner `unknown`, with human publication review pending ([[summaries/REQ-active-session-renewal]]). The underlying timing rules are themselves unresolved — session version 1 contains both 105- and 225-minute refresh-token durations, contradictory `auth_time` handling, and states both that refresh tokens are bounded and unbounded ([[concepts/token-lifecycle-and-timeout-policy]]). The one-hour Entra provider session in the production pilot does not settle the portal refresh-token lifetime.
