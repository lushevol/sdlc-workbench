# SDLC authoring catalog

This catalog supplies reusable authoring templates and illustrative samples.
Its current consumer is the user who requested the SDLC catalog.
Its benefit is a consistent starting point for AI-assisted engineering documents.
Each guide contains instructions, a copyable template, a sample, and completion checks.

## AI authoring contract

Business intake applies to business behavior requirements and defects in existing repositories.
Harness configuration, upgrades, tooling, and template maintenance require no task or business knowledge record.
Use ordinary project documentation and applicable checks for harness work. Follow [the scope rules](../../../tasks/README.md#scope).

1. Create `tasks/<task-id>/` for a new business issue or requirement. Reuse an existing task when applicable.
2. Select the intake template before discovery. For other artifacts, select the relevant guide. Read its instructions and source revisions.
3. Copy only its Template block. Use `tasks/<task-id>/intake.md` for requirement or issue intake.
4. Replace every `{{placeholder}}` with supported content.
5. Keep required sections. Mark an irrelevant section `not applicable` and give a reason.
6. Use `unknown` for a missing owner. Use null for unavailable structured values.
7. Record facts, inferences, and unresolved questions separately.
8. Give each finding evidence, a consequence, an owner, and a next action.
9. Keep reviewer identities and review dates empty until an actual review occurs.
10. Check the completed artifact against its completion checks.
11. Run the artifact linter. Correct errors and investigate warnings before handoff.
12. After completed material clarification, update affected knowledge and the intake knowledge-update log before handoff.

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
Keep business issue and requirement intake under `tasks/<task-id>/intake.md` at the workspace root.
Follow the [task contract](../../../tasks/README.md) for evidence retention and phase readiness.
Keep new task reports and evidence under that task.
Other authoritative business documents can remain in the owning project's location. Link them from the task when relevant.
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

## Artifact linting

Use the [document validation skill](../../../.agents/skills/validate-sdlc-documents/SKILL.md) to combine automated lint with content review.
Ask: `Use $validate-sdlc-documents to check docs/sdlc for missing fields and measurable Gherkin acceptance criteria.`

Use the installed `ai-sdlc lint` command for completed authoring artifacts.
Copy the selected guide's Template block into a separate Markdown file first.
Keep the YAML frontmatter and required level-two headings.
Replace placeholders with supported values. Use `unknown` owners and null structured values when evidence is unavailable.

```sh
ai-sdlc lint docs/requirements/view-invoice.md
ai-sdlc lint docs/requirements/view-invoice.md docs/design/invoice-service.md
ai-sdlc lint docs/sdlc
ai-sdlc lint docs/sdlc --strict
```

Directory inputs select Markdown files recursively.
Keep completed artifacts in their own directory before using directory inputs.
The catalog guides contain nested Template and Sample blocks; they are not completed artifacts.
Do not pass `knowledge/templates/sdlc/` as the completed artifact directory.
Explicit ordinary documents without artifact frontmatter require correction or a different input selection.

The command reads files without changing their contents, reviews, or execution records.
It returns exit code `0` when the selected checks pass.
It returns exit code `1` when errors exist.
With `--strict`, warnings also produce exit code `1`.
Normal mode permits draft warnings so authors can inspect incomplete evidence explicitly.
Strict mode supports a project handoff gate when the project requires resolved warnings.

| Check class | Examples | Result |
| --- | --- | --- |
| Metadata and schema | Missing fields, unsupported kinds, invalid values, unexpected field structure. | Error |
| Document structure | Missing required sections, repeated headings, empty required sections. | Error |
| Ambiguous identity | Duplicate artifact IDs or duplicate YAML keys. | Error |
| Unfinished content | Unresolved `{{placeholder}}` values. | Error |
| Input safety | Malformed YAML, invalid UTF-8, symlink escapes, input-size limit violations. | Error |
| Gherkin structure | Missing Feature, Scenario, Given, When, or Then where the form requires Gherkin. | Error |
| Structured acceptance | Invalid requirement criteria, unsupported operators, or quoted numeric targets. | Error |
| Evidence and responsibility | Unknown owner or empty source references. | Warning |
| Review state | Pending business review or incomplete writing review. | Warning |
| Illustrative content | `SAMPLE-` identifiers in metadata, related references, or document bodies. | Warning |

Requirements and nonfunctional requirements need structured acceptance criteria with numeric measure values.
Keep all criteria in one `acceptance_criteria` list and add matching scenarios within one Gherkin Feature.
Remove quotes around numeric targets after replacing their placeholders.
Review readable Gherkin against structured criteria and measurement conditions.
The linter checks selected syntax and structure. It does not establish equivalent business meaning across these representations.

### Schema access

The [authoring schema](sdlc-artifact.schema.json) defines metadata and required sections for all 37 artifact kinds.
The packaged runtime owns the canonical `core/schemas/sdlc-artifact.schema.json` source.
The catalog copy supports inspection beside the guides.
Use this command to export the installed runtime's schema:

```sh
ai-sdlc lint --print-schema > sdlc-artifact.schema.json
```

The schema uses JSON Schema Draft 2020-12.
Its instance is a parsed projection of one Markdown artifact:

| Property | Projection |
| --- | --- |
| `metadata` | Mapping parsed from the artifact's opening YAML frontmatter. |
| `sections` | Mapping from exact level-two heading text to that section's Markdown body. |

The CLI creates this projection before schema checks.
A general JSON Schema validator requires the same projection; raw Markdown is not a JSON Schema instance.
Preserve heading spelling and case from the Template block.
The CLI also checks duplicate identities, placeholders, selected Gherkin, and other rules outside JSON Schema.
Schema validation alone does not perform those checks.

### Python use

Use the installed package API when another local tool needs structured findings.

```python
import json
from ai_sdlc_workbench.artifact_lint import artifact_schema, lint_artifacts

result = lint_artifacts(["docs/sdlc"], strict=False)
print(json.dumps(result, indent=2))
schema = artifact_schema()
```

The result includes `schema_version`, `status`, `valid`, `artifacts`, `findings`, and `limitations`.
Each finding identifies its input path, code, severity, and message.
`status` is `PASSED` or `FAILED`; `valid` reflects the selected normal or strict gate.

### Local CI use

Select the directory that contains completed authoring artifacts.
Run the same gate before review and in local CI:

```sh
ai-sdlc lint docs/sdlc --strict
```

Exit code `0` passes this lint gate.
Exit code `1` fails this lint gate.
The JSON result reports status, artifact count, findings, and evidence limits.
Retain that result with the reviewed revision when the project needs check evidence.
Resolve unknown information through the responsible owner; do not invent values to remove warnings.

### Validation boundaries

Artifact linting checks authoring forms selected by `artifact_kind`.
`ai-sdlc --workspace PATH validate` checks the separate governed Workbench knowledge contracts and provenance.
Use both commands when an authored document also becomes a governed knowledge record.

A lint result does not authenticate reviewers, establish source authority, grant approval, or verify business execution.
It does not resolve external source references or prove traceability relationships.
It does not run business tests, execute Gherkin steps, or establish complete ASD-STE100 compliance.
Markdown checks cover selected headings, fences, comments, and code spans. They do not implement a complete CommonMark parser.
Keep required human review and retained execution evidence separate from lint findings.

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

Apply this intake sequence to business behavior requirements and defects in existing repositories.
Create the business task directory before source discovery or investigation.
Start its `intake.md` with the defect report for unexpected behavior or the requirement guide for requested behavior.
Record known facts and prior answers before asking focused questions about material gaps.
Search existing knowledge, linked requirements, and cited source bytes before asking the user to restate intent.
Record applicable criterion IDs and source limits. Keep documented intent separate from publication approval.
After a required clarification completes, update affected knowledge and its provenance before handoff.
Do not leave resolved material knowledge changes only in chat or task notes.
Then inspect registered code, test assertions, and investigation results. Repositories can use `repos/` or configured locations.
Read existing reports as secondary evidence and inspect their cited sources.
Use the [intake procedure](../../../.agents/skills/analyze-requirement/SKILL.md) for question rounds, evidence collection, and phase readiness.
Retain new results under the same task's `evidence/` directory with an evidence index.
Keep authoritative domain snapshots and audit events in their established locations.
An explicitly authorized task-evidence relocation preserves exact bytes and source identities through an old-to-new locator manifest.
Archive the earlier provenance manifest, update active snapshot paths, and append a new relocation audit event.
Use `READY` only when material uncertainty is resolved for the named next phase. Record the rationale.
`READY_WITH_LIMITS` permits evidence collection only. `NEEDS_CLARIFICATION` blocks downstream work.
Keep investigation readiness separate from implementation approval and business review.
Unknown deployed revisions must not prevent authorized local evidence collection.
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
Run ai-sdlc lint on the saved artifact and report errors, warnings, and evidence limits.
```
