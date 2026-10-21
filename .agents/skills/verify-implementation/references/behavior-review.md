# Review behavior evidence

Use this handoff for story review, change mapping, assertion mapping, behavior tracing, and later evidence checks.
Keep intent review, source inspection, assertion coverage, and execution results separate.

## Procedure homes

Use existing skills for the nine review procedures.
These names identify procedures, not additional skills or runtime commands.

| Procedure | Workbench skill | Handoff section |
| --- | --- | --- |
| `extract-story-behaviors` | `analyze-requirement` | Extract atomic behaviors |
| `map-change-to-behavior` | `impact-analysis` | Map implementation |
| `map-tests-to-behavior` | `verify-implementation` | Map assertions and execution |
| `analyze-requirement-gap` | `analyze-requirement` and `detect-gaps` | Classify gaps |
| `analyze-implementation-gap` | `detect-gaps` | Classify gaps |
| `analyze-test-gap` | `detect-gaps` | Classify gaps |
| `trace-behavior` | `query-knowledge` | Trace one behavior |
| `verify-story-change-test` | `verify-implementation` | Coordinate a review |
| `continuous-sdlc-check` | `verify-implementation` | Check later changes |

## Keep one evidence handoff

Start from the [requirement template](../../../../core/knowledge/templates/sdlc/requirement.md) when intent needs an authored requirement.
Use the [traceability template](../../../../core/knowledge/templates/sdlc/traceability-record.md) for the shared review record.
These are authoring artifacts, not published knowledge or executable assurance baselines.
Use [knowledge governance](../../../../knowledge/README.md) for authorized candidate creation, review, and publication.

Keep the template headings and metadata.
Add behavior IDs, versions, grades, and evidence limits to the relevant tables.
Use separate rows for many-to-many relationships.
Do not invent code, test, assertion, execution, or review records before evidence exists.

| Identity or record | Required detail |
| --- | --- |
| Scope | Story/source identity, included behaviors, excluded boundaries, exact repository refs, environment, and required verification levels. |
| Behavior | Stable story-qualified ID, version, criterion IDs, actor, conditions, trigger, action, outcomes, and applicable negative cases. |
| Intent | Exact source ID, revision, locator, available hash, explicit or inferred origin, authority, and recorded review state. |
| Implementation | Repository ID, exact revision, file hash, path, symbol or line range, and changed or unchanged path. |
| Assertion | Stable test ID, assertion ID, exact test revision/hash, setup, invocation, predicate, helper chain, and boundaries. |
| Relationship | Both endpoint identities and versions, supporting source locator, evidence class, grade, and limitations. |
| Execution | Original result/action ID, tested revisions/hashes, assertion IDs, inputs, configuration, environment, mode, and retained output. |
| Finding | Stable finding ID, affected behavior/version, category, evidence, consequence, owner, next action, and resolution evidence. |

Use an ID such as `STORY-104:BEH-01` within its source-qualified story scope.
Keep existing criterion IDs distinct and link them to behavior IDs.
Preserve behavior IDs when unchanged behavior moves or its display order changes.
Increment the behavior version when its predicate or relevant intent dependency changes.
Record split, replacement, and retirement relationships instead of silently reusing an old identity.

Retain each saved phase as a new traceability artifact with a unique artifact ID.
Record its predecessor in `related_ids` and link the retained earlier file.
Preserve earlier snapshots, findings, and execution results.
Do not carry an approval onto changed intent or reconstruct a run's original bindings from later records.

Use these relationship grades alongside the evidence class:

| Grade | Meaning |
| --- | --- |
| `CONFIRMED` | Inspected exact evidence supports the stated relationship within its limits. |
| `LIKELY` | Consistent indirect evidence leaves a material link missing. |
| `POSSIBLE` | A semantic match needs inspection. |
| `UNRESOLVED` | Evidence is missing, stale, conflicting, or ambiguous. |

A confirmed declaration does not establish an implemented or executed behavior.
An inferred business rule does not become approved intent through a relationship grade.

## Extract atomic behaviors

1. Read the exact story, criteria, linked decisions, and authoritative sources.
2. Identify actors, triggers, preconditions, permissions, actions, outcomes, side effects, failures, and invariants.
3. Split compound rules into predicates that can be traced and tested independently.
4. Preserve source terminology and distinguish explicit rules from inferred scenarios.
5. Inspect negative, boundary, permission, persistence, integration, and regression-preservation cases within the requested scope.
6. Write measurable Gherkin with conditions, an action, an observable result, and any required limit.
7. Record missing thresholds and ambiguous rules as owner decisions; do not invent them.

Keep readable Gherkin and structured criteria consistent when creating a requirement artifact.
Code and tests can establish current behavior while leaving target intent unresolved.

## Map implementation

