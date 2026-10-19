---
artifact_kind: requirement
id: REQ-portal-task-material-ownership
version: 1
status: draft
owner: unknown
source_refs:
  - SRC-portal-task-organization-20261020
related_ids:
  - DEFECT-portal-background-session-20261019
review:
  state: pending
  reviewer: null
  reviewed_at: null
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
    - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Keep issue material with its task and return clarified intent to knowledge

## Description

As the project owner, I need issue material under its task so that knowledge remains useful and clear.
Move this incident's investigation evidence, logs, report history, and source excerpts into the portal task.
Keep domain sources, governed knowledge, and immutable governance history in their knowledge locations.
Use existing document templates. Extend those templates when a required record is absent.

When investigation finds missing, ambiguous, or stale knowledge, resolve the material question before changing its meaning.
After clarification, update the affected knowledge record and its provenance before handoff.
Do not leave completed clarification only in chat or task notes.

## Rationale

The earlier consolidation copied selected evidence but left original investigation directories outside this task.
The user requested full task ownership and a standing clarification feedback rule.
The source request is retained under this task.

## Scope

| Included behavior | Excluded behavior | Reason |
| --- | --- | --- |
| Move incident evidence and archive historical locators | Move independent business repositories | Repositories retain their own ownership |
| Update active snapshot references without changing source identities or bytes | Rewrite existing audit events or historical execution outputs | History must remain reviewable |
| Update shared intake, knowledge guidance, and templates | Implement a workflow runtime or change portal session behavior | This request concerns storage and process |
| Record clarified knowledge updates before handoff | Publish important business intent without required review | Clarification and publication have separate gates |

### Intake readiness and authority

| Named next phase | Readiness | Rationale and evidence limits | Blocked actions | Owner and next action |
| --- | --- | --- | --- | --- |
| Relocate task material and update guidance | READY | The user directly specifies storage ownership and the feedback rule. Existing snapshot paths permit task storage. | Portal correction and business publication | Codex; migrate bytes and validate references |

- Expected behavior authority: The user's direct instruction in SRC-portal-task-organization-20261020.
- Existing authorization: Move related materials and update necessary templates and rules.
- Evidence index: [Organization evidence](evidence/organization-20261020/relocation-map.json).
- Business review: pending. This request does not approve new session policy.
- Assessment: Codex; 20 October 2026 in Asia/Singapore.
- Qualitative risk: Medium because snapshot references, historical locators, and distributed guides must remain consistent.

## Actors and business rules

| Actor | Rule ID | Condition | Required behavior | Source |
| --- | --- | --- | --- | --- |
| Investigation agent | OWN-1 | Issue investigation produces evidence | Store it under the owning task and index its provenance | User request |
| Knowledge agent | FEEDBACK-1 | Required clarification is complete | Update affected knowledge with the answer source, scope, and version | User request |
| Knowledge agent | REVIEW-1 | Important intent needs publication | Retain required human review and append-only audit gates | Knowledge contract |

## Dependencies

| Related ID | Relationship | Evidence | Unresolved impact |
| --- | --- | --- | --- |
| DEFECT-portal-background-session-20261019 | Owns this material | Existing intake and evidence manifest | The business defect remains unresolved |
| RAW-portal-session-local-2026-10-19 | Supplies registered evidence | Raw source manifest and original audit event | Only snapshot locations change |

## Acceptance criteria

```gherkin
Feature: Own issue evidence and retain clarified knowledge

  Scenario: Move all inventoried incident materials
    Given an inventory of incident materials outside the task
    When the authorized relocation completes
    Then every inventoried material has exactly 1 canonical task destination
    And exactly 0 inventoried original files remain outside the task
    And every destination matches its recorded SHA-256

  Scenario: Preserve provenance and governance history
    Given 58 registered incident snapshots and existing audit events
    When their snapshot locations change
    Then all 58 source identity triples remain unchanged
    And exactly 0 existing audit event bytes change
    And exactly 1 new relocation audit event records the migration

  Scenario: Return completed clarification to knowledge
    Given a material knowledge gap with a completed source-backed clarification
    When the intake prepares its next handoff
    Then exactly 1 knowledge-update log identifies its answer source and affected record
    And exactly 0 resolved material clarifications remain recorded only in chat or task notes
    And every required publication review remains separate from clarification
```

