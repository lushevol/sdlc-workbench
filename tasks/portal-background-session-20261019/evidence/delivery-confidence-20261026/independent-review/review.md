# Independent MFE Base review

**Two regressions block an unconditional no-impact claim.**
Owner: unknown application owner. Correct final cancellation cleanup and scheduled acquisition eligibility before claiming preserved behavior.
The [cancellation evidence](#del-cr-01-final-cancellation-retains-the-loader) and [timer evidence](#del-cr-02-a-late-callback-can-remove-manual-recovery) show main-versus-candidate differences.
The timer case uses a synthetic matching-expiry state. Natural occurrence remains unobserved.

## Scope and result

The [current request](../user-input.md#exact-user-input) authorizes expanded review and tests.
The [structured review](review.json) covers all thirty frozen branch paths.
Main and merge base are `f025513f696476a9cc8162681410cbd21e029bcb`.
The candidate is `c42e7609c4e14eb53de32702e4bd3424a223988a`.
The [context](context.json) records fingerprint `894c69511c017e7042f11722c2e4135d51b1e85784e84e463da7db559f75493a`.
The [source manifest](source-manifest.json) binds thirty changed paths and thirty-four supporting sources.

Concurrent delivery tests have separate identities. They do not change the frozen runtime comparison.

## DEL-CR-01: final cancellation retains the loader

Priority: P2, proposed. Confidence: HIGH for the reproduced public-client outcome.
The public shared client accepts an AbortSignal. Its request handler enables loading by default.
The new [error-handler guard](../../../../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L10) rejects cancellation before loading cleanup.
The unchanged [renderer](../../../../../repos/ui/mfe-base/src/routing/index.tsx#L27) displays PageLoader while loading remains true.

Setup: one loading-enabled current-session request exists. No replacement or later response occurs.

1. Start the request through the exported shared client.
2. Abort its signal before completion.
3. Observe request rejection, authentication, error state, loading, and PageLoader.

Intended result: reject cancellation without credential or error changes. Clear loading when no current loading request remains.
Old result: main clears loading and removes PageLoader.
New result: candidate keeps loading and PageLoader active.
Both revisions reject `ERR_CANCELED`. Both preserve credentials and error state.

The [main browser result](../browser/main/main-cancelledLoader-20261026T153205/artifacts/DEL-14-cancelled-generic-request-loader-1793028733686/result.json) passes.
The [candidate browser result](../browser/candidate-headless/candidate-cancelledLoader-20261026T153330/artifacts/DEL-14-cancelled-generic-request-loader-1793028820175/result.json) fails.
Both execute actual Axios through public `Service.getService`.
The [earlier handler comparison](cancellation-comparison.json) agrees with the browser observations.

Browser user agents identify headless Edge. These results establish DOM and service behavior.
They supply no native lifecycle evidence or production-frequency estimate.

Consequence: final cancellation can leave PageLoader active after the request settles.
Owner: unknown application owner.
Next action: track current-session loading work through cancellation and settlement. Preserve stale-session isolation.
Keep loading active while replacement work remains pending. A bare `loading=false` dispatch can hide that pending work.

Verify [DEL-14](../../../06-test-cases.md#del-14) and [DEL-19](../../../06-test-cases.md#del-19) together.

Counterevidence: inspected local admin callers abort and immediately replace requests.
No ordinary local final-abort GUI gesture or production occurrence was observed.
The exported AbortSignal interface supports the tested trigger. Deployed frequency remains unknown.

## DEL-CR-02: a late callback can remove manual recovery

Priority: P2, proposed. Confidence: HIGH for the controlled matching-expiry comparison.
The [scheduler](../../../../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L147) targets access expiry minus twenty-five seconds.
Its [guard](../../../../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L140) requires twenty-five seconds remaining when refresh already exists.
A callback one millisecond late sees `24999` milliseconds. It skips acquisition despite valid access and refresh credentials.

Setup: visible Home has access and refresh credentials that expire together in sixty seconds.
No activity, hidden transition, or provider delay occurs. Immediate adapter responses isolate the scheduling difference.

1. Mount Home with the declared credentials.
2. Record initial credential claims, hashes, store expiry, and request count.
3. Displace the controlled wall clock by one millisecond.
4. Run the previously scheduled acquisition timer.
5. Advance through credential expiry and the Logout delay.
6. Observe replacement refresh, Extend availability, authentication, and Logout requests.

Intended result: preserve the scheduled acquisition despite slight callback delay. Keep the separate restriction against late page-return replay.
Old result: main acquires replacement refresh. Extend remains enabled, and no Logout request occurs.
New result: candidate skips acquisition. Extend becomes unavailable, both Logout requests run, and authentication clears.

The [comparison](late-timer-comparison.json) binds both exact source archives and the common test hash.
The [main observation](late-timer-initial-main-observation.json) and [candidate observation](late-timer-initial-candidate-observation.json) contain identical initial objects.
Both start with equal access and refresh expiry, identical credential hashes, visible Home, and zero requests.
The [main Jest result](late-timer-initial-main-jest.json) passes all eight assertions.
The [candidate Jest result](late-timer-initial-candidate-jest.json) passes four setup assertions, then fails the forced-logout assertion.
Exact commands, environment, times, and exit codes are retained in the [command metadata](late-timer-initial-commands.json).

Consequence: this state loses manual recovery and starts Logout after a slight acquisition delay.
Owner: unknown application owner.
Next action: distinguish scheduled-callback eligibility from the visibility replay cutoff.
Preserve stale-session isolation, pending-request reuse, expiry reconciliation, and late-return behavior.
Verify [DEL-20](../../../06-test-cases.md#del-20) with those controls. No fixed grace period is proposed.

The state and clock displacement are synthetic. Natural matching-expiry occurrence and native timer jitter remain unobserved.
The experiment observes recovery availability. It does not click Extend or contact a live provider.

The earlier [F-02 review](../../../07-code-review-minor-20261021.md#f-02-p3-permit-acquisition-when-its-timer-runs-slightly-late) remains historical evidence.
That earlier case retained a usable refresh credential. This case adds the matching-expiry consequence.

The [provider audit](follow-up-audit.json) supplies a source-compatible sequence as an inference.
Access extension issues new access without replacing refresh. Access and refresh expiries use independent issue times and configured lifetimes.
Extension near an older refresh deadline can produce matching expiries. No inspected provider rule requires deadline ordering.
This inference does not establish a deployed occurrence or effective configuration.

A [default-lifetime control](late-timer-provider-comparison.json) uses older issue times with the same expiry sixty seconds ahead.
Access lifetime equals fifteen minutes. Refresh lifetime equals 225 minutes plus twenty-four seconds.
The [main control](late-timer-provider-main-jest.json) passes ten assertions.
The [candidate control](late-timer-provider-candidate-jest.json) passes six setup and lifetime assertions, then fails the forced-logout assertion.

The initial claims and credential hashes match across revisions. Natural occurrence remains unobserved.
The [control commands](late-timer-provider-commands.json) retain exact execution inputs.

## Other reviewed boundaries

Ownership stamping precedes dispatch. Logout and fresh login invalidate older response ownership.
Current-session invalid-token errors still clear authentication. Ordinary access rotation preserves refresh credentials.
Timeout waits for renewal completion. Rejection preserves usable retry, and Logout can cancel pending recovery.

Valid access permits refresh replacement after refresh expiry. Provider validation remains unchanged.
Workspace guards prevent undefined selections. No additional actionable defect was confirmed in these inspected paths.

The [follow-up audit](follow-up-audit.json) records provider response contracts and inspected token setters.
Known login paths install access through `setAuthorization`. OpenFin storage is followed by hard navigation.
No inspected Base, Ratan, or Cashflow application caller directly invokes exported `dispacthToken`.
Unknown deployed setters remain outside this inspected scope.

The [configuration evaluation](build-config-effects.json) finds loopback HTTP chunk publicPath from committed server settings.
`FILE_LIMIT` parses to one byte. The inspected server exposes static files and health GET routes.
No supported JSON-body business route was found. No `cduplatform` import was found in application source.

External pipeline rewriting and immutable delivery settings remain unavailable. These limits block a positive target-configuration conclusion.

Continuous mouse activity still resets its five-second timer. Keyboard and scroll handlers remain absent.
Those behaviors also exist on main. Their recorded P4/S4 backlog disposition remains separate from these regressions.
The independent review does not verify the exact four-hour criterion.

## Validation and limits

The [review validation](validation.json) checks identity, path coverage, and changed-line anchors.
The [scan](scan.json) completed secret-pattern inspection. Its candidates are synthetic test-token assignments.
No weakened legacy assertions were found in inspected delivery additions.
Deferred four-hour component adapters prove settlement handling. They do not prove four-hour Axios network survival.

The final full-suite and canonical test manifest belong to the parallel verification worker.

No runtime source, dependency, credential, or unrelated compiler cache was changed by this review.
No immutable delivery artifact, target configuration, or live provider execution was assessed.
Source inspection does not grant deployment approval or establish complete absence of regressions.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
