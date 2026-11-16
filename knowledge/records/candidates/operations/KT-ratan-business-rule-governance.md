---
{
  "type": "KnowledgeTopic",
  "id": "KT-ratan-business-rule-governance",
  "version": 1,
  "owner": "unknown",
  "governance_state": "candidate",
  "status": "draft",
  "sources": [
    {
      "id": "SRC-b0e2f7f0147cbec79576d6c4",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/FMRP China Cash Settlement Delivery Plan/Cash Settlement RATAN ONE 2024 Release Plan/Release On 2024-06-15 CR CHG0470053/page.md",
      "revision": "sha256:07a528db0e071ccbeb0eb89e1009c79ddba46d0b187af9e23bb84ac7dd937c5f",
      "sha256": "07a528db0e071ccbeb0eb89e1009c79ddba46d0b187af9e23bb84ac7dd937c5f",
      "snapshot": "knowledge/evidence/sources/sha256/07a528db0e071ccbeb0eb89e1009c79ddba46d0b187af9e23bb84ac7dd937c5f.md"
    },
    {
      "id": "SRC-198270cd815996bd10a57204",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Ratan One Processing Guide (DOI)/Business Rules Maintenance/page.md",
      "revision": "sha256:2f934f10867c82e727c9a32a37feb021169be4153b612499b01526a0c77359b0",
      "sha256": "2f934f10867c82e727c9a32a37feb021169be4153b612499b01526a0c77359b0",
      "snapshot": "knowledge/evidence/sources/sha256/2f934f10867c82e727c9a32a37feb021169be4153b612499b01526a0c77359b0.md"
    }
  ],
  "generated": {
    "by": "agent:codex/sol_cn_workflow_review",
    "at": "2026-11-16T01:31:00.552515+00:00"
  },
  "verified": [],
  "classification": "operations",
  "scope": "Business-rule governance and maintenance intent",
  "summary": "Strategic rule maintenance is ringfenced.",
  "related": [],
  "open_questions": [
    "Confirm the current rule approval authority, annual-review owner, and effective profiles.",
    "Confirm precedence between general maker/checker control and immediate operator activation/disable."
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
# Business-rule governance and maintenance intent

> **PROPOSED candidate:** Retained source intent awaits authority and current-applicability confirmation.

## Scope

Business-rule governance and maintenance intent. This candidate retains the source-specific conditions and applicability limits below.

## Summary

Strategic rule maintenance is ringfenced.

## Documented knowledge

### Approval and review

Strategic rule maintenance is ringfenced. Rules require maker/checker control, UAT testing, and approval before production setup. Proposals identify purpose, scope, and entity/counterparty impact. MT reviews the rule. After MT approval, eOPS requests DataOps setup. UAT amendments return to MT. Record MT approval dates in the DOI. MT or delegate reviews every rule annually; record reviewer and date. Consider payment failure, reconciliation breaks, NSTP volume, and STP effects when removing controls.

[Source 31, lines 5-10](../../../../knowledge/evidence/sources/sha256/2f934f10867c82e727c9a32a37feb021169be4153b612499b01526a0c77359b0.md#L5-L10) [Source 31, lines 14-14](../../../../knowledge/evidence/sources/sha256/2f934f10867c82e727c9a32a37feb021169be4153b612499b01526a0c77359b0.md#L14-L14) [Source 31, lines 16-21](../../../../knowledge/evidence/sources/sha256/2f934f10867c82e727c9a32a37feb021169be4153b612499b01526a0c77359b0.md#L16-L21) [Source 31, lines 82-84](../../../../knowledge/evidence/sources/sha256/2f934f10867c82e727c9a32a37feb021169be4153b612499b01526a0c77359b0.md#L82-L84)

### Rule maintenance contract

Fields form AND conditions; grouping supports complex rules. Creation requires a reason; comments are optional. New rules require checker approval, except dry-run rules. Dry-run rules do not execute immediately. Maker and checker must differ for creation and update. Authorized operators can disable live rules immediately. They can activate a live dry-run rule immediately for subsequent trade/cashflow processing. Updates require a reason and checker approval or rejection. Users can inspect history, export rules, and filter rule fields.

[Source 31, lines 69-76](../../../../knowledge/evidence/sources/sha256/2f934f10867c82e727c9a32a37feb021169be4153b612499b01526a0c77359b0.md#L69-L76)

### Rule-class scope

Cashflow suppression prevents downstream delivery and generates neither payment nor settlement accounting. Create suppression rules only when they avoid payment failure and reconciliation breaks. Addition and deletion require different maker/checker persons. Swift suppression prevents Swift/payment in Razor; listed maintenance profiles are `FMO_BR_APR`, `FMO_BR_MKR`, `FMO_OPS`, and `FMO_OPS_SUP`. These roles are source-specific and do not establish current entitlements. The source excludes legacy FX/equity rule maintenance from its strategic scope. Its China Day 1 auto-netting scope excludes that capability and requests a VD-1 enhancement.

[Source 31, lines 93-106](../../../../knowledge/evidence/sources/sha256/2f934f10867c82e727c9a32a37feb021169be4153b612499b01526a0c77359b0.md#L93-L106) [Source 31, lines 108-113](../../../../knowledge/evidence/sources/sha256/2f934f10867c82e727c9a32a37feb021169be4153b612499b01526a0c77359b0.md#L108-L113) [Source 31, lines 116-128](../../../../knowledge/evidence/sources/sha256/2f934f10867c82e727c9a32a37feb021169be4153b612499b01526a0c77359b0.md#L116-L128)

### Dated June 2024 scope

The June release list requests a `DISABLED` state and updates, China rule tiles, CurrentDate variables, and rule-engine/Hashicorp integration. It also lists the EBBS Solace consumer bridge and a LOANIQ netting-required hold before business go-live. Its development-pass labels do not prove execution or current rollout.

[Source 7, lines 28-33](../../../../knowledge/evidence/sources/sha256/07a528db0e071ccbeb0eb89e1009c79ddba46d0b187af9e23bb84ac7dd937c5f.md#L28-L33)

## Connections

The cited source clauses connect the roles, interfaces, and controls described above. Their scope remains limited to the cited revisions.

## Evidence limits

This candidate records selected source meaning. It establishes no execution, deployment, current policy, or human approval.

## Open questions

- Confirm the current rule approval authority, annual-review owner, and effective profiles.
- Confirm precedence between general maker/checker control and immediate operator activation/disable.
