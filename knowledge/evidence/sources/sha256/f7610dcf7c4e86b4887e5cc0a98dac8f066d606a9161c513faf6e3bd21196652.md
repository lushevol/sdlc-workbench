# Function Flow

# User cases to decide if the cashflow need to re-stamping

| Case ID | SSI+ Event | Cashflow Status | Sub Status | Cashflow Exceptions | Eligible for SSI Refresh | Logic to identify the impacted cashflows |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | New/Amend/Re-active | WAITING | - Pending Operator | Missing Vostro | Y | Restamping if the SSI & cashflow have same values on below field - Counterpart - Currency - CFI Code: - Branch id( e.g. HK, SG or Global) If there's any exception from the restamping, the sub status will be 'Pending Operator' which need Maker's input again. |
| 2 | New/Amend/Re-active | WAITING | - Pending Verification | Missing Vostro | N |
| 3 | New/Amend/Re-active | WAITING | - Pending Operator | Multi Vostro | Y |
| 4 | New/Amend/Re-active | WAITING | - Pending Verification | Multi Vostro | N |
| 5 | New/Amend/Re-active | WAITING | - Pending Operator | Nostro vs Vostro Mismatch | Y |
| 6 | New/Amend/Re-active | WAITING | - Pending Verification | Nostro vs Vostro Mismatch | N |
| 7 | New/Amend/Re-active | WAITING | | Adhoc SI | N |
| 8 | New/Amend/Re-active | WAITING | - Pending Operator | Secondary Vostro | Y |
| 9 | New/Amend/Re-active | WAITING/READY | NA+NA | Good System Assigned Vostro | Y |
| 10 | Delete/De-active | WAITING | - Pending Operator | Multi Vostro | Y | If the deleted SSI is one of the Multi SSI, redo the SSI Stamping. |
| 11 | Delete/De-active | WAITING/READY | NA+NA | Good System Assigned Vostro | Y | If the deleted SSI is assigned to the cashflow, redo the SSI Stamping. |

# Logic to query the impacted cashflows

Base on the above table matrix we need additional query logic to narrow down the impacted cashflow scope.

**The logic for SSI 'New/Amend/Re-active' events:**

1. Counterpart FMID: To compare the FMID between the SSI message & cashflow. | Data Source | Logical Model Field | | --- | --- | | Cashflow | Entity.Counterparty_SCI_FMID | | SSI data | Settlement_Instruction.Counterparty_SCI_FMID |
2. Currency: To compare the currency between SSI message & cashflow | Data Source | Logical Model Field | | --- | --- | | Cashflow | Cashflow.Payment_Currency | | SSI data | Settlement_Instruction.Payment_Currency |
3. CFI Code: Take the CFI Code from SSI message and compare with the cashflow 1. Logical model path | Data Source | Logical Model Field | | --- | --- | | Cashflow | Instrument_Common.CFI_Code | | SSI data | Settlement_Instruction.CFI_Code | 2. CFI Code from SSI should be at higher or equal granular level than the CFI in cashflow Below are some sample | SSI CFI | Cashflow CFI | Good to pick up cashflow? | | --- | --- | --- | | *R**** | SRXXXX | Yes | | *F**** | JFXXXX | Yes | | ****** | SRXXXX | Yes | | SRF*** | SRXXXX | No |
4. Branch ID: Take the branch id from SSI message and compare with the cashflow 1. Logical Model path: | Data Source | Logical Model Field | | --- | --- | | Cashflow | Entity.Booking_Entity_SCI_FMCODE | | SSI data | Settlement_Instruction.BranchId_Murex3Id | 2. If the SSI is Branch specific then only look up the cashflows stamped to the specific branch, if the SSI is global then query both the cashflow stamped with 'Global' and specific branch SSI. | Branch from SSI Event | Branches from assigned SSI | | --- | --- | | SCB LONDON*LDN | SCB LONDON*LDN | | Global | All |

**The Logics for SSI 'Delete/De-active' events:**

1. Take the SSI ID from notification message. | Data Source | Logical Model Field | | --- | --- | | SSI data | Settlement_Instruction.SSI_Id |
2. Compare the SSI ID with the below cashflows. 1. Multi Vostro Exception: If the deleted SSI is one of the multi SSI cause the exception. 2. Good System assigned Vostro: If the deleted SSI is the one stamped to the cashflow.