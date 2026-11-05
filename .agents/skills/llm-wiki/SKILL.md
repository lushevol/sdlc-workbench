---
name: llm-wiki
description: Generate, refresh, query, and review a source-linked wiki over existing business-domain knowledge, with connected source summaries, entities, concepts, and synthesis.
---

# Build and maintain the knowledge wiki

Use the llm-wiki authoring pattern to make existing project knowledge easier to understand and navigate.
Maintain connected source summaries, entity pages, concept pages, and a living overview.
Use the current coding agent. This skill requires no separate model API, package installation, or server.

This skill adapts [SamurAIGPT/llm-wiki-agent](references/upstream.md) at the recorded revision.
Read [the mode procedures](references/workflows.md) for generation, refresh, queries, health, semantic lint, or graph navigation.

## Select the source and output boundary

Default output: `knowledge/wiki/` in the selected workspace.
Start with the workspace's structured domain records and their existing review states.
Read every selected record, including its sources, rules, exceptions, and unresolved questions.
For raw document ingestion, use [ingest-knowledge](../ingest-knowledge/SKILL.md) first, then compile its resulting records.
Do not reinterpret implementation observations as intended business behavior.

The wiki is derived navigation over canonical knowledge, not a separate publication path.
Use Markdown links to exact canonical records, headings, and supporting sources.
Retain record IDs, versions, candidate states, conflicts, and applicability limits beside the summaries.
Reopen canonical records before using a wiki claim for engineering decisions.
Changes to intended meaning still follow normal ingestion, review, and audit requirements.

## Use the supported wiki layout

```text
knowledge/wiki/
  index.md                          # Catalog and coverage scope.
  overview/index.md                 # Living cross-source synthesis.
  sources/<record-id>/index.md       # One summary per selected record.
  entities/<slug>/index.md           # Supported component or domain-entity explanation.
  concepts/<slug>/index.md           # Supported cross-source concept.
  syntheses/<slug>/index.md          # Reusable answer when saving is authorized.
```

Create only pages with useful supported content.
Each navigation page uses `index.md` without a governed-record frontmatter block.
This layout follows the existing Workbench navigation contract.

Do not add raw sources, logs, JSON, reports, or generated runtime graphs under `knowledge/`.
Keep original evidence at its existing location.
Keep wiki inventories, generation logs, and health reports in the owning report's evidence directory or ignored working storage.
Use record IDs for source-page directories and readable ASCII slugs for other page directories.

## Complete the requested mode

Generate a complete wiki for the declared record scope when the user requests generation.
Include the overview, source summaries, useful connections, and consequential unknowns.
For refresh, compare exact input hashes and update only affected derived navigation.
Preserve predecessor records, raw snapshots, and immutable audit events.

Run cheap structural health checks before semantic lint.
Health checks cover missing or empty pages, index coverage, links, source bindings, and input/output hashes.
Semantic lint reviews support, contradictions, missing topics, and applicability.
Broken links create findings or proposed pages; they do not authorize invented content or automatic healing.
Use the existing [graph skill](../service-dependencies-graph/SKILL.md) for graph operations.
Wiki connections cannot establish dependencies, source authority, approval, or business execution.

Report record coverage with its denominator, actual health results, retained evidence, and material limits.
Distinguish complete record navigation from complete source ingestion, semantic truth, and verified business behavior.
Do not rebuild graphs or change other skill workflows unless that work belongs to the user's requested stage.
