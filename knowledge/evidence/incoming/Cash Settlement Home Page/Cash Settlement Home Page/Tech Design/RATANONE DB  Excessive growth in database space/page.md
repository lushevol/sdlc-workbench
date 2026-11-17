table list:

| schema_name | table_name | Size (MB) | Checker | House keeping Logic |
| --- | --- | --- | --- | --- |
| ratanone | act_hi_detail | 344625 | [@Yang3, Chen](mailto:Chen.Yang3@sc.com) | truncate first time, truncate every one month after |
| ratanone | event_record | 266549 | | |
| ratanone | act_hi_varinst | 135739 | [@Yang3, Chen](mailto:Chen.Yang3@sc.com) | truncate first time, truncate every one month after |
| ratanone | event_history | 126773 | | |
| ratanone | act_hi_actinst | 93896 | [@Yang3, Chen](mailto:Chen.Yang3@sc.com) | truncate first time, truncate every one month after |
| ratan_cashflow_group_management_service | ratan_cashflow_message_io | 87643 | [@Huang, Caroline Xinmiao](mailto:CarolineXinmiao.Huang@sc.com) | Keep 1 month data for trouble shooting |
| ratanone | act_ge_bytearray | 62591 | [@Yang3, Chen](mailto:Chen.Yang3@sc.com) | Not required at present |
| cash_settlement_lms_service | lms_raw_message | 52760 | [@Yang3, Chen](mailto:Chen.Yang3@sc.com) | created_at is over 90 days |
| cash_settlement_query_cn | cashflow_data_history | 42947 | [@Huang, Caroline Xinmiao](mailto:CarolineXinmiao.Huang@sc.com) | Option 1: Keep all Option 2: Settlement date has expired more than 1 year from now TBC whether need a archived table for historical data query |
| ratan_cashflow_lifecycle_service | ratanone_cashflow_service__cqrs_cashflow_events | 38243 | [@Huang, Caroline Xinmiao](mailto:CarolineXinmiao.Huang@sc.com) | Option 1: Clean up all event by settlement date has expired more than 1 year from now Option 2: Keep latest event for each payment only each option need condition status = 'SENT' |
| ratan_cashflow_group_management_service | ratan_cashflow_group_message_history | 30789 | [@Huang, Caroline Xinmiao](mailto:CarolineXinmiao.Huang@sc.com) | Keep 1 month data for trouble shooting |
| ratanone_rule_service | dry_run_record | 26313 | [@Cheng, Ben](mailto:Ben.Cheng@sc.com)[@Wang, Nick Long](mailto:NickLong.Wang@sc.com) | |
| ratanone | lms_raw_message | 20505 | ~~Yang Chen~~ | BAU related table |
| cash_settlement_query_cn | cashflow_data | 10678 | [@Huang, Caroline Xinmiao](mailto:CarolineXinmiao.Huang@sc.com) | Option 1: Keep all Option 2: Settlement date has expired more than 1 year from now TBC whether need a archived table for historical data query |
| ratanone | act_ru_variable | 10102 | [@Yang3, Chen](mailto:Chen.Yang3@sc.com) | Not required at present |