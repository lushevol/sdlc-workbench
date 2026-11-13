# Background

Manual entities send to Ratan from Murex 2.11 last year ,but cashflow suppressed in Ratan ,now we are going to enabling settlement the manual entities in Ratan to avoid manual payment.

# ADO

[Story 11759091 [Enabling Settlement for Manual Entities] BAHRAIN-BAHRAIN](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/11759091/)

[Story 12529837 [Enabling Settlement for Manual Entities] QATAR-DOHA](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/12529837/)

[Story 12529867 [Enabling Settlement for Manual Entities] QATAR-SLATE_QFC](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/12529867/)

[Story 12529900 [Enabling Settlement for Manual Entities] KENYA-KENYA](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/12529900/)

[Story 12529902 [Enabling Settlement for Manual Entities] ZAMBIA-ZAMBIA](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/12529902/)

[Story 12529903 [Enabling Settlement for Manual Entities] UGANDA-UGANDA](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/12529903/)

[Story 12529904 [Enabling Settlement for Manual Entities] TANZANIA-TANZANIA](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/12529904/)

[Story 12529905 [Enabling Settlement for Manual Entities] GHANA-GHANA](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/12529905/)

[Story 12529907 [Enabling Settlement for Manual Entities] NIGERIA-NIGERIA](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/12529907/)

[Story 12529910 [Enabling Settlement for Manual Entities] SRI LANKA-SRI LANKA](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/12529910/)

[Story 12529912 [Enabling Settlement for Manual Entities] SRI LANKA-FCBUSLANKA](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/12529912/)

[Story 12529914 [Enabling Settlement for Manual Entities] VIETNAM-HANOI](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/12529914/)

[Story 12529916 [Enabling Settlement for Manual Entities] PAKISTAN-KARACHI](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/12529916/)

[Story 12529918 [Enabling Settlement for Manual Entities] BANGLADESH-DHAKA](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/12529918/)

# Scope

| | Country | MX2.11 Entity | FMID | FMCODE | User | Comment |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | BAHRAIN | BAHRAIN | 10036430 | SCB BAHRAI*MAN | David/Gomathy/Joseph, Synthia | |
| 2 | ~~BOTSWANA~~ | ~~BOTSWANA~~ | ~~10036775~~ | ~~SCB BOTSWAN*GBE~~ | ~~Joseph, Synthia~~ | 2026-02-11 Confirmed with Dinesh , drop Botswana & replace it with Qatar,Since SCB is closing down Botswana branch |
| 3 | Qatar | DOHA | 300010782 | SCB DOHA*DOH | Gomathy/Joseph, Synthia | 2026-02-11 New added instead of BOTSWANA |
| 4 | SLATE_QFC | 401081696 | SLATE ONE LLC*DOH | Gomathy/Joseph, Synthia |
| 5 | KENYA | KENYA | 300011525 | SCB KENYA B*NBO | Gomathy/Joseph, Synthia | |
| 6 | ZAMBIA | ZAMBIA | 10041903 | SCB ZAMBIA*LUS | Gomathy/Joseph, Synthia | |
| 7 | UGANDA | UGANDA | 10041902 | SCB UGANDA*KAM | Gomathy/Joseph, Synthia | |
| 8 | TANZANIA | TANZANIA | 10040387 | SCB TANZANI*DAR | Mahela, Simon Godfrey; Dahal, Leyla(In country) | |
| 9 | GHANA | GHANA | 10037477 | SCB GHANA*ACC | Gomathy/Joseph, Synthia | |
| 10 | NIGERIA | NIGERIA | 300084297 | SCB NIGERIA*LAG | David/Gomathy/Joseph, Synthia | |
| 11 | SRI LANKA | SRI LANKA | 10036647 | SCB COLOMBO*CMB | Wellage, Samanthi ; Fonseka, Shalini | |
| 12 | FCBUSLANKA | 10022098 | SCB COL FCB*CMB | Wellage, Samanthi ; Fonseka, Shalini | |
| 13 | Vietnam | HANOI | 10041530 | SCB HANOI*HNI | David | |
| 14 | Pakistan | KARACHI | 10036655 | SCB KARACHI*KHI | David + FMOPS_Pakistan(In Country) FMOPS_Pakistan(In Country): Sattar, Adil /Ali, Shaukat/Zaidi, Hadi | |
| 15 | Bangladesh | DHAKA | 300011470 | SCB DHAKA*DAC | Morshed, Golam; Niloy, Nehabul Haque(In Country) | |

# Static Details

## Nostro Static Data

| | Country | MX2.11 Entity | FMID | FMCODE | Nostro Static | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Bahrain | BAHRAIN | 10036430 | SCB BAHRAI*MAN | 📎 [Nostro Static Data0729.xlsx](attachments/Nostro Static Data0729.xlsx) | 2026-05-15 Offline confirmed with Synthia ,BH NOS+USD MAIN ,“senders_correspondent53_swift” is SCBLUS33XXX 2026-05-13 Confirmed by user about the open point ,waiting for final confirmation 2026-05-08 Synthia confirmed the unclear records,but still have open points ,waiting user to feedback 2026-04-27 Have call with user to discuss the open points,need user to check and come back 2026-04-17 After send the signoff to user ,user feedback some open pionts ,I found some duplicated records need to double confrim with user 2026-03-24 3/24/2026：Review the duplicate records with Synthia and Sumita ,delete Sumita records 2026-03-17 update notice to receive ,duplicated records need to confirm with user 2026-02-26 |
| 2 | QATAR | DOHA | 300010782 | SCB DOHA*DOH | 2026-06-23 Sumita requested to add new nostro static data for QA-USD 2026-05-08 Synthia confirmed the unclear records 2026-04-27 Have call with user to discuss the open points,need user to check and come back 2026-04-17 After send the signoff to user ,user feedback some unclear record ,need to recheck. 2026-04-03 Synthia confirmed the nostro static ,Grace summarized 2026-04-02 Grace did the mapping and get notice to receive from Yashas's excel and send email to user to double confirm 2026-04-01 Synthia provided nostro static from Razor 2026-03-24 Synthia help to review the nostro static 2026-03-17 Summarized the static ,need user to double confirm |
| 3 | SLATE_QFC | 401081696 | SLATE ONE LLC*DOH | 2026-03-23 Confirmed with Synthia ,SLATE cashflow will be cashflow suppressed ,then rest of static is not required. Only Cashflow Suppression static is required. 2026-03-18 Dinesh feedback : 2026-03-18 Synthia mentioned that SLATE will be suppressed in Ratan ,so need to double confirm if cashflow suppressed ,if yes ,then no need to setup the static for this entity 2026-03-17 not provided by user |
| 4 | Kenya | KENYA | 300011525 | SCB KENYA B*NBO | 2026-05-08 Synthia confirmed the unclear records 2026-04-27 Have call with user to discuss the open points,need user to check and come back 2026-04-17 After send the signoff to user ,user feedback some unclear record ,need to recheck. 2026-03-17 Updated the notice to receive based on Yashas's excel |
| 5 | Zambia | ZAMBIA | 10041903 | SCB ZAMBIA*LUS | 2026-08-17Deepak requested to update ZM -ZMW Main :senders_correspondent53_account from 0011203060069 to 0160398000003,dev update on UAT(but not reflected on the excel) ,production need ops user to update 📎 [RE ZM SCPAY -AC03-InvalidDebitAccountNumber-ZM5FI2608110000L--SCBLZMLXFMO-Haowen.msg](attachments/RE ZM SCPAY -AC03-InvalidDebitAccountNumber-ZM5FI2608110000L--SCBLZMLXFMO-Haowen.msg) 📎 [RE ZM SCPAY -AC03-InvalidDebitAccountNumber-ZM5FI2608110000L--SCBLZMLXFMO-Nick.msg](attachments/RE ZM SCPAY -AC03-InvalidDebitAccountNumber-ZM5FI2608110000L--SCBLZMLXFMO-Nick.msg) 2026-06-25 Gomathy requested to add new nostro static for USD MAIN 2026-04-17 Provide signoff for static data 2026-03-17 Updated the notice to receive based on Yashas's excel |
| 6 | Uganda | UGANDA | 10041902 | SCB UGANDA*KAM | 2026-04-17 Provide signoff for static data 2026-03-17 Updated the notice to receive based on Yashas's excel |
| 7 | Tanzania | TANZANIA | 10040387 | SCB TANZANI*DAR | 2026-07-12 Deepak confirmed the DFCC nostro static 2026-05-12 DFCC need to add new nostro static data ,waiting for user feedback 2026-04-15 Provide signoff for static data 2026-03-20 Confirmed with Simon .update senders_correspondent53_account from 166599257800 to 0166599257800 2026-03-17 Updated the notice to receive based on Yashas's excel,concerns on one record,need to confirm with user |
| 8 | Ghana | GHANA | 10037477 | SCB GHANA*ACC | 2026-05-08 Synthia confirmed the unclear records 2026-04-27 Have call with user to discuss the open points,need user to check and come back 2026-04-17 After send the signoff to user ,user feedback some unclear record ,need to recheck. 2026-03-17 Updated the notice to receive based on Yashas's excel |
| 9 | Nigeria | NIGERIA | 300084297 | SCB NIGERIA*LAG | 2026-07-29 Deepak and Gomathy requested to add two NGB nostro static 2026-05-08 Synthia confirmed the unclear records 2026-04-27 Have call with user to discuss the open points,need user to check and come back 2026-04-17 After send the signoff to user ,user feedback some unclear record ,need to recheck. 2026-03-24 Review the duplicate records with Synthia and Sumita ,delete Sumita records 2026-03-17 notice to receive,duplicated records need to confirm with user |
| 10 | Sri Lanka | SRI LANKA | 10036647 | SCB COLOMBO*CMB | 2026-06-11 Confirmed with Deepak and Dinesh, need to add two new nostro static data for LKO, replicated the nostro from LKR ,update the ccy to LKO and LKO in settlement as well 2026-05-13 Shalini provided the final signoff of nostro static data 2026-05-12 confirmed with Shalini ,need to remove one nostro static data ,waiting for final confrimation 2026-04-10 Provide signoff for static data |
| FCBUSLANKA | 10022098 | SCB COL FCB*CMB | 2026-04-10 Provide signoff for static data |
| 11 | Vietnam | HANOI | 10041530 | SCB HANOI*HNI | 2026-07-13 Requested by Sumita ,update NOX to NOS 2026-06-17 Sumita requested to add two new nostro static data of VNO for VN 2026-06-16 Sumita requested to amend F53 of all No 2 Account (regardless of currency) to 09000680007 for Nostro of VN 2026-03-26 Provide signoff for static data 2026-03-04 Comment from Dinesh Hi Yash, For other markets we carried over the Nostro static from Murex, but since we don’t have that as a reference point, we can setup only USD and VND aligned to BAU process. 2026-03-04 Comment from Yashas: Sumita has confirmed that Vietnam operations currently settle only in USD and VND, with nostro account requests limited to these two currencies. However, our Razor system configuration includes nostro setups for all currencies. We require guidance on whether to: 1. Align with current operational practice by maintaining only USD and VND currency configurations, or 2. Retain the comprehensive multi-currency setup currently in place |
| 12 | Pakistan | KARACHI | 10036655 | SCB KARACHI*KHI | 2026-04-30 Provide signoff for static data 2026-04-20 Shaukat confirm the blank senders_correspondent53_account to be set as '09961118070 2026-04-07 User mentioned to remove the NOX nostro static ,already remove and send user to review 2026-03-31 Aligned with Shaukat and Sumita ,and summary the nostro static ,send user to double confirm 2026-03-17 More records in Yashas excel than Sumita's some value are different,confirm with user |
| 13 | Bangladesh | DHAKA | 300011470 | SCB DHAKA*DAC | 2026-06-11 Confirmed with Deepak,add new nostro static data for BDO ,just replicated the BDT nostro sttaic data and change the ccy from BDT to BDO 2026-05-14 Got signoff from Golam except swift static data 2026-05-08 Send signoff email ,waiting for signoff 2026-04-07 Golam confirmed should be INR and INR MAIN Have call with Golam ,will double confirm the INR nostro static 2026-03-30 1.Confirmed with Deepak and Golam ,Notice to Receive is set to ‘N’ for BDT ccy,please kindly refer to attached 2.Golam will help to check the nostro static for INO record,not sure if it should be INO or INR 2026-03-17 one record missing Notice to receive,waiting user to confirm |

## Swift Static Data

| | Country | MX2.11 Entity | FMID | FMCODE | Branch Code | Swift static data | Comment | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Bahrain | BAHRAIN | 10036430 | SCB BAHRAI*MAN | 55 | 📎 [Swift Static data2026-07-21.xlsx](attachments/Swift Static data2026-07-21.xlsx) 2026-06-26 Confirmed by Deeapk ,update all the Field 53 CCY in the excel | 2026-02-23Update 53BIC and 58BIC from SCBLBHBMAXXX to SCBLBHBMGMO 2026-01-28 Provided by @Cordelia Sumita K Thirunavukarasu | |
| 2 | QATAR | DOHA | 300010782 | SCB DOHA*DOH | QA | 2026-03-24 Confirmed with Deepak and Synthia ,QA is used for branch code 2026-03-05 Synthia suggested to use QA ,need Yashas and Deepak to check with downstream teams 2026-03-03 Synthia help to confirm the branch code,Grace help to check if charator can be used for branch code 2026-02-23do the mapping with user and PO, need user to confirm the branch code | |
| 3 | SLATE_QFC | 401081696 | SLATE ONE LLC*DOH | QA | 2026-03-23 Confirmed with Synthia ,SLATE cashflow will be cashflow suppressed ,then rest of static is not required. Only Cashflow Suppression rule is required. 2026-03-05 Synthia suggested to use QA ,need Yashas and Deepak to check with downstream teams2026-03-03 Synthia help to confirm the branch code,Grace help to check if charator can be used for branch code 2026-02-23 do the mapping with user and PO, need user to confirm the branch code | |
| 4 | Kenya | KENYA | 300011525 | SCB KENYA B*NBO | 39 | 2026-02-23 aligned with Dinesh and Synthia during the call | |
| 5 | Zambia | ZAMBIA | 10041903 | SCB ZAMBIA*LUS | 52 | 2026-02-23 aligned with Dinesh and Synthia during the call | |
| 6 | Uganda | UGANDA | 10041902 | SCB UGANDA*KAM | UG | 2026-03-24 Confirmed with Deepak and Synthia ,UG is used for branch code 2026-03-05 Synthia suggested to use UG,need Yashas and Deepak to check with downstream teams 2026-03-03 Synthia help to confirm the branch code,Grace help to check if charator can be used for branch code 2026-02-23 aligned with Dinesh and Synthia during the call | |
| 7 | Tanzania | TANZANIA | 10040387 | SCB TANZANI*DAR | 50 | 2026-03-20 Confirmed with Deepak ,no need to update swift static data 2026-03-04 Aligned the swift static data with Deepak and Simon .Simon help to check with Razor PSS and get a nostro main MT202 sample,then decide if need to update the swift static data | |
| 8 | Ghana | GHANA | 10037477 | SCB GHANA*ACC | 35 | 2026-02-23 aligned with Dinesh and Synthia during the call | |
| 9 | Nigeria | NIGERIA | 300084297 | SCB NIGERIA*LAG | 82 | 2026-01-28Provided by @Cordelia Sumita K Thirunavukarasu | |
| 10 | Sri Lanka | SRI LANKA | 10036647 | SCB COLOMBO*CMB | 84 | 2026-02-27 confirmed with Dinesh Copy Sender BIC to 53BIC and 58BIC for SRI LANKA | |
| FCBUSLANKA | 10022098 | SCB COL FCB*CMB | 85 | 2026-07-21 confirmed by Deepak, no need to setup Field 53ccy for this entity in swift static data 2026-07-10 For 10022098,waiting confirmation from Deepak 2026-02-27 confirmed with Dinesh Copy Sender BIC to 53BIC and 58BIC for SRI LANKA | |
| 11 | Vietnam | HANOI | 10041530 | SCB HANOI*HNI | 29 | 2026-01-28 Provided by @Cordelia Sumita K Thirunavukarasu | |
| 12 | Pakistan | KARACHI | 10036655 | SCB KARACHI*KHI | 97 | 2026-03-03 Confirmed the swift static data with Pakistan in country team and PO 2026-02-26 In country team help to provided some samples then decided if need to be added 2026-01-28 Provided by @Cordelia Sumita K Thirunavukarasu | |
| 13 | Bangladesh | DHAKA | 300011470 | SCB DHAKA*DAC | 86 | 2026-05-22 Confirmed with Deepak ,setup 58 BIC the same with 53BIC first because 58BIC can’t be empty 2026-05-14 Golam provided the signoff except swift static data 2026-05-08 Send signoff email ,waiting for signoff exclude swift static data 2026-05-07 pending on user provide swift sample then can finalize the swift static data 2026-03-30 Golam provided some swift message samples 2026-03-04 Golam help to provide some swift message samples ,then summaried the swift static data together | |

## ![](https://confluence.global.standardchartered.com/download/attachments/3244588508/image-2025-5-21_16-34-44.png?version=1&modificationDate=1747816484000&api=v2)

## Branch Code

| Branch code | FMID |
| --- | --- |
| 55 | 10036430 |
| 29 | 10041530 |
| 82 | 300084297 |
| 97 | 10036655 |
| 35 | 10037477 |
| UG | 10041902 |
| 52 | 10041903 |
| 39 | 300011525 |
| QA | 300010782 |
| 84 | 10036647 |
| 85 | 10022098 |
| 50 | 10040387 |
| 86 | 300011470 |

## Release CutOff

