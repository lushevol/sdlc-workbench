# Background

Recently we met several critical issues for release, we need to make a stop and think over how we could avoid these kind of issue for the future, let’s have a retro to review below.

1. 8<sup>th</sup> Aug release, a single cashflow wrongly STPed post Auto netting, which caused 17M USD unexpectedly paid out, fix done by a normal change on 15<sup>th</sup> Aug
2. 18<sup>th</sup> July release, BCS SI stamping issue, which caused an ECR CHG1034441 on 20<sup>th</sup> July

# A single cashflow wrongly STPed

## **Executive Summary**

On 11 Aug 2026, a payment of USD 17.68M was incorrectly released as gross via STP when it should have been routed for NSTP maker-checker approval(“settle as gross” or “manual netting”). The payment was successfully recalled and no financial loss occurred.

The issue was traced to a defect introduced in a recent SSI Stamping service release supporting the FMRP FXO UBER rollout on 8 Aug 2026. The defect resulted in two Auto-Netting control attributes not being passed to the NSTP control service, Consequently the NSTP control could not identify the payment as requiring manual intervention and the payment proceeded via STP.

An interim control(ad-hoc NSTP rule) has been implemented on 12 Aug 2026 to prevent recurrence, and a full impact assessment identified 6 affected payments since deployment. One payment required recall and was successfully recovered, while the remaining five required no corrective action(agreed with client settle as gross). No broader payment processing impact has been identified.

Client / Financial Impact: No client loss, bank loss, liquidity impact, or financial loss was incurred as a result of this incident.

Current Status: The issue has been contained. Interim controls have been implemented and validated, and no additional impacted payments have been identified following the historical review.

Permanent remediation has been identified, along with enhanced validation controls and test coverage, will be released by 29 Aug 2026.

## **Root Cause**

A defect introduced in the SSI Stamping service release on 8 Aug 2026 caused two Auto-Netting control attributes (Is_Auto_Netting and Auto_Netting_Stp_Level) not being passed to the NSTP control, Consequently the NSTP control could not identify the payment as requiring manual intervention and the payment proceeded via STP.

## **Impact Assessment**

The issue was limited to a specific payment scenario where the payment entered the Auto-Netting process and No netting candidate was found, resulting in the payment remaining as a gross payment.

Payments outside this scenario were not affected, No broader payment processing impact has been identified.

A full database review was performed covering the period from the production release date through interim solution put in place:

The review identified 6 payments matching the impact criteria.

Of these:

- 1 payment required funding recall and was successfully recovered.
- 5 payments required no further action.
- No financial loss was incurred.

** **

## **Why Testing Did Not Detect the Issue**

The regression test suite did not include a test case covering the specific Auto-Netting exception flow where payments settle as gross and require NSTP validation. Consequently, the defect was not detected during pre-production testing.

## **Action Plan**

**Immediate Actions **

1. Interim NSTP rule implemented to prevent recurrence.
2. Full historical scan completed to identify impacted payments.
3. Funding for the affected payment successfully recalled.

** **

**Strategic Fixes by 29 Aug 2026**

1. Correct the SSI Stamping service defect to ensure the attributes Is_Auto_Netting and Auto_Netting_Stp_Level are always propagated correctly.
2. Enhance NSTP Check controls to enforce mandatory field validation. Missing control attributes will result in a hard stop and exception rather than STP.
3. Strengthen test coverage by adding explicit regression test cases covering Auto-Netting, NSTP exceptions, and missing control attribute scenarios.

