# Dependency source audit

Find dependency declarations missing from the generated graph.
Scripts extract facts and retain evidence.
Source review identifies unsupported syntax and false positives.
Do not add graph facts from architectural expectations.

## Establish the baseline

```sh
ai-sdlc --workspace PATH graph build
ai-sdlc --workspace PATH call service-dependencies coverage --args '{}'
```

Record snapshot identity, generation time, repository commits, dirty states, and source content fingerprints.
Review every census entry, including unsupported and missing repositories.
Inspect unresolved boundaries before source comparison.

## Compare source and output

Use the source inventory exclusions when selecting source files.
Inspect enclosing declarations, imports, and configuration bindings before assigning a dependency type.

| Family | Declarations to inspect |
| --- | --- |
| HTTP | Feign, Java URI calls, fetch, axios, RTK Query, Spring mappings, and gateway routes. |
| GraphQL and WebSocket | Client construction, static endpoints, annotated resolvers, STOMP registration, and upgrade routes. |
| Messaging | Kafka listeners and sends, constants, configuration getters, typed helpers, and Camel routes. |
| Build | npm manifests, Maven coordinates, scopes, modules, parents, and profiles. |
| Data | Runtime clients, ORM mappings, native queries, mapper XML, and explicit cache clients. |
| Composition | SystemJS imports, MFE package identities, import maps, and source layout. |
| Infrastructure | Static nginx routes, upstream declarations, rewrites, and unresolved template expressions. |

For each reviewed declaration, record extracted evidence, a candidate, an unresolved boundary, or a coverage gap.
Check false positives and missing declarations.
An external authority must survive URL normalization.
A package declaration does not establish a service call.

A transport route does not establish handler execution.
Equal topic names do not establish a shared cluster.

## Repair and complete

Save a minimal regression for a confirmed defect.
Cover the relevant positive, negative, ambiguous, and unsupported forms.
Update extraction, resolution, validation, and projections only where the defect requires changes.
Run relevant regressions, then the runtime test suite:

```sh
python -m unittest discover -s tests -v
```

Run tests from the standalone source checkout.
Generated workspaces contain no runtime tests.
Rebuild the graph after the completed change set.
Compare the repaired evidence with the reviewed declaration.

Do not hand-edit generated facts or checksums.

Complete the audit when every reviewed declaration has evidence or an explicit gap record.
Report reviewed protocols, source layouts, unresolved values, owner, and next action.
Do not claim complete runtime dependency coverage.
