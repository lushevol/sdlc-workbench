---
type: "Concept"
sources: ["summaries/KT-ces-migration-parity.md", "summaries/KT-authentication-and-sessions.md", "summaries/KT-release-operations.md", "summaries/KT-admin-and-onboarding.md", "summaries/KT-sdk-and-entitlements.md"]
description: "How EMS2 creates and assigns entity, action, role, and subject records, and how they map to CES."
---

> Derived candidate/draft knowledge; publication review remains pending. [Canonical source bindings](../../source-manifest.json).

# EMS2 entitlement provisioning

## Definition

EMS2 entitlement provisioning is the procedure that creates and assigns authorization data in [[entities/ems2]] so that a user can enter the [[entities/fmo-post-trade-portal]] and use an onboarded application. It produces the entity, action, role, and subject records that portal and application code read at runtime. It is a prerequisite for access, not proof that access exists.

## Why it matters

Onboarding an application is not complete when the frontend assets load and the backend route resolves. The application also needs role or entitlement data in EMS2, and its services must validate JWTs and read entitlements through the [[entities/single-ui-sdk]]. Provisioning therefore spans routing, authentication, authorization data, and UI registration. See [[summaries/KT-admin-and-onboarding]] and [[summaries/KT-sdk-and-entitlements]].

## Procedure as documented

The recorded setup sequence has four record types and one assignment step.

1. Create an entity.
2. Create actions for that entity.
3. Create roles.
4. Create subjects.
5. Assign actions to role-and-subject combinations.

The documented procedure creates distinct entities, roles, subjects, and actions, then assigns actions to role-and-subject combinations. Under the reviewed CES migration mapping, an EMS2 subject maps to a CES feature. Keep each subject’s specific meaning bound to its reviewed application mapping. See [[concepts/ems2-to-ces-permission-mapping]].

## Portal admin entitlements

The admin user manual identifies `FMO PORTAL ADMIN` entitlements for three portal administration functions: Module Mapping, Drawer Category, and Tile Configuration. These entitlements control who can change the application catalog. The catalog functions themselves are described in [[concepts/admin-catalog-configuration]].

The manual also requires different maker and checker users for those catalog changes. That review rule is separate from EMS2 provisioning: the entitlement permits the action, and the workflow controls its approval. See [[concepts/maker-checker-verification-workflow]].

## Relationship to tile authorization

A tile record can link to one or more EMS2 entities and to role subjects. At launch time the portal checks the user against that configuration. This is the mechanism behind [[concepts/portal-entry-and-tile-authorization]] and the [[concepts/portal-tile-workspace-model]].

A recorded user clarification handles one narrow case. When a tile's subject setting is empty, the portal permits tile visibility and launch through one configured entity, if the user first satisfies portal-entry requirements and holds entitlement for that entity. The owner of this decision is the [[entities/portal-team]], and it applies to local, test, UAT, and production. The decision is pending approval. It resolves the single-entity, empty-subject scope only. It selects no multiple-entity matching rule and no SSDR delegation option.

The provisional SSDR discussion records other alternatives: multiple tile entities, optional subject checks for selected tenants, adding missing EMS2 assignments, and delegating authorization to SSDR. The temporary guest-access proposal is struck through. The discussion states that the portal does not implement entitlement control outside existing systems such as EMS2. None of these alternatives is an approved or deployed rule.

