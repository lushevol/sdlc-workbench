# Business task intake and evidence

Start business behavior requirements and defects in existing repositories under `tasks/<task-id>/` before discovery or diagnosis.
Use one stable folder for the task across SDLC stages.
Update an existing task when it already covers the request.

The current consumers are requirement intake, the portal session investigation, and its change review.
This structure keeps questions, conclusions, and evidence available outside chat history.
The [intake skill](../.agents/skills/analyze-requirement/SKILL.md) applies this procedure.
Agents assess the gate. The core runtime does not enforce workflow transitions.

## Scope

Classify work by its effect on business behavior.

| Work scope | Required record | Examples |
| --- | --- | --- |
| Business behavior in existing repositories | Business task; update domain knowledge when its meaning changes | Portal session rules, feature requirements, service outcomes, and business regressions |
| Harness maintenance only | Code, applicable guides, checks, and Git commits; no task or business knowledge record | Workbench configuration, dependency upgrades, browser setup, tooling, and template maintenance |
| Mixed business and harness work | One business task; handle harness support as maintenance | Reproduce a portal defect using locally configured browser tools |

A configuration change that alters business behavior follows business intake.
Harness maintenance does not require business clarification logs, knowledge publication, or governance audit events.
Keep harness artifacts in a business task only when they support its investigation or verification.
Preserve existing source snapshots and governance history. This scope rule does not authorize their removal.

## Create the task

Choose a stable identifier without path separators.
Create the task folder before reading additional project sources.
Select the [requirement](../core/knowledge/templates/sdlc/requirement.md) or [defect](../core/knowledge/templates/sdlc/defect-report.md) template.
Copy only its Template block into `intake.md`.
Keep required sections and record supplied facts before asking questions.
If template creation fails, repair and save the intake before domain discovery.
Then discover registered sources and grants with workspace status before domain source review.

```text
tasks/
├── README.md
└── <task-id>/
    ├── intake.md                  # Initial issue, investigation, and named readiness decision.
    ├── change-review.md           # Later change scope, impact, and stage readiness when needed.
    └── evidence/
        ├── index.md               # Source, claim, revision, hash, result, and limits.
        └── ...                    # New source captures, investigation outputs, and checks.
```

