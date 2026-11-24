# AI SDLC Workbench project guide

This project connects existing engineering assets through shared context, relationships, evidence, and executable tools.
This file is the entry guide. Follow the linked procedures when their scope applies; their requirements remain mandatory.
Read relevant sections and operation references as needed. Do not load every workflow for an unrelated task.
Before structural changes, read [principles](PRINCIPLE.md), [architecture](ARCHITECTURE.md), and [workspace design](docs/WORKSPACE_DESIGN.md).

## Implementation boundary

- Keep the single Python runtime and responsibility guides under `core/`; preserve the installed package name `ai_sdlc_workbench`.
- Generated workspaces receive responsibility guides, shared skills, and empty catalogs, without runtime source or project history.
- Keep supported catalog examples under `registry/examples/`. Retain implementation and tests only with demonstrated current value.
- Preserve independent checkout ownership. Follow [repository placement](repos/README.md) for Git exclusions, portable locations, and local overrides.
- Do not import a parent project or require parent-relative commands. Keep implemented capabilities separate from planned work.

## Brownfield portability

Follow the [adoption boundary](docs/WORKSPACE_DESIGN.md#brownfield-adoption-boundary).
Keep shared skills independent of business domain, source host, language, test engine, and agent client.
Use specialized helpers only within their evidenced coverage; inspect source directly when extraction is unsupported.
An empty graph does not prove no dependencies. Metadata classifications do not add parsers, connectors, or execution grants.
Keep tenant settings in project configuration or evidence; generated defaults remain empty and unset.
Authority: the [brownfield adoption boundary](docs/WORKSPACE_DESIGN.md#brownfield-adoption-boundary).

## User input and reference priority

Preserve exact user input, source, and date in the owning task before investigation or delegation. Link it from the current record.
The latest explicit clarification governs intended behavior within its scope. Preserve conflicting sources and unresolved questions.
Keep intent, implementation, assertions, execution, knowledge publication, acceptance, and deployment authorization as separate facts.
Investigate available sources before asking meaningful remaining questions. Give supported answers with confidence, rationale, source links, and limits.
Use the [investigation rules](tasks/README.md#investigate-before-asking) and [editable knowledge-review questions](tasks/README.md#document-based-knowledge-review).
A continuation request supplies no missing answer or approval.

### Investigation-first source

The [investigate-before-asking procedure](tasks/README.md#investigate-before-asking) governs source review before meaningful questions.
Historical authority links can refer to source-checkout evidence. Generated workspaces follow the current procedures linked here.

## Documentation and task ownership

Follow [documentation ownership](docs/WORKSPACE_DESIGN.md#documentation-ownership) and [task handoff](tasks/README.md#keep-current-documentation-synchronized).
Keep `docs/` as the stable, integrated current view across lifecycles and domains. Update existing sections as changes become current.
Keep incremental requests, decisions, investigations, and evidence under the owning `tasks/<task-id>/`.
Keep canonical business intent in `knowledge/records/`; docs link it without competing authority.

## Requirement and issue intake

Create or reuse the owning task before new analysis. Apply the [scope rules](tasks/README.md#scope).
Business behavior requirements and defects use `01-intake.md`, the applicable template, and a [lifecycle entry route](tasks/README.md#lifecycle-entry-routes).
Harness maintenance uses a [lightweight maintenance record](tasks/README.md#lightweight-maintenance-records), without business intake, ACs, readiness, or publication gates.
For mixed work, apply business gates only to the business scope. A configuration change that alters business behavior follows business intake.
Supplied implementation retains its actual revisions and dates; do not invent prior intent, history, or approval.
Only evidence-backed `READY` permits the named phase within existing authorization, including [bounded exploration](tasks/README.md#start-bounded-exploration).
`READY_WITH_LIMITS` permits intake evidence collection only. `NEEDS_CLARIFICATION` blocks the next phase. These are agent procedures, not runtime gates.
Follow [task document order](tasks/README.md#document-order), [baseline comparisons](tasks/README.md#compare-behavior-for-gap-analysis), and [knowledge reconciliation](tasks/README.md#update-knowledge-after-clarification).
Save each completed case immediately, including parallel completions, under the [resume checkpoint rules](tasks/README.md#save-case-evidence-and-resume-checkpoints).
Apply [critical evidence retention](tasks/README.md#critical-evidence-and-reusable-payloads), [growth controls](tasks/README.md#control-evidence-growth-before-execution), and [cleanup rules](tasks/README.md#evidence-priorities-and-cleanup).
Retain one canonical payload. Preserve meaningful failures, contradictory evidence, registered snapshots, immutable audits, and recovery information.
Authorized cleanup records paths, hashes, prior revisions, and reasons. Relocation preserves bytes and identities, records mappings, and repairs active references.

## Evidence and knowledge

Follow the [knowledge contract](knowledge/README.md) and [governance design](docs/WORKSPACE_DESIGN.md#knowledge-format-and-governance).
Use one `knowledge/` parent: `records/` for canonical business intent, `evidence/` for sources and governance, and `llm-wiki/` for derived navigation.
Keep schemas and templates under `core/knowledge/`; task investigations and implementation/deployment gaps stay under their owning task.
A defect fix changes conformance evidence. Change intended meaning only from a sourced requirement, decision, or clarification.
When clarification changes intent, reconcile its canonical record, provenance, version, and task update log before handoff; retain required publication review.
Preserve raw snapshot bytes, stable source identities, prior manifests during relocation, candidates, and unresolved findings.
Append new snapshots for changed sources and new immutable governance audit events. Never overwrite earlier evidence or audit history.
Important requirements and decisions need recorded human review before publication. Do not invent authority, actors, approval, or execution results.
Catalog relationships are declarations, not execution grants or runtime proof. Inspect exact source revisions and cited originals before relying on claims.
Write measurable Gherkin ACs and canonical cases with explicit assertions under the [case rules](tasks/README.md#canonical-gherkin-test-cases).
Knowledge `verified`, valid metadata, fresh hashes, and passing commands do not establish passing business behavior.

## Reusable knowledge lifecycle skills

Use [manage-knowledge-lifecycle](.agents/skills/manage-knowledge-lifecycle/SKILL.md) at knowledge workflow entry and handoff.
Identify the evidence-backed stage and concrete next action. Reuse completed operations and continue authorized independent work.
Follow the [lifecycle and skill map](docs/KNOWLEDGE_LIFECYCLE.md), keeping source preparation, canonical governance, and wiki freshness separate.
Run file-level planning before semantic work. Use `sources plan`, queued `sources view --plan`, and reviewed `sources complete` receipts.
Load queued sources, affected prior records, former dependents, and necessary governing context; broaden discovery when relationships are incomplete.
Plan wiki scope before dispatch. Skip unchanged work only when reviewed completion and current outputs agree; keep partial work retryable.
Reuse existing validators, hashing, locks, schemas, checkpoints, and engine lifecycle controls. Do not create parallel state machines or advance receipts over unfinished work.

## Source preparation before knowledge ingestion

Use [prepare-knowledge-sources](.agents/skills/prepare-knowledge-sources/SKILL.md) and its [command reference](.agents/skills/ingest-knowledge/references/source-preparation.md).
The stages are complete export → filtered source view → canonical knowledge → derived wiki.
Keep replaceable imports in ignored `knowledge/evidence/incoming/`, retained originals in `knowledge/evidence/sources/`, and decisions in `knowledge/evidence/selections/`.
Apply the semantic filter policy by section; preserve conditions, exceptions, draft status, conflicts, and missing-content limits.
Bind decisions and views to original hashes, ranges, policy, context, source identity, and output hashes. Verify bindings before reuse.
Reassess changed pages, exclusions, policy, and context. Missing pages do not authorize deletion. Source preparation grants no publication or wiki freshness.

## Primary knowledge wiki

Use the [Workbench llm-wiki bridge](.agents/skills/llm-wiki/SKILL.md) and [project-scoped commands](.agents/skills/llm-wiki/references/workflows.md#project-scoped-commands).
Start at the workspace root with `python3 .agents/skills/llm-wiki/scripts/wiki.py run status`; bare `openkb` may select another global KB.
Use OpenKB model operations only with explicit `OPENAI_API_BASE` and `LLM_API_KEY`; otherwise follow unchanged llm-wiki-agent instructions in the current ADE session.
Do not select device OAuth automatically or reuse ADE authentication. Keep private configuration in local settings.
Maintain one existing `knowledge/llm-wiki/` workspace across engine changes, with its detailed pages, native fields, index, and saved explorations.
Keep `raw/` and `wiki/sources/` as immutable canonical links. Never run upstream source-owning ingest/refresh operations on them.
Canonical scanners select `knowledge/records/`. Coordinate provenance finalization, bridge verification, and recovery; reopen canonical sources before relying on derived claims.

## Coverage output

Follow the [coverage procedure](docs/BEHAVIOR_REVIEW.md#coverage-output-for-requirements-and-defects) and traceability template for applicable reviews.
Show AC-to-test, AC-to-code-change, and code-change-to-test matrices with separate inventories, denominators, definitions, assertions, conformance, and passing execution.
`TC >= AC = Code Change` means behavior containment and equivalence, not matching artifact counts.
Inspect direct assertion chains; shared AC links do not prove change-to-test coverage.
Keep missing, contradictory, extra, untraced, unchanged, maintenance, and test-only scope explicit. Links, line coverage, and passing commands cannot prove exact conformance.
Authority: the [coverage output procedure](docs/BEHAVIOR_REVIEW.md#coverage-output-for-requirements-and-defects).

## Migration compatibility in code review

Existing caller APIs and exposed behavior are the migration baseline. Preserve upper-application calls through deterministic lower-layer adapters where possible.
Inspect endpoints, omitted defaults, response fields, types, nullability, identity meaning, JWT claims, permissions, and errors.
Trace actual old callers against candidate providers and supported mixed versions.
Separate contract breaks, availability defects, and conditional operational risks. Explain old contract, candidate behavior, affected caller, consequence, and smallest preserving correction.
Do not invent scalar roles, owners, permissions, or business mappings to imitate an old response.
When valid new semantics cannot fit, identify the unresolved decision and necessary caller change explicitly.
Keep source-derived compatibility, controlled execution, and live verification separate.
Authority: [10 November migration clarification](tasks/ces-tile-rollout-review-20261109/evidence/user-followup-20261110.md#exact-user-input).

## Portal backward compatibility

Backward compatibility is mandatory for changes affecting FMO Post Trade Portal (Markets Operations One), including `single-ui-bff` and `mfe-base`.
Design changes so existing production consumers can upgrade without modifications or observable behavior changes.
For every portal change, review API compatibility, data structure compatibility, downstream-observable behavior, and whether existing APIs become slower.
Follow the [backward compatibility review procedure](docs/BEHAVIOR_REVIEW.md#review-backward-compatibility).
If a downstream-visible change is unavoidable, minimize API changes and highlight the before-and-after contracts and behavior.
Authority: the [backward compatibility review procedure](docs/BEHAVIOR_REVIEW.md#review-backward-compatibility).

## Code review verification

Use [code-review](.agents/skills/code-review/SKILL.md). Review alone does not authorize fixes, deployment, publication, or external messages.
Use existing tests or a focused authorized E2E probe when it can establish a reachable trigger and tangible consequence.
For regressions, compare the same baseline/candidate case. Assert the failure and observable impact; retain exact sources, assertions, environment, and configuration.
Save each completed case immediately. Disclose substituted services, synthetic data, controlled clocks, unavailable environments, and failed reproduction.
Controlled execution proves its stated scope only; it does not establish production reachability, frequency, or impact.

## Before editing

Inspect the worktree and preserve unrelated changes. Inspect callers, importers, and affected interfaces before changing an existing symbol.
Record affected scope and qualitative risk in the owning record. Follow instructions in each affected business repository.
Use direct inspection without a usable index; do not invent a GitNexus score or query an unrelated repository.

### Learn reusable capabilities

Use [domain-capability-extractor](.agents/skills/domain-capability-extractor/SKILL.md) for reusable domain contracts, workflows, failures, tools, and background context.
Maintain linked Contracts, Workflows, and Knowledge under `knowledge/integrations/<domain>/` through ordinary agent tools.
Extraction requires no hook, learning engine, or experience packet. Keep canonical business intent under existing governance.

Use [capability-learning](.agents/skills/capability-learning/SKILL.md) when scoped registry retrieval or reconciliation is relevant to the task.
For that workflow, search the registry at entry. Load linked skills and contracts, then check scope and permissions.
Use granted connectors and retain exact evidence. Reconcile reusable discoveries at its checkpoints and handoff.
Submit minimized evidence references without waiting for a separate learning request when registry learning applies.
Use validated rules in future sessions. Recheck uncertain evidence when it could change the outcome.
Keep unresolved registry claims as candidates. Follow canonical governance for business intent and entitlement decisions.
Continue the primary task if registry learning fails. Use its [checkpoint fallback](docs/CAPABILITY_LEARNING.md#configure-and-diagnose) when native hooks are unavailable.
Direct domain extraction follows the extractor workflow. Registry work remains separate unless requested or independently relevant.

### Coding tasks with Ponytail

Read [Ponytail](.agents/skills/ponytail/SKILL.md) before coding, reviewing code, refactoring, or choosing dependencies.
Use `full` mode unless the user selects `lite`, `ultra`, or `off`. Preserve architecture and required intake, evidence, coverage, tests, security, accessibility, and authorization.

### Shared native hooks

Follow [the hook guide](docs/HOOKS.md) for client-specific installation, launcher commands, scope binding, and removal.
Keep behavior in the installed Python runtime and native translation in thin adapters, without machine paths in reusable registrations.
Bind the explicit living record and dependencies to the exact client session. Never infer scope from dirty files or another session.
Preserve unrelated settings. Hooks are advisory evidence, not readiness, publication, acceptance, or deployment grants.

## Release confidence assessments

### User-impact priority

Apply this rule to every issue, including failed, partial, blocked, and review outcomes.
Lower priority when disruptive user impact is unproved or minimal. Retain priority for demonstrated session disruption, forced reauthentication, unusable flows, or blocking security failures.
Give each retained blocker concrete consequences and supporting evidence. An unavailable test environment is not a product failure or automatic release hold.
Keep verification status, potential severity, priority, and blocking disposition separate. Lower priority never converts a failure into a pass.
Authority: [user-impact priority direction](tasks/portal-background-session-20261019/evidence/user-input-20261029-impact-priority-layout.txt).

### Assessment procedure

Use [release-confidence](.agents/skills/release-confidence/SKILL.md) for PROD suitability; assess business/system impact, review, conformance, tests, and operational evidence.
Lead with the recommendation and essential metrics. Keep confidence, known failures, residual risk, and human deployment authorization distinct.
For UAT, follow the [runtime log procedure](.agents/skills/release-confidence/references/runtime-log-evidence.md): remote logs, E2E and representative usage, exact build/environment/configuration/time/correlation bindings.
Local logs do not satisfy remote UAT evidence. Missing evidence limits the conclusion without proving an application defect.
Apply [principle 10](PRINCIPLE.md#10-delivery-requires-passing-unit-tests): every applicable candidate unit test must pass, without skipped failures, expected failures, narrowed scope, or weakened assertions.

### Unit-test release source

The exact [27 October unit-test direction](tasks/portal-background-session-20261019/evidence/delivery-confidence-20261026/ut-release-principle-user-input-20261027.md#exact-user-input) remains preserved.

## Dependency maintenance

Apply [principle 7](PRINCIPLE.md#7-local-first-minimal-dependencies) and update [dependencies](docs/DEPENDENCIES.md) and [setup](docs/SETUP.md) together.
Update affected manifests, lockfiles, the shared installer, offline preparation, diagnostics, regression tests, and installed-workspace checks.
Record current consumers, version/platform constraints, download sources, runtime endpoints, and untested access or platforms. Keep diagnosis available before installation.
Every scripted acquisition needs bounded deadlines and retries, sanitized failure guidance, and concrete matching-platform manual/offline recovery.
Keep browser downloads explicit. Do not introduce undeclared startup downloads or automatic external update checks.

## External system access

Use Workbench CLI/MCP under the [connector procedure](docs/CONNECTORS.md).
Discover resources with `ai-sdlc --workspace PATH status`; inspect schemas and exact grants with resource `list` before authorized `call` operations.
Keep private connector variables in the selected workspace's `.env`, never in catalogs, reports, or call arguments.

## Validation and commits

Run applicable checks for changed interfaces. Add a regression for confirmed behavioral defects; documentation changes need link, command, and diff checks.
Runtime tests and wheel builds run from the standalone source checkout:

```sh
python -m unittest discover -s tests -v
python -m pip wheel . --no-deps --wheel-dir dist
ai-sdlc --workspace PATH validate
```

For package/distribution changes, initialize from the built wheel outside this checkout and verify shipped guides, skills, schemas, and templates.
Generated workspaces omit runtime source, `pyproject.toml`, and runtime tests. Do not rebuild unrelated indexes or generated graphs.
After a completed stage passes required checks, explicitly stage its complete change, review the staged diff, and commit automatically.
Keep commits scoped and preserve unrelated edits. Never use `git add repos/`. Report commit, checks, and remaining blockers.

## SDLC output standard

Follow [task naming and content](tasks/README.md#document-order) and the [authoring catalog](core/knowledge/templates/sdlc/README.md#task-document-selection).
Use ASD-STE100: active voice, stable terms, one main idea per sentence, at most 20 prose words per sentence and six sentences per paragraph.
Findings need evidence, consequence, owner, and next action; mark unknown owners and material limits explicitly.
Use the [critical-conclusion callout](tasks/README.md#critical-conclusions-in-task-documents) and [exact definition/evidence links](tasks/README.md#link-task-definitions-and-evidence).
Preserve exact quotations, code, commands, identifiers, logs, and machine statuses.
Every saved report separates actual automated checks from ASD writing review:

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not establish complete writing review.
```

Set `automated_check` from actual checks; only complete writing review can set `asd_review: PASSED`.
