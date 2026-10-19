---
artifact_kind: test-execution-report
id: EXEC-session-renewal-browser-20261020
version: 1
status: draft
owner: unknown
source_refs:
  - SRC-session-browser-final-manifest-20261020
  - SRC-session-e2e-final-20261020
  - SRC-session-stage-baseline-20261020
related_ids:
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

# Session renewal browser execution

## Run identity and provenance

```yaml
execution_id: native-edge-post-change-20261020
execution_status: PASSED
repository_id: ratan-test-engine
repository_revision: 66595b84e2ed8c78ff1a74f1e1fc0afc856d33af
test_revision: 66595b84e2ed8c78ff1a74f1e1fc0afc856d33af
test_source_sha256: 41d3ee444936039f1ec09cdca12bee8a3fdca5d25d2c5ec741c753e5c43a8b3a
application_repository: mfe-base
application_revision: 4da985a9fa302d7f1ecc04a81b2924b49410ce6a
service_repository: single-ui-bff
service_revision: 85d7cc03eb12710d6facf581987fd4ae24fc9844
environment_identity: local isolated portal root-fast on 127.0.0.1:8103 and BFF fixture on 127.0.0.1:8091
started_at: "2026-10-19T19:04:57Z"
completed_at: "2026-10-19T20:18:38Z"
command_or_tool_reference: .workbench/session-post-change-20261020/browser-runner.mjs
process_exit_status: 0
actual_results: 14 final-source cases passed; two observation cases remain policy-limited.
retained_execution_refs:
  - evidence/post-change-review-20261020/browser-execution/final/manifest.json
```

## Browser environment and suite completeness

- Case inventory: 14 cases; seven original cases and seven added cases.
- Original defect cases: 7; all have final-source result bindings or final long runs.
- Additional cases: 7; all have final-source result bindings or final long runs.
- Target: `http://127.0.0.1:8103/`; protected operation: `/api/auth/v2/sso/validate`.
- Browser: Microsoft Edge `155.0.4283.62`, macOS, fresh native profile, CDP `noDefaults=true`.
- Launch settings: disabled first-run, sync, updater, and background networking; no personal profile.
- Clock: real wall clock. Fast access lifetime is 60 seconds. Fast refresh lifetime is 144 seconds.
- Natural cases use at least 1,800 seconds hidden time. No clock override or page heartbeat runs during that time.
- Controls: real local MFE and BFF. Route holds and transport failures are disclosed test controls.
- Protected assertion: response JSON `result` equals `true`; request token hashes are retained.
- Source integrity: final short cases match test hash `41d3ee...a8b3`. Long final runs started with that hash.
- Missing executions: none.

## Assertions and outcomes

| Test ID | Requirement or criterion | Inspected assertion | Expected result | Actual result | Outcome | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| AC-1 | Continuous mouse activity | `sessionRenewal.cjs:216` | Trusted mouse input renews access. | 144 trusted events; two successful renewals. | PASSED | `browser-execution/final/mouse-final` |
| AC-2 | Continuous keyboard activity | `sessionRenewal.cjs:216` | Trusted keyboard input renews access. | 138 trusted events; two successful renewals. | PASSED | `browser-execution/final/keyboard-final` |
| AC-3 | Continuous scroll activity | `sessionRenewal.cjs:216` | Trusted scroll input renews access. | 145 trusted events; two successful renewals. | PASSED | `browser-execution/final/scroll-final` |
| AC-4 live boundary | `sessionRenewal.cjs:314` | Activity crosses initial refresh expiry without login or prompt. | 186 seconds; 18 renewals; replacement refresh; zero login, navigation, or prompt events. | PASSED | `browser-execution/final/cross-1` |
| TC-01 / AC-5–6 | Pending manual renewal | `sessionRenewal.cjs:290` | Pending prompt stays open; success closes once. | Zero pending closures; one completion closure. | PASSED | `browser-execution/final/pending-fast-001` |
| TC-02 / AC-7 | Failed renewal retry | `sessionRenewal.cjs:297` | Failure preserves retry; later success closes once. | Failed attempt kept prompt open; retry passed. | PASSED | `browser-execution/final/retry-fast-001` |
| TC-03 / TC-06 | Natural background pair | `sessionRenewal.cjs:353` | Hidden and visible controls run after 30 minutes. | 1,800 seconds elapsed; freeze observed; pending prompt closed after valid renewal. | PASSED | `browser-execution/final/natural-edge-final-001` |
| Changed boundary | Slow activity single flight | `sessionRenewal.cjs:416` | Repeated activity shares one pending extension. | 115 events; one pending request; zero cancellations. | PASSED | `browser-execution/final/single-fast-002` |
| Changed boundary | Manual logout cancellation | `sessionRenewal.cjs:466` | Logout cancels renewal and ignores late success. | Request cancelled; access remained cleared. | PASSED | `browser-execution/final/manual-logout-final` |
| Changed boundary | Home unmount cancellation | `sessionRenewal.cjs:498` | Logout unmount cancels activity renewal. | Extension cancelled; access was not restored. | PASSED | `browser-execution/final/activity-logout-final` |
| Changed boundary | Late activity response | `sessionRenewal.cjs:528` | Late activity cannot replace manual success. | Manual token preserved; one prompt closure. | PASSED | `browser-execution/final/late-final` |
| TC-04 | No-refresh background observation | `sessionRenewal.cjs:601` | Record actual outcome without inventing recovery policy. | 1,800 seconds elapsed; no refresh observed; sign-in shown on return; freeze observed. | OBSERVATION_ONLY | `browser-execution/final/missing-edge-final-001` |
| TC-05 | Expired credential denial | `sessionRenewal.cjs:564` | Actual expired credential receives 401 or 403. | Initial validation 200; replay returned 401. | PASSED | `browser-execution/final/expired-fast-001` |
| TC-07 | Workspace descriptor observation | `sessionRenewal.cjs:654` | Compare descriptors after same-user sign-in. | Two workspaces; descriptors and entitlements matched. | OBSERVATION_ONLY | `browser-execution/final/workspace-final` |

