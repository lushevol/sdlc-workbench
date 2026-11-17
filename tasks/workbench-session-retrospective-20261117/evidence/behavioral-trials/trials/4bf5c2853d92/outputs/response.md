# Recovery draft handoff

The authorized recovery draft is resumed at [tasks/recovery-draft.md](../tasks/recovery-draft.md).
The immediate next action is `owner:settlement` review and a retention-duration answer in existing KQ-12. [Saved question](../tasks/questions.md#L18)

## Completed draft scope

- Rejected payments can be retried with their original payment reference. [Recovery source](../sources/settlement/recovery.md#L5)
- Repeating an accepted reference must not create a second payment. [Recovery source](../sources/settlement/recovery.md#L6)
- Late-arrival retention remains unresolved, without a supplied default. [Recovery source](../sources/settlement/recovery.md#L7)

These clauses retain the source's draft status and 10 November 2026 date.
Confidence is high for documentary alignment within the synthetic fixture. Business behavior remains `NOT_VERIFIED`. [Source status](../sources/settlement/recovery.md#L3)

## Checkpoint and remaining work

| Dimension | Current evidence and next action | Owner |
| --- | --- | --- |
| Accepted work | Reused checkpoint acceptance for `portal/activity.md` and `context.md`. Content re-extraction was unnecessary. | unknown |
| Recovery draft | Original-reference and duplicate-prevention clauses now have source-linked wording. Review the draft. | owner:settlement |
| Retention decision | KQ-12 retains its blank answer. Supply the retention duration in the existing question document. | owner:settlement |
| Held scope | `access/grants.md` retains the recorded denial-clause review hold. Review during a later authorized canonical pass. | unknown |
| Canonical processing | Recovery incorporation remains pending. Reconcile the source, candidate, and unsupported `no_change` declaration through `ingest-knowledge`. | unknown |
| Publication | Candidate status remains recorded. Human approval is pending. | unknown |
| Derived wiki | The selection declares fresh inputs. Runtime freshness verification is `NOT_RUN`. | unknown |
| Business execution | Selection records historical local-fixture execution. Current execution is `NOT_RUN`. | unknown |

The checkpoint and KQ-10 identify recovery as the continuation point. [Checkpoint](../tasks/checkpoint.json) [Saved answer](../tasks/questions.md#L16)
The saved progress summary claims all four selected sources are complete.
The recovery receipt has empty outputs, while the canonical record says recovery incorporation remains pending.
This discrepancy requires later reconciliation. [Progress](../tasks/progress.md) [Selection](../selection.json) [Canonical recovery](../knowledge/records/settlement.md#L8)

Use `manage-knowledge-lifecycle` for reassessment and `ingest-knowledge` for the later canonical review workflow.
Completion requires reviewed canonical wording and matching valid completion evidence within renewed write scope.
The KQ-12 decision concerns retention duration. The other recovery clauses can proceed through independent review.

## Preserved state and dispatch

Protected-input hash checks confirm preservation of canonical records, saved answers, selection declarations, checkpoint, wiki, and other listed inputs.
The action log records the original draft hash, subsequent output hashes, actual tools, commands, reads, writes, and checks. [Action log](actions.json)

The requested worker settings are `luna` and `max`.
The saved observed dispatch is `null`. Runtime model, reasoning, and client are `UNKNOWN`.
Requested settings remain unverified. [Dispatch evidence](../tasks/checkpoint.json)

## Validation and limits

Initial link validation found two invalid settlement locators and a pending action-log target.
The locators were corrected, and the action log was created before rechecking.

- All 24 input bindings and five skill bindings matched their supplied SHA-256 hashes.
- All 23 protected fixture inputs matched their original hashes after the draft write.
- The final local check passed for three draft clauses and 24 Markdown destinations and line locators.
- Runtime source planning, sealed harness checks, wiki checks, and business execution are `NOT_RUN`.
- Supplied fixture declarations provide the planning context. Runtime receipt validity remains unverified.
- The available evidence is synthetic. Production applicability and deployment remain unverified.

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
