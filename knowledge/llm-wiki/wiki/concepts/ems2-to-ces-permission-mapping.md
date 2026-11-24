---
type: "Concept"
sources: ["summaries/KT-ces-migration-parity.md"]
description: "How EMS2 roles, entities, subjects, and actions map to CES entitlements, applications, features, and actions with parity rules."
---

> Derived candidate/draft knowledge; publication review remains pending. [Canonical source bindings](../../source-manifest.json).

Canonical basis: [authorization mapping](../../../records/candidates/security/KT-ces-migration-parity.md#mapping-between-authorization-concepts) and [frontend compatibility criteria](../../../records/candidates/security/KT-ces-migration-parity.md#intended-frontend-acceptance-criteria).

# EMS2 to CES Permission Mapping and Parity

## Definition

The migration from EMS2 to CES changes the authorization model vocabulary. Parity means that after concepts are mapped, permission *meaning* is preserved for every scoped account — not merely that catalog totals happen to match. This page defines the concept mapping, the comparison boundaries that make parity testable, and the known gaps.

See [[summaries/KT-ces-migration-parity]] for the source intent and acceptance criteria.

## Concept mapping

| EMS2 concept | CES concept | Required comparison boundary |
| --- | --- | --- |
| Role | Entitlement | Compare the mapped definition and its assigned accounts. |
| Entity | Application | Preserve application scope when comparing permission names. |
| Subject | Feature | Compare each subject through its explicit feature mapping. |
| Action | Action | Compare the permitted operation within the mapped feature. |

Two rules follow directly:

- Names shared by different applications do **not** establish equivalent permissions.
- Numeric source identifiers may differ without changing mapped permission meaning.

This mapping is distinct from the earlier entity-name intent (EMS2 `X_RATANONE` → CES `RATAN_ENTITLEMENT_RULE`), which retains its own source and scope. See [[summaries/KT-sdk-and-entitlements]].

## Parity is definitional, not aggregate

Different entitlements can produce the same combined effective permissions. That combined result does not prove equal entitlement definitions or assignments. Parity therefore requires comparison at each mapped application, entitlement, feature, and action relationship — catalog totals are not evidence of completeness.

Entitlement provisioning side: [[concepts/ems2-entitlement-provisioning]]. Retrieval side: [[concepts/entitlement-retrieval]].

## Account-level parity

- Compare all accounts discovered within the selected entity scope; two supplied examples do not bound the population.
- Expand cells or response collections containing several account IDs and count each distinct account once in the denominator.
- Retain application and entitlement scope when comparing assignments and effective permissions.
- Compare data restrictions through authoritative definitions and resolved values; a matching data-profile *name* alone proves nothing.

## Coverage accounting

Fully matched migrated content moves into coverage totals and leaves the active difference list. Missing content, additional content, unresolved mappings, and unavailable comparisons stay visible. An unavailable comparison establishes neither equality nor missing permissions — the expected population must remain visible.

### FMO scope exception

FMO Portal Admin sits outside the production migration comparison. Its non-production comparison is kept separate and lower priority, and must not enter production coverage denominators. Any future production scope requires a sourced update. See [[entities/fmo-post-trade-portal]].

## Provider selection is orthogonal to mapping

Mapping defines meaning; provider selection defines which system is consulted. Each tile selects its provider independently — an EMS2 tile keeps its admission logic, a CES tile uses CES identity and permission structure. In the wire contract, the CES path carries the value `EMS3`.

See [[concepts/per-tile-provider-selection]] and [[concepts/portal-entry-and-tile-authorization]].

## Permission checks across the union

Existing `hasPermission(code)` calls may accept a mapped grant from **either** provider, with the supplying provider logged and no new caller argument. This shared functional check is separate from tile admission. See [[concepts/permission-check-provider-union]].

## Role multiplicity — the known compatibility gap

CES assignments may carry multiple roles. A combined effective permission set must not be treated as one assigned role, and a named role must not be inferred from effective action membership. Callers expecting a scalar role need a sourced business mapping; until then, CES role-owned writes (saved views, filters) stay deferred while EMS2 write behavior is preserved. See [[concepts/ces-role-multiplicity]] and [[concepts/application-ownership]].

## Entity metadata that carries the mapping

Two new EMS3 entity fields, `roleList` and `applicationId`, expose CES assignment names and identity without changing EMS2 behavior. The table also includes the clarified values of the existing `name` and `applicationName` fields; those existing fields are retained.

| Field | Value in the RATAN case | Meaning |
| --- | --- | --- |
| `roleList` | CES `entitlements.entitlement_name` values | Application-scoped assignment names |
| `applicationId` | `"51358"` | CES application `itam_id` |
| `name` | `RATAN_ENTITLEMENT_RULE` | CES application/entity name for `X_RATANONE` |
| `applicationName` | `RATAN` | Legacy team/display label |

CES `user_data.app_name` supplies the CES authorization name, not the legacy team label. The additions must remove no existing fields and change no EMS2 decisions. See [[entities/ratan]], [[entities/mfe-ratan-container]], [[entities/mfe-base]], [[entities/single-ui-bff]].

## Open questions

1. Which authoritative source defines the complete legacy data field and value restrictions per profile?
2. Which reviewed scope covers CES-only management permissions outside migrated business permissions?
3. How must multiple CES roles map to existing caller role contracts?
4. Which approved mappings cover each upper-application API and its CES permission inputs?

## Related

- [[summaries/KT-ces-migration-parity]]
- [[concepts/per-tile-provider-selection]]
- [[concepts/permission-check-provider-union]]
- [[concepts/ces-role-multiplicity]]
- [[concepts/ems2-entitlement-provisioning]]
- [[concepts/entitlement-retrieval]]
- [[entities/ems2]] · [[entities/ces]] · [[entities/ems3]]