| | Country | MX2.11 Entity | FMID | FMCODE | cut_off_time | cut_off_shifter | Comment | Release Cutoff Excel | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Bahrain | BAHRAIN | 10036430 | SCB BAHRAI*MAN | 15:00 UTC | VD-1BD | 2026-01-20 Confirmed by @Cordelia Sumita K Thirunavukarasu @David George Thomas will follow London(10075222) ccy | 📎 [Release Cutoff.xlsx](attachments/Release Cutoff.xlsx) | |
| 2 | QATAR | DOHA | 300010782 | SCB DOHA*DOH | | | 2026-03-25 Confirmed with Deepak ,will use the Currency /Shifter/Time/Timezone from Razor ,but not use the blank ccy,For the blank ccy ,will follow Ratan logic. In Ratan , if release cut off time for any entity + ccy not configured ,then our system will set the release cutoff to a default time which is VD-1business day 18:00 GMT 📎 [Details on Enabling settlement for manual_Entities-Release cutoff.xlsx](attachments/Details on Enabling settlement for manual_Entities-Release cutoff.xlsx) 2026-03-20 Deepak help to check which column to be used 2026-03-05 Synthia provided release cutoff provided by Razor 2026-03-03 Synthia will help to confirm | |
| 3 | SLATE_QFC | 401081696 | SLATE ONE LLC*DOH | NA | NA | 2026-03-23 Confirmed with Synthia ,SLATE cashflow will be cashflow suppressed ,then rest of static is not required. Only Cashflow Suppression static is required. 2026-03-03 Synthia will help to confirm | |
| 4 | Kenya | KENYA | 300011525 | SCB KENYA B*NBO | 15:00 UTC | VD-1BD | 2026-01-26 Confirmed by @Joseph, Synthia follow the same with BAHRAIN will follow London(10075222) ccy | |
| 5 | Zambia | ZAMBIA | 10041903 | SCB ZAMBIA*LUS | 15:00 UTC | VD-1BD | 2026-01-26 Confirmed by @Joseph, Synthia follow the same with BAHRAIN will follow London(10075222) ccy | |
| 6 | Uganda | UGANDA | 10041902 | SCB UGANDA*KAM | 15:00 UTC | VD-1BD | 2026-01-26 Confirmed by @Joseph, Synthia follow the same with BAHRAIN will follow London(10075222) ccy | |
| 7 | Tanzania | TANZANIA | 10040387 | SCB TANZANI*DAR | | | 2026-03-26 Confirmed with Deepak ,will use the Currency /Shifter/Time/Timezone from Razor ,but not use the blank ccy,For the blank ccy ,will follow Ratan logic. In Ratan , if release cut off time for any entity + ccy not configured ,then our system will set the release cutoff to a default time which is VD-1business day 18:00 GMT 📎 [MX.ALL.RelDate.csv](attachments/MX.ALL.RelDate.csv) 2026-03-20 Deepak help to check which column to be used 2026-03-04 Confirmed with Simon and Deepak ,copy the below four column and setup in Ratan(CURR/SHIFTER/TIME/TIMEZONE).pls refer to attached MX.ALL.RelDate.csv In Ratan ,if release cut off time for any entity+ccy not configured ,then our system will set the release cutoff to a default time which is VD-1business day 18:00 GMT 2026-02-03 Simon provided release cutoff (retrieved from Razor PSS) 2026-01-27 Mahela, Simon Godfrey help to check from Razor then feedback | |
| 8 | Ghana | GHANA | 10037477 | SCB GHANA*ACC | 15:00 UTC | VD-1BD | 2026-01-26 Confirmed by @Joseph, Synthia follow the same with BAHRAIN will follow London(10075222) ccy | |
| 9 | Nigeria | NIGERIA | 300084297 | SCB NIGERIA*LAG | 17:00 UTC | VD-1BD | 2026-01-20 Confirmed by @Cordelia Sumita K Thirunavukarasu @David George Thomas will follow London(10075222) ccy | |
| 10 | Sri Lanka | SRI LANKA | 10036647 | SCB COLOMBO*CMB | 13:00 UTC | VD-1BD | 2026-02-26 Confirmed with Shalini and Dinesh ,release cutoff should be 13:00 UTC VD-1BD,will follow London(10075222) ccy can ignore the release cutoff excel from Razor 2026-02-12 Shalini provided release cutoff 2026-01-26 Wellage, Samanthi ; Fonseka, Shalini help to provide | |
| FCBUSLANKA | 10022098 | SCB COL FCB*CMB | 13:00 UTC | VD-1BD | 2026-02-26 Confirmed with Shalini and Dinesh ,release cutoff should be 13:00 UTC VD-1BD,will follow London(10075222) ccy can ignore the release cutoff excel from Razor 2026-02-12Shalini provided release cutoff 2026-01-26 Wellage, Samanthi ; Fonseka, Shalini help to provide | |
| 11 | Vietnam | HANOI | 10041530 | SCB HANOI*HNI | 11:00 UTC | VD-1BD | 2026-01-20 Confirmed by @Cordelia Sumita K Thirunavukarasu @David George Thomas ,will follow London(10075222) ccy | |
| 12 | Pakistan | KARACHI | 10036655 | SCB KARACHI*KHI | 13:00 UTC | VD-1BD | 2026-01-20 Confirmed by @Cordelia Sumita K Thirunavukarasu @David George Thomas ,will follow London(10075222) ccy | |
| 13 | Bangladesh | DHAKA | 300011470 | SCB DHAKA*DAC | | | 2026-05-14 Got signoff from Golam except swift static data 2026-05-08 Send signoff email ,waiting for signoff exclude swift static data 2026-04-07 Confirmed with Deepak ,will use the Currency /Shifter/Time/Timezone from Razor ,but not use the blank ccy,For the blank ccy ,will follow Ratan logic. In Ratan , if release cut off time for any entity + ccy not configured ,then our system will set the release cutoff to a default time which is VD-1business day 18:00 GMT 📎 [release cutoff configuration for Bangladesh(FMID 300011470 FMCODE SCB DHAKA DAC)in Razor.xls](attachments/release cutoff configuration for Bangladesh(FMID 300011470 FMCODE SCB DHAKA DAC)in Razor.xls) 2026-03-30 | |

<details>
<summary>Expand Details</summary>

UTC Time

**EXPAND: UTC Time**

![image-2026-1-22_11-52-19-1.png](attachments/image-2026-1-22_11-52-19-1.png)

---

![image-2026-1-22_11-52-31-1.png](attachments/image-2026-1-22_11-52-31-1.png)

---

![image-2026-1-22_11-52-51-1.png](attachments/image-2026-1-22_11-52-51-1.png)

---

![image-2026-1-22_11-53-47-1.png](attachments/image-2026-1-22_11-53-47-1.png)

![image-2026-2-27_15-28-59.png](attachments/image-2026-2-27_15-28-59.png)

**EXPAND_END**

</details>

## Non-ISO to ISO Currency

NGB-NGN,PKO-PKR need to be added on Ratan side,for the others ,keep as is

| Non ISO Currency(Currency in cashflow) | ISO Currency | Comment |
| --- | --- | --- |
| **NGB** | **NGN** | 2026-03-25 NGB-NGN not exists in Ratan ,need to add this new mapping 2026-03-11 Conrirmed with Synthia ,this mapping need to added for Nigeria |
| **PKO** | **PKR** | 2026-01-20 Confirmed with @Cordelia Sumita K Thirunavukarasu For Pakistan, Non ISO to ISO mapping is PKO -PKR, doesn't exist in current mapping list, need to be added |
| VNO | VND | 2026-02-25 Confirmed with Yashas and Deepak ,this need to be setup in Ratan ,already exists 2026-01-20 For Vietnam,the Non ISO to ISO mapping is VNO-VND,we already have this mapping |
| LKO | LKR | 2026-02-25 Confirmed with Yashas and Deepak ,this need to be setup in Ratan ,already exists 2026-01-26 For Sri lanka ,the Non ISO to ISO mapping is LKO-LKR,we already have this mapping |
| BDO | BDT | 2026-01-20 Confirmed with Yashas and Deepak ,this need to be setup in Ratan ,already exists |
| NGX | NGN | 2026-03-25 Confirmed with Yashas and Deepak ,this need to be setup in Ratan ,already exists |

Below mapping is setup in Ratan

<details>
<summary>Expand Details</summary>

| Non ISO Currency(Currency in cashflow) | ISO Currency | Comment |
| --- | --- | --- |
| BRO | BRL | |
| CNO | CNY | |
| CNH | CNY | |
| EGO | EGP | |
| IDO | IDR | |
| INO | INR | |
| KRO | KRW | |
| MYO | MYR | |
| PHO | PHP | |
| RUO | RUB | |
| TWO | TWD | |
| VNO | VND | 2026-01-20 Confirmed with @Cordelia Sumita K Thirunavukarasu For Vietnam,Non ISO to ISO mapping is VNO-VND, exists in current list ,no need to be added |
| THO | THB | |
| LKO | LKR | 2026-01-26 Confirmed with Fonseka, Shalini For SRILANKA,Non ISO to ISO mapping is LKO-LKR,, exists in current list ,will check if any new to be added |
| THN | THB | |
| DOL | USD | |
| NGO | NGN | |
| XD1 | XPD | |
| XD2 | XPD | |
| XG1 | XAG | |
| XR1 | XRH | |
| XT1 | XPT | |
| XT2 | XPT | |
| XT3 | XPT | |
| AOH | AOA | |
| XU4 | XAU | |
| XU5 | XAU | |
| XD3 | XPD | |
| XG2 | XAG | |
| XU1 | XAU | |
| XU2 | XAU | |
| XU6 | XAU | |
| XU7 | XAU | |
| KEH | KES | |
| TZH | TZS | |
| XUC | XAU | |
| NGY | NGN | |
| XU8 | XAU | |
| XG3 | XAG | |
| XGC | XAG | |
| EUO | EUR | |
| JPO | JPY | |
| CNF | CNY | |
| GHH | GHS | |
| UGH | UGX | |
| SGB | SGD | |
| SGO | SGD | |
| JPB | JPY | |
| EUB | EUR | |
| NGH | NGN | |
| XUD | XUD | |
| ZMH | ZMW | |
| BDO | BDT | |
| NGX | NGN | |
| NGA | NGN | |
| IDY | IDR | |
| LKH | LKR | |
| RUW | RUB | |
| MZH | MZN | |
| PKH | PKR | |
| THS | THB | |
| MYZ | MYR | |
| INY | INR | |
| CNS | CNY | |

</details>

## Rounding Logic

2026-08-14

Deepak and Gomathy confirmed thata NGN rounding percision should be 2

📎 [RE NGN rounding precision open question.msg](attachments/RE NGN rounding precision open question.msg)

2026-08-05

Gokul requested to set up rounding off for **NGB ccy to 2 precision.**

📎 [RE ROUNDING NGB CCY PRECISION.msg](attachments/RE ROUNDING NGB CCY PRECISION.msg)

2026-04-02

~~As confirmed with Deepak and Synthia  , for NGN rounding setup in Ratan ,precison  will update from 2 to 0,and rounding type will keep as is  ROUNDING_OFF.For the others, keep as is ~~

| k_currency | v_precision | v_type | Comment |
| --- | --- | --- | --- |
| ~~NGN~~ | ~~0~~ | ~~ROUNDING_OFF~~ | 2026-08-14 Deepak and Gomathy confirmed thata NGN rounding percision should be 2 |
| NGB | 2 | ROUNDING_OFF | |

2026-03-05 Synthia mentioned that NGN settlement amount should not have any digits after decimal,need to double confirm the precision and rounding type

**EXPAND: Rounding**

