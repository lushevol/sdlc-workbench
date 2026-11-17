# Background

**a) Nostro Account: **Nostro Account is the actual account held by a Legal Entity <u>with another Legal Entity</u> for purpose of paying / receiving funds (example: SCB London holds a CHF Nostro with Credit Suisse Zurich called 'CHF MAIN' and a SGD account with SCB Singapore called 'SGD MAIN'). A single Nostro Account can be used by all departments in SCB (FM, TM, Cash, Trade etc). For EBBS countries, a EBBS account is opened as the Nostro Ledger account to consolidate all the Nostro entries from the different systems / departments.

**b) Over Account: **Accounts opened <u>within the same Legal entity</u> for purpose of paying / receiving funds from clients who also hold account with the same Legal entity (example: SCB London holds a CHF account with SCB London called as 'CHF No 2')

**c) Suspense Account:  **Suspense accounts are internal accounts opened <u>within the same Legal Entity</u> for purpose of posting settlement accounting entries. No Payment / receipt of funds involved (example: SCB London used 'DVSUS' for settling Derivative transactions which do not involve a payment)

Nostro Accounts must be made available in the FMO systems (RATAN, RAZOR, GPTM, MUREX2.11 etc) in order to generate payment / receipt instructions to the correct Nostro account. However currently there is no golden source for Nostro static.

All three categories (Nostro / over account / suspense) are treated as Nostro static and maintained within the respective TP systems (RATAN, RAZOR, GPTM, MUREX2.11).

Creating a Golden source will reduce the efforts to maintain same Nostro static in multiple systems and reduce the risk of omission.

As part of FMRP, NAMS is being proposed to be used as the Golden Source as Nostro static already exists in NAMS database. RATAN will be the pilot to consume the Nostro static from NAMS via RDM and subsequently other FMO systems (RAZOR / GPTM) will also consume data from RDM.

Note: Metal CCY Nostros are not available in NAMS, but will have to maintained in RDM directly.

# Mapping between NAMS and SCI

Below are the fields required for Nostro static maintenance

| Data Source | Field S.No | Unique Key for Nostro Best Matching Logic | Nostro Static Field Name | Sample | Source System | Source System Field | Field is currently Mandatory in NAMS? | Value | Comment |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Existing Fields in NAMS** | 1 | Y | Agent Bank SCI Code | 11034125/1 | NAMS | Agent Bank SCI Code | TBC | | |
| 2 | Y | Status | Open/Closed | NAMS | Status | TBC | Open/Closed | |
| 3 | | Ledger Account Number_EBBS | HK7251800192082CNY238 | NAMS | Ledger Code | TBC | HK7251800192082CNY238 | |
| 4 | | Agent Bank_Swift | SCBLCNSXSHA | NAMS | Agent Bank BIC Code | TBC | SCBLCNSXSHA | |
| 5 | | Statement Account Number | 501511239996 | NAMS | Account Number | TBC | 501511239996 | Need data massaging by FMO in RDM |
| 6 | | Recon System Nostro ID | 20USD48 | NAMS | Recon System NostroId | TBC | 20USD48 | Manually input in NAMS, no interface with TLM |
| 7 | Y | Settlement_currency | CNY BDT,etc | NAMS | Currency Code | TBC | CNY | |
| **New Fields to be created in RDM** | 8 | Y | Settlement_means | NOS | NAMS/RDM | Settlement_means | | NOS / Over Account / Suspense etc | Need to add in RDM for Overaccount / Suspense Nostros |
| 9 | Y | Settlement_account | BDT MAIN | NAMS/RDM | | ---- | | New field in RDM |
| 10 | Y | Effective Start Date | 01/Jan/2023 | RDM | ---- | ---- | | New field in RDM |
| 11 | Y | Effective Closure Date | 31/Dec/2022 | RDM | ---- | ---- | | New field in RDM |
| 12 | Y | Nostro Used by FMO | Y (leave Blank if No) | RDM | ---- | ---- | Y / Blank | New field in RDM |
| 13 | Y | FMO System | RATAN | RDM | FMO system | ---- | ALL / RAZOR / GPTM / RATAN | New field in RDM |
| 14 | | Notice_to_receive | Y (leave Blank if No) | RDM | ---- | ---- | Y / Blank | New field in RDM |
| 15 | | PSGL Chart Field | 2387251800122102761950 | RDM | ---- | ---- | Various | New field in RDM |
| **RDM to Source Data from SCI** | 16 | Y | Legal_entity_fmid | 400452428 | SCI | ALTAS_ID | ---- | 400452428 | ALTAS_ID:2 SCI_ID: 11153358 SCI &NAMS link RDM to source from SCI |
| 17 | | Legal_entity_code | SCB HONGKON*HKG | SCI | ATLAS_CODE | ---- | SCB HONGKON*HKG | RDM to source from SCI |
| 18 | | Agent Bank_fullname | SCB CHINA SHANGHAI SHA | SCI | NM_PARTY_SHORT | ---- | SCB CHINA SHANGHAI SHA | RDM to source from SCI |
| 19 | | Agent Bank_address | 25 TH FLOOR STAN CHART TOWER 201 CENTURY AVENUE PUDONG SHANG | SCI | NM_ADDRESS1 NM_ADDRESS2 | ---- | 25 TH FLOOR STAN CHART TOWER 201 CENTURY AVENUE PUDONG | RDM to source from SCI |
| 20 | | Agent Bank City | SHANGHAI CN | SCI | NM_ADDRESS4 | ---- | SHANGHAI | RDM to source from SCI |
| 21 | | Agent Bank Postal Code | 200120 | SCI | NM_POST_CODE | ---- | 200120 | RDM to source from SCI |
| **To be Analyzed if relevant** | 22 | | SSI | | NAMS | SSI | TBC | SSI / Non-SSI / Blank | Need to determine if this field is relevant |
| 23 | | Correspondent Type | | NAMS | Business Type | TBC | "Securities" / "Cash/Correspondent" | Need to determine if this field is relevant |

