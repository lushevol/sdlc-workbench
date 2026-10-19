---
artifact_kind: test-execution-report
id: REPORT-portal-task-evidence-review-20261019
version: 2
status: draft
owner: unknown
source_refs:
  - SRC-task-portal-consolidation-20261019
  - SRC-portal-run001-d1f015546cc4cb277d
  - SRC-portal-run002-06b888608f75bf62a4
  - SRC-browser-final-verification-20261019
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

# Portal issue evidence review

## Run identity and provenance

The retained execution demonstrates automatic logout after a natural Edge tab freeze in a local portal.
It supports a local failure mechanism. It does not establish the cause in PROD.
This report consolidates existing evidence. It records no new portal or browser execution.

```yaml
execution_id: portal-edge-background-001
execution_status: OBSERVED_LOCAL_FAILURE
repository_id: mfe-base
repository_revision: f025513f696476a9cc8162681410cbd21e029bcb
test_revision: null
environment_identity: all-local-portal-edge-run-001
started_at: "2026-10-19T07:49:54.884Z"
completed_at: null
command_or_tool_reference: evidence/manifest.json; retained browser events and original reproduction report
process_exit_status: null
actual_results: Natural freeze, delayed refresh, automatic logout, HTTP 401, and authentication clear
retained_execution_refs:
  - SRC-portal-run001-d1f015546cc4cb277d
  - SRC-portal-run002-06b888608f75bf62a4
related_repository_revisions:
  mfe-root-config: 83091d85beff5306ca0cd643955d8ea6ed0a2d93
  single-ui-bff: 85d7cc03eb12710d6facf581987fd4ae24fc9844
```

The start timestamp identifies observer initialization, not login or service startup.
No final browser-process exit receipt establishes a complete execution end time.
The original portal used Edge `155.0.4283.60` on macOS `26.5` arm64.
The access lifetime was 900 seconds. Login supplied no refresh credential.
External identity, catalog, analytics, database, and toolkit boundaries were synthetic.
The BFF used the inspected controller, JWT, session, and JPA paths with local substitutions.

## Assertions and outcomes

| Test ID | Requirement / criterion | Inspected assertion location | Expected result | Actual result | Outcome | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| OBS-001 | Background lifecycle investigation | Run 001 events 11–14; observer review | Retain hidden, freeze, resume, and visible times | Natural freeze precedes resume; hidden-to-visible interval is 1,865,955 ms | OBSERVED | C-003 |
| OBS-002 | Refresh scheduling mechanism | Home controller snapshot:87–100; event 15 | Record scheduled target and actual callback | Callback runs 1,018,349 ms late, after access expiry | OBSERVED | C-003, C-005 |
| OBS-003 | Missing-refresh timeout mechanism | Timeout controller snapshot:25–41; events 18–20 | Record credential state and selected branch | Missing refresh selects automatic logout before the response | OBSERVED | C-003, C-005 |
| OBS-004 | Expired access rejection | BFF controller snapshot:303–324; browser event 22; server log:205–208 | Record the refresh response and correlation | HTTP 401 `TOKEN_INVALID_EXPIRED` follows the logout selection | OBSERVED | C-003, C-005 |
| OBS-005 | Authentication cleanup | Error handler snapshot:29–31; browser event 23 | Record state after the rejected refresh | `CLEAR` follows HTTP 401 | OBSERVED | C-003, C-005 |
| OBS-006 | Repeat background observation | Run 002 event stream and return accessibility capture | Retain an independent background observation | Background mechanism repeats; return capture contains `Expired Session, please login again.` | OBSERVED_WITH_LIMITS | C-004 |
| REG-001 | REQ-active-session-renewal / AC-5–AC-7 | Proposed scenarios in intake; no executable steps | Eligible pending or failed renewal retains the prompt | No matching retained correction execution | NOT_RUN | C-001, C-006 |
| REG-002 | Proposed saved workspace restoration | Two-descriptor scenario in intake | Restore the same eligible descriptor identifiers and parameters after sign-in | No second-login content comparison | NOT_RUN | C-006, C-007 |
| CONTROL-001 | Foreground and hidden comparison | No matching foreground assertion | Retain equivalent sessions under both visibility conditions | Both runs use background conditions | NOT_RUN | C-003, C-004 |

The observation rows describe existing instrumentation and source checks.
They do not represent passing regressions for corrected behavior.
AC-5 and AC-6 require usable refresh credentials. Run 001 did not have those credentials.
The requirement also treats browser suspension as a separate boundary.

### Existing test coverage

The [source receipt](evidence/source-inspection.json) records exact revisions, locators, and hashes for these checks.
The test review inspected assertions. It executed no tests.

