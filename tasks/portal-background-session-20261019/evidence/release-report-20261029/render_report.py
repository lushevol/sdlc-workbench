"""Render the scoped Markdown assessment and its essential HTML companion."""
from pathlib import Path
import html
import json

EVIDENCE = Path(__file__).resolve().parent
TASK = EVIDENCE.parent.parent
failures = json.loads((EVIDENCE / 'failure-impact-audit.json').read_text())
CASES = {c['case_id']: c for c in failures['cases']}


def md(label, href):
    return f'[{label}]({href})'


def a(label, href):
    return f'<a href="{html.escape(href, quote=True)}">{html.escape(label)}</a>'


def failure_row(case_id, point, impact, severity, disposition):
    c = CASES[case_id]
    anchor = 'failure-' + case_id.lower()
    sources = ', '.join(md('source' if i == 0 else 'support', x) for i, x in enumerate(c['source_links']))
    links = sources + '; ' + md('assertions', c['assertion_link']) + '; ' + md('result', c['result_link'])
    return f'| <a id="{anchor}"></a>{md(case_id, c["definition"])} | {point} | {impact} | **{severity}**. {disposition} | {links} |'


ROWS = [
    ('RN-S002', 'Expired-access logout returns success, records zero revocations, and permits valid refresh replay. Expected replay status: 401; actual: 200.',
     'Another holder of copied, valid refresh credentials can regain authentication after apparent logout in a matching deployment. Persistence was mocked. No theft or protected business action was demonstrated.',
     'S2 High, conditional / P1', 'Inherited server defect. **Hold security sign-off** until correction or verified non-applicability.'),
    ('REVIEW-E2E-01', 'Replacement login occurs during delayed Logout. The old dialog remains; Extend is disabled; a second Logout starts no request.',
     'A valid replacement session is unusable through the dialog actions in the local flow. Supported application caller remains unknown.',
     'S2 High, conditional / P2', 'Introduced guard. **Investigate before positive review sign-off**; current persistence is a source prediction.'),
    ('E2E-01', 'Continuous mouse movement produces zero successful renewals during 15 seconds. Each event resets the five-second trailing debounce.',
     'Mouse-only work does not extend the session in this interval. Later expiry and interruption are possible; logout or lost work was not observed.',
     'S4 Minor / P4, user', 'Inherited. **Backlog retained** under the recorded direction.'),
    ('E2E-02', 'Continuous keyboard input produces zero successful renewals during 15 seconds. The renewal binding is absent.',
     'Typing alone does not extend the session. Later expiry and interruption are possible; actual logout or lost work was not observed.',
     'S4 Minor / P4, user', 'Inherited. **Backlog retained**.'),
    ('E2E-03', 'Continuous scroll input produces zero successful renewals during 15 seconds. The renewal binding is absent.',
     'Scrolling alone does not extend the session. Later expiry and interruption are possible; actual logout or lost work was not observed.',
     'S4 Minor / P4, user', 'Inherited. **Backlog retained**.'),
    ('E2E-08', 'Expected one pending renewal after continuous movement; observed zero. The activity prerequisite fails before request sharing runs.',
     'Renewal does not start in this fixture. This run proves neither a sharing failure nor later session loss.',
     'S4 Minor / P4, proposed', 'Inherited prerequisite. **Backlog candidate** within the retained activity scope.'),
    ('BROWSER-SHARING-PENDING', 'Expected one pending request; observed two requests and one cancellation. A later activity event replaces the first request.',
     'Duplicate service work is observed. Slow connections could delay renewal; user blocking and session loss remain unmeasured.',
     'S3 Moderate, conditional / P4', 'Inherited. **Backlog retained**; representative-latency impact remains unknown.'),
    ('E2E-12', 'A response body says result=false, but its authorization header still enters client state.',
     'An inconsistent provider response changes credentials despite failure. Valid-provider occurrence, unauthorized access, and interruption remain unproved.',
     'Severity UNKNOWN / P3', '**Acceptability unknown**. Inspect the supported provider contract and resulting user journey.'),
    ('E2E-18', 'Pending activity work is not canceled after Logout and Home unmount.',
     'Service work remains pending after leaving the session. This failure does not prove access restoration; later assertions did not execute.',
     'S4 Minor / P4, user', 'Inherited. **Backlog retained**; verify stale completion separately.'),
    ('E2E-19', 'An earlier activity request remains pending when the expiry dialog opens.',
     'Old work overlaps recovery. Token overwrite and extra prompt closure were not observed because the case stopped at cancellation.',
     'S4 Minor / P4, user', 'Likely inherited. **Backlog retained**; original baseline setup was incomplete.'),
]

