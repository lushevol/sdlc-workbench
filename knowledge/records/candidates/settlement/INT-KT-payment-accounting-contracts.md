---
type: KnowledgeTopic
id: INT-KT-payment-accounting-contracts
version: 2
owner: unknown
governance_state: candidate
status: draft
sources:
- id: SRC-a8d6b61a9af763cbeb9582c5
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Payment Accounting/Cash Settlement - Aspire Accounting/page.md
  revision: sha256:e29343b246403b331196e29dfd593b4a0c38147cd590ec13419f8929d932c771
  sha256: e29343b246403b331196e29dfd593b4a0c38147cd590ec13419f8929d932c771
- id: SRC-1a0753077e82602a1e216e29
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Payment Accounting/Cash Settlement - EBBS Accounting/page.md
  revision: sha256:cac36fca967c51ce4d6563763c74a0a88c35f4c9f6b96125dfa612a4df228a40
  sha256: cac36fca967c51ce4d6563763c74a0a88c35f4c9f6b96125dfa612a4df228a40
- id: SRC-9c84fa180c15832fc5d7410d
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Payment Accounting/Cash Settlement - Korea Accounting Recon - RATAN-
    TLM/page.md
  revision: sha256:87712fe287796fc9588a6b9f62e974c9091dceeca2640937b0e20aa0d9996967
  sha256: 87712fe287796fc9588a6b9f62e974c9091dceeca2640937b0e20aa0d9996967
- id: SRC-5be365e3ad3b6763af0a402b
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Payment Accounting/Korea Cashflow Migration -Ratan to OLTP Accounting/page.md
  revision: sha256:1023d7e0fe6af94c86f2e5ce9920a9479a6c0550921e162c490c9ce0c6bc9872
  sha256: 1023d7e0fe6af94c86f2e5ce9920a9479a6c0550921e162c490c9ce0c6bc9872
- id: SRC-ca58cfddf68e3eb32f2c3c17
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Payment Accounting/page.md
  revision: sha256:071c84ca1600030202cdd33c354093a1aa3d77cd1233646bb95be10f9bba3f97
  sha256: 071c84ca1600030202cdd33c354093a1aa3d77cd1233646bb95be10f9bba3f97
- id: SRC-bf23d68ea9b4a6a361c4eaf9
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Cash Settlement
    BAU Hand Over/page.md
  revision: sha256:f0eff734d685281a85f1c3377ae4df1cafe75b653db16decd8e1870961d1821c
  sha256: f0eff734d685281a85f1c3377ae4df1cafe75b653db16decd8e1870961d1821c
- id: SRC-a61cff86b0f7b647e754f2ff
  resource: source:ratan-51358/RATAN - 51358/RATAN -Core Function/RATAN-Settlement  8_Accounting/page.md
  revision: sha256:b6483eac46350162278f908db435d2554eda3a472b1ddaab4c931431a62e511c
  sha256: b6483eac46350162278f908db435d2554eda3a472b1ddaab4c931431a62e511c
generated:
  by: agent:codex:sol-functional-lane-3-review
  at: '2026-11-16T02:07:00.740706+00:00'
verified: []
classification: settlement
scope: Dated eBBS, Aspire, Korea OLTP, and interim TLM accounting intent; their contracts
  remain separate
summary: Selected source descriptions preserve scoped intended responsibilities. Current
  authority and applicability remain unresolved.
related:
- INT-KT-ratan-cashflow-settlement-interfaces
open_questions:
- 'KDQ-ea95a56751: Which entity/account/milestone routing matrix is authoritative,
  with effective dates?'
- 'KDQ-dc74e4402a: Which Aspire component-withdrawal accounting rule applies to Swift
  Suppressed or Failed?'
- 'KDQ-c8c1dcbb7e: Does Aspire `12 PM` mean noon or midnight, and which local timezone
  and OLA apply?'
