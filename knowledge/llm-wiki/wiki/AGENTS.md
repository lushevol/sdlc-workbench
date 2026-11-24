# Wiki Schema

## Workbench authoring context

Use the [Workbench bridge](../../../.agents/skills/llm-wiki/SKILL.md) and its [direct ADE maintenance contract](../../../.agents/skills/llm-wiki/references/fallback.md) for this shared wiki. The native compiler's body-only instruction below applies when OpenKB code wraps a model response. When the ADE agent edits files directly, it must create/preserve complete native frontmatter and complete the reviewed source bindings. These project rules resolve differences from the original llm-wiki-agent layout; original upstream packages remain unchanged.

## Directory Structure
- sources/ — Document content. Short docs as .md, long docs as .json (per-page). Do not modify directly.
- sources/images/ — Extracted images from documents, referenced by sources.
- summaries/ — One per source document. Summary of key content.
- concepts/ — Focused reusable topics and cross-document synthesis. Create a page for a recurring question or current consumer; a useful single-source topic can remain, with its source count explicit.
- entities/ — Specific named things: people, organizations, places, products, named works, events. One page per entity, accumulated across documents.
- explorations/ — Saved query results, analyses, and comparisons worth keeping.
- reports/ — Lint health check reports. Auto-generated.

## Special Files
- index.md — Content catalog: every page with link, one-line summary, organized by category.
- log.md — Chronological append-only record of operations (ingests, queries, lints).

## Page Types
- **Summary Page** (summaries/): Key content of a single source document.
- **Concept Page** (concepts/): A focused reusable topic with [[wikilinks]], often synthesized across documents. Keep its actual source count explicit.
- **Entity Page** (entities/): A specific named thing (proper noun) — e.g. a person, organization, place, product, named work, or event. Each page has a `type:` frontmatter field; the exact allowed type set is configurable (default: person, organization, place, product, work, event, other) and the authoritative set for this run is given in the compilation prompt. An entity differs from a concept: a concept is an abstract recurring idea; an entity is a specific named thing. Create an entity page only when the entity is central to a document or recurs across sources — do not page passing mentions.
- **Exploration Page** (explorations/): Saved query results — analyses, comparisons, syntheses.
- **Index Page** (index.md): One-liner summary of every page in the wiki. Auto-maintained.

## Index Page Format
index.md lists all documents, concepts, entities, and explorations with metadata:
- Documents: name, one-liner description, type (short|pageindex), detail access path
- Concepts: name, one-liner description
- Entities: name, type, one-liner description
- Explorations: name, one-liner description

## Log Format
Each log entry: `## [YYYY-MM-DD HH:MM:SS] operation | description`
Operations: ingest, query, lint

## Format
- Use [[wikilink]] to link other wiki pages (e.g., [[concepts/attention]])
- Standard Markdown heading hierarchy
- Keep each page focused on a single topic
- Keep entity introductions focused on identity, responsibility and interfaces. Link to the focused concepts for detailed rules; retain unique source context, conflicts and evidence limits when reorganizing existing pages.

## Frontmatter (managed by code — do NOT emit it in generated content)

This section governs responses to the native compiler. For direct ADE file authoring, use the complete metadata examples in the Workbench contract above.
- Every summary/concept/entity page carries a non-empty `type:` — `Summary`,
  `Concept`, or a capitalized entity subtype (e.g. `Organization`). This is the
  one field OKF requires; consumers use it for routing/filtering/presentation.
- `description:` — a single-sentence one-liner (the field formerly named `brief`).
- Do not include YAML frontmatter (---) in generated content; it is managed by code.
