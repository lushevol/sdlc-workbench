# Background

This requirement comes from a production accident.

UK settlement team released & settled two Swap Agent+Coupon cashflows in Ratan  which should be handled by clearing ops team and swift suppressed in Ratan.

To avoid this accident happened again ,business user would like to add a hard blocker to block the SWAP_AGENT Coupon and SWAP_AGENT Interim MTM released from Ratan.

# ADO

[Story 9832947 [Swap Agent Day2] hard blocker requirement finalization](https://dev.azure.com/sc-ado/FMQPR/_workitems/edit/9832947)

# Clarification History

| # | Date | Item | Attached |
| --- | --- | --- | --- |
| 1 | 2025-08-11 2025-09-15 | Scope confirmation email from users | |
| 2 | 2025-08-12 | Hard Blocker confirmation screenshot from users | |
| 3 | 2025-10-14 | Manual Netting side block scope | Offline chat with Vanessa & Dinesh ,Swap Agent+Coupon (Interim MTM ) can't net with the other payment type cashflow,Coupon will net only with Coupon ,and Interim MTM will net with Interim MTM |

# Requirement Details

As offline confirmed with user, SWAP AGENT Coupon cashflow will not net with the other payment type cashflow except SWAP AGENT Coupon ,SWAP AGENT +Interim MTM will not net with the other payment type cashflow except SWAP AGENT Interim MTM.

### Manual Netting Block Scope(If cashflow with same booking entity ,counterparty,ccy,payment date)

| **Scenario** ** ** | **Cashflow1** | **Cashflow2** | **Manual Netting** | **Manual Netting Block or not** | **NSTP Block or not** |
| --- | --- | --- | --- | --- | --- |
| **Murex Product Strategy** | **Payment Type** | **Murex Product Strategy** | **Payment Type** |
| 1 | SWAP_AGENT | Coupon | SWAP_AGENT | Coupon | Bilateral Netting | Manual Netting not block | Resultant cashflow blocked by NSTP hard block rule |
| 2 | SWAP_AGENT | Interim MTM | SWAP_AGENT | Interim MTM | Bilateral Netting | Manual Netting not block | Resultant cashflow blocked by NSTP hard block rule |
| 3 | SWAP_AGENT | Coupon | SWAP_AGENT | Interim MTM | Bilateral Netting | Manual Netting block Popup error message "SWAP AGENT Coupon or Interim MTM can't net with the other payment type cashflow to avoid clearing eligible cashflows settling Bilaterally" | Not Block |
| 4 | SWAP_AGENT | Coupon | SWAP_AGENT | Initial Notional | Bilateral Netting | Same with above | Not Block |
| 5 | SWAP_AGENT | Coupon | SWAP_AGENT | Final Notional | Bilateral Netting | Same with above | Not Block |
| 6 | SWAP_AGENT | Interim MTM | SWAP_AGENT | Initial Notional | Bilateral Netting | Same with above | Not Block |
| 7 | SWAP_AGENT | Interim MTM | SWAP_AGENT | Final Notional | Bilateral Netting | Same with above | Not Block |
| 8 | SWAP_AGENT | Coupon/Interim MTM | Other | Other | Bilateral Netting | Same with above | Not Block |

NSTP Hard Blocker

User need a hard blocker in Ratan to complete block Swap Agent Interim MTM & Coupon cashflow released from Ratan.

![image-2025-10-9_16-20-40.png](attachments/image-2025-10-9_16-20-40.png)

# Proposed solution

We would like to add block from both Manual Netting side  and NSTP side.

### Manual Netting Block: Block netting of SWAP AGENT+ Coupon with other payment types, and block netting of SWAP AGENT+ Interim MTM with other cashflow types

When SWAP AGENT +Coupon manual net with the other payment type cashflow or SWAP AGENT +Interim MTM manual net with the other payment type cashflow,will popup up error message  "SWAP AGENT Coupon or Interim MTM can't net with the other payment type cashflow to avoid clearing eligible cashflows settling Bilaterally" on GUI.

![image-2025-10-20_19-51-53.png](attachments/image-2025-10-20_19-51-53.png)

### NSTP: Block single cashflow after ‘Settle as Gross' and resultant cashflow which  one of the component cashflow is SWAP AGENT+Coupon or SWAP AGENT+Interim MTM

| Scenario | Single Cashflow | Resultant Cashflow |
| --- | --- | --- |
| SWAP AGENT | if the single cashflow meet the below condition Instrument_Common__Murex_Product_Strategy == "SWAP_AGENT"&& Cashflow__Payment_Type == "Coupon" or Instrument_Common__Murex_Product_Strategy == "SWAP_AGENT" && Cashflow__Payment_Type == "Interim MTM" it should hit the new NSTP rule | If it is a resultant cashflow, need to check component cashflow if one of the component cashflows meet the below condition , Instrument_Common__Murex_Product_Strategy == "SWAP_AGENT"&&Cashflow__Payment_Type == "Coupon" or Instrument_Common__Murex_Product_Strategy == "SWAP_AGENT"&&Cashflow__Payment_Type == "Interim MTM" it should hit the new NSTP rule |

1.To add new NSTP Hard Block Swap Agent rule.

![image-2025-8-28_9-31-30.png](attachments/image-2025-8-28_9-31-30.png)

Exception Category:HARD_BLOCKER

Exception Code:Hard Block Swap Agent

Operational Level: MAKER_CHECKER

| No | NSTP Rule Condition | Exception Code | Operation Level | Exception Category | Bulk Eligible | Requestor/Eops reference |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | ((Instrument_Common__Murex_Product_Strategy == "SWAP_AGENT" && Cashflow__Payment_Type in ("Coupon", "Interim MTM")) || Cashflow__Is_Hard_Blocker == true) | Hard Block Swap Agent | MAKER_CHECKER | HARD_BLOCKER | Not ticked | Hard Block Swap Agent |
| ~~1~~ | ~~(Cashflow__Netting_Id == null || Cashflow__Netting_Id == "") && Instrument_Common__Murex_Product_Strategy == "SWAP_AGENT" && (Cashflow__Payment_Type == "Coupon" || Cashflow__Payment_Type == "Interim MTM")~~ | ~~Hard Block Swap Agent~~ | ~~MAKER_CHECKER~~ | ~~HARD_BLOCKER~~ | ~~Not ticked~~ | ~~Hard Block Swap Agent-Single cashflow~~ |
| ~~2~~ | ~~(Cashflow__Netting_Id != null && Cashflow__Netting_Id != "") && (Cashflow__Component_Strategy_Payment_Hard_Blocker matches "(?i)^.*(^|,)SWAP_AGENT#Coupon(,|$).*$" || Cashflow__Component_Strategy_Payment_Hard_Blocker matches "(?i)^.*(^|,)SWAP_AGENT#Interim MTM(,|$).*$")~~ | ~~Hard Block Swap Agent~~ | ~~MAKER_CHECKER~~ | ~~HARD_BLOCKER~~ | ~~Not ticked~~ | ~~Hard Block Swap Agent-Resultant cashflow~~ |

2.When the single cashflow or resultant cashflow hit the NSTP rule, Hard Block Swap Agent exception code will display on the GUI in red color.

![image-2025-10-16_15-50-58.png](attachments/image-2025-10-16_15-50-58.png)

3.When user do the maker submit or checker approve ,will popup an error message "This is a Swap Agent Coupon or Interim MTM cashflow ,can't be release from Ratan" and can't submit or approve ,so that means can't fix the hard blocker NSTP exception.

![image-2025-10-16_15-51-43.png](attachments/image-2025-10-16_15-51-43.png)

# UAT Testing

[Hard Block UAT testing - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Hard+Block+UAT+testing)

# Business User Case

| AC-No | Function | Scenario | Expected Result |
| --- | --- | --- | --- |
| AC-Settlement-SAL Hard Blocker-001 | Different payment type netting | 1. Book 2 cashflow C1,C2 which is same booking entity ,same counterparty, same ccy ,same payment date and cover the below 5 scenarios | Scenario | Cashflow | Murex_Product_strategy | Payment Type | Cashflow | Murex_Product_strategy | Payment Type | | --- | --- | --- | --- | --- | --- | --- | | 1 | C1 | SWAP_AGENT | Coupon | C2 | SWAP_AGENT | Interim MTM | | 2 | C1 | SWAP_AGENT | Coupon | C2 | SWAP_AGENT | Initial Notional | | 3 | C1 | SWAP_AGENT | Coupon | C2 | SWAP_AGENT | Final Notional | | 4 | C1 | SWAP_AGENT | Interim MTM | C2 | SWAP_AGENT | Initial Notional | | 5 | C1 | SWAP_AGENT | Interim MTM | C2 | SWAP_AGENT | Final Notional | | 6 | C1 | SWAP_AGENT | Coupon | C2 | RECALC | Coupon | 2.Select C1,C2,right click 'Net Selected Cashflow', click net all cashflows and update affirmation | 2. Can't net C1&C2.Popup error message "SWAP AGENT Coupon or Interim MTM can't net with the other payment type cashflow to avoid clearing eligible cashflows settling Bilaterally" |
| Scenario | Cashflow | Murex_Product_strategy | Payment Type | Cashflow | Murex_Product_strategy | Payment Type |
| 1 | C1 | SWAP_AGENT | Coupon | C2 | SWAP_AGENT | Interim MTM |
| 2 | C1 | SWAP_AGENT | Coupon | C2 | SWAP_AGENT | Initial Notional |
| 3 | C1 | SWAP_AGENT | Coupon | C2 | SWAP_AGENT | Final Notional |
| 4 | C1 | SWAP_AGENT | Interim MTM | C2 | SWAP_AGENT | Initial Notional |
| 5 | C1 | SWAP_AGENT | Interim MTM | C2 | SWAP_AGENT | Final Notional |
| 6 | C1 | SWAP_AGENT | Coupon | C2 | RECALC | Coupon |
| AC-Settlement-SAL Hard Blocker-002 | Same payment type netting | 1. Create a Hard Blocker NSTP rule with Maker Checker (Maker Only/Checker Only) 2. Book 2 cashflow C1,C2 which is Murex_Product_strategy=SWAP_AGENT ,same booking entity ,same counterparty,same ccy ,same payment date and cover the below 2 scenarios | Scenario | Cashflow | Payment Type | Cashflow | Payment Type | | --- | --- | --- | --- | --- | | 1 | C1 | Coupon | C2 | Coupon | | 2 | C1 | Interim MTM | C2 | Interim MTM | 3. Select C1,C2,right click 'Net Selected Cashflow',click net all cashflows and update affirmation 4. Maker submit 5. Click right button and select 'Swift Suppressed' | 1.Hard Blocker NSTP rule is live in Settlement NSTP Rules Blotter 3.N1 generated,N1 hit Hard Blocker NSTP rule, 'Hard block Swap Agent' Exception Code displayed on GUI in red color 4.Popup error message "This is a Swap Agent Coupon or Interim MTM cashflow ,can't be released from Ratan", maker can't submit 5.C1 in 'Swift Suppressed' status |
| Scenario | Cashflow | Payment Type | Cashflow | Payment Type |
| 1 | C1 | Coupon | C2 | Coupon |
| 2 | C1 | Interim MTM | C2 | Interim MTM |
| AC-Settlement-SAL Hard Blocker-003 | Single cashflow-Pending Auto Netting-Coupon&Interim MTM-Swift Suppressed | 1. Create a Hard Blocker NSTP rule with Maker Checker (Maker Only/Checker Only) 2. Book 1 cashflow C1 which is Murex_Product_strategy=SWAP_AGENT, Payment Type ='Interim MTM' or 'Coupon' and in 'Pending Auto Netting' Status 3. Click right button and select 'Settle as Gross' 4. Maker submit 5. Click right button and select 'Swift Suppressed' | 1.Hard Blocker NSTP rule is live in Settlement NSTP Rules Blotter 3.C1 hit Hard Blocker NSTP rule, 'Hard block Swap Agent' Exception Code displayed on GUI in red color 4.Popup error message "This is a Swap Agent Coupon or Interim MTM cashflow ,can't be released from Ratan", maker can't submit 5.C1 in 'Swift Suppressed' status |
| AC-Settlement-SAL Hard Blocker-004 | Single cashflow-Pending Auto Netting-Coupon&Interim MTM-Manual Action | 1. Create a Hard Blocker NSTP rule with Checker Only (Maker Only/Maker Checker) 2. Book 1 cashflow C1 which is Murex_Product_strategy=SWAP_AGENT, Payment Type ='Interim MTM' or 'Coupon' and in 'Pending Auto Netting' Status 3. Click right button and select 'Settle as Gross' 4. Checker approve 5. Click right button and select Manual Failed/Hold&Unhold/Suppress Cashflow action | 1.Hard Blocker NSTP rule is live in Settlement NSTP Rules Blotter 3.C1 hit Hard Blocker NSTP rule, 'Hard block Swap Agent' Exception Code displayed on GUI in red color 4.Popup error message "This is a Swap Agent Coupon or Interim MTM cashflow ,can't be released from Ratan", checker can't approve 5.C1 in Failed/Pending Exception/Hold/Cashflow Suppressed status |
| AC-Settlement-SAL Hard Blocker-005 | Bulk Exception-Bulk Eligible not ticked | 1. Create a Hard Blocker NSTP rule with Maker Checker(Checker Only/Maker Only),Bulk Eligible not ticked 2. Book 2 cashflow C1,C2( or N1) meet below conditions 1-1.C1 hit multiple exceptions, and one of the exception is NSTP Hard Blocker 1-2.C2 or N1 hit multiple exceptions ,but not hit NSTP Hard Blocker 3.Select C1 and C2(N1)Right Click Button, Bulk Submit | 3.C1 is not eligible to submit |
| AC-Settlement-SAL Hard Blocker-006 | Bulk Exception-Bulk Eligible ticked | 1. Create a Hard Blocker NSTP rule with Maker Checker(Checker Only/Maker Only),Bulk Eligible ticked 2. Book 2 cashflow C1,C2( or N1) meet below conditions 1-1.C1 hit multiple exceptions, and one of the exception is NSTP Hard Blocker 1-2.C2 or N1 hit multiple exceptions ,but not hit NSTP Hard Blocker 3.Select C1 and C2(N1)Right Click Button, Bulk Submit | 3.C1 is not eligible to submit |
| AC-Settlement-SAL Hard Blocker-007 | Disable auto swift suppressed rule | 1. Create a Hard Blocker NSTP rule with Maker Checker (Maker Only/Checker Only),Disable auto swift suppressed rule 2. Book 2 cashflow C1,C2 which is Murex_Product_strategy=SWAP_AGENT ,same booking entity ,same counterparty,same ccy ,same payment date | Scenario | Cashflow | Payment Type | Cashflow | Payment Type | | --- | --- | --- | --- | --- | | 1 | C1 | Interim MTM | C2 | Interim MTM | | 2 | C1 | Coupon | C2 | Coupon | 3. Auto netting job trigger | 3.N1 generated and hit Hard Blocker NSTP rule |
| Scenario | Cashflow | Payment Type | Cashflow | Payment Type |
| 1 | C1 | Interim MTM | C2 | Interim MTM |
| 2 | C1 | Coupon | C2 | Coupon |
| AC-Settlement-SAL Hard Blocker-008 | Single cashflow-Pending Exception-Initial Notional&Final Notional | 1. Create a Hard Blocker NSTP rule with Maker Only(Maker Checker/Checker Only) 2. Book 1 cashflow C1 which Murex_Product_strategy=SWAP_AGENT, Payment Type ='Initial Notional' or 'Final Notional' and in 'Pending Exception' Status 3. Ops release the cashflow | 1.Hard Blocker NSTP rule is live in Settlement NSTP Rules Blotter 2.C1 will not hit Hard Blocker NSTP rule 3.C1 released from Ratan |
| AC-Settlement-SAL Hard Blocker-009 | Single cashflow-Coupon&Interim MTM-Multiple Exception | 1. Create a Hard Blocker NSTP rule with Maker Checker (Maker Only/Checker Only) 2. Book 1 cashflow C1 which is Murex_Product_strategy=SWAP_AGENT, Payment Type ='Interim MTM' or 'Coupon' ,hit Hard Blocker NSTP and Missing Vostro(Missing nostro/Pending Affirmation, etc) 3. Maker submit 4. Click right button and select 'Swift Suppressed' | 1.Hard Blocker NSTP rule is live in Settlement NSTP Rules Blotter 2.C1 hit Hard Blocker NSTP rule, 'Hard block Swap Agent' Exception Code displayed on GUI in red color 3.Popup error message "This is a Swap Agent Coupon or Interim MTM cashflow ,can't be released from Ratan", maker can't submit 4.C1 in 'Swift Suppressed' status |
| AC-Settlement-SAL Hard Blocker-010 | Resultant cashflow -Coupon&Interim MTM-Mutiple Exception | 1. Create a Hard Blocker NSTP rule with Maker Checker(Checker Only/Maker Only) 2. Book 2 cashflow C1,C2 meet below conditions 2-1.C1 Murex_Product_strategy=SWAP_AGENT, Payment Type ='Interim MTM' or 'Coupon' and in 'Pending Auto Netting' Status 2-2.C2 Murex_Product_strategy=SWAP_AGENT, Payment Type ='Interim MTM' or 'Coupon' and in 'Pending Auto Netting' Status 2-3.C1,C2 have the same booking entity ,same counterparty, same value date ,same ccy 2-4.Resultant Cashflow will hit multiple exception (Missing Vostro/Pending Affirmation,etc) 3.Select C1,C2,right click and select "Net Selected Cashflow". 4.Maker submit 5.Select N1 and click right Unnet/Swift Suppressed/Manual Failed/Reinstate/Hold&Unhold/Cashflow Suppressed action | 1.Hard Blocker NSTP rule is live in Settlement NSTP Rules Blotter 3.C1, C2 cashflow state ='NETTED', N1 generated,N1 hit Hard Blocker NSTP rule and other exception(hit mutiple exception), 'Hard block Swap Agent' Exception Code displayed on GUI in red color ,other exception display on GUI as existing 4.Popup error message "This is a Swap Agent Coupon or Interim MTM cashflow ,can't be released from Ratan", maker can't submit 5.N1 can unnet or in Swift Suppressed/Failed/Pending Exception/Hold/Cashflow Suppressed status |
| AC-Settlement-SAL Hard Blocker-011 | SWAP AGENT with Interim MTM or Coupon | 1. Create auto netting rule and Auto swift suppressed rule 2. Book 2 cashflow C1,C2 which is SAL with Interim MTM or Coupon 3. Trigger auto netting job | 2.C1,C2 cashflow state ='WAITING', cashflow sub state type ='Pending Auto Netting' 3.C1,C2 cashflow state ='Netted', Netting resultant N1 created (Cashflow State = 'SWIFT_SUPPRESSED', payment type ='SAL MTM Netting') |
| AC-Settlement-SAL Hard Blocker-012 | Create NSTP rule | 1. Create a **non** Hard Blocker NSTP rule with Maker Checker(Checker Only/Maker Only) | 1.Can create success |
| AC-Settlement-SAL Hard Blocker-013 | Manual Netting | Regression BIC Netting,CCIL Netting ,Bilateral Netting | Function works well |
| AC-Settlement-SAL Hard Blocker-014 | Bulk Submit | Regression Bulk submit and bulk approve | Function works well |
| ~~AC-Settlement-SAL Hard Blocker-003~~ | ~~Single cashflow -Pending Netting-Coupon&Interim MTM~~ | 1. ~~Create a Hard Blocker NSTP rule with Maker Only(Maker Checker/Checker Only)~~ 2. ~~Book cashflow C1 which Murex_Product_strategy=SWAP_AGENT, Payment Type ='Interim MTM' or 'Coupon' and in 'Pending Netting' Status~~ 3. ~~Click right button and select 'Settle as Gross'~~ 4. ~~Maker submit~~ 5. ~~Click right button and select 'Swift Suppressed'~~ | ~~1.Hard Blocker NSTP rule is live in Settlement NSTP Rules Blotter~~ ~~3.C1 hit Hard Blocker NSTP rule, 'Hard block Swap Agent' Exception Code displayed on GUI in red color~~ ~~4.Popup error message "This is a Swap Agent Coupon or Interim MTM cashflow ,can't be released from Ratan", maker can't submit ~~ ~~5.C1 in 'Swift Suppressed' status~~ |
| ~~AC-Settlement-SAL Hard Blocker-005~~ | ~~Resultant cashflow-Un-Net~~ | 1. ~~Create a Hard Blocker NSTP rule with Checker Only(Maker Checker/Maker Only)~~ 2. ~~Book 2 cashflow C1,C2 meet below conditions~~ ~~ 2-1. C1 Murex_Product_strategy=SWAP_AGENT, Payment Type ='Interim MTM' or 'Coupon' and in 'Pending Auto Netting' Status~~ ~~ 2-2.C2 Murex_Product_strategy=SWAP_AGENT, Payment Type ='Initial Notional' or 'Final Notional' and in 'Pending Exception' Status~~ ~~ 2-3.C1,C2 have the same booking entity ,same counterparty, same value date ,same ccy ~~ ~~ 3.Select C1,C2,right click 'Net Selected Cashflow'~~ ~~ 4.Checker approve~~ ~~ 5.Select N1 ,right click 'Un-Net Cashflow'~~ ~~ 6.Select C1,right click and 'Settle as Gross',C2 to fix the exception~~ | ~~1.Hard Blocker NSTP rule is live in Settlement NSTP Rules Blotter~~ ~~3.C1, C2 cashflow state ='NETTED', N1 generated,N1 hit Hard Blocker NSTP rule, 'Hard block Swap Agent' Exception Code displayed on GUI in red color~~ ~~4.Popup error message "This is a Swap Agent Coupon or Interim MTM cashflow ,can't be released from Ratan", checker can't approve~~ ~~5.N1 cashflow state='DEAD',C1 cashflow in 'WAITING'+ 'Pending Auto Netting' ,C2 cashflow in 'WAITING'+ 'Pending Exception'~~ ~~6.C1 hit the hit Hard Blocker NSTP rule,C2 can release from Ratan~~ |
| ~~AC-Settlement-SAL Hard Blocker-006~~ | ~~Resultant cashflow- Manual Action~~ | 1. ~~Create a Hard Blocker NSTP rule with Maker Only(Maker Checker/Checker Only)~~ 2. ~~Book 2 cashflow C1,C2 meet below conditions~~ ~~ 2-1.C1 Murex_Product_strategy=SWAP_AGENT, Payment Type ='Interim MTM' or 'Coupon' and in 'Pending Auto Netting' Status~~ ~~ 2-2.C2 Murex_Product_strategy=SWAP_AGENT, Payment Type ='Initial Notional' or 'Final Notional' and in 'Pending Exception' Status~~ ~~ 2-3.C1,C2 have the same booking entity ,same counterparty, same value date ,same ccy ~~ ~~ 3.Select C1,C2,right click 'Net Selected Cashflow'~~ ~~ 4.Maker submit~~ ~~ 5.Select N1 ,right click button and select Manual Failed/Hold&Unhold/Suppress Cashflow action ~~ | ~~1.Hard Blocker NSTP rule is live in Settlement NSTP Rules Blotter~~ ~~3.C1, C2 cashflow state ='NETTED', N1 generated,N1 hit Hard Blocker NSTP rule, 'Hard block Swap Agent' Exception Code displayed on GUI in red color~~ ~~4.Popup error message "This is a Swap Agent Coupon or Interim MTM cashflow ,can't be released from Ratan", maker can't submit ~~ ~~5.N1 in Swift Suppressed/Failed/Pending Exception/Hold/Cashflow Suppressed status~~ |

# Open questions

| Question | Answer |
| --- | --- |
| Will SWAP AGENT+Coupon (SWAP AGENT+Interim MTM )net with the other payment type cashflow? if no we will add UI blocker to block SWAP AGENT+Coupon (SWAP AGENT+Interim MTM )net with the other payment type cashflow . | 2025-10-14 offline chat with Dinesh and Vanessa,SWAP AGENGT+Coupon will net with the other payment type cashflow,SWAP AGENGT+Interim MTM will net with the other payment type cashflow. |
| What kind of hard blocker user expected for a cashflow if misoperation? 1-1.NSTP exception can be fixed -means can release cashflow ,propose High Risk NSTP 1-2.NSTP exception can't be fixed-means complete blocker, can't release cashflow | 2025-08-27 ![image-2025-9-1_15-42-13.png](attachments/image-2025-9-1_15-42-13.png) ![image-2025-9-1_15-42-36.png](attachments/image-2025-9-1_15-42-36.png) ![image-2025-9-1_15-42-59.png](attachments/image-2025-9-1_15-42-59.png) ![image-2025-9-1_15-43-37.png](attachments/image-2025-9-1_15-43-37.png) 2025-08-20 ![image-2025-8-25_10-24-16.png](attachments/image-2025-8-25_10-24-16.png) 2025-08-12 User would like to select the NSTP hard blocker that can't release cashflow from Ratan 2025-08-11 Babu's team will check and feedback later |
| What is the scope of this blocker?SWAP Agent,UK LCH All Products,CME EUREX JSCC ICE?any others ? single/resultant cashflow? | 2025-08-11 Only Swap Agent is required |