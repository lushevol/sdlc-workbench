---
standard: ASD-STE100
automated_check: NOT_RUN
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Claude Code retained review output

**Read the Codex dispositions before using these external findings.**
Action: use [the reconciliation](claude-validation.md) to identify accepted findings and corrected claims.
Consequence: raw reviewer conclusions contain unsupported claims. Owner: Codex.

Tool: Claude Code 2.1.310. Configured model: `deepseek-v4-flash`.
The output below preserves the provider response. It establishes no execution, approval, or deployment result.

Original response: [adversarial-response.json](adversarial-response.json).

2. Its `expected.isLoading === false` is derived from **main's behavior**, not from an independent requirement. "FAILED" therefore records a divergence from main; it does not establish that the candidate violates a spec. The draft hedges this in its `intended` field ("business approval of a new policy is not claimed"), but the case status label overstates the result.

### 2.2 Reachability is unproven (QUALIFY F2)

The draft's trigger requires four conditions simultaneously: current session, exported shared client, loader enabled, cancellation with no replacement or later response. Within `mfe-base` I could not demonstrate that any caller produces that state:

- **Admin abort-and-replace** (`src/admin/{Tile,Category,ImportMap}/services/useServices.ts`): `if (ref.current) ref.current.abort(); ref.current = new AbortController(); await postService(...)`. The abort is always immediately followed by a replacement request on a loader-enabled endpoint, which sets `isLoading` true and eventually clears it. No unmount cleanup exists, so there is no "final" abort here.
- **`getRefreshToken`** (`src/hooks/service/index.ts`): aborts the prior controller only on the path that then posts `/auth/v2/sso/refreshtoken`; it early-returns before aborting when the refresh token still has >3h (`REFRESH_TOKEN_REUSE_WINDOW_MS`) or when it joins the pending promise. Replacement or no-op, never final.
- **`relogin`** (same file): aborts the prior controller, then posts `/auth/v2/sso/relogin`. Replacement follows.
- **`src/hooks/service/util/extend.ts:8–16`**: this is the one genuine abort-without-replacement, but `/api/auth/v2/sso/extend` is in the request handler's loader-suppression list, so it never set `isLoading` true and there is nothing to clear. Good catch by the candidate's design; it does not support DELIVERY-01.
- **`continuLogout`** (`src/components/Timeout/common/useController.ts`): aborts pending `getRefreshToken`/`relogin`, then waits ~1000ms before `logout()`. That is a real in-repo instance of a current-session cancellation **not** clearing the loader. Impact is bounded: the logout POST/GET are loader-enabled and clear loading when they settle. This is a candidate-introduced transient (≤1s) worth listing, not a blocker.

**External reachability is architecturally plausible but unevidenced.** `src/root.tsx:35` exports `* as Service from "./hooks/service"`, exposing `service`/`getService`/`postService` on the `@fm/base` SystemJS module, and the Axios client accepts `signal`. But: `webpack.config.js:42–52` has `name: "baseContainer"`, `remotes`, `shared`, and **no `exposes`**, and no consumer in this workspace imports `@fm/base` Service. The draft says "External consumer production frequency is unknown," which is honest; the P2 label is not tied to any evidence of one.

### 2.3 The proposed cleanup is unsafe (REJECT F3)

The core fact the draft misses is that `isLoading` is a **single global boolean with no per-request ownership and no counter**. The draft's wording "releases the loading state owned by that ended request" describes a model the store does not implement. Consequences:

- At cancellation time the client **cannot know** whether the cancellation is "final." The draft's trigger ("No replacement or other response follows") is a property of the future, not of the handler.
- Restoring a dispatch for cancellations reintroduces the base race: request A aborted while replacement B is in flight → A's rejection clears the loader while B is still running. That is precisely the base defect the candidate removes.
- The draft's own hedge ("preserve stale-session rejection") avoids cross-session damage, but does not fix the same-session race, and still cannot distinguish final from non-final cancellation.
- A correct fix needs a pending-request refcount, or a watchdog that clears a loader with no in-flight owner. It cannot be a dispatch inside the error handler. Regressing to main's behavior would restore a base defect (last-writer-wins loader) rather than fix a candidate one.

So: the `next_action` should be rejected as written even though F1 is true.

### 2.4 Priority calibration

- As a **behavior delta**, confirmed, HIGH confidence.
- As a **user-visible regression**, conditional: it becomes consequential only if an external (or future in-repo) consumer passes a `signal` on a loader-enabled endpoint and does not issue a replacement. The full-viewport overlay with no watchdog would make it severe *if* reached.
- **Recommendation: P3-conditional**, promoted to P2 only after (a) a real Axios abort reproduction and (b) an external consumer inventory. The draft's "HIGH for handler behavior; integration reproduction pending" confidence line is accurate; its P2 is not calibrated to the evidence.

