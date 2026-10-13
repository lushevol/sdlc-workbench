# Ingestion responsibility

Ingestion preserves source material before interpretation.
Register the source identity, locator, owner, authority, and access method in `registry/sources.yaml`.
Keep credentials outside tracked declarations.

Retain unchanged source snapshots under `knowledge/raw/` when source access permits a local copy.
Record the source revision, retrieval time, original locator, hash, and snapshot path in the raw manifest.
Keep external source ownership intact.
Add a new snapshot when the source changes.
Do not rewrite earlier snapshot bytes or manifest history.

Use the [ingestion procedure](../../skills/ingest-knowledge/SKILL.md).
Use the [source adapter boundary](../../adapters/sources/README.md) when adding a source integration.
Deterministic validation checks declared records and retained provenance.
Automatic external ingestion and source synchronization remain future capabilities.

The single runtime lives under `core/`.
This directory defines the procedure boundary without an automatic ingestion engine.
