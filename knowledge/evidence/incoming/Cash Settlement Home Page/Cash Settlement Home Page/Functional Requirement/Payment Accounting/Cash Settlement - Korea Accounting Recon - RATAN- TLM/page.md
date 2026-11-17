# Background

Considering Aspire can't catchup Korea release timeline, in order to do recon in TLM,  TLM would like to query accounting information(Including all accounting already sent to OLTP, including which acked & nacked & no_responsed) from RATAN via API.

[Cash Settlements Migration -Korea- Scope & Plan - FM re-platforming - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3588497557#CashSettlementsMigrationKoreaScope&Plan-Objective:)

In the future,

TLM ADO : [Feature 11898201 TLM-KR-Onboard the recon from OLTP>ASPIRE>TLM (Decomm from RATAN to TLM)](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/11898201)

# Business Agreement:

Parameters needed when query RATAN API.

Only support Korea entity(10036645) in parameter 'fmidList'.

Implicit Conditions: **ratan_accounting_request_task_history.task_status = 'SENT' **

**The longest time span is 3 days**

**Request Sample **: curl -X GET "[http://localhost:8080/v1/accounting/queryReconRecords/?fmidList=*10036645*&startReleaseTime=*2026-04-02T00:00:00*&endReleaseTime=*2026-04-05T00:00:00*](http://localhost:8080/v1/accounting/queryReconRecords/?fmidList=10075222&fmidList=10075223&startReleaseTime=2026-04-04T00:00:00&endReleaseTime=2026-04-05T00:00:00)"

| startReleaseTime | DateTime(yyyy-mm-dd HH24:MM:SS) need covert to GMT | M | ratan_accounting_request_task_history. created_at > startReleaseTime |
| --- | --- | --- | --- |
| fmidList | List<String> | M | ratan_accounting_request_task_history. booking_entity_fmid in fmidList |
| endReleaseTime | DateTime(yyyy-mm-dd HH24:MM:SS) need covert to GMT | M | ratan_accounting_request_task_history. created_at <= endReleaseTime |

# Accounting Status Introduction

Accounting status in 'SUCCESS', 'SENT' and 'REJECTED' will respond to TLM.

| **Accounting Status** | **Generation logic** | **Comment** |
| --- | --- | --- |
| HOLD | When cashflow not reach value date, status of accounting will in 'HOLD' | Accounting entry generated but not reaching VD yet, so holding the posting |
| MISSING_INFO | When cashflow not reach value date, and can't get mandatory fields filled | It's for the SWIFT_SUPPRESSED case when the Nostro is not available, Ratan won't generate the accounting entry Or if any mandatory field value is missing. |
| DISABLED | Accounting generated but no need to send out | Accounting entry generated and won't sent to OLTP. For settlement account="UIDD/UISUS" &settlement means='NOX' |
| SUCCESS | Accounting entry generated and sent to OLTP, and get 'SUCCESS' respond | Accounting entry generated and sent to OLTP, and get 'SUCCESS' respond |
| SENT | Accounting entry generated and sent to OLTP, and have not got any respond | Accounting entry generated and sent to OLTP, and have not got any respond |
| REJECTED | Accounting entry generated and sent to OLTP, and get 'REJECTED' respond | Accounting entry generated and sent to OLTP, and get 'REJECTED' respond |

# Response file Sample

{
  "totalNumberOfRecords": 1,
  "accountingRecords": [
    {
      "publishTimestamp": "2024-06-01 12:00:00", //Timestamp when post response messages
      "message": {
       "data": {
         "id": "**Field_Message_ID**",     //Refer to logic as below
         "type": "post-transactions",   //hardcode
         "attributes": {
          "request": {
            "source-system": "RATAN",
            "posting-type": "FundsTransfer",  //hardcode
            "transaction-type": "RTN",        //hardcode
            "posting-branch": "**Field_Posting_Branch**",   //Refer to logic as below
            "external-system-key": "Cashflow.Cashflow_Id.Cashflow.Cashflow_Business_Versio.Cashflow.Cashflow_Minor_Version",  //Refer to logic as below
            "transaction-currency": "**Field_Transaction_Currency**",  //Refer to logic as below
            "transaction-amount": "**Field_Transaction_Amount**",      //Refer to logic as below
            "transaction entry": [
             {
               "narratives": {
                "narration1": "DV||Branch_code||CashflowID",
                "narration2": "Party2.SCI.Entity.FM_CODE",
                "narration3": "Payment.Instrument_Common.ISDA_Taxonomy",
                "narration4": "Trade_Id Source_System_Trade_Internal_Id",
                "narration5": "Blank for non utilization",
                "narration6": "Cashflow.Cashflow_State Data_Flow.Data_Source_System"
               },
               "extended-narratives": {
                "extended-narration1": "Instrument_Common.Murex_Product_Strategy#Cashflow.Payment_Type#Cashflow.Netting_Id",
                "extended-narration2": "Cashflow.splitParentId#Party1.Entity.Booking_Entity_SCI_FMID Party1.SCI.Entity.FM_CODE",
                "extended-narration3": "Blank for non utilization",
                "extended-narration4": "Party2.Entity.Counterparty_SCI_FMID",
                "extended-narration5": "Party2.SCI.Entity.Counterparty_Long_Name",
                "extended-narration6": "Portfolio.Booking_Entity_Trade_Portfolio_Name"
               },
               "value-date": "**Field_Value_Date**",              //Refer to logic as below
               "account-number": "**Field_eBBS_Nostro_Account**", //Refer to logic as below
               "allow-insufficient-funds": "Y",
               "casa-currency-code": "USD",
               "transaction-code": "**Field_Transaction_code**",  //Refer to logic as below
               "transaction-nature": "**Field_eBBS_Nostro_DebitCredit**"  //Refer to logic as below
             },
             {
               "narratives": {
                "narration1": "DV||Branch_code||CashflowID",
                "narration2": "Party2.SCI.Entity.FM_CODE",
                "narration3": "Payment.Instrument_Common.ISDA_Taxonomy",
                "narration4": "Trade_Id Source_System_Trade_Internal_Id",
                "narration5": "Blank for non utilization",
                "narration6": "Cashflow.Cashflow_State Data_Flow.Data_Source_System"
               },
               "extended-narratives": {
                "extended-narration1": "Instrument_Common.Murex_Product_Strategy#Cashflow.Payment_Type#Cashflow.Netting_Id",
                "extended-narration2": "Cashflow.splitParentId#Party1.Entity.Booking_Entity_SCI_FMID Party1.SCI.Entity.FM_CODE",
                "extended-narration3": "Blank for non utilization",
                "extended-narration4": "Party2.Entity.Counterparty_SCI_FMID",
                "extended-narration5": "Party2.SCI.Entity.Counterparty_Long_Name",
                "extended-narration6": "Portfolio.Booking_Entity_Trade_Portfolio_Name"
               },
               "value-date": "**Field_Value_Date**",                     //Refer to logic as below
               "account-number": "**Field_eBBS_Nostro_Account**",        //Refer to logic as below
               "allow-insufficient-funds": "Y",
               "casa-currency-code": "USD",
               "transaction-code": "**Field_Transaction_code**",          //Refer to logic as below
               "transaction-nature": "**Field_eBBS_Nostro_DebitCredit**"  //Refer to logic as below
             }
            ]
          }
         }
       }
      }
    }
  ]
}

Fields logic

- **Field_Message_ID**: UUID with max length as 50
- **Field_Posting_Branch: **Need to map according to entity FMID (static data to be maintained in RATAN)
- **Field_External_System_Key (Mandatory): **Cashflow.Cashflow_Id + "." + Cashflow.Cashflow_Business_Version + "." + Cashflow.Cashflow_Minor_Version - New cashflow C1: Ratan send new entry to eBBS with external id as 'C1.1.1', - Cashflow C1 withdrawal: Ratan send reversal entry to eBBS with external id as 'C1.2.1'
- **Field_Transaction_Currency (Mandatory): ** - Get the cashflow currency Cashflow.Payment_Currency - Query the ISO currency from static data and return **(Speical logica for SG CNH)**.
- **Field_Transaction_Amount: ** 1. Get the Cashflow.Payment_Amount from cashflow data 2. Rounding logic, same logic with SWIFT (Low priority)
- **Field_Value_Date (Mandatory): ** 1. Get Cashflow.Payment_Date from cashflow data 2. Verify the format is YYYY-MM-DD(2024-01-08)
- **Field_eBBS_Nostro_Account (Mandatory): **Get Settlement_Instruction.Account.EBBS_Account_Number and return
- **Field_eBBS_Nostro_DebitCredit (Mandatory):** 1. Get payer reference Cashflow.Payment_Payer_Party_Reference from cashflow 2. if Cashflow.Payment_Payer_Party_Reference == party1 and Cashflow.Cashflow_Event_Type==New then return 'C' else return 'D'
- **Field_eBBS_Bridge_Account (Mandatory)** 1. Get the entity FMID(Entity.Booking_Entity_SCI_FMID) from cashflow 2. Looup the ebbs bridge account number from the static data mapping 'eBBS bridge account mapping', return the ebbs bridge account number
- **Field_Transaction_code: **

According to posting branch and Debit/Credit, get the transaction code from Static table

- **Field_eBBS_Bridge_DebitCredit (Mandatory):** 1. Get payer reference Cashflow.Payment_Payer_Party_Reference from cashflow 2. if Cashflow.Payment_Payer_Party_Reference == party1 Cashflow.Cashflow_Event_Type==New then return 'D' else return 'C'

| Path | eBBS Field | Type | Length | RATAN Length | Mandatory | Ratan Logic | Comment |
| --- | --- | --- | --- | --- | --- | --- | --- |
| data/attributes/request/transaction entry/narratives | narration1**(Mandatory)** | VARCHAR | 35 | 32 | M | "DV" + Branch code +cashflow ID | SWIFT tag 20 |
| narration2 | VARCHAR | 50 | | M | Party2.SCI.Entity.FM_CODE | Counterparty FM CODE |
| narration3 | VARCHAR | 50 | text | M | Payment.Instrument_Common.ISDA_Taxonomy | Product Taxonomy |
| narration4 | VARCHAR | 35 | text | M | Trade_Id +" "+Source_System_Trade_Internal_Id | Trade_Id (Mandatory)+ " " +S2BX Trade Id |
| narration5 | VARCHAR | 35 | text | M | Transaction_Banking_Comments | TB Comments Field (from Trade) Contains Source system Payment Reference (From Trade) + Underlying client ID Blank for non utilization |
| narration6 | VARCHAR | 35 | text | M | Cashflow.Cashflow_State +" " +Data_Flow.Data_Source_System | Cashflow Status + “ ” + Data_Source_System |
| data/attributes/request/transaction entry/extended-narratives | EXTENDEDNARRATIVE1 | VARCHAR | 65 | text | M | - Instrument_Common.Murex_Product_Strategy#Cashflow.Payment_Type#Cashflow.Netting_Id | - Original requirement: Netting ID - New change requirement from Swap Agent initiative(ADO 5967599) from UK cashflow migration, detail requirement refer to [RFR and Swap Agent - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/RFR+and+Swap+Agent) |
| EXTENDEDNARRATIVE2 | VARCHAR | 65 | text | M | Cashflow.splitParentId#Party1.Entity.Booking_Entity_SCI_FMID+" "+Party1.SCI.Entity.FM_CODE | booking entity FMID+ Entity FM CODE |
| EXTENDEDNARRATIVE3 | VARCHAR | 65 | text | M | FXU.Payment Reference +“ ” +FXU.Area code +" " + FXU.Maker ID +" " FXU.Checker ID+ FXU.utilization status | Blank for non utilization & auto util & pastdue |
| EXTENDEDNARRATIVE4 | VARCHAR | 65 | text | M | Party2.Entity.Counterparty_SCI_FMID | CounterParty FMID Blank for non split |
| EXTENDEDNARRATIVE5 | VARCHAR | 65 | | M | Party2.SCI.Entity.Counterparty_Long_Name | Counterparty long name |
| EXTENDEDNARRATIVE6 | VARCHAR | 65 | text | M | Portfolio.Booking_Entity_Trade_Portfolio_Name | Biz Portfolio |

# Static Data

| Entity Name | FMID | Country Code | Branch code |
| --- | --- | --- | --- |
| SCFB_SEOUL | 10036645 | KR | 70 |

| M_ENTITY | FMID | Currency | Bridge Account |
| --- | --- | --- | --- |
| SCFB_SEOUL | 10036645 | KRW | 000287 |
| SCFB_SEOUL | 10036645 | FCY | 040446 |

More information refer to: [Static date summary - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Static+date+summary)

# Tech Design

[Korea Accounting - TLM Recon - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Korea+Accounting+-+TLM+Recon)