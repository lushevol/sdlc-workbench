| Tranche2 | Technical go live date in Ratan | Business go live date |
| --- | --- | --- |
| BH | | Third week of Sepetember |
| QA |
| UG |
| GH |
| NG |

# Static Details

## Nostro Static Data

| Country | MX2.11 Entity | FMID | FMCODE | Nostro Static |
| --- | --- | --- | --- | --- |
| Bahrain | BAHRAIN | 10036430 | SCB BAHRAI*MAN | 📎 [Nostro Static Data0729.xlsx](attachments/Nostro Static Data0729.xlsx) |
| QATAR | DOHA | 300010782 | SCB DOHA*DOH |
| SLATE_QFC | 401081696 | SLATE ONE LLC*DOH |
| Uganda | UGANDA | 10041902 | SCB UGANDA*KAM |
| Ghana | GHANA | 10037477 | SCB GHANA*ACC |
| Nigeria | NIGERIA | 300084297 | SCB NIGERIA*LAG |

## Swift Static Data

| Entity FMCODE | Country Code | Branch code | FMID | Sender Bic | Field 53 BIC(Rule1) | Field 53 CCY to be used | Field 58 BIC(Rule2) | Swift Static Data |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SCB BAHRAI*MAN | BH | 55 | 10036430 | SCBLBHBMXXX | SCBLBHBMGMO | BHD | SCBLBHBMGMO | 📎 [Swift Static data2026-07-21.xlsx](attachments/Swift Static data2026-07-21.xlsx) |
| SCB NIGERIA*LAG | NG | 82 | 300084297 | SCBLNGLAATSY | SCBLNGLAFMO | NGN | SCBLNGLAFMO |
| SCB GHANA*ACC | GH | 35 | 10037477 | SCBLGHACXXX | SCBLGHACFMO | GHS | SCBLGHACFMO |
| SCB UGANDA*KAM | UG | UG | 10041902 | SCBLUGKAXXX | SCBLUGKAFMO | UGX | SCBLUGKAFMO |
| SCB DOHA*DOH | QA | QA | 300010782 | SCBLQAQXXXX | SCBLQAQXGMO | QAR | SCBLQAQXGMO |

## ![](https://confluence.global.standardchartered.com/download/attachments/3244588508/image-2025-5-21_16-34-44.png?version=1&modificationDate=1747816484000&api=v2)

## Branch Code

| Country | Branch Code | FMID |
| --- | --- | --- |
| Bahrain | 55 | 10036430 |
| Nigeria | 82 | 300084297 |
| Ghana | 35 | 10037477 |
| Uganda | UG | 10041902 |
| QATAR | QA | 300010782 |

## Release CutOff

| | Country | MX2.11 Entity | FMID | FMCODE | cut_off_time | cut_off_shifter | Release cutoff |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Bahrain | BAHRAIN | 10036430 | SCB BAHRAI*MAN | 15:00 UTC | VD-1BD | |
| 2 | QATAR | DOHA | 300010782 | SCB DOHA*DOH | | Confirmed with Deepak and user ,will use the Currency /Shifter/Time/Timezone from Razor |
| SLATE_QFC | 401081696 | SLATE ONE LLC*DOH | NA | NA |
| 3 | Uganda | UGANDA | 10041902 | SCB UGANDA*KAM | 15:00 UTC | VD-1BD |
| 4 | Ghana | GHANA | 10037477 | SCB GHANA*ACC | 15:00 UTC | VD-1BD |
| 5 | Nigeria | NIGERIA | 300084297 | SCB NIGERIA*LAG | 17:00 UTC | VD-1BD |

## Non-ISO to ISO Currency

NGB-NGN,PKO-PKR need to be added on Ratan side,for the others ,keep as is

| **NGB** | **NGN** | 2026-03-25 NGB-NGN not exists in Ratan ,need to add this new mapping 2026-03-11 Conrirmed with Synthia ,this mapping need to added for Nigeria |
| --- | --- | --- |

