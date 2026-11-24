| Version | Author | **Description of Change** |
| --- | --- | --- |
| 1.0 | 2023-11-01 | Initial version - FMRP CN Settlement |
| 1.1 | 2024-06-06 | Revise version - Blue font is update for FMRP SG IN KL Settlement migration |

# Background

Today settlement ops perform cross-product netting across multi desks in Murex G2000. As part of Murex G2000 decommission, RATAN will be the place to perform CPN in the target state.  This is phased program so our design need to support cross product netting when specific desks are migrated to strategic system by phase within the same entity. i.e. For China entity, cash flow for Rates desk generated from strategic system when remaining desks are in Murex G2000.

# Data Flow Chart

![](https://confluence.global.standardchartered.com/download/attachments/2480743195/High-level%20Flow.png?version=31&modificationDate=1672993447000&api=v2)

## Global Role Mapping

| Hub/Team | Activities Handled |
| --- | --- |
| CN: [GBSDerivSettsGCNA@sc.com](mailto:GBSDerivSettsGCNA@sc.com) **SG: **[GBSDerivSetts.SIN@sc.com](mailto:GBSDerivSetts.SIN@sc.com) **MY: **[GBSDerivSetts.SIN@sc.com](mailto:GBSDerivSetts.SIN@sc.com) **IN: **[Sett_INDerivatives@sc.com](mailto:Sett_INDerivatives@sc.com) | Payment validate Operation |

# Purpose/Objectives

This section aims to provide a comprehensive information on activities performed to meet the following purpose/objectives:

1. 1. Process around the MX2.11 Payment Message flow to Ratan & Ratan reverse ACK/ RELEASED Message 2. Monitor target cashflow flowing behavior. 3. Exception handling

# Scope

## In Scope (Ratan Eligible)

- **EXPAND: RATAN Eligible Entity** > **INFO** > SCB_ENTITY_DBF used to save below M_LABEL (Entity Name). > > For this Project, the data of CN Entity would not be changed. > > Any Amendment need to raise change ticket. | M_LABEL | M_CTP_COD | M_EBBS | M_ENTITY_TYP | M_FEDS_ENT | M_PAY_HUB | | --- | --- | --- | --- | --- | --- | | BEIJING | SCB/BEIJING | Y | subsidiary | CHN | CHINA | | NANJING | SCB/NANJING | Y | subsidiary | CHN | CHINA | | TIANJIN | SCB/TIANJIN | Y | subsidiary | CHN | CHINA | | ZHUHAI | SCB/ZHUHAI | Y | subsidiary | CHN | CHINA | | SHANGHAI | SCB/SHA | Y | subsidiary | CHN | CHINA | | XIAMEN | SCB/XIA | Y | subsidiary | CHN | CHINA | | SHENZHEN | SCB/SHENZHEN | Y | subsidiary | CHN | CHINA | | GUANGZHOU | SCB/GUANGZHOU | Y | subsidiary | CHN | CHINA | | SUZHOU | SCB/SUZHOU | Y | subsidiary | CHN | CHINA | | CHENGDU | SCBCHENGDU/CGD | Y | subsidiary | CHN | CHINA | | QINGDAO | SCB/QDO | Y | subsidiary | CHN | CHINA | | CHONGQING | SCBCNCQG/CQG | Y | subsidiary | CHN | CHINA | | HHANGZHOU | SCBCNHANGZH/HNZ | Y | subsidiary | CHN | CHINA | | NNCHANG | SCBCHINANAN/NCG | Y | subsidiary | CHN | CHINA | | DALIAN | SCBCHINADAL/DLN | Y | subsidiary | CHN | CHINA | | NINGBO | SCBCHNIBR/NGB | Y | subsidiary | CHN | CHINA | | HOHHOT | SCBCHHOBR/HHH | Y | subsidiary | CHN | CHINA | | XXIAN | SCBLXIAN/XIN | Y | subsidiary | CHN | CHINA | | FOSHAN | SCBCNFOSBR/FOS | Y | subsidiary | CHN | CHINA | | JINAN | SCBCNJNABR/JNA | Y | subsidiary | CHN | CHINA | | CHANGSHA | SCBCNCHANG/CGS | Y | subsidiary | CHN | CHINA | | FUZHOU | SCBCNFUZHOU/FZH | Y | subsidiary | CHN | CHINA | | KUNMING | SCBCNKMG/KMG | Y | subsidiary | CHN | CHINA | | FT2 SHA | SCBSHAFTU/FT2 | Y | subsidiary | CHN | CHINA | | SHYANG | SCBCNSHY/SYG | Y | subsidiary | CHN | CHINA | | CHINA HO | SCBCNCHO/CHO | Y | subsidiary | CHN | CHINA | | WUHAN | SCBL/WUH | Y | subsidiary | CHN | CHINA | | ACU SING | SCBACU/SIN | Y | branch | SG | SOUTH EAST ASIA | | DBU SING | SCB/SIN | Y | branch | SG | SOUTH EAST ASIA | | SACU SING | SSCBACU/SIN | Y | subsidiary | SG | SOUTH EAST ASIA | | SDBU SING | SSCB/SIN | Y | subsidiary | SG | SOUTH EAST ASIA | | MUMBAI | SCB/MMB | Y | branch | MUM | EAST ASIA | | GIFTCITY | SCBGIFTCITY/MUM | Y | branch | GFT | EAST ASIA | | KLISLAMIC | ISLAMICKL/KUL | Y | | KL | SOUTH EAST ASIA | | KLUMPUR | SCB/KUL | Y | subsidiary | KL | SOUTH EAST ASIA | **EXPAND_END**
- Payment value date within **9** days

## Out of Scope (Ratan Non-Eligible)

- ~~Bullion CCY payment~~
- Non-Deliverable CCY payment for NDS Product,
- The payment's related trades already flow to Razor
- Amount =0

# Contact Person for Clarification on this DOI

Should there be any query regarding Settlement DOI, kindly contact Functional Lead as stated below.

| Functional Lead | PSID | Function Email | Function SharePoint/Bridge |
| --- | --- | --- | --- |
| Dinesh, Arockia | 1289935 | K.[A.Dinesh@sc.com](mailto:A.Dinesh@sc.com) | |
| | | | |

# Operational Risk Framework Processes

Not Applicable

# Document of Operating Instructions (DOI)

- **EXPAND: Auto Feed Cashflow to RATAN** 1. Login MX 2.11 2. The cashflows will be automatically sent to RATAN based on the booking in MX2.11. Sample trade below ![2023-09-13 17_20_44-Search.png](attachments/2023-09-13 17_20_44-Search.png) 3.System generate payment ![image2023-9-13_18-8-36.png](attachments/image2023-9-13_18-8-36.png) 4.The data publisher will automatically send the eligible payment Message to Ratan ![Ratan insert.png](attachments/Ratan insert.png) **EXPAND_END**
- **EXPAND: Manual Publish of Cashflow to RATAN** Below operation should not exceed 30 payments each time. 1. In case there is an issue with auto publish, there will be an automatic email notification to PSS & Ops users. In case of urgency, Settlement user can choose to manual publish cashflow to RATAN, User manually validate a payment from INIT to SNTR - Login MX 2.11 and select the correct Profile (GBL_DO_SET, GBL_DOS_1, GBL_DOS_2, GBL_DOS_3, GBL_DOS_4, GBS_IN_SET ) - Go to Payment → Payment Workflow -> FMRP:INIT2SNTR MAN ![image2023-3-24_15-4-0.png](attachments/image2023-3-24_15-4-0.png) - Fill the Value date and Counterparty ![INIT2SNTR_1.png](attachments/INIT2SNTR_1.png) - Select the Payment and Click 'Proceed' ![Manul Push Murex.png](attachments/Manul Push Murex.png) - The data publisher will automatically send a payment Message to Ratan ![Manual Push Ratan.png](attachments/Manual Push Ratan.png) 1. User manually change a payment from SNTR to INIT If user manually change payment from SNTR to INIT, then the payment could not trigger the auto process any more. User has to manually move it from INIT to SNTR to publish the cashflow to RATAN - Login MX 2.11 and select the correct Profile - Go to Payment → Payment Workflow ![image2023-3-24_15-48-51.png](attachments/image2023-3-24_15-48-51.png) - Fill the Value date and Counterparty ![SNTR2INIT_1.png](attachments/SNTR2INIT_1.png) - Select the Payment and Click 'Proceed' ![SNTR2INIT_2.png](attachments/SNTR2INIT_2.png) **EXPAND_END**
- **EXPAND: Auto Publish Sequencing** The Cashflow Publish Processing for future 9 days will be auto triggered via a batch flow - 110 payments on 00:00-17:00 GMT from Monday to Friday every 15min. Any new booking / amend for VD yesterday, today, tmr would be sent to RATAN via a separate real time flow. ![batch Ratan.png](attachments/batch Ratan.png) **EXPAND_END**
- **EXPAND: User Monitor** 1. Monitor Process There is an <u>**optional **</u>feature to monitor the CN Payment Status. The real-time ACK Process will be primary control for data flow between Murex and Ratan. Ops user will use TLM to do the END to END reconciliation. - Login MX 2.11 and select the correct Profile - Go to Payment → Payment query → Query payment table ![image2023-3-27_9-34-3.png](attachments/image2023-3-27_9-34-3.png) - select "User filter" → select **FMRP Cashflow Monitor** → Proceed ![image2023-3-27_9-35-39.png](attachments/image2023-3-27_9-35-39.png) - And then shows below screen, | Payment Status | Reason | Description | Issue or not | Contact Point | Action | | --- | --- | --- | --- | --- | --- | | INIT | - | Payment in scope but not triggered push Ratan process | N | Ops User | Two Choice: - User can manual pushes the data by **FMRP:INIT2SNTR MAN** - Waiting the auto process to publish the data to Ratan | | SNTR | - | Payment have already push to Ratan, but not Acknowledged in Ratan | Y | Ratan PSS | User need to wait 5 mins and refresh the window to check the payment status. If the Reason still empty, then need to contact Ratan PSS to identify the Root Cause. and follow the Exception Handling. | | SNTR | RATAN Acknowledged | Payment have already push to Ratan and Acknowledged in Ratan | N | - | - | | RLSR | RATAN Acknowledged | Payment settled in Ratan. | N | - | - | ![Picture1.png](attachments/Picture1.png) **EXPAND_END**
- **EXPAND: Exception handle** | Type | Exception Scenario | Handle Process | | --- | --- | --- | | System Outbound Connectivity Issue | Any MQ Connectivity Issue (example can be Disconnected or Slowness), which cause OLA break | PSS and OPS receive alert, Ops standard process is to wait for MQ recovery (SLA is 2 hours) Exception auto-resolves on MQ recovery… Where required, OPS to check Ratan blotter if payment received If yes, then false alert and no further action required by FMO. If no, Ops to check with Murex 2.11 PSS. In case of urgent payment manual payment via Oscar should be done <u>only if there is no risk of duplication</u> | | For MQ incident, MQ PSS team will send broadcast to impacted according to the incident severity / impact. MUREX PSS team will also notify business teams if there is impact to MUREX G2000 and its business. | | ~~NACK received from RATAN~~: ~~If ~~a~~ny mandatory attributes are missing, RATAN will send a NACK.~~ ~~This is to be built as an enhancement and R&R to be agreed between PSS & OPS.~~ Descope from 2024 H1: NACK workflow was discussed in context of scenario where mandatory payment attributes were missing in Cashflow sent to RATAN. This issue has not been observed in RATAN CN BAU flow (and also not observed cases within MX2.11 in prior years). If this happens, there will be an automated email alert sent to users, who can raise the issue to PSS. | | System Inbound Connectivity Issue | Any MQ Connectivity Issue (example can be Disconnected or Slowness), which cause OLA break | RATAN PSS will check with Murex PSS if the released request has been received and ack has been sent. If required, RATAN PSS to notify Settlement user can manually trigger 'Status WriteBack' to resend the status update to Murex2.11 | | System Issue | Application technical issue | Application PSS should monitor own issues, investigate root cause and notify stakeholders in time. | | System Issue | **Issue statement: ** there is one CN payment status is SNTR (means should send to RATAN) but discard in murex workflow. **Root cause:** Dev located the issue is murex workflow issue, but root cause could not be identified as the issue can not be replicated in dev env. **Handling:** This is rare case (only happen once) and Dev confirmed the issue won't applicable in H2 solution because in H2 there won't be any workflow process. Discussed with PO (Dinesh and Jons) and agreed enhancement in murex that if payment status is SNTR but Murex-Ratan publishing audit have no publishing timestamp recorded over 10 min against the timing when status changed to SNTR, murex will send alter email to ops. Issue context email: Handling agreement: [Murex 2.11 - RATAN Design agreements - FM re-platforming - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/FMRP/Murex+2.11+-+RATAN+Design+agreements) H1 Impediment item #1 | Ops will be notified by alert Email and follow existing BAU process to engage support team and PSS for investigation. | **EXPAND_END**
- **EXPAND: Payment Query for LIEN** Currently LIEN is placed at trade level and not sent to RATAN as part of Cashflow. A workaround has been agreed that Ops will check if there are any trades booked / updated with LIEN in MX2.11 To monitor any cashflows where LIEN has been placed in MX2.11, below query must be used (the logic sync to payment queue LIEN -INIT-INIT) 1. Create payment filter in production - Login MX 2.11 and select the correct Profile - Go to Payment → Payment query → Query payment table ![image2023-3-27_9-34-3.png](attachments/image2023-3-27_9-34-3.png) - select 'User filter' →click 'Filter' dropdown list → insert a new filter ![image2024-6-28_16-42-0.png](attachments/image2024-6-28_16-42-0.png) - Setup filter condition as below ![image2024-6-28_16-38-14.png](attachments/image2024-6-28_16-38-14.png) | RQWHERE("PAY_FLOW_DBF.M_FLOW_ID in (SELECT PF.M_FLOW_ID from ((((((MUREXDB.PAY_FLOW_DBF PF left join MUREXDB.TABLE#DATA#DEALIRD_DBF IRD on (PF.M_TRN_REF=IRD.M_NB)) left join MUREXDB.TABLE#DATA#DEALCURR_DBF CURR on (PF.M_TRN_REF=CURR.M_NB)) left join MUREXDB.TABLE#DATA#DEALCOM_DBF COM on (PF.M_TRN_REF=COM.M_NB)) left join MUREXDB.TABLE#DATA#DEALCRD_DBF CRD on (PF.M_TRN_REF=CRD.M_NB)) left join MUREXDB.TABLE#DATA#DEALSCF_DBF SCF on (PF.M_TRN_REF=SCF.M_NB)) left join MUREXDB.TABLE#DATA#PAYFLOW_DBF PUDT on (PF.M_FLOW_ID=PUDT.M_FLOW_ID)) where(IRD.M_LIEN_MONIT !='' or CURR.M_LIEN_MONIT !='' or COM.M_LIEN_MONIT !='' or CRD.M_LIEN_MONIT !='' or SCF.M_LIEN_MONIT !='') and PF.M_STATUS IN ('INIT','SNTR','RLSR') and PUDT.M_XLIEN_FLAG <>1 and PF.M_VALUE_DATE >= (select M_DATE from MUREXDB.TRN_PC_DBF) and PF.M_VALUE_DATE <= ( select dateadd(dd,7,M_DATE) from MUREXDB.TRN_PC_DBF))","") .AND.AMOUNT<>0.AND.(.NOT.("ALOC/"$CNTRP)).AND.VALUE_DATE>=DENV('DATE_BO').AND.CNTRP<>'CAASH/ROLL'.AND.TRN_GRP<>'SFUT'.AND.TRN_GRP<>'LFUT' | | --- | **EXPAND_END**

# Record Retention

- FMRP_ENTITY_DBF : Permanent. Any amendment about this table need to raise Change Ticket and join MX 2.11 Pre-Cab.
- SCB_FMRP_DBF : After the flow released in Ratan, data will be saved as value date within 1 Month. job FMRP_PURGE use to realize the function.

# Appendices

Not Applicable

# FMO Data Management Projects

Not Applicable

# Approval of DOI