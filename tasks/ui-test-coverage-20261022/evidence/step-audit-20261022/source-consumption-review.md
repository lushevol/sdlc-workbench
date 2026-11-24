---
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
    - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Review retained source consumption

> **No further source-driven reruns are required for the final 62 changed-file cases.**
> Action: Retain their exact execution snapshots and [final decisions](source-rerun-decisions-final.json).
> Consequence: Existing failures and prerequisites keep their actual outcomes.
> Owner: Codex harness maintainer.
> Evidence: The [import closures](source-consumption.json), [callback comparisons](source-symbol-review-final.json), and [reviewed differences](source-diff-review-final.json).

## Reviewed scope

The [read-only script](../../../../e2e/scripts/review-source-consumption.mjs) follows transitive local runtime imports from each latest case specification.
It includes audit configuration, reporter entry points, and their local imports.
It excludes type-only imports from runtime reachability.
It records external packages, unresolved dynamic imports, and browser module loads separately.
The script checks retained snapshot hashes before reading their source graphs.
It does not change application source, browser state, database values, snapshots, or test results.

The final review contains 494 in-scope cases and 40 distinct import closures.
All 494 cases have retained attempts, with no active runs.
Imported source bytes match current files for 432 cases.
The remaining 62 cases have changes in six imported specification files.
Their other imported runtime files match the retained source bytes.
These counts describe source reuse, not execution acceptance.

The [first provisional review](source-consumption-provisional-01.json) and [second provisional review](source-consumption-provisional-02.json) preserve earlier states.
The [earlier rerun plan](source-rerun-plan.json) remains historical planning evidence.
Later BFF reruns and the final review supersede its pending actions.

## Exact changed-file cases

