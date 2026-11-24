#

# Requirement

During the last meeting , below was the proposal for RATAN Indonesia rule maintenance .  The call to discuss on feasibility/agreement on the below requirement

~~**<u>Global rule </u>**~~

1. Current UI’s to be enhances with option (like Checkbox) to publish a copy of the rule to RATAN Indonesia instance .
2. When user selects the checkbox while creating Rule , then copy of the rule should be published to RATAN Indonesia instance.
3. In case of any amendment/deletion of the specific rule , the necessary amendment/deletion should feed to RATAN Indonesia instance . PS : The option (like checkbox) in UI should be Locked / Greyed out during amendment/deletion of rule.
4. Maker / Checker should be required to rule addition/amendment/deletion on UI .

**<u>Indonesia market rule</u>**

1. User will directly input RATAN Indonesia instance
2. All Manual input of static data / rule directly in RATAN Indonesia should go via maker/check control.

# Function Scope

![image-2026-8-14_10-55-18.png](attachments/image-2026-8-14_10-55-18.png)

In technical kickoff meeting, we analyzed the rule sync scope.

1. All existing rules related to ID will be initialized to DB when environment setup.
2. Increment rules in functions 1~5 which tagged **RED **in GUI snapshot will be automatically sync to ID instance when they are created as **'Global'** which meet the condition: 1. ** business flow=STRATEGIC_SETTLEMENT** 2. ** rule type in （"NSTP", "SUPPRESSION", "SWIFT_SUPPRESSION", "NETTING", "AUTO_NETTING"）**

This design focus on the 'Global' rule automatic synchronization from RATAN GDC to RATAN ID.

# ~~Global Rule & ID Specific Rule~~

Global & ID rule related to Entity__Booking_Entity_SCI_FMID and Entity__Booking_Entity_SCI_FMCODE now. Both of them  identified automatically by FE & Rule server base on user input.

- Global rule - When rule expression does not contain Entity__Booking_Entity_SCI_FMID and Entity__Booking_Entity_SCI_FMCODE, it will be tagged Global rule. - Global rule can not be updated to Non Global rule when user update it in GUI. (Because the rule will be in DEAD status and will be hidden in GUI, and the revoke sync status can not be handled properly) - Forbid input ID's Entity__Booking_Entity_SCI_FMID and Entity__Booking_Entity_SCI_FMCODE in GDC GUI. - Global rule is read-only on ID side. - Global rule sync status should be returned to user and support manual resync by user.
- ID Rule - Rule expression will contains ID's Entity__Booking_Entity_SCI_FMID and Entity__Booking_Entity_SCI_FMCODE by default and greyed to forbid update.

# Rule Service

## Proposal A(data copy)

Proposal A is data transfer way for Global rule copy from RATAN GDC to RATAN ID.

The implement is in rule service itself and use a global configuration to identify GDC(data producer) and ID( data consumer).

We use FM solace as connection middleware between RATAN GDC and RATAN ID instead of API call.

### Design Key Points

1. Follow unidirectional mode(RATAN GDC→ RATAN ID).
2. Data transaction.
3. Transport no loss, no repeat, no disorder.
4. Support multi consumers in one sync event.
5. Implement in separate package for low coupling.

### Design Diagram

This diagram uses Indonesia represent XDC for an example.

### Rule Synchronizer

- Each rule has **only one** sync record to record the **newest **sync event in Producer side.
- Every sync event for one rule will bring a unique request_id and bring all its parents latest rule histories(would be the DEAD one for each parent).
- Retry sync event will **reuse **the **request_id **and override the previous sync content.
- Sync status are SENT ACK NACK FAILED TIMEOUT IGNORE for each downstream DC

SENT: Data produced successfully by Producer.

FAILED:  Data produced failed by Producer.

ACK:  Data consumed successfully by Consumer.

NACK: Data consumed failed by Consumer.

TIMEOUT: No response received in 5 minutes.

