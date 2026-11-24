****

**General Suggested Principle: **

1. SUSPENDED will be marked by Stella, Suppressed will be cashflow published as PROJECTED by Stella and marked in Ratan.
2. If the cashflow will be eventually settled in Ratan, then Ratan will filter the cashflow, others will be SUSPENDED in Stella.
3. If the new filter will reduce large cashflow volume, then it will be remain in Stella.
4. If the logic is simple and static, then it will remain in Stella, others logic will be maintained in RATAN.

# Logic in Stella

| | Rule Summary | Current Rule logic in Stella | Ratan Rule Logic |
| --- | --- | --- | --- |
| 1 | Migration cashflow | Trade has **Trade_Second_Source_System_Name** = 'Migrated' and Cashflow payment type starts with 'Migrated_Aggregated%', then outcome is always **SUSPENDED** | NA |
| 2 | Placeholder trade | If Placeholder trade (manual mark for IRS in blade, stp in VPA), i.e. trade has Is_Shell_Trade = true, then outcome is always **SUSPENDED** | NA |
| 3 | ETD cashflow | If trade is ETD (Base_Product in 'Listed Option','Future'), then outcome is always **SUSPENDED** | NA |
| 4 | PreAllocation cashflow | Trade **Allocation_Reporting_Status** = 'PreAllocation', then outcome is always **SUSPENDED**, regardless whether Cashflow is from Deliveries or additionalPayment | NA |
| 5 | FX cashflow | **Current**: Isda taxonomy in (ForeignExchange:Spot, ForeignExchange:Forward, ForeignExchange:Swap) and portfolio hierarchy is Eligible per below list and Cashflow is from additionalPayment section, is always **SUSPENDED** **Future**: All FX cashflow should be **PROJECTED** | Per below table |
| 6 | FXO PCD/DCD | |
| 7 | FXO Structure | | it's part of package (Logic_Package_ID != empty) and **counterparty is external**, it should be processed as PROJECTED |
| 8 | Portfolio Reassignment Aggregation | Trade_Event.Business_Event_Type = 'Portfolio Reassignment' and Effective Date>=Payment_Date, is always **SUSPENDED** | |
| 9 | | Rest **PROJECTED** | |

### Suspended will be dropped in group blotter

### Which portfolio business hierarchy are eligible for SUSPENDED?

- **MDS.SD_PCT_PORTFOLIO**, if **BUSINESS_HIERARCHYL1** matches any of below values: - '|Group|Corporate and Institutional Banking|Financial Markets|Financial Markets excluding XVA|Macro Trading|FXO*' - '|Group|Corporate and Institutional Banking|Financial Markets|Financial Markets excluding XVA|Macro Trading|Rates*' - '|Group|Corporate and Institutional Banking|Financial Markets|Financial Markets excluding XVA|Macro Trading|Commodities*'

### Background for FXO Structure

In one structure trade, it may contain FXO, LNBR, CCS, if the FXO exercise generated FXD, which would have the same structure ID (contract ID in FMRP), and to be netted off with LNBR/CCS, so it would need to processed in RATAN with PROJECTED status.

# Logic in FX replication into Razor

