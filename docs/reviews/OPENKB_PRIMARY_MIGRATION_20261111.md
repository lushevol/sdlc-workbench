# OpenKB primary wiki migration — 11 November 2026

## Follow-up rule and duplicate cleanup

Source: user message in the same Workbench knowledge chat, 11 November 2026. Exact wording:

> OK, now safe remove duplicate llm wikis documents only keep authed one. The rule is openKB as primary llm-wiki if provide llm url and token other wise use llm-wiki-agent instead.

This supersedes unconditional OpenKB selection below. Keep one active wiki at `knowledge/llm-wiki/`, retaining its richer compiled documents. Select OpenKB only when both an explicit LLM URL and token are available; otherwise select the unchanged llm-wiki-agent workflow in the current ADE session. Existing page provenance remains historical fact when the maintenance engine changes. Preserve comparison results while consolidating their redundant browsable snapshots.

See [the current selection and cleanup report](LLM_WIKI_ROUTING_AND_CLEANUP_20261111.md) for the implemented rule and verified archive. The remainder records the earlier migration state before this follow-up.

## Earlier migration state

OpenKB now supplies Workbench's active compiled knowledge wiki. The previous llm-wiki documents are archived for comparison, the saved OpenKB compilation replaces them, and Workbench skills route through the OpenKB workflow.

## Authorizing input

Source: user message in the Workbench knowledge comparison chat, 11 November 2026. Exact wording:

> OK, replace existing llm-wiki documents with OpenKB wiki documents, which openkb generated are better. Then install openkb as primary llm wiki solution for workbench. Can openkb be used in context of ADE without providing LLM url and token ?

Earlier user constraints retained: link canonical raw files rather than duplicate them; preserve comparison materials; use the wiki engine's actual knowledge graph rather than the Workbench service dependency graph; candidate sources apply now, confirmed sources later.

## Result and provenance

