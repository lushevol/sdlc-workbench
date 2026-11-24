---
type: KnowledgeTopic
id: INT-KT-indonesia-reference-data-and-rule-sync
version: 1
owner: unknown
governance_state: candidate
status: draft
sources:
- id: SRC-248b70f0222ba42a05ae124e
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/2026
    Design/Cash Settlement Platform Architecture - Indonesia/RDM API call for compensation/page.md
  revision: sha256:aa5a1f7b7419d4bed560f1a762c3e3b4df0486afc50b3646a4f950ab1e5e8ee0
  sha256: aa5a1f7b7419d4bed560f1a762c3e3b4df0486afc50b3646a4f950ab1e5e8ee0
- id: SRC-2c1c0f966037f5829e5c1d40
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/2026
    Design/Cash Settlement Platform Architecture - Indonesia/RDM API call for compensation/RDM
    Integration via Kong Gateway/page.md
  revision: sha256:9db94c45f437f3a6728954933a3fbfa4c6903098b64730207ab0d71af1065129
  sha256: 9db94c45f437f3a6728954933a3fbfa4c6903098b64730207ab0d71af1065129
- id: SRC-faaf4f1814b9a6f177c456fb
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/2026
    Design/Cash Settlement Platform Architecture - Indonesia/Rule Sync From Ratan
    GDC to Ratan ID/page.md
  revision: sha256:5e70856f60a6850bfc963c69f1e9783cbf4f3c8461f49f7d144fb109cecb77dd
  sha256: 5e70856f60a6850bfc963c69f1e9783cbf4f3c8461f49f7d144fb109cecb77dd
- id: SRC-46989640736a488b3cbf5751
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/2026
    Design/Cash Settlement Platform Architecture - Indonesia/Static Data Synchronizer/page.md
  revision: sha256:e6364619c67bb6be406fb2c6eac2e50cec770adb97b96cb1d03035e2f3f98f0c
  sha256: e6364619c67bb6be406fb2c6eac2e50cec770adb97b96cb1d03035e2f3f98f0c
generated:
  by: agent:codex:sol-integrations-review
  at: '2026-11-16T01:30:46.186769+00:00'
verified: []
classification: settlement
scope: Indonesia reference-data and rule synchronization intent
summary: Selected source descriptions preserve scoped intended responsibilities. Current
  authority and applicability remain unresolved.
related:
- INT-KT-entity-and-reference-data-design
open_questions:
- 'KDQ-bfa0a3c6e2: Which RDM reconciliation, complete pagination, date conversion,
  and timezone rules are approved for Indonesia compensation?'
- 'KDQ-24234ca879: Which versioned RDM endpoint syntax and environment table are approved,
  including the double-question-mark currency URL?'
- 'KDQ-9384a93b2e: Which rule/static synchronization contract is authoritative, including
  eligibility, timeout, IGNORE, and adapter compatibility?'
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# Indonesia reference-data and rule synchronization intent

## Scope

Indonesia reference-data and rule synchronization intent.
These source descriptions define separate contracts. They establish no deployed or tested behavior.

## Summary

The selected sources describe related responsibilities and conditions.
Their original authority, effective dates, and current applicability remain unresolved.

## Documented knowledge

### SYNC-01 — Indonesia RDM compensation choice

Indonesia cannot mount NAS for RDM files. The selected design chooses EOD API compensation over no compensation or GDC replication.
The scoped compensation covers holidays and country codes. Common rule data and BRDM LEI are outside this source-defined Indonesia need.
The selected answer defines the API date interval as `>=dateFrom,<dateTo`.
The RDM holiday key combines center_id, event_date, event_name, and file_type.
RDM changes a key through deletion; unchanged keys permit updates. The RATAN note instead prescribes insert/delete.
The exact reconciliation of those semantics remains unresolved.
Holiday paging starts at 1; country paging starts at 0, with a stated country default of 100.
The API and real-time feed use different date formats and require explicit conversion.
The schedule says after 8am IST for Indonesia and after 9am HK for GDC. IST remains undefined.
A development SSL-bypass suggestion does not establish accepted security policy. Source code-analysis tables remain task evidence.

