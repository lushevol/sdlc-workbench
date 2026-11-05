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

# MFE Base impact evidence

> **Critical conclusion: Reconcile workspace and deep-link checks with the BFF authorization decision before CES rollout.**
> Action: update the shared tile check and its consumers. Consequence: authorized CES pages can be rejected.
> Owner: unknown. Evidence: [current check](../../../repos/ui/mfe-base/src/utils/common.ts#L260-L311) and [BFF mapping](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/TileAuthorizationServiceImpl.java#L155-L165).

## Scope and identities

The [user request](user-input.md#exact-user-input) authorizes analysis. Application source remains unchanged.

| Repository | Baseline | Inspected candidate | Limits |
| --- | --- | --- | --- |
| single-ui-bff | `834b4155232222347220e47139a502ee43a9cbdf` | `267081800cc28b6af0f8e080fa67c2d5f14d3a26` | Local `main` comparison; no live environment. |
| mfe-base | `f025513f696476a9cc8162681410cbd21e029bcb` | `66c6411ade58e4d134e381c2baee8ad3f76a8dbf` | Local Home controller formatting edits remain preserved. |

The frontend branch changes session handling. Its shared entitlement models and tile administration fields retain baseline semantics.
`src/utils/common.ts` has session changes elsewhere. Its tile validation retains the baseline behavior.

## Required runtime work

### BASE-01: Use the BFF authorization decision for CES tile access

Confidence: high for the source incompatibility. Actual deployed reachability remains untested.

The BFF maps CES `applicationName` into `entity.name`.
It maps CES features into subject names and tags those subjects `EMS3`.
The drawer retains `ems2_subject`, while its entity names change to configured CES application names.
The BFF grants individual tiles from case-insensitive configured feature matches, independent of the action value.

Sources: [application mapping](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/TileAuthorizationServiceImpl.java#L139-L165), [subject mapping](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/AuthorizationResultMapper.java#L62-L96), [drawer construction](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java#L184-L206), and [drawer entity selection](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java#L271-L289).

Setup: A non-template tile has a legacy subject that differs from its configured CES feature.

1. Return the tile in the BFF authorized drawer.
2. Restore its saved workspace, or open its URL deep link.
3. Evaluate the current shared tile check.

| Result class | Result |
| --- | --- |
| Proposed migration expectation | The authorized tile opens. A tile absent from the authorized drawer stays unavailable. |
| Old source prediction | A matching EMS2 entity and subject pass the shared check. |
| New source prediction | The CES application matches, but its feature differs from the legacy subject. The shared check returns false. |
| Consequence | Workspace validation discards the saved page. Deep-link opening does not add the page. |

Affected source: [validateTile and validateWorkspace](../../../repos/ui/mfe-base/src/utils/common.ts#L260-L311), [workspace caller](../../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L284-L299), and [deep-link caller](../../../repos/ui/mfe-base/src/pages/Home/common/useParameters.ts#L66-L85).

Next action: establish one tile-access helper using the current authorized drawer.
Treat membership as the CES tile decision. Preserve denied-tile rejection and declared rollback behavior.
Avoid reconstructing tile authorization from aggregate subject grants.
The public drawer lacks the per-tile feature list and application ID.

The stored `entitlementSource` alone does not identify the effective provider.
`EMS2_ONLY` uses legacy authorization even when a stored tile source is `EMS3`.
Its drawer still exposes the stored source.
Use authoritative drawer membership consistently, or add effective-provider evidence before branching by source.
Sources: [mode handling](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/TileAuthorizationServiceImpl.java#L42-L73) and [drawer source](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java#L206).

Owner: unknown. Qualitative risk: high for affected page entry; no forced logout is established.

### BASE-02: Represent the CES compatibility payload accurately

Confidence: high. This is a contract and presentation change.

Add `entitlementSource?: "EMS2" | "EMS3"` to `Subject` and `Tile`.
Allow null or absent CES IDs, role identifiers, role names, and entity application names.
The CES mapper sets names and actions. It does not populate legacy numeric identifiers or role metadata.
Source: [shared interfaces](../../../repos/ui/mfe-base/src/hooks/model/root.ts#L42-L81) and [mapper](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/AuthorizationResultMapper.java#L62-L96).

Adapt profile titles and React keys for these fields.
The current profile displays `* :: application :: null` for typical CES entities.
Multiple CES entities use null React keys and repeated DOM IDs.
Use stable composite keys from available identity and source. Do not invent a CES role assignment.
Sources: [profile title](../../../repos/ui/mfe-base/src/components/Profile/util.ts#L1-L5), [entity keys](../../../repos/ui/mfe-base/src/components/Profile/index.tsx#L129-L138), and [subject IDs](../../../repos/ui/mfe-base/src/components/Profile/index.tsx#L39-L43).

The current token key remains `entityName:roleName`.
For serialized null roles, Java and JavaScript both form `entityName:null`.
Therefore, missing role metadata does not prove an inevitable profile crash.
Defensive action lookup should support absent or inconsistent token entries.
Sources: [BFF token map](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L131-L143) and [profile lookup](../../../repos/ui/mfe-base/src/components/Profile/index.tsx#L109-L120).

Owner: unknown. Qualitative risk: low for presentation; shared contract consumers need regression checks.

## Conditional administration work

### BASE-03: Expose the new tile entitlement configuration

Confidence: high for missing fields. Delivery priority depends on use of this administration module.

Add these fields to the tile form, table, verification view, and audit view:

| Field | Supported value |
| --- | --- |
| `entitlementSource` | `EMS2` or `EMS3`; use an explicit valid default for new records. |
| `entitlementAppId` | One trimmed value, maximum 64 characters; no comma. |
| `entitlementAppName` | English-comma list; normalized stored length at most 512 characters. |
| `entitlementAppFeature` | English-comma list; normalized stored length at most 512 characters. |

For `EMS3`, require nonempty application ID, application names, and features.
Preserve case-sensitive application names. Feature duplicate normalization is case-insensitive.
The backend validates these rules. Client validation should show errors before submission.
The backend error text mentions `ems2Entities`, but its configuration helper does not require that field.
Do not introduce that extra client requirement from the message alone.
Source: [backend configuration rules](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/TileEntitlementConfig.java#L22-L68).

The current form is generated from columns. Those columns contain only legacy role fields.
The audit table also omits the four new fields.
Sources: [tile columns](../../../repos/ui/mfe-base/src/admin/Tile/common/useController.tsx#L232-L259), [new record creation](../../../repos/ui/mfe-base/src/admin/Tile/common/useController.tsx#L342-L360), [form generator](../../../repos/ui/mfe-base/src/components/TableDetail/index.tsx#L48-L60), and [audit columns](../../../repos/ui/mfe-base/src/admin/Tile/common/useAudit.tsx#L124-L137).

Existing services spread complete records into create, maker, and checker requests.
Opening a record also clones all fields. Existing CES fields can survive unrelated edits.
Therefore, do not report that every legacy edit resets CES configuration.
Sources: [record clone](../../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L26-L34) and [request bodies](../../../repos/ui/mfe-base/src/admin/Tile/services/useServices.ts#L66-L137).

Owner: unknown. Next action: add visible fields when this module enters delivery scope.
Treat admin owner-role migration separately. Current BFF validation still requires the legacy administrative role token.
Sources: [frontend admin role](../../../repos/ui/mfe-base/src/admin/common/utils/index.ts#L3-L10) and [BFF admin validation](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java#L43-L65).

## Adjacent compatibility concern

`handleDrawers` ignores an explicit empty list.
A successful empty authorization result can therefore leave previous drawers in memory.
This predates the CES migration. It is an adjacent correction, not an introduced regression.
Distinguish an absent drawers field from `drawers: []` during renewal and validation handling.
Retain missing fields for responses that do not return entitlements.
Source: [drawer handler](../../../repos/ui/mfe-base/src/utils/login.ts#L98-L107) and [response routing](../../../repos/ui/mfe-base/src/hooks/service/util/succes.response.handler.ts#L84-L96).
Owner: unknown. Next action: define and assert explicit empty-result replacement.
User impact remains a source prediction. No deployed access bypass is established.

## Confirmed compatibility boundaries

- Login and validate URLs remain unchanged.
- The BFF still returns `entities`, `drawers`, and `entitlementsToken`.
- Current handlers already store these response fields.
- No direct browser-to-CES client is required by this BFF contract.
- Do not rename stored admin ownership field `ems2Role` without a separate backend contract change.

Sources: [BFF response construction](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L100-L143), [login parsing](../../../repos/ui/mfe-base/src/utils/login.ts#L65-L105), and [service URLs](../../../repos/ui/mfe-base/src/services/index.ts#L10-L38).

## Controlled helper observations

The parent investigation executed actual helper bodies with synthetic BFF-shaped payloads.
[PROBE-01](../06-test-cases.md#probe-01--legacy-subject-rejects-an-authorized-ces-tile) confirms legacy acceptance and CES rejection under differing subject names.
The [retained result](PROBE-01.json) includes workspace replacement and a zero-count launch callback.
This does not establish browser, live BFF, CES, or production behavior.

## Inspected assertion evidence and remaining tests

| Existing source | Actual assertions | Limit |
| --- | --- | --- |
| [common.test.ts](../../../repos/ui/mfe-base/src/utils/common.test.ts#L339-L356) | Legacy subject matching and saved-workspace filtering. | No CES feature-versus-legacy-subject assertion. |
| [drawer.test.ts](../../../repos/ui/mfe-base/src/utils/drawer.test.ts#L142-L158) | Legacy subject retrieval and missing-subject rejection. | No CES source separation. |
| [Profile test](../../../repos/ui/mfe-base/src/components/Profile/index.test.tsx#L111-L127) | EMS2 role title, subject text, and close handler. | No null-role CES entity fixture. |
| [Tile service test](../../../repos/ui/mfe-base/src/admin/Tile/services/index.test.tsx#L29-L57) | Service calls execute; screen exists. | No request-payload assertion for entitlement fields. |

Add meaningful assertions for CES workspace preservation and deep links with differing legacy subjects.
Assert denied tile removal, mixed EMS2/CES users, application-name separation, and EMS2 rollback compatibility.
Assert null-role profile rendering and explicit empty-drawer replacement.
If administration enters scope, assert create/edit/verify/audit field preservation and validation boundaries.
No application test suite or live browser case ran in this analysis.

Automated document check: 37 local links resolve. [Source hashes](mfe-base-source-hashes.json) identify 25 cited files.
This check does not validate complete ASD grammar or execute application behavior.