| Item | Result |
| --- | --- |
| Primary engine | [VectifyAI/OpenKB](https://github.com/VectifyAI/OpenKB), revision `ff54396e575ee6feb0113b631a34caa082b441cc` |
| Installed package | `0.5.0rc2.dev3+gff54396e5`, isolated `.venv-openkb`, Python 3.13.14 |
| Native skill | [Official skill](../../.agents/skills/openkb/SKILL.md), schema/command references and Apache-2.0 license copied unchanged; [source lock](../../.agents/skills/openkb/source-lock.json) binds the bytes |
| Workbench integration | Existing [llm-wiki skill ID](../../.agents/skills/llm-wiki/SKILL.md) now bridges to OpenKB; shared packaging includes the native skill and Claude alias |
| Active wiki | [Catalog](../../knowledge/llm-wiki/wiki/index.md): 12 summaries, 34 concepts, 39 entities, 6 saved explorations |
| Input provenance | [Source manifest](../../knowledge/llm-wiki/source-manifest.json): 12 canonical record IDs, paths, versions, lifecycle fields and SHA-256 bindings |
| Source storage | 12 `raw/` links and 12 `wiki/sources/` links, all relative symlinks to the canonical classified candidate records |
| Original OpenKB compilation | Imported from [preserved benchmark](benchmark-evidence/wiki-comparison-snapshots-20261111.manifest.json) (`openkb/wiki/index.md`), previously compiled with DeepSeek; no new provider call made during migration |
| Previous llm-wiki output | [Archived comparison](benchmark-evidence/wiki-comparison-snapshots-20261111.manifest.json) (`llm-wiki/README.md`), including the prior exporter implementation and a 26-file hash inventory |
| Previous upstream source | `.agents/skills/llm-wiki/upstream/` remains unchanged as historical reference; it is no longer the active engine |

The installed wheel SHA-256 is `4c6378fdd4a72f4b3a169167821a2caf28e568f25e36b172aeadf3ec54f4d179`. Package installation used the cached pinned source/wheel and prepared dependencies. Dependency validation passed for all 112 installed packages. Workbench's base environment and standard offline bundle do not absorb the separate OpenKB runtime.

Active pages received limited agent-authored repairs after import: one missing release-governance concept, 14 broken wikilinks, six self-links, and ambiguous descriptions of two new CES fields versus existing fields. The [operation log](../../knowledge/llm-wiki/wiki/log.md) records these changes. The historical OpenKB benchmark pages were not repaired or overwritten.

## ADE use and authentication

**Yes: the current ADE agent can use OpenKB's wiki without configuring another LLM URL or token.** This is the default Workbench route. The agent reads the index, focused concepts/entities, summaries, and linked canonical sources using its normal tools and reasons in its existing model context. Explicitly requested maintenance can author pages using the OpenKB schema and reconcile the index and log. The unchanged official skill itself prefers current-agent reading over a second `openkb query` call.

The standalone CLI is a separate client. Workbench `compile` invokes the original OpenKB semantic compiler; native `query` and semantic `lint` use independent LiteLLM model calls. Supported `chatgpt/<model>` routes can use device OAuth without a manually supplied API key or custom URL. They may require a separate device login and do not automatically reuse Codex's authentication. Installation seeds an ignored configuration with `chatgpt/gpt-5.4` as an example; account/model access and live OAuth were not tested. Other providers retain their own private configuration requirements.

Local installation, `verify`, `status`, `list` and graph visualization require no model access. Current-agent maintenance and native CLI compilation must be described separately; no deterministic export is represented as semantic compilation.

## Source and workflow boundaries

The bridge calls OpenKB's original `compile_short_doc`, uses native provider configuration and an ingest lock, and preserves linked full-text inputs. It rejects conflicting IDs, filename collisions, inputs resolving outside the project, and source changes during compilation. Source hash bindings advance only after a successful compiler return and an unchanged source. Manifest reads occur inside the lock so simultaneous runs retain existing bindings.

Native `add`, `remove`, `watch`, `recompile`, `init`, `use`, and `delete-kb` assume owned files or alter KB selection/state. They are blocked through the bridge for this linked corpus, including an attempted leading `--` dispatch bypass. Use canonical ingestion/governance plus bridge compilation. Compilation may update derived pages before a later failure; inspect the diff and failure before retrying. Moving a candidate record to a confirmed location requires reconciliation of its existing source links before compilation; the bridge refuses a conflicting link rather than silently repointing it.

Native CLI query can read compiled pages, but its file tool confines resolved paths to the wiki root and therefore rejects the external canonical source symlinks. ADE file tools can read those exact canonical records. This upstream limitation is documented, with no patch to OpenKB.

Workbench canonical validation, ingestion baselines, `knowledge.local` inventory/access and service-graph knowledge projection now exclude the exact reserved `knowledge/llm-wiki/` workspace. This prevents native page types, state and source aliases from being interpreted as canonical records or feeding back into the service graph. Provider access also rejects symlink aliases into the derived workspace. Canonical records elsewhere, including nested directories named `llm-wiki`, retain strict validation. The OpenKB bridge separately checks its own pages and bindings.

Candidates remain candidate/draft. Compilation, structurally valid pages, graph links and package tests do not establish approved policy, production behavior or acceptance. Release-window duration (10 versus 24 hours) and urgent-release confirmation versus proceeding on silence remain unresolved source questions.

## Validation

| Check | Observed result |
| --- | --- |
| Canonical integrity | All 12 source hashes match the original saved OpenKB inputs; all 24 source aliases are valid relative symlinks |
| Former comparison integrity | All 26 archived file hashes match the preservation inventory |
| Native structural lint | Zero broken links, orphans, missing entries, index-sync issues, invalid frontmatter or missing required OKF fields |
| Native graph | Original `visualize --no-open`; [interactive HTML](../../knowledge/llm-wiki/output/visualize/graph.html), 85 nodes and 1,468 directed wikilinks; renderer and data embedded |
| Browser graph check | Local headless Chrome rendered the canvas; native search/inspector and mind-map mode passed, with zero JavaScript errors or external requests |
| Source-boundary tests | 14 tests pass without a provider, covering original compiler dispatch, links, lifecycle bindings, failure/source races, conflicting sources, native mutation guards and all six verification categories |
| Shared skill packaging | 23 workspace-layout tests pass, including sdist/wheel/initialization and unchanged native/legacy skill byte checks |
| Canonical integration | 63 governance, ingestion, graph-projection and derived-boundary tests pass; 13 provider tests pass, using permitted loopback access for the local Eureka mock |
| Workbench validation | `ai-sdlc --workspace . validate`: VALID, 14 canonical/governance documents, zero findings |
| Fresh workspace | Empty project bootstrap and verification pass using the installed runtime, with no global KB registration or model call |
| Source formatting | `git diff --check` passes |

The 113 targeted tests cover the changed boundaries and packaging. They do not exercise live LLM compilation, provider OAuth, business-system behavior or native Windows execution.

The graph excludes sources, saved explorations and navigation files according to the original OpenKB graph implementation. Its nodes represent the 12 summaries, 34 concepts and 39 entities. It remains distinct from the governed Workbench service dependency graph.

Reproduce the local workflow from the workspace root:

```sh
python3 .agents/skills/llm-wiki/scripts/wiki.py verify
python3 .agents/skills/llm-wiki/scripts/wiki.py run status
python3 .agents/skills/llm-wiki/scripts/wiki.py graph
```

See [setup and authentication](../SETUP.md#openkb-primary-wiki), [dependency inventory](../DEPENDENCIES.md#openkb-primary-wiki), and the [bridge procedures](../../.agents/skills/llm-wiki/references/workflows.md). Unrelated release-report work was preserved.
