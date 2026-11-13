# Business Processing Flow

Cashflows from Murex: Can be seen as only event NEW exists, all the other events will be treated as incremental cashflows.

Cashflow from STELLA

| Transaction Action | Cashflow 1 Original Status | Cashflow 1 Event | Cashflow 1 Status | Cashflow 2 Event | Cashflow 2 Status |
| --- | --- | --- | --- | --- | --- |
| Book trade | PROJECTED | NEW | PROJECTED | NA |
| QUEUED | QUEUED |
| Undo/Cancel trade | PROJECTED | WITHDRAWAL | PROJECTED |
| QUEUED | QUEUED |
| PENDING | PENDING |
| VALIDATED | VALIDATED |
| RELEASED | WITHDRAWAL + CANCELLED | CANCELLED |
| SETTLED | CANCELLED |
| NOSTRO MATCHED | CANCELLED |
| Update trade | PROJECTED | AMEND | QUEUED |
| QUEUED | QUEUED |
| PENDING | QUEUED |
| VALIDATED | QUEUED |
| RELEASED | WITHDRAWAL | CANCELLED | NEW | PROJECTED |
| SETTLED | CANCELLED |
| NOSTRO MATCHED | CANCELLED | QUEUED |

# Use Cases

## Transaction Booking

| | Cashflow ID | Status | Sub-Status | Cashflow Version | Technical Version | Trigger point |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | C01 | PROJECTED | NA | 0 | 0 | Flow from STELLA or Murex or Razor |
| 2 | C01 | QUEUED | NA | 1 | 1 | On VD-5, 1. Receive QUEUED cashflow from STELLA 2. Move Murex cashflows from PROJECTED to QUEUED |
| 3 | C01 | PENDING | NA | 2 | 2 | Intermediate status when sub status is "NA" |
| 4 | C01 | VALIDATED | NA | 3 | 3 | Auto validation passed |
| 5 | C01 | RELEASED | NA | 4 | 4 | SWIFT message published to AMH |
| 6 | C01 | SETTLED | NA | 5 | 5 | AMH ACKED |
| 7 | C01 | NOSTRO MATCHED | NA | 6 | 6 | |

## NSTP Release Case

| Cashflow ID | Status | Sub-Status | Cashflow Version | Technical Version | Trigger point |
| --- | --- | --- | --- | --- | --- |
| C01 | PROJECTED | NA | 0 | 0 | Flow from STELLA or Murex or Razor |
| C01 | QUEUED | NA | 1 | 1 | On VD-5, 1. Receive QUEUED cashflow from STELLA 2. Move Murex cashflows from PROJECTED to QUEUED |
| C01 | PENDING | Pending_Validation_Maker | 2 | 2 | **Hit the NSTP rule, waiting for Manual verification** |
| C01 | PENDING | Pending_Validation_Checker | 2 | 3 | **Maker released the cashflow** |
| C01 | VALIDATED | NA | 3 | 4 | **Checker confirmed the releasing** |
| C01 | RELEASED | NA | 4 | 5 | SWIFT message published to AMH |
| C01 | SETTLED | NA | 5 | 6 | AMH ACKED |
| C01 | NOSTRO MATCHED | NA | 6 | 7 | |

## CPN Case

| | Cashflow ID | Source | Status | Netting Id | Sub-Status | Cashflow Version | Technical Version | Trigger point |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | C01 | STELLA | PROJECTED | | NA | 0 | 0 | Flow from STELLA or Murex or Razor |
| 2 | C01 | STELLA | QUEUED | | NA | 1 | 1 | On VD-5, Receive QUEUED cashflow from STELLA |
| 3 | C01 | STELLA | PENDING | | Pending_Netting_Maker | 2 | 2 | CPN eligible, hold the cashflow for manual netting |
| 4 | C02 | MUREX | PROJECTED | | NA | 0 | 0 | Flow from STELLA or Murex or Razor |
| 5 | C02 | MUREX | QUEUED | | NA | 1 | 1 | On VD-5, Move Murex cashflows from PROJECTED to QUEUED |
| 6 | C02 | MUREX | PENDING | | Pending_Netting_Maker | 2 | 2 | CPN eligible, hold the cashflow for manual netting |
| 7 | C01 | STELLA | NETTED | Net001 | NA | 3 | 3 | **Maker netted the cashflow C01 and C02** 1. **NETTED cashflow will be received from STELLA for C01** 2. **CS Platform need to move C02 to NETTED status** 3. **CS Platform generates C03 as netted cashflow** |
| 8 | C02 | MUREX | NETTED | Net001 | NA | 3 | 3 |
| 9 | C03 | CPN | QUEUED | Net001 | NA | 0 | 0 |
| 10 | C03 | CPN | PENDING | Net001 | Pending_Netting_Checker | 1 | 1 | Hold the netted cashflow for verification |
| 11 | C03 | CPN | VALIDATED | Net001 | NA | 2 | 2 | Continue the rest of the status update |