- 'KDQ-27369af01f: Is eBBS automatic retry capped at three or at least three; what
  authorizes manual resend?'
- 'KDQ-716b15d693: How is the released resultant accounting entry selected across
  multiple versions?'
- 'KDQ-f71f76aece: Does eBBS SUCCESS display precedence apply per accounting transaction
  or only cashflow ID?'
- 'KDQ-7911026376: Is Korea OLTP intended eligibility the stated allowlist or all
  accounts except NOX UISUS/UIDD?'
- 'KDQ-669a5b8a75: Which TLM query parameters and inclusive time boundaries apply,
  and when does the interim API retire?'
- 'KDQ-fbea97b573: Who confirms the Korea no-retry contract and manual EOD recovery
  ownership?'
- 'KDQ-9858551c0a: Which dated accounting-job API contract and invocation authority
  are approved?'
- 'KDQ-4642350543: Which prior-posting or released-only withdrawal predicate governs
  the accounting overview?'
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
previous_content_sha256: fa15b1aef566c76e75a63f9ae1f450ed28c3aaabe46354f52a0b263dc53aaf8a
---
# Payment accounting contracts by destination and milestone

## Scope

Dated eBBS, Aspire, Korea OLTP, and interim TLM accounting intent; their contracts remain separate.
These source descriptions define separate contracts. They establish no deployed or tested behavior.

## Summary

The selected sources describe related responsibilities and conditions.
Their original authority, effective dates, and current applicability remain unresolved.

## Documented knowledge

### INT-ACC-01 — Aspire scope and daily files

The FMRP 2025 H1 proposal targets EOD CSV accounting through FileIT.
It names Bangkok, Taipei, OBU Taipei, SCS HK, and New York; Hong Kong is struck out in that list.
The EOD agreement includes value dates up to today and eligible states reached before `22:00` local time.
Eligible states are Release, Settled, Failed, and Swift Suppressed.
Aspire requires a file each Monday through Friday, except 25 December and 1 January.
A delayed file must still be sent when ready. Aspire must hold its later file until the earlier file reaches TLM.
The stated filename example is `RATAN_PAYMENT_TRANSACTION_TH_YYYYMMDD_01.csv`.
The source requires the Murex-compatible file format and truncation to agreed field lengths.
Unselected field mappings do not establish those lengths in this candidate.

