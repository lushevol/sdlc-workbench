---
artifact_kind: change-request
id: CR-CES-BFF-ENTITY-FIELDS-20261106
version: 3
status: draft
owner: unknown
source_refs: [USER-ROLE-NAME-PROJECTION-20261106, USER-BFF-ENTITY-FIELDS-20261106, USER-APPLICATION-IDENTITY-20261106, BFF-CANDIDATE, CES-USER-API]
related_ids: [CES-MIGRATION, CR-CES-FRONTEND-ENTITLEMENT-IMPACT]
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
---

# CES entity fields and remaining contract compatibility

> **Additive fields supply CES role names and application identity. Scalar role compatibility remains unresolved.**
> Action: preserve EMS2 response fields and implement the two requested EMS3 fields.
> Consequence: existing scalar-role consumers still require a defined projection or multiple-role handling.
> Owner: unknown. Evidence: [latest request](evidence/frontend-entitlement-impact-20261105/user-bff-entity-fields-20261106.md#exact-user-input).

| Essential result | Evidence boundary |
| --- | --- |
| Two requested fields implemented across three production files. | Local BFF source only; no deployment. |
| 33 mapper test invocations passed; zero failures, skips, aborts, or container errors. | One complete mapper test class with real cached dependencies. |
| Two selected service test classes remain unrun. | Private dependencies block their compilation and the owning Maven build. |
| Complete frontend and release acceptance remain unverified. | Shared frontend adapters and scalar-role policy remain separate work. |

## Request and source facts

The [latest design question](evidence/frontend-entitlement-impact-20261105/user-role-name-projection-20261106.md#exact-user-input) proposes comma-joined roles and an application-name substitution.
It does not authorize either substitution. The [assessment below](#proposed-field-substitution-assessment) retains them as proposals.
The [identity clarification](evidence/frontend-entitlement-impact-20261105/user-clarification-application-identity-20261106.md#exact-user-input) corrects the application-name meaning.

Entry route: requirements first for a bounded BFF enhancement.
The [user request](evidence/frontend-entitlement-impact-20261105/user-bff-entity-fields-20261106.md#exact-user-input) authorizes minimal BFF implementation.
The [CES example](api/EMS3-user%20entitlements%20by%20app%20and%20user%20%281481696%29.yml) supplies both fields.
Its exact paths are `user_data.itam_id` and `entitlements.entitlement_name`.
`applicationId` remains a string. The supplied value is `"51358"`.
`roleList` preserves all returned entitlement names. It does not establish individual role-to-action attribution.
The BFF baseline is `d93455b6533bc017ab6bc42b0b585b804e1e96a1`.
No frontend application change or deployment is authorized by this request.

## Stage boundary and readiness

- Next phase: minimal local BFF implementation and scoped unit verification.
- Readiness: `READY`.
- Rationale: explicit field names, authoritative source paths, and existing DTOs define the requested mapping.
- Scope: shared Entity DTO, CES mapping, application-identity preservation, and affected assertion paths.
- Risk: low for additive fields; application merging requires an identity assertion.
- EMS2 fields remain unchanged. Null new fields must remain absent from EMS2 JSON.
- Missing optional source metadata must not introduce a new authorization failure.
- The original intake remains unchanged. This record owns the later implementation stage.
- Full frontend compatibility, business acceptance, and deployment remain unverified.
- Delivery recommendation: pending completion of the applicable unit suite, as required by [principle 10](../../PRINCIPLE.md#10-delivery-requires-passing-unit-tests).

## Proposed change

The requested BFF fields are implemented locally. Frontend adapters remain proposed.

| Aspect | Baseline | Local candidate | Evidence |
| --- | --- | --- | --- |
| CES assignment names | Discarded during normalization. | `roleList` copies all corresponding `entitlement_name` strings. | [Mapper](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/AuthorizationResultMapper.java#L73-L77). |
| CES application identity | Missing from serialized entity. | String `applicationId` copies `user_data.itam_id`. | [DTO](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/dto/ems2/v2/Entity.java#L13-L22). |
| Legacy team application name | Previously proposed from CES `user_data.app_name`. | Must remain the authoritative legacy team label. For this mapping: `applicationName: RATAN`, `name: RATAN_ENTITLEMENT_RULE`, `applicationId: "51358"`. | [Identity clarification](evidence/frontend-entitlement-impact-20261105/user-clarification-application-identity-20261106.md#confirmed-correspondence). |
| Missing optional metadata | Effective grants still map. | Role names become `[]`; missing ITAM ID remains absent. | [Assertions](../../repos/services/single-ui-bff/src/test/java/com/scb/sso/singleuibff/service/v2/authorization/AuthorizationResultMapperTest.java#L63-L73). |
| EMS2 JSON | Existing scalar fields and legacy IDs. | Existing fields remain; null new fields are omitted. | [Serialization assertion](../../repos/services/single-ui-bff/src/test/java/com/scb/sso/singleuibff/service/v2/authorization/AuthorizationResultMapperTest.java#L76-L90). |
| Equal CES names with different IDs | The merge key can collapse applications. | The merge key includes `applicationId`. | [Merge key](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/TileAuthorizationServiceImpl.java#L194-L206). |

The new fields do not replace legacy `id`, `roleId`, `roleName`, or `applicationName`.
`roleList` does not assign the aggregate feature/action union separately to each named role.
The mapper copies the response ITAM ID. The legacy team label comes from the explicit migration mapping keyed by CES application ID.
The mapper must not derive `RATAN` from `RATAN_ENTITLEMENT_RULE` by string manipulation.

## Scope and affected artifacts

Four production source/config files and two test files change in the independent BFF checkout.
The [latest request](evidence/frontend-entitlement-impact-20261105/user-bff-entity-fields-20261106.md#exact-user-input) defines the implementation scope.
The DTO, CES mapper, application merge key, and migration identity configuration are the changed production units.
Existing controller response assembly and endpoint signatures remain unchanged.
Existing callers include `TileAuthorizationServiceImpl` and the common login response builder.
The inspected `main` revision remains the earlier migration baseline `834b4155232222347220e47139a502ee43a9cbdf`.
This enhancement compares against migration candidate `d93455b6533bc017ab6bc42b0b585b804e1e96a1`.
Enhancement commits: `e116320e697b36d9e712e841908bf14d1d13e27d` and follow-up identity correction `c114b9c67f7bd6a2afc8a4394b4c372e2aea2e2d`.
Execution records identify the pre-commit checkout and exact file hashes. The final validation binds those bytes to this commit.

## User impact

The response now carries CES assignment names and application identity for shared frontend adapters.
EMS2 serialization remains unchanged for the tested legacy fixture.
No browser flow, session effect, or deployed business behavior was tested by source inspection.
Implementation owner: unknown. Next action: integrate the shared frontend adapters within a separate authorized change.

## System impact

The mapper remains the only normalization path changed by this request.
Per-field null omission keeps absent CES metadata out of ordinary EMS2 JSON.
Application-aware merge identity prevents one application's metadata and actions from replacing another application's data.
The signed entitlement-token representation is unchanged by these new fields.
No database migration, endpoint, configuration, external call, or dependency is added.

## Options and consequences

| Option | Consequence | Disposition |
| --- | --- | --- |
| Add the requested fields and preserve legacy fields. | Supplies new metadata with a small shared mapping change. | Implemented locally. |
| Replace scalar `roleName` with a list. | Breaks callers that require a string. | Not selected. |
| Put ITAM IDs into numeric legacy `id`. | Changes identity meaning and type. | Not selected. |
| Change entitlement-token keys now. | Expands scope across existing token consumers. | Deferred; requires a separate contract. |

## Proposed acceptance and validation

Canonical criteria: [BFF-ENTITY-AC-001](../../knowledge/records/candidates/security/KT-ces-migration-parity.md#bff-entity-ac-001), [BFF-ENTITY-AC-002](../../knowledge/records/candidates/security/KT-ces-migration-parity.md#bff-entity-ac-002), and [BFF-ENTITY-AC-003](../../knowledge/records/candidates/security/KT-ces-migration-parity.md#bff-entity-ac-003).
Cases: [BFF entity field extension](06-test-cases.md#bff-entity-field-extension).
Definitions, inspected assertions, execution, and business acceptance remain separate evidence classes.

### AC-to-test matrix

| Criterion | Canonical cases | Direct assertion scope |
| --- | --- | --- |
| [BFF-ENTITY-AC-001](../../knowledge/records/candidates/security/KT-ces-migration-parity.md#bff-entity-ac-001) | [TC-BFF-ENTITY-001](06-test-cases.md#tc-bff-entity-001), [TC-BFF-ENTITY-005](06-test-cases.md#tc-bff-entity-005) | Seven exact names and separate application role lists. |
| [BFF-ENTITY-AC-002](../../knowledge/records/candidates/security/KT-ces-migration-parity.md#bff-entity-ac-002) | [TC-BFF-ENTITY-002](06-test-cases.md#tc-bff-entity-002), [TC-BFF-ENTITY-005](06-test-cases.md#tc-bff-entity-005) | Exact textual ITAM ID and two isolated applications. |
| [BFF-ENTITY-AC-003](../../knowledge/records/candidates/security/KT-ces-migration-parity.md#bff-entity-ac-003) | [TC-BFF-ENTITY-001](06-test-cases.md#tc-bff-entity-001), [TC-BFF-ENTITY-003](06-test-cases.md#tc-bff-entity-003), [TC-BFF-ENTITY-004](06-test-cases.md#tc-bff-entity-004) | No invented scalar role; legacy JSON equality; optional metadata does not discard grants. |

Definition linkage: 3/3 scoped criteria. Complete frontend compatibility is outside this denominator.

### AC-to-code-change matrix

| Criterion | Changed production unit | Required unchanged path |
| --- | --- | --- |
| [BFF-ENTITY-AC-001](../../knowledge/records/candidates/security/KT-ces-migration-parity.md#bff-entity-ac-001) | [Entity fields](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/dto/ems2/v2/Entity.java#L20-L21), [mapper](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/AuthorizationResultMapper.java#L76-L77), [merge](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/TileAuthorizationServiceImpl.java#L194-L206). | Existing feature/action mapping. |
| [BFF-ENTITY-AC-002](../../knowledge/records/candidates/security/KT-ces-migration-parity.md#bff-entity-ac-002) | [Entity fields](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/dto/ems2/v2/Entity.java#L16-L17), [mapper](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/AuthorizationResultMapper.java#L75), [merge](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/TileAuthorizationServiceImpl.java#L194-L206). | Legacy numeric IDs. |
| [BFF-ENTITY-AC-003](../../knowledge/records/candidates/security/KT-ces-migration-parity.md#bff-entity-ac-003) | [Per-field serialization](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/dto/ems2/v2/Entity.java#L16-L21), [optional metadata](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/service/v2/authorization/AuthorizationResultMapper.java#L75-L77). | Existing EMS2 routing and scalar fields. |

Source linkage: 3/3 scoped criteria. Links alone do not establish execution or universal conformance.

### Code-change-to-test matrix

| Changed production unit | Direct assertion location | Canonical cases |
| --- | --- | --- |
| Entity DTO serialization | [Mapper test](../../repos/services/single-ui-bff/src/test/java/com/scb/sso/singleuibff/service/v2/authorization/AuthorizationResultMapperTest.java#L30-L90). | [TC-BFF-ENTITY-001](06-test-cases.md#tc-bff-entity-001), [TC-BFF-ENTITY-002](06-test-cases.md#tc-bff-entity-002), [TC-BFF-ENTITY-003](06-test-cases.md#tc-bff-entity-003). |
| CES metadata mapping | [Mapper test](../../repos/services/single-ui-bff/src/test/java/com/scb/sso/singleuibff/service/v2/authorization/AuthorizationResultMapperTest.java#L30-L73). | [TC-BFF-ENTITY-001](06-test-cases.md#tc-bff-entity-001), [TC-BFF-ENTITY-002](06-test-cases.md#tc-bff-entity-002), [TC-BFF-ENTITY-004](06-test-cases.md#tc-bff-entity-004). |
| Application merge identity | [Service test](../../repos/services/single-ui-bff/src/test/java/com/scb/sso/singleuibff/service/v2/authorization/Ems3ApplicationNameAuthorizationTest.java#L110-L142). | [TC-BFF-ENTITY-005](06-test-cases.md#tc-bff-entity-005). |

Assertion linkage: 3/3 changed production units. Two changed test files support those units.
No unsupported extra business behavior was identified in the inspected delta.
Runtime branch coverage and complete frontend conformance are not measured here.

### Execution coverage

| Measure | Result | Limit |
| --- | --- | --- |
| Scoped case definitions with inspected assertions | 5/5 | Definitions and assertions only. |
| Scoped cases with passing execution | 4/5 at the initial field definition | The later [TC-BFF-ENTITY-002](06-test-cases.md#tc-bff-entity-002) identity scenario and [TC-BFF-ENTITY-005](06-test-cases.md#tc-bff-entity-005) remain unrun. |
| Changed production units with passing direct assertions | 2/3 | DTO and mapper pass; merge service execution remains blocked. |
| Selected unit classes executed | 1/3 | Mapper class: 33 passed. Two service classes: zero executions. |
| Complete BFF unit suite | Not established | The owning Maven command stops during dependency resolution. |

Passing evidence: [verification summary](evidence/frontend-entitlement-impact-20261105/bff-entity-fields-verification.json) and [mapper execution](evidence/frontend-entitlement-impact-20261105/bff-entity-fields-mapper-20261106/result.json).
Blocked evidence: [Maven outcome](evidence/frontend-entitlement-impact-20261105/bff-entity-fields-maven-result.json) and [service compiler diagnostics](evidence/frontend-entitlement-impact-20261105/bff-entity-fields-isolated-20261106/service-compile.log).
No complete criterion conformance claim follows from the linkage counts above.

## Implementation and release proposal

- Implementation: local BFF enhancement only.
- Frontend implementation: not part of this change.
- Release and environment: unknown; no deployment performed.
- Reversal: revert the isolated BFF enhancement commit.
- Bounded exploration: not applicable; the user requested specific implementation.

## Remaining compatibility

**Multiple roles remain the main unavoidable semantic difference. Other shared-adapter gaps can often preserve existing upper-application calls.**
The [source assessment](evidence/frontend-entitlement-impact-20261105/remaining-contract-gaps-20261106.json) records pre-enhancement code bindings.
Its application merge finding is addressed by this enhancement. Other frontend findings remain unimplemented.
Confidence: high for inspected contracts; deployed reachability and complete consumer coverage remain unverified.

| Remaining gap | What still differs or fails | Compatibility action |
| --- | --- | --- |
| Scalar roles | `roleList` supplies assignments, but no rule selects one legacy `roleName` or `getUser().role`. | Keep EMS2 scalar behavior. Define each multiple-role consumer's required semantics. |
| Raw identities and nullability | CES entity names and string ITAM IDs differ from EMS2 names and numeric IDs. Legacy fields remain null. | Preserve separate identities. Adapt shared types and profile display; do not fabricate legacy IDs. |
| Legacy entitlement token | The token still uses `entity.name:roleName`, including CES `:null` keys. | Use structured entities for CES metadata. Token-only consumers need an additive design. |
| Shared permission helper | `X_RATANONE` dispatch and `getUser()` normalization ignore the new metadata. | Implement provider-aware shared adapters while keeping ordinary permission signatures. |
| Per-tile context | Global imports cannot identify conflicting same-feature tile scopes automatically. Drawer metadata is incomplete for this boundary. | Supply authoritative bindings. Resolve ambiguous callers explicitly; never select one global provider. |

Owner for all remaining contract work: unknown.
Next action: implement the shared frontend design and resolve only the dependent scalar-role policy.
Direct consumers of raw names, legacy IDs, or token keys need review even when their method signatures remain unchanged.
The complete inventory of strict external JSON consumers remains unknown.

### Proposed field substitution assessment

**Comma-joined roles preserve a string type, but do not preserve single-role behavior. Keep application names separate from IDs.**
Source: [latest question](evidence/frontend-entitlement-impact-20261105/user-role-name-projection-20261106.md#exact-user-input).
Confidence: high for inspected source consequences. No substitution, browser test, or backend ownership query was executed.

| Proposal | Compatible surface | Remaining difference and evidence |
| --- | --- | --- |
| Set `roleName` to `roleList.join(",")`. | Text display and a scalar JSON string remain possible. | Exact role comparisons treat the complete string as one role. See [exception checks](../../repos/ui/mfe-ratan-container/src/ratanutils/authenticator.ts#L281-L287). |
| Pass that string into `getUser().role`. | Existing method signatures stay callable. | View ownership compares one stored owner against the whole role string. See [view controller](../../repos/ui/mfe-ratan-container/src/ratancomponents/ViewSelector/common/useViewNameController.ts#L106-L112). |
| Use the joined string in saved-content requests. | Existing request fields remain strings. | Queries send the entire value as `assignee` and `moduleOwner`. Backend list interpretation remains unverified. See [view requests](../../repos/ui/mfe-ratan-container/src/ratancomponents/ViewSelector/store.ts#L21-L31). |
| Set `applicationName` to `applicationId`. | The inspected frontend still receives a string. | Profile display shows `51358` instead of the legacy team name. This substitution does not change permission lookup. See [profile label](../../repos/ui/mfe-base/src/components/Profile/util.ts#L1-L5). |

For example, `"PSS_RO,FMO_OPS" !== "PSS_RO"` evaluates as a different scalar value.
If a CES adapter exposes that value as `user.role`, the old exact-role restriction no longer identifies `PSS_RO` membership.
This is a source-derived conditional consequence. It is not a current deployed failure or an approved multiple-role restriction rule.
Similarly, stored owner `FMO_OPS` differs from combined value `FMO_OPS,FMO_RO`.
The view controller can mark that content read-only when its role-aware feature is enabled.

The current [user helper](../../repos/ui/mfe-ratan-container/src/ratanutils/authenticator.ts#L15-L25) selects `roleName` only for `X_RATANONE`.
Changing the CES BFF field alone does not make that helper read it.
The [token builder](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L131-L143) would also embed the joined value in its key.
The [profile lookup](../../repos/ui/mfe-base/src/components/Profile/index.tsx#L109-L113) uses the same entity field, so newly generated matching responses can remain aligned.
Those keys still describe a role combination. They do not establish separate per-role feature/action grants.

Recommendation: retain canonical `roleList` and `applicationId`.
Keep `applicationName` as the legacy team label. For this case, map `RATAN_ENTITLEMENT_RULE` and `"51358"` to `RATAN` through an authoritative configuration or migration table.
Keep `name` as the CES entity value `RATAN_ENTITLEMENT_RULE` for CES permission scope.
Join role names at the display boundary where no authorization or ownership logic consumes the string.
If a legacy `roleName` projection is selected, define its display-only meaning and adapt each logical consumer explicitly.
Keep EMS2 values unchanged. Do not infer a scalar role or business membership rule from a display projection.

Owner: unknown. Next action: decide the projection contract before implementing field substitutions.
The user asked for an assessment. No knowledge intent or application code changed for this question.
Validation and source bindings: [assessment checks](evidence/frontend-entitlement-impact-20261105/role-name-projection-validation-20261106.json).

## Sources and evidence limits

- Intent: [exact request](evidence/frontend-entitlement-impact-20261105/user-bff-entity-fields-20261106.md#exact-user-input) and [candidate contract](../../knowledge/records/candidates/security/KT-ces-migration-parity.md#ces-entity-role-and-application-fields).
- API sample: [supplied CES response](api/EMS3-user%20entitlements%20by%20app%20and%20user%20%281481696%29.yml). No live request was sent.
- Prior frontend source findings: [impact analysis](05-impact-analysis-frontend-entitlements.md).
- Remaining contracts: [source hashes and locators](evidence/frontend-entitlement-impact-20261105/remaining-contract-gaps-20261106.json).
- Execution: [prior real-source mapper run](evidence/frontend-entitlement-impact-20261105/bff-entity-fields-mapper-20261106/result.json) and [offline helper](evidence/frontend-entitlement-impact-20261105/verify_bff_entity_fields.py).
- Validation: [document checks and implementation hashes](evidence/frontend-entitlement-impact-20261105/bff-entity-fields-validation-20261106.json) and [identity correction validation](evidence/frontend-entitlement-impact-20261105/identity-correction-validation-20261106.json).

## Unknowns and blockers

Scalar-role policy blocks complete acceptance of dependent role-aware frontend behavior.
It does not block these additive BFF fields.
Complete deployment, external consumer, and business acceptance evidence is unavailable.
Owner: unknown. Next action: bind the intended release and verify the affected shared consumers.
Private starter and FMAA dependencies block complete selected service-unit execution.
This missing evidence does not establish an application failure.
Owner: unknown. Next action: restore private dependency access and run the selected classes through the owning Maven build.

## Stage evidence and completion

Implementation and assertion inspection are complete.
The prior [mapper run](evidence/frontend-entitlement-impact-20261105/bff-entity-fields-mapper-20261106/result.json) passes all 33 invocations, including the three initial field tests.
The follow-up adds explicit legacy-team mapping assertions, but the selected Maven tests could not start because private dependencies are unavailable.
The [Maven run](evidence/frontend-entitlement-impact-20261105/bff-entity-fields-maven.log) stops before compilation because two private starters are unavailable.
Isolated service compilation also requires unavailable private FMAA and common classes.
The [first isolated attempt](evidence/frontend-entitlement-impact-20261105/bff-entity-fields-isolated-20261106/result.json) records an additional harness setup failure.
Implicit source loading did not process Lombok annotations correctly. Explicit production-source compilation fixed that harness problem.
No application assertion failed in that setup attempt because no test executed.
The [final mapper result](evidence/frontend-entitlement-impact-20261105/bff-entity-fields-mapper-20261106/result.json) retains actual source and dependency hashes.
The local helper uses Spring `6.1.13`, not every explicit BFF dependency override.
These controlled results do not establish a complete suite, live endpoint, browser behavior, or production compatibility.

## Knowledge-update log

The explicit field decision updates [CES migration parity](../../knowledge/records/candidates/security/KT-ces-migration-parity.md#ces-entity-role-and-application-fields) from version 2 to version 3.
The [update record](evidence/frontend-entitlement-impact-20261105/entity-fields-knowledge-update-20261106.json) binds source hashes, criteria, review, and validation.
The [new audit event](../../knowledge/evidence/audit/AUD-20261106-KT-ces-migration-parity-v3.yaml) preserves predecessor identity.
The record remains a draft candidate. No scalar-role projection or publication approval was added.
The [identity clarification update](evidence/frontend-entitlement-impact-20261105/identity-knowledge-update-20261106.json) advances the candidate to version 4.
It preserves legacy team `applicationName`, CES `name`, and application ID as separate meanings.
Its [v4 audit](../../knowledge/evidence/audit/AUD-20261106-KT-ces-migration-parity-v4.yaml) retains the version 3 predecessor.
The refined [identity criterion](../../knowledge/records/candidates/security/KT-ces-migration-parity.md#bff-entity-ac-002) has a separate unrun test scenario.


## Requested decision and actual disposition

The user authorized minimal BFF implementation through the [latest request](evidence/frontend-entitlement-impact-20261105/user-bff-entity-fields-20261106.md#exact-user-input).
The additive implementation and prior mapper verification are complete. The identity correction is committed, but its follow-up tests remain unrun because private dependencies and a compatible Java 17 runner are unavailable.
Human knowledge review, business acceptance, and deployment remain pending.
