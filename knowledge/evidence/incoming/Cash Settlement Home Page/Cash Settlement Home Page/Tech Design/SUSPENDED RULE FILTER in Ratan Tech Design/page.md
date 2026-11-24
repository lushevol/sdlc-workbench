# Background

Currently, SUSPENDED cashflow status is handled uniformly without distinguishing business rules. As the requirement evolves, SUSPENDED logic needs to be customizable and rule-driven, so it will be migrated to Ratan.

# Requirements

When a cashflow message (from either SCBML or Uber source) carries a SUSPENDED status, the system should:

Invoke Ratan Rule Service to evaluate whether the cashflow satisfies the SUSPENDED rule.
If the rule matches: mark the cashflow group message as SUSPENDED, persist it to ratan_cashflow_group_message, and stop all further processing (no GroupReadyEvent, no STP publish).
If the rule does not match: continue with the existing normal flow.

REQUIREMENTS PAGE  :  [SUSPENDED vs PROJECTED cashflow status in Ratan - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/SUSPENDED+vs+PROJECTED+cashflow+status+in+Ratan)

# Solution Design

Two implementation options are proposed. Background and requirements are identical for both; they differ only in where the SUSPENDED rule check is performed.

## Proposed 1 — Camunda Workflow Layer** (implemented)**

Conclusion: No changes to cash-settlement-group-management-service handler logic. SUSPENDED rule check is implement in rule Service  Camunda call it , executed after the full group message processing is complete.

![image-2026-4-23_12-14-57.png](attachments/image-2026-4-23_12-14-57.png)

### Scope

| Service | Change Type |
| --- | --- |
| `ratan-cash-settlement-orchestration` | BPMN: 1. add FxReplication Rule Check Moudle 2. add Status Update to RATAN_SUSPENDED Moudle |
| lifecycle-service | Add Ratan_Supened Action and RATAN_SUSPENDED status |
| `ratan-rule-service` | Add 1 new REST endpoints |
| db Migration | Insert 1 rule sql |

### rule-service Change

1.New Endpoint In Rule-Service:
- POST /v1/ratanSuspendedRule/check

2.Rule Service Logic :
##

### lifecycle-service change design

| scope | change | | |
| --- | --- | --- | --- |
| CashflowEnumAction.java | ADD : Ratan_Suspend | | |
| CashflowEnumMainStatus.java | ADD : RATAN_SUSPENDED | | |
| CashflowStatus.java | ADD :public static CashflowStatus RatanSuspended = new CashflowStatus( CashflowEnumMainStatus.RATAN_SUSPENDED, CashflowEnumSubStatus.NA, CashflowEnumSubStatusType.NA); | | |
| RatanSuspendedTransactionList.java (new file ： Path: lifecycle/domain/transaction/list/) | @Configuration public class RatanSuspendedTransactionList extends CashflowStatusTransactionList { @Override public void initCashflowStatusTransactionList() { this.setCashflowStatusTransaction(new ArrayList<>(Arrays.asList( CashflowStatusTransaction.builder() .previousStatus(CashflowStatus.RatanSuspended) .action(CashflowEnumAction.Withdrawal) .allowBusinessVersionUpgrade(true) .nextStatus(CashflowStatus.Cancelled) .build()))); } } | | |

## Proposed 2 - Standard Service Layer

### SCBML MSG Design

Option : After getOrSave()

Why : saves directly as SUSPENDED; no redundant PENDING write and follow-up process.

Conclusion: Check after getOrSave, before savePending.

### Uber MSG Design

Option : After Save Group

Why : saves directly as SUSPENDED; no redundant OFFSET and PENDING  write and follow-up process.

Conclusion: Check after Save Group, before offset.

### Suspended logic Design

Bief : Create isSuspend() function, The isSuspended() method applies a two-level check:

Why ：Level 1 is purely an optimization shortcut — it avoids a network call for the most common SUSPENDED case

``

## Proposed Comparison

