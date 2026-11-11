---
type: "Concept"
sources: ["summaries/KT-authentication-and-sessions.md"]
description: "Access, refresh, and idle/absolute token timeout concepts plus the unresolved portal timing rules."
---

# Token Lifecycle and Timeout Policy

## Definition

Token lifecycle and timeout policy is the set of rules that govern how a portal issues, renews, and expires credentials during an authenticated session. It distinguishes four related but separate mechanisms: an **access token** that authenticates application requests, an **idle timeout** that limits inactivity, an **absolute timeout** that limits the interval since authentication, and a **refresh token** that permits another authentication interval without repeating the initial SSO journey.

These are documented design concepts. They are not a confirmed runtime contract, deployed behavior, or approved security policy. See [[summaries/KT-authentication-and-sessions]] for the full source topic.

## Why the distinction matters

Each mechanism answers a different question:

- Idle timeout — has the user stopped interacting?
- Absolute timeout — how long has passed since the user last proved identity?
- Refresh token — can the session continue without a full SSO round trip?
- Access token — is this specific request still authorized?

Conflating them produces policies that either expire active users or silently extend sessions past their intended bound. The [[concepts/session-activity-renewal]] requirement depends on this separation: continued eligible activity should sustain renewal across the initial refresh-token expiry, while elapsed time alone should not force re-authentication.

## Documented proposals and their conflicts

### Session version 0

- Absolute timeout below 60 minutes; idle timeout below 15 minutes.
- Examples use a 15-minute access token and a 24-hour refresh token.
- Proposes inactivity warning, session extension, single-device login, and reused-token rejection.

The strict-limit wording is ambiguous, and the examples do not resolve it.

### Session version 1

- Idle timeout proposed as `exp = iat + 15 minutes`.
- Absolute timeout tied to `auth_time` and a 60-minute `max_age` interval.
- Flow obtains a refresh token before access-token expiry, then exchanges it for another access token at a later relogin.
- Single-device login and token blacklist work are deferred to a backlog.

Version 1 contradicts itself:

1. It contains both **105-minute** and **225-minute** refresh-token durations in the same calculation.
2. Its absolute-timeout discussion proposes modifying `auth_time` during continued activity, which would defeat the purpose of an absolute bound.
3. It separately states that refresh tokens have **no absolute timeout** because they lack `auth_time` and `max_age`.

No single reliable timing rule follows from these statements without authoritative review.

## Renewal and recovery behavior

The intended target, held canonically by [[summaries/REQ-active-session-renewal]], includes continued renewal across the initial refresh-token expiry. During manual recovery:

- The expiry prompt stays open while renewal is pending.
- Successful renewal closes it exactly once.
- A rejected renewal preserves it and permits another attempt.

This behavior is described in [[concepts/session-expiry-prompt-recovery]]. The requirement owns the measurable scenarios; token policy supplies no additional scenario or timeout setting.

## Relationship to authentication and migration

[[entities/entra]] migration replaces the SSO provider but preserves separate entitlement and portal-session responsibilities. The BFF component ([[entities/single-ui-bff]]) performs the authorization-code exchange, builds user information, retrieves [[entities/ems2]] entitlements, and issues authentication and entitlement tokens.

Important boundary: the production pilot describes a **one-hour Entra provider session**. That provider-session statement does not settle portal refresh-token lifetime. The two lifetimes are governed by different layers — see [[concepts/identity-provider-delegation]] and [[concepts/cross-application-authentication-handoff]].

Phase 1 UI SSO scope explicitly excludes portal session management and EMS2 replacement.

## Machine-to-machine contrast

[[concepts/machine-to-machine-authentication]] uses client-credential flows with much longer validity. The historical [[entities/fmaa]] reference states 17-year validity for service accounts and seven-day validity for bank IDs. These historical values do **not** establish approved portal-session limits or current token policy, and copying them into target rules requires authoritative approval.

## Downstream consumers

Token lifetime and claims shape what downstream services can validate. [[concepts/single-ui-sdk-authentication]] and [[concepts/entitlement-retrieval]] describe how token validation and entitlement data reach applications. [[entities/ratan-auth-server]] supplies existing interface context, but declarations do not prove that a migration design runs in any environment. Token policy also interacts with entry decisions in [[concepts/portal-entry-and-tile-authorization]].

## Open questions

| Question | Status |
|---|---|
| Which timeout and refresh-duration rules apply per environment? | Unresolved — session designs conflict |
| Does `auth_time` change during continued activity or not? | Contradictory within version 1 |
| Is refresh-token lifetime bounded at all? | Version 1 states both bounded and unbounded |
| Which token-reuse and single-device rules are intended? | Backlogged, not decided |
| Does the one-hour Entra session constrain the portal session? | Not established |

Owner: unknown session owner. Next action: reconcile the intended timing table and token-reuse rule before policy publication.

## Evidence limits

The source documents carry local byte revisions but no confirmed original page revisions or approval authority, which limits their use as current security policy. Implementation and execution comparisons live in a separate gap record outside this concept.