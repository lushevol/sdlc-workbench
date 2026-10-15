# SDLC authoring catalog

This catalog supplies reusable authoring templates and illustrative samples.
Its current consumer is the user who requested the SDLC catalog.
Its benefit is a consistent starting point for AI-assisted engineering documents.
Each guide contains instructions, a copyable template, a sample, and completion checks.

## AI authoring contract

1. Select the artifact that answers the current engineering question.
2. Read its instructions and the relevant source revisions.
3. Copy only its Template block into the chosen document location.
4. Replace every `{{placeholder}}` with supported content.
5. Keep required sections. Mark an irrelevant section `not applicable` and give a reason.
6. Use `unknown` for a missing owner. Use null for unavailable structured values.
7. Record facts, inferences, and unresolved questions separately.
8. Give each finding evidence, a consequence, an owner, and a next action.
9. Keep reviewer identities and review dates empty until an actual review occurs.
10. Check the completed artifact against its completion checks.

Do not copy sample business rules, identities, thresholds, dates, or results into real artifacts without supporting evidence.
Keep identifiers stable across related documents.
Keep repository, service, capability, contract, source, and tool identities separate.
Read source contents before treating them as intent.
Use exact source revisions for code evidence.

Catalog declarations do not establish runtime relationships or execution permission.

## Common authoring fields

The Template blocks use this authoring envelope:

```yaml
artifact_kind: "{{catalog_slug}}"
id: "{{stable_artifact_id}}"
version: 1
status: draft
owner: unknown
source_refs: []
related_ids: []
review:
  state: pending
  reviewer: null
  reviewed_at: null
writing_review:
  standard: ASD-STE100
  automated_check: NOT_RUN
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
    - Automated checks do not check the complete approved dictionary or grammar rules.
```

`artifact_kind` selects an authoring form. It is not a Workbench knowledge `type`.
`status` describes document maturity. Keep execution and review results in separate fields.

`source_refs` lists source IDs. Resolve each ID through a source table or the owning source catalog.
Each source record needs a locator, exact revision, available hash, owner, and authority assessment.
Mark missing source details explicitly. Do not invent a revision or hash.

`related_ids` identifies referenced artifacts. Explain each relationship in the document body.
Business review and writing review have separate purposes.
Set each check status from checks actually performed.
Only a complete writing review can set `asd_review: PASSED`.

## Workbench storage and validation

These guides remain under `knowledge/templates/` and ship with initialized workspaces.
Templates and samples remain excluded from knowledge record validation.
Author completed business documents in the owning project's document location.
Keep existing authoritative assets at their original locations.
Register those documents as sources when Workbench needs their context.

Use the [supported knowledge templates](../README.md) when creating governed Workbench records.
Those templates define `Requirement`, `Architecture`, `Decision`, `RepositoryProfile`, `KnowledgeTopic`, and `GovernanceFinding`.
Transfer relevant authored content into the matching supported record.
Use `KnowledgeTopic` when no specialized knowledge type applies.
Use the [knowledge contract](../../README.md) for mandatory fields and provenance.
The authoring envelope alone does not satisfy that contract.

Requirements need structured `acceptance_criteria` and matching readable Gherkin.
Important requirements and decisions need recorded human review before publication.
Record each real governance change in a new audit event file.
Preserve earlier source snapshots, candidates, findings, and audit events.
Knowledge review does not establish passing business execution.
Inspect actual assertions and retained execution before claiming verified behavior.

## Sample rules

Read [the illustrative context](sample-context.md) before using a sample.
All samples use a fictional invoice portal and remain drafts.
`SAMPLE-SRC-001` refers only to that context at the illustrative revision `sample-v1`.
This source label is not a registered raw manifest entry.
Sample links and references establish navigation within this library only.
No sample records a real reviewer, approved business rule, deployed system, or passing execution.

## Catalog

The catalog contains 37 authoring guides.

