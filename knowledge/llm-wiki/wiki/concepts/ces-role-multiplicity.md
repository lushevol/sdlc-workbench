---
type: "Concept"
sources: ["summaries/KT-ces-migration-parity.md"]
description: "CES assignments can hold multiple roles, which cannot be collapsed into one scalar role for legacy callers."
---

# CES role multiplicity and scalar role contracts

## Definition

CES role multiplicity is the condition in which a single CES assignment carries more than one entitlement (role) name. It becomes a compatibility problem when an existing upper-application contract expects exactly one role — for example, a saved view or filter that must record a single owner. CES role multiplicity must not be resolved by arbitrarily picking one name or merging several names into a scalar value.

This concept is defined in [[summaries/KT-ces-migration-parity]] as the known frontend compatibility gap of the EMS2-to-CES migration.

## Why multiplicity is not permission equivalence

A combined effective permission set is not the same thing as one assigned role. Two different entitlement definitions can produce identical combined feature/action permissions, and a set of action grants does not prove membership in a named role. Consequently:

- The distinction between **assigned roles** and **effective feature/action permissions** must be preserved.
- A caller that expects one role needs a sourced business mapping; the role must not be inferred from effective action membership.
- Equality of mapped permission meaning (see [[concepts/ems2-to-ces-permission-mapping]]) does not imply a scalar role can be derived.

## Effect on role-owned writes

CES saved-view and filter writes that require a single owner are deferred until an ownership rule is agreed. The interim rule requires:

- Zero CES role-owned write requests while the rule is unresolved.
- Zero CES roles selected as a fabricated scalar owner.
- Zero comma-joined role names submitted as a scalar owner.
- Zero changes to established EMS2 role-owned write decisions caused by the CES deferral.

Existing EMS2 role-owned write behavior is preserved unchanged. The deferral covers write ownership only; it does not define CES query visibility, role-query rules, or a multiple-role exclusion policy.

## Effect on API compatibility

Preserving upper-application APIs (see [[concepts/per-tile-provider-selection]] for the per-tile routing objective) means role-dependent callers cannot be declared compatible until their role contract is mapped. Specifically:

- An unknown role mapping cannot be satisfied by fabricating a scalar role.
- Role-dependent callers must be recorded as compatibility exceptions before affected behavior is accepted.
- The shared provider-union permission check (see [[concepts/permission-check-provider-union]]) is unaffected: it evaluates mapped feature/action grants, not role identity.

## Additive entity metadata does not resolve this

The CES entity fields `roleList` (CES `entitlements.entitlement_name` values, scoped to their corresponding application) and `applicationId` (CES `itam_id`) expose assignment names and application identity. They are additive, must not remove existing fields, and must not change EMS2 decisions. Crucially, a populated `roleList` does not establish one selected scalar role; any later scalar projection requires a separate sourced business mapping.

## Open questions

- How must multiple CES roles map to existing upper-application role contracts and role-dependent business rules?
- Which reviewed scope identifies CES-only management permissions outside the migrated business permissions?

Until these are answered, CES role-owned writes remain pending and role-dependent callers remain unresolved compatibility items.

## Related pages

- [[summaries/KT-ces-migration-parity]]
- [[concepts/ems2-to-ces-permission-mapping]]
- [[concepts/per-tile-provider-selection]]
- [[concepts/permission-check-provider-union]]
- [[concepts/application-ownership]]
- [[entities/ces]]
- [[entities/ems2]]
