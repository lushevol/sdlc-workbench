# Governance responsibility

Governance controls knowledge quality and its publication state.
Keep candidate, investigated, verified, and published knowledge distinguishable.
Use contested, stale, and superseded states when evidence requires them.
Keep Workbench lifecycle state separate from OKF `status`.

Use the [governance procedure](../../.agents/skills/govern-knowledge/SKILL.md).
Check source identity, revision, snapshot hashes, evidence links, review records, and acceptance criteria.
Important requirements and decisions require recorded human review before publication.
Never manufacture a human actor, approval, or verification event.

Record each change in a new YAML file under `evidence/knowledge/audit/`.
Preserve earlier events and their Git history.
A correction requires a new event that references the earlier event.
Hashes support integrity checks; they do not establish the truth of a source claim.

```sh
ai-sdlc --workspace PATH validate
```

This command performs deterministic contract and provenance checks.
It does not reason about business correctness or authenticate a reviewer.
AI governance, approval workflows, and source adapters remain future capabilities.
This directory implements the deterministic validator within the single `core/` runtime.
