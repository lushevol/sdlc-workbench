| S.No | Tranche 1 Country | RATAN Technical Go live date | RATAN Business Go live date | ISO Go live date |
| --- | --- | --- | --- | --- |
| 1 | KE | 8-Aug-2026 | 24-Aug-2026 | 13-Jun |
| 2 | TZ | 13-Jun |
| **3** | **VN** | **10-10-2026**** 22-Aug 03-Oct** |
| 4 | BD | 05-Sep |
| 5 | LK | 05-Sep |
| 6 | PK | 05-Sep |
| **7** | **ZM** | **22-08-2026**** 17-Oct** |

# Static Details

## Nostro Static Data

| Country | MX2.11 Entity | FMID | FMCODE | Nostro static data |
| --- | --- | --- | --- | --- |
| Kenya | KENYA | 300011525 | SCB KENYA B*NBO | |
| Zambia | ZAMBIA | 10041903 | SCB ZAMBIA*LUS |
| Tanzania | TANZANIA | 10040387 | SCB TANZANI*DAR |
| Sri Lanka | SRI LANKA | 10036647 | SCB COLOMBO*CMB |
| FCBUSLANKA | 10022098 | SCB COL FCB*CMB |
| Vietnam | HANOI | 10041530 | SCB HANOI*HNI |
| Pakistan | KARACHI | 10036655 | SCB KARACHI*KHI |
| Bangladesh | DHAKA | 300011470 | SCB DHAKA*DAC |

## Swift Static Data

| Entity FMCODE | Country Code | Branch code | FMID | Sender Bic | Field 53 BIC(Rule1) | Field 53 CCY to be used | Field 58 BIC(Rule2) | Swift Static Data |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SCB HANOI*HNI | VN | 29 | 10041530 | SCBLVNVXXXX | SCBLVNVXFMO | VND | SCBLVNVXFMO | |
| SCB KARACHI*KHI | PK | 97 | 10036655 | SCBLPKKXXXX | SCBLPKKXXXX | PKR | SCBLPKKXXXX |
| SCB ZAMBIA*LUS | ZM | 52 | 10041903 | SCBLZMLXXXX | SCBLZMLXFMO | ZMW | SCBLZMLXFMO |
| SCB KENYA B*NBO | KE | 39 | 300011525 | SCBLKENXXXX | SCBLKENXFMO | KES | SCBLKENXFMO |
| SCB COLOMBO*CMB | LK | 84 | 10036647 | SCBLLKLXXXX | SCBLLKLXXXX | LKR | SCBLLKLXXXX |
| SCB COL FCB*CMB | LK | 85 | 10022098 | SCBLLKLXXXX | SCBLLKLXXXX | LKR | SCBLLKLXXXX |
| SCB TANZANI*DAR | TZ | 50 | 10040387 | SCBLTZTXXXX | SCBLTZTXFMO | TZS | SCBLTZTXFMO |
| SCB DHAKA*DAC | BD | 86 | 300011470 | SCBLBDDXXXX | SCBLBDDXXXX | BDT | SCBLBDDXXXX |

## Branch Code

| | Country | Branch Code | FMID |
| --- | --- | --- | --- |
| 1 | Vietnam | 29 | 10041530 |
| 2 | Pakistan | 97 | 10036655 |
| 3 | Zambia | 52 | 10041903 |
| 4 | Kenya | 39 | 300011525 |
| 5 | Sri Lanka | 84 | 10036647 |
| 6 | Sri Lanka | 85 | 10022098 |
| 7 | Tanzania | 50 | 10040387 |

## Release CutOff

