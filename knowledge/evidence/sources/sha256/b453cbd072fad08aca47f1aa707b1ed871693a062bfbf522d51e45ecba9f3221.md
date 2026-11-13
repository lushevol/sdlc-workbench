## Migration Flow

## Need to be migrated table

| Table | Related Filed | Prod count - 08/27 | Size |
| --- | --- | --- | --- |
| cash_netting_service.**ratan_auto_netting_cashflow** | Cashflow_id | 0 | |
| cash_netting_service.**ratan_auto_netting_cashflow_history** | Cashflow_id **(no index)** | 0 | |
| cash_netting_service.**splitting_cashflow** | Cashflow_id | 9 | 1k * 9 = 9K = 0.01MB |
| cash_netting_service.**t****_cashflow** | cashflow__cashflow_id | 983 | 1k* 983 = 983K = 0.96MB |
| cash_settlement_lms_service.**lms_message** | Cashflow_id/party1_fm_id | 1045 | 1k*1045 = 1045k = 1.02MB |
| cash_settlement_lms_service.**lms_raw_message** | message_key <-> **lms_message****.**aggregate_root_id ? | 156 | 3k * 156 = 468k = 0.46MB |
| cash_settlement_query_cn.**cashflow_data** | Cashflow__cashflow_id and entity__booking_entity_sci_fmid = '8' | 2293 | 22k * 2293 = 50446K = 49.26MB |
| cash_settlement_query_cn.**cashflow_data_history** | Cashflow__cashflow_id | 78950 | 1k * 78950 = 78950k = 77.10MB |
| cash_settlement_ssi_cn.**cashflow_stamping** | Cashflow_id/party1_fm_id | 5382 | 1k * 5382 = 5382K = 5.26MB |
| cash_settlement_ssi_cn.**cashflow_stamping_legacy_exception** | Cashflow_id | 9562 | 1k * 9562 = 9562K = 9.34MB |
| cash_settlement_ssi_cn.**maker_checker_request** | Cashflow_id | 111 | 6k * 111 = 666k = 0.65MB |
| ~~cash_settlement_ssi_cn.**raw_message**~~ | message_key(cashflow_id) ？ **(no index)** | 18970 | 49k * 18970 = 929530K = 907.74MB |
| cash_settlement_ssi_cn.**stamped_nostro_account** | cashflow_stamping_id(cashflow_id) | 5383 | 1k * 5383 = 5383K = 5.25MB |
| cash_settlement_ssi_cn.**stamped_vostro_account** | cashflow_stamping_id(cashflow_id) | 5149 | 4k * 5149 = 20596K = 20.11MB |
| cash_settlement_ssi_cn.**stamping_outbox_events ?** | | | |
| ratan_cash_accounting_service.**ratan_accounting_message** | task_id <-> **ratan_accounting_request_task.id** | 0 | |
| ratan_cash_accounting_service.**ratan_accounting_request_task** | cashflow_id/booking_entity_fmid | 4385 | 3k * 4385 = 13155K = 12.85MB |
| ratan_cash_accounting_service.**ratan_accounting_request_task_history** | cashflow_id/booking_entity_fmid | 17462 | 3k * 17462 = 52386K = 51.16MB |
| ratan_cash_accounting_service.**ratan_accounting_response_info** | external_system_key <-> **ratan_accounting_request_task****.**external_system_key | 4385 | 1k * 4385 = 4385K = 4.28MB |
| ratan_cash_settlement_batch_service.**cash_mxg_batch_fix_notify** | flow_id(cashflow_id) | 351 | 1k * 351 = 351K = 0.34MB |
| ratan_cashflow_group_management_service.**ratan_cashflow_group** | trade_id | 4151 | 1k * 4151 = 4151K = 4.05MB |
| ratan_cashflow_group_management_service**.****ratan_cashflow_group_history** | trade_id | 17935 | 1k * 17935 = 17935K = 17.51MB |
| ratan_cashflow_group_management_service**.****ratan_cashflow_group_message** | cashflow_id/booking_entity_id | 6244 | 16k * 6244 = 99904K = 97.56MB |
| ratan_cashflow_group_management_service.**ratan_cashflow_group_message_history** | cashflow_id/booking_entity_id | 4555 | 1k * 4555 = 4555K = 4.45MB |
| ratan_cashflow_group_management_service.**ratan_cashflow_mapping** | Original_cashflow_id | 6 | 1k |
| ratan_cashflow_group_management_service.**ratan_cashflow_mapping****_history** | Mapping_id/Original_cashflow_id | 6 | 1k |
| ratan_cashflow_group_management_service**.ratan_cashflow_status_sync_up_blocking_queue ** | | 20 | |
| ratan_cashflow_group_management_service.**ratan_inbound_message** | | 322 | |
| ratan_cashflow_group_management_service.**ratan_trade** | trade_id | 1367 | 1k * 1367 = 1367K = 1.33MB |
| ratan_cashflow_group_management_service.**ratan_trade_history** | trade_id | 3051 | 1k * 3051 = 3051K = 2.98MB |
| ratan_cashflow_lifecycle_service.**ratan_cashflow_affirmation_status** | cashflow_id | 731 | 1k * 731 = 731K = 0.71MB |
| ratan_cashflow_lifecycle_service.**ratan_cashflow_holding_message** | cashflow_id | 7317 | 1k * 7317 = 7317K = 7.15MB |
| ratan_cashflow_lifecycle_service.**ratan_cashflow_scbml_history** | cashflow_id | 79012 | 1k * 79012 = 79012K = 77.16MB |
| ratan_cashflow_lifecycle_service.**ratan_cashflow_scbml_message** | Id <-> **ratan_cashflow_scbml_history****.**body_event_rowkey | 5810 | 16k * 5810 = 92960K = 90.78MB |
| ratan_cashflow_lifecycle_service.**ratan_stella_message_event_source** | cashflow_id/entity_fmid | 6386 | 1k * 6386 = 6386K = 6.24MB |
| ratan_exception_platform.**rep_exception** | entity_id(cashflow_id) ？ | 16229 | 1k * 16229 = 16229K = 15.85MB |
| ratan_exception_platform.**rep_exception_history** | entity_id(cashflow_id) ？ | 28567 | 1k * 28567 = 28567K = 27.90 |
| ratan_rule_service.**ratan_rule_exception** | | 7094 | |
| ratan_rule_service.**ratan_rule_exception_action_metadata** | | 510 | |
| ratanone_swift_service.**ratanone_holding_mx_cashflow** | | 0 | |
| ratanone_swift_service.**ratanone_swift_conversion_record** | cashflow_data(cashflow_id) | 2237 | 5k * 2237 = 11185K = 10.92MB |
| ratanone_swift_service**.****swift_message** | cashflow_id | 4208 | 1k * 4208 = 4208K = 4.11MB |
| ratanone_swift_service.**swift_raw_message** | cashflow_id | 12633 | 5k * 12633 = 63165K = 61.68MB |
| | | | |

Estimated size total: **1576MB = 1.54GB**

PT

table: cash_settlement_query_cn.cashflow_data

count: 125000 size: 2.56GB zip size: 47MB

export to csv cost: 1 min

import from csv to DB cost: 2 mins

## Migration shell

[Pull requests - Repos](https://dev.azure.com/sc-ado/FMQPR/_git/51358-ratanone-ansible/pullrequestcreate?sourceRef=feature/indonesia_data_migration&targetRef=main&sourceRepositoryId=022df49f-6906-4549-ab9d-1d281d34660b&targetRepositoryId=022df49f-6906-4549-ab9d-1d281d34660b)