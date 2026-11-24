- Ref

[SQL performance using bitmap - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/SQL+performance+using+bitmap)

[SQL performance in different condition - Derivative Strategy Projects - Confluence (standardchartered.com)](https://confluence.global.standardchartered.com/display/DSP/SQL+performance++in+different+condition)

Slow query category from kibana:

```
1、multi condition with 'not in' query:
 explain analyse
 select
       *
    from
        cash_settlement_query_cn.cashflow_data cfd1_0
    where
         jsonb_extract_path_text(cfd1_0.cashflow, 'Entity', 'Booking_Entity_SCI_FMID') = '10075222'
   and 
  (
            jsonb_extract_path_text(cfd1_0.cashflow, 'Cashflow', 'Cashflow_State')  not in ('READY','RELEASED','SETTLED','CASHFLOW_SUPPRESSED','SWIFT_SUPPRESSED','CANCELLED','ERROR','DEAD','FAILED','NETTED', 'NOSTROMATCH')
            or jsonb_extract_path_text(cfd1_0.cashflow, 'Cashflow', 'Cashflow_State') is null
        )
        and jsonb_extract_path_text(cfd1_0.cashflow, 'Cashflow', 'Is_Commodity')='false'
        and (
            jsonb_extract_path_text(cfd1_0.cashflow, 'Entity', 'Counterparty_SCI_FMID')  not in ('40083122', '10037537')
            or jsonb_extract_path_text(cfd1_0.cashflow, 'Entity', 'Counterparty_SCI_FMID') is null
        )
        and (
            jsonb_extract_path_text(cfd1_0.cashflow, 'Instrument_Common', 'Murex_Product_Typology') not in ('STL-Cust', 'NDF')
            or jsonb_extract_path_text(cfd1_0.cashflow, 'Instrument_Common', 'Murex_Product_Typology') is null
        )
        and (
            jsonb_extract_path_text(cfd1_0.cashflow, 'Instrument_Common', 'ISDA_Taxonomy') not in ('Credit:Loans:TermLoan')
            or jsonb_extract_path_text(cfd1_0.cashflow, 'Instrument_Common', 'ISDA_Taxonomy') is null
        )
  
    order by
         cfd1_0.created_at desc
    offset
        0 rows
    fetch
        first 1000 rows only

2、muliti condition using index query:
 explain analyse
 select
    *
     from
        cash_settlement_query_cn.cashflow_data cfd1_0
    where
         jsonb_extract_path_text(cfd1_0.cashflow, 'Entity', 'Booking_Entity_SCI_FMID')='10075222' 
   and
         jsonb_extract_path_text(cfd1_0.cashflow, 'Cashflow', 'Payment_Date') between ('2025-04-01') and ('2025-05-07') 
   and
         jsonb_extract_path_text(cfd1_0.cashflow, 'Instrument_Common', 'ISDA_Taxonomy')='InterestRate:IRSwap:FixedFloat'
   order by
         cfd1_0.created_at desc
    offset
        0 rows
    fetch
        first 1000 rows only

3、signle condition query:
 explain analyse
 select
       *
    from
        cash_settlement_query_cn.cashflow_data cfd1_0
    where
   jsonb_extract_path_text(cfd1_0.cashflow, 'Entity', 'Booking_Entity_SCI_FMID') = '10075222'  
    order by
         cfd1_0.created_at desc
    offset
        0 rows
    fetch
        first 1000 rows only
  
4、sigle condition range query:
 explain analyse
 select
       *
  from
        cash_settlement_query_cn.cashflow_data cfd1_0
    where
        jsonb_extract_path_text(cfd1_0.cashflow, 'Cashflow', 'Payment_Date') between ('2025-04-01') and ('2025-05-07')
    order by
        cfd1_0.created_at desc
    offset
        0 rows
    fetch
        first 1000 rows only
 

 #1，Translate 'not in' to 'in' will go to #2
 #2，Bitmap scan in lossy model ref: https://confluence.global.standardchartered.com/display/DSP/SQL+performance+with+daily+database
 #3，In actual, the SQL is fast. not issue with SQL.
 #4，Only exists in some special date in staging environment. Replace the order by column with one of the condition index column.
 
```

**Some common conclusion:**

**a. Using index column in where condition as more as better, PostgreSQL will calculate and choose the best execute plan.**

**b. Multi condition query will use bitmap scan, if the bitmap gets too large it will be convert to "lossy" style. Increase work_mem setting can speed up performance.(up to 30MB in Ratan business)**

**c. Using one of the WHERE conditions on index column for ORDER BY clause can obviously speed up performance.**

**d. Immutable function can not be used by index. to_number（jsonb_extract_path_text（xxx,xxx,xxx））can not use the jsonb_extract_path_text() index because the mismatch pattern.**

**e. Conditions use on index column will be applied to Index Cond  operation, which will reduce the fetch rows and speed up performance, but conditions do not use index column will be applied to Filter operation which will fetch more data and have to filter the rows that not meet the condition, that will obviously slow down performance.**

data distribution by create date in daily db:
![image-2025-5-21_9-42-34.png](attachments/image-2025-5-21_9-42-34.png)

data distribution by payment date in daily db:
![image-2025-5-21_10-19-44.png](attachments/image-2025-5-21_10-19-44.png)
![image-2025-5-21_10-19-2.png](attachments/image-2025-5-21_10-19-2.png)
![image-2025-5-21_10-17-49.png](attachments/image-2025-5-21_10-17-49.png)