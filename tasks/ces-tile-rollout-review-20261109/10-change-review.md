---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Service migration code review

> **Four findings remain open. BFF dependency initialization fails in controlled execution.**
> Action: align dependencies and correct the affected rollout paths. Owner: unknown.
> Consequence: service initialization and tile isolation cannot be accepted from this evidence.
> Evidence: [dependency results](evidence/bff-dependencies.json), [rollout results](evidence/bff-rollout-probe.json), and [auth mapping result](evidence/auth-mapping-probe.json).

## Findings

### REV-001: [P1] Align the BFF dependency overrides with Spring Boot

Evidence: [Jackson override](../../repos/services/single-ui-bff/pom.xml#L249-L251) and [validator override](../../repos/services/single-ui-bff/pom.xml#L254-L257), candidate `95480c0`.
Spring Boot remains at `3.3.4`.
Its dependency management retains Jackson core and annotations `2.17.2`, Jakarta Validation `3.0.2`, and JBoss Logging `3.5.3.Final`.
The new direct overrides introduce databind `2.21.8` and Hibernate Validator `9.0.2.Final`.

Trigger: initialize the JSON mapper or validator with those dependency combinations.
The [paired probe](evidence/bff-dependencies.json) reproduces `NoClassDefFoundError: JsonSerializeAs` and `NoSuchMethodError: Logger.getMessageLogger`.
Exact baseline Jackson reads the same JSON successfully.
The validator comparison uses cached `8.0.2`, whereas Boot manages baseline `8.0.1`.

Consequence: JSON infrastructure cannot initialize under the declared dependency combination. Validator initialization independently fails.
The actual BFF startup consequence is source-derived. Corporate dependencies prevented whole-service execution.
Owner: unknown.
Next action: use compatible dependency families, then run actual startup and the full owning suite.
Validation: [TC-DEP-JACKSON](06-test-cases.md#tc-dep-jackson), [TC-DEP-VALIDATOR](06-test-cases.md#tc-dep-validator), and [assertions](evidence/probe_bff_dependencies.py).
Confidence: high for the linkage failures. No deployed failure is claimed.
Resolution: open.

### REV-002: [P2] Preserve successful CES applications when another application fails

Evidence: [aggregation loop](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/TileAuthorizationServiceImpl.java#L123-L136), candidate `95480c0`.
Trigger: two CES application groups serve different tiles. One succeeds and the other throws.
The aggregation throws before it returns any CES result.
The [outer catch](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/TileAuthorizationServiceImpl.java#L62-L72) retains the empty initial CES result.
Successful application grants and tile IDs therefore disappear together with the failed application.

The actual-source probe starts with visible tile IDs `[1,2,3]`.
After application B fails, visible IDs become `[1]`. Application A's authorized tile 2 also disappears.
An empty functional grant list triggers the same collateral loss through the real mapper.
The live provider's empty-assignment representation remains unverified.

Consequence: one application failure prevents unrelated CES tile use in mixed mode.
In `EMS3_ONLY`, the exception instead reaches login or relogin error handling.
Baseline `main` has no CES aggregation. This is a new-path defect, not a paired baseline execution regression.
Owner: unknown.
Next action: retain each successful group and deny only the failed group's tiles. Preserve fail-closed provider selection.
Validation: [BFF-ROLLOUT-MIXED](06-test-cases.md#bff-rollout-mixed), [BFF-ROLLOUT-FAILURE](06-test-cases.md#bff-rollout-failure), and [BFF-ROLLOUT-EMPTY](06-test-cases.md#bff-rollout-empty).
Assertions and results: [probe](evidence/probe_bff_rollout.py), [execution](evidence/bff-rollout-probe.json).
Confidence: high within the controlled service and drawer boundary.
The CES transport, private error bases, and executor are substituted. No browser or deployed session was exercised.
Resolution: open.

### REV-003: [P2] Preserve the existing provider when an update omits migration fields

Evidence: [request default](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/dto/request/RequestOfApplicationTile.java#L31-L35), candidate `95480c0`.
Trigger: an older client submits an ordinary maker update for an existing CES tile without `entitlementSource`.
The DTO initializes the missing property to `EMS2`.
The [update validator](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L281-L288) preserves the stored provider only when the property is null.
The [update path](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v1/ApplicationTileController.java#L89-L107) therefore saves EMS2 for that CES tile.

The probe confirms that omitted source becomes `EMS2`, while explicit null remains null.
Persistence was not executed. The save consequence follows inspected production source.
After checker activation, the tile uses legacy admission instead of its CES feature.
Users can lose access or regain legacy admission, depending on their legacy grants.

Baseline `main` has no provider selector to reset. This is an additive-field compatibility defect.
The current inspected [frontend service](../../repos/ui/mfe-base/src/admin/Tile/services/useServices.ts#L66-L82) forwards the tile data.
Its [editor](../../repos/ui/mfe-base/src/admin/Tile/common/useController.tsx#L339-L359) includes migration fields.
The finding concerns older or partial request payloads, not every current editor update.
Owner: unknown.
Next action: distinguish omitted update fields from the default used for tile creation.
Validation: [BFF-ROLLOUT-REQUEST](06-test-cases.md#bff-rollout-request), [assertions](evidence/probe_bff_rollout.py), and [result](evidence/bff-rollout-probe.json).
Confidence: high for deserialization and source flow. No current production occurrence is claimed.
Resolution: open.

### REV-004: [P2] Apply configured auth mapping revisions to cached grants

Evidence: [cache key](../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/entitlement/cache/RedisEntitlementCacheService.java#L120-L124), candidate `cacc4d2`.
Trigger: restrict role mappings or allowed actions, change `EMS3_MAPPING_VERSION`, and restart against existing Redis entries.
The [exported revision](../../repos/services/ratan-auth-server/src/main/resources/application.yml#L187-L199) never controls the cache key or mapped result revision.
Both paths use the constant `ems3-v1`.
The [cache reader](../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/entitlement/cache/RedisEntitlementCacheService.java#L35-L46) validates source and payload, without checking the effective mapping revision.
The [service](../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/service/Ems3LegacyEntitlementService.java#L29-L46) returns cached grants before current mapping runs.

Consequence: old roles or permitted actions can enter fresh authentication responses after the configuration change.
The shipped cache TTL bounds this condition to remaining cache lifetime, normally at most 3,600 seconds.
The actual-source mapper probe sets `ems3-v2` but still emits `ems3-v1`.
Redis acceptance and subsequent authentication effects are source-derived. No live exposure was observed.
Baseline `main` has no CES functional projection cache. No paired baseline execution is claimed.
Owner: unknown.
Next action: partition or invalidate cache entries using the effective mapping revision. Reject incompatible envelopes.
Validation: [AUTH-PROBE-001](06-test-cases.md#auth-probe-001), [assertions](evidence/AuthMappingProbe.java), and [result](evidence/auth-mapping-probe.json).
Confidence: high for the source behavior. The operational consequence requires the stated surviving-cache condition.
Resolution: open. This conditional finding does not establish a demonstrated release blocker.

## Independent tile rollout

**Per-tile selection works. Complete operational and backend independence does not.**
The [tile assessment](09-tile-rollout.md) explains modes, rollback, admin limits, regional filters, and all 113 retained tile records.
The export contains 45 CES rows and 68 EMS2 rows. Of those, 43 CES rows and 58 EMS2 rows have active tile flags.
These counts describe retained metadata, not a current deployment.

The auth server selects its provider by [user and migration mode](../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/migration/EntitlementMigrationFacade.java#L35-L65).
It receives no BFF tile identifier at that selection boundary.
An allowlisted user can therefore receive CES backend grants while some BFF tiles still use EMS2 admission.
Validate backend grants for every tile that remains usable by that user.
A BFF-only toggle cannot establish complete business-flow independence.

## Comparison identity and stage boundary

| Field | BFF | Authentication server |
| --- | --- | --- |
| Registered checkout | `repos/services/single-ui-bff` | `repos/services/ratan-auth-server`; Maven artifact `ratanone-auth-server` |
| Comparison | Local `main...HEAD` | Local `main...HEAD` |
| Base | `834b4155232222347220e47139a502ee43a9cbdf` | `7e8cbfa49051ffcd4cd4aa87a6382edfaf8daaee` |
| Candidate | `95480c0e2563bc2a5a639bca1f22ecedb61936c2` | `cacc4d218747e1591d5fb990eb5a8d8bcfb231a5` |
| Fingerprint | `38590d689e9548162164a93477b1130da6e116ca3b20c44d9211c1ef34325272` | `fce9cdbcaf3f5ddcd86e3bef12cc14beb3b7ad667b7f9afb76bd5205eaec51cb` |
| Changed paths | 58 | 66 |
| Context | [BFF context](evidence/single-ui-bff-context.json) | [Auth context](evidence/ratan-auth-server-context.json) |
| Per-file disposition | [BFF review](evidence/bff-review.json) | [Auth review](evidence/auth-review.json) |

Input authority: [exact user request](evidence/user-input.md#exact-user-input).
Entry route: bounded review of existing implementation. Registration date: 2026-11-09, Asia/Singapore.
Readiness: `READY` for the completed local review and controlled probes only.
Review owner: Codex. Business and correction owners: unknown.
Application fixes, deployment, and business acceptance remain outside this stage.
The new [intake](01-intake.md) is preserved with this report. Its SHA-256 is recorded in final validation.
No earlier intake commit or historical approval is implied.
Both service worktrees were clean. Unrelated Workbench and frontend-task changes were excluded.
The inspected frontend consumer is clean at `5295bd7ad66f62ee5cbb547f5aa5f6ef576c41d7`.

## Review coverage

All selected production diffs were inspected with affected callers and interfaces.
The BFF review records 54 inspected paths and four partially inspected large authorization test files.
The auth review identifies inspected production paths, selected assertions, and unchanged test bodies that were not fully read.
These are inspection dispositions. They do not establish complete behavioral coverage.
No generated graphs or unrelated indexes were rebuilt.

| Boundary | Evidence | Disposition and limit |
| --- | --- | --- |
| BFF login, relogin, tile routing, provider reads, DTOs, CRUD, CSV, database fields | [BFF review](evidence/bff-review.json), [rollout assessment](09-tile-rollout.md). | Inspected; controller and deployed integration unexecuted. |
| Auth migration, mapper, cache, data entitlements, JWT projection | [Auth review](evidence/auth-review.json). | Inspected; full suite and Redis execution unavailable. |
| Dependency initialization | [Paired probe](evidence/bff-dependencies.json). | Executed with real cached jars; full application startup unavailable. |
| Tile inventory | [All 113 rows](09-tile-rollout.md#per-tile-result). | Historical metadata only; category/import-map activation unavailable. |

## Validation evidence

| Check | Result | Evidence | Claim limit |
| --- | --- | --- | --- |
| Existing routing and drawer assertions | 28 passed; zero failures, skips, or aborts. | [Result and source bindings](evidence/bff-routing-tests/result.json). | Cached Spring 6.1.13; controlled dependency set. |
| Existing mapper assertions | 34 passed; zero failures, skips, or aborts. | [Result and source bindings](evidence/bff-mapper-service-tests/result.json). | Controlled dependency set; does not exercise the broken POM combination. |
| Mixed routing, failed app, empty grants, omitted DTO field | Four observed-behavior assertions passed. | [Probe result](evidence/bff-rollout-probe.json). | Passing assertions reproduce current defects; not product-conformance passes. |
| Jackson and validator comparisons | Candidate failures reproduced; comparison runs initialize successfully. | [Dependency result](evidence/bff-dependencies.json). | Validator comparison is compatible 8.0.2, not exact baseline 8.0.1. |
| Auth mapper revision | Configured revision ignored; observation asserted. | [Mapper result](evidence/auth-mapping-probe.json). | Isolated mapper; Java 26 release-21 bytecode; no Redis execution. |
| Full BFF service test compilation | Blocked; service suite executed zero cases. | [Compilation result](evidence/bff-mapper-service-tests/result.json), [failure log](evidence/bff-mapper-service-tests/service-compile.log). | Missing private FMAA/Ratan dependencies. |
| Auth Maven suite | Blocked before compilation; zero tests executed. | [Auth review](evidence/auth-review.json). | Private BOM `ratanone-dependencies:6.7.2` unavailable offline. |
| BFF effective POM helper | Blocked. | [BFF review](evidence/bff-review.json). | Maven help plugin unavailable offline; managed versions inspected from cached BOM. |
| Document structure, local links, source identity, and diff | Final result retained separately. | [Review validation](evidence/review-validation.json). | Automated checks do not establish full ASD compliance or business verification. |

The complete owning service suites did not pass because they could not run.
No full-suite, delivery, UAT, deployment, or production-readiness recommendation is made.

## Coverage mappings

The [review-output criteria](01-intake.md#acceptance-criteria) define two outputs, not product behavior acceptance.
Their denominator is two scoped criteria. The historical business AC inventory is unresolved for this broad branch review.

### AC-to-test matrix

| Criterion | Definition or assertion | Retained execution | Result |
| --- | --- | --- | --- |
| [REVIEW-AC-001](01-intake.md#acceptance-criteria) | [Jackson case](06-test-cases.md#tc-dep-jackson), [validator case](06-test-cases.md#tc-dep-validator), [request case](06-test-cases.md#bff-rollout-request), [auth case](06-test-cases.md#auth-probe-001). | [Dependency](evidence/bff-dependencies.json), [rollout](evidence/bff-rollout-probe.json), [auth](evidence/auth-mapping-probe.json). | Both repository comparisons reported. Defects remain open. |
| [REVIEW-AC-002](01-intake.md#acceptance-criteria) | [Mixed case](06-test-cases.md#bff-rollout-mixed), [failure case](06-test-cases.md#bff-rollout-failure), [empty case](06-test-cases.md#bff-rollout-empty). | [Rollout execution](evidence/bff-rollout-probe.json). | Selection works. Failure isolation fails. |

Definition links: 2/2 review criteria. Product conformance is not measured by this ratio.

### AC-to-code-change matrix

| Criterion | Inspected existing changes | Coverage meaning |
| --- | --- | --- |
| [REVIEW-AC-001](01-intake.md#acceptance-criteria) | Both 58-path and 66-path comparisons. [BFF](evidence/bff-review.json), [auth](evidence/auth-review.json). | Review inspection, not implementation of these review-output criteria. |
| [REVIEW-AC-002](01-intake.md#acceptance-criteria) | [Tile service](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/TileAuthorizationServiceImpl.java), [routing](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/EntitlementRouting.java), [drawer](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/util/AdminModuleUtil.java). | Source supports the bounded rollout assessment. |

New application changes in this review: zero. Implementation-conformance denominator: unavailable business AC inventory.

### Code-change-to-test matrix

| Selected changed unit | Direct assertion chain | Execution and gap |
| --- | --- | --- |
| POM dependency overrides | [Dependency probe](evidence/probe_bff_dependencies.py). | [Failures reproduced](evidence/bff-dependencies.json). Whole-service startup remains unexecuted. |
| CES aggregation and drawer result | [Rollout probe](evidence/probe_bff_rollout.py), [drawer tests](../../repos/services/single-ui-bff/src/test/java/com/scb/sso/singleuibff/util/AdminModuleUtilTest.java). | [Probe](evidence/bff-rollout-probe.json), [28 existing checks](evidence/bff-routing-tests/result.json). |
| Request provider default | [DTO deserialization assertion](evidence/probe_bff_rollout.py). | [Observed EMS2 default](evidence/bff-rollout-probe.json). Controller persistence remains unexecuted. |
| Auth mapper revision and cache key | [Mapper assertion](evidence/AuthMappingProbe.java). | [Revision mismatch](evidence/auth-mapping-probe.json). Cache acceptance remains source-derived. |

These four finding-related units have inspected assertion links.
The 124 changed-path inventory includes supporting configuration and tests. It is not a fully executed behavior denominator.
No 100% product conformance or passing-execution claim follows from these links.

## Independent passes and open limits

| Pass | Outcome | Evidence and limit |
| --- | --- | --- |
| BFF dependency and correctness review | Finding present. | [Independent review](evidence/bff-review.json). |
| Auth mapper, cache, and compatibility review | Conditional finding present. | [Independent review](evidence/auth-review.json). |
| Actual BFF routing execution | Collateral CES denial reproduced. | [Controlled probe](evidence/bff-rollout-probe.json). |
| Tile configuration and operational review | Per-tile selection confirmed from source. | [Rollout assessment](09-tile-rollout.md). |

The BFF executor qualifier suspicion was rejected. Only one relevant executor bean was established locally.
Pre-existing Boot namespace imports were excluded from introduced-defect findings.
The CES client uses an unchanged bare RestTemplate. New aggregation waits without a deadline on shared workers.
A stalled request can therefore affect shared capacity. No hanging-network execution established frequency or deployed impact.
This remains an operational caveat, not another demonstrated blocker.

CES multi-role scalar mapping and live empty-grant contracts require authoritative provider or business evidence.
No invented policy resolves them here.
No question blocks delivery of this bounded review.
Actual correction acceptance requires focused rechecks and the applicable full service suites.
Human business acceptance and deployment authorization remain unknown.

## Review outcome

Assessment: findings present. Three concern the BFF; one concerns the authentication server.
Per-tile provider selection is supported. Complete operational and cross-service independence is unsupported.
[Final validation](evidence/review-validation.json) binds the final identities and preserved intake bytes.
No reviewed application source was modified.
