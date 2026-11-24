# Spring Boot extraction

This guide preserves source-review targets from the imported procedure.
The [implemented analysis](automated-analysis.md) defines current supported forms and diagnostics.
Inspect declaring classes, imports, source lines, and configuration bindings alongside graph evidence.
Annotations and injected types do not establish runtime execution.

## Deterministic inventory

Inspect application roots, component scans, profiles, auto-configuration, bean declarations, and configuration properties.
Review inbound controllers, selected GraphQL resolvers, STOMP registration, filters, and security configuration when relevant.
Keep unsupported framework semantics explicit.
Static `open-apis` routes identify transport declarations within supported forms.

Inspect services, validators, persistence adapters, messaging, schedulers, integration clients, and internal Maven coordinates.
Constructor or field injection identifies a declared dependency without proving a call.
Profiles and conditions can select different beans.
Multiple candidates require resolution evidence.

Mixed manifests select Spring when `pom.xml` and `src/main/java` identify Java source.
An npm tooling wrapper does not replace that classification.
Nested Maven modules can remain outside runtime extraction.
Inspect coverage before interpreting SDK or generated-client dependencies.

## Providers and callers

Check direct controller declarations and class/method mappings.
Keep methods, path arrays, constants, and configuration-derived routes distinct.
Feign declarations identify callers and cannot become providers.
Composed annotations, inherited mappings, and dynamic constants need supported extraction or explicit gaps.

Context paths, content negotiation, and active profiles cannot be guessed.
Annotated GraphQL resolvers can identify selected root or nested fields.
Explicit GraphQL gateway routes establish transport ownership without field-level handler claims.
STOMP registration does not establish broker reachability or live subscriptions.

Feign identities require a unique provider alias.
URL overrides and alias collisions remain unresolved or ambiguous.
Java URI clients require supported literals or unambiguous constant evidence.
General receiver typing and compiler-level data flow remain outside supported claims.

Transaction annotations identify declared configuration.
They cannot establish actual proxy traversal, self-invocation behavior, or executed transaction boundaries alone.
Inspect relevant callers and tests when those semantics matter.

## Kafka and configuration indirection

Trace topics through supported constants, placeholders, configuration keys, and bounded typed helpers.
Keep dynamic caller values unresolved.
Configuration-only values cannot establish publication or consumption.
Equal topic names without shared cluster identity remain candidates.

Producer records and topic headers require supported topic binding evidence.
Ambiguous implementations, overloads, reassignment, and external helpers remain unresolved.
Camel getter bindings require exact configuration keys.
Generic file or HTTP channels cannot become Kafka through naming.

## Database and cache

Entity/table mappings identify associations and can remain inferred.
Literal framework table configuration cannot establish a concrete CRUD call.
Read/write claims require supported runtime client or query evidence.
Migration SQL establishes migration scope without runtime access proof.

Dynamic SQL, imported query constants, stored procedures, and ORM execution can remain unsupported.
Datasource names require identity evidence before shared-database joins.
Redis imports alone cannot establish cache dependencies.
Record secret keys as references, never values.

## Brownfield cautions

Profiles can change topics, datasources, routes, beans, and flags.
Do not select active variants without environment evidence.
Generated clients and shared starters can hide boundaries beyond supported root layouts.
Comments and documentation cannot establish active behavior.

Read [external boundaries](external-boundaries.md) for identity joins.
Use the [source audit](dependency-audit.md) for confirmed gaps.
