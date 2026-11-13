---
artifact_kind: test-execution-report
id: EXEC-session-runtime-log-pilot-20261031
version: 1
status: draft
owner: unknown
source_refs:
  - SRC-runtime-log-user-20261031
  - SRC-runtime-log-plan-20261031
  - SRC-runtime-log-binding-20261031
  - SRC-runtime-log-run-20261031
  - SRC-runtime-log-analysis-20261031
  - SRC-renewal-candidate-v5
related_ids:
  - DEFECT-portal-background-session-20261019
  - REQ-active-session-renewal
  - TEST-session-canonical-20261021
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

# Session renewal runtime log pilot

> **Local pilot: three candidate cases passed all 56 assertions. Runtime log evidence covers five of six planned observations.**
> Action: add request correlation, then exercise the missing stale-renewal response path. Owner: unknown application verification owner.
> Consequence: the pilot cannot establish complete essential-path evidence. See [analysis](evidence/runtime-log-pilot-20261031/analysis.json).
>
> **Remote UAT collection remains NOT_RUN. Local results cannot satisfy the required UAT runtime metric.**
> Action: identify the remote log source, deployment, observation inventory, and access. Owner: unknown UAT verification owner.
> Consequence: remote UAT evidence remains unsupported. See [user instruction](evidence/runtime-log-pilot-20261031/user-input.md#exact-user-input).

| Essential result | Local outcome | Evidence boundary |
| --- | --- | --- |
| Candidate browser cases | 3 passed; 0 failed; 56 passing assertions | Selected local cases only. |
| Runtime log evidence assessed | 5/6 observations, 83.3% | Five of six selected essential paths; no code-coverage claim. |
| Analysis completion | 6/6 observations | The missing path was analyzed as unexercised. |
| Matching runtime behavior | 5/6 observations pass; one remains unverified | Experiment predicates, not complete approved requirement conformance. |
| App event collection | Candidate 192/192; baseline 22/22 | Contiguous sequences; zero parse errors in the selected run. |
| Baseline pending-renewal comparison | Two assertions fail; candidate equivalents pass | Existing early closure reproduced under controlled conditions. |
| Remote UAT runtime evidence | NOT_RUN; N/A denominator | No remote inventory, query, deployment binding, or logs. |

The pilot demonstrates useful separation between passing E2E cases and incomplete runtime-path evidence.
It also exposes an event-matching error: a discarded logout response cannot prove stale-renewal response rejection.
The [historical release assessment](10-release-confidence.md) retains its original source composition, failures, and holds.
This report makes no new full-release recommendation or deployment authorization.

## Run identity and provenance

```yaml
execution_id: runtime-log-pilot-20261031T040919922Z
execution_status: PASSED
repository_id: mfe-base
repository_revision: 66c6411ade58e4d134e381c2baee8ad3f76a8dbf
baseline_revision: f025513f696476a9cc8162681410cbd21e029bcb
test_revision: dd86cb024268e55606d0e7c5b1a5a16193331753765bcfb8ab5827ee38b0bcaf
environment_identity: isolated-local-portal-runtime-log-pilot
source_kind: local_development
started_at: '2026-10-31T04:09:20.055Z'
completed_at: '2026-10-31T04:09:44.606Z'
command_or_tool_reference: evidence/runtime-log-pilot-20261031/run-browser.mjs
process_exit_status: 0
actual_results: evidence/runtime-log-pilot-20261031/runs/2026-10-31T04-09-19-922Z/browser-summary.json
retained_execution_refs:
  - evidence/runtime-log-pilot-20261031/analysis.json
  - evidence/runtime-log-pilot-20261031/local-source-binding.json
  - evidence/runtime-log-pilot-20261031/runs/2026-10-31T04-09-19-922Z/browser-summary.json
uat_execution_status: NOT_RUN
uat_required_observations: null
uat_runtime_evidence_metric: N/A
```

The actual capture window was 12:09:20.055–12:09:44.606 on 31 October 2026, Asia/Singapore.
`execution_status` describes completion of the declared candidate run. The baseline comparison intentionally retains its failures.
The [runner](evidence/runtime-log-pilot-20261031/run-browser.mjs#L95) permits those baseline failures without changing their recorded outcomes.
The earlier [setup failure](evidence/runtime-log-pilot-20261031/setup-attempt-001/result.json) records denied loopback listening and application status NOT_RUN.
The [earlier browser run](evidence/runtime-log-pilot-20261031/runs/2026-10-31T04-07-22-992Z/browser-summary.json) retains its original outcomes.
Only the final run above supplies the current counts.

### Current task state

| Item | Current state |
| --- | --- |
| Task | Existing portal background-session task. |
| Entry route | Bounded exploration using supplied session-renewal implementation and canonical cases. |
| Goal | Check whether essential-path logs explain local renewal outcomes and expose overlooked behavior. |
| Requested metric | Runtime log evidence is a key release-confidence metric during UAT. |
| UAT source rule | Collect UAT logs from remote log systems. Local logs support local development only. |
| Authority | [Exact task input](evidence/runtime-log-pilot-20261031/user-input.md#exact-user-input); [harness reference](../../docs/evidence/runtime-log-verification-20261031/user-followup.md#exact-user-input). |
| Prior results | [Historical assessment](10-release-confidence.md); original failures and holds remain unchanged. |
| Implementation disposition | Isolated archived source with disclosed instrumentation; business checkouts remain unchanged by this pilot. |
| Intent disposition | [Renewal requirement](../../knowledge/records/candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria) remains candidate version 5, with human review pending. |
| Acceptance | No business acceptance, UAT completion, or deployment authorization is established here. |
| Next action | Close the local observation gap, then establish separately authorized remote UAT collection. |

### Exploration boundary

The user authorized local execution to test the runtime-evidence method.
The experiment created task-owned harnesses, instrumented source copies, logs, assertions, and browser captures.
Business checkout edits remain outside this pilot. Session policy, unrelated defects, UAT traffic, and production traffic remain outside scope.
The experiment used existing dependencies and local tools. Substitutions, controlled clocks, shortened lifetimes, and source transformations appear below.

Required evidence includes source revisions, hashes, expected path events, independent assertions, retained logs, screenshots, and per-case outcomes.
Controlled E2E cases and bounded representative usage test local behavior within disclosed boundaries.
The stop condition was retained outcomes for selected paths, or an environment failure preventing further meaningful local execution.
Failures and partial results remain retained. Missing instrumentation and unexercised paths remain separate from application failures.
Results belong in this record and the [task evidence index](evidence/index.md).
Reusable procedure changes belong in Workbench maintenance.

### Named phase readiness

State: READY for the scoped local runtime-log pilot.
Rationale: source inspection, existing canonical cases, and prepared instrumentation defined the permitted observations.
The [observation plan](evidence/runtime-log-pilot-20261031/observation-plan.json) declared six required rows before execution.
The [source binding](evidence/runtime-log-pilot-20261031/local-source-binding.json) identifies frontend revisions and cached fixture classes.
The [instrumentation patch](evidence/runtime-log-pilot-20261031/instrumentation.patch) changes isolated source copies only.
Qualitative risk: medium. Authentication timing and instrumentation can affect the observed flow.
Controlled clocks and synthetic responses follow the selected canonical cases.
The local BFF fixture uses historical classes. It does not execute the current BFF checkout.
Unknown remote log access cannot change this local experiment. It prevents remote UAT verification until suitable evidence exists.
The experiment is complete with one declared path gap. This readiness record does not establish product acceptance.

## Browser environment and suite completeness

- Case inventory: [canonical catalog](06-test-cases.md), version 19, hash `5622dab3b635113ff0137fbf66489f385bbcb11dc4444ec0070f7203d19a7037`.
- Selected cases: [RN-X001](06-test-cases.md#rn-x001), [RN-X002](06-test-cases.md#rn-x002), and [RN-X003](06-test-cases.md#rn-x003).
- Candidate completeness: three selected cases passed; zero failed, errored, skipped, blocked, or unrun cases.
- Baseline completeness: [RN-X002](06-test-cases.md#rn-x002) completed with six passing and two failing assertions.
- Browser: headless Microsoft Edge `156.0.4314.50`; Chromium control through existing Playwright; fresh context per case.
- Profile and viewport: isolated browser contexts; 1150×760. Launch arguments appear in the [run summary](evidence/runtime-log-pilot-20261031/runs/2026-10-31T04-09-19-922Z/browser-summary.json).
- Clock: controlled browser time starts at `2026-10-31T00:00:00Z`; fast-forwarded expiry and logout delays replace wall-clock waiting.
- Representative usage: six scripted failure/retry cycles with three empty workspace descriptors. This is no production-traffic sample.
- Frontend: archived candidate and baseline revisions above; root configuration revision `83091d85beff5306ca0cd643955d8ea6ed0a2d93`.
- BFF: cached classes originally associated with `85d7cc03eb12710d6facf581987fd4ae24fc9844`, plus recorded local fixture overrides.
- Current BFF exclusion: checkout `134a340472f29d2a4136e07e516690de6a18e323` was not executed.
- Authentication substitutions: local fixture login, synthetic access and refresh credentials, controlled 503 responses, and held renewal responses.
- Timing substitutions: synthetic access lasts 60 seconds; synthetic refresh lasts four hours. This is no four-hour soak.
- Toolkit: retained local substitute. Actual portal DOM, React, Axios, reducers, controller, and dialog execute.
- Collection: optional synchronous observers emit structured safe fields. Sequence checks establish local collector completeness within each case.
- Missing branch: [OBS-06](evidence/runtime-log-pilot-20261031/observation-plan.json#L86) remains unexercised and unbound.

The [source binding](evidence/runtime-log-pilot-20261031/local-source-binding.json) records original and instrumented hashes, configuration hashes, and excluded checkout edits.
The [served artifact captures](evidence/runtime-log-pilot-20261031/served-artifact-checks.json) record local bundles and fixture readiness.
Each final result also retains actual lazy-loaded script hashes. The main bundle alone does not contain every instrumentation marker.
The [cleanup record](evidence/runtime-log-pilot-20261031/local-cleanup.json) records termination of owned local process groups.
No native sleep, real identity provider, embedded business data, target deployment, or production parity was tested.

## Assertions and outcomes

| Test ID | Requirement / criterion | Inspected assertion | Expected result | Actual result | Outcome | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| [RN-X001](06-test-cases.md#rn-x001) | [Requirement v5](../../knowledge/records/candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria), [AC-6](../../knowledge/records/candidates/requirements/REQ-active-session-renewal.md#L223), [AC-7](../../knowledge/records/candidates/requirements/REQ-active-session-renewal.md#L230) | [Runner lines 68–76](evidence/runtime-log-pilot-20261031/run-browser.mjs#L68-L76) | Six failures preserve retry and workspaces; six successes install usable changed access and close once. | 44/44 assertions pass; 12 renewal attempts; initial workspace IDs preserved. | PASSED locally | [Result](evidence/runtime-log-pilot-20261031/runs/2026-10-31T04-09-19-922Z/candidate-rn-x001/result.json); [events](evidence/runtime-log-pilot-20261031/runs/2026-10-31T04-09-19-922Z/candidate-rn-x001/application-events.ndjson). |
| [RN-X002](06-test-cases.md#rn-x002) | [AC-5](../../knowledge/records/candidates/requirements/REQ-active-session-renewal.md#L216), [AC-6](../../knowledge/records/candidates/requirements/REQ-active-session-renewal.md#L223), v5 candidate | [Runner lines 77–81](evidence/runtime-log-pilot-20261031/run-browser.mjs#L77-L81) | One request for 25 clicks; prompt stays pending; usable access precedes final closed state. | 8/8 assertions pass; zero pending closures; one successful closure. | PASSED locally | [Candidate result](evidence/runtime-log-pilot-20261031/runs/2026-10-31T04-09-19-922Z/candidate-rn-x002/result.json); [events](evidence/runtime-log-pilot-20261031/runs/2026-10-31T04-09-19-922Z/candidate-rn-x002/application-events.ndjson). |
| [RN-X003](06-test-cases.md#rn-x003) | Proposed security diagnostic; no separate approved AC. | [Runner lines 82–87](evidence/runtime-log-pilot-20261031/run-browser.mjs#L82-L87) | Logout during held renewal leaves final authentication absent. | 4/4 assertions pass; one held request; authentication remains absent. | PASSED for final-state predicates | [Result](evidence/runtime-log-pilot-20261031/runs/2026-10-31T04-09-19-922Z/candidate-rn-x003/result.json); [events](evidence/runtime-log-pilot-20261031/runs/2026-10-31T04-09-19-922Z/candidate-rn-x003/application-events.ndjson). Stale renewal-response handling remains unverified. |
| [RN-X002 baseline](06-test-cases.md#rn-x002) | Same [AC-5](../../knowledge/records/candidates/requirements/REQ-active-session-renewal.md#L216) pending predicate and controlled case. | [Same runner](evidence/runtime-log-pilot-20261031/run-browser.mjs#L77-L81) | Prompt stays visible with zero closures while response is held. | Prompt is absent; one closure occurs before response release. Six assertions pass; two fail. | FAILED baseline comparison | [Baseline result](evidence/runtime-log-pilot-20261031/runs/2026-10-31T04-09-19-922Z/baseline-rn-x002/result.json); [events](evidence/runtime-log-pilot-20261031/runs/2026-10-31T04-09-19-922Z/baseline-rn-x002/application-events.ndjson). |

### Old and candidate behavior comparison

Setup: use the isolated portal with controlled time, three workspaces, and one held renewal response.

1. Reach access expiry.
2. Send 25 click events to Extend.
3. Inspect the pending dialog and closure count.
4. Release one valid synthetic renewal response.
5. Inspect installed access, final dialog state, and workspace identities.

Intended result: the prompt stays visible before renewal succeeds, then closes exactly once after completion.
Old result: the prompt closes while the response remains held. The baseline close request is sequence 18; response receipt is 19.
Candidate result: zero pending closures occur. Response receipt is sequence 18; renewal success is 20; close request is 21.
The token reducer event is sequence 23. Independent token, pending-dialog, and final-DOM assertions pass.

React dispatch batching explains why a reducer event can follow the close request.
That event order does not establish early visible closure. The pilot records no new candidate defect from this sequence.
The [analysis](evidence/runtime-log-pilot-20261031/analysis.json) binds both sequences to their original results and logs.

### Runtime observation results

| Observation definition | Essential path and mode | Acquired / bound / analyzed / assessed | Behavior result | Limit |
| --- | --- | --- | --- | --- |
| [OBS-01](evidence/runtime-log-pilot-20261031/observation-plan.json#L7) | Manual renewal pending; E2E. | yes / yes / yes / yes | PASSED | Local synthetic renewal only. |
| [OBS-02](evidence/runtime-log-pilot-20261031/observation-plan.json#L22) | Manual renewal success; E2E. | yes / yes / yes / yes | PASSED | React event ordering needs independent state assertions. |
| [OBS-03](evidence/runtime-log-pilot-20261031/observation-plan.json#L39) | Renewal failure and retry; representative usage. | yes / yes / yes / yes | PASSED | Six scripted cycles, not broad traffic. |
| [OBS-04](evidence/runtime-log-pilot-20261031/observation-plan.json#L54) | Repeated renewal success; representative usage. | yes / yes / yes / yes | PASSED | Three empty workspace descriptors. |
| [OBS-05](evidence/runtime-log-pilot-20261031/observation-plan.json#L70) | Logout during renewal; E2E diagnostic. | yes / yes / yes / yes | PASSED final state | No approved security AC is supplied. |
| [OBS-06](evidence/runtime-log-pilot-20261031/observation-plan.json#L86) | Stale-renewal response handler; E2E diagnostic. | no / no / yes / no | NOT_VERIFIED | Relogin was canceled. The logout discard event also lacks required request-path correlation. |

The [candidate logout log](evidence/runtime-log-pilot-20261031/runs/2026-10-31T04-09-19-922Z/candidate-rn-x003/application-events.ndjson#L22) records canceled relogin.
Its [response boundary](evidence/runtime-log-pilot-20261031/runs/2026-10-31T04-09-19-922Z/candidate-rn-x003/application-events.ndjson#L28-L29) associates the discarded event with logout.
Matching the name `auth.response.discarded` alone would falsely count the stale-renewal path.
The [discard instrumentation](evidence/runtime-log-pilot-20261031/instrumentation.patch#L48) records an abort flag without the request path.
The [analyzer](evidence/runtime-log-pilot-20261031/analyze.py#L43-L45) requires that path before it can qualify renewal evidence.
A future run needs request correlation and actual stale-renewal delivery. The current observer cannot qualify this row alone.
The [collector negative control](evidence/runtime-log-pilot-20261031/collector-negative-control.json) removes one event from a synthetic copy.
The altered collection is rejected, and assessed observations fall from five to three. Original evidence remains unchanged.

## Coverage inventories and summary

Intent inventory: [requirement v5](../../knowledge/records/candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria), hash `3db69ca6827b4afa0eb9f3182f15045f80dac012f9d37004d62144740424c359`.
All seven ACs remain candidate definitions with human review pending.
The pilot selects only local predicates from [AC-5](../../knowledge/records/candidates/requirements/REQ-active-session-renewal.md#L216), [AC-6](../../knowledge/records/candidates/requirements/REQ-active-session-renewal.md#L223), and [AC-7](../../knowledge/records/candidates/requirements/REQ-active-session-renewal.md#L230).
The other four ACs and their wider existing evidence are outside this pilot.
The [RN-X003](06-test-cases.md#rn-x003) security diagnostic supplies no approved additional criterion.

Test inventory: three canonical browser cases and six planned observation rows.
The [runner](evidence/runtime-log-pilot-20261031/run-browser.mjs) has hash `dd86cb024268e55606d0e7c5b1a5a16193331753765bcfb8ab5827ee38b0bcaf`.
Change inventory: zero business implementation changes in this pilot.
The selected candidate predates this experiment. Instrumentation modifies isolated execution copies only.
No complete business-change inventory is reconstructed from the baseline comparison.

| Metric | Qualified / total | Percentage | Gap or limit | Evidence |
| --- | --- | --- | --- | --- |
| Experiment observation definitions | 6/6 | 100% of declared local rows | This does not establish approved product definitions. | [Plan](evidence/runtime-log-pilot-20261031/observation-plan.json). |
| Log acquisition | 5/6 | 83.3% | Stale-renewal handler is unexercised. | [Analysis](evidence/runtime-log-pilot-20261031/analysis.json). |
| Candidate and run binding | 5/6 | 83.3% | Same unbound observation. | [Analysis](evidence/runtime-log-pilot-20261031/analysis.json). |
| Analysis completion | 6/6 | 100% of declared local rows | Includes the recorded unexercised-path disposition. | [Analysis](evidence/runtime-log-pilot-20261031/analysis.json). |
| Runtime log evidence assessed | 5/6 | 83.3% | Intersection of qualified local rows, not an average. | [Analysis](evidence/runtime-log-pilot-20261031/analysis.json). |
| Matching passing runtime behavior | 5/6 | 83.3% | One observation remains unverified. | [Results](evidence/runtime-log-pilot-20261031/runs/2026-10-31T04-09-19-922Z/browser-summary.json). |
| Selected unique essential paths | 5/6 | 83.3% | This plan has one distinct path per row. No line or branch denominator exists. | [Plan](evidence/runtime-log-pilot-20261031/observation-plan.json). |
| Selected local AC predicates to definitions / assertions / passing execution | 3/3 for each relationship | 100% within selected local predicates | Full seven-AC conformance remains NOT_ASSESSED. | [Matrices below](#ac-to-test-case-coverage). |
| Full requirement conformance | NOT_ASSESSED | N/A | Complete predicates and environments were not reassessed. | [Candidate requirement](../../knowledge/records/candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria). |
| AC to business code changes | N/A; zero pilot changes | N/A | Required unchanged implementation appears below. | [Source binding](evidence/runtime-log-pilot-20261031/local-source-binding.json). |
| Business code changes to tests | N/A; zero pilot changes | N/A | No changed-business-unit denominator exists. | [Source binding](evidence/runtime-log-pilot-20261031/local-source-binding.json). |
| Remote UAT runtime evidence | NOT_RUN; inventory unknown | N/A | Local observations cannot populate this denominator. | [UAT status](evidence/runtime-log-pilot-20261031/analysis.json). |

### AC to test case coverage

| Criterion and version | Selected predicate | Canonical case | Inspected assertion | Local passing execution | Limit |
| --- | --- | --- | --- | --- | --- |
| [AC-5](../../knowledge/records/candidates/requirements/REQ-active-session-renewal.md#L216), candidate v5 | Zero successful closures while renewal is pending. | [RN-X002](06-test-cases.md#rn-x002). | [Pending assertions](evidence/runtime-log-pilot-20261031/run-browser.mjs#L78-L79). | [Candidate result](evidence/runtime-log-pilot-20261031/runs/2026-10-31T04-09-19-922Z/candidate-rn-x002/result.json). | Three empty workspaces and held synthetic response. |
| [AC-6](../../knowledge/records/candidates/requirements/REQ-active-session-renewal.md#L223), candidate v5 | Install usable access and close exactly once after success. | [RN-X001](06-test-cases.md#rn-x001); [RN-X002](06-test-cases.md#rn-x002). | [Cycle assertions](evidence/runtime-log-pilot-20261031/run-browser.mjs#L72-L76); [held-success assertions](evidence/runtime-log-pilot-20261031/run-browser.mjs#L80-L81). | [Cycle result](evidence/runtime-log-pilot-20261031/runs/2026-10-31T04-09-19-922Z/candidate-rn-x001/result.json); [held-success result](evidence/runtime-log-pilot-20261031/runs/2026-10-31T04-09-19-922Z/candidate-rn-x002/result.json). | Local timing and synthetic credentials. |
| [AC-7](../../knowledge/records/candidates/requirements/REQ-active-session-renewal.md#L230), candidate v5 | Failure leaves the prompt and permits retry. | [RN-X001](06-test-cases.md#rn-x001). | [Failure and retry assertions](evidence/runtime-log-pilot-20261031/run-browser.mjs#L69-L74). | [Cycle result](evidence/runtime-log-pilot-20261031/runs/2026-10-31T04-09-19-922Z/candidate-rn-x001/result.json). | Exactly six controlled 503 failures. |
| [AC-1](../../knowledge/records/candidates/requirements/REQ-active-session-renewal.md#L187), [AC-2](../../knowledge/records/candidates/requirements/REQ-active-session-renewal.md#L194), [AC-3](../../knowledge/records/candidates/requirements/REQ-active-session-renewal.md#L201), [AC-4](../../knowledge/records/candidates/requirements/REQ-active-session-renewal.md#L208), candidate v5 | Activity and duration predicates. | Existing catalog remains authoritative. | Not inspected for this pilot. | NOT_RUN in this pilot. | Outside selected local predicates; historical evidence remains separate. |

### AC to code change coverage

All source links below identify retained candidate bytes at `66c6411ade58e4d134e381c2baee8ad3f76a8dbf`.
The [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json) records exact hashes and source identities.
`UNCHANGED` means this pilot made no business implementation change. It does not mean baseline and candidate are identical.

| Criterion | Intended predicate | Pilot change classification | Inspected source | Local conformance limit |
| --- | --- | --- | --- | --- |
| [AC-5](../../knowledge/records/candidates/requirements/REQ-active-session-renewal.md#L216) | Keep the pending prompt visible. | UNCHANGED required implementation. | [Dialog pending guard](evidence/comprehensive-renewal-20261028/sources/c30ed46d9ea5/useController.ts#L131-L147); [returned renewal promise](evidence/comprehensive-renewal-20261028/sources/12f895009ad5/index.ts#L107-L121). | Selected pending predicate matches source and retained local execution. |
| [AC-6](../../knowledge/records/candidates/requirements/REQ-active-session-renewal.md#L223) | Accept usable renewal and close once. | UNCHANGED required implementation. | [Usable access validation](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L48-L73); [close after awaited renewal](evidence/comprehensive-renewal-20261028/sources/c30ed46d9ea5/useController.ts#L138-L147). | Synthetic token validity and observed DOM only; no real provider verification. |
| [AC-7](../../knowledge/records/candidates/requirements/REQ-active-session-renewal.md#L230) | Preserve retry after failure. | UNCHANGED required implementation. | [Failure and settlement](evidence/comprehensive-renewal-20261028/sources/c30ed46d9ea5/useController.ts#L148-L154). | Six controlled failures pass; broader failure inventory remains outside scope. |
| Proposed security diagnostic. | Logout invalidates ownership and prevents restoration. | UNCHANGED supporting boundary. | [Logout abort and epoch guard](evidence/comprehensive-renewal-20261028/sources/c30ed46d9ea5/useController.ts#L113-L128); [session epoch](evidence/comprehensive-renewal-20261028/sources/b524186ae494/sessionEpoch.ts#L8-L18); [response guard](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L35-L44). | Final authentication is absent; stale-renewal response branch remains unexercised. |

### Code change to test case coverage

Business changes introduced by this pilot: zero. Changed-business-unit assertion and passing-execution metrics are N/A.
The comparison uses the recorded baseline and candidate revisions. It does not redefine their complete historical change inventory.
The following supporting changes belong to the experiment and have separate purposes.

| Supporting change | Rationale | Affected observation | Canonical case | Assertion or validation | Retained result and limit |
| --- | --- | --- | --- | --- | --- |
| [Instrumentation patch](evidence/runtime-log-pilot-20261031/instrumentation.patch) | Observe essential paths in isolated archived copies. | Six planned rows; eight candidate files and seven baseline files. | [RN-X001](06-test-cases.md#rn-x001); [RN-X002](06-test-cases.md#rn-x002); [RN-X003](06-test-cases.md#rn-x003). | [Anchor and parser checks](evidence/runtime-log-pilot-20261031/preparation-checks.json); [runner outcomes](evidence/runtime-log-pilot-20261031/run-browser.mjs#L68-L91). | [Source binding](evidence/runtime-log-pilot-20261031/local-source-binding.json); [final results](evidence/runtime-log-pilot-20261031/runs/2026-10-31T04-09-19-922Z/browser-summary.json). Instrumentation may affect timing. |
| [Browser runner](evidence/runtime-log-pilot-20261031/run-browser.mjs) | Collect safe events beside independent DOM, token, and workspace assertions. | Candidate and baseline case runs. | [RN-X001](06-test-cases.md#rn-x001); [RN-X002](06-test-cases.md#rn-x002); [RN-X003](06-test-cases.md#rn-x003). | [Assertions](evidence/runtime-log-pilot-20261031/run-browser.mjs#L68-L87); [collector checks](evidence/runtime-log-pilot-20261031/run-browser.mjs#L91). | [Final summary](evidence/runtime-log-pilot-20261031/runs/2026-10-31T04-09-19-922Z/browser-summary.json). No remote collector runs. |
| [Analysis script](evidence/runtime-log-pilot-20261031/analyze.py) | Qualify per-row acquisition, binding, analysis, and passing behavior. | Six required rows. | Existing cases above supply execution evidence. | [Negative collection control](evidence/runtime-log-pilot-20261031/collector-negative-control.json). | [Analysis](evidence/runtime-log-pilot-20261031/analysis.json). Event names alone do not establish path coverage. |

## Retained evidence inventory

Hashes below identify current retained bytes. Each result also includes individual screenshot hashes and collection counts.

| Evidence ID | Locator | SHA-256 | Run identity | Integrity or availability limit |
| --- | --- | --- | --- | --- |
| E-PLAN | [observation-plan.json](evidence/runtime-log-pilot-20261031/observation-plan.json) | `700ea10096240f4790fd42ca0c998cf76fb58bcd850d56df1d641349edc2dbef` | pilot support | Declared local inventory. |
| E-BIND | [local-source-binding.json](evidence/runtime-log-pilot-20261031/local-source-binding.json) | `d988958c2e24e28dccdad91647a6212624304d95e846bd3e2822958d925a3206` | pilot support | Original and transformed source hashes. |
| E-PATCH | [instrumentation.patch](evidence/runtime-log-pilot-20261031/instrumentation.patch) | `4db0b54da92faba11a85de8a8c967101da38dcdacf70a234dfaa3c6938f60f64` | pilot support | Isolated logging transformations only. |
| E-RUNNER | [run-browser.mjs](evidence/runtime-log-pilot-20261031/run-browser.mjs) | `dd86cb024268e55606d0e7c5b1a5a16193331753765bcfb8ab5827ee38b0bcaf` | pilot support | Exact inspected assertion and collector source. |
| E-ANALYSIS | [analysis.json](evidence/runtime-log-pilot-20261031/analysis.json) | `5bcae35ded3907c7bf0639eee22c4d12df7742ba436cfe4faa99c69746516d6b` | pilot support | Derived analysis; original evidence retained. |
| E-SUMMARY | [runs/2026-10-31T04-09-19-922Z/browser-summary.json](evidence/runtime-log-pilot-20261031/runs/2026-10-31T04-09-19-922Z/browser-summary.json) | `433d4abd553932cb0ad410dc34cc2d689d67d0ad40e08dfaaf739ded16cc1287` | final local run | Final run only. |
| E-X001 | [runs/2026-10-31T04-09-19-922Z/candidate-rn-x001/result.json](evidence/runtime-log-pilot-20261031/runs/2026-10-31T04-09-19-922Z/candidate-rn-x001/result.json) | `cd54db3ebd7774606e39187c5ab48561f4fb0ac9c66791ceb7a9b993ecc0c6d7` | final local run | 44 passing candidate assertions. |
| E-X001-LOG | [runs/2026-10-31T04-09-19-922Z/candidate-rn-x001/application-events.ndjson](evidence/runtime-log-pilot-20261031/runs/2026-10-31T04-09-19-922Z/candidate-rn-x001/application-events.ndjson) | `355be570647d054bef68db3e69fb71252c6c03453d03e5e06271405ab44da763` | final local run | 138 contiguous events. |
| E-X002 | [runs/2026-10-31T04-09-19-922Z/candidate-rn-x002/result.json](evidence/runtime-log-pilot-20261031/runs/2026-10-31T04-09-19-922Z/candidate-rn-x002/result.json) | `0cba3c51ed1f17b561a470e61d6e01cfd55626d098429e27c6d28050e3b4f48a` | final local run | 8 passing candidate assertions. |
| E-X002-LOG | [runs/2026-10-31T04-09-19-922Z/candidate-rn-x002/application-events.ndjson](evidence/runtime-log-pilot-20261031/runs/2026-10-31T04-09-19-922Z/candidate-rn-x002/application-events.ndjson) | `4382a9da4ffdc8b984f8938aec63246b2855a61b878eb7865ec232c82ccee011` | final local run | 25 contiguous events. |
| E-X003 | [runs/2026-10-31T04-09-19-922Z/candidate-rn-x003/result.json](evidence/runtime-log-pilot-20261031/runs/2026-10-31T04-09-19-922Z/candidate-rn-x003/result.json) | `9feed413099fdc330ea48138d0c3eb89861660ad38cac81130aae861747f6565` | final local run | 4 passing candidate assertions; stale-renewal branch unexercised. |
| E-X003-LOG | [runs/2026-10-31T04-09-19-922Z/candidate-rn-x003/application-events.ndjson](evidence/runtime-log-pilot-20261031/runs/2026-10-31T04-09-19-922Z/candidate-rn-x003/application-events.ndjson) | `0a0d9a6791d99dc60cb0897c11a5cae721dc605048710d519cd31e01eea36db9` | final local run | 29 contiguous events; logout discard is not renewal discard. |
| E-BASELINE | [runs/2026-10-31T04-09-19-922Z/baseline-rn-x002/result.json](evidence/runtime-log-pilot-20261031/runs/2026-10-31T04-09-19-922Z/baseline-rn-x002/result.json) | `e79c0fb38c1b49990e98f19628eb6d95c0e6d26abe65bf828dd31f823a3b588d` | final local run | 6 passing and 2 failing assertions. |
| E-BASELINE-LOG | [runs/2026-10-31T04-09-19-922Z/baseline-rn-x002/application-events.ndjson](evidence/runtime-log-pilot-20261031/runs/2026-10-31T04-09-19-922Z/baseline-rn-x002/application-events.ndjson) | `15365c384a9d12292312fc2590bca200b421d95526b7b55a81951d45da5d0eed` | final local run | 22 contiguous events. |
| E-COLLECTOR-CONTROL | [collector-negative-control.json](evidence/runtime-log-pilot-20261031/collector-negative-control.json) | `deac487e8f32ca78626b57b2f528d9524eda4c6fc7a69f2102811cfd9db0e148` | pilot support | Synthetic altered copy; original logs unchanged. |

The [source binding](evidence/runtime-log-pilot-20261031/local-source-binding.json) retains original/instrumented source hashes and fixture class hashes.
The [historical source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json) retains candidate source snapshots without copying them here.
The [initial discussion](../../docs/evidence/runtime-log-verification-20261031/discussion.md) and [selected observation modes](../../docs/evidence/runtime-log-verification-20261031/user-clarification.md#exact-user-answer) preserve earlier context.

## Browser evidence bindings

These are actual Playwright captures from the final run. Wall-clock times below use Asia/Singapore.
The browser clock is controlled. Screenshots corroborate visible state; result assertions establish token and workspace predicates.

| Case and step | Capture time and phase | Screenshot | SHA-256 | Assertion or event evidence | Supported claim and limit |
| --- | --- | --- | --- | --- | --- |
| [RN-X002](06-test-cases.md#rn-x002), start-before-renewal | 2026-10-31T12:09:36.314000+08:00; start-before-renewal | [start-before-renewal.png](evidence/runtime-log-pilot-20261031/runs/2026-10-31T04-09-19-922Z/candidate-rn-x002/start-before-renewal.png) | `ed43a3e3f8b8ef5db1974128e445cf4f1768482cfe48e7a090e18c8988b58b78` | [Case result](evidence/runtime-log-pilot-20261031/runs/2026-10-31T04-09-19-922Z/candidate-rn-x002/result.json); [assertions](evidence/runtime-log-pilot-20261031/run-browser.mjs#L78-L81). | Three workspace labels; identity requires independent assertions. |
| [RN-X002](06-test-cases.md#rn-x002), pending-after-rapid-clicks | 2026-10-31T12:09:36.697000+08:00; pending-after-rapid-clicks | [pending-after-rapid-clicks.png](evidence/runtime-log-pilot-20261031/runs/2026-10-31T04-09-19-922Z/candidate-rn-x002/pending-after-rapid-clicks.png) | `5194553f7f05eb3496a563cc29513211a4f6e5df3c44b224d575f2ca27274177` | [Case result](evidence/runtime-log-pilot-20261031/runs/2026-10-31T04-09-19-922Z/candidate-rn-x002/result.json); [assertions](evidence/runtime-log-pilot-20261031/run-browser.mjs#L78-L81). | Prompt remains visible during held renewal; zero closures asserted. |
| [RN-X002](06-test-cases.md#rn-x002), held-renewal-complete | 2026-10-31T12:09:36.748000+08:00; held-renewal-complete | [held-renewal-complete.png](evidence/runtime-log-pilot-20261031/runs/2026-10-31T04-09-19-922Z/candidate-rn-x002/held-renewal-complete.png) | `96b023415596560d15bc95a217c5f326ac42baf5c88c56ba121a0d63443a1d6f` | [Case result](evidence/runtime-log-pilot-20261031/runs/2026-10-31T04-09-19-922Z/candidate-rn-x002/result.json); [assertions](evidence/runtime-log-pilot-20261031/run-browser.mjs#L78-L81). | Prompt absent after usable access installation; workspace IDs preserved. |

### Before renewal

![RN-X002 before renewal](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/portal-background-session-20261019/evidence/runtime-log-pilot-20261031/runs/2026-10-31T04-09-19-922Z/candidate-rn-x002/start-before-renewal.png)

Three workspace labels are visible. Their identities require the independent result assertions.

### Pending renewal

![RN-X002 pending after 25 click events](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/portal-background-session-20261019/evidence/runtime-log-pilot-20261031/runs/2026-10-31T04-09-19-922Z/candidate-rn-x002/pending-after-rapid-clicks.png)

The expiry prompt remains visible with Extend disabled. The held response has not completed.

### Completed renewal

![RN-X002 after held renewal completes](/Users/lushevol/code/github/ratan-release-impact/workbench/tasks/portal-background-session-20261019/evidence/runtime-log-pilot-20261031/runs/2026-10-31T04-09-19-922Z/candidate-rn-x002/held-renewal-complete.png)

The prompt is absent after completion. The result confirms installed access and unchanged workspace identities.

## Verification conclusion

The method works for the declared local pilot. Confidence is HIGH for the bounded observation counts and baseline comparison.
Three candidate cases pass 56 assertions. Correlated logs explain the baseline's early closure and the candidate's awaited response.
Five planned runtime observations have matching evidence. One remains unexercised despite all selected E2E cases passing.
This difference demonstrates why E2E pass counts cannot replace the runtime-evidence metric.

The candidate reducer event follows the close request because React dispatch processing is batched.
The response arrives first; pending and final-DOM assertions pass. This ordering does not establish a new candidate defect.
No extra application fixes were made for these observations.

Full seven-AC conformance, branch coverage, unit readiness, current BFF behavior, and production suitability remain NOT_ASSESSED here.
Requirement version 5 remains a candidate without recorded human publication review.
The security observations remain proposed diagnostics. They do not establish an approved additional business rule.
No business implementation change was introduced, so this pilot makes no new full behavioral-equality claim.
Remote UAT is NOT_RUN. Its unknown inventory yields N/A, never a local-derived percentage.

## Facts, inferences, and unresolved questions

- Fact: the final [run](evidence/runtime-log-pilot-20261031/runs/2026-10-31T04-09-19-922Z/browser-summary.json) retains three passing candidate cases and one failing baseline comparison.
- Fact: [analysis](evidence/runtime-log-pilot-20261031/analysis.json) qualifies five of six local observation rows, with all six analyzed.
- Fact: the discarded response in the logout case belongs to logout; canceled relogin does not exercise stale-renewal response delivery.
- Inference: this evidence model can expose hidden path gaps during UAT when remote queries and deployment bindings exist.
- Unknown: the required UAT observation inventory, remote log source, access, deployment, and collector completeness. Owner: unknown UAT verification owner.
- Unknown: endpoints behind the 404 console signals and their occurrence in the target environment. Owner: unknown application owner.

## Findings

| Finding and evidence | Consequence | Priority and disposition | Owner | Next action |
| --- | --- | --- | --- | --- |
| Missing stale-renewal response observation: [OBS-06](evidence/runtime-log-pilot-20261031/observation-plan.json#L86), [analysis](evidence/runtime-log-pilot-20261031/analysis.json). | Complete selected-path evidence remains unsupported; final logout state still passes. Cancellation and missing request correlation prevent qualification. | Verification gap; no demonstrated session disruption. No new application defect is inferred. | unknown application verification owner | Add request correlation to the observer, then reach stale-renewal response rejection in an authorized focused case. |
| Remote UAT evidence absent: [analysis UAT state](evidence/runtime-log-pilot-20261031/analysis.json). | The required UAT runtime-evidence conclusion remains blocked. | Evidence requirement; no application-failure severity assigned. | unknown UAT verification owner | Declare UAT rows and collect remote logs with original queries, windows, deployment bindings, and completeness evidence. |
| 76 candidate 404 console signals: [analysis](evidence/runtime-log-pilot-20261031/analysis.json), individual final result console captures. | Originating endpoints remain unknown; selected session assertions show no associated disruption. | Low priority; user impact unproved. Counts describe console signals, not unique requests. | unknown application owner | Correlate originating requests in representative UAT capture before classifying an application issue. |
| 30 candidate React/CSS warnings: [analysis](evidence/runtime-log-pilot-20261031/analysis.json). | Development warnings occur with the toolkit substitute; target impact remains unverified. | Low priority; no demonstrated session disruption. | unknown application owner | Compare target tooling and retained UAT evidence if these warnings recur. |
| Six controlled 503 signals: [RN-X001 result](evidence/runtime-log-pilot-20261031/runs/2026-10-31T04-09-19-922Z/candidate-rn-x001/result.json). | Planned failures exercise retry; all six recovery cycles pass. | Expected experiment input; no new defect. | local pilot operator | Retain them separately from unexplained errors; no application fix follows from these injections. |
| Baseline early closure: [baseline result](evidence/runtime-log-pilot-20261031/runs/2026-10-31T04-09-19-922Z/baseline-rn-x002/result.json). | The dialog disappears while renewal is held. Candidate pending assertions pass. | Historical comparison defect, corrected for this local candidate case. No new release disposition. | unknown application owner | Preserve comparison evidence; obtain separately scoped deployment and UAT evidence. |

## Sources

| Source ID | Locator | Exact revision or capture | Hash | Owner, authority, and limits |
| --- | --- | --- | --- | --- |
| SRC-runtime-log-user-20261031 | [Exact user request](evidence/runtime-log-pilot-20261031/user-input.md#exact-user-input). | 31 October 2026, Asia/Singapore. | `11092ffab7698bb915154620ddbd230923f69184bfe68c341063ae2998037425` | User intent authorizes this local pilot and requires remote UAT evidence. |
| SRC-runtime-log-plan-20261031 | [Observation inventory](evidence/runtime-log-pilot-20261031/observation-plan.json). | Declared before the final run. | `700ea10096240f4790fd42ca0c998cf76fb58bcd850d56df1d641349edc2dbef` | Local six-row inventory; does not define complete UAT scope. |
| SRC-runtime-log-binding-20261031 | [Source binding](evidence/runtime-log-pilot-20261031/local-source-binding.json). | Candidate `66c6411ade58e4d134e381c2baee8ad3f76a8dbf`; baseline `f025513f696476a9cc8162681410cbd21e029bcb`. | `d988958c2e24e28dccdad91647a6212624304d95e846bd3e2822958d925a3206` | Observed local composition; historical BFF and toolkit substitutions. |
| SRC-runtime-log-run-20261031 | [Final run](evidence/runtime-log-pilot-20261031/runs/2026-10-31T04-09-19-922Z/browser-summary.json). | 12:09:20.055–12:09:44.606, Asia/Singapore. | `433d4abd553932cb0ad410dc34cc2d689d67d0ad40e08dfaaf739ded16cc1287` | Actual controlled browser execution, not UAT. |
| SRC-runtime-log-analysis-20261031 | [Analysis](evidence/runtime-log-pilot-20261031/analysis.json). | Derived from the final run. | `5bcae35ded3907c7bf0639eee22c4d12df7742ba436cfe4faa99c69746516d6b` | Derived classification; original evidence remains separately retained. |
| SRC-renewal-candidate-v5 | [Requirement](../../knowledge/records/candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria). | Version 5; candidate and draft. | `3db69ca6827b4afa0eb9f3182f15045f80dac012f9d37004d62144740424c359` | User-sourced intent; human publication review pending. |

Artifact lint passed with zero errors and four warnings.
Unknown owner, pending review, unresolved values, and pending writing review remain visible.
The [reconciliation checks](evidence/runtime-log-pilot-20261031/validation.json) retain link, source, result, log, and screenshot checks.
The [manifest](evidence/runtime-log-pilot-20261031/evidence-manifest.json) binds this report and all retained pilot artifacts.
The [cleanup confirmation](evidence/runtime-log-pilot-20261031/cleanup-confirmation.json) confirms closed ports and absent owned processes.
Prose sentence-length checks passed. These checks do not establish business approval or complete ASD-STE100 writing compliance.
