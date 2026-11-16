# Source conversion audit

Conversion remains partial. Exact citations cover 589 of 622 selected source identities (94.69%).
Current receipts link 139 selected identities to canonical outputs (22.35%).
These are structural rates. Neither rate establishes complete semantic coverage.
Two sampled accepted receipts omit selected draft intent.

## Scope and method

This audit covers four registered filesystem collections. It uses fresh `canonical-v1` plans and source verification results.
The audit reads original snapshots, selection metadata, receipt bindings, canonical citations, and recorded review evidence.
The sample contains 19 sources across four collections. It uses purposive strata, including omissions and reopened dependencies.
Each sample records original lines, source hashes, canonical mappings, conditions, and limits.
The audit makes no population estimate from the sample.

The launcher supplied native `magpie auto/gpt-6.1-sol medium`. Independent runtime attestation was unavailable.
No model, configuration, network, repair, completion, or publication operation ran.

## Collection census

| Collection | Registered identities | Unique original hashes | KEEP | KEEP_SECTIONS | EXCLUDE | EVIDENCE_ONLY | HOLD |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| cash-settlement-home-page | 884 | 763 | 69 | 373 | 150 | 253 | 39 |
| ratan-51358 | 189 | 182 | 0 | 78 | 25 | 83 | 3 |
| portal-document-export | 85 | 85 | 6 | 55 | 12 | 11 | 1 |
| settlement-netting | 55 | 55 | 4 | 37 | 2 | 11 | 1 |
| All collections | 1,213 | 1,030 | 79 | 543 | 189 | 358 | 44 |

All 1,213 registered files are present. All retained original hashes match.
No unknown selection state, stale selection binding, or missing original snapshot was found.
All four verification commands returned exit 1 and `NEEDS_REVIEW`. The 44 holds explain these expected outcomes.

The latest two exports contain 1,073 identities and 944 unique original hashes.
They have 520 selected identities, 425 processing items, and 42 held identities.
Their output-linked receipt rate is 77/520 (14.81%). Their exact citation rate is 489/520 (94.04%).
These denominators exclude the earlier Portal and settlement-netting collections.

## Processing and citation coverage

| Collection | Selected denominator | Exact cited selected | Current output-linked selected | All historical receipts | Current receipts | Process queue | Review queue |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| cash-settlement-home-page | 442 | 422 | 40 | 105 | 52 | 393 | 39 |
| ratan-51358 | 78 | 67 | 37 | 49 | 46 | 32 | 3 |
| portal-document-export | 61 | 61 | 61 | 80 | 80 | 0 | 1 |
| settlement-netting | 41 | 39 | 1 | 1 | 1 | 40 | 1 |
| All collections | 622 | 589 | 139 | 235 | 179 | 465 | 44 |

The selected denominator uses present `KEEP` and `KEEP_SECTIONS` identities with current selection bindings.
Current receipts require matching input fingerprints and current output hashes. Independent recalculation confirms all 179 accepted receipts.
Of these, 159 cover selected identities. Twenty selected receipts have zero outputs and do not count as domain-output conversions.
Twenty other accepted receipts cover excluded or evidence-only identities.

The process queue contains 409 never-completed identities and 56 identities with changed inputs or dependencies.
Thirty-two of those 56 also have changed or missing outputs. These reason counts overlap.
The queue includes 463 selected identities and two exclusions with dependent canonical claims.
The 44 held identities form a separate review queue.

Exact citations bind resource identity, revision, and original content hash. No canonical source tuple mismatches the source manifest.
There are 33 selected identities without exact citations. Twelve are queued; twenty have zero-output accepted receipts.
The remaining identity has linked receipt outputs without a direct citation.
Unique-content citation coverage is 518/549 selected original hashes (94.35%).

The audit finds 117 substantive canonical records and one navigation index.
All 117 records have valid manifest citations. Active collection citations reach 114 records.
Current receipts link 66 records. Fifty-one records lack current receipt linkage.
Historical receipts link 67 existing records through 68 output paths. Fifty records lack any receipt linkage.
Absent receipt linkage does not establish a provenance orphan or missing semantic content.

## Manifest reconciliation

The source manifest contains 1,633 distinct resource/revision/hash tuples.
Its rows reconcile as 1,213 current collection identities, 17 historical removed Portal rows, 195 Git-collection rows, and 208 other evidence rows.
The manifest has 1,398 unique content hashes. Repeated bytes do not mean duplicate provenance identities.
There are 1,594 present manifest snapshots and 39 explicitly removed historical snapshots.
All 17 additional Portal rows have recorded removal status.
Current collection missing-file counts remain zero.

