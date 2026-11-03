---
artifact_kind: test-case
id: CES-COVERAGE-CASES
version: 4
status: draft
owner: unknown
source_refs: [USER-DETAILED-REPORT-20261103, USER-EMS2-ENV-20261103, USER-COVERAGE-20261103, USER-MOCK-20261103, KT-ces-migration-parity]
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

> **Mock runner checks establish only the supplied-response behavior.**
> Action: retain missing captures and data definitions as unassessed comparison evidence.
> Consequence: two paired examples cannot establish complete migration parity.
> Owner: unknown. Evidence: [mock execution boundary](evidence/coverage-mock-20261103/user-input.md#exact-user-input).

## Objective and traceability

These cases define coverage automation checks for the [current migration scope](01-intake.md#current-task-state).
The [candidate intent](../../knowledge/candidates/security/KT-ces-migration-parity.md#documented-knowledge) defines the mapped permission concepts.
Case definitions have version 4. Actual execution remains separate.

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
| USER-DETAILED-REPORT-20261103 | [Exact reporting request](evidence/ems2-environment-coverage-20261103/detailed-report-user-input.md#exact-user-input) | user-request-20261103-detailed-report | SHA-256 in the [reporting validation](evidence/detailed-coverage-report-20261103/validation.json). | User-defined report scope; existing supplied-response boundary applies. |
| USER-EMS2-ENV-20261103 | [Exact extension request](evidence/ems2-environment-coverage-20261103/user-input.md#exact-user-input) | user-request-20261103-environment-coverage | SHA-256 in the [environment validation](evidence/ems2-environment-coverage-20261103/validation.json). | User-defined tooling scope; mock execution only in this session. |
| USER-COVERAGE-20261103 | [Exact request](evidence/coverage-automation-20261103/user-input.md#exact-user-input) | user-clarification-20261103-1 | `10c503fba499b7dfbcad08481293fcfd9cf0b108f692052bb9f5537a3d89ff57` | User-stated intent; no actual execution or publication approval. |
| USER-MOCK-20261103 | [Exact mock instruction](evidence/coverage-mock-20261103/user-input.md#exact-user-input) | user-clarification-20261103-mock | `72e80490baec682cca54f4288496026105466d2e2b676c7d964bc72f135da887` | User-defined execution boundary; excludes enterprise access from this session. |
| KT-ces-migration-parity | [Candidate knowledge](../../knowledge/candidates/security/KT-ces-migration-parity.md) | Version 1 | Final file hash in its candidate audit event. | Candidate synthesis; human review pending. |