header = '''---
artifact_kind: release-readiness
id: ASSESS-session-delivery-confidence-20261028
version: 4
status: draft
owner: unknown
source_refs:
  - SRC-session-refresh-report-20261029
  - SRC-session-comprehensive-tests-20261028
  - SRC-session-refresh-audits-20261029
  - SRC-session-backlog-scope-20261027
related_ids:
  - DEFECT-portal-background-session-20261019
  - REQ-active-session-renewal
  - COVERAGE-comprehensive-session-renewal
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

# Session Refresh release report: decision, coverage, and user impact

> **Conclusion: NO_GO for the assessed source composition. The remaining problems are not acceptable as a whole.**
> Action: correct or disprove applicability of [SEC-01](07-security-review-renewal.md#sec-01), then reassess matching source and tests.
> Consequence: a copied, valid refresh credential can regain authentication after apparent logout in the isolated controller test.
> Owner: unknown authentication and security owners. Evidence: [failed replay result](evidence/comprehensive-renewal-20261028/expired-logout-case.json).
> Production exposure remains unverified. This is an inherited server defect, not a demonstrated new frontend bypass.

**Recommendation: DO_NOT_RECOMMEND. Decision certainty: HIGH, 100/100 evidence support for the hold. `can_go: false`.**
The score concerns certainty in the source-based hold. It is not readiness, incident probability, or complete test coverage.
The earlier conditional assessment is superseded by the new security failure.

### Metrics summary

| Metric | Current result | Decision meaning |
| --- | --- | --- |
| New case design | **467 instances across 40 use cases** | 271 individual definitions plus 196 outline examples. Design is not execution. |
| New instance execution | **16/467 executed, 3.43%** | **15 pass, one fails; 451 NOT_RUN**. No aggregate completeness claim. |
| New browser / server security results | **Browser 3/3 pass; controller 12/13 pass** | The failed server case is [RN-S002](06-test-cases.md#rn-s002). Inventories remain separate. |
| AC → test case | **7/7 defined and associated with selected assertions** | **3/7 have selected current passing execution**; one partial; three not rerun. Complete assertions remain unknown. |
| AC → code change | **3/7 match within the inspected valid-refresh scope** | Three activity targets are contradictory or missing; one long-session criterion is partial. Complete conformance remains unknown. |
| Code change → test case | **12/12 runtime paths reach selected assertions and passing tests** | Full changed-predicate coverage remains unknown. Six paths are behavioral; six support maintenance. |
| Complete current unit-test condition | **UNKNOWN: only 157/157 selected tests ran** | The full 471-test pass belongs to an older candidate. It cannot establish current full-suite readiness. |
| Code review | **36-path historical review plus inspected Timeout delta** | No new complete independent review. Stale-dialog applicability remains open. |

### Go-live impact and acceptability

**Do not treat all remaining issues as equally acceptable.**
[High/S2 logout revocation](#failure-rn-s002) blocks a positive source-security recommendation.
[High/S2 stale-dialog impact](#failure-review-e2e-01) needs supported-caller validation before review closure.
The recorded [minor backlog scope](evidence/user-input-20261027-backlog-scope.txt) can remain deferred within its stated limits.
Unknown provider behavior and untested consumer journeys still need evidence; they have no recorded blanket acceptance.

[HTML decision view](10-release-confidence.html) · [All failures and impacts in one table](#all-failed-cases-and-observed-user-impact) · [Closure actions](#confidence-increasing-actions).

## Release scope

Assessment date: **29 October 2026, Asia/Singapore**.
The [latest request](evidence/user-input-20261029-refresh-release-report.txt) requires every failure's impact, severity, and an essential HTML view.
The [SDLC clarification](evidence/user-input-20261028-sdlc-coverage.txt) remains in force. Release artifacts remain excluded.
Named phase: **READY for source-bound evidence reconciliation and release-report refresh**.
The supplied cases and retained executions support this assessment. This phase grants no fix, acceptance, or deployment approval.

| Identity | Selected source and evidence |
| --- | --- |
| Current frontend candidate | `66c6411ade58e4d134e381c2baee8ad3f76a8dbf`; local Home edits remain excluded. |
| Frontend baseline | `f025513f696476a9cc8162681410cbd21e029bcb`. It is a local comparison, not an identified production deployment. |
| Assessed BFF / SDK | BFF `19f484efbbfbd4a9d16cdec8a64c4b7fa66e901a`; SDK `b0aa82005e7f14202f85f5ef583f25e42da9eeb3`. |
| New execution identities | [Committed-source binding](evidence/comprehensive-renewal-20261028/execution-source-binding.json), [assertion map](evidence/comprehensive-renewal-20261028/assertion-map.json), and [security binding](evidence/comprehensive-renewal-20261028/security-probe-execution.json). |
| Historical candidate | `e0030f5cf920b715f5831faf7df86cb9789b6d0f`; browser runtime `1b7de4fe5d7db0c7f490a060d4e3b1c441a5c303`. Historical test engine: `78141a4eec8040dd0d1ac8a6579b20f612fca0f0`. |
| Source change since historical pass | Timeout retains the mount-time analytics callback and changes effect dependencies. Exact delta was inspected. |
| Intent and decisions | Requirement version 5 has seven criteria. Refinement review, business acceptance, and deployment authorization remain pending. |
| Scope exclusions | Packaging, release artifacts, deployments, effective target settings, and operational readiness were not reassessed. |

The [three audits](evidence/release-report-20261029/source-manifest.json) bind source, result, assertion, and report identities.
The prior report is preserved at Workbench commit `59b8b32e4`. Earlier raw evidence remains unchanged.

### Business impact

Users need reliable renewal, a usable recovery dialog, stable workspace state, and effective logout.
The new browser passes show retry and successful renewal across six controlled cycles with three empty workspace descriptors.
They also show rapid-click deduplication and local logout ownership. They do not prove embedded application-state retention.
The server failure means logout can leave the same session renewable when access has expired.
A holder of copied refresh credentials can regain authentication. Theft, protected business access, and production frequency were not demonstrated.

### System impact

Shared Home, Timeout, reducers, Axios guards, loading ownership, and server revocation affect authentication boundaries.
Cashflow REST calls inherit the shared client. GraphQL, WebSocket, and notification enforcement have separate boundaries.
The [consumer assessment](10-release-readiness.md#upper-layer-application-impact) and [new transport cases](03-use-cases-renewal.md#main-flow) retain those limits.
Current final-candidate Cashflow mutations, populated workspaces, and connection continuity remain unverified.

## Readiness conditions

The [unit-test principle](../../PRINCIPLE.md#10-delivery-requires-passing-unit-tests) requires complete matching execution with zero failures.
Only the declared 157-test selection is current. Missing full execution is a blocker to GO, not a demonstrated unit failure.
The material server failure takes precedence and establishes NO_GO for this assessed composition.

<details>
<summary>Evidence scorecard: condition status, limits, and closure</summary>

| Dimension | Score / status | Critical | Evidence and limit | Owner | Action | Target / effect | Closure evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Server logout revocation | **5/5 FAILED** | yes | [Current failed assertion](evidence/comprehensive-renewal-20261028/expired-logout-case.json). Direct isolated proof; target exposure unknown. | unknown authentication owner | [A1](#a1) | 5/5 SUPPORTED; remove controlling NO_GO cause. | Same-session replay rejects after expired-access logout; valid and forged-credential controls remain correct. |
| Code review | 3/5 LIMITED | yes | [Review and source audit](evidence/release-report-20261029/metrics-audit.json); stale-dialog supported caller unknown. | unknown application owner | [A2](#a2) | 4/5 SUPPORTED; close review risk. | Caller trace and matching recovery result. |
| Intent and conformance | 3/5 LIMITED | yes | [Current matrices](09-renewal-coverage.md#inspected-implementation-and-assertions); proposed policies remain unresolved. | unknown business owner | [A4](#a4) | 4/5 SUPPORTED; define accepted behavior. | Reviewed scope and canonical expected outcomes. |
| Assertion and case coverage | 3/5 LIMITED | yes | [Metrics audit](evidence/release-report-20261029/metrics-audit.json); 451 new instances unrun; full predicate inventory unknown. | unknown test owner | [A4](#a4) | 4/5 SUPPORTED; close selected critical gaps. | Inspected assertions and matching retained outcomes. |
| Complete candidate unit suite | 2/5 UNKNOWN | yes | [157 selected passes](evidence/comprehensive-renewal-20261028/unit-execution.json); complete suite was not rerun. | unknown test owner | [A3](#a3) | 5/5 SUPPORTED; restore mandatory full-suite evidence. | Complete candidate inventory, command, identities, and zero failures. |
| Browser and consumers | 3/5 LIMITED | yes | [Three browser passes](evidence/comprehensive-renewal-20261028/new-e2e-summary.json); synthetic credentials and empty workspaces. | unknown application and test owners | [A4](#a4) | 4/5 SUPPORTED; support consumer compatibility. | Risk-selected business action, populated-state, and transport results. |
| Business impact | 3/5 LIMITED | yes | [Consolidated impacts](evidence/release-report-20261029/failure-impact-audit.json); exposure unmeasured. | unknown business and security owners | [A1](#a1), [A4](#a4) | 4/5 SUPPORTED; support an informed risk decision. | Actual exposure, affected journeys, and recorded disposition. |
| System impact | 4/5 LIMITED | yes | [Security review](07-security-review-renewal.md#threats-and-controls) and [consumer trace](evidence/up-layer-impact-20261028/consumer-trace.json); replica and transport limits. | unknown architecture owner | [A4](#a4) | 5/5 SUPPORTED; close relevant boundaries. | Matching server, replica, and consumer assertions. |

</details>

Release artifacts contribute no score or penalty here. Their exclusion cannot establish deployed safety.

## Execution evidence

### Current and historical results: separate denominators

| Inventory | Actual outcome | Source and boundary |
| --- | --- | --- |
| New expanded catalog | **467 designed; 16 executed; 15 pass; one fails; 451 NOT_RUN** | [Design and execution audit](evidence/release-report-20261029/metrics-audit.json). Only 3.43% executed. |
| Current selected unit tests | **157/157 pass; ten suites** | [Execution metadata](evidence/comprehensive-renewal-20261028/unit-execution.json). Zero failures, skips, todos, expected-failure declarations, or runner errors in this selection. |
| Current new browser cases | **3/3 pass; 56 assertions** | [Results](evidence/comprehensive-renewal-20261028/new-e2e-summary.json). Actual portal, controlled time, synthetic renewal responses, empty workspace descriptors. |
| Current server security cases | **12 pass, one fails, 13 total** | [Security binding](evidence/comprehensive-renewal-20261028/security-probe-execution.json). Actual controller, RSA, and session service; mocked repositories, entitlements, and servlet objects. |
| Historical complete units | **471/471 pass; 123 suites** | [Original result](evidence/four-checks-20261027/coverage/test-only-final-2/results.json). Older `e0030f5` only. |
| Historical UI/service inventory | **19/27 pass; eight fail** | [Original reconciliation](evidence/four-checks-20261027/e2e/reconciliation.json). Native browser 18/25; DOM/service headless 1/2. Not rerun for current source. |
| Historical review diagnostics | **Nine paired investigations; twenty observations** | [Result index](evidence/review-e2e-20261028/results.json). One locally blocking flow; separate from the 27-case inventory. |

The 157 existing unit tests are not 157 of the 467 new instances. Do not combine those denominators.
The new 467-instance expansion includes 60 policy-open individual cases. Those definitions do not approve new requirements.
The 797/797 factor-pair metric concerns design only. Combination execution remains NOT_RUN.
Complete execution of every proposed case is not an invented release gate. Required checks must follow accepted scope and material risk.

### AC-to-test coverage matrix

| Criterion inventory | Definitions / selected assertion associations | Matching selected current execution | Full assertion coverage |
| --- | --- | --- | --- |
| Seven version-5 criteria | **7/7 defined; 7/7 have selected direct assertion links** | **3/7 pass, 42.86%; one partial; three not rerun** | **UNKNOWN/7**; association is not complete predicate coverage. |
| Sixteen earlier proposed refinements | Retained historical links in [earlier matrix](09-coverage.md#final-ac-to-test-matrix-proposed-refinements) | Earlier source only; current completion not re-established. | Do not promote the historical 14/16 assertion count into current coverage. |

[AC-1](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L187), [AC-2](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L194), and [AC-3](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L201) retain activity gaps.
They were not rerun in the new stage. [AC-4](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L208) remains partial.
[AC-5](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L216), [AC-6](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L223), and [AC-7](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L230) pass selected manual-recovery predicates.
See the [current case, assertion, and execution matrix](09-renewal-coverage.md#ac-to-test-case-coverage).

### AC-to-code-change coverage matrix

| Current scope | Inspected relationship | Conformance |
| --- | --- | --- |
| Seven criteria | **7/7 source locations inspected**, including absent or contradictory behavior | Three bounded matches; one partial; one contradictory; two missing. **Complete equivalence UNKNOWN/7**. |
| Unchanged activity support | Existing Home activity and extension handling | Mouse debounce contradicts the target. Keyboard and scroll renewal bindings are absent. |
| Proposed security and policy cases | Source-backed proposals and open policy | These cases cannot approve their own behavior. Review remains pending. |

The [current code matrix](09-renewal-coverage.md#ac-to-code-change-coverage) separates changed behavior from required unchanged support.
Source locations identifying absent code do not establish implementation coverage.

### Code-change-to-test coverage matrix

| Runtime change inventory | Selected assertion links | Selected passing evidence | Complete changed behavior |
| --- | --- | --- | --- |
| Twelve runtime paths | **12/12** | **12/12** for selected predicates | **UNKNOWN/12** for complete assertions, conformance, and execution. |
| Six behavioral paths | Direct chains retained in the current mapping | Selected current execution | Full behavioral justification remains UNKNOWN/6. |
| Six supporting-maintenance paths | Direct chains retained separately | Selected current execution | Maintenance classification does not establish zero consumer impact. |

The [path-by-path matrix](09-renewal-coverage.md#code-change-to-test-case-coverage) links exact old/new bytes, canonical cases, assertions, and results.
An overall SDLC coverage percentage remains unavailable. `TC >= AC = Code Change` is not established for the complete intended scope.

## Risks and exceptions

### All failed cases and observed user impact

**This table consolidates every open failed result and the separate locally blocking review observation.**
It contains **one current security failure, eight historical failed cases, and one diagnostic issue**.
These ten rows do not form one current execution denominator.
All application owners are unknown. [RN-S002](06-test-cases.md#rn-s002) belongs to the unknown authentication owner.
The source, assertion, and result links are separate in every row.

| Case | First failure point | User impact if live; observed limits | Severity, origin, and acceptability | Exact evidence |
| --- | --- | --- | --- | --- |
'''
body = header + '\n'.join(failure_row(*row) for row in ROWS) + '''

The historical failures retain their original revisions. Relevant activity and response-handler bytes match the current candidate.
The Timeout guard remains unchanged, but its analytics effect changed. Its current blocking effect is source-predicted, not freshly reproduced.
No passing cancellation, overwrite, workspace, or protected-access result is inferred after an earlier assertion stops a case.

### Severity and acceptance advice

**S2 High** means serious authentication-control or core-journey impact under the stated conditions.
**S3 Moderate** means limited service or recovery degradation. **S4 Minor** retains the stated backlog impact.
**UNKNOWN** means the evidence cannot support a defensible user-impact level.
These are analyst classifications unless a row explicitly attributes them to the user. Priority is separate from severity.
No official organizational severity threshold or new human acceptance was supplied.

| Remaining problem | Is it acceptable on present evidence? | Owner and required disposition |
| --- | --- | --- |
| Logout revocation / copied-refresh replay | **No positive security recommendation.** Inherited origin does not waive this newly proved material failure. | unknown authentication and security owners: correct the authenticated revocation path or prove effective non-applicability. |
| Stale dialog with replacement login | **Not closed.** Serious local availability impact exists; supported caller remains unknown. | unknown application owner: trace callers and verify recovery when applicable. |
| User-rated minor activity and cancellation issues | **Can remain in the recorded backlog scope.** This is not blanket release acceptance. | unknown application and business owners: retain limits and existing priorities. |
| Pending-request replacement and inconsistent provider response | **Limited or unknown acceptability.** Delay and supported-provider consequences are unmeasured. | unknown application owner: establish actual service contract and latency impact. |
| Current full suite, populated workspaces, mutations, and transports | **Insufficient evidence.** Missing execution is not proof of a runtime failure. | unknown test and application owners: collect risk-selected matching evidence. |

### Setup failures and resolved history

Setup failures do not establish user-facing product defects. They remain visible beside their corrective reruns.

| Attempt or earlier result | Failure point and effect | Subsequent evidence |
| --- | --- | --- |
| New browser first attempt | Synthetic credentials reached an unmocked activity endpoint. Intended recovery assertions did not execute. | [Setup diagnosis](evidence/comprehensive-renewal-20261028/browser-attempt1/fixture-failure.json); [three final passes](evidence/comprehensive-renewal-20261028/new-e2e-summary.json). |
| Security probe first attempt | Mockito attachment failed before assertions. No product impact was established. | [Initial result](evidence/comprehensive-renewal-20261028/security-probe-execution-initial.json); [executed suite](evidence/comprehensive-renewal-20261028/security-probe-execution.json). |
| Earlier near-expiry review attempts | An undefined access fixture raised a TypeError. Suspected recovery blocking was not established. | [Earlier observations](evidence/review-e2e-20261028/final-focused/browser-summary.json); [successful paired rerun](evidence/review-e2e-20261028/near-expiry-final/browser-summary.json). |
| Earlier diagnostic units | Missing-export mocks and invalid success fixtures preceded the older complete pass. They are not five remaining confirmed runtime regressions. | [Diagnostic comparison](evidence/delivery-confidence-20261026/unit/main-assertion-comparison.json); [historical complete pass](evidence/four-checks-20261027/coverage/test-only-final-2/results.json). |
| Earlier loader and late-acquisition defects | Both were corrected before the older final candidate. Do not count them as current open failures. | [Cancellation closure](evidence/ut-remediation-20261027/final-cancellation-browser/comparison.json); [timer closure](evidence/ut-remediation-20261027/final-timer-control/comparison.json). |

### Other unresolved user-impact boundaries

Populated workspaces, unsaved edits, financial mutation reconciliation, notification reconnects, and server stream revocation remain unverified.
The [living policy questions](05-test-strategy-renewal.md#policy-questions) retain unknown expectations. No new business answer is inferred here.
The [security risk register](07-security-review-renewal.md#threats-and-controls) distinguishes other source risks from demonstrated vulnerabilities.
No release artifact, production test, application fix, publication approval, or deployment occurred in this refresh.

## Confidence score and release status

**NO_GO / DO_NOT_RECOMMEND** supersedes the earlier conditional assessment for this expanded authentication scope.
The controlling dimension is **server logout revocation: 5/5 evidence, FAILED condition**.
Decision certainty is `20 × 5 = 100/100`, HIGH support for holding the matching source composition.
Other dimensions remain incomplete. Their lower scores cannot offset or dilute the directly proved security failure.
Production reachability, occurrence frequency, and affected user counts remain unknown.
If the release excludes this BFF path, record a source-backed applicability decision before reassessment.
Do not silently extend the earlier P4 backlog decision to this newly found P1 security issue.

### Confidence-increasing actions

| ID / order | Owner | Current condition | Action and closure evidence | Target / status effect | Reassessment trigger |
| --- | --- | --- | --- | --- | --- |
| <a id="a1"></a>A1 / first | unknown authentication and security owners | Revocation 5/5 FAILED | Correct authenticated revocation or prove effective non-applicability. Verify expired-access logout, copied-refresh rejection, valid controls, browser flow, and replicas. | 5/5 SUPPORTED. Improves readiness; certainty is already maximal for the present hold. | Inspect matching source and retained closure assertions. |
| <a id="a2"></a>A2 / second | unknown application owner | Review 3/5 LIMITED | Establish supported replacement-login callers. Correct dialog ownership when applicable and rerun [REVIEW-E2E-01](06-test-cases.md#review-e2e-01). | 4/5 SUPPORTED; removes the conditional availability concern. | Inspect caller trace and completed recovery result. |
| <a id="a3"></a>A3 / third | unknown test owner | Complete candidate units 2/5 UNKNOWN | Run the complete applicable suite at the final source. Retain inventory, command, counts, and zero failures without narrowed checks. | 5/5 SUPPORTED; satisfies the mandatory unit condition. | Inspect matching complete results after final source selection. |
| <a id="a4"></a>A4 / fourth | unknown business, security, application, and test owners | Coverage and consumers 3/5 LIMITED | Review open policies. Execute risk-selected populated-state, mutation, transport, and assertion-gap cases with actual expected outcomes. | 4/5 SUPPORTED; supports conformance and informed residual-risk judgment. | Inspect accepted scope, direct assertions, outcomes, and actual dispositions. |

Closing A1 alone does not establish GO. All applicable mandatory conditions and material risks require reassessment.
Actions define closure evidence; they do not grant application-change or deployment authorization.

## Readiness conclusion and authorization

<details>
<summary>Structured assistant assessment and human decision fields</summary>

```yaml
assistant_assessment:
  assessment_state: COMPLETE
  evidence_confidence_score: 100
  confidence_level: HIGH
  confidence_score_basis: Server logout revocation is the controlling 5/5 FAILED dimension; 20 times 5 supports the source-composition hold.
  release_status: NO_GO
  can_go: false
  production_recommendation: DO_NOT_RECOMMEND
  scope_basis: Current source authentication composition, new and retained tests; release artifacts excluded.
  business_impact_refs:
    - 10-release-confidence.md#all-failed-cases-and-observed-user-impact
  system_impact_refs:
    - 07-security-review-renewal.md#threats-and-controls
  controlling_evidence_refs:
    - evidence/comprehensive-renewal-20261028/expired-logout-case.json
    - evidence/release-report-20261029/security-decision-audit.json
  blocking_action_refs: [A1, A2, A3, A4]
  residual_risk_refs:
    - 10-release-confidence.md#severity-and-acceptance-advice
  confidence_increasing_actions: [A1, A2, A3, A4]
  reassess_when:
    - Matching closure evidence or an explicit source-backed applicability decision is inspected.
    - Candidate code, assertions, accepted behavior, or composition changes.
unit_test_status: INCOMPLETE
unit_test_inventory_ref: evidence/comprehensive-renewal-20261028/unit-execution.json
unit_test_command_ref: evidence/comprehensive-renewal-20261028/unit-execution.json
unit_test_total: null
unit_test_passed: null
unit_test_failed: null
unit_test_skipped: null
unit_test_expected_failures: null
unit_test_runner_errors: null
unit_test_completed: false
selected_unit_results:
  total: 157
  passed: 157
  failed: 0
  skipped: 0
  todo: 0
  runner_errors: 0
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

</details>

Null complete-suite counts mean unavailable current full execution. They do not hide the declared selection's passing results.
This is an assistant technical recommendation. No human acceptance, risk exception, or deployment authorization is recorded.

## Facts, inferences, and unresolved questions

- Fact: the current isolated controller case issues access after expired-access logout and valid refresh replay.
- Fact: the 16 newly executed catalog instances contain 15 passes and one failure. The other 451 remain unrun.
- Inference: a matching deployment with copied valid refresh credentials can retain authentication after apparent logout.
- Unknown: deployed reachability, credential theft, protected business access, frequency, and complete required acceptance scope.

The [living question document](05-test-strategy-renewal.md#policy-questions) remains authoritative for unresolved renewal policy.
The report supplies evidence-backed advice. It does not invent a business answer or require the user to rediscover individual failures.

## Findings

| Finding | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| [SEC-01](07-security-review-renewal.md#sec-01), [RN-S002](06-test-cases.md#rn-s002) | Same-session refresh can regain authentication after apparent logout in the isolated source flow. | unknown authentication owner | [A1](#a1). |
| [REVIEW-01](10-issue-catalog.md#review-01) | A valid replacement session remains behind unusable dialog actions in the historical local browser reproduction. | unknown application owner | [A2](#a2). |
| [Current incomplete suite](08-test-execution-renewal.md#run-identity-and-provenance) | Selected passes cannot satisfy the complete-unit delivery condition. | unknown test owner | [A3](#a3). |
| [Remaining SDLC gaps](09-renewal-coverage.md#coverage-inventories-and-summary) | New definitions and complete links do not establish complete behavior conformance. | unknown business and test owners | [A4](#a4). |

## Sources

| Source ID | Locator | Exact identity | Authority and limit |
| --- | --- | --- | --- |
| SRC-session-refresh-report-20261029 | [Exact refresh request](evidence/user-input-20261029-refresh-release-report.txt) | 29 October 2026; SHA-256 in manifest. | User requests consolidated failures, user severity, and essential HTML. |
| SRC-session-comprehensive-tests-20261028 | [Generated-case request](evidence/user-input-20261028-comprehensive-renewal.txt), [strategy](05-test-strategy-renewal.md) | Current source and case hashes retained. | Bounded design and local verification; no approval inferred. |
| SRC-session-refresh-audits-20261029 | [Metrics audit](evidence/release-report-20261029/metrics-audit.json), [failure audit](evidence/release-report-20261029/failure-impact-audit.json), [security audit](evidence/release-report-20261029/security-decision-audit.json) | Exact revisions, source hashes, assertions, results, and limits. | Independent read-only reconciliation. No new execution or acceptance. |
| SRC-session-backlog-scope-20261027 | [Exact scope answer](evidence/user-input-20261027-backlog-scope.txt) | 27 October 2026; retained bytes. | Preserves inherited backlog. Does not waive the newly discovered security failure. |

The [source manifest](evidence/release-report-20261029/source-manifest.json) binds all current claim-bearing inputs.
The [validation record](evidence/release-report-20261029/validation.json) separates document and HTML checks from business verification.
Document lint, workspace validation, links, source hashes, and HTML layout are checked separately.
Unknown ownership, pending business review, unresolved values, and pending writing review remain disclosed lint warnings.
Automated checks do not establish full ASD-STE100 compliance. The complete writing review remains pending.
'''
(TASK / '10-release-confidence.md').write_text(body)

