---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
implementation_status: PLANNED
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
  - Targets apply to reviewed source scope, not complete runtime dependency discovery.
  - Proposed acceptance criteria have not been implemented or executed.
---

# Service dependency graph coverage plan

Planning date: 15 October 2026.
Status: Proposed engineering work, without a business approval claim.

## Goal and ownership

Represent every discoverable dependency in the selected source scope with traceable evidence.
Expose unsupported declarations and missing identities beside the resulting graph.
Make every canonical record accessible through repository exploration.
Measure extraction quality separately from provider resolution and viewer visibility.

Engineers and agents use this graph for architecture discovery and change impact.
The expected benefit is fewer hidden API, configuration, messaging, shared-code, and data dependencies.
The implementation owner is the graph skill maintainer; the assigned person is unknown.
The source-scope owner is the workspace maintainer; the assigned person is unknown.

Keep extraction, resolution, schemas, reports, queries, visualization, and regressions inside the [canonical skill](../../.agents/skills/service-dependencies-graph/SKILL.md).
Keep Workbench CLI and MCP integrations as thin adapters.
Keep business repositories unchanged.
Use source mappings for existing checkouts when additional provider source becomes available.

This planning stage adds this document and its evidence record only.
It changes no extractor, graph contract, viewer, catalog, or generated snapshot.
The planning stage has low qualitative risk.
Implementation risks appear below.

## Evidence baseline

The [baseline evidence](../evidence/service-dependencies-coverage-baseline.json) identifies the inspected snapshots and source fingerprints.
The current [coverage artifact](../../relationships/service-dependencies/generated/analysis-coverage.json) records nine census entries.
Eight entries have graph roots; the test engine remains inventory-only.

| Finding | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| Rendering hides existing dependency families. | [Viewer selection](../../.agents/skills/service-dependencies-graph/tools/viewer.html), functions `setLevel` and `graphProjection` | BFF tables and reads disappear from its default diagram. | Skill maintainer, unknown | Restore complete repository exploration. |
| Evidence counts do not measure semantic recall. | [Coverage reporting](../../.agents/skills/service-dependencies-graph/tools/repository_reports.py) and [source audit](../../.agents/skills/service-dependencies-graph/references/architecture/dependency-audit.md) | A successful build cannot quantify missed declarations. | Skill maintainer, unknown | Establish independent reviewed denominators. |
| Nested Java source is omitted. | [SDK parent POM](../../repos/libraries/single-ui-sdk-starter/pom.xml) and coverage artifact | Twenty Java files receive no runtime extraction. | Skill maintainer, unknown | Discover declared modules and source roots. |
| Ordinary Java HTTP calls are omitted. | [HTTP parser](../../.agents/skills/service-dependencies-graph/tools/extract_java_http.py), constant `CALL` | Twenty reviewed callsites lack API representation. | Skill maintainer, unknown | Add typed calls and symbolic destinations. |
| Configuration bindings lack a general model. | Auth, BFF, and SDK source audit | Seventeen configuration classes lack binding-level coverage. | Skill maintainer, unknown | Model declarations, bindings, and reads separately. |
| JPA naming limits omit entity mappings. | [Table parser](../../.agents/skills/service-dependencies-graph/tools/extract_java_dependencies.py), function `table_annotation_name` | Seven BFF entities lack repository mapping coverage. | Skill maintainer, unknown | Preserve logical mappings and naming uncertainty. |
| Class detail depends on names and selected roles. | [Class selection](../../.agents/skills/service-dependencies-graph/tools/build_graph.py), function `ensure_java_detail_component` | Configuration and implementation classes collapse into groups. | Skill maintainer, unknown | Discover source roles and typed dependencies. |
| Parent providers are absent locally. | Identical-source comparison and repository census | Many service links lack provider evidence. | Workspace maintainer, unknown | Record included, missing, and excluded provider scope. |

Both generators passed graph validation against identical parent source.
The imported skill retained all 2,456 parent nodes, 4,259 relationships, and 5,122 evidence records.
It added five nodes, 38 relationships, and 44 evidence records.
These results establish extractor parity for that corpus, not completeness for other source forms.

The independently reviewed Java subset contains these targets:

| Source subset | Auth | BFF | Nested SDK | Total |
| --- | ---: | ---: | ---: | ---: |
| Eligible Java files | 70 | 104 | 20 | 194 |
| Direct RestTemplate callsites | 8 | 10 | 2 | 20 |
| ConfigurationProperties classes | 8 | 8 | 1 | 17 |
| Schema-only JPA entities | 0 | 7 | 0 | 7 |
| Explicit Column annotations | 0 | 28 | 0 | 28 |

