Subject updated to BPMS APP and Interface APP, For example, "RATAN and TDS3"..

Below form to clarify when this article are updated and if it has been reviewed for reference, Status updated to Published after reviewed.

| Updated by | Update Date | Reviewed by | Review Date | Status |
| --- | --- | --- | --- | --- |
| @Yunzhe Ta @Zhenzhen Liu | 2026-01-28 | @Yunzhe Ta @Daiqi Wang | 2026-01-28 | |

### Description:

Murex KR sends MxML messages to RATAN via MQ, then generate MT in RATAN, AND converted to MX format except MT210 and then transmitted to ENISIS via FM solace.

### E2E Data Flow:

1. **Murex KR** generates MxML messages and sends to **RATAN** via **MQ**.
2. **RATAN** receives the message, generates MT, then converts it from **MT (SWIFT MT)** format to **MX (ISO 20022 XML)** format except MT210.
3. The converted MX message and MT210 is then securely transmitted to **ENISIS** via FM solace.
4. **ENISIS** acts as the gateway to process these messages and forward them to the **SWIFT network.**

![image-2026-7-22_21-33-23.png](attachments/image-2026-7-22_21-33-23.png)

### Connection details:

**Korea onboard：**

| **Source ** | **Target** | ** Data type ** | **Data format** | **Environment** | **Host/IP address** | **Sender Topic** | **Receiver Queue** | **Max Bind Count** | **Max-spool-usage (MB)** | **Reject-msg-to-sender-on-discard** | **Expected number of messages – Average / day** | **Expected number of messages – Peak / day** | **Largest Message Size** | **Average Message Size** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 51358-RATAN | 50157-ENISIS | MX-Swift | SCBML | PROD | | v1/settlement/51358-ratanone/ratanone/-/scbml-4.0/swift/mx/pub | | 6 | 300 | Y | 100 | 2000 | 15K | 10K |
| 50157-ENISIS | 51358-RATAN | MX-ACK/NACK | SCBML | PROD | | v1/settlement/50157-enisis/enisis/-/scbml-4.0/swift/mx/pub/ack | q-51358-ratanone-enisis-mx-status-ack | 6 | 300 | Y | 100 | 2000 | 15K | 5K |
| 51358-RATAN | 50157-ENISIS | MT-Swift | JSON | PROD | | v1/settlement/51358-ratanone/ratanone/-/scbml-4.0/swift/mt/pub | | 6 | 300 | Y | 100 | 2000 | 15K | 10K |
| 50157-ENISIS | 51358-RATAN | MT-ACK/NACK | JSON | PROD | | v1/settlement/50157-enisis/enisis/-/scbml-4.0/swift/mt/pub/ack | q-51358-ratanone-enisis-mt-status-ack | 6 | 300 | Y | 100 | 2000 | 15K | 5K |
| | | | | | | | | | | | | | | |

### Interface Specification:

Related articles appear here based on the labels you select. Click to edit the macro and add or change labels.

### Interface team contact:

| App Name | PSS Contact | PSS Manager |
| --- | --- | --- |
| ENISIS | ENISIS - SCBK.FX_Support <SCBK.FX_Support@[sc.com](http://sc.com/)> | 박정현(Park, Jung Hyeon) <[JungHyeon.Park@sc.com](mailto:JungHyeon.Park@sc.com)> |

### OLA:

BPMS OLA location, no change required

[RATAN - OLA - FM Settlement - IS - Confluence](https://confluence.global.standardchartered.com/display/PSS/RATAN+-+OLA)

📎 [FM ESB Aide Common_9.22.docx](attachments/FM ESB Aide Common_9.22.docx)

### Other Useful Docs:

Related articles appear here based on the labels you select. Click to edit the macro and add or change labels.

### Known Issues:

Related articles appear here based on the labels you select. Click to edit the macro and add or change labels.

### Troubleshooting Steps:

| Murex(Korea) -> MQ(MxML)->RATAN→FM solace( MX&MT)->ENISIS | Murex send out the MxML but RATAN didn't receive | 1. Murex would send exception email to Korea FMO 2. Korea FMO check with PSS/dev team what's the actual issue, if there's tech issue which the payment can't be resumed by system manually draft the MX message in ENISIS or draft the payment in OSCAR |
| --- | --- | --- |
| RATAN Swift exception due to invalid Murex data | 1. RATAN won't return ACK to Murex, Murex would send exception email to Korea FMO 2. Korea FMO check with PSS/dev team what's the actual issue, if there's tech issue which the payment can't be resumed by system manually draft the MX message in ENISIS or draft the payment in OSCAR |
| RATAN Swift generation exception | 1. Korea FMO monitor the exceptions from RATAN MX exception blotter 2. Korea FMO check with PSS/dev team what's the actual reason of the exception 1. If the exception is caused by static data setup or service temporally not available, Korea FMO can manually replay the message after static data corrected or service resumed, Korea FMO would replay from the MX exception blotter to retrigger the MT to MX conversion 2. if there's tech issue which the payment can't be resolved by replay manually draft the MX message in ENISIS or draft the payment in OSCAR |
| Message sent by RATAN but not received ACK from ENISIS | 1. Korea FMO monitor dashboard for SWIFT error. 2. SSDR generate report to Korea FMO ops. 3. Korea FMO manually extract the MX message from ENISIS by source system. 4. Korea FMO ops manually compare the payment report with ENISIS extraction and identify the discrepancy. In case there's missing or failure payment in ENISIS Korea FMO manually draft the MX message in ENISIS or draft the payment in OSCAR |

## MX Exception Scenario

| 1 | Exception between Murex2.11 and RATAN | - Murex would send notification email to Korea FMO. - Korea FMO would manually draft the payment in Oscar or MX in ENISIS. |
| --- | --- | --- |
| 2 | Exception within RATAN | - New MX exception blotter would be built as per Korea FMO requirement, Korea FMO would take the responsibility to monitor the exceptions as their normal BAU. - There would be replay function in the MX exception blotter for Korea FMO to manually reprocess the underlying payment. - For exceptions which can’t be resolved by replay, Korea FMO would manually draft the payment in Oscar or MX in ENISIS. |
| 3 | Message missing or failure in ENISIS | - Korea FMO would manually do the recon between SSDR payment reports & ENISIS swift messages to identify if any payment missing/failure in ENISIS. - For exceptions which can’t be resolved by tech, Korea FMO would manually draft the payment in Oscar or MX in ENISIS. |