[Selected original evidence](../../../evidence/sources/sha256/aa5a1f7b7419d4bed560f1a762c3e3b4df0486afc50b3646a4f950ab1e5e8ee0.md#L1-L7), [Selected original evidence](../../../evidence/sources/sha256/aa5a1f7b7419d4bed560f1a762c3e3b4df0486afc50b3646a4f950ab1e5e8ee0.md#L17-L40), [Selected original evidence](../../../evidence/sources/sha256/aa5a1f7b7419d4bed560f1a762c3e3b4df0486afc50b3646a4f950ab1e5e8ee0.md#L57-L85), [Selected original evidence](../../../evidence/sources/sha256/aa5a1f7b7419d4bed560f1a762c3e3b4df0486afc50b3646a4f950ab1e5e8ee0.md#L95-L97), [Selected original evidence](../../../evidence/sources/sha256/aa5a1f7b7419d4bed560f1a762c3e3b4df0486afc50b3646a4f950ab1e5e8ee0.md#L126-L132).

### SYNC-02 — RDM Kong interface distinctions

The Kong table distinguishes SIT, UAT, and PROD endpoints and three API families.
Holiday currency/weekend uses `v2/holidayCalendarCurrencyHldyWkend`; special holiday uses `v2/holidayCalendarSpecial`.
Country data uses `v1/countries`.
The literal currency URL contains two question marks. This review does not silently repair it or approve its syntax.

[Selected original evidence](../../../evidence/sources/sha256/9db94c45f437f3a6728954933a3fbfa4c6903098b64730207ab0d71af1065129.md#L15-L29).

### SYNC-03 — Rule synchronization eligibility and controls

The later rule design replaces manual checkbox selection with automatic eligibility detection.
The automatic scope uses `STRATEGIC_SETTLEMENT` and NSTP, SUPPRESSION, SWIFT_SUPPRESSION, NETTING, or AUTO_NETTING rule types.
Global rules contain neither booking-entity FMID nor FMCODE predicates. They cannot become nonglobal through editing.
GDC input prohibits Indonesia entity predicates. Global rules remain read-only in Indonesia.
Indonesia-specific rules include locked Indonesia predicates. Local manual rules/static require maker/checker control.
Proposal A copies data one-way through FM Solace. Proposal B remains a data-sharing alternative heading, without a selected complete contract.

[Selected original evidence](../../../evidence/sources/sha256/5e70856f60a6850bfc963c69f1e9783cbf4f3c8461f49f7d144fb109cecb77dd.md#L3-L18), [Selected original evidence](../../../evidence/sources/sha256/5e70856f60a6850bfc963c69f1e9783cbf4f3c8461f49f7d144fb109cecb77dd.md#L19-L28), [Selected original evidence](../../../evidence/sources/sha256/5e70856f60a6850bfc963c69f1e9783cbf4f3c8461f49f7d144fb109cecb77dd.md#L30-L35), [Selected original evidence](../../../evidence/sources/sha256/5e70856f60a6850bfc963c69f1e9783cbf4f3c8461f49f7d144fb109cecb77dd.md#L37-L53).

### SYNC-04 — Rule request lifecycle

Each rule has one latest producer sync record. Events carry unique request IDs and latest DEAD histories for parent rules.
Retries reuse the request ID and replace prior sync content. Version and history handle ordering.
Per-target statuses are SENT, ACK, NACK, FAILED, TIMEOUT, and IGNORE. The rule timeout is five minutes.
Wrong-request-ID responses are ignored. FAILED and TIMEOUT events may retry and return to SENT.
IGNORE marks superseded parent events to avoid unnecessary retry.
Manual resend uses `POST /api/ratan/v1/rule-sync/{ruleId}/resend` with a target-region array.
The source requires status and error-message visibility. It does not establish no-loss execution.

[Selected original evidence](../../../evidence/sources/sha256/5e70856f60a6850bfc963c69f1e9783cbf4f3c8461f49f7d144fb109cecb77dd.md#L59-L87), [Selected original evidence](../../../evidence/sources/sha256/5e70856f60a6850bfc963c69f1e9783cbf4f3c8461f49f7d144fb109cecb77dd.md#L326-L354), [Selected original evidence](../../../evidence/sources/sha256/5e70856f60a6850bfc963c69f1e9783cbf4f3c8461f49f7d144fb109cecb77dd.md#L356), [Selected original evidence](../../../evidence/sources/sha256/5e70856f60a6850bfc963c69f1e9783cbf4f3c8461f49f7d144fb109cecb77dd.md#L393-L408).

### SYNC-05 — Generic static synchronizer

The generic design uses a separate asynchronous service to avoid blocking the GDC main flow.
It requires observable request/response synchronization, manual resend, idempotency, and per-target status for multiple consumers.
One latest producer record carries request ID and data version. Retries reuse both values.
The generic TIMEOUT range is five to ten minutes, distinct from the rule-specific five minutes.
Generic IGNORE uses a SyncIgnoreConstraint for special IDs, distinct from superseded-parent rule semantics.
FAILED and TIMEOUT may retry. Consumers use request ID and data version for duplicate and disorder handling.
Inbound/outbound adapters permit heterogeneous data and endpoint protocols. No accepted SDK compatibility or delivery guarantee is proved.

[Selected original evidence](../../../evidence/sources/sha256/e6364619c67bb6be406fb2c6eac2e50cec770adb97b96cb1d03035e2f3f98f0c.md#L3-L31), [Selected original evidence](../../../evidence/sources/sha256/e6364619c67bb6be406fb2c6eac2e50cec770adb97b96cb1d03035e2f3f98f0c.md#L33-L67), [Selected original evidence](../../../evidence/sources/sha256/e6364619c67bb6be406fb2c6eac2e50cec770adb97b96cb1d03035e2f3f98f0c.md#L68-L129), [Selected original evidence](../../../evidence/sources/sha256/e6364619c67bb6be406fb2c6eac2e50cec770adb97b96cb1d03035e2f3f98f0c.md#L131-L134), [Selected original evidence](../../../evidence/sources/sha256/e6364619c67bb6be406fb2c6eac2e50cec770adb97b96cb1d03035e2f3f98f0c.md#L194-L198), [Selected original evidence](../../../evidence/sources/sha256/e6364619c67bb6be406fb2c6eac2e50cec770adb97b96cb1d03035e2f3f98f0c.md#L229-L231).

## Connections

Related canonical IDs: `INT-KT-entity-and-reference-data-design`.

## Evidence limits

Source descriptions supply documented intent and historical proposals only.
They do not establish current approval, implementation, configuration, deployment, execution, or acceptance.
Unselected content and attachments were not used to fill gaps.

## Open questions

Owner: unknown. Answers remain pending in the single [task question register](../../../../tasks/workbench-knowledge-raw-import-20261113/evidence/canonical-draft-questions-20261115.md).
