---
type: "Concept"
sources: ["summaries/KT-ces-migration-parity.md", "summaries/KT-authentication-and-sessions.md", "summaries/REQ-active-session-renewal.md", "summaries/KT-admin-and-onboarding.md", "summaries/KT-application-interoperability.md", "summaries/KT-portal-purpose.md", "summaries/ARC-portal-service-relationships.md", "summaries/KT-sdk-and-entitlements.md"]
description: "Two-layer portal access model: portal entry plus per-tile admission by EMS2 or CES provider."
---

> Derived candidate/draft knowledge; publication review remains pending. [Canonical source bindings](../../source-manifest.json).

# Portal Entry and Tile Authorization

This concept covers the two-layer access decision for the [[entities/fmo-post-trade-portal]]: whether an authenticated user may enter the portal at all, and whether a given tile is visible and launchable. The portal is documented as a common entry point and workspace for integrated tenant applications, while application teams retain their domain business functions. Its entry and identity capability includes SSO, MFA, and session renewal; its access capability includes [[entities/ems2]] roles and configured tile eligibility. These documented capabilities align with the rules below but do not establish deployed or tested enforcement.

Both layers are distinct from application data permissions inside the tile's own backend. They are also distinct from the shared permission-check function that a migrated frontend may use to read either provider.

The administrative material in [[summaries/KT-admin-and-onboarding]] supplies the configuration side of the model. It describes how tile eligibility records are created, reviewed, and activated. It does not add an enforcement guarantee. The authentication and session material in [[summaries/KT-authentication-and-sessions]] supplies the identity side. It records the same rules and separates them from login, session, and provider-migration concerns. The CES migration material in [[summaries/KT-ces-migration-parity]] adds intended per-tile provider selection and a provider-union permission check. It does not change the portal-entry rule, and it does not establish implemented behavior.

## Layer 1: portal entry

The user-stated rule denies portal entry to an authenticated SC user who holds no entitlement for any application entity registered in the portal. The policy was selected for local, test, UAT, and production environments. The [[entities/portal-team]] is named as owner.

The clarification defines a direction only. It specifies no HTTP status, denial wording, timing limit, or entity-versus-role precedence. The authentication topic states that the owner name is user-reported, so portal-team authority and approval remain unconfirmed across all four environments. A conflicting historical tile-security proposal permitted SC accounts to enter; that proposal is retained as historical evidence, not selected intent. The draft-principles material also lists SSO and tile authorization as priorities, but its login and tile-eligibility statements remain draft intent rather than accepted rules.

Portal entry depends on entitlement data that is created outside the portal admin module. The [[concepts/ems2-entitlement-provisioning]] procedure creates an entity, actions, roles, and subjects, and then assigns actions to role-and-subject combinations. The admin user manual identifies `FMO PORTAL ADMIN` entitlements for the import-map, category, and tile functions. These are prerequisites. They do not show that any current operator holds a grant.

The CES migration records do not restate or replace this entry rule. They focus on tile admission and permission checks after a user is already inside the portal. Provider migration therefore does not move the portal-entry decision into the identity provider or into the shared permission check.

## Layer 2: tile visibility and launch

The portal model treats a tile as an application view that a user opens in a workspace; a workspace holds opened tiles. See [[concepts/portal-tile-workspace-model]]. For a tile that selects [[entities/ems2]], eligibility is configured through EMS2 entities and subjects rather than inferred from general portal access. Two configuration edge cases were clarified.

**Empty entity configuration.** When a tile has zero configured [[entities/ems2]] entities, the portal hides the tile and denies direct launch until an entity is configured. The tile count and launch count must each equal zero. The authentication topic records this as a separate user-stated rule, owned by the [[entities/portal-team]] in local, test, UAT, and production.

**Empty subject configuration.** When a tile has one configured EMS2 entity and zero configured subjects, the portal shows the tile and authorizes launch provided the user satisfies the portal-entry rule and holds entitlement for that single entity. The visible tile count and launch authorization count must each equal one. No multiple-entity matching rule was defined. The authentication topic records one configured entity and zero configured subjects for this rule, with the same environments and owner.

The admin material records the same counts for this case: one configured entity, zero configured subjects. It adds that the tile subject setting must be empty, and that the user must still satisfy portal-entry requirements and hold entitlement for that entity. It records the decision as pending approval.

All three rules apply in local, test, UAT, and production and remain owned by the [[entities/portal-team]]. User-stated intent is their only basis. None of them is approved policy.

### Per-tile provider selection

