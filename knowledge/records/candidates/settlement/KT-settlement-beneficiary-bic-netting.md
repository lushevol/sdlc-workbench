---
type: KnowledgeTopic
id: KT-settlement-beneficiary-bic-netting
version: 1
owner: unknown
governance_state: candidate
status: draft
sources:
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Netting/Beneficiary
    BIC Netting.md
  revision: sha256:9d71b3560ee2400e9bc35283507101ca99de6d4cf1fb5f126f293ee9837cde62
  sha256: 9d71b3560ee2400e9bc35283507101ca99de6d4cf1fb5f126f293ee9837cde62
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Netting/Beneficiary
    BIC Netting/page.md
  revision: sha256:9d71b3560ee2400e9bc35283507101ca99de6d4cf1fb5f126f293ee9837cde62
  sha256: 9d71b3560ee2400e9bc35283507101ca99de6d4cf1fb5f126f293ee9837cde62
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Netting/Beneficiary
    BIC Netting/Beneficiary BIC Netting Demo.md
  revision: sha256:f9a862207bd017ab0d329975bffa3b9ca9b92603a867a9bcebc8e8c56d2475a4
  sha256: f9a862207bd017ab0d329975bffa3b9ca9b92603a867a9bcebc8e8c56d2475a4
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Netting/Beneficiary
    BIC Netting/Beneficiary BIC Netting Demo/page.md
  revision: sha256:f9a862207bd017ab0d329975bffa3b9ca9b92603a867a9bcebc8e8c56d2475a4
  sha256: f9a862207bd017ab0d329975bffa3b9ca9b92603a867a9bcebc8e8c56d2475a4
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Netting/Business User
    Case/03 Beneficiary BIC Netting.md
  revision: sha256:88191dbdf57f27dd63de4fa6c5d2006b4283fc533826f0dee623426c80fad8e9
  sha256: 88191dbdf57f27dd63de4fa6c5d2006b4283fc533826f0dee623426c80fad8e9
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Netting/Business User
    Case/03 Beneficiary BIC Netting/page.md
  revision: sha256:88191dbdf57f27dd63de4fa6c5d2006b4283fc533826f0dee623426c80fad8e9
  sha256: 88191dbdf57f27dd63de4fa6c5d2006b4283fc533826f0dee623426c80fad8e9
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Netting/Beneficiary
    BIC Netting/Beneficiary BIC Netting Demo.md
  revision: sha256:f9a862207bd017ab0d329975bffa3b9ca9b92603a867a9bcebc8e8c56d2475a4
  sha256: f9a862207bd017ab0d329975bffa3b9ca9b92603a867a9bcebc8e8c56d2475a4
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Netting/Beneficiary
    BIC Netting.md
  revision: sha256:9d71b3560ee2400e9bc35283507101ca99de6d4cf1fb5f126f293ee9837cde62
  sha256: 9d71b3560ee2400e9bc35283507101ca99de6d4cf1fb5f126f293ee9837cde62
- resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/Netting/Business
    User Case/03 Beneficiary BIC Netting.md
  revision: sha256:88191dbdf57f27dd63de4fa6c5d2006b4283fc533826f0dee623426c80fad8e9
  sha256: 88191dbdf57f27dd63de4fa6c5d2006b4283fc533826f0dee623426c80fad8e9
generated:
  by: agent:sol-auto-netting-review
  at: '2026-11-16T08:52:24.654494+08:00'
verified: []
classification: settlement
scope: Beneficiary BIC eligibility, manual controls, resultant mapping, and affirmation.
summary: Retained sources describe intended workflows. Conflicting criteria and dated proposals remain explicit
  pending owner review.
related:
- KT-settlement-manual-netting
- KT-settlement-ccil-netting
- KT-settlement-auto-netting
- KT-settlement-cashflow-identity-and-stella-write-back
open_questions:
- Who owns and approves BIC eligibility rules, applicable entities, and the SCI mediumUsage contract?
- 'Which BIC key applies: the prototype fields or the additional product fields in the July 2024 minutes?'
- Which resultant mapping governs payment type, counterparty selection, and the ordering of component cashflows?
- Which affirmation stage, maintenance profiles, and strategic SWIFT cancellation-message requirements apply?
- What complete component and resultant transitions apply after release or settlement?
---
# Beneficiary BIC netting

