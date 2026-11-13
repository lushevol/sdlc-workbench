# Background

To increase even more of the settlement STP rate, we are building the capability of automating cashflow affirmation process

1. enable cashflow affirmation automated by email to client
2. to drive the auto settlement process with the response from AI factory layer

# Requirement Details

### System send email with required cashflow details

1. Scheduled time to send email 1. VD -1? 2. dynamic configured?
2. Select cashflow to be listed in the email 1. query condition? booking entity ? payment date? status? exception code? 2. hard code condition or dynamic rule configuration?
3. Email subject, from to and other predefined properties
4. Required fields in the email | Trade ID | Trade_Id | Y | for Gross cashflow, value is parent trade id, for netted resultant cashflow, value is **Net** | | --- | --- | --- | --- | | FlowID | Cashflow_Id | Y | cashflow id | | Entity | Booking_Entity_SCI_FMCODE | ? | cashflow booking entity name, | | Value Date | Payment_Date | Y | value date | | Counterpart | Counterparty_SCI_FMCODE | ？ | counterparty name, could be blank for net resultant | | Cur | Payment_Currency | Y | currency | | Amount | Payment_Amount | Y | credit / debit, SCB pay will be less than zero (-12,270.00), SCB receive will be greater than zero (12,270.00) | | SCB Pay / Receive | Pay_Receive_Indicator | Y | SCB Pay / SCB Receive | | Taxonomy | ISDA_Taxonomy | N | optional for resultant cashflow | | Portfolio | Booking_Entity_Trade_Portfolio_Name | N | optional for resultant cashflow | | Strategy | Murex_Product_Strategy | N | | | Bene_AC | Settlement_Instruction.Account. Beneficiary_Account_Number | N | special format: hide part of the number? XXX XXX 51869 | | Bene_Agent | settlement_Instruction.account. beneficiary_Bank_BIC_code | N | | | Bene_Int | settlement_Instruction.account. beneficiary_Correspondent_BIC_code | N | | | Email Field Name | Logic Model Field | Mandatory (Y/N) | Description | **Samples**: <details> <summary>Expand Details</summary> ![image-2025-12-25_15-33-23.png](attachments/image-2025-12-25_15-33-23.png)![image-2025-12-25_15-39-55.png](attachments/image-2025-12-25_15-39-55.png)![image-2025-12-25_15-46-20.png](attachments/image-2025-12-25_15-46-20.png)![image-2025-12-25_15-48-10.png](attachments/image-2025-12-25_15-48-10.png)![image-2025-12-25_16-51-1.png](attachments/image-2025-12-25_16-51-1.png) </details>
5. exception cases?

### System receive user confirmation and trigger cashflow STP

1. System receive user confirmation - technical integration changes
2. System trigger cashflow STP ： close the "pending affirmation" exception

# Business Use Case

| | Description | Scenario | Expected Result |
| --- | --- | --- | --- |
| 1 | email trigger cashflow auto STP | 1. cashflow received in Ratan and hold in WAITING status with "Pending Affirmation" status 2. system send email to user at scheduled time 3. user replied affirmation and system release the cashflow from NSTP queue | |
| 2 | | | |