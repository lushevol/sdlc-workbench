# Background

For India market there're trades booked with CCIL counterparties and settlement ops would net these to one cashflow against the CCIL central counterparty. Swift generation would be bypassed for the netting resultant cashflow and only accounting required.

# CCIL cashflows samples & Netting in Murex 2.11

- **Guaranteed** CCIL cashflows a) Trades are cleared in CCIL and Cashflows are novated to CCIL central counterparty( column L) b) Cashflows are netted to one netting resultant cashflow which facing CCIL central counterparty ![image2024-4-10_15-32-41.png](attachments/image2024-4-10_15-32-41.png)
- Non Guaranteed CCIL Cashflows a) Trade are not cleared in CCIL and cashflows are still booked with original counterparty b) Multi component cashflows with different counterparties are netted to one netting resultant cashflow which the counterparty is the pre-defined CCIL central counterparty ![image2024-4-10_15-36-50.png](attachments/image2024-4-10_15-36-50.png)

# Problem statement of current BAU

- There's no golden source for Non Guaranteed CCIL client static data, it's manually maintained in Murex 2.11 logical static data.
- There's no clear ownership for the Murex 2.11 CCIL static data
- Data quality issue of the CCIL client static

# Strategy Requirement & Approach(FMRP)

- Settlement Requirement 1. Ratan can hold Guaranteed & Non Guaranteed cashflows as NSTP 2. Quick filter on the Guaranteed & Non Guaranteed cashflows from GUI 3. Different Netting actions on the Guaranteed & Non Guaranteed cashflows in Ratan 4. Pre-netting review page to help ops to identify the discrepancy between SCB & CCIL system( exiting function).

- Strategy approach 1. There would be golden source of Non Guaranteed CCIL client list 2. Stella would identify the Guaranteed & Non Guaranteed CCIL cashflows and stamp the settlement method as 'CCIL' 3. Business rules would be created to stop the STP of the Guaranteed & Non Guaranteed cashflows 4. Ratan to build the capacity for settlement ops to quickly filter the Guaranteed & Non Guaranteed cashflows 5. Build the netting capacity for settlement ops to net the CCIL cashflows - Netting Action on Guaranteed CCIL cashflows( Existing netting action) - Netting Action on the Non Guaranteed CCIL cashflows ( To Be built)

# CCIL Netting Function Flow - Tactical Solution

India is one of the H1 2024 FMRP cashflow migration market and CCIL netting is mandatory requirement for India, strategy approach won't be ready by the release timeline and we have to look for the tactical solution to cater for the business requirement.

Proposed tactical solution as below.

- Copy the Murex 2.11 CCIL client static data to Ratan and maintained as logical static, data correction & review required **- Tactical and would throw away after Murex 2.11 Decommission**
- System identify the Non Guaranteed CCIL cashflows with this Ratan local static data, stamp these cashflow with settlement method == 'CCIL'. **- Tactical and would throw away after Murex 2.11 Decommission**
- Business rules would be created to stop the STP of the Guaranteed & Non Guaranteed cashflows - **Generic and can work for Strategy flow**
- Ratan to build the capacity for settlement ops to quickly filter the Guaranteed & Non Guaranteed cashflows - **Generic and can work for Strategy flow**
- Build the netting capacity for settlement ops to net the CCIL cashflows - **Generic and can work for Strategy flow** - Netting Action on Guaranteed CCIL cashflows( Existing netting action) - Netting Action on the Non Guaranteed CCIL cashflows ( To Be built)

# Cashflows eligible for Bilateral Netting & CCIL Netting

Given we're leverage the exiting bilateral netting for the Guaranteed cashflows, below are the updated matrix for bilateral netting.

| **Bilateral Netting Criteria** | **Conditions** | **Validation in GUI** | **Validation from backend** |
| --- | --- | --- | --- |
| Generic | Settlement Method != CCIL and Cashflow Status in (WAITING, READY) | Yes | Yes |
| CCIL Guaranteed | Settlement Method == CCIL and Cashflow Status in (WAITING) and sub status type =='Pending Netting' and Counterparty FMID ==400021949 | Yes | Yes |

