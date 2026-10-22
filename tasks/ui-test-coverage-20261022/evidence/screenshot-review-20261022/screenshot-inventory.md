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

# Review of repeated step screenshots

> **Critical conclusions: Correct evidence context before audit handoff**
>
> **Image presence does not establish adequate step evidence.**
> Action: Add setup checkpoints, exact timing observations, and browser target identities.
> Consequence: Some timelines cannot show the state described by their step text.
> Owner: Audit harness maintainer. Evidence: The [findings](#confirmed-context-gaps) and [machine inventory](screenshot-inventory.json).
>
> **The canonical CTX-B screenshots for AUTH-116 show CTX-A.**
> Action: Capture the named context and rerun the affected case.
> Consequence: Its current step images cannot establish the CTX-B workspace observation.
> Owner: Audit harness maintainer. Evidence: The [target review](#browser-targets).

## Scope and method

This review uses the immutable [report-002 case ledger](../audit-run-20261022/report-002/case-results.json).
The [machine inventory](screenshot-inventory.json) records its SHA-256 and every inspected image binding.
The review changes no original screenshot, report, canonical definition, or application result.
No application execution ran during this review.

The byte check verifies each original PNG against its recorded SHA-256.
The pixel check decodes PNG files with Playwright's bundled decoder.
It hashes image dimensions and RGBA bytes.
The comparison uses the final bound frame for each step.
This comparison rule cannot select the correct browser target in every case.
The browser-target review below records that limit.

| Checked item | Count |
| --- | ---: |
| Canonical cases | 521 |
| Latest cases with executed steps | 494 |
| Executed canonical steps | 4,478 |
| Bound step frames | 4,555 |
| Unique PNG byte sequences | 1,896 |
| Unique decoded pixel images | 1,896 |
| Cases with repeated step images | 384 |
| Cases with identical images throughout execution | 15 |
| Unchanged action candidates | 135 |
| Cases with unchanged action candidates | 94 |
| Frame hash errors | 0 |

An unchanged action candidate has the same pixels as its preceding step.
Its effective Gherkin type is `When`, including subsequent `And` actions.
The inventory assigns each candidate a source-bound disposition.
It preserves `pixelOnlyDefectClaim: false` for every candidate.
Twenty-one retained test-source snapshots support these dispositions.
Their recorded hashes match their retained bytes.

## Confirmed context gaps

### AUTH-084

The [canonical case](../../test-cases.md#auth-084) contains seven steps.
Steps 1–4 have identical pixels.
Steps 5–7 have another identical pixel image.
Only 34 header-clock pixels differ between these groups.
The dialog pixels remain identical throughout all seven steps.

The [step 1 frame](../audit-run-20261022/application/run-050/cases/auth-084-timeout-refresh-cutoff-17c528533e10-attempt-1/001-step-01.png) already shows the expired-session dialog.
The [step 5 frame](../audit-run-20261022/application/run-050/cases/auth-084-timeout-refresh-cutoff-17c528533e10-attempt-1/005-step-05.png) shows the same dialog after the clock change.
Its header displays minutes, which cannot establish `T+597.999 seconds`.
The retained `sessionSetup` source performs complete expired-session setup during step 1.
Later setup steps assert states that already exist.
The [source bindings and pixel bounds](screenshot-inventory.json) preserve this evidence.

Consequence: The timeline omits separate authentication and expiry setup boundaries.
Owner: Audit harness maintainer.
Next action: Capture those boundaries and bind exact controlled-time observations to each timing step.
The required enabled dialog can correctly remain unchanged before the cutoff.
Do not introduce a visual change to manufacture image differences.

### Browser targets

The static search found two audit cases that create additional browser pages.
They are [AUTH-115](../../test-cases.md#auth-115) and [AUTH-116](../../test-cases.md#auth-116).
The [machine inventory](screenshot-inventory.json) records the search scope and exact retained source bindings.
Both cases use the same URL in their two browser targets.
The URL cannot identify which target supplied a screenshot.

| Case | Retained evidence | Consequence and next action |
| --- | --- | --- |
| [AUTH-115](../../test-cases.md#auth-115) | Explicit TAB-B captures exist for steps 1, 3, and 6–13. Automatic TAB-A captures follow them. | The final frame can identify the wrong tab. Label targets and select each step's intended target. Owner: Audit harness maintainer. |
| [AUTH-116](../../test-cases.md#auth-116) | Steps 8–10 operate or assert CTX-B. Automatic canonical frames capture CTX-A. Step 10 separately attaches a CTX-B image. | The [canonical step 10 image](../audit-run-20261022/application/run-075/cases/auth-116-independent-contexts-preserve-separate-server-sessions-548fb9e4c550-attempt-1/010-step-10.png) shows login while the step describes WS-A. Bind CTX-B explicitly and rerun. Owner: Audit harness maintainer. |

## Disposition of every unchanged action candidate

The [machine inventory](screenshot-inventory.json) contains all 135 individual dispositions and their source references.
The following counts preserve those individual classifications.

| Disposition | Steps | Interpretation |
| --- | ---: | --- |
| Plausible unchanged UI | 22 | Already-empty fields, disabled controls, selected tabs, reload restoration, or already-visible tooltips. |
| Lifecycle or activity event | 52 | Controlled visibility and mouse events need separate state or request observations. |
| Controlled time change | 19 | The exact clock value can change without changing displayed pixels. |
| Service or credential operation | 11 | Requests, responses, and installed credentials can change without a screen change. |
| Persisted state change | 9 | Concurrent database changes intentionally leave a stale dialog unchanged. |
| Existing rendered setup | 12 | Setup already creates the state that the action observes. |
| Accessibility or artifact probe | 4 | Data inspection does not request a visible transition. |
| Focus transition | 1 | DOM focus can move without a visible focus indicator. |
| Expected failure frame | 2 | Failed actions preserve their actual unchanged failure screen. |
| Target selection gap | 2 | Correct TAB-B frames exist before automatic TAB-A frames. |
| Wrong canonical target | 1 | The canonical frame captures CTX-A for a CTX-B action. |
| Total | 135 | Duplicate pixels alone do not establish a defect. |

The failure frames concern [AUTH-098](../../test-cases.md#auth-098) and [UX-030](../../test-cases.md#ux-030).
Their failed actions did not reach later visible states.
Their unchanged screenshots accurately retain those failures.

The [UI-SHL-009](../../test-cases.md#ui-shl-009) tooltip is already visible before its explicit hover step.
The [UX-044](../../test-cases.md#ux-044) hover image also contains its complete tooltip.
Its next image adds asynchronously loaded tenant content.
That later image difference does not establish a missing tooltip capture.
Wait for tenant readiness when a step claims loaded tenant content.

The [UX-017](../../test-cases.md#ux-017) bindings assert focus on record 102 after ArrowDown.
All four images have identical pixels and show no focus indicator.
Consequence: Screenshots alone cannot demonstrate the focus transition.
Owner: Audit harness maintainer.
Next action: Retain active-element observations and assess the intended focus indicator separately.
This evidence does not establish screenshot reuse.

## Identical images throughout a case

These 15 cases have one decoded image across their executed steps.
Their complete status and exact frame bindings remain in the [inventory](screenshot-inventory.json).
The list does not classify them all as failures.

| Group | Cases |
| --- | --- |
| Clock, lifecycle, or credential behavior | [AUTH-050](../../test-cases.md#auth-050), [AUTH-051](../../test-cases.md#auth-051), [AUTH-052](../../test-cases.md#auth-052), [AUTH-053](../../test-cases.md#auth-053), [AUTH-058](../../test-cases.md#auth-058), [AUTH-063](../../test-cases.md#auth-063), [AUTH-071](../../test-cases.md#auth-071), [AUTH-072](../../test-cases.md#auth-072), [AUTH-079](../../test-cases.md#auth-079) |
| Stable workspace or accessibility state | [UI-SHL-011](../../test-cases.md#ui-shl-011), [UI-SHL-026](../../test-cases.md#ui-shl-026), [UX-009](../../test-cases.md#ux-009), [UX-017](../../test-cases.md#ux-017), [UX-021](../../test-cases.md#ux-021) |
| Failed administration case | [BFF-ADM-082](../../test-cases.md#bff-adm-082) |

## Review limits

Nine original frames received direct visual inspection.
The inventory lists their paths, hashes, and case steps.
This sample does not establish visual review of all 4,555 frames.
No duplicate-image count establishes source assertion completeness, business approval, or a passing result.
The historical report's image-presence check remains distinct from this evidence-suitability review.
