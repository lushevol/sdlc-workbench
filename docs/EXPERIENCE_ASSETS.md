# Reusable domain experience

The `package-domain-experience` and `learn-domain-experience` skills turn supported task results into concise project assets.
They provide a reusable execution card with provenance, scripts, fixtures, variable templates, recovery steps, and links to canonical knowledge.

## Storage

Promoted packets live under the project-owned `assets/experience/` area.
Scratch scans and candidate material stay in ignored `.workbench/experience/` storage until selected.
Full execution logs, screenshots, traces, and source evidence remain under their owning task.

```text
assets/experience/
├── index.yaml
└── packets/<experience-id>/
    ├── manifest.yaml
    ├── experience.md
    ├── variables.example.yaml
    ├── references.yaml
    ├── scripts/
    └── fixtures/
```

The index contains retrieval metadata. The packet contains the shortest usable procedure and its reusable inputs.
Each manifest records the source task, session when available, exact evidence hashes, tested conditions, status, sensitivity classification, and known limits.

## Capture and learning

Use `package-domain-experience` after a supported successful result.
Use `learn-domain-experience` to scan retained task records or explicitly supplied session exports, identify repeated patterns, and prepare candidate packets.
The scan does not establish success, business approval, production reachability, or knowledge publication.

Use `observed` for one supported result, `replayed` after a qualifying repeat, `reviewed` after applicable human review, and `retired` when the packet no longer applies.
Preserve earlier packets when later replay disagrees.

## Knowledge and configuration

Packets link to canonical `knowledge/records/` and derived wiki topics by identity, version, and hash.
They do not duplicate the knowledge base.
New business intent follows the existing knowledge lifecycle.

Track variable names, types, sources, allowed values, and placeholders.
Keep secrets, personal data, private tokens, and environment-specific values in ignored configuration or approved process environment.
Label fixtures as synthetic or redacted and state their evidence limits.

Both skills use the canonical `.agents/skills/` path. Codex, Claude Code, Copilot CLI, and VS Code Copilot share the same procedures and packet format.
