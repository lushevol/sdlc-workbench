# Keep one current task view

Use this procedure for business task status, resume, and handoff requests.
It summarizes existing records. It creates no new workflow gate or runtime status.
For harness maintenance, report the engineering scope and checks directly.

## Choose the current record

Read the task intake, evidence index, relevant stage records, and the user's latest scope decision.
Identify the [entry route](../../../../tasks/README.md#lifecycle-entry-routes) before interpreting implementation or readiness.
Supplied code can predate intake. Preserve its actual dates and source identity without implying earlier approval.
Use the living intake during initial investigation.
After intake freezes, use the existing stage record that covers the selected scope.
Follow the [intake and stage boundaries](../../../../tasks/README.md#review-completed-code-changes).
Do not select a stage or result solely from a filename, modification time, or passing count.
If records conflict, identify the competing scopes and evidence. Mark the current stage unresolved until evidence selects it.

Place one short `Current task state` section near the top of the selected record.
Keep the required [critical conclusion](../../../../tasks/README.md#critical-conclusions-in-task-documents) before that section.
Reuse an existing summary when it serves this purpose.
Link the selected record from mutable task navigation, such as the evidence index.
Preserve frozen intake and historical evidence bytes. Do not create a separate status report for each update.

## Reconcile before summarizing

Check the current implementation, canonical cases, assertion mappings, and retained execution inputs before reusing a result.
Record exact repository IDs and commits. Include relevant local source hashes when uncommitted changes affect the selected scope.
Keep requirement and case revisions separate from implementation and test revisions.
For execution, identify the environment, configuration, fixture limits, and retained source bindings.
Mark unavailable identities explicitly. A branch name alone does not identify executed bytes.

| Evidence condition | Current view treatment |
| --- | --- |
| Result matches selected sources, assertions, environment, and scope | Report its asserted outcomes with evidence limits. |
| Result belongs to another branch, source revision, case version, or changed input | Keep the historical result. Mark its current applicability stale or unresolved. |
| Relevant results conflict | Show the conflict and the conditions of each run. Keep the decision open. |
| Execution is missing, interrupted, skipped, or blocked | State that status. Do not infer a passing outcome. |

Separate results for different revisions and environments. Do not combine their passing counts into current coverage.
Source inspection can support a prediction. Label it separately from executed behavior.
Use existing [assurance checks](../../../../docs/BEHAVIOR_REVIEW.md#validate-save-and-report) when a compatible baseline exists.
Those checks run on demand. They cannot decide whether evidence proves a claim or grants approval.

## Keep the view short and actionable

Use a compact table or a few paragraphs. Link detail instead of copying definitions or execution inventories.

| Item | Include |
| --- | --- |
| Current scope | Selected task, entry route, stage record, business goal, and latest applicable scope decision. |
| Independent dispositions | Implementation state, intent review, execution outcome, and business acceptance, each with its own evidence or explicit unknown. |
| Exploration boundary | Authorized experiment, permitted edits, measurable outcome, stop condition, and disposition; not applicable when no exploration exists. |
| Source identity | Current implementation and case versions; tested versions when they differ. |
| Result | Scoped outcome, current applicability, environment, and the evidence that supports the decision. |
| Readiness | Named next phase, existing readiness state, rationale, and material limits. |
| Blocker or decision | Required action, blocked activity, consequence, accountable owner or `unknown`, and supporting evidence. |
| Next action | One concrete action, its owner, and the observable result needed to finish it. |
| Navigation | Exact criterion and case definitions, executable assertions, retained results, and key screenshots when relevant. |

Link each AC or TC ID to its canonical definition through the [task reference rules](../../../../tasks/README.md#link-task-definitions-and-evidence).
Link executable scripts separately from readable case definitions and retained results.
Show where to find detailed steps without copying the canonical Gherkin into the summary.
Keep readiness, passing execution, business approval, and publication review separate.
Do not invent an owner, approval, policy threshold, or passing result to fill the view.

## Resolve known answers before questions

Before asking a question, inspect the intake answers, current stage decisions, relevant knowledge, and cited original sources.
Reuse the existing question log. Record whether each material issue is answered, conflicting, or unknown, with its source.
An unpublished candidate can record prior user intent. Keep its publication status explicit.

Apply the [investigation and confidence rules](../../../../tasks/README.md#investigate-before-asking).
Record resolved answers with confidence, rationale, exact source links, and limits before preparing residual questions.

Ask only about a material unknown or a conflict that available evidence cannot resolve.
For a conflict, cite the competing answers and explain which next decision they block.
Do not ask the user to repeat an available answer because its source needs further review.

## Refresh at meaningful boundaries

Refresh after a scope decision, source change, material case result, resolved question, blocker change, or readiness change.
Save completed case evidence first under the [case checkpoints](../../../../tasks/README.md#save-case-evidence-and-resume-checkpoints).
At resume, compare retained inputs with current sources before keeping a `current` label.
Before handoff, reconcile the view, case inventory, and evidence index. Preserve conflicting and historical outcomes.
Record when the view was assessed. Do not rewrite unchanged reports or add duplicate checkpoints while waiting.
