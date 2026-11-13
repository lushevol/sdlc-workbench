# Backgroup & Purpose

1. currently **stamping nostro** need to support some **ways** are as follows: 1. use multi condition like **entity+ccy+settlementMeans+settlementAccount** to query static data(**default** behaviour in prod) 2. use **portfolio **and **ccy **to query static data(for **RFI**) 3. more demands and other conditions...
2. about support **RFI **case and more forthcomings **dedicated small quantity **nostro** **demands, we want to make the stamping **nostro** logic more **relevant universal **to meet more cases and **easy** to change, to let code **centralization **and **minimal **dependency, we choose put the match condition in ratan-cash-settlement-ssi-stamping-service

involving ssi can refer:  [SSI Relevant - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/SSI+Relevant#SSIRelevant-StampingInvolvingSystem)
more demands can refer:  [RFI Nostro stamping based on Portfolio - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/RFI+Nostro+stamping+based+on+Portfolio)

**EXPAND: more action need to do**

1. from walking through design and code we found there are many **duplicated** code and **tricky** code in existing project,
2. so **currently **we enhance minimum changing point, // **currently** we need to do
3. but for the **long term** we had better to do some **re-structure** to let it more changable and easy understand // **next step** we will do

**EXPAND_END**

**EXPAND: deprecated_design**

Proposal Compare

| | Choice | Description | UI page | User action for RFI | System changing | Advantage | Disadvantage |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Choice 1 | 1.**add rule page** 2.existing nostro UI page | 1.rule page** ![image-2026-1-7_11-40-42.png](attachments/image-2026-1-7_11-40-42.png) **2.nostro page** ![image-2026-1-7_11-40-23.png](attachments/image-2026-1-7_11-40-23.png)** | 1.**config **nostro for RFI **coexist **in same nostro UI page 2.**config **rule linking nostro above | 1.frontend create one rule UI page 2.backend 1) enhance stamping logic: a. **invoke rule** to dedide nostroId then to fetch nostro by id, if got then break b. use entity+ccy+settlementMeans+settlementAccount to fetch(**same as before**) | 1.flexibility and extension for forthcomings change 1) if user want to **add more** portfolio, they can change rule 2) config **any wildcard character** rule condition 3) if user want to use **other field**, they can **add new **rule linking other nostro | 1.involve one new rule page adding more non-convenience for user operation |
| 2 | Choice 2 | 1.enhance existing nostro UI page **adding** one **tab **for portfolio in existing nostro UI page | 1.nostro page with tab normal ![image-2026-1-7_11-39-38.png](attachments/image-2026-1-7_11-39-38.png) 2.nostro page with tab RFI ![image-2026-1-7_11-39-50.png](attachments/image-2026-1-7_11-39-50.png) | 1.**choose **normal type **or **RFI type 2.only need config **portofolio **and **ccy **column | 1.frontend 1) enhance nostro UI page adding tab and relevent column need to consider code changing complexity 2.backend 1) enhance static system a. add **two column** for nostro, nostroType and portfolio, b. consider existing calling client interface compatibility c. add interface fetching data by new type and condition 2) enhance ssi stamping logic a. use **portfolio+ccy** to fetch if got then break b. use entity+ccy+settlementMeans+settlementAccount+**default** to fetch or put all params to let static-service decide fetching sequence **quesiton**: 1. need prioritize fetching sequence, for normal, RFI, other Field // currently RFI>normal 2.if support one nostro support multi type? // do not sure further demand 3.we cannot predict enough condition, like portofolio is portfolio+ccy, other filed maybe need other field+ccy? or we can let the new field more common can indicate any thing, but if user want to add other field, we need do other enhancement // do not sure further demand 4.how to consider refresh for RFI? refer: [SSI Relevant - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/SSI+Relevant#SSIRelevant-Nostrorefresh) // may refresh more than expected 5.unique key will change to entity+ccy+settlementMeans+settlementAccount+**portofolio**? // yes | 1.maintain in existing one page | 1.only can support **exactly match **condition fetching 2.may **add **a **great many **of **item **if there are many portfolios 3.will **add other type, column **and also need change code in path and ssi logic if need add new filed 4.hard code portofolio path in project 5.**lose **some performance, since we need first use RFI condition then use other type condition finally use default condition 6.need to change existing static fetching data logic, using entity+ccy+settlementMeans+settlementAccount+**default ** |
| 3 | Choice 3 | 1.enhance existing nostro UI page **adding** one column named **portofolio** | 1.nostro page adding one column **portofolio** ![image-2026-1-7_14-40-31.png](attachments/image-2026-1-7_14-40-31.png) | 1.besides all must field need filled, user need additional fill **portofolio** | 1.frontend 1) enhance nostro UI page adding one column need to consider code changing complexity 2.backend 1) enhance static system a. add **one column** named portfolio, b. enhance existing fetching data interface and make sure compatibility c. 2) enhance ssi stamping logic a. use **portfolio+ccy** to fetch if got then break b. use entity+ccy+settlementMeans+settlementAccount+**default** to fetch c.client need use portofolio filed indicate this nostro is dedicated | same above 1.all existing field and page do not affected 2.all restriction can keep | same above 1.maybe additionally add some not necessary field for RFI 2.affect existing data(entity+ccy+settlementMeans+settlementAccount), may generate duplicate for normal and RFI |
| 4 | Choice 4 | 1.**add** one nostro blotter page | 1.**normal **nostro page** ![image-2026-1-7_11-40-21.png](attachments/image-2026-1-7_11-40-21.png) **2.**RFO **nostro page** ![image-2026-1-7_11-40-23.png](attachments/image-2026-1-7_11-40-23.png)** | 1.config **new **nostro UI page | 1.frontend create a new nostro UI page 2.backend 1) enhance new nostro config 2) enhance ssi stamping logic a. use portfolio+ccy to fetch **in new nostro list ** if got break b. use entity+ccy+settlementMeans+settlementAccount+**default** to fetch | 1.**separate **page for RFI puropose [2.do](http://2.do) not have interaction effect especially do not affect refresh logic 3.we can treat this data as special nostro rule | above all additional info: 1.cannot see all nostro data in one page 2.need to enhance existing **refresh **logic to support using portofolio and ccy |
| 5 | **Conclusion** | from what discussed mentioned above we can draw a **conclustion **that: actually ideally we expect **Choice 1** **but may be** user do not have various change on portofoli, **or** they only want to more convenience to see all thing in one UI page, **or **event new field is also limited in number, which means the case is **extremely small** **so**, **choice 3** seems suitable for current demands easy understand as before centre control in one place not involve other rule component but from changing effect and dedicated perspective, prefer Choice 4 seperate one blotter or tab for this dedicated nostro things do not affect any each other approach one place or dedicated management not involve other rule component action refer: )-,Proposal,-Proposals |

