Subject updated to BPMS APP and Interface APP, For example, "RATAN and TDS3"..

Below form to clarify when this article are updated and if it has been reviewed for reference, Status updated to Published after reviewed.

| Updated by | Update Date | Reviewed by | Review Date | Status |
| --- | --- | --- | --- | --- |
| @Yunzhe Ta @Zhenzhen Liu @Junying Jiang | 2026-09-02 | @Yunzhe Ta @Pengpeng Li | 2026-01-28 | |

### Description:

Murex KR sends MT & MxML messages to RATAN via MQ, where they are converted to MX format and then transmitted to ENISIS via SFTP.

Murex KR sends trade confirmation status messages to RATAN via MQ, where RATAN will consume and process for payment STP.

### E2E Data Flow:

`[MX KR]
│
▼
MT SWIFT Messages & Payment XML Files & Trade confirmation status (COMP)
│
▼
Via MQ → [Ratan]
│
▼
Ratan converts messages from MT to MX (ISO 20022) format / RATAN will consume and process COMP status for payment STP
   │
▼
Via SFTP → [ENISIS]

`
### Connection details:

### Interface Specification:

### Interface team contact:

| Murex Korea lead | [JaeHyeon.Oh@sc.com](mailto:JaeHyeon.Oh@sc.com) |
| --- | --- |
| KR Murex | [SCBK.FM_Support@sc.com](mailto:SCBK.FM_Support@sc.com) |

### OLA:

BPMS OLA location, no change required

[RATAN - OLA - FM Settlement - IS - Confluence](https://confluence.global.standardchartered.com/display/PSS/RATAN+-+OLA)

### Other Useful Docs:

Related articles appear here based on the labels you select. Click to edit the macro and add or change labels.

### Known Issues:

Related articles appear here based on the labels you select. Click to edit the macro and add or change labels.

### Troubleshooting Steps:

Related kafka  topic:

KR_MXG_SWF_ACK
KR_MXG_SWF_IN
Swift_MX_ENISIS_Out
KR_MXG_SWF_IN_Internal

| Murex(Korea) -> MQ(MT & MxML)->RATAN->SFTP( MX)->ENISIS | Murex send out the MT & MxML but RATAN didn't receive | 1. Murex would send exception email to Korea FMO 2. Korea FMO check with PSS/dev team what's the actual issue, if there's tech issue which the payment can't be resumed by system manually draft the MX message in ENISIS or draft the payment in OSCAR |
| --- | --- | --- |
| RATAN Swift exception due to invalid Murex data | 1. RATAN won't return ACK to Murex, Murex would send exception email to Korea FMO 2. Korea FMO check with PSS/dev team what's the actual issue, if there's tech issue which the payment can't be resumed by system manually draft the MX message in ENISIS or draft the payment in OSCAR |
| RATAN Swift generation exception | 1. Korea FMO monitor the exceptions from RATAN MX exception blotter 2. Korea FMO check with PSS/dev team what's the actual reason of the exception 1. If the exception is caused by static data setup or service temporally not available, Korea FMO can manually replay the message after static data corrected or service resumed, Korea FMO would replay from the MX exception blotter to retrigger the MT to MX conversion 2. if there's tech issue which the payment can't be resolved by replay manually draft the MX message in ENISIS or draft the payment in OSCAR |
| Message sent by RATAN but not received by ENISIS(SFTP) | 1. Murex extract the payment report & sent to SSDR, Korea FMO download the report from SSDR 2. Korea FMO manually extract the MX message from ENISIS by source system 3. Korea FMO ops manually compare the Murex payment report with ENISIS extraction and identify the discrepancy. In case there's missing or failure payment in ENISIS Korea FMO manually draft the MX message in ENISIS or draft the payment in OSCAR |

Confirmation message missing case

When cashflow failed or suppressed as 'Pending Affirmation' exception does not be processed by system, could use below sql to check if received related COMP message.

If result is null, indicates no COMP message received by RATAN.

select trade_id,trade_state from ratan_cashflow_group_management_service.ratan_trade where trade_id ='*trade id*' and trade_state='COMP'.