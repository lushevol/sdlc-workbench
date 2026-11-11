# Complete source exports

Place the complete current Markdown export under `raw/incoming/`.
That directory stays outside Workbench Git. You can replace its contents with the next complete export.
Do not remove irrelevant documents or edit mixed documents before importing them.
Never overwrite registered snapshots under `evidence/knowledge/sources/`.

Register the source collection in `registry/sources.yaml` using its filesystem type and an appropriate source ID.
Use the existing source ID when importing an updated export from the same collection.
The source preparation commands require a registered local collection.

```sh
ai-sdlc --workspace . sources refresh --source YOUR_SOURCE_ID --input raw/incoming
ai-sdlc --workspace . sources verify --source YOUR_SOURCE_ID
```

Refresh retains new source revisions and creates or updates the selection index.
New or changed pages require classification, including pages excluded before.
An absent page stays recorded without deleting its evidence or knowledge.

Follow the [source preparation procedure](../.agents/skills/ingest-knowledge/references/source-preparation.md) to record decisions and generate views.
Filtered views contain selected excerpts or source links. Every link records its source-page SHA-256.
Canonical knowledge uses the retained original source, revision, hash, and locator.
The wiki continues to use canonical knowledge records.

The runtime imports local UTF-8 Markdown. It does not fetch attachments or interpret unsupported formats.
Use approved source export tools before this stage when the original format differs.