| | Dimension | Proposed 1 — Camunda Workflow Layer | Proposed 2 — Group Service Layer | | --- | --- | --- | | **Interception point** | Inside Camunda BPMN `1_1_Cash_Settlement_Inbound.bpmn`, after group message processing completes | Before savePending() / offsetAndSaveGroupMessage(), inside MessageInboundEventHandler / BatchMessageInboundEventHandler | | **Change service** | add new endpoint in rule-service and update Camunda BPMN | update Group Service | | Transactional risk | **✅ Camunda delegate runs in separate thread, no transaction concern** | ⚠️ Feign call runs inside `@Transactional` scope; requires short timeout + fail-open （SCBML） | | Incomplete filtering risk | ✅ Each cashflow is an independent Camunda process instance — naturally isolated | ⚠️ complex logic in group service, easily leads to incomplete filter | | **Processing overhead** | ⚠️ Higher — cashflow fully processed through GroupService before Camunda intercepts | ✅ Low — stopped before offset/PENDING write | | **Deployment complexity** | BPMN and rule service endpoint | Support XCBML And Uber both filter | | |
| --- | --- |
| Dimension | Proposed 1 — Camunda Workflow Layer | Proposed 2 — Group Service Layer |
| **Interception point** | Inside Camunda BPMN `1_1_Cash_Settlement_Inbound.bpmn`, after group message processing completes | Before savePending() / offsetAndSaveGroupMessage(), inside MessageInboundEventHandler / BatchMessageInboundEventHandler |
| **Change service** | add new endpoint in rule-service and update Camunda BPMN | update Group Service |
| Transactional risk | **✅ Camunda delegate runs in separate thread, no transaction concern** | ⚠️ Feign call runs inside `@Transactional` scope; requires short timeout + fail-open （SCBML） |
| Incomplete filtering risk | ✅ Each cashflow is an independent Camunda process instance — naturally isolated | ⚠️ complex logic in group service, easily leads to incomplete filter |
| **Processing overhead** | ⚠️ Higher — cashflow fully processed through GroupService before Camunda intercepts | ✅ Low — stopped before offset/PENDING write |
| **Deployment complexity** | BPMN and rule service endpoint | Support XCBML And Uber both filter |

## SQL Design

SQL ：** FX replication Both rule and Cashflow rule, SUSPENDED Payment Type Fees**

