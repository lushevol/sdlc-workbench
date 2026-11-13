| Target Release | |
| --- | --- |
| Epic | [RATAN-15255](https://jira.global.standardchartered.com/browse/RATAN-15255) |
| Document Status | |
| Document Owner | |
| Designer | @Lin Liang |
| Developers | @Lin Liang |
| QA | |

# 1. Background

Rule engine is regarded as a sophisticated if/then statement interpreted; it can easily separate the business logic from the source code. Drools is the one of most mature open-source rule engines in the world.  It has been widely adopted in the industries as its' powerful and rich features. In Ratan One, there're various types of rules, e.g., suppression rules, validation rules and entitlement rules etc. Drools is considered as a better alternative to define and trigger the rules.

# 2. Solution

Drools treats the rules as the static resources, each rule file must follow its lifecycle in Drools, such as definition, compile, deployment and execution. In the meanwhile, Drools provides a collection of convenient APIs to build everything which includes rule definition, compilation, verification and execution. We can leverage this feature to trigger the rules hot deployment and refreshment once some changes apply to them.

## 2.1 Overview

In the overview diagram above, ratanone rule service will expose two kinds of API to presentation layer via API gateway, one is the rule maintenance API to create, update, query and delete the rules, while other is the rule execution API which is used for rule validation against the specified dataset.

## 2.2 Process Flow

### 2.2.1 Rule Maintenance

As the rule interpreter, Drools has its own language (Drools Rule Language) to define the rules, it is easily to separate the complex business logic from your code. However, in the other hand, it's difficult to design the interactive process to maintenance your rules definition on GUI. For this case, we have two table to store the rules for different purposes. The table ***ratan_rule ***is used for storing the rules that can be manipulated via API, such as operation add, update, query and delete. Once there are some changes applied to the rules, the corresponding DRL file will be generated automatically and persist in the table ***ratan_drools_rule ***finally.

The process flow of generating the DRL Files is shown as below:

**

The sample for rules that transformed to DRL*.*

```
Data_Flow.Data_Target_System == ORCID
```

```
import com.scb.ratan.rule.drools.api.Fact;
import java.util.*;

dialect "mvel"

rule "1709829242988974080"
  when
    Fact(name == 'scbml', $m : value)
    Map(Data_Flow!.Data_Target_System[0] matches "(?i)^ORCID$") from $m
  then
    // empty action
end
```

### 2.2.2 Rule Execution

The following diagram illustrates the process flow of rule execution.

**Process flow**

| Process | Flow | Description |
| --- | --- | --- |
| **Facts Preparation** | A1 > A2 > A3 > A4.1, A4.2 > A5 | In Drools terminology, facts represent the data that serves as input of the rules. There're two types of fact: - SCBML message passed by the clients, it will be transformed to JSON format that compliant with SCB logical model, and then enrich by calling ***fieldsXpath ***service. - Custom fact processors are used for producing the facts that need to fetch data from third-party services, such as check if the client is GSAM client by the given FMID. |
| **Rule Loading** | B1 > B2 | Load the specified DRL (Drools Rule File) content by given *'business flow'* and *'rule type'* from database. |
| **Rule Execution** | C1, C2 > C3 > C4 | The basic workflow of Drools rule engine. When the data is inserted into the working memory of Drools engine in the form of one or more facts. The drools engine matches those facts to the conditions of the rules that stored in production memory to determine the eligible rule execution. When the rule conditions are met, the Drools engine activates and registers rules in the agenda, where the eligible rules can be triggered and executed. |

**Rule execution sequence diagram**

**![rule_execution_flow.png](attachments/rule_execution_flow.png)**

## 2.3 Database Design

### 2.3.1 Data Model

### 2.3.2 Table ratan_rule

- Add one column* 'fact_processor' to handle the case that need to fetch data from another data sources.*
- Remove columns* such as 'operation_level', 'exception_code', 'exception_category'.*

| Item. # | Column Name | Data Type | Nullable | Comment |
| --- | --- | --- | --- | --- |
| 1 | id | text | false | primary key |
| 2 | business_flow | varchar | false | the value can be the one of the following: CONFIRMATION, SETTLEMENT or SETTLEMENT_AUTO_NETTING |
| 3 | rule_type | varchar | false | the value can be the one of the following: NSTP, NETTING, IRS, SUPPRESSION, SWIFT_SUPPRESSION or FX |
| 4 | rule | text | true | |
| 5 | status | varchar | false | |
| 6 | reason | text | true | |
| 7 | *fact_processor* | varchar | true | either column *'rule'* or* 'fact_processor'* is not null |
| 8 | version | int4 | false | |
| 9 | created_at | timestamp | false | |
| 10 | updated_at | timestamp | false | |
| 11 | created_by | varchar | false | |
| 12 | updated_by | varchar | false | |

### **2.3.3 Table **ratan_drools_rule

- The composite unique index contains filed "business_workflow" and "rule_type", please refer to the appendix 3.3.

| Item. # | Column Name | Data Type | Nullable | Comment |
| --- | --- | --- | --- | --- |
| 1 | id | text | false | primary key |
| 2 | business_flow | varchar | false | the value can be the one of the following: CONFIRMATION, SETTLEMENT or SETTLEMENT_AUTO_NETTING |
| 3 | rule_type | varchar | false | the value can be the one of the following: NSTP, NETTING, IRS, SUPPRESSION, SWIFT_SUPPRESSION or FX |
| 4 | fact_processor | varchar | false | a list of data processors that can fetch the data from various data sources. |
| 5 | drl_content | text | false | DRL (Drools Rule File) content that can be converted from human-readable rules in Table ***ratan_rule*** |
| 6 | version | int4 | false | the version of DRL file, default is 1. The version plus 1 when the rule is updated. |
| 7 | created_at | timestamp | false | creation time, default is the point time of data inserted. |
| 8 | updated_at | timestamp | false | last update time. |

### 2.2.4 Table ratan_drools_fact_processor

| Item. # | Column Name | Data Type | Nullable | Comment |
| --- | --- | --- | --- | --- |
| 1 | id | int | false | primary key |
| 2 | name | varchar | false | the name of fact processor |
| 3 | fact_name | varchar | false | the name of fact produced by the fact processor. |
| 4 | fact_expression | text | false | the expression of fact used in DRL file. Sample: *[* * {"expression": "Fact(name == '${fact_name}', $excludedCounterpartyList : value)"}, * * {"expression": "Map(this['Entity']!.Counterparty_SCI_FMID[0] not memberOf $excludedCounterpartyList) from $m"}* *]* |
| 5 | created_at | timestamp | false | creation time, default is the time of data inserted. |
| 6 | updated_at | timestamp | false | in history table, it shall be same as the creation time. |

## 2.4 API Design

| API Group | URL | Method | Request / Response | Description |
| --- | --- | --- | --- | --- |
| Rule Maintenance | /v2/rules?executionFlag=NOT_EXECUTED&needDryRunFlag=false add rule - executionFlag: not mandatory, by default is EXECUTION (supported values: EXECUTION , NOT_EXECUTION) - needDryRunFlag: not mandatory, by default is false (UI will popup a checkbox, only for maker) | POST | mandatory: businessFlow, ruleType, rule optional: reason, comment, metaData, ruleCategory ruleCategory by default => NORMAL **EXPAND: Request** { "businessFlow": "SETTLEMENT", "ruleType": "NSTP", "rule": " Cashflow__Payment_Amount > 2.01 && (Cashflow__Status_Event_Type == \"123123\" || Cashflow__Status_Event_Type == \"aaaabbbb\") ", "reason": "test", "comment": "maker add", "metaData": "[{\"exceptionTypeCategory\": \"ExceptionCaAAA\",\"level\": \"Maker\",\"test\":\"aaa\"},{\"exceptionTypeCategory\": \"ExceptionCaAAA\",\"level\": \"Checker\",\"test\":\"aaa\"},{\"exceptionTypeCategory\": \"ExceptionCaBBB\",\"level\": \"Maker\",\"test\":\"aaa\"},{\"exceptionTypeCategory\": \"ExceptionCaBBB\",\"level\": \"Checker\",\"test\":\"aaa\"}]", "ruleCategory":"SPECIAL" } **EXPAND_END** **EXPAND: Response** { "id": "7185832832437264384", "businessFlow": "SETTLEMENT", "ruleType": "NSTP", "userRule": " Cashflow__Payment_Amount > 2.01 && (Cashflow__Status_Event_Type == \"123123\" || Cashflow__Status_Event_Type == \"aaaabbbb\") ", "runningRule": "import com.scb.ratan.rule.drools.model.MatchedRule;\r\nimport java.util.*;\r\nimport com.scb.ratan.rule.drools.model.fact.EnhancedFact;\r\n\r\ndialect \"java\"\r\n\r\nglobal java.util.List matchedRuleSet;\r\n\r\nrule \"7185832832437264384-0\"\r\n when\r\n EnhancedFact( Cashflow__Payment_Amount > 2.01 )\r\n then\r\n MatchedRule matchedRule = new MatchedRule();\r\n matchedRule.setRuleId(\"7185832832437264384-0\");\r\n matchedRule.setReason(\"Cashflow__Payment_Amount > 2.01\");\r\n matchedRuleSet.add(matchedRule);\r\nend\r\nrule \"7185832832437264384-1\"\r\n when\r\n EnhancedFact( (Cashflow__Status_Event_Type == \"123123\" || Cashflow__Status_Event_Type == \"aaaabbbb\") )\r\n then\r\n MatchedRule matchedRule = new MatchedRule();\r\n matchedRule.setRuleId(\"7185832832437264384-1\");\r\n matchedRule.setReason(\"(Cashflow__Status_Event_Type == \\\"123123\\\" || Cashflow__Status_Event_Type == \\\"aaaabbbb\\\")\");\r\n matchedRuleSet.add(matchedRule);\r\nend\r\n", "status": "ADD_PENDING", "reason": "test", "metaData": "[{\"exceptionTypeCategory\": \"ExceptionCaAAA\",\"level\": \"Maker\",\"test\":\"aaa\"},{\"exceptionTypeCategory\": \"ExceptionCaAAA\",\"level\": \"Checker\",\"test\":\"aaa\"},{\"exceptionTypeCategory\": \"ExceptionCaBBB\",\"level\": \"Maker\",\"test\":\"aaa\"},{\"exceptionTypeCategory\": \"ExceptionCaBBB\",\"level\": \"Checker\",\"test\":\"aaa\"}]", "ruleCategory": "SPECIAL", "comment": "maker add", "executionFlag": "EXECUTION", "needDryRun": false, "version": 0, "createdAt": "2024-04-16T02:54:13.5718262Z", "updatedAt": "2024-04-16T02:54:13.5718262Z", "createdBy": "1632093", "updatedBy": "1632093" } **EXPAND_END** | |
| /v2/rules?executionFlag=NOT_EXECUTED&needDryRunFlag=false update rule | PUT | mandatory: id, rule optional: reason, comment, metaData, ruleCategory ruleCategory by default => NORMAL **EXPAND: Request** { "id":"7185832832437264384", "rule": "Cashflow__Status_Event_Type == \"Unsuppress123456sssaaaaaa\"", "reason": "test", "comment": "maker add", "metaData": "", "ruleCategory":"NORMAL" } **EXPAND_END** **EXPAND: Response** { "id": "7185824384781852672", "businessFlow": "SETTLEMENT", "ruleType": "NSTP", "userRule": " Cashflow__Payment_Amount > 2.01 && (Cashflow__Status_Event_Type == \"123123\" || Cashflow__Status_Event_Type == \"aaaabbbb\") ", "runningRule": "....", "status": "SAVE_CONFIRMED", "reason": "test", "metaData": "......", "ruleCategory": "NORMAL", "comment": "456", "executionFlag": "EXECUTION", "needDryRun": false, "version": 2, "createdAt": "2024-04-16T02:20:39.508375Z", "updatedAt": "2024-04-16T02:20:57.963719Z", "createdBy": "1632093", "updatedBy": "200000" } **EXPAND_END** | |
| /v2/rules | GET | [ { "id": "7185824384781852672", "businessFlow": "SETTLEMENT", "ruleType": "NSTP", "userRule": " Cashflow__Payment_Amount > 2.01 && (Cashflow__Status_Event_Type == \"123123\" || Cashflow__Status_Event_Type == \"aaaabbbb\") ", "runningRule": "import...", "status": "SAVE_CONFIRMED", "reason": "test", "metaData": "...", "ruleCategory": "NORMAL", "comment": "456", "executionFlag": "EXECUTION", "needDryRun": false, "version": 2, "createdAt": "2024-04-16T02:20:39.508375Z", "updatedAt": "2024-04-16T02:20:57.963719Z", "createdBy": "1632093", "updatedBy": "200000" } ] | change： rule -》userRule add： "runningRule": "..." "comment": "user comment", "executionFlag": "EXECUTION", "needDryRun": false, "referenceRuleId": "7165211647473512333", "version": 0, |
| /v2/rules/filter | GET | **EXPAND: Request** GET /v2/rules/filter?businessFlow=CONFIRMATION,SETTLEMENT&ruleType=SUPPRESSION&status=DEL_PENDING,ADD_CONFIRMED,UPDATE_PENDING **EXPAND_END** Response data will be sorted by "updatedAt", lastest data will be in top CREATING, UPDATING will be added as default status **EXPAND: Response** [ { "id": "7185824384781852672", "businessFlow": "SETTLEMENT", "ruleType": "NSTP", "userRule": " Cashflow__Payment_Amount > 2.01 && (Cashflow__Status_Event_Type == \"123123\" || Cashflow__Status_Event_Type == \"aaaabbbb\") ", "runningRule": "import...", "status": "SAVE_CONFIRMED", "reason": "test", "metaData": "...", "ruleCategory": "NORMAL", "comment": "456", "executionFlag": "EXECUTION", "needDryRun": false, "version": 2, "createdAt": "2024-04-16T02:20:39.508375Z", "updatedAt": "2024-04-16T02:20:57.963719Z", "createdBy": "1632093", "updatedBy": "200000" } ] **EXPAND_END** | |
| /v2/rules/{ruleId} | GET | **EXPAND: Request** GET /v2/rules/7185824384781852672 **EXPAND_END** **EXPAND: Response** { "id": "7185824384781852672", "businessFlow": "SETTLEMENT", "ruleType": "NSTP", "userRule": " Cashflow__Payment_Amount > 2.01 && (Cashflow__Status_Event_Type == \"123123\" || Cashflow__Status_Event_Type == \"aaaabbbb\") ", "runningRule": "import...", "status": "SAVE_CONFIRMED", "reason": "test", "metaData": "...", "ruleCategory": "NORMAL", "comment": "456", "executionFlag": "EXECUTION", "needDryRun": false, "version": 2, "createdAt": "2024-04-16T02:20:39.508375Z", "updatedAt": "2024-04-16T02:20:57.963719Z", "createdBy": "1632093", "updatedBy": "200000" } **EXPAND_END** | |
| /v2/rules/{ruleId} | DELETE | **EXPAND: Request** DELETE /v2/rules/7185833295664586752 { "comment": "123" } **EXPAND_END** **EXPAND: Response** { "id": "7185824384781852672", "businessFlow": "SETTLEMENT", "ruleType": "NSTP", "userRule": " Cashflow__Payment_Amount > 2.01 && (Cashflow__Status_Event_Type == \"123123\" || Cashflow__Status_Event_Type == \"aaaabbbb\") ", "runningRule": ".....", "status": "DELETE_PEDING", "reason": "test", "metaData": "[{\"exceptionTypeCategory\": \"ExceptionCaAAA\",\"level\": \"Maker\",\"test\":\"aaa\"},{\"exceptionTypeCategory\": \"ExceptionCaAAA\",\"level\": \"Checker\",\"test\":\"aaa\"},{\"exceptionTypeCategory\": \"ExceptionCaBBB\",\"level\": \"Maker\",\"test\":\"aaa\"},{\"exceptionTypeCategory\": \"ExceptionCaBBB\",\"level\": \"Checker\",\"test\":\"aaa\"}]", "ruleCategory": "NORMAL", "comment": "456", "executionFlag": "EXECUTION", "needDryRun": false, "version": 2, "createdAt": "2024-04-16T02:20:39.508375Z", "updatedAt": "2024-04-16T02:20:57.963719Z", "createdBy": "1632093", "updatedBy": "200000" } **EXPAND_END** | |
| /v2/rules/{ruleId}/history | GET | **EXPAND: Request** GET /v2/rules/7185833295664586752/history **EXPAND_END** **EXPAND: Response** [ { "id": "7185833295664586752", "businessFlow": "SETTLEMENT1", "ruleType": "NSTP", "userRule": " Cashflow__Payment_Amount > 2.01 && (Cashflow__Status_Event_Type == \"123123\" || Cashflow__Status_Event_Type == \"aaaabbbb\") ", "runningRule": "import...", "status": "SAVE_CONFIRMED", "reason": "test", "comment": "456", "executionFlag": "EXECUTION", "needDryRun": false, "version": 0, "createdAt": "2024-04-16T02:54:13.571826Z", "updatedAt": "2024-04-16T02:56:03.574633Z", "createdBy": "1632093", "updatedBy": "200000", "ruleId": "7185832832437264384", "dataVersion": 2 } ] **EXPAND_END** | |
| /v2/rules/history | GET | **EXPAND: Request** /v2/rules/history?ruleId=7166641870997913601&businessFlow=SETTLEMENT&ruleType=NSTP&status=ADD_PENDING,UPDATE_PENDING&startTime=2024-02-20T09:26:28Z&endTime=2024-02-23T09:26:28Z ruleId – optional businessFlow – optional, can be multiple values like SETTLEMENT,CONFIRMATION ruleType – optional status — optional can be multiple values like ADD_PENDING,UPDATE_PENDING startTime – optional endTime – optional **EXPAND_END** **EXPAND: Response** [ { "id": "7165211647473512448", "ruleId": "7165211647473512550", "businessFlow": "SETTLEMENT", "ruleType": "NSTP", "userRule": "Data_Flow__Data_Type == 'aaaa11111222' && Data_Flow__Data_Source_System_Domain_Name == 'FM'", "runningRule": "...", "status": "ADD_PENDING", "reason": "The target system is 'Cashflow Data'", "comment": "user comment", "executionFlag": "EXECUTION", "needDryRun": false, "referenceRuleId": "7165211647473512333", "version": 0, "createdAt": "2024-02-19T05:12:59.953340101Z", "updatedAt": "2024-02-19T05:12:59.953361678Z", "createdBy": "1632093", "updatedBy": "1632093" } ] **EXPAND_END** | |
| /v2/rules/{ruleId}/status/{targetStatus} | PUT | Status machine can be refered to [RATAN Rule Engine Overview - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/RATAN+Rule+Engine+Overview) **EXPAND: Request** Request URL /v2/rules/1722810986574258176/status/SAVE_CONFIRMED { "comment": "123", – optional "userAction": "CHECKER_CONFIRM" – this is **mandatory only** for status from UPDATE_PENDING to SAVE_CONFIRMED, value can be only CHECKER_CONFIRM, CHECKER_REJECT } **EXPAND_END** **EXPAND: Response** Response Body { "id": "7185832832437264384", "businessFlow": "SETTLEMENT1", "ruleType": "NSTP", "userRule": " Cashflow__Payment_Amount > 2.01 && (Cashflow__Status_Event_Type == \"123123\" || Cashflow__Status_Event_Type == \"aaaabbbb\") ", "runningRule": "import ....", "status": "CREATING", "reason": "test", "metaData": "....", "ruleCategory": "SPECIAL", "comment": "456", "executionFlag": "EXECUTION", "needDryRun": false, "version": 1, "createdAt": "2024-04-16T02:54:13.571826Z", "updatedAt": "2024-04-16T02:55:57.0823008Z", "createdBy": "1632093", "updatedBy": "200000" } **EXPAND_END** | |
| /v2/rules/{ruleId}/{enable/disable} This is only for special rule control disabled rule will be enabled enabled rule will be disabled | PUT | **EXPAND: Request** /v2/rules/1722810986574258176/enable /v2/rules/1722810986574258176/disable **EXPAND_END** **EXPAND: Response** { "id": "7185832832437264384", "businessFlow": "SETTLEMENT1", "ruleType": "NSTP", "userRule": " Cashflow__Payment_Amount > 2.01 ", "runningRule": "import ....", "status": "SAVE_CONFIRMED", "reason": "test", "metaData": "....", "ruleCategory": "SPECIAL", "**enabled****": true,** "comment": "456", "executionFlag": "EXECUTION", "needDryRun": false, "version": 1, "createdAt": "2024-04-16T02:54:13.571826Z", "updatedAt": "2024-04-16T02:55:57.0823008Z", "createdBy": "1632093", "updatedBy": "200000" } **EXPAND_END** | |
| /v2/rules/activate/{ruleId} This for activate dry run rule | | **EXPAND: Response** { "id": "7185832832437264384", "businessFlow": "SETTLEMENT1", "ruleType": "NSTP", "userRule": " Cashflow__Payment_Amount > 2.01 ", "runningRule": "import ....", "status": "SAVE_CONFIRMED", "reason": "test", "metaData": "....", "ruleCategory": "SPECIAL", ** "enabled": true,** "comment": "456", "executionFlag": "EXECUTION", "needDryRun": false, "version": 1, "createdAt": "2024-04-16T02:54:13.571826Z", "updatedAt": "2024-04-16T02:55:57.0823008Z", "createdBy": "1632093", "updatedBy": "200000" } **EXPAND_END** | |
| Rule Execution @Deprecated v1 will be decommissioned in the future | ~~/v1/rules/validate~~ | POST | **EXPAND: Request** { "businessFlow": "SETTLEMENT", "ruleType": "NSTP", "scbml": "<xml message>" } **EXPAND_END** **EXPAND: Response** { "code": "FILTERED", "matchedRules": [ { "ruleId": "1714835710721036288", "reason": "Cashflow.Payment_Date '2023-09-23' is not a valid business day" }, { "ruleId": "1715280364784480256", "reason": "value date: 2023-09-23 is before the current system date '2023-11-10'" } ] } **EXPAND_END** | Rule validation. |
| Rule Execution v2 | /v2/rules/validate logicFacts => consist data format in logicModel additionalFacts => consist extra data format(not in logic model) | POST | **EXPAND: Request** { "businessFlow": "SETTLEMENT", "ruleType": "NETTING", "message": { "logicFacts": { "Entity": { "Counterparty_Is_Internal": [ "INTERNAL" ], "Counterparty_Murex_Display_Shortcode": [ "SC_COMSH_BTB" ], "Booking_Entity_SCI_FMID": [ "10032025" ], "Counterparty_SCI_FMID": [ "400888471" ] }, "Trade_Lake_Valid_From_Date_Time": [], "Swap_Instrument": { "IR_Leg": { "First_Leg": { "Schedule_Generation_Rule": { "Business_Center": { "Payment_Date_Business_Center": [ "" ] } } } } }, "Portfolio": { "Booking_Entity_Trade_Portfolio_Name": [ "COM_XIAMEN_BTB" ] }, "pipelineExceptionFields": {}, "Trade_Id": [ "85573048" ], "Trade_State": [ "TOBESENT" ], "Major_Version": [ "" ], "Trade_Lake_Valid_To_Date_Time": [], "exceptions": { "Trade_Lake_Valid_From_Date_Time": [ "2024-12-02" ], "Trade_Lake_Valid_To_Date_Time": [ "2024-12-02" ] }, "Cashflow": { "Cashflow_Affirmation_Status": [ "Unaffirmed" ], "Cashflow_Business_Version": [ "0" ], "Status_Event_Type": [ "" ], "Is_STP": [ "" ], "Is_Cashflow_Unnet": [ "false" ], "Is_Cashflow_Unsuppress": [ "" ], "Is_Cashflow_SettleAsGross": [ "" ], "Cashflow_Event_Reason": [ "" ], "Is_Withdrawal_On_Component": [ "" ], "Payment_Type": [ "" ], "Booking_System_Event": [ "New" ], "Payment_Date": [ "2023-12-11" ], "Is_Amended_Post_Settlement": [ "false" ], "Is_Cashflow_Reinstate": [ "" ], "Murex_Structure_Id": [ "0" ], "Is_Private_Banking_Cashflow": [ "false" ], "Cashflow_Event_Type": [ "New" ], "Data_Flow__Data_Source_System": [ "MUREX" ], "Cashflow_State": [ "Projected" ], "Netting_Id": [ "" ], "Is_Adhoc_Net": [ "" ], "Payment_Currency": [ "CNO" ], "Is_Cashflow_Swift_Unsuppress": [ "" ], "Payment_Amount": [ "0.01" ], "Cashflow_Id": [ "M00015700049" ] }, "Trade_Version": [ "" ], "Instrument_Common": { "Murex_Product_Typology": [ "" ], "Murex_Product_Family": [ "CURR" ], "Murex_Product_Strategy": [ "" ], "Murex_Product_Group": [ "FXD" ], "Murex_Product_Type": [ "FXD" ], "CFI_Code": [ "IFXXXX" ], "Source_System_Instrument_Sub_Type": [ "CURR|FXD|FXD" ], "ISDA_Taxonomy": [ "CURR|FXD|FXD" ] }, "Trade_Purpose": [ "" ], "Data_Flow": { "Data_Type": [ "aaaa11111222" ], "Data_Source_System_Domain_Name": [ "FM" ], "Data_Sender": [ "MUREX" ], "Data_Publication_Date_Time": [ "2023-07-24T06:32:10Z" ], "Data_Source_System_Country_Code": [ "ALL" ], "Data_Publication_Id": [ "MUREX-15700049--2023-07-24T06:32:10Z" ], "Data_Source_System": [ "MUREX" ] }, "BCS_Trade_Id": [ "85573048" ], "Delivery_Method": [ "" ] }, "additionalFacts": { "Data_Flow": { "Data_Type": [ "wwwwwww" ] } } } } **EXPAND_END** **EXPAND: Response** { "code": "SUCCESS", "matchedRules": [ ], "unMatchedRules": [ { "ruleId": "7161558747297562624", "rule": "Data_Flow__Data_Type == 'aaaa11111222' && Data_Flow__Data_Source_System_Domain_Name == 'FM'", "reason": "The target system is 'Cashflow Data'", "matchedSubRules": [ { "ruleId": "7161562470145052672", "reason": "Data_Flow__Data_Type == 'aaaa11111222'" } ] } ] } **EXPAND_END** matchedRules data format refers to unMatchedRules | |
| | /v2/rules/validate/adaptor/{type} type: supported type: cashflow, trade, other type won't supported at current moment. This is v2 adaptor solution to consume scbml message | | **EXPAND: Request** { "businessFlow": "SETTLEMENT", "ruleType": "NSTP", "scbml": "<xml message>" } **EXPAND_END** **EXPAND: Response** { "code": "SUCCESS", "matchedRules": [ ], "unMatchedRules": [ { "ruleId": "7161558747297562624", "rule": "Data_Flow__Data_Type == 'aaaa11111222' && Data_Flow__Data_Source_System_Domain_Name == 'FM'", "reason": "The target system is 'Cashflow Data'", "matchedSubRules": [ { "ruleId": "7161562470145052672", "reason": "Data_Flow__Data_Type == 'aaaa11111222'" } ] } ] } **EXPAND_END** | |
| | /v2/rules/validate/multi This API only for testing specific field value in two input Json, to see if the values are same, or are different. messageOne, messageTwo data format will be refered to API /v2/rules/validate | POST | Request will contain two logic facts, messageOne messageTwo <details> <summary>展开详情</summary> ```text { "businessFlow": "SETTLEMENT", "ruleType": "NETTING", "factMessageList": [ { "logicFacts": { "Entity": { "Counterparty_Is_Internal": [ "INTERNAL" ], "Counterparty_Murex_Display_Shortcode": [ "SC_COMSH_BTB" ], "Booking_Entity_SCI_FMID": [ "10032025" ], "Counterparty_SCI_FMID": [ "400888471" ] } }, "additionalFacts": { "Data_Flow": { "Data_Type1": [ "wwwwwww" ] } } }, { "logicFacts": { "Entity": { "Counterparty_Is_Internal": [ "INTERNAL" ], "Counterparty_Murex_Display_Shortcode": [ "SC_COMSH_BTB" ], "Booking_Entity_SCI_FMID": [ "10032025" ], "Counterparty_SCI_FMID": [ "400888471" ] } }, "additionalFacts": { "Data_Flow": { "Data_Type1": [ "wwwwwww" ] } } } ] } ``` </details> **EXPAND: Response** { "code": "SUCCESS", "matchedRules": [ ], "unMatchedRules": [ { "ruleId": "7161558747297562624", "rule": "Data_Flow__Data_Type == 'aaaa11111222' && Data_Flow__Data_Source_System_Domain_Name == 'FM'", "reason": "The target system is 'Cashflow Data'", "matchedSubRules": [ { "ruleId": "7161562470145052672", "reason": "Data_Flow__Data_Type == 'aaaa11111222'" } ] } ] } **EXPAND_END** | |
| | /v2/rules/validate/batch This API receives a list of request, each request contains two messages, messageOne, messageTwo data format will be refered to API /v2/rules/validate list size can't exceed 400, | | Each Object will contain a pair of two facts, messageOne messageTwo <details> <summary>展开详情</summary> ```text [ { "uniqueId": "12312asdas", "businessFlow": "SETTLEMENT", "ruleType": "NETTING", "messageOne": { "logicFacts": { "Trade_Id": [ "85573048" ] }, "additionalFacts": {} }, "messageTwo": { "logicFacts": { "Trade_Id": [ "85573049" ] }, "additionalFacts": {} } }, { "uniqueId": "12312asdas", "businessFlow": "SETTLEMENT", "ruleType": "NETTING", "messageOne": { "logicFacts": { "Trade_Id": [ "85573050" ] }, "additionalFacts": {} }, "messageTwo": { "logicFacts": { "Trade_Id": [ "85573051" ] }, "additionalFacts": {} } } ] ``` </details> **EXPAND: Response** [ { "uniqueId": "123asdads", "code": "SUCCESS", "matchedRules": [], "unMatchedRules": [ { "ruleId": "7161558747297562624", "rule": "Data_Flow__Data_Type=='aaaa11111222'&&Data_Flow__Data_Source_System_Domain_Name=='FM'", "reason": "Thetargetsystemis'CashflowData'", "matchedSubRules": [ { "ruleId": "7161562470145052672", "reason": "Data_Flow__Data_Type=='aaaa11111222'" } ] } ] }, { "uniqueId": "sadasdasdasw", "code": "SUCCESS", "matchedRules": [], "unMatchedRules": [ { "ruleId": "7161558747297562624", "rule": "Data_Flow__Data_Type=='aaaa11111222'&&Data_Flow__Data_Source_System_Domain_Name=='FM'", "reason": "Thetargetsystemis'CashflowData'", "matchedSubRules": [ { "ruleId": "7161562470145052672", "reason": "Data_Flow__Data_Type=='aaaa11111222'" } ] } ] } ] **EXPAND_END** | |

# 3. Appendix

## 3.1 Convert Suppression Rule to Drools Rule Format

MVEL (MVFLEX Expression Language) is the default language used in Drools Rule conditions constraints segment. MVEL was inspired by Java syntax, but has some fundamental differences aimed at making it more efficient as an expression language, such as operators that directly support collection, array and string matching, as well as regular expressions. Therefore, some original rules must be transformed and compliant with MVEL syntax.

| Original Rule | Drools Rule | Description |
| --- | --- | --- |
| Source_System_Trade_Internal_Id==2376489 | ***this[***'Source_System_Trade_Internal_Id'***]***==2376489 | As the input data was inserted into Drools runtime as a* java.util.Map* object, MVEL must use*** 'this[key]' ***operator to retrieve the value. |
| Source_System_Validation_Status==MO_Validated | ***this['***Source_System_Validation_Status***']***=='MO_Validated' | The single or double quote is a must-have for the string values, otherwise it will be treated as a variable. |
| Cashflow.Cashflow_State==PROJECTED * * | Cashflow***!.***Cashflow_State=='PROJECTED' | **!.** is the null-safe bean property navigator, it is equivalent to: ***Cashflow != null && Cashflow.Cashflow_State=='PROJECTED'*** |
| Cashflow.Cashflow_State==PROJECTED | Cashflow!.Cashflow_State ***matches '(?i)^PROJECTED$' *** | As the equal operator '==' doesn't support the ***String#equalsIgnoreCase ***method in Java, the matches operator can be a replacement for comparing the values without case sensitive. |
| Entity.Counterparty_Country_ISO_Code==FR | Entity.Counterparty_Country_ISO_Code***[0]* **matches '(?i)^FR$' | Support JSONArray Object index navigator |

## 3.2 Sample of Suppression Rule execution

Scenario: Trade Confirmation Orchestration Process is shown as below. In the step of suppression, it will call the suppression service to determine whether the trade is suppressed.

![ConfirmationFlow.PNG](attachments/ConfirmationFlow.PNG)

Verification steps:

- Get the SCBML message from Kafka topic ***’Confirmation_Orchestration_Process_In‘.***
- Use the Postman to request the suppression rule service in DEV environment.
- Use the Postman to request the new rule service in Local environment.
- Compare the response from suppression rule service and new rule service to see whether they are same or not.

| | New Rule Service | Suppression Service |
| --- | --- | --- |
| URL | [http://localhost:8080/v2/suppressions/rules/check](http://localhost:8080/v2/suppressions/rules/check) | [http://uklvadapp1340.uk.dev.net:8079/v2/suppressions/rules/check](http://uklvadapp1340.uk.dev.net:8079/v2/suppressions/rules/check) |
| Request Body | { "trackingId": "MOCK_CONFIRMATION_TRACKING_00000001", "data": { "BusinessFlow": "CONFIRMATION", "ProductType": "All" }, "message": "<SCBML MESSAGE>" } | { "trackingId": "MOCK_CONFIRMATION_TRACKING_00000001", "data": { "BusinessFlow": "CONFIRMATION", "ProductType": "All" }, "message": "<SCBML MESSAGE>" } |
| Match Rules | *Data_Flow.Data_Target_System==ORCID* |
| Response | { "trackingId": "MOCK_CONFIRMATION_TRACKING_00000001", "message": "<scbml message>", "metadata": null, "data": { "BusinessFlow": "CONFIRMATION", "ProductType": "All" }, "camundaResponseCode": "SUCCESS", "description": "[]" } | { "trackingId": "MOCK_CONFIRMATION_TRACKING_00000001", "message": "<scbml message>", "metadata": null, "data": { "BusinessFlow": "CONFIRMATION", "ProductType": "All" }, "camundaResponseCode": "SUCCESS", "description": "[]" } |
| Match Rules | *Data_Flow.Data_Target_System==ORCID* *Entity.Counterparty_Country_ISO_Code==FR&&Source_System_Trade_Internal_Id==2376489* |
| Response | { "trackingId": "MOCK_CONFIRMATION_TRACKING_00000001", "message": "<scbml message>", "metadata": null, "data": { "BusinessFlow": "CONFIRMATION", "ProductType": "All" }, "camundaResponseCode": "FILTERED", *"description": "[{\"description\":\"Rule[Entity.Counterparty_Country_ISO_Code==FR&&Source_System_Trade_Internal_Id==2376489] matched\",\"id\":32376,\"reason\":\"For testing purpose\",\"result\":\"FILTERED\"}]"* } ![image2023-8-18_22-26-41.png](attachments/image2023-8-18_22-26-41.png) | { "trackingId": "MOCK_CONFIRMATION_TRACKING_00000001", "message": "<scbml message>", "metadata": null, "data": { "BusinessFlow": "CONFIRMATION", "ProductType": "All" }, "camundaResponseCode": "FILTERED", *"description": "[{\"result\":\"FILTERED\",\"reason\":\"For testing purpose\",\"description\":\"Rule [Entity.Counterparty_Country_ISO_Code==FR] matched, expectedRuleValue is 'FR' ,realRuleValue value is 'FR'.Rule [Source_System_Trade_Internal_Id==2376489] matched, expectedRuleValue is '2376489' ,realRuleValue value is '2376489'.\",\"id\":\"32376\"}]*" } ![image2023-8-18_22-27-46.png](attachments/image2023-8-18_22-27-46.png) |

| No | description | status | Question | Answer |
| --- | --- | --- | --- | --- |
| 1 | ![image2024-3-7_10-37-25.png](attachments/image2024-3-7_10-37-25.png) | Done | 1. add rule response no referenceRuleId | response will display field whose contains value. for adding rule, referenceRuleId will always be empty. But for updating rule, referenceRuleId field will contain previous ruleId |
| 2 | version remove for all of add/update/delete | Done | | |
| 3 | [Rule Migration Summary - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/Rule+Migration+Summary) ![image2024-3-11_14-24-1.png](attachments/image2024-3-11_14-24-1.png) **all Instr. Modif cases are failed** | Open | select * from ratanone.event_history where comment like '%RATAN accepts Equity & OTC Option & market events%' and reference_id='**000000634A**' and tracking_id like '%**9e43b761-87e3-4545-b02e-f78c836fe97a**%'; 这个[N] BCS Trade with primaryAssetClass=Equity and subType=OTC Option and tradeEventType does is** Instr. Modif**，不应该被suppression，但是被suppression了 | |
| 4 | select * from ratanone.event_history where reference_id='**300021100006**'; select * from ratanone.event_history where reference_id='100021100365'; ![image2024-3-11_14-25-10.png](attachments/image2024-3-11_14-25-10.png) | Open | EG TOBESENT does not pass pre-check | |
| 5 | [P] BCS Trade with primaryAssetClass=Equity and subType=Funded Swap and subType does not Buy/Sell action_FieldDict=Create Dictionary||primaryAssetClass=Equity||subType=Funded Swap||tradeEventType=Buy/Sell1; action_tradeId||trackingno=GenTradeBCS||&{FieldDict}; select * from ratanone.event_history where reference_id='**000000634A**' and tracking_id like '%**7026856e-2791-4383-91b5-7d70c1ad7b23**%'; | Open | should be suppress by RATAN accepts Equity & Funded Swap & market events% but suppress by RATAN accepts Equity & Equity Swap & market events | |