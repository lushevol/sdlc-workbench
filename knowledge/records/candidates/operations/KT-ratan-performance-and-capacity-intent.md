---
{
  "type": "KnowledgeTopic",
  "id": "KT-ratan-performance-and-capacity-intent",
  "version": 1,
  "owner": "unknown",
  "governance_state": "candidate",
  "status": "draft",
  "sources": [
    {
      "id": "SRC-e7bdeb62a9f252e67fd72554",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/FMRP China Cash Settlement Delivery Plan/Cash Settlement RATAN ONE 2025 Release Plan/Release On 2025-01-22 --- fix cashflow dashboard performance issue/page.md",
      "revision": "sha256:3b2b31332a0dcf7561659dbb359c5220f690971ba83ff127601d38448456bde5",
      "sha256": "3b2b31332a0dcf7561659dbb359c5220f690971ba83ff127601d38448456bde5",
      "snapshot": "knowledge/evidence/sources/sha256/3b2b31332a0dcf7561659dbb359c5220f690971ba83ff127601d38448456bde5.md"
    },
    {
      "id": "SRC-767f272c36d0f766c4bd57ab",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/FMRP China Cash Settlement Delivery Plan/Cash Settlement RATAN ONE 2026 Release Plan/Release On 2026-03-28 CR    RATAN Settlement Uber FXU Go-Live/RATAN One Settlement - Performance Test For Uber FXU Go-Live/1. Test Plan/page.md",
      "revision": "sha256:981637c57f4daa20684d179fcd28eac041f9e315a06b7b0a22c53395b0673f03",
      "sha256": "981637c57f4daa20684d179fcd28eac041f9e315a06b7b0a22c53395b0673f03",
      "snapshot": "knowledge/evidence/sources/sha256/981637c57f4daa20684d179fcd28eac041f9e315a06b7b0a22c53395b0673f03.md"
    },
    {
      "id": "SRC-39945535412e6176ea6613e0",
      "resource": "source:ratan-51358/RATAN - 51358/RATAN -Capacity/page.md",
      "revision": "sha256:51ee793f59a1db606970bf6df3627151d7b09f2a48da68a6c291a64e99f3f273",
      "sha256": "51ee793f59a1db606970bf6df3627151d7b09f2a48da68a6c291a64e99f3f273",
      "snapshot": "knowledge/evidence/sources/sha256/51ee793f59a1db606970bf6df3627151d7b09f2a48da68a6c291a64e99f3f273.md"
    }
  ],
  "generated": {
    "by": "agent:codex/sol_cn_workflow_review",
    "at": "2026-11-16T01:10:12.691356+00:00"
  },
  "verified": [],
  "classification": "operations",
  "scope": "RATAN performance and capacity intent",
  "summary": "The January 2025 dashboard release records 24x7 availability and five-second average API latency under normal load.",
  "related": [],
  "open_questions": [
    "Which effective environment, workload, time unit, percentile, latency metric, and acceptance authority govern each retained target?",
    "Which baseline and retained execution results establish capacity and performance after the architecture change?"
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
# RATAN performance and capacity intent

> **PROPOSED candidate:** Retained source intent awaits authority and current-applicability confirmation.

## Scope

RATAN performance and capacity intent. This candidate retains the source-specific conditions and applicability limits below.

## Summary

The January 2025 dashboard release records 24x7 availability and five-second average API latency under normal load.

## Documented knowledge

### Dated dashboard NFR

The January 2025 dashboard release records 24x7 availability and five-second average API latency under normal load. It lists 50 concurrent users, 23,769 concurrent requests per hour, and a sustained-load test at one-times load. The asterisks remain unexplained. These figures describe that source scope.

[Source 12, lines 21-29](../../../../knowledge/evidence/sources/sha256/3b2b31332a0dcf7561659dbb359c5220f690971ba83ff127601d38448456bde5.md#L21-L29)

### Capacity workload assumptions and test levels

The capacity table explicitly labels peak volume as an assumption. It lists 19,396 Settlement, 10,927 Trade intraday, and 58,713 Trade EOD. Its heading leaves the hourly-versus-minute unit unresolved. The performance-standard row uses four-times Settlement and Trade intraday load, and two-times Trade EOD load. It gives 77,584 Settlement, 43,708 Trade intraday, and 117,426 Trade EOD transactions per hour. It also gives 412 concurrent users at four-times load. The heading says four-times hourly volume, although the EOD row uses two-times. These source-listed workload assumptions and test levels require current owner confirmation. They establish no measured capacity or passing execution.

[Workload assumptions and test levels](../../../../knowledge/evidence/sources/sha256/51ee793f59a1db606970bf6df3627151d7b09f2a48da68a6c291a64e99f3f273.md#L21-L23)

### Distinct latency scope

The capacity table gives cashflow-blotter loading a five-second maximum and two-second average. The January 2025 dashboard NFR gives five-second average API latency under normal load. These measurements have different labels and cannot establish one universal latency target.

[Source 50, lines 24-24](../../../../knowledge/evidence/sources/sha256/51ee793f59a1db606970bf6df3627151d7b09f2a48da68a6c291a64e99f3f273.md#L24-L24) [Source 12, lines 25-26](../../../../knowledge/evidence/sources/sha256/3b2b31332a0dcf7561659dbb359c5220f690971ba83ff127601d38448456bde5.md#L25-L26)

### Architecture test purpose and acceptance

The architecture test plan calls for platform performance testing before a deployment-architecture change reaches production. It requires assessment of service capability after microservice orchestration and configuration changes. Acceptance preserves pre-upgrade service capability where a baseline exists, or relies on key-stakeholder belief that business requirements are met. This alternative is the retained proposal; it establishes no stakeholder approval.

[Source 17, lines 9-30](../../../../knowledge/evidence/sources/sha256/981637c57f4daa20684d179fcd28eac041f9e315a06b7b0a22c53395b0673f03.md#L9-L30)

### Planned cases and execution method

The plan covers peak-load, endurance, and stress tests at 200%, 400%, 600%, and 800%, until performance targets fail. Volumes refer to a separate NFR document. Cases cover settlement Murex, Stella, suspended flows and BAU new; Trade Control Murex and FMRP; and FMO GUI. Cases run in parallel. Python generates backend traffic, mainly Kafka; JMeter simulates core APIs. Central Monitoring and ELK monitor execution. Increase load gradually from one-times to higher multiples, then clean test data and reset the environment. The retained plan contains no execution outcomes.

[Source 17, lines 19-30](../../../../knowledge/evidence/sources/sha256/981637c57f4daa20684d179fcd28eac041f9e315a06b7b0a22c53395b0673f03.md#L19-L30) [Source 17, lines 32-36](../../../../knowledge/evidence/sources/sha256/981637c57f4daa20684d179fcd28eac041f9e315a06b7b0a22c53395b0673f03.md#L32-L36) [Source 17, lines 73-83](../../../../knowledge/evidence/sources/sha256/981637c57f4daa20684d179fcd28eac041f9e315a06b7b0a22c53395b0673f03.md#L73-L83) [Source 17, lines 85-95](../../../../knowledge/evidence/sources/sha256/981637c57f4daa20684d179fcd28eac041f9e315a06b7b0a22c53395b0673f03.md#L85-L95)

## Connections

Capacity targets connect to workload definitions and planned backend, API, and GUI cases, as scoped above.

## Evidence limits

This candidate records selected source meaning. It establishes no execution, deployment, current policy, or human approval.

## Open questions

- Which effective environment, workload, time unit, percentile, latency metric, and acceptance authority govern each retained target?
- Which baseline and retained execution results establish capacity and performance after the architecture change?