IGNORE:  When rule update event happen, will mark its parents rule's sync event status as IGNORE to avoid unnecessary failed retry in producer side.

- Sync message disorder handle

Use rule version and rule history to handle message disorder.

- Sync response with wrong request_id will be **ignore**.

### Resync Automatically In Producer Side

There is a SyncFailedRetryer in data producer to resync the records with  FAILED and TIMEOUT status and set status to SENT.

### Resync Manually In Producer Side

Sync Data Definition

- Confirm event without parent rule(rule creation)

```
REQ:
	{
		"id": 1, 
		"ruleId": "7469639288002646016", 
		"requestId": "5b02926e-e83c-4936-b7a8-28c2f17231f9", 
		"dc": "GLOBAL", 
		"currentRuleEngine": {
		  "id" : "7469639288002646016",
		  "businessFlow" : "STRATEGIC_SETTLEMENT",
		  "ruleType" : "NSTP",
		  "userRule" : "Trade_Id == \"4\"",
		  "runningRule" : "xxx",
		  "status" : "LIVE",
		  "reason" : "test",
		  "comment" : "2",
		  "needDryRun" : false,
		  "referenceRuleId" : null,
		  "createdAt" : "2026-06-21T23:28:44.915Z",
		  "updatedAt" : "2026-06-21T23:33:47.629Z",
		  "createdBy" : "1492285",
		  "updatedBy" : "1434424",
		  "version" : 2,
		  "metaData" : "xxx"
		},
		"parentRuleEngineLatestHistories": []
	}

RESP:
	{
		"id": 1,
		"ruleId": "7469639288002646016",
		"requestId": "5b02926e-e83c-4936-b7a8-28c2f17231f9",
		"dc": "ID",
		"message": "",
		"status": "ACK"
	}
	OR
	{
		"id": 1,
		"ruleId": "7469639288002646016",
		"requestId": "5b02926e-e83c-4936-b7a8-28c2f17231f9",
		"dc": "ID",
		"message": "xxx",
		"status": "NACK"
	}
```

- Confirm rule with parent rule(rule update)

```
REQ:
	{
		"id": 2, 
		"ruleId": "7469675703558148096", 
		"requestId": "5b02926e-e83c-4936-b7a8-28c2f17231fa", 
		"dc": "GLOBAL", 
		"currentRuleEngine": {
			"id" : "7469675703558148096",
			"businessFlow" : "STRATEGIC_SETTLEMENT",
			"ruleType" : "NSTP",
			"userRule" : "Trade_Id == \"4\"",
			"runningRule" : "xxx",
			"status" : "LIVE",
			"reason" : "test",
			"comment" : "2",
			"needDryRun" : false,
			"referenceRuleId" : "7469639288002646016",
			"createdAt" : "2026-06-21T23:28:44.915Z",
			"updatedAt" : "2026-06-21T23:33:47.629Z",
			"createdBy" : "1492285",
			"updatedBy" : "1434424",
			"version" : 2,
			"metaData" : "xxx"

		}
		"parent_rule_engine_latest_histories": [{
		  "id" : "7469639288002646016",
		  "businessFlow" : "STRATEGIC_SETTLEMENT",
		  "ruleType" : "NSTP",
		  "userRule" : "Trade_Id == \"4\"",
		  "runningRule" : "xxx",
		  "status" : "DEAD",
		  "reason" : "test",
		  "comment" : "2",
		  "needDryRun" : false,
		  "referenceRuleId" : null,
		  "createdAt" : "2026-06-21T23:28:44.915Z",
		  "updatedAt" : "2026-06-21T23:33:47.629Z",
		  "createdBy" : "1492285",
		  "updatedBy" : "1434424",
		  "version" : 6,
		  "metaData" : "xxx"
		}]
	}

RESP:
	{
		"id": 2,
		"ruleId": "7469675703558148096",
		"requestId": "5b02926e-e83c-4936-b7a8-28c2f17231fa",
		"dc": "ID",
		"message": "",
		"status": "ACK"
	}
	OR
	{
		"id": 2,
		"ruleId": "7469675703558148096",
		"requestId": "5b02926e-e83c-4936-b7a8-28c2f17231fa",
		"dc": "ID",
		"message": "xxx",
		"status": "NACK"
	}
```

