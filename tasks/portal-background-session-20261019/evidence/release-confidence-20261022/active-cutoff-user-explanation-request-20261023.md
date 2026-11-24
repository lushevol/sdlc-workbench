# Active cutoff user explanation request

**Explain the user journey that reaches active cutoff.**
Action: connect the existing reproduction to user activity.
Consequence: the user needs this explanation to judge the release issue.
Owner: Codex. Evidence: the exact user input below.

Source: User message in this Codex chat, 2026-10-23, Asia/Singapore.

Exact user input:

> no.1 is a valid issue right? describe how user will got this issue

Scope: Explain existing issue 1. Do not change business policy or application code.

## Explanation basis

Candidate: `6e34da31961eb6bce4ef6c3daea83a2f7bd48e85`.
Baseline: `f025513f696476a9cc8162681410cbd21e029bcb`.

| Claim | Class | Evidence and limit |
| --- | --- | --- |
| C1: Active access can be cleared at the original refresh deadline. | Observed execution | [Candidate result](../code-review-refresh-20261021/lifecycle-candidate-active_cutoff/actual.json) records 23 extensions, valid access, and one logout. [Baseline result](../code-review-refresh-20261021/lifecycle-baseline-active_cutoff/actual.json) records zero logouts. The clock and responses were controlled. |
| C2: Repeated activity can postpone refresh acquisition while retaining the original refresh. | Inspected implementation | [Home activity and scheduling](../../../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L60-L173) reset acquisition around the extended access deadline. [Access updates](../../../../repos/ui/mfe-base/src/hooks/reducer/root0.reducers.ts#L6-L9) retain refresh. |
| C3: An earlier hide transition can supply the initial refresh before foreground activity continues. | Inference from inspected implementation | [Hidden-page handling](../../../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L126-L167) calls acquisition with valid access and no refresh. [Acquisition](../../../../repos/ui/mfe-base/src/hooks/service/index.ts#L37-L71) sends the request. This full user journey was not newly executed. |
| C4: The frontend ends the session when refresh expires, despite valid access. | Inspected implementation | [Expiry reconciliation](../../../../repos/ui/mfe-base/src/pages/Home/common/useController.ts#L118-L173) opens Timeout. [Timeout](../../../../repos/ui/mfe-base/src/components/Timeout/common/useController.ts#L25-L51) starts logout. |

## User journey

1. The user already has a refresh token, such as from an earlier successful acquisition during a tab switch.
2. The user returns before access expiry and keeps the portal visible.
3. The user moves the mouse periodically and leaves five quiet seconds for each access extension.
4. Successful extensions keep access valid beyond the original refresh deadline.
5. No replacement refresh arrives before that deadline.
6. The frontend opens Timeout at refresh expiry and starts automatic logout.
7. The retained controlled result shows Sign in after the one-second logout delay.

The [canonical case](../../06-test-cases.md#review-f01) remains the only definition of the reproduced assertions.
The [prior source check](blocker-reproduction-review.json) records source hashes and retained execution limits.
Four hours and fifteen minutes are fixture lifetimes. Effective PROD lifetimes and occurrence frequency remain unknown.
Owner: unknown application owner. Next action: correct active cutoff and repeat the canonical comparison.
No application edit, business policy change, or new business execution occurred.
Automated checks passed for ten source hashes, links, source ranges, and exact user input.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not check the complete approved dictionary or grammar rules.
```