[Ratan / TDS3 Replication to Razor - Formalisation & Process Governance FMO - Confluence](https://confluence.global.standardchartered.com/pages/viewpage.action?pageId=2934697333)

**Requirement**:

1. Rules is enable to edit in front end.
2. SUSPENDED cashflow can be manually STPed into cashflow blotter per maker-checker process.

| | Rule Summary | Current Rule logic in Ratan Trade (AND condition) | Ratan Abort Rule Logic (AND condition) | Scope |
| --- | --- | --- | --- | --- |
| 1 | Stella Cashflow | Data_Flow__Source_Stack_Flow_Name == "FMRPSTELLA" | Data_Source_System='Stella' | Both |
| 2 | FX spot/forward/swap | Instrument_Common__ISDA_Taxonomy in ("ForeignExchange:Spot", "ForeignExchange:Forward", "ForeignExchange:Swap") | Apply the same | Both |
| 3 | EG/NP/SA | Entity__Booking_Entity_SCI_FMID not in ("401036553", "400991880", "400007847") | Apply the same | Both |
| 4 | PCD/DCD JE/external client → Ratan Internal entity->Razor | Contract_Typology NOT IN (FX_DCD, FX_PCD, FX_PCD_AXKI, FX_PCD_DIF) OR Parent_Position_Id IS NULL OR Parent_Position_Id = '' OR ( Entity.Counterparty_Country_ISO_Code != JE AND Cpty IN (SCB internal entity list) ) @Kuan Wang** (Elena):** 2026-06-08 Note: Entity__Counterparty_SCI_FMID in (**"400001378", "10020899", "235003861", "10078716", "10036642", "10062461", "10032025", "400054708", "400054737", "400054741", "400057714", "400075752", "400085753", "400090093", "400095464", "400130180", "400130178", "400185419", "400193370", "400209000", "400218197", "400220273", "400229749", "400516443", "400516442", "400667486", "400677737", "400683682", "400798477", "400899993", "300036368", "3", "400452428", "400451508", "4", "400960089", "9", "400093619", "400041070", "10075222", "400906330", "401053411", "5", "400045551", "8", "300089409", "10036428", "10036382", "400032489", "2", "300011345", "300075472", "6", "10038345", "1003665", "10036775", "400825315", "10041902", "400823482", "7"**) | Apply the same ![image-2026-7-17_17-26-54.png](attachments/image-2026-7-17_17-26-54.png) | Both |
| 5 | Certain entity & Counterparty | Entity__Counterparty_SCI_FMID not in ("401038280", "401038281", "400009154", "300079654", "300037428", "300037430", "401046131", "401045020", "401044980", "400036904", "400590585", "400915609") && (Entity__Booking_Entity_SCI_FMID != "10075222" || Entity__Counterparty_SCI_FMID not in ("300010953", "300037151", "300037746")) && (Entity__Booking_Entity_SCI_FMID != "2" || Entity__Counterparty_SCI_FMID not in ("400011374")) && (Entity__Booking_Entity_SCI_FMID != "6" || Entity__Counterparty_SCI_FMID not in ("401059381", "401059382")) && (Entity__Booking_Entity_SCI_FMID != "4" || Entity__Counterparty_SCI_FMID not in ("400178086", "400178088", "400178085")) && (Entity__Booking_Entity_SCI_FMID != "400960089" || Entity__Counterparty_SCI_FMID not in ("401014976")) 2026-06-30 **zhangjiangnan** Add rule : - &&(Entity__Booking_Entity_SCI_FMID!= "400452428" || Entity__Counterparty_SCI_FMID not in ("400451508")) - &&(Entity__Booking_Entity_SCI_FMID!= "9" || Entity__Counterparty_SCI_FMID not in ("400038228")) Update rule : - && (Entity__Booking_Entity_SCI_FMID != "6" || Entity__Counterparty_SCI_FMID not in ("401059381", "401059382", "400003775")) 2026-08-22 zhangjiangnan / Elena **Add rule :** - **(Entity__Booking_Entity_SCI_FMID != "400906330 -STAN CHART AG*FRA" || Entity__Counterparty_SCI_FMID not in ("400928073", "300010953"))** - 400906330 - STAN CHART AG*FRA ** ** - 400928073 - IRS SECTION AG*FRA - "fmType": "INTLACC", - 300010953 - **IRS SECTION*LDN**" - covered by cashflow suppression rule - *STELLA TDSX RATAN FXO UBER Migration* **Update rule :** - Before: && (Entity__Booking_Entity_SCI_FMID != "10075222" || Entity__Counterparty_SCI_FMID not in ("300010953", "300037151", "300037746")) After: && (Entity__Booking_Entity_SCI_FMID != "10075222" || Entity__Counterparty_SCI_FMID not in ("300010953", "300037151","300037746",** "10039205", "400035821"**)) - - **10039205 - **CURR OPT**** ** – covered **by cashflow suppression rule - *Suppress by Murex 2.11 label* - **400035821** ** – covered **by cashflow suppression rule - UK Internal Clients - Before: && (Entity__Booking_Entity_SCI_FMID != "4" || Entity__Counterparty_SCI_FMID not in ("400178086", "400178088", "400178085")) After: && (Entity__Booking_Entity_SCI_FMID != "4" || Entity__Counterparty_SCI_FMID not in ("400178086", "400178088", "400178085",** ****"400178087"**)) - - **400178087 - **INDIA OPTION*MMB - ** covered **by cashflow suppression rule - *MX MUMBAI inter counterparty / Intra Entity for Mumbai* | Not applicable. so intern counterparty will remain as SUSPEND in Ratan also 2026-06-02 **Elena** **To be updated to 'Apply the same' ? ****Need to Double confirm with @Arockia Dinesh .** - **Sample: FMRP8.0 Trade Migration - India; ****Trade Id: 8002535874** - **2026-06-04 Elena should be CASHFLOW_SUPPRESSED since FMRP1 env not sync the newest suppression rule: 7455186167809089536 - MX MUMBAI inter counterparty** ![image-2026-6-2_11-27-2.png](attachments/image-2026-6-2_11-27-2.png) 2026-06-04 **Elena** Entity__Counterparty_SCI_FMID not in ("401038280 - INTL/SPOT DESK*CN", "401038281 - INTL/FWD DESK*CN", "400009154 - INTL*FWD DESK", "300079654 - INTL*SPOT DESK", "300037428 - INTL*FX INTL*FX", "300037430 - INTL*OPTN", "401046131 - INTLSPOTHK*KWT", "401045020 - INTL/SPOT TW", "401044980 - INTL/SPOT.FWDTW", "400036904 - SCB DUMMY IRD*TPE", "400590585 - TBFX CASH PAYMENTS", "400915609 - SCB DUMMY IRD S*SIN") – 7461021018864951296 Suppress by Murex 2.11 label && (Entity__Booking_Entity_SCI_FMID != "10075222 - SCB LONDON*LDN" || Entity__Counterparty_SCI_FMID not in ("300010953 - IRS SECTION*LDN", "300037151 - CAASH*ROLL", "300037746 - NDFIRS*LDN")) && (Entity__Booking_Entity_SCI_FMID != "2 - SCB HONGKON*HKG" || Entity__Counterparty_SCI_FMID not in ("400011374 - SCB INTERNAL*HKG")) && (Entity__Booking_Entity_SCI_FMID != "6 - SCB BANGKOK*BKK" || Entity__Counterparty_SCI_FMID not in ("401059381 - INTLFWD TH DESK*BKK", "401059382 - INTLSPOT TH DESK*BKK")) && (Entity__Booking_Entity_SCI_FMID != "4 - SCB BOMBAY*MMB" || Entity__Counterparty_SCI_FMID not in ("400178086 - INDIA FORWARD*MMB", "400178088 - INDIA IRD*MMB", "400178085 - INDIA SPOT DESK*MMB")) && (Entity__Booking_Entity_SCI_FMID != "400960089 - GIFT CITY TM*MUM" || Entity__Counterparty_SCI_FMID not in ("401014976 - INDOPTDES*GUJ")) | Both |
| 6 | ~~Fees~~ | ~~NA~~ | ~~Payment type doesn't contains Fees~~ | Cashflow |
| 7 | (Trade) Entity and Counterparty should be different | Entity__Booking_Entity_SCI_FMID != §Entity__Counterparty_SCI_FMID | Can Apply the same auto suppressed by Ratan | Both |
| 8 | (Trade) Not Duplicate | Is_Duplicate_Booking != true | No impact if apply the same in cash settlement Checked with Stella Stella > Murex, no cashflows from Stella (Teams checked with Lorraine) | Both |
| 9 | (Trade) Booked trade | Trade_State == "BOOKED" | Cashflow status = "PROJECTED" | Trade |
| 10 | (Trade) Limit market event | (Trade_Event__Business_Event_Type in ("Trade", "Amendment", "PartialTermination", "CloseOut", "RemainingPartyFull", "PortfolioReassignment", "Withdrawal", "Termination") && Last_Action_Type in ("Book", "Undo")) || ((Trade_Event__Business_Event_Type in ("RemainingPartyFullNovation", "StepInFull", "StepInPartial", "Clearing") && Last_Action_Type == "Book")) | in Uber: Business version is not processed yet ~~in SCBML: filter out cashflow event type = Status_Update && Sequence is xxxx_1_1~~ | Trade |

**Special Scenario**

May not be a valid scenario for contract_typology, which can't be amended, but need to consider when onboarding any new field/logic can be amended.

then it will have duplicate payment/missing payment issue.

| Trade ID | Trade Event | Major Version | ISDA Taxonomy | Cashflow ID | Cashflow Event | Currency | Amount | Direction | Contract_Typology | Expected to be Settled in |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T01 | Trade | 1 | ForeignExchange:Spot | C01 | New | USD | 100 | Pay | Null | Razor |
| | Trade | 1 | ForeignExchange:Spot | C02 | New | CNY | 700 | Receive | Null | Razor |
| | | | | | | | | | | |
| T01 | Amendment | 2 | ForeignExchange:Spot | C01 | Withdrawal | USD | 100 | Pay | Null | Razor |
| | Amendment | 2 | ForeignExchange:Spot | C02 | Withdrawal | CNY | 700 | Receive | Null | Razor |
| | Amendment | 2 | ForeignExchange:Spot | C03 | New | USD | 100 | Pay | FX_DCD | Ratan |
| | Amendment | 2 | ForeignExchange:Spot | C04 | New | CNY | 700 | Receive | FX_DCD | Ratan |

# Logic in Murex 2.11

Reference: [2024 FMRP Murex Deliverable - H2 - Murex Development Team - Confluence](https://confluence.global.standardchartered.com/display/BODSD/2024+FMRP+Murex+Deliverable+-+H2)

| | Publishing Criteria | Ratan Rule Logic |
| --- | --- | --- |
| 1 | Excluding Internal funding deals (settled in Razor ALM) | 1. 401043901,401079573,401059381,401046131,401045020,401046130,401044980,401079570,401059382,400172170,401013999,401014191,400060078,401009326,400084944,400041525,400992472,400058094 needs to be added into cashflow suppression rule - Suppress by Murex 2.11 label 1. Cashflow suppression rule - Suppress by Murex 2.11 label needs to exclude NDF, Phy_Precious, Emissions FX? Note: some inactive counterparty are excluded |
| 2 | Excluding trades in Dummy portfolios -TABLE#LIST#FLTPF_IN_DBF | No booking for now in Stella yet |
| 3 | Excluding Non deliverable currency payments but not for typology PHP_DELIVERABLE and IDR_DELIVERABLE Include TWD currency for HK entity | no Non deliverable currency payments in Stella |
| 4 | Excluding FXD payments (settled in Razor FX) unless: - Typology is NDF, Phy_Precious and Emissions FX - Strategy is FEDSVALIDATOR - XIT payment - Strategy is FX_PDC, FX_DCD , DCD and internal JERSEY or all external counterparts - FXD trade generate by exercise for OPT trade - Bullion currency FXD | - NDF is already processed in Stella - FXD trade generate by exercise for OPT trade is processed in Stella and typology =PayModeSett - Bullion currency FXD will be under commodity taxonomy - XIT payment: as historical reason in Murex, Razor can't process fee generated from XIT, so needs to be processed in Ratan Need attention to monitor - Typology is Phy_Precious and Emissions FX - Strategy is FEDSVALIDATOR - Strategy is FX_PDC, FX_DCD , DCD and internal JERSEY or all external counterparts |
| 5 | Excluding Payments in Auto Suppression | | M_ENTITY | M_FAMILY | M_GROUP | M_STRATEGY | M_TYPE | M_TYPOLOGY | M_ATLAS_LEID | | --- | --- | --- | --- | --- | --- | --- | | LONDON | | | | | | 400891880,400940204,400902549,400929025,400949238,400937678,400880519,400959890, 400930982,400812227,400917781,400881639,400889353,400912088,400934094,300037798, 400089624,400805668,400935870,400948418,400063823,401034351,401008886,400861619, 10036642 | | LONDON | COM | FWD | | | | 400137596 | | LONDON | SCF | SCF | | | | 400137596 | | LONDON,BANGKOK,HONGKONG,JAKARTA,MAURITIUS,SACU SING,SCAG,KLUMPUR | IRD | BOND | | | | 400058727 | | LONDON | IRD | LN_BR | | | | 400258208 | | LONDON | SCF | SCF | | | | 400059609 | | HONGKONG | IRD | LN_BR | | | | 400041098 | | LONDON | COM | OFUT | | | | 400059609 | | LONDON | CURR | FXD | | | | 400999656 | | LONDON | IRD | IRS | | | | 400058727 | | LONDON | SCF | SCF | | | | 400059979 | | LONDON | CURR | FXD | | | NDF | 400009154 | | LONDON | CRD | CDS | | | | 400045461 | | LONDON | SCF | SCF | | | | 400040412 | | LONDON | CURR | FXD | | | NDS Fixing | 400058727 | | LONDON | CURR | FXD | | | NDF | 400973688 | | LONDON | SCF | SCF | | | | 401039314 | | CHINA HO | CURR | FUT | | FUT | | 400571122 | | LONDON | SCF | SCF | | | | 400058727 | | SCAG | CURR | FXD | | | | 400058727 | | MUMBAI | SCF | SCF | SCF_LTFX_IN | SCF | | | |
| M_ENTITY | M_FAMILY | M_GROUP | M_STRATEGY | M_TYPE | M_TYPOLOGY | M_ATLAS_LEID |
| LONDON | | | | | | 400891880,400940204,400902549,400929025,400949238,400937678,400880519,400959890, 400930982,400812227,400917781,400881639,400889353,400912088,400934094,300037798, 400089624,400805668,400935870,400948418,400063823,401034351,401008886,400861619, 10036642 |
| LONDON | COM | FWD | | | | 400137596 |
| LONDON | SCF | SCF | | | | 400137596 |
| LONDON,BANGKOK,HONGKONG,JAKARTA,MAURITIUS,SACU SING,SCAG,KLUMPUR | IRD | BOND | | | | 400058727 |
| LONDON | IRD | LN_BR | | | | 400258208 |
| LONDON | SCF | SCF | | | | 400059609 |
| HONGKONG | IRD | LN_BR | | | | 400041098 |
| LONDON | COM | OFUT | | | | 400059609 |
| LONDON | CURR | FXD | | | | 400999656 |
| LONDON | IRD | IRS | | | | 400058727 |
| LONDON | SCF | SCF | | | | 400059979 |
| LONDON | CURR | FXD | | | NDF | 400009154 |
| LONDON | CRD | CDS | | | | 400045461 |
| LONDON | SCF | SCF | | | | 400040412 |
| LONDON | CURR | FXD | | | NDS Fixing | 400058727 |
| LONDON | CURR | FXD | | | NDF | 400973688 |
| LONDON | SCF | SCF | | | | 401039314 |
| CHINA HO | CURR | FUT | | FUT | | 400571122 |
| LONDON | SCF | SCF | | | | 400058727 |
| SCAG | CURR | FXD | | | | 400058727 |
| MUMBAI | SCF | SCF | SCF_LTFX_IN | SCF | | |
| 6 | Excluding CPN eligible Payments | No such logic in Ratan |
| 7 | Already included logic | Trade status Control - The trade status has to be VALD or COMP Entity List - H2 Entity list only Excluding Cash Roll Over Trades Amount must greater than 0 and TRN_ID is not 0: SWAP_AGENT is taken in separate queue, which doesn't have TRN_ID is 0 limitation Excluding Client Clearing trades from portfolio level (CLIENT_CLRG_LCH and CLIENT_CLR_HKEX) Excluding ETD payments RFR and Swap Agent payments will be sent via a dedicated payment queue Typology NDS Fixing is handled in a dedicated queue and publish to Ratan via MXML Value date is from T-1 to T+7 business date (excluding 25 Dec and 01 Jan each year) - Not in scope |

Reference