| Source | Inspected assertions | Coverage limit |
| --- | --- | --- |
| MFE Timeout `index.test.tsx:34–89` | Extend and Logout button presence with immediate service responses and synchronous timers | No pending refresh, natural freeze, failure recovery, or authenticated outcome |
| MFE Timeout `index0.test.tsx:33–70` | Button presence and clicks with immediate service responses | Clicks do not establish successful renewal |
| MFE Home `index.test.tsx:196–474` | Home elements, workspace controls, and two Remove elements | No post-login workspace identity or content comparison |
| MFE root model tests and reducer test | Fixed initial states and `CLEAR` on initial state | No populated workspace preservation or reauthentication sequence |
| MFE `common.test.ts:105,353–356` | Cleanup invocation and default, filtered, and eligible workspace lists | No workspace preservation assertion after sign-in |
| BFF controller test `857–932` | Mocked refresh status, result, expiration, and session rejection | Validation and issuance are mocked; no browser or frontend pending-state integration |
| Robot `Tests/workbench/offline.robot:1–16` | Arithmetic results, returned values, and expected assertion failure | Framework smoke explicitly covers no business behavior |
| Robot shared browser launch keyword | Browser type without branded Edge channel | Existing setup does not establish Edge lifecycle fidelity |

MFE assertions use revision `f025513f696476a9cc8162681410cbd21e029bcb`.
BFF assertions use revision `85d7cc03eb12710d6facf581987fd4ae24fc9844`.
Robot assertions use revision `a639c6a92b2f125e2e99a0ca282ad7178e8c2c40`.
The bounded Robot search found no explicit portal freeze, visibility, session-timeout, or renewal scenario.
Its API netting credential helper supplies no browser recovery assertion.
The search scope does not establish universal absence of coverage.

### Corrected evidence interpretation

| Existing evidence | Correction or limit | Consequence |
| --- | --- | --- |
| Causal review `race_order` | Its first two entries reverse the refresh target and later access expiry | Use timestamp fields and the intake chronology |
| Run 001 Sign In capture | Retention metadata describes a pre-scenario capture; post-return phase binding remains unresolved | Do not use it to prove the returned page |
| Run 002 | It is a second background portal | Do not label it a foreground control |
| No Extend event | Automatic logout starts before the refresh response | A brief click window before disabled rendering cannot be excluded |
| Original report test count | The matching original command output is absent | Treat the original successful-test total as unsupported |
| Later Workbench tests | They validate the harness and packaging | They do not repair the earlier missing log or prove portal recovery |
| Workspace loss | The reporter describes loss and rework after sign-in | Local events do not establish restoration failure or unsaved-edit loss |

The earlier report remains unchanged for historical review.
Read it with these corrections and the retained harness review.

### Separate expired-token service fixture

The expired-token service fixture runs separately at `http://127.0.0.1:8089/api/auth`.
It sets access expiry one minute in the past and retains normal controller timeout settings.
Its expired-access refresh and Extend requests receive HTTP 401.
Its relogin request with a valid refresh credential receives HTTP 200 and `result=true`.
The result includes token claims and hashes without raw credentials.

This fixture distinguishes access-based endpoints from the valid-refresh relogin path.
It does not reproduce a natural freeze or verify the browser recovery interface.
Its controlled expiry does not change the natural Run 001 lifetime claim.
The manifest identifies this fixture as C-013.

### Separate browser tooling checks

Final tooling used Playwright `1.64.1`, Node `24.16.0`, and Edge `155.0.4283.62`.
Chromium was `156.0.8078.4`, revision `1248`.
The final record retains Edge, Chromium, and prepared-bundle Chromium smoke results.
It also retains thirteen passing Node regressions and four successful native agent commands.
The prepared bundle installed through offline npm in a new directory.

These results demonstrate local tooling capability on macOS arm64.
The short background smokes use synthetic fixtures and approximately two-second hidden intervals.
They do not repeat the thirty-minute portal incident or prove session recovery.
The original portal browser version differs from the final tooling version.
Native Windows and MCP client registration remain untested.

Earlier failed tooling attempts remain available at their original paths.
The browser setup report links sandbox socket failures and clean-bundle visibility failures.
The final successful smokes do not erase those earlier failures.

## Retained evidence inventory

The [evidence index](evidence/index.md) maps claim IDs to original sources and retained copies.
The [manifest](evidence/manifest.json) records canonical paths, SHA-256 values, and exact source revisions.
The authorized relocation preserves evidence bytes and existing audit events.
The prior source manifest remains archived under task evidence.
Accessibility captures moved with their original bytes. They retain incidental browser metadata.
Archived report copies use `.md.txt` names. Their relative links refer to their original locations.

