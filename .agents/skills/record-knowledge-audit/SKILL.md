---
name: record-knowledge-audit
description: Append truthful immutable governance events for prepared record bytes while preserving prior events and preventing duplicate retry writes.
---

# Record knowledge audit events

Input: final prepared records and hashes, permitted transitions, exact source evidence, and actual review or approval records.
Output: new event YAML paths bound to the final record bytes, or an existing matching result on retry.
Use [the audit schema](../../../core/knowledge/schemas/audit-event.schema.json) and [review gates](../../../knowledge/README.md#review-gates).

## Append events

1. Recheck each prepared full-file hash before writing. Finish all record metadata and formatting before computing event hashes.
2. Inspect existing events and operation evidence. Resume an existing matching result instead of duplicating an event on retry.
3. Write each new event as `knowledge/evidence/audit/<id>.yaml`. Never overwrite or remove an earlier event.
4. Record item ID, version, actor, timezone-aware timestamp, action, states, final SHA-256, reason, and nonempty exact evidence references.
5. Record only actual actors, times, verification, approvals, and source authority. Git and hashes do not authenticate an actor.
6. Correct an earlier event through a new event with `previous_event_id`. Preserve the earlier bytes and the correction rationale.

Verification metadata and its matching transition event must identify the same actor, time, item ID, version, and current hash.
Published requirements and decisions need a matching `human:<id>` verifier and approval actor for the current hash.
Approval follows that actor's verification. Publication follows approval. Approval events start from `verified` under the contract.

The base validator permits unaudited candidates. The ingestion harness requires a current event for its changed selected records.
Use that operation's stricter requirements without claiming every candidate requires publication approval.
Earlier events remain immutable even when their content hash differs from the current record.

## Stop and complete

If a prepared hash changed or required review evidence is missing, stop affected writes and return to preparation.
After a later content correction, repeat affected review and preparation, then append the required correction or successor event.
Run [integrity checks](../check-knowledge-integrity/SKILL.md) after appending events. Final checks cannot defer required gates.
Return event paths, record bindings, correction links, and remaining findings separately from publication or execution claims.
