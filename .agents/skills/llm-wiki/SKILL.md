---
name: llm-wiki
description: Orchestrate maintenance of the single derived Workbench wiki through existing OpenKB or current-session llm-wiki-agent controls.
---

# Orchestrate the project knowledge wiki

Keep one active wiki at `knowledge/llm-wiki/` across engine changes.
This parent selects operations and reconciles their results. The reusable units own their procedures.

## Route the requested work

Start through the [project-scoped launcher](references/workflows.md#project-scoped-commands):

```sh
python3 .agents/skills/llm-wiki/scripts/wiki.py run status
python3 .agents/skills/llm-wiki/scripts/wiki.py engine
```

Use OpenKB semantic operations only with both `OPENAI_API_BASE` and `LLM_API_KEY` configured.
Otherwise use unchanged [llm-wiki-agent workflows](upstream/AGENTS.md) in the current ADE session.
The [engine contract](references/workflows.md#engine-selection-and-installation) defines precedence, installation, and private configuration.
A printed handoff performs no semantic work.

| Request or stage | Reusable unit | Required result |
| --- | --- | --- |
| New, changed, or relocated canonical inputs | [bind-wiki-sources](../bind-wiki-sources/SKILL.md) | Validated selection, canonical aliases, starting hashes, and recovery material. |
| Compile or update derived pages | [maintain-wiki-content](../maintain-wiki-content/SKILL.md) | Engine-maintained pages and reviewed source/output receipt. |
| Finish an update | [finalize-wiki-update](../finalize-wiki-update/SKILL.md) | Consistent provenance, verification, truthful completion, or coordinated recovery. |
| Inspect freshness or quality | [check-wiki-health](../check-wiki-health/SKILL.md) | Read-only integrity, structural, and applicable semantic findings. |

For maintenance, run binding, semantic maintenance, then finalization in that order.
Stop affected completion when a unit reports missing evidence, changed bytes, or failed checks.
Query-only work uses the [query procedure](references/workflows.md#query-and-saved-synthesis); graph requests use the [native viewer](references/workflows.md#wiki-graph).
Neither operation completes a pending update.
Requested engine lint uses the [lint command](references/workflows.md#health-and-semantic-review); it can persist a report and log.

## Preserve lifecycle boundaries

The pipeline is complete export → filtered source view → canonical knowledge → derived wiki.
Use [source preparation](../prepare-knowledge-sources/SKILL.md) before canonical ingestion.
Use [ingest-knowledge](../ingest-knowledge/SKILL.md) and [govern-knowledge](../govern-knowledge/SKILL.md) for canonical meaning and publication.

Reuse the engines' existing ingestion, freshness, compilation, and quality controls through the bridge.
Do not add another source approval state machine.
Candidate sources remain candidates. Wiki freshness cannot supply publication approval or business execution evidence.

Report the selected engine, completed units, source scope/hashes, actual page changes, findings, and unresolved knowledge limits.
Keep partial maintenance visible. Reading sources or changing metadata alone is not semantic compilation.