| Evidence ID | Locator | Hash | Run identity | Integrity or availability limit |
| --- | --- | --- | --- | --- |
| C-001 | [Knowledge and intent](evidence/index.md) | Individual hashes in manifest | requirement v2 and historical designs | Publication review pending; historical refresh durations conflict |
| C-003 | [Run 001](evidence/portal/run-001/browser/browser-events-001.json) | `b62ce8cc5e0fc45dda707a30b3b2c4f73abf88164694bc92630bee606a272193` | portal-edge-background-001 | Synthetic external boundaries and instrumented frontend |
| C-004 | [Run 002](evidence/portal/run-002/browser/browser-events-001.json) | `516512a5fc833446ffb7e310b6b2b863fef4994caa02ec1158a34b7dcde1f172` | local-run-002-2026-10-19 | Another background condition |
| C-008 | [Final browser checks](evidence/browser-final/verification.json) | `8d957fc1bd93766e5c3e438e859d9aa2ce6df9fe343424b8e348815bbec1c04b` | local-validation-2026-10-19 | Tooling checks only |
| C-010 | [Current document checks](evidence/validation.json) | See its file inventory | task-consolidation-2026-10-19 | Documentation and evidence integrity only |

## Verification conclusion

- Behavior claim: The local tab missed scheduled refresh and selected automatic logout with absent refresh state.
- Covered conditions: Natural freeze, expired access, absent refresh credential, local BFF rejection, and authentication clear.
- Uncovered conditions: Matching foreground behavior, usable refresh after suspension, corrected recovery, post-login workspace contents, and PROD parity.
- Evidence limits: No new portal execution occurred. No portal correction or closure is claimed.

The earlier 19 October consolidation passed artifact lint and workspace validation.
Artifact lint retains eight warnings for unknown owners, unresolved content, pending business review, and pending ASD writing review.
Integrity checks matched eighty indexed sources, fifty-seven copies, and seventeen exact-revision source reads.
The checks found no broken local links, malformed tables, or prose sentences above twenty words.
All 492 checked original raw and audit files remain unchanged.
Privacy-pattern checks found no matching secret formats. These patterns cannot detect every secret format.
The [earlier validation record](evidence/validation.json) retains those results and original check outputs.
The [migration report](organization-verification.md) records the later relocation and its validation.
Historical paths resolve through the task relocation map.

The reported incident remains open.
The next correction phase remains `NEEDS_CLARIFICATION`.
`READY_WITH_LIMITS` permits continued intake evidence collection only.
The [intake](intake.md) records open questions, owners, hypotheses, and proposed regressions.

## Facts, inferences, and unresolved questions

- Fact: Existing events establish the local sequence before and after freeze.
- Reported fact: Users repeatedly sign in and report workspace loss and rework.
- Documented intent: Existing sources retain refresh-based renewal after inactivity with applicable credential conditions.
- Inference: The local mechanism could explain the PROD symptom.
- Unknown: Effective PROD revisions, configuration, original lifecycle, and measured impact remain unavailable.
- Unknown: Missing-credential recovery after suspension needs a decision or further source evidence.
- Unknown: No retained post-login comparison establishes the workspace-loss mechanism.

## Findings

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| Local events and exact source snapshots | Automatic logout is explained within local conditions | unknown | Collect paired controls and test credential states |
| AC-5–AC-7 and absent Run 001 refresh state | Recorded renewal intent does not settle every suspension outcome | unknown | Resolve missing-credential recovery before correction handoff |
| No matching foreground run | Visibility comparison remains incomplete | unknown | Retain continuously visible and hidden controls |
| No PROD deployment mapping | The incident cause remains unconfirmed in PROD | unknown | Obtain permitted deployed revisions and effective settings |
| Reported workspace loss without content assertions | Business impact exceeds demonstrated logout behavior | unknown | Compare workspace state before logout and after sign-in |
| Final browser tooling results | Local evidence collection tools are available | unknown | Use isolated profiles and task-local evidence for future investigations |

## Sources

| Source ID | Locator | Exact revision | Hash | Owner, authority, and limits |
| --- | --- | --- | --- | --- |
| SRC-task-portal-consolidation-20261019 | [Task manifest](evidence/manifest.json) and [request](evidence/task-request.txt) | task-consolidation-2026-10-19 | See manifest | Codex; consolidation only; human review pending |
| SRC-portal-run001-d1f015546cc4cb277d | [Run 001 events](evidence/portal/run-001/browser/browser-events-001.json) | local-run-001-2026-10-19 | `b62ce8cc5e0fc45dda707a30b3b2c4f73abf88164694bc92630bee606a272193` | unknown; local instrumentation; no PROD equivalence |
| SRC-portal-run002-06b888608f75bf62a4 | [Run 002 events](evidence/portal/run-002/browser/browser-events-001.json) | local-run-002-2026-10-19 | `516512a5fc833446ffb7e310b6b2b863fef4994caa02ec1158a34b7dcde1f172` | unknown; repeat background condition |
| SRC-browser-final-verification-20261019 | [Final tooling checks](evidence/browser-final/verification.json) | local-validation-2026-10-19 | `8d957fc1bd93766e5c3e438e859d9aa2ce6df9fe343424b8e348815bbec1c04b` | unknown; synthetic tooling checks only |
