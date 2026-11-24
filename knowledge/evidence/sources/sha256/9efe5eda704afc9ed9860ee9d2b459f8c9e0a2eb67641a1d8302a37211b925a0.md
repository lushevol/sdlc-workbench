#

# Background

Current new-entity onboarding requires multiple backend configuration changes and static data imports that must be deployed on scheduled release windows. This creates a long lead time and limits the team’s ability to respond quickly to business needs. The goal of this requirement is to introduce a user self‑service solution that streamlines onboarding, improves turnaround time, and reduces dependency on scheduled deployments.

# ADO

[https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/11351733](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/11351733)

# Requirement Details

- ~~**Option 1**: provide excel template for user to import all the static via file, system will import the data to backend table.~~
- **Option 2: **build new blotter for new entity onboarding, and required static are added as sub tiles

### **User Profile**

Static ops have edit access , other user profile have read only access - same as existing nostro static blotter

### Process Impact

- After the change, data ops add static from UI (update cashflow suppression rule, nostro static, currency mapping (NEW), New Entity onboarding (New))
- MX bifurcation logic to be updated from backend
- If new country code added, EBBS connection, Accounting schedule job to be created from backend
- If CPT required, CPT control adding/removal need to be done from backend
- Any Other Country Specific requirement need specific analysis.
- After Entity Onboarding, data ops can update the static, will this require additional control? or directly take effect after data updated.

### **Static Details**

| Section | Section Mandatory? | Field Name | Description | Open Questions | Mandatory? | Editable? | info in UI? | Validation Rules | Impacted Table/Config |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| (HEADER) | Y | Booking Entity FMID | Internal FM identifier of the booking entity | | Y | N | NA | only digit | - Strtegic_FM_list which is used to control swift generation scope - Unique key in other entity related static |
| Booking Entity FMCODE | Business code of the booking entity associated with the FMID | | Y | N | NA | (system auto populate when FMID added) | related info to Booking entity FMID |
| Branch Code | Two-character code identifying the branch | Is there any golden source for the field, any other validation can be added to make sure user input is correct? Deepak will check with Razor/GPTM set up | Y | Y | NA | 2-characters | impact Swift generation and Accounting process |
| Currency Mapping | N (not link to entity directly, PO suggest to have separate blotter/section.) --if no ccy rounding static added, system will directly use the amount from upstream | Currency | the payment currency from cashflow, it can be ISO or non-ISO ccy | | Y | Y | if this is non-ISO ccy, add the mapped ISO ccy in the column "ISO Currency" | 3-characters | |
| Precision | Defines the decimal precision rule for a currency，(for example, 0, 1,2, or 3 decimal places). It is used for rounding | this was built for Murex as tactical solution, will this impact FMRP cashflow? Deepak will check | Y | Y | the number of decimals | digits dropdown, and manual inpur | |
| Rounding Type | Dropdown list: - ROUNDING_OFF - ROUNDING_DOWN - ROUNDING_UP | | Y | Y | add description and example | Dropdown list | |
| ISO Currency | The ISO standard currency code used to identify the currency | | N | Y | | Dropdown list, and allow user manual input | |
| Release Time | Y | Currency | the payment currency from cashflow, it can be ISO or non-ISO ccy | | Y | Y | | 3-characters | |
| Release Time (GMT) | the time when the cashflow will be released from RATAN | guidance to set the time | Y | Y | Good to have : check if possible to have user input local time and time zone, system convert to GMT time | time | |
| Release Date | define if the cashflow need to be released at or before VD dropdown list: - VD-2 - VD-1 - VD | | Y | Y | | dropdown list | |
| ~~cutoff shifter unit~~ | default to "BUSINESS DAY" from backend | | Y | N | | default value | |
| Swift Generation | N | Sender BIC | the booking entity bic and will be used in block 1 of swift message | | Y | Y | | | |
| Country Code | required by downstream, by default set to substr (sender bic,5,2) --SCBLGB2LTSY --GB | | Y | Y | | system will set the value once sender bic added, allow user to update - 2-characters | |
| Field 53 BIC | this is used to customiz 53 BIC for following scenarios, if no static added, system will pick 53 BIC from nostro static Scenario 1: - Settlement means = Over-Account - Swift message type in (MT202 direct/MT103) Scenario 2: - Swift message type in (MT202 direct/ MT202 COV/MT103) - cashflow ccy match the field 53 CCY - settlement means = NOS | | N | Y | this is used to customiz 53 BIC for following scenarios, if no static added, system will pick 53 BIC from nostro static Scenario 1: - Settlement means = Over-Account - Swift message type in (MT202 direct/MT103) Scenario 2: - Swift message type in (MT202 direct/ MT202 COV/MT103) - cashflow ccy match the field 53 CCY - settlement means = NOS | - Field 53 BIC must be 8 or 11 characters - Only one Field 53 currency can be added for each FMID. | |
| Field 53 CCY | | N | Y |
| Field 58 BIC | customize 58 BIC for MT202Flip, if no static added, system will get error to generate MT202Flip | | N | Y | warning: the field is mandatory for MT202Flip | 8 or 11 characters | |
| Accounting | N if accounting is required | Currency | the relative parameter are set to the CCY, default to ALL, allow user to change | | Y | Y | TBC how to display: Settlement Accounting will be suppressed at backend for these currencies and entities | 3-characters | |
| EBBS Bridge Account | The EBBS bridge account number used to route or temporarily bridge postings between EBBS and internal accounting/settlement flows. | | Y | Y | | | |
| Posting Branch | The branch where the transaction is posted in the accounting system share sample to Dinesh to confirm the description. | | Y | Y | the equivalent in EBBS to understand what branch this is being posted for | | |
| Txn Type Code | The transaction type code identifies the source of the accounting entry. Default to RTN for RATAN | | Y | N | Default value is set as 'RTN' indicate RATAN. In some countries where RTN is used to indicate other applications, it is set as 'RTO' (example: Nepal) | RTN | |
| Dr Txn Code | Debit transaction code used to determine accounting treatment for the debit leg. | | Y | Y | identify whether it's a debit or credit. The code may differ between branches | | |
| Cr Txn Code | Credit transaction code used to determine accounting treatment for the credit leg. | | Y | Y | | |
| Country Code | should this reuse the one from Swift? No | | Y | Y | | | |
| ZoneId | defines the time to execute EOD job to trigger batch job, dropdown for user to select check if possible to use the format: - GMT+8 - GMT-8 | | Y | Y | | | |
| Nostro Static | | | | | | | | | |

