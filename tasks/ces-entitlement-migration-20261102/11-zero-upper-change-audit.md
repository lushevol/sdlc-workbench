---
artifact_kind: change-request
id: CR-CES-ZERO-UPPER-CHANGE-AUDIT
version: 3
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
> **The shared compatibility optimization is applied.**
> Existing `hasPermission(code)` calls accept valid EMS2 or mapped CES grants and record the decision path.
> No new upper scope/facade API is required. Legacy duplicate launches, valid active-workspace retention, and blank-feature tile admission are reconciled centrally.
> Source: [latest exact user clarification](evidence/frontend-entitlement-impact-20261105/user-gap-clarification-20261109.json) and the applied evidence below.

## Request and source facts

Updated: 10 November 2026. Confidence: HIGH for inspected source; deployed outcomes remain unverified.
The latest user clarification controls this assessment and supersedes earlier provider-isolation recommendations.
The base/container optimization is applied on delivery branches. Role mappings and backend remedies remain proposed.
The [applied source review](/Users/lushevol/Documents/Codex/2026-11-10/do-you-want-to-optimize-mfe/applied-optimization-review.json) binds inspected hashes and reports no actionable findings within its declared scope.
The [base optimization results](/Users/lushevol/Documents/Codex/2026-11-10/do-you-want-to-optimize-mfe/base-optimization-results.json) bind changed source and local test limits.
This stage supplies no migration activation or deployment approval.

## Scope and affected artifacts

| Repository | Baseline | Inspected candidate or source |
| --- | --- | --- |
| mfe-base | `4c36f8e14e3d9f178b226000ebbcb41aa611616a` | Squashed delivery `10560f39a57e8ce4010cee634f7682559b1a6bdd`; same verified source bytes |
| mfe-ratan-container | Supplied snapshot `647e6b3e703e5144ab4b37c4b43aa22a28dfdd07`; PROD identity unknown | Squashed delivery `a7e38d048545dd913ae5996a1475980056de18bd`; same verified source bytes |
| single-ui-bff | `834b4155232222347220e47139a502ee43a9cbdf` | `95480c0e2563bc2a5a639bca1f22ecedb61936c2` |
| ratan-auth-server | `7e8cbfa49051ffcd4cd4aa87a6382edfaf8daaee` | `cacc4d218747e1591d5fb990eb5a8d8bcfb231a5` |
| single-ui-sdk-starter | `b0aa82005e7f14202f85f5ef583f25e42da9eeb3` | `0240b1c260337bf3c38f2b5ecaad2d1ec157296d` |
| Cashflow, Trades, Rules | Supplied filesystem snapshots; no independent Git history | File hashes in the [current source binding](evidence/frontend-entitlement-impact-20261105/gap-reassessment-validation-20261109.json) and linked case evidence |

Base, container, and BFF source remain on their existing delivery branches.
The [internal patch bundle](delivery/20261110-frontend-optimization/README.md) exports both complete frontend migrations, including tests, from these exact baselines.
Each patch reproduces the amended target tree in a temporary Git index. Main refs and BFF source remain unchanged.
Cashflow cleanup changes two ignored snapshot files. The [retained patch](evidence/frontend-entitlement-impact-20261105/cashflow-unused-entitlements-20261109.patch) preserves those edits for delivery.
No nested repository was created. Parent Workbench commits do not identify consumer snapshot revisions.

## Sources and evidence limits

The linked reports retain exact source hashes and supplied-capture comparisons.
Direct inspection replaces the earlier stale graph for these consumers.
No live CES response or deployed business flow ran during this reassessment.

## Corrections to the earlier findings

