# Spring Boot Internal Extraction

This document describes extraction targets. The [implemented extraction guide](automated-analysis.md) lists the current supported forms and diagnostics; do not assume every feature below is implemented.

Use a Java parser/compiler model for declarations and calls plus parsed Spring configuration. Annotations are framework semantics, not text patterns; resolve composed/meta-annotations and constants when possible.

## Deterministic inventory

- Application/runtime: `@SpringBootApplication`, component scan, profiles, auto-configuration, `@Configuration`, `@Bean`, `@ConfigurationProperties`, `@Value`, conditional beans, discovery/client enablement.
- Inbound: `@RestController`, class/method request mappings, GraphQL `@QueryMapping`/`@MutationMapping`/`@SubscriptionMapping`, DGS `@DgsQuery`/`@DgsMutation`/`@DgsSubscription`/`@DgsData`, and `@SchemaMapping`, Spring STOMP `registerStompEndpoints` declarations, filters, interceptors, security chains, exception handlers. The implemented extractor also reads static `open-apis.apis` routing declarations.
- Domain/application: services, use cases, domain services, validators, mappers, transaction boundaries and propagation.
- Persistence: Spring Data repositories, JDBC templates, MyBatis/MyBatis-Plus mappers and XML, JPA entities/table mappings, native queries, cache annotations/clients.
- Async/integration: schedulers, batch jobs, event listeners/publishers, Kafka listeners/templates/producers, Camel routes, Feign clients, RestTemplate/WebClient/RestClient, GraphQL clients.
- Contracts: endpoint request/response DTOs, Kafka message/schema types, API specifications, internal Maven coordinates.

## Graph construction

Create explicit entry nodes and follow call/injection edges to semantic components:

```text
REST endpoint -> Controller -> Application/Domain Service -> Repository Adapter -> Table
Kafka topic -> Consumer -> Service -> Database
Scheduler -> Service -> Database -> Kafka topic
Service -> Feign/HTTP client -> External endpoint placeholder
WebSocket route -> STOMP endpoint -> Notification publisher
GraphQL operation -> Resolver -> Service
```

Constructor/field injection proves a dependency but not invocation. Emit `DEPENDS_ON` for injection and `CALLS` only for a call site. Interface-to-implementation mapping is `IMPLEMENTS`; link an injected interface to candidate beans using Spring resolution rules (`@Qualifier`, `@Primary`, profile/condition). Multiple active candidates are ambiguous variants.

Record `@Transactional` at class/method level, propagation, read-only, and the entry/exit component. Calls crossing proxies differ from self-invocation; do not claim a transaction boundary from an annotation on an unreachable or self-invoked method without noting the limitation.

## Endpoint resolution

Compose class and method mappings, HTTP method, path arrays, consumes/produces, context/server base paths, and gateway routes as separate facts. The implemented route join supports nginx `location`/`rewrite`/`proxy_pass` plus Spring `open-apis.apis` entrypoint/endpoint declarations. A Feign client such as a service-discovery name plus method mapping emits a client component and outbound interface; provider matching happens later. A resolved join retains the original unresolved boundary with candidate providers and adds a separate resolved provider edge.

Normalize service aliases case-insensitively where the discovery mechanism is case-insensitive, but preserve raw forms such as `RATAN-CASHFLOW-LIFECYCLE-SERVICE` and `ratan-cashflow-lifecycle-service` as aliases with evidence.

## Kafka and configuration indirection

Resolve topics and groups through constants, property placeholders, default values, `@ConfigurationProperties`, SpEL bean properties, Camel URIs, and deployment overrides. Preserve the expression and every environment value. Examples such as `${ratanone.topic.domain-events-inbound}` or `#{__listener.ssiEventTopic}` are not concrete topics until the binding is proven.

For `KafkaTemplate.send(record)`, trace the `ProducerRecord` topic; for `send(topic, key, payload)`, trace the topic argument. Conditional topic selection creates guarded edges per candidate topic. Capture serializer/schema/message type and key type when statically available.

## Database semantics

- Entity/table mapping proves an entity-to-table association, not read/write behavior. The extractor accepts positional and named `@Table` literals (`name` or `value`), including mappings without a scanned repository adapter; these rows remain inferred.
- Literal framework table configuration such as `.withTableName("...")` and `.tableName("...")` is retained as an inferred `FRAMEWORK_CONFIG` table declaration. It does not prove a concrete CRUD call.
- Repository method names and generic base types may support conservative CRUD inference; custom SQL/mapper operations provide stronger evidence.
- SQL `SELECT`, `INSERT`, `UPDATE`, `DELETE`, stored-procedure calls, and ORM operations determine `READS`/`WRITES` when the mapped table is resolved.
- Datasource/Flyway configuration proves connectivity/migration scope only.
- Dynamic table names, generic mappers, and native SQL fragments remain unresolved or inferred.

## Brownfield cautions

Profile files may change datasources, topics, routes, beans, and feature flags. Model variants rather than picking `application.yml`. Generated clients/shared starters can hide boundaries; emit the internal library dependency and inspect generated/API contracts when in scope. Comments, disabled annotations, unused beans, and README endpoint tables do not confirm active behavior. Schema-only GraphQL fields without an annotated resolver, reflection, AOP, BPMN/Camunda delegates, and scheduled configuration require dedicated extractors or explicit diagnostics. Camel `from(...)` and `getEndpoint(...)` values are directionally bound only when a Java getter matches an exact configuration key; `file:` and HTTP route values remain unresolved external boundaries.
