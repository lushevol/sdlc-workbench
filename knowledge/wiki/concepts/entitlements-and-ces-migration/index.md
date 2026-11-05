# Entitlements and CES migration

Derived navigation, 6 November 2026.
**The linked records remain candidate/draft. Migration intent does not establish permission parity, publication approval, or deployed enforcement.**

## Separate access decisions

The documented model separates Portal entry, tile visibility and launch, and application data permissions.
The user selected the following entry and tile rules across local, test, UAT, and production environments.
Each rule retains its own conditions and approval limits.

| Decision | User-stated intended result | Canonical definition |
| --- | --- | --- |
| Portal entry | Deny an authenticated SC user without entitlement for any registered application entity. | [Entry rule](../../../candidates/security/KT-sdk-and-entitlements.md#ui-entry-ac-001) |
| Tile without an EMS2 entity | Hide the tile and deny direct launch until an entity is configured. | [Empty-entity rule](../../../candidates/security/KT-sdk-and-entitlements.md#ui-empty-entity-ac-001) |
| Tile with one entity and no subject | Permit visibility and launch when entry requirements and the configured entity entitlement are satisfied. | [Empty-subject rule](../../../candidates/security/KT-sdk-and-entitlements.md#ui-empty-subject-ac-001) |

These definitions belong to [SDK and entitlements](../../../candidates/security/KT-sdk-and-entitlements.md), candidate/draft, version 8.
They do not select multiple-entity matching or application data permissions.
Portal-team ownership is user-reported for these rules; approval and enforcement remain unconfirmed.
The [onboarding clarification](../../../candidates/operations/KT-admin-and-onboarding.md#current-empty-subject-clarification), candidate/draft, version 3, preserves the single-entity scope.

## Preserve permission meaning across systems

The migration maps EMS2 roles to CES entitlements, entities to applications, subjects to features, and actions to actions.
Application scope must accompany permission comparisons.
Matching names or different numeric identifiers cannot independently establish equivalent permissions.
See [authorization mapping](../../../candidates/security/KT-ces-migration-parity.md#mapping-between-authorization-concepts), candidate/draft, version 1.

The user separately confirms EMS2 `X_RATANONE` corresponds to CES `RATAN_ENTITLEMENT_RULE`.
This name correspondence does not establish equal role definitions, identifiers, or deployed assignments.
See the [name-migration clarification](../../../candidates/security/KT-sdk-and-entitlements.md#user-confirmed-ems2-to-ces-name-migration), candidate/draft, version 8.

## Compare definitions, assignments, and effective access

Entitlement completeness and account permission completeness have separate denominators.
The account comparison includes every discovered account within the selected entity scope.
Combined effective permissions cannot establish equal entitlement definitions or assignments.
Matching data-profile names cannot establish equivalent data restrictions.
See [entitlement preservation](../../../candidates/security/KT-ces-migration-parity.md#entitlement-preservation) and [account preservation](../../../candidates/security/KT-ces-migration-parity.md#account-permission-preservation), candidate/draft, version 1.

Fully matched content remains in coverage totals and leaves the active difference list.
Missing, additional, unresolved, and unavailable comparisons remain visible.
FMO Portal Admin has a separate, lower-priority non-production comparison.
Its content must stay outside production comparison denominators under the dated clarification.
See [coverage handling](../../../candidates/security/KT-ces-migration-parity.md#coverage-and-active-differences) and [FMO exception](../../../candidates/security/KT-ces-migration-parity.md#fmo-scope-exception), candidate/draft, version 1.

## SDK compatibility target and open policy

SDK version `3.0.0` must preserve the old permission contract where supported CES evidence permits.
The caller supplies the FMAA bearer token; the SDK must make no independent token-acquisition request.
Unsupported attribution or unmapped meaning remains a compatibility gap.
The user has not selected a failure-handling policy.
See [SDK migration intent](../../../candidates/security/KT-sdk-and-entitlements.md#sdk-300-ces-migration-intent), candidate/draft, version 8.

Legacy data-restriction definitions and CES-only management-grant scope remain unresolved.
Owners are unknown; the next action is to bind authoritative definitions and reviewed comparison scope.
See the [migration questions](../../../candidates/security/KT-ces-migration-parity.md#open-questions), candidate/draft, version 1.

## Canonical records and related topics

| Canonical record | Version | Source state |
| --- | --- | --- |
| [KT-sdk-and-entitlements](../../../candidates/security/KT-sdk-and-entitlements.md) | 8 | candidate/draft |
| [KT-ces-migration-parity](../../../candidates/security/KT-ces-migration-parity.md) | 1 | candidate/draft |
| [KT-admin-and-onboarding](../../../candidates/operations/KT-admin-and-onboarding.md) | 3 | candidate/draft |

Continue with [session lifecycle](../session-lifecycle/index.md) or [administration and release](../admin-onboarding-and-release/index.md).
Return to the [wiki index](../../index.md).
