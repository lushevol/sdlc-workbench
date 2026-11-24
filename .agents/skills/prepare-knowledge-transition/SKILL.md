---
name: prepare-knowledge-transition
description: Prepare final governed record bytes, actual review evidence, and the existing harness checkpoint before appending lifecycle audit events.
---

# Prepare a knowledge transition

Input: proposed records, baseline and plan, starting ID/version/hash bindings, intended transition, source evidence, and actual review or approval evidence.
Output: final proposed bytes, declared transition and review scope, and a `PREPARED` checkpoint or explicit blocking findings.
Preparation does not grant a review, human approval, or publication.

## Prepare exact bytes

1. Read [the knowledge contract](../../../knowledge/README.md#review-gates) and inspect existing versions, reviews, and events before preparing changes.
2. Reuse the baseline captured before source or record edits. If edits have not started, capture it now.
3. Confirm starting hashes still match. Reconcile concurrent changes before preparing affected writes or transferring review evidence.
4. Select a permitted transition. Preserve predecessor identity and history; changed meaning needs a sourced candidate or successor.
5. Finish wording, metadata, source references, Gherkin scenarios, finding resolutions, and formatting, including file endings.
6. Reconcile semantic review summaries, evidence limits, actual actors and times, and the bytes reviewed.
7. Run applicable writing checks. Keep ASD review fields pending unless a complete ASD review occurred.
8. Run the existing harness with `--phase prepare` using [the harness procedure](../ingest-knowledge/references/workflow.md#harness-commands).

Keep Workbench lifecycle state separate from OKF status and execution outcomes.
Use the normal candidate → investigated → verified → published path, with contested, stale, or superseded when supported.
Use the contract for exact permitted transitions. Superseded records retain history and have no next state.
Published requirements and decisions need actual human review and approval bound to the final content hash.
Do not carry earlier approvals onto changed content or invent actors, timestamps, authority, or evidence.

## Checkpoint and stop

Report selected paths, final ID/version/hash bindings, proposed states, review scope, required events, and pending decisions.
Do not present a later snapshot as pre-edit preservation evidence. Disclose a missing baseline and its verification limits.
A prepared checkpoint may defer selected missing transition events. It preserves the actual validation findings and deferred scope.
Complete semantic review against the prepared bytes before audit. The seal alone supplies no semantic review or human approval.
It cannot defer missing business decisions or supply semantic truth, verification, or human approval.
If preparation fails, repair the affected input and produce a new checkpoint. Preserve prior checkpoint evidence.
Any later document edit invalidates its prepared hash, including metadata or newline changes.
Repeat affected review and preparation before [recording audit events](../record-knowledge-audit/SKILL.md).
