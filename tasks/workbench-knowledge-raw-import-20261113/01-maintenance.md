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

- Latest continuation in the same Codex chat:

  > go on

- Continuation on 14 November 2026 (Asia/Singapore):

  > go on

- Source-filtering follow-up and continuation in the same chat:

  > why you missed the first step filtering ?

  > go on

- Goal request on 14 November 2026 (Asia/Singapore), from the same Codex chat:

  > make a goal to process all knowledges till blocked by my input

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

## Grouping and settlement rules filtering

On 14 November 2026, this batch reviewed 43 pages. It kept 31, classified five as evidence only, excluded five, and placed two on hold.

| Collection | Pages kept | Evidence only | Excluded | Held in this batch | Pending source review | Selected pages queued for processing |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `cash-settlement-home-page` | 22 | 5 | 5 | 0 | 756 | 27 |
| `ratan-51358` | 9 | 0 | 0 | 2 | 161 | 16 |

The Cash selections cover Group Blotter visibility, trade validation, and manual STP. They also cover market-specific SSI matching, suppression, and LMS eligibility. The decisions retain conflicting status names, eligibility conditions, and market scope. See the [Cash decisions](evidence/filter-grouping-and-rules-cash-settlement-home-page.json).

The RATAN selections cover netting, SSI stamping, exception checks, SWIFT, accounting, and related interfaces. Last Mile Check remains held because its prose and SQL give different economic comparisons. The interface diagram remains held because the export contains only its link. See the [RATAN decisions](evidence/filter-grouping-and-rules-ratan-51358.json).

Workspace validation passed. Both source verifiers returned `NEEDS_REVIEW` with zero binding findings. All 43 queued outputs match their retained hashes and source lines. See the [batch checks](evidence/filter-grouping-and-rules-checks.json).

## Release eligibility and accounting filtering

On 14 November 2026, this batch reviewed 50 pages. It kept 37, classified eight as evidence only, excluded two, and placed three on hold.

| Collection | Pages kept | Evidence only | Excluded | Held in this batch | Pending source review | Selected pages queued for processing |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `cash-settlement-home-page` | 28 | 8 | 2 | 3 | 718, including four holds | 55 |
| `ratan-51358` | 9 | 0 | 0 | 0 | 152, including two holds | 25 |

The Cash selections cover payment release, splitting, Nostro, SWIFT, and accounting by market. The high-value exception prose and scenario table disagree on the maker-only case. The Korea TLM technical page remains on hold because the sources give different query boundaries and parameter types. The other holds cover a possible Korea rejection flow and a missing TLM UAT artifact. The two exclusions contain only headings or navigation. See the [Cash decisions](evidence/filter-release-and-accounting-cash-settlement-home-page.json).

The RATAN selections cover Aspire, EBBS, ENISIS, FXU, Murex, OLTP, TIS, and TLM. The Korea sources describe SFTP as the baseline and Solace as the proposed target. The TLM selections preserve opposite endpoint inclusivity rules for the query window. See the [RATAN decisions](evidence/filter-release-and-accounting-ratan-51358.json).

Workspace validation passed. Both source verifiers returned `NEEDS_REVIEW` with zero binding findings. All 80 queued outputs match the retained source hashes and selected lines. This batch stopped at filtered views. See the [batch checks](evidence/filter-release-and-accounting-checks.json).

## Full processing goal

Complete semantic filtering for both registered exports. Process the supported selections into reviewed candidates and applicable wiki pages. Continue independent work while any source or decision is pending.

### First source review checkpoint

This batch reviewed 111 pages. It kept 52, classified 28 as evidence only, excluded 28, and placed three on hold.

| Collection | Pages reviewed | Pages kept | Evidence only | Excluded | Held in this batch | Pending source review | Selected pages queued for processing |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `cash-settlement-home-page` | 76 | 20 | 27 | 26 | 3 | 645 | 75 |
| `ratan-51358` | 35 | 32 | 1 | 2 | 0 | 117 | 57 |

The Cash decisions cover onboarding, market routing, blotter fields, netting, and exception handling. Three holds cover Murex cancellation sequencing, Razor precedence, and the entitlement fetch flow. The last two lack their source diagrams. See the [Cash decisions](evidence/goal-source-review-01-cash-settlement-home-page.json).

