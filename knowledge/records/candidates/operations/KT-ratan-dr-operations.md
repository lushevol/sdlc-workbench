---
{
  "type": "KnowledgeTopic",
  "id": "KT-ratan-dr-operations",
  "version": 1,
  "owner": "unknown",
  "governance_state": "candidate",
  "status": "draft",
  "sources": [
    {
      "id": "SRC-c67e3f23eccd8f3ccafbe020",
      "resource": "source:ratan-51358/RATAN - 51358/RATAN -Service Restart Guide/RATAN DR Plan/page.md",
      "revision": "sha256:71a1221a8f9158a331cefec81532dc5166582899d0df6b51f97ea896ad976fa1",
      "sha256": "71a1221a8f9158a331cefec81532dc5166582899d0df6b51f97ea896ad976fa1",
      "snapshot": "knowledge/evidence/sources/sha256/71a1221a8f9158a331cefec81532dc5166582899d0df6b51f97ea896ad976fa1.md"
    }
  ],
  "generated": {
    "by": "agent:codex/sol_cn_workflow_review",
    "at": "2026-11-16T01:09:13.304630+00:00"
  },
  "verified": [],
  "classification": "operations",
  "scope": "RATAN disaster recovery coordination",
  "summary": "The runbook lists WAT-to-ARK failover and subsequent network reinstatement.",
  "related": [],
  "open_questions": [
    "Who owns the effective DR runbook and confirms current topology, schedule, infrastructure readiness, and EOD completion evidence?"
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
# RATAN disaster recovery coordination

> **PROPOSED candidate:** Retained source intent awaits authority and current-applicability confirmation.

## Scope

RATAN disaster recovery coordination. This candidate retains the source-specific conditions and applicability limits below.

## Summary

The runbook lists WAT-to-ARK failover and subsequent network reinstatement.

## Documented knowledge

### WAT to ARK

The runbook lists WAT-to-ARK failover and subsequent network reinstatement. Check completion of database, NAS, network, and VM failover through coordinated status before proceeding. Check RATAN health and report application failover completion time. After network reinstatement, check health, report verification completion time, and update the DR page.

[Source 74, lines 11-11](../../../../knowledge/evidence/sources/sha256/71a1221a8f9158a331cefec81532dc5166582899d0df6b51f97ea896ad976fa1.md#L11-L11) [Source 74, lines 17-17](../../../../knowledge/evidence/sources/sha256/71a1221a8f9158a331cefec81532dc5166582899d0df6b51f97ea896ad976fa1.md#L17-L17) [Source 74, lines 19-19](../../../../knowledge/evidence/sources/sha256/71a1221a8f9158a331cefec81532dc5166582899d0df6b51f97ea896ad976fa1.md#L19-L19)

### ARK to WAT

The return path expects RATAN active-active operation after infrastructure failover. Check health and confirm RATAN EOD status with ETL squads before reporting completion. After network reinstatement, start the A node and check health. Hold Sunday MLZ jobs when the P node is unavailable because those jobs run only there. Confirm EOD status with ETL squads, report verification completion, and update the DR page.

[Source 74, lines 24-24](../../../../knowledge/evidence/sources/sha256/71a1221a8f9158a331cefec81532dc5166582899d0df6b51f97ea896ad976fa1.md#L24-L24) [Source 74, lines 30-30](../../../../knowledge/evidence/sources/sha256/71a1221a8f9158a331cefec81532dc5166582899d0df6b51f97ea896ad976fa1.md#L30-L30) [Source 74, lines 32-32](../../../../knowledge/evidence/sources/sha256/71a1221a8f9158a331cefec81532dc5166582899d0df6b51f97ea896ad976fa1.md#L32-L32)

### Approximate timing

The runbook lists approximately 04:00 for failover and 10:05 for network reinstatement. It requires confirmation from coordinated infrastructure status. These approximate times do not establish a current schedule or completed failover.

[Source 74, lines 17-17](../../../../knowledge/evidence/sources/sha256/71a1221a8f9158a331cefec81532dc5166582899d0df6b51f97ea896ad976fa1.md#L17-L17) [Source 74, lines 19-19](../../../../knowledge/evidence/sources/sha256/71a1221a8f9158a331cefec81532dc5166582899d0df6b51f97ea896ad976fa1.md#L19-L19) [Source 74, lines 30-30](../../../../knowledge/evidence/sources/sha256/71a1221a8f9158a331cefec81532dc5166582899d0df6b51f97ea896ad976fa1.md#L30-L30) [Source 74, lines 32-32](../../../../knowledge/evidence/sources/sha256/71a1221a8f9158a331cefec81532dc5166582899d0df6b51f97ea896ad976fa1.md#L32-L32)

## Connections

Infrastructure failover connects to RATAN health checks and ETL confirmation, as scoped above.

## Evidence limits

This candidate records selected source meaning. It establishes no execution, deployment, current policy, or human approval.

## Open questions

- Who owns the effective DR runbook and confirms current topology, schedule, infrastructure readiness, and EOD completion evidence?
