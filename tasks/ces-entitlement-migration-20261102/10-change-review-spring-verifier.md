---
artifact_kind: change-request
id: CR-CES-SPRING-VERIFIER-20261104
version: 1
status: draft
owner: unknown
source_refs: [USER-SPRING-VERIFIER-20261104, SDK-BASE, SDK-CANDIDATE]
related_ids: [CES-MIGRATION, CR-CES-SDK-FUNCTION-COVERAGE-20261104]
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

# Spring SDK migration verification project

> **The Spring example passes 32 unit tests and eight actual-SDK replay checks. Company parity remains unverified.**
> Action: follow the [company-network guide](spring-verifier/README.md#3-configure-company-network-execution) with complete reviewed scope and authorized endpoints.
> Consequence: synthetic matches cannot establish complete enterprise migration or seamless consuming application behavior.
> Owner: company execution owner, unknown.
> Evidence: [complete build](evidence/spring-verifier-20261104/full-build-05/result.json) and [actual-SDK replay results](evidence/spring-verifier-20261104/actual-sdk-replays-05/result.json).

## Current task state

The user requests a runnable Spring example for actual EMS2-to-CES SDK migration verification.
The [previous review](10-change-review-sdk-function-coverage.md#current-task-state) supplies the exact implementations and known coverage limits.
Implementation and controlled local verification are complete. Company endpoints remain outside this session's available environment.
The [operating guide](spring-verifier/README.md) provides build, replay, company configuration, and result interpretation.

## Request and source facts

- User input: [4 November request](evidence/spring-verifier-20261104/user-input.md#exact-user-input).
- Entry route: bounded verification-tool implementation using supplied business code.
- Baseline SDK: `b0aa82005e7f14202f85f5ef583f25e42da9eeb3`.
- Candidate SDK: `fd9a157e260850b6d9efa10da3223950ea61133a`.
- Intended result: preserve role-scoped permission meaning without missing or unsupported additional grants.
- Source: [existing compatibility intent](../../knowledge/candidates/security/KT-sdk-and-entitlements.md#sdk-ces-intent-ac-001).
- The tool does not change assignments, business policy, application source, or deployment.
- Preserved intake: Workbench revision `5f9ae762688274d6f1c57fd701b5308c91f1476a`; SHA-256 `5271d9c60da0687a58726e7e37858a998f56e596f7a24673cad961ccbb64b0bd`.

## Stage boundary and readiness

Stage: task-specific Spring verifier implementation and controlled local execution.
Readiness: `READY`. Exact source, user authorization, and measurable tool outcomes support this scope.
Permitted work: standalone task project, acquisition checks, fixtures, reports, tests, and operating guidance.
Stop condition: execute actual baseline and candidate SDK artifacts against controlled HTTP fixtures and retain all outcomes.
Full company acceptance remains dependent on live data, complete inventories, policy evidence, and actual consuming application journeys.
The existing intake remains preserved. No historical approval is inferred.

## Proposed change

Create the [Spring project](spring-verifier/README.md) as a current task-owned verification consumer.
Keep Java outside the single Python Workbench runtime. The installed wheel and generated workspaces remain unchanged.
Use isolated class loaders for the two SDK jars. Their identical package names must not shadow each other.
Default execution uses controlled HTTP fixtures. Live execution requires explicit configuration and credentials.

## Scope and affected artifacts

The project compares actual legacy method outputs, HTTP acquisition outcomes, and exact account/role/subject/action boundaries.
Qualitative risk is high for false positive parity claims and credential disclosure.
Report zero denominators, missing scope, network failures, and malformed responses explicitly.
Existing Workbench coverage commands remain separate and unchanged.

## User impact

The company operator receives an executable Spring project and detailed per-account differences.
Matching examples do not establish complete enterprise migration or seamless downstream user journeys.

## System impact

The task project adds Java 17, Maven, and declared Spring/Jackson test and runtime dependencies.
It uses real SDK jars without changing their source checkout.
Company read-only requests require existing authorized endpoint access.

## Options and consequences

Use actual isolated SDK artifacts to test the original Java lookup contract.
Comparing only direct API payloads cannot establish the adapter's output equivalence.
Keep full migration acceptance separate from scoped SDK-map parity.

## Proposed acceptance and validation

### SPR-AC-001

Execute both actual SDK artifacts and compare all declared accounts through their existing lookup signature.
Every role, subject, action occurrence, empty role, and list-order difference must remain visible.
Canonical definitions: [SPR-TC-001](06-test-cases.md#spr-tc-001) and [SPR-TC-002](06-test-cases.md#spr-tc-002).

### SPR-AC-002

Missing or additional content must prevent scoped parity success.
Failed acquisition, malformed data, incomplete account scope, or missing credentials must remain incomplete.
An empty denominator must not become an unconditional 100% result.
Canonical definitions: [SPR-TC-002](06-test-cases.md#spr-tc-002), [SPR-TC-003](06-test-cases.md#spr-tc-003), and [SPR-TC-004](06-test-cases.md#spr-tc-004).

### SPR-AC-003

Default execution must use local controlled responses without company access or credentials.
Live execution must use bounded HTTP requests and preserve TLS verification.
Each completed account must immediately produce durable sanitized evidence.
Canonical definition: [SPR-TC-005](06-test-cases.md#spr-tc-005).

### SPR-AC-004

The project must build, run, and retain complete passing tests plus controlled actual-SDK integration evidence.
Setup must preserve SDK checkout bytes, declare prerequisites, bound acquisition, and support prepared offline dependencies.
Canonical definition: [SPR-TC-006](06-test-cases.md#spr-tc-006).

### AC-to-test matrix

| Criterion | Canonical cases | Inspected assertions and retained execution | Limit |
| --- | --- | --- | --- |
| [SPR-AC-001](#spr-ac-001) | [001](06-test-cases.md#spr-tc-001), [002](06-test-cases.md#spr-tc-002) | [Comparator assertions](spring-verifier/src/test/java/com/example/migration/PermissionComparisonTest.java), [eight actual-SDK checks](evidence/spring-verifier-20261104/actual-sdk-replays-05/result.json). | Synthetic equal and unequal assignments; complete company inventory unavailable. |
| [SPR-AC-002](#spr-ac-002) | [002](06-test-cases.md#spr-tc-002), [003](06-test-cases.md#spr-tc-003), [004](06-test-cases.md#spr-tc-004) | [Audit assertions](spring-verifier/src/test/java/com/example/migration/SdkBridgeTest.java), [runner assertions](spring-verifier/src/test/java/com/example/migration/VerificationRunnerTest.java), and [missing-token check](evidence/spring-verifier-20261104/missing-live-token-final/result.json). | Complete business scope remains operator-supplied. |
| [SPR-AC-003](#spr-ac-003) | [005](06-test-cases.md#spr-tc-005) | [Report assertions](spring-verifier/src/test/java/com/example/migration/VerificationReportTest.java), [output reconciliation](evidence/spring-verifier-20261104/durable-output-validation-05.json), actual loopback requests. | Immediate checkpoint sequencing is source-inspected. Forced interruption and company TLS remain unexecuted. |
| [SPR-AC-004](#spr-ac-004) | [006](06-test-cases.md#spr-tc-006) | [Full verifier build](evidence/spring-verifier-20261104/full-build-05/result.json), [SDK preparation](evidence/spring-verifier-20261104/qualified-sdk-preparation/preparation.json). | Ordinary offline SDK lifecycle lacks formatter dependencies. Windows and connected preparation remain untested. |

Definition links: 4/4 scoped tool criteria. Inspected assertion links: 4/4 scoped tool criteria.
These counts measure traceability. They do not establish complete business coverage or execution of every setup branch.

### AC-to-code-change matrix

| Criterion | Implementation units | Conformance and limit |
| --- | --- | --- |
| [SPR-AC-001](#spr-ac-001) | [SPR-C01](#spr-c01), [SPR-C02](#spr-c02), [SPR-C04](#spr-c04) | Actual original lookup and exact map predicates passed controlled execution. |
| [SPR-AC-002](#spr-ac-002) | [SPR-C01](#spr-c01), [SPR-C02](#spr-c02), [SPR-C03](#spr-c03) | Missing, additional, failed, malformed, empty, and incomplete boundaries remain distinct. |
| [SPR-AC-003](#spr-ac-003) | [SPR-C01](#spr-c01), [SPR-C03](#spr-c03), [SPR-C05](#spr-c05) | Sanitized output and persisted completed accounts passed. Interruption timing remains source-inspected. |
| [SPR-AC-004](#spr-ac-004) | [SPR-C06](#spr-c06) | Full verifier build passes. Qualified SDK artifacts preserve source and all tests. Full SDK lifecycle remains unavailable offline. |

Implementation links: 4/4 scoped tool criteria. No business implementation changed.
The tool's required behavior does not establish the SDK's complete organizational acceptance criteria.

### Code-change-to-test matrix

#### SPR-C01

The [SDK bridge](spring-verifier/src/main/java/com/example/migration/SdkBridge.java) loads both exact artifacts and audits their real requests.
It validates payloads through each isolated SDK's actual DTO classes before the SDK can swallow conversion failures.

#### SPR-C02

The [comparator](spring-verifier/src/main/java/com/example/migration/PermissionComparison.java) preserves role, subject, action multiplicity, and action sequence.
Effective permission equality cannot conceal role attribution differences.

#### SPR-C03

The [runner](spring-verifier/src/main/java/com/example/migration/VerificationRunner.java) separates match, difference, and unassessed results.
Live mode requires explicit completeness and inventory provenance. Replay defaults cannot authorize live completeness.

#### SPR-C04

The [replay service](spring-verifier/src/main/java/com/example/migration/ReplayServer.java) supplies controlled actual-HTTP fixtures.
Its variants exercise matching, missing, additional, failed, empty, and malformed responses.

#### SPR-C05

The [report writer](spring-verifier/src/main/java/com/example/migration/VerificationReport.java) writes complete JSON, HTML, and Markdown with escaped values.
Reports and account checkpoints preserve all assessed and unassessed results.

#### SPR-C06

The [POM](spring-verifier/pom.xml), [preparer](spring-verifier/prepare-sdks.py), and platform launchers provide task-specific setup and execution.
The [dependency guide](spring-verifier/docs/DEPENDENCIES.md) declares acquisition, platform, and prepared-cache boundaries.

| Changed unit | Direct assertion path | Retained result |
| --- | --- | --- |
| [SPR-C01](#spr-c01) | [SdkBridgeTest](spring-verifier/src/test/java/com/example/migration/SdkBridgeTest.java) and [actual-JAR invocation assertions](evidence/spring-verifier-20261104/verify_project.py). | Passing request, response audit, artifact hash, malformed DTO, and actual lookup checks. |
| [SPR-C02](#spr-c02) | [PermissionComparisonTest](spring-verifier/src/test/java/com/example/migration/PermissionComparisonTest.java). | Ten passing tests cover empty roles, empty subjects, duplicates, order, extra grants, role attribution, and zero denominators. |
| [SPR-C03](#spr-c03) | [VerificationRunnerTest](spring-verifier/src/test/java/com/example/migration/VerificationRunnerTest.java), [live missing-token assertions](evidence/spring-verifier-20261104/missing-live-token-final/result.json). | Six passing unit tests plus controlled completeness and startup failures. |
| [SPR-C04](#spr-c04) | [Replay predicates](evidence/spring-verifier-20261104/verify_project.py). | Eight completed cases through actual SDK artifacts, including six response variants. |
| [SPR-C05](#spr-c05) | [VerificationReportTest](spring-verifier/src/test/java/com/example/migration/VerificationReportTest.java), [artifact reconciliation](evidence/spring-verifier-20261104/durable-output-validation-05.json). | Three passing unit tests, three formats, exact account files, and matching progress records. |
| [SPR-C06](#spr-c06) | [Full build](evidence/spring-verifier-20261104/full-build-05/result.json), [SDK build evidence](evidence/spring-verifier-20261104/qualified-sdk-preparation/preparation.json), and launcher execution. | Verifier packages successfully. Candidate SDK runs all 44 tests; baseline declares zero tests. Setup/platform limits remain explicit. |

Direct assertion links: 6/6 grouped implementation units. Setup acquisition and target-platform execution remain partial.
Documentation and example configuration support these units. They do not add business behavior.

## Implementation and release proposal

No business release, deployment, or organizational acceptance is proposed.
The bounded implementation is complete only after the declared checks pass.

## Sources and evidence limits

Exact user input and baseline/candidate revisions above define this stage.
Known missing account populations, role definitions, data restrictions, and downstream journeys remain explicit acceptance gaps.
No generated report can manufacture those missing facts.

## Unknowns and blockers

Company-network endpoint access and complete population authority remain unknown.
These unknowns limit enterprise conclusions, while permitting the authorized verifier implementation.
Owner: unknown. Next action: run the completed project with reviewed company configuration and retain matching evidence.

## Stage evidence and completion

| Check | Result | Evidence and limit |
| --- | --- | --- |
| Verifier `clean verify` | PASSED, 32 tests; zero failures/errors/skips. | [Build result](evidence/spring-verifier-20261104/full-build-05/result.json), exact source hashes and Surefire assertions. |
| Actual SDK replay | PASSED, eight checks. | [Results](evidence/spring-verifier-20261104/actual-sdk-replays-05/result.json), synthetic HTTP and exact SDK artifact hashes. |
| Missing live credentials | PASSED. | [Result](evidence/spring-verifier-20261104/missing-live-token-final/result.json); no lookup starts, no inherited completeness declaration. |
| Durable report contents | PASSED. | [Reconciliation](evidence/spring-verifier-20261104/durable-output-validation-05.json); interruption timing remains source-inspected. |
| SDK source and candidate tests | PASSED within qualified module goals. | [Preparation manifest](evidence/spring-verifier-20261104/qualified-sdk-preparation/preparation.json); all 44 candidate tests pass, unchanged source. |
| Ordinary offline SDK `clean package` | BLOCKED before compilation. | [Retained failure](evidence/spring-verifier-20261104/qualified-sdk-preparation/ordinary-helper-failure/preparation.json); formatter dependencies unavailable. |
| Company parity and consumer journeys | NOT_RUN. | Live access, complete inventories, deployed consumers, and remote runtime logs unavailable. |

Initial builds and failed sandbox replays remain retained.
The [first replay](evidence/spring-verifier-20261104/actual-sdk-replays/result.json) failed before account lookup.
The [diagnostic replay](evidence/spring-verifier-20261104/actual-sdk-replays-03/result.json) identifies the sandbox socket restriction.
The final authorized loopback execution resolves this local execution limit.
No company request, credential use, source change, or test weakening was required.
No complete connected acquisition or ordinary offline SDK packaging pass is claimed.

Stage: deliver the task-specific verifier and local operating guidance. Status: `READY`.
Assessor: Codex, 4 November 2026. The completed build and actual-SDK checks support this delivery scope.
Company acceptance remains `NOT_VERIFIED`. Missing business evidence does not become an application defect.
ASD writing review and business publication approval remain separate from automated checks.
The [final validation record](evidence/spring-verifier-20261104/validation.json) retains document checks, executable source bindings, and remaining warnings.

## Requested decision and actual disposition

Requested outcome: a runnable Spring example that can detect missing and extra migration permissions.
Implementation state: complete for the task-specific verification project.
Intent review: existing user compatibility objective applies.
Execution outcome: 32 passing verifier tests, eight passing actual-SDK replay checks, and one passing missing-token startup check.
Business acceptance: unverified; no deployment authorization inferred.
