---
type: KnowledgeTopic
id: KT-settlement-ccil-netting
version: 1
owner: unknown
governance_state: candidate
status: draft
sources:
- id: SRC-512ace11dd56f19bf781d531
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Netting/CCIL Netting/page.md
  revision: sha256:a2ce9ca6a14777d7d688410c3c2c6b19caedf6f8a202f84c4253da78a93736a1
  sha256: a2ce9ca6a14777d7d688410c3c2c6b19caedf6f8a202f84c4253da78a93736a1
- id: SRC-5f68d1e47d5b2c04e8639c17
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Netting/Business User Case/02 CCIL Netting.md
  revision: sha256:e03e964bdf2adc695771ca3e066d3fe899f6823f4ccf6a864e5f53d24010e506
  sha256: e03e964bdf2adc695771ca3e066d3fe899f6823f4ccf6a864e5f53d24010e506
- id: SRC-d856b444e14a0493cc473bde
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Netting/Business User Case/02 CCIL Netting/page.md
  revision: sha256:e03e964bdf2adc695771ca3e066d3fe899f6823f4ccf6a864e5f53d24010e506
  sha256: e03e964bdf2adc695771ca3e066d3fe899f6823f4ccf6a864e5f53d24010e506
- id: SRC-83752d4f8891392fb5d5d81a
  resource: source:settlement-netting/Cash Settlement Home Page/Cash Settlement Home
    Page/Functional Requirement/Netting/Business User Case/02 CCIL Netting.md
  revision: sha256:e03e964bdf2adc695771ca3e066d3fe899f6823f4ccf6a864e5f53d24010e506
  sha256: e03e964bdf2adc695771ca3e066d3fe899f6823f4ccf6a864e5f53d24010e506
- id: SRC-2ed473c923bd76833481326f
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/CCIL
    Netting Design.md
  revision: sha256:246312dc39ff8687020ca048e6b01e19c992164d70b2a8b1c2d720bd83e8135f
  sha256: 246312dc39ff8687020ca048e6b01e19c992164d70b2a8b1c2d720bd83e8135f
- id: SRC-17f5cbc4dfeeb07df7397528
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/CCIL
    Netting Design/page.md
  revision: sha256:246312dc39ff8687020ca048e6b01e19c992164d70b2a8b1c2d720bd83e8135f
  sha256: 246312dc39ff8687020ca048e6b01e19c992164d70b2a8b1c2d720bd83e8135f
- id: SRC-a5bac081fa53386d1cebeb7d
  resource: source:settlement-netting/Cash Settlement Home Page/Cash Settlement Home
    Page/Tech Design/CCIL Netting Design.md
  revision: sha256:246312dc39ff8687020ca048e6b01e19c992164d70b2a8b1c2d720bd83e8135f
  sha256: 246312dc39ff8687020ca048e6b01e19c992164d70b2a8b1c2d720bd83e8135f
- id: SRC-36e628fbb28fa91eae5735d7
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/CCIL
    Netting Design/Stella CCIL Identify/page.md
  revision: sha256:3957b43f30b3c7b23f2b189d8f54d4349268db06b3bb48f67d7248d9fcb0550e
  sha256: 3957b43f30b3c7b23f2b189d8f54d4349268db06b3bb48f67d7248d9fcb0550e
- id: SRC-426393fda3ed4becdfc99390
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Netting/Netting
    Service - GUI & API intergration.md
  revision: sha256:88f99202a018ce56e4c173be3026561afc7342bc035ef97eb298491436682e24
  sha256: 88f99202a018ce56e4c173be3026561afc7342bc035ef97eb298491436682e24
- id: SRC-47997ab448281d8fdb1ba7a4
  resource: source:settlement-netting/Cash Settlement Home Page/Cash Settlement Home
    Page/Functional Requirement/Netting/Netting Service - GUI & API intergration.md
  revision: sha256:88f99202a018ce56e4c173be3026561afc7342bc035ef97eb298491436682e24
  sha256: 88f99202a018ce56e4c173be3026561afc7342bc035ef97eb298491436682e24
- id: SRC-337472978edf74a738f8a7c4
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Netting/Netting Service - GUI & API intergration/page.md
  revision: sha256:88f99202a018ce56e4c173be3026561afc7342bc035ef97eb298491436682e24
  sha256: 88f99202a018ce56e4c173be3026561afc7342bc035ef97eb298491436682e24
