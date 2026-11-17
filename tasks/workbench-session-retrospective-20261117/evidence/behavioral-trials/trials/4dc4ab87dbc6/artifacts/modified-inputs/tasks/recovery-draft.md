# Recovery draft

## Resumed draft

The saved checkpoint identifies this draft as unfinished.
KQ-10 authorizes continuing payment recovery while retaining accepted work.
See the [checkpoint](checkpoint.json) and [saved answer](questions.md).

The source records draft target behavior dated 10 November 2026.
The following clauses retain that draft status. [Payment recovery](../sources/settlement/recovery.md#L3)

## Draft target behavior

- A rejected payment can be retried with its original payment reference. [Source](../sources/settlement/recovery.md#L5)
- Repeating an accepted reference must not create a second payment. [Source](../sources/settlement/recovery.md#L6)
- Late-arrival retention duration remains unresolved. The source supplies no default. [Source](../sources/settlement/recovery.md#L7)

## Remaining decision

KQ-12 asks how long late arrivals must be retained.
Its saved answer remains blank.
The responsible owner is `owner:settlement`. [Living questions](questions.md)

The owner must supply the retention duration and applicable conditions.
This unresolved duration does not prevent retaining the supported retry and duplicate clauses as draft intent.

## Resume point

Source review for these recovery clauses is complete.
Canonical recovery incorporation remains pending.
The current settlement candidate states that no recovery source has been incorporated. [Settlement candidate](../knowledge/records/settlement.md#recovery)

Continue from this draft when canonical editing is authorized.
Preserve the accepted Portal and context work recorded in the checkpoint.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not establish complete writing review.
```
