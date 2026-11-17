# Git-only resume blocker investigation

> **Confirmed: absent ignored inboxes move processing work into review and block views despite intact retained snapshots.**
> The Git-only handoff omitted this runtime dependency. Reconstruct the historical inbox inventory before creating fresh plans.

Date: 17 November 2026 (Asia/Singapore).

## Exact user input

```text
/Users/lushevol/Downloads/IMG_3584.HEIC check why it blocked
```

Image SHA-256: `cf30d182f8ab94cdea19d2004b0cca9f9b40dc70682d8b0e2358e85a42cc4959`.
The image remains local. The path identifies the supplied evidence, not a portable project dependency.

## Investigation scope

Inspect the pictured blocker against the Git-only handoff and current source preparation runtime.
Use isolated fixtures for reproduction. Preserve exports, selections, receipts, records, audits, and unrelated changes.
This diagnosis does not change source freshness rules or establish the other machine's current state.

Inspected revision: `6dd2e44fc05f26501e0d2d7c8b99fc10b8190b85`.
Runtime risk: none from inspection. A future freshness correction must preserve changed-export detection and retained-source integrity checks.

## Screenshot observation

The other agent reports 1,213 registered bindings with existing, matching retained snapshots.
It reports missing export folders for Cash Settlement (884), RATAN (189), and Settlement netting (55).
Those three collections total 1,128 bindings. The screenshot reports `input_presence_changed` and rejected filtered views.
These are screenshot observations until independently reproduced or checked against this checkout.

## Result

All 1,213 selection bindings resolve to existing, Git-tracked snapshots with matching SHA-256 values.
They reference 1,030 unique snapshot paths. These counts describe bound inputs, not semantic conversion coverage.

| Collection | Bound pages | Recorded input root | Git transfer |
| --- | ---: | --- | --- |
| Cash Settlement | 884 | `knowledge/evidence/incoming/Cash Settlement Home Page` | Ignored inbox absent on a clean clone. |
| RATAN | 189 | `knowledge/evidence/incoming/RATAN - 51358` | Ignored inbox absent on a clean clone. |
| Settlement netting | 55 | `knowledge/evidence/incoming/settlement-netting` | Ignored inbox absent on a clean clone. |
| Portal | 85 | `knowledge/evidence/sources/confluence` | Tracked input directory survives Git transfer. |

The three affected collections total 1,128 bindings, matching the screenshot.
All four input directories currently exist on this machine. The destination filesystem was not inspected directly.

## Exact failure chain

1. [Freshness checking](../../../core/ingestion/sources.py#L453) treats an absent `input_root` as an empty inventory.
2. Stored `present: true` rows receive `input_presence_changed` and `input_missing` findings.
3. [Planning](../../../core/ingestion/incremental.py#L270) moves those rows into review because `input_presence_changed` remains blocking.
4. [View generation](../../../core/ingestion/sources.py#L553) rejects the same freshness finding before reading retained snapshots.

The [snapshot validation](../../../core/ingestion/sources.py#L217) independently checks retained source identities and bytes.
However, valid snapshots do not satisfy the separate export-presence guard.
The runtime cannot distinguish a non-transferred inbox from an export that actually omitted pages.

The [earlier handoff](knowledge-conversion-git-only-handoff-20261117.md#the-incoming-folder) correctly identifies the retained source of record.
Its claim that fresh plans and views suffice was incomplete. Inbox reconstruction was also required by this runtime.

## Tested recovery for the destination AI

Use this bounded recovery before resuming the existing handoff:

1. Read each collection's selection index and verify every binding against the retained manifest and snapshot hash.
2. Recover only an entirely absent `input_root` beneath ignored `knowledge/evidence/incoming/`.
3. For every `present: true` row, recreate `input_root/path` from its exact verified `source.snapshot` bytes.
4. Include all decisions: `KEEP`, `KEEP_SECTIONS`, `EVIDENCE_ONLY`, `EXCLUDE`, and `HOLD`.
5. Preserve `present: false` omissions. Reject path escapes, symlinks, conflicting paths, and any unexpected existing directory.
6. Record restored paths and hashes. Confirm that manifest, selections, receipts, canonical records, and audits remain unchanged.
7. Run `sources verify`, then create fresh plans and fresh plan-bound views under the existing handoff.

These copies reconstruct the last registered inventory. They do not represent a new or current upstream export.
Keep reconstructed inboxes ignored. The original incoming export does not need transfer.
Unresolved `HOLD` decisions and other genuine freshness findings remain blockers within their actual scope.
Do not require a whole collection to become `READY` before processing its eligible, reviewed subset.

Do not run `sources refresh` against an absent or empty inbox.
An absent directory fails refresh before mutation.
[Refresh from an existing empty directory](../../../core/ingestion/sources.py#L419) would mark all existing pages `present: false`.
That would change the registered export inventory.
Do not point refresh at retained snapshot storage, edit presence flags, or suppress freshness checks.
An explicit retained-snapshot mode would be a separate runtime change; this diagnosis implements none.

## Executed checks and limits

The [retained reproduction](git-only-resume-blocker-20261117.json) records ten passing assertions using the existing source preparation fixture.

- Present inbox: verification reports `READY`; two sources enter processing and render successfully.
- Absent inbox: both sources return to review; zero sources enter processing; view creation fails as stale.
- Retained source hashes remain valid throughout the failure.
- Reconstructed inbox: planning and views recover without refresh or changes to the fixture's manifest, selection, policy, or registry.

The reproduction used an isolated temporary legacy-layout fixture and current runtime functions.
It exercised two `KEEP`, `present: true` pages.
Recovery safeguards for other decisions and `present: false` rows received code review, not fixture execution.
The current consolidated checkout received a read-only binding and hash audit.
An independent GPT-6.1 Sol / Medium reviewer confirmed the failure chain and recovery constraints.
Configured model selection is recorded; independent backend attestation remains unavailable.
The other machine's recovery and semantic conversion remain unexecuted here.

Owner of destination recovery: the destination AI agent. No business answer or new source export is required for this blocker.
Completion condition: restored historical inventory, unchanged tracked source state, and fresh views for eligible queued sources.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not establish complete writing review.
```
