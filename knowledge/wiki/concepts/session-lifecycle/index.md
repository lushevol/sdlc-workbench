# Session lifecycle

Derived navigation, 6 November 2026.
**The linked records remain candidate/draft. Human publication review and policy authority remain unresolved.**

## Identity, entry, and continued use

The authentication design separates identity-provider authentication, entitlement retrieval, and Portal session responsibilities.
The Entra UI SSO migration scope excludes EMS2 replacement and Portal session management.
An identity-provider session duration therefore does not settle the Portal refresh-token lifetime.
See [authentication responsibilities](../../../candidates/security/KT-authentication-and-sessions.md#authentication-responsibilities), candidate/draft, version 9.

The user selected denial when an authenticated SC user has no entitlement for any registered application entity.
That intended entry rule applies to local, test, UAT, and production environments.
Portal-team authority, approval, and deployed enforcement remain unconfirmed.
See the [portal-entry rule](../../../candidates/security/KT-authentication-and-sessions.md#current-user-stated-portal-entry-rule), candidate/draft, version 9.

## Requested renewal behavior

The canonical requirement makes mouse movement, keyboard input, and scrolling eligible renewal activity.
Elapsed time alone must not require fresh authentication while eligible activity and successful renewal continue.
The target includes continued renewal across the initial refresh-token expiry.
These statements describe requested target behavior rather than observed operation.
See [active renewal intent](../../../candidates/requirements/REQ-active-session-renewal.md#description), candidate/draft, version 7.

With an idle-expiry prompt and usable refresh token, manual recovery keeps the prompt open while renewal is pending.
Successful renewal closes the prompt exactly once after completion.
Rejected renewal preserves the prompt and permits another attempt under the canonical conditions.
The [measurable renewal criteria](../../../candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria) define the canonical scenarios for this candidate requirement.

The requirement does not authorize renewal with expired or revoked credentials.
Its controlled timing examples are test fixtures, without new production timeout settings.
See the [renewal rationale](../../../candidates/requirements/REQ-active-session-renewal.md#rationale) and [criterion limits](../../../candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria), candidate/draft, version 7.

## Token and permission boundaries

The SDK guides distinguish authentication tokens from entitlement tokens.
An entitlement token must not serve as a login credential.
SDK validation and entitlement retrieval do not establish application data permission enforcement.
See [entitlement retrieval](../../../candidates/security/KT-sdk-and-entitlements.md#entitlement-retrieval-and-lifecycle), candidate/draft, version 8.

This connects session continuity with [entitlement boundaries](../entitlements-and-ces-migration/index.md).
Continued login does not itself grant additional tile or application permissions.
The linked records preserve these responsibilities separately.

## Unresolved policy and evidence

Historical session designs contain conflicting refresh durations and absolute-timeout proposals.
Their examples cannot select one approved timing policy.
Entra activation grammar and persistence also need reconciliation.
See [session concepts](../../../candidates/security/KT-authentication-and-sessions.md#session-concepts-and-intended-lifecycle) and [evidence limits](../../../candidates/security/KT-authentication-and-sessions.md#evidence-limits), candidate/draft, version 9.

Session-policy ownership remains unknown; portal-team ownership is user-reported for entry policy only.
The canonical [open questions](../../../candidates/security/KT-authentication-and-sessions.md#open-questions) retain required authority and applicability review.
Implementation, execution, and rollout belong in the independent gap records linked from the requirement.
This page adds no conformance or deployment claim.

## Canonical records and related topics

| Canonical record | Version | Source state |
| --- | --- | --- |
| [KT-authentication-and-sessions](../../../candidates/security/KT-authentication-and-sessions.md) | 9 | candidate/draft |
| [REQ-active-session-renewal](../../../candidates/requirements/REQ-active-session-renewal.md) | 7 | candidate/draft |
| [KT-sdk-and-entitlements](../../../candidates/security/KT-sdk-and-entitlements.md) | 8 | candidate/draft |

Use [service responsibilities](../../entities/portal-service-responsibilities/index.md) for the reported BFF and SDK roles.
Return to the [wiki index](../../index.md).
