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

## Source lifecycle ownership

Existing engines own operational document maintenance. Workbench owns canonical authority and the linked-source boundary.

| Layer | Existing control | Shared-workspace adaptation |
| --- | --- | --- |
| Canonical knowledge | Workbench source history, review, and publication gates. | Preserve source IDs, versions, hashes, and governance state. |
| llm-wiki-agent | Full-source ingestion, semantic maintenance, health/lint, and hash-based source refresh. | Reuse semantic reasoning in ADE with OpenKB-format layout mappings. |
| Native OpenKB | Hash registry, deduplication, changed-source handling, compilation, removal, and journaled ingestion recovery. | Invoke the semantic compiler through the bridge while keeping canonical aliases immutable. |

Native source-owning transactions copy or remove their input artifacts.
They do not own Workbench's canonical records.
The bridge calls the compiler directly, so native `add` batch rollback does not cover the whole bridge update.
Partial derived pages can remain after failure. ADE's two provenance writes are also not crash-atomic.
Reuse the existing controls without introducing another canonical source approval lifecycle.

## Compile canonical records

Use these reusable operations in order:

1. [bind-wiki-sources](../../bind-wiki-sources/SKILL.md) selects canonical inputs, validates aliases, captures starting hashes, and prepares ADE recovery material.
2. [maintain-wiki-content](../../maintain-wiki-content/SKILL.md) applies the selected engine's semantic workflow and records reviewed output.
3. [finalize-wiki-update](../../finalize-wiki-update/SKILL.md) checks completion, provenance, and verification, with coordinated recovery where applicable.

```sh
python3 .agents/skills/llm-wiki/scripts/wiki.py compile
python3 .agents/skills/llm-wiki/scripts/wiki.py compile --source knowledge/candidates/security
```

With both configured settings, the bridge calls OpenKB's original semantic compiler under its ingest lock.
Without both settings, it returns an agent handoff and changes no pages or bindings.
Follow the reusable units after a handoff; do not report that output as completed compilation.

`raw/<name>.md` and `wiki/sources/<name>.md` remain relative symlinks to canonical records.
Derived summaries live in `wiki/summaries/`; saved synthesis lives in `wiki/explorations/`.
Direct ADE authoring uses the [native-format metadata contract](fallback.md#author-complete-native-format-pages).

Never run either engine's source-owning native `add`, `remove`, `watch`, `recompile`, `ingest`, or `refresh` on these links.
The bridge also blocks interactive `chat`, whose `/add` bypasses scoped compilation.
Use canonical ingestion/governance for source changes. Reconcile origins and aliases explicitly after authorized record moves.
Symlink failure is an error; do not duplicate canonical files as a workaround.
Missing sources do not authorize automatic deletion.

## Query and saved synthesis

In fallback mode use the original llm-wiki-agent query workflow in the current ADE context: read the index, relevant concepts/entities and summaries, follow links, reopen canonical sources for important claims, and answer with evidence and qualifications. Save an answer to `wiki/explorations/` only when requested.

```sh
python3 .agents/skills/llm-wiki/scripts/wiki.py run query "What does the wiki say about session renewal?"
```

With both URL and token, this uses native OpenKB query and makes a separate provider call. Otherwise it prints the current-agent handoff. Native OpenKB query cannot follow full-text symlinks resolving outside `wiki/`; use current-agent source reads for exact canonical content. A read-only answer does not refresh the wiki.

## Health and semantic review

Use [check-wiki-health](../../check-wiki-health/SKILL.md) for local hash/link/structure checks and requested semantic review.
It reports findings without advancing provenance or publication state.
Use [finalize-wiki-update](../../finalize-wiki-update/SKILL.md) to finish a reviewed update.

Requested engine lint uses `run lint` with OpenKB only when both URL and token are configured.
Otherwise use original llm-wiki-agent reasoning in the current ADE session.
Native lint writes a report and log even without `--fix`; it is separate from read-only health inspection.

<a id="openkb-wiki-graph"></a>

## Wiki graph

```sh
python3 .agents/skills/llm-wiki/scripts/wiki.py graph
```

This invokes unchanged OpenKB `visualize --no-open` on the retained OpenKB document format in either semantic mode. It needs no URL/token or provider call. The self-contained viewer at `knowledge/llm-wiki/output/visualize/graph.html` embeds data and renderer assets. It extracts directed wikilinks from summaries, concepts and entities; source links, navigation and saved explorations are outside its node set.

This is the original OpenKB wiki graph, separate from Workbench's service dependency graph. Semantic engine selection does not rewrite existing pages or substitute service relationships for wiki links.
