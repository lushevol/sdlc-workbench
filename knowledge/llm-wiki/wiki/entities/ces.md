---
sources: ["summaries/KT-ces-migration-parity.md", "summaries/KT-architecture-evolution.md", "summaries/KT-sdk-and-entitlements.md"]
type: "Product"
description: "Successor entitlement service to EMS2, supplying CES roles and application identity to consumers."
---

# CES (Central Entitlement Service)

## What it is

CES is the entitlement service that supplies role-scoped permission data to downstream applications. In the material summarized in [[summaries/KT-sdk-and-entitlements]], CES appears as the successor system to [[entities/ems2]] for entitlement retrieval, and as the data source that the [[entities/single-ui-sdk]] must read during its planned 3.0.0 release. In [[summaries/KT-ces-migration-parity]] it is the target of the EMS2 production to CES UAT permission-preservation comparison.

The documents do not describe CES deployment topology, ownership, or operational interfaces beyond its role as a permission source and migration target.

## Key facts from these documents

### Name migration from EMS2

The user confirms that EMS2 entity `X_RATANONE` was renamed to CES application `RATAN_ENTITLEMENT_RULE` during migration. The confirming clarification is dated 30 October 2026.

This statement resolves the name correspondence for that migration scope only. It does not establish:

- equivalent entity, application, subject, or role numeric identifiers;
- role equivalence between the two systems;
- deployment status or publication approval.

The companion field mapping separates these names from each system's identifier structures. Retaining that distinction matters when mapping consumers and permission definitions. See [[concepts/ems2-to-ces-permission-mapping]].

### Application identity and entity fields

The migration-parity material requires two new fields on EMS3 entities served to upper applications: `roleList` carries the corresponding CES `entitlements.entitlement_name` values, and `applicationId` carries the CES application `itam_id`. For the RATAN mapping the requested example value is `51358`.

For that mapping, the new `applicationId` field and the retained `name` and `applicationName` fields have three distinct meanings. The retained fields are not additional new fields:

| Field | Value | Meaning |
| --- | --- | --- |
| `name` | `RATAN_ENTITLEMENT_RULE` | CES application/entity name for EMS2 `X_RATANONE` |
| `applicationName` | `RATAN` | Legacy team/display label, not the CES app name |
| `applicationId` | `"51358"` | Corresponding CES `itam_id` |

CES `user_data.app_name` supplies the CES authorization name, not the legacy team label. The role list must stay bound to its own application; entitlement names from another application may not populate it. These additive fields expose assignment names and application identity but do not resolve scalar role semantics.

### Migration parity scope and concept mapping

The intended migration preserves permission meaning after EMS2 and CES concepts are mapped:

| EMS2 concept | CES concept |
| --- | --- |
| Role | Entitlement |
| Entity | Application |
| Subject | Feature |
| Action | Action |

Shared permission names across different applications do not establish equivalent permissions, and numeric source identifiers can differ without changing mapped meaning. Entitlement completeness is assessed separately from account permission completeness. Different entitlements can produce the same combined effective permissions without proving equal definitions or assignments. Account comparisons must cover every account in the selected entity scope, with application, entitlement, and applicable data restrictions compared through authoritative definitions rather than profile names alone.

FMO Portal Admin is excluded from the production comparison and tracked as separate, lower-priority non-production content that must not enter production coverage denominators.

### Role multiplicity

CES assignments can contain multiple roles. Multiple assigned roles must not be represented as one proven assigned role, and a combined effective permission set is not an assigned role. Callers that expect one role require a sourced business mapping; no arbitrary role may be selected or inferred from effective action membership. See [[concepts/ces-role-multiplicity]].

### Per-tile provider selection and the CES wire value

Each tile selects its entitlement provider independently. An EMS2 tile keeps its existing admission logic; a CES tile uses CES admission logic, configured application identity, and CES permission structure. Moving one tile to CES must not force unrelated tiles to change provider. In the migration contract the `EMS2 (CES)` phrase denotes the CES path, with `EMS3` as its wire value; this interpretation does not merge legacy EMS2 and CES tile admission choices. See [[concepts/per-tile-provider-selection]].

### Provider union for permission checks

