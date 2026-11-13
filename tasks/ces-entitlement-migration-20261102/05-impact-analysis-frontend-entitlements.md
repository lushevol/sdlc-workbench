---
artifact_kind: change-request
id: CR-CES-FRONTEND-ENTITLEMENT-IMPACT
version: 5
status: draft
owner: unknown
source_refs: [USER-MINIMAL-FRONTEND-20261106, USER-APPLICATION-IDENTITY-20261106, USER-BFF-ENTITY-FIELDS-20261106, USER-FRONTEND-SNIPPETS-20261106, USER-FRONTEND-COMPATIBILITY-20261106, USER-FRONTEND-20261105, BFF-MAIN, BFF-CANDIDATE, MFE-BASE, RATAN-CONTAINER, LOGIN-CAPTURE, TILE-DUMP]
related_ids: [CES-MIGRATION]
review:
  state: pending
  reviewer: null
  reviewed_at: null
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
    - Automated checks do not check the complete approved dictionary or grammar rules.
---

# CES migration: required frontend entitlement changes

Current implementation: [tests-first shared adapters](10-change-review-frontend-adapters.md).
The source findings and unapplied snippets below retain their original proposal baseline and verification limits.

> **Preserve upper-application APIs and select authorization independently for each tile.**
> Action: adapt shared internals for EMS2 and CES. Reconcile role multiplicity as the known public-contract gap.
> Consequence: replacing shared APIs or forcing batch cutover would contradict the latest migration decisions.
> Owner: unknown. Evidence: [user decisions](evidence/frontend-entitlement-impact-20261105/user-clarification-20261106.md#exact-user-input).

> **Preserving global permission calls requires authoritative provider routing.**
> Action: supply current feature-to-provider/application bindings and bind conflicting same-feature callers explicitly.
> Consequence: granted entities alone cannot identify a denied tile's provider or distinguish simultaneous conflicting callers.
> Owner: unknown. Evidence: [routing boundary](#required-routing-input-and-the-plain-function-limit).

| Essential result | Evidence boundary |
| --- | --- |
| Shared helper resolves 1/31 captured CES grants; 30 fail. | Original TypeScript execution with capture-fed hooks. No browser execution. |
| Helper resolves 0/24 grants whose features have exact tile-dump references. | Counts include all database rows. They do not establish deployed business scope. |
| All 41 captured CES tiles fit the portal's generic entity/subject predicate. | Source-predicate replay; no original-module or browser tile execution. |
| Nine existing base tests pass across four files. | Focused subset. Some tests contain no assertions. No complete unit-suite claim. |
| Frontend changes remain proposed. | The separate BFF enhancement does not implement the frontend adapters. |
| The smallest proposal covers shared models, launch, profile, authenticator, roles, and admin routing controls. | [Latest request](evidence/frontend-entitlement-impact-20261105/user-minimal-frontend-adapters-20261106.md#exact-user-input). No frontend patch applied. |
| API compatibility and independent tile selection are required design constraints. | Latest user intent; complete compatibility remains unverified. |

## Request and source facts

Latest request: [minimal shared frontend changes](evidence/frontend-entitlement-impact-20261105/user-minimal-frontend-adapters-20261106.md#exact-user-input).
This stage refines proposals. It does not apply frontend source changes.
The [identity clarification](evidence/frontend-entitlement-impact-20261105/user-clarification-application-identity-20261106.md#exact-user-input) distinguishes three fields.
Keep `name: RATAN_ENTITLEMENT_RULE`, `applicationName: RATAN`, and `applicationId: "51358"` separate.
BFF commit `c114b9c67f7bd6a2afc8a4394b4c372e2aea2e2d` implements the explicit legacy team mapping.
Its subsequent test execution remains unavailable. See the [BFF stage](10-change-review-bff-entity-fields.md#stage-evidence-and-completion).

The [later BFF field request](evidence/frontend-entitlement-impact-20261105/user-bff-entity-fields-20261106.md#exact-user-input) selects additive `roleList` and `applicationId` fields.
The [BFF enhancement stage](10-change-review-bff-entity-fields.md) records that implementation and its separate verification limits.
Frontend snippets below remain proposed. Original capture findings retain their earlier source bindings.

Latest authority: [compatibility and per-tile decisions](evidence/frontend-entitlement-impact-20261105/user-clarification-20261106.md#exact-user-input), 6 November 2026.
Preserve upper-application APIs where possible. EMS2 tiles retain legacy logic; CES tiles use configured CES identities and structures.
Roles need explicit treatment because a single role is no longer assured.
The design below applies this clarification. Earlier capture findings retain their original evidence boundaries.

Assessment: 6 November 2026, Asia/Singapore. Assessor: Codex.
The [request](evidence/frontend-entitlement-impact-20261105/user-input.md#exact-user-input) arrived on 5 November and authorizes required-change identification.
The user identifies the CSV as a database dump.
The user identifies the JSON as a real login capture for account `1481696`.
Capture environment, build, and time remain unknown.
Entry route: existing implementation with supplied database and runtime evidence.

The [capture summary](evidence/frontend-entitlement-impact-20261105/capture-summary.json) records 113 database rows: 45 EMS3 and 68 EMS2.
All 45 EMS3 rows use app ID `51358` and app name `RATAN_ENTITLEMENT_RULE`.
Their legacy `ems2_entities` values retain `X_RATANONE`.
The login contains 61 tiles: 41 EMS3 and 20 EMS2.
Its CES aggregate contains 21 features and 31 feature/action pairs.
CES role names and legacy numeric identifiers are null.
The entitlement token contains the key `RATAN_ENTITLEMENT_RULE:null`. This suffix is not an assigned role.

The [existing name clarification](evidence/user-input-20261030-field-equivalence.txt) establishes the migration name correspondence.
The [permission intent](../../knowledge/records/candidates/security/KT-ces-migration-parity.md#mapping-between-authorization-concepts) requires application scope.
Matching feature names across different applications cannot establish equivalent permissions.

## Stage boundary and readiness

- Stage: bounded frontend compatibility impact analysis, completed within the inspected scope.
- Readiness: `READY` for compatibility analysis handoff and scoped engineering design.
- Rationale: exact BFF sources and both frontend consumers establish the required compatibility surfaces.
- Existing intake: [01-intake.md](01-intake.md), preserved unchanged. Its hash appears in the [capture summary](evidence/frontend-entitlement-impact-20261105/capture-summary.json).
- BFF comparison: local `main...HEAD`; `main` equals the merge base. No remote fetch occurred.
- Role multiplicity is confirmed. Its scalar API behavior still needs a defined contract.
- Same-feature tile context and blank-feature admission need resolution before their dependent implementation acceptance.
- Business acceptance, knowledge publication, and deployment retain their separate pending states.
- Full frontend implementation readiness is not established by this analysis.

## Proposed change

### Compatibility principle and per-tile routing

The [latest user decisions](evidence/frontend-entitlement-impact-20261105/user-clarification-20261106.md#exact-user-input) control the design.
Keep existing `mfe-base` and `@fm/ratan_container` imports, component entry points, and permission calls where possible.
Keep `hasPermission(module: string)` and existing feature/action strings for upper applications.
Keep its boolean result contract. Hide provider normalization and application lookup inside shared adapters.
Keep `getUser()` callable through its existing interface. Treat scalar role meaning as the explicit compatibility exception.
The user identifies roles as the known gap. Other compatibility remains a required goal, not a proven result.

| Selected tile source | Internal route | Upper-application expectation |
| --- | --- | --- |
| `EMS2` | Existing entities, subjects, actions, roles, and legacy checks. | Existing behavior and calls remain unchanged. |
| CES, wire value `EMS3` | Configured CES application/entity and CES permission structures. | Shared adapters preserve existing feature/action permission calls where possible. |

Select the provider from the specific tile configuration.
Do not select CES merely because a user has any CES grant.
Do not retry a denied CES action against EMS2, or reverse that direction.
Mixed EMS2 and CES tiles must work in the same portal session.
Changing one tile must not change another tile's selected provider.
Global cutover settings cannot substitute for per-tile selection during normal staged migration.
Existing administrative rollback modes need separate effective configuration and verification.
The [BFF dual-provider path](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/TileAuthorizationServiceImpl.java#L43-L72) already partitions tiles by source.
Its `EMS3_ONLY` branch excludes EMS2 grants. That mode does not support the normal mixed-provider rollout.
The [checked-in setting](../../repos/services/single-ui-bff/src/main/resources/application.yml#L85-L88) selects `EMS3_PRIMARY_DUAL_READ`.
Confirm the effective environment setting before testing independent tile selection.

The [base mount](../../repos/ui/mfe-base/src/pages/Home/common/Container.tsx#L26-L32) currently passes five legacy props.
It does not pass the tile's provider or application identity.
The [shared helper](../../repos/ui/mfe-ratan-container/src/ratanutils/authenticator.ts#L1-L12) reads the global base hooks store.
Next action: carry tile identity and provider through shared internals with additive metadata where needed.
A module-wide active-provider variable cannot isolate simultaneous tiles with different selections.
Keep a per-instance binding design explicit before claiming unchanged callers work in ambiguous same-feature cases.
Do not silently choose the first matching tile or merge both providers' grants.
The [design evidence](evidence/frontend-entitlement-impact-20261105/compatibility-design.json) records the inspected context boundary.
The current dump has no feature configured across both providers. Nine CES features repeat across tiles.
The same-feature mixed-provider boundary can arise during future independent tile changes.
It is a design constraint, not an observed production failure.

Preserve the public method signatures where the selected scope can be established internally.
If an existing caller has no distinguishable tile context, record that compatibility limit before selecting a workaround.
No mandatory new public argument is approved by this analysis.

### Proposed code snippets

Source: [minimal-change request](evidence/frontend-entitlement-impact-20261105/user-minimal-frontend-adapters-20261106.md#exact-user-input).
These snippets are proposals. No frontend source patch or application execution accompanies this refinement.
Existing public imports, permission strings, and ordinary launch arguments remain the compatibility baseline.

#### Smallest shared change set

| Shared area | Minor internal change | Upper-application effect |
| --- | --- | --- |
| Base response models and login | Add `applicationId`, `roleList`, and source metadata. Retain structured entities. Replace the drawer store even when its valid response is empty. | Existing login envelope and endpoint remain. |
| Base launch and restore | Retain database tile identity. Resolve current authorized tiles before mounting. Pass optional internal scope. | Keep ordinary `dispatchOpenTile` and accessibility calls. |
| Base profile | Display team, CES entity name, and role list. Read CES actions from subjects. Use scoped presentation keys. | No business-role projection. |
| Ratan authenticator | Select configured provider first. Keep EMS2 logic and add exact application/feature/action lookup for CES. | Keep `hasPermission(code): boolean` and higher-level permission helpers. |
| Ratan user and shared role components | Retain identity fields and legacy scalar role. Add application-scoped role-list access. Adapt saved views, filters, and role restrictions separately. | Role-sensitive behavior remains the explicit semantic gap. |
| Base admin editor | Add the four existing BFF routing fields to edit, detail, and audit views. | Operational requirement when administrators switch tiles through this UI. |

The [login code](../../repos/ui/mfe-base/src/utils/login.ts#L65-L95) already retains returned entities.
A new CES HTTP client, login endpoint, or token-decoding scheme is unnecessary for these adapters.
Avoid routing authorization through the display field `applicationName`.

#### Base: retain metadata and current tile identity

Add these optional metadata fields to existing models. Correct nullable wire identifiers in a separate boundary type.
Widening exported numeric or scalar types can cause TypeScript errors in existing upper applications.
Do not claim source compatibility merely because runtime JSON remains readable.

```ts
// Additive fields on existing models:
interface Entity {
  applicationId?: string;
  roleList?: string[];
}
interface Subject {
  entitlementSource?: "EMS2" | "EMS3";
}
interface Tile {
  entitlementSource?: "EMS2" | "EMS3";
}

// Internal base/container boundary; fields are proposals.
interface TileEntitlementScope {
  tileId: string;
  source: "EMS2" | "EMS3";
  applications: Array<{ applicationId: string; entityName: string }>;
}
```

The current wire response permits null legacy entity, role, subject, and action identifiers.
Keep those nulls in the wire model. Do not create fake IDs to satisfy the old TypeScript declarations.
Review exported type consumers before exposing stricter nullable contracts.

Before replacing the database ID with a workspace UUID, retain it separately:

```ts
const container = {
  ...tile,
  applicationTileId: String(tile.id),
  id: uuidv4(),
  parameters,
};
```

Apply this in drawer clicks, deep links, `OpenCashflow`, and `dispatchOpenTile`.
The drawer click currently uses an explicit field list. Add `applicationTileId` there before calling `addTile`.
Resolve that identity against the latest authorized drawer at mount and restore.
For old saved workspaces, require one current route and entry-name match. Do not select the first ambiguous match.
Forward optional `entitlementScope` from [Container.tsx](../../repos/ui/mfe-base/src/pages/Home/common/Container.tsx#L26-L32).
The Ratan App and Routing already spread their received props.
That forwarding does not bind existing global imported permission functions automatically.

For CES admission, use the current server-authorized tile decision.
For EMS2, retain the old validator over EMS2 subjects only.
Keep the existing exported `validateTile` signature; introduce the source-aware wrapper internally.
Reconcile blank-feature admission separately. This proposal does not approve its current BFF bypass policy.

The current [drawer handler](../../repos/ui/mfe-base/src/utils/login.ts#L98-L106) ignores an empty list.
Replace the truthy length test with an array check so current empty catalogs replace stale ones:

```ts
if (Array.isArray(response?.data?.drawers)) {
  baseDispatch({
    type: ActionType.SET_DRAWERS,
    data: { drawers: response.data.drawers },
  });
}
```

Refresh must replace entities and bindings together before permission checks resume.
Local workspace data supplies a locator. It does not supply current authorization authority.

#### Base: keep profile presentation inside the shared layer

Use [Profile/util.ts](../../repos/ui/mfe-base/src/components/Profile/util.ts#L1-L5) to display roles without changing their meaning:

```ts
export const getName = (entity) => {
  const roles = entity.roleList?.length
    ? entity.roleList.join(", ")
    : entity.roleName ?? "*";
  return `${entity.applicationName ?? "*"} :: ${entity.name} :: ${roles}`;
};
```

For this application, the label starts with `RATAN :: RATAN_ENTITLEMENT_RULE`.
At the [profile action lookup](../../repos/ui/mfe-base/src/components/Profile/index.tsx#L109-L113), read CES actions directly:

```ts
const actionObj = subject.entitlementSource === "EMS3"
  ? subject.actions.map(action => action.name)
  : entitlements[`${entity.name}:${entity.roleName}`][subject.name];
```

Use application ID, CES entity name, and feature name for internal presentation keys when numeric IDs are null.
Keep legacy keys where their identifiers remain available.
This avoids requiring CES profile display to reconstruct legacy `name:roleName` token keys.

#### Container: retain the public permission signature

Extract the old resolver into `legacyHasPermission`. Feed it an EMS2-only user projection.
Preserve its legacy action-string handling and role behavior.
Select the provider before that resolver or its flat `user.actions` shortcut can grant access.

The resolver below uses one selected CES application for clarity. Multiple configured names need equivalent exact scope checks.
`resolveConfiguredTarget` and `readEms2User` are integration points to implement; neither exists in the current source.
The former requires routing evidence independently of the user's grants.

```ts
export const hasPermission = (code: string): boolean => {
  const target = resolveConfiguredTarget(code);
  if (!target) return false;

  if (target.source === "EMS2") {
    return legacyHasPermission(code, readEms2User());
  }
  if (target.source !== "EMS3") return false;

  const [feature, action, ...extra] = code.split(":");
  if (!feature || !action || extra.length) return false;

  return (getHooks().store?.entities ?? []).some(entity =>
    entity.applicationId === target.applicationId &&
    entity.name === target.entityName &&
    entity.subjects?.some(subject =>
      subject.entitlementSource === "EMS3" &&
      subject.name === feature &&
      subject.actions?.some(item => item.name === action)
    )
  );
};
```

For the clarified CES target, use `applicationId: "51358"` and `entityName: "RATAN_ENTITLEMENT_RULE"`.
Its entity `applicationName: "RATAN"` remains display metadata.
Evaluate every matching entity row. Do not overwrite earlier grants through a name-only map.
No CES denial may fall back to the EMS2 resolver.
Keep exported higher-level helpers calling this function, including private/public view and exception helpers.

#### Required routing input and the plain-function limit

**The supplied BFF response cannot yet populate a complete provider-routing index.**
Current drawers contain authorized tiles and source markers. They omit denied tiles, application IDs, and CES feature configuration.
The [drawer builder](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java#L202-L225) establishes that limit.
The entity `applicationId` identifies grants. It cannot establish which provider a denied tile selected.

Use a complete authoritative routing map, including denied bindings, to populate `resolveConfiguredTarget`.
Prefer a small additive BFF routing catalog derived from the same effective tile configuration.
Alternatively, a reviewed complete migration configuration can supply that map, provided it stays synchronized with tile changes.
Forwarding app IDs and features on authorized drawer tiles helps instance binding but does not supply denied bindings.
Filter that catalog to necessary identifiers. Do not expose admin or assignment details merely to route permissions.
Resolve the requested feature's target, including cross-feature calls. Do not blindly use the caller tile's application.
Unknown, invalid, incomplete, or conflicting targets must not grant permission.
Explicitly include authoritative legacy action-string routes; lack of a CES mapping must not imply EMS2.

The supplied dump has unambiguous feature-to-provider/application bindings.
A complete map can therefore preserve ordinary one-argument calls for this configuration.
If two tiles use the same feature under different providers, a global imported function cannot identify its caller.
For that case, bind a facade at the shared consumer boundary or add optional explicit scope for affected callers.
A facade can retain `hasPermission(code)` on the bound object, but consumers must actually use that binding.
React context alone cannot change plain imported functions or permissions computed at module initialization.
A global active-tile variable also fails when multiple tiles remain mounted.

#### Keep getUser and separate the role exception

Keep `getUser()` callable. Retain its `id`, `name`, `actions`, and existing entitlement-map fields where their meanings remain supported.
Do not use its name-only entitlement map as the authoritative CES permission source.
Keep EMS2 scalar `role` semantics. Add scoped role-list access from exact CES application ID and entity name.
An optional `getUser().roleList` can expose CES assignments when its application scope is explicitly defined.
It does not turn the legacy scalar `role` into a role collection.

The shared ViewSelector and FilterSelector need internal changes for role lists.
Membership checks, existing owner matching, query filtering, and new owner selection are separate decisions.
Existing backend `assignee` and `moduleOwner` fields remain scalar; do not send comma-joined roles without an agreed backend contract.
Review `PSS_RO` restrictions against the accepted multiple-role rule before replacing equality with membership.
Do not choose the first CES role or invent role priority.
Do not derive a trusted data profile from `Global` or another assignment name alone.

The analytics-only profile helper can format a joined role list if that telemetry field accepts assignment labels.
That display string must not become authorization or data-profile truth.

Validation: [minimal proposal checks](evidence/frontend-entitlement-impact-20261105/minimal-frontend-adapters-validation-20261106.json).
Those checks cover syntax, sources, and references. They do not execute these proposed adapters.

### FE-01: Replace identity-specific shared permission dispatch

Priority: P2. Confidence: high. Owner: unknown.
Location: [authenticator.ts](../../repos/ui/mfe-ratan-container/src/ratanutils/authenticator.ts#L38-L105).
Setup and numbered steps: [TC-FE-CES-001](06-test-cases.md#tc-fe-ces-001).

Required result: preserve mapped, application-scoped grants through the migration.
Old source path: `X_RATANONE` selects exact subject/action lookup.
New input: `RATAN_ENTITLEMENT_RULE` reaches legacy entity-name substring matching.
Most feature names do not match that application name. The helper returns false despite a captured grant.
The sole passing pair has feature name `RATAN_ENTITLEMENT_RULE`, which accidentally matches the application name.
A synthetic name-only control resolves all 31 grants. This is not an actual EMS2 baseline.

Next action: introduce an internal resolver for tile, application, feature, action, and selected provider.
Keep upper applications calling the existing permission helpers.
Keep EMS2 compatibility during mixed rollout. Use reviewed configuration for application correspondence.
Keep existing feature/action constants when their CES meanings match.
Merge duplicate rows within the selected application. Do not merge grants across unrelated applications.
Do not use a global feature search or substring matching to select an application.

The [shared export](../../repos/ui/mfe-ratan-container/src/root.tsx#L12) reaches [cashflow consumers](../../repos/ui/mfe-cashflow-blotter/src/Root/import/ratanutils/index.ts#L6-L7).
Update the shared container and verify its deployed import-map consumers together.

### FE-02: Reconcile roles independently from action grants

Priority: P2 for contract work. Confidence: high for absent roles; downstream impact remains conditional. Owner: unknown.
Location: [getUser](../../repos/ui/mfe-ratan-container/src/ratanutils/authenticator.ts#L6-L35).
Observation: [TC-FE-CES-005](06-test-cases.md#tc-fe-ces-005).

Old source path: `X_RATANONE.roleName` supplies a scalar role.
New input: the CES aggregate has no role name. `getUser().role` is unavailable.
[Saved views](../../repos/ui/mfe-ratan-container/src/ratancomponents/ViewSelector/store.ts#L21-L38) use role values for assignee and ownership filters.
[Saved filters](../../repos/ui/mfe-ratan-container/src/ratancomponents/FilterSelector/store.ts#L22-L39) also consume role values.
[Exception checks](../../repos/ui/mfe-ratan-container/src/ratanutils/authenticator.ts#L319-L335) contain `PSS_RO` restrictions.
No live API result establishes those downstream consequences.

The user confirms that roles are no longer unique. The original normalized login aggregate does not expose those names.
Next action: define multiple-role handling with BFF and CES assignment evidence.
Keep existing EMS2 scalar-role behavior unchanged.
The [later field decision](10-change-review-bff-entity-fields.md#proposed-change) selects `roleList` and `applicationId`.
Its scalar-role projection remains undecided. Earlier capture evidence does not contain the new metadata.
Do not select the first role, concatenate names, or invent a priority rule.
Do not derive `PSS_RO`, maker/checker, or admin roles from the effective action union.
The [admin role helper](../../repos/ui/mfe-base/src/admin/common/utils/index.ts#L3-L10) remains tied to `FMO PORTAL ADMIN`.
That entity remains EMS2 in this capture. Its CES migration requires coordinated backend authorization changes.

### FE-03: Align portal tile admission with the CES contract

Priority: P2 for supported configuration compatibility. Current sample impact is not demonstrated. Owner: unknown.
Location: [validateTile](../../repos/ui/mfe-base/src/utils/common.ts#L260-L311).
Cases: [TC-FE-CES-002](06-test-cases.md#tc-fe-ces-002) and [TC-FE-CES-003](06-test-cases.md#tc-fe-ces-003).

Old contract: drawer subjects and grants both use EMS2 subjects.
New contract: BFF authorizes `entitlement_app_feature`, but drawer `subject` still contains `ems2_subject`.
The [BFF drawer builder](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java#L208-L225) changes granted tile entities to CES app names.
The [portal validator](../../repos/ui/mfe-base/src/utils/common.ts#L265-L290) still requires a matching nonblank legacy subject.
[Direct launch](../../repos/ui/mfe-base/src/pages/Home/common/useParameters.ts#L66-L85) and workspace retention reuse that check.

All 41 captured CES tiles have matching, nonblank subjects. Their generic predicates succeed.
The base `X_RATANONE` occurrence is a legacy fallback, not this sample's failure cause.
A different or blank legacy subject can contradict a valid BFF CES grant.
Next action: branch inside the shared validator using the selected tile provider.
Keep EMS2 validation unchanged. Apply one reviewed CES decision across launch and workspace restoration.
For feature-controlled tiles, use current authorized drawer membership or an explicit normalized grant contract.
Deny tiles absent from the current authorized catalog. Reconcile template and blank-feature rules separately.

The candidate BFF bypasses CES lookup when the configured feature is blank.
That behavior can return a tile with empty entities. It is not approved by this source analysis.
The prior [empty-subject intent](../../knowledge/records/candidates/security/KT-sdk-and-entitlements.md#current-user-stated-empty-subject-rule) still requires an entitled configured entity.
CSV tile `192` is inactive and absent from this login. It does not establish a current login failure.
Do not expand blank-feature access until this policy difference is reconciled.

### FE-04: Add CES tile configuration and audit controls

Priority: P2. Confidence: high. Owner: unknown.
Locations: [tile editor](../../repos/ui/mfe-base/src/admin/Tile/common/useController.tsx#L232-L259) and [audit view](../../repos/ui/mfe-base/src/admin/Tile/common/useAudit.tsx#L124-L137).
Proposed validation: [TC-FE-CES-004](06-test-cases.md#tc-fe-ces-004).

Old UI: administrators configure legacy entity, subject, and ownership fields.
New BFF interfaces add `entitlementSource`, `entitlementAppId`, `entitlementAppName`, and `entitlementAppFeature`.
The current UI cannot create or change these CES routing values, or inspect them during checker review.
Next action: add all four fields to create, edit, detail, and audit controls.
Use display label `CES` with wire value `EMS3`. Supported wire values are `EMS2` and `EMS3`.
Match [backend validation](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/TileEntitlementConfig.java#L22-L74).
App ID is one value, limited to 64 characters.
App names and features support English-comma lists, limited to 512 characters each.
EMS3 requires app ID and app name. Blank features need the policy decision described above.

Existing fetched-row edits preserve hidden fields through whole-row spreading.
No current ordinary-edit source reset is established.
The BFF defaults an actually omitted source to EMS2. Retain explicit metadata round-trip assertions.
Backend CSV contracts also add four fields. Extend actual CSV consumers if identified.
No CSV UI was found in the inspected base TypeScript sources. No new CSV UI is required by this request.

### FE-05: Correct shared response types and provider propagation

Priority: P3 contract maintenance. Confidence: high. Owner: unknown.
Location: [response models](../../repos/ui/mfe-base/src/hooks/model/root.ts#L42-L80).

Old models require numeric identifiers, application names, and role names.
New CES entities, subjects, and actions carry null legacy identifiers.
Next action: model nullable fields inside provider adapters according to the actual response contract.
Preserve exported compatibility where callers need the existing normalized representation.
Add optional provider context to shared internals. Preserve it through route and container creation.
Avoid mandatory new upper-application props when the shared layer can supply the context.
Keep provider selection separate from the feature/action meaning and business ownership role.
The existing [login decoder](../../repos/ui/mfe-base/src/utils/login.ts#L65-L95) already accepts the normalized envelope.
No new login endpoint or frontend CES HTTP client is required.

### FE-06: Update analytics profile extraction

Priority: P3. Confidence: high for source behavior. Owner: unknown.
Location: [profile extraction](../../repos/ui/mfe-ratan-container/src/packages/Analysis/v2/User/utils.ts#L7-L44).
Old extraction searches entitlement-token keys for `X_RATANONE`.
The new key yields no profile through that lookup.
Next action: use the reviewed role/profile contract, or report profile unavailability explicitly.
No session disruption or analytics delivery failure was demonstrated.

## Scope and affected artifacts

| Artifact | Exact source identity | Risk and basis |
| --- | --- | --- |
| BFF baseline | `834b4155232222347220e47139a502ee43a9cbdf` | Baseline contract, read from local `main`. |
| BFF candidate | `d93455b6533bc017ab6bc42b0b585b804e1e96a1`, 5 November | High compatibility risk: authorization identities and tile semantics change. |
| Base | `4c36f8e14e3d9f178b226000ebbcb41aa611616a`, clean `main` | Conditional launch risk and confirmed admin management gaps. |
| Ratan container | Filesystem copy; [file hashes](evidence/frontend-entitlement-impact-20261105/ratan-container.json) | Confirmed local permission failures. Independent application revision is unknown. |
| Captures | [SHA-256 bindings](evidence/frontend-entitlement-impact-20261105/capture-summary.json) | One account and unspecified environment cannot establish enterprise coverage. |

All accountable implementation owners remain unknown.
The BFF review covers frontend-facing migration paths, not every change among the 54 changed paths.

## User impact

[FE-01](#fe-01-replace-identity-specific-shared-permission-dispatch) can disable granted business controls through a shared helper.
[FE-02](#fe-02-reconcile-roles-independently-from-action-grants) can change saved-content queries when role-dependent features are enabled.
[FE-03](#fe-03-align-portal-tile-admission-with-the-ces-contract) can make launch paths disagree for supported configuration boundaries.
[FE-04](#fe-04-add-ces-tile-configuration-and-audit-controls) prevents frontend management and review of CES routing.
Browser impact, frequency, forced logout, and deployed reachability remain unverified.
These observations establish no automatic production release hold.

## System impact

The BFF normalizes CES applications, features, and actions into the existing entity/subject/action envelope.
[Mapper evidence](evidence/frontend-entitlement-impact-20261105/bff-contract.json) binds old and new source hashes.
Migration modes permit mixed providers. Frontend permission resolution must preserve selected scope.
The [resolver boundary case](06-test-cases.md#tc-fe-ces-006) addresses duplicate rows and unrelated applications.
Static consumer inspection does not establish the deployed shared-module version or effective migration mode.

## Options and consequences

| Option | Consequence | Assessment |
| --- | --- | --- |
| Replace only the string `X_RATANONE`. | Can restore sample action lookup, but leaves roles, mixed scope, types, and admin gaps. | Insufficient migration scope. |
| Keep public APIs and add internal per-tile adapters. | Preserves callers while routing each tile to its selected provider. Roles retain an explicit exception. | Required design direction. |
| Require every upper application to use new permission arguments. | Moves provider details into consumers and increases migration changes. | Not selected by the user. |
| Add direct CES calls in each frontend. | Duplicates BFF responsibilities and adds unsupported interfaces. | No source-backed need. |

## Proposed acceptance and validation

The latest user decisions establish three scoped intent criteria in the [knowledge candidate](../../knowledge/records/candidates/security/KT-ces-migration-parity.md#frontend-compatibility-and-per-tile-migration).
Complete product AC inventory and business acceptance remain unresolved.
Case definitions do not establish implementation conformance or passing business execution.

### AC-to-test mapping

| Available intent or proposed boundary | Canonical cases | Assertion and execution state |
| --- | --- | --- |
| [FE-COMPAT-AC-001](../../knowledge/records/candidates/security/KT-ces-migration-parity.md#fe-compat-ac-001): preserve upper APIs. | [TC-FE-CES-007](06-test-cases.md#tc-fe-ces-007) | Compatibility integration `NOT_RUN`. |
| [FE-COMPAT-AC-002](../../knowledge/records/candidates/security/KT-ces-migration-parity.md#fe-compat-ac-002): per-tile provider routing. | [TC-FE-CES-006](06-test-cases.md#tc-fe-ces-006) | Provider isolation `NOT_RUN`. |
| [FE-COMPAT-AC-003](../../knowledge/records/candidates/security/KT-ces-migration-parity.md#fe-compat-ac-003): independent cutover and role boundary. | [TC-FE-CES-008](06-test-cases.md#tc-fe-ces-008), [TC-FE-CES-005](06-test-cases.md#tc-fe-ces-005) | Mixed-instance cutover `NOT_RUN`; scalar multiple-role semantics remain open. |
| Preserve scoped permission meaning. | [TC-FE-CES-001](06-test-cases.md#tc-fe-ces-001), [TC-FE-CES-006](06-test-cases.md#tc-fe-ces-006) | Original-module failure retained; cross-app boundary `NOT_RUN`. |
| Preserve reviewed tile admission. | [TC-FE-CES-002](06-test-cases.md#tc-fe-ces-002), [TC-FE-CES-003](06-test-cases.md#tc-fe-ces-003) | Capture predicates match; changed-feature integration `NOT_RUN`. |
| Manage CES metadata; preserve role attribution. | [TC-FE-CES-004](06-test-cases.md#tc-fe-ces-004), [TC-FE-CES-005](06-test-cases.md#tc-fe-ces-005) | Admin assertions unavailable; absent-role observation retained. |

### AC-to-code-change mapping

| Denominator | Mapping | Conformance limit |
| --- | --- | --- |
| Three sourced compatibility criteria; full product inventory remains unknown. | [Shared adapter design](#compatibility-principle-and-per-tile-routing) maps the proposed changes to existing surfaces. | No frontend implementation change exists. No conformance percentage applies. |
| Relevant existing BFF contract. | [BFF source and assertion map](evidence/frontend-entitlement-impact-20261105/bff-contract.json). | Implementation evidence does not approve blank-feature or role policy. |

### Code-change-to-test mapping

| Change population | Direct assertion evidence | Result |
| --- | --- | --- |
| New frontend application changes: 0. | None. | Empty denominator; not 100% coverage. |
| Inspected BFF migration interfaces. | Mapper, application-name, blank-feature, and tile-create assertions in [BFF evidence](evidence/frontend-entitlement-impact-20261105/bff-contract.json). | Assertions inspected; BFF suite `NOT_RUN`. |
| Required unchanged base paths. | [Nine existing tests](evidence/frontend-entitlement-impact-20261105/mfe-base-tests.json). | All pass. No captured CES assertion chain or complete-suite result. |

Definition, assertion, conformance, and passing execution remain separate.
Before acceptance, run equivalent EMS2/CES cases through login, renewal, direct launch, workspace restoration, and actual business controls.
Include denied actions, mixed providers, multiple applications, role-dependent APIs, and admin maker/checker round trips.

## Implementation and release proposal

Keep public API signatures and existing upper-application permission strings as the compatibility baseline.
Design internal per-tile provider binding, normalization, and the shared resolver first.
Add admin routing controls and unify the reviewed tile admission contract.
Resolve role multiplicity before changing role-dependent APIs or restrictions.
Update telemetry after the role/profile contract is known.
Verify the actual deployed import map and consuming microfrontends.
No implementation estimate, release date, or deployment authorization is supplied.

## Sources and evidence limits

- [Preserved request](evidence/frontend-entitlement-impact-20261105/user-input.md#exact-user-input).
- [Latest compatibility and per-tile decisions](evidence/frontend-entitlement-impact-20261105/user-clarification-20261106.md#exact-user-input).
- [Original database dump](<ces migration/application_tile_1105.csv>) and [login capture](<ces migration/login-response.json>).
- [Capture hashes and derived facts](evidence/frontend-entitlement-impact-20261105/capture-summary.json).
- [BFF contract and comparison identities](evidence/frontend-entitlement-impact-20261105/bff-contract.json).
- [Base source and assertions](evidence/frontend-entitlement-impact-20261105/mfe-base.json).
- [Container source, probe, and classifications](evidence/frontend-entitlement-impact-20261105/ratan-container.json).

Original supplied captures remain local and untracked. No token-bearing payload is added to this analysis commit.
Fresh checkouts need those supplied files to reproduce capture-dependent probes.
The probe substitutes the hooks store and executes no browser, backend API, or live authorization service.
Missing database tiles can reflect assignment or activity. They do not establish an entitlement defect.
No new business rule is inferred from the capture.
The latest user clarification updates intended migration knowledge. It does not supply passing implementation evidence.

### Knowledge update log

| Record | Intended meaning changed | Source and disposition |
| --- | --- | --- |
| [KT-ces-migration-parity](../../knowledge/records/candidates/security/KT-ces-migration-parity.md), version 1 → 2. | Preserve upper APIs, select providers per tile, and retain the non-unique-role boundary. | [User clarification](evidence/frontend-entitlement-impact-20261105/user-clarification-20261106.md#exact-user-input). Candidate and draft remain unchanged. |
| [KT-ces-migration-parity](../../knowledge/records/candidates/security/KT-ces-migration-parity.md), version 3 → 4. | Keep legacy team `applicationName: RATAN` separate from CES `name` and string ITAM ID. | [Identity clarification](evidence/frontend-entitlement-impact-20261105/user-clarification-application-identity-20261106.md#exact-user-input) and [sealed update checks](evidence/frontend-entitlement-impact-20261105/identity-knowledge-update-20261106.json). Candidate status remains. |
| Three compatibility criteria. | Define measurable mapped-call compatibility, provider isolation, and independent tile changes. | [FE-COMPAT-AC-001](../../knowledge/records/candidates/security/KT-ces-migration-parity.md#fe-compat-ac-001), [FE-COMPAT-AC-002](../../knowledge/records/candidates/security/KT-ces-migration-parity.md#fe-compat-ac-002), [FE-COMPAT-AC-003](../../knowledge/records/candidates/security/KT-ces-migration-parity.md#fe-compat-ac-003). Execution remains separate. |

The [knowledge update binding](evidence/frontend-entitlement-impact-20261105/knowledge-update-20261106.json) records the predecessor, source hash, successor, and audit event.
An independent agent read checked the revised intent against the preserved clarification.
That read supplies no human approval, publication, business acceptance, or completed ASD writing review.

## Unknowns and blockers

| Remaining dependency | Consequence | Owner and next action |
| --- | --- | --- |
| Multiple-role projection through existing scalar APIs. | Role-dependent implementation acceptance remains blocked. | unknown; obtain assignments and define role-consumer behavior. |
| Tile binding for identical features in simultaneous mixed-provider instances. | Complete unchanged-caller compatibility remains unproved. | unknown; design per-instance shared context and verify isolation. |
| Blank-feature admission versus existing configured-entity intent. | That access-policy decision remains unresolved. | unknown; reconcile policy before expanding admission. |
| Target builds, migration mode, import maps, and runtime evidence. | Deployed impact and full migration acceptance remain unverified. | unknown; bind actual UAT execution to exact artifacts. |

## Stage evidence and completion

Source inspection and compact capture analysis are complete within the declared scope.
The [container probe](evidence/frontend-entitlement-impact-20261105/ratan-container.json) confirms a local compatibility failure.
Its passing diagnostic assertions describe failing required permission behavior.
The [base test result](evidence/frontend-entitlement-impact-20261105/mfe-base-tests.json) records nine passing existing tests.
[Original document checks](evidence/frontend-entitlement-impact-20261105/validation.json) retain the prior analysis boundary.
[Compatibility refinement checks](evidence/frontend-entitlement-impact-20261105/compatibility-validation-20261106.json) validate the revised documents and source bindings.
Browser execution and complete applicable application suites remain `NOT_RUN`.

## Requested decision and actual disposition

Requested output: identify required changes in both frontends from the BFF migration and supplied captures.
Actual disposition: revised analysis follows the user's API compatibility and independent per-tile migration decisions.
Application implementation: unchanged. Intent review: sourced compatibility principles with role and instance-binding design limits.
Execution evidence retained: the prior helper probe, source-predicate analysis, and nine existing base tests.
The refinement added no application execution. New compatibility cases remain `NOT_RUN`.
Business acceptance, knowledge publication, and release authorization: pending and outside this analysis.
