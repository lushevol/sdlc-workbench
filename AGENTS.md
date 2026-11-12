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
- Keep `repos/` visible for independent Git checkouts from any source host.
- Exclude grouped checkout directories from Workbench Git with `/repos/*/*/`.
- Keep repository guides available for Workbench tracking.
- Add exact parent ignore entries for custom flat checkout paths.
- Each checkout owns its `.git`, remotes, branches, and commits.
- Track portable relative checkout locations in `registry/repositories.yaml`.
- Initialization ships `repos/README.md` and empty catalogs. It does not clone repositories.
- Keep machine paths in ignored `workspace.local.yaml` when possible.
- Do not import a parent project or require parent-relative commands.
- Keep source adapters, future AI governance, and implemented deterministic validation clearly distinguished.

## Brownfield portability

High-priority source: user request, 30 October 2026. Exact wording:

> make this project designed generic as possible, I want to ship any brown field projects. check if skills and functional components and constructions are generic enough.

The source checkout preserves this input in `docs/evidence/generic-brownfield-portability-20261030/user-input.md`.
Read [the adoption boundary](docs/WORKSPACE_DESIGN.md#brownfield-adoption-boundary) before adding project-specific support.

- Keep shared skills independent of a business domain, source host, language, test engine, and agent client.
- Select specialized helpers only when the inspected project fits their documented coverage.
- Use direct source inspection and existing repository tools when extraction support is absent.
- Report unsupported scope explicitly. An empty graph does not establish the absence of dependencies.
- Keep tenant identities, endpoints, stream mappings, and business fixtures in project configuration or retained evidence.
- Keep generated catalogs empty and tenant settings unset. Preserve existing repositories and their instruction files.
- Treat custom catalog classifications as metadata. They do not add parsers, connectors, or execution grants.

## User input and reference priority

Record the user's input before further investigation or delegation. Preserve its exact wording and source.
Keep business-task input under the owning task's evidence directory. Keep harness instructions in the applicable project guide.
Always save each user input as a high-priority reference with its source and date.
Link preserved input from the active review document or applicable guide before using it to change meaning.

Use the latest explicit user clarification as the first-priority reference for intended behavior within its stated scope.
Preserve conflicting sources. Keep observed behavior, deployment evidence, execution verification, and publication approval separate from user intent.
Do not infer a missing business answer from a request to continue.

Investigate available evidence before sending clarification questions to the user.
Answer resolved questions with a confidence level, supporting source links, rationale, and material limits.
Ask only meaningful remaining questions when the evidence cannot support a confident answer for the next decision.
Apply the [investigation and confidence rules](tasks/README.md#investigate-before-asking).
High-priority source: [user instruction, 26 October 2026](#investigation-first-source).

Use one living question document for each related clarification scope. Collect material open questions in that document.
Let the user answer a batch before review. Preserve returned answers before further investigation.

For knowledge review, provide short topic narratives with questions beside the relevant explanation.
Give each question suggested options and an editable answer field. Permit another answer, unknown, or a named contact.
Label proposed choices clearly. Do not preselect a business answer or replace an existing recorded answer.
Hand over the editable document for asynchronous completion. Resume ingestion when the user returns answers and requests continuation.
Preserve unanswered questions. A continuation request supplies no missing business answer or publication approval.

Refine affected knowledge and record reviews and provenance. Repeat in the same document until no material question remains.
Keep unresolved evidence distinct from unanswered policy. Publish resolved knowledge when its review and publication requirements are met.

### Investigation-first source

High-priority source: user message, 26 October 2026. Exact wording:

> You must try your best to investigate the answers to questions first, answer with confidence level and sources , only ask meaningful questions. Only throw questions to me if you are not confident. update in rules.

## Requirement and issue intake

Use task intake for business behavior requirements and defects in existing business repositories.
Harness maintenance requires no task or business knowledge record.
This includes Workbench setup, configuration upgrades, dependencies, and tooling.
Maintain their code, guides, validation, and Git commits directly.

Classify work by its effect on business behavior. A configuration change that alters session policy follows business intake.
For mixed requests, track the business scope in its task and handle harness support as maintenance.

At Workbench entry, create or reuse `tasks/<task-id>/` before new analysis or implementation.
Read [the task guide](tasks/README.md) and create `01-intake.md` from the applicable requirement or defect template.
Select the [lifecycle entry route](tasks/README.md#lifecycle-entry-routes) before further work.
Accept supplied implementation as evidence. Record its actual revisions and dates without reconstructing prior intent or approval.
Use `READY` for explicitly bounded exploration when its goal, authorization, constraints, and required evidence support that stage.
Full product ACs can follow exploration. Product implementation, acceptance, and release retain their own readiness and approval requirements.
Keep implementation state, intent review, execution outcome, and acceptance disposition separate.
High-priority source: user adoption request, 26 October 2026. Exact wording:

> yes, how can you enhance this flow into workbench ?

Use the [lifecycle document order](tasks/README.md#document-order) for task filenames.
Keep the question log, investigation results, new reports, and new evidence under that task.
Index existing evidence with exact locators, revisions, and hashes.
Keep authoritative domain sources and existing audit events in their established locations.
Keep task-generated investigation evidence under its owning task.

Save each completed case immediately in durable task evidence, including parallel completions, before further execution, waits, or handoff.
Follow [the case evidence checkpoints](tasks/README.md#save-case-evidence-and-resume-checkpoints) for progress updates, volatile state, interrupted runs, and final reconciliation.

Keep one living intake and a short evidence index prominent. Apply the [task retention priorities](tasks/README.md#evidence-priorities-and-cleanup).
Apply the [critical evidence policy](tasks/README.md#critical-evidence-and-reusable-payloads) to business tasks and harness maintenance.
Retain only evidence needed for decisions, reproduction, required assertions, recovery, or protected provenance.
Keep each payload once. Reuse exact paths and hashes with separate case and run identities.
Keep optional exports and routine diagnostics in ignored runtime storage. Preserve required evidence before runtime cleanup.
High-priority source: [critical evidence request, 7 November 2026](docs/evidence/evidence-retention-review-20261107/user-followup.md#exact-user-input).
Apply [evidence growth controls](tasks/README.md#control-evidence-growth-before-execution) before each investigation run.
Retain one canonical capture payload. Reference shared run bindings from compact case records.
Update living reports during active work. Create frozen successors only when a retained decision requires a new baseline.
Keep required case durability, consequential failures, registered snapshots, and immutable audit history.
High-priority source: [evidence growth request, 5 November 2026](docs/evidence/task-evidence-growth-20261105/user-input.md#exact-user-input).
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
Knowledge describes requirements, intent, and ideal target system behavior.
Retain business terms, intended rules, workflows, requirements, decisions, contracts, and target business-system architecture.
Business-system technical knowledge qualifies when it explains intended domain behavior or responsibilities.
Record actual implementation, deployment observations, and intent-to-reality differences in independent task gap Markdown.
Link each gap to canonical intent, exact old/new source, assertions, retained observations, consequence, owner, and next action.
A defect fix changes conformance evidence. It does not change the intended rule.
Update knowledge meaning only when a sourced requirement, decision, or clarification changes that intent.
High-priority source: [user clarification, 1 November 2026](docs/evidence/knowledge-intent-boundary-20261101/user-input.md#exact-user-input).
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

Follow the [coverage output rules](#coverage-output) for requirement, defect, implementation, and verification reviews.

## Reusable knowledge lifecycle skills

High-priority source: [skill decomposition and implementation request, 12 November 2026](docs/evidence/knowledge-skill-lifecycle-20261112/user-input.md#exact-user-input).

Follow [the knowledge lifecycle and skill map](docs/KNOWLEDGE_LIFECYCLE.md).
Keep source preparation, canonical governance, and derived wiki freshness as separate lifecycles.
Use major-step parents as orchestrators. Reuse their operation skills for scoped work and check each operation's output.
Keep hashing, validators, schemas, locks, and engine lifecycle mechanics in existing tools.
Do not add a parallel wiki state machine or infer knowledge approval from successful compilation.
Keep wiki provenance finalization, verification, and required recovery coordinated.

High-priority source: [incremental update request and authorization, 12 November 2026](docs/evidence/knowledge-skill-lifecycle-20261112/incremental-update-proposal.md#exact-user-input).
Run local file-level change planning before semantic knowledge work.
Use `sources plan` after refresh and selection; use `sources view --plan` for queued kept pages.
Load only queued sources, prior affected records, and necessary governing context into semantic review.
Review former dependents when a source withdraws claims. Broaden discovery when declared relationships are incomplete.
Record successful canonical processing with `sources complete`; selection or observed hashes alone do not establish completion.
Keep processing receipts under `evidence/knowledge/processing/`; keep full planning baselines in ignored working storage.
Plan wiki updates before engine dispatch. Skip unchanged inputs only when reviewed receipts and current outputs agree.
Use exact canonical record selection for scoped wiki work. Missing completion evidence requires scoped review.
Keep failed and partial work retryable. Do not advance receipts to conceal incomplete processing.
Preserve original full-file hashes. Section-level optimization remains outside the current processing contract.

## Source preparation before knowledge ingestion

High-priority source: [implementation request, 11 November 2026](docs/evidence/initial-ingestion-source-filter-20261111/user-implementation.md#exact-user-input).
Layout correction: [cleanup authorization, 12 November 2026](docs/evidence/initial-ingestion-source-filter-20261111/user-layout-cleanup.md#exact-user-input).

Use these processing stages: complete raw export → filtered source view → canonical knowledge → derived wiki.
Accept complete exports in ignored `evidence/knowledge/incoming/COLLECTION/`. Do not create a separate top-level raw directory.
Keep retained originals under `evidence/knowledge/sources/`. Preserve registered source snapshots and previous manifest records.
Use [prepare-knowledge-sources](.agents/skills/prepare-knowledge-sources/SKILL.md), [the command reference](.agents/skills/ingest-knowledge/references/source-preparation.md), and installed `ai-sdlc sources` commands.
Keep selection metadata under `evidence/knowledge/selections/`. Generate filtered views only in ignored working storage.

Apply [the source filter policy](.agents/skills/ingest-knowledge/assets/source-filter.yaml) through semantic source review.
Select intended behavior, domain definitions, contracts, responsibilities, and behavior-relevant constraints.
Route actual implementation, deployment observations, and execution results to evidence.
Exclude generic tutorials, unrelated operational logistics, unfilled templates, and navigation-only content from the intent input.

Read mixed documents by section. Preserve conditions, exceptions, draft status, conflicts, and missing-content limits.
Do not decide meaning from filenames, keywords, or implementation alone.

Save the source page's SHA-256 with every selection and generated link.
Bind each decision to its source revision, selected ranges, policy hash, and governing context hashes.
Bind generated views to original source identity and output hashes. Verify bindings before reuse.

Reassess changed pages, including previously excluded pages. Changed rules or context also require reassessment.
Missing pages do not authorize deletion of evidence or knowledge.

Generate exact excerpts or links instead of copying full source trees.
Keep canonical citations bound to original retained revisions. Source preparation does not publish knowledge or refresh the wiki.
The wiki consumes canonical records through hash-bound aliases. Never write through those source links.

## Primary knowledge wiki

Use the [Workbench llm-wiki bridge](.agents/skills/llm-wiki/SKILL.md) to select the wiki engine.
Start native skill operations through `python3 .agents/skills/llm-wiki/scripts/wiki.py run status` from this workspace, then use the [project command translations](.agents/skills/llm-wiki/references/workflows.md#project-scoped-commands).
These project instructions override upstream discovery examples: bare `openkb` can select a different global KB. Keep the explicit workspace selection; do not set a global default to repair project discovery.
Use [OpenKB](.agents/skills/openkb/SKILL.md) as primary only when both an LLM URL and token are configured.
Use private `OPENAI_API_BASE` and `LLM_API_KEY` in the project KB `.env` or process environment.
If either value is absent, use the unchanged llm-wiki-agent skill in the current ADE agent context.
Keep the active compiled workspace at `knowledge/llm-wiki/` and link source inputs to canonical records.
Reserve that directory for the single derived wiki, source aliases, state, and visualization; canonical knowledge validation, ingestion and service-graph projection exclude it and continue checking the original records.
Validate its engine-specific format and source bindings with the bridge's `verify` command.
In fallback mode, read llm-wiki-agent's original `AGENTS.md`, then apply the bridge's source-link and existing-layout constraints.
Maintain summaries, concepts, entities, contradictions, and the index. Preserve OpenKB fields and use explorations for saved synthesis.
Keep `raw/` and `wiki/sources/` immutable canonical symlinks; do not invoke upstream scripted ingest or refresh on them.
Keep the existing rich pages in that shared workspace; switching engines does not regenerate a parallel wiki.
Use the bridge for installation, semantic engine selection, source bindings, and local OpenKB verification and visualization in either mode.
OpenKB model operations use explicit URL and token configuration. Do not select device OAuth automatically or reuse the ADE login.
Reopen canonical sources before relying on derived claims, preserve unresolved conflicts, and keep publication and actual-behavior evidence under their existing procedures.

## Coverage output

High-priority source: user message, 25 October 2026. Exact wording:

> enhance coverage output, should display the coverage of requirements/defact AC -> Test Case coverages, AC -> code change coverage and code change -> Test Case Coverage, ideally TC >= AC = Code Change, code implementation should 100% the same with requirement/defacts, no more no less.

Show AC-to-test, AC-to-code-change, and code-change-to-test matrices with separate evidence and denominators.
Tests must cover each applicable AC and relevant boundaries. Implementation must match intended business behavior exactly.
Interpret `TC >= AC = Code Change` as behavior containment and equivalence, not equal counts of artifacts.
One change can implement several ACs. Several cases can test one AC.
Inspect direct assertion chains before linking changes to tests. Shared AC links do not establish that relationship.
Keep missing behavior, contradictory behavior, unsupported additional behavior, and untraced changes visible.
Distinguish required unchanged implementation from changed units, supporting maintenance, and test-only changes.
Do not claim 100% conformance from complete links, passing commands, or measured line coverage.
Keep definition, assertion, conformance, and passing-execution metrics separate. Report unresolved scope and empty denominators explicitly.
Use the [coverage procedure](.agents/skills/verify-implementation/references/behavior-review.md#report-coverage) and shared traceability template.

## Migration compatibility in code review

High-priority source: [user clarification, 10 November 2026](tasks/ces-tile-rollout-review-20261109/evidence/user-followup-20261110.md#exact-user-input).
Exact wording:

> explain issues in details, please keep in mind when code review that the migration principle is keep API and expose contracts as before as possible so that upper application can be migrate seamless.

Treat existing caller APIs and exposed behavior as the migration compatibility baseline.
Prefer service, SDK, or shared-layer adapters that preserve existing upper-application calls where possible.
Inspect endpoints, omitted request defaults, response fields, types, nullability, identity meaning, JWT claims, permissions, and errors.
Trace actual old consumers against candidate providers and supported mixed deployment versions.
Separate direct contract breaks from availability defects and conditional operational risks.
For each compatibility issue, show the old contract, candidate behavior, affected caller, consequence, and smallest preserving correction.
Do not require upper-application changes when a deterministic lower-layer projection can preserve the contract.
Do not invent scalar roles, owners, permissions, or business mappings to imitate the old response shape.
When valid new semantics cannot fit the old contract, highlight the exception, unresolved decision, and any necessary caller change.
Keep source-derived compatibility, controlled execution, and live verification separate.

## Code review verification

Use actual end-to-end verification when it can establish a review issue's reachable trigger and tangible user or system impact.
Use existing tests or a focused authorized probe. Compare the same case against baseline and candidate when claiming a regression.
Assert the failure and its observable consequence. Bind results to exact source revisions, assertions, environment, and configuration.
Retain screenshots and request or state evidence where applicable. Disclose substituted services, synthetic data, and controlled clocks.
Save each completed case immediately under the owning task's evidence rules.
Keep failed reproduction and unavailable environments visible. They do not confirm a defect or prove its absence.
Controlled execution proves only its stated boundaries. It does not establish production reachability, frequency, or impact.
Preserve existing authorization. Verification does not authorize application fixes or deployment.

High-priority source: user message, 28 October 2026. The exact wording follows.
The original capture remains in the source checkout task evidence.
Exact wording:

> When you're doing a code review, if you find an issue, you can use actual end-to-end verification to prove it's real and has a tangible impact. Please add this to the rule as well.

## Before editing

Inspect the worktree and preserve unrelated changes.
Before changing an existing symbol, inspect its callers, importers, and affected interface paths.
Record the affected scope and qualitative risk in the task notes or progress report.
Use direct source inspection when this project has no usable index.
Do not invent a GitNexus score or query an unrelated business repository.
Follow an owning business repository's instructions when changes extend into that repository.

### Coding tasks with Ponytail

High-priority source: [user request, 6 November 2026](docs/evidence/ponytail-integration-20261106/user-input.md#exact-user-input).

Use the canonical [Ponytail skill](.agents/skills/ponytail/SKILL.md) for coding tasks by default.
Read it before writing, fixing, refactoring, reviewing code, or choosing dependencies.
Use `full` mode unless the user requests `lite`, `ultra`, or `off`.
Honor the user's mode changes within the coding scope.
Preserve the owning repository's architecture and instructions.
Keep required intake, coverage, evidence, tests, security, accessibility, and authorization checks.
A smaller change must still implement the complete authorized behavior.

## Release confidence assessments

### User-impact priority

High-priority source: user instruction, 29 October 2026. The exact wording follows.
The original capture remains in the source checkout task evidence.
Exact wording:

> Our rule is this: as long as there's no evidence that a failure, partial issue, or blocker affects the user's experience, or if the impact is very minimal, doesn't disrupt their session, doesn't force-logout them, and doesn't break the app so they can't use it, we can lower its priority, unless it's a truly blocking problem.
>
> Please apply this principle to every issue you find. Also, for that original layout, clean it up by removing everything unnecessary.

Apply this rule to each issue, including failed cases, partial verification, blocked checks, and review observations.
Lower priority when disruptive user impact is unproved or the observed effect is minimal.
Retain higher priority for demonstrated session disruption, forced reauthentication, unusable application flows, or genuine blocking security failures.
State the concrete consequence and evidence for each retained blocker.
Do not treat an unavailable test environment as a product failure or an automatic release hold.
Keep verification status, potential severity, priority, and release-blocking disposition separate.
Lower priority does not convert a failure into a pass or establish complete verification.
Show the release conclusion and essential metrics first. Put supporting detail behind expandable sections or direct links.

### Assessment procedure

Use [release-confidence](.agents/skills/release-confidence/SKILL.md) for production readiness judgments.
Assess business impact, system impact, review, requirements, tests, and operational evidence.
Report qualitative evidence confidence separately from the production recommendation.
Keep missing evidence, known failures, and residual risks visible.
Keep the recommendation separate from recorded human deployment authorization.

Treat runtime log evidence as a key release-confidence metric during UAT.
Collect UAT evidence from remote log systems. Local logs support local development only.
Use both E2E execution and bounded representative usage, with essential paths declared for the selected change.
Bind logs to the tested build, environment, configuration, cases, time window, and request or session correlations.
Report acquisition, binding, analysis, behavior outcomes, and unexplained signals separately.
Follow the [runtime log evidence procedure](.agents/skills/release-confidence/references/runtime-log-evidence.md).
Missing required remote evidence limits UAT conclusions. It does not establish an application defect.
High-priority source: [user instruction, 31 October 2026](docs/evidence/runtime-log-verification-20261031/user-followup.md#exact-user-input).

Apply [principle 10](PRINCIPLE.md#10-delivery-requires-passing-unit-tests) before recommending delivery or release.
Every applicable candidate unit test must pass. Require zero failures and complete execution of the declared suite.
Keep test counts, runner errors, source identity, and retained execution evidence visible.
Do not obtain passing status through removed checks, skipped failures, expected failures, narrowed scope, or weakened assertions.
Correct test defects only with evidence. Preserve genuine application failures and their release hold until correction passes.

### Unit-test release source

High-priority source: user message, 27 October 2026. Exact wording:

> add UT all pass no failure to delivery release principle, fix UT failure, better not change any code.

## Dependency maintenance

High-priority source: [user request, 3 November 2026](docs/evidence/dependency-setup-maintenance-20261103/user-input.md#exact-user-input).

Apply [principle 7](PRINCIPLE.md#7-local-first-minimal-dependencies) to every dependency change.
Apply this rule whenever a new component introduces a package, runtime, tool, service, or platform prerequisite.
Update [dependency analysis](docs/DEPENDENCIES.md) and [setup instructions](docs/SETUP.md) in the same change.
Update package manifests, lockfiles, setup scripts, offline preparation, and readiness checks for the affected installation paths.
Keep one installer implementation behind [the macOS launcher](setup.command), [the Windows launcher](setup.cmd), and [Python setup](core/bootstrap.py).
Extend [dependency diagnostics](core/doctor.py) when the new component introduces a prerequisite that can be checked locally.
Report missing prerequisites and concrete next actions. Exclude credential values from reports.
Keep diagnosis available before installation. Keep package readiness separate from live service access and business verification.
Update relevant regression tests and check installed-package and generated-workspace behavior when those interfaces change.
Record the dependency's current consumer, version constraints, platform needs, download domains, and runtime network calls.
Check both connected installation and installation from a prepared bundle when those paths are affected.
State any target platform or external access that remains untested.
Do not introduce an undeclared startup download or an automatic external update check.

High-priority source: [download timeout request, 3 November 2026](docs/evidence/dependency-download-timeouts-20261103/user-input.md#exact-user-input).
Every new scripted dependency acquisition path must define a bounded command deadline and bounded request retries.
Use the shared configurable download deadline for setup and offline preparation where applicable.
When acquisition fails or times out, warn users and identify the affected component and concrete manual recovery steps.
Document approved download sources, matching versions and platforms, local asset placement, and the readiness command after recovery.
Keep credential values out of warnings and instructions. Preserve incomplete status until the prerequisite checks pass.
Keep optional browser downloads explicit and provide matching-platform bundle instructions when direct downloads are blocked.

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

High-priority source: user message, 28 October 2026. Exact wording:

> Reorganize the naming and content guidelines for these SDLC documents into a standard format, and check their templates.

Use the [task naming and content standard](tasks/README.md#document-order) and the [SDLC authoring catalog](core/knowledge/templates/sdlc/README.md#task-document-selection).
Select the form by its purpose. Preserve its required headings and record template checks separately from business verification.

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
