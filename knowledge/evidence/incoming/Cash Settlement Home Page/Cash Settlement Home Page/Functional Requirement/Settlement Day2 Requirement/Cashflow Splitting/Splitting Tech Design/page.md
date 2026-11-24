> **INFO**
> This page describing details cashflow split tech design

# Splitting Core Function

## Service Interaction

v

## Table Design

```sql
CREATE TABLE cash_netting_service.splitting_cashflow (
	id bigserial NOT NULL,
	cashflow_character text NULL,
	"action" text NULL,
	splitting_id text NULL,
	cashflow_id text NULL,
	business_version text NULL,
	minor_version text NULL,
	amount text NULL,
	currency text NULL,
	counterparty_fmid text NULL,
	entity_fmid text NULL,
	payment_date timestamp NULL,
	status text  NULL,
	split_type text NULL,
	created_at timestamp DEFAULT now() NOT NULL,
	updated_at timestamp NULL
	CONSTRAINT splitting_cashflow_pkey PRIMARY KEY (id)
);
CREATE INDEX splitting_cashflow__cashflow_id_index ON cash_netting_service.splitting_cashflow USING btree (cashflow_id);
CREATE INDEX splitting_cashflow__splitting_id_index ON cash_netting_service.splitting_cashflow USING btree (splitting_id);
```

## Workflow Change

1、Cash_Settlement_Inbound on Withdrawal Scenario

![image-2025-11-5_16-30-35.png](attachments/image-2025-11-5_16-30-35.png)

2、Version Control

![image-2025-8-14_15-45-27.png](attachments/image-2025-8-14_15-45-27.png)

3、Send_To_Swift_GateWay（autosplit)

![image-2025-8-14_15-44-19.png](attachments/image-2025-8-14_15-44-19.png)

# Manual Splitting

## Manual splitting disable for currency PM

| no | option solution | comment |
| --- | --- | --- |
| 1 | | |
| 2 | | |

# Auto Splitting

# Split rule static

## split rule state machine

# Detailed Design

## New API

### Manual splitting api

**EXPAND: Request Schema**

