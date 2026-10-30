# Backend migration source investigation

> **Full EMS2 retirement remains unresolved.**
> Action: define the target for legacy data roles, SDK lookups, and admin ownership.
> Consequence: `EMS3_ONLY` does not remove all EMS2 calls.
> Owner: unknown. Evidence: [JWT conversion](../../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/jwtparser/convertor/JwtConvertorForNewUse.java:113).

## Scope and source identity

The [user request](user-input-20261030-migration-plan.txt) is the high-priority reference, dated 30 October 2026.
The [recovered user statements](historical-user-inputs-20261028-29.json) preserve high-priority migration intent from 28–29 October.
The 29 October statement requires zero EMS2 dependencies across RATAN for the final November release.
It permits per-tile EMS2/CES switching during testing. Service authorization targets CES throughout testing, onboarding, and release.
These are user-stated requirements. They do not establish deployed completion.
This investigation inspected source, recent diffs, configuration, and selected test assertions.
It executed no business tests or external service calls.
The [source manifest](backend-source-manifest-20261030.json) preserves exact inspected identities and hashes.
All three worktrees were clean during inspection.

| Repository | Current revision | Commit date, Singapore time | Baseline used |
| --- | --- | --- | --- |
| Auth server | `dd6ebe87371d0fd484b68ce254fd2f18cc58bfd2` | 30 October 2026, 07:49:37 | `3b32ad5a76c1f7c1cdf7bd7b72b3f3c27360b5ce`, 27 October |
| Single UI BFF | `134a340472f29d2a4136e07e516690de6a18e323` | 30 October 2026, 07:52:24 | `19f484efbbfbd4a9d16cdec8a64c4b7fa66e901a`, 27 October |
| Auth SDK | `b0aa82005e7f14202f85f5ef583f25e42da9eeb3` | 14 October 2026, 09:28:09 | Current source only |

Today's commits are named `CES Migration` in both services.
Their presence establishes local implementation, not deployment or acceptance.

## Confirmed auth server behavior

Confidence: high for the inspected source and assertions. Deployment remains unknown.

| Claim | Inspected evidence | Consequence and limit |
| --- | --- | --- |
| Full reads support `EMS2_ONLY`, `EMS3_PRIMARY_DUAL_READ`, and `EMS3_ONLY`. | [Facade](../../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/migration/EntitlementMigrationFacade.java:35). | Base configuration selects dual read. Effective environment overrides remain uninspected. |
| Dual read returns CES as primary and compares EMS2 asynchronously. | [Executor](../../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/migration/EntitlementDualReadExecutor.java:70). | CES failure propagates. It does not trigger EMS2 fallback. |
| CES requests use app ID, app name, user ID, and an FMAA bearer token. | [Repository](../../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/repo/Ems3Repository.java:40). | Target path is `/fmces/v1/entitlement/app/{appId}/{appName}/user/{userId}`. |
| The mapper preserves legacy role and action fields through a unified model. | [Mapper](../../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/entitlement/mapper/DefaultEms3EntitlementMapper.java:28). | User actions become `feature:action`. System actions become `RATAN_FUNC:action:feature`. |
| Entitlement names require configured role mapping. | [Role resolution](../../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/entitlement/mapper/DefaultEms3EntitlementMapper.java:77). | Missing mapping or conflicting mapped roles fails the read. |
| Current mappings include `RATAN_ENTITLEMENT_COMMON` to `FMO_OPS_BOM`. | [Configuration](../../../repos/services/ratan-auth-server/src/main/resources/application.yml:170). | This is configured behavior. Business approval is not established. |
| Data profiles can map to legacy role names inside the full projection. | [Data-role mapping](../../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/entitlement/mapper/DefaultEms3EntitlementMapper.java:114). | Sample mappings use `approved-legacy-data-role`. Production completeness remains unknown. |
| JWT role and actions use the selected full read. JWT data roles use a separate EMS2 account read. | [JWT converter](../../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/jwtparser/convertor/JwtConvertorForNewUse.java:113). | CES-derived data-profile roles do not replace JWT data roles. |
| The separate data-role read always selects EMS2, regardless of migration mode. | [Facade](../../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/migration/EntitlementMigrationFacade.java:58); [reader](../../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/migration/Ems2LegacyEntitlementReader.java:145). | It uses `/ems2/rest/account/{userId}` without the full entitlement cache. |
| The separate CES data-filter API remains independent of full migration mode. | [Data service](../../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/service/Ems3EntitlementService.java:60). | It returns fields, values, and ANY/ALL filter relations. |
| CES projection caches separate user and system keys and record their source. | [Cache](../../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/entitlement/cache/RedisEntitlementCacheService.java:30). | Redis operations and effective expiry need runtime verification. |

