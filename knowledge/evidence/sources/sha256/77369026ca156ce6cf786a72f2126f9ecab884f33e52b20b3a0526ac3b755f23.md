# Business Requirement

[https://confluence.global.standardchartered.com/display/DSP/Cash+Settlement+-+Korea+TLM+Accounting](https://confluence.global.standardchartered.com/display/DSP/Cash+Settlement+-+Korea+TLM+Accounting)

# Restful API design

UAT4:

curl --location --request GET '[https://uklvadapp1344.uk.dev.net:8453/api/ratan/v1/accounting/queryReconRecords?fmidList=10036645&startReleaseTime=2026-05-28T09:00:00&endReleaseTime=2026-05-29T09:00:00](https://uklvadapp1344.uk.dev.net:8453/api/ratan/v1/accounting/queryReconRecords?fmidList=10036645&startReleaseTime=2026-05-28T09:00:00&endReleaseTime=2026-05-29T09:00:00)' --header 'Accept-Encoding: gzip' --compressed

As this API could return over 10MB size JSON, pls add **--header 'Accept-Encoding: gzip'** in request header.

And this API also need 3 header attributes,

***--header 'FMAA-Token: ${token from FMAA}' ***

***--header 'FMAA-userId: ${userId from FMAA}'***

***--header ‘FMAA-appId: ${appId from FMAA}’***

***Above these info both are generated in FMAA. So clients need register in FMAA first.***

PROD:

url : https://fmo-mfe.gdc.standardchartered.com:8453/api/ratan/[v1/accounting/queryReconRecords?fmidList=10036645&startReleaseTime=2026-03-30T00:00:00&endReleaseTime=2026-04-01T00:00:00](https://uklvadapp1344.uk.dev.net:8453/api/ratan/v1/accounting/queryReconRecords?fmidList=10036645&startReleaseTime=2026-05-28T09:00:00&endReleaseTime=2026-05-29T09:00:00)

## Fetch accounting feed for EBBS

### Data scope

1. OLTP accounting tasks for Korea.
2. Max time scope is 72 hours . So need to check it in case too many records response. e.g. ratan_accounting_request_task_history. created_at >= '2026-04-15 21:00:00' and ratan_accounting_request_task_history. created_at < '2026-04-18 21:00:00'.

### Scenarios

| No | cashflow | fmid | payment date | system date | action | action date | publish time | publish method |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | cf1 | 401036553 | 2025-04-15 | 2025-04-15 | release | 2025-04-14 | 2025-04-15 06:00:00 | sod job |
| 2 | cf2 | 401036553 | 2025-04-15 | 2025-04-15 | release | 2025-04-15 | 2025-04-15 10:30:52 | real time |
| 3 | cf3 | 401036553 | 2025-04-15 | 2025-04-16 | release | 2025-04-16 | 2025-04-16 10:06:52 | real time |

call API with paramters

| No | startReleaseTime | endReleaseTime | fmidList | response |
| --- | --- | --- | --- | --- |
| 1 | 2025-04-14 05:00:00 | 2025-04-15 05:00:00 | 401036553 | no cashflow accounting records |
| 2 | 2025-04-15 05:00:00 | 2025-04-16 05:00:00 | 401036553 | return cf1 and cf2 accounting records |
| 3 | 2025-04-16 00:00:00 | 2025-04-16 23:00:00 | 401036553 | return cf3 accounting record |
| 4 | 2025-04-15 08:00:00 | 2025-04-16 08:00:00 | 401036553 | return cf2 accounting record |

### Parameters

| name | type | M/O | sample | comment |
| --- | --- | --- | --- | --- |
| startReleaseTime | DateTime(yyyy-mm-dd'T'HH24:MM:SS) need covert to GMT | M | 2026-04-30T00:00:00 | ratan_accounting_request_task_history. created_at >= startReleaseTime |
| endReleaseTime | DateTime(yyyy-mm-dd'T'HH24:MM:SS) need covert to GMT | M | 2026-05-01T00:00:00 | ratan_accounting_request_task_history. created_at < endReleaseTime |
| fmidList | String | M | 10036645,[10075222](http://localhost:8080/v1/accounting/queryReconRecords/?fmidList=10075222&fmidList=10075223&startReleaseTime=2026-04-04T00:00:00&endReleaseTime=2026-04-05T00:00:00) but only support 10036645 currently | ratan_accounting_request_task_history. booking_entity_fmid in fmidList |

Implicit Conditions: **ratan_accounting_request_task_history.task_status = 'SENT'**

**logic**:

step:

- find ratan_accounting_request_task_history max(id) by created_at between startReleaseTime and endReleaseTime, and booking_entity_fmid in (fmidList) , and task_status = 'SENT'
- fetch created_at as publishTime and request_info by ratan_accounting_request_task_history by id = above max(id)
- need add new index for booking_entity_id /created_at/country/task_status column at least

SQL sample:
select distinct on (task_id) id , task_id, rarth.created_at , rarth.request_info from ratan_accounting_request_task_history rarth
where rarth.created_at >= '2026-04-04 01:50:00' and rarth.created_at < '2026-04-04 01:55:00' and booking_entity_fmid in ('10036645')
and task_status in ('SENT') order by task_id, id desc;

### Response

| field name | type | comment |
| --- | --- | --- |
| totalRecords | int | |
| accountingFeeds | JsonArray | message: EBBS json, publishTimestamp |

### Exception code

| | Exception scenario | ErrorMessage |
| --- | --- | --- |
| 1 | When fill in start time after end time | startReleaseTime can not after endReleaseTime |
| 2 | When the period between start time and end time is over 72 hours | can not fetch records over 72 hours |
| 3 | When parameter is empty | Parameters are mandatory |

### EBBS json Sample

**EXPAND: response**

{
"totalNumberOfRecords": 1,
"accountingRecords": [
{
"publishTimestamp": "2024-06-01 12:00:00",
"message": {
"data": {
"id": "Field_Message_ID",
"type": "post-transactions",
"attributes": {
"request": {
"source-system": "RATAN",
"posting-type": "FundsTransfer",
"transaction-type": "RTN",
"posting-branch": "Field_Posting_Branch",
"external-system-key": "Cashflow.Cashflow_Id.Cashflow.Cashflow_Business_Versio.Cashflow.Cashflow_Minor_Version",
"transaction-currency": "Field_Transaction_Currency",
"transaction-amount": "Field_Transaction_Amount",
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
"value-date": "Field_Value_Date",
"account-number": "Field_eBBS_Nostro_Account",
"allow-insufficient-funds": "Y",
"casa-currency-code": "USD",
"transaction-code": "Field_Transaction_code",
"transaction-nature": "Field_eBBS_Nostro_DebitCredit"
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
"value-date": "Field_Value_Date",
"account-number": "Field_eBBS_Bridge_Account",
"allow-insufficient-funds": "Y",
"casa-currency-code": "USD",
"transaction-code": "Field_Transaction_code",
"transaction-nature": "Field_eBBS_Bridge_DebitCredit"
}
]
}
}
}
}
}
]
}

