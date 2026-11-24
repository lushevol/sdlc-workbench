# Evidence and log retention

> **Critical conclusion: Commit decision evidence and keep routine diagnostic output in ignored local storage.**
>
> Owner: Workbench maintainer. Next action: use this boundary for subsequent task output and evidence selection.
> Historical evidence remains protected by the existing cleanup rules.

## Request and scope

Source: current Codex chat, 24 November 2026, Asia/Singapore.

> implement `clarify evidence and log retention`

The earlier user direction establishes the requested boundary:

> separate evidence with logs, evidence is important to key decision and should be record with git source management, but logs more likely to use one time or troubleshooting, should not commit in git. Your opinion ?

Baseline: `92a3f2c721d0239f933b1e7a74ef2f0eb9691317`.
The worktree was clean at entry.
Apply the boundary to current instructions and applicable routine-output defaults.
Preserve required assertion, failure, timing, correlation, recovery, and governance evidence.
Keep one maintenance record. Store routine command output in ignored local logs.
Remote history replacement remains outside this implementation step.

### Task-local log clarification

Source: current Codex chat, 24 November 2026, Asia/Singapore.

> I prefer to keep logs still in task but git ignore them.

Clarification baseline: `e76b86e8947ce3ebe4d798940b45d78a5bc7bf35`.
This clarification governs routine task output placement.
Keep routine logs under `tasks/<task-id>/logs/<run-id>/` and exclude those directories from Git.
Keep selected evidence under `tasks/<task-id>/evidence/` and preserve its existing retention rules.
Update affected instructions, audit defaults, ignore rules, and generated-workspace checks.
Qualitative risk: medium if ignore rules hide evidence or explicit output destinations change.
Implemented the clarification and verified its Git and package boundaries.

## Scope, consumers, and risk

Inspect task procedures, root guidance, experience extraction instructions, generated-workspace assets, and E2E capture consumers.
Qualitative risk: medium if changed output defaults hide required evidence or break readers.
Keep existing explicit evidence-run paths and retention contracts compatible.

## Outcome and checks