Each tile selects its entitlement provider independently. See [[concepts/per-tile-provider-selection]]. An EMS2-selected tile retains its existing admission logic. A CES-selected tile uses CES admission logic, its configured application identity, and the CES permission structure. Within that selected scope, the [[entities/ces]] application becomes the new entity identity. The migration contract uses `EMS3` as the CES wire value; see [[entities/ems3]].

Moving one tile to CES must not force unrelated tiles to change provider. Application scope must be preserved in both provider paths. Names shared by different applications do not establish equivalent tile eligibility. The CES migration material states this intent for `mfe-base`, the shared Ratan container, and their upper applications; see [[entities/mfe-base]] and [[entities/mfe-ratan-container]]. It does not establish that any tile has already been migrated.

### Shared permission checks across providers

Tile admission is separate from the functional permission check used inside upper applications. The CES migration material permits an existing `hasPermission(code)` call to accept a mapped EMS2 grant or a mapped CES grant. See [[concepts/permission-check-provider-union]] and [[concepts/ems2-to-ces-permission-mapping]]. The check must log which provider supplied an accepted grant, and callers must not be required to pass a new scope argument.

This union does not select the tile's admission provider and does not merge the two admission choices. It also does not select a scalar role. A denial produces no accepted-grant log because neither provider supplies a matching grant. These rules record intended behavior; implementation and deployed log collection are not established.

### CES entity metadata

The CES migration material requires two new fields on EMS3 entities: `roleList` and `applicationId`. `roleList` must contain the corresponding CES `entitlements.entitlement_name` values, bound to their application. `applicationId` must contain the corresponding CES application's `itam_id` value. The requested example identifies the RATAN application as `51358`; see [[entities/ratan]].

For that clarified mapping, the table records `applicationId` alongside the clarified meanings of the existing `name` and `applicationName` fields. The existing fields are retained; the table does not identify three additional new fields.

| Field | Required value | Meaning |
| --- | --- | --- |
| `name` | `RATAN_ENTITLEMENT_RULE` | CES application/entity name corresponding to EMS2 `X_RATANONE`. |
| `applicationName` | `RATAN` | Legacy team/display application name. |
| `applicationId` | `"51358"` | Corresponding CES `itam_id`. |

CES `user_data.app_name` supplies the CES authorization name; it does not supply the legacy team label. These additive fields must not remove existing entity fields or change EMS2 authorization decisions. They expose assignment names and application identity, but they do not resolve scalar role semantics. The clarified values apply to this RATAN mapping and do not establish labels for other CES applications.

### How tile authorization records are administered

The admin user manual describes three functions inside [[concepts/admin-catalog-configuration]]: Module Mapping, Drawer Category, and Tile Configuration. A tile record connects display details, container and route information, and entitlement configuration. Tile configuration captures role subjects and role entities. The schema draft separates application categories, application tiles, and tile authorization records, and its tile authorization records link a tile to [[entities/ems2]] entities. Module and tile paths must match their corresponding routing paths, and comma-separated role entities are converted into an array by the API. These statements explain the design vocabulary. They do not establish the deployed database schema or the active routing table. See [[concepts/portal-ingress-path]] for the routing intake fields.

### Review and activation workflow

The manual requires different maker and checker users. Creation or modification produces an `un-verified` record. Another user checks and verifies that record before activation. Deactivation of a verified record returns it to `un-verified`. Each admin function keeps its own audit history. See [[concepts/maker-checker-verification-workflow]].

The supplied text does not fully specify rollback, activation propagation, or concurrent edits. It also does not show that the different-user check is enforced in code. The maker-checker procedure is therefore documented workflow, not tested access control.

## Boundary with authentication and session handling

Portal entry presumes an authenticated session. Login, session renewal, and timeout handling decide whether a valid session exists; they do not decide entitlement. The authentication topic keeps these responsibilities separate. The BFF completes an authorization-code exchange, builds user information, retrieves [[entities/ems2]] entitlements, and issues authentication and entitlement tokens. Entity and subject checks therefore consume the retrieval step recorded in [[concepts/entitlement-retrieval]]; they do not create entitlements.

Session renewal supports continued activity without fresh authentication. See [[concepts/session-activity-renewal]], [[concepts/session-expiry-prompt-recovery]], [[concepts/token-lifecycle-and-timeout-policy]], and [[summaries/REQ-active-session-renewal]]. These materials define when a session stays valid. They do not change the result of an entry or tile decision. An expired session forces a new authentication before any entry check runs again. The session documents also contain unresolved timing proposals, so no timeout value of theirs can serve as an authorization input.

