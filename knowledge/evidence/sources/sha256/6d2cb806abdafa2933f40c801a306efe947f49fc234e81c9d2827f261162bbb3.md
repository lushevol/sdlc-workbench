# 1. Background

Currently there are three rule service components in ratanone platform, which includes ratan-rule-service (for CN rules), ratan-suppression-service (for BAU rules) and ratanone-rule-service (for FX-replication filtering rules & detective rules). The goal is to migrate ratan-rule-service and ratan-suppression-service to ratanone-rule-service, all of the rules should be maintained and validated in ratanone-rule-service. Hence, it's better to list out all of the differences and the integration points including database, service, API and UI level before the rule migration.

***AS-IS Diagram***

***To-be Diagram***

# 2. Database

## 2.1 Table Schema

As all of existing rules need to be moved from their own database schema to the ratanone-rule-service schema, we need to find out the changes to table schema across all the rule services and work out the solution to cater these changes.

- ***ratanone-suppression-service* vs *ratanone-rule-service***

| | ratanone.ratan_suppresion_rule | ratanone_rule_service.ratan_rule | |
| --- | --- | --- | --- |
| **Column Changed** | id (bigserial) | id (text) | Column type was changed from bigserial to text. |
| *business_workflow* | *business_flow* | Column name changed. |
| creator | created_by | Column name changed. |
| create_timestamp | created_at | Column name changed. |
| last_modifier | updated_by | Column name changed. |
| last_modify_timestamp | updated_at | Column name changed. |
| *hierarchy* | N/A | Removed. |
| *value_date* | N/A | Removed. |

***Questions***

1. Do we agree for the columns' name changes? ***Yes***
2. As for the columns removed, do we confirm that these columns are no longer used in the new rule service? ***Yes***

- ***ratan-rule-service vs ratanone-rule-service***

| | ratan_rule_service.ratan_rule | ratanone_rule_service.ratan_rule | |
| --- | --- | --- | --- |
| **Column Changed** | operation_level | N/A | Removed. |
| exception_code | N/A | Removed. |
| exception_category | N/A | Removed. |
| N/A | fact_processor | Add, a replacement for CN special rule processor. |

***      Questions***

1. As discussed before, the relationship of exception and rule shall not be maintained in the rule service? ***Yes***

## 2.2 Load rules from database

In ratanone rule service, all the rules are stored in the database tables. Once it needs to do the rule validation against the specified dataset, the corresponding rules shall be loaded from database by given parameters ***‘business_flow'*** and ***'rule_type'***. Consider migrating the existing rules that includes CN and BAU to the same table ***'ratanone_rule_service.ratan_rule'***, a new column is a must-have to differentiate which rules are applicable for CN, which are applicable for BAU etc.

- The following table shows all the BAU rules group by column*** 'business_workflow' ***and ***'rule_type'*** in UAT env:

| Item # | business_workflow | rule_type | num_of_rules |
| --- | --- | --- | --- |
| 1 | SETTLEMENT | nstp | 6 |
| 2 | SETTLEMENT | NULL | 11 |
| 3 | SETTLEMENT_AUTO_NETTING | netting | 2 |
| 4 | CONFIRMATION | NULL | 16 |

Query SQL:

***select sr.business_workflow, sr.rule_type, count(1) as num_of_rules from ratanone.ratan_suppression_rule sr ***
***  where sr.status = 'ADD_CONFIRMED' or sr.status = 'DEL_PEDNING' group by sr.business_workflow, sr.rule_type***;

- The CN rule groups are shown as below in UAT env:

| Item # | business_flow | rule_type | num_of_rules |
| --- | --- | --- | --- |
| 1 | STRATEGIC_SETTLEMENT | IRS | 1 |
| 2 | STRATEGIC_SETTLEMENT | NSTP | 23 |
| 3 | STRATEGIC_SETTLEMENT | NETTING | 2 |
| 4 | STRATEGIC_SETTLEMENT | SUPPRESSION | 29 |

Query SQL:

***select rr.business_flow, rr.rule_type, count(1) as num_of_rules from ratan_rule_service.ratan_rule rr ***
***    where rr.status = 'ADD_CONFIRMED' or rr.status = 'DEL_PEDNING' group by rr.business_flow, rr.rule_type;***

**Questions**

1. Are there all the groups for CN and BAU rules listed out above？

* BAU and CN need to provide the existing rules in PROD env with the format of the below sample.csv, then **@Lin Liang import into the rule service and generate the corresponding drools rule records in database.*

*          *
📎 [sample.csv](attachments/sample.csv)

2. Can we have the default value for column ***'rule_type'***?

*Yes.*

3. How do we differentiate the CN rules or BAU rules?

*Confirm to use the 'business flow' and 'rule type' to differentiate.*

# 3. Service

- ***BAU Rule Service List***

| Iteam # | Service Name | Remark |
| --- | --- | --- |
| 1 | Suppression Rule | Implement in ratanone-rule-service. |
| 2 | Netting Rule | Same as suppression rule, but the rule type is 'netting'. |
| 3 | Data Entitlement Rule | Consider as a standalone service, it won't migrate to the ratanone-rule-service. |
| 4 | Fileds | This service is used for enriching SCBML dataset before rule validation.* Consider moving outside or still part of ratanone-rule-service?* |

