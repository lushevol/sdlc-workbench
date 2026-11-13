# Documentation migration review

**Five corrections are required: two P2 findings and three P3 findings. The migration's structural checks passed, but its deletion and consumer review was incomplete. No further deletion or source fix was performed during this review.**

- Source: [latest review request and diagram follow-up](evidence/user-review-request-20261113.md).
- Comparison mode: exact committed range.
- Base: `79a4104035785b7d8c37e6d424d5d4c888104eee`.
- Candidate: `516857d649f5dc557ff58731bb17a09e0308ffce`.
- Scope: deletion/content-loss review, relocated consumers, current documentation and package contracts.
- Excluded: unrelated `core/release-report/`, `core/connectors/yarn.lock`, and the separate ADO skills assessment task.
- Change fingerprint: `5348f9129a3a26c4549a45420107439978a7020506380820a1fd0738eae80100`.

## Findings

### R1 — P2: Repair the active graph context before relocating its source

The active [architecture context](../../relationships/service-dependencies/architecture-context.json#L279) still names `docs/evidence/graph-instruction-integration-20261028/relationship-investigation.json`.
The file moved into its [owning task](../workbench-graph-instruction-integration-20261028/evidence/graph-instruction-integration-20261028/relationship-investigation.json) with identical bytes.
The normal [graph build](../../.agents/skills/service-dependencies-graph/tools/generate_all_graphs.py#L111) loads this context before generation; its loader requires the cited source at the declared path.

Setup: Use the unchanged context and its 46 exact retained source snapshots in a controlled temporary workspace.

1. Call the actual context loader with the baseline source locations.
2. Apply only the committed source relocation and call it again.

Intended result: The existing context remains loadable after a documentation relocation.
Base result: All 46 source snapshots load.
Candidate result: `ValueError: Architecture context source is missing or outside the workspace: docs/evidence/graph-instruction-integration-20261028/relationship-investigation.json`.

Consequence: The default graph generation path cannot load its configured input. This is a Workbench operation failure; business application and production impact are not established.
Owner: Workbench maintainer; human owner is unrecorded.
Correction: Rebind the active context to the exact-byte task destination. Preserve captured historical context and hashes, then check the normal context load and build.
Confidence: High. The paired execution used the real read-only loader; it did not run a complete graph build or business application.
Evidence: [RC-01 and controlled reproduction](evidence/review-consumers.json).

### R2 — P2: Retain useful diagram sources until an adequate replacement exists

The migration removed both root Draw.io files and all four exported Workbench overview diagrams.
The [deletion ledger](evidence/changes.json#L13876) labels the editable sources unreferenced and assigns `ARCHITECTURE.md` as their replacement.
The prior [retention review](../workbench-evidence-retention-review-20261107/evidence/evidence-retention-review-20261107/review.md#L178) explicitly identifies both files as editable design sources with navigation consumers.
The deleted diagram index also records the owner's diagram request as its current consumer.

Setup: Compare the diagram sources and index at the base with the current architecture and workspace design.

1. Inspect the concept and lifecycle views, navigation and stated consumers at the base.
2. Inspect all candidate diagram blocks and their subjects.

Intended result: The stable document series keeps a usable overall SDLC explanation and visual entry point while stale details are updated.
Base result: Editable concept/lifecycle views and their rendered overview were available.
Candidate result: The overall workflow is [text only](../../ARCHITECTURE.md#core-workflow). The remaining [folder data flow](../../docs/WORKSPACE_DESIGN.md#folder-data-flow) and [traceability](../../docs/WORKSPACE_DESIGN.md#traceability) diagrams address narrower subjects.

Consequence: Readers lost the overall visual explanation and editable design material. The user's [diagram follow-up](evidence/user-review-request-20261113.md) demonstrates the missing use.
Owner: Workbench documentation maintainer; human owner is unrecorded.
Correction: Recover the editable material from the base. Update the concept/lifecycle explanation in the existing maintained guide and verify its coverage before retiring old assets. Keep useful historical sources with their task when they remain necessary for recovery or design traceability.
Confidence: High. Source and semantic comparisons establish the missing views; Git recovery does not make a current replacement available.
Evidence: [Deleted-content comparison and prior consumers](evidence/review-deleted-content.json).

### R3 — P3: Preserve a usable replay procedure for relocated verification scripts

Five retained scripts derive their workspace from a fixed `Path(__file__).resolve().parents[...]` depth.
For example, the relocated [timeout probe](../workbench-dependency-download-timeouts-20261103/evidence/dependency-download-timeouts-20261103/probe-timeouts.py#L14) selects `parents[3]`, and the [graph comparison](../workbench-conversation-improvements-20261030/evidence/conversation-improvements-implementation-20261030/stage-6-graph/verify_snapshot_delta.py#L9) selects `parents[4]`.
The additional `tasks/<owner>/evidence/` nesting changes both results to the workspace's `tasks/` directory.

Setup: Use exact committed script bytes and their old and new file locations.

1. Evaluate only each script's root-binding expression.
2. Read the next required timeout-probe source at the derived root without running the full script.

Intended result: Retained reproduction remains usable under its documented prerequisites.
Base result: Root selection identifies the workspace; `core/bootstrap.py` can be read.
Candidate result: All five expressions identify `tasks/`; the timeout source read raises `FileNotFoundError` for `tasks/core/bootstrap.py`.

Consequence: Linked verification/reproduction procedures fail before checking their original assertions. Saved results remain intact.
Owner: Workbench maintainer; human owner is unrecorded.
Correction: Keep hash-bound historical bytes. Add a current replay or temporary reconstruction procedure to the owning record, with correct workspace and input selection, and point reproduction links to it. Verify setup without overwriting retained results.
Confidence: High for root selection and the failed required read. Whole historical scripts were deliberately not executed because several overwrite their retained result files.
Evidence: [RC-02, all five scripts and paired prefix probes](evidence/review-consumers.json).

### R4 — P3: Repair surviving living-task and report links

Seven links regress: six remain unchanged in living task or retained report documents, and one generic-portability report link was rewritten to another removed path.
The [living knowledge question log](../ui-test-coverage-20261022/05-knowledge-questions.md#L1413) cannot open its sole MOM source-review HOLD explanation.
The portal [release assessment](../portal-background-session-20261019/10-release-confidence.md#L191) and [runtime-log supplement](../portal-background-session-20261019/10-runtime-log-pilot.md#L98) also lose direct access to relevant user instructions and clarifications.

Setup: Resolve the seven local targets against each exact committed tree.

1. Open each source link from its base document location.
2. Repeat from the candidate document location and check the mapped task destination.

Intended result: Current task navigation continues to reach its supporting context.
Base result: All seven targets resolve.
Candidate result: All seven targets are missing at the linked locations; their mapped task destinations exist.

Consequence: Readers must search the migration ledger or Git to find authority and unresolved-question context. This is navigation loss, not deletion of the underlying evidence.
Owner: Workbench maintainer; human owner is unrecorded.
Correction: Rebind mutable task/report links. For a deliberately frozen report, provide a nearby current locator companion reachable from its active entry point.
Confidence: High for local target resolution; external URLs and arbitrary historical embedded locators remain outside this claim.
Evidence: [RC-03, seven exact source lines, old/new targets and corrections](evidence/review-consumers.json).

### R5 — P3: Preserve the supplied-source recovery guidance before deleting the preparation guide

Base `docs/RELEASE_REPORT_REPRODUCTION.md`, lines 38–57, contained the only Markdown links to the supplied-source archive and inventory, with instructions for temporary recovery.
The [deletion entry](evidence/changes.json#L211) points only to the canonical test catalog as its replacement.
The retained [implementation report](../workbench-release-report-20261024/implementation.md#L19) still cites `core/release-report/release/details.tsx`, and line 65 states that the supplied TypeScript source is untracked.

Setup: Inspect a fresh candidate Git tree without the unrelated local `core/release-report/` directory.

1. Follow the retained implementation report's supplied-source citation.
2. Search committed Markdown for its archive and inventory recovery instructions.

Intended result: A reviewer can recover the supplied source used by retained implementation and UI analyses.
Base result: The preparation guide identifies the archive, inventory and temporary extraction procedure.
Candidate result: There are no tracked TypeScript source files at the citation and no Markdown references to the archive or inventory. The archive itself remains intact with 44 members.

Consequence: A fresh-checkout reader loses the documented route to reproduce source inspection. The current local untracked directory masks the gap.
Owner: Workbench documentation maintainer; human owner is unrecorded.
Correction: Restore the recovery section in the owning release-report task record and connect the source citations to it. Preserve the original [archive](../workbench-release-report-20261024/evidence/release-report-intake-20261024/supplied-source.tar.gz) and [inventory](../workbench-release-report-20261024/evidence/release-report-intake-20261024/source-inventory.json).
Confidence: High for committed-tree discovery and preserved archive bytes. This is loss of recovery guidance, not loss of the source archive.
Evidence: [Deleted-content semantic comparison and archive checks](evidence/review-deleted-content.json).

## Focused case definitions

These cases specify documentation and tooling conformance. They are not business acceptance criteria or claims of passing business execution.
The baseline and candidate outcomes above remain separate from the intended assertions below.

```gherkin
Feature: Preserve useful documentation and consumers during relocation

  @DOC-REV-01
  Scenario: Load the default architecture context after source relocation
    Given the recorded architecture context and all 46 exact retained source snapshots
    When the context loader reads the context after a source moves into its owning task
    Then all 46 sources load with their recorded hashes

  @DOC-REV-02
  Scenario: Keep an overall SDLC visual explanation available
    Given existing concept and lifecycle diagrams with recorded consumers
    When current documentation replaces outdated diagram details
    Then the maintained guide exposes the overall concept and lifecycle views
    And required editable design material remains available

  @DOC-REV-03
  Scenario: Select the workspace root for retained replay material
    Given a retained verification script at its new task evidence location
    When its documented replay procedure selects the workspace root
    Then the selected root is the workspace directory
    And its required runtime source paths resolve outside the task history

  @DOC-REV-04
  Scenario: Follow current task links after evidence relocation
    Given the seven identified task and report source links
    When a reader opens each link from its current document location
    Then each link resolves to its retained supporting material

  @DOC-REV-05
  Scenario: Recover supplied release-report source in a fresh checkout
    Given a fresh checkout without the untracked TypeScript source directory
    When a reviewer follows the release-report task's supplied-source recovery guidance
    Then the archive and inventory are directly discoverable
    And the documented procedure identifies a temporary extraction location
```

## Checks and limits

The [scope record](evidence/review-scope.json) binds the exact comparison and file dispositions.
The review helper reports 1,144 file records, including 916 exact-byte renames. Edited relocations can appear as separate deletion/addition records.
The sealed ledger identifies 966 planned relocations and 65 deletions; these are different denominators.

| Boundary | Review outcome and evidence |
| --- | --- |
| All 65 deletions | Assessed by original content, consumers, replacement and recovery value. Findings R2 and R5 identify incomplete replacements. [Deleted-content pass](evidence/review-deleted-content.json), [retention pass](evidence/review-retention.json). |
| All 49 edited relocation payloads | Inspected differences: 45 change locator destinations or mapped literal paths; four change gallery/export/recovery descriptions. No additional semantic content-loss finding established. |
| Protected source/audit history | All 225 prior files are byte-identical to baseline. All 558 prior source identities remain; two declared snapshot locators moved and two new sources were appended. |
| Meaningful failures | All 51 inspected retained failure-named payloads remain byte-identical. Two bulky outputs recover byte-for-byte from pinned retained inputs in a different root without Git or business runners. |
| Repeated diagram PNG exports | All 42 removed derivatives retain their original SVG panels, captions and navigation text. The unmatched summary PNG remains. This does not establish equivalence for the separate deleted overview/Draw.io material. |
| Canonical report cases | All 14 original RR/RR-P Gherkin blocks match exactly. The exact recorded release-ID answer remains in returned questions. |
| Active consumers | Paired checks confirm R1, R3 and R4. Frozen source/audit locators are not treated as mutable current configuration. |
| Current ownership and package contracts | No additional actionable defect established in current docs/tasks ownership or scaffold selection. Source-only implementation links retain their declared distribution limits. |

The [fresh review validation](evidence/review-validation.json) records 76 affected tests passing in 5.533 seconds and current workspace validation with zero findings.
The limited added-text pattern scan reports no candidates; binary files and large outputs received separate retention checks.
These passing checks do not cover the missing views, stale graph input, all task links or replay roots.

The graph check used the actual read-only loader and exact retained inputs. It did not run complete graph generation.
Replay probes evaluated root expressions and a required source read; whole scripts were not run because some overwrite retained evidence.
No full runtime suite, live business scenario, external service, native Windows recovery or complete ASD writing review was performed.

## Recommended correction order

1. Repair the active graph-context locator and verify the loader/build boundary.
2. Recover the editable diagram material and maintain the overall visual explanation in its existing guide.
3. Repair current task links and provide usable replay/recovery instructions in the owning records.
4. Recheck all affected consumers and the meaningful content replacement before any further deletion.

Use Git recovery to restore useful material. Keep the stable current series and task-owned history; a full migration rollback is not supported by these findings.
Preserve the sealed ledger and audit as the record of what occurred. Any subsequent correction needs its own truthful change record and affected checks.

## Review outcome

Assessment: Findings present. R1–R5 are open at the reviewed candidate.
Confidence: High within the inspected source, loader and local-path boundaries. No production impact is asserted.
No fixes, deletion, graph publication, external writes or business approvals were performed during review.
The owning maintenance record now links this review so its earlier completion statement cannot be mistaken for a clean semantic review.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not establish a complete writing review or preservation of useful meaning.
```
