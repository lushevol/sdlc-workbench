# LLM wiki adoption

**Historical stage report.** The installation and 19-page wiki below belong to revision `c10336b65e2c033e8b6d8c287cc511db1f3bcc39`. Use the [current wiki workflow](../../.agents/skills/llm-wiki/SKILL.md) and [engine-selection report](LLM_WIKI_ROUTING_AND_CLEANUP_20261111.md) for present operation. The frozen output links below preserve that stage; its installation statements do not describe the active tools today.

**Adopted: the project wiki skill now produces a source-linked wiki over all 12 current domain records.**

The [historical wiki index](https://github.com/lushevol/sdlc-workbench/blob/c10336b65e2c033e8b6d8c287cc511db1f3bcc39/knowledge/wiki/index.md) opens 19 pages, including summaries, concepts, responsibilities, and a living overview.
All source records remain candidate/draft.
Wiki generation supplies no publication approval or business verification.

Owner: Workbench maintainer.
Started: 5 November 2026. Completed: 6 November 2026, Asia/Singapore.
The [latest user input](../evidence/knowledge-mechanism-review-20261103/user-input.md#exact-wiki-adoption-input) controls this stage.
The [upstream assessment](LLM_WIKI_AGENT_INTEGRATION_20261105.md) supplies the pinned source and compatibility findings.

## Scope and sequence

Adopt the skill first.
Generate the knowledge wiki next.
Then assess integration coverage across existing skills.
This stage follows the requested sequence: skill adoption, wiki generation, then integration assessment.
The integration assessment covers every existing shared skill.
Deeper workflow changes remain recommendations for the next stage.

## Adopted skill and affected interfaces

The canonical [llm-wiki skill](../../.agents/skills/llm-wiki/SKILL.md) adapts upstream revision `37145b8ba04d0acc6f3b6b0c02606768d1862c9a`.
Its [origin record](../../.agents/skills/llm-wiki/references/upstream.md) explains retained workflows and compatibility changes.
The original [MIT notice](../../.agents/skills/llm-wiki/LICENSE.md) is preserved byte-for-byte.

The skill provides generation, refresh, queries, structural health, semantic lint, and existing graph navigation.
It uses the current coding agent without a separate model API, converter, package, or server.
The upstream Python tools, automatic healer, graph format, and scheduler recipe were not installed.
This is an instruction-based skill, without a new automatic pipeline or background synchronization service.

Inspection covered runtime skill discovery, scaffold copying, wheel construction, offline fingerprints, and Claude alias fallback before editing those interfaces.
The existing implementation already discovers and ships canonical skill directories.
Changes add the skill, its Claude alias, scaffold mapping, and expected-skill inventory.
No Python runtime implementation changed.

Qualitative risk: low for installation, medium for summary freshness and semantic interpretation.
Exact input bindings, visible source states, canonical citations, and independent retrieval review address those boundaries.

## Generated wiki

The [historical living overview](https://github.com/lushevol/sdlc-workbench/blob/c10336b65e2c033e8b6d8c287cc511db1f3bcc39/knowledge/wiki/overview/index.md) connects entry, composition, permissions, session continuity, onboarding, release, and observation.
Four concept pages explain cross-source behavior.
One entity page explains intended service responsibilities.
Twelve source pages summarize every current structured domain record.

| Coverage | Result | Meaning and limit |
| --- | --- | --- |
| Canonical record summaries | 12/12. | Every selected structured domain record has a source summary. |
| Generated navigation | 19/19 pages reachable. | Index, overview, 12 source pages, four concepts, and one entity page. |
| Existing workflow assessment | 16/16 skills. | Each workflow has an integration recommendation and evidence boundary below. |
| Source state preservation | All 12 remain candidate/draft. | Summary generation changes no review or publication state. |
| Protected evidence | Existing protected inventories match the baseline. | Governed records, snapshots, manifest history, and audit bytes remain unchanged. |

The [generation binding](../evidence/knowledge-mechanism-review-20261103/wiki-adoption/generation.json) records exact canonical paths, IDs, versions, hashes, outputs, and health results.
Source summaries retain original qualifiers and unresolved questions.
The wiki links the existing living question document rather than creating competing policy answers.
Directory `index.md` pages use Workbench's existing navigation contract without inventing new governed record types.

Generation reviewed canonical records and their declared source locators.
It did not independently reread every raw snapshot behind those records.
The 12/12 figure measures record navigation, rather than complete domain knowledge or assertion coverage.
Actual implementation, deployment, execution, and conformance remain in their existing task evidence and gaps.

## Integration coverage across existing skills

This table assesses all 16 pre-existing canonical skills.
The new wiki skill references existing ingestion and graph procedures where needed.
The original skill entrypoints retain their existing behavior during this initial adoption stage.

| Existing skill | Wiki use and refresh point | Authoritative evidence boundary | Recommendation |
| --- | --- | --- | --- |
| [analyze-requirement](../../.agents/skills/analyze-requirement/SKILL.md#L48-L91) | Locate intended behavior and answered questions. Refresh after sourced canonical clarification. | Exact definitions, task answers, and source authority control intake readiness. | Add optional navigation after core knowledge workflows. |
| [code-review](../../.agents/skills/code-review/SKILL.md#L28-L34) | Optional domain and consumer discovery. A code diff alone does not refresh intent. | Exact baseline/candidate code, assertions, and reproduction evidence control findings. | Keep review usable without the wiki. |
| [connectors](../../.agents/skills/connectors/SKILL.md#L65-L110) | Optional source discovery. Refresh after authorized results become canonical knowledge. | Live schemas, grants, configuration, and action results control access. | No direct integration initially. |
| [detect-gaps](../../.agents/skills/detect-gaps/SKILL.md#L15-L56) | Locate conflicting topics and intent. Refresh after canonical topic or finding navigation changes. | Exact old/new behavior, assertions, and retained results control actual gaps. | Add advisory discovery and health findings. |
| [gherkin-quality](../../.agents/skills/gherkin-quality/SKILL.md#L18-L74) | Locate vocabulary and requirements. Refresh after canonical definitions change. | Exact criteria, UI evidence, component identities, and helper assertions control cases. | Use summaries only to locate definitions. |
| [govern-knowledge](../../.agents/skills/govern-knowledge/SKILL.md#L30-L64) | Review affected topics. Refresh after final content, lifecycle, review, or provenance changes. | Actual reviewers, final bytes, schemas, and immutable events control publication. | High-value refresh integration after ingestion and query. |
| [impact-analysis](../../.agents/skills/impact-analysis/SKILL.md#L29-L59) | Locate behavior and related topics. Refresh after confirmed intent or topic relationships change. | Exact callers, contracts, typed relationships, and freshness control impact. | Add an optional discovery route. |
| [ingest-knowledge](../../.agents/skills/ingest-knowledge/SKILL.md#L32-L49) | Inspect topic coverage, then refresh after the final ingestion checkpoint. | Snapshots, claim review, compliant candidates, and audit bindings remain canonical. | First integration priority. |
| [query-knowledge](../../.agents/skills/query-knowledge/SKILL.md#L16-L48) | Begin from wiki navigation. Read-only queries require no rewrite. | Reopen applicable records and cited sources; preserve intent/actual and candidate/published distinctions. | First integration priority. |
| [release-clinic](../../.agents/skills/release-clinic/SKILL.md#L139-L161) | Optional domain context. Refresh intent through separately authorized ingestion. | Collector results, retained attachments, rule editions, and report hashes control findings. | Link existing Clinic reports directly; avoid recomputation. |
| [release-confidence](../../.agents/skills/release-confidence/SKILL.md#L33-L76) | Locate rules and journeys. Refresh after actual canonical intent changes. | Candidate bytes, assertions, executions, remote logs, and deployment evidence control release assessment. | Wiki navigation cannot increase an evidence score. |
| [repository-onboarding](../../.agents/skills/repository-onboarding/SKILL.md#L24-L44) | Optional existing context. Refresh when authorized findings become governed candidates. | Exact revisions, repository sources, assessments, and retained limits remain authoritative. | Keep repository documentation and publication separate. |
| [service-dependencies-graph](../../.agents/skills/service-dependencies-graph/SKILL.md#L8-L13) | Wiki links existing graph queries. Check freshness after knowledge inventory changes. | Canonical records and typed directed evidence control graph facts. | Prevent wiki-to-graph-to-wiki evidence cycles. |
| [sync-release-knowledge](../../.agents/skills/sync-release-knowledge/SKILL.md#L33-L67) | Locate affected topics. Refresh after completed target-rule or navigation updates. | Sourced intent changes revise target knowledge; release observations revise independent conformance evidence. | High-value refresh integration. |
| [validate-sdlc-documents](../../.agents/skills/validate-sdlc-documents/SKILL.md#L19-L37) | Optional navigation. Refresh after authorized canonical corrections. | Runtime schemas, templates, and exact selected documents control validation. | Check wiki pages as navigation; preserve record contracts. |
| [verify-implementation](../../.agents/skills/verify-implementation/SKILL.md#L31-L58) | Locate intended behavior. Execution alone does not refresh intended knowledge. | Exact ACs, code, assertion chains, and matching results control coverage. | A wiki page cannot count as implementation or passing execution. |

Recommended next sequence: ingestion and query, then governance and release synchronization, then optional consumers.
Existing knowledge providers do not automatically index derived wiki navigation as governed records.
The new skill and normal file navigation provide wiki access in this stage.
Adding wiki-aware retrieval later needs explicit freshness and applicability handling.

The existing graph may report stale inputs after new knowledge navigation files appear.
This stage does not rebuild it or add wiki summaries as graph facts.
Inspect freshness before using saved graph results.

## Validation and remaining limits

The [validation manifest](../evidence/knowledge-mechanism-review-20261103/wiki-adoption/validation.json) records commands, outcomes, hashes, and retained results.
The full runtime suite passed 883 tests with zero failures, errors, skips, or expected failures.
The wheel build, installed-workspace checks, skill validation, navigation health, and independent retrieval review also passed.
The [ingestion check](../evidence/knowledge-mechanism-review-20261103/wiki-adoption/harness-check.json) checks all 19 wiki pages against the protected baseline.
Additional health checks validate heading anchors, record coverage, and index reachability.

An independent reader inspected all 12 canonical records and all 19 wiki pages.
The [retrieval review](../evidence/knowledge-mechanism-review-20261103/wiki-adoption/retrieval-review.json) answers six representative questions with citations and exact reviewed hashes.
It includes unanswered timeout policy, multiple-entity matching, and a proposed tenant-onboarding requirement.
This exercise assesses supported retrieval; it does not establish business execution or production approval.

The [installed-wheel check](../evidence/knowledge-mechanism-review-20261103/wiki-adoption/installed-wheel-check.json) uses an isolated package outside this checkout.
It confirms skill discovery, source/reference/license bytes, Claude alias resolution, and empty-workspace validation.
The new workspace contains 17 canonical skills and excludes this project's wiki and runtime source.
It reuses the existing dependency environment.

The initial runtime run encountered sandbox socket restrictions.
Its [retained output](../evidence/knowledge-mechanism-review-20261103/wiki-adoption/runtime-tests-sandbox.log) distinguishes environmental errors from assertion failures.
The complete rerun enables the installed optional Node integration checks.
The preceding unrestricted run [omitted those two optional checks](../evidence/knowledge-mechanism-review-20261103/wiki-adoption/runtime-tests-without-optional.log).

The final run executes both, without narrowing the suite.
The [final runtime output](../evidence/knowledge-mechanism-review-20261103/wiki-adoption/runtime-tests.log) records actual suite counts and outcome.
No test, assertion, or application behavior was weakened for this delivery.

Connected dependency acquisition, Windows execution, automatic synchronization, and weaker-model reliability remain untested.
No separate provider call, upstream Python execution, source re-ingestion, or graph rebuild occurred.
Source authority and publication remain unresolved wherever canonical records leave them unresolved.

## Checks and writing review

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
