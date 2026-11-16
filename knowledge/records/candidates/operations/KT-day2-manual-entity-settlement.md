---
type: KnowledgeTopic
id: KT-day2-manual-entity-settlement
version: 1
owner: unknown
governance_state: candidate
status: draft
verified: []
sources:
- id: SRC-9ab2613819f0ef372d4ba406
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Settlement Day2 Requirement/Enable Settlement for Manual Entities/00
    Manual Entities Onboarding Checklist/page.md
  revision: sha256:be61f283209ddc7623e48b85f0afc0eebe5c2a1b2bc3c60b22dc94e048a5ae8f
  sha256: be61f283209ddc7623e48b85f0afc0eebe5c2a1b2bc3c60b22dc94e048a5ae8f
- id: SRC-965e5beb215a78fd7c90f71f
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Settlement Day2 Requirement/Enable Settlement for Manual Entities/01
    Enabling Settlement for Manual Entities/page.md
  revision: sha256:274a2f16e543f5fa10c5c9bd8fbebf709040b5bc689553c3019151a587770ad0
  sha256: 274a2f16e543f5fa10c5c9bd8fbebf709040b5bc689553c3019151a587770ad0
- id: SRC-3944e699eb7866bc77945faf
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Settlement Day2 Requirement/Enable Settlement for Manual Entities/02
    Swift Message Analysing for manual entities/page.md
  revision: sha256:a1e50c06a7f2fe0ea2c9a9afff1dd3ffa69f275a2ab575a803a5aca4addfdf67
  sha256: a1e50c06a7f2fe0ea2c9a9afff1dd3ffa69f275a2ab575a803a5aca4addfdf67
- id: SRC-70ad4e5a1b8cd791d6489387
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Settlement Day2 Requirement/Enable Settlement for Manual Entities/03
    UAT testing/003 QATAR SLATE ONE LLC DOH(GBS)/page.md
  revision: sha256:7d1194a3901058a8da6c0d6d76572741c88ee698ed0148bc787c67e1ceac5119
  sha256: 7d1194a3901058a8da6c0d6d76572741c88ee698ed0148bc787c67e1ceac5119
classification: operations
scope: Manual-entity settlement onboarding and regional controls
summary: Source-specific intended rules and proposals retain their conditions and
  unresolved authority.
related:
- KT-ratan-entity-and-currency-onboarding-controls
- KT-ratan-settlement-integration-checklist-scope
- KT-settlement-lms-feed
open_questions:
- 'KDQ-1ab120fcba: Which dated entity/static matrix governs cutoff attachments, SSI
  hierarchy, country MX eligibility, and SLATE downstream treatment?'
- 'KDQ-11d2231b79: Which effective Vietnam USD VCB and field-53/MX customization requirements
  apply to each message family?'
generated:
  by: agent:codex:sol-functional-lane-3-review
  at: '2026-11-16T01:47:34.235225+00:00'
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# Manual-entity settlement onboarding and regional controls

## Scope

Manual-entity settlement onboarding and regional controls.
This candidate retains documented intent and source-specific proposals.

## Summary

The selected sources define related responsibilities, predicates, and exceptions.
Their effective authority and current applicability remain unresolved.

## Documented knowledge

### ME-01 — Dated entity and release-cutoff scope

The manual-entity requirement enables RATAN settlement for the listed Murex 2.11 entities.
Botswana is struck out and replaced by Qatar in the February 2026 scope. SLATE_QFC remains cashflow-suppressed.
The roster covers Bahrain, Qatar, Kenya, Zambia, Uganda, Tanzania, Ghana, Nigeria, Sri Lanka, Vietnam, Pakistan, and Bangladesh.
It also names SLATE_QFC and FCBUSLANKA separately. Country counts and entity counts must remain distinct.
Bahrain, Kenya, Zambia, Uganda, and Ghana use VD-1 business day at 15:00 UTC, following the London currency set.
Nigeria uses 17:00 UTC; Sri Lanka/FCBUSLANKA and Pakistan use 13:00 UTC; Vietnam uses 11:00 UTC.
Qatar, Tanzania, and Bangladesh use supplied Razor currency/shifter/time/timezone values, excluding blank-currency rows.
Their documented missing-configuration fallback is VD-1 business day at 18:00 GMT.
Referenced spreadsheets and static sign-offs were not inspected. These notes do not verify current settings.

