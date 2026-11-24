### No "payment date" scope:

| Cashflow State | Count | Time(s) | If added Index for "created_at" Time(s) |
| --- | --- | --- | --- |
| NOT IN (DEAD, NETTED) **Current default** | 445240 | 11.87 | 6.11 |
| WAITING | 68867 | 11.04 | 6 |
| READY | 93 | 0.376 | 0.353 |
| QUEUED | 18422 | 1.12 | 1.12 |
| IN (WAITING, READY, QUEUED) | 87382 | 11.32 | 5.92 |

**SQL statement for above:**

```sql
SELECT * FROM cashflow_data where jsonb_extract_path_text(cashflow, 'Cashflow', 'Cashflow_State') not in ('DEAD','NETTED') order by created_at desc limit 500;
SELECT * FROM cashflow_data where jsonb_extract_path_text(cashflow, 'Cashflow', 'Cashflow_State') = 'WAITING' order by created_at desc limit 500;
SELECT * FROM cashflow_data where jsonb_extract_path_text(cashflow, 'Cashflow', 'Cashflow_State') = 'READY' order by created_at desc limit 500;
SELECT * FROM cashflow_data where jsonb_extract_path_text(cashflow, 'Cashflow', 'Cashflow_State') = 'QUEUED' order by created_at desc limit 500;
SELECT * FROM cashflow_data where jsonb_extract_path_text(cashflow, 'Cashflow', 'Cashflow_State') in ('WAITING', 'READY', 'QUEUED') order by created_at desc limit 500;
```

Added time scope for "payment date" and created Indexes for "created at":

| Cashflow State | payment date within 1 month | payment date within 0.5 month |
| --- | --- | --- |
| **Count** | **Time(s)** | **Count** | **Time(s)** |
| NOT IN (DEAD, NETTED) **Current default** | 46146 | 10.11 | 19944 | 1.96 |
| WAITING | 29069 | 1.70 | 8114 | 1.05 |
| READY | 7 | 0.356 | 7 | 0.351 |
| QUEUED | 3784 | 1.01 | 1998 | 0.96 |
| IN (WAITING, READY, QUEUED) | 32860 | 1.56 | 10119 | 1.48 |

| Cashflow State | payment date within last 7 days |
| --- | --- |
| **Count** | **Time(s)** |
| IN (NETTED, DEAD, CANCELLED, SETTLED) | 1070 | 1.17 |

**SQL statement for above:**

```sql
SELECT * FROM cashflow_data where jsonb_extract_path_text(cashflow, 'Cashflow', 'Cashflow_State') not in ('DEAD','NETTED') and jsonb_extract_path_text(cashflow, 'Cashflow', 'Payment_Date') between '2024-05-22' and '2024-06-06' order by created_at desc limit 500;
SELECT * FROM cashflow_data where jsonb_extract_path_text(cashflow, 'Cashflow', 'Cashflow_State') = 'WAITING' and jsonb_extract_path_text(cashflow, 'Cashflow', 'Payment_Date') between '2024-05-22' and '2024-06-06' order by created_at desc limit 500;
SELECT * FROM cashflow_data where jsonb_extract_path_text(cashflow, 'Cashflow', 'Cashflow_State') = 'READY' and jsonb_extract_path_text(cashflow, 'Cashflow', 'Payment_Date') between '2024-05-22' and '2024-06-06' order by created_at desc limit 500;
SELECT * FROM cashflow_data where jsonb_extract_path_text(cashflow, 'Cashflow', 'Cashflow_State') = 'QUEUED' and jsonb_extract_path_text(cashflow, 'Cashflow', 'Payment_Date') between '2024-05-22' and '2024-06-06' order by created_at desc limit 500;
SELECT * FROM cashflow_data where jsonb_extract_path_text(cashflow, 'Cashflow', 'Cashflow_State') in ('WAITING', 'READY', 'QUEUED') and jsonb_extract_path_text(cashflow, 'Cashflow', 'Payment_Date') between '2024-05-22' and '2024-06-06' order by created_at desc limit 500;
 
 
SELECT * FROM cashflow_data where jsonb_extract_path_text(cashflow, 'Cashflow', 'Cashflow_State') in ('NETTED', 'DEAD', 'CANCELLED', 'SETTLED') and jsonb_extract_path_text(cashflow, 'Cashflow', 'Payment_Date') between '2024-06-01' and '2024-06-07' order by created_at desc limit 500;
```

### **Conclusion:**

As if we shorten the payment date period, we can save the query latency from >**11s** to <**2s**.