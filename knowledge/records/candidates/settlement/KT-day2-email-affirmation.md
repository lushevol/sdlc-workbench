---
type: KnowledgeTopic
id: KT-day2-email-affirmation
version: 1
owner: unknown
governance_state: candidate
status: draft
verified: []
sources:
- id: SRC-5f150b010a4978d537bc8727
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Settlement Day2 Requirement/Derivative Settlement Affirmation - Email
    Automation/page.md
  revision: sha256:22b6ca79e747d45699bdb105511c47b54f1b29829a4cef75ea3ff8d21d79c24d
  sha256: 22b6ca79e747d45699bdb105511c47b54f1b29829a4cef75ea3ff8d21d79c24d
- id: SRC-a44d21a651d420650d26b13c
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Settlement Day2 Requirement/Email Affirmation Automation/Email Affirmation
    Automation Tech Design/page.md
  revision: sha256:0c9eec2b7386a00b7f2c8f6b10e0bef07c1945a498a49d2d4d9faf73dea82e18
  sha256: 0c9eec2b7386a00b7f2c8f6b10e0bef07c1945a498a49d2d4d9faf73dea82e18
- id: SRC-11d947fb43420e648914539f
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Settlement Day2 Requirement/Email Affirmation Automation/page.md
  revision: sha256:d4ab25d502ce4c21b002f10d0e5f0d9916aa92269f8a12148c54c2b4bd59e95e
  sha256: d4ab25d502ce4c21b002f10d0e5f0d9916aa92269f8a12148c54c2b4bd59e95e
- id: SRC-41b572c37582fccbc7c8726f
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional
    Requirement/Settlement Day2 Requirement/Trade event trigger cashflow STP/page.md
  revision: sha256:b5a5cd9e6118b1cf502751949cd4843098a463d0cfffac3a6281fa58dc7a2f53
  sha256: b5a5cd9e6118b1cf502751949cd4843098a463d0cfffac3a6281fa58dc7a2f53
classification: settlement
scope: Email and trade-driven affirmation control intent
summary: Source-specific intended rules and proposals retain their conditions and
  unresolved authority.
related:
- KT-settlement-multi-exception-control
- INT-KT-ratan-reference-and-control-interfaces
open_questions:
- 'KDQ-e4089deafe: Which dated publication filters, mandatory fields, schedules, and
  AI-review controls govern email affirmation?'
- 'KDQ-a911d63bc2: Which trade event maps to which Trade_State, and what downstream
  STP action follows the affirmation predicate?'
generated:
  by: agent:codex:sol-functional-lane-3-review
  at: '2026-11-16T01:44:20.716757+00:00'
writing_review:
  standard: ASD-STE100
  automated_check: PASSED
  asd_review: PENDING
  reviewer: null
  reviewed_at: null
  limitations:
  - Automated checks do not establish complete writing review.
---
# Email and trade-driven affirmation control intent

## Scope

Email and trade-driven affirmation control intent.
This candidate retains documented intent and source-specific proposals.

## Summary

The selected sources define related responsibilities, predicates, and exceptions.
Their effective authority and current applicability remain unresolved.

## Documented knowledge

### AFF-01 — Outbound publication scope

RATAN publishes selected cashflows with client SSI and SCB Nostro details to CDUPS.
Netting scope includes the net amount and component breakdown.
The proposal makes eligibility configurable by booking entity, client FMID/BIC, product granularity, portfolio, source, payment type, and settlement method.
Status scenarios differ: one selects WAITING/Pending Operator, while another includes valid client flows that already passed STP.
Pending-fixing and Pending Another Leg flows remain excluded from publication.
Dated refinements exclude corporate Eclipse portfolios, SIP strategies, SLT-CUST/loan flows, and Swap Agent Coupon/Interim MTM.
The March refinement also excludes CCIL deals. Islamic ISL-portfolio handling remains a feasibility question.
These dated refinements qualify the broader configuration proposal; they are not one accepted current universal filter.

