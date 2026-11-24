# What is a Nostro Account?

A bank account held in a foreign country by a domestic bank, denominated in the currency of that country. <u>Nostro accounts</u> are used to facilitate settlement of foreign exchange and trade transactions. The term is derived from the Latin word for "ours." Conversely, accounts that are held by the domestic bank in its home country for foreign banks are called <u>Vostro accounts</u>, derived from the Latin word for "yours."

# What is a NAMS?

The NAMS system is the golden inventory source for all nostro accounts details (Cash & Securities) held by Standard Chartered Bank (SCB) and its subsidiaries. The system controls the account opening, closing and amendments through a standardized workflow. Publishing of account static data onto the banking infrastructure, thereby making it available for consumption by other applications and processes within the bank. Integrated with bank’s client identifier system to ensure accuracy and consistency of the information.

# What is scope of NAMS include?

-Cash/correspondent ,

-Financial Market Securities Operations

-Financial security services (Only Mauritius and DIFC with Third part agents is live for NAMS workflow )

# Open Nostro Account workflow

There are two types Nostro Account in NAMS. One is  **Cash/Correspondent (NA)** , another is **Securities (NS)** which include SSO, FMSO, PvB & WM and etc. So for different type NAMS prepared different workflow.

**EXPAND: Cash/Correspondent (NA)**

![](https://confluence.global.standardchartered.com/plugins/servlet/pptslide?attachment=NAMS+Workflow+Process+v0.4.pdf&attachmentId=1846184312&attachmentVer=1&pageId=1825423902&slide=0)

**EXPAND_END**

**EXPAND: Securities (NS) - SSO, FMSO, PvB & WM**

![](https://confluence.global.standardchartered.com/plugins/servlet/pptslide?attachment=Securities+Business+NAMS+workflow+-+On+Bal+Sheet+Open+Cash+and+Securities+Account+v0.1.pdf&attachmentId=1825424068&attachmentVer=1&pageId=1825423902&slide=0)

**EXPAND_END**

# How to create a Nostro Account in NAMS?

**EXPAND: Creation details**

## *Step 1:  *login into NAMS: [https://smartflow.gdc.standardchartered.com/prweb/PRWebLDAP1/app/NAMS/](https://smartflow.gdc.standardchartered.com/prweb/PRWebLDAP1/app/NAMS/)

![image2022-8-26_16-20-55.png](attachments/image2022-8-26_16-20-55.png)

## *Step 2:  *Login the system and you will see below page , then Click '**+ Create**' → Choose the '**Open Nostro Account**'

![image2022-8-26_16-49-34.png](attachments/image2022-8-26_16-49-34.png)

## *Step 3:  *Fill the business requirement information

![Picture1.png](attachments/Picture1.png)

**SCB Entity**

- Account requesting entity or which SCB entity is requesting new account opening
- There is dropdown available to select the respective SCB entity as per business requirement. User need to select from dropdown

* Requestor need to be sure about SCB Entity and the best combination to ascertain the SCB Entity as per requirement is – Name + Country + LEID. In case of ambiguity request should confirm by Network manager of that market

**Business Type**

- Requestor need to select business type based on an account type. If it is correspondent bank account, requestor need to select the same. if security account kindly refers DOI for security accounts

**Currency**

- Select currency as per the requirement of the business

**Provider Country**

## *Step 4:  Fill the below form as per business requirements and click search*

Below Screen will appears, if for respective SCB Entity and Currency any Nostro is available it will reflect in the below highlighted screen.  Purpose of this screen to broadcast the list of available Nostro for that currency in respective country.  Requestor can either choose one or click to **CREATE NEW**

**![Picture2.png](attachments/Picture2.png)**

## Step 5:  Fill the below form*** ***

![Picture3.png](attachments/Picture3.png)

- Highlighted in yellow information is predefined based on previous selection and rest need to be update by the requestor
- Expected Average Transaction Volumes Per Month**: **Please select from the drop down, it could be 0-50,50-100 & >100
- Account required for Regulatory Purposes: Requestor can check this box if account is required to fulfil any regulatory requirement
- SSI: This is defaulted to NON-SSI however requestor can choose as per business requirement

1. 1. NON-SSI: Transactions of two or more entities are combined and carried in the name of the account holder 2. SSI: Designated for special purpose activities or dedicated to single client

- Business Owner**: **the primary business requiring/requesting the Nostro (best efforts, utility nostros like SSI used by all businesses, this can be a challenge, in that case defer to most senior Ops person in-country)
- Reconciliation Owner: Requestor need to select from drop down menu as per below guidance

1. 1. GRU: Account reconciled in TLM 2. IRU: Inter country reconciliation unit

- Target Balance: Requestor can either fill this is it is known or leave blank as it will be updated by Treasury market
- Business Justification: This is very important column to be filed by request and below is the guidance

1. 1. Requestor should explicitly explain about the business requirement and justify the need to this account to gain further approvals 2. Requestor should explain why can’t existing account be used if any to gain further approvals

## *Step 6:  Below screen is part of the same form and it depicts existing Nostro Account Providers to SCB selected entity for that currency in respective country.*

- Requestor can choose the available service provider or agent bank as per business requirement
- If service provider is not available in this screen, please move to step 7

![Picture4.png](attachments/Picture4.png)

## *Step 7:  Below screen is part of the same form and if requestor didn’t find the required service provider or agent bank as per business requirement. Requestor can propose the agent bank into below field*

![Picture5.png](attachments/Picture5.png)

![Picture6.png](attachments/Picture6.png)

* It is highly recommended to reach out to respective Network manager before proposing a new agent to ensure required agent is in SCB Network. NM’s have the final say on Agent selection. * Once agent is selected click “**NEXT”***

## *Step 8:  Team and System Details*

This part of the form is very important as based on the selection approvals will be triggered and account will be setup in respective TP systems. Requestor need to select team and respective TP Systems

![Picture7.png](attachments/Picture7.png)

![Picture8.png](attachments/Picture8.png)

## *Step 9:  **Account Info*

Below information can be filled by requestor if available

![Picture9.png](attachments/Picture9.png)

## *Step 10:  Once relevant information is submitted the NAMS case reference will be generated and requestor need to track till closure*

**EXPAND_END**

# NAMS Approvals

NAMS has three stages for an account opening

1. Initiation
2. Approval
3. Account Opening or setup

![Picture10.png](attachments/Picture10.png)

# Who can help during the whole process?

NM_COE <NM_COE@[sc.com](http://sc.com)> can help guild to resolve the issues during the process.

# Reference document:

[NAMS - Documents and Other Resources - FS Client Service Group - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/pages/viewpage.action?spaceKey=FCSG&title=NAMS+-+Documents+and+Other+Resources#NAMSDocumentsandOtherResources)