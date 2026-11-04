---
artifact_kind: traceability-record
id: TRACE-SINGLE-UI-CES-300
version: 1
status: draft
owner: unknown
source_refs: [USER-IMPLEMENTATION, SDK-BASE, SDK-CANDIDATE, CES-SAMPLES, RUN-04, COMPAT-01]
related_ids: [CR-SINGLE-UI-CES-300, TC-SINGLE-UI-CES-300]
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

# SDK 3.0.0 migration coverage

> **Local contract checks pass; complete deployed permission equivalence remains unverified.**
> Action: compare synchronized assignments and compile actual consumers before adoption.
> Consequence: local fixtures cannot establish complete historical permission compatibility.
> Owner: application and entitlement owners, currently unknown.
> Evidence: [paired result](evidence/compatibility-run-01/result.json) and [compatibility limits](evidence/role-compatibility-design.md).

## Scope and identities

- Capability: Single UI authentication and entitlement lookup; no formal capability ID was supplied.
- Requirement: [REQ-SINGLE-UI-CES-001](01-intake.md); the latest implementation clarification governs this stage.
- Defect IDs: not applicable; migration and compatibility preservation are the requested effects.
- Repository ID: `single-ui-auth-sdk`; independent checkout `repos/libraries/single-ui-sdk-starter`.
- Contracts: CES assigned-role HTTP response and SDK nested-map Java API; formal contract IDs remain unavailable.
- Included scope: six criteria, twelve canonical predicates, seven implementation units, and required unchanged JWT paths.
- Excluded scope: live CES, application-owned token acquisition, deployed consumer execution, and organizational acceptance.

Baseline: `b0aa82005e7f14202f85f5ef583f25e42da9eeb3`.
Candidate: `fd9a157e260850b6d9efa10da3223950ea61133a`.
The [final binding](evidence/final-commit-binding.json) matches all 40 pre-run paths to the candidate commit.
No source changed during [run 04](evidence/candidate-run-04/result.json).
The [frozen intake](01-intake.md) remains at Git `1ed95a9f2`.
Its SHA-256 is `2affec0a12f0c41f7211a949b139bc3dbd9c2e5dca5417374611679e070c11ff`.

## Requirement and criterion declarations

