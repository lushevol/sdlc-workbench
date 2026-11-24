---
{
  "type": "KnowledgeTopic",
  "id": "KT-ratan-uber-queue-partitioning",
  "version": 1,
  "owner": "unknown",
  "governance_state": "candidate",
  "status": "draft",
  "sources": [
    {
      "id": "SRC-24455f4726af8a7e85ff793d",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/RATAN - Data entitlement test cases/solace queue split test case for Uber/page.md",
      "revision": "sha256:b6cf2fd49904b08adaffca4249fd24b59d8f74aac4479aad8f8ebb28bca08443",
      "sha256": "b6cf2fd49904b08adaffca4249fd24b59d8f74aac4479aad8f8ebb28bca08443",
      "snapshot": "knowledge/evidence/sources/sha256/b6cf2fd49904b08adaffca4249fd24b59d8f74aac4479aad8f8ebb28bca08443.md"
    }
  ],
  "generated": {
    "by": "agent:codex/sol_cn_workflow_review",
    "at": "2026-11-16T01:12:00.283885+00:00"
  },
  "verified": [],
  "classification": "operations",
  "scope": "Uber queue partitioning proposal",
  "summary": "The source proposes replacing one Uber solution queue with eight queues based on primary asset class.",
  "related": [],
  "open_questions": [
    "Which approved asset-class queue topology, effective entity set, and routing assertions govern both filter variants?"
  ],
  "standard": "ASD-STE100",
  "automated_check": "PASSED",
  "asd_review": "PENDING",
  "reviewer": null,
  "reviewed_at": null,
  "limitations": [
    "Automated checks do not establish complete writing review.",
    "Retained intent does not establish current approval, execution or rollout."
  ]
}
---
# Uber queue partitioning proposal

> **PROPOSED candidate:** Retained source intent awaits authority and current-applicability confirmation.

## Scope

Uber queue partitioning proposal. This candidate retains the source-specific conditions and applicability limits below.

## Summary

The source proposes replacing one Uber solution queue with eight queues based on primary asset class.

## Documented knowledge

### Topology and filtering

The source proposes replacing one Uber solution queue with eight queues based on primary asset class. Its retained test setup sends one source to two targets. The fx_other target filters Source_Stack_Flow_Name using FMRP and FMRPSTELLA. The fx_other_egnpsa target filters Booking_Entity_SCI_FMID. Two examples use different entity-set sizes: three and four. These examples do not establish a universal entity set, complete eight-queue topology, or current deployment. The selected text names test results but omits outcome evidence; it does not establish a passing routing test.

[Source 46, lines 1-5](../../../../knowledge/evidence/sources/sha256/b6cf2fd49904b08adaffca4249fd24b59d8f74aac4479aad8f8ebb28bca08443.md#L1-L5) [Source 46, lines 24-26](../../../../knowledge/evidence/sources/sha256/b6cf2fd49904b08adaffca4249fd24b59d8f74aac4479aad8f8ebb28bca08443.md#L24-L26) [Source 46, lines 30-30](../../../../knowledge/evidence/sources/sha256/b6cf2fd49904b08adaffca4249fd24b59d8f74aac4479aad8f8ebb28bca08443.md#L30-L30) [Source 46, lines 42-42](../../../../knowledge/evidence/sources/sha256/b6cf2fd49904b08adaffca4249fd24b59d8f74aac4479aad8f8ebb28bca08443.md#L42-L42) [Source 46, lines 58-58](../../../../knowledge/evidence/sources/sha256/b6cf2fd49904b08adaffca4249fd24b59d8f74aac4479aad8f8ebb28bca08443.md#L58-L58) [Source 46, lines 70-70](../../../../knowledge/evidence/sources/sha256/b6cf2fd49904b08adaffca4249fd24b59d8f74aac4479aad8f8ebb28bca08443.md#L70-L70)

## Connections

Primary asset class connects message streams to the proposed routing filters, as scoped above.

## Evidence limits

This candidate records selected source meaning. It establishes no execution, deployment, current policy, or human approval.

## Open questions

- Which approved asset-class queue topology, effective entity set, and routing assertions govern both filter variants?
