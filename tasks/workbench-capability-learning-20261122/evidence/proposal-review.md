---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not establish complete writing review.
---

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

The current skill links to the shared guide for classification, evidence, reconciliation, and promotion.
A short authoring reference would clarify when to update registry data and when to revise instructions.
The CES capability already has a feedback path through the migration scan skill.
Hooks capture lifecycle metadata. The agent extracts discoveries at checkpoints.

### Instruction-only changes

The Workbench maintenance owner should track reviewed changes to skill instructions in the lifecycle.
In a temporary workspace, an initial manual promotion recorded the fixture skill hash.
The probe changed the skill instructions and submitted new evidence for the existing rule.
The checkpoint returned `NO_CHANGE`, and the capability history still contained one revision.
Consequently, that submission did not provide an updated review record for the skill instructions.
The rule comparison drives the decision before the new skill digest can affect it.
Track skill content changes separately from rule equality. Test review and promotion with unchanged rule data.
[Rule comparison](../../../core/capability_learning.py#L301) · [Skill validation](../../../core/capability_learning.py#L330)

## Acceptance probe

An inline isolated probe used separate CLI processes and a local fixture bridge.

Session A retained one release-branch ADO observation. It remained an EXTEND candidate because one build did not satisfy independent verification.
Session B retrieved that candidate, added a second build with a distinct commit, and promoted revision 2 of ado-deploy-artifact.
Session C imported the versioned capability history into a newly initialized workspace.
It resolved the release artifact without an explicit artifact name. The main-branch rule still resolved its prior artifact.
The scoped capability data changed the outcome with the same skill file hash.

The probe used fixture transport and independent CLI processes.
Live ADO execution and language-model sessions were outside its scope.

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
