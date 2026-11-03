---
artifact_kind: test-case
id: CES-COVERAGE-CASES
version: 1
status: draft
owner: unknown
source_refs: [USER-COVERAGE-20261103, KT-ces-migration-parity]
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

> **Controlled runner checks cannot establish live migration parity.**
> Action: retain paired EMS2 production and CES UAT responses for the full scoped account population.
> Consequence: controlled outcomes establish runner behavior within their declared fixtures only.
> Owner: unknown. Evidence: [user request](evidence/coverage-automation-20261103/user-input.md#exact-user-input).

## Objective and traceability

These cases define coverage automation checks for the [current migration scope](01-intake.md#current-task-state).
The [candidate intent](../../knowledge/candidates/security/KT-ces-migration-parity.md#documented-knowledge) defines the mapped permission concepts.
Case definitions have version 1. Actual execution remains separate.

| Criterion | Cases | Observable requirement |
| --- | --- | --- |
| [COV-AC-001](01-intake.md#cov-ac-001) | [TC-COV-001](#tc-cov-001), [TC-COV-003](#tc-cov-003) | Compare application, entitlement, feature, and action relationships. |
| [COV-AC-002](01-intake.md#cov-ac-002) | [TC-COV-002](#tc-cov-002) | Discover and fetch every distinct scoped account. |
| [COV-AC-003](01-intake.md#cov-ac-003) | [TC-COV-003](#tc-cov-003), [TC-COV-008](#tc-cov-008) | Separate assignment, effective permission, and data-scope comparisons. |
| [COV-AC-004](01-intake.md#cov-ac-004) | [TC-COV-004](#tc-cov-004) | Retain matched counts while showing active differences. |
| [COV-AC-005](01-intake.md#cov-ac-005) | [TC-COV-005](#tc-cov-005) | Retain errors and incomplete comparisons without false passes. |
| [COV-AC-006](01-intake.md#cov-ac-006) | [TC-COV-006](#tc-cov-006) | Keep the FMO exception outside production denominators. |
| [COV-AC-007](01-intake.md#cov-ac-007) | [TC-COV-007](#tc-cov-007), [TC-COV-009](#tc-cov-009) | Run both checks in one invocation and retain durable results. |

## Preconditions and fixtures

| Item | Required state | Setup evidence |
| --- | --- | --- |
| Coverage runner | Exact candidate source revision and hashes are recorded before execution. | Execution record; unavailable until the implementation is inspected. |
| Controlled HTTP services | Local responses implement only the inspected EMS2 and CES request contracts. | Fixture server, request ledger, and response hashes. |
| Source matrices | Temporary workbooks define the case's exact accounts, assignments, and permission content. | Workbook hashes and exact cell locators. |
| Output directory | A new local directory belongs to the current run. | Run identifier and absolute output location. |
| Live comparison | Authorized EMS2 production and CES UAT access is configured privately. | Environment identity and acquired response evidence. |

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

## Execution binding

```yaml
execution_status: NOT_RUN
repository_id: ai-sdlc-workbench
repository_revision: null
test_revision: null
assertion_locations: []
environment_identity: null
execution_id: null
actual_results: null
retained_execution_refs: []
```

The execution record must bind each inspected assertion to its canonical case above.
These definitions do not establish implemented tests or passing execution.
Actual live migration results must identify production and UAT hosts, extraction times, source versions, and the complete account inventory.

## Facts, inferences, and unresolved questions

- Facts: the user requires both coverage checks through one script invocation.
- Facts: the user specifies the four-concept mapping and the lower-priority FMO exception.
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
| USER-COVERAGE-20261103 | [Exact request](evidence/coverage-automation-20261103/user-input.md#exact-user-input) | user-clarification-20261103-1 | `10c503fba499b7dfbcad08481293fcfd9cf0b108f692052bb9f5537a3d89ff57` | User-stated intent; no actual execution or publication approval. |
| KT-ces-migration-parity | [Candidate knowledge](../../knowledge/candidates/security/KT-ces-migration-parity.md) | Version 1 | Final file hash in its candidate audit event. | Candidate synthesis; human review pending. |
