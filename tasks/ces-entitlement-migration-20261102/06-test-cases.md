---
artifact_kind: test-case
id: CES-COVERAGE-CASES
version: 9
status: draft
owner: unknown
source_refs: [USER-APPLICATION-IDENTITY-20261106, USER-BFF-ENTITY-FIELDS-20261106, USER-FRONTEND-COMPATIBILITY-20261106, USER-FRONTEND-20261105, USER-SPRING-VERIFIER-20261104, USER-DETAILED-REPORT-20261103, USER-EMS2-ENV-20261103, USER-COVERAGE-20261103, USER-MOCK-20261103, KT-ces-migration-parity]
related_ids: [CES-MIGRATION]
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

# CES migration coverage cases

> **Additive BFF metadata does not resolve the existing scalar role contract.**
> Action: verify the [BFF field cases](#bff-entity-field-extension) and retain multiple-role policy as unresolved.
> Consequence: role-dependent upper applications still need a defined mapping.
> Owner: unknown. Evidence: [field request](evidence/frontend-entitlement-impact-20261105/user-bff-entity-fields-20261106.md#exact-user-input).

> **Mock runner checks establish only the supplied-response behavior.**
> Action: retain missing captures and data definitions as unassessed comparison evidence.
> Consequence: two paired examples cannot establish complete migration parity.
> Owner: unknown. Evidence: [mock execution boundary](evidence/coverage-mock-20261103/user-input.md#exact-user-input).

## Objective and traceability

These cases define coverage automation checks for the [current migration scope](01-intake.md#current-task-state).
The [candidate intent](../../knowledge/candidates/security/KT-ces-migration-parity.md#documented-knowledge) defines the mapped permission concepts.
Historical coverage case definitions retain version 4. The Spring extension below has definition version 1.
Actual execution remains separate.

| Criterion | Cases | Observable requirement |
| --- | --- | --- |
| [COV-AC-001](01-intake.md#cov-ac-001) | [TC-COV-001](#tc-cov-001), [TC-COV-003](#tc-cov-003) | Compare application, entitlement, feature, and action relationships. |
| [COV-AC-002](01-intake.md#cov-ac-002) | [TC-COV-002](#tc-cov-002) | Discover and fetch every distinct scoped account. |
| [COV-AC-003](01-intake.md#cov-ac-003) | [TC-COV-003](#tc-cov-003), [TC-COV-008](#tc-cov-008) | Separate assignment, effective permission, and data-scope comparisons. |
| [COV-AC-004](01-intake.md#cov-ac-004) | [TC-COV-004](#tc-cov-004) | Retain matched counts while showing active differences. |
| [COV-AC-005](01-intake.md#cov-ac-005) | [TC-COV-005](#tc-cov-005) | Retain errors and incomplete comparisons without false passes. |
| [COV-AC-006](01-intake.md#cov-ac-006) | [TC-COV-006](#tc-cov-006) | Keep the FMO exception outside production denominators. |
| [COV-AC-007](01-intake.md#cov-ac-007) | [TC-COV-007](#tc-cov-007), [TC-COV-009](#tc-cov-009) | Run both checks in one invocation and retain durable results. |
| [COV-AC-008](01-intake.md#cov-ac-008) | [TC-COV-010](#tc-cov-010) | Default to supplied-response replay with no HTTP or credential loading. |
| [COV-AC-009](01-intake.md#cov-ac-009) | [TC-COV-011](#tc-cov-011), [TC-COV-012](#tc-cov-012) | Compare PROD and UAT without losing environment or entity context. |
| [COV-AC-010](01-intake.md#cov-ac-010) | [TC-COV-013](#tc-cov-013) | Run both comparison families and report their independent and aggregate outcomes. |
| [COV-AC-011](01-intake.md#cov-ac-011) | [TC-COV-014](#tc-cov-014), [TC-COV-015](#tc-cov-015) | Produce complete readable Markdown and HTML without false parity or unsafe rendering. |

## Preconditions and fixtures

| Item | Required state | Setup evidence |
| --- | --- | --- |
| Coverage runner | Exact candidate source revision and hashes are recorded before execution. | Execution record; unavailable until the implementation is inspected. |
| Controlled HTTP services | Local responses implement only the inspected EMS2 and CES request contracts. | Fixture server, request ledger, and response hashes. |
| Source matrices | Temporary workbooks define the case's exact accounts, assignments, and permission content. | Workbook hashes and exact cell locators. |
| Output directory | A new local directory belongs to the current run. | Run identifier and absolute output location. |
| Supplied-response replay | Stored API response bodies are available for the configured requests. | API example hashes and mock execution binding. |

Environment specification: each execution record names controlled endpoints or the actual environment hosts.
Controlled fixtures use synthetic IDs and grants. They do not establish production reachability or permission parity.
Isolation: run against local fixture services with a separate output directory.
Cleanup: stop only the fixture services started by the run. Preserve claim-bearing results before removing temporary resources.

The fixture names below have these definitions:

- `legacy-app` maps to CES application `target-app`.
- EMS2 role `reader` maps to CES entitlement `reader`.
- EMS2 subject `trade` maps to CES feature `trade`.
- EMS2 action `view` maps to CES action `view`.
- `user-a`, `user-b`, `service-c`, and `user-d` are synthetic account IDs.
- A permission definition is the scoped tuple `(application, entitlement, feature, action)`.
- Effective permissions are the mapped feature/action union for one account within one application.

## Procedure and assertions

Each stable case below defines its fixture, comparison action, and explicit observable assertions.
Keep actual results in the execution record, separate from these expected results.

## TC-COV-001

Purpose: compare mapped permission definitions without using numeric ID equality.
Level: controlled comparison unit and runner integration checks.
Criterion: [COV-AC-001](01-intake.md#cov-ac-001).

```gherkin
Feature: Preserve mapped permission definitions
  @TC-COV-001
  Scenario: Equivalent definitions use different source identifiers
    Given EMS2 defines role "reader" in entity "legacy-app" for subject "trade" and action "view"
    And CES defines entitlement "reader" in application "target-app" for feature "trade" and action "view"
    And the explicit mapping connects those four EMS2 concepts to those four CES concepts
    And the EMS2 and CES numeric identifiers differ
    When the coverage runner compares the mapped definitions
    Then the expected definition count equals 1
    And the matched definition count equals 1
    And the missing definition count equals 0
    And the active difference count equals 0
```

Additional boundary: the same feature and action in another application cannot satisfy the expected definition.
The boundary must produce one missing definition within `target-app`.

## TC-COV-002

Purpose: expand multiple accounts, combine discovery sources, and deduplicate requests.
Level: controlled HTTP runner integration.
Criterion: [COV-AC-002](01-intake.md#cov-ac-002).

```gherkin
Feature: Compare every discovered account
  @TC-COV-002
  Scenario: Matrix cells and CES membership expose more than two accounts
    Given a matrix cell contains account IDs "user-a,user-b"
    And another matrix cell contains account IDs "user-b;service-c"
    And the CES application catalog lists account IDs "user-b" and "user-d"
    And each account has a valid controlled EMS2 response and CES response
    And "user-d" has no EMS2 permissions and has one CES permission
    When the coverage runner discovers and compares the scoped accounts
    Then the distinct comparison population equals "user-a,user-b,service-c,user-d"
    And the distinct discovery population count equals 4
    And the baseline account denominator equals 3
    And the request ledger contains one EMS2 permission acquisition for each distinct account
    And the request ledger contains one CES permission acquisition for each distinct account and target application
    And no account is omitted because the supplied examples contain only two accounts
    And the target-only permission for "user-d" remains visible as an additional grant
```

Additional boundaries: list-valued cells, newline delimiters, whitespace, duplicate IDs, and service account punctuation preserve the intended IDs.
An explicitly configured request retry may add attempts. It must not add accounts to the denominator.

## TC-COV-003

Purpose: detect role definition or assignment differences hidden by equal effective grants.
Level: controlled comparison unit and runner integration checks.
Criteria: [COV-AC-001](01-intake.md#cov-ac-001) and [COV-AC-003](01-intake.md#cov-ac-003).

```gherkin
Feature: Compare profile content separately from effective permissions
  @TC-COV-003
  Scenario: Equal effective unions have different profile assignments
    Given EMS2 assigns "user-a" to role "reader" with permission "trade:view"
    And CES assigns "user-a" to entitlement "different-reader" with permission "trade:view"
    And no mapping connects role "reader" to entitlement "different-reader"
    When the coverage runner compares the account assignments and effective permissions
    Then the effective permission comparison matches one permission
    And the assignment comparison reports missing entitlement "reader"
    And the assignment comparison reports additional entitlement "different-reader"
    And the exact profile equality result is not a pass
```

Additional boundary: swapping grants between two entitlements must produce definition differences, even when their combined effective union stays equal.

## TC-COV-004

Purpose: filter completed migration content without erasing counts or additional grants.
Level: controlled comparison unit and report integration checks.
Criterion: [COV-AC-004](01-intake.md#cov-ac-004).

```gherkin
Feature: Show unresolved migration differences
  @TC-COV-004
  Scenario: One grant matches while another is missing and a third is additional
    Given the expected mapped permissions are "trade:view" and "trade:edit"
    And CES returns "trade:view" and "trade:approve" within the same scoped profile
    When the coverage runner writes the comparison report
    Then the expected permission count equals 2
    And the matched permission count equals 1
    And the preservation coverage equals 50 percent
    And the missing permission list contains exactly "trade:edit"
    And the additional permission list contains exactly "trade:approve"
    And the active difference list excludes matched permission "trade:view"
```

CES grants outside the mapped business scope remain separately visible until their classification has an authoritative source.

## TC-COV-005

Purpose: prevent request failures or invalid response bodies from becoming empty, passing comparisons.
Level: controlled HTTP runner integration.
Criterion: [COV-AC-005](01-intake.md#cov-ac-005).

```gherkin
Feature: Keep unavailable comparisons visible
  @TC-COV-005
  Scenario: One account fetch fails within a two-account population
    Given the expected account population contains "user-a" and "user-b"
    And both permission acquisitions succeed for "user-a" with equal scoped content
    And the CES permission acquisition for "user-b" returns an HTTP authentication failure
    When the coverage runner completes the run
    Then the expected account denominator equals 2
    And the assessed account count equals 1
    And the unassessed account count equals 1
    And "user-b" is reported as an acquisition error
    And "user-b" is not reported as equal or as an empty permission profile
    And the report does not claim complete user profile coverage
```

Additional boundaries: timeouts, invalid JSON, unexpected response shape, incomplete pagination, and mismatched returned user IDs remain visible.
Failure details must not include authentication headers, passwords, or token values.

## TC-COV-006

Purpose: honor the user-defined FMO non-production exception.
Level: controlled runner integration.
Criterion: [COV-AC-006](01-intake.md#cov-ac-006).

```gherkin
Feature: Keep non-production FMO scope separate
  @TC-COV-006
  Scenario: Historical FMO rows do not enlarge the production population
    Given a production matrix contains synthetic account "user-a"
    And a historical FMO Portal Admin matrix contains synthetic account "user-b"
    And the current scope marks FMO Portal Admin as a lower-priority non-production exception
    When the coverage runner calculates production migration coverage
    Then the production account denominator equals 1
    And the production entitlement denominator excludes all FMO Portal Admin definitions
    And the FMO exception appears separately with its scope reason
    And the report does not claim current FMO assignment verification from the historical matrix
```

## TC-COV-007

Purpose: complete both checks with one invocation and preserve each completed account result.
Level: controlled HTTP runner integration.
Criterion: [COV-AC-007](01-intake.md#cov-ac-007).

```gherkin
Feature: Run entitlement and account coverage together
  @TC-COV-007
  Scenario: One invocation writes both coverage results and durable account evidence
    Given a scoped definition catalog and two synthetic account responses are available
    And a new output directory belongs to the controlled run
    When the operator invokes the coverage launcher once
    Then the output contains an entitlement coverage result
    And the output contains a user profile coverage result
    And the output contains a human-readable report and machine-readable comparison details
    And each completed account result is durable before processing the next completed account result
    And each retained result identifies its source responses and assessment limits
```

An interruption after the first completed account must leave that account's saved result readable.
The incomplete account inventory must remain visible after the interruption.

## TC-COV-008

Purpose: distinguish functional equality from unavailable data-scope evidence.
Level: controlled comparison and report integration checks.
Criterion: [COV-AC-003](01-intake.md#cov-ac-003).

```gherkin
Feature: Assess data restrictions through authoritative definitions
  @TC-COV-008
  Scenario: Equal profile names lack a comparable legacy data-scope definition
    Given EMS2 and CES both name the account's data profile "Global"
    And the mapped functional permissions are equal
    And CES returns resolved field and value restrictions
    And no authoritative comparable EMS2 field and value definition is available
    When the coverage runner reports the account comparison
    Then the functional permission result can report equality
    And the data-scope comparison is reported as unassessed
    And the report does not claim complete permission profile equality from the name "Global"
```

## TC-COV-009

Purpose: preserve checkpoint identity and prevent silent omission during recovery.
Level: controlled runner recovery integration.
Criterion: [COV-AC-007](01-intake.md#cov-ac-007).

```gherkin
Feature: Retain complete population accounting during recovery
  @TC-COV-009
  Scenario: Recovery retains completed and pending account states
    Given the expected account population contains "user-a" and "user-b"
    And a durable checkpoint identifies a completed comparison for "user-a"
    And the run stops before completing "user-b"
    When the operator resumes or reruns the coverage command using the retained source identity
    Then the final report accounts for both expected accounts
    And the completed result is preserved or replaced by a newly identified acquisition
    And the report contains no silently omitted pending account
    And evidence from a changed configuration is not presented as the unchanged checkpoint result
```

## TC-COV-010

Purpose: verify the default mock workflow without enterprise access or private credentials.
Level: controlled default-entry-point and supplied-response integration checks.
Criterion: [COV-AC-008](01-intake.md#cov-ac-008).
Source: [mock execution boundary](evidence/coverage-mock-20261103/user-input.md#exact-user-input).

```gherkin
Feature: Run supplied responses as mock data
  @TC-COV-010
  Scenario: Default invocation cannot contact enterprise services
    Given configured examples contain a catalog and paired user responses
    And the discovered population contains one account without a paired response
    And HTTP construction, HTTP requests, and private credential loading fail if attempted
    When the operator starts the runner without selecting an execution mode
    Then the execution mode equals "replay"
    And the runner makes zero HTTP requests
    And the runner loads zero private credential files
    And the output labels the execution as mock verification
    And the account without a paired response remains unassessed
    And the final complete-profile coverage rate remains null
```

Additional boundary: supplied credentials or an invalid enterprise CA path must not affect replay execution.
The report must preserve supplied response differences without extrapolating responses to uncaptured accounts.

## TC-COV-011

Purpose: compare EMS2 environment content by names within its entity.
Level: controlled environment-comparator integration checks.
Criterion: [COV-AC-009](01-intake.md#cov-ac-009).
Source: [EMS2 comparison request](evidence/ems2-environment-coverage-20261103/user-input.md#exact-user-input).

```gherkin
Feature: Compare EMS2 PROD with UAT
  @TC-COV-011
  Scenario: Environment IDs differ but business content defines equality
    Given PROD and UAT use different numeric IDs for the same entity, role, subject, and action names
    And account "user-a" has the same named role and permission content in both environments
    And account "user-b" has a UAT role change and a missing PROD subject/action grant
    When the operator runs the environment comparator with stored responses
    Then "user-a" has matching assignments, effective grants, and role-specific grants
    And "user-b" reports its missing and additional role assignments
    And "user-b" reports its missing subject/action grant
    And inventory missing items mean PROD names absent from UAT
    And inventory additional items mean UAT names absent from PROD
    And the same subject name under another entity remains a separate comparison item
    And detailed matched content remains in JSON and leaves active difference rows
```

## TC-COV-012

Purpose: keep incomplete EMS2 environment evidence outside passing coverage.
Level: controlled source, recovery, and denominator checks.
Criteria: [COV-AC-009](01-intake.md#cov-ac-009), [COV-AC-005](01-intake.md#cov-ac-005), [COV-AC-008](01-intake.md#cov-ac-008).
Source: [environment comparison request](evidence/ems2-environment-coverage-20261103/user-input.md#exact-user-input) and [mock boundary](evidence/coverage-mock-20261103/user-input.md#exact-user-input).

```gherkin
Feature: Preserve EMS2 environment evidence limits
  @TC-COV-012
  Scenario: Missing or invalid captures cannot become an equal environment result
    Given the declared population contains an account without a valid UAT response
    And one requested entity inventory is unavailable
    And HTTP client construction and private credential loading fail if attempted
    When the operator runs the default EMS2 environment comparison
    Then the runner uses replay and makes zero HTTP requests
    And the unavailable account remains in the population as unassessed
    And complete-profile coverage remains null
    And the unavailable inventory prevents a complete inventory coverage claim
    And response count or environment-context errors remain visible
    And FMO Portal Admin remains excluded from production denominators
    And each completed account has a durable checkpoint with source identity
    And changed source identities or changed checkpoint content cannot reuse passing evidence
    And empty-role and data-policy equality remain explicitly unassessed
```

## TC-COV-013

Purpose: run the full comparison suite and preserve each result.
Level: controlled suite entry-point integration checks.
Criterion: [COV-AC-010](01-intake.md#cov-ac-010).
Source: [all-coverage guidance request](evidence/ems2-environment-coverage-20261103/user-input.md#exact-user-input).

```gherkin
Feature: Run all configured coverage
  @TC-COV-013
  Scenario Outline: Both comparisons produce an honest combined result
    Given the suite includes the migration and EMS2 environment comparators
    And their controlled outcomes are "<migration>" and "<environment>"
    When the operator runs the suite without selecting an execution mode
    Then both comparators receive replay mode and their declared configurations
    And both comparisons are attempted
    And the dashboard records each actual child outcome and available detailed report
    And the suite returns exit code <exit_code>
    And the suite does not invent a complete cross-comparison coverage percentage

    Examples:
      | migration       | environment      | exit_code |
      | FUNCTIONAL_MATCH | FUNCTIONAL_MATCH | 0         |
      | DIFFERENCES      | FUNCTIONAL_MATCH | 1         |
      | INCOMPLETE       | DIFFERENCES      | 2         |
      | SETUP_ERROR      | FUNCTIONAL_MATCH | 2         |
```

The suite's setup-error case must retain the failure reason and still attempt the other configured comparison.

## TC-COV-014

Purpose: retain full comparison detail in Markdown and HTML from the same result.
Level: renderer and suite integration checks.
Criterion: [COV-AC-011](01-intake.md#cov-ac-011).
Source: [detailed report request](evidence/ems2-environment-coverage-20261103/detailed-report-user-input.md#exact-user-input).

```gherkin
Feature: Explain every coverage difference
  @TC-COV-014
  Scenario: Detailed reports preserve both comparison families and every result row
    Given the suite includes EMS2 PROD to CES UAT and EMS2 PROD to EMS2 UAT
    And the retained results contain missing, additional, matched, and unassessed items
    And user assignments differ while some effective permissions match
    When the suite renders its results
    Then index.md and index.html contain both comparison results without adding their populations
    And each comparison has report.md and report.html with the same measured counts
    And every missing and additional tuple appears in typed detail tables in both formats
    And each user has separate assignment, effective-permission, and role-specific grant results
    And matched items remain counted and available outside the active difference list
    And each matched user appendix retains its account identity and status for search and filtering
    And every unassessed account remains listed with its acquisition or scheduling reason
    And entity exclusions and source bindings remain available through report evidence links
    And all declared report links resolve to the retained output files
```

The supplied-response run must preserve all 747 EMS2 comparison accounts and all 1,051 migration comparison accounts.
These populations overlap. Their counts cannot form a combined account denominator.

## TC-COV-015

Purpose: prevent unsafe text and incomplete evidence from becoming false passing report content.
Level: renderer boundary and failure-isolation checks.
Criteria: [COV-AC-011](01-intake.md#cov-ac-011), [COV-AC-005](01-intake.md#cov-ac-005).
Source: [detailed report request](evidence/ems2-environment-coverage-20261103/detailed-report-user-input.md#exact-user-input).

```gherkin
Feature: Keep report content safe and evidence-bound
  @TC-COV-015
  Scenario: Supplied names and incomplete inventories remain literal and unassessed
    Given a supplied account, role, subject, or label contains HTML and Markdown control characters
    And one required inventory or account response is unavailable
    And full role definitions and data policies are unavailable
    When the runner writes detailed Markdown and HTML
    Then supplied text appears as literal content without executable markup
    And Markdown control characters do not create extra table columns or links
    And unavailable comparisons remain unassessed with their reasons
    And empty denominators do not produce a fabricated coverage percentage
    And role-name presence does not establish equal role-to-subject-to-action definitions
    And full data-profile equality remains unassessed
    And a failed child keeps its actual outcome while the other comparison remains available
    And automated report checks remain separate from pending ASD writing review
```

## Execution binding

```yaml
execution_status: PASSED
repository_id: ai-sdlc-workbench
source_identity: SHA-256 digests retained in detailed-coverage-report-20261103/validation.json
assertion_locations: Direct assertion chains in 10-change-review-coverage-automation.md
environment_identity: Local controlled tests and supplied API response replay
execution_id: detailed-coverage-report-20261103
actual_results:
  tests_run: 850
  failures: 0
  errors: 0
  skips: 0
  comparison_status: INCOMPLETE
retained_execution_refs:
  - evidence/detailed-coverage-report-20261103/validation.json
  - evidence/detailed-coverage-report-20261103/unit-tests-all.log
  - evidence/detailed-coverage-report-20261103/sample-verification.json
```

The [review matrices](10-change-review-coverage-automation.md#ac-to-test-matrix) bind inspected assertion chains to the canonical cases above.
The [validation record](evidence/detailed-coverage-report-20261103/validation.json) binds current source digests to the [850-test execution](evidence/detailed-coverage-report-20261103/unit-tests-all.log).
The [sample verification](evidence/detailed-coverage-report-20261103/sample-verification.json) checks supplied response results and the complete discovered account inventory.
Passing tooling tests do not establish complete environment parity. Both sample comparisons remain `INCOMPLETE` because required captures are unavailable.
Any later live migration evidence requires its own environment and extraction identity.

## Facts, inferences, and unresolved questions

- Facts: the user requires both coverage checks through one script invocation.
- Facts: the user specifies the four-concept mapping and the lower-priority FMO exception.
- Facts: supplied API responses remain the authorized execution data because real environments are inaccessible.
- Facts: the latest request adds EMS2 UAT-versus-PROD comparison and instructions for all coverage scripts.
- Facts: the reporting request requires detailed Markdown and HTML sample outputs from the completed scripts.
- Inference: catalog definitions and effective user responses need separate comparisons because they answer different questions.
- Unresolved: authoritative legacy data restrictions and classification of additional CES management grants remain source-dependent.

## Findings

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| [Current request](evidence/coverage-automation-20261103/user-input.md#exact-user-input) requires all users, beyond the two examples. | A two-account comparison cannot establish complete user coverage. | unknown | Execute dynamic discovery and retain the full inventory. |
| [Candidate intent](../../knowledge/candidates/security/KT-ces-migration-parity.md#evidence-limits) records remaining evidence limits. | Functional agreement alone cannot prove complete data-scope equality. | unknown | Acquire the required legacy data definitions or retain an unassessed result. |

## Sources

| Source ID | Locator | Exact revision | Hash | Owner, authority, and limits |
| --- | --- | --- | --- | --- |
| USER-SPRING-VERIFIER-20261104 | [Exact Spring request](evidence/spring-verifier-20261104/user-input.md#exact-user-input) | user-request-20261104-spring-verifier | `bb3fafbb2b9f3e9770a5f47ee711aa1bc48ce35813f21e13b0523297286d3c5f` | User-defined verification scope; no company access or migration acceptance supplied. |
| USER-DETAILED-REPORT-20261103 | [Exact reporting request](evidence/ems2-environment-coverage-20261103/detailed-report-user-input.md#exact-user-input) | user-request-20261103-detailed-report | SHA-256 in the [reporting validation](evidence/detailed-coverage-report-20261103/validation.json). | User-defined report scope; existing supplied-response boundary applies. |
| USER-EMS2-ENV-20261103 | [Exact extension request](evidence/ems2-environment-coverage-20261103/user-input.md#exact-user-input) | user-request-20261103-environment-coverage | SHA-256 in the [environment validation](evidence/ems2-environment-coverage-20261103/validation.json). | User-defined tooling scope; mock execution only in this session. |
| USER-COVERAGE-20261103 | [Exact request](evidence/coverage-automation-20261103/user-input.md#exact-user-input) | user-clarification-20261103-1 | `10c503fba499b7dfbcad08481293fcfd9cf0b108f692052bb9f5537a3d89ff57` | User-stated intent; no actual execution or publication approval. |
| USER-MOCK-20261103 | [Exact mock instruction](evidence/coverage-mock-20261103/user-input.md#exact-user-input) | user-clarification-20261103-mock | `72e80490baec682cca54f4288496026105466d2e2b676c7d964bc72f135da887` | User-defined execution boundary; excludes enterprise access from this session. |
| KT-ces-migration-parity | [Candidate knowledge](../../knowledge/candidates/security/KT-ces-migration-parity.md) | Version 1 | Final file hash in its candidate audit event. | Candidate synthesis; human review pending. |

## Spring verifier case extension

> **These cases verify the Spring tool within its declared SDK scope.**
> Action: retain separate company evidence before claiming complete migration or seamless application behavior.
> Consequence: passing synthetic checks cannot establish enterprise permission equality.
> Owner: company execution owner, unknown.
> Evidence: [exact Spring request](evidence/spring-verifier-20261104/user-input.md#exact-user-input).

This extension adds six canonical cases. It does not change earlier cases or their historical execution binding.
The [Spring change review](10-change-review-spring-verifier.md#proposed-acceptance-and-validation) defines the four applicable criteria.
The source assertions below implement readable case predicates. They do not execute these Gherkin statements directly.
The [Spring stage evidence](10-change-review-spring-verifier.md#stage-evidence-and-completion) owns current execution results and exact source hashes.

| Criterion | Canonical cases | Defined scope |
| --- | --- | --- |
| [SPR-AC-001](10-change-review-spring-verifier.md#spr-ac-001) | [SPR-TC-001](#spr-tc-001), [SPR-TC-002](#spr-tc-002) | Execute actual SDKs and preserve exact permission maps. |
| [SPR-AC-002](10-change-review-spring-verifier.md#spr-ac-002) | [SPR-TC-002](#spr-tc-002), [SPR-TC-003](#spr-tc-003), [SPR-TC-004](#spr-tc-004) | Reject differences, acquisition failures, incomplete populations, and false percentages. |
| [SPR-AC-003](10-change-review-spring-verifier.md#spr-ac-003) | [SPR-TC-003](#spr-tc-003), [SPR-TC-005](#spr-tc-005) | Keep replay local and retain sanitized, durable evidence. |
| [SPR-AC-004](10-change-review-spring-verifier.md#spr-ac-004) | [SPR-TC-006](#spr-tc-006) | Check builds, prerequisites, artifact preparation, and setup limits. |

### Spring setup and terms

The operator is a developer running the task-owned Spring application on JDK 17 or later.
Controlled execution substitutes loopback HTTP fixtures for EMS2 and CES. It uses no company credentials.
Each run uses a new output directory. Stop only the fixture server started by that run.
Keep reports and completed account evidence after server cleanup.

| Item | Exact definition and source |
| --- | --- |
| Baseline SDK | Revision `b0aa82005e7f14202f85f5ef583f25e42da9eeb3`, loaded from a separately hashed JAR. |
| Candidate SDK | Revision `fd9a157e260850b6d9efa10da3223950ea61133a`, loaded through another isolated class loader. |
| Lookup interface | Original `AuthorizationService.getEntitlements(String userId)` method on both SDKs. |
| Declared accounts | `alice`, `bob`, and `service.demo`, from [replay users](spring-verifier/config/replay-users.csv). |
| Entity scope | `LEGACY_APP`, `LEGACY_DATA`, and `LEGACY_SYSTEM`, from [replay mappings](spring-verifier/config/replay-mappings.json). |
| Role map | The exact structure `entity:role -> subject -> ordered action list`, including empty roles and repeated actions. |
| Account parity | Equality for every declared account with completed acquisition and an explicit population completeness basis. |
| Empty denominator | No expected items exist for that metric; `coveragePercent` remains `null`. |
| Artifact identity | Exact revision metadata and matching SHA-256 bytes for each distinct SDK JAR. |
| Assertion source | [Java tests](spring-verifier/src/test/java/com/example/migration/) and the [actual-SDK probe](evidence/spring-verifier-20261104/verify_project.py). |

## SPR-TC-001

Purpose: preserve exact SDK output across three entities, empty roles, repeated actions, and action order.
Definition version: 1. Level: comparator unit tests and controlled actual-SDK integration.
Criterion: [SPR-AC-001](10-change-review-spring-verifier.md#spr-ac-001).
Source: [exact Spring request](evidence/spring-verifier-20261104/user-input.md#exact-user-input).

```gherkin
Feature: Preserve the original SDK permission contract
  @SPR-TC-001
  Scenario: Actual baseline and candidate SDKs return equal scoped maps
    Given the operator has both exact SDK artifacts and the declared three-account replay setup
    And "alice" has roles "LEGACY_APP:READER", "LEGACY_APP:EMPTY", and "LEGACY_DATA:GLOBAL"
    And "LEGACY_APP:READER" has subject "TRADE" with action list "view,view,export"
    And "LEGACY_APP:EMPTY" has an empty subject map
    And "LEGACY_DATA:GLOBAL" has subject "DATA" with action "view"
    And "bob" has the same reader map
    And "service.demo" has role "LEGACY_SYSTEM:SERVICE" with subject "SYSTEM" and action "query"
    When the operator runs the packaged application with replay variant "match"
    Then the report retains exactly 3 accounts with status "MATCH"
    And the report entity list equals "LEGACY_APP,LEGACY_DATA,LEGACY_SYSTEM"
    And the compared maps retain the empty role and both occurrences of action "view"
    And every account comparison has zero differences
    And the report status equals "SCOPED_SDK_PARITY_PASS" with exit code 0
    And the scoped account parity equals 100 percent
    And the report field "migrationVerified" equals false
```

| Boundary | Explicit predicate | Inspected assertion |
| --- | --- | --- |
| Matching maps | Preserve empty roles, repeated actions, and three entity names. | [Actual-SDK match predicates](evidence/spring-verifier-20261104/verify_project.py#L109-L118), `emptyRolePreserved`, `duplicatesPreserved`, and `threeEntityScopes`. |
| Action order | Reordered actions produce one sequence mismatch, zero missing grants, and a failed exact match. | [Comparator assertions](spring-verifier/src/test/java/com/example/migration/PermissionComparisonTest.java#L75-L83), `reorderedActionsFailExactCompatibilityWithoutInventingMissingPermissions`. |
| Duplicate loss | Removing one repeated action yields one missing occurrence and `66.6667` percent occurrence coverage. | [Comparator assertions](spring-verifier/src/test/java/com/example/migration/PermissionComparisonTest.java#L64-L71), `duplicateLossIsAContractDifferenceDespiteEqualUniquePermissions`. |
| Role attribution | Moving a grant between roles fails exact comparison despite 100 percent effective coverage. | [Comparator assertions](spring-verifier/src/test/java/com/example/migration/PermissionComparisonTest.java#L52-L60), `effectiveUnionCannotHidePermissionMovementBetweenRoles`. |
| Entity identity | Changing entity case produces one missing role and one additional role. | [Comparator assertions](spring-verifier/src/test/java/com/example/migration/PermissionComparisonTest.java#L98-L105), `anotherEntityOrCaseVariantCannotSatisfyTheExpectedScope`. |

## SPR-TC-002

Purpose: prevent missing or additional permissions from receiving scoped parity success.
Definition version: 1. Level: comparator unit tests and controlled actual-SDK integration.
Criteria: [SPR-AC-001](10-change-review-spring-verifier.md#spr-ac-001), [SPR-AC-002](10-change-review-spring-verifier.md#spr-ac-002).

```gherkin
Feature: Detect missing and additional migration content
  @SPR-TC-002
  Scenario Outline: One changed permission prevents a scoped pass
    Given the operator has the declared three-account replay setup
    And the candidate response for "bob" applies variation "<variant>" to "LEGACY_APP:READER"
    When the operator runs the packaged application with replay variant "<variant>"
    Then the report retains exactly 3 assessed accounts
    And the account "bob" has status "DIFFERENT"
    And the differences contain kind "<difference>"
    And the report status equals "DIFFERENCES" with exit code 1
    And the report field "migrationVerified" equals false

    Examples:
      | variant | difference            |
      | missing | MISSING_PERMISSION    |
      | extra   | ADDITIONAL_PERMISSION |
```

The missing fixture removes `TRADE:export`. The extra fixture appends `TRADE:delete`.
Both fixtures preserve the other two accounts.
The extra fixture can retain 100 percent baseline permission coverage. Its additional grant must still prevent success.

Assertion mapping: [actual-SDK difference predicates](evidence/spring-verifier-20261104/verify_project.py#L119-L124) check the difference kind and rejected pass.
[Additional-permission unit assertions](spring-verifier/src/test/java/com/example/migration/PermissionComparisonTest.java#L87-L94) check one additional occurrence despite 100 percent baseline coverage.
[Empty-role assertions](spring-verifier/src/test/java/com/example/migration/PermissionComparisonTest.java#L33-L38) require one missing role when an empty role disappears.
[Empty-subject assertions](spring-verifier/src/test/java/com/example/migration/PermissionComparisonTest.java#L42-L48) require one missing subject when its empty action list disappears.

## SPR-TC-003

Purpose: expose failures hidden by the SDK compatibility method's empty-map fallback.
Definition version: 1. Level: acquisition audit unit tests and controlled actual-SDK integration.
Criteria: [SPR-AC-002](10-change-review-spring-verifier.md#spr-ac-002), [SPR-AC-003](10-change-review-spring-verifier.md#spr-ac-003).

```gherkin
Feature: Keep failed SDK acquisitions outside parity assessment
  @SPR-TC-003
  Scenario Outline: HTTP or DTO failure cannot become empty-map equality
    Given the operator has the declared three-account replay setup
    And replay variation "<variant>" introduces error "<error>"
    When the operator runs the packaged application with replay variant "<variant>"
    Then exactly <unassessed> accounts have status "UNASSESSED"
    And each affected candidate acquisition retains error "<error>"
    And affected accounts have no passing permission comparison
    And the report status equals "INCOMPLETE" with exit code 2
    And the report field "sdkParityPercent" equals null
    And the report field "migrationVerified" equals false

    Examples:
      | variant   | error                                | unassessed |
      | failure   | HTTP_503                             | 1          |
      | malformed | SDK_RESPONSE_DESERIALIZATION_FAILURE | 3          |
```

The HTTP fixture affects `bob`. The malformed fixture supplies `appUID="not-a-number"` to the actual candidate DTO.
The bridge must deserialize complete response bodies before the compatibility method can hide parsing failures.

| Failure boundary | Explicit predicate | Inspected assertion |
| --- | --- | --- |
| Actual HTTP and DTO failures | Preserve HTTP 503 and DTO failures as unassessed acquisitions. | [Actual-SDK failure predicates](evidence/spring-verifier-20261104/verify_project.py#L125-L133), `httpFailureUnassessed` and `dtoErrorsCannotBecomeEmptyParity`. |
| Selected and unselected DTOs | Reject invalid numeric `appUID` in either application scope. | [Typed audit assertions](spring-verifier/src/test/java/com/example/migration/SdkBridgeTest.java#L120-L129), `dtoDeserializationFailureCannotBecomeAnEmptySuccessForSelectedOrUnselectedRoles`. |
| Unused legacy field | Reject malformed `action.id` even when output mapping does not read that field. | [Typed audit assertions](spring-verifier/src/test/java/com/example/migration/SdkBridgeTest.java#L133-L137), `baselineFieldsUnusedByOutputStillMustDeserializeIntoSdkDtos`. |
| Legacy response identity | Reject another user's envelope, inconsistent counts, and unassigned role grants. | [Audit assertions](spring-verifier/src/test/java/com/example/migration/SdkBridgeTest.java#L57-L72). |
| Destination identity | Separate scheme, host, and effective port before request execution. | [Origin assertions](spring-verifier/src/test/java/com/example/migration/SdkBridgeTest.java#L141-L145). |

Live TLS, gateway routing, and actual timeout behavior require company-network execution.
Source inspection alone does not establish those environment outcomes.

## SPR-TC-004

Purpose: keep population completeness, valid empty maps, and artifact identity separate from permission coverage.
Definition version: 1. Level: denominator and configuration unit tests plus controlled actual-SDK integration.
Criterion: [SPR-AC-002](10-change-review-spring-verifier.md#spr-ac-002).

```gherkin
Feature: Require a valid comparison denominator and exact artifacts
  @SPR-TC-004
  Scenario Outline: Scope and identity guards preserve honest status
    Given the operator has the declared three-account replay setup
    And the run applies condition "<condition>"
    When the operator runs the packaged application for that condition
    Then the report status equals "<status>" with exit code <exit>
    And the report field "sdkParityPercent" equals <parity>
    And the report field "migrationVerified" equals false

    Examples:
      | condition                         | status                 | exit | parity |
      | population-complete=false         | INCOMPLETE             | 2    | null   |
      | valid empty assignment responses  | SCOPED_SDK_PARITY_PASS | 0    | 100    |
      | baseline manifest hash mismatch   | INCOMPLETE             | 2    | null   |

  Scenario: Missing live credentials stop SDK acquisition
    Given the operator selects live mode with both base URLs equal to "http://127.0.0.1:1"
    And the environment has no "SDK_VERIFY_CES_TOKEN" value
    And the operator supplies no live completeness declaration or population source
    When the operator runs the packaged application
    Then the report status equals "INCOMPLETE" with exit code 2
    And the report contains zero account lookup results
    And the report field "populationDeclaredComplete" equals false
    And the report field "populationSource" equals an empty string
    And the report field "migrationVerified" equals false
```

Valid empty responses retain `null` coverage for role, subject, and permission denominators.
Their 100 percent account parity describes three completed equal comparisons only.
A mismatched JAR hash must retain `ARTIFACT_SHA256_MISMATCH` and leave every affected account unassessed.

| Guard | Explicit predicate | Inspected assertion |
| --- | --- | --- |
| Integration guards | Empty permission coverage stays null; incomplete populations omit parity; wrong artifacts remain unassessed. | [Actual-SDK guard predicates](evidence/spring-verifier-20261104/verify_project.py#L128-L135). |
| Empty population | Zero declared accounts produce `INCOMPLETE` and null account parity. | [Runner assertions](spring-verifier/src/test/java/com/example/migration/VerificationRunnerTest.java#L26-L28). |
| Live completeness | Live mode requires explicit completeness and a nonblank inventory source. | [Runner assertions](spring-verifier/src/test/java/com/example/migration/VerificationRunnerTest.java#L30-L39), `liveModeRequiresExplicitCompletenessAndSource`. |
| Invalid account list | Duplicate IDs, unsafe IDs, and an empty list raise an input error. | [Runner assertions](spring-verifier/src/test/java/com/example/migration/VerificationRunnerTest.java#L41-L48). |
| Empty permission metrics | Equal empty maps match while every applicable coverage denominator stays null. | [Comparator assertions](spring-verifier/src/test/java/com/example/migration/PermissionComparisonTest.java#L109-L116). |
| Artifact failure | Missing artifacts and mismatched hashes return errors without executing HTTP. | [Bridge assertions](spring-verifier/src/test/java/com/example/migration/SdkBridgeTest.java#L21-L37). |

Missing live credentials must produce `INCOMPLETE` before requests execute.
The [runner's required configuration path](spring-verifier/src/main/java/com/example/migration/VerificationRunner.java) defines that predicate.
The [missing-token startup result](evidence/spring-verifier-20261104/missing-live-token-final/result.json) retains the separate execution assertions.

## SPR-TC-005

Purpose: retain complete reports and each completed account without credentials or executable supplied text.
Definition version: 1. Level: renderer and serialization unit tests plus controlled actual-SDK integration.
Criterion: [SPR-AC-003](10-change-review-spring-verifier.md#spr-ac-003).

```gherkin
Feature: Preserve safe and durable verification evidence
  @SPR-TC-005
  Scenario: A local run preserves account evidence and sanitized reports
    Given the operator has the declared replay setup and a new output directory
    And the controlled service token equals "synthetic-service-token"
    When the operator runs the packaged application with replay variant "match"
    Then execution uses loopback HTTP without company credentials
    And each completed account has a readable numbered JSON checkpoint before the next account starts
    And "progress.json" identifies every completed account and its acquisition outcomes
    And the final directory contains "report.json", "report.html", and "report.md"
    And reports retain account IDs, permission differences, errors, scope, and source hashes
    And reports exclude the controlled service token and authorization headers
    And the report field "migrationVerified" equals false
```

| Boundary | Explicit predicate | Inspected assertion or limit |
| --- | --- | --- |
| Token serialization | Settings text and Jackson properties exclude the service token. | [Bridge assertions](spring-verifier/src/test/java/com/example/migration/SdkBridgeTest.java#L41-L46). |
| Report token retention | The actual-SDK JSON report excludes `synthetic-service-token`. | [Integration assertion](evidence/spring-verifier-20261104/verify_project.py#L136-L138), `syntheticTokenNotRetained`. |
| Complete format output | JSON, HTML, and Markdown retain incomplete status, gaps, and acquisition errors. | [Renderer assertions](spring-verifier/src/test/java/com/example/migration/VerificationReportTest.java#L19-L37). |
| Durable final files | Three report formats exist; account files and progress equal the final report's account results and metrics. | [Final-file assertions](evidence/spring-verifier-20261104/durable-output-validation-05.json); eight replay outputs checked. |
| Supplied markup | HTML escapes supplied script text; Markdown fences remain closed; JSON preserves exact literal values. | [Renderer assertions](spring-verifier/src/test/java/com/example/migration/VerificationReportTest.java#L41-L56). |
| Existing evidence | An existing JSON report is unchanged and prevents creation of replacement HTML. | [Renderer assertions](spring-verifier/src/test/java/com/example/migration/VerificationReportTest.java#L60-L65). |
| Checkpoint timing | Save account JSON and progress before the loop processes another account. | [Runner write order](spring-verifier/src/main/java/com/example/migration/VerificationRunner.java); interruption timing needs separate retained execution. |

Reports contain account and permission data. Use the company's approved evidence storage process.
Interrupted-run recovery and company credential handling remain unverified until matching execution evidence exists.

## SPR-TC-006

Purpose: check the supported build and setup path without changing the independent SDK checkout.
Definition version: 1. Level: complete verifier unit suite, artifact packaging, and setup boundary probes.
Criterion: [SPR-AC-004](10-change-review-spring-verifier.md#spr-ac-004).

```gherkin
Feature: Build a reproducible verification project
  @SPR-TC-006
  Scenario: Approved prerequisites and prepared dependencies build the verifier
    Given the operator has approved JDK 17, Maven 3.8 or later, Git, and Python 3.10 or later
    And the independent SDK checkout contains both exact revisions
    And the Maven cache contains the declared dependencies for offline execution
    And source hashes identify the SDK inputs and verifier inputs
    When the operator runs prerequisite diagnosis
    Then diagnosis reports readiness without dependency acquisition or SDK source changes
    When the operator prepares both SDK artifacts in a new output directory
    Then preparation records each exact revision, artifact hash, command, and complete applicable test counts
    And preparation preserves every exported source input byte
    And each build stops within its configured command deadline
    And failed, skipped, or absent applicable candidate tests prevent readiness
    When the operator runs the complete verifier build
    Then the applicable unit suite has zero failures, zero errors, and zero skipped tests
    And the executable verifier JAR exists
    And verifier source hashes remain unchanged
```

| Setup boundary | Explicit predicate | Evidence and limits |
| --- | --- | --- |
| Full verifier build | Maven exits zero; executed tests exceed zero; failures, errors, and skips equal zero; source bytes stay unchanged. | [Build predicates](evidence/spring-verifier-20261104/verify_project.py#L59-L82). |
| Local diagnosis | `--check` discovers prerequisites without acquisition and states its readiness limits. | [Preparation checks](evidence/spring-verifier-20261104/prepare-helper-checks.json). |
| Command deadline | Invalid deadlines fail; a timed-out build process terminates and retains incomplete status. | [Preparation checks](evidence/spring-verifier-20261104/prepare-helper-checks.json) and [helper deadline handling](spring-verifier/prepare-sdks.py#L170-L186). |
| Source extraction | Reject traversal, absolute archive entries, and symbolic links; extract ordinary source files. | [Preparation checks](evidence/spring-verifier-20261104/prepare-helper-checks.json). |
| Existing artifact | Refuse SDK artifact overwrite before build execution. | [Preparation checks](evidence/spring-verifier-20261104/prepare-helper-checks.json). |
| Artifact qualification | Preserve SDK source hashes and all 44 candidate test results for controlled artifacts. | [Qualified artifact record](evidence/spring-verifier-20261104/qualified-sdk-preparation/preparation.json). |

The baseline revision contains no tracked unit tests. This absence cannot establish baseline unit coverage.
The ordinary offline SDK lifecycle encountered unavailable formatter dependencies.
The [retained failure](evidence/spring-verifier-20261104/qualified-sdk-preparation/ordinary-helper-failure/preparation.json) remains separate from controlled module-goal qualification.
The qualified artifact record does not establish a passing ordinary connected or offline SDK lifecycle.
Windows launchers, company dependency mirrors, and company-network setup require matching platform execution.

### Spring execution binding

```yaml
definition_version: 1
execution_status: PASSED
execution_scope: Inspected unit assertions and eight controlled actual-SDK replay predicates only
repository_id: ai-sdlc-workbench
source_identity: Exact verifier and assertion hashes in the Spring stage evidence
baseline_revision: b0aa82005e7f14202f85f5ef583f25e42da9eeb3
candidate_revision: fd9a157e260850b6d9efa10da3223950ea61133a
assertion_locations:
  - spring-verifier/src/test/java/com/example/migration/PermissionComparisonTest.java
  - spring-verifier/src/test/java/com/example/migration/SdkBridgeTest.java
  - spring-verifier/src/test/java/com/example/migration/VerificationRunnerTest.java
  - spring-verifier/src/test/java/com/example/migration/VerificationReportTest.java
  - evidence/spring-verifier-20261104/verify_project.py
environment_identity: Local controlled HTTP responses; actual exact SDK artifacts
actual_results:
  verifier_tests: 32
  failures: 0
  errors: 0
  skipped: 0
  actual_sdk_replays: 8
  passing_actual_sdk_replays: 8
  complete_enterprise_migration: UNVERIFIED
retained_execution_refs:
  - evidence/spring-verifier-20261104/full-build-05/result.json
  - evidence/spring-verifier-20261104/actual-sdk-replays-05/result.json
  - evidence/spring-verifier-20261104/durable-output-validation-05.json
  - evidence/spring-verifier-20261104/missing-live-token-final/result.json
limits:
  - Forced interruption and checkpoint timing were not executed.
  - Ordinary offline SDK lifecycle failed on unavailable formatter dependencies.
  - Company network and Windows execution remain unverified.
```

Use the [Spring stage evidence](10-change-review-spring-verifier.md#stage-evidence-and-completion) for reconciled execution results.
The [final build](evidence/spring-verifier-20261104/full-build-05/result.json) records 32 passing unit tests without failures, errors, or skips.
The [final replay record](evidence/spring-verifier-20261104/actual-sdk-replays-05/result.json) records eight passing controlled replay predicates.
The [durable output check](evidence/spring-verifier-20261104/durable-output-validation-05.json) confirms final checkpoints and all three report formats.
These final-file checks do not establish checkpoint write timing during interruption.
Earlier failed builds and replays remain historical evidence. They cannot satisfy changed-source case predicates.
Company migration acceptance remains unverified, including data restrictions, unassigned role definitions, and downstream application journeys.

## Frontend compatibility extension

Definition version: 2. Sources: [frontend request](evidence/frontend-entitlement-impact-20261105/user-input.md#exact-user-input) and [compatibility decisions](evidence/frontend-entitlement-impact-20261105/user-clarification-20261106.md#exact-user-input).
These cases support the [frontend impact analysis](05-impact-analysis-frontend-entitlements.md#proposed-acceptance-and-validation).
Historical definitions above retain their existing scope and execution bindings.
The original captures remain canonical. Their hashes appear in the [capture summary](evidence/frontend-entitlement-impact-20261105/capture-summary.json).
Use the [repository bindings](evidence/frontend-entitlement-impact-20261105/bff-contract.json) and [frontend bindings](evidence/frontend-entitlement-impact-20261105/mfe-base.json).
The container has [file hashes](evidence/frontend-entitlement-impact-20261105/ratan-container.json), without independent Git history.
No frontend implementation change exists. User-stated compatibility decisions do not establish passing implementation evidence.
The [knowledge criteria](../../knowledge/candidates/security/KT-ces-migration-parity.md#frontend-compatibility-and-per-tile-migration) define the scoped intent.
Earlier probe results retain their actual source identities and case-definition scope.

### TC-FE-CES-001

Purpose: resolve captured Ratan feature/action grants through the shared helper.
Level: controlled helper compatibility probe. Owner: unknown.
Intent: [permission preservation](../../knowledge/candidates/security/KT-ces-migration-parity.md#mapping-between-authorization-concepts).
Setup: inject captured entities into `Hooks.getHooks`; use no network or browser.
The probe transpiles the original TypeScript module without changing its source.
Isolation: use one Node process. Cleanup: terminate that process after saving the compact result.

1. Load the captured entities into the hooks store.
2. Invoke `hasPermission` for each listed permission.
3. Invoke `hasPermission` for the absent public-view permission.

```gherkin
Feature: Preserve captured CES action access
  @TC-FE-CES-001
  Scenario Outline: Resolve an explicitly granted permission
    Given the capture grants "<permission>" within application "RATAN_ENTITLEMENT_RULE"
    And the hooks store contains the captured entities
    When the shared helper checks "<permission>"
    Then hasPermission returns true

    Examples:
      | permission |
      | RATAN_CASHFLOW_BLOTTER:F_Export_Data |
      | RATAN_CASHFLOW_BLOTTER:F_Custom_Query_Builder |
      | RATAN_CASHFLOW_BLOTTER:F_Custom_View_Builder_Private |
      | RATAN_PROFILE_LIMITS:ACCESS_FMO_POST_TRADE_PORTAL |
      | RATAN_SETTLEMENT_EXCEPTION:ACCESS_FMO_POST_TRADE_PORTAL |

  Scenario: Reject a permission absent from the captured application
    Given the capture has no "RATAN_CASHFLOW_BLOTTER:F_Custom_View_Builder_Public" grant
    When the shared helper checks "RATAN_CASHFLOW_BLOTTER:F_Custom_View_Builder_Public"
    Then hasPermission returns false
```

Assertions and actual results: [original-module probe](evidence/frontend-entitlement-impact-20261105/ratan-container.json).
Five required positive checks fail. The negative check passes.
The complete scan records all 31 captured grants. Seven lack exact feature references in the supplied tile dump.
Those seven remain capture observations, not additional business requirements.
Renaming only the aggregate entity provides a synthetic dispatch control.
That control supplies no actual EMS2 baseline or passing migration result.

### TC-FE-CES-002

Purpose: preserve portal admission for the supplied nonblank CES tile mappings.
Level: source-predicate analysis; browser validation remains `NOT_RUN`. Owner: unknown.
Setup: use the unchanged capture and all 41 returned CES tiles.
No live login or persistent state change occurs during predicate analysis.

1. Read each returned CES tile.
2. Compare its application and subject with captured entities.
3. Inspect each portal launch and workspace caller of `validateTile`.

```gherkin
Feature: Preserve normalized CES tile admission
  @TC-FE-CES-002
  Scenario: Match the supplied CES drawer tiles
    Given the login capture contains 41 EMS3 tiles
    And each tile uses a nonblank subject matching its CES feature
    When the current generic entity and subject predicate evaluates these tiles
    Then 41 tile predicates return true
    And 0 tile predicates return false
```

Actual predicates: [capture summary](evidence/frontend-entitlement-impact-20261105/capture-summary.json).
The replay implements the inspected predicate in Python. It does not execute the original frontend module.
Login, direct launch, saved workspace, refresh, and denial require original-module or browser assertions before verification.
Existing [base tests](evidence/frontend-entitlement-impact-20261105/mfe-base-tests.json) do not assert this capture.

### TC-FE-CES-003

Purpose: characterize admission when CES features differ from legacy subjects.
Level: proposed contract integration case; `NOT_RUN`. Owner: unknown.
Setup: select an approved feature-controlled CES tile. Use an isolated fixture, without database writes.
The fixture grants `feature-a` and sets the tile's legacy subject to `legacy-a`.
Blank-feature access is excluded pending policy reconciliation.

1. Load the isolated authorized-tile fixture.
2. Evaluate direct launch and saved workspace retention.
3. Evaluate a tile absent from the authorized drawer.

```gherkin
Feature: Use one reviewed CES tile admission decision
  @TC-FE-CES-003
  Scenario: Preserve admission when legacy and CES feature names differ
    Given the BFF grants a feature-controlled CES tile through feature "feature-a"
    And the tile legacy subject equals "legacy-a"
    And the current authorized drawer contains that tile
    When the portal evaluates direct launch and saved workspace retention
    Then both paths use the reviewed CES grant decision
    And neither path denies access solely because "legacy-a" differs from "feature-a"
    And a tile absent from the current authorized drawer remains denied
```

Assertion implementation: unavailable. Contract basis: [BFF drawer analysis](evidence/frontend-entitlement-impact-20261105/bff-contract.json).
This proposed expectation requires the shared admission contract before implementation acceptance.
CSV tile `192` has blank fields and is inactive. It does not reproduce this case.

### TC-FE-CES-004

Purpose: manage CES tile metadata through create, edit, checker review, and audit.
Level: proposed frontend/BFF integration case; `NOT_RUN`. Owner: unknown.
Setup: use an authorized admin and isolated tile data. Retain existing maker/checker rules.
Wire fields: `entitlementSource`, `entitlementAppId`, `entitlementAppName`, and `entitlementAppFeature`.
Use source `EMS3`, app ID `51358`, app name `RATAN_ENTITLEMENT_RULE`, and feature `RATAN_CASHFLOW_BLOTTER`.

1. Create the isolated tile with all four fields.
2. Review the tile through a different authorized checker.
3. Change only the tile title.
4. Inspect the submitted payload and audit record.

```gherkin
Feature: Manage CES tile routing
  @TC-FE-CES-004
  Scenario: Preserve four routing fields across the admin workflow
    Given an authorized admin creates a CES tile with the four defined routing fields
    When a different authorized checker reviews the tile
    Then the review displays all four submitted routing values
    When an authorized admin changes only the title
    Then the submitted routing values remain unchanged
    And the audit record displays all four routing values
```

Assertion implementation: unavailable. Source: [admin contract inspection](evidence/frontend-entitlement-impact-20261105/mfe-base.json).
Current fetched-row edits preserve hidden fields through spreading. This case does not allege an observed source reset.
CSV uses a separate backend interface. Extend only actual CSV consumers within their identified scope.

### TC-FE-CES-005

Purpose: keep absent CES role metadata separate from functional grants.
Level: controlled observation plus proposed role-contract validation. Owner: unknown.
Setup: use the captured aggregate with `roleName: null` and no legacy Ratan role.

1. Load the captured aggregate into the isolated hooks store.
2. Invoke `getUser`.
3. Inspect the returned role and its attribution evidence.

```gherkin
Feature: Preserve role attribution boundaries
  @TC-FE-CES-005
  Scenario: Observe missing role metadata without inventing a role
    Given the captured CES entity has no role name
    And no legacy Ratan role is supplied
    When the current shared helper reads the user role
    Then the user role is unavailable
    And no assigned role can be established from the captured feature/action union
```

Observation: [role probe](evidence/frontend-entitlement-impact-20261105/ratan-container.json).
The assigned-role contract remains unresolved. Saved views, filters, and `PSS_RO` checks need separate expected results.
The capture cannot establish those business outcomes. Those assertions remain `NOT_RUN`.
The latest user decision confirms that roles are no longer unique.
Keep existing EMS2 scalar-role behavior unchanged. Multiple-role projection remains an unresolved API decision.
Do not infer multiple assigned role names from this aggregate or select a first role without a decision.

### TC-FE-CES-006

Purpose: prevent permissions from crossing applications or migration providers.
Level: proposed resolver boundary case; `NOT_RUN`. Owner: unknown.
Setup: use isolated EMS2 and CES fixtures with explicit application scope.
Duplicate rows belong to one selected application. Unrelated application grants cannot satisfy its requested permission.

1. Load the isolated application fixtures.
2. Resolve the requested action within `app-a`.
3. Inspect the scoped permission map and unrelated grants.

```gherkin
Feature: Preserve application scope during mixed migration
  @TC-FE-CES-006
  Scenario: Reject another application's grant
    Given application "app-a" has no "feature-a:action-a" grant
    And application "app-b" grants "feature-a:action-a"
    When the resolver checks "feature-a:action-a" within "app-a"
    Then the resolver returns false

  Scenario: Preserve duplicate grants within the selected application
    Given two rows for "app-a" grant different actions for "feature-a"
    When the resolver builds the scoped permission map
    Then both granted actions remain available within "app-a"
    And the resolver adds 0 actions from unrelated applications

  Scenario: Route a legacy tile to its selected provider
    Given a tile selects "EMS2" for feature "feature-a"
    And EMS2 denies "feature-a:action-a"
    And CES grants "feature-a:action-a"
    When the shared resolver checks "feature-a:action-a" for that tile
    Then the resolver returns false through the EMS2 path
    And the CES grant does not override the selected provider

  Scenario: Route a CES tile to its selected provider
    Given a tile selects "EMS3" with configured application "app-a"
    And CES denies "feature-a:action-a" within "app-a"
    And EMS2 grants "feature-a:action-a"
    When the shared resolver checks "feature-a:action-a" for that tile
    Then the resolver returns false through the CES path
    And the EMS2 grant does not override the selected provider
```

Assertion implementation: unavailable. Source: [resolver boundary analysis](evidence/frontend-entitlement-impact-20261105/ratan-container.json).
Matching names alone cannot establish cross-application equivalence.
Effective migration mode and provider precedence require a bound target configuration.
Intent: [FE-COMPAT-AC-002](../../knowledge/candidates/security/KT-ces-migration-parity.md#fe-compat-ac-002).
The resolver interface above is internal. It does not require new upper-application arguments.

### TC-FE-CES-007

Purpose: preserve existing upper-application permission APIs during provider adaptation.
Definition version: 1. Level: proposed compatibility integration case; `NOT_RUN`. Owner: unknown.
Intent: [FE-COMPAT-AC-001](../../knowledge/candidates/security/KT-ces-migration-parity.md#fe-compat-ac-001).
Setup: retain an unchanged upper-application consumer and equivalent mapped EMS2/CES feature/action fixtures.
Bind one tile unambiguously to its provider inside the shared frontend layer.
Use no production state. Dispose of isolated fixture processes after saving results.

1. Load the unchanged consumer with an EMS2 tile fixture.
2. Invoke the existing permission helper.
3. Select the equivalent CES fixture through the shared tile context.
4. Invoke the same consumer call.

```gherkin
Feature: Preserve upper-application permission calls
  @TC-FE-CES-007
  Scenario: Keep feature and action calls unchanged across providers
    Given an upper application imports the existing shared permission helpers
    And the upper application calls hasPermission with "feature-a:action-a"
    And equivalent EMS2 and CES fixtures grant that mapped permission
    When each fixture is evaluated through its selected tile provider
    Then both helper calls return boolean true
    And the upper application requires 0 new mandatory arguments
    And the upper application requires 0 provider-specific import changes
    And the upper application requires 0 feature or action string changes
```

Assertion implementation: unavailable. Design basis: [shared boundary inspection](evidence/frontend-entitlement-impact-20261105/compatibility-design.json).
Include denied equivalents and unchanged higher-level helper calls before acceptance.
The scalar role contract is excluded from this case. Its exception remains in [TC-FE-CES-005](#tc-fe-ces-005).

### TC-FE-CES-008

Purpose: migrate one tile without changing another tile's provider or permission result.
Definition version: 1. Level: proposed mixed-instance integration case; `NOT_RUN`. Owner: unknown.
Intent: [FE-COMPAT-AC-003](../../knowledge/candidates/security/KT-ces-migration-parity.md#fe-compat-ac-003).
Setup: mount two isolated tile instances in one session with distinct internal tile identities.
Both use `feature-a:action-a`. EMS2 grants it, while CES denies it within the configured application.
Start both tiles on EMS2. Keep both mounted during the provider change.
The case does not approve any specific context-binding implementation.

1. Observe both tile permission results on EMS2.
2. Change only tile A to CES.
3. Evaluate both tiles while they remain mounted.
4. Re-evaluate tile B after activating tile A.

```gherkin
Feature: Select entitlement providers independently for each tile
  @TC-FE-CES-008
  Scenario: Change one tile while another tile retains EMS2 behavior
    Given tile A and tile B both select "EMS2"
    And both tiles return true for "feature-a:action-a"
    When only tile A changes to "EMS3" with configured application "app-a"
    Then tile A returns false through the CES path
    And tile B still returns true through its unchanged EMS2 path
    And activating tile A does not change tile B's result
    And tile B requires 0 provider changes
```

Assertion implementation: unavailable. No simultaneous mixed-provider execution was performed.
The [context inspection](evidence/frontend-entitlement-impact-20261105/compatibility-design.json) identifies shared-state and early-evaluation boundaries.
Run module-initialization and mounted-instance variants before claiming complete unchanged-caller compatibility.

## BFF entity field extension

Definition version: 1. Source: [explicit BFF request](evidence/frontend-entitlement-impact-20261105/user-bff-entity-fields-20261106.md#exact-user-input).
The [stage record](10-change-review-bff-entity-fields.md) separates implementation and execution from these case definitions.
Use only local fixtures. No live CES, database, or login endpoint is required.
Run each fixture with a new mapper or service instance. Delete temporary classes after retaining compact execution evidence.
The [unit test assertions](../../repos/services/single-ui-bff/src/test/java/com/scb/sso/singleuibff/service/v2/authorization/AuthorizationResultMapperTest.java) implement the mapper cases.
The [service assertions](../../repos/services/single-ui-bff/src/test/java/com/scb/sso/singleuibff/service/v2/authorization/Ems3ApplicationNameAuthorizationTest.java) implement application separation.

### TC-BFF-ENTITY-001

Purpose: expose corresponding CES entitlement names and preserve their complete list.
Intent: [BFF-ENTITY-AC-001](../../knowledge/candidates/security/KT-ces-migration-parity.md#bff-entity-ac-001).
Level: mapper and JSON serialization unit case. Owner: unknown.

```gherkin
Feature: Return CES entitlement names
  @TC-BFF-ENTITY-001
  Scenario: Return all seven names from the supplied application example
    Given the CES response contains the seven entitlement_name values in the supplied example
    And the response grants feature "positions" action "read"
    When the BFF maps and serializes that application's EMS3 entities
    Then each entity roleList equals the seven source names in source order
    And each entity still grants feature "positions" action "read"
    And each entity roleName and roleId remain null
```

Assertions: exact list equality, seven serialized entries, unchanged action, and no invented scalar role.
Fixture names come from the [supplied CES capture](api/EMS3-user%20entitlements%20by%20app%20and%20user%20%281481696%29.yml).

### TC-BFF-ENTITY-002

Definition version: 2. The original ITAM assertion remains unchanged.
The added scenario follows the [identity clarification](evidence/frontend-entitlement-impact-20261105/user-clarification-application-identity-20261106.md#exact-user-input).
Purpose: preserve the CES application identifier, authorization name, and legacy team label separately.
Intent: [BFF-ENTITY-AC-002](../../knowledge/candidates/security/KT-ces-migration-parity.md#bff-entity-ac-002).
Level: mapper and JSON serialization unit case. Owner: unknown.

```gherkin
Feature: Return CES application identity
  @TC-BFF-ENTITY-002
  Scenario: Use the response ITAM identifier for applicationId
    Given the CES response user_data.itam_id equals "51358"
    And the test invokes the mapper with configured identifier "configured-id"
    When the BFF maps and serializes that application's EMS3 entities
    Then each applicationId equals the JSON string "51358"
    And each legacy entity id remains null
```

Assertions: response-sourced exact value, textual JSON type, and unchanged legacy entity ID.
The mismatched configured identifier proves the selected mapping source only. It does not approve mismatched upstream responses.

```gherkin
Feature: Keep legacy team labels separate from CES identity
  @TC-BFF-ENTITY-002
  Scenario: Preserve the clarified RATAN application mapping
    Given a CES response has user_data.itam_id "51358"
    And its CES application name is "RATAN_ENTITLEMENT_RULE"
    And the configured legacy team name for "51358" is "RATAN"
    When the mapper builds the CES entity with that team mapping
    Then name equals "RATAN_ENTITLEMENT_RULE"
    And applicationName equals "RATAN"
    And applicationId equals the JSON string "51358"
```

Assertions: [mapper identity test](../../repos/services/single-ui-bff/src/test/java/com/scb/sso/singleuibff/service/v2/authorization/AuthorizationResultMapperTest.java#L63-L74).
This added scenario is `NOT_RUN`. The earlier 33 passing invocations predate it.

### TC-BFF-ENTITY-003

Purpose: preserve an EMS2 entity's existing JSON fields without null CES additions.
Intent: [BFF-ENTITY-AC-003](../../knowledge/candidates/security/KT-ces-migration-parity.md#bff-entity-ac-003).
Level: DTO serialization unit case. Owner: unknown.

```gherkin
Feature: Preserve EMS2 entity serialization
  @TC-BFF-ENTITY-003
  Scenario: Round trip the legacy entity fixture
    Given an EMS2 entity contains numeric entity and role IDs
    And it contains scalar roleName "maker" and a subject with one action
    When the BFF deserializes and serializes that entity
    Then its JSON tree equals the original legacy fixture
    And applicationId and roleList are absent
```

Assertions: complete JSON tree equality and absence of both new fields.
This case establishes fixture serialization only. Existing dual-provider tests cover unchanged EMS2 routing separately.

### TC-BFF-ENTITY-004

Purpose: keep optional metadata absence independent from effective action grants.
Intent: [BFF-ENTITY-AC-003](../../knowledge/candidates/security/KT-ces-migration-parity.md#bff-entity-ac-003).
Level: mapper unit case. Owner: unknown.

```gherkin
Feature: Preserve grants when optional metadata is missing
  @TC-BFF-ENTITY-004
  Scenario: Map a previously accepted response without optional CES metadata
    Given a CES response grants feature "positions" action "read"
    And its user_data and entitlement_name values are absent
    When the BFF maps that response
    Then the entity still grants feature "positions" action "read"
    And roleList equals an empty array
    And applicationId is absent from serialized JSON
```

Assertions: unchanged granted action, an empty list, and no fabricated application identifier.

### TC-BFF-ENTITY-005

Purpose: preserve application identity and role lists through service assembly.
Intent: [BFF-ENTITY-AC-001](../../knowledge/candidates/security/KT-ces-migration-parity.md#bff-entity-ac-001) and [BFF-ENTITY-AC-002](../../knowledge/candidates/security/KT-ces-migration-parity.md#bff-entity-ac-002).
Level: actual authorization service with mocked upstreams. Owner: unknown.

```gherkin
Feature: Keep CES applications separate
  @TC-BFF-ENTITY-005
  Scenario: Preserve separate grants for equal names with different application IDs
    Given application "APP" with ITAM ID "51358" grants "feature:read" and roles "maker" and "common"
    And application "APP" with ITAM ID "other-id" grants "feature:write" and role "checker"
    And the service selects EMS3_ONLY mode
    When the BFF assembles authorization for both configured tiles
    Then it returns exactly two entities with applicationId values "51358" and "other-id"
    And the first entity has only roles "maker" and "common" and action "read"
    And the second entity has only role "checker" and action "write"
    And the EMS2 authorization service receives zero calls
```

Assertions: two entities, exact application IDs, isolated role lists, isolated action sets, and zero EMS2 interaction.
