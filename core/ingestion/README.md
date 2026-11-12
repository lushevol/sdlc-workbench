# Ingestion responsibility

Ingestion derives reusable business-domain knowledge from inspected sources.
Keep `knowledge/` limited to domain Markdown records and navigation.
Exclude Workbench maintenance, raw sources, logs, code copies, fixtures, execution results, reports, and intermediate files.
Preserve useful source material outside the knowledge base before interpretation.

The shared skill can first review a batch without importing it.
Ingestion then classifies sources and creates connected topic candidates when requested.
Register the source identity, locator, owner, authority, and access method in `registry/sources.yaml`.
Keep credentials outside tracked declarations.

Retain unchanged source snapshots under `evidence/knowledge/sources/` when source access permits a local copy.
Record revisions, retrieval times, locators, hashes, and snapshot paths in `evidence/knowledge/manifest.yaml`.
Keep external source ownership intact.
Reuse original files already retained under `evidence/knowledge/sources/` without creating redundant copies.
Use a content hash revision when the original revision is unavailable.
Add a new snapshot when the source changes.
Do not rewrite earlier snapshot bytes or manifest history.

Use the [ingestion procedure](../../.agents/skills/ingest-knowledge/SKILL.md).
Use [source preparation](../../.agents/skills/prepare-knowledge-sources/SKILL.md) before deriving candidates from complete exports.
Its capture and selection operations reuse the existing commands and retained source identities.
The [lifecycle map](../../docs/KNOWLEDGE_LIFECYCLE.md) identifies reusable steps and their checkable outputs.
Use the [source adapter boundary](../../adapters/sources/README.md) when adding a source integration.
Deterministic validation checks declared records and retained provenance.
Local source preparation uses `ai-sdlc sources refresh`, `select`, `verify`, and `view`.
It accepts complete Markdown exports from registered filesystem collections.
It preserves source revisions and creates hash-bound selection indexes without copying full filtered source trees.
Read [source preparation](../../.agents/skills/ingest-knowledge/references/source-preparation.md) for commands, decisions, and limits.
Every generated source link records the original page hash and output hash.

New source bytes, changed policy, and changed governing context invalidate previous selections.
Missing pages remain visible without downstream deletion.

The stages are complete raw export → filtered source view → canonical knowledge → derived wiki.
Semantic classification, knowledge reconciliation, and publication remain agent and review responsibilities.
Automatic remote collection and source synchronization remain future capabilities.
Agent-assisted synthesis and classification use the shared skill and the shipped `KnowledgeTopic` contract.

The single runtime lives under `core/`.
The installed `ai_sdlc_workbench.ingestion.harness` module checks agent-assisted ingestion checkpoints.
It reuses workspace validation and checks retained history, locators, execution source hashes, and prepared content.
Read [the harness workflow](../../.agents/skills/ingest-knowledge/references/workflow.md#harness-commands) for commands and supported plan fields.
The checker reads local evidence and writes only its requested checkpoint report.
The checkpoint checker supplies no source collection, semantic classification, business execution, or approval.
