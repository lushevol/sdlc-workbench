---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Read-only data connectors

**Live access remains unverified. Owner: workspace operator. Configure endpoints, allowed log indices, and restricted credentials before live analysis. [Evidence](verification-manifest.json).**

Local verification passed: 753 Python tests and 39 connector tests. Both suites recorded zero failures and zero skips.
Connected and prepared-cache npm installations passed. Wheel installation and generated workspace checks also passed.

## Authority and scope

The [user request](user-input.md#exact-user-input) defines this maintenance scope and its read-only boundary.
This change adds Workbench tools. It does not change business rules or domain knowledge.

Baseline `8b949bb9939d402fbc7d697e9b8bfd3b56688fcf` has neither connector in its provider allowlist or native server.
The candidate adds Kibana log analysis and PostgreSQL schema inspection and data analysis.
Unrelated worktree changes were preserved. Exact candidate files are identified in the [verification manifest](verification-manifest.json).

## Affected paths and risk

The [Python provider](../../../core/providers/connectors.py) invokes the [Node bridge](../../../core/connectors/workbench/bridge.js) after exact grants.
The bridge reads selected-workspace settings and registers connector tools.
Catalog examples, initialization assets, doctor checks, and offline installation consume these interfaces.
The [integration guide](../../CONNECTORS.md) documents those consumers and their access limits.

Qualitative risk is moderate because these tools access logs and a primary database.
Kibana exposes fixed mapping and search operations through Console proxy requests.
PostgreSQL uses restricted credentials, read-only transactions, and bounded analysis queries.
No application database or company Kibana endpoint was used during local verification.

## Behavior coverage

The denominator contains four bounded acceptance scenarios from the [connector guide](../../CONNECTORS.md#acceptance-criteria).
All four have inspected assertions, implementation links, and passing local execution evidence.
These links do not establish complete KQL compatibility or production conformance.

### Acceptance criteria to test assertions

| Acceptance scenario | Inspected assertions | Execution |
| --- | --- | --- |
| [Kibana Console analysis](../../CONNECTORS.md#kibana-console-log-analysis) | [Mapping, KQL semantics, routing, and explanations](../../../core/connectors/workbench/kibana.test.js#L36); [actual bridge](../../../core/connectors/workbench/bridge.test.js#L204). | [39 passing connector tests](node-tests-final.log). |
| [Kibana query rejection](../../CONNECTORS.md#kibana-query-rejection) | [Invalid arguments and unsupported fields](../../../core/connectors/workbench/kibana.test.js#L101); [sanitized bridge errors](../../../core/connectors/workbench/bridge.test.js#L204). | [Connector execution](node-tests-final.log). |
| [PostgreSQL bounded analysis](../../CONNECTORS.md#postgresql-bounded-analysis) | [Transactions, parameters, and row caps](../../../core/connectors/workbench/postgresql.test.js#L32); [real database fixture](../../../core/connectors/workbench/postgresql.test.js#L109). | [PostgreSQL execution and source identity](postgresql-integration.json). |
| [PostgreSQL mutation rejection](../../CONNECTORS.md#postgresql-mutation-rejection) | [Invalid commands](../../../core/connectors/workbench/postgresql.test.js#L63); [persistent write and escape denial](../../../core/connectors/workbench/postgresql.test.js#L109). | [Original database results](postgresql-integration.log). |

Assertion and local passing-execution coverage: 4/4 scenarios.
No measured line-coverage percentage or complete business conformance percentage is claimed.

### Acceptance criteria to changed code

| Acceptance scenario | Changed implementation | Limits |
| --- | --- | --- |
| [Kibana Console analysis](../../CONNECTORS.md#kibana-console-log-analysis) | [Kibana reader and KQL compiler](../../../core/connectors/workbench/kibana.js). | Supports the documented KQL subset only. |
| [Kibana query rejection](../../CONNECTORS.md#kibana-query-rejection) | [Strict schemas and mapping checks](../../../core/connectors/workbench/kibana.js); [safe error messages](../../../core/connectors/workbench/bridge.js). | Unknown syntax fails explicitly. |
| [PostgreSQL bounded analysis](../../CONNECTORS.md#postgresql-bounded-analysis) | [Read-only query execution](../../../core/connectors/workbench/postgresql.js). | Role privileges and reachable production services remain unverified. |
| [PostgreSQL mutation rejection](../../CONNECTORS.md#postgresql-mutation-rejection) | [SQL guard, extended protocol, and rollback](../../../core/connectors/workbench/postgresql.js). | Database owners must restrict unsafe function execution. |

Implementation-link coverage: 4/4 scenarios. Deployed behavior remains unverified for all four.

### Changed code to test assertions

| Changed unit | Classification | Assertions and evidence |
| --- | --- | --- |
| Kibana reader and compiler | Required behavior | [Kibana assertions](../../../core/connectors/workbench/kibana.test.js); [connector execution](node-tests-final.log). |
| PostgreSQL query executor | Required behavior | [Database assertions](../../../core/connectors/workbench/postgresql.test.js); [real execution](postgresql-integration.log). |
| Provider, registration, configuration, catalogs, and bridge | Supporting integration | [Configuration assertions](../../../core/connectors/workbench/config.test.js); [provider assertions](../../../tests/test_connector_provider.py#L263); [Python execution](python-tests.log). |
| Doctor configuration checks | Supporting maintenance | [Readiness assertions](../../../tests/test_doctor.py#L135); [final focused execution](doctor-tests-final.log). |
| Driver manifest and lockfile | Supporting maintenance | [Fresh connected and offline installations](installation-checks.json). |
| Guides, examples, environment template, and shipped skill | Supporting maintenance | [Document checks](document-checks.json); [wheel workspace assertions](wheel-installation.json). |

Changed-unit assertion coverage: 6/6 groups. Tests and retained evidence support these groups without adding business behavior.

## Verification and evidence index

| Check | Result | Evidence |
| --- | --- | --- |
| Complete Python suite with native connector integration | 753 passed; zero failures, errors, or skips. | [Original execution](python-tests.log). |
| Complete connector suite | 39 passed; zero failures, errors, or skips. | [Final execution](node-tests-final.log). |
| PostgreSQL 18.4 fixture | Reads pass; writes and transaction escapes fail; table remains unchanged. | [Environment and hashes](postgresql-integration.json); [results](postgresql-integration.log). |
| CLI discovery | Both resources expose exactly their granted read tools. | [Kibana](kibana-discovery.json); [PostgreSQL](postgresql-discovery.json). |
| Root npm installation | Fresh offline and connected installations pass with `pg@8.16.3`. | [Installation assertions](installation-checks.json); [log](installation-checks.log). |
| Wheel build | Passed with installed `setuptools==84.0.0` and build isolation disabled. | [Successful build](wheel-build-final.log). |
| Wheel installation and initialization | Installed runtime creates a valid workspace with empty catalogs and shipped connector resources. | [Artifact assertions](wheel-installation.json). |
| Source workspace validation | `VALID`; zero findings. | [Validation](workspace-validation.json). |
| Documentation and diff | Local links and authored whitespace pass. Original pip output retains two whitespace-only lines. | [Document checks](document-checks.json); [scoped diff check](diff-checks.json). |

The default isolated wheel build could not reach its build dependency inside the sandbox.
The [original failure](wheel-build.log) remains preserved. The successful build used the existing compatible build dependency.
Initial PostgreSQL sandbox and incomplete-cache results remain in the [database log](postgresql-integration-initial.log) and [cache check](installation-checks-initial.json).
Those environment failures do not establish product defects.

## Remaining limits and actions

| Limit and evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| [No company endpoint execution](verification-manifest.json). | Live routing, authentication, and deployed Console compatibility remain unverified. | Workspace operator | Configure private settings and run an authorized mapping read and bounded database read. |
| [Supported KQL subset](../../CONNECTORS.md#analyze-elasticsearch-logs-through-kibana). | Nested queries, value lists, field wildcards, and other unsupported syntax fail. | Connector maintainer | Extend supported syntax only when a required query supplies evidence and tests. |
| [Function privilege boundary](../../CONNECTORS.md#analyze-postgresql-data). | Read-only transactions do not sandbox external side effects from unsafe functions. | Database owner; identity unknown | Restrict role memberships, ownership, unsafe extension access, and function execution privileges. |
| [Buffered database rows](../../DEPENDENCIES.md#read-only-data-analysis-connectors). | A single large value can consume memory before response rejection. | Workspace operator | Select narrow columns and bounded values for primary database analysis. |
| [Platform and TLS limits](postgresql-integration.json). | Native Windows and live database TLS remain unverified. | Deployment operator; identity unknown | Check the required target platform and trusted certificate before use. |

Missing connector variables were merged into ignored `.env`. Existing values were preserved.
No credential value was stored in tracked catalogs or retained verification output.
