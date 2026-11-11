# Native wiki workflows

Commands below run from the selected workspace root.
For a different workspace, place `--project PATH` before `install`, `export`, `graph`, `run`, or `verify`.
The launcher isolates data without changing upstream implementation files.
Read the original [agent instructions](../upstream/AGENTS.md) for detailed native authoring procedures.

## Install and inspect integrity

```sh
python3 .agents/skills/llm-wiki/scripts/wiki.py install
python3 .agents/skills/llm-wiki/scripts/wiki.py verify
```

`install --python PATH` selects Python 3.11–3.13 for `.venv-llm-wiki/` and the complete dependency set.
Inspect installation results before reporting availability of converters or model-backed tools.
Keep the complete [upstream tree](../upstream/) unchanged and use its [source lock](../upstream-lock.json) for integrity checks.
Do not patch original scripts to relocate their data; their paths derive from their implementation location.
The launcher prepares unchanged runtime implementation copies beside the persistent data under `knowledge/llm-wiki/`.
Runtime code copies remain ignored and are separate from the pristine vendored tree.

## Export existing Workbench knowledge

```sh
python3 .agents/skills/llm-wiki/scripts/wiki.py export
python3 .agents/skills/llm-wiki/scripts/wiki.py run health --json
python3 .agents/skills/llm-wiki/scripts/wiki.py run ingest --validate-only
```

The default export reads `knowledge/candidates/` raw records and produces native `knowledge/llm-wiki/wiki/` source pages.
It supplies unique lowercase filename stems, candidate IDs and versions, native frontmatter, resolvable `[[wikilinks]]`, and source-bound provenance.
Use `export --source knowledge/confirmed` after confirmed source records are introduced.
Inspect the export inventory and actual coverage before claiming all canonical records or original sources were read.
Canonical IDs, versions, lifecycle states, full hashes, and unresolved questions remain relevant after export.
Native page types describe wiki roles; they are not Workbench governance states.

Refresh exports after authorized canonical or navigation changes, then rebuild the native graph when that output is requested.
Preserve human-authored changes and native ingest outputs when reconciling an export; inspect conflicts rather than overwriting unrelated work.
Keep changed-source provenance, predecessor identity, and publication history outside the derived export's authority.
A candidate successor cannot silently become applicable published policy.

## Native ingest and conversion

The original tools accept Markdown and supported non-Markdown formats through the installed converters.
Use `run ingest <source-path> [other-paths...]` with original upstream arguments; inspect tool help and supported formats first.
Use `run file_to_md` or `run pdf2md` for the original conversion workflows.
Resolve source arguments for the selected runtime and keep retained original snapshots immutable.

Native ingest can create source, entity, and concept pages, update the index and overview, and append the native log.
Model-backed ingestion sends selected source context to the configured provider.
Use the current coding agent's original upstream workflow when no second model API is desired.
Keep unsupported claims and contradictions explicit in either route.

For reusable canonical intended knowledge, continue through [ingest-knowledge](../../ingest-knowledge/SKILL.md) and its provenance and candidate checks.
Native wiki outputs supply proposals and navigation; they do not replace source review or canonical publication requirements.

## Query and saved synthesis

For an ordinary knowledge answer, read the native index, relevant pages, canonical records, and material original sources.
Use [query-knowledge](../../query-knowledge/SKILL.md) for claim-level citations, applicability, confidence, and evidence distinctions.
Read-only questions do not require running a model tool or modifying the wiki.

The original scripted route is available when requested:

```sh
python3 .agents/skills/llm-wiki/scripts/wiki.py run query "What does the wiki say about session renewal?"
```

This script calls the model and appends `wiki/log.md` even without `--save`.
Its page selection is bounded and does not resolve applicable published Workbench versions automatically.
Use the original `--save syntheses/<unique-stem>.md` only for requested reusable synthesis.
Saved answers remain derived and need inspected citations; upstream synthesis metadata does not supply canonical provenance or approval.

## Health, semantic lint, refresh, and heal

Run original structural health before semantic review:

```sh
python3 .agents/skills/llm-wiki/scripts/wiki.py run health --json
python3 .agents/skills/llm-wiki/scripts/wiki.py run ingest --validate-only
```

Health checks empty pages, index synchronization, and source-log coverage without model calls.
Ingest validation reports native broken links and index omissions; inspect reported issues as well as the process exit code.
Check export bindings and full canonical hashes separately: structural health does not establish freshness or semantic support.
Use `health --save` for the original `wiki/health-report.md` output when requested.

`run lint` performs original structural and model-based semantic analysis.
Review contradictions, missing exceptions, unsupported additional behavior, stale summaries, and applicability against exact canonical sources.
Keep unresolved business decisions in the existing living question document.
Use independent retrieval questions where useful, including an unsupported question and a proposed requirement.

`run refresh --dry-run` lists upstream refresh candidates; `run refresh` can call ingest and rewrite native pages.
Inspect actual raw inputs and full hashes before relying on a stale-source decision.
`run heal` remains available and can generate native entity pages through the model.
Review those pages as derived proposals. Missing links and dense graphs cannot establish a missing domain rule.
No tool result automatically creates canonical knowledge, approves an intended rule, or closes a governance finding.

## Original upstream graph

```sh
python3 .agents/skills/llm-wiki/scripts/wiki.py graph --no-infer --report --save
```

This command invokes the unchanged upstream `tools/build_graph.py` against the populated native wiki.
Use that implementation for llm-wiki graphs. The service-dependencies graph is a separate output with different semantics.

The original graph writes `{nodes, edges, built}` to `knowledge/llm-wiki/graph/graph.json` and renders `graph.html` beside it.
Nodes retain page IDs, labels, types, paths, complete Markdown, preview, community group, and degree-based value.
Explicit edges retain `from`, `to`, `type: EXTRACTED`, and confidence `1.0` for an existing textual link.
That confidence does not grade the truth of the relationship.

`--no-infer` skips model inference and inference-cache writes; existing cache files may still be read.
The graph operation appends the native wiki log.
`--report` needs NetworkX. `--save` writes `graph/graph-report.md` only when a report is generated.
Report generation appends a second log event. `--save` alone does not generate a report.
`--clean` deletes an existing inference checkpoint, including alongside `--no-infer`.
Omitting `--no-infer` enables the original configured model inference and its cache/checkpoint behavior.

Upstream excludes `index.md`, `log.md`, and `lint-report.md` from graph nodes.
Wikilinks resolve by filename stem; keep stems unique across the wiki and use simple `[[stem]]` targets.
Missing targets are omitted from extracted edges. Reciprocal edges can collapse through original unordered-pair deduplication.
Graph reports describe connectivity, orphan pages, hubs, communities, bridges, and missing referenced pages.
These metrics do not establish domain completeness, dependency direction, source authority, or business acceptance.

Open `knowledge/llm-wiki/graph/graph.html` to inspect native filters and page details.
The unchanged renderer loads vis-network from an external unpkg URL; opening the HTML requires asset access unless already cached.
Check the actual browser result before claiming a working visualization.
Retain source-integrity results, nonempty node/edge counts, expected edge types, resolved links, and actual model-use limits in the completion report.