Existing `hasPermission(code)` calls may accept a mapped grant from either provider. CES can therefore satisfy a permission check that EMS2 would otherwise deny, and the implementation must log which provider supplied an accepted grant. No additional caller scope argument is required. This shared functional check is separate from tile admission and does not select a scalar role or resolve saved-item ownership. See [[concepts/permission-check-provider-union]].

### Deferred CES role-owned writes

CES saved-view and filter writes that require one owner role stay unavailable until an ownership rule is agreed. No primary CES role may be selected, and comma-joined role names may not be submitted as a scalar owner. Existing EMS2 role-owned write behavior is preserved. This interim rule does not define CES query visibility, role-query rules, or a multiple-role exclusion policy.

### SDK 3.0.0 compatibility requirement

The user selected version `3.0.0` for the SDK migration and requires that the old contract be preserved where possible, with complete compatibility assessed. The SDK caller supplies the FMAA token, and the SDK must use that token as its bearer credential when requesting the caller's configured CES entitlement scope, making zero independent token-acquisition requests.

The returned permission map must contain zero missing and zero unsupported additional role-scoped permissions while preserving required legacy subject and action meaning. Where CES evidence cannot preserve that meaning, the gap must be surfaced explicitly rather than filled by invented role attribution or extra grants.

### Open compatibility questions

- Which supported CES data preserves each legacy role-specific grant for SDK 3.0.0 compatibility?
- Which failure-handling contract should SDK 3.0.0 callers use when CES returns incomplete or ambiguous permission data?
- Is any CES identifier or role structure equivalent to its EMS2 predecessor?
- How must multiple CES roles map to existing upper-application role contracts and role-dependent business rules?
- Which CES-only management permissions fall outside the migrated business permissions?

## Boundaries and limits

CES provides entitlement context, not application authorization. [[concepts/entitlement-retrieval]] through the [[entities/single-ui-sdk]] does not by itself enforce subject-and-action permissions inside each tile application. [[concepts/portal-entry-and-tile-authorization]] therefore remains separate from business-data permission checks performed by applications.

The migration-parity material records user-stated intent and comparison scope only. It does not establish completed migration, current CES account assignments, deployed permission equality, or implemented and tested CES entity responses. The provider-union clarification changes permission-check intent without proving implementation or deployed log collection. No CES endpoint contract or compatibility build was inspected, and no human review or migration acceptance is recorded. The applicable artifact and runtime behavior for each consumer remain unresolved.

## Related pages

- [[entities/ems2]] — the predecessor entitlement system and its entity, role, subject, and action model.
- [[entities/ems3]] — the wire value identifying the CES authorization path in migrated contracts.
- [[entities/single-ui-sdk]] — the SDK that reads CES entitlements and must migrate to 3.0.0 without contract drift.
- [[entities/ratan]] and [[entities/mfe-ratan-container]] — the team label, shared container, and CES application mapping used as the worked example.
- [[entities/mfe-base]] — the shared base whose upper-application APIs must stay compatible.
- [[entities/fmo-post-trade-portal]] — the portal whose tiles consume entitlement data.
- [[entities/portal-team]] — the user-reported owner of entry and tile policies that rely on entitlement decisions.
- [[concepts/single-ui-sdk-authentication]] — token validation behavior that CES retrieval must not be confused with.
- [[concepts/entitlement-retrieval]] — the two documented retrieval paths and their lifecycle caveats.
- [[concepts/portal-entry-and-tile-authorization]] — how entitlement results drive entry and tile visibility decisions.
- [[concepts/ems2-to-ces-permission-mapping]] — the role/entitlement, entity/application, subject/feature, action/action comparison model.
- [[concepts/per-tile-provider-selection]] — independent provider admission for each tile.
- [[concepts/permission-check-provider-union]] — accepting mapped grants from either provider through one caller API.
- [[concepts/ces-role-multiplicity]] — why multiple CES roles cannot collapse into one assigned role.
- [[summaries/KT-sdk-and-entitlements]] — the source summary for the SDK compatibility material.
- [[summaries/KT-ces-migration-parity]] — the source summary for the migration parity material.


See also: [[summaries/KT-architecture-evolution]]
