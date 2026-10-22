# AI SDLC Workbench project guide

This project connects existing engineering assets through shared context, relationships, evidence, and executable tools.
The standalone root is this directory.
Read [PRINCIPLE.md](PRINCIPLE.md), [ARCHITECTURE.md](ARCHITECTURE.md), and [the workspace design](docs/WORKSPACE_DESIGN.md) before structural changes.

## Implementation boundary

- Keep the single Python runtime and its responsibility guides under `core/`.
- Preserve the installed package name `ai_sdlc_workbench` through package mapping.
- Copy only responsibility guides into generated workspaces. Do not copy runtime source.
- Keep catalog examples under `registry/examples/` and check them against the supported contracts.
- Retain items only with a current consumer, observable benefit, and supporting evidence.
- Remove speculative implementation and demonstrations. Preserve evidence under the retention rules below.
- Keep tests for supported behavior, consequential boundaries, and confirmed defects.
- Keep `repos/` visible for independent Azure DevOps (ADO) Git checkouts.
- Exclude grouped checkout directories from Workbench Git with `/repos/*/*/`.
- Keep repository guides available for Workbench tracking.
- Add exact parent ignore entries for custom flat checkout paths.
- Each checkout owns its `.git`, remotes, branches, and commits.
- Track portable relative checkout locations in `registry/repositories.yaml`.
- Initialization ships `repos/README.md` and empty catalogs. It does not clone repositories.
- Keep machine paths in ignored `workspace.local.yaml` when possible.
- Do not import a parent project or require parent-relative commands.
- Keep source adapters, future AI governance, and implemented deterministic validation clearly distinguished.

## User input and reference priority

Record the user's input before further investigation or delegation. Preserve its exact wording and source.
Keep business-task input under the owning task's evidence directory. Keep harness instructions in the applicable project guide.

Use the latest explicit user clarification as the first-priority reference for intended behavior within its stated scope.
Preserve conflicting sources. Keep observed behavior, deployment evidence, execution verification, and publication approval separate from user intent.
Do not infer a missing business answer from a request to continue.

Use one living question document for each related clarification scope. Collect material open questions in that document.
Let the user answer a batch before review. Preserve returned answers before further investigation.

Refine affected knowledge and record reviews and provenance. Repeat in the same document until no material question remains.
Keep unresolved evidence distinct from unanswered policy. Publish resolved knowledge when its review and publication requirements are met.

## Requirement and issue intake

Use task intake for business behavior requirements and defects in existing business repositories.
Harness maintenance requires no task or business knowledge record.
This includes Workbench setup, configuration upgrades, dependencies, and tooling.
Maintain their code, guides, validation, and Git commits directly.

Classify work by its effect on business behavior. A configuration change that alters session policy follows business intake.
For mixed requests, track the business scope in its task and handle harness support as maintenance.

