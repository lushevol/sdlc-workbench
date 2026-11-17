# Business Requirement

## Korea business requirement

[Korea Cashflow Migration -Ratan to OLTP Accounting - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Korea+Cashflow+Migration+-Ratan+to+OLTP+Accounting)

## EBBS Tech Desgin

[Swift Generation & Settlement Accounting Tech design - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=2962449544)

# Task Generation Process

## Init Task part

| Task Type | Downstream | Diff |
| --- | --- | --- |
| Normal | EBBS | set task.System_Date as Payment_Date, 1 entity only have 1 bridge_account |
| OLTP | set task.System_Date as Payment_Date, but bridge_account depends on currency |
| Reversal | EBBS | same as Normal type |
| OLTP | same as Normal type |
| Netted/Split | EBBS | same as Normal type |
| OLTP | same as Normal type |

## Validate Task

| Task Type | Downstream | Diff |
| --- | --- | --- |
| Normal | EBBS | check nostro and bridge account are stamped, then check EBBS json fileds are filled |
| OLTP | check nostro and bridge account are stamped, if settlementMeans = 'NOX' and settlementAccount contains 'UUID'/'UISUS' then disable the task |

## Generate JSON message

| Task Type | Downstream | Diff |
| --- | --- | --- |
| Normal | EBBS | set task.Request_info = EBBS format json |
| OLTP | set task.ExtColumn2 = OLTP format json, 53 BIC/Receiver BIC need add new logic |
| Reversal | EBBS | update task.Request_info json, flip account and direction |
| OLTP | update task.ExtColumn2 json, also flip account and direction in TransData part |
| Netted/Split | EBBS | same as Normal type |
| OLTP | same as Normal type |

## Publish Message to Downstream

| Task Type | Downstream | Diff |
| --- | --- | --- |
| Normal | EBBS | existed function for publish message to ebbs |
| OLTP | create a new kafka topic for OLTP message and create a new method for this |
| Reversal | EBBS | same as Normal type |
| OLTP | same as Normal type |
| Netted/Split | EBBS | same as Normal type |
| OLTP | same as Normal type |

# Resend JSON message

| Downstream | Diff |
| --- | --- |
| EBBS | 1. Sent but no response will retry 3 times interval 4 min 2. if response is TXN99999 or TEC0004 will retry 3 times interval 4min |
| OLTP | no retry mechanism, but need to exclude KR tasks from retry job |

# SOD Job

| Downstream | Diff |
| --- | --- |
| EBBS | 1. start at 06:00 every day interval 1 hour util 18:00. It will collect all Hold and payment_date <= current_date tasks. 2. check if request_info is empty will generate json message first |
| OLTP | 1. start at 06:00 every day interval 1 hour util 18:00. It will collect all Hold and payment_date <= current_date tasks. 2. check **extColumn2 **is empty? yes, then generate json first |

# Ack/Nack process

| Downstream | Diff |
| --- | --- |
| EBBS | 1. receive response msg from topic 2. save message 3. update task status |
| OLTP | it follows EBBS process, only receive response from different topic |

# JSON Sample Comparation

