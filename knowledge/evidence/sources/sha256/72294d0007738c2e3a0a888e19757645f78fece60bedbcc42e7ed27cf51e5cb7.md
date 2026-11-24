Roadmap

![image2024-2-21_16-21-0.png](attachments/image2024-2-21_16-21-0.png)

# Purpose

This wiki majorly implicates the future enhancement in RatanOne Rule Service

# Rule Information

## Operator

[Drools Features Explore - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/Drools+Features+Explore)

And

**EXPAND: Request**

//Infix `and`:

Color( colorType : type ) and Person( favoriteColor == colorType )

//Infix `and` with grouping:

(Color( colorType : type ) and (Person( favoriteColor == colorType ) or Person( favoriteColor == colorType ))

// Prefix `and`:

(and Color( colorType : type ) Person( favoriteColor == colorType ))

// Default implicit `and`:

Color( colorType : type ) Person( favoriteColor == colorType )

**EXPAND_END**

Or

**EXPAND: Request**

//Infix `or`:

Color( colorType : type ) or Person( favoriteColor == colorType )

//Infix `or` with grouping:

(Color( colorType : type ) or (Person( favoriteColor == colorType ) and Person( favoriteColor == colorType ))

// Prefix `or`:

(or Color( colorType : type ) Person( favoriteColor == colorType ))

**EXPAND_END**

## Rule Attribute

**EXPAND: Attribute Detail**

| Attribute | Value |
| --- | --- |
| `salience` | An integer defining the priority of the rule. Rules with a higher salience value are given higher priority when ordered in the activation queue. Example: `salience 10` **EXPAND: Request** import com.scb.ratan.rule.drools.fact.Fact; import com.scb.ratan.rule.drools.function.JsonPathHelper; import com.scb.ratan.rule.drools.model.MatchedRule; import java.util.*; import com.scb.ratan.rule.common.web.vo.Property dialect "mvel" global java.util.List matchedRuleSet; // request consumes direct property format rule "salience_rule_1" salience 1 when then MatchedRule matchedRule = new MatchedRule(); matchedRule.setRuleId("salience_rule_1"); matchedRuleSet.add(matchedRule); end rule "salience_rule_2" salience 100 when then MatchedRule matchedRule = new MatchedRule(); matchedRule.setRuleId("salience_rule_2"); matchedRuleSet.add(matchedRule); end **EXPAND_END** |
| `enabled` | A Boolean value. When the option is selected, the rule is enabled. When the option is not selected, the rule is disabled. Example: `enabled true` |
| `date-effective` | A string containing a date and time definition. The rule can be activated only if the current date and time is after a `date-effective` attribute. Example: `date-effective "4-Sep-2018"` |
| `date-expires` | A string containing a date and time definition. The rule cannot be activated if the current date and time is after the `date-expires` attribute. Example: `date-expires "4-Oct-2018"` **EXPAND: Request** import com.scb.ratan.rule.drools.fact.Fact; import com.scb.ratan.rule.drools.function.JsonPathHelper; import com.scb.ratan.rule.drools.model.MatchedRule; import java.util.*; import com.scb.ratan.rule.common.web.vo.Property dialect "mvel" global java.util.List matchedRuleSet; // request consumes direct property format rule "1001" //date-effective "18-05-2024" date-effective "2024-01-29 15:00:26" date-expires "2024-02-22 10:54:26" when Fact(name == 'property', $property : value) Property(field == "key1", value == 'value1' ) from $property then MatchedRule matchedRule = new MatchedRule(); matchedRule.setRuleId("1001"); matchedRuleSet.add(matchedRule); end **EXPAND_END** |
| `no-loop` | A Boolean value. When the option is selected, the rule cannot be reactivated (looped) if a consequence of the rule re-triggers a previously met condition. When the condition is not selected, the rule can be looped in these circumstances. Example: `no-loop true` |
| `agenda-group` | A string identifying an agenda group to which you want to assign the rule. Agenda groups allow you to partition the agenda to provide more execution control over groups of rules. Only rules in an agenda group that has acquired a focus are able to be activated. Example: `agenda-group "GroupName"` **EXPAND: Request** import com.scb.ratan.rule.drools.fact.Fact; import com.scb.ratan.rule.drools.function.JsonPathHelper; import com.scb.ratan.rule.drools.model.MatchedRule; import java.util.*; import com.scb.ratan.rule.common.web.vo.Property dialect "mvel" global java.util.List matchedRuleSet; // request consumes direct property format rule "agenda_group_001_rule_1" agenda-group "group-001" when then MatchedRule matchedRule = new MatchedRule(); matchedRule.setRuleId("agenda_group_001_rule_1"); matchedRuleSet.add(matchedRule); end rule "agenda_group_001_rule_2" agenda-group "group-001" when then MatchedRule matchedRule = new MatchedRule(); matchedRule.setRuleId("agenda_group_001_rule_2"); matchedRuleSet.add(matchedRule); end rule "agenda_group_002_rule_3" agenda-group "group-002" when then MatchedRule matchedRule = new MatchedRule(); matchedRule.setRuleId("agenda_group_002_rule_3"); matchedRuleSet.add(matchedRule); end rule "agenda_group_no_group_rule_4" when then MatchedRule matchedRule = new MatchedRule(); matchedRule.setRuleId("agenda_group_no_group_rule_4"); matchedRuleSet.add(matchedRule); end **EXPAND_END** |
| `activation-group` | A string identifying an activation (or XOR) group to which you want to assign the rule. In activation groups, only one rule can be activated. The first rule to fire will cancel all pending activations of all rules in the activation group. Example: `activation-group "GroupName"` **EXPAND: Request** import com.scb.ratan.rule.drools.fact.Fact; import com.scb.ratan.rule.drools.function.JsonPathHelper; import com.scb.ratan.rule.drools.model.MatchedRule; import java.util.*; import com.scb.ratan.rule.common.web.vo.Property dialect "mvel" global java.util.List matchedRuleSet; // request consumes direct property format rule "activation_group_001_rule_1" activation-group "group-001" salience 1 when then System.out.println("activation_group_001_rule_1"); end rule "activation_group_001_rule_2" activation-group "group-001" salience 2 when then System.out.println("activation_group_001_rule_2"); end rule "activation_group_002_rule_3" activation-group "group-002" when then System.out.println("activation_group_002_rule_3"); end rule "activation_group_no_group_rule_4" when then System.out.println("activation_group_no_group_rule_4"); end **EXPAND_END** |
| `duration` | A long integer value defining the duration of time in milliseconds after which the rule can be activated, if the rule conditions are still met. Example: `duration 10000` |
| `timer` | A string identifying either `int` (interval) or `cron` timer definitions for scheduling the rule. Example: `timer ( cron:* 0/15 * * * ? )` (every 15 minutes) |
| `calendar` | A [Quartz](http://www.quartz-scheduler.org/) calendar definition for scheduling the rule. Example: `calendars "* * 0-7,18-23 ? * *"` (exclude non-business hours) |
| `auto-focus` | A Boolean value, applicable only to rules within agenda groups. When the option is selected, the next time the rule is activated, a focus is automatically given to the agenda group to which the rule is assigned. Example: `auto-focus true` |
| `lock-on-active` | A Boolean value, applicable only to rules within rule flow groups or agenda groups. When the option is selected, the next time the ruleflow group for the rule becomes active or the agenda group for the rule receives a focus, the rule cannot be activated again until the ruleflow group is no longer active or the agenda group loses the focus. This is a stronger version of the `no-loop` attribute, because the activation of a matching rule is discarded regardless of the origin of the update (not only by the rule itself). This attribute is ideal for calculation rules where you have a number of rules that modify a fact and you do not want any rule re-matching and firing again. Example: `lock-on-active true` |
| `ruleflow-group` | A string identifying a rule flow group. In rule flow groups, rules can fire only when the group is activated by the associated rule flow. Example: `ruleflow-group "GroupName"` |
| `dialect` | A string identifying either `JAVA` or `MVEL` as the language to be used for code expressions in the rule. By default, the rule uses the dialect specified at the package level. Any dialect specified here overrides the package dialect setting for the rule. Example: `dialect "JAVA"` |

**EXPAND_END**

# Solution

## Enhancement Direction

### Rule Maintenance

1. F2E solution
2. Align with DM - logical model
3. Maker / Checker rule control (CRUD)
4. Self-service user management
5. Rule dry-run (TODO,-- verification, activation)
6. From simple to complex rule support

### Rule Execution

1. High performance
2. Filtered rule indication
3. HA
4. Rich operator

## User Guide Principle

1. One rule should have only **&&** operator when **not** using **group** (FE need add constraints)
2. **||** operator only happens inside group
3. Different rule logic relation is '**or**'

Example:

permitted:

```text
-- case 1
Cashflow.Payment_Amount == 100 
&& 
Cashflow.Payment_Currency in ('USD', 'CNY')

-- case 2
Cashflow.Payment_Amount == 100 
&& 
Cashflow.Payment_Currency in ('USD', 'CNY') 
&&
(Cashflow.Payment_Date == '2024-01-27' || Cashflow.STP_Cutoff_Date_Time == '2024-01-27 17:19:27')


```

forbidden:

```text
-- case 1
Cashflow.Payment_Amount == 100 
|| 
Cashflow.Payment_Currency in ('USD', 'CNY')

-- case 2
Cashflow.Payment_Amount == 100 
|| 
Cashflow.Payment_Currency in ('USD', 'CNY') 
||
(Cashflow.Payment_Date == '2024-01-27' && Cashflow.STP_Cutoff_Date_Time == '2024-01-27 17:19:27')


```

| Template | Sample | **Pros** | **Cons** |
| --- | --- | --- | --- |
| ```java dialect "java" global java.util.List matchedRuleSet; <#list rules as rule> rule "${rule.id}" when Rule(${rule.condition}) then MatchedRule matchedRule = new MatchedRule(); matchedRule.setRuleId(${rule.id}); matchedRule.setReason(${rule.condition}); matchedRuleSet.add(matchedRule); end </#list> ``` | Predefined rule ```text Cashflow.Payment_Amount == 100 && Cashflow.Payment_Currency in ('USD', 'CNY') && (Cashflow.Payment_Date == '2024-01-27' || Cashflow.STP_Cutoff_Date_Time == '2024-01-27 17:19:27') ``` Only conversion : (BE or FE) . converted to __ ```text Cashflow__Payment_Amount == 100 && Cashflow__Payment_Currency in ('USD', 'CNY') && (Cashflow__Payment_Date == '2024-01-27' || Cashflow__STP_Cutoff_Date_Time == '2024-01-27 17:19:27') ``` <details> <summary>Expand Details</summary> ```java global java.util.List matchedRuleSet; rule "001" when Rule(Cashflow__Payment_Amount == 100 ) then MatchedRule matchedRule = new MatchedRule(); matchedRule.setRuleId("001"); matchedRule.setReason("Cashflow__Payment_Amount == 100"); matchedRuleSet.add(matchedRule); end rule "002" when Rule( Cashflow__Payment_Currency in ('USD', 'CNY') ) then MatchedRule matchedRule = new MatchedRule(); matchedRule.setRuleId("002"); matchedRule.setReason("Cashflow__Payment_Currency in ('USD', 'CNY')"); matchedRuleSet.add(matchedRule); end rule "003" when Rule(Cashflow__Payment_Date == '2024-01-27' || Cashflow__STP_Cutoff_Date_Time == '2024-01-27 17:19:27') then MatchedRule matchedRule = new MatchedRule(); matchedRule.setRuleId("003"); matchedRule.setReason("Cashflow__Payment_Date == '2024-01-27' || Cashflow__STP_Cutoff_Date_Time == '2024-01-27 17:19:27'"); matchedRuleSet.add(matchedRule); end ``` </details> | 1. less transformations on rule 2. only one table to store user's input rule | 1. FE need synchronize DM if need 2. BE need synchronize DM if need |

# Operator Supported

We choose those from what drools supported.

For exact operator, please refer to wiki: [Drools Rule and Rule Builder Integration - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/Drools+Rule+and+Rule+Builder+Integration)

# Enhancement Design

## Rule Maintenance Status Machine

Running status: SAVE_CONFIRMED, DELETE_PENDING

Not Running status: status expect SAVE_CONFIRMED, DELETE_PENDING

# API Definition

refer to: [Rule Service Tech Design - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/Rule+Service+Tech+Design)   v2 API series

# UML Design

## Maintenance UML

Maker Action

Checker Action

Event Treatment

## Execution UML

# Removal Functionalities

## Scbml conversion

Next release, ratanone rule service will drop scbml conversion. instead, rule service will consume json format as request input

## Trade relative function

Current rule service contains many trade validation functionalities and replicate functions

Instead, rule service will support common function, which means requestor will also do adapt change.

## Old Specific Processor Refactor

Current rule service contains specific processor functions, these are not common at all. Also these need to be enhanced when the requirement changed.

**EXPAND: Previous Processor**

| RuleName | Description | Refactor Plan | Fact & Rule | New Design Solution |
| --- | --- | --- | --- | --- |
| badBusinessDayFactProcessor | 1. query static data service with (currency + date) 2. static data returns if currency + date is holiday | move to domain service | NA | NA |
| highValueFactProcessor | 1. retrieve currency & amount 2. query static data service with currency & amount, then get rate 3. calculate USD amount calculated 4. if result calcualted > 100000000 | 1 ~ 3 => move to domain service 4 => maintain in Rule Service | Fact: Cashflow.Cashflow_Amount Rule: Cashflow.Cashflow_Amount > 100000000 | { "businessFlow": "STRATEGIC_SETTLEMENT", "ruleType": "NSTP", "message": { "logicFacts": { "Entity": { "Counterparty_Is_Internal": [ "INTERNAL" ] } }, "additionalFacts": { "Cashflow":{ "Cashflow_Amount_Usd_Transfered": 100000000 } } } } |
| gsamClientFactProcessor | 1. ""retrieve Counterparty_SCI_FMID 2. query DA with Counterparty_SCI_FMID, then retrieve result fmEntity.legalEntity.operationStatus1Value 3. "REFER".equalsIgnoreCase(result) | 1 ~ 2 => move to domain service 3 => keep in Rule Service | Fact: Entity.legalEntity.operationStatus1Value Rule: Entity.legalEntity.operationStatus1Value matches 'REFER' | ```text { "businessFlow": "STRATEGIC_SETTLEMENT", "ruleType": "NSTP", "message": { "logicFacts": { "Entity": { "Counterparty_Is_Internal": [ "INTERNAL" ] } }, "additionalFacts": { "fmEntity": { "legalEntity": { "operationStatus1Value": "rEFER" } } } } } ``` |
| affirmationFactProcessor | 1. retrieve bookingEvent, eventReason 2. compare ~~"Amendment".equalsIgnoreCase(bookingEvent) &&~~ "Reversal".equalsIgnoreCase(eventReason) | 1 => move to domain service 2 => keep in Rule Service | | { "businessFlow": "STRATEGIC_SETTLEMENT", "ruleType": "NSTP", "message": { "logicFacts": { "Entity": { "Counterparty_Is_Internal": [ "INTERNAL" ] } }, "additionalFacts": { "Cashflow": { "Booking_System_Event": "Amendment", "Cashflow_Event_Reason": "Reversal" } } } } |
| corpClientFactProcessor | 1. retrieve Counterparty_SCI_FMID 2. query DA with Counterparty_SCI_FMID, then retrieve result fmEntity.fmAccount.fmType 3. "CORP".equalsIgnoreCase(result) | 1 ~ 2 => move to domain service 3 => keep in Rule Service | Fact: fmEntity.fmAccount.fmType Rule: fmEntity.fmAccount.fmType matches 'CORP' | ```text { "businessFlow": "STRATEGIC_SETTLEMENT", "ruleType": "NSTP", "message": { "logicFacts": { "Entity": { "Counterparty_Is_Internal": [ "INTERNAL" ] } }, "additionalFacts": { "fmEntity": { "fmAccount": { "fmType": "CORP" } } } } } ``` |
| backValueFactProcessor | 1. retrieve Cashflow.Payment_Date 2. format paymentDate with "yyyy-mm-dd" 3. get current system date as now 4. paymentDate.isBefore(now) | move to domain service | NA | |

**EXPAND_END**

## Special Rule

| Rule Type | Method | Notice | Status |
| --- | --- | --- | --- |
| Compare two fields user want to compare two fields values. | A.B == #C.D | 1. current we only support ==, != 2. fields should be only focus on logic model | Deployed under DEV VM |
| Compare same field in different input json | FactOne(Cashflow__Payment_Amount) == FactTwo(Cashflow__Payment_Amount) | 1. current we only support ==, != 2. fields should be only focus on logic model | Dev Done |

# Scbml Support Analyze

***Notice***:

1. v1 version let's keep as is. will be decommissioned in the future. If squad use v1, then migration from v1 to v2 should provide.
2. Ratan Rule Engine v1 v2 has huge difference from high level to low level. V1 won't be maintained from now.

| Solution | Pros | Cons | Notice |
| --- | --- | --- | --- |
| Client input Json | 1. Ratan Rule Engine will be light weight. 2. Customize rule can be defined (like: "fmEntity.fmAccount.fmType") 3. No external effort inside Ratan Rule Engine (no regression effort at all) | 1. each domain service maintain transformation | |
| Client input Scbml rule engine convert to json and using new way | 1. no more legacy code maintenance 2. using new design to process 3. migration to input Json way is very simple | 1. how to support customize rule like 'fmEntity.fmAccount.fmType == 'AAA'' is unclear 2. Ratan Rule Engine need maintain transformation logic internally (if using tl-model-client => rule engine need upgrade) 3. **tl-model-client can't support cashflow parsing** 4. Ratan Rule Engine Regression 1. Rule Engine Regression 2. Each Squad Regression (we need sign off) | tl-model-client 1. latest version 3.18.7(tds3 confirmed), local test => around 300ms 2. performance test => in progress 3. functional test => need test Rule Engine won't maintain an external mapping table |

# Performance

| Thread | Duration | Total Rule | Rule Filtered | Performance Result | Performance Detail |
| --- | --- | --- | --- | --- | --- |
| 2 | 5m | 7 settlement + nstp | 2 | 436/s no errors | <details> <summary>Expand Details</summary> ![image2024-2-29_11-21-29.png](attachments/image2024-2-29_11-21-29.png) </details> |
| | 5m | | | | |
| | | | | | |

# Dry Run Design

# Actions To Be Followed

Once refactored version is finished.

We must face following actions. (Till 2024-01-31)

| Priority | Description | Scope |
| --- | --- | --- |
| High | Rules migration | 1. BCS 2. CN 3. Trade Review |
| High | XML convert into Json | 1. BCS 2. CN 3. Trade Review |
| Medium | Trade relative function Trade Review squad need to refactor this part to their own domain service | Trade Review |
| Medium | Specific Processor Function CN Squad need move specific functions to their own domain service | CN |
| Medium | Drools Performance Enhancement | Rule Service |

# Reference

[Drools Documentation](https://docs.drools.org/7.74.1.Final/drools-docs/html_single/#drl-rules-WHEN-con_drl-rules)