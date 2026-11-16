---
type: KnowledgeTopic
id: OPS-A-KT-SSI-AND-NOSTRO
version: 4
owner: unknown
governance_state: candidate
status: draft
sources:
- id: SRC-a666b8a256e9c88651c7451e
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/FMRP China
    Cash Settlement Delivery Plan/Cash Settlement RATAN ONE 2024 Release Plan/Release
    On 2024-02-03 CR  CHG0361089/page.md
  revision: sha256:b9773419b85178ee3041032d15aa27243455f8276f29f8e46c51ec238df3a7cd
  sha256: b9773419b85178ee3041032d15aa27243455f8276f29f8e46c51ec238df3a7cd
- id: SRC-6b78ebc7ddb721d5b4591df5
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/FMRP China
    Cash Settlement Delivery Plan/Cash Settlement RATAN ONE 2024 Release Plan/Release
    On 2024-03-30 CR  CHG0426911/page.md
  revision: sha256:640d3730e1bc4c49ef803b6ed9ac58519c0234f24cde98119a0fc5cf368b823e
  sha256: 640d3730e1bc4c49ef803b6ed9ac58519c0234f24cde98119a0fc5cf368b823e
- id: SRC-ffc256f51159c0b5e1cf2553
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/FMRP China
    Cash Settlement Delivery Plan/Cash Settlement RATAN ONE 2025 Release Plan/2025
    Cash Settlement Tranche1 Release Check Point/page.md
  revision: sha256:6d68691de6c2b6ca0bc79d450e117dcb1cb864d03e9cf6bd19ca75ec0b74ace8
  sha256: 6d68691de6c2b6ca0bc79d450e117dcb1cb864d03e9cf6bd19ca75ec0b74ace8
- id: SRC-53ffa7d156a23f8789fb5ffa
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/FMRP China
    Cash Settlement Delivery Plan/Cash Settlement RATAN ONE 2026 Release Plan/Release
    On 2026-08-08  CR    RATAN Settlement FMRP8.0 - FXO - Suspension logic movement/Retrospective
    2026-08-26/page.md
  revision: sha256:7a66033559c607df0a44a6139ed654c77121308deb6e8edb340689ed0bb1dee1
  sha256: 7a66033559c607df0a44a6139ed654c77121308deb6e8edb340689ed0bb1dee1
- id: SRC-1e9231a378d43046cd6e6149
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/04-Onboarding(Entity Product) Check List/F2B Milestone Onboarding
    check list/F2B Milestone Checklist - HK & TW/page.md
  revision: sha256:1cb0ccb49eeaf9292e881036a00f4729b14938812ae53fee3aec968b2090cfdc
  sha256: 1cb0ccb49eeaf9292e881036a00f4729b14938812ae53fee3aec968b2090cfdc
- id: SRC-1fb7ba38d601b0564039298a
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/04-Onboarding(Entity Product) Check List/F2B Milestone Onboarding
    check list/F2B Milestone Checklist - Prime Day 2/page.md
  revision: sha256:f68137a3bf28077a4402e37a9ac639174d5d0d9d1dfc57eb55cfa2c914758d2a
  sha256: f68137a3bf28077a4402e37a9ac639174d5d0d9d1dfc57eb55cfa2c914758d2a
- id: SRC-0a6dff417e9803686301f674
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/04-Onboarding(Entity Product) Check List/F2B Milestone Onboarding
    check list/F2B Milestone check list - Korea Cashflow Migration/page.md
  revision: sha256:f8de834bf389f3fa20fbce4979a28d067f498aa90d28f144a73794618758d79e
  sha256: f8de834bf389f3fa20fbce4979a28d067f498aa90d28f144a73794618758d79e
- id: SRC-d6dffff053e930f8b7be19bd
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Ratan One Processing Guide (DOI)/page.md
  revision: sha256:f723cc9719dcb14240a8b0af86bdc26342d42368ed48d4ca5a16dfb31b825ed0
  sha256: f723cc9719dcb14240a8b0af86bdc26342d42368ed48d4ca5a16dfb31b825ed0
  snapshot: knowledge/evidence/sources/sha256/f723cc9719dcb14240a8b0af86bdc26342d42368ed48d4ca5a16dfb31b825ed0.md
generated:
  by: agent:codex/sol_cn_workflow_review
  at: '2026-11-16T01:29:26.253854+00:00'
verified: []
classification: operations
scope: Dated SSI and Nostro intent for CN, HK/TW, Prime UK, and Korea; current authority
  and applicability remain unknown.
