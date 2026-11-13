# Summary of Changes Required

As the request from VN government & the strategy for Vietnam market, we’re working on a draft proposal of setting up a new branch in IFC (International Financial Centre) – this branch is not under SCB Vietnam entity – it should be considered as a new branch of SCB Singapore. We have discussed and listed the business services in the attached file (**Column Q – for list of applications**) and need your support to provide ballpark estimate for system setup / implementation for this new branch.

# Assumption

1. New FMID/Entity for Vietnam, which is under SCB Singapore
2. FMRP flow only
3. Onboarding only, no customized features
4. Based on strategic trade SI stamping

# Estimation

| Phase | Effort |
| --- | --- |
| Support EBBS accounting for new branch | 15 |
| Static setup (Swift, Accounting, Cutoff, Nostro, ISO Currency, Rules, Workflow) | 6 |
| SIT/Regression | 2 |
| UAT Support | 6 |
| Release | 5 |

**Settlement**: 34 MD

**Trade Control**: 10 MD

**C&A**: No MD

| # | Description | Details | Type | Required? | Done By |
| --- | --- | --- | --- | --- | --- |
| 1 | ~~Bypass Validation Rule ~~Not required any longer as New MO Validation Model solved the issue. | ~~Bypass LOANIQ/FX, rest need validation~~ ~~Post MO Validation moved to FMRP, then not required?~~ | | | |
| 2 | LMS Feed Entity List Update | Blacklist includes: EG/NP/SAUDI/KL/TH/TW | Config | No | Dev Team (CR) |
| 3 | [Murex Cash Migration Only] Entity list for the Batch Solution | H2 Adaptor whitelist includes: UK, DE (Set as default) H1 Adaptor whitelist includes: CN/SG/MY/IN | Config | |
| 4 | - BCS vs Strategic Routing - Entity whitelist for in scope entities (covered via Cashflow Suppression rule) - Entity whitelist setup to send to RAZOR or handle in RATAN (RATAN generates SWIFT & Accounting | Workflow whitelist: 1. LOANIQ (legacy flow) 2. Strategic flow (New Entity/SG/MY/IN/UK/DE/EG/NP/SAUDI) | Config | Yes |
| 5 | SWIFT Generation Changes - Booking Entity FMID(mandatory for each entity) - Booking Entity SWIFT BIC (Sender BIC in SWIFT) (mandatory for each entity) - Field 53 SWIFT BIC (for LCY & Over Account) (mandatory for each entity) - Field 58 SWIFT BIC (for Flip MT202) (mandatory for each entity) - Receiver BIC (MT604/605) - Branch code mapping (mandatory for each entity) - Any other branch specific requirement on SWIFT | Need to be added for new entity | Config | Yes |
| 6 | Currency Release Time (mandatory for each entity) | Need to be added for new entity | Config | Yes |
| 7 | NDS Auto Netting | Blacklist: TBD | Config | No for FMRP |
| 8 | Pending Fixing STP/NSTP Control( in case new product have fixing events) | Blacklist: TBD | Config | No |
| 9 | SSI Stamping Hierarchy - Follow UK model (give priority to "Country Specific + Global Product" SSI over Global Entity + Product Specific SSI) | All New logic | Config | No |
| 10 | Currency Configuration (if applicable) - Non-ISO to ISO Code mapping - Precious Currency Mapping | | Config | No |
| 11 | Settlement Accounting - Bridge Account # (mandatory for each entity) - EBBS Branch code & EBBS Transaction type (mandatory for each entity) - Any other branch specific requirement (example: Settlement Accounting is suppressed for Precious Metal CCY's in UK) | Need to be added for new entity New Solace topic/queue Accounting service adapt to new entity | Config/Dev | Yes |
| 12 | Include new branch in GUI Drop down - Cashflow Blotter (mandatory for each entity) - Dashboard (mandatory for each entity) | Need to be added for new entity | Config | Yes |
| 13 | Vostro SI Input Screen - Include New Settlement Means | | Config | No |
| 14 | Rounding - applicable for special currency/requirement only | | Config | No | |
| 15 | Nostro Static Setup (mandatory for each entity) | | Static | Yes | If volume high will be done by Dev Team (CR). Else Data Ops |
| 16 | Vostro Static Setup (Vostro to drive Nostro assignment) - Over-Account Clients to be created as Branch specific SSI | | Static | No | Data Ops |
| 17 | Business Rules Setup - Cashflow Suppression - White List for in scope entities - Swift Suppression - Auto Debit by Agent - Nostros shared with other entity (example: China) - NSTP - Add new entity to Rules where SCB Entities as Counterparty is bypassed - Add new entity to Rules where SCB entities are added as Booking Entity - Netting Static - BIC Netting Static | | Static | Yes | Data Ops |
| 18 | Open Firewall for users in new location | | Config | Yes | Dev Team |
| 19 | Downstream Engagement to determine additional requirements if any | | Analysis | No | Dev Team |
| 20 | UAT support | | Testing | Yes | Settlement Ops |
| 21 | Regression Testing / SIT | | Testing | Yes | Dev Team |
| 22 | CPT | | Testing | Yes | MO/Settlement Ops |
| 23 | Data Entitlement | | | | |
| 24 | Release Preparation on script, configuration chagne | | | Yes | |

# Murex Special Function Checklist

| | Function Summary | Function Introduction | Confluence |
| --- | --- | --- | --- |
| 1 | Batch File | For value date today, tomorrow and day after, Murex will send real time message, others will be in batch file. | |
| 2 | Pending Fixing | As there is pre-netting function in Murex, for COM ASIAN/FW/SWP IRD/CF/CS/FRA/IRS products, cashflow can be auto netted together. So when 1 cashflow comes, Murex will have a field pending fixing flag to mark whether the cashflow should be in WAITING + Pending Another Leg in Ratan | [IRS Fix Leg & Floating leg payment handling - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=2726685251) |
| 3 | NDS Auto Netting | For ND products in Murex, it will generate child FXD trade to convert ND ccy to delivery ccy. So in Ratan side, it would auto net delivery ccy cashflow in parent trade with delivery ccy cashflow in child trade. | [NDS Auto Netting - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/NDS+Auto+Netting) |
| 4 | SWAP AGENT | Ratan will mark payment type for RFR and Swap Agent based on identifier from Murex, for auto netting/SWIFT suppression handling in Ratan | [RFR and Swap Agent - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/RFR+and+Swap+Agent) |
| 5 | Special Flag | - COM or Non COM - Pending Clearing - Linked trade Id | |

# LMS Feeding entity config

- Entity Feeding to LMS or not: **Need to confirm with settlement team & LMS if new entity is required to send to LMS.** | Entity FM Code | Entity FMID | Feeding to LMS | | --- | --- | --- | | SCB EGYPT*CAI | 401036553 | No | | SCB SAUDI*RYD | 400991880 | No | | NEPAL GRINDLAYS*KTM | 400007847 | No | | SCB KL*KUL? | 9 | No | | STANCHART SAADIQ*KUL | 400093619 | No | | TAIPEI | | No | | OBU TAIPEI | | No | | BANGKOK | | No | | Other | Other | Yes |
- Source System & Tag 20 agreement: **Need to agree with LMS the source system & tag 20 logic for new entity onboarding** | Booking System | Source System | Flow | Prefix of field 20 | Comment | | --- | --- | --- | --- | --- | | SABRE EQ | STELLA | SABRE EQ -> BCS STELLA -> STELLA -> TDS3 -> RATAN | EQ | This is in the BAU stack not in the Strategy stack, just for information here. | | LOANIQ | LOANIQ | LOANIQ -> STELLA -> TDS3 -> RATAN ONE | LQ | | | BLADE/S2BX/CFETS | FMRP | BLADE/S2BX/CFETS -> STELLA -> TDS3 -> RATAN | DV | |

# Nostro

Defined with granular level of legal entity + currency, there're 2 ways to maintain the Nostro static data.

- Batch initialization by db script: This is applicable for the new project where there're hundreds of new data to be created, **need to ask settlement ops provide the reviewed Nostro static data with below file format and tech team release the data to production by CR.** 📎 [WMSUS.xlsx](attachments/WMSUS.xlsx)
- RTS team manually maintain by GUI, maker/checker required

# Release cutoff

Defined with granular level of legal entity + currency: **Need ops share the reviewed & approved release cutoff with as below & dev team deploy the data to production by CR.**
![image2024-7-19_15-55-13.png](attachments/image2024-7-19_15-55-13.png)

# Business Rules

- NSTP Rules: Rule setup can be done in 2 ways as below. - **Ops review & share the rules to dev, dev team release rules by scripts through a CR**. This is applicable for the project which there're hundreds of new rules setup. - **Business Rule team maintain the rules from RATAN GUI as their BAU**, maker checker required.
- Cashflow Suppression Rules: **Similar approach as NSTP Rule**
- Suppression Rules: **Similar approach as NSTP Rule**
- Netting Rules: **Similar approach as NSTP Rule**

# Swift Generation Local Static Data

- Sender's BIC: Hardcoded BIC for each entity which is provided by settlement ops, below is the sample for CN entities. **Need to get the BIC for new onboarding entity from ops & add to the RATAN local config and release by CR.** ![image2024-7-19_15-23-0.png](attachments/image2024-7-19_15-23-0.png)
- Field 53 SWIFT BIC - LCY - MT103, MT202 & MT103+202COV - Over-Account - MT103 & MT202
- Booking Currency to Currency ISO Code mapping
- PM Currency List: Right now there's PM List replicated from Murex 2.11 which is to used to identify the currency is PM and driven the PM swift template generation( MT604/MT605/MT692). N**eed to confirm with PO & users if there's new PM entity to be added for new onboarding entity, CR is required to release to production.**
- Other UDF tables we copied from Murex 2.11 driving the PM swift generation. N**eed to confirm with PO & users if there's new PM entity to be added for new onboarding entity, CR is required to release to production** - UDF_Strategy - UDF_SWF_LS
- GUI Swift query with tag 20: Right now RATAN is query the swift message from different source | **Function Flow** | **Entities** | **Swift Message Source** | **Query Condition** | **Tag 20 logic** | **Comment** | | --- | --- | --- | --- | --- | --- | | BCS Stella | SG/UK/Jersey/HK | FMSRE | Tag 20 | EQ + Branch Code + Cashflow ID | This is in the BCS Stack only not in the Strategy stack, put here for information only. | | Egypt/Nepal/Saudi | Egypt/Nepal/Saudi | FMSRE | Tag 20 | FX + Branch Code + Cashflow ID | | | LOANIQ | LOANIQ entities | BLADE/S2BX/CFETS | Tag 20 | LQ+ Branch Code + Cashflow ID | | | FMRP | SG/MY/IN/CN | RATAN | cashflow ID | | |

# Accounting Generation Local Static Data

- Branch code & Transaction code: **Need to get the branch code for new entity & release by CR.**
- Booking Currency to Currency ISO Code mapping: **Need to get the new booking currency & ISO Code from ops/PO & release by CR.**
- eBBS Bridge Account: **Need to get the new account number from eBBS team for new onboarding entity & release by CR**

# GUI Dropdown & Query

- Cashflow blotter query dropdown
- Dashboard query dropdown

# Downstream Engagement

- RATAN EOD: **Check with them if there's report related to the new entity in case they need to do report migration.**
- SSDR: **Check with them if they need additional cashflow information from RATAN for new onboarding entity.**
- CIS: **Check with them if they need additional cashflow information from RATAN for new onboarding entity.**
- FMMIS: **Check with them if they need additional cashflow information from RATAN for new onboarding entity.**