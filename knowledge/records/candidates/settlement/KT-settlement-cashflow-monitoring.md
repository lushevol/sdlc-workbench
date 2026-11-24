---
type: KnowledgeTopic
id: KT-settlement-cashflow-monitoring
version: 2
owner: unknown
governance_state: candidate
status: draft
sources:
- id: SRC-713f1c4ad8de46361b74800b
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Grouping Blotter Monitoring/page.md
  revision: sha256:0b01a5cff3f22789e716a4f313d6c99ef4ca95934eeb3357d1f536711f1fa3d7
  sha256: 0b01a5cff3f22789e716a4f313d6c99ef4ca95934eeb3357d1f536711f1fa3d7
  snapshot: knowledge/evidence/sources/sha256/0b01a5cff3f22789e716a4f313d6c99ef4ca95934eeb3357d1f536711f1fa3d7.md
- id: SRC-ca7e3edc7111e978313c158a
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/KTLO Requirement/9244099-Add timer Dashboard exceptions/page.md
  revision: sha256:1bbc8f746200553d7c3b7ba8cf6bb0d8f249f17cd2e28219793d64b9f13c2504
  sha256: 1bbc8f746200553d7c3b7ba8cf6bb0d8f249f17cd2e28219793d64b9f13c2504
  snapshot: knowledge/evidence/sources/sha256/1bbc8f746200553d7c3b7ba8cf6bb0d8f249f17cd2e28219793d64b9f13c2504.md
- id: SRC-35d67fec74236455bc812343
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/RATAN Cashflow Dashboard/page.md
  revision: sha256:874cbc9010d6d423b2e0a5be226815e592b5bc361c083a844f95d598b2c2f255
  sha256: 874cbc9010d6d423b2e0a5be226815e592b5bc361c083a844f95d598b2c2f255
  snapshot: knowledge/evidence/sources/sha256/874cbc9010d6d423b2e0a5be226815e592b5bc361c083a844f95d598b2c2f255.md
generated:
  by: agent:sol_complete_sources
  at: '2026-11-16T08:15:07.668955+00:00'
verified: []
classification: settlement
scope: Cashflow counters, group investigation, search dimensions, and the proposed
  exception timer.
summary: Use categorized dashboard counters to investigate settlement exceptions and
  incomplete or unvalidated groups.
related:
- KT-settlement-monitoring-and-touchpoints
- KT-settlement-trade-validation-and-confirmation
- KT-settlement-event-sequencing
open_questions:
- What are the Queued, Hold, and Group Pending Validation counter predicates?
- Which local date, timezone, and five-minute timer boundaries apply?
- Which entity and country dropdown mappings govern the dashboard?
standard: ASD-STE100
automated_check: PASSED
asd_review: PENDING
reviewer: null
reviewed_at: null
limitations:
- Automated checks do not establish complete writing review.
- Authority, applicability, and human publication review remain pending.
previous_version: 1
previous_content_sha256: 02e679ca2841bad3764c2a7ca98ab5d79c47e7273cd4b743f1350e33d77d96e0
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# Cashflow dashboard and group monitoring

## Scope

Cashflow counters, group investigation, search dimensions, and the proposed exception timer.
These isolated proposals require canonical integration and authority review.

## Summary

Use categorized dashboard counters to investigate settlement exceptions and incomplete or unvalidated groups.
These documents describe intended responsibilities and proposals. They do not establish current implementation or deployment.

## Documented knowledge

### WF-CF-024

Dashboard Group Pending and Group Pending Validation counters open filtered Group Blotter views; original trade ID and pending reasons support missing-payment investigation.

