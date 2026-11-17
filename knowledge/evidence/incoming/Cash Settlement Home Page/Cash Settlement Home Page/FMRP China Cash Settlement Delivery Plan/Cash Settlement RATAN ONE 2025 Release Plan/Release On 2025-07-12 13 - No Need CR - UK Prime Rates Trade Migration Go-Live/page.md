# Release Work Item: N/A.

Note: *Rule: Client clearing Portfolio UK* ready since new trade booking for UK Prime Rates already go-live.

# SQL for Recon

| SQL des. | SQL template | Comment |
| --- | --- | --- |
| Cf Num. in Group Blotter | ```sql select count(distinct cashflow_id) from ratan_cashflow_group_management_service.ratan_cashflow_group_message rcgm where created_at >= '2025-06-21 02:30:33' and (raw_message like '%ECL_EDBKR_UK_STL%' or raw_message like '%ECL_TPBKR_UK_STL%' or raw_message like '%CLIENT_CLRG_LCH_STL%' or raw_message like '%CLIENT_CLR_HKEX_STL%'); ``` | **TBC: created_at >= '2025-06-21 02:30:33'** |
| Export cfs in Group Blotter | ```sql select distinct cashflow_id , trade_id, status , cashflow_seq , cashflow_cnt , cashflow_status from ratan_cashflow_group_management_service.ratan_cashflow_group_message rcgm where created_at >= '2025-06-21 02:30:33' and (raw_message like '%ECL_EDBKR_UK_STL%' or raw_message like '%ECL_TPBKR_UK_STL%' or raw_message like '%CLIENT_CLRG_LCH_STL%' or raw_message like '%CLIENT_CLR_HKEX_STL%') order by trade_id desc; ``` |
| Cf Num. in Cashflow Blotter | ```sql select count(distinct cashflow__cashflow_id) from cash_settlement_query_cn.cashflow_data cd where created_at >= '2025-06-03 02:30:33' and portfolio__booking_entity_trade_portfolio_name in ('ECL_EDBKR_UK_STL','ECL_TPBKR_UK_STL','CLIENT_CLRG_LCH_STL','CLIENT_CLR_HKEX_STL'); ``` |
| Export cfs in Cashflow Blotter | ```sql select cashflow__cashflow_id , trade_id , cashflow_status,cashflow__payment_date, portfolio__booking_entity_trade_portfolio_name from cash_settlement_query_cn.cashflow_data cd where created_at >= '2025-06-03 02:30:33' and portfolio__booking_entity_trade_portfolio_name in ('ECL_EDBKR_UK_STL','ECL_TPBKR_UK_STL','CLIENT_CLRG_LCH_STL','CLIENT_CLR_HKEX_STL'); ``` |

# Recon Result

| No. | Test Scenario | Expected | Actual | Test Result | Comments |
| --- | --- | --- | --- | --- | --- |
| 1 | Total Num of Received Cashflows in Group Blotter | | | | |
| 2 | Total Num of Received Cashflows in Cashflow Blotter | | | | |

| CF_Status | Num. | Comments |
| --- | --- | --- |
| CASHFLOW_SUPPRESSED | | |
| PROJECTED | | |
| QUEUED | | |
| Total | | |