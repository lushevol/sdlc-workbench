---
name: validate-sdlc-documents
description: Validate SDLC Markdown documents against Workbench schemas and templates. Use for missing essential fields or sections, Gherkin acceptance criteria, measurable outcomes, and document handoff checks.
---

# Validate SDLC documents

Check document structure with the existing Workbench validators.
Review business meaning separately through agent reasoning.
Use this skill for the SDLC authoring catalog and supported governed knowledge records.

## Select the contract

Read applicable repository instructions and the selected documents before running checks.
Use explicit file paths or directories containing completed artifacts only.
Identify the workspace root when governed records need validation.
Infer inputs from the request and current context when they are clear.

| Input | Validation route |
| --- | --- |
| Markdown with `artifact_kind` | Run `ai-sdlc lint` against the selected authoring artifacts. |
| Supported governed knowledge `type` | Run `ai-sdlc --workspace PATH validate` against the owning workspace. |
| Ordinary document without either discriminator | Compare content manually with the selected template. Report the missing contract declaration. |
| Catalog guide with Template and Sample blocks | Inspect the requested inner artifact separately. The guide itself is not a completed artifact. |

Supported governed types are `Requirement`, `Architecture`, `Decision`, `RepositoryProfile`, `KnowledgeTopic`, and `GovernanceFinding`.
For mixed inputs, use each applicable route and keep their results separate.
If classification is uncertain, state the inferred kind and its evidence.
Ask for clarification only when different contracts would change a material finding.

For UI E2E specifications, also use [gherkin-quality](../gherkin-quality/SKILL.md) for explicit targets, evidence support, and automation mapping.
Its opt-in checks supplement artifact structure validation. Keep business-only acceptance criteria independent of UI implementation details.

Read [the catalog guide](../../../core/knowledge/templates/sdlc/README.md) for authoring contracts and the selected artifact's template.
Read [the knowledge guide](../../../knowledge/README.md) for governed records, provenance, and audit rules.
Use contracts shipped with the selected runtime and workspace.
State any version mismatch before interpreting results.

## Run deterministic checks

Use the installed runtime, or an available project virtual environment.
These commands read documents without changing their contents:

```sh
ai-sdlc lint "docs/requirements/view-invoice.md" "docs/design/invoice-service.md"
ai-sdlc lint "docs/sdlc" --strict
ai-sdlc lint --print-schema
ai-sdlc --workspace "<workspace_root>" validate
```

Replace example paths with selected inputs.
Start with normal lint unless the user or project requires strict validation.
Strict mode fails on warnings as well as errors.
Normal mode can pass with unresolved warnings; report them explicitly.
Use `--print-schema` alone to inspect required metadata and exact headings for the declared `artifact_kind`.
The exported schema describes parsed metadata and sections; raw Markdown is not a JSON Schema instance.

Keep all selected authoring artifacts in one lint call when checking duplicate IDs across those files.
Record the command, selected paths, exit code, status, findings, and stated limitations.
Workspace validation covers configured knowledge and catalogs, not an arbitrary standalone governed file.
Separate findings on selected documents from other workspace findings.
Do not move a governed record or create provenance merely to make validation run.

When reviewing catalog guides, extract only the requested Template or Sample block into temporary storage.
Keep its bytes unchanged and report expected placeholders or illustrative warnings.
Do not lint the catalog directory as completed documents.

If the runtime is unavailable, state that automated validation did not run.
Continue useful manual inspection and identify the required command.
Do not install dependencies, create another validator, or claim schema success as a substitute.

## Check essential content

Use the selected schema and template as the required-field authority.
Check missing metadata, required headings, empty sections, unresolved placeholders, and duplicate identities.
Review meaningful content beyond field presence:

- Identify the purpose, description, scope, exclusions, and responsible owner where the template requires them.
- Resolve source references through available source records. Inspect cited contents before treating them as approved intent.
- Check source locators, exact revisions, available hashes, ownership, and authority assessments.
- Check related IDs and explanations against the referenced documents available within scope.
- Separate facts, inferences, unresolved questions, and justified `not applicable` statements.
- Report pending or rejected reviews and recorded failed checks, even when schema validation permits them.

Mark unavailable evidence and owners `unknown`.
Do not invent identifiers, source authority, review identities, approval dates, thresholds, or execution results.
The artifact linter does not fetch sources or prove relationships.

## Review acceptance criteria

Apply these checks to requirements and other documents that declare acceptance criteria.
Use Gherkin scenarios with explicit conditions, actions, and observable results.

- `Given` identifies relevant conditions and test data.
- `When` identifies the business action or event.
- `Then` identifies the observable result and any required limit.
- `And` and `But` continue the preceding step type without hiding missing conditions, actions, or results.
- A `Scenario Outline` has matching parameters and concrete `Examples` values.
- Positive, negative, boundary, and failure scenarios cover the behavior supported by the stated scope and sources.

For authoring `requirement` and `nonfunctional-requirement`, check one complete structured `acceptance_criteria` list and matching Gherkin scenarios.
Check unique criterion IDs, `given`, `when`, `then`, and `measure` fields against the contract.
Numeric measures need a supported operator, numeric target, unit, and applicable measurement conditions.
Do not quote numeric targets or invent a target to satisfy the schema.
If intent lacks a measurable limit, report the owner decision needed.

Compare descriptions, structured criteria, Gherkin, and Examples for matching intent, values, units, and conditions.
Report contradictions even when automated lint passes.
For example, a structured two-second limit conflicts with a Gherkin five-second limit.
This comparison is an agent review, not an automated equivalence check.

The artifact linter checks an English Gherkin subset; it does not execute step definitions.
Governed requirement validation checks structured criteria, not complete fenced Gherkin syntax.
Review readable scenarios manually when that syntax was not checked automatically.

## Review test case definitions

Apply the [canonical Gherkin test case rules](../../../tasks/README.md#canonical-gherkin-test-cases) to requirement refinement, defect refinement, and implementation verification.
Check that `tasks/<task-id>/test-cases.md` contains the single definition source, with stable case headings for consumer links.
Review complete `Given`/`When`/`Then` steps, measurable assertions, defined entities, test data, and explicit limits.
Report ambiguous terms, missing assertions, duplicate definitions, and broken case links as content findings.
Keep this review separate from schema validation and execution results.

## Report results and corrections

Keep automated results separate from agent content findings and unresolved owner decisions.
Give each finding its path and section or line, evidence, consequence, owner, and next action.
Preserve the validator's finding code and severity when reporting automated results.
Use `unknown` when the responsible owner is unavailable.
State which documents and references were inspected and which checks did not run.
Report warning counts and evidence limits beside any passing status.

Validation is read-only by default.
Apply corrections when the user's request or existing authorization covers them.
Preserve unrelated content and retain unresolved intent for owner review.
After an authorized correction, rerun the applicable checks and report remaining findings.
Changes to governed records must preserve source snapshots and append-only audit history.

When saving a report, follow repository report rules and keep automated checks separate from ASD writing review.
Use this metadata with the actual automated result:

```yaml
standard: ASD-STE100
automated_check: PASSED # Use FAILED when checks fail; use NOT_RUN when checks did not run.
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```

A passing lint or workspace result does not establish approval, business correctness, or verified execution.
Keep recorded human review and retained business execution evidence separate.
Do not claim full ASD-STE100 compliance from automated checks.
