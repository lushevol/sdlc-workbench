---
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
    - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Run coverage inside the internal network

> **Run the existing suite with `--mode live` on the internal machine. Reports are generated locally.**
> Action: install the core, check endpoint configuration, supply credentials, and run the commands below.
> Consequence: inaccessible endpoints and missing definitions remain unassessed.
> Owner: internal operator, identity unknown.
> Source: [user question](../evidence/internal-network-run-guide-20261103/user-input.md#exact-user-input).

These instructions cover EMS2 PROD versus CES UAT and EMS2 PROD versus EMS2 UAT.
The [SDK verification steps](#6-verify-the-java-sdk-path) also cover the actual Java client and consuming application.
Source: [SDK network-verification question](../evidence/sdk-company-network-20261104/user-input.md#exact-user-input), 4 November 2026.
This guide does not record enterprise execution. The retained sample uses supplied responses.

## 1. Transfer and install

Use a complete copy of this Workbench source checkout on the internal machine.
Preserve the task folder, including `coverage/`, `api/`, `ces migration/`, and the launchers.
The installed Python wheel does not contain those task inputs.
The EMS2 environment comparison reads stored API request keys during account discovery, including live runs.

Install approved Python 3.10 or later, with compatible dependency wheels available for that interpreter.
Select the same interpreter when preparing dependencies and installing them.
Node.js and a report server are unnecessary for these coverage commands.
Create the Python environment on the target computer. Do not copy `.venv` between computers.

If the internal machine can reach an approved Python package index, run core setup from the Workbench root:

| System | Install | Check installation |
| --- | --- | --- |
| Windows PowerShell | `.\setup.cmd --core-only` | `.\setup.cmd --check --core-only` |
| macOS | `./setup.command --core-only` | `./setup.command --check --core-only` |

If package registries are unavailable, prepare a core bundle on a connected staging computer:

| System | Prepare on staging computer | Install on internal computer |
| --- | --- | --- |
| Windows PowerShell | `py -3 core\offline.py prepare --output offline-bundle --core-only` | `.\setup.cmd --core-only --offline-bundle .\offline-bundle` |
| macOS | `python3 core/offline.py prepare --output offline-bundle --core-only` | `./setup.command --core-only --offline-bundle ./offline-bundle` |

The staging and target computers must match operating system, CPU architecture, Python minor version, interpreter implementation, and ABI.
Transfer the unchanged source checkout and `offline-bundle/` together through the approved company process.
Do not transfer `.env`, `.venv`, `node_modules`, or private package-manager settings.
See the [offline setup contract](../../../docs/SETUP.md#install-without-package-registry-access) for target checks and bundle validation.

## 2. Check endpoint configuration

Check the endpoint addresses and entity identifiers against the internal environment.
Keep FMO Portal Admin excluded from production denominators.

| File | Fields to check |
| --- | --- |
| [config.json](config.json) | `ems2.base_url`, `ces.base_url`, request paths, EMS2 entity IDs, CES application routing, matrix paths. |
| [ems2-config.json](ems2-config.json) | `prod.base_url`, `uat.base_url`, request paths, each entity's `prod_id` and `uat_id`. |
| [suite.json](suite.json) | Both child configurations and the output location. |

The current configurations target EMS2 PROD, EMS2 UAT, and CES UAT.
Environment-specific numeric identifiers locate requests. Names define comparison identity.
The default request timeout is 15 seconds, with one retry and four account workers.
Adjust these configuration values to the internal service limits when required.

The internal host needs DNS and HTTPS access to all configured endpoints.
Allow GET for CES and inventory requests. Allow JSON POST for the EMS2 `entitlementList` read operation.

## 3. Create private configuration

Create `.env` at the Workbench root, beside `setup.cmd` and `setup.command`.
Use valid API credentials supplied through your internal access process.

```dotenv
CES_COVERAGE_BEARER_TOKEN=replace-with-CES-UAT-token
CES_COVERAGE_EMS2_TOKEN=replace-with-EMS2-PROD-token-if-required
EMS2_COVERAGE_PROD_TOKEN=replace-with-EMS2-PROD-token-if-required
EMS2_COVERAGE_UAT_TOKEN=replace-with-EMS2-UAT-token-if-required
CES_COVERAGE_CA_FILE=C:/Company/Certificates/enterprise-ca.pem
```

On macOS, use the corresponding local certificate path.
Omit `CES_COVERAGE_CA_FILE` when Python already trusts every endpoint certificate chain.
A relative CA path resolves from the Workbench root. TLS certificate verification remains enabled.
The shared CA bundle must trust all three endpoints when supplied.

Both PROD token variables can contain the same token when they access the same service.
EMS2 tokens can remain unset only when those endpoints permit requests without an authorization header.
CES requires its configured token. Raw tokens receive the `Bearer` prefix automatically.
Explicit `Bearer ...` and `Basic ...` authorization values are also supported.
An existing browser login does not supply credentials to this runner.
Browser SSO cookies, Kerberos, NTLM, client certificate configuration, and redirects are not supported by this client.

If your network requires a proxy, configure `HTTPS_PROXY` and the appropriate `NO_PROXY` host list.
`HTTP_PROXY` and lowercase forms are also supported.
Process environment variables override `.env`, including explicit empty values.
Keep credential values outside JSON configurations and source control.

## 4. Run both comparisons

Run commands from the Workbench root.
Start with a bounded live run to check account collection and report generation.
The bound limits scheduled accounts per comparison. Catalog and inventory requests still run.
Its account selection follows each comparator's discovery order; the two samples can contain different accounts.

Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe -m ai_sdlc_workbench.coverage_suite --config tasks/draft-ces-migration/coverage/suite.json --mode live --user-limit 2 --open
```

macOS or Linux, using an installed environment:

```sh
.venv/bin/python -m ai_sdlc_workbench.coverage_suite --config tasks/draft-ces-migration/coverage/suite.json --mode live --user-limit 2 --open
```

Check each report's evidence source. It must say `LIVE: collected API responses`.
Check source errors and account outcomes. A bounded run can report `INCOMPLETE` because accounts remain unscheduled.
Then remove `--user-limit 2` to compare the complete discovered population:

Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe -m ai_sdlc_workbench.coverage_suite --config tasks/draft-ces-migration/coverage/suite.json --mode live --open
```

macOS or Linux:

```sh
.venv/bin/python -m ai_sdlc_workbench.coverage_suite --config tasks/draft-ces-migration/coverage/suite.json --mode live --open
```

Alternatively, pass `--mode live` to the existing launcher from a terminal:

| System | Run all live comparisons |
| --- | --- |
| Windows PowerShell | `.\tasks\draft-ces-migration\run-all-coverage.cmd --mode live` |
| macOS | `./tasks/draft-ces-migration/run-all-coverage.command --mode live` |

Double-clicking these launchers without arguments still runs supplied-response replay.
On a server without a desktop, use the Python command and omit `--open`.
Keep API calls on the internal host. Open the generated files on an internal desktop when needed.

## 5. Read and retain the reports

Each run creates a timestamped directory under `tasks/draft-ces-migration/evidence/coverage-runs/`.
The terminal prints the actual Markdown and HTML paths.

| Output | Content |
| --- | --- |
| `index.html` and `index.md` | Both complete comparisons, with separate populations and denominators. |
| Child `report.html` and `report.md` | Detailed entitlements, assignments, permissions, role grants, matches, and unassessed accounts. |
| Child `differences.csv` | Exact missing, additional, inconsistent, and unassessed items. |
| `result.json`, `binding.json`, `cases.jsonl`, and `responses/` | Metrics, source identities, durable account checkpoints, and retained response evidence. |

HTML reports contain their styles and scripts. They need no public CDN or web server.
Retain the complete run directory when moving or sharing the report internally, so relative evidence links continue to work.

| Exit code | Meaning |
| --- | --- |
| `0` | Functional comparisons match within the declared scope. |
| `1` | Completed comparisons contain differences. |
| `2` | At least one comparison is incomplete, or setup failed. |

Network, TLS, or authorization failures can stop further account scheduling. The remaining accounts stay unassessed.
Review `MISSING_CREDENTIAL`, HTTP 401/403, `TLS_ERROR`, `TLS_CONFIGURATION`, or `NETWORK_ERROR` before another run.
Check [individual-run recovery](README.md#recover-an-individual-run) when continuing a retained child run.
Repeat `--mode live` when resuming a live child. The suite itself has no `--resume` option.
Recovery reuses successful captures. Start a new run for fresh acceptance evidence.

## 6. Verify the Java SDK path

> **The live comparator does not execute the SDK.**
> Action: verify the assigned-role endpoint and run the actual SDK inside a consuming application.
> Consequence: a matching comparator report alone cannot close SDK compatibility gaps.
> Owner: application and CES operators, identities unknown.
> Evidence: [SDK review](../10-change-review-sdk-function-coverage.md#current-task-state) and [current user question](../evidence/sdk-company-network-20261104/user-input.md#exact-user-input).

### Build the reviewed candidate

Use the SDK checkout at `fd9a157e260850b6d9efa10da3223950ea61133a`.
First inspect its revision and worktree. Preserve local changes before selecting another revision.
The [SDK setup guide](../../../repos/libraries/single-ui-sdk-starter/docs/SETUP.md#connected-build) explains JDK 17, Maven, artifact access, and consumer installation.
Run these commands from the SDK repository root:

```sh
git rev-parse HEAD
java -version
mvn -version
mvn -Dformatter.skip=true clean verify
```

The reviewed candidate has 44 tests across five classes. Require zero failures, errors, and skips.
Retain the actual count and revision if another candidate adds tests.
Inspect `single-ui-sdk-starter/target/surefire-reports/` and retain the complete build result.
These tests use mock CES responses. Running them inside the company network does not make them live tests.
Use the artifact installation instructions before compiling the real consumer against SDK `3.0.0`.
Historical `1.1.1` consumers require an API compatibility check, including instance-based `JwtTokenUtil` usage.

### Check the SDK endpoint

Use your internal API client and the caller's valid CES FMAA service token.
Configure the application JVM to trust the approved enterprise certificate chain.
The Python comparator's `CES_COVERAGE_CA_FILE` does not configure JVM trust.
Request each selected account through the exact configured CES origin:

```http
GET /fmces/v1/entitlement/user/<user-id>
Authorization: Bearer <caller-FMAA-token>
```

The expected response is an array of assigned-role objects.
Each selected role needs `appId`, `appName`, `entitlementName`, and `featureActionDtos`.
Each grant needs `features.featureName` and `actions.actionName`.
Validate the selected application's identifiers against the approved environment configuration.
Retain the response, environment, capture time, status, and request correlation. Exclude credential values.

The existing comparator uses `/fmces/v1/entitlement/app/51358/{app}/user/{user}` and application catalogs.
Those response shapes differ from the SDK assigned-role contract.
If the assigned-role route is unavailable, record that result and resolve its supported contract with the CES owner.
Changing the SDK endpoint property alone cannot adapt an aggregate response.

### Configure all required legacy scopes

The consuming application supplies its CES origin, entity mappings, and `FmaaTokenProvider`.
The comparator's Workbench `.env` does not configure the Spring SDK automatically.
The SDK explicit overload accepts a raw token without the `Bearer ` prefix.
The existing one-argument method needs the caller token-provider bean.
Without that provider, it returns an empty map without a CES request.

Review each required legacy entity separately:

| Legacy entity | Required mapping check |
| --- | --- |
| `X_RATANONE` | Preserve each approved functional role and its own subject/action grants. |
| `RATAN_DATA_ENTITLEMENT` | Preserve the approved data-role key and marker without routing it under `X_RATANONE`. |
| `RATAN_FUNC` | Preserve approved system roles and functional subjects for service accounts. |

The [three-account mapping example](../evidence/sdk-function-coverage-20261104/api-parity.md#configuration-needed-for-the-matched-sample-scope) is a proposal for supplied samples.
Expand it from reviewed assignments before comparing the complete population.
Role allowlists and feature scopes must prevent unrelated grants from crossing legacy entity boundaries.
A matching data-role marker does not establish equal resolved data restrictions.

### Invoke the real SDK and compare outputs

Use an integration test or existing consuming application running inside the company network.
Inject the actual SDK `AuthorizationService` and its configured transport. Do not substitute `MockRestServiceServer` for this check.
The SDK supplies no standalone live-verification launcher.
The following fragment shows the required invocation and assertion inside that application test:

```java
Map<String, Object> actual = authorizationService.getEntitlements(userId, fmaaToken);
assertEquals(expectedLegacyMap, actual);
```

`userId`, `fmaaToken`, and `expectedLegacyMap` come from the application's test setup.
The expected map must come from the matched baseline and reviewed mapping for that account.
It must preserve `entity:role -> subject -> actions` and applicable empty roles.
Use the explicit-token overload during diagnosis so service failures remain distinguishable from valid empty assignments.
Also exercise the application's normal one-argument path when it uses `FmaaTokenProvider`.

Start with the supplied accounts `1289935`, `1481696`, and `srv.ratan.001`, subject to current approved test access.
Their historical permission examples are in the [API comparison](../evidence/sdk-function-coverage-20261104/api-parity.json).
Historical samples establish comparison inputs, not today's expected account policy.
Retain expected and actual maps and each exact difference.
Then expand to every account in the declared migration population.

Use the [canonical SDK cases](../../single-ui-sdk-ces-migration-20261101/06-test-cases.md#procedure-and-assertions) as the predicate definitions.
Record live results separately from their existing controlled executions.

| Canonical predicate | Required company-network observation |
| --- | --- |
| [Role map](../../single-ui-sdk-ces-migration-20261101/06-test-cases.md#sdk-tc-001) and [paired compatibility](../../single-ui-sdk-ces-migration-20261101/06-test-cases.md#sdk-tc-008) | Compare complete role/subject/action maps under equivalent account scope. Keep unexplained differences visible. |
| [Scope isolation](../../single-ui-sdk-ces-migration-20261101/06-test-cases.md#sdk-tc-002) | An allowed action remains allowed. An unassigned or excluded action remains absent. No grant crosses roles or entities. |
| [Token and CES-only request](../../single-ui-sdk-ces-migration-20261101/06-test-cases.md#sdk-tc-003) | A correlated SDK lookup reaches CES with the caller token and makes zero EMS2 requests through that lookup. |
| [Empty assignments](../../single-ui-sdk-ces-migration-20261101/06-test-cases.md#sdk-tc-005) | A confirmed empty account produces an empty result without a hidden upstream failure. |
| [Failure classification](../../single-ui-sdk-ces-migration-20261101/06-test-cases.md#sdk-tc-006) | A controlled invalid-token request produces a classified failure and no grants. Keep synthetic timeout tests separate. |
| [JWT validation](../../single-ui-sdk-ces-migration-20261101/06-test-cases.md#sdk-tc-009), [entitlement tokens](../../single-ui-sdk-ces-migration-20261101/06-test-cases.md#sdk-tc-010), and [filter attributes](../../single-ui-sdk-ces-migration-20261101/06-test-cases.md#sdk-tc-011) | The real consumer preserves its authentication and request-context contracts. |
| [Spring wiring](../../single-ui-sdk-ces-migration-20261101/06-test-cases.md#sdk-tc-012) | The actual consumer resolves SDK `3.0.0`, starts, and invokes its configured caller token provider. |

Exercise allowed and denied operations through the actual consumer after comparing its map.
A returned map alone does not prove that the application enforces each permission correctly.
Verify caller token renewal across successive lookups when assessing operational acceptance.
The current SDK tests omit logout/replay and effective timeout assertions. Those checks remain separate open coverage items.

### Retain evidence and decide the result

Save results immediately under the owning task's `evidence/` directory on the company machine.
Retain the comparator's complete run directory. Keep SDK results in the same investigation scope.
Record SDK and consumer revisions, artifact hashes, effective mapping hashes, environment, times, accounts, assertions, and actual outcomes.
Use remote UAT logs to bind the tested build and request correlations to observed service behavior.
Keep tokens, authorization headers, and private credential configuration outside retained reports.

Require zero missing and unsupported extra permissions within the declared complete comparison scope.
Keep role assignments, effective grants, role-specific grants, and data restrictions as separate results.
A failed request, unknown account population, or unresolved policy remains unassessed or open.
Do not count those items as matching permissions.
Internal execution has not occurred in this chat. These instructions define the evidence to collect.

## Evidence limits

Live mode replaces supplied response bodies with current API collection. It does not add missing endpoint contracts.
Discovery uses matrices, CES memberships where applicable, configured users, and stored EMS2 request keys.
It cannot prove a complete enterprise account directory.
The EMS2 comparison supports an explicit `users` array in [ems2-config.json](ems2-config.json) for additional known accounts.
Complete role definitions, empty assigned roles, and full data-policy equality still require authoritative comparable sources.
The runner does not add pagination beyond the supplied contracts.
Captured requests do not establish an atomic snapshot across environments.
Read inventory presence, definition retention, user equality, and acquisition completeness as separate measurements.

## Verification

The [SDK guide checks](../evidence/sdk-company-network-20261104/validation.json) cover links, command options, and exact source identities.
They do not establish successful company-network execution.

The [guide validation](../evidence/internal-network-run-guide-20261103/validation.json) records source inspection and local command checks.
Those checks do not establish internal installation, endpoint connectivity, or live comparison success.
Windows commands were inspected but not executed on a Windows host.
The [reporting validation](../evidence/detailed-coverage-report-20261103/validation.json) retains the earlier tooling test and sample evidence.
