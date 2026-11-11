# Upstream installation and boundaries

Repository: [SamurAIGPT/llm-wiki-agent](https://github.com/SamurAIGPT/llm-wiki-agent).
Installed revision: [`f03eff653886672ee8a92bb6a28faae9190d90d2`](https://github.com/SamurAIGPT/llm-wiki-agent/tree/f03eff653886672ee8a92bb6a28faae9190d90d2).
The complete original tree is retained under [upstream/](../upstream/), including [its MIT license](../upstream/LICENSE).
The [source lock](../upstream-lock.json) records exact upstream file hashes.

The earlier instruction-only adaptation used revision `37145b8ba04d0acc6f3b6b0c02606768d1862c9a`.
The current installation includes the original implementation and native graph instead of replacing those capabilities.

## Original and integration files

| Layer | Responsibility |
| --- | --- |
| `upstream/` | Complete pinned source, preserved unchanged. |
| `scripts/wiki.py` | External installation, export, isolation, and invocation wrapper. |
| `.venv-llm-wiki/` | Dedicated Python environment for upstream dependencies. |
| Runtime implementation under `knowledge/llm-wiki/` | Ignored unchanged code copies beside the persistent native data. |
| `knowledge/llm-wiki/{raw,wiki,graph}/` | Native inputs, editable derived pages, operation logs, and original graph outputs. |
| Canonical Workbench records and evidence | Intended rules, exact provenance, lifecycle, review, publication, and immutable audit history. |

All upstream workflows remain available: ingest, query, health, semantic lint, refresh, heal, graph, and document conversion.
The original agent instructions and `.claude/commands/` are retained in the vendored tree.
Use the original [AGENTS.md](../upstream/AGENTS.md) or [CLAUDE.md](../upstream/CLAUDE.md) for native workflow details.
Apply their wiki operations within the isolated native data workspace.

The wrapper does not modify upstream source, replace its graph algorithm, or turn native pages into published Workbench records.
It exports Workbench candidate records into native source-page metadata, unique filename stems, and `[[wikilinks]]`.
Confirmed source records can be selected later with the launcher's `--source` option.
Source-bound provenance remains available beside those derived pages.
Keep canonical changes within Workbench ingestion and governance procedures.

## Execution requirements

The upstream project declares Python `>=3.10,<3.14`.
The complete dependency installation requires Python 3.11–3.13 because the declared NetworkX version requires Python 3.11 or later.
Its project dependencies include `markitdown[all]>=0.1.5,<0.2.0` and `tqdm>=4.67.3,<5.0.0`.
Its separate requirements declare `litellm~=1.83.10` and `networkx~=3.6.1`.
Use the launcher installation path to prepare the dedicated environment and inspect actual readiness output.

Agent-authored wiki work can use the current coding agent without a second model API.
Original scripted ingest, query, semantic lint, heal, refresh, and inferred graph operations use LiteLLM and configured model access.
Upstream model selection uses `LLM_MODEL` and, where applicable, `LLM_MODEL_FAST`.
Keep provider credentials in the process environment, outside pages, manifests, command arguments, and reports.

The original HTML renderer requests an unpinned vis-network script from `https://unpkg.com/vis-network/standalone/umd/vis-network.min.js`.
Its source describes the HTML as self-contained, but browser rendering depends on that external asset.
Preserving upstream unchanged retains this dependency.
The scheduler recipe remains available as documentation; installation does not request a recurring job.
