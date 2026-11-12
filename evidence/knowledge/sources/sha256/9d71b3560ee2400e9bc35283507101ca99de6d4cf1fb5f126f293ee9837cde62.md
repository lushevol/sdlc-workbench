## Requirement

1. Ratan will build similar filter logic for Beneficiary BIC netting as Murex, including entity, value date, counterparty etc as PAYSTP_NET table.
2. Ratan will build control before performing BIC netting, including same BIC label, same value date, same currency, same entity.
3. Proposed netting process as:
4. Per discussed, ops user will take decision, full control and risk for which cashflow should be netted together as manual process.
5. Segregation among manual netting is required, and **BIC netting should have higher priority than Bilateral manual netting**.
6. PAYSTP_NET table should be **configurable** by user.

## Beneficiary BIC Netting Eligible Flag – BIC_Net

When Cashflow Satisfies, update to **Pending Netting**

Entity = LONDON

~~Payment Date >= Today~~

Below table:

**EXPAND: PAYSTP_NET**

**EXPAND_END**

Beneficiary BIC is the BIC code from SCI where mediumUsage='MXR'

BIC_NET flag Logical Model: Entity.Counterparty_SCI_BIC_Net_Flag
BIC_NET flag Physical Model: /scb:SCBML/scb:payload/scb:cashflowPayload/scb:party[@id='party2']/conf:bicNetFlag

## Prototype

Customized Filter – Step 1

![image2024-7-22_14-18-31.png](attachments/image2024-7-22_14-18-31.png)

Customized Filter – Step 2

BIC Netting Button will only be shown when selected cashflow satisfies:

- **Same BIC_Net Flag**
- **Same Beneficiary BIC**
- **Same Value Date**
- **Same Currency**
- **Same Entity**

![image2024-7-22_14-19-6.png](attachments/image2024-7-22_14-19-6.png)

BIC Netting Preview

![image2024-7-22_14-19-56.png](attachments/image2024-7-22_14-19-56.png)![image2024-7-22_14-20-15.png](attachments/image2024-7-22_14-20-15.png)

BIC Netting Result

![image2024-7-22_14-20-43.png](attachments/image2024-7-22_14-20-43.png)

## **Netting Execution:**

- Validate the cashflows eligibility: BIC_Net** == 'Y'** and **Cashflow.Cashflow_Sub_State_Type == 'Pending Netting'**** **
- Netting Resultant cashflow generation | Logical model field | Generation Logic | Comment | | --- | --- | --- | | Data_Flow.Unique_Identifier_Message_Id | UUID | | | Execution_Date_Time | latest time stmap | | | Cashflow.Cashflow_Id | fix length 12: 'N' + 11 numeric | | | Cashflow.Cashflow_Event_Type | pre-config: New | | | Cashflow.Cashflow_State | pre-config: QUEUED | | | Cashflow.Cashflow_Affirmation_Status | pre-config: Unaffirmed | | | Cashflow.Cashflow_Sub_State | pre-config: Blank | | | Cashflow.Cashflow_Sub_State_Updater | pre-config: Blank | | | Cashflow.Cashflow_Sub_State_Type | pre-config: Blank | | | Cashflow.Payment_Type | pre-config: Blank | | | Cashflow.Netting_Id | UUID | | | **Counterparty FMID** | Randomly pick up | | | **Counterparty Murex shortcode** | Consistent with cpty FMID | | | **Family** | Inherit from component cashflow if the values are same, empty if value are different | | | **Group** | Inherit from component cashflow if the values are same, empty if value are different | | | **Type** | Inherit from component cashflow if the values are same, empty if value are different | | | **Typology** | Inherit from component cashflow if the values are same, empty if value are different | | | **Strategy** | Inherit from component cashflow if the values are same, empty if value are different | | | **Trade_Id** | Inherit from component cashflow if the values are same, empty if value are different | | | **Taxonomy** | Restamp according to current family/group/type/typology/strategy | | | **CFI Code** | Restamp according to current family/group/type/typology/strategy | | | **Settlement Method** | Pre-config: GROSS | | | **Delivery Method** | Pre-config: CASH | | | Pre-config: Blank | Pre-config: Blank | | | Parent_Trade_Id | NA | | | Trade_State | pre-config: TOBESENT | | | Cashflow.Cashflow_Version | Pre-Config: 0 | | | Cashflow.Cashflow_Business_Version | Pre-Config: 0 | | | Cashflow.FMO_Comment | Pre-config: Blank | | | Cashflow.FMO_Comment_Updater | Pre-config: Blank | | | Cashflow.FMO_Comment_Timestamp | Pre-config: Blank | | | Data_Flow.Data_Publication_Date_Time | Latest timestamp | | | Other Attributes | Copy from first cashflow | |

## **Current BAU Process**

1. On VD-1 Ops user will go into payment queue LDN: CR CPTY NET, system would load all the Ben BIC Netting eligible payments into this queue.
2. Ops tick all the BIC(VD tmr) & save, system would run the netting with key Entity/Currency/Value Date/Ben BIC.
3. Ops take the Ben BIC netting resultant payments and do the affirmation with client, with the client affirmation on the netting resultant payment ops will move the payment status from the typical maker(INIT to CHCK)/checker(CHCK to SNET) queue.
4. In case client raise dispute on the netting resultant payment affirmation, settlement ops will manually un-net the netting resultant payment(from maker or checker queue) and go the BIC netting queue ‘LDN: CR CPTY NET’ again to perform the netting if required by client.
5. Post settled trade amendment: There’s probability MO perform trade amendment after ops settle the BIC netting resultant payment. There’re different cases in the Murex BAU.

## **Problem Statement as BAU**

From Babu:

In our current BAU, we have multiple challenges with BIC based netting and I have listed them down for your reference.

- - We will have lot of Give up counterparties onboarded to murex on daily basis and we will not have visibility of those counterparties. Settlements team will come to know only once the trades are booked and we will have mismatch on settlement amount where newly created counterparty not part of PAYSTP_NET Table. - This allow user to manually net cash flows between multiple queues (Bilateral netting and BIC Based Netting) and we need to suppress all cash flows and arrange for manual payment via OSCAR. - We have also noticed Swift BIC not getting captured in Murex system which is causing manual actions for team where we need to net cash flows in different queue and payment done out side murex. - We also have significant risk where UDF tables not getting updated on time leading to Gross Net Issues.

## **Meeting Minutes 20240715- Requirement For Cashflow Migration**

1. Ratan should have the ability to filter out the Ben BIC netting eligible cashflows from cashflow blotter, new netting action ‘Ben BIC Netting to be created for these cashflows.
2. Affirmation information is not required in the netting pre-review page.
3. Ben BIC Netting key: Entity/Currency/Value Date/Ben BIC/Family/Group/Type/Typology/Strategy
4. After netting performed, netting resultant cashflow ID should be displayed.
5. Netting resultant cashflow would be NSTP/Pending Affirmation.
6. Ratan should have the ability to auto unnet the resultant cashflow if withdrawal/amendment happens and resultant cashflow is not released.
7. Affirmation info is required to be filled in after netting resultant cashflow generated.
8. Maker-Checker Process is required for netting resultant cashflow verification.
9. SWIFT 192/292 message is required in strategic solution.
10. Non-function requirement (including response time) will be discussed separately.