# Knowledge index

Read [the standards](README.md) before you add a document.
Consult the registry catalogs for available business sources.
Require recorded review before treating knowledge as approved intent.
Ingested projects use `candidates/index.md` as their classified topic map.

Read each topic's review state and evidence limits before relying on its claims.
Use the [Workbench llm-wiki bridge](../.agents/skills/llm-wiki/SKILL.md) for compiled project knowledge.
Select [OpenKB](../.agents/skills/openkb/SKILL.md) when both an LLM URL and token are configured; otherwise use llm-wiki-agent in the current ADE context.
When initialized, start at `llm-wiki/wiki/index.md` for source summaries, focused concepts, entities, and saved explorations.
Both routes use this single wiki and retain its existing rich pages; engine selection does not create duplicate documents.
Source entries under both `llm-wiki/raw/` and `llm-wiki/wiki/sources/` remain relative links to selected canonical records, preserving their review states and evidence limits.
Use the bridge's `compile` command to select explicit provider compilation or the llm-wiki-agent procedure while retaining source links and hashes.
The compiled wiki and its graph provide derived navigation; applicable records and publication review establish authority.

- [Raw source manifest](../evidence/knowledge/manifest.yaml)
- [Candidate guidance](candidates/README.md)
- [Requirements](requirements/README.md)
- [Architecture](architecture/README.md)
- [Decisions](decisions/README.md)
- [Repository profiles](repository-profiles/README.md)
- [Governance findings](../evidence/knowledge/findings/README.md)
- [Audit events](../evidence/knowledge/audit/README.md)
- [Illustrative templates](../core/knowledge/templates/README.md)
