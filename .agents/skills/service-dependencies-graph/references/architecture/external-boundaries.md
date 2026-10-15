# Repository External Boundary Extraction

Extract independently per protocol, then join findings through evidence and configuration keys. Each interface keeps raw values, normalized values, environment/profile, owner component, and unresolved expression.

## REST/HTTP

Inbound evidence includes Spring mappings, generated/open API server contracts, nginx/gateway routes, and deployed ingress. Outbound evidence includes Feign, WebClient/RestClient/RestTemplate, frontend fetch/axios/RTK Query, generated clients, and reverse-proxy calls.

Capture method, raw and normalized path template, base URL/service name/host, query/header/content type, request/response contract, auth mechanism, timeout/retry only when relevant, and configuration chain. Do not strip a gateway prefix unless a route/rewrite declaration proves it. Dynamic URL fragments remain templates with variable bindings.

## GraphQL

Capture inbound query/mutation/subscription root fields and resolver symbols. For outbound operations capture endpoint, transport (HTTP/WebSocket), operation type/name, root fields, document/schema fingerprint, variables/result type, and client. Multiple operations may share one endpoint; emit operation interfaces, not only a generic GraphQL dependency.

## Kafka and messaging

Capture produced/consumed topic, consumer group, key/message type, serializer/deserializer or schema subject, headers/routing key, cluster alias, concurrency, and environment. Resolve constants/placeholders/SpEL/Camel URIs through configuration. A topic name without cluster/environment may match candidates later but is not globally unique.

One producer or listener with conditional/dynamic topics emits variants. A consumer group is not the provider identity, but it is a useful compatibility/behavior signal. Comments and disabled listeners do not confirm an active interface.

## Database

Capture datasource identity/key, dialect, database/schema/object, and `READ`/`WRITE`/`EXECUTE`/`MIGRATE`. Code/SQL determines object-level behavior; datasource config alone emits a database connection dependency. Never store credentials or unredacted connection strings.

Shared-table dependencies require both repository access declarations and later identity resolution through datasource + schema + object. Same table names on unknown datasources stay ambiguous.

## MFE, browser events, and interoperability

Capture single-spa application names, lifecycle exports, SystemJS/import-map modules and targets, Module Federation remotes/exposes, runtime-loaded components, custom browser/BroadcastChannel/postMessage events, storage keys used as inter-app contracts, and FDC3 intents/channels/context types.

An import map is configuration evidence; `System.import`/federated import is static use evidence; a browser trace is runtime evidence. Preserve environment-specific import-map entries and override mechanisms.

## Internal libraries and contracts

Include a Maven/npm dependency as an architectural interface when at least one applies:

- coordinates belong to an internal namespace/catalog;
- it carries an API client, domain/event/schema contract, shared database model, plugin/extension point, MFE/runtime module, security integration, or generated code used across repositories;
- runtime/deployment behavior depends on its artifact identity or version;
- another in-scope repository produces the artifact.

Exclude ordinary third-party implementation libraries such as Jackson, Lombok, React, or test frameworks unless the question specifically concerns them or they define a runtime plugin boundary. Preserve excluded dependency counts/reasons in diagnostics so filtering is auditable.

## Configuration/runtime chain

Parse `application.yml`/properties, environment templates, Webpack/import maps, nginx/gateway rules, Helm/Kubernetes, Docker/Compose, deployment descriptors, and CI/CD definitions that bind artifact, service, route, topic, datasource, or configuration identities. CI/CD proves packaging/deployment intent at a revision; only deployment/runtime evidence proves an active environment.

Build a directed key-resolution graph:

```text
code use -> logical property -> base config -> profile override
  -> environment/secret reference -> deployment binding -> observed value
```

Store secret keys and redacted fingerprints, never values. Values that differ by profile/environment create interface `variants`. A default placeholder value is a default variant, not proof of deployed use. Spring application name, Maven artifact ID, package name, deployment/service names, host aliases, import-map name, and repository metadata become aliases with provenance.

## Evidence precedence and failures

Static, configuration, deployment, and runtime evidence describe different facts; do not overwrite one with another. Runtime may prove an observed route while source proves additional dormant paths. Documentation-only dependencies remain inferred.

Emit diagnostics for unsupported clients, reflection, dynamically generated queries, unknown shared-library behavior, missing profiles, conflicting route rules, inaccessible runtime artifacts, and possible dead code. Never treat missing evidence as an absence claim.
