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
python3 .agents/skills/llm-wiki/scripts/wiki.py plan --source knowledge/candidates --output .workbench/wiki/plan.json
python3 .agents/skills/llm-wiki/scripts/wiki.py compile
python3 .agents/skills/llm-wiki/scripts/wiki.py compile --source knowledge/candidates/security
python3 .agents/skills/llm-wiki/scripts/wiki.py compile --source knowledge/candidates --record knowledge/candidates/security/access.md --recipe default
```

Run `plan` before semantic dispatch. It uses local hashes and metadata without credentials, runtime installation, or model calls.
With `--output`, keep the full inventory on disk and return compact counts and queued paths.
Choose an unused output path below the selected workspace's ignored `.workbench/` directory.
Use repeated `--record` for exact workspace-relative canonical inputs inside `--source`.
Directory planning discovers new records and reports missing bound records without deleting their history.
Keep the same nonsecret `--recipe` across planning, compilation, and review.
Change its identity when semantic settings or governing policy change, including the selected model.
The planner also binds the incremental contract, pinned compiler revision, and wiki authoring policy hash.
It does not read private model configuration to infer recipe changes.

| Planned result | Next operation |
| --- | --- |
| `unchanged` | Skip semantic compilation; reviewed source, bindings, dependencies, and outputs still match. |
| `new`, `changed`, `recipe_changed`, or `retry` | Maintain the selected source and its affected outputs. |
| `bootstrap_review` | Review existing legacy pages and record completion; automatic recompilation is unnecessary. |
| `pending_review` | Inspect generated output and finish actual semantic review before completion. |
| `repair_review` | Reconcile bindings or changed/missing outputs, then review the affected scope. |
| `missing` | Investigate missing canonical input; preserve history and unsupported-claim qualifications. |

`--force` explicitly requests recompilation of selected present inputs, including legacy bindings.
Use it only when regeneration is intended. Missing completion evidence alone calls for review.
Native compiler return records a pending attempt, not successful semantic completion.
Unchanged completed inputs make zero additional compiler calls.

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

## Reviewed completion receipts

After actual semantic review, finalize either engine's work through the same command:

```sh
python3 .agents/skills/llm-wiki/scripts/wiki.py review --receipt .workbench/wiki/RUN/review.json
```

This local operation requires the installed OpenKB schema and lock helpers, but performs no provider call or credential read.
Prepare a JSON receipt using actual reviewed hashes and scope:

```json
{
  "recipe": "default",
  "engine": "llm-wiki-agent",
  "reviewed_by": "ACTUAL_REVIEWER",
  "reviewed_at": "2026-11-12T00:00:00Z",
  "review_note": "REPLACE_WITH_ACTUAL_SEMANTIC_REVIEW",
  "sources": [{
    "path": "knowledge/candidates/security/access.md",
    "sha256": "SOURCE_BEFORE_SHA256",
    "outputs": ["wiki/summaries/access.md", "wiki/index.md"],
    "withdrawn_outputs": []
  }],
  "outputs": [
    {"path": "wiki/summaries/access.md", "sha256": "REVIEWED_OUTPUT_SHA256", "sources": ["CANONICAL_ID"], "note": "ACTUAL_REVIEW"},
    {"path": "wiki/index.md", "sha256": "REVIEWED_INDEX_SHA256", "sources": ["ALL_PRESERVED_SOURCE_IDS"], "note": "ACTUAL_REVIEW"}
  ]
}
```

Replace placeholders. Copy the full expected output scope from the plan, including concepts, entities, contradictions, and affected explorations.
Inspect prior dependents as well as newly selected pages when sources withdraw claims.
Each output lists the canonical IDs whose claims its complete reviewed bytes preserve.
Shared-page review must preserve every existing owner or explicitly withdraw that source's support.
Updated global navigation hashes do not independently force unrelated canonical inputs through compilation.

Use source-level `unchanged_reason` when review supports unchanged summary bytes after a source change.
Use `relocation_reason` when an authorized canonical move changes the binding path.
For former dependencies, add `withdrawn_outputs: [{"path": "wiki/concepts/FORMER.md", "reason": "ACTUAL_DISPOSITION"}]`.
Also supply `withdrawal_review_note` and review the former output's current bytes after removing or qualifying unsupported claims.
For an authorized removed derived page, its output entry uses `sha256: null` and `disposition: "removed"`.
Missing raw or canonical sources alone authorize no deletion.
Affected saved explorations require reviewed qualification or authorized regeneration before completion.

The bridge stores compact completion, output ownership, and pending attempts under existing `source-manifest.json` metadata.
It checks native structure, source/output bytes, relative aliases, and paired registry consistency under the native lock.
It retains both provenance before-images and intended hashes under ignored `.workbench/wiki/` before replacing either binding file.
Failed writes or verification restore both before-images only when current bytes belong to that attempt.
Crash interruption still requires coordinated recovery; inspect its recovery record and preserve unrelated writes.
Semantic edits remain available for review after failures.
Finalization still requires full wiki binding and structural verification.
Another stale source or shared-output owner can block completion; retain successful compilation and pending attempts for reconciliation.
Use [finalize-wiki-update](../../finalize-wiki-update/SKILL.md) for completion and interrupted recovery.
Hash receipts record declared review; they do not authenticate actors, establish semantic truth, or grant canonical publication.

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
