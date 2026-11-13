| | user operation | event_type | rule_status | action （from frontend) | rule_action |
| --- | --- | --- | --- | --- | --- |
| create | maker create | SAVE | ADD_PENDING | | |
| checker approve | CONFIRM | LIVE | confirm | create_confirm |
| checker reject | REMOVE | DEAD | reject | |
| update | maker update | CONFIRM(old) | LIVE | update | |
| SAVE(new) | UPDATE_PENDING | | |
| checker approve | REMOVE(old) | DEAD | | |
| CONFIRM(new) | LIVE | confirm | update_confirm |
| checker reject | REMOVE(new) | DEAD | reject | |
| enable | enable | CONFIRM | LIVE | enable | enable |
| disable | disable | REMOVE | DISABLED | disable | disable |
| delete | delete | REMOVE | DEAD | null | null |

add_pending:

{
  "type": "SAVE",
  "ruleScript": "import com.scb.ratan.rule.drools.model.MatchedRule;\r\nimport com.scb.ratan.rule.drools.model.fact.EnhancedFact;\r\nimport java.time.*;\r\n\r\nimport static com.scb.ratan.rule.utils.CustomFunctionUtils.*;\r\n\r\ndialect \"java\"\r\n\r\nglobal java.util.List matchedRuleSet;\r\n\r\nrule \"7341393194514690048-0\"\r\n    when\r\n        EnhancedFact( BCS_Trade_Id == \"\" )\r\n    then\r\n        MatchedRule matchedRule = new MatchedRule();\r\n        matchedRule.setRuleId(\"7341393194514690048-0\");\r\n        matchedRule.setReason(\"BCS_Trade_Id == \\\"\\\"\");\r\n        matchedRuleSet.add(matchedRule);\r\nend\r\n",
  "userRule": "BCS_Trade_Id == \"\"",
  "scriptHashKey": "125667540420D695C8779900B11E7AA5F6E4800C468CEA896A4B57F14AD1FBD4",
  "ruleAdditionalInfo": {
    "ruleId": "7341393194514690048",
    "metadata": "{\"ruleUuid\":\"3cc5dff6-5c9e-42be-915a-74f2486f9896\",\"autoNettingConfig\":{\"nettingDate\":\"VD\",\"nettingTime\":\"00:00\",\"stpLevel\":\"NSTP_MAKER_CHECKER\",\"nettingType\":\"BIC Netting\"}}",
    "ruleStatus": "ADD_PENDING"
  },
  "businessFlow": "STRATEGIC_SETTLEMENT",
  "ruleType": "AUTO_NETTING"
}

add:

{
  "type": "CONFIRM",
  "ruleScript": "import com.scb.ratan.rule.drools.model.MatchedRule;\r\nimport com.scb.ratan.rule.drools.model.fact.EnhancedFact;\r\nimport java.time.*;\r\n\r\nimport static com.scb.ratan.rule.utils.CustomFunctionUtils.*;\r\n\r\ndialect \"java\"\r\n\r\nglobal java.util.List matchedRuleSet;\r\n\r\nrule \"7341393194514690048-0\"\r\n    when\r\n        EnhancedFact( BCS_Trade_Id == \"\" )\r\n    then\r\n        MatchedRule matchedRule = new MatchedRule();\r\n        matchedRule.setRuleId(\"7341393194514690048-0\");\r\n        matchedRule.setReason(\"BCS_Trade_Id == \\\"\\\"\");\r\n        matchedRuleSet.add(matchedRule);\r\nend\r\n",
  "userRule": "BCS_Trade_Id == \"\"",
  "scriptHashKey": "125667540420D695C8779900B11E7AA5F6E4800C468CEA896A4B57F14AD1FBD4",
  "ruleAdditionalInfo": {
    "ruleId": "7341393194514690048",
    "metadata": "{\"ruleUuid\":\"3cc5dff6-5c9e-42be-915a-74f2486f9896\",\"autoNettingConfig\":{\"nettingDate\":\"VD\",\"nettingTime\":\"00:00\",\"stpLevel\":\"NSTP_MAKER_CHECKER\",\"nettingType\":\"BIC Netting\"}}",
    "ruleStatus": "LIVE"
  },
  "businessFlow": "STRATEGIC_SETTLEMENT",
  "ruleType": "AUTO_NETTING",
  "rule_action": "confirm"
}

