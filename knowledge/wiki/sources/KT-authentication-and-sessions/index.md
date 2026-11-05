# Authentication and sessions

Derived navigation. Source state: candidate/draft. This page grants no approval.

[Wiki index](../../index.md)

Canonical record: [KT-authentication-and-sessions, version 9](../../../candidates/security/KT-authentication-and-sessions.md#L2-L7).

## Summary

The candidate separates portal authentication, intended session renewal, and Entra migration responsibilities.
Historical session proposals retain unresolved timing and activation rules.
See the canonical [scope](../../../candidates/security/KT-authentication-and-sessions.md#scope) and [summary](../../../candidates/security/KT-authentication-and-sessions.md#summary).

## Key rules and qualifiers

- Eligible activity must support continued renewal. Manual recovery preserves the prompt until success and permits retry after rejection.
  See [intended session renewal](../../../candidates/security/KT-authentication-and-sessions.md#intended-session-renewal).
- User-stated intent denies entry without entitlement for any registered application entity across local, test, UAT, and production.
  Authority, approval, and enforcement remain separate.
  See the [portal-entry rule](../../../candidates/security/KT-authentication-and-sessions.md#current-user-stated-portal-entry-rule).
- A tile without a configured EMS2 entity has a separate user-stated denial rule.
  See the [empty-entity connection](../../../candidates/security/KT-authentication-and-sessions.md#L196-L197).
- Empty-subject visibility and launch depend on the separately defined single-entity rule.
  See the [empty-subject connection](../../../candidates/security/KT-authentication-and-sessions.md#L199-L201).
- The Entra phase-one scope separates UI SSO from EMS2 replacement, portal session management, and service-account migration.
  See [authentication responsibilities](../../../candidates/security/KT-authentication-and-sessions.md#authentication-responsibilities).

## Unresolved questions

- What evidence confirms portal-team authority and approval for the user-stated entry policy?
  Owner: portal team, user-reported for that policy only.
- Which intended timeout and refresh-duration rules apply in each supported environment?
- Which activation grammar, persistence rule, provider scope, and fallback boundaries have authoritative approval?

See the canonical [open questions](../../../candidates/security/KT-authentication-and-sessions.md#open-questions) and [activation limits](../../../candidates/security/KT-authentication-and-sessions.md#L297-L303).
Other owners remain unknown. Next action: obtain policy and migration decisions without treating historical examples as accepted limits.

## Connections

- [Active session renewal](../REQ-active-session-renewal/index.md)
- [SDK and entitlements](../KT-sdk-and-entitlements/index.md)
- [Administration and onboarding](../KT-admin-and-onboarding/index.md)

The canonical [renewal section](../../../candidates/security/KT-authentication-and-sessions.md#intended-session-renewal) and [connections](../../../candidates/security/KT-authentication-and-sessions.md#connections) define these relationships.