- ***CN Rule Service List***

| Item # | Service Name | Remark |
| --- | --- | --- |
| 1 | Suppression Rule | Check the logical model field 'Cashflow.Is_Cashflow_Unsuppress' to determine if trade is suppressed. |
| 2 | Special Rule | Fetching data from third-party service, implement in ratanone-rule-service. |
| 3 | IRS Rule | Additional rule check logic for this kind of rule before the rule validation. |
| 4 | Netting Rule | Additional rule check logic for this kind of rule before the rule validation. |
| 5 | NSTP Rule | Check if exceptions exist, if so, rule validation won't started. |
| 6 | Swift Suppression Rule | Same as Suppression Rule |
| 7 | ***Fields Xpath*** | *Same as BAU fields config service.* |
| 8 | ***Profile Limitation*** | Seems not the part of rule service. |
| 9 | ***Validation Rule*** | Rules for frontend logic validation. |

**Questions**

1. The*** fields service*** should be a part of rule service or not? It seems to me that*** fields service ***shall run as a standalone service.

*Yes, it is most likely to be part of static data service, hence this will be removed from rule service.*

2. The ***profile limitation service*** should be exclusive of rule service?

* In scope of Rule domain service.*

3. Whether the ***rule service*** include validation rules or not?

*No, as validation rules are used for frontend form validation. It shall be part of static data service.*

# 4. API

- ***CN Rule Service API***

| API Group | API Endpoint | Method | Remark |
| --- | --- | --- | --- |
| **Rule Maintenance** | /v1/rule/add | POST | Add a new rule. |
| /v1/nstpRule/addSpecial | POST | Add a new special rule. |
| /v1/nstpRule/SpecialConfig/{businessFlow} | POST | Special rule configuration by given business_flow. |
| /v1/rule/{businessFlow}/listAll | GET | List all the rules by given business_flow. |
| [/v1/rule/NSTP/listByType](http://v1/rule/NSTP/listByType) | GET | List all the nstp rules. |
| /v1/rule/SWIFT_SUPPRESSION/listByType | GET | List all the swift_suppression rules. |
| /v1/rule/SUPPRESSION/listByType | GET | List all the suppression rules. |
| /v1/rule/NETTING/listByType | GET | List all the netting rules. |
| /v1/rule/histories | GET | Get the histories of rules. |
| /v1/rule/{ruleId}/delete | DELETE | Delete the rule by given rule id. |
| /v1/rule/{ruleId}/delete/confirm | PUT | Confirm the deleted rule. |
| /v1/rule/{ruleId}/delete/cancel | PUT | Cancel the rule deletion. |
| ***Exception*** | /v1/nstpException/metaData | GET | Removed. |
| /v1/nstpException/actionData | GET | Removed. |
| ***Profile Limitation?*** | /v1/profileLimitation/create | POST | |
| /v1/profileLimitation/edit | PUT | |
| /v1/profileLimitation/{profile}/{currency} | DELETE | |
| /v1/profileLimitation/reject/{profile}/{currency}/{status} | PUT | |
| /v1/profileLimitation/confirm/{profile}/{currency}/{status} | PUT | |
| ***Fields*** | /v1/fields | GET | |
| /v1/fields/upload | PUT | |
| /v1/fields/export | GET | |
| /v1/fields/config/upload | PUT | |
| /v1/fields/versions | GET | |
| /v1/fields/versions/activate | GET | |
| /versions/{tableName}/{version}/active | PUT | |
| /v1/fields/versions/{tableName}/{version} | DELETE | |
| /v1/fields/recon/{version} | PUT | |
| ***Validation Rule*** | /v1/validationRules/entities/{entity} | PUT | |
| /v1/validationRules/entities/{entity}/fields/{field} | PUT | |
| /v1/validationRules/entities | PUT | |
| /rule/v1/validationRules/entities/{entity}/validate | POST | |
| /rule/v1/validationRules/entities/{entity}/fields/{field} | DELETE | |

- ***BAU Suppression Service API***

| API Group | API Endpoint | Method | Remark |
| --- | --- | --- | --- |
| Suppression Rule | /v1/suppressions/rules | GET | |
| /v1/suppressions/criteria | GET | |
| /v1/suppressions/rules | POST | |
| /v1/suppressions/rules/{id}/status | PUT | |
| /v1/suppressions/rules/{id}/approve | PUT | |
| /v1/suppressions/rules/histories | GET | |
| ***Validation Rule*** | | | |
| ***Fields*** | | | Same as CN rule |
| ***Data Entitlement*** | | | Out of scope |

- ***RATANONE-RULE-SERVICE API***

Please refer to ***[Rule Service Tech Design - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/Rule+Service+Tech+Design#RuleServiceTechDesign-2.4APIDesign).***

***Questions:***

1. Can the new Rule Service API meet the CN requirements? If not, please raise the ticket to list out what API do you want to add.

*Schedule the weekly meeting to sync up the rule migration.*

# 5. UI

As all of rule services will be merged to one component, the changes applied to API layer that have impact on the interaction between frontend and backend services. Therefore, we need to find out what we need to change accordingly during the rule migration.

***Questions:***

1. Estimate the efforts of UI changes.