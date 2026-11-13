---
type: "Concept"
sources: ["summaries/KT-authentication-and-sessions.md"]
description: "Portal idle and absolute ceilings, individual credential lifetimes, and historical timing proposals."
---

> Derived candidate/draft knowledge; publication review remains pending. [Canonical source bindings](../../source-manifest.json).

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

Conflating them produces policies that either expire active users or silently extend sessions past their intended bound. The [[concepts/session-activity-renewal]] requirement depends on this separation: eligible activity supports renewal within the absolute deadline, including across initial refresh expiry while access remains valid.

## Current session ceilings

The user attributed two ceilings to ICS bank security policy: at most 15 minutes idle and at most 60 minutes absolute from portal authentication. The absolute limit applies during eligible activity and renewal. RATAN owns and reviews portal policy. The [current requirement](../../../records/candidates/requirements/REQ-active-session-renewal.md#intended-scope) records the source and the remaining review limits.

## Historical proposals and their conflicts

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

These historical conflicts leave individual token lifetimes and configuration details open.

## Renewal and recovery behavior

The intended target, held canonically by [[summaries/REQ-active-session-renewal]], supports continued renewal across the initial refresh-token expiry while access remains valid and before the absolute deadline. During manual recovery within that deadline:

- The expiry prompt stays open while renewal is pending.
- Successful renewal closes it exactly once.
- A rejected renewal preserves it and permits another attempt.

This behavior is described in [[concepts/session-expiry-prompt-recovery]]. The requirement defines the measurable idle and absolute expiry criteria.

## Relationship to authentication and migration

[[entities/entra]] migration replaces the SSO provider but preserves separate entitlement and portal-session responsibilities. The BFF component ([[entities/single-ui-bff]]) performs the authorization-code exchange, builds user information, retrieves [[entities/ems2]] entitlements, and issues authentication and entitlement tokens.

Important boundary: the production pilot describes a **one-hour Entra provider session**. That provider-session statement does not settle portal refresh-token lifetime. The two lifetimes are governed by different layers — see [[concepts/identity-provider-delegation]] and [[concepts/cross-application-authentication-handoff]].

Phase 1 UI SSO scope explicitly excludes portal session management and EMS2 replacement.

## Machine-to-machine contrast

The historical [[concepts/machine-to-machine-authentication]] reference describes client-credential flows and gives validity examples longer than the portal session ceilings. The [[entities/fmaa]] reference states 17-year validity for service accounts and seven-day validity for bank IDs. These historical values do **not** establish credential-rotation rules, approved portal-session limits or current token policy, and copying them into target rules requires authoritative approval.

## Downstream consumers

Token lifetime and claims shape what downstream services can validate. [[concepts/single-ui-sdk-authentication]] and [[concepts/entitlement-retrieval]] describe how token validation and entitlement data reach applications. [[entities/ratan-auth-server]] supplies existing interface context, but declarations do not prove that a migration design runs in any environment. Token policy also interacts with entry decisions in [[concepts/portal-entry-and-tile-authorization]].

## Open questions

| Question | Status |
|---|---|
| Which exact timeout settings and token lifetimes apply by environment? | Open within the stated ceilings |
| Which ICS policy revision governs the limits and idle recovery? | Pending RATAN review |
| Which token-reuse and single-device rules are intended? | Backlogged, not decided |
| Does the one-hour Entra session constrain the portal session? | Not established |

Owner: RATAN team for portal policy. Review the applicable ICS revision and the environment-specific settings before publication.

## Evidence limits

The source documents carry local byte revisions but no confirmed original page revisions or approval authority, which limits their use as current security policy. Implementation and execution comparisons live in a separate gap record outside this concept.
