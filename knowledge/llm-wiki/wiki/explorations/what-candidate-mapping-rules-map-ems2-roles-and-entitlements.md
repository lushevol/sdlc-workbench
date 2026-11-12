---
query: "What candidate mapping rules map EMS2 roles and entitlements to CES permissions, and what parity limits remain unresolved?"
---

> Review qualification, 12 November 2026: Only `roleList` and `applicationId` are new additive fields. `name` and `applicationName` are existing fields retained with the clarified CES authorization name and legacy team/display label. Apply this qualification to the additive-fields sentence in the saved synthesis below. [Current canonical entity-field meanings](../../../candidates/security/KT-ces-migration-parity.md#ces-entity-role-and-application-fields).


> Derived candidate/draft knowledge; publication review remains pending. [Canonical source bindings](../../source-manifest.json).

## Candidate EMS2 → CES mapping rules

Per [[summaries/KT-ces-migration-parity]] (a `candidate` draft recording user-stated intent, not verified execution) and [[concepts/ems2-to-ces-permission-mapping]], the concept mapping is:

| EMS2 concept | CES concept | Comparison boundary |
| --- | --- | --- |
| Role | Entitlement | Compare the mapped definition **and** its assigned accounts |
| Entity | Application | Preserve application scope when comparing permission names |
| Subject | Feature | Compare through an explicit feature mapping |
| Action | Action | Compare the permitted operation within the mapped feature |

Supporting rules:
- **Names are not proof of equivalence** — a name shared across different applications does not establish equal permission; numeric source identifiers may differ without changing mapped meaning.
- **Parity is definitional, not aggregate** — equal combined effective permissions do not prove equal definitions or assignments, so comparison must occur at each mapped application/entitlement/feature/action relationship. Catalog totals are not completeness evidence.
- **Account-level parity** — include every account in the selected entity scope, expand multi-ID cells (each distinct account counted once), retain application/entitlement scope, and compare data restrictions via authoritative definitions and resolved values (not profile names alone).
- **Coverage accounting** — matched content moves into coverage totals; missing, additional, unresolved, and unavailable comparisons stay visible (an unavailable comparison proves neither equality nor missing permissions). FMO Portal Admin is excluded from production scope (see [[entities/fmo-post-trade-portal]]).
- **Provider selection is orthogonal** — mapping defines meaning; each tile independently selects EMS2 or CES ([[concepts/per-tile-provider-selection]]), with the CES path carrying wire value `EMS3`.
- **Provider-union hasPermission** — existing `hasPermission(code)` calls accept a matching grant from either provider, log the supplying provider, and add no caller arguments ([[concepts/permission-check-provider-union]]).
- **Additive CES entity fields** expose the mapping without changing EMS2 decisions: `roleList`, `applicationId` (e.g. `"51358"`), `name` (`RATAN_ENTITLEMENT_RULE`), `applicationName` (`RATAN`) — see [[entities/ratan]].

## Unresolved parity limits

The source records **intent and comparison scope only** — it does not prove completed migration, deployed permission equality, implemented BFF behavior, or log collection, and no human review is recorded. The specific open gaps:

1. **Role multiplicity / scalar role contracts** — CES assignments can hold multiple roles that must not be collapsed into one scalar role or inferred from effective action membership. Callers expecting a scalar role need a sourced business mapping; until then, **CES role-owned writes (saved views, filters) stay deferred** while EMS2 write behavior is preserved ([[concepts/ces-role-multiplicity]]). Acceptance criterion FE-ROLE-WRITE-AC-001 requires zero fabricated scalar owners.
2. **Authoritative data-field/value restrictions** — no source defines the complete legacy data field and value restrictions per profile.
3. **CES-only management permissions** — no reviewed scope covers CES-only management permissions that fall outside migrated business permissions.
4. **Upper-application API mappings** — no approved mappings yet cover each upper-application API and its CES permission inputs (FE-COMPAT-AC-001/002/003 remain targets, not proven results).
5. **Provider-union implementation** — the rule does not merge legacy EMS2 and CES tile admission choices, does not resolve saved-item ownership, and its expectation about returned legacy entities remains an implementation question ([[concepts/permission-check-provider-union]]).

In short: the mapping vocabulary and comparison boundaries are defined as candidate intent, but the **scalar-role/role-owned-write gap** is the central unresolved parity limit, alongside missing authoritative data-restriction sources, CES-only permission scope, and per-API CES mappings.