The Entra phase 1 scope covers UI SSO only. It excludes EMS2 replacement and portal session management. Provider migration therefore keeps existing entry and tile authorization ownership. It does not move entitlement decisions into the identity provider. The production guide notes that AD profile values differ from OUD values for surname formatting, country codes, and locale. Those differences can affect downstream audit or application logic. The supplied material does not show that they change entity or subject matching. See [[concepts/identity-profile-attribute-migration]] and [[concepts/identity-provider-delegation]].

The CES provider-union rule changes functional permission checks after entry. It does not change the SSO boundary or the session boundary.

## Boundary with application permissions

Portal entry and tile authorization govern presence and launch. They do not grant permission to read or edit business data. The tile-security proposal delegates data access and editing permissions to each tile application, which defines entities, roles, subjects, and actions in [[entities/ems2]] and is expected to enforce subject-and-action checks itself.

Because [[entities/single-ui-sdk]] primarily documents JWT validation and [[concepts/entitlement-retrieval]], it does not establish automatic subject-and-action enforcement for every API. A visible tile is therefore not evidence of an authorized business action. Assuming otherwise can leave protected operations unspecified.

The admin material states the same boundary for tenant onboarding. It records that the portal does not implement entitlement control outside existing systems such as [[entities/ems2]]. The SSDR discussion in that material also records that a temporary guest-access proposal was struck through. Recorded alternatives are not an approved bypass.

### Role multiplicity and role-owned writes

Multiple assigned CES roles must not be treated as one proven assigned role. A combined effective permission set is not the same as a single role assignment. The CES migration material identifies non-unique roles as the known frontend compatibility gap. Callers that expect one role require a sourced business mapping; no arbitrary role may be selected and no named role may be inferred from effective action membership. See [[concepts/ces-role-multiplicity]].

The same material defers CES saved-view and filter writes that require one owner role. Until an ownership rule is agreed, the portal must not select a primary CES role or submit comma-joined role names as a scalar owner. Existing EMS2 role-owned write behavior is preserved. This interim rule does not define CES query visibility, role-query rules, or a multiple-role exclusion policy. The `roleList` and `applicationId` entity fields do not resolve this scalar-role question.

## Tenant and record boundaries

The admin proposal discusses tenant-specific roles, while the manual lists shared admin subjects and a different-user check. The supplied text does not establish record-level tenant isolation for maker and checker users. A tenant that shares the `FMO PORTAL ADMIN` subject with other tenants therefore has no documented record boundary.

## Status and evidence limits

Every rule above records user-stated intent. None is approved policy, an executable result, or evidence of deployed enforcement. Owner authority, publication approval, and runtime behavior remain unconfirmed, and no UI or service observation binding was verified. The associated business criteria (`UI-ENTRY-AC-001`, `UI-EMPTY-ENTITY-AC-001`, `UI-EMPTY-SUBJECT-AC-001`) preserve the historical test-case versions without byte changes. The authentication topic records their definition in [[summaries/KT-sdk-and-entitlements]] and states that approval for intended applicability remains pending.

The wider portal material adds further limits. The portal introduction remains under edit, the principles remain draft, and the capabilities page mixes present-tense descriptions with an unfinished FDC3 item and depends on screenshots absent from the supplied export. A separate deployment proposal describes onboarding changes, workflow AI, telemetry, infrastructure migration, notification, dashboards, and OpenFin for 2026 and early 2027, but it has no approval record in these materials. Proposed services and roadmap items therefore cannot serve as current implementation facts for entry or tile authorization.

The admin sources add their own limits. The admin overview and schema are proposals; the user manual is procedural. Their source revisions and current applicability remain unconfirmed. The EMS2 setup page refers to entitlement spreadsheets, change attachments, and later setup actions that are absent from the export, and the manual depends on screenshots absent from this copy. The [[entities/flyway]] SQL, the [[entities/nginx]] draft, and the firewall register have no inspected deployment or connectivity execution. Retained definitions cannot establish the current schema, active routes, or network permissions. The SSDR discussion records alternatives without a retained approval or execution record.

The authentication sources repeat this pattern. They have local byte revisions but no confirmed original page revisions or approval authority. Their historical session and migration designs contain unresolved and conflicting proposals. The supplied migration guides also disagree on the activation grammar, using `ENABLE_ENTRA_SSO=true/false` in one place and `yes/no` in another. Such documents identify intended responsibilities only. They cannot serve as current security policy for entry or tile authorization.

