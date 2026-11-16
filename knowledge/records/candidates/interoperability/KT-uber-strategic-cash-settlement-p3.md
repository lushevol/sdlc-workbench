---
type: KnowledgeTopic
id: KT-uber-strategic-cash-settlement-p3
version: 3
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/RATANONE
    Cash Settlement Technical Design/RATAN - Uber Integration/EG   NP   SAU UBER Roll
    Out & FXU Business Go-Live Runbook on 04 04/page.md
  revision: sha256:d9cda0a943effd477895865bd974392c71f1659fcc06adb98429b5e86ca9b3bd
  sha256: d9cda0a943effd477895865bd974392c71f1659fcc06adb98429b5e86ca9b3bd
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/RATANONE
    Cash Settlement Technical Design/RATAN - Uber Integration/PT result for UBER/page.md
  revision: sha256:3acdfbc0f3909267b615849e63a06e04f1f72c592bc64384e097e7d629de523b
  sha256: 3acdfbc0f3909267b615849e63a06e04f1f72c592bc64384e097e7d629de523b
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/RATANONE
    Cash Settlement Technical Design/RATAN - Uber Integration/UBER Precious Metals
    Tech Design/page.md
  revision: sha256:176cf0771c92b380d06965b1348038a8ef597349f86a0ee418d6fe11df03c953
  sha256: 176cf0771c92b380d06965b1348038a8ef597349f86a0ee418d6fe11df03c953
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/RATANONE
    Cash Settlement Technical Design/RATAN - Uber Integration/Uber & FXU Technical
    Live Plan/page.md
  revision: sha256:155aeadc7dc58a689f9855947e41d18dd928906564436fe9b905d27def9c1772
  sha256: 155aeadc7dc58a689f9855947e41d18dd928906564436fe9b905d27def9c1772
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/RATANONE
    Cash Settlement Technical Design/RATAN - Uber Integration/Upstream Integration/page.md
  revision: sha256:a9814666e10116b6f0c5fda79efff5cca1631290d13bd5d5a622c0a24f7a3fea
  sha256: a9814666e10116b6f0c5fda79efff5cca1631290d13bd5d5a622c0a24f7a3fea
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/RATANONE
    Cash Settlement Technical Design/RATAN - Uber Integration/page.md
  revision: sha256:d8dadc02c466ebbafefb494647d1838ff3d60823b466a0bd7b80915ebbbeed35
  sha256: d8dadc02c466ebbafefb494647d1838ff3d60823b466a0bd7b80915ebbbeed35
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/[MB]
    Uber performance optimization/page.md
  revision: sha256:6b95e87e645bcc9e4875a09e465b49f1b2d3ec14e880056917a81bde73bf0470
  sha256: 6b95e87e645bcc9e4875a09e465b49f1b2d3ec14e880056917a81bde73bf0470
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/[Settlement
    processing optimization] Data flow segregation/page.md
  revision: sha256:44984139d5477ae4dae6bdab27be835e0937a93cc4e00835e1f2fdcd13446e50
  sha256: 44984139d5477ae4dae6bdab27be835e0937a93cc4e00835e1f2fdcd13446e50
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/[group]Analyzing
    uber msg would be deleted by wrongly in inbound table if any exception happen
    while Kafka topic consuming Uber msg/page.md
  revision: sha256:2b72709c5368b3a40b99554891d139e7936ea683a1ada3f49e5f128152b6aed1
  sha256: 2b72709c5368b3a40b99554891d139e7936ea683a1ada3f49e5f128152b6aed1
generated:
  by: agent:sol-auto-netting-review
  at: '2026-11-16T09:01:44.308554+08:00'
verified: []
classification: interoperability
scope: Historical Uber snapshot, validation, migration, recovery, performance, precious-metal,
  segregation, and cutover design.
summary: Selected designs describe Uber integration and compatibility constraints.
  Current approval and applicability remain unresolved.
related: []
open_questions:
- Which schema, field filter, entity configuration, and effective scope are currently
  approved?
- Which migration alternative and group responsibilities are approved?
- Which retry, DLT, duplicate, and query-fallback contracts apply by environment?
- What acceptance source and workload define historical compatibility and SCBML non-regression?
- Which precious-metal paths and netting keys apply by source system and portfolio,
  and what defines 26C generation?
