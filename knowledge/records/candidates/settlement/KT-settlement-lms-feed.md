---
type: KnowledgeTopic
id: KT-settlement-lms-feed
version: 1
owner: unknown
governance_state: candidate
status: draft
classification: settlement
scope: RATAN cashflow eligibility, entity scope, payload fields, and LMS consumption.
summary: The reviewed 2023 rule covers released and settled cashflows. Later proposals broaden entity delivery and add some
  receipt events.
sources:
- id: SRC-d9395ef13337815ed6b2930c
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Surrounding System Integration/LMS
    Feed/page.md
  revision: sha256:000779415d39ee3787259cdae6646ec26bb10ac2fe8dad8367a32e8aa4b30118
  sha256: 000779415d39ee3787259cdae6646ec26bb10ac2fe8dad8367a32e8aa4b30118
- id: SRC-e3f43b080d634b27d61a0a12
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Settlement Day2 Requirement/LMS/Include
    Swift Suppressed status in LMS feed (only for receipts)/page.md
  revision: sha256:b284c8591daf044d40e88e4d2e050c9fef51bdf943ca8605a123f5ac6ef516b0
  sha256: b284c8591daf044d40e88e4d2e050c9fef51bdf943ca8605a123f5ac6ef516b0
- id: SRC-ef2234a83e1732ff3e1f76e3
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Settlement Day2 Requirement/LMS/LMS
    - Remove the entity filter in LMS feed/page.md
  revision: sha256:1dc5b93719af2cbee98e77408b4b40adc495b717eb6e31f4519d97cebac51b8e
  sha256: 1dc5b93719af2cbee98e77408b4b40adc495b717eb6e31f4519d97cebac51b8e
- id: SRC-46c14e159ee07f02369b0821
  resource: source:ratan-51358/RATAN - 51358/RATAN -Interfaces/Ratan and LMS 50686/page.md
  revision: sha256:5db209ace4456e002ce43e6123ffd33666a1b3f4d335058d69d59c86c04da746
  sha256: 5db209ace4456e002ce43e6123ffd33666a1b3f4d335058d69d59c86c04da746
- id: SRC-0d60837a781b41fc6aa621c6
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Surrounding System Integration/Source
    Stack Flow Name in LMS Feed/page.md
  revision: sha256:a6c6a0fe35529ad22d5009986d81b057b6568e2eda7af7d24e0fb7e146c9840e
  sha256: a6c6a0fe35529ad22d5009986d81b057b6568e2eda7af7d24e0fb7e146c9840e
- id: SRC-256b00485f16723a43eb2aa2
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/RATANONE Cash Settlement Technical Design/Ratan
    - LMS feed/page.md
  revision: sha256:ef80d9b2baac593bbaac2d8cbb0ef8abbfa5fc02143a4dce172ce2dd460fbaf8
  sha256: ef80d9b2baac593bbaac2d8cbb0ef8abbfa5fc02143a4dce172ce2dd460fbaf8
- id: SRC-d1adf07cf5a7409022497053
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/LMS Integration/page.md
  revision: sha256:0c993b048f5ee1bb09fa5150dcc150533bf8f96ad18d0ae8b67719539fe450e4
  sha256: 0c993b048f5ee1bb09fa5150dcc150533bf8f96ad18d0ae8b67719539fe450e4
generated:
  by: agent:codex
  at: '2026-11-15T09:09:18.836152+00:00'
verified: []
related: []
open_questions:
- Which statuses, settlement means, beneficiary BIC rules, and account fields apply to each LMS consumer and payment flow?
- Which Swift Suppressed receipt events should LMS accept for undo, withdrawal, and manual failure?
- Which replacement or correction payload does LMS need if account stamping is unavailable?
- Which entities may RATAN send, and which entities must each LMS consumer exclude?
- Which source value, Field 20 prefix, and netting-resultant fallback apply to each Murex, Stella, and LOANIQ flow?
- What should RATAN send when allotment or product taxonomy is blank outside the cross-product netting case?
---
# Settlement cashflow feeds to LMS

## Scope

RATAN cashflow eligibility, entity scope, payload fields, and Liquidity Management System (LMS) consumption.

## Summary

The reviewed 2023 rule describes payment release and settlement feeds. Later proposals broaden RATAN entity delivery and add some receipt events.

