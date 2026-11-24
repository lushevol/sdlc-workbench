---
type: KnowledgeTopic
id: KT-settlement-korea-trade-confirmation
version: 1
owner: unknown
governance_state: candidate
status: draft
classification: settlement
scope: Korea Murex trade COMP as the affirmation input for RATAN payment STP.
summary: The Korea migration designs propose direct MXML COMP over IBM MQ for the payment confirmation gate.
sources:
- id: SRC-9fc5fb9a81c4d52639910652
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Korea Murex Trade COMP High Level Solution/page.md
  revision: sha256:c371fd73c51a1a422a60d5f1cd9bd0cd86a5c1176d121e9b1dc89170a02debeb
  sha256: c371fd73c51a1a422a60d5f1cd9bd0cd86a5c1176d121e9b1dc89170a02debeb
- id: SRC-5b777973297263c3929d8d6e
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Functional Requirement/2026 Changes/Cash Settlement
    -- Korea Migration/COMP status to drive STP process/page.md
  revision: sha256:a27ec94a124c1ad80e2235ed7b782db25f05967eaa6732bd63f2c6b7144d74d6
  sha256: a27ec94a124c1ad80e2235ed7b782db25f05967eaa6732bd63f2c6b7144d74d6
- id: SRC-e698e0c6ad4b767d2a454902
  resource: source:cash-settlement-home-page/Cash Settlement Home Page/Tech Design/Korea Murex Trade COMP Design/page.md
  revision: sha256:65cbb66e81eddc58797efd4ec8f28baa4c7798f9feca17852f8bceb26fce36bf
  sha256: 65cbb66e81eddc58797efd4ec8f28baa4c7798f9feca17852f8bceb26fce36bf
- id: SRC-ba86435ac90f289ab511ed78
  resource: source:ratan-51358/RATAN - 51358/RATAN -Interfaces/Ratan and Murex KR 50216/page.md
  revision: sha256:1d0f8b241659e360f31d955a218a358ab662c172686fee3092b3a09a3c974936
  sha256: 1d0f8b241659e360f31d955a218a358ab662c172686fee3092b3a09a3c974936
generated:
  by: agent:codex
  at: '2026-11-15T09:09:18.836152+00:00'
verified: []
related: []
open_questions:
- Which MXML contract, scope, and effective date does the Korea settlement owner approve?
- Which trade identifier and version bind a COMP event to the correct cashflow?
- How should RATAN handle out-of-order, duplicate, or late COMP after cancellation and reissue?
- Which acknowledgement, replay, or manual affirmation control applies when a COMP message is missing?
- What condition switches the tactical confirmation transport to the strategic path?
---
# Korea Murex COMP and settlement confirmation

## Scope

Korea Murex trade COMP as the affirmation input for RATAN payment straight-through processing (STP).

## Summary

The migration designs seek to replace manual affirmation caused by missing Korea trade COMP. The remaining tactical proposal uses MXML over IBM MQ.

## Documented knowledge

### Confirmation gate

The design states that trade confirmation is required for payment STP. It records a Korea Operations go-live dependency because of the expected manual volume. The functional proposal sends trade COMP directly from Korea Murex while TDS3 lacks that event. [Confirmation objective](../../../evidence/sources/sha256/c371fd73c51a1a422a60d5f1cd9bd0cd86a5c1176d121e9b1dc89170a02debeb.md#L1-L7) [Functional proposal](../../../evidence/sources/sha256/a27ec94a124c1ad80e2235ed7b782db25f05967eaa6732bd63f2c6b7144d74d6.md#L1)

For an unconfirmed original trade, the recorded cancel-and-reissue answer cancels the old cashflow. The new cashflow waits for its own COMP. [Cancel and reissue](../../../evidence/sources/sha256/a27ec94a124c1ad80e2235ed7b782db25f05967eaa6732bd63f2c6b7144d74d6.md#L25-L27)

### Transport options

The initial proposal reuses Murex GDC, Trade Lake, TDS3, and RATAN. The document records that Murex PSS rejected the option. The later direct SCBML proposal over IBM MQ was ruled out because Murex could not produce SCBML. [Trade Lake option](../../../evidence/sources/sha256/c371fd73c51a1a422a60d5f1cd9bd0cd86a5c1176d121e9b1dc89170a02debeb.md#L9-L24) [SCBML option](../../../evidence/sources/sha256/c371fd73c51a1a422a60d5f1cd9bd0cd86a5c1176d121e9b1dc89170a02debeb.md#L26-L42)

The remaining tactical proposal sends Murex Korea MXML to RATAN over IBM MQ. It adds custom COMP handling at RATAN and requires a removal plan when the strategic path is available. The strategy and switch criteria remain open. [Tactical option](../../../evidence/sources/sha256/c371fd73c51a1a422a60d5f1cd9bd0cd86a5c1176d121e9b1dc89170a02debeb.md#L44-L65)

### Mapping and retained message

The functional mapping sets SCBML sender to Murex. It copies MXML trade validation level COMP to SCBML substate and MXML action validation to SCBML transaction type. The detailed sketch proposes a table with a unique ID, trade ID, action, raw message, and timestamps. [Field mapping](../../../evidence/sources/sha256/a27ec94a124c1ad80e2235ed7b782db25f05967eaa6732bd63f2c6b7144d74d6.md#L13-L19) [Retained message design](../../../evidence/sources/sha256/65cbb66e81eddc58797efd4ec8f28baa4c7798f9feca17852f8bceb26fce36bf.md#L9-L18)

The interface catalog describes trade confirmation over MQ for payment STP. Its missing-confirmation procedure checks for a received COMP when Pending Affirmation fails or is suppressed. An empty result means the search found no COMP in RATAN. [Confirmation interface](../../../evidence/sources/sha256/1d0f8b241659e360f31d955a218a358ab662c172686fee3092b3a09a3c974936.md#L9-L13) [Missing confirmation diagnosis](../../../evidence/sources/sha256/1d0f8b241659e360f31d955a218a358ab662c172686fee3092b3a09a3c974936.md#L71-L75)

## Connections

The Korea interface catalog also covers MT and MxML payment-message conversion to MX for ENISIS. That payment transport and its exception handling have a separate scope. COMP supplies a trade confirmation gate in the proposed path. [Payment and confirmation boundaries](../../../evidence/sources/sha256/1d0f8b241659e360f31d955a218a358ab662c172686fee3092b3a09a3c974936.md#L9-L13)

## Evidence limits

The high-level solution labels the MXML route tactical and the detailed design in progress. The selected evidence leaves trade/version association and duplicate handling unresolved. The selected catalog excerpt describes the interface and recovery cases. It provides no executed result for this review.

## Open questions

- Which MXML contract, scope, and effective date does the Korea settlement owner approve?
- Which trade identifier and version bind a COMP event to the correct cashflow?
- How should RATAN handle out-of-order, duplicate, or late COMP after cancellation and reissue?
- Which acknowledgement, replay, or manual affirmation control applies when a COMP message is missing?
- What condition switches the tactical confirmation transport to the strategic path?
