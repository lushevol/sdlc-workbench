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

> **Four implementation findings and one exposed-contract gap remain open.**
> Action: align dependencies and correct the affected rollout paths. Owner: unknown.
> Consequence: service initialization and tile isolation cannot be accepted from this evidence.
> Evidence: [dependency results](evidence/bff-dependencies.json), [rollout results](evidence/bff-rollout-probe.json), and [auth mapping result](evidence/auth-mapping-probe.json).

## Migration compatibility priority

The [10 November clarification](evidence/user-followup-20261110.md#exact-user-input) controls this follow-up review.
Preserve existing APIs and exposed contracts where possible, so upper applications can migrate with minimal change.
A stable endpoint or field name does not prove stable value meaning or behavior.
Prefer deterministic compatibility handling in the BFF, auth server, SDK, or shared container.
Highlight exceptions that require business mapping or upper-application changes.

This restates the existing [permission compatibility intent](../../knowledge/candidates/security/KT-ces-migration-parity.md#fe-compat-ac-001).
The existing [provider-union rule](../../knowledge/candidates/security/KT-ces-migration-parity.md#fe-compat-ac-004) permits mapped grants from either provider.
Provider union is not itself a finding. CES identity and scalar business profile remain different contracts.
No new business meaning or knowledge publication results from this clarification.
The [project guide](../../AGENTS.md#migration-compatibility-in-code-review) now records the review principle.

| Item | Classification | Existing caller effect | Preferred correction location |
| --- | --- | --- | --- |
| [REV-001](#rev-001-p1-align-the-bff-dependency-overrides-with-spring-boot) | Availability and runtime compatibility | Existing calls can become unavailable during initialization failure. | BFF dependency management. |
| [REV-002](#rev-002-p2-preserve-successful-ces-applications-when-another-application-fails) | Availability and tile isolation | Valid grants disappear from an otherwise successful mixed login response. | BFF application-group error handling. |
| [REV-003](#rev-003-p2-preserve-the-existing-provider-when-an-update-omits-migration-fields) | Direct request compatibility | An old valid update payload silently changes a tile's provider. | BFF request deserialization and update defaults. |
| [REV-004](#rev-004-p2-apply-configured-auth-mapping-revisions-to-cached-grants) | Conditional permission correctness | Existing response fields can carry outdated roles or actions. | Auth mapper and cache revision handling. |
| [REV-005](#rev-005-p2-preserve-the-scalar-profile-needed-by-existing-callers) | Exposed value and downstream request compatibility | A CES-only user can produce an undefined authorization-limit profile. | Trusted profile mapping and lower shared compatibility layer. |

The first four corrections require no new upper-application API.
The fifth needs an authoritative scalar-profile mapping before its smallest complete correction can be selected.

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

#### REV-001 reproduction and preserving correction

Setup: the BFF uses Boot 3.3.4 and the committed direct dependency overrides.

1. Construct `ObjectMapper` using the candidate dependency combination.
2. Read the same empty JSON object used by the baseline probe.
3. Initialize a validator with the candidate validator and Boot-managed logging library.

| Intended compatibility | Old comparison | Candidate result |
| --- | --- | --- |
| Existing JSON calls keep working. | Exact baseline Jackson reads `{}`. | Jackson initialization throws a missing-class error. |
| Existing validation keeps working. | Compatible cached Validator 8.0.2 initializes. | Validator 9.0.2 calls a logging method absent from the managed library. |

This concerns internal library compatibility. It does not require an upper application to change its request or response model.
Align supported dependency families inside the BFF. Do not use a frontend workaround for server initialization failure.
The validator comparison is not exact baseline execution. Whole-service startup remains unexecuted.

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

#### REV-002 reproduction and preserving correction

Setup: tile 1 uses EMS2. Tile 2 uses CES application A. Tile 3 uses CES application B.

1. Return valid grants from both CES applications. Observe tiles `[1,2,3]`.
2. Keep A's successful response and make B throw.
3. Observe that only tile `[1]` remains, because the entire CES aggregate is discarded.

```java
Ems3TileReadResult result = join(future);
entitlements = merge(entitlements, result.entitlements());
```

| Intended independent operation | Old comparison | Candidate result |
| --- | --- | --- |
| Deny failed B while preserving successful A and the EMS2 tile. | Baseline has no CES grouping. Normal candidate control admits all three tiles. | A and B both disappear after B fails. |

Handle errors for each application group, while retaining successful results.
Keep failed CES scopes denied. Do not grant them through an EMS2 fallback.
This correction preserves existing login response fields and caller APIs.
The retained 45 CES rows share one application. The cross-application probe adds a synthetic second application.
The result proves the supported multi-application path, not a currently deployed multi-application incident.

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

#### REV-003 reproduction and preserving correction

Setup: a stored tile uses CES. An older client sends a complete legacy maker payload without the four new CES fields.

1. Deserialize the valid legacy payload.
2. Observe that omitted `entitlementSource` becomes EMS2.
3. Follow the update validator and its persistence call.
4. After checker activation, the tile uses EMS2 admission.

```java
private EntitlementSource entitlementSource = EntitlementSource.EMS2;
```

The preservation branch checks `request.getEntitlementSource() == null`. Omission does not satisfy that check.

| Intended request compatibility | Old comparison | Candidate result |
| --- | --- | --- |
| An ordinary legacy edit changes only the supplied configuration. | Baseline has no migration provider to reset. | The same legacy payload selects EMS2 on an existing CES tile. |

Keep omitted update fields distinct from explicit provider changes.
Use EMS2 as the creation default, while retaining the stored provider for omitted update values.
This keeps older clients usable. Requiring all clients to send the new field would weaken migration compatibility.
The DTO behavior was executed. Controller persistence remains source-derived.

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

#### REV-004 reproduction and preserving correction

Setup: Redis holds a CES projection that includes `FEATURE:WRITE` under mapping revision `ems3-v1`.

1. Change the mapping to permit only `FEATURE:READ`.
2. Set `EMS3_MAPPING_VERSION` to `ems3-v2` and restart against the same Redis.
3. Read the existing cache entry before its TTL expires.
4. The current service returns the old projection before applying the new mapping.

```java
+ Constant.EMS3_DATA_ROLE_MAPPING_VERSION + ":" + userId;
```

| Intended mapping control | Old comparison | Candidate result |
| --- | --- | --- |
| A new mapping revision cannot reuse an incompatible projection. | Baseline has no CES projection cache. | The configured revision does not change the cache partition or mapped revision. |

Use the effective configured revision consistently for mapping, cache keys, and envelope acceptance.
Refresh incompatible entries internally. Keep existing response fields and caller arguments.
This is a permission-value issue. The outward API shape can remain identical while its decision is wrong.
A surviving cache entry is required. Redis and backend effects were not executed.

### REV-005: [P2] Preserve the scalar profile needed by existing callers

This follow-up identifies an exposed-contract gap beyond the four original implementation findings.
Evidence: [CES entity mapping](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/AuthorizationResultMapper.java#L84-L105).
The mapper exposes the CES application name and additive `roleList`, without setting the legacy scalar `roleName`.
The [shared user accessor](../../repos/ui/mfe-ratan-container/src/ratanutils/authenticator.ts#L27-L69) only obtains a scalar role from legacy sources.
Those sources are an `X_RATANONE` entity or the older `user.entitlement` fallback.
A CES-only response can provide neither source.

The existing Cashflow caller still needs one scalar profile.
Its [role helper](../../repos/ui/mfe-cashflow-blotter/src/Cashflow_CN/components/CashflowDetails/MultiExceptions/common/utils.ts#L1072-L1075) returns `getUser().role`.
Its [authorization-limit flow](../../repos/ui/mfe-cashflow-blotter/src/Cashflow_CN/components/CashflowDetails/MultiExceptions/hooks/useData.ts#L688-L697) supplies that value as `profile`.
Its [HTTP service](../../repos/ui/mfe-cashflow-blotter/src/Cashflow_CN/services/index.ts#L128-L134) inserts the profile into the existing URL path.

Setup: a CES-only Cashflow session has valid functional grants, without a legacy role fallback.
The selected cashflow has sub-state `PendingVerification`, which invokes this authorization-limit check.

1. Read the CES entity and call the unchanged `getUser()` API.
2. Obtain an undefined scalar role from the current shared accessor.
3. Build the authorization-limit request through the unchanged Cashflow service.

| Intended exposed behavior | Old contract | Candidate source prediction |
| --- | --- | --- |
| Existing callers receive the reviewed business profile required by their requests. | The legacy scalar role supplies the authorization-limit profile. | The request contains `/api/ratan/v1/profileLimitation/checkLimitation/undefined/<currency>/<amount>`. |

Consequence: the existing request loses its required profile identity, despite an unchanged function signature.
Backend rejection and business-flow failure were not executed. No forced logout or data exposure is claimed.
Owner: unknown.
Next action: identify the authoritative CES-to-legacy business profile mapping and preserve that scalar contract in a lower shared layer.
Do not select the first CES entitlement, join role names, or rename the CES entity to invent a profile.
The existing [role mapping question](../../knowledge/candidates/security/KT-ces-migration-parity.md#open-questions) remains unresolved.
If valid CES roles cannot map to one existing profile, document the necessary caller exception before acceptance.
Validation: [TC-CONTRACT-PROFILE](06-test-cases.md#tc-contract-profile), [BFF contract trace](evidence/bff-contract-followup.json).
Confidence: high for the inspected source chain under the stated missing-fallback condition.
Execution: `NOT_RUN` for the actual HTTP and backend flow.
Resolution: open compatibility exception. The correction needs sourced business mapping.

The unchanged [entitlement-token serializer](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L135-L147) also uses `entity.name + ":" + roleName`.
CES therefore produces a key such as `RATAN_ENTITLEMENT_RULE:null`.
That differs from legacy `X_RATANONE:<role>`. Direct token consumers need their own compatibility checks.
No additional reachable direct-token defect is inferred from the different key alone.

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
Review priority: [10 November clarification](evidence/user-followup-20261110.md#exact-user-input).
Preserve existing APIs and exposed contracts where possible, so upper applications can migrate with minimal change.
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

Assessment: four implementation findings and one exposed-contract gap remain open.
Three original findings concern the BFF. One concerns the authentication server.
The additional gap crosses BFF output, the shared container, and an existing Cashflow caller.
Per-tile provider selection is supported. Complete operational and cross-service independence is unsupported.
[Final validation](evidence/review-validation.json) binds the final identities and preserved intake bytes.
No reviewed application source was modified.
The [auth contract comparison](evidence/auth-contract-followup.json) found no additional confirmed direct wire-format break.
Its response DTOs, controller contracts, and legacy role/action projection retain their exposed field shapes.
That source comparison does not prove equivalent permissions for every migrated account.
