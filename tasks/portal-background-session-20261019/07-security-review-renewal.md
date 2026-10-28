---
artifact_kind: threat-model
id: SECURITY-session-renewal-comprehensive
version: 1
status: draft
owner: unknown
source_refs: [SRC-comprehensive-renewal-20261028, SRC-renewal-security-source-20261028]
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

# Session renewal security review

> **Critical conclusions: Logout can leave a valid refresh credential usable after access expiry.**
> Action: correct and verify server revocation before security acceptance. Consequence: copied refresh credentials can recover authenticated access after logout.
> Owner: unknown authentication owner. Evidence: [failed assertion](evidence/comprehensive-renewal-20261028/expired-logout-case.json).
> This inherited BFF behavior was reproduced with servlet mocks. Production reachability remains unverified.
>
> **Absolute security is not established.**
> Action: complete target, stream, policy, and artifact checks. Consequence: security acceptance remains blocked.
> Owner: unknown security owner. Evidence: [residual risks](#residual-risks-and-review).

## Scope and assumptions

| Field | Value |
| --- | --- |
| Included components and interfaces | Shell renewal interceptors, session generation, timeout ownership, browser storage, BFF renewal and logout, downstream SDK guards. |
| Environment and revision | Shell `66c6411ade58e4d134e381c2baee8ad3f76a8dbf`; BFF `19f484efbbfbd4a9d16cdec8a64c4b7fa66e901a`; SDK `b0aa82005e7f14202f85f5ef583f25e42da9eeb3`. |
| Frontend comparison | Merge base `f025513f696476a9cc8162681410cbd21e029bcb` through committed shell candidate. |
| Security requirements | [User request](evidence/user-input-20261028-comprehensive-renewal.txt) and [requirement rationale](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#rationale). Security proposals remain distinguishable from approved business criteria. |
| Exclusions and evidence limits | No production test, target artifact binding, penetration test, dependency vulnerability scan, or external identity-provider execution. |
| Worktree boundary | Local Home-controller formatting edits and generated compiler state were preserved. They were excluded from committed-source conclusions. |
| Assumptions needing confirmation | Gateway trust, revocation consistency, stream authorization, retention policy, and actual session owners remain unknown. |

The [test strategy](05-test-strategy-renewal.md#goal-and-scope) authorizes this bounded assessment.
No application fixes or deployment actions occurred during this review.
The selected source and assertion hashes appear in the [security register](evidence/comprehensive-renewal-20261028/security-review.json).

## Assets and trust boundaries

| Asset ID | Asset and sensitivity | Entry point | Trust boundary | Protection objective |
| --- | --- | --- | --- | --- |
| A-1 | Access credentials and user identity | Login, extend, refresh acquisition, relogin | Browser or external client to BFF | Require valid credentials and the correct identity. |
| A-2 | Refresh credentials and revocation state | Relogin and logout | Client-held credential to shared server state | Prevent unauthorized recovery after revocation. |
| A-3 | Workspace records and business actions | Shared requests and restored workspaces | Shell, imported module, and business service | Prevent prior-user data exposure and unauthorized operations. |
| A-4 | Connection credentials and subscriptions | WebSocket, SSE, reconnect, upload completion | Connection setup to continued server processing | Recheck authorization at the required boundaries. |
| A-5 | Credential diagnostics and browser persistence | Storage, console, exported reports, URLs | Runtime state to retained or shared observations | Prevent raw credential disclosure. |
| A-6 | Current session generation and availability | Delayed responses and timeout callbacks | Old asynchronous operation to current shell state | Prevent stale operations from changing the current session. |

## Threats and controls

| Threat ID | Misuse and preconditions | Evidence state | Consequence | Proposed or existing control | Owner | Next action |
| --- | --- | --- | --- | --- | --- | --- |
| [SEC-01](#sec-01) | Replay a copied refresh credential after logout with expired access. | Confirmed in isolated controller execution; inherited BFF logic. | Logout reports success, but relogin issues new access. | Revoke the authenticated session through a reviewed usable-credential path. Never trust unverified JWT payloads. | unknown authentication owner | Add the correction and retain server plus browser regression evidence. |
| SEC-02 | Deliver session A success or rejection after fresh login B. | New generation guards inspected in [response handling](../../repos/ui/mfe-base/src/hooks/service/util/succes.response.handler.ts#L35-L110). | A stale response could replace credentials or clear B authentication. | Existing generation guard rejects stale intercepted responses. | unknown shell owner | Execute distinct-subject, multi-tab, and consumer-boundary cases. |
| SEC-03 | Dispatch B access directly while A refresh remains. | Candidate reducer preserves refresh; supported replacement caller remains unavailable. | Recovery could return A while the user expects B. | Fresh-login interceptors clear refresh and advance generation. Direct dispatch requires caller review. | unknown shell owner | Establish external caller applicability and run distinct-subject replacement. |
| SEC-04 | Read stored access through an injected same-origin script. | Inherited JavaScript-readable storage is [source fact](../../repos/ui/mfe-base/src/utils/common.ts#L47-L79). No injection was demonstrated. | A successful script compromise could obtain reusable credentials. | Review script trust, CSP, dependency loading, storage, and incident response. | unknown security owner | Inspect effective target controls and test isolated credential canaries. |
| SEC-05 | Send shared-client credentials to an unintended absolute URL. | [Request handler](../../repos/ui/mfe-base/src/hooks/service/util/success.request.handler.ts#L26-L37) has no destination allow list. Trusted-caller exposure remains unknown. | A caller-selected destination could receive access headers. | Constrain destinations or enforce a reviewed trusted-module boundary. | unknown shell owner | Inspect public consumers and execute the isolated destination test. |
| SEC-06 | Forge a configured SDK skip header at an untrusted ingress. | [SDK skip logic](../../repos/libraries/single-ui-sdk-starter/single-ui-sdk-starter/src/main/java/com/scb/fmoportal/auth/filter/AuthTokenFilter.java#L59-L68) is inherited. Deployment configuration remains unknown. | An exposed trusted header could bypass JWT filtering. | Strip untrusted headers and restrict bypass configuration at ingress. | unknown platform owner | Verify effective configuration and ingress behavior. |
| SEC-07 | Continue a stream after logout or permission withdrawal. | Server stream enforcement and revocation timing were unavailable. | Previously authorized connections could retain unauthorized data access. | Define authorization checkpoints and revocation deadlines for each transport. | unknown transport owner | Execute stream delivery and reconnect cases against the actual servers. |
| SEC-08 | Forge cross-origin requests or read renewal headers. | BFF requires explicit refresh input. Effective deployment CORS and CSRF evidence was unavailable. | Misconfigured ingress could expose credentials or authenticated actions. | Review actual origins, credentials, cookie settings, preflight, and header exposure. | unknown platform owner | Run two-origin browser tests against the target composition. |
| SEC-09 | Replay old refresh credentials after replacement. | Local BFF generates replacement credentials without an inspected single-use store. | A copied old refresh might remain valid until expiry or session revocation. | Decide rotation and replay policy explicitly. Preserve existing semantics until reviewed. | unknown authentication owner | Resolve the policy and test old/new credential behavior. |
| SEC-10 | Revoke on one service replica while another retains access. | BFF uses repository checks. SDK uses a process-local session list. | Global logout cannot be inferred from one endpoint response. | Bind each consumer to the reviewed revocation mechanism. | unknown architecture owner | Validate replica consistency and downstream authorization. |

These source risks are not all demonstrated vulnerabilities.
Only [SEC-01](#sec-01) has new failing execution evidence in this assessment.
No newly introduced authentication bypass was demonstrated in the frontend comparison.
That conclusion does not prove the absence of other defects.

## Security verification

The [probe runner](evidence/comprehensive-renewal-20261028/run_security_probe.py) compiles four exact current BFF source files.
It uses actual RSA verification, actual controller methods, and actual session-service logic.
The repository and entitlement dependencies use mocks. Servlet objects also use mocks.
No HTTP server, browser, external provider, or production service participates.

| Threat or requirement | Planned input or attack | Observable assertion | Test revision | Execution evidence | Result |
| --- | --- | --- | --- | --- | --- |
| [RN-S001](06-test-cases.md#rn-s001) | Logout with valid access, then replay refresh. | Relogin returns 401 and issues zero access credentials. | [Probe hash](evidence/comprehensive-renewal-20261028/security-probe-execution.json) | [Valid-access control](evidence/comprehensive-renewal-20261028/valid-logout-case.json) | PASSED |
| [RN-S002](06-test-cases.md#rn-s002) | Logout with expired access, then replay valid refresh. | Relogin issues zero access credentials. | Same probe hash. | [Expired-access result](evidence/comprehensive-renewal-20261028/expired-logout-case.json) | FAILED: relogin returned 200 and issued access. |
| [RN-S011](06-test-cases.md#rn-s011) | Expired refresh. | Response 401; zero access or refresh credentials. | Same probe hash. | [Result](evidence/comprehensive-renewal-20261028/RN-S011-credential-case.json) | PASSED |
| [RN-S012](06-test-cases.md#rn-s012) | Modified refresh signature. | Response 401; zero access or refresh credentials. | Same probe hash. | [Result](evidence/comprehensive-renewal-20261028/RN-S012-credential-case.json) | PASSED |
| [RN-S013](06-test-cases.md#rn-s013) | Access credential in refresh slot. | Response 401; zero access or refresh credentials. | Same probe hash. | [Result](evidence/comprehensive-renewal-20261028/RN-S013-credential-case.json) | PASSED |
| [RN-S014](06-test-cases.md#rn-s014) | Entitlement credential in refresh slot. | Response 401; zero access or refresh credentials. | Same probe hash. | [Result](evidence/comprehensive-renewal-20261028/RN-S014-credential-case.json) | PASSED |
| [RN-S015](06-test-cases.md#rn-s015) | Foreign issuer with a valid test signature. | Response 401; zero access or refresh credentials. | Same probe hash. | [Result](evidence/comprehensive-renewal-20261028/RN-S015-credential-case.json) | PASSED |
| [RN-S016](06-test-cases.md#rn-s016) | Unsigned JWT. | Response 401; zero access or refresh credentials. | Same probe hash. | [Result](evidence/comprehensive-renewal-20261028/RN-S016-credential-case.json) | PASSED |
| [RN-S017](06-test-cases.md#rn-s017) | Malformed JWT. | Response 401; zero access or refresh credentials. | Same probe hash. | [Result](evidence/comprehensive-renewal-20261028/RN-S017-credential-case.json) | PASSED |
| [RN-S018](06-test-cases.md#rn-s018) | Expired access during refresh acquisition. | Response 401; zero access or refresh credentials. | Same probe hash. | [Result](evidence/comprehensive-renewal-20261028/RN-S018-credential-case.json) | PASSED |
| [RN-S019](06-test-cases.md#rn-s019) | Refresh credential in access slot. | Response 401; zero access or refresh credentials. | Same probe hash. | [Result](evidence/comprehensive-renewal-20261028/RN-S019-credential-case.json) | PASSED |
| [RN-S020](06-test-cases.md#rn-s020) | Future not-before claim. | Response 401; zero access or refresh credentials. | Same probe hash. | [Result](evidence/comprehensive-renewal-20261028/RN-S020-credential-case.json) | PASSED |
| [RN-S021](06-test-cases.md#rn-s021) | Missing refresh header. | Response 401; zero access or refresh credentials. | Same probe hash. | [Result](evidence/comprehensive-renewal-20261028/RN-S021-credential-case.json) | PASSED |

**Result: 13 controller integration cases completed; 12 passed and one failed.**
The suite result is `FAILED`. The runner returns failure when a security assertion fails.
The [initial setup failure](evidence/comprehensive-renewal-20261028/security-probe-execution-initial.json) remains retained.
Mockito attachment failed before assertions. The successful run uses the subclass mock maker.

The [security definitions](evidence/comprehensive-renewal-20261028/security-cases.json) contain 55 adversarial cases across six use cases.
Fourteen cases describe unresolved policy. Their acceptance remains blocked until expectations are resolved.
The remaining definitions are not passing execution evidence.
The [canonical catalog](06-test-cases.md) keeps the human-readable Gherkin definitions.

## Residual risks and review

| Risk | Remaining exposure and evidence limit | Decision owner | Decision | Review evidence |
| --- | --- | --- | --- | --- |
| Server revocation gap | Expired-access logout permits refresh replay in the isolated controller probe. Target reachability remains unverified. | unknown authentication owner | Correction and verification required | [Failed case](evidence/comprehensive-renewal-20261028/expired-logout-case.json) |
| Global revocation | Replica propagation and SDK consumers were not exercised. | unknown architecture owner | pending | null |
| Target composition | Served artifact, effective settings, gateways, identities, and entitlements were not bound to the tested composition. | unknown release owner | pending | null |
| Streams and long operations | Server enforcement, reconnect policy, replay rules, and permission withdrawal remain unverified. | unknown transport owner | pending | null |
| Browser and module trust | Storage exposure, module loading, CSP, destination restrictions, and cross-origin behavior need target tests. | unknown security owner | pending | null |
| Long session policy | Continuous renewal target does not establish enterprise approval for every lifetime or compromised-credential condition. | unknown business and security owners | pending | [Requirement rationale](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#rationale) |
| Security instrumentation | No configured vulnerability analyzer, live penetration result, or production telemetry was evaluated. | unknown security owner | pending | null |

Operational controls: retain hashes and synthetic observations. Exclude raw credentials, customer data, and private keys from saved evidence.
Review boundary: exact local source and the disclosed controlled integration cases.
Security acceptance, business acceptance, publication approval, and deployment authorization remain separate decisions.

## Evidence and uncertainty

| Source ID | Locator | Exact revision | Hash | Owner, authority, and inspected scope |
| --- | --- | --- | --- | --- |
| SRC-comprehensive-renewal-20261028 | [Exact user request](evidence/user-input-20261028-comprehensive-renewal.txt) | user-message-20261028 | [Register](evidence/comprehensive-renewal-20261028/security-review.json) | User; authorizes comprehensive test design and security assessment. |
| SRC-renewal-security-source-20261028 | [Source and comparison register](evidence/comprehensive-renewal-20261028/security-review.json) | Exact repository commits above | Per-file SHA-256 values retained | unknown source owners; inspected code establishes implementation facts. |
| SRC-renewal-security-probe-20261028 | [Execution binding](evidence/comprehensive-renewal-20261028/security-probe-execution.json) | Exact BFF source plus probe hash | Per-source, class, and dependency hashes retained | Controlled execution; mocked persistence and entitlements limit environmental claims. |
| SRC-existing-session-review | [Existing issue catalog](10-issue-catalog.md#findings) | Historical conclusions retain original bindings | Referenced results retain original hashes | Secondary evidence; earlier browser results are not silently promoted to current-source passes. |

Facts: current BFF source validates access before recording logout revocation.
The inherited baseline has the same validation order.
The probe observes zero revocation entries and successful refresh replay when access has expired.
Inferences: this path can preserve copied refresh credentials after an apparent logout in a matching deployment.
Limits: no credential theft, production incident, frequency, or deployed exposure was demonstrated.
Unresolved questions: stream enforcement, target trust controls, session owners, rotation policy, and revocation consistency remain unknown.

## Findings and actions

<a id="sec-01"></a>

### SEC-01: expired-access logout does not revoke the renewable session

Proposed priority: P1, conditional on copied valid refresh credentials. This is an inherited server defect.
Confidence: high for the isolated code path. Production applicability remains unknown.

Setup: synthetic user A owns expired access A and valid refresh A for one session identifier.

1. Submit access A to `POST /v2/sso/logout`.
2. Inspect the response and revocation repository.
3. Submit refresh A to `POST /v2/sso/relogin`.
4. Inspect the returned access header.

Intended security result: completed logout prevents subsequent renewal for the revoked session.
Historical source result: validation can throw before `sessionService.create`; the handler still reports success.
Current actual result: logout returns 200 with `result: true`; zero revocation entries exist; relogin issues access.
The valid-access control records one revocation entry and rejects replay with 401.

| Finding ID | Evidence | Consequence | Owner | Next action | State |
| --- | --- | --- | --- | --- | --- |
| SEC-01 | [Logout implementation](../../repos/services/single-ui-bff/src/main/java/com/scb/sso/singleuibff/controller/v2/JwtAuthenticationController.java#L370-L383), [failed assertion](evidence/comprehensive-renewal-20261028/expired-logout-case.json), [baseline comparison](evidence/comprehensive-renewal-20261028/security-review.json) | Copied valid refresh can recover access after apparent logout. | unknown authentication owner | Correct revocation through a reviewed authenticated path. Add browser, replica, and server regression evidence. | OPEN; no fix applied |
| SEC-GAP-01 | [Generation and direct-dispatch cases](evidence/comprehensive-renewal-20261028/security-cases.json) | Cross-user and external caller safety remains unverified. | unknown shell owner | Bind supported callers and execute distinct-subject tests. | OPEN evidence gap |
| SEC-GAP-02 | [Residual risk table](#residual-risks-and-review) | Target security acceptance remains unsupported. | unknown security owner | Resolve policies and retain target execution with exact artifact identity. | OPEN evidence gap |
