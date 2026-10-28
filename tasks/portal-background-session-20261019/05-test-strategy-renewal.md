---
artifact_kind: test-strategy-plan
id: PLAN-comprehensive-session-renewal
version: 1
status: draft
owner: unknown
source_refs: [SRC-comprehensive-renewal-20261028]
related_ids: [REQ-active-session-renewal, TEST-session-canonical-20261021]
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

# Comprehensive session renewal test strategy

> **Critical conclusions: An inherited logout revocation defect blocks security acceptance.**
> Action: correct and verify [SEC-01](07-security-review-renewal.md#sec-01). Consequence: copied refresh credentials can recover access after apparent logout.
> Owner: unknown authentication owner. Evidence: [failed controller assertion](evidence/comprehensive-renewal-20261028/expired-logout-case.json).
> The probe used actual controller code with mocked repositories. Production applicability remains unverified.

## Goal and scope

The [high-priority request](evidence/user-input-20261028-comprehensive-renewal.txt) governs this bounded test-design and security-assessment stage.
Use the existing implementation-supplied entry route. Preserve prior intake, executions, and business decisions.
Named phase: `READY` for comprehensive case design, source inspection, and isolated local verification.
The request defines the scope. Existing requirement criteria define supported renewal expectations.
Unknown workspace and transport policies remain proposed checks. They do not block independent test design.
Application fixes, publication, deployment, and acceptance remain separate activities.

## Inputs and revisions

| Resource | Exact identity | Evidence and limit |
| --- | --- | --- |
| Shell candidate | `66c6411ade58e4d134e381c2baee8ad3f76a8dbf` | [Committed-source binding](evidence/comprehensive-renewal-20261028/execution-source-binding.json); local edits excluded |
| Shell comparison base | `f025513f696476a9cc8162681410cbd21e029bcb` | [Assertion map](evidence/comprehensive-renewal-20261028/assertion-map.json) |
| BFF candidate | `19f484efbbfbd4a9d16cdec8a64c4b7fa66e901a` | [Security source register](evidence/comprehensive-renewal-20261028/security-review.json) |
| SDK candidate | `b0aa82005e7f14202f85f5ef583f25e42da9eeb3` | [Security source register](evidence/comprehensive-renewal-20261028/security-review.json) |
| Consumer source | Per-file hashes and revision claims | [Source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json); worktree observations are separate |
| Requirement | Candidate version 5; SHA-256 in source manifest | [Seven criteria](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria); publication review pending |

The [current catalog](06-test-cases.md) remains the single case-definition source.

## Planned coverage

The [40 use cases](03-use-cases-renewal.md#main-flow) link 271 individual cases and three outlines.
The outlines contain 196 examples. The expansion therefore contains 467 test instances.
Historical cases remain separately preserved. These counts describe the new expansion only.

| Scope | Individual cases | Canonical definition |
| --- | --- | --- |
| Activity, timing, manual recovery, payloads, races, loops, lifecycle, and failures | 117 | [Expansion navigation](06-test-cases.md#expansion-navigation) |
| Workspaces, loading, transports, and browser contexts | 96 | [Expansion navigation](06-test-cases.md#expansion-navigation) |
| Adversarial security | 55 | [Security cases](06-test-cases.md#rn-s001) |
| Newly executed browser probes | 3 | [RN-X001](06-test-cases.md#rn-x001), [RN-X002](06-test-cases.md#rn-x002), [RN-X003](06-test-cases.md#rn-x003) |

Every case has explicit Gherkin assertions and an evidence class.
Sixty individual cases retain unresolved policy. No new acceptance rule is inferred from those observations.
Case priorities are analyst proposals. Existing business backlog priorities remain distinct.

The combinatorial design covers all 797 declared factor-value pairs with 37 examples across 11 factors.
The Cartesian design population contains 1,866,240 combinations. Those combinations were not all executed or enumerated.
Another 144 examples exhaust a selected four-factor subset. Fifteen examples exhaust one six-event partial-order model.
The [combination manifest](evidence/comprehensive-renewal-20261028/combinations.json) defines factors, seed, coverage, feasibility, and limits.
Finite design and execution cannot cover all possible histories or prove absolute security.

## Change-derived case inventory

The [three matrices](09-renewal-coverage.md#inspected-implementation-and-assertions) map criteria, changed paths, and inspected assertions separately.
The comparison contains 12 changed runtime paths. Six support maintenance; six contain behavioral changes.
The unchanged activity handlers remain explicit. Their target gaps retain the recorded backlog disposition.
The [independent design review](evidence/comprehensive-renewal-20261028/independent-core-design-review.json) identified nine specification corrections.
The [resolution record](evidence/comprehensive-renewal-20261028/design-review-resolution.json) records their final disposition.

## Environment and data

Use isolated local fixtures with synthetic identities. Record mocks, controlled time, and unavailable target services.
Never retain real credentials. Save each completed result before continuing execution.
The browser fixture uses three empty workspace descriptors. Loaded application data and real sockets remain unverified.
The browser uses Edge with controlled time and synthetic authentication. The controller probe uses servlet mocks and mocked repositories.
See [execution boundaries](08-test-execution-renewal.md#browser-environment-and-suite-completeness) and [security boundaries](07-security-review-renewal.md#security-verification).

Risk is high because stale credentials can cross identity boundaries. Workspace loading and transport reconnection increase concurrency.

## Entry and completion conditions

Entry is `READY` for the bounded scope above.
Completion requires canonical definitions, source mapping, security findings, document checks, and a scoped commit.
Security acceptance requires reviewed policies and representative target evidence. That acceptance is not established here.
The completed test-design stage is `READY` for owner review and separately scoped execution planning.
Application correction and target security acceptance remain blocked by their respective findings and evidence gaps.

## Execution planning

```yaml
execution_status: FAILED
repository_revision: 66c6411ade58e4d134e381c2baee8ad3f76a8dbf
test_revision: SHA-256 identities in execution and source manifests
environment_identity: isolated Edge frontend and Java controller fixtures
planned_run_locator: evidence/comprehensive-renewal-20261028/
actual_results:
  targeted_unit: 157 passed of 157
  browser_e2e: 3 passed of 3
  controller_security: 12 passed and 1 failed of 13
retained_execution_refs:
  - evidence/comprehensive-renewal-20261028/unit-execution.json
  - evidence/comprehensive-renewal-20261028/new-e2e-summary.json
  - evidence/comprehensive-renewal-20261028/security-probe-execution.json
approval: null
```

## Facts, inferences, and unresolved questions

The [requirement](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria) contains seven criteria and pending publication review.
Existing reports contain local results and unresolved release evidence. New definitions do not establish passing execution.

## Findings

| Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- |
| [Request](evidence/user-input-20261028-comprehensive-renewal.txt) | Broad coverage needs explicit finite boundaries | unknown application owner | Record dimensions, pair coverage, and exclusions |
| [SEC-01](07-security-review-renewal.md#sec-01) | One inherited revocation assertion fails | unknown authentication owner | Correct revocation and rerun replay checks |

## Sources

| Source ID | Locator | Exact revision | Hash | Owner, authority, and limits |
| --- | --- | --- | --- | --- |
| SRC-comprehensive-renewal-20261028 | [Exact request](evidence/user-input-20261028-comprehensive-renewal.txt) | user-message-20261028 | See stage manifest | User; test generation and security assessment authorization |

## Policy questions

This is the living question register for the new renewal-policy scope. Existing intake answers remain preserved.
The following questions affect acceptance. They do not block independent source inspection or isolated test design.
Options are proposals. No business answer is selected. Each answer can be another rule, unknown, or a named contact.

### Q-RN-01: Input beyond ordinary shell activity

Mouse, keyboard, and scroll targets already exist. Cross-origin iframe input and passive transport activity have different observation boundaries.
Evidence: [activity cases](06-test-cases.md#rn-a007) and [transport findings](evidence/comprehensive-renewal-20261028/workspace-transport-findings.json).
Question: which cross-origin input, heartbeat, or passive-message events qualify as user activity?
Suggested options: only explicit user input; named additional events; unknown or named contact.
Answer: _Unanswered_. Owner: unknown business owner. Consequence: acceptance remains blocked for the affected input classes.

### Q-RN-02: Recovery without usable credentials

Valid-credential recovery has existing criteria. Recovery without usable access or refresh remains unresolved in the [frozen intake](01-intake.md#material-open-questions).
Question: should this boundary require fresh SSO, preserve another recovery method, or follow another rule?
Suggested options: fresh SSO; a named alternative; unknown or named contact.
Answer: _Unanswered_. Owner: unknown authentication owner. Consequence: absent-credential recovery cannot receive acceptance.

### Q-RN-03: Pending renewal and retry limits

The prompt must remain truthful while renewal is pending. No reviewed maximum pending duration or automatic retry budget was found.
Evidence: [never-settled renewal](06-test-cases.md#rn-f011) and [source deadline boundaries](06-test-cases.md#rn-b004).
Question: what deadline, cancellation action, and retry rule apply to an indefinitely pending request?
Suggested options: reviewed service timeout; explicit user cancellation with a named deadline; unknown or named contact.
Answer: _Unanswered_. Owner: unknown product and service owners. Consequence: availability acceptance remains blocked for that boundary.

### Q-RN-04: Logout scope and refresh replay

The BFF can revoke one session identifier. The [security review](07-security-review-renewal.md#residual-risks-and-review) found no reviewed global or single-use policy.
Question: what scope covers other tabs, devices, rotated refresh credentials, and service replicas?
Suggested options: current session only; all sessions for the user; another defined scope, unknown, or named contact.
Answer: _Unanswered_. Owner: unknown security owner. Consequence: global logout and rotation acceptance remain blocked.
This question does not defer the reproduced same-session revocation defect.

### Q-RN-05: Workspace continuity and changed permissions

The shell preserves workspace descriptors. Descriptor continuity does not establish recovery of unsaved business data.
Evidence: [workspace cases](06-test-cases.md#rn-w001) and [prior-user data protection](06-test-cases.md#rn-s042).
Question: which drafts, selections, results, and subscriptions can survive renewal, logout, or reduced permissions?
Suggested options: reviewed per-application retention rules; descriptors only with authorized reload; unknown or named contact.
Answer: _Unanswered_. Owner: unknown application and business owners. Consequence: workspace-data retention acceptance remains blocked.

### Q-RN-06: Continued connection authorization

GraphQL WebSocket and STOMP clients use separate connection paths. Server authorization and revocation deadlines remain unavailable.
Evidence: [transport cases](06-test-cases.md#rn-t001) and [stream threat](07-security-review-renewal.md#threats-and-controls).
Question: when must each transport reauthenticate, stop delivery, and discard buffered data after identity or permission changes?
Suggested options: every protected message; handshake plus a reviewed revocation mechanism; unknown or named contact.
Answer: _Unanswered_. Owner: unknown transport and security owners. Consequence: transport security acceptance remains blocked.

### Q-RN-07: Mutation recovery and long transfers

Renewal does not define whether a completed mutation can be retried. Upload and download authorization can outlive individual HTTP requests.
Evidence: [mutation replay case](06-test-cases.md#rn-s053) and [long-transfer cases](06-test-cases.md#rn-t020).
Question: which operations can retry, and which idempotency and authorization checkpoints apply?
Suggested options: reviewed service-specific contract; no automatic mutation retry; unknown or named contact.
Answer: _Unanswered_. Owner: unknown business-service owners. Consequence: mutation and transfer acceptance remains blocked.

## Document and automation checks

Artifact lint passed with zero errors. Unknown owners, unresolved policy, pending business review, and pending ASD review remain warnings.
The [design validation](evidence/comprehensive-renewal-20261028/design-validation.json) checks local references, source hashes, case identities, and combination coverage.
The [UI Gherkin checker](evidence/comprehensive-renewal-20261028/gherkin-check.json) returns `UNVERIFIED` for the three executed browser specifications.
It reports zero hard failures. Candidate intent review and complete semantic binding review remain pending.
Actual browser execution remains separate from that authoring-readiness result.