The live AC-4 case is a short real-time boundary check.
It does not replace the controlled four-hour AC-4 fixture.
TC-04 and TC-07 record observations because their acceptance policies remain unresolved.

## Retained evidence inventory

| Evidence ID | Locator | Hash or binding | Run identity | Limit |
| --- | --- | --- | --- | --- |
| E-001 | `browser-execution/final/manifest.json` | Contains 14 per-case hashes and artifact paths. | `native-edge-post-change-20261020` | TC-04 and TC-07 remain observation-only. |
| E-002 | `browser-execution/final/*/result-artifacts/result.json` | Sanitized result JSON with token hashes. | Per-case native Edge runs. | No raw credentials or token values retained. |
| E-003 | `browser-execution/final/*/result-artifacts/*.png` | SHA-256 files retained in the evidence tree. | Per-case before, decisive, and after captures. | Screenshots show the local test account UI. |
| E-004 | `stage-baseline.json` | Frozen intake SHA-256 retained. | Post-change stage. | Intake remains unchanged. |

## Browser evidence bindings

The manifest binds each short case to its result JSON and screenshots.
Natural final captures are retained after their 1,800-second windows.
Each result records before and after screenshots, request statuses, lifecycle events, and token hashes.

## Verification conclusion

- Behavior claim: Fourteen final-source browser cases passed in the local portal fixture.
- Covered conditions: Active input, retry, completion, cancellation, stale response, expiry denial, refresh replacement, and natural freeze observation.
- Uncovered conditions: Production deployment, absent-credential recovery policy, and populated application descriptor retention remain outside acceptance.
- Evidence limits: Local services and shortened lifetimes do not establish production behavior or indefinite renewal.

## Facts, inferences, and unresolved questions

- Facts: The native Edge runner recorded real request statuses, lifecycle events, screenshots, and sanitized token hashes.
- Facts: The active final-source cases used MFE commit `4da985a` and BFF commit `85d7cc0`.
- Inferences: The source correction works for the recorded local journeys.
- Unresolved questions: Production settings, absent-credential recovery, and populated application descriptor retention remain open.

## Findings

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| Final natural runs completed. | The complete 14-case inventory has final results. | unknown: session test owner | Review the retained results before release decisions. |
| TC-04 has no approved recovery outcome. | A pass cannot establish expected behavior after refresh failure. | unknown: authentication owner | Approve the recovery policy. |
| TC-07 uses empty workspace descriptors. | Application parameter retention remains unverified. | unknown: workspace owner | Provide two populated descriptors and acceptance criteria. |
| Local deployment identities differ from PROD identities. | Local passes cannot establish release readiness. | unknown: environment owner | Bind deployed frontend, gateway, and BFF revisions. |

## Sources

| Source ID | Locator | Exact revision | Hash | Authority and limit |
| --- | --- | --- | --- | --- |
| SRC-session-browser-final-manifest-20261020 | [Final browser manifest](evidence/post-change-review-20261020/browser-execution/final/manifest.json) | Test `66595b84e2ed8c78ff1a74f1e1fc0afc856d33af`; MFE and BFF above. | Per-case hashes in manifest. | Actual local browser evidence; no PROD claim. |
| SRC-session-e2e-final-20261020 | `repos/testing/ratan-test-engine` session source | `66595b84e2ed8c78ff1a74f1e1fc0afc856d33af` | `41d3ee444936039f1ec09cdca12bee8a3fdca5d25d2c5ec741c753e5c43a8b3a` | Final test source bytes. |
| SRC-session-stage-baseline-20261020 | [Stage baseline](evidence/post-change-review-20261020/stage-baseline.json) | Intake revision `cfcc2be`. | `1650a20f...e0948` | Frozen scope and limits. |