- Disable/Enable rule(rule control)

```
REQ:
	{
		"id": 3, 
		"rule_id": "7469675703558148096", 
		"request_id": "5b02926e-e83c-4936-b7a8-28c2f17231f0", 
		"dc": "GLOBAL", 
		"current_rule_engine": {
			"id" : "7469675703558148096",
			"businessFlow" : "STRATEGIC_SETTLEMENT",
			"ruleType" : "NSTP",
			"userRule" : "Trade_Id == \"4\"",
			"runningRule" : "xxx",
			"status" : "DISABLE",
			"reason" : "test",
			"comment" : "2",
			"needDryRun" : false,
			"referenceRuleId" : "7469639288002646016",
			"createdAt" : "2026-06-21T23:28:44.915Z",
			"updatedAt" : "2026-06-21T23:33:47.629Z",
			"createdBy" : "1492285",
			"updatedBy" : "1434424",
			"version" : 3,
			"metaData" : "xxx"

		}
		"parent_rule_engine_latest_histories": [{
		  "id" : "7469639288002646016",
		  "businessFlow" : "STRATEGIC_SETTLEMENT",
		  "ruleType" : "NSTP",
		  "userRule" : "Trade_Id == \"4\"",
		  "runningRule" : "xxx",
		  "status" : "DEAD",
		  "reason" : "test",
		  "comment" : "2",
		  "needDryRun" : false,
		  "referenceRuleId" : null,
		  "createdAt" : "2026-06-21T23:28:44.915Z",
		  "updatedAt" : "2026-06-21T23:33:47.629Z",
		  "createdBy" : "1492285",
		  "updatedBy" : "1434424",
		  "version" : 6,
		  "metaData" : "xxx"
		}]
	}

RESP:
	{
		"id": 3,
		"ruleId": "7469675703558148096",
		"requestId": "5b02926e-e83c-4936-b7a8-28c2f17231fa",
		"dc": "ID",
		"message": "",
		"status": "ACK"
	}
	OR
	{
		"id": 2,
		"ruleId": "7469675703558148096",
		"requestId": "5b02926e-e83c-4936-b7a8-28c2f17231fa",
		"dc": "ID",
		"message": "xxx",
		"status": "NACK"
	}
```

- Resync for special DC

```
{
    "id": 3, 
    "ruleId": "7469675703558148096", 
    "requestd": "5b02926e-e83c-4936-b7a8-28c2f17231fa", 
    "dc": "ID", 
    "currentRuleEngine": {
		"id" : "7469675703558148096",
		"businessFlow" : "STRATEGIC_SETTLEMENT",
		"ruleType" : "NSTP",
		"userRule" : "Trade_Id == \"4\"",
		"runningRule" : "xxx",
		"status" : "LIVE",
		"reason" : "test",
		"comment" : "2",
		"needDryRun" : false,
		"referenceRuleId" : "7469639288002646016",
		"createdAt" : "2026-06-21T23:28:44.915Z",
		"updatedAt" : "2026-06-21T23:33:47.629Z",
		"createdBy" : "1492285",
		"updatedBy" : "1434424",
		"version" : 2,
		"metaData" : "xxx"

	}
    "parentRuleEngineLatestHistories": [{
	  "id" : "7469639288002646016",
 	  "businessFlow" : "STRATEGIC_SETTLEMENT",
 	  "ruleType" : "NSTP",
 	  "userRule" : "Trade_Id == \"4\"",
 	  "runningRule" : "xxx",
 	  "status" : "DEAD",
 	  "reason" : "test",
 	  "comment" : "2",
 	  "needDryRun" : false,
 	  "referenceRuleId" : null,
 	  "createdAt" : "2026-06-21T23:28:44.915Z",
 	  "updatedAt" : "2026-06-21T23:33:47.629Z",
 	  "createdBy" : "1492285",
 	  "updatedBy" : "1434424",
 	  "version" : 6,
 	  "metaData" : "xxx"
	}]
}
```

