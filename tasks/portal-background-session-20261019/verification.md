---
artifact_kind: test-execution-report
id: REPORT-portal-task-evidence-review-20261019
version: 3
status: draft
owner: unknown
source_refs:
  - SRC-portal-run001-d1f015546cc4cb277d
  - SRC-portal-run002-06b888608f75bf62a4
  - SRC-browser-edge-smoke-20261019
related_ids:
  - DEFECT-portal-background-session-20261019
  - REQ-active-session-renewal
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

# Portal evidence verification detail

## Run identity and provenance

This report supplies assertion and capture details for [the issue](intake.md).
It reviews retained evidence. No browser, business service, or business test executes during this cleanup.

| Identity | Retained value |
| --- | --- |
| Natural portal execution | `portal-edge-background-001`; local Edge 155.0.4283.60; macOS 26.5 arm64. |
| MFE | `f025513f696476a9cc8162681410cbd21e029bcb`. |
| Root config | `83091d85beff5306ca0cd643955d8ea6ed0a2d93`. |
| BFF | `85d7cc03eb12710d6facf581987fd4ae24fc9844`. |
| Robot assertion inspection | `a639c6a92b2f125e2e99a0ca282ad7178e8c2c40`. |
| Substitutions | Synthetic identity, catalog, analytics, H2, process keys, and authorized toolkit mock. |
| Observation limit | Instrumented frontend; no matching foreground portal control; no PROD deployment mapping. |

## Assertions and outcomes

| Observation | Exact evidence | Result and limit |
| --- | --- | --- |
| Natural suspension | Run 001 events 11–14. | Hidden → freeze → resume → visible. Hidden interval: 1,865,955 milliseconds. |
| Delayed refresh issuance | Home controller snapshot:87–100; events 10 and 15. | Callback runs 1,018,349 milliseconds late, after access expiry. |
| Automatic logout | Timeout snapshot:25–41; events 18–21. | Missing refresh selects logout at 08:23:06.398Z, before HTTP 401 at .477Z. |
| Authentication clear | Error-handler snapshot:29–31; events 22–23; BFF log:205–208. | Expired-access rejection precedes `CLEAR`. |
| Repeat background observation | Run 002 events and return accessibility text. | Return text includes `Expired Session, please login again.` This is not a foreground control. |
| Eligible renewal correction | REQ-active-session-renewal v2 AC-5–AC-7. | NOT_RUN. No retained corrected execution or closure exists. |
| Workspace restoration | Proposed two-descriptor case in intake. | NOT_RUN. No second-login content comparison exists. |

All event times above are UTC on 19 October 2026.
The historical causal review reverses two timeline entries. Use raw timestamps.
No Extend event establishes user-selected renewal. A brief rendered click window cannot be excluded.
AC-5 and AC-6 require usable refresh credentials. Run 001 starts without those credentials.

### Inspected test assertions

[The source receipt](evidence/source-inspection.json) retains exact revisions, paths, lines, and hashes.
[The test-engine inspection](evidence/browser-setup/test-engine-inspection.json) records the bounded Robot search.

| Inspected source | Assertion scope | Missing coverage |
| --- | --- | --- |
| MFE Timeout `index.test.tsx:34–89` and `index0.test.tsx:33–70` | Buttons and clicks; immediate responses and synchronous timers. | Natural freeze, pending refresh, rejection recovery, and authenticated outcome. |
| MFE Home `index.test.tsx:196–474` | Home elements and workspace controls. | Workspace identity and parameters after reauthentication. |
| Root model, reducers, and `common.test.ts` | Initial states, cleanup invocation, and workspace filtering. | Populated workspace preservation through logout and sign-in. |
| BFF controller tests:857–932 | Mocked validation, issuance, response fields, and session rejection. | Browser integration and real credential-expiry recovery. |
| Robot offline cases and shared browser launch | Arithmetic and framework checks; browser type selection. | Portal lifecycle assertions and explicit branded Edge selection. |