## Review claim reconciliation

The recorded 161-review claim reconciles to 161 distinct collection/source-ID/revision identities and 159 original content hashes.
Checkpoint 219 contributes 136 identities. Checkpoints 221 and 222 each add one.
Checkpoint 223 adds eleven; checkpoint 224 adds twelve. There is no identity overlap.
All 161 currently have accepted receipts. Their retained input and referenced binding checks pass.

The union includes 141 selected identities and 20 excluded or evidence-only identities.
It therefore does not establish 161 domain conversions.
The audit reconstructs actual recorded review provenance. It does not reperform every historical semantic review.
Other receipt review assertions remain separately inventoried.

## Findings

> [!IMPORTANT]
> Accepted receipts do not establish complete intent preservation.
> Samples S17 and S18 contain selected draft rules with current zero-output receipts and no canonical representation.

| ID | Severity | Evidence | Consequence | Owner | Next action |
| --- | --- | --- | --- | --- | --- |
| SRC-F01 | MEDIUM | S17; original lines 22–25; checkpoint-175-nochange-review.json | Four RATAN form principles disappear from canonical retrieval. | unknown | Retain qualified draft principles during authorized conversion. |
| SRC-F02 | MEDIUM | S18; original lines 27–30; current receipt review | Notification reconnection and entitlement conditions disappear. | unknown | Capture draft rules separately from policy approval. |
| SRC-F03 | LOW | S04; roadmap targets and line 67; selection rationale | Mixed historical intent may be excluded as planning evidence. | unknown | Review source sections and cross-source coverage. |
| SRC-F04 | LOW | S01; original preview fields; WF-CF-048 | Canonical prose lacks exact preview field inventories. | unknown | Assess retrieval needs and preserve exact source fields. |

SRC-F01 preserves a named draft scope: RATAN UI forms.
Its rules require completed rendering, validation at both layers, validation for disabled fields, and central rule maintenance.
The prior review rejects the draft because it lacks a workflow or schema.
That rationale does not preserve its qualified intended meaning.

SRC-F02 exposes a later-phase prerequisite applied to earlier intent capture.
The prior review requires accepted security policy before representing the selected notification draft.
Missing approval prevents adoption; it does not prevent source-qualified draft capture.
No current approved notification behavior is inferred here.

SRC-F03 remains a review finding. The audit did not exhaustively reconcile every roadmap target against other sources.
SRC-F04 concerns detail compression. The original source remains accessible through its citation.
None of these findings establishes a production failure or release blocker.

## Sample results and limits

Samples S02, S06, S10, and S13 preserve the inspected source conditions in current canonical sections.
S03 confirms a byte-identical duplicate exclusion. Its paired selected identity preserves all four enhancement requirements.
S08 confirms an empty-template exclusion. S11 retains a scoped engineering proposal despite exclusion from the initial business seed.
S09 and S12 correctly hold unavailable architecture and meeting attachments.

S05 retains unresolved validation-design evidence. S14 holds workbook-dependent cases while independent design context can proceed.
Neither hold should block unrelated supported draft capture.
S15 preserves event-trigger and NSTP conditions but remains queued for its collection identity.
S16 preserves rounding constraints and conflicting accounting scopes despite a reopened dependency receipt.
S19 exposes a source-to-output link gap; full cross-source semantic loss remains unproved.

The audit read complete originals for all 19 samples. It searched relevant canonical text for missing clauses.
It did not fetch external attachments, authenticate reviewers, or infer current business approval.
Canonical governance and wiki diagnostics belong to the other diagnostic lane.
Full-workspace validation was delegated to that lane and was not run here.

## Evidence and checks

- `source-metrics.json`: formulas, denominators, collection totals, and scope limits.
- `commands.json`: actual fresh plan and verification exits.
- `snapshot-integrity.json`: original content hash checks.
- `receipt-current-checks.json`: independent receipt fingerprint checks.
- `review-161-reconciliation.json`: deduplicated review identities and actual evidence references.
- `sample-review-summary.json` and `sample-S01.json` through `sample-S19.json`: clause mappings and sample limits.
- `findings.json`: severity, evidence, consequences, owners, and proposed actions.
- `state-drift.json`: final comparison against the starting protected-data hashes.

The immediate next action is an authorized review of the two omitted draft-intent cases.
Keep current applicability, human publication review, and deployment authorization separate.

```yaml
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
  - Automated checks do not establish complete writing review.
  - Expected source hold outcomes do not mean collection readiness.
```
