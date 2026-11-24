---
artifact_kind: test-execution-report
id: SESSION-PAIRED-VERIFICATION-RESULT-20261030
version: 1
status: draft
owner: unknown
source_refs: [USER-20261030-GOAL]
related_ids: [RN-S001, RN-S002, RN-R020]
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

# Paired logout verification

> **Expired-access logout permits refresh replay on both inspected revisions.**
> Action: review the logout contract and verify the actual server consequence.
> Consequence: the proposed zero-access security assertion remains failed.
> Owner: unknown authentication and security owners. Evidence: [paired results](paired-comparison.json).
> Priority: P2 pending target evidence. Protected business acceptance and production impact remain unverified.

The four local cases completed: **two passed, two failed, zero errored, and zero remain unrun**.
The failed behavior is inherited. This stage does not assess release suitability or authorize application changes.

## Run identity and provenance

- Execution ID: `SESSION-PAIRED-20261030`.
- Execution status: `COMPLETED_WITH_ASSERTION_FAILURES`.
- Baseline: BFF `19f484efbbfbd4a9d16cdec8a64c4b7fa66e901a`.
- Candidate: BFF `134a340472f29d2a4136e07e516690de6a18e323`.
- Test identity: shared [Java probe](SecurityLogoutProbe.java); exact SHA-256 appears in the [execution manifest](paired-execution.json).
- Environment: OpenJDK 17, local macOS, cached public verification dependencies, and servlet mocks.
- Entry authorization: [user input](user-input.md) and [bounded READY stage](01-paired-verification-stage.md).
- Command: `python3 tasks/portal-background-session-20261019/evidence/conversation-improvements-20261030/run_paired_security_probe.py`.
- Final process exit: `1`, because two application assertions failed.
- Timestamps, compiler commands, source inputs, class hashes, and dependency hashes: [execution manifest](paired-execution.json).

## Browser environment and suite completeness

