---
artifact_kind: change-request
id: CR-CES-SDK-FUNCTION-COVERAGE-20261104
version: 1
status: draft
owner: unknown
source_refs: [USER-SDK-REVIEW-20261104, SDK-BASE, SDK-CANDIDATE, MIGRATION-APIS]
related_ids: [CR-SINGLE-UI-CES-300, CES-MIGRATION]
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

# SDK CES migration function coverage review

> **Complete function parity cannot be confirmed. No new actionable SDK defect was found.**
> Action: verify the assigned-role endpoint, complete entity mappings, and actual consumer adoption.
> Consequence: these gaps prevent a complete migration-coverage claim.
> Owner: unknown. Evidence: [API assessment](evidence/sdk-function-coverage-20261104/api-parity.md#remaining-evidence-gaps) and [consumer findings](evidence/sdk-function-coverage-20261104/consumer-contracts.json).

## Current task state

Assessment date: 4 November 2026, Asia/Singapore.
The latest local migration is `fd9a157`. The checkout started on baseline `main` at `b0aa820`.
The [final check](evidence/sdk-function-coverage-20261104/final-checkout-state.json) finds it on `codex/initial-baseline` at the reviewed candidate.
The comparison endpoints and inspected candidate bytes remain unchanged.
The requested `single-ui-starter-sdk` resolves to registered `single-ui-sdk-starter`.
The review used exact Git objects and isolated exports. Application implementation and deployment were outside its scope.

| Measure | Result | Boundary |
| --- | --- | --- |
| Changed paths inspected | 20/20 | Exact baseline-to-candidate diff; [source review](evidence/sdk-function-coverage-20261104/code-review.json). |
| PROD sample grant rows matched | 60/60; 0 missing | EMS2 PROD samples → CES UAT catalog definitions and assignments for three supplied accounts. |
| Distinct PROD permission tuples matched | 59/59 | Same snapshot comparison; entity, role, subject, action; repeated data permission counted once. |
| Declared PROD data/system subjects matched | 4/4 | Feature-name presence only; no complete action dictionary is supplied. |
| Observed PROD subject/action pairs present | 36/36 | Role-free union of supplied grant examples; complete feature/action inventory remains unknown. |
| Actual assigned-role endpoint execution | NOT_RUN | Current API directory supplies no capture of this endpoint. |
| Retained complete SDK suite | 44 passed; 0 failures, errors, or skips | Run on 1 November; all 40 recorded files match the candidate. |
| Fresh complete test suite | 44 passed; 0 failures, errors, or skips | All five test classes in the sole SDK module; explicit compilation/test goals. |
| Fresh full packaging lifecycle | BLOCKED before tests | Missing formatter-plugin dependencies; full verify was not reproduced. |
| Complete account and permission population | UNKNOWN | Three examples do not define the complete migration denominator. |

The [API result](evidence/sdk-function-coverage-20261104/api-parity.json) retains sample counts and differences.
The [fresh result](evidence/sdk-function-coverage-20261104/candidate-module-test-run/result.json) records every executed test method.
The [execution binding](evidence/sdk-function-coverage-20261104/retained-execution-binding.json) verifies retained source and test hashes.
Neither result establishes current live permission equality.

## Request and source facts

- Requester: user in this Codex chat.
- Request source: [exact user input](evidence/sdk-function-coverage-20261104/user-input.md#exact-user-input), 4 November 2026.
- Entry route: supplied implementation with existing compatibility intent and canonical SDK cases.
- Baseline: `b0aa82005e7f14202f85f5ef583f25e42da9eeb3`, 14 October 2026.
- Candidate: `fd9a157e260850b6d9efa10da3223950ea61133a`, 1 November 2026.
- Candidate branch: `codex/initial-baseline`; this is the latest available local SDK commit.
- Repository: [registered SDK checkout](../../repos/libraries/single-ui-sdk-starter/).
- API source: [supplied migration APIs](api/).
- Intent: [exact compatibility and token clarification](../../evidence/knowledge/sources/user-clarifications/single-ui-sdk-ces-migration-20261101/user-clarification-implementation.md#exact-user-input).
- Prior implementation record: [SDK stage](../single-ui-sdk-ces-migration-20261101/10-change-review.md#selected-compatibility-design).

No remote-head or deployment comparison was performed. “Latest” means the latest available local migration commit.
Historical source paths can be stale. Candidate locators below refer to exact Git objects, not the baseline checkout.

## Stage boundary and readiness

- Stage: bounded local source, API, consumer, assertion, and retained-execution review.
- Readiness: `READY` for the requested review; the review is complete.
- Assessor: Codex, 4 November 2026, Asia/Singapore.
- Rationale: exact comparison endpoints, supplied APIs, compatibility intent, and test assertions were available.
- Full deployed parity: `READY_WITH_LIMITS` for additional evidence collection only.
- Blocked claim: complete migration equivalence without current endpoint, mappings, and consumer evidence.
- Resolution owner: unknown; obtain matched assignments and compile actual consumers.
- Intake integrity: both intake files remain unchanged; [hashes and revisions](evidence/sdk-function-coverage-20261104/retained-execution-binding.json).

The SDK intake SHA-256 remains `2affec0a12f0c41f7211a949b139bc3dbd9c2e5dca5417374611679e070c11ff`.
The migration intake SHA-256 remains `5271d9c60da0687a58726e7e37858a998f56e596f7a24673cad961ccbb64b0bd`.
The [binding record](evidence/sdk-function-coverage-20261104/retained-execution-binding.json) also records exact intake Git revisions.
Workbench `README.md` changes and untracked `core/release-report/` remain outside this review commit.
SDK generated `.flattened-pom.xml` files remain preserved; final hashes appear in the checkout-state record.

## Proposed change

This record assesses implemented changes. It proposes no application source change.

| Aspect | Old behavior | Candidate behavior | Assessment |
| --- | --- | --- | --- |
| Entitlement retrieval | EMS2 account GET and entitlement-list POST. | CES assigned-role GET. | Source supports zero EMS2 calls through migrated lookup. |
| Public map | `entity:role -> subject -> actions`. | Same map shape with configured entity, role, and subject mappings. | Conditional compatibility; equivalent assignments are required. |
| Service token | No caller token in old EMS2 lookup. | Explicit FMAA token or caller `FmaaTokenProvider`. | Intended migration requirement; consumer setup remains necessary. |
| Failure | Legacy method returns an empty map. | Legacy method retains that shape; explicit overload provides classified errors. | Implemented recommendation; organizational outage policy remains unapproved. |
| JWT and servlet filter | Existing token and request-attribute contracts. | Identical implementation bytes. | Inspected preservation; complete session assertion coverage is absent. |
| Artifact | `2.0.0-SNAPSHOT`. | `3.0.0`. | Source version matches user intent. Historical `1.1.1` consumer compatibility is separate. |

## Scope and affected artifacts

| Scope | Source and assertion evidence | Result and qualitative risk |
| --- | --- | --- |
| Role map, order, duplicates, empty roles | [Reviewed assertion chains](evidence/sdk-function-coverage-20261104/code-review.json); [SDK-TC-001](../single-ui-sdk-ces-migration-20261101/06-test-cases.md#sdk-tc-001). | Controlled predicates pass in retained execution. High consequence if role attribution broadens access. |
| Application, entity, role, and feature scopes | Same source review; [SDK-TC-002](../single-ui-sdk-ces-migration-20261101/06-test-cases.md#sdk-tc-002). | Exact selectors and configured allowlists exist. Project mappings remain necessary. |
| Token, encoded user path, zero EMS2 | Same source review; [SDK-TC-003](../single-ui-sdk-ces-migration-20261101/06-test-cases.md#sdk-tc-003). | Explicit bearer and per-call provider behavior have inspected assertions. Live token refresh remains unverified. |
| Malformed data and collisions | Same source review; [SDK-TC-004](../single-ui-sdk-ces-migration-20261101/06-test-cases.md#sdk-tc-004). | Candidate rejects unsupported or ambiguous selected data without partial grants. |
| No assignments and upstream failures | [SDK-TC-005](../single-ui-sdk-ces-migration-20261101/06-test-cases.md#sdk-tc-005), [SDK-TC-006](../single-ui-sdk-ces-migration-20261101/06-test-cases.md#sdk-tc-006), [SDK-TC-007](../single-ui-sdk-ces-migration-20261101/06-test-cases.md#sdk-tc-007). | Empty success and explicit failure are distinguished. Legacy empty-map ambiguity remains by design. |
| Existing Java API | [SDK-TC-008](../single-ui-sdk-ces-migration-20261101/06-test-cases.md#sdk-tc-008); [paired execution](../single-ui-sdk-ces-migration-20261101/evidence/compatibility-run-01/result.json). | Existing signature and constructor remain. Synthetic baseline-compiled caller produced equal maps. |
| Authentication and entitlement JWTs | [Consumer evidence](evidence/sdk-function-coverage-20261104/consumer-contracts.json); [SDK-TC-009](../single-ui-sdk-ces-migration-20261101/06-test-cases.md#sdk-tc-009), [SDK-TC-010](../single-ui-sdk-ces-migration-20261101/06-test-cases.md#sdk-tc-010). | Issuer, signature, expiry, maximum age, and entitlement extraction have assertions. |
| Filter attributes and path selection | [SDK-TC-011](../single-ui-sdk-ces-migration-20261101/06-test-cases.md#sdk-tc-011). | Request attributes, missing JWT, and include/exclude behavior have assertions. Logout/replay does not. |
| Spring configuration and timeouts | [SDK-TC-012](../single-ui-sdk-ces-migration-20261101/06-test-cases.md#sdk-tc-012). | Bean wiring, provider injection, and mapping configuration have assertions. Timeout wiring is source-inspected; timeout values and behavior lack assertions. |
| Data restriction resolution | [API function inventory](evidence/sdk-function-coverage-20261104/api-parity.md#function-and-contract-inventory). | Both implementations expose markers, not resolved policy fields. No new restriction-resolution regression is established. |
| Account status | Same API inventory. | Neither lookup enforces account status. Unknown policy does not establish an introduced defect. |

The scan flagged `synthetic-fmaa-token` in test code. This is a synthetic fixture, not a confirmed credential leak.
All 20 changed paths have dispositions in the [source review](evidence/sdk-function-coverage-20261104/code-review.json).
No graph rebuild or unrelated index operation was performed.

## User impact

No current user disruption or blocking SDK defect was demonstrated.
The following gaps limit a completeness claim. They do not automatically block a release.
Priority follows the user's impact rule. Unknown deployment reachability remains beside each consequence.

| Finding | Trigger and consequence | Old versus new | Owner and next action |
| --- | --- | --- | --- |
| G1, P3 evidence gap: API contract | Substitute the supplied effective-user or catalog endpoint directly. The explicit API rejects its incompatible response shape. | Old uses EMS2 DTOs. Candidate requires assigned-role DTOs; source prediction, not a live failure. | unknown; capture and exercise the actual assigned-role endpoint. |
| G2, P3 configuration gap: three entity scopes | Adopt only the README's `X_RATANONE` example. Legacy data and system entity keys cannot appear. | Old uses assigned legacy entities. Candidate emits configured aliases. Actual configuration is unknown. | unknown; review and execute separate scoped mappings for all required entities. |
| G3, P3 adoption gap: historical consumer | Upgrade Auth Server from declared `1.1.1` without adapting its static validator calls. Source predicts compilation failure. | Instance validator already exists at SDK baseline. This is an unchanged adoption boundary, not a CES regression. | unknown; bind the actual artifact, adapt injection, compile, and start the consumer. |
| G4, P3 assertion gap: logout/replay | Claim complete authentication regression coverage. Candidate tests contain no `validateSession` logout/replay assertions. | Session implementation is byte-identical; baseline had no tracked tests. No new session defect is established. | unknown; add scoped logout/replay verification when complete session assurance is required. |
| G5, P3 scope gap: role inventory | Claim every PROD role is migrated. `EMS2_ADMIN` lacks a CES name match. | Retained inventory comparison only. Its description identifies IAM management; migration disposition remains unknown. | unknown; classify platform-management scope before treating this as a business permission omission. |

G2 is configuration-dependent. The adapter supports multiple entity mappings; absence of deployed mapping evidence is not missing adapter code.
The [sample-derived mapping proposal](evidence/sdk-function-coverage-20261104/api-parity.md#configuration-needed-for-the-matched-sample-scope) covers the three supplied PROD accounts only.
The current retained SDK fixture lacks `Global`, while newer effective-user and catalog samples include it.
That fixture difference does not prove a current assigned-role endpoint omission.

## System impact

The candidate replaces the authorization transport and adds caller-token ownership.
It retains public EMS2 DTOs and accessors for compatibility. Their presence does not create EMS2 network requests.
Application, role, and feature selectors prevent unrelated grants from being copied when configuration defines the correct scopes.
Incorrect aliases can deny permissions or route grants under the wrong legacy entity.
Actual token renewal, TLS, endpoint deployment, and application enforcement remain unverified.

Auth Server remains at `dd6ebe87371d0fd484b68ce254fd2f18cc58bfd2` and declares SDK `1.1.1`.
Two static validator calls conflict with the candidate instance API. The [consumer manifest](evidence/sdk-function-coverage-20261104/consumer-contracts.json) gives exact paths and hashes.
No registered direct SDK `AuthorizationService` caller was found. This bounded search does not establish an empty consumer population.

## Options and consequences

| Option | Consequence | Decision status |
| --- | --- | --- |
| Verify current assigned-role API and scoped mappings. | Preserves the adapter's existing role-specific contract. | Next evidence action; endpoint and ownership remain unknown. |
| Use the supplied aggregate effective-user response directly. | Loses per-role provenance and fails candidate DTO validation. | Cannot establish legacy compatibility through endpoint configuration alone. |
| Design a catalog-based adapter. | Requires separate contract, assignment, consistency, and error review. | Not implemented or requested by this review. |

## Proposed acceptance and validation

These matrices reuse existing canonical criteria and cases. They define no new business rule.
The complete intended permission inventory remains unknown. No overall conformance percentage is justified.

### AC-to-test matrix

| Criterion | Canonical cases | Inspected assertions and execution | Limit |
| --- | --- | --- | --- |
| [AC-COMPAT](../single-ui-sdk-ces-migration-20261101/06-test-cases.md#ac-compat) | [001](../single-ui-sdk-ces-migration-20261101/06-test-cases.md#sdk-tc-001), [002](../single-ui-sdk-ces-migration-20261101/06-test-cases.md#sdk-tc-002), [004](../single-ui-sdk-ces-migration-20261101/06-test-cases.md#sdk-tc-004), [008](../single-ui-sdk-ces-migration-20261101/06-test-cases.md#sdk-tc-008) | Exact maps, exclusions, malformed responses, and paired equality. | Conditional fixtures; no complete deployed parity. |
| [AC-TOKEN](../single-ui-sdk-ces-migration-20261101/06-test-cases.md#ac-token) | [003](../single-ui-sdk-ces-migration-20261101/06-test-cases.md#sdk-tc-003), [007](../single-ui-sdk-ces-migration-20261101/06-test-cases.md#sdk-tc-007) | Exact bearer, fresh provider calls, and missing-token rejection. | No live FMAA renewal. |
| [AC-FAIL](../single-ui-sdk-ces-migration-20261101/06-test-cases.md#ac-fail) | [005](../single-ui-sdk-ces-migration-20261101/06-test-cases.md#sdk-tc-005), [006](../single-ui-sdk-ces-migration-20261101/06-test-cases.md#sdk-tc-006) | Empty assignments, classified HTTP/transport failures, sanitized messages. | Engineering failure policy remains a proposal. |
| [AC-JWT](../single-ui-sdk-ces-migration-20261101/06-test-cases.md#ac-jwt) | [009](../single-ui-sdk-ces-migration-20261101/06-test-cases.md#sdk-tc-009), [010](../single-ui-sdk-ces-migration-20261101/06-test-cases.md#sdk-tc-010), [011](../single-ui-sdk-ces-migration-20261101/06-test-cases.md#sdk-tc-011) | JWT validation/extraction and filter assertions. | No logout/replay assertion chain. |
| [AC-BUILD](../single-ui-sdk-ces-migration-20261101/06-test-cases.md#ac-build) | [012](../single-ui-sdk-ces-migration-20261101/06-test-cases.md#sdk-tc-012) and full suite | Spring context assertions and retained full build. | Fresh tests passed; full verify remains blocked. |
| [AC-CES](../single-ui-sdk-ces-migration-20261101/06-test-cases.md#ac-ces) | [003](../single-ui-sdk-ces-migration-20261101/06-test-cases.md#sdk-tc-003) | Expected single CES request; unexpected EMS2 calls fail mock verification. | Actual CES endpoint execution remains NOT_RUN. |

Definition links: 6/6 scoped criteria. Inspected assertion links: 6/6 scoped criteria.
These counts concern declared local predicates. Complete business acceptance coverage remains UNKNOWN.
Actual predicates and source locators appear in the [assertion inventory](evidence/sdk-function-coverage-20261104/code-review.json).
Fresh execution appears in the [current result](evidence/sdk-function-coverage-20261104/candidate-module-test-run/result.json).
The separate paired comparison remains [retained historical execution](../single-ui-sdk-ces-migration-20261101/evidence/compatibility-run-01/result.json).

### AC-to-code-change matrix

| Criterion | Changed implementation units | Source conformance |
| --- | --- | --- |
| [AC-COMPAT](../single-ui-sdk-ces-migration-20261101/06-test-cases.md#ac-compat) | [C01](../single-ui-sdk-ces-migration-20261101/09-coverage.md#c01), [C03](../single-ui-sdk-ces-migration-20261101/09-coverage.md#c03), [C04](../single-ui-sdk-ces-migration-20261101/09-coverage.md#c04) | MATCH for supported equal-assignment predicates; complete parity UNKNOWN. |
| [AC-TOKEN](../single-ui-sdk-ces-migration-20261101/06-test-cases.md#ac-token) | [C02](../single-ui-sdk-ces-migration-20261101/09-coverage.md#c02), [C06](../single-ui-sdk-ces-migration-20261101/09-coverage.md#c06) | MATCH for caller-provided token path. |
| [AC-FAIL](../single-ui-sdk-ces-migration-20261101/06-test-cases.md#ac-fail) | [C05](../single-ui-sdk-ces-migration-20261101/09-coverage.md#c05) | MATCH to implemented engineering suggestion; policy acceptance UNKNOWN. |
| [AC-JWT](../single-ui-sdk-ces-migration-20261101/06-test-cases.md#ac-jwt) | Required unchanged JWT/filter/configuration. | MATCH for inspected byte preservation; session execution incomplete. |
| [AC-BUILD](../single-ui-sdk-ces-migration-20261101/06-test-cases.md#ac-build) | [C07](../single-ui-sdk-ces-migration-20261101/09-coverage.md#c07) | Source version MATCH; fresh full suite and historical complete build passed. |
| [AC-CES](../single-ui-sdk-ces-migration-20261101/06-test-cases.md#ac-ces) | [C02](../single-ui-sdk-ces-migration-20261101/09-coverage.md#c02) | MATCH for migrated lookup source; live service support UNKNOWN. |

Inspected implementation links: 6/6 scoped criteria, including required unchanged implementation.
A complete link is not equivalent to full business conformance.
No unsupported extra behavior was confirmed after inspecting intent and configuration boundaries.

### Code-change-to-test matrix

Fresh execution covers all 44 existing unit tests. The paired binary probe remains a separate historical result.

| Changed unit | Direct assertion path | Assertion outcome and remaining limit |
| --- | --- | --- |
| [C01](../single-ui-sdk-ces-migration-20261101/09-coverage.md#c01), Java compatibility | `existingImplementationsRemainFunctionalInterfaces`; `retainedConstructorSupportsExplicitCallerToken`; [paired probe](../single-ui-sdk-ces-migration-20261101/evidence/CompatibilityProbe.java). | Passing local checks; historical consumer source upgrade remains unverified. |
| [C02](../single-ui-sdk-ces-migration-20261101/09-coverage.md#c02), CES/token HTTP | `encodesUserPathAndSendsExactCallerTokenWithoutEms2Requests`; `doesNotCacheCallerTokensOrAcquireIndependentCredentials`. | Passing mock HTTP assertions; actual CES/FMAA unverified. |
| [C03](../single-ui-sdk-ces-migration-20261101/09-coverage.md#c03), role normalization | `preservesRoleSpecificLegacyMapIncludingEmptyRoles`; `mapsActualRetainedRoleShape`; malformed-response assertions. | Passing supplied/synthetic fixtures; current complete assigned-role response missing. |
| [C04](../single-ui-sdk-ces-migration-20261101/09-coverage.md#c04), mappings | `appliesRoleAliasesAsAnAllowlist`; `appliesFeatureRestrictionAndSubjectAliasWithoutExtraGrants`; collision assertions. | Passing scoped fixtures; three-entity deployed configuration unverified. |
| [C05](../single-ui-sdk-ces-migration-20261101/09-coverage.md#c05), failures | `classifiesHttpFailuresAndPreservesLegacyEmptyMapPolicy`; `classifiesTransportFailureWithoutLeakingItsCause`. | Passing controlled failures; organizational policy remains unresolved. |
| [C06](../single-ui-sdk-ces-migration-20261101/09-coverage.md#c06), wiring | `bindsConfigurationAndWiresCallerProvider`; `startsWithoutTokenProviderAndPreservesEmptyLookup`. | Passing Spring context; downstream context unverified. |
| [C07](../single-ui-sdk-ces-migration-20261101/09-coverage.md#c07), version/tests | Full [run 04](../single-ui-sdk-ces-migration-20261101/evidence/candidate-run-04/result.json) and artifact identity. | Fresh 44/0/0/0; full packaging lifecycle remains blocked. |

Inspected direct assertion chains: 7/7 previously defined changed implementation units.
These units group behavior; they are not file counts or measured line coverage.
Supporting documentation, package configuration, and test-only changes have separate dispositions in the [source review](evidence/sdk-function-coverage-20261104/code-review.json).
No link was inferred solely from a shared criterion ID.

## Implementation and release proposal

No application fix, artifact publication, release, or deployment is proposed.
Verification preserves the user's review-only scope.
Bounded exploration implementation is not applicable; only isolated source exports and review evidence were created.

Fresh runs used Java `17.0.19`, Maven `3.9.16`, and copied local dependencies in temporary directories.
The full test suite passed through explicit goals for the sole SDK module.
All five test classes ran with no test exclusions, skips, assertion changes, or source changes.
The parent aggregator has no tests; the module command avoids its empty-project test guard.

Earlier unsuccessful attempts remain retained:

- [Complete verify attempt](evidence/sdk-function-coverage-20261104/candidate-run/result.json): missing formatter-plugin dependencies.
- [Compilation/test goal attempt](evidence/sdk-function-coverage-20261104/candidate-test-run/result.json): offline plugin prefix resolution failed.
- [Qualified goal attempt](evidence/sdk-function-coverage-20261104/candidate-qualified-test-run/result.json): the parent aggregator stopped because it contains no tests.

The [successful module run](evidence/sdk-function-coverage-20261104/candidate-module-test-run/result.json) records 44 passing tests.
Its [inputs](evidence/sdk-function-coverage-20261104/candidate-module-test-run/inputs.json) bind the command and all 40 unchanged source, test, and configuration files.
This test command does not establish a successful complete packaging lifecycle.
No assertions were removed, skipped, or weakened. No dependency download or application-source edit was performed.
The [runner](evidence/sdk-function-coverage-20261104/run_candidate.py) retains exact commands, source hashes, results, and limits.
Browser execution is not applicable to these library checks. No actual consumer workflow or remote runtime logs were collected.

## Sources and evidence limits

| Source | Locator | Identity and limit |
| --- | --- | --- |
| User scope | [Preserved request](evidence/sdk-function-coverage-20261104/user-input.md#exact-user-input). | 4 November user message; review authorization. |
| SDK comparison | [Review context](evidence/sdk-function-coverage-20261104/review-context.json). | Exact full base/head commits and changed-file hashes. |
| API source | [API inventory](evidence/sdk-function-coverage-20261104/api-inventory.json). | Twenty YAML files; eighteen response examples; retained snapshots only. |
| API interpretation | [Detailed comparison](evidence/sdk-function-coverage-20261104/api-parity.md). | PROD and UAT remain separate; set comparisons omit array order and duplicates. |
| Consumer source | [Consumer manifest](evidence/sdk-function-coverage-20261104/consumer-contracts.json). | Exact current Auth Server revision and source hashes; deployment unknown. |
| Fresh test evidence | [Current result](evidence/sdk-function-coverage-20261104/candidate-module-test-run/result.json). | Forty exact files; all 44 unit tests passed; controlled mock services. |
| Retained test evidence | [Retained binding](evidence/sdk-function-coverage-20261104/retained-execution-binding.json). | All 40 prior run files match candidate; historical complete packaging execution. |
| Prior paired execution | [Comparison result](../single-ui-sdk-ces-migration-20261101/evidence/compatibility-run-01/result.json). | Synthetic equal assignments; no claim about all actual accounts. |
| Discovery | [Workspace status](evidence/sdk-function-coverage-20261104/workspace-status.json). | Local registered resources; no live external operation invoked. |

Confidence is HIGH for exact source, inspected assertions, and supplied snapshot comparisons.
Confidence is UNKNOWN for complete deployed parity because its required evidence is absent.
No knowledge meaning, review state, or publication approval changed.

## Unknowns and blockers

| Open item | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| Current assigned-role endpoint and complete responses | Live SDK retrieval remains unverified. | unknown | Capture representative human, service, empty, and failure responses from the exact deployment. |
| Required entity, role, and feature mappings | Complete emitted legacy keys remain unverified. | unknown | Review all scoped mappings and assert allowed and denied operations. |
| Full role/account scope | Sample equality cannot prove full population equality. | unknown | Classify remaining names and compare complete assignments and definitions. |
| Data policy semantics | Matching `Global` and `VIEW_ENTITLEMENT` cannot prove resolved restriction equality. | unknown | Compare authoritative policy definitions and resolved values outside marker-only SDK behavior. |
| Historical consumers | Direct upgrade compatibility remains unverified. | unknown | Bind actual artifacts and execute consumer compilation, startup, and permission checks. |
| Logout/replay assertions | Complete authentication regression verification remains incomplete. | unknown | Add explicit assertions before claiming full session-function coverage. |

FMO administration remains a separate lower-priority non-production comparison under the [recorded scope](../../knowledge/candidates/security/KT-ces-migration-parity.md#fmo-scope-exception).
UAT `FMO_OPS_BOM` assignments differ from the CES catalog.
The CES role definition contains five additional pairs compared with EMS2 UAT.
UAT subject `srv.fxu.001` lacks a feature-name match in both supplied CES catalogs.
Its actions, affected accounts, and current migration applicability remain unknown.
The [complete dictionary assessment](evidence/sdk-function-coverage-20261104/api-parity.md#complete-supplied-function-inventory) keeps these limits explicit.
Those differences remain visible in the [API comparison](evidence/sdk-function-coverage-20261104/api-parity.json); they do not invalidate matched PROD examples.

## Stage evidence and completion

[Final automated checks](evidence/sdk-function-coverage-20261104/validation.json) passed.
Artifact lint retains warnings for unknown ownership, pending review, and unresolved business scope.
ASD writing review remains pending. No automated result supplies business approval.
Raw Maven logs retain their exact trailing spaces. Authored-file whitespace checks exclude those preserved logs.

| Stage | Result | Evidence and remaining limit |
| --- | --- | --- |
| Impact and source review | COMPLETE | All 20 changed paths and relevant unchanged consumers inspected. |
| API comparison | COMPLETE within supplied snapshots | All 60 PROD sample grant rows match; complete definitions and accounts unavailable. |
| Assertion mapping | COMPLETE within declared local criteria | Six scoped criteria and seven implementation units have inspected links. |
| Retained execution reconciliation | PASSED | Forty recorded file hashes match candidate; original 44 tests passed. |
| Fresh test execution | PASSED | Forty-four tests, zero failures/errors/skips, unchanged source bytes; mock CES transport. |
| Fresh full packaging lifecycle | BLOCKED before tests | Offline formatter dependencies unavailable; historical packaging pass remains separately bound. |
| Complete migration parity | NOT_VERIFIED | Current endpoint, full mappings, population, and consumers remain unverified. |

## Requested decision and actual disposition

- Requested decision: determine whether the latest SDK migration covers every function without gaps.
- Actual disposition: core migration paths have inspected coverage; complete function and deployment parity cannot be confirmed.
- New actionable SDK defects: none confirmed in the selected diff.
- Implementation state: candidate exists at `fd9a157e260850b6d9efa10da3223950ea61133a`.
- Intent review: existing user compatibility direction applies; engineering failure policy remains a proposal.
- Execution outcome: fresh matching 44-test pass; full packaging verification remains unavailable offline.
- Business acceptance and deployment authorization: not established by this review.