- id: SRC-29e240338779d97eca0bed84
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Cashflow
    Blotter/User Actions on Cashflow Blotter/page.md
  revision: sha256:55087e09edeb5dfb048c3665eee350c70629cb1efb194c9f7af8361d039c6891
  sha256: 55087e09edeb5dfb048c3665eee350c70629cb1efb194c9f7af8361d039c6891
generated:
  by: agent:codex
  at: '2026-11-15T10:49:56+00:00'
verified: []
classification: settlement
scope: Guaranteed and non-guaranteed CCIL workflows, tactical stamping, and staged
  IRS netting.
summary: Retained sources describe intended workflows. Conflicting criteria and dated
  proposals remain explicit pending owner review.
related:
- KT-settlement-manual-netting
- KT-settlement-beneficiary-bic-netting
- KT-settlement-auto-netting
- KT-settlement-cashflow-identity-and-stella-write-back
open_questions:
- Which SWIFT handling is authoritative for each tactical and FMRP CCIL flow?
- Who owns the CCIL client golden source, and when does the tactical list cease to
  apply?
- How does CCIL netting handle different-counterparty components when the general backend proposal requires a counterparty match?
- Which status gates govern CCIL netting across the GUI and API when the general action and backend lists differ?
- Which team owns novation review, gross exceptions, and static-data changes?
- Which approved change-control and testing route governs new CCIL client onboarding?
- Which decision authorizes staged IRS auto-netting and settlement-method inheritance
  for each India flow?
- Confirm canonical family/group predicates, CASH versus GROSS meaning, and final
  resultant state.
- Confirm corrected post-release cases and reconcile QUEUED/Unaffirmed mapping with
  affirmed scenario outcomes.
- Confirm the family/group labels and approved interface before implementation.
- Which lookup-failure and recovery contract is approved?
---
# India CCIL netting

## Scope

Guaranteed and non-guaranteed CCIL workflows, tactical stamping, and staged IRS netting.
This isolated proposal awaits canonical integration and human review.

## Summary

Retained sources describe intended workflows. Conflicting criteria and dated proposals remain explicit pending owner review.

## Documented knowledge

### NET-M-021

The CCIL requirement groups India guaranteed and non-guaranteed flows into a central-counterparty resultant. Its stated target bypasses SWIFT generation and retains accounting.

