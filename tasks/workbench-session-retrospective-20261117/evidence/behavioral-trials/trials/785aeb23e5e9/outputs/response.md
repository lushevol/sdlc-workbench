# Interrupted-work handoff

The [payment recovery draft](../tasks/recovery-draft.md) now preserves all three source predicates.
The immediate next action is `owner:settlement` answering KQ-12 about late-arrival retention duration.
The saved answer remains blank. Confidence is high for the bounded draft interpretation.
See [the source](../sources/settlement/recovery.md#L3-L7) and [living questions](../tasks/questions.md).

## Completed draft

A rejected payment can be retried using its original payment reference.
Repeating an accepted reference must not create a second payment.
Late-arrival retention duration remains unresolved, and the source provides no default.
These clauses remain proposed intent dated 10 November 2026.
Their actor, environment, and version are unspecified.
The fixture is synthetic.

## Reconciled checkpoint

The [saved progress claim](../tasks/progress.md) declares all four selected sources complete.
Current artifacts retain two pending identities.

| Selected identity | Current disposition | Evidence and consequence |
| --- | --- | --- |
| `portal/activity.md` | Accepted work retained. | Its receipt links the existing [Activity section](../knowledge/records/portal.md#L3-L5). |
| `context.md` | Accepted contextual disposition retained. | [The agenda](../sources/context.md#L3) adds no new intent. |
| `settlement/recovery.md` | Draft resumed. Canonical coverage pending. | [Recovery](../knowledge/records/settlement.md#L7-L8) still says no source was incorporated. |
| `access/grants.md` | Held canonical review remains pending. | [The denial clause](../sources/access/grants.md#L7) is absent from [Grants](../knowledge/records/access.md#L3-L5). |

The selected denominator remains four identities.
Four reviewed receipts are declared, with one output-linked source and one justified contextual source.
Two substantive, output-free receipts lack completed source-to-canonical accounting.
No accepted case was repeated.

## Lifecycle position

| Dimension | Current evidence |
| --- | --- |
| Source coverage | Partial. Two accepted identities remain supported. Two identities remain pending canonical coverage. |
| Canonical processing | Recovery draft advanced. Canonical records and processing receipts retain their original bytes. |
| Intent and governance | Recovery is proposed intent. KQ-12 remains unresolved. The responsible canonical reviewer is unknown. |
| Publication | Candidate status. Human approval remains absent in [selection.json](../selection.json). |
| Derived wiki | Selection declares fresh inputs. [The excerpt](../wiki/proposed.md#L3-L5) conflicts with current Portal and role intent. |
| Implementation and execution | Historical local fixture only. This continuation performs no business execution. |

The wiki claims exactly 15 seconds in production and a primary scalar role.
The [Portal candidate](../knowledge/records/portal.md#L3-L5) and [Access candidate](../knowledge/records/access.md#L3-L5) contain different intent.
Whole-workflow completion therefore remains unsupported.

## Remaining actions

| Action | Owner | Skill | Required input | Completion condition |
| --- | --- | --- | --- | --- |
| Answer existing KQ-12. | `owner:settlement` | `manage-knowledge-lifecycle` | Scoped retention policy answer. | Duration and authority are recorded in the existing question. |
| Review recovery and the held denial clause. | unknown | `ingest-knowledge` | Authorization for canonical work. The denial clause needs no new policy answer. | Every material clause has reviewed canonical coverage or a retained unresolved disposition. |

## Checks and worker settings

[The action log](actions.json) retains commands, file access, results, timings, and settings.
Initial SHA-256 verification matched all 24 fixture inputs and all five selected skill files.
Final local checks cover protected hashes, source-to-draft predicates, and link targets.
The ingestion harness is `NOT_RUN` because this continuation permits draft and handoff writes.
Business behavior is `NOT_VERIFIED`.

The checkpoint requests model `luna` and reasoning `max`.
Observed model, reasoning, client, and dispatch identity are `UNKNOWN`.
The checkpoint's observed dispatch is null.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not establish complete writing review.
```