```
method: post
url: /v1/cashSettlement/cashflows/manualSplit
content-type: application/json
request:
{
	"parentCashflow": {
		"cashflowId": "M00551190000",
		"amount": "10",
		"currency": "CNO"
	},
	"childCashflows": [
		{
			"amount": "4",
			"currency": "CNO",
	        "vostroAccount": {
				"ssiType": "Secondary",
				"swiftType": "MT202",
				"settlementMeans": "NOS",
				"settlementAccount": "XAU MAIN",
				"beneficiaryBic": "CHASGB2LXXX",
				"beneficiaryName": "VIRTU FINANCIAL GLOBAL MARKETS LLC",
				"beneficiaryName2": "",
				"beneficiaryAddress": "OA JP MORGAN CHASE BANK NA LDN",
				"beneficiaryCity": "United States",
				"beneficiaryAccount": "",
				"isThirdPartyPayment": "N",
				"coveredPayment": "N",
				"charges": "",
				"accountWithInstitutionBic": "CHASCHGXBUL",
				"accountWithInstitutionName": "",
				"accountWithInstitutionAddress": "",
				"accountWithInstitutionCity": "",
				"accountWithInstitutionAccount": "",
				"intermediaryBic": "UBSBCHZZXXX",
				"intermediaryName": "",
				"intermediaryAddress": "",
				"intermediaryPostcode": "",
				"intermediaryAccount": "",
				"receiversCorrespondentBic": "",
				"receiversCorrespondentName": "",
				"receiversCorrespondentAddress": "",
				"receiversCorrespondentCity": "",
				"receiversCorrespondentAccount": "",
				"orderCustomerBic": "CHASUS33FXR",
				"orderCustomerName": "VIRTU FINANCIAL GLOBAL MARKETS LLC OA JP MORGAN CHASE BANK NA LDN",
				"orderCustomerAddress": "1111 POLARIS PARKWAY CBS",
				"orderCustomerCity": "UNITED STATES OF AMERICA",
				"orderCustomerAccount": "400935394",
				"senderToReceiver1": "",
				"senderToReceiver2": "",
				"senderToReceiver3": "",
				"senderToReceiver4": "",
				"senderToReceiver5": "",
				"senderToReceiver6": "",
				"remittanceInformation1": "",
				"remittanceInformation2": "",
				"remittanceInformation3": "",
				"remittanceInformation4": "",
				"popDubai": "",
				"settlementMethod": "CASH",
                "ssiId": "sssss"
			},
			"nostroAccount": {
				"settlementMeans": "NOS",
				"settlementAccount": "XAU MAIN",
				"sendersCorrespondent53Swift": "CHASGB2LBUL",
				"sendersCorrespondent53Fullname": "JPMORGAN CHASE BK NA PRE LET LDN",
				"sendersCorrespondent53Address": "125 LONDON WALL EC2Y 5AJ",
				"sendersCorrespondent53City": "LONDON",
				"sendersCorrespondent53Account": "779",
				"noticeToReceive": "N",
				"ebbsNostroAccount": "XXXXXXXXXXX"
			}
        },
		{
			"amount": "6",
			"currency": "CNO",
	        "vostroAccount": {
				"ssiType": "Secondary",
				"swiftType": "MT202",
				"settlementMeans": "NOS",
				"settlementAccount": "XAU MAIN",
				"beneficiaryBic": "CHASGB2LXXX",
				"beneficiaryName": "VIRTU FINANCIAL GLOBAL MARKETS LLC",
				"beneficiaryName2": "",
				"beneficiaryAddress": "OA JP MORGAN CHASE BANK NA LDN",
				"beneficiaryCity": "United States",
				"beneficiaryAccount": "",
				"isThirdPartyPayment": "N",
				"coveredPayment": "N",
				"charges": "",
				"accountWithInstitutionBic": "CHASCHGXBUL",
				"accountWithInstitutionName": "",
				"accountWithInstitutionAddress": "",
				"accountWithInstitutionCity": "",
				"accountWithInstitutionAccount": "",
				"intermediaryBic": "UBSBCHZZXXX",
				"intermediaryName": "",
				"intermediaryAddress": "",
				"intermediaryPostcode": "",
				"intermediaryAccount": "",
				"receiversCorrespondentBic": "",
				"receiversCorrespondentName": "",
				"receiversCorrespondentAddress": "",
				"receiversCorrespondentCity": "",
				"receiversCorrespondentAccount": "",
				"orderCustomerBic": "CHASUS33FXR",
				"orderCustomerName": "VIRTU FINANCIAL GLOBAL MARKETS LLC OA JP MORGAN CHASE BANK NA LDN",
				"orderCustomerAddress": "1111 POLARIS PARKWAY CBS",
				"orderCustomerCity": "UNITED STATES OF AMERICA",
				"orderCustomerAccount": "400935394",
				"senderToReceiver1": "",
				"senderToReceiver2": "",
				"senderToReceiver3": "",
				"senderToReceiver4": "",
				"senderToReceiver5": "",
				"senderToReceiver6": "",
				"remittanceInformation1": "",
				"remittanceInformation2": "",
				"remittanceInformation3": "",
				"remittanceInformation4": "",
				"popDubai": "",
                "ssiId": "sssss" ,
                "settlementMethod": "CASH"
			},
			"nostroAccount": {
				"settlementMeans": "NOS",
				"settlementAccount": "XAU MAIN",
				"sendersCorrespondent53Swift": "CHASGB2LBUL",
				"sendersCorrespondent53Fullname": "JPMORGAN CHASE BK NA PRE LET LDN",
				"sendersCorrespondent53Address": "125 LONDON WALL EC2Y 5AJ",
				"sendersCorrespondent53City": "LONDON",
				"sendersCorrespondent53Account": "779",
				"noticeToReceive": "N",
				"ebbsNostroAccount": "XXXXXXXXXXX"
			}
        }
	],
	"affirmationDetails": {
		"affirmedBy": "test",
		"phone_email": "test.com",
		"affirmedAt": 1747374638465
    }
}
respone:
{
    "status": 200,
    "message": "cashflowId M00000039085 split successful",
    "data": null
}
```

**EXPAND_END**

### Auto splitting api

**EXPAND: Request Schema**

```
method: post
url: /v1/cashSettlement/cashflows/camunda/autoSplit
content-type: application/json
request:
{
	"trackingId": "44233223",
	"message": "scbml"
}
respone:
{
}
```

**EXPAND_END**

### Get currency precision api

**EXPAND: Request Schema**

```
method: get
url: /v1/cashflow/lifecycle/getRoundingConfig/{currency}

response:
{
    "currency": "USD",
	"precision": 2,
    "type": "ROUNDING_OFF"
}
```

**EXPAND_END**

### Splitting Static - Create splitting rule api

**EXPAND: Request Schema**

```
method: post
url: /v1/static/splittingRule/create
request: 
{
    "entityFmId": "10075222",
    "nostroAgent": "SCBLUS33XXX",
    "currency": "TRY",
    "threshold": "80000000",
    "amount": "2000000",
    "limitation": "60000000"
}

response:
{
    "status": 200,
    "errorCode": "200",
    "errorMessage": "success"
}
```