## Documented knowledge

### Release and settlement baseline

The July 2023 page records business agreement for the then-current feed. It lists RELEASED and SETTLED as feedable. Settlement means must be NOS. Beneficiary BIC `REJECTXXALL` excludes the cashflow. The page requires Nostro and Vostro for SCB pay and Nostro for SCB receive. [Reviewed baseline](../../../evidence/sources/sha256/000779415d39ee3787259cdae6646ec26bb10ac2fe8dad8367a32e8aa4b30118.md#L1-L2) [States and accounts](../../../evidence/sources/sha256/000779415d39ee3787259cdae6646ec26bb10ac2fe8dad8367a32e8aa4b30118.md#L12-L25) [Settlement means and BIC](../../../evidence/sources/sha256/000779415d39ee3787259cdae6646ec26bb10ac2fe8dad8367a32e8aa4b30118.md#L89-L103)

The baseline examples require booking entity eligibility. A released withdrawal can feed after maker/checker action. A withdrawal in WAITING with Pending Exception does not feed at that step. The settled receipt example sets Notice to Receive to N. [Withdrawal and receipt examples](../../../evidence/sources/sha256/000779415d39ee3787259cdae6646ec26bb10ac2fe8dad8367a32e8aa4b30118.md#L75-L85)

### Proposed receive-only Swift suppression

The October 2025 proposal adds a feed for a receive-only cashflow in Swift Suppressed. The payment can arrive despite suppressed SWIFT and no RATAN Nostro payment. The page records an internal request to send another message on undo and on withdrawal to CANCELLED. The scenario table still lists those two events as pending confirmation with LMS. The template, FAILED transition behavior, and stamping data remain open. [Proposed statuses](../../../evidence/sources/sha256/b284c8591daf044d40e88e4d2e050c9fef51bdf943ca8605a123f5ac6ef516b0.md#L5-L13) [Transition decisions and questions](../../../evidence/sources/sha256/b284c8591daf044d40e88e4d2e050c9fef51bdf943ca8605a123f5ac6ef516b0.md#L25-L39)

### Entity scope and downstream delivery

The October 2025 entity proposal removes RATAN's booking entity filter. It keeps the message template. This is a sender-side change. Confirm downstream consumption and which other feed conditions apply to the wider scope. [Entity proposal](../../../evidence/sources/sha256/1dc5b93719af2cbee98e77408b4b40adc495b717eb6e31f4519d97cebac51b8e.md#L9-L20) [Baseline page enhancement](../../../evidence/sources/sha256/000779415d39ee3787259cdae6646ec26bb10ac2fe8dad8367a32e8aa4b30118.md#L49) [Enhancement and examples](../../../evidence/sources/sha256/000779415d39ee3787259cdae6646ec26bb10ac2fe8dad8367a32e8aa4b30118.md#L72-L85)

A separate interface catalog describes RATAN delivery to LMS through Solace. It lists Stella feeds for HK, UK, SG, and Jersey, with a Jersey exclusion for SAIL-LMS. It lists LOANIQ feed scope as UK, SG, and HK. Its FMRP list names CN, IN, SG, UK, DE, HK, Dubai, New York, and DIFC. The catalog also lists separate FMRP exclusions for SAIL-LMS. These are catalog scopes. Confirm which LMS consumer and period they apply to after the proposed RATAN filter removal. [Interface country and product matrix](../../../evidence/sources/sha256/5db209ace4456e002ce43e6123ffd33666a1b3f4d335058d69d59c86c04da746.md#L9-L19) [Solace delivery](../../../evidence/sources/sha256/5db209ace4456e002ce43e6123ffd33666a1b3f4d335058d69d59c86c04da746.md#L21-L23)

### Source values, netting, and Field 20

The feed page assigns LMS responsibility for deriving the Field 20 prefix. Its table maps STELLA to EQ, LOANIQ to LQ, and FMRP to DV. Its prose cites MX for the Razor SWIFT on the FMRP China flow. Confirm whether these are separate consumer outputs and when each mapping applies. [Source and prefix rules](../../../evidence/sources/sha256/000779415d39ee3787259cdae6646ec26bb10ac2fe8dad8367a32e8aa4b30118.md#L105-L117)

The source stack design routes settlement by `Source_Stack_Flow_Name`. It maps BCSSTELLA to BCS and FMRPSTELLA and FMRPSTELLA-LOANIQ to FMRP. It excludes NativeSTELLA from RATAN. Proposal 1 uses the selected stack mapping to populate the existing LMS source field. It retains STELLA for the BCS example. Proposal 2 adds a separate field and is marked rejected. [Routing and current values](../../../evidence/sources/sha256/a6c6a0fe35529ad22d5009986d81b057b6568e2eda7af7d24e0fb7e146c9840e.md#L5-L12) [Current message fields](../../../evidence/sources/sha256/a6c6a0fe35529ad22d5009986d81b057b6568e2eda7af7d24e0fb7e146c9840e.md#L16-L28) [Proposal 1](../../../evidence/sources/sha256/a6c6a0fe35529ad22d5009986d81b057b6568e2eda7af7d24e0fb7e146c9840e.md#L30-L38) [Rejected proposal](../../../evidence/sources/sha256/a6c6a0fe35529ad22d5009986d81b057b6568e2eda7af7d24e0fb7e146c9840e.md#L40-L42)

The source stack table proposes that netting resultants inherit a common stack or fallback to FMRPSTELLA in its Murex example. It lists both FMRPSTELLA and FMRPMUREX as possible LMS values for Murex. The short technical note shows FMRPSTELLA as its Murex/Stella default. Confirm the common-component and mixed-component mapping before use. [Netting and Murex mapping](../../../evidence/sources/sha256/a6c6a0fe35529ad22d5009986d81b057b6568e2eda7af7d24e0fb7e146c9840e.md#L30-L38) [Technical mapping note](../../../evidence/sources/sha256/ef80d9b2baac593bbaac2d8cbb0ef8abbfa5fc02143a4dce172ce2dd460fbaf8.md#L1-L6)

The proposal stages netting stack derivation before changing the LMS message value. It records backward compatibility for FMRP and LOANIQ values. [Proposed sequence](../../../evidence/sources/sha256/a6c6a0fe35529ad22d5009986d81b057b6568e2eda7af7d24e0fb7e146c9840e.md#L56-L63) [Backward compatibility answer](../../../evidence/sources/sha256/a6c6a0fe35529ad22d5009986d81b057b6568e2eda7af7d24e0fb7e146c9840e.md#L79-L81)

The feed page proposes defaulting blank allotment to `NETTING RESULTANT` for cross-product netting resultants with an N-prefixed ID. The entity proposal leaves the general null-product-taxonomy rule open. [Cross-product fallback](../../../evidence/sources/sha256/000779415d39ee3787259cdae6646ec26bb10ac2fe8dad8367a32e8aa4b30118.md#L119-L122) [Null taxonomy question](../../../evidence/sources/sha256/1dc5b93719af2cbee98e77408b4b40adc495b717eb6e31f4519d97cebac51b8e.md#L13-L14)

### Event sources

The design tracks the lifecycle cashflow publication, stamping completion, and successful trade LEID and trader enrichment. They appear on the orchestration, cashflow domain, and trade event topics respectively. This table records listeners. It leaves the corresponding send predicates blank. [Event and topic table](../../../evidence/sources/sha256/0c993b048f5ee1bb09fa5150dcc150533bf8f96ad18d0ae8b67719539fe450e4.md#L19-L23)

## Connections

The source-stack design depends on netting-resultant metadata. LMS status and taxonomy rules also apply to payment-flow integration. Country onboarding, accounting, release remediation, and payment adjustment each need their own scoped treatment.

## Evidence limits

The July 2023 document records agreement for its baseline scope. The later publisher changes need an effective date and the applicable downstream consumer contract. The selected views omit attachments and parts of the original pages. The change records give candidate behavior.

## Open questions

- Which statuses, settlement means, beneficiary BIC rules, and account fields apply to each LMS consumer and payment flow?
- Which Swift Suppressed receipt events should LMS accept for undo, withdrawal, and manual failure?
- Which replacement or correction payload does LMS need if account stamping is unavailable?
- Which entities may RATAN send, and which entities must each LMS consumer exclude?
- Which source value, Field 20 prefix, and netting-resultant fallback apply to each Murex, Stella, and LOANIQ flow?
- What should RATAN send when allotment or product taxonomy is blank outside the cross-product netting case?
