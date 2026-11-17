# Recovery draft

Resumed the unfinished payment recovery draft from the saved checkpoint.
The immediate next action is owner:settlement answering KQ-12 in the existing living questions.

## Draft target behavior

The source records draft target behavior dated 10 November 2026.

- A rejected payment can be retried with its original payment reference.
- Repeating an accepted reference must not create a second payment.
- Late-arrival retention duration remains unresolved. The source supplies no default.

These statements retain the source's draft status.
Implementation, execution, approval, and deployment remain unverified for this recovery behavior. [Recovery source](../sources/settlement/recovery.md#L3-L7)

Source SHA-256 is `7873d7ffc27ae5a9631fafa8c2a2e99618558082b4906a4699b716eb0e8e4db6`.
The supplied input manifest and current source bytes agree. [Input manifest](../evaluation-input.json)

## Saved decisions and unresolved scope

KQ-10 directs continuation of this draft while retaining accepted work.
KQ-11 requires consumer and provenance review before deleting equal-hash evidence.
Both saved answers retain their exact existing scope.
KQ-12 remains unanswered for operator, UAT, v1.
Owner:settlement must supply the retention duration.
The seven-day value in reader draft A lacks support in the recovery source. [Living questions](questions.md) [Reader draft A](../drafts/answer-a.md)

## Recovery checkpoint

| Scope | Evidence-backed position | Next action |
| --- | --- | --- |
| Portal activity | Accepted unchanged work remains reusable. Its canonical activity text agrees with the selected source. | Retain accepted work. |
| Navigation context | Accepted unchanged context declares no additional intent. | Retain its existing disposition. |
| Payment recovery | This draft now includes original-reference retries and accepted-reference duplicate prevention. Canonical recovery remains unincorporated. | Resolve KQ-12. Retain supported draft clauses meanwhile. |
| Access grants | Held. The canonical record omits the source's missing-action-grant denial clause. | Authorized canonical reviewer reviews that clause. No new human answer is required to retain draft intent. |

The checkpoint identifies recovery as unfinished and access as held.
The progress summary's collection-complete claim conflicts with those artifacts.
Settlement and access receipts declare no change, with empty outputs and no supporting reason.
Their current canonical contents leave the identified clauses unincorporated.
This continuation supplies draft work only. [Checkpoint](checkpoint.json) [Progress summary](progress.md) [Selection declarations](../selection.json) [Settlement candidate](../knowledge/records/settlement.md#L7-L8) [Access source](../sources/access/grants.md#L3-L7) [Access candidate](../knowledge/records/access.md) [Portal source](../sources/portal/activity.md) [Portal candidate](../knowledge/records/portal.md) [Navigation source](../sources/context.md)

## Authorization and continuation source

The exact continuation prompt follows.

> In /var/folders/3q/zc3tlwsj1p1_pskzk1j9r5100000gn/T/wb-evaluation-sft1jwcb/7bfddbad1906, Continue the authorized unfinished draft from the saved checkpoint and record a handoff at outputs/response.md. You may edit only tasks/recovery-draft.md and outputs/. Keep canonical records, saved answers, receipts and wiki unchanged. The fixture is synthetic. Local file reading and the named output writes are authorized; network calls and business transitions are not. Use the selected skills from evaluation-input.json.

The selected skills are manage-knowledge-lifecycle and ingest-knowledge.
The checkpoint requests luna with max reasoning.
Observed model, reasoning, and client settings are UNKNOWN.
Observed dispatch evidence is null. [Task input](../evaluation-input.json) [Checkpoint](checkpoint.json)

## Checks and limits

Automated checks cover supplied hashes, protected-input preservation, recovery draft contents, local links, and sentence lengths.
Detailed commands and results are retained in the action log.
Source planning, governed harness checks, receipts, publication, and wiki operations have status NOT_RUN.
This synthetic draft continuation establishes documented intent within the cited source. [Action log](../outputs/actions.json)

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