Implemented the [evidence and log boundary](../README.md#git-managed-evidence-and-local-logs).
Commit selected evidence that supports consequential decisions, assertions, findings, reproduction, recovery, or protected provenance.
Keep routine diagnostics in ignored `tasks/<task-id>/logs/<run-id>/` storage.
Classify content by purpose. File extensions do not determine retention.
Keep necessary raw context. A hash cannot replace required source bytes.

Updated root guidance, architecture, browser procedures, Robot procedures, capability extraction, experience packaging, and knowledge composition.
Canonical source snapshots remain under `knowledge/evidence/sources/`.
Required native assertion results and remote UAT log evidence remain required.
Compact routine check receipts belong in the living record.

The [audit configuration](../../e2e/audit.config.ts) defaults to ignored `tasks/e2e-audit/logs/<run-id>/` output.
Explicit `E2E_AUDIT_OUTPUT` destinations remain supported.
The [audit guide](../../e2e/README.md#screenshot-audit-runs) explains selection, promotion, reference checks, and exact-file staging.
The `/tasks/*/logs/` ignore rule covers routine task output.
The `.workbench/` rule still covers disposable runtime state and scratch storage.

The [configuration regression](../../e2e/unit/audit-retention.test.ts) checks default and explicit destinations across all reporters and artifact paths.
The [generated-workspace regression](../../tests/test_workspace_layout.py) checks Git behavior with real files.
Routine `.log` and JSON output stays ignored. Selected `.log`, JSON, and raw text evidence stages normally.
Task-log exclusion applies to separate tasks without hiding nested evidence directories named `logs/`.
Robot examples select the owning task's log root before entering the independent test repository.
Private configuration remains local runtime state.

Independent review identified conflicting snapshot placement and unconditional Robot retention wording.
The final guidance links canonical snapshots and distinguishes routine output from retained business verification evidence.
Promotion also preserves required procedures and protected provenance.

### Initial implementation verification

Source: initial implementation committed as `e76b86e89`, 24 November 2026.
Environment: local macOS, repository Python environment, Node, and controlled Chromium fixtures.
The candidate commit includes this record and the scoped changes.
Initial routine output now resides in `tasks/workbench-evidence-log-retention-20261124/logs/implementation/`.

| Check | Exit status and result |
| --- | --- |
| `WORKBENCH_CONNECTOR_INTEGRATION=1 .venv/bin/python -m unittest discover -s tests -v` | `0`; 1,165 passed, zero failures or skips. |
| `npm run e2e:unit` | `0`; 30 passed, zero failures or skips. Includes nine audit-retention tests. |
| `npm run e2e:typecheck` | `0`; TypeScript checks passed. |
| `node --import tsx --test e2e/integration/audit-retention.test.ts` | `0`; one integration test passed. Controlled passing and failing cases verify artifacts, hashes, and trace retention. |
| Skill structure validation | `0`; the three changed skills passed `quick_validate.py`. |
| `.venv/bin/ai-sdlc --workspace . validate` | `0`; workspace valid, zero findings. |
| Wheel build and installed-workspace smoke check | `0`; 13 shipped files match source. Two routine files stay ignored; three selected evidence files stage. |
| Changed Markdown links and anchors; `git diff --check` | `0`; 14 changed links and anchors resolve. Whitespace checks passed. |

No related registry capability matched the scoped lookup. No registry promotion is required.
The built wheel was installed outside this checkout with `pip install --no-index --no-deps --target`.
The isolated smoke check imported the installed runtime and initialized a fresh workspace.
The generated workspace validated with zero findings.
It retained responsibility guides and omitted project tasks, runtime Python source, tests, and `pyproject.toml`.
The wheel build used `pip wheel . --no-deps --no-build-isolation` with output under the local log directory.
These checks establish local retention behavior and package integrity within their stated scope.
They do not establish business acceptance or live environment verification.
Historical payloads and the cleanup receipt remain unchanged.
Remote publication was not performed.

### Task-local clarification verification

Source: follow-up candidate on clarification baseline `e76b86e89`, 24 November 2026.
Environment: local macOS, repository Python environment, Node, and controlled browser fixtures.
Routine output: `tasks/workbench-evidence-log-retention-20261124/logs/task-local-followup/`.
Moved ten local files from `.workbench/logs/workbench-evidence-log-retention-20261124/implementation/` to this task's `logs/implementation/`.
All ten SHA-256 values matched after relocation.
No required evidence or frozen manifest was relocated.
Independent review found no actionable defects in the final follow-up diff.

| Check | Exit status and result |
| --- | --- |
| `WORKBENCH_CONNECTOR_INTEGRATION=1 .venv/bin/python -m unittest discover -s tests -v` | `0`; 1,165 passed, zero failures or skips. Local server permission was available. |
| `.venv/bin/python -m unittest tests.test_workspace_layout -v` | `0`; 24 passed, including the task-local Git regression. |
| `npm run e2e:unit` | `0`; 30 passed. Default, explicit task-log, and explicit evidence destinations remain consistent. |
| `npm run e2e:typecheck` | `0`; TypeScript checks passed. |
| `node --import tsx --test e2e/integration/audit-retention.test.ts` | `0`; one controlled Chromium integration passed with local browser permission. |
| Wheel build and installed-workspace smoke check | `0`; seven changed shipped files match source. The installed Git regression passed. |
| `.venv/bin/ai-sdlc --workspace . validate` | `0`; workspace valid, zero findings. |
| Changed Markdown links, Robot shell syntax, and `git diff --check` | `0`; six links and six shell blocks passed. All five Robot output paths use task logs. |

Sandbox attempts could not start local test servers or Chromium.
Observed diagnostics included `PermissionError: [Errno 1] Operation not permitted` and Chromium startup `EPERM` with `SIGABRT`.
Permitted local execution passed without test changes.
The two troubleshooting logs remain ignored beside this receipt's other routine output.
Robot commands received syntax checks; no business Robot case was executed.
The follow-up does not change remote branches or required evidence retention.

### Return to the previous branch

Source: current Codex chat, 24 November 2026, Asia/Singapore.

> Apply changes in this branch to previous branch, I want to use back

Source branch: `feature/clean-baseline-20261124` at `6a84cb97c`.
Previous branch: `feature/knowledge-layout-consolidation` at `60698ebdf`.
Carry the current tracked snapshot, including task cleanup and retention changes, onto the previous branch.
Append a commit to its existing history and return this checkout to that branch.
Preserve the source branch, ignored task logs, independent repositories, and existing stash.
Qualitative risk: medium because the branches have unrelated history and many task files differ.
Compare tree identities and guard the destination's original revision before changing its reference.
Returned this checkout to `feature/knowledge-layout-consolidation`.
The transfer commit has the previous branch tip as its sole parent.
Its tracked snapshot matches `6a84cb97c`, apart from this updated handoff record.
The source branch remains unchanged.
Verified all 25 pre-existing task-log hashes and the original stash identity.
Workspace validation passed with zero findings. Diff whitespace checks passed.
The implementation matches the previously tested snapshot; no runtime tests were repeated for this Git transfer.
The previous branch retains its historical commits. No remote reference was changed.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not establish complete writing review.
```
