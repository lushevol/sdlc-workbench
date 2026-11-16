# Conversion workflow diagnostic

> **The workflow is incomplete. Accepted receipts and candidate counts do not establish complete semantic coverage.**

The [workflow facts](conversion-diagnostic-20261117-workflow-facts.json) retain counts, hashes, timestamps, session metadata and checkpoint checks.
The audit inspected checkpoint artifacts from 178 through 225. It inventoried 508 direct checkpoint files.
It inspected 22 finalization summaries and reopened 20 referenced final-check results.
The two wiki finalizations use separate bridge evidence. Their detailed review belongs to the canonical/wiki auditor.

## Evidence and trust

Native session events request `auto/gpt-6.1-sol` with `medium` for source and wiki review.
Document and held-document sessions request `auto/gpt-6-luna` with `max`.
These events establish client selection. Independent runtime attestation remains unavailable.
Historical unverified drafts require fresh affected semantic review.
Exact-byte validation checks bindings and format. It cannot establish human approval or business correctness.

Checkpoint 178 corrected declarations and refreshed 44 prior receipts.
Checkpoint 179 first rejected completion because its changed navigation index was absent from declared outputs.
Its corrected completion preserved that failure and included the sealed index.
Later preparation failures and rejected event drafts remain retained.
Checkpoint 225 refreshed 103 prior receipts after shared dependencies changed.
These receipt refreshes do not establish 147 newly read documents.

## Workflow findings

| ID | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- |
| WF-01 | Source status reports two stale wiki inputs. Wiki status records three refreshed summaries. | Saved status can trigger repeated work or incorrect remaining counts. | unknown | Reconcile current canonical hashes, wiki outputs and current plan. |
| WF-02 | The cohort index binds 477 queued identities. Current saved plans queue 465. | Earlier inventories require reconciliation before dispatch or acceptance. | unknown | Reconcile exact source and closure bindings. Review the ready proposal before acceptance. |
| WF-03 | Both Luna sessions contain approximately nine-hour event gaps. Tool errors and retries remain recorded. | Wall-clock duration cannot establish continuous semantic work or a reliable ETA. | unknown | Measure accepted distinct cases during bounded working intervals. |
| WF-04 | Checkpoints 178 and 225 refreshed dependency receipts. | Summed receipt counts overstate new source reading. | unknown | Separate new identities, original hashes and refreshed receipts. |

The current document status records one ready case and zero accepted reused cases.
Its private successor remains `UNREVIEWED_PROPOSAL` and `accepted: false`.
The held-document status records one limited review, zero full-content reviews and zero resolved proposals.
Neither status establishes accepted canonical conversion.
Console termination and `agent_settled` events describe saved runs. They do not prove current operating-system activity.

## Timing and throughput

The document session records a 33,000.385-second gap between 13:56:36Z and 23:06:36Z on 16 November.
The held-document session records a 32,969.716-second gap between 13:57:23Z and 23:06:53Z.
These gaps are idle or unobserved intervals. They are separate from recorded working intervals.
The wiki session has a further 981.869-second gap.
Subtracting large gaps gives an event-span measure. It does not measure model computation or productive reading time.

Checkpoint 219 accepted 136 distinct reviewed identities at 13:23:39.208940Z.
Checkpoint 225 records 25 additional distinct cases by 13:55:02.798853Z.
The bounded acceptance rate is `25 / 0.5232194202777778 hours`, approximately 47.78 identities per hour.
This interval measures receipt integration. Reviews can predate that interval.
It does not measure distinct-original semantic throughput and cannot support a completion ETA.
The inspected current report already states uncertain duration. No reproducible numerical ETA was identified in inspected status evidence.

## Closure and index behavior

The implementation in [incremental.py](../../../core/ingestion/incremental.py#L145) builds relationships from canonical body links and `related` IDs.
Direct source citations and prior outputs seed reverse dependent closure. Forward closure supplies dependency hashes.
Navigation files are hashed but do not create topic dependency edges.
The index rejection at checkpoint 179 concerns changed-output membership in completion checks.
It does not establish that all index links expand runtime dependencies.
Source declarations and cross-topic relationships can still make review closures large.
Missing relationships can also omit relevant consumers. No runtime changes were made.

## Questions and available work

The reviewed owner-bundle tables contain 310 distinct row IDs with blank answers.
These are document rows. Overlapping decisions can remain across bundles and earlier registers.
The older register contains 987 exact-text rows from 1,527 occurrences.
Checkpoint 220 maps 108 proposals to existing topics: 103 summary proposals and five domain proposals.
These counts cannot be added to obtain independent owner decisions.
The 28 earlier held-review groups remain separate from 44 held collection identities.
Existing model-gate answers remain preserved. Current policy and publication answers cannot be inferred.

There are 465 queued identities and 44 held identities in the current saved plans.
Publication remains zero. Those facts do not establish that all conversion work requires owner answers.
Agents can review supported selected intent and reconcile valid receipts under separate conversion authorization.
Owners must supply only remaining source authority, missing artifacts and material policy decisions.
Human publication review remains separate.

## Storage and verification limits

The metadata snapshot counted 118,728,099 bytes across 134 files under `.workbench/pi/`.
It found 25 duplicate files, with 1,888 duplicate bytes.
Task evidence contained 19,820,654 bytes across 1,113 files.
It found 90 duplicate files, with 403,275 duplicate bytes.
Duplicate bytes count extra exact-byte copies after retaining one copy per hash.
The Pi totals include sessions, console logs and ongoing diagnostic work at the snapshot time.
The four conversion session files total 12,218,233 bytes. The nine conversion console files total 85,247,523 bytes.
These groups contain no identical whole-file duplicates. Nine stderr files are empty.
Streaming logs repeat event information without necessarily creating identical whole files.
These totals do not authorize deletion. No cleanup ran.

## Writing review

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not establish complete writing review.
```
