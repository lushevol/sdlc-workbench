---
artifact_kind: change-request
id: CR-SINGLE-UI-CES-300
version: 1
status: draft
owner: unknown
source_refs: [USER-IMPLEMENTATION, SDK-BASE, CES-SAMPLES]
related_ids: [REQ-SINGLE-UI-CES-001]
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

# Implement SDK CES migration version 3.0.0

> **SDK 3.0.0 is implemented; live permission equivalence remains unproved.**
> Action: compare approved assignments and compile actual consumers before acceptance.
> Consequence: local passing tests cannot establish full deployed compatibility.
> Owner: unknown for acceptance. Evidence: [execution report](08-test-execution-report.md) and [sample differences](evidence/role-compatibility-design.md#sample-comparisons).

## Request and source facts

- Requester: User in this Codex chat.
- Current baseline: [frozen intake](01-intake.md), SDK `b0aa82005e7f14202f85f5ef583f25e42da9eeb3`.
- Request source: [exact implementation clarification](evidence/user-clarification-implementation.md).
- Supported rationale: preserve the old contract where possible, assess full compatibility, set version `3.0.0`, and add tests.
- Evidence limit: supplied CES samples do not establish current deployed API behavior or equivalent account assignments.
- Entry route and basis: requirements first; user now authorizes implementation and tests.
- Actual chronology: original analysis completed on 1 November 2026. This clarification follows that assessment.

## Stage boundary and readiness

- Stage: CES role-detail adapter implementation, packaging, and complete SDK tests.
- Frozen intake: `01-intake.md`, Git `1ed95a9f2`, SHA-256 `2affec0a12f0c41f7211a949b139bc3dbd9c2e5dca5417374611679e070c11ff`.
- Compared implementation: SDK base `b0aa82005e7f14202f85f5ef583f25e42da9eeb3`; candidate initially absent.
- Readiness: READY for SDK implementation and local verification within the compatibility boundaries below.
- Assessor and time: Codex, 1 November 2026, Asia/Singapore.
- Rationale and evidence: user supplied version, token ownership, compatibility objective, and testing authorization.
- Blocked actions: artifact publication, deployment, and claims of full live permission equivalence.
- Resolution owner and next action: Codex; implement scoped per-role mapping and retain compatibility limits.
- Intake integrity result: matched preserved baseline before this stage.

### Selected compatibility design

Use the assigned-role endpoint `/fmces/v1/entitlement/user/{userId}`.
Its supplied response binds `featureActionDtos` to each `entitlementName`.
The aggregate endpoint remains insufficient for exact per-role results.
Select application ID/name and entity aliases through configuration. No RATAN identity becomes a library default.
Role mappings act as an allowlist when configured. Unmapped names remain unchanged only when no role map is configured.
Optional feature scopes and subject aliases preserve reviewed legacy entity/subject boundaries.
Preserve source action order and duplicates. Reject ambiguous alias collisions instead of merging unrelated roles.
Empty assigned roles produce an empty result. Assigned roles without functional grants retain an empty role map.

Keep `getEntitlements(String)` and the existing three-argument constructor.
Add an explicit-token overload and optional caller-provided `FmaaTokenProvider` bean.
Legacy calls return an empty map on failures. Explicit-token calls expose typed, sanitized exceptions.
Treat CES failures as no new grant. Do not cache tokens, retry requests, or fall back to EMS2.
This is the invited failure-handling recommendation implemented as additive behavior.

The user authorizes best-effort compatibility and tests. Missing deployed assignments cannot change this bounded adapter design.
They block broader parity acceptance, rather than local implementation.

## Proposed change

| Aspect | Current baseline | Proposed replacement or addition | Basis |
| --- | --- | --- | --- |
| Version | `2.0.0-SNAPSHOT`. | `3.0.0`. | User input. |
| Lookup | EMS2 account GET and grants POST. | CES role-aware lookup preserving `entity:role -> subject -> actions` where supported. | User compatibility direction. |
| Authentication | No explicit outbound token in old EMS2 lookup. | SDK caller provides FMAA token through an injectable provider or explicit overload. | User input; concrete API design follows source review. |
| Failure handling | Errors return an empty map. | Preserve legacy method behavior where practical. Offer explicit errors for callers that need failure distinctions. | Engineering proposal; no access granted on errors. |
| Tests | None in the supplied checkout. | CES mapping, errors, zero EMS2 traffic, wiring, and JWT regression tests. | User input and consequential boundaries. |

## Scope and affected artifacts

| Artifact ID | Exact version or revision | Proposed effect | Evidence | Risk and basis | Owner |
| --- | --- | --- | --- | --- | --- |
| SDK | `b0aa82005e7f14202f85f5ef583f25e42da9eeb3`. | Client, properties, configuration, and tests. | [source assessment](evidence/sdk-scope.md). | High access consequence if mapping broadens grants; tests must check isolation. | Codex. |
| Consumer applications | Deployed versions unknown. | Usage instructions and compatibility evidence only. | [consumer scope](evidence/consumer-scope.md). | Old static validator calls differ from the supplied instance API. | unknown. |
| Knowledge | SDK intent candidate. | Record clarified compatibility and token-ownership intent. | [user clarification](evidence/user-clarification-implementation.md). | Keep candidate state and publication review separate. | Codex. |

## User impact

| Actor and journey | Trigger | Before and after behavior | Benefit or adverse consequence | Evidence and limit | Owner | Next action |
| --- | --- | --- | --- | --- | --- | --- |
| SDK caller | Read permissions. | EMS2 map becomes CES-backed map. | Preserve downstream permission checks where semantics map. | Source-backed target; no live result. | Codex. | Compare role-specific fixtures and negative scopes. |
| SDK caller | CES failure. | Legacy method returns no grants; explicit API can distinguish failure. | No grant expansion from errors. | Engineering proposal. | Codex. | Assert empty/failed results separately. |

## System impact

| Changed path | Affected caller or consumer | Interface or state effect | Failure or concurrency risk | Evidence and limit | Owner | Next action |
| --- | --- | --- | --- | --- | --- | --- |
| `AuthorizationService`, implementation, and bean wiring. | Direct SDK entitlement callers. | Preserve existing method; add token-supply path. | Token lifetime belongs to caller; do not retain raw tokens. | [consumer assessment](evidence/consumer-scope.md). | Codex. | Inspect imports and implement tests. |
| POMs and SDK package. | Application dependency resolution. | Publishable version becomes `3.0.0`. | Framework compatibility remains bounded to tested runtimes. | [SDK POM](../../repos/libraries/single-ui-sdk-starter/pom.xml). | Codex. | Run the complete declared suite and package. |

## Options and consequences

| Option | Expected consequence | Evidence or inference | Required decision |
| --- | --- | --- | --- |
| Aggregate CES endpoint only. | Cannot attribute each merged grant to its role. | [CES findings](evidence/ces-reference.md). | Avoid fabricated role grants. |
| CES assigned-role detail endpoint. | Can preserve per-role feature/action grouping when the response provides it. | [role detail sample](../draft-ces-migration/api/-fmces-v1-entitlement-user-1481696.json). | Inspect identity, scopes, missing data-role semantics, and supported endpoint limits. |

## Proposed acceptance and validation

Canonical cases reside in [06-test-cases.md](06-test-cases.md).
All twelve canonical cases have controlled passing execution. The [execution report](08-test-execution-report.md) records their limits.

| Changed requirement or criterion ID | Canonical change location | Required validation | Current result | Evidence reference |
| --- | --- | --- | --- | --- |
| Contract compatibility. | [canonical cases](06-test-cases.md). | Compare representative maps, reject unrelated scopes, and preserve role boundaries. | PASSED within local controlled scope. | [Final results](evidence/candidate-run-04/result.json). |
| Token provision. | [canonical cases](06-test-cases.md). | Inspect bearer header and provider invocations; no token storage or logging. | PASSED within local controlled scope. | [Final results](evidence/candidate-run-04/result.json). |
| Failure behavior. | [canonical cases](06-test-cases.md). | Assert no grants on errors and explicit error classification where offered. | PASSED within local controlled scope. | [Final results](evidence/candidate-run-04/result.json). |
| Existing authentication behavior. | [canonical cases](06-test-cases.md). | JWT issuer/signature/expiry and filter attributes. | PASSED within local controlled scope. | [Final results](evidence/candidate-run-04/result.json). |

## Implementation and release proposal

- Proposed implementation scope: SDK `3.0.0`, tests, README/setup/dependency documentation, and task evidence.
- Proposed release: `3.0.0`; publication and deployment are not authorized.
- Estimate and basis: unknown; compatibility and Maven dependency availability determine remaining work.
- Reversal approach: restore prior SDK artifact and configuration before cutover under application-owner control.

### Bounded exploration

Not applicable to completed product changes. Source investigation occurs within the user's implementation request.
No disposable experimental application or unrelated infrastructure is planned.

## Sources and evidence limits

| Source ID | Locator | Exact revision | Available hash | Owner, authority, and limit |
| --- | --- | --- | --- | --- |
| USER-IMPLEMENTATION | [User clarification](evidence/user-clarification-implementation.md). | 2026-11-01 message. | To be recorded in implementation manifest. | User; implementation intent and token ownership. |
| SDK-BASE | [source manifest](evidence/source-manifest.json). | `b0aa82005e7f14202f85f5ef583f25e42da9eeb3`. | Exact hashes in manifest. | Local source owner unknown; not deployed proof. |
| CES-SAMPLES | [role details](../draft-ces-migration/api/-fmces-v1-entitlement-user-1481696.json). | Capture metadata unknown. | Existing sample manifest. | User-supplied example; current live contract unverified. |

## Unknowns and blockers

| Finding or question | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| Full role/data equivalence. | Samples differ in role assignments and structure. | Cannot claim 100% deployed permission equivalence. | unknown. | Compare supported scoped fixtures and report gaps. |
| Live service and deployed consumers. | No credential or deployment evidence supplied. | Integration/UAT and consumer adoption remain unverified. | unknown. | Test under authorized environment access after local implementation. |

## Stage evidence and completion

| Stage | Required evidence | Record or execution locator | Current result | Remaining blocker and next action |
| --- | --- | --- | --- | --- |
| Impact analysis | Exact source and callers. | [earlier SDK](evidence/sdk-scope.md) and [consumer findings](evidence/consumer-scope.md). | Source inspected. | Complete role-specific comparison. |
| Code review | Final diff and focused independent review. | Pending. | NOT_RUN. | Implement first. |
| E2E expansion | Original and new case inventory with assertions. | [canonical cases](06-test-cases.md). | NOT_RUN. | Add HTTP-client and Spring integration tests. |
| Browser execution | Not applicable to this library-only scope. | No UI change. | NOT_APPLICABLE. | Service-level and consumer integration replace browser checks. |

## Requested decision and actual disposition

- Requested decision: preserve the old contract as possible, assess full compatibility, release version `3.0.0`, and add tests.
- Authorized decision owner: User in this chat; organizational business ownership remains unknown.
- Actual decision: implementation and tests authorized; failure policy suggestions invited.
- Actual decision reference: [exact input](evidence/user-clarification-implementation.md).
- Implementation status and source: not started when this stage record was created.
- Intent review: user intent recorded; no additional business mapping is invented.
- Execution outcome: NOT_RUN.
- Business acceptance: pending; implementation authority does not supply deployment or acceptance approval.

## Completed stage disposition

The SDK now uses CES assigned-role details and preserves the existing nested map and lookup method.
Version `3.0.0` artifacts build. The caller supplies FMAA tokens through an explicit overload or provider.
The proposed failure policy preserves the legacy empty result and adds typed errors through the explicit API.
This engineering choice is not recorded business approval of operational retry or acceptance policy.
The complete suite passes: 44 tests, zero failures, zero errors, and zero skips.
Connected preparation and final offline `clean verify` completed.
The unchanged compiled caller passes against baseline and candidate with equal permission maps for equivalent fixtures.
The [coverage record](09-coverage.md) maps criteria, changes, assertions, and results.

| Dimension | Final state | Evidence and limit |
| --- | --- | --- |
| Implementation | Complete for the bounded SDK adapter and version change. | [Final source manifest](evidence/candidate-run-04/inputs.json). |
| Local verification | PASSED; confidence HIGH. | [Execution report](08-test-execution-report.md). Mocks omit live CES and FMAA. |
| Complete permission compatibility | Not established; confidence MEDIUM. | [Role sample differences](evidence/role-compatibility-design.md#sample-comparisons). |
| Consumer adoption | Pending outside this SDK patch. | [Known consumer limits](evidence/consumer-scope.md#confirmed-consumers-and-compatibility). |
| Knowledge | Clarified intent recorded in candidate version 8. | [Knowledge update](evidence/knowledge-update.md). Publication remains pending. |
| Acceptance and deployment | No authorization or completed acceptance is recorded. | Local passing checks do not establish those facts. |

No deployed session disruption or unusable flow was demonstrated.
Missing live evidence limits acceptance claims. It does not establish a production defect.
Next owner: unknown for application acceptance. Next action: verify actual mappings, allowed/denied actions, token refresh, and consumer builds.

Final SDK commit: `fd9a157e260850b6d9efa10da3223950ea61133a`.
All forty recorded repository files match the [commit binding](evidence/final-commit-binding.json).
The SDK worktree is clean.

The [compiled API comparison](evidence/public-api-comparison.json) found no missing public members across 23 baseline classes.
This check covers the supplied baseline. It does not establish compatibility with historical SDK `1.1.1` artifacts.

## Final document checks

[Artifact lint](evidence/implementation-artifact-lint.json) passes for all four current stage documents.
Warnings retain unknown business owners, pending review, unresolved live evidence, and pending ASD writing review.
[Link and length checks](evidence/implementation-document-checks.json) pass: 472 local links and 181 fragments.
No inspected prose line exceeds twenty words. This check does not establish full ASD-STE100 compliance.
[Workspace validation](evidence/implementation-workspace-validation.json) is VALID.
Workbench runtime source did not change. Its runtime tests and wheel build do not apply to this SDK stage.
