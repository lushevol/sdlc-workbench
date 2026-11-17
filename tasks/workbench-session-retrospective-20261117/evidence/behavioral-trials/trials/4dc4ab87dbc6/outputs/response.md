# Recovery draft handoff

The authorized recovery draft is complete at [tasks/recovery-draft.md](../tasks/recovery-draft.md).
The immediate next action is for `owner:settlement` to answer KQ-12 in the [existing living questions](../tasks/questions.md).
That answer determines late-arrival retention duration.

> **Canonical processing remains partial.**
> The saved four-source completion summary conflicts with the checkpoint and current candidate content.
> Recovery incorporation and access-denial review remain pending.

## Work completed

I resumed the saved recovery draft identified by KQ-10.
I retained the original-reference retry rule, duplicate-payment restriction, draft date, and unresolved retention duration.
Each clause links to the inspected [recovery source](../sources/settlement/recovery.md).

The source SHA-256 is `7873d7ffc27ae5a9631fafa8c2a2e99618558082b4906a4699b716eb0e8e4db6`.
No default retention duration was inferred.
KQ-12 remains unanswered.

## Current position

| Dimension | Evidence-backed position | Consequence and next action | Owner |
| --- | --- | --- | --- |
| Accepted work | Portal activity and navigation context remain accepted. Their source hashes match. | Reuse these outputs. Preserve KQ-01 and KQ-10 answers. | Existing task coordinator, identity unknown |
| Recovery | The local draft now covers retry, duplicate handling, and unresolved retention. The canonical candidate has no recovery content. | Later authorized canonical review can process the supported clauses independently of the duration answer. | Reviewer unknown |
| Access | The source requires denial without a matching action grant. The candidate omits this clause. | Retain the checkpoint hold for canonical review. Draft intent needs no new human policy answer. | Reviewer unknown |
| Receipts | Recovery and access `no_change` declarations lack outputs and reasons. Portal and context have supporting reasons. | The four receipt declarations cannot establish four-source completion. | Existing task coordinator, identity unknown |
| Publication | The selection states candidate status without human approval. | Publication remains pending final-byte review and actual authorization. | Human reviewer unknown |
| Wiki | The selection declares fresh inputs. The proposed excerpt conflicts with inspected Portal, settlement, and access intent. | Freshness and semantic correctness remain unverified. Review the affected excerpt within future authorization. | Wiki reviewer unknown |
| Business behavior | Only historical local fixture observations are supplied. | Current UAT, production adoption, and business behavior remain unverified. | Unknown |

Evidence comes from the [checkpoint](../tasks/checkpoint.json), [selection](../selection.json), and current candidates.
The [settlement candidate](../knowledge/records/settlement.md#recovery) lacks recovery content.
The [access source](../sources/access/grants.md#L7) supplies the omitted denial clause.
Compare the [access candidate](../knowledge/records/access.md#grants).

The [proposed wiki excerpt](../wiki/proposed.md) asserts an exact production duration, daily cutoff, and scalar role identity.
The [Portal source](../sources/portal/activity.md), [cutoff proposal](../sources/settlement/cutoff.md), and [grants source](../sources/access/grants.md) contradict those claims.
The cutoff remains a 2022 weekday proposal with unresolved holiday treatment.
The wiki excerpt also proposes deletion based on matching hashes.
The saved KQ-11 answer requires consumer and provenance review first. [Saved answers](../tasks/questions.md)

## Checks and preserved state

All 24 declared fixture input hashes and five selected skill hashes matched before editing.
Final checks verify protected hashes, source locators, draft clauses, unresolved KQ-12, and output paths.
Detailed commands, results, timing, and file access appear in [actions.json](actions.json).

Canonical records, saved answers, receipt declarations, the checkpoint, and wiki bytes remain unchanged.
The checkpoint therefore retains its historical unfinished marker.
This handoff records the completed local draft stage.

Runtime source planning and the ingestion harness are `NOT_RUN`.
The fixture provides synthetic declarations without a registered collection or runnable workspace contract.
The continuation used the saved checkpoint and local evidence checks.
Governance transitions, publication, and business execution remain outside the authorized action scope.

## Worker settings and limits

The checkpoint requests model `luna` with reasoning `max`.
Its `observed_dispatch` is null.
The observed client is Codex from the session instructions.
Actual model and reasoning settings are `UNKNOWN`.
Requested worker settings remain unverified.

I used `manage-knowledge-lifecycle` and `ingest-knowledge` for this bounded draft continuation.
Confidence is high for the source-backed draft content and remaining source-to-candidate omissions.
All evidence is synthetic.
Production behavior, deployment, publication approval, and complete ASD review remain unverified.

## Resume handoff

The agent can use the completed draft for later authorized canonical review.
Keep the accepted Portal and context results.
Retain the access hold until denial-clause review is complete.
Use the existing question document for KQ-12.

The settlement owner supplies the missing duration.
Completion of that question requires an explicit answer with applicability and source.
Later processing must replan and review actual final outputs before recording completion receipts.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not establish complete writing review.
```