Source status: documented design; unconfirmed current authority.
[Retained original, lines 1–11](../../../../knowledge/evidence/sources/sha256/0b01a5cff3f22789e716a4f313d6c99ef4ca95934eeb3357d1f536711f1fa3d7.md#L1-L11) [Retained original, lines 16–19](../../../../knowledge/evidence/sources/sha256/0b01a5cff3f22789e716a4f313d6c99ef4ca95934eeb3357d1f536711f1fa3d7.md#L16-L19)

Limit: No implementation, deployment, or business execution established.

### WF-CF-034

The dashboard timer proposal displays queued/pending-exception and group-pending indicators only after more than five minutes, with group validation status mapping still to confirm.

Conditions: Stuck for more than 5 minutes.

Source status: timer proposal with status scope TBC.
[Retained original, lines 1–7](../../../../knowledge/evidence/sources/sha256/1bbc8f746200553d7c3b7ba8cf6bb0d8f249f17cd2e28219793d64b9f13c2504.md#L1-L7)

Limit: The Group Pending row includes a to-be-confirmed group trade-validation mapping.

### WF-CF-063

The dashboard design filters by country/entity/client type/status/sub-status and defines categorized counters for waiting/failed today, future-window errors, accounting errors, SWIFT errors, and group states.

Conditions: Error window is Current Date through Current Date +7D. Accounting Error lists SENT, DISABLED, HOLDING, REJECTED, MISSING_INFO. SWIFT Error lists AMH Error, FMSGW Error, FMSRE Error, MX Generation Error, Ratan Internal Error, SCPAY Error.

Source status: documented design; unconfirmed current authority.
[Retained original, lines 3–3](../../../../knowledge/evidence/sources/sha256/874cbc9010d6d423b2e0a5be226815e592b5bc361c083a844f95d598b2c2f255.md#L3-L3) [Retained original, lines 13–15](../../../../knowledge/evidence/sources/sha256/874cbc9010d6d423b2e0a5be226815e592b5bc361c083a844f95d598b2c2f255.md#L13-L15) [Retained original, lines 19–22](../../../../knowledge/evidence/sources/sha256/874cbc9010d6d423b2e0a5be226815e592b5bc361c083a844f95d598b2c2f255.md#L19-L22) [Retained original, lines 24–36](../../../../knowledge/evidence/sources/sha256/874cbc9010d6d423b2e0a5be226815e592b5bc361c083a844f95d598b2c2f255.md#L24-L36)

Limit: Queued and Hold counter predicates are blank; local date/timezone and Group Pending Validation definition are unprovided.

### Counter predicates and investigation context

Waiting VD Today requires state WAITING and payment date equal to Current Date.
Failed VD Today requires FAILED and the same date equality.
Error requires state Error and payment date within the inclusive Current Date through Current Date+7D window.
Accounting Error uses SENT, DISABLED, HOLDING, REJECTED or MISSING_INFO.
Swift Error uses AMH Error, FMSGW Error, FMSRE Error, MX Generation Error, Ratan Internal Error or SCPAY Error.
Group Pending uses group state PENDING; Group Error uses ERROR.
Queued and Hold predicates are blank.
Search dropdown values for entity, client type and status depend on the source's frontend scope lists; no complete inventory is supplied.
[Counter predicates](../../../../knowledge/evidence/sources/sha256/874cbc9010d6d423b2e0a5be226815e592b5bc361c083a844f95d598b2c2f255.md#L28-L36)
[Search scope](../../../../knowledge/evidence/sources/sha256/874cbc9010d6d423b2e0a5be226815e592b5bc361c083a844f95d598b2c2f255.md#L19-L22)

Group monitoring distinguishes incomplete feeding from pending trade validation.
The source includes next-batch payments and Murex-workflow delays, or a market event awaiting MO validation/trade-ID synchronization.
Original trade ID and pending reasons identify missing group payments.
Pending Validation opens a Pending Trade Validation view and directs attention to near-future payment dates.
These source examples do not establish diagnosed production incidents.
[Group investigation](../../../../knowledge/evidence/sources/sha256/0b01a5cff3f22789e716a4f313d6c99ef4ca95934eeb3357d1f536711f1fa3d7.md#L1-L11)
[Pending validation](../../../../knowledge/evidence/sources/sha256/0b01a5cff3f22789e716a4f313d6c99ef4ca95934eeb3357d1f536711f1fa3d7.md#L16-L19)

### Timer proposal indicator scope

The source names separate QUEUED/pending-exception, Group Pending and Group Pending Validation indicators.
All named indicators use its stuck-for-more-than-five-minutes display condition.
The Group Pending row retains its to-be-confirmed trade-validation mapping.
[Selected original lines 1–7](../../../evidence/sources/sha256/1bbc8f746200553d7c3b7ba8cf6bb0d8f249f17cd2e28219793d64b9f13c2504.md#L1-L7)

## Connections

Related proposed or existing records: `KT-settlement-monitoring-and-touchpoints`, `KT-settlement-trade-validation-and-confirmation`, `KT-settlement-event-sequencing`.
The reconciliation file identifies integration overlaps.

## Evidence limits

Only the selected source views were read. Excluded original lines were not opened.
Linked diagrams, attachments, policies, configurations, and external destinations were not inspected.
Documented designs do not establish executed behavior or current rollout.
Source authority and current applicability remain unconfirmed.
No publication approval or business verification is recorded.

## Open questions

Owner: unknown.

- What are the Queued, Hold, and Group Pending Validation counter predicates?
- Which local date, timezone, and five-minute timer boundaries apply?
- Which entity and country dropdown mappings govern the dashboard?
