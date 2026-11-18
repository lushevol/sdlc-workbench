# Autonomous dependency discovery refinement

> **Human relationship hints are now optional.**
> The skill starts from available repositories and records source-backed relationships.
>
> **Complete semantic recall remains unproved.**
> Action: continue independent review of unresolved syntax and unavailable bindings when sources permit.
> Owner: Workbench maintainer; person unknown. Evidence: [comparison limits](evidence/autonomous-discovery-20261118/claim-comparison.json).

Date: 18 November 2026. Scope: graph skill maintenance and source-backed dependency discovery.

## Exact user input

Source: current Codex chat, 18 November 2026.

```text
Let's continue refining the service dependencies graph. \
\
In the last task, I provided some input based on my own understanding of the current dependencies between services. However, my expectation is that all graph and dependency relationships should be found and completed entirely through this skill. \
\
Therefore, based on my input, please refine, check for missing pieces, and analyze why this graph failed to find the corresponding dependencies. Our goal is to eliminate the need for any human input so that this skill alone can discover all the relationships.
```

## Scope and source baseline

Workbench baseline: `cad633b996d7c014837ca495aa9b27fb91f38916`.
Preserve pre-existing retrospective changes, deleted lockfile, and untracked release-report files.
Existing callers include the skill runner, Workbench graph adapter, snapshot queries, and viewer.
Change risk is medium: incorrect identity joins can create misleading cross-repository relationships.
Business repository sources remain read-only.

Use the [prior architecture input](../../knowledge/evidence/sources/user-clarifications/architecture-20261022/user-message.txt) as regression expectations.
Discover source declarations independently before comparing those expectations.
Inspect the [current skill](../../.agents/skills/service-dependencies-graph/SKILL.md), extraction, resolution, and coverage reports.

## Outcome and missing relationships

The source-only [comparison](evidence/autonomous-discovery-20261118/claim-comparison.json) accounts for all 23 historical expectations.
Source supports 17 expectations. One remains inferred. Five lack sufficient implementation, consumer, routing, or deployment evidence.
These five exclusions do not establish absent dependencies.

The investigation also found BFF directory access outside the original architecture notes.
The current [architecture context](../../relationships/service-dependencies/architecture-context.json) contains 19 relationships: 18 supported and one inferred.
Its 43 sources contain repository evidence only. No `USER_CLARIFICATION` source supplies a relationship or component identity.
Six investigations reuse canonical relationships instead of adding duplicate reviewed edges.

The [baseline](evidence/autonomous-discovery-20261118/baseline.json) records extraction without saved architecture context across 11 repositories.
The candidate retains nine directory operations, 29 uncertain HTTP call arguments, and nine symbolic Nginx upstream boundaries.
Single-SPA registration evidence now joins the existing Root Config to shell relationship independently of architecture notes.
These declaration counts do not measure deployed services or semantic recall.

## Why discovery failed

| Cause and evidence | Consequence | Correction | Owner |
| --- | --- | --- | --- |
| [Baseline workflow](evidence/autonomous-discovery-20261118/validation.json) centered investigation on supplied architecture hints. | Saved context supplied semantics beyond deterministic extraction. | Start with repository census, independent clients and providers, and all supported boundary families. | Workbench maintainer; person unknown |
| [Single-SPA extraction](../../.agents/skills/service-dependencies-graph/tools/extract_single_spa_layout.py) lacked the layout-to-loader registration chain. | Dynamic `System.import(name)` did not identify its bound literal application name. | Inspect framework imports, layout, loader, registration, mutations, and exact package identities. | Workbench maintainer; person unknown |
| [Directory extraction](../../.agents/skills/service-dependencies-graph/tools/extract_ldap_dependencies.py) lacked typed LDAP and JNDI operations. | Auth and BFF directory calls appeared only as generic Java structure. | Retain typed operations and unresolved directory platforms without guessing endpoint identity. | Workbench maintainer; person unknown |
| [Gateway extraction](../../.agents/skills/service-dependencies-graph/tools/build_graph.py) skipped every Jinja template. | Proxy routes disappeared despite explicit symbolic destinations. | [Parse template braces](../../.agents/skills/service-dependencies-graph/tools/extract_gateway_routes.py) and retain symbolic route boundaries. | Workbench maintainer; person unknown |
| [HTTP extraction](../../.agents/skills/service-dependencies-graph/tools/extract_web_interfaces.py) stopped at uninspected client routing. | Diagnostics lacked concrete graph declarations for the supplied call arguments. | Retain inferred `declared_path` boundaries. Exclude them from provider matching. | Workbench maintainer; person unknown |
| [Pattern queries](../../.agents/skills/service-dependencies-graph/tools/snapshot.py) lacked pagination. | Large candidate sets could not traverse the full denominator through queries. | Add compatible `offset` and `next_offset` fields. | Workbench maintainer; person unknown |
| [Context subjects](../../.agents/skills/service-dependencies-graph/tools/architecture_context.py) required human-reported or excluded labels. | Source-only discoveries could not identify their provenance honestly. | Add source-evidenced `SOURCE_REVIEWED` for investigated context. | Workbench maintainer; person unknown |

## Evidence boundaries

Discovery now requires no human relationship list. The active agent performs semantic investigation; the build remains deterministic.
The build does not invoke a model or refresh saved investigation decisions automatically.
The workflow repairs proven extractor omissions and preserves unsupported syntax, ambiguity, and unavailable sources.

Semantic recall and precision remain `UNKNOWN` across the complete source census.
This investigation reviewed the compared architecture claims and the added directory dependency.
It did not semantically adjudicate every independent search candidate.
Gateway-to-BFF configuration, universal backend SDK/Auth adoption, effective ingress DNS, and Auth Entra SPN delegation remain unproved.
Runtime-selected container metadata remains inferred.
Static evidence does not establish environment selection, shared credentials, deployment, or execution.

The previous context remains retrievable at the baseline revision and hash in the comparison.
The candidate moved into the existing context path. Later edits reused canonical edges; cited repository bytes remained unchanged.
The comparison records its former locator and current identity.
Business repository sources and canonical business knowledge remain unchanged.

## Verification and review

The [check results](evidence/autonomous-discovery-20261118/validation.json) retain commands, outcomes, source hashes, and material limits.
The [graph verification](evidence/autonomous-discovery-20261118/graph-validation.json) records matching source inventories and current snapshot freshness.
The [distribution result](evidence/autonomous-discovery-20261118/distribution.json) records wheel verification through its [reproducer](evidence/autonomous-discovery-20261118/verify-distribution.py).

All 242 graph tests passed. The final repository run completed 1,110 tests without failures or errors.
Two optional connector integration tests remained disabled. Their skipped status does not establish connector execution.
Workspace validation, skill validation, link checks, diff checks, and offline wheel distribution checks passed.

The graph suite checks positive declarations, unknown identities, ambiguous providers, source freshness, and publication recovery.
Negative cases cover shadowed loaders, mutable registration objects, uncertain HTTP routing, template/static collisions, and URL sanitization.
Source-only context tests require no human clarification source. Query tests traverse complete paginated fixture results.

Final independent review found option overrides and generic type shadowing that could create false relationships.
Unknown Single-SPA option overrides now remain unresolved. Java generic parameters suppress LDAP recognition within their declared scope.
Both corrections have negative regressions. Genuine imported LDAP calls outside the generic scope still extract.

The first full suite hit 38 sandbox errors while binding local test servers.
The authorized loopback runs include the final sanitization regression.

The initial wheel command attempted build-tool downloads. Offline building uses the existing installed tooling.
An initial viewer test expected old label wording. The updated assertion checks context labels and reviewed assessments.

The distribution probe initially rejected guide directories. Corrected assertions exclude runtime source while permitting responsibility guides.

The final pattern census contains 13,069 search candidates; 9,790 require independent semantic review.
These are search results, including unsupported or non-runtime syntax. They are not counts of missing dependencies.

## Current documentation

Updated the [skill](../../.agents/skills/service-dependencies-graph/SKILL.md), [source discovery workflow](../../.agents/skills/service-dependencies-graph/references/architecture/initial-instruction-investigation.md), and [context contract](../../.agents/skills/service-dependencies-graph/references/architecture/user-architecture-context.md).
Updated [automated extraction](../../.agents/skills/service-dependencies-graph/references/architecture/automated-analysis.md), [external boundaries](../../.agents/skills/service-dependencies-graph/references/architecture/external-boundaries.md), and [audit queries](../../.agents/skills/service-dependencies-graph/references/architecture/dependency-audit.md).
Updated [workspace design](../../docs/WORKSPACE_DESIGN.md#brownfield-adoption-boundary), [graph entry guide](../../relationships/service-dependencies/README.md), and [optional notes](../../relationships/service-dependencies/initial-instructions.md).
These guides distinguish source-driven skill operation, deterministic builds, reviewed semantics, and unavailable evidence.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not establish complete writing review.
```
