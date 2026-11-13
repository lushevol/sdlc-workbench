# Workbench living-documentation migration

**The migration is committed. The follow-up review found five open corrections: a stale graph input, missing overview diagrams, broken replay roots, task links and source-recovery guidance.**

- Work type: Workbench maintenance.
- Date: 13 November 2026.
- Owner: agent:codex; human maintenance owner is not recorded.
- Authority: [exact migration and cleanup request](evidence/knowledge-layout-assessment-20261113/user-input.md#documentation-migration-authorization).
- Governing model: [latest living-documentation clarification](evidence/knowledge-layout-assessment-20261113/user-input.md#living-documentation-model-clarification).
- Design: [current reviewed proposal](design.md#stable-document-series-and-incremental-task-history).
- Follow-up: [user review request](evidence/user-review-request-20261113.md) and [migration review](review.md).
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
The review applied no fixes or further deletion. Correction should preserve useful material, restore affected consumers and verify replacement meaning before additional cleanup.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks cannot establish complete writing review or business verification.
```
