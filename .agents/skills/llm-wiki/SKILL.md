---
name: llm-wiki
description: Maintain the single Workbench knowledge wiki with OpenKB when an LLM URL and token are configured, otherwise with llm-wiki-agent in the current ADE session.
---

# Maintain the project knowledge wiki

Use one active wiki at `knowledge/llm-wiki/`. Keep its existing detailed summaries, focused concepts, entities, saved explorations and cross-links. Do not create another wiki when the selected engine changes.

For this project, translate native OpenKB skill commands through the [project-scoped launcher](references/workflows.md#project-scoped-commands). Begin with `python3 .agents/skills/llm-wiki/scripts/wiki.py run status`; bare upstream discovery can select another global KB.

## Select the semantic engine

```sh
python3 .agents/skills/llm-wiki/scripts/wiki.py engine
```

When **both** `OPENAI_API_BASE` and `LLM_API_KEY` are configured in `knowledge/llm-wiki/.env` or the process environment, use [OpenKB](../openkb/SKILL.md) as primary for semantic compilation, query and lint. KB-local nonempty values take precedence. Use a provider-compatible model in the ignored `.openkb/config.yaml`. URL and token presence selects the engine; it does not verify authentication or endpoint availability.

Otherwise use the original [llm-wiki-agent instructions](upstream/AGENTS.md) in the **current ADE session**, without another model URL or token. Do not automatically substitute OAuth or infer a URL from a provider-specific key. The launcher's `compile` and semantic `run` commands return an explicit agent handoff in this mode; that output does not mean compilation ran. Carry out the requested semantic work using the current agent's tools.

For direct file authoring, read the [fallback metadata and provenance procedure](references/fallback.md). It defines native-format new pages and how reviewed source changes finish with consistent bindings. Its Workbench layout rules take precedence over the original agent's page format and native compiler body-only prompts.

## Maintain the shared documents

The processing stages are complete raw export → filtered source view → canonical knowledge → derived wiki.
Use [source preparation](../ingest-knowledge/references/source-preparation.md) for raw imports and hash-bound source selections.
Compile canonical knowledge records only. Keep filtered excerpts and original raw exports outside the wiki's source aliases.
Save the canonical source page's SHA-256 when linking it in `raw/` and `wiki/sources/`.

Keep that hash in `source-manifest.json` and verify it before reuse. Both aliases must resolve to the same canonical record.
Changed source hashes require reconciliation before advancing wiki bindings. Missing sources do not authorize automatic knowledge deletion.

Read the complete canonical source, the index and relevant existing pages before writing. In fallback mode, apply the original agent's ingest/query/contradiction workflows with these external layout constraints: derived source summaries live in `wiki/summaries/`; `wiki/sources/` and `raw/` are immutable relative links to canonical records; saved synthesis lives in `wiki/explorations/`. Preserve the existing page metadata and wiki-relative links. Use the current index as the synthesis map; a second overview or duplicate source-summary tree is unnecessary.

Never run upstream scripted `ingest` or `refresh` against those source aliases: they assume owned source-summary files and could write through canonical symlinks. The [Workbench procedures](references/workflows.md) explain source bindings, supported commands and validation. Both original upstream code and the official OpenKB skill remain unchanged.

Use [ingest-knowledge](../ingest-knowledge/SKILL.md) and [govern-knowledge](../govern-knowledge/SKILL.md) for canonical changes and publication. Retain source IDs, hashes, versions, lifecycle, applicability and unresolved conflicts. Derived wiki content and graph connectivity do not approve policy or prove implementation behavior.

## Verify and visualize

```sh
python3 .agents/skills/llm-wiki/scripts/wiki.py verify
python3 .agents/skills/llm-wiki/scripts/wiki.py graph
```

These local checks use the stored OpenKB page format in either semantic mode. Verification and original OpenKB visualization make no model calls. The graph at `knowledge/llm-wiki/output/visualize/graph.html` is the wiki's native wikilink graph; keep it separate from the service dependency graph.

Report the selected semantic engine, actual work performed, source integrity, structural findings and remaining knowledge limits. Reading or exporting metadata is not semantic compilation.
