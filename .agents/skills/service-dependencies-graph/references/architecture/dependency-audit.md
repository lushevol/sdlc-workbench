# Dependency source audit

## Purpose and baseline

Find source dependency declarations missing from the graph.
Scripts extract facts and retain evidence.
Source review identifies unsupported syntax and false positives.
Do not add graph facts from names or architectural expectations.

Run the local skill build command before source comparison.
Read coverage, repository relationships, and unresolved boundaries.
Record snapshot identity, generation time, repository revisions, dirty states, and source fingerprints.
Review all census entries, including unsupported and missing repositories.

The build reads local source without cloning or selecting active profiles.
Missing repositories remain coverage gaps.
Read the [implemented analysis](automated-analysis.md) before claiming syntax support.

## Source comparison

Use source-inventory exclusions when selecting files.
Inspect enclosing declarations, imports, and configuration bindings before assigning a dependency type.

| Family | Declarations to inspect |
| --- | --- |
| HTTP clients | Feign, Java URI calls, fetch, axios, wrappers, and RTK Query. |
| Providers | Spring mappings, inherited/composed annotations, and gateway routes. |
| GraphQL | Selected resolver annotations, transport routes, client links, and request base queries. |
| WebSocket | SockJS/STOMP construction, Spring registration, and upgrade routes. |
| Messaging | Kafka listeners/sends, topic headers, constants, configuration getters, typed helpers, and Camel routes. |
| Build | Root/nested npm manifests, Maven coordinates, scopes, modules, parents, and profiles. |
| Data | Runtime clients, ORM mappings, native queries, mapper XML, and explicit cache clients. |
| External | Selected SDK calls, platform clients, file operations, and external authorities. |
| Composition | SystemJS imports, exact ES value imports, MFE package identities, and source layout. |
| Infrastructure | Static nginx locations, rewrites, proxy targets, upstream pools, and unresolved templates. |

For every reviewed declaration, record one result:

- Extracted: canonical evidence records source path, line, dependency, and direction.
- Candidate: a supported declaration needs corroborating provider identity.
- Unresolved: a boundary or diagnostic records unsupported syntax or missing identity.
- Coverage gap: the census records missing source, unsupported stack, or unscanned layout.

Check false positives and missing declarations.
A runtime topic parameter is not a topic identity.
A build package is not a service call.
A transport route does not establish handler execution.

External authorities must survive path normalization.
Equal topic names cannot establish shared clusters.
Similar module names cannot establish aliases.
Unknown upstream addresses cannot establish concrete providers.

## Repair loop

Save a minimal regression for a confirmed defect under this skill's `tests/` directory.
Cover relevant positive, negative, ambiguous, and unsupported forms.
Update affected extraction, resolution, schema, and projections inside this skill.
Run the relevant skill tests.

```sh
python -m unittest discover -s .agents/skills/service-dependencies-graph/tests -v
```

Run broader workspace tests when adapters or packaging change.
Rebuild the snapshot after the completed change set.
Compare repaired evidence with reviewed source declarations.
Inspect the matching manifest and projections.

Keep both source endpoints on resolved joins.
Keep dynamic values unresolved when bounded analysis cannot establish them.
Never edit generated facts or checksums manually.
Update the skill's references when supported behavior changes.

## Completion

Complete the audit when every reviewed declaration has evidence or an explicit gap record.
Repeat source comparison when a repair exposes another missing syntax form.
Report reviewed protocols, layouts, unresolved values, owner, and next action.
Do not claim complete runtime dependency coverage.

Retain validation commands, results, snapshot identity, and remaining actions.
Keep automated checks separate from ASD review under the skill instructions.