| k_currency | v_precision | v_type |
| --- | --- | --- |
| **NGB** | **2** | **ROUNDING_OFF** |
| AED | 2 | ROUNDING_OFF |
| AFN | 2 | ROUNDING_OFF |
| AGH | 1 | ROUNDING_OFF |
| AGP | 2 | ROUNDING_OFF |
| AL1 | 2 | ROUNDING_OFF |
| AL3 | 1 | ROUNDING_OFF |
| ALH | 1 | ROUNDING_OFF |
| ALL | 2 | ROUNDING_OFF |
| AMD | 2 | ROUNDING_OFF |
| ANG | 2 | ROUNDING_OFF |
| AOA | 2 | ROUNDING_OFF |
| AOH | 1 | ROUNDING_OFF |
| ARS | 2 | ROUNDING_OFF |
| ASA | 2 | ROUNDING_OFF |
| ATS | 1 | ROUNDING_OFF |
| AUD | 2 | ROUNDING_OFF |
| AWG | 2 | ROUNDING_OFF |
| AYM | 2 | ROUNDING_OFF |
| AZN | 2 | ROUNDING_OFF |
| B10 | 2 | ROUNDING_OFF |
| BAM | 2 | ROUNDING_OFF |
| BBD | 2 | ROUNDING_OFF |
| BDH | 2 | ROUNDING_OFF |
| BDO | 1 | ROUNDING_OFF |
| BDT | 2 | ROUNDING_OFF |
| BEF | 2 | ROUNDING_OFF |
| BGN | 2 | ROUNDING_OFF |
| BHD | 3 | ROUNDING_OFF |
| BHO | 1 | ROUNDING_OFF |
| BIF | 0 | ROUNDING_OFF |
| BMD | 2 | ROUNDING_OFF |
| BND | 2 | ROUNDING_OFF |
| BOB | 2 | ROUNDING_OFF |
| BR1 | 2 | ROUNDING_OFF |
| BR2 | 2 | ROUNDING_OFF |
| BR3 | 2 | ROUNDING_OFF |
| BRL | 2 | ROUNDING_OFF |
| BRO | 2 | ROUNDING_OFF |
| BSD | 2 | ROUNDING_OFF |
| BSK | 2 | ROUNDING_OFF |
| BTN | 2 | ROUNDING_OFF |
| BWP | 2 | ROUNDING_OFF |
| BYN | 2 | ROUNDING_OFF |
| BYR | 0 | ROUNDING_OFF |
| BZD | 2 | ROUNDING_OFF |
| BZI | 2 | ROUNDING_OFF |
| CAB | 1 | ROUNDING_OFF |
| CAD | 2 | ROUNDING_OFF |
| CDF | 2 | ROUNDING_OFF |
| CER | 1 | ROUNDING_OFF |
| CHB | 1 | ROUNDING_OFF |
| CHF | 2 | ROUNDING_OFF |
| CL4 | 1 | ROUNDING_OFF |
| CLF | 1 | ROUNDING_OFF |
| CLO | 2 | ROUNDING_OFF |
| CNF | 2 | ROUNDING_OFF |
| CNH | 2 | ROUNDING_OFF |
| CNO | 2 | ROUNDING_OFF |
| CNS | 2 | ROUNDING_OFF |
| CNY | 2 | ROUNDING_OFF |
| COP | 0 | ROUNDING_OFF |
| COX | 2 | ROUNDING_OFF |
| CRC | 2 | ROUNDING_OFF |
| CTN | 1 | ROUNDING_OFF |
| CU1 | 2 | ROUNDING_OFF |
| CUC | 2 | ROUNDING_OFF |
| CUH | 1 | ROUNDING_OFF |
| CUP | 2 | ROUNDING_OFF |
| CVE | 0 | ROUNDING_OFF |
| CYM | 2 | ROUNDING_OFF |
| CYP | 1 | ROUNDING_OFF |
| CZK | 2 | ROUNDING_OFF |
| DBT | 1 | ROUNDING_OFF |
| DEM | 2 | ROUNDING_OFF |
| DJE | 2 | ROUNDING_OFF |
| DJF | 0 | ROUNDING_OFF |
| DKK | 2 | ROUNDING_OFF |
| DOL | 1 | ROUNDING_OFF |
| DOP | 2 | ROUNDING_OFF |
| DZD | 2 | ROUNDING_OFF |
| ECS | 2 | ROUNDING_OFF |
| ECU | 2 | ROUNDING_OFF |
| EEK | 2 | ROUNDING_OFF |
| EGO | 2 | ROUNDING_OFF |
| ENP | 2 | ROUNDING_OFF |
| ERN | 2 | ROUNDING_OFF |
| ESP | 2 | ROUNDING_OFF |
| ETB | 2 | ROUNDING_OFF |
| ETH | 3 | ROUNDING_OFF |
| EUA | 1 | ROUNDING_OFF |
| EUB | 2 | ROUNDING_OFF |
| EUO | 1 | ROUNDING_OFF |
| EUR | 2 | ROUNDING_OFF |
| FIM | 2 | ROUNDING_OFF |
| FJD | 2 | ROUNDING_OFF |
| FKP | 2 | ROUNDING_OFF |
| FRF | 2 | ROUNDING_OFF |
| FTI | 1 | ROUNDING_OFF |
| GBB | 1 | ROUNDING_OFF |
| GBI | 1 | ROUNDING_OFF |
| GBP | 2 | ROUNDING_OFF |
| GHC | 2 | ROUNDING_OFF |
| GHH | 2 | ROUNDING_OFF |
| GHO | 2 | ROUNDING_OFF |
| GHS | 2 | ROUNDING_OFF |
| GIP | 2 | ROUNDING_OFF |
| GMD | 2 | ROUNDING_OFF |
| GNF | 0 | ROUNDING_OFF |
| GOL | 1 | ROUNDING_OFF |
| GRD | 2 | ROUNDING_OFF |
| GSE | 2 | ROUNDING_OFF |
| GTQ | 2 | ROUNDING_OFF |
| GYD | 2 | ROUNDING_OFF |
| GYI | 2 | ROUNDING_OFF |
| GYM | 2 | ROUNDING_OFF |
| HKD | 2 | ROUNDING_OFF |
| HNL | 2 | ROUNDING_OFF |
| HRK | 2 | ROUNDING_OFF |
| HSF | 1 | ROUNDING_OFF |
| HTG | 2 | ROUNDING_OFF |
| HUF | 2 | ROUNDING_OFF |
| IDO | 0 | ROUNDING_OFF |
| IDY | 2 | ROUNDING_OFF |
| IEP | 2 | ROUNDING_OFF |
| ILS | 2 | ROUNDING_OFF |
| INO | 2 | ROUNDING_OFF |
| INP | 2 | ROUNDING_OFF |
| INR | 2 | ROUNDING_OFF |
| INY | 2 | ROUNDING_OFF |
| ITL | 2 | ROUNDING_OFF |
| JMD | 2 | ROUNDING_OFF |
| JPB | 2 | ROUNDING_OFF |
| KEH | 2 | ROUNDING_OFF |
| KEO | 2 | ROUNDING_OFF |
| KES | 2 | ROUNDING_OFF |
| KGS | 2 | ROUNDING_OFF |
| KHR | 2 | ROUNDING_OFF |
| KRX | 2 | ROUNDING_OFF |
| KYD | 2 | ROUNDING_OFF |
| IRR | 1 | ROUNDING_OFF |
| ISK | 0 | ROUNDING_OFF |
| JOD | 3 | ROUNDING_OFF |
| JPO | 1 | ROUNDING_OFF |
| KMF | 0 | ROUNDING_OFF |
| KPW | 0 | ROUNDING_OFF |
| KWD | 3 | ROUNDING_OFF |
| KZO | 1 | ROUNDING_OFF |
| CLP | 0 | ROUNDING_DOWN |
| JPY | 0 | ROUNDING_DOWN |
| KZT | 2 | ROUNDING_OFF |
| LEU | 2 | ROUNDING_OFF |
| LGB | 2 | ROUNDING_OFF |
| LKH | 2 | ROUNDING_OFF |
| LKO | 2 | ROUNDING_OFF |
| LKR | 2 | ROUNDING_OFF |
| LRD | 2 | ROUNDING_OFF |
| LSL | 2 | ROUNDING_OFF |
| LTL | 2 | ROUNDING_OFF |
| LUS | 2 | ROUNDING_OFF |
| LVL | 2 | ROUNDING_OFF |
| LVP | 2 | ROUNDING_OFF |
| MAD | 2 | ROUNDING_OFF |
| MDL | 2 | ROUNDING_OFF |
| MKD | 2 | ROUNDING_OFF |
| MND | 2 | ROUNDING_OFF |
| MNT | 2 | ROUNDING_OFF |
| MOP | 2 | ROUNDING_OFF |
| MRU | 2 | ROUNDING_OFF |
| MUR | 2 | ROUNDING_OFF |
| MVR | 2 | ROUNDING_OFF |
| MWK | 2 | ROUNDING_OFF |
| MXN | 2 | ROUNDING_OFF |
| MYO | 2 | ROUNDING_OFF |
| MYR | 2 | ROUNDING_OFF |
| MYZ | 2 | ROUNDING_OFF |
| MZN | 2 | ROUNDING_OFF |
| NAD | 2 | ROUNDING_OFF |
| NGH | 2 | ROUNDING_OFF |
| NGL | 2 | ROUNDING_OFF |
| **NGN** | **2** | **ROUNDING_OFF** |
| NGX | 2 | ROUNDING_OFF |
| NI1 | 2 | ROUNDING_OFF |
| NIO | 2 | ROUNDING_OFF |
| NLG | 2 | ROUNDING_OFF |
| NOK | 2 | ROUNDING_OFF |
| NPH | 2 | ROUNDING_OFF |
| NZD | 2 | ROUNDING_OFF |
| PB1 | 2 | ROUNDING_OFF |
| PEN | 2 | ROUNDING_OFF |
| PEO | 2 | ROUNDING_OFF |
| PGK | 2 | ROUNDING_OFF |
| PHO | 2 | ROUNDING_OFF |
| PHP | 2 | ROUNDING_OFF |
| PKO | 2 | ROUNDING_OFF |
| PKR | 2 | ROUNDING_OFF |
| PLN | 2 | ROUNDING_OFF |
| PMP | 2 | ROUNDING_OFF |
| PTE | 2 | ROUNDING_OFF |
| PYG | 2 | ROUNDING_OFF |
| QAR | 2 | ROUNDING_OFF |
| RON | 2 | ROUNDING_OFF |
| RSD | 2 | ROUNDING_OFF |
| RUB | 2 | ROUNDING_OFF |
| RUR | 2 | ROUNDING_OFF |
| RUW | 2 | ROUNDING_OFF |
| SAR | 2 | ROUNDING_OFF |
| SBD | 2 | ROUNDING_OFF |
| SCR | 2 | ROUNDING_OFF |
| SDG | 2 | ROUNDING_OFF |
| SEK | 2 | ROUNDING_OFF |
| SGD | 2 | ROUNDING_OFF |
| SGH | 2 | ROUNDING_OFF |
| SGN | 2 | ROUNDING_OFF |
| SGO | 2 | ROUNDING_OFF |
| SHP | 2 | ROUNDING_OFF |
| SIT | 2 | ROUNDING_OFF |
| SKK | 2 | ROUNDING_OFF |
| SLE | 2 | ROUNDING_OFF |
| SLL | 2 | ROUNDING_OFF |
| SN1 | 2 | ROUNDING_OFF |
| SRD | 2 | ROUNDING_OFF |
| SSP | 2 | ROUNDING_OFF |
| STN | 2 | ROUNDING_OFF |
| SVC | 2 | ROUNDING_OFF |
| SYP | 2 | ROUNDING_OFF |
| SZL | 2 | ROUNDING_OFF |
| THB | 2 | ROUNDING_OFF |
| THO | 2 | ROUNDING_OFF |
| THS | 2 | ROUNDING_OFF |
| TJS | 2 | ROUNDING_OFF |
| TMT | 2 | ROUNDING_OFF |
| TOP | 2 | ROUNDING_OFF |
| TRY | 2 | ROUNDING_OFF |
| TTD | 2 | ROUNDING_OFF |
| TYO | 2 | ROUNDING_OFF |
| TZH | 2 | ROUNDING_OFF |
| TZO | 2 | ROUNDING_OFF |
| TZS | 2 | ROUNDING_OFF |
| UAH | 2 | ROUNDING_OFF |
| UFF | 2 | ROUNDING_OFF |
| UGH | 2 | ROUNDING_OFF |
| UGO | 2 | ROUNDING_OFF |
| USB | 2 | ROUNDING_OFF |
| USD | 2 | ROUNDING_OFF |
| UYU | 2 | ROUNDING_OFF |
| UZH | 2 | ROUNDING_OFF |
| UZS | 2 | ROUNDING_OFF |
| VEB | 2 | ROUNDING_OFF |
| VEF | 2 | ROUNDING_OFF |
| WST | 2 | ROUNDING_OFF |
| XAQ | 2 | ROUNDING_OFF |
| XCD | 2 | ROUNDING_OFF |
| XEU | 2 | ROUNDING_OFF |
| NGA | 1 | ROUNDING_OFF |
| NGY | 1 | ROUNDING_OFF |
| NIH | 1 | ROUNDING_OFF |
| OIL | 1 | ROUNDING_OFF |
| OMR | 3 | ROUNDING_OFF |
| PTH | 1 | ROUNDING_OFF |
| RUO | 2 | ROUNDING_OFF |
| RWF | 0 | ROUNDING_OFF |
| SGB | 1 | ROUNDING_OFF |
| SNH | 1 | ROUNDING_OFF |
| STD | 0 | ROUNDING_OFF |
| THN | 1 | ROUNDING_OFF |
| TND | 1 | ROUNDING_OFF |
| TRL | 1 | ROUNDING_OFF |
| TWO | 0 | ROUNDING_OFF |
| UGX | 0 | ROUNDING_OFF |
| UVR | 1 | ROUNDING_OFF |
| VND | 0 | ROUNDING_OFF |
| VNO | 0 | ROUNDING_OFF |
| XAF | 0 | ROUNDING_OFF |
| XAG | 3 | ROUNDING_OFF |
| XAH | 1 | ROUNDING_OFF |
| XAU | 3 | ROUNDING_OFF |
| XD1 | 3 | ROUNDING_OFF |
| XD2 | 3 | ROUNDING_OFF |
| XD3 | 3 | ROUNDING_OFF |
| XDN | 3 | ROUNDING_OFF |
| XG1 | 3 | ROUNDING_OFF |
| XG2 | 3 | ROUNDING_OFF |
| XG3 | 3 | ROUNDING_OFF |
| XGB | 2 | ROUNDING_OFF |
| XUS | 2 | ROUNDING_OFF |
| YDA | 2 | ROUNDING_OFF |
| YDI | 2 | ROUNDING_OFF |
| ZAR | 2 | ROUNDING_OFF |
| ZIG | 2 | ROUNDING_OFF |
| ZMH | 2 | ROUNDING_OFF |
| ZMO | 2 | ROUNDING_OFF |
| ZMW | 2 | ROUNDING_OFF |
| ZN1 | 2 | ROUNDING_OFF |
| ZWL | 2 | ROUNDING_OFF |
| XG4 | 3 | ROUNDING_OFF |
| XG5 | 3 | ROUNDING_OFF |
| XG6 | 3 | ROUNDING_OFF |
| XGC | 3 | ROUNDING_OFF |
| XGD | 1 | ROUNDING_OFF |
| XGI | 3 | ROUNDING_OFF |
| XI1 | 1 | ROUNDING_OFF |
| XIR | 1 | ROUNDING_OFF |
| XOF | 0 | ROUNDING_OFF |
| XOH | 1 | ROUNDING_OFF |
| XPD | 3 | ROUNDING_OFF |
| XPF | 0 | ROUNDING_OFF |
| XPT | 3 | ROUNDING_OFF |
| XR1 | 3 | ROUNDING_OFF |
| XRM | 1 | ROUNDING_OFF |
| XRU | 3 | ROUNDING_OFF |
| XS4 | 3 | ROUNDING_OFF |
| XS5 | 3 | ROUNDING_OFF |
| XS6 | 3 | ROUNDING_OFF |
| XS9 | 3 | ROUNDING_OFF |
| XSD | 3 | ROUNDING_OFF |
| XT1 | 3 | ROUNDING_OFF |
| XT2 | 3 | ROUNDING_OFF |
| XT3 | 3 | ROUNDING_OFF |
| XTN | 3 | ROUNDING_OFF |
| XU1 | 3 | ROUNDING_OFF |
| XU2 | 3 | ROUNDING_OFF |
| XU3 | 3 | ROUNDING_OFF |
| XU4 | 3 | ROUNDING_OFF |
| XU5 | 3 | ROUNDING_OFF |
| XU7 | 3 | ROUNDING_OFF |
| XU8 | 3 | ROUNDING_OFF |
| XU9 | 1 | ROUNDING_OFF |
| XUC | 3 | ROUNDING_OFF |
| XUD | 3 | ROUNDING_OFF |
| XUX | 1 | ROUNDING_OFF |
| YD2 | 1 | ROUNDING_OFF |
| YER | 0 | ROUNDING_OFF |
| ZCN | 1 | ROUNDING_OFF |
| ZEU | 1 | ROUNDING_OFF |
| ZGB | 1 | ROUNDING_OFF |
| ZIN | 1 | ROUNDING_OFF |
| ZMK | 0 | ROUNDING_OFF |
| ZNH | 1 | ROUNDING_OFF |
| ZZA | 1 | ROUNDING_OFF |
| IQD | 3 | ROUNDING_OFF |
| LAK | 0 | ROUNDING_OFF |
| MZH | 1 | ROUNDING_OFF |
| NGO | 1 | ROUNDING_OFF |
| NGZ | 1 | ROUNDING_OFF |
| PBH | 1 | ROUNDING_OFF |
| PDH | 1 | ROUNDING_OFF |
| PKH | 1 | ROUNDING_OFF |
| VUV | 0 | ROUNDING_OFF |
| WTI | 1 | ROUNDING_OFF |
| KRO | 0 | ROUNDING_DOWN |
| DZH | 1 | ROUNDING_OFF |
| EGP | 2 | ROUNDING_OFF |
| GEL | 2 | ROUNDING_OFF |
| IDR | 0 | ROUNDING_OFF |
| KRW | 0 | ROUNDING_OFF |
| LBP | 0 | ROUNDING_OFF |
| LYD | 3 | ROUNDING_OFF |
| MAH | 1 | ROUNDING_OFF |
| MGA | 0 | ROUNDING_OFF |
| MMK | 0 | ROUNDING_OFF |
| MRO | 1 | ROUNDING_OFF |
| NPR | 2 | ROUNDING_OFF |
| PAB | 2 | ROUNDING_OFF |
| SOS | 2 | ROUNDING_OFF |
| TNH | 1 | ROUNDING_OFF |
| TWD | 1 | ROUNDING_OFF |
| UDI | 2 | ROUNDING_OFF |
| XBT | 3 | ROUNDING_OFF |
| XET | 3 | ROUNDING_OFF |
| XG7 | 1 | ROUNDING_OFF |
| XGA | 1 | ROUNDING_OFF |
| XGF | 1 | ROUNDING_OFF |
| XRH | 1 | ROUNDING_OFF |
| XSF | 2 | ROUNDING_OFF |
| XSI | 2 | ROUNDING_OFF |
| XU6 | 1 | ROUNDING_OFF |

**EXPAND_END**

## EBBS Bridge Account

2026-03-09 Yashas provided the data ,but QATAR and Bangladesh need to be double confirm

| id | closing_entity | legal_entity | fmid | ebbs_bridge_account | Comment |
| --- | --- | --- | --- | --- | --- |
| | | SCB BAHRAI*MAN | 10036430 | 09906397050 | |
| | | SCB DOHA*DOH | 300010782 | 09473025940 | |
| | | SLATE ONE LLC*DOH | 401081696 | NA | 2026-03-23 Confirmed with Synthia ,SLATE cashflow will be cashflow suppressed ,then rest of static is not required. Only Cashflow Suppression static is required. |
| | | SCB KENYA B*NBO | 300011525 | 0062599158900 | |
| | | SCB ZAMBIA*LUS | 10041903 | 0062599158900 | |
| | | SCB UGANDA*KAM | 10041902 | 0062599158900 | |
| | | SCB TANZANI*DAR | 10040387 | 0062599158900 | |
| | | SCB GHANA*ACC | 10037477 | 0062599150800 | |
| | | SCB NIGERIA*LAG | 300084297 | 9625047537 | |
| | | SCB COLOMBO*CMB | 10036647 | 09995954893 | |
| | | SCB COL FCB*CMB | 10022098 | 09995954895 | |
| | | SCB HANOI*HNI | 10041530 | 09434372001 | |
| | | SCB KARACHI*KHI | 10036655 | 09900006470 | |
| | | SCB DHAKA*DAC | 300011470 | 09111178468 | |

📎 [EBBS bridge account.xlsx](attachments/EBBS bridge account.xlsx)

## EBBS Posting_Branch/Txn_dr_code/Txn_cr_code/Txn_type_code（Transaction Type）

2026-06-15  Got update from ebbs that Cr Txn Code should be update to 578 from 278 for TZ

📎 [RATAN ISD UPDATE _ TZ TRNCD.msg](attachments/RATAN ISD UPDATE _ TZ TRNCD.msg)
   
📎 [EBBS posting branch etc.xlsx](attachments/EBBS posting branch etc.xlsx)

| FMID | Country | Posting Branch | Txn Type code | Dr Txn Code | Cr Txn Code |
| --- | --- | --- | --- | --- | --- |
| 10037477 | GH | 00001 | RTN | 478 | 278 |
| 10041530 | VN | 099 | RTN | 478 | 378 |
| 300011525 | KE | 07800 | RTN | 478 | 278 |
| 300084297 | NG | 00100 | RTN | 478 | 278 |
| 10040387 | TZ | 08700 | RTN | 478 | 578 |
| 10041902 | UG | 00001 | RTN | 478 | 278 |
| 10041903 | ZM | 01700 | RTN | 478 | 278 |
| 300011470 | BD | 068 | RTN | 478 | 378 |
| 10036655 | PK | 001 | RTN | 478 | 678 |
| 10036647 | LK | 093 | RTN | 478 | 378 |
| 10022098 | LK | 093 | RTN | 478 | 378 |
| 10036430 | BH | 055 | RTN | 478 | 378 |
| 300010782 | QA | 042 | RTN | 478 | 378 |

## TimeZone

When generate accounting ,system will get country by fmid from above static table ,then get zoneid via country, if there is new country on boarding ,we need to config this

2026-03-13

Provided  by J, Madhankumar and Yashas

| Country full name | Country | zoneId |
| --- | --- | --- |
| BAHRAIN | BH | Asia/Bahrain |
| QATAR | QA | Asia/Qatar |
| KENYA | KE | Africa/Nairobi |
| ZAMBIA | ZM | Africa/Lusaka |
| UGANDA | UG | Africa/Kampala |
| TANZANIA | TZ | Africa/Dar_es_Salaam |
| GHANA | GH | Africa/Accra |
| NIGERIA | NG | Africa/Lagos |
| SRI LANKA | LK | Asia/Colombo |
| Vietnam | VN | Asia/Ho_Chi_Minh |
| Pakistan | PK | Asia/Karachi |
| Bangladesh | BD | Asia/Dhaka |

📎 [Accounting TimeZone.xlsx](attachments/Accounting TimeZone.xlsx)

**EXPAND: Accounting Timezone**

| time-zone: |
| --- |
| mappings: |
| - country: CN |
| zoneId: Asia/Shanghai |
| - country: SG |
| zoneId: Singapore |
| - country: MY |
| zoneId: Asia/Kuching |
| - country: IN |
| zoneId: Asia/Kolkata |
| - country: UK |
| zoneId: GMT |
| - country: GB |
| zoneId: GMT |
| - country: DE |
| zoneId: Europe/Berlin |
| - country: US |
| zoneId: America/New_York |
| - country: TW |
| zoneId: Asia/Taipei |
| - country: HK |
| zoneId: Asia/Hong_Kong |
| - country: TH |
| zoneId: Asia/Bangkok |
| - country: JP |
| zoneId: Asia/Tokyo |
| - country: AE |
| zoneId: Asia/Dubai |
| - country: PH |
| zoneId: Asia/Manila |
| - country: ID |
| zoneId: Asia/Jakarta |
| - country: MU |
| zoneId: Indian/Mauritius |
| - country: ZA |
| zoneId: Africa/Johannesburg |
| - country: EG |
| zoneId: Africa/Cairo |
| - country: NP |
| zoneId: Asia/Kathmandu |
| - country: SA |
| zoneId: Asia/Riyadh |
| - country: JE |
| zoneId: Europe/Jersey |

**EXPAND_END**

## Currency on UI dropdown list

2026-08-04

Need to add Non ISO /ISO ccy in Cashflow Blotter-Quick Search- Currency-dropdown list on UI for manual entities

![image-2026-8-4_14-55-7.png](attachments/image-2026-8-4_14-55-7.png)

| ISO | Non ISO |
| --- | --- |
| BHD | |
| VND | VNO |
| NGN | NGO/NGY/NGH/NGX/NGA/NGB |
| PKR | PKH/PKO |
| GHS | GHH |
| UGX | UGH |
| ZMW | ZMH |
| KES | KEH |
| QAR | |
| LKR | LKO/LKH |
| TZS | TZH |
| BDT | BDO |

## Not Generate Accounting

2026-03-06 Confirmed with Yashas, due to no PM ccy go live ,so no additional  requirement for this part

if the entity in 10075222,400041070 and PM currency in below list ,will  not generate accounting

**EXPAND: Accounting PM Currency**

| XAG |
| --- |
| XAU |
| XD1 |
| XD2 |
| XD3 |
| XG1 |
| XG2 |
| XG3 |
| XG4 |
| XG5 |
| XG7 |
| XGA |
| XGF |
| XI1 |
| XIR |
| XPD |
| XPT |
| XR1 |
| XRH |
| XRM |
| XRU |
| XS5 |
| XS9 |
| XSD |
| XSF |
| XSI |
| XT1 |
| XT2 |
| XT3 |
| XU1 |
| XU2 |
| XU3 |
| XU4 |
| XU5 |
| XU6 |
| XU7 |
| XU8 |
| XU9 |
| XUD |
| XUX |

**EXPAND_END**

## PM Currency

2026-02-25got confirmation from @Deepak K and @Yashas Balaji  , no Metal currencies which are applicable for manual enties

![image-2026-2-26_9-40-16.png](attachments/image-2026-2-26_9-40-16.png)

2026-01-20Confirmed by @Arockia Dinesh  No new PM currency added for manual entities

**EXPAND: PM Currency**

| PM currency |
| --- |
| XAU |
| XAG |
| XPD |
| XPT |
| XRH |
| XU5 |
| XG2 |
| XT3 |
| XD3 |
| XRU |
| XS9 |
| XS5 |
| XSD |
| XU6 |
| XU7 |
| XG5 |
| XUC |
| XG3 |
| XGC |
| XD1 |
| XD2 |
| XG1 |
| XR1 |
| XT1 |
| XT2 |
| XU1 |
| XU2 |
| XU3 |
| XU4 |
| XU8 |
| XTN |
| XDN |
| XUD |
| XG4 |
| XG6 |
| XGF |
| XS6 |
| XSF |
| XSI |
| XS4 |
| XGI |
| XGA |
| XG7 |

**EXPAND_END**

## Receiver BIC(MT604/MT605)

2026-02-25got confirmation from @Deepak K and @Yashas Balaji  , no Metal currencies which are applicable for manual enties, so no impact for this part

<details>
<summary>Expand Details</summary>

2026-02-02

Double confirmed with Sumita,all PM cashflows upto today is cashflow suppressed,so **no hard code **receiver bic required

2026-01-20 For BAHRAIN ,Confirmed by @Cordelia Sumita K Thirunavukarasu need to hardcode the Receiver BIC in MT604/MT605