[Original evidence](../../../evidence/sources/sha256/22b6ca79e747d45699bdb105511c47b54f1b29829a4cef75ea3ff8d21d79c24d.md#L1-L13). [Original evidence](../../../evidence/sources/sha256/22b6ca79e747d45699bdb105511c47b54f1b29829a4cef75ea3ff8d21d79c24d.md#L39-L68).

### AFF-02 — Scheduling, contacts, and distribution audit

The proposal supports configurable publication times by entity and client, manual regeneration, and an ad hoc stop.
CDUPS owns templates and separate affirmation contacts, with maker/checker maintenance at FMID/BIC and product scope.
CDUPS sends through MDIS and encrypts attachments to Bank standards. The selected text gives no specific encryption configuration.
CDUPS returns dispatch success/failure and timing to RATAN. RATAN exposes sent, failed, and pending-response filters.
A failure for one recipient among several must notify SCB contacts. Sender identity remains unspecified.
Phase 2 chasers reuse the original email. Post-send additions and pre-send ad hoc exclusions retain unresolved handling.

[Original evidence](../../../evidence/sources/sha256/22b6ca79e747d45699bdb105511c47b54f1b29829a4cef75ea3ff8d21d79c24d.md#L7-L13). [Original evidence](../../../evidence/sources/sha256/22b6ca79e747d45699bdb105511c47b54f1b29829a4cef75ea3ff8d21d79c24d.md#L65-L72).

### AFF-03 — Inbound AI response control

The intended AI layer classifies client responses as positive or negative/ambiguous.
A positive response removes the pending-affirmation exception through maker automation and marks its AI origin for the checker.
Other outstanding exceptions keep the cashflow NSTP. A positive email does not approve or release every cashflow automatically.
Negative or ambiguous responses require a maker indicator and manual intervention.
The audit trail records the outbound email and received response.

[Original evidence](../../../evidence/sources/sha256/22b6ca79e747d45699bdb105511c47b54f1b29829a4cef75ea3ff8d21d79c24d.md#L74-L82).

### AFF-04 — Proposed email fields and transport

The technical field table remains subject to business confirmation.
It proposes mandatory Trade ID, FlowID, value date, counterparty, currency, amount, and pay/receive indicator.
For net resultants, Trade ID is `Net`; entity and counterparty can be blank under the table descriptions.
That blank-counterparty allowance conflicts with its mandatory marker and requires resolution.
Pay amounts are negative and receive amounts positive in this proposed email representation.
Taxonomy, portfolio, strategy, and beneficiary details are optional in the table.
The transport proposal uses Solace and distribution ACK/NACK. NFRs remain unconfirmed.

[Original evidence](../../../evidence/sources/sha256/0c9eec2b7386a00b7f2c8f6b10e0bef07c1945a498a49d2d4d9faf73dea82e18.md#L16-L33). [Original evidence](../../../evidence/sources/sha256/0c9eec2b7386a00b7f2c8f6b10e0bef07c1945a498a49d2d4d9faf73dea82e18.md#L35-L41).

### AFF-05 — Scheduled outbound versus inbound trigger

The use case starts with WAITING/Pending Affirmation, schedules an outbound email, and uses a client reply to close the exception.
Its selection conditions, subject, sender/recipient properties, exception cases, and VD-1 timing remain open.
The selected use-case Expected Result cell is empty. It cannot establish an approved complete release sequence.

[Original evidence](../../../evidence/sources/sha256/d4ab25d502ce4c21b002f10d0e5f0d9916aa92269f8a12148c54c2b4bd59e95e.md#L3-L6). [Original evidence](../../../evidence/sources/sha256/d4ab25d502ce4c21b002f10d0e5f0d9916aa92269f8a12148c54c2b4bd59e95e.md#L10-L14). [Original evidence](../../../evidence/sources/sha256/d4ab25d502ce4c21b002f10d0e5f0d9916aa92269f8a12148c54c2b4bd59e95e.md#L16). [Original evidence](../../../evidence/sources/sha256/d4ab25d502ce4c21b002f10d0e5f0d9916aa92269f8a12148c54c2b4bd59e95e.md#L18-L21). [Original evidence](../../../evidence/sources/sha256/d4ab25d502ce4c21b002f10d0e5f0d9916aa92269f8a12148c54c2b4bd59e95e.md#L23-L27).

### AFF-06 — Separate trade-state input and affirmation predicate

A separate trade-event note lists three inputs that trigger a Trade_State change.
They are Inbound Completed paired with Match Completed, Inbound Not Required, or Match Outside CDU.
The note does not map each input to its resulting Trade_State.
Its NSTP predicate requires all three: Trade_State differs from AFFIRMED, Trade_State differs from CONFIRMED, and cashflow affirmation differs from Affirmed.
This predicate is distinct from email dispatch success and AI response classification. Neither supplies the missing state mapping.

[Original evidence](../../../evidence/sources/sha256/b5a5cd9e6118b1cf502751949cd4843098a463d0cfffac3a6281fa58dc7a2f53.md#L8-L14). [Original evidence](../../../evidence/sources/sha256/b5a5cd9e6118b1cf502751949cd4843098a463d0cfffac3a6281fa58dc7a2f53.md#L18-L20).

## Connections

Related canonical IDs: `KT-settlement-multi-exception-control`, `INT-KT-ratan-reference-and-control-interfaces`.

## Evidence limits

This candidate establishes no inspected implementation, execution, rollout, publication, or business acceptance.
Unselected content and linked attachments were not used to fill missing rules.

## Open questions

Owner: unknown. Answers remain pending in the single [central question register](../../../../tasks/workbench-knowledge-raw-import-20261113/evidence/canonical-draft-questions-20261115.md).
