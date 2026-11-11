# Knowledge evidence and governance

Keep source snapshots, provenance, governance findings, and immutable audit events outside the domain knowledge tree.
Use [the knowledge contract](../../knowledge/README.md) for record and publication gates.
The [manifest](manifest.yaml) preserves source identities, revisions, hashes, and available snapshot paths.
A missing snapshot limits validation to the recorded reference.
Keep new task-generated evidence under its owning task.

The source pipeline is complete raw export → filtered source view → canonical knowledge → derived wiki.
Keep replaceable imports separate from registered snapshots.
The [source preparation commands](../../.agents/skills/ingest-knowledge/references/source-preparation.md) append revisions and reuse existing retained payloads.

`selections/COLLECTION.json` records source-page hashes, exact ranges, decisions, policy hashes, and governing context bindings.
Generate filtered excerpts or links in ignored working storage. Bind each generated entry to its original source and output hashes.
Retain original-to-output mappings when excerpting. Do not copy full raw trees merely to represent another processing stage.

Missing input remains visible. It does not authorize removal of source history, canonical knowledge, or wiki pages.

Keep authorized cleanup and relocation records beside the affected evidence.
Record prior locators, hashes, Git revisions, and reasons before deleting redundant artifacts.
Preserve previous manifest bytes and immutable audit events when relocating registered sources.
Keep source identities stable and start new baselines after a layout change.