```
INSERT INTO ratanone_rule_service.ratan_rule_engine
(id, business_flow, rule_type, user_rule, running_rule, status, reason, "comment", need_dry_run, reference_rule_id, created_at, updated_at, created_by, updated_by, "version", meta_data)
VALUES(
'7444684846945615873333',
'STRATEGIC_SETTLEMENT',
'RATAN_SUSPENDED',
'Data_Flow__Source_Stack_Flow_Name == "FMRPSTELLA" 
&& Entity__Booking_Entity_SCI_FMID != §Entity__Counterparty_SCI_FMID 
&& Entity__Counterparty_SCI_FMID not in ("401038280", "401038281", "400009154", "300079654", "300037428", "300037430", "401046131", "401045020", "401044980", "400036904", "400590585", "400915609") 
&& (Entity__Booking_Entity_SCI_FMID != "10075222" || Entity__Counterparty_SCI_FMID not in ("300010953", "300037151", "300037746")) 
&& (Entity__Booking_Entity_SCI_FMID != "2" || Entity__Counterparty_SCI_FMID not in ("400011374")) 
&& (Entity__Booking_Entity_SCI_FMID != "6" || Entity__Counterparty_SCI_FMID not in ("401059381", "401059382", "400003775")) 
&& (Entity__Booking_Entity_SCI_FMID != "4" || Entity__Counterparty_SCI_FMID not in ("400178086", "400178088", "400178085")) && (Entity__Booking_Entity_SCI_FMID != "400960089" || Entity__Counterparty_SCI_FMID not in ("401014976")) && (Entity__Booking_Entity_SCI_FMID != "400452428" || Entity__Counterparty_SCI_FMID not in ("400451508")) 
&& (Entity__Booking_Entity_SCI_FMID != "9" || Entity__Counterparty_SCI_FMID not in ("400038228")) 
&& Instrument_Common__ISDA_Taxonomy in ("ForeignExchange:Spot", "ForeignExchange:Forward", "ForeignExchange:Swap") 
&& Is_Duplicate_Booking != true && Entity__Booking_Entity_SCI_FMID not in ("401036553", "400991880", "400007847") 
&& (Contract_Typology not in ("FX_DCD", "FX_PCD", "FX_PCD_AXKI", "FX_PCD_DIF") || Parent_Position_Id == null || Parent_Position_Id == "" || (Entity__Counterparty_Country_ISO_Code != "JE" 
&& Entity__Counterparty_SCI_FMID in ("400001378", "10020899", "235003861", "10078716", "10036642", "10062461", "10032025", "400054708", "400054737", "400054741", "400057714", "400075752", "400085753", "400090093", "400095464", "400130180", "400130178", "400185419", "400193370", "400209000", "400218197", "400220273", "400229749", "400516443", "400516442", "400667486", "400677737", "400683682", "400798477", "400899993", "300036368", "3", "400452428", "400451508", "4", "400960089", "9", "400093619", "400041070", "10075222", "400906330", "401053411", "5", "400045551", "8", "300089409", "10036428", "10036382", "400032489", "2", "300011345", "300075472", "6", "10038345", "1003665", "10036775", "400825315", "10041902", "400823482", "7"))) 
&& (Cashflow__Payment_Type == null || !(Cashflow__Payment_Type matches "(?i).*fee.*"))',
'import com.scb.ratan.rule.drools.model.MatchedRule;
import com.scb.ratan.rule.drools.model.fact.EnhancedFact;
import java.time.*;

import static com.scb.ratan.rule.utils.CustomFunctionUtils.*;

dialect "java"

global java.util.List matchedRuleSet;

rule "7444684846945615873333-0"
    when
        EnhancedFact( Data_Flow__Source_Stack_Flow_Name == "FMRPSTELLA" )
    then
        MatchedRule matchedRule = new MatchedRule();
        matchedRule.setRuleId("7444684846945615873333-0");
        matchedRule.setReason("Data_Flow__Source_Stack_Flow_Name == \"FMRPSTELLA\"");
        matchedRuleSet.add(matchedRule);
end

rule "7444684846945615873333-1"
    when
        EnhancedFact( Entity__Booking_Entity_SCI_FMID != Entity__Counterparty_SCI_FMID )
    then
        MatchedRule matchedRule = new MatchedRule();
        matchedRule.setRuleId("7444684846945615873333-1");
        matchedRule.setReason("Entity__Booking_Entity_SCI_FMID != §Entity__Counterparty_SCI_FMID");
        matchedRuleSet.add(matchedRule);
end

rule "7444684846945615873333-2"
    when
        EnhancedFact( Entity__Counterparty_SCI_FMID not in ("401038280", "401038281", "400009154", "300079654", "300037428", "300037430", "401046131", "401045020", "401044980", "400036904", "400590585", "400915609") )
    then
        MatchedRule matchedRule = new MatchedRule();
        matchedRule.setRuleId("7444684846945615873333-2");
        matchedRule.setReason("Entity__Counterparty_SCI_FMID not in (\"401038280\", \"401038281\", \"400009154\", \"300079654\", \"300037428\", \"300037430\", \"401046131\", \"401045020\", \"401044980\", \"400036904\", \"400590585\", \"400915609\")");
        matchedRuleSet.add(matchedRule);
end

rule "7444684846945615873333-3"
    when
        EnhancedFact( (Entity__Booking_Entity_SCI_FMID != "10075222" || Entity__Counterparty_SCI_FMID not in ("300010953", "300037151", "300037746")) )
    then
        MatchedRule matchedRule = new MatchedRule();
        matchedRule.setRuleId("7444684846945615873333-3");
        matchedRule.setReason("(Entity__Booking_Entity_SCI_FMID != \"10075222\" || Entity__Counterparty_SCI_FMID not in (\"300010953\", \"300037151\", \"300037746\"))");
        matchedRuleSet.add(matchedRule);
end

rule "7444684846945615873333-4"
    when
        EnhancedFact( (Entity__Booking_Entity_SCI_FMID != "2" || Entity__Counterparty_SCI_FMID not in ("400011374")) )
    then
        MatchedRule matchedRule = new MatchedRule();
        matchedRule.setRuleId("7444684846945615873333-4");
        matchedRule.setReason("(Entity__Booking_Entity_SCI_FMID != \"2\" || Entity__Counterparty_SCI_FMID not in (\"400011374\"))");
        matchedRuleSet.add(matchedRule);
end

rule "7444684846945615873333-5"
    when
        EnhancedFact( (Entity__Booking_Entity_SCI_FMID != "6" || Entity__Counterparty_SCI_FMID not in ("401059381", "401059382", "400003775")) )
    then
        MatchedRule matchedRule = new MatchedRule();
        matchedRule.setRuleId("7444684846945615873333-5");
        matchedRule.setReason("(Entity__Booking_Entity_SCI_FMID != \"6\" || Entity__Counterparty_SCI_FMID not in (\"401059381\", \"401059382\", \"400003775\"))");
        matchedRuleSet.add(matchedRule);
end

rule "7444684846945615873333-6"
    when
        EnhancedFact( (Entity__Booking_Entity_SCI_FMID != "4" || Entity__Counterparty_SCI_FMID not in ("400178086", "400178088", "400178085")) )
    then
        MatchedRule matchedRule = new MatchedRule();
        matchedRule.setRuleId("7444684846945615873333-6");
        matchedRule.setReason("(Entity__Booking_Entity_SCI_FMID != \"4\" || Entity__Counterparty_SCI_FMID not in (\"400178086\", \"400178088\", \"400178085\"))");
        matchedRuleSet.add(matchedRule);
end

rule "7444684846945615873333-7"
    when
        EnhancedFact( (Entity__Booking_Entity_SCI_FMID != "400960089" || Entity__Counterparty_SCI_FMID not in ("401014976")) )
    then
        MatchedRule matchedRule = new MatchedRule();
        matchedRule.setRuleId("7444684846945615873333-7");
        matchedRule.setReason("(Entity__Booking_Entity_SCI_FMID != \"400960089\" || Entity__Counterparty_SCI_FMID not in (\"401014976\"))");
        matchedRuleSet.add(matchedRule);
end

rule "7444684846945615873333-8"
    when
        EnhancedFact( (Entity__Booking_Entity_SCI_FMID != "400452428" || Entity__Counterparty_SCI_FMID not in ("400451508")) )
    then
        MatchedRule matchedRule = new MatchedRule();
        matchedRule.setRuleId("7444684846945615873333-8");
        matchedRule.setReason("(Entity__Booking_Entity_SCI_FMID != \"400452428\" || Entity__Counterparty_SCI_FMID not in (\"400451508\"))");
        matchedRuleSet.add(matchedRule);
end

rule "7444684846945615873333-9"
    when
        EnhancedFact( (Entity__Booking_Entity_SCI_FMID != "9" || Entity__Counterparty_SCI_FMID not in ("400038228")) )
    then
        MatchedRule matchedRule = new MatchedRule();
        matchedRule.setRuleId("7444684846945615873333-9");
        matchedRule.setReason("(Entity__Booking_Entity_SCI_FMID != \"9\" || Entity__Counterparty_SCI_FMID not in (\"400038228\"))");
        matchedRuleSet.add(matchedRule);
end

rule "7444684846945615873333-10"
    when
        EnhancedFact( Instrument_Common__ISDA_Taxonomy in ("ForeignExchange:Spot", "ForeignExchange:Forward", "ForeignExchange:Swap") )
    then
        MatchedRule matchedRule = new MatchedRule();
        matchedRule.setRuleId("7444684846945615873333-10");
        matchedRule.setReason("Instrument_Common__ISDA_Taxonomy in (\"ForeignExchange:Spot\", \"ForeignExchange:Forward\", \"ForeignExchange:Swap\")");
        matchedRuleSet.add(matchedRule);
end

rule "7444684846945615873333-11"
    when
        EnhancedFact( Is_Duplicate_Booking != true )
    then
        MatchedRule matchedRule = new MatchedRule();
        matchedRule.setRuleId("7444684846945615873333-11");
        matchedRule.setReason("Is_Duplicate_Booking != true");
        matchedRuleSet.add(matchedRule);
end

rule "7444684846945615873333-12"
    when
        EnhancedFact( Entity__Booking_Entity_SCI_FMID not in ("401036553", "400991880", "400007847") )
    then
        MatchedRule matchedRule = new MatchedRule();
        matchedRule.setRuleId("7444684846945615873333-12");
        matchedRule.setReason("Entity__Booking_Entity_SCI_FMID not in (\"401036553\", \"400991880\", \"400007847\")");
        matchedRuleSet.add(matchedRule);
end

rule "7444684846945615873333-13"
    when
        EnhancedFact( (Contract_Typology not in ("FX_DCD", "FX_PCD", "FX_PCD_AXKI", "FX_PCD_DIF") || Parent_Position_Id == null || Parent_Position_Id == "" || (Entity__Counterparty_Country_ISO_Code != "JE" && Entity__Counterparty_SCI_FMID in ("400001378", "10020899", "235003861", "10078716", "10036642", "10062461", "10032025", "400054708", "400054737", "400054741", "400057714", "400075752", "400085753", "400090093", "400095464", "400130180", "400130178", "400185419", "400193370", "400209000", "400218197", "400220273", "400229749", "400516443", "400516442", "400667486", "400677737", "400683682", "400798477", "400899993", "300036368", "3", "400452428", "400451508", "4", "400960089", "9", "400093619", "400041070", "10075222", "400906330", "401053411", "5", "400045551", "8", "300089409", "10036428", "10036382", "400032489", "2", "300011345", "300075472", "6", "10038345", "1003665", "10036775", "400825315", "10041902", "400823482", "7"))) )
    then
        MatchedRule matchedRule = new MatchedRule();
        matchedRule.setRuleId("7444684846945615873333-13");
        matchedRule.setReason("(Contract_Typology not in (\"FX_DCD\", \"FX_PCD\", \"FX_PCD_AXKI\", \"FX_PCD_DIF\") || Parent_Position_Id == null || Parent_Position_Id == \"\" || (Entity__Counterparty_Country_ISO_Code != \"JE\" && Entity__Counterparty_SCI_FMID in (\"400001378\", \"10020899\", \"235003861\", \"10078716\", \"10036642\", \"10062461\", \"10032025\", \"400054708\", \"400054737\", \"400054741\", \"400057714\", \"400075752\", \"400085753\", \"400090093\", \"400095464\", \"400130180\", \"400130178\", \"400185419\", \"400193370\", \"400209000\", \"400218197\", \"400220273\", \"400229749\", \"400516443\", \"400516442\", \"400667486\", \"400677737\", \"400683682\", \"400798477\", \"400899993\", \"300036368\", \"3\", \"400452428\", \"400451508\", \"4\", \"400960089\", \"9\", \"400093619\", \"400041070\", \"10075222\", \"400906330\", \"401053411\", \"5\", \"400045551\", \"8\", \"300089409\", \"10036428\", \"10036382\", \"400032489\", \"2\", \"300011345\", \"300075472\", \"6\", \"10038345\", \"1003665\", \"10036775\", \"400825315\", \"10041902\", \"400823482\", \"7\")))");
        matchedRuleSet.add(matchedRule);
end

rule "7444684846945615873333-14"
    when
        EnhancedFact( Cashflow__Payment_Type == null || !(Cashflow__Payment_Type matches "(?i).*fee.*") )
    then
        MatchedRule matchedRule = new MatchedRule();
        matchedRule.setRuleId("7444684846945615873333-14");
        matchedRule.setReason("Cashflow__Payment_Type == null || !(Cashflow__Payment_Type matches \"(?i).*fee.*\")");
        matchedRuleSet.add(matchedRule);
end
',
'LIVE',
'FX Replication Rule for Global Rates',
'',
false,
'7444553081115459584',
'2026-03-31 09:59:43.067',
'2026-03-31 10:00:45.936',
'1376592',
'1376592',
2,
'{"autoClose":true}'
);
```

**Code change : ValidationRequestV2.RuleType**

```
// ValidationRequestV2.java
public enum RuleType {
    TRADE_VALIDATION,    
    RATAN_SUSPENDED           // [NEW] SQL 1,2 — RATAN_SUSPENDED 
}
```

# Error Log Monitoring

| Scenario | Handling |
| --- | --- |
| Rule service timeout/unavailable | Catch exception, log warning, `return false` (fail-open — continue normal flow) |
| Rule service returns empty `matchedRules` | Not suspended, continue normal flow |
| Rule service returns unexpected error | Log error, `return false` (fail-open) |

# verification

| Verification Item | Verification Method | Evidence screenshots | Result |
| --- | --- | --- | --- |
| RATAN_SUSPENDED FILTER | match suspended rule | ![image-2026-4-30_17-25-30.png](attachments/image-2026-4-30_17-25-30.png)![image-2026-4-30_17-26-22.png](attachments/image-2026-4-30_17-26-22.png) | **PASS** |
| PROCESSED | no match suspended rule | ![image-2026-4-30_17-19-39.png](attachments/image-2026-4-30_17-19-39.png) ![image-2026-4-30_17-23-0.png](attachments/image-2026-4-30_17-23-0.png) | **PASS** |
| | | | |