# Recovery handoff

The recovery draft is complete for the permitted continuation. Collection processing remains partial.
Next, `owner:settlement` should answer saved KQ-12 with the applicable late-arrival retention duration and scope. [Saved question](../tasks/questions.md#L18)

## Produced draft

The continued draft preserves original-reference retries, accepted-reference duplicate prevention, and unresolved late-arrival retention.
It retains the original checkpoint note and exact continuation request. [Recovery draft](../tasks/recovery-draft.md)

The source records proposed target behavior dated 10 November 2026. Confidence is high for these source-backed draft statements.
Its SHA-256 is `7873d7ffc27ae5a9631fafa8c2a2e99618558082b4906a4699b716eb0e8e4db6`. [Recovery source](../sources/settlement/recovery.md#L3-L7)

Draft A's seven-day duration conflicts with the source's unresolved duration. This handoff follows the retained source.
Draft B also preserves the unresolved duration. [Draft A](../drafts/answer-a.md), [draft B](../drafts/answer-b.md)

## Reconciled coverage

The saved summary declares all four selected sources complete. Current canonical omissions conflict with that declaration. [Saved summary](../tasks/progress.md#L3)

The requested denominator contains four identities. Two accepted identities were reused. Two substantive identities retain pending canonical work.

| Selected identity | Receipt evidence | Current disposition |
| --- | --- | --- |
| `portal/activity.md` | Reviewed `no_change`, output-linked to `knowledge/records/portal.md#activity` | Accepted checkpoint case reused with hash checks. |
| `context.md` | Reviewed `no_change`, justified as navigation context and duplicate agenda | Accepted contextual case reused with hash checks. |
| `settlement/recovery.md` | Reviewed `no_change`, empty outputs and missing justification | Draft completed. All recovery predicates await canonical incorporation. |
| `access/grants.md` | Reviewed `no_change`, empty outputs and missing justification | Held. Existing grants cover union and multiple roles. Denial remains omitted. |

All four identities have reviewed receipt declarations. One identity has a linked canonical output. One has a contextual justification.
The selected recovery and grants identities remain in the denominator. [Selection and receipts](../selection.json#L4-L44)

The settlement candidate explicitly records missing recovery incorporation. The access candidate omits the source's missing-grant denial clause.
Owners are `maintainer` for resumed review and `unknown` for access review assignment. [Settlement candidate](../knowledge/records/settlement.md#L7-L8), [access source](../sources/access/grants.md#L5-L7), [access candidate](../knowledge/records/access.md#L3-L8)

## Lifecycle position

| Dimension | Evidence-backed position |
| --- | --- |
| Source bindings | All four selected source hashes match fixture declarations. |
| Canonical processing | Partial. Recovery and access denial need incorporation or reviewed resolution. |
| Governance and publication | Fixture declares candidate status with human approval pending. |
| Wiki | Freshness is fixture-declared. Bridge verification is `NOT_RUN`. Canonical omissions remain visible. |
| Implementation and execution | Synthetic historical local fixture evidence only. Business behavior is `NOT_VERIFIED`. |

Publication and execution positions come from fixture declarations. [Lifecycle declarations](../selection.json#L46-L53)

## Saved scope and worker evidence

KQ-10 retains accepted work. KQ-12 remains open within its exact operator, UAT, v1 scope.
Other saved answers retain their original scopes. [Saved answers](../tasks/questions.md#L3-L18)

The checkpoint requested model `luna` with reasoning `max`. Its observed dispatch field is null.
Current observed model, reasoning, and client are `UNKNOWN`. [Worker request](../tasks/checkpoint.json#L16-L20)

## Checks and next work

Local SHA-256 checks, output links, and draft predicate checks are recorded in the action log.
Harness, source-planner, bridge, and business execution checks are `NOT_RUN` within this draft-only exercise. [Action log](actions.json)

Twenty-three protected fixture input hashes and five selected skill hashes matched their declared originals.
The permitted draft and two output files comprise this continuation's writes.

During separately authorized canonical work, the maintainer can review retry and duplicate clauses while KQ-12 remains unresolved.
An assigned access reviewer can review the explicit denial clause using `ingest-knowledge`.
Completion requires traceable canonical predicates and actual reviewed, bound processing evidence. [Recovery accounting](../tasks/recovery-draft.md#predicate-accounting), [Held scope](../tasks/checkpoint.json#L9-L10)

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not establish complete writing review.
  - Synthetic evaluation inputs do not establish business behavior.
  - Observed model, reasoning, and client settings are UNKNOWN.
```
