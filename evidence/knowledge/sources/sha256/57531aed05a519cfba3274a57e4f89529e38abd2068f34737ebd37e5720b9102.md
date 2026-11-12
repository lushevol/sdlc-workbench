> **INFO**
> Detailed business requirement could refer to [Cashflow Auto Netting - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Cashflow+Auto+Netting)

# 1. Business Workflow

![](https://confluence.global.standardchartered.com/download/attachments/3287980420/AutoNetting.png?version=13&modificationDate=1747363425000&api=v2)

# 2. Camunda Workflow

![screenshot-process.png](attachments/screenshot-process.png)

# 3. Service Interaction

### 3.1 Auto Net Rule Check(netting service)

### 3.2 Cashflow Auto Net Job(netting service)

### 3.3 Cashflow refresh By Rule Changed(netting service)

# 4. Detailed Design

## 4.1. New API

### 4.1.1. Rule Management (Directly interaction with Rule Engine API)

**EXPAND: Request Schema**

```
create auto netting rule request:
{
    "id": "7336280228010184705",
    "businessFlow": "STRATEGIC_SETTLEMENT",
    "ruleType": "AUTO_NETTING",
    "userRule": "BCS_Trade_Id == \"s33\"",
    "runningRule": "",
    "status": "PROCESSING",
    "reason": "test",
    "metaData": "{\"ruleUuid\":\"5330079720543199232\",\"autoNettingConfig\":{\"nettingDate\":\"VD-1\",\"nettingTime\":\"09:00\",\"stpLevel\":\"FULL_STP\",\"nettingType\":\"Bilateral Netting\",\"ruleActiveTime\":\"2025-05-26 11:12:00\"}}",
    "needDryRun": false,
    "version": 0,
    "createdAt": "2025-06-05T06:38:27.853065197Z",
    "updatedAt": "2025-06-05T06:38:27.853073295Z",
    "createdBy": "1622463",
    "updatedBy": "1622463"
}

metaData structure in above request:
{
	"ruleUuid": "5330079720543199232",
	"autoNettingConfig": {
		"nettingDate": "VD-1",
		"nettingTime": "09:00",
		"stpLevel": "FULL_STP",
		"nettingType": "Bilateral Netting",
		"ruleActiveTime": "2025-05-26 11:12:00"
	}
}
```

**EXPAND_END**

### 4.1.2. Auto Netting API (Trigger by control M job)

**EXPAND: Request**

method: get

url: /v1/cashflows/autoNetting/job

**EXPAND_END**

**EXPAND: Response**

{
    "success":  true

"message": ""

}

**EXPAND_END**

### 4.1.3 Auto Netting Rule Check API

**EXPAND: Request**

method: get

url: /v1/cashflows/autoNetting/check

**EXPAND_END**

**EXPAND: Response**

CamundaApiResponse
case 1: matched auto netting rule

{
    "camundaResponseCode": "SUCCESS”,

"metadata": {

"autoNettingRuleCheckResultCode": 'HIT_AUTO_NETTING'

}
}

case 2: not matched auto netting rule

{
    "camundaResponseCode": "FILTERED”,

"metadata": {

"autoNettingRuleCheckResultCode": "NOT_HIT_AUTO_NETTING"

}
}

**EXPAND_END**

## 4.2. New Tables

### 4.2.1. table(ratan_auto_netting_cashflow)

| # | column | type | comments |
| --- | --- | --- | --- |
| 1 | id | Bigserial | PK |
| 2 | cashflow_id | TEXT | |
| 3 | bussiness_version | TEXT | |
| 4 | minor_version | TEXT | |
| 5 | payment_date | DATE | |
| 6 | currency | TEXT | |
| 7 | rule_id | TEXT | |
| 8 | rule_uuid | TEXT | the reason to add this field is rule id will be changed when the rule updated by user. |
| 9 | stp_level | TEXT | for netting resultant cashflow 1. MakerChecker 2. CheckerOnly 3. FullStp |
| 10 | net_type | TEXT | 1. BilateralNetting 2. SwapAgentNetting 3. CcilNetting 4. BicNetting 5. ... |
| 11 | net_trigger_time | TIMESTAMP | |
| 12 | net_status | TEXT | 1. Waiting 2. Pending 3. Done 4. Disabled 5. Failed |
| 13 | net_group_key | TEXT | format: seperate by comon samples for cci netting as below: 400452428,2024-06-04,USD |
| 14 | failed_reason | TEXT | |
| 15 | version | INT | for optimistic locking |
| 16 | created_at | TIMESTAMP | |
| 17 | updated_at | TIMESTAMP | |

### 4.2.1. table(ratan_auto_netting_config)

| # | column | type | comments |
| --- | --- | --- | --- |
| 1 | id | Bigserial | PK |
| 2 | net_type | TEXT | 1. BilateralNetting 2. SwapAgentNetting 3. CcilNetting 4. BicNetting |
| 3 | net_group_key_config | TEXT | format: json group key including fields to grouped, samples as below: [ { "field": "entityFmid", "xpath": "" }, { "field": "valueDate", "xpath": "" }, { "field": "settlementCurrency", "xpath": "" } ] |
| 4 | resultant_mapping_config | TEXT | format: json samples as below, for ccil netting, couterparty of resultant cashflow will be filled to fixed value: { "counterpartyFmId": "400021949", "counterpartyFmCode": "CLEARING CORP*MMB", "settlementMethod": "Cash" } |
| 5 | description | TEXT | |
| 6 | created_at | TIMESTAMP | |
| 7 | updated_at | TIMESTAMP | |

### 4.2.2. Index

# 5. Performance

### 5.1 refresh cashflows after rule changed

| version | environment | service instances number | cashflows number | table row count | total time spent |
| --- | --- | --- | --- | --- | --- |
| old version | uat2 | 3 | 150,000 | | 5min |
| frmp1 | 3 | 53,000 | 12,562,217 | 65s-83s |
| staging | 6 | 25,612 | 39,500,554 | time out |
| new version | frmp1 | 3 | 54,382 | 12,803,124 | 14s-21s |
| staging | 4 | 25,617 | 39,516,462 | 50s-65s |
| production | 4 | 57,940 | 51,423754 | 30s-55s |

### 5.1 auto netting

| env | service instances number | optimization | volume | group count | call lifecycle for query details time | call lifecycle for update status time | total time | comment |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| fmrp1 | 3 | | 5k | 1 | 1min | 1min10s | 2min16s | ratanTraceId: 2752775a3c56b4e69698a50789f79c62 |
| fmrp1 | 3 | | 5k | 1 | 6s | 44s | 57s | ratanTraceId: 875b3c640d45d26898e9f48366ed6476 (before lifecycle optimiation) |
| fmrp1 | 3 | | 5k | 1 | 8s | 38s | 56s | ratanTraceId: 9cb28b7d9aa6622c3897d95a321318f5 |
| fmrp2 | 3 | | 5k | 1 | 10s | 25s | 43s | ratanTraceId: 41f979e27af48daff895a99e75393adc |
| fmrp2 | 3 | | 10k | 1 | 18s | 54s | 81s | ratanTraceId: d63933182697241766e3e7febfa97360 |
| staging | 6 | before | 5k | 1 | 24s | 1min | 1min52s | ratanTraceId: e58c8844c2a1416ab0232c6107325119 |
| staging | 6 | before | 10k | 1 | 25s | 2min43s | 3min30s | ratanTraceId: 6f05020c77c32fc5c22f54123d8c018f |
| staging | 6 | before | 10k | 2 | 47s | 2min22s | 3min35s | ratanTraceId: 90997fd1a41721f425f8d3db9b45c5f0 |
| staging | 6 | after | 5k | 1 | 26s | 56s | 1min46s | ratanTraceId: 91e513017e4e9b1dbe8ac06922a97e35 |
| staging | 6 | after | 10k | 1 | 41s | 1min31s | 3min | ratanTraceId: 5fe6b5254eee0023cae425fedfec2e18 |
| staging | 6 | after | 10k | 2 | 42s | 1min4s | 2min9s | ratanTraceId: 96183c80f34debfa639ab44c4e1ae5ce |

# 6. Test cases

| test case | description | expected |
| --- | --- | --- |
| case01 | single cashflow reinstate | also processing auto rule check and manual rule check |