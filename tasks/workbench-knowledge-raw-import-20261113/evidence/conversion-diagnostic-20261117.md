# Knowledge conversion diagnostic — 17 November 2026

> **Conversion is partial. Current output-linked receipts cover 139/622 selected identities (22.35%). Complete semantic coverage is UNKNOWN.**
>
> The wiki has current bindings for 117/117 candidates and matching hashes for 208/208 reviewed outputs.
> These results do not establish complete source conversion. Two sampled accepted receipts omit selected draft intent.
> Publication remains 0/117. Available agent work remains: 465 queued identities and 44 separate held identities.

The immediate next action is an authorized review of the two omitted draft-intent cases.
The diagnostic performed no conversion repairs, publication, cleanup or external operations.

## Scope, evidence and trust

The [exact request](user-comprehensive-diagnostic-20261117.md) asks for conversion rates and coverage.
This report assesses the current checkout, including existing uncommitted wiki refreshes.
The [companion JSON](conversion-diagnostic-20261117.json) records snapshot timestamps, formulas, hashes, checks and evidence paths.

Three audit lanes cover [sources](conversion-diagnostic-20261117-source-audit.md), [canonical records and wiki](conversion-diagnostic-20261117-workflow-canonical-wiki-audit.md), and [workflow](conversion-diagnostic-20261117-workflow-review.md).
Their retained evidence contains exact source identities, original line ranges, current hashes and review limits.
The auditors checked protected data for drift. No diagnostic knowledge changes were found.

Confidence is HIGH for current counts, hash bindings and observed check results.
Confidence is bounded for historical review claims. The audit did not repeat every historical semantic review.
Complete semantic coverage remains UNKNOWN. No exhaustive clause inventory supplies its denominator.

Native sessions request GPT-6.1 Sol / Medium for reviews and GPT-6 Luna / Max for document processing.
Independent runtime attestation remains unavailable under the [accepted selection limit](user-review-model-decision-20261116.md).
Earlier unverified drafts do not inherit fresh review. Exact-byte checks cannot establish semantic correctness or human approval.

## Conversion rates and denominators

Each percentage uses `100 × numerator / denominator`.
A selected identity is a present `KEEP` or `KEEP_SECTIONS` identity with current selection bindings.
A current receipt requires matching input fingerprints and current output hashes.
An output-linked receipt must also name at least one canonical output.
That output relationship does not prove complete source-clause coverage.

| Measure | Numerator / denominator | Result | Meaning and limit |
| --- | ---: | ---: | --- |
| Current collection presence | 1,213 / 1,213 | 100.00% | Registered source identities are present; retained hashes match. |
| Non-held selection dispositions | 1,169 / 1,213 | 96.37% | Metadata dispositions exist; semantic filtering can still be incomplete. |
| Current selected processing receipts | 159 / 622 | 25.56% | Includes 20 selected zero-output dispositions. |
| Current selected output-linked receipts | 139 / 622 | 22.35% | Structural source-to-canonical processing measure. |
| Selected sources with exact canonical citations | 589 / 622 | 94.69% | Exact resource, revision and original hash match. |
| Distinct selected original hashes with exact citations | 518 / 549 | 94.35% | Deduplicates original bytes; does not deduplicate business decisions. |
| Latest two exports: selected output-linked receipts | 77 / 520 | 14.81% | Cash and RATAN exports only. |
| Latest two exports: selected processing receipts | 97 / 520 | 18.65% | Includes selected zero-output dispositions. |
| Latest two exports: exact selected citations | 489 / 520 | 94.04% | Citation reach only. |
| Complete semantic conversion | unknown / unknown | UNKNOWN | Samples demonstrate omissions; no complete clause denominator exists. |

`117/1073` is not a conversion rate. Canonical topics and source identities measure different units.
Citation reach, receipt acceptance, semantic preservation and publication remain separate facts.

## Collection coverage

| Collection | Identities | Distinct original hashes | Selected | EXCLUDE | EVIDENCE_ONLY | HOLD |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Cash Settlement | 884 | 763 | 442 | 150 | 253 | 39 |
| RATAN | 189 | 182 | 78 | 25 | 83 | 3 |
| Portal | 85 | 85 | 61 | 12 | 11 | 1 |
| Historical Settlement | 55 | 55 | 41 | 2 | 11 | 1 |
| All collections | 1,213 | 1,030 | 622 | 189 | 358 | 44 |

Distinct-hash totals are deduplicated across collections. Individual collection hash counts must not be added to obtain the global total.
The selected total includes 79 `KEEP` and 543 `KEEP_SECTIONS` identities.
The latest two exports contain 1,073 identities and 944 distinct original hashes.
They contain 520 selected identities, 425 queued identities and 42 holds.
Across all collections, selected content has 549 distinct original hashes.

