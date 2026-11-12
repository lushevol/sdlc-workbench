---
name: maintain-wiki-content
description: Maintain derived wiki pages from bound canonical records using the selected existing OpenKB or llm-wiki-agent semantic workflow.
---

# Maintain derived wiki content

Input: the prepared source scope from [bind-wiki-sources](../bind-wiki-sources/SKILL.md), selected engine, and existing wiki context.
Keep the existing summaries, concepts, entities, index, saved explorations, and cross-links in the shared workspace.

## Apply the existing engine workflow

Read each complete selected canonical record, the index, and relevant existing pages before semantic changes.
Preserve source status, applicability, conditions, conflicts, and evidence limits beside derived claims.
Do not infer implementation, execution verification, or publication approval from intended rules.

With both configured URL and token, use the bridge's native semantic compiler:

```sh
python3 .agents/skills/llm-wiki/scripts/wiki.py compile --source knowledge/candidates
```

Select the actual authorized canonical directory for `--source`; the example is not a required scope.
Follow the [engine and command contract](../llm-wiki/references/workflows.md#engine-selection-and-installation).
The bridge compiles full canonical records under its ingest lock and checks source bytes before advancing bindings.
It calls the compiler directly; native source-owning `add` transaction recovery does not cover this whole bridge operation.
Native failure stops affected completion. Partial pages and earlier per-source successful bindings may remain for inspection.
Do not silently switch engines to hide a failed native operation.

Without both settings, read the unchanged [llm-wiki-agent workflow](../llm-wiki/upstream/AGENTS.md) and work in the current ADE session.
The bridge's handoff alone edits no pages or provenance.
Apply the upstream semantic ingestion and contradiction steps with these layout mappings:

| Upstream responsibility | Shared workspace location |
| --- | --- |
| Derived source summary | `wiki/summaries/` |
| Original/full source | Immutable `raw/` and `wiki/sources/` canonical aliases |
| Saved synthesis | `wiki/explorations/`, only when requested |

Maintain summaries, focused concepts, entities, contradictions, and index entries together as needed by the changed claims.
Preserve unrelated pages and imported engine/version/revision/archive provenance.
Use the existing index as the synthesis map. Do not create a second overview or source-summary tree.
For direct authoring, follow the [native-format metadata contract](../llm-wiki/references/fallback.md#author-complete-native-format-pages).

## Review and hand off

Review changed claims against exact canonical sections.
Record reviewed page paths/hashes, source-before hashes, actual engine/mode, and a short semantic review note.
For changed sources with unchanged summaries, record the supported reason, such as a metadata-only source change.
An unexplained unchanged summary is incomplete maintenance.

Return actual changes, unchanged dispositions, source/output receipt, and unresolved semantic findings to [finalize-wiki-update](../finalize-wiki-update/SKILL.md).
Stop finalization if source bytes changed or a material claim lacks support.
Keep raw/full-text aliases immutable throughout.