**EXPAND_END**

Field logic:

- **Field_Message_ID**: UUID with max length as 50
- **Field_Posting_Branch: **Need to map according to entity FMID (static data to be maintained in RATAN) **will be empty for Korea **
- **Field_External_System_Key (Mandatory): **Cashflow.Cashflow_Id + "." + Cashflow.Cashflow_Business_Version + "." + Cashflow.Cashflow_Minor_Version - New cashflow C1: Ratan send new entry to eBBS with external id as 'C1.1.1', - Cashflow C1 withdrawal: Ratan send reversal entry to eBBS with external id as 'C1.2.1'
- **Field_Transaction_Currency (Mandatory): ** - Get the cashflow currency Cashflow.Payment_Currency - Query the ISO currency from static data and return **(Speical logica for SG CNH)**.
- **Field_Transaction_Amount: ** 1. Get the Cashflow.Payment_Amount from cashflow data 2. Rounding logic, same logic with SWIFT (Low priority)
- **Field_Value_Date (Mandatory): ** 1. Get Cashflow.Payment_Date from cashflow data 2. Verify the format is YYYY-MM-DD(2024-01-08)
- **Field_eBBS_Nostro_Account (Mandatory): **Get Settlement_Instruction.Account.EBBS_Account_Number and return
- **Field_eBBS_Nostro_DebitCredit (Mandatory):** 1. Get payer reference Cashflow.Payment_Payer_Party_Reference from cashflow 2. if Cashflow.Payment_Payer_Party_Reference == party1 and Cashflow.Cashflow_Event_Type==New then return 'C' else return 'D'
- **Field_eBBS_Bridge_Account (Mandatory)** 1. Get the entity FMID(Entity.Booking_Entity_SCI_FMID) from cashflow 2. Looup the ebbs bridge account number from the static data mapping 'eBBS bridge account mapping', return the ebbs bridge account number
- **Field_Transaction_code: **

