---
name: analyze-requirement
description: Start issue or requirement intake with the existing template, resolve material ambiguities, and assess evidence before implementation.
---

# Analyze an issue or requirement

Use this procedure with any coding agent.
The Workbench core owns context, relationships, evidence, and execution records.
Use registry references to inspect existing assets in their current locations.

## Start intake immediately

Select the existing authoring template before discovery, diagnosis, or implementation.
Use the [defect report](../../../knowledge/templates/sdlc/defect-report.md) for an unexpected observed behavior.
Use the [requirement](../../../knowledge/templates/sdlc/requirement.md) for a requested behavior.
Read the [authoring contract](../../../knowledge/templates/sdlc/README.md) and copy only the selected Template block.
Update an existing intake when one already covers the issue. Preserve its stable ID and answer history.

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

Ask focused questions about material ambiguities and suspicious conditions.
Ask only questions that can change investigation, impact, expected behavior, or the next decision.
Use small question rounds. Inspect available evidence between rounds.
Do not re-ask answered details unless evidence conflicts. State the conflict when confirmation is necessary.
For each question, record its ID, answer, answer source, status, resolution owner, consequence, and next action.
Mark an unavailable owner `unknown`. Keep hypotheses in a separate table with supporting and contradicting evidence.

For browser session issues, examine timing, tab visibility, browser sleep, device sleep, and user actions.
Check session policy, network changes, VPN, SSO state, extensions, browser version, and effective settings when relevant.
Use the defect template's reproduction fields. Do not treat this list as mandatory questions for every issue.
For requirements, retain the same intake tables under `Facts, inferences, and unresolved questions`.

Assess readiness for a named investigation scope, separately from approval to implement or publish.
Readiness requires clear expected and observed behavior, environment, timing, actions, impact, and an explicit evidence plan.
A proposed expectation or bounded impact statement can support investigation when its limits remain explicit.
Use `READY`, `READY_WITH_LIMITS`, or `NEEDS_CLARIFICATION`, with reasons and blocked actions.
Unresolved policy or PROD revision permits `READY_WITH_LIMITS` for authorized local evidence collection.
It prevents claims about approved policy or PROD parity.
Continue authorized source inspection and safe evidence collection while independent questions remain open.
Do not infer runtime implementation approval from intake readiness.

## Analyze the selected scope

1. **Discover:** Read `ai-sdlc --workspace PATH status`, or call MCP `workbench_status`.
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
Use the shared [evidence handoff](../verify-implementation/references/behavior-review.md#keep-one-evidence-handoff) for later code and assertion mapping.
Give each finding an evidence source, consequence, owner, and next action.
Mark unknown owners explicitly.

Phase 1 uses agent reasoning and existing tool execution.
Automated governance and complete behavior verification remain future core capabilities.
A passing command does not establish `VERIFIED` behavior.
