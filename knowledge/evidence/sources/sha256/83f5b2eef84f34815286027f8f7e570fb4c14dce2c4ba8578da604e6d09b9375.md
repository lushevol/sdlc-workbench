**Table of Contents**

# ***Document History***

| Version | Date | Author | Description of Change |
| --- | --- | --- | --- |
| V0.1 | | Feng, Lina | |
| V0.2 | 2025-08-06 | Xue, Carrie | Added description of auto netting |

# User Access

RATAN user with profile FMO_STA_CKR/FMO_STA_MKR is able to update in Netting and Nostro Static Tile.

[How to apply for RATAN ONE access - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/How+to+apply+for+RATAN+ONE+access)

# Netting Static

Netting static is to setup netting client checking rule in RATAN ONE.  "Rule type" is to indicate it's created for auto netting or manual netting

![image-2025-8-7_11-46-4.png](attachments/image-2025-8-7_11-46-4.png)

- For maker, user can add rule/delete rule/check history in Netting Static.

![image2023-9-22_13-6-42.png](attachments/image2023-9-22_13-6-42.png)

- When adding rule, select required fields with values, then fill in Reason. Different fields will be taken as 'AND' condition into the rule.

![image2023-9-22_13-10-8.png](attachments/image2023-9-22_13-10-8.png)

- if need to add **auto netting** rule, system will populate extra fields for user to config ![image-2025-7-31_20-32-53.png](attachments/image-2025-7-31_20-32-53.png)

- - **Netting Date Time**: define the time when system start to perform netting - **STP Level**: define the STP level for netting resultant cashflow - NSTP_MAKER_CHECKER - NSTP_CHECKER_ONLY - **Netting Type: **different netting type will have different result, please make sure this is set correctly

![image-2025-7-31_21-1-45.png](attachments/image-2025-7-31_21-1-45.png)

- Auto netting rule creation/update/disable will trigger cashflow refresh - if data ops **create new auto netting rule,** system will check all cashflow in below status and filter a list of cashflow need to be refreshed - **Refresh **Netting id ='' or Netting id is null** **and Cashflow_Status = WAITING (Pending Netting, Pending Exception) or Cashflow_Status = READY (cashflow state type is null) and meet the rule condition - **NOT** refresh cashflow in WAITING (Pending Another leg, Pending Auto netting) READY (Pending Ack), HOLD, SUPPRESSED, NETTED, RELEASED, SETTLED - if data ops **disable existing auto netting rule, **system will refresh below cashflow - **Refresh** Cashflow_Status = WAITING (Pending Auto Netting) and tagged to the disabled rule - **NOT** refresh cashflow in WAITING (Pending Another leg, Pending Netting, Pending Exception), READY, HOLD, SUPPRESSED, NETTED, RELEASED, SETTLED - if data ops **update existing rule**, - Update existing auto netting rule without rule type change - **Refresh **Cashflow_Status = WAITING (Pending Auto Netting) and tagged to the updated rule - **Refresh **Netting id ='' or Netting id is null** **and Cashflow_Status = WAITING (Pending Netting, Pending Exception) or Cashflow_Status = READY (cashflow state type is null) and meet the rule condition - **NOT** refresh cashflow in WAITING (Pending Another leg, Pending Auto netting) READY (Pending Ack), HOLD, SUPPRESSED, NETTED, RELEASED, SETTLED - Update manual netting rule to auto netting rule - **Refresh **Netting id ='' or Netting id is null** **and Cashflow_Status = WAITING (Pending Netting, Pending Exception) or Cashflow_Status = READY (cashflow state type is null) and meet the rule condition - **NOT** refresh cashflow in WAITING (Pending Another leg, Pending Auto netting) READY (Pending Ack), HOLD, SUPPRESSED, NETTED, RELEASED, SETTLED - Update auto netting rule to manual netting rule - **Refresh** Cashflow_Status = WAITING (Pending Auto Netting) and tagged to the rule - **NOT** refresh cashflow in WAITING (Pending Another leg, Pending Netting, Pending Exception), READY, HOLD, SUPPRESSED, NETTED, RELEASED, SETTLED

- Newly added rule will be effective once checker approves.
- Rule maker and checker should be different person. When checker verifies the rule, he/she can approve/reject the rule.

![image2023-9-22_13-21-57.png](attachments/image2023-9-22_13-21-57.png)

# Nostro Static

Nostro static records all the Nostro data in RATAN ONE table, it's used for cashflow SSI stamping before sending to any downstream.

- Nostro static list show all nostro record except deleted ones.
- User can view nostro details in form view by double click the record in list view:

![image2023-9-27_16-4-47.png](attachments/image2023-9-27_16-4-47.png)

- User can view the change history for the specific record in nostro details popup > history tab.

![image2023-9-27_16-8-45.png](attachments/image2023-9-27_16-8-45.png)

- User can view change history for all nostro records (including deleted records) by clicking History button from list view.

![image2023-9-27_20-13-40.png](attachments/image2023-9-27_20-13-40.png)

![image2023-9-27_20-18-29.png](attachments/image2023-9-27_20-18-29.png)

- For maker, user can create/update/delete Nostro in Nostro Static.

![image2023-9-27_20-20-21.png](attachments/image2023-9-27_20-20-21.png)

- When Creating/Updating Nostro, fields with * are mandatory. - Legal Entity FMCode, Legal Entity FMID, CCY, Settlement Means, Settlement Account and EBBS account are mandatory. - Correspondent Swift and Nostro Account are mandatory when 'NOS' is chosen as Settlement Means. (For Korea Nostro, Settlement Means= 'NOX' & Settlement Account in ('KRO UIBOK', 'KRO BOKSEO'), Correspondent Swift is mandatory, 11 characters; account in 'eBBS information' must be 6 digits)

![image2023-9-22_13-36-38.png](attachments/image2023-9-22_13-36-38.png)

- Duplicate check: when maker submit the change and there is existing record with the same key values (Legal entity FMID, currency, settlement means, settlement account and ccy pair), system will return error message:

![image2023-9-27_16-26-16.png](attachments/image2023-9-27_16-26-16.png)

- Primary check: when maker create/update the nostro with primary flag ticked and there is existing primary nostro for the same legal entity fmid + currency, system will return error message:

![image2023-9-27_18-59-55.png](attachments/image2023-9-27_18-59-55.png)

- Nostro maker and checker should be different person. When checker verifies the Nostro, he/she can submit/Reject the Nostro.

![image2023-9-22_13-39-15.png](attachments/image2023-9-22_13-39-15.png)

- Newly added/updated/deleted Nostro will be effective once checker approves.
- User is able to export the static data

![image2023-9-27_15-58-10.png](attachments/image2023-9-27_15-58-10.png)

- Ability to update Start/End date to enable/disable the Nostro: the feature to be added in Q4 2023.