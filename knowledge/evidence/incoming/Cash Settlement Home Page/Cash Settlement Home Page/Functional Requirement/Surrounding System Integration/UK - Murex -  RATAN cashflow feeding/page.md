# Background

As continue of FMRP journey we would migrate UK cashflows from Murex 2.11 to RATAN, considering the significant payment volume the CN/SG/IN/MY solution won't be working. A new model need to be design & implement to cater for the high volume.

# Murex Feeding

- Payments can be sent by individual MxML( one payment per MxML file) or sent by CSV file( multi payments in one file), there's no cashflow overlap on these 2 feeding types. - Real time feed cover VD-1, VD and VD+1 business day - CSV file cover VD from T+2 to T+7 business day (exclude weekend, 12.25;01.01)
- Batch files publishing from GMT 00:00 to 19:00. - [@Ren, Eric Shiyi](mailto:EricShiyi.Ren@sc.com) will double check and confirm the time
- Each batch will contain 3 files as below naming convention: - **YYYYMMDD** is the date of batch - **XXX** is the sequence number within the day, 001,002,003…010 - **ZZZZ** is the count of payments in base file, used for recon purpose - FMRP_Murex_Payments_YYYYMMDD_XXX_Base.csv - FMRP_Murex_Payments_YYYYMMDD_XXX_Snapshot.csv - FMRP_Murex_Payments_YYYYMMDD_XXX_Completion_ZZZZ.csv
- For the last file finished each day, an extra ending file will send to indicate the batch file finished for the day:** FMRP_Murex_Payments_YYYYMMDD_END.csv** - If there is no batch file processed during the day, Murex will also send the ending file
- Murex will only send required column in the base file with fixed column name and sequence – initial version finalized
- For the snapshot file, only CNCL and SNTR status need to be processed from Ratan. INIT will also show up in the snapshot file but no need to process from Ratan.
- Since Murex cannot automatically re-generate the batch file, we need to hold the file transfer if there is any batch process issue. Murex need to wait the batch ACK from Ratan to process the next batch - Ratan will send ACK/NACK FILE to a different folder - time out – 30 min: if Murex does not get any Ratan response in 30 minutes, the batch process will be on hold. Murex PSS will monitor this and check the root cause - NACK: Ratan send the NACK response, meanwhile need Ratan PSS raise the issue to murex PSS - ACK/NACK file name - FMRP_Murex_Payments_YYYYMMDD_XXX_Ack.csv FMRP_Murex_Payments_YYYYMMDD_XXX_Nack.csv
- Exception Handling: - File NACK: Ratan will stop processing, further batches will be stopped as well. The agreement is Murex need to guarantee the batch file publishing and accuracy - Payment level error: Ratan keep processing batch, but generate exception for particular payment level indicating. how to display and process the error to be discussed | **Category** | **Description** | **Exception Code** | **Ratan Behavior** | **Expected Action (TBC with Murex)** | | --- | --- | --- | --- | --- | | File NACK | File missed (complete file received, but base or snapshot not received) | BatchFileNotComplete | Received file in this batch will be moved to error folder and send NACK | Murex replay the same file | | ~~Received file name , sequence not as expected~~ | | | | | Recon issue: the provided count does not match the count in base file | BatchReconError | Received file in this batch will be moved to error folder and send NACK | Murex investigate and resend | | Column number, sequence not as expected | BatchFormatError | Received file in this batch will be moved to error folder and send NACK | Murex investigate and resend | | Invalid document format: files not properly ended | | 001 received, but the last batch file is not ending file | BatchDateNotEnd | hold 001 file and wait for the ending file | Murex investigate and resend the ending file | | | 001 received, 002 not received | no exception | repeating join to continue checking if 002_completion file received | | | Payment error | Payment validation exception: mandatory field value missed invalid value payment in base not in snapshot | PaymentValidationError | TBC | TBC |

# UK - Murex → RATAN Payment Feeding flow

**EXPAND: Flow_v0**

#

**EXPAND_END**

# Batch File Spec