update_pending:

{
  "type": "CONFIRM",
  "ruleScript": "import com.scb.ratan.rule.drools.model.MatchedRule;\r\nimport com.scb.ratan.rule.drools.model.fact.EnhancedFact;\r\nimport java.time.*;\r\n\r\nimport static com.scb.ratan.rule.utils.CustomFunctionUtils.*;\r\n\r\ndialect \"java\"\r\n\r\nglobal java.util.List matchedRuleSet;\r\n\r\nrule \"7341393194514690048-0\"\r\n    when\r\n        EnhancedFact( BCS_Trade_Id == \"\" )\r\n    then\r\n        MatchedRule matchedRule = new MatchedRule();\r\n        matchedRule.setRuleId(\"7341393194514690048-0\");\r\n        matchedRule.setReason(\"BCS_Trade_Id == \\\"\\\"\");\r\n        matchedRuleSet.add(matchedRule);\r\nend\r\n",
  "userRule": "BCS_Trade_Id == \"\"",
  "scriptHashKey": "125667540420D695C8779900B11E7AA5F6E4800C468CEA896A4B57F14AD1FBD4",
  "ruleAdditionalInfo": {
    "ruleId": "7341393194514690048",
    "metadata": "{\"ruleUuid\":\"3cc5dff6-5c9e-42be-915a-74f2486f9896\",\"autoNettingConfig\":{\"nettingDate\":\"VD\",\"nettingTime\":\"00:00\",\"stpLevel\":\"NSTP_MAKER_CHECKER\",\"nettingType\":\"BIC Netting\"}}",
    "ruleStatus": "LIVE"
  },
  "businessFlow": "STRATEGIC_SETTLEMENT",
  "ruleType": "AUTO_NETTING",
  "rule_action": "update"
}

{
  "type": "SAVE",
  "ruleScript": "import com.scb.ratan.rule.drools.model.MatchedRule;\r\nimport com.scb.ratan.rule.drools.model.fact.EnhancedFact;\r\nimport java.time.*;\r\n\r\nimport static com.scb.ratan.rule.utils.CustomFunctionUtils.*;\r\n\r\ndialect \"java\"\r\n\r\nglobal java.util.List matchedRuleSet;\r\n\r\nrule \"7341393701123698688-0\"\r\n    when\r\n        EnhancedFact( BCS_Trade_Id == \"1233\" )\r\n    then\r\n        MatchedRule matchedRule = new MatchedRule();\r\n        matchedRule.setRuleId(\"7341393701123698688-0\");\r\n        matchedRule.setReason(\"BCS_Trade_Id == \\\"1233\\\"\");\r\n        matchedRuleSet.add(matchedRule);\r\nend\r\n",
  "userRule": "BCS_Trade_Id == \"1233\"",
  "scriptHashKey": "407B11EA93ED6CBDD7B1DE7AE44A5531A296D7D3CD716DB9E539E5B46E885FCC",
  "ruleAdditionalInfo": {
    "ruleId": "7341393701123698688",
    "referenceRuleId": "7341393194514690048",
    "metadata": "{\"ruleUuid\":\"3cc5dff6-5c9e-42be-915a-74f2486f9896\",\"autoNettingConfig\":{\"nettingDate\":\"VD\",\"nettingTime\":\"00:00\",\"stpLevel\":\"NSTP_MAKER_CHECKER\",\"nettingType\":\"SAL MTM Netting\"}}",
    "ruleStatus": "UPDATE_PENDING"
  },
  "businessFlow": "STRATEGIC_SETTLEMENT",
  "ruleType": "AUTO_NETTING"
}

update:

