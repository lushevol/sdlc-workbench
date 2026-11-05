# CES migration permission preservation

Derived navigation. Source state: candidate/draft. This page grants no approval.

[Wiki index](../../index.md)

Canonical record: [KT-ces-migration-parity, version 1](../../../candidates/security/KT-ces-migration-parity.md#L2-L7).

## Summary

The candidate defines intended permission preservation between EMS2 production and CES UAT.
It separates mapped entitlement completeness from account permission completeness and retains the FMO scope exception.
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

## Unresolved questions

- Which authoritative source defines legacy data field and value restrictions?
- Which CES-only management grants fall outside the migrated business scope?

See the canonical [open questions](../../../candidates/security/KT-ces-migration-parity.md#open-questions).
Owner: unknown. Next action: bind legacy restrictions and additional grants to reviewed scope definitions.

## Connections

- [SDK and entitlements](../KT-sdk-and-entitlements/index.md)
- [Canonical migration connections](../../../candidates/security/KT-ces-migration-parity.md#connections)

The source's [evidence limits](../../../candidates/security/KT-ces-migration-parity.md#evidence-limits) preserve the distinction between expected parity and completed verification.