| **CCIL Netting Criteria** | **Conditions** | **Validation in GUI** | **Validation from backend** |
| --- | --- | --- | --- |
| Non Guaranteed | Settlement Method == CCIL and Cashflow Status in (WAITING) and sub status type =='Pending Netting' and Counterparty FMID !=400021949 | Yes | Yes |

# User cases

1. Happy Case: - Guaranteed cashflows had been fully novated to central counterparty CCIL/MMB in Murex2.11. - Ratan had segregated the Guaranteed & Non Guaranteed cashflows, ops review these cashflows and good to perform netting. 2 netting resultant cashflows populated - There's no discrepancy between SCB netting resultant amount VS CCIL system, all good. | **Netting Action** | **Cashflow ID** | **Booking Entity** | **Counterparty FMID** | **Counterpart** | **Settlement Method** | **Sub Status Type** | **Cashflow Status** | **Currency** | **Amount** | **Pay/Receive** | **Value** | **Family** | **Group** | **Typology** | | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | | **Bilateral Netting(Guaranteed)** | M0099544835 | MUMBAI | 400021949 | CCIL/MMB | CCIL | Pending Netting | WAITING | INO | 100.00 | Receive | 4/26/2024 | IRD | IRS | Vanilla IR Swap | | M0099544838 | MUMBAI | 400021949 | CCIL/MMB | CCIL | Pending Netting | WAITING | INO | 100.00 | Pay | 4/27/2024 | IRD | IRS | Vanilla IR Swap | | M0099544839 | MUMBAI | 400021949 | CCIL/MMB | CCIL | Pending Netting | WAITING | INO | 200.00 | Pay | 4/28/2024 | IRD | IRS | Vanilla IR Swap | | **Netting Resultant cashflow** | N0000000001 | MUMBAI | 400021949 | CCIL/MMB | Cash | Pending Exception | WAITING | INO | 200 | Pay | 4/28/2024 | IRD | IRS | Vanilla IR Swap | | | | **CCIL Netting(Non Guaranteed)** | M0099592071 | MUMBAI | 300070884 | BOA/MMB | CCIL | Pending Netting | WAITING | INO | 100.00 | Pay | 4/26/2024 | IRD | IRS | Vanilla IR Swap | | M0099544834 | MUMBAI | 10040528 | CAI/MMB | CCIL | Pending Netting | WAITING | INO | 150.00 | Pay | 4/27/2024 | IRD | IRS | Vanilla IR Swap | | M0097489984 | MUMBAI | 155001881 | CMB/MMB | CCIL | Pending Netting | WAITING | INO | 50.00 | Receive | 4/28/2024 | IRD | IRS | Vanilla IR Swap | | **Netting Resultant cashflow** | N00000000002 | MUMBAI | 400021949 | CCIL/MMB | Cash | Pending Exception | WAITING | INO | 200 | Pay | 4/28/2024 | IRD | IRS | Vanilla IR Swap |
2. Guaranteed cashflows are not full novated E.g. the below counterpart 300070884 are suppose be novated to central CCIL counterpart 400021949 but MO didn't done that yet intraday, these to be novated cashflows would always fall into the Non Guaranteed cashflow list. Settlement ops would do the pre-netting review and recognize the dispute between SCB netting & CCIL system and do the necessary investigation, when address the to be novated cashflows settlement ops would approach MO to perform the novation. | **Netting Action** | **Cashflow ID** | **Booking Entity** | **Counterparty FMID** | **Counterpart** | **Settlement Method** | **Sub Status Type** | **Cashflow Status** | **Currency** | **Amount** | **Pay/Receive** | **Value** | **Family** | **Group** | **Typology** | | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | | **Bilateral Netting(Guaranteed)** | M0099544835 | MUMBAI | 400021949 | CCIL/MMB | CCIL | Pending Netting | WAITING | INO | 100.00 | Receive | 4/26/2024 | IRD | IRS | Vanilla IR Swap | | M0099544838 | MUMBAI | 400021949 | CCIL/MMB | CCIL | Pending Netting | WAITING | INO | 100.00 | Pay | 4/27/2024 | IRD | IRS | Vanilla IR Swap | | M0099544839 | MUMBAI | 400021949 | CCIL/MMB | CCIL | Pending Netting | WAITING | INO | 200.00 | Pay | 4/28/2024 | IRD | IRS | Vanilla IR Swap | | | | **CCIL Netting(Non Guaranteed)** | M0099592071 | MUMBAI | 300070884 | BOA/MMB | CCIL | Pending Netting | WAITING | INO | 100.00 | Pay | 4/26/2024 | IRD | IRS | Vanilla IR Swap | | M0099544834 | MUMBAI | 10040528 | CAI/MMB | CCIL | Pending Netting | WAITING | INO | 150.00 | Pay | 4/27/2024 | IRD | IRS | Vanilla IR Swap | | M0097489984 | MUMBAI | 155001881 | CMB/MMB | CCIL | Pending Netting | WAITING | INO | 50.00 | Receive | 4/28/2024 | IRD | IRS | Vanilla IR Swap |
3. CCIL Guaranteed cashflows & Non CCIL Cashflows netting? **there're some cashflows booked with 400021949 on the other products, but there's no requirement to net these with the CCIL guaranteed cashflows.** | **Netting Action** | **Cashflow ID** | **Booking Entity** | **Counterparty FMID** | **Counterpart** | **Settlement Method** | **Sub Status Type** | **Cashflow Status** | **Currency** | **Amount** | **Pay/Receive** | **Value** | **Family** | **Group** | **Typology** | | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | | **Bilateral Netting(Guaranteed)** | M0099544835 | MUMBAI | 400021949 | CCIL/MMB | CCIL | Pending Netting | WAITING | INO | 100.00 | Receive | 4/26/2024 | **IRD** | **IRS** | Vanilla IR Swap | | M0099544838 | MUMBAI | 400021949 | CCIL/MMB | CCIL | Pending Netting | WAITING | INO | 100.00 | Pay | 4/27/2024 | **IRD** | **IRS** | Vanilla IR Swap | | M0099544839 | MUMBAI | 400021949 | CCIL/MMB | CCIL | Pending Netting | WAITING | INO | 200.00 | Pay | 4/28/2024 | **IRD** | **IRS** | Vanilla IR Swap | | | M0099544840 | MUMBAI | 400021949 | CCIL/MMB | CASH | Pending Netting | WAITING | INO | 100.00 | Pay | 4/28/2024 | IRD | CS | Vanilla CS Swap | | | M0099544841 | MUMBAI | 400021949 | CCIL/MMB | CASH | Pending Exception | WAITING | INO | 100.00 | Pay | 4/28/2024 | IRD | Bond | Vanilla CS Swap | | | | **CCIL Netting(Non Guaranteed)** | M0099592071 | MUMBAI | 300070884 | BOA/MMB | CCIL | Pending Netting | WAITING | INO | 100.00 | Pay | 4/26/2024 | IRD | IRS | Vanilla IR Swap | | M0099544834 | MUMBAI | 10040528 | CAI/MMB | CCIL | Pending Netting | WAITING | INO | 150.00 | Pay | 4/27/2024 | IRD | IRS | Vanilla IR Swap | | M0097489984 | MUMBAI | 155001881 | CMB/MMB | CCIL | Pending Netting | WAITING | INO | 50.00 | Receive | 4/28/2024 | IRD | IRS | Vanilla IR Swap |
4. Ops want to remove cashflow from the Non Guaranteed list and manually settle as Gross with client. **Rationale of this case: The client would be defined as Non Guaranteed client and most cashflows with this client would continue do the netting, it's just on the adhoc basics client would approach settlement team to settle specific cashflows as gross.** | **Netting Action** | **Cashflow ID** | **Booking Entity** | **Counterparty FMID** | **Counterpart** | **Settlement Method** | **Sub Status Type** | **Cashflow Status** | **Currency** | **Amount** | **Pay/Receive** | **Value** | **Family** | **Group** | **Typology** | | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | | **Bilateral Netting(Guaranteed)** | M0099544835 | MUMBAI | 400021949 | CCIL/MMB | CCIL | Pending Netting | WAITING | INO | 100.00 | Receive | 4/26/2024 | IRD | IRS | Vanilla IR Swap | | M0099544838 | MUMBAI | 400021949 | CCIL/MMB | CCIL | Pending Netting | WAITING | INO | 100.00 | Pay | 4/27/2024 | IRD | IRS | Vanilla IR Swap | | M0099544839 | MUMBAI | 400021949 | CCIL/MMB | CCIL | Pending Netting | WAITING | INO | 200.00 | Pay | 4/28/2024 | IRD | IRS | Vanilla IR Swap | | | | **CCIL Netting(Non Guaranteed)** | M0099592071 | MUMBAI | 300070884 | BOA/MMB | CCIL | Pending Netting | WAITING | INO | 100.00 | Pay | 4/26/2024 | IRD | IRS | Vanilla IR Swap | | M0099544834 | MUMBAI | 10040528 | CAI/MMB | CCIL | Pending Netting | WAITING | INO | 150.00 | Pay | 4/27/2024 | IRD | IRS | Vanilla IR Swap | | 1. **Settlement ops pick up the Non Guaranteed cashflow and manually 'Settle as Gross' ( already supported by Ratan) ** 2. **Cashflow will go to gross settlement process but additional exception would be triggered and requesting 4 eye validation on this action settlement ops pick up the cashflow and manually 'Settle as Gross'** | M0097489984 | MUMBAI | 155001881 | CMB/MMB | CCIL | Pending Netting | WAITING | INO | 50.00 | Receive | 4/28/2024 | IRD | IRS | Vanilla IR Swap |
5. Cashflows not tagged to Non Guaranteed but ops want to include these as part of Non Guaranteed netting. Reason for this: There's client newly onboarding to CCIL system but this client FMID is not updated to the Non Guaranteed cashflow list yet. **The agreed Ratan static data & business rule model & leading time is as below.** a) Adding the client FMID to the Non Guaranteed cashflow list: This would go with CR and normally will take weeks for the change/UAT/release process. b) Adding new NSTP rule to hold these to be onboarded Non Guaranteed client cashflows, agreed with Dinesh we can test this rule setup in UAT and no need to perform UAT if there's additional FMID adding to this rule in the BAU. The leading time for static data team adding the new NSTP rule would be within one business day. | **Netting Action** | **Cashflow ID** | **Booking Entity** | **Counterparty FMID** | **Counterpart** | **Settlement Method** | **Sub Status Type** | **Cashflow Status** | **Currency** | **Amount** | **Pay/Receive** | **Value** | **Family** | **Group** | **Typology** | | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | | **Bilateral Netting(Guaranteed)** | M0099544835 | MUMBAI | 400021949 | CCIL/MMB | CCIL | Pending Netting | WAITING | INO | 100.00 | Receive | 4/26/2024 | IRD | IRS | Vanilla IR Swap | | M0099544838 | MUMBAI | 400021949 | CCIL/MMB | CCIL | Pending Netting | WAITING | INO | 100.00 | Pay | 4/27/2024 | IRD | IRS | Vanilla IR Swap | | M0099544839 | MUMBAI | 400021949 | CCIL/MMB | CCIL | Pending Netting | WAITING | INO | 200.00 | Pay | 4/28/2024 | IRD | IRS | Vanilla IR Swap | | | | **CCIL Netting(Non Guaranteed)** | M0099592071 | MUMBAI | 300070884 | BOA/MMB | CCIL | Pending Netting | WAITING | INO | 100.00 | Pay | 4/26/2024 | IRD | IRS | Vanilla IR Swap | | M0099544834 | MUMBAI | 10040528 | CAI/MMB | CCIL | Pending Netting | WAITING | INO | 150.00 | Pay | 4/27/2024 | IRD | IRS | Vanilla IR Swap | | M0097489984 | MUMBAI | 155001881 | CMB/MMB | CCIL | Pending Netting | WAITING | INO | 50.00 | Receive | 4/28/2024 | IRD | IRS | Vanilla IR Swap | | | | 1. NSTP Rule to hold the cashflows 2. Settlement ops would check the Nostro account number manually 3. Manually swift suppress the cashflows 4. Approach Ratan dev team to add the client FMID to the Non Guaranteed client list, after this the NSTP rule can be removed | M0099544844 | MUMBAI | 111111 | AAA/MMB | CASH | Pending Exception | WAITING | INO | 100.00 | Pay | 4/26/2024 | IRD | IRS | Vanilla IR Swap | | M0099544845 | MUMBAI | 222222 | BBB/MMB | CASH | Pending Exception | WAITING | INO | 150.00 | Pay | 4/27/2024 | IRD | IRS | Vanilla IR Swap | | M0099544846 | MUMBAI | 333333 | CCC/MMB | CASH | Pending Exception | WAITING | INO | 50.00 | Receive | 4/28/2024 | IRD | IRS | Vanilla IR Swap |
6. **FMRP Flow – Elena 2026-06-24 [Story 14473106 [FMRP 8.0] IN - Settlement Method update to CCIL for resultant cashflow from IRS Netting](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/14473106)**

