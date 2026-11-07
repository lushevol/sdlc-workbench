---
artifact_kind: change-review
id: CR-CES-ZERO-UPPER-CHANGE-AUDIT
version: 1
status: draft
owner: unknown
review:
  state: pending
  reviewer: null
  reviewed_at: null
writing_review:
  standard: ASD-STE100
  automated_check: NOT_RUN
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
---

# EMS2 to CES zero-upper-change audit

> **Zero upper-layer source changes cannot preserve every EMS2 behavior.**
> Ordinary unambiguous permission calls and ordinary launches remain compatible.
> Scalar role, role-owned data, admin ownership, and conflicting provider calls do not.

## Scope and revisions

This audit compares the supplied UI and backend repositories.

| Repository | Baseline | Candidate or snapshot | Consumer evidence |
| --- | --- | --- | --- |
| `mfe-base` | `4c36f8e` | `5295bd7` | Cashflow snapshot and shared imports |
| `mfe-ratan-container` | `647e6b3` | `72a446f` | Cashflow snapshot and shared imports |
| `mfe-cashflow-blotter` | filesystem snapshot | filesystem snapshot | SHA-256-bound source |
| `single-ui-bff` | `834b415` | `95480c0` | BFF tests and DTO/service source |
| `ratan-auth-server` | `7e8cbfa` | `cacc4d2` | auth-server tests and source |
| `single-ui-sdk-starter` | `b0aa820` | `fd9a157` | SDK compatibility tests and source |
| `mfe-root-config` | supplied snapshot | supplied snapshot | no entitlement consumer found |
| `mfe-trades` | filesystem snapshot | filesystem snapshot | direct legacy role and entitlement readers |
| `mfe-rules` | filesystem snapshot | filesystem snapshot | scalar role, filter ownership, and rule permission consumers |

No live CES request, deployed upper application, or production backend response was executed.

## Findings

