---
artifact_kind: release-readiness
id: ASSESS-session-refresh-active-cutoff-20261025
version: 1
status: draft
owner: unknown
source_refs:
  - SRC-session-active-cutoff-fix-request-20261024
  - SRC-session-active-cutoff-fix-inputs-20261024
  - SRC-session-release-source-20261022
  - SRC-session-release-coverage-20261022
related_ids:
  - ASSESS-session-refresh-release-20261022
  - DEFECT-portal-background-session-20261019
  - REQ-active-session-renewal
  - CHANGE-session-post-review-20261020
review:
  state: pending
  reviewer: null
  reviewed_at: null
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
    - Automated checks do not check the complete approved dictionary or grammar rules.
---

# MFE Base corrected candidate release confidence

> **Do not promote candidate `ae8213f2963047e7c126d01f4003cee1236abc25` to PROD.**
> Action: correct the failed natural recovery and the remaining session defects, then rerun affected cases.
> Consequence: background recovery can still lose the visible Timeout prompt, and fresh sessions remain exposed to stale responses.
> Owner: unknown application owner; unknown release owner for artifact evidence.
> Evidence: [E2E-07 result](evidence/active-cutoff-fix-20261024/browser/cutoff-natural-20261025T004053/artifacts/result.json), [current comparison](08-active-cutoff-fix-20261024.md), and [prior findings](10-release-confidence.md#findings).

> **Evidence confidence is HIGH for this technical hold.**
> The recommendation is separate from deployment authorization. No deployment authorization or criterion waiver is recorded.

## Release scope and identity

This successor assessment evaluates the corrected issue 1 candidate after the authorized local reruns.
The prior [22 October assessment](10-release-confidence.md) remains historical evidence for the uncorrected candidate.

| Identity | Evidence and limit |
| --- | --- |
| Application | `mfe-base`; candidate commit `ae8213f2963047e7c126d01f4003cee1236abc25`; base `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85`. [Commit binding](evidence/active-cutoff-fix-20261024/commit-binding.json). |
| Changed source | `src/pages/Home/common/useController.ts` and two focused test files. [Source binding](evidence/active-cutoff-fix-20261024/setup/source-binding.json). |
| Test revision | `ratan-test-engine` revision `7a504c13a8d51bb52af5cc89bd4af88d1988da94`; assertion module SHA-256 `94db4519b1d8e2f3669eeea6df59b7a4242300e797f53d28fb2e3152c689e984`. |
| Browser candidate | Edge `156.0.4314.42`; isolated native runs and local BFF fixtures. UAT and PROD parity remain unverified. |
| Build and artifact | No immutable build ID, package digest, deployment identity, or provenance receipt was supplied or found. |
| Target | PROD. Served module identity, effective settings, dependency composition, rollback target, and operators remain unknown. |
| Authorization | No human deployment authorization, criterion waiver, or release exception is recorded. |

## Business impact

The change intends to preserve active portal work across refresh credential expiry.
The corrected boundary case now succeeds in the declared local browser fixture.
Natural background recovery still fails when the Timeout prompt becomes hidden during pending renewal.
The delayed recovery requirement remains a known failure.
Stale-session ownership remains a known failure.

| Journey | Current evidence | Business consequence | Required action |
| --- | --- | --- | --- |
| Active work crosses refresh expiry | [E2E-06 passed](evidence/active-cutoff-fix-20261024/browser/cutoff-cross-20261024T234223/artifacts/result.json); original-Home baseline failed. | The corrected branch preserves the tested active journey. | Confirm the served candidate and retain production-parity evidence. |
| Natural background return | [E2E-07 failed](evidence/active-cutoff-fix-20261024/browser/cutoff-natural-20261025T004053/artifacts/result.json) after 1,800,046 milliseconds. | A user can lose the visible recovery control before renewal completes. | Preserve prompt visibility through actual response delivery, then rerun. |
| Delayed refresh delivery | [Required delayed case](06-test-cases.md#review-delayed-scheduled) remains failed. | Usable late credentials can arrive after logout. | Correct the delayed recovery path or record an approved behavior change. |
| Fresh session after another session ends | [Stale-session findings](10-release-confidence.md#rc-02-stale-responses-can-clear-a-fresh-session) remain unresolved. | A stale response can clear a current session. | Add session ownership checks and verify both delivery orders. |

Affected user counts, financial loss, unsaved-work exposure, and PROD frequency remain unknown.
No unauthorized data access or credential disclosure was demonstrated.

## System impact

The patch changes shared Home expiry reconciliation and authentication state handling.
It affects active and idle paths that consume the shared MFE runtime.
The patch adds no endpoint, dependency, configuration key, or storage contract.
The failed natural case shows a lifecycle and prompt-state interaction that remains unresolved.

| Boundary | Assessment | Required evidence |
| --- | --- | --- |
| Home lifecycle | Issue 1 boundary behavior improves in E2E-06. Natural recovery still fails in E2E-07. | Served source identity and production-parity natural recovery. |
| Embedded consumers | Shared runtime can affect supplied Blotter and Ratan consumers. Static links do not prove deployed usage. | Actual embedded versions and representative integration runs. |
| Authentication deadlines | Local fixtures use shortened and natural test lifetimes. Effective UAT and PROD values remain unknown. | Effective property sources, JWT `exp - iat`, refresh deadlines, and clock agreement. |
| Release composition | Local BFF and test fixtures are separate identities. No deployable bundle is bound. | Build manifest, artifact digest, dependency versions, and deployment receipt. |
| Recovery operations | Rollback, monitoring, stop conditions, and accountable operators remain unbound. | Tested rollback target, smoke checks, alerts, and operator ownership. |

## Evidence assessment

| Dimension | State | Evidence and limit |
| --- | --- | --- |
| Code review | LIMITED | The focused review found no new actionable defect in the selected patch. Its machine outcome remains `INCOMPLETE` because a pre-existing compiler cache is excluded. [Review](evidence/active-cutoff-fix-20261024/review.json). |
| Requirement conformance | FAILED | E2E-06 passes its mapped boundary. E2E-07 fails. Delayed recovery and stale-session requirements remain failed. [Canonical cases](06-test-cases.md#catalog-navigation). |
| Unit and integration tests | PASSED_WITH_LIMITS | Candidate focused execution records 79 runner passes and zero failures. Full Jest records 116 suites and 413 runner passes, including one expected delayed-recovery failure. [Unit report](evidence/active-cutoff-fix-20261024/unit/report.md). |
| Browser execution | FAILED | The final candidate progress has 13 failed cases, 6 passed cases, 1 diagnostic failure, and 2 observations. E2E-07 is a valid failure. E2E-21 is observation-only. [Progress](evidence/active-cutoff-fix-20261024/progress.json). |
| Integrity and traceability | PASSED_WITH_LIMITS | Source and retained artifact hashes bind the candidate. The final validator fails because E2E-21 remains outside the ready locked scope. [Completion gate](evidence/active-cutoff-fix-20261024/browser-completion-gate.json). |
| Deployment evidence | UNKNOWN | No build, artifact, target configuration, rollout, rollback, or operational ownership evidence is bound. |

The final validator status is `FAILED`, with three scope-completeness checks failing.
Those checks preserve the E2E-21 lifecycle limitation and do not invalidate the E2E-07 failure.
The validator does not establish passing business behavior or release approval.

## Readiness conclusion and authorization

```yaml
assistant_assessment:
  assessment_state: COMPLETE
  evidence_confidence: HIGH
  production_recommendation: DO_NOT_RECOMMEND
  scope_basis: Corrected issue 1 candidate with retained local source, unit, browser, and impact evidence.
  business_impact_refs:
    - "#business-impact"
  system_impact_refs:
    - "#system-impact"
  controlling_evidence_refs:
    - evidence/active-cutoff-fix-20261024/browser/cutoff-natural-20261025T004053/artifacts/result.json
    - evidence/active-cutoff-fix-20261024/browser/cutoff-cross-20261024T234223/artifacts/result.json
    - evidence/active-cutoff-fix-20261024/browser-completion-gate.json
    - 10-release-confidence.md#findings
  blocking_action_refs:
    - "#findings"
    - 06-test-cases.md#review-delayed-scheduled
    - 10-release-confidence.md#rc-02-stale-responses-can-clear-a-fresh-session
  residual_risk_refs:
    - evidence/release-confidence-20261022/impact-operations-review.json
    - evidence/active-cutoff-fix-20261024/progress.json
  reassess_when:
    - E2E-07 passes with the required prompt-visibility and recovery assertions.
    - Delayed recovery and stale-session ownership are corrected or explicitly accepted.
    - Immutable build, target, configuration, rollback, and operator evidence is supplied.
readiness_state: pending
readiness_decision: null
reviewer: null
reviewed_at: null
decision_evidence: null
deployment_authorization: null
authorizing_actor: null
authorized_at: null
audit_event_ref: null
```

The technical recommendation is `DO_NOT_RECOMMEND` with `HIGH` evidence confidence.
This recommendation does not authorize deployment and does not record a human decision.

## Findings

### RC-05: Natural background recovery loses the prompt

The fresh E2E-07 run reached the original assertions after 1,800,046 real milliseconds.
The control prompt was hidden while renewal was pending. The required assertion failed.
Owner: unknown application owner. Action: keep the prompt visible until the actual renewal response completes, then rerun E2E-07.

### RC-06: Required delayed recovery remains unmet

The delayed-refresh case remains a known expected failure.
Owner: unknown application owner. Action: correct late credential handling or record an approved behavior change before acceptance.

### RC-07: PROD artifact and operating evidence remain unknown

No immutable build, target configuration, rollback artifact, or accountable operator evidence is bound.
Owner: unknown release owner. Action: provide the release manifest, target identity, effective settings, rollback proof, and operating checks.

## Facts, inferences, and unresolved questions

- Fact: candidate commit `ae8213f2963047e7c126d01f4003cee1236abc25` passes the focused source regression and E2E-06.
- Fact: E2E-07 fails its prompt-visibility assertion after the full natural wait.
- Fact: E2E-21 is observation-only because the native lifecycle scope was interrupted by the Mac lock.
- Inference: deployed users can still experience failed natural recovery when the target shares this runtime and timing condition.
- Unknown: deployed bytes, effective settings, user exposure, occurrence rate, rollback operators, and deployment authorization.

No deployment, push, pull request, or external communication occurred during this assessment.
