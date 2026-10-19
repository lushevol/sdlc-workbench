---
name: govern-knowledge
description: Investigate business-domain knowledge, record findings and reviews, and control evidence-backed publication for existing business repositories.
---

# Govern engineering knowledge

Use this procedure with any coding agent.
Apply it to business-domain knowledge for existing business repositories.
Changes limited to harness setup, configuration, tooling, dependencies, or Workbench maintenance require no task or business knowledge record.
Classify work by business impact using [the scope rules](../../../tasks/README.md#scope).
Maintain their engineering guides and configuration directly, with checks appropriate to the changed interfaces.
For mixed requests, govern only the affected business knowledge and track only the business scope in its task.
Preserve existing governed record integrity and audit history when those records actually change.
Read [the knowledge contract](../../../knowledge/README.md) before editing records.
Use its [schemas](../../../core/knowledge/schemas/) and [templates](../../../core/knowledge/templates/) for knowledge, findings, manifests, and audit events.
Keep Workbench lifecycle state separate from OKF `status` and execution outcomes.
Keep `knowledge/` limited to business-domain Markdown records and navigation.
Business-system technical knowledge qualifies when it explains domain behavior, contracts, or responsibilities.
Exclude Workbench maintenance, logs, raw sources, code copies, fixtures, execution results, reports, and intermediate files.
Store snapshots and their manifest under `evidence/knowledge/`.
Store findings under `evidence/knowledge/findings/` and new immutable events under `evidence/knowledge/audit/`.

1. **Discover:** Read the candidate, registered sources, retained snapshots, and relevant findings.
   Define the requirement, decision, capability, service, and contract scope.
   Inspect exact revisions and source locators.
2. **Investigate:** Check authority, freshness, consistency, completeness, and traceability.
   Record evidence for each claim.
   Preserve uncertainty as a finding with evidence, consequence, owner, and next action.
   Mark an unknown owner explicitly.
3. **Clarify:** Make acceptance criteria actionable and measurable.
   Use Gherkin conditions, actions, and observable results.
   Record missing business decisions without filling them from implementation intuition.
   Resolve ambiguous, missing, or stale knowledge through cited sources or the responsible owner.
   Keep unresolved conflicts open with an owner and next action.
4. **Review:** Record the actual reviewers, review times, evidence scope, and limits.
   Important requirements and decisions require human review before publication.
   Do not fabricate a review or treat generated text as approval.
5. **Prepare:** Validate the candidate before preparing its next state.
   Follow the candidate → investigated → verified → published lifecycle.
   Use contested, stale, or superseded when evidence requires those states.
   Retain the predecessor identity and supporting evidence during replacement.
   Prepare the proposed content, state, required approval evidence, and audit event together.
6. **Audit:** Add a new event YAML file for each proposed state or review change.
   Preserve earlier events and their Git history.
   Correct an earlier event through a new event that references it.
7. **Validate:** Run `ai-sdlc --workspace PATH validate` against the complete proposed records.
   Treat publication as complete only after required reviews and deterministic checks pass.
   Keep published knowledge separate from candidate records.
   Report deterministic check results and unresolved findings separately.
   Review the diff and preserve exact source evidence.

Validation checks records and provenance.
It does not authenticate humans, decide business correctness, or prove passing execution.
Knowledge review and behavior verification need different evidence.
Automatic AI governance and durable approval workflows remain future capabilities.

## Apply completed clarifications

When material clarification resolves a knowledge gap, update the affected record or create a candidate successor.
Do this before handing off the resolved scope. Do not retain the answer only in chat or task notes.
Record the answer source, decision authority, applicable scope, environment or version, and remaining limits.
Add or revise measurable Gherkin criteria when the clarification changes required behavior.
Link the task question, retained evidence, affected record, and finding resolution.
Use the existing knowledge template. Preserve predecessor identity, source provenance, and earlier review history.
Keep incident logs and execution evidence under their task. Reference them from knowledge through stable sources.

Complete the intake's knowledge-update log with record versions, criterion IDs, finding references, and audit references.
Record `not applicable` with a reason when an answer changes no domain knowledge.
Append a new audit event for each governance change. Never alter an earlier event.
Keep changed content as a candidate until the required review and publication gates pass.
Important requirements and decisions require recorded human review before publication.
Do not transfer an earlier approval to changed content or present reported behavior as approved policy.

## Prepare exact bytes before recording events

Use this order when changing governed records:

1. Finish wording, metadata, source references, scenarios, and file formatting.
2. Run content checks and perform the required semantic review against those proposed bytes.
3. Reconcile review summaries, finding resolutions, evidence limits, and the actual reviewed hash.
4. Keep ASD review fields pending unless a complete writing review occurred.
5. Compute the final full-file hash and append the required event files.
6. Recheck the prepared hashes and all governance gates after adding events.

The [ingestion harness](../ingest-knowledge/references/workflow.md#harness-commands) supplies prepared-content and final checkpoints.
Preparation can defer a selected missing transition event; final validation cannot.
The harness does not supply semantic review, verification, or human approval.
Its prepared hash identifies checked bytes, not an authenticated reviewer.

Avoid formatting or metadata changes after creating an event.
Any later edit changes the hash, including a trailing newline.
Preserve earlier events and create a corrected version or event under the knowledge contract.
Reference the predecessor with `previous_event_id` when correcting its event.
For a new review result, keep actual semantic review time separate from pending ASD review fields.
