# Workbench shared knowledge wiki

Use the [Workbench wiki workflow](../../.agents/skills/llm-wiki/SKILL.md). This is the single active derived wiki for the project. Select OpenKB for semantic operations only when both `OPENAI_API_BASE` and `LLM_API_KEY` are explicitly configured; otherwise use the original [llm-wiki-agent workflow](../../.agents/skills/llm-wiki/upstream/AGENTS.md) in the current ADE session.

Project selection takes precedence over native skill examples. Use the [command translations](../../.agents/skills/llm-wiki/references/workflows.md#project-scoped-commands), starting with the bridge's `run status` from the Workbench root. From another directory, invoke the absolute launcher with `--project` set to this Workbench. Bare `openkb status` can select a different global KB.

`wiki/` contains the active OpenKB compilation. Its [catalog](wiki/index.md) routes to summaries, concepts, entities, and explorations. `raw/` and `wiki/sources/` are links to canonical records; preserve their bytes and use Workbench ingestion/governance to change intended meaning. Exact bindings are in [source-manifest.json](source-manifest.json).

Keep these existing detailed OpenKB-format pages in both modes. For fallback maintenance, apply the original agent's source-summary steps to `wiki/summaries/`, preserve `wiki/sources/` and `raw/` as canonical links, and save requested synthesis under `wiki/explorations/`. Do not run native ingest/refresh scripts that assume writable source files. Do not create another wiki or redundant overview. OpenKB's local format validation and original visualization remain available without model credentials. Existing page/compilation provenance does not change when the selected maintenance engine changes.

The model and private authentication configuration are local runtime settings. This workspace contains candidate/draft knowledge; generated pages, graph edges, and successful tool operations do not establish approved intent or deployed behavior.
