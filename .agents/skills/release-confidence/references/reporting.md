# Retain a release confidence assessment

Use the existing [release-readiness template](../../../../core/knowledge/templates/sdlc/release-readiness.md).
Preserve its frontmatter and required level-two headings.
Do not add a new artifact kind or reinterpret its human decision fields.
Follow the [authoring contract](../../../../core/knowledge/templates/sdlc/README.md).

## Location and preservation

For business scope, save the assessment under the owning task.
Use a lifecycle-compatible name such as `10-release-confidence.md` under the [document order](../../../../tasks/README.md#document-order).
Keep supporting results under that task's evidence directory.
Index existing evidence through exact locators, revisions, and hashes instead of copying it.
For a release spanning tasks, name the assessment owner and link all participating task scopes.
Keep one assessment rather than divergent copies.

For harness maintenance, use a relevant `docs/` location without creating business knowledge.
Preserve earlier assessments and raw results.
Save a uniquely identified successor with a predecessor link when evidence changes.
Retain each completed case immediately under the [checkpoint rules](../../../../tasks/README.md#save-case-evidence-and-resume-checkpoints).

## Report content

Start with a short decision view. Aim for 300 words or fewer before supporting detail.
Show the release status, candidate, controlling blockers, and prioritized next actions first.
Label the evidence score `Decision certainty` and place its recommendation beside it.
For example: `Release: NO_GO. Decision certainty: HIGH (100/100 evidence support for the hold).`
Explain the score in one sentence. Never describe it as percent ready or probability of success.
Use a compact metric table with the rule, actual condition status, and evidence strength.
Keep full scorecards, action records, hashes, and repeated machine fields in collapsed or linked detail.
Preserve required headings and evidence fields there. The decision view must stand alone.
For task documents, add the required bold critical-conclusion callout near the top.
Name the required action, consequence, owner, and linked evidence.
If applicable, state `No critical conclusions require user attention or action.`
Follow the [task document rules](../../../../tasks/README.md#critical-conclusions-in-task-documents).
Keep facts, inferences, unresolved policy, and unavailable evidence distinct.
Summarize the largest business consequence and broadest supported system effect near the recommendation.

Show the [mandatory unit-test condition](decision-model.md#mandatory-unit-test-condition) in the decision view and readiness scorecard.
Declare the complete applicable inventory and any exclusions with their evidence-based rationale.
Retain the exact command, source revision, test revision, environment identity, result locator, and execution completion status.
Report total, passed, failed, skipped, runner-level expected-failure, and runner-error counts separately.
Use unavailable values explicitly. A zero or unknown test denominator cannot establish passing unit-test readiness.
Keep legitimate test corrections, genuine application defects, and unresolved execution failures separate.
Preserve original failures and explain any fixture or assertion correction before reporting the matching rerun.

| Template section | Assessment content |
| --- | --- |
| Release scope | Candidate inventory, base/head identities, artifact provenance, behavior versions, target PROD, configuration, policy, exclusions, time, and linked impacts. |
| Readiness conditions | Per-dimension score, status, criticality, sourced conditions, applicability, actual evidence, confidence limits, owners, and next actions. |
| Confidence score and release status | Evidence score, confidence level, technical go/no-go status, `can_go`, score basis, and actions that increase confidence. |
| Execution evidence | Coverage inventories and fractions, inspected predicates, matching runs, failures, skips, retries, and environment limits. |
| Risks and exceptions | Consequence, exposure, mitigation evidence, actual disposition, authority, scope, and validity limits. |
| Readiness conclusion and authorization | Separate assistant assessment from actual readiness decisions and deployment authorization. |
| Facts, inferences, and unresolved questions | Claim classes, missing rules, unresolved identities, and the single living question document. |
| Findings | Linked evidence, consequence, owner, next action, and closure evidence for each finding. |
| Sources | Exact policy, requirement, source, assertion, result, artifact, environment, and decision locators with versions or hashes. |

Under `Release scope`, add separate `Business impact` and `System impact` level-three headings.
Link existing impact records under those headings. Keep one authoritative definition for each effect.
Use the [impact rules](decision-model.md#business-and-system-impact) when the required assessment is missing.

For business impact, identify actors, journeys, benefits, adverse outcomes, exposure, obligations, workarounds, owners, and evidence limits.
For system impact, identify components, consumers, interfaces, state, data, dependencies, effective settings, and failure propagation.
Link each material effect to its applicable condition, canonical case, required verification level, result, mitigation, and owner.
Retain exposure, recovery, and deferral uncertainties beside the conclusions they limit.
Mark inapplicable effects with evidence and a rationale. Do not use empty tables to imply no impact.

Add a small assistant assessment block under `Readiness conclusion and authorization`.
Use the following field names with actual values:

```yaml
assistant_assessment:
  assessment_state: PROVISIONAL
  evidence_confidence_score: 0
  confidence_level: UNDETERMINED
  evidence_confidence: UNDETERMINED
  confidence_score_basis: null
  release_status: BLOCKED
  can_go: false
  production_recommendation: INSUFFICIENT_EVIDENCE
  scope_basis: null
  business_impact_refs: []
  system_impact_refs: []
  controlling_evidence_refs: []
  blocking_action_refs: []
  residual_risk_refs: []
  confidence_increasing_actions: []
  reassess_when: []
```

Use `COMPLETE` only after completing the scoped assessment and its required intake gate.
A complete assessment can still recommend stopping or collecting more evidence.
Replace nulls and empty lists where actual evidence exists. Explain unavailable values.
Use the [confidence score and release status rules](decision-model.md#confidence-score-and-release-status).
Use `confidence_level` as the canonical level field. Keep `evidence_confidence` only as a backward-compatible alias when an existing report uses it.
The report must include a scorecard table with one row per applicable dimension. Each row must include `score` from `0` to `5`, `status`, `critical`, evidence, owner, action, target score/status, expected release-status effect, and closure evidence.
Retain prioritized actions in a table or structured records. Avoid duplicating complete action records in both formats.
Each action needs an ID, priority, owner, current score/status, action, closure evidence, target, expected status effect, and reassessment trigger.
Every score below `100`, every material `FAILED`, `LIMITED`, or `UNKNOWN` row, and every non-`GO` status must have at least one action.
Set `can_go` to `true` only for technical `GO`; keep it `false` for all other technical statuses.
Reassess after closure evidence or an applicable exception. Human authorization alone does not resolve a failed or unknown condition.
Keep the template's `readiness_decision`, `reviewer`, and deployment fields null unless actual decision evidence exists.
Attribute supplied decisions to their actual source. Do not invent actors or audit events.
An assistant recommendation cannot populate human authorization fields.

## Traceable findings

Link each requirement, behavior, case, assertion, execution, and finding ID to its exact definition separately.
Use the [task reference rules](../../../../tasks/README.md#link-task-definitions-and-evidence).
Preserve requirement and test versions through exact revisions or hashes.
Link behavior definitions, test assertions, and retained results separately.
Do not treat an execution log as a substitute for an approved behavior definition.

For each material gap, link one canonical Gherkin case with explicit assertions.
Include setup, numbered steps, and separate intended, old, and new results.
Label source predictions and unavailable comparisons explicitly.
Follow the [behavior comparison](../../verify-implementation/references/behavior-review.md#compare-old-and-new-behavior).
Do not duplicate canonical cases in each report.

## Check and hand off

Check linked local sources and cited ranges. Recheck candidate identity and relevant evidence freshness.
Run applicable existing document checks:

```text
ai-sdlc lint ASSESSMENT.md
ai-sdlc --workspace PATH validate
```

Lint checks the authored artifact contract.
Workspace validation checks separate saved knowledge and registry contracts.
Neither command verifies business execution, approves PROD, or calculates release confidence.
Retain actual commands, outcomes, warning counts, and limits.
Do not rerun business suites merely to complete document linting.

Use ASD-STE100 for human-facing findings and proposed actions.
Keep one main idea per sentence, with at most 20 words per prose sentence.
Keep paragraphs within six sentences.
Preserve exact quotations, code, commands, logs, and identifiers.
Keep automated results separate from the writing review:

```yaml
standard: ASD-STE100
automated_check: NOT_RUN
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```

Set automated status from actual checks. Do not infer full writing compliance from a lint result.
Return the saved assessment link, recommendation, confidence, material blockers, and actual authorization state.
State which evidence or decisions remain necessary, with explicit owners or `unknown`.