These counts seed the audit; they are not complete dependency denominators.
The existing BFF graph already contains seven tables and eight read relationships.
Shared UI component counts match the parent for base, cashflow, and container.
Neither inspected snapshot models database columns or general configuration-key reads.

## Coverage measures and completion targets

Report each measure by repository, module, dependency family, and source scope.
Report the numerator, denominator, exclusions, audit status, and snapshot identity.
Use `UNKNOWN` when no reviewed denominator exists.
Use `N/A` when the reviewed denominator is zero.

| Measure | Definition | Proposed target |
| --- | --- | --- |
| Source discovery | Included eligible files and modules divided by independently inventoried files and modules | 100% for declared, supported roots; explicit gaps elsewhere |
| Parse coverage | Successfully parsed included files divided by included files requiring parsing | 100% or individually recorded failures |
| Declaration accountability | Reviewed declarations with canonical evidence or explicit dispositions divided by reviewed declarations | 100%; zero silent omissions |
| Semantic extraction recall | Correctly represented declarations divided by independently reviewed declarations | 100% for each implemented syntax corpus; remaining project gaps stay visible |
| Reviewed precision | Source-supported generated claims divided by reviewed generated claims | Zero known unsupported claims; disclose review sample size |
| Provider resolution | Evidence-supported joins divided by extracted boundaries requiring provider matching | Maximize supported joins; report missing source and dynamic identities separately |
| Viewer reachability | Accessible matching canonical records divided by matching canonical records | 100%, including isolated nodes |
| Reference retention | Retained reference relationships and evidence divided by the fixed reference baseline | 100%, except reviewed correctness changes |

An unresolved destination can accompany a correctly extracted call.
An explicit gap improves accountability but does not improve extraction recall.
Adding packages cannot compensate for missed runtime declarations.
Node totals, evidence-file totals, and `SCANNED` status cannot establish semantic coverage.

Retain a reviewed declaration ledger alongside generated coverage.
Record source identity, path, line or span, family, source form, disposition, canonical evidence, reason, owner, and next action.
Keep extraction disposition separate from provider resolution status.
Use independent source review to check both missed declarations and generated false positives.
Preserve previous audit evidence when source changes create a new baseline.

## Delivery sequence

### Stage 1: Establish measurable source coverage

Freeze graph and manifest identities, source fingerprints, revision availability, exclusions, and reference counts.
Inventory each repository, declared module, source root, manifest, configuration file, and parse failure.
Build the declaration ledger from reviewed source, starting with the audited subsets above.
Audit every existing extractor family, including UI wrappers, GraphQL, WebSocket, gateway routes, messaging, and platform clients.
Show coverage gaps in generated reports and queries.

Retain parent-only providers as missing or excluded source until the workspace scope includes them.
Account for all nine absent backend repositories without requiring their inclusion.
Keep the parent comparison optional and external to standalone operation.
Retain minimal reference fixtures for supported behavior inside the skill.

Exit: All census entries have explicit scope, and every reviewed declaration has a disposition.
Risk: Medium; incorrect denominators can create misleading coverage claims.

### Stage 2: Restore complete viewer exploration

Keep Highest for resolved system connections, Medium for repository detail, and Lowest for package declarations.
Add visible summaries for unresolved and external boundaries beside system connections.
Priority describes navigation depth; business criticality requires separate reviewed evidence.
Keep runtime and business dimensions independently selectable.

Provide repository views for APIs provided, APIs called, messages, storage, configuration, and components.
Index all owned nodes and relevant incident relationships within the selected dimension.
Include isolated nodes in search and inspection.
Enable ownership structure by default within the component view.

Replace degree-ranked truncation with expandable groups and focused neighborhoods.
Display matching, rendered, grouped, and omitted counts.
Retain complete indexes when rendering uses a limited budget.
Make every indexed item open its diagram neighborhood and evidence.
Preserve filters, legends, arrow meanings, and assertion and resolution statuses.

Restore component kinds, business meaning, source paths, and canonical properties in inspectors.
Show protocols, handlers, database access, clients, configuration expressions, and configuration paths when present.
Show an extraction gap distinctly from an inspected family with zero declarations.

Exit: Every matching canonical record is reachable, and category totals reconcile with the snapshot.
Risk: Medium; large repository views require grouping and visual checks.

### Stage 3: Cover source layouts and component identities

Traverse declared Maven modules and supported source roots before extraction.
Handle module exclusions, duplicate roots, cycles, and unavailable modules explicitly.
Preserve repository ownership while assigning module and symbol identities.
Use bounded source analysis; do not execute business builds to discover dependencies.

Discover configuration, implementation, controller, repository, client, and shared-component roles from parsed declarations.
Remove filename-suffix dependence for these reviewed roles.
Retain inferred capability and area grouping as navigation context.
Keep ownership relationships separate from direct calls and injection relationships.

