## VM Setups:

| Enviroment | OS | CPU | Mem |
| --- | --- | --- | --- |
| UAT hostname: uklvadapp1341 | RedHat_8.9 x86_64 | Intel(R) Xeon(R) Gold 6152 CPU @ 2.10GHz 16 cores | Total: 125G Used: 62.77G |

## Once query ( V1 ):

```sql
curl -k -i -s -H 'Content-Type: application/json' -XPOST 'https://10.198.199.161:9006/v1/data/provider/query/cashflows' -d '{"queryCondition": "Select Cashflow.Cashflow_Id, Cashflow.Audit, * from cash_settlement_query_cn.cashflow_data LIMIT ${VOLUME_AMOUNT} OFFSET 0"}'
```

| Query Volume | Number | Time (s) | JVM Mem | Mem usage | Comment |
| --- | --- | --- | --- | --- | --- |
| 300k | 1 | 1 | -Xms**1024m** -Xmx**4096m** -XX:MaxMetaspaceSize=**256m** | ![Picture3.png](attachments/Picture3.png) | **OOM** |
| 300k | 3 | 1 | -Xms**1024m** -Xmx**8192m** -XX:MaxMetaspaceSize=**256m** | ![Picture4.png](attachments/Picture4.png) | **OOM** |
| 300k | 5 | 1 | -Xms**10240m** -Xmx**12288m** -XX:MaxMetaspaceSize=**256m** | ![image2024-6-26_21-35-49.png](attachments/image2024-6-26_21-35-49.png) | **OOM** |

## Loop query ( V2 Draft ):

```sql
curl -k -i -s -H 'Content-Type: application/json' -XPOST 'https://10.198.199.161:9006/v2/data/provider/query/cashflows/loop' -d '{"queryCondition": "Select Cashflow.Cashflow_Id, Cashflow.Audit, * from cash_settlement_query_cn.cashflow_data LIMIT ${VOLUME_AMOUNT} OFFSET 0"}'
```

1. #### By 10k each;
2. #### Collect each loop result json data list into one big data list.
3. #### Response with the big data list.

| Query Volume | Number | Time (s) | JVM Mem | One Query time (s) | Mem usage | Comment |
| --- | --- | --- | --- | --- | --- | --- |
| 300k | 1 | 1 | -Xms**1024m** -Xmx**4096m** -XX:MaxMetaspaceSize=**256m** | | ![Picture5.png](attachments/Picture5.png) | Close to max JVM Mem |
| 300k | 3 | 1 | -Xms**1024m** -Xmx**8192m** -XX:MaxMetaspaceSize=**256m** | 192 | ![image2024-6-26_13-22-39.png](attachments/image2024-6-26_13-22-39.png) | Close to max JVM Mem |
| 300k | 5 | 1 | -Xms**1024m** -Xmx**8192m** -XX:MaxMetaspaceSize=**256m** | | ![Picture6.png](attachments/Picture6.png) | **OOM** |
| 300k | 3 | 1 | -Xms**10240m** -Xmx**12288m** -XX:MaxMetaspaceSize=**256m** | 86 | ![image2024-6-27_14-25-44.png](attachments/image2024-6-27_14-25-44.png) | Close to max JVM Mem |
| 300k | 5 | 1 | -Xms**10240m** -Xmx**12288m** -XX:MaxMetaspaceSize=**256m** | 108 | ![image2024-6-27_14-15-33.png](attachments/image2024-6-27_14-15-33.png) | **OOM** |
| 300k | 10 | 2 | -Xms**10240m** -Xmx**12288m** -XX:MaxMetaspaceSize=**256m** | 395 | ![image2024-6-26_22-28-3.png](attachments/image2024-6-26_22-28-3.png) ![image2024-6-26_22-27-21.png](attachments/image2024-6-26_22-27-21.png) Resize maximum connection pool to 30, then: ![image2024-6-27_13-31-53.png](attachments/image2024-6-27_13-31-53.png) | Maximum pool size=10 1. JDBC connection **timeout**; 2. **Failed **to obtain JDBC Connection. Maximum pool size=30 1. **OOM** |