| ID | Boundary | Upper-layer consequence | Can lower layers preserve the old contract? |
| --- | --- | --- | --- |
| ZUC-UI-01 | Cashflow exports only global `hasPermission` and `getUser`; its mount type omits the optional scope. | A same-feature EMS2/CES conflict cannot identify the tile. Global calls fail closed. | Only if the container supplies an instance-bound facade internally. The current container provider does not store the scope. Otherwise this requires upper changes or a rollout with no conflicting features. |
| ZUC-UI-02 | Cashflow and container use scalar `getUser().role` for authorization-limit URLs and role-owned queries. | CES-only users can send `/undefined/<currency>/<amount>` and saved-item queries cannot represent all roles. | Only if the backend supplies an authoritative legacy scalar. `roleList.join(",")` is unsafe. |
| ZUC-UI-03 | View and filter stores send `assignee` and `moduleOwner` as one role. | CES role-owned create, update, and delete are held. Reads can omit valid shared items. | No frontend-only solution. Ownership and query semantics must be defined by the backend. |
| ZUC-UI-04 | Settlement client-data close/replay checks exclude `PSS_RO` through one scalar role. | The CES actions are denied even when the action grant exists. | No safe compatibility mapping exists without a CES multi-role exclusion rule. |
| ZUC-UI-05 | Base admin Category, ImportMap, and Tile controllers derive `FMO PORTAL ADMIN` `roleName` as `ems2Role`. | CES admin maker/checker payloads lose their owner and can be rejected. | Only if the admin path remains EMS2 or the backend accepts a CES admin identity. |
| ZUC-UI-06 | Raw helpers and telemetry still search for `X_RATANONE`; profile action lookup uses `entity.name:roleName`. | Direct readers miss CES permissions. CES-only telemetry has an empty legacy profile. | Authorization can be preserved through route-aware calls. Direct legacy readers cannot be preserved without a compatibility projection. |
| ZUC-UI-07 | Cashflow permission booleans are computed at module load. | A grant or provider replacement during an existing session leaves controls stale. | Load entitlements before remotes, or make the container provide reactive decisions. The current upper source cannot be changed under this constraint. |
| ZUC-UI-08 | Tile lookup now rejects duplicate structural routes. | Existing string-only deep links can stop opening when two catalog rows match. | Only by preserving first-match behavior, adding a lower-layer deterministic ID lookup, or removing duplicate catalog rows. |
| ZUC-UI-09 | `mfe-trades` derives product-specific behavior by finding the first `X_RATANONE` key and stripping its prefix. | If this helper is reached, a CES-only user has `RATAN_ENTITLEMENT_RULE` plus `roleList`; the lookup returns an empty role and product-specific header behavior can be wrong or blank. Multiple CES roles would also be reduced to one first match. No production caller was found in this snapshot, so the current runtime impact is conditional. | A lower layer can emit an explicit `X_RATANONE:<role>` compatibility alias only for an approved deterministic role. CES role multiplicity cannot be safely projected into this scalar reader. |
| ZUC-UI-10 | `mfe-trades` gates the confirmation deep link with `getUser().role` against four EMS2 roles. | A CES-only or multi-role user has no equivalent scalar role, so “View Confirmation” is hidden even when the required permission exists. | Only a lower-layer scalar projection preserves one-role users. Multi-role users require a permission-based compatibility rule or an upper change. |
| ZUC-UI-11 | `mfe-rules` sends one `assignee` and one `moduleOwner` and classifies returned filters against one role. | CES role-owned filters can be omitted, placed in the wrong group, or written with an arbitrary owner. The current role-ownership guard therefore keeps valid CES writes pending. | No lower layer can invent the owner. Define CES ownership and query semantics, or keep affected role-owned writes unavailable. |
| ZUC-UI-12 | `mfe-rules` filters MO business-flow and initial route configuration with scalar role equality and `includes`. | `getUser().role` is undefined for a CES-only user in the current adapter, and a multi-role user cannot select all applicable flows. The page can open with no rule type or business flow. | A lower layer can preserve this only with one authoritative legacy role. A joined `roleList` is unsafe because no configured value equals a comma-delimited list. |
| ZUC-UI-13 | `mfe-rules` feature flags check configured entitlement strings against `Object.keys(curUser.entitlements)`. | CES-only payloads expose CES entity names and roleList values. Legacy feature flags can evaluate false and silently hide features unless the lower layer preserves legacy keys. | Preserve the old entitlement-key projection for legacy flags, or migrate each flag configuration. The latter changes upper-layer configuration and violates the zero-change constraint. |
| ZUC-UI-14 | Rule tiles use legacy `F_Input_Delete_Modify_*` permission codes for maker/checker controls. | The supplied CES login capture contains only `ACCESS_FMO_POST_TRADE_PORTAL` for rule subjects, while the CES catalog contains nested role entitlements with `F_Input_Delete_Modify_*`. If the login payload remains as captured, rule mutation controls are disabled. | The BFF/auth adapter must flatten the authoritative CES role-entitlement actions into the existing subject/action projection. The UI cannot recover actions from roleList alone. |
| ZUC-UI-15 | `mfe-trades` reads `hooks.store.user.entitlements` directly in the legacy helper, while `mfe-base` populates that field only from the legacy `entitlementsToken` and stores CES entities separately. | A CES response without a legacy flat entitlement token leaves this direct reader empty even if the container's `getUser()` and `hasPermission()` adapters work. | A container-only fix cannot reach this store-level read. The lower login/base projection must populate legacy keys, or this latent helper remains incompatible. |
| ZUC-BFF-01 | `single-ui-bff` has global `EMS2_ONLY`, `EMS3_PRIMARY_DUAL_READ`, and `EMS3_ONLY` modes. | `EMS3_ONLY` reads no EMS2 scopes. Remaining EMS2 tiles disappear during a per-tile rollout. | Mixed migration requires dual-read mode or a new per-scope backend selection. A global EMS3-only switch cannot support partial migration. |
| ZUC-BFF-02 | CES mapper maps `entitlement_name` to `roleList` and role grants to subjects, but leaves `id`, `roleId`, and `roleName` unset. | Upper code that expects required EMS2 IDs or a scalar role receives null values. | Preserve legacy values where authoritative, make nullability explicit, and keep scalar consumers on an approved compatibility mapping. |
| ZUC-BFF-03 | CES DTOs contain `data_profiles` and `data_policies`, but the mapper discards them. | The Cashflow data profile cannot be recovered from the entity response. | Add a separate profile contract or retain the legacy data-profile service. `roleList` cannot replace it. |
| ZUC-BFF-04 | Mapper rejects empty `role_entitlements`; `EMS3_ONLY` propagates the failure. | A valid CES user with no functional grant can fail login instead of receiving an empty deny result. | Treat an empty valid CES assignment as an empty authorization result. Verify CES response semantics first. |
| ZUC-BFF-05 | BFF flat entitlement token uses `entity.name:roleName`. | CES can emit `RATAN_ENTITLEMENT_RULE:null`. Admin token validation still searches for `FMO PORTAL ADMIN:<role>`. | Keep admin identity on EMS2 or migrate token and admin validation together. Frontend changes cannot fix this. |
| ZUC-BFF-06 | CES feature fields are optional in tile configuration, while frontend CES admission requires a complete route. | BFF may show a CES tile with blank feature control while the frontend hides it. Invalid CES configuration is also retained as a CES route and denied later. | Define one blank-feature policy and reject invalid rows before login. |
| ZUC-BFF-07 | Tile IDs are parsed as `Long` while route construction is performed during login. | A malformed or missing catalog ID can fail the login/drawer build. | Validate catalog IDs before authorization assembly. |
| ZUC-BFF-08 | The supplied login response has only `ACCESS_FMO_POST_TRADE_PORTAL` for rule subjects, although the CES application catalog contains nested role-entitlement action grants. | Existing rule UIs call `F_Input_Delete_Modify_Initiate` and `F_Input_Delete_Modify_Verify`; those controls fail closed if the nested grants are not flattened into the response. | Verify the live CES user response and map the authoritative nested role-entitlement actions. Do not treat the captured login response as action-parity evidence until this discrepancy is resolved. |
| ZUC-BFF-09 | Adding only CES `roleList` and `applicationId` preserves profile metadata, but the new UIs never read either field for authorization. | If the BFF does not also preserve the legacy `subject:action` projection, every `hasPermission("RATAN_*:F_*")` call fails closed. The UI cannot reconstruct actions from roleList. | Keep the complete legacy action projection as an additive compatibility view. `roleList` and `applicationId` are required metadata, not a replacement for subjects and actions. |
| ZUC-AUTH-01 | `ratan-auth-server` selects EMS3 by user allowlist, not by tile. | Users outside the allowlist retain EMS2, and one user's source is globally selected. This cannot express mixed tile ownership. | Use the BFF per-tile dual-read path, or add resource-level routing to the auth server. |
| ZUC-AUTH-02 | `DefaultEms3EntitlementMapper` requires one mapped scalar role and throws on multiple mapped roles. | Multi-role CES users cannot be projected into the legacy JWT contract. | Only an authoritative role mapping can preserve the old contract. Otherwise the JWT contract must change. |
| ZUC-AUTH-03 | `RatanEntitlement` exposes only scalar `role`, `actions`, and scalar `dataEntitlementRoles`. | CES role multiplicity and data profiles are discarded before upper applications receive the token. | Additive fields are required, or affected consumers must retain EMS2. |
| ZUC-AUTH-04 | Data-role resolution recognises only `Global`, `GBS`, and `Onshore` names. | Other CES data profiles resolve to empty and can fail JWT creation or authorization-limit calls. | Map the authoritative CES data profile explicitly. Do not infer it from entitlement names. |
| ZUC-AUTH-05 | Auth-server CES mapping rejects empty action lists and incomplete responses. | Data-only or no-grant users can fail authentication rather than receive a valid empty permission set. | Return a valid deny projection for valid empty assignments; reserve failure for malformed or unavailable responses. |
| ZUC-AUTH-06 | Dual-read comparisons only log differences. | A successful login does not prove EMS2/CES permission parity. | Add a release decision gate or retain EMS2 for any mismatch. |
| ZUC-SDK-01 | The SDK preserves the old `entity:role -> subject -> actions` map and rejects ambiguous role or feature mappings. | Multiple CES roles or colliding feature aliases cannot be represented without a mapping decision. | Keep the old map only for assignments with a deterministic one-to-one mapping. Otherwise the old contract cannot be preserved. |