| FMRP Flow |
| --- |
| Trade Event | Trade ID | Settlement Method | Ctpty FMCODE | Cashflow ID | Payment Type / Comment | Cashflow Event | Cf Status | Netting ID | Comment |
| New Booking | T1 | CCIL | CLEARING CORP*MMB | C1 | Coupon/Fixed | New | WAITING + Pending Another Leg | | |
| Fixing | NETTED | | |
| C2 | Coupon/Float | New | NETTED | | |
| Gross → Expectation: CCIL | N1 | Aggregated By Ratan Settlement automatically | New | WAITING + Pending Exception → Expectation: Pending Auto Netting | XXXX-XXXX-XXXX-XXXX | To Hit Auto Netting Rule: CCIL Guarantee |
| | | | | | | | | | |
| New Booking | T2 | CCIL | CLEARING CORP*MMB | C3 | Coupon/Fixed | New | WAITING + Pending Another Leg | | |
| Fixing | NETTED | | |
| C4 | Coupon/Float | New | NETTED | | |
| Gross → Expectation: CCIL | N2 | Aggregated By Ratan Settlement automatically | New | WAITING + Pending Exception → Expectation: Pending Auto Netting | XXXX-XXXX-XXXX-XXXX | To Hit Auto Netting Rule: CCIL Guarantee |
| TO follow BAU Behavior, N1 & N2 should Pending Auto Netting and do Net while timing, hence need to update Auto Netting Rule: CCIL Guarantee |
| | | CCIL | CLEARING CORP*MMB | N1 | Aggregated By Ratan Settlement automatically | New | NETTED | XXXX-XXXX-XXXX-XXXX | |
| | | CCIL | N2 | Aggregated By Ratan Settlement automatically | New | NETTED | XXXX-XXXX-XXXX-XXXX | |
| | | Gross (Keep it as it is) | N3 | Resultant cf from Bilaterial Auto Netting | New | SWIFT_SUPPRESSED by user manually | XXXX-XXXX-XXXX-XXXX | |