1. Identify each repository and its exact base/head revisions independently.
2. Inspect changed files, symbols, contracts, schemas, queries, events, configuration, and dependencies.
3. Inspect relevant unchanged paths, callers, importers, and consumers before declaring implementation absent.
4. Map each meaningful change to behaviors or a supported maintenance rationale.
5. Record direct source locations and distinguish implementation links from change links.
6. Inspect API, event, persistence, and upstream/downstream boundaries affected by the change.
7. Record unexplained changes and unavailable boundaries without turning missing mappings into demonstrated defects.

Use configured graph operations to discover candidates when available.
Check graph coverage and freshness; inspect exact source before confirming a link.
Use direct inspection when no usable graph or index exists.

## Map assertions and execution

1. Select test repositories and suites through the registry and requested verification scope.
2. Inspect existing cases and changed tests; search suites directly when catalogs omit cases.
3. Follow fixture setup, imported helpers, Robot keywords, invocation, and concrete assertions.
4. Map each assertion to the exact behavior predicate and implementation path it checks.
5. Record test level, actual services, simulated backends, mocks, omitted boundaries, and required verification level.
6. Inspect retained execution or run authorized configured operations when the necessary environment exists.
7. Bind each result to its original assertions, exact code/test bytes, configuration, inputs, environment, and execution mode.

