# Direct llm-wiki comparison

**Historical comparison.** The separate comparison workspace and redundant root source copy have been removed. The results below remain retained evidence. Use the [current wiki workflow](../../.agents/skills/llm-wiki/SKILL.md) and [conditional engine rule](LLM_WIKI_ROUTING_AND_CLEANUP_20261111.md#engine-rule) for the single active wiki.

## Inputs

The temporary standalone source copy at `llm-wiki-agent/`, revision `f03eff653886672ee8a92bb6a28faae9190d90d2`, was used for this comparison. Its 33 upstream files matched the skill's pinned source byte-for-byte, so the redundant root copy was removed after comparison. The skill-owned upstream copy remains unchanged.

The comparison compiled candidates in the separate `knowledge/llm-wiki-direct-compare/` workspace. Its 12 raw inputs were symlinks to `knowledge/candidates/`, so the candidate records have one content copy.

## Results

| Measure | Previous local-Codex wiki | Direct upstream-schema compilation |
| --- | ---: | ---: |
| Candidate source records | 12 | 12 |
| Source pages | 12 | 12 |
| Concept pages | 4 | 4 |
| Entity pages | 1 | 1 |
| Overview and graph nodes | 18 | 18 |
| Graph edges | 63 | 65 |
| Raw input symlinks | 12 | 12 |
| Broken wikilinks | 0 | 0 |

The direct compilation uses the upstream source-page format, candidate metadata, summaries, key claims, related-record links, and open questions. Five locally reasoned cross-source pages were then added in the same upstream schema: four concepts and one entity. The original upstream graph contains 18 nodes and 65 extracted edges with no inferred edges.

The previous output uses `wb-candidate-*` page names and the five derived topic pages. The direct output uses source-record slugs such as `kt-ces-migration-parity` and keeps the source record as the primary page.

Both outputs retain candidate or draft status. Neither establishes confirmed source authority, publication, implementation conformance, or business acceptance.

## Direct workspace commands

The temporary standalone source was separate from Workbench skill discovery and wrappers. The comparison graph was generated with the original upstream command:

```sh
python tools/build_graph.py --no-infer --report --save
```

The comparison workspace under `knowledge/llm-wiki-direct-compare/` was removed after the comparison; the measurements above are retained here. The former Workbench llm-wiki output is preserved in [the comparison snapshot](benchmark-evidence/wiki-comparison-snapshots-20261111.manifest.json) (`llm-wiki/README.md`). The richer OpenKB-generated documents remain active under `knowledge/llm-wiki/`; later maintenance follows the conditional rule above.