Audit nested web manifests and roots using the same scope rules.
Do not classify fixtures, tooling, or test modules as production services automatically.

Exit: All 194 known Java files receive parse and extraction dispositions.
Risk: Medium; duplicate roots can duplicate identities or cross source scopes.

### Stage 4: Model configuration dependencies

Model configuration keys, declarations, bindings, and actual reads as separate facts.
Inspect ConfigurationProperties, Value annotations, Environment reads, YAML, properties, and observed environment or template references.
Trace supported getter and placeholder chains into HTTP, database, messaging, and gateway declarations.
Retain repository, module, source file, profile, and environment context.
Keep unknown activation and precedence explicit.
Do not select an active deployment profile from available filenames.

Store key names, sanitized expressions, and source locations.
Exclude credentials, token values, and other secret values from evidence and generated artifacts.
Keep equal keys in different contexts separate unless binding evidence supports a join.

Exit: All 17 configuration classes retain declared binding evidence.
Unsupported member forms and unresolved values retain explicit records.
Every reviewed read and placeholder chain has a source-backed result or unresolved reason.
Risk: High; incorrect precedence or sanitization can expose values or invent destinations.

### Stage 5: Cover API calls and provider matching

Extract typed RestTemplate calls with string literals, variables, constants, getters, and supported URL composition.
Use configuration bindings from Stage 4 when they establish destination parts.
Retain the callsite, HTTP method, symbolic destination, and unresolved reason when concrete identity remains unknown.
Account for all 20 reviewed callsites, including the nested SDK.

Audit existing UI fetch, axios, RTK Query, and wrapper handling against source declarations.
Audit provider mappings, Feign contracts, context paths, gateway rewrites, and inherited or composed annotations.
Extend only forms present in the reviewed corpus.
Separate GraphQL transport endpoints, operations, fields, schemas, and resolver bindings.
Keep dynamic request fields and missing provider implementations explicit.
Retain WebSocket endpoint and message-destination distinctions.

Match method, path, authority, service identity, and applicable gateway evidence.
Retain consumer and provider evidence for every resolved join.
Keep duplicate providers ambiguous and unknown configuration unresolved.

Exit: Every audited API declaration has evidence or a gap; every resolved join has both endpoint sources.
Risk: High; path-only or guessed-authority matching can create false service relationships.

### Stage 6: Cover tables, columns, and data access

Represent all seven BFF entity mappings and their repository type bindings.
Preserve explicit table names, schema expressions, naming strategies, and logical entity identities.
Keep physical names unresolved when naming configuration cannot establish them.
Resolve constants only within supported source and configuration scope.

Add explicit column mappings for all 28 reviewed Column annotations.
Separate Java fields, column mappings, SQL column references, and read or write operations.
Extract supported SQL aliases, projections, predicates, joins, insert targets, and update assignments.
Represent wildcard and dynamic SQL limits explicitly.
Separate migration declarations from runtime access.
Record repository operation declarations without claiming their runtime execution.

Scope table and column identities through datasource, schema, and ownership evidence.
Do not merge equal table names across unknown databases.
Retain existing cache, search, platform, and file boundaries during the extension.

Exit: All reviewed mappings and query references have evidence or explicit unresolved records.
Risk: High; naming strategies, SQL aliases, and ORM behavior can produce incorrect access claims.

### Stage 7: Cover internal and shared dependencies

Extract imports, constructor and field injection, bean bindings, and typed direct calls for reviewed Java source forms.
Link controller, service, repository, and client responsibilities through explicit evidence.
Preserve interface ambiguity, overload uncertainty, dynamic dispatch, and reflection limits.
Keep arbitrary method-call analysis outside supported claims until regressions establish its scope.

Extract web value imports through relative paths, configured aliases, barrels, and local package exports.
Link shared components and functions to exact symbols when source supports resolution.
Separate module use, symbol use, type-only references, package declarations, and runtime calls.
Keep missing and duplicate publishers explicit.

Group class and function details until the user expands their source area.
Do not add every symbol to the system overview.

Exit: Each reviewed injection, import, and direct call resolves with evidence or retains a specific uncertainty.
Risk: High; type and dispatch mistakes can create false call chains.

### Stage 8: Close remaining observed boundaries

Audit Kafka listeners, producers, helpers, topic bindings, and Camel forms against the reference corpus.
Retain configuration-only topics separately from publication and consumption.
Require cluster identity before resolved cross-repository messaging claims.
Report local Kafka recall as N/A when the reviewed local denominator remains zero.

Audit nginx templates, upstreams, import maps, and observed deployment configuration for missing bindings.
Retain dynamic values when source cannot establish an environment-specific route.
Review identity, external SDK, cache, file, and operational integrations found in the ledger.
Prioritize actual source gaps by affected consumers and dependency consequence.