These are inspected assertions, not newly executed tests.
The requirement's isolated pilot uses another MFE revision. Its characterization does not establish this run's recovery behavior.

### Separate service fixture

The retained expired-token fixture runs on port 8089 and deliberately expires access one minute earlier.
Expired-access refresh and Extend return HTTP 401. Valid-refresh relogin returns HTTP 200 with `result=true`.
This fixture distinguishes credential paths. It does not establish natural browser recovery.
[Fixture result](evidence/portal/run-001/expired-fixture/expired-result.json).

## Retained evidence inventory

[The short index](evidence/index.md) highlights useful evidence. [The manifest](evidence/manifest.json) records file hashes and cleanup history.

| Capture | Identity and method | Supported claim and limit |
| --- | --- | --- |
| [Edge smoke screenshot](evidence/browser-final/edge/returned.png) | Playwright 1.64.1; Edge 155.0.4283.62; run 19 October 2026, 14:10:20–14:10:24Z; returned phase. | Shows `Browser control confirmed`. Synthetic tooling smoke, with a 2,033-millisecond hidden interval. |
| [Smoke result](evidence/browser-final/edge/result.json), [snapshot](evidence/browser-final/edge/snapshot.yaml), [trace](evidence/browser-final/edge/trace.zip), and [hash manifest](evidence/browser-final/edge/manifest.json) | Temporary isolated profile; local fixture; click and native visibility assertions. | Preserves the screenshot's execution context. It does not demonstrate portal unit-test execution or the thirty-minute failure. |
| [Portal Sign In image](evidence/portal/run-001/reviews/sign-in-context.jpg) | Existing JPEG; original capture time and phase unresolved. | Shows local Sign In only. No retained binding establishes a post-return capture. |

Related accessibility-capture metadata describes a pre-scenario capture. File modification times cannot establish this image's phase.
No retained screenshot establishes portal unit-test execution.

## Verification conclusion

The retained events and inspected source explain the local failure chain.
PROD causation, missing-credential recovery policy, and reported workspace loss remain unresolved.
The correction and closure remain `NOT_RUN`. The intake's phase gate remains `NEEDS_CLARIFICATION`.
The [current checks](evidence/defect-document-checks-20261020.json) concern documentation, references, and evidence integrity only.

## Facts, inferences, and unresolved questions

- Fact: Run 001 records freeze, delayed issuance, absent refresh, logout selection, HTTP 401, and authentication clear.
- Reported fact: Users describe repeated sign-in, workspace loss, and rework.
- Inference: The demonstrated mechanism could explain the PROD symptom.
- Unknown: Deployed revisions, effective settings, original tab lifecycle, recovery policy, and lost workspace contents remain unavailable.

## Findings

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| Run 001 and exact snapshots | The local mechanism is explained within disclosed substitutions. | unknown | Collect paired controls and resolve missing-credential recovery. |
| No deployment mapping or workspace comparison | PROD causation and workspace loss remain unverified. | unknown | Obtain permitted operational evidence and compare workspace contents. |
| Screenshot result and trace | Browser tooling capture remains traceable. | unknown | Bind future business screenshots to run, time, origin, and phase. |

## Sources

| Source ID | Locator | Revision or hash authority | Limits |
| --- | --- | --- | --- |
| SRC-portal-run001-d1f015546cc4cb277d | [Run 001 events](evidence/portal/run-001/browser/browser-events-001.json) | Local run dated 19 October 2026; SHA-256 in manifest. | Instrumented local observations; owner unknown. |
| SRC-portal-run002-06b888608f75bf62a4 | [Run 002 events](evidence/portal/run-002/browser/browser-events-001.json) | Separate local run dated 19 October 2026; SHA-256 in manifest. | Another background condition; owner unknown. |
| SRC-browser-edge-smoke-20261019 | [Edge result](evidence/browser-final/edge/result.json) | Source revision `d7786150dd35c1668e69974e1afe2918515b8761`; hashes in retained smoke manifest. | Synthetic fixture; owner unknown; no portal behavior verification. |
