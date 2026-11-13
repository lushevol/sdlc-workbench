Subject updated to BPMS APP and Interface APP, For example, "RATAN and TDS3"..

Below form to clarify when this article are updated and if it has been reviewed for reference, Status updated to Published after reviewed.

| Updated by | Update Date | Reviewed by | Review Date | Status |
| --- | --- | --- | --- | --- |
| @Chongxuan Li @Yunzhe Ta | 2026-07-29 | | | |

### Description:

Describe the background and purpose of the flow.

> **INFO**
> Ratan sends **Korea accounting feed**s to KREDMI and OLTP (On Line Transaction Posting) via FM Solace. 
> Instead of Murex-KR, RATAN will send real time accounting messages to OLTP. Cashflow scope is same with that flow into RATAN from Murex-KR.
>
> | **Accounting Status in RATAN** | **Account Status Reason** | **Comment** |
> | --- | --- | --- |
> | HOLD | | Accounting entry generated but not reaching VD yet, so holding the posting |
> | DISABLED | | Accounting entry generated for Sett Means = 'NOX' and Sett Account in ('CCY UISUS', 'CCY UIDD'), but not sent to OLTP. So disable it. |
> | SENT | | Accounting entry generated and sent to OLTP but didn't receive response from OLTP yet. |
> | SUCCESS | | OLTP consume the accounting entry successfully and return the ACK |
> | REJECTED | OLTP Error Code | OLTP can't consume the accounting entry and response with error code. |
> | MISSING_INFO | | It's for the SWIFT_SUPPRESSED case when the Nostro is not available, Ratan won't generate the accounting entry Or if any mandatory field value is missing. |

### E2E Data Flow:

Describe the end to end  flow.

> ![OLTP.png](attachments/OLTP.png)
>
>
>
> Normal flow:
>
> 1. Ratan generate Accounting json → FMSolace → KREDMI → OLTP
> 2. OLTP receive and validate Accounting json → KREDMI→ FMSolace → Ratan
>
> EOD flow (11:30 ~ 12:30 KST):
>
> 1. Ratan generate Accounting json → FMSolace → KREDMI
> 2. KREDMI Nack → FMSolace → Ratan

### Connection details:

### Interface Specification:

Related articles appear here based on the labels you select. Click to edit the macro and add or change labels.

### Interface team contact:

### OLA:

📎 [FM ESB Aide Common_9.22.docx](attachments/FM ESB Aide Common_9.22.docx)

### Other Useful Docs:

Related articles appear here based on the labels you select. Click to edit the macro and add or change labels.

### Known Issues:

Related articles appear here based on the labels you select. Click to edit the macro and add or change labels.

### Troubleshooting Steps:

Describe whom and where to check if any interface related issue. Click to edit the macro and add or change labels.