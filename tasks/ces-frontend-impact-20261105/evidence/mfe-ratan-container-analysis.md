---
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
    - Automated checks do not check the complete approved dictionary or grammar rules.
---

# MFE Ratan Container CES impact

> **Critical conclusions: Update permission lookup before using CES application entities. Resolve role-dependent behavior before retiring EMS2 roles.**
> Owner: unknown. Next action: agree the scoped permission and profile contracts, then implement the adapters.
> Consequence: valid actions can disappear; saved filters and views can lose their role association.
> Evidence: [BFF application naming](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/TileAuthorizationServiceImpl.java:155) and [container lookup](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/ui/mfe-ratan-container/src/ratanutils/authenticator.ts:38).

## Scope and identities

The [user request](user-input.md#exact-user-input) authorizes impact analysis.
Application files remain unchanged.

- BFF base: `834b4155232222347220e47139a502ee43a9cbdf`, local `main`.
- BFF candidate: `267081800cc28b6af0f8e080fa67c2d5f14d3a26`.
- Container identity: filesystem copy; no independent `.git` directory or baseline commit exists.
- The parent Workbench commit is not the container revision.
- [Source hashes](container-source-hashes.json) identify all claim-bearing inspected files.
- Application suites and live execution: `NOT_RUN`. The parent retained controlled helper probes separately.

## Provider contract

The BFF retains the `entities -> subjects -> actions` response structure.
CES changes the identities and optional metadata inside that structure.

| Field | BFF main | BFF candidate | Source |
| --- | --- | --- | --- |
| `entity.name` | EMS2 entity, such as `X_RATANONE`. | Configured CES application name. | [application mapper call](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/TileAuthorizationServiceImpl.java:155) |
| `subject.name` | EMS2 subject. | CES `role_entitlements[].feature`. | [subject mapping](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/AuthorizationResultMapper.java:74) |
| `subject.entitlementSource` | Unavailable in the old DTO. | `EMS3` for mapped CES subjects. | [source marker](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/AuthorizationResultMapper.java:77) |
| `action.name` | EMS2 action. | CES `role_entitlements[].action`. | [action mapping](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/AuthorizationResultMapper.java:80) |
| Role and numeric IDs | EMS2 supplies role names and IDs. | The mapper does not assign them. | [complete entity mapping](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/AuthorizationResultMapper.java:72) |
| Token entitlement key | `entityName:roleName`. | The same serializer produces `appName:null` when the role is absent. | [token serializer](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java:131) |

CES data policies, profiles, and entitlement names do not become frontend profile fields in this mapper.
The source marker exists on response subjects; token serialization drops that marker.

## Required work

### RC-01: Resolve permissions by application, feature, and action

**High confidence: the current lookup cannot support general CES application names.**

[getUser](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/ui/mfe-ratan-container/src/ratanutils/authenticator.ts:15) builds a map keyed by `entity.name`.
[hasPermission](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/ui/mfe-ratan-container/src/ratanutils/authenticator.ts:56) searches `X_RATANONE` first and returns immediately when that entity exists.
Its fallback requires an entity name that contains the requested subject.
A CES application name need not contain its feature name.

Setup: compare equivalent permissions from EMS2 and CES.

1. Request `RATAN_TRADE_BLOTTER:F_Export_Data`.
2. Supply EMS2 entity `X_RATANONE` with that subject and action.
3. Supply CES entity `RATAN` with the same feature and action.

- Intended result: preserve the granted action for the correct application.
- Old source prediction: `true`, through the `X_RATANONE` branch.
- New source prediction: `false`, because `RATAN` does not contain `RATAN_TRADE_BLOTTER`.
- User consequence: controls can remain hidden or disabled despite a valid CES grant.
- Owner: unknown. Next action: add a source-aware permission adapter and preserve exact action matching.

Inspect the current application's CES entity before legacy fallback.
Pass or obtain the application scope through a shared Base contract.
Keep legacy behavior for EMS2 subjects.
Do not grant an action from an unrelated application's matching feature.

The current container props contain `module` and `tile`, without an entitlement application identifier.
See [ContainerProps](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/ui/mfe-ratan-container/src/Root/routing/common/interface.ts:1).
The container imports shared hooks from [@fm/base](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/ui/mfe-ratan-container/src/Root/import/index.ts:1).
Coordinate this scope contract with `mfe-base`.

### RC-02: Preserve grants during mixed migration

**High confidence: current normalization and early returns can discard or shadow grants.**

[normalization](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/ui/mfe-ratan-container/src/ratanutils/authenticator.ts:17) replaces the previous map for each repeated entity name.
The BFF combines EMS2 and CES entities in [assemble](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/TileAuthorizationServiceImpl.java:75).
CES results from different app IDs can also share an application name.

The `X_RATANONE` early return prevents fallback when its subject lacks an action.
A separate CES entity with that action is ignored.

Owner: unknown. Next action: retain application identity and source during normalization.
Merge only grants whose source and application scope are equivalent.
Test both entity orders and legacy denial followed by CES grant.
An unscoped union across all applications can create a new authorization error.

### RC-03: Resolve role-dependent filters, views, and exception gates

**High confidence: current consumers require a role that CES mapping does not provide.**

[role extraction](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/ui/mfe-ratan-container/src/ratanutils/authenticator.ts:11) reads the old token role or exact `X_RATANONE.roleName`.
A pure CES result usually leaves that role undefined.

| Consumer | Current role use | Required action |
| --- | --- | --- |
| [FilterSelector query](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/ui/mfe-ratan-container/src/ratancomponents/FilterSelector/store.ts:22) | Sends `assignee` and `moduleOwner`. | Obtain an approved profile or sharing-group contract. |
| [ViewSelector query](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/ui/mfe-ratan-container/src/ratancomponents/ViewSelector/store.ts:21) | Sends `assignee` and `moduleOwner`. | Preserve saved-view access under the agreed identifier. |
| [Filter save and ownership](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/ui/mfe-ratan-container/src/ratancomponents/FilterSelector/common/useFieldNameController.ts:23) | Compares ownership and saves `moduleOwner`. | Handle missing profiles explicitly; preserve existing ownership semantics. |
| [View save and ownership](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/ui/mfe-ratan-container/src/ratancomponents/ViewSelector/common/useViewNameController.ts:22) | Compares ownership and saves `moduleOwner`. | Align backend ownership and frontend selection. |
| [Filter role selector](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/ui/mfe-ratan-container/src/ratancomponents/FilterSelector/FilterName.tsx:63) and [view role selector](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/ui/mfe-ratan-container/src/ratancomponents/ViewSelector/ViewName.tsx:86) | Builds “For My Role” choices. | Supply reviewed sharing groups or disable unsupported choices explicitly. |
| [AdvancedSearch context](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/ui/mfe-ratan-container/src/ratancomponents/RatanFilterBuilder/AdvancedSearch/hooks/useContext.ts:65) | Exposes `userRole`. | Update consumers when the agreed contract changes. |
| [Close gate](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/ui/mfe-ratan-container/src/ratanutils/authenticator.ts:283) and [replay gate](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/ui/mfe-ratan-container/src/ratanutils/authenticator.ts:330) | Excludes `PSS_RO` for settlement client data. | Preserve this restriction through an approved profile or permission rule. |

A missing role passes `undefined !== "PSS_RO"`.
That can remove the UI restriction when a matching action remains granted.
This predicts a UI authorization difference; it does not prove server authorization bypass.

Do not invent a CES role from feature names, action names, or application names.
The BFF needs an explicit profile contract if existing role semantics remain required.
Owner: unknown. Next action: decide and document role, sharing, and restriction semantics before implementation.

## Conditional work

| ID | Condition and evidence | Action and consequence | Owner |
| --- | --- | --- | --- |
| RC-04 | Analytics profile remains a required dimension. [getUserProfile](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/ui/mfe-ratan-container/src/packages/Analysis/v2/User/utils.ts:38) parses `X_RATANONE:ROLE`. | Use the agreed profile contract. A generic CES app returns an empty profile. | unknown |
| RC-05 | CES changes the feature or action spelling. [permission helpers](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/ui/mfe-ratan-container/src/ratanutils/authenticator.ts:148) uses existing `RATAN_*` and `F_*` strings. | Confirm deployed CES identifiers. Add reviewed mappings only where names differ. | unknown |
| RC-06 | A pilot feature uses entitlement configuration. [FeatureFlag](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/ui/mfe-ratan-container/src/packages/FeatureFlag/index.ts:54) calls `.includes` on the entitlement map. | Route checks through the shared permission API and refresh cached decisions after user or entitlement changes. | unknown |

RC-06 is an existing compatibility concern.
This comparison does not establish that an active pilot configuration reaches that branch.
Keep its priority below confirmed migration work until usage is established.

## No BFF-driven change established

The container's HTTP entitlement-rule endpoints remain separate backend contracts.
See [entitlement-rule calls](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/ui/mfe-ratan-container/src/ratanutils/http/api.ts:324).
This BFF diff does not change those URLs or prove their service's CES migration.
Inspect that backend before changing requests, role identifiers, or data filtering.

No direct browser CES client is required by the inspected BFF contract.
Continue to obtain grants through `@fm/base` hooks and existing BFF responses.
Do not copy CES credentials or service connection settings into the UI.

## Controlled helper observations

The parent investigation executed actual permission helpers with synthetic Hooks fixtures.
[PROBE-02](../06-test-cases.md#probe-02--ces-application-bypasses-legacy-permission-lookup) confirms a legacy grant resolves true while its CES counterpart resolves false.
[PROBE-03](../06-test-cases.md#probe-03--a-legacy-entity-masks-a-ces-grant) confirms legacy masking.
[PROBE-04](../06-test-cases.md#probe-04--repeated-application-names-overwrite-grants) confirms repeated-name overwriting.
The [summary](contract-probe-summary.json) binds source hashes and runtime versions.
These probes do not establish live CES mappings or deployed user impact.

## Inspected assertions and remaining coverage

| Assertion source | Inspected coverage | Missing migration evidence |
| --- | --- | --- |
| [authenticator.xratanone.test.ts](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/ui/mfe-ratan-container/src/ratanutils/authenticator.xratanone.test.ts:21) | Exact grant and denial under `X_RATANONE`; legacy subject-name fallback. | Generic CES app names; source marker; mixed sources; duplicate app names. |
| [authenticator.test.ts](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/ui/mfe-ratan-container/src/ratanutils/authenticator.test.ts:397) | Expects `FMO_OPS_SUP` from legacy entities. | Roleless CES; approved profile mapping; preservation of `PSS_RO` restrictions. |
| [analytics profile test](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/ui/mfe-ratan-container/src/packages/Analysis/v2/User/utils.test.ts:3) | Extracts `TEST_PROFILE` from `TEST_SUBJECT:TEST_PROFILE`. | CES application without role; mixed token forms; missing profile. |

Required verification should cover exact allow and deny results within the selected CES application.
Include wrong application, feature, and action; empty grants; duplicate entities; mixed sources; and both entity orders.
Verify saved-filter and saved-view ownership after the profile decision.
Keep legacy fixture coverage during migration.

No application tests ran for this analysis.
No browser, live CES, deployment, or production evidence establishes these source predictions.
The candidate's public response and deployed application names still need contract verification.
