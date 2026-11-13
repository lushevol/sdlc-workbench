# Cash Settlement and RATAN knowledge intake

> **The two collections are registered. Both still need source review.**
>
> Use the reviewed subset for draft knowledge. Confirm the applicable write-back rules with the Settlement domain owner before using them as requirements. The owner is unknown.

## Request and scope

- Date: 13 November 2026 (Asia/Singapore).
- User, in this Codex chat:

  > I updated knowledge to add raw docs

- Selected source identities:

  > Register two new collections: `cash-settlement-home-page` and `ratan-51358` (Recommended)

- Continuation in the same chat:

  > go on

- User follow-up on source order in the same Codex chat:

  > won’t you the first step be filtering raw knowledge before processing?

  Apply source filtering first. Use only reviewed selections in any later candidate update.

- Baseline: `ff077ed85`. The unrelated connector lockfile deletion, release-report files, and Azure DevOps assessment are outside this task.

## Retention and review

| Collection | Supplied | Retained | Kept in first filtered view | Still needs source review |
| --- | ---: | ---: | ---: | ---: |
| `cash-settlement-home-page` | 884 | 872 | 5 | 864, including one hold |
| `ratan-51358` | 189 | 188 | 6 | 180 |

The original exports remain in their ignored inboxes. The existing `settlement-netting` collection keeps its prior identity, bytes, and bindings.
The first selection pass relied too heavily on path and content patterns. Its receipts remain in ignored recovery storage and do not establish semantic review.
The active selections contain only page-level decisions from the [Cash review](evidence/reviewed-cash-settlement-home-page.json) and [RATAN review](evidence/reviewed-ratan-51358.json).

The [retention screen](evidence/retention-screen.json) records 13 withheld pages, their original hashes, and relevant line numbers.
The Cash Status Machine page contains apparent authentication credentials. Other matches need credential review.
The complete flagged bytes remain in the ignored user inboxes. They were removed from this attempt's uncommitted snapshot copies before staging.
The original manifest remains the exact prefix of the current manifest. All 560 prior registrations are preserved.
An independent scan found no additional suspected secrets in the new snapshots using the tested patterns. It cannot establish complete absence.

The active selection roots are screened, ignored copies under `knowledge/evidence/incoming/retention-screen-20261113/`.
To restore a screened inbox, recreate the collection directory and each `origin_path` from its registered snapshot. Verify the bytes against its manifest hash.
Review flagged pages before adding them. Bind permitted excerpts to their original hashes and line ranges.
The [view checks](evidence/scoped-source-checks.json) bind both plans and verify all 11 selected outputs against the original bytes and line ranges.
The LMS action matrix remains on hold because its workbook is missing.

## First candidate and wiki update

[Cashflow identity and Stella write-back](../../knowledge/records/candidates/settlement/KT-settlement-cashflow-identity-and-stella-write-back.md) covers four Cash pages and two RATAN pages.
The [independent claim review](evidence/candidate-review.json) records the exact candidate hash. The final ingestion check passed with one new candidate event.
The [wiki summary](../../knowledge/llm-wiki/wiki/summaries/KT-settlement-cashflow-identity-and-stella-write-back.md) carries the same evidence limits. The scoped wiki plan now returns unchanged.
The [completion evidence](evidence/completion.json) records both processing receipts. The six source pages match the reviewed selection hashes and ranges.

## Source filtering follow-up

Review retained raw pages and create a filtered view before processing them into candidates. The earlier batch did this for the six processed pages. The earlier handoff put candidate work ahead of the remaining source review.

The follow-up reviewed 86 additional pages. It kept exact sections from seven and excluded 79 confirmed empty exports. The retained originals remain available for provenance.

| Collection | Additional pages kept | Empty pages excluded | Pending source review | Selected pages queued for processing |
| --- | ---: | ---: | ---: | ---: |
| `cash-settlement-home-page` | 4 | 72 | 788, including one hold | 5 |
| `ratan-51358` | 3 | 7 | 170 | 7 |

The Cash selections cover Group Blotter fields and monitoring, cashflow data, and SCBML generation. The RATAN selections cover prechecks, suppression, and stamping. Both preserve unresolved scope and source differences. See the [Cash decisions](evidence/filter-followup-cash-settlement-home-page.json) and [RATAN decisions](evidence/filter-followup-ratan-51358.json).

Workspace validation passed. Source verification found no binding issues and returned `NEEDS_REVIEW` for both collections. The new partial views match the selected hashes and line ranges. See the [filtering checks](evidence/filter-followup-checks.json).

## Validation and maintenance

The larger source manifest exceeded the validator's one MiB record limit.
The validator now accepts source manifests up to 16 MiB. The limit for individual records and audit events remains one MiB.
The [workspace design](../../docs/WORKSPACE_DESIGN.md#knowledge-format-and-governance) records the current limit.
The regression covers an accepted large manifest and a rejected oversized record.
Workspace validation passed with zero findings. The wheel built and initialized a valid empty workspace with the shipped guides, skills, and schemas.
The first [test run](evidence/runtime-tests.log) had 36 sandbox errors at local loopback binds.
The loopback rerun finished with 1,068 tests, two skips, and no failures or errors.

## Next action

Continue filtering raw pages in topic groups. Use each verified view as the input for later candidate processing. Prioritize related sources that clarify Group Blotter visibility, suppression states, and market applicability.
The Settlement owner needs to confirm the effective rules below. The owner is unknown.
The sources describe design and proposed behavior. Approval, current applicability, and production behavior remain unverified.

| Question for the Settlement owner | Current evidence | Owner answer |
| --- | --- | --- |
| Which parties send each ACK or NACK? What triggers retry or reconciliation? | The FX source names an internal NACK and a Razor ACK. The SABRE page describes a separate Stella booking response. | Pending |
| Which cashflow version, event, and matching fields apply to each flow? | The Uber validation description and Stella integration proposal use different duplicate checks. The FX source also names a message ID and tolerances. | Pending |
| Which entity, event, and reversal conditions govern the write-back rule? | The FX requirements and technical flow list different trigger sets. Their current scope is unresolved. | Pending |

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not establish complete writing review.
  - Source checks do not establish applicability, approval, or production behavior.
```
