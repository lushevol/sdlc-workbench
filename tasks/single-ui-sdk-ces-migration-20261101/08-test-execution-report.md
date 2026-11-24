---
artifact_kind: test-execution-report
id: EXEC-SINGLE-UI-CES-300
version: 1
status: draft
owner: unknown
source_refs: [USER-IMPLEMENTATION, SDK-BASE, CES-SAMPLES]
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

# SDK 3.0.0 test execution

> **All 44 tests pass; complete live permission compatibility remains unproved.**
> Action: verify comparable assignments and actual consumers before migration acceptance.
> Consequence: local results cannot establish deployed permission equality.
> Owner: unknown. Evidence: [final results](evidence/candidate-run-04/result.json) and [sample differences](evidence/role-compatibility-design.md#sample-comparisons).

## Run identity and provenance

- Execution: `candidate-run-04`; offline `clean verify`, exit `0`.
- Baseline: SDK `b0aa82005e7f14202f85f5ef583f25e42da9eeb3`.
- Candidate: uncommitted bytes recorded before execution in [inputs](evidence/candidate-run-04/inputs.json).
- Time: 2026-11-01T15:53:23.598702+00:00 through 2026-11-01T15:53:27.883702+00:00, UTC.
- Environment: macOS arm64, Java 17, Maven 3.9.16, declared Spring Boot `4.0.6`.
- Exact tools: [environment](evidence/candidate-run-04/environment.txt).
- Results: 44 tests, zero failures, zero errors, zero skips.
- Source integrity: no recorded file changed during execution.
- Formatter: disabled to preserve source. No tests were excluded.
- Connected preparation: [run 03](evidence/candidate-run-03/result.json) completed with public Maven artifact downloads.
- Final artifact: `single-ui-sdk-starter/target/fmoportal-auth-sdk-3.0.0.jar`.
- Artifact SHA-256: `6c7b0f6e331b6f4a4724a44618cbcac506c5da1aeec03e3055027329818d02d1`.

## Browser environment and suite completeness

Browser execution is not applicable. This library changes service lookup and retains servlet and JWT behavior.
CES HTTP responses use Spring mock transport. RSA keys and JWTs are synthetic local fixtures.
No live CES, FMAA token acquisition, remote logs, deployed consumer, or business workflow executed.
The complete declared JUnit suite ran. The baseline compiled on Java 17 but contained zero tests.
The [paired comparison](evidence/compatibility-run-01/result.json) separately executed one caller against baseline and candidate classes.
That caller was compiled once against the baseline API. Both executions asserted the same permission map.
Their response shapes differ because each upstream contract differs.
Equivalent assignments, role names, subject names, action order, duplicates, and empty-role expectations remain constant.

## Assertions and outcomes

All case IDs link their canonical setup, numbered steps, and assertions.
The [coverage record](09-coverage.md) links exact executable assertions and source changes separately.
The [case result inventory](evidence/candidate-run-04/result.json) records each executed Java method.

| Test ID | Inspected predicate | Actual outcome | Evidence |
| --- | --- | --- | --- |
| [SDK-TC-001](06-test-cases.md#sdk-tc-001) | Preserve role-specific map, order, duplicates, and empty roles. | PASSED in controlled fixtures. | [JUnit results](evidence/candidate-run-04/result.json). |
| [SDK-TC-002](06-test-cases.md#sdk-tc-002) | Exclude unrelated scopes and apply configured aliases. | PASSED, including missing unrelated grant lists. | [JUnit results](evidence/candidate-run-04/result.json). |
| [SDK-TC-003](06-test-cases.md#sdk-tc-003) | Send the caller bearer token and encoded user path without EMS2 requests. | PASSED. | [JUnit results](evidence/candidate-run-04/result.json). |
| [SDK-TC-004](06-test-cases.md#sdk-tc-004) | Reject malformed selected data without fabricated or partial grants. | PASSED. | [JUnit results](evidence/candidate-run-04/result.json). |
| [SDK-TC-005](06-test-cases.md#sdk-tc-005) | Return zero permissions for valid empty assignments. | PASSED. | [JUnit results](evidence/candidate-run-04/result.json). |
| [SDK-TC-006](06-test-cases.md#sdk-tc-006) | Classify failures and preserve legacy empty-map results. | PASSED. | [JUnit results](evidence/candidate-run-04/result.json). |
| [SDK-TC-007](06-test-cases.md#sdk-tc-007) | Reject missing token or invalid scope before HTTP; return no legacy grants. | PASSED. | [JUnit results](evidence/candidate-run-04/result.json). |
| [SDK-TC-008](06-test-cases.md#sdk-tc-008) | Compare baseline and candidate through an unchanged compiled caller. | PASSED; equal maps, two old requests and one CES request. | [Paired results](evidence/compatibility-run-01/result.json) and [probe assertions](evidence/CompatibilityProbe.java). |
| [SDK-TC-009](06-test-cases.md#sdk-tc-009) | Validate authentication JWT issuer, signature, and expiry. | PASSED. | [JUnit results](evidence/candidate-run-04/result.json). |
| [SDK-TC-010](06-test-cases.md#sdk-tc-010) | Validate entitlement JWT and preserve extracted content. | PASSED. | [JUnit results](evidence/candidate-run-04/result.json). |
| [SDK-TC-011](06-test-cases.md#sdk-tc-011) | Preserve filter attributes and authentication rejection/bypass behavior. | PASSED. | [JUnit results](evidence/candidate-run-04/result.json). |
| [SDK-TC-012](06-test-cases.md#sdk-tc-012) | Bind CES configuration and create SDK Spring beans. | PASSED with and without a token provider. | [JUnit results](evidence/candidate-run-04/result.json). |

## Coverage inventories and summary

The declared inventory has six scoped criteria and twelve canonical cases.
All twelve cases have passing controlled execution. These are not twelve production journeys.
The [coverage record](09-coverage.md) owns predicate inventories, three matrices, and qualified denominators.
No line coverage measurement or complete production permission-equivalence percentage is claimed.

### AC to test case coverage

See [AC-to-test matrix](09-coverage.md#ac-to-test-case-coverage) for criteria, assertions, matching results, and limits.

### AC to code change coverage

See [AC-to-change matrix](09-coverage.md#ac-to-code-change-coverage) for changed and retained implementation.

### Code change to test case coverage

See [change-to-test matrix](09-coverage.md#code-change-to-test-case-coverage) for each meaningful unit and its direct assertions.

## Retained evidence inventory

| Evidence | Locator | Integrity and limit |
| --- | --- | --- |
| Final inputs | [Pre-run manifest](evidence/candidate-run-04/inputs.json). | Exact source/test hashes and command. |
| Final output | [Build log](evidence/candidate-run-04/build.log) and [result](evidence/candidate-run-04/result.json). | Full offline build; zero failures, errors, or skips. |
| Original runner files | [Surefire reports](evidence/candidate-run-04/surefire-reports/). | Controlled JVM assertions and tool properties. |
| Compatibility caller | [Probe](evidence/CompatibilityProbe.java) and [inputs](evidence/compatibility-run-01/inputs.json). | Compiled against unchanged baseline. |
| Paired comparison | [Baseline](evidence/compatibility-run-01/baseline-result.json) and [candidate](evidence/compatibility-run-01/candidate-result.json). | Synthetic equivalent assignments only. |
| Baseline build | [Baseline result](evidence/baseline-build-result.json). | Compilation succeeds; no baseline tests exist. |
| Earlier attempts | [Run 01](evidence/candidate-run-01/result.json), [run 02](evidence/candidate-run-02/result.json), [run 03](evidence/candidate-run-03/result.json). | Compile/setup and dependency failures remain visible. Runs 02/03 lack pre-run source manifests. |
| Independent review | [Review](evidence/sdk-code-review.md). | Initial sample assertion and scope-isolation findings were corrected. |

## Browser evidence bindings

Not applicable. No browser journey or screenshot is used to support these JVM claims.

## Verification conclusion

The final source passes its complete declared unit suite and offline artifact packaging.
The paired case preserves map equality for the stated equivalent role assignments.
JWT validation and filter assertions pass against unchanged authentication code.
The default lookup retains empty-map failure behavior. The additive explicit API reports sanitized failure reasons.
The caller owns FMAA token supply and refresh. No credential acquisition, caching, or automatic retry was added.
These results support local implementation confidence: HIGH.
Full migration compatibility remains MEDIUM confidence because live assignments and actual consumer builds remain unavailable.
Missing environments are evidence limits. They do not demonstrate a production defect or session disruption.
No publication, deployment, or business acceptance is recorded.

## Facts, inferences, and unresolved questions

- Facts: 44 tests pass; one baseline/candidate caller comparison passes; version `3.0.0` artifacts build.
- Inference: reviewed equivalent CES assignments can preserve the legacy permission map through explicit configuration.
- Unknown: live assigned-role endpoint support, synchronized account equivalence, data-role mappings, and deployed consumer compatibility.

## Findings

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| [Different supplied assignments](evidence/role-compatibility-design.md#sample-comparisons). | Full permission equivalence cannot be claimed. | unknown | Compare reviewed same-user assignments and allowed/denied actions. |
| [Consumer API mismatch](evidence/consumer-scope.md#confirmed-consumers-and-compatibility). | Historical static JWT callers may require source changes. | unknown | Compile actual consumers with artifact `3.0.0`. |
| [No live test](evidence/candidate-run-04/result.json). | Endpoint, trust, token refresh, and production behavior remain unverified. | unknown | Execute authorized consumer integration acceptance. |

## Sources

| Source | Locator | Authority and limit |
| --- | --- | --- |
| USER-IMPLEMENTATION | [Exact clarification](evidence/user-clarification-implementation.md). | User scope, version, token ownership, and tests. |
| SDK-BASE | [Baseline build](evidence/baseline-build-result.json). | Exact revision and Java 17 build evidence. |
| CES-SAMPLES | [Role comparison](evidence/role-compatibility-design.md). | Supplied static payloads; capture environment unknown. |

Final SDK commit: `fd9a157e260850b6d9efa10da3223950ea61133a`.
All forty recorded repository files match the [commit binding](evidence/final-commit-binding.json).
The SDK worktree is clean.

The [compiled API comparison](evidence/public-api-comparison.json) found no missing public members across 23 baseline classes.
This check covers the supplied baseline. It does not establish compatibility with historical SDK `1.1.1` artifacts.
