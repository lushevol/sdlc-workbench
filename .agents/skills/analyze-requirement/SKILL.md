---
name: analyze-requirement
description: Create task intake from an existing template, drill material ambiguities, and retain evidence before any downstream SDLC phase.
---

# Analyze an issue or requirement

Use this procedure with any coding agent.
The Workbench core owns context, relationships, evidence, and execution records.
Use registry references to inspect existing assets in their current locations.

## Start intake immediately

Create `tasks/<task-id>/` at the workspace root before discovery, diagnosis, or implementation.
Follow the [task contract](../../../tasks/README.md) for storage, evidence, and handoff.
Use the [defect report](../../../knowledge/templates/sdlc/defect-report.md) for an unexpected observed behavior.
Use the [requirement](../../../knowledge/templates/sdlc/requirement.md) for a requested behavior.
Read the [authoring contract](../../../knowledge/templates/sdlc/README.md). Copy the selected Template block into `tasks/<task-id>/intake.md`.
Update the same task when it already covers the request. Preserve its stable ID, earlier answers, and evidence history.
If template creation fails, repair and save the intake before domain discovery.
After saving intake, discover registered sources and tool grants with workspace status before domain source review.

Record supplied facts and prior answers first. Cite their message, document, or evidence locator.
Keep reported symptoms separate from directly observed reproductions and approved expected behavior.
Mark a proposed expectation as proposed when its policy source is unavailable.
Use explicit unknowns. Missing exact deployed revisions must not prevent safe local investigation.

Search existing knowledge before asking the user for policy or previously recorded context.
Read the knowledge index, relevant domain indexes, linked requirements, prior answers, and cited source bytes.
Use registered knowledge search and read operations when available. Otherwise inspect local sources directly.
Record the search scope, source revision or hash, applicable criterion IDs, conflicts, and retrieval limits in the intake.
Distinguish documented user intent from publication approval. Pending governance does not erase recorded intent.
Do not call a policy missing until the bounded source review fails to resolve the material question.
When sources conflict, name the conflict and ask only for the decision that available evidence cannot resolve.

Next inspect registered repositories, exact implementation revisions, test assertions, and investigation results.
Repositories can use optional `repos/` clones or configured locations. Do not move independent business repositories.
Use existing reports as secondary evidence alongside their cited sources.
Reports summarize evidence. Read their cited code, assertions, and retained results before relying on conclusions.
A test name or passing command does not establish the asserted business behavior.

Drill material ambiguities and suspicious conditions with focused questions and evidence checks.
Ask only questions that can change investigation, impact, expected behavior, or the next decision.
Use small question rounds. Inspect available evidence between rounds.
Do not re-ask answered details unless evidence conflicts. State the conflict when confirmation is necessary.
For each question, record its ID, answer, answer source, status, resolution owner, consequence, and next action.
Mark an unavailable owner `unknown`. Keep hypotheses in a separate table with supporting and contradicting evidence.

For browser session issues, examine timing, tab visibility, browser sleep, device sleep, and user actions.
Check session policy, network changes, VPN, SSO state, extensions, browser version, and effective settings when relevant.
Use the defect template's reproduction fields. Do not treat this list as mandatory questions for every issue.

## Collect evidence during intake

Investigation remains part of intake until material uncertainty is resolved for the named next phase.
Use real browser or Playwright execution when UI behavior needs direct observation.
Inspect the current state and pre-implementation behavior. Retain controls, environment identity, mocks, and observer effects.
For service or business behavior, inspect the live data flow when the next decision needs runtime evidence.
Use production evidence only within existing authorization and available access. Never infer production parity from local execution.
If required production evidence is unavailable, record the block, responsible owner, consequence, and next action.
Do not require production access for an unrelated documentation or harness task.
Inspect test-engine setup, helpers, fixtures, and assertions before inferring current behavior.
Separate assertion inspection from actual execution and expected behavior from implementation behavior.

Retain each new investigation result under `tasks/<task-id>/evidence/` with an evidence index.
Index source locators, hashes, exact revisions, claim IDs, results, and evidence limits.
Reference existing raw snapshots, manifests, and audit events at their original paths. Never move or rewrite their history.
Record each evidence round and its effect on open questions. Preserve failed, stale, and contradictory results.

## Gate the next phase

Record the named next phase, readiness, rationale, evidence limits, blocked actions, owner, and next action.
Use `READY` only when no unresolved material uncertainty can change that phase's scope, behavior, or decision.
Explain why remaining unknowns do not affect that phase. State facts and inferences separately.
Use `READY_WITH_LIMITS` only for continued evidence collection. It never permits a downstream SDLC phase.
Use `NEEDS_CLARIFICATION` when material intent or evidence gaps remain. It blocks downstream SDLC work.
Continue authorized evidence collection while questions remain open. Reassess readiness after each material answer or result.
Do not infer business approval from readiness. Preserve existing authorization and record any separately required approval.

## Analyze the selected scope

1. **Discover:** Reuse the intake's `ai-sdlc --workspace PATH status` result, or MCP `workbench_status`.
   Refresh discovery when configured sources or access change.
   Select relevant capabilities, knowledge resources, repositories, and tool operations.
   Read each operation schema before calling it.
2. **Understand:** Read exact requirement, acceptance criteria, design, and decision sources.
   Record source locators, revisions, authority, and freshness.
   Separate approved intent from drafts, current implementation, and inferred behavior.
   Use [behavior extraction](../verify-implementation/references/behavior-review.md#extract-atomic-behaviors) when creating or revising a story baseline.
   Retain atomic predicates, stable story-qualified IDs, negative cases, and measurable Gherkin.
3. **Relate:** Map each expected behavior to business capabilities and relevant services.
   Attach source references to each relationship.
   Mark candidate links and missing evidence explicitly.
4. **Analyze:** Identify conflicting rules, missing conditions, unclear outcomes, and acceptance criteria that tests cannot evaluate.
   Use the shared [gap categories](../verify-implementation/references/behavior-review.md#classify-gaps) for requirement findings and unresolved intent.
   A search miss does not prove that a rule does not exist.
   Request an owner decision only when available evidence cannot resolve a material ambiguity.
5. **Execute:** Invoke relevant configured operations through CLI `call` or MCP `workbench_call`.
   Preserve the task scope and existing authorization.
   Continue independent work when a missing decision blocks only part of the analysis.
6. **Verify:** Check that every behavior has a source and a testable expected result.
   Retain action IDs and evidence references.
   State confirmed facts, inferences, and unresolved questions separately.

Use this CLI form with discovered resource IDs, operation names, and schema arguments:

```text
ai-sdlc --workspace PATH call RESOURCE OPERATION --args JSON
ai-sdlc --workspace PATH runs
```

Report the behavior baseline and remaining requirement gaps.
Apply the phase gate before handing the baseline to impact analysis, design, implementation, or downstream verification.
Use the shared [evidence handoff](../verify-implementation/references/behavior-review.md#keep-one-evidence-handoff) for later code and assertion mapping.
Give each finding an evidence source, consequence, owner, and next action.
Mark unknown owners explicitly.

Phase 1 uses agent reasoning and existing tool execution.
Automated governance and complete behavior verification remain future core capabilities.
A passing command does not establish `VERIFIED` behavior.