| **FMRP Flow – Elena 2026-08-20 [Story 15765034 [FMRP 8.0] IN Rates - enrich Settlement_Method as CCIL for FMRP flow](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/15765034)** **FMRP - Settlement Method: GROSS - non Guarantee ctpty** |
| --- |
| Trade ID | Settlement Method | Ctpty | Cashflow ID | Payment Type / Comment | Cashflow Event | Cf Status | Netting ID | Comment |
| T1 | GROSS -> CCIL by Ratan Settlement | BK OF BARO*MMB -> 300068455 | T1_C1 | Coupon/Fixed | New | WAITING + Pending Another Leg | | Settlement Method: not CCIL while booking |
| T2 | CCIL | ECL FINANCE LTD*MMB -> 400120724 | T2_C2 | Coupon/Fixed | New | WAITING + Pending Another Leg | | Settlement Method: CCIL while booking |
| Fixing |
| T1 | GROSS -> CCIL by Ratan Settlement | BK OF BARO*MMB -> 300068455 | T1_C1 | Coupon/Fixed | New | NETTED | XXXX-XXXX-XXXX-XXXX1 | |
| T1_C2 | Coupon/Float | New | NETTED | |
| CCIL | N1 | IRS Netting | New | WAITING + Pending Auto Netting | Hit Auto Netting Rule: CCIL Netting |
| T2 | CCIL | ECL FINANCE LTD*MMB -> 400120724 | T2_C1 | Coupon/Fixed | New | NETTED | XXXX-XXXX-XXXX-XXXX2 | |
| T2_C2 | Coupon/Float | New | NETTED | |
| N2 | IRS Netting | New | WAITING + Pending Auto Netting | Hit Auto Netting Rule: CCIL Netting |
| Auto Netting Job ran |
| T1 | CCIL | BK OF BARO*MMB -> 300068455 | T1_C1 | Coupon/Fixed | New | NETTED | XXXX-XXXX-XXXX-XXXX3 | |
| T1_C2 | Coupon/Float | New | NETTED | |
| N1 | IRS Netting | New | DEAD | | |
| T2 | CCIL | ECL FINANCE LTD*MMB -> 400120724 | T2_C1 | Coupon/Fixed | New | NETTED | XXXX-XXXX-XXXX-XXXX3 | |
| T2_C2 | Coupon/Float | New | NETTED | |
| N2 | IRS Netting | New | DEAD | | |
| | Gross | CLEARING CORP*MMB -> 400021949 | N3 | CCIL Netting | New | WAITING + Pending Exception | | Exception Code: - Auto Netting - INO IRS |

