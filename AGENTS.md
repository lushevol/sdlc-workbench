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

## Evidence and knowledge

Repositories, services, capabilities, contracts, sources, and executable tools have separate identities.
Support many-to-many relationships through declared IDs and evidence links.
Metadata declarations do not grant execution or prove a runtime relationship.
Inspect exact source revisions before treating code as evidence.
Read cited sources before treating retrieved text as approved intent.

Preserve raw snapshot bytes and their manifest records.
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
