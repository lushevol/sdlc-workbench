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
Use the [source adapter boundary](../../adapters/sources/README.md) when adding a source integration.
Deterministic validation checks declared records and retained provenance.
Automatic external ingestion and source synchronization remain future capabilities.
Agent-assisted synthesis and classification use the shared skill and the shipped `KnowledgeTopic` contract.

The single runtime lives under `core/`.
The installed `ai_sdlc_workbench.ingestion.harness` module checks agent-assisted ingestion checkpoints.
It reuses workspace validation and checks retained history, locators, execution source hashes, and prepared content.
Read [the harness workflow](../../.agents/skills/ingest-knowledge/references/workflow.md#harness-commands) for commands and supported plan fields.
The checker reads local evidence and writes only its requested checkpoint report.
It supplies no automatic source collection, semantic classification, business execution, or approval.
