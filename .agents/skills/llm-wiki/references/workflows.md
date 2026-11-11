# Workbench wiki procedures

Keep one active document set at `knowledge/llm-wiki/`. It retains OpenKB's detailed page format regardless of which engine maintains it. Use `--project PATH` before a launcher command to select a different workspace.

## Project-scoped commands

Workbench owns project selection. Apply this table when the unchanged OpenKB skill shows native commands. Run relative commands from the Workbench root. From another directory, use the absolute launcher path and put `--project /absolute/workspace` before the command.

| Upstream example | Workbench operation |
| --- | --- |
| `openkb status` | `python3 .agents/skills/llm-wiki/scripts/wiki.py run status` |
| `openkb list` | `python3 .agents/skills/llm-wiki/scripts/wiki.py run list` |
| `openkb query "question"` | `python3 .agents/skills/llm-wiki/scripts/wiki.py run query "question"` |
| `openkb lint` | `python3 .agents/skills/llm-wiki/scripts/wiki.py run lint` |
| `openkb visualize` | `python3 .agents/skills/llm-wiki/scripts/wiki.py graph` |
| `openkb add`, `remove`, `watch`, `recompile`, `init`, `use` or interactive `chat` | Use authorized Workbench canonical ingestion/governance and the compile procedure below; these native transactions do not own the linked source files. |

The bridge supplies an explicit KB directory to native operations, independent of a global default. Keep the reported root at the selected workspace's `knowledge/llm-wiki/`. Use the source paths there for file reads. Do not run bare discovery or register a global KB to work around project selection. The original upstream skill remains unchanged reference material; these project-scoped commands take precedence in Workbench.

## Engine selection and installation

```sh
python3 .agents/skills/llm-wiki/scripts/wiki.py engine
python3 .agents/skills/llm-wiki/scripts/wiki.py install
```

OpenKB is the semantic engine only when **both** `OPENAI_API_BASE` and `LLM_API_KEY` are nonempty. The launcher reads single-line literal assignments from ignored `knowledge/llm-wiki/.env`, then falls back per value to the process environment. It accepts optional `export`, quoted literals and comments; it does not expand shell variables. Keep credentials private. The selector reports only presence, never values. Root project secrets, global OpenKB credentials, provider-specific keys and OAuth caches do not select the engine.

Set the provider-compatible `model` in ignored `.openkb/config.yaml`; the installer seeds `openai/gpt-4.1` as an example. A configured pair is not proof of valid credentials or model access. OpenKB is pinned at `ff54396e575ee6feb0113b631a34caa082b441cc` (`0.5.0rc2.dev3+gff54396e5`). Its isolated `.venv-openkb/` also supplies the local native format validator and graph viewer. `install --python PATH`, `install --wheelhouse PATH` and `install --offline` retain bounded installation options. Installation does not register a global default KB or authenticate to a provider.

The bridge rejects OAuth-only model prefixes and LiteLLM credential/endpoint overrides for semantic operations. Use the explicit pair and an API model; native dispatch binds that selected URL and token. Installation migrates only the exact old generated ChatGPT example configuration, preserving customized configuration.

When either value is absent, select **llm-wiki-agent in the current ADE session**. Read [the unchanged original workflow](../upstream/AGENTS.md) and apply the shared source/layout boundaries below. The no-credential workflow does not require launching OpenKB model commands. Existing pages remain available in both modes.

## Compile canonical records

```sh
python3 .agents/skills/llm-wiki/scripts/wiki.py compile
python3 .agents/skills/llm-wiki/scripts/wiki.py compile --source knowledge/confirmed
```

With both credentials configured, `compile` invokes OpenKB's original `compile_short_doc` using the selected URL and token explicitly, native configuration and an ingest lock. It reads full canonical records, deduplicates equal IDs, rejects conflicting records and filenames, links raw/full-text sources, and advances provenance bindings only after successful compilation and an unchanged source. Native failures are reported; they do not silently switch engines. Partial derived edits may remain after a failure, so inspect the diff before retrying.

Without both credentials, `compile` prints an **agent handoff** and changes no pages or bindings. The current ADE agent then performs the explicitly requested work: read each source fully, maintain meaningful summaries, extract/update concepts and entities, preserve contradictions, reconcile the index, and log source IDs/hashes and the actual execution mode. Do not report the handoff alone as completed compilation. Keep the existing rich page layout and detailed content; do not replace it with metadata exports or a second generated tree.

`raw/<name>.md` and `wiki/sources/<name>.md` remain relative symlinks to canonical records. `wiki/summaries/` holds derived source summaries; `wiki/explorations/` holds saved synthesis. Original llm-wiki-agent instructions call their derived source-summary folder `sources/`; apply that step to `summaries/` here. Preserve the existing OpenKB frontmatter and wiki-relative `[[concepts/...]]`, `[[entities/...]]`, `[[summaries/...]]` links. Use the index and relevant pages as the existing context; do not introduce a redundant overview document.

Never run either engine's source-owning native `add`, `remove`, `watch`, `recompile`, `ingest` or `refresh` on linked canonical inputs. The bridge blocks unsafe OpenKB commands, including interactive `chat`, whose `/add` command bypasses scoped compilation. Use Workbench canonical ingestion/governance for source changes; reconcile source-manifest origins and links explicitly when a record moves to confirmed storage. Symlink creation failure is an error, not permission to duplicate files. Source bindings and lifecycle history must remain truthful.

## Query and saved synthesis

In fallback mode use the original llm-wiki-agent query workflow in the current ADE context: read the index, relevant concepts/entities and summaries, follow links, reopen canonical sources for important claims, and answer with evidence and qualifications. Save an answer to `wiki/explorations/` only when requested.

```sh
python3 .agents/skills/llm-wiki/scripts/wiki.py run query "What does the wiki say about session renewal?"
```

With both URL and token, this uses native OpenKB query and makes a separate provider call. Otherwise it prints the current-agent handoff. Native OpenKB query cannot follow full-text symlinks resolving outside `wiki/`; use current-agent source reads for exact canonical content. A read-only answer does not refresh the wiki.

## Health and semantic review

`verify` checks source links/hashes and all six native OpenKB structural categories without an LLM. This validates the stored format in either semantic mode. `run status` and `run list` are also local. Semantic `run lint` follows the engine-selection rule: native OpenKB with the complete pair, current ADE llm-wiki-agent otherwise.

The original llm-wiki-agent health/graph scripts expect a different index, source-summary layout and bare-stem wikilinks. Running them directly on these shared OpenKB pages produces false findings or missing edges. Retain them unchanged as original capabilities; use the shared-format native validator and viewer below for this document set.

Review semantic fidelity, completeness, conflicts and applicability separately. Candidate sources remain candidate/draft, and no engine can supply missing publication approval or evidence of implemented behavior.

<a id="openkb-wiki-graph"></a>

## Wiki graph

```sh
python3 .agents/skills/llm-wiki/scripts/wiki.py graph
```

This invokes unchanged OpenKB `visualize --no-open` on the retained OpenKB document format in either semantic mode. It needs no URL/token or provider call. The self-contained viewer at `knowledge/llm-wiki/output/visualize/graph.html` embeds data and renderer assets. It extracts directed wikilinks from summaries, concepts and entities; source links, navigation and saved explorations are outside its node set.

This is the original OpenKB wiki graph, separate from Workbench's service dependency graph. Semantic engine selection does not rewrite existing pages or substitute service relationships for wiki links.