| | Country | FMID | FMCODE | cut_off_time | cut_off_shifter | Release cutoff |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Kenya | 300011525 | SCB KENYA B*NBO | 15:00 UTC | VD-1BD | 📎 [Release CutOff.xlsx](attachments/Release CutOff.xlsx) |
| 2 | Zambia | 10041903 | SCB ZAMBIA*LUS | 15:00 UTC | VD-1BD |
| 3 | Vietnam | 10041530 | SCB HANOI*HNI | 11:00 UTC | VD-1BD |
| 4 | Bangladesh | 300011470 | SCB DHAKA*DAC | | Confirmed with Deepak and user ,will use the Currency /Shifter/Time/Timezone from Razor |
| 5 | Sri Lanka | 10022098/10036647 | SCB COLOMBO*CMB/SCB COL FCB*CMB | 13:00 UTC | VD-1BD |
| 6 | Tanzania | 10040387 | SCB TANZANI*DAR | | Confirmed with Deepak and user ,will use the Currency /Shifter/Time/Timezone from Razor |
| 7 | Pakistan | 10036655 | SCB KARACHI*KHI | 13:00 UTC | VD-1BD |

## Non-ISO to ISO Currency

NGB-NGN,PKO-PKR need to be added on Ratan side,for the others ,keep as is

| **PKO** | **PKR** | 2026-01-20 Confirmed with @Cordelia Sumita K Thirunavukarasu For Pakistan, Non ISO to ISO mapping is PKO -PKR, doesn't exist in current mapping list, need to be added |
| --- | --- | --- |

## EBBS Bridge Account

2026-03-09 Yashas provided the data ,but QATAR and Bangladesh need to be double confirm

| id | closing_entity | legal_entity | fmid | ebbs_bridge_account |
| --- | --- | --- | --- | --- |
| | | SCB KENYA B*NBO | 300011525 | 0062599158900 |
| | | SCB ZAMBIA*LUS | 10041903 | 0062599158900 |
| | | SCB TANZANI*DAR | 10040387 | 0062599158900 |
| | | SCB COLOMBO*CMB | 10036647 | 09995954893 |
| | | SCB COL FCB*CMB | 10022098 | 09995954895 |
| | | SCB HANOI*HNI | 10041530 | 09434372001 |
| | | SCB KARACHI*KHI | 10036655 | 09900006470 |
| | | SCB DHAKA*DAC | 300011470 | 09111178468 |

## EBBS Posting_Branch/Txn_dr_code/Txn_cr_code/Txn_type_code（Transaction Type）

2026-06-15  Got update from ebbs that Cr Txn Code should be update to 578 from 278 for TZ

| FMID | Country | Posting Branch | Txn Type code | Dr Txn Code | Cr Txn Code |
| --- | --- | --- | --- | --- | --- |
| 10041530 | VN | 099 | RTN | 478 | 378 |
| 300011525 | KE | 07800 | RTN | 478 | 278 |
| 10040387 | TZ | 08700 | RTN | 478 | 578 |
| 10041903 | ZM | 01700 | RTN | 478 | 278 |
| 300011470 | BD | 068 | RTN | 478 | 378 |
| 10036655 | PK | 001 | RTN | 478 | 678 |
| 10036647 | LK | 093 | RTN | 478 | 378 |
| 10022098 | LK | 093 | RTN | 478 | 378 |

## TimeZone

When generate accounting ,system will get country by fmid from above static table ,then get zoneid via country, if there is new country on boarding ,we need to config this

2026-03-13

Provided  by J, Madhankumar and Yashas

| KENYA | KE | Africa/Nairobi |
| --- | --- | --- |
| ZAMBIA | ZM | Africa/Lusaka |
| TANZANIA | TZ | Africa/Dar_es_Salaam |
| SRI LANKA | LK | Asia/Colombo |
| Vietnam | VN | Asia/Ho_Chi_Minh |
| Pakistan | PK | Asia/Karachi |
| Bangladesh | BD | Asia/Dhaka |

# MX bifurcation logic