{
  "type": "REMOVE",
  "ruleScript": "import com.scb.ratan.rule.drools.model.MatchedRule;\r\nimport com.scb.ratan.rule.drools.model.fact.EnhancedFact;\r\nimport java.time.*;\r\n\r\nimport static com.scb.ratan.rule.utils.CustomFunctionUtils.*;\r\n\r\ndialect \"java\"\r\n\r\nglobal java.util.List matchedRuleSet;\r\n\r\nrule \"7341393194514690048-0\"\r\n    when\r\n        EnhancedFact( BCS_Trade_Id == \"\" )\r\n    then\r\n        MatchedRule matchedRule = new MatchedRule();\r\n        matchedRule.setRuleId(\"7341393194514690048-0\");\r\n        matchedRule.setReason(\"BCS_Trade_Id == \\\"\\\"\");\r\n        matchedRuleSet.add(matchedRule);\r\nend\r\n",
  "userRule": "BCS_Trade_Id == \"\"",
  "scriptHashKey": "125667540420D695C8779900B11E7AA5F6E4800C468CEA896A4B57F14AD1FBD4",
  "ruleAdditionalInfo": {
    "ruleId": "7341393194514690048",
    "metadata": "{\"ruleUuid\":\"3cc5dff6-5c9e-42be-915a-74f2486f9896\",\"autoNettingConfig\":{\"nettingDate\":\"VD\",\"nettingTime\":\"00:00\",\"stpLevel\":\"NSTP_MAKER_CHECKER\",\"nettingType\":\"BIC Netting\"}}",
    "ruleStatus": "DEAD"
  },
  "businessFlow": "STRATEGIC_SETTLEMENT",
  "ruleType": "AUTO_NETTING"
}

{
  "type": "CONFIRM",
  "ruleScript": "import com.scb.ratan.rule.drools.model.MatchedRule;\r\nimport com.scb.ratan.rule.drools.model.fact.EnhancedFact;\r\nimport java.time.*;\r\n\r\nimport static com.scb.ratan.rule.utils.CustomFunctionUtils.*;\r\n\r\ndialect \"java\"\r\n\r\nglobal java.util.List matchedRuleSet;\r\n\r\nrule \"7341393701123698688-0\"\r\n    when\r\n        EnhancedFact( BCS_Trade_Id == \"1233\" )\r\n    then\r\n        MatchedRule matchedRule = new MatchedRule();\r\n        matchedRule.setRuleId(\"7341393701123698688-0\");\r\n        matchedRule.setReason(\"BCS_Trade_Id == \\\"1233\\\"\");\r\n        matchedRuleSet.add(matchedRule);\r\nend\r\n",
  "userRule": "BCS_Trade_Id == \"1233\"",
  "scriptHashKey": "407B11EA93ED6CBDD7B1DE7AE44A5531A296D7D3CD716DB9E539E5B46E885FCC",
  "ruleAdditionalInfo": {
    "ruleId": "7341393701123698688",
    "referenceRuleId": "7341393194514690048",
    "metadata": "{\"ruleUuid\":\"3cc5dff6-5c9e-42be-915a-74f2486f9896\",\"autoNettingConfig\":{\"nettingDate\":\"VD\",\"nettingTime\":\"00:00\",\"stpLevel\":\"NSTP_MAKER_CHECKER\",\"nettingType\":\"SAL MTM Netting\"}}",
    "ruleStatus": "LIVE"
  },
  "businessFlow": "STRATEGIC_SETTLEMENT",
  "ruleType": "AUTO_NETTING",
  "rule_action": "confirm"
}

enable:

{
  "type": "CONFIRM",
  "ruleScript": "import com.scb.ratan.rule.drools.model.MatchedRule;\r\nimport com.scb.ratan.rule.drools.model.fact.EnhancedFact;\r\nimport java.time.*;\r\n\r\nimport static com.scb.ratan.rule.utils.CustomFunctionUtils.*;\r\n\r\ndialect \"java\"\r\n\r\nglobal java.util.List matchedRuleSet;\r\n\r\nrule \"7341393701123698688-0\"\r\n    when\r\n        EnhancedFact( BCS_Trade_Id == \"1233\" )\r\n    then\r\n        MatchedRule matchedRule = new MatchedRule();\r\n        matchedRule.setRuleId(\"7341393701123698688-0\");\r\n        matchedRule.setReason(\"BCS_Trade_Id == \\\"1233\\\"\");\r\n        matchedRuleSet.add(matchedRule);\r\nend\r\n",
  "userRule": "BCS_Trade_Id == \"1233\"",
  "scriptHashKey": "407B11EA93ED6CBDD7B1DE7AE44A5531A296D7D3CD716DB9E539E5B46E885FCC",
  "ruleAdditionalInfo": {
    "ruleId": "7341393701123698688",
    "referenceRuleId": "7341393194514690048",
    "metadata": "{\"ruleUuid\":\"3cc5dff6-5c9e-42be-915a-74f2486f9896\",\"autoNettingConfig\":{\"nettingDate\":\"VD\",\"nettingTime\":\"00:00\",\"stpLevel\":\"NSTP_MAKER_CHECKER\",\"nettingType\":\"SAL MTM Netting\"}}",
    "ruleStatus": "LIVE"
  },
  "businessFlow": "STRATEGIC_SETTLEMENT",
  "ruleType": "AUTO_NETTING",
  "rule_action": "enable"
}

