# Business task intake and evidence

Start business behavior requirements and defects in existing repositories under `tasks/<task-id>/` before discovery or diagnosis.
Use one stable folder for the task across SDLC stages.
Update an existing task when it already covers the request.

The current consumers are requirement intake and the portal session investigation.
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
Select the [requirement](../knowledge/templates/sdlc/requirement.md) or [defect](../knowledge/templates/sdlc/defect-report.md) template.
Copy only its Template block into `intake.md`.
Keep required sections and record supplied facts before asking questions.
If template creation fails, repair and save the intake before domain discovery.
Then discover registered sources and grants with workspace status before domain source review.

```text
tasks/
├── README.md
└── <task-id>/
    ├── intake.md                  # Selected template, questions, and readiness decision.
    └── evidence/
        ├── index.md               # Source, claim, revision, hash, result, and limits.
        └── ...                    # New source captures, investigation outputs, and checks.
```

Keep `intake.md` as the main living issue or requirement document.
Update its current understanding and link supporting evidence. Do not create another report for each investigation round.
Keep necessary later plans inside the same task when those stages become ready.
Create subdirectories only when an investigation produces artifacts.
Do not copy runtime source or relocate business repositories into a task.

## Gather and clarify

Use three evidence sources:

| Source | Inspect | Record |
| --- | --- | --- |
| `knowledge/` and registered knowledge sources | Domain terms, rules, requirements, prior answers, decisions, and cited source bytes. | Applicable criteria, authority, conflicts, revisions, and limits. |
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
Use the existing [knowledge templates](../knowledge/templates/) and [governance procedure](../.agents/skills/govern-knowledge/SKILL.md).

Record the answer source, authority, scope, environment or version, and remaining evidence limits.
Add measurable Gherkin criteria when the clarification changes required behavior.
Link the task question and evidence to the updated record, finding resolution, and new audit events.
Keep prior source bytes, record identities, and audit history available.
Keep changed content as a candidate until required reviews permit publication.
Important requirements and decisions require recorded human review before publication.

Complete the intake template's knowledge-update log for each material knowledge gap.
Record `not applicable` and its reason when an answer changes no domain knowledge.
Incident observations and reported symptoms remain task evidence. They do not establish a general business rule.
Keep logs and execution materials under the task. Link their stable source references from knowledge when needed.

## Investigate the current system

For UI behavior, use a real browser or Playwright when observable behavior matters.
Retain the pre-implementation state, actions, screenshots or snapshots, traces, and relevant requests.
Use the [browser guide](../docs/BROWSER_INVESTIGATIONS.md) for isolated tooling and evidence limits.
Choose controls that test competing explanations when causation matters.
Distinguish a tooling smoke from reproduction of a business issue.

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

Save all new task evidence under the task's `evidence/` directory.
Configure output paths where supported.
If a tool writes elsewhere, retain its original output and copy the task evidence without changing its bytes.
Record both locations and matching hashes.
Exclude credentials and raw tokens from retained evidence.
Identify redacted captures as redacted and state their evidence limits.

Maintain `evidence/index.md` with these columns:

| Evidence ID | Claim or question | Locator and retained path | Exact revision or capture time | SHA-256 | Result and limits |
| --- | --- | --- | --- | --- | --- |

Use source IDs from the intake's Sources section.
Record command arguments, exit codes, environment, runtime versions, and assertion outcomes for executions.
Retain failed results and partial evidence. Add new runs instead of overwriting previous runs.
Explain the relationship between source evidence and each conclusion.

Keep authoritative domain source snapshots and audit records at their established paths.
Reference them from the task index with their revision and hash. Never rewrite their bytes or history.
An explicit user request can relocate task evidence, including registered execution snapshots, into its task.
For each move, record the original locator, destination locator, revision, and matching SHA-256 hashes in a relocation manifest.
Preserve source IDs, resource names, revisions, and hashes. Update affected snapshot locators and references.
Keep provenance manifest records and immutable audit events. Validate relocated bytes against their recorded hashes.
Governed publication still uses the existing knowledge contracts and append-only audit events.
Keep the task evidence and link any additional governance snapshot or record.

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
Reopen intake if new evidence contradicts its baseline.
Readiness does not establish business approval, publication approval, or passing business execution.

Run artifact lint against explicit completed artifacts, rather than the mixed task folder.
Retain the result under the task. Address errors and explain remaining warnings.
The [document validation skill](../.agents/skills/validate-sdlc-documents/SKILL.md) defines the applicable checks.

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
