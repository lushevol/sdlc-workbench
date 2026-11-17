Subject updated to BPMS APP and Interface APP, For example, "RATAN and TDS3"..

Below form to clarify when this article are updated and if it has been reviewed for reference, Status updated to Published after reviewed.

| Updated by | Update Date | Reviewed by | Review Date | Status |
| --- | --- | --- | --- | --- |
| @Chongxuan Li @Yunzhe Ta | 2026-07-29 | | | |

### Description:

Describe the background and purpose of the flow.

> **INFO**
> Considering Aspire can't catchup Korea release timeline, in order to do recon in TLM,  TLM would like to query accounting information(Including all accounting already sent to OLTP, including which acked & nacked & no_responsed) from RATAN via API.
>
>
>
> **Business Agreement:**
>
> Parameters needed when query RATAN API.
>
> Only support Korea entity(10036645) in parameter 'fmidList'.
>
> Implicit Conditions: **ratan_accounting_request_task_history.task_status**** = 'SENT'**** **
>
> **The longest time span is 3 days**

### E2E Data Flow:

Describe the end to end  flow.

> You may want to use a panel to highlight different Flow details for different purpose
> 1. TLM <> RESTFUL API <> RATANONE

### Connection details:

### Interface Specification:

PROD URL: [https://fmo-mfe.gdc.standardchartered.com:8453/api/ratan/](https://fmo-mfe.gdc.standardchartered.com:8453/api/ratan/)[v1/accounting/queryReconRecords?fmidList=10036645&startReleaseTime=2026-03-30T00:00:00&endReleaseTime=2026-04-01T00:00:00](https://uklvadapp1344.uk.dev.net:8453/api/ratan/v1/accounting/queryReconRecords?fmidList=10036645&startReleaseTime=2026-05-28T09:00:00&endReleaseTime=2026-05-29T09:00:00)

| parameters | type | M/O | sample | comment |
| --- | --- | --- | --- | --- |
| fmidList | String | M | 10036645,[10075222](http://localhost:8080/v1/accounting/queryReconRecords/?fmidList=10075222&fmidList=10075223&startReleaseTime=2026-04-04T00:00:00&endReleaseTime=2026-04-05T00:00:00) but only support 10036645 currently | ratan_accounting_request_task_history. booking_entity_fmid in fmidList |
| startReleaseTime | DateTime(yyyy-mm-dd'T'HH24:MM:SS) need covert to GMT | M | 2026-04-30T00:00:00 | ratan_accounting_request_task_history. created_at >= startReleaseTime |
| endReleaseTime | DateTime(yyyy-mm-dd'T'HH24:MM:SS) need covert to GMT | M | 2026-05-01T00:00:00 | ratan_accounting_request_task_history. created_at < endReleaseTime |

PT result:

response total accounting feeds: 20286

Sent time scope: 22-July-2026T00:00:00 to 25-July-2026T00:00:00

[Apache JMeter Dashboard](https://uklvadrtn006a.pi.dev.net:8081/performance-test/1785131956910/report/index.html)

Related articles appear here based on the labels you select. Click to edit the macro and add or change labels.

### Interface team contact:

### OLA:

Application self OLA consolidate link can add here

### Other Useful Docs:

Related articles appear here based on the labels you select. Click to edit the macro and add or change labels.

### Known Issues:

Related articles appear here based on the labels you select. Click to edit the macro and add or change labels.

### Troubleshooting Steps:

Describe whom and where to check if any interface related issue. Click to edit the macro and add or change labels.