Base configuration sets 15-second total read deadlines for each source.
It declares separate thread pools and bounded queues.
It sets one-second connect timeouts, with two-second EMS2 and three-second CES read timeouts.
These declarations do not establish measured login latency.
Evidence: [configuration](../../../repos/services/ratan-auth-server/src/main/resources/application.yml:156).

Current diagnostic configuration enables detailed and raw logging.
Payload logging exists in the facade, mapper, and CES repository.
Operational exposure and production settings remain unknown.
Evidence: [facade diagnostics](../../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/migration/EntitlementMigrationFacade.java:120).

## Confirmed BFF behavior

Confidence: high for source behavior. Approved policy and runtime results remain unknown.

| Claim | Inspected evidence | Consequence and limit |
| --- | --- | --- |
| Tiles carry source, app ID, app name, and app feature configuration. | [Configuration model](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/TileEntitlementConfig.java:11). | Missing source defaults to EMS2. CES requires nonempty app ID, names, and features. |
| CES app names and features support comma-separated lists. | [Parser](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/TileEntitlementConfig.java:22). | App ID is a single value. Names and feature lists have length limits. |
| Requests group tiles by CES app ID and app name. | [Routing](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/TileAuthorizationServiceImpl.java:115). | Calls run through a configured executor. Runtime latency remains unmeasured. |
| CES tile grants use any matching configured feature, ignoring case. | [Matcher](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/TileFeatureMatcher.java:13). | Visibility matching does not itself inspect the action name. |
| Per-tile grants remain separate from combined legacy entity data. | [Result model](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/TileAuthorizationResult.java:10). | This adds application-specific visibility control. It does not prove downstream authorization isolation. |
| EMS2 subjects and CES subjects carry distinct source tags. | [Mapper](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/AuthorizationResultMapper.java:74); [drawer filtering](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java:124). | Legacy visibility filters select EMS2 subjects. CES tiles require their granted tile ID. |
| Dual mode reads EMS2 for legacy tiles and CES for migrated tiles. | [Source selection](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/TileAuthorizationServiceImpl.java:43). | This differs from auth's same-user full-read comparison. Comparisons can contain disjoint scopes. |
| A CES failure in dual mode preserves existing EMS2 results. | [Failure handling](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/TileAuthorizationServiceImpl.java:61). | Migrated tile scopes receive no automatic EMS2 fallback. |
| A specific CES user-not-found response yields no application grants. | [Application read](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/TileAuthorizationServiceImpl.java:139). | Other CES exceptions propagate in EMS3_ONLY mode. |
| Database changes cover live tiles and tile audits. | [Migration](../../../repos/services/single-ui-bff/src/main/resources/db/migration/V1_1_1__application_tile_add_entitlement.sql:1). | Existing tiles default to EMS2. Source and target database migration histories remain unknown. |
| CSV import parses all four entitlement columns. | [CSV parser](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/CsvUtility.java:120). | Legacy CSV without these columns preserves existing settings through update logic. |
| Tile edits preserve omitted entitlement fields. | [Controller](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java:281). | This differs from the 27 October review baseline. |
| Login still returns `entities`, tokens, and drawers through existing response structures. | [Login construction](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java:100). | Frontend compatibility needs verification against actual consumers. |
| CES data filters remain a second drawer-filtering step. | [Filter](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/filter/Ems3AuthFilter.java:40). | Failed or empty filter lookup removes affected filtered tiles. |

## Remaining legacy dependencies

These are planning gaps against the recovered zero-EMS2 target.
This investigation does not establish production impact or assign release-blocking defect priorities.

| Area | Evidence and confidence | Consequence | Owner and next action |
| --- | --- | --- | --- |
| JWT data roles | [Separate EMS2 read](../../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/jwtparser/convertor/JwtConvertorForNewUse.java:128); high. | Switching full reads to CES cannot retire EMS2. | unknown; implement a reviewed CES replacement before the final release. |
| Downstream SDK lookups | [AuthorizationImpl](../../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImpl.java:70); high. | SDK still calls EMS2 account and entitlement endpoints. Actual consumers remain unproved. | unknown; inventory deployed SDK consumers and migrate applicable calls. |
| Admin ownership | [Token construction](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java:131); [role validation](../../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java:43); high. | CES mapper supplies subjects/actions without a trusted entity role name. Admin ownership still depends on that role. | unknown; define the role or ownership contract before migrating admin entities. |
| Auth disable and failure controls | [Full CES service](../../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/service/Ems3LegacyEntitlementService.java:30); [separate filter service](../../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/service/Ems3EntitlementService.java:60); high. | `enabled`, `disabled-users`, and `fail-closed` do not establish one shared control contract. | unknown; define controls for each path. |
| Mappings and expiry | [Auth settings](../../../repos/services/ratan-auth-server/src/main/resources/application.yml:170); high. | Configured values do not establish approved mappings or acceptable revocation delay. | unknown; supply approved mapping inventory and effective environment settings. |
| Rollout state | Local clean commits only; high. | No deployed CES adoption or production traffic coverage is established. | unknown; identify rollout units, deployed revisions, owners, and operational evidence. |