**EXPAND_END**

### Splitting Static - Update splitting rule api

**EXPAND: Request Schema**

```
method: post
url: /v1/static/splittingRule/update
request: 
{
    "id": 7,
    "entityFmId": "ALL",
    "nostroAgent": "ALL",
    "currency": "TRY",
    "threshold": "90000000",
    "amount": "2000000",
    "limitation": "60000000"
}

response:
{
    "status": 200,
    "errorCode": "200",
    "errorMessage": "success"
}
```

**EXPAND_END**

### Splitting Static - Confirm splitting rule api for checker approve

**EXPAND: Request Schema**

```
method: post
url: /v1/static/splittingRule/confirm
request: 
{
    "id": 7
}

response:
{
    "status": 200,
    "errorCode": "200",
    "errorMessage": "success"
}
```

**EXPAND_END**

### Splitting Static - Reject splitting rule api for checker reject

**EXPAND: Request Schema**

```
method: post
url: /v1/static/splittingRule/reject
request: 
{
    "id": 8
}

response:
{
    "status": 200,
    "errorCode": "200",
    "errorMessage": "success"
}
```

**EXPAND_END**

### Splitting Static - Delete splitting rule api

**EXPAND: Request Schema**

```
method: delete
url: /v1/static/splittingRule/delete/{id}

response:
{
    "status": 200,
    "errorCode": "200",
    "errorMessage": "success"
}
```

**EXPAND_END**

### Splitting Static - Query splitting rules api

**EXPAND: Request Schema**

```
method: get
url: /v1/static/splittingRule/query?page=0&size=2&entityFmId=400001378&nostroAgent=SCBLSG22XXX&currency=USD
request params:
 page: required
 size: required
 entityFmId: optional
 nostroAgent: optional
 currency: optional

response:
{
    "pageNo": 0,
    "pageSize": 2,
    "totalPages": 2,
    "totalHits": 4,
    "results": [
        {
            "id": 3,
            "ruleUniqued": 3,
            "entityFmId": "10075222",
            "nostroAgent": "ALL",
            "currency": "USD",
            "threshold": "200",
            "amount": "50",
            "limitation": "100",
            "dataStatus": "SAVE_CONFIRMED",
            "referenceId": null,
            "makerId": "1622463",
            "checkerId": "1622463",
            "createdAt": "2025-09-01T11:17:37Z",
            "updatedAt": "2025-09-01T11:20:26Z"
        }
    ]
}
```

**EXPAND_END**

### Splitting Static - Query splitting rule audit api

**EXPAND: Request Schema**

```
method: get
url: /v1/static/splittingRule/audit?page=0&size=2&ruleUniqueId=4
response:
{
    "pageNo": 0,
    "pageSize": 2,
    "totalPages": 3,
    "totalHits": 6,
    "results": [
        {
            "id": 7,
            "ruleUniqueId": 4,
            "splittingManipulation": {
                "id": 9,
                "ruleUniqued": 4,
                "entityFmId": "10075222",
                "nostroAgent": "SCBLUS33XXX",
                "currency": "TRY",
                "threshold": "80000000",
                "amount": "2000000",
                "limitation": "60000000",
                "dataStatus": "DISCARDED",
                "referenceId": 7,
                "makerId": "1622463",
                "checkerId": "1434424",
                "createdAt": "2025-09-16T07:55:15Z",
                "updatedAt": "2025-09-16T07:55:15Z"
            },
            "action": "Reject",
            "dataStatus": "DISCARDED",
            "userId": "1434424",
            "createdAt": "2025-09-17T03:19:11Z"
        },
        {
            "id": 5,
            "ruleUniqueId": 4,
            "splittingManipulation": {
                "id": 9,
                "ruleUniqued": 4,
                "entityFmId": "10075222",
                "nostroAgent": "SCBLUS33XXX",
                "currency": "TRY",
                "threshold": "80000000",
                "amount": "2000000",
                "limitation": "60000000",
                "dataStatus": "DELETE_PENDING",
                "referenceId": 7,
                "makerId": "1622463",
                "checkerId": "1622463",
                "createdAt": "2025-09-16T07:55:15Z",
                "updatedAt": "2025-09-16T07:55:15Z"
            },
            "action": "Delete",
            "dataStatus": "DELETE_PENDING",
            "userId": "1622463",
            "createdAt": "2025-09-16T07:55:15Z"
        }
    ]
}
```

**EXPAND_END**

### Cashflow UnSplit Api

**EXPAND: Request Schema**

