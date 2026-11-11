---
type: "Concept"
sources: ["summaries/KT-ces-migration-parity.md"]
description: "Each portal tile selects EMS2 or CES entitlement admission independently, without forcing other tiles to migrate."
---

# Per-tile entitlement provider selection

## Definition

Per-tile provider selection is the migration rule that each tile in the portal chooses its own entitlement provider — legacy EMS2 or CES — and that choice governs only that tile's admission logic. Moving one tile to CES must not force unrelated tiles to change provider, rewrite their admission code, or alter their caller contracts.

This rule comes from the CES migration parity knowledge topic, recorded as user intent in the 6 November 2026 frontend clarification and the 9 November 2026 provider clarification. See [[summaries/KT-ces-migration-parity]].

## Why it matters

The EMS2-to-CES migration is a change of authorization concept (role → entitlement, entity → application, subject → feature), not a single cutover event. A big-bang migration would require every tile, every shared container API, and every upper application to be compatible at the same moment. Per-tile selection reduces that risk by allowing incremental, independently reversible migration.

## How selection works

| Tile selection | Admission behavior |
| --- | --- |
| EMS2 | Retains its existing EMS2 admission rules unchanged |
| CES | Uses CES admission logic, the configured CES application identity, and the CES permission structure |

Within the CES path, the CES application acts as the new entity identity for that selected scope. Application scope must be preserved in both provider paths — a grant from an unrelated application never admits a tile.

The migration contract uses `EMS3` as the CES wire value. In source material, the phrase `EMS2 (CES)` denotes the CES path; plain `EMS2` denotes the legacy path. These two admission choices remain distinct and are not merged.

## Separation from the shared permission check

Tile admission is not the same as the shared functional permission check. The latest provider clarification permits an existing `hasPermission(code)` call to be satisfied by a mapped grant from *either* provider, with a log identifying the supplying provider. That union check is a cross-cutting rule and does not override per-tile admission selection. See [[concepts/permission-check-provider-union]].

## Role multiplicity stays separate

A CES tile may receive multiple role assignments. This is a compatibility concern distinct from provider selection and from mapped feature/action permission meaning. Multiple roles must not be collapsed into one proven assigned role, and a caller expecting a single role needs a sourced business mapping. See [[concepts/ces-role-multiplicity]].

## Acceptance criteria

**FE-COMPAT-AC-002** — two tiles, one on EMS2 and one on CES, each admit through their selected provider with zero admissions based only on an unrelated application's grant.

**FE-COMPAT-AC-003** — when one declared tile switches from EMS2 to CES:

- the number of provider selections changed on other tiles equals 0;
- the number of upper-application permission call signatures changed solely by the switch equals 0;
- multiple role assignments are not represented as one proven assigned role.

Record compatibility exceptions before accepting affected caller behavior. Acceptance of role-dependent callers requires the unresolved role mapping.

## Limits

The criteria define target behavior, not passing execution. They do not establish complete API compatibility, deployed behavior, or a resolved scalar role policy. The value "two" in the admission criterion describes the comparison case and does not cap the supported tile population.

## Related pages

- [[summaries/KT-ces-migration-parity]]
- [[concepts/permission-check-provider-union]]
- [[concepts/ces-role-multiplicity]]
- [[concepts/ems2-to-ces-permission-mapping]]
- [[concepts/portal-entry-and-tile-authorization]]
- [[entities/ems2]]
- [[entities/ces]]
- [[entities/ems3]]
- [[entities/mfe-base]]
- [[entities/mfe-ratan-container]]
