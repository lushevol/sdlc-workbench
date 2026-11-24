# Discover and connect service call snippets

Use this procedure when discovering internal or external service calls across repositories.
The script collects candidate snippets. The active agent connects their meaning through inspected source.
Prioritize who calls whom, the operation, transport, destination binding, and reply or event direction.
Package and internal code relationships support these call chains.

## Collect broadly

Supply the common repository parent through `build --repos PATH --layout flat`.
Flat repository directories require no `ui`, `services`, or other category names.
The flat option treats each immediate directory as a repository, including directories named `ui` or `services`.
The default `auto` layout preserves existing grouped workspaces.
Candidate discovery reads text files recursively, independent of extension and source-root layout.
Read discovery inventory skips before interpreting missing candidates.

Typed extractors retain their documented language and source-root limits separately.
Repositories without typed extraction retain a `SOURCE_ONLY` inventory anchor when readable text exists.
Bind reviewed findings through its explicit `node_id`; the anchor alone establishes no service or provider.

Use three complementary searches:

| Search | Examples | Purpose |
| --- | --- | --- |
| Call and handler syntax | HTTP clients, provider mappings, RPC stubs, message publishers, listeners, and SDK calls. | Find caller and provider code independently. |
| Destinations and bindings | URLs, host settings, broker properties, topic or queue names, route definitions, and service identities. | Connect symbolic calls to available destination evidence. |
| Contracts and client libraries | OpenAPI, AsyncAPI, GraphQL, protobuf, WSDL, package declarations, and imported client types. | Find indirect integrations and unsupported frameworks. |

Keep patterns in the existing scanner and its helpers. Each pattern records a stable identifier and dependency family.
Treat matches as candidates, including comments, documentation, examples, and unsupported languages.
Use surrounding code to reject false matches. A broad search cannot establish runtime invocation by itself.

Retain each occurrence when equal destination values appear at several callsites.
Snippets contain bounded, sanitized context and exact source locators. Reopen source when context is insufficient.

## Retrieve a review batch

Use the existing `patterns` operation with `service_only` and `include_snippets`.
Search related candidates with `query`, including calls outside the initial repository.

```sh
python .agents/skills/service-dependencies-graph/scripts/graph.py --workspace PATH query --data-dir relationships/service-dependencies/generated patterns --args '{"service_only":true,"include_snippets":true,"limit":5,"occurrence_limit":3}'
python .agents/skills/service-dependencies-graph/scripts/graph.py --workspace PATH query --data-dir relationships/service-dependencies/generated patterns --args '{"query":"destination-or-symbol","include_snippets":true,"limit":5,"occurrence_limit":3}'
python .agents/skills/service-dependencies-graph/scripts/graph.py --workspace PATH query --data-dir relationships/service-dependencies/generated patterns --args '{"candidate_id":"COPY_RETURNED_CANDIDATE_ID","include_snippets":true,"occurrence_offset":3,"occurrence_limit":3}'
```

Continue candidate pagination using `next_offset` within one manifest checksum.
Each candidate returns at most ten occurrences by default; `occurrence_limit` accepts one through 500.
Use small batches when requesting snippets.
Copy the candidate's `id` into `candidate_id` to retrieve that exact candidate.
Continue its occurrences using `next_occurrence_offset` until the value is null.
Each match retains its full `occurrence_count`, original `line`, and current `occurrence_offset`.

Canonical evidence links cover only the returned occurrence ranges.
Saved artifacts retain every occurrence; pagination limits query responses only.

The service filter prioritizes boundary candidates. Search supporting imports, package declarations, and configuration when tracing their bindings.
It includes generic `CALL_HINT` candidates so wrappers and publisher calls remain available for AI binding review.
It excludes standalone `MODULE_IMPORT` and `PACKAGE_DECLARATION` facts; retrieve those with `query` when following a call.

Protocol and role hints guide review. They do not prove receiver types, provider identity, or execution.
Canonical evidence at matching source locations can support the investigation without establishing semantic equivalence.

## Connect the snippets

For each caller, follow this chain where the source permits:

```text
Service A handler or job
  -> local helper or shared SDK
  -> client operation
  -> configuration key and available route binding
  -> Service B endpoint, broker destination, or external authority
  -> receiving handler or reply path, when available
```

1. Identify the calling function and its repository. Distinguish invocation from imports, interface declarations, examples, and unused configuration.
2. Follow imported wrappers and SDK methods. Read their arguments, HTTP method, serializer, destination construction, and relevant interceptors.
3. Trace destination expressions into constants, properties, environment references, routes, or persisted metadata.
4. Find providers independently. Compare exact service identities, HTTP authority/method/path, RPC service/method, or broker bindings.
5. Retain external targets even when provider source is unavailable. Label the external authority or unresolved platform explicitly.
6. Record direction, operation, transport, binding, source references, and missing links in the existing investigated context.

Reuse canonical edges when their endpoints and meaning match.
Use the [investigated context contract](user-architecture-context.md#investigated-contract-version-110) for reviewed relationships and exact source citations.
Keep different hops visible when a gateway, SDK, or broker separates caller and provider.
Unproved hops remain unresolved. Do not bridge them through similar names.

## Solace and asynchronous calls

Inspect Solace JCSMP, Java APIs, JavaScript clients, JMS, and Spring Cloud Stream bindings when present.
Look for session or service creation, producers, consumers, subscriptions, queues, topics, and request/reply APIs.
Trace broker host, message VPN, destination type, subscriptions, and configuration references.
Credentials stay outside graph evidence.

Represent publish/subscribe chains through their broker boundary:

```text
Service A -> publishes destination -> Solace broker/VPN -> subscription or queue binding -> Service B handler
```

Matching destination strings alone cannot prove a shared broker or message VPN.
A queue name does not establish its topic subscriptions.
Treat JMS and generic publish calls as protocol candidates until imports or configuration identify their provider.
Solace patterns collect snippets; they do not add a typed Solace execution model automatically.
Preserve existing Kafka declarations when sources contain them. Future platform preference cannot rewrite current implementation evidence.

## Review completion

Record whether each candidate establishes a call, supplies supporting evidence, remains unresolved, or is irrelevant with a reason.
Check unmatched providers, unmatched callers, disconnected repositories, and skipped discovery files.
Add patterns and regressions when source reveals a missed call form.
Rebuild after changes. Compare source hashes and repeat the affected searches.
Candidate counts and passing tests do not establish complete semantic recall.