Use the [assertion worksheet](../../ingest-knowledge/references/evidence.md#assertion-and-execution-worksheet) for the complete chain.
Report scenario coverage, inspected assertion coverage, and execution separately.
Unit coverage cannot close a required integration or system gap.
A mocked path cannot establish actual execution of the omitted dependency.
Keep stale, failed, simulated, unavailable, and unrun results visible beside their limits.

## Classify gaps

| Category | Required distinction |
| --- | --- |
| Requirement | Missing scenarios, ambiguous conditions, conflicts, untestable outcomes, or unresolved owner decisions. |
| Implementation | Inspected source contradicts an applicable requirement or omits a demonstrated required path. |
| Traceability | A relationship lacks adequate evidence; implementation absence remains unproven. |
| Assertion coverage | A scenario is missing, an assertion is weak, or the test omits the required path or boundary. |
| Execution | Required assertions were not run, failed, used stale bytes, or executed at an insufficient level. |

Check permissions, negative outcomes, side effects, integration boundaries, and preservation of affected existing behavior.
Distinguish unsuccessful bounded searches from demonstrated absence.
State evidence limits with each finding.
Use `unknown` for unavailable owners.
Closing a finding requires resolution evidence; deleting its row does not establish resolution.

### Compare old and new behavior

Always compare old and new behavior for requirement-to-implementation gaps, including proposed changes without an implementation.
Record the old revision, new revision or proposal, requirement version, environment, and evidence limits.
Keep these three results separate:

| Result | Required detail |
| --- | --- |
| Intended behavior | Required observable result and its exact requirement source. Mark unresolved intent explicitly. |
| Old behavior | Observed baseline result, or an explicit source prediction when execution is unavailable. |
| New behavior | Actual result at the selected candidate, or an explicit prediction when implementation or execution is unavailable. |

Use equivalent conditions, actions, data, timing, and dependency behavior for both versions.
State each necessary difference and its effect on the comparison.
Inspect relevant unchanged paths before attributing a failure to the change.
Use paired execution when available and authorized. Label source-based predictions and unrun cases explicitly.
For a new capability, record evidence of the missing old path or mark its baseline unavailable.
Do not invent old results or treat missing evidence as passing behavior.

| Comparison | Required evidence |
| --- | --- |
| Introduced failure | The old version satisfies the case; the new version fails under equivalent conditions. |
| Worsened existing failure | Both contain a failure, but the change expands its conditions, consequence, or duration. |
| Unchanged existing failure | Both fail the same condition with no demonstrated increase in consequence. |
| Corrected failure | The old version fails; the new version satisfies the required outcome. |
| Unknown | Missing evidence or material setup differences prevent a supported comparison. |

Keep this comparison separate from requirement conformance and the existing gap category.
An unchanged failure can still violate the requested outcome.
Explain any reduction in incremental release importance through the compared conditions and business consequence.
Do not reduce business severity automatically or infer a requirement waiver from a pre-existing failure.

### Describe each gap case

Define test cases under the [canonical Gherkin rules](../../../../tasks/README.md#canonical-gherkin-test-cases).
Link the case from each finding. Keep its steps and intended assertions in the canonical task catalog.

Use ASD-STE100 for the setup, numbered steps, results, consequence, and next action.
Use stable terms. Explain technical terms that the reader needs to follow the case.
Keep one action per step and identify who performs it.
Give enough timing, input, and dependency detail to distinguish the case from similar cases.

Keep these fields in the canonical case or link them from the finding's comparison record:

| Field | Required detail |
| --- | --- |
| Setup | Actor, initial state, permissions, relevant inputs, timing, dependencies, and controlled conditions. |
| Steps | Numbered actions in execution order, with one action per step. |
| Required result | Observable outcome linked to its requirement or an explicit unresolved policy. |
| Old result | Observable baseline outcome linked to its evidence and exact revision. |
| New result | Observable candidate outcome linked to its evidence, or a clearly labelled prediction. |
| Difference | What changed, the comparison classification, and its consequence for the user. |
| Action and limits | Owner, next action, evidence limits, and the reason for any priority change. |

Keep setup actions distinct from user actions. Identify clock changes, held responses, mocks, and direct service calls as controlled operations.
Do not describe a simulated sequence as an executed browser journey.
Preserve earlier evidence and report interpretation changes in the current finding.

## Trace one behavior

Resolve the requested behavior ID and version before following its evidence.
Trace intent and criteria through services, contracts, implementation, assertions, and retained execution.
Show exact source locators, grades, and limits on each relationship.
Show whether a test was located, inspected, or executed.
Keep missing links visible and distinguish a complete static mapping from behavior verification.
Read-only tracing does not authorize new records or execution.

## Coordinate a review

Use the full sequence for an implemented story or PR:

1. Establish scope and extract behaviors with `analyze-requirement`.
2. Analyze requirement gaps with `detect-gaps`.
3. Map code changes and relevant unchanged paths with `impact-analysis`.
4. Analyze implementation and traceability gaps with `detect-gaps`.
5. Map assertions and applicable execution with `verify-implementation`.
6. Analyze assertion and execution gaps with `detect-gaps`.
7. Check the completed handoff and report each behavior's evidence chain and remaining limits.

For a prospective requirement without a diff, stop at applicable requirement and impact analysis.
Mark missing inputs unassessed and continue independent work within scope.
Preserve recorded intent review separately from execution status.
Limit `VERIFIED` claims to approved predicates with matching retained actual execution at the required level.
Unresolved material findings, stale evidence, or missing approval prevent that claim.
Document lint and workspace validation do not compute a complete assurance verdict.

## Report coverage

Declare the included inventories before calculating coverage.
For every metric, show its numerator, denominator, scope, and evidence limit.
Use `N/A` when the denominator is empty or unknown.
Do not infer an inventory from mapped rows alone.

| Direction | Denominator | Numerator |
| --- | --- | --- |
| Story to code | Included active behaviors | Behaviors with confirmed inspected implementation links |
| Story to test | Included active behaviors | Behaviors with confirmed inspected assertion links at the required level |
| Code to story | Included meaningful code changes | Changes linked to a sourced behavior or declared impact |
| Code to test | Included changed implementation paths | Paths reached by inspected applicable assertion chains |
| Test to story | Included test cases | Cases with confirmed links to sourced behaviors |
| Test to code | Included test cases | Cases with confirmed inspected implementation paths |
| Behavior execution | Included active behaviors | Approved predicates with matching passing actual execution and no material unresolved finding |

Count each denominator item once despite many-to-many links.
Report unit, contract, integration, system, and E2E coverage separately when their boundaries differ.
Maintenance rationale explains a change but does not establish story coverage by itself.
Do not reduce intent, mapping, assertion quality, and execution into one pass/fail score.

## Check later changes

Use this procedure on demand after a retained baseline exists.
Scheduling or automatic triggers require separate explicit configuration.
Without a usable earlier record, perform the scoped full review.

1. Read the earlier record and compare exact story, code, test, and contract revisions or hashes.
2. Identify changed artifacts and their affected behaviors, relationships, callers, and transitive boundaries.
3. Reassess affected evidence and invalidate unsupported earlier conclusions.
4. Reuse unchanged evidence only after checking relevant bytes, applicability, configuration, and execution bindings.
5. Save a successor artifact; retain the earlier records and explain new, changed, and resolved gaps.
6. Report requirement, implementation, assertion, contract, and traceability changes with explicit limits.

Changed relevant intent needs renewed review before approval can support a verification claim.
Changed code or assertions require matching execution before reusing a passing result.
Unrelated commits need not invalidate unchanged source bytes.
Finding counts alone do not establish historical assurance improvement or approved resolution.

## Check the handoff

Use the [behavior evidence guide](../../../../docs/BEHAVIOR_REVIEW.md) for the optional narrow JSON baseline and deterministic assurance commands.
These commands check contracts and source freshness; business verification remains `NOT_VERIFIED`.

Use supported Workbench commands with the selected paths:

```sh
ai-sdlc --workspace PATH status
ai-sdlc lint REQUIREMENT.md TRACEABILITY.md
ai-sdlc --workspace PATH validate
ai-sdlc --workspace PATH runs
ai-sdlc --workspace PATH run ACTION_ID
```

Replace placeholder paths and IDs with the actual review inputs.
Lint completed authoring artifacts, not template guides or this reference.
Use [document validation](../../validate-sdlc-documents/SKILL.md) for contract selection and interpretation limits.
Inspect every cited range and compare source hashes manually when no configured operation checks them.
Retain actual commands, results, action IDs, warning counts, and unresolved evidence limits.
Keep automated check results separate from the required ASD writing review in saved reports.
These checks do not authenticate approvals, prove source meaning, or establish business execution.
