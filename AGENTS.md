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
- Keep business repositories independent. Clones under ignored `repos/` are optional.
- Keep machine paths in ignored `workspace.local.yaml` when possible.
- Do not import a parent project or require parent-relative commands.
- Keep source adapters, future AI governance, and implemented deterministic validation clearly distinguished.

## Requirement and issue intake

Start every new requirement or issue in `tasks/<task-id>/` before analysis or implementation.
Read [the task guide](tasks/README.md) and create `intake.md` from the applicable requirement or defect template.
Keep the question log, investigation results, new reports, and new evidence under that task.
Index existing evidence with exact locators, revisions, and hashes.
Keep authoritative domain sources and existing audit events in their established locations.
Keep task-generated investigation evidence under its owning task.
For an authorized relocation, preserve bytes and stable source identities in an old-to-new locator manifest.
Archive the prior provenance manifest, update active snapshot paths, and append a relocation audit event.

Use three primary inputs: `knowledge/`, registered repository code and tests, and investigation results.
Read existing reports as additional evidence before asking users to repeat available information.
Inspect registered repository code, test assertions, and retained executions at exact revisions.
Use applicable browser, Playwright, service, or live data-flow investigations within granted access and user authorization.
Record facts, inferences, conflicts, missing evidence, and each clarification answer with its source.
Resolve material knowledge ambiguity, missing rules, or stale content before changing its meaning.
After clarification, update the affected knowledge record, version, provenance, and knowledge-update log before handoff.
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

Repositories, services, capabilities, contracts, sources, and executable tools have separate identities.
Support many-to-many relationships through declared IDs and evidence links.
Metadata declarations do not grant execution or prove a runtime relationship.
Inspect exact source revisions before treating code as evidence.
Read cited sources before treating retrieved text as approved intent.

Preserve raw snapshot bytes and stable manifest source identities.
Preserve previous manifest bytes when an explicitly authorized relocation changes snapshot locations.
Add a new snapshot when a source changes.
Preserve candidate knowledge and findings until investigation resolves them.
Keep approved knowledge separate from candidates and raw sources.
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
Inspect test assertions and retained execution before claiming behavior verification.
A passing command alone does not establish verified behavior.

## Before editing

Inspect the worktree and preserve unrelated changes.
Before changing an existing symbol, inspect its callers, importers, and affected interface paths.
Record the affected scope and qualitative risk in the task notes or progress report.
Use direct source inspection when this project has no usable index.
Do not invent a GitNexus score or query an unrelated business repository.
Follow an owning business repository's instructions when changes extend into that repository.

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
Report the commit hash, validation results, and any remaining blocker.

## SDLC output standard

Use ASD-STE100 for human-facing reports, findings, behavior descriptions, and proposed actions.
Use one main idea per sentence, active voice, and stable technical terms.
Use no more than 20 words per prose sentence and six sentences per paragraph.
Give each finding evidence, a consequence, an owner, and a next action.
Mark an unknown owner explicitly.
State evidence limits with the claims they limit.

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
