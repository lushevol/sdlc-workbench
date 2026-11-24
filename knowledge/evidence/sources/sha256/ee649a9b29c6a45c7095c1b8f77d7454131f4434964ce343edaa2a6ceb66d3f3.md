# 1 Rule types in CN rule service

All the rules are stored in the ***ratan_rule_service.ratan_rule ***table. The below table shows the type of rules in CN.

| Rule Name | Business Workflow | Rule Type | Rule Status | Comment |
| --- | --- | --- | --- | --- |
| IRS Rule | n/a | IRS | ADD_CONFIRMED DEL_PENDING | - Skip the rule checking if *Cashflow.Is_Cashflow_SettleAsGross* is true. - Call the remote service called ***CashflowService ***to determine if the cashflow is resultant released. |
| Suppression Rule | SETTLEMENT | SUPPRESSION | ADD_CONFIRMED DEL_PENDING | - Skip the rule checking if *Cashflow.Is_Cashflow_Unsuppress* is true. - The rest is same as the *ratanone_suppression_service *does. |
| Swift Suppression Rule | SETTLEMENT | SWIFT_SUPPRESSION | ADD_CONFIRMED DEL_PENDING | - Skip the rule checking if *Cashflow.Is_Cashflow_Swift_Unsuppress* is true. - The rest is same as the *ratanone_suppression_service *does. |
| Netting Rule | n/a | Netting | ADD_CONFIRMED DEL_PENDING | - Skip rule checking if *Cashflow.Is_Cashflow_SettleAsGross* is true. |
| *NSTP Rule* | SETTLEMENT | NSTP | ADD_CONFIRMED DEL_PENDING | - Two types of NSTP rule, one is common rule, the other is the special rule that will call the thirty-party service to determine whether the rule is matched. - Generated the exception according to the *operation_level*, *exception_code*, *exception_category*. |

Problem statement: Load the rules from cache instead of database to improve the performance.

Proposed:

- If loading the rules from cache, we shall ensure the data consistency between database (PG) and cache (Redis).
- Load priority as it seems to me that this is not the performance bottleneck issue.
- Use the design pattern such as strategy pattern to refactor and allows that the rules can be easily load the rules from somewhere else rather than database in the future.

# 2 Table Design (AS-IS)

As mentioned above, CN rule service use the table ***ratan_rule_service.ratan_rule ***to replace the table ***ratanone.ratan_suppression_rule ***to store all the rules. Compare these two tables, some additional columns have been added for handling the special rules, while some other columns have been removed for unknown reasons.

- Columns added in table ***ratan_rule_service.ratan_rule***: *created_by, updated_by*, operation_level, exception_code and exception_category.
- Cloumns removed from table ***ratanone.ratan_suppression_rule******: **creator, last_modifier, approver,* approve_time, hierarchy and value_date.

Duplicate columns** ***operation_level, exception_code and exception_category* both in the Table ***ratan_rule_service.ratan_rule*** and ***ratan_rule_service.ratan_rule_exception***.

Column *operation_level* is defined by the type of exception or something else?

Table ***ratan_rule_service.ratan_special_rule_config ***store the configuration for special rules which includes *business_workflow, rule_type, exception_code, exception_category, operation_level and **processor**.*

# 3 Parallel execution for checking rules

The current checking rule execution model is shown as below:

Potential weaknesses

- As some special rules will call the third-party services to retrieve the data, then determine if the rules are hit. Therefore, the performance is also subject to the third-party services' capacity.
- Thread pool settings, performance testing is a good way to fine tuning thread pool configuration: - Core size, max size and block queue size: should consider scaling out the instances when come across the performance issues. - Rejection policy: the default is aborted policy, suggest changing to caller runs policy instead.
- If some rules matched, the corresponding exceptions will be generated and persist in the database, and then publish these exceptions info to the specified Kafka topic, but it seems that we haven't take account into the case that success to insert the data into database but fail to send the message to Kafka. As for this case, please refer to* [Microservice Transactional Outbox pattern](https://microservices.io/patterns/data/transactional-outbox.html)*.

Unfortunately, Drools doesn't support the in-parallel rule match algorithm, as it is based on the Rete rule match algorithm which is the sequential execution algorithm. However, we can prepare the data in parallel mode because retrieving the data remotely is a time-consuming activity.

# 4 The Scope of PoC

NSTP rule implement based on Drools.