| Earlier concern | Current classification | Source code and snippet | Consequence and required action |
| --- | --- | --- | --- |
| Mixed EMS2/CES `hasPermission` requires new upper scope parameters | Resolved in shared adapter | [Container authenticator:168–205](../../repos/ui/mfe-ratan-container/src/ratanutils/authenticator.ts#L168): `const allowed = legacy \|\| !!ces;` | An EMS2 grant or complete mapped CES grant now suffices. Decision-path logging is applied. No new upper argument, scope prop, or facade is required. |
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
| R1: Shared scalar role contract | [Container:24–66](../../repos/ui/mfe-ratan-container/src/ratanutils/authenticator.ts#L24): `dataEntitlementRoles \|\| role`, then `role = item.roleName` for `X_RATANONE` | EMS2 provides one business role. CES `roleList` does not populate that field. The returned scalar can be absent, stale, or a data category with different meaning. | Business/Auth owners must define an authoritative compatibility role. Keep business roles separate from data profiles. Expose the agreed scalar through the existing getter. | **WARNING: one string cannot represent arbitrary memberships tested by equality across disjoint legacy role lists. Zero API/source change cannot preserve full multi-role behavior generally.** |
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
| S1: Permission routing and source tracking | [Container:168–205](../../repos/ui/mfe-ratan-container/src/ratanutils/authenticator.ts#L168): `const allowed = legacy \|\| !!ces;`; [logging:150–165](../../repos/ui/mfe-ratan-container/src/ratanutils/authenticator.ts#L150): `logger.info(message)` | **Resolved adapter difference.** Provider conflicts no longer force denial. CES still needs matching application ID, entity name, feature, and action. Logs identify checked path, code, result, and CES application ID when used; repeated identical snapshot/user decisions are deduplicated. | **No upper caller change. Applied.** Independent tile admission remains. Existing UAT HTTP log suppression remains; logs do not independently prove upstream provenance. Permissions are recalculated even when logs are deduplicated. |
| S2: Settlement `PSS_RO` exclusion | [Container:253–264](../../repos/ui/mfe-ratan-container/src/ratanutils/authenticator.ts#L253), [close:443](../../repos/ui/mfe-ratan-container/src/ratanutils/authenticator.ts#L443), [replay:491](../../repos/ui/mfe-ratan-container/src/ratanutils/authenticator.ts#L491): `return !ces && getUser().role !== "PSS_RO";` | CES CLIENT_DATA close/replay remains pending even with an action grant. Matching CES/mixed targets deny; absent/empty routing with CES data stays conservative. Explicit matching EMS2-only routes retain the legacy role test. No callers were found in Cashflow, Trades, or Rules; other exported consumers remain unknown. | Business owner must define exclusion precedence or confirm CES action grants enforce it. **Conditional external-consumer warning; no required new upper API.** The grant-union change does not resolve this role policy. |
| S3: Portal administration scalar identity | [Base admin helper:3–10](../../repos/ui/mfe-base/src/admin/common/utils/index.ts#L3-L10), [BFF token:135–147](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L135-L147), [admin validation:53–65](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java#L53-L65): `entity.getName() + ":" + entity.getRoleName()` | Moving the separate FMO admin entity to CES can remove its scalar owner/token role. Admin actions can fail. Migrating `X_RATANONE` alone does not establish this trigger. FMO is outside the earlier production comparison scope. | Keep a trusted admin-role projection or migrate shared base/BFF admin checks together. **Conditional admin impact; no Cashflow/Trades/Rules source change.** |
| S4: Analytics profile | [Container analytics:38–44](../../repos/ui/mfe-ratan-container/src/packages/Analysis/v2/User/utils.ts#L38-L44): `extractProfileBySubject(entitlements, X_RATANONE)` | CES-only token keys produce an empty analytics profile. No user-flow failure is established. | Adapt shared telemetry labels to CES role data if needed. **Low impact; upper source unchanged.** |
| S5: Blank CES feature admission | [BFF bypass:181–190](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java#L181-L190), [base admission:1–15](../../repos/ui/mfe-base/src/utils/tileAdmission.ts#L1): `return routes.length === 1 && routes[0].source === "EMS3";` | **Resolved adapter difference.** Base admits the current server-authorized tile with one matching EMS3 route, including BFF-authorized blank-feature tiles. It does not add a local nonblank-feature restriction. CES action checks still require full feature/action identity. | **Applied centrally; no upper source change.** This preserves the existing BFF policy and does not establish live tile-catalog acceptance. |
| S6: Duplicate legacy launch identity | [Base lookup:40–43](../../repos/ui/mfe-base/src/utils/drawer.ts#L40): `matches.every((tile) => tile.entitlementSource !== "EMS3")`; [named dispatch:125](../../repos/ui/mfe-base/src/hooks/dispathcer/index.ts#L125) | **Resolved adapter difference.** All-EMS2 duplicate restore, named launch, accessibility, and Cashflow launch retain first-match behavior. Ambiguous matches involving CES and duplicate database IDs still deny. The earlier [controlled comparison](evidence/frontend-minimize-20261106/upper-launch-probe.json) is historical pre-fix evidence. | **Applied centrally; no new upper caller fields.** CES/mixed ambiguity remains a catalog/identity constraint; no affected deployed caller has been established. Dashboard analysis remains excluded. |
| S7: Active workspace after grant refresh | [Base effect:294–300](../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L294): `workspace.id === store.currentWorkspace?.id` | **Resolved adapter difference.** Revalidation retains the active workspace if still valid and selects the first valid workspace only when the active one is withdrawn. | **Applied shared-shell fix; no upper API/source change.** Local assertions do not establish deployed session-refresh parity. |

Rows S1, S5, S6, and S7 are now resolved shared-adapter differences. Rows S2–S4 retain their stated policy, configuration, or telemetry limits.
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

## Applied shared change

The public `hasPermission(code): boolean` call is unchanged. Its implementation now returns an existing legacy grant or a complete mapped CES grant:

```ts
const legacy = legacyHasPermission(code);
// Otherwise match CES application ID, entity name, feature, and action.
const allowed = legacy || !!ces;
logPermission(store, {
  code,
  source: legacy ? "EMS2" : ces ? "EMS3" : "NONE",
  ...(ces ? { applicationId: ces.applicationId } : {}),
  allowed,
});
return allowed;
```

The [source:168–205](../../repos/ui/mfe-ratan-container/src/ratanutils/authenticator.ts#L168) retains EMS2 aliases and CES application identity.
Logs contain decision metadata, not complete tokens or entitlement payloads. Existing environment delivery limits still apply.
Independent tile admission follows each tile's configured provider.
Unused `createAuthenticator`, scope types, and mount props are removed; upper callers retain their existing API.

**Unresolved warning:** this permission adaptation does not repair scalar role, saved-item owner, PSS exclusion, or limit-profile semantics.
No shared helper can infer those business decisions from a list's ordering or comma formatting.

## Options and consequences

A reviewed scalar compatibility mapping preserves callers only for its supported role combinations.
Supporting arbitrary multi-role membership requires changing scalar consumer semantics or their contract.
Retain pending role-owned writes until the ownership decision is supplied.

## Implementation and release proposal

The unused Cashflow feature-flag cleanup and the bounded base/container optimization are applied.
Role mappings and backend remedies remain proposals.
Shared changes remain on delivery branches for review and applicable validation.
No deployment recommendation or authorization is supplied here.

## Unknowns and blockers

Scalar business roles, Cashflow limit-profile aggregation, and new role-owned item selection remain unresolved.
These block claims of complete compatibility for the affected flows, rather than this bounded assessment.
Business/backend ownership and actual deployed configuration remain unknown.

## Requested decision and actual disposition

The user requested a source-backed gap table, conditional unused-code removal, and minimal shared-adapter optimization.
The source assessment and bounded implementation are complete within the linked evidence boundary; the [final optimization results](/Users/lushevol/Documents/Codex/2026-11-10/do-you-want-to-optimize-mfe/optimization-results.json) bind execution to source hashes. No optimization commits were created; main remains untouched.
The existing ownership hold remains effective. No additional business answer is inferred.

## Proposed acceptance and validation

The candidate [FE-COMPAT-AC-004](../../knowledge/candidates/security/KT-ces-migration-parity.md#fe-compat-ac-004) defines the newly clarified permission rule.
It includes all four EMS2/CES grant combinations and accepted-decision source logs.
Historical strict-routing cases do not test conformance to this revised rule.

| Coverage relation | Declared denominator | Current evidence and gap |
| --- | --- | --- |
| AC to test | Four grant-union examples in FE-COMPAT-AC-004 | Current [resolver assertions](../../repos/ui/mfe-ratan-container/src/ratanutils/authenticator.ces.test.ts) cover the grant combinations, decision-source logs, invalid chains, deduplication, and logger failure. The [real-logger test](../../repos/ui/mfe-ratan-container/src/ratanutils/authenticator.logging.test.ts) checks integration with mocked transport. Review is linked above; 84/84 focused container checks passed across nine suites in the [final optimization results](/Users/lushevol/Documents/Codex/2026-11-10/do-you-want-to-optimize-mfe/optimization-results.json). The full owning container build remains unrun. |
| AC to code change | One grant-union criterion | Applied in [hasPermission](../../repos/ui/mfe-ratan-container/src/ratanutils/authenticator.ts#L168) with decision-path logging and preserved CES identity. No new upper argument or scalar-role policy. |
| Code change to test | Bounded base/container optimization plus earlier Cashflow cleanup | [Base evidence](/Users/lushevol/Documents/Codex/2026-11-10/do-you-want-to-optimize-mfe/base-optimization-results.json) maps mount, duplicate-launch, workspace-refresh, and blank-feature assertions. Container assertions and source review are linked above. Earlier Cashflow probes retain their original boundary. Broader app/live execution remains unavailable. |

These denominators describe the bounded shared rule and source assessment only. They do not replace historical coverage or prove full migration conformance.
The Cashflow removal implements the user's cleanup instruction; it adds no entitlement behavior.

## Verification and completion

| Check | Result | Scope and limit |
| --- | --- | --- |
| Source and supplied-capture audit | Complete within named snapshots | [Roles](evidence/frontend-entitlement-impact-20261105/role-ownership-reassessment-20261109.json), [Rules chain](evidence/frontend-entitlement-impact-20261105/rules-subject-chain-20261109.json), [backend](evidence/frontend-entitlement-impact-20261105/backend-role-recheck-20261109.json). Predictions remain separate from live observations. |
| Cashflow focused checks | Baseline 3/3; retained candidate 2/2 passed | Removed one obsolete entitlement-only test with the deleted feature. Isolated getUser/getEnv mocks and borrowed Jest runtime are disclosed. |
| Actual Cashflow configuration comparison | 112 cases passed; 448 assertions | Seven flags, eight environments, two user entitlement shapes. Actual configured outputs and cached results match before/after. |
| Complete Cashflow Jest setup | BLOCKED before tests | Available runtime lacks `ag-grid-react`. No full-suite passing claim. |
| Applied base optimization | 515/515 full-suite tests across 130 suites; final mount checks 9/9; full base TypeScript passed | Production was unchanged after the full suite. See [final optimization results](/Users/lushevol/Documents/Codex/2026-11-10/do-you-want-to-optimize-mfe/optimization-results.json); the base runner used `--forceExit` after all declared tests completed because open handles remain. |
| Applied container optimization | 84/84 focused tests across nine suites; selected types passed | Actual logger tested with transport mocked. Borrowed runtime used offline cache-verified `loglevel` through Jest `--modulePaths`; selected typing used an explicit logger declaration. Full owning container build was not run. |
| Current browser and portal | 16/16 shared-module checks; 4/4 portal checkpoints; source hashes verified | Services remain synthetic. Historical strict-provider results retain their original source and policy limits. |
| Live CES, saved-item backend, and deployed consumer parity | NOT_RUN | No enterprise execution or production acceptance claim. |
| Documentation and provenance checks | [Historical 9 November validation](evidence/frontend-entitlement-impact-20261105/gap-reassessment-validation-20261109.json); current report checks remain separate | Earlier source/line/link/hash/lint checks retain their original revisions and do not establish business behavior. |

The [independent source review](evidence/frontend-entitlement-impact-20261105/independent-gap-review-20261109.json) checked material findings.
Its CA-feature wording correction is applied here; the earlier evidence retains its historical wording.
The [stage record](10-change-review-frontend-adapters.md#upper-application-impact) links this living assessment.
The candidate knowledge update records the clarified permission rule. The applied shared source now implements that union rule; it does not add a scalar-role or ownership policy.
Owners must still resolve scalar-role and new-item ownership semantics. No new policy answer is inferred from a continuation request.
