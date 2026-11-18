# Dependency discovery plan

Date: 18 November 2026. Status: proposed checks; implementation remains partial.
Scope: service dependencies across available repositories, configuration, and deployment sources.
This maintenance plan follows the [completed refinement](01-maintenance.md).

> **Complete discovery is not established.**
> The plan requires complete file accounting and reviewed candidate decisions within a recorded source boundary.
> Owner: Workbench maintainer; person unknown. Next action: audit source exclusions before processing remaining candidates.

## Exact user input

Source: current Codex chat, 18 November 2026.

```text
please tell me your plan in plain expression on how many kinds of dependencies you will check, and how you guarantee to filter them all out, what's your filter rules/patterns.
```

## Fourteen dependency groups

These groups organize review. They do not claim universal parser support.
Test dependencies receive separate scope labels across these groups.

| Group | What to find | Current limit |
| --- | --- | --- |
| 1. HTTP and REST | Clients, wrappers, exposed endpoints, Feign, fetch, axios, and Java HTTP calls. | Arbitrary wrappers and dynamic destinations require investigation. |
| 2. GraphQL | Client operations, schemas, transport routes, and resolver declarations. | Schema names alone cannot connect clients to providers. |
| 3. Live connections | WebSocket, STOMP, streaming clients, and upgrade routes. | The skill extracts selected WebSocket forms; generic streaming needs review. |
| 4. Messages and events | Producers, consumers, topics, queues, browser messages, and interoperability calls. | Kafka/Camel has selected extractors; browser and other messaging needs review. |
| 5. Databases | Queries, ORM mappings, repositories, tables, schemas, and datasource bindings. | Dynamic SQL and effective database identities remain limited. |
| 6. Caches and shared state | Redis clients, cache configuration, and shared browser storage use. | Redis has selected extractors; browser storage relationships need review. |
| 7. Directories | LDAP and JNDI directory operations. | Provider identities remain unknown without binding evidence. |
| 8. RPC and remote SDKs | Remote method calls, SDK wrappers, channels, and protocol contracts. | The skill extracts selected internal SDK calls; generic gRPC remains a gap. |
| 9. Frontend composition | Microfrontend registration, remote loading, layouts, and import maps. | The skill extracts selected SystemJS and Single-SPA chains. |
| 10. Code structure | Imports, injected services, inheritance, implementations, and internal calls. | The skill extracts selected Java and web structures. |
| 11. Shared packages | npm/Maven dependencies, publishers, nested modules, and dependency scope. | Transitive dependencies and effective build models remain limited. |
| 12. Traffic routing | Gateways, Nginx, ingress, DNS references, proxies, and service discovery. | Templates and deployment-selected identities can remain unresolved. |
| 13. Configuration and deployment | Environment reads, properties, profiles, manifests, and destination bindings. | Source declarations do not select active deployment values. |
| 14. Files and shared storage | File clients, shared paths, transfer clients, and object storage. | The skill extracts selected Java file operations; transfers and storage protocols need review. |

## Candidate search rules

The current [pattern scanner](../../.agents/skills/service-dependencies-graph/tools/extract_pattern_candidates.py) supplies seven broad search families.
The [typed extractors](../../.agents/skills/service-dependencies-graph/references/architecture/automated-analysis.md) inspect supported code structures independently.
Search matches start an investigation. They do not become confirmed graph relationships automatically.

| Search family | Current examples |
| --- | --- |
| Endpoint strings and calls | `https://`, `wss://`, selected rooted paths, `fetch(...)`, `axios(...)`, and selected HTTP method calls. |
| Configuration access | `process.env.NAME`, `import.meta.env.NAME`, `System.getenv(...)`, `@Value(...)`, `${key}`, and environment key declarations. |
| Message channels | `@KafkaListener`, selected Kafka sends, and Camel `kafka:` routes. |
| Database tables | `SELECT ... FROM`, `INSERT INTO`, `UPDATE`, and `DELETE FROM`. |
| Module imports | Selected `import`, `require(...)`, and `System.import(...)` forms. |
| Gateway routes | `location`, `proxy_pass`, `rewrite`, and `upstream`. |
| GraphQL contracts | `.graphql`, `.graphqls`, and `.gql` files. |

These patterns have literal, file, and expression limits.
They cannot alone establish complete coverage of the fourteen review groups.
Extend independent searches for directory, cache, file, RPC, browser, and infrastructure mechanisms where the existing search misses declarations.
Trace imports, receiver types, enclosing functions, wrappers, constants, and configuration chains before assigning a relationship.

## Filtering and matching rules

1. Keep actual calls and supported declarations. Keep comments, example strings, and unrelated identifiers out of confirmed runtime relationships.
2. Resolve imported types and binding scopes. Reject shadowed framework names, replaced loaders, and unknown mutations as provider proof.
3. Keep package dependencies and runtime calls distinct. A manifest entry establishes package use without proving a service invocation.
4. Require evidence from both endpoints before joining repositories. Match exact identities, protocols, HTTP methods, paths, and supported routing transformations.
5. Retain host and environment uncertainty. Equal paths, topic names, tables, or similar package names cannot establish common providers.
6. Preserve unknown destinations as visible boundaries. Dynamic configuration, duplicate providers, and missing sources must not disappear during filtering.
7. Remove credentials and query values from retained graph evidence. Preserve useful paths, source locations, and unresolved binding reasons.
8. Deduplicate repeated findings without losing their source references. Keep production and test dependency scopes distinct.

Every candidate needs a recorded outcome:

- A supported relationship with exact source evidence.
- A declared boundary with missing or ambiguous provider identity.
- An unsupported form requiring source investigation or extractor repair.
- A rejected candidate with a source-based reason.

## File coverage and completion

First compare a complete repository file inventory with the current included-source inventory.
Record each included file, excluded file, unreadable file, and unsupported format with its reason.
Review hidden directories, symlinks, generated clients, and test exclusions before accepting their exclusion from the relevant scope.

The current [source policy](../../.agents/skills/service-dependencies-graph/tools/source_inventory.py) omits unsupported names and suffixes.
It can exclude `Dockerfile`, `Makefile`, shell scripts, Terraform, templates, and hidden workflow directories.
The pattern scanner also skips most JSON files and files larger than two megabytes.
An independent complete file audit is proposed here. It is not implemented by the completed refinement.

Inspect clients and providers independently across every included repository and review group.
Review source beyond pattern matches because unknown syntax can produce no match.
Trace newly discovered endpoints and repair proven omissions with positive and negative regressions.
Repeat discovery after repairs. Keep source hashes stable throughout the comparison.

Claim reviewed-scope completion only when every file and candidate has a recorded disposition.
No unreviewed files or candidates may remain within that claim.
An automated `RECORDED` label does not establish semantic review.
Any unresolved boundaries, unavailable bindings, and unsupported semantics remain explicit limits.
Unresolved boundaries cannot count as resolved dependencies.

The [last completed census](evidence/autonomous-discovery-20261118/graph-validation.json) contains 9,790 candidates requiring semantic review.
That count does not measure missing dependencies. Reviewed-scope completion has not been reached.
Unknown code, reflection, and unavailable runtime configuration prevent a universal discovery guarantee.

## Output review

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not establish complete writing review.
  - Proposed coverage checks are separate from implemented extraction support.
```
