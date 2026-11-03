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

# Run migration and EMS2 environment coverage

> **Run all configured comparisons through one launcher. Complete population parity remains unassessed with the supplied captures.**
> Action: run the combined launcher and review the detailed [HTML](../evidence/coverage-runs/detailed-sample-20261103-v2/index.html) or [Markdown](../evidence/coverage-runs/detailed-sample-20261103-v2/index.md) sample.
> Consequence: unavailable users and inventories remain visible; mock results cannot establish current environment parity.
> Owner: unknown. Source: [detailed report request](../evidence/ems2-environment-coverage-20261103/detailed-report-user-input.md#exact-user-input).

## Sample reports

The sample uses the supplied API responses and production matrices. It does not acquire current environment data.

| Scope | Markdown | HTML |
| --- | --- | --- |
| Both comparisons | [Complete combined report](../evidence/coverage-runs/detailed-sample-20261103-v2/index.md) | [Interactive combined report](../evidence/coverage-runs/detailed-sample-20261103-v2/index.html) |
| EMS2 PROD to CES UAT | [Migration details](../evidence/coverage-runs/detailed-sample-20261103-v2/ems2-prod-to-ces-uat/report.md) | [Migration details](../evidence/coverage-runs/detailed-sample-20261103-v2/ems2-prod-to-ces-uat/report.html) |
| EMS2 PROD to EMS2 UAT | [Environment details](../evidence/coverage-runs/detailed-sample-20261103-v2/ems2-prod-to-ems2-uat/report.md) | [Environment details](../evidence/coverage-runs/detailed-sample-20261103-v2/ems2-prod-to-ems2-uat/report.html) |

The [validation record](../evidence/detailed-coverage-report-20261103/validation.json) binds actual checks and sample results to their source identities.
Unavailable accounts and inventories remain unassessed. A complete report does not establish complete migration coverage.
Both sample comparisons report `INCOMPLETE` because supplied captures cover only two comparable users per comparison.
The [sample verification](../evidence/detailed-coverage-report-20261103/sample-verification.json) checked 1,304 unique comparison tuples and 1,798 checkpoint hashes.

## Configure once

Start from the Workbench root. Use its installed Python environment; see [setup](../../../docs/SETUP.md) if `.venv` is absent.
The existing Workbench package supplies the required dependencies. No additional spreadsheet package is required.
Set `CES_COVERAGE_PYTHON` only when the launcher must use another Python executable with Workbench installed.

| Configuration | Comparison and scope |
| --- | --- |
| [suite.json](suite.json) | Run both comparison families and write one dashboard. |
| [config.json](config.json) | EMS2 PROD baseline against CES UAT; definitions, assignments, and functional permission content. |
| [ems2-config.json](ems2-config.json) | EMS2 PROD baseline against EMS2 UAT; subject and role inventories, assignments, and permission content. |

EMS2 role/entity/subject/action map to CES entitlement/application/feature/action in the migration configuration.
Optional `role_mapping`, `subject_mapping`, and `action_mapping` entries define confirmed name translations within each EMS2 entity.
Keep FMO Portal Admin `included: false`. Its unlaunched non-production exception stays outside production denominators.
The default `replay` mode reads supplied API response bodies and local matrices.
It needs no credentials, certificate file, or enterprise access. It does not construct HTTP clients or load private `.env` files.

## Run all coverage

1. On macOS, double-click [run-all-coverage.command](../run-all-coverage.command).
2. On Windows, double-click [run-all-coverage.cmd](../run-all-coverage.cmd).
3. Review `index.html` or `index.md`, then inspect each comparison's exact differences and evidence limits.

From the Workbench root, the equivalent macOS or Linux command is:

```sh
.venv/bin/python -m ai_sdlc_workbench.coverage_suite --config tasks/draft-ces-migration/coverage/suite.json --open
```

In Windows Command Prompt:

```bat
.venv\Scripts\python.exe -m ai_sdlc_workbench.coverage_suite --config tasks\draft-ces-migration\coverage\suite.json --open
```

The suite runs both comparisons even when one reports differences or incomplete source data.
It writes `index.html`, `index.md`, combined `result.json`, and separate result directories for each comparison.
Both combined formats contain the detailed comparison results. Individual reports remain available in each child directory.
The default mode is supplied-response replay. `--user-limit N` provides a bounded diagnostic run and preserves unassessed accounts.

## Run both checks

The original migration launcher runs entitlement and user checks for EMS2 PROD against CES UAT.
Use [run-coverage.command](../run-coverage.command) on macOS or [run-coverage.cmd](../run-coverage.cmd) on Windows.

```sh
.venv/bin/python -m ai_sdlc_workbench.entitlement_coverage --config tasks/draft-ces-migration/coverage/config.json --open
```

## Run EMS2 UAT versus PROD

Use [run-ems2-coverage.command](../run-ems2-coverage.command) on macOS or [run-ems2-coverage.cmd](../run-ems2-coverage.cmd) on Windows.

```sh
.venv/bin/python -m ai_sdlc_workbench.ems2_coverage --config tasks/draft-ces-migration/coverage/ems2-config.json --open
```

For either individual command on Windows, replace `.venv/bin/python` with `.venv\Scripts\python.exe`.
Windows Command Prompt accepts the remaining arguments as shown.

The saved comparison direction is PROD baseline to UAT target.
A missing item exists in PROD but is absent from UAT. An additional item exists only in UAT.
For the reverse UAT-to-PROD question, UAT-only items are absent from PROD.
The shared count stays the same. The reverse retention denominator is the UAT item count.
Compare entity, role, subject, and action names. Different numeric IDs between environments do not establish permission differences.
Separate role assignments, effective subject/action grants, and role-specific grants prevent equal permission unions from hiding role differences.
The same subject name under different entities remains a separate item.

## Read the output

Each new run writes a timestamped folder under `tasks/draft-ces-migration/evidence/coverage-runs/`.
The suite writes child directories named `ems2-prod-to-ces-uat` and `ems2-prod-to-ems2-uat`.

| File | Purpose |
| --- | --- |
| `index.html` | Complete suite report with both comparisons, interactive controls, and child evidence links. |
| `index.md` | Complete suite report in portable Markdown, with independent comparison denominators. |
| `report.html` | Individual report with readable inventory tables, user details, complete differences, and expandable matches. |
| `report.md` | The same comparison detail in Markdown, including matched supporting detail and unassessed accounts. |
| `result.json` | Complete metrics, matched content, differences, account outcomes, and source identities. |
| `differences.csv` | Missing, additional, inconsistent, and unassessed items. |
| `cases.jsonl` | Durable account checkpoints, saved as each comparison completes. |
| `responses/` | Retained response data with request identities and hashes. |
| `binding.json` | Configuration, implementation, matrix, and replay identities for individual-run recovery. |

Matched records remain in JSON and coverage totals. They also remain available in the report's supporting detail.
Detailed matches leave the active HTML and CSV difference views.
For CES comparisons, only explicit `excluded_features` separate administration scope. Unknown features and additional report permissions remain visible.

## Read each coverage layer

The reports keep the following measurements separate. Each percentage must retain its own denominator and completeness limit.

| Layer | What the report compares | Evidence limit |
| --- | --- | --- |
| Subject or feature inventory | Scoped names present in each environment or mapped catalog. | Matching names cannot establish matching actions. |
| Role or entitlement inventory | Scoped profile names present in each source. | Matching names cannot establish equal role definitions. |
| Permission definitions | Available role, entity/application, subject/feature, and action tuples. | Missing complete definitions remain unassessed. |
| Migration source consistency | EMS2 API inventory names against the supplied production matrix names. | This checks API-to-matrix consistency, separately from matrix-to-CES migration coverage. |
| User assignments | Roles attributed to the same account within the scoped entity or application. | EMS2 permission rows cannot reveal empty assigned roles. |
| User effective permissions | The union of available subject/feature and action grants for each account. | Equal unions can conceal different role assignments. |
| User role-specific grants | Permission tuples retaining the assigned role's identity. | Equal effective grants under different roles remain different profile content. |
| Data restrictions | Comparable field/value policy content. | Complete definitions are unavailable in the supplied captures. |
| Acquisition completeness | Assessed and unassessed accounts and inventories from the declared discovery scope. | Discovery sources do not prove a complete enterprise account directory. |

Every missing and additional item remains in a detail table. No difference list is truncated to a preview.
Every unassessed account remains listed with a source error or scheduling reason.
The HTML report supports search and expandable supporting details. The Markdown report includes equivalent retained content.
Source hashes, retained responses, checkpoints, and configuration bindings let reviewers trace counts to the supplied evidence.
Report generation does not alter profile assignments or entitlement definitions.

| Exit code | Meaning |
| --- | --- |
| `0` | Functional comparisons agree within the declared scope. Full data-profile equality still requires comparable definitions. |
| `1` | Comparisons completed and contain differences. |
| `2` | Comparison is incomplete, or setup failed. Missing captures commonly cause this result in mock mode. |

The suite gives incomplete results priority over differences when it selects its aggregate exit code.
A completed script with exit code `2` can still produce valid partial reports.

## Recover an individual run

Use `--resume` with the individual runner and its retained child directory:

```sh
.venv/bin/python -m ai_sdlc_workbench.ems2_coverage --config tasks/draft-ces-migration/coverage/ems2-config.json --resume tasks/draft-ces-migration/evidence/coverage-runs/RUN-DIRECTORY/ems2-prod-to-ems2-uat --open
```

Replace `RUN-DIRECTORY` with the actual suite folder. Use `entitlement_coverage` and its matching configuration for the CES child.
Recovery requires unchanged configuration, implementation, matrices, execution mode, and applicable replay source hashes.
Changed bindings require a new run. Re-running the suite starts a new suite run.

## Interpret the scope

The migration comparator discovers accounts from production matrices and CES catalog memberships.
The EMS2 environment comparator discovers accounts from included matrices and scoped request examples from both EMS2 environments.
The EMS2 environment configuration can declare additional accounts. Neither discovery route proves a complete account directory.
No complete EMS2 account-directory endpoint was supplied. Undiscovered accounts remain outside demonstrated discovery coverage.

Replay verifies only supplied captures. Missing or invalid responses remain unassessed; the runner does not invent permission responses.
Final complete-profile coverage remains `null` while required account assessment is incomplete.
Subject and role inventory coverage also remain incomplete when their required environment responses are unavailable.
The supplied EMS2 examples contain `X_RATANONE` role inventories and subject inventories for the other two included entities.
The other requested inventories lack captures. The service-account UAT example also has mismatched request context and remains unassessed.
EMS2 assignments come from permission rows. Empty roles and complete data field/value policies require separate authoritative definitions.
No missing PROD names were found in the assessed UAT inventories. UAT still has four additional roles and one additional subject.
These name-level findings do not establish complete role-to-subject-to-action equality or a difference limited to users.
Captured timestamps do not establish an atomic synchronization snapshot across environments.

The [source contracts](../evidence/ems2-environment-coverage-20261103/contracts.json) and [validation](../evidence/ems2-environment-coverage-20261103/validation.json) identify exact supplied evidence and execution limits.
The [earlier migration mock report](../evidence/coverage-runs/mock-supplied-20261103/report.html) retains its original source binding.

## Explicit live mode

Use live mode only from an environment with approved endpoint access. This session verifies supplied mocks only.
Prepare private values in the ignored Workbench root `.env`, or export process environment variables.
Process values override `.env` values, including explicit empty values.

```dotenv
CES_COVERAGE_BEARER_TOKEN=your-CES-token
CES_COVERAGE_EMS2_TOKEN=your-EMS2-PROD-token-if-required
EMS2_COVERAGE_PROD_TOKEN=your-EMS2-PROD-token-if-required
EMS2_COVERAGE_UAT_TOKEN=your-EMS2-UAT-token-if-required
CES_COVERAGE_CA_FILE=/absolute/path/to/trusted-enterprise-ca.pem
```

The two comparators use separate EMS2 token references. A configured optional token can remain unset when its endpoint allows this.
Custom CA configuration is optional when the system trust store already trusts the endpoint chain.
Relative CA paths resolve from the Workbench root. TLS certificate verification remains enabled.
Keep credentials outside configuration files and source control. Supplied request headers are not reused as live credentials.

```sh
.venv/bin/python -m ai_sdlc_workbench.coverage_suite --config tasks/draft-ces-migration/coverage/suite.json --mode live --open
```

An individual runner also accepts `--mode live`. Each runner recalculates its declared account population and fetches every scheduled account.
Global authorization, network, or TLS failures stop further scheduling and leave the remaining accounts unassessed.
Complete comparison still requires a complete account population and comparable data definitions.
The [historical TLS preflight](../evidence/coverage-runs/live-access-check-unsandboxed/result.json) does not verify current connectivity.