```yaml
acceptance_criteria:
  - id: AC-OWN-1
    given: Given an inventoried incident material
    when: When relocation completes
    then: Then exactly one canonical task destination preserves its SHA-256
    measure: {metric: canonical destination count, operator: equals, value: 1, unit: count}
  - id: AC-OWN-2
    given: Given 58 registered incident snapshots
    when: When snapshot locations change
    then: Then zero source identity triples change
    measure: {metric: changed source identity count, operator: equals, value: 0, unit: count}
  - id: AC-FEEDBACK-1
    given: Given a completed material knowledge clarification
    when: When intake prepares its next handoff
    then: Then zero resolved clarifications remain only in chat or task notes
    measure: {metric: missing knowledge update count, operator: equals, value: 0, unit: count}
```

## Measurement conditions

| Criterion ID | Measurement method | Environment and data | Interval and load | Evidence required |
| --- | --- | --- | --- | --- |
| AC-OWN-1 | Compare old and new hashes and check original absence | Local tracked materials and relocation map | One migration | Migration validation |
| AC-OWN-2 | Compare source triples and existing audit hashes | Before and after manifests | One migration | Manifest and audit integrity results |
| AC-FEEDBACK-1 | Inspect procedures, templates, and knowledge-update log | Shared guides and this task | Before handoff | Authoring checks and agent review |

## Traceability

| Criterion ID | Design ID | Repository and exact revision | Test assertion and revision | Retained execution |
| --- | --- | --- | --- | --- |
| AC-OWN-1 | Existing confined snapshot paths | Workbench `64cc4d58e766fb227f3b495117c0a4c43d1e92f7` | Migration hash and location checks | [Integrity checks](evidence/organization-20261020/integrity-check.json) |
| AC-OWN-2 | Stable resource, revision, and hash identities | Same Workbench revision | Manifest and audit comparison | [Integrity checks](evidence/organization-20261020/integrity-check.json) |
| AC-FEEDBACK-1 | Intake knowledge-update log | Shared skills and templates | Procedure and sample inspection | [Authoring checks](evidence/organization-20261020/authoring-check.json) |

## Sources

| Source ID | Locator | Exact revision | Available hash | Owner and authority | Limits |
| --- | --- | --- | --- | --- | --- |
| SRC-portal-task-organization-20261020 | [User request](evidence/organization-20261020/request.txt) | task-relocation-20261020 | See relocation map | User; storage and process instruction | No approval of new business behavior |

## Evidence and open questions

| Kind | Statement | Evidence or required source | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- | --- |
| Fact | Task-local snapshot paths satisfy the existing contract | Knowledge guide and validator inspection | No runtime path extension is needed | Codex | Update active locations |
| Fact | Historical ingestion baselines preserve earlier locations | Ingestion harness inspection | They cannot validate this explicit relocation | Codex | Preserve old baselines and create a new baseline |
| Unknown | Missing-credential session recovery remains unresolved | Portal intake O-001 | No business policy update is justified | unknown | Continue the original investigation |

### Answer and question log

| Round and ID | Question or supplied detail | Answer | Answer source | Status | Resolution owner | Consequence and next action |
| --- | --- | --- | --- | --- | --- | --- |
| 1 / OWN-1 | Where should issue materials live? | Under this task | Current user request | answered | User | Relocate registered evidence with provenance |
| 1 / FEEDBACK-1 | What follows a completed knowledge clarification? | Update knowledge and keep it current | Current user request | answered | User | Update shared rules and templates |

### Knowledge-update log

| Gap or question ID | Affected record and prior version | Clarified rule, source, and applicability | Updated record, version, and criteria | Finding and audit references | Publication state, owner, and next action |
| --- | --- | --- | --- | --- | --- |
| OWN-1 | Knowledge storage guidance and pre-relocation source manifest | User request assigns incident evidence to its task; domain sources retain knowledge locations | UPDATED; guides and manifest; AC-OWN-1 and AC-OWN-2 | AUD-20261020-RAW-portal-task-relocation-v2; organization report | No business publication; Codex; maintain canonical paths |
| FEEDBACK-1 | Shared knowledge governance and intake procedures | User request requires clarified knowledge updates before handoff | UPDATED; shared skills and both intake templates; AC-FEEDBACK-1 | Organization report; no domain governance change | No business publication; Codex; apply updated procedures |
| Portal O-001 | Session requirement boundary; REQ-active-session-renewal v2 | Unresolved recovery after suspension without refresh; no policy source resolves it | OPEN; pending; no invented criterion | Portal intake O-001; no governance change | Candidate; unknown; complete clarification before a knowledge change |
