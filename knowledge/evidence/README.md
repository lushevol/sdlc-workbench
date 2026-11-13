# Knowledge evidence and governance

Keep source snapshots, provenance, governance findings, and immutable audit events outside the domain knowledge tree.
Use [the knowledge contract](../README.md) for record and publication gates.
The [manifest](manifest.yaml) preserves source identities, revisions, hashes, and available snapshot paths.
A missing snapshot limits validation to the recorded reference.
Keep new task-generated evidence under its owning task.

The source pipeline is complete raw export → filtered source view → canonical knowledge → derived wiki.
The [source preparation commands](../../.agents/skills/ingest-knowledge/references/source-preparation.md) append revisions and reuse existing retained payloads.

## Complete source imports

Place the complete current Markdown export under `knowledge/evidence/incoming/COLLECTION/`.
Replace `COLLECTION` with the source's registered ID. Keep that ID for later exports from the same collection.
The incoming directory stays outside Workbench Git. Replace its contents with the next complete export.
Do not remove irrelevant documents or edit mixed documents before importing them.

Retained originals stay under `knowledge/evidence/sources/`. Never overwrite registered snapshot bytes with a new export.
Incoming files and retained snapshots have different lifecycles. Both belong in this evidence area.
No separate top-level raw directory is required.

Register new collections as `type: filesystem` in `registry/sources.yaml`.
Keep an existing collection's registered identity and location when importing another export. The input option selects its inbox.

```sh
ai-sdlc --workspace . sources refresh --source COLLECTION --input knowledge/evidence/incoming/COLLECTION
ai-sdlc --workspace . sources verify --source COLLECTION
```

Refresh retains new source revisions and updates the selection index.
New or changed pages require classification, including pages excluded before.
An absent page stays recorded without deleting its evidence or knowledge.
Follow the source preparation procedure to apply decisions and generate views.

## Source selections and retained history

`selections/COLLECTION.json` records source-page hashes, exact ranges, decisions, policy hashes, and governing context bindings.
Generate filtered excerpts or links in ignored working storage. Bind each generated entry to its original source and output hashes.
Retain original-to-output mappings when excerpting. Do not copy full raw trees merely to represent another processing stage.

Missing input remains visible. It does not authorize removal of source history, canonical knowledge, or wiki pages.

Keep authorized cleanup and relocation records beside the affected evidence.
Record prior locators, hashes, Git revisions, and reasons before deleting redundant artifacts.
Preserve previous manifest bytes and immutable audit events when relocating registered sources.
Keep source identities stable and start new baselines after a layout change.
