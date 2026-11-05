# SDK and entitlements

Derived navigation. Source state: candidate/draft. This page grants no approval.

[Wiki index](../../index.md)

Canonical record: [KT-sdk-and-entitlements, version 8](../../../candidates/security/KT-sdk-and-entitlements.md#L2-L7).

## Summary

The candidate separates authentication-token validation, entitlement retrieval, tile eligibility, and application data permissions.
It records the SDK 3.0.0 compatibility objective and user-confirmed EMS2-to-CES name correspondence.
See the canonical [summary](../../../candidates/security/KT-sdk-and-entitlements.md#summary), [migration intent](../../../candidates/security/KT-sdk-and-entitlements.md#sdk-300-ces-migration-intent), and [name mapping](../../../candidates/security/KT-sdk-and-entitlements.md#user-confirmed-ems2-to-ces-name-migration).

## Key rules and qualifiers

- Authentication and entitlement tokens serve different purposes. Entitlement tokens must not authenticate or log in users.
  See [entitlement retrieval](../../../candidates/security/KT-sdk-and-entitlements.md#entitlement-retrieval-and-lifecycle).
- SDK 3.0.0 must preserve supported legacy permission meaning without missing or unsupported additional role-scoped grants.
  See [SDK-CES-INTENT-AC-001](../../../candidates/security/KT-sdk-and-entitlements.md#sdk-ces-intent-ac-001).
- The caller supplies the FMAA token; the SDK must make zero independent token-acquisition requests for that criterion.
  See [SDK-CES-INTENT-AC-002](../../../candidates/security/KT-sdk-and-entitlements.md#sdk-ces-intent-ac-002).
- `X_RATANONE` corresponds to `RATAN_ENTITLEMENT_RULE` within the clarified migration scope.
  This correspondence does not establish numeric identifier or role equivalence.
  See the [name migration](../../../candidates/security/KT-sdk-and-entitlements.md#user-confirmed-ems2-to-ces-name-migration).
- User-stated entry, empty-entity, and empty-subject criteria retain separate conditions and pending approval.
  See [UI-ENTRY-AC-001](../../../candidates/security/KT-sdk-and-entitlements.md#ui-entry-ac-001), [UI-EMPTY-ENTITY-AC-001](../../../candidates/security/KT-sdk-and-entitlements.md#ui-empty-entity-ac-001), and [UI-EMPTY-SUBJECT-AC-001](../../../candidates/security/KT-sdk-and-entitlements.md#ui-empty-subject-ac-001).
- Tile visibility does not establish permission to read or modify application data.
  The proposal assigns those permissions to each application.
  See [responsibility boundaries](../../../candidates/security/KT-sdk-and-entitlements.md#integration-purpose-and-responsibility-boundary).

## Unresolved questions

- Which supported CES data preserves each legacy role-scoped grant, and which failure contract should callers use?
  See [canonical questions](../../../candidates/security/KT-sdk-and-entitlements.md#L146-L147).
- Which trusted control replaces JWT validation on excluded paths or skip headers?
- How do applications invalidate cached entitlements and reject logged-out sessions across instances?

See the canonical [open questions](../../../candidates/security/KT-sdk-and-entitlements.md#open-questions).
Owner: unknown for these questions. Next action: establish supported mappings, caller contracts, and application-specific controls.

## Connections

- [Authentication and sessions](../KT-authentication-and-sessions/index.md)
- [Administration and onboarding](../KT-admin-and-onboarding/index.md)
- [CES migration parity](../KT-ces-migration-parity/index.md)

The canonical [connections](../../../candidates/security/KT-sdk-and-entitlements.md#connections) and [parity connection](../../../candidates/security/KT-ces-migration-parity.md#connections) define these relationships.