[02 Swift Message Analysing for manual entities - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/02+Swift+Message+Analysing+for+manual+entities)   ---[MX Eligibility Rule](https://confluence.global.standardchartered.com/display/DSP/02+Swift+Message+Analysing+for+manual+entities#id-02SwiftMessageAnalysingformanualentities-MXEligibilityRule)

# Business Rule Setup

## NSTP

## Cashflow Suppression

📎 [Business rule0811.xlsx](attachments/Business rule0811.xlsx)

# UAT Testing Signoff

| Country | Attached |
| --- | --- |
| KE/TZ/BD/LK/PK/ZM/VN | [FW Tanzania - TrainingUAT - Sign off required.msg](https://confluence.global.standardchartered.com/download/attachments/3551982887/FW%20Tanzania%20-%20TrainingUAT%20-%20Sign%20off%20required.msg?version=1&modificationDate=1786669616000&api=v2) [RE Tanzania - TrainingUAT - Sign off required.msg](https://confluence.global.standardchartered.com/download/attachments/3551982887/RE%20Tanzania%20-%20TrainingUAT%20-%20Sign%20off%20required.msg?version=2&modificationDate=1786669648000&api=v2) [RE Bangladesh - TrainingUAT closure overall sign off.msg](https://confluence.global.standardchartered.com/download/attachments/3551982887/RE%20Bangladesh%20-%20TrainingUAT%20closure%20%20overall%20sign%20off.msg?version=1&modificationDate=1786669619000&api=v2) [RE CASH FLOW MIGRATION - FUNCTIONAL TESTING OF MANUAL ENTITIES - UAT Sign off .msg](https://confluence.global.standardchartered.com/download/attachments/3551982887/RE%20CASH%20FLOW%20MIGRATION%20-%20%20FUNCTIONAL%20TESTING%20OF%20MANUAL%20ENTITIES%20-%20UAT%20Sign%20off%20.msg?version=2&modificationDate=1786669643000&api=v2) [RE FMRP 8.0 - Cashflow Migration Functional Testing of Manual Entities - Vietnam.msg](https://confluence.global.standardchartered.com/download/attachments/3551982887/RE%20FMRP%208.0%20-%20%20Cashflow%20Migration%20Functional%20Testing%20of%20Manual%20Entities%20-%20Vietnam.msg?version=2&modificationDate=1786669644000&api=v2) [RE Pakistan - TrainingUAT closure overall sign off.msg](https://confluence.global.standardchartered.com/download/attachments/3551982887/RE%20Pakistan%20-%20TrainingUAT%20closure%20%20overall%20sign%20off.msg?version=2&modificationDate=1786669644000&api=v2) [RE Sri Lanka - TrainingUAT closure overall sign off.msg](https://confluence.global.standardchartered.com/download/attachments/3551982887/RE%20Sri%20Lanka%20-%20TrainingUAT%20closure%20%20overall%20sign%20off.msg?version=2&modificationDate=1786669647000&api=v2) LMS [RE Request for UAT Sign-off Approval - Ratan Tranche 1 (Except TZ).msg](https://confluence.global.standardchartered.com/download/attachments/3551982887/RE%20Request%20for%20UAT%20Sign-off%20Approval%20-%20Ratan%20Tranche%201%20%28Except%20TZ%29.msg?version=3&modificationDate=1786669645000&api=v2) [RE Request for UAT Sign-off Approval - Ratan Tranche 1.msg](https://confluence.global.standardchartered.com/download/attachments/3551982887/RE%20Request%20for%20UAT%20Sign-off%20Approval%20-%20Ratan%20Tranche%201.msg?version=3&modificationDate=1786669646000&api=v2) |

# STRATEGIC_FM_LIST

When generate swift message ,will check if the entities in below list ,if in ,will generate swift message

Because  below entity will be in cashflow suppressed ,so no need to config in STRATEGIC_FM_LIST,for the other manual entities ,need to add fmid in this strategic _fm_list

| SLATE_QFC | 401081696 | SLATE ONE LLC*DOH |
| --- | --- | --- |

# CPT

[Tranche:1 Countries (Bangladesh, Tanzania, Sri Lanka, Pakistan, Kenya, Vietnam,  Zambia )Manual entities cash Settlements Migration Day 2 - Operational readiness & Post go live Issue Tracker - FM re-platforming - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3790204945)

[01 CPT -Tranche1-LMS verification - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/01+CPT+-Tranche1-LMS+verification)