if (entityFMID in ('300036368','3','400451508','400452428','2', '400906330', '10036430') and {Field_Currency} in ( XAU,XAG,XPD,XPT))
        return receiverBIC =CHASGB2LXXXX

</details>

## UDF_Strategy

2026-02-25got confirmation from @Deepak K and @Yashas Balaji  , no Metal currencies which are applicable for manual enties ,so no impact for this part

For MT604/MT605 ,field 23,26,32 ,we need static data from below tables

![image-2026-1-19_9-47-4.png](attachments/image-2026-1-19_9-47-4.png)

![image-2026-1-19_9-47-23.png](attachments/image-2026-1-19_9-47-23.png)

![image-2026-1-19_9-47-46.png](attachments/image-2026-1-19_9-47-46.png)

**EXPAND: UDF_Strategy**

| k_strategy | v_allocation | v_available_location |
| --- | --- | --- |
| COM_BOE_DELIV | ALLOC | BOE |
| COM_CHAS_LDN | | LONDON |
| COM_CHAS_ZRH | | ZURICH |
| COM_JMUK_DELIV | | JMUK |
| COM_JMVF_DELIV | | JMVF |
| COM_RAND_DELIV | | RAND |
| COM_BDF_DELIV | ALLOC | PARIS |
| COM_BDF_DVP | ALLOC | PARIS |
| COM_LDN_DVP | | LONDON |
| COM_BOE_DELIV_S | ALLOC | BOE |
| COM_ZRH_DELIV_S | | ZURICH |
| COM_BDF_DELIV_S | ALLOC | PARIS |

**EXPAND_END**

## UDF_SWF_LS

2026-02-25got confirmation from @Deepak K and @Yashas Balaji  , no Metal currencies which are applicable for manual enties ,so no impact for this part

**EXPAND: UDF_SWF_LS**

| k_currency | v_allocation | v_available_location | v_quality | v_type | v_unit |
| --- | --- | --- | --- | --- | --- |
| XAG | UNALL | LONDON | 9990 | SILV | GOZ |
| XAQ | UNALL | LONDON | | GOLD | FOZ |
| XAU | UNALL | LONDON | 9950 | GOLD | FOZ |
| XD1 | ALLOC | TBC | 9995 | PALL | GOZ |
| XD2 | ALLOC | TBC | 9995 | PALL | GOZ |
| XD3 | ALLOC | TBC | Palladium Warrants | PALL | GOZ |
| XG1 | ALLOC | TBC | 9990 | SILV | GOZ |
| XG2 | ALLOC | TBC | 9990 | SILV | GOZ |
| XG3 | ALLOC | TBC | 9990 | SILV | GOZ |
| XG5 | ALLOC | TBC | 9995 | SILV | GOZ |
| XGC | UNALL | LONDON | | SILV | GOZ |
| XGD | UNALL | LONDON | | SILV | GOZ |
| XPD | UNALL | ZURICH | 9995 | PALL | GOZ |
| XR1 | ALLOC | TBC | 995 | RHOD | TOZ |
| XRH | UNALL | LONDON | | RHOD | TOZ |
| XRU | UNALL | LONDON | | RUTH | TOZ |
| XS5 | ALLOC | TBC | 9995 | GOLD | FOZ |
| XS9 | ALLOC | TBC | 9999 | GOLD | FOZ |
| XSD | UNALL | LONDON | | GOLD | FOZ |
| XT1 | ALLOC | TBC | 9995 | PLAT | GOZ |
| XT2 | ALLOC | TBC | 9995 | PLAT | GOZ |
| XT3 | ALLOC | TBC | Platinum Warrants | PLAT | GOZ |
| XU1 | ALLOC | TBC | 9999 | GOLD | FOZ |
| XU2 | ALLOC | TBC | 995 | GOLD | FOZ |
| XU3 | ALLOC | TBC | 995 | GOLD | FOZ |
| XU4 | ALLOC | TBC | 9999 | GOLD | FOZ |
| XU5 | ALLOC | NEW YORK | | GOLD | FOZ |
| XU6 | ALLOC | TBC | 999 | GOLD | FOZ |
| XU7 | ALLOC | TBC | 999 | GOLD | FOZ |
| XU8 | ALLOC | TBC | 995 | GOLD | FOZ |
| XUC | UNALL | LONDON | | GOLD | FOZ |
| XGI | ALLOC | TBC | 9990 | SILV | GOZ |
| XPT | UNALL | ZURICH | 9995 | PLAT | GOZ |
| XG7 | ALLOC | TBC | 9990 | SILV | GOZ |

**EXPAND_END**

## CFI CODE

Confirm with  @Arockia Dinesh ,no new CFI code for manual entities

# MX Bifurcation logic

