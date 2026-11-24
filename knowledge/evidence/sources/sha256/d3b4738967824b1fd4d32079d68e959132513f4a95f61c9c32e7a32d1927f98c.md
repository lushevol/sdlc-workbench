## 1. Functional Changes

| No | Object | | Name | Details | Comment |
| --- | --- | --- | --- | --- | --- |
| 1 | Staging Table | | SCB_FMRP_DBF | | M_FLOW_ID | numeric(10,0) | murex cashflow id | | --- | --- | --- | | M_STATUS | char(4) | murex cashflow status INIT/SENT/MATH/CANC | | M_RATAN_ID | char(12) | Ratan cashflow id | | M_RATAN_NET_ID | char(12) | Ratan net resultant id when cashflow got net in Ratan, otherwise value 0 | | M_INS_DATETIME | datetime | cashflow record insertion timestamp | | M_ACK_DATETIME | datetime | murex receive Ratan ACK message timestamp | | M_RLS_DATETIME ** ** | datetime | murex receive Ratan RELEASE message timestamp | | M_PUB_DATETIME | datetime | murex send out message timestamp | | DB Change |
| M_FLOW_ID | numeric(10,0) | murex cashflow id |
| M_STATUS | char(4) | murex cashflow status INIT/SENT/MATH/CANC |
| M_RATAN_ID | char(12) | Ratan cashflow id |
| M_RATAN_NET_ID | char(12) | Ratan net resultant id when cashflow got net in Ratan, otherwise value 0 |
| M_INS_DATETIME | datetime | cashflow record insertion timestamp |
| M_ACK_DATETIME | datetime | murex receive Ratan ACK message timestamp |
| M_RLS_DATETIME ** ** | datetime | murex receive Ratan RELEASE message timestamp |
| M_PUB_DATETIME | datetime | murex send out message timestamp |
| 2 | Static Table | | **FMRP_ENTITY_DBF** | **M_ENTITY char (16)** | |
| 3 | Stored Procedure | | scb_payfmrp | | insert the eligible payment flow into Staging Table |
| 4 | Payment Status | | SNTR RLSR | don't send any accounting entry | |
| 5 | Data Publisher (payment validation) | | PAY_VALID | ((Status(Dest) = 'SENT' and Status(Src) = 'CHCK' and Trn-Group != 'LFUT' and Trn-Group != 'SFUT')) or (((Status(Dest) = 'SENT' and Status(Src) = 'STP'))) or (((Trn-Type = 'XSW' or Trn-Type = 'FXD')) and (Flow Type0 = 'CAP' and Flow Type1 = 'XIT' and MOPID != '0.000000' and Status(Dest) = 'SENT' and Status(Src) = 'CHCK' and Trn-Group = 'FXD')) or ((Key = 'US2I')) or ((((Status(Dest) = 'CNET' and Status(Src) = 'INIT')) or ((Status(Dest) = 'INIT' and Status(Src) = 'CNET')) or ((Status(Dest) = 'SNTR' and Status(Src) = 'INIT')) or ((Status(Dest) = 'INIT' and Status(Src) = 'SNTR')))) | |
| 6 | Payment Q | | FAIS | RQWHERE("PAY_FLOW_DBF.M_FLOW_ID in (select M_FLOW_ID from TEMP_SCB_FMRP_DBF where M_STATUS='INIT')","") | Auto INIT 2 SNTR |
| 7 | Payment Q | | ~~FACR~~ | ~~RQWHERE("PAY_FLOW_DBF.M_FLOW_ID in (select M_FLOW_ID from SCB_FMRP_DBF where M_STATUS='MACH')","")~~ | ~~Auto CNET 2 RLSD~~ |
| 8 | Payment Q | | FMIS | Fill: TRN_ID>0 .AND.VALUE_DATE>=^D,VALUE-DATE:,VALUE-DATE^ .AND.CNTRP==^C15,COUNTERPARTY:,^ Show: TRN_ID>0 .AND.VALUE_DATE>=CTOD("00000000") .AND.CNTRP=="" | Manual INIT 2 SNTR |
| 9 | Payment Q | | FMSI | Fill: VALUE_DATE>=^D,VALUE-DATE:,VALUE-DATE^ .AND.CNTRP==^C15,COUNTERPARTY:,^ .AND.RQWHERE("PAY_FLOW_DBF.M_FLOW_ID in (select M_FLOW_ID from SCB_FMRP_DBF where M_STATUS='SENT')","") Show: VALUE_DATE>=CTOD("00000000") .AND.CNTRP=="" .AND.RQWHERE("PAY_FLOW_DBF.M_FLOW_ID in (select M_FLOW_ID from SCB_FMRP_DBF where M_STATUS='SENT')","") | Manual reverse SNTR 2 INIT |
| 10 | Processing shell | | PAY_FMRP_PRE | | Auto insert eligible trade into Staging table |
| 11 | Processing Script | | PAY_FMRP_STP | FAIS | Auto trigger the payment Status |
| 12 | Data Publisher (payment insertion) | Modify | POS_DATA_PUBLISHER->PAY_INS_ND->PAY_INS_NDF | ![image2022-12-13_16-44-7.png](attachments/image2022-12-13_16-44-7.png) **fmrpConstrain_Scope** DBCOUNT("FMRP_ENTITY","M_ENTITY='"+{Entity}+"'") **fmrpConstrain_VD** IIF({Value Date}<=DT_SKIP(DENV('DATE_SYS'),'+9D','LONBOX'),1,0).AND.{Value Date}>=DENV('DATE_SYS'),1,0) | DATE skip following calendar LONBOX |
| 13 | Payment Q | | I2SR | | No filter, for workflow |
| 14 | Stored Procedure | Modify | sp_pre_stp | -- skip the processing of those flows that will flow to FMRP AND (not exists (select 1 from MUREXDB.FMRP_ENTITY_DBF where A.M_ENTITY=M_ENTITY) or ( exists(select 1 from MUREXDB.FMRP_ENTITY_DBF where A.M_ENTITY=M_ENTITY) and (exists(select 1 from MUREXDB.TABLE#DATA#CURRENCY_DBF where (B.M_BRW_NOMU1=M_LABEL or B.M_BRW_NOMU2=M_LABEL or B.M_BRW_ODNC0=M_LABEL or B.M_BRW_ODNC1=M_LABEL) and M_BUL_CUR_FL='Y') OR exists(select 1 from MUREXDB.TABLE#DATA#CURRENCY_DBF where (substring(B.M_INSTRUMENT,1,3))= M_LABEL and M_BUL_CUR_FL='Y') OR exists(select 1 from MUREXDB.TABLE#DATA#CURRENCY_DBF B where A.M_CURRENCY=B.M_LABEL and B.M_NDF_CCY='Y') OR ( A.M_TRN_GRP = 'FXD' and A.M_STRATEGY <>'FEDSVALIDATOR' and (A.M_STRATEGY<>'FX_DCD' or C.M_CLASSIFY='INTERNAL') and A.M_TYPOLOGY NOT IN('NDF','NDS Fixing') ) ) ) ) | Due to the Production sp_check_auto_netting.sql missing schema, so need to modify, and recreate sp_nstp_reason sp_insert_stp |
| 15 | Payment Q | | S2RR | | No filter, for workflow |
| 16 | Payment Q | | FMRO | RQWHERE("PAY_FLOW_DBF.M_FLOW_ID in (select M_FLOW_ID from SCB_FMRP_DBF where M_STATUS='SENT')","") | For One time rollback purpose.(CPT code) |
| 17 | Payment Query Filter | | **FMRP Cashflow Monitor** | RQWHERE("PAY_FLOW_DBF.M_FLOW_ID in (select M_FLOW_ID from SCB_FMRP_DBF)","") .AND.VALUE_DATE>=^D,FROM_VALUE_DATE,FROM_VALUE_DATE^ .AND.VALUE_DATE<=^D,TO_VALUE_DATE,FROM_VALUE_DATE^ | User Monitor |
| 18 | Payment Viewer | | FMRP Cashflow Basic | | User Monitor |
| 19 | Static Data | Modify | TABLE#LIST#HRDBLKUS_DBF | enrich 27 entity profile to this table | |
| 20 | consistency Rule | Modify | NoMKTOP on Fut. Flow | **isFutValdate** IIF(DBCOUNT("PAY_FLOW_DBF","M_STATUS in ('SENT','INV','NET',**'RLSR'**) AND M_VALUE_DATE > '"+DTOC({Header->Date})+"' AND M_TRN_ID ="+STR({Header->Origin-Trn#}) )>0,0,1) | |
| 21 | Static Data | Modify | TABLE#LIST#PAY_SUPP_DBF | remove related CN entity's data | descope CN eligible cashflow from Auto Supprise Process |
| 22 | DB View | Modify | SCB_VW_PAY_INIT_TO_SUPP | ( ( exists(select 1 from MUREXDB.FMRP_ENTITY_DBF where T1.M_ENTITY=M_ENTITY) and (exists(select 1 from MUREXDB.TABLE#DATA#CURRENCY_DBF where (T3.M_BRW_NOMU1=M_LABEL or T3.M_BRW_NOMU2=M_LABEL or T3.M_BRW_ODNC0=M_LABEL or T3.M_BRW_ODNC1=M_LABEL) and M_BUL_CUR_FL='Y') OR exists(select 1 from MUREXDB.TABLE#DATA#CURRENCY_DBF where (substring(T3.M_INSTRUMENT,1,3))= M_LABEL and M_BUL_CUR_FL='Y') OR exists(select 1 from MUREXDB.TABLE#DATA#CURRENCY_DBF where T1.M_CURRENCY=M_LABEL and M_NDF_CCY='Y') OR ( T1.M_TRN_GRP = 'FXD' and T1.M_STRATEGY <>'FEDSVALIDATOR' and (T1.M_STRATEGY<>'FX_DCD' or T4.M_CLASSIFY='INTERNAL') and T1.M_TYPOLOGY NOT IN('NDF','NDS Fixing') ) ) ) or not exists(select 1 from MUREXDB.FMRP_ENTITY_DBF where T1.M_ENTITY=M_ENTITY) ) | descope CN eligible cashflow from Auto Supprise Process |
| 23 | Control M | | | 1. FMRP Daily job 2. SCB_FMRP_DBF Monthly purge | |
| 24 | Static Data | Modify | TABLE#LIST#PAYSTP_M_DBF | select * from TABLE#LIST#PAYSTP_M_DBF T1,FMRP_ENTITY_DBF T2 WHERE T1.M_ENTITY=T2.M_ENTITY TABLE#LIST#PAYSTP_M_DBF.M_PAYMODULE = **N** | CN Payment STP Stop 1 week |

## 2. Workflow Changes

### Workflow Task & Formula Dictionary

<u>*[CN Settlement - Murex 2.11 workflow change]*</u>

### MQ Connectivity

For Dev/Testing we use murex existing UAT MQ, but go live Program will apply for new MQ. Totally 2 MQ is required for inbound and outbound.

| Env | I/O | Murex MQ Config | MLS Config |
| --- | --- | --- | --- |
| DEV | Murex->RATAN | Host 10.198.198.93 Port 8212 Channel UKMXGCLNTS2 Queue manager UKFM02S1 Queue GM.MXG.MLS.FEDS.UAT User ukmxgmq | ibmmq.hostname=[ukswiclnts1.chl.mq.ibm.com](http://ukswiclnts1.chl.mq.ibm.com) ibmmq.port=8212 ibmmq.channel=UKSWICLNTS1 ibmmq.queueManager=UKFM02S1 ibmmq.username=swiop ibmmq.password= ibmmq.CCSID=819 ibmmq.SSLCipherSuite=TLS_RSA_WITH_AES_256_CBC_SHA256 ibmmq.sslEnable=true ibmmq.sslTrustFile=/appmls/coordinator/sha2-certs_new/swapswire.jks ibmmq.sslKeyStoreFile=/appmls/coordinator/sha2-certs_new/swapswire.jks GM.MXG.MLS.FEDSIN.UAT |
| DEV | RATAN→Murex (We shared UAT MQ with FXDC, so before testing need to make sure MXG_QUANT PCT_STP FXDC inbound MQ is stopped.) | Host 10.193.106.152 Port 1414 Channel UKMXGCLNTS1 Queue manager UKIG01S2 Queue GMPCI.MLS.MXG.RQSTIN User ukmxgmq | mlsmq.hostname=10.193.106.152 mlsmq.port=1414 mlsmq.channel=UKMLSCLNTS1 mlsmq.queueManager=UKIG01S2 mlsmq.username=ukmlsmq mlsmq.password= |

### MQ Connectivity

| Env | I/O | Murex MQ Config | Config |
| --- | --- | --- | --- |
| DEV | Murex→RATAN (Outbound MQ) | Host 10.198.198.93 Port 8212 Channel UKMXGCLNTS2 Queue manager UKFM02S1 Queue CF.MXG.RATAN.RQST User ukmxgmq | ![image2023-3-9_15-54-9.png](attachments/image2023-3-9_15-54-9.png) |
| DEV | RATAN→Murex (Inbound MQ) | Host 10.198.198.93 Port 8212 Channel UKMXGCLNTS2 Queue manager UKFM02S1 Queue CF.RATAN.MXG.RESPIN User ukmxgmq | ![image2023-3-9_15-47-54.png](attachments/image2023-3-9_15-47-54.png)![image2023-3-9_15-50-18.png](attachments/image2023-3-9_15-50-18.png) CIPHERSUITE=TLS_RSA_WITH_AES_256_CBC_SHA256 PEER VALUE = CN=*ukfm02s1 |

### Reverse Message Template (Ratan→Murex)

##### <u>***ACK Message - RATAN publish once murex cashflow is received in RATAN***</u>

| <?xml version="1.0" encoding="UTF-8"?> | |
| --- | --- |
| **<MxPayMLResponse>** | XML Root |
| ** <sourceSystem>**RATAN**</sourceSystem>** | hardcode RATAN |
| ** <objectNature>**cashflow**</objectNature>** | hardcode cashflow |
| ** <timestamp>**2003-11-26 17:09:35**</timestamp>** | Ratan ack-ed timestamp, format **yyyy-MM-dd hh:mm:ss** |
| ** <sourceID>**M00087755146**</sourceID>** | char(12), corresponding flow id in RATAN |
| ** <event>**New**</event>** | corresponding event in RATAN For murex amendment | murex id | murex flow type | ratan id | ratan event | | --- | --- | --- | --- | | 87755146 | original flow | M00087755146 | New | | 87755147 | reverse flow | M00087755146 | Withdrawal | | 87755148 | amended flow | M00087755148 | New | |
| murex id | murex flow type | ratan id | ratan event |
| 87755146 | original flow | M00087755146 | New |
| 87755147 | reverse flow | M00087755146 | Withdrawal |
| 87755148 | amended flow | M00087755148 | New |
| ** <result>**success**</result>** | RATAN process result, success to Ack. failed to Nack |
| ** <message>**RATAN Acknowledged**</message>** | if success then return **RATAN Acknowledged** if failed then return** Fail Reason** |
| ** <MXG2000>** | |
| ** <flowID id="flow_87755146">**87755146**</flowID>** | Murex flow id, this tag should have attribute id="flow_<murex flow id>" |
| ** </MXG2000>** | |
| **</MxPayMLResponse>** | |

##### <u>***Release Message - RATAN publish once cashflow is released or directly settled in RATAN***</u>

| <?xml version="1.0" encoding="UTF-8"?> | |
| --- | --- |
| **<MxPayMLResponse>** | XML Root |
| ** <sourceSystem>**RATAN**</sourceSystem>** | hardcode RATAN |
| ** <objectNature>**cashflow**</objectNature>** | hardcode cashflow |
| ** <timestamp>**2003-11-26 17:09:35**</timestamp>** | Ratan 'released' timestamp, format **yyyy-MM-dd hh:mm:ss** |
| ** <sourceID>**N00000000001**</sourceID>** | char(12), RATAN Flow id. For Gross settle, it will be Ratan Gross flow id(corresponding flow id in RATAN). for NET/CPN settle, it will be ratan NET **resultant **flow id. |
| ** <event>**Released**</event>** | Return 'Released' for RELEASE message |
| ** <result>**success**</result>** | RATAN process result, success |
| ** <message>**RATAN Released**</message>** | if success then return **RATAN Released** |
| ** <MXG2000>** | |
| ** <flowID id="flow_87755146">87755146</flowID>** | Murex flow ids. this tag should have attribute id="flow_<murex flow id>" For Gross there will be only one cashflow id tag. For NET/CPN there will be multiple tags which should be all murex cashflow ids belong to same NET process。 |
| ** <flowID id="flow_87755147">87755147</flowID>** |
| ** ...** |
| ** </MXG2000>** | |
| **</MxPayMLResponse>** | |

### Message Template (Murex→Ratan)

##### <u>***ACK Message - Murex publish once murex released cashflow is received in Murex***</u>

| <?xml version="1.0" encoding="UTF-8"?> | |
| --- | --- |
| **<MxPayMLResponse>** | XML Root |
| ** <sourceSystem>**MUREX**</sourceSystem>** | hardcode MUREX |
| ** <objectNature>**cashflow**</objectNature>** | hardcode cashflow |
| ** <timestamp>**2003-11-26 17:09:35**</timestamp>** | Murex ack-ed timestamp, format **yyyy-MM-dd hh:mm:ss** |
| ** <sourceID>**M00087755146**</sourceID>** | char(12), corresponding flow id in RATAN |
| ** <event>**New**</event>** | corresponding event in Murex |
| ** <result>**success**</result>** | Murex process result, success(ACK) or failed (NACK) |
| ** <message>**MUREX Acknowledged**</message>** | if success then return **MUREX Acknowledged** if failed then return failed reason |
| ** <MXG2000>** | |
| ** <flowID id="flow_87755146">**87755146**</flowID>** | Murex flow id, this tag should have attribute id="flow_<murex flow id>" |
| ** </MXG2000>** | |
| **</MxPayMLResponse>** | |

## 3. Technical Exception Handling

| Type | Exception Scenario | Cause | Capture | Owner | Handle Process |
| --- | --- | --- | --- | --- | --- |
| System Outbound | Murex published, RATAN not displayed | message crash in murex workflow | immediately captured by workflow error queue | Murex PSS | treat as prod workflow issue, PSS follow BAU support process |
| System Outbound | Murex published, RATAN not displayed | MQ issue | Recon report | RATAN | RATAN will design recon rule based on Recon report sent from Murex2.11. If break identified, user can user manual queue SNTR→INIT. then re-trigger publishing to RATAN by auto job or manual queue INIT->SNTR. |
| System Outbound | Murex published, RATAN not displayed | message crash in RATAN workflow | | RATAN | |
| System Inbound | RATAN response, murex not sync | message crash in RATAN workflow | | RATAN | |
| System Inbound | RATAN response, murex not sync | MQ issue | Recon report | | RATAN will design recon rule based on Recon report sent from Murex2.11 If break identified, RATAN to replay response message to murex. |
| System Inbound | RATAN response, murex not sync | message crash in murex workflow | immediately captured by workflow error queue | Murex PSS | treat as prod workflow issue, PSS follow BAU support process |

## 4. Murex Ringfence Cashflow to RATAN

We have got generic approach for all entities and all product. Refer to <u>**</u>

If murex trade meet the conditions

1. Entity in scope **EXPAND: Entity in Scope** | BEIJING | | --- | | CHANGSHA | | CHENGDU | | CHINA HO | | CHONGQING | | DALIAN | | FOSHAN | | FT2 SHA | | FUZHOU | | GUANGZHOU | | HHANGZHOU | | HOHHOT | | JINAN | | KUNMING | | NANJING | | NINGBO | | NNCHANG | | QINGDAO | | SHANGHAI | | SHENZHEN | | SHYANG | | SUZHOU | | TIANJIN | | WUHAN | | XIAMEN | | XXIAN | | ZHUHAI | **EXPAND_END**
2. Have cashflow containing precious metal currency

Then trade is treated as ‘precious metal deal’, and all cashflow under this trade should continue settled from Mx2.11. Otherwise will send to Ratan.

## 6. Murex Extra Tag Enrichment

| | Extra Tag Label | Desc | Logic |
| --- | --- | --- | --- |
| 1 | <publicationDateTime> | Message generation timestamp | |
| 2 | <validationLevel> | Trade validation status | VAL_STATUS |
| 3 | <entityFMID> | entity FMID | Entity_SCI_FMID Entity_SCI_LEID select rtrim(M_ATLAS_LEID ) 'LEID', rtrim(M_SCI_ID) 'SCIID' from TABLE#DATA#COUNTERP_DBF c, TABLE#DATA#ENTITY_DBF e where c.M_LABEL = e.M_CTP_COD and e.M_LABEL = 'MxCTX#NAME#Mx' |
| 4 | <entityLEID> | entity LEID |
| 5 | <counterpartyFMID> | counterparty FMID | select rtrim( M_ATLAS_LEID ) M_ATLAS_LEID from TABLE#DATA#COUNTERP_DBF b where b.M_LABEL='MxCTX#NAME#Mx |
| 6 | <portBizUnit> | portfolio biz unit | TABLE#DATA#PORTFOLI_DBF.M_BIZ_UNIT |
| 7 | <traderID> | trader | TRN_HDR_DBF.TRADER |
| 8 | <amendmentFlag> | Y/N Y means cashflow is part of amendment. | **IF **cashflow comment contain 'reverse' **THEN **Y **ELSE IF** MKT_OP_DBF.M_DEST_NB = cashflow.TRN_ID and Mktops Type in (RPL,RPL_M) **THEN **Y **ELSE **N |
| 9 | <action> | action | PAY_FLOW_DBF.M_ACTION |
| 10 | <tradeLastMKT> | trade last market Operation 1: EXR 2: EXP 3: XIT 4: NET 5: RPL 6: RPL_M 7: RPL_D | SELECT CASE WHEN M_MOP_LAST > 0 THEN M_MOP_LAST ELSE M_MOP_CREAT END AS 'M_MOP' FROM MUREXDB.TRN_HDR_DBF WHERE M_NB=MxCTX#NB#Mx |
| 11 | <TrnParentID> | trade parent id | select convert(varchar(10), M_CREATOR) ,convert(varchar(10), CASE WHEN M_MRPL_ONB<1 THEN M_NB ELSE M_MRPL_ONB END) from MUREXDB.TRN_HDR_DBF where M_NB=MxCTX#NB#Mx |
| 12 | <TrnOrginalID> | trade orginal id |
| 13 | <flow> | related cashflow for trade | SELECT 'Flowid:'+convert(varchar(10), M_FLOW_ID)+', status:'+M_STATUS+', value_date:'+convert(varchar(10), M_VALUE_DATE,112) , '1' --SELECT convert(varchar(10), M_FLOW_ID),M_STATUS,convert(varchar(10), M_VALUE_DATE,112) FROM MUREXDB.PAY_FLOW_DBF WHERE M_TRN_REF=MxCTX#tradeRef#Mx |
| 14 | <mxSystemDate> | MX System Date | TRN_PC_DBF.M_DATE |

## 7. High Level Tech Design

| **We will combine 'Regular Approach' and 'Real-time Approach' together within Murex** ***<u>Regular Approach (every 2 hours)</u>*** **Process Scope:** VD -7 **Change Details:** 1. Control M job1 Query every 2 hours and populate in staging table 2. Control M job2 move status INIT->SNTR based on staging table 3. INIT->SNTR status movement will trigger 'validation' message for SNTR cashflow to RATAN. 4. Workflow sync status back to staging table ***<u>Real-time Approach</u>*** **Process Scope:** VD -7 **Change Details:** 1. Enhance payment data publisher, which will trigger real-time message upon cashflow insertion(INIT status). Data publisher criteria would be like VD=T Entity=China etc. Note this is 'Insertion' message for INIT cashflow and won't send to RATAN. 2. Workflow real-time move status INIT->SNTR Step 3 and Step 4 is same as regular approach, they share same workflow tasks and formula. <u>***Real-time Approach feasibility* **</u> has been tested for below scenario a.Trade booking generate INIT cashflow - send to RATAN - expected b.Trade amendment generate INIT cashflow - send to RATAN - expected c.Fixing generate INIT cashflow - send to RATAN - expected d.Payment queue move status from XXX->INIT - NOT send to RATAN – expected ***<u>Real-time Approach (Data publisher for payment insertion) performance impact</u>*** PAY FIX Impact: | Object to be Tested | Dataset Volume | Pre Runtime | Post Runtime | Diff | Test Evidence | % Delay | | --- | --- | --- | --- | --- | --- | --- | | PAY FIX Procedure | Same as monthly Pay fix run | 16H 58mins | 17H 7mins | 9min | | 0.8% | | Data Publisher | China daily VD-7 cashflows | 47min 58s | 50min 47s | 2min 49s | | 5.87% | |
| --- |
| Object to be Tested | Dataset Volume | Pre Runtime | Post Runtime | Diff | Test Evidence | % Delay |
| PAY FIX Procedure | Same as monthly Pay fix run | 16H 58mins | 17H 7mins | 9min | | 0.8% |
| Data Publisher | China daily VD-7 cashflows | 47min 58s | 50min 47s | 2min 49s | | 5.87% |

## 8. RATAN Logic to process murex amendment

Murex → Ratan Mxml-SCBML Adaptor → Ratan

Ratan Mxml-SCBML Adaptor is a middle layer dedicated build for transfer Mxml to SCBML before feeding to Ratan. Going forward once murex decom it will be removed.  Adaptor Detail: [Ratan MxML->SCBML Adaptor - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/Ratan+MxML-%3ESCBML+Adaptor)

| Murex flow id-> | RATAN MxML-SCBML Adaptor -> | RATAN Display | RATAN ->LMS | RATAN ->RAZOR |
| --- | --- | --- | --- | --- |
| 01 - original | Ratan cashflow id: M00+01 Event Type: New Flow Version: 0 | id=M0001, eventType=New, version 0, status=QUEUED | Send flow=01, eventtype=New | Send flow=01, eventtype=New |
| 02 - reverse of 01 | Ratan cashflow id: M00+01 Event Type: Withdrawal Flow Version: 1 | id=M0001, eventType=Withdrawal, version 1, status=CANCELLED (Ratan DB will record version 0 and 1, but GUI will show latest version, user in GUI not able to see version, user will see latest status is being Withdrawal, meaning this flow is Cancelled) | Ratan will further check if 01 has sent to LMS, then will send 02 (flow id 01, eventtype= withdrawl) to LMS. if 01 has not send to LMS, then both 01 and 02 will be filtered and NOT send to LMS, because 01 is regard as 'cancelled' in Ratan | if 01 is 'settled', send 02 (flow id 01, eventtype= withdrawl) to RAZOR if 01 status is not 'settled', then both 01 and 02 won't send to Razor, because 01 is regard as 'cancelled' in Ratan |
| 03 - correction | Ratan cashflow id: M00+03 Event Type: New Flow Version: 0 | id=M0003, eventType=New, version 0, status=QUEUED Ratan identify this is correction flow (Refer to Rule 9), then set is as NSTP for user intervation. user is responsible to decide whether/when 03 is send to Ratan for settelement | Send flow=03, eventtype=New | Send flow=03, eventtype=New |