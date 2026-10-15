# External dependency investigation

Identify external relationships that can affect startup, requests, messages, data, permissions, delivery, or engineering execution.
Include provided interfaces and local configuration assets, even when they have no remote peer.
Use [the evidence contract](readiness-and-evidence.md) for exact JSON fields, evidence statuses, and profile validation rules.
This guide defines investigation scope; it does not extend Workbench catalogs or implement graph extraction.

## Required report placement

Place the critical dependency summary immediately after repository identity and purpose.
Place dependency details and family coverage before readiness.
Use stable local dependency IDs across summary rows, details, claims, and findings.
Do not equate these IDs with canonical services, capabilities, sources, or contracts.

The summary needs an affected workflow, consequence, evidence status, owner, and next action for each critical relationship.
Include unresolved permissions, activation, configuration, and impact when they can affect the requested workflow.
Use qualitative criticality from evidenced consequences, with its own evidence status and rationale.
Do not infer severity from technology names or dependency counts.
Keep source-derived business impact inferred unless applicable evidence supports a narrower observed claim.
Use unknown impact when the available evidence cannot establish the consequence.

## Discovery families

Review every family and record its coverage disposition.
Examples guide inspection; they do not justify invented relationships.
Keep runtime, configuration, build, test, deployment, and optional dependency scopes distinct.

| Family key | Candidate technologies and assets |
| --- | --- |
| `api` | REST/HTTP, GraphQL, gRPC, SOAP/WSDL, JSON-RPC, XML-RPC, OData, webhooks, callbacks, WebSocket, SSE, TCP/UDP protocols. |
| `messaging` | Kafka/Streams, JMS, IBM MQ, RabbitMQ, ActiveMQ/Artemis, AMQP, MQTT, Solace, TIBCO, NATS/JetStream, Pulsar, Redis Streams, ZeroMQ. |
| `managed-events` | SQS/SNS, Kinesis, EventBridge, Azure Service Bus/Event Hubs, Google Pub/Sub, managed event routing. |
| `data` | SQL/JDBC/R2DBC/ODBC, document/key-value/graph/time-series stores, warehouses, caches, search indexes, vector stores. |
| `identity` | LDAP/LDAPS, Active Directory, Kerberos, OAuth/OIDC, SAML, SCIM, JWKS, token introspection, federation, entitlements. |
| `trust` | Vault, secret managers, KMS/HSM, certificate authorities, trust stores, mTLS identities, signing, encryption services. |
| `configuration` | YAML/JSON/TOML/XML/properties/INI, profiles, imports, environment references, arguments, configuration servers, Consul/ZooKeeper, feature flags, mounted settings. |
| `storage` | Local/shared files, NFS/SMB, SFTP/FTP, object/blob stores, imports/exports, file watchers, document repositories. |
| `network` | DNS, service discovery, registries, proxies, ingress, gateways, load balancers, VPNs, service meshes, network policies. |
| `platform` | Kubernetes APIs, cloud SDK operations, metadata services, sidecars, serverless bindings, platform control services. |
| `scheduling` | Cron, Quartz, batch/workflow engines, external job triggers, distributed locks, leader election. |
| `observability` | Logs, metrics, traces, audit sinks, alerts, health probes, monitoring agents, operational control endpoints. |
| `frontend` | Remote micro frontends, module federation, import maps, CDNs, browser SDKs, postMessage, FDC3/OpenFin, desktop bridges, analytics. |
| `business-provider` | SMTP/IMAP, SMS, push, payments, market feeds, FIX, licensing, third-party SaaS, domain-specific providers. |
| `delivery` | Package registries, libraries, native binaries, FFI, container bases, artifact stores, VCS, CI runners, toolchains, test services. |
| `other` | Additional source-supported dependency kinds with an explicit description and inspection scope. |

A dependency can involve several concerns.
Use separate relationships when distinct operations, directions, activation, access controls, or failures require different evidence.
Cross-reference related dependency IDs instead of merging unrelated conclusions.
Do not merge records solely because host aliases, package names, topics, queues, or database names match.
Preserve broker, namespace, datasource, profile, environment, and operation distinctions.

## Common relationship investigation

