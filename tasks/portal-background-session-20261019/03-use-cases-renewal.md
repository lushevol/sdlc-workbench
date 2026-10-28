---
artifact_kind: use-case
id: USE-CASES-comprehensive-session-renewal
version: 1
status: draft
owner: unknown
source_refs: [SRC-comprehensive-renewal-20261028]
related_ids: [REQ-active-session-renewal]
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
# Session renewal user journeys

> **Critical conclusions: Security acceptance remains blocked by a reproduced revocation gap and missing target evidence.**
> Action: resolve the [security findings](07-security-review-renewal.md#findings-and-actions). Consequence: these journeys cannot establish secure deployment.
> Owner: unknown service and application owners. Evidence: [security probe](evidence/comprehensive-renewal-20261028/security-probe-execution.json).

## Context and source facts

The [exact user request](evidence/user-input-20261028-comprehensive-renewal.txt) defines this test-design scope.
Primary actors are synthetic portal users A and B. Supporting actors include the shell, BFF, application containers, and transport servers.
The system boundary includes session continuation and concurrent work. It includes authorization observations at downstream boundaries.
The [requirement](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria) remains candidate version 5 with pending publication review.
The [source manifest](evidence/comprehensive-renewal-20261028/source-manifest.json) identifies inspected revisions and retained bytes.

## Proposed flow conditions

Use the [canonical fixture and oracles](06-test-cases.md#renewal-fixture-and-oracles). Each journey states additional conditions below.
Distinguish target behavior, source observations, proposed security invariants, and unresolved policy.
A journey succeeds only when its linked assertions pass. A rejected or pending response cannot establish successful renewal.
Policy-open journeys permit observation. Their acceptance remains blocked until the applicable rule is reviewed.

## Main flow

This catalog contains 40 use cases. Detailed test steps exist only in the canonical test catalog.

### UC-R01

**Continue activity with each supported input**

Goal: Keep eligible activity renewing the session.

Trigger: Mouse, keyboard, or scroll activity begins.

Preconditions: At least 30 seconds of access remain.

| Step | Actor action | System response | Rule or requirement IDs | Observable evidence |
| --- | --- | --- | --- | --- |
| 1 | Generate source-defined input for 15 seconds | Assert successful renewal and protected validation | See linked case evidence classes | [RN-A001](06-test-cases.md#rn-a001), [RN-A002](06-test-cases.md#rn-a002), [RN-A003](06-test-cases.md#rn-a003) |

Limits: Continuous input can expose the recorded debounce defect

### UC-R02

**Use mixed input and embedded application controls**

Goal: Observe which input reaches the shell.

Trigger: User changes input method or application context.

Preconditions: Identify same-origin and cross-origin boundaries.

| Step | Actor action | System response | Rule or requirement IDs | Observable evidence |
| --- | --- | --- | --- | --- |
| 1 | Exercise the named input context | Measure shell events and the applicable renewal target | See linked case evidence classes | [RN-A004](06-test-cases.md#rn-a004), [RN-A005](06-test-cases.md#rn-a005), [RN-A006](06-test-cases.md#rn-a006), [RN-A007](06-test-cases.md#rn-a007), [RN-A008](06-test-cases.md#rn-a008), [RN-A009](06-test-cases.md#rn-a009), [RN-A010](06-test-cases.md#rn-a010), [RN-A011](06-test-cases.md#rn-a011), [RN-A012](06-test-cases.md#rn-a012), [RN-A013](06-test-cases.md#rn-a013), [RN-A014](06-test-cases.md#rn-a014), [RN-A015](06-test-cases.md#rn-a015) |

Limits: Cross-origin, touch, composition, and passive activity eligibility remain unresolved

### UC-R03

**Renew at the activity cutoff**

Goal: Check both sides of the 25-second implementation guard.

Trigger: An activity callback runs.

Preconditions: Use an isolated controlled clock.

| Step | Actor action | System response | Rule or requirement IDs | Observable evidence |
| --- | --- | --- | --- | --- |
| 1 | Invoke shared activity renewal at each boundary | Count outbound requests separately from renewal success | See linked case evidence classes | [RN-B001](06-test-cases.md#rn-b001), [RN-B002](06-test-cases.md#rn-b002), [RN-B003](06-test-cases.md#rn-b003) |

Limits: These are implementation thresholds, not business lifetime policies

### UC-R04

**Use manual recovery near refresh expiry**

Goal: Check the source recovery deadline.

Trigger: User selects manual renewal.

Preconditions: Use a timeout controller and controlled refresh expiry.

| Step | Actor action | System response | Rule or requirement IDs | Observable evidence |
| --- | --- | --- | --- | --- |
| 1 | Activate renewal around refresh expiry minus 2000 milliseconds | Count accepted relogin requests | See linked case evidence classes | [RN-B004](06-test-cases.md#rn-b004), [RN-B005](06-test-cases.md#rn-b005), [RN-B006](06-test-cases.md#rn-b006) |

Limits: The two-second margin is source behavior

### UC-R05

**Reuse or acquire refresh credentials**

Goal: Check the three-hour reuse branch.

Trigger: The shell requests refresh acquisition.

Preconditions: Current identity and expiry are known.

| Step | Actor action | System response | Rule or requirement IDs | Observable evidence |
| --- | --- | --- | --- | --- |
| 1 | Request acquisition around the reuse boundary | Count acquisition POSTs | See linked case evidence classes | [RN-B007](06-test-cases.md#rn-b007), [RN-B008](06-test-cases.md#rn-b008), [RN-B009](06-test-cases.md#rn-b009) |

Limits: The reuse interval is implementation behavior

### UC-R06

**Recover from delayed clocks and callbacks**

Goal: Separate elapsed time from callback delivery.

Trigger: A timer runs late or browser visibility changes.

Preconditions: Record absolute expiry and current visibility.

| Step | Actor action | System response | Rule or requirement IDs | Observable evidence |
| --- | --- | --- | --- | --- |
| 1 | Deliver the callback under the named state | Observe acquisition and timeout decisions | See linked case evidence classes | [RN-B010](06-test-cases.md#rn-b010), [RN-B011](06-test-cases.md#rn-b011), [RN-B012](06-test-cases.md#rn-b012), [RN-B013](06-test-cases.md#rn-b013), [RN-B014](06-test-cases.md#rn-b014), [RN-B015](06-test-cases.md#rn-b015), [RN-B016](06-test-cases.md#rn-b016), [RN-B017](06-test-cases.md#rn-b017) |

Limits: Clock skew acceptance remains unresolved

### UC-R07

**Complete manual recovery**

Goal: Keep the prompt pending until usable access arrives.

Trigger: User selects Extend.

Preconditions: A usable refresh credential exists.

| Step | Actor action | System response | Rule or requirement IDs | Observable evidence |
| --- | --- | --- | --- | --- |
| 1 | Hold, reject, or complete the renewal response | Assert prompt transitions and credential installation | See linked case evidence classes | [RN-M001](06-test-cases.md#rn-m001), [RN-M002](06-test-cases.md#rn-m002), [RN-M003](06-test-cases.md#rn-m003), [RN-M004](06-test-cases.md#rn-m004), [RN-M005](06-test-cases.md#rn-m005) |

Limits: Service provider behavior remains outside substituted responses

### UC-R08

**Leave or replace a pending recovery**

Goal: Keep old controller actions isolated.

Trigger: Logout, unmount, or account replacement occurs.

Preconditions: A pending request belongs to session A.

| Step | Actor action | System response | Rule or requirement IDs | Observable evidence |
| --- | --- | --- | --- | --- |
| 1 | Complete the ownership transition before delivery | Assert zero obsolete credential installation | See linked case evidence classes | [RN-M006](06-test-cases.md#rn-m006), [RN-M007](06-test-cases.md#rn-m007), [RN-M008](06-test-cases.md#rn-m008), [RN-M009](06-test-cases.md#rn-m009), [RN-M010](06-test-cases.md#rn-m010), [RN-M011](06-test-cases.md#rn-m011), [RN-M012](06-test-cases.md#rn-m012) |

Limits: Cross-device revocation needs separate policy

### UC-R09

**Validate the renewal response shape**

Goal: Reject unusable access before prompt closure.

Trigger: The relogin response arrives.

Preconditions: Use the real response interceptor.

| Step | Actor action | System response | Rule or requirement IDs | Observable evidence |
| --- | --- | --- | --- | --- |
| 1 | Deliver each concrete invalid or ambiguous response | Observe installation and closure separately | See linked case evidence classes | [RN-P001](06-test-cases.md#rn-p001), [RN-P002](06-test-cases.md#rn-p002), [RN-P003](06-test-cases.md#rn-p003), [RN-P004](06-test-cases.md#rn-p004), [RN-P005](06-test-cases.md#rn-p005), [RN-P006](06-test-cases.md#rn-p006), [RN-P007](06-test-cases.md#rn-p007), [RN-P008](06-test-cases.md#rn-p008), [RN-P009](06-test-cases.md#rn-p009), [RN-P010](06-test-cases.md#rn-p010), [RN-P011](06-test-cases.md#rn-p011), [RN-P012](06-test-cases.md#rn-p012), [RN-P013](06-test-cases.md#rn-p013), [RN-P014](06-test-cases.md#rn-p014), [RN-P015](06-test-cases.md#rn-p015), [RN-P016](06-test-cases.md#rn-p016), [RN-P017](06-test-cases.md#rn-p017), [RN-P018](06-test-cases.md#rn-p018) |

Limits: Browser header normalization and future-iat policy need review

### UC-R10

**Deliver old responses after account changes**

Goal: Prevent prior-session results from changing the current user.

Trigger: A delayed response reaches the client.

Preconditions: A and B have distinct session generations.

| Step | Actor action | System response | Rule or requirement IDs | Observable evidence |
| --- | --- | --- | --- | --- |
| 1 | Change ownership before releasing the old response | Assert current identity and zero stale writes | See linked case evidence classes | [RN-R001](06-test-cases.md#rn-r001), [RN-R002](06-test-cases.md#rn-r002), [RN-R003](06-test-cases.md#rn-r003), [RN-R004](06-test-cases.md#rn-r004), [RN-R005](06-test-cases.md#rn-r005), [RN-R006](06-test-cases.md#rn-r006), [RN-R007](06-test-cases.md#rn-r007), [RN-R008](06-test-cases.md#rn-r008) |

Limits: Local isolation does not establish server revocation

### UC-R11

**Share a pending operation within its actual scope**

Goal: Avoid repeated same-owner acquisition or controller calls.

Trigger: Several callers arrive before settlement.

Preconditions: Use one epoch and one mounted Timeout controller for manual actions.

| Step | Actor action | System response | Rule or requirement IDs | Observable evidence |
| --- | --- | --- | --- | --- |
| 1 | Invoke the declared number of callers | Assert the operation count and final owner | See linked case evidence classes | [RN-R009](06-test-cases.md#rn-r009), [RN-R010](06-test-cases.md#rn-r010), [RN-R011](06-test-cases.md#rn-r011), [RN-R012](06-test-cases.md#rn-r012), [RN-R013](06-test-cases.md#rn-r013), [RN-R014](06-test-cases.md#rn-r014) |

Limits: Direct relogin calls have different cancellation behavior

### UC-R12

**Reorder concurrent work**

Goal: Expose stale callback and completion interactions.

Trigger: Requests or timers finish together.

Preconditions: Hold independently identified operations.

| Step | Actor action | System response | Rule or requirement IDs | Observable evidence |
| --- | --- | --- | --- | --- |
| 1 | Deliver both controlled orders | Record each final owner and state | See linked case evidence classes | [RN-R015](06-test-cases.md#rn-r015), [RN-R016](06-test-cases.md#rn-r016), [RN-R017](06-test-cases.md#rn-r017), [RN-R018](06-test-cases.md#rn-r018), [RN-R019](06-test-cases.md#rn-r019), [RN-R020](06-test-cases.md#rn-r020) |

Limits: Several same-epoch ordering policies remain unresolved

### UC-R13

**Repeat recovery and lifecycle operations**

Goal: Detect accumulated state and resources.

Trigger: The fixture starts a finite loop.

Preconditions: Record expected mounted-resource baselines.

| Step | Actor action | System response | Rule or requirement IDs | Observable evidence |
| --- | --- | --- | --- | --- |
| 1 | Complete the declared cycle count | Assert pending-network settlement and stable resource counts | See linked case evidence classes | [RN-L001](06-test-cases.md#rn-l001), [RN-L002](06-test-cases.md#rn-l002), [RN-L003](06-test-cases.md#rn-l003), [RN-L004](06-test-cases.md#rn-l004), [RN-L005](06-test-cases.md#rn-l005), [RN-L006](06-test-cases.md#rn-l006), [RN-L007](06-test-cases.md#rn-l007), [RN-L008](06-test-cases.md#rn-l008), [RN-L009](06-test-cases.md#rn-l009), [RN-L010](06-test-cases.md#rn-l010) |

Limits: Finite loops do not prove unlimited lifetime or performance

### UC-R14

**Continue beyond initial refresh expiry**

Goal: Test the requested four-hour activity behavior.

Trigger: The initial refresh expiry occurs.

Preconditions: Activity and successful renewals continue before access deadlines.

| Step | Actor action | System response | Rule or requirement IDs | Observable evidence |
| --- | --- | --- | --- | --- |
| 1 | Advance through four controlled hours | Assert zero prompts caused solely by elapsed lifetime | See linked case evidence classes | [RN-L011](06-test-cases.md#rn-l011) |

Limits: No finite test proves indefinite renewal

### UC-R15

**Resume across browser and device habits**

Goal: Measure identity and recovery across lifecycle boundaries.

Trigger: Reload, sleep, crash, network change, or another context occurs.

Preconditions: Use distinct synthetic contexts and record real lifecycle events.

| Step | Actor action | System response | Rule or requirement IDs | Observable evidence |
| --- | --- | --- | --- | --- |
| 1 | Apply the named lifecycle event | Record authorization and installed state | See linked case evidence classes | [RN-H001](06-test-cases.md#rn-h001), [RN-H002](06-test-cases.md#rn-h002), [RN-H003](06-test-cases.md#rn-h003), [RN-H004](06-test-cases.md#rn-h004), [RN-H005](06-test-cases.md#rn-h005), [RN-H006](06-test-cases.md#rn-h006), [RN-H007](06-test-cases.md#rn-h007), [RN-H008](06-test-cases.md#rn-h008), [RN-H009](06-test-cases.md#rn-h009), [RN-H010](06-test-cases.md#rn-h010), [RN-H011](06-test-cases.md#rn-h011), [RN-H012](06-test-cases.md#rn-h012) |

Limits: Global logout and restoration policies remain unresolved

### UC-R16

**Handle rejected or incomplete renewal**

Goal: Preserve truthful pending and failure outcomes.

Trigger: The service rejects, times out, or returns malformed success.

Preconditions: Refresh remains usable unless the case states otherwise.

| Step | Actor action | System response | Rule or requirement IDs | Observable evidence |
| --- | --- | --- | --- | --- |
| 1 | Deliver the named failure through the real client | Assert no false successful closure and applicable retry state | See linked case evidence classes | [RN-F001](06-test-cases.md#rn-f001), [RN-F002](06-test-cases.md#rn-f002), [RN-F003](06-test-cases.md#rn-f003), [RN-F004](06-test-cases.md#rn-f004), [RN-F005](06-test-cases.md#rn-f005), [RN-F006](06-test-cases.md#rn-f006), [RN-F007](06-test-cases.md#rn-f007), [RN-F008](06-test-cases.md#rn-f008), [RN-F009](06-test-cases.md#rn-f009), [RN-F010](06-test-cases.md#rn-f010), [RN-F011](06-test-cases.md#rn-f011), [RN-F012](06-test-cases.md#rn-f012) |

Limits: Maximum pending duration and service retry policy remain unresolved

### UC-W01

**Continue work across multiple workspace states**

Goal: Keep renewal and workspace lifecycle operations attributable to their original workspace..

Trigger: Renewal overlaps a tab action or module lifecycle event..

Preconditions: W-A and W-B are authorized synthetic workspaces. The fixture records IDs, selected tab, descriptors, and module instance IDs..

| Step | Actor action | System response | Rule or requirement IDs | Observable evidence |
| --- | --- | --- | --- | --- |
| 1 | User A starts work in W-A. | The shell selects W-A by stable workspace ID. | See linked case evidence classes | [RN-W001](06-test-cases.md#rn-w001), [RN-W002](06-test-cases.md#rn-w002), [RN-W003](06-test-cases.md#rn-w003), [RN-W004](06-test-cases.md#rn-w004), [RN-W005](06-test-cases.md#rn-w005), [RN-W006](06-test-cases.md#rn-w006), [RN-W007](06-test-cases.md#rn-w007), [RN-W008](06-test-cases.md#rn-w008), [RN-W009](06-test-cases.md#rn-w009), [RN-W010](06-test-cases.md#rn-w010), [RN-W011](06-test-cases.md#rn-w011), [RN-W012](06-test-cases.md#rn-w012), [RN-W017](06-test-cases.md#rn-w017), [RN-W019](06-test-cases.md#rn-w019), [RN-W022](06-test-cases.md#rn-w022), [RN-W023](06-test-cases.md#rn-w023), [RN-W024](06-test-cases.md#rn-w024), [RN-W027](06-test-cases.md#rn-w027) |
| 2 | Renewal overlaps workspace navigation or loading. | The fixture records operation order and credential identity. | See linked case evidence classes | Same canonical cases |
| 3 | A protected request completes after renewal. | The service principal and workspace response routing are asserted. | See linked case evidence classes | Same canonical cases |

Limits: Observed source invariants do not create new business acceptance policy.

### UC-W02

**Renew while workspace requests remain loading**

Goal: Keep shared loading state consistent with outstanding current-session requests..

Trigger: Renewal overlaps loading, cancellation, errors, or completion..

Preconditions: The fixture tracks each request ID and session epoch..

| Step | Actor action | System response | Rule or requirement IDs | Observable evidence |
| --- | --- | --- | --- | --- |
| 1 | W-A and W-B start controlled requests. | The loader reflects current pending requests. | See linked case evidence classes | [RN-Q001](06-test-cases.md#rn-q001), [RN-Q002](06-test-cases.md#rn-q002), [RN-Q003](06-test-cases.md#rn-q003), [RN-Q004](06-test-cases.md#rn-q004), [RN-Q005](06-test-cases.md#rn-q005), [RN-Q006](06-test-cases.md#rn-q006), [RN-Q007](06-test-cases.md#rn-q007), [RN-Q008](06-test-cases.md#rn-q008), [RN-Q009](06-test-cases.md#rn-q009), [RN-Q010](06-test-cases.md#rn-q010), [RN-Q011](06-test-cases.md#rn-q011), [RN-Q012](06-test-cases.md#rn-q012), [RN-Q013](06-test-cases.md#rn-q013), [RN-Q014](06-test-cases.md#rn-q014), [RN-Q015](06-test-cases.md#rn-q015), [RN-Q016](06-test-cases.md#rn-q016), [RN-Q017](06-test-cases.md#rn-q017), [RN-Q018](06-test-cases.md#rn-q018), [RN-Q019](06-test-cases.md#rn-q019), [RN-Q020](06-test-cases.md#rn-q020) |
| 2 | Renewal completes while requests remain held. | Renewal credentials and loading state are observed separately. | See linked case evidence classes | Same canonical cases |
| 3 | Requests settle in the selected order. | Final loading and each caller result are asserted. | See linked case evidence classes | Same canonical cases |

Limits: PageLoader visibility and store.isLoading are different observations.

### UC-W03

**Prevent workspace data from crossing session boundaries**

Goal: Keep protected records and callbacks bound to the authorized principal and workspace..

Trigger: Permissions, identity, or workspace ownership changes..

Preconditions: Synthetic User A and User B have distinct entitlements..

| Step | Actor action | System response | Rule or requirement IDs | Observable evidence |
| --- | --- | --- | --- | --- |
| 1 | The fixture starts protected work for User A. | The original principal and workspace ID are retained. | See linked case evidence classes | [RN-W013](06-test-cases.md#rn-w013), [RN-W014](06-test-cases.md#rn-w014), [RN-W018](06-test-cases.md#rn-w018), [RN-W020](06-test-cases.md#rn-w020), [RN-W021](06-test-cases.md#rn-w021), [RN-W026](06-test-cases.md#rn-w026) |
| 2 | Identity or permission changes before completion. | The service receives the changed authorization state. | See linked case evidence classes | Same canonical cases |
| 3 | The delayed action completes. | No unauthorized protected record reaches the new principal or workspace. | See linked case evidence classes | Same canonical cases |

Limits: Proposed security invariants require owner review and matching server evidence.

### UC-W04

**Observe workspace and edit restoration boundaries**

Goal: Measure descriptors and unsaved state without inventing restoration policy..

Trigger: Renewal, logout, restart, or browser crash occurs..

Preconditions: The fixture records descriptor hashes and unsaved edit hashes separately..

| Step | Actor action | System response | Rule or requirement IDs | Observable evidence |
| --- | --- | --- | --- | --- |
| 1 | User A populates two workspaces. | The fixture records persisted and volatile state. | See linked case evidence classes | [RN-W015](06-test-cases.md#rn-w015), [RN-W016](06-test-cases.md#rn-w016), [RN-W025](06-test-cases.md#rn-w025) |
| 2 | The lifecycle event occurs. | The fixture retains exact event order. | See linked case evidence classes | Same canonical cases |
| 3 | User A returns to the portal. | Before and after state is recorded separately. | See linked case evidence classes | Same canonical cases |

Limits: O-004 and application-owned unsaved-state policy remain unresolved.

### UC-W05

**Receive desktop launch intent during renewal**

Goal: Observe FDC3 launch handling while access is expired or renewal is pending..

Trigger: The isolated desktop adapter emits one declared launch intent..

Preconditions: Use an isolated FDC3 adapter and synthetic trade X..

| Step | Actor action | System response | Rule or requirement IDs | Observable evidence |
| --- | --- | --- | --- | --- |
| 1 | The adapter sends the intent. | Intent type and parameters are retained. | See linked case evidence classes | [RN-W028](06-test-cases.md#rn-w028) |
| 2 | The shell observes login state. | The fixture records storage and provider credential identities. | See linked case evidence classes | Same canonical cases |
| 3 | The target module requests data. | Service authorization and workspace creation are recorded. | See linked case evidence classes | Same canonical cases |

Limits: Intent arrival does not establish eligible human activity.

### UC-W06

**Renew through user activity inside workspaces**

Goal: Check the requested mouse, keyboard, and scroll behavior in realistic module contexts..

Trigger: User A sends controlled native input inside a populated workspace..

Preconditions: Access has at least 30 seconds remaining. The input interval equals the requirement fixture..

| Step | Actor action | System response | Rule or requirement IDs | Observable evidence |
| --- | --- | --- | --- | --- |
| 1 | User A performs the named input every 100 milliseconds for 15 seconds. | The fixture records native event type and target. | See linked case evidence classes | [RN-W029](06-test-cases.md#rn-w029), [RN-W030](06-test-cases.md#rn-w030), [RN-W031](06-test-cases.md#rn-w031), [RN-W032](06-test-cases.md#rn-w032) |
| 2 | The shell requests renewal. | The fixture records response completion and installed access. | See linked case evidence classes | Same canonical cases |
| 3 | The protected probe uses installed access. | The service accepts the expected principal. | See linked case evidence classes | Same canonical cases |

Limits: Cross-origin child input requires a separate activity contract.

### UC-W07

**Use several tabs, windows, and browser contexts**

Goal: Measure session coordination and enforce principal isolation across contexts..

Trigger: A context renews, logs out, changes identity, closes, or restores..

Preconditions: Record origin, profile, storage type, and provider identity for every context..

| Step | Actor action | System response | Rule or requirement IDs | Observable evidence |
| --- | --- | --- | --- | --- |
| 1 | User A opens the declared contexts. | The fixture records context and credential identities. | See linked case evidence classes | [RN-D001](06-test-cases.md#rn-d001), [RN-D002](06-test-cases.md#rn-d002), [RN-D003](06-test-cases.md#rn-d003), [RN-D004](06-test-cases.md#rn-d004), [RN-D005](06-test-cases.md#rn-d005), [RN-D006](06-test-cases.md#rn-d006), [RN-D007](06-test-cases.md#rn-d007), [RN-D008](06-test-cases.md#rn-d008), [RN-D009](06-test-cases.md#rn-d009), [RN-D010](06-test-cases.md#rn-d010), [RN-D011](06-test-cases.md#rn-d011), [RN-D012](06-test-cases.md#rn-d012), [RN-D013](06-test-cases.md#rn-d013), [RN-D014](06-test-cases.md#rn-d014) |
| 2 | One context changes session state. | The fixture records local storage and in-memory state separately. | See linked case evidence classes | Same canonical cases |
| 3 | Another context requests protected data. | The service principal and visible data are checked. | See linked case evidence classes | Same canonical cases |

Limits: Global logout scope, idle scope, and multiple-root support require explicit contracts.

### UC-T01

**Authenticate a reconnect with current access**

Goal: Check credential propagation from renewal to the next transport handshake..

Trigger: A GraphQL or STOMP connection reconnects after renewal..

Preconditions: Use synthetic peers and record only credential hashes..

| Step | Actor action | System response | Rule or requirement IDs | Observable evidence |
| --- | --- | --- | --- | --- |
| 1 | The session renews. | Usable access is installed. | See linked case evidence classes | [RN-T001](06-test-cases.md#rn-t001), [RN-T002](06-test-cases.md#rn-t002), [RN-T010](06-test-cases.md#rn-t010), [RN-T019](06-test-cases.md#rn-t019), [RN-T020](06-test-cases.md#rn-t020) |
| 2 | The transport reconnects. | The handshake records current credential identity. | See linked case evidence classes | Same canonical cases |
| 3 | The server authorizes the connection. | The principal equals User A. | See linked case evidence classes | Same canonical cases |

Limits: A new handshake cannot prove authorization of an existing connection.

### UC-T02

**Constrain established connections across expiry and identity changes**

Goal: Measure socket lifetime and prevent ended-session authority..

Trigger: Expiry, logout, revocation, or account change occurs..

Preconditions: The synthetic peer records connection identity, message IDs, and authorization decisions..

| Step | Actor action | System response | Rule or requirement IDs | Observable evidence |
| --- | --- | --- | --- | --- |
| 1 | User A establishes a protected connection. | The peer records principal and credential expiry. | See linked case evidence classes | [RN-T003](06-test-cases.md#rn-t003), [RN-T004](06-test-cases.md#rn-t004), [RN-T005](06-test-cases.md#rn-t005), [RN-T006](06-test-cases.md#rn-t006), [RN-T007](06-test-cases.md#rn-t007), [RN-T008](06-test-cases.md#rn-t008), [RN-T009](06-test-cases.md#rn-t009), [RN-T018](06-test-cases.md#rn-t018) |
| 2 | The lifecycle boundary occurs. | The fixture records the boundary timestamp. | See linked case evidence classes | Same canonical cases |
| 3 | The peer emits a protected message or reconnects. | Authorization and client delivery are asserted separately. | See linked case evidence classes | Same canonical cases |

Limits: Mid-connection reauthentication and revocation policy require transport-owner evidence.

### UC-T03

**Keep subscription routing and permission checks distinct**

Goal: Prevent topic and workspace confusion when subscriptions overlap..

Trigger: Multiple subscriptions connect, reconnect, or receive malformed data..

Preconditions: The fixture provides authorized and denied topics with distinct message IDs..

| Step | Actor action | System response | Rule or requirement IDs | Observable evidence |
| --- | --- | --- | --- | --- |
| 1 | W-A and W-B subscribe. | The fixture records topic and connection identities. | See linked case evidence classes | [RN-T011](06-test-cases.md#rn-t011), [RN-T012](06-test-cases.md#rn-t012), [RN-T013](06-test-cases.md#rn-t013), [RN-T016](06-test-cases.md#rn-t016), [RN-T017](06-test-cases.md#rn-t017) |
| 2 | The server sends selected messages. | Each workspace receives only its intended authorized payload. | See linked case evidence classes | Same canonical cases |
| 3 | The driver checks subscription state. | Counts, callback routing, and authorization are asserted. | See linked case evidence classes | Same canonical cases |

Limits: Client callback checks do not prove server topic authorization.

### UC-T04

**Recover message delivery after reconnect**

Goal: Measure duplicate and missed messages during renewal reconnect..

Trigger: A disconnect creates a replay or delivery gap..

Preconditions: Message IDs and sequence numbers are available from the synthetic peer..

| Step | Actor action | System response | Rule or requirement IDs | Observable evidence |
| --- | --- | --- | --- | --- |
| 1 | The peer delivers N-1. | The fixture records callback and UI counts. | See linked case evidence classes | [RN-T014](06-test-cases.md#rn-t014), [RN-T015](06-test-cases.md#rn-t015) |
| 2 | The socket disconnects and renews. | The peer records the outage interval. | See linked case evidence classes | Same canonical cases |
| 3 | The peer replays or resumes. | The fixture records duplicates and recovery requests. | See linked case evidence classes | Same canonical cases |

Limits: Exactly-once UI delivery and permitted loss are not defined by the renewal requirement.

### UC-T05

**Protect long HTTP and transfer operations across renewal**

Goal: Bind long-lived requests and mutations to their correct session and operation..

Trigger: Renewal overlaps polling, SSE, download, upload, or TLS interruption..

Preconditions: Use isolated synthetic endpoints and unique operation IDs..

| Step | Actor action | System response | Rule or requirement IDs | Observable evidence |
| --- | --- | --- | --- | --- |
| 1 | User A starts the long operation. | The fixture records request principal and operation ID. | See linked case evidence classes | [RN-T021](06-test-cases.md#rn-t021), [RN-T022](06-test-cases.md#rn-t022), [RN-T023](06-test-cases.md#rn-t023), [RN-T024](06-test-cases.md#rn-t024), [RN-T025](06-test-cases.md#rn-t025), [RN-T026](06-test-cases.md#rn-t026), [RN-T027](06-test-cases.md#rn-t027), [RN-T030](06-test-cases.md#rn-t030) |
| 2 | Renewal or logout occurs. | The lifecycle boundary and credential identity are retained. | See linked case evidence classes | Same canonical cases |
| 3 | The operation settles or resumes. | Protected access, content identity, and mutation count are checked. | See linked case evidence classes | Same canonical cases |

Limits: Transfer continuation and SSE lifetime acceptance need protocol-specific contracts.

### UC-T06

**Handle background execution and cached protected results**

Goal: Prevent workers and caches from crossing identity boundaries..

Trigger: A worker or service worker completes after logout or account change..

Preconditions: Record actual worker presence and cache provenance..

| Step | Actor action | System response | Rule or requirement IDs | Observable evidence |
| --- | --- | --- | --- | --- |
| 1 | User A starts background work. | The fixture records session and request identity. | See linked case evidence classes | [RN-T028](06-test-cases.md#rn-t028), [RN-T029](06-test-cases.md#rn-t029) |
| 2 | The current identity changes. | The fixture records the new principal. | See linked case evidence classes | Same canonical cases |
| 3 | The background result or cached response returns. | No prior-principal protected result is exposed to the new principal. | See linked case evidence classes | Same canonical cases |

Limits: Synthetic worker probes do not establish a deployed worker consumer.

### UC-S01

**Revoke renewable credentials**

Goal: Prevent renewal after explicit logout.

Trigger: User signs out with renewable credentials.

Preconditions: A synthetic identity owns access and refresh credentials.

| Step | Actor action | System response | Rule or requirement IDs | Observable evidence |
| --- | --- | --- | --- | --- |
| 1 | Submit logout and attempt renewal | Prevent renewal after explicit logout | See linked case evidence classes | [RN-S001](06-test-cases.md#rn-s001), [RN-S002](06-test-cases.md#rn-s002), [RN-S003](06-test-cases.md#rn-s003), [RN-S004](06-test-cases.md#rn-s004), [RN-S005](06-test-cases.md#rn-s005), [RN-S006](06-test-cases.md#rn-s006), [RN-S007](06-test-cases.md#rn-s007), [RN-S008](06-test-cases.md#rn-s008), [RN-S009](06-test-cases.md#rn-s009), [RN-S010](06-test-cases.md#rn-s010) |

Limits: Global logout policy and deployed propagation remain unknown.

### UC-S02

**Validate renewal credentials**

Goal: Reject invalid or inappropriate credentials.

Trigger: A client requests refresh acquisition or relogin.

Preconditions: Use an isolated issuer and synthetic RSA keys.

| Step | Actor action | System response | Rule or requirement IDs | Observable evidence |
| --- | --- | --- | --- | --- |
| 1 | Submit a controlled credential and inspect response plus state | Reject invalid or inappropriate credentials | See linked case evidence classes | [RN-S011](06-test-cases.md#rn-s011), [RN-S012](06-test-cases.md#rn-s012), [RN-S013](06-test-cases.md#rn-s013), [RN-S014](06-test-cases.md#rn-s014), [RN-S015](06-test-cases.md#rn-s015), [RN-S016](06-test-cases.md#rn-s016), [RN-S017](06-test-cases.md#rn-s017), [RN-S018](06-test-cases.md#rn-s018), [RN-S019](06-test-cases.md#rn-s019), [RN-S020](06-test-cases.md#rn-s020), [RN-S021](06-test-cases.md#rn-s021), [RN-S022](06-test-cases.md#rn-s022), [RN-S023](06-test-cases.md#rn-s023), [RN-S024](06-test-cases.md#rn-s024) |

Limits: Provider contract and target verifier settings require confirmation.

### UC-S03

**Isolate session generations**

Goal: Prevent an old session from changing a replacement session.

Trigger: A delayed result arrives after login or logout.

Preconditions: Session A and session B have distinct synthetic subjects.

| Step | Actor action | System response | Rule or requirement IDs | Observable evidence |
| --- | --- | --- | --- | --- |
| 1 | Hold A response; establish B; release A; inspect B | Prevent an old session from changing a replacement session | See linked case evidence classes | [RN-S025](06-test-cases.md#rn-s025), [RN-S026](06-test-cases.md#rn-s026), [RN-S027](06-test-cases.md#rn-s027), [RN-S028](06-test-cases.md#rn-s028), [RN-S029](06-test-cases.md#rn-s029), [RN-S030](06-test-cases.md#rn-s030), [RN-S031](06-test-cases.md#rn-s031), [RN-S032](06-test-cases.md#rn-s032) |

Limits: Direct dispatch callers and cross-tab ownership policy remain unknown.

### UC-S04

**Enforce origin and destination boundaries**

Goal: Prevent credential leakage and forged renewal.

Trigger: A lower-trust origin or module invokes a request.

Preconditions: Use two local test origins and synthetic credentials.

| Step | Actor action | System response | Rule or requirement IDs | Observable evidence |
| --- | --- | --- | --- | --- |
| 1 | Observe request destinations, CORS, and authenticated effects | Prevent credential leakage and forged renewal | See linked case evidence classes | [RN-S033](06-test-cases.md#rn-s033), [RN-S034](06-test-cases.md#rn-s034), [RN-S035](06-test-cases.md#rn-s035), [RN-S036](06-test-cases.md#rn-s036), [RN-S037](06-test-cases.md#rn-s037), [RN-S038](06-test-cases.md#rn-s038), [RN-S039](06-test-cases.md#rn-s039), [RN-S040](06-test-cases.md#rn-s040) |

Limits: These checks propose security invariants; target proxy evidence is unavailable.

### UC-S05

**Contain retained session data**

Goal: Prevent credentials and prior-user data disclosure.

Trigger: Logout, account switch, or diagnostics run.

Preconditions: Use synthetic users A and B with distinct records.

| Step | Actor action | System response | Rule or requirement IDs | Observable evidence |
| --- | --- | --- | --- | --- |
| 1 | Inspect browser state and sanitized observations | Prevent credentials and prior-user data disclosure | See linked case evidence classes | [RN-S041](06-test-cases.md#rn-s041), [RN-S042](06-test-cases.md#rn-s042), [RN-S043](06-test-cases.md#rn-s043), [RN-S044](06-test-cases.md#rn-s044), [RN-S045](06-test-cases.md#rn-s045), [RN-S046](06-test-cases.md#rn-s046), [RN-S047](06-test-cases.md#rn-s047) |

Limits: Sensitive data retention policy and approved telemetry fields remain unknown.

### UC-S06

**Authorize every continued connection**

Goal: Prevent streams from retaining unauthorized access.

Trigger: Renewal, revocation, or permission change occurs.

Preconditions: Use isolated stream servers with observable authorization.

| Step | Actor action | System response | Rule or requirement IDs | Observable evidence |
| --- | --- | --- | --- | --- |
| 1 | Renew or revoke identity; inspect stream actions and deliveries | Prevent streams from retaining unauthorized access | See linked case evidence classes | [RN-S048](06-test-cases.md#rn-s048), [RN-S049](06-test-cases.md#rn-s049), [RN-S050](06-test-cases.md#rn-s050), [RN-S051](06-test-cases.md#rn-s051), [RN-S052](06-test-cases.md#rn-s052), [RN-S053](06-test-cases.md#rn-s053), [RN-S054](06-test-cases.md#rn-s054), [RN-S055](06-test-cases.md#rn-s055) |

Limits: Server stream contracts and revocation deadlines require owner decisions.

### UC-X01

**Six manual recovery cycles preserve three workspaces**

Goal: Verify the stated real-browser predicate.

Trigger: User A reaches access expiry in each of six controlled cycles.

Preconditions: User A uses the isolated local portal fixture with three empty workspaces the browser clock is controlled and renewal responses use synthetic credentials the fixture records initial workspace IDs and prompt closure transitions.

| Step | Actor action | System response | Rule or requirement IDs | Observable evidence |
| --- | --- | --- | --- | --- |
| 1 | Run the linked canonical browser case | Retain per-assertion results and source identity | See linked case evidence classes | [RN-X001](06-test-cases.md#rn-x001) |

Limits: Actual portal DOM and Axios; synthetic authentication, controlled time, empty workspace descriptors. No embedded application data, real transport, provider validation or deployment proof.

### UC-X02

**Twenty-five click events share one pending manual renewal**

Goal: Verify the stated real-browser predicate.

Trigger: User A reaches access expiry.

Preconditions: User A uses the isolated local portal fixture with three empty workspaces the browser clock is controlled and renewal responses use synthetic credentials the fixture records initial workspace IDs and prompt closure transitions the manual renewal response remains held.

| Step | Actor action | System response | Rule or requirement IDs | Observable evidence |
| --- | --- | --- | --- | --- |
| 1 | Run the linked canonical browser case | Retain per-assertion results and source identity | See linked case evidence classes | [RN-X002](06-test-cases.md#rn-x002) |

Limits: Actual portal DOM and Axios; synthetic authentication, controlled time, empty workspace descriptors. No embedded application data, real transport, provider validation or deployment proof.

### UC-X03

**Logout rejects late completion from pending manual renewal**

Goal: Verify the stated real-browser predicate.

Trigger: User A reaches access expiry.

Preconditions: User A uses the isolated local portal fixture with three empty workspaces the browser clock is controlled and renewal responses use synthetic credentials the fixture records initial workspace IDs and prompt closure transitions the manual renewal response remains held.

| Step | Actor action | System response | Rule or requirement IDs | Observable evidence |
| --- | --- | --- | --- | --- |
| 1 | Run the linked canonical browser case | Retain per-assertion results and source identity | See linked case evidence classes | [RN-X003](06-test-cases.md#rn-x003) |

Limits: Actual portal DOM and Axios; synthetic authentication, controlled time, empty workspace descriptors. No embedded application data, real transport, provider validation or deployment proof.

### UC-C01

**Combine declared session states**

Goal: Cover declared interactions with independent observable assertions.

Trigger: The interaction runner selects one fixture row.

Preconditions: Create an isolated context for every row.

| Step | Actor action | System response | Rule or requirement IDs | Observable evidence |
| --- | --- | --- | --- | --- |
| 1 | Apply the selected factors in canonical order | Measure stale writes, authorization, and mutation uniqueness | See linked case evidence classes | [RN-C001](06-test-cases.md#rn-c001), [RN-C002](06-test-cases.md#rn-c002) |

Limits: Pairwise design coverage does not establish business correctness

### UC-C02

**Enumerate late-response event orders**

Goal: Keep old replies from changing a replacement identity.

Trigger: The runner selects one six-event ordering.

Preconditions: A and B have distinct synthetic sessions.

| Step | Actor action | System response | Rule or requirement IDs | Observable evidence |
| --- | --- | --- | --- | --- |
| 1 | Deliver the exact canonical event sequence | Assert final B identity and zero obsolete writes | See linked case evidence classes | [RN-O001](06-test-cases.md#rn-o001) |

Limits: Only the declared finite partial order is exhausted

## Alternative and exception flows

| Flow ID | Branch from step | Condition | Action and response | Outcome | Criterion IDs |
| --- | --- | --- | --- | --- | --- |
| [UC-R01-ALT-1](#uc-r01) | 1 | The named boundary or failure occurs | Retain the linked case observations | Continuous input can expose the recorded debounce defect | See each canonical case; unresolved policy stays blocked |
| [UC-R02-ALT-1](#uc-r02) | 1 | The named boundary or failure occurs | Retain the linked case observations | Cross-origin, touch, composition, and passive activity eligibility remain unresolved | See each canonical case; unresolved policy stays blocked |
| [UC-R03-ALT-1](#uc-r03) | 1 | The named boundary or failure occurs | Retain the linked case observations | These are implementation thresholds, not business lifetime policies | See each canonical case; unresolved policy stays blocked |
| [UC-R04-ALT-1](#uc-r04) | 1 | The named boundary or failure occurs | Retain the linked case observations | The two-second margin is source behavior | See each canonical case; unresolved policy stays blocked |
| [UC-R05-ALT-1](#uc-r05) | 1 | The named boundary or failure occurs | Retain the linked case observations | The reuse interval is implementation behavior | See each canonical case; unresolved policy stays blocked |
| [UC-R06-ALT-1](#uc-r06) | 1 | The named boundary or failure occurs | Retain the linked case observations | Clock skew acceptance remains unresolved | See each canonical case; unresolved policy stays blocked |
| [UC-R07-ALT-1](#uc-r07) | 1 | The named boundary or failure occurs | Retain the linked case observations | Service provider behavior remains outside substituted responses | See each canonical case; unresolved policy stays blocked |
| [UC-R08-ALT-1](#uc-r08) | 1 | The named boundary or failure occurs | Retain the linked case observations | Cross-device revocation needs separate policy | See each canonical case; unresolved policy stays blocked |
| [UC-R09-ALT-1](#uc-r09) | 1 | The named boundary or failure occurs | Retain the linked case observations | Browser header normalization and future-iat policy need review | See each canonical case; unresolved policy stays blocked |
| [UC-R10-ALT-1](#uc-r10) | 1 | The named boundary or failure occurs | Retain the linked case observations | Local isolation does not establish server revocation | See each canonical case; unresolved policy stays blocked |
| [UC-R11-ALT-1](#uc-r11) | 1 | The named boundary or failure occurs | Retain the linked case observations | Direct relogin calls have different cancellation behavior | See each canonical case; unresolved policy stays blocked |
| [UC-R12-ALT-1](#uc-r12) | 1 | The named boundary or failure occurs | Retain the linked case observations | Several same-epoch ordering policies remain unresolved | See each canonical case; unresolved policy stays blocked |
| [UC-R13-ALT-1](#uc-r13) | 1 | The named boundary or failure occurs | Retain the linked case observations | Finite loops do not prove unlimited lifetime or performance | See each canonical case; unresolved policy stays blocked |
| [UC-R14-ALT-1](#uc-r14) | 1 | The named boundary or failure occurs | Retain the linked case observations | No finite test proves indefinite renewal | See each canonical case; unresolved policy stays blocked |
| [UC-R15-ALT-1](#uc-r15) | 1 | The named boundary or failure occurs | Retain the linked case observations | Global logout and restoration policies remain unresolved | See each canonical case; unresolved policy stays blocked |
| [UC-R16-ALT-1](#uc-r16) | 1 | The named boundary or failure occurs | Retain the linked case observations | Maximum pending duration and service retry policy remain unresolved | See each canonical case; unresolved policy stays blocked |
| [UC-W01-ALT-1](#uc-w01) | 1 | A module import rejects. | Retain the linked case observations | Module failure and session outcome are recorded separately. | See each canonical case; unresolved policy stays blocked |
| [UC-W01-ALT-2](#uc-w01) | 1 | The selected workspace is removed. | Retain the linked case observations | The next selection is checked against source-derived behavior. | See each canonical case; unresolved policy stays blocked |
| [UC-W02-ALT-1](#uc-w02) | 1 | An old-session request completes. | Retain the linked case observations | Its response cannot alter the replacement session loader. | See each canonical case; unresolved policy stays blocked |
| [UC-W02-ALT-2](#uc-w02) | 1 | Response parsing fails. | Retain the linked case observations | Rejection and loader cleanup are checked independently. | See each canonical case; unresolved policy stays blocked |
| [UC-W03-ALT-1](#uc-w03) | 1 | A module import resolves after logout. | Retain the linked case observations | Ended-session credentials cannot authorize protected service work. | See each canonical case; unresolved policy stays blocked |
| [UC-W03-ALT-2](#uc-w03) | 1 | A removed workspace receives data. | Retain the linked case observations | Another workspace must not display that data. | See each canonical case; unresolved policy stays blocked |
| [UC-W04-ALT-1](#uc-w04) | 1 | Unsaved state differs. | Retain the linked case observations | Acceptance remains blocked until preservation policy is defined. | See each canonical case; unresolved policy stays blocked |
| [UC-W05-ALT-1](#uc-w05) | 1 | No usable credential exists. | Retain the linked case observations | Queueing and recovery acceptance remain unresolved. | See each canonical case; unresolved policy stays blocked |
| [UC-W06-ALT-1](#uc-w06) | 1 | Only passive server updates occur. | Retain the linked case observations | Activity eligibility remains policy-open. | See each canonical case; unresolved policy stays blocked |
| [UC-W07-ALT-1](#uc-w07) | 1 | Contexts share local storage. | Retain the linked case observations | Synchronization policy and observed effects remain distinct. | See each canonical case; unresolved policy stays blocked |
| [UC-W07-ALT-2](#uc-w07) | 1 | Contexts use separate profiles. | Retain the linked case observations | Credentials and protected records remain isolated. | See each canonical case; unresolved policy stays blocked |
| [UC-T01-ALT-1](#uc-t01) | 1 | The handshake fails. | Retain the linked case observations | Transport rejection is not a successful renewal. | See each canonical case; unresolved policy stays blocked |
| [UC-T01-ALT-2](#uc-t01) | 1 | Renewal is still pending. | Retain the linked case observations | No success is inferred before response completion. | See each canonical case; unresolved policy stays blocked |
| [UC-T02-ALT-1](#uc-t02) | 1 | Only heartbeats or pushed messages occur. | Retain the linked case observations | Human activity eligibility remains unresolved. | See each canonical case; unresolved policy stays blocked |
| [UC-T02-ALT-2](#uc-t02) | 1 | A retry was queued before logout. | Retain the linked case observations | No new ended-session grant is permitted. | See each canonical case; unresolved policy stays blocked |
| [UC-T03-ALT-1](#uc-t03) | 1 | Both subscriptions share one URL. | Retain the linked case observations | Shared retry-state effects are measured. | See each canonical case; unresolved policy stays blocked |
| [UC-T03-ALT-2](#uc-t03) | 1 | A payload is malformed. | Retain the linked case observations | No mutation is created from invalid data. | See each canonical case; unresolved policy stays blocked |
| [UC-T04-ALT-1](#uc-t04) | 1 | N-2 was emitted during disconnection. | Retain the linked case observations | The result records replay, recovery, or loss without assuming policy. | See each canonical case; unresolved policy stays blocked |
| [UC-T05-ALT-1](#uc-t05) | 1 | The target has no actual SSE consumer. | Retain the linked case observations | The gap remains explicit; synthetic checks do not prove target coverage. | See each canonical case; unresolved policy stays blocked |
| [UC-T05-ALT-2](#uc-t05) | 1 | A transfer resumes. | Retain the linked case observations | Ended-session authority cannot authorize the resume. | See each canonical case; unresolved policy stays blocked |
| [UC-T06-ALT-1](#uc-t06) | 1 | The target has no worker or service worker. | Retain the linked case observations | Record the composition gap and keep target execution unverified. | See each canonical case; unresolved policy stays blocked |
| [UC-S01-ALT-1](#uc-s01) | 1 | Expired access; unavailable revocation store; concurrent renewal | Retain the linked case observations | Global logout policy and deployed propagation remain unknown. | See each canonical case; unresolved policy stays blocked |
| [UC-S02-ALT-1](#uc-s02) | 1 | Wrong issuer; modified signature; expired claims; header ambiguity | Retain the linked case observations | Provider contract and target verifier settings require confirmation. | See each canonical case; unresolved policy stays blocked |
| [UC-S03-ALT-1](#uc-s03) | 1 | Old success; old error; direct token dispatch; parallel login | Retain the linked case observations | Direct dispatch callers and cross-tab ownership policy remain unknown. | See each canonical case; unresolved policy stays blocked |
| [UC-S04-ALT-1](#uc-s04) | 1 | Cookie-only calls; hostile endpoint; iframe; skipped headers | Retain the linked case observations | These checks propose security invariants; target proxy evidence is unavailable. | See each canonical case; unresolved policy stays blocked |
| [UC-S05-ALT-1](#uc-s05) | 1 | Storage; history; diagnostics; stale workspace data | Retain the linked case observations | Sensitive data retention policy and approved telemetry fields remain unknown. | See each canonical case; unresolved policy stays blocked |
| [UC-S06-ALT-1](#uc-s06) | 1 | WebSocket; SSE; upload; permission withdrawal; reconnect storm | Retain the linked case observations | Server stream contracts and revocation deadlines require owner decisions. | See each canonical case; unresolved policy stays blocked |
| [UC-X01-ALT-1](#uc-x01) | 1 | A predicate fails | Retain the linked case observations | Save the failure before continuing | See each canonical case; unresolved policy stays blocked |
| [UC-X02-ALT-1](#uc-x02) | 1 | A predicate fails | Retain the linked case observations | Save the failure before continuing | See each canonical case; unresolved policy stays blocked |
| [UC-X03-ALT-1](#uc-x03) | 1 | A predicate fails | Retain the linked case observations | Save the failure before continuing | See each canonical case; unresolved policy stays blocked |
| [UC-C01-ALT-1](#uc-c01) | 1 | A guard prevents renewal | Retain the linked case observations | Record zero outbound requests without fabricating success | See each canonical case; unresolved policy stays blocked |
| [UC-C02-ALT-1](#uc-c02) | 1 | The A response rejects or is malformed | Retain the linked case observations | B remains isolated | See each canonical case; unresolved policy stays blocked |

## Related artifacts

| Artifact ID | Relationship | Location |
| --- | --- | --- |
| Test catalog | Single definition source | [Canonical cases](06-test-cases.md#comprehensive-renewal-expansion) |
| Strategy | Scope and completion | [Test strategy](05-test-strategy-renewal.md) |
| Security review | Threats and evidence | [Review](07-security-review-renewal.md) |
| Coverage | Separate coverage dimensions | [Coverage](09-renewal-coverage.md) |

## Sources and evidence limits

| Source ID | Locator | Exact revision | Available hash | Owner, authority, and limit |
| --- | --- | --- | --- | --- |
| SRC-comprehensive-renewal-20261028 | [Exact request](evidence/user-input-20261028-comprehensive-renewal.txt) | user-message-20261028 | [Manifest](evidence/comprehensive-renewal-20261028/source-manifest.json) | User; design and assessment authorization |
| Requirement and inspected code | [Manifest](evidence/comprehensive-renewal-20261028/source-manifest.json) | Per-source revisions | Per-source SHA-256 | Publication review and target parity remain unproved |

## Unknowns and risks

| Finding or question | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| Revocation gap | [Security result](07-security-review-renewal.md#findings-and-actions) | Logout cannot establish complete credential invalidation | unknown service owner | Correct the boundary and rerun replay cases |
| Transport and restoration policy | [Policy register](05-test-strategy-renewal.md#policy-questions) | Several acceptance outcomes remain blocked | unknown business and security owners | Record one reviewed answer per policy scope |

## Review and execution status

Required review covers actors, eligibility, recovery, authorization, retention, and transport behavior. Actual human review reference: null.
Three new browser journeys passed within their disclosed fixture. Other new journeys remain unexecuted.
Read the [execution report](08-test-execution-renewal.md) for exact predicates, substitutions, failures, and source identity.
