# Refresh expiry timer question

**Confirm the timer callback and sign-out sequence.**
Action: trace the quoted timer through Timeout handling.
Consequence: this trace identifies the active-session logout trigger.
Owner: Codex. Evidence: the exact user input below.

Source: User message in this Codex chat, 2026-10-23, Asia/Singapore.

Exact user input:

> is this code finally triggered timeout dialog and sign out ?
>
>     const refreshExpiryTimer = refreshExpiresAt
>       ? setTimeout(reconcileExpiry, Math.max(0, refreshExpiresAt - Date.now()))
>       : undefined;

## Confirmed chain

Candidate: `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85`.
Class: inspected implementation. The [retained result](../code-review-refresh-20261021/lifecycle-candidate-active_cutoff/actual.json) separately records controlled execution.

1. [The timer](../../../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L171-L173) schedules expiry reconciliation at the refresh deadline.
2. [Reconciliation](../../../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L118-L123) opens Timeout when either credential expires.
3. [Home](../../../../repos/ui/mfe-base/src/pages/Home/index.tsx#L127) mounts Timeout.
4. [Timeout](../../../../repos/ui/mfe-base/src/components/Timeout/common/useController.ts#L25-L51) starts automatic logout because its refresh deadline has passed.
5. After an intentional one-second wait, [logout](../../../../repos/ui/mfe-base/src/services/index.ts#L20-L30) clears local credentials.

Valid access does not prevent this refresh-expiry branch.
A replacement refresh can cancel the previous timer. Browser scheduling can delay execution.
Returning to the foreground also calls [reconciliation](../../../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L150-L159).
The refresh-expiry condition therefore remains relevant if the standalone timer is removed.
Owner: unknown application owner. Next action: correct expiry handling and repeat [REVIEW-F01](../../06-test-cases.md#review-f01).
No code edit, policy change, or new business execution occurred.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```

## Source identity checks

Automated checks passed for source identity, local links, source ranges, and exact quoted input.

```json
{
  "src/pages/Home/common/useController.ts": "1b500b9f6ad3ad755a98a4cd912613baf737a4ff97a048e0d7abd773d3dacfbb",
  "src/pages/Home/index.tsx": "9b574c0779c3b48514b0068c39ff4ea800255bea9e800dfdd247badbf6f087de",
  "src/components/Timeout/common/useController.ts": "d1e40e3d9c804870b33c239908024e3faab9c2e185cad3b1866a950cd0976bb8",
  "src/services/index.ts": "dd7a772b8b6f69266bd6d7e498635268920c749036548d5f2858252d011ed118"
}
```