### Table

- ratan_rule_engine_sync

| Filed | Data Type | Not Null | Unique | Description | Primary |
| --- | --- | --- | --- | --- | --- |
| id | bigserial | Y | | | Y |
| rule_id | text | Y | Y | | |
| rule_version | int | Y | | | |
| sync_content | text | Y | | {} | |
| sync_status | text | Y | | [ { "dc": "ID", "request_id": "", "status": "ACK" }, { “dc”: "TL" "request_id": "", "status": "NACK", } ] // status set: ACK, NACK, SENT, FAILED, TIMEOUT | |
| all_sync_done | bool | Y | | true/false | |
| create_at | timestamp | Y | | | |
| update_at | timestamp | Y | | | |

### Rest API(For FE)

- (NEW) POST /api/ratan/v1/rule-sync/{ruleId}/resend

REQ:

["ID"]

RESP:

{
          "ruleId": "7480861795379347456",
          "message": "SENT" // FAILED
        }

- (EXISTING) GET /api/idns/ratan/v2/rules/filter

RESP:

{
  "id": "7480861795379347456",
  "businessFlow": "STRATEGIC_SETTLEMENT",
  "ruleType": "NSTP",
  "runningRule": "import com.scb.ratan.rule.drools.model.MatchedRule;\nimport com.scb.ratan.rule.drools.model.fact.EnhancedFact;\nimport java.time.*;\n\nimport static com.scb.ratan.rule.utils.CustomFunctionUtils.*;\n\ndialect \"java\"\n\nglobal java.util.List matchedRuleSet;\n\nrule \"7480861795379347456-0\"\n    when\n        EnhancedFact( BCS_Trade_Id == \"-1\" )\n    then\n        MatchedRule matchedRule = new MatchedRule();\n        matchedRule.setRuleId(\"7480861795379347456-0\");\n        matchedRule.setReason(\"BCS_Trade_Id == \\\"-1\\\"\");\n        matchedRuleSet.add(matchedRule);\nend\n",
  "status": "LIVE",
  "reason": "-2",
  "metaData": "{\"exceptions\":[{\"exceptionCode\":\"1\",\"operationLevel\":\"MAKER_CHECKER\",\"exceptionCategory\":\"NSTP\",\"bulkEligible\":false}]}",
  "needDryRun": false,
  "version": 2,
  "createdAt": "2026-07-09T02:45:15.004823Z",
  "updatedAt": "2026-07-09T02:51:58.509726Z",
  "createdBy": "1434424",
  "updatedBy": "1414551745409443831",
  "rule": "BCS_Trade_Id == \"-2\"",
  "ruleId": "7480861795379347456",
  "sync": true,

"syncStatus": [

{

“dc”:  "ID",

"status":  “ACK”,  // SENT, ACK, NACK, FAILED, TIMEOUT

"message": ""

}

]
}

### Change Scope

ratanone-rule-service

### GUI DEMO

[Session-19: Rule Sync From Ratan GDC to Ratan ID - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/Session-19%3A+Rule+Sync+From+Ratan+GDC+to+Ratan+ID)

## Proposal B(data share)

Proposal B is a data share way for global rule shared by Ratan GDC and Ratan ID

# Question

1. What if user create/update/delete rule with multiple entity fmid or non Indonesia entity fmid and ticked copy bottion? 1. identified automatically rather than manually.
2. What should be displayed in UI if copy error ? Only status or need error message? 1. both status and message will return back to user.

# Appendix