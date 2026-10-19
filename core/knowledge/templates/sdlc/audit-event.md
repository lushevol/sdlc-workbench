# Governance audit event

## Purpose

Prepare a new immutable event for an actual knowledge lifecycle change.

Read the [AI authoring contract](README.md) before use.
Read the [sample context](sample-context.md) before interpreting the example.

## AI instructions

- Read the audit contract and the current artifact before drafting an event.
- Record the actual actor, action, timestamp, item version, and final file hash.
- Remove quotes around the item_version placeholder after replacing it with a positive integer.
- Use a new event ID and filename for every actual event.
- Never overwrite an earlier audit file.
- Human approval requires an actual human reviewer and matching verification evidence.
- The sample below is incomplete and must never enter evidence/knowledge/audit/.

## Template

Copy this block. Replace placeholders and retain the required sections.

````markdown
---
artifact_kind: audit-event
id: "{{artifact_id}}"
version: 1
status: draft
owner: unknown
source_refs: []
related_ids: []
review:
  state: pending
  reviewer: null
  reviewed_at: null
writing_review:
  standard: ASD-STE100
  automated_check: NOT_RUN
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
    - Automated checks do not check the complete approved dictionary or grammar rules.
---

# {{audit_preparation_title}}

## Subject and event preparation

{{actual_change_reason_supporting_evidence_and_event_destination}}

## Event YAML

```yaml
id: "{{new_event_id}}"
item_id: "{{item_id}}"
item_version: "{{positive_integer_version}}"
actor: "{{actual_actor_identity}}"
at: "{{actual_timestamp_with_timezone}}"
action: "{{transition_or_approval}}"
from_state: "{{current_state}}"
to_state: "{{next_state}}"
content_sha256: "{{sha256_of_final_markdown_bytes}}"
reason: "{{actual_reason}}"
evidence:
  - resource: "{{registered_source_locator}}"
    revision: "{{registered_revision}}"
    sha256: "{{registered_source_sha256}}"
```

## Pre-write checks

{{actor_evidence_allowed_transition_final_hash_filename_and_chronology_checks}}

## Evidence and open questions

| Kind | Statement | Evidence or required source | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- | --- |
| {{fact_inference_or_unknown}} | {{statement}} | {{source_or_missing_evidence}} | {{effect}} | unknown | {{action}} |
````

## Illustrative sample

This sample is fictional. It records no actual approval or execution.

````markdown
---
artifact_kind: audit-event
id: "SAMPLE-AUDIT-GUIDE-001"
version: 1
status: draft
owner: unknown
source_refs: [SAMPLE-SRC-001]
related_ids: []
review:
  state: pending
  reviewer: null
  reviewed_at: null
writing_review:
  standard: ASD-STE100
  automated_check: NOT_RUN
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
    - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Prepare an initial candidate event

## Subject and event preparation

SAMPLE-REQ-001 is an illustrative requirement.
No actual lifecycle change occurred.
Do not write this preparation example into evidence/knowledge/audit/.

## Event YAML

```yaml
id: SAMPLE-EVENT-001
item_id: SAMPLE-REQ-001
item_version: 1
actor: null
at: null
action: transition
from_state: untracked
to_state: candidate
content_sha256: null
reason: Illustrate the fields needed for a new candidate event.
evidence:
  - resource: null
    revision: null
    sha256: null
```

The null fields make this sample invalid as an actual audit event.
They prevent missing identities and hashes from becoming fabricated evidence.

## Pre-write checks

The actual actor, event time, final item hash, and registered evidence remain missing.
Execution status is NOT_RUN.
No audit file exists for this sample.
Actual events must use the supported schema and a new filename.

## Evidence and open questions

| Kind | Statement | Evidence or required source | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- | --- |
| Unknown | No actual artifact transition occurred. | SAMPLE-SRC-001 is illustrative context only. | An audit event cannot truthfully record this transition. | unknown | Wait for an actual authored candidate and its evidence. |
| Unknown | Actor and final content hash are unavailable. | Required event values are null. | The draft cannot satisfy audit validation. | unknown | Record actual values from the completed change. |
````

## Completion checks

- The event describes an actual change and actor.
- Its content hash matches the final complete Markdown bytes.
- Each evidence entry matches retained provenance.
- The transition and timestamp order satisfy the audit contract.
- The filename is new and earlier events remain unchanged.
- Approval claims use actual human review and matching verification evidence.
