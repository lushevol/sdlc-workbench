---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Focused validation cases for EMS3 migration review

> **These cases have not executed.**
> Action: Resolve the named policy limits and execute the relevant cases after private dependencies become available.
> Consequence: These definitions provide no passing verification or business acceptance.
> Owner: unknown. Evidence: [review validation](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#validation-evidence).

Catalog version: 1. Prepared: 27 October 2026, Asia/Singapore.
Each case uses the base and candidate revisions recorded in the [review](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#comparison-identity).

The cases propose focused checks or observe current behavior. They are not approved business ACs.
Use isolated fixture services, caches, and storage. Perform no production mutation.

Fixture identifiers are synthetic. Clear created fixture entries and log appenders after each case.
Gherkin order defines the setup, action, and assertion sequence. Behavior execution is NOT_RUN for every case.

## TC-AUTH-01

**Separate data-only reads from full authorization.**

Definition version: 1. Purpose: [AUTH-01](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#auth-01). Level: service/component integration with controlled dependencies.

Expected behavior status: Source defect. Owner: unknown.

Setup and limits: Use isolated repository and cache doubles, but execute the real reader and mapper. DATA_R1 is a fixture mapping.

```gherkin
Scenario: Return bank-user data roles without functional actions
  Given an active FMAA system account has valid full authorization
  And bank user bank-user has mapped data role DATA_R1 and no functional role actions
  And the EMS3 fixture contains nonempty data_entitlements
  When authentication reads the bank-user data roles through the real mapper
  Then dataEntitlementRoles equals DATA_R1
  And the read does not require a functional role or action
```

Assertion mapping: Each Then/And assertion addresses [AUTH-01](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#auth-01).

Executable assertion evidence: See the finding for inspected tests and missing boundaries.

Execution: `NOT_RUN`. Actual results: unavailable. No screenshot or live service evidence exists.

## TC-AUTH-02

**Validate data lists at the data-filter boundary.**

Definition version: 1. Purpose: [AUTH-02](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#auth-02). Level: service/component integration with controlled dependencies.

Expected behavior status: Source defect; P2 narrowed. Owner: unknown.

Setup and limits: Exact no-data response: BLOCKED_PENDING_POLICY. This case checks the exception class only; it specifies no HTTP outcome.

```gherkin
Scenario: Guard a functional-only data-filter response
  Given EMS3 returns the requested user with functional actions and null data_entitlements
  And the data-filter cache is empty
  When the data-filter service converts that response
  Then no NullPointerException escapes the boundary
```

Assertion mapping: Each Then/And assertion addresses [AUTH-02](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#auth-02).

Executable assertion evidence: See the finding for inspected tests and missing boundaries.

Execution: `NOT_RUN`. Actual results: unavailable. No screenshot or live service evidence exists.

## TC-AUTH-03

**Preserve EMS2 role filtering and aggregation.**

Definition version: 1. Purpose: [AUTH-03](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#auth-03). Level: service/component integration with controlled dependencies.

Expected behavior status: Source defect. Owner: unknown.

Setup and limits: Compare role sets, without requiring comma ordering. Empty the fixture cache before each example.

```gherkin
Scenario Outline: Preserve ordinary EMS2 role semantics
  Given EMS2_ONLY mode reads an uncached ordinary user with valid actions
  And the user has <roles>
  When the ordinary entitlement service reads that user
  Then the outcome equals <outcome>

  Examples:
    | roles                      | outcome                                    |
    | ROLE_A and ROLE_B           | role set equals {ROLE_A, ROLE_B}         |
    | RATAN_ENTITLEMENT_SUP_USER  | throws NoRoleException  |
```

Assertion mapping: Each Then/And assertion addresses [AUTH-03](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#auth-03).

Executable assertion evidence: See the finding for inspected tests and missing boundaries.

Execution: `NOT_RUN`. Actual results: unavailable. No screenshot or live service evidence exists.

## TC-AUTH-04

**Clarify unused EMS3 failure configuration.**

Definition version: 1. Purpose: [AUTH-04](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#auth-04). Level: service/component integration with controlled dependencies.

Expected behavior status: Policy question; earlier P1 fallback claim withdrawn. Owner: unknown.

Setup and limits: Observation of current source behavior only. This case does not propose fallback or establish the intended flag contract.

```gherkin
Scenario: Observe the current failure policy independently of failClosed
  Given dual-read has a successful EMS2 shadow response
  And the EMS3 read throws a controlled failure
  And fail-closed is false
  When the migration facade reads the user entitlement
  Then the propagated exception is identical to the controlled EMS3 failure
  And no EMS2 entitlement substitutes for the failed EMS3 result
```

Assertion mapping: Each Then/And assertion addresses [AUTH-04](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#auth-04).

Executable assertion evidence: See the finding for inspected tests and missing boundaries.

Execution: `NOT_RUN`. Actual results: unavailable. No screenshot or live service evidence exists.

## TC-AUTH-05

**Disable raw migration logging by default.**

Definition version: 1. Purpose: [AUTH-05](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#auth-05). Level: service/component integration with controlled dependencies.

Expected behavior status: Source defect; operational exposure unverified. Owner: unknown.

Setup and limits: Capture only EntitlementMigrationFacade, DefaultEms3EntitlementMapper, and Ems2LegacyEntitlementReader. Pre-existing repository logs are excluded. Clear the fixture appender afterward.

```gherkin
Scenario: Keep raw cache contents out of default migration logs
  Given a fixture user has distinct role and data-role markers
  And both migration reads succeed with default logging configuration
  When the migration comparison finishes
  Then the new migration loggers emit zero raw cache payloads at INFO
  And those loggers emit zero complete role-action or data-role marker lists
```

Assertion mapping: Each Then/And assertion addresses [AUTH-05](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#auth-05).

Executable assertion evidence: See the finding for inspected tests and missing boundaries.

Execution: `NOT_RUN`. Actual results: unavailable. No screenshot or live service evidence exists.

## TC-AUTH-06

**Honor cache disabling and mapping version changes.**

Definition version: 1. Purpose: [AUTH-06](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#auth-06). Level: service/component integration with controlled dependencies.

Expected behavior status: Source defect. Owner: unknown.

Setup and limits: v1 and v2 are controlled mapping versions. No stale-age or universal revocation interval is inferred.

```gherkin
Scenario Outline: Apply projection cache controls
  Given an existing projection uses mapping version v1
  And cache controls specify <control>
  When the EMS3 projection service reads the user entitlement
  Then <assertion>

  Examples:
    | control                         | assertion                                               |
    | cache.enabled=false             | projection cache reads and writes have count 0          |
    | configured mapping version v2   | v1 is rejected and refreshed projection reports v2       |
```

Assertion mapping: Each Then/And assertion addresses [AUTH-06](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#auth-06).

Executable assertion evidence: See the finding for inspected tests and missing boundaries.

Execution: `NOT_RUN`. Actual results: unavailable. No screenshot or live service evidence exists.

## TC-AUTH-07

**Resolve removal of the scoped Kong token contract.**

Definition version: 1. Purpose: [AUTH-07](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#auth-07). Level: service/component integration with controlled dependencies.

Expected behavior status: Compatibility finding; external consumers unverified. Owner: unknown.

Setup and limits: Conditional compatibility case. Confirm retirement status first; base assertions provide the historical expected values.

```gherkin
Scenario: Preserve custom scope when compatibility is retained
  Given the scoped v4 token contract remains supported
  And a controlled Kong endpoint accepts custom.scope
  When the client requests GET /v4/kong/token with scope custom.scope
  Then the response status equals 200
  And the outbound token request contains scope=custom.scope
```

Assertion mapping: Each Then/And assertion addresses [AUTH-07](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#auth-07).

Executable assertion evidence: See the finding for inspected tests and missing boundaries.

Execution: `NOT_RUN`. Actual results: unavailable. No screenshot or live service evidence exists.

## TC-BFF-001

**Preserve trusted role identity for admin tokens.**

Definition version: 1. Purpose: [BFF-001](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#bff-001). Level: service/component integration with controlled dependencies.

Expected behavior status: Source defect. Owner: unknown.

Setup and limits: ADMIN_R1 is a fixture role. The trusted role mapping requires approval; a tile owner does not grant user permissions.

```gherkin
Scenario: Keep trusted admin role identity through EMS3 login
  Given the admin entity comes only from a controlled EMS3 response
  And an approved mapping grants the fixture user trusted role ADMIN_R1
  And a target record belongs to ADMIN_R1
  When the user authenticates and submits an authorized admin update
  Then the entitlement token contains the approved role ADMIN_R1
  And the record ownership check accepts ADMIN_R1
  And the role segment does not equal the literal null
```

Assertion mapping: Each Then/And assertion addresses [BFF-001](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#bff-001).

Executable assertion evidence: See the finding for inspected tests and missing boundaries.

Execution: `NOT_RUN`. Actual results: unavailable. No screenshot or live service evidence exists.

## TC-BFF-002

**Preserve application boundaries during permission merging.**

Definition version: 1. Purpose: [BFF-002](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#bff-002). Level: service/component integration with controlled dependencies.

Expected behavior status: Source defect. Owner: unknown.

Setup and limits: Both EMS3 responses must contain valid nonempty role lists. Empty responses are not this case.

```gherkin
Scenario: Keep permissions within their granting application
  Given app A and app B use entity E
  And both non-template tiles require subject S and have no additional data filter
  And app A returns role entitlement S:read
  And app B returns nonempty role entitlement T:read without S
  When the authorization service builds and filters the drawers
  Then app A tile is present exactly once
  And app B tile is absent
  And permissions assigned to app B do not contain S:read
```

Assertion mapping: Each Then/And assertion addresses [BFF-002](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#bff-002).

Executable assertion evidence: See the finding for inspected tests and missing boundaries.

Execution: `NOT_RUN`. Actual results: unavailable. No screenshot or live service evidence exists.

## TC-BFF-003

**Preserve settings omitted by legacy tile updates.**

Definition version: 1. Purpose: [BFF-003](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#bff-003). Level: service/component integration with controlled dependencies.

Expected behavior status: Source defect. Owner: unknown.

Setup and limits: Use normal edit mode. Checker and deactivate branches are outside this case. Authorization effects follow later activation.

```gherkin
Scenario: Preserve EMS3 configuration during a legacy edit
  Given a stored tile uses EMS3 with application APP1 and name AppOne
  And an authorized legacy JSON edit omits all three entitlement fields
  When the controller processes the normal edit
  Then the stored entitlement_source equals EMS3
  And entitlement_app_id equals APP1
  And entitlement_app_name equals AppOne
```

Assertion mapping: Each Then/And assertion addresses [BFF-003](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#bff-003).

Executable assertion evidence: See the finding for inspected tests and missing boundaries.

Execution: `NOT_RUN`. Actual results: unavailable. No screenshot or live service evidence exists.

## TC-BFF-004

**Align advertised fallback with actual failure behavior.**

Definition version: 1. Purpose: [BFF-004](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#bff-004). Level: service/component integration with controlled dependencies.

Expected behavior status: Policy-dependent finding. Owner: unknown.

Setup and limits: Observation of the current test contract only. Define outage versus authoritative-denial policy before corrective acceptance.

```gherkin
Scenario: Observe the current outcome of a migrated-scope outage
  Given legacy tile L uses entity E_L and migrated tile M uses entity E_M
  And EMS2 grants L and EMS3 throws a controlled outage for M
  When dual-read authorization builds the current result
  Then the result contains entity E_L
  And the result does not contain entity E_M
  And the EMS2 request entity list equals [E_L]
  And the EMS2 request entity list excludes E_M
```

Assertion mapping: Each Then/And assertion addresses [BFF-004](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#bff-004).

Executable assertion evidence: See the finding for inspected tests and missing boundaries.

Execution: `NOT_RUN`. Actual results: unavailable. No screenshot or live service evidence exists.

## TC-BFF-005

**Connect entitlement fields to CSV import.**

Definition version: 1. Purpose: [BFF-005](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#bff-005). Level: service/component integration with controlled dependencies.

Expected behavior status: Integration gap; bulk migration intent unconfirmed. Owner: unknown.

Setup and limits: The CSV column names and bulk migration scope require agreement. Existing records currently preserve their prior settings.

```gherkin
Scenario: Persist EMS3 fields from CSV when bulk migration is supported
  Given the agreed CSV contract contains source EMS3 and application APP1 with name AppOne
  And the import contains one new tile and one existing EMS2 tile
  When the real CSV parser and bulk controller persist both records
  Then both saved sources equal EMS3
  And both saved application identifiers equal APP1
  And both saved application names equal AppOne
```

Assertion mapping: Each Then/And assertion addresses [BFF-005](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#bff-005).

Executable assertion evidence: See the finding for inspected tests and missing boundaries.

Execution: `NOT_RUN`. Actual results: unavailable. No screenshot or live service evidence exists.

## TC-BFF-006

**Retain authorization settings in tile audit history.**

Definition version: 1. Purpose: [BFF-006](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#bff-006). Level: service/component integration with controlled dependencies.

Expected behavior status: Source defect. Owner: unknown.

Setup and limits: Use isolated storage fixtures. Read the persisted audit record through the audit service, not only a mock invocation.

```gherkin
Scenario: Reconstruct an entitlement configuration from tile audit history
  Given an authorized operator changes a tile from EMS2 to EMS3
  And the new application identifier equals APP1 with name AppOne
  When the controller saves the tile and its audit record
  Then the audit record contains entitlement_source EMS3
  And the audit record contains entitlement_app_id APP1
  And the audit record contains entitlement_app_name AppOne
```

Assertion mapping: Each Then/And assertion addresses [BFF-006](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#bff-006).

Executable assertion evidence: See the finding for inspected tests and missing boundaries.

Execution: `NOT_RUN`. Actual results: unavailable. No screenshot or live service evidence exists.

## TC-BFF-007

**Compare equivalent authorization scopes.**

Definition version: 1. Purpose: [BFF-007](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#bff-007). Level: service/component integration with controlled dependencies.

Expected behavior status: Source defect. Owner: unknown.

Setup and limits: Use the same logical grants in both sources. If no baseline exists, report unavailable instead of claiming parity.

```gherkin
Scenario: Compare equivalent migrated-scope permissions
  Given controlled EMS2 and EMS3 fixtures grant equivalent permissions for migrated scope M
  And unrelated legacy scope L has its own permissions
  When the parity service compares authorization for M
  Then the compared EMS2 and EMS3 inputs both cover M
  And L does not enter the M comparison
  And the comparison status equals MATCH
```

Assertion mapping: Each Then/And assertion addresses [BFF-007](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#bff-007).

Executable assertion evidence: See the finding for inspected tests and missing boundaries.

Execution: `NOT_RUN`. Actual results: unavailable. No screenshot or live service evidence exists.

## TC-BFF-008

**Remove complete authorization payloads from INFO logs.**

Definition version: 1. Purpose: [BFF-008](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#bff-008). Level: service/component integration with controlled dependencies.

Expected behavior status: Source defect; operational exposure unverified. Owner: unknown.

Setup and limits: Capture AuthorizationResultMapper, TileAuthorizationServiceImpl, AuthorizationComparisonService, and JwtAuthenticationController. Use synthetic markers. Operational logging rules remain unverified.

```gherkin
Scenario: Keep complete functional entitlements out of INFO logs
  Given controlled EMS3 responses contain distinct permission markers
  When the successful login path maps and merges the responses
  Then the new authorization loggers emit zero complete response payloads at INFO
  And those loggers emit zero complete permission lists
```

Assertion mapping: Each Then/And assertion addresses [BFF-008](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/ems3-entitlement-review-20261027/07-code-review.md#bff-008).

Executable assertion evidence: See the finding for inspected tests and missing boundaries.

Execution: `NOT_RUN`. Actual results: unavailable. No screenshot or live service evidence exists.
