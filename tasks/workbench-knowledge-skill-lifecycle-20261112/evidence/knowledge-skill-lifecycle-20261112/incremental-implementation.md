# Incremental knowledge processing implementation

Source: [the user goal and implementation authorization](incremental-update-proposal.md#exact-user-input), 12 November 2026.
Scope: Workbench maintenance on branch `codex/knowledge-skill-lifecycle-20261112`.

## Delivered behavior

Local file-level plans precede semantic reading and separate pending selection review from canonical processing.
Planned views emit queued kept pages with original source hashes, output hashes, and exact line mappings.
Canonical receipts distinguish reviewed completion from source selection and observed hashes.
Updated outputs require matching prepared and sealed final ingestion checkpoints.
No-change results preserve starting output bytes. Partial results report remaining review and processing work separately.

The planner follows source citations, canonical links, related IDs, and prior receipt outputs.
Completion rejects newly discovered dependents without reviewed output coverage.
Shared navigation changes preserve earlier source completions; domain-record changes still invalidate affected processing.
Raw snapshots, existing source identities, and immutable audit history remain protected.
No copied source tree, parallel wiki, or new package dependency was introduced.

The wiki bridge supports local planning, exact record selection, recipe invalidation, and reviewed unchanged-input skipping.
Legacy bindings require scoped bootstrap review. Compiler return alone leaves explicit output review pending.
Review receipts cover prior and new dependents, shared-output owners, and affected saved explorations.
Paired provenance writes retain recovery material and reject concurrent changes.
Plan output paths cannot overwrite canonical documents or existing files.
Parents continue orchestrating reusable operation skills. Rules and command references describe the incremental contract.

## Scope and qualitative risk

Affected callers include source CLI commands, filtered views, ingestion checkpoints, and the existing wiki bridge.
Generated workspaces receive updated guides and skills. The installed Python package supplies deterministic source planning.
The main risk is false completion after partial work or stale dependencies.
Review receipts, current hashes, sealed checkpoints, dependency coverage, and negative-case regressions address that risk.
Hashes identify bytes. They cannot authenticate a reviewer or establish semantic truth.

## Verification

| Check | Result |
| --- | --- |
| Full runtime suite with connector integration enabled | 984 tests passed; zero failures, errors, or skips. |
| Wiki workflow regressions | 55 passed, including zero compiler calls for unchanged completed input. |
| Source, CLI, and checkpoint checks | 65 passed, including real sealed-checkpoint fixtures. |
| Wheel build | Passed with no new dependencies. |
| Fresh installed-wheel workspace | Valid; shipped skills present; incremental CLI lifecycle passed; unchanged queue empty. |
| Current workspace validation | Valid; 14 documents; no findings. |
| Changed skill validation | 11 skills passed. |
| Markdown links and whitespace | Local targets and final diff passed. |

Commands used:

```sh
WORKBENCH_CONNECTOR_INTEGRATION=1 .venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m pip wheel . --no-deps --no-build-isolation --wheel-dir dist
.venv/bin/ai-sdlc --workspace . validate
```

The installed-wheel check used a temporary directory outside this checkout.
It verified the loaded package path, initialized a workspace, and exercised source planning, scoped rendering, completion, and unchanged reuse.
The generated wiki launcher also produced an empty local plan without provider setup.
Routine command output remains in ignored `.workbench/` storage.

Independent forward evaluation found no remaining guidance gaps in source preparation or wiki maintenance scenarios.
Independent code review reproduced and resolved unsafe report output and missing review coverage for newly discovered dependents.
Concurrent provenance edits reject safely. The final review pass reported no remaining open findings.

## Current workspace and limits

A read-only wiki plan found 12 legacy canonical bindings requiring bootstrap review.
The command made no model calls and changed no canonical records, derived pages, or durable bindings.
Only ignored planning output was created.
No live provider compilation, remote access, or token benchmark ran.
Mock compiler fixtures establish call counts and recovery behavior within their declared boundaries.

Deterministic dependency discovery follows declared relationships. Missing declarations require broader semantic investigation.
Final wiki completion still requires full binding and structural verification.
Another stale source or shared-output owner can block finalization while successful compilation and pending attempts remain durable.
Two provenance replacements are not crash-atomic. Interrupted recovery must preserve unrelated edits and inspect ownership.
Section-level processing remains deferred. No percentage token reduction is claimed.

## Procedure

Use [the source plan and completion commands](../../../.agents/skills/ingest-knowledge/references/source-preparation.md#plan-incremental-canonical-work)
and [wiki planning and review receipts](../../../.agents/skills/llm-wiki/references/workflows.md#compile-canonical-records).
The [lifecycle diagram](../../KNOWLEDGE_LIFECYCLE.md) shows the connected stages and completion boundaries.