Also correct F4: recovery is not limited to "an unrelated later response." The request handler's suppressed-URL branch and the logout POST/GET also clear loading; the accurate statement is "until a later loader-enabled request settles, a suppressed request is issued, or the route unmounts."

---

## 3. Supported conclusions

**C1 — "No additional actionable new runtime defect established…" → QUALIFY.**
The hedge ("limited evidence, not absence proof") is right, but "after inspected full branch and callers" overstates coverage: the caller inventory for the exported client covers this workspace only; deployed consumers are unknown. Also, two candidate issues below (M-1, M-2) were not covered by the inspected cases. Reword to "none confirmed by executed reproduction."

**C2 — Ownership guards / same-session rotation → ACCEPT.**
`src/hooks/service/util/succes.response.handler.ts` throws `CanceledError` for stale/aborted responses before any handler; the error handler early-returns for stale requests; the epoch is invalidated only by fresh login and `clearStorageWhenLogout` (`src/utils/common.ts`). `/extend` rotation reuses the epoch and re-stamps only on fresh login, so same-session ownership survives. Caveats: these guards also suppress loader/error handling (M-3), and `isStaleSessionRequest(undefined)` safety is unverified.

**C3 — Extend waits for validated relogin → ACCEPT (caveat).**
`extend` `await`s `relogin()`, closes only when mounted, epoch unchanged, and logout not started; catch swallows; finally resets flags under the same guards. Caveat: validation requires numeric `exp > iat` with `iat > 0`. The rest of the app merely tolerates missing `iat` (`dispacthUserLoginTime` only acts when both exist); the new path *rejects* the response via `errorHandler`. If the BFF's relogin token lacks `iat`, Extend fails closed and the deadline logout fires. That is a contract question, not a code defect — see C5/residual V6.

**C4 — Fresh login clears refresh credentials at request start and adoption → QUALIFY.**
Request-start clearing is unconditional in the `isFreshLogin` branch; response-adoption clearing is conditional on the same branch; `SET_TOKEN` no longer clears `refreshToken` (`src/hooks/reducer/root0.reducers.ts`), while `SET_REFRESH_TOKEN` exists and is handled (`src/hooks/reducer/root.reducers.ts`, `ActionType.ts:10`). So the invariant holds **only for URLs matching** `/\/auth\/v[23]\/sso\/login(?:[?#]|$)/`. It is not a general "any login clears" guarantee (M-4).

**C5 — "Follows the inspected BFF credential contract" → REJECT as stated.**
The client flow is verifiable: `reconcileExpiry` requests replacement when refresh is expired and access valid; `getRefreshToken` posts `{ singleUIAuthorization: store.token }` and reads `single-ui-refresh`. But no BFF source or contract artifact was in the supplied evidence, so "inspected BFF credential contract" is an assertion the review cannot support. Keep the client-side claim; move the server contract to residual validation.

---

## 4. Unresolved items

**U1 — Real Axios cancellation reproduction → ACCEPT; highest priority.** It is the single item that could convert DELIVERY-01 from QUALIFY to ACCEPT. Specify both abort shapes: pre-dispatch (`throwIfCancellationRequested` after request interceptors) and in-flight adapter abort; assert the rejection really carries `ERR_CANCELED` and `config.signal.aborted`.

**U2 — Six browser failures need main attribution → ACCEPT; not closeable now.** `ae8213f` is a prior baseline, not main. Note the three failing cases (E2E-01/02/03, continuous activity renewal) sit exactly in the Home scheduler area where M-1 lives — treat this as the leading hypothesis, not a coincidence. Browser services are currently refused/503, so this must wait.

**U3 — Full test execution and main-assertion compatibility → ACCEPT.** The added `sessionCompatibility.test.ts` covers DEL-09…DEL-13 (credentials, rotation, error reporting, invalidation, ignored URLs) but **not cancellation/loader**. I did not run it.

**U4 — No production artifact/config/rollback/ownership → ACCEPT.**

**U5 — Extra ACs have no business review → ACCEPT.**

**Addition:** browser execution is not merely pending — the readiness probes show the environment unavailable, so U2 cannot be closed in this session.

---

## 5. Missed / qualifying findings

**M-1 (highest value) — Home acquisition timer contradicts its own guard. QUALIFY, potentially consequential.**
In `src/pages/Home/common/useController.ts` (`scheduleAcquisition`/`requestRefresh`, ≈134–145):

- Timer delay = `accessExpiresAt − 25_000 − now`; `setTimeout` never fires early, so at fire time `accessExpiresAt − Date.now() ≤ 25_000`.
- `requestRefresh` requires `accessExpiresAt − Date.now() >= 25_000` **whenever `refreshExpiresAt` is truthy**.
- Therefore, with an existing refresh token, the scheduled callback is a no-op except on exact-boundary firing (rare).
- The mount path calls `requestRefresh` only when `!refreshExpiresAt`, so it does not compensate.