[Original evidence](../../../evidence/sources/sha256/274a2f16e543f5fa10c5c9bd8fbebf709040b5bc689553c3019151a587770ad0.md#L1-L3). [Original evidence](../../../evidence/sources/sha256/274a2f16e543f5fa10c5c9bd8fbebf709040b5bc689553c3019151a587770ad0.md#L35-L53). [Original evidence](../../../evidence/sources/sha256/274a2f16e543f5fa10c5c9bd8fbebf709040b5bc689553c3019151a587770ad0.md#L115-L132).

### ME-02 — Currency conversion, rounding, and accounting context

The source requests NGB→NGN and PKO→PKR mappings and retains VNO→VND, LKO→LKR, BDO→BDT, and NGX→NGN.
The later August notes set NGN and NGB precision to two decimals. The older NGN zero-decimal proposal is struck out.
NGB uses ROUNDING_OFF. Earlier speculative rounding notes cannot supersede the later explicit correction.
The source requires no new CFI code. It treats DFCC as NOS rather than a new settlement means.
It lists country-specific ZoneIds for accounting. These are source-scoped configuration requirements.
A Tanzania note changes the credit transaction code from 278 to 578. Other account/branch values require their supplied static authority.
The page lists all manual entities for LMS and says all twelve countries use eBBS.
The 14-row entity list and twelve-country wording must not be treated as contradictory counts without distinguishing their units.
SLATE suppression and LMS publication still require their lifecycle scopes to be reconciled.

[Original evidence](../../../evidence/sources/sha256/274a2f16e543f5fa10c5c9bd8fbebf709040b5bc689553c3019151a587770ad0.md#L161-L172). [Original evidence](../../../evidence/sources/sha256/274a2f16e543f5fa10c5c9bd8fbebf709040b5bc689553c3019151a587770ad0.md#L248-L271). [Original evidence](../../../evidence/sources/sha256/274a2f16e543f5fa10c5c9bd8fbebf709040b5bc689553c3019151a587770ad0.md#L680-L682). [Original evidence](../../../evidence/sources/sha256/274a2f16e543f5fa10c5c9bd8fbebf709040b5bc689553c3019151a587770ad0.md#L704-L706). [Original evidence](../../../evidence/sources/sha256/274a2f16e543f5fa10c5c9bd8fbebf709040b5bc689553c3019151a587770ad0.md#L712-L725). [Original evidence](../../../evidence/sources/sha256/274a2f16e543f5fa10c5c9bd8fbebf709040b5bc689553c3019151a587770ad0.md#L1006-L1016). [Original evidence](../../../evidence/sources/sha256/274a2f16e543f5fa10c5c9bd8fbebf709040b5bc689553c3019151a587770ad0.md#L1043). [Original evidence](../../../evidence/sources/sha256/274a2f16e543f5fa10c5c9bd8fbebf709040b5bc689553c3019151a587770ad0.md#L1104-L1121). [Original evidence](../../../evidence/sources/sha256/274a2f16e543f5fa10c5c9bd8fbebf709040b5bc689553c3019151a587770ad0.md#L1127-L1137). [Original evidence](../../../evidence/sources/sha256/274a2f16e543f5fa10c5c9bd8fbebf709040b5bc689553c3019151a587770ad0.md#L1205-L1206).

### ME-03 — Scope-specific controls and UI configuration

The requirement adds manual-entity currency choices to quick search, including ISO and non-ISO aliases.
It specifies maker/checker DVP checks for Sri Lanka and Pakistan, broad Bangladesh NSTP, and later Tanzania NSTP.
The Islamic-portfolio rules extend to Bahrain and Qatar only in the stated June clarification.
A scoped precious-metal suppression rule covers Kenya, Bahrain, Uganda, Zambia, Nigeria, Ghana, and Qatar.
SLATE_QFC needs its suppression rule and no strategic SWIFT-list entry. Other in-scope entities need the SWIFT-list entry.
The source says manual entities should not send to Razor. This is distinct from the LMS target.
Rule identifiers, Done labels, and alleged production references do not establish implemented controls.

[Original evidence](../../../evidence/sources/sha256/274a2f16e543f5fa10c5c9bd8fbebf709040b5bc689553c3019151a587770ad0.md#L779-L804). [Original evidence](../../../evidence/sources/sha256/274a2f16e543f5fa10c5c9bd8fbebf709040b5bc689553c3019151a587770ad0.md#L1022-L1025). [Original evidence](../../../evidence/sources/sha256/274a2f16e543f5fa10c5c9bd8fbebf709040b5bc689553c3019151a587770ad0.md#L1029-L1032). [Original evidence](../../../evidence/sources/sha256/274a2f16e543f5fa10c5c9bd8fbebf709040b5bc689553c3019151a587770ad0.md#L1045-L1048). [Original evidence](../../../evidence/sources/sha256/274a2f16e543f5fa10c5c9bd8fbebf709040b5bc689553c3019151a587770ad0.md#L1053). [Original evidence](../../../evidence/sources/sha256/274a2f16e543f5fa10c5c9bd8fbebf709040b5bc689553c3019151a587770ad0.md#L1064-L1071). [Original evidence](../../../evidence/sources/sha256/274a2f16e543f5fa10c5c9bd8fbebf709040b5bc689553c3019151a587770ad0.md#L1090-L1096).

### ME-04 — Onboarding prerequisites and unresolved checklist items

The checklist requires entity sender/53/58/receiver BICs, branch mappings, release cutoff, accounting bridge and eBBS configuration, and Nostro static.
Business-rule setup covers cashflow/SWIFT suppression, auto-debit, entity scope, netting, and BIC netting.
Several NDS, pending-fixing, SSI-hierarchy, UI, and settlement-means rows are marked No? or ask questions.
The UK hierarchy prioritizes country-specific/global-product SSI over global-entity/product-specific SSI.
Its literal legacy whitelist includes LOANID. The checklist asks whether manual entities should use the new hierarchy.
Those unresolved rows cannot establish final applicability for every entity.

[Original evidence](../../../evidence/sources/sha256/be61f283209ddc7623e48b85f0afc0eebe5c2a1b2bc3c60b22dc94e048a5ae8f.md#L1-L2). [Original evidence](../../../evidence/sources/sha256/be61f283209ddc7623e48b85f0afc0eebe5c2a1b2bc3c60b22dc94e048a5ae8f.md#L7-L11). [Original evidence](../../../evidence/sources/sha256/be61f283209ddc7623e48b85f0afc0eebe5c2a1b2bc3c60b22dc94e048a5ae8f.md#L13-L19).

### ME-05 — Vietnam customization and dated MX bifurcation

The September Vietnam requirement sets field 53 to STBVVNVXXXX for MT103/MT202 and equivalent MX paths when Nostro account is VNO SBV.
MT103COV/202COV, MT202 Flip, and CrossDebit are excluded from that field-53 customization.
For Vietnam pacs008/pacs009, InstrForNxtAgt/InstrInf omits the `/FIN53/{53BIC}` prefix.
The dated bifurcation table distinguishes new MT103/MT202/MT202COV conversion from cancellation of original MX messages.
Cancellation eligibility depends on the original message being MX and the corresponding MT192/MT292 family.
Local-receiver exclusions apply separately to Sri Lanka, Ghana, and Qatar in their listed rows. Uganda all-to-MX remains pending.
The Kenya row contains a Tanzania sender-prefix condition. This unresolved row cannot be silently corrected.
The Vietnam USD VCB analysis contains contradictory accounting/no-SWIFT and NOS-pay statements. It does not define a current exemption.
The table provides planned dates and source-specific predicates, not completed country rollouts.

[Original evidence](../../../evidence/sources/sha256/a1e50c06a7f2fe0ea2c9a9afff1dd3ffa69f275a2ab575a803a5aca4addfdf67.md#L58). [Original evidence](../../../evidence/sources/sha256/a1e50c06a7f2fe0ea2c9a9afff1dd3ffa69f275a2ab575a803a5aca4addfdf67.md#L69-L71). [Original evidence](../../../evidence/sources/sha256/a1e50c06a7f2fe0ea2c9a9afff1dd3ffa69f275a2ab575a803a5aca4addfdf67.md#L89-L104). [Original evidence](../../../evidence/sources/sha256/a1e50c06a7f2fe0ea2c9a9afff1dd3ffa69f275a2ab575a803a5aca4addfdf67.md#L113).

### ME-06 — SLATE suppression exception

The selected SLATE note requires cashflow suppression only. Other static setup is not required in that stated scope.
Its presence under a UAT directory does not establish executed testing or acceptance.

[Original evidence](../../../evidence/sources/sha256/7d1194a3901058a8da6c0d6d76572741c88ee698ed0148bc787c67e1ceac5119.md#L1).

## Connections

Related canonical IDs: `KT-ratan-entity-and-currency-onboarding-controls`, `KT-ratan-settlement-integration-checklist-scope`, `KT-settlement-lms-feed`.

## Evidence limits

This candidate establishes no inspected implementation, execution, rollout, publication, or business acceptance.
Unselected content and linked attachments were not used to fill missing rules.

## Open questions

Owner: unknown. Answers remain pending in the single [central question register](../../../../tasks/workbench-knowledge-raw-import-20261113/evidence/canonical-draft-questions-20261115.md).