| FMRP - Settlement Method: GROSS - Guarantee ctpty |
| --- |
| Trade ID | Settlement Method | Ctpty | Cashflow ID | Payment Type / Comment | Cashflow Event | Cf Status | Netting ID | Comment |
| T1 | GROSS -> CCIL by Ratan Settlement | CLEARING CORP*MMB -> 400021949 | T1_C1 | Coupon/Fixed | New | WAITING + Pending Another Leg | | Settlement Method: not CCIL while booking |
| T2 | CCIL | CLEARING CORP*MMB -> 400021949 | T2_C2 | Coupon/Fixed | New | WAITING + Pending Another Leg | | Settlement Method: CCIL while booking |
| Fixing |
| T1 | GROSS -> CCIL by Ratan Settlement | CLEARING CORP*MMB -> 400021949 | T1_C1 | Coupon/Fixed | New | NETTED | XXXX-XXXX-XXXX-XXXX1 | |
| T1_C2 | Coupon/Float | New | NETTED | |
| CCIL | N1 | IRS Netting | New | WAITING + Pending Auto Netting | Hit Auto Netting Rule: CCIL Guarantee |
| T2 | CCIL | CLEARING CORP*MMB -> 400021949 | T2_C1 | Coupon/Fixed | New | NETTED | XXXX-XXXX-XXXX-XXXX2 | |
| T2_C2 | Coupon/Float | New | NETTED | |
| N2 | IRS Netting | New | WAITING + Pending Auto Netting | Hit Auto Netting Rule: CCIL Guarantee |
| Auto Netting Job ran |
| T1 | CCIL | CLEARING CORP*MMB -> 400021949 | T1_C1 | Coupon/Fixed | New | NETTED | XXXX-XXXX-XXXX-XXXX3 | |
| T1_C2 | Coupon/Float | New | NETTED | |
| N1 | IRS Netting | New | DEAD | | |
| T2 | CCIL | CLEARING CORP*MMB -> 400021949 | T2_C1 | Coupon/Fixed | New | NETTED | XXXX-XXXX-XXXX-XXXX3 | |
| T2_C2 | Coupon/Float | New | NETTED | |
| N2 | IRS Netting | New | DEAD | | |
| | Gross | CLEARING CORP*MMB -> 400021949 | N3 | Bilateral Netting | New | WAITING + Pending Exception | | Exception Code: - Auto Netting - INO IRS |

