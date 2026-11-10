# Entitlements and CES migration

Derived navigation. Refreshed 10 November 2026.
**The linked records remain candidate/draft. Migration intent does not establish permission parity, publication approval, or deployed enforcement.**

## Separate access decisions

The documented model separates Portal entry, tile visibility and launch, and application data permissions.
The user selected the following entry and tile rules across local, test, UAT, and production environments.
Each rule retains its own conditions and approval limits.

| Decision | User-stated intended result | Canonical definition |
| --- | --- | --- |
| Portal entry | Deny an authenticated SC user without entitlement for any registered application entity. | [Entry rule](../../../candidates/security/KT-sdk-and-entitlements.md#ui-entry-ac-001) |
| Tile without an EMS2 entity | Hide the tile and deny direct launch when the tile has no configured entity. | [Empty-entity rule](../../../candidates/security/KT-sdk-and-entitlements.md#ui-empty-entity-ac-001) |
| Tile with one entity and no subject | Permit visibility and launch when entry requirements and the configured entity entitlement are satisfied. | [Empty-subject rule](../../../candidates/security/KT-sdk-and-entitlements.md#ui-empty-subject-ac-001) |

These definitions belong to [SDK and entitlements](../../../candidates/security/KT-sdk-and-entitlements.md), candidate/draft, version 8.
They do not select multiple-entity matching or application data permissions.
Portal-team ownership is user-reported for these rules; approval and enforcement remain unconfirmed.
The [onboarding clarification](../../../candidates/operations/KT-admin-and-onboarding.md#current-empty-subject-clarification), candidate/draft, version 3, preserves the single-entity scope.

## Preserve permission meaning across systems

The migration maps EMS2 roles to CES entitlements, entities to applications, subjects to features, and actions to actions.
Application scope must accompany permission comparisons.
Matching names or different numeric identifiers cannot independently establish equivalent permissions.
See [authorization mapping](../../../candidates/security/KT-ces-migration-parity.md#mapping-between-authorization-concepts), candidate/draft, version 6.

The user separately confirms EMS2 `X_RATANONE` corresponds to CES `RATAN_ENTITLEMENT_RULE`.
This name correspondence does not establish equal role definitions, identifiers, or deployed assignments.
See the [name-migration clarification](../../../candidates/security/KT-sdk-and-entitlements.md#user-confirmed-ems2-to-ces-name-migration), candidate/draft, version 8.

## Compare definitions, assignments, and effective access

Entitlement completeness and account permission completeness have separate denominators.
The account comparison includes every discovered account within the selected entity scope.
Combined effective permissions cannot establish equal entitlement definitions or assignments.
Matching data-profile names cannot establish equivalent data restrictions.
See [entitlement preservation](../../../candidates/security/KT-ces-migration-parity.md#entitlement-preservation) and [account preservation](../../../candidates/security/KT-ces-migration-parity.md#account-permission-preservation), candidate/draft, version 6.

Fully matched content remains in coverage totals and leaves the active difference list.
Missing, additional, unresolved, and unavailable comparisons remain visible.
FMO Portal Admin has a separate, lower-priority non-production comparison.
Its content must stay outside production comparison denominators under the dated clarification.
See [coverage handling](../../../candidates/security/KT-ces-migration-parity.md#coverage-and-active-differences) and [FMO exception](../../../candidates/security/KT-ces-migration-parity.md#fmo-scope-exception), candidate/draft, version 6.

## Independent tile admission and shared permission checks

Preserve existing base and shared-container caller contracts within reviewed mappings.
Each tile selects its admission provider independently and retains its application scope.
An EMS2 tile keeps its established admission rules. A CES tile uses its configured CES application and permission structure.
One tile's migration requires no provider change on other tiles.
See [frontend compatibility](../../../candidates/security/KT-ces-migration-parity.md#frontend-compatibility-and-per-tile-migration) and [tile selection](../../../candidates/security/KT-ces-migration-parity.md#independent-tile-provider-selection), candidate/draft, version 6.

The shared `hasPermission(code)` check accepts a mapped grant from EMS2 or CES.
Reviewed application, feature, and action mappings must define the requested permission.
The caller supplies no additional scope argument.
Each accepted decision requires a log identifying at least one provider that supplied a matching grant.
If neither provider supplies a matching grant, the result is false.

That denial case requires no accepted-grant log.
See [FE-COMPAT-AC-004](../../../candidates/security/KT-ces-migration-parity.md#fe-compat-ac-004), candidate/draft, version 6.

The shared check does not replace the tile's provider-specific admission decision.
Neither combined effective permissions nor provider selection establishes one assigned CES role.
See [provider boundaries](../../../candidates/security/KT-ces-migration-parity.md#independent-tile-provider-selection), candidate/draft, version 6.

## CES entity metadata and role-owned writes

The BFF adds `roleList` from the corresponding application's CES `entitlements.entitlement_name` values.
It adds `applicationId` from that application's CES `itam_id`.
The role list must exclude names taken solely from another application.
Retain existing entity fields and EMS2 authorization behavior.
See [CES entity fields](../../../candidates/security/KT-ces-migration-parity.md#ces-entity-role-and-application-fields), candidate/draft, version 6.

For the clarified RATAN mapping, retain these field meanings.

| Field | Intended value | Meaning |
| --- | --- | --- |
| `name` | `RATAN_ENTITLEMENT_RULE` | CES authorization name corresponding to EMS2 `X_RATANONE`. |
| `applicationName` | `RATAN` | Legacy team/display label. |
| `applicationId` | `"51358"` | Corresponding CES `itam_id`. |

These values define this RATAN mapping. They do not establish labels for other CES applications.
See [BFF-ENTITY-AC-002](../../../candidates/security/KT-ces-migration-parity.md#bff-entity-ac-002), candidate/draft, version 6.

CES saved-view and filter writes remain unavailable when they need one owner role without an agreed ownership rule.
Do not select a primary CES role or submit comma-joined role names as a scalar owner.
Preserve existing EMS2 role-owned write behavior.
This interim rule leaves CES query visibility, role-query rules, and multiple-role exclusion policy undefined.
See [role-owned writes](../../../candidates/security/KT-ces-migration-parity.md#interim-rule-for-ces-role-owned-writes), candidate/draft, version 6.

## SDK compatibility target and open policy

SDK version `3.0.0` must preserve the old permission contract where supported CES evidence permits.
The caller supplies the FMAA bearer token; the SDK must make no independent token-acquisition request.
Unsupported attribution or unmapped meaning remains a compatibility gap.
The user has not selected a failure-handling policy.
See [SDK migration intent](../../../candidates/security/KT-sdk-and-entitlements.md#sdk-300-ces-migration-intent), candidate/draft, version 8.

Legacy data-restriction definitions and CES-only management-grant scope remain unresolved.
Multiple-role caller contracts and complete upper-application API mappings also remain unresolved.
Owners are unknown. Bind authoritative definitions and reviewed mappings before accepting the affected behavior.
See the [migration questions](../../../candidates/security/KT-ces-migration-parity.md#open-questions), candidate/draft, version 6.

The frontend clarifications define intended behavior. They do not establish complete API compatibility, deployed metadata, or collected provider logs.
See [migration evidence limits](../../../candidates/security/KT-ces-migration-parity.md#evidence-limits), candidate/draft, version 6.

## Canonical records and related topics

| Canonical record | Version | Source state |
| --- | --- | --- |
| [KT-sdk-and-entitlements](../../../candidates/security/KT-sdk-and-entitlements.md) | 8 | candidate/draft |
| [KT-ces-migration-parity](../../../candidates/security/KT-ces-migration-parity.md) | 6 | candidate/draft |
| [KT-admin-and-onboarding](../../../candidates/operations/KT-admin-and-onboarding.md) | 3 | candidate/draft |

Continue with [session lifecycle](../session-lifecycle/index.md) or [administration and release](../admin-onboarding-and-release/index.md).
Return to the [wiki index](../../index.md).
