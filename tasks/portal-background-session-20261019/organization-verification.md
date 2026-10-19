---
artifact_kind: test-execution-report
id: REPORT-portal-task-organization-20261020
version: 1
status: draft
owner: unknown
source_refs:
  - SRC-portal-task-organization-20261020
  - SRC-portal-task-relocation-20261020
related_ids:
  - REQ-portal-task-material-ownership
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

# Task material relocation and clarification feedback

## Run identity and provenance

This stage moves incident materials into the portal task and updates knowledge-feedback guidance.
It changes no portal runtime behavior and runs no new portal reproduction.

```yaml
execution_id: portal-task-relocation-20261020
execution_status: PASSED
repository_id: ai-sdlc-workbench
repository_revision: 64cc4d58e766fb227f3b495117c0a4c43d1e92f7
test_revision: sha256:5fafeef0572a2bf7c795884f0b9f30800a04a207bca7759160df4f71c67ccc3b
environment_identity: local-macos-arm64-workbench
started_at: "2026-10-19T16:03:24.019580+00:00"
completed_at: "2026-10-19T16:12:14.257955+00:00"
command_or_tool_reference: evidence/organization-20261020/check-relocation.py
process_exit_status: 0
actual_results: 178 relocation entries pass integrity checks; 69 focused tests pass
retained_execution_refs:
  - SRC-portal-task-relocation-20261020
```

The map records 178 old locations and their canonical task destinations.
These locations include 177 files outside the task and one duplicate task copy.
Fifty-seven destinations already held identical bytes. Those duplicates were removed after comparison.
The other 121 files moved into their canonical task destinations.

## Assertions and outcomes

| Test ID | Requirement / criterion | Inspected assertion location | Expected result | Actual result | Outcome | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| MOVE-1 | AC-OWN-1 | Relocation map and migration check | Every destination matches its original SHA-256; zero old locations remain | 178 entries match hashes; zero old files remain | PASSED | [Integrity check](evidence/organization-20261020/integrity-check.json) |
| SOURCE-1 | AC-OWN-2 | Before and current provenance manifests | All 58 source identity triples remain unchanged | 58 snapshot-only changes; two new records resolve | PASSED | [Integrity check](evidence/organization-20261020/integrity-check.json) |
| AUDIT-1 | AC-OWN-2 | Existing audit files at base revision | Zero existing audit files change; one relocation event is appended | 28 existing audit files remain unchanged; one new event resolves | PASSED | [Integrity check](evidence/organization-20261020/integrity-check.json) |
| FEEDBACK-1 | AC-FEEDBACK-1 | Shared skills, templates, root guides, and intake log | Completed clarification must update knowledge before handoff | Procedures, templates, and task logs include the rule | PASSED | [Authoring checks](evidence/organization-20261020/authoring-check.json) |
| CONTENT-1 | Authoring contract | Completed task artifacts | Required sections, sources, scenarios, and limits remain valid | Four artifacts pass with 16 expected warnings | PASSED | [Artifact lint](evidence/organization-20261020/artifact-lint-final.json) |

The repository revision identifies the base. The retained diff contains this stage's guide and template changes.

Artifact lint reports 16 expected warnings across four task artifacts.
The warnings concern unknown owners, pending business review, unresolved content, and pending writing review.
Workspace validation reports 13 governed documents and zero findings.
The 51 artifact tests and 18 workspace-layout tests pass.
The wheel installs and initializes a separate workspace with all 14 changed shipped files preserved.
These checks use prepared local dependencies. Other platforms and connected installation remain untested.

## Retained evidence inventory

| Evidence ID | Locator | Hash | Run identity | Integrity or availability limit |
| --- | --- | --- | --- | --- |
| ORG-REQUEST | [User instruction](evidence/organization-20261020/request.txt) | Registered in raw source manifest | user-request-20261020 | Storage and process instruction only |
| ORG-MAP | [Relocation map](evidence/organization-20261020/relocation-map.json) | Registered in raw source manifest | portal-task-relocation-20261020 | Resolves historical paths without changing original file bytes |
| ORG-BEFORE | [Prior source manifest](evidence/organization-20261020/manifest-before.yaml) | Recorded in relocation map | pre-relocation-20261020 | Historical provenance; current snapshot paths differ |
| ORG-PRIOR | [Prior consolidation manifest](evidence/organization-20261020/prior-consolidation/evidence/manifest.json) | Retained original bytes | consolidation-20261019 | Earlier checks describe the earlier layout |
| ORG-BASELINE | [New ingestion baseline](evidence/organization-20261020/ingestion-baseline.json) | File inventory in record | post-migration-20261020 | Starts future retention checks from this authorized layout |
| ORG-CHECKS | [Validation record](evidence/organization-20261020/validation.json) | File inventory in record | portal-task-relocation-20261020 | Documentation, packaging, and provenance checks only |

Historical report snapshots remain under `evidence/reports/`.
Their relative links and embedded paths identify their original locations.
The relocation map and recorded Git revision resolve those historical references.
Current navigation uses canonical task paths.

## Verification conclusion

- Behavior claim: Related investigation materials have canonical task locations with unchanged retained bytes.
- Covered conditions: Registered incident snapshots, browser setup, tooling checks, harness logs, reports, and incident source excerpts.
- Uncovered conditions: Original PROD incident causation, corrected session recovery, and post-login workspace restoration.
- Evidence limits: Validation results concern organization and guidance. They establish no new business policy or runtime recovery.

Knowledge retains domain sources, governed candidates, findings, schemas, templates, provenance metadata, and audit history.
It no longer holds this task's raw execution tree or incident-specific source excerpts.
Independent business repositories and installed tool runtimes keep their own locations.

The knowledge-update rule now requires a completed clarification to update affected knowledge before handoff.
The update must retain its source, scope, version, evidence, and review state.
Important requirements and decisions still require human review before publication.
The unresolved missing-credential recovery question remains open. No new answer is invented.

Earlier ingestion baselines remain historical records of the earlier layout.
This explicit relocation has its own authorization, old manifest, map, audit event, and new baseline.
Normal retention checks still reject unrecorded removal or manifest rewrites.

## Facts, inferences, and unresolved questions

- Fact: The user requested relocation and the clarification feedback rule.
- Fact: Snapshot paths can point inside the task under the existing workspace contract.
- Fact: Existing source identity triples do not need to change for a location update.
- Inference: Keeping investigation artifacts with their task reduces incidental material in knowledge retrieval.
- Unknown: The original portal correction still needs the evidence and decisions listed in its intake.

## Findings

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| Duplicate evidence existed outside the task | Investigation materials had several storage locations | Codex | Use canonical task paths and the relocation map |
| Previous checks assumed old paths remained present | Earlier checker cannot validate the new layout | Codex | Retain it as historical evidence and use migration checks |
| Clarification answers could remain only in task notes | Knowledge could remain stale after investigation | Codex | Update knowledge before handoff and record the result |
| Missing-credential recovery is unresolved | The business correction remains blocked | unknown | Complete that clarification and update the affected requirement |

## Sources

| Source ID | Locator | Exact revision | Hash | Owner, authority, and limits |
| --- | --- | --- | --- | --- |
| SRC-portal-task-organization-20261020 | [Request](evidence/organization-20261020/request.txt) | task-relocation-20261020 | See raw source manifest | User; organization instruction; no new session policy |
| SRC-portal-task-relocation-20261020 | [Map](evidence/organization-20261020/relocation-map.json) | task-relocation-20261020 | See raw source manifest | Codex; observed file relocation; no business verification |