All current collection originals are retained and present. No stale selection binding or missing current snapshot was found.
Four source verifiers returned exit 1 with `NEEDS_REVIEW`. The 44 holds explain these expected outcomes.
Their zero binding findings do not establish complete semantic selection.

The wider manifest contains 1,633 distinct resource/revision/hash tuples and 1,398 distinct content hashes.
Its rows comprise 1,213 current collection identities, 17 historical removed Portal rows, 195 Git rows and 208 other evidence rows.
There are 1,594 present snapshot references and 39 explicitly removed historical snapshot references.
Those historical removals do not mean 39 current collection sources are missing.

## Current receipts and remaining work

| Collection | Selected denominator | Current selected receipts | Current selected output-linked receipts | Exact selected citations | Queued | Held |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Cash Settlement | 442 | 51 | 40 | 422 | 393 | 39 |
| RATAN | 78 | 46 | 37 | 67 | 32 | 3 |
| Portal | 61 | 61 | 61 | 61 | 0 | 1 |
| Historical Settlement | 41 | 1 | 1 | 39 | 40 | 1 |
| All collections | 622 | 159 | 139 | 589 | 465 | 44 |

The ledgers contain 235 historical receipts. Independent recalculation finds 179 current receipts and 56 reopened identities.
Current receipts comprise 139 selected output-linked receipts, 20 selected zero-output receipts and 20 non-selected receipts.
A zero-output receipt is not automatically defective. The semantic sample confirms two specific defective dispositions.

The queue contains 409 never-completed identities and 56 identities with changed inputs or dependencies.
Thirty-two reopened identities also have changed or missing outputs. Those reason counts overlap.
The 465 queued identities comprise 463 selected identities and two exclusions with dependent canonical claims.
The 44 held identities form a separate review queue.

Thirty-three selected identities lack exact direct citations. Twelve are queued; twenty have accepted zero-output receipts.
One remaining identity has receipt outputs without a direct source citation.
Current receipts link 66 of 117 canonical records. Fifty-one records lack current receipt linkage.
All 117 records have exact valid manifest citations. Missing receipt linkage does not establish a provenance orphan.

The recorded review union contains 161 distinct collection/source-ID/revision identities and 159 distinct original hashes.
It comprises 136 checkpoint-219 identities, two later single cases, eleven control cases and twelve interface cases.
Its 20 excluded or evidence-only identities cannot count as domain conversions.
Checkpoint 225 refreshed 103 prior receipts. Checkpoint 178 refreshed 44 prior receipts.
These refreshes do not establish 147 newly read documents.

## Canonical governance and wiki integrity

| Measure | Numerator / denominator | Result | Limit |
| --- | ---: | ---: | --- |
| Current candidate records | 117 / 117 | 100.00% | All remain `candidate` and `draft`. |
| Current exact-byte audit bindings | 114 / 117 | 97.44% | Three current byte sets lack matching events. |
| Current audit-linked semantic-review evidence | 109 / 117 | 93.16% | Five additional matching events lack explicit semantic-review locators. |
| Current narrative review at some layer | 117 / 117 | 100.00% | Eight supplemental wiki comparisons have narrower governance scope. |
| Source declarations matching manifest tuples | 717 / 717 | 100.00% | Nine deliberately retired empty sources lack physical snapshots. |
| Present physical source declarations | 708 / 717 | 98.74% | Historical retirement remains explicit. |
| Current candidate-to-wiki input bindings | 117 / 117 | 100.00% | Both aliases, recipe and completion bindings match. |
| Current reviewed wiki output hashes | 208 / 208 | 100.00% | Hash integrity does not establish complete semantic preservation. |
| Current human publication approvals | 0 / 117 | 0.00% | No human approval inferred. |
| Published records | 0 / 117 | 0.00% | Publication remains separate from conversion work. |

There are 119 candidate Markdown files: 117 substantive records and two navigation files.
The records include 111 `KnowledgeTopic`, five `Architecture`, and one `Requirement` document.
The wiki has 117 summaries, 41 concepts, 43 entities, six explorations and one index.
Its 234 relative source aliases match all 117 current inputs. No pending wiki attempt remains.

Fresh planning under `pi-sol-medium-review-v2` reports 117 unchanged inputs.
The paired provenance files, source hashes and output hashes agree.
The latest operation reviewed three semantic source deltas and reused 114 unchanged sources and 205 unchanged outputs.
Shared completion timestamps reflect receipt assembly. They do not establish 117 new semantic reviews.

