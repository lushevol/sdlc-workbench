# Prepare source documents before knowledge ingestion

Use the installed local source commands before deriving knowledge from a complete Markdown export.
They preserve sources and apply inspected selections. They do not classify meaning or approve knowledge.

## Processing stages

1. **Complete raw export:** accept the whole collection in ignored `evidence/knowledge/incoming/COLLECTION/`.
2. **Filtered source view:** retain source revisions, record selections, and generate exact excerpts or source links when needed.
3. **Canonical knowledge:** reconcile intent across selected sources through the ingestion and governance procedures.
4. **Derived wiki:** compile canonical records through the [wiki bridge](../../llm-wiki/SKILL.md).

The input directory is replaceable. Registered snapshots under `evidence/knowledge/sources/` remain protected.
Keep these lifecycles separate within the existing evidence area. No top-level raw directory is required.
Keep generated views outside `knowledge/`. A view does not create another source of authority.
The commands do not refresh wiki pages, publish knowledge, or delete missing source material.

## Refresh the complete export

Register the source collection as `type: filesystem` in `registry/sources.yaml`.
Use a workspace-relative directory containing Markdown source files.
Use regular UTF-8 Markdown files, each no larger than 16 MiB.
Keep source preparation paths workspace-relative and free of symbolic links.
Use the source's actual registered ID in place of `COLLECTION`.
Keep existing registered source identities and locations. The input option selects the replaceable inbox for the current export.

```sh
ai-sdlc --workspace PATH sources refresh --source COLLECTION --input evidence/knowledge/incoming/COLLECTION
```

Refresh records source identity, revision, snapshot location, and SHA-256 before interpretation.
It reuses retained bytes and prior source records when possible.
It appends new revisions without overwriting registered snapshots.
The selection index lives at `evidence/knowledge/selections/COLLECTION.json`.

New and changed pages require review, including previously excluded pages.
Changed policy or governing context also invalidates previous decisions.
Missing pages remain visible as missing input. They do not revoke requirements or trigger downstream deletion.

The default policy is [source-filter.yaml](../assets/source-filter.yaml).
Supply `--policy WORKSPACE_RELATIVE_PATH` to refresh with a project-specific policy.
The index records the exact policy hash.
The runtime detects stale bindings. An agent still determines whether each passage supports intended behavior.

## Apply the filter pattern

Read each complete source and necessary linked context before deciding.
Use the policy's topics and patterns to select intended system behavior and required domain context.
Use filenames and keywords only to locate candidate material.
Technical content qualifies when it explains intended responsibilities or contracts relevant to the project.

| Decision | Meaning |
| --- | --- |
| `KEEP` | Retain the complete source page as substantive intent or necessary context, with its actual status and limits. |
| `KEEP_SECTIONS` | Select relevant passages from a mixed document. Preserve their conditions and definitions. |
| `EVIDENCE_ONLY` | Keep implementation, deployment, or observed results outside the intent input. |
| `EXCLUDE` | Omit unrelated process material, generic tutorials, or empty templates from the intent input. |
| `HOLD` | Missing context or conflicting meaning prevents a reliable selection. |

`NEEDS_REVIEW` is the runtime's pending state. It is not a semantic source decision.
Relevant draft proposals remain proposed intent. Source age alone does not justify exclusion.
Do not derive a target requirement from code or a passing test.

Record decisions in a JSON file inside the workspace:

```json
{
  "schema_version": 1,
  "source_id": "COLLECTION",
  "decisions": [
    {
      "path": "design/page.md",
      "sha256": "0000000000000000000000000000000000000000000000000000000000000000",
      "decision": "KEEP_SECTIONS",
      "reason": "The selected section defines the intended rejection rule.",
      "ranges": [[10, 18]],
      "topic": "Request validation",
      "intent_status": "proposed",
      "context": []
    }
  ]
}
```

This example is illustrative. Replace its path, hash, ranges, and meaning with inspected source evidence.
Paths identify pages relative to the imported collection.
Use the current source hash from the selection index.
Ranges use one-based inclusive physical lines. Keep them ordered and disjoint.
`KEEP_SECTIONS` requires selected ranges. Other exclusion decisions have no kept ranges.
`KEEP` requires the complete source page. Omit its ranges to select all source lines automatically.

Use `context` for governing workspace files, such as applicable clarification sources.
Each context entry records `path` and `sha256`.
Keep authority, applicability, and unresolved questions explicit in the decision rationale and resulting knowledge.

```sh
ai-sdlc --workspace PATH sources select --source COLLECTION --decisions decisions.json
ai-sdlc --workspace PATH sources verify --source COLLECTION
```

The checker rejects stale source bindings and invalid source ranges.
It checks recorded hashes. It cannot decide whether selected text proves the proposed meaning.
Successful refresh and selection commands can still report `NEEDS_REVIEW` for unresolved pages.
`verify` returns a nonzero exit status unless the collection is `READY`.

## Generate the filtered view

```sh
ai-sdlc --workspace PATH sources view --source COLLECTION --output .workbench/ingestion/filtered/RUN
```

Choose a new output directory for each view.
Views use exact selected excerpts or relative source links, with original-to-output line mappings where applicable.
Whole-page selections use links when supported. Otherwise, the runtime creates a byte-identical copy.
Each view entry records the original source ID, revision, SHA-256, snapshot, and emitted output hash.
The view's `manifest.json` records these entries, selection and policy bindings, and omitted pages.
Verify those bindings before following a link or using a passage as evidence.
Views can contain current reviewed selections while omitting pending, held, or missing pages.
The output reports those omissions. A partial view does not establish complete source collection coverage.
Stale selected bindings must not render as current source content.

Do not manually maintain generated excerpts. Record corrected selections and generate another view.
Do not silently repair policies, invent missing values, or remove exceptions during cleaning.
The first cleanup operation selects exact text. Semantic synthesis belongs in canonical knowledge ingestion.

Canonical knowledge cites original retained source revisions and exact source ranges.
The filtered view supplies convenient input. It does not replace the raw source manifest.
Keep only the selection metadata and retained bytes required for provenance and reproduction.

## Continue through knowledge and wiki

Return to [the ingestion workflow](workflow.md#4-draft-the-connected-knowledge) after source review.
Create candidate records, preserve unresolved rules, and complete the existing checks and applicable governance gates.
Then compile the affected canonical records through the wiki bridge.

The wiki's `raw/` and `wiki/sources/` entries are aliases to canonical knowledge records.
They are separate from the replaceable export and filtered source view.
Keep their canonical source hashes in the wiki source manifest and verify them before reuse.
Never write through those aliases or run upstream refresh against them.
