# Dependency discovery plan

> **The skill now uses two stages: collect snippets, then connect their meaning.**
> Scripts search available files. The active agent traces internal and external service calls through source evidence.
>
> **No universal discovery guarantee follows from search patterns.**
> Action: review candidate decisions and explicit skips before claiming completion within a source boundary.
> Owner: Workbench maintainer; person unknown. Evidence: [discovery procedure](../../.agents/skills/service-dependencies-graph/references/architecture/snippet-discovery.md).

Date: 18 November 2026. Scope: service calls across available repositories, configuration, deployment files, and contracts.
This plan refines the [earlier graph maintenance](01-maintenance.md).
The [latest clarification](evidence/snippet-discovery-20261118/user-input.txt) prioritizes broad snippet searches, AI connection, flat repositories, and Solace.

## Exact earlier user input

Source: current Codex chat, 18 November 2026.

```text
please tell me your plan in plain expression on how many kinds of dependencies you will check, and how you guarantee to filter them all out, what's your filter rules/patterns.
```

## Stage one: collect broadly

Put repositories under one common parent. Use `build --repos PATH --layout flat` to scan each immediate repository directory.
Repository names and internal folder layouts do not determine the broad search scope.
The [file audit](../../.agents/skills/service-dependencies-graph/tools/discovery_sources.py) recursively accounts for text files without requiring particular extensions.
It includes hidden workflows, custom files, deployment inputs, tests, and generated client sources when no specific skip applies.
Typed parsers retain their separate language and source-root limits.

Repositories without typed extraction receive source-only anchors when readable text exists.
The agent can bind reviewed relationships to those anchors without inventing runtime services or providers.

Run three complementary searches over that same file inventory:

| Search | What it looks for | Why it matters |
| --- | --- | --- |
| Calls and handlers | Client creation, request methods, publisher calls, listeners, controller mappings, RPC stubs, and SDK methods. | Finds consumers and providers independently. |
| Destinations and bindings | URLs, hosts, configuration keys, broker settings, topics, queues, subscriptions, proxies, and service identities. | Connects symbolic calls to their possible destinations. |
| Contracts and client libraries | OpenAPI, AsyncAPI, GraphQL, protobuf, WSDL, imports, and package declarations. | Exposes indirect calls and frameworks without typed parser support. |

The [pattern scanner](../../.agents/skills/service-dependencies-graph/tools/extract_pattern_candidates.py) uses regular expressions and bounded source context.
Each candidate retains its pattern, file hash, source locations, sanitized snippets, and possible protocol or role hints.
Equal destination strings keep their separate callsite occurrences.
Comments and documentation remain candidates until source review determines their meaning.
Unknown receiver types and generic calls remain uncertain; the script does not invent a protocol or provider.

## Fourteen dependency groups

These groups organize coverage. They are not fourteen complete language parsers.
Service-to-service calls, including external services, receive primary attention.
Code and package relationships help connect their call chains.
Test and example relationships need separate scope labels during review.

| Group | What the searches collect | What source review must establish |
| --- | --- | --- |
| 1. HTTP and REST | HTTP clients, Feign, wrappers, fetch, axios, request methods, and exposed endpoints. | Caller, method, destination, path, and provider binding. |
| 2. GraphQL | Operations, schemas, clients, transport routes, and resolver declarations. | Transport destination and corresponding provider operations. |
| 3. Live connections | WebSocket, STOMP, streaming clients, subscriptions, and upgrade routes. | Connection target, message direction, and supported handler binding. |
| 4. Messaging | Solace/JCSMP/JMS clients, publishers, consumers, queues, topics, subscriptions, and request/reply calls. | Broker, message VPN, destination type, subscription, and handler direction. |
| 5. Databases | Database clients, queries, ORM mappings, tables, schemas, and datasource settings. | Actual access declaration and database identity where available. |
| 6. Caches and shared state | Redis clients, cache operations, configuration, and shared storage clues. | Client operation, target, and shared-instance evidence. |
| 7. Directories | LDAP and JNDI clients, context acquisition, authentication, and directory operations. | Directory operation and available endpoint identity. |
| 8. RPC and remote SDKs | RPC clients, channels, stubs, remote methods, SDK wrappers, and protocol contracts. | Service, method, channel destination, and provider contract. |
| 9. Frontend composition | Remote imports, microfrontend registration, layouts, import maps, and module loading. | Exact module identity and supported registration or loading chain. |
| 10. Code structure | Imports, injected clients, wrappers, functions, classes, and internal calls. | How local code reaches the remote operation. |
| 11. Shared packages | npm/Maven declarations, library imports, publishers, modules, and scopes. | Library identity and whether source actually invokes its client. |
| 12. Traffic routing | Nginx, gateways, ingress, proxies, rewrites, DNS references, and service discovery. | Each declared forwarding hop and its unresolved deployment values. |
| 13. Configuration and deployment | Environment reads, properties, manifests, profiles, broker settings, and deployment bindings. | How an operation obtains its destination without selecting unknown active values. |
| 14. Files and shared storage | File operations, transfer clients, shared paths, object storage, and network storage clues. | Access direction, remote storage identity, and available protocol evidence. |

