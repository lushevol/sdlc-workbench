---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
implementation_status: PLANNED
limitations:
- Automated checks do not check the complete approved dictionary or grammar rules.
- This plan defines proposed reporting behavior, not implemented dependency discovery.
- Static inspection cannot establish complete production connectivity or effective deployed permissions.
---

# Repository onboarding dependency reporting plan

Investigation date: 15 October 2026.
Inspected source revision: `608153ed1fb838a3d807a591f3e96dea48094eba`.
This stage completes investigation and planning before skill implementation.

## Purpose

Make critical dependency relationships prominent, traceable, and useful for engineering decisions.
Identify provided interfaces, consumed systems, execution conditions, access restrictions, configuration bindings, and failure consequences.
Expose unresolved relationships and coverage limits beside each conclusion.
The current consumers are agents preparing repository assessments and engineers reviewing those assessments.
The expected benefit is fewer hidden interface, environment, permission, and operational assumptions.

## Findings from current source

| Finding | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| Dependency reporting has one generic table. | [Assessment template](../../.agents/skills/repository-onboarding/assets/assessment.template.md), lines 37–41 | Important permissions, conditions, and operational details can disappear into brief rows. | unknown | Add a prominent summary and dedicated dependency sections. |
| Discovery guidance covers a limited set of relationship kinds. | [Discovery guide](../../.agents/skills/repository-onboarding/references/discovery-guide.md), lines 30–35 | Agents lack specific guidance for gRPC, LDAP, permissions, and operational dependencies. | unknown | Add a focused dependency investigation guide. |
| Structured claims have no dependency register. | [Evidence contract](../../.agents/skills/repository-onboarding/references/readiness-and-evidence.md), lines 33–103 | Dependency attributes and coverage cannot receive consistent structural checks. | unknown | Define dependency records linked to existing claims. |
| Validation checks claims and citations only. | [Evidence validator](../../.agents/skills/repository-onboarding/scripts/validate_evidence.py), lines 42–165 | Missing dependency fields and unresolved claim references currently pass. | unknown | Validate an explicitly selected dependency report profile. |
| Configuration candidates rely on specific filenames. | [Scanner](../../.agents/skills/repository-onboarding/scripts/scan_repo.py), lines 37–43 | Environment profiles and deployment settings need supplemental inspection. | unknown | Extend filename discovery and disclose remaining limits. |
| Runtime contracts intentionally support six types. | [Catalog loader](../../core/context/catalogs.py), lines 16–17 and 46–62 | Arbitrary dependency types cannot become valid catalog types. | unknown | Keep detailed dependency records inside the staged assessment. |

The review inspected helper callers, tests, catalog interfaces, packaging, and the graph ownership boundary.
Two independent agents reviewed coverage and compatibility without modifying files.
Existing unrelated README and SDLC template changes remain outside this stage.

## Proposed report layout

Place a critical dependency summary immediately after repository identity and purpose.
Place detailed dependency sections before the general readiness table.
Use stable local dependency IDs to connect the summary, details, claims, and findings.
These local IDs grant no canonical service or catalog identity.

| Section | Required content |
| --- | --- |
| Critical dependency summary | Affected workflow, dependency ID, failure or permission consequence, evidence status, owner, and next action. |
| Provided interfaces | Every identified operation, exposure boundary, authentication, authorization, and enforcement evidence. |
| Outbound interactions | Remote operation, initiating caller, trigger, conditions, execution phase, configuration, and failure behavior. |
| Messaging | Producer or consumer role, broker binding, destination, delivery behavior, permissions, and activation conditions. |
| Databases and data services | Connection binding, engine, reads or writes, data objects, transactions, migrations, and access restrictions. |
| Configuration dependencies | Source files, key names, consumers, profiles, precedence, external injection, and unresolved substitutions. |
| Other dependencies | Relevant identity, storage, network, platform, operations, frontend, execution, and supply dependencies. |
| Coverage and exclusions | Each family inspected, evidence scope, omissions, unresolved runtime inputs, and follow-up action. |

A dependency card can hold details that make a comparison table unreadable.
Keep summary rows short and link them to the detailed records.
Separate a configured endpoint from an endpoint exposed in the inspected deployment configuration.
Do not describe either as active production exposure without applicable runtime evidence.

## Dependency coverage families

The following list guides discovery and remains extensible.
Examples identify technologies to investigate, not relationships to invent.
A manifest entry establishes a declaration until inspected callers establish more.