## Historical DEV and SDK statements

The [29 October user statement](historical-user-inputs-20261028-29.json) reports that migration was completed in DEV.
It does not identify the deployed SDK artifact or its source revision.
The prior assistant guide specifically says that Portal Auth SDK CES support was implemented in DEV.
Evidence: [conversation capture](chatgpt-conversation-20261030.json), turn `d37bb048-d6ff-4e24-a27a-27c7257b4301`, agent message `27c02ac6-f0e7-4daf-ba81-568988216f7c`.
That SDK-specific statement is historical assistant text, not inspected deployment evidence.

The local SDK revision predates that report and still contains EMS2 lookups.
This source does not disprove CES support in a newer or differently deployed SDK.
The concrete action is to bind DEV's SDK artifact to its source revision and inventory its actual consumers.
Owner: unknown. Consequence: the current local source cannot establish final SDK migration completeness.

## Assertion evidence

The following assertions were inspected. Execution status is `NOT_RUN` for this investigation.

| Test source | Inspected assertion | Limit |
| --- | --- | --- |
| [EntitlementDataMigrationTest](../../../repos/services/ratan-auth-server/src/test/java/com/scb/auth/login/migration/EntitlementDataMigrationTest.java:23) | Every mode uses only the EMS2 data reader. | Mocks do not prove external EMS2 availability. |
| [JwtDataEntitlementCompatibilityTest](../../../repos/services/ratan-auth-server/src/test/java/com/scb/auth/login/jwtparser/convertor/JwtDataEntitlementCompatibilityTest.java:42) | JWT actions come from full reads; data roles come from EMS2. | No live token exchange or deployed parity. |
| [JWT data failure assertion](../../../repos/services/ratan-auth-server/src/test/java/com/scb/auth/login/jwtparser/convertor/JwtDataEntitlementCompatibilityTest.java:80) | Data-read failure rejects authentication with PRECONDITION_FAILED. | Inspected assertion, not executed failure proof. |
| [TileAuthorizationServiceImplTest](../../../repos/services/single-ui-bff/src/test/java/com/scb/sso/singleuibff/service/v2/authorization/TileAuthorizationServiceImplTest.java:210) | Grouped CES requests grant only matching application tiles. | Unit fixture; browser and downstream consumers excluded. |
| [Ems3EntitlementsSeparationTest](../../../repos/services/single-ui-bff/src/test/java/com/scb/sso/singleuibff/service/v2/authorization/Ems3EntitlementsSeparationTest.java:40) | Malformed permissions fail. Unrelated CES failures propagate in CES-only mode. | No actual CES service or rollout proof. |

No approved AC inventory exists in this task yet.
AC-to-test and AC-to-code denominators are unresolved, not zero percent or complete.
Code-to-test coverage remains partial source inspection, with no passing-execution claim.

## Historical report applicability

The [27 October review](../../ems3-entitlement-review-20261027/07-code-review.md#comparison-identity) assessed earlier commits.
Its auth head was `3b32ad5a76c1f7c1cdf7bd7b72b3f3c27360b5ce`.
Its BFF head was `19f484efbbfbd4a9d16cdec8a64c4b7fa66e901a`.
Today's heads changed 16 auth files and 39 BFF files against those revisions.

The earlier report identified 15 findings and unavailable compilation dependencies.
It did not execute its focused behavior cases.
Those results cannot establish the current heads' test or defect status.
Evidence: [historical validation](../../ems3-entitlement-review-20261027/07-code-review.md#validation-evidence).

Today's source includes changes in several previously flagged areas.
These include separate EMS2 data reads, configuration preservation, CSV fields, audit columns, and tile-level grants.
This source investigation does not close historical findings or replace a current code review.
A regression review must bind each retained finding to today's source and assertions.

## Material decisions

1. What remains to remove the inspected EMS2 data-role path and applicable SDK calls before final release?
2. Which source approves entitlement-name, admin-role, feature/action, system-account, and data-profile mappings?
3. Which outage and authoritative-denial behavior applies separately to login, tile visibility, and data filtering?
4. Which application groups, tiles, consumers, environments, and accounts define the complete rollout inventory?
5. Which deployed revisions and effective settings establish the baseline and rollback target?

The recovered user intent already resolves the final target: no EMS2 dependencies across RATAN.
The current source therefore leaves an implementation gap against that target.
The owner and completion date for that remaining work are unknown.
Other decision owners remain unknown from inspected sources.
Available code answers implementation questions. It does not approve these business decisions.

## Writing checks

Local source links resolve. Manifest generation completed with recorded SHA-256 values.
These checks do not execute business assertions or approve source meaning.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
  - Source inspection does not establish business approval, deployment, or passing execution.
```