Keep `intake.md` as the living issue or requirement document during initial investigation.
Update its current understanding and link supporting evidence. Do not create another report for each investigation round.
After investigation completes, preserve its bytes as the intake baseline.
Record later changes in a separate stage record. Follow [the post-change procedure](#review-completed-code-changes).
Keep the intake, current stage record, and a short evidence index prominent. Apply the priorities below to supporting files.
Keep necessary later plans inside the same task when those stages become ready.
Create subdirectories only when an investigation produces artifacts.
Do not copy runtime source or relocate business repositories into a task.

## Critical conclusions in task documents

Add a prominent callout for critical conclusions to every new or revised human-facing document under `tasks/<task-id>/`.
This includes intake, stage records, reports, findings, plans, and evidence indexes.
Place it after frontmatter and the title, before detailed analysis.
Use a concise, bold lead sentence for each conclusion that requires user attention, action, or a decision.
Order critical conclusions by their effect on the current decision.

State the required action, consequence, accountable owner, and supporting evidence for each critical conclusion.
Use exact evidence locators and state material evidence limits with the conclusion.
Mark an unavailable owner `unknown`.
Name the blocked action or stage when a known blocker exists.
Keep the callout short and link supporting details instead of repeating the analysis.

Use this format when action is required:

```markdown
> **Critical conclusions: Action required**
>
> **[Decision or blocker requiring attention].**
> Action: [specific next action]. Consequence: [impact or blocked stage].
> Owner: [accountable owner or unknown]. Evidence: [source and exact locator].
```

When applicable, state: **No critical conclusions require user attention or action.**
This statement does not establish readiness, business approval, or release approval.

Apply this rule to current documents going forward.
Do not retrofit callouts into frozen records, historical reports, raw captures, or source snapshots.
Preserve their bytes and existing evidence identities.
Identify stale or historical conclusions in the current document and link their preserved sources.
Record new conclusions in the current stage record when the intake is frozen.

## Link task definitions and evidence

Use inline Markdown links for cross-document criteria, test cases, findings, evidence, and sources in human-facing task documents.
Place each link beside the claim or decision that uses it.
Link AC and TC IDs to their exact criterion or test case definitions.
Use a stable heading anchor or a supported line locator. Link every ID in a range separately.
Identify changed or historical requirement and test versions with their exact Git revision or SHA-256.

Link behavior definitions, test assertions, and retained execution evidence separately.
Make Given/When/Then conditions, actions, expected outcomes, and limits traceable to the linked behavior definition.
Do not invent missing BDD, policy, source authority, or approval.
Mark unavailable definitions and unresolved policy explicitly. Record their owner and next action; use `unknown` when the owner is unavailable.
Source links do not establish business authority or passing execution.

Apply these rules to new and revised current documents.
Preserve frozen records, historical reports, raw captures, source snapshots, and immutable audit bytes.
Provide current navigation links to preserved historical documents and their exact source versions.
Explain changed interpretations in the current stage record. Do not rewrite frozen definitions or retained evidence to add links.

## Gather and clarify

Use three evidence sources:

| Source | Inspect | Record |
| --- | --- | --- |
| Domain knowledge and evidence sources | Read `knowledge/` for domain records. Read cited originals through `evidence/knowledge/` or registered sources. | Applicable criteria, authority, conflicts, revisions, and limits. |
| Registered repositories, optionally under `repos/` | Exact implementation revisions and actual test-engine assertions. | Repository ID, commit, file, symbol or assertion, and coverage limits. |
| Investigation results | Existing reports, browser observations, service flows, and retained test executions. | Environment, method, inputs, timestamps, assertions, actual outcomes, and artifacts. |

Machine paths remain in ignored `workspace.local.yaml` when possible.
Repository metadata does not grant execution or prove deployed behavior.
Read sources before treating retrieved text as intent.
Tests can reveal implemented expectations. They cannot establish a future business rule alone.

Repeat this intake loop until the evidence supports the next stage:

1. Record known facts, suspected conditions, impact, and the requested outcome.
2. Search available knowledge, code, tests, and prior investigations for material answers.
3. Separate documented intent, observed behavior, inference, contradiction, and missing evidence.
4. Ask a small set of focused questions that can change the next decision.
5. Record each answer, source, resolution owner, consequence, and next action.
6. Collect evidence that tests the important hypotheses and suspicious boundaries.
7. Apply completed knowledge clarifications and record their knowledge updates.
8. Review the evidence and record the scoped readiness decision.

Do not repeat answered questions without an identified conflict.
Mark an unavailable owner `unknown`.
Keep the task open when a material ambiguity remains.
An unexplained confidence label cannot replace supporting evidence.

## Update knowledge after clarification

Identify ambiguous, missing, or stale knowledge during source review.
Resolve material gaps through available sources or the responsible owner. Keep unresolved conflicts open.
When clarification changes business understanding, update the domain knowledge record or create its candidate successor before handoff.
Do not leave resolved knowledge only in chat or task notes.
Use the existing [knowledge templates](../core/knowledge/templates/) and [governance procedure](../.agents/skills/govern-knowledge/SKILL.md).

Record the answer source, authority, scope, environment or version, and remaining evidence limits.
Add measurable Gherkin criteria when the clarification changes required behavior.
Link the task question and evidence to the updated record, finding resolution, and new audit events.
Keep prior source bytes, record identities, and audit history available.
Keep changed content as a candidate until required reviews permit publication.
Important requirements and decisions require recorded human review before publication.

Complete the intake template's knowledge-update log for each material knowledge gap.
Record `not applicable` and its reason when an answer changes no domain knowledge.
Incident observations and reported symptoms remain task evidence. They do not establish a general business rule.
Keep logs, execution materials, and investigation reports under the task.
Keep `knowledge/` limited to reusable business-domain Markdown records and navigation.
Do not copy task progress, code snapshots, fixtures, or Workbench maintenance into the knowledge base.
Link stable evidence references from domain records when needed.

## Investigate the current system

For UI behavior, use a real browser or Playwright when observable behavior matters.
Retain the pre-implementation state, actions, screenshots or snapshots, traces, and relevant requests.
Use the [browser guide](../docs/BROWSER_INVESTIGATIONS.md) for isolated tooling and evidence limits.
Choose controls that test competing explanations when causation matters.
Distinguish a tooling smoke from reproduction of a business issue.
Browser investigation screenshots are not unit-test evidence unless the executed unit test produced them.
Label each screenshot with its run, time, phase, capture method, supported claim, and limits.
Mark unknown capture details explicitly. Keep synthetic tooling captures separate from business reproduction evidence.

For service or business behavior, inspect the relevant live data flow when authorized access exists.
Use PROD when the question requires PROD evidence and the authorized connector permits it.
Retain deployment identity, request or event boundaries, responses, correlations, and relevant observations.
If required PROD evidence is unavailable, record the missing access or deployment evidence as a blocker.
Local substitutes cannot establish PROD parity.
Do not require PROD execution for a task whose decision does not depend on PROD behavior.

Inspect existing test cases and their actual assertions before using them as behavioral evidence.
Record assertion revisions and retained results. Distinguish an unexecuted test from a passing execution.
Source inspection and authorized investigations remain part of intake while the next stage is blocked.

## Keep evidence with the task

Save meaningful new task evidence under the task's `evidence/` directory.
Configure output paths where supported.
If a tool writes elsewhere, copy meaningful task evidence without changing its bytes.
Record both locations and matching hashes.
Exclude credentials and raw tokens from retained evidence.
Identify redacted captures as redacted and state their evidence limits.

Keep `evidence/index.md` short. Lead with the evidence needed to assess current claims and decisions.
Use a machine-readable manifest for detailed file inventories and hashes when the inventory becomes large.
Use these columns for the key evidence:

| Evidence ID | Claim or question | Locator and retained path | Exact revision or capture time | SHA-256 | Result and limits |
| --- | --- | --- | --- | --- | --- |

Use source IDs from the intake's Sources section.
Record command arguments, exit codes, environment, runtime versions, and assertion outcomes for executions.
Retain failures and partial results when they support a claim, unresolved question, or consequential investigation limit.
Preserve contradictory evidence. Add new meaningful runs instead of overwriting retained runs.
Explain the relationship between source evidence and each conclusion.

Keep authoritative domain snapshots under `evidence/knowledge/sources/` and immutable events under `evidence/knowledge/audit/`.
Reference them from the task index with their revision and hash. Never rewrite their bytes or history.
An explicit user request can relocate task evidence, including registered execution snapshots, into its task.
For each move, record the original locator, destination locator, revision, and matching SHA-256 hashes in a relocation manifest.
Preserve source IDs, resource names, revisions, and hashes. Update affected snapshot locators and references.
Keep provenance manifest records and immutable audit events. Validate relocated bytes against their recorded hashes.
Governed publication still uses the existing knowledge contracts and append-only audit events.
Keep the task evidence and link any additional governance snapshot or record.

## Save case evidence and resume checkpoints

Set supported artifact output paths to the task evidence directory before execution.
If a tool cannot write there, copy each completed result immediately and verify its hashes.

Save each completed case immediately, including cases that finish in parallel.
Do this before starting another case, waiting for other runs, or handing off work.
Do not wait for the full suite to finish.
Save results under the task's durable `evidence/` path. Ignored runtime folders and chat alone do not preserve completed evidence.

Record the case and run IDs, expected predicates, actual values, status, start and end times, and exact source revisions.
Retain source and configuration hashes, assertion links, screenshots, result files, artifact hashes, fixture identity, and material limits.
Preserve failures, errors, skips, blocked cases, and partial results with their limits.
Copy completed outputs from temporary locations without changing their bytes. Record both locators and matching hashes.

Update the case inventory or progress manifest, and the evidence index, after each completed case.
Keep these records consistent when parallel cases complete.

Capture volatile lifecycle events before navigation, reload, page closure, browser teardown, or other state replacement.
Save a long-run checkpoint before extended waits, planned interruptions, context compaction, or handoff.
Include completed case IDs, current case state, retained paths and hashes, pending actions, and resume instructions.
After an unexpected interruption, preserve available partial evidence and pending actions as soon as work can resume.
Update checkpoints for meaningful state changes or interruption boundaries. Do not create duplicate checkpoints while state remains unchanged.

At resume and completion, reconcile saved case IDs, statuses, counts, revisions, hashes, and artifacts.
Identify incomplete or interrupted cases explicitly. Do not infer their outcomes from process exit, case names, or prior runs.
Keep frozen intake, retained raw evidence, and immutable audit history unchanged.
Record current progress through the existing stage record, inventory, and evidence index.

## Evidence priorities and cleanup

| Priority | Keep | Presentation |
| --- | --- | --- |
| Necessary | Initial `intake.md`, current stage record when needed, and a short `evidence/index.md` | Main entry points |
| Important | Direct claim-bearing executions, source snapshots, inspected assertions, useful screenshots, and required provenance | Link from the intake or index |
| Unimportant | Redundant reports, repeated attempts without distinct findings, empty output, and unrelated harness bulk | Delete during authorized cleanup |

Classify by current consumer and evidence value. A failure or unresolved question can make evidence important.
Keep only useful harness artifacts in a business task. Maintain general harness guidance outside business tasks.
Do not replace clutter with archive folders or another summary report.

For authorized cleanup, record removed paths, SHA-256 hashes, prior Git revisions, and reasons in one machine-readable record.
Use `null` for an unavailable prior revision. State when Git cannot recover an untracked artifact.
Keep registered raw snapshots, stable source identities, prior provenance manifests, and immutable audit events unchanged.
Repair active links and inventories. Historical locators can resolve through the cleanup record and retained Git revision.
Validate retained hashes and references after cleanup. Remove empty directories and redundant check outputs.

## Decide whether intake can finish

Name the proposed next stage and the evidence required for that decision.
Check the following points before leaving intake:

- The problem or requested behavior, affected actors, scope, and business impact are clear.
- Expected behavior has a source. Current behavior has evidence or an explicit, justified applicability limit.
- Acceptance criteria identify conditions, actions, observable results, and required limits.
- Material hypotheses, contradictions, dependencies, and suspicious conditions have supporting analysis.
- Necessary source inspection, assertions, and investigations have retained evidence.
- Completed knowledge clarifications have updated records, traceable sources, and the required audit and review state.
- No unresolved material question can change the proposed next-stage decision.

Record the decision inside `intake.md`:

| Status | Meaning | Permitted action |
| --- | --- | --- |
| `NEEDS_CLARIFICATION` | Material information or required evidence is missing. | Continue questions and authorized evidence collection. Block the next stage. |
| `READY_WITH_LIMITS` | Some facts support further investigation, but material uncertainty remains. | Continue intake evidence collection only. Block the next stage. |
| `READY` | Evidence supports the named next stage, with no unresolved material uncertainty. | Proceed within existing authorization and applicable review requirements. |

Identify the assessor, assessment time, evidence references, unresolved items, and blocked actions.
Use the actual agent or human identity. Do not invent an accountable business owner or approval.
Explain why each deferred item cannot change the next-stage decision.
If new evidence contradicts completed intake, record the conflict in a successor stage record.
Preserve the original intake bytes. Resolve material scope changes before the affected next stage.
Readiness does not establish business approval, publication approval, or passing business execution.

Run artifact lint against explicit completed artifacts, rather than the mixed task folder.
Retain the result under the task. Address errors and explain remaining warnings.
The [document validation skill](../.agents/skills/validate-sdlc-documents/SKILL.md) defines the applicable checks.

## Review completed code changes

Freeze `intake.md` after its issue definition and investigation finish.
Do not add change progress, review findings, or execution results to that baseline.
Record its exact Git revision and SHA-256 in `change-review.md` or an equivalent identified stage record.
An explicit user freeze applies immediately, including when wider issue closure remains open.
Verify the intake hash before and after each stage.

Use the [change request template](../core/knowledge/templates/sdlc/change-request.md) for the stage record.
Keep its `artifact_kind: change-request`. Record implemented code as implemented, with exact source evidence.
Reuse existing impact reports when they cover the selected diff. Extend their evidence without duplicating conclusions.
Use the [post-change procedure](../.agents/skills/impact-analysis/references/post-change-review.md) for the following sequence:

1. Identify exact base and head commits, changed paths, local modifications, requirements, and preserved intake bytes.
2. Analyze affected user journeys and system paths. Include unchanged callers, consumers, contracts, and qualitative risks.
3. Review the actual diff. Record suggestions without editing application code when the user requests review only.
4. Expand executable E2E coverage from changed paths and review risks. Keep original defect cases in scope.
5. Run every declared original and new case in a real browser. Retain assertions, failures, screenshots, and source bindings.
6. Assess the next named stage from current evidence. Keep incomplete browser execution explicitly open.

Store each stage decision in the current stage record, not the frozen intake.
Record the phase, status, assessor, timestamp, rationale, evidence, blocked actions, owner, and next action.
`READY` permits only that named stage within existing authorization.
`READY_WITH_LIMITS` permits more evidence collection for that decision. `NEEDS_CLARIFICATION` blocks the dependent stage.
A ready review stage does not establish browser execution readiness, business approval, or release approval.
A failed or blocked case cannot count as completed passing execution.

Keep later questions and knowledge-update references in the current stage record.
Apply material knowledge clarifications through the existing governance procedure. Preserve the intake baseline.
When intent changes, identify a successor requirement or change request and its authority.
Do not rewrite original evidence to match later intent.

## Distribution boundary

New workspaces receive this guide and the existing templates and skills.
They receive no task records or evidence from the source checkout.
This procedure adds no dependency, background investigation, or automatic PROD access.

## Output review

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
