# Recovery draft

> The recovery clauses are drafted for review. Late-arrival retention duration remains unresolved.

The immediate next action is settlement-owner review of this draft and the existing KQ-12 question.

## Request and checkpoint

The saved checkpoint identifies this draft as unfinished. Its accepted inputs are `portal/activity.md` and `context.md`.
The saved KQ-10 answer directs continuation of the payment recovery draft. [Checkpoint](checkpoint.json) [Saved answer](questions.md#L16)

The request was supplied through `evaluation-input.json` on 17 November 2026.

> In /var/folders/3q/zc3tlwsj1p1_pskzk1j9r5100000gn/T/wb-evaluation-sft1jwcb/4bf5c2853d92, Continue the authorized unfinished draft from the saved checkpoint and record a handoff at outputs/response.md. You may edit only tasks/recovery-draft.md and outputs/. Keep canonical records, saved answers, receipts and wiki unchanged. The fixture is synthetic. Local file reading and the named output writes are authorized; network calls and business transitions are not. Use the selected skills from evaluation-input.json.

## Proposed recovery behavior

The source describes draft target behavior dated 10 November 2026. [Source status](../sources/settlement/recovery.md#L3)

| Claim | Draft wording | Evidence |
| --- | --- | --- |
| REC-1 | A rejected payment can be retried with its original payment reference. | [Recovery source, line 5](../sources/settlement/recovery.md#L5) |
| REC-2 | Repeating an accepted reference must not create a second payment. | [Recovery source, line 6](../sources/settlement/recovery.md#L6) |
| REC-3 | Late-arrival retention duration remains unresolved. The source provides no default. | [Recovery source, line 7](../sources/settlement/recovery.md#L7) |

The source SHA-256 is `7873d7ffc27ae5a9631fafa8c2a2e99618558082b4906a4699b716eb0e8e4db6`.
Confidence is high for alignment with these supplied source clauses.
The synthetic fixture provides documentary support only. Business behavior remains `NOT_VERIFIED`.

## Open decision

KQ-12 asks how long late arrivals must be retained. Its answer remains blank.
The recorded owner is `owner:settlement`. The unresolved duration permits drafting REC-1 and REC-2. [Existing KQ-12](questions.md#L18)

The owner must supply the duration before the retention rule can become complete.

## Resume boundaries and handoff

The checkpoint retains `access/grants.md` as held for canonical review of its denial clause.
Its recorded reason says retaining draft intent requires no human answer. [Held scope](checkpoint.json)

The saved summary overstates completion. Its recovery receipt declares `no_change` with an empty output list.
The settlement candidate states that recovery incorporation remains pending. [Selection declaration](../selection.json) [Settlement recovery](../knowledge/records/settlement.md#L8)

A later authorized canonical pass must reconcile these clauses and the unsupported completion declaration.
Use `ingest-knowledge` and its existing review, sealing, and completion workflow.
Use `manage-knowledge-lifecycle` to reassess the remaining held scope and handoff.
The review owner for that canonical pass is `unknown`.

The worker request specifies `luna` with `max` reasoning. The saved observed dispatch is `null`.
Observed runtime model, reasoning, and client are `UNKNOWN`. [Worker checkpoint](checkpoint.json)

## Checks and writing review

Manual source-clause review covered recovery lines 3–7 and the settlement recovery section.
Local automated checks cover input hashes, protected-file preservation, output links, and required draft clauses.
Runtime planning, sealed ingestion checks, wiki verification, and business execution are `NOT_RUN`.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not establish complete writing review.
  - Synthetic inputs do not establish business behavior.
```
