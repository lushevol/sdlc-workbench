---
artifact_kind: traceability-record
id: COVERAGE-comprehensive-session-renewal
version: 1
status: draft
owner: unknown
source_refs: [SRC-comprehensive-renewal-20261028]
related_ids: [REQ-active-session-renewal, PLAN-comprehensive-session-renewal]
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
# Session renewal coverage and remaining evidence

> **Critical conclusions: Security acceptance is blocked by one reproduced inherited revocation defect.**
> Action: correct [SEC-01](07-security-review-renewal.md#sec-01) and collect target evidence. Consequence: secure deployment cannot be recommended.
> Owner: unknown authentication owner. Evidence: [failed controller case](evidence/comprehensive-renewal-20261028/expired-logout-case.json).

## Scope and identities

Scope: the [current request](evidence/user-input-20261028-comprehensive-renewal.txt), seven renewal criteria, and 12 changed shell runtime paths.
Capability: single-ui-authentication. Related capabilities include workspace composition and E2E verification.
Repositories: mfe-base, single-ui-bff, authentication SDK, application consumers, and ratan-test-engine.
Contracts: token family, shared HTTP client, container props, and test-suite execution.
Shell comparison: `f025513f696476a9cc8162681410cbd21e029bcb` to `66c6411ade58e4d134e381c2baee8ad3f76a8dbf`.
Local Home-controller edits remain excluded from current execution claims. Worktree observations have separate source hashes.

## Requirement and criterion declarations

Requirement version 5 SHA-256: `3db69ca6827b4afa0eb9f3182f15045f80dac012f9d37004d62144740424c359`. Publication review remains pending.

| Requirement or defect ID | Criterion ID | Measurable expected behavior | Source revision | Knowledge review state |
| --- | --- | --- | --- | --- |
| REQ-active-session-renewal | [AC-1](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L187) | Mouse input renews during 15 seconds | v5; hash above | pending |
| REQ-active-session-renewal | [AC-2](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L194) | Keyboard input renews during 15 seconds | v5; hash above | pending |
| REQ-active-session-renewal | [AC-3](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L201) | Scroll input renews during 15 seconds | v5; hash above | pending |
| REQ-active-session-renewal | [AC-4](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L208) | Four controlled hours cross initial refresh expiry without elapsed-time SSO | v5; hash above | pending |
| REQ-active-session-renewal | [AC-5](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L216) | Pending renewal has zero early closures | v5; hash above | pending |
| REQ-active-session-renewal | [AC-6](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L223) | Successful renewal closes exactly once | v5; hash above | pending |
| REQ-active-session-renewal | [AC-7](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L230) | Rejected renewal preserves retry | v5; hash above | pending |

## Coverage inventories and summary

Target: `TC >= AC = Code Change` concerns behavior containment and equivalence. Counts cannot establish that equivalence.
New catalog inventory: **271 individual cases plus three outlines, with 196 example rows: 467 expanded instances.**
The [40 use cases](03-use-cases-renewal.md#main-flow) link those definitions. Historical cases remain separately preserved.
The expansion includes 60 policy-open individual cases. They are not 60 approved new requirements.
New execution inventory: 3 browser cases and 13 controller cases. Fifteen pass; one security case fails.
The other 451 expanded instances remain `NOT_RUN`. Existing unit tests are counted separately.

| Metric | Qualified / total | Percentage | Incomplete or failed IDs | Evidence and limit |
| --- | --- | --- | --- | --- |
| AC with canonical definitions | 7 / 7 | 100% definition only | none | New and retained definitions cover the seven named targets |
| AC with inspected direct assertions | 7 / 7 | 100% relationship only | Broader boundaries remain incomplete | [Assertion map](evidence/comprehensive-renewal-20261028/assertion-map.json); no conformance claim |
| AC with current matching local passing execution | 3 / 7 | 42.9% within disclosed fixture | AC-4 partial; AC-1, AC-2, AC-3 not rerun | Synthetic manual recovery only |
| AC with inspected implementation locations | 7 / 7 | 100% mapping only | AC-1 contradictory; AC-2 and AC-3 missing; AC-4 partial | Locations do not establish conformance |
| Complete business conformance | UNKNOWN / 7 | UNKNOWN | Target and policy limits remain | No complete equivalence claim |
| Changed runtime paths with selected direct assertions | 12 / 12 | 100% relationship only | Complete branch coverage UNKNOWN | Includes six supporting-maintenance paths |
| Changed runtime paths with selected passing tests | 12 / 12 | 100% selected predicates only | Complete path behavior UNKNOWN | [Current executions](08-test-execution-renewal.md) |
| Behavioral-change justification | UNKNOWN / 6 | UNKNOWN | Policy and scope review incomplete | Six runtime paths classified behavioral; six supporting maintenance |
| Complete changed-behavior assertion coverage | UNKNOWN / 12 | UNKNOWN | Full changed-predicate denominator unavailable | Path counts are not behavior completeness |
| Declared factor-value pair design coverage | 797 / 797 | 100% design only | Execution NOT_RUN | 37 rows across 11 declared factors |
| Instrumented line or branch coverage | UNKNOWN | UNKNOWN | No instrumentation collected here | Keep separate from behavioral coverage |

The [design manifest](evidence/comprehensive-renewal-20261028/design-manifest.json) lists every new case and its evidence class.
The Cartesian population has 1,866,240 rows. Pair coverage does not execute that population.
The selected four-factor subset has 144 explicit rows. Fifteen more rows enumerate one finite response-order model.

## Relationship evidence

| From ID | Relationship | To ID | Evidence | Evidence class | Limit |
| --- | --- | --- | --- | --- | --- |
| User request | Authorizes | Test design and assessment | [Exact input](evidence/user-input-20261028-comprehensive-renewal.txt) | user intent | No application fix or deployment performed |
| Seven criteria | Have case and source links | Canonical and executable cases | [Assertion map](evidence/comprehensive-renewal-20261028/assertion-map.json) | inspected relationship | Complete equivalence remains unestablished |
| Local executions | Establish stated assertions | Local candidate and fixtures | [Execution report](08-test-execution-renewal.md) | retained execution | No target or provider parity |

## Inspected implementation and assertions

### AC to test case coverage

| AC version | Predicate | Canonical cases | Inspected assertion | Definition / assertion status | Matching execution | Gap and limit |
| --- | --- | --- | --- | --- | --- | --- |
| [AC-1](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L187) v5 | Mouse input renews during 15 seconds | [E2E-01](06-test-cases.md#e2e-01), [RN-A001](06-test-cases.md#rn-a001), [RN-A004](06-test-cases.md#rn-a004) | [activity.cjs](evidence/comprehensive-renewal-20261028/sources/cff93d755ace/activity.cjs#L10-L42) | Defined; inspected selected predicates | NOT_RUN | Continuous 100ms mouse activity resets the 5s trailing debounce; keyboard/scroll have no Home renewal binding. Existing backlog disposition remains unchanged. Inspected current modular test assertions. Those browser assertions were not executed against this pinned source in this stage. |
| [AC-2](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L194) v5 | Keyboard input renews during 15 seconds | [E2E-02](06-test-cases.md#e2e-02), [RN-A002](06-test-cases.md#rn-a002), [RN-A004](06-test-cases.md#rn-a004) | [activity.cjs](evidence/comprehensive-renewal-20261028/sources/cff93d755ace/activity.cjs#L10-L42) | Defined; inspected selected predicates | NOT_RUN | Continuous 100ms mouse activity resets the 5s trailing debounce; keyboard/scroll have no Home renewal binding. Existing backlog disposition remains unchanged. Inspected current modular test assertions. Those browser assertions were not executed against this pinned source in this stage. |
| [AC-3](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L201) v5 | Scroll input renews during 15 seconds | [E2E-03](06-test-cases.md#e2e-03), [RN-A003](06-test-cases.md#rn-a003), [RN-A004](06-test-cases.md#rn-a004) | [activity.cjs](evidence/comprehensive-renewal-20261028/sources/cff93d755ace/activity.cjs#L10-L42) | Defined; inspected selected predicates | NOT_RUN | Continuous 100ms mouse activity resets the 5s trailing debounce; keyboard/scroll have no Home renewal binding. Existing backlog disposition remains unchanged. Inspected current modular test assertions. Those browser assertions were not executed against this pinned source in this stage. |
| [AC-4](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L208) v5 | Four controlled hours cross initial refresh expiry without elapsed-time SSO | [E2E-04](06-test-cases.md#e2e-04), [REVIEW-F01-RECOVERY](06-test-cases.md#review-f01-recovery), [RN-L011](06-test-cases.md#rn-l011) | [sessionLifecycle.test.tsx](evidence/comprehensive-renewal-20261028/sources/f08b678e8428/sessionLifecycle.test.tsx#L540-L607); [run.mjs](evidence/comprehensive-renewal-20261028/sources/f775bad036f6/run.mjs#L75-L108) | Defined; inspected selected predicates | PARTIAL | No finite test proves indefinite operation. Cross-source historical results retain their original bindings. |
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

## Retained execution and verification

Targeted units: **157 / 157 passed across ten suites**, with zero failures, skips, or runner errors.
New browser cases: **3 / 3 passed**, with 56 assertions. Actual shell DOM and Axios ran with substituted authentication.
Security controller cases: **12 / 13 passed**. The inherited logout replay case failed.
The security runner exits with failure when its security assertion fails. A successful compilation does not override that result.
See [unit and browser evidence](08-test-execution-renewal.md), [controller evidence](07-security-review-renewal.md#security-verification), and [source-map binding](evidence/comprehensive-renewal-20261028/served-source-binding.json).
The full application suite was not rerun. This stage makes no delivery recommendation.

## Coverage gaps

Real application data, dirty forms, lazy modules, live WebSockets, STOMP, SSE, and long transfers remain unexecuted.
Target identity-provider integration, deployed settings, revocation replicas, and physical sleep remain unverified.
Activity targets retain their prior backlog disposition. Their source gaps remain visible above.
Full four-hour current-candidate browser verification remains absent. Component and historical executions have narrower claims.
Use the [policy register](05-test-strategy-renewal.md#policy-questions) for unresolved acceptance decisions.

## Facts, inferences, and unresolved questions

Facts: the retained executions establish only their asserted fixture outcomes. One security assertion fails.
Inference: broader workspace and transport interactions require additional implementation-specific execution.
Unknowns: deployed composition, complete policy inventory, and target security controls remain unavailable.

## Findings

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| [SEC-01](07-security-review-renewal.md#sec-01) | Logout can leave refresh usable in the isolated path | unknown authentication owner | Correct revocation and rerun replay assertions |
| [Policy-open cases](evidence/comprehensive-renewal-20261028/design-manifest.json) | Acceptance remains blocked for those outcomes | unknown business and security owners | Resolve the consolidated policy questions |
| [Source and execution limits](08-test-execution-renewal.md) | Local passes cannot establish secure target behavior | unknown test owner | Bind and execute the reviewed target composition |

## Sources

| Source ID | Locator | Exact revision | Hash | Owner, authority, and limits |
| --- | --- | --- | --- | --- |
| User request | [Exact input](evidence/user-input-20261028-comprehensive-renewal.txt) | user-message-20261028 | [Source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json) | User; test and security scope |
| Requirement and source | [Source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json) | Per-source exact revisions | SHA-256 per item | Candidate intent and inspected source remain separate |
| Direct assertion and baseline bytes | [Coverage manifest](evidence/comprehensive-renewal-20261028/coverage-source-manifest.json) | Per-item revisions | SHA-256 per item | Selected predicate chains only |