| Family | Examples and required distinctions |
| --- | --- |
| Provided and consumed APIs | REST/HTTP, GraphQL, gRPC, SOAP/WSDL, JSON-RPC, XML-RPC, OData, TCP/UDP clients, webhooks, callbacks, WebSocket, and SSE. |
| Messaging and streaming | Kafka, Kafka Streams, JMS, IBM MQ, RabbitMQ, ActiveMQ/Artemis, AMQP, MQTT, Solace, TIBCO, NATS/JetStream, Pulsar, Redis Streams, and ZeroMQ. |
| Managed event services | SQS/SNS, Kinesis, EventBridge, Azure Service Bus/Event Hubs, Google Pub/Sub, and equivalent event routing services. |
| Databases and data services | SQL/JDBC/R2DBC/ODBC, document stores, key-value stores, graph databases, time-series stores, warehouses, caches, search, and vector stores. |
| Identity and directory services | LDAP/LDAPS, Active Directory, Kerberos, OAuth/OIDC, SAML, SCIM, JWKS, token introspection, federation, and entitlement services. |
| Secrets and trust | Vault, cloud secret managers, KMS/HSM, certificate authorities, trust stores, mTLS identities, signing, and encryption services. |
| Configuration and feature control | YAML/JSON/TOML/XML/properties/INI, profiles, environment names, arguments, configuration servers, Consul/ZooKeeper, feature flags, and mounted settings. |
| Files, objects, and transfer | Local/shared files, NFS/SMB, SFTP/FTP, object stores, blob stores, batch imports/exports, watchers, and document repositories. |
| Network and discovery | DNS, service registries, proxies, ingress, gateways, load balancers, VPN dependencies, service meshes, and network policies. |
| Platform and cloud services | Kubernetes APIs, cloud SDK calls, runtime metadata services, sidecars, serverless bindings, and platform control services. |
| Scheduling and coordination | Cron, Quartz, batch engines, workflow engines, distributed locks, leader election, and externally triggered jobs. |
| Observability and operations | Logging, metrics, traces, audit sinks, alerting, health probes, monitoring agents, and operational control endpoints. |
| Frontend and desktop integration | Remote MFEs, module federation, import maps, CDNs, browser SDKs, postMessage, FDC3/OpenFin, desktop bridges, and analytics. |
| Notifications and business providers | SMTP/IMAP, SMS, push, payment providers, market feeds, FIX, licensing, third-party SaaS, and other domain-specific integrations. |
| Build, test, deployment, and execution | Package registries, libraries, native binaries, FFI, container bases, artifact stores, VCS, CI runners, toolchains, and test services. |
| Other | Additional evidence-supported dependency kinds with an explicit description and reviewable scope. |

Keep runtime dependencies separate from build, test, deployment, and optional integrations.
Treat local configuration files as configuration dependencies, even when they have no remote peer.
Do not merge relationships solely because they share a host alias, topic name, package name, or database name.
Preserve broker, environment, namespace, profile, and operation distinctions when evidence supplies them.

## Required relationship details

Each relationship needs a common record plus applicable family details.
Use explicit unknowns and reasons when inspected evidence cannot establish a field.
Do not populate required fields with invented values.
Different fields can have different evidence states within the same relationship.

| Common field group | Required information |
| --- | --- |
| Identity | Local dependency ID, family, relationship direction, local component, peer or asset, protocol, and operation/resource. |
| Scope | Runtime/build/test/deployment/configuration phase, environment/profile, optionality, and declared activation. |
| Initiation | Caller, initiating event, startup/request/message/schedule/manual/shutdown trigger, guards, feature flags, and timing. |
| Interaction | Synchronous/asynchronous behavior, request/reply or streaming pattern, and relevant data effects. |
| Access | Authentication, authorization, network restrictions, enforcement points, and unsupported permission conclusions. |
| Configuration | Source paths, nonsecret key names, override precedence, external bindings, defaults, and unresolved values. |
| Failure and resilience | Timeout, retry, backoff, fallback, circuit breaker, delivery behavior, and affected workflow. |
| Evidence and review | Existing claim references, per-field status, limits, known or unknown owner, questions, and next action. |
| Criticality | Qualitative consequence, supporting rationale, confidence, and project-specific limits. |

For provided APIs, inspect method/path, GraphQL field, RPC service/method, stream, or callback operation.
Trace authentication and authorization through global, route, method, resolver, interceptor, gateway, and deployment controls.
Record roles, scopes, entitlements, tenant/resource checks, anonymous access, and administrative restrictions when source supports them.
Keep network reachability, CORS, CSRF, authentication, and authorization distinct.
Missing authorization evidence means unknown restrictions, not public access.
Do not equate target API permissions with Workbench execution grants.

For outbound calls, trace callers and guards before describing when the call occurs.
Record startup, UI actions, inbound requests, message handlers, schedules, transaction stages, retries, and feature/profile conditions.
Preserve unresolved cron timezones, endpoint substitutions, dynamic targets, and runtime routing.
For gRPC, capture streaming mode, deadlines, interceptors, metadata, transport security, and target resolution.
A client declaration alone cannot establish invocation frequency or an active remote connection.

