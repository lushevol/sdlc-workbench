# Repository discovery guide

Use these signals to investigate candidate ownership and dependency relationships.
A filename or declaration does not prove invocation, connectivity, permission, or behavior.
Use [the external dependency guide](external-dependencies.md) for family coverage and required investigation details.

## General sequence

1. Capture the exact revision, checkout changes, instructions, inventory warnings, and inspection scope.
2. Separate tracked source from generated, vendored, ignored, nested-repository, and unavailable material.
3. Read applicable instructions, architecture, manifests, CI configuration, and deployment definitions.
4. Locate deployable entrypoints and provided interfaces before inspecting leaf functions.
5. Trace callers, access controls, outbound clients, configuration bindings, and failure paths.
6. Group business functions by responsibility and source patterns; avoid a component for every file.
7. Inspect tests and assertions for the identified behavior; retain execution limits.
8. Record exact source citations and a coverage disposition for every dependency family.

Inspect inventory `category_counts`, `enumeration_truncated`, and reporting limits before selecting source candidates.
Counts describe enumerated files only.
Truncated candidate lists and enumeration prevent exhaustive coverage claims.
Use `migration_candidates` as migration discovery hints, rather than proof of datasource use.

## React, TypeScript, and micro frontends

- Locate package/workspace manifests, TypeScript configuration, bundler configuration, import maps, and micro frontend registration.
- Inspect routes, server handlers, GraphQL resolvers, UI actions, state stores, clients, sockets, workers, and desktop bridges.
- Trace the UI action through hooks or state to the remote operation and its configuration.
- Inspect authentication providers, token attachment, entitlement checks, route guards, and resource checks.
- A hidden button or client guard does not establish server authorization.
- Separate compile-time imports from dynamic module federation, browser resolution, and broker routing.
- Record CDN assets, analytics, browser storage, service workers, postMessage, FDC3/OpenFin, and remote SDK dependencies when applicable.
- Do not infer remote implementation from an alias, import-map key, or package name.

## Spring Boot and Java

- Locate Maven/Gradle manifests, application classes, profiles, deployment bindings, and imported configuration.
- Inspect controllers, resolvers, RPC services, security filters, method security, interceptors, and gateway controls.
- Inspect Feign/HTTP/gRPC clients, LDAP templates, messaging listeners/producers, repositories, migrations, and scheduled handlers.
- Trace inbound requests or events through services to data access, outbound calls, and emitted messages.
- Trace client construction separately from callsites and lifecycle activation.
- Inspect profiles, conditional beans, feature flags, reflection, transactions, and proxies before describing activation.
- Identify startup hooks, schedulers, request handlers, transaction callbacks, retries, and shutdown hooks.
- Keep schema declarations, migration activation, and application datasource use separate.

## Other stacks and deployment configuration

Use equivalent framework entrypoints and client patterns for other languages.
Inspect source imports and callsites before treating an installed library as a runtime relationship.

- Inspect YAML/JSON/TOML/XML/properties/INI configuration, profiles, imports, arguments, and environment variable references.
- Inspect Compose, Kubernetes, Helm, Kustomize, Terraform, ingress, service meshes, and network policies when available.
- Inspect OpenAPI, AsyncAPI, GraphQL, Protobuf, WSDL/XSD, Avro, migrations, and payload schemas.
- Inspect package locks, native bindings, binaries, container bases, CI runners, artifact stores, and test-service configuration.
- Trace nonsecret configuration keys to consumers and external injection references.
- Preserve missing external settings, unresolved precedence, substitutions, and deployment overrides as limits.

## Contracts and cross-repository relationships

Prefer inspected source, configuration, and versioned contracts over unsupported documentation claims.
Keep declaration evidence separate from implementation, deployment configuration, and retained runtime observations.
Confirm a relationship across repositories only when evidence from both boundaries supports it.
An authoritative contract can support a declared relationship within its stated scope.
Otherwise preserve the peer or relationship as a candidate with explicit limits.

Record the actual protocol, operation, direction, broker/datasource binding, profile, and environment when evidence provides them.
Use the profile's family keys from [the evidence contract](readiness-and-evidence.md).
Do not restrict discovery to canonical catalog contract types.
Record gRPC, LDAP, and other unsupported catalog mappings in the assessment.
Include service identities only when confirmed; repository IDs do not establish service identities.
Equal names do not establish shared endpoints, brokers, queues, topics, databases, or runtime connectivity.

## Sensitive data and execution

Exclude credentials, secret values, customer data, directory entries, trading data, key stores, generated bundles, and large logs.
Record secret mechanisms and nonsecret key names through safe references without opening credential files.
Treat `.env*` and mounted secret contents as unavailable unless authorized inspection can preserve sensitive-data boundaries.
An unavailable file needs an explicit coverage limit; do not silently count it as inspected.

Use approved source access and tooling.
Do not disclose source to unrelated services.
Do not run installers, builds, runtime tests, migrations, database probes, or network calls without authorization covering that execution.
Filename inventory and static evidence validation do not execute target code.