## Verification gaps in the new repositories

- `mfe-trades/src/utils/filter.test.ts` covers only `X_RATANONE:<role>` fixtures. It has no CES `applicationId` or `roleList` case, so the empty-role failure is untested. The helper has no production caller in this snapshot, so this is a latent risk.
- `mfe-rules/src/DroolsRule/hooks/useUser.test.ts` covers synthetic maker/checker permission combinations. It does not cover an undefined or multi-role `getUser().role`, so blank MO routes and role-owned filter behavior are untested.
- No live CES login or deployed upper application was executed. These findings are static source and supplied-capture evidence only.

## Hard warnings

The following gaps cannot be resolved by `mfe-base` and `mfe-ratan-container` alone:

1. A CES multi-role user needs a scalar data profile.
2. A CES multi-role user needs one role owner for shared views and filters.
3. `PSS_RO` exclusion semantics must be defined for CES.
4. CES admin operations need a role-bearing token or a new admin authorization contract.
5. Mixed EMS2/CES tiles need dual-read or per-tile backend routing.
6. A valid CES response with no functional grants must not be treated as a malformed login.

The safe behavior is fail closed for these cases. That prevents unauthorized access, but it can hide valid CES actions and block valid writes. No lower-layer fallback can safely invent a role, owner, or data profile.

## Compatible without upper source changes

The following paths remain compatible when their route and data prerequisites are met:

- Ordinary unambiguous `hasPermission(code)` calls.
- `getUser().id`, identity, and ordinary mount parameters.
- Unique tile launches with preserved application tile IDs.
- EMS2-only tiles and EMS2 private creator-owned saved items.
- Creator-owned AdvancedSearch flows that use user ID rather than role ownership.
- CES profile display through `applicationName`, CES `name`, `applicationId`, and `roleList`.

These compatible paths do not establish complete migration parity.
