#### Cashflow data provider query API sequence diagram.

#### Cashflow data record size calculates.

**UAT env:**

| SELECT count(*) FROM cashflow_data | 439668 (num) |
| --- | --- |
| SELECT pg_relation_size('cashflow_data') | 473743360 (Byte) |
| One record size of "cashflow_data" in DB = 473743360 / 439668 = 1077 (Byte) = **1KB** |

| API call "/v1/data/provider/query/cashflows" | Payload size |
| --- | --- |
| {"queryCondition": "Select * from cash_settlement_query_cn.cashflow_data LIMIT 1 OFFSET 0"} | 10.11KB |
| {"queryCondition": "Select * from cash_settlement_query_cn.cashflow_data LIMIT 100 OFFSET 0"} | 941.29KB |
| One record size of "cashflow_data" in response payload = **9.4KB** |

So actually, payload data size is much bigger, perhaps due to the long name of each field.

| Records | 10k | 30k | 100k | 1200k |
| --- | --- | --- | --- | --- |
| DB data size | 10M | 30M | 100M | 1.2G |
| Payload data size | 94M | 275M | 940M | 10.74G |

**Issue**:

Call data provider API for 8 times, each request fetch 30K records cause OOM.

**OOM analyze:**

Problem:

1. How to mitigate OOM?
2. How to reduce response time?

#### Solution A

Since the SSDR may call data provider API many times, maybe we can prepare the processed "Cashflow data" into a report table (cashflow_data_report) in advance. (Daily or Hourly)

This solution can save time cost and duplicate work of DB query and internal API call when user call our data provider API.

**How to accelerate the data transmission ?**

Since large amount of data remain in Application server may cause OOM, then query cashflow data by slices and write each slice into a json report file and compress.

When the writing report files done, then read each zipped json file and send to SSDR via gRPC stream.  SSDR should expose an endpoint for receiving the stream of files and extract them.

#### Solution B

1. DQSL as gRPC server, expose a gRPC server port.
2. Cashflow query service as a gRPC client.

**Note**: The Cashflow query service could response "Received" soon after receiving the request, but the file sending can continue at the background.

#### Solution C

1. DQSL as gRPC client.
2. Cashflow query service as a gRPC server.

**Note**: The Cashflow query service could response "Received" soon after receiving the request, but the file sending can continue at the background.

#### Solution D

1. DQSL client no need any modifications;
2. Cashflow query service loop query cashflow data, and response each query result with stream bytes base on Spring WebMvc feature of StreamingResponseBody.

Benefits:

1. No big query data set remain in Mem.
2. No big data file remain in Disk.
3. No trigger Circuit Breaker timeout setting.

Defects:

1. Loop query may take longer time than once query, due to multiple calls to PG.

#### Questions

1. What's the scenario of the request from SSDR users? What's the concurrency?
2. How to split the big volume of the request, by Day or Number?
3. How often does the cashflow data change?
4. Can we return the same report data in a scope of period? If so, we can store data to file to avoid duplicate query for resource saving.
5. If there's a file server to store the report data? If no, then use the VM disk to store files. But may delete / archive them after files sent.

#### Comparation for several solutions:

| The way of DQSL request/response | Procedure | Conditions | Benefits | Defects |
| --- | --- | --- | --- | --- |
| 1. req: HTTP RESTful 2. res: Json data | 1. DQSL split the big volume request into small Volume request. 2. Ratan query service response Json data to DQSL. | 1. Need install SDK to DQSL | 1. No Large volume remain in query service, relief Mem occupation in query service. | 1. Each response volume is still big. |
| 1. req: HTTP RESTful 2. res: gzipped Json data | 1. DQSL split the big Volume request into small Volume request. 2. Ratan query service 1. Write query resulst into files and gzip. 2. Response gzipped Json data to DQSL. | 1. Need install SDK to DQSL | 1. Same above. 2. Save time cost of transferring via gzip. | 1. Need disk to store files and delete. |
| 1. req: RESTful API 2. res: gRPC binary | 1. DQSL keep original request. 2. Ratan query service 1. Response "Received". 2. Split big query into small query and save results into files and zip. 3. Read each file and return gRPC binary to DQSL. | 1. Need install SDK into DQSL 2. DQSL play as a gRPC server. 3. Ratan query service play as a gRPC client. | 1. Response with small binary chunks, so Mem occupation can be much smaller. 2. Base on HTTP 2.0 which can improve transfer efficiency. | 1. Need DQSL open a gRPC server port. |
| 1. req: gRPC client request 2. res: gRPC binary | 1. DQSL send gRPC request. 2. Ratan query service 1. Response "Received". 2. Split big query into small query and save result into files. 3. Read each file and return gRPC binary to DQSL. | 1. Need install SDK into DQSL 2. Ratan query service play as a gRPC server. 3. DQSL play as a gRPC client. | same above. | 1. gRPC client request from DQSL need AA in Ratan API Gateway. 2. Ratan API Gateway need support both Http2 and Http1.1. |

### **Conclusion:**

Prefer solution D.

It can:

1. Support as least 120w volume query with QPS > 5;
2. Almost no OOM issue;