# The companion deliberately presents decisions and grouped impacts, with detail links.
impact_groups = [
    ('S2 High · P1', 'hold', ['RN-S002'], 'Logout can leave copied refresh credentials usable',
     'After expired-access logout, valid refresh replay obtains new access. Copied credentials and a matching deployment are prerequisites. Persistence was mocked.',
     'Hold security sign-off. Correct revocation or prove effective non-applicability.'),
    ('S2 High · P2', 'high', ['REVIEW-E2E-01'], 'A valid replacement session can be blocked by the old dialog',
     'Extend stays disabled and another Logout cannot recover the workspace through these actions. Historical local impact is proved. Current persistence is source-predicted; a supported caller remains unknown.',
     'Resolve caller applicability before positive review sign-off.'),
    ('S4 Minor · P4', 'minor', ['E2E-01', 'E2E-02', 'E2E-03', 'E2E-08'], 'Continuous activity does not start the expected renewal',
     'Mouse, typing, or scrolling can leave the renewal target unmet. Later interruption is possible; logout and lost work were not observed.',
     'Keep the recorded inherited backlog scope. E2E-08 stops before sharing runs; its S4 severity is proposed.'),
    ('S3 Moderate · P4', 'moderate', ['BROWSER-SHARING-PENDING'], 'Repeated activity replaces pending renewal work',
     'Two requests and one cancellation are observed. Slow connections could delay recovery; user blocking remains unmeasured.',
     'Backlog retained; representative-latency acceptability remains unproved.'),
    ('Severity unknown · P3', 'unknown', ['E2E-12'], 'A negative response body still changes access state',
     'The authorization header is installed despite result=false. Supported-provider occurrence and actual user harm remain unknown.',
     'Establish the provider contract before accepting this behavior.'),
    ('S4 Minor · P4', 'minor', ['E2E-18', 'E2E-19'], 'Old activity work remains pending during logout or recovery',
     'Requests are not canceled. Token restoration or overwrite was not observed because later assertions did not run.',
     'Keep the recorded backlog scope. Do not infer an authentication bypass.'),
]
rows=[]
for sev, cls, ids, title, consequence, advice in impact_groups:
    case_links=' · '.join(a(i, '10-release-confidence.md#failure-'+i.lower()) for i in ids)
    sources=[]
    for i in ids:
        source=CASES[i]['source_links'][0]
        if source not in sources: sources.append(source)
    source_links=' · '.join(a('Source' if j==0 else 'Source '+str(j+1),x) for j,x in enumerate(sources))
    result_links=' · '.join(a(i+' result',CASES[i]['result_link']) for i in ids)
    rows.append(f'<tr><td><span class="severity {cls}">{html.escape(sev)}</span></td><td><strong>{html.escape(title)}</strong><p>{html.escape(consequence)}</p><div class="refs">{case_links}</div></td><td><p>{html.escape(advice)}</p><div class="refs">{source_links} · {result_links}</div></td></tr>')
