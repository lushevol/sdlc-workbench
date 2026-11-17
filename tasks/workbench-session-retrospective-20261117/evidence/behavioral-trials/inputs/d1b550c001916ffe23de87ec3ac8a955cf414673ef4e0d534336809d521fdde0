---
name: maintain-wiki-content
description: Maintain derived wiki pages from bound canonical records using the selected existing OpenKB or llm-wiki-agent semantic workflow.
---

# Maintain derived wiki content

Input: the prepared source scope from [bind-wiki-sources](../bind-wiki-sources/SKILL.md), selected engine, and existing wiki context.
Keep the existing summaries, concepts, entities, index, saved explorations, and cross-links in the shared workspace.

## Apply the existing engine workflow

Read each complete queued canonical record, the index, and relevant existing pages before semantic changes.
Unchanged records may supply necessary context without independent compilation.
Preserve source status, applicability, conditions, conflicts, and evidence limits beside derived claims.
Do not infer implementation, execution verification, or publication approval from intended rules.

Before changing a derived page, classify each material changed or removed claim as `intent`, `implementation`, `test`, `execution`, `deployment`, `approval`, or `unknown`. A policy correction can retire an unsupported acceptance fixture while retaining the same numbers as implementation or test evidence. For every removed numeric or behavioural fact, record a retention mapping with its disposition (`preserved`, `superseded`, or `withdrawn`) and exact evidence. Inspect retained source snapshots, gap records, case definitions, and execution results named by the affected topic; a closure search over wiki pages alone is insufficient.

With both configured URL and token, use the bridge's native semantic compiler:

```sh
python3 .agents/skills/llm-wiki/scripts/wiki.py compile --source knowledge/records/candidates
python3 .agents/skills/llm-wiki/scripts/wiki.py compile --source knowledge/records/candidates --record knowledge/records/candidates/security/access.md --recipe default
```

Select the actual authorized canonical directory for `--source`; the example is not a required scope.
Follow the [engine and command contract](../llm-wiki/references/workflows.md#engine-selection-and-installation).
The bridge compiles full canonical records under its ingest lock and checks source bytes before advancing bindings.
It skips completed unchanged inputs. Matching legacy bindings require bootstrap review; `--force` explicitly requests recompilation.
Compiler return leaves output review pending. Finish through the bridge's `review --receipt` command.
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
Review prior and new dependents, even when a new compiler plan omits a former claim's page.
Remove or qualify withdrawn support and review affected saved explorations.
Without requested regeneration, review an explicit stale qualification. Unresolved affected claims keep completion pending.
Preserve unrelated pages and imported engine/version/revision/archive provenance.
Use the existing index as the synthesis map. Do not create a second overview or source-summary tree.
For direct authoring, follow the [native-format metadata contract](../llm-wiki/references/fallback.md#author-complete-native-format-pages).

Record semantic completion through `wiki.py review` and its changed-output `claim_review` guard. Do not edit `source-manifest.json` or `.openkb/hashes.json` directly to advance a review; direct provenance edits bypass the required claim-loss checks.

## Review and hand off

Review changed claims against exact canonical sections.
Record reviewed page paths/hashes, source-before hashes, actual engine/mode, and a short semantic review note.
For changed sources with unchanged summaries, record the supported reason, such as a metadata-only source change.
An unexplained unchanged summary is incomplete maintenance.
Use [the review receipt contract](../llm-wiki/references/workflows.md#reviewed-completion-receipts) for machine-checkable completion.
For shared pages, name every canonical source whose claims the reviewed output preserves.

Return actual changes, unchanged dispositions, source/output receipt, and unresolved semantic findings to [finalize-wiki-update](../finalize-wiki-update/SKILL.md).
Stop finalization if source bytes changed or a material claim lacks support.
Keep raw/full-text aliases immutable throughout.