The draft portal principles require matching both the configured EMS2 entity and subject when a tile requires a subject. This is historical draft context. [Historical configured-subject rule](../../../candidates/security/KT-sdk-and-entitlements.md#historical-configured-subject-rule)

## Provisioned records in the CES migration comparison

The recorded EMS2-to-CES mapping converts each provisioned record type into a CES counterpart:

| EMS2 record | CES concept | Comparison boundary |
| --- | --- | --- |
| Role | Entitlement | Compare the mapped definition and its assigned accounts. |
| Entity | Application | Preserve application scope when comparing permission names. |
| Action | Action | Compare the permitted operation within the mapped feature. |
| Subject | Feature | Compare each subject through its explicit feature mapping. |

The mapping is defined in [[concepts/ems2-to-ces-permission-mapping]]. It has three consequences for provisioning work:

- Names shared by different applications do not establish equivalent permissions, and numeric source identifiers may differ without changing mapped meaning.
- Different CES entitlements can produce the same combined effective permission as an EMS2 role. Equal effective permissions do not prove equal definitions or assignments, so provisioning parity needs record-level comparison, not catalog totals.
- The intended migration is stated to have no missing mapped entitlements or permission gaps. That statement is a user expectation, not retained execution proof.

The migration scope, the per-provider admission rule, and the frontend contract are recorded in [[summaries/KT-ces-migration-parity]].

## Coexistence with CES during migration

Provisioning is not switched in one step. Each tile selects its entitlement provider independently, as described in [[concepts/per-tile-provider-selection]]. An EMS2 tile keeps its existing admission logic; a CES tile uses CES admission logic and CES application identity. Moving one tile to CES must not force other tiles to change provider.

Two rules keep callers stable while both providers supply authorization data:

- Existing `hasPermission(code)` calls may accept a mapped grant from either provider. The check logs which provider supplied an accepted grant and requires no new caller argument. See [[concepts/permission-check-provider-union]].
- Multiple assigned CES roles are not collapsed into one proven role. A combined effective permission set is not one assigned role, and callers that expect a single role need a sourced business mapping. See [[concepts/ces-role-multiplicity]].

A related interim rule defers CES saved-view and filter writes that need one owner role. No primary CES role is selected and no comma-joined role names are submitted as a scalar owner. Existing EMS2 role-owned write behavior is unchanged. This rule concerns CES-owned writes only; it does not change how EMS2 roles are provisioned.

For response metadata, EMS3 entities expose CES entitlement names through `roleList` and the CES application `itam_id` through `applicationId`. For the Ratan mapping, `name` is `RATAN_ENTITLEMENT_RULE` and `applicationName` remains the legacy team label `RATAN`. These fields expose assignment names and application identity; they do not resolve scalar role semantics. See [[entities/ces]], [[entities/ems3]], and [[entities/ratan]].

## Boundary with authentication

EMS2 provisioning answers what a user may do. It does not answer who the user is. Login, session handling, and cross-application token handling belong to [[concepts/single-ui-sdk-authentication]] and [[concepts/cross-application-authentication-handoff]]. [[concepts/entitlement-retrieval]] covers how a running application reads the provisioned data.

## Evidence limits

The EMS2 setup page in the source material refers to entitlement spreadsheets, change attachments, and later setup actions that are absent from the retained copy. The admin user manual depends on screenshots that are also absent. Detailed grants and visual procedures cannot be reconstructed from those references alone. The setup page describes prerequisites; it does not establish completed grants for a current operator, and it does not establish an approval.

The migration material adds its own limits. It states intent and comparison scope, not completed migration or deployed permission equality. It does not prove that the provider-union log is implemented or collected. It does not define a mapping from multiple CES roles to existing role contracts.

Known gaps:

- Portal administrators may read audit history and configuration across tenants. Cross-tenant writes and verification remain open, as does the classification of shared tenant records. A tile must never reference metadata from another tile. [Admin access criteria](../../../candidates/operations/KT-admin-and-onboarding.md#portal-administrator-reads-and-tile-metadata-references)
- Multiple-entity tile matching is unresolved.
- SSDR delegation is unresolved.
- The applicable revision of the setup procedure for the current environment is unconfirmed.
- No authoritative source defines the legacy data field and value restrictions for each profile.
- No reviewed scope identifies which CES-only management entitlements fall outside the migrated business permissions.

## Open questions

- Which SSDR entitlement option and multiple-entity matching rule apply to the current tenant configuration?
- Which cross-tenant writes and verification actions are permitted for makers and checkers?
- Which missing materials would let a team reconstruct the detailed grants?
- Which source defines the complete legacy data field and value restrictions per profile?
- How must multiple CES roles map to the existing upper-application role contracts?

## Related pages

- [[concepts/ems2-to-ces-permission-mapping]] — how each provisioned record type maps to CES.
- [[concepts/per-tile-provider-selection]] — how a tile chooses between EMS2 and CES authorization.
- [[concepts/permission-check-provider-union]] — how one permission check reads either provider.
- [[concepts/ces-role-multiplicity]] — why several CES roles are not one assigned role.
- [[concepts/frontend-onboarding]] — the UI-side steps that precede or parallel provisioning.
- [[concepts/admin-catalog-configuration]] — the catalog functions that `FMO PORTAL ADMIN` protects.
- [[concepts/maker-checker-verification-workflow]] — the review rule applied to catalog records.
- [[concepts/portal-entry-and-tile-authorization]] — how tile-level entity checks work.
- [[concepts/entitlement-retrieval]] — how applications read provisioned data.
- [[entities/ems2]], [[entities/ces]], [[entities/ems3]], [[entities/ratan]], [[entities/single-ui-sdk]], [[entities/single-ui-bff]], [[entities/portal-team]]
- [[summaries/KT-admin-and-onboarding]], [[summaries/KT-sdk-and-entitlements]], [[summaries/KT-ces-migration-parity]], [[summaries/KT-application-interoperability]]

See also: [[summaries/KT-release-operations]]

See also: [[summaries/KT-authentication-and-sessions]]