html_text='''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Session Refresh release decision, SDLC coverage and remaining user impacts. 29 October 2026.">
<title>Session Refresh — release decision</title>
<style>
:root{color-scheme:light;--ink:#152638;--muted:#526474;--line:#dbe3e9;--red:#922b32;--paper:#fff;--bg:#f3f6f8;--blue:#155b91}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}main{max-width:1130px;margin:auto;padding:36px 28px 24px}a{color:var(--blue);text-decoration-thickness:1px;text-underline-offset:3px}a:focus-visible{outline:3px solid #306c9d;outline-offset:4px;border-radius:2px}.eyebrow{color:var(--muted);font-size:12px;letter-spacing:.11em;font-weight:700;text-transform:uppercase}h1{font-size:36px;letter-spacing:-.035em;line-height:1.15;margin:8px 0 10px}h2{font-size:21px;letter-spacing:-.02em;margin:0 0 14px}p{margin:0 0 12px}.meta{color:var(--muted);font-size:13px}.decision{margin:24px 0;background:#fff2f2;border:1px solid #e8c2c5;border-left:6px solid var(--red);border-radius:10px;padding:22px 24px}.decision-head{display:flex;align-items:center;gap:14px;margin-bottom:12px}.badge{background:var(--red);color:white;font-size:13px;font-weight:800;letter-spacing:.06em;border-radius:5px;padding:5px 10px}.decision h2{margin:0;font-size:23px}.decision p{max-width:950px}.certainty{font-size:13px;color:#6c3339}.nav{display:flex;gap:18px;flex-wrap:wrap;font-size:13px;margin-top:18px}.cards{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin:18px 0 24px}.card{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:17px}.label{font-size:12px;color:var(--muted);font-weight:650}.number{display:block;font-size:28px;line-height:1.3;font-weight:750;letter-spacing:-.03em;margin:7px 0}.small{font-size:12px;color:var(--muted)}.panel{padding:23px;background:var(--paper);border:1px solid var(--line);border-radius:10px;margin:16px 0}.table-wrap{overflow:auto}table{width:100%;border-collapse:collapse;text-align:left;font-size:13px}th{font-size:11px;letter-spacing:.04em;text-transform:uppercase;color:var(--muted);padding:10px 12px;border-bottom:2px solid var(--line)}td{padding:15px 12px;vertical-align:top;border-bottom:1px solid var(--line)}tbody tr:last-child td{border-bottom:0}td p{margin:5px 0 8px}td:first-child{width:145px}.refs{font-size:11px;line-height:1.8;overflow-wrap:anywhere}.severity{display:inline-block;font-size:11px;font-weight:750;border-radius:5px;padding:5px 7px;white-space:nowrap}.hold,.high{color:#8c222b;background:#fde8e9}.moderate{color:#76520b;background:#fff2ce}.minor{color:#355b4b;background:#edf4ef}.unknown{color:#535163;background:#efedf6}.coverage td:first-child{width:220px;font-weight:650}.next{display:grid;grid-template-columns:1fr 1fr;gap:24px}.next ol{padding-left:18px;margin:0}.next li{margin-bottom:9px}.note{background:#f4f7f9;padding:12px 14px;border-radius:7px;font-size:12px;color:var(--muted);margin-top:15px}.footer{font-size:11px;color:var(--muted);margin:21px 0 0;line-height:1.8}.docs{display:flex;gap:12px 20px;flex-wrap:wrap}.risk-intro{color:var(--muted);font-size:13px;margin-bottom:12px}
@media(max-width:760px){main{padding:22px 14px}h1{font-size:29px}.cards{grid-template-columns:repeat(2,minmax(0,1fr))}.decision{padding:18px}.decision-head{align-items:flex-start;flex-direction:column;gap:8px}.decision h2{font-size:21px}.panel{padding:15px}.next{grid-template-columns:1fr;gap:18px}th,td{padding:10px 8px}.impact-table{min-width:680px}}
@media(max-width:760px){.impact-table{min-width:0}.impact-table thead{display:none}.impact-table tbody,.impact-table tr,.impact-table td{display:block}.impact-table tr{padding:10px 0;border-bottom:1px solid var(--line)}.impact-table tr:last-child{border-bottom:0}.impact-table td{width:auto;border:0;padding:4px 8px}.impact-table td:first-child{width:auto}.impact-table td:last-child{padding-bottom:10px}.impact-table .refs{font-size:12px}.coverage{min-width:0}.coverage td:first-child{width:auto}}
@media print{body{background:white}main{max-width:none;padding:0}.decision,.panel,.card{break-inside:avoid}.nav{display:none}a{color:inherit}.table-wrap{overflow:visible}.impact-table{min-width:0}.cards{grid-template-columns:repeat(4,1fr)}.panel{padding:15px}body{font-size:11px}h1{font-size:27px}}
</style>
</head>
<body>
<main>
<header>
<div class="eyebrow">Release decision · 29 October 2026</div>
<h1>Session Refresh</h1>
<p class="meta">Source candidate <a href="10-release-confidence.md#release-scope">66c6411</a> · Authentication composition review · Release artifacts excluded</p>
</header>
<section class="decision" aria-labelledby="decision-title">
<div class="decision-head"><span class="badge">NO GO</span><h2 id="decision-title">The remaining problems are not acceptable as a whole.</h2></div>
<p><strong>Hold the release recommendation.</strong> Logout with expired access reports success, yet copied valid refresh credentials can still obtain new access. This inherited server defect is proved in an isolated controller test. Production exposure remains unverified.</p>
<p class="certainty"><strong>Recommendation: DO_NOT_RECOMMEND · Decision certainty: HIGH, 100/100 support for the hold.</strong><br>This is certainty in the source-based decision, not a readiness percentage or incident probability.</p>
<nav class="nav" aria-label="Report sections"><a href="#impacts">All remaining failure groups</a><a href="#coverage">SDLC coverage</a><a href="#actions">Closure actions</a><a href="10-release-confidence.md">Full report and evidence</a></nav>
</section>
<section class="cards" aria-label="Essential metrics">
<div class="card"><div class="label">New cases executed</div><span class="number">16 / 467</span><div class="small">15 pass · 1 fails · 451 not run<br>3.43% of designed instances</div></div>
<div class="card"><div class="label">Current new browser / security</div><span class="number">3/3 · 12/13</span><div class="small">Browser passes · server security<br>One failed replay assertion</div></div>
<div class="card"><div class="label">ACs with selected current passes</div><span class="number">3 / 7</span><div class="small">1 partial · 3 not rerun<br>Full conformance unknown</div></div>
<div class="card"><div class="label">Current unit-test selection</div><span class="number">157 / 157</span><div class="small">Selected tests pass<br>Complete current suite not run</div></div>
</section>
<section class="panel" id="impacts" aria-labelledby="impacts-title">
<h2 id="impacts-title">What users could experience if this goes live</h2>
<p class="risk-intro">Every remaining failed case is represented below: one current security failure, eight historical failed cases, and one separate local review issue. Their execution denominators remain separate.</p>
<div class="table-wrap"><table class="impact-table"><thead><tr><th scope="col">Severity / priority</th><th scope="col">Failure point and user impact</th><th scope="col">Acceptability and evidence</th></tr></thead><tbody>
'''+ '\n'.join(rows) + '''
</tbody></table></div>
<div class="note"><strong>Severity:</strong> S2 High = serious authentication-control or core-journey impact; S3 Moderate = limited service degradation; S4 Minor = backlog impact. Conditional impact is not a proved production incident. User S4 ratings remain intact; other ratings are analyst proposals. No blanket risk acceptance is recorded. Owners remain unknown.</div>
</section>
<section class="panel" id="coverage" aria-labelledby="coverage-title">
<h2 id="coverage-title">SDLC coverage — links, behavior, and execution</h2>
<div class="table-wrap"><table class="coverage"><thead><tr><th scope="col">Relationship</th><th scope="col">Evidence</th><th scope="col">Material limit</th></tr></thead><tbody>
<tr><td>AC → test case</td><td>7/7 defined and associated with selected assertions. 3/7 selected current passing.</td><td>Complete assertion coverage remains unknown. One AC is partial; three activity ACs were not rerun.</td></tr>
<tr><td>AC → code change</td><td>Three bounded matches; one partial; one contradictory; two missing.</td><td>All seven source locations inspected. Locations do not establish complete conformance.</td></tr>
<tr><td>Code change → test case</td><td>12/12 runtime paths reach selected assertions and passing tests.</td><td>Complete changed-predicate coverage and behavioral equivalence remain unknown.</td></tr>
</tbody></table></div>
<p class="small">40 use cases and 467 new instances are designed. Passing test counts and design links do not measure complete SDLC coverage. <a href="09-renewal-coverage.md">Detailed current matrices</a>.</p>
<div class="note"><strong>Code review:</strong> 36 paths were reviewed historically; the later Timeout delta was inspected. Complete independent current review was not repeated. Stale-dialog caller applicability remains open. <a href="10-release-confidence.md#readiness-conditions">Review evidence and limits</a>.</div>
</section>
<section class="panel next" id="actions" aria-labelledby="actions-title">
<div><h2 id="actions-title">Required before reassessment</h2><ol>
<li><strong>Authentication / security owner:</strong> correct logout revocation or prove the selected path inapplicable. Verify replay rejection and controls.</li>
<li><strong>Application owner:</strong> identify supported replacement-login callers and resolve stale-dialog recovery when reachable.</li>
<li><strong>Test owner:</strong> run the complete applicable unit suite at the final candidate. The older 471-test pass covers earlier bytes.</li>
<li><strong>Business and test owners:</strong> resolve open policy and execute critical populated-workspace, mutation, and transport journeys.</li>
</ol><p class="small">Owners are unknown. Closing the security failure alone does not establish GO. <a href="10-release-confidence.md#confidence-increasing-actions">Closure evidence and decision rules</a>.</p></div>
<div><h2>Read the supporting documents</h2><div class="docs"><a href="10-release-confidence.md#all-failed-cases-and-observed-user-impact">Every failed case in one table</a><a href="07-security-review-renewal.md#sec-01">Security finding</a><a href="08-test-execution-renewal.md">Current execution</a><a href="09-renewal-coverage.md">SDLC matrices</a><a href="05-test-strategy-renewal.md">Strategy and policy questions</a><a href="06-test-cases.md#expansion-navigation">Canonical test catalog</a></div><div class="note"><strong>Evidence boundaries:</strong> controlled browser time, synthetic renewal responses, empty workspace descriptors, and mocked server persistence. No new tests, fixes, production verification, or deployment occurred during this refresh.</div></div>
</section>
<footer class="footer">Current source: frontend 66c6411; BFF 19f484e. Historical failures retain their original source bindings. Human acceptance and deployment authorization remain pending.<br>Writing review: ASD-STE100 · automated checks: PASSED · full ASD review: PENDING. <a href="evidence/release-report-20261029/validation.json">Validation and limits</a>.</footer>
</main>
</body>
</html>
'''
(TASK / '10-release-confidence.html').write_text(html_text)
summary = {
    'assessment_date': '2026-10-29', 'timezone': 'Asia/Singapore',
    'release_status': 'NO_GO', 'production_recommendation': 'DO_NOT_RECOMMEND',
    'can_go': False, 'evidence_confidence_score': 100, 'confidence_level': 'HIGH',
    'score_basis': 'Server logout revocation is the controlling 5/5 FAILED dimension. Certainty in holding the assessed source composition.',
    'candidate': '66c6411ade58e4d134e381c2baee8ad3f76a8dbf',
    'bff': '19f484efbbfbd4a9d16cdec8a64c4b7fa66e901a',
    'new_catalog': {'designed': 467, 'executed': 16, 'passed': 15, 'failed': 1, 'not_run': 451},
    'current_selected_units': {'passed': 157, 'total': 157, 'complete_candidate_suite': 'NOT_RUN'},
    'current_new_browser': {'passed': 3, 'total': 3},
    'current_security_controller': {'passed': 12, 'total': 13, 'failed': 1},
    'sdlc': {'ac_to_test_selected_assertion_links': '7/7', 'ac_selected_passing': '3/7',
             'ac_complete_assertion_coverage': 'UNKNOWN/7', 'complete_conformance': 'UNKNOWN/7',
             'changed_path_selected_assertions': '12/12', 'complete_changed_behavior': 'UNKNOWN/12'},
    'failure_inventory': failures['inventory'],
    'essential_impact_groups': [{'severity': g[0], 'ids': g[2], 'failure_point': g[3], 'impact': g[4], 'acceptability': g[5]} for g in impact_groups],
    'scope_exclusions': ['Release artifacts', 'Deployment and operational readiness'],
    'approval': None, 'deployment_authorization': None,
}
(EVIDENCE / 'decision-summary.json').write_text(json.dumps(summary, indent=2)+'\n')
print('Rendered Markdown, essential HTML, and decision-summary.json.')
