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

# Admin boundary source inspection

> **Proposed boundary expectations require review before acceptance.**
> Action: Resolve proposed policies before acceptance. Consequence: Their acceptance outcomes remain unapproved.
> Owner: unknown. Evidence: [Canonical admin boundaries](../test-cases.md#group-admin-validation). No business execution occurred.

## Scope and revisions

The contribution adds 97 admin boundary cases. It contains 70 implementation characterizations and 27 proposed expectations.
The comparison used the existing UI contribution to avoid duplicating its routine admin paths.
No application source changed. No business case ran.

| Repository | Exact HEAD | Worktree state |
| --- | --- | --- |
| single-ui-bff | `834b4155232222347220e47139a502ee43a9cbdf` | Clean before this inspection. |
| mfe-base | `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85` | Existing `tsconfig.tsbuildinfo` modification remains outside this work. |

The inspected path includes DTOs, controllers, role helpers, services, entities, DDL, exception handling, and UI response consumers.
Qualitative risk is high for owner checks, concurrent approval, and partial saves.
Current DDL limits apply only to prepared-schema fixtures. Deployed database parity remains unknown.

## Coverage

| Category | Cases |
| --- | --- |
| Admin validation | 26 |
| Admin uniqueness | 4 |
| Admin storage boundary | 16 |
| Admin persistence | 12 |
| Admin authority | 15 |
| Admin references | 9 |
| Admin concurrency | 9 |
| Admin URL security | 5 |
| Admin audit fidelity | 1 |

## Findings and evidence limits

| Finding | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| ADM-F-001: The DTOs contain no reviewed version identifier. | [Category DTO](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/dto/request/RequestOfApplicationCategory.java#L6), [update branch](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationCategoryController.java#L40) | A stale verification can act on changed server values. No entity `@Version` was found. | unknown | Review concurrent edit and approval policy before accepting the proposed conflict cases. |
| ADM-F-002: Checker mode falls through when a record is already active. | [Import Map update](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ImportMapController.java#L71) | A second verification can enter the maker branch and deactivate the record. Source predicts this outcome. | unknown | Execute duplicate-verification cases and confirm the intended conflict result. |
| ADM-F-003: Tile create omits the update owner-reference helper. | [Create](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L118), [update helper](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java#L183) | Foreign-owner references may pass create validation. UI filtering does not establish server enforcement. | unknown | Review reference ownership policy and execute substituted-request cases. |
| ADM-F-004: Audit reads do not compare record ownership. | [Category audit reader](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationCategoryController.java#L105) | Valid admin credentials alone can reach an audit lookup by identifier. | unknown | Confirm audit read permissions and execute foreign-owner cases. |
| ADM-F-005: Primary saves precede separate audit writes. | [Category save and audit](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationCategoryController.java#L68) | An error response can follow a successful primary save. Rollback behavior remains unexecuted. | unknown | Inspect transaction boundaries during persistence-failure execution. |
| ADM-F-006: Filter Rule errors use unchecked exceptions. | [Filter Rule parser](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java#L201) | The dedicated validation response shape is unproved. | unknown | Execute malformed JSON and wrong-filter-type UI cases. |
| ADM-F-007: Tile audit assigns theme image fields in reverse. | [Audit builder](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L238) | Audit values can disagree with the saved theme values. This is a source prediction. | unknown | Execute the distinct-image audit case. |
| ADM-F-008: Import Map URL validation checks blanks and spaces. | [Create validation](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ImportMapController.java#L114) | Allowed schemes, hosts, namespace input, and URL safety remain unresolved. | unknown | Obtain policy before accepting proposed URL rejection. |

These findings describe source risks. They do not establish reproduced defects or changed behavior.
The task requests case design. No old-versus-new implementation comparison is attributed.

## Inspected assertions

The Import Map controller test asserts HTTP 400 and `result=false` for self-verification.
The Tile controller test asserts HTTP 400 and `result=false` for denied owner and maker/checker branches.
The Category service tests assert exact creation-disabled, duplicate-ID, and repository-failure messages.
These tests use mocked collaborators. They do not prove persisted schema limits, cross-owner access, or browser behavior.
No inspected assertion was executed during this task.

## Source locators and hashes

| Source path and locator | Exact revision | SHA-256 |
| --- | --- | --- |
| [repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationCategoryController.java:40](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationCategoryController.java#L40) | `834b4155232222347220e47139a502ee43a9cbdf` | `cf5c2266952bb6684f2600ecb268c8120d1efbbf5220d8fadf528c9f8a5b91b3` |
| [repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationCategoryController.java:80](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationCategoryController.java#L80) | `834b4155232222347220e47139a502ee43a9cbdf` | `cf5c2266952bb6684f2600ecb268c8120d1efbbf5220d8fadf528c9f8a5b91b3` |
| [repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationCategoryController.java:105](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationCategoryController.java#L105) | `834b4155232222347220e47139a502ee43a9cbdf` | `cf5c2266952bb6684f2600ecb268c8120d1efbbf5220d8fadf528c9f8a5b91b3` |
| [repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java:46](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L46) | `834b4155232222347220e47139a502ee43a9cbdf` | `ee98fe6f1d416e6646bf26ed950a47927218b4b56c96aff77f02c21afcc8ed79` |
| [repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java:118](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L118) | `834b4155232222347220e47139a502ee43a9cbdf` | `ee98fe6f1d416e6646bf26ed950a47927218b4b56c96aff77f02c21afcc8ed79` |
| [repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java:180](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L180) | `834b4155232222347220e47139a502ee43a9cbdf` | `ee98fe6f1d416e6646bf26ed950a47927218b4b56c96aff77f02c21afcc8ed79` |
| [repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java:215](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L215) | `834b4155232222347220e47139a502ee43a9cbdf` | `ee98fe6f1d416e6646bf26ed950a47927218b4b56c96aff77f02c21afcc8ed79` |
| [repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ImportMapController.java:60](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ImportMapController.java#L60) | `834b4155232222347220e47139a502ee43a9cbdf` | `17e4241303c4e1efaec0dd3f4623d4d823bb232e87a882b7214e48fa1c3c13d0` |
| [repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ImportMapController.java:107](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ImportMapController.java#L107) | `834b4155232222347220e47139a502ee43a9cbdf` | `17e4241303c4e1efaec0dd3f4623d4d823bb232e87a882b7214e48fa1c3c13d0` |
| [repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ImportMapController.java:141](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ImportMapController.java#L141) | `834b4155232222347220e47139a502ee43a9cbdf` | `17e4241303c4e1efaec0dd3f4623d4d823bb232e87a882b7214e48fa1c3c13d0` |
| [repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/dto/request/RequestOfApplicationCategory.java:6](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/dto/request/RequestOfApplicationCategory.java#L6) | `834b4155232222347220e47139a502ee43a9cbdf` | `29d457abd23f5f30cf7a2637cdae5653e3c52daf35501a0d7d8e3b3619348bb8` |
| [repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/dto/request/RequestOfApplicationTile.java:6](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/dto/request/RequestOfApplicationTile.java#L6) | `834b4155232222347220e47139a502ee43a9cbdf` | `b393a586a8d34102c487deeae5d2e53d68b72a99b8b277e968264241bdd224be` |
| [repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/dto/request/RequestOfImportMap.java:6](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/dto/request/RequestOfImportMap.java#L6) | `834b4155232222347220e47139a502ee43a9cbdf` | `166e5d1d44394aa7994e7df587ef73bad94365024d7553dbafe674b4529968af` |
| [repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/repository/ApplicationCategoryRepo.java:24](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/repository/ApplicationCategoryRepo.java#L24) | `834b4155232222347220e47139a502ee43a9cbdf` | `f655d6b7ef99fc5e15bdb14c77dbcbfdbd15bc9b04474e7c039627494582ed44` |
| [repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v1/implementation/ApplicationCategoryServiceImpl.java:40](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v1/implementation/ApplicationCategoryServiceImpl.java#L40) | `834b4155232222347220e47139a502ee43a9cbdf` | `b7dcd37c30101a642faf4a6abc72b116693d7d4eb9b46e6fe3e75ae7895860fc` |
| [repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v1/implementation/ApplicationTileServiceImpl.java:61](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v1/implementation/ApplicationTileServiceImpl.java#L61) | `834b4155232222347220e47139a502ee43a9cbdf` | `78839d4f12fb4e1133d8d18eff46f6613de2a2b69218e43cbd98a0cee7a8bc12` |
| [repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v1/implementation/ImportMapServiceImpl.java:42](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v1/implementation/ImportMapServiceImpl.java#L42) | `834b4155232222347220e47139a502ee43a9cbdf` | `706fe4b63a262f3e42c8e5aaed84cea6d86888faad273d6d3287704f7b47791b` |
| [repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java:42](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java#L42) | `834b4155232222347220e47139a502ee43a9cbdf` | `a515c30c585304810bd6a1dc7044fbccadf2dcb416efb907c0c5960dec4a612d` |
| [repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java:183](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java#L183) | `834b4155232222347220e47139a502ee43a9cbdf` | `a515c30c585304810bd6a1dc7044fbccadf2dcb416efb907c0c5960dec4a612d` |
| [repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java:201](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java#L201) | `834b4155232222347220e47139a502ee43a9cbdf` | `a515c30c585304810bd6a1dc7044fbccadf2dcb416efb907c0c5960dec4a612d` |
| [repos/services/single-ui-bff/src/main/resources/db/migration/V1_0_0__fmo_schema_init.sql:50](../../../repos/services/single-ui-bff/src/main/resources/db/migration/V1_0_0__fmo_schema_init.sql#L50) | `834b4155232222347220e47139a502ee43a9cbdf` | `4202fd63691063b5c1f093fd81d3c739a1b95bfdf062a9773ee6ed2ee4ecd839` |
| [repos/services/single-ui-bff/src/main/resources/db/migration/V1_1_0__application_tile_modify.sql:1](../../../repos/services/single-ui-bff/src/main/resources/db/migration/V1_1_0__application_tile_modify.sql#L1) | `834b4155232222347220e47139a502ee43a9cbdf` | `837029aa32f0b1d98dfc1fda580e5eb09d312da219dc80963970d9ca04b09031` |
| [repos/services/single-ui-bff/src/test/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileControllerTest.java:631](../../../repos/services/single-ui-bff/src/test/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileControllerTest.java#L631) | `834b4155232222347220e47139a502ee43a9cbdf` | `1bd7716e5e9fc419c9034007c0673a1c3750193b75ce5dc1105e29a8cde927f5` |
| [repos/services/single-ui-bff/src/test/java/com/scb/sso/singleuibff/controller/v1/ImportMapControllerTest.java:544](../../../repos/services/single-ui-bff/src/test/java/com/scb/sso/singleuibff/controller/v1/ImportMapControllerTest.java#L544) | `834b4155232222347220e47139a502ee43a9cbdf` | `629cc44ef58c36a9b8fd05a233fcb846df0fd2efae41b93a90b6d66f46c47e30` |
| [repos/services/single-ui-bff/src/test/java/com/scb/sso/singleuibff/service/v1/ApplicationCategoryServiceTest.java:220](../../../repos/services/single-ui-bff/src/test/java/com/scb/sso/singleuibff/service/v1/ApplicationCategoryServiceTest.java#L220) | `834b4155232222347220e47139a502ee43a9cbdf` | `07a14513af9b5381c12ef66eae3b9f5486dad8c64bb0598d685e2f3bc3dc3017` |
| [repos/ui/mfe-base/src/admin/Category/common/useTableDetail.ts:48](../../../repos/ui/mfe-base/src/admin/Category/common/useTableDetail.ts#L48) | `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85` | `12606cf789bd2d727b507f2442cf66409578f7476712f979510ae04ee1802d31` |
| [repos/ui/mfe-base/src/admin/ImportMap/common/useTableDetail.ts:61](../../../repos/ui/mfe-base/src/admin/ImportMap/common/useTableDetail.ts#L61) | `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85` | `cc125326fdcb539a1829ce1d29b7099f744b5fb1806e43a12b78f5a461c6a190` |
| [repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts:64](../../../repos/ui/mfe-base/src/admin/Tile/common/useTableDetail.ts#L64) | `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85` | `2bf4b22926c294c1ea8ab89daeb5d11db80154f4a88dea4f06b2d42858f581d3` |
| [repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts:6](../../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6) | `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85` | `9e49eeb3288a4b574b7eee1c5e90462a34c6bd794bd4965f06899942791f00e3` |

## Handoff

All cases have `NOT_RUN` status. The [canonical catalog](../test-cases.md) contains the current definitions.
IMPLEMENTATION cases characterize inspected source and prepared fixture behavior. They do not establish business approval.
PROPOSED cases state reviewable expectations where implementation or policy support is missing.
Database lengths and uniqueness constraints come from retained migration DDL. No live database or deployment was queried.
The source-reference and unique-ID checks passed. The canonical artifact linter remains the parent task responsibility.
