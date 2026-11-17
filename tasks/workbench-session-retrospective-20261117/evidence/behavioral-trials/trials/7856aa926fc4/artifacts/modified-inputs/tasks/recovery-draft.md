# Recovery draft

Resumed from the saved checkpoint on 17 November 2026.
This draft preserves the source's draft target behavior from 10 November 2026.
KQ-10 directs continuation of this draft and retention of accepted work. [Saved answer](questions.md)

## Proposed recovery behavior

A rejected payment can be retried with its original payment reference.
Repeating an accepted reference must not create a second payment.
Late-arrival retention duration remains unresolved.
The source supplies no default duration. [Recovery source](../sources/settlement/recovery.md#L3-L7)

## Source-to-draft accounting

| Source predicate | Source lines | Draft destination | Disposition |
| --- | --- | --- | --- |
| Retry uses the original payment reference. | 5 | Proposed recovery behavior, first sentence | Preserved |
| Repeating an accepted reference creates no second payment. | 6 | Proposed recovery behavior, second sentence | Preserved |
| Retention duration remains unresolved, with no default. | 7 | Proposed recovery behavior, final two sentences | Unresolved and visible |

The source SHA-256 is `7873d7ffc27ae5a9631fafa8c2a2e99618558082b4906a4699b716eb0e8e4db6`.

## Remaining decision and handoff

KQ-12 remains unanswered in the living questions.
Owner `owner:settlement` must provide the late-arrival retention duration.
The seven-day statement in reader draft A lacks support from this source.
This draft supplies the supported Q-04 answer. [Living questions](questions.md) [Reader draft A](../drafts/answer-a.md)

Canonical incorporation requires separately authorized ingestion.
The current settlement candidate still states that recovery has no incorporated source. [Settlement candidate](../knowledge/records/settlement.md#recovery)

## Writing review

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks cover hashes, links, and required draft text.
  - Automated checks do not establish complete writing review.
```
