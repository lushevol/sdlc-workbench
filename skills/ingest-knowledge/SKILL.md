---
name: ingest-knowledge
description: Preserve registered source material and provenance before creating candidate engineering knowledge.
---

# Ingest engineering knowledge

Use this procedure with any coding agent.
Use existing source access and preserve the user's authorization.
This procedure does not install or implement a remote source adapter.
Read [the knowledge contract](../../knowledge/README.md) before creating records.
Use its [schemas](../../knowledge/schemas/) and [templates](../../knowledge/templates/) for record structure.

1. **Discover:** Inspect workspace status and `registry/sources.yaml`.
   Select the source identity, owner, locator, access method, and authority.
   Mark unknown metadata explicitly.
   Discover permitted resource operations before invoking tools.
2. **Read:** Access the exact source revision through a supported tool or local path.
   Record retrieval time and access limits.
   Do not treat a search snippet or generated summary as the complete source.
3. **Preserve:** Retain unchanged bytes under `knowledge/raw/` when local retention is permitted.
   Add provenance to the raw manifest using its shipped contract.
   Use a new snapshot record for a changed source.
   Preserve earlier snapshots and records.
4. **Understand:** Create candidate knowledge with the shipped templates.
   Link claims to exact source records and locators.
   Separate facts, inferences, and unresolved questions.
   Record conflicts, missing context, or stale sources as findings.
5. **Record:** Add a new audit event YAML file for the candidate creation transition.
   Preserve existing events and Git history.
   Never invent source approval or reviewer identities.
6. **Validate:** Run `ai-sdlc --workspace PATH validate`.
   Correct contract or provenance errors within the authorized scope.
   Report unresolved source access and evidence limits.

Use [govern-knowledge](../govern-knowledge/SKILL.md) for investigation and publication.
Ingestion creates source evidence and candidates.
It does not establish approved business intent or verified execution.
