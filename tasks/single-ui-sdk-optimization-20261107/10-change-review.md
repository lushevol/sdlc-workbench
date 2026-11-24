---
artifact_kind: change-request
id: SDK-OPT-CHANGE-20261107
version: 1
status: draft
owner: unknown
source_refs: [SDK-OPT-INPUT, SDK-OPT-BASE]
related_ids: [SDK-OPT-20261107]
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

# Simplify the CES permission mapper

> **The local optimization passes; a transparent migration remains unproved.**
> Action: reconcile the current CES endpoint, assignments, mappings, and consumer integration before claiming unchanged access.
> Consequence: the SDK upgrade alone cannot establish that guarantee.
> Owner: unknown for integration acceptance. Evidence: [API assessment](#api-compatibility-follow-up-8-november-2026).

## Request and source facts

- Requester: human user in Codex.
- Request: [optimize the latest SDK change](evidence/user-input.md#exact-user-input) using Ponytail full mode.
- Baseline: SDK `fd9a157e260850b6d9efa10da3223950ea61133a`, implemented on 1 November 2026.
- Entry route: existing implementation. Optimization registered on 7 November 2026.
- Rationale: simplify private mapping logic while preserving behavior.

## Stage boundary and readiness

- Stage: local refactoring and complete SDK test execution.
- Readiness: READY within the [frozen intake scope](01-intake.md#selected-affected-scope-and-risk).
- Assessor: Codex, 7 November 2026, Asia/Singapore.
- Frozen intake Git: `00ca372335962067299f41ece0cda2785f539340`.
- Frozen intake SHA-256: `2040e41872caa6fc36275754a23c4f07835de87da31da43d26066799dfb6c022`.
- Compared implementation: baseline above to SDK `0240b1c260337bf3c38f2b5ecaad2d1ec157296d`.
- Intake integrity: the frozen hash matches before and after implementation.
- Blocked actions: none within local optimization. Artifact publication and deployment are outside scope.
- Owner and next action: Codex; complete the evidence handoff.

## Proposed change

Both changes are implemented in [AuthorizationImpl](../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImpl.java).

| Aspect | Current baseline | Replacement | Basis |
| --- | --- | --- | --- |
| <a id="opt-c1"></a>OPT-C1: Role aliases | Check membership, then retrieve the alias. | Retrieve once; skip missing aliases. | Configuration validation forbids null aliases. |
| <a id="opt-c2"></a>OPT-C2: Subject actions | Store lists as objects and cast them back. | Store typed action lists internally. | Every inserted subject value is a string list. |

## Scope and affected artifacts

| Artifact | Version | Effect | Evidence | Risk and basis | Owner |
| --- | --- | --- | --- | --- | --- |
| Private `mapRoles` | Baseline above plus scoped diff. | Two local simplifications. | [Source](../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImpl.java). | Low change risk; permission errors remain consequential. | Codex |
| Tests, fixtures, properties, exports, and dependencies | Same baseline. | No changes required. | [Baseline hashes](evidence/baseline-result.json). | Existing assertions cover the selected boundaries. | Codex |

## User impact

SDK callers retain the same public methods and permission-map structure.
Selected roles preserve action order, duplicates, and mutable lists.
Excluded roles and invalid responses retain their existing failure behavior.
No user-visible behavior change is intended.

## System impact

`AuthConfiguration` and direct callers construct the same SDK service.
The public `AuthorizationService` interface remains compatible.
Each selected alias now requires one retrieval after configuration validation.
The local subject map no longer requires an unchecked cast.
No throughput or latency gain is claimed without measurement.

## Options and consequences

Keep DTOs, compatibility constructors, and mutable configuration behavior.
Removing these contracts could break unknown external consumers.
Indexing configuration or caching tokens would add lifecycle and compatibility risk without a demonstrated need.

## Proposed acceptance and validation

Reuse the existing canonical cases and all 44 SDK tests.
Do not add duplicate cases for unchanged behavior.

| Criterion | Required validation | Current result | Evidence |
| --- | --- | --- | --- |
| [OPT-AC-1](01-intake.md#acceptance-criteria) | Complete suite, exact assertions, and final diff inspection. | Baseline and candidate pass; 44/44 tests each. | [Baseline](evidence/baseline-result.json) and [candidate](evidence/candidate-result.json). |

### AC-to-test coverage

| Criterion | Canonical cases | Assertion basis | Coverage |
| --- | --- | --- | --- |
| [OPT-AC-1](01-intake.md#acceptance-criteria) | [SDK-TC-001](../single-ui-sdk-ces-migration-20261101/06-test-cases.md#sdk-tc-001), [SDK-TC-002](../single-ui-sdk-ces-migration-20261101/06-test-cases.md#sdk-tc-002), [SDK-TC-004](../single-ui-sdk-ces-migration-20261101/06-test-cases.md#sdk-tc-004), [SDK-TC-007](../single-ui-sdk-ces-migration-20261101/06-test-cases.md#sdk-tc-007) | [Authorization assertions](../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/test/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImplTest.java). | 1/1 scoped criteria have direct assertions. |

### AC-to-code-change coverage

| Criterion | Changed units | Required unchanged behavior | Coverage |
| --- | --- | --- | --- |
| [OPT-AC-1](01-intake.md#acceptance-criteria) | [OPT-C1](#opt-c1) and [OPT-C2](#opt-c2). | Validation, scoping, collisions, action order, duplicate actions, and mutable output. | 1/1 scoped criteria traced; no added product behavior. |

### Code-change-to-test coverage

| Changed unit | Direct assertion chain | Execution |
| --- | --- | --- |
| [OPT-C1](#opt-c1) | [Selected and excluded aliases](../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/test/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImplTest.java:130), [null aliases](../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/test/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImplTest.java:140), [excluded malformed roles](../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/test/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImplTest.java:272), and [invalid aliases](../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/test/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImplTest.java:404). | [Baseline](evidence/baseline-result.json) and [candidate](evidence/candidate-result.json) pass. |
| [OPT-C2](#opt-c2) | [Exact maps, duplicates, and empty roles](../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/test/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImplTest.java:60), [feature/subject aliases](../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/test/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImplTest.java:150), and [subject collisions](../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/test/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImplTest.java:429). | [Baseline](evidence/baseline-result.json) and [candidate](evidence/candidate-result.json) pass. |

Both changed units have direct assertion links: 2/2.
These links do not establish full migration conformance or production parity.
All 44 tests remain in the execution denominator.

## Implementation and release proposal

- Implementation: one production file; no new dependencies or public interfaces.
- Release: no publication or deployment is proposed.
- Reversal: revert the isolated SDK optimization commit.
- Bounded exploration: not applicable; this is an authorized behavior-preserving refactor.

## Sources and evidence limits

| Source | Locator | Identity and authority | Limit |
| --- | --- | --- | --- |
| SDK-OPT-INPUT | [Exact user input](evidence/user-input.md#exact-user-input) | Human request, 7 November 2026. | Optimization authority only. |
| SDK-OPT-BASE | [Baseline result](evidence/baseline-result.json) | SDK revision and exact source/test hashes. | Controlled local execution. |
| Prior design | [Migration design](../single-ui-sdk-ces-migration-20261101/10-change-review.md#selected-compatibility-design) | Preserved migration constraints. | Live entitlement parity remains unverified. |

## Unknowns and blockers

The fresh [offline packaging attempt](evidence/packaging-result.json) stops before tests because formatter-plugin dependencies are absent.
This limits packaging verification. It does not establish an SDK defect.
Owner: unknown for build-environment maintenance; prepare the missing artifacts before the next full lifecycle run.
Live CES/FMAA and deployed consumers remain unverified.
These limits do not block the selected local refactor.
Accountable integration owner: unknown; verify actual consumers before adoption.

## Stage evidence and completion

| Stage | Evidence | Current result | Next action |
| --- | --- | --- | --- |
| Impact and source inspection | [Frozen intake](01-intake.md#selected-affected-scope-and-risk). | Complete. | Preserve selected boundaries. |
| Code review | Scoped diff and independent agent inspection. | No actionable findings. | None within the selected scope. |
| SDK execution | [Baseline](evidence/baseline-result.json) and [candidate](evidence/candidate-result.json). | 44/44 tests pass in both runs; zero failures, errors, or skips. | None within the selected scope. |
| Browser execution | Library-only change; no UI code. | Not applicable. | Use SDK HTTP and Spring assertions. |

## Requested decision and actual disposition

- Actual authorization: simplify and verify the latest SDK change.
- Implementation: SDK commit `0240b1c260337bf3c38f2b5ecaad2d1ec157296d`; one changed production file.
- Execution: baseline and candidate pass all 44 tests. The full offline lifecycle remains blocked by missing plugin dependencies.
- Business acceptance and live migration parity: not assessed.
- Knowledge meaning: unchanged; no domain record update is required.

### Verification reconciliation

The first candidate invocation executed zero tests. Its existing XML reports were stale.
The [runner-failure record](evidence/candidate-runner-failure.json) excludes those reports from passing evidence.
The cause of that discovery failure remains unknown. No application failure was established.
The candidate then compiled and passed in an isolated checkout with matching source hashes.
The first packaging invocation omitted a module argument. The [corrected attempt](evidence/packaging-result.json) records the actual dependency block.

The independent source review found no actionable defect.
Null and empty alias maps retain role names. Excluded aliases still skip grant validation.
Typed values retain mutable maps and lists, action order, and duplicates.
No concurrent configuration mutation or custom stateful map behavior was evaluated.

No new test was needed because existing assertions cover both transformations and their relevant boundaries.
No new feature, dependency, token cache, configuration index, or public contract was introduced.

[Document checks](evidence/document-checks.json) record automated results and pending human reviews.

### API compatibility follow-up, 8 November 2026

The [exact follow-up question](evidence/user-api-compatibility-question-20261108.md#exact-user-input) asks whether the SDK guarantees a transparent migration.
Inspect the supplied EMS2 and CES APIs, current SDK source, and actual consumer contracts.
Keep business-user experience separate from developer integration changes.
This follow-up authorizes assessment only. It changes no application implementation or intended entitlement policy.

**Answer: the current SDK cannot guarantee unchanged user permissions or an integration without modifications.**
Confidence is high for this conclusion from inspected APIs and source.
Business users could retain their screens and workflows after integration and permission equivalence are verified.
Developers must supply configuration and credentials. Some existing consumers also require source adaptation.

#### Evidence-backed claims

| Claim | Class and confidence | Evidence | Meaning and limit |
| --- | --- | --- | --- |
| API-C1: The Java method and nested permission-map shape remain available. | Inspected implementation; high. | [Current mapper](../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImpl.java:53), SDK `0240b1c260337bf3c38f2b5ecaad2d1ec157296d`. | Structure compatibility does not establish identical grants or legacy keys. |
| API-C2: All 60 supplied PROD grant rows match their selected CES catalog role definitions and user memberships. | Static retained-data comparison; high. | [Comparison and source hashes](evidence/api-compatibility-20261108.json). | Three accounts only. CES URLs identify UAT, while EMS2 files are labeled PROD. |
| API-C3: Complete effective permission unions differ in the supplied examples. | Static retained-data comparison; high. | [Effective response](<../ces-entitlement-migration-20261102/api/EMS3-user entitlements by app and user (1481696).yml:238>) and comparison above. | Extra grants may belong to other CES roles. No synchronized production regression is established. |
| API-C4: Current API captures do not supply the assigned-role endpoint used by this SDK. | Inspected API inventory and source; high. | [Default route](../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/properties/AuthProperties.java:38), [DTO](../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/entity/CesRole.java:12), and [actual aggregate schema](<../ces-entitlement-migration-20261102/api/EMS3-user entitlements by app and user (1481696).yml:63>). | An endpoint change alone cannot adapt these bodies. Current support for the required endpoint remains unknown. |
| API-C5: Entitlement lookup needs new CES mappings and caller-owned FMAA credentials. | Inspected implementation; high. | [Required configuration](../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImpl.java:118) and [provider handling](../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/services/implementation/AuthorizationImpl.java:53). | Without a provider, the retained one-argument method returns an empty map. Filter-only usage has a different integration scope. |
| API-C6: One actual consumer has a historical API mismatch. | Inspected implementation; high. | Auth Server [SDK 1.1.1 dependency](../../repos/services/ratan-auth-server/pom.xml:98), [static call](../../repos/services/ratan-auth-server/src/main/java/com/scb/auth/login/controller/LoginController.java:157), and SDK [instance method](../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/util/JwtTokenUtil.java:42). | Source adaptation or a verified compatibility mechanism is needed. This mismatch predates the mapper optimization. No consumer build ran here. |

The [assessment record](evidence/api-compatibility-20261108.json) binds exact API hashes and repository revisions.
Auth Server source is `cacc4d218747e1591d5fb990eb5a8d8bcfb231a5`.
Candidate domain knowledge records remain drafts. They describe the compatibility objective, rather than executed parity.

#### Matched PROD role definitions

| EMS2 PROD example | Selected role | EMS2 pairs | CES catalog pairs | Missing or extra pairs within that role |
| --- | --- | --- | --- | --- |
| `1289935` | `X_RATANONE:FMO_RO` | 27 | 27 | 0 |
| `1289935` | `RATAN_DATA_ENTITLEMENT:Global` | 1 | 1 | 0 |
| `1481696` | `X_RATANONE:NON_FMO_RO` | 28 | 28 | 0 |
| `1481696` | `RATAN_DATA_ENTITLEMENT:Global` | 1 | 1 | 0 |
| `srv.ratan.001` | `RATAN_FUNC:SYS_RO` | 3 | 3 | 0 |

These 60 account grant rows contain 59 distinct entity/role/subject/action tuples.
Matching selected roles does not establish equality of every role returned for the user.
The CES [catalog URL](<../ces-entitlement-migration-20261102/api/EMS3-user entitlements by application.yml:8>) identifies UAT.
Capture synchronization and current deployment applicability remain unknown.

#### Effective response differences and SDK endpoint

| User | EMS2 PROD pair union | CES UAT effective pair union | Extra CES pairs |
| --- | --- | --- | --- |
| `1289935` | 28 | 47 | 19 administration and reporting pairs. |
| `1481696` | 29 | 31 | `Entitlement/View` and `Reports/View`. |

Neither comparison has an old-only pair. Pair unions omit entity and role attribution, ordering, and duplicates.
Extra pairs may be valid CES administration permissions. Their existence still prevents a blanket equality claim.
The SDK must preserve approved role-specific mappings without assigning aggregate grants to every listed role.
FMO Portal Admin remains outside the stated production comparison.

The SDK requests `/fmces/v1/entitlement/user/{userId}` and expects camel-case assigned-role rows.
Current API captures expose app-scoped catalog and app/user aggregate routes with different schemas.
The current mapper rejects missing assigned-role application identity.
Pointing its endpoint property at an aggregate route would not establish compatibility.

The SDK fixture matches a historical assigned-role response recovered from Git.
Its exact revision and hash appear in the assessment record. It contains six roles and 30 unique pairs.
The newer `1481696` effective example contains seven role names and 31 pairs, including the `Global` data grant.
The historical fixture supports parser checks, but cannot establish current complete account equivalence.
These differently sourced captures do not prove a runtime regression.

#### Required evidence for an unchanged business-user experience

1. Verify the supported CES assigned-role endpoint and current response schema for human and service accounts.
2. Reconcile entity, role, feature, subject, action, and required data-scope mappings for each supported consumer.
3. Supply and verify FMAA token renewal and the required CES configuration.
4. Compile actual consumers and compare allowed and denied actions under equivalent assignments.
5. Include additional CES roles, zero-grant roles, failures, and permission revocation in the declared comparison scope.

The acceptance owner remains unknown. These actions support a compatibility claim; they do not grant deployment authorization.
No application fix, live request, consumer build, or new SDK test execution occurred in this follow-up.
The earlier 44 passing tests establish their controlled assertions only.
No new business rule was clarified, so no governed knowledge meaning changed.
The [follow-up checks](evidence/api-compatibility-checks-20261108.json) separate automated validation from pending human reviews.

### Detailed gap explanation request

The [latest user request](evidence/user-seamless-migration-gaps-20261108.md#exact-user-input) asks for detailed seamless-migration gaps.
Keep the SDK/API comparison scope and distinguish business users from application integrators.
Record intended, old, and new results in the task's independent gap document.
No application fixes, deployment, or new entitlement policy are authorized by this explanation request.

The [independent gap register](09-intent-reality-gaps.md#risk-and-issue-entries) records seven SDK and integration gaps.
It separates confirmed source conditions, conditional consequences, and missing execution evidence.
The [source bindings](evidence/gap-source-bindings-20261108.json) reuse retained API captures and record additional inspected source.
The [gap checks](evidence/gap-checks-20261108.json) record document validation, source reconciliation, and pending reviews.
No new business rule or application change results from this explanation.