# Additional Ratan local static data(Tactical) - Non Guaranteed CCIL client list

sample format as below

| No | CCIL Member Id | Member Name | FMID | Shortname |
| --- | --- | --- | --- | --- |
| 1 | CCBNCNRB0011 | CANARA BANK | 155001698 | CANARA/MMB |
| 2 | CCBPHDFC0005 | HDFC BANK LIMITED | 130000556 | HDFC/MMB |
| 3 | CCBPICIC0049 | ICICI BANK LIMITED | 400006168 | ICICIBK/MMB |
| 4 | CCPDISEC0033 | ICICI SECURITIES PRIMARY DEALERSHIP LIMITED | 300036942 | ZICICI/MMB |
| 5 | CCBPIDBL0218 | IDBI BANK LTD | 400002527 | IDBIBK/MMB |
| 6 | CCBNSBIN0031 | STATE BANK OF INDIA | 400007691 | SBI/MMB |
| 7 | CCBPFDRL0020 | THE FEDERAL BANK LIMITED | 155001365 | FEDBK/CCN |
| 8 | CCBPRABL0129 | THE RATNAKAR BANK LTD. | 400199971 | RATBANK/KOH |
| 9 | CCBNUBIN0007 | UNION BANK OF INDIA | 155001352 | UBIN/MMB |
| 10 | CCBPUTIB0028 | AXIS BANK LTD | 155001402 | UTIB/MMB |

