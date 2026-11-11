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

Apply the [investigation and confidence rules](../../../tasks/README.md#investigate-before-asking) before sending unresolved questions to the user.

Keep Workbench lifecycle state separate from OKF `status` and execution outcomes.
Keep `knowledge/` limited to business-domain Markdown records and navigation.
Business-system technical knowledge qualifies when it defines intended domain behavior, contracts, or responsibilities.
Keep knowledge focused on requirements, intent, and ideal target behavior.
Record actual implementation, deployment, observations, and intent-to-reality differences in independent task gap Markdown.
A source-backed implementation fact cannot redefine an intended rule.
Exclude Workbench maintenance, logs, raw sources, code copies, fixtures, execution results, reports, and intermediate files.
Store snapshots and their manifest under `evidence/knowledge/`.
Store findings under `evidence/knowledge/findings/` and new immutable events under `evidence/knowledge/audit/`.

1. **Discover:** Read the candidate, registered sources, retained snapshots, and relevant findings.
   Define the requirement, decision, capability, service, and contract scope.
   Inspect exact revisions and source locators.
2. **Investigate:** Check intent authority, freshness, consistency, completeness, and traceability.
   Distinguish a supported change of intent from code that restores or contradicts an existing rule.
   Keep the rule unchanged for implementation-only changes. Update the independent gap record instead.
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

## Reconcile the compiled wiki

Use the [llm-wiki bridge](../llm-wiki/SKILL.md) after authorized record or lifecycle changes.
Select [OpenKB](../openkb/SKILL.md) with both private `OPENAI_API_BASE` and `LLM_API_KEY`; otherwise use llm-wiki-agent in the current ADE context.
Read changed canonical sources and related compiled pages, then revise affected summaries, concepts, entities, source qualifications, and index entries.
In fallback mode, read llm-wiki-agent's original `AGENTS.md` and apply the bridge's current-layout and source-link constraints.
Preserve OpenKB metadata, treat summaries as derived source pages, and use explorations for saved synthesis.
Keep source symlinks immutable; do not invoke upstream scripted ingest or refresh against this layout.
Retain one active wiki and its existing rich pages; engine selection does not create duplicate content.
Run the bridge's local verification before reporting current wiki coverage.
Use local OpenKB verification and original visualization in either semantic mode when graph maintenance is requested.
Keep derived data under `knowledge/llm-wiki/` separate from canonical records and their audit history, with both raw and full-text source entries linked relatively to the canonical records.
Use the bridge's `compile` route with source links and hashes preserved. OpenKB uses explicit provider URL and token; no automatic OAuth.
Semantic lint, saved explorations, and graph relationships can inform investigation.
They cannot supply a reviewer, approve a rule, resolve source authority, or automatically transition a governed record.
Preserve candidate, contested, stale, and superseded qualifications in compiled pages and graph explanations.

## Apply completed clarifications

When material clarification resolves a knowledge gap, update the affected record or create a candidate successor.
Do this before handing off the resolved scope. Do not retain the answer only in chat or task notes.
Record the answer source, decision authority, applicable scope, environment or version, and remaining limits.
Add or revise measurable Gherkin criteria when the clarification changes required behavior.
Link the task question, retained evidence, affected record, and finding resolution.
Use the existing knowledge template. Preserve predecessor identity, source provenance, and earlier review history.
Keep incident logs, implementation facts, and execution evidence under their task.
Reference the independent gap document from knowledge navigation when needed. Keep actual-behavior descriptions and delivery status there.
A supported clarification changes knowledge only when it changes or resolves intended target meaning.

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
