---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Workbench workflows, skills, and hook recommendations

**Implementation follow-up:** the user [authorized implementation](../evidence/workflow-hooks-assessment-20261112/implementation-request.md#exact-user-input)
after this assessment. The current [hook guide](../HOOKS.md) describes the shared runtime, installation, native adapters, and execution limits.
The implemented Claude adapter uses isolated `.claude/workbench-hooks.json` with an explicit `--settings` launch command,
so Copilot does not inherit a duplicate registration from ordinary Claude settings.
The assessment below preserves the preimplementation baseline. Its source hashes, inspection counts, candidate mappings, and validation outcomes are historical evidence.

**Recommendation: share one Workbench hook implementation across Codex, GitHub Copilot, and Claude Code through thin client adapters.**

Hooks can reduce missed checks and repeated context discovery. They are not required for Workbench operation.
Compatibility with all three clients is required for the proposed feature. Client configuration and event names can differ.
The expected benefit remains unmeasured. No hook was implemented or enabled during this assessment.

## Scope and evidence

- Authority: [exact user request, 12 November 2026](../evidence/workflow-hooks-assessment-20261112/user-input.md#exact-user-input).
- First-priority clarification: [hooks must work across all three clients](../evidence/workflow-hooks-assessment-20261112/cross-client-requirement.md#exact-user-input).
- Scope: harness assessment and suggestions. No business intake or knowledge transition is required.
- Source baseline: `88bb73bb2b94fae40f2c1bd0ae51c6ea0a38450f`, with existing local changes.
- Exact inspected file hashes: [source bindings](../evidence/workflow-hooks-assessment-20261112/source-bindings.json).
- Inspected local changes include the new knowledge lifecycle manager and its guide integration.
- Consumer: Workbench users and agents performing engineering work, knowledge maintenance, and handoffs.
- Owner: Workbench maintainer; named owner unknown.
- Risk: low for this assessment. Future hook integration introduces latency, duplicate execution, and scope-selection risks.

The review inspected all 39 local skill names and descriptions, selected workflow bodies, adapters, validation entrypoints, and scaffolding.
It did not execute every skill or establish general model adherence.
Pre-existing code, task, knowledge, and wiki changes remain outside this assessment's edits.

## Current workflow assessment

| Area | Inspected design | Assessment and consequence |
| --- | --- | --- |
| Business SDLC | [Core workflow](../../ARCHITECTURE.md#core-workflow) and [entry routes](../../tasks/README.md#lifecycle-entry-routes) distinguish requirements, supplied implementation, and exploration. | Keep these routes. Hooks cannot infer business approval or readiness from file changes. |
| Knowledge coordination | [Lifecycle manager](../../.agents/skills/manage-knowledge-lifecycle/SKILL.md) selects existing operations and distinguishes inspection from authorized continuation. | Reuse this coordinator. Another router or status ledger would duplicate responsibility. |
| Skill decomposition | [Lifecycle map](../KNOWLEDGE_LIFECYCLE.md#major-step-orchestrators) defines six parent skills and 17 operation skills. | The structure supports selective loading. Load the relevant parent and operations instead of every knowledge skill. |
| Incremental work | [Source planning](../../core/ingestion/incremental.py) and [wiki bridge](../../.agents/skills/llm-wiki/scripts/wiki.py) identify changed and unfinished work. | Reuse these mechanisms. A watcher and separate hash database would duplicate existing mechanics. |
| Evidence handoffs | [Current task view](../../.agents/skills/analyze-requirement/references/current-task-view.md) and [case checkpoints](../../tasks/README.md#save-case-evidence-and-resume-checkpoints) define persistence and reconciliation. | Strong procedures exist. Their timely execution still depends on agent behavior. |
| Deterministic checks | [CLI](../../core/cli.py), [workspace validation](../../core/validation.py), and [assurance contracts](../BEHAVIOR_REVIEW.md#validate-save-and-report) expose reusable checks. | Hooks can invoke these checks at declared boundaries. Passing checks do not establish semantic conformance. |
| Client integration | [Claude adapter](../../adapters/claude-code/README.md), [Copilot adapter](../../adapters/copilot/README.md), and [scaffold](../../scaffold.json) reuse canonical skills. | Preserve client independence. Put optional event configuration in adapters. |

The architecture explicitly describes agent procedures, rather than an implemented durable workflow runner.
Hooks should improve procedure timing without creating another workflow engine.

## Existing hooks and discovery

No general Workbench client hook configuration or pre-commit configuration was found in the inspected project sources.
The root has no `.codex/` directory or `.github/workflows/` directory. Local `core.hooksPath` is unset.
These observations do not cover global client configuration or externally managed policies.

Two imported Release Clinic files contain hook declarations:

- [Report plugin](../../core/release-clinic/plugins/test/dtp-tda-report/hooks.json): its command only echoes `DISABLED:skill_usage_logger dtp-tda-report`.
- [Service plugin](../../core/release-clinic/plugins/test/dtp-tda-service/hooks.json): its command only echoes `DISABLED:skill_usage_logger dtp-tda-service`.

These commands provide no validation, recovery, or real logging. Their presence does not prove registration with the active client.
[Ponytail setup](../SETUP.md#ponytail-coding-skill) explicitly excludes upstream hooks, dashboards, global plugins, and auxiliary commands.

One discovery inconsistency exists independently of hooks.
[CES migration scan](../../.agents/skills/ces-migration-scan/SKILL.md) is a canonical skill but lacks a declared Claude alias in [scaffold.json](../../scaffold.json).
All 38 declared aliases currently resolve to matching skill bytes.
Claude users relying on those aliases have inconsistent access to this additional specialized skill.
Priority is low; no failed user session was demonstrated.
Owner: Workbench maintainer, named owner unknown. Next action: align its alias with the intended distribution scope.

## Recommended shared hook behavior

| Order | Shared behavior and trigger | Action | Expected benefit and boundary |
| --- | --- | --- | --- |
| 1 | Completion check, after changes within an explicitly selected scope | Run applicable existing validation and evidence-reference checks once for that content. Return a compact advisory result. | Catch missed checks before handoff. Skip unchanged turns and unrelated drafts. A finding does not authorize repairs or semantic updates. |
| 2 | Session context, when the client starts an agent session | Supply the selected workspace, active living record, and next required check. Point to the existing coordinator. | Reduce repeated discovery and context loss. Keep output short. Do not infer the active task from modification times or dirty files. |
| Later | Client-supported compaction or resume events | Remind the agent to reconcile retained cases and the living report. | Support interruption recovery. This cannot replace immediate persistence after each completed case. |
| Later | Knowledge freshness check after relevant source changes | Invoke existing planners for an explicit collection or canonical scope. Report queues only. | Expose unfinished work without compiling, governing, or advancing receipts. Planning can write ignored working files. |
| Later | Optional Git pre-commit | Validate the staged candidate with the same deterministic primitives. | Catch errors outside agent sessions. Existing filesystem validators need a staged-content adapter before this is reliable. |

Start with the first two behaviors across all three clients. Keep extra client events outside the shared minimum.

### Select checks by declared scope

The following commands already exist. Replace placeholders with selected local inputs.

```sh
ai-sdlc --workspace PATH validate
ai-sdlc --workspace PATH lint DOCUMENT
ai-sdlc --workspace PATH gherkin TEST_CASE
ai-sdlc --workspace PATH assurance index --input INDEX --require-current
ai-sdlc --workspace PATH assurance questions --input INDEX
ai-sdlc --workspace PATH assurance validate --baseline BASELINE --require-current
```

Use artifact lint only for supported artifact formats. Use Gherkin checks only for relevant cases.
Use assurance operations when the selected task has a compatible index or baseline.
Workspace validation inspects broader workspace content. Report pre-existing findings separately from findings within the selected scope.
Do not make unrelated drafts trigger repeated blocking feedback.

Do not infer unrun test success from a validation result. Full applicable unit tests remain a deliberate delivery requirement.
Running the full suite after every edit would add friction without replacing that requirement.

### Keep the adapter small

Use the installed Python runtime and existing commands. Keep reusable implementation under `core/` if implementation is later requested.
Generated workspaces should receive configuration and guides, while using the installed runtime.
Use client adapters only to translate event payloads, configuration, and result presentation.
Keep scope selection, validation rules, and check results shared across clients.
Do not duplicate business rules in `.codex/`, `.github/`, and `.claude/` configuration.
Extend the existing [agent-independent architecture](../../PRINCIPLE.md#5-agent-agnostic-by-design).
Keep active-scope pointers session-local and ignored. They locate existing records; they do not become another lifecycle store.
Bind pointers and disposable caches to the client, session, selected workspace, and explicit scope.
If no scope is selected, provide neutral guidance and skip task-specific checks.
Cache only disposable check identities and results. Key them by selected inputs, content hashes, configuration, and validator version.
Discard stale cache entries. A cache hit cannot establish approval or business verification.

Proposed pilot limits: a short explicit timeout and no more than 500 context tokens per resume cue.
These are design targets, not measured results. Failures should identify the skipped check and its concrete cause.
Missing prerequisites should produce one actionable message, without installing packages automatically.
Use one bounded check batch per relevant content version. An advisory hook should not request automatic continuation.

### Documented client support

Client integration must map the shared behavior to each native configuration and event contract.
The following Copilot mapping uses its current shared harness.

| Client surface | Project configuration | Context event | Completion event |
| --- | --- | --- | --- |
| Codex | `.codex/hooks.json`, or inline hooks in `.codex/config.toml` | `SessionStart` | `Stop` |
| Claude Code | `hooks` in `.claude/settings.json` or `.claude/settings.local.json` | `SessionStart` | `Stop` |
| GitHub Copilot CLI | `.github/hooks/*.json`, with `version: 1` | `sessionStart` | `agentStop` |
| GitHub Copilot in VS Code, Copilot harness | Same Copilot hook format | `sessionStart` | `agentStop` |

The [Claude Code reference](https://code.claude.com/docs/en/hooks) documents session startup, resume, and per-turn completion.
Its context output uses `hookSpecificOutput.additionalContext` with the matching `hookEventName`.
Claude and Codex share some event names, but their complete schemas and failure behavior require separate adapter validation.

The [Copilot reference](https://docs.github.com/en/copilot/reference/hooks-configuration) documents local CLI and cloud execution separately.
The [VS Code guide](https://code.visualstudio.com/docs/copilot/customization/hooks) confirms the shared Copilot harness and marks hooks as preview.
Its deprecated Local harness has a separate format. Do not use that legacy schema for the new Copilot adapter.
`sessionEnd` is session termination. It must not replace the Copilot turn-completion event, `agentStop`.

Copilot command hooks support model-visible `sessionStart` context through top-level `additionalContext`.
Its PascalCase compatibility event names select snake_case input fields. The canonical camelCase names select camelCase fields.
Adapters must translate these contracts explicitly instead of sharing JSON configuration blindly.

Copilot also reads repository `.claude/settings.json` and `.claude/settings.local.json` hook blocks.
Applicable sources accumulate, so independent Claude and Copilot registrations can duplicate execution.
The installer must account for inherited registrations and verify deduplication with all three client configurations present.
Do not infer a reliable native client identity solely from compatible payload fields.

Copilot cloud hooks require the package and configuration inside the cloud environment.
Local installation does not establish cloud availability. Cloud and deprecated harness support require separate declared validation.
All linked client hook references were fetched on 12 November 2026.
They establish documented capability. Installed client versions and live cross-client behavior were not verified.

### Codex-specific constraints

The [official OpenAI hook documentation](https://learn.chatgpt.com/docs/hooks) was fetched on 12 November 2026.
It documents project `.codex/hooks.json`, inline configuration, lifecycle events, and desktop hook review.
This establishes documented capability, not successful execution in the installed desktop build.

- Non-managed hooks require review and trust. Changed definitions require renewed review.
- Hooks from multiple configuration layers accumulate. Matching command hooks can run concurrently.
- `SessionStart` supports `startup`, `resume`, and `compact`, including context after automatic compaction.
- A blocking `Stop` requests continuation. It does not establish a release gate.
- Any future continuation mode must inspect `stop_hook_active` and impose a bounded retry policy.
- Background hooks can complete out of order and be cancelled. They cannot guarantee durable case evidence.
- Tool hooks have coverage exceptions. They are useful guardrails, rather than complete enforcement.

Keep the initial hook pair advisory. Avoid concurrent writes to task records, knowledge, provenance, or audit files.
Use each client's actual documented event schema. Do not assume Codex configuration also works in Claude or Copilot.

### Required compatibility checks

Both shared behaviors must work through the three client integrations before the feature can be called supported.
Configuration parsing alone cannot establish successful hook execution.

| Case | Required result across the supported clients |
| --- | --- |
| Same explicit scope and source bytes | Equivalent context pointers, selected validators, and check findings. |
| Missing scope, read-only work, or unrelated drafts | No guessed task, broad scan, or false failure attribution. |
| Existing hook configuration | Preserve unrelated hooks and settings during installation, update, disablement, and removal. |
| Claude settings loaded by Copilot | With all client configurations installed, execute each shared operation once and deliver context through the actual host contract. |
| Concurrent clients and sessions | Isolate scope and disposable cache identities. Do not switch another session's task. |
| Missing runtime, timeout, or failed validation | Show a bounded advisory result. Do not loop, repair semantic content, or report a false pass. |
| Generated workspace | Invoke the installed package without copying runtime source or requiring this checkout. |
| Native Windows and macOS | Resolve executable paths, spaces, Unicode, and subdirectory launches correctly. |
| Resume or compaction differences | Declare supported events separately. Do not claim identical lifecycle coverage. |

Installation should merge Workbench-owned entries idempotently. Removal should delete only those entries.
Test native payload and output contracts, then run actual hook smoke tests for every declared client surface.
Keep native event names in diagnostics so unsupported events and adapter failures remain visible.

## Changes that hooks should not perform

Keep intent interpretation, readiness decisions, publication approval, audit creation, and processing completion in their existing workflows.
Do not automatically compile the wiki, rebuild graphs, execute remote tools, or alter permissions.
The [wiki bridge](../../.agents/skills/llm-wiki/scripts/wiki.py) already rejects native watcher operations for linked canonical records.
Avoid installing the wider upstream Ponytail hook ecosystem without demonstrated local need.

Exact prompt capture could be assessed later, with explicit owning scope and retention rules.
Generated continuation prompts must not become new human instructions or approval evidence.
An ignored chat journal cannot replace the required durable task input.

## Validation and limits

| Check | Result |
| --- | --- |
| `.venv/bin/ai-sdlc --workspace . validate` | Exit 0; `VALID`; 15 canonical documents; no findings. This does not validate all task evidence or wiki semantics. |
| Local skill metadata | 39 entrypoints; names match directory IDs; descriptions are present; zero metadata errors. |
| Declared Claude aliases | 38 aliases; zero missing files or byte differences. CES is absent from the declared alias set. |
| Initial assessment documentation | 25 local links and anchors resolved. All 59 bound source hashes matched. Whitespace checks passed. |
| Revised cross-client assessment | 28 local links and anchors resolve. All 59 bound source hashes still match. Whitespace checks pass. |
| Live hook behavior and latency | Not run. No hook implementation exists in this change. |
| Runtime unit suite and package build | Not run for this documentation-only assessment. |

`ai-sdlc` is available through the project virtual environment, but absent from the active shell's default command path.
The pilot must select an installed interpreter and command explicitly.
Generic `status` constructs [Workbench](../../core/runtime.py) and [Store](../../core/store.py), which can initialize local state.
`validate` bypasses that construction. Do not describe every status or planning operation as read-only.

Confidence is high for inspected structure and command boundaries.
Confidence is moderate for expected experience improvements because no comparative usage trial was performed.

Next action: implement and pilot both shared behaviors with adapters for all three clients when requested.
Compare added latency, useful findings, duplicate messages, and resume effort across representative sessions.
Include read-only work, unrelated dirty files, subdirectory starts, compaction, missing CLI, and concurrent sessions.
Retain the pilot only if its observed benefit exceeds its overhead.
