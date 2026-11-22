# Skill lifecycle suggestion review

Date: 22 November 2026
Compared revision: b04f3cf74
Scope: Review the supplied proposal against the implemented Workbench capability-learning foundation.

## Decision

Adopt the Skill Lifecycle Manager framing as a conceptual model.
Keep one skill and one Python engine.
Do not add a Node.js engine under packages/capability-engine/.

The six areas map to current behavior.

| Proposal area | Current Workbench evidence | Assessment |
| --- | --- | --- |
| Discovery | Lifecycle hooks and checkpoint discovery schemas | Implemented with bounded event capture |
| Extraction | Agent checkpoint creates structured discovery JSON | Implemented as agent-side semantic extraction |
| Reconciliation | Scoped registry lookup and conflict detection | Implemented |
| Skill authoring | Linked skill validation and hash binding | Partial. Skill files are not auto-authored |
| Validation | Evidence hashes, schema, scope, security and fixture checks | Implemented |
| Maintenance | Immutable revision chain and rollback | Implemented |

## Material gaps

The current skill has no progressive references taxonomy files, templates, or examples.
The current engine does not generate or edit SKILL.md.
The CES capability intentionally reuses ces-migration-scan guidance rather than adding a duplicate skill.
Hooks capture lifecycle metadata, but semantic extraction still occurs at an agent checkpoint.

These limits preserve the single Python runtime, existing skill ownership, security review, and knowledge boundaries.
The proposal's compatibility Node.js text would be inaccurate for this Workbench.

## Acceptance probe

An inline isolated probe used separate CLI processes and a local fixture bridge.

Session A retained one release-branch ADO observation. It remained an EXTEND candidate because one build did not satisfy independent verification.
Session B retrieved that candidate, added a second build with a distinct commit, and promoted revision 2 of ado-deploy-artifact.
Session C used a newly initialized workspace containing only the versioned capability history. It resolved the release artifact without an explicit artifact name. The existing main-branch rule still resolved its prior artifact.
The canonical skill file hash was unchanged. The improved behavior came from scoped capability data.

The probe used fixture transport. It made no live ADO request and did not create a new skill source file.
This proves cross-process and cross-workspace capability reuse. It does not prove three live agent sessions.

Commands used:

    .venv/bin/python - <<'PY' ... PY
    .venv/bin/ai-sdlc --workspace TMP learning ado-resolve ...
    .venv/bin/ai-sdlc --workspace TMP learning checkpoint --ado-observation ...
    .venv/bin/ai-sdlc --workspace TMP learning pending
    .venv/bin/ai-sdlc --workspace TMP learning history ado-deploy-artifact

The exact inline probe was not retained as a repository script.
The repeatable focused suite is:

    .venv/bin/python -m unittest discover -s tests -p 'test_capability*.py' -v

Result: 20 tests passed.
