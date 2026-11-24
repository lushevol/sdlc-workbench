---
{
  "type": "KnowledgeTopic",
  "id": "KT-ratan-data-entitlement-and-access",
  "version": 1,
  "owner": "unknown",
  "governance_state": "candidate",
  "status": "draft",
  "sources": [
    {
      "id": "SRC-6d317e0d9d38e22ea9aebf64",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Ratan One Processing Guide (DOI)/How to apply for RATAN ONE access/page.md",
      "revision": "sha256:4a360c2affb24d4d6a18b571bb5d4f3711ac1ced5c3ec51b670e789779b9e47c",
      "sha256": "4a360c2affb24d4d6a18b571bb5d4f3711ac1ced5c3ec51b670e789779b9e47c",
      "snapshot": "knowledge/evidence/sources/sha256/4a360c2affb24d4d6a18b571bb5d4f3711ac1ced5c3ec51b670e789779b9e47c.md"
    },
    {
      "id": "SRC-ce99e06b55fa6e98d810a52f",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/RATAN - Data entitlement test cases/Copy of RATAN - Data entitlement test cases/page.md",
      "revision": "sha256:c58c1ce14bf6a320599565103521aa1719ba0c3cdc0bc3b488cb450cb203a65b",
      "sha256": "c58c1ce14bf6a320599565103521aa1719ba0c3cdc0bc3b488cb450cb203a65b",
      "snapshot": "knowledge/evidence/sources/sha256/c58c1ce14bf6a320599565103521aa1719ba0c3cdc0bc3b488cb450cb203a65b.md"
    },
    {
      "id": "SRC-523e8bdec274e3b0564b93e7",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/RATAN - Data entitlement test cases/page.md",
      "revision": "sha256:b563bc564baf6522da400243c2db038dbc1cb6468966967ab1e0d16632ba0c46",
      "sha256": "b563bc564baf6522da400243c2db038dbc1cb6468966967ab1e0d16632ba0c46",
      "snapshot": "knowledge/evidence/sources/sha256/b563bc564baf6522da400243c2db038dbc1cb6468966967ab1e0d16632ba0c46.md"
    },
    {
      "id": "SRC-c9ab3c29c66d4cd796fa7b93",
      "resource": "source:ratan-51358/RATAN - 51358/RATAN -Release/Ratan Release Plan 2026/Ratan New Onboarding Checklist 2026/2026_01_17_CHG0912552_CES onboard to MFE/page.md",
      "revision": "sha256:4b73bc29d8ebdf40ed7bdce17fbc13104db5eda14d1551410d28370c04eaadb9",
      "sha256": "4b73bc29d8ebdf40ed7bdce17fbc13104db5eda14d1551410d28370c04eaadb9",
      "snapshot": "knowledge/evidence/sources/sha256/4b73bc29d8ebdf40ed7bdce17fbc13104db5eda14d1551410d28370c04eaadb9.md"
    },
    {
      "id": "SRC-8167d17b31812d0ae19013be",
      "resource": "source:ratan-51358/RATAN - 51358/RATAN -Release/Ratan Release Plan 2026/Ratan New Onboarding Checklist 2026/2026_05_23_CHG0989771_Enable data entitlement by integration with FMCES/page.md",
      "revision": "sha256:076a08663c38af82e6cb5693ece39d9b6451a409913eadc6bcd1c0fd45b25d39",
      "sha256": "076a08663c38af82e6cb5693ece39d9b6451a409913eadc6bcd1c0fd45b25d39",
      "snapshot": "knowledge/evidence/sources/sha256/076a08663c38af82e6cb5693ece39d9b6451a409913eadc6bcd1c0fd45b25d39.md"
    },
    {
      "id": "SRC-d6dffff053e930f8b7be19bd",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Ratan One Processing Guide (DOI)/page.md",
      "revision": "sha256:f723cc9719dcb14240a8b0af86bdc26342d42368ed48d4ca5a16dfb31b825ed0",
      "sha256": "f723cc9719dcb14240a8b0af86bdc26342d42368ed48d4ca5a16dfb31b825ed0",
      "snapshot": "knowledge/evidence/sources/sha256/f723cc9719dcb14240a8b0af86bdc26342d42368ed48d4ca5a16dfb31b825ed0.md"
    }
  ],
  "generated": {
    "by": "agent:codex/sol_cn_workflow_review",
    "at": "2026-11-16T01:12:00.279837+00:00"
  },
  "verified": [],
  "classification": "operations",
  "scope": "RATAN access and data entitlement boundaries",
  "summary": "The processing guide describes FMCES-controlled cashflow visibility by profile, location, and allowed entities.",
  "related": [],
  "open_questions": [
    "Which effective authority resolves removed-versus-new business-rule roles and conflicting historical GBS country scopes?",
    "Which CES application, subject, action, and data-entitlement policy governs each tile and system-only API path, including the duplicated Nostro subject?",
    "Which blank role-country matrix entries are incomplete data, and which current signed permission tests supersede these historical expectations?"
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
# RATAN access and data entitlement boundaries

> **PROPOSED candidate:** Retained source intent awaits authority and current-applicability confirmation.

## Scope

RATAN access and data entitlement boundaries. This candidate retains the source-specific conditions and applicability limits below.

## Summary

The processing guide describes FMCES-controlled cashflow visibility by profile, location, and allowed entities.

## Documented knowledge

### Need-to-know visibility

The processing guide describes FMCES-controlled cashflow visibility by profile, location, and allowed entities. Missing data entitlement requires an FMCES request and CES onboarding. This business-data boundary is separate from Portal tile visibility and SDK name correspondence. The existing SDK topic retains that separate migration contract.

[Source 35, lines 52-64](../../../../knowledge/evidence/sources/sha256/f723cc9719dcb14240a8b0af86bdc26342d42368ed48d4ca5a16dfb31b825ed0.md#L52-L64)

### Function-role inventory

The access-request guide lists existing roles FMO_MO, FMO_MO_SUP, FMO_OPS, FMO_OPS_SUP, FMO_RO, FMO_STA_CKR, FMO_STA_MKR, NON_FMO_RO, and PSS_RO. It marks FMO_OPS_BO, FMO_OPS_BOC, FMO_OPS_BOL, FMO_OPS_BOM, FMO_OPS_INV, FMO_OPS_MKR, and FMO_OPS_BOS as new. Function-role rows request Global, GBS, or Onshore data entitlement. The guide marks all three data-entitlement roles as new. The guide marks FMO_BR_APR and FMO_BR_MKR removed. However, the broader processing guide lists them as new. No effective-date precedence is established.

[Source 32, lines 17-39](../../../../knowledge/evidence/sources/sha256/4a360c2affb24d4d6a18b571bb5d4f3711ac1ced5c3ec51b670e789779b9e47c.md#L17-L39) [Source 35, lines 68-71](../../../../knowledge/evidence/sources/sha256/f723cc9719dcb14240a8b0af86bdc26342d42368ed48d4ca5a16dfb31b825ed0.md#L68-L71)

### Request subjects and tiles

The request guide maps RATAN_TRADE_BLOTTER to Trade Blotter; RATAN_CASHFLOW_BLOTTER to FX and Equity Cashflow Blotter; RATAN_STRATEGIC_CASHFLOW_BLOTTER to strategic Cashflow Blotter; and RATAN_CASHFLOW_GROUP_BLOTTER to Grouping Blotter. RATAN_VALIDATION_EXCEPTION and RATAN_SETTLEMENT_EXCEPTION identify their exception tiles. RATAN_PROFILE_LIMITS identifies Authorization Limits. RATAN_SETTLEMENT_STP_RULE, RATAN_SUPPRESSION_RULE, and RATAN_AUTO_NETTING_RULE identify business-rule tiles, including the listed FX/Equity or Swift/Cashflow variants. RATAN_ENTITLEMENT_RULE labels Data Entitlement Rules in this request table. RATAN_NOSTRO_BLOTTER labels both Nostro Static and BIC Netting Static; RATAN_NETTING_RULE labels Netting Static. RATAN_MO_EXCEPTION is struck through as unused. These request labels do not establish runtime permission grants or resolve the duplicate static subject.

[Source 32, lines 43-59](../../../../knowledge/evidence/sources/sha256/4a360c2affb24d4d6a18b571bb5d4f3711ac1ced5c3ec51b670e789779b9e47c.md#L43-L59)

### Historical country-scope conflict

The backup entitlement table permits KL GBS all branches, including PK and Indonesia. Its India GBS row excludes PK, TZ, BD, and LK. The main table labels its first matrix pre-data-entitlement-change implementation. It excludes PK, TZ, BD, LK, and NP for India GBS; KL excludes TZ, BD, and NP. Both preserve domicile-specific onshore access, China PSS/Dev read-only access across branches, India PO read-only access except PK, SG PO read-only access including PK, and Dubai read-only access for Egypt and Saudi branches. These retained tables disagree and cannot define one current permission policy.

[Source 44, lines 1-12](../../../../knowledge/evidence/sources/sha256/c58c1ce14bf6a320599565103521aa1719ba0c3cdc0bc3b488cb450cb203a65b.md#L1-L12) [Source 45, lines 1-9](../../../../knowledge/evidence/sources/sha256/b563bc564baf6522da400243c2db038dbc1cb6468966967ab1e0d16632ba0c46.md#L1-L9)

### Role-country matrix limits

The main X_RATANONE test matrix supplies expected countries and profile names for individual roles. It includes All, All except PK, location-limited profiles, and blank entries. It includes Clearing Ops and Prime User profiles without complete country mappings. Blank roles or countries are unresolved source data, not wildcard permissions. The full literal matrix remains source evidence; this candidate does not resolve every role-country mapping or current CES equivalence.

[Source 45, lines 11-119](../../../../knowledge/evidence/sources/sha256/b563bc564baf6522da400243c2db038dbc1cb6468966967ab1e0d16632ba0c46.md#L11-L119)

### Separate CES UI onboarding

The January 2026 onboarding checklist describes global FM-CES tiles hosted through RATAN UI services. It states UI-only integration, without RATAN data feeds. This hosting scope does not itself enable cashflow data entitlement.

[Source 53, lines 3-3](../../../../knowledge/evidence/sources/sha256/4b73bc29d8ebdf40ed7bdce17fbc13104db5eda14d1551410d28370c04eaadb9.md#L3-L3) [Source 53, lines 6-10](../../../../knowledge/evidence/sources/sha256/4b73bc29d8ebdf40ed7bdce17fbc13104db5eda14d1551410d28370c04eaadb9.md#L6-L10) [Source 53, lines 12-13](../../../../knowledge/evidence/sources/sha256/4b73bc29d8ebdf40ed7bdce17fbc13104db5eda14d1551410d28370c04eaadb9.md#L12-L13) [Source 53, lines 16-18](../../../../knowledge/evidence/sources/sha256/4b73bc29d8ebdf40ed7bdce17fbc13104db5eda14d1551410d28370c04eaadb9.md#L16-L18)

### Data-entitlement integration checklist

The May 2026 checklist proposes centralized FMCES restrictions for all countries and products, including cashflow blotter and related functions. It lists real-time RATAN-to-CES HTTP integration. The SSDR path through DQSL supplies system ID, user ID, and country with entitlement enabled. TLM through DQSL supplies system ID; FMMIS, EOD, and CIS call RATAN with system ID. The source does not define equivalent user-country checks on these latter system-only paths. CES onboarding or entitlement errors appear in UI and require CES onboarding. For network issues, Auth service retries three times. Auto-recovery and Ops alerts are recorded checklist intentions, without execution results.

[Source 55, lines 16-18](../../../../knowledge/evidence/sources/sha256/076a08663c38af82e6cb5693ece39d9b6451a409913eadc6bcd1c0fd45b25d39.md#L16-L18) [Source 55, lines 31-32](../../../../knowledge/evidence/sources/sha256/076a08663c38af82e6cb5693ece39d9b6451a409913eadc6bcd1c0fd45b25d39.md#L31-L32) [Source 55, lines 51-51](../../../../knowledge/evidence/sources/sha256/076a08663c38af82e6cb5693ece39d9b6451a409913eadc6bcd1c0fd45b25d39.md#L51-L51)

## Connections

Access requests connect function roles, data profiles, tiles, and system API paths, as scoped above.

## Evidence limits

This candidate records selected source meaning. It establishes no execution, deployment, current policy, or human approval.

## Open questions

- Which effective authority resolves removed-versus-new business-rule roles and conflicting historical GBS country scopes?
- Which CES application, subject, action, and data-entitlement policy governs each tile and system-only API path, including the duplicated Nostro subject?
- Which blank role-country matrix entries are incomplete data, and which current signed permission tests supersede these historical expectations?
