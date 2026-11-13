# Background

Exceptions summarized in -> [NSTP Workflow - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/NSTP+Workflow)

Generation logic: [Multi Exceptions - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/Multi+Exceptions)

- Agreed to keep exceptions within Cashflow Blotter (It was discussed that the option to close exceptions should be removed in exception blotter, but it’s irrelevant since we will move the business exceptions into cashflow blotter itself)
- Requirement is to avoid any limitation in terms of max number of cashflows that can be loaded into the blotter (as netting clients have high volume)
- User confirmed that all exceptions need to be handled together
- Preferable to have the cashflow status distinguished between action required by maker vs checker
- Affirmation – can be at single level, separate exception must be triggered if value of cashflow is above USD 100 Mio
- New Exception required for checker if Netting client cashflows is moved from Gross to Net. Added to confluence page, but it is not applicable for China Day 1 as FX deals will be directly booked and settled in RAZOR (Settlement Method needs to be stamped at trade level as part of Day2)
- Gross client exception to be non-stp if unnetted. Same user cannot accept the exception if they did unnet. – Added to the confluence page
- Any cashflows with currency specific mandatory requirements like RUB can still be STP on back of confirmation match
- Above 100 Mio cashflows can STP if no other exceptions. It needs to be NSTP for ringfenced checker only if there was a settlements manual touch on it
- Confirmation manual touch will not be considered for Settlement NSTP
- Need ability to mark a cashflow as failed – to be raised as separate requirement.
- System to prevent regeneration of payment from the same cashflow if a payment was sent previously. Where resending of payment is required, it is handled manually via AMH.
- MT199/299 for recall of funds – not required to send as part of MT192/292 release, but require capability to send it on adhoc basis with pre-defined template to send to our Nostro Agent / Beneficiary Agent / Beneficiary
- Approval of exceptions across cashflows is not allowed as there is risk of inadvertent approval of multiple cashflows
- Auto identification of TPP beneficiary based on Beneficiary vs Counterparty information to be included for China Day 1
- Cover flag missing and mandatory CCY information will be SI input level validations instead of separate exception

# Operation model

1. User will see all the business exceptions in one go, which is in the cashflow details page
2. User will solve all the exceptions together as maker/checker 1. Maker will have only 1 action "Submit" 2. Checker will have 2 actions "Approve" and "Reject" 3. On rare case some of the exception might get solved failed, like 10 exceptions in total, 9 fixed by maker, 1 failed because of network issue 1. The maker fix will be partial 2. Cashflow still stuck in pending operator 3. Next time maker open, only 1 failed exception will exist and get fixed
3. On

# Process Flow

1. User will see all the business exceptions in one go, which is in the cashflow details page. SSI exception + Pending affirmation + Back value exception + NSTP exceptions.
2. User will solve all the exceptions together as maker/checker 1. Maker will have only 1 action "Submit" 2. Checker will have 2 actions "Approve" and "Reject"
3. Partial success capability to support edge case: 1. On very rare case some of the exception might get solved failed, like 10 exceptions in total, 9 fixed by maker, 1 failed because of network issue. It is not expected that user to input and solve the 9 successfully solved exceptions again, 1. Maker 1. The maker fix will be partial, 9 got fixed and 1 left to be handled 2. Cashflow still stuck in pending operator 3. Next time maker open, only 1 failed exception will exist and get fixed 2. Checker 1. d

# Process Flow

# Transactions

# Interfaces & Parameters

## Domain Service Request: CamundaApiResponse

This is used by Camunda and domain service on API calling

```java
public class CamundaApiRequest<T> implements Serializable, Cloneable {
    private static final long serialVersionUID = 1L;
    private String trackingId;
    private String message;
    private Map<String, Object> metadata;
    private List<?> metadataList = Lists.newArrayList();  //This is for Exception Information
```

Example :
CamundaApiResponse response = new CamundaApiResponse();
...List<CommonException> commonExceptionList = Lists.newArrayList();
...response.setMetadataList(commonExceptionList);

## Domain Service Response: CommonException

This is used by Camunda and domain service on API response, exception information to be returned for flowing in BPMN.

Request :  CamundaApiRequest

Response: CamundaApiRespose

if exception happen in  ssi stamping / nstp,  domain service should create exceptions list as below

```
public class CommonException {
    private String exceptionId;
    private CommonExceptionStatus commonExceptionStatus; // PENDING_OPERATOR  PENDING_VERIFICATION
}

public enum CommonExceptionStatus {
    PENDING_OPERATOR,
    PENDING_VERIFICATION,
    CLOSED
}
```

for example:

```java
List<CommonException> commonExceptionList = Lists.newArrayList();
CommonException e1 = new CommonException();
e1.setExceptionId("e001");
e1.setCommonExceptionStatus(CommonExceptionStatus.PENDING_VERIFICATION);
commonExceptionList.add(e1);
response.setMetadataList(commonExceptionList);
response.setCamundaResponseCode(CamundaResponseCode.SUCCESS);
return response;
```

## Domain Service Generated Exception

