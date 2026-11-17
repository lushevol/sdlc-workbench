- SQL example

According to the actual SQL we use in environment, one example list below.

This topic compare the performance difference  between*** order by cfd1_0.created_at desc*** and*** order by jsonb_extract_path_text(cfd1_0.cashflow, 'Cashflow', 'XXX_Date')  desc*** on different ***where  ***condition.

```sql
explain analyse
select
      cfd1_0.xxxx,
      cfd1_0...
      cfd1_0...
      cfd1_0...,
      cfd1_0.updated_at
    from
        xxx_data cfd1_0
    where
        jsonb_extract_path_text(cfd1_0.cashflow, 'Cashflow', 'Payment_Date') between ('2025-03-19') and ('2025-03-19')
    order by
        cfd1_0.created_at desc
    offset
        0 rows
    fetch
        first 1000 rows only;
```

- Environment

stag_host: [uklvaddbs097.uk.dev.net](http://uklvaddbs097.uk.dev.net)

stag_port: 6524

stag_user: ratanone_stg

stag_database: ratanone_staging

table:  cashflow_data

table data volume(cashflow_data): 1359511

work_mem: 4MB

shared_buffers: 15972MB

- Comparation

**  **Column mark blue is now in use.

** **data volume：3.18(7.7w)、3.19（25w）

**Payment_Date:**

| No. | Where Condition | 2025.3.18~? | 2025.3.19~? |
| --- | --- | --- | --- |
| *** order by*** *** cfd1_0.created_at desc*** | *** order by jsonb_extract_path_text(cfd1_0.cashflow, 'Cashflow', 'Payment_Date') desc*** | ***order by *** ***cfd1_0.created_at desc*** | *** order by *** ***jsonb_extract_path_text(cfd1_0.cashflow, 'Cashflow', 'Payment_Date') desc*** |
| 1 | ``` explain analyse select * from cash_settlement_query_cn.cashflow_data cfd1_0 where jsonb_extract_path_text(cfd1_0.cashflow, 'Cashflow', 'Payment_Date') between ('2025-03-19') and ('2025-03-19') order by jsonb_extract_path_text(cfd1_0.cashflow, 'Cashflow', 'Payment_Date') desc offset 0 rows fetch first 1000 rows only ``` | first time: long time no result follow-up: around 40000ms ![image-2025-4-17_15-47-59.png](attachments/image-2025-4-17_15-47-59.png) | first time: around 1500ms follow-up: around 100ms ![image-2025-4-17_15-49-19.png](attachments/image-2025-4-17_15-49-19.png) | first time: long time no result follow-up: around 20000ms ![image-2025-4-17_16-29-43.png](attachments/image-2025-4-17_16-29-43.png) | first time: around 1100ms follow-up: around 50ms ![image-2025-4-17_15-51-51.png](attachments/image-2025-4-17_15-51-51.png) |
| first time: around 1000ms follow-up: around 800ms ![image-2025-4-21_9-12-56.png](attachments/image-2025-4-21_9-12-56.png) | first time: around 5000ms follow-up: around 50ms ![image-2025-4-22_9-20-4.png](attachments/image-2025-4-22_9-20-4.png) | first time: around 700ms follow-up: around 700ms ![image-2025-4-21_9-14-51.png](attachments/image-2025-4-21_9-14-51.png) | first time: around1000ms follow-up: around 50ms ![image-2025-4-22_9-18-12.png](attachments/image-2025-4-22_9-18-12.png) |
| 2 | ``` explain analyse select * from cash_settlement_query_cn.cashflow_data cfd1_0 where jsonb_extract_path_text(cfd1_0.cashflow, 'Cashflow', 'Payment_Date') between ('2025-03-19') and ('2025-03-25') order by jsonb_extract_path_text(cfd1_0.cashflow, 'Cashflow', 'Payment_Date') desc offset 0 rows fetch first 1000 rows only ``` | first time: around 8000ms follow-up: around 800ms ![image-2025-4-18_11-42-22.png](attachments/image-2025-4-18_11-42-22.png) | first time: around 8000ms follow-up: around 200ms ![image-2025-4-18_14-30-10.png](attachments/image-2025-4-18_14-30-10.png) | first time: around 400ms follow-up: around 300ms ![image-2025-4-18_11-41-22.png](attachments/image-2025-4-18_11-41-22.png) | first time: around 200ms follow-up: around 200ms ![image-2025-4-18_11-40-26.png](attachments/image-2025-4-18_11-40-26.png) |

**Event_Date:**

| No. | Where Condition | 2025.3.18~? | 2025.3.19~? |
| --- | --- | --- | --- |
| *** order by*** *** cfd1_0.created_at desc*** | *** order by jsonb_extract_path_text(cfd1_0.cashflow, 'Cashflow', 'Event_Date') desc*** | ***order by *** ***cfd1_0.created_at desc*** | *** order by *** ***jsonb_extract_path_text(cfd1_0.cashflow, 'Cashflow', 'Event_Date') desc*** |
| 3 | explain analyse select * from cash_settlement_query_cn.cashflow_data cfd1_0 where jsonb_extract_path_text(cfd1_0.cashflow, 'Cashflow', 'Event_Date') between ? and ? ***no index on Event_Date*** | first time: around 18000ms follow-up: around 15000ms ![image-2025-4-18_15-24-9.png](attachments/image-2025-4-18_15-24-9.png) | first time: around 14000ms follow-up: around 14000ms ![image-2025-4-17_17-15-2.png](attachments/image-2025-4-17_17-15-2.png) | first time: around 21000ms follow-up: around 15000ms ![image-2025-4-18_15-25-32.png](attachments/image-2025-4-18_15-25-32.png) | first time: around 14000ms follow-up: around 14000ms ![image-2025-4-17_17-13-35.png](attachments/image-2025-4-17_17-13-35.png) |
| first time: around 600ms follow-up: around 600ms ![image-2025-4-18_15-31-7.png](attachments/image-2025-4-18_15-31-7.png) | first time: around 50000ms follow-up: around 40000ms ![image-2025-4-22_9-44-14.png](attachments/image-2025-4-22_9-44-14.png) | first time: around 600ms follow-up: around 500ms ![image-2025-4-18_15-3-26.png](attachments/image-2025-4-18_15-3-26.png) | first time: around 14000ms follow-up: around 14000ms ![image-2025-4-22_9-55-2.png](attachments/image-2025-4-22_9-55-2.png) |

**Other Type：**

| No. | Where Condition | order by created_at | order by where condition field |
| --- | --- | --- | --- |
| first time: around 50ms follow-up: around 50ms ![image-2025-4-18_14-7-33.png](attachments/image-2025-4-18_14-7-33.png) | first time: around 500ms follow-up: around 100ms ![image-2025-4-18_14-7-42.png](attachments/image-2025-4-18_14-7-42.png) |
| 4 | explain analyse select * from cash_settlement_query_cn.cashflow_data cfd1_0 where to_number(jsonb_extract_path_text (cfd1_0.cashflow, 'Cashflow', 'Payment_Amount'), '99999999999999999.999999')<=10000000::numeric |
| 5 | explain analyse select * from cash_settlement_query_cn.cashflow_data cfd1_0 where ( jsonb_extract_path_text(cfd1_0.cashflow, 'Cashflow', 'Booking_System_Event')<>'' or jsonb_extract_path_text(cfd1_0.cashflow, 'Cashflow', 'Booking_System_Event') is null ) ***no index on Booking_System_Event*** | first time: around 100ms follow-up: around 50ms ![image-2025-4-18_14-9-42.png](attachments/image-2025-4-18_14-9-42.png) | first time: around 40000ms follow-up: around 30000ms ![image-2025-4-18_14-21-2.png](attachments/image-2025-4-18_14-21-2.png) |

**Complex not in condition：**

| No. | Origin SQL | where conditon are all '***not in'*** | where condition are all '***in'*** |
| --- | --- | --- | --- |
| 6 | ``` explain analyse select * from cash_settlement_query_cn.cashflow_data cfd1_0 where ( jsonb_extract_path_text(cfd1_0.cashflow, 'Cashflow', 'Cashflow_State') not in ('READY','RELEASED','SETTLED','CASHFLOW_SUPPRESSED','SWIFT_SUPPRESSED','CANCELLED','ERROR','DEAD','FAILED','NETTED') or jsonb_extract_path_text(cfd1_0.cashflow, 'Cashflow', 'Cashflow_State') is null ) and jsonb_extract_path_text(cfd1_0.cashflow, 'Cashflow', 'Is_Commodity')='false' and ( jsonb_extract_path_text(cfd1_0.cashflow, 'Entity', 'Counterparty_SCI_FMID') not in ('40083122', '10037537') or jsonb_extract_path_text(cfd1_0.cashflow, 'Entity', 'Counterparty_SCI_FMID') is null ) and ( jsonb_extract_path_text(cfd1_0.cashflow, 'Instrument_Common', 'Murex_Product_Typology') not in ('STL-Cust', 'NDF') or jsonb_extract_path_text(cfd1_0.cashflow, 'Instrument_Common', 'Murex_Product_Typology') is null ) and ( jsonb_extract_path_text(cfd1_0.cashflow, 'Instrument_Common', 'ISDA_Taxonomy') not in ('Credit:Loans:TermLoan') or jsonb_extract_path_text(cfd1_0.cashflow, 'Instrument_Common', 'ISDA_Taxonomy') is null ) and ( jsonb_extract_path_text(cfd1_0.cashflow, 'Entity', 'Counterparty_Client_Type') not in ('INTEBCH', 'INTECOM', 'INTLACC') or jsonb_extract_path_text(cfd1_0.cashflow, 'Entity', 'Counterparty_Client_Type') is null ) and jsonb_extract_path_text(cfd1_0.cashflow, 'Entity', 'Booking_Entity_SCI_FMID')='10075222' order by cfd1_0.created_at desc offset 0 rows fetch first 1000 rows only ``` | first time: around 40000ms follow-up: around 30000ms ![image-2025-4-23_16-28-3.png](attachments/image-2025-4-23_16-28-3.png) | first time: around 15000ms follow-up: around 100ms ![image-2025-4-23_16-32-5.png](attachments/image-2025-4-23_16-32-5.png) |
| 7 | ``` explain analyse select * from cash_settlement_query_cn.cashflow_data cfd1_0 where jsonb_extract_path_text(cfd1_0.cashflow, 'Cashflow', 'Cashflow_State') in ('WAITING') and jsonb_extract_path_text(cfd1_0.cashflow, 'Entity', 'Booking_Entity_SCI_FMID') in ('400001378', '10020899') and jsonb_extract_path_text(cfd1_0.cashflow, 'Entity', 'Counterparty_SCI_FMCODE') not in ('SHANGHAI CLE HOU*SHA') -- and jsonb_extract_path_text(cfd1_0.cashflow, 'Cashflow', 'Payment_Date')='2025-03-18' -- and jsonb_extract_path_text(cfd1_0.cashflow, 'Cashflow', 'Cashflow_Sub_State') in ('Pending Operator') order by -- jsonb_extract_path_text(cfd1_0.cashflow, 'Cashflow', 'Payment_Date') desc -- cfd1_0.id desc -- cfd1_0.created_at desc -- jsonb_extract_path_text(cfd1_0.cashflow, 'Entity', 'Counterparty_SCI_FMCODE') -- jsonb_extract_path_text(cfd1_0.cashflow, 'Cashflow', 'Cashflow_State') jsonb_extract_path_text(cfd1_0.cashflow, 'Entity', 'Booking_Entity_SCI_FMID') offset 0 rows fetch first 1000 rows only ``` | first time: around14000ms follow-up: around 2800ms ![image-2025-4-23_16-44-36.png](attachments/image-2025-4-23_16-44-36.png) | first time: around 100ms follow-up: around 100ms ![image-2025-4-23_16-45-1.png](attachments/image-2025-4-23_16-45-1.png) |

- Conclusion

1. In the **Payment_Date** **#1 **where condition** order by *jsonb_extract_path_text(cfd1_0.cashflow, 'Cashflow', 'Payment_Date') desc*** has ***much better*** performance than ***order by cfd1_0.created_at desc.***
2. In the **Payment_Date** **#2 **where condition** order by *jsonb_extract_path_text(cfd1_0.cashflow, 'Cashflow', 'Payment_Date') desc*** has ***almost the same performance to ****** cfd1_0.created_at desc.***
3. In the **Event_Date #3 **where condition** order by *jsonb_extract_path_text(cfd1_0.cashflow, 'Cashflow', 'Event_Date') desc*** has almost the same performance to ***order by cfd1_0.created_at desc.（both are slow. There is no index on Event_Date）***
4. In the **Payment_Date #1** and **Event_Date #3 both 18th and 19th, wide range condition query has a better performance than the small range condition**.
5. In the bad performance situation, the explain analyze result show it scans a big data collection and** removes a lot of rows by the filter**, while in the good performance situation, the analyze result show it scans a more effective data collection and **removes a few rows by the filter**. It seems that **remove by filter is a time consuming action**(**scan rows = rows + rows removed by filter**).
6. According to #6. The more indexed fields used in where clause conditions the better performance it has.
7. According to #7

1、**Where clause has few conditions and order by created_at**, even it uses an index , but  has a bad performance.(no screenshot）

2、**Where clause has few conditions**  and ***order by one of the where condition*** field：

Left screenshot: Even use an index, but is low selective, has a bad performance.

Right screenshot: Change the where clause conditions from 'not in' to 'in' and order by one of the where condition field, it has better performance.

So, there are some conclusion:

Use more index filed in where clause conditions(**change 'not in' to 'in'**)

Try to use one indexed field of where clause conditions in order by clause.

8. Most time it has a good performance in the ***order by cfd1_0.created_at desc ***situation.

9. With the same SQL, multiple executions **have better performance than **first time execution because of the shared buffer hit.

- A few tips from DBA

![image-2025-4-18_11-59-12.png](attachments/image-2025-4-18_11-59-12.png)

- How to Measure Selectivity: Formula: Selectivity = (Number of distinct values) / (Total number of rows) A selectivity closer to 1 indicates a highly selective index.
- [PostgreSQL: Re: Bitmap indexes etc.](https://www.postgresql.org/message-id/12553.1135634231@sss.pgh.pa.us)