## Suppression Case

Doable for status:  [lyn question: doable for netting rresultant flow?]

1. PROJECTED
2. QUEUED
3. PENDING
4. VALIDATED

| | Cashflow ID | Status | Sub-Status | Cashflow Version | Technical Version | Trigger point |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | C01 | PROJECTED | NA | 0 | 0 | Flow from STELLA or Murex or Razor |
| 2 | C01 | QUEUED | NA | 1 | 1 | On VD-5, 1. Receive QUEUED cashflow from STELLA 2. Move Murex cashflows from PROJECTED to QUEUED |
| 3 | C01 | PENDING | NA | 2 | 2 | Intermediate status when sub status is "NA" |
| 4 | C01 | VALIDATED | NA | 3 | 3 | Auto validation passed |
| 5 | C01 | PENDING | Pending_Suppression_Checker | 4 | 4 | Maker manually suppress the cashflow |
| 6 | C01 | SUPPRESSED | NA | 5 | 5 | Checker confirmed the suppression |

## Transaction Amend/Undo on PROJECTED/QUEUED/PENDING/VALIDATED

| | Cashflow ID | Event | Status | Sub-Status | Cashflow Version | Technical Version | Trigger point |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | C01 | NEW | PROJECTED | NA | 0 | 0 | Flow from STELLA or Murex or Razor |
| 2 | C01 | NEW | QUEUED | NA | 1 | 1 | On VD-5, 1. Receive QUEUED cashflow from STELLA 2. Move Murex cashflows from PROJECTED to QUEUED |
| 3 | C01 | NEW | PENDING | NA | 2 | 2 | Intermediate status when sub status is "NA" |
| 4 | C01 | NEW | VALIDATED | NA | 3 | 3 | Auto validation passed |
| 5 | C01 | AMEND | PENDING | NA | 4 | 4 | **Transaction Update by FO from Blade, a withdraw will be consumed** |
| 6 | C01 | AMEND | VALIDATED | NA | 5 | 5 | |

| | Cashflow ID | Event | Status | Sub-Status | Cashflow Version | Technical Version | Trigger point |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | C01 | NEW | PROJECTED | NA | 0 | 0 | Flow from STELLA or Murex or Razor |
| 2 | C01 | NEW | QUEUED | NA | 1 | 1 | On VD-5, 1. Receive QUEUED cashflow from STELLA 2. Move Murex cashflows from PROJECTED to QUEUED |
| 3 | C01 | NEW | PENDING | NA | 2 | 2 | Intermediate status when sub status is "NA" |
| 4 | C01 | NEW | VALIDATED | NA | 3 | 3 | Auto validation passed |
| 5 | C01 | WITHDRAWAL | DEAD | NA | 4 | 4 | **Transaction Undo by FO from Blade, a withdraw will be consumed** |
| 6 | C01 | WITHDRAWAL | VALIDATED | NA | 5 | 5 | |

## Transaction Amend on RELEASED/SETTLED/NOSTRO MATCHED

Cashflow withdraw & new will only be consumed from STELLA, which means FO/MO amend a transaction to cancel the cashflow and generate a new cashflow.

Open questions:

1. When SWIFT already released, which one preferred from settlement ops: 1. Reversal SWIFT to be released 2. Cancellation

| | Cashflow ID | Event | Status | Sub-Status | Cashflow Version | Technical Version | Trigger point |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | C01 | NEW | PROJECTED | NA | 0 | 0 | Flow from STELLA or Murex or Razor |
| 2 | C01 | NEW | QUEUED | NA | 1 | 1 | On VD-5, 1. Receive QUEUED cashflow from STELLA 2. Move Murex cashflows from PROJECTED to QUEUED |
| 3 | C01 | NEW | PENDING | NA | 2 | 2 | Intermediate status when sub status is "NA" |
| 4 | C01 | NEW | VALIDATED | NA | 3 | 3 | Auto validation passed |
| 5 | C01 | NEW | RELEASED | NA | 4 | 4 | |
| 6 | C01 | WITHDRAWAL | CANCELLED | NA | 4 | 4 | **Transaction Amend by MO from Blade, a withdraw&new will be consumed** |
| 7 | C02 | NEW | QUEUED | NA | 0 | 0 |
| 8 | C02 | NEW | PENDING | Pending_Linked_Withdrawal_Done | 1 | 1 | Hold until the withdrawal done |
| 9 | C02 | NEW | VALIDATED | NA | 2 | 2 | **Auto validation passed** **Withdrawal done** |
| 10 | C02 | NEW | RELEASED | NA | 3 | 3 | SWIFT message published to AMH |
| 11 | C02 | NEW | SETTLED | NA | 4 | 4 | AMH ACKED |
| 12 | C02 | NEW | NOSTRO MATCHED | NA | 5 | 5 | |