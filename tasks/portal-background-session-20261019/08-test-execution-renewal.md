---
artifact_kind: test-execution-report
id: EXEC-comprehensive-session-renewal
version: 2
status: draft
owner: unknown
source_refs: [SRC-session-remaining-execution-20261029]
related_ids: [REQ-active-session-renewal, DEFECT-portal-background-session-20261019]
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

# Session Refresh: remaining-case execution and evidence limits

> **Critical conclusions: NO_GO remains. Complete unit tests pass, but material security failure remains.**
> Action: correct or disprove applicable [SEC-01](07-security-review-renewal.md#sec-01), then reassess.
> Consequence: copied valid refresh credentials can regain authentication after apparent logout in the isolated controller test.
> Owner: unknown authentication and security owners. Evidence: [replay failure](evidence/comprehensive-renewal-20261028/expired-logout-case.json).
> Target exposure remains unverified. Complete case execution remains blocked where its required environment is unavailable.

| Metric | Current result |
| --- | --- |
| Requested 451 remaining instances | Every instance has a retained result or explicit execution blocker |
| Entire 467-instance catalog | **197 fully executed: 182 pass, 15 fail** |
| Incomplete catalog execution | **199 partial; 71 blocked**; none counted as passing |
| Full current unit suite | **471/471 pass; 123/123 suites**; zero failures, skips, todos, expected failures, or runner errors |
| SDLC coverage | Seven criteria linked; three selected passing outcomes, three activity failures, one partial |

See the [release conclusion and consolidated failure impacts](10-release-confidence.md) and [essential HTML](10-release-confidence.html).

## Run identity and provenance

The [latest instruction](evidence/user-input-20261029-run-remaining-cases.txt) authorizes remaining local execution and report refresh.
The [READY stage](evidence/remaining-execution-20261029/stage-checkpoint.json) preserves scope, authorization, and excluded actions.
No application fixes, production tests, or deployments were performed.
Every case completion was retained before further execution. Interrupted and corrected attempts remain available.

```yaml
execution_id: remaining-execution-20261029
execution_status: COMPLETED_WITH_BLOCKED_CASES
repository_id: mfe-base
repository_revision: 66c6411ade58e4d134e381c2baee8ad3f76a8dbf
test_revision: "Canonical catalog SHA-256 5622dab3b635113ff0137fbf66489f385bbcb11dc4444ec0070f7203d19a7037"
environment_identity: local-immutable-source-with-disclosed-synthetic-peers
command_or_tool_reference: evidence/remaining-execution-20261029/aggregate/final-inventory.json
process_exit_status: "Per-run originals retained; no single suite process covers the expanded catalog."
actual_results:
  catalog_total: 467
  fully_executed: 197
  passed: 182
  failed: 15
  partially_executed: 199
  blocked: 71
  current_unit_passed: 471
  current_unit_failed: 0
  current_unit_suites: 123
retained_execution_refs:
  - evidence/remaining-execution-20261029/aggregate/final-inventory.json
  - evidence/remaining-execution-20261029/full-unit-execution.json
```

Each run retains its start and completion times. The [inventory](evidence/remaining-execution-20261029/aggregate/final-inventory.json) binds original results and definitions.
The [source binding](evidence/remaining-execution-20261029/execution-source-binding.json) identifies immutable frontend bytes and the historical synthetic BFF fixture.
Actual current BFF and SDK logic ran separately in the [security composition](evidence/remaining-execution-20261029/security/server-execution.json).
The browser login fixture does not establish current composed server-byte acceptance.

## Browser environment and suite completeness

The [canonical catalog](06-test-cases.md) contains 467 expanded instances across 40 use cases.
Its hash is recorded above. Earlier 27-case and review inventories keep their historical revisions.
The catalog retains design-time execution annotations. The final inventory supplies current execution status.
Browser: Microsoft Edge 156.0.4314.50, headless Chromium, macOS, isolated contexts.
Controlled clocks accelerate expiry and endurance. Controlled visibility events do not reproduce native OS suspension.
Actual portal DOM, Home, Timeout, reducers, shared Axios, and source transport callbacks execute where bound.
Synthetic peers replace authentication responses, embedded business modules, and transport servers where disclosed.
Security probes execute actual controller, RSA, SDK-filter, and session-service logic with mocked collaborators.
Source hashes bind each assertion boundary. Twenty-six definitions cite dirty Home bytes excluded from execution.
The [inventory](evidence/remaining-execution-20261029/aggregate/final-inventory.json) records that discrepancy and each missing predicate.
No blocked case is promoted to a pass. Characterization passes do not establish accepted security behavior.
Screenshots are retained per browser case. Source-function and jsdom probes have no native browser screenshot.

| Inventory | Total | Pass | Fail | Partial | Blocked |
| --- | ---: | ---: | ---: | ---: | ---: |
| combinations | 196 | 15 | 0 | 181 | 0 |
| core-browser | 80 | 48 | 7 | 12 | 13 |
| core-integration | 37 | 37 | 0 | 0 | 0 |
| prior-browser | 3 | 3 | 0 | 0 | 0 |
| prior-security | 13 | 12 | 1 | 0 | 0 |
| security | 42 | 21 | 3 | 2 | 16 |
| workspace-transport | 96 | 46 | 4 | 4 | 42 |

## Assertions and outcomes

The following results are selected navigation points. The [full inventory](evidence/remaining-execution-20261029/aggregate/final-inventory.json) includes every case separately.
Each result identifies assertions, expected values, actual values, source bindings, and omitted boundaries.

| Canonical case | Predicate or boundary | Outcome | Assertions and actual result |
| --- | --- | --- | --- |
| [RN-A001](06-test-cases.md#rn-a001) | Continuous mouse movement reaches the requested renewal target | FAILED | [Bound result and assertions](evidence/remaining-execution-20261029/core-browser-attempt3/RN-A001/result.json) |
| [RN-A002](06-test-cases.md#rn-a002) | Continuous keyboard input reaches the requested renewal target | FAILED | [Bound result and assertions](evidence/remaining-execution-20261029/core-browser/RN-A002/result.json) |
| [RN-A003](06-test-cases.md#rn-a003) | Continuous scroll activity reaches the requested renewal target | FAILED | [Bound result and assertions](evidence/remaining-execution-20261029/core-browser/RN-A003/result.json) |
| [RN-M001](06-test-cases.md#rn-m001) | the relogin response is held pending | PASSED | [Bound result and assertions](evidence/remaining-execution-20261029/core-browser-attempt2/RN-M001/result.json) |
| [RN-M002](06-test-cases.md#rn-m002) | the relogin response supplies usable future access | PASSED | [Bound result and assertions](evidence/remaining-execution-20261029/core-browser-attempt9-validation/RN-M002/result.json) |
| [RN-M003](06-test-cases.md#rn-m003) | the relogin response rejects while refresh remains usable | PASSED | [Bound result and assertions](evidence/remaining-execution-20261029/core-browser/RN-M003/result.json) |
| [RN-L011](06-test-cases.md#rn-l011) | Four-hour requested target crosses initial refresh expiry | PARTIALLY_EXECUTED | [Bound result and assertions](evidence/remaining-execution-20261029/core-browser-attempt5-stress/RN-L011/result.json) |
| [RN-Q009](06-test-cases.md#rn-q009) | Response parsing error preserves another pending loader | FAILED | [Bound result and assertions](evidence/remaining-execution-20261029/workspace-transport/RN-Q009/result.json) |
| [RN-S023](06-test-cases.md#rn-s023) | Reject conflicting duplicate refresh headers | FAILED | [Bound result and assertions](evidence/remaining-execution-20261029/security/rn-s023/result.json) |
| [RN-S035](06-test-cases.md#rn-s035) | Prevent credential forwarding to an external destination | FAILED | [Bound result and assertions](evidence/remaining-execution-20261029/security/rn-s035/result.json) |
| [RN-S037](06-test-cases.md#rn-s037) | Reject forged skip-header authentication | FAILED | [Bound result and assertions](evidence/remaining-execution-20261029/security/rn-s037/result.json) |

All failed cases have consequences, severity, owners, and actions in the [release failure table](10-release-confidence.md#all-failed-cases-and-observed-user-impact).
Fixture errors remain distinct from application failures. Later fixture corrections do not erase the original attempts.
The [core reconciliation](evidence/remaining-execution-20261029/core-browser/reconciled-summary.json) identifies selected final outcomes and retained superseded attempts.

## Coverage inventories and summary

Intent: seven version-5 criteria. Change inventory: twelve runtime paths from `f025513f696476a9cc8162681410cbd21e029bcb` to `66c6411ade58e4d134e381c2baee8ad3f76a8dbf`.
Six paths are behavioral; six support maintenance. Complete changed-predicate and required assertion inventories remain unknown.
The [coverage report](09-renewal-coverage.md) distinguishes definitions, assertions, conformance, and execution.
The current unit suite passes without path narrowing or assertion changes. Its [JSON](evidence/remaining-execution-20261029/full-unit-results.json) retains individual test identities.
This report assesses SDLC coverage. Unit line coverage cannot establish behavioral equivalence.

| Metric | Qualified / total | Scope and limit |
| --- | --- | --- |
| Canonical criterion definitions | 7/7 | Definition relationship only |
| Selected direct assertion associations | 7/7 | Complete required assertion coverage remains UNKNOWN/7 |
| Selected matching passing execution | 3/7 | Synthetic manual recovery scope; three activity failures, one partial |
| Bounded implementation matches | 3/7 | One partial, one contradictory, two missing; complete equivalence unknown |
| Changed-path selected assertion reach | 12/12 | Complete changed-predicate coverage UNKNOWN/12 |
| Factor-pair design | 797/797 | Design only; 181 combination rows retain missing business-operation predicates |

### AC to test case coverage

| AC version | Predicate | Canonical cases | Inspected assertion | Definition / assertion status | Matching execution | Gap and limit |
| --- | --- | --- | --- | --- | --- | --- |
| [AC-1](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L187) v5 | Mouse input renews during 15 seconds | [E2E-01](06-test-cases.md#e2e-01), [RN-A001](06-test-cases.md#rn-a001), [RN-A004](06-test-cases.md#rn-a004) | [Current browser assertions](evidence/remaining-execution-20261029/core-browser-attempt3.mjs#L107); [current workspace assertion](evidence/remaining-execution-20261029/workspace-transport/run-workspace.mjs#L137); [retained supplemental activity.cjs](evidence/comprehensive-renewal-20261028/sources/cff93d755ace/activity.cjs#L10-L42) | Defined; inspected selected predicates | **FAILED**: [RN-A001 result](evidence/remaining-execution-20261029/core-browser-attempt3/RN-A001/result.json); [RN-W029 result](evidence/remaining-execution-20261029/workspace-transport/RN-W029/result.json) | Continuous 100ms mouse activity resets the 5s trailing debounce; keyboard/scroll have no Home renewal binding. Existing backlog disposition remains unchanged. Current committed-source browser execution confirms zero renewal in the measured interval. Later session loss was not observed. |
| [AC-2](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L194) v5 | Keyboard input renews during 15 seconds | [E2E-02](06-test-cases.md#e2e-02), [RN-A002](06-test-cases.md#rn-a002), [RN-A004](06-test-cases.md#rn-a004) | [Current browser assertions](evidence/remaining-execution-20261029/core-browser-attempt1.mjs#L104); [current workspace assertion](evidence/remaining-execution-20261029/workspace-transport/run-workspace.mjs#L137); [retained supplemental activity.cjs](evidence/comprehensive-renewal-20261028/sources/cff93d755ace/activity.cjs#L10-L42) | Defined; inspected selected predicates | **FAILED**: [RN-A002 result](evidence/remaining-execution-20261029/core-browser/RN-A002/result.json); [RN-W030 result](evidence/remaining-execution-20261029/workspace-transport/RN-W030/result.json) | Continuous 100ms mouse activity resets the 5s trailing debounce; keyboard/scroll have no Home renewal binding. Existing backlog disposition remains unchanged. Current committed-source browser execution confirms zero renewal in the measured interval. Later session loss was not observed. |
| [AC-3](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L201) v5 | Scroll input renews during 15 seconds | [E2E-03](06-test-cases.md#e2e-03), [RN-A003](06-test-cases.md#rn-a003), [RN-A004](06-test-cases.md#rn-a004) | [Current browser assertions](evidence/remaining-execution-20261029/core-browser-attempt1.mjs#L104); [current workspace assertion](evidence/remaining-execution-20261029/workspace-transport/run-workspace.mjs#L137); [retained supplemental activity.cjs](evidence/comprehensive-renewal-20261028/sources/cff93d755ace/activity.cjs#L10-L42) | Defined; inspected selected predicates | **FAILED**: [RN-A003 result](evidence/remaining-execution-20261029/core-browser/RN-A003/result.json); [RN-W031 result](evidence/remaining-execution-20261029/workspace-transport/RN-W031/result.json) | Continuous 100ms mouse activity resets the 5s trailing debounce; keyboard/scroll have no Home renewal binding. Existing backlog disposition remains unchanged. Current committed-source browser execution confirms zero renewal in the measured interval. Later session loss was not observed. |
| [AC-4](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L208) v5 | Four controlled hours cross initial refresh expiry without elapsed-time SSO | [E2E-04](06-test-cases.md#e2e-04), [REVIEW-F01-RECOVERY](06-test-cases.md#review-f01-recovery), [RN-L011](06-test-cases.md#rn-l011) | [sessionLifecycle.test.tsx](evidence/comprehensive-renewal-20261028/sources/f08b678e8428/sessionLifecycle.test.tsx#L540-L607); [run.mjs](evidence/comprehensive-renewal-20261028/sources/f775bad036f6/run.mjs#L75-L108) | Defined; inspected selected predicates | PARTIAL | Current [RN-L011 result](evidence/remaining-execution-20261029/core-browser-attempt5-stress/RN-L011/result.json) retains its exact outcome and omitted assertions. Controlled time cannot establish actual provider, native suspension, or indefinite operation. |
| [AC-5](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L216) v5 | Pending renewal has zero early closures | [PEND-01](06-test-cases.md#pend-01), [RN-X002](06-test-cases.md#rn-x002), [RN-M001](06-test-cases.md#rn-m001), [RN-M005](06-test-cases.md#rn-m005) | [sessionPending.test.tsx](evidence/comprehensive-renewal-20261028/sources/cb931d6812f9/sessionPending.test.tsx#L149-L159); [sessionPending.test.tsx](evidence/comprehensive-renewal-20261028/sources/cb931d6812f9/sessionPending.test.tsx#L112-L117) | Defined; inspected selected predicates | PASSED | Synthetic response credentials bypass server validation. Policy and target acceptance remain separate. |
| [AC-6](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L223) v5 | Successful renewal closes exactly once | [PEND-01](06-test-cases.md#pend-01), [RN-X001](06-test-cases.md#rn-x001), [RN-X002](06-test-cases.md#rn-x002), [RN-M002](06-test-cases.md#rn-m002), [RN-W023](06-test-cases.md#rn-w023) | [sessionPending.test.tsx](evidence/comprehensive-renewal-20261028/sources/cb931d6812f9/sessionPending.test.tsx#L149-L159); [sessionPending.test.tsx](evidence/comprehensive-renewal-20261028/sources/cb931d6812f9/sessionPending.test.tsx#L112-L117) | Defined; inspected selected predicates | PASSED | Synthetic response credentials bypass server validation. Policy and target acceptance remain separate. |
| [AC-7](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L230) v5 | Rejected renewal preserves retry | [PEND-02](06-test-cases.md#pend-02), [RN-X001](06-test-cases.md#rn-x001), [RN-M003](06-test-cases.md#rn-m003), [RN-M004](06-test-cases.md#rn-m004) | [sessionPending.test.tsx](evidence/comprehensive-renewal-20261028/sources/cb931d6812f9/sessionPending.test.tsx#L162-L173); [sessionPending.test.tsx](evidence/comprehensive-renewal-20261028/sources/cb931d6812f9/sessionPending.test.tsx#L112-L117) | Defined; inspected selected predicates | PASSED | Synthetic response credentials bypass server validation. Policy and target acceptance remain separate. |

### AC to code change coverage

| AC version | Intended predicate | Change ID or UNCHANGED | Exact old/new source | Conformance | Gap and evidence limit |
| --- | --- | --- | --- | --- | --- |
| [AC-1](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L187) v5 | Mouse input renews during 15 seconds | UNCHANGED activity handler inside changed Home file | [useController.ts](evidence/comprehensive-renewal-20261028/sources/cf5f6312f3fb/useController.ts#L60-L68); [index.tsx](evidence/comprehensive-renewal-20261028/sources/9b574c0779c3/index.tsx#L64-L64); baseline links below | CONTRADICTORY | Source assessment; new definitions cannot approve their own behavior |
| [AC-2](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L194) v5 | Keyboard input renews during 15 seconds | UNCHANGED activity handler inside changed Home file | [useController.ts](evidence/comprehensive-renewal-20261028/sources/cf5f6312f3fb/useController.ts#L60-L68); [index.tsx](evidence/comprehensive-renewal-20261028/sources/9b574c0779c3/index.tsx#L64-L64); baseline links below | MISSING | Source assessment; new definitions cannot approve their own behavior |
| [AC-3](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L201) v5 | Scroll input renews during 15 seconds | UNCHANGED activity handler inside changed Home file | [useController.ts](evidence/comprehensive-renewal-20261028/sources/cf5f6312f3fb/useController.ts#L60-L68); [index.tsx](evidence/comprehensive-renewal-20261028/sources/9b574c0779c3/index.tsx#L64-L64); baseline links below | MISSING | Source assessment; new definitions cannot approve their own behavior |
| [AC-4](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L208) v5 | Four controlled hours cross initial refresh expiry without elapsed-time SSO | [CH-RN-10](#ch-rn-10) | [useController.ts](evidence/comprehensive-renewal-20261028/sources/cf5f6312f3fb/useController.ts#L104-L197); [index.ts](evidence/comprehensive-renewal-20261028/sources/12f895009ad5/index.ts#L48-L105); baseline links below | PARTIAL | Source assessment; new definitions cannot approve their own behavior |
| [AC-5](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L216) v5 | Pending renewal has zero early closures | [CH-RN-01](#ch-rn-01), [CH-RN-02](#ch-rn-02), [CH-RN-05](#ch-rn-05) | [useController.ts](evidence/comprehensive-renewal-20261028/sources/c30ed46d9ea5/useController.ts#L131-L155); [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L56-L85); baseline links below | MATCH_WITHIN_INSPECTED_VALID_REFRESH_SCOPE | Source assessment; new definitions cannot approve their own behavior |
| [AC-6](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L223) v5 | Successful renewal closes exactly once | [CH-RN-01](#ch-rn-01), [CH-RN-02](#ch-rn-02), [CH-RN-05](#ch-rn-05), [CH-RN-08](#ch-rn-08) | [useController.ts](evidence/comprehensive-renewal-20261028/sources/c30ed46d9ea5/useController.ts#L131-L155); [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L56-L85); baseline links below | MATCH_WITHIN_INSPECTED_VALID_REFRESH_SCOPE | Source assessment; new definitions cannot approve their own behavior |
| [AC-7](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L230) v5 | Rejected renewal preserves retry | [CH-RN-01](#ch-rn-01), [CH-RN-02](#ch-rn-02), [CH-RN-05](#ch-rn-05), [CH-RN-06](#ch-rn-06), [CH-RN-08](#ch-rn-08) | [useController.ts](evidence/comprehensive-renewal-20261028/sources/c30ed46d9ea5/useController.ts#L131-L155); [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L56-L85); baseline links below | MATCH_WITHIN_INSPECTED_VALID_REFRESH_SCOPE | Source assessment; new definitions cannot approve their own behavior |

### Code change to test case coverage

| Change ID | Kind and changed path | Exact old/new bytes | Direct assertion chain | Canonical cases | Current execution | Limit |
| --- | --- | --- | --- | --- | --- | --- |
| <a id="ch-rn-01"></a>CH-RN-01 | behavioral; `src/components/Timeout/common/useController.ts` | Old: [useController.ts](evidence/comprehensive-renewal-20261028/sources/d1e40e3d9c80/useController.ts#L1-L73); new: [useController.ts](evidence/comprehensive-renewal-20261028/sources/c30ed46d9ea5/useController.ts#L1-L169) | [sessionPending.test.tsx](evidence/comprehensive-renewal-20261028/sources/cb931d6812f9/sessionPending.test.tsx#L149-L218) | [PEND-01](06-test-cases.md#pend-01), [PEND-02](06-test-cases.md#pend-02), [PEND-08](06-test-cases.md#pend-08) | [Selected passing run](evidence/comprehensive-renewal-20261028/focused-unit-results.json) | A direct inspected assertion chain establishes this selected relationship. Complete changed-branch coverage and behavioral equivalence remain unknown. |
| <a id="ch-rn-02"></a>CH-RN-02 | behavioral; `src/components/Timeout/index.tsx` | Old: [index.tsx](evidence/comprehensive-renewal-20261028/sources/e1b53e638523/index.tsx#L1-L52); new: [index.tsx](evidence/comprehensive-renewal-20261028/sources/6ad1a1e4cc1b/index.tsx#L1-L54) | [sessionPending.test.tsx](evidence/comprehensive-renewal-20261028/sources/cb931d6812f9/sessionPending.test.tsx#L195-L218) | [PEND-07](06-test-cases.md#pend-07), [PEND-08](06-test-cases.md#pend-08) | [Selected passing run](evidence/comprehensive-renewal-20261028/focused-unit-results.json) | A direct inspected assertion chain establishes this selected relationship. Complete changed-branch coverage and behavioral equivalence remain unknown. |
| <a id="ch-rn-03"></a>CH-RN-03 | supporting-maintenance; `src/hooks/reducer/root0.reducers.ts` | Old: [root0.reducers.ts](evidence/comprehensive-renewal-20261028/sources/9adfdb9bfeaf/root0.reducers.ts#L1-L52); new: [root0.reducers.ts](evidence/comprehensive-renewal-20261028/sources/0d573acb6199/root0.reducers.ts#L1-L51) | [sessionOwnership.test.tsx](evidence/comprehensive-renewal-20261028/sources/31d97cab978e/sessionOwnership.test.tsx#L201-L217) | [OWN-01](06-test-cases.md#own-01), [OWN-02](06-test-cases.md#own-02) | [Selected passing run](evidence/comprehensive-renewal-20261028/focused-unit-results.json) | A direct inspected assertion chain establishes this selected relationship. Complete changed-branch coverage and behavioral equivalence remain unknown. |
| <a id="ch-rn-04"></a>CH-RN-04 | supporting-maintenance; `src/hooks/service/config.ts` | Old: [config.ts](evidence/comprehensive-renewal-20261028/sources/f3856b594a59/config.ts#L1-L21); new: [config.ts](evidence/comprehensive-renewal-20261028/sources/aac27acebae1/config.ts#L1-L23) | [cancellationPreservation.test.ts](evidence/comprehensive-renewal-20261028/sources/3e7762c68fd8/cancellationPreservation.test.ts#L14-L70) | [DEL-14](06-test-cases.md#del-14), [DEL-19](06-test-cases.md#del-19) | [Selected passing run](evidence/comprehensive-renewal-20261028/loading-workspace-unit-results.json) | A direct inspected assertion chain establishes this selected relationship. Complete changed-branch coverage and behavioral equivalence remain unknown. |
| <a id="ch-rn-05"></a>CH-RN-05 | behavioral; `src/hooks/service/index.ts` | Old: [index.ts](evidence/comprehensive-renewal-20261028/sources/f25c800dc21f/index.ts#L1-L127); new: [index.ts](evidence/comprehensive-renewal-20261028/sources/12f895009ad5/index.ts#L1-L187) | [refreshToken.test.ts](evidence/comprehensive-renewal-20261028/sources/7e5ba4d16b48/refreshToken.test.ts#L134-L230) | [RN-R009](06-test-cases.md#rn-r009) | [Selected passing run](evidence/comprehensive-renewal-20261028/focused-unit-results.json) | A direct inspected assertion chain establishes this selected relationship. Complete changed-branch coverage and behavioral equivalence remain unknown. |
| <a id="ch-rn-06"></a>CH-RN-06 | behavioral; `src/hooks/service/util/error.response.handler.ts` | Old: [error.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/9e49eeb3288a/error.response.handler.ts#L1-L42); new: [error.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/294792814aa8/error.response.handler.ts#L1-L52) | [sessionOwnership.test.tsx](evidence/comprehensive-renewal-20261028/sources/31d97cab978e/sessionOwnership.test.tsx#L219-L225) | [OWN-03](06-test-cases.md#own-03) | [Selected passing run](evidence/comprehensive-renewal-20261028/focused-unit-results.json) | A direct inspected assertion chain establishes this selected relationship. Complete changed-branch coverage and behavioral equivalence remain unknown. |
| <a id="ch-rn-07"></a>CH-RN-07 | supporting-maintenance; `src/hooks/service/util/requestLoading.ts` | Old: New file; baseline absent; new: [requestLoading.ts](evidence/comprehensive-renewal-20261028/sources/66da1245fcc7/requestLoading.ts#L1-L43) | [cancellationPreservation.test.ts](evidence/comprehensive-renewal-20261028/sources/3e7762c68fd8/cancellationPreservation.test.ts#L14-L189) | [DEL-14](06-test-cases.md#del-14), [DEL-19](06-test-cases.md#del-19), [DEL-21](06-test-cases.md#del-21), [DEL-22](06-test-cases.md#del-22), [DEL-23](06-test-cases.md#del-23), [DEL-24](06-test-cases.md#del-24) | [Selected passing run](evidence/comprehensive-renewal-20261028/loading-workspace-unit-results.json) | A direct inspected assertion chain establishes this selected relationship. Complete changed-branch coverage and behavioral equivalence remain unknown. |
| <a id="ch-rn-08"></a>CH-RN-08 | behavioral; `src/hooks/service/util/succes.response.handler.ts` | Old: [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/4f7aa44caa1f/succes.response.handler.ts#L1-L51); new: [succes.response.handler.ts](evidence/comprehensive-renewal-20261028/sources/33c7f335a174/succes.response.handler.ts#L1-L112) | [sessionPending.test.tsx](evidence/comprehensive-renewal-20261028/sources/cb931d6812f9/sessionPending.test.tsx#L176-L193) | [PEND-03](06-test-cases.md#pend-03), [PEND-04](06-test-cases.md#pend-04), [PEND-05](06-test-cases.md#pend-05), [PEND-06](06-test-cases.md#pend-06) | [Selected passing run](evidence/comprehensive-renewal-20261028/focused-unit-results.json) | A direct inspected assertion chain establishes this selected relationship. Complete changed-branch coverage and behavioral equivalence remain unknown. |
| <a id="ch-rn-09"></a>CH-RN-09 | supporting-maintenance; `src/hooks/service/util/success.request.handler.ts` | Old: [success.request.handler.ts](evidence/comprehensive-renewal-20261028/sources/ed3a4cbd70d4/success.request.handler.ts#L1-L53); new: [success.request.handler.ts](evidence/comprehensive-renewal-20261028/sources/25a914336e2a/success.request.handler.ts#L1-L60) | [sessionOwnership.test.tsx](evidence/comprehensive-renewal-20261028/sources/31d97cab978e/sessionOwnership.test.tsx#L276-L296) | [OWN-08](06-test-cases.md#own-08), [OWN-09](06-test-cases.md#own-09) | [Selected passing run](evidence/comprehensive-renewal-20261028/focused-unit-results.json) | A direct inspected assertion chain establishes this selected relationship. Complete changed-branch coverage and behavioral equivalence remain unknown. |
| <a id="ch-rn-10"></a>CH-RN-10 | behavioral; `src/pages/Home/common/useController.ts` | Old: [useController.ts](evidence/comprehensive-renewal-20261028/sources/d7f9cb147cf7/useController.ts#L1-L219); new: [useController.ts](evidence/comprehensive-renewal-20261028/sources/cf5f6312f3fb/useController.ts#L1-L324) | [sessionLifecycle.test.tsx](evidence/comprehensive-renewal-20261028/sources/f08b678e8428/sessionLifecycle.test.tsx#L540-L607) | [REVIEW-F01-RECOVERY](06-test-cases.md#review-f01-recovery) | [Selected passing run](evidence/comprehensive-renewal-20261028/focused-unit-results.json) | A direct inspected assertion chain establishes this selected relationship. Complete changed-branch coverage and behavioral equivalence remain unknown. |
| <a id="ch-rn-11"></a>CH-RN-11 | supporting-maintenance; `src/utils/common.ts` | Old: [common.ts](evidence/comprehensive-renewal-20261028/sources/93d6fb57f00f/common.ts#L1-L321); new: [common.ts](evidence/comprehensive-renewal-20261028/sources/3b6a12d1577f/common.ts#L1-L323) | [sessionOwnership.test.tsx](evidence/comprehensive-renewal-20261028/sources/31d97cab978e/sessionOwnership.test.tsx#L201-L225) | [OWN-01](06-test-cases.md#own-01), [OWN-02](06-test-cases.md#own-02), [OWN-03](06-test-cases.md#own-03) | [Selected passing run](evidence/comprehensive-renewal-20261028/focused-unit-results.json) | A direct inspected assertion chain establishes this selected relationship. Complete changed-branch coverage and behavioral equivalence remain unknown. |
| <a id="ch-rn-12"></a>CH-RN-12 | supporting-maintenance; `src/utils/sessionEpoch.ts` | Old: New file; baseline absent; new: [sessionEpoch.ts](evidence/comprehensive-renewal-20261028/sources/b524186ae494/sessionEpoch.ts#L1-L18) | [sessionOwnership.test.tsx](evidence/comprehensive-renewal-20261028/sources/31d97cab978e/sessionOwnership.test.tsx#L201-L225) | [OWN-01](06-test-cases.md#own-01), [OWN-02](06-test-cases.md#own-02), [OWN-03](06-test-cases.md#own-03) | [Selected passing run](evidence/comprehensive-renewal-20261028/focused-unit-results.json) | A direct inspected assertion chain establishes this selected relationship. Complete changed-branch coverage and behavioral equivalence remain unknown. |


## Retained evidence inventory

| Evidence | Locator | Integrity and availability limit |
| --- | --- | --- |
| Final case inventory | [All 467](evidence/remaining-execution-20261029/aggregate/final-inventory.json) | Exact definition blocks, outline rows, results, and source bindings have SHA-256 |
| Complete units | [Execution](evidence/remaining-execution-20261029/full-unit-execution.json), [results](evidence/remaining-execution-20261029/full-unit-results.json) | 471/471 at current candidate; delayed-exit warning retained |
| Security | [Final audit](evidence/remaining-execution-20261029/security/final-audit.json) | Forty-two newly requested cases; mocks and blocked target checks remain explicit |
| Workspace and transport | [Summary](evidence/remaining-execution-20261029/workspace-transport/summary.json) | Synthetic modules, controlled routes, and source mismatch retained |
| Combinations | [Summary](evidence/remaining-execution-20261029/combinations/combination-summary.json) | 283 bounded assertions pass; only fifteen complete ordering cases pass |
| Original prior executions | [Earlier binding](evidence/comprehensive-renewal-20261028/execution-source-binding.json) | Sixteen prior instances remain separate from the 451 newly requested instances |

## Browser evidence bindings

Case directories retain setup/failure/final captures where available. Result JSON binds captures to the executed predicates.
The [workspace loading failure](evidence/remaining-execution-20261029/workspace-transport/RN-Q009/result.json) includes held-response state and loader disappearance.
Its [screenshot](evidence/remaining-execution-20261029/workspace-transport/RN-Q009/attempt-failed.png) supports the visible state, not a data-loss claim.
The [core summary](evidence/remaining-execution-20261029/core-browser/reconciled-summary.json) and [workspace manifest](evidence/remaining-execution-20261029/workspace-transport/evidence-manifest.json) identify retained captures.
Java, jsdom, and source-function cases rely on assertion and request evidence. Native screenshots are not applicable there.

## Verification conclusion

**The requested catalog is fully reconciled, but complete canonical execution remains unavailable for the blocked predicates.**
Passing results verify only their stated conditions. Full units now satisfy the mandatory current-suite condition.
Security failure, current activity gaps, partial consumers, and policy uncertainty prevent complete conformance or acceptance claims.
`TC >= AC = Code Change` remains unestablished. Unsupported additional behavior and full boundary inventories remain unknown.

## Facts, inferences, and unresolved questions

Facts: per-case results retain actual assertions. Failed predicates remain visible. Current full unit execution passes.
Inferences: conditional security and session interruption risks depend on supported callers and matching deployment settings.
Unknowns: actual business writes, transport authorization, native lifecycle behavior, and pending policy remain unresolved.
Use the [single living policy register](05-test-strategy-renewal.md#policy-questions). No business answer is inferred from execution authorization.

## Findings

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| [SEC-01](07-security-review-renewal.md#sec-01) | Logout can leave refresh usable | unknown authentication owner | Correct or disprove applicable failure; retain rejection controls |
| [New security impacts](evidence/remaining-execution-20261029/security/new-failure-impacts.json) | Conditional credential and authorization risks remain | unknown security owner | Trace actual callers and gateway enforcement |
| [All incomplete predicates](evidence/remaining-execution-20261029/aggregate/final-inventory.json) | Complete acceptance is unavailable | unknown test and service owners | Bind missing environments and exact assertions |
| [Current activity and loading failures](evidence/remaining-execution-20261029/workspace-transport/findings.json) | Renewal and visible loading targets fail | unknown application owner | Retain approved backlog scope; decide loading-gap disposition |

## Sources

| Source | Locator | Revision, hash, and authority |
| --- | --- | --- |
| User | [Latest instruction](evidence/user-input-20261029-run-remaining-cases.txt) | 29 October 2026; local test authorization |
| Canonical definitions | [Catalog](06-test-cases.md) | Exact SHA-256 above; policy acceptance remains separate |
| Sources and results | [Final inventory](evidence/remaining-execution-20261029/aggregate/final-inventory.json) | Exact revisions, assertion bindings, and SHA-256 per item |
| Historical baseline and source map | [Original assertion map](evidence/comprehensive-renewal-20261028/assertion-map.json) | Selected relationships, not complete equivalence |
| Final automated checks | [Validation](evidence/release-report-execution-20261029/validation.json) | Structural checks only; full ASD writing review pending |
