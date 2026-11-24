******

# ***Overview***

- *Settlements team have the capability to setup Business Rules as part of BAU via front end, which removes the dependency on Change Release*
- *For the Strategic workflow, ringfenced group of users have been given access to maintain the rules for purpose of control & oversight*
- *Rules can be updated only via Maker / Checker (Checker can also perform Maker action)*
- *Rules have to be tested in UAT environment before updating in production*
- *Approval has to be obtained before setting up the rule in production*
- *Due diligence must be exercised to prevent incorrect rule setup as it could result in payment failure / reconciliation breaks / high NSTP*

## ***Approval / Governance Process***

1. Any new business rules proposed must outline the rule’s purpose, scope and impact on any entity and/or counterparties.
2. Proposed business rule complete with the required information is to be emailed to the MT for review <FMOFXDerivSetts-MT@[exchange.standardchartered.com](http://exchange.standardchartered.com)>
3. The MT will review the rule to ensure clarity and Impact of the proposed rule.
4. If the rule is approved by the MT – raise an eOPS for DataOps to raise the rule in the FMO Post Trade Portal.
5. The designated maker and checker will ensure the rule is tested in the UAT environment as required. Upon successful testing ; the rule can be released into production.
6. If amendments are required as a result of UAT testing, updates to the rule are to be sent to the MT again. Once the amended rule successfully passes the UAT testing, the rule can be released into production.
7. The new rule will be added to the DOI along with the date of approval from the MT.
8. All rules to be reviewed by the MT (or delegate) on an annual basis to ensure that it is still relevant and required for effective and efficient settlement processing as well as meeting all compliance requirements. Date of annual review and reviewer to be documented in the DOI at the completion of the review.

## ***User Access***

****

## ***FMO Post Trade Portal***

****

## ***Architecture***

******

## ***Login***

****

## ***List of Business Rule Tables***

- *Authorization Limits*
- *Settlement NSTP Rules (New)*
- *Suppression Rules [Cashflow]*
- *Suppression Rules [Swift]*
- *Auto Netting Rules*
- *Settlement NSTP Rules [FX & Equity]*
- *Suppression Rules [FX & Equity]*

# ***Authorization Limits***

- *The Limits have been setup in line with RAZOR to facilitate that the users are able to approve cashflows which are within their delegated authority.*
- *Normally these are not expected to be updated during BAU. But new profiles can be setup or existing limits amended if required*
- *Any new rules are to be tested in UAT before updating in PROD*

# ***![authlimitCapture.JPG](attachments/authlimitCapture.JPG)***

# ***Rules Engine Blotter***

In FM TPT, the need for efficient and powerful rule management systems has become paramount. The New Rule is our answer to this demand, offering a completely refactored interface with advanced rule filtering and maintenance capabilities. Ratan One has processed upgrading Rule Service engine to Drools since 2023, creation, maintenance and execution on rule are migrate to Rule Service.

The New Rule is built upon a modern design philosophy, providing users with unparalleled control over the entire lifecycle of a rule. It's not just a facelift; it's a complete overhaul designed to enhance user interaction and operational efficiency.

For more technical details in how we integrate Drools, please refer to [https://confluence.global.standardchartered.com/x/sk53qQ](https://confluence.global.standardchartered.com/x/sk53qQ)

So, all the rule blotter in RATANONE follow same style and common feature follow the rule engine like below. Also rule engine support customize feature.

| Function | Steps |
| --- | --- |
| Rule Blotter | - User login, select target rule blotter. ![image2024-8-16_15-26-8.png](attachments/image2024-8-16_15-26-8.png) |
| **Create Rule** | - For maker, user can create rule by click "Create Rule". - "Business Flow" type will be default choose depend on which blotter open. - For rule item, select required fields with values, different fields will be taken as 'AND' condition into the rule. - Support group rule to meet complex scenarios. - Reason will be displayed as mandatory when creating. Comment is optional as feel free to input as additional comment. - Newly added rule will be effective once checker approves.(except dry run rule). - When user choose "dry run" means this rule would not be execute immediately, user are able to check whether any unexpected rule configurations to rectify before live to business. - Rule maker and checker should be different person. When checker verifies the rule, he/she can approve/reject as appropriate. ![image2024-8-16_15-27-25.png](attachments/image2024-8-16_15-27-25.png) ![image2024-8-16_15-28-6.png](attachments/image2024-8-16_15-28-6.png) |
| **Disable Rule** | - For user who have the operate permission can disable an existing live rule by right click menu in UI and effect immediately. ![image2024-8-16_16-19-44.png](attachments/image2024-8-16_16-19-44.png) |
| **Activate Rule** | - For user who have the operate permission can activate an existing dry run live rule by right click menu in UI and effect immediately. After that this rule will be execute once trade/ cashflow follow into RATAN. ![image2024-8-16_16-22-40.png](attachments/image2024-8-16_16-22-40.png) |
| Update Rule | - For maker, user can update existing live rule by right click "Update Rule" - Input what condition you would like to update. - Input why you update this rule in Reason textarea. - Click "Update" to submit the update information. pending check to approve/reject. - Rule maker and checker should be different person. When checker verifies the rule, he/she can approve/reject as appropriate. ![image2024-8-16_16-26-27.png](attachments/image2024-8-16_16-26-27.png) ![image2024-8-16_16-27-36.png](attachments/image2024-8-16_16-27-36.png) |
| **Check History** | - User can view the change history for the specific record double click target record → choose Rule History tab. ![image2024-8-19_11-49-38.png](attachments/image2024-8-19_11-49-38.png) - User can view whole rule history by click "Rule Histories". ![image2024-8-19_11-56-2.png](attachments/image2024-8-19_11-56-2.png) ![image2024-8-19_11-55-12.png](attachments/image2024-8-19_11-55-12.png) |
| **Export Rule** | - User can export rule by click "Export". ![image2024-8-19_11-57-20.png](attachments/image2024-8-19_11-57-20.png) |
| **Filter Rule** | - For each field in Rule, it can be filtered for better view. ![image2024-8-19_11-58-43.png](attachments/image2024-8-19_11-58-43.png) ![image2024-8-19_11-59-31.png](attachments/image2024-8-19_11-59-31.png) |

For further details refer  [RATAN Rule Engine - User Manual Book - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/RATAN+Rule+Engine+-+User+Manual+Book)

# ***Settlement NSTP Rules [NEW]***

- *Rules can be defined in this table to prevent STP of Cashflows based on the parameters setup*
- *Impact of the rule must be considered before setup (i.e., how many cashflows will become NSTP due to the rule)*
- *Removal of existing rules must also be considered carefully (is it ok to STP these now)*
- *Rules currently setup in production are in link → *
- *Steps to setup / remove are similar to Suppression Rules below*

# ***Suppression Rules[Cashflow]

**ANCHOR: Cashflow Suppression**
***

- Suppression Rule will define the suppression condition for settlement. If cashflow satisfies the suppression rule, it will not be sent to downstream (Razor / FMSRE / AMH).
- Current rules have been replicated from MX2.11 →

The cashflow will not generate any Payment or Settlement Accounting. Hence rule should created only if it will not create any payment failure or reconciliation break.

Steps for maintenance: In Ratan, it has provided functions to create rule/delete rule/view history/Export data.

| Function | Steps |
| --- | --- |
| **Create Rule** | - For maker, user can create rules to Suppress Cashflow - For rule item, select required fields with values, different fields will be taken as 'AND' condition into the rule. - Reason will be displayed when the suppression is created. - Newly added rule will be effective once checker approves. - Rule maker and checker should be different person. When checker verifies the rule, he/she can approve/reject as appropriate. - More details can be found in <u>[auto cashflow suppression](#Suppression)</u> ![image2023-10-19_11-30-20.png](attachments/image2023-10-19_11-30-20.png) ![image2023-10-19_11-31-22.png](attachments/image2023-10-19_11-31-22.png) |
| **Delete Rule** | - For maker, user can delete an existing rule. - Newly deleted rule will be effective once checker approves. - Rule maker and checker should be different person. When checker verifies the rule, he/she can approve/reject deleting the rule. ![image2023-10-19_11-32-15.png](attachments/image2023-10-19_11-32-15.png) ![image2023-10-13_15-50-19.png](attachments/image2023-10-13_15-50-19.png) |
| **Check History** | - User can view the change history for the specific record in Suppression Rule > history tab. ![image2023-10-19_11-33-2.png](attachments/image2023-10-19_11-33-2.png) ![image2023-10-19_11-33-30.png](attachments/image2023-10-19_11-33-30.png) |
| **Export Rule** | ![image2023-10-19_11-34-28.png](attachments/image2023-10-19_11-34-28.png) |
| **Filter Rule** | - For each field in Rule, it can be filtered for better view. ![image2023-10-19_11-35-23.png](attachments/image2023-10-19_11-35-23.png) |

# ***Business Rule - Suppression Rules[Swift]***

- Suppression Rule[Swift] will define the suppression condition for swift message. If cashflow satisfies the suppression rule, it will not generate swift/payment in Razor.
- RATAN user with profile FMO_BR_APR/FMO_BR_MKR/FMO_OPS/FMO_OPS_SUP is able to update in Suppression Rule Tile.
- Currently no rules are setup for SWIFT suppression.
- In Ratan, it has provided functions to add rule/delete rule/check history/Export rule/filter rules, similar function can be found in <u>[Suppression Rule[Cashflow]](#Cashflow Suppression).</u>
- More Details can be found in .

# ***Auto Netting Rules***

- *This table provides the capability to setup auto netting of cashflows at a pre-defined date & time*
- *For China Day 1, this is not being required, hence not covered here*
- *Enhancement required to add VD-1 into the rule*

# ***Settlement NSTP Rules [FX & Equity]***

- *This Blotter is used for the legacy flow and legacy profiles (OPS / OPS_SUP) will do the maintenance, hence not covered here. In future, the legacy flow will be moved to Strategic flow*

# ***Suppression Rules ******[FX & Equity]***

- *This Blotter is used for the legacy flow and legacy profiles (OPS / OPS_SUP) will do the maintenance*, hence not covered here. In future, the legacy flow will be moved to Strategic flow**

# ***Rules Approval History***

| # | Rule (NSTP / Cashflow Suppression) | Criteria | Reason for request | Approval Date | Approved By | Comments |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | NSTP Rule | Cashflow.Booking_System_Event==NonEcoAmend | - To prevent duplicate payments on non financial amendments due to SI change from MX2.11 - Rule changed from 'High Risk NSTP 'to 'NSTP' | 2023-11-16 2023-11-21 | Prakash Gopi | |
| 2 | NSTP Rule | Cashflow.Booking_System_Event==Amendment | - To prevent duplicate payments on financial changes done after non financial amendments due to SI change from MX2.11 - Rule changed from 'High Risk NSTP 'to 'NSTP' | 2023-11-17 2023-11-21 | Prakash Gopi | |

# ***Rules Review History***

| # | Review Date | Reviewed By | Comments |
| --- | --- | --- | --- |
| | | | |