Inspect the current test engine's Python, XML, and configuration boundary forms.
Represent useful test dependencies in a separate test scope where source supports them.
Do not treat test calls as production calls or passing behavior evidence.
Add language or framework extraction only when this audit identifies a current consumer.

Exit: No reviewed source form remains silently omitted; outstanding limitations retain owners and next actions.
Risk: Medium to high; scope mixing can overstate production coverage.

## Scheduling and priority

Complete Stage 1 before assigning coverage percentages.
Stage 2 can proceed with Stage 3 after the baseline is fixed.
Complete module discovery before counting SDK extraction results.
Complete configuration bindings before claiming configured HTTP or resource identities.
API, database, and shared-code work can proceed independently after their model contracts are defined.
Run Stage 8 audits throughout implementation and repeat them at completion.

Prioritize runtime and data dependencies, missing source roots, and hidden existing evidence.
Complete package detail after these items, except where package identity enables a supported shared-code join.
Resolve high-consequence unknown boundaries before adding cosmetic descriptions.
Keep AI descriptions labeled as inferred; descriptions cannot add dependency facts.

## Proposed measurable acceptance criteria

```gherkin
Scenario: Account for the audited source declarations
  Given the pinned Java audit contains 194 files and 20 HTTP callsites
  When the skill builds the graph
  Then all 194 files have parse and extraction dispositions
  And all 20 callsites have canonical call evidence
  And unknown destinations remain unresolved

Scenario: Inspect all existing BFF storage details
  Given the baseline graph contains 7 BFF tables and 8 READS relationships
  When the user opens the BFF Storage view
  Then the index contains all 7 tables and all 8 READS relationships
  And every item opens its evidence and focused diagram

Scenario: Reach records beyond the rendering budget
  Given a graph contains more than 36 nodes and 48 relationships
  And the graph contains API, storage, messaging, and shared-code families
  When the user searches and expands each family
  Then every matching canonical record is reachable
  And rendered and indexed counts reconcile
  And isolated nodes remain searchable

Scenario: Retain configuration and column evidence
  Given the audit contains 17 configuration classes and 28 Column annotations
  When the skill extracts those declarations
  Then all 17 classes retain declared binding evidence
  And unsupported member forms remain explicit
  And all 28 annotations retain mapping evidence
  And mappings do not assert executed reads or writes
  And generated evidence contains no secret values

Scenario: Reject unsupported provider joins
  Given equal paths have different authorities
  And equal topics lack shared cluster identity
  And equal tables lack shared datasource identity
  When the skill resolves relationships
  Then it creates zero resolved joins from those similarities alone

Scenario: Preserve the reference corpus
  Given a fixed reviewed reference graph and its source fixtures
  When the updated standalone skill builds that corpus
  Then every removed relationship has a reviewed correctness explanation
  And every retained resolved relationship preserves both endpoint sources

Scenario: Report an unknown coverage denominator
  Given a source family has no independently reviewed declaration inventory
  When the skill reports semantic extraction coverage
  Then the rate is UNKNOWN
  And evidence-file counts do not substitute for that denominator
```

## Validation and delivery gates

Update affected schema semantics, version policy, validation, projections, queries, viewer behavior, and skill references together.
Inspect callers and importers before changing existing symbols.
Add focused positive, negative, ambiguous, and unsupported regressions for each confirmed defect.
Use synthetic regression sources for portability; keep live business source outside the package.
Check that all new fields survive queries, projections, inspection, and manifest validation.

Run skill tests after each affected implementation stage:

```sh
python -m unittest discover -s .agents/skills/service-dependencies-graph/tests -v
```

Run the project-required checks for completed implementation stages:

```sh
python -m unittest discover -s tests -v
python -m pip wheel . --no-deps --wheel-dir dist
ai-sdlc --workspace . validate
```

For packaging changes, initialize an external workspace from the built wheel.
Check shipped skills, schemas, templates, guides, and operation without the parent harness.
Build comparison snapshots in isolated output directories before replacing the published bundle.
Reject publication when sources change during generation or validation fails.
Compare reviewed declarations, per-family counts, evidence, and documented removals after each build.
Perform browser interaction and visual checks; report blocked visual checks as incomplete.

Complete the final local rebuild through the canonical skill:

```sh
python .agents/skills/service-dependencies-graph/scripts/graph.py --workspace . build
```

Record commands, results, source identities, manifest checksums, measured gains, remaining gaps, owners, and next actions.
Review the staged diff and commit each completed stage after its required checks pass.
Preserve unrelated changes and earlier source or audit evidence.
Do not claim complete runtime coverage from static inspection.

The planning stage checks document links, evidence identities, prose limits, and its diff.
It does not require a new graph build or runtime test execution.
ASD review remains pending.
