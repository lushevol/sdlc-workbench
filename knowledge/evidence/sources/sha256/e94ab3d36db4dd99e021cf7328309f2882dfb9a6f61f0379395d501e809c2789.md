| Version | Author | **Description of Change** |
| --- | --- | --- |
| 1.0 | 2023-11-01 | Initial version - FMRP CN Settlement |
| 1.1 | 2024-06-06 | updated for FMRP SG IN KL Settlement migration |
| 2.0 | 2024-10-09 | Revised Version - Updated for SCAG entity |
| 2.1 | 2025-01-09 | Revised version - updated for LONDON and SSTL entities |
| 2.2 | 2025-05-12 | Revised version - updated for HK/TW/TH Entities |
| 2.3 | 2025-06-09 | Revised Version - Updated for SG/IN/MY re-model to UK publishing method |
| 2.4 | 2025-07-01 | Revised version - Updated CN entities to UK publishing method |
| 2.5 | 2025-08-04 | Revised version - Updated for Tranche 2 Entities |
| 2.6 | 2025-09-22 | Revised version - Updated for Tranche 3 Release |
| 2.7 | 2026-08-03 | Revised version - HAU currency to be Com flag as Y |

# Background

The SFRMP cash settlement migration project aims to decommission Murex 2.11 application for settlement processing function.

The payment information are still produced in Murex but they are sent to Ratan for processing, as long as the trades are still booked in Murex till the trade migration is completed.

# Data Flow Chart:

0 . Introduced 2 new payment status for SFMRP. **SNTR **indicates the payment is sent to RATAN, **RLSR **indicates payment is released via RATAN.

1 . Murex system checks whether the payment is RATAN eligible on regular basis.

2 . For those payments are RATAN eligible, Murex auto move the payment status from INIT to SNTR.

3 . For those payments are not RATAN eligible, Murex still provides the manual approach to send the cashflow to RATAN.  This design is mainly for: 1) Technical exception handling 2) Ad Hoc requirement

4. The payments in Ratan could be NET/GROSS and once the payments is **Released**, Ratan trigger notification to Murex that the payment status move from **SNTR **to **RLSR**

![FMRP_H2_FlowChart_v1.png](attachments/FMRP_H2_FlowChart_v1.png)

## Global Role Mapping

