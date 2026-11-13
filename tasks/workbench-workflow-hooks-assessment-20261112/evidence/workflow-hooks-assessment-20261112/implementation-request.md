# Hook implementation authorization

- Source: user message in the current Codex chat
- Date: 13 November 2026 (Asia/Singapore)
- Governing requirement: [support Codex, Copilot, and Claude Code](cross-client-requirement.md#exact-user-input).

## Exact user input

> implement

## Authorized scope

Implement the shared session-context and scoped completion-check behavior from [the assessment](../../reviews/WORKFLOW_HOOKS_ASSESSMENT_20261112.md).
Provide native adapters for all three clients, safe configuration installation, packaging, documentation, and relevant verification.
Keep semantic workflows and business approval outside hooks. Preserve unrelated worktree changes and existing client settings.