- Case inventory: [RN-S001](../../06-test-cases.md#rn-s001) and [RN-S002](../../06-test-cases.md#rn-s002), each on two revisions.
- Original cases: four revision instances; two passed and two failed.
- Additional cases: none; the shared HTTP 401 check supplements the proposed expired-access security observation.
- Browser identity: not applicable; this is direct controller integration without HTTP transport.
- Target deployment: unavailable; no deployment or protected business service executes.
- Clock: actual wall clock, with access expiry set ten minutes before or after case setup.
- Fixtures: ephemeral RSA-2048 keys, synthetic users, signed credentials, and in-memory mocked session persistence.
- Substitutions: drawer, entitlement, and filter collaborators are mocked. Servlet requests and responses are mocked.
- Source integrity: 54 baseline and 55 candidate Java inputs were compiled from pinned exports, including the shared probe.
- Source limits: unrelated injection types can use hashed cached application classes from revision `834b4155232222347220e47139a502ee43a9cbdf`.
- Executed controller, JWT, session, DTO, and configuration inputs are pinned in the compilation manifest.
- Missing local executions: none. Native browser, real database, provider, replicas, and protected-operation execution remain outside this stage.

## Assertions and outcomes

| Case | Intent status | Expected result | Baseline result | Candidate result | Evidence |
| --- | --- | --- | --- | --- | --- |
| [RN-S001](../../06-test-cases.md#rn-s001) | Observed behavior | Logout succeeds; replay returns 401 and issues no access. | PASSED; one revoked session; replay 401. | PASSED; one revoked session; replay 401. | [Baseline](baseline-RN-S001.json), [candidate](candidate-RN-S001.json), [assertions](SecurityLogoutProbe.java) |
| [RN-S002](../../06-test-cases.md#rn-s002) | Proposed security behavior | Replay issues no access; record revocation and HTTP outcome. | FAILED; zero revoked sessions; replay 200 issues access. | FAILED; zero revoked sessions; replay 200 issues access. | [Baseline](baseline-RN-S002.json), [candidate](candidate-RN-S002.json), [assertions](SecurityLogoutProbe.java) |

Both expired-access logout responses return HTTP 200 and `result: true`.
Both servlet sessions are invalidated. Neither expired-access case writes the session revocation record.
The retained, valid refresh credential then obtains a new access credential through the actual controller.
The same probe bytes and assertions execute on both revisions.
Reflection adapts the renamed entitlement mock API. It does not change security assertions.

## Coverage inventories and summary

- Intent inventory: two canonical cases; neither has a separate approved product criterion in the catalog.
- Test inventory: two controller cases, repeated against two pinned revisions.
- Change inventory: no application change was made; selected logout and replay methods are unchanged across revisions.
- Required boundaries: actual RSA validation and session-service logic execute; persistence, HTTP, and protected operations do not.
- Full BFF change coverage: unknown; this bounded stage does not review unrelated migration changes.

| Metric | Qualified / total | Percentage | Incomplete or failed items | Evidence and limit |
| --- | --- | --- | --- | --- |
| Selected case definitions with inspected assertions | 2 / 2 | 100% | None | [Probe](SecurityLogoutProbe.java); approved-product AC denominator is empty. |
| Completed revision instances | 4 / 4 | 100% | None | [Execution](paired-execution.json); local controller scope only. |
| Passing revision instances | 2 / 4 | 50% | Both [RN-S002](../../06-test-cases.md#rn-s002) instances | [Comparison](paired-comparison.json) |
| AC-to-test definition, assertion, and pass coverage | 0 / 0 | N/A | No approved AC is in this bounded inventory. | Canonical cases retain observed and proposed-security status. |
| AC-to-code mapping and conformance | 0 / 0 | N/A | No approved AC is in this bounded inventory. | No product conformance percentage is claimed. |
| Application-change-to-test coverage | 0 / 0 | N/A | No application changes were made. | Unrelated BFF migration changes remain unassessed. |

### AC to test case coverage

| Intent source | Applicable predicate | Canonical case | Inspected assertion | Matching execution | Gap and limit |
| --- | --- | --- | --- | --- | --- |
| Observed behavior; no separate approved AC | Logout succeeds; replay rejects access. | [RN-S001](../../06-test-cases.md#rn-s001) | [Shared probe](SecurityLogoutProbe.java) | [Baseline pass](baseline-RN-S001.json), [candidate pass](candidate-RN-S001.json) | Local integration only. |
| Proposed security behavior; no separate approved AC | Expired-access logout prevents refresh access. | [RN-S002](../../06-test-cases.md#rn-s002) | [Shared probe](SecurityLogoutProbe.java) | [Baseline failure](baseline-RN-S002.json), [candidate failure](candidate-RN-S002.json) | Intent approval and target impact remain unestablished. |

### AC to code change coverage

| Intent source | Predicate | Change classification | Exact source comparison | Conformance | Limit |
| --- | --- | --- | --- | --- | --- |
| [RN-S001](../../06-test-cases.md#rn-s001) observation | Valid-access logout revokes refresh replay. | Required unchanged implementation | [Pinned method identities](paired-source-inspection.json) | Matches the local observed predicate. | No production equivalence claim. |
| [RN-S002](../../06-test-cases.md#rn-s002) proposal | Expired-access logout prevents refresh access. | Required unchanged implementation | [Pinned method identities](paired-source-inspection.json) | Contradicts the proposed zero-access predicate. | No approved product AC is inferred. |

### Code change to test case coverage

| Change inventory | Maintenance rationale | Cases | Inspected assertions | Execution | Limit |
| --- | --- | --- | --- | --- | --- |
| No application change; denominator 0 | Add paired evidence for an existing consequential case. | [RN-S001](../../06-test-cases.md#rn-s001), [RN-S002](../../06-test-cases.md#rn-s002) | [Probe](SecurityLogoutProbe.java) | [Four retained instances](paired-execution.json) | This does not cover unrelated BFF migration changes. |

## Retained evidence inventory

| Evidence | Locator | Identity and limit |
| --- | --- | --- |
| Authorization and readiness | [User input](user-input.md), [stage](01-paired-verification-stage.md) | Local exploration only. |
| Complete execution | [Execution manifest](paired-execution.json) | Exact revisions, source hashes, dependencies, configuration, and per-case checkpoints. |
| Paired result comparison | [Comparison](paired-comparison.json) | Same observables; inherited failure classification. |
| Inspected source | [Source inspection](paired-source-inspection.json) | Exact file hashes and normalized method hashes. |
| Initial compilation failure | [Preserved attempt](attempt-01-index.json) | Harness issue; no application case ran in this attempt. |
| External contracts | [Dispositions](contract-dispositions.json) | Existing evidence reconciled; no new server verification claimed. |
| Integrity checks | [Validation](validation.json) | Automated checks only; ASD review remains pending. |

## Browser evidence bindings

Not applicable: no browser runs in this paired controller experiment.
The separate [stale-response evidence](../remaining-execution-20261029/core-integration/RN-R020/result.json) uses actual React integration in jsdom.
Its controlled response clears renewed credentials. Its passing status records an observation, not approved behavior.

## Verification conclusion

- Behavior claim: both pinned revisions permit refresh replay after expired-access logout in the disclosed local integration.
- Covered conditions: valid and expired access, unexpired same-session refresh, actual RSA checks, and actual controller calls.
- Uncovered conditions: real HTTP transport, provider behavior, database persistence, replicas, and protected business acceptance.
- Behavioral equality: selected observables and inspected security methods match between revisions.
- Missing behavior: both revisions fail the proposed expired-access zero-access assertion.
- Additional unsupported behavior: whole-candidate conformance remains unknown; unrelated changes were not assessed.
- Product acceptance and release recommendation: not established or reassessed by this stage.

## Facts, inferences, and unresolved questions

Facts: both valid-access cases pass. Both expired-access cases issue access after logout.
The inspected logout, replay, JWT-validation, and session-service methods are unchanged.
Inference: the local failure is inherited, rather than introduced by the compared BFF migration.
The result does not establish production exposure or a protected transaction.

| Item | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| Expired-access replay | [Paired failure](paired-comparison.json) | Local logout leaves refresh access usable. | unknown authentication and security owners | Review the contract; verify the actual endpoint and protected consequence. |
| Stale unauthorized response | [RN-R020 observation](../remaining-execution-20261029/core-integration/RN-R020/result.json) | Controlled client credentials are cleared. Actual provider occurrence remains unverified. | unknown MFE and provider owners | Bind response semantics, expected handling, and the user recovery journey. |
| Protected operation | [Combination predicates](../remaining-execution-20261029/combinations/combination-summary.json) | 181 combination rows retain unavailable server predicates. | unknown business-service and security owners | Name an authorized endpoint, operation ID, and durable commit observer. |
| Upload and financial commits | [Workspace execution](../remaining-execution-20261029/workspace-transport/summary.json) | Client request counts cannot prove business commit semantics. | unknown business-service owner | Supply an inspected endpoint and authoritative transaction audit. |

Unavailable contracts remain evidence gaps. They are not product failures or automatic release holds.
The [contract dispositions](contract-dispositions.json) preserve exact evidence hashes and required external boundaries.
