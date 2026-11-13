---
type: "Summary"
description: "RATAN policy ownership, Entra sign-in, session ceilings, and the ideal portal logout boundary."
doc_type: short
full_text: "sources/KT-authentication-and-sessions.md"
---

> Derived from [KT-authentication-and-sessions, version 10](../../../records/candidates/security/KT-authentication-and-sessions.md), candidate/draft. [Source bindings](../../source-manifest.json).

# Authentication and sessions

## Overview
This candidate topic consolidates portal user authentication, session design, and Entra migration materials. It separates user-stated intent from source proposals and historical evidence, and it does not establish deployed behavior, approved security policy, or approval authority. Its main contribution is a structured map of authentication and session responsibilities, plus the gaps that block policy publication. The target portal authenticates users, obtains entitlements, and issues tokens for application requests.

## Portal entry and entitlements
- User-stated intent: an authenticated SC user with no entitlement for any registered application entity must be denied portal entry in local, test, UAT, and production. The [[entities/portal-team]] is named as owner only by user report; authority and approval are unconfirmed. The answer defines no HTTP status, denial wording, or entity-versus-role semantics.
- Draft principles state the same denial direction. An older tile-security proposal instead permits SC entry; it remains conflicting historical evidence, not selected intent.
- Separate user-stated rules: deny tiles without a configured [[entities/ems2]] entity; allow tile visibility and launch through the empty-subject rule when one EMS2 entity is configured and zero subjects are configured, owned by the [[entities/portal-team]] across the same environments.

Links: [[concepts/portal-entry-and-tile-authorization]], [[concepts/ems2-entitlement-provisioning]], [[summaries/KT-sdk-and-entitlements]].

## Intended session renewal
The RATAN team owns and reviews portal policy under ICS bank security policy. The user set ceilings of 15 minutes idle and 60 minutes absolute from portal authentication. Eligible mouse, keyboard, and scroll activity supports renewal within the absolute deadline, including across initial refresh credential expiry while access remains valid. At the deadline, further access requires a new authenticated portal session. Before the deadline, the prior idle-prompt recovery keeps the prompt open while renewal is pending, closes it once after success, and permits another eligible attempt after rejection.

The ideal logout target immediately revokes all of the user's portal sessions. Protected actions and renewals using those sessions should fail after logout completes. Entra and other identity-provider sessions are outside that revocation scope. The [logout criterion](../../../records/candidates/security/KT-authentication-and-sessions.md#portal-logout-ac-001) remains a candidate for RATAN review.

Links: [[concepts/session-activity-renewal]], [[concepts/session-expiry-prompt-recovery]], [[summaries/REQ-active-session-renewal]].

## Authentication responsibilities and Entra migration
- Entra design: browser redirect, authorization-code exchange through the [[entities/single-ui-bff]]; the BFF builds user information, retrieves [[entities/ems2]] entitlements, and issues authentication and entitlement tokens. The historical design retained OneMFA fallback and described a separate username/password path. The current production target prohibits OneMFA fallback. [Sign-in criterion](../../../records/candidates/security/KT-authentication-and-sessions.md#portal-sso-ac-001).
- Phase 1 covers UI SSO only. It excludes EMS2 replacement, portal session management, and tenant-onboarding authentication. Machine-to-machine authentication has a separate migration document with unresolved central dependencies.
- Non-production verification requires a development AD account, Authenticator registration, and RATAN AD-group membership; it checks successful login, user information, and expected tile visibility. The FAQ ties missing entitlements to tile access and EMS2 configuration.
- The production pilot describes Windows Hello or Authenticator login and a one-hour [[entities/entra]] session; that provider session does not settle the portal refresh-token lifetime. It also warns that AD profile values differ from OUD values: surname formatting, country codes, and missing locale values can affect downstream audit or application logic.

Links: [[concepts/identity-provider-delegation]], [[entities/entra]], [[concepts/identity-profile-attribute-migration]].

## Session concepts and historical timing proposals
The source distinguishes an access token for application requests, an idle timeout for inactivity, an absolute timeout since authentication, and a refresh token for another authentication interval without repeating the initial SSO journey. These are documented concepts, not a confirmed runtime contract.
- Session version 0 states limits below 60 minutes for absolute timeout and below 15 minutes for idle timeout. Its examples use a 15-minute access token and a 24-hour refresh token. It proposes an inactivity warning, session extension, single-device login, and reused-token rejection.
- Session version 1 proposes `exp = iat + 15 minutes` for idle timeout, ties absolute timeout to `auth_time` and a 60-minute `max_age`, obtains a refresh token before access-token expiry, and exchanges it at a later relogin. Single-device login and token blacklist work sit on a backlog.
- Version 1 conflicts with itself: it contains both 105-minute and 225-minute refresh-token durations, proposes changing `auth_time` during continued activity, and also says refresh tokens have no absolute timeout because they lack `auth_time` and `max_age`. These competing durations are historical proposals. The latest clarification sets the two session ceilings and leaves individual token lifetimes open.

Links: [[concepts/token-lifecycle-and-timeout-policy]], [[concepts/session-activity-renewal]].

## Historical machine-to-machine authentication
The historical [[entities/fmaa]] reference describes client-credential authentication for machine-to-machine callers, separates service-account onboarding from bank-ID onboarding, and describes OUD-managed accounts authenticated through FMAA. It states 17-year validity for service accounts and seven-day validity for bank IDs. These historical values do not establish approved portal-session limits or current token policy.

Links: [[concepts/machine-to-machine-authentication]].

## Evidence limits and open questions
The 12 November answer assigns policy ownership to RATAN. The applicable ICS revision and environment-specific timeout and token values require review. Open questions include authorization to initiate logout when the access token has already expired, the intended profile contract, and the applicability of historical FMAA flows. Retained sources supply no deployed enforcement or publication decision.

Links: [[entities/portal-team]], [[concepts/token-lifecycle-and-timeout-policy]].

## Connections
[[summaries/KT-sdk-and-entitlements]] covers downstream token validation and entitlement responsibilities. [[summaries/KT-admin-and-onboarding]] connects tenant setup with role and tile configuration. [[summaries/KT-frontend-composition]] explains the UI context for login and user state. Registry capability `single-ui-authentication` and contract `single-ui-sso-token-family` provide existing interface context for [[entities/single-ui-bff]] and [[entities/mfe-base]], but these declarations do not prove that a migration design runs in any environment.

## Related Concepts
- [[concepts/single-ui-sdk-authentication]]
- [[concepts/entitlement-retrieval]]
- [[concepts/cross-application-authentication-handoff]]
- [[concepts/application-ownership]]
- [[concepts/tenant-production-readiness]]

## Entities
- [[entities/ratan-auth-server]]
- [[entities/fmo-post-trade-portal]]
- [[entities/single-ui-sdk]]
- [[entities/admin-module]]