## Loop query ( V2 Final ):

```sql
curl -k -i -s -H 'Content-Type: application/json' -XPOST 'https://10.198.199.161:9006/v2/data/provider/query/cashflows/loop' -d '{"queryCondition": "Select Cashflow.Cashflow_Id, Cashflow.Audit, * from cash_settlement_query_cn.cashflow_data LIMIT ${VOLUME_AMOUNT} OFFSET 0"}'
```

1. #### By 5k each;
2. #### Transform result json data list into bytes;
3. #### Response iteratively with bytes via streaming feature of SpirngMVC.

**JVM Mem:  **-Xms**10240m** -Xmx**12288m** -XX:MaxMetaspaceSize=**256m**

| Query Volume | Number | Time (s) | Query method | One Query time (s) | Mem usage | Comment |
| --- | --- | --- | --- | --- | --- | --- |
| 300k | 5 | 1 | | 267 | ![image2024-6-30_9-37-36.png](attachments/image2024-6-30_9-37-36.png) | |
| 500k | 3 | 1 | 1. order by "created_at desc and created_at <= now()" 2. max connection pool = 10 | 391 | ![image2024-8-3_20-33-26.png](attachments/image2024-8-3_20-33-26.png) ![image2024-8-3_20-32-54.png](attachments/image2024-8-3_20-32-54.png) | All success |
| 500k | 5 | 1 | 1. order by "created_at desc and created_at <= now()" 2. max connection pool = 10 | 218 | ![image2024-8-3_17-50-51.png](attachments/image2024-8-3_17-50-51.png) ![image2024-8-3_17-51-46.png](attachments/image2024-8-3_17-51-46.png) | 3 loop query failed to obtain JDBC connections. |
| 500k | 5 | 1 | 1. order by "created_at desc and created_at <= now()" 2. max connection pool = 20 | 197 | ![image2024-8-3_20-3-54.png](attachments/image2024-8-3_20-3-54.png) | All success |
| 500k | 3 | 1 | 1. in cashflow_Ids 2. max connection pool = 10 | 265 | ![image2024-8-3_17-23-21.png](attachments/image2024-8-3_17-23-21.png) ![image2024-8-3_17-22-27.png](attachments/image2024-8-3_17-22-27.png) | All success |
| 500k | 5 | 1 | 1. in cashflow_Ids 2. max connection pool = 10 | 379 | ![image2024-8-3_17-14-1.png](attachments/image2024-8-3_17-14-1.png) ![image2024-8-3_17-9-37.png](attachments/image2024-8-3_17-9-37.png) ![image2024-8-3_17-10-6.png](attachments/image2024-8-3_17-10-6.png) | 2 loop query failed to obtain JDBC connections. |
| 500k | 5 | 1 | 1. in cashflow_Ids 2. max connection pool = 20 | 166 | ![image2024-8-3_18-20-46.png](attachments/image2024-8-3_18-20-46.png) | All success |
| 1200k | 3 | 1 | 1. order by "created_at desc and created_at <= now()" 2. max connection pool = 10 | 3357 | ![image2024-7-30_14-52-4.png](attachments/image2024-7-30_14-52-4.png) ![image2024-7-30_14-50-55.png](attachments/image2024-7-30_14-50-55.png) | |
| 1200k | 3 | 1 | 1. in cashflow_Ids 2. max connection pool = 20 | 320 | ![image2024-8-4_22-50-0.png](attachments/image2024-8-4_22-50-0.png) Success log: ![image2024-8-4_22-49-39.png](attachments/image2024-8-4_22-49-39.png) | |
| 1200k | 5 | 1 | 1. in cashflow_Ids 2. max connection pool = 20 | 334 | ![image2024-8-4_23-0-47.png](attachments/image2024-8-4_23-0-47.png) Success log: ![image2024-8-4_22-59-59.png](attachments/image2024-8-4_22-59-59.png) ![image2024-8-4_22-59-7.png](attachments/image2024-8-4_22-59-7.png) | |