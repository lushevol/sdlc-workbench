# Additional delivery acceptance criteria

> **Two preservation criteria currently fail.**
> Action: resolve [DC-AC-10](#dc-ac-10) and [DC-AC-16](#dc-ac-16) before claiming no regression.
> Consequence: cancellation can retain loading. A delayed acquisition callback can end the guarded session.
> Owner: unknown application owner. Evidence: [paired cancellation results](cancellation-candidate/results.json) and [timing observations](candidate-final-verified/case-observations/DEL-20.json).

These sixteen criteria are proposed refinements for this authorized delivery review.
They do not establish human business approval or publication approval.
The [current request](../user-input.md#exact-user-input) authorizes additional criteria, tests, and code review.
The [earlier correction request](../../minor-fixes-20261025/user-request.txt) authorizes the two issue fixes.
The [candidate requirement](../../../../../knowledge/candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria) retains its seven existing criteria.
The latest backlog disposition remains separate from these preservation checks.

Runtime candidate: `c42e7609c4e14eb53de32702e4bd3424a223988a`.
Main baseline: `f025513f696476a9cc8162681410cbd21e029bcb`.
Definition version: 1. Owner: unknown application owner.

## Authority and scope

Criteria derived from requested fixes refine verification within the existing correction scope.
Baseline preservation criteria describe inspected main behavior. They do not invent additional business policy.
Workspace and sharing criteria remain proposed supporting boundaries. Their product acceptance authority remains unavailable.
Source links identify current files. The [source binding](candidate-final-verified/source-binding.json) fixes their inspected candidate hashes.
Main comparisons use exact Git bytes in the [main binding](main-full/source-binding.json).
Tests use synthetic credentials and controlled transport. They do not establish provider trust or PROD parity.

## DC-AC-01

Clear prior refresh credentials before fresh-login completion.
Source lineage: [the requested ownership correction and its prior regression definitions](../../../06-test-cases.md#own-04).

```gherkin
Scenario: DC-AC-01
  Given session A has a refresh credential
  When fresh login starts through authentication version 2 or version 3
  Then session A refresh state is empty before the fresh-login response arrives
```

## DC-AC-02

Retain the newest overlapping fresh login.
Source lineage: [the requested ownership correction; overlapping-login extension remains proposed](../../../06-test-cases.md#own-02).

```gherkin
Scenario: DC-AC-02
  Given two fresh login requests overlap
  And the second request has installed session B access
  When the first request succeeds or rejects with an expired-credential error
  Then session B access and expiry remain unchanged
  And no error from the first request enters session B
```

## DC-AC-03

Reject stale manual renewal completion.
Source lineage: [the ownership correction and pending-completion criteria](../../../06-test-cases.md#pend-10).

```gherkin
Scenario: DC-AC-03
  Given session A manual renewal remains pending
  And fresh login has installed session B access
  When session A renewal succeeds or rejects with an expired-credential error
  Then session B access and expiry remain unchanged
  And session A completion records zero successful prompt closures
  And session A completion starts zero logout requests
```

## DC-AC-04

Preserve pending renewal through the recovery deadline.
Source lineage: [pending-completion criteria](../../../../../knowledge/candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria).

```gherkin
Scenario: DC-AC-04
  Given manual renewal started with usable refresh credentials
  When the recovery deadline passes while renewal remains pending
  Then zero automatic logout requests start
  When that renewal returns currently usable access
  Then the returned access and expiry enter the current session
  And the prompt closes exactly once
```

## DC-AC-05

Apply expiry fallback after unsuccessful late renewal.
Source lineage: [the inherited Timeout recovery deadline; this is a preservation expectation](../../../../../repos/ui/mfe-base/src/components/Timeout/common/useController.ts#L81).

```gherkin
Scenario: DC-AC-05
  Given manual renewal remains pending beyond the refresh recovery deadline
  When renewal rejects with a retryable transport failure
  And the existing one-second logout delay ends
  Then exactly one logout request starts
  And access and refresh state are empty
```

## DC-AC-06

Retain current-session credential rejection.
Source lineage: [the requirement security rationale and existing invalidation path](../../../../../knowledge/candidates/requirements/REQ-active-session-renewal.md#rationale).

```gherkin
Scenario: DC-AC-06
  Given a request belongs to the current authenticated session
  When the service rejects that request with TOKEN_INVALID_EXPIRED
  Then access and refresh state are empty
  And persisted access is absent
  And the session error equals "Expired Session, please login again."
```

## DC-AC-07

Preserve ordinary shared-client requests and errors.
Source lineage: [main shared-client behavior at the recorded baseline](../../../../../repos/ui/mfe-base/src/hooks/service/util/success.request.handler.ts#L8).

```gherkin
Scenario: DC-AC-07
  Given the shared client has session access and user identity
  When an ordinary protected request succeeds
  Then its request carries the existing access and user identity
  And its caller receives the unchanged response data and status
  When another current-session request rejects with an ordinary service error
  Then its caller receives that rejection
  And the global error contains the service message
  And authentication state remains unchanged
```

## DC-AC-08

Retain pending work during access rotation.
Source lineage: [continued eligible renewal and existing ownership control](../../../06-test-cases.md#own-06).

```gherkin
Scenario: DC-AC-08
  Given a protected request remains pending in session A
  When session A access rotates through successful activity renewal
  And the protected request completes
  Then the caller receives the protected response
  And the rotated access remains installed
  And session A refresh credentials remain unchanged
```

## DC-AC-09

Preserve excluded endpoint error handling.
Source lineage: [main error-handler exclusions at the recorded baseline](../../../../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L18).

```gherkin
Scenario: DC-AC-09
  Given the current session has an existing error notice
  When an analytics, server-event, or logout request rejects with TOKEN_INVALID_EXPIRED
  Then current access and refresh state remain unchanged
  And the existing error notice remains unchanged
  And loading equals false
```

## DC-AC-10

Clear loading after final current-session cancellation.
Source lineage: [main loading cleanup at the recorded baseline](source-baselines/main/error.response.handler.ts.snapshot#L40).

```gherkin
Scenario: DC-AC-10
  Given one current-session protected request has set loading to true
  And no replacement request starts
  When the caller cancels that request through its AbortSignal
  Then the caller receives ERR_CANCELED
  And loading equals false
  And authentication state remains unchanged
```

## DC-AC-11

Retain selection after an invalid workspace index.
Source lineage: [changed defensive workspace handling; product approval is unavailable](../../../../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L44).

```gherkin
Scenario: DC-AC-11
  Given workspace A is selected and workspaces A and B exist
  When a stale tab event selects an unavailable workspace index
  Then workspace A remains selected
  And the workspace identifiers remain A and B
```

## DC-AC-12

Select an available neighbor after workspace deletion.
Source lineage: [changed first-workspace selection and unchanged later-workspace behavior](../../../../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L255).

```gherkin
Scenario: DC-AC-12
  Given workspaces A and B exist
  When the user deletes the selected workspace
  Then the remaining available workspace becomes selected
  And stored workspace descriptors contain only that remaining workspace
```

## DC-AC-13

Retain the empty-workspace fallback.
Source lineage: [existing workspace validation; the new guard adds no reachable branch here](../../../../../repos/ui/mfe-base/src/utils/common.ts#L293).

```gherkin
Scenario: DC-AC-13
  Given every saved workspace descriptor refers to an unavailable catalog entry
  When Home validates saved workspaces with no matching entitlements
  Then exactly one blank workspace remains
  And that workspace is selected
  And its label equals "Workspace 1"
  And its container list is empty
```

## DC-AC-14

Reuse a pending activity renewal.
Source lineage: [the requested sharing boundary; no separately approved criterion exists](../../../06-test-cases.md#e2e-08).

```gherkin
Scenario: DC-AC-14
  Given one activity renewal request remains pending
  When more accepted activity reaches the renewal dispatcher
  Then exactly one activity renewal request exists
  And the original request remains uncanceled
  When the original response returns usable access
  Then that access enters session state
  And a protected validation request succeeds
```

## DC-AC-15

Retain loading while a replacement request remains pending.
Source lineage: the [rendered PageLoader](../../../../../repos/ui/mfe-base/src/components/Loader/PageLoader.tsx) uses the shared loading state.
This proposed overlap control protects the correction for [DC-AC-10](#dc-ac-10).
It does not approve a new product rule. It exposes an inherited main race separately.

```gherkin
Scenario: DC-AC-15
  Given current-session request A and replacement request B are pending
  When the caller cancels request A
  Then loading remains true while request B remains pending
  When request B succeeds
  Then its caller receives the response
  And loading equals false
  And authentication state remains unchanged
```

## DC-AC-16

Preserve recovery after a slightly delayed scheduled acquisition.
Source lineage: [main scheduled acquisition](source-baselines/main/Home-useController.ts.snapshot#L94) and the [existing timing finding](../../../06-test-cases.md#review-f02).
This proposed preservation case uses equal synthetic access and refresh expiry at sixty seconds.
A one-millisecond wall-clock displacement models callback lateness. It does not measure native timer latency.
No fixed grace interval or additional credential authority is proposed.

```gherkin
Scenario: DC-AC-16
  Given visible Home has access and refresh credentials expiring after sixty seconds
  And refresh acquisition is scheduled twenty-five seconds before access expiry
  When that scheduled callback runs one millisecond late
  And the authentication service can issue a replacement refresh credential
  And initial access expiry occurs
  Then replacement refresh state remains installed
  And the expiry prompt remains visible with manual renewal available
  And no automatic logout request starts
```

## Review metadata

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
