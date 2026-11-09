# Workbench and parent project comparison

Date: 9 November 2026.
Source: [Exact user request](../evidence/parent-project-comparison-20261109/user-input.md#exact-user-input).
Scope: Local source comparison and recommendations. Proposed implementation remains separate.

**Workbench already generalizes much of the parent. Prioritize repeatable quality gates, impact queries, and original execution bindings.**

The comparison needs no immediate user decision.
The recommendations below concern improvement order. They do not establish product defects or authorize implementation.

## Scope and source identity

This is a harness comparison. Business-task intake and knowledge publication do not apply.
The [source manifest](../evidence/parent-project-comparison-20261109/source-manifest.json) records 49 inspected source hashes and exact revisions.

| Project | Inspected revision | Local state and limit |
| --- | --- | --- |
| Standalone Workbench | `1f3baf488635904f6f31d12a55b599f7764a30c0`, branch `main` | Existing untracked `core/release-report/` remains outside the comparison. |
| Parent Release Impact | `b43f21001b6d696bdd48e0c1b041eea4025d7634`, branch `codex/mvp-setup` | Existing staged and unstaged changes remain untouched. Inspected parent sources match this revision. |

The projects have separate Git roots and remotes.
Parent Git also tracks a historical `workbench/` tree as ordinary files.
That tracked tree contains the earlier `src/` layout. The standalone repository uses `core/`.
Parent Git therefore reports changes against its older snapshot when it inspects the nested directory.
Directory nesting does not establish current runtime dependence.

Affected scope: this report and compact supporting evidence.
Qualitative risk: low; documentation changes only.

## Principal differences

The table forms the claim register. Confidence concerns inspected sources, rather than deployed behavior or measured business value.

| ID | Difference | Class, confidence, and evidence | Consequence and limit |
| --- | --- | --- | --- |
| C1 | Parent supplies a configured Ratan settlement harness. Workbench supplies reusable brownfield infrastructure. | Documented intent and inspected implementation; HIGH. [Parent overview](https://github.com/lushevol/ratan-release-impact/blob/b43f21001b6d696bdd48e0c1b041eea4025d7634/README.md#L1-L9), [Workbench boundary](../WORKSPACE_DESIGN.md#brownfield-adoption-boundary). | Parent defaults accelerate its selected system. Workbench preserves different hosts, layouts, languages, and owners. |
| C2 | Parent expects its source checkout. Workbench supports an installed runtime and separate generated workspaces. | Documented contracts and inspected packaging; HIGH. [Parent ownership](https://github.com/lushevol/ratan-release-impact/blob/b43f21001b6d696bdd48e0c1b041eea4025d7634/docs/MODULE_OWNERSHIP.md#L3-L6), [package mapping](../../pyproject.toml), [workspace packaging](../../setup.py). | Preserve Workbench's standalone installation and empty initialization. Parent's wheel omits required resources. |
| C3 | Parent combines OpenKB raw sources, a compiled wiki, and optional QMD retrieval. Workbench separates canonical intent, provenance, governance, and derived views. | Documented contracts and inspected implementation; HIGH. [Parent knowledge](https://github.com/lushevol/ratan-release-impact/blob/b43f21001b6d696bdd48e0c1b041eea4025d7634/knowledge-base/README.md#L14-L25), [Workbench knowledge](../../README.md#preserve-and-govern-knowledge), [literal search](../../core/providers/knowledge.py). | Workbench's built-in knowledge search uses literal text. Retrieval rank cannot establish source authority or publication approval. |
| C4 | Parent provides typed impact traversal. Workbench provides richer graph extraction, snapshots, direct neighborhoods, and bounded recorded paths. | Inspected implementation and documented boundary; HIGH. [Parent traversal](https://github.com/lushevol/ratan-release-impact/blob/b43f21001b6d696bdd48e0c1b041eea4025d7634/ratan_harness/graph/graph_query.py#L130-L305), [current query limits](../../.agents/skills/service-dependencies-graph/references/architecture/impact-analysis.md#supported-commands-and-integrations), [snapshot operations](../../.agents/skills/service-dependencies-graph/tools/snapshot.py). | Workbench lacks automatic typed transitive impact analysis. Recorded path enumeration does not classify affected consumers. |
| C5 | Both projects support immutable baseline saves and comparisons. Parent additionally imports results with original execution binding manifests. | Inspected implementation; HIGH. [Parent importer](https://github.com/lushevol/ratan-release-impact/blob/b43f21001b6d696bdd48e0c1b041eea4025d7634/ratan_harness/assurance_execution.py#L119-L164), [Workbench assurance](../../core/assurance.py), [current result limits](../BEHAVIOR_REVIEW.md#interpret-metrics). | Workbench marks assertion bindings `DECLARED` and behavior `NOT_VERIFIED`. These conservative statuses remain appropriate. |
| C6 | Parent has a tracked GitHub quality workflow and deterministic API evaluations. Workbench has runtime regressions and separate agent decision trials. | Inspected tracked files and assertions; HIGH. [Parent CI](https://github.com/lushevol/ratan-release-impact/blob/b43f21001b6d696bdd48e0c1b041eea4025d7634/.github/workflows/quality.yml), [API evaluation](https://github.com/lushevol/ratan-release-impact/blob/b43f21001b6d696bdd48e0c1b041eea4025d7634/docs/QUALITY_EVALUATION.md#L18-L49), [Workbench trials](../../tests/README.md#evaluate-skill-decisions). | No tracked Workbench `.github` workflow was found. External CI configuration remains unknown. Existing tests still protect consequential boundaries. |
| C7 | Parent aggregates dependency, knowledge, repository, and MCP health. Workbench separates resource discovery from local setup diagnostics. | Inspected implementation; HIGH. [Parent aggregation](https://github.com/lushevol/ratan-release-impact/blob/b43f21001b6d696bdd48e0c1b041eea4025d7634/scripts/ratan.py#L800-L829), [Workbench doctor](../../core/doctor.py), [resource discovery](../../core/runtime.py). | Workbench already reports concrete next actions and `integration_access: UNTESTED`. A unified view could reduce navigation. |

## Practices already adopted

The parent is a useful source of tested patterns. Several patterns already exist in Workbench.

- The graph uses canonical snapshots, checksums, coverage declarations, source fingerprints, diagnostics, and explicit unresolved boundaries.
- A [previous comparison](SERVICE_DEPENDENCIES_IMPLEMENTATION_REPORT.md#snapshot-comparison) ran both extractors against the same parent sources.
  It demonstrated additional Workbench extraction and recorded identity reconciliation. Its historical totals do not measure current semantic coverage.
- Workbench already has immutable saves, baseline comparison, evidence freshness, and direct coverage matrices.
  See [behavior review](../BEHAVIOR_REVIEW.md) and [the review index](../REVIEW_INDEX.md#derive-coverage-matrices).
- The graph skill already contains the [report prose checker](../../.agents/skills/service-dependencies-graph/tools/output_standard.py).
  Reuse that checker when justified. Another copied implementation would create maintenance work.
- The installed `ai-sdlc` CLI already supplies a common operational interface.
  Parent shell wrappers illustrate discoverable commands; Workbench does not need another command framework.
- Workbench already supports registered test commands and Robot execution.
  Preserve application suites and runner environments in their owning repositories.

Workbench also offers broader setup controls through [Windows/macOS launchers](../SETUP.md), [offline bundles](../DEPENDENCIES.md), and bounded downloads.
The parent setup script should not replace those controls.

## Recommended applications

These are proposals derived from the inspected differences. Confidence in the ordering is MEDIUM because adoption costs remain unmeasured.
Owners identify roles. Named accountable people remain unknown.

| Order | Proposal and supporting claim | Expected benefit | Owner and concrete next increment |
| --- | --- | --- | --- |
| 1 | Add a repeatable standalone quality gate. See C6. | Detect regressions through one maintained command and a hosted workflow. | Workbench maintainer. Run all declared runtime tests, contract checks, wheel build, and fresh workspace initialization. Add relevant existing Node checks. |
| 2 | Add deterministic API quality cases beside current unit and agent tests. See C6. | Detect wrong impact classifications, unsupported retrieval results, broken citations, and incorrect empty answers. | Graph and knowledge maintainers. Define independent expected inclusions, exclusions, and abstentions before observing results. Retain fixture hashes and raw denominators. |
| 3 | Adapt typed impact traversal to the existing graph interface. See C4. | Trace changed ownership through dependency chains while preserving uncertain consumers and unresolved boundaries. | Graph maintainer. Start with exact changed files and explicit repositories. Return supported, possible, context, and unresolved result sets. |
| 4 | Capture original assertion-to-behavior bindings when the selected runner executes. See C5. | Detect attempts to reuse results after assertion, code, configuration, or data changes. | Verification maintainer and selected test owner. Extend one existing runner and the review index with original binding evidence. |
| 5 | Offer one scoped readiness summary. See C7. | Reduce repeated commands during onboarding and investigation setup. | Workbench maintainer. Compose existing diagnostics with selected repository and graph freshness checks. Keep optional features and live access separate. |

For proposal 1, a passing run needs complete execution of the declared suite and zero failures.
Do not omit checks, weaken assertions, or hide failures to obtain passing status.
Native Windows and offline checks need their own evidence when those installation paths change.

For proposal 2, reuse the parent's evaluation method through Workbench's actual APIs.
Its fixtures test eight impact cases and four local retrieval cases.
They are technical synthetic data. They supply no business acceptance evidence.
Current agent decision evaluations address a different layer and should remain separate.

For proposal 3, preserve Workbench's newer node types, relationships, snapshot identities, and coverage limits.
The parent prevents a shared dependency from automatically making all its users affected.
It also distinguishes write-to-reader and publisher-to-consumer propagation.
Port those semantics with positive, negative, ambiguous, and unresolved cases.
Move domain synonyms and seeding policies into project configuration when a consumer requires them.
Remove parent runtime imports, flat repository assumptions, and implicit Ratan defaults from any adaptation.

For proposal 4, preserve the original report and exact code, test, assertion, configuration, and data identities.
Reject stale bindings and duplicate run identities through the existing contracts.
The parent importer cannot authenticate execution and has no native JUnit or Robot importer.
Its contract is a useful pattern, rather than a complete adapter solution.

The [Robot provider](../../core/providers/robot.py) already captures revision, dirty state, and selected suite hashes before execution.
Its source capture excludes suite imports and private inputs outside the selected sources.
Build on those records and existing runtime configuration hashes.
The additional scope concerns original assertion-to-behavior bindings and complete declared input identities.

Keep Workbench's historical saves available when evidence is stale or unknown.
Apply current-evidence requirements to the named assessment or execution step.
Keep knowledge approval and publication in the existing governance mechanism.
Do not introduce another approval store or automatically grant `VERIFIED`.

## Conditional lessons and transfer boundaries

Ranked retrieval is a conditional improvement.
The parent's [QMD integration](https://github.com/lushevol/ratan-release-impact/blob/b43f21001b6d696bdd48e0c1b041eea4025d7634/knowledge-base/README.md#L42-L70) checks freshness and provides a local fallback.
First benchmark actual Workbench questions against literal search and the existing derived wiki.
Measure relevant results, unsupported results, citation resolution, abstention, latency, and maintenance effort.
Add optional retrieval dependencies only when those measurements justify them.

Repository inventory and freshness checks are useful before optional clone or index automation.
Keep initialization empty. Repository execution requires explicit grants and owning-project instructions.
Do not copy the parent's automatic Azure repository cloning, settlement corpus, Robot paths, or endpoint mappings into defaults.

The parent also offers [optional tracing](https://github.com/lushevol/ratan-release-impact/blob/b43f21001b6d696bdd48e0c1b041eea4025d7634/ratan_harness/tracing.py).
Consider a timing export from existing action records only after a measured investigation need arises.
Keep telemetry optional and avoid duplicate audit payloads.

The nested Git arrangement deserves separate housekeeping.
Parent maintainers should decide whether to retire its tracked historical Workbench snapshot.
Preserve both histories and existing local changes before any migration.
The [system isolation proposal](../SYSTEM_WORKSPACE_ISOLATION.md#recommended-construction) already describes independent framework and system ownership.
This comparison does not authorize deletion or relocation.

## Verification and limits

The [source manifest](../evidence/parent-project-comparison-20261109/source-manifest.json) records commands, environment attempts, topology, and source hashes.
Workbench resource discovery succeeded through its existing virtual environment.
System Python lacked PyYAML. This environment difference does not establish a runtime defect.

The [retained parent evaluation](../evidence/parent-project-comparison-20261109/parent-quality.json) passed all 12 declared synthetic cases.
All three expected abstentions were correct. All three returned citations resolved.
These results concern parent impact helpers and local retrieval only.
They do not establish QMD quality, private-corpus quality, business behavior, or deployed service operation.

This comparison changed no runtime code, source contracts, business policy, credentials, or execution grants.
Full runtime suites and wheel builds were not repeated for this documentation stage.
The [recent assessment](../evidence/ai-sdlc-assessment-20261107/assessment.md#local-verification) retains earlier Workbench validation with its exact limits.
Those historical results are not current executions.

Implementation boundaries have HIGH source confidence.
Expected productivity gains and improvement ordering remain inferences with MEDIUM confidence.
Live integrations, deployment state, external CI, and production applicability remain outside this comparison.

## Output review

[Document checks](../evidence/parent-project-comparison-20261109/document-checks.json) record local links, source identities, evidence hashes, and prose checks.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
