# OpenKB native skill and runtime source

Upstream: [VectifyAI/OpenKB](https://github.com/VectifyAI/OpenKB).
Pinned revision: [`ff54396e575ee6feb0113b631a34caa082b441cc`](https://github.com/VectifyAI/OpenKB/tree/ff54396e575ee6feb0113b631a34caa082b441cc).
Runtime package: `openkb==0.5.0rc2.dev3+gff54396e5`.

`SKILL.md` and both files under `references/` are copied unchanged from upstream `skills/openkb/`. The original Apache-2.0 license is retained as `LICENSE`. `source-lock.json` binds their original bytes. The installed Python package remains unchanged in the separate `.venv-openkb` environment.

The [Workbench bridge](../llm-wiki/SKILL.md) supplies canonical source linking, project selection, and governance boundaries. It selects OpenKB semantic operations only with both an explicit `OPENAI_API_BASE` and `LLM_API_KEY`; otherwise the current ADE uses llm-wiki-agent on the same wiki. It does not replace the original OpenKB compiler or graph renderer.

The initial installation reused the cached benchmark wheel with SHA-256 `4c6378fdd4a72f4b3a169167821a2caf28e568f25e36b172aeadf3ec54f4d179`.

Upstream authentication capabilities are documented in the pinned [README](https://github.com/VectifyAI/OpenKB/blob/ff54396e575ee6feb0113b631a34caa082b441cc/README.md#-getting-started). Workbench does not automatically select OAuth: the user-defined rule requires the explicit URL/token pair for native semantic operations. Local verification and visualization still need no model access in either semantic mode. Live credential/provider execution was not tested during this migration.