# Settlement Method Stamping - Murex 2.11 cashflows ( Tactical)

Additional enhancement to the Murex 2.11 to Ratan interface to stamp the settlement method as below, implementation would be covered in the MxML adaptor service (**Rule 4.1: Settlement Method Stamping**)  [Ratan MxML->SCBML Adaptor - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/Ratan+MxML-%3ESCBML+Adaptor).

- Entity.Booking_Entity_SCI_FMID == '**4**'
- Instrument_Common.Murex_Product_Family=='**IRD**' and Instrument_Common.Murex_Product_Group=='**IRS**'
- Entity.Counterparty_SCI_FMID is **400021949 **or the FMID from the above non guaranteed CCIL client static data list
- Cashflow.Payment_Currency is **INO**

# Netting Rule - Working for Tactical(Murex 2.11 booking) & Strategy( Stella booking)

![image2024-4-25_14-23-20.png](attachments/image2024-4-25_14-23-20.png)

# Netting of guaranteed cashflows - Existing Bilateral Netting Action

The netting on guaranteed cashflow would be bilateral netting which already supported in the Ratan exiting function, only additional config required and no function change requirement.

- **Guaranteed cashflows filter**: Cashflow sub State Type == '**Pending Netting**' and Settlement Method == '**CCIL**' and counterparty FMID =='**400021949**'
- **Bilateral Netting Action**: Settlement ops perform the typical bilateral netting action

# Netting of non guaranteed cashflows - To Be Built

- **Non Guaranteed cashflows filter**: Sub Status Type =='**Pending Netting**' and Settlement Method == '**CCIL**' and counterparty FMID !='**400021949**' ![image2024-4-22_18-51-9.png](attachments/image2024-4-22_18-51-9.png)
- **New netting action: CCIL Netting(Non Guaranteed):** This new netting action is only applicable for the **Non Guaranteed** cashflows, this menu won't display if any other cashflows ticked. ![image2024-4-22_19-4-13.png](attachments/image2024-4-22_19-4-13.png)
- **CCIL netting execution**: - Validate the cashflows eligibility: **Settlement_Method == 'CCIL'** and **Cashflow.Cashflow_Sub_State_Type == 'Pending Netting'**** **and** counterparty FMID !='400021949' ** - Netting Resultant cashflow generation | Logical model field | Generation Logic | Comment | | --- | --- | --- | | Data_Flow.Unique_Identifier_Message_Id | UUID | | | Execution_Date_Time | latest time stmap | | | Cashflow.Cashflow_Id | fix length 12: 'N' + 11 numeric | | | Cashflow.Cashflow_Event_Type | pre-config: New | | | Cashflow.Cashflow_State | pre-config: QUEUED | | | Cashflow.Cashflow_Affirmation_Status | pre-config: Unaffirmed | | | Cashflow.Cashflow_Sub_State | pre-config: Blank | | | Cashflow.Cashflow_Sub_State_Updater | pre-config: Blank | | | Cashflow.Cashflow_Sub_State_Type | pre-config: Blank | | | Cashflow.Payment_Type | pre-config: Blank | | | Cashflow.Netting_Id | UUID | | | Entity.Counterparty_SCI_FMID | pre-config: 400021949 | | | Entity.Counterparty_Murex_Display_Shortcode | pre-config: CCIL/MMB | | | Settlement_Method | pre-config: CASH | | | Delivery_Method | pre-config: CASH | | | Trade_Id | Pre-config: Blank | | | Pre-config: Blank | Pre-config: Blank | | | Parent_Trade_Id | NA | | | Trade_State | pre-config: TOBESENT | | | Cashflow.Cashflow_Version | Pre-Config: 0 | | | Cashflow.Cashflow_Business_Version | Pre-Config: 0 | | | Cashflow.FMO_Comment | Pre-config: Blank | | | Cashflow.FMO_Comment_Updater | Pre-config: Blank | | | Cashflow.FMO_Comment_Timestamp | Pre-config: Blank | | | | | | | | | | | Data_Flow.Data_Publication_Date_Time | Latest timestamp | | | Other Attributes | Copy from first cashflow | |