# Workbench capability and dependency review

**Core is locally ready. Optional integrations need configuration and separate live verification before use.**

Owner: Workbench maintainer and selected integration owners.
Next action: select required integrations and address their [readiness gaps](#local-readiness-and-findings).
The [verification summary](verification-summary.json) records passing local checks and their limits.

## Scope and reference

[The user input](user-input.md) is the high-priority source for this review.
Review date: 3 November 2026, Asia/Singapore.
Source revision: `c9cb8ac3ecad4816b8b9c97e2515f6cc4d3ee834`.
This review covers Workbench capabilities, dependency consumers, local checks, and installation boundaries.
Business repository execution is outside scope.
Unrelated README edits, staged task assets, and untracked `core/release-report/` files remain outside the reviewed candidate.
No runtime source, dependency, grant, or private configuration was changed.
Change risk is low because this stage adds review documents and retained evidence.

## Critical dependency summary

| Dependency | Workflow and consequence | Evidence state | Owner and next action |
| --- | --- | --- | --- |
| Python and five core packages | Required for installed core commands. Local requirements are satisfied. | [Observed declarations](../../../pyproject.toml#L1-L16); [local check](pip-check.log) | Workbench maintainer: preserve tested versions and platform compatibility. |
| Node and npm | Required for optional native connectors and release collection. They are available locally. | [Manifest](../../../package.json); [doctor](doctor.json) | Workbench maintainer: use supported Node versions and the root lockfile. |
| Private endpoints, credentials, and grants | Selected integrations remain unavailable until their prerequisites are satisfied. | [Local readiness](doctor.json); live access unknown | Integration owners: configure selected features and verify bounded access. |
| Release Clinic Python extra | Local `extract-msg` is missing. Full Clinic readiness remains incomplete. | [Declared extra](../../../pyproject.toml#L18-L32); [doctor](doctor.json) | Workbench maintainer: install the approved extra when Clinic is required. |
| Company certificates and optional browser isolation | Some optional clients disable certificate checks or browser sandboxing. | [Existing dependency analysis](../../../docs/DEPENDENCIES.md#findings-and-next-actions); source review below | Owner unknown: review affected paths before enabling them. Live impact remains unproved. |

## Current capabilities

The current scope is a local, agent-assisted SDLC foundation.
Ten built-in providers and sixteen shared skills support that scope.

| Capability | Current support | Evidence and material limit |
| --- | --- | --- |
| Workspace context | Initialization, six catalogs, configuration checks, and portable references | [Workspace model](../../../docs/WORKSPACE_DESIGN.md#brownfield-adoption-boundary); metadata does not prove deployed relationships. |
| CLI and MCP | Shared local resource discovery, operation calls, skill access, and action history | [CLI](../../../core/cli.py); [interface assertions](../../../tests/test_interfaces.py). No independent model runtime is supplied. |
| Knowledge governance | Schema, provenance, freshness, review metadata, and publication checks | [Governance assertions](../../../tests/test_knowledge_governance.py); semantic review and human approval remain separate. |
| Requirement and defect work | Shared intake, clarification, investigation, and Gherkin procedures | [Shared skills](../../../.agents/skills); these procedures require an external agent. |
| Dependency and impact analysis | Static extraction, graph snapshots, comparison, and source freshness checks | [Extraction coverage](../../../.agents/skills/service-dependencies-graph/SKILL.md#dependency-extraction-map); unsupported syntax needs direct inspection. |
| Implementation assurance | AC-to-test, AC-to-code-change, and code-change-to-test matrices; evidence and question reconciliation | [Coverage assertions](../../../tests/test_review_coverage.py); complete links alone do not establish conformance. |
| Testing | Registered commands, Robot execution, planning, and environment preflight | [Test preflight assertions](../../../tests/test_test_preflight.py); target runners and authenticated environments remain separate dependencies. |
| Local evidence adapters | Git, bounded log reading, read-only SQLite, and configured Eureka discovery | [Provider assertions](../../../tests/test_providers.py); local fixtures do not prove live discovery access. |
| External analysis | Nine named connector families, including Kibana Console/KQL and PostgreSQL reads | [Connector source](../../../core/connectors/workbench/server.js); [connector assertions](../../../tests/test_connector_provider.py); grants and private settings control use. |
| Release analysis | Collection, offline report rendering, retained hash checks, and optional Release Clinic | [Release assertions](../../../tests/test_release_report_integration.py); live collection requires configured services. |

The [architecture](../../../ARCHITECTURE.md#six-core-capabilities) distinguishes foundation tools from target engines.
Automatic ingestion, AI governance, complete assertion mapping, and durable approval workflows remain planned.
Durable workflow execution, remote runners, and the independent platform interface also remain planned.

Generic workspace metadata supports many project types.
Graph extraction centers on Java/Spring, JavaScript/TypeScript, npm/Maven, and selected Python/Robot patterns.
[Internal gRPC recognition](../../../.agents/skills/service-dependencies-graph/tools/extract_grpc_dependencies.py#L22-L28) and DQSL recognition retain project-specific assumptions.
An empty graph cannot establish that dependencies are absent.
Release Clinic retains ADO and collector-specific configuration.

## Package and platform dependencies

| Group | Required versions or packages | Consumer and boundary |
| --- | --- | --- |
| Core interpreter | Python `>=3.10` | CLI, MCP, catalogs, knowledge checks, evidence, and graph helpers. |
| Mandatory Python packages | `PyYAML==6.0.2`; `tree-sitter==0.25.2`; `tree-sitter-java==0.23.5`; `tree-sitter-typescript==0.23.2`; `jsonschema==4.25.1` | YAML loading, Java/TypeScript parsing, and JSON Schema validation. |
| Python build | `setuptools>=68` | Source installation and wheel creation. |
| Optional Release Clinic | Twelve direct packages: HTTP clients, parsers, API clients, cryptography, matching, service, and attachment parsing | [Exact declaration](../../../pyproject.toml#L18-L32). Minimum versions leave transitive resolution variable. |
| Optional Node runtime | Node `22.12+` within version 22, or Node `24+`; npm | Connector bridge and release collection. Core Python commands do not require Node. |
| Direct Node libraries | MCP SDK, axios, Azure DevOps SDK, dotenv, https-proxy-agent, node-fetch, zod, and `pg@8.16.3` | [Root manifest](../../../package.json); [root lockfile](../../../package-lock.json). |
| UI test tools | Playwright `1.64.1`, TypeScript `5.9.3`, tsx `4.20.6`, and Vitest | Optional source test harness. Browser binaries require separate provisioning. |
| Repository and desktop tools | Git; selected repository toolchains; optional browser, Outlook, Teams, and Windows `pywin32>=305` | [Setup requirements](../../../docs/SETUP.md#runtime-dependencies); these tools have separate consumers and platform limits. |
| Local persistence | Python standard-library SQLite and filesystem | Action history and evidence. No dedicated database server is required. |

The inspected root npm lock contains 435 package records and 390 HTTPS tarball entries.
All tarball entries use `registry.npmjs.org`.
These counts include workspace links and platform variants. They do not count active runtime libraries.
Root direct dependency declarations match the lockfile.
Python core transitives and Clinic extras have no complete checked-in lock.
The [dependency inventory](dependency-inventory.json) records source hashes, declared constraints, and installed versions.

## Installation and external services

Connected installation uses configured Python indexes and locked npm tarballs.
[Offline preparation](../../../core/offline.py) retains Python wheels, npm tarballs, integrity metadata, source fingerprints, and target identity.
Bundles require matching operating system, CPU, Python minor version, and interpreter ABI.
An offline package bundle does not supply live services or valid credentials.

The wheel ships the Python runtime, scaffold resources, and Release Clinic assets.
[Packaging](../../../setup.py) excludes the Node connector source and `node_modules`.
Generated workspaces need a separate connector installation when those integrations are selected.
Initialization supplies empty catalogs and guides without business checkouts or runtime source copies.

Runtime integrations include ADO, Confluence, XWiki, SonarQube, Nexus IQ, Kibana, PostgreSQL, web, and desktop messaging.
Optional Clinic clients can also use Genie, Artifactory, ServiceNow, and Vault.
Core local validation requires none of these services.
Kibana uses its Console proxy and bounded KQL support.
[PostgreSQL](../../../core/connectors/workbench/postgresql.js#L118-L160) enforces read-only transactions, role checks, query limits, and verified TLS by default.
Its database role must also restrict unsafe user functions. Deployed permissions remain unverified.

## Local readiness and findings

The [doctor result](doctor.json) reports core `READY` and integration access `UNTESTED`.
The default all-feature result is `INCOMPLETE`.
It includes missing optional settings and two deliberately unsupported interfaces: app-bridge and ado-upload-app.
This aggregate status does not establish a core failure.

### F1: Optional integration setup remains incomplete

Priority: P2 for this general review. Owner: selected integration owners.
ADO, Confluence, XWiki, Sonar, Kibana, and PostgreSQL lack required local configuration.
Nexus and messaging also lack required grants.
Clinic lacks `extract-msg` and private settings.
Source: [doctor](doctor.json). Consequence: the affected features are not ready for live use.
Next action: configure only selected features, then retain bounded authentication and behavior evidence.
Browser installation alone does not establish an authenticated business session.

### F2: Node engine metadata is broader than setup support

Priority: P2. Owner: Workbench maintainer.
The [root manifest](../../../package.json#L7) accepts Node `>=22`.
[Bootstrap](../../../core/bootstrap.py#L60-L79) rejects Node 22.0–22.11 and version 23.
Consequence: package metadata can imply unsupported compatibility.
No current runtime failure was reproduced on installed Node 24.16.0.
Next action: align metadata with the existing setup policy in a separate maintenance change.

### F3: Python installation reproducibility has limits

Priority: P2. Owner: Workbench maintainer.
Core direct versions are pinned. Python transitives and Clinic extras remain resolver-selected.
Source: [declared requirements](../../../pyproject.toml) and [existing analysis](../../../docs/DEPENDENCIES.md#python-and-node-packages).
Consequence: fresh connected installations can select different dependency sets.
Next action: retain approved bundles for repeatable installation on matching targets.
No dependency resolution failure occurred in the prepared local environment.

### F4: Optional paths reduce certificate checks or browser isolation

Priority: P2 within this review. Owner: unknown.
[Vault](../../../core/release-clinic/plugins/test/dtp-tda-service/service/vault_client.py#L79) and [Confluence](../../../core/release-clinic/plugins/test/dtp-tda-report/skills/dtp-tda-report/scripts/tda/integrations/confluence.py#L28) disable certificate verification.
[Web search](../../../core/connectors/packages/web/scripts/search-ddg.py#L36-L43) and [browser crawling](../../../core/connectors/packages/web/src/tools/webcrawlbrowser.js#L95-L101) also reduce these controls.
Browser crawling includes `--no-sandbox`.
Consequence: affected calls omit normal peer checks or browser isolation.
Live reachability, compromise, and disruptive user impact remain unproved.
Next action: review approved CA handling and browser isolation before operational use of affected paths.
These conditions were already disclosed in the dependency guide. They are not newly introduced regressions.

### Proposed follow-up checks

These criteria define possible maintenance checks. They do not authorize implementation or live access.

```gherkin
Scenario: Node metadata matches the supported installer policy
  Given the supported Node versions are 22.12 or later within 22, and 24 or later
  When package metadata and setup validate each boundary version
  Then both accept Node 22.12 and Node 24
  And both reject Node 22.11 and Node 23

Scenario: Selected optional integration has bounded readiness evidence
  Given an owner has configured a selected integration and its exact grants
  When the owner runs its declared readiness check and an authorized bounded probe
  Then the retained evidence identifies the build, environment, operation, and result
  And untested permissions and behavior remain explicit
```

## Dependency family coverage

This assessment covers core and declared optional integration boundaries.
It excludes business repository runtime relationships, private values, and exhaustive upstream SDK internals.
The [structured profile](repo-onboarding.json) models eleven bounded relationships and thirty source claims.
An inspected family has a modeled relationship. Unknown families retain incomplete mapping or unavailable evidence.

| Family | Disposition | Inspected scope and limits |
| --- | --- | --- |
| API | Inspected | Connector, Eureka, and Clinic clients. Live endpoints and effective permissions remain unknown. |
| Messaging | Not observed | No broker dependency was found in reviewed Workbench runtime paths. Desktop messaging uses applications. |
| Managed events | Not observed | No managed event broker was found in reviewed runtime paths. |
| Data | Inspected | SQLite history, PostgreSQL reads, and Kibana queries. Deployed permissions remain unknown. |
| Identity | Inspected | Credential references and Vault AppRole source. Private values and effective identities were excluded. |
| Trust | Inspected | TLS settings, CA extension, and identified optional bypasses. Live trust remains unverified. |
| Configuration | Unknown completeness | Declarations and precedence were inspected. Private values and comprehensive binding relationships were excluded. |
| Storage | Inspected | Action history, evidence, scaffold resources, and bundle artifacts. Target permissions remain environment-specific. |
| Network | Unknown completeness | Declared hosts and transports were inspected. Live routing and complete network policy remain unknown. |
| Platform | Not observed | No core cloud-platform API was found. Python, Node, browser, and desktop prerequisites have separate declarations. |
| Scheduling | Unknown completeness | Clinic startup and worker source were located. Complete coordination and recovery relationships were not assessed. |
| Observability | Inspected | Local action evidence and optional Kibana queries. Remote production logging remains unverified. |
| Frontend | Inspected | Local reports and optional browser tools. Browser binaries and hosted documentation assets remain separate. |
| Business provider | Unknown completeness | Desktop messaging prerequisites were inspected. Sessions, permissions, and delivery relationships remain unverified. |
| Delivery | Inspected | Python build, npm lock, scaffold packaging, and offline bundle preparation. No package advisory query ran. |
| Other | Not observed | No additional family was established within reviewed source. This does not prove production absence. |

## Readiness and verification

| Dimension | Assessment | Evidence or limit |
| --- | --- | --- |
| Repository identity | Ready | Exact source revision recorded above; unrelated worktree changes remain excluded. |
| Purpose and ownership | Partial | Responsibilities are documented. Several integration owners remain unknown. |
| Agent instructions | Ready | Shared skills and installed workspace guides are available. |
| Build and tests | Ready locally | Complete Python suite, connector suite, wheel build, and external initialization passed. |
| Interface contracts | Partial | CLI, MCP, and provider assertions passed. Live service contracts remain unverified. |
| Functional mapping | Ready within scope | Source, entrypoints, and representative assertions support the capability map. |
| Dependency visibility | Partial | Direct packages and optional boundaries are mapped. Private bindings and live access remain unknown. |
| Evidence governance | Ready within scope | Revision, retained results, input, and limitations are linked. Semantic approval remains separate. |

| Check | Result | Evidence |
| --- | --- | --- |
| Complete Python suite with connector integration enabled | 824 passed; zero failures, errors, or skips | [Execution](unit-tests-loopback.log) |
| Native connector tests | 39 passed; zero failures or skips | [Execution](connector-tests-loopback.log) |
| Installed Python requirements | No broken requirements | [pip check](pip-check.log) |
| Current workspace | VALID; 14 knowledge documents; zero findings | [Validation](workspace-validation.json) |
| Local readiness | Core READY; all-feature INCOMPLETE; live access UNTESTED | [Doctor](doctor.json) |
| Wheel build and local install | Passed with prepared build dependencies | [Build](wheel-build.log); [install](wheel-install.log) |
| Wheel initialization outside checkout | Passed; empty catalogs, shipped guides and schema, no runtime copy | [Probe](wheel-smoke.py); [result](wheel-smoke.json) |
| Initial restricted test attempts | Local server restrictions blocked execution; retained before full reruns | [Python](unit-tests.log); [Node](connector-tests.log) |
| Initial wheel probe | Reviewer used a nonexistent schema filename; corrected without product changes | [Original probe](wheel-smoke-initial.py); [failure](wheel-smoke.stderr) |
| Document checks | Local links passed; no whitespace or prose-length findings | [Bounded checks](document-checks.json) |
| Source evidence helper | Passed for 30 claims and 11 dependency relationships | [Validation](evidence-validation.log); semantic accuracy and completeness remain separate. |

The complete suites passed after loopback access was available for their local mock servers.
Suite totals are separate. They do not measure business AC coverage.
The wheel probe reused prepared dependencies. It did not resolve dependencies through a fresh connected or complete offline installation.
The initial filename inventory enumerated 42,645 files and truncated test candidate and omitted-directory listings.
Filename inventory does not establish exhaustive dependency discovery.
Source review focused on current harness code and excluded archived business evidence.
No indexes or dependency graphs were rebuilt.

Native Windows, live services, business E2E, and production reachability remain unverified.
No vulnerability advisory service was queried.
No deployment or publication approval is claimed.
No runtime fixes or catalog proposals were made.

Confidence is high for local execution results and inspected declarations.
Confidence is medium for dependency completeness because source inventory and upstream inspection have stated limits.
Live integration and target-environment outcomes remain unknown.

## Writing review

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