Workspace validation reports `VALID`: 119 documents and zero findings.
The current sealed harness check passes using the original checkpoint-224 baseline, plan and seal.
It checks 119 selected documents, 2,238 links and 1,886 line fragments.
Fresh wiki verification and native structural checks pass. Selected local paths and fragments have no findings.
These checks permit candidate governance gaps and cannot establish complete intent preservation.

No unsupported universal current-behavior claim was confirmed in the inspected semantic sample.
Historical measurements and implementation observations remain qualified within its inspected scope.
Uninspected claims remain outside that conclusion.
Consumer discovery is incomplete: catalog, citation and ownership metadata cannot establish actual implementation consumers or runtime use.

The graph has 201 expected nodes and 1,716 edges, without missing or extra nodes.
Its static metadata matches the inspected catalog. Node presence does not establish semantic freshness.

## Ranked findings and consequences

Every listed owner is `unknown`. Proposed actions require later remediation authorization.
These findings establish no production failure or automatic release hold.

| Priority | Finding and exact evidence | Consequence | Next action |
| --- | --- | --- | --- |
| MEDIUM | **SRC-F01:** source sample S17, original lines 22–25, current zero-output receipt. | Four draft RATAN form principles disappear from canonical retrieval. | Preserve rendering completion, validation at both layers, disabled-field validation and central rule maintenance as qualified draft intent. |
| MEDIUM | **SRC-F02:** source sample S18, original lines 27–30, current zero-output receipt. | Notification reconnection, blocking-error, JWT-header and entitlement-filtering conditions disappear. | Capture the selected draft rules; keep current policy approval unresolved. |
| MEDIUM | **CW-01:** current hashes for `ARC-portal-service-relationships` v1, `REQ-active-session-renewal` v9 and `KT-ces-migration-parity` v6. | Three current byte sets lack matching immutable audit events. | Review exact bytes and append truthful events through authorized governance. |
| LOW | **CW-02:** five audit events lack explicit semantic-review locators. | Later wiki narrative reviews cannot establish original-source canonical review. | Locate the actual reviews; preserve existing events and their limits. |
| LOW | **SRC-F03:** source sample S04, 2025 Target selection. | A whole-page evidence-only disposition may omit qualified historical capability intent. | Review mixed sections and cross-source coverage before selecting a disposition. |
| LOW | **SRC-F04:** source sample S01, original preview inventories and canonical `WF-CF-048`. | Canonical-only retrieval cannot reconstruct exact preview fields. | Assess consumer needs and preserve exact field names if required. |
| LOW | **CW-03:** RFI summary versus canonical `L3-NOSTRO-07`, original lines 12–42. | Standalone summary omits economic fallback, cashflow/trade scope and the KRW-only MT210 condition. | Review a concise scope addition or an explicit amendment/manual-scope link. |
| LOW | **CW-04 / WF-01:** saved source status versus fresh 117-input wiki plan. | A resumed coordinator can repeat completed work. | Use current hashes and this diagnostic; keep old handoffs as history. |
| LOW | **WF-02 / WF-03:** old cohort inventory, private ready case, retries and event gaps. | Planning and elapsed time can be mistaken for accepted processing. | Reconcile current plans and review concrete cases before acceptance. |

Exact evidence and hashes are retained in the [source payload](conversion-diagnostic-20261117-source-evidence.json), [canonical/wiki payload](conversion-diagnostic-20261117-workflow-canonical-wiki-evidence.json), and [workflow facts](conversion-diagnostic-20261117-workflow-facts.json).

Broad wiki ownership is a further metadata limit, `CW-05`.
There are 116 multi-owner summaries among 117 summaries. The auto-netting summary declares 13 owners, including Portal records.
These dependency sets cannot serve as precise claim-source citations. The audit found no resulting semantic corruption.
Use original clauses and native canonical links when answering knowledge questions.

The source sample identified no unsafe byte-duplicate or empty-template exclusion in its inspected cases.
It identified one evidence-only roadmap disposition requiring renewed review.
Unsafe exclusion across the remaining corpus remains unmeasured.

## Semantic samples

The source auditor read 19 distinct originals across all four collections.
Its purposive strata include selected, excluded, evidence-only, held, accepted and dependency-reopened sources.
Two cases confirm omitted selected draft intent. One roadmap case needs selection review; one case shows preview-detail compression.
This sample does not support a population error rate.

The canonical/wiki auditor compared selected clauses across 16 of 117 records, or 13.68% of records.
Results were 15 PASS, one PARTIAL and zero FAIL for those inspected comparisons.
The sample pass fraction is `15/16 = 93.75%`. It is not whole-corpus semantic accuracy.
Its partial case is the RFI summary. The canonical record retains the omitted conditions.

