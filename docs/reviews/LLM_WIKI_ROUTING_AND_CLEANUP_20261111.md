# Wiki selection and duplicate cleanup — 11 November 2026

One active compiled wiki remains at [knowledge/llm-wiki/wiki/index.md](../../knowledge/llm-wiki/wiki/index.md). It retains the richer OpenKB-generated pages: 12 summaries, 34 concepts, 39 entities and six saved explorations. Changing the maintenance engine does not create a second wiki or rewrite the documents' original compilation provenance.

## Authorizing input

Source: user message in the Workbench knowledge chat, 11 November 2026. Exact wording:

> OK, now safe remove duplicate llm wikis documents only keep authed one. The rule is openKB as primary llm-wiki if provide llm url and token other wise use llm-wiki-agent instead.

This supersedes unconditional OpenKB selection in the earlier [migration report](OPENKB_PRIMARY_MIGRATION_20261111.md). The earlier instruction to keep comparison materials still applies: duplicate browsable snapshots are consolidated, with their historical bytes preserved.

Commit and push authorization: user message in the same chat, 11 November 2026. Exact wording:

> commit and push

## Engine rule

| Explicit configuration | Selected semantic engine |
| --- | --- |
| Both `OPENAI_API_BASE` and `LLM_API_KEY` are nonempty | OpenKB, using the configured API URL/token and a compatible API model |
| Either or both values are missing | llm-wiki-agent in the current ADE session, using the existing agent's model access |

The launcher accepts those two single-line literal settings from ignored `knowledge/llm-wiki/.env` or the process environment, with nonempty KB-local values taking precedence. It does not select an engine from global authentication, root project secrets, a provider-specific key, or an OAuth cache. The engine command outputs only presence flags. Configured values are not proof of successful authentication.

Current presence-only check selected **llm-wiki-agent**: neither explicit URL nor token is configured. No provider call or OAuth login was made. Model commands in this mode produce a truthful agent handoff; the ADE agent must then perform the requested semantic work. A handoff alone is not a compiled result.

The fallback reads the unchanged original [llm-wiki-agent instructions](../../.agents/skills/llm-wiki/upstream/AGENTS.md), applying the shared-layout constraints in the [bridge](../../.agents/skills/llm-wiki/SKILL.md): source summaries live under `summaries/`, canonical source aliases remain immutable under `sources/` and `raw/`, saved synthesis lives under `explorations/`, and existing metadata and wiki-relative links are preserved. Do not invoke original scripted ingest/refresh operations on those source links. The native upstream code and official OpenKB skill remain unchanged.

OpenKB's local native validator and graph visualizer continue to check the **stored OpenKB page format** in either semantic mode. They make no model calls. The [graph](../../knowledge/llm-wiki/output/visualize/graph.html) represents wiki links, separately from Workbench's service dependency graph.

Native semantic dispatch rejects OAuth model prefixes and LiteLLM credential overrides, binds the selected API URL/token, and blocks source-owning commands and the interactive chat `/add` bypass. The installer replaces only the exact old generated OAuth example configuration with an API-model example; customized configuration is preserved.

## Duplicate cleanup and recovery

Removed the expanded `docs/reviews/benchmark-evidence/openkb/` and `docs/reviews/benchmark-evidence/llm-wiki/` trees after preserving all **135 files** in one deterministic [archive](benchmark-evidence/wiki-comparison-snapshots-20261111.tar.gz), with an exact per-file [hash manifest](benchmark-evidence/wiki-comparison-snapshots-20261111.manifest.json). The [archive guide](benchmark-evidence/README.md) contains recovery commands and the authorizing input.

The original trees contained 1,569,283 logical bytes; the archive is 399,698 bytes. Every archive member was verified against its original SHA-256 before deletion, then read back after deletion. The old llm-wiki 26-file preservation inventory also verifies inside the archive. Historical links in the comparison reports now use explicit archive-member locators. The active [source manifest](../../knowledge/llm-wiki/source-manifest.json) retains its original import identity and adds the archive path, hash and member prefix.

Preserved the predefined questions, comparison reports, unique historical results, all original upstream files, and all canonical records. All 24 active source entries remain relative symlinks. The former `knowledge/wiki/`, `knowledge/llm-wiki-direct-compare/` and root `llm-wiki-agent/` copies were already absent. Upstream sample/template wiki files are part of the unchanged installed source, not another project wiki.

## Verification

Validation covers credential routing and handoff, source links and hash bindings, structural schema checks, canonical-scanner boundaries, native graph dispatch and shared-skill packaging.

- All 55 targeted tests pass: 28 routing/source-boundary tests, four canonical-scanner boundary tests and 23 shared-skill packaging tests.
- All 135 archived files verify after removal of the expanded copies; both upstream source locks are unchanged.
- All 12 canonical source hashes and 24 relative symlinks verify; all six native structural categories report zero findings.
- Workbench validates as VALID with 14 canonical/governance documents and zero findings.
- The native graph generates with 85 nodes and 1,468 directed links. All 309 checked current local Markdown links resolve, and `git diff --check` passes.

Reproduce the local checks:

```sh
python3 .agents/skills/llm-wiki/scripts/wiki.py engine
python3 .agents/skills/llm-wiki/scripts/wiki.py verify
python3 .agents/skills/llm-wiki/scripts/wiki.py graph
.venv/bin/ai-sdlc --workspace . validate
```

The preserved knowledge remains candidate/draft. This change does not claim a new semantic recompilation, live credential acceptance or business-system verification.
