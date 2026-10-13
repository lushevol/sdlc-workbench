# Claude Code adapter

Claude Code consumes the same [canonical skills](../../skills/) as other agents.
Keep workflow logic in those skills.
Avoid copies that can develop different behavior.

Install this standalone project before using its `ai-sdlc` command.
Select the workspace that contains `workspace.yaml`.

```text
ai-sdlc --workspace PATH status
ai-sdlc --workspace PATH skills
ai-sdlc --workspace PATH skills analyze-requirement
ai-sdlc --workspace PATH call RESOURCE OPERATION --args JSON
ai-sdlc --workspace PATH runs
```

Replace placeholders with discovered resource IDs, operation names, and schema arguments.
The CLI exposes the Workbench core; Claude Code supplies reasoning and task execution.
Existing assets stay at their registered locations.

For stdio MCP access, use the [shared MCP adapter](../mcp/README.md).
The four tools expose status, operations, action records, and canonical skills.

Native skill discovery depends on the Claude Code version and project configuration.
Expose canonical files through the supported client mechanism, or read them through CLI or MCP.
This directory supplies integration guidance.
It does not install or configure a Claude Code connection.
Preserve the user's task scope and existing authorization when invoking operations.