Inspect each relationship through the following questions.
Populate the structured contract's required attributes with supported values or explicit unknowns and reasons.
Record additional family details in the corresponding contract fields and human report.

| Concern | Required investigation |
| --- | --- |
| Identity | Local component, peer or asset, protocol, operation/resource, direction, and confirmed identities. |
| Scope | Runtime/configuration/build/test/deployment phase, environment/profile, optionality, and activation declaration. |
| Initiation | Calling symbol, initiating event, lifecycle trigger, timing, guards, feature flags, and unresolved frequency. |
| Interaction | Synchronous/asynchronous mode, request/reply or streaming pattern, and data effects. |
| Access | Authentication, authorization, network restrictions, enforcement points, and unavailable controls. |
| Configuration | Safe source paths/key names, consumers, defaults, required values, imports, precedence, and external injection. |
| Failure | Timeouts, retries/backoff, fallback, circuit breakers, delivery failures, and affected workflows. |
| Review | Field-level claim references, evidence status, limits, known or unknown owner, unresolved questions, and next action. |
| Criticality | Consequence, rationale, evidence status, and project-specific impact limits. |

Trace a client declaration through its callsite and configuration before describing an interaction.
Keep declaration, reachable source path, configured deployment binding, and retained runtime observation separate.
Source reachability does not prove a call occurred.

An observed field cannot transfer certainty to another field.
Unknown attributes need a reason; inferred attributes need supporting claims and an inference reason.
Conflicting attributes retain both observations and explain the conflict.
Use existing claim IDs for citations; do not duplicate provenance in dependency records.

## Provided interfaces and permissions

Inventory each identified operation and its exposure boundary.
Record HTTP method/path, GraphQL field, RPC service/method, stream, webhook, callback, or equivalent operation.
Trace application binding through available deployment, gateway, ingress, and proxy configuration.
Keep source registration, configured exposure, and observed production reachability separate.

Inspect global filters, ordered security chains, route rules, method guards, resolver checks, interceptors, and deployment controls.
Record authentication mechanisms, roles, scopes, entitlements, tenant/resource checks, and administrative restrictions when supported.
Inspect anonymous exceptions and profile-dependent overrides before describing effective source-declared restrictions.
Preserve control ordering and conflicts when the inspected source cannot resolve them.
Record the enforcement location and operation scope for each permission claim.
Keep authentication, authorization, network reachability, CORS, and CSRF distinct.

Missing permission evidence means unknown restrictions; it does not mean public access.
A UI entitlement check does not establish server enforcement.
A documented security requirement does not establish its implementation.
Target application permissions do not grant Workbench execution rights.

## Outbound APIs, RPC, and streams

Record remote operation, initiating caller, trigger, conditions, lifecycle phase, and synchronous/asynchronous behavior.
Trace UI actions, inbound requests, message handlers, schedules, startup hooks, manual actions, retries, and shutdown hooks.
Identify transaction stages, including calls before or after commit, when source establishes that ordering.
Record feature flags, profiles, conditional bindings, payload guards, and response-dependent branches.
Preserve unresolved cron timezones, event ordering, runtime frequency, dynamic targets, and endpoint substitutions.
Client construction alone does not establish a call, frequency, or active connection.

For gRPC, inspect Protobuf services/methods, unary/streaming mode, target resolution, deadlines, interceptors, and metadata.
Record transport security and authentication/authorization separately.
For HTTP and SOAP, inspect request construction, methods/actions, redirects, proxy settings, credentials mechanisms, and response handling.
For webhooks and callbacks, identify registration and invocation directions separately.
For WebSocket and SSE, identify connection initiation, subscriptions, reconnect conditions, and closure behavior.
Keep retries, backoff, circuit breakers, fallback, and failure consequences within their evidenced scope.

## Messaging and managed events

Record publish, subscribe, send, receive, request, or reply roles for each relationship.
Identify broker binding, protocol, destination, routing key, subscription, consumer group, and namespace when available.
Link payload/schema definitions and schema registry dependencies.
Record listener activation, filters, selectors, schedules, and application guards.
Keep broker availability separate from listener or producer registration.

