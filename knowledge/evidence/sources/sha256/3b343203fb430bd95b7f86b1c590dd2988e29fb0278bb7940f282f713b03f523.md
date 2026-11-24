# Version History

| Version | Date | Description | Reference |
| --- | --- | --- | --- |
| 1.0 | 2026-09-10 | Version 1 is finalized and ready for development | |
| 1.1 | 2026-09-22 | HAU should follow the Hong Kong weekend and holiday calendar, and the solution should support calendar mapping for non-ISO currencies. | |
| 1.2 | 2026-09-24 | add requirement to customize tag20 in MT692 | |
| 1.3 | 2026-09-29 | add requirement to map non-ISO ccy to ISO ccy in DVP field 72 | |
| 1.4 | 2026-09-30 | add requirement to populate field 11S of MT692 with last update time of original new message | |
| 1.5 | | | |

# Background

SCB HK will become a Gold Clearing Agent as part of HKCS (HK Commodity Settlement) imitative, deal will be booked in SCB HK and gold will be booked as ‘HAU’ instead of ‘XAU’.

# ADO

[https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14724643](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14724643)

# Requirement Details

1. Deal will be booked in SCB HK books (FMID =2)
2. Product Scope：FX
3. Gold will be booked as ‘HAU’ instead of ‘XAU’. The counter ccy cashflow need to be suppressed from RATAN.
4. Customize the Swift message for MT604 / MT605 1. Receiver of SWIFT should be **BKCHHKHHGSI **BIC code 2. field 26C：Update the mapping in RATAN to capture field 26C for HAU equivalent ![image-2026-9-1_11-53-34.png](attachments/image-2026-9-1_11-53-34.png) 3. field 23：set as TRANSFER in RATAN 4. field 32F： 1. Input “FOZ” + quantity of commodity to be transferred; 2. A maximum of 3 decimal places is supported 5. Field 87A/88a are mandatory for HKCS payment | | | MT604 | MT605 | | --- | --- | --- | --- | | 87A | Input the BIC of the receiving DP | Input the BIC of the paying DP | | 88 | A | If commodity account number is NOT provided: Line 1: Input the BIC of the beneficiary of the commodity (Confirmed with Vivek, Weng Hien, need to map to the entity sender bic static, for HK, this will always be SCBLHKHHXXX) If commodity account number is provided: Line 1: Input “/” + the commodity account number of the beneficiary of the commodity Line 2: Input the BIC of the beneficiary of the commodity | As confirmed With Weng Hien and Vivek, need to map to the entity sender BIC static, Line 1: Sender BIC (SCBLHKHHXXX) | | D 2026-09-18confirmed with Vivek that this scenario won't happen in BAU | Line 1: Must input “/” + the account number of the beneficiary | | All other information in this field will be ignored by HKCS | For SCT: All other information in this field will be ignored by HKCS For DVP: Name and address must be provided | 6. Field 72: - for SCT (single credit transfer), – non PVP cashflow - :[72:/ACC/SCRTRF](http://72/ACC/SCRTRF) - append other values from SSI+ from line 2 with // - for PVP cashflow - identify PVP cashflow: - Murex cashflow: Murex_product_strategy ='PVP' - Stella cashflow: settlement method ='PVP' - Line 1: Input “/ACC/DVPTRF” - Line 2: Input “/OCMT/” + settlement currency + settlement amount + “/” where - settlement currency: - HKD, USD, EUR or CNY - need to map the cashflow ccy to ISO ccy if it's not. - the currency of the other leg linked to current HAU cashflow. The condition to query the other cashflow: - Murex cashflow: trade id + VD - Stella cashflow: trade id + major version + VD - if failed to get the other cashflow or get multiple cashflow matched, what's the expectation？- Ratan swift generation error, user can reinstate to regenerate. - settlement amount: 15d (i.e. a maximum of 13 digits without leading zero plus 2 decimal points while “,” should be used as decimal separator and no thousand separators is allowed) - append other values from SSI+ from line 3 with // - ~~For MT605, if the cash account of the creditor is known, ~~– Confirmed with Vivek, this can be ignored - ~~Line 3 (optional): Input “/ACCT/” + creditor’s cash account~~ - Sample： Line 1: 72:/ACC/DVPTRF Line 2: /OCMT/USD36675000,00/
5. Customize the Swift message for MT692 1. Field 20: "CANC"+{cashflow Id} 2. Date from 11S: input the last update time of original new message from RATAN instead of event date of withdrawal event
6. **EXPAND: Sample Swift** ![image-2026-9-22_17-48-25.png](attachments/image-2026-9-22_17-48-25.png) **EXPAND_END**
7. Swift Exception Handling: 1. if mandatory field info missed, cashflow will remain in READY status with swift generation error, user can reinstate to input the mandatory info and regenerate the swift. 2. if failed to get the other leg or get multiple cashflow matched for DVP case, cashflow will remain in READY status with swift generation error, user can reinstate to regenerate. 3. if unexpected issue blocked the swift generation, Ops will contact CTMU to process.
8. HAU release cut off: VD-1 10:00(GMT)
9. Settlement Accounting – Ratan will <u>**not **</u>send accounting, CIS will query the data from RATAN API
10. Nostro: Separate HAU MAIN Nostro to be setup with BKCHCHKHHGSI as the Nostro Agent
11. SSI Stamping – Vostros are expected to be setup as HAU MAIN
12. For Approval limits, use the same as XAU - Upstream has set FX rate for XAU/USD, no change required in RATAN
13. Upstream & Downstream 1. Conversion Rate in MDS 2. Weekend/Holiday – RDM (Non ISO ccy holiday → ISO ccy holiday) 1. new ccy mapping logic to be added for non-ISO ccy : for HAU cashflow, need to apply HKD weekend/holiday to calculate release cutoff/netting time 3. HAU to be sent in RATAN to CIS feed - CIS query RATANAPI instead of Ratan sending data, no change required in RATAN 4. HAU message need to be sent to LMS

