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

**Recommendation: pilot two optional hooks for completion checks and resume context. Keep workflow decisions in the existing skills.**

Hooks can reduce missed checks and repeated context discovery. They are not required for Workbench operation.
The expected benefit remains unmeasured. No hook was implemented or enabled during this assessment.

## Scope and evidence

- Authority: [exact user request, 12 November 2026](../evidence/workflow-hooks-assessment-20261112/user-input.md#exact-user-input).
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

## Recommended hook pilot

| Order | Event and trigger | Action | Expected benefit and boundary |
| --- | --- | --- | --- |
| 1 | `Stop`, after changes within an explicitly selected scope | Run applicable existing validation and evidence-reference checks once for that content. Return a compact advisory result. | Catch missed checks before handoff. Skip unchanged turns and unrelated drafts. A finding does not authorize repairs or semantic updates. |
| 2 | `SessionStart`, for startup, resume, or compact | Supply the selected workspace, active living record, and next required check. Point to the existing coordinator. | Reduce repeated discovery and context loss. Keep output short. Do not infer the active task from modification times or dirty files. |
| Later | `PreCompact` or scoped handoff check | Remind the agent to reconcile retained cases and the living report. | Support interruption recovery. This cannot replace immediate persistence after each completed case. |
| Later | Knowledge freshness check after relevant source changes | Invoke existing planners for an explicit collection or canonical scope. Report queues only. | Expose unfinished work without compiling, governing, or advancing receipts. Planning can write ignored working files. |
| Later | Optional Git pre-commit | Validate the staged candidate with the same deterministic primitives. | Catch errors outside agent sessions. Existing filesystem validators need a staged-content adapter before this is reliable. |

Do not introduce every candidate together. Start with the first two and measure their value.

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
Keep active-scope pointers session-local and ignored. They locate existing records; they do not become another lifecycle store.
If no scope is selected, provide neutral guidance and skip task-specific checks.
Cache only disposable check identities and results. Key them by selected inputs, content hashes, configuration, and validator version.
Discard stale cache entries. A cache hit cannot establish approval or business verification.

Proposed pilot limits: a short explicit timeout and no more than 500 context tokens per resume cue.
These are design targets, not measured results. Failures should identify the skipped check and its concrete cause.
Missing prerequisites should produce one actionable message, without installing packages automatically.
Use one bounded check batch per relevant content version. An advisory hook should not request automatic continuation.

### Codex support and constraints

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
| Assessment documentation | 25 local links and anchors resolve. All 59 bound source hashes still match. Whitespace checks pass. |
| Live hook behavior and latency | Not run. No hook implementation exists in this change. |
| Runtime unit suite and package build | Not run for this documentation-only assessment. |

`ai-sdlc` is available through the project virtual environment, but absent from the active shell's default command path.
The pilot must select an installed interpreter and command explicitly.
Generic `status` constructs [Workbench](../../core/runtime.py) and [Store](../../core/store.py), which can initialize local state.
`validate` bypasses that construction. Do not describe every status or planning operation as read-only.

Confidence is high for inspected structure and command boundaries.
Confidence is moderate for expected experience improvements because no comparative usage trial was performed.

Next action: pilot the two optional adapters when implementation is requested.
Compare added latency, useful findings, duplicate messages, and resume effort across representative sessions.
Include read-only work, unrelated dirty files, subdirectory starts, compaction, missing CLI, and concurrent sessions.
Retain the pilot only if its observed benefit exceeds its overhead.