| Message Type | EBBS | OLTP |
| --- | --- | --- |
| Request | ```js { "data": { "id": "Field_Message_ID", "type": "post-transactions", "attributes": { "request": { "source-system": "RATAN", "posting-type": "FundsTransfer", "transaction-type": "RTN", "posting-branch": "Field_Posting_Branch", "external-system-key": "Field_External_System_Key", "transaction-currency": "Field_Transaction_Currency", "transaction-amount": Field_Transaction_Amount, //"maker-id": "SYSTEM", Optional //"maker-date": "2019-11-30", Optional //"checker-id": "SYSTEM", Optional //"approver-id": "SYSTEM", Optional "transaction entry": [ { "narratives": { "narration1": "Narration_001", "narration2": "Narration_002", "narration3": "Narration_003", "narration4": "Narration_004", "narration5": "Narration_005", "narration6": "Narration_006" }, "extended-narratives": { "extended-narration1": "Extended_Narrative_01", "extended-narration2": "Extended_Narrative_02" }, //"force-post": "N", Optional "value-date": "Field_Value_Date", "account-number": "Field_eBBS_Nostro_Account", //"allow-insufficient-funds": "N", Optional "casa-currency-code": same with transaction-currency "transaction-code": "Field_Transaction_code", // "master-number": "239082", Optional "transaction-nature": "Field_eBBS_Nostro_DebitCredit" }, { "narratives": { "narration1": "Narration_001", "narration2": "Narration_002", "narration3": "Narration_003", "narration4": "Narration_004", "narration5": "Narration_005", "narration6": "Narration_006" }, "extended-narratives": { "extended-narration1": "Extended_Narrative_01", "extended-narration2": "Extended_Narrative_02" }, //"force-post": "N", Optional "value-date": "Field_Value_Date", "account-number": "Field_eBBS_Bridge_Account", //"allow-insufficient-funds": "N", Optional "casa-currency-code": same with transaction-currency "transaction-code": "Field_Transaction_code", // "master-number": "239082", Optional "transaction-nature": "Field_eBBS_Nostro_DebitCredit" }, } } } } ``` | ```js { "ns:SCBML": { "ns:header": { "ns:messageDetails": { "ns:messageVersion": "1.0", //hardcord "ns:messageType": { "ns:typeName": "CoreBanking:ratanCommonRoute" //hardcord } }, "ns:originationDetails": { "ns:messageSender": { "ns:messageSender": { "*body": "RATAN" //hardcord }, "ns:senderDomain": { "ns:domainName": { "*body": "CoreBanking" //hardcord } }, "ns:countryCode": "KR" //hardcord }, "ns:initiatedTimestamp": "2025-11-28T02:28:35.563+00:00" //Timestamp Ratan send the message in GMT yyyy-MM-dd'T'HH:mm:ssXXX }, "ns:captureSystem": "OLTP" //hardcord }, "payload": { "ns:payloadFormat": "json", //hardcord "ns:payloadVersion": "1.0", //hardcord "scbmlPayload": { "REQUESTMESSAGE": { "SYSTEMHEADER": { "TMSG_WRTG_DT": "20251128", //RATAN side "TMSG_WRTG_TM": "1111497", //RATAN side "TRSC_GRCO_CD": "01", //hardcord "TMSG_CRE_SYS_NM": "0998ISA1",//hardcord TBD "ISS_SRL_NO": "", //hardcord "IPV6_ADR": "10.61.17.205", //RATAN side hardcode "INPT_DLV_CD": "M", //hardcord "ENVR_INFO_DV_CD": "D", //hardcord "RQST_RSPS_DV_CD": "Q", //hardcord "TRSC_SYNC_DV_CD": "S", //hardcord "TRAN_CD": "RATAN_OLTP_001", //EDMI side TBD "TMSG_RSPS_DTM": "", //hardcord "PROC_RSLT_DV_CD": "", //hardcord "CHNL_TYP_CD": "ISA", //hardcord "MCI_ND_NO": "", //hardcord "MCI_SESS_ID_NO": "" //hardcord }, "TRANCOMMONHEADER": { "TMSG_MSG_TYP_CD" : "1", //hardcord "BLNG_GRCO_CD" : "01", //hardcord "BLNG_BR_NO" : "998", //hardcord "EMP_NO" :null, //hardcord "OFLV_CD" :null, //hardcord "OFDY_CD" :null, //hardcord "EMP_CD_NO" :null, //hardcord "TXN_BR_NO" :"998", //hardcord "APV_CD" : null, //hardcord "APV_BRNCD_1" : null, //hardcord "APV_EMP_NO_1" : null, //hardcord "APV_PASSWD_1" : null, //hardcord "APV_BRNCD_2" : null, //hardcord "APV_EMP_NO_2" : null, //hardcord "APV_PASSWD_2" : null, //hardcord "APV_BRNCD_3" : null, //hardcord "APV_EMP_NO_3" : null, //hardcord "APV_PASSWD_3" : null, //hardcord "SCRN_ID" : null, //hardcord "SUB_SCRN_ID" : null, //hardcord "SIMUL_CD" : " ", //hardcord "PSBK_PRTR_CONN_DV_CD" : "0", //hardcord "PSBK_DV_CD" : "0", //hardcord "PSBK_MS_VAL" : null, //hardcord "PSBK_COVER_PAGE" : " ", //hardcord "OUTPUT_LINE_VAL" : "00", //hardcord "CRD_DV_CD" : " ", //hardcord "CRD_MDCL_DV_CD" : " ", //hardcord "PAPER_DV_CD" : " ", //hardcord "FUTURE_TRAN_KEY" : " ", //hardcord "CANCEL_KEY" : " ", //hardcord "PREV_DAY_KEY" : " ", //hardcord "PAST_DATE_KEY" : " ", //hardcord "PRINT_CONT_START" : " ", //hardcord "PRINT_CONT" : " ", //hardcord "MPGB" : " ", //hardcord "TRXCD" : "", //hardcord TBD "BIZDISTCD" : "", //hardcord TBD "INPUTDISTCD" : "", //hardcord TBD "INPUTDISTCD_CANCEL" : "",//hardcord TBD "CHANNELID" : "", //hardcord TBD "OLDACCTCD" : "", //hardcord TBD "MACRO_AI" : "", //hardcord TBD "MACRO_AO" : "", //hardcord TBD "SERVERMSG" : null //hardcord }, "CUSTOMINFO": null, //hardcord "CONTTRAN": null, //hardcord "TRANDATA": { //Please refer to field mapping table "YIGRILJA":"20251107", //RATAN side "YIREFNO ":"M700054313360101", //RATAN side "YIGJJRSU":"02", //RATAN side "YIGJ":[{ "YIBRNO":"017", //RATAN side "YICODE":"043150", //RATAN side suspend account/bridge account "YISECD":"000", //RATAN side "YITONG":"001", //RATAN side currency "YIIPJI":"10", //RATAN side "YIAMT":"235102.23", //RATAN side "YIGUBN":"N"} //RATAN side Domestic Amount ,{"YIBRNO":"017", "YICODE":"040320", //nostro account "YISECD":"000", "YITONG":"001", "YIIPJI":"30", "YIAMT":"235102.23", //amount "YIGUBN":"N"} //Domestic Amount ] "YIRCJRSU":"1", //RATAN side "YIRC":[{ "YIRCTYPE":"1", //RATAN side "YIRCBIC":"KOEXKRSExxx", //RATAN side "YIRCTONG":"001", //RATAN side "YIRCIPJI":"2", //RATAN side "YIRCDATE":"20251107", //RATAN side "YIRCAMT":"235102.23", //RATAN side "YIRCNO":"DV70M00125825123", //RATAN side "YIRCGBN":"N"} //RATAN side ] } } } } } } } ``` |
| ACK | ```java { "data": { "id": "7440245409631444992", "type": "post-transactions", "attributes": { "response": { "transaction entry": [ { "account-number": "44799919449", "casa-currency-code": "HKD", "amount": 91806.71, "transaction-nature": "D", "cost-rate": 1, "customer-rate": 1 }, { "account-number": "44799919686", "casa-currency-code": "HKD", "amount": 91806.71, "transaction-nature": "C", "cost-rate": 1, "customer-rate": 1 } ], "external-system-key": "N00000126511.0.4", "response-code": "TXN00000", "response-description": "Success" } } } } ``` | **EXPAND: ACK from OLTP** { "ns:SCBML": { "ns:header": { "ns:messageDetails": { "ns:messageVersion": "1.0", "ns:messageType": { "ns:typeName": "CoreBanking:ratanCommonRoute" } }, "ns:originationDetails": { "ns:messageSender": { "ns:messageSender": { "*body": "RATAN" }, "ns:senderDomain": { "ns:domainName": { "*body": "CoreBanking" } }, "ns:countryCode": "KR" }, "ns:initiatedTimestamp": "2025-11-28T02:28:35.563+00:00", "ns:trackingId": "M0000123456.01.07" }, "ns:captureSystem": "OLTP" }, "payload": { "ns:payloadFormat": "json", "ns:payloadVersion": "1.0", "scbmlPayload": { "REQUESTMESSAGE": { "SYSTEMHEADER": { "TMSG_WRTG_DT": "20251128", "TMSG_WRTG_TM": "111149", "TRSC_GRCO_CD": "01", "TMSG_CRE_SYS_NM": "0998ISA1", "ISS_SRL_NO": "", "IPV6_ADR": "10.61.17.205", "INPT_DLV_CD": "M", "ENVR_INFO_DV_CD": "D", "RQST_RSPS_DV_CD": "Q", "TRSC_SYNC_DV_CD": "S", "TRAN_CD": "RATAN_OLTP_001", "TMSG_RSPS_DTM": "", "PROC_RSLT_DV_CD": "", "CHNL_TYP_CD": "RAT", "MCI_ND_NO": "", "MCI_SESS_ID_NO": "" }, "TRANCOMMONHEADER": { "TMSG_MSG_TYP_CD": "1", "BLNG_GRCO_CD": "01", "BLNG_BR_NO": "0998", "EMP_NO": null, "OFLV_CD": null, "OFDY_CD": null, "EMP_CD_NO": null, "TXN_BR_NO": "0998", "APV_CD": null, "APV_BRNCD_1": null, "APV_EMP_NO_1": null, "APV_PASSWD_1": null, "APV_BRNCD_2": null, "APV_EMP_NO_2": null, "APV_PASSWD_2": null, "APV_BRNCD_3": null, "APV_EMP_NO_3": null, "APV_PASSWD_3": null, "SCRN_ID": null, "SUB_SCRN_ID": null, "SIMUL_CD": null, "PSBK_PRTR_CONN_DV_CD": null, "PSBK_DV_CD": null, "PSBK_MS_VAL": null, "PSBK_COVER_PAGE": null, "OUTPUT_LINE_VAL": null, "CRD_DV_CD": null, "CRD_MDCL_DV_CD": null, "PAPER_DV_CD": null, "FUTURE_TRAN_KEY": null, "CANCEL_KEY": null, "PREV_DAY_KEY": null, "PAST_DATE_KEY": null, "PRINT_CONT_START": null, "PRINT_CONT": null, "MPGB": null, "TRXCD": "TI1FBS02", "BIZDISTCD": "89", "INPUTDISTCD": "G002", "INPUTDISTCD_CANCEL": null, "CHANNELID": null, "OLDACCTCD": "89", "MACRO_AI": "YIYJM60", "MACRO_AO": "YOYJM60", "SERVERMSG": null }, "CUSTOMINFO": null, "CONTTRAN": null, "TRANDATA": { "YOREFNO ": "M700054313360101", "YOACK": "ACK", "YOEERR": "TXN00000", "YOEMSG": "SUCCESS" } } } } } } **EXPAND_END** |
| NACK | ```java { "data": { "id": "7439498479767928832", "type": "post-transactions", "attributes": { "response": { "external-system-key": "M09955476283.0.11", "response-code": "TXN00015", "response-description": "Account Number and currency code combination provided is not correct USD2387251800191710761950 " } } } } ``` | **EXPAND: NACK from OLTP** { "ns:SCBML": { "ns:header": { "ns:messageDetails": { "ns:messageVersion": "1.0", "ns:messageType": { "ns:typeName": "CoreBanking:ratanCommonRoute" } }, "ns:originationDetails": { "ns:messageSender": { "ns:messageSender": { "*body": "RATAN" }, "ns:senderDomain": { "ns:domainName": { "*body": "CoreBanking" } }, "ns:countryCode": "KR" }, "ns:initiatedTimestamp": "2025-11-28T02:28:35.563+00:00", "ns:trackingId": "M0000123456.01.07" }, "ns:captureSystem": "OLTP" }, "payload": { "ns:payloadFormat": "json", "ns:payloadVersion": "1.0", "scbmlPayload": { "REQUESTMESSAGE": { "SYSTEMHEADER": { "TMSG_WRTG_DT": "20251128", "TMSG_WRTG_TM": "111149", "TRSC_GRCO_CD": "01", "TMSG_CRE_SYS_NM": "0998ISA1", "ISS_SRL_NO": "", "IPV6_ADR": "10.61.17.205", "INPT_DLV_CD": "M", "ENVR_INFO_DV_CD": "D", "RQST_RSPS_DV_CD": "Q", "TRSC_SYNC_DV_CD": "S", "TRAN_CD": "RATAN_OLTP_001", "TMSG_RSPS_DTM": "", "PROC_RSLT_DV_CD": "", "CHNL_TYP_CD": "RAT", "MCI_ND_NO": "", "MCI_SESS_ID_NO": "" }, "TRANCOMMONHEADER": { "TMSG_MSG_TYP_CD": "1", "BLNG_GRCO_CD": "01", "BLNG_BR_NO": "0998", "EMP_NO": null, "OFLV_CD": null, "OFDY_CD": null, "EMP_CD_NO": null, "TXN_BR_NO": "0998", "APV_CD": null, "APV_BRNCD_1": null, "APV_EMP_NO_1": null, "APV_PASSWD_1": null, "APV_BRNCD_2": null, "APV_EMP_NO_2": null, "APV_PASSWD_2": null, "APV_BRNCD_3": null, "APV_EMP_NO_3": null, "APV_PASSWD_3": null, "SCRN_ID": null, "SUB_SCRN_ID": null, "SIMUL_CD": null, "PSBK_PRTR_CONN_DV_CD": null, "PSBK_DV_CD": null, "PSBK_MS_VAL": null, "PSBK_COVER_PAGE": null, "OUTPUT_LINE_VAL": null, "CRD_DV_CD": null, "CRD_MDCL_DV_CD": null, "PAPER_DV_CD": null, "FUTURE_TRAN_KEY": null, "CANCEL_KEY": null, "PREV_DAY_KEY": null, "PAST_DATE_KEY": null, "PRINT_CONT_START": null, "PRINT_CONT": null, "MPGB": null, "TRXCD": "TI1FBS02", "BIZDISTCD": "89", "INPUTDISTCD": "G002", "INPUTDISTCD_CANCEL": null, "CHANNELID": null, "OLDACCTCD": "89", "MACRO_AI": "YIYJM60", "MACRO_AO": "YOYJM60", "SERVERMSG": null }, "CUSTOMINFO": null, "CONTTRAN": null, "TRANDATA": { "YOREFNO": "M700054313360101", "YOACK": "NACK", "YOEERR": "TXN00001", "YOEMSG": "Transaction date must be in numeric format" } } } } } } **EXPAND_END** |
| EOD NACK | none | **EXPAND: NACK from OLTP** { "SCBML" : { "ns:header" : { "ns:messageDetails" : { "ns:messageType" : { "ns:subType" : { }, "ns:typeName" : "CoreBanking:businessOnlineBCommonRoute" }, "ns:messageVersion" : "1.0", "ns:multiMessage" : { "ns:multiMessageKnown" : { } } }, "ns:originationDetails" : { "ns:trackingId" : "BBW010120260513174000921031", "ns:checksum" : { }, "ns:initiatedTimestamp" : "2026-05-13T17:40:00:435", "ns:serviceBusID" : "CB_TBS03_H221", "ns:messageSender" : { "ns:countryCode" : "KR", "ns:messageSender" : { "*body" : "BOB" }, "ns:senderDomain" : { "ns:domainName" : { "*body" : "CoreBanking" }, "ns:subDomainName" : { } } }, "ns:possibleDuplicate" : "FALSE" }, "ns:captureSystem" : "OLTP", "ns:process" : { "ns:eventType" : "" }, "ns:exceptions" : { "ns:exception" : [ { "ns:timestamp" : "2026-05-13T08:41:02.101+00:00", "ns:code" : { "*body" : "Error" }, "ns:description" : "com.wm.app.b2b.server.ServiceException: [ISS.0086.9067] wait timed out\n\tat scbIntServicesUtilities.java.throwException(java.java:938)\n\tat jdk.internal.refle } ] } } } } **EXPAND_END** |

# Solace Configuration

## Kafka topic:

- To OLTP: Cash_Settlement_OLTP_Accounting_KR
- From OLTP: Cash_Settlement_OLTP_Response

## Solace config

📎 [KR_OLTP_ProjectEngagement_Template.xlsx](attachments/KR_OLTP_ProjectEngagement_Template.xlsx)

# Static-data service change

## Properties change

```yml
        - bookingEntitySciFmid: 10036645
          branchCode: 70
```

## Code change

[com.scb.ratan.sd](http://com.scb.ratan.sd).entity.EbbsAccount need add new attribute "currency" as Korea have 2 bridge account for different currencies.

| M_ENTITY | FMID | ISO Currency | Bridge Account |
| --- | --- | --- | --- |
| SCFB_SEOUL | 10036645 | KRW | 000287 |
| SCFB_SEOUL | 10036645 | FCY | 040446 |

# Properties service change

## add Korea FMID in STRATEGIC_FM_LIST

| Entity Name | FMID | Country Code |
| --- | --- | --- |
| SCFB_SEOUL | 10036645 | KR |

## add CPT confirguration

CPT cashflow release condition to be updated to VD<= 14-Aug

currency - USD = 1 & KRW = 1

# DB change

## ratan_cash_accounting_service.ratan_accounting_request_task

| column name | type | default value |
| --- | --- | --- |
| settlement_means | varchar | null |
| settlement_account | varchar | null |
| booking_entity_BIC_code | varchar | null |

## ratan_cash_accounting_service.ratan_accounting_request_task_history

| column name | type | default value |
| --- | --- | --- |
| settlement_means | varchar | null |
| settlement_account | varchar | null |
| booking_entity_BIC_code | varchar | null |

index:

CREATE INDEX IF NOT EXISTS ratan_accounting_request_task_history_task_status_idx ON ratan_cash_accounting_service.ratan_accounting_request_task_history USING btree (task_status, booking_entity_fmid, created_at);

## ratan_cash_accounting_service.ratan_accounting_response_info

| column name | type | default value |
| --- | --- | --- |
| original_response | text | null |