```
method: post
url: /v1/cashSettlement/cashflows/unsplit
request: 
{
  "cashflowId": "M00000039085",
  "minorVersion": "3",
  "businessVersion": "0",
  "splittingId": "356acc61-79ad-11f0-9855-005056acee79"
}

response:
{
	"status": 200,
	"message": "cashflowId M00000039085 unsplit successful",
	"data": null
}
```

**EXPAND_END**

### Cashflow Amend Amount Api

**EXPAND: Request Schema**

```
method: POST
url:  /v1/cashSettlement/cashflows/amendSplitAmount
request: 
{
  "splittingId": "M00000039085",
  "requestList": [
  {
    "cashflowId": "M00000039085",
    "amount": "1.11"
  }
  ]
}

response:
{
	"status": 200,
	"message": "Amend amount success",
	"data": null
}or
{
"status": 500,
"message": "error msg",
"data": null
}
```

**EXPAND_END**

# RATAN Restful API To External

| Change | Details | Remarks |
| --- | --- | --- |
| API | /api/v2/data/provider/query/cashflows | No change |
| Query Service | Indexing splitting id in the table | |
| | | |

# Relevant Service

| Service | Feature Branch | Version | Comments |
| --- | --- | --- | --- |
| ratan-cashflow-lifecycle-service | [feature/settlement-day2-split-common](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cashflow-lifecycle-service) | 3.4.0 | |
| ratan-cash-settlement-netting-service | [feature/settlement-day2-split-common](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cash-settlement-netting-service) | 1.7.0 | |
| ratan-cash-settlement-query-service | [feature/settlement-day2-split-9939815](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cash-settlement-query-service) | 3.2.0 | |
| ratan-cash-settlement-orchestration | [feature/settlement-day2-split-common](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cash-settlement-orchestration?path=%2F&version=GBfeature%2Fsettlement-day2-split-common&_a=contents) | 3.4.0 | |
| ratan-cash-settlement-accounting-service | feature/settlement-day2-split-common | 1.4.0 | |
| ratan-cash-settlement-ssi-stamping-service | feature/split-with-ssi | 2.5.8 | |
| ratan-cash-settlement-group-management-service | [feature/settlement-day2-split-common](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cash-settlement-group-management-service) | 2.2.0 | |
| ratan-rule-service | [feature/settlement-day2-split-common](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-rule-service) | 2.3.0 | |
| ratanone-rule-service | [feature/settlement-day2-split-common](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-rule-service) | 2.4.0 | |
| ratanone-swift-service | [feature/settlement-day2-split-common](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-swift-service) | 2.5.0 | |
| ratanone-static-data-service | [feature/settlement-day2-split-common](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-swift-service) | 3.7.0 | |
| ratanone-db-repository | [feature/settlement-day2-split-common](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cash-settlement-group-management-service) | develop | |

# Test cases

