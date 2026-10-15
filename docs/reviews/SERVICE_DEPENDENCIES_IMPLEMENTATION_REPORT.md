---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
implementation_status: IMPLEMENTED_WITH_LIMITS
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
  - Static source declarations do not establish runtime execution.
  - Semantic recall and reviewed precision remain UNKNOWN outside reviewed source subsets.
  - Browser policy blocked visual inspection of the local viewer.
---

# Service dependency graph implementation and comparison

Report date: 15 October 2026.
The [canonical skill](../../.agents/skills/service-dependencies-graph/SKILL.md) now extracts more dependency forms and exposes complete filtered indexes.
The [coverage plan](SERVICE_DEPENDENCIES_COVERAGE_PLAN.md) remains the historical planning record.
This report records implementation results and remaining limits.

## Scope and risk

Changes cover skill extraction, source discovery, coverage audits, validation, projections, queries, visualization, guides, and regressions.
Workbench adapters remain thin.
Business source and the parent's published graph remain unchanged.
Generated local graphs remain outside Git.

Qualitative risk is high for identity matching and evidence sanitization.
Focused positive, negative, ambiguous, and dynamic fixtures check those boundaries.
Static declarations cannot establish deployed connectivity or executed business behavior.

## Snapshot comparison

The [comparison evidence](../evidence/service-dependencies-implementation-comparison.json) records hashes, source fingerprints, revisions, exclusions, and per-repository counts.
Repository counts below describe repositories with graph facts.
The former local census also included an inventory-only test repository.

| Snapshot | Repositories | Nodes | Relationships | Evidence |
| --- | ---: | ---: | ---: | ---: |
| Local before enhancement | 8 | 961 | 1,413 | 1,452 |
| Parent published graph | 13 | 2,456 | 4,259 | 5,122 |
| Enhanced local graph | 9 | 6,555 | 16,997 | 16,515 |
| Enhanced skill with parent source | 13 | 10,715 | 26,157 | 46,253 |

An isolated parent harness build reproduced the published parent's category counts on the inspected parent source.
The enhanced skill then processed that same source set.
This comparison separates extractor changes from differences between local and parent repositories.
Record totals alone do not measure semantic coverage.

The local graph contains 6,135 production nodes and 12,669 production relationships.
It separately contains 420 testing nodes and 4,328 testing relationships.
The viewer selects production scope initially.

## Implemented detail

| Area | Result | Evidence boundary |
| --- | --- | --- |
| Source discovery | Declared Maven modules and literal custom roots now participate. | Dynamic, excluded, missing, and escaping roots retain diagnostics. |
| Java structure | Types, imports, inheritance, injection, and bounded typed calls retain source evidence. | Interfaces retain dispatch ambiguity. |
| Configuration | Keys, sources, bindings, reads, references, and profile context remain separate. | Values and defaults stay excluded; profiles remain unselected. |
| HTTP | Typed RestTemplate calls support literal, constant, initialized, and symbolic destinations. | Unknown authority or destination prevents provider resolution. |
| Web structure | Relative imports, aliases, barrels, exports, and symbols retain exact identities. | Type-only imports cannot establish value use. |
| GraphQL | Documents retain partial operation and selection metadata when source permits. | Documents cannot establish transport calls or resolver bindings. |
| Storage | JPA mappings and supported SQL references include tables, columns, and reference roles. | Mapping declarations cannot assert executed reads or writes. |
| Testing | Selected Python integrations and Robot imports retain testing scope. | Extraction neither executes tests nor proves passing behavior. |
| Coverage | A checksum-backed declaration audit exposes fingerprints, parse results, dispositions, and independent markers. | Parse success and marker accountability cannot establish semantic recall. |

The [declaration audit](../../relationships/service-dependencies/generated/coverage-declarations.json) contains these reviewed local targets.
Repeated declarations can merge into fewer canonical relationships.

| Reviewed target | Result |
| --- | --- |
| Java files | 194 files have parse and extraction dispositions. |
| Direct RestTemplate callsites | All 20 callsites retain canonical call evidence. |
| Configuration classes | All 17 classes retain binding evidence. |
| Configuration field bindings | 103 bindings retain source evidence. |
| Configuration reads | 123 source reads produce 111 canonical relationships. |
| HTTP configuration chains | 12 endpoint-expression links retain relevant getter evidence. |
| BFF entities | Seven entities retain table mappings and repository bindings. |
| Column annotations | All 28 annotations retain mappings; 14 retain unknown physical names. |
| GraphQL documents | All 36 documents retain partial metadata and dynamic limitations. |

