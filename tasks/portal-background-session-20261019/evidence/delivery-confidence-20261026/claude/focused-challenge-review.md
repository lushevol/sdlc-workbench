---
standard: ASD-STE100
automated_check: NOT_RUN
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
---

# Claude Code focused challenge

**Use the Codex dispositions before accepting these reviewer claims.**
Action: read [the reconciliation](claude-validation.md). Owner: Codex.
Consequence: the timer comparison needed a stronger initial-state binding.
Original response: [focused-challenge-response.json](focused-challenge-response.json).
Tool: Claude Code 2.1.310. Configured model: `deepseek-v4-flash`.

## Adversarial review

No execution is claimed. I rely solely on the supplied source and artifacts.

### DELIVERY-01 — ACCEPT (evidence-scoped)

**Mechanism.** Main's `errorHandler` reaches the unconditional `SET_IS_LOADING false` at base:40 even for `ERR_CANCELED`. Candidate base:8–14 early-returns before `getHooksBase()`, so no dispatch occurs. The browser artifact is exact and differential: main `after.isLoading=false`, `loaderVisible=false`; candidate `true`/`true`; both reject `ERR_CANCELED` with token/error unchanged. Trigger wording is precise: final cancellation with no replacement. Supported.

**Counterevidence and overclaim checks.**
- The fixture proves a **supported public-client contract**, not deployed frequency. `service` and `getService` are exported and accept `AxiosRequestConfig.signal`, but the artifact's own limit calls it a "diagnostic cancellation route." In-app callers (`getRefreshToken`, `relogin`) abort-and-replace, so the replacement sets loading true and later clears it; the persistent-loader state requires an external caller or a final abort with no replacement.
- "Routing keeps PageLoader visible until an unrelated later response clears it" is an inference. The supplied fixture ends with no later request; no success-response handler source is supplied. The candidate artifact proves the loader is visible after final cancellation, not the clearing behavior of an unrelated response.
- The cited `unit/candidate-final-with-overlap/execution.json` is aggregate only: 456 tests, 455 passed, 1 failed, no per-case identity. It neither corroborates DEL-14 nor attributes the failing test. DEL-14's weight rests on `browser/supplemental-comparison.json`.
- Candidate base:11 also suppresses clearing for **any** caller-aborted request (`error.config?.signal?.aborted`), not only `ERR_CANCELED`. That widens the trigger family, while the consequence is the same.
- The BROWSER-SHARING-PENDING failure is inherited by both refs and is correctly excluded from this finding.

**Remedy safety.** The stated `next_action` is directionally safe only as written: track current-session pending loading work, clear on final settlement, preserve stale-session isolation, and require DEL-19. Restoring main's unconditional clear, or using a bare counter that decrements on a late abort, reintroduces the prior defect—hiding a replacement request that is still pending. Note that `intended`'s phrase "preserves main behavior" conflicts with the ownership requirement; the action, not the phrase, should govern. Preserve `isStaleSessionRequest` first.

**Residual limits.** No production caller frequency, owner, or impact duration; no supplier of the success-response path; headless Edge; no native visibility/device evidence.

### DELIVERY-02 — QUALIFY

**Mechanism is source-supported, consequence is not general.** Candidate base:134–144 schedules at `accessExpiresAt - 25000 - Date.now()` with `delay > 0`, but `requestRefresh` rechecks `accessExpiresAt - Date.now() >= 25000`. Any callback lateness ≥1 ms yields 24999 ms and suppresses acquisition. That boundary fragility is real in the supplied source, and 1 ms is a minimal displacement. However, the artifacts use controlled clocks and immediate adapter responses; natural timer jitter is not measured.

**Concrete counterevidence to the forced-logout framing.** Suppression does not by itself force logout:
- If refresh expiry is well after access expiry, the Timeout modal mounts with `recoveryDeadline` in the future (candidate Timeout base:76–108), `canExtend` remains true, there are no logout requests; only automatic acquisition is lost, with manual Extend still available.
- If refresh expiry is **before** access expiry, candidate's `refreshExpiryTimer` fires while access is valid and `reconcileExpiry` calls `getRefreshToken` (candidate Home base:124–132), recovering.
- Forced logout requires refresh expiry equal to or within roughly 2 s after access expiry, because `recoveryDeadline = refreshExpiresAt - 2000`. The supplied fixture constructs exact equality; it does not measure frequency.

**Reachability claim is the weakest point.** "Equal expiry is reachable after repeated access rotation relative to an older refresh credential" is unsupported by the supplied source and appears backwards: an older refresh expires before access and falls into the reconcile-recovery branch, not the failing branch. No supplied artifact shows natural equal expiry.

**Comparison validity.** The two observation files do not record a common initial credential state. At the same `preExpiry` timestamp (`...835001`), main shows a refresh token expiring at `...987200` (about 4 h, subject `replacement-refresh`), while candidate shows one expiring at `...860000` (about 60 s, subject `nearly-expired-refresh`). Main's artifact therefore does not itself demonstrate an equal-expiry start. If main began with 4 h remaining, its non-logout could be credential state rather than successful acquisition. Also, "main can recover" means manual Extend, not automatic recovery.

**Remedy safety.** Do not loosen the guard globally. A tolerance can issue a refresh after access expiry or re-enable acquisition on hidden→visible resume, defeating the no-late-replay intent. The fix should distinguish timer-origin eligibility from the visibility cutoff, permit bounded lateness only for the scheduled callback, retain hidden/resume behavior, retain in-flight deduplication, and preserve the refresh-before-access reconcile branch.

**Residual limits.** Synthetic clocks, a single 1 ms displacement, no jitter distribution, no production frequency or owner, and only the two observation JSONs as assertion evidence.

**Overall.** DEL-01 is supported for the public-client final-cancellation fixture, not production frequency. DEL-02's off-by-one guard is supported; the equal-expiry forced-logout consequence and its stated reachability are qualified, and the main/candidate observations lack a demonstrated common starting state. No test execution is claimed.