The central-counterparty identity is explicit in the detailed field mapping.
The dated 2026 scenario later shows manual SWIFT suppression, which needs reconciliation.
Source status: documented requirement. Source date: not established.
[Original lines 3–3](../../../evidence/sources/sha256/a2ce9ca6a14777d7d688410c3c2c6b19caedf6f8a202f84c4253da78a93736a1.md#L3) [Original lines 18–20](../../../evidence/sources/sha256/a2ce9ca6a14777d7d688410c3c2c6b19caedf6f8a202f84c4253da78a93736a1.md#L18-L20)

### NET-M-022

The tactical CCIL proposal copies Murex client static data into RATAN, corrects and reviews it, and retires that local approach after Murex 2.11 decommissioning.

The H1 2024 migration motivates the tactical design. NSTP rules, filters, and netting capability are described as reusable.
The strategy golden source and current static-data owner are not established.
Source status: tactical proposal. Source date: H1 2024.
[Original lines 12–14](../../../evidence/sources/sha256/a2ce9ca6a14777d7d688410c3c2c6b19caedf6f8a202f84c4253da78a93736a1.md#L12-L14) [Original lines 24–32](../../../evidence/sources/sha256/a2ce9ca6a14777d7d688410c3c2c6b19caedf6f8a202f84c4253da78a93736a1.md#L24-L32)

### NET-M-023

The CCIL matrix routes WAITING/Pending Netting flows with settlement method CCIL and FMID 400021949 to bilateral netting. Other counterparties use the CCIL action.

Generic bilateral flows have method != CCIL and state WAITING or READY.
The rule is scoped to this tactical matrix, not a universal counterparty mapping.
Source status: documented requirement. Source date: not established.
[Original lines 38–45](../../../evidence/sources/sha256/a2ce9ca6a14777d7d688410c3c2c6b19caedf6f8a202f84c4253da78a93736a1.md#L38-L45) [Original lines 149–150](../../../evidence/sources/sha256/a2ce9ca6a14777d7d688410c3c2c6b19caedf6f8a202f84c4253da78a93736a1.md#L149-L150) [Original lines 156–156](../../../evidence/sources/sha256/a2ce9ca6a14777d7d688410c3c2c6b19caedf6f8a202f84c4253da78a93736a1.md#L156)

### NET-M-024

The CCIL operating examples require discrepancy review and MO novation where necessary. Ad-hoc gross settlement requires a four-eye exception review.

Flows sharing central-counterparty FMID but outside CCIL settlement are not automatically included.
The examples are intended handling, not retained operational execution.
Source status: illustrative operating requirements. Source date: not established.
[Original lines 50–53](../../../evidence/sources/sha256/a2ce9ca6a14777d7d688410c3c2c6b19caedf6f8a202f84c4253da78a93736a1.md#L50-L53)

### NET-M-025

The CCIL onboarding example distinguishes a CR for client-list changes from a temporary NSTP hold rule. It describes manual Nostro checking and SWIFT suppression while awaiting onboarding.

The text gives historical lead times of weeks for CR and within one business day for the hold rule.
Do not treat those historical lead times or UAT wording as present release authorization.
Source status: historical operating agreement. Source date: not established.
[Original lines 53–53](../../../evidence/sources/sha256/a2ce9ca6a14777d7d688410c3c2c6b19caedf6f8a202f84c4253da78a93736a1.md#L53)

### NET-M-026

The June and August 2026 CCIL examples route IRS resultants into Pending Auto Netting. The later scheduled net marks intermediate IRS resultants DEAD and creates a new gross resultant.

The August non-guaranteed example expects CCIL Netting; the guaranteed example expects Bilateral Netting.
These dated examples do not state a current, generally approved scope for IRS re-netting or settlement-method inheritance.
Source status: dated expected FMRP workflow. Source date: 2026-06-24 and 2026-08-20.
[Original lines 54–71](../../../evidence/sources/sha256/a2ce9ca6a14777d7d688410c3c2c6b19caedf6f8a202f84c4253da78a93736a1.md#L54-L71) [Original lines 73–92](../../../evidence/sources/sha256/a2ce9ca6a14777d7d688410c3c2c6b19caedf6f8a202f84c4253da78a93736a1.md#L73-L92) [Original lines 94–113](../../../evidence/sources/sha256/a2ce9ca6a14777d7d688410c3c2c6b19caedf6f8a202f84c4253da78a93736a1.md#L94-L113)

### NET-M-027

The tactical Murex stamping rule uses entity FMID 4, family IRD, group IRS, currency INO, and the guaranteed FMID or maintained client list. Non-guaranteed resultants map to FMID 400021949 and CCIL/MMB.

The mapping specifies CASH settlement and CASH delivery, N plus 11 digits, QUEUED, and Unaffirmed.
The tactical predicate lists family IRD and group IRS. The technical design reverses those values. The owner must confirm the authoritative mapping.
Source status: tactical mapping proposal. Source date: not established.
[Original lines 136–139](../../../evidence/sources/sha256/a2ce9ca6a14777d7d688410c3c2c6b19caedf6f8a202f84c4253da78a93736a1.md#L136-L139) [Technical family/group predicate, line 10](../../../evidence/sources/sha256/246312dc39ff8687020ca048e6b01e19c992164d70b2a8b1c2d720bd83e8135f.md#L10) [Original lines 156–156](../../../evidence/sources/sha256/a2ce9ca6a14777d7d688410c3c2c6b19caedf6f8a202f84c4253da78a93736a1.md#L156)

### NET-M-028

The CCIL scenario sheet expects non-guaranteed components to become NETTED, creates an affirmed CCIL Netting resultant, and restores Pending Netting after reversal or recovery actions.

Key equality is entity, value date, and currency; counterparty may differ.
These expected outcomes are not executed tests. The post-release row uses bilateral labels.
Source status: expected scenario. Source date: not established.
[Original lines 3–7](../../../evidence/sources/sha256/e03e964bdf2adc695771ca3e066d3fe899f6823f4ccf6a864e5f53d24010e506.md#L3-L7) [Original lines 10–14](../../../evidence/sources/sha256/e03e964bdf2adc695771ca3e066d3fe899f6823f4ccf6a864e5f53d24010e506.md#L10-L14)

### NET-M-029

The CCIL technical design proposes adapter stamping, a settlement-method NSTP rule, dedicated preview controllers, and shared netting service logic.

The frontend proposal requires equal entity, value date, and currency, plus WAITING/Pending Netting.
The technical stamping predicate lists family IRS and group IRD, opposite to the tactical predicate in NET-M-027.
Source status: technical design proposal. Source date: not established.
[Original lines 10–13](../../../evidence/sources/sha256/246312dc39ff8687020ca048e6b01e19c992164d70b2a8b1c2d720bd83e8135f.md#L10-L13)

### NET-M-030

The Stella CCIL design proposes lookup by booking FMID, counterparty FMID, currency, family, and group. Lookup exceptions set settlement UNKNOWN; pre-check maps UNKNOWN to TechFail.

Static data service supplies the query API, table changes, and caching.
No source code, execution, retry policy, or deployed configuration was inspected.
Source status: technical design proposal. Source date: not established.
[Original lines 7–8](../../../evidence/sources/sha256/3957b43f30b3c7b23f2b189d8f54d4349268db06b3bb48f67d7248d9fcb0550e.md#L7-L8) [Original lines 10–10](../../../evidence/sources/sha256/3957b43f30b3c7b23f2b189d8f54d4349268db06b3bb48f67d7248d9fcb0550e.md#L10)

### NET-M-031

The broader backend proposal requires payment currency, payment date, booking entity, and counterparty FMID to match across component cashflows. The CCIL technical proposal separately permits different counterparties for CCIL flows. It does not define how the two rules interact.

These are documented proposals. The applicable CCIL backend exception and its implementation remain unconfirmed.
Source status: conflicting functional and technical proposals. Source date: not established.
[General backend component validation, line 17](../../../evidence/sources/sha256/88f99202a018ce56e4c173be3026561afc7342bc035ef97eb298491436682e24.md#L17) [CCIL netting service proposal, line 12](../../../evidence/sources/sha256/246312dc39ff8687020ca048e6b01e19c992164d70b2a8b1c2d720bd83e8135f.md#L12)

### NET-M-032

The general GUI guide lists netting actions for Projected, Queued, Pending, Validated, Ready, Waiting, or Hold cashflows with blank netting IDs. The backend proposal lists Projected, Queued, Pending, or Validated states. The CCIL matrix requires WAITING with Pending Netting, while the Cashflow Blotter action lists Pending Netting or Pending Auto Netting.

The sources do not establish one consistent status gate or the precedence between GUI actions and backend validation.
Source status: conflicting functional and technical proposals. Source date: not established.
[General GUI netting gate, line 5](../../../evidence/sources/sha256/88f99202a018ce56e4c173be3026561afc7342bc035ef97eb298491436682e24.md#L5) [General backend status gate, line 17](../../../evidence/sources/sha256/88f99202a018ce56e4c173be3026561afc7342bc035ef97eb298491436682e24.md#L17) [CCIL matrix, lines 41–45](../../../evidence/sources/sha256/a2ce9ca6a14777d7d688410c3c2c6b19caedf6f8a202f84c4253da78a93736a1.md#L41-L45) [CCIL blotter action, line 28](../../../evidence/sources/sha256/55087e09edeb5dfb048c3665eee350c70629cb1efb194c9f7af8361d039c6891.md#L28)

## Connections

The scheduled workflow remains in `KT-settlement-auto-netting`.
Resultant identity remains in `KT-settlement-cashflow-identity-and-stella-write-back`.
The sibling proposals separate bilateral, BIC, and CCIL rules.

## Evidence limits

Only reviewed source views supplied domain evidence.
Missing images, populated static tables, and external stories remain unavailable.
Scenario sheets provide expected behavior, without executed assertions.
Struck-through refresh rules and copied post-release scenarios cannot establish current policy.
No source date alone establishes authority or supersession.
Owner review must resolve the conflicts before these proposals support definitive requirements.

## Open questions

Owner: unknown.

- Which SWIFT handling is authoritative for each tactical and FMRP CCIL flow?
- Who owns the CCIL client golden source, and when does the tactical list cease to apply?
- How does CCIL netting handle different-counterparty components when the general backend proposal requires a counterparty match?
- Which status gates govern CCIL netting across the GUI and API when the general action and backend lists differ?
- Which team owns novation review, gross exceptions, and static-data changes?
- Which approved change-control and testing route governs new CCIL client onboarding?
- Which decision authorizes staged IRS auto-netting and settlement-method inheritance for each India flow?
- Confirm canonical family/group predicates, CASH versus GROSS meaning, and final resultant state.
- Confirm corrected post-release cases and reconcile QUEUED/Unaffirmed mapping with affirmed scenario outcomes.
- Confirm the family/group labels and approved interface before implementation.
- Which lookup-failure and recovery contract is approved?
