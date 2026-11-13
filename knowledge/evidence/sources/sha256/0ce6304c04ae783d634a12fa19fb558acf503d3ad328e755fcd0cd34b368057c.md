# [The purpose](https://confluence.global.standardchartered.com/display/DSP/The+cache+data+layer+design#Thecachedatalayerdesign-Thepurpose)

This document is use for defining the solution of how to expose cashflow data to other system.

# Requirement

Needs to supported expose data at any time.

Needs to return all valid data that meets the query criteria.

| System | User id | Role in EMS2 | Note |
| --- | --- | --- | --- |
| RATANEOD | srv.ratan.001 | RATAN_FUNC: SYS_RO | |
| DQSL | fmdp_dqsl_batch | RATAN_FUNC: SYS_RO | request from SSDR |
| FMMIS | g.fmoappdev.001 | RATAN_FUNC: SYS_RO | |

# Design

## Phase one

### Scenario for phase one :

- Cashflow below 100,000 records in database
- CN DayOne Release

### PT for this Scenario

[PT-Ratan expose the cashflow data to SSDR - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/PT-Ratan+expose+the+cashflow+data+to+SSDR)

### Question mark

- frequency of daily query - about 20~50 tims in half an hour
- Expected return time
- could SSDR team provide the attributes in the query condition

### Query Interface

| API Name | Interface | Method | Request Sample | Response Sample | Header | Scenario | Note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Query Cashflows | http://{domain}/v1/data/provider/query/cashflows | Post | { queryCondition：“SQL string” } | { [cashflow info list with json formatt] } | FMAA-Token：“string” FMAA-UserId:"string" FMAA-AppId:"string" Bank-Id:"string"(only for DQSL) Country : string"(only for DQSL) | records less than 30000 ，2 request/second for each node | [[RATAN-16976] RATAN EOD query support - [Backend] PT research for query cashflow data based on 30K - Jira (standardchartered.com)](https://jira.global.standardchartered.com/browse/RATAN-16976) |