Inspect acknowledgements, transactions, commit mode, ordering, partitions, replay, retention, deduplication, and idempotency when applicable.
Inspect timeout, retry/backoff, poison-message handling, dead-letter queues, and consumer concurrency.
Record source-declared delivery guarantees without claiming observed delivery.
Keep credentials references, ACL declarations, TLS, and destination permissions separate.

For Kafka, inspect producer/consumer configuration, topic binding, groups, offsets, serializers, schema registry, and transactional settings.
For JMS and MQ, inspect connection factories, destinations, selectors, acknowledgement modes, transactions, and reply destinations.
For RabbitMQ/AMQP, inspect exchanges, queues, bindings, routing keys, durability, and publisher confirms.
For Solace, inspect VPN/broker binding, topics/queues, subscriptions, direct/guaranteed delivery, and acknowledgement behavior.
For managed events, inspect resource bindings, policies, subscriptions, filters, fan-out, and delivery/dead-letter settings.
Equal destinations on different broker bindings do not establish shared connectivity.

## Databases and data services

Identify engine/client, datasource binding, schema/table/collection/index, query/procedure, and read/write effects.
Trace repository/query calls to their calling workflows and configuration.
Record transaction boundaries, consistency/read preferences, pools, replicas, failover, and access restrictions when available.
Include caches, search, vector stores, warehouses, and embedded databases when their failure can affect the workflow.
Distinguish source query construction from successful execution and deployed database permissions.

Inspect migration files and their activation separately from application datasource use.
A migration alone does not prove an active connection or deployed schema.
Record initialization requirements, schema ownership uncertainty, and external provisioning gaps.
Do not include data rows, credentials, or sensitive query parameters.

## Configuration, identity, and trust

Trace consumers to configuration files, imports, keys, profiles, arguments, environment references, or external providers.
Record required/default behavior, overrides, precedence, and unresolved substitutions.
Identify configuration loaded at build, startup, request time, refresh, or deployment when source establishes that timing.
An external value that was not inspected remains unknown.
Do not choose a deployment value by guessing precedence.
Use nonsecret key names and reference mechanisms without copying secret values or credential file contents.

For LDAP, inspect bind method, TLS, search/base references, filters, group mapping, and downstream authorization consumers.
Keep directory authentication, group retrieval, and application authorization separate.
Do not retain directory entries, user identifiers, bind credentials, or sensitive search values.
For OAuth/OIDC/SAML, inspect issuer/discovery, token validation, audience, scopes, JWKS, introspection, and refresh dependencies.
For trust services, inspect secret/certificate references, retrieval/rotation timing, trust boundaries, and unavailable provisioning.
Record fail-open/fail-closed behavior only when inspected source supports the claim.

## Other engineering dependencies

Trace storage paths, mounts, file formats, import/export triggers, permissions, and missing-file behavior.
Inspect discovery/network bindings, proxy paths, mesh policies, DNS assumptions, and unavailable deployment controls.
Inspect platform operations, scheduling/coordination, telemetry export, health checks, and operational control paths.
Inspect frontend remote resolution, desktop bridges, third-party providers, package supply, native execution, and test services.
Keep engineering dependencies separate from active business runtime relationships.
An SDK import, package lock, container base, or CI declaration establishes only its supported declaration scope.

## Coverage and completion

Each family needs `inspected`, `not-observed`, `unknown`, or `out-of-scope` disposition, with scope and reason.
Coverage dispositions differ from relationship attribute evidence statuses.
Record inspected paths, exclusions, missing environments, inaccessible settings, and required follow-up.
Preserve enumeration limits and truncated inventory categories in coverage reasons.
Candidate counts cover enumerated files, not every file in the repository.

Use `not-observed` only for the inspected scope; it never establishes absence from production.
Use `out-of-scope` for an explicit boundary, rather than as a substitute for missing evidence.
Unknown owners remain unknown until evidence establishes responsibility.

Validate the dependency profile through the existing evidence helper.
Revisit unsupported certainty and preserve unresolved findings after structural validation passes.
The helper cannot prove completeness, semantic truth, effective permissions, deployed connectivity, or business approval.
The separate graph skill owns automatic graph extraction.
Unsupported canonical contract mappings remain in this assessment, with their evidence and review needs.