All criteria below belong to [CR-SINGLE-UI-CES-300 version 1](10-change-review.md#request-and-source-facts).
The [exact user clarification](evidence/user-clarification-implementation.md) supplies compatibility, version, token ownership, and testing intent.
It invites failure-handling suggestions. It does not approve an organizational retry or outage policy.

| Requirement or defect ID | Criterion ID | Measurable expected behavior | Source revision | Knowledge review state |
| --- | --- | --- | --- | --- |
| [CR-SINGLE-UI-CES-300](10-change-review.md) | [AC-COMPAT](06-test-cases.md#ac-compat) | Preserve the Java lookup and role-specific nested map when CES supplies equivalent meaning. | User clarification, 1 November 2026. | Intent recorded; deployed parity unresolved. |
| [CR-SINGLE-UI-CES-300](10-change-review.md) | [AC-TOKEN](06-test-cases.md#ac-token) | Use the caller's FMAA token; reject invalid token inputs before HTTP. | User clarification, 1 November 2026. | Intent recorded. |
| [CR-SINGLE-UI-CES-300](10-change-review.md) | [AC-FAIL](06-test-cases.md#ac-fail) | Preserve legacy empty failures; expose sanitized classified failures through the additive API. | Engineering suggestion invited by the user. | Proposed policy; no human policy approval recorded. |
| [CR-SINGLE-UI-CES-300](10-change-review.md) | [AC-JWT](06-test-cases.md#ac-jwt) | Preserve token validation, entitlement extraction, and request attributes. | Baseline contract and user compatibility direction. | Intent recorded; implementation unchanged. |
| [CR-SINGLE-UI-CES-300](10-change-review.md) | [AC-BUILD](06-test-cases.md#ac-build) | Build version 3.0.0; complete all declared tests with zero failures, errors, and skips. | User clarification, 1 November 2026. | Intent recorded. |
| [CR-SINGLE-UI-CES-300](10-change-review.md) | [AC-CES](06-test-cases.md#ac-ces) | Use assigned-role CES lookup and make zero EMS2 requests. | [Migration input](evidence/user-input.md). | Intent recorded; live endpoint unverified. |

## Coverage inventories and summary

`TC >= AC = Code Change` concerns behavior containment and equivalence, rather than equal artifact counts.
The complete deployed permission inventory is unknown. No percentage below applies to that unavailable inventory.

- Intent inventory: six scoped criteria, expanded into twelve predicates in the AC-to-test matrix.
- Canonical inventory: [twelve cases](06-test-cases.md#procedure-and-assertions), version 1.
- Implementation inventory: [C01](#c01), [C02](#c02), [C03](#c03), [C04](#c04), [C05](#c05), [C06](#c06), and [C07](#c07).
- Required unchanged paths: `JwtTokenUtil`, `AuthTokenFilter`, and `JwtConfiguration`.
- Execution: local macOS arm64, Java 17, Spring Boot 4.0.6, mock transport, generated keys, and Spring configuration context.
- Exact source/test identity: [pre-run hashes](evidence/candidate-run-04/inputs.json), checked against the [final commit](evidence/final-commit-binding.json).

| Metric | Qualified / total | Percentage | Partial, missing, unknown, failed, stale, or not-run IDs | Evidence and limit |
| --- | --- | --- | --- | --- |
| AC to canonical test definitions | 6 / 6 | 100% | None within declared local predicates. | Twelve definitions; complete deployed inventory remains UNKNOWN. |
| AC to inspected assertions | 6 / 6 | 100% | Live and consumer predicates are outside this denominator. | Concrete assertions and package identity checks below. |
| AC to passing execution | 6 / 6 | 100% | Complete deployed compatibility remains unverified. | Run 04 and paired comparison; local scope only. |
| AC to inspected implementation mapping | 6 / 6 | 100% | None within declared implementation scope. | Includes unchanged JWT paths and POM configuration. |
| AC to conforming implementation | 4 / 6 | 66.7% | AC-COMPAT: full parity unresolved. AC-FAIL: policy proposed. | Local passing evidence does not establish those broader acceptance conclusions. |
| Change to canonical test definitions | 7 / 7 | 100% | None within seven implementation units. | Supporting documents are outside this denominator. |
| Change to inspected assertions | 7 / 7 | 100% | Live and actual consumer boundaries remain unavailable. | Direct assertions and package identity checks; no line-coverage claim. |
| Change to passing execution | 7 / 7 | 100% | None within declared local predicates. | Run 04 and paired comparison match the candidate source bytes. |
| Behavioral change justification | 5 / 6 | 83.3% | C05 remains an engineering recommendation. | C01 through C06 are behavior units. C07 supports build/version intent. |
| Complete historical permission acceptance | UNKNOWN | UNKNOWN | Same-user parity, service/data semantics, and consumer adoption. | No complete acceptance denominator exists. |

All twelve local predicates passed. The Maven suite ran 44 methods with zero failures, errors, or skips.
The paired comparison separately exercised one unchanged baseline-compiled caller under both classpaths.
These counts do not establish production conformance, line coverage, or business approval.
Instrumented line and branch coverage were not collected.

### C01

Retain `getEntitlements(String)` and the three-argument constructor.
Add a default explicit-token interface overload and a provider constructor.
One-method third-party implementations retain their existing method contract.
Migration configuration and token supply remain caller responsibilities.
The [compiled API comparison](evidence/public-api-comparison.json) retains all public members from 23 baseline classes.
This bounded API check does not establish every historical consumer or deployed permission mapping.

### C02

Replace EMS2 requests with one encoded CES assigned-role GET.
Use the exact caller token and obtain provider tokens for each lookup.
The SDK performs no token acquisition, caching, retries, or EMS2 fallback.

### C03

Parse `CesRole` assignments and preserve role-specific subject/action maps.
Preserve empty roles, action order, and duplicate actions.
Reject malformed selected data, aggregate-only responses, and inconsistent nested application metadata.

### C04

Add application mappings, optional role allowlists, feature scopes, and subject aliases.
Retain the entity filter over emitted legacy entity names.
Validate configuration and reject ambiguous role or subject aliases.

### C05

Preserve legacy empty-map failures and add classified explicit failures.
Expose advisory retryability without upstream causes, response bodies, or token text.
This recommendation remains separate from approved operational policy.

### C06

Wire CES authorization through the existing Spring bean and optional caller token provider.
Preserve existing JWT/filter creation and timeout properties.

### C07

Set parent revision and pipeline default to `3.0.0`.
Add JUnit Jupiter, Spring test support, and Surefire 3.5.5.
Require test discovery and execute the complete declared suite.

### Supporting and preserved inventories

| Artifact group | Classification | Rationale and evidence | Denominator treatment |
| --- | --- | --- | --- |
| Five Java test classes and one CES fixture. | Test-only. | Assert twelve canonical cases. The retained sample hash matches its source. | Evidence for C01 through C07. |
| README, setup guide, and dependency guide. | Supporting maintenance. | Explain token ownership, configuration, build preparation, and compatibility limits. | Excluded from implementation-change denominator. |
| Pipeline package version. | C07 maintenance. | Use the requested artifact version by default. | Included once within C07. |
| `.gitignore`. | Supporting maintenance. | Ignore generated `target/` and flattened POM files. | Excluded from behavior denominator. |
| JWT utility, token filter, and JWT configuration. | Required unchanged implementation. | Preserve AC-JWT behavior. | Mapped without a new behavior change. |
| Existing EMS2 DTO classes and properties. | Retained public surface. | Avoid removing historical types and accessors. They cause no migrated HTTP lookup. | Not counted as new implementation. |

## Relationship evidence

| From ID | Relationship | To ID | Evidence | Evidence class | Limit |
| --- | --- | --- | --- | --- | --- |
| [User clarification](evidence/user-clarification-implementation.md) | Declares criteria | [AC-COMPAT](06-test-cases.md#ac-compat), [AC-TOKEN](06-test-cases.md#ac-token), [AC-BUILD](06-test-cases.md#ac-build) | Exact retained wording. | CONFIRMED declaration. | No deployed parity or operational policy approval. |
| [Baseline contract](evidence/sdk-scope.md) | Supports preservation | [AC-JWT](06-test-cases.md#ac-jwt) | Unchanged source and user compatibility direction. | CONFIRMED declaration and inspection. | Historical artifacts can have different APIs. |
| [Migration input](evidence/user-input.md) | Requires replacement | [AC-CES](06-test-cases.md#ac-ces) | EMS2-to-CES objective. | CONFIRMED declaration. | Other services remain outside this SDK scope. |
| [Failure suggestion](10-change-review.md#selected-compatibility-design) | Proposes behavior | [AC-FAIL](06-test-cases.md#ac-fail) | Legacy failure source and additive API design. | CONFIRMED proposal. | No organizational policy approval. |
| [Twelve canonical cases](06-test-cases.md#procedure-and-assertions) | Assert through | [Executable assertion inventory](#inspected-implementation-and-assertions) | Each case has an individual matrix row below. | CONFIRMED assertion mapping. | Controlled local predicates only. |
| [Executable assertions](#inspected-implementation-and-assertions) | Execute in | [RUN-04](evidence/candidate-run-04/result.json), [COMPAT-01](evidence/compatibility-run-01/result.json) | Exact methods, retained results, and matching byte identities. | CONFIRMED local execution. | No live CES or actual consumer execution. |

## Inspected implementation and assertions

Each assertion below was inspected with its fixture, invocation, and helper chain.
`assertFailure` checks reason, retryability, absent credential text, and absent exception cause.
Mock-server verification rejects unexpected HTTP traffic. Generated keys isolate token checks from live credentials.
Full file hashes appear in [run 04 inputs](evidence/candidate-run-04/inputs.json).
The [commit binding](evidence/final-commit-binding.json) confirms the tested source and test bytes.

| Criterion ID | Repository ID | Code revision | Code location | Test ID | Test revision | Assertion ID and location | Assertion contents |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [AC-COMPAT](06-test-cases.md#ac-compat) | single-ui-auth-sdk | `fd9a157e260850b6d9efa10da3223950ea61133a` | [AuthorizationImpl](../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImpl.java), `mapRoles`. | [SDK-TC-001](06-test-cases.md#sdk-tc-001), [SDK-TC-002](06-test-cases.md#sdk-tc-002), [SDK-TC-004](06-test-cases.md#sdk-tc-004), [SDK-TC-008](06-test-cases.md#sdk-tc-008) | Same commit; probe retained separately. | [AuthorizationImplTest](../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/test/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImplTest.java), assertions listed below. | Exact maps, scope isolation, malformed-data rejection, and paired equality. |
| [AC-TOKEN](06-test-cases.md#ac-token), [AC-CES](06-test-cases.md#ac-ces) | single-ui-auth-sdk | Same candidate. | `AuthorizationImpl.getEntitlements`, `requestUri`. | [SDK-TC-003](06-test-cases.md#sdk-tc-003), [SDK-TC-007](06-test-cases.md#sdk-tc-007) | Same candidate. | `AuthorizationImplTest` request expectations and provider counter. | Exact bearer, encoded path, zero EMS2, fresh provider calls, and invalid-input zero HTTP. |
| [AC-FAIL](06-test-cases.md#ac-fail) | single-ui-auth-sdk | Same candidate. | `AuthorizationImpl`; `EntitlementLookupException`. | [SDK-TC-005](06-test-cases.md#sdk-tc-005), [SDK-TC-006](06-test-cases.md#sdk-tc-006) | Same candidate. | `AuthorizationImplTest` empty-map assertions and `assertFailure`. | Valid empty success, classified failures, retryability, and sanitized exceptions. |
| [AC-JWT](06-test-cases.md#ac-jwt) | single-ui-auth-sdk | Unchanged baseline bytes. | `JwtTokenUtil`; `AuthTokenFilter`. | [SDK-TC-009](06-test-cases.md#sdk-tc-009), [SDK-TC-010](06-test-cases.md#sdk-tc-010), [SDK-TC-011](06-test-cases.md#sdk-tc-011) | Candidate test commit. | [JwtTokenUtilTest](../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/test/java/com/scb/fmoportal/auth/util/JwtTokenUtilTest.java); [AuthTokenFilterTest](../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/test/java/com/scb/fmoportal/auth/filter/AuthTokenFilterTest.java). | Signature, issuers, time limits, extraction, user fields, and path selection. |
| [AC-BUILD](06-test-cases.md#ac-build) | single-ui-auth-sdk | Same candidate. | POMs; `AuthConfiguration`. | [SDK-TC-012](06-test-cases.md#sdk-tc-012) | Same candidate. | [AuthConfigurationTest](../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/test/java/com/scb/fmoportal/auth/config/AuthConfigurationTest.java); [package result](evidence/candidate-run-04/result.json). | Properties, bean type, missing-provider startup, artifact 3.0.0, and suite 44/0/0/0. |

### AC to test case coverage

Each row defines one local predicate, version 1. The complete historical permission inventory remains unknown.
Line locators refer to candidate files linked above. Test hashes are retained in the pre-run manifest.

| Requirement/defect and AC version | Applicable predicate | Canonical case and level | Inspected assertion and test revision/hash | Definition / assertion completeness | Matching execution and outcome | Gap and limit |
| --- | --- | --- | --- | --- | --- | --- |
| [CR v1](10-change-review.md) / [AC-COMPAT](06-test-cases.md#ac-compat) | P01: exact role-specific map, including empty roles. | [SDK-TC-001](06-test-cases.md#sdk-tc-001); unit HTTP-client test. | [AuthorizationImplTest:60,69,74](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/test/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImplTest.java:60); [CesRoleSampleTest:23,50](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/test/java/com/scb/fmoportal/auth/entity/CesRoleSampleTest.java:23). [Exact hashes](evidence/candidate-run-04/inputs.json). | Complete / complete locally. | [RUN-04](evidence/candidate-run-04/result.json): PASSED. | Controlled roles and retained sample; no deployed assignments. |
| [CR v1](10-change-review.md) / [AC-COMPAT](06-test-cases.md#ac-compat) | P02: exclude unrelated application, entity, role, and feature grants. | [SDK-TC-002](06-test-cases.md#sdk-tc-002); unit HTTP-client test. | [AuthorizationImplTest:80,93,104,113,130,140,150,257,272](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/test/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImplTest.java:80). [Exact hashes](evidence/candidate-run-04/inputs.json). | Complete / complete locally. | [RUN-04](evidence/candidate-run-04/result.json): PASSED. | Configured scopes do not approve business mappings. |
| [CR v1](10-change-review.md) / [AC-TOKEN](06-test-cases.md#ac-token) / [AC-CES](06-test-cases.md#ac-ces) | P03: exact bearer, encoded user path, and zero EMS2. | [SDK-TC-003](06-test-cases.md#sdk-tc-003); unit HTTP-client test. | [AuthorizationImplTest:162,177,438,465](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/test/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImplTest.java:162). [Exact hashes](evidence/candidate-run-04/inputs.json). | Complete / complete locally. | [RUN-04](evidence/candidate-run-04/result.json): PASSED. | No actual network or FMAA refresh. |
| [CR v1](10-change-review.md) / [AC-COMPAT](06-test-cases.md#ac-compat) | P04: reject malformed selected data without fabricated or partial grants. | [SDK-TC-004](06-test-cases.md#sdk-tc-004); unit HTTP-client test. | [AuthorizationImplTest:188,203,221,236,246,284,294,420,429](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/test/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImplTest.java:188); helper:529. [Exact hashes](evidence/candidate-run-04/inputs.json). | Complete / complete locally. | [RUN-04](evidence/candidate-run-04/result.json): PASSED. | Optional absent nested metadata is accepted; conflicting supplied metadata is rejected. |
| [CR v1](10-change-review.md) / [AC-FAIL](06-test-cases.md#ac-fail) | P05: valid empty assignments return zero permissions. | [SDK-TC-005](06-test-cases.md#sdk-tc-005); unit HTTP-client test. | [AuthorizationImplTest:302,306,307](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/test/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImplTest.java:302). [Exact hashes](evidence/candidate-run-04/inputs.json). | Complete / complete locally. | [RUN-04](evidence/candidate-run-04/result.json): PASSED. | Valid empty success is distinct from lookup failure. |
| [CR v1](10-change-review.md) / [AC-FAIL](06-test-cases.md#ac-fail) | P06: legacy empty failures and classified sanitized explicit failures. | [SDK-TC-006](06-test-cases.md#sdk-tc-006); unit HTTP-client test. | [AuthorizationImplTest:312,334,346](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/test/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImplTest.java:312); helper:529. [Exact hashes](evidence/candidate-run-04/inputs.json). | Complete / complete locally. | [RUN-04](evidence/candidate-run-04/result.json): PASSED. | Policy remains proposed. Retryability does not execute a retry. |
| [CR v1](10-change-review.md) / [AC-TOKEN](06-test-cases.md#ac-token) | P07: invalid token, request, or configuration causes zero HTTP. | [SDK-TC-007](06-test-cases.md#sdk-tc-007); unit HTTP-client test. | [AuthorizationImplTest:357,365,373,387,404,453](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/test/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImplTest.java:357). [Exact hashes](evidence/candidate-run-04/inputs.json). | Complete / complete locally. | [RUN-04](evidence/candidate-run-04/result.json): PASSED. | Application token-provider implementation remains outside scope. |
| [CR v1](10-change-review.md) / [AC-COMPAT](06-test-cases.md#ac-compat) | P08: baseline and candidate maps match equivalent assignments. | [SDK-TC-008](06-test-cases.md#sdk-tc-008); paired compiled-caller test. | [CompatibilityProbe](evidence/CompatibilityProbe.java):19,61; separate runtime bindings retained. | Complete / complete locally. | [COMPAT-01](evidence/compatibility-run-01/result.json): PASSED. | One baseline-compiled caller; synthetic equivalent assignments. |
| [CR v1](10-change-review.md) / [AC-JWT](06-test-cases.md#ac-jwt) | P09: preserve authentication signature, issuer, expiry, and maximum age. | [SDK-TC-009](06-test-cases.md#sdk-tc-009); generated-key unit test. | [JwtTokenUtilTest:41,58,78](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/test/java/com/scb/fmoportal/auth/util/JwtTokenUtilTest.java:41). [Exact hashes](evidence/candidate-run-04/inputs.json). | Complete / complete locally. | [RUN-04](evidence/candidate-run-04/result.json): PASSED. | No deployed key rotation or portal session. |
| [CR v1](10-change-review.md) / [AC-JWT](06-test-cases.md#ac-jwt) | P10: exact entitlement text; invalid or authentication tokens return null. | [SDK-TC-010](06-test-cases.md#sdk-tc-010); generated-key unit test. | [JwtTokenUtilTest:89,111](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/test/java/com/scb/fmoportal/auth/util/JwtTokenUtilTest.java:89). [Exact hashes](evidence/candidate-run-04/inputs.json). | Complete / complete locally. | [RUN-04](evidence/candidate-run-04/result.json): PASSED. | No live application execution. |
| [CR v1](10-change-review.md) / [AC-JWT](06-test-cases.md#ac-jwt) | P11: preserve five userInfo fields, version 3, and path selection. | [SDK-TC-011](06-test-cases.md#sdk-tc-011); servlet filter unit test. | [AuthTokenFilterTest:48,65,78,93,108](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/test/java/com/scb/fmoportal/auth/filter/AuthTokenFilterTest.java:48). [Exact hashes](evidence/candidate-run-04/inputs.json). | Complete / complete locally. | [RUN-04](evidence/candidate-run-04/result.json): PASSED. | Mock servlet chain; actual consumers remain untested. |
| [CR v1](10-change-review.md) / [AC-BUILD](06-test-cases.md#ac-build) | P12: CES service wiring, artifact 3.0.0, and complete passing suite. | [SDK-TC-012](06-test-cases.md#sdk-tc-012); Spring configuration and Maven package checks. | [AuthConfigurationTest:23,42,51](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/test/java/com/scb/fmoportal/auth/config/AuthConfigurationTest.java:23); [artifact and counts](evidence/candidate-run-04/result.json). | Complete / complete locally. | [RUN-04](evidence/candidate-run-04/result.json): PASSED; 44/0/0/0. | Java 17, Boot 4.0.6, and macOS arm64 only. |

### AC to code change coverage

Old locations use the baseline commit. New locations use the candidate commit.
The [baseline manifest](evidence/source-manifest.json) and [candidate manifest](evidence/candidate-run-04/inputs.json) retain exact byte identities.

| Requirement/defect and AC version | Intended predicate | Change ID or UNCHANGED | Exact old/new source locations | Conformance | Missing, extra, contradictory, or unknown behavior | Evidence and limit |
| --- | --- | --- | --- | --- | --- | --- |
| [CR v1](10-change-review.md) / [AC-COMPAT](06-test-cases.md#ac-compat) | P01 / P08: signature and role map. | [C01](#c01), [C03](#c03) | Old `AuthorizationImpl`:30,132. New `AuthorizationImpl`:39,53,163; `AuthorizationService`:7,13. | MATCH for equivalent local fixtures; broader parity UNKNOWN. | Data semantics and complete same-user assignments remain unresolved. | Exact maps and paired unchanged caller. |
| [CR v1](10-change-review.md) / [AC-COMPAT](06-test-cases.md#ac-compat) | P02: scoped entity, role, and subject grants. | [C03](#c03), [C04](#c04) | Old `AuthorizationImpl`:34,41. New `AuthProperties`:33; `AuthorizationImpl`:169,177,195,215. | MATCH for local scopes. | Approved business mappings remain external. | Application ID and name both select each role. |
| [CR v1](10-change-review.md) / [AC-COMPAT](06-test-cases.md#ac-compat) | P04: no fabricated grants from invalid selected data. | [C03](#c03), [C04](#c04) | Old `AuthorizationImpl`:65,71,105. New `CesRole`:11; `AuthorizationImpl`:181,187,193,229. | MATCH for rejection predicates. | Invalid selected data rejects the complete result. | Strict selected-response handling preserves access boundaries. |
| [CR v1](10-change-review.md) / [AC-TOKEN](06-test-cases.md#ac-token) | P03 / P07: caller token and invalid-input rejection. | [C01](#c01), [C02](#c02), [C04](#c04), [C06](#c06) | Old `AuthorizationImpl`:71,118; no caller-token path. New `AuthorizationImpl`:53,67,106,118; `FmaaTokenProvider`:4. | MATCH locally. | Token lifetime and refresh remain application responsibilities. | One bearer request; no token cache. |
| [CR v1](10-change-review.md) / [AC-FAIL](06-test-cases.md#ac-fail) | P05 / P06: empty failures and classified exceptions. | [C05](#c05) | Old `AuthorizationImpl`:65. New `AuthorizationImpl`:53,82,86; `EntitlementLookupException`:4. | PROPOSED policy; assertions pass. | Explicit API and retryability are additive engineering behavior. | Operational policy approval remains separate. |
| [CR v1](10-change-review.md) / [AC-JWT](06-test-cases.md#ac-jwt) | P09 / P10 / P11: token and filter preservation. | UNCHANGED | Baseline and candidate `JwtTokenUtil`, `AuthTokenFilter`, and `JwtConfiguration` hashes match. | MATCH within inspected predicates. | Historical consumers can use different static utility APIs. | Generated keys and mock servlet requests. |
| [CR v1](10-change-review.md) / [AC-BUILD](06-test-cases.md#ac-build) | P12: version and complete suite. | [C06](#c06), [C07](#c07) | Old parent revision `2.0.0-SNAPSHOT`. New parent POM:11,28,66; module POM:63; pipeline:7. | MATCH locally. | Actual consumer compilation and other platforms remain unverified. | Run 04 packages 3.0.0 with 44 passing tests. |
| [CR v1](10-change-review.md) / [AC-CES](06-test-cases.md#ac-ces) | P03: zero EMS2 lookup. | [C02](#c02) | Old `AuthorizationImpl`:73,125. New `AuthorizationImpl`:80. | MATCH locally. | Other services retain independent dependencies. | Exact CES URL and single-request expectations; no fallback. |

### Code change to test case coverage

Every row compares the baseline and candidate commits stated above.
Direct assertion chains establish these relationships. Shared criterion links alone do not establish them.

| Change ID and repository base/head | Changed symbol or hunk | AC links or maintenance rationale | Affected predicate | Canonical case and required level | Inspected assertion | Matching execution and outcome | Gap and limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [C01](#c01); declared baseline/candidate. | Interface default overload and retained constructors. | [AC-COMPAT](06-test-cases.md#ac-compat), [AC-TOKEN](06-test-cases.md#ac-token) | P01 / P03 / P08 / P12. | [SDK-TC-001](06-test-cases.md#sdk-tc-001), [SDK-TC-003](06-test-cases.md#sdk-tc-003), [SDK-TC-008](06-test-cases.md#sdk-tc-008), [SDK-TC-012](06-test-cases.md#sdk-tc-012); unit and paired caller. | [AuthConfigurationTest:51](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/test/java/com/scb/fmoportal/auth/config/AuthConfigurationTest.java:51); [AuthorizationImplTest:465](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/test/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImplTest.java:465); paired probe map assertion. | [RUN-04](evidence/candidate-run-04/result.json), [COMPAT-01](evidence/compatibility-run-01/result.json): PASSED. | Historical released consumers remain uncompiled. |
| [C02](#c02); declared baseline/candidate. | Lookup transport, provider call, and URI encoding. | [AC-TOKEN](06-test-cases.md#ac-token), [AC-CES](06-test-cases.md#ac-ces) | P03 / P07. | [SDK-TC-003](06-test-cases.md#sdk-tc-003), [SDK-TC-007](06-test-cases.md#sdk-tc-007); unit HTTP client. | [AuthorizationImplTest:162,177,438,453](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/test/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImplTest.java:162). | [RUN-04](evidence/candidate-run-04/result.json): PASSED. | CES/FMAA network behavior remains untested. |
| [C03](#c03); declared baseline/candidate. | CES DTO, `mapRoles`, and grant application validation. | [AC-COMPAT](06-test-cases.md#ac-compat) | P01 / P04 / P05 / P08. | [SDK-TC-001](06-test-cases.md#sdk-tc-001), [SDK-TC-004](06-test-cases.md#sdk-tc-004), [SDK-TC-005](06-test-cases.md#sdk-tc-005), [SDK-TC-008](06-test-cases.md#sdk-tc-008); unit and paired caller. | [AuthorizationImplTest:60,188,203,221,236,246,257,272,284,294](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/test/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImplTest.java:60); [CesRoleSampleTest:23](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/test/java/com/scb/fmoportal/auth/entity/CesRoleSampleTest.java:23). | [RUN-04](evidence/candidate-run-04/result.json), [COMPAT-01](evidence/compatibility-run-01/result.json): PASSED. | Controlled data cannot prove synchronized account parity. |
| [C04](#c04); declared baseline/candidate. | Properties, scope predicates, alias checks, and configuration validation. | [AC-COMPAT](06-test-cases.md#ac-compat), [AC-TOKEN](06-test-cases.md#ac-token) | P02 / P04 / P07. | [SDK-TC-002](06-test-cases.md#sdk-tc-002), [SDK-TC-004](06-test-cases.md#sdk-tc-004), [SDK-TC-007](06-test-cases.md#sdk-tc-007); unit HTTP client. | [AuthorizationImplTest:80,93,104,113,130,140,150,373,387,404,420,429](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/test/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImplTest.java:80). | [RUN-04](evidence/candidate-run-04/result.json): PASSED. | Approved service/data mappings remain absent. |
| [C05](#c05); declared baseline/candidate. | Legacy catch and classified sanitized exceptions. | [AC-FAIL](06-test-cases.md#ac-fail) | P05 / P06 / P07. | [SDK-TC-005](06-test-cases.md#sdk-tc-005), [SDK-TC-006](06-test-cases.md#sdk-tc-006), [SDK-TC-007](06-test-cases.md#sdk-tc-007); unit HTTP client. | [AuthorizationImplTest:302,312,334,346,357,453](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/test/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImplTest.java:302); helper:529. | [RUN-04](evidence/candidate-run-04/result.json): PASSED. | Passing execution does not approve operational policy. |
| [C06](#c06); declared baseline/candidate. | Optional provider wiring and existing Spring beans. | [AC-TOKEN](06-test-cases.md#ac-token), [AC-BUILD](06-test-cases.md#ac-build) | P07 / P12. | [SDK-TC-007](06-test-cases.md#sdk-tc-007), [SDK-TC-012](06-test-cases.md#sdk-tc-012); Spring configuration. | [AuthConfigurationTest:23,42](/Users/lushevol/code/github/ratan-release-impact/workbench/repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/test/java/com/scb/fmoportal/auth/config/AuthConfigurationTest.java:23). | [RUN-04](evidence/candidate-run-04/result.json): PASSED. | Full consumer auto-configuration remains untested. |
| [C07](#c07); declared baseline/candidate. | Revision, pipeline default, dependencies, and Surefire discovery. | [AC-BUILD](06-test-cases.md#ac-build) | P12. | [SDK-TC-012](06-test-cases.md#sdk-tc-012); Maven suite and package checks. | POM revision and [artifact/count result](evidence/candidate-run-04/result.json). | [RUN-04](evidence/candidate-run-04/result.json): PASSED. | One platform and prepared dependency repository. |

## Retained execution and verification

| Criterion ID | Assertion ID | Execution ID | Exact tested revision | Actual result | Execution status | Retained evidence | Verification claim and limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [AC-COMPAT](06-test-cases.md#ac-compat) | P01 / P02 / P04 / P08. | RUN-04 and COMPAT-01. | Candidate commit; baseline commit for paired run. | Exact fixture maps match; isolation and rejection assertions pass. | PASSED_LOCAL | [RUN-04](evidence/candidate-run-04/result.json), [COMPAT-01](evidence/compatibility-run-01/result.json). | Equivalent synthetic assignments only; no full parity claim. |
| [AC-TOKEN](06-test-cases.md#ac-token), [AC-CES](06-test-cases.md#ac-ces) | P03 / P07. | RUN-04. | Candidate commit and matching manifest. | Exact bearer and URL; zero EMS2; invalid inputs make zero HTTP. | PASSED_LOCAL | [RUN-04](evidence/candidate-run-04/result.json). | Mock transport; no token refresh or live CES. |
| [AC-FAIL](06-test-cases.md#ac-fail) | P05 / P06. | RUN-04. | Candidate commit and matching manifest. | Valid empty, legacy failure, and explicit exception assertions pass. | PASSED_LOCAL | [RUN-04](evidence/candidate-run-04/result.json). | Policy acceptance remains pending. |
| [AC-JWT](06-test-cases.md#ac-jwt) | P09 / P10 / P11. | RUN-04. | Candidate tests; unchanged baseline implementation hashes. | Validation, extraction, attributes, and path assertions pass. | PASSED_LOCAL | [RUN-04](evidence/candidate-run-04/result.json). | Generated keys and mock servlet chain. |
| [AC-BUILD](06-test-cases.md#ac-build) | P12. | RUN-04. | Candidate commit and matching manifest. | Artifact 3.0.0; tests 44; failures 0; errors 0; skipped 0. | PASSED_LOCAL | [RUN-04](evidence/candidate-run-04/result.json). | Local Java 17 / Boot 4.0.6 / macOS arm64. |

Run 04 used offline Maven after connected dependency preparation.
It ran `clean verify` with formatter execution disabled. No tests were excluded or skipped.
Its result records zero source changes and hashes both generated 3.0.0 JARs.
Earlier failures and incomplete bindings remain retained in runs 01 through 03.
They do not replace the authoritative run 04 bindings.

The [baseline build](evidence/baseline-build-result.json) passed with zero tests. That result establishes compilation, not behavior.
The paired probe separately asserts equal maps for equivalent assignments.
It asserts two old EMS2 requests and one new CES request.
Returned maps preserve separated roles, duplicate actions, action order, and empty roles.

## Coverage gaps

| Missing link | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| Same-user permission parity. | [Supplied assignments differ](evidence/role-compatibility-design.md). | Complete permission compatibility cannot be accepted. | Entitlement owner unknown. | Compare synchronized allowed and denied assignments for representative users. |
| Live assigned-role endpoint support. | [Run 04](evidence/candidate-run-04/result.json) uses mock transport. | Deployment availability and response compatibility remain unverified. | CES owner unknown. | Exercise the configured endpoint in an authorized environment. |
| Service-account and data-role semantics. | [CES assessment](evidence/ces-reference.md) lacks complete mappings. | Unsupported data grants and aliases cannot be asserted. | Business mapping owner unknown. | Supply reviewed service/data examples and exact expected legacy output. |
| Actual consumer compilation and startup. | [Consumer assessment](evidence/consumer-scope.md) identifies historical static JWT callers. | Dependency replacement alone may not adopt the current API. | Application owners unknown. | Compile actual consumers and exercise startup and permission checks. |
| Operational failure policy. | [User clarification](evidence/user-clarification-implementation.md) invites suggestions. | Retry, refresh, logging, and outage choices remain application decisions. | Application owner unknown. | Review the proposed distinction and apply bounded application policy. |
| Broader platform evidence. | [Run 04 limits](evidence/candidate-run-04/result.json) specify one local target. | Local results cannot establish every deployment target. | Release owner unknown. | Run applicable target-platform and environment checks before adoption. |

## Facts, inferences, and unresolved questions

- Facts: all 44 declared Java tests passed without failures, errors, or skips.
- Facts: the paired caller produced equal maps under baseline and candidate classpaths.
- Facts: migrated lookup uses caller token input and one CES request. No EMS2 fallback exists in that path.
- Facts: the assigned-role sample lacks response user identity. The SDK binds the request path, not a returned user identifier.
- Inferences: reviewed equivalent assignments can preserve old nested-map values through scoped configuration.
- Inferences: retryable classification can support caller policy. It does not establish that retrying is safe or required.
- Unresolved questions: live support, synchronized permissions, service/data mappings, and actual consumer adoption remain open.
- Unresolved authority: failure handling remains an engineering recommendation. Human operational policy review remains pending.

## Findings

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| [Local results](evidence/candidate-run-04/result.json), [paired comparison](evidence/compatibility-run-01/result.json), and [commit binding](evidence/final-commit-binding.json) match. | Inspected local contract predicates have passing evidence at the candidate commit. | Codex for implementation. | Preserve these bindings for review. |
| [Supplied role assignments differ](evidence/role-compatibility-design.md). | A 100% deployed compatibility claim remains unsupported. This is an evidence gap, not a demonstrated product defect. | Entitlement owner unknown. | Compare synchronized assignments before acceptance. |
| [Consumer APIs differ](evidence/consumer-scope.md). | Historical adoption requires actual compilation and startup evidence. | Application owners unknown. | Verify selected consumers against artifact 3.0.0. |

## Sources

| Source ID | Locator | Exact revision | Hash | Owner, authority, and limits |
| --- | --- | --- | --- | --- |
| USER-IMPLEMENTATION | [Exact clarification](evidence/user-clarification-implementation.md). | 1 November 2026. | Retained bytes; original message preserved verbatim. | User intent; failure suggestions invited. |
| SDK-BASE | [Baseline manifest](evidence/source-manifest.json). | `b0aa82005e7f14202f85f5ef583f25e42da9eeb3`. | Exact per-file hashes. | Existing source contract; no deployed identity claim. |
| SDK-CANDIDATE | [Pre-run manifest](evidence/candidate-run-04/inputs.json), [commit binding](evidence/final-commit-binding.json). | `fd9a157e260850b6d9efa10da3223950ea61133a`. | All 40 source, test, and build paths match. | Executed candidate bytes; no publication approval. |
| CES-SAMPLES | [Assigned-role sample](../ces-entitlement-migration-20261102/api/-fmces-v1-entitlement-user-1481696.json). | Capture metadata unknown. | `8f841cc6573449027db65a97ad26a01d2720f4f60c565e6dd9e18314651d32f3`. | Supplied structural example; no current assignment claim. |
| RUN-04 | [Result](evidence/candidate-run-04/result.json), [inputs](evidence/candidate-run-04/inputs.json). | Tested candidate bytes, unchanged during execution. | Log: `cfeb6ea849f7d32face277af5bb65f67034509b64979c02eaf24981367e7bb22`. | Complete local Maven suite; mock CES. |
| COMPAT-01 | [Paired result](evidence/compatibility-run-01/result.json), [probe](evidence/CompatibilityProbe.java). | Baseline and candidate in separate JVMs. | Execution directory retains exact input bindings. | Equivalent synthetic assignments; one baseline-compiled caller. |