Start each business requirement or issue in `tasks/<task-id>/` before analysis or implementation.
Read [the task guide](tasks/README.md) and create `01-intake.md` from the applicable requirement or defect template.
Use the [lifecycle document order](tasks/README.md#document-order) for task filenames.
Keep the question log, investigation results, new reports, and new evidence under that task.
Index existing evidence with exact locators, revisions, and hashes.
Keep authoritative domain sources and existing audit events in their established locations.
Keep task-generated investigation evidence under its owning task.

Save each completed case immediately in durable task evidence, including parallel completions, before further execution, waits, or handoff.
Follow [the case evidence checkpoints](tasks/README.md#save-case-evidence-and-resume-checkpoints) for progress updates, volatile state, interrupted runs, and final reconciliation.

Keep one living intake and a short evidence index prominent. Apply the [task retention priorities](tasks/README.md#evidence-priorities-and-cleanup).
Keep claim-bearing execution, source, test, and provenance evidence as supporting material.
Remove redundant reports, repeated outputs, empty artifacts, and unrelated harness bulk when cleanup is authorized.
Retain meaningful failed and contradictory evidence. Preserve registered snapshots and immutable audit history.
Record deleted paths, hashes, prior Git revisions, and reasons in one cleanup record. Repair active references.
For an authorized relocation, preserve bytes and stable source identities in an old-to-new locator manifest.
Archive the prior provenance manifest, update active snapshot paths, and append a relocation audit event.

Use three primary inputs: `knowledge/`, registered repository code and tests, and investigation results.
Read existing reports as additional evidence before asking users to repeat available information.
Inspect registered repository code, test assertions, and retained executions at exact revisions.
Always compare old and new behavior when analyzing requirement-to-implementation gaps.
Describe each gap with clear ASD-STE100 setup, numbered steps, and separate intended, old, and new results.
Follow the [baseline comparison and case rules](tasks/README.md#compare-behavior-for-gap-analysis).
Use applicable browser, Playwright, service, or live data-flow investigations within granted access and user authorization.
Record facts, inferences, conflicts, missing evidence, and each clarification answer with its source.
Resolve material knowledge ambiguity, missing rules, or stale content before changing its meaning.
When clarification changes business understanding, update affected domain knowledge, provenance, version, and the task's knowledge-update log before handoff.
Do not leave a resolved material clarification only in chat or task notes.
Keep required human review and publication gates separate from clarification.
Continue evidence collection until material uncertainties no longer block the named next phase.

Only `READY` permits that next phase, with evidence and a scope-specific rationale.
`READY_WITH_LIMITS` permits further intake evidence collection only.
`NEEDS_CLARIFICATION` blocks the next phase.
Keep intake readiness separate from business approval and knowledge publication.
These states guide agent procedure; the core does not enforce an executable intake gate or workflow runner.
Generated workspaces receive `tasks/README.md` without project task contents.

## Evidence and knowledge

Keep `knowledge/` limited to business-domain Markdown records and navigation.
Retain business terms, rules, workflows, requirements, decisions, contracts, and relevant business-system architecture.
Business-system technical knowledge qualifies when it explains domain behavior or responsibilities.
Exclude Workbench maintenance, logs, raw sources, code copies, fixtures, execution results, reports, and intermediate files.
Keep task investigations under `tasks/<task-id>/evidence/`.

Store retained source snapshots under `evidence/knowledge/sources/` and their manifest at `evidence/knowledge/manifest.yaml`.
Store governance findings and immutable audit events under `evidence/knowledge/findings/` and `evidence/knowledge/audit/`.
Keep record schemas and templates under `core/knowledge/`.
Knowledge records can cite external evidence without copying it into `knowledge/`.

Repositories, services, capabilities, contracts, sources, and executable tools have separate identities.
Support many-to-many relationships through declared IDs and evidence links.
Metadata declarations do not grant execution or prove a runtime relationship.
Inspect exact source revisions before treating code as evidence.
Read cited sources before treating retrieved text as approved intent.

Preserve raw snapshot bytes and stable manifest source identities.
Preserve previous manifest bytes when an explicitly authorized relocation changes snapshot locations.
Add a new snapshot when a source changes.
Preserve candidate knowledge and findings until investigation resolves them.
Keep approved domain knowledge separate from candidates. Keep raw evidence outside `knowledge/`.
Use the shipped schemas and templates for Workbench records.

Record each governance change in a new audit event YAML file.
Do not overwrite an existing audit event or rewrite its history.
Retain the event files in Git with the related changes.
Git history and hashes support review. They do not authenticate an actor or establish business approval.

Important requirements and decisions require recorded human review before publication.
Do not invent reviewer identities, approvals, source authority, or execution results.
State facts, inferences, and unresolved questions separately.
An OKF `verified` record concerns knowledge review.
It does not establish passing execution of a business behavior.

Write acceptance criteria as measurable Gherkin scenarios.
Name the conditions, action, observable result, and any required limit.
Test cases defined during requirement or defect refinement or code-change verification must include clear Gherkin steps.
Always include explicit assertions.
Define actors, entities, keywords, data, and limits without ambiguity. Keep one canonical definition source and link each case from consumers.
Follow the [canonical Gherkin test case rules](tasks/README.md#canonical-gherkin-test-cases).
Inspect test assertions and retained execution before claiming behavior verification.
A passing command alone does not establish verified behavior.

## Before editing

Inspect the worktree and preserve unrelated changes.
Before changing an existing symbol, inspect its callers, importers, and affected interface paths.
Record the affected scope and qualitative risk in the task notes or progress report.
Use direct source inspection when this project has no usable index.
Do not invent a GitNexus score or query an unrelated business repository.
Follow an owning business repository's instructions when changes extend into that repository.

## Release confidence assessments

Use [release-confidence](.agents/skills/release-confidence/SKILL.md) for production readiness judgments based on review, requirements, tests, and operational evidence.
Report qualitative evidence confidence separately from the production recommendation.
Keep missing evidence, known failures, and residual risks visible.
Keep the recommendation separate from recorded human deployment authorization.

## Dependency maintenance

Apply [principle 7](PRINCIPLE.md#7-local-first-minimal-dependencies) to every dependency change.
Update [dependency analysis](docs/DEPENDENCIES.md) and [setup instructions](docs/SETUP.md) in the same change.
Update package manifests, lockfiles, setup scripts, offline preparation, and readiness checks for the affected installation paths.
Record the dependency's current consumer, version constraints, platform needs, download domains, and runtime network calls.
Check both connected installation and installation from a prepared bundle when those paths are affected.
State any target platform or external access that remains untested.
Do not introduce an undeclared startup download or an automatic external update check.

## External system access

Use the existing Workbench CLI or MCP interface for external connector tools.
Run `ai-sdlc --workspace PATH status` to discover registered connector resources.
Use each resource's `list` operation to inspect tool schemas and exact tool grants.
Use `call` only for a granted tool within the user's authorized task.
Maintain private connector variables in `.env` at the selected workspace root.
Never put credentials in tool catalogs or call arguments.
Read [the connector guide](docs/CONNECTORS.md) for installation, supported systems, and evidence limits.

## Validation and commits

Run runtime tests and wheel builds from the standalone source checkout:

```sh
python -m unittest discover -s tests -v
python -m pip wheel . --no-deps --wheel-dir dist
```

Generated workspaces do not contain package source, `pyproject.toml`, or runtime tests.
Use the installed command to validate either kind of workspace:

```sh
ai-sdlc --workspace PATH validate
```

Add a regression for a confirmed behavioral defect.
Run checks appropriate to the changed interfaces and data contracts.
For packaging changes, initialize a workspace from the built wheel outside this checkout.
Check that shipped guides, schemas, templates, and shared skills remain available.
For documentation-only changes, check links, commands, and the diff.
Do not rebuild unrelated indexes or generated graphs.

After a completed stage passes its required checks, stage the complete change and commit automatically.
Do not wait for a separate commit request.
Keep each commit within the completed stage.
Review the staged diff and preserve unrelated changes.

Stage harness files explicitly. Do not use `git add repos/`.
Report the commit hash, validation results, and any remaining blocker.

## SDLC output standard

Use ASD-STE100 for human-facing reports, findings, behavior descriptions, and proposed actions.
Use one main idea per sentence, active voice, and stable technical terms.
Use no more than 20 words per prose sentence and six sentences per paragraph.
Give each finding evidence, a consequence, an owner, and a next action.
Mark an unknown owner explicitly.
State evidence limits with the claims they limit.

Highlight critical conclusions near the top of every new or revised human-facing document under `tasks/<task-id>/`.
Use a concise, bold callout for conclusions that require user attention, action, or a decision.
Include the required action, consequence, owner, and supporting evidence.
State known blockers and their blocked actions explicitly.
State `No critical conclusions require user attention or action.` when applicable.
Follow [the task document rules](tasks/README.md#critical-conclusions-in-task-documents) for placement and historical evidence boundaries.

Use inline Markdown links for cross-document criteria, test cases, findings, evidence, and sources in human-facing documents.
Link each ID separately to its exact definition through a heading anchor or supported line locator, including ranges.
Identify changed or historical requirement and test versions with their exact Git revision or SHA-256.
Link behavior definitions, test assertions, and retained execution evidence separately. Mark unresolved policy and unavailable definitions explicitly.
Follow [the reference rules](tasks/README.md#link-task-definitions-and-evidence) for BDD traceability and preserved historical documents.

Preserve exact quotations, code, commands, identifiers, logs, and machine statuses.

Every saved report must keep automated checks separate from the ASD review:

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```

Set `automated_check` from checks actually performed.
Only a complete writing review can set `asd_review: PASSED`.
Do not claim full ASD-STE100 compliance from an automated check alone.