- Which segregation alternative, partition allocation, and fallback acceptance apply?
- Which current cutover and support authority supersedes the dated plans?
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# Uber integration and strategic cash settlement

## Scope

Historical Uber snapshot, validation, migration, recovery, performance, precious-metal, segregation, and cutover design.

## Summary

Selected designs describe Uber integration and compatibility constraints. Current approval and applicability remain unresolved.

## Documented knowledge

### UBER-001: Snapshot and integration purpose

The proposal combines trade records, cashflow data, fixing notices, and change information in protobuf snapshots.
Each trade or cashflow transaction generates a snapshot.
The integration aims to improve processing and preserve historical compatibility without introducing new business requirements.

Sources: [original lines 9–24](../../../evidence/sources/sha256/d8dadc02c466ebbafefb494647d1838ff3d60823b466a0bd7b80915ebbbeed35.md#L9-L24), [original lines 63–75](../../../evidence/sources/sha256/d8dadc02c466ebbafefb494647d1838ff3d60823b466a0bd7b80915ebbbeed35.md#L63-L75), [original lines 91–94](../../../evidence/sources/sha256/d8dadc02c466ebbafefb494647d1838ff3d60823b466a0bd7b80915ebbbeed35.md#L91-L94).

### UBER-002: Event and temporal limits

The design permits non-atomic events and partial success.
An exception indicator can filter the whole message.
It proposes comparing cashflow differences and latest versions instead of trusting change flags.
It proposes timestamp and tracking-ID duplicate checks.

A missed final message needs upstream monitoring.
The design defaults optional asOf and effective query times to NOW and specifies transaction and valid-time interval boundaries.

Sources: [original lines 91–108](../../../evidence/sources/sha256/d8dadc02c466ebbafefb494647d1838ff3d60823b466a0bd7b80915ebbbeed35.md#L91-L108).

### UBER-003: Initial entity validation

The March 28 integration scope names entity FMIDs `400007847`, `401036553`, and `400991880`.
For this scope, `TDS3Data.cashflowCheckResult.passed=true` permits processing.
A false value drops the whole Uber message.
Other entities initially use a hardcoded true value.

Additional configuration is required before enabling those entities.

Sources: [original lines 1–15](../../../evidence/sources/sha256/a9814666e10116b6f0c5fda79efff5cca1631290d13bd5d5a622c0a24f7a3fea.md#L1-L15).

### UBER-004: Common model and migration alternatives

The proposed common model combines the domain model with internal fields.
The design chooses readable JSON transmission and generated protobuf models.
The bridge converts EDMI bytes to JSON and preserves the correct persistence and replay key.
Standardization identifies cashflows, validates and stamps trades, and filters `IntentToSettle=false`.

The component plan retains group and group-message tables for management and UI use.
A benefits section also says grouping logic is no longer required.
These statements do not establish removal of all group responsibilities.
The estimates retain two alternatives: common JSON processing with outbound conversion, or group conversion to SCBML.

Sources: [original lines 123–128](../../../evidence/sources/sha256/d8dadc02c466ebbafefb494647d1838ff3d60823b466a0bd7b80915ebbbeed35.md#L123-L128), [original lines 166–194](../../../evidence/sources/sha256/d8dadc02c466ebbafefb494647d1838ff3d60823b466a0bd7b80915ebbbeed35.md#L166-L194), [original lines 214–216](../../../evidence/sources/sha256/d8dadc02c466ebbafefb494647d1838ff3d60823b466a0bd7b80915ebbbeed35.md#L214-L216), [original lines 236–260](../../../evidence/sources/sha256/d8dadc02c466ebbafefb494647d1838ff3d60823b466a0bd7b80915ebbbeed35.md#L236-L260).

### UBER-005: Historical compatibility responsibilities

The SSI plan adds an UBER raw-message type, stores JSON, and parses by message type.
It classifies SSI work as a data-model change.
The lifecycle plan retains historical SCBML state compatibility and converts updated inputs to JSON.
It proposes common domain events and SCBML generation before Razor publication.

It classifies lifecycle work as restructuring.
These classifications describe separate components.

Sources: [original lines 218–219](../../../evidence/sources/sha256/d8dadc02c466ebbafefb494647d1838ff3d60823b466a0bd7b80915ebbbeed35.md#L218-L219).

### UBER-006: Field scope and ownership

The design identifies 122 supplemental RATAN fields.
Its table marks fields for retention, removal, correction, or unresolved review.
It does not supply the complete protobuf schema.
The configurable-field proposal masks unnecessary fields to reduce payload size.

Without a black or white list, it proposes publishing the entire payload; this remains marked TBD.
Applications maintain additional data outside the domain-model SDK.

Sources: [original lines 268–407](../../../evidence/sources/sha256/d8dadc02c466ebbafefb494647d1838ff3d60823b466a0bd7b80915ebbbeed35.md#L268-L407), [original lines 441–454](../../../evidence/sources/sha256/d8dadc02c466ebbafefb494647d1838ff3d60823b466a0bd7b80915ebbbeed35.md#L441-L454).

### UBER-007: Parsing and filtering proposal

The optimization proposes parsing protobuf once and reusing JSON, common fields, and exchange metadata.
It proposes compact JSON serialization and exchange JSON reuse.
It assigns Uber filtering to the group service.
The source claim that filtering already moved does not establish rollout.

Sources: [original lines 53–138](../../../evidence/sources/sha256/6b95e87e645bcc9e4875a09e465b49f1b2d3ec14e880056917a81bde73bf0470.md#L53-L138).

### UBER-008: Persistent retries and recovery

The remediation proposes five retry attempts by default.
The initial delay is 15000 milliseconds, with a multiplier of two.
Retry partitions default to three; concurrency defaults to one.
The DLT proposal saves inbound, group, and group-message records.

It compares major version and New/Withdrawal events, skips processed records, and marks eligible unprocessed records ERROR.
The earlier `deleteById` retention alternative is struck through.
A separate query comparison specifies an empty-set fallback after three retries.
ERROR records remain available for recovery.

Sources: [original lines 125–132](../../../evidence/sources/sha256/2b72709c5368b3a40b99554891d139e7936ea683a1ada3f49e5f128152b6aed1.md#L125-L132), [original lines 135–178](../../../evidence/sources/sha256/2b72709c5368b3a40b99554891d139e7936ea683a1ada3f49e5f128152b6aed1.md#L135-L178), [original lines 194–201](../../../evidence/sources/sha256/2b72709c5368b3a40b99554891d139e7936ea683a1ada3f49e5f128152b6aed1.md#L194-L201).

### UBER-009: Performance objectives

The selected objectives require no impact on existing SCBML processing.
Better Uber performance is desirable.
The test scope includes settlement STP and netting/unnetting.
This selected objective section supplies no measurable acceptance threshold.

Sources: [original lines 1–14](../../../evidence/sources/sha256/3acdfbc0f3909267b615849e63a06e04f1f72c592bc64384e097e7d629de523b.md#L1-L14).

### UBER-010: Precious-metal handling

The precious-metal design uses custodian and delivery-location fields across grouping, querying, netting, SWIFT, and rules.
It names `tradeRecord.Entity.Custodian_SCI_FMID` and `tradeRecord.Delivery_Location`.
Later field lists also use `Trade.Entity` and instrument delivery-location paths.
Murex cashflows use `Murex_Product_Strategy`.

Historical Stella cashflows use that field only for portfolio `PRC_ECOM_SPOT_STL`.
New Stella cashflows use `Trade.Entity.Custodian_SCI_FMID` and `Trade.Delivery_Location`.
Precious-metal currencies do not support splitting.
The selected 26C heading supplies no generation rule; referenced screenshots are unavailable.

Sources: [original lines 7–19](../../../evidence/sources/sha256/176cf0771c92b380d06965b1348038a8ef597349f86a0ee418d6fe11df03c953.md#L7-L19), [original lines 23–27](../../../evidence/sources/sha256/176cf0771c92b380d06965b1348038a8ef597349f86a0ee418d6fe11df03c953.md#L23-L27), [original lines 71–85](../../../evidence/sources/sha256/176cf0771c92b380d06965b1348038a8ef597349f86a0ee418d6fe11df03c953.md#L71-L85), [original lines 91–105](../../../evidence/sources/sha256/176cf0771c92b380d06965b1348038a8ef597349f86a0ee418d6fe11df03c953.md#L91-L105), [original lines 107–121](../../../evidence/sources/sha256/176cf0771c92b380d06965b1348038a8ef597349f86a0ee418d6fe11df03c953.md#L107-L121), [original lines 123–125](../../../evidence/sources/sha256/176cf0771c92b380d06965b1348038a8ef597349f86a0ee418d6fe11df03c953.md#L123-L125).

### UBER-011: Flow segregation alternatives

The segregation proposal aims to isolate country flows.
It retains country-topic and partition-group alternatives.
The partition approach changes participating producers and leaves consumers unchanged.
Scaling recalculates the allocation.

It requires fallback to the default partitioner for insufficient partitions, uncovered keys, or exceptions.
Partition groups may overlap.
Country grouping is preferred; weighting remains unresolved.
These alternatives do not establish the selected Uber architecture or a demonstrated no-loss guarantee.

Sources: [original lines 1–14](../../../evidence/sources/sha256/44984139d5477ae4dae6bdab27be835e0937a93cc4e00835e1f2fdcd13446e50.md#L1-L14), [original lines 30–70](../../../evidence/sources/sha256/44984139d5477ae4dae6bdab27be835e0937a93cc4e00835e1f2fdcd13446e50.md#L30-L70), [original lines 348–359](../../../evidence/sources/sha256/44984139d5477ae4dae6bdab27be835e0937a93cc4e00835e1f2fdcd13446e50.md#L348-L359), [original lines 383–407](../../../evidence/sources/sha256/44984139d5477ae4dae6bdab27be835e0937a93cc4e00835e1f2fdcd13446e50.md#L383-L407).

### UBER-012: Historical rollout and cutover scope

The March 28, 2026 technical-live plan scopes Uber to EG, NP, and SA, without FXU initially.
It plans FXU for April 4 and retains SCBML elsewhere.
It requires SCBML non-regression and existing-data compatibility.
It limits OpenSearch to developers and makes CES the PT default.

The April 4 runbook requires no message backlog and no pending groups before cutover.
Missing cashflows can require conditional replay.
Publisher-stop steps include withdrawn or conditional instructions.
The selected runbook also stops the bridge.

These dated plans supply no execution or deployment confirmation.

Sources: [original lines 7–15](../../../evidence/sources/sha256/155aeadc7dc58a689f9855947e41d18dd928906564436fe9b905d27def9c1772.md#L7-L15), [original lines 23–28](../../../evidence/sources/sha256/155aeadc7dc58a689f9855947e41d18dd928906564436fe9b905d27def9c1772.md#L23-L28), [original lines 32–33](../../../evidence/sources/sha256/155aeadc7dc58a689f9855947e41d18dd928906564436fe9b905d27def9c1772.md#L32-L33), [original lines 40–40](../../../evidence/sources/sha256/155aeadc7dc58a689f9855947e41d18dd928906564436fe9b905d27def9c1772.md#L40-L40), [original lines 43–45](../../../evidence/sources/sha256/155aeadc7dc58a689f9855947e41d18dd928906564436fe9b905d27def9c1772.md#L43-L45), [original lines 17–28](../../../evidence/sources/sha256/d9cda0a943effd477895865bd974392c71f1659fcc06adb98429b5e86ca9b3bd.md#L17-L28).

## Connections

The source designs connect upstream snapshots, group processing, SSI, lifecycle, and downstream publication.
No related canonical record was inspected for this review.

## Evidence limits

These are historical, source-specific candidate statements.
Current owner approval, effective policy, implementation, deployment, and executed behavior remain unverified.
The selected performance section contains objectives; excluded measurements were not reviewed.
Retry baseline and repair-result claims are source reports, without retained execution proof.
Full selected-range review does not cover excluded page content or unavailable attachments.

## Open questions

Owner: unknown.

- Which schema, field filter, entity configuration, and effective scope are currently approved?
- Which migration alternative and group responsibilities are approved?
- Which retry, DLT, duplicate, and query-fallback contracts apply by environment?
- What acceptance source and workload define historical compatibility and SCBML non-regression?
- Which precious-metal paths and netting keys apply by source system and portfolio, and what defines 26C generation?
- Which segregation alternative, partition allocation, and fallback acceptance apply?
- Which current cutover and support authority supersedes the dated plans?