The BFF Storage view exposes 16 tables, 56 columns, eight read relationships, and seven entity mappings.
Seven tables retain prior access evidence; seven represent logical ORM mappings; two represent SQL declaration targets.
These categories do not establish 16 executed table accesses.
No Kafka declarations occur in the reviewed local Java subset.
Local Kafka recall therefore has no positive reviewed denominator.

## Viewer hierarchy and access

Highest shows confirmed, resolved links between repositories.
Medium shows individual APIs, messages, storage, configuration, components, and uncertain boundaries.
Lowest shows package declarations.
These levels describe navigation depth; they do not assign business criticality.

The viewer includes legends, status explanations, repository slices, dimensions, scope selection, search, filters, and sorting.
Every matching node and relationship remains accessible through complete indexes and diagram pages.
Each diagram page contains at most 36 nodes and 48 relationships.
Focused neighborhoods include isolated nodes.
Inspectors retain canonical properties and source evidence.

An actual-data JavaScript audit reached all 16,623 non-package relationships across 614 pages.
The package view separately reached all 374 package relationships.
Interaction fixtures checked filtering, inspection, pagination, and testing scope.
Browser policy blocked visual inspection of the local file URL.
These interaction checks do not establish visual layout quality.

## Reference retention and corrections

The [identity reconciliation](../evidence/service-dependencies-identity-reconciliation.json) explains every removed reference record.
Exact ID retention covers 2,442 of 2,456 nodes and 4,244 of 4,259 relationships.
It also covers 5,096 of 5,122 evidence records.
Thirteen REST operation identities changed after query-value normalization.
Their call relationships retain corresponding normalized targets.
Twenty-four REST evidence records have sanitized replacements at matching source locations.

The old parser also interpreted GraphQL interpolation `$` as an operation name.
The correction removes that false operation, two merged call relationships, and two evidence records.
Valid named operations retain their identities.
These changes explain the lower GraphQL call count.

The enhanced parent-source graph preserves all 175 exposed APIs and the original messaging and database access families.
It preserves 46 publish, 52 consume, 54 topic-configuration, 79 read, and 75 write relationships.
All original 73 table identities and package relationships remain represented.
More nodes cannot compensate for unsupported declarations.

## Findings and next actions

| Finding | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| Nine parent backend repositories are absent locally. | Comparison evidence, `parent_only_repositories` | Their APIs, Kafka usage, and database details cannot appear as local provider facts. | Workspace maintainer; person UNKNOWN | Register or map available provider checkouts when scope requires them. |
| Dynamic destinations remain unresolved. | Declaration audit and graph diagnostics | Static source cannot establish concrete providers or deployment routes. | Repository owners UNKNOWN | Supply authoritative environment and provider evidence before resolving identities. |
| Local GraphQL documents remain partial. | 36 document audit records | Runtime selections and wrapper providers can prevent complete operation extraction. | UI owners UNKNOWN | Review dynamic construction and seven unresolved wrapper providers. |
| Five source files have parse errors. | Declaration audit, file parse states | Dependencies inside affected syntax can remain incomplete. | Repository owners UNKNOWN | Review four web files and one testing Python file. |
| Parent column markers expose additional gaps. | Parent declaration audit, independent source candidates | The enhanced comparison still lacks mapping evidence for 256 column markers. | Skill maintainer; person UNKNOWN | Review framework and annotation forms before extending mapping support. |
| Global semantic denominators remain unknown. | Coverage query and repository audit measures | No defensible whole-codebase recall or precision percentage exists. | Skill maintainer; person UNKNOWN | Extend independent semantic reviews by dependency family. |
| Visual review remains incomplete. | Browser policy refusal and JavaScript audit | Layout quality lacks direct observation. | Skill maintainer; person UNKNOWN | Inspect the viewer when an authorized browser surface supports local files. |

The parent column gaps include 198 inherited `MappedSuperclass` fields and 48 Spring Data relational annotations.
Another ten use JPA columns within a Spring Data table class without `Entity`.
The current mapping extractor requires direct entity declarations and direct members.
The parent audit records these gaps; Java parse success does not remove them.

## Validation

The [validation evidence](../evidence/service-dependencies-implementation-validation.json) records actual results, commands, log hashes, and audit outputs.
The runtime suite passes, and the skill suite passes.
Both graph builds and their projections pass validation.
The coverage query reports `CURRENT` source freshness.
Workspace validation and skill metadata validation pass.

The isolated wheel workspace includes executable skills, schemas, templates, and responsibility guides.
Its graph build and workspace validation pass without the parent harness.
The required isolated build command could not fetch build dependencies through the restricted network.
The offline wheel build passed with installed build tools and `--no-build-isolation`.
Automated writing checks remain separate from the pending ASD review.