| | Fields | RuleEngineFields | Test evidence for Uber | Rule | Rule Dependency | Result |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Cashflow.Auto_Netting_Stp_Level | CASHFLOW__AUTO_NETTING_STP_LEVEL | case no: TC-STML-API-RULE-002-18 cashflow id: N00000530433 (stg env) | Cashflow.Is_Auto_Netting == true AND Cashflow.Auto_Netting_Stp_Level == "NSTP_MAKER_CHECKER" | Yes | Pass |
| 2 | Cashflow.Booking_System_Event | CASHFLOW__BOOKING_SYSTEM_EVENT | case no: TC-STML-API-RULE-001-47 cashflow id: 843089981849 (stg env) | Cashflow__Booking_System_Event matches "(?i)AmendmentError" | Yes | Pass |
| 3 | Cashflow.Cashflow_Affirmation_Status | CASHFLOW__CASHFLOW_AFFIRMATION_STATUS | case no: TC-STML-API-RULE-001-48 cashflow id: 000000378285 (stg env) | Cashflow__Status_Event_Type == "RevertToQueued" && Cashflow__Cashflow_Affirmation_Status == "Affirmed" | Yes | Pass |
| 4 | Cashflow.Cashflow_Amount_USD_Transfered | CASHFLOW__CASHFLOW_AMOUNT_USD_TRANSFERED | case no: TC-STML-API-RULE-001-01 cashflow id: 0478188598 (stg env) | Cashflow__Cashflow_Amount_USD_Transfered > 10 && Cashflow__Cashflow_Id in ( "M06789535204", "0478188598" ) | Yes | Pass |
| 5 | Cashflow.Cashflow_Event_Reason | CASHFLOW__CASHFLOW_EVENT_REASON | case no: TC-STML-API-RULE-002-07 cashflow id: 927890937572 (fmrp1 env) | Cashflow.Cashflow_Event_Reason==Reversal | Yes | Pass |
| 6 | Cashflow.Cashflow_Event_Type | CASHFLOW__CASHFLOW_EVENT_TYPE | case no: TC-STML-API-RULE-001-48 cashflow id: 159603004661 (stg env) | Data_Flow__Data_Source_System matches "(?i)^Stella$" && Instrument_Common__ISDA_Taxonomy in ("InterestRate:IRSwap:FixedFloat","InterestRate:IRSwap:OIS","InterestRate:IRSwap:FloatFloat","InterestRate:IRSwap:Basis","InterestRate:IRSwap:FixedFixed") && Cashflow__Payment_Type in ("Coupon/Fixed","Coupon/Float") && Cashflow__Cashflow_Event_Type not matches "(?i)Withdrawal" && (Cashflow__Netting_Id == null || Cashflow__Netting_Id == "") | Yes | Pass |
| 7 | Cashflow.Clearing_Alpha | CASHFLOW__CLEARING_ALPHA | case no: TC-STML-API-RULE-001-52 cashflow id: M03542405417 (stg env) | Cashflow.Clearing_Alpha == true | Yes | Pass |
| 8 | Cashflow.Is_Adhoc_Net | CASHFLOW__IS_ADHOC_NET | case no: TC-STML-API-RULE-001-54 cashflow id: N00000530464 (stg env) | Cashflow__Is_Adhoc_Net == true | Yes | Pass |
| 9 | Cashflow.Is_Auto_Netting | CASHFLOW__IS_AUTO_NETTING | case no: TC-STML-API-RULE-002-18 cashflow id: N00000530768 (stg env) | Cashflow.Is_Auto_Netting == true AND Cashflow.Auto_Netting_Stp_Level == "NSTP_MAKER_CHECKER" | Yes | Pass |
| 10 | Cashflow.Is_Cashflow_Reinstate | CASHFLOW__IS_CASHFLOW_REINSTATE | case no: TC-STML-API-RULE-002-21 cashflow id: 842540150447 (stg env) | Cashflow.Is_Cashflow_Reinstate==true | Yes | Pass |
| 11 | Cashflow.Is_Cashflow_SettleAsGross | CASHFLOW__IS_CASHFLOW_SETTLEASGROSS | case no: TC-STML-API-RULE-001-13 cashflow id: 995126792176 (stg env) | CASHFLOW__IS_CASHFLOW_SETTLEASGROSS == true && Cashflow__Cashflow_Id = 014609102602 | Yes | Pass |
| 12 | Cashflow.Is_Cashflow_Unnet | CASHFLOW__IS_CASHFLOW_UNNET | case no: TC-STML-API-RULE-002-22 cashflow id: 644338649015 (stg env) | Cashflow.Is_Cashflow_Unnet==true | Yes | Pass |
| 13 | Cashflow.Is_Cashflow_Unsplit | CASHFLOW__IS_CASHFLOW_UNSPLIT | case no: TC-STML-API-RULE-002-16 cashflow id: 247008457116 (stg env) | Cashflow__Is_Cashflow_Unsplit == true | Yes | Pass |
| 14 | Cashflow.Is_Commodity | CASHFLOW__IS_COMMODITY | case no: TC-STML-API-RULE-001-60 cashflow id: N00000530467 (stg env) | Cashflow.Is_Commodity == true | Yes | Pass |
| 15 | Cashflow.Is_Netting_Required | CASHFLOW__IS_NETTING_REQUIRED | 000000311570 prod on 2026-08-13 | Cashflow__Is_Netting_Required == true | Yes | Pass, LOANIQ only, SCBML from upstream |
| 16 | Cashflow.Is_Payment_Date_Before_Today | CASHFLOW__IS_PAYMENT_DATE_BEFORE_TODAY | case no: TC-STML-API-RULE-001-63 cashflow id: 207034875364 (stg env) | Cashflow__Is_Payment_Date_Before_Today == true && Cashflow__Cashflow_Id in ( "M06762566064", "207034875364" ) | Yes | Pass |
| 17 | Cashflow.Is_Payment_Date_Holiday | CASHFLOW__IS_PAYMENT_DATE_HOLIDAY | case no: TC-STML-API-RULE-001-03 cashflow id: 073544300103 (stg env) | Cashflow__Is_Payment_Date_Holiday == true && Cashflow__Cashflow_Id in ( "M06043039665", "073544300103" ) | Yes | Pass |
| 18 | Cashflow.Is_Split_Amend_Amount | CASHFLOW__IS_SPLIT_AMEND_AMOUNT | case no: TC-STML-API-RULE-002-08 cashflow id: S00000530387 (stg env) | Cashflow.Is_Split_Amend_Amount == true | Yes | Pass |
| 19 | Cashflow.Is_STP | CASHFLOW__IS_STP | case no: TC-STML-API-RULE-002-08 cashflow id: 462747996355 (stg env) | Cashflow__Is_STP == false && Cashflow__Cashflow_Id in ( "462747996355" ) | Yes | Pass |
| 20 | Cashflow.Is_Unaffirmed_Processed | CASHFLOW__IS_UNAFFIRMED_PROCESSED | case no: TC-STML-API-RULE-001-79 cashflow id: 962039972359 (stg env) | Cashflow__Is_Unaffirmed_Processed == true && Cashflow__Cashflow_Id in ( "229477573612", "410685554365" ) | Yes | Pass |
| 21 | Cashflow.Is_Withdrawal_On_Component | CASHFLOW__IS_WITHDRAWAL_ON_COMPONENT | case no: TC-STML-API-RULE-002-19 cashflow id: 687515605303 (stg env) | Cashflow.Is_Withdrawal_On_Component==true | Yes | Pass |
| 22 | Cashflow.Is_Withdrawal_On_Split | CASHFLOW__IS_WITHDRAWAL_ON_SPLIT | case no: TC-STML-API-RULE-002-20 cashflow id: (stg env) | Cashflow.Is_Withdrawal_On_Split == true | Yes | Pass |
| 23 | Cashflow.Netting_Id | CASHFLOW__NETTING_ID | case no: TC-STML-API-RULE-002-02 cashflow id: N00000221617 (fmrp1 env) | Cashflow__Netting_Id != null && Cashflow__Netting_Id != "" && Cashflow__Is_Auto_Netting == false && Cashflow__Payment_Type != "IRS Netting" | Yes | Pass |
| 24 | Cashflow.Pay_Receive_Indicator | CASHFLOW__PAY_RECEIVE_INDICATOR | case no: TC-STML-API-RULE-001-74 cashflow id: N00000221617 (fmrp1 env) | Cashflow__Pay_Receive_Indicator == "Receive" && Cashflow__Cashflow_Id in ( "469373948218" ) | Yes | Pass |
| 25 | Cashflow.Payment_Amount | CASHFLOW__PAYMENT_AMOUNT | case no: TC-STML-API-RULE-001-36 cashflow id: 3310557479 | Cashflow__Cashflow_Id == "3310557479" && Cashflow__Payment_Amount == 10 | Yes | Pass |
| 26 | Cashflow.Payment_Currency | CASHFLOW__PAYMENT_CURRENCY | case no: TC-STML-API-RULE-001-76 cashflow id: 602773983908 | Cashflow__Payment_Currency == "USD" && Cashflow__Cashflow_Id in ( "602773983908" ) | Yes | Pass |
| 27 | Cashflow.Payment_Date | CASHFLOW__PAYMENT_DATE | case no: TC-STML-API-RULE-001-77 cashflow id: 679833919136 | Cashflow__Payment_Date equals "2026-08-21" && Cashflow__Cashflow_Id in ( "679833919136" ) | Yes | Pass |
| 28 | Cashflow.Payment_Payer_Party_Reference | CASHFLOW__PAYMENT_PAYER_PARTY_REFERENCE | case no: TC-STML-API-RULE-001-78 cashflow id: 240985181043 | Cashflow__Payment_Payer_Party_Reference == "party2" && Cashflow__Cashflow_Id in ( "240985181043" ) | Yes | Pass |
| 29 | Cashflow.Payment_Type | CASHFLOW__PAYMENT_TYPE | case no: TC-STML-API-RULE-001-79 cashflow id: 240985181043 | Cashflow__Payment_Type == "Cashflow" && Cashflow__Cashflow_Id in ( "835952737422" ) | Yes | Pass |
| 30 | Cashflow.Splitting_Id | CASHFLOW__SPLITTING_ID | case no: TC-STML-API-RULE-001-42 cashflow id: S00000530435 | Cashflow__Splitting_Id != null && Cashflow__Splitting_Id != "" | Yes | Pass |
| 31 | Cashflow.Status_Event_Type | CASHFLOW__STATUS_EVENT_TYPE | case no: TC-STML-API-RULE-001-33 cashflow id: 007943529217 (PROD) | Cashflow__Status_Event_Type == "RevertToQueued" && Cashflow__Cashflow_Affirmation_Status == "Affirmed" | Yes | Pass |
| 32 | Entity.Booking_Entity_SCI_FMCODE | ENTITY__BOOKING_ENTITY_SCI_FMCODE | case no: TC-STML-API-RULE-001-08 cashflow id: 371044822180 (fmrp1 env) | Entity__Booking_Entity_SCI_FMCODE = "SCB CHINA*XMN" && Cashflow__Cashflow_Id in ( "M00300677879 ","890352734586" ) | Yes | Pass |
| 33 | Entity.Counterparty_Client_Type | ENTITY__COUNTERPARTY_CLIENT_TYPE | case no: TC-STML-API-RULE-001-07 cfid: M08953174269 (fmrp1 env) case no: TC-STML-API-RULE-001-07 cashflow id: 371044822180 (fmrp1 env) | Entity__Counterparty_Client_Type == "CLGHSE" && Cashflow__Cashflow_Id in ( "M08953174269","371044822180" ) | Yes | Pass |
| 34 | Instrument_Common.ISDA_Taxonomy | INSTRUMENT_COMMON__ISDA_TAXONOMY | case no: TC-STML-API-RULE-001-79 cashflow id: 962039972359 (stg env) | Cashflow__Payment_Type == "Cashflow" && Cashflow__Cashflow_Id in ( "${cashflowId}" ) && Data_Flow__Data_Source_System == "Stella" && Entity__Booking_Entity_SCI_FMID == "400085753" && Entity__Counterparty_Country_ISO_Code == "EG" && Entity__Counterparty_SCI_FMID == "400899993" && Instrument_Common__Financial_Instrument_Code == "SRCXXX" && Instrument_Common__ISDA_Taxonomy == "Commodity:Metals:Precious:SpotFwd:Physical" && Settlement_Instruction__Account__Beneficiary_Account_Name == "" && Settlement_Instruction__Account__Booking_Entity_Correspondent_Street_Address == "1095 AVENUE OF THE AMERICAS" && Settlement_Instruction__Account__SCB_Nostro_Account_Number == "USD MAIN" && Settlement_Instruction__Account__SCB_Nostro_Account_Type == "NOS" | Yes | Pass |
| 35 | Instrument_Common.Financial_Instrument_Code | INSTRUMENT_COMMON__FINANCIAL_INSTRUMENT_CODE | Yes | Pass |
| 36 | Data_Flow.Data_Source_System | DATA_FLOW__DATA_SOURCE_SYSTEM | Yes | Pass |
| 37 | Entity.Booking_Entity_SCI_FMID | ENTITY__BOOKING_ENTITY_SCI_FMID | Yes | Pass |
| 38 | Entity.Counterparty_SCI_FMID | ENTITY__COUNTERPARTY_SCI_FMID | Yes | Pass |
| 39 | Trade.Entity.Counterparty_Country_ISO_Code | ENTITY__COUNTERPARTY_COUNTRY_ISO_CODE | Yes | Pass |
| 40 | Settlement_Instruction.Account.SCB_Nostro_Account_Type | SETTLEMENT_INSTRUCTION__ACCOUNT__SCB_NOSTRO_ACCOUNT_TYPE | Yes | Pass-Sequencial SSI NSTP |
| 41 | Settlement_Instruction.Account.SCB_Nostro_Account_Number | SETTLEMENT_INSTRUCTION__ACCOUNT__SCB_NOSTRO_ACCOUNT_NUMBER | Yes | Pass-Sequencial SSI NSTP |
| 42 | Settlement_Instruction.Account.Beneficiary_Account_Name | SETTLEMENT_INSTRUCTION__ACCOUNT__BENEFICIARY_ACCOUNT_NAME | Yes | Pass-Sequencial SSI NSTP |
| 43 | Settlement_Instruction.Account.Beneficiary_Street_Address | SETTLEMENT_INSTRUCTION__ACCOUNT__BENEFICIARY_STREET_ADDRESS | Yes | Pass-Sequencial SSI NSTP |
| 44 | Settlement_Instruction.SSI_Unique_Id | SETTLEMENT_INSTRUCTION__SSI_UNIQUE_ID | case no: TC-STML-API-RULE-001-103-06 cashflow id: 865489911862 (stg env) | Settlement_Instruction__SSI_Unique_Id == "46820181" && Cashflow__Cashflow_Id in ( "865489911862" ) | Yes | Pass-Sequencial SSI NSTP |
| 45 | Entity.Counterparty_SCI_BIC_Code | ENTITY__COUNTERPARTY_SCI_BIC_CODE | case no: TC-STML-API-RULE-001-09 cfid: M06471139689 (fmrp1 env) case no: TC-STML-API-RULE-001-09 cashflow id: 435338219054 (fmrp1 env) | Entity__Counterparty_SCI_BIC_Code == "SCBLCNSXSHA" && Cashflow__Cashflow_Id in ( "M06471139689","435338219054" ) | Yes | Pass |
| 46 | Entity.Counterparty_SCI_BIC_Net_Flag | ENTITY__COUNTERPARTY_SCI_BIC_NET_FLAG | case no: TC-STML-API-RULE-001-11 cfid: M06217266371 (fmrp1 env) case no: TC-STML-API-RULE-001-11 cashflow id: 254178098678 (fmrp1 env) | Entity__Counterparty_SCI_BIC_Net_Flag == "N" && Cashflow__Cashflow_Id in ( "M06217266371","254178098678" ) | Yes | Pass |
| 47 | Entity.Counterparty_SCI_FMCODE | ENTITY__COUNTERPARTY_SCI_FMCODE | case no: TC-STML-API-RULE-001-10 cfid: M07627999744 (fmrp1 env) case no: TC-STML-API-RULE-001-10 cashflow id: 284166463181 (fmrp1 env) | Entity__Counterparty_SCI_FMCODE == "SCB SHANGH*SHA" && Cashflow__Cashflow_Id in ( "M07627999744","284166463181" ) | Yes | Pass |
| 48 | fmEntity.fmAccount.fmType | FMENTITY__FMACCOUNT__FMTYPE | case no: TC-STML-API-RULE-001-04 cfid: M08953174269 (fmrp1 env) case no: TC-STML-API-RULE-001-07 cashflow id: 371044822180 (fmrp1 env) | Entity__Counterparty_Client_Type == "CLGHSE" && Cashflow__Cashflow_Id in ( "M08953174269","371044822180" ) | Yes | Pass |
| 49 | Portfolio.Booking_Entity_Trade_Portfolio_Name | PORTFOLIO__BOOKING_ENTITY_TRADE_PORTFOLIO_NAME | case no: TC-STML-API-RULE-001-105 cfid: 105954519741 (stg env) | Portfolio__Booking_Entity_Trade_Portfolio_Name == "STL-FX-EG" && Cashflow__Cashflow_Id in ( "105954519741" ) | Yes | Pass |
| 50 | Settlement_Method | SETTLEMENT_METHOD | case no: TC-STML-API-RULE-002-22 cashflow id: 410519002040 (stg env) | Settlement_Method==DVP | Yes | Pass |
| 51 | Trade.Contract_Typology | CONTRACT_TYPOLOGY | case no: TC-STML-API-RULE-001-103-07 cashflow id: 582913888984 (stg env) | Contract_Typology == "FX_KIKOF" && Cashflow__Cashflow_Id in ( "582913888984" ) | Yes | Pass |
| 52 | Trade.Data_Flow.Source_Stack_Flow_Name | Data_Flow__Source_Stack_Flow_Name | case no: TC-STML-API-RULE-001-103-08 cashflow id: 972413746926 (stg env) | Trade.Entity.Counterparty_Country_ISO_Code | Yes | Pass |
| 53 | Trade.Is_Duplicate_Booking | IS_DUPLICATE_BOOKING | case no: TC-STML-API-RULE-009-006 cashflow id: 058442776797 | Cashflow.Cashflow_Id == "058442776797" AND Is_Duplicate_Booking == false | Yes | Pass |
| 54 | Trade.Lien_Monitoring | LIEN_MONITORING | case no: TC-STML-API-RULE-002-20 cashflow id: 812863979390 (stg env) | (Cashflow__Lien_Monitoring == "Y" || (Lien_Monitoring != null && Lien_Monitoring != "")) | Not Yet | Pass |
| 55 | Trade.Logical_Package_Id | LOGICAL_PACKAGE_ID | case no: TC-STML-API-RULE-002-20 cashflow id: 551636538646 (stg env) | Logical_Package_Id == "779978" && Position_Id =="22370895" && Trade_Id == "22370895" && Cashflow__Cashflow_Id in ( "551636538646" ) | Yes | Pass |
| 56 | Trade.Parent_Position_Id | PARENT_POSITION_ID | case no: TC-STML-API-RULE-001-103-05 cashflow id: 186264912751 (stg env) | Parent_Position_Id == "77146948" && Cashflow__Cashflow_Id in ( "186264912751" ) | Yes | Pass |
| 57 | Trade_Id | TRADE_ID | case no: TC-STML-API-RULE-001-103-04 cashflow id: 378355457061 (stg env) | Position_Id == "88013441" && Trade_Id == "88013441" && Cashflow__Cashflow_Id in ( "378355457061" ) | Yes | Pass |
| 58 | Trade_Original_Source_System_Name | TRADE_ORIGINAL_SOURCE_SYSTEM_NAME | case no: TC-STML-API-RULE-009-005 cashflow id: 719488718527 | Cashflow.Cashflow_Id == "719488718527" AND Trade_Original_Source_System_Name == "S2BX" | Yes | Pass |
| 59 | Trade_Purpose | TRADE_PURPOSE | case no: TC-STML-API-RULE-009-004 cashflow id: 912495865180 | Cashflow.Cashflow_Id == "912495865180" AND Trade_Purpose == "TC-STML-API-RULE-009-004" | Yes | Pass |
| 60 | Cashflow.Cashflow_Id | CASHFLOW__CASHFLOW_ID | case no: TC-STML-API-RULE-002-22 cashflow id: 378355457061 (stg env) | Position_Id == "88013441" && Trade_Id == "88013441" && Cashflow__Cashflow_Id in ( "378355457061" ) | Not Yet | Pass |
| 61 | Cashflow.Is_Cashflow_Swift_Unsuppress | CASHFLOW__IS_CASHFLOW_SWIFT_UNSUPPRESS | case no: TC-STML-API-RULE-001-40 cashflow id: 9715481932 | Cashflow__Cashflow_Id == "9715481932" && Cashflow__Is_Cashflow_Swift_Unsuppress == true | Not Yet | Pass |
| 62 | Cashflow.Is_Cashflow_Unsuppress | CASHFLOW__IS_CASHFLOW_UNSUPPRESS | case no: TC-STML-API-RULE-001-43 cashflow id: 2114981661 | Cashflow__Cashflow_Id == "2114981661" && Cashflow__Is_Cashflow_Unsuppress == true | Not Yet | Pass |
| 63 | Delivery_Method | DELIVERY_METHOD | case no: TC-STML-API-RULE-009-001 cashflow id: N00000530522 | Delivery_Method == "Cash" | Not Yet | Pass |
| 64 | Entity.Counterparty_SCI_DOMICILE_COUNTRY | ENTITY__COUNTERPARTY_SCI_DOMICILE_COUNTRY | case no: TC-STML-API-RULE-001-35 cashflow id: 3534027925 | Cashflow__Cashflow_Id == "3534027925" && Entity__Counterparty_SCI_DOMICILE_COUNTRY == "EG" | Not Yet | Pass |
| 65 | Trade.Is_Client_Leg | TRADE__IS_CLIENT_LEG | case no: TC-STML-API-RULE-009-001 cashflow id: 903131496204 | Is_Client_Leg == false && Cashflow__Cashflow_Id in ( "903131496204" ) | Not Yet | Pass |
| 66 | ENTITY.COUNTERPARTY_IS_INTERNAL | ENTITY__COUNTERPARTY_IS_INTERNAL | case no: TC-STML-API-RULE-001-34 cashflow id: 5253739784 | Cashflow__Cashflow_Id == "5253739784" && Entity__Counterparty_Is_Internal == false | Not Yet | Pass |
| 67 | Cashflow.Is_Pending_Fixing | CASHFLOW__IS_PENDING_FIXING | case no: TC-STML-API-RULE-001-64 cashflow id: M07228677047 (stg env) | Cashflow__Is_Pending_Fixing == false && Cashflow__Cashflow_Id in ( "M07228677047" ) | Yes | Pass |
| 68 | Cashflow.Lien_Monitoring | CASHFLOW__LIEN_MONITORING | case no: TC-STML-API-RULE-001-69 cashflow id: M02320490932 (stg env) | (Cashflow__Lien_Monitoring == "Y" || (Lien_Monitoring != null && Lien_Monitoring != "")) | Yes | Pass |
| 69 | Cashflow.Murex_Structure_Id | CASHFLOW__MUREX_STRUCTURE_ID | case no: TC-STML-API-RULE-001-71 cashflow id: 812863979390 (stg env) | Cashflow.Murex_Structure_Id != null AND Cashflow.Murex_Structure_Id != "" AND Cashflow.Murex_Structure_Id != "0" | Yes | Pass |
| 70 | Cashflow.ND_Parent_Typology | CASHFLOW__ND_PARENT_TYPOLOGY | case no: TC-STML-API-RULE-001-12 cfid: M01878141094 (stg env) | CASHFLOW__ND_PARENT_TYPOLOGY == true && Cashflow__Cashflow_Id = M01878141094 | Yes | Pass |
| 71 | Cashflow.Pending_Fixing_Flag | CASHFLOW__PENDING_FIXING_FLAG | Existing test case for Murex case no: TC-STML-API-RULE-001-32 cfid: M03322347396 (uat4 env) | | Yes | Pass |
| 72 | Entity.Counterparty_Murex_Display_Shortcode | ENTITY__COUNTERPARTY_MUREX_DISPLAY_SHORTCODE | Existing test case for Murex case no: TC-STML-API-RULE-001-32 cfid: M03322347396 (uat4 env) | | Yes | Pass |
| 73 | Instrument_Common.Murex_Product_Family | INSTRUMENT_COMMON__MUREX_PRODUCT_FAMILY | Existing test case for Murex case no: TC-STML-API-RULE-001-32 cfid: M03322347396 (uat4 env) | | Yes | Pass |
| 74 | Instrument_Common.Murex_Product_Group | INSTRUMENT_COMMON__MUREX_PRODUCT_GROUP | Existing test case for Murex case no: TC-STML-API-RULE-001-32 cfid: M03322347396 (uat4 env) | | Yes | Pass |
| 75 | Instrument_Common.Murex_Product_Strategy | INSTRUMENT_COMMON__MUREX_PRODUCT_STRATEGY | Existing test case for Murex case no: TC-STML-API-RULE-001-32 cfid: M03322347396 (uat4 env) | | Yes | Pass |
| 76 | Instrument_Common.Murex_Product_Type | INSTRUMENT_COMMON__MUREX_PRODUCT_TYPE | Existing test case for Murex case no: TC-STML-API-RULE-001-32 cfid: M03322347396 (uat4 env) | | Yes | Pass |
| 77 | Instrument_Common.Murex_Product_Typology | INSTRUMENT_COMMON__MUREX_PRODUCT_TYPOLOGY | Existing test case for Murex case no: TC-STML-API-RULE-001-32 cfid: M03322347396 (uat4 env) | | Yes | Pass |
| 78 | BCS_Parent_Trade_Id | BCS_PARENT_TRADE_ID | Existing test case for Murex case no: TC-STML-API-RULE-001-32 cfid: M03322347396 (uat4 env) | | Yes | Pass |
| 79 | Cashflow.Duplicate_NDS_FXD | CASHFLOW__DUPLICATE_NDS_FXD | Existing test case for Murex case no: TC-STML-API-RULE-001-32 cfid: M03322347396 (uat4 env) | Cashflow.Duplicate_NDS_FXD != null AND Cashflow.Duplicate_NDS_FXD != "" | Yes | Pass |
| 80 | fmEntity.legalEntity.operationStatus1Value | FMENTITY__LEGALENTITY__OPERATIONSTATUS1VALUE | Existing test case case no: TC-STML-API-RULE-002-05 cfid: 561370143963 (uat4 env) | PROD NSTP rule: GSAM | Yes | Pass |
| 81 | Trade.Swap_Agent_Id | SWAP_AGENT_ID | FMRP 8.0 UAT Covered FMRP1: - Test Data: trade id 8027630462 | (Cashflow__Netting_Id == null || Cashflow__Netting_Id == "") && ((Instrument_Common__Murex_Product_Strategy == "SWAP_AGENT" && Cashflow__Payment_Type == "Interim MTM") || ((Swap_Agent_Id != null && Swap_Agent_Id != "") && Cashflow__Payment_Type matches "(?i).*AmortizationExchange.*")) | | |

## Where is the GAP?

## What We Could Do Better

# BCS SI stamping issue

## **<u>Issue Summary:</u>**

BCS payments are currently experiencing SSI stamping failures, impacting 291 payments, incident **INC4844109** raised for tracking the issue

## **<u>Root Cause:</u>**

The issue is tied to a library update implemented to address a vulnerability. Notably, this service hasn't been upgraded in the past two years, which could be contributing to the problem.

## **<u>Solution:</u>**

Upgrade a java lib in BCS SSI stamping service.

## **<u>Defer Impact:</u>**

If we defer implementing this fix, there will be a delay in the BSC settlement processing, which we want to avoid.

**<u>Implementation Time</u>****:** 2:30 PM 20<sup>th</sup> July 2026

## Where is the GAP?

## What We Could Do Better