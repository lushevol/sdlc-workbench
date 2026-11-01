---
artifact_kind: test-case
id: TC-SINGLE-UI-CES-300
version: 1
status: draft
owner: unknown
source_refs: [USER-IMPLEMENTATION, SDK-BASE, CES-SAMPLES]
related_ids: [CR-SINGLE-UI-CES-300]
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

# SDK 3.0.0 canonical test cases

> **Controlled fixtures cannot prove deployed permission equivalence.**
> Action: compare approved account assignments through live CES before release acceptance.
> Consequence: passing local tests establishes only the asserted SDK boundaries.
> Owner: unknown. Evidence: [implementation source](evidence/user-clarification-implementation.md).

## Objective and traceability

Test the [authorized migration](10-change-review.md#request-and-source-facts) without inventing role ownership from aggregate grants.
Stable case headings below are the single definitions. Executable tests and coverage reports must link these headings.

| Criterion | Required behavior | Authority |
| --- | --- | --- |
| <a id="ac-compat"></a>AC-COMPAT | Preserve the old Java lookup and nested map where CES supplies sufficient meaning. | User compatibility direction. |
| <a id="ac-token"></a>AC-TOKEN | Use the FMAA token provided by the SDK caller. | User token-ownership direction. |
| <a id="ac-fail"></a>AC-FAIL | Legacy calls return no grants on failure; explicit calls expose classified failures. | Suggested compatibility-preserving engineering policy. |
| <a id="ac-jwt"></a>AC-JWT | Preserve current token validation and request attributes. | Existing SDK contract; user compatibility direction. |
| <a id="ac-build"></a>AC-BUILD | Set version `3.0.0`; execute all applicable tests without skips or failures. | User version and testing directions. |
| <a id="ac-ces"></a>AC-CES | Perform zero EMS2 calls through migrated lookup. | Existing final migration objective. |

## Preconditions and fixtures

| Item | Required state | Setup evidence |
| --- | --- | --- |
| HTTP | Controlled local server or Spring mock transport. No live credentials. | Per-test request expectations. |
| Roles | Synthetic roles A and B with distinct grants under a selected application. | Versioned fixture definitions in executable tests. |
| Compatibility | Same entity/role/subject/action names and assignments for baseline/candidate comparison. | Old DTO-shaped fixture and CES detail-shaped fixture. |
| JWT | Generated RSA test key and signed tokens. Fixed expiry conditions without external sessions. | Per-test Java fixture. |
| Spring | Boot 4.0.6 configuration context and Jackson 2 mapper where required. | Versioned test setup. |

- Environment specification: exact JDK, Maven, dependency inputs, and configuration will be retained with each run.
- Isolation: create new transport, properties, maps, keys, and application context per case.
- Cleanup: close contexts and mock servers. Do not persist tokens or credentials.

## Procedure and assertions

### SDK-TC-001

Criterion: [AC-COMPAT](#ac-compat).

```gherkin
@SDK-TC-001 @AC-COMPAT
Feature: Preserve role-specific legacy map
  Scenario: Preserve role-specific legacy map
    Given roles A and B have distinct feature/action grants under the selected CES application
    When the application requests the user entitlements
    Then the map contains the configured legacy entity and role keys
    And each key contains exactly its own subject/action grants
```

1. Configure the stated fixture.
2. Perform the stated lookup or validation.
3. Assert both stated outcomes.

### SDK-TC-002

Criterion: [AC-COMPAT](#ac-compat).

```gherkin
@SDK-TC-002 @AC-COMPAT
Feature: Preserve scope and legacy filters
  Scenario: Preserve scope and legacy filters
    Given CES returns grants from configured and unrelated applications and features
    When the caller requests configured legacy entities
    Then the map contains 0 unrelated application or excluded entity grants
    And application aliases and feature scopes follow configuration
```

1. Configure the stated fixture.
2. Perform the stated lookup or validation.
3. Assert both stated outcomes.

### SDK-TC-003

Criterion: [AC-TOKEN](#ac-token).

```gherkin
@SDK-TC-003 @AC-TOKEN
Feature: Use caller-provided bearer token
  Scenario: Use caller-provided bearer token
    Given the SDK caller provides the synthetic token test-token
    When the SDK requests assigned-role details
    Then the CES request has Authorization equal to Bearer test-token
    And the request uses the encoded requested user ID and makes 0 EMS2 requests
```

1. Configure the stated fixture.
2. Perform the stated lookup or validation.
3. Assert both stated outcomes.

### SDK-TC-004

Criterion: [AC-COMPAT](#ac-compat).

```gherkin
@SDK-TC-004 @AC-COMPAT
Feature: Reject malformed and unsupported role data
  Scenario: Reject malformed and unsupported role data
    Given a selected CES role has malformed grant identity or an aggregate-only response
    When the caller uses the explicit lookup
    Then the lookup reports invalid response and grants 0 permissions
    And no fabricated role, application, or subject key is returned
```

1. Configure the stated fixture.
2. Perform the stated lookup or validation.
3. Assert both stated outcomes.

### SDK-TC-005

Criterion: [AC-FAIL](#ac-fail).

```gherkin
@SDK-TC-005 @AC-FAIL
Feature: Return empty permissions for valid no-grant response
  Scenario: Return empty permissions for valid no-grant response
    Given CES returns a valid empty assigned-role response
    When the caller requests the user entitlements
    Then the returned map has 0 entries
    And the lookup completes without granting access
```

1. Configure the stated fixture.
2. Perform the stated lookup or validation.
3. Assert both stated outcomes.

### SDK-TC-006

Criterion: [AC-FAIL](#ac-fail).

```gherkin
@SDK-TC-006 @AC-FAIL
Feature: Separate legacy failure compatibility from explicit errors
  Scenario: Separate legacy failure compatibility from explicit errors
    Given CES returns authentication failure, authorization failure, server error, or a transport failure
    When the caller invokes the legacy and explicit lookup paths separately
    Then the legacy lookup returns a map with 0 entries
    And the explicit path reports the applicable classified failure without including the token
```

1. Configure the stated fixture.
2. Perform the stated lookup or validation.
3. Assert both stated outcomes.

### SDK-TC-007

Criterion: [AC-TOKEN](#ac-token).

```gherkin
@SDK-TC-007 @AC-TOKEN
Feature: Validate missing token and configuration
  Scenario: Validate missing token and configuration
    Given the token is missing or configured CES application scope is invalid
    When the caller invokes lookup
    Then the lookup makes 0 HTTP requests
    And the explicit API reports token or configuration failure and the legacy API returns no grants
```

1. Configure the stated fixture.
2. Perform the stated lookup or validation.
3. Assert both stated outcomes.

### SDK-TC-008

Criterion: [AC-COMPAT](#ac-compat).

```gherkin
@SDK-TC-008 @AC-COMPAT
Feature: Preserve baseline map for equivalent assignments
  Scenario: Preserve baseline map for equivalent assignments
    Given EMS2 and CES fixtures define equal entity role subject and action assignments
    When the old and migrated lookup process their respective fixtures
    Then the two returned maps are equal
    And role separation and action values are unchanged
```

1. Configure the stated fixture.
2. Perform the stated lookup or validation.
3. Assert both stated outcomes.

### SDK-TC-009

Criterion: [AC-JWT](#ac-jwt).

```gherkin
@SDK-TC-009 @AC-JWT
Feature: Preserve authentication token validation
  Scenario: Preserve authentication token validation
    Given test tokens have valid or invalid signature issuer expiry and maximum age
    When the application validates each token
    Then only tokens satisfying the existing authentication contract are accepted
    And an entitlement token is rejected as an authentication token
```

1. Configure the stated fixture.
2. Perform the stated lookup or validation.
3. Assert both stated outcomes.

### SDK-TC-010

Criterion: [AC-JWT](#ac-jwt).

```gherkin
@SDK-TC-010 @AC-JWT
Feature: Preserve entitlement token extraction
  Scenario: Preserve entitlement token extraction
    Given valid and invalid entitlement tokens contain a known entitlement text value
    When the application extracts entitlement data
    Then the valid entitlement token returns exactly the expected text
    And invalid or authentication-issuer tokens return null
```

1. Configure the stated fixture.
2. Perform the stated lookup or validation.
3. Assert both stated outcomes.

### SDK-TC-011

Criterion: [AC-JWT](#ac-jwt).

```gherkin
@SDK-TC-011 @AC-JWT
Feature: Preserve request-filter attributes and path selection
  Scenario: Preserve request-filter attributes and path selection
    Given a protected request supplies a valid authentication token and known user fields
    When the SDK filter processes the request
    Then the userInfo attribute preserves userId sessionId oud entitlements and version 3
    And configured excluded paths retain their current validation behavior
```

1. Configure the stated fixture.
2. Perform the stated lookup or validation.
3. Assert both stated outcomes.

### SDK-TC-012

Criterion: [AC-BUILD](#ac-build).

```gherkin
@SDK-TC-012 @AC-BUILD
Feature: Wire the CES implementation and execute release tests
  Scenario: Wire the CES implementation and execute release tests
    Given the supported Spring context has CES properties and a caller token provider
    When the context creates the authorization service and runs its complete test suite
    Then the service uses the CES implementation and version is 3.0.0
    And the declared suite has 0 failures 0 skips and 0 runner errors
```

1. Configure the stated fixture.
2. Perform the stated lookup or validation.
3. Assert both stated outcomes.

## Execution binding

```yaml
execution_status: PASSED_CONTROLLED_SCOPE
repository_id: single-ui-auth-sdk
repository_revision: b0aa82005e7f14202f85f5ef583f25e42da9eeb3
test_revision: evidence/candidate-run-04/inputs.json
assertion_locations: []
environment_identity: macOS-arm64-Java17-SpringBoot4.0.6
execution_id: candidate-run-04-and-compatibility-run-01
actual_results: 44 unit tests and one paired compatibility case passed
retained_execution_refs:
  - evidence/candidate-run-04/result.json
  - evidence/compatibility-run-01/result.json
```

The [execution report](08-test-execution-report.md) binds each case to its retained result.
The source manifest identifies exact worktree bytes before execution; the listed baseline revision remains unchanged.

## Facts, inferences, and unresolved questions

- Facts: the old map is role-specific. The assigned-role CES sample contains feature/action pairs per role.
- Inferences: equivalent reviewed assignments can preserve map values through a scoped adapter.
- Unresolved questions: live endpoint support and full historical role/data assignment equivalence remain unknown.

## Findings

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| Sample captures lack environment and synchronized assignments. | Local equality cannot establish production permission equivalence. | unknown | Compare authorized same-user assignments before acceptance. |

## Sources

| Source ID | Locator | Exact revision | Hash | Owner, authority, and limits |
| --- | --- | --- | --- | --- |
| USER-IMPLEMENTATION | [User clarification](evidence/user-clarification-implementation.md). | 2026-11-01. | Retained input manifest. | User intent. |
| SDK-BASE | [SDK evidence](evidence/sdk-scope.md). | `b0aa82005e7f14202f85f5ef583f25e42da9eeb3`. | Existing manifest. | Source, not execution. |
| CES-SAMPLES | [CES assigned roles](../draft-ces-migration/api/-fmces-v1-entitlement-user-1481696.json). | Capture metadata unknown. | Existing sample manifest. | Structural sample; not current live proof. |
