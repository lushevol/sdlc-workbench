- SQL use Index scan but with different ‘work_mem’ value, PT list bellow:

| SQL | work_mem |
| --- | --- |
| 4MB(default) | 10MB | 30MB |
| ``` explain analyse select * from cash_settlement_query_cn.cashflow_data cfd1_0 where jsonb_extract_path_text(cfd1_0.cashflow, 'Entity', 'Booking_Entity_SCI_FMID')='10075222' and jsonb_extract_path_text(cfd1_0.cashflow, 'Cashflow', 'Payment_Date') between ('2025-04-01') and ('2025-05-07') and jsonb_extract_path_text(cfd1_0.cashflow, 'Instrument_Common', 'ISDA_Taxonomy')='InterestRate:IRSwap:FixedFloat' order by cfd1_0.created_at desc offset 0 rows fetch first 1000 rows only ``` | around 15000ms ![image-2025-5-8_14-5-38.png](attachments/image-2025-5-8_14-5-38.png) | around 5000ms ![image-2025-5-8_14-6-16.png](attachments/image-2025-5-8_14-6-16.png) | around 400ms ![image-2025-5-8_14-6-46.png](attachments/image-2025-5-8_14-6-46.png) |
| ``` explain analyse select * from cash_settlement_query_cn.cashflow_data cfd1_0 where ( jsonb_extract_path_text(cfd1_0.cashflow, 'Cashflow', 'Cashflow_State') in ('READY','RELEASED','SETTLED','CASHFLOW_SUPPRESSED','SWIFT_SUPPRESSED','CANCELLED','ERROR','DEAD','FAILED','NETTED') -- or jsonb_extract_path_text(cfd1_0.cashflow, 'Cashflow', 'Cashflow_State') is null ) and jsonb_extract_path_text(cfd1_0.cashflow, 'Cashflow', 'Is_Commodity')='false' and ( jsonb_extract_path_text(cfd1_0.cashflow, 'Entity', 'Counterparty_SCI_FMID') in ('40083122', '10037537') -- or jsonb_extract_path_text(cfd1_0.cashflow, 'Entity', 'Counterparty_SCI_FMID') is null ) and ( jsonb_extract_path_text(cfd1_0.cashflow, 'Instrument_Common', 'Murex_Product_Typology') in ('STL-Cust', 'NDF') -- or jsonb_extract_path_text(cfd1_0.cashflow, 'Instrument_Common', 'Murex_Product_Typology') is null ) and ( jsonb_extract_path_text(cfd1_0.cashflow, 'Instrument_Common', 'ISDA_Taxonomy') in ('Credit:Loans:TermLoan') -- or jsonb_extract_path_text(cfd1_0.cashflow, 'Instrument_Common', 'ISDA_Taxonomy') is null ) and ( jsonb_extract_path_text(cfd1_0.cashflow, 'Entity', 'Counterparty_Client_Type') not in ('INTEBCH', 'INTECOM', 'INTLACC') or jsonb_extract_path_text(cfd1_0.cashflow, 'Entity', 'Counterparty_Client_Type') is null ) and jsonb_extract_path_text(cfd1_0.cashflow, 'Entity', 'Booking_Entity_SCI_FMID')='10075222' order by cfd1_0.created_at desc offset 0 rows fetch first 1000 rows only ``` | around 1600ms ![image-2025-5-8_14-10-3.png](attachments/image-2025-5-8_14-10-3.png) | around 1200ms ![image-2025-5-8_14-8-42.png](attachments/image-2025-5-8_14-8-42.png) | around 400ms ![image-2025-5-8_13-42-8.png](attachments/image-2025-5-8_13-42-8.png) |
| ``` explain analyse select * from cash_settlement_query_cn.cashflow_data cfd1_0 where jsonb_extract_path_text(cfd1_0.cashflow, 'Instrument_Common', 'Murex_Product_Typology')='NDF' and jsonb_extract_path_text(cfd1_0.cashflow, 'Entity', 'Booking_Entity_SCI_FMID') = '10075222' and jsonb_extract_path_text(cfd1_0.cashflow, 'Cashflow', 'Cashflow_State') in ('READY','RELEASED','SETTLED','CASHFLOW_SUPPRESSED','SWIFT_SUPPRESSED','CANCELLED','ERROR','DEAD','FAILED','NETTED', 'NOSTROMATCH') order by cfd1_0.created_at desc offset 0 rows fetch first 1000 rows only ``` | around 30000ms ![image-2025-5-8_14-47-29.png](attachments/image-2025-5-8_14-47-29.png) | around 5000ms ![image-2025-5-8_14-45-51.png](attachments/image-2025-5-8_14-45-51.png) | around 600ms ![image-2025-5-8_14-45-13.png](attachments/image-2025-5-8_14-45-13.png) |

- Conclusion

When using a bitmap index scan (multi condition query) , if the bitmap gets too large, it will be converted to "lossy" style, and need to scan the entire block to find matching rows, also cause a condition recheck. All this will slow down performance.

Increase the work_mem setting to allow PostgreSQL store a large bitmap in memory is a effective way to speed up performance.(according to PT above, work_mem=30M at least.)

- Reference

[PostgreSQL: Re: Bitmap indexes etc.](https://www.postgresql.org/message-id/12553.1135634231@sss.pgh.pa.us)

from chat GTP:

![image-2025-5-8_15-6-23.png](attachments/image-2025-5-8_15-6-23.png)