summary: Selected sources describe cashflow display, SSI and Nostro stamping, validation,
  and regional onboarding expectations.
related: []
open_questions:
- 'KDQ-f6c5e6a653: Confirm the exact `Release` status meaning and the state and Vostro
  lookup rules.'
- 'KDQ-ae4e60b7e0: Confirm Nostro effective dates and primary-Nostro refresh rules.'
- 'KDQ-21c11727dd: Confirm current SSI effective dates and hierarchy.'
- 'KDQ-f6b21f48f4: Confirm whether NOX is in the effective validation list.'
- 'KDQ-a8f2c7244f: Confirm effective SSI/NSTP target controls and mandatory fields.'
- 'KDQ-6f50e337aa: Confirm the authoritative HK/TW checklist rows.'
- 'KDQ-e2c589f5c5: Confirm HK/TW SGO mapping and netting outcomes.'
- 'KDQ-c83d9ee9e1: Confirm current Prime checklist scope.'
- 'KDQ-0384781ae4: Confirm effective Prime static mappings and suppressions.'
- 'KDQ-42d5558966: Confirm Korea mapping, TDS3, and migration controls.'
- 'KDQ-8ad3b904b1: Confirm Korea static, rule, downstream, and go-live decisions.'
- 'KDQ-fa019a8c49: Confirm the effective scope, authority, and applicability owner.'
- 'KDQ-3de0093001: Confirm source authority and effective version.'
- 'KDQ-SSI-DOI-ID: Confirm the effective DOI SSI-ID editing and maker-checker rules,
  including restoration of edited values.'
---
# SSI and Nostro operations

## Scope

This topic preserves dated SSI and Nostro intent from CN, HK/TW, Prime UK, and Korea sources.
It does not claim current approval, rollout, or universal regional behavior.

## Summary

The selected material covers status display, SSI lookup, Nostro refresh, static data, validation, and onboarding scope.

## Documented knowledge

