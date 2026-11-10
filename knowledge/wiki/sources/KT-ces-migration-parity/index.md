# CES migration permission preservation

Derived navigation. Source state: candidate/draft. This page grants no approval.

[Wiki index](../../index.md)

Canonical record: [KT-ces-migration-parity, version 6](../../../candidates/security/KT-ces-migration-parity.md#L2-L7).

## Summary

The candidate defines intended permission preservation between EMS2 production and CES UAT.
It separates mapped entitlement completeness from account permission completeness and retains the FMO scope exception.
It also defines frontend compatibility, provider selection, shared permission checks, and additive CES entity metadata.
See the canonical [scope](../../../candidates/security/KT-ces-migration-parity.md#scope) and [summary](../../../candidates/security/KT-ces-migration-parity.md#summary).

## Key rules and qualifiers

- The mapping connects role to entitlement, entity to application, subject to feature, and action to action.
  Shared names or differing numeric IDs alone do not establish permission equivalence.
  See [authorization concepts](../../../candidates/security/KT-ces-migration-parity.md#mapping-between-authorization-concepts).
- Compare mapped definitions and assignments separately from combined effective permissions.
  Equal combined permissions do not establish equal entitlement definitions.
  See [entitlement preservation](../../../candidates/security/KT-ces-migration-parity.md#entitlement-preservation).
- Include all scoped accounts and count each distinct account once overall.
  Data-profile names alone do not establish equal data restrictions.
  See [account preservation](../../../candidates/security/KT-ces-migration-parity.md#account-permission-preservation).
- Count matched content in coverage while retaining missing, additional, unresolved, and unavailable comparisons separately.
  See [coverage and active differences](../../../candidates/security/KT-ces-migration-parity.md#coverage-and-active-differences).
- FMO Portal Admin remains outside the production comparison, with separate lower-priority non-production coverage.
  See the [FMO exception](../../../candidates/security/KT-ces-migration-parity.md#fmo-scope-exception).

- Preserve existing upper-application APIs within reviewed mappings while migrating tile admission providers independently.
  Keep assigned roles separate from combined effective permissions.
  See [frontend compatibility](../../../candidates/security/KT-ces-migration-parity.md#frontend-compatibility-and-per-tile-migration).
- Keep tile admission specific to its selected provider and application.
  Shared `hasPermission(code)` checks accept mapped EMS2 or CES grants without an additional caller argument.
  Accepted decisions require a log identifying at least one provider that supplied a matching grant.
  The denial case requires no accepted-grant log.
  See [provider selection](../../../candidates/security/KT-ces-migration-parity.md#independent-tile-provider-selection) and [FE-COMPAT-AC-004](../../../candidates/security/KT-ces-migration-parity.md#fe-compat-ac-004).
- Keep CES saved-view and filter writes unavailable when they require an unresolved owner role.
  Do not select a primary role or submit comma-joined roles as one owner.
  Preserve existing EMS2 role-owned writes. CES query visibility and exclusion rules remain undefined.
  See the [interim write rule](../../../candidates/security/KT-ces-migration-parity.md#interim-rule-for-ces-role-owned-writes).
- Add application-scoped `roleList` entitlement names and `applicationId` from the corresponding CES `itam_id`.
  Keep the CES authorization `name` separate from the legacy team label in `applicationName`.
  These fields do not select a scalar role.
  See [CES entity fields](../../../candidates/security/KT-ces-migration-parity.md#ces-entity-role-and-application-fields).

## Unresolved questions

- Which authoritative source defines legacy data field and value restrictions?
- Which CES-only management grants fall outside the migrated business scope?
- How must multiple CES roles map to existing caller role contracts?
- Which reviewed application, feature, action, and caller mappings support each upper-application API?

See the canonical [open questions](../../../candidates/security/KT-ces-migration-parity.md#open-questions).
Owner: unknown. Bind authoritative restrictions, reviewed grant scope, and each affected caller contract before acceptance.

## Connections

- [SDK and entitlements](../KT-sdk-and-entitlements/index.md)
- [Entitlements and CES migration](../../concepts/entitlements-and-ces-migration/index.md)
- [Canonical migration connections](../../../candidates/security/KT-ces-migration-parity.md#connections)

The source's [evidence limits](../../../candidates/security/KT-ces-migration-parity.md#evidence-limits) preserve the distinction between expected parity and completed verification.
