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

# BFF migration contract analysis

> **Critical conclusion: CES retains the response structure but changes entitlement meaning.**
> Action: adapt frontend grant selection and preserve tile configuration.
> Consequence: legacy role checks cannot represent CES feature permissions.
> Owner: unknown; frontend and BFF maintainers.
> Evidence: [CES mapper](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/AuthorizationResultMapper.java#L68).

## Scope and source identities

The [current user request](user-input.md#exact-user-input) authorizes this analysis.
Application files remain unchanged.

| Repository | Baseline | Candidate | Local state |
| --- | --- | --- | --- |
| single-ui-bff | `834b4155232222347220e47139a502ee43a9cbdf` (`main`) | `267081800cc28b6af0f8e080fa67c2d5f14d3a26` | Clean; branch `codex/apply-service-diffs-20261027`. |

`git diff main...HEAD` contains 53 changed paths.
This analysis follows changed contracts and relevant unchanged paths.
All conclusions below describe inspected source behavior.
No application execution or live CES request occurred.

## Public contract comparison

| Interface | Baseline result | Candidate result | Required frontend response |
| --- | --- | --- | --- |
| Login, Entra login, validation, and relogin | Returns `entities`, `drawers`, and `entitlementsToken`. | Keeps these fields and the JWT response header. Replaces entitlement assembly. | Retain current transport. Update semantic assumptions in grant selectors and tests. |
| `entities[].name` | EMS2 entity name. | CES application name for migrated tiles; EMS2 names remain for legacy tiles. | Select the correct application identity for each tile. Avoid hardcoded legacy entity names. |
| `subjects[].name` and `longName` | EMS2 subject. | CES feature, with both names equal to that feature. | Evaluate CES feature and action permissions. |
| `subjects[].entitlementSource` | Absent. | `EMS2` or `EMS3`. | Add the optional field and preserve compatibility with old responses. Use `EMS3` on the wire. |
| `entities[].roleName`, entity IDs, subject IDs, action IDs | EMS2 metadata available. | CES mapper leaves these values null. CES action objects contain the action name. | Make metadata nullable. Do not derive CES grants from legacy role names or numeric IDs. |
| Authorized drawer tile `entity` | Configured `ems2_entities`. | Configured CES app names for granted CES tiles. | Pass these names to grant selection. Preserve the server-authorized drawer. |
| Authorized drawer tile `entitlementSource` | Absent. | Additional string from tile configuration. | Preserve it where needed. It alone does not identify effective rollback grants. |
| Tile administration | Existing EMS2 configuration fields. | Adds source, app ID, app names, and features. | Add complete create, edit, read, audit, and CSV handling if this interface is supported. |
| Entitlement token | `entity:roleName` keys contain subject/action maps. | Same encoding; CES entities have null role names. | Treat the token as opaque. Do not fabricate legacy roles from CES grants. |

Sources:

- [Authentication assembly](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L100), lines 100–143.
- [Authentication response DTO](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/dto/response/ResponseOfAuthenticate.java#L13), lines 13–22; unchanged.
- [CES mapping](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/AuthorizationResultMapper.java#L62), lines 62–95.
- [CES application identity](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/TileAuthorizationServiceImpl.java#L155), lines 155–166.
- [Source marker](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/dto/ems2/v2/Subject.java#L11), lines 11–18.
- [Legacy source marker](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/implementation/EMS2AuthorizationImplementation.java#L52), lines 52–63.
- [Drawer construction](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java#L183), lines 183–206 and 271–291.

Baseline source locators use the same paths at baseline commit `834b4155232222347220e47139a502ee43a9cbdf`.
Baseline authentication assembly occupies lines 97–137.
Baseline drawer filtering and construction occupy `AdminModuleUtil.java`, lines 101–176.
Baseline `Subject.java` contains no source marker.

## Tile configuration requirements

The wire enum values are `EMS2` and `EMS3`.
CES is the business name; `CES` is not an accepted enum value.

| Field | Candidate validation | Frontend work |
| --- | --- | --- |
| `entitlementSource` | Defaults to `EMS2` when omitted. | Set and preserve the selected source explicitly. |
| `entitlementAppId` | One trimmed value; maximum 64 characters. Commas are rejected. | Provide one app ID for EMS3 tiles. |
| `entitlementAppName` | English comma-separated list; maximum 512 normalized characters. Case-sensitive deduplication. | Provide app names for EMS3 tiles. Quote lists in CSV. |
| `entitlementAppFeature` | English comma-separated list; maximum 512 normalized characters. Case-insensitive deduplication. | Provide features for EMS3 tiles. Quote lists in CSV. |

All three CES values must be nonempty for `EMS3`.
The validation error mentions `ems2Entities`, but this helper does not require that legacy field.
CES authorization reads application names, not `ems2Entities`.
See [configuration validation](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/TileEntitlementConfig.java#L22), lines 22–68.
See [scope parsing](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/TileAuthorizationServiceImpl.java#L271), lines 271–296.

An old update payload can replace an existing CES source with `EMS2`.
The request DTO initializes the source before the controller applies null preservation.
The three CES strings remain preserved when omitted, but the initialized source wins.
This creates inconsistent source configuration without a frontend field.
The consequence is a source prediction; no browser reproduction occurred.
See [request default](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/dto/request/RequestOfApplicationTile.java#L32).
See [update merging](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L277), lines 277–300.
Owner: unknown; frontend and BFF maintainers.
Next action: send all four fields and test editing an existing CES tile.
A backend change to omission handling could also protect older clients.

CSV adds four headers: `Entitlement Source`, `Entitlement App Id`, `Entitlement App Name`, and `Entitlement App Feature`.
The parser accepts all four together or none.
Legacy CSV updates preserve existing CES fields through null values.
Partial CES headers fail validation.
See [CSV parser](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/CsvUtility.java#L93), lines 93–160.
See [bulk merge](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationConfigController.java#L246), lines 246–267.

## Authorization and migration boundaries

The server authorizes CES tiles before returning drawers.
A configured tile requires any matching CES feature, independent of its action value.
The server then applies the existing CES data filter.
Frontends should consume returned drawers and use feature/action grants for controls inside an application.
They should not replace server tile authorization with role-name checks.
See [feature match](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/TileFeatureMatcher.java#L13), lines 13–22.
See [drawer filtering](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java#L118), lines 118–179.

| Mode | Candidate source behavior | Frontend implication |
| --- | --- | --- |
| `EMS2_ONLY` | Reads legacy entities for every row. | Preserve legacy compatibility during rollback. |
| `EMS3_PRIMARY_DUAL_READ` | Reads EMS2 for legacy rows and CES for migrated rows. CES failures retain EMS2 results. | Support mixed subjects. A CES tile can disappear without requiring a session transport change. |
| `EMS3_ONLY` | Reads CES rows only. | Legacy-only tiles disappear from authorization. |

The class default is `EMS2_ONLY`; `application.yml` selects `EMS3_PRIMARY_DUAL_READ`.
Effective deployed configuration remains unverified.
The browser receives no migration mode property.
A tile configured `EMS3` can still use legacy grants in rollback mode.
Prefer actual subject source markers when separating grant systems.
See [mode selection](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/TileAuthorizationServiceImpl.java#L42), lines 42–72.
See [configuration](../../../repos/services/single-ui-bff/src/main/resources/application.yml#L85), lines 85–100.

CES role authorization and data filtering remain separate server paths.
`getAuthorization` validates role entitlements; data filtering validates data entitlements.
Existing `filterRule` and `entryName` contracts remain in use.
The migration does not require a direct browser-to-CES integration or FMAA token handling.
See [CES request](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/filter/ems3/Ems3EntitlementService.java#L111), lines 111–131 and 191–229.
See [existing data filter](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/filter/Ems3AuthFilter.java#L40), lines 40–69.

### Conditional admin dependency

The [3 November user clarification](../../../evidence/knowledge/sources/user-clarifications/ces-migration-coverage-20261103/user-input.md#exact-user-input) gives FMO Portal Admin lower priority.
It exists only outside production, has not launched, and has no assigned users.
This dependency does not establish a production blocker.

The BFF still derives admin ownership from an EMS2 entity and role in the entitlement JWT.
CES mapping leaves `roleName` null, so token keys become `APP:null`.
Changing only frontend admin visibility cannot supply backend maker/checker authorization.
Retain the existing admin boundary until an explicit CES mapping and backend support exist.
Owner: unknown; admin policy and BFF maintainers.
Next action: define CES admin semantics before enabling CES-only administration.
See [admin validation](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java#L43), lines 43–65.
See [tile ownership checks](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L52), lines 52–65.

### Conditional application identity limitation

The returned CES entity contains app name but no app ID.
Same-name applications can merge their subjects and actions across app IDs.
Server tile grants remain independently checked by tile ID.
No evidence establishes duplicate names in the current deployment.
Frontend action isolation needs a contract extension if duplicate names require distinct permissions.
Owner: unknown; BFF and application maintainers.
Next action: confirm app-name uniqueness before relying on app-name-only permission keys.
See [application grouping](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/TileAuthorizationServiceImpl.java#L115), lines 115–166 and 190–204.

## Inspected test assertions

All test sources use candidate revision `267081800cc28b6af0f8e080fa67c2d5f14d3a26`.
Their assertions were inspected. Their execution status is `NOT_RUN` for this task.

| Test source | Inspected assertion | Limits |
| --- | --- | --- |
| [Application-name authorization](../../../repos/services/single-ui-bff/src/test/java/com/scb/sso/singleuibff/service/v2/authorization/Ems3ApplicationNameAuthorizationTest.java#L64), lines 64–103 | App names become entity names; actions remain isolated by app name; drawer entity names match. | Mocked CES and synchronous executor. |
| [Same-name app IDs](../../../repos/services/single-ui-bff/src/test/java/com/scb/sso/singleuibff/service/v2/authorization/Ems3ApplicationNameAuthorizationTest.java#L106), lines 106–122 | A grant for one app ID cannot show another tile. | Does not prove app-ID isolation in returned action entities. |
| [Missing user and invalid app names](../../../repos/services/single-ui-bff/src/test/java/com/scb/sso/singleuibff/service/v2/authorization/Ems3ApplicationNameAuthorizationTest.java#L125), lines 125–157 | Denies affected tiles without manufacturing entities. | Mocked upstream. |
| [Rollback and mixed mode](../../../repos/services/single-ui-bff/src/test/java/com/scb/sso/singleuibff/service/v2/authorization/Ems3ApplicationNameAuthorizationTest.java#L160), lines 160–196 | Preserves legacy names during rollback and distinct names during dual-read. | No browser state assertions. |
| [Mapper](../../../repos/services/single-ui-bff/src/test/java/com/scb/sso/singleuibff/service/v2/authorization/AuthorizationResultMapperTest.java#L28), lines 28–88 | Feature names, actions, source marker, deduplication, and case preservation. | Tests the mapper only. |
| [Tile create validation](../../../repos/services/single-ui-bff/src/test/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileControllerTest.java#L355), lines 355–416 | Rejects missing CES config; persists all four fields. | Mocked admin access. |
| [Tile update validation](../../../repos/services/single-ui-bff/src/test/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileControllerTest.java#L453), lines 453–474 | Rejects an explicit EMS3 update with missing CES config. | Does not assert old-client omission behavior. |

## Confidence and limits

Confidence is high for the inspected contract differences.
Required frontend edits still depend on their current consumer implementations.
No runtime behavior, deployment state, full application acceptance, or production parity is established.
No application code, package dependencies, graph, or external system was changed.
