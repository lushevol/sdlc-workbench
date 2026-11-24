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

## Scope, consumers, and risk

Inspect task procedures, root guidance, experience extraction instructions, generated-workspace assets, and E2E capture consumers.
Qualitative risk: medium if changed output defaults hide required evidence or break readers.
Keep existing explicit evidence-run paths and retention contracts compatible.

## Outcome and checks

Implemented the [evidence and log boundary](../README.md#git-managed-evidence-and-local-logs).
Commit selected evidence that supports consequential decisions, assertions, findings, reproduction, recovery, or protected provenance.
Keep routine diagnostics in ignored `.workbench/logs/<task-id>/<run-id>/` storage.
Classify content by purpose. File extensions do not determine retention.
Keep necessary raw context. A hash cannot replace required source bytes.

Updated root guidance, architecture, browser procedures, Robot procedures, capability extraction, experience packaging, and knowledge composition.
Canonical source snapshots remain under `knowledge/evidence/sources/`.
Required native assertion results and remote UAT log evidence remain required.
Compact routine check receipts belong in the living record.

The [audit configuration](../../e2e/audit.config.ts) now defaults to ignored local output.
Explicit `E2E_AUDIT_OUTPUT` destinations remain supported.
The [audit guide](../../e2e/README.md#screenshot-audit-runs) explains selection, promotion, reference checks, and exact-file staging.
The ignore policy already covers `.workbench/`; this change adds an explanatory comment.

The [configuration regression](../../e2e/unit/audit-retention.test.ts) checks default and explicit destinations across all reporters and artifact paths.
The [generated-workspace regression](../../tests/test_workspace_layout.py) checks Git behavior with real files.
Routine `.log` and JSON output stays ignored. Selected `.log`, JSON, and raw text evidence stages normally.

Independent review identified conflicting snapshot placement and unconditional Robot retention wording.
The final guidance links canonical snapshots and distinguishes routine output from retained business verification evidence.
Promotion also preserves required procedures and protected provenance.

### Verification receipt

Source: candidate worktree on the recorded baseline, 24 November 2026.
Environment: local macOS, repository Python environment, Node, and controlled Chromium fixtures.
The candidate commit includes this record and the scoped changes.
Routine output remains in `.workbench/logs/workbench-evidence-log-retention-20261124/implementation/`.

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

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not establish complete writing review.
```
