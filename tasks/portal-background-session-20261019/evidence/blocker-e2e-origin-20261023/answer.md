---
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Test evidence for the three release blockers

> **Do not describe all three blockers as exact browser E2E reproductions.**
> Action: retain the test level and environment with each finding.
> Consequence: integration evidence alone does not establish complete browser behavior.
> Owner: Codex for this explanation; unknown application test owner for further verification.
> Evidence: [classification checks](classification.json).

The [user question](user-request.txt) asks whether E2E tests identified the three issues.
All three have executed test evidence. They combine source review, controlled integration tests, and browser probes.
The retained records do not establish the first discovery event for every issue.

| Issue | Browser E2E evidence | Exact reproduction and limits |
| --- | --- | --- |
| Active-session logout at refresh expiry | Related [E2E-06](../../06-test-cases.md#e2e-06) failed. [Result](../minor-branch-rerun-20261020/browser/minor-cross-20261020T142434/artifacts/result.json). Later boundary assertions were not reached. | [REVIEW-F01](../../06-test-cases.md#review-f01) uses controlled Home and Timeout integration. The [run](../code-review-refresh-20261021/lifecycle-candidate-active_cutoff/run.json) invokes Jest. Mock time and adapter responses reproduce logout despite valid access. |
| Old response contaminates a new session | No exact browser reproduction was established in the inspected evidence. Original logout E2E cases cover related cancellation boundaries. | [Before-login](../../06-test-cases.md#review-f03a) and [after-login](../../06-test-cases.md#review-f03b) cases use reducer, interceptor, and service integration. [Run](../code-review-refresh-20261021/races-candidate-f03-after/run.json). HTTP responses and revocation are adapter fixtures. |
| Late refresh leaves Extend disabled | Yes. A [supplemental browser probe](../../06-test-cases.md#probe-delayed-refresh) failed with native Edge and a local BFF fixture. [Result](../minor-branch-rerun-20261020/supplemental/delayed-refresh/result.json). | The driver holds an actual refresh response until access expires. Real wall time passes. Extend remains disabled and logout follows. Controlled integration tests also reproduce the failure. Natural browser freezing remains unproven. |

The exact current-candidate integration runs use MFE revision `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85`.
The supplemental browser run uses MFE revision `6d4c37c839b99d14ea41fd936da1a36cda526b17`.
Its [source binding](../minor-branch-rerun-20261020/supplemental/delayed-refresh/source-binding.json) records separate application, test, and service identities.
The [release assessment](../../10-release-confidence.md#release-scope) records unchanged causal runtime bytes between those MFE revisions.

Some diagnostic runners report `PASSED` because their assertions confirm the adverse behavior.
That runner status does not mean the business requirement passed.
No new business test or application change occurred for this answer.
Owners remain unknown. Further verification must retain exact browser cases, assertions, revisions, and results.
