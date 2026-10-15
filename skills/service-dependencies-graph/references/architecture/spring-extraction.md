# Spring source review

Read [implemented analysis](automated-analysis.md) before assuming annotation or client support.
Inspect declaring classes, imports, configuration bindings, and source lines alongside graph evidence.
An annotation or injected type does not establish runtime execution.

## Providers and callers

Check direct Spring controller declarations and class/method request mappings.
Keep method, path arrays, literal constants, and configuration-derived route declarations distinct.
Feign declarations identify callers and cannot become providers.
Composed annotations, inherited mappings, and dynamic constants require supported extraction or an explicit gap.

Context paths and active profiles cannot be guessed.

Annotated GraphQL resolvers identify selected root or nested fields.
An explicit GraphQL gateway route can establish transport ownership.
It cannot establish field-level resolver calls.
Spring STOMP registration identifies a declared endpoint.

It does not establish broker reachability or live subscriptions.

Feign names and static service aliases require unique provider identity.
URL overrides and alias collisions remain unresolved or ambiguous.
Java URI-based clients require supported literal or unambiguous constant evidence.
General invocation typing and compiler-level data flow remain outside these static claims.

## Data and messaging

Trace Kafka topics through supported constants, configuration keys, and bounded typed helper calls.
Keep dynamic caller values unresolved.
Configuration-only topics do not establish publication or consumption.
Equal names without shared cluster identity remain candidates.

Camel getter bindings require an exact configuration key.
Do not classify generic file or HTTP channels as Kafka.

Entity/table mappings identify an association and can remain inferred.
Concrete read/write claims require supported runtime client or query evidence.
Migration SQL cannot establish runtime use.
Redis imports alone cannot establish a cache dependency.

Record credentials as key references, never values.

Use the [boundary review](external-boundaries.md) for cross-repository joins and the [source audit](dependency-audit.md) for extraction gaps.