| No | scenario | steps | comment |
| --- | --- | --- | --- |
| 1 | manual split with calling lifecycle timeout to update status | 1. book new cashflow C1 2. insert sleep code in update status api of lifecycle service to simulate processing timeout. 3. manual split cashflow C1 to 20 child cashflow S1 to S20 | env: uat6 sample: M0Q107000006 **EXPAND: evidence** 1.insert code that sleep 6min40s before update status for simulate processing timeout, then deploy to uat6 ![image-2025-11-14_23-16-18.png](attachments/image-2025-11-14_23-16-18.png) 2. manual split cashflow to 5 child cashflows ![image-2025-11-14_23-16-34.png](attachments/image-2025-11-14_23-16-34.png) 3. in netting service, calling lifecycle service timeout when update parent and child cashflows status to SPLIT, then popup error log. ![image-2025-11-14_23-17-10.png](attachments/image-2025-11-14_23-17-10.png) 4.after lifecycle processing successfully, compensate the child cashflows to proceed by consuming domain event of parent cashflow ![image-2025-11-14_23-17-21.png](attachments/image-2025-11-14_23-17-21.png) 5.in cashflow blotter, parent cashflow split to child cashflows successfully. ![image-2025-11-14_23-16-54.png](attachments/image-2025-11-14_23-16-54.png) **EXPAND_END** |
| 2 | auto split with calling lifecycle timeout to update status | 1. create split rule in nostro threshold static blotter 2. book new cashflow C1 which meet above split rule 3. (**pre process**)insert sleep code in update status api of lifecycle service to simulate processing timeout. 4. early release cashflow C1 | env: uat6 sample: M0Q107000008 behavior: 1. parent cashflow - READY->TechFail 2. child cashflows - not generate child cashflows **EXPAND: evidence** 1.insert code that sleep 6min40s for simulate processing timeout, then deploy to uat6 ![image-2025-11-14_23-16-18.png](attachments/image-2025-11-14_23-16-18.png) 2.create split rule which will meet the test cashflow ![image-2025-11-15_12-36-22.png](attachments/image-2025-11-15_12-36-22.png) 3.early release this cashflow ![image-2025-11-15_12-36-42.png](attachments/image-2025-11-15_12-36-42.png) 4.this cashflow hit this split rule and split to several child cashflows from log ![image-2025-11-15_20-47-26.png](attachments/image-2025-11-15_20-47-26.png) 6.cammuda detect the timeout of auto split api, then move parent cashflow status to TechFail but not generate child cashflows ![image-2025-11-15_20-48-28.png](attachments/image-2025-11-15_20-48-28.png) **EXPAND_END** |
| 3 | auto split with calling lifecycle timeout to update status | 1. create split rule in nostro threshold static blotter 2. book new cashflow C1 which meet above split rule 3. (**process**)insert sleep code in update status api of lifecycle service to simulate processing timeout. 4. early release cashflow C1 | env: uat6 sample: M0Q107000010 behavior: 1. parent cashflow - READY->SPLIT->TechFail 2. child cashflows - generate child cashflows but stuck in Queue status **EXPAND: evidence** 1.insert code that sleep 6min40s for simulate processing timeout, then deploy to uat6 ![image-2025-11-15_21-23-38.png](attachments/image-2025-11-15_21-23-38.png) 2.create split rule which will meet the test cashflow ![image-2025-11-15_12-36-22.png](attachments/image-2025-11-15_12-36-22.png) 3.early release this cashflow ![image-2025-11-15_21-23-50.png](attachments/image-2025-11-15_21-23-50.png) 4.this cashflow hit this split rule and split to several child cashflows from log ![image-2025-11-15_21-39-22.png](attachments/image-2025-11-15_21-39-22.png) 6.cammuda detect the timeout of auto split api, then move parent cashflow status to TechFail but generate child cashflows and stuck in Queue status ![image-2025-11-15_21-38-13.png](attachments/image-2025-11-15_21-38-13.png)![image-2025-11-15_21-38-20.png](attachments/image-2025-11-15_21-38-20.png) 7.not trigger compensate child cashflows from log Discover - Elastic **EXPAND_END** |
| 4 | auto split with calling lifecycle timeout to update status | 1. create split rule in nostro threshold static blotter 2. book new cashflow C1 which meet above split rule 3. (**post process**)insert sleep code in update status api of lifecycle service to simulate processing timeout. 4. early release cashflow C1 | env: uat6 sample: M0Q107000009 behavior: 1. parent cashflow - READY→SPLIT->TechFail 2. child cashflows - generate child cashflows successfully **EXPAND: evidence** 1.insert code that sleep 6min40s for simulate processing timeout, then deploy to uat6 ![image-2025-11-15_20-40-53.png](attachments/image-2025-11-15_20-40-53.png) 2.create split rule which will meet the test cashflow ![image-2025-11-15_12-36-22.png](attachments/image-2025-11-15_12-36-22.png) 3.early release this cashflow ![image-2025-11-15_12-36-42.png](attachments/image-2025-11-15_12-36-42.png) 4.this cashflow hit this split rule and split to several child cashflows from log ![image-2025-11-15_12-37-12.png](attachments/image-2025-11-15_12-37-12.png) 5.generate child cashflows successfully ![image-2025-11-15_12-39-23.png](attachments/image-2025-11-15_12-39-23.png) 6.cammuda detect the timeout of auto split api, then move parent cashflow status to TechFail ![image-2025-11-15_12-39-34.png](attachments/image-2025-11-15_12-39-34.png) **EXPAND_END** |
| 5 | auto split fail due to the auto split rule is not reasonable, which will auto split too many child cashflows. | 1. book new cashflow C1, amount like 10000000 2. set auto split rule like 1. threshold: 1000 2. amoun:100 3. limitation: 200 | **EXPAND: evidence** first splitting: ![image-2025-11-14_11-9-49.png](attachments/image-2025-11-14_11-9-49.png) ![image-2025-11-14_11-23-17.png](attachments/image-2025-11-14_11-23-17.png) after modify the auto split rule, then manual fail → reinstate, cashflow auto split successful. ![image-2025-11-14_11-40-14.png](attachments/image-2025-11-14_11-40-14.png) ![image-2025-11-14_11-43-9.png](attachments/image-2025-11-14_11-43-9.png) **EXPAND_END** |