---
artifact_kind: change-request
id: CR-CES-ZERO-UPPER-CHANGE-AUDIT
version: 2
status: draft
owner: unknown
source_refs: [USER-GAP-CLARIFICATION-20261109, CES-MIGRATION]
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
    - Source predictions and controlled probes do not establish deployed CES behavior.
---

# EMS2 to CES: compatibility gaps after clarification

> **The unresolved contract is the meaning of one scalar `getUser().role`.**
> Action: define the compatibility role and saved-item ownership rules before enabling affected role-dependent flows.
> Consequence: Cashflow profile requests, Trades confirmation menus, and Rules business-flow selection can change.
> Owner: business and backend owners unknown. Evidence: [role consumers](#role-dependent-upper-application-gaps).
>
> **Provider isolation is no longer a required upper-application change.**
> Action: simplify shared permission checks to accept mapped EMS2 or CES grants and log their source.
> Consequence: existing `hasPermission(code)` calls can remain unchanged. Current container code still enforces strict routing.
> Owner: shared container owner unknown. Source: [latest exact user clarification](evidence/frontend-entitlement-impact-20261105/user-gap-clarification-20261109.json).

## Request and source facts

Assessment: 9 November 2026. Confidence: HIGH for inspected source; deployed outcomes remain unverified.
The latest user clarification controls this assessment and supersedes earlier provider-isolation recommendations.
Readiness: `READY` for the requested source assessment and conditional Cashflow cleanup.
Other implementation remedies below remain proposed. This stage supplies no migration activation or deployment approval.

## Scope and affected artifacts

| Repository | Baseline | Inspected candidate or source |
| --- | --- | --- |
| mfe-base | `4c36f8e14e3d9f178b226000ebbcb41aa611616a` | `5295bd7ad66f62ee5cbb547f5aa5f6ef576c41d7` |
| mfe-ratan-container | Supplied snapshot `647e6b3e703e5144ab4b37c4b43aa22a28dfdd07`; PROD identity unknown | `72a446f1a6b2be4a44a4dad6df7c4c37530cae85` |
| single-ui-bff | `834b4155232222347220e47139a502ee43a9cbdf` | `95480c0e2563bc2a5a639bca1f22ecedb61936c2` |
| ratan-auth-server | `7e8cbfa49051ffcd4cd4aa87a6382edfaf8daaee` | `cacc4d218747e1591d5fb990eb5a8d8bcfb231a5` |
| single-ui-sdk-starter | `b0aa82005e7f14202f85f5ef583f25e42da9eeb3` | `0240b1c260337bf3c38f2b5ecaad2d1ec157296d` |
| Cashflow, Trades, Rules | Supplied filesystem snapshots; no independent Git history | File hashes in the [current source binding](evidence/frontend-entitlement-impact-20261105/gap-reassessment-validation-20261109.json) and linked case evidence |

Base, container, and BFF source remain on their existing delivery branches.
Cashflow cleanup changes two ignored snapshot files. The [retained patch](evidence/frontend-entitlement-impact-20261105/cashflow-unused-entitlements-20261109.patch) preserves those edits for delivery.
No nested repository was created. Parent Workbench commits do not identify consumer snapshot revisions.

## Sources and evidence limits

The linked reports retain exact source hashes and supplied-capture comparisons.
Direct inspection replaces the earlier stale graph for these consumers.
No live CES response or deployed business flow ran during this reassessment.

## Corrections to the earlier findings

| Earlier concern | Current classification | Source code and snippet | Consequence and required action |
| --- | --- | --- | --- |
| Mixed EMS2/CES `hasPermission` requires new upper scope parameters | Lower-layer simplification | [Container authenticator:199–229](../../repos/ui/mfe-ratan-container/src/ratanutils/authenticator.ts#L199-L229): `if (!target) return false;` and provider-specific dispatch | The user accepts either provider. Remove this restriction centrally and log the satisfying source. No upper argument or unused scope wiring is required. |
| All `X_RATANONE` tiles move, but its legacy entity might remain | User expectation confirmed within the configured BFF path | [BFF service:61–78](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/TileAuthorizationServiceImpl.java#L61-L78): `readEms2(userId, entitiesOf(ems2Scopes))`; [EMS2 implementation:38–40](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/implementation/EMS2AuthorizationImplementation.java#L38-L40): filters to requested names | In dual-read mode, no EMS2 tile requesting `X_RATANONE` means it is not requested or returned. `EMS3_ONLY` reads no EMS2 grants. `EMS2_ONLY` ignores tile migration choices and is an explicit exception. Other EMS2 entities can remain. |
| Cashflow shared selectors always use role ownership | Overstated; conditional configuration only | [View store:33–44](../../repos/ui/mfe-ratan-container/src/ratancomponents/ViewSelector/store.ts#L33-L44): role query or `owner: id`; [production config:23–41](../../repos/ui/mfe-ratan-container/src/ratanstatic/ratanConfig/production/ratanConfig.json#L23-L41) excludes Cashflow builder types | Supplied production config uses the private owner-ID view path for Cashflow. Its filters use a custom builder. No current Cashflow role-owned-selector failure is established. Runtime configuration remains unverified. |
| Cashflow entitlement feature flags break with CES objects | Unused support removed | [Cashflow controller:131–134](../../repos/ui/mfe-cashflow-blotter/src/Root/common/utils/featureFlagController.ts#L131-L134): `const { users } = settingsOfCurrentEnv \|\| {};` | All seven actual flags use booleans across eight environments. No production custom factory caller exists. Removed unused entitlement type, comments, branch, and obsolete synthetic test. Public function calls remain unchanged. |
| Rules entitlement feature flags require an API addition | Latent support; no active configuration | [Rules flags:26–100](../../repos/ui/mfe-rules/src/Root/common/utils/featureFlagController.ts#L26-L100): actual flags are booleans; generic `entitlements` branch is unused | No migration addition is required. Rules source remains unchanged. |
| Add `RATAN_ENTITLEMENT_RULE` beside `X_RATANONE` to fix Trades role parsing | Name alias alone is insufficient; helper is unused | [Trades helper:5–11](../../repos/ui/mfe-trades/src/utils/filter.ts#L5-L11): `.find(item => item.includes("X_RATANONE"))`; `.replace("X_RATANONE:", "")` | CES token key can be `RATAN_ENTITLEMENT_RULE:null`; recognizing that prefix does not recover `roleList`. No production caller exists in the supplied Trades snapshot. Add no unused compatibility code. Active confirmation-role logic remains a separate gap. |
| Rules maker/checker actions are lost in supplied CES login | No regression established for user 1481696 | [PROD EMS2:114–146](<api/PROD/[PROD] EMS2 entitlementList for user id (1481696).yml#L114-L146>), [PROD EMS2:654–687](<api/PROD/[PROD] EMS2 entitlementList for user id (1481696).yml#L654-L687>), [CES effective grants:284–329](<api/EMS3-user entitlements by app and user (1481696).yml#L284-L329>) | Both captures grant Rules entry access without initiate/verify actions. A broader catalog includes grants for other roles; it does not prove this user should receive them. Other assignments remain unverified. |
| Dashboard findings | Excluded by user scope | [Latest clarification, item 6](evidence/frontend-entitlement-impact-20261105/user-gap-clarification-20261109.json) | No dashboard change is proposed. No unused upper scope props are required. |

The [Cashflow audit](evidence/frontend-entitlement-impact-20261105/cashflow-unused-entitlements-audit-20261109.json) records configuration searches and cleanup checks.
The [Rules chain evidence](evidence/frontend-entitlement-impact-20261105/rules-subject-chain-20261109.json) records captures, source hashes, and the subject comparison.

## Role-dependent upper-application gaps

All rows describe source-derived consequences. None establishes deployed failure frequency.
Each owner is unknown unless a responsibility is named below.

| ID and category | Exact source and code snippet | Old versus CES behavior and concrete impact | Smallest resolution preserving callers | Upper source impact or warning |
| --- | --- | --- | --- | --- |
| R1: Shared scalar role contract | [Container:27–65](../../repos/ui/mfe-ratan-container/src/ratanutils/authenticator.ts#L27-L65): `dataEntitlementRoles \|\| role`, then `role = item.roleName` for `X_RATANONE` | EMS2 provides one business role. CES `roleList` does not populate that field. The returned scalar can be absent, stale, or a data category with different meaning. | Business/Auth owners must define an authoritative compatibility role. Keep business roles separate from data profiles. Expose the agreed scalar through the existing getter. | **WARNING: one string cannot represent arbitrary memberships tested by equality across disjoint legacy role lists. Zero API/source change cannot preserve full multi-role behavior generally.** |
| R2: Cashflow authorization-limit profile | [Role getter:1072–1074](../../repos/ui/mfe-cashflow-blotter/src/Cashflow_CN/components/CashflowDetails/MultiExceptions/common/utils.ts#L1072-L1074), [single request:683–695](../../repos/ui/mfe-cashflow-blotter/src/Cashflow_CN/components/CashflowDetails/MultiExceptions/hooks/useData.ts#L683-L695), [bulk checker:46–60](../../repos/ui/mfe-cashflow-blotter/src/Cashflow_CN/components/BulkFixExceptions/utils/filter.ts#L46-L60), [URL:128–133](../../repos/ui/mfe-cashflow-blotter/src/Cashflow_CN/services/index.ts#L128-L133): `profile: getUserRole()`; `${CHECK_AUTH_LIMIT}/${data.profile}/${data.currency}/${data.amount}` | One legacy profile selected the limit. Missing scalar constructs `/undefined/...`; joined roles construct an unrecognised profile. Single PendingVerification and bulk Checker authorization checks can fail. Backend result remains unexecuted. | Auth/profile owners must map the user to the existing trusted limit-profile identifier. Preserve the current API only if the mapping is valid. Backend must enforce the trusted policy. | **Active scalar consumer.** Zero Cashflow source change is conditional on a compatible profile. If several profiles require aggregation, the contract needs a backend policy or an application change. |
| R3: Trades View Confirmation | [Menu:352–383](../../repos/ui/mfe-trades/src/Trade/components/TradeDataGrid/common/RightClickMenuBuilder.tsx#L352-L383): `["FMO_MO_TV", "FMO_MO_TE", "FMO_MO_TV_SUP", "FMO_MO_TE_SUP"].includes(role)`; [active caller:147](../../repos/ui/mfe-trades/src/Trade/components/TradeDataGrid/common/BaseTradeDataGrid.tsx#L147) | A permitted legacy role offers the menu for eligible trade states. An absent, unrelated, or comma-joined scalar fails the allowlist and hides it. A CES action grant cannot bypass this local role test. | Supply an agreed legacy scalar centrally for supported users. Otherwise replace the local test with membership or an equivalent permission rule. | **Active upper logic.** If users need multiple incompatible role identities, shared getter changes alone cannot guarantee unchanged behavior. |
| R4: Rules business flows and defaults | [Role matching:3–19](../../repos/ui/mfe-rules/src/MoRules/utils/convert.ts#L3-L19), [defaults:22–89](../../repos/ui/mfe-rules/src/MoRules/utils/convert.ts#L22-L89), [page consumer:25–29](../../repos/ui/mfe-rules/src/MoRules/MoRulesHome.tsx#L25-L29): `element.role.includes(role)` and `role === "FMO_MO_TE"` | Legacy role selects local rule types and defaults. Missing/unmatched scalar removes role-restricted options and can produce empty business-flow/default values. Multiple roles cannot match as one joined value. | A reviewed scalar works only for the intended single-role behavior. Full multi-role union requires adapting local rule-config evaluation or an equivalent reviewed application contract. | **Active upper logic; strongest zero-change limit.** A scalar cannot select all disjoint allowed role sets without changing their meaning. |
| R5: Shared role-owned saved views/filters | [View reads:30–45](../../repos/ui/mfe-ratan-container/src/ratancomponents/ViewSelector/store.ts#L30-L45), [write hold:83–92](../../repos/ui/mfe-ratan-container/src/ratancomponents/ViewSelector/store.ts#L83-L92), [delete hold:125–141](../../repos/ui/mfe-ratan-container/src/ratancomponents/ViewSelector/store.ts#L125-L141), [Filter equivalents:31–46](../../repos/ui/mfe-ratan-container/src/ratancomponents/FilterSelector/store.ts#L31-L46), [new owner:44–52](../../repos/ui/mfe-ratan-container/src/ratancomponents/ViewSelector/common/useViewNameController.ts#L44-L52): `assignee: role, moduleOwner: role` | One legacy role identifies shared visibility and ownership. CES reads cannot represent every role. Enabled CES role-owned writes now reject with `CES role ownership is pending.` Known private operations can continue. Trades enables these builder types in supplied config. | Container/saved-item owners can query mapped role memberships centrally with backend support or validated fanout. Historical owner identifiers need a mapping. Existing records can retain their owner. New records still need an agreed owner rule. | **Shared-layer UI/API changes can be avoided.** Behavior remains reduced until ownership is agreed. Preserve the user's pending-write decision. Cashflow role-owned mode is conditional, not currently configured. |
| R6: Rules Dry Run role-owned reads and grouping | [Queries:91–110](../../repos/ui/mfe-rules/src/DryRunCenter/CreatePlan/common/utils.ts#L91-L110), [grouping:26–45](../../repos/ui/mfe-rules/src/DryRunCenter/CreatePlan/common/utils.ts#L26-L45), [schedule:119](../../repos/ui/mfe-rules/src/DryRunCenter/CreatePlan/PlanScheduleComp.tsx#L119): `assignee: role, moduleOwner: role`; `item.moduleOwner === role` | Shared filters are fetched and grouped using one role. Missing or different role names can omit shared items or misclassify ownership groups. These direct Rules reads do not acquire the shared selector's fix automatically. | Preserve one reviewed scalar, or adapt the shared HTTP/backend query projection and verify local grouping. Membership-aware grouping still needs local changes when several owners must match. | **Direct upper scalar dependency.** The selector write hold does not cover every custom Rules path. Full multi-role visibility/grouping cannot be promised with the unchanged scalar. |

### What saved-item ownership means

A private view belongs to a user ID. Its owner does not change when that user gains another role.
A role-shared view has an owner role and may be assigned to another role.
These are separate from the permission to open the builder.

Example setup: an old view has `moduleOwner="FMO_MO_TE"` and `assigneeList="FMO_MO_TV"`.

1. The user logs in with two CES entitlement names.
2. The application requests saved items using one `assignee` and one `moduleOwner`.
3. The user attempts to create a shared view.

Intended result: preserve agreed visibility and select an authorised owner for the new item.
Old result: the unique EMS2 role supplied those scalar fields.
Current CES result: no agreed scalar supplies membership or selects one owner.
A comma-joined name is a new owner key. It matches neither existing role.
Choosing the first CES role makes owner selection depend on response ordering.
An existing item's owner can remain unchanged, but new ownership still needs a decision.

This does not require every upper application to change its selector calls.
The shared container and saved-item backend can implement the eventual policy.
Rules' direct scalar comparisons remain an additional boundary.

## Remaining shared-layer and configuration gaps

| ID and category | Exact source and code snippet | Concrete impact and evidence limit | Resolution and upper application impact |
| --- | --- | --- | --- |
| S1: Permission routing exceeds the clarified requirement | [Container:153–229](../../repos/ui/mfe-ratan-container/src/ratanutils/authenticator.ts#L153-L229): conflicting targets resolve `undefined`; `if (!target) return false;` | A grant can be denied because provider routes conflict. CES without routing is also denied. No decision-source logging exists in this helper. Earlier controlled cases establish these predicates. | Implement EMS2-or-CES checks in the shared helper and record the satisfying provider/application/feature/action. Keep tile admission independent and preserve application identity. **No upper caller change. Proposed, not applied.** |
| S2: Settlement `PSS_RO` exclusion | [Container:278–282](../../repos/ui/mfe-ratan-container/src/ratanutils/authenticator.ts#L278-L282), [close:460–466](../../repos/ui/mfe-ratan-container/src/ratanutils/authenticator.ts#L460-L466), [replay:508–512](../../repos/ui/mfe-ratan-container/src/ratanutils/authenticator.ts#L508-L512): `if (target?.source === "EMS3") return false;` | CES CLIENT_DATA close/replay helpers deny before the grant check. No callers were found in Cashflow, Trades, or Rules. Other exported consumers remain unknown. | Business owner must define exclusion precedence or confirm CES action grants already enforce it. Change the shared helper only. **Conditional external-consumer warning; no required new upper API.** |
| S3: Portal administration scalar identity | [Base admin helper:3–10](../../repos/ui/mfe-base/src/admin/common/utils/index.ts#L3-L10), [BFF token:135–147](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L135-L147), [admin validation:53–65](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java#L53-L65): `entity.getName() + ":" + entity.getRoleName()` | Moving the separate FMO admin entity to CES can remove its scalar owner/token role. Admin actions can fail. Migrating `X_RATANONE` alone does not establish this trigger. FMO is outside the earlier production comparison scope. | Keep a trusted admin-role projection or migrate shared base/BFF admin checks together. **Conditional admin impact; no Cashflow/Trades/Rules source change.** |
| S4: Analytics profile | [Container analytics:38–44](../../repos/ui/mfe-ratan-container/src/packages/Analysis/v2/User/utils.ts#L38-L44): `extractProfileBySubject(entitlements, X_RATANONE)` | CES-only token keys produce an empty analytics profile. No user-flow failure is established. | Adapt shared telemetry labels to CES role data if needed. **Low impact; upper source unchanged.** |
| S5: Blank CES feature policy | [BFF bypass:181–190](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java#L181-L190), [base admission:13–18](../../repos/ui/mfe-base/src/utils/tileAdmission.ts#L13-L18): BFF bypasses blank feature authorization; base requires a nonblank route feature | Such a tile can appear in BFF drawers and disappear in the shell. This is an adapter/configuration mismatch. No need to change upper permission calls. | Define one shared blank-feature admission policy. Reject invalid config or align shell admission with the intended BFF bypass. Owners unknown. **Resolve centrally.** |
| S6: Duplicate legacy launch identity | [Base lookup:24–40](../../repos/ui/mfe-base/src/utils/drawer.ts#L24-L40): `matches.length === 1 ? matches[0] : undefined` | The same captured duplicate route selected the first tile before this adapter change and now returns no tile. [Controlled comparison](evidence/frontend-minimize-20261106/upper-launch-probe.json) confirms this for its bounded module case. No affected deployed upper caller was established. | Preserve existing legacy launch behavior centrally or resolve catalog duplicates without requiring new caller fields. **Adapter compatibility difference; conditional consumer impact. Dashboard analysis excluded.** |
| S7: Active workspace after grant refresh | [Base effect:284–300](../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L284-L300): `dispacthCurrentWorkspace(validWorkspaces[0])` | Added grant/catalog dependencies can select the first retained workspace even when the current workspace remains valid. This is source-predicted tab switching. | Preserve the current valid workspace during revalidation. **Shared shell fix; no upper API/source change.** |

These rows are migration implementation/configuration differences, not additional business-role semantics.
They do not justify unused upper scope arguments or wrappers.

## Backend compatibility audit

These checks supplement the UI audit. They do not establish every deployed backend consumer.
The [bounded backend recheck](evidence/frontend-entitlement-impact-20261105/backend-role-recheck-20261109.json) retains exact sources and limits.

| ID and category | Exact source and snippet | Problem and trigger | Resolution; upper source impact |
| --- | --- | --- | --- |
| B1: Staged rollout mode | [BFF:46–72](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/TileAuthorizationServiceImpl.java#L46-L72): `EMS3_ONLY` assembles `emptyResult()` for EMS2 | Selecting global CES-only mode while EMS2 tiles remain removes their grants. Dual-read already supports per-tile requests; missing backend support is not established. | Retain dual-read during staged migration. Use CES-only after remaining dependencies are reconciled. **Deployment configuration only; zero upper source change.** |
| B2: Auth JWT role projection | [Auth mapper:64–100](../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/entitlement/mapper/DefaultEms3EntitlementMapper.java#L64-L100): `throw new IllegalStateException("EMS3 maps to multiple roles")` | More than one distinct configured legacy role fails scalar mapping. Zero mapped roles also fail. Multiple CES names alone do not prove failure; current config maps only the common entitlement to `FMO_OPS_BOM`. | Define authoritative scalar projection or revise the backend JWT contract and its consumers. **UI adapters cannot fix a rejected authentication result. Multi-role warning is conditional on actual mappings.** |
| B3: Data profile/category meaning | [BFF DTO:37–50](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/filter/ems3/dto/Ems3DataEntitlementDto.java#L37-L50), [BFF projection:84–105](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/AuthorizationResultMapper.java#L84-L105), [Auth resolver:11–36](../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/entitlement/mapper/Ems3DataRoleResolver.java#L11-L36): `case "global" -> "Global"` | BFF entity projection does not return CES data policies/profiles. Auth recognises only Global/GBS/Onshore names and selects the first match. These are data categories, not business roles or proven Cashflow limit profiles. Blank data category does not necessarily fail JWT creation. | Preserve each intended profile meaning through a trusted backend mapping and retain structured data filters. **No frontend concatenation can recover discarded semantics. Existing caller compatibility depends on that mapping.** |
| B4: Valid empty grants versus login failure | [BFF mapper:35–45](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/AuthorizationResultMapper.java#L35-L45), [Auth mapper:47–52](../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/entitlement/mapper/DefaultEms3EntitlementMapper.java#L47-L52): empty `role_entitlements` throws | If valid no-grant or data-only users should retain portal/private access, they can fail login. If all such users must be denied entry, this can be intended. Captured assigned user does not settle the policy. | Distinguish a valid deny result from malformed/unavailable responses under the agreed login policy. **Backend-only fix possible; conditional compatibility warning.** |
| B5: Auth and BFF provider selection differ | [Auth facade:36–65](../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/migration/EntitlementMigrationFacade.java#L36-L65): provider chosen by user/mode; no tile ID | A user's BFF can retain EMS2 tile grants while their JWT already uses CES actions/data. Actual failure needs an assignment mismatch. Auth `EMS3_ONLY` still leaves non-allowlisted users on EMS2. | Reconcile backend grants for all usable tiles or implement the accepted provider union/routing centrally. **Rollout/backend work; upper UI source can remain unchanged.** |
| B6: SDK token and mapping prerequisites | [SDK constructor/check:38–61](../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImpl.java#L38-L61), [Spring wiring:41–50](../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/config/AuthConfiguration.java#L41-L50): no `FmaaTokenProvider` returns an empty map | Existing calls still compile but lose entitlements if the provider, CES URL, or mappings are missing. No deployed manual-constructor consumer was established. | Supply shared token-provider wiring and CES configuration. **Avoidable caller change; deployment configuration is required.** |
| B7: SDK role-alias collapse | [SDK validation:146–148](../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImpl.java#L146-L148), [key build:174–188](../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImpl.java#L174-L188) | SDK supports several `entity:role` keys. It rejects distinct roles collapsing into one configured legacy key. Earlier blanket claims that all multiple roles fail were too broad. | Only if the approved policy needs a many-to-one alias, merge mapped grants centrally. **Conditional SDK mapping gap; no such deployed mapping verified.** |

Malformed catalog IDs can fail BFF route construction at [EntitlementRouting:29](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/EntitlementRouting.java#L29).
This is invalid-input hardening, not an unavoidable contract break for valid rows. Validate catalog IDs before activation.
Nullable legacy IDs are metadata differences. No active numeric-ID entitlement consumer was found in these three upper snapshots.
Do not fabricate EMS2 IDs to fill CES fields.

## Rules ems2Subject: complete answer

The prop name can remain. It identifies an existing permission prefix; it does not query the database.

| Route and database tile | Existing Rules code | CES feature | Compatibility result |
| --- | --- | --- | --- |
| MO Rules, tile 35 | [Root:55](../../repos/ui/mfe-rules/src/Root/routing/index.tsx#L55): `<MORule ems2Subject="MO_RULE" page="MO_RULE" />` | `RATAN_MO_RULE` | Compatible with supplied CES configuration. |
| CA Rules, tile 114 | [Root:59](../../repos/ui/mfe-rules/src/Root/routing/index.tsx#L59): `<MORule ems2Subject="MO_RULE" page="CA_RULE" />` | `RATAN_MO_RULE` | Compatible with current configuration. Changing only the database feature to `RATAN_CA_RULE` leaves actions checking MO grants. CA-only grants would be ignored; MO grants could still permit actions. |
| FM COO Rules, tile 104 | [Root:63](../../repos/ui/mfe-rules/src/Root/routing/index.tsx#L63): `<MORule ems2Subject="FM_COO_RULE" />` | `RATAN_FM_COO_RULE` | Compatible with supplied CES configuration. |

[Rules:83–92](../../repos/ui/mfe-rules/src/MoRules/Routing.tsx#L83-L92) constructs the same feature names:

```ts
hasPermission(`RATAN_${ems2Subject}:F_Input_Delete_Modify_Initiate`)
hasPermission(`RATAN_${ems2Subject}:F_Input_Delete_Modify_Verify`)
```

[BFF routing:33–52](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/EntitlementRouting.java#L33-L52) reads `entitlement_app_feature` for CES.
It reads `ems2_subject` only for EMS2 routes.
[BFF mapping:61–66](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/AuthorizationResultMapper.java#L61-L66) copies the CES feature and action into subjects/actions.
Therefore, clearing the database EMS2 subject on CES tiles does not remove these frontend constants or permission names.
Preserve the existing feature/action vocabulary in CES or map aliases centrally.
Do not rename the prop solely because its name contains EMS2.

## Proposed change

The following is a proposal, not the current implementation:

```ts
// Preserve the existing public call.
export const hasPermission = (code: string): boolean => {
  const ems2 = legacyHasPermission(code);
  const ces = cesHasPermission(code); // matching mapped app, feature, and action
  recordPermissionSource(code, { ems2, ces });
  return ems2 || ces;
};
```

`cesHasPermission` and `recordPermissionSource` above are illustrative names, not new API commitments.
Retain the original EMS2 aliases and validate CES grants within the corresponding application.
Log decision metadata through existing logging facilities. Do not log complete tokens or entitlement payloads.
Keep independent tile admission through each tile's configured provider.
No consumer must adopt `createAuthenticator`, receive a new scope prop, or read an unused role-list API.

**Unresolved warning:** this permission adaptation does not repair scalar role, saved-item owner, or limit-profile semantics.
No shared helper can infer those business decisions from a list's ordering or comma formatting.

## Options and consequences

A reviewed scalar compatibility mapping preserves callers only for its supported role combinations.
Supporting arbitrary multi-role membership requires changing scalar consumer semantics or their contract.
Retain pending role-owned writes until the ownership decision is supplied.

## Implementation and release proposal

Only the unused Cashflow feature-flag cleanup is applied in this stage.
Provider-union implementation, role mappings, and backend remedies remain proposals.
Stage and ship shared changes on delivery branches after their applicable checks pass.
No deployment recommendation or authorization is supplied here.

## Unknowns and blockers

Scalar business roles, Cashflow limit-profile aggregation, and new role-owned item selection remain unresolved.
These block claims of complete compatibility for the affected flows, rather than this bounded assessment.
Business/backend ownership and actual deployed configuration remain unknown.

## Requested decision and actual disposition

The user requested a source-backed gap table and conditional unused-code removal.
Both are complete within the stated evidence boundary.
The existing ownership hold remains effective. No additional business answer is inferred.

## Proposed acceptance and validation

The candidate [FE-COMPAT-AC-004](../../knowledge/candidates/security/KT-ces-migration-parity.md#fe-compat-ac-004) defines the newly clarified permission rule.
It includes all four EMS2/CES grant combinations and accepted-decision source logs.
Historical strict-routing cases do not test conformance to this revised rule.

| Coverage relation | Declared denominator | Current evidence and gap |
| --- | --- | --- |
| AC to test | Four grant-union examples in FE-COMPAT-AC-004 | Four criterion examples are defined; zero current executable assertions establish the revised rule. Implementation tests remain required. |
| AC to code change | One grant-union criterion | Zero implementation changes in this stage satisfy it. Current strict dispatch remains a documented gap. |
| Code change to test | One Cashflow production unit changed; no new business behavior | Existing retained users/env tests inspect this unit. The actual-config probe asserts 112 before/after outcomes and cached results. Broader app execution remains unavailable. |

These denominators describe this reassessment only. They do not replace historical coverage or prove full migration conformance.
The Cashflow removal implements the user's cleanup instruction; it adds no entitlement behavior.

## Verification and completion

| Check | Result | Scope and limit |
| --- | --- | --- |
| Source and supplied-capture audit | Complete within named snapshots | [Roles](evidence/frontend-entitlement-impact-20261105/role-ownership-reassessment-20261109.json), [Rules chain](evidence/frontend-entitlement-impact-20261105/rules-subject-chain-20261109.json), [backend](evidence/frontend-entitlement-impact-20261105/backend-role-recheck-20261109.json). Predictions remain separate from live observations. |
| Cashflow focused checks | Baseline 3/3; retained candidate 2/2 passed | Removed one obsolete entitlement-only test with the deleted feature. Isolated getUser/getEnv mocks and borrowed Jest runtime are disclosed. |
| Actual Cashflow configuration comparison | 112 cases passed; 448 assertions | Seven flags, eight environments, two user entitlement shapes. Actual configured outputs and cached results match before/after. |
| Complete Cashflow Jest setup | BLOCKED before tests | Available runtime lacks `ag-grid-react`. No full-suite passing claim. |
| Broader shared/frontend/backend suites | Not rerun for this source assessment | Shared source is unchanged. Earlier controlled executions retain their original revisions and limits. |
| Live CES, saved-item backend, and deployed consumer parity | NOT_RUN | No enterprise execution or production acceptance claim. |
| Documentation and provenance checks | See [current validation](evidence/frontend-entitlement-impact-20261105/gap-reassessment-validation-20261109.json) | Source/line/link/hash/lint checks do not establish business behavior. |

The [independent source review](evidence/frontend-entitlement-impact-20261105/independent-gap-review-20261109.json) checked material findings.
Its CA-feature wording correction is applied here; the earlier evidence retains its historical wording.
The [stage record](10-change-review-frontend-adapters.md#upper-application-impact) links this living assessment.
The candidate knowledge update records the clarified permission rule separately from implementation status.
Owners must still resolve scalar-role and new-item ownership semantics. No new policy answer is inferred from a continuation request.
