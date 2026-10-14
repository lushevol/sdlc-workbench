---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
- Automated checks do not check the complete approved dictionary or grammar rules.
---

# SDK and E2E repository registration

Review date: 14 October 2026.
Workbench baseline: `aaf6ff4`.
Scope: Two independent source baselines, catalog relationships, candidate contracts, and retained evidence.
Risk: Low for Workbench execution because this stage changes metadata and knowledge records only.

The [user request](../knowledge/raw/2026-10-14-sdk-e2e-registration/user-request.txt) authorizes initialization and contract registration.
Both supplied copies now have independent Git metadata on `codex/initial-baseline`.
Original repository history remains unavailable.

| Repository ID | Initial commit | Tracked files |
| --- | --- | --- |
| `single-ui-auth-sdk` | `b0aa82005e7f14202f85f5ef583f25e42da9eeb3` | 27 |
| `ratan-test-engine` | `432f898f59fb06414bc14152d6e463a6a1f4eac2` | 1793 |

The SDK source directory is `repos/libraries/single-ui-sdk-starter`.
Its Maven module is `com.scb.fmoportal:fmoportal-auth-sdk:2.0.0-SNAPSHOT`.
The test engine source directory is `repos/testing/ratan-test-engine`.
Ignored local configuration maps both portable repository IDs to these paths.

The [baseline inventory](../knowledge/raw/2026-10-14-sdk-e2e-registration/initial-baselines.json) records the source identities and limits.
Local Git exclusions omit generated reports, dependencies, environment files, and credential containers.
Source bytes remain unchanged.

The engine's [commit convention](../knowledge/raw/2026-10-14-sdk-e2e-registration/ratan-test-engine/CLAUDE.md.L264-L270.snapshot) requires an Azure DevOps work item ID.
The user supplied no work item ID for this initial import.
The initial commit uses `Initialize supplied source baseline` under the explicit initialization request.
No work item ID or original source history was invented.

## Catalog and contract changes

The catalogs now contain five repositories, two services, five capabilities, sixteen candidate contracts, and five technical sources.
The SDK has type `library`; the engine has type `testing`.
Their roles do not identify additional business services.

| Repository | New candidate contracts |
| --- | --- |
| SDK | Spring configuration, JWT validation, request context, EMS2 entitlement lookup |
| Test engine | Robot execution inputs, Excel generation, result export, keyword MCP |

The existing SSO contract now links SDK token consumption and Robot login consumption.
SDK consumption covers token format and does not imply calls to every SSO endpoint.
The authentication capability includes both repositories through those source declarations.
The E2E support capability groups suite definitions, generation, discovery, and export.

The [architecture candidate](../knowledge/candidates/ARCH-sdk-e2e-contracts.md) records the interfaces, evidence, and unresolved questions.
Thirty-two new business snapshots retain bytes from exact commits.
Two additional snapshots retain the request and baseline inventory.
The existing BFF constant snapshot supplies an unchanged source reference.
Earlier snapshots, manifest records, candidates, findings, and audit events remain available.

## Findings and evidence limits

The [SDK finding](../knowledge/findings/FND-sdk-authorization-enforcement.md) separates authentication and entitlement lookup from endpoint permission enforcement.
The filter validates tokens and sets one serialized JSON `userInfo` request attribute.
A configured skip header bypasses validation when its incoming request value is nonempty.
URL exclusions also bypass validation.
Its logout rejection list remains local to the filter instance.
No downstream SDK consumer or permission enforcement result was established.

The [export finding](../knowledge/findings/FND-ratan-skipped-result-status.md) records that Robot `SKIP` becomes exported `PASSED`.
This mapping prevents exported status alone from proving passing assertions.
Source assertions establish test intent; retained executions must establish observed results.
Business tests, SDK builds, generation scripts, and MCP startup were not executed.

Owner: unknown.
Next action: identify downstream permission checks and review Robot XML results before claiming verified behavior.
All sixteen contracts remain candidates with unresolved documentation gaps.
No executable tools or operation grants were added.

## Stage acceptance

```gherkin
Scenario: Register the SDK and E2E source baselines
  Given two supplied copies selected as initial repositories
  When independent initial commits and candidate contracts are registered
  Then both Git roots resolve to their own source directories
  And all sixteen contract source paths resolve at exact commit IDs
  And all thirty-two new business snapshots match committed source bytes
  And all sixteen contracts retain candidate status
  And a generated starter workspace contains no live repository records
```

## Validation

| Check | Result |
| --- | --- |
| Workbench catalog tests | PASSED: 11 tests. |
| Source workspace validation | VALID: five governed documents and zero structural findings. |
| Independent source roots and exact contract revisions | PASSED: five clean roots and sixteen source paths. |
| New source bytes and retained history | PASSED: thirty-two business snapshots match commits; earlier evidence remains unchanged. |
| Starter workspace isolation | PASSED: six empty catalogs and an empty raw manifest. |
| Local links and automated prose limits | PASSED. Complete ASD review remains pending. |

The [stage checks](evidence/sdk-e2e-registration-checks.json) retain the observed results and evidence limits.
The [workspace validation](evidence/sdk-e2e-workspace-validation.json) retains the final structural result.
Checks used macOS and Python 3.14.5.
ASD writing review remains pending.
