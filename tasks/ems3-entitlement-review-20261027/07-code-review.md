---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
---

# EMS3 entitlement migration code review

> **Resolve the authorization findings before accepting this migration.**
> Action: Assess the P1 findings and establish corrective ownership.
> Consequence: Application permission mixing, role loss, and authentication failures remain source-predicted risks.
> Owner: unknown. Evidence: [AUTH-01](#auth-01), [AUTH-03](#auth-03), [BFF-001](#bff-001), [BFF-002](#bff-002), and [BFF-003](#bff-003).

> **Behavior execution remains unavailable.**
> Action: Resolve private dependencies and run the focused cases.
> Consequence: This report establishes no passing runtime verification or business acceptance.
> Owner: unknown. Evidence: [validation results](#validation-evidence).

Prepared: 27 October 2026, Asia/Singapore.
Scope and delivery authority: [review request](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/evidence/user-input.md#u-003-review-request) and [document request](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/evidence/user-input.md#u-004-document-request).
Entry record: [intake](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/01-intake.md).

## Findings

All 15 prior review items remain visible below. AUTH-04 is a policy question, not a confirmed fallback defect.
BFF-004 needs a failure-policy decision. AUTH-07 needs compatibility evidence. Priorities express engineering attention, not deployment authorization.

Every behavior result below is a source prediction. No service behavior case was executed.

| Issue | Priority | Classification | Primary comment location |
| --- | --- | --- | --- |
| [AUTH-01](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#auth-01) — Separate data-only reads from full authorization | P1 | Source defect | [Ems3LegacyEntitlementReader.java:19](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/migration/Ems3LegacyEntitlementReader.java:19); lines 19–21; right |
| [AUTH-03](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#auth-03) — Preserve EMS2 role filtering and aggregation | P1 | Source defect | [Ems2LegacyEntitlementReader.java:99](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/migration/Ems2LegacyEntitlementReader.java:99); lines 99–101; right |
| [BFF-001](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#bff-001) — Preserve trusted role identity for admin tokens | P1 | Source defect | [AuthorizationResultMapper.java:46](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/AuthorizationResultMapper.java:46); lines 46–48; right |
| [BFF-002](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#bff-002) — Preserve application boundaries during permission merging | P1 | Source defect | [TileAuthorizationServiceImpl.java:189](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/TileAuthorizationServiceImpl.java:189); lines 189–192; right |
| [BFF-003](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#bff-003) — Preserve settings omitted by legacy tile updates | P1 | Source defect | [ApplicationTileController.java:105](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java:105); lines 105–108; right |
| [AUTH-02](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#auth-02) — Validate data lists at the data-filter boundary | P2 | Source defect; P2 narrowed | [Ems3Repository.java:95](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/repo/Ems3Repository.java:95); lines 95–99; right |
| [AUTH-04](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#auth-04) — Clarify unused EMS3 failure configuration | P2 | Policy question; earlier P1 fallback claim withdrawn | [Ems3Config.java:19](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/configuration/Ems3Config.java:19); lines 19–22; right |
| [AUTH-05](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#auth-05) — Disable raw migration logging by default | P2 | Source defect; operational exposure unverified | [EntitlementMigrationFacade.java:85](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/migration/EntitlementMigrationFacade.java:85); lines 85–89; right |
| [AUTH-06](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#auth-06) — Honor cache disabling and mapping version changes | P2 | Source defect | [RedisEntitlementCacheService.java:39](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/entitlement/cache/RedisEntitlementCacheService.java:39); lines 39–44; right |
| [AUTH-07](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#auth-07) — Resolve removal of the scoped Kong token contract | P2 | Compatibility finding; external consumers unverified | [AuthenticationController.java:207, base side](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/evidence/base-source-excerpts.md#auth-07-base-controller); lines 207–210; left |
| [BFF-004](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#bff-004) — Align advertised fallback with actual failure behavior | P2 | Policy-dependent finding | [TileAuthorizationServiceImpl.java:74](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/TileAuthorizationServiceImpl.java:74); lines 74–78; right |
| [BFF-005](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#bff-005) — Connect entitlement fields to CSV import | P2 | Integration gap; bulk migration intent unconfirmed | [ApplicationTileConfig.java:31](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/dto/config/ApplicationTileConfig.java:31); lines 31–33; right |
| [BFF-006](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#bff-006) — Retain authorization settings in tile audit history | P2 | Source defect | [V1_1_1__application_tile_add_entitlement.sql:2](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/resources/db/migration/V1_1_1__application_tile_add_entitlement.sql:2); lines 2–4; right |
| [BFF-007](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#bff-007) — Compare equivalent authorization scopes | P2 | Source defect | [TileAuthorizationServiceImpl.java:80](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/TileAuthorizationServiceImpl.java:80); lines 80–81; right |
| [BFF-008](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#bff-008) — Remove complete authorization payloads from INFO logs | P2 | Source defect; operational exposure unverified | [AuthorizationResultMapper.java:23](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/AuthorizationResultMapper.java:23); lines 23–23; right |

Use the primary range for an inline review comment. Supporting links identify the remaining cause and consumer paths.
Candidate-side links open current checkout files. Their line numbers apply only to the recorded candidate commits.
Base-side links open retained historical excerpts. Use the specified base revision when placing comments on deleted code.

### AUTH-01

**[P1] Separate data-only reads from full authorization.**

Classification: Source defect. Owner: unknown. Resolution: OPEN.

Comment location: [Ems3LegacyEntitlementReader.java:19](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/migration/Ems3LegacyEntitlementReader.java:19). Range: `19–21`. Side: `right`.

Revision: `3b32ad5a76c1f7c1cdf7bd7b72b3f3c27360b5ce`.

**Trigger.** FMAA authentication includes Bank-Id. The system account succeeds. The bank user has data entitlements but no functional actions.

**Base result.** The EMS2 bank-user lookup returned data roles without requiring functional actions.

**Candidate result.** The EMS3 data reader calls the full mapper. That mapper requires a functional role and at least one action.

**Consequence.** The bank-user lookup throws. Authentication returns an entitlement configuration error.

**Next action.** Add a data-only projection and keep full authorization validation on full reads.

Supporting evidence: [AuthenticationController.java:115](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/controller/AuthenticationController.java:115); [Ems2EntitlementService.java:27](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/service/Ems2EntitlementService.java:27); [DefaultEms3EntitlementMapper.java:51](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/entitlement/mapper/DefaultEms3EntitlementMapper.java:51); [Ems2EntitlementService.java:221, base side](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/evidence/base-source-excerpts.md#auth-01-base-data-read).

**Focused validation.** [TC-AUTH-01](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/06-test-cases.md#tc-auth-01). Definition version: 1. Execution: `NOT_RUN`.
Inspected assertions:

- [Ems3DataEntitlementReaderTest.java:13](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/test/java/com/scb/auth/login/migration/Ems3DataEntitlementReaderTest.java:13): Only checks delegation to a mocked full service; it never runs the mapper.

- [DefaultEms3EntitlementMapperTest.java:87](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/test/java/com/scb/auth/login/entitlement/mapper/DefaultEms3EntitlementMapperTest.java:87): Confirms full mapper rejects missing role actions; no data-only reader integration assertion.

**Confidence and limits.** high, source-predicted conditional failure; not executed.

- Actual production EMS3 data-only payload frequency is unknown.

- A data_profiles-only payload without data_entitlements or role_entitlements is rejected even earlier by repository validation.

**Suggested inline comment**

> This data-only lookup calls the full mapper, which requires functional actions. A bank user with only data entitlements cannot authenticate. Separate data-role projection from full authorization mapping.

**Reviewer response:**

<!-- Add your response here. Leave ownership and disposition unresolved until assigned. -->

### AUTH-03

**[P1] Preserve EMS2 role filtering and aggregation.**

Classification: Source defect. Owner: unknown. Resolution: OPEN.

Comment location: [Ems2LegacyEntitlementReader.java:99](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/migration/Ems2LegacyEntitlementReader.java:99). Range: `99–101`. Side: `right`.

Revision: `3b32ad5a76c1f7c1cdf7bd7b72b3f3c27360b5ce`.

**Trigger.** An uncached ordinary user has multiple roles, or only RATAN_ENTITLEMENT_SUP_USER with a valid action. EMS2_ONLY mode applies.

**Base result.** The ordinary EMS2 service aggregated non-super roles. It rejected accounts with no remaining role.

**Candidate result.** The new reader retains only the first role. It also accepts the previously excluded super-user role.

**Consequence.** Multi-role output loses roles. Previously rejected ordinary entitlement requests can now succeed.

**Next action.** Restore filtering, aggregation, and no-role rejection for ordinary EMS2 service reads.

Supporting evidence: [Ems2EntitlementService.java:137, base side](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/evidence/base-source-excerpts.md#auth-03-base-role-handling); [Ems2EntitlementService.java:16](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/service/Ems2EntitlementService.java:16).

**Focused validation.** [TC-AUTH-03](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/06-test-cases.md#tc-auth-03). Definition version: 1. Execution: `NOT_RUN`.
Inspected assertions:

- [Ems2LegacyEntitlementReaderTest.java:65](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/test/java/com/scb/auth/login/migration/Ems2LegacyEntitlementReaderTest.java:65): Asserts a single ROLE only; no multi-role or SUP_USER assertion.

**Confidence and limits.** high for source behavior change; downstream privilege effect depends on consumers.

- Do not claim every JWT auth path previously filtered SUP_USER: the old X_RATANONE shortcut already selected its first role.

- Scope the regression to migrated Ems2EntitlementService ordinary reads.

- Warm pre-existing cache can defer the changed behavior.

**Suggested inline comment**

> Keeping the first role changes ordinary EMS2 behavior. Main aggregates non-super roles and rejects a super-user-only account. Preserve those semantics for EMS2_ONLY and add both boundary cases.

**Reviewer response:**

<!-- Add your response here. Leave ownership and disposition unresolved until assigned. -->

### BFF-001

**[P1] Preserve trusted role identity for admin tokens.**

Classification: Source defect. Owner: unknown. Resolution: OPEN.

Comment location: [AuthorizationResultMapper.java:46](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/AuthorizationResultMapper.java:46). Range: `46–48`. Side: `right`.

Revision: `19f484efbbfbd4a9d16cdec8a64c4b7fa66e901a`.

**Trigger.** The admin entity comes only from EMS3. No merged EMS2 entity supplies its roleName.

**Base result.** EMS2 entities supplied role metadata used by the existing token and admin validation flow.

**Candidate result.** The EMS3 mapper sets entity names and subjects without roleName. Token construction produces ENTITY:null.

**Consequence.** Admin validation extracts the literal null role. Ownership checks reject records assigned to actual roles.

**Next action.** Implement trusted EMS3 role mapping, or update token creation and admin validation under an approved contract.

Supporting evidence: [EMS2AuthorizationImplementation.java:99](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/implementation/EMS2AuthorizationImplementation.java:99); [JwtAuthenticationController.java:130](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java:130); [AdminModuleUtil.java:53](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java:53); [AdminModuleUtil.java:188](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java:188).

**Focused validation.** [TC-BFF-001](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/06-test-cases.md#tc-bff-001). Definition version: 1. Execution: `NOT_RUN`.
Inspected assertions:

- [AuthorizationResultMapperTest.java:36](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/test/java/com/scb/sso/singleuibff/service/v2/authorization/AuthorizationResultMapperTest.java:36): Asserts entity names, actions, and subject names. It does not assert roleName or admin token compatibility.

**Confidence and limits.** high for stated source flow; behavior execution NOT_RUN.

- Requires migration of the configured admin-module entity. Existing EMS2-only admin configuration can mask this failure.

- The trusted EMS3-to-admin-role policy is unavailable. A tile owner string must not be treated automatically as a granted user role.

**Suggested inline comment**

> EMS3 entities have no roleName. Admin token construction emits ENTITY:null, and ownership checks then use null as the role. Preserve trusted role identity across mapping and admin validation.

**Reviewer response:**

<!-- Add your response here. Leave ownership and disposition unresolved until assigned. -->

### BFF-002

**[P1] Preserve application boundaries during permission merging.**

Classification: Source defect. Owner: unknown. Resolution: OPEN.

Comment location: [TileAuthorizationServiceImpl.java:189](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/TileAuthorizationServiceImpl.java:189). Range: `189–192`. Side: `right`.

Revision: `19f484efbbfbd4a9d16cdec8a64c4b7fa66e901a`.

**Trigger.** Apps A and B share entity E. Both tiles require subject S. A grants S:read; B grants only T:read.

**Base result.** No per-tile EMS3 application routing existed. Permissions came from the EMS2 entity authorization model.

**Candidate result.** Both EMS3 responses pass validation. Merge combines their subjects using only entity name E.

**Consequence.** App B tile passes subject filtering using S from app A. App B did not grant S.

**Next action.** Preserve application or tile identity through mapping, merging, token creation, and drawer filtering.

Supporting evidence: [TileAuthorizationServiceImpl.java:116](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/TileAuthorizationServiceImpl.java:116); [TileAuthorizationServiceImpl.java:195](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/TileAuthorizationServiceImpl.java:195); [AuthorizationResultMapper.java:46](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/AuthorizationResultMapper.java:46); [AdminModuleUtil.java:115](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java:115); [Ems3EntitlementService.java:198](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/filter/ems3/Ems3EntitlementService.java:198); [AuthFilterExecutor.java:84](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/filter/AuthFilterExecutor.java:84).

**Focused validation.** [TC-BFF-002](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/06-test-cases.md#tc-bff-002). Definition version: 1. Execution: `NOT_RUN`.
Inspected assertions:

- [TileAuthorizationServiceImplTest.java:151](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/test/java/com/scb/sso/singleuibff/service/v2/authorization/TileAuthorizationServiceImplTest.java:151): Explicitly verifies subjects/actions are unioned for shared entities. It does not test same entity across distinct EMS3 apps with one missing required subject.

**Confidence and limits.** high for stated source flow; behavior execution NOT_RUN.

- Both responses must contain a role item. A completely empty app B role list throws before the final union and is not the leakage trigger.

- Use tiles without a further data filter, or users for whom that filter does not remove the tile. Exposure concerns tiles and issued permission tokens; backend data access was not tested.

**Suggested inline comment**

> Merging by entity name discards application identity. If A grants S and B grants only T for entity E, B gains S through the union. Preserve application boundaries through the final tile filter.

**Reviewer response:**

<!-- Add your response here. Leave ownership and disposition unresolved until assigned. -->

### BFF-003

**[P1] Preserve settings omitted by legacy tile updates.**

Classification: Source defect. Owner: unknown. Resolution: OPEN.

Comment location: [ApplicationTileController.java:105](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java:105). Range: `105–108`. Side: `right`.

Revision: `19f484efbbfbd4a9d16cdec8a64c4b7fa66e901a`.

**Trigger.** A normal edit updates an existing EMS3 tile. The legacy JSON payload omits all three entitlement fields.

**Base result.** The base had no provider fields. An ordinary edit could not change an authorization provider.

**Candidate result.** The DTO defaults omitted source to EMS2. The controller writes EMS2 and clears both application fields.

**Consequence.** An unrelated content edit changes authorization settings. The changed provider takes effect after later tile activation.

**Next action.** Distinguish omitted fields from explicit provider changes. Preserve stored settings when fields are absent.

Supporting evidence: [RequestOfApplicationTile.java:31](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/dto/request/RequestOfApplicationTile.java:31); [ApplicationTileController.java:109](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java:109); [ApplicationTileController.java:61](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java:61).

**Focused validation.** [TC-BFF-003](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/06-test-cases.md#tc-bff-003). Definition version: 1. Execution: `NOT_RUN`.
Inspected assertions:

- [ApplicationTileControllerTest.java:463](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/test/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileControllerTest.java:463): Rejects an explicit EMS3 request missing application configuration. Does not check omitted fields against a stored EMS3 tile.

**Confidence and limits.** high for stated source flow; behavior execution NOT_RUN.

- Applies to normal edit mode. Checker and deactivate branches skip these writes. The update sets active=false, so exposure follows later activation.

**Suggested inline comment**

> Legacy payloads omit these fields, so the DTO supplies EMS2. This update overwrites the stored EMS3 source and clears application fields. Preserve stored settings when fields are absent.

**Reviewer response:**

<!-- Add your response here. Leave ownership and disposition unresolved until assigned. -->

### AUTH-02

**[P2] Validate data lists at the data-filter boundary.**

Classification: Source defect; P2 narrowed. Owner: unknown. Resolution: OPEN.

Comment location: [Ems3Repository.java:95](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/repo/Ems3Repository.java:95). Range: `95–99`. Side: `right`.

Revision: `3b32ad5a76c1f7c1cdf7bd7b72b3f3c27360b5ce`.

**Trigger.** A matching EMS3 response contains functional actions and null data_entitlements. The data-filter cache is empty.

**Base result.** Repository validation rejected the payload with an explicit invalid-response error.

**Candidate result.** Repository validation accepts the payload. The data-filter converter dereferences the null data list.

**Consequence.** The endpoint fails with NullPointerException instead of its explicit invalid-response contract. The base path also returned an error.

**Next action.** Validate data_entitlements within the data-filter service. Define the intended response for users without data permissions.

Supporting evidence: [Ems3EntitlementService.java:114](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/service/Ems3EntitlementService.java:114); [Ems3Repository.java:95, base side](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/evidence/base-source-excerpts.md#auth-02-base-response-validation); [Ems3Error.java:7](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/exceptions/Ems3Error.java:7).

**Focused validation.** [TC-AUTH-02](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/06-test-cases.md#tc-auth-02). Definition version: 1. Execution: `NOT_RUN`.
Inspected assertions:

- [Ems3RepositoryTest.java:79](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/test/java/com/scb/auth/login/repo/Ems3RepositoryTest.java:79): Checks both lists empty, not functional-only responses.

- [Ems3EntitlementServiceTest.java:109](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/test/java/com/scb/auth/login/service/Ems3EntitlementServiceTest.java:109): Success fixture always supplies data_entitlements.

**Confidence and limits.** high for null dereference; no runtime execution.

- Do not describe this as a previously successful endpoint becoming HTTP 500. The old missing-data path also rejected the response with an error carrying status 500.

- No approved behavior defines whether functional-only users should receive empty filters or an explicit error.

**Suggested inline comment**

> Role-only responses now pass this validation, but the data-filter caller dereferences data_entitlements. Preserve endpoint-specific validation before conversion. The previous path also rejected this payload; this finding concerns null handling and error classification.

**Reviewer response:**

<!-- Add your response here. Leave ownership and disposition unresolved until assigned. -->

### AUTH-04

**[P2] Clarify unused EMS3 failure configuration.**

Classification: Policy question; earlier P1 fallback claim withdrawn. Owner: unknown. Resolution: OPEN.

Comment location: [Ems3Config.java:19](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/configuration/Ems3Config.java:19). Range: `19–22`. Side: `right`.

Revision: `3b32ad5a76c1f7c1cdf7bd7b72b3f3c27360b5ce`.

**Trigger.** An operator sets fail-closed=false while migration reads EMS3. Existing enabled and disabled-users settings also need scope clarification.

**Base result.** Enabled and disabled-user settings controlled the separate data-filter API. No full-auth EMS3 migration policy existed.

**Candidate result.** The new failClosed property has no consumer. Migration code deliberately propagates EMS3 failures.

**Consequence.** Changing fail-closed has no effect. Available tests contradict the earlier claim that fallback is required.

**Next action.** Document each setting scope. Remove the unused property or implement an approved failure policy.

Supporting evidence: [Ems3LegacyEntitlementService.java:25](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/service/Ems3LegacyEntitlementService.java:25); [Ems3EntitlementService.java:60](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/service/Ems3EntitlementService.java:60); [EntitlementDualReadExecutor.java:72](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/migration/EntitlementDualReadExecutor.java:72).

**Focused validation.** [TC-AUTH-04](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/06-test-cases.md#tc-auth-04). Definition version: 1. Execution: `NOT_RUN`.
Inspected assertions:

- [EntitlementDataMigrationTest.java:70](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/test/java/com/scb/auth/login/migration/EntitlementDataMigrationTest.java:70): Explicitly asserts no EMS2 fallback after modern failure.

- [Ems3EntitlementServiceTest.java:55](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/test/java/com/scb/auth/login/service/Ems3EntitlementServiceTest.java:55): Tests disable flags only on the data-filter service.

**Confidence and limits.** high for unused configuration; fallback requirement unestablished.

- Downgrade the earlier P1 fallback defect to an unresolved policy/configuration question.

- The test dualReadNeverFallsBackAfterModernFailure explicitly requires modern failure propagation.

- Do not imply EMS2 fallback is required by EMS3_PRIMARY_DUAL_READ alone.

- Data-filter-only enabled/disabled semantics predate this patch.

**Suggested inline comment**

> The new failClosed setting has no consumer. Tests explicitly require no EMS2 fallback after EMS3 failure. Clarify the property contract and disable-setting scope before changing failure behavior.

**Reviewer response:**

<!-- Add your response here. Leave ownership and disposition unresolved until assigned. -->

### AUTH-05

**[P2] Disable raw migration logging by default.**

Classification: Source defect; operational exposure unverified. Owner: unknown. Resolution: OPEN.

Comment location: [EntitlementMigrationFacade.java:85](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/migration/EntitlementMigrationFacade.java:85). Range: `85–89`. Side: `right`.

Revision: `3b32ad5a76c1f7c1cdf7bd7b72b3f3c27360b5ce`.

**Trigger.** Default dual-read succeeds while INFO logging is enabled. Detailed and raw diagnostic flags retain their shipped values.

**Base result.** Baseline services already logged some entitlements. Migration comparison and cache dumps did not exist.

**Candidate result.** The migration path adds raw cache payloads, role actions, and data roles to INFO logs.

**Consequence.** Log readers receive additional user authorization metadata. Unauthorized log access has not been demonstrated.

**Next action.** Default raw diagnostics off. Prefer comparison status and counts, with approved redaction for exceptional diagnostics.

Supporting evidence: [application.yml:157](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/main/resources/application.yml:157); [EntitlementMigrationFacade.java:80](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/migration/EntitlementMigrationFacade.java:80); [DefaultEms3EntitlementMapper.java:63](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/entitlement/mapper/DefaultEms3EntitlementMapper.java:63).

**Focused validation.** [TC-AUTH-05](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/06-test-cases.md#tc-auth-05). Definition version: 1. Execution: `NOT_RUN`.
Existing assertion evidence: No matching log-content assertion was found in the inspected tests.

**Confidence and limits.** high for logged data; production log exposure policy unknown.

- Do not present Ems3Repository response logging as newly introduced; it exists in main.

- No deployed log configuration or organization data-classification policy was inspected.

- Severity P1 was not supported by confirmed unauthorized log access.

**Suggested inline comment**

> Default migration settings enable these raw cache dumps at INFO. This adds user authorization and data-role details to logs. Disable raw diagnostics by default and use aggregate comparison information.

**Reviewer response:**

<!-- Add your response here. Leave ownership and disposition unresolved until assigned. -->

### AUTH-06

**[P2] Honor cache disabling and mapping version changes.**

Classification: Source defect. Owner: unknown. Resolution: OPEN.

Comment location: [RedisEntitlementCacheService.java:39](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/entitlement/cache/RedisEntitlementCacheService.java:39). Range: `39–44`. Side: `right`.

Revision: `3b32ad5a76c1f7c1cdf7bd7b72b3f3c27360b5ce`.

**Trigger.** An EMS3 cache entry exists when cache.enabled=false. Alternatively, the configured mapping version changes before the entry expires.

**Base result.** The shared EMS3 projection cache and mapping-version setting did not exist.

**Candidate result.** Cache reads and writes ignore enabled. Cache reads accept obsolete versions. The mapper hardcodes ems3-v1.

**Consequence.** Disabled caching still serves cached permissions. Mapping changes can reuse an obsolete authorization projection.

**Next action.** Bypass projection caching when disabled. Bind versions to configuration and reject obsolete cached projections.

Supporting evidence: [EntitlementCacheProperties.java:12](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/configuration/EntitlementCacheProperties.java:12); [EntitlementMappingProperties.java:17](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/configuration/EntitlementMappingProperties.java:17); [DefaultEms3EntitlementMapper.java:22](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/entitlement/mapper/DefaultEms3EntitlementMapper.java:22); [RedisEntitlementCacheService.java:59](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/entitlement/cache/RedisEntitlementCacheService.java:59).

**Focused validation.** [TC-AUTH-06](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/06-test-cases.md#tc-auth-06). Definition version: 1. Execution: `NOT_RUN`.
Inspected assertions:

- [RedisEntitlementCacheServiceTest.java:39](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/test/java/com/scb/auth/login/entitlement/cache/RedisEntitlementCacheServiceTest.java:39): Accepts an envelope version v and generated timestamp 1; no age/version/disable checks.

**Confidence and limits.** high for ignored controls and version; staleMaxAge policy unresolved.

- staleMaxAgeSeconds is unused, but its name does not establish a maximum age for all normal cache hits. Do not claim every hit older than 300 seconds violates policy.

- A revocation remaining until configured TTL is normal cache behavior unless a stronger freshness rule exists.

- The explicit disabled flag and mapping-version control are the supported defect scope.

**Suggested inline comment**

> Cache reads ignore enabled and accept envelopes without checking the configured mapping version. The mapper also hardcodes ems3-v1. Honor disabling and reject old mapping versions before returning cached permissions.

**Reviewer response:**

<!-- Add your response here. Leave ownership and disposition unresolved until assigned. -->

### AUTH-07

**[P2] Resolve removal of the scoped Kong token contract.**

Classification: Compatibility finding; external consumers unverified. Owner: unknown. Resolution: OPEN.

Comment location: [AuthenticationController.java:207, base side](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/evidence/base-source-excerpts.md#auth-07-base-controller). Range: `207–210`. Side: `left`.

Revision: `7e8cbfa49051ffcd4cd4aa87a6382edfaf8daaee`.

**Trigger.** A client requests GET /v4/kong/token with a custom scope.

**Base result.** The controller exposed the v4 route. Its service forwarded custom scope to Kong. Base tests asserted this contract.

**Candidate result.** The route and scoped overload are deleted. The remaining v3 route requests one fixed scope.

**Consequence.** Existing v4 clients lose the route. Switching to v3 cannot preserve custom scope requests.

**Next action.** Restore compatibility or provide approved retirement and consumer migration evidence.

Supporting evidence: [KongGatewayAuthService.java:58](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/service/KongGatewayAuthService.java:58); [KongGatewayAuthService.java:80](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/service/KongGatewayAuthService.java:80).

**Focused validation.** [TC-AUTH-07](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/06-test-cases.md#tc-auth-07). Definition version: 1. Execution: `NOT_RUN`.
Inspected assertions:

- [AuthenticationControllerTest.java:59, base side](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/evidence/base-source-excerpts.md#auth-07-base-controller-test): Deleted test asserts /v4/kong/token with scope returns HTTP 200.

- [KongGatewayAuthServiceTest.java:74, base side](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/evidence/base-source-excerpts.md#auth-07-base-scope-test): Deleted test asserts custom.scope in outbound token request.

**Confidence and limits.** high for removed contract; external use and approved deprecation unknown.

- No in-repository production caller or deployed usage evidence found.

- Deletion comment must bind to main/base left-side lines 207-210, not current lines 202-204.

- The deleted main test is contract evidence, not a currently runnable assertion.

**Suggested inline comment**

> This deletion removes the tested v4 scoped-token contract. Existing clients lose the route, and v3 uses a fixed scope. Restore the contract or provide retirement and consumer migration evidence.

**Reviewer response:**

<!-- Add your response here. Leave ownership and disposition unresolved until assigned. -->

### BFF-004

**[P2] Align advertised fallback with actual failure behavior.**

Classification: Policy-dependent finding. Owner: unknown. Resolution: OPEN.

Comment location: [TileAuthorizationServiceImpl.java:74](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/TileAuthorizationServiceImpl.java:74). Range: `74–78`. Side: `right`.

Revision: `19f484efbbfbd4a9d16cdec8a64c4b7fa66e901a`.

**Trigger.** A migrated tile has an EMS2 equivalent. In dual-read mode, its EMS3 call fails during an outage.

**Base result.** The base queried EMS2 for all configured tile entities.

**Candidate result.** EMS2 reads exclude migrated scopes. The catch logs fallback without reading those failed scopes.

**Consequence.** Migrated tiles disappear. With only migrated tiles, the result is empty despite the fallback message.

**Next action.** Establish the outage policy. Implement approved fallback per scope, or report deliberate fail-closed behavior accurately.

Supporting evidence: [TileAuthorizationServiceImpl.java:66](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/TileAuthorizationServiceImpl.java:66); [TileAuthorizationServiceImpl.java:80](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/TileAuthorizationServiceImpl.java:80).

**Focused validation.** [TC-BFF-004](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/06-test-cases.md#tc-bff-004). Definition version: 1. Execution: `NOT_RUN`.
Inspected assertions:

- [TileAuthorizationServiceImplTest.java:164](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/test/java/com/scb/sso/singleuibff/service/v2/authorization/TileAuthorizationServiceImplTest.java:164): The test named dualReadFallsBackToEms2WhenEms3Fails explicitly expects only the legacy entity. It establishes current behavior, not a business fallback requirement.

**Confidence and limits.** high for stated source flow; behavior execution NOT_RUN.

- Fallback policy is not supplied. Fail-closed behavior may be intended. This is a concrete mismatch with the log and migration fallback claim; approval of fail-open behavior is unavailable.

- Do not automatically grant EMS2 permissions after EMS3 denial. Any fallback policy must separate outage from authoritative denial.

**Suggested inline comment**

> This catch advertises EMS2 fallback, but EMS2 reads exclude migrated scopes. Failed migrated tiles disappear. Confirm the outage policy, then implement per-scope fallback or describe deliberate fail-closed behavior accurately.

**Reviewer response:**

<!-- Add your response here. Leave ownership and disposition unresolved until assigned. -->

### BFF-005

**[P2] Connect entitlement fields to CSV import.**

Classification: Integration gap; bulk migration intent unconfirmed. Owner: unknown. Resolution: OPEN.

Comment location: [ApplicationTileConfig.java:31](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/dto/config/ApplicationTileConfig.java:31). Range: `31–33`. Side: `right`.

Revision: `19f484efbbfbd4a9d16cdec8a64c4b7fa66e901a`.

**Trigger.** An operator uses CSV upload to create or migrate an EMS3 tile.

**Base result.** CSV supported legacy tile fields and persisted EMS2 configuration.

**Candidate result.** The DTO adds entitlement fields. Fixed headers, parsing, and persistence do not consume them.

**Consequence.** New imported tiles default to EMS2. Existing records retain their previous settings; CSV cannot migrate their source.

**Next action.** Extend the CSV contract, validation, parser, and persistence. Alternatively, reject unsupported entitlement columns explicitly.

Supporting evidence: [Constant.java:29](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/Constant.java:29); [CsvUtility.java:113](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/CsvUtility.java:113); [ApplicationConfigController.java:199](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationConfigController.java:199); [ApplicationConfigController.java:230](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationConfigController.java:230); [ApplicationTile.java:80](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/entity/ApplicationTile.java:80).

**Focused validation.** [TC-BFF-005](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/06-test-cases.md#tc-bff-005). Definition version: 1. Execution: `NOT_RUN`.
Inspected assertions:

- [ApplicationConfigControllerTest.java:72](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/test/java/com/scb/sso/singleuibff/controller/v1/ApplicationConfigControllerTest.java:72): Mocks CsvUtility and checks upload HTTP success for legacy fields. It does not inspect EMS3 fields from CSV bytes or persisted entities.

**Confidence and limits.** high for stated source flow; behavior execution NOT_RUN.

- Previous wording that all CSV uploads reset entitlement settings was too broad. Existing records preserve fields because the controller never writes them.

- Whether EMS3 CSV import belongs to approved scope is not supplied. The added bulk config DTO fields indicate unfinished plumbing.

**Suggested inline comment**

> These bulk-import fields are never parsed or persisted. New CSV-created tiles default to EMS2; existing records keep their old settings. Complete the import path or reject unsupported entitlement columns explicitly.

**Reviewer response:**

<!-- Add your response here. Leave ownership and disposition unresolved until assigned. -->

### BFF-006

**[P2] Retain authorization settings in tile audit history.**

Classification: Source defect. Owner: unknown. Resolution: OPEN.

Comment location: [V1_1_1__application_tile_add_entitlement.sql:2](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/resources/db/migration/V1_1_1__application_tile_add_entitlement.sql:2). Range: `2–4`. Side: `right`.

Revision: `19f484efbbfbd4a9d16cdec8a64c4b7fa66e901a`.

**Trigger.** An operator creates a tile or changes its entitlement source or application through REST.

**Base result.** Audit records retained the supported legacy authorization fields.

**Candidate result.** Only the live table gains the three new fields. Audit schema, entity, and builders omit them.

**Consequence.** Historical audit responses cannot reconstruct which source and application applied to a change.

**Next action.** Extend audit columns, entity fields, and both audit builders alongside the live-table changes.

Supporting evidence: [ApplicationTile.java:80](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/entity/ApplicationTile.java:80); [ApplicationTileAudit.java:71](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/entity/ApplicationTileAudit.java:71); [ApplicationTileController.java:247](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java:247); [ApplicationConfigController.java:248](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationConfigController.java:248).

**Focused validation.** [TC-BFF-006](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/06-test-cases.md#tc-bff-006). Definition version: 1. Execution: `NOT_RUN`.
Inspected assertions:

- [ApplicationTileControllerTest.java:236](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/test/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileControllerTest.java:236): Checks successful audit endpoint response with an empty mocked result. It does not assert entitlement source or app history.

**Confidence and limits.** high for stated source flow; behavior execution NOT_RUN.

- No production audit policy document was supplied. The repository guide states all admin actions have audit logging. This finding concerns missing reconstruction fields, not absent audit rows.

**Suggested inline comment**

> Only the live table receives authorization source and application fields. Audit records omit them, so historical configuration cannot be reconstructed. Extend the audit schema, entity, and builders.

**Reviewer response:**

<!-- Add your response here. Leave ownership and disposition unresolved until assigned. -->

### BFF-007

**[P2] Compare equivalent authorization scopes.**

Classification: Source defect. Owner: unknown. Resolution: OPEN.

Comment location: [TileAuthorizationServiceImpl.java:80](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/TileAuthorizationServiceImpl.java:80). Range: `80–81`. Side: `right`.

Revision: `19f484efbbfbd4a9d16cdec8a64c4b7fa66e901a`.

**Trigger.** Dual-read contains distinct legacy and migrated entities, or only migrated entities with nonempty permissions.

**Base result.** No EMS2-to-EMS3 parity comparison existed.

**Candidate result.** The caller compares non-migrated EMS2 scopes with migrated EMS3 scopes as complete permission sets.

**Consequence.** Routing differences become reported permission differences. A fully migrated configuration compares populated EMS3 results against empty EMS2 results.

**Next action.** Shadow-read equivalent scopes. Report unavailable baselines separately from permission mismatches.

Supporting evidence: [TileAuthorizationServiceImpl.java:58](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/TileAuthorizationServiceImpl.java:58); [AuthorizationComparisonService.java:28](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/AuthorizationComparisonService.java:28); [AuthorizationComparisonService.java:54](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/AuthorizationComparisonService.java:54).

**Focused validation.** [TC-BFF-007](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/06-test-cases.md#tc-bff-007). Definition version: 1. Execution: `NOT_RUN`.
Inspected assertions:

- [AuthorizationComparisonServiceTest.java:46](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/test/java/com/scb/sso/singleuibff/service/v2/authorization/AuthorizationComparisonServiceTest.java:46): Injects matching canonical sets. It does not check that both sources query the same tile scope.

**Confidence and limits.** high for stated source flow; behavior execution NOT_RUN.

- Mixed scopes are not necessarily disjoint when entity names overlap. The finding applies to ordinary distinct entity scopes and all-migrated configurations with nonempty grants.

- A complete business parity definition is unavailable. These logs cannot substantiate source equivalence.

**Suggested inline comment**

> These permission sets cover different tile scopes. Comparing them produces routing-induced DIFFs, including empty EMS2 versus populated EMS3 after full migration. Compare equivalent scopes or report missing baselines separately.

**Reviewer response:**

<!-- Add your response here. Leave ownership and disposition unresolved until assigned. -->

### BFF-008

**[P2] Remove complete authorization payloads from INFO logs.**

Classification: Source defect; operational exposure unverified. Owner: unknown. Resolution: OPEN.

Comment location: [AuthorizationResultMapper.java:23](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/AuthorizationResultMapper.java:23). Range: `23–23`. Side: `right`.

Revision: `19f484efbbfbd4a9d16cdec8a64c4b7fa66e901a`.

**Trigger.** EMS3 functional authorization succeeds with normal INFO logging enabled.

**Base result.** Baseline data-filter logging existed. The new functional payload and merged authorization logs did not exist.

**Candidate result.** The mapper logs raw responses and permission sets. Merge and login paths log complete entitlement results.

**Consequence.** User-to-permission mappings enter logs. Actual log access controls and retention were not inspected.

**Next action.** Use status, counts, and correlation identifiers. Gate redacted diagnostics with explicit configuration.

Supporting evidence: [AuthorizationResultMapper.java:40](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/AuthorizationResultMapper.java:40); [TileAuthorizationServiceImpl.java:167](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/TileAuthorizationServiceImpl.java:167); [JwtAuthenticationController.java:105](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java:105); [AuthorizationComparisonService.java:31](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/AuthorizationComparisonService.java:31).

**Focused validation.** [TC-BFF-008](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/06-test-cases.md#tc-bff-008). Definition version: 1. Execution: `NOT_RUN`.
Existing assertion evidence: No matching log-content assertion was found in the inspected tests.

**Confidence and limits.** high for stated source flow; behavior execution NOT_RUN.

- Log destination, retention, access controls, and approved logging policy were not inspected. No unauthorized reader or credential exposure was demonstrated.

- The concrete source fact is expanded entitlement payload logging. Security impact depends on operational log controls.

**Suggested inline comment**

> This INFO statement logs the complete functional authorization response. New merge and login logs also publish permission sets. Replace payloads with counts and status, and verify default log content.

**Reviewer response:**

<!-- Add your response here. Leave ownership and disposition unresolved until assigned. -->

## Purpose of the changes

The following purpose comes from code and configuration. It does not establish approved business requirements.

Auth moves full and data-role entitlement reads behind an EMS2/EMS3 migration facade.
It adds source selection, bounded dual reads, mapping into legacy fields, Redis projection caching, and comparison diagnostics.
JWT and FMAA paths now use the facade. The patch also removes the scoped Kong route.
Evidence: [facade](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/migration/EntitlementMigrationFacade.java:33), [mapper](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/entitlement/mapper/DefaultEms3EntitlementMapper.java:27), and [Kong removal](#auth-07).

BFF adds tile source, application ID, and application name fields.
It routes tile authorization by source, groups EMS3 requests by application, and converts grants into the existing entity model.
It also adds permission comparison and live-table migration fields.
Evidence: [routing](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/TileAuthorizationServiceImpl.java:44), [mapping](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/AuthorizationResultMapper.java:18), and [database migration](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff/src/main/resources/db/migration/V1_1_1__application_tile_add_entitlement.sql:1).

## Comparison identity

Comparison mode: `branch`. Target: local `main`. Both merge bases equal their recorded target commits.
Branch in both services: `codex/apply-service-diffs-20261027`. No remote-main freshness or PR identity was established.

| Repository | Base and merge base | Candidate | Changed paths | Change fingerprint |
| --- | --- | --- | --- | --- |
| [auth](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/ratan-auth-server) | `7e8cbfa49051ffcd4cd4aa87a6382edfaf8daaee` | `3b32ad5a76c1f7c1cdf7bd7b72b3f3c27360b5ce` | 63 | `89d141c2d233b830acd43f4663a3a223f822b80e84a472c8efb32f57471818f8` |
| [bff](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/services/single-ui-bff) | `834b4155232222347220e47139a502ee43a9cbdf` | `19f484efbbfbd4a9d16cdec8a64c4b7fa66e901a` | 32 | `3da98fe07cc6cd892206c4be9a8c4d2f2c10862a8b794fbe44c3ff09442490df` |

Untracked supplied patch files remain in each service: `diff` and `diff-bff`. They are excluded from the committed comparison.
Workbench has unrelated `core/release-report/` content. This documentation stage preserves it.
No service source, branch, or commit changed during documentation.

## Review coverage

Exact changed-path inventories and content hashes: [auth](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/evidence/auth-context.json) and [BFF](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/evidence/bff-context.json).
This document retains the prior review and independently checks the 15 finding chains and comment locations.
The prior review covered selected diffs and consumers. This documentation stage does not repeat an exhaustive review of all 95 paths.

Findings cover authentication, role projection, application isolation, tile edits, import, audit, cache controls, and diagnostics.
Independent evidence: [auth audit](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/evidence/auth-comment-audit.json) and [BFF audit](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/evidence/bff-comment-audit.json).

Compilation, live integrations, database migrations, browser flows, and runtime policy were not verified.
No dependency vulnerability analyzer, production logging audit, or deployed revision check was performed.
BFF guide references an absent `.github/copilot-instructions.md`. Its additional instructions were unavailable.

## Validation evidence

| Check | Auth | BFF | Evidence and limit |
| --- | --- | --- | --- |
| Context and branch identities | PASSED | PASSED | [Auth context](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/evidence/auth-context.json); [BFF context](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/evidence/bff-context.json). Local commits only. |
| Secret-pattern scan | No candidates | No candidates | [Auth scan](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/evidence/auth-scan.json); [BFF scan](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/evidence/bff-scan.json). Does not prove credential absence. |
| YAML parse | PASSED | PASSED | [Auth YAML](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/evidence/auth-yaml.log); [BFF YAML](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/evidence/bff-yaml.log). Syntax only. |
| `git diff --check main...HEAD` | PASSED | FAILED | [Auth log](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/evidence/auth-diff-check.log); [BFF log](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/evidence/bff-diff-check.log). BFF reports whitespace on added CRLF lines. |
| `mvn -o -DskipTests compile` | BLOCKED | BLOCKED | [Auth build](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/evidence/auth-compile.log); [BFF build](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/evidence/bff-compile.log). Dependency resolution stops before compilation. |
| Focused behavior cases | NOT_RUN | NOT_RUN | No passing execution or deployed parity evidence exists. |

Auth lacks private BOM `com.scb.ratan:ratanone-dependencies:6.7.2` and its managed versions.
BFF lacks private service and HashiCorp starter artifacts at `6.3.1`.
Exact commands, timestamps, exit codes, and output hashes: [validation manifest](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/evidence/validation.json).

## Coverage mappings

No approved business AC inventory was supplied. Both AC denominators are `UNKNOWN`, not zero.
Proposed case definitions do not establish business acceptance or implementation conformance.

### AC-to-test coverage

| AC denominator | Case definitions | Inspected assertion coverage | Passing execution |
| --- | --- | --- | --- |
| UNKNOWN; approved AC definitions unavailable | 15 finding-focused definitions | Partial, missing, or contrary assertions are listed per finding | 0 case executions; no conformance percentage |

### AC-to-code-change coverage

| AC denominator | Code evidence | Conformance |
| --- | --- | --- |
| UNKNOWN; approved AC definitions unavailable | 95 identified changed paths at exact commits | UNKNOWN; links do not prove business equivalence |

### Code-change-to-test coverage

The denominator below is 15 review boundaries. It is not all changed units or all business behaviors.
Each row links its source, inspected assertion evidence, and separate proposed case definition.

| Review boundary and source/assertion evidence | Canonical focused case | Execution |
| --- | --- | --- |
| [AUTH-01](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#auth-01) | [TC-AUTH-01](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/06-test-cases.md#tc-auth-01) | NOT_RUN |
| [AUTH-02](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#auth-02) | [TC-AUTH-02](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/06-test-cases.md#tc-auth-02) | NOT_RUN |
| [AUTH-03](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#auth-03) | [TC-AUTH-03](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/06-test-cases.md#tc-auth-03) | NOT_RUN |
| [AUTH-04](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#auth-04) | [TC-AUTH-04](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/06-test-cases.md#tc-auth-04) | NOT_RUN |
| [AUTH-05](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#auth-05) | [TC-AUTH-05](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/06-test-cases.md#tc-auth-05) | NOT_RUN |
| [AUTH-06](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#auth-06) | [TC-AUTH-06](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/06-test-cases.md#tc-auth-06) | NOT_RUN |
| [AUTH-07](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#auth-07) | [TC-AUTH-07](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/06-test-cases.md#tc-auth-07) | NOT_RUN |
| [BFF-001](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#bff-001) | [TC-BFF-001](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/06-test-cases.md#tc-bff-001) | NOT_RUN |
| [BFF-002](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#bff-002) | [TC-BFF-002](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/06-test-cases.md#tc-bff-002) | NOT_RUN |
| [BFF-003](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#bff-003) | [TC-BFF-003](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/06-test-cases.md#tc-bff-003) | NOT_RUN |
| [BFF-004](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#bff-004) | [TC-BFF-004](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/06-test-cases.md#tc-bff-004) | NOT_RUN |
| [BFF-005](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#bff-005) | [TC-BFF-005](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/06-test-cases.md#tc-bff-005) | NOT_RUN |
| [BFF-006](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#bff-006) | [TC-BFF-006](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/06-test-cases.md#tc-bff-006) | NOT_RUN |
| [BFF-007](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#bff-007) | [TC-BFF-007](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/06-test-cases.md#tc-bff-007) | NOT_RUN |
| [BFF-008](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#bff-008) | [TC-BFF-008](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/06-test-cases.md#tc-bff-008) | NOT_RUN |

## Corrections and unresolved decisions

| Item | Correction or unresolved decision | Owner and next action |
| --- | --- | --- |
| [AUTH-04](#auth-04) | Earlier mandatory fallback claim is withdrawn. A current test explicitly requires failure propagation. | unknown; define setting scope |
| [AUTH-02](#auth-02) | Base also rejected missing data. The defect concerns null handling and explicit error classification. | unknown; define no-data response |
| [AUTH-05](#auth-05) | Priority narrowed to P2. Baseline repository response logs are excluded from the introduced finding. | unknown; apply logging policy |
| [AUTH-06](#auth-06) | No universal 300-second freshness rule is inferred from staleMaxAgeSeconds. | unknown; define stale-data policy separately |
| [AUTH-07](#auth-07) | Route removal is established. External usage and approved retirement remain unknown. | unknown; inspect consumers and retirement evidence |
| [BFF-002](#bff-002) | Reachable trigger requires a nonempty unrelated permission from app B. Empty roles would fail validation earlier. | unknown; test application isolation |
| [BFF-004](#bff-004) | Fallback is policy-dependent. Current assertions expect only unrelated legacy scopes after failure. | unknown; separate outage from denial |
| [BFF-005](#bff-005) | Existing CSV records retain source settings. Newly imported records default to EMS2. | unknown; define import scope |
| Ownership | Earlier component names did not establish accountable owners. | unknown; assign ownership |

No answer is required to deliver this document. Business-policy decisions remain open for implementation and acceptance.
Human review decision: pending. Approval evidence: null. Findings remain open.

Documentation checks: [document-checks.json](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/evidence/document-checks.json).
Source identities: [source-manifest.json](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/evidence/source-manifest.json).
Final service identity check: [final-identity.json](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/evidence/final-identity.json).

Authored documents and JSON pass the staged whitespace check. Raw logs and historical excerpts retain captured whitespace.
Evidence: [staged-diff-check.json](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/evidence/staged-diff-check.json).