**EXPAND: History info**

- #### Currency Mapping (including rounding static and iso ccy mapping ) - | Currency | Precision | Type | ISO Currency | | --- | --- | --- | --- | | CNS | 0 | ROUNDING_OFF | CNY | | CNH | 0 | ROUNDING_OFF | CNY | | CNO | 0 | ROUNDING_OFF | CNY | | CNY | 0 | ROUNDING_OFF | |
- #### Onboarding Dashboard - (Drilldown from "New Entity Onboarding" from home page) - | Booking Entity FMID | Booking Entity FMCODE | Status | Missing Static | | --- | --- | --- | --- | | | | | format to be confirmed | - ##### Branch Code - no FMCODE value for historical values - | Booking Entity FMID | Booking Entity FMCODE | Branch Code | | --- | --- | --- | | | | | - ##### Nostro Static - existing Blotter, link to new entity onboarding - need to enable bulk upload function - ##### Swift Generation: - | Booking Entity FMID | Booking Entity FMCODE | Country Code | Sender BIC | Field 53 BIC | Field 53 CCY | Field 58 BIC | | --- | --- | --- | --- | --- | --- | --- | | | | | | | | | - ##### Release Time - | Booking Entity FMID | Booking Entity FMCODE | Currency | cutoff time (GMT) | cutoff shifter | cutoff shifter unit | | --- | --- | --- | --- | --- | --- | | | | | | -2/-1/0 | BUSINESS DAY | - ##### Accounting Static - no country full name for historical values - | Booking Entity FMID | Booking Entity FMCODE | EBBS Bridge Account | Currency (add i icon) | Posting Branch | Txn Type Code | Dr Txn Code | Cr Txn Code | Country Code | ZoneId () | | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | | | | | ALL default to ALL, allow user to set to other ISO ccy | 055 | RTN | 478 | 378 | BH | Asia/Bahrain |

**EXPAND_END**

- **EXPAND: Below items are not mandatory for new entity onboarding, keep in backend for now** - | ~~PM CCY~~ | ~~PM CCY Receiver BIC~~ | | --- | --- | | | | - ~~UDF_Strategy ~~- | k_strategy | v_allocation | v_available_location | | --- | --- | --- | | COM_BOE_DELIV | ALLOC | BOE | | COM_CHAS_LDN | | LONDON | - ~~UDF_SWF_LS~~ - not mandatory for new entity onboarding, keep in backend for now | k_currency | v_allocation | v_available_location | v_quality | v_type | v_unit | | --- | --- | --- | --- | --- | --- | | XAG | UNALL | LONDON | 9990 | SILV | GOZ | | XAQ | UNALL | LONDON | | GOLD | FOZ | - CFI Code Mapping - MX bifurcation logic: is maintained in code level, not in this change scope **EXPAND_END**

# Link

[Self Service new branch/entity onboarding Design - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3556617786)

# UI Changes

- Separate Static Blotter

| | Blotter | Mock UI |
| --- | --- | --- |
| 1 | Tile | ![image-2026-7-3_17-21-37.png](attachments/image-2026-7-3_17-21-37.png) |
| 2 | Onboarding Dashboard | Option1![image-2026-7-10_17-25-0.png](attachments/image-2026-7-10_17-25-0.png) VS Option2 ![image-2026-7-10_17-25-19.png](attachments/image-2026-7-10_17-25-19.png) |
| 3 | Branch Code | ![image-2026-7-10_17-28-46.png](attachments/image-2026-7-10_17-28-46.png) |
| 4 | Release Time | ![image-2026-7-10_17-25-57.png](attachments/image-2026-7-10_17-25-57.png) |
| 5 | Currency Mapping | ![image-2026-7-10_17-27-23.png](attachments/image-2026-7-10_17-27-23.png) |
| 6 | Settlement Accounting | ![image-2026-7-10_17-27-48.png](attachments/image-2026-7-10_17-27-48.png) |
| 7 | Swift Static | ![image-2026-7-2_17-36-12.png](attachments/image-2026-7-2_17-36-12.png) |
| 8 | Bulk Upload Function | ![image-2026-7-2_17-36-34.png](attachments/image-2026-7-2_17-36-34.png) ![image-2026-7-2_17-36-52.png](attachments/image-2026-7-2_17-36-52.png) ![image-2026-7-2_17-37-6.png](attachments/image-2026-7-2_17-37-6.png) ![image-2026-7-2_17-37-31.png](attachments/image-2026-7-2_17-37-31.png) ![image-2026-7-2_17-37-48.png](attachments/image-2026-7-2_17-37-48.png) |