Rule UI Changing

| | change point | UI/column | description | |
| --- | --- | --- | --- | --- |
| 1 | rule config change | | **new one blotter: **Nostro Stamp Rules** new fields**: 1.NostroStaticId: **select **from nostro static config list 2.NostroId: for backend to fetch other considerations: 1.when we need **add** more **portfoli**, only need to change rule config. 2.when we need **add other types**, need update rule 3.when we need **other types for other nostro**, create other rule | |

Stamping Invocation Sequence Flow

**EXPAND_END**

# nvolving Changing Point

non-economic logic can refer:

**EXPAND: deprecated_design**

**EXPAND_END**

# Relationship between MatchCondition and Nostro

# Rule|MatchCondition&Nostro Maintain for RFI

## **MatchCondition Choices List:**

| | Choice | | Pros | Cros |
| --- | --- | --- | --- | --- |
| 1 | use rule-engine to decide if it is RFI first config rule | | 1.all rule config in one centralization place where it should be 2.official statndard logic model field 3.easy leverage existing business knowledge 4.only change db when new dedicated demand | 1. maybe have some missing // will reach out PO/CDUPS team supplement relevant logic model 2. need config many logic model field in "in" where clause if logic model is huge, which will lead complex rule **too long** to maintain // should be 3.slightly breakdown existing rule usage // this can be test and make compatibility 4.for trade, maximal case is need 4 rule, |
| 2 | use rule-engine to decide if it is RFI first config rule | | | |
| 3 | simulate rule in ssi-service | | 1.all logic in ssi-serice | 1.need do some code change if have new matchWay 2.logic the same as rule 3.many path need to config |
| 4 | **Conclusion**: 1 |

