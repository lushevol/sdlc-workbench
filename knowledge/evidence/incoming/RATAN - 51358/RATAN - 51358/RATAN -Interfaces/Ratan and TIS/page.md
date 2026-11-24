Subject updated to BPMS APP and Interface APP, For example, "RATAN and TDS3"..

Below form to clarify when this article are updated and if it has been reviewed for reference, Status updated to Published after reviewed.

| Updated by | Update Date | Reviewed by | Review Date | Status |
| --- | --- | --- | --- | --- |
| @Yinghua Song @Yunzhe Ta | 2026-07-29 | | | |

### Description:

Describe the background and purpose of the flow.

> **INFO**
> As some payment need to manually key-in everyday via OLTP(UI), user hope that those payment information could get automatically from API.
>
> Once cashflow is Released status in Ratan side, then SSI update is not supported.
>
> Withdrawal cashflow will not be available for TIS/OTLP query, cashflow status will be in Settled with Reversed/Reversal flag
>
> **TIS (Total Information System) Scope: **
>
> 1.'Released' or 'Settled' cashflow
>
> 2.STTL_MEANS = NOX
>
> 3.No reversal event
>
> 4.Entity FMID: 10036645
>
> ![image-2026-7-29_14-22-26-1.png](attachments/image-2026-7-29_14-22-26-1.png)

### E2E Data Flow:

Describe the end to end  flow.

> You may want to use a panel to highlight different Flow details for different purpose
> 1. TIS <> RESTFUL API <> RATANONE

### Connection details:

### Interface Specification:

Related articles appear here based on the labels you select. Click to edit the macro and add or change labels.

### Interface team contact:

### OLA:

📎 [OLA_RATAN_API_TIS_v1.0.docx](attachments/OLA_RATAN_API_TIS_v1.0.docx)

### Other Useful Docs:

Related articles appear here based on the labels you select. Click to edit the macro and add or change labels.

### Known Issues:

Related articles appear here based on the labels you select. Click to edit the macro and add or change labels.

### Troubleshooting Steps:

Describe whom and where to check if any interface related issue. Click to edit the macro and add or change labels.