Solace is the stated future messaging direction. Its patterns collect candidates for AI investigation.
Generic JMS and `publish` or `send` calls do not prove Solace use without imports or configuration.
Existing Kafka/Camel declarations remain evidence when current sources contain them.
The future preference does not rewrite current implementation evidence.

## Stage two: connect the snippets

The active agent follows each possible service call through the available source:

```text
Caller handler or job
  -> local helper or shared SDK
  -> client operation
  -> configuration, constant, or destination expression
  -> gateway or broker hop, when present
  -> internal service endpoint or external authority
  -> receiving handler or reply path, when available
```

Use `patterns` with `service_only: true` and `include_snippets: true` for the primary review batch.
Generic `CALL_HINT` candidates stay in that batch because wrappers and publisher calls can hide their protocol.
Use literal `query` searches to find the same symbol, destination, configuration key, or imported client elsewhere.
Retrieve supporting imports and package declarations without the service filter when needed.
Follow every `next_offset` within the same manifest checksum.
Matching canonical evidence and node references help reopen the corresponding graph neighborhood.

The agent applies these review rules:

1. Distinguish actual calls from imports, interfaces, comments, examples, and unused settings.
2. Follow wrappers and imported clients before interpreting their arguments or protocol hints.
3. Trace destination expressions into constants, environment reads, properties, routes, or persisted metadata.
4. Find providers independently. Require exact identity and compatible operation evidence before joining repositories.
5. Keep gateway, SDK, and broker hops visible. Do not replace an unproved hop with a plausible direct call.
6. Keep external targets visible even when their implementation source is unavailable.
7. Match broker and message VPN evidence before joining publish and subscribe paths. Topic or queue names alone are insufficient.
8. Keep production, tests, examples, package declarations, and runtime calls distinct.
9. Sanitize credentials and sensitive values. Preserve useful symbols, destination structure, source references, and uncertainty.
10. Reuse canonical edges when their meaning matches. Save additional reviewed relationships through the existing context contract.

Each reviewed candidate receives one outcome: a supported call, supporting evidence, an unresolved boundary, or an irrelevant match with rationale.
Unsupported syntax requires source inspection or an extractor repair with a regression.
Missing identity never authorizes a guessed provider.

## Coverage assurance and limits

The implemented broad audit records scanned files and explicit skipped files or subtrees.
Skip reasons include Git metadata, dependency installations, recognized build caches, symlinks, binary data, unreadable files, and oversized text.
The current text limit is two megabytes per file.
A skipped subtree represents excluded scope; its files do not count as individually inspected sources.
Review those exclusions when they could contain an integration.

File hashes bind candidate snippets to source bytes. Publication checks source inventories before and after generation.
A source change stops publication and preserves the previous bundle.
Old snapshots without broad discovery hashes retain an explicit discovery-freshness limit.

[Inventory fixtures](../../.agents/skills/service-dependencies-graph/tests/test_discovery_sources.py) check custom paths, hidden files, encodings, skips, and source changes.
[Pattern fixtures](../../.agents/skills/service-dependencies-graph/tests/test_pattern_candidates.py) check representative search forms and sensitive-value handling.
[Query fixtures](../../.agents/skills/service-dependencies-graph/tests/test_service_snippets.py) check snippet retrieval, filters, pagination, checksums, and legacy compatibility.
Fixtures demonstrate those cases. They do not prove complete recall across unknown code.

Inspect unmatched callers, unmatched providers, disconnected repositories, unsupported languages, and remaining candidate decisions.
Read source beyond known pattern matches because unknown syntax can produce no match.
Add a pattern when inspected source reveals an omission. Rebuild and repeat the affected searches.
Claim reviewed-scope completion only when all included files and candidates have traceable dispositions.
An automated `RECORDED` label does not establish semantic review.

No universal guarantee can cover unavailable code, reflection, arbitrary syntax, or runtime-only configuration.
The practical guarantee is complete accounting for the declared file boundary and honest reporting of unfinished review and unresolved links.
No final test count or semantic-completion result forms part of this plan.

## Output review

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not establish complete writing review.
  - Pattern matches and fixtures do not establish complete semantic recall.
```
