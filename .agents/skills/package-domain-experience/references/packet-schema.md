# Experience packet contract

Create this layout only when a packet is promoted.

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

`experience.md` is the short execution card. Keep it below the size needed for the problem, inputs, ordered steps, expected outputs, recovery, verification scope, and limits.

The manifest uses these fields.

```yaml
schema_version: 1
id: exp.<domain>.<slug>.v1
title: A short task-oriented title
domain: domain-name
status: observed
applies_when:
  - A concrete trigger or condition
requires:
  tools: []
  variables: []
provenance:
  task_id: task-name
  session_id: optional-session-id
  source_revisions: []
  evidence:
    - path: tasks/task-name/evidence/result.json
      sha256: 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
verification:
  outcome: successful
  conditions: []
  assertions: []
assets:
  procedure: experience.md
  variables: variables.example.yaml
  scripts: []
  fixtures: []
knowledge:
  records: []
  wiki_topics: []
security:
  classification: synthetic
  secrets_present: false
limits: []
```

Paths in `assets` are packet-relative. Evidence paths are workspace-relative and retain their original hashes. Every referenced file must exist. The index contains only retrieval metadata, packet paths, applicability terms, and status.

Use `classification` values such as `public`, `redacted`, `synthetic`, or `private-reference`. Private references may point to an ignored local configuration path through a variable name, but they contain no private value.

Knowledge references identify canonical records or wiki topics with their current path, version, and hash. A packet can support reuse without becoming a second knowledge authority.