## **Nostro Changing:**

## Other Consideration

1. Why we choose DEDICATED_PORTFOLIO and DEDICATED_CURRENCY?
since currently for cashflow stamp we can use two specific path to extract data form cashflow xml,
**but **for trade, we have many **eight **product which have different path for currency and portfoli,
**so** we have to leverage existing code to pass the param what we need

2. Why we choose jsonb instead of child table?

| | Choice | Pros | Cros | |
| --- | --- | --- | --- | --- |
| 1 | use jsonb | 1.only one table easy to understand and maintain 2.keep compability for exisitng logic 3.easy extension for any field since it designed unstructured | involving new field in existing table | |
| 2 | use child table | 1.have seperate table maintain dedicated info | 1.not easy to extension, every adding new type like strategy, need add one column 2.every type data may have some blank value for other purpose 3.need change existing logic to meet compability 4.sql need to join to fetch data | |
| 3 | use child table with jsonb | as above choice2 | as above choice2 point 3&4 | |
| 4 | **Conclustion**: consider nostro data volumn is not huge and basic stable, and easy to understantd and maintain, lie RFI and other demand is belong to edge case, so we prefer chioce3 | |

3. **New **similar dedicated demand will involve **actions **we need to do like **strategy**:
1.let user give us strategy list  // **must**
2.let user give us match condition, RFI is portfolio+ccy  // **must**
3.initialize **nostro** static data base on step1  // **must****
**4.write **dedicate condition** into table base on step1&2  // **must
**5.pass **new** param condition match need at ratan-cash-settlement-ssi-stamping-service**
**

**Conclusion**:
**if **current nostro_table all field is enough(currently we provided **nostroType **and** dedicated_info**** **field for common)
**and**
all attribute value coming from cashflow or trade xml  // should be
we **do not** need to change any code **only** need to **add** rule script and **add** nostro data**
**for more **complex** case we need do some code change base on further design

**EXPAND: deprecated_design**

// rule

import com.scb.ratan.rule.drools.model.MatchedRule;

import com.scb.ratan.rule.drools.model.fact.EnhancedFact;

import java.time.*;

import java.util.*;

import static com.scb.ratan.rule.utils.CustomFunctionUtils.*;

dialect "java"

global java.util.List matchedRuleSet;

rule "7411243068010086400-0"

when

EnhancedFact( Portfolio__Booking_Entity_Trade_Portfolio_Name in ("111","222"), $portfolio: this.Portfolio__Booking_Entity_Trade_Portfolio_Name)

then

MatchedRule matchedRule = new MatchedRule();

matchedRule.setRuleId("7411243068010086400-0");

matchedRule.setReason("Portfolio__Booking_Entity_Trade_Portfolio_Name in (\"111\",\"222\")");

Map<String, String> matchData = new HashMap<>();

matchData.put("Portfolio__Booking_Entity_Trade_Portfolio_Name",$portfolio);

matchedRule.setMatchData(matchData);

matchedRuleSet.add(matchedRule);

end

rule "7411243068010086400-1"

when

EnhancedFact( Forward_Future_Instrument__Exchanged_Currency1_Payment_Amount_Currency == "NPR", $ccy: this.Forward_Future_Instrument__Exchanged_Currency1_Payment_Amount_Currency)

or

EnhancedFact( Forward_Future_Instrument__Exchanged_Currency2_Payment_Amount_Currency == "NPR", $ccy: this.Forward_Future_Instrument__Exchanged_Currency2_Payment_Amount_Currency)

then

MatchedRule matchedRule = new MatchedRule();

matchedRule.setRuleId("7411243068010086400-1");

