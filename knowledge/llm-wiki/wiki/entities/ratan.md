---
sources: ["summaries/KT-ces-migration-parity.md"]
type: "Organization"
description: "Legacy team and shared container whose EMS2 entity X_RATANONE maps to CES application RATAN_ENTITLEMENT_RULE (itam_id 51358)."
---

> Derived candidate/draft knowledge; publication review remains pending. [Canonical source bindings](../../source-manifest.json).

# RATAN

**Type:** Organization

## What it is

RATAN is the legacy team and display application name carried by the shared Ratan container ([[entities/mfe-ratan-container]]) and its upper applications. In the EMS2-to-CES permission migration, RATAN is the reference mapping used to clarify how legacy entity identity, CES application identity, and the legacy team label stay distinct.

## Key facts from the migration scope

The [[summaries/KT-ces-migration-parity]] document records the clarified field mapping for this organization. The table includes the existing `name` and `applicationName` fields and the new `applicationId` field. The two new fields requested by the source are `roleList` and `applicationId`; `name` and `applicationName` are retained fields.

| Field | Required value | Meaning |
| --- | --- | --- |
| `name` | `RATAN_ENTITLEMENT_RULE` | CES application/entity name corresponding to EMS2 entity `X_RATANONE` |
| `applicationName` | `RATAN` | Legacy team/display application name |
| `applicationId` | `"51358"` | Corresponding CES `itam_id` |

Additional points:

- CES `user_data.app_name` supplies the CES authorization name; it does not supply the legacy team label.
- The team label must not be replaced with the CES application name or application ID.
- `roleList` entries for a RATAN entity must come from that application's own `entitlements.entitlement_name` values, never from another application.
- These additive fields must not remove existing entity fields or change legacy EMS2 authorization decisions.

## Boundaries

- The clarified values apply to this RATAN mapping only. They do not establish team labels for other CES applications.
- The mapping does not resolve scalar role semantics, role-owned write ownership, or role-dependent caller contracts.
- The identity clarification defines target metadata; it does not establish implemented, tested, or deployed BFF behavior.

## Related pages

- [[entities/ces]] — the target authorization system and its application identity model
- [[entities/ems2]] — the legacy authorization system holding entity `X_RATANONE`
- [[entities/ems3]] — the wire value used by the CES path in the migration contract
- [[entities/single-ui-bff]] — the component expected to expose `roleList` and `applicationId`
- [[concepts/ems2-to-ces-permission-mapping]] — the entity-to-application mapping boundary
- [[concepts/ces-role-multiplicity]] — why multiple entitlement names are not one scalar role
- [[concepts/permission-check-provider-union]] — accepting grants from either provider
- [[concepts/per-tile-provider-selection]] — per-tile admission through EMS2 or CES
- [[summaries/KT-ces-migration-parity]] — source scope for these facts
- [[summaries/KT-sdk-and-entitlements]] — the related EMS2-to-CES entity-name migration intent