```
public class PlatformException {
    private String originalExceptionId;
    private String businessFlow;
    private String sourceSystem;
    private String exceptionCode;
    private RatanExceptionType exceptionType;
    private String description;
    private List<Action> actions;
    private Map<String, String> metaData;
    private String entityId;
    private int entityVersion;
    private String entityType;
    private String trackingId;
    private Instant exceptionTime;
    private String status; //Pending Operator/Pending Verification/Closed
} 
class Action {

    private String actionName;
    private String apiUrl;
    private String apiMethod;
    private String actionType;

}
enum RatanExceptionType {
    TECHNICAL,
    BUSINESS,
    TECHNICAL_VISIBLE;
}
```

## UI Parameters to trigger maker/checker request

It is the exception list, but with possible **requestBody** such as for SSI fix action, which is an extra attribute than the exception details queried from exception module

maker api url : /v1/camunda/task/{buisnessType}/maker

checker api url : /v1/camunda/task/{businessType}/checker

businessType:   nstpssi

request body as below:

method : POST

```
{
    "cashflowId": "009381505007",
    "businessVersion": "0",
    "cashflowVersion": "0",
    "minorVersion": "3",
    "action": "Submit",
    "exceptions": [
        {
            "id": "ratan-10007",
            "exceptionCode": "exception-code-001",
            "sourceSystem": "SSI Service",
            "exceptionType": "BUSINESS",
            "exceptionCategory": "MissingVostro",
            "businessFlow": "SETTLEMENT",
            "description": "Missing Vostro",
            "actions": [
                {
                    "actionName": "Submit",
                    "actionType": "Rest",
                    "apiUrl": "http://localhost:8991/ratan/camunda/cashflow/ssi/maker",
                    "apiMethod": "POST",
					"requestBody": "{BIC:xxx}"
                }
            ],
            "metaData": null,
            "entityId": "000012345678",
            "entityVersion": "0-0-2",
            "entityType": "Cashflow",
            "trackingId": "000012345678-001",
            "status": "Pending Operator"
        },
        {
            "id": "ratan-10007",
            "exceptionCode": "exception-code-001",
            "sourceSystem": "SSI Service",
            "exceptionType": "BUSINESS",
            "exceptionCategory": "MissingVostro",
            "businessFlow": "SETTLEMENT",
            "description": "Missing Vostro",
            "actions": [
                {
                    "actionName": "Submit",
                    "actionType": "Rest",
                    "apiUrl": "http://localhost:8991/ratan/camunda/cashflow/service2",
                    "apiMethod": "POST"
                }
            ],
            "metaData": null,
            "entityId": "000012345678",
            "entityVersion": "0-0-2",
            "entityType": "Cashflow",
            "trackingId": "000012345678-001",
            "status": "Pending Operator"
        }
    ]
}
```

Response:

| Http Code | Message | Reason |
| --- | --- | --- |
| 200 | Success | |
| 500 | Maker/Checker task can not be found | task has completed no such cashflowId and version |
| | Maker/Checker task still uncompleted | exceptions remain, not fully be fixed |
| | Fix exception failed during executing following api: xxxxx | execution fixing api error |
| | | |

## Camunda call domain service on exception fixing

### SCBML update:

```
call http://localhost:8991/ratan/ssi/maker, POST   API type: POST
Request parameter: CamundaApiRequest

{
    "trackingId":"xxxx",
    "message":"<SCBML1/>",
    "metadata":{
        "cashflowId":"009381505007",
        "businessVersion":"0",
        "cashflowVersion":"0",
        "minorVersion":"4",
        "exceptionId":"xxxxxx",
        "exceptionStatus":"Pending_Verification",
        "requestBody": "{xxxxxxxxxxxxxxxx}" //Nullable
    }
}

Response: CamundaApiResposne

{
    "trackingId":"xxxx",
    "camundaResponseCode":"SUCCESS",
    "description":"xxxxxx",
    "message":"<SCBML2/>",
    "metadata":{
        "cashflowId":"009381505007",
        "businessVersion":"0",
        "cashflowVersion":"0",
        "minorVersion":"5",
        "exceptionId":"xxxxxx",
        "exceptionStatus":"CLOSED"
    }
}
 
```

## Rule Service

