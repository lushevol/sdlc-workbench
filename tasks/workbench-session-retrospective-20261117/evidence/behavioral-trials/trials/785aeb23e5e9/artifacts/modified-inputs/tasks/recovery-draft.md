# Recovery draft

The saved payment recovery draft is resumed from [the checkpoint](checkpoint.json).
The source records proposed intent dated 10 November 2026.
Its actor, environment, and version are unspecified.

## Proposed recovery behavior

A rejected payment can be retried with its original payment reference.
Repeating an accepted reference must not create a second payment.
Late-arrival retention duration remains unresolved. The source supplies no default.
See [the payment recovery source](../sources/settlement/recovery.md#L3-L7).

| Predicate | Source | Draft disposition | Remaining limit |
| --- | --- | --- | --- |
| Retry a rejected payment with its original reference. | recovery.md, lines 5–5 | Preserved in Proposed recovery behavior. | Synthetic draft intent only. |
| Repeating an accepted reference must not create a second payment. | recovery.md, lines 6–6 | Preserved in Proposed recovery behavior. | Execution is unverified. |
| Late-arrival retention duration is unresolved, with no default. | recovery.md, lines 7–7 | Preserved as unresolved. | KQ-12 remains unanswered. |

The source SHA-256 is `7873d7ffc27ae5a9631fafa8c2a2e99618558082b4906a4699b716eb0e8e4db6`.
It matches the [selection](../selection.json) and evaluation input.
Confidence is high for this bounded source-to-draft interpretation.

## Saved work and remaining scope

The checkpoint accepts `portal/activity.md` and `context.md`.
Their accepted dispositions are retained.
This continuation reviews the unfinished recovery draft.

The [settlement candidate](../knowledge/records/settlement.md#L7-L8) still records no incorporated recovery source.
Its output-free receipt therefore leaves substantive recovery coverage pending.
The draft adds no canonical processing completion.

The checkpoint holds `access/grants.md` for canonical denial-clause review.
The [source](../sources/access/grants.md#L7) requires denial without a matching action grant.
The [access candidate](../knowledge/records/access.md#L3-L5) omits that clause.
Retaining this draft intent needs no additional human answer.
Canonical review remains outside the authorized write scope.

## Owner handoff

The immediate owner action is to answer KQ-12 in [the existing living questions](questions.md).
Owner `owner:settlement` must specify the late-arrival retention duration.
The completion condition is a scoped, sourced answer.
The current blank answer remains preserved.

Later canonical processing requires authorization for the affected records and existing lifecycle operations.
The responsible reviewer is unknown.
Use `ingest-knowledge` for clause accounting and `manage-knowledge-lifecycle` for the subsequent handoff.

## Resume authorization

The exact request is retained below, dated 17 November 2026.
Its source is [evaluation-input.json](../evaluation-input.json), field `prompt`.

> In /var/folders/3q/zc3tlwsj1p1_pskzk1j9r5100000gn/T/wb-evaluation-sft1jwcb/785aeb23e5e9, Continue the authorized unfinished draft from the saved checkpoint and record a handoff at outputs/response.md. You may edit only tasks/recovery-draft.md and outputs/. Keep canonical records, saved answers, receipts and wiki unchanged. The fixture is synthetic. Local file reading and the named output writes are authorized; network calls and business transitions are not. Use the selected skills from evaluation-input.json.

## Checks and limits

Local checks verify source hashes, protected input hashes, links, and draft predicates.
The ingestion harness is `NOT_RUN` under this draft-only scope.
Canonical publication remains candidate status without human approval.
Business behavior is `NOT_VERIFIED` by this synthetic continuation.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not establish complete writing review.
```
