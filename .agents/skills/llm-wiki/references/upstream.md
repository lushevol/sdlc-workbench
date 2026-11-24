# Original llm-wiki-agent installation

Repository: [SamurAIGPT/llm-wiki-agent](https://github.com/SamurAIGPT/llm-wiki-agent).
Revision: `f03eff653886672ee8a92bb6a28faae9190d90d2`.
The complete [upstream tree](../upstream/) and its MIT license remain unchanged; [upstream-lock.json](../upstream-lock.json) binds every original file.

This is Workbench's semantic fallback when either `OPENAI_API_BASE` or `LLM_API_KEY` is missing. Read its [AGENTS.md](../upstream/AGENTS.md) for original agent workflows, then apply the shared-layout and canonical-link constraints in [the Workbench procedures](workflows.md). It runs in the current ADE context without another model URL or token.

Original scripts remain available unchanged. Their ingest/refresh operations assume writable owned source-summary files, and their health/graph tools expect bare-stem links and the original index layout. Do not run those directly on the current shared OpenKB-format wiki. Local verification and visualization use OpenKB's unchanged format tools; semantic fallback still uses llm-wiki-agent reasoning in the ADE.

No second wiki or root-level upstream copy is needed. The existing `.venv-llm-wiki/` is an optional runtime for original standalone scripts, not a requirement for current-agent reasoning. Original standalone model scripts use independent LiteLLM provider configuration. The original llm-wiki-agent HTML renderer also requires a vis-network script from unpkg; the shared OpenKB viewer embeds its own assets.
