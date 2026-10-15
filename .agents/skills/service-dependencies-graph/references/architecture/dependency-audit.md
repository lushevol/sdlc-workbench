# Dependency source audit

## Purpose

Find source dependency declarations that the generated graph does not represent.
Scripts must extract facts and retain source evidence.
AI can identify a missing syntax form and explain its effect.
AI must not add graph facts from naming or architectural expectations.

## Baseline

1. Run `./scripts/graph-build.sh` before the source review.
2. Read `analysis-report.md` and `analysis-coverage.json`.
3. Record the snapshot checksum, generation time, repository revisions, and source fingerprints.
4. Read `repository-relationships.json` and its unresolved boundaries.
5. Review all local repositories and manifest entries in the census.

The build reads local source.
It does not clone missing repositories or select active profiles.
The missing repository remains a coverage gap.

## Source comparison

Use the checked-in source inventory to exclude dependencies, generated files, tests, and build output.
Search source and configuration for these declaration families.
Inspect the enclosing declaration and its imports before assigning a dependency type.

| Family | Source declarations to inspect |
| --- | --- |
| HTTP clients | Feign mappings, Java URI calls, fetch, axios, client wrappers, and RTK Query base queries and endpoints |
| HTTP providers | Spring mappings, composed annotations, inherited mappings, and gateway routes |
| GraphQL | DGS and Spring GraphQL annotations, transport declarations, HTTP links, and GraphQL request base queries |
| WebSocket | SockJS, STOMP, WebSocket links, Spring endpoint registration, and nginx upgrade routes |
| Messaging | Kafka listeners, KafkaTemplate sends, ProducerRecord, topic headers, constants, configuration getters, and typed helper calls |
| Camel | Literal routes, getter-bound routes, dynamic endpoints, and input or publish direction |
| Build | Root and nested npm package manifests, Maven coordinates, dependency scopes, modules, parents, and profiles |
| Data access | Runtime database clients, ORM mappings, native queries, mapper XML, and explicit cache clients |
| External clients | Internal gRPC SDK calls, other gRPC clients, platform clients, file transfers, and external authorities |
| Application composition | SystemJS imports, MFE package identities, and nested source layouts |

For each reviewed declaration, select one result:

- Extracted: canonical evidence records its source path, line, dependency, and direction.
- Candidate: the graph retains a supported declaration, but the provider identity needs evidence.
- Unresolved: a diagnostic or boundary records the unsupported expression or missing identity.
- Coverage gap: the census records a missing repository, unsupported stack, or unscanned source layout.

Check false positives as well as missing declarations.
Check each unresolved canonical boundary in the relationship projection, including repository-owned file boundaries.
A runtime topic parameter is not a topic identity.
A package dependency is not a runtime service call.
A transport route is not handler execution evidence.
An external authority must survive path normalization.
Equal topic names do not prove a shared Kafka cluster.

## Repair loop

1. Save a minimal fixture for the observed syntax.
2. Add positive and negative cases for identity, ambiguity, and unsupported expressions.
3. Update extraction, resolution, validation, and projections as required.
4. Run the relevant fixture tests.
5. Run `./scripts/run-tests.sh` for shared graph or MCP behavior changes.
6. Run `./scripts/graph-build.sh` after the completed change set.
7. Compare the new evidence with the reviewed source declarations.
8. Inspect the published manifest and matching projections.

Keep both consumer and provider evidence on resolved links.
Keep dynamic caller values unresolved when bounded helper analysis cannot establish them.
Never hand-edit generated facts or checksums.

## Completion gate

Stop when every reviewed declaration has evidence or an explicit gap record.
Repeat the source comparison when a repair reveals another missing syntax form.
Report any unresolved dynamic values, source parse failures, nested layouts, and missing repositories.
State the exact audit scope.
Do not report absolute dependency completeness.

Save the validation commands, results, snapshot identity, and remaining actions in the audit report.
Record automated output checks and ASD review separately.