## Rounding Logic

2026-08-14 Deepak and Gomathy confirmed thata NGN rounding percision should be 2

2026-08-05 Gokul requested to set up rounding off for **NGB ccy to 2 precision.**

2026-04-02

As confirmed with Deepak and Synthia  , for NGN rounding setup in Ratan ,precison  will update from 2 to 0,and rounding type will keep as is  ROUNDING_OFF.For the others, keep as is

| k_currency | v_precision | v_type | Comment |
| --- | --- | --- | --- |
| ~~NGN~~ | ~~0~~ | ~~ROUNDING_OFF~~ | 2026-08-14 Deepak and Gomathy confirmed thata NGN rounding percision should be 2 |
| NGB | 2 | ROUNDING_OFF | |

## EBBS Bridge Account

2026-03-09 Yashas provided the data ,but QATAR and Bangladesh need to be double confirm

| id | closing_entity | legal_entity | fmid | ebbs_bridge_account |
| --- | --- | --- | --- | --- |
| | | SCB BAHRAI*MAN | 10036430 | 09906397050 |
| | | SCB DOHA*DOH | 300010782 | 09473025940 |
| | | SCB UGANDA*KAM | 10041902 | 0062599158900 |
| | | SCB GHANA*ACC | 10037477 | 0062599150800 |
| | | SCB NIGERIA*LAG | 300084297 | 9625047537 |

## EBBS Posting_Branch/Txn_dr_code/Txn_cr_code/Txn_type_code（Transaction Type）

2026-06-15  Got update from ebbs that Cr Txn Code should be update to 578 from 278 for TZ

| FMID | Country | Posting Branch | Txn Type code | Dr Txn Code | Cr Txn Code |
| --- | --- | --- | --- | --- | --- |
| 10037477 | GH | 00001 | RTN | 478 | 278 |
| 300084297 | NG | 00100 | RTN | 478 | 278 |
| 10041902 | UG | 00001 | RTN | 478 | 278 |
| 10036430 | BH | 055 | RTN | 478 | 378 |
| 300010782 | QA | 042 | RTN | 478 | 378 |

## TimeZone

When generate accounting ,system will get country by fmid from above static table ,then get zoneid via country, if there is new country on boarding ,we need to config this

2026-03-13

Provided  by J, Madhankumar and Yashas

| BAHRAIN | BH | Asia/Bahrain |
| --- | --- | --- |
| QATAR | QA | Asia/Qatar |
| UGANDA | UG | Africa/Kampala |
| GHANA | GH | Africa/Accra |
| NIGERIA | NG | Africa/Lagos |

# MX bifurcation logic

[02 Swift Message Analysing for manual entities - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/02+Swift+Message+Analysing+for+manual+entities)   ---[MX Eligibility Rule](https://confluence.global.standardchartered.com/display/DSP/02+Swift+Message+Analysing+for+manual+entities#id-02SwiftMessageAnalysingformanualentities-MXEligibilityRule)

# Business Rule Setup

## NSTP

## Cashflow Suppression

📎 [Business rule0811.xlsx](attachments/Business rule0811.xlsx)

# UAT Testing Signoff

| Country | Attached |
| --- | --- |
| BH/NG/QA/UG/GH | |

# CPT

[Tranche:2 Countries (Nigeria, Ghana, Qatar, Bahrain, Uganda)Manual entities cash Settlements Migration Day 2 - Operational readiness & Post go live Issue Tracker - FM re-platforming - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3817314605)

[02 CPT -Tranche2-LMS verification - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/02+CPT+-Tranche2-LMS+verification)

# STRATEGIC_FM_LIST

When generate swift message ,will check if the entities in below list ,if in ,will generate swift message

Because  below entity will be in cashflow suppressed ,so no need to config in STRATEGIC_FM_LIST,for the other manual entities ,need to add fmid in this strategic _fm_list

| SLATE_QFC | 401081696 | SLATE ONE LLC*DOH |
| --- | --- | --- |