| API name | API URL | API Type | API Method | Request Sample | Response Sample | Comments |
| --- | --- | --- | --- | --- | --- | --- |
| Add Rule | [http://10.198.199.160:8453/api/v1/r](http://10.198.199.160:8004/v1/rep/exceptions/byEntity)ule/add | Rest | POST | { "ruleType":"NETTING", "businessFlow":"string", "rule":"string", "reason":"string", "exceptionCode":"string", "exceptionCategory":"NSTP", "operationLevel":"CHECKER_ONLY" } | { "createdAt": "2023-03-16T06:41:06.072Z", "updatedAt": "2023-03-16T06:41:06.072Z", "createdBy": "string", "updatedBy": "string", "version": 0, "id": "string", "businessFlow": "SETTLEMENT", "ruleType": "NETTING", "rule": "string", "reason": "string", "exceptionCode": "string", "exceptionCategory": "NSTP", "status": "ADD_PENDING", "operationLevel": "CHECKER_ONLY" } | GUI |
| Confirm Adding Rule | [http://10.198.199.160:8453](http://10.198.199.160:8004/v1/rep/exceptions/byEntity)[/api](http://10.198.199.160:8004/v1/rep/exceptions/byEntity)/v1/rule/{ruleId}/add/confirm | Rest | PUT | | { "createdAt": "2023-03-16T06:45:38.448Z", "updatedAt": "2023-03-16T06:45:38.448Z", "createdBy": "string", "updatedBy": "string", "version": 0, "id": "string", "businessFlow": "SETTLEMENT", "ruleType": "NETTING", "rule": "string", "reason": "string", "exceptionCode": "string", "exceptionCategory": "NSTP", "status": "ADD_CONFIRMED", "operationLevel": "CHECKER_ONLY" } | GUI |
| Cancel Adding Rule | [http://10.198.199.160:8453](http://10.198.199.160:8004/v1/rep/exceptions/byEntity)[/api](http://10.198.199.160:8004/v1/rep/exceptions/byEntity)/v1/rule/{ruleId}/add/cancel | Rest | PUT | | { "createdAt": "2023-03-16T06:45:38.448Z", "updatedAt": "2023-03-16T06:45:38.448Z", "createdBy": "string", "updatedBy": "string", "version": 0, "id": "string", "businessFlow": "SETTLEMENT", "ruleType": "NETTING", "rule": "string", "reason": "string", "exceptionCode": "string", "exceptionCategory": "NSTP", "status": "ADD_CANCELLED", "operationLevel": "CHECKER_ONLY" } | GUI |
| Delete Rule | [http://10.198.199.160:8453](http://10.198.199.160:8004/v1/rep/exceptions/byEntity)[/api](http://10.198.199.160:8004/v1/rep/exceptions/byEntity)/v1/rule/{ruleId}/delete | Rest | PUT | | { "createdAt": "2023-03-16T06:45:38.448Z", "updatedAt": "2023-03-16T06:45:38.448Z", "createdBy": "string", "updatedBy": "string", "version": 0, "id": "string", "businessFlow": "SETTLEMENT", "ruleType": "NETTING", "rule": "string", "reason": "string", "exceptionCode": "string", "exceptionCategory": "NSTP", "status": "DEL_PENDING", "operationLevel": "CHECKER_ONLY" } | GUI |
| Confirm Deleting Rule | [http://10.198.199.160:8453](http://10.198.199.160:8004/v1/rep/exceptions/byEntity)[/api](http://10.198.199.160:8004/v1/rep/exceptions/byEntity)/v1/rule/{ruleId}/delete/confirm | Rest | PUT | | { "createdAt": "2023-03-16T06:45:38.448Z", "updatedAt": "2023-03-16T06:45:38.448Z", "createdBy": "string", "updatedBy": "string", "version": 0, "id": "string", "businessFlow": "SETTLEMENT", "ruleType": "NETTING", "rule": "string", "reason": "string", "exceptionCode": "string", "exceptionCategory": "NSTP", "status": "DEL_CONFIRMED", "operationLevel": "CHECKER_ONLY" } | GUI |
| Cancel Deleting Rule | [http://10.198.199.160:8453](http://10.198.199.160:8004/v1/rep/exceptions/byEntity)[/api](http://10.198.199.160:8004/v1/rep/exceptions/byEntity)/v1/rule/{ruleId}/delete/cancel | Rest | PUT | | { "createdAt": "2023-03-16T06:45:38.448Z", "updatedAt": "2023-03-16T06:45:38.448Z", "createdBy": "string", "updatedBy": "string", "version": 0, "id": "string", "businessFlow": "SETTLEMENT", "ruleType": "NETTING", "rule": "string", "reason": "string", "exceptionCode": "string", "exceptionCategory": "NSTP", "status": "ADD_CONFIRMED", "operationLevel": "CHECKER_ONLY" } | GUI |
| Rule Histories | [http://10.198.199.160:8453](http://10.198.199.160:8004/v1/rep/exceptions/byEntity)[/api](http://10.198.199.160:8004/v1/rep/exceptions/byEntity)/v1/rule/histories | Rest | POST | { "ruleId": "string", "ruleType": "NETTING", "ruleStatus": "ADD_PENDING", "startTime": "2023-03-16T07:13:19.595Z", "endTime": "2023-03-16T07:13:19.595Z" } | [ { "createdAt": "2023-03-16T07:13:19.609Z", "updatedAt": "2023-03-16T07:13:19.609Z", "createdBy": "string", "updatedBy": "string", "version": 0, "id": "string", "businessFlow": "SETTLEMENT", "ruleType": "NETTING", "rule": "string", "reason": "string", "exceptionCode": "string", "exceptionCategory": "NSTP", "status": "ADD_PENDING", "operationLevel": "CHECKER_ONLY", "ruleId": "string" } ] | GUI |
| Get Rules By Type | [http://10.198.199.160:8453](http://10.198.199.160:8004/v1/rep/exceptions/byEntity)[/api](http://10.198.199.160:8004/v1/rep/exceptions/byEntity)/v1/rule/{ruleType}/listByType | Rest | GET | | [ { "createdAt": "2023-03-10T03:10:26.986247", "updatedAt": "2023-03-10T03:12:36.896137", "createdBy": "ratanone-control-m", "updatedBy": "ratanone-control-m", "version": 1, "id": "1634028915853275136", "businessFlow": "SETTLEMENT", "ruleType": "NSTP", "rule": "", "reason": "Block CORP Client", "exceptionCode": "CORP Client", "exceptionCategory": "NSTP", "status": "ADD_CONFIRMED", "operationLevel": "CHECKER_ONLY" } ] | GUI |
| Get Special Rule List | [http://10.198.199.160:8453](http://10.198.199.160:8004/v1/rep/exceptions/byEntity)[/api](http://10.198.199.160:8004/v1/rep/exceptions/byEntity)/v1/nstpRule/SpecialConfig/{businessFlow} | Rest | GET | | [ { "id": 2, "businessFlow": "SETTLEMENT", "ruleType": "NSTP", "exceptionCode": "Back Value Date", "exceptionCategory": "BACK_VALUE" }, { "id": 1, "businessFlow": "SETTLEMENT", "ruleType": "NSTP", "exceptionCode": "GSAM Client", "exceptionCategory": "" } ] | GUI |
| Add Special Rule | [http://10.198.199.160:8453](http://10.198.199.160:8004/v1/rep/exceptions/byEntity)[/api](http://10.198.199.160:8004/v1/rep/exceptions/byEntity)/v1/nstpRule/addSpecial | Rest | POST | { "ruleConfigId": 1, "exceptionCategory": "NSTP", "operationLevel": "CHECKER_ONLY" } | { "createdAt": "2023-03-16T08:05:06.221Z", "updatedAt": "2023-03-16T08:05:06.221Z", "createdBy": "string", "updatedBy": "string", "version": 0, "id": "string", "businessFlow": "SETTLEMENT", "ruleType": "NETTING", "rule": "string", "reason": "string", "exceptionCode": "string", "exceptionCategory": "NSTP", "status": "ADD_PENDING", "operationLevel": "CHECKER_ONLY" } | GUI |
| NSTP Rule Check | [http://10.198.199.160:8453](http://10.198.199.160:8004/v1/rep/exceptions/byEntity)[/api](http://10.198.199.160:8004/v1/rep/exceptions/byEntity)/v1/nstpRule/check | Rest | POST | { "message": "scbml" } | { "trackingId": "string", "message": "string", "metadata": { "additionalProp1": {}, "additionalProp2": {}, "additionalProp3": {} }, "metadataList": [ {} ], "data": { "exceptionId": "string", "commonExceptionStatus": "PENDING_OPERATOR" }, "camundaResponseCode": "FILTERED", "description": "string" } | Camunda |
| Suppression Rule Check | [http://10.198.199.160:8453](http://10.198.199.160:8004/v1/rep/exceptions/byEntity)[/api](http://10.198.199.160:8004/v1/rep/exceptions/byEntity)/v1/suppressionRule/check | Rest | Post | { "message": "scbml" } | { "trackingId": "string", "message": "scbml", "metadata": { "additionalProp1": {}, "additionalProp2": {}, "additionalProp3": {} }, "metadataList": [ {} ], "camundaResponseCode": "FILTERED", "description": "Rule expression Entity.Counterparty_SCI_FMID==400799319 matched: expected value: 400799319, actual value: 400799319. \n;Rule expression Cashflow.Payment_Currency==USD matched: expected value: USD, actual value: USD. \n" } | |
| Exception Submit | [http://10.198.199.160:8453](http://10.198.199.160:8004/v1/rep/exceptions/byEntity)[/api](http://10.198.199.160:8004/v1/rep/exceptions/byEntity)/v1/nstpException/submit | Rest | POST | { "trackingId": "string", "message": "string", "metadata": { "additionalProp1": {}, "additionalProp2": {}, "additionalProp3": {} }, "metadataList": [ {} ], "data": {} } | { "trackingId": "string", "message": "string", "metadata":{ "cashflowId":"009381505007", "businessVersion":"0", "cashflowVersion":"0", "minorVersion":"4", "exceptionId":"xxxxxx", "exceptionStatus":"Pending_Operator", "requestBody": "{xxxxxxxxxxxxxxxx}" //Nullable } "metadataList": [ {} ], "data": { "exceptionId": "string", "commonExceptionStatus": "PENDING_VERIFICATION" }, "camundaResponseCode": "SUCCESS", "description": "string" } | Camunda |
| Exception Approve | [http://10.198.199.160:8453](http://10.198.199.160:8004/v1/rep/exceptions/byEntity)[/api](http://10.198.199.160:8004/v1/rep/exceptions/byEntity)/v1/nstpException/approve | Rest | POST | { "trackingId": "string", "message": "string", "metadata": { "additionalProp1": {}, "additionalProp2": {}, "additionalProp3": {} }, "metadataList": [ {} ], "data": {} } | { "trackingId": "string", "message": "string", "metadata":{ "cashflowId":"009381505007", "businessVersion":"0", "cashflowVersion":"0", "minorVersion":"4", "exceptionId":"xxxxxx", "exceptionStatus":"Pending_Verification", "requestBody": "{xxxxxxxxxxxxxxxx}" //Nullable } "metadataList": [ {} ], "data": { "exceptionId": "string", "commonExceptionStatus": "CLOSED" }, "camundaResponseCode": "SUCCESS", "description": "string" } | Camunda |
| Exception Reject | [http://10.198.199.160:8453](http://10.198.199.160:8004/v1/rep/exceptions/byEntity)[/api](http://10.198.199.160:8004/v1/rep/exceptions/byEntity)/v1/nstpException/reject | Rest | POST | { "trackingId": "string", "message": "string", "metadata": { "additionalProp1": {}, "additionalProp2": {}, "additionalProp3": {} }, "metadataList": [ {} ], "data": {} } | { "trackingId": "string", "message": "string", "metadata":{ "cashflowId":"009381505007", "businessVersion":"0", "cashflowVersion":"0", "minorVersion":"4", "exceptionId":"xxxxxx", "exceptionStatus":"Pending_Verification", "requestBody": "{xxxxxxxxxxxxxxxx}" //Nullable } "metadataList": [ {} ], "data": { "exceptionId": "string", "commonExceptionStatus": "PENDING_OPERATOR" }, "camundaResponseCode": "SUCCESS", "description": "string" } | Camunda |
| Query Exception Action Data | [http://10.198.199.160:8453](http://10.198.199.160:8004/v1/rep/exceptions/byEntity)[/api](http://10.198.199.160:8004/v1/rep/exceptions/byEntity)/v1/nstpException/actionData | Rest | GET | [http://10.198.199.160:8453](http://10.198.199.160:8004/v1/rep/exceptions/byEntity)[/api](http://10.198.199.160:8004/v1/rep/exceptions/byEntity)/v1/nstpException/actionData?exceptionId=1234567 | { "createdAt": "2023-03-16T08:55:41.562Z", "updatedAt": "2023-03-16T08:55:41.562Z", "createdBy": "string", "updatedBy": "string", "version": 0, "id": "string", "exceptionId": "string", "actionName": "string", "actionMetadata": "string", "status": "ACTIVE" } | GUI |
| Query Exception Meta Data | [http://10.198.199.160:8453](http://10.198.199.160:8004/v1/rep/exceptions/byEntity)[/api](http://10.198.199.160:8004/v1/rep/exceptions/byEntity)/v1/nstpException/metaData | Rest | GET | [http://10.198.199.160:8453](http://10.198.199.160:8004/v1/rep/exceptions/byEntity)[/api](http://10.198.199.160:8004/v1/rep/exceptions/byEntity)/v1/nstpException/metaData?exceptionId=1234567 | {"backvalue_date":"2023-03-13"} | GUI |
| | | | | | | |

## Exception platform

| API name | API URL | API Type | API Method | Request Sample | Response Sample |
| --- | --- | --- | --- | --- | --- |
| Exception list query | [http://10.198.199.160:8004/v1/rep/exceptions/byEntity](http://10.198.199.160:8004/v1/rep/exceptions/byEntity) | Rest | POST | { "entityId": "009381504326", "entityVersion": 0 } | [ { "id": "1626132595465424896", "exceptionCode": "RATAN-200400001", "businessFlow": "SETTLEMENT", "sourceSystem": "RULE-SERVICE", "exceptionType": "BUSINESS", "exceptionCategory": null, "description": "Rule [Cashflow.Cashflow_Id==009381504326] matched, expectedRuleValue is '009381504326' ,realRuleValue value is '009381504326'.", "actions": [], "metaData": null, "entityId": "009381504326", "entityVersion": 0, "entityType": "CASHFLOW", "trackingId": "1626132450021695488", "exceptionTime": "2023-02-16T16:12:42.244127", "status": "CLOSED" }, { "id": "1626132596815990784", "exceptionCode": "RATAN-200400001", "businessFlow": "SETTLEMENT", "sourceSystem": "RULE-SERVICE", "exceptionType": "BUSINESS", "exceptionCategory": null, "description": "Rule [Cashflow.Cashflow_Business_Version==0] matched, expectedRuleValue is '0' ,realRuleValue value is '0'.", "actions": [ { "actionName": "makerFix", "actionType": null, "apiUrl": "[http://10.198.199.160:8868/api/v1/nstpException/fix?exceptionId=1626132452982874112](http://10.198.199.160:8868/api/v1/nstpException/fix?exceptionId=1626132452982874112)", "apiMethod": "POST", "componentName": null, "componentUrl": null } ], "metaData": null, "entityId": "009381504326", "entityVersion": 0, "entityType": "CASHFLOW", "trackingId": "1626132455524622336", "exceptionTime": "2023-02-16T16:12:43.558508", "status": "PENDING_OPERATOR" }, { "id": "1626404209260138496", "exceptionCode": "RATAN-200400001", "businessFlow": "SETTLEMENT", "sourceSystem": "RULE-SERVICE", "exceptionType": "BUSINESS", "exceptionCategory": null, "description": "Rule [Cashflow.Cashflow_Affirmation_Status==Unaffirmed] matched, expectedRuleValue is 'Unaffirmed' ,realRuleValue value is 'Unaffirmed'.", "actions": [ { "actionName": "checkerApprove", "actionType": null, "apiUrl": "[http://10.198.199.160:8453/api/v1/nstpException/approve?exceptionId=1626404208849129472](http://10.198.199.160:8453/api/v1/nstpException/approve?exceptionId=1626404208849129472)", "apiMethod": "POST", "componentName": null, "componentUrl": null } ], "metaData": null, "entityId": "009381504326", "entityVersion": 0, "entityType": "CASHFLOW", "trackingId": "1626404208941404160", "exceptionTime": "2023-02-17T02:12:35.184826", "status": "PENDING_VERIFICATION" } ] |

# Database Tables

**exception**:

| Column | Type | Nullable | Sample | Unique |
| --- | --- | --- | --- | --- |
| exception_id | Text | Mandatory | 1 | Yes |
| cashflow__cashflow_id | Text | Mandatory | 003690235910 | |
| cashflow__cashflow_business_version | Text | Mandatory | 0 | |
| cashflow__cashflow_version | Text | Mandatory | 0 | |
| cashflow__cashflow_minor_version | Text | Nullable | 2 | |
| status | Text | Mandatory | Pending_Operator Pending_Verification | |
| reason | Jsonb | Nullable | | |
| ratan_label | Text | Nullable | | |
| created_at | Timestamp | Mandatory | | |
| updated_at | Timestamp | Mandatory | | |

**rules**:

| Column | Type | Nullable | Sample |
| --- | --- | --- | --- |
| ... | | | |
| exception_code | Text | Mandatory | Unaffirmed Cashflow |
| operation_level | Number | Mandatory | 1(Checker only) 2 (M/C) 3 (Maker only) |

# Cases

## Happy case

Cashflow lifecycle service: cashflow

| Cashflow Id | Business Version | Cashflow Version | Minor Version | Status | Sub Status | Status Type |
| --- | --- | --- | --- | --- | --- | --- |
| C01 | 0 | 0 | 0 | PROJECTED | NA | NA |
| C01 | 0 | 0 | 1 | QUEUED | NA | NA |
| C01 | 0 | 0 | 2 | WAITING | Pending_Operator | Pending Exception |
| | | | | | | |

Camunda: User_Action

| Id | Status | Type | Instance Id | Cashflow Id | Business Version | Cashflow Version | Minor Version |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 01 | INIT | Maker | 000000001 | C01 | 0 | 0 | 2 |

Camunda: Exception_Summary

| Id | Instance Id | Total Exception | Pending Operator | Pending Verification |
| --- | --- | --- | --- | --- |
| 01 | 000000001 | 5 | 4 | 1 |

Exception module: exception

| Id | Code | Status | Reason | Cashflow Id | Business Version | Cashflow Version | Minor Version |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 01 | E0001 | Pending_Operator | Missing Vostro + Missing Nostro | C01 | 0 | 0 | 2 |
| 02 | E0002 | Pending_Operator | Unaffirmed cashflow | C01 | 0 | 0 | 2 |
| 03 | E0003 | Pending_Operator | Netting resultant cashflow | C01 | 0 | 0 | 2 |
| 04 | E0004 | Pending_Operator | GSAM client | C01 | 0 | 0 | 2 |
| 05 | E0005 | Pending_Verification | Bad Business Day | C01 | 0 | 0 | 2 |

## Maker fixed:

Cashflow lifecycle service: cashflow

| Cashflow Id | Business Version | Cashflow Version | Minor Version | Status | Sub Status | Status Type |
| --- | --- | --- | --- | --- | --- | --- |
| C01 | 0 | 0 | 3 | WAITING | Pending_Verification | Pending Exception |

Cashflow lifecycle service: cashflow

| Id | Status | Type | Instance Id | Cashflow Id | Business Version | Cashflow Version | Minor Version |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 01 | CLOSED | Maker | 000000001 | C01 | 0 | 0 | 2 |
| 02 | INIT | Checker | 000000001 | C01 | 0 | 0 | 3 |

Camunda: Exception_Summary

| Id | Instance Id | Total Exception | Pending Operator | Pending Verification |
| --- | --- | --- | --- | --- |
| 01 | 000000001 | 5 | 0 | 5 |

Exception module: exception

| Id | Code | Status | Reason | Cashflow Id | Business Version | Cashflow Version | Minor Version |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 01 | E0001 | Pending_Verification | Missing Vostro + Missing Nostro | C01 | 0 | 0 | 3 |
| 02 | E0002 | Pending_Verification | Unaffirmed cashflow | C01 | 0 | 0 | 3 |
| 03 | E0003 | Pending_Verification | Netting resultant cashflow | C01 | 0 | 0 | 3 |
| 04 | E0004 | Pending_Verification | GSAM client | C01 | 0 | 0 | 3 |
| 05 | E0005 | Pending_Verification | Bad Business Day | C01 | 0 | 0 | 3 |

## Checker fixed:

Cashflow lifecycle service: cashflow

| Cashflow Id | Business Version | Cashflow Version | Minor Version | Status | Sub Status | Status Type | Comment |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C01 | 0 | 0 | 4 | WAITING | Pending_Verification | NA | SSI stamped |
| C01 | 0 | 0 | 5 | WAITING | Pending_Verification | NA | PaymentDateUpdate |
| C01 | 0 | 0 | 6 | WAITING | Pending_Verification | NA | ManualAffirm |
| C01 | 0 | 0 | 7 | READY | NA | NA | |
| C01 | 0 | 0 | 8 | RELEASED | NA | NA | |
| C01 | 0 | 0 | 9 | SETTLED | NA | NA | |

Camunda: User_Action

| Id | Status | Type | Instance Id | Cashflow Id | Business Version | Cashflow Version | Minor Version |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 01 | CLOSED | Maker | 000000001 | C01 | 0 | 0 | 2 |
| 02 | CLOSED | Checker | 000000001 | C01 | 0 | 0 | 7 |

Camunda: Exception_Summary

| Id | Instance Id | Total Exception | Pending Operator | Pending Verification |
| --- | --- | --- | --- | --- |
| 01 | 000000001 | 5 | 0 | 0 |

Exception module: exception

| Id | Code | Status | Reason | Cashflow Id | Business Version | Cashflow Version | Minor Version |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 01 | E0001 | CLOSED | Missing Vostro | C01 | 0 | 0 | 4 |
| 02 | E0002 | CLOSED | Unaffirmed cashflow | C01 | 0 | 0 | 5 |
| 03 | E0003 | CLOSED | Netting resultant cashflow | C01 | 0 | 0 | 6 |
| 04 | E0004 | CLOSED | GSAM client | C01 | 0 | 0 | 3 |
| 05 | E0005 | CLOSED | Bad Business Day | C01 | 0 | 0 | 3 |

## Checker reject SSI:

Cashflow lifecycle service: cashflow

| Cashflow Id | Business Version | Cashflow Version | Minor Version | Status | Sub Status | Status Type | Comment |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C01 | 0 | 0 | 0 | PROJECTED | NA | NA | |
| C01 | 0 | 0 | 1 | QUEUED | NA | NA | |
| C01 | 0 | 0 | 2 | WAITING | Pending_Operator | Pending Exception | |
| C01 | 0 | 0 | 3 | WAITING | Pending_Verification | Pending Exception | Maker fix |
| C01 | 0 | 0 | 4 | WAITING | Pending_Operator | Pending Exception | Checker reject SSI |
| | | | | | | | |
| | | | | | | | |

Camunda: User_Action

| Id | Status | Type | Instance Id | Cashflow Id | Business Version | Cashflow Version | Minor Version |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 01 | CLOSED | Maker | 000000001 | C01 | 0 | 0 | 2 |
| 02 | CLOSED | Checker | 000000001 | C01 | 0 | 0 | 3 |
| 03 | INIT | Maker | 000000001 | C01 | 0 | 0 | 4 |

Camunda: Exception_Summary

| Id | Instance Id | Total Exception | Pending Operator | Pending Verification |
| --- | --- | --- | --- | --- |
| 01 | 000000001 | 5 | 1 | 3 |

Exception module: exception

| Id | Code | Status | Reason | Cashflow Id | Business Version | Cashflow Version | Minor Version |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 01 | E0001 | Pending_Operator → Pending_Verification→ Pending_Operator | Missing Vostro + Missing Nostro | C01 | 0 | 0 | 4 |
| 02 | E0002 | Pending_Operator → Closed | Unaffirmed cashflow | C01 | 0 | 0 | 4 |
| 03 | E0003 | Pending_Operator → Pending_Verification | Netting resultant cashflow | C01 | 0 | 0 | 4 |
| 04 | E0004 | Pending_Operator → Pending_Verification | GSAM client | C01 | 0 | 0 | 4 |
| 05 | E0005 | Pending_Operator → Pending_Verification | Bad Business Day | C01 | 0 | 0 | 4 |

## Adhoc SSI

### Good stamping and Adhoc SSI made by maker when Pending Operator

**Dummy exception only get generated on good stamping: **

1. **No SSI exception at all**
2. **Only secondary SSI or Not match**

Cashflow lifecycle service: cashflow

| Cashflow Id | Business Version | Cashflow Version | Minor Version | Status | Sub Status | Status Type | Comment |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C01 | 0 | 0 | 0 | PROJECTED | NA | NA | |
| C01 | 0 | 0 | 1 | QUEUED | NA | NA | |
| C01 | 0 | 0 | 2 | WAITING | Pending_Operator | Pending Exception | |
| C01 | 0 | 0 | 3 | WAITING | Pending_Verification | Pending Exception | Maker adhoc add SSI |
| C01 | 0 | 0 | 4 | READY | NA | NA | Checker approve |

Exception module: exception

| Id | Code | Status | Reason | Cashflow Id | Business Version | Cashflow Version | Minor Version | Actions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 01 | E0001 | Closed (2)→ Pending_Verification (3)→ Closed (4) | Adhoc SSI | C01 | 0 | 0 | 2 | **Submit **+ Reject (2) → **Approve **+ Reject (3)→ Submit + Reject (4) |
| 02 | E0002 | Pending_Operator (2)→ Closed (3) | Unaffirmed cashflow | C01 | 0 | 0 | 2 | **Sumbit (2)**→ Empty (3) |

### Good stamping and Checker reject when Pending Verification

Cashflow lifecycle service: cashflow

| Cashflow Id | Business Version | Cashflow Version | Minor Version | Status | Sub Status | Status Type | Comment |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C01 | 0 | 0 | 0 | PROJECTED | NA | NA | |
| C01 | 0 | 0 | 1 | QUEUED | NA | NA | |
| C01 | 0 | 0 | 2 | WAITING | Pending_Operator | Pending Exception | |
| C01 | 0 | 0 | 3 | WAITING | Pending_Verification | Pending Exception | Maker approve without adhoc SSI |
| C01 | 0 | 0 | 4 | WAITING | Pending_Operator | Pending Exception | Checker reject the SSI |
| C01 | 0 | 0 | 5 | WAITING | Pending_Verification | Pending Exception | Maker adhoc add SSI |
| C01 | 0 | 0 | 6 | READY | NA | NA | Checker approve |

Exception module: exception

| Id | Code | Status | Reason | Cashflow Id | Actions |
| --- | --- | --- | --- | --- | --- |
| 01 | E0001 | Closed (2)→ Closed (3)→ Pending_Operator (4)→ Pending_Verification (5)→ Closed (6) | Adhoc SSI | C01 | Submit + Reject (2) → Submit+ **Reject **(3)→ **Submit **(4)→ **Approve **+ Reject (5)→ Submit + Reject (6) |
| 02 | E0002 | Pending_Operator (2)→ Closed(3) | Unaffirmed cashflow | C01 | **Sumbit** (2)→ Empty (3) |
| 03 | E0003 | Pending_Verification (2)→Pending_Verification (3)→ Closed (4) | Secondary SSI | | Approve+ Reject (2)→ Approve + **Reject **(3) → Empty (4) |

### Good stamping and Adhoc SSI made by maker when READY

Cashflow lifecycle service: cashflow

| Cashflow Id | Business Version | Cashflow Version | Minor Version | Status | Sub Status | Status Type | Comment |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C01 | 0 | 0 | 0 | PROJECTED | NA | NA | |
| C01 | 0 | 0 | 1 | QUEUED | NA | NA | |
| C01 | 0 | 0 | 2 | WAITING | Pending_Operator | Pending Exception | |
| C01 | 0 | 0 | 3 | WAITING | Pending_Verification | Pending Exception | Maker approve without adhoc SSI |
| C01 | 0 | 0 | 4 | READY | NA | NA | Checker approve |
| C01 | 0 | 0 | 5 | WAITING | Pending_Verification | Pending Exception | Maker add adhoc SSI |
| C01 | 0 | 0 | 6 | READY | NA | NA | Checker approve |

Exception module: exception

| Id | Code | Status | Reason | Cashflow Id | Actions |
| --- | --- | --- | --- | --- | --- |
| 01 | E0001 | Pending_Operator (2)→ Pending_Verification (3)→ Closed (4) | Multiple SSI | C01 | **Submit **(2) → **Approve**+ Reject (3)→ Empty (4) |
| 02 | E0002 | Closed (4)→ Pending_Verification (5)→ Closed (6) | Adhoc SSI | C01 | **Submit **+ Reject (4)→ **Approve **+ Reject (5)→ Submit + Reject (6) |

### Change point

1. SSI service: 1. Generate below exception when Good Stamping (No SSI exception at all, or only Secondary SSI exception) 1. Status: Closed 2. Exception Code: Adhoc SSI 3. Exception Category: SSI 4. Actions: 1. Submit (For maker to trigger an adhoc SSI) 2. Reject (For checker to reject and trigger) 2. When a.Submit triggered, exception updated to below, and it will be a normal case for SI exception handling to checker: 1. Status: Pending Verification 2. Exception Code: Adhoc SSI 3. Exception Category: SSI 4. Actions: 1. Approve 2. Reject 3. When a.Reject triggered, exception updated to below, and it will be a normal case for SI exception handling starting from maker: 1. Status: Pending Operator 2. Exception Code: Adhoc SSI 3. Exception Category: SSI 4. Actions: 1. Submit
2. UI, minor change: 1. Enable Edit button on SI block when the 1. dummy Exception exists: Exception Code=Adhoc SSI and Exception Category=SSI and Status=Closed 2. Status is WAITING + Pending Operator OR READY 2. Attach the body to the exception like other SI exception handling on the dummy exception
3. Orchestration service, minor change: 1. Remove the exception number validation and call the action API if a closed exception has the action
4. Exception service, minor change: 1. make the exception creation/update as a sync API call

## Open questions:

1. Adhoc SSI maker when pending multiple exception

# SSI Service Migration Assessment

| **Service** | **Change point** | **Estimation** |
| --- | --- | --- |
| Strategic Query Service Exception platform | 1. Support graphql query only on Exception list by 2. Data entitlement (for EG, BCS, CN) | 4 |
| Strategic SSI Stamping Service | 1. Support to differentiate BCS and CN cashflows 2. Close exceptions on stamping request 3. Trade stamping migration | 16 |
| Cashflow Service | 1. status machine 2. fmcode stamping in advance 3. close exception by calling ssi service when new version cashflow comes in 4. API to provide cashflow status on impacted cashflow query | 16 |
| BAU Exception Blotter | 1. Client data query from Strategic Query Service 2. Inherit from CN on the SSI exception form 3. [Future] Going forward to query other exception here as well | 8 |
| BAU camunda | 1. Exception close to call stamping service 2. Stamp FMCODE before calling SSI ??? Generate interface exception on query failure 3. Give up exception publishing | 8 |
| Test + BUg fix | | 8 |