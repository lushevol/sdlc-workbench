---
type: Summary
description: "Records an Uber queue-partition proposal and source-specific filter examples without claiming a passing routing test."
doc_type: short
full_text: sources/KT-ratan-uber-queue-partitioning.md
---

> **Candidate/draft only:** The topology and routing filters remain unconfirmed; retained test descriptions lack outcome evidence. Owner is unknown; `verified` is empty.

# Uber queue partitioning proposal

The source proposes replacing one Uber solution queue with eight queues by primary asset class. The selected test setup sends one source to two targets. `fx_other` filters `Source_Stack_Flow_Name` for FMRP and FMRPSTELLA; `fx_other_egnpsa` filters `Booking_Entity_SCI_FMID`. Two retained entity-filter examples use sets of three and four entities.

The selected text names test results but omits their outcomes. The retained copy does not include every routing rule or the assertion outcomes for the examples. It therefore does not establish a passing routing test, the complete eight-queue topology, a universal entity list, or current deployment. No current route was inspected. Both filter variants require confirmation against their actual queue and entity scope.

The active [[summaries/KT-platform-uber-migration-contracts]] describes competing Uber integration and compatibility proposals. It does not approve this asset-class routing design.

## Canonical sections

- [Topology and filtering](../../../records/candidates/operations/KT-ratan-uber-queue-partitioning.md#topology-and-filtering)

## Related candidate topics

- [[summaries/KT-uber-strategic-cash-settlement-p3]]

These links connect source-specific proposals. Their rules retain their separate scope and evidence limits.