#### **disable:**

{
  "type": "REMOVE",
  "ruleScript": "import com.scb.ratan.rule.drools.model.MatchedRule;\r\nimport com.scb.ratan.rule.drools.model.fact.EnhancedFact;\r\nimport java.time.*;\r\n\r\nimport static com.scb.ratan.rule.utils.CustomFunctionUtils.*;\r\n\r\ndialect \"java\"\r\n\r\nglobal java.util.List matchedRuleSet;\r\n\r\nrule \"7341393701123698688-0\"\r\n    when\r\n        EnhancedFact( BCS_Trade_Id == \"1233\" )\r\n    then\r\n        MatchedRule matchedRule = new MatchedRule();\r\n        matchedRule.setRuleId(\"7341393701123698688-0\");\r\n        matchedRule.setReason(\"BCS_Trade_Id == \\\"1233\\\"\");\r\n        matchedRuleSet.add(matchedRule);\r\nend\r\n",
  "userRule": "BCS_Trade_Id == \"1233\"",
  "scriptHashKey": "407B11EA93ED6CBDD7B1DE7AE44A5531A296D7D3CD716DB9E539E5B46E885FCC",
  "ruleAdditionalInfo": {
    "ruleId": "7341393701123698688",
    "referenceRuleId": "7341393194514690048",
    "metadata": "{\"ruleUuid\":\"3cc5dff6-5c9e-42be-915a-74f2486f9896\",\"autoNettingConfig\":{\"nettingDate\":\"VD\",\"nettingTime\":\"00:00\",\"stpLevel\":\"NSTP_MAKER_CHECKER\",\"nettingType\":\"SAL MTM Netting\"}}",
    "ruleStatus": "DISABLED"
  },
  "businessFlow": "STRATEGIC_SETTLEMENT",
  "ruleType": "AUTO_NETTING",
  "rule_action": "disable"
}

**reject:**

{
  "type": "REMOVE",
  "ruleScript": "import com.scb.ratan.rule.drools.model.MatchedRule;\r\nimport com.scb.ratan.rule.drools.model.fact.EnhancedFact;\r\nimport java.time.*;\r\n\r\nimport static com.scb.ratan.rule.utils.CustomFunctionUtils.*;\r\n\r\ndialect \"java\"\r\n\r\nglobal java.util.List matchedRuleSet;\r\n\r\nrule \"7341394656200273920-0\"\r\n    when\r\n        EnhancedFact( BCS_Trade_Id == \"12\" )\r\n    then\r\n        MatchedRule matchedRule = new MatchedRule();\r\n        matchedRule.setRuleId(\"7341394656200273920-0\");\r\n        matchedRule.setReason(\"BCS_Trade_Id == \\\"12\\\"\");\r\n        matchedRuleSet.add(matchedRule);\r\nend\r\n",
  "userRule": "BCS_Trade_Id == \"12\"",
  "scriptHashKey": "FF37C4DF2DD5299D1AC8CE8FF9B97B7AD78EDB9D4428738A19FF6B5C96355103",
  "ruleAdditionalInfo": {
    "ruleId": "7341394656200273920",
    "referenceRuleId": "7341393701123698688",
    "metadata": "{\"ruleUuid\":\"3cc5dff6-5c9e-42be-915a-74f2486f9896\",\"autoNettingConfig\":{\"nettingDate\":\"VD\",\"nettingTime\":\"00:00\",\"stpLevel\":\"NSTP_MAKER_CHECKER\",\"nettingType\":\"SAL MTM Netting\"}}",
    "ruleStatus": "DEAD"
  },
  "businessFlow": "STRATEGIC_SETTLEMENT",
  "ruleType": "AUTO_NETTING",
  "rule_action": "reject"
}