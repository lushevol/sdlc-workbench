**Table of Contents**

**

# ***Document History***

| Version | Date | Author | Description of Change |
| --- | --- | --- | --- |
| V0.1 | 2023-Sep-25 | Feng, Lina | - Added Multi Exception; Netting and Nostro Static |
| V0.2 | 2023-Oct-12 | Du, Jill | - [Hold/Unhold Cashflow](https://confluence.global.standardchartered.com/display/DSP/CN+Ratan+Processing+Guide#CNRatanProcessingGuide-Hold/UnholdCashflow) - [Manually Net/Un-Net Cashflow](https://confluence.global.standardchartered.com/display/DSP/CN+Ratan+Processing+Guide#CNRatanProcessingGuide-ManuallyNet/Un-NetCashflow) - [Cashflow Suppression](https://confluence.global.standardchartered.com/display/DSP/CN+Ratan+Processing+Guide#CNRatanProcessingGuide-CashflowSuppression) - [Swift Suppression](https://confluence.global.standardchartered.com/display/DSP/CN+Ratan+Processing+Guide#CNRatanProcessingGuide-SwiftSuppression) |
| v0.3 | 2023-Oct-20 | Feng, Lina | - Added User Access; Suppression Rule; Cashflow Blotter |
| v0.4 | 2024-Apr-30 | Pradeesh Lakshmanan | - Added China Drop 2 handling in section 8 |
| v0.5 | 2024-May-06 | Dinesh, Arockia | - Added Dashboard section |
| v0.6 | 2024-Jun-25 | Feng, Lina | - Added swift message, accounting details in chapter 5 cashflow blotter - Added bulk process in section 6.2 Exception Handling - Added CCIL netting in section 6.5 manually netting |
| v0.7 | 2024-07-01 | Cordelia Sumita | - DOI of Lien Monitoring between Murex & RATAN |
| v0.8 | 2024-10-08 | Feng, Lina | - Added 6.2.6 Multi Exception Query - Added 6.5.6 NDS Fixing Netting - Added 5.7 New Fields for 2024 H2 UK&AG go live |
| v0.9 | 2024-11-05 | Xue, Carrie | - Added LOANIQ specific change in - 5.7 New Fields - 6.2.1. Exception Type - 9 LOANIQ highlights |
| v1.0 | 2024-11-20 | Feng, Lina | - Added 6.5.7 Beneficiary BIC Netting - Added 6.9 RFR and Swap Agent |
| v1.1 | 2025-03-27 | Dinesh, Arockia | - Added 5.3.1 Guidelines on Routing number for FEDWIRE / SORT CODE |
| V1.2 | 2025-07-29 | Sylvia. Huang | - Korea Exception Blotter |
| V1.3 | 2025-07-29 | Xue, Carrie | - Added SWAP AGENT(SAL*) payment type in 5.7 - Added new type to 6.1.5 - Added new exception to 6.2.1 - Added auto netting to 6.6.8 |
| V1.4 | 2025-10-16 | Xue, Carrie | - Updated manual fail to maker/checker requested and bulk allowed in 6.2.1 Exception Type - Added 6.5.3 Send to WAITING |
| V1.5 | 2025-11-03 | Hou,Grace | - Added 'Hard Block Swap Agent' Exception to 6.2.1 - Added 6.6.1-4 Add blocker from manual netting side for Swap Agent hard blocker |
| V1.6 | 2025-11-19 | Xue, Carrie | - Added 6.11. Split/Auto Distribution |
| V1.7 | 2026-03-08 | Dinesh, Arockia | - Updated section 2.5 on available Tiles |
| V1.8 | 2026-04-03 | Xue Carrie | - Add the linkage for RFI nostro stamping details to *3. Static Maintenance* |
| v1.9 | 2026-04-15 | Feng Judy | - Add the linkage for Quick Search and Custom Filter query validation |
| v2.0 | 2026-04-29 | Wang, Nick Long | - Add group blotter user manual deliver |
| v2.1 | 2026-05-19 | Xue, Carrie | - Add new section 5.3.2 cross border debit |
| v2.2 | 2026-05-22 | Song, Yinghua | - Add Korea Vostro static data |
| V2.3 | 2026-06-03 | Xue, Carrie | - Add new section for inter entity netting |
| v2.4 | 2026-07-09 | Li1, Johnny | - Add new seciont for last mile check, phase 1 technical golive |
| V2.5 | 2026-07-21 | Xue, Carrie | - Add new section 5.8 SSI ID population |
| V2.6 | 2026-07-28 | Song, Yinghua | - Add Korea Settlement Section |
| V2.7 | 2026-07-29 | Hou,Grace | - Delete 'Hard Block Swap Agent' Exception to 6.2.1 - Delete 6.6.1-4 Add blocker from manual netting side for Swap Agent hard blocker |
| V2.8 | 2026-07-29 | Hou,Grace | - Add UI indicator for autoDVP in 5.2.1 |
| V2.9 | 2026-09-15 | Xue, Carrie | - Add DVP exception and auto DVP info in 6.2.1 |
| v.2.10 | 2026-09-17 | yang3, chen | Add Stella CCIL Netting in 6.6.6 |

# *Overview*

## *Introduction*

Currently Derivative trades and cashflows are processed in MXG 2000 (Murex2.11 or MX2.11) system, which is a legacy system and in the process of decommission due to obsolescence risk. The FM re-platforming programme is implementing a decommissioning strategy which will migrate cashflow to the FM target platforms (RATAN) for settlements processing, including cashflow lifecycle management, SSI Stamping, Netting process, Suppression, Hold/Unhold, USD Limit Control and etc. The decommission will be phases and first phase is to migrate Murex 2.11 cash settlements of CHINA to FMRP strategic cash stack in Nov 2023 ahead of the Trade Migration which is planned for 2024.

## *User Access*

<u>*[FMRP RATAN UAT User Access - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/FMRP+RATAN+UAT+User+Access)*</u>

<u>*[How to apply for RATAN ONE access - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/How+to+apply+for+RATAN+ONE+access)*</u>

## *Data Entitlement*

*[FM-CES Entitlement Policy (Data Sovereignty) - Country Requirements - FM COO - Conduct and Controls - Confluence](https://confluence.global.standardchartered.com/display/FMCOOCC/FM-CES+Entitlement+Policy+%28Data+Sovereignty%29+-+Country+Requirements)*

*By regulatory requirement, Ratan integrated with FMCES on data entitlement, allow OPS to view on need to know basis, different profile/location would see cashflows only under allowed list of entities. *

*When seeing below error, it indicates that you don't have data entitlement properly setup, please r*aise FMCES request to obtain data entitlement.

![image-2026-4-20_11-26-40.png](attachments/image-2026-4-20_11-26-40.png)

Please refer below guide to request CES onboarding:

📎 [RATAN Access - After CES Go Live.docx](attachments/RATAN Access - After CES Go Live.docx)

## *Profiles*

| Request Category | Request Group | Request Sub-Group | Role | Request Data Entitlement Role | New/Existing |
| --- | --- | --- | --- | --- | --- |
| RATAN Function Access Role | FMO | Business Rule Approver | FMO_BR_APR | Global/GBS/Onshore | New |
| RATAN Function Access Role | FMO | Business Rule Maker | FMO_BR_MKR | Global/GBS/Onshore | New |
| RATAN Function Access Role | FMO | MO User | FMO_MO | Global/GBS/Onshore | Existing |
| RATAN Function Access Role | FMO | MO Super User | FMO_MO_SUP | Global/GBS/Onshore | Existing |
| RATAN Function Access Role | FMO | Operations User | FMO_OPS | Global/GBS/Onshore | Existing |
| RATAN Function Access Role | FMO | Operations Back Office Officer | FMO_OPS_BO | Global/GBS/Onshore | New |
| RATAN Function Access Role | FMO | Operations Back Office Clerk | FMO_OPS_BOC | Global/GBS/Onshore | New |
| RATAN Function Access Role | FMO | Operations Back Office Leader | FMO_OPS_BOL | Global/GBS/Onshore | New |
| RATAN Function Access Role | FMO | Operations Back Office Manager | FMO_OPS_BOM | Global/GBS/Onshore | New |
| RATAN Function Access Role | FMO | Operations Investigator | FMO_OPS_INV | Global/GBS/Onshore | New |
| RATAN Function Access Role | FMO | Operations Maker | FMO_OPS_MKR | Global/GBS/Onshore | New |
| RATAN Function Access Role | FMO | Operations Super User | FMO_OPS_SUP | Global/GBS/Onshore | Existing |
| RATAN Function Access Role | FMO | FMO Read Only User | FMO_RO | Global/GBS/Onshore | Existing |
| RATAN Function Access Role | FMO | Static Data Checker | FMO_STA_CKR | Global/GBS/Onshore | Existing |
| RATAN Function Access Role | FMO | Static Data Maker | FMO_STA_MKR | Global/GBS/Onshore | Existing |
| RATAN Function Access Role | NON FMO | NON FMO Read Only User | NON_FMO_RO | Global/GBS/Onshore | Existing |
| RATAN Function Access Role | PSS | PSS | PSS_RO | Global/GBS/Onshore | Existing |
| RATAN Data Entitlement Role | N/A | N/A | GBS | GBS | New |
| RATAN Data Entitlement Role | N/A | N/A | Global | Global | New |
| RATAN Data Entitlement Role | N/A | N/A | Onshore | Onshore | New |

## *Architecture*

**

*High Level Architecture*

![High Level Architecture.JPG](attachments/High Level Architecture.JPG)

## *FMO Post Trade Portal*

*FMO Post Trade Portal is a unified one stop service for Post Trade users. The Portal is based on Micro Frontend (MFE) framework, which lays the foundation for a unified & seamless user experience for FMO post trade users across multiple functions by accessing the relevant services & systems in a single UI, doing away with the need to log-in to multiple applications. Different Components / systems are displayed as Tiles within the same GUI. Access is controlled by respective systems. Currently the components that are live are *

- *Trade Processing* - *Trade Blotter*
- *Settlement* - *Cashflow Blotter [FX & Equity]* - *Cashflow Blotter* - *Grouping Blotter* - *Cashflow Dashboard*
- *Exception Management* - *Validation Exceptions (Confirmations)* - *Settlement Exceptions*
- *Business Rules* - *Authorization Limits* - *Settlement NSTP Rules (New)* - *Settlement NSTP Rules [FX & Equity]* - *Suppression Rules [FX & Equity]* - *Suppression Rules [Swift]* - *Suppression Rules [Cashflow]* - *Auto Netting Rules*
- *Static* - *Netting Static* - *Nostro Static* - *BIC Netting Static* - *Nostro Threshold Static*
- *SSDR *

## *Login*

*Access Link [FMO Post Trade Portal (standardchartered.com)](https://fmo-mfe.gdc.standardchartered.com:8453/)*

*Click on SSO*

![image-2025-10-9_14-22-44.png](attachments/image-2025-10-9_14-22-44.png)

*Access Forge Rock Application on mobile. Accept the Notification (or) key in the OTP and click on Log In*

*![image2023-10-28_10-28-28.png](attachments/image2023-10-28_10-28-28.png)*

*You will be logged on to the** Home **Page.*

*![image2023-10-28_10-30-58.png](attachments/image2023-10-28_10-30-58.png)*

*Click on** 'Find Tile' / 'New Tile' to view the available Tiles, which will vary based on the user's allotted access.*

*![image2023-10-28_10-31-49.png](attachments/image2023-10-28_10-31-49.png)*

# *Static Maintenance*

[Netting and Nostro Static - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/Netting+and+Nostro+Static)

- Field mapping | Field in UI | Field in the rule | Comment | | --- | --- | --- | | Client Type | Entity/Client Type | fmEntity/fmAccount/fmType only work in NSTP rule, not for other rules | | | | |

[BIC Netting Static - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/BIC+Netting+Static)

[RFI Nostro stamping based on Portfolio - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/RFI+Nostro+stamping+based+on+Portfolio)

Korea Vostro static data:

1. When swiftType = MT103 or (swiftType = MT202 and settlementMeans = Over-Account), as vostro 58/59 beneficiary account can't be empty, please fill in ‘DUMMY’ instead of NULL value (not case- sensitive).
2. In order to identify Internal Movement, 5338 & 5339 in TIS, vostro 58/59 beneficiary account need to start with ‘BR%’.

# *Business Rules Maintenance*

[Business Rules Maintenance - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/Business+Rules+Maintenance)

# *Cashflow Blotter*

RATAN ONE BCS fetches the BCS cashflows data from TDS3.

RATAN ONE Strategic Settlement fetches the cashflows data from RATAN as we are the golden source of FMRP & Murex cashflows.

Cashflow Blotter, shows all the cashflow list and related info. In this tile, user can process cashflows / view details including cashflow history and trade details (if trade was booked in FMRP).

User actions : [User Actions on Cashflow Blotter - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/User+Actions+on+Cashflow+Blotter)

## How to search a cashflow

<u>Quick Search</u>

- User can use "Quick Search" as below to search trade. Fields in "Quick Search" are fixed.
- Once Filter is selected, click on Search button, it will return cashflow satisfies the condition.
- User search condition should follow <u>[query validation](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3684478597)</u><u> </u>after validation passed then will trigger query.

![image-2026-2-5_14-24-24.png](attachments/image-2026-2-5_14-24-24.png)

Noted: For UK region user, suggest to using **Value Date** + **Booking Entity** + **FM Code** to search for better query performance.

<u>Custom Search</u>

- User can click "Create Or Modify" button to create complex filters with more available fields and save the filter condition for future use.

![image-2026-2-5_14-19-34.png](attachments/image-2026-2-5_14-19-34.png)

- When user fill in the filter name, this filter can be created for further use.
- If it's just one time search, then user can directly click on Search Button.
- if Is Private flag is checked, this filter will only be visible to current user, else this filter will be visible to all users.
- User search condition should follow <u>[query validation](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3684478597)</u><u> </u>after validation passed then will trigger query or save filter.

![image-2026-2-5_14-21-15.png](attachments/image-2026-2-5_14-21-15.png)

How to create a customized view

- User can click "Create Or Modify" button to customize the displayed column in trade blotter and save for future use.

![image-2026-2-5_14-29-7.png](attachments/image-2026-2-5_14-29-7.png)

- The available fields are categorized, user can search the field in the header and drag the field to "Display View" or click the icon in the Display view to delete the field from Blotter view.
- User can add View name in the header and click "Create View" button to save the config.
- if Is Private flag is checked, this view will only be visible to current user, else this view will be visible to all users.

![image2023-10-18_13-42-40.png](attachments/image2023-10-18_13-42-40.png)

## Cashflow Details

- In cashflow list, to check cashflow details, you can right click on the cashflow, then select View Cashflow Details or double click on cashflow.

![image2023-10-18_13-8-6.png](attachments/image2023-10-18_13-8-6.png)

- In Cashflow details, it has Trade Detail on the top. For further trade info, can click on Open Trade Details button. Note: MX2.11 Trades will not be available.
- A pop-up dialog box will appear with Cashflow Details.
- Cashflow Status changes are shown on the right side.
- In middle, it would have Action history, in which, user manual actions will be displayed.
- For Vostro and Nostro Info, please refer to <u></u> for more details.

![image2023-10-18_13-45-0.png](attachments/image2023-10-18_13-45-0.png)

- “DVP received” tag in cashflow details indicates either: - - the DVP exception was auto closed by RTA, or - the cashflow bypassed NSTP exception handling due to RTA receipt. - If the DVP exception is manually closed by Ops, the “DVP received” tag will not be added

![image-2026-7-9_17-29-0.png](attachments/image-2026-7-9_17-29-0.png)

## SWIFT Generation

Effective Jul 2024, RATAN will generate SWIFT message directly for selected entities and sent to FM Swift Gateway (FMSGW). (LOANIQ,EG,NP,SA swift are still generated by Razor)

RATAN will generate SWIFT only if Settlement Means is 'NOS' or 'Over-Account'. For other Settlement Means (Example: WMSUS), SWIFT will not be generated.

For deals requiring settlement to wealth management suspense, the cashflow must be settled to Settlement Means 'WMSUS' and Settlement Account also as 'WMSUS'. Existing SSI's with WM/AEB flag have already been updated in SSI+ as 'WMSUS' in Settlement Means and Account

How to check cashflow's SWIFT Message

- In Cashflow details, it has SWIFT Message tab on the top, which will provide the SWIFT Message if released.
- MT message generated by Ratan (CN,MY,IN,SG) - downstream is FMSGW. Field 20 reference will start with DV
- MT message generated by Razor (LOANIQ, EG, NP, SA) - downstream is FMSRE. Field 20 reference for Loaniq will start with LQ and for EG/NP/SA it will start with FX.
- In future, MX message will be generated by Ratan - downstream will be TBC
- [Details can be found in ](https://confluence.global.standardchartered.com/display/DSP/FMRP+Swift+Generation)<u>[FMRP Swift Generation - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/FMRP+Swift+Generation)</u>

Sample of SWIFT Message below.

![image2024-6-25_16-14-35.png](attachments/image2024-6-25_16-14-35.png)

New fields have been added to Cashflow Blotter to show the SWIFT message type and the status of the SWIFT (Not applicable for LOANIQ, EG,NP,SA)

Notes: In case of any pre-validation failure (e.g. status is not expected, duplication check), Cashflow Swift Status will be showing as 'Ratan Internal Error', the main Cashflow State will have no change as RELEASED. If this happens, need to check Swift tabs via cashflow details to see if Swift message generated or not.

![image2024-6-28_14-39-48.png](attachments/image2024-6-28_14-39-48.png)

In case of any errors in SWIFT generation or in downstream, it will be shown in Dashboard (Not applicable for LOANIQ, EG,NP,SA)

![image2024-6-28_14-18-42.png](attachments/image2024-6-28_14-18-42.png)

### Guidelines for Routing Number capture in SWIFT

![image-2025-3-27_20-6-29.png](attachments/image-2025-3-27_20-6-29.png)

### Cross Border Debit

- For <u>receive</u> flow, if settlement account is in format “CCY CROSSDEBIT” (such as USD CROSSDEBIT), then follow below swift mapping
- | Swift Tag | Field Name | Mandatory | MT202 CROSSDEBIT SI mapping | | --- | --- | --- | --- | | Block1 | Message sender | Y | Vostro SI 57BIC | | Block2 | Message receiver | Y | Vostro SI 57BIC | | 52 | Ordering Institution | Y | Vostro SI Bene detail (58) | | 53 | Sender's Correspondent | Y | bene Account in vostro (58) | | 57 | Account With Institution | Y | Nostro agent BIC (53) | | 58 | Beneficiary Institution | Y | Legal entity BIC |
- no impact to accounting process
- the cashflow feed will be sent to LMS, if new entity onboard the cross border debit account, need to inform LMS to config the mapping

More details updated to [FMRP Swift Generation - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/FMRP+Swift+Generation)

## Accounting Generation

(Not applicable for LOANIQ, EG,NP,SA)

Effective Jul 2024, RATAN will generate Accounting message directly for selected entities (CN, IN, SG, MY) and sent to eBBS via real time feed.

How to check cashflow's accounting Detail

- In Cashflow details, it has accounting detail tab on above, which will provide the accounting details if cashflow is in RELEASED/SETTLED/FAILED/SWIFT_SUPPRESSED status.
- If payment has reached value date, accounting will be in SENT status; else will be in HOLD status and waiting for value date, 6 AM local time on VD will be sent to EBBS. For Korea entity,accounting will sent to OLTP.
- If cashflow is withdrawal/ reinstated / unsuppressed, an reversal accounting entry will be posted. When FAILED cashflow goes to RELEASED status, a new entry will be sent.
- If there is technical NACK from EBBS, RATAN will retry 3 times within 3 mins. If it's still failed, Ops user can raise a ticket to RATAN PSS for manual retrigger.
- Details can be found in <u>[Cash Settlement - Accounting - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/Cash+Settlement+-+Accounting)</u>

![image2024-6-25_15-57-39.png](attachments/image2024-6-25_15-57-39.png)

New fields have been added to Cashflow Blotter to view the Accounting status

![image2024-6-28_14-41-31.png](attachments/image2024-6-28_14-41-31.png)

In case of accounting issues, it will be highlighted in the Dashboard

![image2024-6-28_14-42-36.png](attachments/image2024-6-28_14-42-36.png)

## **Cashflow History**

How to check cashflow history

- Select history tab to view cashflow history
- In Cashflow History, it shows basic change for the cashflow.
- If more details is required, can click on Show Details button on the right side. It shows the difference between current version and previous version.

![image2023-10-18_13-50-5.png](attachments/image2023-10-18_13-50-5.png)

![image2023-10-18_13-51-32.png](attachments/image2023-10-18_13-51-32.png)

## **Trade Info**

- In cashflow list, to check cashflow's trade details, you can right click on the cashflow, then select View Trade Details or double click on cashflow, then choose Open Trade Details.
- Trade Details is queried from SABRE-TDS3. MX2.11 Trades are not available

![image2023-10-18_13-8-20.png](attachments/image2023-10-18_13-8-20.png)

![image2023-10-18_12-58-42.png](attachments/image2023-10-18_12-58-42.png)

## **New Fields**

**Is Pending Fixing**

Indicator from Murex 2.11 to mark if the cashflow C1 is pending fixing which need to be held as pending another leg.

If the value is X, it means cashflow is pending for the actual true/false value from Murex.

- **No manual touch from ops user **before the actual value is updated.
- ![image2024-11-25_13-52-18.png](attachments/image2024-11-25_13-52-18.png)![image2024-11-25_14-27-34.png](attachments/image2024-11-25_14-27-34.png)

If the value is true, cashflow will be in WAITING + Pending another leg status.

- Once floating cashflow C2 is fixed in Murex, C1 & C2 will be auto netted as N1 in Murex.
- Then Murex will send C1 reversal and N1 to RATAN.

If the value is false, cashflow will go through rest checking for STP.

**Clearing Alpha**

Indicator from Murex 2.11 to mark  if the cashflow C1 is pending to be cleared。

If the value is true, cashflow will be in WAITING + Pending Exception status.

Once the trade is cleared in Murex, Murex will send C1 reversal, and cashflow C2 with clearing house as the counterparty.

**Payment Type**

Field Payment Type will identify the cashflow type as

For Murex Swap Agent, value includes:

- Initial Notional
- Interim MTM
- Coupon
- Final Notional

For netting type, current value includes:

- Bilateral Netting
- CCIL Netting
- Ben BIC Netting
- NDS Fixing Netting
- SAL Coupon Netting
- SAL MTM Netting

**Is Commodity**

Indicator from Murex 2.11 to mark if Commodity & non Commodity product.

**Is Netting Required** (for LOANIQ)

Indicator to show if netting required.

There is NSTP rule created in RATAN to hold the cashflow if the value is true.

**General Ledger Owner Id **（for LOANIQ）

Indicator to link the payment in LOANIQ.

if the cashflow hit "Netting Required" exception, ops user should check and net the cashflow with the same general ledger owner id.

**Trade Purpose**

‘Trade Purpose’ field will tactically capture the Strategy information for ePM deal cashflows flown from STELLA and needs to be referred for Settlement Processing in same way as ‘Strategy’ field is used for Murex Cashflows.

![1.png](attachments/1.png)

## SSI ID population

- system auto stamped SI: SSI ID is populated
- user manually enter vostro SI: SSI ID is blank
- User select from available SI and submit without any changes: system set the SSI ID value with the selected SI ID.
- For auto stamped SI or user selected SI, - user update only 70/72 values, - system will keep the SSI ID - system will highlight "Field 70/72 Customized" as below (only highlight 70/72 update when SSI ID exist and user updated 70/72; if no SSI ID, no such highlight field show up.) ![](https://confluence.global.standardchartered.com/download/attachments/3722335608/image-2026-7-8_14-37-30.png?version=1&modificationDate=1783492651000&api=v2) - user update values other than 70/72 fields, system will remove the SSI ID
- User select from available SI, update any field, then manually update back to original values, system remove SSI ID as user manually updated the SI, even the value is the same as original
- if maker select from available SI, checker manually input the same value, system will consider this as different input and popup validation error
- if maker select SSI, checker will not see the SSI ID maker selected
- user approve the cashflow when vostro SI in edit mode, SSI ID should not be impacted if user does not update SI

# *Settlements Processing*

## Monitoring

### API Status

Cashflow Blotter will display the API status as Green if all services are up and running. If there is any issue, it will be shown in Red. Settlements team can raise the issue to PSS to investigate the issue.

![API status1.JPG](attachments/API status1.JPG)

Clicking on the Api status will display the list of Apis and their status

![API status2.JPG](attachments/API status2.JPG)

Sample for API down status

![APIstatusCapture.JPG](attachments/APIstatusCapture.JPG)

### Pending Items

Settlements team need to constantly monitor and clear the queue for items that are pending for user action. All Cashflows should have moved to SETTLED status well in time before each Nostro agent currency cutoff (except for NETTED, CANCELLED, CASHFLOW SUPPRESSED, SWIFT_SUPPRESSED, DEAD).

Refer to the Cashflow status section for each status description.

At EOD Manager / delegate should evidence that there are no items pending for value today / early currency value tomorrow.

- Waiting Status : All Cashflows that are flown in for the first time (New / Amend / Cancel) and require manual action are tagged as 'Pending Operator' or 'Pending Verification'.

Cashflows that are value today / tomorrow and pending for Ops action are highlighted on the right section, split by Pending Operator (Maker) and Pending Verification (Checker)

![Pending Items.JPG](attachments/Pending Items.JPG)

By clicking on either value today or value tomorrow cashflows automatically filter to the specified criteria setup for value today or value tomorrow and only show value today or value tomorrow in the cashflow blotter

![Pending Operator.JPG](attachments/Pending Operator.JPG)

- Failed Status : Cashflows (Auto or Manual Failed)

Cashflows not affirmed due to various reason and are identified as fail is to be moved to Failed status by right clicking the selected cashflow and clicking Fail

![Failed status.JPG](attachments/Failed status.JPG)

- Released Status : Normally these should move to SETTLED when Ack'd by AMH

![Released.JPG](attachments/Released.JPG)

- Ready Status: If Sub Status is 'NA', it means that the cashflow is not yet released from RATAN, waiting for release time. If the sub status is Pending Ack, then it means that cashflow has been sent to RAZOR and waiting for Ack.

![image2023-11-10_10-44-27.png](attachments/image2023-11-10_10-44-27.png)

- Hold Status : Put on hold by a user previously

![Hold.JPG](attachments/Hold.JPG)

- ERROR status: Mandatory attributes required by RATAN are not received. Normally this is not expected to happen. But if encountered, raise the issue to RATAN PSS if unable to identify the reason. If it's a MX2.11 cashflow and the missing field is known, raise the issue to MX2.11 PSS.

![image2023-11-10_18-12-10.png](attachments/image2023-11-10_18-12-10.png)

Note: If there are more than 500 records, only the first 500 records are being displayed. If any column filters are selected, they will be applied only within the records displayed, not on the entire population. Warning is provided on screen to indicate this.

User should apply filters to reduce the results below 500 if they intend to view all cashflows fitting within a criteria

![500 cashflows.JPG](attachments/500 cashflows.JPG)

As an example below, there are totally 90050 cashflows, but only first 500 are displayed.

If user applies currency filter as 'AUD', search is done only within the first 500 records will be displayed - here no AUD cashflow is displayed.

![AUD1.JPG](attachments/AUD1.JPG)

Whereas if custom filter is used to fetch 'AUD' cashflows, system displays all AUD cashflows within the total population of 90050 cashflows.

![AUD2.JPG](attachments/AUD2.JPG)

![AUD4.JPG](attachments/AUD4.JPG)

### Cashflow Status

Below are the Cashflow Statuses (Main status)

| flow Status | Process Step | User Description / Action Required |
| --- | --- | --- |
| PROJECTED | STELLA generates cashflow | Cashflow generated but not yet due for settlement (beyond 5 days from Current calendar date) |
| QUEUED | RATAN materializes the Cashflow & checks for exceptions | Cashflow due for settlement, system does the validation checks to determine if exceptions are present |
| WAITING | Cashflow has exceptions which require manual action | Cashflow specifically waiting for user to resolve the exception. Resolve the exceptions before each cutoff |
| READY (sub status NA) | No exceptions found / Exceptions resolved and waiting for release | Cashflow waiting for auto release to downstream when release time is reached. Ensure no cashflows are in this status before each cutoff. Any changes to release time must be agreed with LMS team as the funding cutoff times must be adhered to |
| READY (sub status 'Pending Ack') | Cashflow has been sent downstream and pending Ack | Cashflow waiting for downstream Ack. Ensure no cashflows are in this status before each cutoff |
| RELEASED | Cashflow has been Ack’d by FMSRE | Cash flow message has been released to payment gateway. Ensure no cashflows are in this status before each cutoff |
| SETTLED | Cashflow has been Ack’s by AMH / SCPAY | Released from payment gateway (or) no SWIFT required for receipt |
| NETTED | Cashflow has been Netted in RATAN | Cashflow has been netted part of a netting set and replaced by a net cashflow |
| SPLIT | Cashflow has been Split in RATAN | Cashflow has been split into multiple payments **(only status added, split feature not yet built)** |
| CANCELLED | Withdrawal received from upstream into RATAN | Cashflow has been cancelled due to a trade event |
| SWIFT_SUPPRESSED | Payment / Receipt is Suppressed | No SWIFT or Settlement Accounting will be generated |
| CASHFLOW_ SUPPRESSED | Cashflow is Suppressed (Both SWIFT and Accounting) | No SWIFT or Settlement Accounting will be generated |
| FAILED | Cashflow is left in WAITING status till EOD | Cashflow not processed and marked as failed by system or user. No SWIFT or Settlement Accounting will be generated. Ensure no cashflows are in this status before each cutoff or the reason is known |
| DEAD | Un-net is done in RATAN (status is for Net Resultant Cashflow) | Net resultant Cashflow has been cancelled due to Un-net action |
| HOLD | Cashflow is put on hold in RATAN by user | Cashflow has been put on hold by user. Ensure no cashflows are in this status before each cutoff |
| ERROR | Technical Issue | Mandatory attribute missing from upstream, raise to PSS. Ensure no cashflows are in this status before each cutoff |
| RATAN_SUSPENDED | Cashflow is suspended(Settlement in Razor) | Cashflow is suspended(Settlement in Razor) |

*![Cashflow Status.JPG](attachments/Cashflow Status.JPG)*

### *Cashflow Sub State*

- *Pending Operator (Maker)*
- *Pending Verification (Checker)*

*![sub status.JPG](attachments/sub status.JPG)*

### *Cashflow Sub State Type*

- - *Pending Netting: Cashflows are tagged for Netting and require user to either Net or process them Gross* - *Pending Exception: Cashflows have an exception(s) and require manual action* - *Pending Another Leg: Cashflow is from an IRS deal is waiting for another cashflow leg (configured only for STELLA cashflows)* - *Reversal Rebook: Cashflow has been amended* - *Cashflow Suppression: Interim status where Maker has done the Cashflow Suppression and waiting for Checker approval* - *Swift Suppression: Interim status where Maker has done the SWIFT Suppression and waiting for Checker approval* - *Undo Cashflow Suppression: Interim status where Maker has done the Undo of Cashflow Suppression and waiting for Checker approval* - *Undo Swift Suppression: Interim status where Maker has done the Undo of SWIFT Suppression and waiting for Checker approval* - *Pending Auto Netting: Cashflows are tagged for system to net automatically*

*![sub state type.JPG](attachments/sub state type.JPG)*

## *Exceptions Handling

**ANCHOR: Multi Exception**
*

- The Cashflow will be NSTP based on the exceptions setup. If there are no exceptions found, it will be STP.
- The exceptions are setup in line with business workflow. Exceptions and expected actions captured under confluence page: <u>[NSTP Workflow - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/NSTP+Workflow)</u>
- So when there's new cashflow received in Ratan, it would be published to the settlement workflow and run through the exception types and decide if we need to tag this exception to the cashflow.
- Exceptions are triggered based on backend configuration (example: Missing Vostro) or the NSTP rule setup (example: WHT Client)
- Sub state type is Pending Another Leg - followup for fixing / check if there is only one leg for the value date

### Exception Type

<u>Actions permitted on Cashflows (depending upon Cashflow status)</u>

| Action | Maker / Checker | Bulk Allowed? | Comments |
| --- | --- | --- | --- |
| SI Input | Maker + Checker | No | Dual Blind Input except address and field 70 / 72 |
| Send to Gross | Maker + Checker | Yes | Checker will get exception in Cashflow detail page |
| Swift Suppression | Maker + Checker | Yes | |
| Cashflow Suppression | Maker + Checker | Yes | |
| Reinstate | Maker + Checker | Yes | Checker will get exception in Cashflow detail page |
| Un-suppress | Maker + Checker | Yes | |
| Hold | Maker Only | Yes | Release cannot be done by same user |
| Add Comment | Maker Only | Yes | |
| Early Materialization | Maker Only | Yes | |
| Update Affirmation | Maker Only | No | |
| Manual Fail | Maker + Checker | Yes | |

- Below are the baseline Exceptions

**EXPAND: Exception Type**

**EXPAND_END**

Further Exceptions are configurable as per BAU requirement. Below are the current list of Exceptions setup for China Day 1:

![NSTP Exceptions.JPG](attachments/NSTP Exceptions.JPG)

- <u>Maker only exceptions</u> - Pending Affirmation

- <u>Maker/Checker exceptions</u>

| Exception | Reason | Resolution |
| --- | --- | --- |
| Missing Vostro | Vostro is missing, more details can be found in <u>[FMRP - SSI Stamping Flow]</u> | Setup SSI / Manual Input SSI |
| Multi Vostro | Multi Vostro stamped on the cashflow, more details can be found in <u>[FMRP - SSI Stamping Flow]</u> | Select from Multiple Vostro |
| Missing Nostro | There's no Nostro defined for particular 'Legal Entity'/'Currency', more details can be found in <u>[FMRP - SSI Stamping Flow]</u> | Setup Nostro |
| GSAM Client | Cashflow's counterparty is 'GSAM Client', if it's legalEntity.operationStatus1Value if 'REFER' in SCI. | Users must obtain approval from GSAM team before releasing payment to client |
| Back Value | Value date of payment is less than current calendar date | Select the correct payment date based on whether Nostro agent will accept back value / cutoff available for current calendar date |
| Bad Business Day | The value date of the Cashflow is marked as a Holiday for the currency | Check with MO if the trade will be amended to a different value date Note: User can still release the payment if it will be settled by the Nostro Agent (example: partial holiday) |
| MUREX IRS | Cashflow belongs to IRS trade and flown from MX2.11. Murex will initially send the fixed leg to RATAN. Subsequently, when fixing is done on the floating leg, MX2.11 will send a reversal to the fixed leg and a new cashflow for the net amount of fixed + floating. | MX2.11 is not able to provide an indicator whether the cashflow is a fixed cashflow or the net amount, hence the NSTP condition is setup. Check in MX2.11 if this is Fixed leg and need to wait for Floating leg. If Net amount across Fixed&Floating legs, then can be released if matching with client amount |
| Reinstate | Cashflow was reinstated from FAILED | Check that the Client now recognizes the deal and right instructions are being used |
| CORP Client | Client type is Corporate as per SCI data | Release after affirmation with Client |
| Validate Bene Info | Beneficiary BIC is Blank on MT202 SSI | Check if the SSI setup is correct and whether payment can go out as MT202 with Bene Name i/o Bene BIC |
| STELLA related exceptions | New exceptions have been added as part of China Drop 2 on 06 May 2024 to cater to new events. | Refer to China Drop 2 section |
| Validate Bene Info | For the scenario when the swift message type is MT202 but Ben BIC is blank | Team to check and update BIC |
| Netting Required | to hold LOANIQ cashflow with "Is Netting Required" field as TRUE | Ops to check and net the cashflow with the same general ledger owner id. |
| Auto Netting | either the cashflow is netting resultant generated from auto netting or single cashflow without other cashflow to net with and released from auto netting queue after netting date time | Check that the net amount and SI are as per client instructions |
| Hard Block Swap Agent | single cashflow which is Swap Agent Coupon or Swap Agent Interim MTM ,after 'Settle As Gross' or resultant cashflow which one of the component cashflow is Swap Agent Coupon or Swap Agent Interim MTM will hit this NSTP hard blocker rule | Blocker Swap Agent Coupon &Swap Agent Interim MTM released from Ratan |

- <u>Checker only exceptions</u>

| Exception | Reason | Resolution |
| --- | --- | --- |
| Secondary Vostro | If the secondary vostro is selected according to best matching rule | Check that it matches with client's expectation |
| Reversal | Cancellation of deal post release of Payment | Check with MO that the cancellation is valid and release MT192/292. Only BOL and BOM profile user can approve |
| Rebook | Deal has been amended post release of Payment | - Check with MO that the amendment is valid - Only BOL and BOM profile user can approve - If non-financial amend, suppress cancellation and new payment - If financial amend: - If amount is amended, net the withdrawal and new to release different payment / receipt - If other attributes like counterparty, value date, currency etc are amended, release cancellation, confirm return of funds before making new payment |
| Adhoc_Netting | Netting done for Client who is not defined for Netting Details can be found in <u></u> | Validate against Client request and release. Only BOL and BOM profiles can release the cashflow |
| NetOverAmend | A cashflow that was netted has been amended | Check the amendment and release differential pay / receive. Only BOL and BOM profile user can approve Do not release the cancellation directly as original payment was for net amount |
| Withdrawal on Component | A cashflow that was netted has been cancelled | Check if valid cancellation and initiate recall of funds via Oscar/AMH. Only BOL and BOM profile user can approve Do not release the cancellation directly as original payment was for net amount |
| Net Cashflow | Cashflow is resultant from Netting action by maker | Check that the net amount and SI are as per client instructions |
| Settled as Gross | Client is tagged as Netting, but Cashflow was moved to Gross Details can be found in <u></u> | Check for TRM approval to release in gross |
| Previously Netted | If the cashflow was netted previously. Technical conditions are : 1. 1. Cashflow.Status_Event_Type == 'Un-Net' 2. Trade.Settlement_Method == 'Gross' | Check that it is valid to be released in Gross. |
| Other NSTP Exceptions | The cashflow matching with the NSTP Rule setup. The exception code will be displayed as per the setup. Examples are : WHT Client, Adhoc Netting Client, Structure Trade etc | To be handled based on BAU process for such exceptions |
| High Value | The payment amount is above USD 100 Mio | Follow High Value payment due diligence. Check that trade is matched / affirmed; Check the Instructions are as per Client request |
| Auto Netting | either the cashflow is netting resultant generated from auto netting or single cashflow without other cashflow to net with and released from auto netting queue after netting date time | Check that the net amount and SI are as per client instructions |

STELLA related exceptions

New exceptions have been added as part of China Drop 2 on 06 May 2024 to cater to new events. Refer to China Drop 2 section

Exceptions Handling in RATAN

Filter cashflow by 'Pending Exception' in Cashflow Sub State Type

![image2023-9-21_16-4-14.png](attachments/image2023-9-21_16-4-14.png)

Double click on the cashflow to display detailed exception.

All exceptions will be displayed on the right side.

![image2023-9-21_16-33-52.png](attachments/image2023-9-21_16-33-52.png)

Pending Affirmation Exception

**EXPAND: Pending Confirmation/Affirmation**

1. This exception will be generated if both parent trade affirmation/confirmation and cashflow affirmation are missing for the cashflow. To resolve the exception, either the trade must be matched or the cashflow must be manually marked as affirmed
2. To identify the confirmation status, **refer only to Trade Status field**. Do not refer to Confirmation Status as it will display confirmation internal statuses like PAIRED, PROPOSED etc 1. For Murex trade, status in Matched,PairedDiscrepHost,PairedDiscrepCounterparty,PairedAutomatically,PairedManually,PairedPaper,PairedPhone would be considered as confirmed and not generate the exception. 2. For FMRP trade, status in Matched|Full Affirm,Matched|Completed,Matched|Complete are considered as matched and not generate exception.

![image2024-8-8_13-47-13.png](attachments/image2024-8-8_13-47-13.png)

c.  Trade Status field will show in an unmatched status if the Trade state is in an Unconfirmed state (example: SENT / TOBESENT)

![image2024-8-8_13-50-19.png](attachments/image2024-8-8_13-50-19.png)

1. For cashflow status: 1. Affirmed: Not generate exception 2. Unaffirmed: Generate exception 3. Other: Generate exception
2. If the cashflow affirmation comes after trade confirmation match, no exception will be generated.
3. If cashflow is unaffirmed before trade confirmation match, exception will be generated. Once trade affirmed/confirmed later, exception will be removed automatically.
4. The 'Cashflow Affirmation' is fixed section in Maker's page. Only be editable when there's 'Pending Affirmation' exception.

To perform cashflow affirmation, double click on the cashflow to bring up the cashfow detail page and update the affirmation details as agreed with the counterparty

![affirm2.JPG](attachments/affirm2.JPG)

**EXPAND_END**

Vostro/Nostro Related Exception

**EXPAND: Vostro/Nostro Related Exception**

For Missing Vostro/Multi Vostro/Nostro vs Vostro Mismatch/Missing Nostro/adhoc SI exceptions, steps are as below:

a. Maker fill in/verify Vostro & Nostro form

To resolve the exeption, get the SSI setup in SSI+. If urgent, user can key in the SSI manually in the cashflow detail page. The checker must also key in the SSI details (Dual Blind input).

Checker should input the SSI based on the original source of the SSI from client, and not based on Maker's input.

Dual Blind Input is introduced as a key control to prevent Checker errors, hence Checker should not obtain the SSI info from Maker as screenshot or via chat

- - - Users must key in CAPITAL LETTERS - Special characters are not allowed (will be auto removed from SSI / SCI data - When exception is in pending operator status, Maker can select suggested Vostro from the available list, or use adhoc SSI. - Vostro can be manually keyed in if there are no Vostrso available. Nostro can only be selected (no key in option) - Validation between Vostro & Nostro required, settlement means & settlement account must be same. - If Settlement account & Settlement means are different between Vostro & Nostro, system will throw an error to the user. This exception generally generated during auto SSI Stamping. When querying Nostro and there is no unique Nostro, system will select primary Nostro, whose settlement means & settlement account may different with Vostro. It may also happen if user missing to select the right Nostro / made an error while selecting / keying in the Vostro details. - If an SSI has already been stamped and need to key in a new SSI, use 'Reset' button to clear the page and then key in the new SSI to avoid errors - If both Vostro and Nostro are missing, only 'Missing Vostro' will be triggered

![Missing Vostro.JPG](attachments/Missing Vostro.JPG)

![image2023-9-22_10-41-14.png](attachments/image2023-9-22_10-41-14.png)

Mandatory fields are highlighted in red.  When user selects message type as MT202 or MT103, some of information will be auto populated.

Note: For CHINA Day1, the country will be populated with the code (example: CN) and user must manually change it to Country Name (example: CHINA)

MT103:

![auto Capture.JPG](attachments/auto Capture.JPG)

<u>MT202:</u>

<u>![202Capture.JPG](attachments/202Capture.JPG)</u>

b. Checker fill in same Vostro & Nostro with Maker

When exception is in pending verification status, Checker can also select suggested Vostro from the available list, or use adhoc SSI.

Validation between Vostro & Nostro required, settlement means & settlement account must be same.

![image2023-9-22_10-50-53.png](attachments/image2023-9-22_10-50-53.png)

If Maker and Checker filled in the same Vostro & Nostro, exception will be resolved.

If Maker and Checker filled in different Vostro & Nostro, there is reminder for different value.

![image2023-9-22_11-7-41.png](attachments/image2023-9-22_11-7-41.png)

c. Checker Reject SSI

If Maker has put in the incorrect SSI, Checker can reject SSI, so the exception will be back to 'Pending Operator' status and Maker can re-fill in the SSI as step a.

![image2023-9-22_11-15-10.png](attachments/image2023-9-22_11-15-10.png)

SI Input for Field 70 / 72:

For field 70, no need to input "//", it will be automatically added during SWIFT generation. Sample below

![field 70 Capture.JPG](attachments/field 70 Capture.JPG)

{1:F01SCBLCNS0AXXX0000000000}{2:I202SCBLUS33XXXXN}{3:{119:COV}{121:7dd7e6e3-2058-4836-891b-8ea740c66392}}{4:
:20:MX73M00095051065
:21:MX73M00095051065
:32A:230809USD214500,
:57A:CITIUS33XXX
:[58A:/36082191](http://58a/36082191)
UBHKHKHHXXX
:[50K:/400108557](http://50k/400108557)
CITIC SECURITIES CO LTD
16F CITIC SECURITIES TWR NO48 BJG
China
:[57A:/36082191](http://57a/36082191)
UBHKHKHHXXX
:[59:/861530053779](http://0.0.0.59/861530053779)
CITIC SECURITIES CO LTD
16F CITIC SECURITIES TWR NO48 BJG
China
:70:Remittance Inform 1
//Remittance Inform 2
//Remittance Inform 3
//Remittance Inform 4
:33B:USD214500,
-}

For Field 72, need to input the "/REF/" in first line alone. Sample below

![72 Capture.JPG](attachments/72 Capture.JPG)

{1:F01SCBLCNS0ASHA0000000000}{2:I103SCBLUS33XXXXN}{3:{121:4c7d2c38-058e-41d4-ac34-107e315e073a}}{4:
:20:MX73M00095033386
:23B:CRED
:32A:230809USD968342,3
:33B:USD968342,3
:[50K:/400062278](http://50k/400062278)
CHAILEASE INTERNATIONAL SHA
ROOM 5102 NO 8 XING YI ROAD
CHINA
:57A:CITIUS33XXX
:[59:/1234567890](http://0.0.0.59/1234567890)
CHAILEASE INTERNATIONAL SHA
ROOM 5102 NO 8 XING YI ROAD
CHINA
:71A:OUR
:[72:/REF/Sender](http://0.0.0.72/REF/Sender) To Reciever 1
//Sender To Reciever 2
//Sender To Reciever 3
//Sender To Reciever 4
//Sender To Reciever 5
//Sender To Reciever 6
-}

Flip MT202

Both Nostro and Vostro Settlement Means should be 'Over Account' and 'CCY NO 2'. Beneficiary account number must be present - it will be captured as the debit account number. Sample below

![FlipMT202Capture.JPG](attachments/FlipMT202Capture.JPG)

{1:F01SCBLCNS0ASHA0000000000}{2:I202SCBLCNSXXSHAN}{3:{121:caafb7cb-3624-4ef9-9c33-e60134e9d4a4}}{4:

:20:MX73M00095209527

:21:MX73M00095209527

:32A:230810CNY29919,31

:[52A:/100100221259636019](http://52a/100100221259636019)

SCBLCNSXKMG

:[53B:/100100221259636019](http://53b/100100221259636019)

:57A:SCBLCNSXSHA

:[58A:/100000000003910205](http://58a/100000000003910205)

SCBLCNSXGMO

-}

**EXPAND_END**

Back Value

**EXPAND: Back Value**

a. Maker select new date as Vaule date and submit

b. Checker select the same date with maker  and submit

c. Checker reject the updated value.

If Checker select the different value date, there will be pop out message, then checker can reject the updated value.

So Maker reinput new value date according to Checker's comment as step a.

![back value.JPG](attachments/back value.JPG)

**EXPAND_END**

Bad Business Day

1. There're currency calendar defined in Ratan which is sourcing from RDM
2. Get the payment date from the cashflow and check if the payment date is falling on the holiday.

![image2023-9-25_15-42-17.png](attachments/image2023-9-25_15-42-17.png)

Review only exceptions

**EXPAND: NSTP exceptions**

For exceptions in GSAM Client/Reversal/Rebook/NetOverAmend/Adhoc_Netting/Net Cashflow/Settled as gross/Reinstated Cashflow/NSTP Exceptions/Corporate Client/High Value Payment/Auto Netting, only need review from ops maker/checker.

- Once Maker/Checker click on the 'submit' button in cashflow details page, these exceptions will be taken as approved in default, no value needs to be filled in.

**EXPAND_END**

Reinstated Cashflow Exception

**EXPAND: Reinstated Cashflow**

- - Settlement Ops perform 'Re-Instate' action on the 'FAILED' cashflow, cashflow status moved from 'FAILED' to 'QUEUED'.

![image2023-9-25_15-25-3.png](attachments/image2023-9-25_15-25-3.png)

- - The re-instate 'QUEUED' cashflow are pushed back to workflow and generate this exception.

![image2023-9-27_16-33-35.png](attachments/image2023-9-27_16-33-35.png)

**EXPAND_END**

CORP Client Exception

**EXPAND: CORP Client**

The rule would be defined with counterpart FMID/FM Code. If client type is 'CORP' in SCI, then populate this as 'Corporate Client' exception.

![image2023-9-25_15-37-38.png](attachments/image2023-9-25_15-37-38.png)

**EXPAND_END**

DVP Exception

**EXPAND: DVP Exception**

The following rules have been created separately for cashflows from Stella and Murex:

![image-2026-9-15_10-19-54.png](attachments/image-2026-9-15_10-19-54.png)

For the SCB receive over-account scenario, EBBS triggers RTA once client account is successfully debited , Ratan consumes the RTA and automatically closes the DVP exception from the corresponding pay leg.

- **NOTE**: If EBBS fails to generate the RTA, if RATAN fails to consume the RTA, or if the RTA is received but the corresponding pay cashflow cannot be identified, the cashflow will remain in the WAITING queue. In such cases, Operations may manually release the cashflow..

Further details are documented in [Auto DVP (eBBS) - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3596082442)

**EXPAND_END**

### Multiple Exceptions Handling

**EXPAND: Multi Exceptions**

- If there are multi exceptions, i.e. Pending affirmation and CORP client

a. Maker should updated all the exceptions and submit, exception will be in 'pending verification' status and ready for checker review

![image2023-9-25_15-0-8.png](attachments/image2023-9-25_15-0-8.png)

b. Checker can verify all the exceptions, and fill in the same value and approve the exception.

![image2023-9-25_15-12-58.png](attachments/image2023-9-25_15-12-58.png)

c. Checker can verify all the exceptions, and reject any single exception as above, then exception will be back to 'Pending Operator' for maker to refill in as step a.

For 'review only exception', it will be taken as approved if any other exception is approved.

Checker can only reject SSI related exceptions/ Back Value/ NSTP exception.

![image2023-9-25_15-15-38.png](attachments/image2023-9-25_15-15-38.png)

**EXPAND_END**

Hard Block Swap Agent

**EXPAND: Hard Block Swap Agent**

### Block single cashflow after ‘Settle as Gross' and resultant cashflow which  one of the component cashflow is SWAP AGENT+Coupon or SWAP AGENT+Interim MTM

**EXPAND_END**

### Amendment / Cancellation

For scenarios where amendment happens after payment is released, user to ensure there is no duplicate payment.

1. Amendment before Payment Release - System will automatically replace the latest cashflow details
2. Cancel before Payment Release - System will automatically move the cashflow to cancelled status
3. Amendment / Cancel on Cashflow which was netted, but before net resultant cashflow is released - system will automatically cancel the net resultant cashflow and update the amended details
4. Cancel on Cashflow which was netted, but before net resultant cashflow is released - system will automatically cancel the net resultant cashflow and update the amended details
5. Amendment after Payment Release - System will generate a withdrawal (reversal will be shown on blotter and exception) and a new cashflow (rebook will be shown on blotter and exception).
6. Cancel after Payment Release - System will generate a withdrawal (reversal will be shown on blotter and exception), which must be released to cancel the original payment.
7. Amendment on Cashflow which was netted, but after net resultant cashflow is released - system will automatically generate a withdrawal and new for the underlying cashflow that was amended. We need to send additional payment or ask client to repay us the excess based on the scenario. Cancellation for the underlying cashflow should not be released as original payment would have been released for Net amount. Users to determine whether to net the reversal and new (or) initiate recall first.
8. Cancel on Cashflow which was netted, but after net resultant cashflow is released - system will automatically cancel the net resultant cashflow and update the amended details- system will automatically generate a withdrawal of the underlying cashflow that was cancelled. We need to send additional payment or ask client to repay us the excess based on the scenario. Cancellation for the underlying cashflow should not be released as original payment would have been released for Net amount.

In the Cashflow Blotter last column 'Event Reason' the indicator of whether it is a 'Reversal' or 'Rebook' will be shown.

This is an important field to monitor to ensure there is no duplicate payment

![Reverse Rebook.JPG](attachments/Reverse Rebook.JPG)

If a cashflow has either 'reversal' or 'rebook' and then it was netted, the net resultant cashflow will contain "reversal_rebook" exception

![image-2025-5-8_10-26-26.png](attachments/image-2025-5-8_10-26-26.png)

### Exception Layout

**EXPAND: Vostro Information is fixed section on the left side**

| SSI Result | Exception Status | Role | Vostro Section Title | Vostro Section Form |
| --- | --- | --- | --- | --- |
| System good stamping | | Maker/Checker | Vostro SI Information | Readonly |
| Missing Vostro | Pending Operator | Maker | Missing Vostro Exception | Editable |
| Pending Verification | Maker | Missing Vostro Exception | Readonly |
| Checker | Missing Vostro Exception | Editable |
| Multi Vostro | Pending Operator | Maker | Multi Vostro Exception | Editable |
| Pending Verification | Maker | Multi Vostro Exception | Readonly |
| Checker | Multi Vostro Exception | Editable |
| Vostro & Nostro Mismatch | Pending Operator | Maker | Vostro & Nostro Mismatch | Editable |
| Pending Verification | Maker | Vostro & Nostro Mismatch | Readonly |
| Checker | Vostro & Nostro Mismatch | Editable |
| Maker Adhoc SSI | Pending Verification | Maker | Adhoc SI Exception | Readonly |
| Checker | Adhoc SI Exception | Editable |
| Checker Reject Adhoc SSI | Pending Operator | Maker | Adhoc SI Exception | Editable |

**EXPAND_END**

**EXPAND: Nostro Information is fixed section on top of right side**

| SSI Result | Excetpion Status | Role | Nostro Section Title | Nostro Section Form |
| --- | --- | --- | --- | --- |
| System good stamping | | Maker/Checker | Nostro SI Information | Readonly |
| Missing Nostro | Pending Operator | Maker | Missing Nostro Exception | Editable |
| Pending Verification | Maker | Missing Nostro Exception | Readonly |
| Checker | Missing Nostro Exception | Editable |

**EXPAND_END**

**EXPAND: Affirmation exception is fixed section below the Nostro information**

| Exception Result | Exception Status | Role | Affirmation Section | Mandatory For Submit |
| --- | --- | --- | --- | --- |
| No Excetpion | | | Readonly with blank | N |
| Pending Affirmation' | Pending Operator | Maker | Editable | Y |

**EXPAND_END**

**EXPAND: Back value exception will be displayed when this exception generated**

| Exception Result | Exception Status | Role | Back Value Section | Mandatory For Submit |
| --- | --- | --- | --- | --- |
| Back Value | Pending Operator | Maker | Editable | Y |
| Pending Verification | Maker | Readonly | NA |
| Checker | Editable | Y |

**EXPAND_END**

- Comment section is fixed section as free text area.
- Maker/Checker's action button are displayed on bottom of exception page.

### Bulk Processing for cashflow

- Details can be found in <u>[Bulk Process for Multi Exceptions - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/Bulk+Process+for+Multi+Exceptions)</u>
- Bulk processing is available on right click of batch cashflow, which have same counterparty/booking entity/value date.
- Bulk Approve/Submit will only appear when cashflow sub state are all in Pending Operator/Pending Verification.

![image2024-6-26_9-47-45.png](attachments/image2024-6-26_9-47-45.png)

- In the bulk process window, cashflow will be separated as eligible for bulk processing or not eligible, based on whether is there non-eligible exception in the cashflow.

![image2024-6-26_9-54-10.png](attachments/image2024-6-26_9-54-10.png)

### Multi Exception Query

- When user try to get cashflow exceptions in cashflow blotter, field NSTP Exception can be used.

![image2024-10-8_15-5-22.png](attachments/image2024-10-8_15-5-22.png)

- When user try to search cashflow by exceptions, NSTP Exception in horizontal search will select all cashflows which contains the exception value.

![image2024-10-8_15-9-22.png](attachments/image2024-10-8_15-9-22.png)

- Exceptions which were processed by maker/checker can be found in cashflow history.

![image2024-10-8_15-12-38.png](attachments/image2024-10-8_15-12-38.png)

## * TPP (Third Party Payment)*

*On the SI input screen, there is a TPP checkbox. If an TPP SSI is flown from SSI+, the checkbox will automatically be ticked.*

*If SI is being manually input, it must be ticked by the settlement user.*

*TPP Cashflow information is sent to FMMIS and consolidated into a TPP report across systems for payment pattern analysis done by FCSO team (Financial Crime Surveillance)*

- **FM Third-party Payments Volume - MI **(Table/file :- tpp_history_s)** :-** [https://tableau-fmglobal.global.standardchartered.com/#/site/FMMIS/views/FMThird-partyPaymentsVolume-MI/FMThird-partyPaymentsVolume-MI?:iid=2](https://tableau-fmglobal.global.standardchartered.com/#/site/FMMIS/views/FMThird-partyPaymentsVolume-MI/FMThird-partyPaymentsVolume-MI?:iid=2)
- **FM Third-party Payment AML Pattern Analysis Monthly Report **(Table/file :- fcc_reporting_history)** ** :- [https://tableau-fmglobal.global.standardchartered.com/#/site/FMMIS/views/FMThird-partyPaymentAMLPatternAnalysisMonthlyReport/FMThird-partyPaymentAMLPatternAnalysisMonthlyReport?:iid=2](https://tableau-fmglobal.global.standardchartered.com/#/site/FMMIS/views/FMThird-partyPaymentAMLPatternAnalysisMonthlyReport/FMThird-partyPaymentAMLPatternAnalysisMonthlyReport?:iid=2)

*![image-2025-5-8_10-47-27.png](attachments/image-2025-5-8_10-47-27.png)*

## *Grouping Blotter*

Grouping Blotter is showing the payments consumed from upstream like Murex and Stella. Mainly it is guaranteeing the payment to be processed in sequence and determine the non-eco amendment processing.

Payments will only be moved to settlement queue (Cashflow Blotter) when the full set of payment under same trade events arrived.

PENDING status will be shown if there are payment not arrived in same batch, normally it is temporary status and will be auto completed soon. On edge case that some payments not arrive, OPS need to manual STP by confirming with Murex on the payment will never arrive:

![image2024-11-27_11-33-37.png](attachments/image2024-11-27_11-33-37.png)

### * User Manual Deliver*

*OPS is able to manually force deliver cashflow from group blotter directly, once any cashflow has been manual STPed, all other cashflows that from the same group will have to be manual STPed as well*

*![image-2026-4-29_11-28-7.png](attachments/image-2026-4-29_11-28-7.png)*

### *Payment cancelled before publish from Murex*

*Below is a sample happened on production, 104727547 need to be manual STP as the other 2 payments won't be published from Murex since they have been cancelled before publishing. *

**Problem Statement: **

102830762,102830763, 104727547 value on 7-May, Ratan expect to receive all of them, but didn’t receive 102830762,102830763. There is No missing or duplicate settlement issue, but make ops confused and additional manual intervention is required on investigation.

**Root Cause:**

104727547 was generated on 28-Apr, which VD is in future 9 calendar days, so it was real-time published to RATAN,

102830762,102830763 were generated on 03-Mar, by when the VD more than 9 calendar days , so it was not real-time published but wait for batch job publish it on 28-Apr, however these payments was cancelled  before 28-Apr, so these payment didn’t publish to Ratan.

![image2024-6-11_9-7-5.png](attachments/image2024-6-11_9-7-5.png)

* For bulk manual stp, please refer below page.*

*[Group Blotter Enhancement - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Group+Blotter+Enhancement) *

### *Pending Trade Validation Case*

*Details please see below page, including for more Group Pending cases*

[Grouping Blotter Monitoring - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/Grouping+Blotter+Monitoring)

## *Hold/Unhold/Send to WAITING Cashflow*

When the cashflow does not reach cashflow "cutoff day" yet and in any status (excludes RELEASED, NET or SPLIT) , user can have the option to put the cashflow on hold due to any reason (e.g. user finds some issue or wants to supplement the cashflow/trade info later)

### Maker to Hold a cashflow:

1. First user as a action Maker, go the "Cashflow Blotter", find the target cashflow which Cashflow is in any status (excludes RELEASED, NET or SPLIT)

2. Right click the cashflow, select and click 'Hold' from the action list.  Input Hold comment, click "Submit" button.

![image2023-9-25_16-26-13.png](attachments/image2023-9-25_16-26-13.png)

![image2023-9-25_16-47-58.png](attachments/image2023-9-25_16-47-58.png)

3.1 After Hold action summited successfully by maker, the cashflow will be updated to Cashflow State "HOLD", Cashflow Sub State "Pending Verification" and Cashflow Sub State Type "NA"

![image2023-9-25_16-28-8.png](attachments/image2023-9-25_16-28-8.png)

![image2023-9-25_16-29-26.png](attachments/image2023-9-25_16-29-26.png)

3.2 When Cashflow State is in "HOLD", user has limited manual actions allowed on Ratan.

Before Hold:

![image2023-9-25_16-49-30.png](attachments/image2023-9-25_16-49-30.png)

After Hold: When cashflow is in 'HOLD' status, Unhold and Send to waiting action is allowed

![image-2025-10-16_11-5-44.png](attachments/image-2025-10-16_11-5-44.png)

Note: To bulk hold, please tick all targeted cashflows first, then right click one of these cashflows, select and click 'Hold' from the action list.

![image2023-9-26_10-55-50.png](attachments/image2023-9-26_10-55-50.png)

### Checker to Unhold a cashflow:

Only Checker is allowed to do Unhold action. Same user who put a cashflow on Hold cannot perform Unhold  (Same user id can't do the hold & unhold on the same cashflow)

1. The second user as a Checker, go the "Cashflow Blotter", find the above HOLD cashflow which  is in any Cashflow State "HOLD"

2. Right click the cashflow, select and click 'Unhold' from the action list. Input Unhold comment, click "Submit" button.

![image2023-9-25_16-31-30.png](attachments/image2023-9-25_16-31-30.png)

![image-2025-10-16_11-9-13.png](attachments/image-2025-10-16_11-9-13.png)

3.1 After 'Unhold' action successfully submitted, the Cashflow State, Cashflow Sub State and Cashflow Sub State Type will revert to previous status before 'Hold"

![image2023-9-25_16-39-34.png](attachments/image2023-9-25_16-39-34.png)

3.2 After ‘Unhold’ successfully and cashflow status reverts back to previous status before 'Hold", user can continue to process from this 'previous' status again.

![image2023-9-25_16-43-30.png](attachments/image2023-9-25_16-43-30.png)

Note: To bulk uhold multiple cashflows, please tick all targeted cashflows first, then right click one of these cashflows, select and click 'Unhold' from the action list.

![image-2025-10-16_11-9-59.png](attachments/image-2025-10-16_11-9-59.png)

### Send to WAITING

After cashflow moved to HOLD status, user can select "Send to WAITING" action from right-click menu

![image-2025-10-16_11-35-17.png](attachments/image-2025-10-16_11-35-17.png)

after send to waiting submitted, cashflow will be moved to WAITING status with "Reinstate" exception.

## *Auto / Manually Net/Un-Net Cashflow*

*Cashflows can be netted automatically by the system or manually by user based on the scenario*

| **Scenarios** | **Operator** | **Affirm during netting** | **Pending Affirmation Exception** |
| --- | --- | --- | --- |
| Bilateral Netting | Manually done by user | User manually key in affirmation info when submit netting | No |
| CCIL Netting | Manually done by user | User manually key in affirmation info when submit netting | No |
| Ben BIC Netting | Manually done by user | NA | Yes |
| NDS Auto Netting | Auto done by system | NA | Yes |
| IRS Fix leg & Floating Leg merge( same trade id, vd) | Auto done by system | NA | Yes |
| Auto Netting | Auto done by system | Affirm by system | No |

### *Adhoc/Manually Net Cashflow

**ANCHOR: Adhoc Netting**
*

In Ratan, user can net the trades if their Currency (CCY), Counterparty, Booking Entity (FMID / FMCODE), Payment Date are the same.

1. Login to Ratan. Go to Cashflow Blotter, find and select the targeted 2 or more cashflows which are in Queued/Projected/Waiting status and with same Currency (CCY), Counterparty, Booking Entity (FMID / FMCODE), and Payment Date. Right click on one of these cashflows, click "Net Selected Cashflow" from the action list.

* **Note**: if cashflow is in 'READY' status,

- cashflow sub state type is "NA", user can do net or un-net.
- cashflow sub state type is "Pending ACK", user can't do the net or un-net.
- less than 10 mins before release cut off, user cannot perform net in READY status. Ops users can move the cashflow back to WAITING by using *Hold > Send to WAITING* action, allowing netting to continue

![image2023-9-26_15-10-43.png](attachments/image2023-9-26_15-10-43.png)

2. Have a double check on the cashflow netting preview for the netting result cashflow and the 2 or more netting component cashflows key information. If no further concern, click "Net All Cashflow With Affirmation", input your name and contact info, then click "Submit".

![image2023-9-26_15-44-58.png](attachments/image2023-9-26_15-44-58.png)

![image2023-9-26_15-48-29.png](attachments/image2023-9-26_15-48-29.png)

3.1 After "Net All Cashflow With Affirmation" submitted successfully, on the Cashflow Netting Preview window, you can see for the netting result cashflow which is the Result of netted the cashflows, a new cashflow ID will be generated and in cashflow status "QUEUED"; and the status of the component cashflow will be moved to "NETTED".

![image2023-9-26_15-58-20.png](attachments/image2023-9-26_15-58-20.png)

3.2 "Adhoc_Netting" will be showed under the Multi Exception list

![image2023-9-26_16-32-2.png](attachments/image2023-9-26_16-32-2.png)

And you can click "Display Component Cashflow" to check the netted component cashflows which resulted this cashflow after netting.

![image2023-9-26_16-43-0.png](attachments/image2023-9-26_16-43-0.png)

### *Unnet Cashflow*

User can manually unnet a netted resultant cashflow.

1. Login Ratan, go to New Tile → Cashflow Blotter. Find the targeted netted result cashflow which is in Queued/Projected/Waiting status, right click on this cashflow and click on "Un-Net Cashflow" from the action list.

* Note: For 'READY' status, if the cashflow is in 'READY' status and release (from Ratan to Razor) cutoff time is not approaching yet, then user can do net or un-net. If cashflow in 'READY' but sub status == Pending ACK, then user can't do the net or un-net.

![image2023-9-27_15-36-41.png](attachments/image2023-9-27_15-36-41.png)

2. Preview the component cashflows after unnet. If no concern, click "Un-Net All Cashflow" button to complete the unnet action.

![image2023-9-27_15-42-37.png](attachments/image2023-9-27_15-42-37.png)

3. Once "Un-Net All Cashflow" successfully, the netting result cashflow's state will move to DEAD.

![image2023-9-27_15-45-52.png](attachments/image2023-9-27_15-45-52.png)

![image2023-9-27_15-46-55.png](attachments/image2023-9-27_15-46-55.png)

And the netting component cashflows' state will move to QUEUED → WAITING.

![image2023-9-27_16-3-15.png](attachments/image2023-9-27_16-3-15.png)

![image2023-9-27_16-4-36.png](attachments/image2023-9-27_16-4-36.png)

* Note:

If any of the netted component cashflows get amended after netting, all the netted component cashflows would auto get unnetted and move to Gross, the netting result cashflow's state would move to DEAD. So the user would have to manually re-net these amended component cashflows accordingly by following above adhoc/manually net cashflow process if netting these cashflows is still desired.

### *Net Cashflows with Past Value Date*

User would be able to net the past value cashflows.

When the cashflows are in Failed status, having NSTP rule and the value date (payment date) is past already, user would have to Reinstate the cashflows first and then manually Net them if netting is requested.

1. Login to Ratan. Go to Cashflow Blotter, find and select 2 or more targeted cashflows which are all in FAILED status, having NSTP rules (by filter isSTP=No) and with same Currency (CCY), Counterparty, Booking Entity (FMID / FMCODE), and Payment Date (the date is already past). Right click on one of these cashflows, click "Reinstate" from the action list.

![image2023-9-28_10-27-47.png](attachments/image2023-9-28_10-27-47.png)

![image2023-9-28_9-51-30.png](attachments/image2023-9-28_9-51-30.png)

2. After Reinstate, the cashflows state will update from FAILED → QUEUED → WAITING

![image2023-9-28_10-29-47.png](attachments/image2023-9-28_10-29-47.png)

3. Select and tick these targeted cashflows again, Right click on one of these cashflows, click "Net Selected Cashflow" from the action list.

![image2023-9-28_10-33-40.png](attachments/image2023-9-28_10-33-40.png)

4. Have a double check on the cashflow netting preview for the netting result cashflow and the 2 or more netting component cashflows key information. If no further concern, click "Net All Cashflow With Affirmation", input your name and contact info, then click "Submit".

![image2023-9-28_10-36-8.png](attachments/image2023-9-28_10-36-8.png)

![image2023-9-28_10-37-33.png](attachments/image2023-9-28_10-37-33.png)

5. After "Net All Cashflow With Affirmation" submitted successfully, on the Cashflow Netting Preview window, you can see for the netting result cashflow which is the Result of netted the cashflows, a new cashflow ID will be generated and in cashflow status "QUEUED" → "WAITING"; and for the component cashflow, its state will be moved to "NETTED".

![image2023-9-28_10-38-16.png](attachments/image2023-9-28_10-38-16.png)

5.2 And in the cashflow detail page of the netting result cashflow, you can click "Display Component Cashflow" to check its netted component cashflows's info.

![image2023-9-28_10-43-43.png](attachments/image2023-9-28_10-43-43.png)

![image2023-9-28_10-44-9.png](attachments/image2023-9-28_10-44-9.png)

### *Settle As Gross **

**ANCHOR: Settle as Gross**
*

When the cashflow is in 'Pending Netting' or 'Pending Another Leg', users can have action option to "Settle as Gross" to manually settle this cashflow as Gross.

Important: This has a impact on Client limits, so we should move a cashflow from 'Pending Netting' or 'DVP' to 'Gross' only if there is an approval from TRM team specifically.

1. First user as a action Maker, Go the "Cashflow Blotter", find the target cashflow which Cashflow State is in "wanting" and Cashflow Sub State Type is in "pending another leg"

2. Right click the cashflow, select 'Settle as Gross' from the action list.

![image2023-9-21_14-56-16.png](attachments/image2023-9-21_14-56-16.png)

3. Then the cashflow is updated to Cashflow Sub State "Pending Verification" (make sure maker has completed to affirm all items under multi exception list which are pending operator), Sub State Type "Pending Exception" , Cashflow Affirmation Status "Affirmed", and then a new exception item "Settle as Gross" will appear under multi exception list.

![image2023-9-25_10-19-17.png](attachments/image2023-9-25_10-19-17.png)![image2023-9-25_10-14-13.png](attachments/image2023-9-25_10-14-13.png)

4.  Second user as a Checker, go to this cashflow detail page in cashflow blotter. Find the "Settle as Gross" in the multiple exception list. Click "Approve" button to approve this "Settle As Gross" action from maker.

![image2023-9-25_10-36-50.png](attachments/image2023-9-25_10-36-50.png)

![image2023-9-25_10-36-16.png](attachments/image2023-9-25_10-36-16.png)

5.1 After checker approves the action, the cashflow status will update to "Ready"

![image2023-9-25_10-39-22.png](attachments/image2023-9-25_10-39-22.png)

5.2 But if Checker rejects the action from the multi exception list, then the Cashflow Sub State will update to "Pending Operator" and the "Settle to Gross" will be changed to "Adhoc SSI" under multi exception list.

Checker will have to select the reason for rejection and comments is mandatory. If only SSI is incorrect, Checker should select SSI while rejecting.

![image2023-11-16_14-49-7.png](attachments/image2023-11-16_14-49-7.png)

![image2023-9-25_14-54-37.png](attachments/image2023-9-25_14-54-37.png)

![image2023-9-25_14-51-9.png](attachments/image2023-9-25_14-51-9.png)

### *CCIL Netting*

- Ratan identify the Guaranteed (booked with counterparty as Clearing Corporation of India - CCIL/MMB) & Non Guaranteed (booked with specific counterparties maintained in Ratan as a backend static). Cashflows will be stamped with settlement method == 'CCIL', based on below logic:

1. 1. Entity.Booking_Entity_SCI_FMID == '4' 2. Instrument_Common.Murex_Product_Family=='IRD' and Instrument_Common.Murex_Product_Group=='IRS' 3. Entity.Counterparty_SCI_FMID is 400021949 or the FMID from the non guaranteed CCIL client static data list 4. Cashflow.Payment_Currency is INO

- Guaranteed: If Cashflow sub State Type == 'Pending Netting' and Settlement Method == 'CCIL' and counterparty FMID =='400021949'
- Non-Guaranteed: If Settlement_Method == 'CCIL' and Cashflow.Cashflow_Sub_State_Type == 'Pending Netting' and counterparty FMID !='400021949'
- Net resultant from guaranteed and non-guaranteed cannot be netted together.
- Details can be found in <u>[CCIL Netting - Derivative Strategy Projects - Confluence (standardchartered.com](https://confluence.global.standardchartered.com/display/DSP/CCIL+Netting)</u>

### <u>Stella CCIL Netting</u>

Ratan identif the uber message from Stella. The whole process refer to:  [Stella CCIL Identify - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Stella+CCIL+Identify)

If

1. Entity.Booking_Entity_SCI_FMID == '4'
2. Instrument_Common.ISDA_Taxonomy== 'InterestRate:IRWap'
3. Entity.Counterparty_SCI_FMID and Entity.BookingEntiyFmId in static client list, the list are the same with Murex client list.
4. Cashflow.Payment_Currency is INO

### *NDS Fixing Netting*

- For Murex non-deliverable cashflow, it will be Auto Netted in RATAN based on NID, except for ND IRS.
- Ratan will query parent trade typology (trade in the same NID) from TDS3 once metalized.
- If cashflow satisfies NSTP rule, Typology in(NDS, NDS Fixing, NDCF, NDFRA, ND CDS Fixing, ND CDS and ND-Convert) and ND_Parent_typology != NDIRS and cashflow event not in (reversal, rebook), then cashflow will be in WAITING + Pending Exception status.
- **No manual touch on the NSTP rule** (Pending NDS Netting), which may impact the auto netting.
- Ratan will scan all cashflows every 30 mins, if it satisfies below condition, cashflow will be auto netted.

a. Cashflow value date is in [Today, Today+2 business day]

b. Same Booking Entity, Counterparty, same VD, CCY, NID

c. Status = WAITING + Pending Exception

d. Pending Exception contains 'Pending NDS Netting'

### *Beneficiary BIC Netting*

- For Murex payment, if it satisfies Beneficiary BIC static, it will be marked as Beneficiary BIC flag =Y and in WAITING + Pending Netting status.
- ![image2024-11-25_13-53-59.png](attachments/image2024-11-25_13-53-59.png)
- ![image2024-11-27_10-13-26.png](attachments/image2024-11-27_10-13-26.png)
- Control build to reduce operation risk, as it only allow cashflow on Same BIC_Net Flag (Y) + Same Beneficiary BIC + Same Value Date + Same Entity, can be performed as BIC Netting.
- For Ben BIC netting eligible cashflow, operation team can manually Settle As Gross if necessary.
- If any amendment or withdrawal on Ben BIC component cashflow, netting resultant cashflow will be auto un-netted if it's not released yet.
- There are segregation between Ben BIC Netting and CCIL Netting/Bilateral Netting
- Affirmation details need to be filled in when validating netting resultant cashflow.
- If any static update, it will take effect immediately. For already materialized cashflow, updated static can take effect after fail and reinstate.

### *Auto Netting*

#### * Auto Netting Static*

![image-2025-7-31_20-32-53.png](attachments/image-2025-7-31_20-32-53.png)

- *FMO Ops can request Data Ops team to create auto netting rule or switch existing manual netting rule to auto netting rule with below properties added:* - **Netting Date Time**: define the time when system start to perform netting - **STP Level**: define the STP level for netting resultant cashflow - NSTP_MAKER_CHECKER - NSTP_CHECKER_ONLY - **Netting Type: **different netting type will have different result, please make sure this is set correctly

![image-2025-7-31_21-1-45.png](attachments/image-2025-7-31_21-1-45.png)

- Auto netting rule creation/update/disable will trigger cashflow refresh - if data ops **create new auto netting rule,** system will check all cashflow in below status and filter a list of cashflow need to be refreshed - **Refresh **Netting id ='' or Netting id is null** **and Cashflow_Status = WAITING (Pending Netting, Pending Exception) or Cashflow_Status = READY (cashflow state type is null) and meet the rule condition - **NOT** refresh cashflow in WAITING (Pending Another leg, Pending Auto netting) READY (Pending Ack), HOLD, SUPPRESSED, NETTED, RELEASED, SETTLED - if data ops **disable existing auto netting rule, **system will refresh below cashflow - **Refresh** Cashflow_Status = WAITING (Pending Auto Netting) and tagged to the disabled rule - **NOT** refresh cashflow in WAITING (Pending Another leg, Pending Netting, Pending Exception), READY, HOLD, SUPPRESSED, NETTED, RELEASED, SETTLED - if data ops **update existing rule**, - Update existing auto netting rule without rule type change - **Refresh **Cashflow_Status = WAITING (Pending Auto Netting) and tagged to the updated rule - **Refresh **Netting id ='' or Netting id is null** **and Cashflow_Status = WAITING (Pending Netting, Pending Exception) or Cashflow_Status = READY (cashflow state type is null) and meet the rule condition - **NOT** refresh cashflow in WAITING (Pending Another leg, Pending Auto netting) READY (Pending Ack), HOLD, SUPPRESSED, NETTED, RELEASED, SETTLED - Update manual netting rule to auto netting rule - **Refresh **Netting id ='' or Netting id is null** **and Cashflow_Status = WAITING (Pending Netting, Pending Exception) or Cashflow_Status = READY (cashflow state type is null) and meet the rule condition - **NOT** refresh cashflow in WAITING (Pending Another leg, Pending Auto netting) READY (Pending Ack), HOLD, SUPPRESSED, NETTED, RELEASED, SETTLED - Update auto netting rule to manual netting rule - **Refresh** Cashflow_Status = WAITING (Pending Auto Netting) and tagged to the rule - **NOT** refresh cashflow in WAITING (Pending Another leg, Pending Netting, Pending Exception), READY, HOLD, SUPPRESSED, NETTED, RELEASED, SETTLED

#### Auto Netting Process

- If cashflow hit the rule defined in the auto netting static, it will be hold in "Pending Auto Netting" status
- There will be scheduled job runs every 30 minutes to check if the pending auto netting cashflow past or equal to the configured netting date time. - if yes, system net the cashflow with defined netting type, the netting resultant cashflow is affirmed by system - if no, keep the cashflow in pending auto netting to wait for next job
- Netting resultant cashflow will be auto affirmed by system and there will <u>**not **</u>be "pending affirmation" exception
- Netting resultant will be hold in NSTP with "Auto Netting" exception requires approval level defined in the netting static (maker_checker, checker_only or full_stp)
- if one cashflow hit multiple rules , system will tag the rule with highest priority netting type and latest created rule to the cashflow. - Netting type priority: SAL MTM Netting > SAL Coupon Netting >Clearing_Swift_Suppress > CCIL Netting > BIC Netting >Bilateral Netting - For example: - if cashflow hit SAL MTM netting rule and another Bilateral Netting rule, system will tag SAL MTM netting rule to the cashflow - if cashflow hit 2 bilateral netting rule, system will tag the latest created rule to the cashflow
- if the netting resultant is not expected, user can manually unnet the cashflow, the component cashflow will be in pending auto netting status and being netted by system when scheduled job triggers
- if user found anything wrong with the netting static, please update the rule before un-net the netting resultant cashflow.

### *Inter entity Netting*

- Scope - ![image-2026-6-8_10-38-30.png](attachments/image-2026-6-8_10-38-30.png) - Inter entity netting to be done on gross cashflow for SCB inter entities (including IRS aggregation resultant) - initial scope: cashflows between SCB CHO and SCB HK - Currency: USD for day1. Additional currencies can be added later. (CIS involvement required if PM ccy is needed). - *Amount <=USD 100K * - *Cashflow event is NEW* - *Cashflow with Rebook, Reversal, Reversal_Rebook event reason is excluded.* - *LOANIQ cashflow is excluded.*
- *Cashflow match the netting rule condition will be moved to "pending auto netting" status, system will perform below match validation when configured netting date time reached.* - CCY, VD. amount should be the same between C1 C2 - Direction of C1 C2 should be opposite - C1 booking entity fmid = C2 counterparty mapped value - C2 booking entity fmid = C1 counterparty mapped value - by default, mapped value will be the the FMID - if there is any special value instead of FMID to be used for any counterparty, need to add the record to backend static (release required), sample as below - ![image-2026-6-4_11-44-37.png](attachments/image-2026-6-4_11-44-37.png)
- if cashflow find matched pair, both cashflow will be eligible for auto netting, system will net them with affirmation. - the ones not matched will be sent as gross without affirmation - the ones matched but there is no other cashflow to net with, will also be sent as gross without affirmation
- new netting type "Inter Entity Netting" need to be selected in the auto netting rule. below backend configuration is linked to the type: - netting key will be： booking entity FMID + VD + Currency + Counterparty mapped value - netting resultant counterparty fmid/bic code will randomly derive from one component cashflow - netting resultant payment type = 'Inter Entity Netting'
- Amendment/Withdrawal happened after netting resultant generated - if both side netting resultant not released from Ratan, system will trigger auto unnet once withdrawal received - if one side netting resultant released from Ratan, system will **not **trigger auto unnet for both side - Withdrawal/new event for the released side will have reversal/rebook exception - Withdrawal/new event for the not released side will not have reversal/rebook exception - User need to release the other side netting resultant since one side have been released - if both side netting resultant released from Ratan, system will not trigger auto unnet for both side
- Manual unnet after netting resultant generated - if manual unnet required, ops should manual unnet netting resultant from both side, component cashflow will be moved back to pending auto netting status and matched cashflow will be netted in 30 minutes - if ops manual unnet only one side, component cashflow will be moved back to pending auto netting, and will be send as gross because of no matched cashflow from other side.

more details can be checked in [Inter Entity Netting - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Inter+Entity+Netting) and [Ratan Inter-Entity Netting - Formalisation & Process Governance FMO - Confluence](https://confluence.global.standardchartered.com/display/FPGWIP/Ratan+Inter-Entity+Netting)

## *Cashflow Suppression*

There are 2 ways to suppress the cashflows In Ratan: Auto cashflow suppression and manual cashflow suppression.

*Auto Cashflow Suppression
**ANCHOR: Suppression**
*

The Suppression rules blotter is where the user can predefine and create the rule for auto suppression of cashflow.

RATAN will not send suppressed cashflows to RAZOR, so no payment or settlement accounting entries will be generated. So this table should be used only for scenarios where no payment or accounting is expected.

In Ratan, this requires a 4 eye checking to approve the suppression, Suppression can be done for individual cashflows or can be made for a particular group.

1. Maker to go to Suppression Rules blotter, the user should click on New Tile -> Suppression Rules [Cashflow]. where you can view the suppression rules which are already created and also can create new rules which will need a 4 eye check and approval

![image2023-10-6_10-52-38.png](attachments/image2023-10-6_10-52-38.png)

2. To add a new rule for cashflow suppression, click "Add Rule" button.

![image2023-10-6_10-54-29.png](attachments/image2023-10-6_10-54-29.png)

3. Input below required rule information then click "Add" button to submit.

- Please Choose Rules Item: There are multiple criteria's from which the user will be able to suppress a cashflow. e.g. if the user wants to suppress all the cashflows for an internal counterparty(DDINT), the user can click on Please Choose Rules Item -> Counterparty and input the Counterparty FMID.
- Reason: free text box for you to input the suppression remarks or reasons.

![image2023-10-6_11-21-43.png](attachments/image2023-10-6_11-21-43.png)

4. Click on Yes to continue. Then the rule will go for validation like a 4 eye check, so you will see the next 'Action' needed is to "Verify" this rule.

![image2023-10-5_14-14-10.png](attachments/image2023-10-5_14-14-10.png)

![image2023-10-6_10-41-16.png](attachments/image2023-10-6_10-41-16.png)

5. Another User as checker who has the rule validation access (not the same user who has created) can logon Ratan and go to New Tile -> Suppression Rules [Cashflow], sort rules according to the Date, find this NSTP rule created just now. Click "Verify" button.

![image2023-10-6_10-55-33.png](attachments/image2023-10-6_10-55-33.png)

6. If this Validator is satisfied with the Suppression rule, Click "Create Rule" button. If this not satisfied with the Suppression rule, Click "Delete Rule" button.

![image2023-10-6_11-0-18.png](attachments/image2023-10-6_11-0-18.png)

7. After this suppression rule is verified, the "Verify" button will disappear and a bin icon will appear under Action.

So once any cashflow is unaffirmed and hits this cashflow suppression rule, it will be suppressed automatically by the system.

![image2023-10-6_11-2-8.png](attachments/image2023-10-6_11-2-8.png)

*Manual Cashflow Suppression*

In Ratan, user can manually suppress the cashflows directly from the cashflow blotter.

RATAN will not send suppressed cashflows to RAZOR, so no payment or settlement accounting entries will be generated. It is not advisable to manually suppress cashflows for this reason, unless no payment settlement and no accounting are required.

1. Maker can go to New Tile -> Cashflow Blotter,

![image2023-10-6_11-31-6.png](attachments/image2023-10-6_11-31-6.png)

2. Select one or multiple cashflow(s) which are in PROJECTED/QUEUED/READY(only when Sub State Type is "NA")/WAITING state, right click on the cashflow, select and click "Suppress Cashflow".

![image2023-10-6_16-11-52.png](attachments/image2023-10-6_16-11-52.png)

3. Once the system prompts below window, input the cashflow suppression comment and click Submit to finish.

![image2023-10-6_15-40-11.png](attachments/image2023-10-6_15-40-11.png)

4. After Maker submit the cashflow suppression, the Cashflow Sub State will update to "Pending Verification" and Cashflow Sub State Type to be "Cashflow Suppression".

![image2023-10-6_17-19-34.png](attachments/image2023-10-6_17-19-34.png)

5. And then this Cashflow goes for a 4 eye check. Another user as checker who has suppression approval permission needs to login Ratan and goes to Cashflow Blotter, find this cashflow, select and click "Confirm Suppression".

![image2023-10-6_17-20-35.png](attachments/image2023-10-6_17-20-35.png)

6. Input your comment and then click "Approve"/Reject" to finish

![image2023-10-6_17-21-25.png](attachments/image2023-10-6_17-21-25.png)

5. Once the suppression is approved, then the Cashflow State will update from "Waiting" to "Cashflow_Suppressed" and Cashflow Sub State &Type to be "NA".

![image2023-10-6_17-22-22.png](attachments/image2023-10-6_17-22-22.png)

![image2023-10-6_17-33-25.png](attachments/image2023-10-6_17-33-25.png)

*Manual Cashflow Un-suppression*

In Ratan, the user will be able to un-suppress the cashflows which are already suppressed, in case the previous suppression was done in error.

1. First user as a Maker, Go to Cashflow Blotter, Search for the suppressed cashflow which cashflow state is "CASHFLOW_SUPPRESSED", Right click on this cashflow, select and click the "Un-Suppress Cashflow" from the available action option list.

![image2023-10-9_14-6-41.png](attachments/image2023-10-9_14-6-41.png)

2. Input comment for un-suppression, click on Submit to confirm the un-suppression.

![image2023-10-9_14-10-34.png](attachments/image2023-10-9_14-10-34.png)

3. Once Maker submits the un-suppression, the Cashflow State will change to "WAITING", Cashflow Sub Sate change to "Pending Verification", Cashflow Sub State Type to "Undo Cashflow Suppression" and Cashflow Affirmation to "Unaffirmed".

![image2023-10-9_14-12-52.png](attachments/image2023-10-9_14-12-52.png)

![image2023-10-9_14-17-46.png](attachments/image2023-10-9_14-17-46.png)

4. Another user as Checker go to Cashflow Blotter, Search for this trying-to-un-suppressed cashflow which Cashflow Sub State is "Pending Verification" and Cashflow Sub State Type is "Undo Cashflow Suppression". Right click on this cashflow, select and click the "Confirm Un-Suppression" from the available action option list.

![image2023-10-9_14-21-37.png](attachments/image2023-10-9_14-21-37.png)

5. Input the comment for un-suppression and Click "Approve" button to complete.

![image2023-10-9_14-25-12.png](attachments/image2023-10-9_14-25-12.png)

6. Once Checker approves the cashflow un-suppression successfully, the Cashflow State will change to from "WAITING" (Cashflow Sub State "Pending Verification" and Cashflow Sub State Type "Undo Cashflow Suppression") to "QUEUED" and then to "WAITING" (Sub State "Pending Operator" and Cashflow Sub State Type "Pending Exception").

![image2023-10-9_14-26-16.png](attachments/image2023-10-9_14-26-16.png)

![image2023-10-9_14-29-59.png](attachments/image2023-10-9_14-29-59.png)

## *Swift Suppression*

For EG / NP / SA / LOANIQ where RAZOR is downstream, RATAN will send not swift suppressed cashflows to RAZOR, no payment and no settlement accounting entries will be generated. So this table is not expected to be used

If payment is to be suppressed, but accounting to be generated, settle the payment to Nostro with 'SUPPRESSXXX' or 'REJECTXXALL' BIC.

For other markets where RATAN is directly generating Accounting, SWIFT Suppression will generate accounting entries as per the Nostro static.

There are 2 ways to suppress the cashflows In Ratan: Auto cashflow suppression and manual cashflow suppression.

*Auto Swift Suppression
**ANCHOR: Swift Suppression**
*

The Suppression rules blotter is where the user can predefine and create the rule for auto swift suppression.

In Ratan, this requires a 4 eye checking to approve the suppression, Suppression can be done for individual cashflows or can be made for a particular group.

1. Maker to go to Suppression Rules blotter, the user should click on New Tile -> Suppression Rules [Swift]. where you can view the suppression rules which are already created and also can create new rules which will need a 4 eye check and approval

![image2023-10-6_11-14-6.png](attachments/image2023-10-6_11-14-6.png)

2. To add a new rule for swift suppression, click "Add Rule" button.

![image2023-10-6_10-54-29.png](attachments/image2023-10-6_10-54-29.png)

3. Input below required rule information then click "Add" button to submit.

- Please Choose Rules Item: There are multiple criteria's from which the user will be able to suppress a cashflow. e.g. if the user wants to suppress all the cashflows which ever is Unaffirmed, the user can click on Please Choose Rules Item -> Cashflow - > Cashflow affirmation status
- Reason: free text box for you to input the suppression marks or reasons.

![image2023-10-6_11-19-43.png](attachments/image2023-10-6_11-19-43.png)

4. Click on Yes to continue. Then the rule will go for validation like a 4 eye check, so you will see the next 'Action' needed is to "Verify" this rule.

![image2023-10-5_14-14-10.png](attachments/image2023-10-5_14-14-10.png)

![image2023-10-6_11-21-3.png](attachments/image2023-10-6_11-21-3.png)

5. Another User as checker who has the rule validation access (not the same user who has created) can logon Ratan and go to New Tile -> Suppression Rules [Cashflow], sort rules according to the Date, find this NSTP rule created just now. Click "Verify" button.

![image2023-10-6_11-23-50.png](attachments/image2023-10-6_11-23-50.png)

6. If this Validator is satisfied with the Suppression rule, Click "Create Rule" button. If this not satisfied with the Suppression rule, Click "Delete Rule" button.

![image2023-10-6_11-24-57.png](attachments/image2023-10-6_11-24-57.png)

7. After this suppression rule is verified, the "Verify" button will disappear and a bin icon will appear under Action.

So once any cashflow is unaffirmed and hits this cashflow suppression rule, it will be suppressed automatically by the system.

![image2023-10-6_11-26-18.png](attachments/image2023-10-6_11-26-18.png)

*Manual Swift Suppression*

In Ratan, user can manually swift suppress the cashflows directly from the cashflow blotter.

RATAN will not send swift suppressed cashflows to RAZOR, no payment and no settlement accounting entries will be generated.

1. Maker can go to New Tile -> Cashflow Blotter.

![image2023-10-6_11-31-6.png](attachments/image2023-10-6_11-31-6.png)

2. Select one or multiple cashflow(s) which are in PROJECTED/QUEUED/READY(only when Sub State Type is "NA")/WAITING state, right click on the cashflow, select and click "Swift Suppression" from the available action list.

![image2023-10-9_15-57-3.png](attachments/image2023-10-9_15-57-3.png)

3. Once the system prompts below window, input the swift suppression comment and click Submit to finish.

![image2023-10-9_15-52-31.png](attachments/image2023-10-9_15-52-31.png)

4. After Maker submit the swift suppression, the Cashflow Sub State will update to "Pending Verification", Cashflow Sub State Type to be "Swift Suppression".

![image2023-10-9_15-58-50.png](attachments/image2023-10-9_15-58-50.png)

![image2023-10-9_15-59-46.png](attachments/image2023-10-9_15-59-46.png)

5. And then this Cashflow goes for a 4 eye check. Another user as checker who has suppression approval permission needs to login Ratan and goes to Cashflow Blotter, find and right click this cashflow, select and click "Verify Swift Suppression".

![image2023-10-9_17-38-50.png](attachments/image2023-10-9_17-38-50.png)

6. Input your comment and then click "Approve" or "Reject" button to finish

![image2023-10-9_17-39-52.png](attachments/image2023-10-9_17-39-52.png)

5. Once the suppression is approved, then the Cashflow State will update from "Waiting" to "SWIFT_SUPPRESSED" and Cashflow Sub State & Type to be "NA".

![image2023-10-9_17-41-22.png](attachments/image2023-10-9_17-41-22.png)

![image2023-10-9_17-43-55.png](attachments/image2023-10-9_17-43-55.png)

*Manual Undo Swift Suppression*

In Ratan, the user will be able to undo swift suppression for the cashflows which are already swift_suppressed, in case the previous suppression was done in error.

1. First user as a Maker, Go to Cashflow Blotter, Search for the swift_suppressed cashflow which cashflow state is "SWIFT_SUPPRESSED", Right click on this cashflow, select and click the "Undo Swift Suppression" from the available action option list.

![image2023-10-10_14-51-57.png](attachments/image2023-10-10_14-51-57.png)

2. Input comment for the undo swift suppression, click on Submit to confirm the un-suppression.

![image2023-10-10_14-52-40.png](attachments/image2023-10-10_14-52-40.png)

3. Once Maker submits the undo swift suppression, the Cashflow State will change to "WAITING", Cashflow Sub Sate change to "Pending Verification", Cashflow Sub State Type to "Undo Cashflow Suppression" and Cashflow Affirmation to "Unaffirmed".

![image2023-10-10_14-55-51.png](attachments/image2023-10-10_14-55-51.png)

![image2023-10-10_14-57-7.png](attachments/image2023-10-10_14-57-7.png)

4. Another user as Checker go to Cashflow Blotter, Search for this trying-to-undo-swift-suppression cashflow which Cashflow Sub State is "Pending Verification" and Cashflow Sub State Type is "Undo Swift Suppression". Right click on this cashflow, select and click the "Verify Undo Swift Suppression" from the available action option list.

![image2023-10-10_15-0-3.png](attachments/image2023-10-10_15-0-3.png)

5. Input the comment for the undo swift suppression and Click "Approve" button to complete.

![image2023-10-10_15-2-25.png](attachments/image2023-10-10_15-2-25.png)

6. Once Checker approves the undo swift suppression successfully, the Cashflow State will change to from "WAITING" (Cashflow Sub State "Pending Verification" and Cashflow Sub State Type "Undo Cashflow Suppression") to "QUEUED" and then to "WAITING" (Sub State "Pending Operator" and Cashflow Sub State Type "Pending Exception").

![image2023-10-10_15-3-5.png](attachments/image2023-10-10_15-3-5.png)

![image2023-10-10_15-4-10.png](attachments/image2023-10-10_15-4-10.png)

## *Lien Monitoring Murex vs RATAN*

Run Lien booked cashflow report via Murex. Steps to retrieve report attached below

1. In Payment > Query Payment Table

![image2024-7-1_13-18-46.png](attachments/image2024-7-1_13-18-46.png)

1. Select Query Payment Table > User Filter > Click Dropdown Button of Filter

![image2024-7-1_13-19-17.png](attachments/image2024-7-1_13-19-17.png)

1. Search FMRP and Enter followed by FMRP Lien

![image2024-7-1_13-20-42.png](attachments/image2024-7-1_13-20-42.png)

1. Once selected click Proceed

![image2024-7-1_13-21-4.png](attachments/image2024-7-1_13-21-4.png)

**Lien Exception in Ratan**

When LIEN is placed & Lien amount update on a trade, all of its cashflows (including interest) must be NSTP in RATAN with 'LIEN' exception (Maker +  Checker).

In the Murex trade booking model, there're market events to place Lien on the trade level and the Lien information is feeding to TDS3. RATAN is going to source the trade Lien information from TDS3 and use this drive the cashflow NSTP exception.

- '**LIEN on Trade**' exception would be system pre-defined maker/checker exception which ops(business rule and data ops profiles) can't update/remove.
- Exception for Gross Cashflow: RATAN need to lookup the Lien amount from latest event from parent trade(by original trade id), if there's Lien available from trade, then generate '**LIEN on Trade**' exception on cashflow

![image2024-11-27_13-53-14.png](attachments/image2024-11-27_13-53-14.png)

## *RFR and Swap Agent*

Murex Booking Model:

- Generally RFR and Swap Agent are 3 trades booked with same LtiID, to book notional on T day, interest on T+2 day CCS trade. - Trade 1 would have T+2 coupon and T+2 dummy notional - Trade 2 would have T notional - Trade 3 would have T+2 dummy notional to reversal trade 1 dummy notional
- So Trade 1 T+2 coupon and Trade 2 T notional will be sent to RATAN
- Strategy 'RECALC' / 'SWAP_AGENT' used to mark these 3 trades & underlying payments

RATAN Handling:

- Interim MTM & Coupon in Swap Agent can be netted together
- Netting resultant cashflow from Interim MTM & Coupon in Swap Agent would be SWIFT Suppressed in RATAN as it would be settled in clearing house, accounting will generate.
- Initial notional and final notional in Swap Agent would be bilateral settled.
- Notional/coupon/interim MTM from RFR would be bilateral settled in RATAN.

![image2024-11-27_14-36-57.png](attachments/image2024-11-27_14-36-57.png)

Details can be found in [RFR and Swap Agent - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/RFR+and+Swap+Agent)

## Split/Auto Distribution

Details referred to [Cashflow Splitting - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Cashflow+Splitting)

### Manual Split

- user can split the cashflow if cashflow is in - WAITING - READY (sub state type is "NA") and more than 10 mins before release cut off. - if cashflow is in READY and less than 10 mins before release cut off, ops users can move the cashflow back to WAITING by using *Hold > Send to WAITING* action, allowing splitting to continue

![image-2025-11-20_9-57-41.png](attachments/image-2025-11-20_9-57-41.png)

![image-2025-9-25_23-4-16.png](attachments/image-2025-9-25_23-4-16.png)

- User can lookup SSI for the split child if needed.
- User confirm the split action and input affirmation info, system will move parent cashflow to SPLIT status and child cashflow generated with S prefix.

![image-2025-11-20_10-2-32.png](attachments/image-2025-11-20_10-2-32.png)

![image-2025-9-25_23-7-40.png](attachments/image-2025-9-25_23-7-40.png)

### Un-Split

- if user found issue after the split, they can select the cashflow and perform un-split if cashflow are in eligible status (QUEUED,WAITING,FAILED, HOLD, READY(NA), CASHFLOW_SUPPRESSED) ![image-2025-9-25_23-9-47.png](attachments/image-2025-9-25_23-9-47.png)
- Un-Split Result 1. Parent cashflow moved to WAITING status with Un-Split exception 2. Child cashflow moved to DEAD status 3. Splitting Id removed from the cashflow ![image-2025-9-25_23-13-35.png](attachments/image-2025-9-25_23-13-35.png)

### Amend Split

- ometimes, ops have released some child cashflow but notice the amount is incorrect for the rest, user can amend the amount If at least 2 child cashflow are in WAITING status
- only the amount of WAITING cashflow can be updated
- user need to make sure the total amount of all child cashflow are equal to the original cashflow ![image-2025-9-25_23-20-25.png](attachments/image-2025-9-25_23-20-25.png) ![image-2025-9-25_23-21-22.png](attachments/image-2025-9-25_23-21-22.png)
- Split Amend Result 1. Parent cashflow will not be impacted, still in SPLIT status 2. child cashflow amount updated to the new value and hold in WAITING status with an extra "Split Amend" exception ![image-2025-9-25_23-27-14.png](attachments/image-2025-9-25_23-27-14.png)

### Withdrawal Event Handling

- If child cashflow have not been released from Ratan, withdrawal event will be moved to SPLIT status, child cashflow will be cancelled
- if any child cashflow have been released from Ratan, withdrawal event will be moved to SPLIT status, child cashflow not released will be directly cancelled, child cashflow released will with corresponding withdrawal event hold in NSTP pending user action

### Auto Distribution Process

Some nostro agent may have threshold for the cashflow amount can be processed. If any cashflow exceed the threshold, system will split the cashflow to lower amount at release cut off time and directly generate swift and accounting for each child to downstream.

1. Nostro Threshold Static 1. add a new blotter to manage related static, data ops have access to create/update/delete. Other users only have read only view. 2. currency is mandatory, booking entity, nostro agent bic are optional ![image-2025-9-26_9-46-9.png](attachments/image-2025-9-26_9-46-9.png)
2. if there is any exception happened in the auto split process, move cashflow to Cashflow State = QUEUED, Cashflow Sub Status Type = Pending Exception, user can check the comment from cashflow history - if the exception is caused by unexpected tech reasons, user can reinstate the cashflow to continue the process. - if the exception is caused by nostro threshold set up, user can request static ops to update the value and reinstate the cashflow to use the latest static set up to generate the child. ![image-2026-2-26_17-0-17.png](attachments/image-2026-2-26_17-0-17.png)

## FX Utilization

Reference Page: [FXU - RATAN analysis - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/FXU+-+RATAN+analysis)

For the FX deals which are booked in FM booking system(S2BX, BLADE) tend to make a payment to Transaction Banking Client(Trade Services, Cash Management, or Security Services) account by intervention of CMO/Trade/Securities OPS.

While for EG/NP/SA entity, FX deals will be processed in Ratan side, FXU (Razor) will query the trade/cashflow data from Ratan, then send the utilization request to Ratan.

### Utilization Workflow

For settlement method='UTIL', cashflow will be identified as utilization cashflow. For these cashflow:

- As there is early utilization request for EG/SA/NP, when cashflow comes it would be the directly materialized without waiting for VD-5.
- Util cashflow will skip rule check (including Cashflow_suppression, SWIFT_suppression, Netting, NSTP).
- Util cashflow will only perform Nostro stamping based on static data setup in Ratan for settlement means and settlement account. - If the client setup as auto util client, settlement means and account should be stamped as FXBRREC - If the client setup as manual util client, settlement means and account should be stamped as FXBRREC-M
- If no Nostro stamping exception, cashflow will directly go to READY status and ready for utilization request.
- Once utilization happens, accounting entry will be generated correspondingly.

### Utilization Status

RATAN would have 3 main cashflow status help FMO identify the utilization status

- UTILIZED**, **: Full amount is utilized and remaining amount is 0 - Manual Util: full utilization amount request from FXU - Auto Util: by auto util cutoff, all auto util cashflow will be auto utilized.
- PARTIALLY-UTILIZED: Partial amount is utilized and remaining amount is not 0 - Partial utilization: partial utilization request from FXU - Reversal: partial utilization can be reversed once got the reversal request from FXU
- PASTDUE: No utilization happen until VD EOD (auto) - For manual util, if no utilization request comes from FXU, then post auto util, status will be moved to pastdue.

For UTILIZED/PARTIALLY-UTILIZED cashflow, Ratan will write status back to Stella for hard blocking any further event for the trade.

Detailed status machine can refer to [Status Machine - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Status+Machine)

### Settlement Method Update

For Gross trades and Util trades, user can switch cashflow settlement method to each other.

The settlement method update has to be on trade level.

- When cashflow status in (PROJECTED, WAITING, READY, PASTDUE) and settlement method in ('', 'GROSS','UTIL') and FX product and data source system !=RATAN and event reason !='reversal', trade will be eligible for settlement method update. - If cashflow status is not in above list, user need to manually process cashflow to make it eligible for processing. - i.e. early materlize for PROJECTED cashflow, unsuppress for CASHFLOW_SUPPRESSED/SWIFT_SUPPRESSED cashflow.
- If user only selected 1 cashflow in cashflow blotter, system will automatically display all cashflows under the same trade.
- For trade contains ERROR cashflow, it would be not eligible for settlement method update request.
- Limitation for bulk update is 100 trade/cashflow.
- During settlement method update, backend code would check utilization static for eligible entity FMIDs as control

### Exception Handling

1. If there is missing nostro/multi nostro exception for util cashflow, FMO needs to add/delete nostro for cashflow processing.
2. If cashflow settlement means is set as FXBRREC/FXBRREC_M, then will not be switched to the other. 1. If the client static is updated, then only newly comes cashflow will have the update settlement means/account
3. If accounting entry got MISS_INFO, then Utilization ops needs to manually handle in Oscar.
4. If cashflow is utilized, but trade is amendment/cancelled, cashflow in Ratan will be in ERROR status and not support for any further action, user needs to manually process accounting entry in Oscar. | | | Trade Id | Product | Cashflow Id | Cashflow Status | Major Version | Payment Type | Currency | Payment Date | Payment Amount | Remaining Amount | Settlement Means | | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | | 7/20/2025 | Trade booking | T01 | Forward | C01 | PROJECTED | 2 | Cashflow | SAR | 8/1/2025 | 800 | 800 | | | | | T01 | Forward | C02 | PROJECTED | 2 | Cashflow | USD | 8/1/2025 | 100 | 100 | | | | | | | | | | | | | | | | | 7/25/2025 | Materialization | T01 | Forward | C01 | READY | 2 | Cashflow | SAR | 8/1/2025 | 800 | 800 | FXBRREC | | | | T01 | Forward | C02 | READY | 2 | Cashflow | USD | 8/1/2025 | 100 | 100 | FXBRREC | | | | | | | | | | | | | | | | 8/1/2025 | Auto Utilization | T01 | Forward | C01 | UTILIZED | 2 | Cashflow | SAR | 8/1/2025 | 800 | 800 | FXBRREC | | | | T01 | Forward | C02 | UTILIZED | 2 | Cashflow | USD | 8/1/2025 | 100 | 100 | FXBRREC | | | Stella failed on hard block | | | | | | | | | | | | | 8/1/2025 | Trade Amendment | T01 | Forward | C01 | ERROR | 2 | Cashflow | SAR | 8/1/2025 | 800 | 800 | FXBRREC | | | | T01 | Forward | C02 | ERROR | 2 | Cashflow | USD | 8/1/2025 | 100 | 100 | FXBRREC | | | | T01 | Forward | C03 | ERROR | 2 | Cashflow | SAR | 8/1/2025 | 700 | 700 | FXBRREC | | | | T01 | Forward | C04 | ERROR | 2 | Cashflow | USD | 8/1/2025 | 100 | 100 | FXBRREC |
5. If accounting entry got NACK from EBBS, ops will manually handle

### Utilization Static

- Utilization Static (Client Static) sample data

| Entity FMID | Entity FMCODE | Counterparty FMID | Counterparty FMCODE | is Auto Util |
| --- | --- | --- | --- | --- |
| 401036553 | SCB EGYPT*CAI | 401039206 | TBFX EGYPT*CAI | Yes |
| 401036553 | SCB EGYPT*CAI | 400818384 | OBATBFX*ACC | Yes |
| 400991880 | SCB SAUDI*RYD | 400992471 | TBFX SAUDI*RYD | Yes |

- Nostro Static - Copied FXBRREC nostro set to FXBRREC-M - For any new utilization currency/nostro onboarding, nostro should be setup for both FXBRREC and FXBRREC-M.

## Last Mile Check

With the increasing business handled by RATAN and the complexity of the business, in order to prevent wrong payment or duplicated payment, we add a final inspection mechanism.
technical design can refer to:  [Last Mile Checker - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Last+Mile+Checker)

currently we are still in **phase **1 which only do technical verification,
in **phase **2 will do business go live then will have one action in cashflow blotter or dashboard; may be as shown in the figure below
![image-2026-7-9_10-28-17.png](attachments/image-2026-7-9_10-28-17.png)

# Dashboard

A Dashboard has been added to provide a Control Tower view of exceptions that require action.

<<This is a handy guide and does not remove the need to monitor and clear the queue directly>>

Group Pending Validation – normally this should automatically get cleared as and when trades are validated. It's useful for Settlements to know if there are cashflows that would flow into Settlement queue post Validation.

**For the rest of the items, Settlements team need to periodically monitor and action the exceptions on timely basis and especially before respective currency payment cut-offs. **Where required, the issue is to be raised to RATAN PSS

![image-2026-5-11_21-41-50-1.png](attachments/image-2026-5-11_21-41-50-1.png)

# FMRP - China Drop 2 (New booking via Blade / STELLA / CFETS)

As part of on going Murex 2.11 decommission work, new trade booking has been enabled via the new FMRP Tech Stack. Deals will be booked either directly in Blade or flown from upstream systems like S2BX / CFETS.

Products in Scope are IRS, CCS, NDF, SCF and FX, only for specific portfolios of Linear Rates Desk and Country = China.

![image2024-5-2_11-19-51.png](attachments/image2024-5-2_11-19-51.png)

Events in Scope are Trade  (New Booking) | Amendment | Withdrawal (Cancellation) | Termination (Full Cancellation with Fee) | Partial Termination (Amendment with Fee) | Close-Out (Only for FX) | Novation (Remaining Party Full) | Portfolio Re-assignment | Expiry (Move from Live to Dead status)

Events Handling in RATAN

| Business Event + Action | Drop 2/Drop3 Handling | Exception |
| --- | --- | --- |
| Trade + Book | No event related NSTP rules | - |
| • Trade + Cancel • Withdrawal + Book | NSTP if original cashflow is released, else cancel original | Reversal |
| •Trade + Update •Amendment /Termination / Partial Termination / Novation + Book | NSTP Cancellation & New if original cashflow is released | Cancellation: Reversal New: Rebook |
| Close Out + Book (New Trade ID will be generated) | Close-out trade will flow to RAZOR FX directly | - |
| Portfolio Re-assignment + Book (New Trade ID will be generated) | •All cashflows from Old trade will be cancelled and generated on new trade ID. •Old trade cashflows will be NSTP as ‘REVERSAL’. New trade cashflow will be NSTP as ‘Port Reassign’. Ops to check whether payment was originally sent and if yes, suppress on new trade. Else pay from new trade | Reversal Port Reassign |
| Trade + Revive (Undo) | • Original Payment not Released: Original Cashflow which went to cancelled status will now become live again • Original Payment released, but Cancellation not yet released: Cancellation will be discarded, original cashflow will remain in Released status • Cancellation (MTx92) Released: FO & MO should not be able to do Undo | - |
| Fixing | NSTP if there was another cashflow which was amended post payment release (same period) | Rebook |
| Trade + Expiry | Discard expiry event cashflow | |

Points to Note:

- FX will directly be replicated to RAZOR, and wont flow to RATAN. However, Fees related to FX bookings will still settle in RATAN (same as MX2.11 behavior).
- Settlement Method - DVP: Currently Strategy is used in MX2.11 to identify DVP trades. In FMRP, 'Settlement Method' is used. Exception code will be 'DVP'.** Please settle the cashflows on DVP basis**. - CCP: For IRS deals, 'CCP' Settlement Method will be tagged as below - AGENCY: Deals booked under IR_CFETSAGENCY strategy in MX2.11 In FMRP, this is related to a certain set of trades executed on CFETS with a specific counterparty in HK
- Validation status Exception - Currently in MX2.11, cashflows do not come to settlement queue before validation. - However, in FMRP, cashflows will come to settlement queue same time as it is booked, irrespective of Validation status. - Until Validation status is built into the F2B workflow (expected in early Q3), a NSTP exception "CCS: Check Validation Status" is added for CCS notional payments alone (since only CCS has notional exchange on trade date). - IRS will have interest payments which will be months away before which Validation would be completed). FX, NDF and SCF do not go through Validation in BAU, so not applicable.
- IRS Handling - IRS two leg cashflows from new booking (Fixed+Fixed / Fixed+Floating / Floating+Floating) will get auto netted. - Amendment post payment release: If there is amendment post release of net payment, the reversal & re-book legs will appear separately and need to be netted manually - Cancellation post payment release: In case of outright cancellation, reversal cashflows of two legs will appear in queue separately - the direction will be opposite of the original booking. - If the two reversal cashflows are netted, the net cashflow must not be released from RATAN, as it is not directly linked to the net amount of the original payment - Where required, cancellation message MT192/292/MT199/MT299 should be released via AMH.
- Stella CORP Exception - Currently Settlement Method changes in BLADE are not consumed by RATAN, so a temporary NSTP condition "Stella_Corp_CCS" has been added for CCS trades since only CCS has exchange of currencies - When this exception is encountered, please check if the trade is expected to be settled on DVP basis and handle accordingly
- Portfolio Reassignment: - All cashflows on a trade from the original booking date until final expiry will be cancelled on the old trade ID and booked in new trade ID - Old Trade ID cashflows will show 'Reversal' exception and New Trade ID cashflows will show 'Portfolio Reassignment' exception. - Please check whether payments have been already released on old Trade. If yes, the payment on new trade needs to be suppressed to avoid duplicate payment. - If payment was not released on Old Trade ID, it must be released from the new Trade ID to avoid missed payment.
- FDL, WHT and Adhoc Netting - Previously these exceptions were setup specifically using Murex LABELs. Now they have also been setup based on FMCODE to take effect on STELLA cashflows.
- Fee and Stella Cashflows are temporary exceptions added as a safeguard and will be removed.

**IRS**

| **Value from CFETS** | **Meaning of Value** | **STELLA Mapping to Sett Method** | **Comments** |
| --- | --- | --- | --- |
| 13 | Bilateral self settlement | GROSS | |
| 6 | clearing by SHANGHAI CLEARING HOUSE | CCP | |

**CCS**

| **Value from CFETS** | **Meaning of Value** | **STELLA Mapping to Sett Method** | **Comments** |
| --- | --- | --- | --- |
| 1 | Bilateral net settlement | GROSS | Default to Gross CFETS did not send a trade in the past 5 year |
| 2 | Bilateral full settlement | GROSS | |
| 3 | Centralized net settlement | GROSS | Default to Gross CFETS did not send a trade in the past 5 year |

NSTP Exceptions Added:

| Exception Criteria | Exception Code | Level |
| --- | --- | --- |
| Settlement_Method==DVP | DVP | MAKER_CHECKER |
| Trade_Original_Source_System_Name<> CFETS & Instrument_Common.ISDA_Taxonomy in('InterestRate:CrossCurrency:FixedFixed','InterestRate:CrossCurrency:FixedFloat', 'InterestRate:CrossCurrency:Basis','InterestRate:CrossCurrency:FloatFloat') & payment type in( InitialExchange/Fixed, InitialExchange/Float) | CCS: Check Validation Status | MAKER_CHECKER |
| Instrument_Common.ISDA_Taxonomy in ('InterestRate:CrossCurrency:FixedFloat', 'InterestRate:CrossCurrency:Basis', 'InterestRate:CrossCurrency:FloatFloat', 'InterestRate:CrossCurrency:FixedFixed')&&Data_Flow.Data_Source_System==Stella&&Entity.Counterparty_Client_Type==CORP | Stella_Corp_CCS | MAKER_CHECKER |
| Cashflow.Payment_Type in ('UpfrontFee', 'AmendmentFee', 'NovationFee', 'TerminationFee') | Fee | MAKER_CHECKER |
| Parent_Trade_Id!=#Trade_Id&&Data_Flow.Data_Source_System in ('Stella', 'stella', 'STELLA') | Portfolio reassignment | MAKER_CHECKER |
| Data_Flow.Data_Source_System==Stella | Stella cashflows | MAKER_CHECKER |
| Entity.Counterparty_SCI_FMCODE in ('ABBBJSWITCHGEAR*BJG','ABBCHONGQING*CQG','ABBELECTRICAL*SHA','ABBHEFEI*HEF','ABBLVINSTALLAT*BJG','ABBSHANGHAI*SHA','ABBSHMOTORS*SHA','ABBTJSWITCHGEAR*TIA', 'ABBXHLOWVOLTAGE*JIA','ABBXMELECTRICAL*XIA','ABBXMLOWVOLTAGE*XIA','ABBXMSWITCHGEAR*XIA','ABBZHONGSHAN*ZSN','ALINK WHEEL LYG*LYG','ANGLOAMERICAN*SHA','BANKOFDG*DGG','BANKOFDL*DLN', 'BASF METALS*SHA','NINGBO COMM BK*NGB','BK OF SUZ CO LTD*SUZ','BANK OF JIANGSU*NJG','BMW BRILLI AUTOM*SYG','BQDWEALTH*QDO','CAINTTRUST*XIN','SINOPLATMETALS*KMG','CDPGROUP*SHA', 'CHENGTONGPRECIOU*BJG','CHENGTUNMINING*XIA','CHINA BOHAI B*TIA','CHINA GALAXY SEC*BJG','CHINA INT CAP CO*BJG','CNMETALCO*SHA','CHINA PLATINUM*SZN','CHINASOFT*GCN','CHINA INTL MAR*SZN', 'CHOW SANG SANG*GZU','CITIC SECURITIES*BJG','CMBWEALTHMANAGE*SZN','CMCNINGBO*NGB','CNFUBONBK*SHA','CHINA SECUR CO*BJG','CNSINOPACBK*NJG','CTDCIBMBKTY*LDN','EASEBOND ELECTRI*SZN', 'EASTCOMPEACE*GDG','EVERBRIGHTWM*QDO','EXPRESS LUCK*SZN','FTELDCSHMTL*SHA','FTERIDGEWAY*SHA','FTESTILLWATER*HNZ','FT HUAQINTLCM*HKG','FTNCDBLEASING*HKG','FTNKORRUN*SHA', 'FTNTOPRANK*WC','FTNVOVOMART*NGB','FTNZHONGDINGHK*HKG','FT SHA KEERUN TR*SHA','BANK OF QIN CO L*QDO','GF SECURITIES*GZU','GRAPHICS*BJG','GUOTAI JUNAN SEC*SHA','HANGZHOU COGEN*HNZ', 'HAITONG SEC CO*SHA','HAITONG*SHA','HERAEUS MTLS SHA*SHA','HES HUA RON*JIA','HNZOOMWEZYAMT*CGS','HUA TAI SEC*NJG','HYUNDAI FIN LEA*SHA','IND & CO CH*BJG','INTL FAR EAST LEASING*SHA', 'JIANGSU JIA COP*SUZ','JIANGXI COPPER*SHA','JINTIAA*NGB','JUSHI GROUP*ZJG','LG CHEM NANJING*NJG','LGESTECNJ*NJG','LOUI DRE COM SHA*BJG','MITSUBISHI*SHA','NAVALANT*HNZ', 'NCHUAQINELECTRON*ANG', 'NIOCOLTD*SHA','NJSHUSHAN*NJG','PATFENGHERILI2*SZN','PINGANWEALTH*SZN','POONGSAN SZN CO*SZN','PSBCWEALTH*BJG','QDLIDONG*QDO','RIDGEWAYSH*SHA','SANJIANGCHEMICAL*JIX','SANY HEAVY IND*CHG', 'SEALANDSECURITIE*GUN','SGS CSTC STD TIA*TIA','SHAANXITRUST*XIN','SHANGHAI CLE HOU*SHA','SHAN KEERUN TCL*SHA','SHA RURAL COM BK*SHA','SHANGHAI YUYUAN*SHA','SHENZ SKYW DIGIT*SZN', 'SHZ CN ST OPTO*SZN','SINO PLATINUM*SHA','SINO PLATINUM*KMG','SINOPAC SEC CORP*TPE','SORIN SHA CORPT*SHA','SHANGHAI PUD*SHA','SWSMUFUND*SHA','SZCHUANGWEIRGB*SZN','SHEN DEV B*SZN#', 'SZJXCOPPER*SZN','SZMEGMEET*SZN','SZN CN STR OPT*SZN','TIANJIN CITY COM*TIA','TRAFIGURA TDG*SHA','TSINGSHAN HOLD*WHO','WANXIANG RESOURC*SHA','XIAMEN C N D INC*XIA','XIAMEN ITG GROUP*XIA','XIANELECTRICENG*XIN','XMITGNONFERROUS*XIA','YIXING YIDA*SUZ','YUNTIANHUA UNIT*KMG','ZHEJIANG HAILIAN*ZJG','ZHEJIANG METALS*HNZ','ZHESHANGDEVELOP*HNZ','ZHONGYUANBANK*ZZU', 'ZIJINCOPPER*FJN','ZIJIN MINING*FJN','ZJMATERIALS*HNZ','ZJWOLONG*ZJG','ZSUROLOGY*SZN') | Adhoc Netting FMCODE | MAKER_CHECKER |
| Entity.Counterparty_SCI_FMCODE in ('MICASA ENTERPRI*HKG','ELISE ENTERPRISE*TTL','FT HUAQIN TLCM*HKG','FTNCHANZ*KOW','GEMTEK TECH*HSI','IRICOINT*TTL','RUNXLIMITED*CB','SITC CONTAINER*HKG','SPRUCE*HKG', 'XIN YA GLOVE IND*JGU','SINOSTAR ENG*BJG') | WHT FMCODE | MAKER_CHECKER |
| Entity.Counterparty_SCI_FMID in (400886173, 400888745, 400901589, 400760276, 400229866, 400201189, 400213780, 400208383, 400914029, 400905340, 400894281, 400909944, 400919759, 400940594, 400944993, 400946120, 400958989, 400927236, 400929839, 400961558, 400954356, 400957726, 401004507, 401018572, 401037356) | CHINA FDL Client | MAKER_CHECKER |

Screenshots:

**<u>Trade + Cancel (</u><u>4357593973)</u>**

![Trade1.png](attachments/Trade1.png)

![Trade2.png](attachments/Trade2.png)

![Trade3.png](attachments/Trade3.png)

![Trade4.png](attachments/Trade4.png)

![Trade5.png](attachments/Trade5.png)

**<u>Cancelled.</u>**

![Trade6.png](attachments/Trade6.png)

![Trade7.png](attachments/Trade7.png)

![Trade8.png](attachments/Trade8.png)

![Trade9.png](attachments/Trade9.png)

![Trade10.png](attachments/Trade10.png)

![Trade11.png](attachments/Trade11.png)

**<u>Withdrawal + Reversal – ( Trade id 4357595347)</u>**

<u>![Trade12.png](attachments/Trade12.png)</u>

<u>![Trade13.png](attachments/Trade13.png)</u>

<u>![Trade14.png](attachments/Trade14.png)</u>

<u>![Trade15.png](attachments/Trade15.png)</u>

**<u>Amendment (Trade id 4360657843)</u>**

**<u>![Trade 1.png](attachments/Trade 1.png)</u>**

<u>Mo has performed amendment as of 10 May 2024 as amended spread of trade from 21bps to 12bps</u>

<u>![Trade 2.png](attachments/Trade 2.png)</u>

<u>![Trade 3.png](attachments/Trade 3.png)</u>

<u>**Full termination performed - 4357595553 as of 18 dec 2023 with fee payment of USD 1000 value 20 dec 2023**</u>

![Trade 1.png](attachments/Trade 1.png)

![Trade 2.png](attachments/Trade 2.png)

![Trade 3.png](attachments/Trade 3.png)

![Trade 4.png](attachments/Trade 4.png)

<u>**Novation performed as of 7 feb 2023 for this trade 4357594678 **</u>

<u>**CP novated from BK OF TYO MITSUB*SHA to SHANGHAI CLE HOU*SHA**</u>

<u>**![Trade 5.png](attachments/Trade 5.png)**</u>

<u>**![Trade 6.png](attachments/Trade 6.png)**</u>

<u>**![Trade 7.png](attachments/Trade 7.png)**</u>

<u>**![Trade 8.png](attachments/Trade 8.png)**</u>

<u>**![Trade 9.png](attachments/Trade 9.png)**</u>

<u>**![Trade 10.png](attachments/Trade 10.png)**</u>

**<u>Partial Termination Trade id - 4357637380</u>**

**<u>![Trade 11.png](attachments/Trade 11.png)</u>**

**<u>![Trade 12.png](attachments/Trade 12.png)</u>**

**<u>![Trade 13.png](attachments/Trade 13.png)</u>**

**<u>![Trade 14.png](attachments/Trade 14.png)</u>**

**<u>Trade + Revive (Undo) 4357637368</u>**

**<u>![Trade 15.png](attachments/Trade 15.png)</u>**

**<u>![Trade 16.png](attachments/Trade 16.png)</u>**

**<u>Cancelled</u>**

**<u>![Trade 17.png](attachments/Trade 17.png)</u>**

**<u>![Trade 18.png](attachments/Trade 18.png)</u>**

**<u>Undo performed.</u>**

**<u>![Trade 19.png](attachments/Trade 19.png)</u>**

**<u>![Trade 20.png](attachments/Trade 20.png)</u>**

**<u>Portfolio Re-assignment + Book 4357637253</u>**

**<u>![Trade 21.png](attachments/Trade 21.png)</u>**

**<u>![Trade 22.png](attachments/Trade 22.png)</u>**

<u>**4357637253 - Portfolio re-assignment done, new trade 4357641020**</u>

<u>**![Trade 23.png](attachments/Trade 23.png)**</u>

<u>**![Trade 24.png](attachments/Trade 24.png)**</u>

<u>**![Trade 25.png](attachments/Trade 25.png)**</u>

<u>**![Trade 26.png](attachments/Trade 26.png)**</u>

**<u>Fixing- 4360658037</u>**

**<u>![Trade 4.png](attachments/Trade 4.png)</u>**

<u>Mo has performed the amendment as of 20 may 2024 amended 2nd calculation period to have customized fixing rate of 5.5%</u>

<u>![Trade 6.png](attachments/Trade 6.png)</u>

<u>![Trade 5.png](attachments/Trade 5.png)</u>

# LOANIQ Highlights

**How to identify LOANIQ cashflow**

- Trade original source system value is "LOANIQ", user can create customize filter to get LOANIQ data ![image2024-11-6_10-51-49.png](attachments/image2024-11-6_10-51-49.png)![image2024-11-6_10-53-6.png](attachments/image2024-11-6_10-53-6.png)
- Product Taxonomy in ("Credit:LoansTermLoan", "CreditLoans:RevolvingTermLoan"), user can select the value in quick search section ![image2024-11-6_10-55-0.png](attachments/image2024-11-6_10-55-0.png)

**LOANIQ specific process:**

- Cashflow received with "Affirmed" status, no user affirmation or trade confirmation required
- There is no amendment/withdrawal cashflow event for LOANIQ. - To withdrawal any payment, user will book new opposite direction cashflow for it - In case of amendment there is an adjustment cashflow generated instead of withdrawal + new
- Swift/Accounting is generated in Razor and send to FMSRE
- Tag20 prefix is LQ in swift message
- User should not net LOANIQ cashflow with other FMRP cashflow
- New attributes - **Is Netting Required** (for LOANIQ) - Indicator to show if netting required. There is NSTP rule created in RATAN to hold the cashflow if the value is true.

- - **General Ledger Owner Id **（for LOANIQ）- Indicator to link the payment in LOANIQ. If the cashflow hit "Netting Required" exception, ops user should check and net the cashflow with the same general ledger owner id.

**Vostro SI **

- LOANIQ vostro SI are maintained separately from existing Murex SIs
- Loaniq SSI should be maintained with XQXXXX security in SSI + (XQXXXX security is mapped to XQ**** CFI code)
- if SC prefix required for specific SSI having sort code, the value should be updated in SSI+
- FEDWIRE SSI - for initial go live existing and new Fedwire SSI will not contain the fedwire number as this is not mandatory for settlement. Once Ratan is able to handle it, this process can be revisited.
- Loan ops will handle the process of Loaniq SSI maintenance

**DO not use SwiftSuppress **

- Razor flow does not allow swift suppress option - its result is same as Cashflow Suppress

**Temporary NSTP after initial go live**

- Loaniq cashflows will be NSTP for an initial period similar to how all SLT cashflows are NSTP in Murex
- Loan ops will provide SSI details for settlement via mail similar to Murex
- Sett ops to verify the SSI attached accordingly or add SSI as per loan ops instruction

# Interface Issues Handling

**MX2.11 to RATAN**

- Realtime Ack / Nack exists between MX2.11 and RATAN
- When Cashflows are published from MX2.11, they are moved to SNTR status
- When Cashflows are released from RATAN, a status update is sent to MX2.11 to move the cashflows to RLSR status for hard block purpose
- In case Ack is not received within OLA (5 minutes), an alert will be given to PSS who will investigate the issue
- In case required, PSS will advise Settlements team, who need to right click on cashflow and re-trigger the status update to MX2.11

![statuswriteback.JPG](attachments/statuswriteback.JPG)

**RATAN to RAZOR**

- Ack / Nack exists between RATAN and RAZOR for non-FMRP cashflow
- Any OLA break will be monitored by PSS via ITRS
- If there is loss of message due to interface issue, Settlements team can right click and re-publish the Cashflow to RAZOR on advise from PSS

**RATAN to FMSGW**

- Ack / Nack exists between RATAN and FMSGW for FMRP cashflow
- Any OLA break will be monitored by PSS via ITRS

# Korea Exception Blotter

## User Access

1.User access and profile

| S/N | SYSTEM | ROLE_NAME | Bank ID | Resource Name | SUBJECT | ACTION |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | RATAN | KR_Ops user | 1370564 | Bae, Na Mi | KR Exceptions Blotter | Edit |
| 2 | RATAN | KR_Ops user | 1372116 | Yang, Ji Hoon | KR Exceptions Blotter | Edit |
| 3 | RATAN | KR_Ops user | 1371935 | Cho, Hye Won | KR Exceptions Blotter | Edit |
| 4 | RATAN | KR_Ops user | 1372224 | Choo, Ji Won | KR Exceptions Blotter | Edit |

| S/N | SYSTEM | ROLE_NAME | Bank ID | Resource Name | SUBJECT | ACTION |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | RATAN | KR_PSS | 1655921 | Oh, Jae Hyeon | KR Exceptions Blotter | Read Only |
| 2 | RATAN | KR_PSS | 1368983 | Lee, Su Jung | KR Exceptions Blotter | Read Only |
| 3 | RATAN | KR_PSS | 1372554 | Jin, Yeon Su | KR Exceptions Blotter | Read Only |
| 4 | RATAN | KR_PSS | 1536845 | Kwon, Ye Jin | KR Exceptions Blotter | Read Only |
| 5 | RATAN | KR_PSS | 1602370 | Park, Hee Jin | KR Exceptions Blotter | Read Only |

2. Approver list

| Role Name | Owner of the Approver Group | Approver Group Members | Approver Group Member's Bank ID | Group Email |
| --- | --- | --- | --- | --- |
| FMO_KR_OPS | Yang, Ji Hoon | Yang, Ji Hoon; Bae, Na Mi; Cho, Hye Won; Choo Ji Won | 1372116; 1370564; 1371935; 1372224 | [dok_settle@sc.com](mailto:dok_settle@sc.com) |
| KR_PSS_RO | [오재현(Oh, Jae Hyeon) ](mailto:JaeHyeon.Oh@sc.com) | [오재현(Oh, Jae Hyeon)；이수정(Lee, Su Jung) ](mailto:JaeHyeon.Oh@sc.com) | 1655921; 1368983 | [SCBK.FM_Support@sc.com ](mailto:SCBK.FM_Support@sc.com) |

3. ID Creation/Amendment/Revoke Account: [RATAN ID Access - myIT](https://scbnow01.service-now.com/myit?id=sc_cat_item&table=sc_cat_item&sys_id=4df8849b879279d0f10884070cbb353b&searchTerm=RATAN)

## MX message Exception Blotter

| Murex(Korea) -> MQ(MxML)->RATAN→FM solace(MX&MT210)->ENISIS | Murex send out the MT & MxML but RATAN didn't receive | 1. Murex would send exception email to Korea FMO 2. Korea FMO check with PSS/dev team what's the actual issue, if there's tech issue which the payment can't be resumed by system manually draft the MX message in ENISIS or draft the payment in OSCAR |
| --- | --- | --- |
| RATAN Swift exception due to invalid Murex data | 1. RATAN won't return ACK to Murex, Murex would send exception email to Korea FMO 2. Korea FMO check with PSS/dev team what's the actual issue, if there's tech issue which the payment can't be resumed by system manually draft the MX message in ENISIS or draft the payment in OSCAR |
| **RATAN Swift generation exception** | 1. **Korea FMO can monitor the exceptions from RATAN MX exception blotter** 2. **Korea FMO can check with PSS/dev team what the actual reason of the exception is** 1. **If the exception is caused by static data setup or service temporarily not available, Korea FMO can manually replay the message after static data corrected or service resumed, Korea FMO would replay from the MX exception blotter to retrigger the MT to MX conversion** 2. **If there's a tech issue which the payment can't be resolved by replay, Korea FMO can manually draft the MX message in ENISIS or draft the payment in OSCAR** |
| Message sent by RATAN but not received by ENISIS | 1. SSDR extract the payment report, Korea FMO download the report from SSDR 2. Korea FMO manually extract the MX message from ENISIS by source system 3. Korea FMO ops manually compare the SSDR report with ENISIS extraction and identify the discrepancy. In case there's missing or failure payment in ENISIS, Korea FMO manually draft the MX message in ENISIS or draft the payment in OSCAR |

### Log in

1st step

Production link - will update when deploy in production environment

Test Link in UAT2 as below

| [https://uklvadapp1344.uk.dev.net:8453/?show_normal_login=y](https://uklvadapp1344.uk.dev.net:8453/?show_normal_login=y) |
| --- |

Test Log in - user ID and password

| Username | Password | Role |
| --- | --- | --- |
| 1370564 | SCBpassword2$ | FMO_KR_OPS |
| 1372116 | SCBpassword2$ | FMO_KR_OPS |
| 1371935 | SCBpassword1$ | FMO_KR_OPS |
| 1372224 | SCBpassword2$ | FMO_KR_OPS |
| 1655921 | SCBpassword1$ | KR_PSS_RO |

![image-2025-7-29_11-26-17-1.png](attachments/image-2025-7-29_11-26-17-1.png)

2nd step

Click the upper right corner 'New Tile', then you will find 'Exception Management - Korea MX Exception'.

![image-2025-7-30_8-31-39.png](attachments/image-2025-7-30_8-31-39.png)

3rd step

Clink 'Exception Management - Korea MX Exception'

pagination - 20/50/100

![](https://confluence.global.standardchartered.com/download/attachments/3414332761/image-2025-7-28_19-7-17.png?version=1&modificationDate=1753700838000&api=v2)

![](https://confluence.global.standardchartered.com/download/attachments/3414332761/image-2025-7-28_19-7-30.png?version=1&modificationDate=1753700851000&api=v2)

### Exception Blotter

#### Replay and Close Single Exception

1.Repay Successfully

Eg. When you click 'replay' for flow ID 100000380', a message is up 'are you sure to replay flow ID 100000380', then you can update comment and click 'ok'.

![image-2025-7-30_8-57-42.png](attachments/image-2025-7-30_8-57-42.png)

Then, you will find flow ID 100000380 disappear automatically in exception blotter, it means replay successfully and this MX can be sent to ENISIS, you can verify if you can find it in ENISIS.

![image-2025-7-30_9-0-46.png](attachments/image-2025-7-30_9-0-46.png)

2. Replay Fail

Eg. When you click 'replay' for flow ID 100000364, a message is up 'are you sure to replay flow ID 100000364, then you can update comment and click 'ok'.

![image-2025-7-30_11-13-35.png](attachments/image-2025-7-30_11-13-35.png)

This exception replay is fail, then it will list top of exception list.

![image-2025-7-30_11-37-26.png](attachments/image-2025-7-30_11-37-26.png)

Then, for exceptions which cannot be resolved by replay in the exception blotter, Korea FMO would manually draft the payment in Oscar or MX in ENISIS.

If Korea FMO manually draft the payment in Oscar or MX in ENISIS successfully, then please click 'close' at the right,  a message will pop up 'are you sure to close exception 100000364', then please update in comment and click 'ok', then this exception will be removed from exception blotter.

E.g. this example just show how to close, not corresponding case of 100000364, the 'close' method is the same.

If Close, then click 'close' at the right, the exception will be removed from exception blotter.

![](https://confluence.global.standardchartered.com/download/attachments/3414332761/image-2025-7-28_18-50-24.png?version=1&modificationDate=1753699826000&api=v2)

#### Replay and Close Multi Exceptions

1.Multi replay successfully

Eg. When you click 'replay selected' for flow ID 100000230 and 100000229', a message is up 'are you sure to replay flow ID 100000230 and 100000229', then you can update comment and click 'ok'.

![image-2025-7-30_13-5-18.png](attachments/image-2025-7-30_13-5-18.png)

Then you will find flow ID 100000373 and 100000229 disappear in exception blotter, it means replay successfully and these 2 MX can be sent to ENISIS, you can verify if you can find them in ENISIS

![image-2025-7-30_13-9-6.png](attachments/image-2025-7-30_13-9-6.png)

2.Multi replay fail

Eg. When you click 'replay selected' for flow ID 100000373 and 100000374, a message is up 'are you sure to replay flow ID 100000373 and 100000374, then you can update comment and click 'ok'.

![image-2025-7-30_13-20-5.png](attachments/image-2025-7-30_13-20-5.png)

The 2  exception replay is fail, then they will list top of exception list.

![image-2025-7-30_13-23-11.png](attachments/image-2025-7-30_13-23-11.png)

Then, for exceptions which cannot be resolved by replay in the exception blotter, Korea FMO would manually draft the payment in Oscar or MX in ENISIS.

If Korea FMO manually draft the payment in Oscar or MX in ENISIS successfully, then please click 'close' at the right,  a message will pop up 'are you sure to close exception 100000373 and 100000374', then please update in comment and click 'ok', then the 2 exceptions will be removed from exception blotter.

E.g. this example just show how to close, not corresponding case of 100000373 and 100000374, the 'close' method is the same.

If Close, click 'close' at the right and the 2 exceptions will be removed from exception blotter.

![](https://confluence.global.standardchartered.com/download/attachments/3414332761/image-2025-7-28_19-1-35.png?version=1&modificationDate=1753700496000&api=v2)

#### Customized View

Step 1 - Click 'create Or modify' at the upper right corner

![image-2025-7-30_14-57-27.png](attachments/image-2025-7-30_14-57-27.png)

Then you will enter into View Builder

Step 2 - you can click 'delete' to move the field name from 'Display View' to 'Available Fields'. Then the fields you deleted will be moved to 'Available Fields'

![image-2025-7-30_15-5-51-1.png](attachments/image-2025-7-30_15-5-51-1.png)![image-2025-7-30_15-7-46.png](attachments/image-2025-7-30_15-7-46.png)

Then the latest exception blotter will be shown without the fields you removed.

![image-2025-7-30_15-11-47.png](attachments/image-2025-7-30_15-11-47.png)

Or if you would like to create your own View, you can input a name in the blank and then click 'create view' and click 'private', then your 'View' can be saved.

![image-2025-7-30_15-14-58.png](attachments/image-2025-7-30_15-14-58.png)

Then close the 'View builder', you can select the name you created from the dropdown, then your customized view will be shown

![image-2025-7-30_15-21-9.png](attachments/image-2025-7-30_15-21-9.png)![image-2025-7-30_15-23-26.png](attachments/image-2025-7-30_15-23-26.png)

If you need resume the original view, please click 'Clear', then original view will be show.

![image-2025-7-30_15-25-9.png](attachments/image-2025-7-30_15-25-9.png)![image-2025-7-30_15-26-23.png](attachments/image-2025-7-30_15-26-23.png)

#### Audit Trail

Audit Trail at RATAN backend, Route - RATAN ONE ->Schemas->ratanone_swift_service->tables→ratanone_swift_coversion_record

SQL - select * from ratanone_swift_service.ratanone_swift_conversion_record rscr where rscr.source_system = 'KR_MUREX' by rscr.created_at desc;

If user need check exception log, please reach out to RATAN team [Sylvia.Huang@sc.com](mailto:Sylvia.Huang@sc.com) or [BruceXinxin.Feng@sc.com](mailto:BruceXinxin.Feng@sc.com)

# Korea Settlement Section

[Ratan One Processing Guide(DOI)-Korea - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Ratan+One+Processing+Guide%28DOI%29-Korea)