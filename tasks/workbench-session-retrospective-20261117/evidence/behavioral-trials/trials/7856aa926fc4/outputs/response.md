# Recovery handoff

The saved recovery draft now includes original-reference retry and duplicate-payment prevention.
Retention duration remains unresolved.
The immediate next action belongs to `owner:settlement`, who must answer KQ-12. [Updated draft](../tasks/recovery-draft.md) [Living questions](../tasks/questions.md)

> Full-collection completion remains unsupported.
> The saved summary conflicts with the checkpoint and current canonical destinations.

## Resumed work

The checkpoint identifies `settlement/recovery.md` as unfinished and assigns `tasks/recovery-draft.md` as its owned draft.
KQ-10 explicitly directs continuation while retaining accepted work.
I selected that unit and completed its source-to-draft accounting. [Checkpoint](../tasks/checkpoint.json) [Saved answer KQ-10](../tasks/questions.md)

The source permits rejected-payment retry with the original reference.
Repeating an accepted reference must create no second payment.
Its retention duration has no default.
The draft preserves all three predicates and their draft status. [Recovery source, lines 3–7](../sources/settlement/recovery.md#L3-L7)

Confidence is high for the source-to-draft transcription.
Retention duration remains unknown.
Reader draft A's seven-day statement conflicts with the source's unresolved duration.
The authoritative saved answer for KQ-12 remains blank. [Reader draft A](../drafts/answer-a.md) [Recovery source](../sources/settlement/recovery.md#L7) [Living questions](../tasks/questions.md)

## Reconciled source accounting

All four selected identities remain in scope.
The fixture declares four reviewed `no_change` receipts.
One receipt links a canonical output.
One provides a contextual reason without output.
Two supply neither output nor justification. [Selection declarations](../selection.json)

| Selected identity | Saved checkpoint | Current evidence and outcome |
| --- | --- | --- |
| `portal/activity.md` | Accepted | Receipt links `knowledge/records/portal.md#activity`. Accepted work retained without repeated semantic processing. |
| `context.md` | Accepted | Receipt explains navigation context and duplicate activity agenda. Accepted contextual disposition retained. |
| `settlement/recovery.md` | Unfinished | Owned draft now covers the source. Canonical Recovery still says no source was incorporated. |
| `access/grants.md` | Held | Canonical Grants retains union evaluation and several-role semantics. The source's denial clause remains absent. |

The accepted identity set remains `portal/activity.md` and `context.md`.
Recovery remains pending canonical incorporation.
Access remains held for denial-clause review.
These gaps contradict the saved claim that all four sources are complete. [Checkpoint](../tasks/checkpoint.json) [Saved summary](../tasks/progress.md) [Settlement candidate](../knowledge/records/settlement.md#recovery) [Access source](../sources/access/grants.md#L5-L7) [Access candidate](../knowledge/records/access.md#grants)

## Independent lifecycle status

| Dimension | Current status |
| --- | --- |
| Source review | Two accepted identities retained. Recovery source reviewed into the owned draft. Access remains held. |
| Canonical processing | Recovery incorporation and access denial remain pending despite reviewed receipt declarations. |
| Intent and governance | Recovery is draft target behavior. KQ-12 remains unresolved. |
| Publication | Candidate state with human approval pending, according to the fixture declaration. |
| Derived wiki | Fresh-input membership is declared. Semantic agreement remains contradicted by the proposed primary-scalar-role claim. |
| Business execution and deployment | NOT_VERIFIED. The fixture declares historical local execution only. |

The wiki's primary-scalar-role statement conflicts with the grant source's explicit absence of that role.
Its fresh-input list supplies no reviewed resolution.
Owner is `unknown`.
The next authorized wiki review must resolve that contradiction after canonical work. [Proposed wiki](../wiki/proposed.md) [Grant source](../sources/access/grants.md#L6) [Selection declarations](../selection.json)

## Next actions

| Action | Reason and evidence | Owner | Selected skill | Required input | Observable completion |
| --- | --- | --- | --- | --- | --- |
| Answer KQ-12. | Recovery source leaves retention unresolved. | `owner:settlement` | `manage-knowledge-lifecycle` | Retention duration and applicable scope. | A sourced answer appears in the existing living question. |
| Incorporate recovery and review held denial when authorized. | Current canonical destinations omit those predicates. | `unknown` | `ingest-knowledge` | Canonical-edit authorization and required review. | Source clauses map to reviewed canonical outputs and valid completion evidence. |

The unresolved retention answer did not prevent completion of the authorized draft.
Saved answers retain their original question scopes. [Living questions](../tasks/questions.md)

## Checks and retained boundaries

Initial SHA-256 checks matched all 24 listed fixture inputs and four inspected skill files.
Final checks verify protected input hashes, output links, and required draft text.
The action log retains commands, results, timing, hashes, and the original interrupted draft. [Action log](actions.json)

The authorized edits are `tasks/recovery-draft.md`, `outputs/response.md`, and `outputs/actions.json`.
All 23 other listed fixture inputs retain their supplied hashes.
This includes canonical records, saved answers, receipt declarations, checkpoint, accepted sources, and wiki.

The source planner and ingestion harness are NOT_RUN under this draft-only authorization.
Business transitions and network calls remain outside the supplied scope.
This synthetic exercise supplies no business acceptance, production, or deployment evidence.

The checkpoint requests model `luna` with reasoning `max`.
Observed model, reasoning, client, and dispatch identity are UNKNOWN.
The checkpoint's observed dispatch is null. [Checkpoint](../tasks/checkpoint.json)

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
