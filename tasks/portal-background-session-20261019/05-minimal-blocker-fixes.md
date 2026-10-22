---
artifact_kind: implementation-plan
id: PLAN-session-minimal-blocker-fixes-20261023
version: 1
status: draft
owner: unknown
source_refs:
  - SRC-session-minimal-request-20261023
  - SRC-session-minimal-source-20261023
  - SRC-session-review-intent-v4
related_ids:
  - REQ-active-session-renewal
  - CHANGE-session-post-review-20261020
  - ASSESS-session-refresh-release-20261022
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

# Smallest candidate corrections for the release blockers

> **The release hold remains. These snippets are proposals, without application changes or passing execution.**
> Action: implement and verify the corrections, then bind the actual release artifact and operating evidence.
> Consequence: the [current failures](10-release-confidence.md#findings) still block a positive PROD recommendation.
> Owner: unknown application and release owners. Evidence: [source designs](evidence/minimal-blocker-fixes-20261023/timeout-recovery-design.json) and [ownership review](evidence/minimal-blocker-fixes-20261023/stale-session-design.json).

## Objective and baseline

| Field | Value |
| --- | --- |
| Outcome and requirement IDs | Preserve valid access, isolate sessions, and permit required delayed recovery. [Requirement version 4](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria). |
| Included and excluded work | Proposed source excerpts for three runtime blockers. No application edits, new executions, or deployment. |
| Repository baselines | `mfe-base`: `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85`; comparison baseline `f025513f696476a9cc8162681410cbd21e029bcb`. |
| Design and decision references | [Release findings](10-release-confidence.md#findings); [current stage](10-change-review.md#current-task-state). No criterion waiver is recorded. |
| Delivery constraints | Timing settings remain unchanged. Existing Axios timeout is 60,000 milliseconds. PROD conditions remain unbound. |
| Plan state | proposed; ready for explanation and review only |

The [exact request](evidence/minimal-blocker-fixes-20261023/user-request.txt) asks how to make the smallest corrections.
The snippets show insertion points. They are not a complete patch.
Imports and existing function bodies must be retained during implementation.
The [source inventory](evidence/minimal-blocker-fixes-20261023/source-inventory.json) records revisions, hashes, and preservation boundaries.

## Affected scope and risk

All MFE locations below use the exact candidate listed above.

| Symbol or boundary | Inspected location | Callers and importers | Expected impact | Qualitative risk and reason |
| --- | --- | --- | --- | --- |
| `reconcileExpiry` | [Home controller](../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L117) | Home timers and visibility changes. | Separate access expiry from refresh replacement. | Medium; valid sessions currently end. |
| Axios request and response interceptors | [Configuration](../../repos/ui/mfe-base/src/hooks/service/config.ts#L17), [request](../../repos/ui/mfe-base/src/hooks/service/util/success.request.handler.ts#L4), [success](../../repos/ui/mfe-base/src/hooks/service/util/succes.response.handler.ts#L26), [error](../../repos/ui/mfe-base/src/hooks/service/util/error.response.handler.ts#L6) | Generic wrappers, direct refresh, relogin, extend, and exported service consumers. | Prevent stale success and errors from changing another session. | High; shared authentication state has many consumers. |
| Session boundaries | [Login handling](../../repos/ui/mfe-base/src/utils/login.ts#L51), [storage clearing](../../repos/ui/mfe-base/src/utils/common.ts#L71) | Fresh v2/v3 login, logout, validation failure, and invalid-token handling. | Clear old refresh state and invalidate old work. | High; ordinary access renewal must preserve the session. |
| Timeout recovery | [Controller](../../repos/ui/mfe-base/src/components/Timeout/common/useController.ts#L25), [buttons](../../repos/ui/mfe-base/src/components/Timeout/index.tsx#L21), [service](../../repos/ui/mfe-base/src/hooks/service/index.ts#L37) | Access expiry and manual Extend. | Wait for pending credentials; close only after usable renewal. | High; timers, loading, and responses can race. |

## Preconditions

| Dependency or question | Required resolution | Owner | Evidence | State |
| --- | --- | --- | --- | --- |
| Intended behavior | Use existing requirement and canonical cases. | unknown application owner | [Requirement](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria). Publication review remains pending. | sufficient for proposal |
| Session tagging | Keep every request interceptor synchronous, or stamp ownership before calling Axios. | unknown application owner | Installed Axios supports the synchronous option. Current source registers one request interceptor. | proposed invariant |
| Credential replacement | Keep the BFF access-token and server-session validation boundary. | unknown authentication owner | [Contract inspection](evidence/minimal-blocker-fixes-20261023/timeout-recovery-design.json). No old refresh token is required by that endpoint. | source inspected; PROD unbound |
| Execution and deployment | Select exact test revisions, artifact, settings, rollback, and operators. | unknown test and release owners | [Operational gaps](10-release-confidence.md#rc-04-prod-artifact-and-operating-evidence-remain-incomplete). | open |

## Ordered tasks

| Task ID | Depends on | Action and output | Owner | Completion evidence | State |
| --- | --- | --- | --- | --- | --- |
| FIX-1 | none | Add session ownership and fresh-login reset. | unknown application owner | Both stale delivery orders pass; current-session invalidation remains effective. | planned |
| FIX-2 | FIX-1 | Replace expired refresh credentials while access remains valid. | unknown application owner | Active-cutoff case passes with a genuinely new refresh credential. | planned |
| FIX-3 | FIX-1, FIX-2 | Wait for current pending acquisition and actual relogin completion. | unknown application owner | Delayed, pending, failure, explicit logout, and immediate controls pass. | planned |
| FIX-4 | FIX-1, FIX-2, FIX-3 | Bind the immutable release and operating evidence. | unknown release owner | Matching build, digest, settings, dependencies, recovery evidence, and responsible operators. | planned |

### FIX-1: reject responses owned by an ended session

Aborting requests alone cannot prevent a response interceptor from installing stale credentials.
An access token also changes during normal renewal. It cannot identify the complete login session.
Use a local session generation for ownership.

Add a dependency-free module, proposed as `src/utils/sessionEpoch.ts`:

```ts
let epoch = 0;

export const currentSessionEpoch = () => epoch;
export const invalidateSession = () => { epoch += 1; };
export const isFreshLogin = (url = "") =>
  /\/auth\/v[23]\/sso\/login(?:[?#]|$)/.test(url);

export const isStaleSessionRequest = (
  config?: { url?: string; sessionEpoch?: number }
) => typeof config?.sessionEpoch === "number" &&
  config.sessionEpoch !== epoch;
```

Register the current request interceptor synchronously in `src/hooks/service/config.ts`:

```ts
service.interceptors.request.use(requestHandler, undefined, {
  synchronous: true,
});
```

Insert this before existing request effects in `success.request.handler.ts`:

```ts
const { store, baseDispatch } = getHooksBase(); // Existing declaration.
if (isFreshLogin(request.url)) {
  invalidateSession();
  baseDispatch({
    type: ActionType.SET_REFRESH_TOKEN,
    data: { refreshToken: undefined },
  });
}
request.sessionEpoch = currentSessionEpoch(); // Local metadata, not a header.
```

Insert this first in `successHandler`, before any `handle*` call:

```ts
if (isStaleSessionRequest(response.config) || response.config?.signal?.aborted) {
  throw new CanceledError("Discarded an ended session response", response.config);
}
const loginAccess = response.headers?.["single-ui-authorization"] ??
  response.headers?.["Single-UI-Authorization"];
if (isFreshLogin(response.config?.url) && loginAccess) {
  // Invalidate requests started with old access while login was pending.
  invalidateSession();
  (response.config as any).sessionEpoch = currentSessionEpoch();
  getHooksBase().baseDispatch({
    type: ActionType.SET_REFRESH_TOKEN,
    data: { refreshToken: undefined },
  });
}
```

Insert this first in `errorHandler`, before invalid-token handling or other state changes:

```ts
if (isStaleSessionRequest(error.config) || error.code === "ERR_CANCELED") {
  return Promise.reject(error);
}
```

Call `invalidateSession()` first in `clearStorageWhenLogout`.
Also invalidate immediately when Timeout's explicit Logout starts, before its existing one-second delay.
Bind that delayed callback to its generation too:

```ts
const logoutStarted = React.useRef(false); // At hook scope.

const continuLogout = async () => {
  if (logoutStarted.current) return;
  logoutStarted.current = true;
  invalidateSession();
  const logoutEpoch = currentSessionEpoch();
  clearAllTimeout();
  dispacthIsOnLogout(true);
  setLoading(true);
  ButtonEvent("click", { name: "logout", ...analyticsData });
  ModalEvent("close", { name: "session control", ...analyticsData });
  await waitFor(1000); // Existing delay.
  if (logoutEpoch !== currentSessionEpoch()) return;
  logout(); // Existing helper clears local state synchronously.
  props.setOpen(false);
};
```

Keep normal `/extend` and `/relogin` responses in the same generation.
Do not clear refresh state on every `SET_TOKEN` action.

Import `CanceledError` from the installed Axios package.
Import the new helpers at their insertion points.
Both login boundaries matter. They reject requests started before login and requests started while login was pending.
The proposal preserves old access after a failed login attempt. It clears the previous refresh credential.

This synchronous registration covers current raw service consumers too.
Future asynchronous interceptors require ownership capture before the Axios call instead.
Current untagged synthetic test responses need realistic request metadata for ownership assertions.

### FIX-2: keep active access after refresh expiry

Replace only `reconcileExpiry` in the Home controller:

```ts
const reconcileExpiry = () => {
  const now = Date.now();
  if (accessExpiresAt <= now) {
    setShowTimeout(true);
    return;
  }
  if (refreshExpiresAt > 0 && refreshExpiresAt <= now &&
      !showTimeout && !store.isOnLogout) {
    void Promise.resolve(getRefreshToken()).catch(() => {
      // The current-session error handler reports request failures.
    });
  }
};
```

Keep the existing refresh-expiry timer. It now replaces refresh credentials through valid access.
This request must not call `/extend` or `/relogin` merely because refresh expired.
Deleting the timer alone leaves an expired refresh credential for later recovery.
Existing fixtures must return a usable replacement token, rather than the same expired token.

### FIX-3: wait for late credentials and actual renewal

First, expose current pending acquisition from `src/hooks/service/index.ts`.
Add `epoch: number` to the existing `refreshTokenRequest` record.
Capture `const epoch = currentSessionEpoch()` before starting acquisition.
Require the same epoch in its existing access-token deduplication condition.
Store that epoch with the promise and controller.

```ts
export const getPendingRefreshToken = (): Promise<void> | undefined => {
  const request = refreshTokenRequest;
  return request?.epoch === currentSessionEpoch() &&
    !request.controller.signal.aborted ? request.promise : undefined;
};
```

Remove the swallowing `.catch` from `getRefreshToken`. Keep controller-owned cleanup in `.finally`.
Add rejection handling to Home's existing fire-and-forget `requestRefresh` call too.
The new `reconcileExpiry` example already handles rejection.
The pending helper only reads existing work. It must not start acquisition after access expiry.

Return the actual relogin promise:

```ts
export const relogin = () => {
  signal.relogin?.abort();
  const controller = new AbortController();
  signal.relogin = controller;
  return service.post(getEndPoint("/auth/v2/sso/relogin"), {}, {
    signal: controller.signal,
  }).finally(() => {
    if (signal.relogin === controller) signal.relogin = undefined;
  });
};
```

Validate relogin access in `successHandler`, after the ownership guard and before existing authentication mutations:

```ts
if (response.config?.url?.includes("/auth/v2/sso/relogin")) {
  try {
    const token = response.headers?.["single-ui-authorization"] ??
      response.headers?.["Single-UI-Authorization"];
    const payload = typeof token === "string" ? getJWTPayload(token) : "";
    if (!payload || typeof payload.exp !== "number" ||
        !Number.isFinite(payload.exp * 1000) ||
        payload.exp * 1000 <= Date.now()) {
      throw new Error("Unusable access");
    }
  } catch {
    return errorHandler(new AxiosError(
      "Relogin did not return usable access", "ERR_BAD_RESPONSE", response.config
    ));
  }
}
```

Import `getJWTPayload`, `AxiosError`, and the existing `errorHandler` at this insertion point.
A decoding failure also rejects the promise. No authentication mutation must precede this validation.
Direct error routing resets global loading and reports the failure.
Throwing inside a fulfilled interceptor does not call its paired rejected interceptor.

Initialize Timeout's waiting state before its effects run:

```ts
const [pendingAtMount] = React.useState(() => getPendingRefreshToken());
const [waitingForRefresh, setWaitingForRefresh] = React.useState(
  Boolean(pendingAtMount)
);
React.useEffect(() => {
  let mounted = true;
  const settled = () => { if (mounted) setWaitingForRefresh(false); };
  pendingAtMount?.then(settled, settled);
  return () => { mounted = false; };
}, [pendingAtMount]);
```

Replace the mount-only logout decision with a reactive deadline effect:

```ts
const refreshExpiresAt = React.useMemo(() => {
  try {
    const payload = store.refreshToken ? getJWTPayload(store.refreshToken) : "";
    return payload && typeof payload.exp === "number" &&
      Number.isFinite(payload.exp * 1000) ? payload.exp * 1000 : 0;
  } catch { return 0; }
}, [store.refreshToken]);

const recoveryDeadline = refreshExpiresAt - 2000; // Existing margin.
React.useEffect(() => {
  clearAllTimeout();
  if (waitingForRefresh || loading || store.isOnLogout) return;
  const remaining = recoveryDeadline - Date.now();
  if (remaining <= 0) {
    void continuLogout();
    return;
  }
  timerPopup.current = setTimeout(() => void continuLogout(), remaining);
  return clearAllTimeout;
}, [recoveryDeadline, waitingForRefresh, loading, store.isOnLogout]);

const canExtend = !waitingForRefresh && !store.isOnLogout &&
  recoveryDeadline > Date.now();
```

Keep the existing modal-open analytics in a separate mount effect.
Use the rendered context after settlement. Do not check `getHooksBase().store` inside that promise callback.
The effect must not start automatic logout while acquisition or manual relogin is pending.
The existing network timeout bounds pending acquisition. No new business grace interval is proposed.

Update manual Extend:

```ts
const extend = async () => {
  if (loading || !canExtend || recoveryDeadline <= Date.now()) return;
  setLoading(true);
  clearAllTimeout();
  ButtonEvent("click", { name: "extend", ...analyticsData });
  try {
    await relogin();
    ModalEvent("close", { name: "session control", ...analyticsData });
    props.setOpen(false);
  } catch {
    // Keep the dialog open after retryable failure.
  } finally {
    setLoading(false);
  }
};
```

Return `canExtend` from the hook. Set `disabled={!canExtend}` on the Extend button only.
Waiting must not set `loading` to true. The user must still be able to select Logout.
Retain current invalid-token logout handling for current-session requests.
Transport or provider failures permit retry only while the credential remains usable.
These changes preserve the existing two-second cutoff margin. They do not establish its business authority.

### FIX-4: complete release evidence

No source snippet can establish the missing PROD facts.
Bind the implemented commit to its CI run, build identifier, immutable artifact digest, and target.
Retain effective access and refresh lifetimes, property origins, clock agreement, and deployed dependency versions.
Retain the applicable rollback artifact, smoke assertions, stop conditions, and responsible operators.
Use actual authorization evidence for deployment. Release intent does not supply missing technical evidence.

## Acceptance and verification

Use existing canonical definitions. This plan adds no duplicate test definitions or new passing claims.
Proposed source does not close any case.
The [documentation checks](evidence/minimal-blocker-fixes-20261023/validation.json) pass structure, links, and source preservation.
They do not compile or execute the snippets. Owner and review warnings remain open.

| Criterion or boundary | Planned check and assertion | Exact test revision | Execution environment and grant | Actual result |
| --- | --- | --- | --- | --- |
| Active access | [REVIEW-F01](06-test-cases.md#review-f01): access remains usable across refresh expiry; replacement refresh supports later recovery. | Future corrected assertions: unknown. Existing references remain in the canonical case. | Planned local browser; this request asks for snippets. | NOT_RUN |
| Session isolation | [REVIEW-F03A](06-test-cases.md#review-f03a), [REVIEW-F03B](06-test-cases.md#review-f03b), [control](06-test-cases.md#review-f03-control): reject old results in both orders. | Future corrected revision: unknown. | Planned local browser. | NOT_RUN |
| Late delivery | [Scheduled delivery](06-test-cases.md#review-delayed-scheduled), [hide delivery](06-test-cases.md#review-delayed-hide), [browser probe](06-test-cases.md#probe-delayed-refresh): late usable credentials enable manual recovery. | Future corrected revision: unknown. | Planned local browser. | NOT_RUN |
| Successful renewal | [AC-5](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L166), [AC-6](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L173): pending requests keep the dialog open; valid completion closes it. | Future corrected revision: unknown. | Planned local browser. | NOT_RUN |
| Failed renewal | [AC-7](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#L180): retry remains possible while usable credentials remain. | Future corrected revision: unknown. | Planned local browser. | NOT_RUN |
| Broader conformance | [Seven-criterion coverage assessment](10-release-confidence.md#execution-evidence): resolve all included failures or record actual scope dispositions. | No future implementation revision exists. | Required execution and review remain open. | NOT_RUN |

Implementation also needs regression coverage for synchronous dispatch, login-pending requests, explicit logout, malformed headers, and stale errors.
Define those cases canonically before implementation verification. They are additional boundaries, not completed test cases.
Keep the known-failure test marker until the corrected behavior passes its actual assertions.

## Recovery and completion

Rollback trigger: session interruption, stale state adoption, or failed recovery after rollout. Decision owner: unknown release owner.
Recovery action: restore the selected previous frontend artifact. Frontend rollback cannot restore sessions already ended.
Irreversible actions: none in this proposal. No deployment occurred.
Completion gate: reviewed implementation, passing scoped cases, resolved included criteria, and matching operational evidence.
Remaining limits: untested snippets, unknown PROD conditions, pending knowledge publication, and unchanged broader requirement gaps.

## Evidence and uncertainty

| Source ID | Locator | Exact revision | Hash | Owner, authority, and inspected scope |
| --- | --- | --- | --- | --- |
| SRC-session-minimal-request-20261023 | [Exact user input](evidence/minimal-blocker-fixes-20261023/user-request.txt) | This chat; 23 October 2026. | [Inventory](evidence/minimal-blocker-fixes-20261023/source-inventory.json). | User; asks for minimal correction examples. |
| SRC-session-minimal-source-20261023 | [Timeout design](evidence/minimal-blocker-fixes-20261023/timeout-recovery-design.json), [ownership design](evidence/minimal-blocker-fixes-20261023/stale-session-design.json), [source inventory](evidence/minimal-blocker-fixes-20261023/source-inventory.json). | MFE `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85`. | Individual SHA-256 values in the linked records. | unknown application owner; source facts and proposed design remain separate. |
| SRC-session-review-intent-v4 | [Candidate requirement](../../knowledge/candidates/requirements/REQ-active-session-renewal.md#acceptance-criteria). | Version 4; source revision and authority remain in its provenance. | `828d62209f11dd9bb9dee893ddc80e7e5d4dc6abd3c58170e902dab61bc587aa`. | User clarifications; candidate publication remains pending. |

Facts: current source contains the three runtime causes described in the release assessment.
Inferences: these targeted corrections should remove those causes. Execution must confirm that prediction.
Unresolved questions: actual PROD settings, artifact, operator ownership, and full requirement dispositions remain open.
No material business clarification changed. No knowledge record or frozen intake was revised.
The [integration review](evidence/minimal-blocker-fixes-20261023/ownership-integration-review.json) identified cancellation, error routing, and delayed-logout safeguards.
This proposal includes those safeguards. It does not claim their execution passed.

## Findings and actions

| Finding ID | Evidence | Consequence | Owner | Next action | State |
| --- | --- | --- | --- | --- | --- |
| [RC-01](10-release-confidence.md#rc-01-active-access-can-end) | [FIX-2](#fix-2-keep-active-access-after-refresh-expiry) | Refresh expiry can end valid access. | unknown application owner | Correct reconciliation and verify real replacement. | open |
| [RC-02](10-release-confidence.md#rc-02-stale-responses-can-clear-a-fresh-session) | [FIX-1](#fix-1-reject-responses-owned-by-an-ended-session) | Old responses can corrupt a fresh session. | unknown application owner | Guard success and errors; verify both delivery orders. | open |
| [RC-03](10-release-confidence.md#rc-03-required-delayed-recovery-remains-unmet) | [FIX-3](#fix-3-wait-for-late-credentials-and-actual-renewal) | Late delivery cannot complete required recovery. | unknown application owner | Wait for current acquisition and validated renewal. | open |
| [RC-04](10-release-confidence.md#rc-04-prod-artifact-and-operating-evidence-remain-incomplete) | [FIX-4](#fix-4-complete-release-evidence) | A positive PROD handoff remains unsupported. | unknown release owner | Bind actual release and recovery evidence. | open |