The RATAN decisions cover external interfaces and scoped release requirements. The decisions preserve entitlement migration scope and an unresolved timestamp convention. See the [RATAN decisions](evidence/goal-source-review-01-ratan-51358.json).

Workspace validation passed. Both source verifiers returned `NEEDS_REVIEW` with zero binding findings. The 132 queued outputs match the original hashes and selected lines. See the [checkpoint checks](evidence/goal-source-review-01-checks.json).

### Second source review checkpoint

This batch reviewed 101 new pages and refined one existing selection.

| Collection | New pages reviewed | Pages kept | Evidence only | Excluded | Held in this batch | Pending source review | Selected pages queued for processing |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `cash-settlement-home-page` | 29 | 6 | 19 | 4 | 0 | 616 | 81 |
| `ratan-51358` | 72 | 13 | 47 | 10 | 2 | 47 | 70 |

The Cash review completes the available manual-entity pages and adds dated release requirements. The updated onboarding selection includes accounting time zones. Retained source line 1211 confirms UK SSI precedence and also contains an entity list. The view omits that line. See the [Cash decisions](evidence/goal-source-review-02-cash-settlement-home-page.json).

The RATAN review covers core functions, operations, and dated release changes. The architecture and firewall pages remain on hold because their referenced content is missing. See the [RATAN decisions](evidence/goal-source-review-02-ratan-51358.json).

The 29 Cash and 72 RATAN decision rows were recovered from the saved post-first plan and pre-third selection snapshots. Their source hashes, reasons, ranges, topics, intent statuses, and contexts match those snapshots. See the [Cash decisions](evidence/goal-source-review-02-cash-settlement-home-page.json), [RATAN decisions](evidence/goal-source-review-02-ratan-51358.json), and [reconstruction record](evidence/goal-source-review-02-reconstruction.json).

The original workspace validation, source verification, and 151-entry view check were not retained. This recovery does not recreate those command results.

### Third source review checkpoint

This batch reviewed 72 new pages and rechecked 17 existing Cash decisions.

| Collection | New pages reviewed | Pages kept | Evidence only | Excluded | Held in this batch | Pending source review | Selected pages queued for processing |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `cash-settlement-home-page` | 29 | 18 | 8 | 2 | 1 | 588 | 99 |
| `ratan-51358` | 43 | 5 | 33 | 5 | 0 | 4, all holds | 75 |

The Cash selections cover 2026 migration controls, new currency static data, Nostro, Vostro, and rounding. The rounding table is a dated 2024 proposal. Its current applicability remains unknown. See the [Cash decisions](evidence/goal-source-review-03-cash-settlement-home-page.json).

The RATAN selections complete the release-plan review. They retain dated requirements and rollout evidence with separate status. See the [RATAN decisions](evidence/goal-source-review-03-ratan-51358.json).

Workspace validation passed. Both source verifiers returned `NEEDS_REVIEW` with zero binding findings. All 174 queued view entries match retained source hashes and selected lines. See the [checkpoint checks](evidence/goal-source-review-03-checks.json).

The check file's before plans show 645 Cash and 117 RATAN pending pages. The saved pre-third selection snapshots show 616 and 47. The immediate before-plan ID is missing; see the [checkpoint integrity note](evidence/goal-source-review-03-integrity-note.json).

Decision and check filenames moved from `goal-source-review-02-*` to `goal-source-review-03-*`. The decision-file hashes stayed unchanged.

### Fourth source review checkpoint

This batch reviewed four Cash pages and selected sections from all four. It made no new RATAN decisions.

| Collection | Pages reviewed | Kept sections | Pending source review | Selected pages queued for processing |
| --- | ---: | ---: | ---: | ---: |
| `cash-settlement-home-page` | 4 | 4 | 584, including eight holds | 103 |
| `ratan-51358` | 0 | 0 | 4, all holds | 75 |

The Cash selections preserve a proposed API Gateway resilience design, Indonesia onshore requirements, the migration cutover sequence, and message-bridge changes. The `folder` route type remains unresolved. The [decision batch](evidence/goal-source-review-04-cash-settlement-home-page.json) records exact ranges and status.

Workspace validation returned `VALID`. Both source verifiers returned `NEEDS_REVIEW` with zero findings. All 103 Cash view entries match source hashes, ranges, mappings, and output hashes. The new ranges passed the configured secret-pattern scan. See the [checkpoint checks](evidence/goal-source-review-04-checks.json).

