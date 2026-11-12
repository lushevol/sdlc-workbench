# Codex adapter

Codex consumes the canonical skills under [`.agents/skills/`](../../.agents/skills/).
Keep workflow logic in those skills and executable behavior in the installed Workbench runtime.

Install Workbench and select the workspace containing `workspace.yaml`.
Use the shared [MCP adapter](../mcp/README.md) when the client needs registered tools and retained action records.

```text
ai-sdlc --workspace PATH skills
ai-sdlc --workspace PATH skills analyze-requirement
ai-sdlc --workspace PATH hooks install --client codex
ai-sdlc --workspace PATH hooks status
```

The optional [hook adapter](../../docs/HOOKS.md) maps `SessionStart` and `Stop` to shared Workbench behavior.
Its project registration is `.codex/hooks.json`.
Installation preserves unrelated entries and uses the selected installed Python executable.
Review and trust non-managed hook definitions through Codex hook settings before expecting execution.

Session context and completion checks use an explicit per-session scope.
Configuration validity does not establish successful client execution or verified business behavior.
This adapter does not configure credentials, grant operations, or change publication approval.