## Scope

Beneficiary BIC eligibility, manual controls, resultant mapping, and affirmation.
This isolated proposal awaits canonical integration and human review.

## Summary

Retained sources describe intended workflows. Conflicting criteria and dated proposals remain explicit pending owner review.

## Documented knowledge

### NET-M-010

The beneficiary BIC requirement calls for configurable eligibility filters and operator-controlled manual grouping. BIC netting has priority over bilateral manual netting.

Entity, value date, counterparty, and BIC label participate in the described controls.
Do not infer any new role or permission mapping from operator control.
Source status: documented requirement. Source date: not established.
[Original lines 3–8](../../../evidence/sources/sha256/9d71b3560ee2400e9bc35283507101ca99de6d4cf1fb5f126f293ee9837cde62.md#L3-L8)

### NET-M-011

The selected BIC eligibility description names London and identifies beneficiary BIC through SCI mediumUsage=MXR. The Payment Date >= Today condition is struck through.

The PAYSTP_NET expansion contains no populated rows in the selected content.
Do not turn the struck-through date check into an active constraint.
Source status: documented requirement. Source date: not established.
[Original lines 12–27](../../../evidence/sources/sha256/9d71b3560ee2400e9bc35283507101ca99de6d4cf1fb5f126f293ee9837cde62.md#L12-L27)

### NET-M-012

The prototype shows the BIC Netting button only when selected components share these values: BIC_Net flag, beneficiary BIC, value date, currency, and entity.
Execution additionally requires BIC_Net=Y and Pending Netting.

All listed fields must match across selected components.
The button condition says the same flag; execution explicitly requires Y.
The 15 July 2024 minutes also include Family, Group, Type, Typology, and Strategy in the BIC netting key.
That additional product-key restriction is absent from the prototype list. Its effective scope remains unresolved.
[July key, original line 80](../../../evidence/sources/sha256/9d71b3560ee2400e9bc35283507101ca99de6d4cf1fb5f126f293ee9837cde62.md#L80)
Source status: documented requirement. Source date: not established.
[Original lines 37–43](../../../evidence/sources/sha256/9d71b3560ee2400e9bc35283507101ca99de6d4cf1fb5f126f293ee9837cde62.md#L37-L43) [Original lines 57–57](../../../evidence/sources/sha256/9d71b3560ee2400e9bc35283507101ca99de6d4cf1fb5f126f293ee9837cde62.md#L57)

### NET-M-013

The BIC resultant design allocates N plus 11 digits, sets QUEUED and Unaffirmed, assigns a UUID netting ID, and uses GROSS settlement with CASH delivery.

The design also initializes cashflow and business versions to zero.
The table leaves payment type blank; the BIC scenario sheet expects Ben BIC Netting.
Source status: proposed resultant mapping. Source date: not established.
[Original lines 58–58](../../../evidence/sources/sha256/9d71b3560ee2400e9bc35283507101ca99de6d4cf1fb5f126f293ee9837cde62.md#L58)

### NET-M-014

The BIC mapping says to select a counterparty randomly and keep its shortcode consistent. It inherits product attributes and trade ID only when component values agree; otherwise it leaves them empty.

Family, group, type, typology, strategy, and trade ID are named. Taxonomy and CFI are restamped.
Other attributes copy from the first cashflow; no deterministic component order is established.
Source status: proposed resultant mapping. Source date: not established.
[Original lines 58–58](../../../evidence/sources/sha256/9d71b3560ee2400e9bc35283507101ca99de6d4cf1fb5f126f293ee9837cde62.md#L58)

### NET-M-015

The 15 July 2024 BIC minutes require a displayed resultant ID, NSTP/Pending Affirmation, affirmation after generation, and maker-checker verification.

Affirmation information is not required in the pre-netting review page.
The minutes require SWIFT 192/292 for the strategic solution.
They defer the response-time discussion.
Source status: recorded meeting requirements. Source date: 2024-07-15.
[Original lines 78–87](../../../evidence/sources/sha256/9d71b3560ee2400e9bc35283507101ca99de6d4cf1fb5f126f293ee9837cde62.md#L78-L87)

### NET-M-017

The BIC demo description proposes user-maintained eligibility through FMO_BR_APR and FMO_BR_MKR, automatic WAITING/Pending Netting, optional Settle As Gross, and pre-release auto-un-netting.

Pre-release auto-un-netting follows component amendment or withdrawal.
These source profile names do not define authorization in other systems.
Source status: demo requirement proposal. Source date: not established.
[Original lines 18–25](../../../evidence/sources/sha256/f9a862207bd017ab0d329975bffa3b9ca9b92603a867a9bcebc8e8c56d2475a4.md#L18-L25)

### NET-M-018

The BIC demo requires affirmation when validating the resultant and keeps SCI mediumUsage=MXR as an open question.

Shared product attributes and trade ID inherit only when equal.
The requirement page states MXR, while the demo retains it as a question.
Source status: demo requirement proposal. Source date: not established.
[Original lines 24–25](../../../evidence/sources/sha256/f9a862207bd017ab0d329975bffa3b9ca9b92603a867a9bcebc8e8c56d2475a4.md#L24-L25) [Original lines 39–41](../../../evidence/sources/sha256/f9a862207bd017ab0d329975bffa3b9ca9b92603a867a9bcebc8e8c56d2475a4.md#L39-L41)

### NET-M-019

The BIC scenario sheet expects mixed Murex and Stella components to net, manual un-netting to restore Pending Netting, and different keys to prevent netting.

The sheet names Ben BIC Netting and maker-checker completion. Settle As Gross leaves a selected flow in Pending Exception.
The mismatched-key scenario describes a preview refusal without a CCIL-style UI warning.
The sheet's released-resultant case instead uses bilateral action and payment-type labels.
Its component outcomes are incomplete and cannot establish a complete BIC post-release policy.
[Conflicting case, original line 8](../../../evidence/sources/sha256/88191dbdf57f27dd63de4fa6c5d2006b4283fc533826f0dee623426c80fad8e9.md#L8)
Source status: expected scenario. Source date: not established.
[Original lines 3–7](../../../evidence/sources/sha256/88191dbdf57f27dd63de4fa6c5d2006b4283fc533826f0dee623426c80fad8e9.md#L3-L7) [Original lines 10–14](../../../evidence/sources/sha256/88191dbdf57f27dd63de4fa6c5d2006b4283fc533826f0dee623426c80fad8e9.md#L10-L14)

## Connections

The scheduled workflow remains in `KT-settlement-auto-netting`.
Resultant identity remains in `KT-settlement-cashflow-identity-and-stella-write-back`.
The sibling topics separate bilateral, BIC, and CCIL rules.

## Evidence limits

The cited selected passages support these source-specific proposals.
The review does not establish complete source, schema, or workflow coverage.
Missing images, populated static tables, and external stories remain unavailable.
Scenario sheets provide expected behavior, without executed assertions.
Struck-through refresh rules and copied post-release scenarios cannot establish current policy.
No source date alone establishes authority or supersession.
Owner review must resolve the conflicts before these proposals support definitive requirements.

## Open questions

Owner: unknown.

- Who owns and approves BIC eligibility rules, applicable entities, and the SCI mediumUsage contract?
- Which BIC key applies: the prototype fields or the additional product fields in the July 2024 minutes?
- Which resultant mapping governs payment type, counterparty selection, and the ordering of component cashflows?
- Which affirmation stage, maintenance profiles, and strategic SWIFT cancellation-message requirements apply?
- What complete component and resultant transitions apply after release or settlement?