| Hub | Ops Team/DL | Activities Handled |
| --- | --- | --- |
| CN | [GBSDerivSettsGCNA@sc.com](mailto:GBSDerivSettsGCNA@sc.com) | Payment validate Operation |
| HK | [GBSDerivSettsGCNA@sc.com](mailto:GBSDerivSettsGCNA@sc.com) |
| SG | [GBSDerivSetts.SIN@sc.com](mailto:GBSDerivSetts.SIN@sc.com) |
| MY | [GBSDerivSetts.SIN@sc.com](mailto:GBSDerivSetts.SIN@sc.com) |
| TW | [GBSDerivSettsGCNA@sc.com](mailto:GBSDerivSettsGCNA@sc.com) |
| TH | [GBSDerivSetts.SIN@sc.com](mailto:GBSDerivSetts.SIN@sc.com) |
| INDIA | [Sett_INDerivatives@sc.com](mailto:Sett_INDerivatives@sc.com) |
| DE/UK | [DerivativesSett-CH@sc.com](mailto:DerivativesSett-CH@sc.com);[COMMSETT_CHENNAI@sc.com](mailto:COMMSETT_CHENNAI@sc.com); Kumar, Babu <Babu.Kumar@[sc.com](http://sc.com)>; Settlements, Commodity <Commodity.Settlements@[sc.com](http://sc.com)>; Thomas, David George |
| MU | GBS Deriv Setts SIN - [GBSDerivSettsSIN@sc.com](mailto:GBSDerivSettsSIN@sc.com) |
| UAE | Commodity Derivs Sett-KL [CommodityDerivsSett-KL@sc.com](mailto:CommodityDerivsSett-KL@sc.com) [DerivativesSett-CH@sc.com](mailto:DerivativesSett-CH@sc.com) |
| ID | GBS Deriv Setts SIN - [GBSDerivSettsSIN@sc.com](mailto:GBSDerivSettsSIN@sc.com) |
| PH | GBS Deriv Setts SIN - [GBSDerivSettsSIN@sc.com](mailto:GBSDerivSettsSIN@sc.com) |
| JP | [GBSDerivSettsGCNA@sc.com](mailto:GBSDerivSettsGCNA@sc.com) |
| SA | [DerivativesSett-CH@sc.com](mailto:DerivativesSett-CH@sc.com) |
| DIFC | Commodity Derivs Sett-KL [CommodityDerivsSett-KL@sc.com](mailto:CommodityDerivsSett-KL@sc.com) , [DerivativesSett-CH@sc.com](mailto:DerivativesSett-CH@sc.com) |
| US | [DerivativesSett-CH@sc.com](mailto:DerivativesSett-CH@sc.com) |
| **JERSEY** | <u>[DerivativesSett-CH@sc.com](mailto:DerivativesSett-CH@sc.com)</u> |
| **OMAN** | <u>[DerivativesSett-CH@sc.com](mailto:DerivativesSett-CH@sc.com)</u> |
| **BAHRAIN** | <u>[DerivativesSett-CH@sc.com](mailto:DerivativesSett-CH@sc.com);Commodity Derivs Sett-KL [CommodityDerivsSett-KL@sc.com](mailto:CommodityDerivsSett-KL@sc.com)</u> |
| **BOTSWANA** | <u>[DerivativesSett-CH@sc.com](mailto:DerivativesSett-CH@sc.com)</u> |
| **COTEDIVOIR** | <u>[DerivativesSett-CH@sc.com](mailto:DerivativesSett-CH@sc.com)</u> |
| **BANGLADESH(DHAKA)** | Morshed, Golam; Niloy, Nehabul Haque; Arifuzzaman, Abu Mohammad |
| **QATAR(DOHA)** | <u>[DerivativesSett-CH@sc.com](mailto:DerivativesSett-CH@sc.com);Commodity Derivs Sett-KL [CommodityDerivsSett-KL@sc.com](mailto:CommodityDerivsSett-KL@sc.com)</u> |
| **SRI LANKA** | FMO_LK [FMO_LK@exchange.standardchartered.com](mailto:FMO_LK@exchange.standardchartered.com); Wickramatunge, Thushara [Thushara.Wickramatunge@sc.com](mailto:Thushara.Wickramatunge@sc.com); Joseph, Chrishani Rebekah [Chrishani.Joseph@sc.com](mailto:Chrishani.Joseph@sc.com); Perera, Peshala [Peshala.Perera@sc.com](mailto:Peshala.Perera@sc.com) |
| **GHANA** | <u>[DerivativesSett-CH@sc.com](mailto:DerivativesSett-CH@sc.com)</u> |
| **VIETNAM(HANOI)** | GBS Deriv Setts SIN - <GBSDerivSettsSIN@[sc.com](http://sc.com) |
| **IRAQ** | <u>[DerivativesSett-CH@sc.com](mailto:DerivativesSett-CH@sc.com)</u> |
| **PAKISTAN(KARACHI)** | GBS Deriv Setts SIN - <GBSDerivSettsSIN@[sc.com](http://sc.com) |
| **KENYA** | <u>[DerivativesSett-CH@sc.com](mailto:DerivativesSett-CH@sc.com)</u> |
| **NIGERIA** | <u>[DerivativesSett-CH@sc.com](mailto:DerivativesSett-CH@sc.com)</u> |
| **SAUDI** | <u>[DerivativesSett-CH@sc.com](mailto:DerivativesSett-CH@sc.com)</u> |
| **TANZANIA** | [FMOps.Tz@sc.com](mailto:FMOps.Tz@sc.com); Dahal, Leyla; Kalinga, Nancy Richard; Mahela, Simon Godfrey; Muhochi1, Florian |
| **UGANDA** | <u>[DerivativesSett-CH@sc.com](mailto:DerivativesSett-CH@sc.com)</u> |
| **ZAMBIA** | <u>[DerivativesSett-CH@sc.com](mailto:DerivativesSett-CH@sc.com)</u> |
| **BOTSWANA** | <u>[DerivativesSett-CH@sc.com](mailto:DerivativesSett-CH@sc.com)</u> |

# Purpose/Objectives

This section aims to provide a comprehensive information on activities performed to meet the following purpose/objectives:

1. 1. Process around the MX2.11 Payment Message flow to Ratan & Ratan reverse ACK/ RELEASED Message 2. Monitor target cashflow flowing behavior. 3. Exception handling

# Scope

## In Scope (Ratan Eligible)

**EXPAND: RATAN Eligible Entity**

> **INFO**
> FMRP_H2_ENTITY_DBF table is used to save below M_LABEL (Entity Name).
>
> Any Amendment need to raise change ticket.

| M_LABEL | M_CTP_COD | M_EBBS | M_ENTITY_TYP | M_FEDS_ENT | M_PAY_HUB | FMID |
| --- | --- | --- | --- | --- | --- | --- |
| BEIJING | SCB/BEIJING | Y | subsidiary | CHN | CHINA | 400001378 |
| NANJING | SCB/NANJING | Y | subsidiary | CHN | CHINA | 10020899 |
| TIANJIN | SCB/TIANJIN | Y | subsidiary | CHN | CHINA | 235003861 |
| ZHUHAI | SCB/ZHUHAI | Y | subsidiary | CHN | CHINA | 10078716 |
| SHANGHAI | SCB/SHA | Y | subsidiary | CHN | CHINA | 10036642 |
| XIAMEN | SCB/XIA | Y | subsidiary | CHN | CHINA | 10062461 |
| SHENZHEN | SCB/SHENZHEN | Y | subsidiary | CHN | CHINA | 10032025 |
| GUANGZHOU | SCB/GUANGZHOU | Y | subsidiary | CHN | CHINA | 400054708 |
| SUZHOU | SCB/SUZHOU | Y | subsidiary | CHN | CHINA | 400054737 |
| CHENGDU | SCBCHENGDU/CGD | Y | subsidiary | CHN | CHINA | 400054741 |
| QINGDAO | SCB/QDO | Y | subsidiary | CHN | CHINA | 400057714 |
| CHONGQING | SCBCNCQG/CQG | Y | subsidiary | CHN | CHINA | 400075752 |
| HHANGZHOU | SCBCNHANGZH/HNZ | Y | subsidiary | CHN | CHINA | 400085753 |
| NNCHANG | SCBCHINANAN/NCG | Y | subsidiary | CHN | CHINA | 400090093 |
| DALIAN | SCBCHINADAL/DLN | Y | subsidiary | CHN | CHINA | 400095464 |
| NINGBO | SCBCHNIBR/NGB | Y | subsidiary | CHN | CHINA | 400130180 |
| HOHHOT | SCBCHHOBR/HHH | Y | subsidiary | CHN | CHINA | 400130178 |
| XXIAN | SCBLXIAN/XIN | Y | subsidiary | CHN | CHINA | 400193370 |
| FOSHAN | SCBCNFOSBR/FOS | Y | subsidiary | CHN | CHINA | 400209000 |
| JINAN | SCBCNJNABR/JNA | Y | subsidiary | CHN | CHINA | 400218197 |
| CHANGSHA | SCBCNCHANG/CGS | Y | subsidiary | CHN | CHINA | 400220273 |
| FUZHOU | SCBCNFUZHOU/FZH | Y | subsidiary | CHN | CHINA | 400229749 |
| KUNMING | SCBCNKMG/KMG | Y | subsidiary | CHN | CHINA | 400667486 |
| FT2 SHA | SCBSHAFTU/FT2 | Y | subsidiary | CHN | CHINA | 400677737 |
| SHYANG | SCBCNSHY/SYG | Y | subsidiary | CHN | CHINA | 400798477 |
| CHINA HO | SCBCNCHO/CHO | Y | subsidiary | CHN | CHINA | 400899993 |
| WUHAN | SCBL/WUH | Y | subsidiary | CHN | CHINA | 400185419 |
| **TAEYUAN** | **SCBCNTAYUAN/TYA** | **Y** | **subsidiary** | **CHN ** | **CHINA ** | **400516443** |
| **ZHENGZHOU** | **SCBCNZHENGZ/ZZU** | **Y** | **subsidiary** | **CHN ** | **CHINA ** | **400516442** |
| ACU SING | SCBACU/SIN | Y | branch | SG | SOUTH EAST ASIA | 300036368 |
| DBU SING | SCB/SIN | Y | branch | SG | SOUTH EAST ASIA | 3 |
| SACU SING | SSCBACU/SIN | Y | subsidiary | SG | SOUTH EAST ASIA | 400452428 |
| SDBU SING | SSCB/SIN | Y | subsidiary | SG | SOUTH EAST ASIA | 400451508 |
| MUMBAI | SCB/MMB | Y | branch | MUM | EAST ASIA | 4 |
| GIFTCITY | SCBGIFTCITY/MUM | Y | branch | GFT | EAST ASIA | 400960089 |
| KLISLAMIC | ISLAMICKL/KUL | Y | | KL | SOUTH EAST ASIA | 400093619 |
| KLUMPUR | SCB/KUL | Y | subsidiary | KL | SOUTH EAST ASIA | 9 |
| SCAG | STANCHAAG/FRA | Y | subsidiary | NONE | LONDON | 400906330 |
| LONDON | SCB/LDN | Y | branch | LON | NA | 10075222 |
| SSTL | SSTL/LDN | NA | branch | GTH | SOUTH EAST ASIA | 400041070 |
| HONGKONG | SCB/HKG | NA | subsidiary | HK | EAST ASIA | 2 |
| SCS HK | CAZEN/HKG | NA | NA | NA | EAST ASIA | 300075472 |
| TAIPEI | SCB/TPE | NA | subsidiary | TW | EAST ASIA | 10038345 |
| OBU TAIPEI | SCOBTP/TPE | NA | subsidiary | TW | EAST ASIA | 300011345 |
| BANGKOK | SCB/BKK | NA | subsidiary | BAN | SOUTH EAST ASIA | 6 |
| **DUBAI** | SCB/DUB | Y | branch | ME | MESA | 5 |
| **DIFC** | SCBDIFC/DUB | NA | branch | NA | NA | 400045551 |
| **TOKYO** | SCB/TYO | Y | branch | TYO | EAST ASIA | 10036382 |
| **JAKARTA** | SCB/JKT | Y | branch | JAK | SOUTH EAST ASIA | 8 |
| **MANILA** | SCB/MNL | Y | branch | NA | SOUTH EAST ASIA | 10036428 |
| **PHILIP FCU** | SCBPHFCDU/MKT | Y | branch | NA | SOUTH EAST ASIA | 300089409 |
| **NEW YORK** | SCB/NYC | NA | branch | NY | AMERICA | 7 |
| **MAURITIUS** | SCB/PLO | Y | subsidiary | NA | SOUTH EAST ASIA | 400018439 |
| **JOBURG** | SCBL/JBG | Y | branch | NA | AFRICA | 400032489 |
| **JERSEY_BR ** | SCPVTBKJEBR/STH | NA | branch | NA | NA | 400910415 |
| **DOHA** | SCB/DOH | NA | NA | ME | NA | 300010782 |
| **BAHRAIN** | SCB/BAH | NA | NA | ME | NA | 10036430 |
| **SRI LANKA** | SCB/CMB | NA | branch | NA | NA | 10036647 |
| **FCBUSLANKA** | **SCB/CMB** | NA | branch | NA | NA | **10036647** |
| **BOTSWANA** | SCB/GBE | NA | subsidiary | NA | NA | 10036775 |
| **KENYA** | SCBLKE/NBO | NA | subsidiary | NA | NA | 300011525 |
| **ZAMBIA** | SCBZAM/LUS | NA | subsidiary | NA | NA | 10041903 |
| **UGANDA** | SCBUGANDA/KAM | NA | subsidiary | NA | NA | 10041902 |
| **TANZANIA** | SCB/DAR | NA | subsidiary | NA | NA | 10040387 |
| **COTEDIVOIR** | COTEDIVOIR | NA | subsidiary | NA | NA | 400011581 |
| **HANOI** | HANOI | NA | subsidiary | NA | NA | 10041530 |
| **KARACHI** | SCB/KHI | NA | subsidiary | NA | NA | 10036655 |
| **GHANA** | SCB/ACC | NA | subsidiary | NA | NA | 10037477 |
| **DHAKA** | SCB/DAC | NA | branch | NA | NA | 300011470 |
| **NIGERIA** | SCBNIGERIA/LAG | NA | subsidiary | NA | NA | 300084297 |
| **SAUDI** | SCBSAUDI/RYD | NA | branch | NA | NA | 400991880 |
| **IRAQ** | SCBLIRQ/BGD | NA | subsidiary | NA | NA | 400625349 |
| **OMAN** | SCB/RWI | NA | branch | NA | NA | 300010730 |
| **HKGCT** | SCBGCT/HKG | NA | subsidiary | NA | EAST ASIA | 400058959 |
| **GCT** | SCBGCTGB/LND | NA | branch | NA | NA | 400044944 |
| **SCBPLC** | SCBPLC/LDN | NA | branch | NA | NA | 400013557 |
| **SCREALESTA** | SCREAESTINV/SIN | NA | NA | SG | NA | 400568282 |
| **PFK_SCPESG** | SC_SGPF_PESG | NA | NA | NA | NA | 400327728 |
| **FINVENTURE** | SC_SFUK_FINVEN | NA | NA | NA | NA | 400107029 |
| **SARAH_UK** | SARAH/LUX | NA | NA | NA | NA | 401037180 |
| **SLATE_QFC** | SLATEONE/DOH | NA | subsidiary | NA | NA | 401081696 |
| **SC NEA** | SCNEATRSCOR/LDN | NA | subsidiary | NA | NA | 400931959 |

**EXPAND_END**

- **While payment value date with 7 system business days (excluding every Sat, Sun, 01 Jan and 25 Dec) for all eligible entities**
- **The past date payments is only with T -1 business day**

## Out of Scope (Ratan Non-Eligible)

For All Entities:

- Trade validation status is not VALD or COMP
- All non deliverable currency payments except typology as PHP_DELIVERABLE and IDR_DELIVERABLE, **or except TWD ccy for HONGKONG entity**
- Cash Roll Over Payments - counterpart label as CAASH/ROLL
- Internal funding trades which is sent to Razor for Settlement
- Client Clearing payments - portfolio is CLIENT_CLRG_LCH or CLIENT_CLR_HKEX
- Payments in dummy portfolios defined in UDT table FLTPF_IN_DBF
- FXD payments already sent to Razor for settle, unless the strategy is **FEDSVALIDATOR for LONDON/SCAG/SSTL/DUBAI/DIFC/JOBURG/BOTSWANA/GHANA/KENYA/NIGERIA/UGANDA/ZAMBIA**
- Payments in Auto Suppression UDT table PAY_SUPP
- ETD Payments - M_TRN_TYPE as LST, CLR and FUT
- CPN eligible payments - except bullion currencies
- RFR and Swap Agent principal payments on Trade 1 and Trade 3 - auto netted off to 0

# Contact Person for Clarification on this DOI

Should there be any query regarding Settlement DOI, kindly contact Functional Lead as stated below.

| Type | SPOC | PSID | Function Email | Function SharePoint/Bridge |
| --- | --- | --- | --- | --- |
| Functional - Primary | Dinesh, Arockia | 1289935 | K.[A.Dinesh@sc.com](mailto:A.Dinesh@sc.com) | |
| Functional - Secondary | **K, Deepak** | **2018468** | **[deepak.k@sc.com](mailto:deepak.k@sc.com)** | |
| Technical - Primary | **Ren, Eric Shiyi** | **1395377** | **EricShiyi.Ren@[sc.com](http://sc.com)** | |
| Technical - Secondary | **Ren, Amy Yuxin** | **1490618** | **[AmyYuxin.Ren@sc.com](mailto:AmyYuxin.Ren@sc.com)** | |

# Operational Risk Framework Processes

Not Applicable

# Document of Operating Instructions (DOI)

- **EXPAND: Auto Feed Cashflow to RATAN** 1. Login MX 2.11 2. The cashflows will be automatically sent to RATAN based on the booking in MX2.11. Sample trade below ![2023-09-13 17_20_44-Search.png](attachments/2023-09-13 17_20_44-Search.png) 3.System generate payment ![image2023-9-13_18-8-36.png](attachments/image2023-9-13_18-8-36.png) 4.The data publisher will automatically send the eligible payment Message to Ratan ![Ratan insert.png](attachments/Ratan insert.png) **EXPAND_END**
- **EXPAND: Manual Publish of Cashflow to RATAN** Below operation should not exceed 30 payments each time. 1. In case there is an issue with auto publish, there will be an automatic email notification to PSS & Ops users. In case of urgency, Settlement user can choose to manual publish cashflow to RATAN, User manually validate a payment from INIT to SNTR - Login MX 2.11 and select the correct Profile (GBL_DO_SET, GBL_DOS_1, GBL_DOS_2, GBL_DOS_3, GBL_DOS_4, GBS_IN_SET ) - Go to Payment → Payment Workflow -> FMRP:INIT2SNTR MAN ![image2023-3-24_15-4-0.png](attachments/image2023-3-24_15-4-0.png) - Fill the Value date and Counterparty ![INIT2SNTR_1.png](attachments/INIT2SNTR_1.png) - **If it is Commodity payments, please do tick the COMMODITY flow box before proceed.** ** ![image2024-10-9_15-50-16.png](attachments/image2024-10-9_15-50-16.png)** ![Manul Push Murex.png](attachments/Manul Push Murex.png) - The data publisher will automatically send a payment Message to Ratan ![Manual Push Ratan.png](attachments/Manual Push Ratan.png) 1. User manually change a payment from SNTR to INIT If user manually change payment from SNTR to INIT, then the payment could not trigger the auto process any more. User has to manually move it from INIT to SNTR to publish the cashflow to RATAN - Login MX 2.11 and select the correct Profile - Go to Payment → Payment Workflow ![image2023-3-24_15-48-51.png](attachments/image2023-3-24_15-48-51.png) - Fill the Value date and Counterparty ![SNTR2INIT_1.png](attachments/SNTR2INIT_1.png) - Select the Payment and Click 'Proceed' ![SNTR2INIT_2.png](attachments/SNTR2INIT_2.png) **EXPAND_END**
- **EXPAND: Auto Publish Sequencing** **The cash flow publish processing for VD T - 1 to T + 1 will be auto triggered by batch flow - 500 payments from 00:00 to 19:30 PM GMT from Monday to Friday every 5 minutes ** **The cash flow publish processing for VD T + 2 to T + 7 will be auto triggered by batch flow - 6K payments from 0000 to 19:00 PM GMT from Monday to Friday every 2 hours ** ![batch Ratan.png](attachments/batch Ratan.png) **EXPAND_END**
- **EXPAND: User Monitor** 1. Monitor Process There is an <u>**optional **</u>feature to monitor the CN Payment Status. The real-time ACK Process will be primary control for data flow between Murex and Ratan. Ops user will use TLM to do the END to END reconciliation. - Login MX 2.11 and select the correct Profile - Go to Payment → Payment query → Query payment table ![image2023-3-27_9-34-3.png](attachments/image2023-3-27_9-34-3.png) - select "User filter" → select **FMRP Cashflow Monitor** → Proceed ![image2023-3-27_9-35-39.png](attachments/image2023-3-27_9-35-39.png) - And then shows below screen, | Payment Status | Reason | Description | Issue or not | Contact Point | Action | | --- | --- | --- | --- | --- | --- | | INIT | - | Payment in scope but not triggered push Ratan process | N | Ops User | Two Choice: - User can manual pushes the data by **FMRP:INIT2SNTR MAN** - Waiting the auto process to publish the data to Ratan | | SNTR | - | Payment have already push to Ratan, but not Acknowledged in Ratan | Y | Ratan PSS | User need to wait 5 mins and refresh the window to check the payment status. If the Reason still empty, then need to contact Ratan PSS to identify the Root Cause. and follow the Exception Handling. | | SNTR | RATAN Acknowledged | Payment have already push to Ratan and Acknowledged in Ratan | N | - | - | | RLSR | RATAN Acknowledged | Payment settled in Ratan. | N | - | - | | **CNCL ** | | **Cancelled Payment** | **N** | **-** | | | **CNET** | | **CPN Sent to MLS** | **N** | | | | **RLSD** | **CPN Released** | **CPN Released** | **N** | **-** | | | **SUPP** | | **Payment Suppressed in Murex ** | **N** | | | ![Picture1.png](attachments/Picture1.png) **EXPAND_END**
- **EXPAND: Exception handle** | Type | Exception Scenario | Handle Process | | --- | --- | --- | | System Outbound Connectivity Issue | Any MQ Connectivity Issue (example can be Disconnected or Slowness), which cause OLA break | PSS and OPS receive alert, Ops standard process is to wait for MQ recovery (SLA is 2 hours) Exception auto-resolves on MQ recovery… Where required, OPS to check Ratan blotter if payment received If yes, then false alert and no further action required by FMO. If no, Ops to check with Murex 2.11 PSS. In case of urgent payment manual payment via Oscar should be done <u>only if there is no risk of duplication</u> | | For MQ incident, MQ PSS team will send broadcast to impacted according to the incident severity / impact. MUREX PSS team will also notify business teams if there is impact to MUREX G2000 and its business. | | ~~NACK received from RATAN~~: ~~If ~~a~~ny mandatory attributes are missing, RATAN will send a NACK.~~ ~~This is to be built as an enhancement and R&R to be agreed between PSS & OPS.~~ Descope from 2024 H1: NACK workflow was discussed in context of scenario where mandatory payment attributes were missing in Cashflow sent to RATAN. This issue has not been observed in RATAN CN BAU flow (and also not observed cases within MX2.11 in prior years). If this happens, there will be an automated email alert sent to users, who can raise the issue to PSS. | | System Inbound Connectivity Issue | Any MQ Connectivity Issue (example can be Disconnected or Slowness), which cause OLA break | RATAN PSS will check with Murex PSS if the released request has been received and ack has been sent. If required, RATAN PSS to notify Settlement user can manually trigger 'Status WriteBack' to resend the status update to Murex2.11 | | System Issue | Application technical issue | Application PSS should monitor own issues, investigate root cause and notify stakeholders in time. | | System Issue | **Issue statement: ** there is one CN payment status is SNTR (means should send to RATAN) but discard in murex workflow. **Root cause:** Dev located the issue is murex workflow issue, but root cause could not be identified as the issue can not be replicated in dev env. **Handling:** This is rare case (only happen once) and Dev confirmed the issue won't applicable in H2 solution because in H2 there won't be any workflow process. Discussed with PO (Dinesh and Jons) and agreed enhancement in murex that if payment status is SNTR but Murex-Ratan publishing audit have no publishing timestamp recorded over 10 min against the timing when status changed to SNTR, murex will send alter email to ops. Issue context email: Handling agreement: [Murex 2.11 - RATAN Design agreements - FM re-platforming - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/FMRP/Murex+2.11+-+RATAN+Design+agreements) H1 Impediment item #1 | Ops will be notified by alert Email and follow existing BAU process to engage support team and PSS for investigation. | **EXPAND_END**
- **EXPAND: Payment Query for LIEN** Currently LIEN is placed at trade level and not sent to RATAN as part of Cashflow. A workaround has been agreed that Ops will check if there are any trades booked / updated with LIEN in MX2.11 To monitor any cashflows where LIEN has been placed in MX2.11, below query must be used (the logic sync to payment queue LIEN -INIT-INIT) 1. Create payment filter in production - Login MX 2.11 and select the correct Profile - Go to Payment → Payment query → Query payment table ![image2023-3-27_9-34-3.png](attachments/image2023-3-27_9-34-3.png) - select 'User filter' →click 'Filter' dropdown list → insert a new filter ![image2024-6-28_16-42-0.png](attachments/image2024-6-28_16-42-0.png) - Setup filter condition as below ![image2024-6-28_16-38-14.png](attachments/image2024-6-28_16-38-14.png) | RQWHERE("PAY_FLOW_DBF.M_FLOW_ID in (SELECT PF.M_FLOW_ID from ((((((MUREXDB.PAY_FLOW_DBF PF left join MUREXDB.TABLE#DATA#DEALIRD_DBF IRD on (PF.M_TRN_REF=IRD.M_NB)) left join MUREXDB.TABLE#DATA#DEALCURR_DBF CURR on (PF.M_TRN_REF=CURR.M_NB)) left join MUREXDB.TABLE#DATA#DEALCOM_DBF COM on (PF.M_TRN_REF=COM.M_NB)) left join MUREXDB.TABLE#DATA#DEALCRD_DBF CRD on (PF.M_TRN_REF=CRD.M_NB)) left join MUREXDB.TABLE#DATA#DEALSCF_DBF SCF on (PF.M_TRN_REF=SCF.M_NB)) left join MUREXDB.TABLE#DATA#PAYFLOW_DBF PUDT on (PF.M_FLOW_ID=PUDT.M_FLOW_ID)) where(IRD.M_LIEN_MONIT !='' or CURR.M_LIEN_MONIT !='' or COM.M_LIEN_MONIT !='' or CRD.M_LIEN_MONIT !='' or SCF.M_LIEN_MONIT !='') and PF.M_STATUS IN ('INIT','SNTR','RLSR') and PUDT.M_XLIEN_FLAG <>1 and PF.M_VALUE_DATE >= (select M_DATE from MUREXDB.TRN_PC_DBF) and PF.M_VALUE_DATE <= ( select dateadd(dd,7,M_DATE) from MUREXDB.TRN_PC_DBF))","") .AND.AMOUNT<>0.AND.(.NOT.("ALOC/"$CNTRP)).AND.VALUE_DATE>=DENV('DATE_BO').AND.CNTRP<>'CAASH/ROLL'.AND.TRN_GRP<>'SFUT'.AND.TRN_GRP<>'LFUT' | | --- | **EXPAND_END**
- **EXPAND: Additional Flags to Ratan** | Flag | Purpose | Murex Logic | Comments | | --- | --- | --- | --- | | COM or Non COM Flag | Commodity Flag will be sent as 'Y' for Cashflows which belong to Commodity trades - for both Precious Metal and Non Precious Metal currency | - The existing payment UDF filed COM_FLOW is utilized, Murex will update this field first before pushing the payment to Ratan. if the value is 1 or ticked in Murex, the payment is a COM payment and will be handled by COM Ops team. otherwise it will be handled by OTC ops team. ![image2024-10-9_15-50-16.png](attachments/image2024-10-9_15-50-16.png) - The payment will be updated the flag as Ticked if it meets one of the below conditions: 1. Trade family is COM (TRN_FMLY=COM) 2. If the product is FXD and one leg is a bullion currency 3. If the product is SCF and the instrument is a bullion currency 4. Portfolio is in COM_OPS_SETT combined port 5. Strategy is with COM_MOD flag on 6. for any other product, Pricing or PL currency is a bullion currency(**HAU is a new bullion currency created for HK and not with name start X**) 7. XAF, XOF and XOH currencies are excluded as they are not bullion currency 8. The Counterpart with M_PB_CUST flag is excluded | | | RFR & SWAP AGENT Flag | RFR & SAL payments need to be clarified the settlement type (initial principal, the final principal, Coupon or intermediate MTM principal) for Ratan. | - The indicators are Typology, Strategy, Flow Types (FLOW_TYPE2) - The last coupon or the final principal payment need the extra indicator, the existing UDF X_DUMMY2 is utilized - The logic for X_DUMMY2 is as below: 1. The family group has to be CS 2. The linked trade id is not 0 3. The Strategy is RECALC or SWAP_AGENT 4. The value date is equal to the trade maturity date | Ratan side logic for identifying RFR and SAL settlement type is as below: - Initial Notional(Trade 2): Strategy in (‘SWAP_AGENT,'RECALC') && Typology in (‘RFR CCS MTM Fixing’, ‘RFR CCS MTM Fwd’) && FLOW_TYPE2==’INIT’ - Interim MTM(Trade 2): Strategy in (‘SWAP_AGENT,'RECALC') && Typology in (‘RFR CCS MTM Fixing’, ‘RFR CCS MTM Fwd’) && FLOW_TYPE2!=’INIT’ && X_DUMMY2=='0' - Coupon(Trade 1): Strategy == ‘SWAP_AGENT’ && （Typology=’Vanilla X-ccy swap’ or Typology=’FWD_START_SWAP' or Typology=’’) - Final Notional(Trade 2): Strategy in (‘SWAP_AGENT,'RECALC') && Typology in (‘RFR CCS MTM Fixing’, ‘RFR CCS MTM Fwd’) && X_DUMMY2==’1’ - **Typology RFR CCS MTM Fwd is not in the scope of 18 Jan 2025 delivery, the final date is to be updated by Ratan team** | | Pending Clearing Flag | The initial principal or upfront fees for clearing eligible trades from Swap Swire systems (IRS and CCS), the payment shall be indicated if it is facing the bilateral client so the NSTP rules can be built up in Ratan. The bilateral client payments shall be reversed in Ratan once the trade get cleared and novate to the clearing house counterpart | - The existing payment UDF X_DUMMY3 is utilized - The logic to update the filed as Y if it meets all below conditions: 1. Trade family is IRD 2. Source system name is SWAPSWIRE and CCP name is not empty 3. Counterpart type is not a clearing house, not in ('LCH/LDN', 'CMECCP/WMN', 'JSCC/TYO', 'SCBOTCCCP/HKG', 'ECLIPSCBHKL/LDN', 'EUREXCAGCCP/FRA', 'ECLIPSESCB/LDN', 'SCBOTCCCP/HKG') **New Added for CFETS FXO:** 1. **Source system name is CFETS or cfets** 2. **The trade group is OPT** 3. **The UDF ADD_COMMENTS is empty (Beta trade will have the value as CCP)** | | | NDS Fixing Duplication Flag | NDS Fixing FXD payments are sent via a dedicated periodical job to Ratan, post the duplication check. The payment from the 2nd FXD trade will be indicated with duplication information if it get scanned out that the same ND parent trade has 2 FXD auto generated in the system | - The existing payment UDF COMMENTS is utilized for duplication information. - The format of information is "Potential duplication of FXD 999999999" | | | Pending Fixing Flag | The extra flag is built to indicate if the payment sent to Ratan, still has at least 1 cash flow is pending fixing event from the same trade, with the same value date and currency. The payments with VD from T-1 to T+1, the WAIT_FIX flag is sent with value as X and then it shall be updated within 1 hour from the enhancement data file to Y or N. The payments with VD from T+2 to T+7, the WAIT_FIX flag is sent to Ratan directly with value Y or N. | - The extra flag WAIT_FIX is introduced in both MXML message and batch file - All payments will be scanned and updated the flag to X, Y or N. | | **EXPAND_END**

# Record Retention

- FMRP_ENT_DBF : Permanent. Any amendment about this table need to raise Change Ticket and join MX 2.11 Pre-Cab.
- SCB_FMRP_DBF : After the flow released in Ratan, data will be saved as value date within 1 Month. job FMRP_PURGE use to realize the function.

# Appendices

Not Applicable

# FMO Data Management Projects

Not Applicable

# Approval of DOI

📎 [DOI_Signoff_CHG0850616.msg](attachments/DOI_Signoff_CHG0850616.msg)
 
📎 [RE DOI Update for HAU Currency - COM flag as Y.msg](attachments/RE DOI Update for HAU Currency - COM flag as Y.msg)