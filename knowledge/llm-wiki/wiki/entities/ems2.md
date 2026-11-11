---
sources: ["summaries/KT-ces-migration-parity.md", "summaries/KT-authentication-and-sessions.md", "summaries/KT-release-operations.md", "summaries/KT-admin-and-onboarding.md", "summaries/KT-observability-and-performance.md", "summaries/KT-architecture-evolution.md", "summaries/KT-portal-purpose.md", "summaries/ARC-portal-service-relationships.md", "summaries/KT-sdk-and-entitlements.md"]
type: "Product"
description: "EMS2 is the legacy entitlement system defining portal application entities, roles, subjects, and actions."
---

# EMS2

## What it is
EMS2 is the entitlement system that defines the application **entities**, **roles**, **subjects**, and **actions** used to authorize access in the [[entities/fmo-post-trade-portal]]. The setup procedure creates those objects and then assigns actions to role-and-subject combinations. Those objects provide entitlement context for application-specific checks.

The portal purpose topic places EMS2 under the portal **Access** capability and describes that capability as EMS2 roles plus configured tile eligibility. This makes EMS2 part of the shared portal capability set rather than an application domain function.

EMS2 is distinct from [[entities/ces]], the system that received the migrated entitlement data.

## Role in the SDK contract
[[entities/single-ui-sdk]] consumers can reach EMS2 in two ways:

- Query EMS2 directly through `AuthorizationService.getEntitlements`.
- Validate and extract a separate entitlement token through `JwtTokenUtil.getEntitlementsToken`.

The SDK guides forbid using an entitlement token for authentication or login. See [[concepts/entitlement-retrieval]] and [[concepts/single-ui-sdk-authentication]].

Direct EMS2 consumers must maintain certificate and endpoint configuration. The Java 17 guide documents account lookup and entitlement-list endpoints, and it permits an application entity list to constrain retrieval.

## EMS2 configuration and tile behavior
EMS2 entity configuration drives tile visibility and launch decisions in the portal:

- A tile with **zero configured EMS2 entities** must be hidden and must deny direct launch.
- A tile with **one configured EMS2 entity** and **zero configured subjects** stays visible and launchable when the user holds entitlement for that entity. The entity check carries the decision.

The portal purpose topic records **EMS2 roles and configured tile eligibility** as the Access capability. Its draft principles keep tile authorization and tile eligibility as draft intent, so those statements do not establish accepted or enforced behavior.

These are user-stated rules owned by the [[entities/portal-team]] across local, test, UAT, and production. The empty-subject clarification records `configured_entity_count: 1` and `configured_subject_count: 0`, with approval still **pending** and deployed enforcement unverified. It selects no multiple-entity matching rule and no SSDR delegation option. See [[concepts/portal-entry-and-tile-authorization]] for the entry rule and the authoritative scope limits.

The historical tile-security proposal permits an empty **role** setting. That example does not define an empty **entity** setting.

### Independent per-tile provider selection
Migration does not require one batch move of every tile. Each tile selects its entitlement provider independently, and an EMS2 tile must retain its existing admission logic. A tile that moves to CES must not force unrelated tiles to change provider. The migration contract distinguishes plain `EMS2` from the final `EMS2 (CES)` phrase; the latter denotes the CES path, whose wire value is `EMS3` in the [[entities/ems3]] contract. That interpretation does not merge legacy EMS2 and CES admission choices. See [[concepts/per-tile-provider-selection]].

## Portal admin entitlements
Admin catalog functions in the portal are gated by EMS2 entitlements. The admin user manual identifies `FMO PORTAL ADMIN` entitlements for the **Module Mapping**, **Drawer Category**, and **Tile Configuration** functions that maintain the application catalog. Those grants are prerequisites for the admin screens; they do not establish that any current operator holds them. See [[concepts/admin-catalog-configuration]] and [[concepts/ems2-entitlement-provisioning]].

FMO Portal Admin sits outside the production migration comparison under the 3 November 2026 user clarification. Its non-production comparison is kept separate and lower in priority, and its content must not enter production coverage denominators. See [[summaries/KT-ces-migration-parity]].

Provisioning order matters for onboarding. The backend onboarding procedure requires application role or entitlement setup in EMS2 before services integrate SDK-based JWT validation, so the entitlement objects exist before the SDK contract is exercised. See [[concepts/frontend-onboarding]] and [[summaries/KT-admin-and-onboarding]].

## SSDR multiple-entity discussion
The SSDR onboarding discussion describes report users and download users with differing EMS2 entity assignments for the same tile. It proposes **multiple tile entities** with optional subject checks for selected tenants; under that proposal an empty subject would skip validation. It also considers adding missing EMS2 assignments or delegating authorization to SSDR.

The temporary guest-access approach is struck through. The discussion states that the portal does not implement entitlement control outside existing systems such as EMS2. These recorded alternatives establish no approved bypass, selected solution, or deployed permission rule, and the multiple-entity matching rule remains unresolved.

## Migration to CES
### Concept mapping boundary
Migration compares EMS2 and CES through an explicit concept mapping:

