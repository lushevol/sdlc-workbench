---
{
  "type": "KnowledgeTopic",
  "id": "KT-ratan-dated-migration-runbooks",
  "version": 1,
  "owner": "unknown",
  "governance_state": "candidate",
  "status": "draft",
  "sources": [
    {
      "id": "SRC-1604008d2072fda00b9093b5",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/FMRP China Cash Settlement Delivery Plan/Cash Settlement RATAN ONE 2024 Release Plan/Release On 2024-10-26 CR  CHG0577854 --- TM/page.md",
      "revision": "sha256:252e8a2f653d9a1dc080c8f36316cd11849fc0639c6ed84cf0351a3951782c95",
      "sha256": "252e8a2f653d9a1dc080c8f36316cd11849fc0639c6ed84cf0351a3951782c95",
      "snapshot": "knowledge/evidence/sources/sha256/252e8a2f653d9a1dc080c8f36316cd11849fc0639c6ed84cf0351a3951782c95.md"
    },
    {
      "id": "SRC-ec96bb301beb242b25501165",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/FMRP China Cash Settlement Delivery Plan/Cash Settlement RATAN ONE 2025 Release Plan/Release On 2025-01-19 CR  CHG0641635--- UK Business Go-Live/page.md",
      "revision": "sha256:f9f74ba761bd6f03246c3b4b35db0148fba18918006162728dbffc12074c2129",
      "sha256": "f9f74ba761bd6f03246c3b4b35db0148fba18918006162728dbffc12074c2129",
      "snapshot": "knowledge/evidence/sources/sha256/f9f74ba761bd6f03246c3b4b35db0148fba18918006162728dbffc12074c2129.md"
    }
  ],
  "generated": {
    "by": "agent:codex/sol_cn_workflow_review",
    "at": "2026-11-16T01:34:00.176708+00:00"
  },
  "verified": [],
  "classification": "operations",
  "scope": "Dated China and UK migration runbook controls",
  "summary": "The China runbook targets payment date 2024-10-28.",
  "related": [],
  "open_questions": [
    "Confirm archival-only applicability and current replacement controls.",
    "Resolve the China product list and UK execution times before any operational reuse."
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
# Dated China and UK migration runbook controls

> **PROPOSED candidate:** Retained source intent awaits authority and current-applicability confirmation.

## Scope

Dated China and UK migration runbook controls. This candidate retains the source-specific conditions and applicability limits below.

## Summary

The China runbook targets payment date 2024-10-28.

## Documented knowledge

### China October 2024 controls

The China runbook targets payment date 2024-10-28. Stella payments require an NSTP rule and no bulk eligibility. Murex payments require that date, IRS/CCS/NDF/SCF/FX taxonomy, and China 30-entity scope, with no bulk eligibility. Operations holds scoped READY payments. Operations avoids touching the 28 October payments on 24–25 October, then processes them after migration from 27 October. Murex payments should remain HOLD or WAITING pending Murex cancellation. The product list still asks for confirmation. The runbook adds temporary Murex withdrawal suppression for dates 2024-10-25 through 2024-10-28 and sends those reversals through rule checks. For 27 October, it schedules workflow/suppression changes at 09:00, go decision at 11:00, reconciliation at 18:00, and PO/Operations signoff at 19:00. The optional script and mandatory reversion stage is 20:00. If Murex payments already went out, optional scripts mark corresponding Stella payments SETTLED. The temporary suppression/workflow change must be reverted. These are dated instructions, not current suppression policy or completed execution.

[Source 8, lines 15-20](../../../../knowledge/evidence/sources/sha256/252e8a2f653d9a1dc080c8f36316cd11849fc0639c6ed84cf0351a3951782c95.md#L15-L20)

### UK January 2025 controls

The 19 January 2025 runbook schedules timeout-configuration deployment, then provides READY and SWIFT_SUPPRESSED payment lists for Operations verification. It calls for CPT-control removal. Scripts release READY payments, and unsuppress then reject SWIFT_SUPPRESSED payments. Operations verifies releases before Murex publishes future payments after value date 22 January. Several execution times remain `??`. The source does not prove completion, current script safety, or ongoing authorization.

[Source 11, lines 17-27](../../../../knowledge/evidence/sources/sha256/f9f74ba761bd6f03246c3b4b35db0148fba18918006162728dbffc12074c2129.md#L17-L27)

## Connections

The cited source clauses connect the roles, interfaces, and controls described above. Their scope remains limited to the cited revisions.

## Evidence limits

This candidate records selected source meaning. It establishes no execution, deployment, current policy, or human approval.

## Open questions

- Confirm archival-only applicability and current replacement controls.
- Resolve the China product list and UK execution times before any operational reuse.
