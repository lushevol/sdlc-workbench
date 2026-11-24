---
{
  "type": "KnowledgeTopic",
  "id": "KT-day2-cashflow-splitting",
  "version": 1,
  "owner": "unknown",
  "governance_state": "candidate",
  "status": "draft",
  "sources": [
    {
      "id": "SRC-77b67cd063ea35b3339b2324",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Settlement Day2 Requirement/Cashflow Splitting/Cashflow Auto Distribution Design/page.md",
      "revision": "sha256:1f892e514d6c756c6a7cfd4d458327eea4021d9a809a18bfe24f465369b89707",
      "sha256": "1f892e514d6c756c6a7cfd4d458327eea4021d9a809a18bfe24f465369b89707",
      "snapshot": "knowledge/evidence/sources/sha256/1f892e514d6c756c6a7cfd4d458327eea4021d9a809a18bfe24f465369b89707.md"
    },
    {
      "id": "SRC-e8adbcd8a645a7b7d1bb809d",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Settlement Day2 Requirement/Cashflow Splitting/Cashflow Split Static/page.md",
      "revision": "sha256:cf0e79e604c73dcab0557ee6f43e01e1db55139fb22a7e6f446c10b519a9f1f6",
      "sha256": "cf0e79e604c73dcab0557ee6f43e01e1db55139fb22a7e6f446c10b519a9f1f6",
      "snapshot": "knowledge/evidence/sources/sha256/cf0e79e604c73dcab0557ee6f43e01e1db55139fb22a7e6f446c10b519a9f1f6.md"
    },
    {
      "id": "SRC-1e52fab3b00c1251ffb3402d",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Settlement Day2 Requirement/Cashflow Splitting/Split Demo Cases/page.md",
      "revision": "sha256:9e1eb5acba4cf682345226ef13dd0f1fb7147b9ce8ef8e33f52f03c0e43778df",
      "sha256": "9e1eb5acba4cf682345226ef13dd0f1fb7147b9ce8ef8e33f52f03c0e43778df",
      "snapshot": "knowledge/evidence/sources/sha256/9e1eb5acba4cf682345226ef13dd0f1fb7147b9ce8ef8e33f52f03c0e43778df.md"
    },
    {
      "id": "SRC-cd3f7f9601b479f1a66549e3",
      "resource": "source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Settlement Day2 Requirement/Cashflow Splitting/page.md",
      "revision": "sha256:2635579967f19c33ff382f1c3a95b4e7693e62c6ad1d27380ee001a51c45ce0c",
      "sha256": "2635579967f19c33ff382f1c3a95b4e7693e62c6ad1d27380ee001a51c45ce0c",
      "snapshot": "knowledge/evidence/sources/sha256/2635579967f19c33ff382f1c3a95b4e7693e62c6ad1d27380ee001a51c45ce0c.md"
    }
  ],
  "generated": {
    "by": "agent:codex/sol_cn_workflow_review",
    "at": "2026-11-16T01:49:39.847510+00:00"
  },
  "verified": [],
  "classification": "settlement",
  "scope": "Cashflow splitting and threshold distribution intent",
  "summary": "The dated requirement limits split functionality to FMRP flows.",
  "related": [],
  "open_questions": [
    "Resolve effective manual-split scope for generic/IRS resultants and exact unreleased withdrawal parent/child states.",
    "Confirm released-child reversal accounting and safe operator actions.",
    "Confirm SWIFT_SUPPRESSED unsplit eligibility and threshold disable/delete contract.",
    "Provide the complete bounded distribution algorithm, selected static, TechFail result/comment and SI-retention rule."
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
# Cashflow splitting and threshold distribution intent

> **PROPOSED candidate:** Retained source intent awaits authority and current-applicability confirmation.

## Scope

Cashflow splitting and threshold distribution intent. This candidate retains the source-specific conditions and applicability limits below.

## Summary

The dated requirement limits split functionality to FMRP flows.

## Documented knowledge

### Scope and manual eligibility

The dated requirement limits split functionality to FMRP flows. It excludes BCS/LOANIQ and historical Razor-routed EG/NP/SA, with EG/NP/SA inclusion conditional on strategic migration before go-live. Manual split requires New, WAITING or READY, no netting ID, no splitting ID and non-LOANIQ source. PROJECTED eligibility is struck through. The action profile matches netting; no manual split rule is required. Manual splitting of generic and IRS netting resultants has conflicting dated scope and test rows. No current resultant permission is selected.

[Source 23, lines 23-42](../../../../knowledge/evidence/sources/sha256/2635579967f19c33ff382f1c3a95b4e7693e62c6ad1d27380ee001a51c45ce0c.md#L23-L42) [Source 23, lines 53-53](../../../../knowledge/evidence/sources/sha256/2635579967f19c33ff382f1c3a95b4e7693e62c6ad1d27380ee001a51c45ce0c.md#L53-L53) [Source 23, lines 110-114](../../../../knowledge/evidence/sources/sha256/2635579967f19c33ff382f1c3a95b4e7693e62c6ad1d27380ee001a51c45ce0c.md#L110-L114) [Source 23, lines 126-126](../../../../knowledge/evidence/sources/sha256/2635579967f19c33ff382f1c3a95b4e7693e62c6ad1d27380ee001a51c45ce0c.md#L126-L126)

### Manual amounts and confirmation

Preview starts with the original amount. Reducing an amount creates another child for the balance. Each input must be greater than zero and below available balance, using currency rounding precision. SI lookup is optional and uses the adhoc-SSI profile. Split With Affirmation requests affirmation details and marks children affirmed, without Pending Affirmation. One user approves the split action; child release still follows its exception controls. The parent becomes SPLIT. Children use an S prefix and length12, return to the main workflow and wait with Split Cashflow. Splitting_Id links parent and children and supports queries/display. No populated sample identity is retained.

[Source 23, lines 43-48](../../../../knowledge/evidence/sources/sha256/2635579967f19c33ff382f1c3a95b4e7693e62c6ad1d27380ee001a51c45ce0c.md#L43-L48) [Source 24, lines 3-6](../../../../knowledge/evidence/sources/sha256/9e1eb5acba4cf682345226ef13dd0f1fb7147b9ce8ef8e33f52f03c0e43778df.md#L3-L6)

### Amendment and unsplit

Amendment requires at least two WAITING children. Only their amounts can change; users cannot add/delete children. Preserve the original total after excluding ineligible-child amounts from the available balance. The source records no authorization-limit restriction for the split action, and one-user amendment without checker. Children retain Split Cashflow plus Split Amend; parent remains SPLIT. Unsplit requires a splitting ID, New event and no RELEASED/SETTLED child. Its main list permits QUEUED,WAITING,FAILED,HOLD,READY with NA, CASHFLOW_SUPPRESSED and SWIFT_SUPPRESSED. The demo omits SWIFT_SUPPRESSED, leaving applicability unresolved. Success makes children DEAD and returns parent to WAITING with Un-Split. The demo removes splitting ID.

[Source 23, lines 49-51](../../../../knowledge/evidence/sources/sha256/2635579967f19c33ff382f1c3a95b4e7693e62c6ad1d27380ee001a51c45ce0c.md#L49-L51) [Source 24, lines 7-10](../../../../knowledge/evidence/sources/sha256/9e1eb5acba4cf682345226ef13dd0f1fb7147b9ce8ef8e33f52f03c0e43778df.md#L7-L10)

### Lifecycle and downstream effects

SPLIT and unsplit changes write back to Stella, not Murex. A released child, or a child settled without prior release, writes back to Murex where applicable, including underlying net components. Split children cannot manually split, net, hit automatic/NDS netting rules or run IRS checks; automatic splitting remains allowed. SPLIT generates no accounting and cannot move to FAILED. Trade Undo after SPLIT moves the new event to ERROR. Non-economic withdrawal/new is ignored when SPLIT has a released/settled child, or manual touch exists; untouched flows process the latest version. Blade hard-blocks split status; Stella and DQSL require split state/field support.

[Source 23, lines 44-47](../../../../knowledge/evidence/sources/sha256/2635579967f19c33ff382f1c3a95b4e7693e62c6ad1d27380ee001a51c45ce0c.md#L44-L47) [Source 23, lines 53-58](../../../../knowledge/evidence/sources/sha256/2635579967f19c33ff382f1c3a95b4e7693e62c6ad1d27380ee001a51c45ce0c.md#L53-L58) [Source 23, lines 83-86](../../../../knowledge/evidence/sources/sha256/2635579967f19c33ff382f1c3a95b4e7693e62c6ad1d27380ee001a51c45ce0c.md#L83-L86) [Source 23, lines 88-88](../../../../knowledge/evidence/sources/sha256/2635579967f19c33ff382f1c3a95b4e7693e62c6ad1d27380ee001a51c45ce0c.md#L88-L88) [Source 23, lines 111-114](../../../../knowledge/evidence/sources/sha256/2635579967f19c33ff382f1c3a95b4e7693e62c6ad1d27380ee001a51c45ce0c.md#L111-L114)

### Withdrawal conflicts

The main rule splits parent withdrawal into child withdrawals: unreleased children CANCELLED; released-child withdrawal waits for manual action, and withdrawal parent remains SPLIT. A later test expects unreleased-child withdrawal to auto-unsplit, make children DEAD and cancel parent. The net-component test additionally auto-unnets, cancels the withdrawn component, returns its partner WAITING and makes resultant/children DEAD. Released-child tests hold withdrawal NSTP and then expect READY with Swift error after manual release. Dated IRS notes disagree about reversal accounting and manual-split permission. These are unresolved expected outcomes, not observed execution.

[Source 23, lines 54-54](../../../../knowledge/evidence/sources/sha256/2635579967f19c33ff382f1c3a95b4e7693e62c6ad1d27380ee001a51c45ce0c.md#L54-L54) [Source 23, lines 110-114](../../../../knowledge/evidence/sources/sha256/2635579967f19c33ff382f1c3a95b4e7693e62c6ad1d27380ee001a51c45ce0c.md#L110-L114) [Source 23, lines 131-134](../../../../knowledge/evidence/sources/sha256/2635579967f19c33ff382f1c3a95b4e7693e62c6ad1d27380ee001a51c45ce0c.md#L131-L134) [Source 24, lines 11-11](../../../../knowledge/evidence/sources/sha256/9e1eb5acba4cf682345226ef13dd0f1fb7147b9ce8ef8e33f52f03c0e43778df.md#L11-L11)

### Threshold static and distribution

DataOps maintains Nostro Threshold Static with maker/checker; other users read only. Currency, threshold, amount and limitation are mandatory. Entity and Nostro-agent BIC are optional; missing entity produces a warning. Agent BIC length is8/11. Numeric fields have no decimals; amount is below threshold and limitation, and limitation below threshold. Duplicate key is entity+agent+currency. The main design uses create/update/disable, while the demo lists delete. Confirm the effective action contract. Before Swift generation, pay cashflows meeting static with amount>=threshold automatically split. Best-match order is currency, entity, then Nostro agent. Net resultants and existing split children may auto-split. Each child generates its own Swift/accounting. Exact selected threshold records still require owner confirmation.

[Source 23, lines 60-68](../../../../knowledge/evidence/sources/sha256/2635579967f19c33ff382f1c3a95b4e7693e62c6ad1d27380ee001a51c45ce0c.md#L60-L68) [Source 22, lines 13-17](../../../../knowledge/evidence/sources/sha256/cf0e79e604c73dcab0557ee6f43e01e1db55139fb22a7e6f446c10b519a9f1f6.md#L13-L17) [Source 24, lines 13-19](../../../../knowledge/evidence/sources/sha256/9e1eb5acba4cf682345226ef13dd0f1fb7147b9ce8ef8e33f52f03c0e43778df.md#L13-L19)

### Split payment annotation

Automatic children add /REC/Split of currency and parent amount. MT103/MT103Cov uses field70 only; MT202/MT202Cov/MT202Flip uses72. MT605/MT210 are excluded. Insert first and shift existing lines, dropping the last if full. INR places the split text third after LEI. This annotation appears in Swift only, not cashflow detail.

[Source 23, lines 71-71](../../../../knowledge/evidence/sources/sha256/2635579967f19c33ff382f1c3a95b4e7693e62c6ad1d27380ee001a51c45ce0c.md#L71-L71)

### Failure and rule controls

The algorithm proposes accumulated deductions below threshold, skipping every tenth child, separating duplicate final amounts and reducing deduction by ten when limits are reached. The selected text is incomplete without its images. A deduction below one raises an exception to stop infinite splitting. The first design uses AutoSplitFail into READY/NA/PendingException. A later proposal replaces that action with TechFail and a comment because withdrawal handling from that state is source-reported as unsupported. Actual TechFail result/comment details remain in an uninspected image. Split Cashflow, Split Amend, Un-Split and Withdrawal on Split rules each use MAKER_CHECKER,NSTP and no bulk eligibility.

[Source 21, lines 13-23](../../../../knowledge/evidence/sources/sha256/1f892e514d6c756c6a7cfd4d458327eea4021d9a809a18bfe24f465369b89707.md#L13-L23) [Source 21, lines 60-80](../../../../knowledge/evidence/sources/sha256/1f892e514d6c756c6a7cfd4d458327eea4021d9a809a18bfe24f465369b89707.md#L60-L80) [Source 22, lines 3-10](../../../../knowledge/evidence/sources/sha256/cf0e79e604c73dcab0557ee6f43e01e1db55139fb22a7e6f446c10b519a9f1f6.md#L3-L10) [Source 23, lines 73-76](../../../../knowledge/evidence/sources/sha256/2635579967f19c33ff382f1c3a95b4e7693e62c6ad1d27380ee001a51c45ce0c.md#L73-L76)

### Future scope and outstanding decisions

The main source lists adhocSSI inside preview and split-rule history as future enhancements. It rejects opposite-direction/above-original splitting as risky, and tracks precious-metal disabling separately. Selected-SI ID retention through reinstate remains unanswered. Blank business-case rows for thresholds and some netting variants supply no expected assertions or execution.

[Source 23, lines 95-117](../../../../knowledge/evidence/sources/sha256/2635579967f19c33ff382f1c3a95b4e7693e62c6ad1d27380ee001a51c45ce0c.md#L95-L117) [Source 23, lines 140-143](../../../../knowledge/evidence/sources/sha256/2635579967f19c33ff382f1c3a95b4e7693e62c6ad1d27380ee001a51c45ce0c.md#L140-L143)

## Connections

The cited source clauses connect the roles, interfaces, and controls described above. Their scope remains limited to the cited revisions.

## Evidence limits

This candidate records selected source meaning. It establishes no execution, deployment, current policy, or human approval.

## Open questions

- Resolve effective manual-split scope for generic/IRS resultants and exact unreleased withdrawal parent/child states.
- Confirm released-child reversal accounting and safe operator actions.
- Confirm SWIFT_SUPPRESSED unsplit eligibility and threshold disable/delete contract.
- Provide the complete bounded distribution algorithm, selected static, TechFail result/comment and SI-retention rule.