| Latest run | Canonical cases | Changed imported files | Decision |
| --- | --- | --- | --- |
| run-050 | [AUTH-029](../../test-cases.md#auth-029), [AUTH-041](../../test-cases.md#auth-041), [AUTH-042](../../test-cases.md#auth-042), [AUTH-140](../../test-cases.md#auth-140), [AUTH-141](../../test-cases.md#auth-141), [AUTH-142](../../test-cases.md#auth-142) | [auth-login-security-expanded.spec.ts](../../../../e2e/audit-specs/auth-login-security-expanded.spec.ts) | AUTH-143 alone changes provider cancellation. AUTH-029 skips every added navigation branch. No source-driven rerun. |
| run-050 | [AUTH-062](../../test-cases.md#auth-062), [AUTH-063](../../test-cases.md#auth-063), [AUTH-093](../../test-cases.md#auth-093), [AUTH-097](../../test-cases.md#auth-097), [AUTH-099](../../test-cases.md#auth-099), [AUTH-104](../../test-cases.md#auth-104), [AUTH-105](../../test-cases.md#auth-105), [AUTH-106](../../test-cases.md#auth-106) | [auth-remaining.spec.ts](../../../../e2e/audit-specs/auth-remaining.spec.ts) | AUTH-098 alone changes the recovery observer. All eight selected callbacks match. No source-driven rerun. |
| run-050 | [AUTH-066](../../test-cases.md#auth-066), [AUTH-112](../../test-cases.md#auth-112), [AUTH-117](../../test-cases.md#auth-117), [AUTH-137](../../test-cases.md#auth-137) | [auth-final.spec.ts](../../../../e2e/audit-specs/auth-final.spec.ts) | AUTH-138 alone changes clock settling. All four selected callbacks match. No source-driven rerun. |
| run-050 | [AUTH-115](../../test-cases.md#auth-115), [UX-036](../../test-cases.md#ux-036) | [additional-boundaries.spec.ts](../../../../e2e/audit-specs/additional-boundaries.spec.ts) | UX-043 alone changes prerequisite disclosure. Both selected callbacks match. No source-driven rerun. |
| run-073 | [KNOW-001](../../test-cases.md#know-001), [KNOW-002](../../test-cases.md#know-002), [KNOW-003](../../test-cases.md#know-003), [KNOW-004](../../test-cases.md#know-004), [KNOW-005](../../test-cases.md#know-005), [KNOW-006](../../test-cases.md#know-006), [KNOW-007](../../test-cases.md#know-007), [KNOW-008](../../test-cases.md#know-008), [KNOW-009](../../test-cases.md#know-009), [KNOW-010](../../test-cases.md#know-010), [KNOW-015](../../test-cases.md#know-015), [KNOW-017](../../test-cases.md#know-017) | [knowledge-current-bff.spec.ts](../../../../e2e/audit-specs/knowledge-current-bff.spec.ts) | KNOW-014 alone adds the prerequisite guard. Twelve other IDs keep equivalent predicates. No source-driven rerun. |
| run-050 | [UX-001](../../test-cases.md#ux-001), [UX-002](../../test-cases.md#ux-002), [UX-003](../../test-cases.md#ux-003), [UX-005](../../test-cases.md#ux-005), [UX-006](../../test-cases.md#ux-006), [UX-007](../../test-cases.md#ux-007), [UX-008](../../test-cases.md#ux-008), [UX-009](../../test-cases.md#ux-009), [UX-010](../../test-cases.md#ux-010), [UX-011](../../test-cases.md#ux-011), [UX-012](../../test-cases.md#ux-012), [UX-013](../../test-cases.md#ux-013), [UX-019](../../test-cases.md#ux-019), [UX-020](../../test-cases.md#ux-020), [UX-023](../../test-cases.md#ux-023), [UX-024](../../test-cases.md#ux-024), [UX-025](../../test-cases.md#ux-025), [UX-026](../../test-cases.md#ux-026), [UX-027](../../test-cases.md#ux-027), [UX-028](../../test-cases.md#ux-028), [UX-037](../../test-cases.md#ux-037), [UX-044](../../test-cases.md#ux-044), [UX-046](../../test-cases.md#ux-046), [UX-048](../../test-cases.md#ux-048), [UX-049](../../test-cases.md#ux-049), [UX-050](../../test-cases.md#ux-050), [UX-063](../../test-cases.md#ux-063), [UX-064](../../test-cases.md#ux-064), [UX-071](../../test-cases.md#ux-071), [UX-072](../../test-cases.md#ux-072) | [ux-shell.spec.ts](../../../../e2e/audit-specs/ux-shell.spec.ts) | UX-004 alone reverses workspace order. Other case branches preserve their fixtures. No source-driven rerun. |

The [callback comparison](source-symbol-review-final.json) records identical callback bytes for 35 selected cases.
Another 27 cases share changed callbacks and require case-conditional review.
The [difference review](source-diff-review-final.json) retains all six exact source differences and their hashes.
The [final decisions](source-rerun-decisions-final.json) record a separate decision for every affected case.
The [knowledge equivalence review](knowledge-blocker-source-equivalence.json) independently records the narrow KNOW-014 prerequisite correction.
No changed imported helper, reporter, or configuration remains in these 62 closures.

AUTH-029 creates additional empty observation arrays before its shared loop.
Every added navigation or cancellation action requires `id==='AUTH-143'`.
Its existing provider destination and navigation remain equivalent.
The added metadata does not establish execution of a real identity provider.

The workspace change allocates the same array before selecting keyboard fixtures.
Only `n===4` reverses its order or records added fixture metadata.
The reviewed keyboard cases use other values.
Their fixture content and executed predicates remain equivalent.
Other responsive and resilience callbacks match exactly.

Every result remains bound to its actual retained source snapshot.
This review does not relabel historical execution as execution of changed whole-file bytes.
The qualitative reuse risk is low for the inspected, unaffected branches.
Existing execution failures require their own behavior investigation.
Their actual outcomes do not improve through this source review.

## Unrelated drift and future review

The reporter snapshots all E2E TypeScript files for each run.
A changed file outside a case's runtime closure does not establish that the case consumed the change.
Each case therefore records imported drift separately from unconsumed drift.
Static import reachability can include unused functions or dormant branches.
The symbol review narrows reruns after this conservative import check.
Regenerate this review after further runtime source changes.

## Frontend failure triage

The [triage ledger](frontend-failure-triage.json) records 51 latest frontend failures or prerequisites before final reruns.
It preserves every actual runner outcome and exact failed-step frame binding.
No assertion or application source changed during this triage.
The following conclusions limit the causes that the failed assertions establish.

### UX-055

Definition: [UX-055](../../test-cases.md#ux-055).
The Reset frame shows Tile Name `Old`.
The dialog title changes to `Undefined ID: 101`.
The locator accepts only new, edit, verify, and deactivate titles.
The failure does not prove that the reset field retained `New`.
The canonical step still requires dialog `edit ID: 101`, so the title mismatch remains an observed failure.

Evidence: [actual result](../audit-run-20261022/application/run-050/cases/ux-055-administration-boundary-with-step-screenshots-643806e944b9-attempt-1/result.json), [failed-step frame](../audit-run-20261022/application/run-050/cases/ux-055-administration-boundary-with-step-screenshots-643806e944b9-attempt-1/005-step-05-failure.png), and [retained assertion](../audit-run-20261022/application/run-050/source-snapshots/e2e/audit-specs/admin-ux.spec.ts#L96).
Result SHA-256: `f133fb918b05dc70caec65db236ed7e14f3be34884e87fd524d9b886b1e0c098`.
Frame SHA-256: `bd589e4f7e01eb008a7f2024a9c6a572825b4715e6e7d3e45edce135793b78e3`.
Assertion source SHA-256: `198cd2b60c7dafc8856c6de69429785ff2a62e1d740a265772cf38ce869bbb3d`.

Owner: unknown for product behavior; Codex harness maintainer for accurate report interpretation.
Next action: Review the exact canonical target and observed predicate before proposing a product change.

### AUTH-137

Definition: [AUTH-137](../../test-cases.md#auth-137).
The visible-control absence assertion passes step 6.
Step 7 searches JSON for the entire store and finds the retained `ENTITY-A App` drawer entry.
That assertion establishes raw store retention.
It does not independently establish unauthorized visible controls or effective catalog access.
Keep the actual failure and this interpretation limit.

Evidence: [actual result](../audit-run-20261022/application/run-050/cases/auth-137-empty-new-login-removes-old-catalog-bfea4de8a187-attempt-1/result.json), [failed-step frame](../audit-run-20261022/application/run-050/cases/auth-137-empty-new-login-removes-old-catalog-bfea4de8a187-attempt-1/007-step-07-failure.png), and [retained assertion](../audit-run-20261022/application/run-050/source-snapshots/e2e/audit-specs/auth-final.spec.ts#L73).
Result SHA-256: `4c644c56a06a47d86aec924d7616559f28885a9a69c88733e8cdd9a5f9834344`.
Frame SHA-256: `bcac5b02e4b7c1dfd8786346ad14f1dcf54b395f64171f22527dc7e587b1e888`.
Assertion source SHA-256: `133a5ec4632074a6d7527c9547510d890f4ede7d1533ab93947176e004455150`.

Owner: unknown for product behavior; Codex harness maintainer for accurate report interpretation.
Next action: Review the exact canonical target and observed predicate before proposing a product change.

### UX-018

Definition: [UX-018](../../test-cases.md#ux-018).
The screenshot visibly shows `Save failed`.
The text assertion passes before the accessibility snapshot returns an empty string.
The failure concerns accessibility-tree exposure, not visual message absence.

Evidence: [actual result](../audit-run-20261022/application/run-050/cases/ux-018-administration-boundary-with-step-screenshots-dc295afc85ad-attempt-1/result.json), [failed-step frame](../audit-run-20261022/application/run-050/cases/ux-018-administration-boundary-with-step-screenshots-dc295afc85ad-attempt-1/003-step-03-failure.png), and [retained assertion](../audit-run-20261022/application/run-050/source-snapshots/e2e/audit-specs/admin-ux.spec.ts#L111).
Result SHA-256: `090c4fa1eaa97b990783c7afdea9d1bd2f2043e565ab19c383c067aee85007f0`.
Frame SHA-256: `c50dca88dd4a4fd4e406fd553e940b56311c6f08226b9b27271280955d5ae6cf`.
Assertion source SHA-256: `198cd2b60c7dafc8856c6de69429785ff2a62e1d740a265772cf38ce869bbb3d`.

Owner: unknown for product behavior; Codex harness maintainer for accurate report interpretation.
Next action: Review the exact canonical target and observed predicate before proposing a product change.

### UX-015

Definition: [UX-015](../../test-cases.md#ux-015).
The verification screenshot shows the dialog and disabled inputs.
The DOM count is 24, while the retained accessibility tree is empty.
The failure concerns accessibility exposure, not absence of disabled controls.

Evidence: [actual result](../audit-run-20261022/application/run-050/cases/ux-015-administration-boundary-with-step-screenshots-1b68bb34e25f-attempt-1/result.json), [failed-step frame](../audit-run-20261022/application/run-050/cases/ux-015-administration-boundary-with-step-screenshots-1b68bb34e25f-attempt-1/003-step-03-failure.png), and [retained assertion](../audit-run-20261022/application/run-050/source-snapshots/e2e/audit-specs/admin-ux.spec.ts#L75).
Result SHA-256: `9fabe2d095dd6f0b2fe7634288c7886609467056af240f886e9cb50d7e87b381`.
Frame SHA-256: `8ef06d460b3cbcaa188eafb810a786d1b82bed407871fb89b01cf9902a657d2d`.
Assertion source SHA-256: `198cd2b60c7dafc8856c6de69429785ff2a62e1d740a265772cf38ce869bbb3d`.

Owner: unknown for product behavior; Codex harness maintainer for accurate report interpretation.
Next action: Review the exact canonical target and observed predicate before proposing a product change.

### UI-RISK-009

Definition: [UI-RISK-009](../../test-cases.md#ui-risk-009).
The global loader intercepts the second Audit click while the first response remains pending.
The later response-ordering steps do not execute.
Do not force a click through the actual loader.
The result establishes the prevented action, not a stale audit response overwrite.

Evidence: [actual result](../audit-run-20261022/application/run-050/cases/ui-risk-009-administration-source-risk-with-live-evidence-2f9989889216-attempt-1/result.json), [failed-step frame](../audit-run-20261022/application/run-050/cases/ui-risk-009-administration-source-risk-with-live-evidence-2f9989889216-attempt-1/004-step-04-failure.png), and [retained assertion](../audit-run-20261022/application/run-050/source-snapshots/e2e/audit-specs/admin-ux.spec.ts#L240).
Result SHA-256: `d795d22465e6c5384ae67e951d910c3a39f725ef65f678db3a825a30a8572610`.
Frame SHA-256: `f5c7f0e0fe93fde241600c8f266f5d9674c8f0142f295256d308aa926cdf2d13`.
Assertion source SHA-256: `198cd2b60c7dafc8856c6de69429785ff2a62e1d740a265772cf38ce869bbb3d`.

Owner: unknown for product behavior; Codex harness maintainer for accurate report interpretation.
Next action: Review the exact canonical target and observed predicate before proposing a product change.

### UX-004

Definition: [UX-004](../../test-cases.md#ux-004).
The [global fixture](../../test-cases.md#L102) explicitly assigns Cashflow workspace index 1.
The earlier harness placed Home first and Cashflow second.
That fixture violated the canonical panel mapping.
Changing the workspace identifier alone did not change its array-based panel index.
The corrected fixture places Cashflow first and focuses Home second before ArrowRight wraps.
Run-077 passes all five unchanged canonical steps.
Keep run-050 and run-076 as failed harness fixture history.
The previous product or definition conflict interpretation is superseded.

Evidence: [latest result](../audit-run-20261022/application/run-077/cases/ux-004-keyboard-and-accessibility-probe-5097a2dd67b6-attempt-1/result.json), [final canonical step frame](../audit-run-20261022/application/run-077/cases/ux-004-keyboard-and-accessibility-probe-5097a2dd67b6-attempt-1/005-step-05.png), and [retained corrected fixture](../audit-run-20261022/application/run-077/source-snapshots/e2e/audit-specs/ux-shell.spec.ts).
Result SHA-256: `5993cebcfa61a19f3ce05e13bec1eb538606abaa40200077eb78e6d53de58936`.
Frame SHA-256: `729207a2f4023b9c8280cda4456813b119455d4bd1531eb73270c57f68dea75d`.
Assertion source SHA-256: `06c3644d14cb3aea5e867e9100bc9f7a3ec127f2e3f805a1d195e966f7cbaeb9`.

Owner: Codex harness maintainer.
Next action: Use run-077 as the latest outcome and retain earlier failed fixtures.

[UX-043](../../test-cases.md#ux-043) remains a separate execution prerequisite.
Its export ran, but native Numbers import did not complete.
The [native investigation](CSVviewer/native-investigation.md) preserves the import boundary.
A CSV parser cannot establish formula evaluation or spreadsheet rendering.
The [current report](current-report.md#remaining-active-prerequisites) records its next action.

## Limits

This source graph does not trace downloaded browser bundles, native runtimes, service binaries, or filesystem reads.
It does not establish production identity integration or deployed configuration equivalence.
Separate migration, build, screenshot, assertion, and execution records support those narrower claims.
A file match alone cannot prove correct assertions or passing behavior.