| Mapping: | NAMS.Agent Bank SCI Code | SCI.SCI_ID+'/'+SUB_PROFILE_SCID |
| --- | --- | --- |
| | 11153358/1 | 11153358/1 |
| | | |
| | NAMS.Agent Bank BIC Code | SCI.ATLAS_CODE |

# Suspense Account Type in Razor (settlement Means)

SUS    GBFXSUS    ALOCSUS    FXBRREC    TBSUS    FXSUS    TBFXSUS    FISUS    DVSUS    WMSUS    FATCASUS    HIBSUS    MMSUS    CPN SUSP    PVBSUS    SUSP    WHTSUS     CLS SUSP

# Suspense Account Key column

| Field S.No | Expect NOS column | Sample | Comment |
| --- | --- | --- | --- |
| 1 | settlement account | DVSUS | Searching Key |
| 2 | settlement means | DVSUS | Searching Key |
| 4 | legal entity/ legal entity | | Searching Key ?? Need to add |
| 5 | currency | | Searching Key ?? Need to add |
| 6 | ebbs account number | | Razor save in TABLE#DATA#SITRN_DBF |
| 7 | PSGL Mapping | | Razor don't save it, maintained by downstream |
| 8 | Bridge Account Number | | Razor use a Lookup table to maintain it |

# Issues

1) Account number is different in RAZOR vs NAMS(example: SCB Singapore's GBP account with SCB London is captured as '05199783101' in NAMS, while it is 'GB83 SCBL 6091 0451 9978 31' in our Nostro SSI PDF List)

| NAMS | RAZOR | Difference |
| --- | --- | --- |
| 15209909601AED | 15 2099096 01 | Currency +space |
| 5000408097 | DK4920005000408097 | Account info |
| 0100001846001 | HU 39120010080000184600100004 | Account info +suffix |
| 600-392027 | IL510126000000000392027 | Account info + replace '-' to '000000' |

2) Multiple accounts existing NAMS, not all are relevant for FM

| NAMS | RAZOR |
| --- | --- |
| SCB Entity SCI Code | Account Number | Currency Code | LEID/SUB ID | Legal Entity | Closing Entity | Settlement Account | Settlement Account Number |
| 12921313/1 | 690750AUD00001 | AUD | 12921313/1 | SCB SG LTD*SIN | CE SGSUBDB | AUD MAIN | 690750AUD00001 |
| 12921313/1 | 1803004693504 | AUD | 12921313/1 | SCB SG LTD*SIN | CE SGSUBDB | AUD OTH 2 | 1803004693504 |
| 11090155/71 | 949321AUD00001 | AUD | 11090155/71 | SCBLDBU*SIN | CE SGDBU | AUD ACLR | CHT0001974 |
| | | | 11090155/71 | SCBLDBU*SIN | CE SGDBU | AUD OTH 2 | 1803004693500 |
| | | | 11090155/71 | SCBLDBU*SIN | CE SGDBU | AUD MAIN | 949321AUD00001 |

# Open Points

1. Where should Suspense data be stored - NAMS, RDM or RATAN
2. Do we store a cache of Nostro data in RATAN
3. 1 Account number match to many Ledger Account(EBBS Nostro accout)

# Reference document: