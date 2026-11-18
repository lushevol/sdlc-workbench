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

## Snippet discovery follow-up

Source: [exact user clarification](evidence/snippet-discovery-20261118/user-input.txt), 18 November 2026.
The user requests broad snippet discovery, followed by AI connection of service call chains.
Internal and external service calls take priority. Patterns must not depend on directory categories or source-root layouts.
The user will supply repositories under one flat parent. Solace replaces Kafka as the future messaging focus.

This clarification does not establish an executed messaging migration.

Scope: refine the existing scanner, source accountability, evidence queries, and source investigation guidance.
Risk: medium; broad searches can introduce false candidates or omit destination bindings.
Keep typed graph resolution and source investigation distinct. Preserve existing graph contracts and unrelated worktree changes.
Inspect extraction callers, snapshot readers, build publication, and source freshness before implementation.
The [discovery plan](02-discovery-plan.md) will track the current stage and verification.

### Implemented snippet workflow

The skill now collects broadly before the active agent connects service calls.
The content catalog provides 37 recognizers across 25 candidate families.
The [procedure](../../.agents/skills/service-dependencies-graph/references/architecture/snippet-discovery.md) covers three searches and source-backed call chains.
The [plan](02-discovery-plan.md) organizes fourteen dependency groups around internal and external calls.

Flat discovery preserves repositories named `ui` or `services` without requiring category folders.
The broad inventory includes hidden workflows, deployment files, tests, unusual extensions, and custom source layouts.
Source-only anchors let reviewed findings retain unsupported repository identities without inventing providers.
Solace/JCSMP/JMS patterns cover clients, destinations, bindings, and generic publisher or receiver calls.
Existing Kafka evidence remains available; this change performs no messaging migration.

The [actual graph check](evidence/snippet-discovery-20261118/graph-validation.json) records 6,928 scanned text files and 180 skipped entries.
The earlier pattern boundary scanned 2,904 files.
The new scan retains 105,489 candidates across 651,884 occurrences.
Those counts include tests, examples, documentation, and repeated calls. They do not count missing dependencies.

The investigated graph still contains 19 reviewed relationships from 43 repository sources.
No human relationship source supplies those bindings.

The expanded candidates have not all received semantic adjudication.
The graph therefore retains the existing supported relationships and exposes new candidates for source investigation.
No Solace protocol hints appeared in this captured corpus. That result cannot establish absence of every Solace integration.
The [file boundary](evidence/snippet-discovery-20261118/graph-validation.json) identifies excluded scope, including seven oversized files.
The current text limit remains two megabytes per file.

### Verification evidence

The [flat fixture](evidence/snippet-discovery-20261118/flat-discovery.json) checks custom paths, external authorities, Solace destinations, RPC contracts, and explicit skips.
Its [reproducer](evidence/snippet-discovery-20261118/verify-flat-discovery.py) confirms stale-source detection and publication preservation.
The [actual query probe](evidence/snippet-discovery-20261118/verify-graph.py) checks source hashes, freshness, and bounded occurrence pages.
Snippets retain sanitized context. The query returns ten occurrences per candidate by default and supplies continuation offsets.

Independent fixtures exposed inline RPC omissions and command credentials leaking into neighboring snippets.
Both defects have regressions. Credential sanitation preserves useful external URLs while removing recognized credential values.
Source-capture regressions reject temporary source revisions, including changes restored before final validation.

The [performance replay](evidence/snippet-discovery-20261118/performance.json) found repeated full-file line counting and linear occurrence checks.
Indexed line offsets and occurrence sets preserve source references while reducing the measured cost.
Previously timed-out files now complete within 1.04 through 1.98 seconds in those bounded replays.
The full audit remains approximately 481 MiB because every occurrence retains context.
Query pagination bounds returned snippets; it does not make the saved audit or its parsing small.

The [validation record](evidence/snippet-discovery-20261118/validation.json) lists final checks and remaining limits.
All 269 graph tests passed. The full suite completed 1,136 tests with two optional connector integration skips.
The [distribution probe](evidence/snippet-discovery-20261118/verify-distribution.py) checks an installed workspace outside this checkout.
It verifies flat custom-source discovery and snippet queries through the shipped skill.

## Current repository graph regeneration

Source: [exact user request](evidence/graph-regeneration-20261118/user-input.txt), 18 November 2026.
Authorized scope: regenerate the local repository graph with the current skill and saved investigated context.
Risk: low; generation replaces derived artifacts and keeps repository sources read-only.
The [run record](evidence/graph-regeneration-20261118/run.json) retains the command, previous snapshot identity, and final checks.

Generation passed graph, dependency, relationship, source-stability, and publication checks.
The published graph contains 11 repositories, 10,923 nodes, 25,137 edges, and 22,986 evidence records.
The published checksum matches its manifest. Current repository fingerprints match the captured inputs.
The [existing build guide](../../.agents/skills/service-dependencies-graph/SKILL.md#readiness-and-build) remains current for this repeated run.

## Remove the knowledge graph projection

Source: [exact user request](evidence/dependency-only-20261118/user-input.txt), 18 November 2026.
Authorized scope: remove knowledge graph generation, queries, schema, and viewer integration from the service dependency graph.
Keep the separate canonical knowledge and wiki capabilities outside this graph's implementation scope.
Risk: medium; affected consumers include graph builds, queries, CLI/MCP operation discovery, validation, viewer, and installed skills.
The [baseline](evidence/dependency-only-20261118/baseline.json) records the current projection before removal.
Next action: remove the integration, run affected regressions, regenerate the graph, and verify dependency-only output.

### Dependency-only outcome

The service graph now contains dependency relationships only.
Generation, schema validation, snapshots, comparisons, queries, resource grants, viewer rendering, and packaging exclude the former knowledge projection.
The separate canonical knowledge, governance, ingestion, and wiki tools remain outside this graph.

The rebuilt graph uses generator `2.6.0`.
It contains 11 repositories, 8,548 nodes, 22,142 edges, and 21,681 evidence records.
It contains no knowledge envelope, knowledge dimensions, knowledge evidence paths, or knowledge viewer interface.
The six supported operations are `coverage`, `patterns`, `relationships`, `services`, `search`, and `neighborhood`.
The retired `knowledge`, `references`, and `paths` operations return `UNKNOWN_OPERATION`.

The [graph validation](evidence/dependency-only-20261118/graph-validation.json) verified the published checksum, 66 artifact checksums, dependency schema, current repository freshness, and current architecture-context freshness.
The [distribution check](evidence/dependency-only-20261118/distribution.json) verified the installed skill outside this checkout.
It verified flat Solace discovery, bounded snippet pagination, and isolation from knowledge-file changes.
The [source review](evidence/dependency-only-20261118/source-review.md) refreshed two changed BFF source bindings and seven shifted endpoint ranges without changing relationship assessments.

The skill suite passed 241 tests.
The full Workbench suite passed 1,109 tests with two optional connector integration skips.
The package wheel built successfully and the workspace validator passed.
Automated documentation checks passed; complete ASD-STE100 review remains pending.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Static graph evidence does not establish deployment or runtime execution.
  - Broad discovery candidates still require source interpretation.
  - Automated checks do not establish complete writing review.
```

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not establish complete writing review.
```