| Phase | Template and sample | Main content |
| --- | --- | --- |
| Planning | [Project charter / product brief](project-charter.md) | Problem, scope, objectives, success measures. |
| Planning | [Delivery plan](delivery-plan.md) | Milestones, dependencies, responsibility, completion conditions. |
| Planning | [Risk and issue register](risk-issue-register.md) | Evidence, consequence, owner, mitigation. |
| Requirements | [Business / product requirements](business-product-requirements.md) | Business needs, capabilities, detailed requirement references. |
| Requirements | [Requirement / user story](requirement.md) | Description, rationale, measurable BDD acceptance criteria. |
| Requirements | [Feature / epic brief](feature-epic.md) | Outcome, scope, related requirements. |
| Requirements | [Business rule specification](business-rule.md) | Conditions, permissions, exceptions, rule examples. |
| Requirements | [Domain glossary](domain-glossary.md) | Terms, definitions, relationships, sources. |
| Requirements | [Nonfunctional requirement](nonfunctional-requirement.md) | Quality target, measurement conditions, Gherkin. |
| Requirements | [Use case / user journey](use-case.md) | Actors, preconditions, normal and alternative flows. |
| Requirements | [Change request](change-request.md) | Proposed change, impact, risks, review. |
| Design | [System architecture / technical design](system-design.md) | Components, interfaces, dependencies, constraints. |
| Design | [Architecture decision record](architecture-decision.md) | Context, options, proposed decision, consequences. |
| Design | [API / event / integration contract](interface-contract.md) | Inputs, outputs, authentication, errors, compatibility. |
| Design | [Data design / migration plan](data-design-migration.md) | Data model, mapping, checks, recovery. |
| Design | [UX and accessibility specification](ux-accessibility.md) | Flows, states, interactions, accessibility criteria. |
| Design | [Threat model / security review](threat-model.md) | Assets, threats, privacy, controls, evidence gaps. |
| Development | [Repository profile](repository-profile.md) | Responsibilities, exact revisions, entry points, validation. |
| Development | [Implementation plan](implementation-plan.md) | Affected scope, tasks, risks, checks. |
| Development | [Pull request / code review](pull-request-review.md) | Problem, change, evidence, risks, findings. |
| Testing | [Test strategy / test plan](test-strategy-plan.md) | Scope, levels, environments, completion criteria. |
| Testing | [BDD feature specification](bdd-feature.md) | Rules, tagged scenarios, measurable outcomes. |
| Testing | [Test case](test-case.md) | Inputs, actions, assertions, requirement links. |
| Testing | [Test data / environment specification](test-data-environment.md) | Data setup, configuration, isolation, cleanup. |
| Testing | [Test execution / verification report](test-execution-report.md) | Revision, assertions, actual results, retained evidence. |
| Testing | [Defect report](defect-report.md) | Reproduction, expected and actual behavior, evidence. |
| Testing | [Requirements traceability record](traceability-record.md) | Requirement, code, assertion, execution, coverage limits. |
| Acceptance | [User acceptance record](user-acceptance.md) | Scope, evidence, exceptions, actual acceptance decision. |
| Release | [Release readiness assessment](release-readiness.md) | Required checks, defects, risks, actual approvals. |
| Release | [Deployment / rollback plan](deployment-rollback.md) | Preconditions, steps, checks, rollback triggers. |
| Release | [Release notes](release-notes.md) | Features, fixes, compatibility, known issues. |
| Operations | [Operational runbook](operational-runbook.md) | Objectives, alerts, diagnosis, recovery, escalation. |
| Operations | [Incident report / postmortem](incident-postmortem.md) | Impact, timeline, causes, corrective actions. |
| Operations | [Retirement / decommission plan](retirement-plan.md) | Consumers, data obligations, removal, recovery. |
| Governance | [Knowledge topic / source assessment](knowledge-source-assessment.md) | Claims, provenance, authority, freshness, open questions. |
| Governance | [Governance finding](governance-finding.md) | Subject, evidence, consequence, resolution action. |
| Governance | [Governance audit event](audit-event.md) | Actual transition, actor, final hash, immutable history. |

## Selection and handoff

Start with the requirement guide for a requested behavior.
Use the feature guide to group requirements and the business overview to explain their value.
Link design choices through architecture decisions and interface contracts.
Link each acceptance criterion to a test assertion and retained execution result.
Use release and operational forms only when their current scope needs them.

For a small change, select only the forms that support an observable engineering outcome.
The catalog does not require one document for every form.
Keep common business rules in one identified source and reference them from related artifacts.

## Suggested AI request

```text
Read the SDLC authoring contract and select the requirement template.
Use the supplied source revisions to create a draft for the requested behavior.
Keep the required sections and replace every placeholder.
Write measurable Gherkin criteria and matching structured acceptance fields.
Separate proposed intent, implementation evidence, and execution results.
List unresolved questions with evidence, consequences, owners, and next actions.
Do not invent business limits, source authority, review identities, or passing results.
Check the draft against the template completion checks.
```