According to posting branch and Debit/Credit, get the transaction code from Static table **will be NULL for Korea **

- **Field_eBBS_Bridge_DebitCredit (Mandatory):** 1. Get payer reference Cashflow.Payment_Payer_Party_Reference from cashflow 2. if Cashflow.Payment_Payer_Party_Reference == party1 Cashflow.Cashflow_Event_Type==New then return 'D' else return 'C'

| Path | Field | Type | Length | RATAN Length | Mandatory | Ratan Logic | Comment |
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

**EXPAND: Korea sample**

{
    "totoalNumberOfRecords": 6,
    "accountingRecords": [
        {
            "publishTimeStamp": "2026-04-30 12:18:54",
            "message": {
                "data": {
                    "id": "7455470406176432128",
                    "type": "post-transactions",
                    "attributes": {
                        "request": {
                            "source-system": "RATAN",
                            "posting-type": "FundsTransfer",
                            "transaction-type": "RTN",
                            "posting-branch": "",
                            "external-system-key": "E02026042907.0.17",
                            "transaction-currency": "USD",
                            "transaction-amount": 741600.000,
                            "transaction entry": [
                                {
                                    "narratives": {
                                        "narration1": "DV70E02026042907",
                                        "narration2": "SCB LONDONLDN",
                                        "narration3": "IRDIRS",
                                        "narration4": "5001589576 ",
                                        "narration5": "",
                                        "narration6": "FAILED MUREX"
                                    },
                                    "extended-narratives": {
                                        "extended-narration1": "##",
                                        "extended-narration2": "10036645 SCB SEOULSEL",
                                        "extended-narration3": "",
                                        "extended-narration4": "10075222",
                                        "extended-narration5": "KCNVCNZC SINZCMZMC UNVJ SFVCFV",
                                        "extended-narration6": "IR_KRFB_STIRT"
                                    },
                                    "value-date": "2026-03-30",
                                    "account-number": "040331",
                                    "allow-insufficient-funds": "Y",
                                    "casa-currency-code": "USD",
                                    "transaction-code": null,
                                    "transaction-nature": "C"
                                },
                                {
                                    "narratives": {
                                        "narration1": "DV70E02026042907",
                                        "narration2": "SCB LONDONLDN",
                                        "narration3": "IRDIRS",
                                        "narration4": "5001589576 ",
                                        "narration5": "",
                                        "narration6": "FAILED MUREX"
                                    },
                                    "extended-narratives": {
                                        "extended-narration1": "##",
                                        "extended-narration2": "10036645 SCB SEOULSEL",
                                        "extended-narration3": "",
                                        "extended-narration4": "10075222",
                                        "extended-narration5": "KCNVCNZC SINZCMZMC UNVJ SFVCFV",
                                        "extended-narration6": "IR_KRFB_STIRT"
                                    },
                                    "value-date": "2026-03-30",
                                    "account-number": "040446",
                                    "allow-insufficient-funds": "Y",
                                    "casa-currency-code": "USD",
                                    "transaction-code": null,
                                    "transaction-nature": "D"
                                }
                            ]
                        }
                    }
                }
            }
        },
        {
            "publishTimeStamp": "2026-04-30 08:00:01",
            "message": {
                "data": {
                    "id": "7455510289598246912",
                    "type": "post-transactions",
                    "attributes": {
                        "request": {
                            "source-system": "RATAN",
                            "posting-type": "FundsTransfer",
                            "transaction-type": "RTN",
                            "posting-branch": "",
                            "external-system-key": "E02026042907.0.57",
                            "transaction-currency": "USD",
                            "transaction-amount": 741600.000,
                            "transaction entry": [
                                {
                                    "narratives": {
                                        "narration1": "DV70E02026042907",
                                        "narration2": "SCB LONDONLDN",
                                        "narration3": "IRDIRS",
                                        "narration4": "5001589576 ",
                                        "narration5": "",
                                        "narration6": "FAILED MUREX"
                                    },
                                    "extended-narratives": {
                                        "extended-narration1": "##",
                                        "extended-narration2": "10036645 SCB SEOULSEL",
                                        "extended-narration3": "",
                                        "extended-narration4": "10075222",
                                        "extended-narration5": "KCNVCNZC SINZCMZMC UNVJ SFVCFV",
                                        "extended-narration6": "IR_KRFB_STIRT"
                                    },
                                    "value-date": "2026-03-30",
                                    "account-number": "040331",
                                    "allow-insufficient-funds": "Y",
                                    "casa-currency-code": "USD",
                                    "transaction-code": null,
                                    "transaction-nature": "C"
                                },
                                {
                                    "narratives": {
                                        "narration1": "DV70E02026042907",
                                        "narration2": "SCB LONDONLDN",
                                        "narration3": "IRDIRS",
                                        "narration4": "5001589576 ",
                                        "narration5": "",
                                        "narration6": "FAILED MUREX"
                                    },
                                    "extended-narratives": {
                                        "extended-narration1": "##",
                                        "extended-narration2": "10036645 SCB SEOULSEL",
                                        "extended-narration3": "",
                                        "extended-narration4": "10075222",
                                        "extended-narration5": "KCNVCNZC SINZCMZMC UNVJ SFVCFV",
                                        "extended-narration6": "IR_KRFB_STIRT"
                                    },
                                    "value-date": "2026-03-30",
                                    "account-number": "040446",
                                    "allow-insufficient-funds": "Y",
                                    "casa-currency-code": "USD",
                                    "transaction-code": null,
                                    "transaction-nature": "D"
                                }
                            ]
                        }
                    }
                }
            }
        },
        {
            "publishTimeStamp": "2026-04-30 08:00:01",
            "message": {
                "data": {
                    "id": "7455510349136392192",
                    "type": "post-transactions",
                    "attributes": {
                        "request": {
                            "source-system": "RATAN",
                            "posting-type": "FundsTransfer",
                            "transaction-type": "RTN",
                            "posting-branch": "",
                            "external-system-key": "E02026042907.0.59",
                            "transaction-currency": "USD",
                            "transaction-amount": 741600.000,
                            "transaction entry": [
                                {
                                    "narratives": {
                                        "narration1": "DV70E02026042907",
                                        "narration2": "SCB LONDONLDN",
                                        "narration3": "IRDIRS",
                                        "narration4": "5001589576 ",
                                        "narration5": "",
                                        "narration6": "QUEUED MUREX"
                                    },
                                    "extended-narratives": {
                                        "extended-narration1": "##",
                                        "extended-narration2": "10036645 SCB SEOULSEL",
                                        "extended-narration3": "",
                                        "extended-narration4": "10075222",
                                        "extended-narration5": "KCNVCNZC SINZCMZMC UNVJ SFVCFV",
                                        "extended-narration6": "IR_KRFB_STIRT"
                                    },
                                    "value-date": "2026-03-30",
                                    "account-number": "040331",
                                    "allow-insufficient-funds": "Y",
                                    "casa-currency-code": "USD",
                                    "transaction-code": "",
                                    "transaction-nature": "D"
                                },
                                {
                                    "narratives": {
                                        "narration1": "DV70E02026042907",
                                        "narration2": "SCB LONDONLDN",
                                        "narration3": "IRDIRS",
                                        "narration4": "5001589576 ",
                                        "narration5": "",
                                        "narration6": "QUEUED MUREX"
                                    },
                                    "extended-narratives": {
                                        "extended-narration1": "##",
                                        "extended-narration2": "10036645 SCB SEOULSEL",
                                        "extended-narration3": "",
                                        "extended-narration4": "10075222",
                                        "extended-narration5": "KCNVCNZC SINZCMZMC UNVJ SFVCFV",
                                        "extended-narration6": "IR_KRFB_STIRT"
                                    },
                                    "value-date": "2026-03-30",
                                    "account-number": "040446",
                                    "allow-insufficient-funds": "Y",
                                    "casa-currency-code": "USD",
                                    "transaction-code": "",
                                    "transaction-nature": "C"
                                }
                            ]
                        }
                    }
                }
            }
        },
        {
            "publishTimeStamp": "2026-04-30 08:00:01",
            "message": {
                "data": {
                    "id": "7455511699463204864",
                    "type": "post-transactions",
                    "attributes": {
                        "request": {
                            "source-system": "RATAN",
                            "posting-type": "FundsTransfer",
                            "transaction-type": "RTN",
                            "posting-branch": "",
                            "external-system-key": "E02026043001.0.10",
                            "transaction-currency": "KRW",
                            "transaction-amount": 741600.000,
                            "transaction entry": [
                                {
                                    "narratives": {
                                        "narration1": "DV70E02026043001",
                                        "narration2": "SCB LONDONLDN",
                                        "narration3": "IRDIRS",
                                        "narration4": "5001589576 ",
                                        "narration5": "",
                                        "narration6": "FAILED MUREX"
                                    },
                                    "extended-narratives": {
                                        "extended-narration1": "##",
                                        "extended-narration2": "10036645 SCB SEOULSEL",
                                        "extended-narration3": "",
                                        "extended-narration4": "10075222",
                                        "extended-narration5": "KCNVCNZC SINZCMZMC UNVJ SFVCFV",
                                        "extended-narration6": "IR_KRFB_STIRT"
                                    },
                                    "value-date": "2026-03-30",
                                    "account-number": "001190",
                                    "allow-insufficient-funds": "Y",
                                    "casa-currency-code": "KRW",
                                    "transaction-code": null,
                                    "transaction-nature": "C"
                                },
                                {
                                    "narratives": {
                                        "narration1": "DV70E02026043001",
                                        "narration2": "SCB LONDONLDN",
                                        "narration3": "IRDIRS",
                                        "narration4": "5001589576 ",
                                        "narration5": "",
                                        "narration6": "FAILED MUREX"
                                    },
                                    "extended-narratives": {
                                        "extended-narration1": "##",
                                        "extended-narration2": "10036645 SCB SEOULSEL",
                                        "extended-narration3": "",
                                        "extended-narration4": "10075222",
                                        "extended-narration5": "KCNVCNZC SINZCMZMC UNVJ SFVCFV",
                                        "extended-narration6": "IR_KRFB_STIRT"
                                    },
                                    "value-date": "2026-03-30",
                                    "account-number": "000287",
                                    "allow-insufficient-funds": "Y",
                                    "casa-currency-code": "KRW",
                                    "transaction-code": null,
                                    "transaction-nature": "D"
                                }
                            ]
                        }
                    }
                }
            }
        },
        {
            "publishTimeStamp": "2026-04-30 08:00:01",
            "message": {
                "data": {
                    "id": "7455514155421134849",
                    "type": "post-transactions",
                    "attributes": {
                        "request": {
                            "source-system": "RATAN",
                            "posting-type": "FundsTransfer",
                            "transaction-type": "RTN",
                            "posting-branch": "",
                            "external-system-key": "E02026043001.0.12",
                            "transaction-currency": "KRW",
                            "transaction-amount": 741600.000,
                            "transaction entry": [
                                {
                                    "narratives": {
                                        "narration1": "DV70E02026043001",
                                        "narration2": "SCB LONDONLDN",
                                        "narration3": "IRDIRS",
                                        "narration4": "5001589576 ",
                                        "narration5": "",
                                        "narration6": "QUEUED MUREX"
                                    },
                                    "extended-narratives": {
                                        "extended-narration1": "##",
                                        "extended-narration2": "10036645 SCB SEOULSEL",
                                        "extended-narration3": "",
                                        "extended-narration4": "10075222",
                                        "extended-narration5": "KCNVCNZC SINZCMZMC UNVJ SFVCFV",
                                        "extended-narration6": "IR_KRFB_STIRT"
                                    },
                                    "value-date": "2026-03-30",
                                    "account-number": "001190",
                                    "allow-insufficient-funds": "Y",
                                    "casa-currency-code": "KRW",
                                    "transaction-code": "",
                                    "transaction-nature": "D"
                                },
                                {
                                    "narratives": {
                                        "narration1": "DV70E02026043001",
                                        "narration2": "SCB LONDONLDN",
                                        "narration3": "IRDIRS",
                                        "narration4": "5001589576 ",
                                        "narration5": "",
                                        "narration6": "QUEUED MUREX"
                                    },
                                    "extended-narratives": {
                                        "extended-narration1": "##",
                                        "extended-narration2": "10036645 SCB SEOULSEL",
                                        "extended-narration3": "",
                                        "extended-narration4": "10075222",
                                        "extended-narration5": "KCNVCNZC SINZCMZMC UNVJ SFVCFV",
                                        "extended-narration6": "IR_KRFB_STIRT"
                                    },
                                    "value-date": "2026-03-30",
                                    "account-number": "000287",
                                    "allow-insufficient-funds": "Y",
                                    "casa-currency-code": "KRW",
                                    "transaction-code": "",
                                    "transaction-nature": "C"
                                }
                            ]
                        }
                    }
                }
            }
        },
        {
            "publishTimeStamp": "2026-04-30 09:14:40",
            "message": {
                "data": {
                    "id": "7455545148714524672",
                    "type": "post-transactions",
                    "attributes": {
                        "request": {
                            "source-system": "RATAN",
                            "posting-type": "FundsTransfer",
                            "transaction-type": "RTN",
                            "posting-branch": "",
                            "external-system-key": "E02026043002.0.31",
                            "transaction-currency": "KRW",
                            "transaction-amount": 741600.000,
                            "transaction entry": [
                                {
                                    "narratives": {
                                        "narration1": "DV70E02026043002",
                                        "narration2": "SCB LONDONLDN",
                                        "narration3": "IRDIRS",
                                        "narration4": "5001589576 ",
                                        "narration5": "",
                                        "narration6": "SETTLED MUREX"
                                    },
                                    "extended-narratives": {
                                        "extended-narration1": "##",
                                        "extended-narration2": "10036645 SCB SEOULSEL",
                                        "extended-narration3": "",
                                        "extended-narration4": "10075222",
                                        "extended-narration5": "KCNVCNZC SINZCMZMC UNVJ SFVCFV",
                                        "extended-narration6": "IR_KRFB_STIRT"
                                    },
                                    "value-date": "2026-03-30",
                                    "account-number": "3457254675288907910980",
                                    "allow-insufficient-funds": "Y",
                                    "casa-currency-code": "KRW",
                                    "transaction-code": null,
                                    "transaction-nature": "C"
                                },
                                {
                                    "narratives": {
                                        "narration1": "DV70E02026043002",
                                        "narration2": "SCB LONDONLDN",
                                        "narration3": "IRDIRS",
                                        "narration4": "5001589576 ",
                                        "narration5": "",
                                        "narration6": "SETTLED MUREX"
                                    },
                                    "extended-narratives": {
                                        "extended-narration1": "##",
                                        "extended-narration2": "10036645 SCB SEOULSEL",
                                        "extended-narration3": "",
                                        "extended-narration4": "10075222",
                                        "extended-narration5": "KCNVCNZC SINZCMZMC UNVJ SFVCFV",
                                        "extended-narration6": "IR_KRFB_STIRT"
                                    },
                                    "value-date": "2026-03-30",
                                    "account-number": "000287",
                                    "allow-insufficient-funds": "Y",
                                    "casa-currency-code": "KRW",
                                    "transaction-code": null,
                                    "transaction-nature": "D"
                                }
                            ]
                        }
                    }
                }
            }
        }
    ],
    "errorMessage": null
}