For messaging, capture publish/subscribe/send/receive/request/reply roles and broker identity or configuration binding.
Record topic/queue/exchange, routing keys, consumer groups, subscriptions, payload/schema references, and schema registry dependencies.
Inspect acknowledgements, transactions, ordering, deduplication, replay, retries, and dead-letter behavior when available.
Capture Kafka security/ACL declarations and Solace direct/guaranteed delivery distinctions when source supplies them.
Do not infer shared connectivity from equal destinations in different broker configurations.

For databases, capture engine/client, datasource binding, schema/table/collection, queries, stored procedures, and read/write effects.
Inspect transaction boundaries, migration activation, connection pools, replica selection, failover, and database permissions when available.
Keep intended schema changes separate from active datasource use.
A migration file alone does not prove that the application connects to that database.

For configuration, trace each consumer to its file, key, profile, override, or external source reference.
Record required/default behavior and missing environment inputs.
Preserve unresolved precedence rather than selecting an assumed deployment value.
Report secret reference mechanisms and nonsecret key names without copying credentials or secret values.
For LDAP, inspect bind method, TLS, search/base configuration, group mapping, and downstream authorization consumers.
Omit sensitive directory entries, user identifiers, and bind credentials.

## Criticality and coverage rules

Prioritize dependencies by evidenced workflow consequences.
Useful signals include startup blocking, synchronous request failure, authorization decisions, unavailable writes, and message delivery failure.
Keep source-derived criticality as an inference unless applicable operational evidence or approved context supports it.
Use `unknown` when business impact cannot be established.
Do not infer severity from technology names or dependency counts.

Each coverage family needs `inspected`, `not-observed`, `unknown`, or `out-of-scope` status.
Record inspected paths, excluded areas, evidence limits, and reasons beside that status.
Coverage dispositions remain separate from claim and dependency attribute evidence statuses.
`not-observed` means no relationship was found within the inspected scope.
It does not mean the dependency is absent from production.
Required unresolved fields and critical unknowns must remain visible in the summary and findings.

## Structured report and compatibility

Keep existing `schema_version: "1.0"` reports valid.
Introduce an explicit optional profile, proposed as `dependency_profile: "external-dependencies/1"`.
New onboarding assessments select that profile and include `external_dependencies` and `dependency_coverage`.
Legacy reports remain valid without claiming the stronger dependency coverage gate.
Reject dependency-extension data that omits or contradicts its declared profile.

Keep citations in existing claims and link dependency fields to those claim IDs.
Require field-level evidence status and unresolved reasons for permissions, triggers, configuration, and criticality.
An observed protocol must not imply observed authorization or deployment.
Finalize exact JSON field names and family-specific requirements in the evidence reference before implementation.

Extend the existing helper to check structure, IDs, enum values, coverage records, and claim references.
Require evidence-bearing claims for observed and inferred dependency attributes.

An observed attribute needs an observed supporting claim for that field.
An inferred attribute needs cited support and an inference reason.
A conflicting attribute needs a conflicting claim or claims citing both conflicting observations.
An unknown attribute needs an explicit reason.
Reject evidence status escalation between an attribute and its supporting claims.

Keep existing commit, byte, path, line-range, and read-only checks active.
Structural validation cannot prove relationship completeness, semantic truth, effective permissions, or deployed connectivity.

Detailed dependency records remain skill-local staging artifacts.
Use existing catalog types only where their supported meaning fits the inspected interface.
Do not mislabel gRPC or LDAP to obtain a valid canonical contract.
Keep unsupported catalog mappings unresolved in the assessment.
The graph skill retains ownership of automatic dependency graph extraction.

## Investigation procedure

1. Capture checkout identity, scope, inventory warnings, and available environments.
2. Locate provided entrypoints and trace their effective source-declared permission controls.
3. Trace outbound callsites through callers, guards, lifecycle triggers, and configuration bindings.
4. Inspect messaging clients/listeners, data access, directory clients, files, platform clients, and operational integrations.
5. Inspect configuration imports, profiles, deployment bindings, defaults, and unavailable external settings.
6. Record failure behavior, affected workflows, unresolved permissions, and confidence for each relationship.
7. Review every coverage family and preserve missing or excluded evidence.
8. Validate the report, revisit questionable mappings, and produce the critical summary.

Keep the scanner a filename and safe metadata inventory.
Expand candidates for profile configuration, deployment settings, migrations, WSDL/XSD, and other interface files.
The scanner already recognizes `.proto`, GraphQL, Avro, OpenAPI, and AsyncAPI candidates.
Add targeted patterns for `application-*`, `bootstrap*`, Helm, Kustomize, Compose, Terraform, Flyway, and Liquibase.
Treat all such matches as candidates until inspected source establishes their role.
Preserve ignored-file, nested-repository, symlink, credential, and output-directory boundaries.