matchedRule.setReason("Cashflow__Payment_Currency == \"USD\"");

Map<String, String> matchData = new HashMap<>();

matchData.put("Cashflow__Payment_Currency",$ccy);

matchedRule.setMatchData(matchData);

matchedRuleSet.add(matchedRule);

end

version2

version 3

version4

1. Why we choose this way to draw our rule:
for RFI case, we need to find 2 condition, one is portfolio the other is ccy, for cashflow xml we can easy to identify this currency using logic model Cashflow__Payment_Currency, but for trade we have many huge path need to identify , the **problem **is
curernt logic in ssi-service we **only **have currency **path **for various product but **do not have** any **logic model**, **but** for rule-engine depends on logic model field
so we have 2 choices:

| | Choice | Pros | Cros |
| --- | --- | --- | --- |
| 1 | find all logic model to match the relevant path, use official logic model to match in rule | a. official statndard field b. easy leverage existing business knowledge | a. maybe have some miss b. need config many logic model field in "in" where clause condition which will lead complex rule **too long** to maintain |
| 2 | use two **fixed customized** field to meet RFI case | a. only have two field easy to write rule and maintain [b.do](http://b.do) not consider any logic model in ssi-service keep as is | a. need to add more logic model field in rule-engine Fact, // maybe we can reuse some fixed fied to process this case, like **DEDICATED_NOSTRO_PORTFOLIO **and **DEDICATED_NOSTRO_CCY **b. need define new path for portfolio for cashflow/trade to fetch data c. if need some other fields in condition, we need add new field in rule-engine code which will lead some leading time |
| 3 | **Conclusion**: base on above analysis, from **standard **perspective and furthcomings maintain, prefer option1 from implement effort or risk, prefer option2 |

2. **New **similar dedicated demand will involve **actions **we need to do like **strategy**:
1.let user give us strategy list  // **must**
2.let user give us match condition, RFI is portfolio+ccy  // **must**
3.initialize nostro static data base on step1  // **must****
**4.write rule script base on step1&2  // **must
**5.add some new logic in ssi-service if there are some new logic or field need add // **optional
**

**Conclusion**:
**if **current nostro_table all field is enough(currently we provided **nostroType **and** dedicated_info**** **field for common)
**and**
all attribute value coming from cashflow or trade xml  // should be
we **do not** need to change any code **only** need to **add** rule script and **add** nostro data**
**for more **complex** case we need do some code change base on further design

version5:

version6

**EXPAND_END**

# Economic Logic Changing in Group Service

for "decide if RFI change logic" part
we can do **some **change in ratan-cash-settlement-ssi-stamping-service to return match data to let group-service know if this cashflow RFI has changed between before and now
for RFI case,
![image-2026-1-19_10-44-32.png](attachments/image-2026-1-19_10-44-32.png)
then group-service can concat above message to compare data between before and now

**EXPAND: old_version**

for "decide if RFI change logic" part
we can do **some **change in rule engine to **reduce** time **cost **when group-service invoke other service as "**old_version**"
for RFI case, now we can **only **invoke ratanone-rule-service to get below result rather than through long invocation chain
![image-2026-1-19_10-44-32.png](attachments/image-2026-1-19_10-44-32.png)

**EXPAND_END**

# Cashflow Stamping Internal Logic Flow

**EXPAND: deprecated_design**

**EXPAND_END**

# Trade Stamping Internal Logic Flow

# Changing Service List

| | service name | comment | PR | |
| --- | --- | --- | --- | --- |
| 1 | ratanone-static-data-service | provide api fetching nostro by **dedicated **condition change CRUD about nostro info | [Pull request 2307440: #11233640 stamp dedicated nostro - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-static-data-service/pullrequest/2307440) | |
| 2 | ~~ratanone-rule-service~~ | ~~provide batch validation for group-service to validation on non-economic case~~ ~~provide matchData for group to identify if change between before and now~~ | ~~[Pull request 2307443: #11233640 stamp dedicated nostro - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-rule-service/pullrequest/2307443)~~ | |
| 3 | ratan-cash-settlement-group-management-service | in amendment case, if meet non-economic conditoin will consider RFI change between before and now | [Pull request 2307438: #11233640 stamp dedicated nostro - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cash-settlement-group-management-service/pullrequest/2307438) | |
| 4 | ratan-cash-settlement-ssi-stamping-service | change being involved on dedicated case: 1.**remove **checking settlementAccout and means when adhoc 2.**change **existing nostro stamping step refer: | [Pull request 2307445: #11233640 stamp dedicated nostro - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cash-settlement-ssi-stamping-service/pullrequest/2307445) | |
| 5 | ratan-cash-settlement-query-service | new field Dedicated_Nostro_Id indicate if this cashflow hited dedicated rule | [Pull request 2314695: #11233640 flag - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cash-settlement-query-service/pullrequest/2314695) | |
| 6 | ~~ratan-cash-settlement-orchestration~~ ~~ratanone-foundation~~ | ~~optimize tech fail comment~~ ~~optimize ssi refresh comment~~ | ~~[Pull request 2307447: #11233640 stamp dedicated nostro - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratan-cash-settlement-orchestration/pullrequest/2307447)~~ ~~[Pull request 2307449: #11233640 stamp dedicated nostro - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-foundation/pullrequest/2307449)~~ | |

# API List

| | method | url | request | response | comment |
| --- | --- | --- | --- | --- | --- |
| 1 | `POST` | /v2/rules/action/create | { "businessFlow": "STRATEGIC_SETTLEMENT", "ruleType": "**NOSTRO_STAMP**", "reason": "3333", "rule": "Portfolio__Booking_Entity_Trade_Portfolio_Name == \"3333\"", "comment": "3333", "**metaData**": "{\"nostroConfig\":{\"nostroId\":\"3e763777-8811-4ee1-a4e6-fc3748c5666e\",\"nostroStaticId\":\"50300629\"}}" } | { "**id**": "7411243068010086400", "businessFlow": "STRATEGIC_SETTLEMENT", "ruleType": "NOSTRO_STAMP", "userRule": "Portfolio__Booking_Entity_Trade_Portfolio_Name == \"3333\"", "runningRule": "import com.scb.ratan.rule.drools.model.MatchedRule;\r\nimport com.scb.ratan.rule.drools.model.fact.EnhancedFact;\r\nimport java.time.*;\r\n\r\nimport static com.scb.ratan.rule.utils.CustomFunctionUtils.*;\r\n\r\ndialect \"java\"\r\n\r\nglobal java.util.List matchedRuleSet;\r\n\r\nrule \"7411243068010086400-0\"\r\n when\r\n EnhancedFact( Portfolio__Booking_Entity_Trade_Portfolio_Name == \"3333\" )\r\n then\r\n MatchedRule matchedRule = new MatchedRule();\r\n matchedRule.setRuleId(\"7411243068010086400-0\");\r\n matchedRule.setReason(\"Portfolio__Booking_Entity_Trade_Portfolio_Name == \\\"3333\\\"\");\r\n matchedRuleSet.add(matchedRule);\r\nend\r\n", "status": "PROCESSING", "reason": "3333", "**metaData**": "{\"nostroConfig\":{\"nostroId\":\"3e763777-8811-4ee1-a4e6-fc3748c5666e\",\"nostroStaticId\":\"50300629\"}}", "comment": "3333", "needDryRun": false, "version": 0, "createdAt": "2025-12-29T03:14:01.651271Z", "updatedAt": "2025-12-29T03:14:01.651271Z", "createdBy": "1111", "updatedBy": "1111" } | create **NOSTRO_STAMP **type rule |
| 2 | PUT | /v2/rules/action/update | same as above | same as above | update NOSTRO_STAMP type rule **same as above** |
| 3 | PUT | /v2/rules/action/confirm | {"ruleId":"7411248833593675776","comment":"111"} | { "id": "7411248833593675776", "businessFlow": "STRATEGIC_SETTLEMENT", "ruleType": "AUTO_NETTING", "userRule": "Portfolio__Booking_Entity_Trade_Portfolio_Name == \"1111\"", "runningRule": "import com.scb.ratan.rule.drools.model.MatchedRule;\r\nimport com.scb.ratan.rule.drools.model.fact.EnhancedFact;\r\nimport java.time.*;\r\n\r\nimport static com.scb.ratan.rule.utils.CustomFunctionUtils.*;\r\n\r\ndialect \"java\"\r\n\r\nglobal java.util.List matchedRuleSet;\r\n\r\nrule \"7411248833593675776-0\"\r\n when\r\n EnhancedFact( Portfolio__Booking_Entity_Trade_Portfolio_Name == \"1111\" )\r\n then\r\n MatchedRule matchedRule = new MatchedRule();\r\n matchedRule.setRuleId(\"7411248833593675776-0\");\r\n matchedRule.setReason(\"Portfolio__Booking_Entity_Trade_Portfolio_Name == \\\"1111\\\"\");\r\n matchedRuleSet.add(matchedRule);\r\nend\r\n", "**status**": "LIVE", "reason": "111122", "metaData": "{\"ruleUuid\":\"70a0c1e5-0e57-42f2-80fe-6739ad8caac4\",\"autoNettingConfig\":{\"nettingDate\":\"VD\",\"nettingTime\":\"00:30\",\"stpLevel\":\"NSTP_MAKER_CHECKER\",\"nettingType\":\"Bilateral Netting\"}}", "comment": "111", "needDryRun": false, "referenceRuleId": "7411242533224779776", "version": 2, "createdAt": "2025-12-29T03:36:56.27341Z", "updatedAt": "2025-12-29T03:38:59.773301115Z", "createdBy": "1434424", "updatedBy": "1492285" } | approve this rule **same as before** |
| 4 | PUT | /v2/rules/action/reject | {"ruleId":"7411248833593675776","comment":"2222"} | | reject this rule **same as before** |
| 5 | POST | [/api/ratan/stmcn/v1/cashflows](https://uklvadapp1346.uk.dev.net:8453/api/ratan/stmcn/v1/cashflows) | {"variables":{},"query":"{\n graphCashFlowDetails(cashflowIds: [\"M0Q45529653\"]) {\n cashflow {\n BCS_Parent_Trade_Id\n BCS_Trade_Id\n Delivery_Method\n Parent_Trade_Id\n Position_Id\n Settlement_Method\n Trade_Id\n Trade_State\n Trade_Version\n Trade_Original_Source_System_Name\n Trade_Date\n Cashflow {\n Cashflow_Id\n Cashflow_Business_Version\n **Dedicated_Nostro_Id**\n} {\n Affirmed_By\n Phone_Email\n Affirmed_At\n }\n }\n}"} | { "data": { "graphCashFlowDetails": [ { "cashflow": { "BCS_Parent_Trade_Id": "55529636", "BCS_Trade_Id": null, "Delivery_Method": "", "Parent_Trade_Id": "0", "Position_Id": "", "Settlement_Method": "Gross", "Trade_Id": "55529636", "Trade_State": "CONFIRMED", "Trade_Version": null, "Trade_Original_Source_System_Name": "", "Trade_Date": "2024-06-03", "Cashflow": { "Cashflow_Id": "M0Q45529653", "Cashflow_Business_Version": 0, "**Dedicated_Nostro_Id**": "1111111-b9f7ba8e-4ec4-40dc-965e-4a0c5bc39600", "Cashflow_Version": 0, "Cashflow_State": "WAITING", "Cashflow_Affirmation_Status": "Unaffirmed", "Cashflow_Event_Type": "New", "Cashflow_Minor_Version": 42, "Payment_Currency": "USD", "Payment_Date": "2025-11-06", "Payment_Type": "", "Payment_Cutoff_Time": "2025-11-05T13:00Z", "Pay_Receive_Indicator": "Pay", "Payment_Amount": "100.00", "Netting_Id": "", "Netting_Cuttoff_Date": null, "Payment_Receiver_Party_Reference": "party2", "Payment_Payer_Party_Reference": "party1", "Cashflow_Sub_State": "Pending Verification", "Cashflow_Sub_State_Type": "Pending Exception", "Cashflow_Sub_State_Updater": "System", "Status_Event_Type": "SsiStamped", "Event_Date": "2024-06-27", "Cashflow_Event_Reason": "Rebook", "Booking_System_Event": "ManualDeliver", "Cashflow_Swift_Message_Standard": null }, | |

**EXPAND: dedicated_design**

Relationship between MatchCondition and Nostro

choice1 use rule-engine+logic model field

Pros:
1.all rule config in one centralization place where it should be
2.easy leverage existing business knowledge
3.official statndard logic model field
4.only change db when new dedicated demand

Cors:
1. maybe have some missing  // will need PO/CDUPS team supplement relevant logic model
2.slightly breakdown existing rule usage  // this can be tested and make compatibility **after all** we only add one field

choice2 use rule-engine+
specifical field

cashflow same as above

Pros:
above 1&2
1.only one rule for every trade product
2.reduce invocation for every trade nostro stamp

Cors:
above 1&2
1.need code change for every new demand, like need other field, but we do not have any logic model field in rule-engine

Choice 5 logic in ssi-service + dedicated_currency

Pros:
all currency_tag only need one dedicatedCondtion record, reduce table size

**Cors**:
one thing is critial, if other demand like strategy, not only need CCY and other field, it also need the currency_tag to different, 
so this choice cannot considered

choice 6

| | Choice | |
| --- | --- | --- |
| 1 | **in-build** identify dedicated logic in ratan-cash-settlement-ssi-stamping-service | backgroud: for **cashflow **stamp, we only need **one times** stamp for **one** cashflow xml, meanwhile we only need one DedicatedMatchCondition for cashflow for **trade **stamp, we need maximal **four times** stamp for **one** trade xml in which **every** currency also have one **currencyTag** like UUID indicated current stamp action so we **prefer** to config different DedicatedMatchCondition for cashflow and trade stamp respectively and we have **stamp context** for each stamp: **messageType**(cashflow|trade)+**nostroType**(RFI|STRATEGY)+**currencyTag**(UUID) Pros: 1.**minimal **dependency, ssi-service do not depend on any other system like rule-engine 2.**centralization**, all logic in ratan-cash-settlement-ssi-stamping-service, code and config can change and understand in one place 3.**easy **change and extension and do not affect any other system 4.config **flexibility** do not have any restriction Cors: 1.need do some **code change** if have new matchWay, currently we suppose only support EQ and IN, or other complex condition 2.logic the same as config in rule-engine means **duplicated** effort also like point1 **only support simple** rule match 3.many path need to config do **not have** any **logic model** field concept |
| 2 | use rule-engine + logic model field + customize field | ![image-2026-1-22_11-29-37.png](attachments/image-2026-1-22_11-29-37.png) since in program existing fetching currency from different product, we can utilize this function to add one new customized logic model field DEDICATED_CURRENCY which can reduce rule script content length(do not depend on different logic model field for trade currency) Pros: 1.all identify rule script in **one** centralization place where it should be 2.leverage **existing business** knowledge 3.official **statndard** logic model field 4.**only change db** when new dedicated demand Cors: 1.slightly **breakdown **existing rule usage // this can be tested and make compatibility **after all** we only add one field 2.involve **other **system dependency, have some **risk **when rule-engine not work // seems meed microsoft funciton and responsibility respectively 3.adding **burden **traffic for rule-engine |
| 3 | **Conclusion**: from **reduce** duplicated effort perspective, since we have already built rule-engine which responsibility is to decide if some condition is match, so we prefer use it instead of build duplicated effort in ssi-service from **abandant** match ability perspective, rule-engine already built a suit of complex match ability while if built-in similar function in ssi-service will only provide simple feature from **self-management and visibility** perspective, if rule-engine is used for centralization and configed by **user**, we **should not** choice1 since it will configed by developer so we prefer built-in ability in ssi-service, which will let rulle-engine do not combine responsibility ~~considering some Corns we can:~~ ~~do full enough testing to ensure the minor changing in rule-engine~~ |

# Backgroup & Purpose

1. brief **backgroup**: need to stamp nostro for **RFI** case using **dedicated** nostro config
2. currently **stamping nostro** need to support some **ways** are as follows: 1. use multi condition like **entity+ccy+settlementMeans+settlementAccount** to query nostro data(**existing **behaviour in prod) 2. use **portfolio+****ccy **to query nostro data(for **RFI**) 3. more demands and other conditions...
3. for supporting **RFI **case and more forthcomings **dedicated small quantity **nostro** **demands, we want a. to make this stamping **nostro** logic more **relevant universal **to meet more cases and **easy** to change,

involving ssi can refer:  [SSI Relevant - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/SSI+Relevant#SSIRelevant-StampingInvolvingSystem)
more demands can refer:  [RFI Nostro stamping based on Portfolio - Derivative Strategy Projects - Confluence](https://confluence.global.standardchartered.com/display/DSP/RFI+Nostro+stamping+based+on+Portfolio)

**EXPAND: more action need to do**

1. from walking through design and code we found there are many **duplicated** code and **tricky** code in existing project,
2. so **currently **we enhance minimum changing point, // **currently** we need to do
3. but for the **long term** we had better to do some **re-structure** to let it more changable and easy understand // **next step** we will do

**EXPAND_END**

# Changing Point Invoved

non-economic logic can refer:

# Economic Logic Changing in Group Service

for "decide if dedicated info changed logic" part
return data sample
![image-2026-1-27_14-32-55.png](attachments/image-2026-1-27_14-32-55.png)
then group-service can concat above message to compare data between New and Withdrawal cashflow to **identify **if change has occurred

# Cashflow Stamping Logic Changing in SSI Service

# MatchCondition & Nostro Maintain

## **MatchCondition Choices**

| | Choice | |
| --- | --- | --- |
| 1 | **in-build** identify dedicated logic in ratan-cash-settlement-ssi-stamping-service | Pros: 1.**minimal **dependency, ratan-cash-settlement-ssi-stamping-service do not depend on any other system like rule-engine 2.**centralization**, all logic in ratan-cash-settlement-ssi-stamping-service, code and config can change and understand in one place 3.**easy **change and extension and do not affect any other system 4.config **flexibility** do not have any restriction, like some filed limitation in rule-engine Cors: 1.need do some **code change** if have new matchWay, currently we suppose **only **support EQ and IN 2.match logic the same as config in rule-engine means **duplicated** effort also like point1 **only support simple** rule match 3.many path need to config do **not have** any **logic model** field concept |
| 2 | use rule-engine + logic model field + customize field | ![image-2026-1-22_11-29-37.png](attachments/image-2026-1-22_11-29-37.png) Pros: 1.all identify rule script in **one** centralization place where it should be 2.leverage **existing business** knowledge 3.official **statndard** logic model field 4.**only change db** when new dedicated demand Cors: 1.slightly **breakdown **existing rule usage // this can be tested and make compatibility **after all** we only add one field 2.involve **other **system dependency, have some **risk **when rule-engine not work // seems meed microsoft funciton and responsibility respectively 3.adding **burden **traffic for rule-engine |
| 3 | **Conclusion**: from **reduce** duplicated effort perspective, since we have already built rule-engine which responsibility is to decide if some condition is match, so we prefer use it instead of build duplicated effort in ssi-service from **abandant** match ability perspective, rule-engine already built a suit of complex match ability while if built-in similar function in ssi-service will only provide simple feature from **self-management and visibility** perspective, if rule-engine is used for centralization and configed by **user**, we **should not** choice1 since it will configed by developer so we prefer built-in ability in ssi-service, which will let rulle-engine do not combine responsibility ~~considering some Corns we can:~~ ~~do full enough testing to ensure the minor changing in rule-engine~~ |

choice7

**EXPAND_END**

**EXPAND: dedicated_design**

Trade Stamping Logic Changing in SSI Service

**EXPAND_END**