| **RATAN Fields** | **Derivation Logic** | **Mandatory?** | **Field Name in Mx Batch Report ** | **Field Type in Murex DB** | **Sample Xpath in MXML** | **Sample Value in MXML** | **SameValue:MXML vs DB** | **DB Sample Value** | **Filed extraction in DB** | **DBValueGenerationApproach** | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Cashflow.Cashflow_Id | Formula_CashflowID | Y | FLOW_ID | numeric(10,0) | /MxPayML/flowID | 107791234 | Y | 107791234 | pay.M_FLOW_ID, | | |
| | | N | LTI_ID | numeric(10,0) | /MxPayML/linkedTradeID | 5741473.000000 | N | 5741473 | pay.M_LTI_ID, | | |
| | | Y | TRN_LINK | numeric(10,0) | /MxPayML/transactionLinkID | 96137655.000000 | N | 96137655 | pay.M_TRN_LINK, | | |
| | | Y | TRN_ID | numeric(10,0) | /MxPayML/transactionOriginID | 96137655.000000 | N | 96137655 | pay.M_TRN_ID, | | |
| | | Y | TRN_REF | numeric(10,0) | /MxPayML/transactionID | 96137655.000000 | N | 96137655 | pay.M_TRN_REF, | | |
| | | Y | AMOUNT | numeric(19,3) | /MxPayML/flowAmount | 3394.730000 | N | 3394.730 | pay.M_AMOUNT, | | |
| | | N | CPU_TIME | numeric(8,0) | /MxPayML/computerTime | 09:24:31 | Y | 09:24:31 | convert(char(8),dateadd(ss,pay.M_CPU_TIME,pay.M_CPU_DATE),108)M_CPU_TIME, | ToFormulate for recon: char(8) | |
| | | N | CPU_DATE | datetime | /MxPayML/computerDate | 20240729 | Y | 20240729 | convert(char(8),pay.M_CPU_DATE, 112) AS 'M_CPU_DATE', | ToFormulate for recon: char(8) | |
| | | Y | STATUS | char(4) | /MxPayML/flowStatus | INIT | Y | INIT | pay.M_STATUS as 'M_STATUS', | Status of base flow ID (<>MXML:INIT) | |
| | | Y | TRN_FMLY | char(5) | /MxPayML/transactionFamily | SCF | Y | SCF | rtrim(pay.M_TRN_FMLY)M_TRN_FMLY, | RTRIM | |
| | | Y | TRN_GRP | char(5) | /MxPayML/transactionGroup | SCF | Y | SCF | rtrim(pay.M_TRN_GRP)M_TRN_GRP, | RTRIM | |
| | | N | TRN_TYPE | char(5) | /MxPayML/transactionType | SCF | Y | SCF | rtrim(pay.M_TRN_TYPE)M_TRN_TYPE, | RTRIM | |
| | | Y | ENTITY | char(10) | /MxPayML/entity | SDBU SING | Y | SDBU SING | rtrim(pay.M_ENTITY)M_ENTITY, | RTRIM | |
| | | Y | CNTRP | char(15) | /MxPayML/counterparty | GUEC00HSHK/HKG | Y | GUEC00HSHK/HKG | rtrim(pay.M_CNTRP)M_CNTRP, | RTRIM | |
| | | N | COMMENT | char(30) | /MxPayML/comment | | Y | | rtrim(pay.M_COMMENT) as 'M_COMMENT', | RTRIM | |
| | | N | TYPOLOGY | char(20) | /MxPayML/transactionTypology | Premium | Y | Premium | rtrim(pay.M_TYPOLOGY)M_TYPOLOGY, | RTRIM | |
| | | Y | CREDIT | char(1) | /MxPayML/isCredit | Y | Y | Y | case when pay.M_CREDIT = 'C' then 'Y' else 'N' end as 'M_CREDIT', | ToFormulate | |
| | | Y | VALUE_DATE | datetime | /MxPayML/valueDate | 20240731 | Y | 20240731 | convert(char(8),pay.M_VALUE_DATE, 112) AS 'M_VALUE_DATE', | ToFormulate for recon: char(8) | |
| | | Y | CURRENCY | char(3) | /MxPayML/currency | USD | Y | USD | rtrim(pay.M_CURRENCY)M_CURRENCY, | RTRIM | |
| | | N | STRATEGY | char(15) | /MxPayML/strategy | FX_TRF | Y | FX_TRF | rtrim(pay.M_STRATEGY)M_STRATEGY, | RTRIM | |
| | | Y | LABEL | char(15) | /MxPayML/portfolio | PAE_T24_TRFDM_S | Y | PAE_T24_TRFDM_S | rtrim(port.M_LABEL)M_LABEL, | RTRIM | |
| | | Y | INST_TYPE | char(5) | /MxPayML/type | Cash | Y | Cash | case when pay.M_INST_TYPE = 0 then 'Cash' when pay.M_INST_TYPE = 1 then 'DVP' when pay.M_INST_TYPE = 2 then 'FOP' when pay.M_INST_TYPE = 3 then 'CashR' end as M_INST_TYPE, | ToFormulate | |
| | | N | FLOW_TYPE0 | char(4) | /MxPayML/flowType/flowType0 | | Y | | rtrim(pay.M_FLOW_TYPE0)M_FLOW_TYPE0, | RTRIM | |
| | | N | FLOW_TYPE1 | char(4) | /MxPayML/flowType/flowType1 | | Y | | rtrim(pay.M_FLOW_TYPE1)M_FLOW_TYPE1, | RTRIM | |
| | | N | FLOW_TYPE2 | char(4) | /MxPayML/flowType/flowType2 | | Y | | rtrim(pay.M_FLOW_TYPE2)M_FLOW_TYPE2, | RTRIM | |
| | | N | FLOW_TYPE3 | char(4) | /MxPayML/flowType/flowType3 | | Y | | rtrim(pay.M_FLOW_TYPE3)M_FLOW_TYPE3, | RTRIM | |
| | | N | FLOW_TYPE4 | char(4) | /MxPayML/flowType/flowType4 | INT | Y | INT | rtrim(pay.M_FLOW_TYPE4)M_FLOW_TYPE4, | RTRIM | |
| | | N | COM_FLOW | numeric(1,0) | [/MxPayML/flowUserDefinedFields/userDefinedField/fieldLabel/@COM_FLOW](https://confluence.global.standardchartered.com/mailto:/MxPayML/flowUserDefinedFields/userDefinedField/fieldLabel/@COM_FLOW) | 0 | Y | 0 | payudf.M_COM_FLOW, | | |
| | | N | NID | numeric(15,0) | [/MxPayML/flowUserDefinedFields/userDefinedField/fieldLabel/@NID](https://confluence.global.standardchartered.com/mailto:/MxPayML/flowUserDefinedFields/userDefinedField/fieldLabel/@NID) | 0 | y | 0 | payudf.M_NID, | | |
| | | Y | SID | numeric(15,0) | /MxPayML/flowUserDefinedFields/userDefinedField/fieldLabel/@SID | 5741469 | Y | 5741469 | payudf.M_SID, | | |
| | | N | X_DUMMY1 | numeric(19,3) | /MxPayML/flowUserDefinedFields/userDefinedField/fieldLabel/@X_DUMMY1 | 3394.73 | N | 3394.730 | payudf.M_X_DUMMY1, | | |
| | | N | X_DUMMY2 | numeric(1,0) | /MxPayML/flowUserDefinedFields/userDefinedField/fieldLabel/@X_DUMMY2 | 0 | Y | 0 | payudf.M_X_DUMMY2, | | |
| | | N | X_DUMMY3 | numeric(1,0) | /MxPayML/flowUserDefinedFields/userDefinedField/fieldLabel/@X_DUMMY3 | 0 | Y | 0 | payudf.M_X_DUMMY3, | | |
| | | N | X_DUMMY4 | numeric(1,0) | /MxPayML/flowUserDefinedFields/userDefinedField/fieldLabel/@X_DUMMY4 | 0 | Y | 0 | payudf.M_X_DUMMY4, | | |
| | | N | TRN_DATE | datetime | /MxPayML/tradeDate | 20240729 | Y | 20240729 | convert(char(8),trade.M_TRN_DATE, 112) AS 'M_TRN_DATE', | ToFormulate for recon: char(8) | |
| | | Y | PUB_DATE_T | datetime | /MxPayML/scbExtraInfoBlock/publicationDateTime | 20-08-2024 08:32:54:550 | N | 30-08-2024 07:22:33:520 | rtrim(convert(char(10),getdate(),105)) + ' ' + rtrim(convert(char(12),getdate(),20)) as 'M_PUB_DATE_T', | ToFormulate for recon: char(23) | |
| | | N | VAL_STATUS | char(4) | /MxPayML/scbExtraInfoBlock/validationLevel | VALD | Y | VALD | trade.M_VAL_STATUS, | | |
| | | Y | LEID | char(10) | /MxPayML/scbExtraInfoBlock/entityFMID | 400451508 | Y | 400451508 | case when entity.M_ATLAS_LEID = null then '0' else entity.M_ATLAS_LEID end as 'M_LEID', | ToFormulate | |
| | | Y | SCI_ID | char(10) | /MxPayML/scbExtraInfoBlock/entityLEID | 12921313 | Y | 12921313 | case when entity.M_SCI_ID = null then '0' else entity.M_SCI_ID end as 'M_SCI_ID', | ToFormulate | |
| | | Y | ATLAS_LEID | char(10) | /MxPayML/scbExtraInfoBlock/counterpartyFMID | 400949160 | Y | 400949160 | case when cpty.M_ATLAS_LEID = null then '0' else cpty.M_ATLAS_LEID end as 'M_ATLAS_LEID', | ToFormulate | |
| | | Y | L_CODE | char(20) | /MxPayML/scbExtraInfoBlock/traderID | SYSTEMID | Y | SYSTEMID | rtrim(psid.M_L_CODE) as 'M_L_CODE', | RTRIM | |
| | | N | BIZ_UNIT | char(30) | /MxPayML/scbExtraInfoBlock/portBizUnit | WM - FX | Y | WM - FX | rtrim(portudf.M_BIZ_UNIT) as 'M_BIZ_UNIT', | RTRIM | |
| | | N | AMD_FLAG | char(1) | /MxPayML/scbExtraInfoBlock/amendmentFlag | N | Y | N | CASE WHEN EXISTS (SELECT 1 from MKT_OP_DBF mop where M_DEST_NB=pay.M_TRN_REF and (M_TYPE='RPL' or M_TYPE='RPL_M') and mop.M_SYS_DATE = pay.M_SYS_DATE) then 'Y' else 'N' end as 'M_AMD_FLAG', | ToFormulate | |
| | | N | DATE | datetime | /MxPayML/scbExtraInfoBlock/mxSystemDate | 20240725 | N | 20240801 | convert(char(8),sysdate.M_DATE, 112) AS 'M_DATE', | ToFormulate for recon: char(8) | |
| | | N | ACTION | char(10) | /MxPayML/scbExtraInfoBlock/action | INS | Y | INS | rtrim (pay.M_ACTION) as 'M_ACTION', | RTRIM | |
| | | N | MOP_LAST | char(5) | /MxPayML/scbExtraInfoBlock/tradeLastMKT | EXP | Y | EXP | rtrim(case when trade.M_MOP_LAST = 1 then 'EXR' when trade.M_MOP_LAST = 2 then 'EXP' when trade.M_MOP_LAST = 3 then 'XIT' when trade.M_MOP_LAST = 4 then 'NET' when trade.M_MOP_LAST = 5 then 'RPL' when trade.M_MOP_LAST = 6 then 'RPL_M' when trade.M_MOP_LAST = 7 then 'RPL_D' when trade.M_MOP_LAST = 0 then '' end) as M_MOP_LAST, | ToFormulate | |
| | | N | CREATOR | char(10) | /MxPayML/scbExtraInfoBlock/TrnParentID | 0 | Y | 0 | convert(varchar(10), trade.M_CREATOR) 'M_CREATOR', | ToFormulate | |
| | | Y | TRN_ORGID | char(10) | /MxPayML/scbExtraInfoBlock/TrnOrginalID | 96137655 | Y | 96137655 | convert(varchar(10), CASE WHEN trade.M_MRPL_ONB<1 THEN trade.M_NB ELSE trade.M_MRPL_ONB END) 'M_TRN_ORGID', | ToFormulate | |
| | | N | WAIT_FIX | char(1) | /MxPayML/scbExtraInfoBlock/isWaitingFixing | N | Y | N | CASE WHEN EXISTS (select pay.M_FLOW_ID from EST_FMRP_DBF EST, FXNG_DBF F where pay.M_TRN_REF = EST.M_NB and pay.M_VALUE_DATE = EST.M_F_VALUE and pay.M_CURRENCY=EST.M_F_CURRENCY and F.M_TRN_NUMBER = EST.M_NB and F.M_CALC_END = EST.M_F_CCFRMCD2 and F.M_LEG = EST. M_F_LEG and F.M_FIRST_FXNG = 0) THEN 'Y' ELSE 'N' END AS 'M_WAIT_FIX' | To Calculate | |

# Business Formula & Rule

- Formula_CashflowID: ```java Set prefix = ' M0' -- Init the prefix --get payment flow id from MxML or batch file murexFlowId=getMxML('/MxPayML/flowID') --e.g. the flow id is '87755146' If the length(murexFlowId) <10 then murexFlowId = '0' + murexFlowId -- e.g. if the murexFlowId length is 8 then we need to add '00' as prefix. -- Concact the prefix with the murexFlowId murexFlowId= prefix + murexFlowId -- if muurex sent the flow aid as 87755146, then the final cashflow id would be M00087755146 ```

# Scenarios