**EXPAND_END**

**EXPAND: uat sample**

{
    "totoalNumberOfRecords": 1,
    "accountingRecords": [
        {
            "publishTimeStamp": "2026-05-21 06:49:15",
            "message": {
                "data": {
                    "id": "7463118698072694784",
                    "type": "post-transactions",
                    "attributes": {
                        "request": {
                            "source-system": "RATAN",
                            "posting-type": "FundsTransfer",
                            "transaction-type": "RTN",
                            "posting-branch": "",
                            "external-system-key": "M00005776864.0.8",
                            "transaction-currency": "USD",
                            "transaction-amount": 92134.500,
                            "transaction entry": [
                                {
                                    "narratives": {
                                        "narration1": "DV70M00005776864",
                                        "narration2": "HSBCSEL",
                                        "narration3": "IRDCS",
                                        "narration4": "5001332739 ",
                                        "narration5": "",
                                        "narration6": "RELEASED MUREX"
                                    },
                                    "extended-narratives": {
                                        "extended-narration1": "##",
                                        "extended-narration2": "10036645 SCB SEOULSEL",
                                        "extended-narration3": "",
                                        "extended-narration4": "300072385",
                                        "extended-narration5": "TII IUXTQUXT PXE SIPXTIPB IPXQBXT",
                                        "extended-narration6": "IR_KRFB_OPT_KRO"
                                    },
                                    "value-date": "2026-03-30",
                                    "account-number": "040331",
                                    "allow-insufficient-funds": "Y",
                                    "casa-currency-code": "USD",
                                    "transaction-code": null,
                                    "transaction-nature": "C"
                                },
                                {
                                    "narratives": {
                                        "narration1": "DV70M00005776864",
                                        "narration2": "HSBCSEL",
                                        "narration3": "IRDCS",
                                        "narration4": "5001332739 ",
                                        "narration5": "",
                                        "narration6": "RELEASED MUREX"
                                    },
                                    "extended-narratives": {
                                        "extended-narration1": "##",
                                        "extended-narration2": "10036645 SCB SEOULSEL",
                                        "extended-narration3": "",
                                        "extended-narration4": "300072385",
                                        "extended-narration5": "TII IUXTQUXT PXE SIPXTIPB IPXQBXT",
                                        "extended-narration6": "IR_KRFB_OPT_KRO"
                                    },
                                    "value-date": "2026-03-30",
                                    "account-number": "040446",
                                    "allow-insufficient-funds": "Y",
                                    "casa-currency-code": "USD",
                                    "transaction-code": null,
                                    "transaction-nature": "D"
                                }
                            ]
                        }
                    }
                }
            }
        }
    ],
    "errorMessage": null
}

**EXPAND_END**

Timing cost:

![image-2026-6-11_17-31-52.png](attachments/image-2026-6-11_17-31-52.png)![image-2026-7-8_16-24-25.png](attachments/image-2026-7-8_16-24-25.png)

PT result:

releaseTimeScope: 2026-07-22T00:00:00 → 2026-07-25T00:00:00

response total accounting feeds: 20286

[Apache JMeter Dashboard](https://uklvadrtn006a.pi.dev.net:8081/performance-test/1785131956910/report/index.html)