No canonical candidate changed during this source-filtering checkpoint.

### Fifth source review checkpoint

This batch reviewed three new Cash pages. It kept one page and classified two as evidence only.

The Indonesia UI page contributes eight dated requirements. The RDM day-zero page describes implementation alternatives, observed database counts, service links, and scheduled jobs. It remains evidence only because no approved business-level data-coverage rule is stated. The upstream and downstream inventory also remains evidence only.

Both collection verifiers returned `NEEDS_REVIEW` with zero findings. Cash has 573 undecided pages and eight holds. RATAN has four holds. The fresh Cash plan queues 104 selected pages for later processing.

Workspace validation returned `VALID`. All 104 queued view entries match their retained source hashes and selected line ranges. See the [checkpoint checks](evidence/goal-source-review-05-checks.json) and [Cash decisions](evidence/goal-source-review-05-cash-settlement-home-page.json).

No canonical candidate changed during this source-filtering checkpoint.

### Sixth source review checkpoint

This batch reviewed 20 Cash pages: six evidence only, four excluded, three kept, five section selections, and two holds.

The kept pages cover a proposed Ratan Code Review Agent, Octopus Service API material, Java coding guidance, and draft quality rules. Proposal and draft status remain explicit. The [decision batch](evidence/goal-source-review-06-cash-settlement-home-page.json) records exact source hashes, ranges, and reasons.

The handover does not decide whether Uber lifecycle actions call `status/move` or publish domain events. The SSI form draft requests further design review. Both pages remain held until their expected behavior is confirmed.

Cash verification returned `NEEDS_REVIEW` with zero binding findings. It reports 553 undecided pages and ten holds. The fresh plan queues 112 pages for later processing. The 112-page view omits both new holds. Its source hashes, ranges, mappings, and output hashes passed checks. See the [checkpoint checks](evidence/goal-source-review-06-checks.json).

Workspace validation returned `VALID`. No canonical candidate changed during this source-filtering checkpoint. RATAN still has four held pages.

## Validation and maintenance

The larger source manifest exceeded the validator's one MiB record limit.
The validator now accepts source manifests up to 16 MiB. The limit for individual records and audit events remains one MiB.
The [workspace design](../../docs/WORKSPACE_DESIGN.md#knowledge-format-and-governance) records the current limit.
The regression covers an accepted large manifest and a rejected oversized record.
Workspace validation passed with zero findings. The wheel built and initialized a valid empty workspace with the shipped guides, skills, and schemas.
The first [test run](evidence/runtime-tests.log) had 36 sandbox errors at local loopback binds.
The loopback rerun finished with 1,068 tests, two skips, and no failures or errors.

## Next action

Continue reviewing Cash pages from the current plan. Skip the two held pages and start with `Testing SpringData with Embedded PostgreSQL`. Process selected pages only after both source queues are decided or remaining pages have supported held dispositions.
The Settlement owner needs to confirm the effective rules below. The owner is unknown.
The sources describe design and proposed behavior. Approval, current applicability, and production behavior remain unverified.

| Question for the Settlement owner | Current evidence | Owner answer |
| --- | --- | --- |
| Which parties send each ACK or NACK? What triggers retry or reconciliation? | The FX source names an internal NACK and a Razor ACK. The SABRE page describes a separate Stella booking response. | Pending |
| Which cashflow version, event, and matching fields apply to each flow? | The Uber validation description and Stella integration proposal use different duplicate checks. The FX source also names a message ID and tolerances. | Pending |
| Which entity, event, and reversal conditions govern the write-back rule? | The FX requirements and technical flow list different trigger sets. Their current scope is unresolved. | Pending |
| Should the Indonesia message bridge keep the `folder` route type? | The integration plan asks this. An unreviewed restructure page contains historical folder routes, but does not answer the Indonesia target. | Pending |
| Does the API Gateway resilience proposal apply to the RATAN Indonesia scope? | The design lists proposed resilience changes without recorded approval or scope confirmation. | Pending |
| For Uber lifecycle updates, should each action call `status/move`, publish only a domain event, or vary by action? | The handover leaves the call open. The Uber workflow API page also says publishing behavior needs confirmation. | Pending |
| For SSI UI, should 57A BIC format validation run independently of mandatory checks and rule order for MT202? | The draft requests further design review. The linked work items and screenshots are not retained. | Pending |

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