Whether another path (visibility handler calling `requestRefresh` directly, `reconcileExpiry`) covers this, and whether `getRefreshToken`'s >3h early-return makes the call moot by design, requires a fake-timer test. This is the most plausible new functional regression I found, and it aligns with the three failing renewal E2E cases.

**M-2 — `signal.aborted` is broader than "cancellation." QUALIFY (low).**
`error.config?.signal?.aborted` can be true when the adapter rejects with a *real* error (e.g., a 401 `TOKEN_INVALID_EXPIRED` racing an abort). Candidate then skips errorMsg, invalidation, and loading clear; base processed them. Narrow race, but a genuine semantic broadening.

**M-3 — Success-path stale throw bypasses same-pair rejection handling. ACCEPT as intent; note.**
`throw new CanceledError("Discarded an ended session response", …)` in `succes.response.handler.ts` goes to the next interceptor/caller, not to `errorHandler`, so stale responses never clear loading or run error typing. Deliberate, but combined with no watchdog it means a stuck loader cannot self-heal.

**M-4 — Refresh clearing is URL-regex-dependent. QUALIFY (intent gap).**
With `SET_TOKEN` no longer clearing `refreshToken`, the only clearing gates are the regex-matched login request/response branches. Any `SET_TOKEN` dispatch outside that URL shape (SSO callback, version drift, header-based flow with a different request URL) carries the prior refresh token across sessions. Audit all `SET_TOKEN` dispatch sites.

**M-5 — `CLEAR` does not reset `isLoading`. Base defect; residual risk.**
Masked today because logout's own requests clear it, but it matters for any future cancellation-aware cleanup design.

**M-6 — Global boolean, no refcount/watchdog. Root-cause correction.**
This is why the draft's "owned by that ended request" language is wrong, and why both main and the proposed cleanup are racy.

**M-7 — Wording.** "Unrelated later response" understates recovery (suppressed-URL request branch, logout requests, route unmount). Verify the suppressed-URL dispatch before quoting it.

---

## 6. Residual validation (specific)

1. **Real Axios abort** through the exported client (`Service.getService(url, { signal })` or `service.get`), real `config.ts` interceptors, loader-enabled URL (e.g., `/api/auth/v1/fmo/admin/category/data`), no replacement. Assert `store.isLoading` and DOM `PageLoader` on both refs.
2. **Cancel-and-replace**: A aborted, B in flight, same session. Assert loader stays true until B settles. Expected: candidate correct, main leaks early. This is the test that proves the proposed cleanup is wrong.
3. **New-session isolation**: A in flight → login (epoch bump) → A rejects. Assert no errorMsg, no invalidation, no loader corruption of the new session.
4. **External consumer inventory**: grep all workspace repos, import maps, and deployment manifests for `@fm/base`, `Service.getService`, `postService`, and `base.js`; confirm whether any deployed consumer passes `signal` and relies on mfe-base's global store.
5. **Home scheduler**: fake timers; access expiry T, refresh token present; advance to T−25s and T−20s; toggle hidden→visible; spy `getRefreshToken`. Run the same T−25s case with no refresh token.
6. **BFF contract**: capture relogin/refresh responses; assert relogin access token has numeric `iat` and `exp > iat`; assert `single-ui-refresh` header on refresh; assert `singleUIAuthorization` accepted.
7. **Abort-vs-error race**: abort the signal immediately after the adapter rejects with 401 `TOKEN_INVALID_EXPIRED`; assert invalidation still occurs.
8. **Null-safety**: `isStaleSessionRequest(undefined)` and requests issued before the interceptor stamps `sessionEpoch`.
9. **Main attribution**: run the 22-case browser queue against a `f025513` artifact (not `ae8213f`) once services are available.

---

## 7. Bottom line

- **DELIVERY-01**: the handler delta is **confirmed**; the P2 framing is **not**. Downgrade to P3-conditional until a real abort reproduction and an external-consumer inventory exist. **Reject** the proposed cleanup: the loader has no ownership model, so "final cancellation" is not observable there; the correct remedy is a refcount or watchdog, and the draft's dispatch would restore main's cancel-and-replace race.
- **C5** is the clearest overclaim: a BFF contract was asserted, not inspected.
- **C4** holds only for regex-matched login URLs; **C1** overstates caller coverage.
- **No other confirmed consequential new regression** was found. The strongest missed candidate is **M-1** (Home timer boundary vs its own `>= 25_000` guard), which lines up with the three failing continuous-renewal E2E cases and deserves priority once execution is possible.
- **Unavailable execution** is the binding constraint: no current browser environment (ports refused/503), no test execution performed by me, and the DEL-14 harness proves handler behavior only.
