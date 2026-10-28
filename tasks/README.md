# Business task intake and evidence

At Workbench entry, register business requirements and defects under `tasks/<task-id>/` before new discovery, diagnosis, or implementation.
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
Copy only its Template block into `01-intake.md`.
Keep required sections and record supplied facts before asking questions.
If template creation fails, repair and save the intake before domain discovery.
Then discover registered sources and grants with workspace status before domain source review.

```text
tasks/
├── README.md
└── <task-id>/
    ├── 01-intake.md               # Initial issue, investigation, and named readiness decision.
    ├── 06-test-cases.md           # Canonical Gherkin case definitions, when cases are defined.
    ├── 10-change-review.md        # Later change scope, impact, and stage readiness when needed.
    └── evidence/
        ├── index.md               # Source, claim, revision, hash, result, and limits.
        └── ...                    # New source captures, investigation outputs, and checks.
```

Keep `01-intake.md` as the living issue or requirement document during initial investigation.
Update its current understanding and link supporting evidence. Do not create another report for each investigation round.
After investigation completes, preserve its bytes as the intake baseline.
Record later changes in a separate stage record. Follow [the post-change procedure](#review-completed-code-changes).
Keep the intake, current stage record, and a short evidence index prominent. Apply the priorities below to supporting files.
Keep necessary later plans inside the same task when those stages become ready.
Create subdirectories only when an investigation produces artifacts.
Do not copy runtime source or relocate business repositories into a task.

## Lifecycle entry routes

Select the entry route from supplied facts and the requested next action.
Record it in the living intake or current stage record.
These route names describe procedure. They add no runtime status or artifact kind.

| Route | Entry evidence | Next control |
| --- | --- | --- |
| Requirements first | Requested behavior and available intent sources | Refine intent and ACs. Assess readiness for the named implementation or review stage. |
| Existing implementation | Code, a PR, tests, or an implemented correction supplied before complete requirements | Register actual source identities. Reconcile proposed intent before business verification or acceptance. |
| Bounded exploration | A question or goal that needs an experiment before complete product ACs | Assess `READY` for a defined experiment using the boundaries below. Return findings to intake. |

Existing code does not require retrospective permission to exist.
Its presence does not authorize further edits, establish intended behavior, or supply prior business approval.
Create missing intake at the actual registration date. Preserve existing frozen intake and historical evidence bytes.
Document numbers support navigation. They do not require a fictional sequence of completed stages.

### Enter with existing implementation

1. Record the original request, available intent sources, implementation dates, and remaining historical unknowns.
2. Identify repository IDs, exact base and head revisions, local changes, and relevant source hashes.
3. Inspect code, affected consumers, test assertions, and retained results as intake evidence within existing authorization.
4. Investigate applicable knowledge and prior decisions. Draft missing requirements and measurable Gherkin ACs from supported sources.
5. Mark code-derived and test-derived expectations as proposed until intent evidence and applicable review support them.
6. Compare intended, old, and new behavior. Record unavailable baselines and unresolved policy explicitly.
7. Reconcile missing, contradictory, additional unsupported, and unknown behavior before the affected acceptance decision.
8. Assess `READY` for each named downstream stage from its required evidence and existing authorization.

Do not create ACs solely to reproduce implementation or obtain passing tests.
Correct mismatched code or record an authorized, versioned intent change with its supporting evidence.
Retain the three [coverage mappings](#coverage-output), including relevant unchanged implementation and unknown inventories.
Source and diff inspection can collect intake evidence before formal downstream review becomes ready.
Keep [completed change review](#review-completed-code-changes) separate from initial investigation and its frozen baseline.

### Start bounded exploration

Use this route when a scoped experiment can resolve uncertainty before complete product ACs exist.
Record the following evidence before coding starts:

| Boundary | Required record |
| --- | --- |
| Goal | The question, observable experiment outcome, and source of the requested investigation. |
| Scope | Selected repository revisions, affected components, permitted edits, constraints, and excluded actions. |
| Authority | Existing authorization source and scope; accountable owner or an explicit unresolved ownership blocker. |
| Evidence | Required observations, assertions, fixtures, environment, and material limitations. |
| Stop condition | A measurable completion or stopping condition and the action when that condition occurs. |
| Disposition | How to retain, revise, or discard experimental changes and return findings to intake. |

Use `READY` only when no material unknown can change the experiment's permitted actions or decision.
Explain why unresolved product rules cannot change that bounded decision.
`READY_WITH_LIMITS` still permits intake evidence collection only. It does not permit exploration coding.
Use `NEEDS_CLARIFICATION` when missing authorization, ownership, constraints, or intent blocks the proposed experiment.
Continue independent authorized investigation while the dependent coding action remains blocked.

Full product ACs can remain incomplete during this stage.
Define concrete experimental assertions without presenting fixture values as business rules.
Keep the intake living while initial investigation remains incomplete. Record the exploration decision and retained results there.
An explicit intake freeze still applies. Use the current stage record when a frozen baseline exists.
Reassess scope before extending the experiment. Exploration readiness does not authorize unrestricted feature implementation, acceptance, or deployment.
Experimental code can enter reconciliation as a candidate implementation.
Product acceptance requires assessed intent, conformance, and applicable verification evidence.

### Keep independent lifecycle facts

Record these facts separately in the current task view:

| Fact | Required distinction |
| --- | --- |
| Implementation | Proposed or present, with exact source identity and actual dates or explicit unknowns. |
| Intent | Sourced or proposed behavior, AC definition version, unresolved rules, and actual review state. |
| Execution | Inspected assertions and retained outcomes, with matching code, test, fixture, and environment identities. |
| Acceptance | Actual business disposition and its authority, or pending when no decision exists. |
| Next stage | Named phase, readiness, assessor, time, rationale, evidence limits, blocked actions, owner, and next action. |

Passing tests cannot approve inferred intent. Implemented code cannot establish acceptance or deployment authorization.
Reuse earlier executions only when inspected assertions and recorded conditions support the current predicates.
Rerun affected cases when relevant source, assertions, fixtures, configuration, or expected predicates change.
Retain human review, knowledge publication, verified execution, and deployment authorization as separate decisions.

## Document order

Name each current task document `NN-purpose[-scope].md`.
Use two digits, lowercase words, and hyphens. Choose the prefix from the main lifecycle purpose below.
Use a scope suffix only when a separately retained scope has its own current consumer and evidence.
Do not add a date for each update. Use a date only when separately retained scopes need disambiguation.
Keep the filename stable during updates. The prefix supports navigation, not freshness, approval, or passing execution.
Feedback can return work to an earlier stage without renaming its document.

| Prefix | Lifecycle stage | Example purpose |
| --- | --- | --- |
| `01` | Receive | `01-intake.md` |
| `02` | Discover | `02-discovery.md` |
| `03` | Understand | `03-system-understanding.md` |
| `04` | Relate | `04-relationships.md` |
| `05` | Analyze | `05-impact-analysis.md`, `05-refinement.md` |
| `06` | Implement | `06-implementation.md`, `06-test-cases.md` |
| `07` | Review | `07-code-review.md` |
| `08` | Execute cases | `08-test-execution-report.md` |
| `09` | Compare evidence | `09-coverage.md`, `09-verification.md` |
| `10` | Scoped handoff | `10-change-review.md`, `10-release-readiness.md`, `10-issue-catalog.md` |

Use one current document per purpose and scope. Update it instead of adding another report for each round.
Separate scopes only when they have distinct consumers, decisions, or retained evidence.
Use `06-test-cases.md` for canonical cases, including cases first defined during refinement.
Use the [authoring catalog](../core/knowledge/templates/sdlc/README.md#task-document-selection) to select the matching template.
Create only documents that support current work. The table does not require ten documents.
Keep `evidence/index.md`, raw evidence filenames, source identities, and immutable audit filenames stable.

Apply the naming convention to new documents. Rename an existing document only when its relocation is authorized.
Preserve its bytes for a rename. Record the old and new paths, SHA-256, and pre-rename Git revision in a task manifest.
Use `null` for an unavailable prior revision and identify unrecoverable untracked material.
Repair active links and validate retained hashes. Preserve frozen documents and registered evidence identities.
Record authorized deletions and historical locator recovery under [evidence priorities and cleanup](#evidence-priorities-and-cleanup).
Keep an old compatibility link only when a current consumer requires it. Do not retain redundant aliases for retired reports.
Frozen historical references can resolve through the cleanup record and retained Git revision.
Generated workspaces contain this guide without project task files or compatibility links.

## Standard task document content

Use the selected artifact template and its exact required level-two headings.
Do not substitute generic headings for a kind-specific schema or require unrelated sections.
Arrange a new current document in this order:

1. Use the template's YAML envelope, including its actual `artifact_kind`, ID, owner, source references, and review fields.
2. Give the document one descriptive title. Place the [critical conclusions](#critical-conclusions-in-task-documents) callout immediately after it.
3. Complete the selected kind's required sections. Add concise scope-specific subsections only when useful.
4. Separate intended behavior, implementation state, execution results, acceptance, publication, and authorization.
5. Link each material claim to its source, exact revision, assertions, or retained execution as applicable.
6. Record findings with evidence, consequence, owner, and next action. Mark unknown owners and unresolved limits explicitly.
7. Record automated checks separately from the pending or completed ASD writing review.

Harness maintenance notes can remain ordinary Markdown when no authoring form applies.
Keep their scope, source identities, performed checks, and writing-review metadata explicit.
Review these notes manually. Do not assign an unrelated artifact kind to make lint pass.

Keep business meaning and supporting evidence in the owning current document or canonical case definition.
Link supporting evidence rather than copying its raw contents or repeating a report's narrative.
Preserve frozen records, registered snapshots, and immutable audit history. Do not rewrite them to match the current format.
Use the [reference rules](#link-task-definitions-and-evidence) and [coverage procedure](#coverage-output) for traceability.

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

## Canonical Gherkin test cases

Apply this rule whenever requirement refinement, defect refinement, or code-change verification defines or revises test cases.
Always write readable Gherkin steps with explicit assertions. Case names, keyword calls, and script links alone are insufficient.
Cover the applicable positive, negative, boundary, failure, and recovery conditions. Explain material exclusions.

### Keep one definition source

Save all current human-readable case definitions for one task in `tasks/<task-id>/06-test-cases.md`.
Update this catalog across refinement, implementation review, and verification. Do not create separate extended or phase-specific definition files.
Create it when the first case is defined. Give each case a stable ID and heading, such as `## TC-001`.
Keep the ID heading stable when the case title changes.
Record definition versions and relevant requirement, implementation, test, and fixture revisions or hashes.
Preserve superseded definitions through exact Git revisions or immutable snapshots when retained evidence depends on them.

Link each case ID to its canonical heading from intake, plans, findings, gap comparisons, reports, and evidence indexes.
Link executable tests or their mapping records back to the same case definition.
Keep detailed steps and expected assertions in the catalog. Consumers can summarize outcomes and link details.
Requirements retain their authoritative acceptance criteria. Cases link each criterion separately instead of redefining its business meaning.
Keep executable assertions and retained execution results in their owning locations. Link them separately from the case definition.
Preserve frozen records and historical evidence. Add current navigation without rewriting their bytes.

### Define clear steps and assertions

Use the [test case](../core/knowledge/templates/sdlc/test-case.md) and [BDD feature](../core/knowledge/templates/sdlc/bdd-feature.md) fields where applicable.
Use existing artifact contracts when declared. This rule adds no schema, execution grant, or automatic runtime gate.
Each case must contain these details:

| Detail | Required content |
| --- | --- |
| Identity and purpose | Stable case ID, clear title, definition version, test level, and exact requirement or defect links. |
| Terms and entities | Named actor and role, permissions, entity identifiers, interfaces, data fields, and relevant states. |
| Setup | Initial state, concrete test data, dependencies, environment, isolation, and cleanup. Identify controlled operations and substitutions. |
| Gherkin | Complete `Given`, `When`, and `Then` steps in execution order. Use `And` or `But` only with a clear preceding step type. |
| Assertions | Each `Then` states an observable value, state, count, response, or error. Include units and timing limits when required. |
| Assertion mapping | Map each expected assertion to its criterion and inspected executable assertion, or mark its implementation unavailable. |
| Results and evidence | Link separate actual results, exact revisions, screenshots, logs, and material limits. Keep unexecuted results `NOT_RUN` or null. |

`Given` names the actor, relevant entity, and initial conditions.
`When` states one concrete action. Keep later actions in separate ordered steps.
`Then` names the observed entity, observation point, comparison, and expected value.
Separate additional assertions into distinct `Then` or `And` steps.
Use `Scenario Outline` with concrete `Examples` when data variations share the same behavior.

Define domain terms and custom step keywords in the case or a linked glossary.
Use the same term for the same entity throughout the case.
Specify exact UI labels, service operations, or data fields when those identities affect reproduction.
For UI E2E cases, follow [gherkin-quality](../.agents/skills/gherkin-quality/SKILL.md) for component types, identities, scopes, and supported assertions.
Keep business behavior separate from UI actions. Mark unavailable component evidence or automation bindings as unverified.
Distinguish similar entities, such as an access token and a refresh token.
Define the timing origin, end condition, units, and real or controlled clock when timing affects the result.
Replace vague outcomes, such as "works correctly" or "is successful", with explicit observations.
Do not leave pronouns, unnamed users, generic "tokens", or undefined keywords with several possible meanings.

Keep setup and numbered action steps in the same case section when needed for manual reproduction or gap comparison.
Map these steps to the Gherkin sequence. They are a reading aid, not a second independent definition.
For gap analysis, link the same case from the [old/new comparison](#compare-behavior-for-gap-analysis).
Keep intended assertions separate from old and new actual results.

Do not invent policies, expected values, permissions, status codes, or timing thresholds to complete a scenario.
Mark missing intent as unresolved. State its source gap, consequence, owner, and next action.
Use `unknown` for an unavailable owner. Keep acceptance blocked for the affected assertion until its expectation is resolved.
Observation cases can record facts without claiming business acceptance.

Review definitions before verification handoff for complete Gherkin, explicit assertions, clear terms, stable links, and one canonical source.
Inspect executable assertions and matching execution evidence before claiming that a defined behavior passed.
Follow [case evidence checkpoints](#save-case-evidence-and-resume-checkpoints) as each executed case completes.

## Coverage output

Use the [three coverage views](../docs/BEHAVIOR_REVIEW.md#coverage-output-for-requirements-and-defects) in requirement and defect verification reports.
Display AC-to-test, AC-to-code-change, and code-change-to-test matrices for exact source revisions.
Include unmapped ACs and changed behaviors. Identify unchanged required paths and supporting maintenance separately.
Link every AC, case, change, assertion, and result to its exact definition or evidence.
Keep definition coverage, inspected assertions, implementation conformance, and passing execution separate.
Report missing, contradictory, unsupported additional, and unresolved behavior explicitly.
The target `TC >= AC = Code Change` compares behavior scope, not artifact counts.
Use the [shared template](../core/knowledge/templates/sdlc/traceability-record.md) and [coverage procedure](../.agents/skills/verify-implementation/references/behavior-review.md#report-coverage).
Retain earlier phase reports when their exact bytes support historical results.

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

### Investigate before asking

Investigate each material question before presenting it to the user.
Inspect prior user answers, relevant knowledge, original sources, registered code, test assertions, and retained investigations within authorized access.
Use available configured tools when they can resolve the question. Read exact sources before relying on retrieved summaries.
Answer the parts that evidence resolves. Keep remaining uncertainty scoped to the named next decision.

Do not ask the user to perform source inspections the agent can complete.

For each investigated answer, record a confidence level, rationale, source links, exact revisions or hashes, and material limits.
Use the evidence class appropriate to the claim. Code can establish implementation without establishing approved policy or deployed behavior.
Confidence concerns the stated answer and scope. It does not supply review, publication approval, or passing execution.

| Confidence | Evidence basis |
| --- | --- |
| `HIGH` | Direct, applicable evidence supports the answer without an unresolved material conflict within its stated scope. |
| `MEDIUM` | Evidence supports a bounded answer with stated assumptions or incomplete scope. |
| `LOW` | Evidence is weak, stale, conflicting, or indirectly relevant to the required answer. |
| `UNKNOWN` | Available evidence cannot support an answer. |

Confidence must follow evidence. These qualitative levels are not measured probabilities.
Do not raise confidence to avoid an unresolved question. Do not ask automatically because confidence is below `HIGH`.
Keep a supported answer when its limits cannot change the selected scope or next decision.
Do not infer missing business policy from implementation behavior.

Ask only when further feasible, authorized investigation cannot resolve material uncertainty that can change the next decision.
An irrelevant uncertainty does not justify a user question.
For each remaining question, record the investigation scope, provisional answer if available, confidence, sources, and unresolved gap.
State its decision consequence, resolution owner or `unknown`, and the exact answer or evidence needed.
If evidence conflicts, identify the competing sources and their applicability limits.

Keep confident findings separate from unanswered questions in the same living review document.
Preserve user answers and leave proposed business choices unselected. Do not overwrite user answer fields with agent inferences.
Required human review remains separate from clarification.

### Document-based knowledge review

Use one living answer document for each related knowledge review scope.
Save each user input verbatim with its source and date before investigation or delegation.
Treat it as a high-priority reference. The latest explicit clarification controls intended behavior within its stated scope.
Link the saved input from the living document. Preserve conflicting sources and earlier answers.
Start each topic with a short narrative. Place its questions beside the relevant explanation.
Give each question suggested choices and an editable `Answer:` field.
Label choices as proposals. Leave them unselected until the user supplies an answer.
Permit another answer, `unknown`, or a named contact. Keep existing answers and question IDs.
Apply the [investigation and confidence rules](#investigate-before-asking) before handing over questions.

Hand over the editable document. The user can complete it asynchronously.
Resume ingestion when the user returns answers and requests continuation.
Preserve the returned bytes before review. Apply completed clarifications through the procedure below.
Keep unanswered questions open. A continuation request does not supply business answers or publication approval.

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
For session timing, follow the [timing and deployment checks](../.agents/skills/verify-implementation/references/browser-investigation.md#verify-timing-inputs-and-deployment-settings).
Trace the full expiry path, including unchanged configuration. Keep effective settings, local scheduling, and lifecycle outcomes separately evidenced.
Shortened local lifetimes cannot establish deployed policy or configuration parity.
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

## Compare behavior for gap analysis

Always compare old behavior with new behavior when analyzing gaps between requirements and implementation.
Apply the shared [comparison and case procedure](../.agents/skills/verify-implementation/references/behavior-review.md#compare-old-and-new-behavior).
Keep the required outcome, old actual result, and new actual result separate.
Use exact revisions and equivalent conditions. Record necessary differences and unavailable baselines explicitly.

Describe each case with ASD-STE100 setup and numbered steps. Give each step one action.
State observable required, old, and new results separately.
Link the requirement, inspected assertions, and retained old and new evidence separately.
Distinguish executed results from source predictions and proposed behavior.
Classify introduced, worsened, unchanged existing, and corrected failures. Use `unknown` when comparison evidence is insufficient.
Explain any lower release importance for an unchanged failure. This classification does not waive an unmet requirement.

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
| Necessary | Initial `01-intake.md`, current stage record when needed, and a short `evidence/index.md` | Main entry points |
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
For [bounded exploration](#start-bounded-exploration), assess its recorded boundaries while keeping incomplete product intake open.
Use the checklist below before product implementation, formal change review, or business verification.
Apply each item to the named scope. Explain any limit that cannot change that stage's decision.
Check the following points before leaving intake:

- The problem or requested behavior, affected actors, scope, and business impact are clear.
- Expected behavior has a source. Current behavior has evidence or an explicit, justified applicability limit.
- Acceptance criteria identify conditions, actions, observable results, and required limits.
- Material hypotheses, contradictions, dependencies, and suspicious conditions have supporting analysis.
- Necessary source inspection, assertions, and investigations have retained evidence.
- Completed knowledge clarifications have updated records, traceable sources, and the required audit and review state.
- No unresolved material question can change the proposed next-stage decision.

Record the decision inside `01-intake.md`:

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
Incomplete exploration drafts can lack full product ACs. Report their lint errors without inventing missing business values.
Document the exploration decision separately. A draft lint failure supplies no business answer or authorization.
The [document validation skill](../.agents/skills/validate-sdlc-documents/SKILL.md) defines the applicable checks.

## Review completed code changes

This procedure also applies when implementation existed before Workbench intake.
Complete the applicable [entry investigation](#enter-with-existing-implementation) before formal downstream review.
Register missing intake truthfully. Never imply that a later requirement or approval preceded the original implementation.
Freeze `01-intake.md` after its issue definition and investigation finish.
Do not add change progress, review findings, or execution results to that baseline.
Record its exact Git revision and SHA-256 in `10-change-review.md` or an equivalent identified stage record.
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

Use actual end-to-end verification when it can confirm a review issue's reachable trigger and tangible impact.
Use existing tests or focused authorized probes. Compare baseline and candidate when claiming a regression.
Assert both the failure and its observable user or system consequence.
Bind results to exact source, assertions, environment, and configuration. Retain applicable screenshots and request or state evidence.
Disclose synthetic data, substituted services, and controlled clocks. Save each completed case before further execution or waits.
Keep failed reproduction and unavailable environments explicit. Controlled results do not establish production reachability, frequency, or impact.
The [code review verification rule](../AGENTS.md#code-review-verification) preserves the user source and authorization boundary.

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