- `OPS-A-CLAIM-009`: The 3 February 2024 CN request asks for the Swift Message tab for current or prior `Settled` or `Release` states. It asks for Vostro means and account lookup by SSI ID when present. It defines no `Released` alias, state precedence, or missing-SSI fallback. Evidence: `knowledge/evidence/sources/sha256/b9773419b85178ee3041032d15aa27243455f8276f29f8e46c51ec238df3a7cd.md#L19`.
- `OPS-A-CLAIM-011`: The archived CN Day 2 list asks for Nostro Start/End Dates and cashflow refresh after primary Nostro creation or deletion. It also asks for an optional Nostro-static address and further unspecified static enhancements. Evidence: `knowledge/evidence/sources/sha256/640d3730e1bc4c49ef803b6ed9ac58519c0234f24cde98119a0fc5cf368b823e.md#L56`.
- `OPS-A-CLAIM-014`: The archived trade-level list asks for Vostro settlement-code display and date-bounded Nostro/Vostro stamping. It asks RATAN to select the correct Vostro SSI and SSI+ to supply the correct CFI when IRS and CCS SSIs differ. It lists CDUPS updates for IRS/CCS, fixing-notice, and SSI-change flows, including start and end dates. Evidence: `knowledge/evidence/sources/sha256/640d3730e1bc4c49ef803b6ed9ac58519c0234f24cde98119a0fc5cf368b823e.md#L63`.
- `OPS-A-CLAIM-UI-058`: The archived CN detail-page list requests Nostro ID display in candidate and Nostro fields. It requests multiple-Vostro selection improvements and retention of checker input after SSI rejection. It requests uppercase SI input, exclusion of fields 70 and 72 from dual blind input, and removal of the Vostro CMS account field. Evidence: `knowledge/evidence/sources/sha256/640d3730e1bc4c49ef803b6ed9ac58519c0234f24cde98119a0fc5cf368b823e.md#L58`.
- `OPS-A-CLAIM-025`: The 2025 tranche checkpoint proposes adding NOX to SSI-stamping validation. It gives no effective validation list or completion evidence. Evidence: `knowledge/evidence/sources/sha256/6d68691de6c2b6ca0bc79d450e117dcb1cb864d03e9cf6bd19ca75ec0b74ace8.md#L1-L3`.
- `OPS-A-CLAIM-038`: The August 2026 retrospective lists fixes due by 29 August. It calls for correct propagation of `Is_Auto_Netting` and `Auto_Netting_Stp_Level`. Missing mandatory NSTP control attributes must produce a hard stop and exception instead of STP. It requests regression cases for auto-netting, NSTP exceptions, and missing controls. This is dated proposed scope, not delivery or execution evidence. Evidence: `knowledge/evidence/sources/sha256/7a66033559c607df0a44a6139ed654c77121308deb6e8edb340689ed0bb1dee1.md#L60-L64`.
- `OPS-A-CLAIM-043`: The HK/TW checklist expects SSI attachment for IRS, CCS, and Loan Depo, with correct CFI capture. It describes hierarchy, settlement method, one or two agents, and CDUPS. It excludes three-agent support. It expects default Nostro stamping and SGO-to-SGD processing, with no Swift/accounting failure. It expects SGO Nostro/Vostro attachment. Its UK-model row prioritizes country-specific plus global-product SSI over global-entity plus product-specific SSI. It leaves the Nostro source marked TBC and gives no Vostro values. Evidence: `knowledge/evidence/sources/sha256/1cb0ccb49eeaf9292e881036a00f4729b14938812ae53fee3aec968b2090cfdc.md#L12-L14, #L41-L42, #L57-L58`.
- `OPS-A-CLAIM-045`: The Prime UK UAT Drop 2 checklist expects default Nostro stamping and SSI attachment for IRS, CCS, and Loan Depo. It expects correct CFI capture and SGO-to-SGD processing, with no Swift/accounting failure. It expects automatic SGO Nostro/Vostro attachment. It supports one or two agents, excludes three, and lists product-based CDUPS stamping. Its UK hierarchy prioritizes country-specific plus global-product SSI over global-entity plus product-specific SSI. Static rows leave the Nostro source TBC and provide no settlement means or account values. Evidence: `knowledge/evidence/sources/sha256/f68137a3bf28077a4402e37a9ac639174d5d0d9d1dfc57eb55cfa2c914758d2a.md#L7-L9, #L36-L37, #L52-L53`.
- `OPS-A-CLAIM-048`: The Korea migration checklist describes old and new SSI hierarchy scope, first-two-character CFI lookup, and extra IRS/CCS logic. It supports one or two agents, excludes three, and lists product-based CDUPS. Its SSI row requests SGO-to-SGD and KRO-to-KRW conversions. Its separate Nostro row says to follow default and strikes out SGO conversion. Static rows mark the Nostro source TBC, leave Vostro values for agreement, and conflict on new settlement means. Evidence: `knowledge/evidence/sources/sha256/f8de834bf389f3fa20fbce4979a28d067f498aa90d28f144a73794618758d79e.md#L4-L5, #L39-L40, #L55, #L57`.

- `OPS-A-CLAIM-SSI-DOI-ID`: The DOI SSI-ID section defines these source-scoped rules. Automatic SI stamping populates the SSI ID. Manual Vostro SI entry leaves it blank. Selecting available SI and submitting unchanged sets the selected SSI ID. For automatic or selected SI, changes limited to fields 70/72 retain the ID. Show `Field 70/72 Customized` only when an SSI ID exists and those fields changed. Without an SSI ID, show no customization indicator. Changes to other fields remove the ID. After selection, editing and manually restoring original values still removes the ID. Maker selection and checker manual entry remain different input paths, even with equal displayed values. That mismatch produces a validation error. The checker cannot see the maker-selected SSI ID. Approval during Vostro edit mode preserves the ID when SI values remain unchanged. Evidence: `knowledge/evidence/sources/sha256/f723cc9719dcb14240a8b0af86bdc26342d42368ed48d4ca5a16dfb31b825ed0.md#L370-L379`.

## Connections

The October 2026 26C and Group Blotter items require separate contract knowledge.
Regional checklists also contain netting, accounting, migration, and integration scope.
Those details belong with their responsible topics and remain unresolved there.

## Evidence limits

These records contain dated proposals, release scope, and checklist expectations.
They do not establish approval, current applicability, implementation, deployment, execution, or acceptance.
The selected HK/TW text links two screenshots. Their image contents were not inspected.
The source text does not establish what those screenshots contain.
Test plans and replay notes remain task evidence, not proof of behavior.

The DOI addition covers lines 370–379 only. Other DOI clauses and the linked image remain outside this review.

## Open questions

Owner: unknown. Answers remain blank in the owning task register.
See the owning task register: `tasks/workbench-knowledge-raw-import-20261113/evidence/canonical-draft-questions-20261115.md`.