| EMS2 concept | CES concept | Comparison boundary |
| --- | --- | --- |
| Role | Entitlement | Compare the mapped definition and its assigned accounts |
| Entity | Application | Preserve application scope when comparing permission names |
| Subject | Feature | Compare each subject through its explicit feature mapping |
| Action | Action | Compare the permitted operation within the mapped feature |

Names shared by different applications do not establish equivalent permissions, and numeric source identifiers can differ without changing mapped permission meaning. See [[concepts/ems2-to-ces-permission-mapping]].

### Entity name change
During migration, EMS2 entity `X_RATANONE` was renamed to CES application `RATAN_ENTITLEMENT_RULE` for the [[entities/ratan]] mapping. The user confirmed this name correspondence for the migration scope only. That mapping also keeps the legacy team label `RATAN` in `applicationName` and the CES `itam_id` `51358` in `applicationId`.

It does **not** establish equivalent entity, application, subject, or role identifiers, role equivalence, deployment status, or publication approval. Retain that distinction when mapping consumers and permission definitions.

### Preserved EMS2 behavior in shared frontend paths
Additive CES metadata and deferred CES writes must not change EMS2 behavior:

- Adding `roleList` and `applicationId` to CES entities must change zero legacy EMS2 authorization decisions and remove zero existing entity fields.
- CES saved-view and filter writes stay pending until an ownership rule is agreed, while an established EMS2 role-owned write keeps its existing EMS2 owner-selection rules. The CES pending rule must change zero EMS2 write decisions.

Multiple CES role assignments do not establish one proven assigned role, so role multiplicity stays a compatibility concern separate from mapped feature/action meaning. See [[concepts/ces-role-multiplicity]].

### Preserved upper-application permission API
Existing `hasPermission(code)` calls may accept a mapped grant from either EMS2 or CES.

- A reviewed application, feature, and action mapping governs how either provider is read.
- The caller passes only the permission code; no new scope argument is required.
- A provider that supplies an accepted grant is logged.

This shared union check is separate from per-tile admission. The clarification changes permission-check intent; it does not prove implementation or deployed log collection. See [[concepts/permission-check-provider-union]].

### Parity comparison scope
The intended migration has no missing mapped entitlements or permission gaps, but that is a user expectation rather than retained execution proof. Entitlement completeness is assessed separately from account permission completeness: compare each mapped application, entitlement, feature, and action relationship before treating catalog totals as evidence, because different entitlements can yield the same combined effective permissions. Account comparisons must cover every account discovered in the selected entity scope, expand multi-ID cells, and count each distinct account once. Applicable data restrictions must be compared through authoritative definitions and resolved values; a matching data profile name alone does not prove equivalent access.

## Entitlement lifecycle notes
The SDK overview recommends caching entitlements and mentions NGINX stickiness for multiple endpoints. It announced removal of EMS2 details from authentication JWTs in DEV on 30 August 2024. That announcement cannot establish the present DEV state or any production state. Cache invalidation, revocation propagation, and cross-instance logout behavior remain unresolved.

## Evidence limits
- The setup procedure alone does not prove that a backend performs subject-and-action checks.
- No downstream service execution or SDK compatibility build was inspected.
- The EMS2 setup page refers to absent entitlement spreadsheets, change attachments, and later setup actions, so detailed grants cannot be reconstructed from it.
- Which CES data preserves each legacy role-specific grant for SDK 3.0.0 remains an open question.
- The portal purpose topic mixes present-tense capability descriptions with draft principles and future proposals; it does not establish deployed or tested EMS2 coverage.
- The migration parity topic records intent and comparison scope only. It does not establish completed migration, current account assignments, deployed permission equality, or implemented provider-union logging.

## Open questions

| Question | Consequence |
| --- | --- |
| Which source defines legacy data field and value restrictions for each profile? | Complete data-scope equality remains unassessed. |
| Which CES-only management grants fall outside the migrated business scope? | Additional grants need classification before equal-content acceptance. |
| How must multiple CES roles map to existing caller role contracts? | Role-dependent CES behavior stays pending without an accepted mapping. |
| Which reviewed mappings cover each upper-application API? | Full compatibility cannot follow from the user objective alone. |

Related: [[summaries/KT-ces-migration-parity]], [[summaries/KT-sdk-and-entitlements]], [[summaries/KT-portal-purpose]], [[summaries/KT-admin-and-onboarding]], [[entities/ces]], [[entities/ems3]], [[entities/ratan]], [[entities/single-ui-sdk]], [[entities/fmo-post-trade-portal]], [[entities/portal-team]], [[concepts/entitlement-retrieval]], [[concepts/portal-entry-and-tile-authorization]], [[concepts/single-ui-sdk-authentication]], [[concepts/ems2-entitlement-provisioning]], [[concepts/ems2-to-ces-permission-mapping]], [[concepts/per-tile-provider-selection]], [[concepts/permission-check-provider-union]], [[concepts/ces-role-multiplicity]], [[concepts/admin-catalog-configuration]], [[concepts/maker-checker-verification-workflow]].

See also: [[summaries/ARC-portal-service-relationships]]

See also: [[summaries/KT-architecture-evolution]]

See also: [[summaries/KT-observability-and-performance]]

See also: [[summaries/KT-release-operations]]

See also: [[summaries/KT-authentication-and-sessions]]