# Impact to other existing RATAN functions:

[Auto Populate Ordering Info for Notice to Receive Cashflow - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Auto+Populate+Ordering+Info+for+Notice+to+Receive+Cashflow)

[SCB Receive Cashflow Stamping - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/SCB+Receive+Cashflow+Stamping)

[FMRP Swift Generation - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/FMRP+Swift+Generation)

# Open Question

| | Description | Comment | Reference doc/mail | Status |
| --- | --- | --- | --- | --- |
| 1 | accounting required to EBBS or not? | 2026-07-03 Confirmed accounting for HAU is not required in RATAN | 📎 [RE_ HONG KONG Physical Gold Settlement initiative---Requirement Discussion from Ratan to EBBS.msg](attachments/RE_ HONG KONG Physical Gold Settlement initiative---Requirement Discussion from Ratan to EBBS.msg) | |
| 2 | HAU holiday static from RDM? | Vivian will confirm | | |
| 3 | HAU currency cutoff data - copy from existing XAU data? | Carrie will extract existing XAU release cut off to Vivian and Vivek to confirm | ![image-2026-10-9_15-58-39.png](attachments/image-2026-10-9_15-58-39.png) | |
| 4 | do we need to add ISO ccy mapping to map HAU to XAU? (currently no accounting required for HAU, and ccy field is not used in precious metal related swift) | not required. | | |
| 5 | Rounding logic for HAU? copy from existing XAU data? | 3 decimals, rounding off | | |
| 6 | nostro static? | | | |
| 7 | Message need to send to LMS? (the ccy will be HAU) | 2026-07-24 Vivian will confirm 2026-07-29 LMS team confirmed HAU cashflow need to be send to LMS, mail attached | 📎 [RE_ Hong Kong Commodity Settlement Initiative -- LMS.msg](attachments/RE_ Hong Kong Commodity Settlement Initiative -- LMS.msg) | |
| 8 | Field 23 in swift: current logic will set 23 to TRANSFER is F26 is UNALL | Vivek confirmed OK to set 23 as TRANSFER | | |
| 9 | For MT605, if the cash account of the creditor is known, Line 3 (optional): Input “/ACCT/” + creditor’s cash account | 2026-09-03 Vivek confirmed this can be ignored | 📎 [RE_ HKCS Requiement Clarification - RATAN.msg](attachments/RE_ HKCS Requiement Clarification - RATAN.msg) | |
| 10 | DVP indicator | 2026-09-07 Deepak and Dinesh confirmed to cashflow hit DVP NSTP rule are treated as DVP cashflow scope | 📎 [RE_ Open Question for Day2_ME requirements.msg](attachments/RE_ Open Question for Day2_ME requirements.msg) | |