| ENV | URL |
| --- | --- |
| Dev | [http://10.198.199.160:8868/v1/data/provider/query/cashflows](http://10.198.199.160:8868/v1/data/provider/query/cashflows) |
| SIT | [https://ratan-aws-sit-ns4-fmo-shell.ir.standardchartered.com/api/v1/data/provider/query/cashflows](https://ratan-aws-sit-ns4-fmo-shell.ir.standardchartered.com/api/v1/data/provider/query/cashflows) |
| Uat | [https://fmo-shell.uk.dev.net:8453/api/v1/data/provider/query/cashflows](https://fmo-shell.uk.dev.net:8453/api/v1/data/provider/query/cashflows) |
| Staging | [https://uklvadrtn002a.pi.dev.net:8868/v1/data/provider/query/cashflows](https://uklvadrtn002a.pi.dev.net:8868/v1/data/provider/query/cashflows) |
| Prod | [https://fmo-shell.gdc.standardchartered.com:8453/api/v1/data/provider/query/cashflows](https://fmo-shell.gdc.standardchartered.com:8453/api/v1/data/provider/query/cashflows) |

| http response code | Behavior | Note |
| --- | --- | --- |
| 200 | OK | |
| 400 | Bad Request | |
| 401 | Unauthorized | |
| 461 | invalid SQL, the SQL not query type ,unsupported operation | will return different message for different error: 1)dataEntitlement Role or userCountry is null value 2)invalid SQL, the SQL with unsupported operation or fields 3)get data entitlement error |
| 462 | 1. System is Busy, try later pls 2. too many records, please use limit to split the sql | |
| 463 | get data entitlement rule fail | |
| 500 | Internal Server Error | |
| 502 | Bad Gateway | |
| 503 | Service Unavailable | |
| 504 | Gateway Timeout | |
| 505 | HTTP Version Not Supported | |

### Request header

| Header Name | Data Type | mandatory/optional | Field Description | note |
| --- | --- | --- | --- | --- |
| FMAA-Token | String | mandatory | the token which was got from FMAA endpoint | |
| FMAA-UserId | String | mandatory | same value with user_id when create FMAA token | |
| FMAA-AppId | String | mandatory | same value with app_id when create FMAA token | |
| Bank-Id | String | optional | user id in bank | if has this attribute and Country in the request header will handle request as return data to SSDR, else will handle request as return data to EOD |
| Country | String | optional | country code from OUD | if has this attribute and Bank-Id in the request header will handle request as return data to SSDR, else will handle request as return data to EOD |
| | | | | |

### Request Sample

**EXPAND: query cashflow request sample**

```groovy
{
    "queryCondition": "Select Data_Flow.Data_Source_System,Data_Flow.Data_Source_System_Country_Code,Data_Flow.Data_Source_System_Domain_Name,Data_Flow.Data_Type,Cashflow.Cashflow_Id,Cashflow.Cashflow_Version,Cashflow.Cashflow_Business_Version,Cashflow.Cashflow_State,Cashflow.Event_Physical_Status,Cashflow.Cashflow_Event_Type,Cashflow.Status_Event_Type,Cashflow.Event_Date,Cashflow.Payment_Payer_Party_Reference,Cashflow.Payment_Receiver_Party_Reference,Cashflow.Payment_Currency,Cashflow.Payment_Amount,Cashflow.Payment_Date,Cashflow.Payment_Date_Business_Day_Convention,Cashflow.Netting_Id,Instrument_Common.CFI_Code,Instrument_Common.ISDA_Taxonomy,Trade_State,Trade_Id,Cashflow.Position_Id,Parent_Trade_Id,Entity.Booking_Entity_SCI_FMID,Entity.Counterparty_SCI_FMID,Settlement_Method,Delivery_Method,Entity.Counterparty_SCI_FMCODE,Entity.Counterparty_CIF_Code,Entity.Counterparty_Source_System_Entity_Id,Cashflow.Pay_Receive_Indicator,Cashflow.Payer_Name,Cashflow.Is_Private_Banking_Cashflow,Cashflow.Is_Amended_Post_Settlement,Cashflow.Payment_Type,Cashflow.Is_Cashflow_Unnet,Cashflow.Transaction_Details,Data_Flow.Unique_Identifier_Message_Id,Execution_Date_Time,Entity.General_Ledger_Business_Unit_Name,Entity.Booking_Entity_General_Ledger_Business_Unit_Id,Trade_Lake_Valid_From_Date_Time,Trade_Lake_Valid_To_Date_Time,Trade_Lake_Latest_Event_Date_Time,Trade_Lake_Raw_Event_Date_Time,Trade_Lake_Transaction_From_Date_Time,Trade_Lake_Transaction_To_Date_Time,BCS_Parent_Trade_Id,BCS_Trade_Id,Trade_Version,Portfolio.Booking_Entity_Trade_Portfolio_Name,Cashflow.Cashflow_Affirmation_Status,Cashflow.Is_STP_RATAN,Cashflow.Is_STP,Cashflow.NSTP_Reason,Settlement_Instruction.Account.EBBS_Bridge_Account_Number,Settlement_Instruction.Account.EBBS_Account_Number,Settlement_Instruction.Account.Booking_Entity_Correspondent_BIC_code,Settlement_Instruction.Account.Booking_Entity_Correspondent_Account_Name,Settlement_Instruction.Account.Booking_Entity_Correspondent_Street_Address,Settlement_Instruction.Account.Booking_Entity_Correspondent_City,Settlement_Instruction.Account.Booking_Entity_Correspondent_Account_Number,Cashflow.Cashflow_Sub_State,Cashflow.Cashflow_Sub_State_Updater,Cashflow.Cashflow_Sub_State_Type,Cashflow.Prev_Cashflow_Id,Cashflow.Next_Cashflow_Id,Cashflow.Validation_Status,Cashflow.Exception_Reason,Cashflow.FMO_Comment,Cashflow.FMO_Comment_Updater,Cashflow.FMO_Comment_Timestamp,Cashflow.STP_Cutoff_Date_Time,Cashflow.Netting_Cuttoff_Date,Entity.Booking_Entity_SCI_FMCODE,Cashflow.Cashflow_Audit_Version,Cashflow.Payment_Cutoff_Time,Settlement_Instruction.Nostro_Swift_Message_Type,Cashflow.Minor_Version_Description,Cashflow.Bypass_Workflow_Indicator,Cashflow.Cashflow_Minor_Version,Settlement_Instruction.SSI_Unique_Id,Settlement_Instruction.SSI_Source,Settlement_Instruction.SSI_Priority,Settlement_Instruction.Swift_Message_Type,Settlement_Instruction.Account.SCB_Nostro_Account_Number,Settlement_Instruction.Account.SCB_Nostro_Account_Type,Settlement_Instruction.Account.Beneficiary_BIC_code,Settlement_Instruction.Account.Beneficiary_Account_Name,Settlement_Instruction.Account.Beneficiary_Account_Name_2,Settlement_Instruction.Account.Beneficiary_Street_Address,Settlement_Instruction.Account.Beneficiary_City,Settlement_Instruction.Account.Beneficiary_Account_Number,Settlement_Instruction.Account.Intermediary_BIC_code,Settlement_Instruction.Account.Intermediary_Account_Name,Settlement_Instruction.Account.Intermediary_Street_Address,Settlement_Instruction.Account.Intermediary_City,Settlement_Instruction.Account.Intermediary_Account_Number,Settlement_Instruction.Account.Beneficiary_Bank_BIC_code,Settlement_Instruction.Account.Beneficiary_Bank_Account_Name,Settlement_Instruction.Account.Beneficiary_Bank_Street_Address,Settlement_Instruction.Account.Beneficiary_Bank_City,Settlement_Instruction.Account.Beneficiary_Bank_Account_Number,Settlement_Instruction.Account.Beneficiary_Correspondent_BIC_code,Settlement_Instruction.Account.Beneficiary_Correspondent_Account_Name,Settlement_Instruction.Account.Beneficiary_Correspondent_Street_Address,Settlement_Instruction.Account.Beneficiary_Correspondent_City,Settlement_Instruction.Account.Beneficiary_Correspondent_Account_Number,Settlement_Instruction.Account.Ordering_Customer_BIC_Code,Settlement_Instruction.Account.Ordering_Customer_Account_Name,Settlement_Instruction.Account.Ordering_Customer_Street_Address,Settlement_Instruction.Account.Ordering_Customer_City,Settlement_Instruction.Account.Ordering_Customer_Account_Number,Settlement_Instruction.Remittance_Information_1,Settlement_Instruction.Remittance_Information_2,Settlement_Instruction.Remittance_Information_3,Settlement_Instruction.Remittance_Information_4,Settlement_Instruction.Sender_To_Receiver_Information_1,Settlement_Instruction.Sender_To_Receiver_Information_2,Settlement_Instruction.Sender_To_Receiver_Information_3,Settlement_Instruction.Sender_To_Receiver_Information_4,Settlement_Instruction.Sender_To_Receiver_Information_5,Settlement_Instruction.Sender_To_Receiver_Information_6,Settlement_Instruction.Account.Counterparty_CMS_Account_Number,Settlement_Instruction.Is_Third_Party_Payment,Settlement_Instruction.Swift_Payment_Method,Settlement_Instruction.Charge_Bearer,Instrument_Common.Source_System_Instrument_Sub_Type,Portfolio.Booking_Entity_Trade_Portfolio_Unique_Name,Entity.Person.Coverage_Marketer_PSID,Entity.Person.Event_Coverage_Marketer_PSID,Entity.Person.Execution_Marketer_PSID,Entity.Person.Event_Execution_Marketer_PSID,Entity.Person.Booking_Marketer_PSID,Entity.Person.Event_Booking_Marketer_PSID,Entity.Person.Trader_PSID,Entity.Person.Event_Trader_PSID,Trade.Event_Physical_Status,Resultant_Position_Id,Trade_Original_Source_System_Name,Cashflow.Is_Payment_Intent_To_Settle,Cashflow.Action_Type,Cashflow.Cashflow_Event_Reason,Settlement_Instruction.Value_Date,Settlement_Instruction.Value_Date_Business_Day_Convention,Instrument_Common.Financial_Instrument_Code,Cashflow.Cashflow_Major_Version,Cashflow.Cashflow_SubEvent_Type,Cashflow_Sequence,Effective_Date_Time,Entity.Booking_Entity_Country_ISO_Code,TP_System_Name,Trade_Purpose,Cashflow.Audit from cash_settlement_query_cn.cashflow_data LIMIT  1  OFFSET  0"
    }
```

**EXPAND_END**

### Response Sample

**EXPAND: query cashflow response sample**

```
[
    {
        "Settlement_Instruction.Account.Ordering_Customer_Account_Name": "",
        "Settlement_Instruction.Account.Intermediary_Account_Number": "",
        "Settlement_Instruction.Account.Beneficiary_Correspondent_City": "",
        "Settlement_Instruction.Swift_Payment_Method": "",
        "Trade.Trade_Lake_Transaction_To_Date_Time": null,
        "Settlement_Instruction.Account.Intermediary_Account_Name": "",
        "Trade.Position_Id": "",
        "Settlement_Instruction.Sender_To_Receiver_Information_2": "",
        "Settlement_Instruction.Sender_To_Receiver_Information_1": "",
        "Cashflow.Cashflow_Event_Type": "New",
        "Data_Flow.Data_Publication_Id": "MUREX-91207191--2023-05-05T10:04:12Z",
        "Cashflow.Cashflow_Sub_State_Updater": "System",
        "Cashflow.Netting_Id": "",
        "Cashflow.Cashflow_Business_Version": "0",
        "Data_Flow.Data_Source_System": "MUREX",
        "Trade.Trade_Lake_Valid_To_Date_Time": null,
        "Cashflow.Is_Private_Banking_Cashflow": "f",
        "Cashflow.Exception_Reason": null,
        "Settlement_Instruction.SSI_Priority": "",
        "Settlement_Instruction.Account.Beneficiary_Correspondent_BIC_code": "",
        "Settlement_Instruction.Account.Beneficiary_Correspondent_Account_Number": "",
        "Trade.Trade_Id": "79547212",
        "Trade.Trade_Lake_Transaction_From_Date_Time": null,
        "Cashflow.Payment_Cutoff_Time": null,
        "Cashflow.Payment_Receiver_Party_Reference": "party2",
        "Cashflow.Cashflow_Sub_State": "NA",
        "Trade.Action_Type": "",
        "Entity.Booking_Entity_General_Ledger_Business_Unit_Id": "",
        "Trade.Resultant_Position_Id": "",
        "Data_Flow.Data_Sender": null,
        "Cashflow.Prev_Cashflow_Id": null,
        "Settlement_Instruction.Account.Beneficiary_Bank_Account_Number": "",
        "Entity.Counterparty_CIF_Code": null,
        "Cashflow.Is_Amended_Post_Settlement": null,
        "Cashflow.Cashflow_Affirmation_Status": "Unaffirmed",
        "Settlement_Instruction.Account.Booking_Entity_Correspondent_City": "",
        "Entity.Counterparty_SCI_FMID": "",
        "Data_Flow.Data_Type": "CashflowData",
        "Entity.Counterparty_Source_System_Entity_Id": "",
        "Cashflow.Is_STP": null,
        "Cashflow.Payment_Payer_Party_Reference": "party1",
        "Cashflow.Is_STP_RATAN": null,
        "Portfolio.Booking_Entity_Trade_Portfolio_Unique_Name": "",
        "Settlement_Instruction.Account.Beneficiary_Bank_Street_Address": "",
        "Cashflow.STP_Cutoff_Date_Time": null,
        "Cashflow.Validation_Status": null,
        "Settlement_Instruction.Charge_Bearer": "",
        "Settlement_Instruction.Account.Beneficiary_Bank_Account_Name": "",
        "Settlement_Instruction.Account.Beneficiary_Correspondent_Account_Name": "",
        "Data_Flow.Unique_Identifier_Message_Id": "b1b376ab-df92-4b2e-8243-beefcb7f5e11",
        "Cashflow.Cashflow_Minor_Version": "0",
        "Settlement_Instruction.Account.EBBS_Bridge_Account_Number": "",
        "Settlement_Instruction.Account.EBBS_Account_Number": "",
        "Cashflow.FMO_Comment_Updater": null,
        "Trade.Trade_Lake_Latest_Event_Date_Time": null,
        "Settlement_Instruction.Account.Booking_Entity_Correspondent_Account_Name": "",
        "Settlement_Instruction.Account.Beneficiary_Bank_City": "",
        "Cashflow.Payment_Date": "2023-03-20",
        "Settlement_Instruction.Is_Third_Party_Payment": "",
        "Instrument_Common.ISDA_Taxonomy": "",
        "Cashflow.Cashflow_Sub_State_Type": "NA",
        "Cashflow.Pay_Receive_Indicator": "Pay",
        "Entity.Counterparty_SCI_FMCODE": "",
        "Cashflow.Payer_Name": "BANGKOK",
        "Cashflow.Execution_Date_Time": "2023-01-08 14:32:52",
        "Cashflow.NSTP_Reason": "",
        "Settlement_Instruction.Account.Intermediary_Street_Address": "",
        "Cashflow.Payment_Currency": "THO",
        "Trade.Trade_State": "TOBESENT",
        "Trade.Trade_Lake_Raw_Event_Date_Time": null,
        "Settlement_Instruction.SSI_Source": "",
        "Settlement_Instruction.Account.Beneficiary_City": "",
        "Cashflow.Transaction_Details": "",
        "Settlement_Instruction.Account.Ordering_Customer_Account_Number": "",
        "Trade.Event_Physical_Status": "",
        "Settlement_Instruction.Account.Beneficiary_BIC_code": "",
        "Settlement_Instruction.SSI_Unique_Id": "",
        "Settlement_Instruction.Account.Counterparty_CMS_Account_Number": "",
        "Settlement_Instruction.Account.Beneficiary_Bank_BIC_code": "",
        "Settlement_Instruction.Account.Ordering_Customer_Street_Address": "",
        "Cashflow.Is_Cashflow_Unnet": "f",
        "Cashflow.Next_Cashflow_Id": null,
        "Cashflow.Cashflow_Audit_Version": null,
        "Settlement_Instruction.Account.Ordering_Customer_City": "",
        "Entity.General_Ledger_Business_Unit_Name": "",
        "Entity.Booking_Entity_SCI_FMCODE": null,
        "Data_Flow.Data_Source_System_Domain_Name": "FM",
        "Cashflow.Payment_Type": "",
        "Cashflow.Status_Event_Type": "New",
        "Cashflow.Is_Payment_Intent_To_Settle": "f",
        "Settlement_Instruction.Account.Beneficiary_Street_Address": "",
        "Instrument_Common.CFI_Code": "",
        "Settlement_Instruction.Nostro_Swift_Message_Type": "",
        "Trade.Trade_Original_Source_System_Name": "",
        "Cashflow.Cashflow_Id": "M00091207191",
        "Settlement_Instruction.Account.Intermediary_BIC_code": "",
        "Cashflow.FMO_Comment": null,
        "Trade.Trade_Lake_Valid_From_Date_Time": null,
        "Cashflow.Minor_Version_Description": "0",
        "Entity.Booking_Entity_SCI_FMID": "",
        "Settlement_Instruction.Account.SCB_Nostro_Account_Type": "",
        "Cashflow.Cashflow_State": "PROJECTED",
        "Cashflow.FMO_Comment_Timestamp": null,
        "Data_Flow.Data_Source_System_Country_Code": "ALL",
        "Cashflow.Payment_Amount": "44888004.720000",
        "Cashflow.Event_Date": "2023-01-08",
        "Settlement_Instruction.Remittance_Information_2": "",
        "Settlement_Instruction.Remittance_Information_3": "",
        "Settlement_Instruction.Account.Ordering_Customer_BIC_Code": "",
        "Settlement_Instruction.Remittance_Information_4": "",
        "Portfolio.Booking_Entity_Trade_Portfolio_Name": "THB LOCAL SWAPS",
        "Data_Flow.Data_Publication_Date_Time": "2023-05-05 18:04:12",
        "Settlement_Instruction.Remittance_Information_1": "",
        "Settlement_Instruction.Account.Beneficiary_Account_Number": "",
        "Cashflow.Cashflow_Version": "0",
        "Settlement_Instruction.Account.Booking_Entity_Correspondent_Street_Address": "",
        "Trade.Parent_Trade_Id": "",
        "Cashflow.Payment_Date_Business_Day_Convention": "NONE",
        "Settlement_Instruction.Account.Booking_Entity_Correspondent_Account_Number": "",
        "Settlement_Instruction.Account.Booking_Entity_Correspondent_BIC_code": "",
        "Settlement_Instruction.Account.SCB_Nostro_Account_Number": "",
        "Settlement_Instruction.Sender_To_Receiver_Information_4": "",
        "Settlement_Instruction.Sender_To_Receiver_Information_3": "",
        "Settlement_Instruction.Account.Beneficiary_Correspondent_Street_Address": "",
        "Settlement_Instruction.Sender_To_Receiver_Information_6": "",
        "Settlement_Instruction.Account.Beneficiary_Account_Name_2": "",
        "Settlement_Instruction.Sender_To_Receiver_Information_5": "",
        "Cashflow.Bypass_Workflow_Indicator": null,
        "Settlement_Instruction.Account.Intermediary_City": "",
        "Settlement_Instruction.Account.Beneficiary_Account_Name": "",
        "Settlement_Instruction.Swift_Message_Type": "",
        "Cashflow.Audit": {
            "touchPointHistory": [
                {
                    "time": "2023-11-21 05:02:08.968011",
                    "user": "1129381",
                    "action": "Materialize"
                }
            ],
            "exceptionList": [
                {
                    "exceptionCode": "Missing Nostro",
                    "businessFlow": "SETTLEMENT",
                    "sourceSystem": "RATAN",
                    "exceptionType": "BUSINESS",
                    "description": "MISSING_NOSTRO_ERROR",
                    "status": "PENDING_OPERATOR"
                }
            ]
        }  
   } ]
```

**EXPAND_END**

**EXPAND: response for 461 Role or country is null**

```
dataEntitlement Role or userCountry is null value
```

**EXPAND_END**

**EXPAND: response for 461 for invalid SQL**

```
invalid SQL, the SQL with unsupported operation
```

**EXPAND_END**

**EXPAND: response for 461 get data entitlement rule error**

```
get data entitlement error
```

**EXPAND_END**

## Phase two

### Scenario for phase two:

- Cashflow more than 300,000 records in database
- Query response time more than 60 seconds and get result less than 100,000 records

### Enhancement part

remove useless columns.

all the column in the query condition need to set default and set to not null.

set suitable DB type for the column which in the query condition.

set index for the column which in the query condition.

### Question mark

So far, RatanOne have two DB instance , one of it is work for DR. If we would like to use leader-follower mode could it support ？

For the follower need to set  hot_standby=on

### Query Interface

| API Name | Interface | Method | Request Sample | Response Sample | Header |
| --- | --- | --- | --- | --- | --- |
| Query Cashflows | http://{domain}/v1/data/provider/query/cashflows | Post | { queryCondition：“SQL string” } | { [cashflow info list with json formatt] } | FMAA-Token：“string” FMAA-UserId:"string" FMAA-AppId:"string" Bank-Id:"string"(only for DQSL) Country：string"(only for DQSL) |

| http response code | Behavior | Note |
| --- | --- | --- |
| 200 | OK | |
| 400 | Bad Request | |
| 401 | Unauthorized | |
| 402 | Payment Required | |
| 403 | Forbidden | |
| 404 | Not Found | |
| 405 | Method Not Allowed | |
| 406 | Not Acceptable | |
| 415 | Unsupported Media Type | |
| 429 | Too Many Requests | |
| 500 | Internal Server Error | |
| 502 | Bad Gateway | |
| 503 | Service Unavailable | |
| 504 | Gateway Timeout | |
| 505 | HTTP Version Not Supported | |

### Response Sample

**EXPAND: Cashflow response sample**

```
[
    {
        "id": "38eb34c3199f367921461b81f5dd4e1e",
        "trade_id": "85672071",
        "trade_state": "CONFIRMED",
        "cashflow_index": "600000009126",
        "cashflow_status": "QUEUED",
        "cashflow__cashflow_event_type": "New"
    },
    {
        "id": "635d7a7ffec22e5798ff359f0f6ee79a",
        "trade_id": "85672071",
        "trade_state": "CONFIRMED",
        "cashflow_index": "600000009127",
        "cashflow_status": "QUEUED",
        "cashflow__cashflow_event_type": "New"
    },
    {
        "id": "5acedc6b9233d6bbc4b04926d91ed6e8",
        "trade_id": "85672071",
        "trade_state": "CONFIRMED",
        "cashflow_index": "600000009128",
        "cashflow_status": "QUEUED",
        "cashflow__cashflow_event_type": "New"
    }
]
```

**EXPAND_END**

## Phase three

### Scenario for phase three:

- Cashflow more than 1,000,000 records in database
- Work as cashflow data provider for many system
- Need to return data at second level

### Enhancement part

Consider to change the storage from Postgres to ES or other middleware.

Consider provide independent storage for this scenario.

# Provide Column Name and DB function keyword for API

## Column Name -V1

| Indexed Term | Field Description | Type |
| --- | --- | --- |
| Data_Flow.Data_Publication_Date_Time | The timestamp that the data flow was first initialised. | String |
| Data_Flow.Data_Publication_Id | The Data Publication Id is used to consistently track the data set through systems. For example a data set that needs to be delivered to an external system may need to go through multiple services for enrichment | String |
| Data_Flow.Data_Sender | The sender name of the data flow | String |
| Data_Flow.Data_Source_System | The upstream system name of the data flow | String |
| Data_Flow.Data_Source_System_Country_Code | Actual upstream system country Code | String |
| Data_Flow.Data_Source_System_Domain_Name | Functional domain of upstream system. Examples are FM and Securities etc.. | String |
| Data_Flow.Data_Type | Relevant type name of the data set ;Typical values are TradeData, StaticData, ReferenceData, MarketData and MarginData etc.. | String |
| Cashflow.Cashflow_Id | The unique identifier for the cashflow object, The payment Id will be stored as a transaction UUID and will be generated based on the trace Id generated by Cortex, which is unique and linked to a specific amount. The Id consists out of a hash created from settlement date / currency / period / leg | String |
| Cashflow.Cashflow_Version | Every time a change is made to the payment transaction, the version will be increased. | String |
| Cashflow.Cashflow_Business_Version | Every time a change is made to the payment businesss version i.e materialized | String |
| Cashflow.Cashflow_State | Cashflow or payment state that this is currently in the lifecycle, it can have these values Queued, Pending, Released, Settled, toBeValidated Validated, Failed | String |
| Cashflow.Event_Physical_Status | This field indicates physical status of the position whether it's live or dead | String |
| Cashflow.Cashflow_Event_Type | Type of event New/Withdrawal/Amendment | String |
| Cashflow.Status_Event_Type | cashflow Batch update event used in status notification | String |
| Cashflow.Event_Date | Time when this payment message event is created | String |
| Cashflow.Payment_Payer_Party_Reference | A reference to the party responsible for making the payments defined by the structure. | String |
| Cashflow.Payment_Receiver_Party_Reference | A reference to the party that receives the payments corresponding to this structure. | String |
| Cashflow.Payment_Currency | The payment amount currency which can diff from base currency | String |
| Cashflow.Payment_Amount | The payment amount per one single cash flow | String |
| Cashflow.Payment_Date | The unadjusted payment date for each single cash flow | String |
| Cashflow.Payment_Date_Business_Day_Convention | Business day convention specifies the convention for adjusting a payment date if it would otherwise fall on a day that is not a business day. | String |
| Cashflow.Netting_Id | Netting ID is generated for multiple cashflow that can be settled together using this ID. | String |
| Instrument_Common.CFI_Code | The Classification of Financial Instruments (CFI) Code (ISO 10962) is used to define and describe financial instruments as a uniform set of codes for all market participants. ISO 10962 provides a global standard for these classifications in the form of specific codes. | String |
| Instrument_Common.ISDA_Taxonomy | OTC Deriviatives Product Classification developed by ISDA. The original ISDA OTC Derivatives Taxonomy (“Taxonomy v1.0”) has been in use for cross-jurisdictional reporting for Credit, Rates, Equities, Commodities and FX since 2012. | String |
| Trade_State | Only applicable to new Stella flow. This specifies the trade workflow status. It indicates each state of the trade under one event or across multiple events. | String |
| Trade_Id | SCB Trade Unique Identifer, this id is assigned by SCB transaction processing system and should be unique throughout the life of a trade internally in SCB/ | String |
| Cashflow.Position_Id | Only applicable to new Stella flow. Do Not Use - TP System Specific Field, Please notify TDS3 and FM Data Modelling Teams If any downstreams are going to consume the data of this field | String |
| Parent_Trade_Id | The trade id of the trade(s) upon which this was based, for example the ID of the trade that was submitted for clearing if this is a cleared trade, or of the original trade if this was novated or cancelled and rebooked, or the list of trades that were netted or compressed together in the case of a compression event. The originatingEvent will explain why the trade was created; the existence and number of originatingTradeId elements should correspond to the originatingEvent, and they should be interpreted using that field. If the trade is inside a business event structure (such as a novation or a compression event) this element shuld not be populated; instead the event shoudl be used to represent the other trades. | String |
| Entity.Booking_Entity_SCI_FMID | The SCI FMID (Atlas Id) of booking entity of the transaction. FMID is the most granualr level of identifier of the entity. FMID to SCI_LEID or legal entity is many to one mapping. Booking Entity is the entity for which the organization supporting the trade's processing has booked/recorded the trade. Generally, booking entity will always be one of SCB entities for the transactions booked in SCB systems. | String |
| Entity.Counterparty_SCI_FMID | The SCI FMID (Atlas Id) of counterparty of the transaction. FMID is the most granualr level of identifier of the entity. FMID to SCI_LEID or legal entity is many to one mapping. | String |
| Settlement_Method | The mechanism by which settlement is to be made. The scheme of domain values will include standard mechanisms such as CLS, Fedwire, Chips ABA, Chips UID, SWIFT, CHAPS and DDA. | String |
| Delivery_Method | Specify the delivery method. There is a business rule associated with this field: if deliveryMethod is DVP then you must specify a cashTransfer and a securityTransfer at the same time. It is incorrect to specify DVP and give only a cash transfer instruction. | String |
| Entity.Counterparty_SCI_FMCODE | FM Code is an unique label like the FMID on each counterparty in the bank | String |
| Entity.Counterparty_CIF_Code | Customer Information File (CIF) code of the counterparty, is appllicable when the counterparty is an individual. | String |
| Entity.Counterparty_Source_System_Entity_Id | A unique identifier of counterparty, generated by source system. This field value could vary across source systems. | String |
| Cashflow.Pay_Receive_Indicator | It is to indicate direction of cashflow from SCB's perspective, whether SCB is Payer and Receiver for this cash settlement. | String |
| Cashflow.Payer_Name | Payer Name as defined by Pay_Receive_Indicator. | String |
| Cashflow.Is_Private_Banking_Cashflow | A flag to indicate if a cashflow is generated due to private banking transaction | String |
| Cashflow.Is_Amended_Post_Settlement | This indicates if this version of cashflow is resultant of an update after original cashlfow is settled. | String |
| Cashflow.Payment_Type | A classification of the type of fee or additional payment, e.g. brokerage, upfront fee etc. | String |
| Cashflow.Is_Cashflow_Unnet | A flag is to indicate if this cashflow is due to un net action performed by business users only and not due to trade amendment. | String |
| Cashflow.Transaction_Details | The field is an encoded and obfuscated representation of the cashflow in FMRP STELLA native format. when data is missing from the FMREP STELLA cache (e.g. from a disaster recovery) we can use this field to efficiently re-load the cashflow transaction into our working cache. | String |
| Data_Flow.Unique_Identifier_Message_Id | This unique identifier field will be stamped by origin system, and it should not be modified by any of the intermediatesystem/downstream in the data flow, it can be used for ack/nack response, and data type can be like UUID etc. | String |
| Execution_Date_Time | Trade execution date time | String |
| Entity.General_Ledger_Business_Unit_Name | General Ledger Business Unit (GLBU) name of booking entity, used to describe the booking entity's organization unit involved in the transaction. | String |
| Entity.Booking_Entity_General_Ledger_Business_Unit_Id | General Ledger Business Unit (GLBU) ID of booking entity, used to describe the booking entity's organization unit involved in the transaction. | String |
| Trade_Lake_Valid_From_Date_Time | It's the time an event (eg. event n) became effective/valid in the TP system | String |
| Trade_Lake_Valid_To_Date_Time | This is the time an event (e.g. event n) ceased to remain effective/valid in the TP system. Note that TPs do not capture the end time. So this is actually the time when the subsequent event (n+1) became effective. | String |
| Trade_Lake_Latest_Event_Date_Time | This refer to the time when tradelake SCBML is generated and sent downstream. For non-replayed versions of the trade this is usually same as Trade_Lake_Raw_Event_Date_Time. For replayed trades, this refers to the time when the replayed was processed and scbml sent downstream. | String |
| Trade_Lake_Raw_Event_Date_Time | This refers to the time when tradelake receives messages from upstream TPs in its raw message log. | String |
| Trade_Lake_Transaction_From_Date_Time | TransactionFrom is the time an event was captured in the TradeLake bitemporal index. | String |
| Trade_Lake_Transaction_To_Date_Time | TransactionTo is the time an event was superseded by another event in TradeLake. | String |
| BCS_Parent_Trade_Id | The BCS Stella trade id of the trade(s) upon which this was based, for example the ID of the trade that was submitted for clearing if this is a cleared trade, or of the original trade if this was novated or cancelled and rebooked, or the list of trades that were netted or compressed together in the case of a compression event. The originatingEvent will explain why the trade was created; the existence and number of originatingTradeId elements should correspond to the originatingEvent, and they should be interpreted using that field. If the trade is inside a business event structure (such as a novation or a compression event) this element shuld not be populated; instead the event shoudl be used to represent the other trades. | String |
| BCS_Trade_Id | This is BCS Stella specific Trade Unique Identifer, this id is assigned by BCS transaction processing system and should be unique throughout the life of a trade internally in SCB. | String |
| Trade_Version | This trade version is controlled and assigned by SCB transaction processing system. It should be increased based on trade business event. It is not available in the trades booked by the TPs which don't maintain the versioning. | String |
| Portfolio.Booking_Entity_Trade_Portfolio_Name | This field captures the unique portfolio name in which this transaction is booked. | String |
| Cashflow.Cashflow_Affirmation_Status | Cashflow affirmation status, it is state updated by MO Ratan users , values allowred is only Unaffirmed, Affirmed | String |
| Cashflow.Is_STP_RATAN | Indicates whether cash flow processing/releasing will be Straight Through Processing (STP) or manual | String |
| Cashflow.Is_STP | Indicates whether cash flow processing/releasing will be Straight Through Processing (STP) or manual | String |
| Cashflow.NSTP_Reason | If cash flow processing/releasing is manual then the reason for the same. | String |
| Settlement_Instruction.Account.EBBS_Bridge_Account_Number | Account per entity | String |
| Settlement_Instruction.Account.EBBS_Account_Number | Account per currency | String |
| Settlement_Instruction.Account.Booking_Entity_Correspondent_BIC_code | BIC code of SCB's Correspondent Bank, the bank that will make delivery of the funds on the paying bank's behalf in the country where the payment is to be made. BIC (Business Identifier Code) is an international standard for routing business transactions and identifying business parties. | String |
| Settlement_Instruction.Account.Booking_Entity_Correspondent_Account_Name | The account name of SCB's Correspondent Bank, the correspondent bank that will make delivery of the funds on the paying bank's behalf in the country where the payment is to be made. | String |
| Settlement_Instruction.Account.Booking_Entity_Correspondent_Street_Address | The set of street and building number information that identifies the postal address of SCB's Correspondent Bank, the correspondent bank that will make delivery of the funds on the paying bank's behalf in the country where the payment is to be made, within city. | String |
| Settlement_Instruction.Account.Booking_Entity_Correspondent_City | The city component of a postal address of SCB's Correspondent Bank, the correspondent bank that will make delivery of the funds on the paying bank's behalf in the country where the payment is to be made. | String |
| Settlement_Instruction.Account.Booking_Entity_Correspondent_Account_Number | The account number of SCB's Correspondent Bank, the correspondent bank that will make delivery of the funds on the paying bank's behalf in the country where the payment is to be made. | String |
| Cashflow.Cashflow_Sub_State | Razor sub state that is currently in for a particular cashflow settlement cycle like NSTP Release & Adhoc SSI. | String |
| Cashflow.Cashflow_Sub_State_Updater | Operator ID of the Person who has updated the Cashflow_Sub_State in Razor. | String |
| Cashflow.Cashflow_Sub_State_Type | Type of Cashflow_Sub_State as defined by Razor. | String |
| Cashflow.Prev_Cashflow_Id | Previous cashflow id display on the 'New' & 'Withdrawal' event, referring to the previous cash flow id which is now been issued as 'Withdrwal'. | String |
| Cashflow.Next_Cashflow_Id | New cashflow id field display on the 'Withdrawal' event, referring to the successor cash flow id which event type is 'New' | String |
| Cashflow.Validation_Status | This is used to indicate the different states during business lifecycle and SCBML cashflow state field will be validated against this filed for reconciliation. | String |
| Cashflow.Exception_Reason | For Event Type Negative Acknowledgement, Razor will send out the Murex error message | String |
| Cashflow.FMO_Comment | Comment made by FMO User in Ratan blotter UI. | String |
| Cashflow.FMO_Comment_Updater | FMO User who added the comment for FMO_Comment. | String |
| Cashflow.FMO_Comment_Timestamp | The Timestamp when FMO_Comment was made. | String |
| Cashflow.STP_Cutoff_Date_Time | The cut off date&time by when the 'Queued' status cash flow will be held in Ratan and not STP to Razor. | String |
| Cashflow.Netting_Cuttoff_Date | The cut off date for netting/un-netting action. | String |
| Entity.Booking_Entity_SCI_FMCODE | Display name for booking entity maintained in SCI. | String |
| Cashflow.Cashflow_Audit_Version | Tracking the changes captured in user manual Maker/Checker actions and other backend enrichment/exception results | String |
| Cashflow.Payment_Cutoff_Time | This is the time by which a payment needs to be successfully initiated for same-day execution.If initiated before cut-off, funds will be debited from your account on same-day. | String |
| Settlement_Instruction.Nostro_Swift_Message_Type | Indicates the SWIFT message type to be used for sending Settlement Instruction. | String |
| Cashflow.Minor_Version_Description | Type of event description that caused new RATAN Minor Version | String |
| Cashflow.Bypass_Workflow_Indicator | This indicates to process this cashflow for settlement even though the previous version of this cashflow is suppressed. | String |
| Cashflow.Cashflow_Minor_Version | RATAN Minor Version | String |
| Settlement_Instruction.SSI_Unique_Id | Unique identifier for the SSI with which a SSI is identified across systems | String |
| Settlement_Instruction.SSI_Source | Describes if the SSI is from the Alert message(STP) or a Manual input. Possible values Alert, Manual,Import,Copy Alert - implies SSI is from DTCC Manual -implies SSI is manually entered in SSI+ Import - Implies the SSI is import from a file import inot SSI+ | String |
| Settlement_Instruction.SSI_Priority | Primary or secondary SSI | String |
| Settlement_Instruction.Swift_Message_Type | Indicates the SWIFT message type to be used for sending Settlement Instruction. | String |
| Settlement_Instruction.Account.SCB_Nostro_Account_Number | SCB Nostro account number, associated with this SSI. | String |
| Settlement_Instruction.Account.SCB_Nostro_Account_Type | SCB Nostro account type, associated with this SSI. Possible values: NOS - Indicates the main account Over the acount - Indicates the secondary account | String |
| Settlement_Instruction.Account.Beneficiary_BIC_code | BIC code of beneficiary party of settlement instruction. BIC (Business Identifier Code) is an international standard for routing business transactions and identifying business parties. | String |
| Settlement_Instruction.Account.Beneficiary_Account_Name | The account name of beneficiary | String |
| Settlement_Instruction.Account.Beneficiary_Account_Name_2 | SecondThe account name of beneficiary. If length is more than 35 characters, then upto first 35 characters are captured in Beneficiary_Account_Name field and remaining are captured in this field. | String |
| Settlement_Instruction.Account.Beneficiary_Street_Address | The set of street and building number information that identifies the postal address of beneficiary, within a city. | String |
| Settlement_Instruction.Account.Beneficiary_City | The city component of a postal address of beneficiary. | String |
| Settlement_Instruction.Account.Beneficiary_Account_Number | The account number of beneficiary | String |
| Settlement_Instruction.Account.Intermediary_BIC_code | BIC code of Intermediary, through which payment will be made by the correspondent bank to the ultimate beneficiary of the funds. BIC (Business Identifier Code) is an international standard for routing business transactions and identifying business parties. | String |
| Settlement_Instruction.Account.Intermediary_Account_Name | The account name of Intermediary, through which payment will be made by the correspondent bank to the ultimate beneficiary of the funds. | String |
| Settlement_Instruction.Account.Intermediary_Street_Address | The set of street and building number information that identifies the postal address of Intermediary, through which payment will be made by the correspondent bank to the ultimate beneficiary of the funds, within city. | String |
| Settlement_Instruction.Account.Intermediary_City | The city component of a postal address of Intermediary, through which payment will be made by the correspondent bank to the ultimate beneficiary of the funds. | String |
| Settlement_Instruction.Account.Intermediary_Account_Number | The account number of Intermediary, through which payment will be made by the correspondent bank to the ultimate beneficiary of the funds | String |
| Settlement_Instruction.Account.Beneficiary_Bank_BIC_code | BIC code of Institution Bank, the bank that acts for the ultimate beneficiary of the funds in receiving payments. BIC (Business Identifier Code) is an international standard for routing business transactions and identifying business parties. | String |
| Settlement_Instruction.Account.Beneficiary_Bank_Account_Name | The account name of Institution Bank, the bank that acts for the ultimate beneficiary of the funds in receiving payments. | String |
| Settlement_Instruction.Account.Beneficiary_Bank_Street_Address | The set of street and building number information that identifies the postal address of Institution Bank, the bank that acts for the ultimate beneficiary of the funds in receiving payments, within city. | String |
| Settlement_Instruction.Account.Beneficiary_Bank_City | The city component of a postal address of Institution Bank, the bank that acts for the ultimate beneficiary of the funds in receiving payments.. | String |
| Settlement_Instruction.Account.Beneficiary_Bank_Account_Number | The account number of Institution Bank, the bank that acts for the ultimate beneficiary of the funds in receiving payments. | String |
| Settlement_Instruction.Account.Beneficiary_Correspondent_BIC_code | BIC code of beneficiary's Correspondent Bank, the bank that will make delivery of the funds on the paying bank's behalf in the country where the payment is to be made. BIC (Business Identifier Code) is an international standard for routing business transactions and identifying business parties. | String |
| Settlement_Instruction.Account.Beneficiary_Correspondent_Account_Name | The account name of beneficiary's Correspondent Bank, the correspondent bank that will make delivery of the funds on the paying bank's behalf in the country where the payment is to be made. | String |
| Settlement_Instruction.Account.Beneficiary_Correspondent_Street_Address | The set of street and building number information that identifies the postal address of beneficiary's Correspondent Bank, the correspondent bank that will make delivery of the funds on the paying bank's behalf in the country where the payment is to be made, within city. | String |
| Settlement_Instruction.Account.Beneficiary_Correspondent_City | The city component of a postal address of beneficiary's Correspondent Bank, the correspondent bank that will make delivery of the funds on the paying bank's behalf in the country where the payment is to be made. | String |
| Settlement_Instruction.Account.Beneficiary_Correspondent_Account_Number | The account number of beneficiary's Correspondent Bank, the correspondent bank that will make delivery of the funds on the paying bank's behalf in the country where the payment is to be made. | String |
| Settlement_Instruction.Account.Ordering_Customer_BIC_Code | BIC code of Ordering Customer, the customer ordering the transaction. BIC (Business Identifier Code) is an international standard for routing business transactions and identifying business parties. | String |
| Settlement_Instruction.Account.Ordering_Customer_Account_Name | The account name of Ordering Customer, the customer ordering the transaction. | String |
| Settlement_Instruction.Account.Ordering_Customer_Street_Address | The set of street and building number information that identifies the postal address of Ordering Customer, the customer ordering the transaction. | String |
| Settlement_Instruction.Account.Ordering_Customer_City | The city component of a postal address of Ordering Customer, the customer ordering the transaction. | String |
| Settlement_Instruction.Account.Ordering_Customer_Account_Number | The account number of Ordering Customer, the customer ordering the transaction. | String |
| Settlement_Instruction.Remittance_Information_1 | This field specifies either the details of the individual transaction or a reference to another message containing the details which are to be transmitted to the beneficiary customer. Typically, provides additional details of the fund name of the counterparty. This field, which may contain a maximum of four lines of 35 characters | String |
| Settlement_Instruction.Remittance_Information_2 | This field specifies either the details of the individual transaction or a reference to another message containing the details which are to be transmitted to the beneficiary customer. Typically, provides additional details of the fund name of the counterparty. This field, which may contain a maximum of four lines of 35 characters | String |
| Settlement_Instruction.Remittance_Information_3 | This field specifies either the details of the individual transaction or a reference to another message containing the details which are to be transmitted to the beneficiary customer. Typically, provides additional details of the fund name of the counterparty. This field, which may contain a maximum of four lines of 35 characters | String |
| Settlement_Instruction.Remittance_Information_4 | This field specifies either the details of the individual transaction or a reference to another message containing the details which are to be transmitted to the beneficiary customer. Typically, provides additional details of the fund name of the counterparty. This field, which may contain a maximum of four lines of 35 characters | String |
| Settlement_Instruction.Sender_To_Receiver_Information_1 | To specify additional information to one of the parties involved in the transaction. Typically, provides additional details of the fund name of the counterparty. This field, which may contain a maximum of six lines of 35 characters | String |
| Settlement_Instruction.Sender_To_Receiver_Information_2 | To specify additional information to one of the parties involved in the transaction. Typically, provides additional details of the fund name of the counterparty. This field, which may contain a maximum of six lines of 35 characters | String |
| Settlement_Instruction.Sender_To_Receiver_Information_3 | To specify additional information to one of the parties involved in the transaction. Typically, provides additional details of the fund name of the counterparty. This field, which may contain a maximum of six lines of 35 characters | String |
| Settlement_Instruction.Sender_To_Receiver_Information_4 | To specify additional information to one of the parties involved in the transaction. Typically, provides additional details of the fund name of the counterparty. This field, which may contain a maximum of six lines of 35 characters | String |
| Settlement_Instruction.Sender_To_Receiver_Information_5 | To specify additional information to one of the parties involved in the transaction. Typically, provides additional details of the fund name of the counterparty. This field, which may contain a maximum of six lines of 35 characters | String |
| Settlement_Instruction.Sender_To_Receiver_Information_6 | To specify additional information to one of the parties involved in the transaction. Typically, provides additional details of the fund name of the counterparty. This field, which may contain a maximum of six lines of 35 characters | String |
| Settlement_Instruction.Account.Counterparty_CMS_Account_Number | CentralManagementSystem account number, if the client has CMS account directly with SCB. | String |
| Settlement_Instruction.Is_Third_Party_Payment | Indicates if the payment is to be made to a third party other than the counterparty beneficiary (possible values true / false) . | String |
| Settlement_Instruction.Swift_Payment_Method | Indicates the Swift payment method (Cover vs Serial payment) to be used, as per client's requirement. | String |
| Settlement_Instruction.Charge_Bearer | Indicates which party to be charged for additional cover payment charges. Below specific codes are used to indicate the charge bearer of settlement. BEN (BENeficiary) – Payee (recipient of the payment) will incur all of the payment transaction fees. OUR – Payer (sender of the payment) will bear all of the payment transaction fees. SHA (SHAred) – Payer (sender of the payment) will pay all fees charged by the sending bank, and Payee (recipient of the payment) will pay all fees charged by the receiving bank. | String |
| Instrument_Common.Source_System_Instrument_Sub_Type | The instrument sub-classification as defined by the TP. Values will be specific to the TP and will not be consistent across TPs. | String |
| Portfolio.Booking_Entity_Trade_Portfolio_Unique_Name | This field captures the unique portfolio name across TP systems in which this transaction is booked. | String |
| Entity.Person.Coverage_Marketer_PSID | The people soft Id (PSID) of the individual/person, who is the Coverage Marketer of the transaction. | String |
| Entity.Person.Event_Coverage_Marketer_PSID | The people soft Id (PSID) of the individual/person, who is the Coverage Marketer of the transaction. | String |
| Entity.Person.Execution_Marketer_PSID | The people soft Id (PSID) of the individual/person, who is the Execution Marketer of the transaction. Execution Marketer is the person, within the investment firm, who is responsible for the execution of transaction. | String |
| Entity.Person.Event_Execution_Marketer_PSID | The people soft Id (PSID) of the individual/person, who is the Execution Marketer of the transaction. Execution Marketer is the person, within the investment firm, who is responsible for the execution of transaction. | String |
| Entity.Person.Booking_Marketer_PSID | The people soft Id (PSID) of the individual/person, who is the Booking Marketer of the transaction. Booking Marketer is the person who is responsible for booking the transaction in the system. | String |
| Entity.Person.Event_Booking_Marketer_PSID | The people soft Id (PSID) of the individual/person, who is the Booking Marketer of the transaction. Booking Marketer is the person who is responsible for booking the transaction in the system. | String |
| Entity.Person.Trader_PSID | The people soft Id (PSID) of the trader. Trader is the person who executed the trade. | String |
| Entity.Person.Event_Trader_PSID | The people soft Id (PSID) of the trader. Trader is the person who executed the trade. | String |
| Trade.Event_Physical_Status | This field indicates physical status of the position whether it's live or dead | String |
| Resultant_Position_Id | An ID which is assigned for new booking that is generated by existing position due to business event and to track the new remaining position. | String |
| Trade_Original_Source_System_Name | Indication of name or Id for the trade source system/trading venue/intermediaries/etc. | String |
| Cashflow.Is_Payment_Intent_To_Settle | Specifies whether given payment is anticipated to be settled | String |
| Cashflow.Action_Type | This defines the transaction typology | String |
| | | String |
| Cashflow.Cashflow_Event_Reason | Indicator for the cashflow 'Reversal'/'Rebook'. | String |
| Settlement_Instruction.Value_Date | Swift Value date, which settlement ops manually key in when they fix the 'Back Value Date' exceptions. This field would be enriched to cashflow SCBML and sent to Razor. | String |
| Settlement_Instruction.Value_Date_Business_Day_Convention | Business day convention specifies the convention for adjusting a value date if it would otherwise fall on a day that is not a business day. | String |
| Instrument_Common.Financial_Instrument_Code | The Classification of Financial Instruments is used to define and describe financial instruments as a set of codes for all market participants. It can be applicable for both Standard CFI and Non Standard CFI codes | String |
| Cashflow.Cashflow_Major_Version | Major version is the only version that increments when Book, Update, Cancel or Undo has been performed. | String |
| Cashflow.Cashflow_SubEvent_Type | TP System Business Event Type | String |
| Cashflow_Sequence | This field will identify the number of cashflows that are present under a trade along with their sequence. | String |
| Effective_Date_Time | This refers to the timestamp when the trade event was effective in the source system. This is usually the audit timestamp in the source system | String |
| Entity.Booking_Entity_Country_ISO_Code | "The ISO country code identifies the domicile country in which the booking entity, involved in the transaction, is operating. Domicile country refers to the country in which business operations of the entity are being performed. Unlike Incorporation country, different branches could have different domiciles, depending on the location in which ther are operating. For example, SCB Singapore branch would have Domicile of 'SG', where as London branch's domicile is 'GB'. Booking Entity is the entity for which the organization supporting the trade's processing has booked/recorded the trade. Generally, booking entity will always be one of SCB entities for the transactions booked in SCB systems." | String |
| TP_System_Name | Captures the name of the system which processes the trades throughout trade lifecycle. | String |
| Trade_Purpose | To define the purpose of trade booking | String |

## Column Name -V2

The SQL must has column Cashflow.Cashflow_Id  when query the Cashflow.Audit

| **Indexed Term** | **Field Description** | **Type** | **Data structure** | **Sample** | **Note** |
| --- | --- | --- | --- | --- | --- |
| Cashflow.Audit | - Number of cashflow manual touchpoints - Detail of cashflow all exceptions on the cashflows - History of cashflow touchpoints is provided (time, user and action) | Json | "Cashflow.Audit": { "touchPointHistory": [Json Array] , "exceptionList": [Json Array] } | "Cashflow.Audit": { "touchPointHistory": [ { "time": "2023-11-21 05:02:08.968011", "user": "1129381", "action": "Materialize" } ], "exceptionList": [ { "exceptionCode": "Missing Nostro", "businessFlow": "SETTLEMENT", "sourceSystem": "RATAN", "exceptionType": "BUSINESS", "description": "MISSING_NOSTRO_ERROR", "status": "PENDING_OPERATOR" } ] } | |
| touchPointHistory | sub key of Cashflow.Audit History of cashflow touchpoints is provided (time, user and action) | Json Array | "touchPointHistory": [ { "time": "String", "user": "String", "action": "String" } ] | "touchPointHistory": [ { "time": "2023-11-21 05:49:41.362789", "user": "1639796", "action": "IsNstpChecker" } ] | |
| exceptionList | sub key of Cashflow.Audit Detail of cashflow all exceptions on the cashflows | Json Array | "exceptionList": [ { "exceptionCode": "String", "businessFlow": "String", "sourceSystem": "String", "exceptionType": "String", "description": "String ", "status": "String" } ] | "exceptionList": [ { "exceptionCode": "Pending Affirmation", "businessFlow": "SETTLEMENT", "sourceSystem": "RATAN-RULE-SERVICE", "exceptionType": "BUSINESS", "description": "Cashflow and trade are not confirmed or affirmed", "status": "CLOSED" }, { "exceptionCode": "Missing Vostro", "businessFlow": "SETTLEMENT", "sourceSystem": "RATAN", "exceptionType": "BUSINESS", "description": "MISSING_VOSTRO_ERROR", "status": "CLOSED" } ] | |

## DB function keyword

So far,  about the version not support DB function keyword at select and where part but limit.

| Function keyword | Note |
| --- | --- |
| limit | |
| count | |

# How to set up EMS2 for FAMM auth

Need to apply the role on EMS2  for Ratan Entity choose RATAN_FUNC and Role choose SYS_RO

## For Prod ENV:

Raise SRM request "Get, modify, or remove privilege and shared application identity (ID)".

Sample Request [My Request - RITM5083294 - Service Portal](https://scbnow01.service-now.com/itsp?id=ticket&table=sc_req_item&sys_id=33da9bc4ebd98354c608fa7c8ad0cde3&view=sp).

![image-2026-6-16_10-53-50.png](attachments/image-2026-6-16_10-53-50.png)

![image-2026-6-16_10-54-20.png](attachments/image-2026-6-16_10-54-20.png)

![image-2026-6-16_10-54-47.png](attachments/image-2026-6-16_10-54-47.png)

![image-2026-6-16_10-56-5.png](attachments/image-2026-6-16_10-56-5.png)

**EXPAND: Deprecated**

**Instruction: **

So please raise a bulk request in [ServiceNow](https://scbnow01.service-now.com/itsp?id=sp_sc_cat_item&sys_id=e61d080d8783a1905c7664290cbb35b8) system to apply user and role on EMS2.  Ratan api should be accessible after request is processed.

[https://scbnow01.service-now.com/itsp?id=sp_sc_cat_item&sys_id=e61d080d8783a1905c7664290cbb35b8](https://scbnow01.service-now.com/itsp?id=sp_sc_cat_item&sys_id=e61d080d8783a1905c7664290cbb35b8)

**Sample attachment:**

![requestRole.png](attachments/requestRole.png)

**EXPAND_END**

## For DEV and UAT ENV:

Testing ENV login:  [https://uklvauems01a.uk.standardchartered.com:16443/ems2/http/web/user/manage](https://uklvauems01a.uk.standardchartered.com:16443/ems2/http/web/user/manage)

Follow the diagram below to operate, please reach out to SABRE and Raise bulk request.

![image2023-8-31_16-29-55.png](attachments/image2023-8-31_16-29-55.png)

![image2023-8-31_16-18-4.png](attachments/image2023-8-31_16-18-4.png)

![image2023-8-31_16-24-43.png](attachments/image2023-8-31_16-24-43.png)

![image2023-8-31_16-25-58.png](attachments/image2023-8-31_16-25-58.png)

# How to set up EMS2 for Data Entitlement

## For Prod ENV:

Bulk-Request:  need to provide 10+ bank Ids and the mapping role and then raise a bulk request in ServiceNow system.

## For DEV and UAT ENV:

![image2023-8-31_16-29-55.png](attachments/image2023-8-31_16-29-55.png)

choose RATAN_DATA_ENTIELEMENT and Add Role

![image2023-9-1_11-26-26.png](attachments/image2023-9-1_11-26-26.png)

binding user with RATAN_DATA_ENTIELEMENT Role（Global，GBS，Onshore）

![image2023-10-18_11-29-18.png](attachments/image2023-10-18_11-29-18.png)

![image2023-10-18_11-30-47.png](attachments/image2023-10-18_11-30-47.png)

![image2023-10-18_11-32-16.png](attachments/image2023-10-18_11-32-16.png)

# Query Sample

| Query Condition Sample | Data |
| --- | --- |
| Request | { "queryCondition":"Select Cashflow.Audit,Data_Flow.Data_Source_System,Data_Flow.Data_Source_System_Country_Code,Data_Flow.Data_Source_System_Domain_Name,Data_Flow.Data_Type,Cashflow.Cashflow_Id,Cashflow.Cashflow_Version,Cashflow.Cashflow_Business_Version,Cashflow.Cashflow_State,Cashflow.Event_Physical_Status,Cashflow.Cashflow_Event_Type,Cashflow.Status_Event_Type,Cashflow.Event_Date,Cashflow.Payment_Payer_Party_Reference,Cashflow.Payment_Receiver_Party_Reference,Cashflow.Payment_Currency,Cashflow.Payment_Amount,Cashflow.Payment_Date,Cashflow.Payment_Date_Business_Day_Convention,Cashflow.Netting_Id,Instrument_Common.CFI_Code,Instrument_Common.ISDA_Taxonomy,Trade_State,Trade_Id,Cashflow.Position_Id,Parent_Trade_Id,Entity.Booking_Entity_SCI_FMID,Entity.Counterparty_SCI_FMID,Settlement_Method,Delivery_Method,Entity.Counterparty_SCI_FMCODE,Entity.Counterparty_CIF_Code,Entity.Counterparty_Source_System_Entity_Id,Cashflow.Pay_Receive_Indicator,Cashflow.Payer_Name,Cashflow.Is_Private_Banking_Cashflow,Cashflow.Is_Amended_Post_Settlement,Cashflow.Payment_Type,Cashflow.Is_Cashflow_Unnet,Cashflow.Transaction_Details,Data_Flow.Unique_Identifier_Message_Id,Execution_Date_Time,Entity.General_Ledger_Business_Unit_Name,Entity.Booking_Entity_General_Ledger_Business_Unit_Id,Trade_Lake_Valid_From_Date_Time,Trade_Lake_Valid_To_Date_Time,Trade_Lake_Latest_Event_Date_Time,Trade_Lake_Raw_Event_Date_Time,Trade_Lake_Transaction_From_Date_Time,Trade_Lake_Transaction_To_Date_Time,BCS_Parent_Trade_Id,BCS_Trade_Id,Trade_Version,Portfolio.Booking_Entity_Trade_Portfolio_Name,Cashflow.Cashflow_Affirmation_Status,Cashflow.Is_STP_RATAN,Cashflow.Is_STP,Cashflow.NSTP_Reason,Settlement_Instruction.Account.EBBS_Bridge_Account_Number,Settlement_Instruction.Account.EBBS_Account_Number,Settlement_Instruction.Account.Booking_Entity_Correspondent_BIC_code,Settlement_Instruction.Account.Booking_Entity_Correspondent_Account_Name,Settlement_Instruction.Account.Booking_Entity_Correspondent_Street_Address,Settlement_Instruction.Account.Booking_Entity_Correspondent_City,Settlement_Instruction.Account.Booking_Entity_Correspondent_Account_Number,Cashflow.Cashflow_Sub_State,Cashflow.Cashflow_Sub_State_Updater,Cashflow.Cashflow_Sub_State_Type,Cashflow.Prev_Cashflow_Id,Cashflow.Next_Cashflow_Id,Cashflow.Validation_Status,Cashflow.Exception_Reason,Cashflow.FMO_Comment,Cashflow.FMO_Comment_Updater,Cashflow.FMO_Comment_Timestamp,Cashflow.STP_Cutoff_Date_Time,Cashflow.Netting_Cuttoff_Date,Entity.Booking_Entity_SCI_FMCODE,Cashflow.Cashflow_Audit_Version,Cashflow.Payment_Cutoff_Time,Settlement_Instruction.Nostro_Swift_Message_Type,Cashflow.Minor_Version_Description,Cashflow.Bypass_Workflow_Indicator,Cashflow.Cashflow_Minor_Version,Settlement_Instruction.SSI_Unique_Id,Settlement_Instruction.SSI_Source,Settlement_Instruction.SSI_Priority,Settlement_Instruction.Swift_Message_Type,Settlement_Instruction.Account.SCB_Nostro_Account_Number,Settlement_Instruction.Account.SCB_Nostro_Account_Type,Settlement_Instruction.Account.Beneficiary_BIC_code,Settlement_Instruction.Account.Beneficiary_Account_Name,Settlement_Instruction.Account.Beneficiary_Account_Name_2,Settlement_Instruction.Account.Beneficiary_Street_Address,Settlement_Instruction.Account.Beneficiary_City,Settlement_Instruction.Account.Beneficiary_Account_Number,Settlement_Instruction.Account.Intermediary_BIC_code,Settlement_Instruction.Account.Intermediary_Account_Name,Settlement_Instruction.Account.Intermediary_Street_Address,Settlement_Instruction.Account.Intermediary_City,Settlement_Instruction.Account.Intermediary_Account_Number,Settlement_Instruction.Account.Beneficiary_Bank_BIC_code,Settlement_Instruction.Account.Beneficiary_Bank_Account_Name,Settlement_Instruction.Account.Beneficiary_Bank_Street_Address,Settlement_Instruction.Account.Beneficiary_Bank_City,Settlement_Instruction.Account.Beneficiary_Bank_Account_Number,Settlement_Instruction.Account.Beneficiary_Correspondent_BIC_code,Settlement_Instruction.Account.Beneficiary_Correspondent_Account_Name,Settlement_Instruction.Account.Beneficiary_Correspondent_Street_Address,Settlement_Instruction.Account.Beneficiary_Correspondent_City,Settlement_Instruction.Account.Beneficiary_Correspondent_Account_Number,Settlement_Instruction.Account.Ordering_Customer_BIC_Code,Settlement_Instruction.Account.Ordering_Customer_Account_Name,Settlement_Instruction.Account.Ordering_Customer_Street_Address,Settlement_Instruction.Account.Ordering_Customer_City,Settlement_Instruction.Account.Ordering_Customer_Account_Number,Settlement_Instruction.Remittance_Information_1,Settlement_Instruction.Remittance_Information_2,Settlement_Instruction.Remittance_Information_3,Settlement_Instruction.Remittance_Information_4,Settlement_Instruction.Sender_To_Receiver_Information_1,Settlement_Instruction.Sender_To_Receiver_Information_2,Settlement_Instruction.Sender_To_Receiver_Information_3,Settlement_Instruction.Sender_To_Receiver_Information_4,Settlement_Instruction.Sender_To_Receiver_Information_5,Settlement_Instruction.Sender_To_Receiver_Information_6,Settlement_Instruction.Account.Counterparty_CMS_Account_Number,Settlement_Instruction.Is_Third_Party_Payment,Settlement_Instruction.Swift_Payment_Method,Settlement_Instruction.Charge_Bearer,Instrument_Common.Source_System_Instrument_Sub_Type,Portfolio.Booking_Entity_Trade_Portfolio_Unique_Name,Entity.Person.Coverage_Marketer_PSID,Entity.Person.Event_Coverage_Marketer_PSID,Entity.Person.Execution_Marketer_PSID,Entity.Person.Event_Execution_Marketer_PSID,Entity.Person.Booking_Marketer_PSID,Entity.Person.Event_Booking_Marketer_PSID,Entity.Person.Trader_PSID,Entity.Person.Event_Trader_PSID,Trade.Event_Physical_Status,Resultant_Position_Id,Trade_Original_Source_System_Name,Cashflow.Is_Payment_Intent_To_Settle,Cashflow.Action_Type,Cashflow.Cashflow_Event_Reason,Settlement_Instruction.Value_Date,Settlement_Instruction.Value_Date_Business_Day_Convention,Instrument_Common.Financial_Instrument_Code,Cashflow.Cashflow_Major_Version,Cashflow.Cashflow_SubEvent_Type,Cashflow_Sequence,Effective_Date_Time,Entity.Booking_Entity_Country_ISO_Code,TP_System_Name,Trade_Purpose from cash_settlement_query_cn.cashflow_data LIMIT 1 OFFSET 0" } |
| Response | [ { "Settlement_Instruction.Account.Ordering_Customer_Account_Name": "", "Settlement_Instruction.Account.Intermediary_Account_Number": "", "Settlement_Instruction.Account.Beneficiary_Correspondent_City": "", "Settlement_Instruction.Swift_Payment_Method": "", "Settlement_Instruction.Account.Intermediary_Account_Name": "", "Settlement_Instruction.Sender_To_Receiver_Information_2": "", "Settlement_Instruction.Sender_To_Receiver_Information_1": "", "Cashflow.Cashflow_Event_Reason": "", "Cashflow.Cashflow_Event_Type": "New", "Instrument_Common.Source_System_Instrument_Sub_Type": "", "Cashflow.Cashflow_Sub_State_Updater": "System", "Cashflow.Netting_Id": null, "Trade_Lake_Raw_Event_Date_Time": null, "Cashflow.Cashflow_Business_Version": "0", "Data_Flow.Data_Source_System": "Stella", "Trade_Purpose": null, "Cashflow.Is_Private_Banking_Cashflow": "false", "TP_System_Name": null, "Entity.Person.Event_Trader_PSID": null, "Cashflow.Exception_Reason": null, "Settlement_Instruction.SSI_Priority": "", "Settlement_Instruction.Account.Beneficiary_Correspondent_BIC_code": "", "Settlement_Instruction.Account.Beneficiary_Correspondent_Account_Number": "", "Trade_Lake_Transaction_From_Date_Time": "2024-02-19 16:18:36.373", "Cashflow.Payment_Cutoff_Time": "2024-02-20 10:00:00", "Cashflow.Payment_Receiver_Party_Reference": "party2", "Cashflow.Cashflow_Sub_State": "Pending Operator", "Entity.Booking_Entity_General_Ledger_Business_Unit_Id": "622", "BCS_Parent_Trade_Id": "", "Cashflow.Prev_Cashflow_Id": null, "Trade_Original_Source_System_Name": "Blade", "Settlement_Instruction.Account.Beneficiary_Bank_Account_Number": "", "Entity.Counterparty_CIF_Code": null, "Cashflow.Is_Amended_Post_Settlement": "null", "Cashflow.Cashflow_Affirmation_Status": "Unaffirmed", "Settlement_Instruction.Account.Booking_Entity_Correspondent_City": "FRANKFURT", "Entity.Counterparty_SCI_FMID": "401024052", "Data_Flow.Data_Type": "CashflowData", "Entity.Counterparty_Source_System_Entity_Id": "", "Cashflow.Is_STP": "false", "Entity.Person.Event_Booking_Marketer_PSID": null, "Cashflow.Payment_Payer_Party_Reference": "party1", "Cashflow.Is_STP_RATAN": "false", "Portfolio.Booking_Entity_Trade_Portfolio_Unique_Name": "SABRE||CNO_SWP_ASX_IR_STL", "Settlement_Instruction.Account.Beneficiary_Bank_Street_Address": "", "Effective_Date_Time": null, "Cashflow.STP_Cutoff_Date_Time": null, "Cashflow.Validation_Status": null, "Settlement_Instruction.Charge_Bearer": "", "Settlement_Instruction.Account.Beneficiary_Bank_Account_Name": "", "Cashflow.Netting_Cuttoff_Date": null, "Settlement_Instruction.Account.Beneficiary_Correspondent_Account_Name": "", "Entity.Person.Execution_Marketer_PSID": "", "Data_Flow.Unique_Identifier_Message_Id": null, "Cashflow.Cashflow_Minor_Version": "3", "Settlement_Instruction.Account.EBBS_Bridge_Account_Number": "100004487036636007", "Delivery_Method": "", "Settlement_Instruction.Account.EBBS_Account_Number": "100004487036636007", "Cashflow.FMO_Comment_Updater": null, "Trade_Lake_Valid_From_Date_Time": "2024-02-19 16:17:55", "Settlement_Instruction.Account.Booking_Entity_Correspondent_Account_Name": "STANDARD CHARTERED BANK AG FRA", "Settlement_Instruction.Account.Beneficiary_Bank_City": "", "Cashflow.Payment_Date": "2024-02-21", "Settlement_Instruction.Is_Third_Party_Payment": "", "Instrument_Common.ISDA_Taxonomy": "InterestRate:CrossCurrency:FixedFloat", "Cashflow.Event_Physical_Status": null, "Execution_Date_Time": "2024-02-19 16:18:33", "Trade_Lake_Valid_To_Date_Time": "9999-12-31 00:00:00", "Cashflow.Cashflow_Sub_State_Type": "Pending Exception", "Parent_Trade_Id": "4333265071", "Cashflow.Pay_Receive_Indicator": "Pay", "Entity.Counterparty_SCI_FMCODE": "TEST 2381", "Entity.Person.Trader_PSID": "", "Cashflow.Payer_Name": "", "Cashflow.NSTP_Reason": "", "Resultant_Position_Id": "4333265071", "Settlement_Instruction.Account.Intermediary_Street_Address": "", "Entity.Person.Event_Execution_Marketer_PSID": null, "Cashflow.Cashflow_SubEvent_Type": null, "Cashflow.Payment_Currency": "EUR", "Entity.Person.Coverage_Marketer_PSID": "", "Settlement_Instruction.Value_Date_Business_Day_Convention": null, "Settlement_Instruction.SSI_Source": "", "Cashflow.Cashflow_Major_Version": null, "Settlement_Instruction.Account.Beneficiary_City": "", "Trade_Id": "4333265071", "Cashflow.Transaction_Details": "H4sIAAAAAAAA/7VXW0/jRhT+Kyurj07qexKkfQiBLbABsgkLWyGExp7jMGB7vDM2m6jqf++Z8Z2llFYqQiI5cy7ffOc23BoRT8cyCseShALGcSogH1OeEpaNrwTJJIkKxjPD/MMoS0aNA8OyPNd1ncC3Jo5hGs8gpFI4sEwjJwKyom92cPtWgK/o8bq27wIA8aZhBHREqWePPHsyHU1pOBu5ENAgdPyYOsPAf96ZGCUrBAY9VR5agLbRnSCs6Ill2+seYNgVIDKS4BkFbXq2OQ/8m283n92rC+9yeXa9+TLvOdkUpABUW7JnQDEpKSuuWIqiW8dyPNMx7ZlpB6Y9NV3XdFzfmgbezEeAEMeAnDzDq+oT01dKkpcigs1eFpBilMMEYWGYH1w8xQn/UUd/k1OpdMY3AwvktnFxQdL3eaAQs4ypJLbOtC36UlmamEamXRkYIqNE0A8LIh8+bKAoEkixDAyVFpbN31MIP4Wct1WngjldtJXgj8hjjxSpfD+SZzIuC5aMTxAFgjDMW+MlIPPvsd7dKbTy3fz2oLYUK6S20yFdX54dL66Oj/4PrAptWEqWgZTHzyjVxavLGE1BSdZApCI+K5MEu4UkjCLQSuUgJokEvHDrtd8VGUqxUZTLyngruJQXKAU6aO7aS4QAdX1UdmuIAedABI15TvYgVkQUe8SYq7+qLwVEgO0wPFCNXSiIR1Um6i5xbLzv95JkBVO6NYcpKR7Gh2x7BBFLSWKYSqu70isuusNzKB54e0EdsuntfuIiXmY4IjS2arRYNvqzfAUUajj1LbkoYp4wXrWYsbi4vN/crO7nm2/3p+v7zdUSTXLBIrja5y03oeBPIJpvKRFPUHTfSwliwVOd9p5II3EsK/BnLjqNd2uNvFKIdyvCWg+Yy3mqLvEGa5b+GVt6jKY5KVjIkv7Nnkmb65xLXfbDOavYUFVgHBSiBJ1xhbm6qHGqOoUkx7vogWRb+PUT2wFtEn3BlTvE0dwPlVeKpZYTTlk8XxAsqOQFF/2jRkZBQ+Sig6+8LSJVY8df10a/CvpSjWZJws6VJAnI0ww56cgFkM1nLtiWZUSVfLs/qhPRdMCqx1Z1RIqCRA9AV6/yqPoiFjzdLA7Plx3nuLjIFn5WxUpJ+wjqCq4iNV15TvJcVVR/8Cx4koBuYvnL10zTyEiYAOriJNOjMArTpNceURXemrkh2JTCdBLaAfGCYDZBQL4zoWFAIkv1dfy9qs+JHT7wbQTWnmfPWGc4sDKaVH4mU99XkiJcdZerWVeRm2WtlV0ydabxzB1NfdsbeaEdjkgQ05EPs8CZzNwYHG9kjxQjKic9tqu+Vg7PySMX7ZCzB0cs6x1ZzRF8L6shZtj3yjXLem+FluS82K+GjV/3NecK/7EeEXVVGYuT04v5h5NLlToqd0uWPVVJdTCnKExYDIt9lIAe6SqbJVabcZlDpgFI7K6q/t9cUaedYveq8ujMjn0HRtSlDpLo4avKisjICYIAgDiebfkvnnNqGPBMLZfWoXxfHa1xdfF0HkW4npZMqg13d1fXkezthzevcaT/XIZq33c29Y3afCm6VcH2nmJN23NaRv/E1arWal4arV09xVfVJDtQqYkwNZhTvRZEAbvatp5yCy0bn67x9xP23VgXimJjXDup0u4MzOqpsN0K2JJqq/YS3Xsgmw/7nJvDfWRWG8gcrB5z+NLsnCsog5296k/pdr6pr+2MI0nCi6rk8A3G5KId8tXrrgHaL/1O+tNLoDs60Y5eSs96LxbY5Uzsj3oTDTdXKfC+fVn3KKgbUmdhUB11Q6vrHxIJgaeS9eg655+tT67323z+ZU4Xm1z+/uV4rn+W8+vEkUfq4/r6enMyUfKPH5v1jRs5i9l2GFENLBjMS9nV5qsJ/U//G/3rLlZPxb8AzmBisuUNAAA=", "Settlement_Instruction.Account.Ordering_Customer_Account_Number": "", "Trade.Event_Physical_Status": "Live", "Settlement_Instruction.Account.Beneficiary_BIC_code": "", "Settlement_Instruction.SSI_Unique_Id": "", "Settlement_Instruction.Account.Counterparty_CMS_Account_Number": "", "Settlement_Instruction.Account.Beneficiary_Bank_BIC_code": "", "Settlement_Instruction.Account.Ordering_Customer_Street_Address": "", "Cashflow.Is_Cashflow_Unnet": "false", "Cashflow.Next_Cashflow_Id": null, "Trade_Version": "0", "Cashflow.Cashflow_Audit_Version": null, "Settlement_Instruction.Account.Ordering_Customer_City": "", "Entity.General_Ledger_Business_Unit_Name": null, "Entity.Booking_Entity_SCI_FMCODE": null, "Data_Flow.Data_Source_System_Domain_Name": "FM", "Cashflow.Payment_Type": "InitialExchange/Fixed", "Cashflow.Status_Event_Type": "NostroStamped", "Cashflow.Is_Payment_Intent_To_Settle": "false", "Settlement_Instruction.Account.Beneficiary_Street_Address": "", "Instrument_Common.CFI_Code": "SRCXCX", "Settlement_Instruction.Nostro_Swift_Message_Type": "", "Cashflow.Cashflow_Id": "004333265072", "Settlement_Instruction.Account.Intermediary_BIC_code": "", "Cashflow.FMO_Comment": null, "Cashflow.Minor_Version_Description": "", "Entity.Person.Event_Coverage_Marketer_PSID": null, "Entity.Booking_Entity_Country_ISO_Code": null, "Entity.Booking_Entity_SCI_FMID": "10036642", "Settlement_Instruction.Account.SCB_Nostro_Account_Type": "NOS", "Cashflow.Cashflow_State": "WAITING", "Cashflow.FMO_Comment_Timestamp": null, "Data_Flow.Data_Source_System_Country_Code": "ALL", "Cashflow.Payment_Amount": "1000000.0", "Cashflow.Event_Date": "2024-02-19", "Settlement_Instruction.Remittance_Information_2": "", "Settlement_Instruction.Remittance_Information_3": "", "Settlement_Instruction.Account.Ordering_Customer_BIC_Code": "", "Settlement_Instruction.Remittance_Information_4": "", "Portfolio.Booking_Entity_Trade_Portfolio_Name": "CNO_SWP_ASX_IR_STL", "Cashflow.Action_Type": null, "Settlement_Instruction.Remittance_Information_1": "", "Cashflow_Sequence": null, "Trade_Lake_Transaction_To_Date_Time": "9999-12-31 00:00:00", "Settlement_Instruction.Account.Beneficiary_Account_Number": "", "Cashflow.Cashflow_Version": "0", "Settlement_Instruction.Account.Booking_Entity_Correspondent_Street_Address": "TAUNUSANLAGE 16 FRANKFURT AM MAIN", "Cashflow.Position_Id": null, "Settlement_Instruction.Value_Date": null, "Instrument_Common.Financial_Instrument_Code": null, "Trade_Lake_Latest_Event_Date_Time": null, "Cashflow.Payment_Date_Business_Day_Convention": "NONE", "Settlement_Instruction.Account.Booking_Entity_Correspondent_Account_Number": "", "Entity.Person.Booking_Marketer_PSID": "", "Trade_State": "TOBESENT", "Settlement_Instruction.Account.Booking_Entity_Correspondent_BIC_code": "SCBLDEFXXXX", "Settlement_Instruction.Account.SCB_Nostro_Account_Number": "EUR MAIN", "Settlement_Instruction.Sender_To_Receiver_Information_4": "", "Cashflow.Audit": { "touchPointHistory": null, "exceptionList": [ { "exceptionCode": "Stella_Corp_CCS", "businessFlow": "STRATEGIC_SETTLEMENT", "sourceSystem": "RATAN-RULE-SERVICE", "exceptionType": "BUSINESS", "description": "Stella Corp CCS", "status": "PENDING_OPERATOR" }, { "exceptionCode": "Pending Affirmation", "businessFlow": "STRATEGIC_SETTLEMENT", "sourceSystem": "RATAN-RULE-SERVICE", "exceptionType": "BUSINESS", "description": "Cashflow and trade are not confirmed or affirmed. cashflow affirmation status is Unaffirmed, nettingId is , sourceSystem is Stella, counterpartyFlag is ", "status": "PENDING_OPERATOR" }, { "exceptionCode": "Missing Vostro", "businessFlow": "SETTLEMENT", "sourceSystem": "RATAN", "exceptionType": "BUSINESS", "description": "MISSING_VOSTRO_ERROR", "status": "PENDING_OPERATOR" }, { "exceptionCode": "CORP Client", "businessFlow": "STRATEGIC_SETTLEMENT", "sourceSystem": "RATAN-RULE-SERVICE", "exceptionType": "BUSINESS", "description": "Entity Counterparty[FMID='401024052'] is corp client", "status": "PENDING_OPERATOR" } ] }, "Settlement_Instruction.Sender_To_Receiver_Information_3": "", "Settlement_Instruction.Account.Beneficiary_Correspondent_Street_Address": "", "Settlement_Instruction.Sender_To_Receiver_Information_6": "", "Settlement_Instruction.Account.Beneficiary_Account_Name_2": "", "Settlement_Instruction.Sender_To_Receiver_Information_5": "", "BCS_Trade_Id": "", "Cashflow.Bypass_Workflow_Indicator": "null", "Settlement_Instruction.Account.Intermediary_City": "", "Settlement_Instruction.Account.Beneficiary_Account_Name": "", "Settlement_Method": "", "Settlement_Instruction.Swift_Message_Type": "" } ] |