## Planned implementation stages

| Stage | Files and changes | Completion gate |
| --- | --- | --- |
| 1. Guidance and report design | Update `SKILL.md`, discovery/readiness/registry references, and assessment/instruction templates. Add `references/external-dependencies.md`. | Every requested family has reporting guidance, evidence rules, and an explicit coverage disposition. |
| 2. Structured checks and inventory | Extend `validate_evidence.py` for the optional profile. Extend `scan_repo.py` filename candidates only. | Legacy reports pass; invalid extension records fail; candidate discovery preserves source boundaries. |
| 3. Regression and independent use | Extend onboarding and resource-shipping tests. Run an isolated mixed-stack assessment with an independent agent. | Reports expose permissions, triggers, messaging, configuration, storage, and unresolved relationships. |
| 4. Distribution and review | Run required checks, build the wheel, initialize an external workspace, retain evidence, and review the staged diff. | Required checks pass; shipped resources match; the completed stage receives a scoped automatic commit. |

Affected implementation paths remain inside the canonical onboarding skill and its existing tests.
Packaging already includes the required Markdown, Python, JSON, and YAML resource types.
No packaging implementation change is currently indicated.
Qualitative risk is moderate because report compatibility and evidence requirements affect agent conclusions.
No business repository execution or network access is needed for implementation validation.

## Planned validation

Use private temporary fixtures with committed source and explicit evaluation boundaries.
Include provided APIs, permission overrides, guarded outbound calls, gRPC, LDAP, Kafka, MQ/Solace, configuration, and database access.
Include declared-only clients and migrations to test evidence limits.
An independent agent receives the skill and raw fixture without the intended findings.
Compare its report with inspected source and retained helper results.

```gherkin
Scenario: Preserve legacy report compatibility
  Given a valid report without a dependency profile
  When the evidence helper validates its committed citations
  Then validation exits with status 0
  And the result does not claim complete dependency profile coverage

Scenario: Validate dependency claim references
  Given a dependency profile contains one reference to an unknown claim ID
  When the evidence helper validates the report
  Then validation returns a failure identifying that dependency and field

Scenario: Reject unsupported permission certainty
  Given an observed permission attribute references only an inferred claim
  When the evidence helper validates the report
  Then validation returns a failure identifying that permission attribute

Scenario: Expose unknown API authorization
  Given an identified API has no available authorization evidence
  When an agent produces the dependency assessment
  Then its permission status is unknown with a reason
  And the report does not describe that API as public

Scenario: Preserve outbound activation conditions
  Given a source call is guarded by a feature flag and initiated by a scheduled handler
  When an agent traces that dependency
  Then the report cites the handler, guard, and configuration binding
  And it preserves an unknown schedule timezone when source does not establish one

Scenario: Keep messaging boundaries separate
  Given two identical topic names use different broker bindings
  When the assessment records their messaging relationships
  Then it retains two separate relationships
  And it does not claim connectivity between those brokers

Scenario: Distinguish declarations from execution relationships
  Given a migration exists and an SDK appears only in a build manifest
  When the assessment reviews data and API dependencies
  Then neither declaration establishes an active runtime connection
  And both retain their inspected scope and evidence limits

Scenario: Preserve dependency guidance in generated workspaces
  Given the built wheel is installed outside the source checkout
  When the installed command initializes and validates a workspace
  Then validation reports zero findings
  And the dependency reference and updated templates match source bytes
  And the generated core directory contains zero Python runtime files
```

Also test missing required fields, duplicate IDs, invalid directions, incomplete coverage, and malformed unknown reasons.
Preserve existing exact-revision, ignored-file, symlink, secret exclusion, and read-only regressions.
Check that scanner output contains safe paths and metadata without configuration values.

Run these required commands from the standalone source checkout during implementation:

```sh
python -m unittest discover -s tests -v
python -m pip wheel . --no-deps --wheel-dir dist
ai-sdlc --workspace PATH validate
```

Use the installed command for external initialized workspaces.
Record actual commands, environment limits, failures, and successful alternatives.
Run skill structure, local-link, report writing, and staged-diff checks.
Keep automated results separate from complete ASD writing review.

## Planning-stage validation and next action

Planning-stage checks cover source citations, local links, prose limits, documented commands, and the diff.
The six cited source files match the inspected revision.
Local link and prose limit checks passed.
Independent reviews found no coverage or compatibility blocker after the evidence status clarification.

Runtime tests, builds, and workflow evaluations belong to the planned implementation stages.
No skill implementation has changed during this stage.
Full ASD writing review remains pending.

Owner: unknown for final dependency reporting contract review.
Next action: implement the reviewed stages with the evidence and compatibility boundaries above.
