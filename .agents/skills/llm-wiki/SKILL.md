---
name: llm-wiki
description: Use the fully installed llm-wiki-agent to ingest, refresh, query, and review a source-linked native wiki and build its original wikilink graph over Workbench knowledge.
---

# Build and maintain the knowledge wiki

Use the complete, unchanged [SamurAIGPT/llm-wiki-agent](references/upstream.md) installed under [upstream/](upstream/).
Its original tools, agent instructions, converters, workflows, and native graph implementation remain available.
Read [the mode procedures](references/workflows.md) for the requested operation and its model or write requirements.
The external [launcher](scripts/wiki.py) manages installation, source integrity, export, and isolated execution.
Do not edit vendored files or replace upstream algorithms with Workbench implementations.

## Select the source and output boundary

The persistent native workspace is `knowledge/llm-wiki/`, with `wiki/`, `raw/`, and `graph/` data directories.
The runtime uses unchanged upstream implementation copies beside those data directories under `knowledge/llm-wiki/`.
Those runtime code copies remain ignored; the complete vendored source stays pristine.
Dependencies live in `.venv-llm-wiki/`, separate from the Workbench runtime.
Changing the shell directory alone cannot redirect upstream data paths. Use the launcher.

The native wiki is derived knowledge, separate from canonical Workbench records and publication.
Retain canonical IDs, versions, hashes, lifecycle states, source citations, conflicts, and applicability limits in exported pages.
Reopen canonical records and relevant sources before using a wiki claim for engineering decisions.
Use [ingest-knowledge](../ingest-knowledge/SKILL.md) and [govern-knowledge](../govern-knowledge/SKILL.md) for changes to canonical intended meaning.
Native ingestion, saved answers, semantic lint, healing, graph edges, and successful commands cannot promote canonical knowledge.

## Use the supported wiki layout

```text
knowledge/llm-wiki/
  raw/                              # Native source inputs.
  wiki/
    index.md                        # Native catalog.
    log.md                          # Upstream operation log.
    overview.md                     # Living synthesis.
    sources/<unique-stem>.md
    entities/<unique-stem>.md
    concepts/<unique-stem>.md
    syntheses/<unique-stem>.md
  graph/
    graph.json                      # Original {nodes, edges, built} output.
    graph.html                      # Original upstream renderer.
    graph-report.md                  # Optional upstream graph report.
```

Use upstream page frontmatter and native `[[filename-stem]]` links.
Export uses unique lowercase filename stems, including across directories, and retains provenance.
Directory `index.md` navigation pages cannot be used directly as graph nodes: upstream excludes that filename everywhere.
Keep canonical records and registered original evidence at their existing locations.

## Complete the requested mode

Run from the selected workspace root:

```sh
python3 .agents/skills/llm-wiki/scripts/wiki.py install
python3 .agents/skills/llm-wiki/scripts/wiki.py export
python3 .agents/skills/llm-wiki/scripts/wiki.py graph --no-infer --report --save
python3 .agents/skills/llm-wiki/scripts/wiki.py verify
```

`export` defaults to the raw `knowledge/candidates/` records and converts them to native source pages and wikilinks.
Use `export --source knowledge/confirmed` when confirmed source records become available.
`graph` invokes the original upstream `tools/build_graph.py`, with arguments passed through unchanged.
Use `run <tool> [args...]` for original tools such as `health`, `ingest`, `query`, `lint`, `refresh`, and `heal`.
For another workspace, put `--project PATH` before the command. Inspect launcher and tool help for options.

Use `--no-infer` for an explicit-link graph without model calls.
The original renderer loads vis-network from an external CDN; graph generation itself does not need that asset.
Use the [service graph skill](../service-dependencies-graph/SKILL.md) for its separate architecture and governed-evidence projection.
It must not substitute for the upstream wiki graph when the user requests llm-wiki graph generation.

Report exported record coverage, actual tool results, source integrity, model use, and material limits.
Structural health and connected pages do not establish semantic truth, publication, deployment, or verified business behavior.