The CES migration parity source is a `candidate` draft based on user clarifications dated 3 to 9 November 2026. It defines intended permission preservation, frontend compatibility, and per-tile provider selection. It does not establish completed migration, deployed permission equality, implemented `hasPermission` union behavior, collected provider logs, or tested `roleList` and `applicationId` responses. No approved scalar role mapping is recorded. Its statement about returned legacy entities remains an implementation question separate from the intended rule.

## Related pages

- [[summaries/KT-portal-purpose]] describes the portal purpose, capability map, draft principles, and roadmap evidence limits.
- [[summaries/KT-sdk-and-entitlements]] documents the source rules, SDK versions, and open questions.
- [[summaries/KT-admin-and-onboarding]] describes the admin module, onboarding sequence, EMS2 setup, and the empty-subject clarification.
- [[summaries/KT-authentication-and-sessions]] records the identity, session, and Entra migration boundaries for these decisions.
- [[summaries/KT-ces-migration-parity]] records the CES migration scope, per-tile provider selection, provider-union check, entity metadata, and role-owned write deferral.
- [[concepts/single-ui-sdk-authentication]] explains the JWT filter that produces the `userInfo` context these decisions rely on.
- [[concepts/entitlement-retrieval]] explains how services obtain the entitlements used by the entity and subject checks.
- [[concepts/cross-application-authentication-handoff]] explains how an authenticated identity moves between the portal and its applications.
- [[concepts/identity-provider-delegation]] and [[concepts/identity-profile-attribute-migration]] explain the provider-replacement boundary that leaves entitlement decisions in place.
- [[concepts/ems2-entitlement-provisioning]] explains how entities, actions, roles, and subjects are created before a tile can be authorized.
- [[concepts/admin-catalog-configuration]] explains the module mapping, drawer category, and tile configuration functions.
- [[concepts/maker-checker-verification-workflow]] explains the un-verified, verify, and activate sequence for admin records.
- [[concepts/frontend-onboarding]] and [[concepts/portal-ingress-path]] explain the deployment and routing inputs that onboarding supplies.
- [[concepts/per-tile-provider-selection]] explains how one tile moves to CES without forcing other tiles to change provider.
- [[concepts/permission-check-provider-union]] explains how `hasPermission(code)` accepts mapped EMS2 or CES grants and logs the provider.
- [[concepts/ems2-to-ces-permission-mapping]] explains the application, feature, and action mapping used by the union check.
- [[concepts/ces-role-multiplicity]] explains why multiple CES roles are not collapsed into one scalar role.
- [[entities/ces]] holds the migrated entitlement rule names relevant to future enforcement.
- [[entities/ems3]] is the CES wire value used by the migration contract.
- [[entities/ratan]] is the clarified application mapping for `roleList` and `applicationId`.
- [[entities/mfe-base]] and [[entities/mfe-ratan-container]] are the shared frontend scopes named in the compatibility objective.
- [[entities/single-ui-sdk]] is the SDK artifact family at issue.
- [[entities/single-ui-bff]] is the reused admin backend recorded in the admin proposal and the component that issues the portal tokens.
- [[entities/entra]] is the replacement SSO provider that leaves EMS2 and portal session management outside its phase 1 scope.

## Open questions

- Does any listed entity suffice when a tile has multiple configured EMS2 entities?
- Which SSDR entitlement option and multiple-entity matching rule apply to the current tenant configuration?
- How are tenant record boundaries enforced for maker and checker users?
- What evidence confirms portal-team authority and approval across the four environments?
- What evidence confirms deployed enforcement of the empty-entity and empty-subject rules?
- Where does each downstream service enforce subject and action permissions?
- Which release, approval, rollback, and emergency-change controls govern configuration changes made through the admin module?
- Which source revisions and environment checks establish the deployed catalog schema?
- Which draft principles, including SSO and tile eligibility, became accepted rules, and when?
- Which 2026 and 2027 proposals have approved scope or deployed implementations?
- Which identity-provider profile contract downstream services must support after the SSO migration?
- Which intended session timeout and refresh-duration rules apply, and do they change when entry checks are repeated?
- Which reviewed application, feature, action, and caller contract mappings define CES tile admission for each migrated tile?
- How must multiple CES roles map to existing upper-application role contracts and role-dependent business rules?
- Which CES-only management permissions fall outside the migrated business permission scope?

See also: [[summaries/ARC-portal-service-relationships]]

See also: [[summaries/KT-application-interoperability]]

See also: [[summaries/REQ-active-session-renewal]]
