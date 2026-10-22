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

Start with the recommendation, confidence, scope, and controlling reason.
For task documents, add the required bold critical-conclusion callout near the top.
Name the required action, consequence, owner, and linked evidence.
If applicable, state `No critical conclusions require user attention or action.`
Follow the [task document rules](../../../../tasks/README.md#critical-conclusions-in-task-documents).
Keep facts, inferences, unresolved policy, and unavailable evidence distinct.

| Template section | Assessment content |
| --- | --- |
| Release scope | Candidate inventory, base/head identities, artifact provenance, behavior versions, target PROD, configuration, policy, exclusions, and time. |
| Readiness conditions | Per-dimension status, sourced conditions, applicability, actual evidence, confidence limits, owners, and next actions. |
| Execution evidence | Coverage inventories and fractions, inspected predicates, matching runs, failures, skips, retries, and environment limits. |
| Risks and exceptions | Consequence, exposure, mitigation evidence, actual disposition, authority, scope, and validity limits. |
| Readiness conclusion and authorization | Separate assistant assessment from actual readiness decisions and deployment authorization. |
| Facts, inferences, and unresolved questions | Claim classes, missing rules, unresolved identities, and the single living question document. |
| Findings | Linked evidence, consequence, owner, next action, and closure evidence for each finding. |
| Sources | Exact policy, requirement, source, assertion, result, artifact, environment, and decision locators with versions or hashes. |

Add a small assistant assessment block under `Readiness conclusion and authorization`.
Use the following field names with actual values:

```yaml
assistant_assessment:
  assessment_state: PROVISIONAL
  evidence_confidence: UNDETERMINED
  production_recommendation: INSUFFICIENT_EVIDENCE
  scope_basis: null
  controlling_evidence_refs: []
  blocking_action_refs: []
  residual_risk_refs: []
  reassess_when: []
```

Use `COMPLETE` only after completing the scoped assessment and its required intake gate.
A complete assessment can still recommend stopping or collecting more evidence.
Replace nulls and empty lists where actual evidence exists. Explain unavailable values.
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
