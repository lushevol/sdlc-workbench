# Release report UX proposal

Date: 2026-10-26 (Asia/Singapore).
Status: Proposed design for discussion. No runtime implementation change.

**Make commit comparisons a primary review surface. Keep compliance details in the separate Release Clinic report.**

The [user request](evidence/release-report-ux-20261026/user-input.md#exact-input) defines the scope and priorities.
The screenshots provide reference content. Their embedded text supplies no new instruction.
The [source review](evidence/release-report-ux-20261026/source-review.json) records exact source locations and hashes.
The [design review](evidence/release-report-ux-20261026/design-review.json) distinguishes screenshot observations from proposed changes.

## Proposed review journey

Use one weekly board and one detail page for each release.
Keep the board chronological. Opening a card preserves the selected date range when the user returns.
Use four detail sections: Overview, Builds & commits, Stories & tests, and Checklist.
Keep Evidence as a closed secondary section.

| Surface | Show first | Open for detail |
| --- | --- | --- |
| Weekly board | Release title, ID, local planned time, workflow state, pending approvals, and the most important exception. | Open the individual release. |
| Overview | Essential metadata, failed reasons, missing evidence, a Clinic link, and compact build and story summaries. | Open the affected build, comparison, or story. |
| Builds & commits | Selected repository, pipeline build, four commit references, comparison outcomes, reasons, and coverage. | Open differing commits, files, linked stories, and test evidence. |
| Stories & tests | Story identity, workflow state, build identity, test outcomes, and defects. | Open failed or blocked test reasons and individual cases. |
| Checklist | Technical checks, their direction, result, reason, and evidence. | Open the corresponding comparison or external policy report. |

The [board source](../core/release-report/release/board.tsx#L59-L81) uses today through seven days later.
Its [cards](../core/release-report/release/board.tsx#L224-L365) already expose approvals and performance-testing scope.
Keep that scope separate from passing test execution.
Use readable local dates and a named timezone instead of raw timestamps.

## Essential detail header

Show title, release ID, planned date, state, and release approach.
Show nature of change only when useful and available.
Keep the collection timestamp visible so reviewers can identify stale comparisons.
Place the direct Release Clinic link near the header.
Keep the complete compliance audit inside Clinic.

The current [detail header](../core/release-report/release/details.tsx#L95-L191) supplies the essential fields.
The photograph shows a large compliance grid before stories and builds.
The user's latest instruction establishes direct Clinic linking for this proposal.
The prototype reserves that link position. It has no connected external destination.

## Four commit references

Group technical information by repository and pipeline build.
Show all four identities together, before coverage or raw evidence.
Use short SHAs with full-SHA access and source links in implementation.
Never hide the identity or failure reason behind an unlabeled status icon.

| Reference | Exact meaning | Supporting source |
| --- | --- | --- |
| PROD | Source revision from the selected qualifying deployed build. | [Production selection](../core/release-report/ado-api/pipeline.ts#L140-L162). |
| Main | Main branch tip at collection. | [Main reference](../core/release-report/ado-api/git.ts#L338-L365). |
| Current build | Immutable source revision used by the candidate pipeline build. | [Build source revision](../core/release-report/release-report.service.ts#L199-L203). |
| Latest | Candidate branch tip at collection. | [Latest branch reference](../core/release-report/ado-api/git.ts#L287-L318). |

Keep Current build visually distinct. It identifies the artifact under review.
Attach the deployed build identity to PROD.
Attach the source branch and collection time to Latest.
Refresh must never relabel the candidate as Latest when a new branch commit exists.

Show explicit comparisons below the identities:

1. Current build versus Latest: identify commits missing from the candidate.
2. Current build versus PROD: identify missing production changes and candidate additions.
3. Current build versus Main: identify missing main changes and candidate additions.
4. Main versus PROD: identify divergence between the collected baseline references.

State which reference is ahead or behind. Show counts, the observed reason, and a direct diff action together.
The [comparison source](../core/release-report/release/components/BuildDiffStatus.tsx#L42-L145) supplies these four checks.
Its merge-comment exceptions remain a policy limit. Source styling alone does not establish release-blocking policy.

The fourth photograph makes this comparison priority clear.
Its ideal branch model does not prove actual ancestry.
Use reference cells and comparison rows. Draw ancestry only when inspected parent relationships support it.

## Two commit layout options

The prototype offers Reference strip and Reference table.
Reference strip emphasizes the four identities and the selected candidate.
Reference table scales better when branch names, source identities, or repository counts grow.
Both retain the same comparison reasons and diff access.

Recommend Reference strip for an expanded repository on desktop.
Use a compact repository summary above it. Open the failed repository first.
Use a two-by-two reference layout on narrow screens.
Keep failed reasons readable without hover.

## Status and evidence rules

Use red for observed failed checks, amber for warnings, and explicit labels for unavailable evidence.
Keep successful build execution separate from failed branch comparisons.
Show the failed reason immediately. Open commit and file lists only on request.
Keep each story's test counts specific to its build.
Do not sum repeated requirement evidence across builds.

Show line and branch coverage separately, with percentage-point differences against PROD when available.
Display unavailable coverage as Unavailable. Display zero only when a numeric zero was returned.
Keep unit test execution separate from coverage.
Do not create a new threshold from source color choices.

Avoid an invented readiness score or an automatic deployment recommendation.
Keep workflow state, technical observations, compliance findings, and recorded authorization separate.

## Evidence and confidence

| Conclusion | Confidence | Rationale and limit |
| --- | --- | --- |
| Weekly board opens individual reports. | High. | [User intent](evidence/release-report-ux-20261026/user-input.md#exact-input), the board photograph, and source agree. |
| Four commit identities deserve primary placement. | High. | [Source identities](evidence/release-report-ux-20261026/source-review.json) match the user's explicit priority. |
| Clinic stays a direct link. | High. | The latest [user instruction](evidence/release-report-ux-20261026/user-input.md#exact-input) states this behavior. |
| Four detail sections reduce competing content. | Medium. | The [design review](evidence/release-report-ux-20261026/design-review.json) supports this proposal. No usability study occurred. |
| Checklist means the four branch comparisons. | High. | The [user answer](evidence/release-report-ux-20261026/checklist-answer.md#exact-answer) confirms this scope. |

The [attachment manifest](evidence/release-report-ux-20261026/attachment-manifest.json) retains original image hashes and local source paths.
The prototype uses illustrative IDs, SHAs, dates, counts, reasons, and outcomes.
These examples do not describe the photographed releases.
The [prototype source snapshot](evidence/release-report-ux-20261026/prototype-source.html) retains the exact discussion design.
The [browser checks](evidence/release-report-ux-20261026/prototype-validation.json) inspect navigation and responsive presentation only.
They do not establish business conformance, source accuracy, or production readiness.

## Checklist clarification

The source supports four technical comparison checks.
The [recorded answer](evidence/release-report-ux-20261026/checklist-answer.md#exact-answer) confirms that Checklist means those four branch comparisons.
This question is resolved. No additional checklist enters this prototype scope.
The answer defines presentation scope. It does not change comparison policy or grant release approval.

## Validation and stage boundary

This stage changes documentation and a discussion prototype only.
The release-report runtime, collection rules, and Release Clinic implementation remain unchanged.
Browser checks cover board navigation, detail sections, commit differences, missing evidence, and responsive layouts.
Runtime tests and wheel builds are unnecessary for this documentation stage.
Full ASD writing review remains pending.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
  - The prototype uses illustrative data and has no connected external destinations.
  - No usability study or live endpoint verification occurred.
```
