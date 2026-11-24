---
type: KnowledgeTopic
id: KT-platform-uber-migration-contracts
version: 1
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/RATANONE
    Cash Settlement Technical Design/RATAN - Uber Integration/Cash Settlement 2.0
    Technical Design/page.md
  revision: sha256:69b9538c0f2cd59b85ca28358d8a9643156f54f7a87803935009576e0e514546
  sha256: 69b9538c0f2cd59b85ca28358d8a9643156f54f7a87803935009576e0e514546
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/RATANONE
    Cash Settlement Technical Design/RATAN - Uber Integration/RATAN - Uber Integration
    - Proposals/page.md
  revision: sha256:c05c0c6bb869071fab884d107c319ad9d77de7940086e4418c815e3aae4c803f
  sha256: c05c0c6bb869071fab884d107c319ad9d77de7940086e4418c815e3aae4c803f
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/RATANONE
    Cash Settlement Technical Design/RATAN - Uber Integration/Uber Development Testing/UBER
    regression - round 2/page.md
  revision: sha256:6242cdf08a5d22d359ce1af15baa08605002438ecc630029e24f0546bad415c4
  sha256: 6242cdf08a5d22d359ce1af15baa08605002438ecc630029e24f0546bad415c4
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/RATANONE
    Cash Settlement Technical Design/RATAN - Uber Integration/Uber Development Testing/Uber
    Dev Testing Question/page.md
  revision: sha256:c707d2349562bcff5b3245d372a169bb7bef6baa4868dbb8fa31fbfe6325f603
  sha256: c707d2349562bcff5b3245d372a169bb7bef6baa4868dbb8fa31fbfe6325f603
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/RATANONE
    Cash Settlement Technical Design/RATAN - Uber Integration/Uber Development Testing/page.md
  revision: sha256:d5334e33127aef83431732cce08c935821b8aef4ce934fced27346054b810fab
  sha256: d5334e33127aef83431732cce08c935821b8aef4ce934fced27346054b810fab
generated:
  by: agent:sol-auto-netting-review
  at: '2026-11-16T09:33:59.580339+08:00'
verified: []
scope: Historical selected-source design for platform uber migration contracts.
classification: interoperability
summary: The selected documents define historical intent and proposals. Current authority
  and applicability remain unresolved.
related: []
open_questions:
- Which migration alternative and compatibility boundary supersede the competing JSON,
  SCBML, and isolated-workflow proposals?
- Which service publishes process-in events for every action, including mixed-history
  transactional operations and SSI refresh?
- What schema-evolution rules preserve required data and default semantics across
  exact protobuf and JSON versions?
- What exact existing-caller API, response, state, timing, and regression evidence
  approves this migration?
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# Platform uber migration contracts

## Scope

Historical selected-source design for platform uber migration contracts.

## Summary

The selected documents define historical intent and proposals. Current authority and applicability remain unresolved.

## Documented knowledge

### Compatible integration alternatives

The integration proposal retains a common strategic JSON model, isolated JSON and SCBML workflows, and incremental SCBML bridging alternatives.
The isolated option preserves Murex SCBML processing.
The incremental option limits mandatory Uber/JSON changes initially to Group service and workflow extraction.
The selected document does not approve one alternative.

Sources: [original lines 1–9](../../../evidence/sources/sha256/c05c0c6bb869071fab884d107c319ad9d77de7940086e4418c815e3aae4c803f.md#L1-L9).

### Migration responsibility boundaries

The proposal assigns group management, cashflow stamping, and trade-validation control to standardization.
Lifecycle handles status movement, persistence, and validation.
Workflow handles business routing and triggers status movement.
The 2.0 proposal separately moves stamping to standardization and cutoff/materialization decisions into workflow.

These statements describe proposed boundaries, not a completed restructuring.

Sources: [original lines 11–26](../../../evidence/sources/sha256/c05c0c6bb869071fab884d107c319ad9d77de7940086e4418c815e3aae4c803f.md#L11-L26), [original lines 45–65](../../../evidence/sources/sha256/69b9538c0f2cd59b85ca28358d8a9643156f54f7a87803935009576e0e514546.md#L45-L65), [original lines 73–77](../../../evidence/sources/sha256/69b9538c0f2cd59b85ca28358d8a9643156f54f7a87803935009576e0e514546.md#L73-L77).

### Existing caller and action consistency

The low-level integration expectations request one lifecycle contract for the same action.
Rule approval, confirmation, netting, UI actions, and SSI refresh require deterministic API and topic routing.
Old and new action APIs must preserve the same externally required behavior.
The proposal explicitly identifies NetNew publication responsibilities for alignment.

The tactical options include lifecycle routing proxies and caller-visible message-type flags.
No final compatibility mechanism is selected.

Sources: [original lines 40–58](../../../evidence/sources/sha256/c05c0c6bb869071fab884d107c319ad9d77de7940086e4418c815e3aae4c803f.md#L40-L58).

### Mixed-history routing remains proposed

The later proposal assigns UI-to-lifecycle and scheduled-job workflow publication to lifecycle.
It proposes entity-based UI selection for netting and multi-exception APIs.
It treats historical SCBML cashflows in Uber entities as conversion cases.
SSI refresh uses a new orchestration subflow with legacy routing based on the status response.

Transactional operations across message types remain an explicit unresolved question.

Sources: [original lines 69–84](../../../evidence/sources/sha256/c05c0c6bb869071fab884d107c319ad9d77de7940086e4418c815e3aae4c803f.md#L69-L84).

### Lifecycle transaction and workflow proposal

The 2.0 design proposes transactional batch status and netting-identity updates for netting, unnetting, and component updates.
Net-new processing inserts new records.
It proposes data persistence after processing and permits parallel processing before persistence.
It proposes TechFail on failed precheck validation and eventual consistency for SWIFT-status writeback.

These proposals do not define an accepted mixed-version transaction contract.

Sources: [original lines 45–65](../../../evidence/sources/sha256/69b9538c0f2cd59b85ca28358d8a9643156f54f7a87803935009576e0e514546.md#L45-L65).

### Compatibility and cutover plan

The proposed phases cover Uber processing, historical and Murex SCBML compatibility, search integration, and cutover rehearsal.
The rehearsal objective requires no lost events during topic transition.
The upstream plan requires coordination with TDSX publishing and release scheduling.
These plans provide no execution or release authorization.

Sources: [original lines 28–33](../../../evidence/sources/sha256/c05c0c6bb869071fab884d107c319ad9d77de7940086e4418c815e3aae4c803f.md#L28-L33), [original lines 86–94](../../../evidence/sources/sha256/c05c0c6bb869071fab884d107c319ad9d77de7940086e4418c815e3aae4c803f.md#L86-L94).

## Connections

Relationships describe the named design responsibilities.
No uninspected canonical relationships are asserted.

## Evidence limits

Historical documents and proposals do not establish current approved behavior.
No implementation, live service, deployment, or business execution was verified.
Excluded page content and unavailable attachments remain unreviewed.

The existing KT-uber-strategic-cash-settlement-p3 version 3 was inspected as overlapping context. This supplement does not replace it.

## Open questions

Owner: unknown.

- Which migration alternative and compatibility boundary supersede the competing JSON, SCBML, and isolated-workflow proposals?
- Which service publishes process-in events for every action, including mixed-history transactional operations and SSI refresh?
- What schema-evolution rules preserve required data and default semantics across exact protobuf and JSON versions?
- What exact existing-caller API, response, state, timing, and regression evidence approves this migration?