Passing cases preserve Day 2 versus Korea accounting differences, Murex status conflicts, SSI alternatives and regional limits.
They also preserve pipeline predicates, interface ACK/NACK distinctions, legacy identity scope and qualified reported observations.
The two samples have different units and can overlap. Their counts must not be added into a combined accuracy percentage.

## Workflow, throughput and remaining duration

The workflow audit inventoried 508 direct artifacts across checkpoints 178–225.
It inspected 22 finalization summaries and reopened 20 referenced canonical final-check results. All 20 report `PASSED`.
The two wiki finalizations have separate bridge evidence.
Preserved rejected completions, preparation findings and event drafts demonstrate actual failures before later acceptance.

The document lane prepared 23 cohorts against an earlier 477-identity queue. The current queue is 465.
Its saved status records one unreviewed ready case and zero accepted reused cases.
The held-document lane records one limited case, zero full-content reviews and zero resolved proposals.
Saved statuses do not prove live activity. Conversion workers are paused, waiting or holding private proposals during this diagnostic.

Both Luna sessions contain approximately nine-hour recorded-event gaps.
The document gap is 33,000.385 seconds. The held-document gap is 32,969.716 seconds.
Recorded tool errors and retry runs remain separate from accepted cases.
The cohort retry console records four terminal errors without a successful final result.
The earlier broad document console lacks a terminal completion. A later narrow run saved the private proposal.

A bounded receipt-integration interval accepted 25 additional distinct identities over 0.5232194202777778 hours.
Its rate is `25 / 0.5232194202777778 = 47.78 identities/hour`.
Reviews can predate this interval. This rate measures receipt integration, not original-document semantic reading.
No reliable completion ETA follows from these mixed intervals, variable source sizes and dependency refreshes.
The inspected prior handoff already states that no defensible whole-run ETA exists.

Runtime inspection explains queue reversals through direct citations, reverse dependents and forward dependency hashes.
Navigation files are hashed but do not create topic dependency edges.
Checkpoint 179 rejected an undeclared changed index in completion outputs. That is completion membership coupling.
It does not establish that every navigation link expands the dependency graph.
No runtime changes were made.

## Questions, storage and next actions

The reviewed owner-bundle tables contain 310 distinct row IDs with blank answers.
The historical register contains 987 exact-text rows from 1,527 occurrences.
Checkpoint 220 maps 108 proposals to existing topics: 103 summary proposals and five domain proposals.
These counts overlap. None is a count of independent business decisions.
The 28 earlier held-review groups remain separate from the 44 current held identities.
Existing answers and IDs remain unchanged. No new owner question was required for these diagnostic findings.

At the workflow snapshot, `.workbench/pi/` contained 118,728,099 bytes across 134 files.
It contained 25 exact duplicate files, representing 1,888 extra bytes.
Task evidence contained 19,820,654 bytes across 1,113 files, with 90 duplicate files and 403,275 extra bytes.
Four conversion session files total 12,218,233 bytes. Nine console files total 85,247,523 bytes.
Session and console groups contain no identical whole-file duplicates. Streaming records can still repeat information.
The diagnostic performed no cleanup. These measurements do not authorize deletion.

Agents can review the omitted drafts, investigate selection compression and reconcile canonical review/audit gaps.
They can also reconcile the current queue and review the existing private case after conversion resumes.
Owners must supply only material unresolved authority, missing artifacts and policy decisions through the existing annex.
Required human publication review remains separate. Zero publications does not make all 465 queued identities owner-blocked.

## Wiki handoff correction and Git boundary

Saved source status reports two stale wiki inputs. The old living report reports three pending refreshes.
Fresh planning and exact hashes establish that all three affected summaries are refreshed and all 117 bindings are current.
Six wiki paths remain uncommitted: both provenance files, the log and three summaries.
The verified refresh therefore exists in this worktree but is absent from the committed wiki baseline.
This diagnostic preserves those files and does not stage them.
The assigned conversion owner must handle their separate reviewed commit.

The catalog and receipt stage is already committed as `f535f0196`.
This report corrects the living record's stale current status while preserving historical checkpoint sections.
The diagnostic commit contains only exact diagnostic artifacts, the preserved request and the living-record update.
No push is authorized or performed.

## Checks and writing review

Actual source checks: four fresh plans, four source verifiers and independent receipt fingerprint recalculation.
Actual canonical/wiki checks: workspace validation, sealed harness check, fresh wiki plan, verification, structure and selected reference checks.
Report checks parse JSON, check local Markdown targets, verify artifact hashes and compare protected file membership and hashes.
They also check scoped and staged Git whitespace. Broad runtime tests were not run for this report-only task.
Automated checks cannot certify complete ASD-STE100 compliance or full semantic coverage.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not establish complete writing review.
  - Semantic samples do not establish whole-corpus conversion coverage.
```