[Selected original evidence](../../../evidence/sources/sha256/e29343b246403b331196e29dfd593b4a0c38147cd590ec13419f8929d932c771.md#L1-L53).

### INT-ACC-02 — Aspire accounting lifecycle

The source requests new entries for Release, Settled, Swift Suppressed, and Failed.
Withdrawal on Swift Suppressed or Failed components requires separate logic, which this selected text does not specify.
A released withdrawal requires reversal. Reinstate reverses immediately.
For unsuppression, a sent suppressed entry reverses after checker approval. A holding entry is disabled after maker initiation.
Un-netting reverses a sent suppressed or failed resultant. It ignores a holding resultant.
Reversal uses the latest accounting entry with the direction reversed.
New SCB-pay accounting debits Bridge and credits Nostro. New SCB-receive accounting debits Nostro and credits Bridge.
Reverse actions invert those directions.
HOLD means waiting for value date; DISABLED means reversal occurred before posting.
Aspire SUCCESS means sent to Aspire. It does not mean an external acknowledgement.
Missing mandatory data, including missing Nostro for suppressed SWIFT, produces MISSING_INFO and requires manual external correction.

[Selected original evidence](../../../evidence/sources/sha256/e29343b246403b331196e29dfd593b4a0c38147cd590ec13419f8929d932c771.md#L11-L42).

### INT-ACC-03 — Aspire file recovery limits

The support table requests batch regeneration after missing files at `22:00/22:30`, then development notification at `23:00` local time.
Its next row literally says `12 PM`, with Aspire PSS notification to hold PSGL processing.
The text does not resolve whether that label means noon or midnight.
At `03:00` local time, it stops compensation. Missing generated data goes into the next day's file with next-day filename and AsOfDate.
The required OLA, timezone, and ambiguous middle cutoff need confirmation.

[Selected original evidence](../../../evidence/sources/sha256/e29343b246403b331196e29dfd593b4a0c38147cd590ec13419f8929d932c771.md#L303-L310).

### INT-ACC-04 — eBBS dated eligibility and timing

The FMRP 2024 H1 proposal targets real-time JSON accounting through Solace for India, Singapore, Malaysia, China, and Hong Kong.
Its `2024-02-07` agreement starts value-date real-time processing at `06:00` local time.
Entries released before value date wait until that time. Entries released on value date proceed in real time.
SETTLED generates only when the same cashflow ID, event, and business version did not already generate accounting at RELEASED.
SWIFT_SUPPRESSED requires additional Nostro lookup. Missing Nostro prevents posting and exposes a failure reason for manual Oscar correction.
Manual FAILED posts on value date, reaching TLM on VD+1. Automatic failure posts at VD+1 `05:00 SGT`, reaching TLM on VD+2.
Reinstate triggers reversal; later release generates a new entry.
The status table suppresses PROJECTED, QUEUED, WAITING, READY, HOLD, CASHFLOW_SUPPRESSED, ERROR, CANCELLED, DEAD, NETTED, and NOSTROMATCH accounting.
NETTED applies to components; the resultant uses RELEASED or SETTLED.
NOSTROMATCH assumes an earlier RELEASED accounting entry.
Receipts without a SWIFT message move directly to SETTLED.
The source describes an eBBS EOD date change at `20:00` local time; next-date postings reach TLM at the next EOD.

[Selected original evidence](../../../evidence/sources/sha256/cac36fca967c51ce4d6563763c74a0a88c35f4c9f6b96125dfa612a4df228a40.md#L1-L45).

### INT-ACC-05 — eBBS reversal and component withdrawal

The eBBS event table uses the same new, reversal, reinstate, unsuppression, and un-netting distinctions described separately for Aspire.
The shared lifecycle does not make the downstream acknowledgements or retry rules equivalent.
A reversal queries the last transaction, flips C/D transaction nature, and switches the transaction codes between legs.
It generates new `id` and `external-system-key` values. Other fields inherit from the new cashflow.
For `isWithdrawalOnComponent = True` in SWIFT_SUPPRESSED or FAILED, use the released resultant's accounting entry.
Retain its Nostro and Bridge account numbers, reverse its direction and transaction-code legs, and generate other fields from the component.
The source does not specify how to select among multiple released resultant versions.

[Selected original evidence](../../../evidence/sources/sha256/cac36fca967c51ce4d6563763c74a0a88c35f4c9f6b96125dfa612a4df228a40.md#L35-L45), [Selected original evidence](../../../evidence/sources/sha256/cac36fca967c51ce4d6563763c74a0a88c35f4c9f6b96125dfa612a4df228a40.md#L207-L236).

### INT-ACC-06 — eBBS statuses retries and alerts

eBBS SENT means sent without a response. SUCCESS requires successful consumption and ACK. REJECTED records an eBBS error code.
HOLD waits for value date; DISABLED suppresses an entry reversed before posting. MISSING_INFO captures missing mandatory data.
A scheduled value-date job retries HOLD postings every one or two hours.
The exception table says to auto-resend three times for no response or `TXN9999`/`TEC0004`.
The technical-retry row instead specifies at least three attempts, three minutes apart, using the original external-system-key.
It describes a PSS retry API after a user ticket. Another row permits GUI resend for HOLD, SENT, REJECTED, and MISSING_INFO.
These entries do not establish one maximum retry count or resend authorization.
The dashboard counts T-1 through T+1 cashflows with SENT, REJECTED, or MISSING_INFO accounting.
For the same cashflow ID, SUCCESS takes display precedence over REJECTED regardless of their arrival order.
The source does not specify transaction-level precedence across separate accounting entries.

[Selected original evidence](../../../evidence/sources/sha256/cac36fca967c51ce4d6563763c74a0a88c35f4c9f6b96125dfa612a4df228a40.md#L48-L77), [Selected original evidence](../../../evidence/sources/sha256/cac36fca967c51ce4d6563763c74a0a88c35f4c9f6b96125dfa612a4df228a40.md#L238-L245).

### INT-ACC-07 — Korea interim TLM query

The proposal lets TLM query RATAN accounting already sent to OLTP, including acknowledged, rejected, and unanswered requests.
Its implicit predicate is `ratan_accounting_request_task_history.task_status = SENT`.
The maximum query span is three days. Responded accounting states are SUCCESS, SENT, and REJECTED.
HOLD waits for value date; MISSING_INFO means mandatory data is unavailable. DISABLED entries are not sent to OLTP.
The page proposes future OLTP → Aspire → TLM delivery under feature `11898201`. It does not establish retirement of the interim RATAN query.
Query fields outside the selected ranges are not inferred.

[Selected original evidence](../../../evidence/sources/sha256/87712fe287796fc9588a6b9f62e974c9091dceeca2640937b0e20aa0d9996967.md#L1-L39).

### INT-ACC-08 — Korea OLTP payment and account eligibility

The Korea proposal replaces Murex-KR accounting generation with real-time RATAN accounting for the same incoming cashflow scope.
New SCB pay increases Bridge and decreases Nostro. New SCB receive increases Nostro and decreases Bridge. Withdrawals invert those movements.
The stated accounting-state scope is Failed, Swift Suppressed, Released, and Settled.
The intended allowlist says NOS, or NOX with `KRO UIBOK` or `KRO BOKSEO`.
The payment matrix excludes NOX accounts `CCY UISUS` and `CCY UIDD` from OLTP accounting.
These internal-movement payments use TIS/OLTP UI for payment processing.
NOX `KRO UIBOK` uses TIS/OLTP UI and produces accounting.
NOX `KRO BOKSEO` requires manual SSDR query and OLTP upload, and produces accounting.
NOS `CCY MAIN`, `CCY KEBSEO`, and `CCY WRBSEO` payments use ENISIS and produce OLTP accounting.
The intended allowlist requires confirmation before it can define one current approved eligibility rule.
The owning task retains an independent gap proposal for the source-reported implementation difference.

[Selected original evidence](../../../evidence/sources/sha256/1023d7e0fe6af94c86f2e5ce9920a9479a6c0550921e162c490c9ce0c6bc9872.md#L1-L47).

### INT-ACC-09 — Korea OLTP acknowledgements and recovery

OLTP SENT means no response; SUCCESS requires OLTP ACK, not EDMI ACK. REJECTED records an OLTP error.
DISABLED applies to NOX `CCY UISUS` or `CCY UIDD` entries that must not be sent.
MISSING_INFO captures absent mandatory data. HOLD waits for value date.
The `2026-03-25` answer says no automatic retry is needed. This differs from eBBS and must remain separate.
The source records accepted processing of held entries at `06:00` local time, continuing hourly when volumes are large.
OLTP EOD interruption is `23:30–00:30 KST`. KREDMI returns an exception with the request tracking ID.
RATAN exposes the accounting error on the dashboard; KR OPS handles it in Oscar/OLTP.
A body value `Error` maps to REJECTED with reason `Can not reach to OLTP`.
The selected answers describe decisions and ownership requests, not proof that those controls ran.

[Selected original evidence](../../../evidence/sources/sha256/1023d7e0fe6af94c86f2e5ce9920a9479a6c0550921e162c490c9ce0c6bc9872.md#L18-L26), [Selected original evidence](../../../evidence/sources/sha256/1023d7e0fe6af94c86f2e5ce9920a9479a6c0550921e162c490c9ce0c6bc9872.md#L569-L575), [Selected original evidence](../../../evidence/sources/sha256/1023d7e0fe6af94c86f2e5ce9920a9479a6c0550921e162c490c9ce0c6bc9872.md#L688-L689), [Selected original evidence](../../../evidence/sources/sha256/1023d7e0fe6af94c86f2e5ce9920a9479a6c0550921e162c490c9ce0c6bc9872.md#L693), [Selected original evidence](../../../evidence/sources/sha256/1023d7e0fe6af94c86f2e5ce9920a9479a6c0550921e162c490c9ce0c6bc9872.md#L697-L698).

### INT-ACC-10 — Keystone routing context

The routing overview separates before-Keystone and after-Keystone intent.
Both stages assign CN, SG, IN, MY, AG, and UK accounting to eBBS for all Nostro accounts.
Before Keystone, HK, TW, and TH use Aspire.
After Keystone, HK Main Nostro uses eBBS and HK Suspense uses Aspire. TW and TH remain on Aspire.
This milestone matrix differs from the separate Aspire and eBBS proposal lists. It supplies no effective dates to reconcile them.

[Selected original evidence](../../../evidence/sources/sha256/071c84ca1600030202cdd33c354093a1aa3d77cd1233646bb95be10f9bba3f97.md#L6-L9).

### INT-ACC-API — Accounting-job API contracts

The BAU handover describes `POST /v1/accounting/job/accounting` with a country-array request body.
It describes `POST /v1/accounting/job/republish` with an external-system-key array.
The documented response has `country`, `totalTasks`, `failInfoMap`, and `success`.
The source labels a different schema as previous: `jobId`, `affectRows`, `exceptionRecords`, `records`, `errorMessage`, and `failInfoMap`.
These schemas remain version-specific alternatives. Their current effective version and invocation authority are not established.
Republish keys refer to cashflow identity and business/minor versions. Fixture identifiers do not define valid production keys.

[Selected original evidence](../../../evidence/sources/sha256/f0eff734d685281a85f1c3377ae4df1cafe75b653db16decd8e1870961d1821c.md#L5-L6).

### L3-ACC-SUP-01 — Separate accounting overview variant

The accounting overview assigns HK, JE, TH, and TW to EOD CSV delivery through FileIT and Aspire.
It assigns other countries to real-time JSON delivery through Solace and eBBS.
This source-specific matrix adds JE to the retained regional alternatives.
The source supplies no effective date or authority to reconcile these matrices.

[Original evidence](../../../evidence/sources/sha256/b6483eac46350162278f908db435d2554eda3a472b1ddaab4c931431a62e511c.md#L11).

### L3-ACC-SUP-02 — Withdrawal predicate conflict

The overview requests reversal when accounting was sent for the previous event.
Its event table instead limits the withdrawal reversal row to released withdrawals.
The component row requires separate logic for SWIFT_SUPPRESSED or FAILED cashflows.
These statements leave the eligible withdrawal states unresolved.
Existing destination-specific accounting contracts remain separate.

[Original evidence](../../../evidence/sources/sha256/b6483eac46350162278f908db435d2554eda3a472b1ddaab4c931431a62e511c.md#L17-L20), [Original evidence](../../../evidence/sources/sha256/b6483eac46350162278f908db435d2554eda3a472b1ddaab4c931431a62e511c.md#L29-L36).

## Connections

Related canonical IDs: `INT-KT-ratan-cashflow-settlement-interfaces`.

## Evidence limits

Source descriptions supply documented intent and historical proposals only.
They do not establish current approval, implementation, configuration, deployment, execution, or acceptance.
Unselected content and attachments were not used to fill gaps.

## Open questions

Owner: unknown. Answers remain pending in the single [task question register](../../../../tasks/workbench-knowledge-raw-import-20261113/evidence/canonical-draft-questions-20261115.md).
