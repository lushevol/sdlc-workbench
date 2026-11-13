# Workbench living-documentation migration

**All five review findings are corrected within the recorded checks. Historical evidence remains preserved. No further deletion requires user action.**

- Work type: Workbench maintenance.
- Date: 13 November 2026.
- Owner: agent:codex; human maintenance owner is not recorded.
- Authority: [exact migration and cleanup request](evidence/knowledge-layout-assessment-20261113/user-input.md#documentation-migration-authorization).
- Governing model: [latest living-documentation clarification](evidence/knowledge-layout-assessment-20261113/user-input.md#living-documentation-model-clarification).
- Design: [current reviewed proposal](design.md#stable-document-series-and-incremental-task-history).
- Follow-up: [user review request](evidence/user-review-request-20261113.md) and [migration review](review.md).
- Current authority: [continuation of the correction actions](evidence/user-correction-request-20261113.md).
- Baseline: `79a410403`; unrelated `core/release-report/`, the concurrent `core/connectors/yarn.lock` deletion, and the separate ADO skills assessment task are excluded.

## Scope and current decision

Maintain a stable documentation series across applicable lifecycle stages and domains. Update existing sections as supported changes become current.
Retain incremental work records and necessary evidence under their owning tasks. Maintenance needs a lightweight record, without business intake gates.
Remove obsolete or conflicting documents and repeated content after checking their current consumers and evidence value.
Preserve exact registered sources, immutable audits, required failures, user input and recovery information.

## Affected scope and risk

Affected consumers include agent instructions, maintained guides, historical reports, task references, canonical navigation, source locators and packaging.
Operational risk is low. Traceability and distribution risk are moderate because many current references cross the old documentation locations.
Use one changes record for original paths, hashes, baseline revisions, destinations and deletion reasons.
Historical locators can resolve through that record and Git. Repair active references without rewriting frozen source payloads or audit history.

## Changes and current documentation

- Reduced `docs/` from 1,042 files to 19 files: 16 maintained guides, including the new [documentation index](../../docs/README.md), and three example files.
- Relocated 966 historical reports and evidence files into their owning tasks. Removed 65 obsolete or redundant files containing 18,238,233 original bytes.
- Reconciled current responsibilities in [workspace design](../../docs/WORKSPACE_DESIGN.md#documentation-ownership), the [task guide](../README.md#lightweight-maintenance-records), root instructions, responsibility guides and first-party skills.
- Integrated the supported workspace-isolation guidance, refreshed current Gherkin examples, and preserved 14 exact release-report case definitions in their [task catalog](../workbench-release-report-20261024/06-test-cases.md).
- Updated package manifests and the existing workspace-initialization test so the maintained documentation index ships to generated workspaces.
- Preserved original source snapshots, canonical record bytes and previous audit events. Repaired active locators, including source-selection context paths, without changing source decisions or hashes.

The sealed [changes ledger](evidence/changes.json) records original paths, hashes, Git recovery revisions, destinations, deletion reasons and current bindings.
The [prior source manifest](evidence/manifest-before.yaml) and new [relocation audit](../../knowledge/evidence/audit/AUD-20261113-documentation-relocation-v1.yaml) preserve the provenance transition.
Meaningful failed graph output has [byte-exact delta recovery](evidence/graph-failure-delta.json). The removed repeated ledger has [deterministic recovery with its original output hash](evidence/ledger-reproduction-receipt.json).

## Validation and outcome

The final [validation record](evidence/validation.json) records the actual checks and limits:

- All 76 affected workspace-layout and Gherkin tests passed. Current workspace validation passed with zero findings.
- All 530 checked current local document links resolve. The wiki verifies 13 unchanged canonical sources without structural findings.
- The wheel built successfully. Installation outside the checkout initialized and validated an empty workspace with the current guides, without project task history, business records or runtime source copies.
- All 225 protected prior source and audit files and 15 governed Markdown files are byte-identical to the original baseline. All 558 prior source identities remain unchanged; two declared snapshot locators moved. All 521 current snapshot bindings match their hashes.
- Both compact recovery methods reproduced the exact original bytes. The sealed ledger's current bindings passed an independent review and final hash verification.
- The separate post-relocation harness passed its prepared and sealed checks. Original-baseline preservation is proved separately; the later harness baseline does not replace that proof.

The final validator exposed an unsupported classification in one newly appended source registration. Correcting it to the supported `implementation` value resolved the finding before commit; prior source records and audit bytes were unchanged.
Portal and netting each retain one existing source-review HOLD, with their previous processing queues still open. These are existing knowledge-workflow limits.
Full runtime tests, live business scenarios, external URLs and native Windows were outside this documentation and packaging check. Some heading fragments remain unchecked by the harness.
This change establishes documentation and storage maintenance, with no business execution, knowledge publication or live deployment claim.

## Follow-up review outcome

The [requested review](review.md) supersedes any inference that the earlier structural checks established a complete or safe content migration.
It found two P2 issues and three P3 issues. The graph loader fails on a moved active source; overall diagram coverage was lost; five replay roots and seven task/report links regress; the release-report source recovery section was removed without an adequate replacement.
All 65 deletions and 49 edited relocations received an independent retention/content assessment. Protected sources, prior audits and the 14 canonical report cases remain exact. Both compacted outputs recover byte-for-byte.
The 76 affected tests passed again and workspace validation remains valid; these checks do not cover the reported defects.
The review applied no fixes or further deletion. The authorized corrections below restore affected consumers and retain useful material.

## Correction outcome

The [continuation request](evidence/user-correction-request-20261113.md) authorized these corrections to the reviewed migration.
The [correction ledger](evidence/correction-changes.json) records changed paths, before/after hashes, and recovered source identities.
The original [review](review.md) remains the assessment of `516857d64`; these corrections do not rewrite that historical result.

| Finding | Correction and focused result | Remaining verification limit |
| --- | --- | --- |
| [R1](review.md#r1--p2-repair-the-active-graph-context-before-relocating-its-source) | Rebound the active graph source. The actual default context entry loads all 46 exact retained snapshots. [Consumer checks](evidence/correction-consumers.json), [entry-boundary check](evidence/final-correction-review.json). | Generation stops before repository fingerprints, build subprocesses, and publication. No graph or index was rebuilt. |
| [R2](review.md#r2--p2-retain-useful-diagram-sources-until-an-adequate-replacement-exists) | Restored current [concept](../../ARCHITECTURE.md#workbench-concept) and [SDLC lifecycle](../../ARCHITECTURE.md#full-sdlc-lifecycle) diagrams. Both original editable Draw.io sources recover byte-for-byte. [Coverage and recovery checks](evidence/correction-diagrams.json). | Mermaid received structural and content checks; visual rendering remains unverified. |
| [R3](review.md#r3--p3-preserve-a-usable-replay-procedure-for-relocated-verification-scripts) | Added the [isolated replay procedure](#replay-historical-verification). All five roots resolve correctly there. Timeout and ledger probes pass. [Replay checks](evidence/correction-replay.json). | Coverage, preflight, and graph scripts require their original repositories, assets, and bundles. They were not fully replayed. |
| [R4](review.md#r4--p3-repair-surviving-living-task-and-report-links) | Repaired all seven identified links and 27 timeout-report root links found during final validation. [Link checks](evidence/correction-consumers.json). | Five other missing task links predate the original migration baseline. External URLs and arbitrary historical locators remain outside this result. |
| [R5](review.md#r5--p3-preserve-the-supplied-source-recovery-guidance-before-deleting-the-preparation-guide) | Restored [source recovery instructions](../workbench-release-report-20261024/implementation.md#recover-the-supplied-source). The documented procedure recovers all 44 files with exact inventory hashes. [Recovery check](evidence/correction-source-recovery.json). | Recovery does not establish executable TypeScript, known original package versions, or production behavior. |

The [final correction validation](evidence/correction-validation.json) records 76 affected tests passing and workspace validation with zero findings.
Independent review found no additional actionable defect within the inspected correction scope.
Protected source, audit, canonical-record, historical-script, generated-graph, and sealed migration bytes remain unchanged.
The correction stage deletes no files. Unrelated local changes remain excluded.
No critical conclusions require user attention or action.

## Replay historical verification

Use an isolated checkout at the pre-relocation revision to replay the five historical scripts below.
Their exact bytes and recorded root calculations remain preserved at their task locations. Running them directly there selects the wrong root and can overwrite retained results.
An isolated checkout restores the original directory depth and sends writes to temporary copies of the evidence.
This procedure needs the existing local Git history and an installed Python/Workbench environment; it does not install dependencies or clone business repositories.

Choose a new absolute replay directory outside the current workspace. Replace both placeholders before running:

```sh
git -C /absolute/path/to/current-workbench worktree add --detach /absolute/path/to/new-replay-workspace 79a4104035785b7d8c37e6d424d5d4c888104eee
```

Select an installed Python environment whose runtime source matches the retained verification receipts.
The Python runtime files used by the timeout and ledger probes match this pre-relocation revision during the 13 November correction check. A distribution version alone does not establish that match after later changes.
Use the environment's absolute interpreter path: `.venv/bin/python` on macOS/Linux or `.venv/Scripts/python.exe` on Windows.

| Historical script inside the replay workspace | Required original inputs and result location |
| --- | --- |
| `docs/evidence/dependency-download-timeouts-20261103/probe-timeouts.py` | Local Git revision `b98215fdbb6053e9e5d7c42ea2fb00051cf9102a`; controlled child processes. Writes baseline/candidate JSON beside the temporary script. |
| `docs/evidence/conversation-improvements-implementation-20261030/stage-3/verify-real-ledger.py` | Retained portal browser inventory, Jest results and bindings from the same checkout. Writes derived ledger and case JSON in temporary `stage-3/`. |
| `docs/evidence/conversation-improvements-implementation-20261030/stage-3/verify-real-coverage.py` | Retained assertion map, adjacent `stage-2/` payload and the two business repositories with the exact cited Git objects. Reads repository source; writes temporary coverage and copied source evidence. |
| `docs/evidence/conversation-improvements-implementation-20261030/stage-4/verify_real_cases.py` | The recorded `.workbench/` stack, asset, source map, build result and source checkouts at their original bindings. Uses controlled loopback fixtures and writes temporary case results. |
| `docs/evidence/conversation-improvements-implementation-20261030/stage-6-graph/verify_snapshot_delta.py` | Complete original baseline and candidate graph bundles at their recorded paths. Writes temporary comparisons and a receipt. |

For example, run the original ledger import against the isolated checkout:

```sh
/absolute/path/to/matching-python /absolute/path/to/new-replay-workspace/docs/evidence/conversation-improvements-implementation-20261030/stage-3/verify-real-ledger.py
```

The supplied path determines the historical workspace root, so the command can start from another directory.
Business checkouts and ignored assets are not copied by `git worktree add`. Check the named prerequisites and their hashes before each replay; a missing historical prerequisite remains unavailable and does not justify substituting current data.
Keep resulting case summaries, source identities and consequential failures under the active task before removing the temporary checkout. Do not replace original retained results with replay output.
The five root calculations and the complete timeout and ledger probes are checked in [the correction evidence](evidence/correction-replay.json). Coverage, preflight and graph execution still depend on their separately recorded prerequisites.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks cannot establish complete writing review or business verification.
```