[02 Swift Message Analysing for manual entities - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/02+Swift+Message+Analysing+for+manual+entities)   ---[MX B](https://confluence.global.standardchartered.com/display/DSP/02+Swift+Message+Analysing+for+manual+entities#id-02SwiftMessageAnalysingformanualentities-MXEligibilityRule)ifurcation Logic

[(3) Manual entity (NG/GH/QA/BH/UG) testing with ISO - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3824859990)

[RATAN ISO20022: 2026 Bifurcation Logic - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/RATAN+ISO20022%3A+2026+Bifurcation+Logic)

# Business Rule Setup

## 📎 [Business rule0811.xlsx](attachments/Business rule0811.xlsx)

## NSTP

| | Country | Action | FMID | Exception Code | Operational Level | Exception Category | Rule Condition | Existing production Rule reference(Exception Code) | Rule Reason | Bulk Eligible | Pre Rule | Post Rule | Requested by | Comment |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | BAHRAIN/NIGERIA | NEW | 10036430 | KL LDN COM | MAKER_CHECKER | NSTP | 1. Counterparty FMID : 400059781, 400073945, 400035746 2. Instrument_Common__ISDA_Taxonomy in ("Commodity:Metals:Precious:SpotFwd:Physical", "Commodity:Metals:Precious:SpotFwd:Cash", "CURR FXD FXD", "CURR OPT SMP", "CURR FXD XSW", "COM SWAP", "IRD LN_BR" 3. Cashflow__Is_Commodity == true | | KL LDN COM | TRUE | | FMRP2:7450078991002316800 ((Entity__Booking_Entity_SCI_FMID == "10036430" && Entity__Counterparty_SCI_FMID in ("400059781", "400073945", "400035746")) || (Entity__Booking_Entity_SCI_FMID == "300084297" && Entity__Counterparty_SCI_FMID in ("400205597", "401027822", "401029422"))) && (Cashflow__Is_Commodity == true || Instrument_Common__ISDA_Taxonomy in ("Commodity:Metals:Precious:SpotFwd:Physical", "Commodity:Metals:Precious:SpotFwd:Cash", "CURR|FXD|FXD", "CURR|OPT|SMP", "CURR|FXD|XSW", "COM|SWAP", "IRD|LN_BR")) | Sumita | 2026-03-09 Approved by Sumita |
| 2 | 300084297 | 1. Counterparty FMID : 400205597,401027822,401029422 CurrencyALL 2.Instrument_Common__ISDA_Taxonomy in ("Commodity:Metals:Precious:SpotFwd:Physical", "Commodity:Metals:Precious:SpotFwd:Cash", "CURR FXD FXD", "CURR OPT SMP", "CURR FXD XSW", "COM SWAP", "IRD LN_BR" 3.Cashflow__Is_Commodity == true |
| 3 | Vietnam | UPDATE | 10041530 | SEA NSTP CORP | MAKER_CHECKER | NSTP | 1. Counterpart FMID : 400005529, 400057688, 400053903, 400053899, 400207966 Currency : ALL | | SEA NSTP CORP (PROD RULE ID : 7348011873748709376) | FALSE | ((Entity__Booking_Entity_SCI_FMID == "400018439" && Entity__Counterparty_SCI_FMID == "401038865") || (Entity__Booking_Entity_SCI_FMID in ("10036428", "400077978") && Entity__Counterparty_SCI_FMID in ("225003194", "400001861", "400021478", "400042450", "400044466")) || (Entity__Booking_Entity_SCI_FMID == "8" && Entity__Counterparty_SCI_FMID in ("300046579", "400027041", "400058687", "400059558", "400070560", "400117714", "400616704", "400919394", "400948948", "400983468", "401017790", "401049571", "401057665"))) | FMRP2: 7450079845900025856 ((Entity__Booking_Entity_SCI_FMID == "400018439" && Entity__Counterparty_SCI_FMID == "401038865") || (Entity__Booking_Entity_SCI_FMID in ("10036428", "300089409") && Entity__Counterparty_SCI_FMID in ("225003194", "400001861", "400021478", "400042450", "400044466")) || (Entity__Booking_Entity_SCI_FMID == "8" && Entity__Counterparty_SCI_FMID in ("300046579", "400027041", "400058687", "400059558", "400070560", "400117714", "400616704", "400919394", "400948948", "400983468", "401017790", "401049571", "401057665")) || (Entity__Booking_Entity_SCI_FMID == "10041530" && Entity__Counterparty_SCI_FMID in ("400005529", "400057688", "400053903", "400053899", "400207966"))) | Sumita | 2026-03-09 Approved by Sumita |
| 4 | Srilanka /Pakistan | NEW | 10036647 10022098 10036655 | DVP Check | MAKER_CHECKER | NSTP | booking entity 10036647， 10022098，10036655 counterpaty anything | | DVP Check | FALSE | | FMRP2: 7484794922794147840 Entity__Booking_Entity_SCI_FMID in ("10036647", "10022098", "10036655") | Shalini/Deepak | 2026-07-20 7/20/2026:Requested by Deepak to add PK in the condition 2026-03-04 Reviewed during the call .Agreed by Dinesh |
| 5 | Bangeladesh | NEW | 300011470 | BD NSTP | MAKER_CHECKER | NSTP | Entity__Booking_Entity_SCI_FMID == "300011470" counterpaty anything | | BD NSTP | TRUE | | FMRP2:7462746525033795584 Entity__Booking_Entity_SCI_FMID == "300011470" | Golam | 2026-04-28 Confirm during the call with Golam and Dinesh |
| 6 | BAHARIN QATAR-DOHA | UPDATE | 10036430, 300010782 | New Islamic Portfolios | MAKER_CHECKER | NSTP | Add 10036430,300010782 in Entity.Booking_Entity_SCI_FMID list | | New Islamic Portfolios | TRUE | Entity__Booking_Entity_SCI_FMID in ("400045551", "5") && Portfolio__Booking_Entity_Trade_Portfolio_Name == "IS_NDF_BTB_DFC" | FMRP2:7467176769140609024 Entity__Booking_Entity_SCI_FMID in ("400045551", "5", "10036430", "300010782") && Portfolio__Booking_Entity_Trade_Portfolio_Name == "IS_NDF_BTB_DFC" | Synthia/Gomathy | 2026-06-01 aAligned with Deepak and Gomathy UPDATE exsiting rule ,only apply to BAHARIN QATAR-DOHA |
| 7 | BAHARIN QATAR-DOHA | UPDATE | 10036430, 300010782 | Islamic Portfolios | MAKER_CHECKER | NSTP | Add 10036430,300010782 in Entity.Booking_Entity_SCI_FMID list | | Islamic Portfolios | TRUE | Portfolio__Booking_Entity_Trade_Portfolio_Name matches ".*(?i)ISL.*" && Entity__Booking_Entity_SCI_FMID in ("10075222", "400045551", "5") | FMRP2: 7467179712199704576 Portfolio__Booking_Entity_Trade_Portfolio_Name matches ".*(?i)ISL.*" && Entity__Booking_Entity_SCI_FMID in ("10075222", "400045551", "5", "10036430", "300010782") | Synthia/Gomathy | 2026-06-01 Aligned with Deepak and Gomathy UPDATE exsiting rule ,only apply to BAHARIN QATAR-DOHA |
| 8 | KENYA, BAHRAIN, UGANDA, ZAMBIA, NIGERIA, GHANA, Qatar | NEW | 10036430 300084297 300010782 300011525 10041903 10037477 10041902 | AME OIS | MAKER_CHECKER | NSTP | 1.Booking entity:10036430,300084297,300010782,300011525,10041903,10037477,10041902 2.the other condition is the same with the existing rule which AND Instrument_Common.Murex_Product_Typology == ""OIS"" AND Entity.Counterparty_SCI_FMID not in (""400953656"", ""300010735"", ""400800797"", ""400933624"", ""400258208"", ""400963307"", ""400812227"", ""400800798"", ""400935870"", ""400178088"", ""300037428"", ""400111150"", ""400969140"", ""400917505"", ""400059979"", ""400174369"", ""300037798"", ""400948418"", ""400036336"", ""10037477"", ""400001378"", ""6"", ""10036647"", ""300011470"", ""5"", ""10036775"", ""2"", ""400035821"", ""8"", ""10036655"", ""9"", ""10075222"", ""4"", ""10036428"", ""7"", ""10036642"", ""10032025"", ""3"", ""400054737"", ""235003861"", ""10038345"", ""10036382"", ""10078716"", ""400095464"", ""400085753"", ""400045551"", ""400076756"", ""400032489"", ""300011525"", ""400028508"", ""300084297"", ""400909808"", ""400909807"", ""400089621"", ""400677737"", ""10041902"", ""400045057"", ""10036645"", ""300011345"", ""400066743"", ""400037785"", ""400452428"", ""400451508"", ""10036430"", ""400220273"", ""400899993"", ""400906330"", ""400058400"", ""400058398"", ""400130180"", ""400057714"", ""400058394"", ""10062461"", ""400107228"", ""400018439"", ""400041299"", ""400040747"", ""400040748"", ""400061773"", ""400037836"", ""400040412"", ""400037791"", ""400037921"", ""400037726"", ""400037729"", ""400037922"", ""400068942"", ""400054708"", ""400185419"", ""400038327"", ""15"", ""400044944"", ""400039759"", ""400040374"", ""400040633"", ""400054741"", ""400039882"", ""400046882"", ""400044796"", ""400063823"", ""400057870"", ""400040016"", ""400040017"", ""400040019"", ""400046458"", ""400037869"", ""400068898"", ""400037875"", ""400037876"", ""400044094"", ""400056963"", ""400063826"", ""400037877"", ""400057191"", ""400058543"", ""400040294"", ""400040027"", ""400037900"", ""400040285"", ""400057418"", ""400040006"", ""400071395"", ""400039582"", ""400060385"", ""400061872"", ""400037926"", ""400037940"", ""400040263"", ""400066464"", ""400037777"", ""400042544"", ""400076878"", ""400040039"", ""400037818"", ""400037820"", ""400037774"", ""400037944"", ""400040235"", ""400040231"", ""400037927"", ""400040044"", ""400040043"", ""400040045"", ""400007847"", ""400107029"", ""400058727"", ""400057346"", ""400039854"", ""400053597"", ""400016899"", ""400016959"", ""10020899"", ""400667486"", ""400798477"", ""400059347"", ""400075752"", ""400209000"", ""400229749"", ""400683682"", ""400130178"", ""400218197"", ""400090093"", ""400516443"", ""400193370"", ""400516442"", ""401053411"", ""400960089"", ""400910415"") | UKDE OIS | AME OIS | TRUE | | FMRP2:7473302955298152448 Entity__Booking_Entity_SCI_FMID in ("10036430", "300084297", "300010782", "300011525", "10041903", "10037477", "10041902") && Instrument_Common__Murex_Product_Typology == "OIS" && Entity__Counterparty_SCI_FMID not in ("400953656", "300010735", "400800797", "400933624", "400258208", "400963307", "400812227", "400800798", "400935870", "400178088", "300037428", "400111150", "400969140", "400917505", "400059979", "400174369", "300037798", "400948418", "400036336", "10037477", "400001378", "6", "10036647", "300011470", "5", "10036775", "2", "400035821", "8", "10036655", "9", "10075222", "4", "10036428", "7", "10036642", "10032025", "3", "400054737", "235003861", "10038345", "10036382", "10078716", "400095464", "400085753", "400045551", "400076756", "400032489", "300011525", "400028508", "300084297", "400909808", "400909807", "400089621", "400677737", "10041902", "400045057", "10036645", "300011345", "400066743", "400037785", "400452428", "400451508", "10036430", "400220273", "400899993", "400906330", "400058400", "400058398", "400130180", "400057714", "400058394", "10062461", "400107228", "400018439", "400041299", "400040747", "400040748", "400061773", "400037836", "400040412", "400037791", "400037921", "400037726", "400037729", "400037922", "400068942", "400054708", "400185419", "400038327", "15", "400044944", "400039759", "400040374", "400040633", "400054741", "400039882", "400046882", "400044796", "400063823", "400057870", "400040016", "400040017", "400040019", "400046458", "400037869", "400068898", "400037875", "400037876", "400044094", "400056963", "400063826", "400037877", "400057191", "400058543", "400040294", "400040027", "400037900", "400040285", "400057418", "400040006", "400071395", "400039582", "400060385", "400061872", "400037926", "400037940", "400040263", "400066464", "400037777", "400042544", "400076878", "400040039", "400037818", "400037820", "400037774", "400037944", "400040235", "400040231", "400037927", "400040044", "400040043", "400040045", "400007847", "400107029", "400058727", "400057346", "400039854", "400053597", "400016899", "400016959", "10020899", "400667486", "400798477", "400059347", "400075752", "400209000", "400229749", "400683682", "400130178", "400218197", "400090093", "400516443", "400193370", "400516442", "401053411", "400960089", "400910415") | Synthia/Gomathy | 2026-06-18 Aligned with Deepak and Gomathy 1.create a new rule and put 7 entities in booking entity list 2.the other condition keep the same with the existing rule |
| 9 | KENYA, BAHRAIN, UGANDA, ZAMBIA, NIGERIA, GHANA, Qatar | NEW | 10036430 300084297 300010782 300011525 10041903 10037477 10041902 | PCD/DCD | MAKER_CHECKER | NSTP | 1.Booking entity:10036430,300084297,300010782,300011525,10041903,10037477,10041902 2.the other condition is the same with the existing rule which AND Instrument_Common.Murex_Product_Strategy in ""FX_PCD"" and FX_DCD 3.AND Entity.Counterparty_SCI_FMID not in (""400953656"", ""300010735"", ""400800797"", ""400933624"", ""400258208"", ""400963307"", ""400812227"", ""400800798"", ""400935870"", ""400178088"", ""300037428"", ""400111150"", ""400969140"", ""400917505"", ""400059979"", ""400174369"", ""300037798"", ""400948418"", ""400036336"", ""10037477"", ""400001378"", ""6"", ""10036647"", ""300011470"", ""5"", ""10036775"", ""2"", ""400035821"", ""8"", ""10036655"", ""9"", ""10075222"", ""4"", ""10036428"", ""7"", ""10036642"", ""10032025"", ""3"", ""400054737"", ""235003861"", ""10038345"", ""10036382"", ""10078716"", ""400095464"", ""400085753"", ""400045551"", ""400076756"", ""400032489"", ""300011525"", ""400028508"", ""300084297"", ""400909808"", ""400909807"", ""400089621"", ""400677737"", ""10041902"", ""400045057"", ""10036645"", ""300011345"", ""400066743"", ""400037785"", ""400452428"", ""400451508"", ""10036430"", ""400220273"", ""400899993"", ""400906330"", ""400058400"", ""400058398"", ""400130180"", ""400057714"", ""400058394"", ""10062461"", ""400107228"", ""400018439"", ""400041299"", ""400040747"", ""400040748"", ""400061773"", ""400037836"", ""400040412"", ""400037791"", ""400037921"", ""400037726"", ""400037729"", ""400037922"", ""400068942"", ""400054708"", ""400185419"", ""400038327"", ""15"", ""400044944"", ""400039759"", ""400040374"", ""400040633"", ""400054741"", ""400039882"", ""400046882"", ""400044796"", ""400063823"", ""400057870"", ""400040016"", ""400040017"", ""400040019"", ""400046458"", ""400037869"", ""400068898"", ""400037875"", ""400037876"", ""400044094"", ""400056963"", ""400063826"", ""400037877"", ""400057191"", ""400058543"", ""400040294"", ""400040027"", ""400037900"", ""400040285"", ""400057418"", ""400040006"", ""400071395"", ""400039582"", ""400060385"", ""400061872"", ""400037926"", ""400037940"", ""400040263"", ""400066464"", ""400037777"", ""400042544"", ""400076878"", ""400040039"", ""400037818"", ""400037820"", ""400037774"", ""400037944"", ""400040235"", ""400040231"", ""400037927"", ""400040044"", ""400040043"", ""400040045"", ""400007847"", ""400107029"", ""400058727"", ""400057346"", ""400039854"", ""400053597"", ""400016899"", ""400016959"", ""10020899"", ""400667486"", ""400798477"", ""400059347"", ""400075752"", ""400209000"", ""400229749"", ""400683682"", ""400130178"", ""400218197"", ""400090093"", ""400516443"", ""400193370"", ""400516442"", ""401053411"", ""400960089"", ""400910415"") | UKDE PCD | PCD/DCD | TRUE | | FMRP2:7473305534138662912 Entity__Booking_Entity_SCI_FMID in ("10036430", "300084297", "300010782", "300011525", "10041903", "10037477", "10041902") && Instrument_Common__Murex_Product_Strategy in ("FX_PCD", "FX_DCD") && Entity__Counterparty_SCI_FMID not in ("400953656", "300010735", "400800797", "400933624", "400258208", "400963307", "400812227", "400800798", "400935870", "400178088", "300037428", "400111150", "400969140", "400917505", "400059979", "400174369", "300037798", "400948418", "400036336", "10037477", "400001378", "6", "10036647", "300011470", "5", "10036775", "2", "400035821", "8", "10036655", "9", "10075222", "4", "10036428", "7", "10036642", "10032025", "3", "400054737", "235003861", "10038345", "10036382", "10078716", "400095464", "400085753", "400045551", "400076756", "400032489", "300011525", "400028508", "300084297", "400909808", "400909807", "400089621", "400677737", "10041902", "400045057", "10036645", "300011345", "400066743", "400037785", "400452428", "400451508", "10036430", "400220273", "400899993", "400906330", "400058400", "400058398", "400130180", "400057714", "400058394", "10062461", "400107228", "400018439", "400041299", "400040747", "400040748", "400061773", "400037836", "400040412", "400037791", "400037921", "400037726", "400037729", "400037922", "400068942", "400054708", "400185419", "400038327", "15", "400044944", "400039759", "400040374", "400040633", "400054741", "400039882", "400046882", "400044796", "400063823", "400057870", "400040016", "400040017", "400040019", "400046458", "400037869", "400068898", "400037875", "400037876", "400044094", "400056963", "400063826", "400037877", "400057191", "400058543", "400040294", "400040027", "400037900", "400040285", "400057418", "400040006", "400071395", "400039582", "400060385", "400061872", "400037926", "400037940", "400040263", "400066464", "400037777", "400042544", "400076878", "400040039", "400037818", "400037820", "400037774", "400037944", "400040235", "400040231", "400037927", "400040044", "400040043", "400040045", "400007847", "400107029", "400058727", "400057346", "400039854", "400053597", "400016899", "400016959", "10020899", "400667486", "400798477", "400059347", "400075752", "400209000", "400229749", "400683682", "400130178", "400218197", "400090093", "400516443", "400193370", "400516442", "401053411", "400960089", "400910415") | Synthia/Gomathy | 2026-06-18 Aligned with Deepak and Gomathy 1.create a new rule and put 7 entities in booking entity list , 2.Instrument_Common.Murex_Product_Strategy in "FX_PCD" and "FX_DCD" 3.the other condition keep the same with the existing rule |
| 10 | KENYA, BAHRAIN, UGANDA, ZAMBIA, NIGERIA, GHANA, Qatar | NEW | 10036430 300084297 300010782 300011525 10041903 10037477 10041902 | AME RTRS | MAKER_CHECKER | NSTP | 1.Booking entity:10036430,300084297,300010782,300011525,10041903,10037477,10041902 2.the other condition is the same with the existing rule which AND Instrument_Common.Murex_Product_Family == ""CRD"" AND Instrument_Common.Murex_Product_Group == ""RTRS"" AND Entity.Counterparty_SCI_FMID not in (""400953656"", ""300010735"", ""400800797"", ""400933624"", ""400258208"", ""400963307"", ""400812227"", ""400800798"", ""400935870"", ""400178088"", ""300037428"", ""400111150"", ""400969140"", ""400917505"", ""400059979"", ""400174369"", ""300037798"", ""400948418"", ""400036336"", ""10037477"", ""400001378"", ""6"", ""10036647"", ""300011470"", ""5"", ""10036775"", ""2"", ""400035821"", ""8"", ""10036655"", ""9"", ""10075222"", ""4"", ""10036428"", ""7"", ""10036642"", ""10032025"", ""3"", ""400054737"", ""235003861"", ""10038345"", ""10036382"", ""10078716"", ""400095464"", ""400085753"", ""400045551"", ""400076756"", ""400032489"", ""300011525"", ""400028508"", ""300084297"", ""400909808"", ""400909807"", ""400089621"", ""400677737"", ""10041902"", ""400045057"", ""10036645"", ""300011345"", ""400066743"", ""400037785"", ""400452428"", ""400451508"", ""10036430"", ""400220273"", ""400899993"", ""400906330"", ""400058400"", ""400058398"", ""400130180"", ""400057714"", ""400058394"", ""10062461"", ""400107228"", ""400018439"", ""400041299"", ""400040747"", ""400040748"", ""400061773"", ""400037836"", ""400040412"", ""400037791"", ""400037921"", ""400037726"", ""400037729"", ""400037922"", ""400068942"", ""400054708"", ""400185419"", ""400038327"", ""15"", ""400044944"", ""400039759"", ""400040374"", ""400040633"", ""400054741"", ""400039882"", ""400046882"", ""400044796"", ""400063823"", ""400057870"", ""400040016"", ""400040017"", ""400040019"", ""400046458"", ""400037869"", ""400068898"", ""400037875"", ""400037876"", ""400044094"", ""400056963"", ""400063826"", ""400037877"", ""400057191"", ""400058543"", ""400040294"", ""400040027"", ""400037900"", ""400040285"", ""400057418"", ""400040006"", ""400071395"", ""400039582"", ""400060385"", ""400061872"", ""400037926"", ""400037940"", ""400040263"", ""400066464"", ""400037777"", ""400042544"", ""400076878"", ""400040039"", ""400037818"", ""400037820"", ""400037774"", ""400037944"", ""400040235"", ""400040231"", ""400037927"", ""400040044"", ""400040043"", ""400040045"", ""400007847"", ""400107029"", ""400058727"", ""400057346"", ""400039854"", ""400053597"", ""400016899"", ""400016959"", ""10020899"", ""400667486"", ""400798477"", ""400059347"", ""400075752"", ""400209000"", ""400229749"", ""400683682"", ""400130178"", ""400218197"", ""400090093"", ""400516443"", ""400193370"", ""400516442"", ""401053411"", ""400960089"", ""400910415"") | UKDE_RTRS | AME RTRS | TRUE | | FMRP2:7473345470881529856 Entity__Booking_Entity_SCI_FMID in ("10036430", "300084297", "300010782", "300011525", "10041903", "10037477", "10041902") && Instrument_Common__Murex_Product_Family == "CRD" && Instrument_Common__Murex_Product_Group == "RTRS" && Entity__Counterparty_SCI_FMID not in ("400953656", "300010735", "400800797", "400933624", "400258208", "400963307", "400812227", "400800798", "400935870", "400178088", "300037428", "400111150", "400969140", "400917505", "400059979", "400174369", "300037798", "400948418", "400036336", "10037477", "400001378", "6", "10036647", "300011470", "5", "10036775", "2", "400035821", "8", "10036655", "9", "10075222", "4", "10036428", "7", "10036642", "10032025", "3", "400054737", "235003861", "10038345", "10036382", "10078716", "400095464", "400085753", "400045551", "400076756", "400032489", "300011525", "400028508", "300084297", "400909808", "400909807", "400089621", "400677737", "10041902", "400045057", "10036645", "300011345", "400066743", "400037785", "400452428", "400451508", "10036430", "400220273", "400899993", "400906330", "400058400", "400058398", "400130180", "400057714", "400058394", "10062461", "400107228", "400018439", "400041299", "400040747", "400040748", "400061773", "400037836", "400040412", "400037791", "400037921", "400037726", "400037729", "400037922", "400068942", "400054708", "400185419", "400038327", "15", "400044944", "400039759", "400040374", "400040633", "400054741", "400039882", "400046882", "400044796", "400063823", "400057870", "400040016", "400040017", "400040019", "400046458", "400037869", "400068898", "400037875", "400037876", "400044094", "400056963", "400063826", "400037877", "400057191", "400058543", "400040294", "400040027", "400037900", "400040285", "400057418", "400040006", "400071395", "400039582", "400060385", "400061872", "400037926", "400037940", "400040263", "400066464", "400037777", "400042544", "400076878", "400040039", "400037818", "400037820", "400037774", "400037944", "400040235", "400040231", "400037927", "400040044", "400040043", "400040045", "400007847", "400107029", "400058727", "400057346", "400039854", "400053597", "400016899", "400016959", "10020899", "400667486", "400798477", "400059347", "400075752", "400209000", "400229749", "400683682", "400130178", "400218197", "400090093", "400516443", "400193370", "400516442", "401053411", "400960089", "400910415") | Synthia/Gomathy | 2026-06-18 Aligned with Deepak and Gomathy 1.create a new rule and put 7 entities in booking entity list 2.the other condition keep the same with the existing rule |
| 11 | KENYA, BAHRAIN, UGANDA, ZAMBIA, NIGERIA, GHANA, Qatar | NEW | 10036430 300084297 300010782 300011525 10041903 10037477 10041902 | AME LN_BR | MAKER_CHECKER | NSTP | 1.Booking entity:10036430,300084297,300010782,300011525,10041903,10037477,10041902 2.the other condition is the same with the existing rule which AND Instrument_Common.Murex_Product_Family == ""IRD"" AND Instrument_Common.Murex_Product_Group == ""LN_BR"" AND Entity.Counterparty_SCI_FMID not in (""400953656"", ""300010735"", ""400800797"", ""400933624"", ""400258208"", ""400963307"", ""400812227"", ""400800798"", ""400935870"", ""400178088"", ""300037428"", ""400111150"", ""400969140"", ""400917505"", ""400059979"", ""400174369"", ""300037798"", ""400948418"", ""400036336"", ""10037477"", ""400001378"", ""6"", ""10036647"", ""300011470"", ""5"", ""10036775"", ""2"", ""400035821"", ""8"", ""10036655"", ""9"", ""10075222"", ""4"", ""10036428"", ""7"", ""10036642"", ""10032025"", ""3"", ""400054737"", ""235003861"", ""10038345"", ""10036382"", ""10078716"", ""400095464"", ""400085753"", ""400045551"", ""400076756"", ""400032489"", ""300011525"", ""400028508"", ""300084297"", ""400909808"", ""400909807"", ""400089621"", ""400677737"", ""10041902"", ""400045057"", ""10036645"", ""300011345"", ""400066743"", ""400037785"", ""400452428"", ""400451508"", ""10036430"", ""400220273"", ""400899993"", ""400906330"", ""400058400"", ""400058398"", ""400130180"", ""400057714"", ""400058394"", ""10062461"", ""400107228"", ""400018439"", ""400041299"", ""400040747"", ""400040748"", ""400061773"", ""400037836"", ""400040412"", ""400037791"", ""400037921"", ""400037726"", ""400037729"", ""400037922"", ""400068942"", ""400054708"", ""400185419"", ""400038327"", ""15"", ""400044944"", ""400039759"", ""400040374"", ""400040633"", ""400054741"", ""400039882"", ""400046882"", ""400044796"", ""400063823"", ""400057870"", ""400040016"", ""400040017"", ""400040019"", ""400046458"", ""400037869"", ""400068898"", ""400037875"", ""400037876"", ""400044094"", ""400056963"", ""400063826"", ""400037877"", ""400057191"", ""400058543"", ""400040294"", ""400040027"", ""400037900"", ""400040285"", ""400057418"", ""400040006"", ""400071395"", ""400039582"", ""400060385"", ""400061872"", ""400037926"", ""400037940"", ""400040263"", ""400066464"", ""400037777"", ""400042544"", ""400076878"", ""400040039"", ""400037818"", ""400037820"", ""400037774"", ""400037944"", ""400040235"", ""400040231"", ""400037927"", ""400040044"", ""400040043"", ""400040045"", ""400007847"", ""400107029"", ""400058727"", ""400057346"", ""400039854"", ""400053597"", ""400016899"", ""400016959"", ""10020899"", ""400667486"", ""400798477"", ""400059347"", ""400075752"", ""400209000"", ""400229749"", ""400683682"", ""400130178"", ""400218197"", ""400090093"", ""400516443"", ""400193370"", ""400516442"", ""401053411"", ""400960089"", ""400910415"") | UKDE LN_BR | AME LN_BR | TRUE | | FMRP2:7473350011159035904 Entity__Booking_Entity_SCI_FMID in ("10036430", "300084297", "300010782", "300011525", "10041903", "10037477", "10041902") && Instrument_Common__Murex_Product_Family == "IRD" && Instrument_Common__Murex_Product_Group == "LN_BR" && Entity__Counterparty_SCI_FMID not in ("400953656", "300010735", "400800797", "400933624", "400258208", "400963307", "400812227", "400800798", "400935870", "400178088", "300037428", "400111150", "400969140", "400917505", "400059979", "400174369", "300037798", "400948418", "400036336", "10037477", "400001378", "6", "10036647", "300011470", "5", "10036775", "2", "400035821", "8", "10036655", "9", "10075222", "4", "10036428", "7", "10036642", "10032025", "3", "400054737", "235003861", "10038345", "10036382", "10078716", "400095464", "400085753", "400045551", "400076756", "400032489", "300011525", "400028508", "300084297", "400909808", "400909807", "400089621", "400677737", "10041902", "400045057", "10036645", "300011345", "400066743", "400037785", "400452428", "400451508", "10036430", "400220273", "400899993", "400906330", "400058400", "400058398", "400130180", "400057714", "400058394", "10062461", "400107228", "400018439", "400041299", "400040747", "400040748", "400061773", "400037836", "400040412", "400037791", "400037921", "400037726", "400037729", "400037922", "400068942", "400054708", "400185419", "400038327", "15", "400044944", "400039759", "400040374", "400040633", "400054741", "400039882", "400046882", "400044796", "400063823", "400057870", "400040016", "400040017", "400040019", "400046458", "400037869", "400068898", "400037875", "400037876", "400044094", "400056963", "400063826", "400037877", "400057191", "400058543", "400040294", "400040027", "400037900", "400040285", "400057418", "400040006", "400071395", "400039582", "400060385", "400061872", "400037926", "400037940", "400040263", "400066464", "400037777", "400042544", "400076878", "400040039", "400037818", "400037820", "400037774", "400037944", "400040235", "400040231", "400037927", "400040044", "400040043", "400040045", "400007847", "400107029", "400058727", "400057346", "400039854", "400053597", "400016899", "400016959", "10020899", "400667486", "400798477", "400059347", "400075752", "400209000", "400229749", "400683682", "400130178", "400218197", "400090093", "400516443", "400193370", "400516442", "401053411", "400960089", "400910415") | Synthia/Gomathy | 2026-06-18 Aligned with Deepak and Gomathy 1.create a new rule and put 7 entities in booking entity list 2.the other condition keep the same with the existing rule |
| 12 | DOHA,ZAMBIA | UPDATE | 300010782, 10041903 | DVP Strategy | MAKER_CHECKER | NSTP | Add 300010782,10041903 in the condition of counterparty not in the list | | DVP Strategy | FALSE | Instrument_Common__Murex_Product_Strategy in ("CCS_DVP", "CM_PMASIANFWDVP", "COM_AMES_DVP", "COM_BDF_DVP", "COM_BOE_DVP", "COM_JMUK_DVP", "COM_JMVF_DVP", "COM_LDN_DVP", "COM_OUTRGHT_DVP", "COM_RAND_DVP", "COM_SOUK_DVP", "COM_UBS_DVP", "COM_ZUR_DVP", "CR_RTM_CCS_DVP", "FX_PMTRF_DVP", "FX_TRF_DVP", "IR_AFR_DVP", "PAR FWD DVP", "PM_TRF_DVP", "PRC_OFFTAKE_DVP", "CM_PMASIANFWDP", "SGE_TRIPARTY_FW", "CCS_CORP_DVP", "CCS_FI_DVP") && Entity__Counterparty_SCI_FMID not in ("400953656", "300010735", "400800797", "400933624", "400258208", "400963307", "400812227", "400800798", "400935870", "400178088", "300037428", "400111150", "400969140", "400917505", "400059979", "400174369", "300037798", "400948418", "400036336", "10037477", "400001378", "6", "10036647", "300011470", "5", "10036775", "2", "400035821", "8", "10036655", "9", "10075222", "4", "10036428", "7", "10036642", "10032025", "3", "400054737", "235003861", "10038345", "10036382", "10078716", "400095464", "400085753", "400045551", "400076756", "400032489", "300011525", "400028508", "300084297", "400909808", "400909807", "400089621", "400677737", "10041902", "400045057", "10036645", "300011345", "400066743", "400037785", "400452428", "400451508", "10036430", "400220273", "400899993", "400906330", "400058400", "400058398", "400130180", "400057714", "400058394", "10062461", "400107228", "400018439", "400041299", "400040747", "400040748", "400061773", "400037836", "400040412", "400037791", "400037921", "400037726", "400037729", "400037922", "400068942", "400054708", "400185419", "400038327", "15", "400044944", "400039759", "400040374", "400040633", "400054741", "400039882", "400046882", "400044796", "400063823", "400057870", "400040016", "400040017", "400040019", "400046458", "400037869", "400068898", "400037875", "400037876", "400044094", "400056963", "400063826", "400037877", "400057191", "400058543", "400040294", "400040027", "400037900", "400040285", "400057418", "400040006", "400071395", "400039582", "400060385", "400061872", "400037926", "400037940", "400040263", "400066464", "400037777", "400042544", "400076878", "400040039", "400037818", "400037820", "400037774", "400037944", "400040235", "400040231", "400037927", "400040044", "400040043", "400040045", "400007847", "400107029", "400058727", "400057346", "400039854", "400053597", "400016899", "400016959", "10020899", "400667486", "400798477", "400059347", "400075752", "400209000", "400229749", "400683682", "400130178", "400218197", "400090093", "400516443", "400193370", "400516442", "401053411", "400960089") | FMRP2:7473204608231038976 Instrument_Common__Murex_Product_Strategy in ("CCS_DVP", "CM_PMASIANFWDVP", "COM_AMES_DVP", "COM_BDF_DVP", "COM_BOE_DVP", "COM_JMUK_DVP", "COM_JMVF_DVP", "COM_LDN_DVP", "COM_OUTRGHT_DVP", "COM_RAND_DVP", "COM_SOUK_DVP", "COM_UBS_DVP", "COM_ZUR_DVP", "CR_RTM_CCS_DVP", "FX_PMTRF_DVP", "FX_TRF_DVP", "IR_AFR_DVP", "PAR FWD DVP", "PM_TRF_DVP", "PRC_OFFTAKE_DVP", "CM_PMASIANFWDP", "SGE_TRIPARTY_FW", "CCS_CORP_DVP", "CCS_FI_DVP") && Entity__Counterparty_SCI_FMID not in ("400953656", "300010735", "400800797", "400933624", "400258208", "400963307", "400812227", "400800798", "400935870", "400178088", "300037428", "400111150", "400969140", "400917505", "400059979", "400174369", "300037798", "400948418", "400036336", "10037477", "400001378", "6", "10036647", "300011470", "5", "10036775", "2", "400035821", "8", "10036655", "9", "10075222", "4", "10036428", "7", "10036642", "10032025", "3", "400054737", "235003861", "10038345", "10036382", "10078716", "400095464", "400085753", "400045551", "400076756", "400032489", "300011525", "400028508", "300084297", "400909808", "400909807", "400089621", "400677737", "10041902", "400045057", "10036645", "300011345", "400066743", "400037785", "400452428", "400451508", "10036430", "400220273", "400899993", "400906330", "400058400", "400058398", "400130180", "400057714", "400058394", "10062461", "400107228", "400018439", "400041299", "400040747", "400040748", "400061773", "400037836", "400040412", "400037791", "400037921", "400037726", "400037729", "400037922", "400068942", "400054708", "400185419", "400038327", "15", "400044944", "400039759", "400040374", "400040633", "400054741", "400039882", "400046882", "400044796", "400063823", "400057870", "400040016", "400040017", "400040019", "400046458", "400037869", "400068898", "400037875", "400037876", "400044094", "400056963", "400063826", "400037877", "400057191", "400058543", "400040294", "400040027", "400037900", "400040285", "400057418", "400040006", "400071395", "400039582", "400060385", "400061872", "400037926", "400037940", "400040263", "400066464", "400037777", "400042544", "400076878", "400040039", "400037818", "400037820", "400037774", "400037944", "400040235", "400040231", "400037927", "400040044", "400040043", "400040045", "400007847", "400107029", "400058727", "400057346", "400039854", "400053597", "400016899", "400016959", "10020899", "400667486", "400798477", "400059347", "400075752", "400209000", "400229749", "400683682", "400130178", "400218197", "400090093", "400516443", "400193370", "400516442", "401053411", "400960089", "300010782", "10041903") | Synthia/Gomathy | 2026-06-18 Aligned with Deepak and Gomathy 1.update existing rule ,add 300010782, 10041903 in the condition of counterparty not in |
| 13 | KENYA, BAHRAIN, UGANDA, ZAMBIA, NIGERIA, GHANA, Qatar | NEW | 10036430 300084297 300010782 300011525 10041903 10037477 10041902 | AME Structured Swap | MAKER_CHECKER | NSTP | 1.Booking entity:10036430,300084297,300010782,300011525,10041903,10037477,10041902 2.the other condition is the same with the existing rule AND Instrument_Common.Murex_Product_Typology == ""Structured Swap"" AND Entity.Counterparty_SCI_FMID not in (""400953656"", ""300010735"", ""400800797"", ""400933624"", ""400258208"", ""400963307"", ""400812227"", ""400800798"", ""400935870"", ""400178088"", ""300037428"", ""400111150"", ""400969140"", ""400917505"", ""400059979"", ""400174369"", ""300037798"", ""400948418"", ""400036336"", ""10037477"", ""400001378"", ""6"", ""10036647"", ""300011470"", ""5"", ""10036775"", ""2"", ""400035821"", ""8"", ""10036655"", ""9"", ""10075222"", ""4"", ""10036428"", ""7"", ""10036642"", ""10032025"", ""3"", ""400054737"", ""235003861"", ""10038345"", ""10036382"", ""10078716"", ""400095464"", ""400085753"", ""400045551"", ""400076756"", ""400032489"", ""300011525"", ""400028508"", ""300084297"", ""400909808"", ""400909807"", ""400089621"", ""400677737"", ""10041902"", ""400045057"", ""10036645"", ""300011345"", ""400066743"", ""400037785"", ""400452428"", ""400451508"", ""10036430"", ""400220273"", ""400899993"", ""400906330"", ""400058400"", ""400058398"", ""400130180"", ""400057714"", ""400058394"", ""10062461"", ""400107228"", ""400018439"", ""400041299"", ""400040747"", ""400040748"", ""400061773"", ""400037836"", ""400040412"", ""400037791"", ""400037921"", ""400037726"", ""400037729"", ""400037922"", ""400068942"", ""400054708"", ""400185419"", ""400038327"", ""15"", ""400044944"", ""400039759"", ""400040374"", ""400040633"", ""400054741"", ""400039882"", ""400046882"", ""400044796"", ""400063823"", ""400057870"", ""400040016"", ""400040017"", ""400040019"", ""400046458"", ""400037869"", ""400068898"", ""400037875"", ""400037876"", ""400044094"", ""400056963"", ""400063826"", ""400037877"", ""400057191"", ""400058543"", ""400040294"", ""400040027"", ""400037900"", ""400040285"", ""400057418"", ""400040006"", ""400071395"", ""400039582"", ""400060385"", ""400061872"", ""400037926"", ""400037940"", ""400040263"", ""400066464"", ""400037777"", ""400042544"", ""400076878"", ""400040039"", ""400037818"", ""400037820"", ""400037774"", ""400037944"", ""400040235"", ""400040231"", ""400037927"", ""400040044"", ""400040043"", ""400040045"", ""400007847"", ""400107029"", ""400058727"", ""400057346"", ""400039854"", ""400053597"", ""400016899"", ""400016959"", ""10020899"", ""400667486"", ""400798477"", ""400059347"", ""400075752"", ""400209000"", ""400229749"", ""400683682"", ""400130178"", ""400218197"", ""400090093"", ""400516443"", ""400193370"", ""400516442"", ""401053411"", ""400960089"", ""400910415"") | UKDE Structured Swap | AME Structured Swap | TRUE | | FMRP2:7473350706975145984 Entity__Booking_Entity_SCI_FMID in ("10036430", "300084297", "300010782", "300011525", "10041903", "10037477", "10041902") && Instrument_Common__Murex_Product_Typology == "Structured Swap" && Entity__Counterparty_SCI_FMID not in ("400953656", "300010735", "400800797", "400933624", "400258208", "400963307", "400812227", "400800798", "400935870", "400178088", "300037428", "400111150", "400969140", "400917505", "400059979", "400174369", "300037798", "400948418", "400036336", "10037477", "400001378", "6", "10036647", "300011470", "5", "10036775", "2", "400035821", "8", "10036655", "9", "10075222", "4", "10036428", "7", "10036642", "10032025", "3", "400054737", "235003861", "10038345", "10036382", "10078716", "400095464", "400085753", "400045551", "400076756", "400032489", "300011525", "400028508", "300084297", "400909808", "400909807", "400089621", "400677737", "10041902", "400045057", "10036645", "300011345", "400066743", "400037785", "400452428", "400451508", "10036430", "400220273", "400899993", "400906330", "400058400", "400058398", "400130180", "400057714", "400058394", "10062461", "400107228", "400018439", "400041299", "400040747", "400040748", "400061773", "400037836", "400040412", "400037791", "400037921", "400037726", "400037729", "400037922", "400068942", "400054708", "400185419", "400038327", "15", "400044944", "400039759", "400040374", "400040633", "400054741", "400039882", "400046882", "400044796", "400063823", "400057870", "400040016", "400040017", "400040019", "400046458", "400037869", "400068898", "400037875", "400037876", "400044094", "400056963", "400063826", "400037877", "400057191", "400058543", "400040294", "400040027", "400037900", "400040285", "400057418", "400040006", "400071395", "400039582", "400060385", "400061872", "400037926", "400037940", "400040263", "400066464", "400037777", "400042544", "400076878", "400040039", "400037818", "400037820", "400037774", "400037944", "400040235", "400040231", "400037927", "400040044", "400040043", "400040045", "400007847", "400107029", "400058727", "400057346", "400039854", "400053597", "400016899", "400016959", "10020899", "400667486", "400798477", "400059347", "400075752", "400209000", "400229749", "400683682", "400130178", "400218197", "400090093", "400516443", "400193370", "400516442", "401053411", "400960089", "400910415") | Synthia/Gomathy | 2026-06-18 Aligned with Deepak and Gomathy 1.create a new rule and put 7 entities in booking entity list 2.the other condition keep the same with the existing rule |
| 14 | KENYA，ZAMBIA，GHANA，UGANDA | UPDATE | 300011525 10041903 10037477 10041902 | INO INR LEI REQUIRED | MAKER_CHECKER | NSTP | add 300011525,10041903,10037477,10041902 in Entity.Booking_Entity_SCI_FMID list | | WHT KL | FALSE | Entity__Booking_Entity_SCI_FMID in ("10036430", "6", "400054741", "400095464", "400130178", "400130180", "400001378", "401053411", "400090093", "10020899", "10032025", "235003861", "10062461", "10078716", "400220273", "400899993", "400075752", "400209000", "400229749", "400085753", "400683682", "400218197", "400667486", "400798477", "400185419", "400045551", "300010782", "5", "400054708", "10041530", "2", "8", "400032489", "10036655", "9", "400093619", "10036428", "400018439", "300084297", "300011345", "300089409", "400057714", "300075472", "400677737", "10036642", "400451508", "40045248", "400054737", "400516443", "10038345", "400041070", "10036382", "400516442", "400193370") && Cashflow__Payment_Currency in ("INO", "INR") && Cashflow__Payment_Amount >= 500000000 | FMRP2:7473207741241819136 Entity__Booking_Entity_SCI_FMID in ("10036430", "6", "400054741", "400095464", "400130178", "400130180", "400001378", "401053411", "400090093", "10020899", "10032025", "235003861", "10062461", "10078716", "400220273", "400899993", "400075752", "400209000", "400229749", "400085753", "400683682", "400218197", "400667486", "400798477", "400185419", "400045551", "300010782", "5", "400054708", "10041530", "2", "8", "400032489", "10036655", "9", "400093619", "10036428", "400018439", "300084297", "300011345", "300089409", "400057714", "300075472", "400677737", "10036642", "400451508", "40045248", "400054737", "400516443", "10038345", "400041070", "10036382", "400516442", "400193370", "300011525", "10041903", "10037477", "10041902") && Cashflow__Payment_Currency in ("INO", "INR") && Cashflow__Payment_Amount >= 500000000 | Synthia/Gomathy | 2026-06-18 Aligned with Deepak and Gomathy 1.update existing rule ,add 300011525 10041903 10037477 10041902 in the booking entity condition |
| 15 | DOHA,ZAMBIA | UPDATE | 300010782 10041903 | Structure Trade | MAKER_CHECKER | NSTP | 1.add 300010782,10041903 in the condition of counterparty not in the list | | Structure Trade | TRUE | Cashflow__Murex_Structure_Id != null && Cashflow__Murex_Structure_Id != "" && Cashflow__Murex_Structure_Id != "0" && Entity__Counterparty_SCI_FMID not in ("400953656", "300010735", "400800797", "400933624", "400258208", "400963307", "400812227", "400800798", "400935870", "400178088", "300037428", "400111150", "400969140", "400917505", "400059979", "400174369", "300037798", "400948418", "400036336", "10037477", "400001378", "6", "10036647", "300011470", "5", "10036775", "2", "400035821", "8", "10036655", "9", "10075222", "4", "10036428", "7", "10036642", "10032025", "3", "400054737", "235003861", "10038345", "10036382", "10078716", "400095464", "400085753", "400045551", "400076756", "400032489", "300011525", "400028508", "300084297", "400909808", "400909807", "400089621", "400677737", "10041902", "400045057", "10036645", "300011345", "400066743", "400037785", "400452428", "400451508", "10036430", "400220273", "400899993", "400906330", "400058400", "400058398", "400130180", "400057714", "400058394", "10062461", "400107228", "400018439", "400041299", "400040747", "400040748", "400061773", "400037836", "400040412", "400037791", "400037921", "400037726", "400037729", "400037922", "400068942", "400054708", "400185419", "400038327", "15", "400044944", "400039759", "400040374", "400040633", "400054741", "400039882", "400046882", "400044796", "400063823", "400057870", "400040016", "400040017", "400040019", "400046458", "400037869", "400068898", "400037875", "400037876", "400044094", "400056963", "400063826", "400037877", "400057191", "400058543", "400040294", "400040027", "400037900", "400040285", "400057418", "400040006", "400071395", "400039582", "400060385", "400061872", "400037926", "400037940", "400040263", "400066464", "400037777", "400042544", "400076878", "400040039", "400037818", "400037820", "400037774", "400037944", "400040235", "400040231", "400037927", "400040044", "400040043", "400040045", "400007847", "400107029", "400058727", "400057346", "400039854", "400053597", "400016899", "400016959", "10020899", "400667486", "400798477", "400059347", "400075752", "400209000", "400229749", "400683682", "400130178", "400218197", "400090093", "400516443", "400193370", "400516442", "401053411", "400521212", "400891890", "400960089", "400910415", "400949160", "10036217", "400017653", "400026648", "401025340", "401042994", "401048225", "401054785", "401030665", "401026106", "400926855", "10036610", "400122527", "401038183", "401024508", "400181959", "400915596", "400891542", "400891543", "400768808", "400685516", "401069581", "401034041", "400097656", "400801131", "400715883", "400655667", "400638407", "400814579", "400885770", "400897651", "400206235", "400678001", "401069905", "400853579", "400490402", "10037300", "10020930", "300068460", "10018319", "400969392", "401072585", "401077111", "401018936", "400988287", "400635099", "400217058", "400926856", "401049239") && Instrument_Common__Murex_Product_Typology != "NDF" && Entity__Booking_Entity_SCI_FMID not in ("2", "300075472", "10038345", "300011345", "400001378", "400220273", "400054741", "400075752", "400095464", "400209000", "400229749", "400054708", "400899993", "10036382", "400085753", "400683682", "400130178", "400218197", "400667486", "400090093", "10020899", "400130180", "400057714", "10036642", "400677737", "400798477", "10032025", "400054737", "400516443", "235003861", "400185419", "10062461", "400193370", "400516442", "10078716", "401053411", "400451508") | FMRP2:7473210995235340288 Cashflow__Murex_Structure_Id != null && Cashflow__Murex_Structure_Id != "" && Cashflow__Murex_Structure_Id != "0" && Entity__Counterparty_SCI_FMID not in ("400953656", "300010735", "400800797", "400933624", "400258208", "400963307", "400812227", "400800798", "400935870", "400178088", "300037428", "400111150", "400969140", "400917505", "400059979", "400174369", "300037798", "400948418", "400036336", "10037477", "400001378", "6", "10036647", "300011470", "5", "10036775", "2", "400035821", "8", "10036655", "9", "10075222", "4", "10036428", "7", "10036642", "10032025", "3", "400054737", "235003861", "10038345", "10036382", "10078716", "400095464", "400085753", "400045551", "400076756", "400032489", "300011525", "400028508", "300084297", "400909808", "400909807", "400089621", "400677737", "10041902", "400045057", "10036645", "300011345", "400066743", "400037785", "400452428", "400451508", "10036430", "400220273", "400899993", "400906330", "400058400", "400058398", "400130180", "400057714", "400058394", "10062461", "400107228", "400018439", "400041299", "400040747", "400040748", "400061773", "400037836", "400040412", "400037791", "400037921", "400037726", "400037729", "400037922", "400068942", "400054708", "400185419", "400038327", "15", "400044944", "400039759", "400040374", "400040633", "400054741", "400039882", "400046882", "400044796", "400063823", "400057870", "400040016", "400040017", "400040019", "400046458", "400037869", "400068898", "400037875", "400037876", "400044094", "400056963", "400063826", "400037877", "400057191", "400058543", "400040294", "400040027", "400037900", "400040285", "400057418", "400040006", "400071395", "400039582", "400060385", "400061872", "400037926", "400037940", "400040263", "400066464", "400037777", "400042544", "400076878", "400040039", "400037818", "400037820", "400037774", "400037944", "400040235", "400040231", "400037927", "400040044", "400040043", "400040045", "400007847", "400107029", "400058727", "400057346", "400039854", "400053597", "400016899", "400016959", "10020899", "400667486", "400798477", "400059347", "400075752", "400209000", "400229749", "400683682", "400130178", "400218197", "400090093", "400516443", "400193370", "400516442", "401053411", "400521212", "400891890", "400960089", "400910415", "400949160", "10036217", "400017653", "400026648", "401025340", "401042994", "401048225", "401054785", "401030665", "401026106", "400926855", "10036610", "400122527", "401038183", "401024508", "400181959", "400915596", "400891542", "400891543", "400768808", "400685516", "401069581", "401034041", "400097656", "400801131", "400715883", "400655667", "400638407", "400814579", "400885770", "400897651", "400206235", "400678001", "401069905", "400853579", "400490402", "10037300", "10020930", "300068460", "10018319", "400969392", "401072585", "401077111", "401018936", "400988287", "400635099", "400217058", "400926856", "401049239", "300010782", "10041903") && Instrument_Common__Murex_Product_Typology != "NDF" && Entity__Booking_Entity_SCI_FMID not in ("2", "300075472", "10038345", "300011345", "400001378", "400220273", "400054741", "400075752", "400095464", "400209000", "400229749", "400054708", "400899993", "10036382", "400085753", "400683682", "400130178", "400218197", "400667486", "400090093", "10020899", "400130180", "400057714", "10036642", "400677737", "400798477", "10032025", "400054737", "400516443", "235003861", "400185419", "10062461", "400193370", "400516442", "10078716", "401053411", "400451508") | Synthia/Gomathy | 2026-06-18 Aligned with Deepak and Gomathy 1.update existing rule , 300010782 10041903 are mising in the counterparty list ,add 300010782 10041903 in the counterparty list , |
| 16 | KENYA, BAHRAIN, UGANDA, ZAMBIA, NIGERIA, GHANA, Qatar | UPDATE | 10036430 300084297 300010782 300011525 10041903 10037477 10041902 | CRD RTRS | MAKER_CHECKER | NSTP | 1.add 7 entities in the booking entity list | | CRD RTRS - Structure Trade | FALSE | Entity__Booking_Entity_SCI_FMID in ("400451508", "400452428", "9", "6", "5", "400045551", "400032489") && Instrument_Common__Murex_Product_Family == "CRD" && Instrument_Common__Murex_Product_Group == "RTRS" && fmEntity__fmAccount__fmType not in ("INTECOM", "INTEBCH", "INTLACC") | FMRP:7473212863967592448 Entity__Booking_Entity_SCI_FMID in ("400451508", "400452428", "9", "6", "5", "400045551", "400032489", "10036430", "300084297", "300010782", "300011525", "10041903", "10037477", "10041902") && Instrument_Common__Murex_Product_Family == "CRD" && Instrument_Common__Murex_Product_Group == "RTRS" && fmEntity__fmAccount__fmType not in ("INTECOM", "INTEBCH", "INTLACC") | Synthia/Gomathy | 2026-06-18 Aligned with Deepak and Gomathy 1.update existing rule and add 7 entities in the booking entities |
| 17 | NIGERIA,DOHA,ZAMBIA | UPDATE | 300084297 300010782 10041903 | MUREX SCF | MAKER_CHECKER | NSTP | 1.add 300084297,300010782,10041903 in the condition of Entity.Counterparty_SCI_FMID not in | | MUREX SCF | TRUE | Entity__Counterparty_SCI_FMID not in ("400953656", "300010735", "400800797", "400258208", "400963307", "400812227", "400800798", "400935870", "400178088", "300037428", "400111150", "400917505", "400059979", "300037798", "400948418", "400036336", "10037477", "400001378", "6", "10036647", "300011470", "5", "10036775", "2", "400035821", "8", "10036655", "9", "10075222", "4", "10036428", "7", "10036642", "10032025", "3", "400054737", "235003861", "10038345", "10036382", "10078716", "400095464", "400085753", "400045551", "400076756", "400032489", "300011525", "400028508", "400909808", "400909807", "400089621", "400677737", "10041902", "400045057", "10036645", "300011345", "400066743", "400037785", "400452428", "400451508", "10036430", "400220273", "400899993", "400906330", "400058400", "400058398", "400130180", "400057714", "400058394", "10062461", "400107228", "400018439", "400041299", "400040747", "400040748", "400061773", "400037836", "400040412", "400037791", "400037921", "400037726", "400037729", "400037922", "400068942", "400054708", "400185419", "400038327", "15", "400044944", "400039759", "400040374", "400040633", "400054741", "400039882", "400046882", "400044796", "400063823", "400057870", "400040016", "400040017", "400040019", "400046458", "400037869", "400068898", "400037875", "400037876", "400044094", "400056963", "400063826", "400037877", "400057191", "400058543", "400040294", "400040027", "400037900", "400040285", "400057418", "400040006", "400071395", "400039582", "400060385", "400061872", "400037926", "400037940", "400040263", "400066464", "400037777", "400042544", "400076878", "400040039", "400037818", "400037820", "400037774", "400037944", "400040235", "400040231", "400037927", "400040044", "400040043", "400040045", "400007847", "400107029", "400058727", "400039854", "400053597", "400016899", "400016959", "10020899", "400667486", "400798477", "400059347", "400075752", "400209000", "400229749", "400683682", "400130178", "400218197", "400090093", "400516443", "400193370", "400516442", "401053411", "400960089", "400910415", "400016898") && (Instrument_Common__ISDA_Taxonomy matches "^Simple Cashflow.*" || Instrument_Common__ISDA_Taxonomy == "SCF|SCF|SCF") | FMRP2:7473215056204464128 Entity__Counterparty_SCI_FMID not in ("400953656", "300010735", "400800797", "400258208", "400963307", "400812227", "400800798", "400935870", "400178088", "300037428", "400111150", "400917505", "400059979", "300037798", "400948418", "400036336", "10037477", "400001378", "6", "10036647", "300011470", "5", "10036775", "2", "400035821", "8", "10036655", "9", "10075222", "4", "10036428", "7", "10036642", "10032025", "3", "400054737", "235003861", "10038345", "10036382", "10078716", "400095464", "400085753", "400045551", "400076756", "400032489", "300011525", "400028508", "400909808", "400909807", "400089621", "400677737", "10041902", "400045057", "10036645", "300011345", "400066743", "400037785", "400452428", "400451508", "10036430", "400220273", "400899993", "400906330", "400058400", "400058398", "400130180", "400057714", "400058394", "10062461", "400107228", "400018439", "400041299", "400040747", "400040748", "400061773", "400037836", "400040412", "400037791", "400037921", "400037726", "400037729", "400037922", "400068942", "400054708", "400185419", "400038327", "15", "400044944", "400039759", "400040374", "400040633", "400054741", "400039882", "400046882", "400044796", "400063823", "400057870", "400040016", "400040017", "400040019", "400046458", "400037869", "400068898", "400037875", "400037876", "400044094", "400056963", "400063826", "400037877", "400057191", "400058543", "400040294", "400040027", "400037900", "400040285", "400057418", "400040006", "400071395", "400039582", "400060385", "400061872", "400037926", "400037940", "400040263", "400066464", "400037777", "400042544", "400076878", "400040039", "400037818", "400037820", "400037774", "400037944", "400040235", "400040231", "400037927", "400040044", "400040043", "400040045", "400007847", "400107029", "400058727", "400039854", "400053597", "400016899", "400016959", "10020899", "400667486", "400798477", "400059347", "400075752", "400209000", "400229749", "400683682", "400130178", "400218197", "400090093", "400516443", "400193370", "400516442", "401053411", "400960089", "400910415", "300010782", "10041903", "300084297") && (Instrument_Common__ISDA_Taxonomy matches "^Simple Cashflow.*" || Instrument_Common__ISDA_Taxonomy == "SCF|SCF|SCF") | Synthia/Gomathy | 2026-06-18 Aligned with Deepak and Gomathy 1.update existing rule and add 300084297 300010782 10041903 in the condition of counterparty not in |
| 18 | TANZANIA | NEW | 10040387 | TZ NSTP | MAKER_CHECKER | NSTP | booking entity is 10040387 counterparty anything | | TZ NSTP | TRUE | | FMRP2:7492890048986910720 Entity.Booking_Entity_SCI_FMID == "10040387" | | 2026-08-11 Requested by TZ user and Deepak |

## Cashflow Suppression

| | Country | FMID | Rule Condition | Action | Rule Reason | Pre Rule | Post Rule | Requested by | Comment |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Tranche1 countries | 300011525-KE 10041903-ZM 10040387-TZ 10036647-LK 10022098-LK 10041530-VN 10036655-PK 300011470-BD | Add tranche1 country in the list | UPDATE | Non FMRP entities | Entity__Booking_Entity_SCI_FMID not in ("400001378", "10020899", "235003861", "10078716", "10036642", "10062461", "10032025", "400054708", "400054737", "400054741", "400057714", "400075752", "400085753", "400090093", "400095464", "400130180", "400130178", "400185419", "400193370", "400209000", "400218197", "400220273", "400229749", "400516443", "400516442", "400667486", "400677737", "400683682", "400798477", "400899993", "300036368", "3", "400452428", "400451508", "4", "400960089", "9", "400093619", "401036553", "400991880", "400007847", "10075222", "400041070", "400906330", "6", "2", "10038345", "300011345", "300075472", "401053411", "400018439", "5", "8", "10036428", "7", "10036382", "400032489", "400045551", "400077978", "300089409", "400910415", "300010730") && Trade_Original_Source_System_Name not matches "(?i)^LOANIQ$" | Entity__Booking_Entity_SCI_FMID not in ("400001378", "10020899", "235003861", "10078716", "10036642", "10062461", "10032025", "400054708", "400054737", "400054741", "400057714", "400075752", "400085753", "400090093", "400095464", "400130180", "400130178", "400185419", "400193370", "400209000", "400218197", "400220273", "400229749", "400516443", "400516442", "400667486", "400677737", "400683682", "400798477", "400899993", "300036368", "3", "400452428", "400451508", "4", "400960089", "9", "400093619", "401036553", "400991880", "400007847", "10075222", "400041070", "400906330", "401053411", "300075472", "6", "300011345", "2", "10038345", "400018439", "5", "8", "10036428", "7", "10036382", "400032489", "400045551", "300089409", "400910415", "300011525", "10041903", "10040387","10036647", "10022098", "10041530", "10036655", "300011470", "10036645") && Trade_Original_Source_System_Name not matches "(?i)^LOANIQ$" | | 2026-06-16 for the other 6 entities except QA-SLQTE ,need to add in this list 2026-06-15 Aligned during the call with Deepak and Synthia/Gomathy ,add these 7 entities in the list(KENYA, BAHRAIN, UGANDA, ZAMBIA, NIGERIA, GHANA, Qatar-DOHA,) 2026-03-09 Approved by Sumita ,but Sumita need to confirm with Dinesh |
| 2 | Tranche2 countries | 10036430-BH 300010782-QA-DOHA 401081696-QA-SLATE(should be cashflow suppressed,no need to add in this rule) 10041902-UG 10037477-GH 300084297-NG | Add tranche2 country in the list | UPDATE | Non FMRP entities | Entity__Booking_Entity_SCI_FMID not in ("400001378", "10020899", "235003861", "10078716", "10036642", "10062461", "10032025", "400054708", "400054737", "400054741", "400057714", "400075752", "400085753", "400090093", "400095464", "400130180", "400130178", "400185419", "400193370", "400209000", "400218197", "400220273", "400229749", "400516443", "400516442", "400667486", "400677737", "400683682", "400798477", "400899993", "300036368", "3", "400452428", "400451508", "4", "400960089", "9", "400093619", "401036553", "400991880", "400007847", "10075222", "400041070", "400906330", "401053411", "300075472", "6", "300011345", "2", "10038345", "400018439", "5", "8", "10036428", "7", "10036382", "400032489", "400045551", "300089409", "400910415") && Trade_Original_Source_System_Name not matches "(?i)^LOANIQ$" | Entity__Booking_Entity_SCI_FMID not in ("400001378", "10020899", "235003861", "10078716", "10036642", "10062461", "10032025", "400054708", "400054737", "400054741", "400057714", "400075752", "400085753", "400090093", "400095464", "400130180", "400130178", "400185419", "400193370", "400209000", "400218197", "400220273", "400229749", "400516443", "400516442", "400667486", "400677737", "400683682", "400798477", "400899993", "300036368", "3", "400452428", "400451508", "4", "400960089", "9", "400093619", "401036553", "400991880", "400007847", "10075222", "400041070", "400906330", "401053411", "300075472", "6", "300011345", "2", "10038345", "400018439", "5", "8", "10036428", "7", "10036382", "400032489", "400045551", "300089409", "400910415", "10036430", "300010782", "10041902", "10037477", "300084297", "10036645") && Trade_Original_Source_System_Name not matches "(?i)^LOANIQ$" | | |
| 3 | BAHRAIN & QATAR-DOHA | 10036430 300010782 | 1. Booking_Entity:10036430,300010782 2. Counterparty FMID : 10075222 3. Currency : XAU, XAG, XPT, XPD | NEW | COM METAL | | FMRP2:7472535286223421440 (Entity__Booking_Entity_SCI_FMID in ("10036430", "300010782") && Cashflow__Payment_Currency in ("XAU", "XAG", "XPT", "XPD") && Entity__Counterparty_SCI_FMID == "10075222") | Sumita/Gomathy | 2026-06-16 Aligned with Sumita .can use this new rule to cover the BH cashflow suppression rule 2026-06-15 Aligned during the call with Deepak and Synthia/Gomathy ,can create a new rule |
| 4 | KENYA, BAHRAIN, UGANDA, ZAMBIA, NIGERIA, GHANA, Qatar-DOHA | 10036430 300084297 300010782 300011525 10041903 10037477 10041902 | 1.Booking entityin (10036430,300084297,300010782,300011525,10041903,10037477,10041902) 2.Counterparty in (400795971, 400058727, 400009156, 300036053,400009154,300079654) Counterparty FMID : SUPPDONOT/LDN 400058727 INTL/ALM DESK 400009156 XVAOMNBUS/LDN 400795971 INTL/FWD DESK 400009154 INTL/ALM 300036053 INTL*SPOT DESK 300079654 | NEW | INTERNAL CPTY | | FMRP2: 7472533966521257984 Entity__Booking_Entity_SCI_FMID in ("10036430", "300084297", "300010782", "300011525", "10041903", "10037477", "10041902") && Entity__Counterparty_SCI_FMID in ("400795971", "400058727", "400009156", "300036053", "400009154", "300079654") | Synthia/Gomathy | 2026-06-15 Aligned during the call with Deepak and Synthia/Gomathy ,can create a new rule |
| 5 | KENYA, BAHRAIN, UGANDA, ZAMBIA, NIGERIA, GHANA, Qatar-DOHA | 10036430 300084297 300010782 300011525 10041903 10037477 10041902 | 1.Booking entityin (10036430,300084297,300010782,300011525,10041903,10037477,10041902) 2.Currency: XAU, XAG, XPT, XPD | NEW | PM trades | | FMRP2: 7472534672435204096 Entity__Booking_Entity_SCI_FMID in ("10036430", "300084297", "300010782", "300011525", "10041903", "10037477", "10041902") && Cashflow__Payment_Currency in ("XAG", "XAU", "XPT", "XPD") | Synthia/Gomathy | 2026-06-15 Aligned during the call with Deepak and Synthia/Gomathy ,can create a new rule |
| 6 | Vietnam | 10041530 | 1. Counterpart FMID : 401052296, 401056396 2. Currency : ALL 3. Instrument_Common__Murex_Product_Group : "LN_BR | NEW | Vietnam LNBR | | FMRP2:7465577874616668160 Entity__Booking_Entity_SCI_FMID == "10041530" && Entity__Counterparty_SCI_FMID in ("401052296", "401056396") && Instrument_Common__Murex_Product_Group == "LN_BR" | Sumita | 2026-05-27 offline confirmed with sumita ,can create a new rule ![image-2026-6-23_15-6-16.png](attachments/image-2026-6-23_15-6-16.png) |
| 7 | SRI LANKA | 10036647 | 300036053,400009156,400009154,400795971 | NEW | Internal Deals | | FMRP2:7450084939641073664 Entity__Booking_Entity_SCI_FMID in ("10036647", "10022098") && Entity__Counterparty_SCI_FMID in ("300036053", "400009156", "400009154", "400795971") | Shalini | 2026-03-04 Reviewed during the call .Agreed by Dinesh | FM CODE | FMID | | --- | --- | | INTL*ALM | 300036053 | | INTL ALM DESK | 400009156 | | INTL*FWD DESKbun | 400009154 | | XVA OMNIBUS*LDN | 400795971 | |
| FM CODE | FMID |
| INTL*ALM | 300036053 |
| INTL ALM DESK | 400009156 |
| INTL*FWD DESKbun | 400009154 |
| XVA OMNIBUS*LDN | 400795971 |
| 8 | 10022098 | 300036053,400009156,400009154,400795971 | |
| 9 | TANZANIA | 10040387 | Request by Simon Booking entity is 10040387 counterparty is 400795971(XVAOMNBUS/LDN) | NEW | XVA Omnibus | | FMRP2:7462766112282480640 Entity__Booking_Entity_SCI_FMID == "10040387" && Entity__Counterparty_SCI_FMID == "400795971" | Simon | 2026-05-05 approved by Deepak via group chat,no need to add isda |

# STRATEGIC_FM_LIST

When generate swift message ,will check if the entities in below list ,if in ,will generate swift message

Because  below entity will be in cashflow suppressed ,so no need to config in STRATEGIC_FM_LIST,for the other manual entities ,need to add fmid in this strategic _fm_list

| SLATE_QFC | 401081696 | SLATE ONE LLC*DOH |
| --- | --- | --- |

**STRATEGIC_FM_LIST: **

<details>
<summary>Expand Details</summary>

401036553|400991880|400910415|400007847|400018439|5|8|10036428|7|10036382|400032489|400045551|300089409|6|2|10038345|300011345|

300075472|10075222|400041070|400906330|300036368|3|400452428|400451508|9|400093619|4|400960089|400001378|400054741|400220273|

400899993|400075752|400095464|400209000|400677737|400229749|400054708|400130178|400085753|400683682|400218197|400667486|

400090093|400130180|10020899|400057714|10036642|400054737|400798477|10032025|235003861|400516443|400185419|400193370|

10062461|10078716|400516442|401053411

</details>

# ORIGINAL SYSTEM TAG

If entity in the FM_LIST or source is from ORIGINAL_SYSTEM_TAG, will send to Razor

2026-01-20  Confirmed with @Arockia Dinesh  ,all the manual entities will not send to Razor ,so no need to change  ORIGINAL_SYSTME_TAG:LOANIQ

# LMS feed

2026-08-13 CPT of Tranch1 for LMS

[01 CPT -Tranche1-LMS verification - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/01+CPT+-Tranche1-LMS+verification)

Note：LMS Testing result are tracking under [03 UAT testing - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/03+UAT+testing)

2026-01-28  Confirmed with LMS team ,all the below manual entities need to feed to LMS from Ratan

| | Country | MX2.11 Entity | FMID | FMCODE | Feed to LMS |
| --- | --- | --- | --- | --- | --- |
| 1 | Bahrain | BAHRAIN | 10036430 | SCB BAHRAI*MAN | Y |
| 2 | QATAR | DOHA | 300010782 | SCB DOHA*DOH | Y |
| 3 | SLATE_QFC | 401081696 | SLATE ONE LLC*DOH | Y |
| 4 | Kenya | KENYA | 300011525 | SCB KENYA B*NBO | Y |
| 5 | Zambia | ZAMBIA | 10041903 | SCB ZAMBIA*LUS | Y |
| 6 | Uganda | UGANDA | 10041902 | SCB UGANDA*KAM | Y |
| 7 | Tanzania | TANZANIA | 10040387 | SCB TANZANI*DAR | Y |
| 8 | Ghana | GHANA | 10037477 | SCB GHANA*ACC | Y |
| 9 | Nigeria | NIGERIA | 300084297 | SCB NIGERIA*LAG | Y |
| 10 | Sri Lanka | SRI LANKA | 10036647 | SCB COLOMBO*CMB | Y |
| 11 | FCBUSLANKA | 10022098 | SCB COL FCB*CMB | Y |
| 12 | Vietnam | HANOI | 10041530 | SCB HANOI*HNI | Y |
| 13 | Pakistan | KARACHI | 10036655 | SCB KARACHI*KHI | Y |
| 14 | Bangladesh | DHAKA | 300011470 | SCB DHAKA*DAC | Y |

# Entity setup in blotter

Already setup in tranche3 ,no need to config any more, double confirmed 2026-01-20 Already done on UI

# Settlement Means

2026-05-12

Aligned with @Simon Godfrey Mahela and @Arockia Dinesh ,for DFCC, settlement means is NOS ,no need to add new settlement means on Ratan UI

📎 [RE DFCC discussion.msg](attachments/RE DFCC discussion.msg)
 
📎 [RE Manual entity -TANZANIA Static data signoff.msg](attachments/RE Manual entity -TANZANIA Static data signoff.msg)

~~DFCC is new settlement means for TAZ,need to be setup in SSI+ and setup in Nostro Static Blotter and Vostro SI Input Screen~~

<details>
<summary>Expand Details</summary>

![image-2026-3-4_16-13-32.png](attachments/image-2026-3-4_16-13-32.png)

~~![image-2026-3-4_16-13-47.png](attachments/image-2026-3-4_16-13-47.png)~~

~~~~![image-2026-3-4_16-13-52.png](attachments/image-2026-3-4_16-13-52.png)~~~~

</details>

# Static Data Signoff Email

| Country | MX2.11 Entity | FMID | FMCODE | User | Signoff Email | Comment |
| --- | --- | --- | --- | --- | --- | --- |
| BAHRAIN | BAHRAIN | 10036430 | SCB BAHRAI*MAN | David/Joseph, Synthia | | |
| NIGERIA | NIGERIA | 300084297 | SCB NIGERIA*LAG | David/Joseph, Synthia | | |
| Vietnam | HANOI | 10041530 | SCB HANOI*HNI | David | | |
| Pakistan | KARACHI | 10036655 | SCB KARACHI*KHI | David + Ali, Shaukat (In Country) | | |
| Qatar | DOHA | 300010782 | SCB DOHA*DOH | Joseph, Synthia | | |
| SLATE_QFC | 401081696 | SLATE ONE LLC*DOH | Joseph, Synthia |
| KENYA | KENYA | 300011525 | SCB KENYA B*NBO | Joseph, Synthia |
| ZAMBIA | ZAMBIA | 10041903 | SCB ZAMBIA*LUS | Joseph, Synthia |
| UGANDA | UGANDA | 10041902 | SCB UGANDA*KAM | Joseph, Synthia |
| GHANA | GHANA | 10037477 | SCB GHANA*ACC | Joseph, Synthia |
| TANZANIA | TANZANIA | 10040387 | SCB TANZANI*DAR | Mahela, Simon Godfrey; Dahal, Leyla(In country ) | | |
| SRI LANKA | SRI LANKA | 10036647 | SCB COLOMBO*CMB | Wellage, Samanthi ; Fonseka, Shalini | | |
| FCBUSLANKA | 10022098 | SCB COL FCB*CMB | Wellage, Samanthi ; Fonseka, Shalini |
| Bangladesh | DHAKA | 300011470 | SCB DHAKA*DAC | Morshed, Golam; Niloy, Nehabul Haque(In Country) | | |
| Other | Trade SI stamping | | | | | |
| Swift static data | | | | | |
| EBBS | | | | | |
| LMS | | | | | |

# Business UAT testcase

[03 UAT testing - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/03+UAT+testing)

[UAT testing checking-Tranche1 - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/UAT+testing+checking-Tranche1)

[UAT testing checking-Tranche2 - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/UAT+testing+checking-Tranche2)

# UAT Testing Signoff

| Country | Attached |
| --- | --- |
| KE | LMS |
| TZ |
| PK |
| LK |
| VN |
| ZM |
| BD |

# CPT

[Tranche:1 Countries (Bangladesh, Tanzania, Sri Lanka, Pakistan, Kenya, Vietnam,  Zambia )Manual entities cash Settlements Migration Day 2 - Operational readiness & Post go live Issue Tracker - FM re-platforming - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3790204945)

[Tranche:2 Countries (Nigeria, Ghana, Qatar, Bahrain, Uganda)Manual entities cash Settlements Migration Day 2 - Operational readiness & Post go live Issue Tracker - FM re-platforming - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3817314605)

Questions

| | Question | Details | Answer | Status |
| --- | --- | --- | --- | --- |
| 1 | Is there any priority for the manual entities or we need to go live all the 12 countries one time ? Country ,fmid ,fmcode mapping | ![image-2026-1-14_10-0-2.png](attachments/image-2026-1-14_10-0-2.png) ![image-2026-1-16_9-55-52.png](attachments/image-2026-1-16_9-55-52.png) | 2026-05-06 ![image-2026-5-7_10-23-21.png](attachments/image-2026-5-7_10-23-21.png)2026-01-30 Confirmed with Yashas ,not decided yet,will sync up if any update 2026-01-22 By next week will get the final go live slot ,then decide the priority continue to follow up with Yashas &Baliji 2026-01-20 Priority need to discuss with EBBS/Aspire then decide 2026-01-16 1.Get the volume for the all the manual entities and send to Dinesh ,then confirm the scope ,priority ,PM ccy applicable or not | |
| 2 | ![image-2026-1-8_11-22-48.png](attachments/image-2026-1-8_11-22-48.png) ![image-2026-1-8_11-32-37.png](attachments/image-2026-1-8_11-32-37.png) | FCBUSLANKA FMID should be 10022098 not 10036647 | 2026-01-16 FCBUSLANKA FMID should be 10022098 | |
| 3 | All the above 12 countries are EBBS countries ,so the accounting will send to EBBS ? | | 2026-01-30 Confirmed with Balaji ,Yes ,all 12 countries will send to EBSS 2026-01-22 Ask balaji to get the final confirmation 2026-01-16 Ask Sittrarasu, Balaji to confirm | |
| 4 | If enable the manual entities in Ratan, do we need to send to LMS? | | 2026-01-28 Confirmed with LMS team ,all the 12 countries need to feed to LMS from Ratan 2026-01-16 Yes Remove entity should go first ,send email to LMS to get confirmation | |
| 5 | 1.Is there any swift customization? 2.Is there any manual entities need to generate MT604/MT605 with customized Receiver BIC(MT604/MT605)? 3.Get from user on Sender BIC,53 Swift Bic and CCY/58 Swift Bic/Branch Code ,some swift static data | ![image-2026-1-8_13-39-18.png](attachments/image-2026-1-8_13-39-18.png) ![](https://confluence.global.standardchartered.com/download/attachments/3244588508/image-2025-5-21_16-34-44.png?version=1&modificationDate=1747816484000&api=v2) | 2026-03-17 Will follow swift related items in [02 Swift Message Analysing for manual entities - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/02+Swift+Message+Analysing+for+manual+entities) 2026-01-26 SRI LANKA:Wellage, Samanthi ; Fonseka, Shalini 1.User will help to provide some samples 2.There is no customized Receiver BIC in MT604/MT605 3.User will help to provide --- David/Sumita-BAHRAIN,NIGERIA,Vietnam,Pakistan2026-02-02 Confirmed with Sumita,no receiver bic hardcode requiremnet for BAHRAIN. 2026-01-20 1.Swift customization,Sumita confirm and send some samples 2.Receiver BIC (MT604,605) BAHRAIN need to add customized Receiver BIC.the other 3 countries no need if (entityFMID in ('300036368','3','400451508','400452428','2', '400906330', '10036430') and {Field_Currency} in ( XAU,XAG,XPD,XPT)) return receiverBIC =CHASGB2LXXXX 3.Sumita will send the swift static data 2026-01-16 1.Check the volume for all manual entity and send to Dinesh 2.Get the volume for the all the manual entities and send to Dinesh ,then confirm the scope ,priority ,PM ccy applicable or not 3.Open ,setup a call and confirm with ops ,send email to ops if any customization? | |
| 6 | Currency release cutoff ,need to get from user for each manual entity | | 2026-03-17 Tracking in Release CutOff Chapter 2026-01-26 SRI LANKA:Wellage, Samanthi ; Fonseka, Shalini User help to provide 2026-01-20 David/Sumita-BAHRAIN,NIGERIA,Vietnam,Pakistan - BAHRAIN:15:00 UTC VD-1BD - NIGERIA:17:00 UTC VD-1BD - Vietnam:11:00 UTC VD-1BD - Pakistan:13:00 UTC VD-1BD - Currency follow 10075222 Grace organized the release cutoff static data and send to Sumita to double confirm 2026-01-16 1.Open ,setup a call and confirm with ops | |
| 7 | NDS Auto Netting There is no entity condition setup in the rule condition ,do we need to add manual entity list or any Product Typology in the rule condition? | Pending NDS Netting： ![image-2026-1-13_15-14-9.png](attachments/image-2026-1-13_15-14-9.png) Instrument_Common__Murex_Product_Typology in ("NDS", "NDCF", "NDFRA", "ND CDS Fixing", "ND CDS", "ND-Convert", "NDS Fixing") && Cashflow__ND_Parent_Typology != "NDIRS" && Cashflow__Cashflow_Event_Reason not in ("Reversal", "Rebook") && (Cashflow__Netting_Id == null || Cashflow__Netting_Id == "") && ((Cashflow__Duplicate_NDS_FXD == null || Cashflow__Duplicate_NDS_FXD == "")) | 2026-01-16 Confirm with @Arockia Dinesh No need to update the rule ,manual entity will hit this rule and do the NDS netting | |
| 8 | Pending Fixing STP/NSTP Control( in case new product have fixing events) There is no entity condition setup in the rule condition ,do we need to add manual entity in the rule condition? or is there any new product have fixing events for these manual entities? | Fixing Unknown: ![image-2026-1-13_15-16-16.png](attachments/image-2026-1-13_15-16-16.png) Cashflow__Pending_Fixing_Flag == "X" && ((Instrument_Common__Murex_Product_Family == "IRD" && Instrument_Common__Murex_Product_Group in ("IRS", "CS", "LN_BR", "CF")) || (Instrument_Common__Murex_Product_Family == "COM" && Instrument_Common__Murex_Product_Group in ("SWAP", "ASIAN", "FWD")) || (Instrument_Common__Murex_Product_Family == "CRD" && Instrument_Common__Murex_Product_Group == "RTRS")) | 2026-01-16 Confirm with @Arockia Dinesh No need to change the rule | |
| 9 | SSI Stamping Hierarchy - Follow UK model Whitelist: CN/MY/IN/SG/LOANID old logic Rest: new logic - UK Model **'**BranchId_Murex3Id' -> 'CFI Code' -> 'Is_Default_SSI' - non UK Model 'CFI Code' -> 'Is_Default_SSI' -> 'Branch' So for the manual entities ,we will follow the UK Model? | NON_UK_ENTITY_LIST "401036553","400991880","400007847","400906330","300036368","3","400452428", "400451508","9","400093619","4","400960089","400001378","400054741","400220273", "400899993","400075752","400095464","400209000","400677737","400229749","400054708", "400130178","400085753","400683682","400218197","400667486","400090093","400130180", "10020899","400057714","10036642","400054737","400798477","10032025","235003861", "400516443","400185419","400193370","10062461","10078716","400516442", "401053411" | 2026-01-16 Confirm with @Arockia Dinesh Manual entities should follow the UK model,no need to add manual entities in this list | |
| 10 | Currency Configuration (if applicable) - Non-ISO to ISO Code mapping - Precious Currency Mapping 1.Is there any new currency to currency ISO mapping for the new manual entities? 2.Is there new PM entity to be added for new onboarding manual entities? 3.Other UDF tables we copied from Murex 2.11 driving the PM swift generation. If there's new PM entity to be added for new onboarding entity？ | Non-ISO to ISO Code mapping ![image-2026-1-9_17-12-21.png](attachments/image-2026-1-9_17-12-21.png) PM Currency list ![image-2026-1-9_16-7-3.png](attachments/image-2026-1-9_16-7-3.png) For field 23,26,32 in MT604/MT605 ,we need to query static data from the below table UDF_Strategy ![image-2026-1-12_19-59-17.png](attachments/image-2026-1-12_19-59-17.png) UDF_SWF_LS ![image-2026-1-12_19-58-55.png](attachments/image-2026-1-12_19-58-55.png) ![image-2026-1-12_19-57-56.png](attachments/image-2026-1-12_19-57-56.png) | 2026-03-17 Tracking in Non-ISO to ISO Currency Chapter 2026-02-26 got confirmation from @Deepak K and @Yashas Balaji , no Metal currencies which are applicable for manual enties 2026-01-26 Wellage, Samanthi ; Fonseka, Shalini-SRI LANKA: 1.For sri lanka ,the non ISO to ISO mapping is LKO-LKR,we have the existing record in our system ,no need to add new mapping 2.No PM ccy 3.No 2026-01-20 1.Non ISO to ISO mapping - Vietnam:VNO-VND already maintained in existing list - Pakistan:PKO-PKR.need to added in the list 2.No new PM Currency for manual entities 3.Sumita will help to provide the samples for item 3 2026-01-16 1.Check the volume for all manual entity and send to Dinesh 2.Get the volume for the all the manual entities and send to Dinesh ,then confirm the scope ,priority ,PM ccy applicable or not 3.Open ,setup a call and confirm with ops | |
| 11 | Settlement Accounting 1.Need to get Bridge Account /EBBS Branch code & EBBS Transaction type 2.Is there any PM ccy in any manual entity doesn't need to generate accounting? 3.Need user to provide the timezone static | Currently if the entity is in - 10075222- 400041070 & PM ccy in the list ,will not generate accounting ![image-2026-1-13_15-20-31.png](attachments/image-2026-1-13_15-20-31.png) | 2026-03-13Tracking in EBBS Posting_Branch/ EBBS Bridge Account/Timezone Chapter 2026-03-06 Confirmed with Yashas,due to no PM ccy go live ,so no additional requirement for this part 2026-01-30 1.Yasha wil check with Razor and feedback 2.Yasha and Balaji need to discuss with Vivek then feedback 3. Yashas and Balaji help to provide 2026-01-22 1&2&3 Confirm with Balaji &Aggarwal, Vivek 2026-01-16 1.Get Static data from Balaji 2.Check the volume for all manual entity and send to Dinesh 3.Get the volume for the all the manual entities and send to Dinesh ,then confirm the scope ,priority ,PM ccy applicable or not | |
| 12 | Include new branch in GUI Drop down - Cashflow Blotter (mandatory for each entity) - Dashboard | I think tranche3 have already go live this [https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/9905654/](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/9905654/)![](https://confluence.global.standardchartered.com/download/attachments/3479085303/image-2025-9-19_16-45-34.png?version=1&modificationDate=1758271535000&api=v2) | 2026-01-16 Already config on UI | |
| 13 | Vostro SI Input Screen - Include New Settlement Means Is there any new settlement means? adhoc dropdown list ![image-2026-1-21_13-35-59.png](attachments/image-2026-1-21_13-35-59.png) nostro static-create ![image-2026-1-21_13-36-32.png](attachments/image-2026-1-21_13-36-32.png) ![image-2026-1-21_13-36-54.png](attachments/image-2026-1-21_13-36-54.png) | | 2026-03-04 DFCC new settlement means need to be setup for TAZ 2026-01-26 SRI LANKA:Wellage, Samanthi ; Fonseka, Shalini There is no new settlement means added for SRI LANKA 2026-01-20 Sumita will help to check if new settlement means to be added for BAHRAIN,NIGERIA,Vietnam,Pakistan 2026-01-16 Open ,setup a call and confirm with ops | |
| 14 | Rounding - applicable for special currency/requirement only Is there any new currency added for the new manual entities? | | 2026-03-05 NIGERIA need to update the rounding ,waiting for user to confirm ,tracking in Rounding chapter 2026-01-26 Wellage, Samanthi ; Fonseka, Shalini-SRI LANKA: Trade is booked as LKO,and settlment is LKR,currently we have these two rounding static data in Ratan system ,so no need to add new rounding static 2026-01-20 BAHRAIN,NIGERIA,Vietnam,Pakistan VNO.VND,PKO,PKR is already config in static data ,no need to add 2026-01-16 Open ,setup a call and confirm with ops | |
| 15 | Nostro Static ,need to get from user for each entities. | | 2026-03-17 Tracking in Nostro Static chapter 2026-01-26 SRI LANKA:Wellage, Samanthi ; Fonseka, Shalini User help to provide 2026-01-20 Sumita will help to provide nostro static for BAHRAIN,NIGERIA,Vietnam,Pakistan 2026-01-16 Open ,setup a call and confirm with ops | |
| 16 | Business rule need to be added? | | 2026-08-13 📎 [Business rule0811.xlsx](attachments/Business rule0811.xlsx) --- SRI LANKA:Wellage, Samanthi ; Fonseka, Shalini 2026-01-16 Open ,setup a call and confirm with ops | |
| 17 | CFI code? Do we need to config new CFI code for manual entities? | ![image-2026-1-14_16-2-23.png](attachments/image-2026-1-14_16-2-23.png) | 2026-01-16 Confirm with @Arockia Dinesh No new for CFI code for manual entities | |
| 18 | Cote D'lvoire–COTEDIVOIR is this some kind of typo? | | 2026-01-16 Use COTE D IVORE | |

<details>
<summary>Expand Details</summary>

| Country or entity? | Priority? | FMID | FMCODE | Question |
| --- | --- | --- | --- | --- |
| BOTSWANA | 1 | 10036775 | SCB BOTSWAN*GBE | |
| GHANA | 1 | 10037477 | SCB GHANA*ACC | |
| Vietnam | 1 | | | 2025-12-01 We should refer to the country column from below table? [Cash Settlements Migration Tranche 3 - Jersey & Manual Entities - FM re-platforming - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=3381939814#CashSettlementsMigrationTranche3Jersey&ManualEntities-Tranche3RiskAssumptionsIssuesDependency) ![image-2025-12-1_10-41-33.png](attachments/image-2025-12-1_10-41-33.png) |
| KENYA | 1 | 300011525 | SCB KENYA B*NBO | |
| NIGERIA | 1 | 300084297 | SCB NIGERIA*LAG | |
| UGANDA | 1 | 10041902 | SCB UGANDA*KAM | |
| BAHRAIN | 2 | 10036430 | SCB BAHRAI*MAN | |
| ZAMBIA | 2 | 10041903 | SCB ZAMBIA*LUS | |
| Pakistan | 3 | | | 2025-12-01 ![image-2025-12-1_10-48-59.png](attachments/image-2025-12-1_10-48-59.png) |
| COTEDIVOIR | 3 | 400011581 | SCBL*ABI | |
| Qatar | 3 | | | 2025-12-01 We have 2 fmid with the same country QATAR,which one do we need ? ![image-2025-12-1_10-46-31.png](attachments/image-2025-12-1_10-46-31.png) ![image-2025-12-1_10-46-53.png](attachments/image-2025-12-1_10-46-53.png) |
| IRAQ*** | | | | 2025-12-01 Is IRAQ*** same with IRAQ? ![image-2025-12-1_10-48-8.png](attachments/image-2025-12-1_10-48-8.png) |
| TANZANIA | | 10040387 | SCB TANZANI*DAR | |
| Bangladesh | | | | 2025-12-01 Do we want the below one? ![image-2025-12-1_10-50-12.png](attachments/image-2025-12-1_10-50-12.png) |
| SRI LANKA | | | | 2025-12-01 There are two fmid with same country ,which one do we need? ![image-2025-12-1_10-50-56.png](attachments/image-2025-12-1_10-50-56.png) ![image-2025-12-1_10-51-16.png](attachments/image-2025-12-1_10-51-16.png) |
| OMAN | | 300010730 | SCB OMAN*RWI | |

</details>