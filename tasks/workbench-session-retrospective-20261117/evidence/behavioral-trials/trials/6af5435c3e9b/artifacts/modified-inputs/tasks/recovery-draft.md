# Recovery draft

The saved recovery draft now contains all three source predicates. Canonical incorporation remains pending.

## Recovery intent

The source records draft target behavior dated 10 November 2026.

- A rejected payment can be retried with its original payment reference.
- Repeating an accepted reference must not create a second payment.
- Late-arrival retention duration remains unresolved. The source supplies no default.

These statements support reader question Q-04 within the source's draft scope. [Recovery source](../sources/settlement/recovery.md#L3-L7)

Source SHA-256 `7873d7ffc27ae5a9631fafa8c2a2e99618558082b4906a4699b716eb0e8e4db6` matches the selected input.

## Predicate accounting

| Source predicate | Draft destination | Canonical disposition | Remaining action |
| --- | --- | --- | --- |
| Recovery L5, retry with original reference | Recovery intent, first bullet | Pending incorporation | Maintainer reviews the sourced draft during authorized canonical work. |
| Recovery L6, accepted-reference duplicate prevention | Recovery intent, second bullet | Pending incorporation | Maintainer reviews the sourced draft during authorized canonical work. |
| Recovery L7, unresolved late-arrival duration | Recovery intent, third bullet | Unresolved | owner:settlement answers saved KQ-12. |

The settlement candidate states that recovery sources have yet to be incorporated. [Settlement candidate](../knowledge/records/settlement.md#L7-L8)

Reader draft A supplies seven days. The retained recovery source supplies an unresolved duration. Draft B preserves that uncertainty. [Draft A](../drafts/answer-a.md), [draft B](../drafts/answer-b.md), [recovery source](../sources/settlement/recovery.md#L7)

## Saved answers and resumption

KQ-10 directs continuation of this payment recovery draft and retention of accepted work.
KQ-12 remains unanswered for the operator, UAT, v1, late-arrival scope.
Owner `owner:settlement` must supply the duration and its applicability. [Living questions](questions.md#L16-L18)

The accepted identities are `portal/activity.md` and `context.md`. Their saved completion was reused with hash checks.
The held identity is `access/grants.md`. Its denial clause awaits canonical review. [Checkpoint](checkpoint.json#L3-L11)

## Original checkpoint note

> A rejected payment can be retried. Original-reference, duplicate, and unresolved late-arrival details still need source review.

## Check status

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not establish complete writing review.
  - Synthetic source statements establish draft intent only.
```

## Continuation request

Source `evaluation-input.json`, recorded 2026-11-17T12:31:59.495768+00:00.

> In /var/folders/3q/zc3tlwsj1p1_pskzk1j9r5100000gn/T/wb-evaluation-sft1jwcb/6af5435c3e9b, Continue the authorized unfinished draft from the saved checkpoint and record a handoff at outputs/response.md. You may edit only tasks/recovery-draft.md and outputs/. Keep canonical records, saved answers, receipts and wiki unchanged. The fixture is synthetic. Local file reading and the named output writes are authorized; network calls and business transitions are not. Use the selected skills from evaluation-input.json.
