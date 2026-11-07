# SDK optimization evidence

> **A transparent migration remains unproved.**
> Action: reconcile the current CES API, grants, and consumer integration before claiming unchanged access.
> Consequence: the SDK upgrade alone cannot establish that claim. Owner: unknown for integration acceptance.
> Evidence: [API follow-up assessment](../10-change-review.md#api-compatibility-follow-up-8-november-2026).

- [User input](user-input.md#exact-user-input): exact optimization request, 7 November 2026. SHA-256: `8a325f427a56e524caa5d6fdca07aa668745caf405828c5c5bf2d2d64dcf0c30`.
- [Frozen intake](../01-intake.md): scope, authority, readiness, and evidence limits.
- [Baseline results](baseline-result.json): 44 tests pass; all source, test, and configuration hashes are retained.
- SDK source: Git `fd9a157e260850b6d9efa10da3223950ea61133a`; parent `b0aa82005e7f14202f85f5ef583f25e42da9eeb3`.
- SDK optimization commit: `0240b1c260337bf3c38f2b5ecaad2d1ec157296d`.
- [Stage review](../10-change-review.md): impact, independent review, coverage, and final disposition.
- [Candidate results](candidate-result.json): matching isolated source; 44 tests pass with zero failures, errors, or skips.
- [Runner failure](candidate-runner-failure.json): zero candidate tests discovered; stale XML reports do not count.
- [Packaging result](packaging-result.json): missing offline formatter dependencies stop the full lifecycle before tests.
- [Optimization document checks](document-checks.json): structure, links, source reconciliation, and evidence inventory at Git `fc1c1e9b0`.
- [Follow-up user question](user-api-compatibility-question-20261108.md#exact-user-input): exact question, 8 November 2026.
- [API assessment data](api-compatibility-20261108.json): 18 request captures, source hashes, role-local matches, and effective-permission differences.
- [Follow-up checks](api-compatibility-checks-20261108.json): document lint, source identity, links, and preserved intake.
- Existing SDK `diff` remains untracked and unchanged: SHA-256 `d632e0b7ff2b8f1e45a7f89aff388ecc8479b6cf21a7e3b660ed09b37de7190e`.
- Unrelated Workbench changes remain outside these commits.
- Retention: compact results, hashes, and exact source locators. Keep routine logs in ignored runtime storage.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
